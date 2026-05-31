"""Manim Voiceover SpeechService that reuses pre-rendered TTS WAVs.

Background
----------
The current TTS pipeline (Coqui / F5) produces ``manifest.json`` listing
``slide_id`` -> WAV path + per-beat ``start_seconds`` / ``duration_seconds``.
manim-voiceover normally drives its own TTS via :class:`SpeechService`. We
need to reuse the existing WAVs untouched, so this module wraps the manifest
into a ``SpeechService`` that returns the right WAV by ``slide_id`` and
synthesises ``word_boundaries`` from the manifest's beat offsets.

Why bookmarks work without Whisper
----------------------------------
``VoiceoverTracker._process_bookmarks`` interpolates bookmark positions
against ``word_boundaries`` (text_offset -> audio_offset). We seed the
boundary list with one anchor per beat: text_offset = position of
``<bookmark mark='<beat_id>'/>`` in the narration string, audio_offset =
manifest beat ``start_seconds``. Linear interpolation between consecutive
beats is accurate to the frame for our use case (verified in Phase 2 spike).
"""
from __future__ import annotations

import json
import re
import wave
from pathlib import Path
from typing import Any

from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import SpeechService
from manim_voiceover.tracker import AUDIO_OFFSET_RESOLUTION

import manim_voiceover.tracker as voiceover_tracker


BOOKMARK_RE = re.compile(r"(<bookmark\s*mark\s*=['\"]\w+[\"\']\s*/>)")
_BOOKMARK_INNER_RE = re.compile(r"<bookmark\s*mark\s*=['\"](\w+)[\"\']\s*/>")


def wav_duration(path: str | Path) -> float:
    with wave.open(str(path), "rb") as handle:
        return handle.getnframes() / handle.getframerate()


_original_get_duration = voiceover_tracker.get_duration


def get_duration_any(path: str | Path) -> float:
    p = Path(path)
    if p.suffix.lower() == ".wav":
        return wav_duration(p)
    return _original_get_duration(p)


# Patch manim-voiceover so its tracker can read .wav durations without
# pulling in pydub (which expects an installed ffmpeg in PATH).
voiceover_tracker.get_duration = get_duration_any


def bookmark_offsets(text: str) -> dict[str, int]:
    """Return mark -> text_offset (in the bookmark-stripped string)."""
    offsets: dict[str, int] = {}
    content = ""
    for part in BOOKMARK_RE.split(text):
        match = _BOOKMARK_INNER_RE.match(part)
        if match:
            offsets[match.group(1)] = len(content)
        else:
            content += part
    return offsets


def boundary_word(clean_text: str, offset: int) -> str:
    tail = clean_text[offset:].strip()
    if not tail:
        return "."
    return tail.split()[0]


class ManifestAudioService(SpeechService):
    """Reuse storyboard WAV files as a Manim Voiceover speech service.

    The service is read-only: ``generate_from_text`` looks up the WAV by
    ``slide_id`` (passed as a kwarg from the BookmarkBeatScene) and returns
    the metadata manim-voiceover needs to track timing.
    """

    def __init__(self, manifest_path: Path, audio_dir: Path):
        self.manifest_path = Path(manifest_path)
        self.audio_dir = Path(audio_dir)
        with self.manifest_path.open("r", encoding="utf-8") as handle:
            manifest = json.load(handle)
        self.slides = {slide["slide_id"]: slide for slide in manifest["slides"]}
        super().__init__(cache_dir=str(self.audio_dir))

    def generate_from_text(
        self,
        text: str,
        cache_dir: str | None = None,
        path: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        slide_id = kwargs.get("slide_id")
        if slide_id is None:
            raise ValueError(
                "ManifestAudioService.generate_from_text requires slide_id kwarg "
                "(BookmarkBeatScene passes this automatically)."
            )
        slide = self.slides.get(slide_id)
        if slide is None:
            raise KeyError(
                f"slide_id '{slide_id}' not present in manifest {self.manifest_path}."
            )
        audio_name = f"{int(slide['slide_number']):02d}_{slide_id}.wav"
        audio_path = self.audio_dir / audio_name
        if not audio_path.exists():
            raise FileNotFoundError(
                f"Audio file missing: {audio_path}. "
                "Run the TTS bridge before rendering."
            )

        return {
            "input_text": text,
            "input_data": {
                "input_text": remove_bookmarks(text),
                "service": "manifest_audio",
                "slide_id": slide_id,
            },
            "original_audio": audio_name,
            "word_boundaries": self._word_boundaries(text, slide, audio_path),
        }

    def _word_boundaries(
        self,
        text: str,
        slide: dict[str, Any],
        audio_path: Path,
    ) -> list[dict[str, Any]]:
        clean_text = remove_bookmarks(text)
        offsets = bookmark_offsets(text)
        duration = wav_duration(audio_path)

        # Always anchor start (offset=0, t=0) and end (offset=len, t=duration);
        # add one anchor per beat that has a matching bookmark in the text.
        anchors: dict[int, float] = {0: 0.0, len(clean_text): duration}
        for beat in slide.get("beats", []) or []:
            mark = beat.get("id")
            if mark and mark in offsets:
                anchors[offsets[mark]] = float(beat["start_seconds"])

        return [
            {
                "audio_offset": int(seconds * AUDIO_OFFSET_RESOLUTION),
                "text_offset": int(offset),
                "word_length": max(len(boundary_word(clean_text, offset)), 1),
                "text": boundary_word(clean_text, offset),
                "boundary_type": "Word",
            }
            for offset, seconds in sorted(anchors.items())
        ]

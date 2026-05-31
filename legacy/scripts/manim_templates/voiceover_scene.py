"""BookmarkBeatScene: VoiceoverScene for two-stage rendering.

Stage 1 (this class): render the scene with audio attachment suppressed.
The output is a silent MP4 + a JSON timeline of bookmark trigger times and
voiceover segments.

Stage 2 (manim_runtime.mux_scene_video_with_audio, downstream): use the
timeline to splice the actual WAVs onto the silent video with ffmpeg. This
keeps the visual cache fingerprint independent of narration text — changing
``voiceover`` without touching ``data`` reuses the cached silent video.

The two-stage split is what preserves the cache-separation property
documented in MANIM_VOICEOVER_MIGRATION_PLAN.md §5.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from manim_voiceover import VoiceoverScene


class BookmarkBeatScene(VoiceoverScene):
    """VoiceoverScene that runs in dry-run-audio mode and records timing.

    Subclasses (or external configurators) should set ``timeline_path`` to a
    pathlib.Path before construct() runs; the scene writes the JSON there
    after every voiceover block. ``dry_run_audio`` defaults to True; flip to
    False when you want manim-voiceover's standard single-stage rendering.
    """

    dry_run_audio: bool = True
    timeline_path: Path | None = None

    bookmark_timeline: list[dict[str, Any]]
    voiceover_segments: list[dict[str, Any]]

    def setup(self) -> None:  # type: ignore[override]
        super().setup()
        self.bookmark_timeline = []
        self.voiceover_segments = []

    def add_sound(self, sound_file, **kwargs):  # type: ignore[override]
        if self.dry_run_audio:
            self.voiceover_segments.append(
                {
                    "scene_time": float(self.renderer.time),
                    "audio_path": str(sound_file),
                    "kwargs": {
                        k: v
                        for k, v in kwargs.items()
                        if isinstance(v, (int, float, str, bool))
                    },
                }
            )
            self._write_timeline()
            return None
        return super().add_sound(sound_file, **kwargs)

    def wait_until_bookmark(self, mark: str) -> None:  # type: ignore[override]
        planned = None
        if self.current_tracker is not None and mark in getattr(
            self.current_tracker, "bookmark_times", {}
        ):
            planned = float(self.current_tracker.bookmark_times[mark])
        super().wait_until_bookmark(mark)
        self.bookmark_timeline.append(
            {
                "mark": mark,
                "scene_time_planned": planned,
                "scene_time_actual": float(self.renderer.time),
                "voiceover_segment": max(len(self.voiceover_segments) - 1, 0),
            }
        )
        self._write_timeline()

    def tear_down(self) -> None:  # type: ignore[override]
        # Manim calls tear_down once construct() finishes. Use it to flush
        # the final scene_time into the timeline so consumers see the true
        # end-of-scene timestamp, not the moment of the last add_sound call.
        try:
            self._write_timeline()
        finally:
            super().tear_down()

    def _write_timeline(self) -> None:
        if self.timeline_path is None:
            return
        try:
            scene_time = float(self.renderer.time)
        except AttributeError:
            scene_time = 0.0
        payload = {
            "scene_class": type(self).__name__,
            "dry_run_audio": self.dry_run_audio,
            "voiceover_segments": self.voiceover_segments,
            "bookmark_timeline": self.bookmark_timeline,
            "final_scene_time": scene_time,
        }
        self.timeline_path.parent.mkdir(parents=True, exist_ok=True)
        self.timeline_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

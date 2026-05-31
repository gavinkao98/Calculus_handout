from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

from shared_media_paths import (
    DEFAULT_DECK_ID,
    audio_dir_path,
    audio_manifest_path,
    deck_json_path,
)
from shared_runtime_bootstrap import REPO_ROOT, bootstrap_repo_deps, ensure_directory, require_path
from slides_script_workflow import final_script_path, load_slide_scripts

bootstrap_repo_deps()

import numpy as np
import soundfile as sf
import torch
from TTS.api import TTS


DEFAULT_REFERENCE = REPO_ROOT / "artifacts" / "voice" / "reference_30s.wav"
XTTS_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"
DEFAULT_BUILTIN_MODEL = "tts_models/en/jenny/jenny"
COQUI_CPML_URL = "https://coqui.ai/cpml"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synthesize per-slide narration audio from the section deck JSON and final narration markdown."
    )
    parser.add_argument("--deck-id", default=DEFAULT_DECK_ID)
    parser.add_argument("--deck-json", type=Path)
    parser.add_argument("--script-file", type=Path)
    parser.add_argument("--reference-wav", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--model-name", default=XTTS_MODEL)
    parser.add_argument("--voice-mode", choices=("clone", "builtin"), default="clone")
    parser.add_argument("--speaker")
    parser.add_argument("--language", default="en")
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--max-slides", type=int)
    parser.add_argument("--coqui-tos-agreed", action="store_true")
    parser.add_argument("--split-sentences", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--speed", type=float, default=1.03)
    parser.add_argument("--repetition-penalty", type=float, default=11.0)
    parser.add_argument("--max-chars-per-chunk", type=int, default=220)
    parser.add_argument("--inter-chunk-pause-ms", type=int, default=120)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def resolve_device(requested: str) -> str:
    if requested == "cpu":
        return "cpu"
    if requested == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA was requested but torch.cuda.is_available() is false.")
        return "cuda"
    return "cuda" if torch.cuda.is_available() else "cpu"


def load_deck(path: Path) -> dict:
    with require_path(path.resolve(), "slide deck JSON").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def default_output_suffix(voice_mode: str) -> str:
    if voice_mode == "builtin":
        return "builtin"
    return ""


def require_coqui_tos_agreement(agreed: bool) -> None:
    if agreed or os.environ.get("COQUI_TOS_AGREED") == "1":
        os.environ["COQUI_TOS_AGREED"] = "1"
        return
    raise RuntimeError(
        "XTTS v2 requires explicit agreement to Coqui's non-commercial CPML terms before the model "
        f"can be downloaded. Re-run with --coqui-tos-agreed if you agree: {COQUI_CPML_URL}"
    )


def model_needs_coqui_tos(model_name: str) -> bool:
    return "xtts" in model_name.lower()


def normalize_script(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_long_clause(clause: str, max_chars: int) -> list[str]:
    words = clause.split()
    if not words:
        return []

    chunks: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
            continue
        chunks.append(current.strip())
        current = word
    chunks.append(current.strip())
    return chunks


def chunk_script(text: str, max_chars: int) -> list[str]:
    if max_chars < 80:
        raise ValueError(f"max_chars_per_chunk must be at least 80, got {max_chars}.")

    normalized = normalize_script(text)
    clauses = [part.strip() for part in re.split(r"(?<=[.!?;:])\s+|(?<=,)\s+", normalized) if part.strip()]
    chunks: list[str] = []
    current = ""

    for clause in clauses:
        clause_parts = [clause]
        if len(clause) > max_chars:
            clause_parts = split_long_clause(clause, max_chars)

        for part in clause_parts:
            if not current:
                current = part
                continue

            candidate = f"{current} {part}"
            if len(candidate) <= max_chars:
                current = candidate
                continue

            chunks.append(current.strip())
            current = part

    if current:
        chunks.append(current.strip())
    return chunks


def synthesize_chunks(
    api: TTS,
    text: str,
    split_sentences: bool,
    max_chars_per_chunk: int,
    inter_chunk_pause_ms: int,
    tts_kwargs: dict,
) -> tuple[np.ndarray, int, list[str]]:
    sample_rate = int(api.synthesizer.output_sample_rate)
    chunks = chunk_script(text, max_chars_per_chunk)
    if not chunks:
        raise ValueError("Chunking produced no text segments.")

    pause_samples = max(int(sample_rate * inter_chunk_pause_ms / 1000), 0)
    pause = np.zeros(pause_samples, dtype=np.float32)
    rendered: list[np.ndarray] = []

    for chunk in chunks:
        wav = api.tts(
            text=chunk,
            split_sentences=split_sentences,
            **tts_kwargs,
        )
        rendered.append(np.asarray(wav, dtype=np.float32))

    combined = rendered[0]
    for wav in rendered[1:]:
        if pause_samples:
            combined = np.concatenate((combined, pause, wav))
        else:
            combined = np.concatenate((combined, wav))

    return combined, sample_rate, chunks


def silence(sample_rate: int, seconds: float) -> np.ndarray:
    sample_count = max(int(round(sample_rate * seconds)), 0)
    return np.zeros(sample_count, dtype=np.float32)


def safe_audio_stem(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip())
    return cleaned.strip("_") or "beat"


def script_from_slide_beats(slide: dict) -> str | None:
    beats = slide.get("voiceover_beats") or []
    if not beats:
        return None
    return normalize_script(" ".join(str(beat["text"]) for beat in beats))


def synthesize_slide_beats(
    api: TTS,
    slide: dict,
    output_dir: Path,
    split_sentences: bool,
    max_chars_per_chunk: int,
    inter_chunk_pause_ms: int,
    tts_kwargs: dict,
) -> tuple[np.ndarray, int, list[dict], str]:
    slide_number = int(slide["slide_number"])
    slide_id = slide["slide_id"]
    beats = slide.get("voiceover_beats") or []
    if not beats:
        raise ValueError(f"Slide {slide_number} ({slide_id}) has no voiceover beats.")

    beat_dir = ensure_directory(output_dir / "beats" / f"{slide_number:02d}_{slide_id}")
    rendered_parts: list[np.ndarray] = []
    manifest_beats: list[dict] = []
    sample_rate: int | None = None
    timeline = 0.0

    for beat_index, beat in enumerate(beats, start=1):
        audio, current_sample_rate, chunks = synthesize_chunks(
            api=api,
            text=beat["text"],
            split_sentences=split_sentences,
            max_chars_per_chunk=max_chars_per_chunk,
            inter_chunk_pause_ms=inter_chunk_pause_ms,
            tts_kwargs=tts_kwargs,
        )
        if sample_rate is None:
            sample_rate = current_sample_rate
        elif sample_rate != current_sample_rate:
            raise RuntimeError(f"TTS sample rate changed within slide {slide_number}.")

        beat_audio_seconds = len(audio) / sample_rate
        hold_after = float(beat.get("hold_after_seconds", 0.0))
        beat_wav = beat_dir / f"{beat_index:02d}_{safe_audio_stem(beat['id'])}.wav"
        sf.write(str(beat_wav), audio, sample_rate)

        rendered_parts.append(audio)
        if hold_after > 0:
            rendered_parts.append(silence(sample_rate, hold_after))

        manifest_beats.append(
            {
                "id": beat["id"],
                "text": beat["text"],
                "reveal": beat.get("reveal", []),
                "audio_file": str(beat_wav),
                "audio_seconds": round(beat_audio_seconds, 3),
                "hold_after_seconds": round(hold_after, 3),
                "start_seconds": round(timeline, 3),
                "end_seconds": round(timeline + beat_audio_seconds + hold_after, 3),
                "chunk_count": len(chunks),
                "chunks": chunks,
            }
        )
        timeline += beat_audio_seconds + hold_after

    if sample_rate is None:
        raise RuntimeError(f"Slide {slide_number} ({slide_id}) produced no beat audio.")
    combined = np.concatenate(rendered_parts) if rendered_parts else silence(sample_rate, 0)
    return combined, sample_rate, manifest_beats, script_from_slide_beats(slide) or ""


def build_tts_kwargs(api: TTS, args: argparse.Namespace, reference_wav: Path | None) -> dict:
    tts_kwargs: dict = {}

    if api.is_multi_lingual:
        tts_kwargs["language"] = args.language

    if reference_wav is not None:
        tts_kwargs["speaker_wav"] = str(reference_wav)
    elif args.speaker:
        tts_kwargs["speaker"] = args.speaker
    elif api.is_multi_speaker and api.speakers:
        tts_kwargs["speaker"] = api.speakers[0]

    if model_needs_coqui_tos(args.model_name):
        tts_kwargs["speed"] = args.speed
        tts_kwargs["repetition_penalty"] = args.repetition_penalty

    return tts_kwargs


def main() -> int:
    args = parse_args()
    deck_json = (args.deck_json or deck_json_path(REPO_ROOT, args.deck_id)).resolve()
    deck = load_deck(deck_json)
    resolved_deck_id = deck["deck_id"]
    script_file = (args.script_file or final_script_path(REPO_ROOT, resolved_deck_id)).resolve()
    scripts = load_slide_scripts(script_file, deck)
    output_dir = ensure_directory(
        (args.output_dir or audio_dir_path(REPO_ROOT, resolved_deck_id, default_output_suffix(args.voice_mode))).resolve()
    )
    manifest_path = (
        args.manifest
        or audio_manifest_path(REPO_ROOT, resolved_deck_id, default_output_suffix(args.voice_mode))
    ).resolve()
    ensure_directory(manifest_path.parent)
    slides = deck["slides"]
    if args.max_slides is not None:
        slides = slides[: args.max_slides]
        scripts = scripts[: args.max_slides]

    if args.dry_run:
        beat_count = sum(len(slide.get("voiceover_beats") or []) for slide in slides)
        print(f"Validated {len(slides)} slide narrations from {script_file} ({beat_count} beat narrations).")
        return 0

    reference_wav = None
    if args.voice_mode == "clone":
        reference_wav = require_path(args.reference_wav.resolve(), "voice reference WAV")
    if model_needs_coqui_tos(args.model_name):
        require_coqui_tos_agreement(args.coqui_tos_agreed)

    device = resolve_device(args.device)
    api = TTS(args.model_name).to(device)
    tts_kwargs = build_tts_kwargs(api, args, reference_wav)

    manifest = {
        "deck_id": deck["deck_id"],
        "script_file": str(script_file),
        "model_name": args.model_name,
        "voice_mode": args.voice_mode,
        "language": args.language,
        "device": device,
        "reference_wav": str(reference_wav) if reference_wav else None,
        "speaker": tts_kwargs.get("speaker"),
        "slides": [],
    }

    for slide, text in zip(slides, scripts):
        slide_number = int(slide["slide_number"])
        slide_id = slide["slide_id"]
        output_wav = output_dir / f"{slide_number:02d}_{slide_id}.wav"

        beat_manifest: list[dict] = []
        narration_mode = "single"
        script_text = text
        if slide.get("voiceover_beats"):
            narration_mode = "beats"
            audio, sample_rate, beat_manifest, script_text = synthesize_slide_beats(
                api=api,
                slide=slide,
                output_dir=output_dir,
                split_sentences=args.split_sentences,
                max_chars_per_chunk=args.max_chars_per_chunk,
                inter_chunk_pause_ms=args.inter_chunk_pause_ms,
                tts_kwargs=tts_kwargs,
            )
            chunks = [chunk for beat in beat_manifest for chunk in beat["chunks"]]
        else:
            audio, sample_rate, chunks = synthesize_chunks(
                api=api,
                text=text,
                split_sentences=args.split_sentences,
                max_chars_per_chunk=args.max_chars_per_chunk,
                inter_chunk_pause_ms=args.inter_chunk_pause_ms,
                tts_kwargs=tts_kwargs,
            )
        sf.write(str(output_wav), audio, sample_rate)

        slide_entry = {
            "slide_number": slide_number,
            "slide_id": slide_id,
            "audio_file": str(output_wav),
            "script": script_text,
            "narration_mode": narration_mode,
            "audio_seconds": round(len(audio) / sample_rate, 3),
            "split_sentences": args.split_sentences,
            "speed": args.speed if model_needs_coqui_tos(args.model_name) else None,
            "repetition_penalty": (
                args.repetition_penalty if model_needs_coqui_tos(args.model_name) else None
            ),
            "chunk_count": len(chunks),
            "chunks": chunks,
            "max_chars_per_chunk": args.max_chars_per_chunk,
            "inter_chunk_pause_ms": args.inter_chunk_pause_ms,
        }
        if beat_manifest:
            slide_entry["beats"] = beat_manifest
        manifest["slides"].append(slide_entry)
        print(f"Synthesized slide {slide_number}: {output_wav.name}")

    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote synthesis manifest to {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

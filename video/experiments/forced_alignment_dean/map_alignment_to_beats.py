"""Map word-level forced-alignment timestamps back to storyboard beats."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

VIDEO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(VIDEO_ROOT))

from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()

from pipeline.audio import wav_duration  # noqa: E402

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")


def load_plan(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def tokenize(text: str) -> list[str]:
    return WORD_RE.findall(text)


def flatten_words(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict) and isinstance(data.get("words"), list):
        return data["words"]
    if isinstance(data, dict) and isinstance(data.get("segments"), list):
        out: list[dict[str, Any]] = []
        for segment in data["segments"]:
            if isinstance(segment, dict) and isinstance(segment.get("words"), list):
                out.extend(segment["words"])
        return out
    if isinstance(data, list):
        return data
    raise SystemExit("unsupported words JSON shape; expected words[] or segments[].words[]")


def load_words(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    words = flatten_words(data)
    clean = []
    for i, item in enumerate(words):
        try:
            start = float(item["start"])
            end = float(item["end"])
        except (KeyError, TypeError, ValueError) as exc:
            raise SystemExit(f"word item {i} lacks numeric start/end: {item!r}") from exc
        clean.append({"word": str(item.get("word") or item.get("text") or ""), "start": start, "end": end})
    return clean


def linear_words(plan: dict[str, Any], duration: float) -> list[dict[str, Any]]:
    transcript_words: list[str] = []
    for beat in plan["beats"]:
        transcript_words.extend(tokenize(beat["text"]))
    if not transcript_words:
        return []
    step = duration / len(transcript_words)
    return [
        {"word": word, "start": i * step, "end": (i + 1) * step}
        for i, word in enumerate(transcript_words)
    ]


def start_for_word(words: list[dict[str, Any]], index: int, audio_duration: float) -> float:
    if not words:
        return 0.0
    if index <= 0:
        return 0.0
    if index < len(words):
        return float(words[index]["start"])
    return audio_duration


def align_beats(plan: dict[str, Any], words: list[dict[str, Any]], audio_duration: float) -> dict[str, Any]:
    beat_starts = [
        start_for_word(words, int(beat["word_start"]), audio_duration)
        for beat in plan["beats"]
    ]
    aligned = []
    warnings = []
    for i, beat in enumerate(plan["beats"]):
        start = beat_starts[i]
        end = beat_starts[i + 1] if i + 1 < len(beat_starts) else audio_duration
        if end < start:
            warnings.append(f"{beat['id']}: end < start; clamped")
            end = start
        if end - start < 0.05:
            warnings.append(f"{beat['id']}: very short duration {end - start:.3f}s")
        aligned.append(
            {
                **beat,
                "start_seconds": round(start, 3),
                "end_seconds": round(end, 3),
                "audio_seconds": round(end - start, 3),
            }
        )
    expected_words = int(plan.get("word_count") or 0)
    word_delta = len(words) - expected_words
    word_delta_ratio = (abs(word_delta) / expected_words) if expected_words else 0.0
    if expected_words and abs(word_delta) > max(3, expected_words * 0.05):
        warnings.append(
            "word count differs: "
            f"transcript={expected_words}, alignment={len(words)}, delta={word_delta}"
        )
    return {
        "scene_id": plan["scene_id"],
        "audio_seconds": round(audio_duration, 3),
        "word_count": len(words),
        "expected_word_count": expected_words,
        "word_count_delta": word_delta,
        "word_count_delta_ratio": round(word_delta_ratio, 4),
        "beats": aligned,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--words", type=Path)
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--linear-from-audio", action="store_true",
                        help="smoke-test plumbing without a real aligner")
    args = parser.parse_args()

    plan = load_plan(args.plan)
    audio_duration = wav_duration(args.audio)
    if args.linear_from_audio:
        words = linear_words(plan, audio_duration)
        mode = "linear_smoke"
    else:
        if args.words is None:
            raise SystemExit("--words is required unless --linear-from-audio is set")
        words = load_words(args.words)
        mode = "forced_alignment"
    result = align_beats(plan, words, audio_duration)
    result["mode"] = mode
    result["audio_file"] = str(args.audio.resolve())
    out = (args.output or (args.plan.resolve().parent / "aligned_beats.json")).resolve()
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[align-map] mode={mode} words={len(words)} audio={audio_duration:.3f}s")
    print(f"[align-map] wrote {out}")
    for warning in result["warnings"]:
        print(f"  WARN {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

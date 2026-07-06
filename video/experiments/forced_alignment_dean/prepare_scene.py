"""Prepare a single storyboard scene for Dean forced-alignment experiments."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

VIDEO_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = VIDEO_ROOT.parent
sys.path.insert(0, str(VIDEO_ROOT))

from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()

import yaml  # noqa: E402

from pipeline.narration import parse_say  # noqa: E402

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def default_out_dir(scene_id: str) -> Path:
    return REPO_ROOT / "video" / "output" / "experiments" / "forced_alignment_dean" / scene_id


def load_scene(storyboard: Path, scene_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    data = yaml.safe_load(storyboard.read_text(encoding="utf-8"))
    by_id = {scene["id"]: scene for scene in data["scenes"]}
    if scene_id not in by_id:
        available = ", ".join(sorted(by_id))
        raise SystemExit(f"unknown scene {scene_id!r}; available: {available}")
    return data["meta"], by_id[scene_id]


def build_plan(storyboard: Path, meta: dict[str, Any], scene: dict[str, Any]) -> dict[str, Any]:
    parsed = parse_say(scene.get("say", ""))
    beats: list[dict[str, Any]] = []
    transcript_parts: list[str] = []
    cursor = 0
    for index, beat in enumerate(parsed, start=1):
        beat_words = words(beat.text)
        start = cursor
        end = cursor + len(beat_words)
        beats.append(
            {
                "index": index,
                "id": f"beat_{index:02d}",
                "reveal": beat.reveal,
                "text": beat.text,
                "word_start": start,
                "word_end": end,
                "word_count": len(beat_words),
            }
        )
        transcript_parts.append(beat.text)
        cursor = end
    transcript = " ".join(part for part in transcript_parts if part).strip()
    return {
        "storyboard": str(storyboard.resolve()),
        "deck_id": meta.get("id"),
        "section": meta.get("section"),
        "scene_id": scene["id"],
        "scene_title": scene.get("title"),
        "tts": {
            "backend": "mimo",
            "model": "mimo-v2.5-tts",
            "voice": "Dean",
        },
        "transcript": transcript,
        "word_count": len(words(transcript)),
        "beats": beats,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--storyboard", type=Path, required=True)
    parser.add_argument("--scene", required=True)
    parser.add_argument("--out-dir", type=Path)
    args = parser.parse_args()

    meta, scene = load_scene(args.storyboard, args.scene)
    if scene.get("kind", "content") != "content":
        raise SystemExit("forced-alignment experiment expects a content scene with say text")
    plan = build_plan(args.storyboard, meta, scene)
    out_dir = (args.out_dir or default_out_dir(args.scene)).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "scene_plan.json").write_text(
        json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out_dir / "transcript.txt").write_text(plan["transcript"] + "\n", encoding="utf-8")
    print(f"[prepare] scene={args.scene} words={plan['word_count']} beats={len(plan['beats'])}")
    print(f"[prepare] wrote {out_dir / 'scene_plan.json'}")
    print(f"[prepare] wrote {out_dir / 'transcript.txt'}")
    print("[prepare] Dean test model=mimo-v2.5-tts voice=Dean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

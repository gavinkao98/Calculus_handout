"""Render one scene using forced-alignment beat durations and mux a scene-level WAV."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

VIDEO_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = VIDEO_ROOT.parent
sys.path.insert(0, str(VIDEO_ROOT))

from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()

import yaml  # noqa: E402

from pipeline.timing import SCENE_LEAD_SECONDS  # noqa: E402


def ffmpeg(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("ffmpeg failed:\n" + " ".join(cmd) + "\n" + result.stderr[-1500:])


def load_scene(storyboard: Path, scene_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    data = yaml.safe_load(storyboard.read_text(encoding="utf-8"))
    by_id = {scene["id"]: scene for scene in data["scenes"]}
    if scene_id not in by_id:
        raise SystemExit(f"unknown scene {scene_id!r}")
    return data["meta"], by_id[scene_id]


def render_scene(meta: dict[str, Any], scene: dict[str, Any], durations: list[float],
                 out_dir: Path, quality: str) -> Path:
    from manim import tempconfig
    from pipeline.scene import LessonScene

    media_dir = out_dir / "_media"
    output_file = f"{meta['id']}__{scene['id']}__aligned"
    LessonScene.spec = scene
    LessonScene.meta = meta
    LessonScene.beat_durations = durations
    cfg: dict[str, Any] = {
        "media_dir": str(media_dir),
        "output_file": output_file,
        "disable_caching": True,
        "verbosity": "ERROR",
    }
    if quality == "high":
        cfg.update({"pixel_width": 1920, "pixel_height": 1080, "frame_rate": 30})
    else:
        cfg["quality"] = "low_quality"
    with tempconfig(cfg):
        LessonScene().render()
    matches = list(media_dir.rglob(f"{output_file}.mp4"))
    if not matches:
        raise SystemExit(f"render produced no mp4 for {output_file}")
    return max(matches, key=lambda p: p.stat().st_mtime)


def mux(video: Path, audio: Path, out: Path) -> None:
    lead_ms = max(int(round(SCENE_LEAD_SECONDS * 1000)), 0)
    ffmpeg([
        "ffmpeg", "-y", "-i", str(video), "-i", str(audio),
        "-filter_complex", f"[1:a]adelay={lead_ms}:all=1,apad[a]",
        "-map", "0:v:0", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-shortest", str(out),
    ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--storyboard", type=Path, required=True)
    parser.add_argument("--scene", required=True)
    parser.add_argument("--aligned", type=Path, required=True)
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--quality", choices=("low", "high"), default="low")
    args = parser.parse_args()

    meta, scene = load_scene(args.storyboard, args.scene)
    aligned = json.loads(args.aligned.read_text(encoding="utf-8"))
    durations = [float(beat["audio_seconds"]) for beat in aligned["beats"]]
    out_dir = (
        args.out_dir
        or (REPO_ROOT / "video" / "output" / "experiments" / "forced_alignment_dean" / args.scene)
    ).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[render-align] rendering {args.scene} with {len(durations)} aligned beat(s)")
    video = render_scene(meta, scene, durations, out_dir, args.quality)
    output = out_dir / f"{args.scene}_aligned_dean.mp4"
    mux(video, args.audio.resolve(), output)
    print(f"[render-align] wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""scratch_frames.py -- render selected scenes' FINAL frame to PNG for visual QA.

Offline, not billed. Reuses the pipeline's LessonScene (no audio / no compose) and
manim's save_last_frame, so each scene dumps its fullest (final) frame for layout /
visual review. Layout is resolution-independent, so a 1080p still is the same
composition as the 4K master.

  python video/scratch_frames.py --storyboard video/storyboards/ch01_inverse_functions.yml \
         --scene one_to_one_definition,first_inverses --out video/output/_qa/baseline
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipeline import _bootstrap

_bootstrap.bootstrap()

import yaml  # noqa: E402
from manim import tempconfig  # noqa: E402

from pipeline.scene import LessonScene  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--storyboard", required=True, type=Path)
    ap.add_argument("--scene", default="all", help="id, 'a,b,c', or 'all'")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    args = ap.parse_args()

    data = yaml.safe_load(args.storyboard.read_text(encoding="utf-8"))
    meta = data["meta"]
    scenes = data["scenes"]
    if args.scene != "all":
        want = [s.strip() for s in args.scene.split(",") if s.strip()]
        by_id = {s["id"]: s for s in scenes}
        missing = [i for i in want if i not in by_id]
        if missing:
            raise SystemExit(f"Unknown scene(s) {missing}. Available: {', '.join(by_id)}")
        scenes = [by_id[i] for i in want]

    args.out.mkdir(parents=True, exist_ok=True)
    media_dir = args.out / "_media"
    for scene in scenes:
        sid = scene["id"]
        output_file = f"{meta['id']}__{sid}"
        LessonScene.spec = scene
        LessonScene.meta = meta
        LessonScene.beat_durations = None
        cfg = {
            "media_dir": str(media_dir),
            "output_file": output_file,
            "disable_caching": True,
            "verbosity": "ERROR",
            "save_last_frame": True,
            "write_to_movie": False,
            "format": "png",
            "pixel_width": args.width,
            "pixel_height": args.height,
        }
        print(f"[frame] {sid} ...", flush=True)
        with tempconfig(cfg):
            LessonScene().render()
        matches = list(media_dir.rglob(f"{output_file}.png"))
        if matches:
            src = max(matches, key=lambda p: p.stat().st_mtime)
            dst = args.out / f"{sid}.png"
            shutil.copyfile(src, dst)
            print(f"        -> {dst}", flush=True)
        else:
            print(f"        !! no png for {output_file}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

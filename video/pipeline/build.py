"""CLI: render storyboard scene(s) to silent preview MP4s, optionally stitched.

    .venv/Scripts/python video/pipeline/build.py \
        --storyboard video/storyboards/ch01_inverse_functions.yml \
        --scene one_to_one,intro --quality low

--scene accepts a single id, a comma-separated list, or "all". manim is
imported ONCE and reused across all requested scenes (import is slow here, so
per-scene processes would pay it repeatedly).

Add --concat to stitch the rendered scenes, in storyboard order, into one silent
MP4 at video/output/<deck-id>.mp4. Audio is out of scope (TTS/mux are later).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()  # must precede any manim / yaml import

import yaml  # noqa: E402
from manim import tempconfig  # noqa: E402

from pipeline.scene import LessonScene  # noqa: E402

_QUALITY = {"low": "low_quality", "medium": "medium_quality", "high": "production_quality"}


def _load_beat_durations(meta) -> dict[str, list[float]]:
    """Map each content scene_id -> per-beat narration seconds, from the TTS manifest.

    Returns {} when nothing has been synthesized yet, so render still works
    standalone (falling back to word-count estimates inside the scene player).
    """
    sec_dir = _bootstrap.section_output_dir(meta)
    audio_subdir = "audio_mimo" if meta["id"].endswith("_mimo") else "audio"
    manifest = sec_dir / audio_subdir / "manifest.json"
    if not manifest.exists():
        return {}
    data = json.loads(manifest.read_text(encoding="utf-8"))
    durations: dict[str, list[float]] = {}
    for scene in data.get("scenes", []):
        if scene.get("narration_mode") == "beats":
            durations[scene["scene_id"]] = [b["audio_seconds"] for b in scene.get("beats", [])]
    return durations


def _render_one(meta, spec, out_dir, quality, durations=None) -> str:
    output_file = f"{meta['id']}__{spec['id']}"
    LessonScene.spec = spec
    LessonScene.meta = meta
    LessonScene.beat_durations = durations
    with tempconfig({
        "quality": _QUALITY[quality],
        "media_dir": str(out_dir / "_media"),
        "output_file": output_file,
        "disable_caching": True,
    }):
        LessonScene().render()
    matches = list((out_dir / "_media").rglob(f"{output_file}.mp4"))
    return str(max(matches, key=lambda p: p.stat().st_mtime)) if matches else f"!! no mp4 for {output_file}"


def _scene_mp4(out_dir: Path, meta, sid: str) -> Path | None:
    # freshest by mtime, not name -- see _render_one / mux._scene_mp4 (stale-res trap)
    matches = list((out_dir / "_media").rglob(f"{meta['id']}__{sid}.mp4"))
    return max(matches, key=lambda p: p.stat().st_mtime) if matches else None


def _concat(out_dir: Path, meta, ordered_ids: list[str]) -> int:
    """Stitch scenes (storyboard order) into one silent MP4 via ffmpeg concat."""
    segments = []
    for sid in ordered_ids:
        mp4 = _scene_mp4(out_dir, meta, sid)
        if mp4 is None:
            print(f"[concat] missing rendered scene: {sid}", flush=True)
            return 1
        segments.append(mp4)

    sec_dir = _bootstrap.section_output_dir(meta)
    sec_dir.mkdir(parents=True, exist_ok=True)
    output = sec_dir / f"{meta['id']}.mp4"
    list_file = out_dir / "_concat_list.txt"
    # ffmpeg is a native Windows exe: feed it Windows-style ('C:/...') paths via
    # as_posix(), NOT MSYS '/c/...' paths (which it cannot open).
    list_file.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in segments) + "\n",
        encoding="utf-8",
    )
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c:v", "libx264", "-preset", "medium", "-pix_fmt", "yuv420p", "-an",
        str(output),
    ]
    print(f"[concat] stitching {len(segments)} scenes -> {output}", flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True)
    list_file.unlink(missing_ok=True)
    if result.returncode != 0:
        print("[concat] ffmpeg failed:\n" + result.stderr[-1500:], flush=True)
        return 1
    print(f"[concat] OK -> {output}", flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--storyboard", required=True)
    parser.add_argument("--scene", required=True, help="id, 'a,b,c', or 'all'")
    parser.add_argument("--quality", default="low", choices=sorted(_QUALITY))
    parser.add_argument("--concat", action="store_true",
                        help="stitch rendered scenes (storyboard order) into one MP4")
    args = parser.parse_args()

    data = yaml.safe_load(Path(args.storyboard).resolve().read_text(encoding="utf-8"))
    meta = data["meta"]
    scenes = {s["id"]: s for s in data["scenes"]}

    if args.scene == "all":
        wanted = list(scenes)
    else:
        wanted = [s.strip() for s in args.scene.split(",") if s.strip()]
    missing = [s for s in wanted if s not in scenes]
    if missing:
        parser.error(f"unknown scene(s) {missing}. Available: {sorted(scenes)}")

    out_dir = _bootstrap.REPO_ROOT / "video" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    durations_by_scene = _load_beat_durations(meta)
    if durations_by_scene:
        print(f"narration timing: using manifest durations for {len(durations_by_scene)} content scene(s)", flush=True)
    else:
        print("narration timing: no manifest found, falling back to word-count estimates", flush=True)

    print(f"rendering {len(wanted)} scene(s): {wanted}", flush=True)
    failures = 0
    for sid in wanted:
        print(f"[render] {sid} ...", flush=True)
        try:
            print(f"[done]   {_render_one(meta, scenes[sid], out_dir, args.quality, durations_by_scene.get(sid))}", flush=True)
        except Exception as exc:
            failures += 1
            print(f"[FAIL]   {sid}: {exc!r}", flush=True)
            traceback.print_exc()

    if args.concat and not failures:
        # Always stitch in full storyboard order, regardless of --scene subset.
        return _concat(out_dir, meta, list(scenes))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

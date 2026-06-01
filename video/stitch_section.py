"""Stitch the full Section 1.1 preview: template scenes + the 5 custom animations.

Renders the 11 *template* scenes (mock, silent, 1080p30) via make.py's own
machinery, then concatenates all 16 scenes in storyboard order -- substituting
each custom-animation clip (demo_*.mp4) for the 5 scenes that have one. The result
is a 1080p30 preview of the integrated section.

This is a stitch-level integration: each custom scene is the standalone demo
dropped into its slot (its own pacing). The audio-synced `hook` integration is a
later step; this is to *see* the complete section now.

  python video/stitch_section.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()

import make  # noqa: E402  (orchestrator: load_storyboard / synth / render)

ROOT = Path(__file__).resolve().parent
SB = ROOT / "storyboards" / "ch01_inverse_functions.yml"
OUT = ROOT / "output"
DEMO = OUT / "_demo_media" / "videos" / "1080p30"

# storyboard scene id -> the custom-animation clip that stands in for it
CUSTOM = {
    "why_reverse_needs_one_to_one": "demo_cue1.mp4",   # mapping arrows
    "why_square_cannot_invert": "demo_hlt.mp4",         # line sweep
    "horizontal_line_test": "demo_cue3.mp4",            # HLT side-by-side
    "composition_identities": "demo_cue4.mp4",          # round-trip
    "reflection_across_y_equals_x": "demo_cue5.mp4",    # reflect y=x
}


def _ffmpeg() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def main() -> int:
    data = make.load_storyboard(SB)
    meta = data["meta"]
    meta["video"] = {"w": 1920, "h": 1080, "fps": 30}   # in-memory 1080p preview (4K stays the disk standard)
    all_scenes = data["scenes"]
    scene_numbers = {s["id"]: i for i, s in enumerate(all_scenes, start=1)}
    templates = [s for s in all_scenes if s["id"] not in CUSTOM]
    print(f"[stitch] {len(templates)} template scenes to render, {len(CUSTOM)} custom clips to drop in", flush=True)

    # render only the template scenes (the 5 custom ones come from demo clips)
    audio_dir = OUT / "audio" / meta["id"]
    manifest = make.synth(meta, templates, scene_numbers, audio_dir, "mock", empty_seconds=0.45)
    (audio_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    rendered, failures = make.render(meta, templates, manifest, OUT, "high")  # high -> meta.video (now 1080p30)
    if failures:
        print(f"[stitch] {failures} render failure(s); aborting", flush=True)
        return 1

    # assemble the ordered segment list: demo clip for custom scenes, render otherwise
    segments: list[Path] = []
    for s in all_scenes:
        sid = s["id"]
        clip = DEMO / CUSTOM[sid] if sid in CUSTOM else rendered.get(sid)
        if not clip or not Path(clip).exists():
            print(f"[stitch] missing clip for scene '{sid}' -> {clip}", flush=True)
            return 1
        tag = "demo " if sid in CUSTOM else "tmpl "
        print(f"[stitch]   {tag}{sid}", flush=True)
        segments.append(Path(clip))

    # concat (video only -- all silent in mock), re-encode to uniform 1080p30
    list_file = OUT / "_section_list.txt"
    list_file.write_text("\n".join(f"file '{p.resolve().as_posix()}'" for p in segments) + "\n", encoding="utf-8")
    out = OUT / "ch01_section1_1_full.mp4"
    try:
        subprocess.run([_ffmpeg(), "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
                        "-an", "-c:v", "libx264", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
                        str(out)], check=True, capture_output=True, text=True)
    finally:
        list_file.unlink(missing_ok=True)
    print(f"[done] {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

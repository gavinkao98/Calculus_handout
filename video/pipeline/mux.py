"""Final assembly: mux narration under each rendered scene, concat to one MP4.

Reads the storyboard (scene order + kinds), the TTS manifest (per-scene narration
WAV), and the silent scene MP4s rendered by ``build.py``. Lays each content
scene's narration under its video -- delayed by the scene player's lead-in so the
first word lands on the first reveal -- gives intro/outro a silent track (bgm is
a later round), then concatenates everything into ``video/output/<id>.mp4`` with
audio.

    .venv/Scripts/python video/pipeline/mux.py \
        --storyboard video/storyboards/ch01_inverse_functions.yml

Run ``build.py --scene all`` first so every scene has a rendered MP4.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()  # for yaml (vendored under .deps)

import yaml  # noqa: E402

LEAD_SECONDS = 0.3  # matches LessonScene's initial self.wait(0.3) before beat 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--storyboard", required=True, type=Path)
    parser.add_argument("--manifest", type=Path, help="defaults to output/audio/<id>/manifest.json")
    parser.add_argument("--output", type=Path, help="defaults to output/<id>.mp4")
    parser.add_argument("--lead", type=float, default=LEAD_SECONDS,
                        help="seconds to delay narration so it lands on the first reveal")
    parser.add_argument("--audio-bitrate", default="192k")
    return parser.parse_args()


def _scene_mp4(media_dir: Path, deck_id: str, sid: str) -> Path | None:
    """Latest rendered MP4 for a scene, across whatever quality subdir build.py used."""
    matches = sorted(media_dir.rglob(f"{deck_id}__{sid}.mp4"))
    return matches[-1] if matches else None


def _run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("ffmpeg failed:\n" + " ".join(cmd) + "\n" + result.stderr[-1500:])


def _mux_content(video: Path, narration: Path, out: Path, lead: float, abr: str) -> None:
    """Lay narration under video, offset by *lead*; video is the master length."""
    _run([
        "ffmpeg", "-y",
        "-i", str(video),
        "-itsoffset", f"{lead:.3f}", "-i", str(narration),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", abr, "-ar", "48000", "-ac", "2",
        str(out),
    ])


def _mux_silent(video: Path, out: Path, abr: str) -> None:
    """Attach a uniform silent stereo track so every segment concats cleanly."""
    _run([
        "ffmpeg", "-y",
        "-i", str(video),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", abr, "-ar", "48000", "-ac", "2",
        "-shortest",
        str(out),
    ])


def _concat(segments: list[Path], out: Path, abr: str) -> None:
    """Concatenate the per-scene A/V segments (re-encode for GOP-safe joins)."""
    list_file = out.parent / "_concat_av_list.txt"
    # ffmpeg is a native Windows exe: feed Windows-style ('C:/...') paths via
    # as_posix(), not MSYS '/c/...' paths (which it cannot open).
    list_file.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in segments) + "\n",
        encoding="utf-8",
    )
    try:
        _run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
            "-c:v", "libx264", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", abr,
            str(out),
        ])
    finally:
        list_file.unlink(missing_ok=True)


def main() -> int:
    args = parse_args()
    data = yaml.safe_load(args.storyboard.resolve().read_text(encoding="utf-8"))
    meta = data["meta"]
    deck_id = meta["id"]

    out_root = _bootstrap.REPO_ROOT / "video" / "output"
    media_dir = out_root / "_media"
    manifest_path = args.manifest or (out_root / "audio" / deck_id / "manifest.json")

    narration_by_scene: dict[str, Path] = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for scene in manifest.get("scenes", []):
            if scene.get("narration_mode") == "beats" and scene.get("audio_file"):
                narration_by_scene[scene["scene_id"]] = Path(scene["audio_file"])
        print(f"[mux] narration for {len(narration_by_scene)} content scene(s) from {manifest_path.name}", flush=True)
    else:
        print("[mux] no manifest found; every scene gets a silent track", flush=True)

    av_dir = out_root / "_av"
    av_dir.mkdir(parents=True, exist_ok=True)

    segments: list[Path] = []
    for scene in data["scenes"]:
        sid = scene["id"]
        video = _scene_mp4(media_dir, deck_id, sid)
        if video is None:
            print(f"[mux] missing rendered scene '{sid}' -- run build.py --scene all first", flush=True)
            return 1
        av = av_dir / f"{sid}.mp4"
        narration = narration_by_scene.get(sid)
        if narration and narration.exists():
            print(f"[mux] {sid}: narration under video", flush=True)
            _mux_content(video, narration, av, args.lead, args.audio_bitrate)
        else:
            print(f"[mux] {sid}: silent track", flush=True)
            _mux_silent(video, av, args.audio_bitrate)
        segments.append(av)

    output = args.output or (out_root / f"{deck_id}.mp4")
    print(f"[concat] stitching {len(segments)} scenes -> {output}", flush=True)
    _concat(segments, output, args.audio_bitrate)
    print(f"[done] wrote {output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

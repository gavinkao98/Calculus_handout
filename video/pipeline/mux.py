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

from pipeline.timing import SCENE_LEAD_SECONDS  # noqa: E402

LEAD_SECONDS = SCENE_LEAD_SECONDS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--storyboard", required=True, type=Path)
    parser.add_argument("--manifest", type=Path, help="defaults to output/audio/<id>/manifest.json")
    parser.add_argument("--output", type=Path, help="defaults to output/<id>.mp4")
    parser.add_argument("--lead", type=float, default=LEAD_SECONDS,
                        help="seconds to delay narration so it lands on the first reveal")
    parser.add_argument("--audio-bitrate", default="192k")
    parser.add_argument("--transition", type=float, default=0.2,
                        help="per-side fade-through-black at every scene boundary "
                             "(0 = hard cuts); matches make.py's mock-preview transition")
    return parser.parse_args()


def _scene_mp4(media_dir: Path, deck_id: str, sid: str) -> Path | None:
    """Freshest rendered MP4 for a scene. Pick by mtime, NOT by name: _media keeps
    per-resolution subdirs (480p15/720p30/1080p30/1440p60/...) across runs, and a
    name sort puts '720p30' after '1440p60' -- muxing a stale low-res clip. (Same
    trap make.py.render() calls out.)"""
    matches = list(media_dir.rglob(f"{deck_id}__{sid}.mp4"))
    return max(matches, key=lambda p: p.stat().st_mtime) if matches else None


def _run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("ffmpeg failed:\n" + " ".join(cmd) + "\n" + result.stderr[-1500:])


def _probe_duration(path: Path) -> float:
    """Seconds via ffprobe; 0.0 if unreadable. (Mirror of make.py -- keep in sync.)"""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0.0


def _fade_vf(video: Path, fade: float) -> str:
    """Fade-in-from-black at start + fade-out-to-black at end; empty if fade<=0
    or the clip is too short. Concatenated faded clips give a ~2*fade dip through
    black at every scene boundary -- the narrated-master twin of make.py's mock
    preview transition. KEEP IN SYNC with make.py._fade_vf.
    """
    if fade <= 0:
        return ""
    dur = _probe_duration(video)
    if dur <= 2.5 * fade:
        return ""
    return (f"fade=t=in:st=0:d={fade:.3f},"
            f"fade=t=out:st={dur - fade:.3f}:d={fade:.3f}")


def _mux_content(video: Path, narration: Path, out: Path, lead: float, abr: str,
                 *, fade: float = 0.0) -> None:
    """Lay narration under video as a FULL-LENGTH track whose duration matches the
    video exactly: real silence for the lead-in (adelay), the narration, then
    silence padding out to the video's end (apad, capped by -shortest).

    Do NOT use -itsoffset here: it shifts the audio's start timestamp but leaves
    the stream ~lead+tail seconds shorter than the video. The concat demuxer then
    advances audio and video by each stream's own length, so the shortfall makes
    A/V drift apart scene by scene (and the gap grows with lead/tail). A
    video-length audio stream keeps every segment in sync, like _mux_silent.
    KEEP IN SYNC with make.py._mux_content."""
    vf = _fade_vf(video, fade)
    vcodec = (["-vf", vf, "-c:v", "libx264", "-preset", "medium", "-pix_fmt", "yuv420p"]
              if vf else ["-c:v", "copy"])
    lead_ms = max(int(round(lead * 1000)), 0)
    _run([
        "ffmpeg", "-y",
        "-i", str(video), "-i", str(narration),
        "-filter_complex", f"[1:a]adelay={lead_ms}:all=1,apad[a]",
        "-map", "0:v:0", "-map", "[a]",
        *vcodec, "-c:a", "aac", "-b:a", abr, "-ar", "48000", "-ac", "2",
        "-shortest", str(out),
    ])


def _mux_silent(video: Path, out: Path, abr: str, *, fade: float = 0.0) -> None:
    """Attach a uniform silent stereo track so every segment concats cleanly."""
    vf = _fade_vf(video, fade)
    vcodec = (["-vf", vf, "-c:v", "libx264", "-preset", "medium", "-pix_fmt", "yuv420p"]
              if vf else ["-c:v", "copy"])
    _run([
        "ffmpeg", "-y",
        "-i", str(video),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-map", "0:v:0", "-map", "1:a:0",
        *vcodec, "-c:a", "aac", "-b:a", abr, "-ar", "48000", "-ac", "2",
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
    sec_dir = _bootstrap.section_output_dir(meta)
    media_dir = out_root / "_media"
    audio_subdir = "audio_mimo" if deck_id.endswith("_mimo") else "audio"
    manifest_path = args.manifest or (sec_dir / audio_subdir / "manifest.json")

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
            _mux_content(video, narration, av, args.lead, args.audio_bitrate, fade=args.transition)
        else:
            print(f"[mux] {sid}: silent track", flush=True)
            _mux_silent(video, av, args.audio_bitrate, fade=args.transition)
        segments.append(av)

    sec_dir.mkdir(parents=True, exist_ok=True)
    output = args.output or (sec_dir / f"{deck_id}.mp4")
    print(f"[concat] stitching {len(segments)} scenes -> {output}", flush=True)
    _concat(segments, output, args.audio_bitrate)
    print(f"[done] wrote {output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

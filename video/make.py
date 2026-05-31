"""make.py -- single-entry orchestrator for the rebuilt video pipeline.

Replaces the gen-2 three-CLI chain (tts.py -> build.py -> mux.py) with ONE
command: parse -> synth -> render -> compose. The manual hand-off between stages
(and its no-cache, edit-one-word-rerun-everything debt) is gone; the retained
lower-layer assets are reused as-is:

  - narration.parse_say        split `say` into reveal-timed beats
  - audio.py                   WAV write / measure / concat
  - scene.LessonScene          audio-driven reveal alignment (the core insight)
  - blocks / templates / brand / theme   Direction B visuals

    python video/make.py --storyboard video/storyboards/ch01_inverse_functions.yml --backend mock

Stages:
  parse    read storyboard -> meta + scene specs + per-scene beats
  synth    one clip per beat (mock = silence sized by word count) + manifest.json
  render   Manim renders each scene silent; reveal hold = measured beat duration
  compose  ffmpeg lays narration under each scene, concats to output/<id>.mp4

Only `mock` synthesis is wired here. Real Gemini TTS is billed and needs explicit
per-run approval (CLAUDE.md), so it is intentionally not callable from this path.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()  # must precede any manim / yaml import

import yaml  # noqa: E402

from pipeline.audio import concat_wavs, silence_pcm, wav_duration, write_pcm_wav  # noqa: E402
from pipeline.narration import estimate_seconds, parse_say  # noqa: E402

QUALITY = {"low": "low_quality", "medium": "medium_quality", "high": "production_quality"}
LEAD_SECONDS = 0.3  # matches LessonScene's initial self.wait(0.3) before beat 1


# ---- small helpers ------------------------------------------------------

def _safe_stem(value: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in value)
    safe = "_".join(p for p in safe.split("_") if p)
    return safe or "beat"


def _text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


# ---- parse --------------------------------------------------------------

def load_storyboard(path: Path) -> dict:
    return yaml.safe_load(path.resolve().read_text(encoding="utf-8"))


def select_scenes(scenes: list[dict], selector: str) -> list[dict]:
    by_id = {s["id"]: s for s in scenes}
    if selector == "all":
        return scenes
    ids = [x.strip() for x in selector.split(",") if x.strip()]
    missing = [i for i in ids if i not in by_id]
    if missing:
        raise SystemExit(f"Unknown scene(s) {missing}. Available: {', '.join(by_id)}")
    return [by_id[i] for i in ids]


# ---- synth (mock) -------------------------------------------------------

def synth_scene(scene: dict, scene_number: int, audio_dir: Path, *, empty_seconds: float) -> dict:
    """Mock synthesis: one silent WAV per beat (sized by word count), then concat.

    Manifest entry shape matches what render (beat durations) and compose
    (per-scene narration WAV) consume.
    """
    scene_id = scene["id"]
    kind = scene.get("kind", "content")
    entry: dict = {"scene_number": scene_number, "scene_id": scene_id, "kind": kind}

    if kind != "content":
        entry.update({
            "narration_mode": "silent",
            "duration": float(scene.get("duration", 0.0)),
            "bgm": scene.get("bgm"),
        })
        return entry

    beats = parse_say(scene.get("say", ""))
    beat_dir = audio_dir / "beats" / f"{scene_number:02d}_{scene_id}"
    scene_wav = audio_dir / "scenes" / f"{scene_number:02d}_{scene_id}.wav"
    beat_paths: list[Path] = []
    manifest_beats: list[dict] = []
    timeline = 0.0
    for i, beat in enumerate(beats, start=1):
        seconds = estimate_seconds(beat.text) if beat.text else empty_seconds
        beat_path = beat_dir / f"{i:02d}_{_safe_stem(beat.reveal or f'beat_{i:02d}')}.wav"
        write_pcm_wav(beat_path, silence_pcm(seconds))
        dur = wav_duration(beat_path)
        beat_paths.append(beat_path)
        manifest_beats.append({
            "index": i, "id": f"beat_{i:02d}", "text": beat.text, "reveal": beat.reveal,
            "audio_file": str(beat_path.resolve()), "audio_seconds": round(dur, 3),
            "start_seconds": round(timeline, 3), "end_seconds": round(timeline + dur, 3),
            "text_hash": _text_hash(beat.text),
        })
        timeline += dur

    scene_seconds = concat_wavs(beat_paths, scene_wav)
    entry.update({
        "narration_mode": "beats",
        "audio_file": str(scene_wav.resolve()),
        "audio_seconds": round(scene_seconds, 3),
        "beat_count": len(manifest_beats),
        "script": " ".join(b.text for b in beats if b.text).strip(),
        "beats": manifest_beats,
    })
    return entry


def synth(meta: dict, scenes: list[dict], scene_numbers: dict[str, int],
          audio_dir: Path, backend: str, *, empty_seconds: float) -> dict:
    if backend != "mock":
        raise SystemExit(
            f"backend '{backend}' is not wired in make.py. Real Gemini TTS is "
            "billed and needs explicit per-run approval (see CLAUDE.md). Use "
            "--backend mock (offline, silent) for now."
        )
    audio_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict = {
        "deck_id": meta["id"], "backend": backend,
        "sample_rate": 24_000, "channels": 1, "sample_width": 2,
        "output_dir": str(audio_dir), "scenes": [],
    }
    for scene in scenes:
        print(f"[synth] {scene['id']} ...", flush=True)
        manifest["scenes"].append(
            synth_scene(scene, scene_numbers[scene["id"]], audio_dir, empty_seconds=empty_seconds)
        )
    return manifest


# ---- render -------------------------------------------------------------

def _beat_durations(manifest: dict) -> dict[str, list[float]]:
    out: dict[str, list[float]] = {}
    for s in manifest["scenes"]:
        if s.get("narration_mode") == "beats":
            out[s["scene_id"]] = [b["audio_seconds"] for b in s.get("beats", [])]
    return out


def render(meta: dict, scenes: list[dict], manifest: dict, out_dir: Path, quality: str):
    """Manim renders each scene silent; reuses scene.LessonScene align core."""
    from manim import tempconfig  # deferred: manim import is slow
    from pipeline.scene import LessonScene

    durations = _beat_durations(manifest)
    media_dir = out_dir / "_media"
    rendered: dict[str, Path | None] = {}
    failures = 0
    for scene in scenes:
        sid = scene["id"]
        print(f"[render] {sid} ...", flush=True)
        output_file = f"{meta['id']}__{sid}"
        LessonScene.spec = scene
        LessonScene.meta = meta
        LessonScene.beat_durations = durations.get(sid)
        try:
            with tempconfig({
                "quality": QUALITY[quality],
                "media_dir": str(media_dir),
                "output_file": output_file,
                "disable_caching": True,
                "verbosity": "ERROR",
            }):
                LessonScene().render()
            matches = sorted(media_dir.rglob(f"{output_file}.mp4"))
            rendered[sid] = matches[-1] if matches else None
            if rendered[sid] is None:
                print(f"[render] !! no mp4 for {output_file}", flush=True)
                failures += 1
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"[render] FAIL {sid}: {exc!r}", flush=True)
            traceback.print_exc()
    return rendered, failures


# ---- compose (ffmpeg) ---------------------------------------------------

def _ffmpeg(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("ffmpeg failed:\n" + " ".join(cmd) + "\n" + result.stderr[-1500:])


def _mux_content(video: Path, narration: Path, out: Path, lead: float, abr: str) -> None:
    _ffmpeg([
        "ffmpeg", "-y", "-i", str(video),
        "-itsoffset", f"{lead:.3f}", "-i", str(narration),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", abr, "-ar", "48000", "-ac", "2",
        str(out),
    ])


def _mux_silent(video: Path, out: Path, abr: str) -> None:
    _ffmpeg([
        "ffmpeg", "-y", "-i", str(video),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", abr, "-ar", "48000", "-ac", "2",
        "-shortest", str(out),
    ])


def _concat(segments: list[Path], out: Path, abr: str) -> None:
    list_file = out.parent / "_concat_av_list.txt"
    list_file.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in segments) + "\n",
        encoding="utf-8",
    )
    try:
        _ffmpeg([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
            "-c:v", "libx264", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", abr, str(out),
        ])
    finally:
        list_file.unlink(missing_ok=True)


def compose(scenes: list[dict], manifest: dict, rendered: dict[str, Path | None],
            out_dir: Path, *, lead: float, abr: str, output: Path) -> Path | None:
    narration_by_scene: dict[str, Path] = {}
    for s in manifest["scenes"]:
        if s.get("narration_mode") == "beats" and s.get("audio_file"):
            narration_by_scene[s["scene_id"]] = Path(s["audio_file"])

    av_dir = out_dir / "_av"
    av_dir.mkdir(parents=True, exist_ok=True)
    segments: list[Path] = []
    for scene in scenes:
        sid = scene["id"]
        video = rendered.get(sid)
        if video is None:
            print(f"[compose] missing rendered scene '{sid}'", flush=True)
            return None
        av = av_dir / f"{sid}.mp4"
        narration = narration_by_scene.get(sid)
        if narration and narration.exists():
            print(f"[compose] {sid}: narration under video", flush=True)
            _mux_content(video, narration, av, lead, abr)
        else:
            print(f"[compose] {sid}: silent track", flush=True)
            _mux_silent(video, av, abr)
        segments.append(av)

    print(f"[compose] concat {len(segments)} scenes -> {output}", flush=True)
    _concat(segments, output, abr)
    return output


# ---- orchestrate --------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--storyboard", required=True, type=Path)
    parser.add_argument("--backend", default="mock", choices=("mock", "gemini"))
    parser.add_argument("--scene", default="all", help="id, 'a,b,c', or 'all'")
    parser.add_argument("--quality", default="low", choices=sorted(QUALITY))
    parser.add_argument("--lead", type=float, default=LEAD_SECONDS)
    parser.add_argument("--audio-bitrate", default="192k")
    parser.add_argument("--empty-beat-seconds", type=float, default=0.45)
    args = parser.parse_args()

    data = load_storyboard(args.storyboard)
    meta = data["meta"]
    all_scenes = data["scenes"]
    scene_numbers = {s["id"]: i for i, s in enumerate(all_scenes, start=1)}
    scenes = select_scenes(all_scenes, args.scene)
    out_dir = _bootstrap.REPO_ROOT / "video" / "output"
    audio_dir = out_dir / "audio" / meta["id"]
    print(f"[parse] {meta['id']}: {len(scenes)}/{len(all_scenes)} scene(s)", flush=True)

    # synth
    manifest = synth(meta, scenes, scene_numbers, audio_dir, args.backend,
                     empty_seconds=args.empty_beat_seconds)
    manifest_path = audio_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[synth] manifest -> {manifest_path}", flush=True)

    # render
    rendered, failures = render(meta, scenes, manifest, out_dir, args.quality)
    if failures:
        print(f"[render] {failures} scene(s) failed; aborting before compose", flush=True)
        return 1

    # compose
    output = out_dir / f"{meta['id']}.mp4"
    result = compose(scenes, manifest, rendered, out_dir,
                     lead=args.lead, abr=args.audio_bitrate, output=output)
    if result is None:
        return 1
    print(f"[done] {result}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

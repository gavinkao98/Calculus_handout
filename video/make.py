"""make.py -- single-entry orchestrator for the rebuilt video pipeline.

Replaces the gen-2 three-CLI chain with ONE command: parse -> synth -> render ->
compose. The manual hand-off between stages (and its no-cache,
edit-one-word-rerun-everything debt) is gone; the retained lower-layer assets are
reused as-is:

  - narration.parse_say        split `say` into reveal-timed beats
  - audio.py                   WAV write / measure / concat
  - scene.LessonScene          audio-driven reveal alignment (the core insight)
  - blocks / templates / brand / theme   Direction B visuals

    python video/make.py --storyboard video/storyboards/_demo_derivation.yml --backend mock

Stages:
  parse    read storyboard -> meta + scene specs + per-scene beats
  synth    one clip per beat (mock = silence sized by word count) + manifest.json
  render   Manim renders each scene silent; reveal hold = measured beat duration
  compose  ffmpeg lays narration under each scene, concats to output/<id>.mp4

Only `mock` synthesis is wired here. Real audio is the MiMo route: run
`tts.py --backend mimo` (billed/external -- needs per-run approval, CLAUDE.md),
then `make.py --reuse-audio` to render against that real manifest.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()  # must precede any manim / yaml import

import yaml  # noqa: E402

from pipeline.audio import concat_wavs, silence_pcm, wav_duration, write_pcm_wav  # noqa: E402
from pipeline import captions  # noqa: E402
from pipeline.derived_check import check_derived_freshness, text_sha256  # noqa: E402
from pipeline.narration import estimate_seconds, parse_say  # noqa: E402
from pipeline.tts import read_manifest_status, _has_audio  # noqa: E402 (manim-free fail-closed guard reuse)
from pipeline import house_audio  # noqa: E402
from pipeline.timing import (  # noqa: E402
    SCENE_LEAD_SECONDS,
    SCENE_TAIL_SECONDS,
    SYNC_TOLERANCE_SECONDS,
    beat_extra_padding_seconds,
    expected_content_video_seconds,
    stock_animation_seconds,
    text_hash,
)

# Render tiers (convention in DESIGN.md): TESTING/preview renders use 1080p
# ("high", the default) -- crisp enough for visual QA / VLM frame critique without
# 4K's cost; only the FINAL delivery uses 4K ("4k"). low/medium are fast scratch
# previews (manim presets); high/4k set explicit dims in render() to control fps.
QUALITY = {"low": "low_quality", "medium": "medium_quality"}
LEAD_SECONDS = SCENE_LEAD_SECONDS


# ---- small helpers ------------------------------------------------------

def _safe_stem(value: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in value)
    safe = "_".join(p for p in safe.split("_") if p)
    return safe or "beat"


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
            "text_hash": text_hash(beat.text),
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
            f"backend '{backend}' is not wired in make.py. Real audio is the MiMo "
            "route: run `tts.py --backend mimo` (billed/external, CLAUDE.md), then "
            "`make.py --reuse-audio`. make.py itself only does --backend mock."
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
        if s.get("narration_mode") in ("beats", "scene_aligned"):
            out[s["scene_id"]] = [b["audio_seconds"] for b in s.get("beats", [])]
    return out


def _check_manifest_schema(manifest: dict) -> None:
    """Refuse a manifest newer than this make.py understands, rather than silently
    misreading it. schema 1 (no field) and schema 2 are both supported."""
    schema = int(manifest.get("schema", 1))
    if schema > 2:
        raise SystemExit(
            f"audio manifest schema {schema} is newer than this make.py supports "
            "(max 2); upgrade the pipeline."
        )


def _scene_manifest_map(manifest: dict) -> dict[str, dict]:
    return {s.get("scene_id", ""): s for s in manifest.get("scenes", [])}


def _validate_scene_aligned(sid: str, scene: dict, beats: list, entry: dict, problems: list) -> None:
    """Render-time freshness for a reused scene_aligned entry (design §3/§9 row 2):
    scene WAV present + duration matches, alignment artifacts present, validation passed,
    scene_text_hash + per-beat reveal/text_hash unchanged. NO per-beat audio_file
    (scene_aligned stores one scene WAV). Deliberately does NOT check the aligner model:
    make.py has no aligner config to compare against, and aligner freshness (§3 row 3) is
    tts.py's job -- whatever model produced the persisted alignment (base.en normally,
    small.en if the arbiter won) is fine to render."""
    manifest_beats = entry.get("beats", [])
    if len(manifest_beats) != len(beats):
        problems.append(f"{sid}: beat count changed ({len(manifest_beats)} manifest, {len(beats)} storyboard)")
        return
    transcript = " ".join(b.text for b in beats if b.text).strip()
    if entry.get("scene_text_hash") != text_hash(transcript):
        problems.append(f"{sid}: scene_text_hash stale (storyboard text changed) -> resynthesize")
    af = entry.get("audio_file"); ap = Path(af) if af else None
    audio_seconds = float(entry.get("audio_seconds") or 0.0)
    if ap is None or not ap.exists():
        problems.append(f"{sid}: scene audio file missing: {af!r}")
    elif abs(wav_duration(ap) - audio_seconds) > SYNC_TOLERANCE_SECONDS:
        problems.append(f"{sid}: scene audio WAV duration differs from manifest")
    if audio_seconds <= 0.0:
        problems.append(f"{sid}: scene audio_seconds is not positive")
    align = entry.get("alignment") or {}
    for key in ("words_file", "aligned_file"):
        p = align.get(key)
        if not p or not Path(p).exists():
            problems.append(f"{sid}: alignment {key} missing: {p!r}")
    if (entry.get("validation") or {}).get("status") not in ("pass", "pass_with_warnings"):
        problems.append(f"{sid}: validation.status={ (entry.get('validation') or {}).get('status')!r }")
    for i, (b, mb) in enumerate(zip(beats, manifest_beats), start=1):
        if mb.get("reveal") != b.reveal:
            problems.append(f"{sid} beat {i:02d}: reveal changed (manifest={mb.get('reveal')!r}, storyboard={b.reveal!r})")
        stored = mb.get("text_hash")
        if stored and stored != text_hash(b.text):
            problems.append(f"{sid} beat {i:02d}: text_hash changed")


def _validate_reuse_manifest(meta: dict, scenes: list[dict], manifest: dict) -> None:
    """Refuse stale or partial real-audio manifests before rendering."""
    problems: list[str] = []
    if manifest.get("deck_id") != meta.get("id"):
        problems.append(
            f"deck_id mismatch: manifest={manifest.get('deck_id')!r}, storyboard={meta.get('id')!r}"
        )

    by_scene = _scene_manifest_map(manifest)
    for scene in scenes:
        if scene.get("kind", "content") != "content":
            continue
        beats = parse_say(scene.get("say", ""))
        if not beats:
            continue
        sid = scene["id"]
        entry = by_scene.get(sid)
        if entry is None:
            problems.append(f"{sid}: missing from audio manifest")
            continue
        mode = entry.get("narration_mode")
        if mode not in ("beats", "scene_aligned"):
            problems.append(f"{sid}: manifest narration_mode={mode!r}, expected 'beats' or 'scene_aligned'")
            continue
        if mode == "scene_aligned":
            _validate_scene_aligned(sid, scene, beats, entry, problems)
            continue

        manifest_beats = entry.get("beats", [])
        if len(manifest_beats) != len(beats):
            problems.append(f"{sid}: beat count changed ({len(manifest_beats)} manifest, {len(beats)} storyboard)")
            continue

        scene_audio_value = entry.get("audio_file")
        scene_audio = Path(scene_audio_value) if scene_audio_value else None
        scene_audio_seconds = float(entry.get("audio_seconds") or 0.0)
        if scene_audio is None or not scene_audio.exists():
            problems.append(f"{sid}: scene audio file missing: {scene_audio_value!r}")
        elif abs(wav_duration(scene_audio) - scene_audio_seconds) > SYNC_TOLERANCE_SECONDS:
            problems.append(f"{sid}: scene audio WAV duration differs from manifest")
        if scene_audio_seconds <= 0.0:
            problems.append(f"{sid}: scene audio_seconds is not positive")

        for index, (beat, manifest_beat) in enumerate(zip(beats, manifest_beats, strict=True), start=1):
            label = f"{sid} beat {index:02d}"
            if manifest_beat.get("reveal") != beat.reveal:
                problems.append(
                    f"{label}: reveal changed (manifest={manifest_beat.get('reveal')!r}, "
                    f"storyboard={beat.reveal!r})"
                )
            expected_hash = text_hash(beat.text)
            stored_hash = manifest_beat.get("text_hash")
            if stored_hash and stored_hash != expected_hash:
                problems.append(f"{label}: text_hash changed ({stored_hash} != {expected_hash})")
            elif not stored_hash and manifest_beat.get("text") != beat.text:
                problems.append(f"{label}: text changed and manifest has no text_hash")
            beat_audio_value = manifest_beat.get("audio_file")
            beat_audio = Path(beat_audio_value) if beat_audio_value else None
            if beat_audio is None or not beat_audio.exists():
                problems.append(f"{label}: beat audio file missing: {beat_audio_value!r}")
            if float(manifest_beat.get("audio_seconds") or 0.0) <= 0.0:
                problems.append(f"{label}: audio_seconds is not positive")

    if problems:
        details = "\n".join(f"  - {p}" for p in problems[:25])
        extra = "" if len(problems) <= 25 else f"\n  ... and {len(problems) - 25} more"
        raise SystemExit(
            "--reuse-audio manifest is stale or incomplete:\n"
            f"{details}{extra}\n"
            "Run tts.py for the current storyboard/scene selection, or delete the stale manifest."
        )


def _warn_short_beats(meta: dict, scenes: list[dict], manifest: dict) -> None:
    """Warn when scene.py must pad a beat because reveal animation exceeds audio."""
    from pipeline.templates import build_blocks  # deferred: imports manim objects

    durations = _beat_durations(manifest)
    issues: list[str] = []
    for scene in scenes:
        if scene.get("kind", "content") != "content":
            continue
        sid = scene["id"]
        beat_seconds = durations.get(sid)
        if not beat_seconds:
            continue
        ground = "dark"
        blocks = build_blocks(scene, {"ground": ground, "meta": meta})
        by_id = {b.id: b for b in blocks}
        for index, beat in enumerate(parse_say(scene.get("say", "")), start=1):
            if index > len(beat_seconds) or not beat.reveal:
                continue
            block = by_id.get(beat.reveal)
            if block is None or block.static:
                continue
            anim_seconds = stock_animation_seconds(block.anim)
            if anim_seconds is None:
                continue
            extra = beat_extra_padding_seconds(float(beat_seconds[index - 1]), anim_seconds)
            if extra > SYNC_TOLERANCE_SECONDS:
                issues.append(
                    f"{sid} beat {index:02d} ({beat.reveal}): audio={beat_seconds[index - 1]:.3f}s, "
                    f"reveal_anim={anim_seconds:.3f}s, scene.py adds ~{extra:.3f}s"
                )

    if issues:
        print(f"[sync] {len(issues)} short/reveal-only beat warning(s):", flush=True)
        for issue in issues[:20]:
            print(f"  WARN   {issue}", flush=True)
        if len(issues) > 20:
            print(f"  WARN   ... and {len(issues) - 20} more", flush=True)
        print("[sync] consider merging consecutive {show} markers into a narrated beat.", flush=True)
    else:
        print("[sync] beat timing clean", flush=True)


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
        cfg = {
            "media_dir": str(media_dir),
            "output_file": output_file,
            "disable_caching": True,
            "verbosity": "ERROR",
        }
        if quality == "high":
            # TESTING standard: 1080p @ 30fps -- crisp for visual QA / VLM frame
            # critique, ~half the render time of 60fps, and fps is irrelevant to
            # the stills the critic extracts.
            cfg["pixel_width"] = 1920
            cfg["pixel_height"] = 1080
            cfg["frame_rate"] = 30
        elif quality == "4k":
            # FINAL delivery: the project standard 4K @ 60fps (manim fourk_quality).
            # A storyboard's meta.video overrides if set; the 3840x2160@60 default
            # enforces the standard when it is omitted.
            v = meta.get("video", {}) or {}
            cfg["pixel_width"] = int(v.get("w", 3840))
            cfg["pixel_height"] = int(v.get("h", 2160))
            cfg["frame_rate"] = int(v.get("fps", 60))
        else:
            cfg["quality"] = QUALITY[quality]
        try:
            with tempconfig(cfg):
                LessonScene().render()
            # _media keeps a per-resolution subdir (480p15/, 1080p30/, ...) across
            # runs, so several matches can exist. Take the freshest (the one this
            # render just wrote) -- sorting by name would pick "480p15" over
            # "1080p30" and mux a stale low-res clip.
            matches = list(media_dir.rglob(f"{output_file}.mp4"))
            rendered[sid] = max(matches, key=lambda p: p.stat().st_mtime) if matches else None
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


def _probe_duration(path: Path) -> float:
    """Seconds of a media file via ffprobe; 0.0 if it cannot be read."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0.0


def _git_commit() -> str:
    """Short HEAD for timeline provenance; 'unknown' if git is unavailable."""
    try:
        out = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True, cwd=str(_bootstrap.REPO_ROOT))
        return out.stdout.strip() or "unknown"
    except Exception:  # noqa: BLE001 - provenance nicety, never fatal
        return "unknown"


def _write_text_atomic(path: Path, text: str) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def _mock_synth_guard(*, status: str, existing: dict | None, audio_dir: Path,
                      force_clobber: bool) -> str | None:
    """Abort message (else None) BEFORE mock synth would overwrite audio -- mock silence
    must never clobber real Dean WAVs. The old make.py guard only aborted on a VALID
    non-mock backend string, so a corrupt manifest (json fails -> backend=None) or a
    deleted manifest with WAVs still present fell through to synth() and overwrote real
    audio. read_manifest_status catches both; this mirrors tts.py's overwrite_guard."""
    if force_clobber:
        return None
    if status == "corrupt":
        return ("manifest is corrupt/invalid and may shadow real WAVs; refusing to mock-overwrite. "
                "Pass --reuse-audio, or --force-clobber to rebuild with mock.")
    if status == "absent" and _has_audio(audio_dir):
        return (f"no valid manifest but WAVs already exist under {audio_dir}; refusing to "
                "mock-overwrite. Pass --reuse-audio, or --force-clobber.")
    if status == "ok" and (existing or {}).get("backend") not in (None, "mock"):
        return (f"existing manifest backend={(existing or {}).get('backend')!r} is real; refusing "
                "to overwrite with mock. Pass --reuse-audio, or --force-clobber.")
    return None


def _audit_render_sync(scenes: list[dict], manifest: dict, rendered: dict[str, Path | None],
                       *, lead: float) -> bool:
    """Return True if rendered scene lengths are compatible with manifest audio."""
    by_scene = _scene_manifest_map(manifest)
    fatals: list[str] = []
    warnings: list[str] = []
    for scene in scenes:
        if scene.get("kind", "content") != "content":
            continue
        sid = scene["id"]
        entry = by_scene.get(sid)
        video = rendered.get(sid)
        if not entry or entry.get("narration_mode") not in ("beats", "scene_aligned") or video is None:
            continue
        audio_seconds = float(entry.get("audio_seconds") or 0.0)
        if entry.get("narration_mode") == "scene_aligned":
            # by construction sum(beat durations)==audio_seconds (mapper); a mismatch
            # means a hand-edited manifest -> refuse rather than render out of sync.
            beat_sum = sum(float(b.get("audio_seconds") or 0.0) for b in entry.get("beats", []))
            if abs(beat_sum - audio_seconds) > SYNC_TOLERANCE_SECONDS:
                fatals.append(f"{sid}: sum(beat durations)={beat_sum:.3f}s != audio_seconds="
                              f"{audio_seconds:.3f}s (hand-edited manifest?)")
        actual = _probe_duration(video)
        audio_end = lead + audio_seconds
        expected = expected_content_video_seconds(audio_seconds, lead_seconds=lead)
        if actual + SYNC_TOLERANCE_SECONDS < audio_end:
            fatals.append(
                f"{sid}: video={actual:.3f}s, narration ends at {audio_end:.3f}s "
                f"(audio={audio_seconds:.3f}s + lead={lead:.3f}s)"
            )
        elif abs(actual - expected) > SYNC_TOLERANCE_SECONDS:
            warnings.append(
                f"{sid}: video={actual:.3f}s, expected ~{expected:.3f}s "
                f"(audio={audio_seconds:.3f}s + lead/tail={lead + SCENE_TAIL_SECONDS:.3f}s)"
            )

    if fatals:
        print(f"[sync] {len(fatals)} render/audio fatal mismatch(es):", flush=True)
        for item in fatals:
            print(f"  ERROR  {item}", flush=True)
        return False
    if warnings:
        print(f"[sync] {len(warnings)} render/audio length warning(s):", flush=True)
        for item in warnings[:20]:
            print(f"  WARN   {item}", flush=True)
        if len(warnings) > 20:
            print(f"  WARN   ... and {len(warnings) - 20} more", flush=True)
    else:
        print("[sync] render/audio lengths clean", flush=True)
    return True


def _fade_vf(video: Path, fade_in: float, fade_out: float) -> str:
    """Video filter: fade in from black at the start (fade_in) and/or out to black at
    the end (fade_out); either side may be 0 for a hard edge there. Per-boundary values
    (T9) let brand-frame boundaries keep the dark handoff while content-content
    boundaries are tightened independently. Empty when neither side fades or the clip is
    too short to carry a requested fade. Concatenated, faded edges give a ~(in+out) dip
    through black at each boundary (matching the intro/outro dark-handoff motif)."""
    dur = _probe_duration(video)
    parts = []
    if fade_in > 0 and dur > 2.5 * fade_in:
        parts.append(f"fade=t=in:st=0:d={fade_in:.3f}")
    if fade_out > 0 and dur > 2.5 * fade_out:
        parts.append(f"fade=t=out:st={dur - fade_out:.3f}:d={fade_out:.3f}")
    return ",".join(parts)


_BRAND_KINDS = {"intro", "outro", "divider"}


def _segment_fades(kinds: list[str], transition: float, intra_act: float) -> list[tuple[float, float]]:
    """(fade_in, fade_out) per segment (T9). Every boundary touching a brand frame
    (intro/outro/divider) and the film's own open/close uses `transition`; a
    content-content boundary uses `intra_act`. Both sides of one boundary get the SAME
    value, so the dip through black at that boundary is symmetric."""
    n = len(kinds)

    def boundary(a: int, b: int) -> float:
        return transition if (kinds[a] in _BRAND_KINDS or kinds[b] in _BRAND_KINDS) else intra_act

    return [(transition if i == 0 else boundary(i - 1, i),
             transition if i == n - 1 else boundary(i, i + 1)) for i in range(n)]


# Single, uniform video encode for every muxed segment (T8/F13). Encoding ONCE here
# (even when there is no fade) lets _concat stream-copy instead of re-encoding, so the
# chain is manim-render -> one mux encode -> concat copy, not up to three generations.
# CRF 18 (visually lossless-ish), explicit BT.709 primaries/transfer/matrix (tag the
# HD colour space instead of leaving it unspecified), yuv420p for broad playback.
# The x264-params ARE needed on top of ffmpeg's -color_* flags: libx264 alone writes
# only matrix_coefficients into the H.264 VUI, leaving colour_primaries/transfer
# "unknown" (verified empirically); colorprim/transfer/colormatrix make all three land.
ENCODE_V = ["-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
            "-color_trc", "bt709", "-colorspace", "bt709",
            "-x264-params", "colorprim=bt709:transfer=bt709:colormatrix=bt709"]


def _mux_content(video: Path, narration: Path, out: Path, lead: float, abr: str,
                 *, fade_in: float = 0.0, fade_out: float = 0.0) -> None:
    """Lay narration under video as a FULL-LENGTH track whose duration matches the
    video exactly: real silence for the lead-in (adelay), the narration, then
    silence padding out to the video's end (apad, capped by -shortest).

    Do NOT use -itsoffset here: it shifts the audio's start timestamp but leaves
    the stream ~lead+tail seconds shorter than the video. The concat demuxer then
    advances audio and video by each stream's own length, so the shortfall makes
    A/V drift apart scene by scene (and the gap grows with lead/tail). A
    video-length audio stream keeps every segment in sync, like _mux_silent."""
    vf = _fade_vf(video, fade_in, fade_out)
    vcodec = ["-vf", vf, *ENCODE_V] if vf else [*ENCODE_V]   # always encode once (T8)
    lead_ms = max(int(round(lead * 1000)), 0)
    _ffmpeg([
        "ffmpeg", "-y", "-i", str(video), "-i", str(narration),
        "-filter_complex", f"[1:a]adelay={lead_ms}:all=1,apad[a]",
        "-map", "0:v:0", "-map", "[a]",
        *vcodec, "-c:a", "aac", "-b:a", abr, "-ar", "48000", "-ac", "2",
        "-shortest", str(out),
    ])


def _mux_silent(video: Path, out: Path, abr: str, *, fade_in: float = 0.0, fade_out: float = 0.0) -> None:
    vf = _fade_vf(video, fade_in, fade_out)
    vcodec = ["-vf", vf, *ENCODE_V] if vf else [*ENCODE_V]   # always encode once (T8)
    _ffmpeg([
        "ffmpeg", "-y", "-i", str(video),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-map", "0:v:0", "-map", "1:a:0",
        *vcodec, "-c:a", "aac", "-b:a", abr, "-ar", "48000", "-ac", "2",
        "-shortest", str(out),
    ])


def _mux_cue(video: Path, cue: Path, out: Path, abr: str, *,
             gain: float, cue_fade_out: float, fade_in: float = 0.0, fade_out: float = 0.0) -> None:
    """Lay a house cue (intro/outro bed or divider stinger) under a brand scene
    that carries no narration. The cue is gained, faded out so it lands cleanly at
    the scene's end (beds run longer than the intro scene, so they must fade rather
    than clip), then padded with silence to the video length (apad + -shortest) --
    the same full-length-audio discipline as _mux_silent/_mux_content, so the
    concat demuxer keeps every segment in A/V sync. Cues are 48 kHz stereo (the
    output format), so no resample is needed."""
    vf = _fade_vf(video, fade_in, fade_out)
    vcodec = ["-vf", vf, *ENCODE_V] if vf else [*ENCODE_V]   # always encode once (T8)
    cue_fade_start = max(_probe_duration(video) - cue_fade_out, 0.0)
    afilter = (f"[1:a]volume={gain:.3f},"
               f"afade=t=out:st={cue_fade_start:.3f}:d={cue_fade_out:.3f},apad[a]")
    _ffmpeg([
        "ffmpeg", "-y", "-i", str(video), "-i", str(cue),
        "-filter_complex", afilter,
        "-map", "0:v:0", "-map", "[a]",
        *vcodec, "-c:a", "aac", "-b:a", abr, "-ar", "48000", "-ac", "2",
        "-shortest", str(out),
    ])


def _concat(segments: list[Path], out: Path, abr: str) -> None:
    list_file = out.parent / "_concat_av_list.txt"
    list_file.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in segments) + "\n",
        encoding="utf-8",
    )
    try:
        # Every segment is already encoded identically (ENCODE_V) + AAC, so concat
        # stream-copies -- no extra video generation -- and +faststart moves the moov
        # atom to the front for progressive playback (T8/F13).
        _ffmpeg([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
            "-c", "copy", "-movflags", "+faststart", str(out),
        ])
    finally:
        list_file.unlink(missing_ok=True)


def compose(scenes: list[dict], manifest: dict, rendered: dict[str, Path | None],
            out_dir: Path, *, lead: float, abr: str, output: Path, transition: float = 0.0,
            intra_act: float | None = None, meta: dict, quality: str,
            storyboard_path: Path, manifest_path: Path) -> Path | None:
    # NB4: --lead only shifts the muxed audio; render() does NOT take lead (LessonScene
    # always waits SCENE_LEAD_SECONDS), so a non-default lead desyncs A/V and subtitles.
    # We don't touch render here -- just warn loudly. Acceptance never ships a non-default lead.
    if abs(lead - SCENE_LEAD_SECONDS) > 1e-6:
        print(f"[compose] WARN: --lead {lead} != render lead {SCENE_LEAD_SECONDS}s; audio and "
              f"subtitles will desync from on-screen reveals (render does not take lead)", flush=True)

    # T9: per-boundary fade. intra_act defaults to `transition` (behaviour unchanged);
    # an A/B pass can set --intra-act-transition 0 to tighten only content-content cuts.
    intra = intra_act if intra_act is not None else transition
    seg_fades = _segment_fades([s.get("kind", "content") for s in scenes], transition, intra)

    narration_by_scene: dict[str, Path] = {}
    mode_by_scene: dict[str, str | None] = {}
    for s in manifest["scenes"]:
        mode_by_scene[s["scene_id"]] = s.get("narration_mode")
        if s.get("narration_mode") in ("beats", "scene_aligned") and s.get("audio_file"):
            narration_by_scene[s["scene_id"]] = Path(s["audio_file"])

    av_dir = out_dir / "_av" / _safe_stem(output.stem)
    av_dir.mkdir(parents=True, exist_ok=True)
    segments: list[Path] = []
    timeline_scenes: list[dict] = []
    offset = 0.0
    for i, scene in enumerate(scenes):
        sid = scene["id"]
        video = rendered.get(sid)
        if video is None:
            print(f"[compose] missing rendered scene '{sid}'", flush=True)
            return None
        av = av_dir / f"{sid}.mp4"
        fin, fout = seg_fades[i]
        narration = narration_by_scene.get(sid)
        cue = house_audio.cue_for_scene(scene)
        if narration and narration.exists():
            print(f"[compose] {sid}: narration under video", flush=True)
            _mux_content(video, narration, av, lead, abr, fade_in=fin, fade_out=fout)
        elif cue is not None and cue.path.exists():
            print(f"[compose] {sid}: house cue {cue.path.name}", flush=True)
            _mux_cue(video, cue.path, av, abr, gain=cue.gain, cue_fade_out=cue.fade_out,
                     fade_in=fin, fade_out=fout)
        else:
            if cue is not None:
                print(f"[compose] {sid}: house cue file missing ({cue.path}); silent", flush=True)
            print(f"[compose] {sid}: silent track", flush=True)
            _mux_silent(video, av, abr, fade_in=fin, fade_out=fout)
        segments.append(av)
        seg_dur = _probe_duration(av)
        timeline_scenes.append(captions.build_timeline_scene(
            scene, meta, start=offset, end=offset + seg_dur,
            narration_mode=mode_by_scene.get(sid)))
        offset += seg_dur

    print(f"[compose] concat {len(segments)} scenes -> {output}", flush=True)
    _concat(segments, output, abr)

    # sidecars (only after concat succeeds; atomic, so a failure leaves no half file).
    # names bound to the OUTPUT STEM (B6) so a --scene subset / A-B run never clobbers
    # another run's sidecars. lead_seconds is recorded so captions time off it, not the
    # render's hard-coded lead (B6).
    stem = output.with_suffix("")
    timeline = {
        "deck_id": meta.get("id"), "output": output.name, "quality": quality,
        "lead_seconds": lead, "scenes": timeline_scenes,
        "provenance": {
            "storyboard_sha256": _safe_storyboard_sha(storyboard_path),
            "manifest_path": str(manifest_path),
            "git_commit": _git_commit(),
        },
    }
    _write_text_atomic(Path(f"{stem}.timeline.json"),
                       json.dumps(timeline, indent=2, ensure_ascii=False) + "\n")
    _write_text_atomic(Path(f"{stem}.vtt"), captions.to_vtt(manifest, timeline))
    chapters = captions.to_chapters(timeline)
    if chapters.strip():
        _write_text_atomic(Path(f"{stem}.chapters.txt"), chapters)
    print(f"[compose] sidecars -> {stem.name}.timeline.json / .vtt"
          f"{' / .chapters.txt' if chapters.strip() else ''}", flush=True)
    return output


def _safe_storyboard_sha(path: Path) -> str:
    try:
        return text_sha256(Path(path))
    except Exception:  # noqa: BLE001 - provenance nicety, never fatal
        return "unknown"


# ---- orchestrate --------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--storyboard", required=True, type=Path)
    parser.add_argument("--backend", default="mock", choices=("mock",),
                        help="only mock (silent) is wired here; real audio = tts.py mimo + --reuse-audio")
    parser.add_argument("--force-clobber", action="store_true",
                        help="allow mock synth to overwrite a corrupt/real audio manifest or orphan "
                             "WAVs (default: fail-closed so mock silence never clobbers real Dean audio)")
    parser.add_argument("--scene", default="all", help="id, 'a,b,c', or 'all'")
    parser.add_argument("--quality", default="high", choices=("low", "medium", "high", "4k"),
                        help="low/medium = fast scratch (480p/720p); high = 1080p testing "
                             "standard (default); 4k = final delivery")
    parser.add_argument("--lead", type=float, default=LEAD_SECONDS)
    parser.add_argument("--audio-bitrate", default="192k")
    parser.add_argument("--transition", type=float, default=0.2,
                        help="per-side fade-through-black at every scene boundary, "
                             "in seconds (0 = hard cuts). The black dip between two "
                             "scenes is ~2x this; the film also opens/closes on black.")
    parser.add_argument("--intra-act-transition", type=float, default=None,
                        help="per-side fade at CONTENT-CONTENT boundaries only (default: "
                             "same as --transition). Set 0 to hard-cut within an act while "
                             "brand-frame boundaries keep --transition (T9 A/B knob).")
    parser.add_argument("--output", type=Path, default=None,
                        help="explicit output mp4 path (default: derived from meta.id / --scene; "
                             "give distinct names for A/B builds so they don't overwrite).")
    parser.add_argument("--empty-beat-seconds", type=float, default=0.45)
    parser.add_argument("--reuse-audio", action="store_true",
                        help="skip synth; reuse the audio manifest already produced by "
                             "tts.py (real-voice render path -- e.g. --backend mimo)")
    parser.add_argument("--skip-lint", action="store_true",
                        help="skip the pre-render storyboard garble lint")
    parser.add_argument("--skip-sizecheck", action="store_true",
                        help="skip the pre-render stacked-prose size-consistency guard")
    parser.add_argument("--skip-schema", action="store_true",
                        help="skip the pre-render storyboard structure validation")
    args = parser.parse_args()

    data = load_storyboard(args.storyboard)

    # refuse a stale *_mimo.yml before any schema/render work (F2 drift guard);
    # returns None for non-generated/malformed decks, so schema still owns those.
    stale = check_derived_freshness(args.storyboard.resolve(), data)
    if stale:
        raise SystemExit(f"[freshness] {stale}")

    # validate structure first -- a malformed storyboard (missing meta/scenes, bad
    # scene kind, duplicate id, unclosed {show}) is caught before lint/render.
    if not args.skip_schema:
        from pipeline.schema import schema_storyboard
        issues = schema_storyboard(data)
        errors = [m for s, m in issues if s == "error"]
        warns = [m for s, m in issues if s == "warn"]
        for msg in warns:
            print(f"  WARN   {msg}", flush=True)
        if errors:
            print(f"[schema] {len(errors)} error(s) -- aborting (use --skip-schema to bypass):", flush=True)
            for msg in errors:
                print(f"  SCHEMA {msg}", flush=True)
            return 2
        print("[schema] structure OK" + (f" ({len(warns)} warning(s))" if warns else ""), flush=True)

    # OTF provenance (warn-default; gates only when meta.otf_enforce is True) -- spec §4:
    # deterministic provenance check runs at the schema/lint stage that gates render.
    from pipeline import provenance as _prov
    _repo_root = Path(__file__).resolve().parent.parent   # video/make.py -> repo root
    _meta = data.get("meta") if isinstance(data, dict) else None
    _meta = _meta if isinstance(_meta, dict) else {}
    _enforce = bool(_meta.get("otf_enforce"))
    _loci = _prov.Loci.from_deck(_meta, _repo_root)
    _prov_issues = _prov.provenance_issues(data, _loci, enforce=_enforce)
    if _prov_issues:
        _p_err = sum(1 for s, _ in _prov_issues if s == "error")
        print(f"[provenance] {len(_prov_issues)} finding(s)"
              f"{' (ENFORCED)' if _enforce else ' (warn-only; set meta.otf_enforce to gate)'}", flush=True)
        for _sev, _msg in _prov_issues:
            print(f"  {'ERROR' if _sev == 'error' else 'WARN '}  {_msg}", flush=True)
        if _p_err:
            print(f"[provenance] {_p_err} error(s) -- aborting (fix refs or unset meta.otf_enforce):", flush=True)
            return 2

    # Pedagogy structural checks (warn-default; gates only when meta.pedagogy_enforce is True)
    from pipeline import pedagogy as _ped
    _ped_enforce = bool(_meta.get("pedagogy_enforce"))
    _ped_issues = _ped.pedagogy_issues(data, enforce=_ped_enforce)
    if _ped_issues:
        _ped_err = sum(1 for s, _ in _ped_issues if s == "error")
        print(f"[pedagogy] {len(_ped_issues)} finding(s)"
              f"{' (ENFORCED)' if _ped_enforce else ' (warn-only; set meta.pedagogy_enforce to gate)'}", flush=True)
        for _sev, _msg in _ped_issues:
            print(f"  {'ERROR' if _sev == 'error' else 'WARN '}  {_msg}", flush=True)
        if _ped_err:
            print(f"[pedagogy] {_ped_err} error(s) -- aborting (fix scaffold/registry or unset meta.pedagogy_enforce):", flush=True)
            return 2

    # lint before doing any work -- catches render-garble ($f$ / \\ printed
    # literally, unbalanced $) statically, so it never reaches the video.
    if not args.skip_lint:
        from pipeline.lint import lint_storyboard
        issues = lint_storyboard(data)
        errors = [m for s, m in issues if s == "error"]
        warns = [m for s, m in issues if s == "warn"]
        for msg in warns:
            print(f"  WARN   {msg}", flush=True)
        if errors:
            print(f"[lint] {len(errors)} error(s) -- aborting (use --skip-lint to bypass):", flush=True)
            for msg in errors:
                print(f"  ERROR  {msg}", flush=True)
            return 2
        print("[lint] clean" + (f" ({len(warns)} warning(s))" if warns else ""), flush=True)

    meta = data["meta"]
    all_scenes = data["scenes"]
    scene_numbers = {s["id"]: i for i, s in enumerate(all_scenes, start=1)}
    scenes = select_scenes(all_scenes, args.scene)

    # size guard: stacked prose siblings (recap points, proof steps, ...) must
    # render at one size. Checks only the scenes about to render (builds blocks,
    # no video), so a regression of "wrap, don't shrink" is caught before render.
    if not args.skip_sizecheck:
        from pipeline.sizecheck import check_scenes
        issues = check_scenes(meta, scenes)
        errors = [m for s, m in issues if s == "error"]
        warns = [m for s, m in issues if s == "warn"]
        for msg in warns:
            print(f"  WARN   {msg}", flush=True)
        if errors:
            print(f"[sizecheck] {len(errors)} error(s) -- aborting (use --skip-sizecheck to bypass):", flush=True)
            for msg in errors:
                print(f"  SIZE   {msg}", flush=True)
            return 2
        print("[sizecheck] consistent" + (f" ({len(warns)} warning(s))" if warns else ""), flush=True)

    out_dir = _bootstrap.REPO_ROOT / "video" / "output"
    sec_dir = _bootstrap.section_output_dir(meta)
    audio_dir = sec_dir / "audio" if not meta["id"].endswith("_mimo") else sec_dir / "audio_mimo"
    manifest_path = audio_dir / "manifest.json"
    print(f"[parse] {meta['id']}: {len(scenes)}/{len(all_scenes)} scene(s)", flush=True)

    # synth -- or reuse real audio produced separately by tts.py (billed/external
    # synthesis stays out of make.py per CLAUDE.md; this only re-reads its output).
    if args.reuse_audio:
        if not manifest_path.exists():
            raise SystemExit(
                f"--reuse-audio: no manifest at {manifest_path}. Run tts.py (real "
                "backend) for this storyboard first."
            )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        print(f"[synth] reusing existing audio manifest -> {manifest_path}", flush=True)
        _check_manifest_schema(manifest)
        _validate_reuse_manifest(meta, scenes, manifest)
    else:
        # Fail-closed (mirrors tts.py T2a): mock silence must never clobber real Dean WAVs.
        existing, status = read_manifest_status(manifest_path)
        abort = _mock_synth_guard(status=status, existing=existing, audio_dir=audio_dir,
                                  force_clobber=args.force_clobber)
        if abort:
            raise SystemExit(f"[synth] {abort}")
        manifest = synth(meta, scenes, scene_numbers, audio_dir, args.backend,
                         empty_seconds=args.empty_beat_seconds)
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[synth] manifest -> {manifest_path}", flush=True)

    _warn_short_beats(meta, scenes, manifest)

    # render
    rendered, failures = render(meta, scenes, manifest, out_dir, args.quality)
    if failures:
        print(f"[render] {failures} scene(s) failed; aborting before compose", flush=True)
        return 1
    if not _audit_render_sync(scenes, manifest, rendered, lead=args.lead):
        print("[sync] render/audio mismatch; aborting before compose", flush=True)
        return 1

    # compose
    sec_dir.mkdir(parents=True, exist_ok=True)
    if args.output:
        output = args.output
        output.parent.mkdir(parents=True, exist_ok=True)
    elif args.scene == "all":
        output = sec_dir / f"{meta['id']}.mp4"
    else:
        output = sec_dir / f"{meta['id']}__{_safe_stem(args.scene)}.mp4"
        print(
            f"[compose] scene subset output -> {output} (full deck mp4 is untouched)",
            flush=True,
        )
    result = compose(scenes, manifest, rendered, out_dir,
                     lead=args.lead, abr=args.audio_bitrate, output=output,
                     transition=args.transition, intra_act=args.intra_act_transition,
                     meta=meta, quality=args.quality,
                     storyboard_path=args.storyboard, manifest_path=manifest_path)
    if result is None:
        return 1
    print(f"[done] {result}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

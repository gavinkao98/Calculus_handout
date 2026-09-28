"""loudnorm.py -- two-pass loudnorm of a finished film's audio to the house target.

Extracted verbatim from the Manim-era make.py (now legacy/manim_video/make.py) on
2026-09-28, when the video line moved to Remotion (video/KICKOFF-remotion-unification.md):
the house loudness contract and its ffmpeg filter are renderer-independent, and the
Remotion line's finishing step (video/remotion/scripts/loudnorm.py)
calls `_loudnorm_final` from here. No manim, no API -- ffmpeg only.
"""
from __future__ import annotations

import subprocess
from pathlib import Path


def _ffmpeg(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise RuntimeError("ffmpeg failed:\n" + " ".join(cmd) + "\n" + result.stderr[-1500:])


# House integrated-loudness target (T10, adjudicated 2026-07-11): the final film's audio
# is two-pass loudnorm'd to this LUFS (video stream-copied). TP ceiling + WARN tolerance.
HOUSE_LUFS = -19.0
LOUDNORM_TP = -1.5
LOUDNORM_TOL_I = 1.0   # WARN when the delivered integrated loudness misses target by > this


def _loudnorm_final(src: Path, out: Path, abr: str, target_i: float,
                    target_tp: float = LOUDNORM_TP) -> tuple[bool, dict]:
    """Two-pass loudnorm the AUDIO of `src` to target_i LUFS -> `out` (video stream-COPIED,
    preserving the single T8 video encode; linear gain keeps A/V sync). Returns
    (normalized, loudness), kept apart (C-03): normalized=False means pass 1 or pass 2
    failed, `out` is not a normalized film, and the caller falls back to the un-normalized
    concat; normalized=True means `out` IS the normalized film and loudness is its ebur128
    {I, TP} -- or {'error':...} when only that after-the-fact measurement failed, which
    must never throw the finished film away."""
    from pipeline.loudness_ab import _parse_loudnorm_json
    from pipeline.listening_pack import measure_loudness
    p1 = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(src), "-vn",
         "-af", f"loudnorm=I={target_i}:TP={target_tp}:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    meas = _parse_loudnorm_json(p1.stderr or "")
    if not all(k in meas for k in ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset")):
        return False, {"error": "loudnorm pass-1 measurement failed"}
    af = (f"loudnorm=I={target_i}:TP={target_tp}:linear=true:"
          f"measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
          f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:"
          f"offset={meas['target_offset']}")
    # this mux IS the delivered file on the real-audio path, so it carries T8's +faststart too
    try:
        _ffmpeg(["ffmpeg", "-y", "-i", str(src), "-map", "0:v:0", "-map", "0:a:0",
                 "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", abr,
                 "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(out)])
    except RuntimeError as exc:   # e.g. an all-silent film: pass 1 measures -inf, pass 2 rejects it
        return False, {"error": "loudnorm pass-2 failed: " + " | ".join(str(exc).strip().splitlines()[-4:])}
    return True, measure_loudness(out)

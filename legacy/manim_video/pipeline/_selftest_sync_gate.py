"""Offline self-test for make.py's render/audio sync HARD GATE (no render, no ffprobe).
Run: python video/pipeline/_selftest_sync_gate.py"""
import contextlib
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import make  # noqa: E402

from pipeline.timing import SYNC_HARD_GATE_FRAMES, expected_content_video_seconds  # noqa: E402

AUDIO = 8.0
LEAD = 1.0
EXPECTED = expected_content_video_seconds(AUDIO, lead_seconds=LEAD)


def _audit(actual: float, fps: float):
    """(ok, printed output) for one audited scene whose probe reports (actual, fps)."""
    scenes = [{"id": "s", "kind": "content"}]
    manifest = {"scenes": [{"scene_id": "s", "narration_mode": "beats", "audio_seconds": AUDIO}]}
    rendered = {"s": Path("s.mp4")}
    original = make._probe_duration_fps
    make._probe_duration_fps = lambda path: (actual, fps)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            ok = make._audit_render_sync(scenes, manifest, rendered, lead=LEAD)
    finally:
        make._probe_duration_fps = original
    return ok, buf.getvalue()


def test_gate_is_two_frames():
    # the 2026-09-13 ruling: 2 frames, not 1 (the worst real scene sits at 1.0 frame).
    assert SYNC_HARD_GATE_FRAMES == 2


def test_three_frames_late_is_fatal():
    ok, out = _audit(EXPECTED + 3 / 30, 30.0)
    assert ok is False, "3 frames over the gate must abort, not warn"
    assert "ERROR" in out, out
    assert "WARN" not in out, "the length mismatch is a gate now, not a warning"
    assert "frames" in out and "expected" in out, out


def test_one_frame_short_passes():
    ok, out = _audit(EXPECTED - 1 / 30, 30.0)
    assert ok is True, out
    assert "ERROR" not in out, out
    assert "hard gate" in out, "the gate in force must be printed"


def test_exactly_two_frames_is_inclusive():
    ok, out = _audit(EXPECTED + 2 / 30, 30.0)
    assert ok is True, "the gate is inclusive: exactly 2 frames passes"
    assert "ERROR" not in out, out


def test_video_shorter_than_narration_is_fatal():
    ok, out = _audit(LEAD + AUDIO - 0.5, 30.0)     # ends before the narration does
    assert ok is False
    assert "narration ends at" in out, out


def test_tolerance_scales_with_fps():
    # 0.05 s = 1.5 frames at 30 fps (passes) but 3 frames at 60 fps (fatal).
    assert _audit(EXPECTED + 3 / 60, 30.0)[0] is True
    assert _audit(EXPECTED + 3 / 60, 60.0)[0] is False


def test_unreadable_frame_rate_is_fatal():
    ok, out = _audit(EXPECTED, 0.0)
    assert ok is False, "no fps means no frame-measured gate -- refuse, never guess"
    assert "ERROR" in out and "frame rate" in out, out


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] make sync hard gate green")

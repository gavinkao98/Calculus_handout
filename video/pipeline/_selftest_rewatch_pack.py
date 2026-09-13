"""Self-test: rewatch_pack locates a still stretch, it does not just measure one.
Run from video/:
    python -m pipeline._selftest_rewatch_pack

What it pins. The pack used to report how LONG the longest still stretch was but only the
COARSE change-event times. The coarse threshold (>0.2 % of pixels) cannot see a formula being
written -- at 192x108 a glyph is about 2x3 px -- so a writing beat reads as still to it and its
events merge with the neighbouring beat's. A reader locating a dead zone from that list is
pointed at the wrong beat, which is exactly what happened on 2026-09-13: scene 09's fine dead
zone was the proof.1 beat, the coarse events put the long gap over the statement beat, and two
render cycles were spent animating the wrong one.

The tests drive the real `motion_stats` over synthesised clips (so the shipped arithmetic is
what runs, not a copy of it) and check that the reported span points at the LONGEST run rather
than the first one, and that `_beat_at` names the beat that span sits in.

Also pinned (2026-09-13, KICKOFF-process-reform §2.3/§3 G1+G4): the two verdicts the pack now
EXITS on rather than merely reporting. `still_gate` is the 12 s measured line -- warn-only is
how eight `[sync]` warnings survived from round 13 to round 20, so a gate that cannot stop
anything is not a gate. `baseline_verdict` refuses an A/B whose baseline was rendered at a
different fps or frame size, because comparing 480p15 against 1080p30 measures `--quality`
and not the change. Both are pure functions so the judging is tested without ffmpeg.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()

import subprocess
import tempfile
from pathlib import Path

import numpy as np

from pipeline import rewatch_pack as RP

W = H = 64


def _clip(still_pattern: "list[bool]", path: Path) -> float:
    """Encode a clip at MOTION_FPS whose frame i differs from i-1 exactly where
    still_pattern[i-1] is False. Returns its duration in seconds."""
    n = len(still_pattern) + 1
    frames = np.zeros((n, H, W), dtype=np.uint8)
    val = 0
    for i, still in enumerate(still_pattern, start=1):
        if not still:
            val = 255 - val            # flip the whole frame: unmistakably "moving"
        frames[i] = val
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray",
         "-s", f"{W}x{H}", "-r", str(RP.MOTION_FPS), "-i", "-",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", str(path)],
        input=frames.tobytes(), check=True, capture_output=True)
    return n / RP.MOTION_FPS


def test_the_span_points_at_the_longest_run_not_the_first():
    """A short still run, then movement, then a LONGER one: the span must name the long one."""
    with tempfile.TemporaryDirectory() as td:
        clip = Path(td) / "a.mp4"
        # 4 still, 2 moving, 12 still, 2 moving   (samples, at MOTION_FPS)
        dur = _clip([True] * 4 + [False] * 2 + [True] * 12 + [False] * 2, clip)
        m = RP.motion_stats(clip, dur, [])
    lo, hi = m["fine_longest_still_span"]
    assert m["fine_longest_still_seconds"] == round(12 / RP.MOTION_FPS, 1), m
    assert lo == round(6 / RP.MOTION_FPS, 1), (lo, hi)      # after the 4 still + 2 moving
    assert round(hi - lo, 1) == m["fine_longest_still_seconds"], (lo, hi)


def test_both_thresholds_report_a_span():
    with tempfile.TemporaryDirectory() as td:
        clip = Path(td) / "b.mp4"
        dur = _clip([True] * 8 + [False] * 2, clip)
        m = RP.motion_stats(clip, dur, [])
    for key in ("longest_still_span", "fine_longest_still_span"):
        span = m[key]
        assert isinstance(span, list) and len(span) == 2 and span[1] >= span[0], (key, span)
    assert isinstance(m["fine_events"], list)


def test_a_clip_too_short_to_difference_still_carries_the_new_keys():
    """The early return is a real code path (a one-frame scene); a caller formatting the md
    would KeyError on it if the keys were only added to the main return."""
    with tempfile.TemporaryDirectory() as td:
        clip = Path(td) / "c.mp4"
        _clip([], clip)
        m = RP.motion_stats(clip, 0.25, [])
    for key in ("longest_still_span", "fine_longest_still_span", "fine_events"):
        assert key in m, key


def test_beat_attribution_names_the_beat_the_span_sits_in():
    beats = [{"index": 0, "reveal": "statement", "start_seconds": 0.0, "end_seconds": 9.9},
             {"index": 1, "reveal": "proof.0", "start_seconds": 9.9, "end_seconds": 25.1},
             {"index": 2, "reveal": "proof.1", "start_seconds": 25.1, "end_seconds": 41.7}]
    lead = RP.SCENE_LEAD_SECONDS
    # scene 09's real numbers: the FINE span is the proof.1 beat ...
    assert RP._beat_at([lead + 26.5, lead + 41.8], beats) == " (beat 2, proof.1)"
    # ... while the COARSE span, which merges the writing beat with its neighbour, is not
    assert RP._beat_at([lead + 7.0, lead + 26.8], beats) == " (beat 1, proof.0)"


def test_beat_attribution_is_silent_without_beats_or_outside_them():
    assert RP._beat_at([1.0, 5.0], []) == ""
    one = [{"index": 0, "reveal": "x", "start_seconds": 0.0, "end_seconds": 2.0}]
    assert RP._beat_at([900.0, 901.0], one) == ""


# ---- the 12 s still gate (G1) ---------------------------------------------------------

def _row(scene: str, still: float, kind: str = "content", where: str = "") -> dict:
    return {"scene": scene, "kind": kind, "still_seconds": still, "where": where}


def test_still_gate_passes_when_every_content_scene_is_under_the_line():
    v = RP.still_gate([_row("a", 11.0), _row("b", 8.5)], 12.0)
    assert v["passed"] and v["over"] == [], v
    assert (v["content"], v["max_seconds"], v["max_scene"]) == (2, 11.0, "a"), v
    assert RP.still_gate_lines(v, 12.0) == [
        "[still-gate] PASS: all 2 content scenes <= 12.0 s (max 11.0 s @ a)"]


def test_still_gate_fails_and_names_the_beat_of_the_scene_over_the_line():
    v = RP.still_gate([_row("a", 11.0), _row("b", 13.4, where=" (beat 2, proof.1)")], 12.0)
    assert not v["passed"] and [r["scene"] for r in v["over"]] == ["b"], v
    assert RP.still_gate_lines(v, 12.0) == [
        "[still-gate] FAIL b: fine longest still 13.4 s > 12.0 s (beat 2, proof.1)",
        "[still-gate] 1/2 content scenes over 12.0 s"]


def test_still_gate_ignores_scenes_that_are_not_content():
    """An intro/divider holds a card on purpose; judging those makes the line unpassable."""
    v = RP.still_gate([_row("intro", 40.0, kind="intro"), _row("d", 44.0, kind="divider"),
                       _row("a", 9.0)], 12.0)
    assert v["passed"] and (v["content"], v["max_scene"]) == (1, "a"), v


def test_still_gate_counts_exactly_the_threshold_as_a_pass():
    assert RP.still_gate([_row("a", 12.0)], 12.0)["passed"]
    assert not RP.still_gate([_row("a", 12.1)], 12.0)["passed"]


def test_still_gate_is_honest_about_a_subset_with_no_content_scene():
    """`--scene intro,divider_limit` measures nothing the gate judges; do not claim it did."""
    v = RP.still_gate([_row("intro", 40.0, kind="intro")], 12.0)
    assert v["passed"] and v["content"] == 0, v
    assert RP.still_gate_lines(v, 12.0) == ["[still-gate] PASS: no content scenes measured"]


# ---- the A/B baseline refusal (G4) ----------------------------------------------------

def _src(fps: str = "30/1", size: str = "1920x1080") -> dict:
    return RP.source_record("deck", {i: {"fps": fps, "size": size} for i in ("a", "b")})


def test_baseline_at_the_same_fps_and_size_continues():
    ok, msg = RP.baseline_verdict(_src(), _src())
    assert ok and msg == "[ab] baseline fps/size match (fps=30/1 size=1920x1080)", msg


def test_baseline_at_a_different_fps_is_refused():
    ok, msg = RP.baseline_verdict(_src(), _src(fps="15/1"))
    assert not ok, msg
    assert msg == ("[ab] REFUSE: baseline fps=15/1 size=1920x1080 vs this render fps=30/1 "
                   "size=1920x1080 -- A/B across different --quality is invalid"), msg


def test_baseline_at_a_different_frame_size_is_refused():
    ok, msg = RP.baseline_verdict(_src(), _src(size="854x480"))
    assert not ok and "baseline fps=30/1 size=854x480 vs this render" in msg, msg


def test_a_baseline_pack_that_records_no_source_is_refused():
    """An old pack has no source record; silently comparing it is how a fake A/B happens."""
    for base in (None, {"deck": "d", "fps": None, "size": None, "scenes": {}}):
        ok, msg = RP.baseline_verdict(_src(), base)
        assert not ok and "baseline pack records no source fps/size" in msg, msg
        assert "rebuild the baseline pack" in msg, msg


def test_this_render_mixing_fps_across_its_own_scenes_is_refused():
    src = RP.source_record("deck", {"a": {"fps": "30/1", "size": "1920x1080"},
                                    "b": {"fps": "15/1", "size": "854x480"}})
    assert src["fps"] is None and src["size"] is None, src
    ok, msg = RP.baseline_verdict(src, _src())
    assert not ok and "this render's scenes disagree" in msg, msg
    assert "fps=15/1 size=854x480" in msg and "fps=30/1 size=1920x1080" in msg, msg


if __name__ == "__main__":
    test_the_span_points_at_the_longest_run_not_the_first()
    test_both_thresholds_report_a_span()
    test_a_clip_too_short_to_difference_still_carries_the_new_keys()
    test_beat_attribution_names_the_beat_the_span_sits_in()
    test_beat_attribution_is_silent_without_beats_or_outside_them()
    test_still_gate_passes_when_every_content_scene_is_under_the_line()
    test_still_gate_fails_and_names_the_beat_of_the_scene_over_the_line()
    test_still_gate_ignores_scenes_that_are_not_content()
    test_still_gate_counts_exactly_the_threshold_as_a_pass()
    test_still_gate_is_honest_about_a_subset_with_no_content_scene()
    test_baseline_at_the_same_fps_and_size_continues()
    test_baseline_at_a_different_fps_is_refused()
    test_baseline_at_a_different_frame_size_is_refused()
    test_a_baseline_pack_that_records_no_source_is_refused()
    test_this_render_mixing_fps_across_its_own_scenes_is_refused()
    print("OK rewatch_pack self-test")

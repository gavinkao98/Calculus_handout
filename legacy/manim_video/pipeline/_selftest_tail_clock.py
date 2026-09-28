"""Self-test: `LessonScene._tail` ends the clip SCENE_TAIL_SECONDS after the narration, even
when the exit fade and the end-of-scene sweep-up eat into the hold
(code-review-2026-09-23 F-03). Run from video/:
    python -m pipeline._selftest_tail_clock

Render-free: `_stage` / `_play_content` / `_tail` are driven UNBOUND against a FakeScene whose
renderer clock advances the way manim's does -- every play / wait becomes a whole number of
frames (np.arange(0, run_time, 1/fps)), a run_time under one frame is rendered as one frame,
and a run_time <= 0 raises -- and the finished length is compared with the [sync] hard gate
(lead + narration + tail, +/- SYNC_HARD_GATE_FRAMES).

Before the fix `_tail` played the exit fade first and then held for
max(end - now, MIN_HOLD), so whatever landed after the last beat -- the closing focus restore,
a corner carry's flight swept up at scene end -- was paid for once by the exit fade and again
by the 0.3 s floor: +3 frames for a corner carry with no marker, +6 for a last-beat dim plus
an `exit:`. Both are legal storyboards and both aborted make.py after the whole render.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # templates import manim at module level -- bootstrap FIRST

import numpy as np
from manim import Square, tempconfig

import pipeline.templates as templates
from pipeline.blocks import Block
from pipeline.scene import MIN_HOLD, LessonScene
from pipeline.timing import (EXIT_FADE_SECONDS, SCENE_LEAD_SECONDS, SCENE_TAIL_SECONDS,
                             SYNC_HARD_GATE_FRAMES, elapsed, expected_content_video_seconds)

FPS = 30


class _Clock:
    time = 0.0


class _FrameScene:
    """manim's clock, minus the pixels: see the module docstring."""

    def __init__(self, spec, durations=None, start=0.0):
        self.spec, self.beat_durations = spec, durations
        self.renderer = _Clock()
        self.renderer.time = start
        self.mobjects = []                    # run_floorprobe: nothing on screen to measure
        self.beat_seconds = None
        self.beat_reserved_seconds = 0.0
        self.calls = []

    def _advance(self, kind, run_time):
        if run_time <= 0:
            raise ValueError(f"{kind} run_time {run_time!r} <= 0 (manim refuses it)")
        self.calls.append((kind, run_time))
        run_time = max(run_time, 1 / FPS)
        for _ in np.arange(0, run_time, 1 / FPS):
            if self.renderer is not None:
                self.renderer.time += 1 / FPS

    def play(self, *anims, run_time=1.0, **kw):
        self._advance("play", run_time)

    def wait(self, duration=1.0, **kw):
        self._advance("wait", duration)

    def add(self, *mobs):
        pass

    def remove(self, *mobs):
        pass


def _run(spec, blocks, durations):
    """(video seconds, [sync] delta in frames) for one content scene."""
    with tempconfig({"frame_rate": FPS}):
        scene = _FrameScene(spec, durations)
        by_id = {b.id: b for b in blocks}
        LessonScene._stage(scene, blocks)
        scene.wait(SCENE_LEAD_SECONDS)
        end = LessonScene._play_content(scene, blocks, by_id, "dark")
        LessonScene._tail(scene, "content", by_id, end)
    video = scene.renderer.time
    return video, (video - expected_content_video_seconds(sum(durations))) * FPS


def _corner_carry_without_marker():
    """A `carry: to: {corner}` whose `as` has no `{show}`: schema only WARNS on it, and the
    flight runs in the end-of-scene sweep-up. The flight Block is the real one
    (templates._apply_carry); only the source scene's build is stubbed."""
    source = [Block("plot.0", Square(), anim="fade", static=True)]
    spec = {"id": "b", "kind": "content", "template": "callout",
            "say": "One sentence here. {show body} Another sentence.",
            "carry": [{"from": "a", "block": "plot.0", "as": "carried.curve",
                       "to": {"corner": "top_right", "scale": 0.4}}]}
    ctx = {"ground": "dark", "meta": {}, "scenes_by_id": {"a": {"id": "a"}, "b": spec}}
    real_build = templates.build_blocks
    templates.build_blocks = lambda _spec, _ctx: source
    try:
        blocks = templates._apply_carry(spec, ctx, [Block("body", Square(), anim="fade")])
    finally:
        templates.build_blocks = real_build
    return spec, blocks


def _last_beat_dim_plus_exit(with_exit=True):
    spec = {"id": "c", "kind": "content", "template": "derivation",
            "say": "{show step.0} First. {show step.1} Second.",
            "focus": [{"at": "step.1", "dim": ["step.0"]}]}
    if with_exit:
        spec["exit"] = ["step.0", "step.1"]
    return spec, [Block("step.0", Square(), anim="fade"), Block("step.1", Square(), anim="fade")]


def test_corner_carry_without_marker_stays_inside_the_sync_gate():
    spec, blocks = _corner_carry_without_marker()
    video, delta = _run(spec, blocks, [3.0, 4.0])
    assert abs(delta) <= SYNC_HARD_GATE_FRAMES, f"video={video:.3f}s delta={delta:+.1f} frames"


def test_last_beat_dim_plus_exit_stays_inside_the_sync_gate():
    spec, blocks = _last_beat_dim_plus_exit()
    video, delta = _run(spec, blocks, [3.0, 4.0])
    assert abs(delta) <= SYNC_HARD_GATE_FRAMES, f"video={video:.3f}s delta={delta:+.1f} frames"


def test_last_beat_dim_without_exit_is_still_on_time():
    spec, blocks = _last_beat_dim_plus_exit(with_exit=False)
    _video, delta = _run(spec, blocks, [3.0, 4.0])
    assert abs(delta) <= SYNC_HARD_GATE_FRAMES, delta


# -- zero behaviour change where the old hold was never clamped ------------------------------

def _old_tail_calls(start, narration_end, with_exit):
    """The pre-fix `_tail`, verbatim in its arithmetic: exit fade first, then
    wait(max(end - now, MIN_HOLD)) off the re-read clock."""
    scene = _FrameScene({}, start=start)
    if with_exit:
        scene.play(run_time=EXIT_FADE_SECONDS)
    scene.wait(max(narration_end + SCENE_TAIL_SECONDS - elapsed(scene), MIN_HOLD))
    return scene.calls


def test_a_tail_with_room_for_fade_and_floor_is_call_for_call_unchanged():
    """remaining = what is left of the hold when `_tail` starts. With remaining >= fade +
    MIN_HOLD (0.8 s with an exit, 0.3 s without) the old `max(..., MIN_HOLD)` never clamped,
    so the new code must issue the SAME plays and waits with the SAME run_times (bit for bit):
    that is every current deck scene whose last beat ends on its narration clock and has
    nothing, or only one short fade, left to sweep up (remaining ~ 0.97-1.0 s)."""
    block = Block("x", Square(), anim="fade")
    with tempconfig({"frame_rate": FPS}):
        for with_exit, floor in ((True, EXIT_FADE_SECONDS + MIN_HOLD), (False, MIN_HOLD)):
            for frames in range(0, 31):
                for sub in (0.0, 0.25, 0.5):           # on and between frame boundaries
                    remaining = floor + (frames + sub) / FPS
                    if remaining > SCENE_TAIL_SECONDS + 1e-9:
                        continue
                    start = 12.0 + (frames % 7) / FPS  # any clock reading
                    narration_end = start + remaining - SCENE_TAIL_SECONDS
                    new = _FrameScene({"exit": ["x"] if with_exit else []}, start=start)
                    LessonScene._tail(new, "content", {"x": block}, narration_end)
                    old = _old_tail_calls(start, narration_end, with_exit)
                    assert new.calls == old, (with_exit, remaining, new.calls, old)


def test_no_clock_path_is_unchanged():
    """Off a real render (the other selftests' FakeScene: no renderer) the tail keeps its
    nominal arithmetic: fade EXIT_FADE_SECONDS, then hold the rest of SCENE_TAIL_SECONDS."""
    class _NoClock(_FrameScene):
        def __init__(self, spec):
            super().__init__(spec)
            self.renderer = None
    block = Block("x", Square(), anim="fade")
    with tempconfig({"frame_rate": FPS}):
        scene = _NoClock({"exit": ["x"]})
        LessonScene._tail(scene, "content", {"x": block})
        assert scene.calls == [("play", EXIT_FADE_SECONDS),
                               ("wait", SCENE_TAIL_SECONDS - EXIT_FADE_SECONDS)], scene.calls
        scene = _NoClock({})
        LessonScene._tail(scene, "content", {})
        assert scene.calls == [("wait", SCENE_TAIL_SECONDS)], scene.calls


def test_a_tail_already_spent_still_fades_the_exit_and_never_waits_zero():
    """remaining <= 0 (a sweep-up longer than the whole hold): the exit still leaves before
    the cut -- in one frame, manim's shortest play -- and no zero/negative wait is issued
    (manim raises on one)."""
    block = Block("x", Square(), anim="fade")
    with tempconfig({"frame_rate": FPS}):
        scene = _FrameScene({"exit": ["x"]}, start=5.0)
        LessonScene._tail(scene, "content", {"x": block}, 5.0 - SCENE_TAIL_SECONDS - 0.2)
        assert scene.calls == [("play", 1 / FPS)], scene.calls


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] tail_clock green")

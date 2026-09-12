"""Stdlib assert self-test for motion primitives 4 (focus) and 6 (beat-paced animation).

Run: .venv/Scripts/python.exe video/pipeline/_selftest_focus_and_pacing.py

Render-free: `focus.apply` and `timing.beat_run_time` are exercised against a fake scene
that records what it was asked to play, so no manim render happens. The schema/sizecheck
validators are pure dict logic.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import focus as F        # noqa: E402
from pipeline import timing as TM      # noqa: E402
from pipeline import schema as S       # noqa: E402


class FakeMob:
    def __init__(self):
        self.opacity = 1.0
        self.animate = self

    def set_opacity(self, v):
        self.opacity = v
        return ("set_opacity", self, v)


class FakeBlock:
    def __init__(self):
        self.mobject = FakeMob()


class FakeScene:
    """Records plays instead of rendering. `beat_seconds` is what the real LessonScene
    sets before each beat."""
    def __init__(self, beat_seconds=None):
        self.beat_seconds = beat_seconds
        self.plays = []

    def play(self, *anims, **kw):
        self.plays.append((len(anims), kw.get("run_time")))


def _by_id(*names):
    return {n: FakeBlock() for n in names}


# -- primitive 6: beat-paced run_time --------------------------------------------

def test_no_beat_context_falls_back():
    assert TM.beat_run_time(FakeScene(), 3.0) == 3.0
    assert TM.beat_run_time(object(), 2.5) == 2.5          # not even the attribute


def test_long_beat_fills_the_beat_minus_a_tail():
    got = TM.beat_run_time(FakeScene(20.2), 3.0)
    assert abs(got - (20.2 - TM.BEAT_PACED_TAIL_SECONDS)) < 1e-9, got
    assert got > 3.0, "a paced animation on a long beat must outlast its fallback"


def test_short_beat_is_not_compressed_below_the_floor():
    assert TM.beat_run_time(FakeScene(0.9), 3.0) == TM.BEAT_PACED_MIN_SECONDS
    assert TM.beat_run_time(FakeScene(0.0), 3.0) == TM.BEAT_PACED_MIN_SECONDS


def test_pacing_is_opt_in_only():
    """A stock animation must not change length just because a beat is long: the primitive
    is `seconds: beat` on one plot, not a global re-timing."""
    assert TM.STOCK_ANIM_SECONDS["write"] == 0.7
    assert TM.STOCK_ANIM_SECONDS["transform"] == 1.2


# -- primitive 4: focus ----------------------------------------------------------

def test_scene_focus_reads_entries_and_empty_dim_means_restore():
    spec = {"focus": [{"at": "result", "dim": ["step.0", "step.1"]},
                      {"at": "check", "dim": []}]}
    assert F.scene_focus(spec) == {"result": ["step.0", "step.1"], "check": []}
    assert F.scene_focus({}) == {}
    assert F.scene_focus({"focus": None}) == {}


def test_apply_dims_only_the_named_blocks():
    by_id = _by_id("a", "b", "c")
    scene = FakeScene(10.0)
    dimmed = F.apply(scene, by_id, ["a", "b"], set())
    assert dimmed == {"a", "b"}
    assert by_id["a"].mobject.opacity == F.DIM_OPACITY
    assert by_id["b"].mobject.opacity == F.DIM_OPACITY
    assert by_id["c"].mobject.opacity == 1.0
    # one play for the whole shift, not one per element
    assert len(scene.plays) == 1 and scene.plays[0][0] == 2
    assert scene.plays[0][1] == F.FADE_SECONDS


def test_apply_restores_what_is_no_longer_wanted():
    by_id = _by_id("a", "b")
    scene = FakeScene(10.0)
    dimmed = F.apply(scene, by_id, ["a"], set())
    dimmed = F.apply(scene, by_id, ["b"], dimmed)
    assert dimmed == {"b"}
    assert by_id["a"].mobject.opacity == 1.0, "a should have been restored"
    assert by_id["b"].mobject.opacity == F.DIM_OPACITY


def test_empty_dim_restores_everything():
    by_id = _by_id("a", "b")
    scene = FakeScene(10.0)
    dimmed = F.apply(scene, by_id, ["a", "b"], set())
    dimmed = F.apply(scene, by_id, [], dimmed)
    assert dimmed == set()
    assert all(b.mobject.opacity == 1.0 for b in by_id.values())


def test_apply_is_a_no_op_when_nothing_changes():
    """A repeated focus must not burn FADE_SECONDS of the beat doing nothing."""
    by_id = _by_id("a")
    scene = FakeScene(10.0)
    dimmed = F.apply(scene, by_id, ["a"], set())
    plays_after_first = len(scene.plays)
    dimmed = F.apply(scene, by_id, ["a"], dimmed)
    assert len(scene.plays) == plays_after_first, "no change must play nothing"


def test_unknown_block_id_is_ignored_at_play_time():
    """sizecheck errors on it before render; the player must not crash if one slips."""
    by_id = _by_id("a")
    scene = FakeScene(10.0)
    dimmed = F.apply(scene, by_id, ["a", "nope"], set())
    assert dimmed == {"a"}


# -- schema validation -----------------------------------------------------------

def _focus_errs(scene, say):
    return [m for sev, m in S._focus_issues("s1", scene, say) if sev == "error"]


def test_schema_accepts_a_well_formed_focus():
    say = "One {show result} two {show check} three"
    scene = {"focus": [{"at": "result", "dim": ["step.0"]}, {"at": "check", "dim": []}]}
    assert _focus_errs(scene, say) == []


def test_schema_rejects_an_at_that_is_never_revealed():
    say = "One {show result} two"
    errs = _focus_errs({"focus": [{"at": "nope", "dim": []}]}, say)
    assert len(errs) == 1 and "never does" in errs[0], errs


def test_schema_rejects_a_duplicate_at():
    say = "One {show result} two"
    errs = _focus_errs({"focus": [{"at": "result", "dim": []},
                                  {"at": "result", "dim": ["x"]}]}, say)
    assert any("already focused" in e for e in errs), errs


def test_schema_rejects_a_missing_or_non_list_dim():
    say = "One {show result} two"
    assert any("required list" in e for e in _focus_errs({"focus": [{"at": "result"}]}, say))
    errs = _focus_errs({"focus": [{"at": "result", "dim": "step.0"}]}, say)
    assert any("required list" in e for e in errs), errs


def test_schema_is_silent_without_the_field():
    assert S._focus_issues("s1", {}, "One {show result} two") == []


if __name__ == "__main__":
    test_no_beat_context_falls_back()
    test_long_beat_fills_the_beat_minus_a_tail()
    test_short_beat_is_not_compressed_below_the_floor()
    test_pacing_is_opt_in_only()
    test_scene_focus_reads_entries_and_empty_dim_means_restore()
    test_apply_dims_only_the_named_blocks()
    test_apply_restores_what_is_no_longer_wanted()
    test_empty_dim_restores_everything()
    test_apply_is_a_no_op_when_nothing_changes()
    test_unknown_block_id_is_ignored_at_play_time()
    test_schema_accepts_a_well_formed_focus()
    test_schema_rejects_an_at_that_is_never_revealed()
    test_schema_rejects_a_duplicate_at()
    test_schema_rejects_a_missing_or_non_list_dim()
    test_schema_is_silent_without_the_field()
    print("OK focus_and_pacing self-test")

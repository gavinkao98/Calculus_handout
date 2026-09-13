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
from pipeline.blocks import Block      # noqa: E402


class FakeMob:
    """Mirrors the manim contract focus.apply relies on: fade / save_state / restore.
    `hollow` stands in for any deliberately-transparent part (the (1)(2)(3) badge rings).
    `set_opacity` is kept because it is the trap: it writes a flat value over the whole
    family and so clobbers `hollow`, which is why neither direction of a focus may use it."""
    def __init__(self, hollow=0.0):
        self.opacity = 1.0
        self.hollow = hollow
        self._saved = None
        self.animate = self

    def set_opacity(self, v):
        self.opacity = v
        self.hollow = v            # manim sets fill AND stroke on the whole family
        return ("set_opacity", self, v)

    def fade(self, darkness):
        # manim's VMobject.fade: scales each family member's OWN opacities, so a part
        # that is transparent on purpose stays transparent.
        factor = 1.0 - darkness
        self.opacity *= factor
        self.hollow *= factor
        return ("fade", self, darkness)

    def save_state(self):
        self._saved = (self.opacity, self.hollow)

    def restore(self):
        assert self._saved is not None, "restore() before save_state()"
        self.opacity, self.hollow = self._saved
        return ("restore", self)


class FakeBlock:
    def __init__(self, hollow=0.0):
        self.mobject = FakeMob(hollow=hollow)


class FakeScene:
    """Records plays instead of rendering. `beat_seconds` is what the real LessonScene
    sets before each beat."""
    def __init__(self, beat_seconds=None):
        self.beat_seconds = beat_seconds
        self.plays = []
        self.anims = []        # the animation objects themselves (indicate tests look inside)

    def play(self, *anims, **kw):
        self.plays.append((len(anims), kw.get("run_time")))
        self.anims.append(anims)

    def wait(self, seconds):
        pass

    def add(self, *mobs):
        pass


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


# -- beat_reserved_seconds: a beat-filling reveal leaves room for its own indicate --

def test_beat_run_time_subtracts_beat_reserved_seconds():
    """`scene.beat_reserved_seconds` (set by `_play_content` before a beat's reveal, when
    that beat's `focus[].indicate` will play after it) must come straight off the budget a
    paced reveal asks for, on top of the existing BEAT_PACED_TAIL_SECONDS reservation --
    the generalisation of what ch03 06's `ineq` hook used to subtract by hand."""
    without_reserve = TM.beat_run_time(FakeScene(10.0), 3.0)
    reserved_scene = FakeScene(10.0)
    reserved_scene.beat_reserved_seconds = 0.8
    with_reserve = TM.beat_run_time(reserved_scene, 3.0)
    assert abs(without_reserve - with_reserve - 0.8) < 1e-9, (without_reserve, with_reserve)


def test_paced_reveal_stays_inside_the_beat_reserved_for_its_indicate():
    """A paced (beat-filling) reveal's actual spend must not exceed
    `beat − BEAT_PACED_TAIL_SECONDS − beat_reserved_seconds`, so a `focus[].indicate` that
    follows it in the same beat lands inside the beat instead of past it (ch03 06's `ineq`
    beat is the instance already in the deck, but the trap is generic to any beat pairing
    a paced reveal with an indicate)."""
    from manim import Dot, VGroup

    from pipeline import pacing as P

    mob = VGroup(*[Dot() for _ in range(3)])
    scene = FakeScene(10.0)
    scene.beat_reserved_seconds = F.INDICATE_SECONDS
    spent = P.paced_reveal(scene, mob, "dark")
    budget = 10.0 - TM.BEAT_PACED_TAIL_SECONDS - F.INDICATE_SECONDS
    assert spent <= budget + 1e-9, (spent, budget)


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


def test_a_hollow_part_stays_hollow_through_a_dim_and_a_restore():
    """Both directions, one defect. Restoring with set_opacity(1.0) fills in anything
    deliberately hollow -- the region badges are rings with fill_opacity=0 -- so two of the
    three (1)(2)(3) badges came back as solid discs with their digits buried; that was fixed
    with save_state/restore on the first render of this primitive. The DIM had the same hole
    and kept it: set_opacity(DIM_OPACITY) writes 0.35 into a ring's fill and makes it a disc,
    which is what scene 06's (1) and (2) were doing at the `tri_outer` beat (2026-09-13).
    A dim is multiplicative -- `fade` -- so it can never paint an invisible part visible."""
    by_id = {"ring": FakeBlock(hollow=0.0)}
    scene = FakeScene(10.0)
    dimmed = F.apply(scene, by_id, ["ring"], set())
    assert by_id["ring"].mobject.opacity == F.DIM_OPACITY, "the visible part dims"
    assert by_id["ring"].mobject.hollow == 0.0, "a hollow part must STAY hollow while dimmed"
    F.apply(scene, by_id, [], dimmed)
    assert by_id["ring"].mobject.opacity == 1.0
    assert by_id["ring"].mobject.hollow == 0.0, "a hollow part must come back hollow"


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


def test_apply_never_redims_a_block_that_is_already_dimmed():
    """Regression for the ch03 06 `sector_inequality` restore-restore-fails-to-fully-
    restore report (2026-09-13, `+41s`/`+55s` sampled darker than a single dim):
    `apply({a})` then `apply({a, b})` then `apply({})` must leave BOTH `a` and `b` at
    full opacity, and `a` must never be faded a SECOND time just because the wanted
    set grew to include it again alongside `b` -- `fade` is multiplicative, so a
    repeat application would compound (0.35 -> 0.1225), not hold steady."""
    by_id = _by_id("a", "b")
    scene = FakeScene(10.0)
    dimmed = F.apply(scene, by_id, ["a"], set())
    assert by_id["a"].mobject.opacity == F.DIM_OPACITY
    dimmed = F.apply(scene, by_id, ["a", "b"], dimmed)
    assert by_id["a"].mobject.opacity == F.DIM_OPACITY, "a must not be dimmed a second time"
    assert by_id["b"].mobject.opacity == F.DIM_OPACITY
    dimmed = F.apply(scene, by_id, [], dimmed)
    assert dimmed == set()
    assert by_id["a"].mobject.opacity == 1.0, "a must land on full opacity, not a doubled dim"
    assert by_id["b"].mobject.opacity == 1.0


def test_apply_only_saves_state_for_a_block_not_already_dimmed():
    """`save_state()` must run exactly once per dim, before the fade that follows it --
    if a block already in the dimmed set were saved again, it would be saved AT its
    current (dimmed) opacity, and `restore()` would land back on that dimmed value
    instead of the original full one."""
    by_id = _by_id("a", "b")
    scene = FakeScene(10.0)
    save_calls = {"a": 0, "b": 0}
    for name in ("a", "b"):
        mob = by_id[name].mobject

        def _wrapped(orig=mob.save_state, n=name):
            save_calls[n] += 1
            orig()
        mob.save_state = _wrapped

    dimmed = F.apply(scene, by_id, ["a"], set())
    dimmed = F.apply(scene, by_id, ["a", "b"], dimmed)
    assert save_calls == {"a": 1, "b": 1}, "each block saves its un-dimmed state exactly once"
    F.apply(scene, by_id, [], dimmed)
    assert by_id["a"].mobject.opacity == 1.0
    assert by_id["b"].mobject.opacity == 1.0


# -- focus[].indicate: the flash variant (SPEC-motion-language rule 3) -----------

def test_scene_indicate_reads_only_entries_that_flash():
    spec = {"focus": [{"at": "ineq", "dim": [], "indicate": ["sector", "tri_outer"]},
                      {"at": "sector", "dim": ["tri_inner"]}]}
    assert F.scene_indicate(spec) == {"ineq": ["sector", "tri_outer"]}
    assert F.scene_indicate({}) == {}
    assert F.scene_indicate({"focus": None}) == {}
    # `indicate` never leaks into the dim plan
    assert F.scene_focus(spec) == {"ineq": [], "sector": ["tri_inner"]}


def _square_blocks(*names):
    from manim import Square

    class B:
        def __init__(self):
            self.mobject = Square()
    return {n: B() for n in names}


def test_indicate_plays_one_flash_for_the_whole_list_and_charges_for_it():
    from manim import Indicate
    by_id = _square_blocks("a", "b", "c")
    scene = FakeScene(10.0)
    secs = F.indicate(scene, by_id, ["a", "b"], "#e8ab63")
    assert secs == F.INDICATE_SECONDS
    assert len(scene.plays) == 1 and scene.plays[0] == (2, F.INDICATE_SECONDS)
    anims = scene.anims[0]
    assert all(isinstance(a, Indicate) for a in anims)
    assert [a.mobject for a in anims] == [by_id["a"].mobject, by_id["b"].mobject]
    assert all(a.scale_factor == F.INDICATE_SCALE for a in anims)
    assert all(str(a.color).lower() == "#e8ab63" for a in anims)


def test_indicate_is_free_when_nothing_matches():
    """Mirror of the dim rule: sizecheck errors on a typo'd id before render; at play time
    an unknown id is skipped and must not burn INDICATE_SECONDS of the beat."""
    scene = FakeScene(10.0)
    assert F.indicate(scene, _square_blocks("a"), ["nope"], "#ffffff") == 0.0
    assert F.indicate(scene, _square_blocks("a"), [], "#ffffff") == 0.0
    assert scene.plays == []


# -- scene.py's focus call site: EVERY `dim` entry runs BEFORE the beat's reveal -

class FakeLessonScene(FakeScene):
    """A FakeScene that `LessonScene._play_content` can be driven against unbound."""
    def wait(self, seconds):
        pass


def _run_play_content(spec, by_id, log):
    """Drive `_play_content` over *spec* with `focus.apply` logging what it was asked
    to do, so the ORDER of dim / restore / reveal is observable."""
    import pipeline.scene as scene_mod

    real_apply = F.apply

    def logging_apply(scene, by_id_, wanted, currently_dimmed):
        log.append("restore" if not wanted else "dim:" + ",".join(sorted(wanted)))
        return real_apply(scene, by_id_, wanted, currently_dimmed)

    fake_scene = FakeLessonScene(10.0)
    fake_scene.spec = spec
    fake_scene.beat_durations = None

    scene_mod.focus.apply = logging_apply
    try:
        scene_mod.LessonScene._play_content(fake_scene, [], by_id, "dark")
    finally:
        scene_mod.focus.apply = real_apply
    return fake_scene


def _reveal_logger(log, name):
    def reveal(scene, mob, ground):
        log.append("reveal-" + name)
        return 0.0
    return reveal


def test_every_focus_entry_runs_before_the_beats_own_reveal():
    """Root cause of the ch03 06 `sector_inequality` report, then of the ch03 24
    `mirror` one: scene.py used to reveal-then-focus (the just-revealed block earns
    full attention before anything dims).

    A `dim: []` entry dims nothing, so there was nothing left to protect by waiting --
    and its whole point is putting everything back for the viewer to compare across
    THIS beat. `ineq`'s reveal walks three terms across a beat that grew to ~22-27 s
    (motion primitive 7), so the old order left the restore stranded in the final
    FADE_SECONDS: a mock render showed the dimmed copies still dimmed at every sampled
    point inside the beat and only snapping back right before the next one started.

    A NON-EMPTY `dim` has exactly the same defect and it is worse, because what is
    dimmed is never the block being revealed -- it is the OTHER half of the screen,
    which the narration is steering attention away from in its FIRST sentence. Scene
    24's `mirror` beat (`dim: [g_v]`, an 11.5 s beat whose hook reveal fills ~5 s)
    rendered with the velocity row still lit until mid-beat, while "hold the bottom
    graph against the top" is the beat's opening line. So `_play_content` now applies
    the WHOLE focus entry before `play_block`; only `indicate` still fires after the
    reveal (it flashes blocks, it does not steer away from one)."""
    log = []
    by_id = {"a": FakeBlock(),
             "setup": Block(id="setup", mobject=FakeMob(), anim=_reveal_logger(log, "setup")),
             "ineq": Block(id="ineq", mobject=FakeMob(), anim=_reveal_logger(log, "ineq"))}
    _run_play_content(
        {"say": "{show setup} one two three {show ineq} four five six",
         "focus": [{"at": "setup", "dim": ["a"]}, {"at": "ineq", "dim": []}]},
        by_id, log)

    # A trailing "restore" is scene.py's own end-of-scene sweep-up (`focus.apply(..., [],
    # dimmed)`, always a no-op here since `dim: []` already restored everything); only the
    # first four events are this fix's concern.
    assert log[:4] == ["dim:a", "reveal-setup", "restore", "reveal-ineq"], log
    assert by_id["a"].mobject.opacity == 1.0, "the restore must actually run, not just move"


def test_a_dim_that_names_its_own_beats_reveal_is_skipped_and_warned():
    """Second line of defence behind the schema error. Now that a `dim` runs BEFORE the
    reveal, dimming the block the SAME beat reveals would have `focus.apply` call
    `save_state()` on a mobject that is not on screen yet -- and a later `dim: []` would
    then `restore()` it back to invisible, silently. No storyboard does this today; the
    order change is what would make it a trap, so the player skips the id and says so."""
    import contextlib
    import io

    log = []
    by_id = {"a": FakeBlock(),
             "row": Block(id="row", mobject=FakeMob(), anim=_reveal_logger(log, "row"))}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _run_play_content({"id": "s24", "say": "{show row} one two three",
                           "focus": [{"at": "row", "dim": ["a", "row"]}]}, by_id, log)

    assert log[:2] == ["dim:a", "reveal-row"], log
    # `_play_content` restores everything on its way out, so the tell is the SNAPSHOT:
    # `a` was dimmed (state saved), `row` was never touched (nothing to restore from).
    assert by_id["a"].mobject._saved is not None, "`a` should have been dimmed"
    assert by_id["row"].mobject._saved is None, "the beat's own reveal must not be dimmed"
    assert by_id["row"].mobject.opacity == 1.0
    out = buf.getvalue()
    assert "row" in out and "s24" in out, out


def test_play_content_sets_beat_reserved_seconds_only_for_the_beat_with_indicate():
    """`scene.beat_reserved_seconds` must equal `focus.INDICATE_SECONDS` while the beat
    that carries a `focus[].indicate` plays its OWN reveal -- set before that reveal, so a
    beat-filling reveal already asks `timing.beat_run_time` for a shorter budget -- 0 in a
    beat with no indicate, and 0 again once the scene has finished walking its beats."""
    from manim import Square       # `plain` is flashed below -- real Indicate() typechecks it

    reserved_at_reveal = {}

    def _reveal(name):
        def reveal(scene, mob, ground):
            reserved_at_reveal[name] = scene.beat_reserved_seconds
            return 0.0
        return reveal

    by_id = {"plain": Block(id="plain", mobject=Square(), anim=_reveal("plain")),
             "ineq": Block(id="ineq", mobject=FakeMob(), anim=_reveal("ineq"))}
    log = []
    scene = _run_play_content(
        {"say": "{show plain} one two {show ineq} three four",
         "focus": [{"at": "ineq", "dim": [], "indicate": ["plain"]}]},
        by_id, log)

    assert reserved_at_reveal["plain"] == 0.0, "no indicate on this beat"
    assert reserved_at_reveal["ineq"] == F.INDICATE_SECONDS, "this beat's own indicate"
    assert scene.beat_reserved_seconds == 0.0, "reset once the scene has finished its beats"


def test_play_content_reserves_fade_seconds_for_a_dim_that_actually_changes():
    """The dim-budget generalisation of the test above: `scene.beat_reserved_seconds` must
    also cover the `focus.apply` FADE_SECONDS play that runs BEFORE this beat's own reveal
    whenever the dim set is about to change (ch03 06's `evenness` beat -- a full-beat hook
    reveal plus a declared `dim` -- is the motivating case). `apply`'s own by_id-filtered
    change test decides "change": a `dim: []` beat that already has nothing dimmed must
    reserve 0, not FADE_SECONDS, and a beat pairing a real dim change with an `indicate`
    must reserve both."""
    from manim import Square

    reserved_at_reveal = {}

    def _reveal(name):
        def reveal(scene, mob, ground):
            reserved_at_reveal[name] = scene.beat_reserved_seconds
            return 0.0
        return reveal

    by_id = {"a": FakeBlock(),
             "dim_only": Block(id="dim_only", mobject=Square(), anim=_reveal("dim_only")),
             "both": Block(id="both", mobject=Square(), anim=_reveal("both")),
             "no_change": Block(id="no_change", mobject=Square(), anim=_reveal("no_change"))}
    log = []
    scene = _run_play_content(
        {"say": ("{show dim_only} one two {show both} three four "
                 "{show no_change} five six"),
         "focus": [{"at": "dim_only", "dim": ["a"]},                    # {} -> {a}: change
                   {"at": "both", "dim": [], "indicate": ["dim_only"]},  # {a} -> {}: change
                   {"at": "no_change", "dim": []}]},                    # {} -> {}: no change
        by_id, log)

    assert reserved_at_reveal["dim_only"] == F.FADE_SECONDS, "dim alone: 0.4 s"
    assert (reserved_at_reveal["both"]
            == F.FADE_SECONDS + F.INDICATE_SECONDS), "dim change + indicate: 1.2 s"
    assert reserved_at_reveal["no_change"] == 0.0, "dim: [] with nothing dimmed: no change"
    assert scene.beat_reserved_seconds == 0.0, "reset once the scene has finished its beats"


# -- schema validation -----------------------------------------------------------

def _focus_errs(scene, say):
    return [m for sev, m in S._focus_issues("s1", scene, say) if sev == "error"]


def test_schema_accepts_indicate_next_to_dim():
    say = "One {show result} two"
    scene = {"focus": [{"at": "result", "dim": ["step.0"], "indicate": ["result"]}]}
    assert _focus_errs(scene, say) == []


def test_schema_rejects_a_malformed_indicate():
    say = "One {show result} two"
    errs = _focus_errs({"focus": [{"at": "result", "dim": [], "indicate": "result"}]}, say)
    assert any("indicate" in e and "list" in e for e in errs), errs
    errs = _focus_errs({"focus": [{"at": "result", "dim": [], "indicate": ["", "x"]}]}, say)
    assert any("indicate" in e for e in errs), errs


def test_schema_rejects_indicating_a_block_the_same_entry_dims():
    """Flashing and dimming the same block in one beat is two animations fighting over one
    mobject; the later one wins silently. Always an authoring mistake."""
    say = "One {show result} two"
    errs = _focus_errs({"focus": [{"at": "result", "dim": ["step.0", "step.1"],
                                   "indicate": ["step.1"]}]}, say)
    assert len(errs) == 1 and "step.1" in errs[0] and "dim" in errs[0], errs


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


def test_schema_rejects_a_dim_that_names_its_own_entrys_at():
    """Always a typo, and since the dim now runs BEFORE the beat's reveal it is a trap:
    `focus.apply` would snapshot the block before it is on screen and a later `dim: []`
    would restore it to invisible. scene.py skips + warns at play time; this is the gate."""
    say = "One {show result} two {show check} three"
    errs = _focus_errs({"focus": [{"at": "result", "dim": ["step.0", "result"]}]}, say)
    assert len(errs) == 1 and "result" in errs[0], errs
    # a dim naming ANOTHER beat's reveal target is fine -- that is the normal case
    assert _focus_errs({"focus": [{"at": "check", "dim": ["result"]}]}, say) == []


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
    test_beat_run_time_subtracts_beat_reserved_seconds()
    test_paced_reveal_stays_inside_the_beat_reserved_for_its_indicate()
    test_scene_focus_reads_entries_and_empty_dim_means_restore()
    test_apply_dims_only_the_named_blocks()
    test_apply_restores_what_is_no_longer_wanted()
    test_a_hollow_part_stays_hollow_through_a_dim_and_a_restore()
    test_empty_dim_restores_everything()
    test_apply_is_a_no_op_when_nothing_changes()
    test_unknown_block_id_is_ignored_at_play_time()
    test_apply_never_redims_a_block_that_is_already_dimmed()
    test_apply_only_saves_state_for_a_block_not_already_dimmed()
    test_scene_indicate_reads_only_entries_that_flash()
    test_indicate_plays_one_flash_for_the_whole_list_and_charges_for_it()
    test_indicate_is_free_when_nothing_matches()
    test_every_focus_entry_runs_before_the_beats_own_reveal()
    test_a_dim_that_names_its_own_beats_reveal_is_skipped_and_warned()
    test_play_content_sets_beat_reserved_seconds_only_for_the_beat_with_indicate()
    test_play_content_reserves_fade_seconds_for_a_dim_that_actually_changes()
    test_schema_accepts_indicate_next_to_dim()
    test_schema_rejects_a_malformed_indicate()
    test_schema_rejects_indicating_a_block_the_same_entry_dims()
    test_schema_accepts_a_well_formed_focus()
    test_schema_rejects_an_at_that_is_never_revealed()
    test_schema_rejects_a_duplicate_at()
    test_schema_rejects_a_dim_that_names_its_own_entrys_at()
    test_schema_rejects_a_missing_or_non_list_dim()
    test_schema_is_silent_without_the_field()
    print("OK focus_and_pacing self-test")

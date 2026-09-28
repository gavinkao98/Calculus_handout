"""Self-test: scene 04's beat 3 is a paced SIDE BRANCH, not a 40 s hold. Run from video/:
    python -m pipeline._selftest_side_branch

§3.1's `difference_quotient_for_sine`, beat 3 (`{show step.0}`, 39.7 s / 109 words) is where
the narration derives the sum-to-product identity itself -- "put u = (A+B)/2 and v = (A-B)/2
... expand sin(u+v) - sin(u-v) with the angle-sum formulas, and the sin u cos v terms cancel,
leaving exactly 2 cos u sin v". The milestone six-lens review filed the same `must` from four
lenses (R3 / R4 independently): the beat carried ONE reveal, and the identity's own derivation
-- a side branch off the main line, which is the difference quotient -- ran with nothing on
screen to show it happening and no mark telling a beginner the block can be set aside.

This pins the two halves of the approved fix against the REAL canonical deck, by driving the
beat's reveal with a FakeScene (the `_selftest_reveal_timing` pattern) and reading its timeline:

  (1) the beat is cut into >= 4 reveal stages -- the identity, the u/v substitution, the
      angle-sum expansion, the cancel -- instead of one;
  (2) no stretch longer than SIDE_BRANCH_MAX_GAP_SECONDS passes with nothing new on screen;
  (3) the branch is MARKED: the draft column carries its own muted tag, so the block reads as
      scratch work beside the chain rather than a fourth row of it;
  (4) the branch LEAVES AS ONE, shrinking as it fades (SPEC-motion-language 規則 1: a temporary
      annotation退場 SHOULD 用縮小加淡出), so the main line is what is left standing.

Manim-backed (it builds the real scene's Tex), so it takes a few seconds, not milliseconds.
"""
from __future__ import annotations

import pathlib

import yaml

from pipeline import _bootstrap

_bootstrap.bootstrap()   # templates import manim at module level -- bootstrap FIRST (repo rule)

from pipeline import timing as TM
from pipeline.templates import build_blocks

DECK = pathlib.Path(__file__).resolve().parents[1] / "storyboards" / "ch03_trig_derivatives.yml"
SCENE_ID = "difference_quotient_for_sine"
REVEAL = "step.0"

# The beat's measured length in the film (rewatch_pack_after17 / the forced alignment the hook's
# own `_CUE` fractions were read off). The hook's cut points are fractions of the beat, so this
# is what turns them back into seconds.
BEAT_SECONDS = 39.7
# The acceptance line the two `must`s were written against: "this beat must not have a stretch
# longer than 10 s with nothing new on screen". (The deck-wide measured line is 12 s, §8; the
# authoring advisory is 6 s, `stillness.UNDECLARED_STILL_SECONDS`.)
SIDE_BRANCH_MAX_GAP_SECONDS = 10.0
MIN_REVEAL_STAGES = 4

# Animations that put something NEW on screen. A fade-out, a dim (`.animate.set_color`) or a
# framing rectangle's removal changes the picture but adds nothing to read, so they do not
# close a gap.
_NEW_ON_SCREEN = {"Write", "FadeIn", "Create", "Transform", "ReplacementTransform",
                  "TransformMatchingShapes", "TransformMatchingTex"}


class FakeScene:
    """Records the beat's timeline. `renderer = None` is what makes the hook report its
    nominal budget instead of a renderer clock (see the hooks module's `_spent`)."""

    renderer = None
    beat_reserved_seconds = 0.0

    def __init__(self, beat_seconds: float):
        self.beat_seconds = beat_seconds
        self.t = 0.0
        self.events: list[tuple[float, float, tuple]] = []

    def add(self, *mobjects):
        pass

    def remove(self, *mobjects):
        pass

    def wait(self, seconds: float = 1.0):
        self.t += float(seconds)

    def play(self, *anims, **kwargs):
        run_time = float(kwargs.get("run_time", 1.0))
        self.events.append((self.t, run_time, anims))
        self.t += run_time


def _tex_strings(mob, out=None) -> list[str]:
    """Every `tex_string` in a mobject tree -- how a test says WHICH line it is looking at."""
    out = [] if out is None else out
    s = getattr(mob, "tex_string", None)
    if isinstance(s, str):
        out.append(s)
    for sub in getattr(mob, "submobjects", None) or []:
        _tex_strings(sub, out)
    return out


def _anim_tex(anim) -> list[str]:
    # `to_add` is where TransformMatchingShapes keeps the line it morphs INTO (it is an
    # AnimationGroup, so it has no `target_mobject` of its own).
    out: list[str] = []
    for attr in ("mobject", "target_mobject", "to_add"):
        target = getattr(anim, attr, None)
        if target is not None:
            _tex_strings(target, out)
    return out


def _run_beat():
    """Drive scene 04's beat-3 reveal with a FakeScene; return (scene, beat run time)."""
    deck = yaml.safe_load(DECK.read_text(encoding="utf-8"))
    spec = next(s for s in deck["scenes"] if s["id"] == SCENE_ID)
    blocks = build_blocks(spec, {"ground": "dark", "meta": deck["meta"], "scenes_by_id": {}})
    block = next(b for b in blocks if b.id == REVEAL)
    assert callable(block.anim), f"{SCENE_ID}/{REVEAL} must be hook-choreographed, not a stock reveal"
    scene = FakeScene(BEAT_SECONDS)
    total = TM.beat_run_time(scene, 18.0)
    block.anim(scene, block.mobject, "dark")
    return scene, total


def _new_content_events(scene) -> list[tuple[float, float, tuple]]:
    return [e for e in scene.events
            if any(type(a).__name__ in _NEW_ON_SCREEN for a in e[2])]


# -- (1) the beat is cut into stages -------------------------------------------

def test_beat_three_is_cut_into_at_least_four_reveal_stages():
    scene, _total = _run_beat()
    stages = _new_content_events(scene)
    assert len(stages) >= MIN_REVEAL_STAGES, (
        f"beat 3 puts something new on screen only {len(stages)} time(s); the approved fix "
        f"splits it into >= {MIN_REVEAL_STAGES} (identity / substitution / expansion / cancel)")


def test_the_four_prescribed_stages_are_the_ones_on_screen():
    """(a) the identity, (b) the u/v substitution, (c) the angle-sum expansion,
    (d) the surviving product -- each named by its own LaTeX, so a stage cannot be
    silently replaced by four fades of the same line."""
    scene, _total = _run_beat()
    shown = " || ".join(t for e in _new_content_events(scene) for a in e[2] for t in _anim_tex(a))
    for fragment in (r"\sin A-\sin B",              # (a) the identity itself
                     r"u=\frac{A+B}{2}",            # (b) the substitution
                     r"\sin(u+v)-\sin(u-v)",        # (c) what the angle-sum formulas expand
                     r"2\cos u\sin v"):             # (d) what survives the cancel
        assert fragment in shown, f"stage missing from beat 3: {fragment!r}"


# -- (2) no long stretch with nothing new --------------------------------------

def test_no_stretch_longer_than_the_acceptance_line_without_new_content():
    scene, total = _run_beat()
    stages = _new_content_events(scene)
    assert stages, "beat 3 reveals nothing at all"
    worst, where = 0.0, 0.0
    last_end = 0.0
    for start, run_time, _anims in stages:
        if start - last_end > worst:
            worst, where = start - last_end, last_end
        last_end = start + run_time
    if total - last_end > worst:                      # the tail, up to the end of the beat
        worst, where = total - last_end, last_end
    assert worst <= SIDE_BRANCH_MAX_GAP_SECONDS, (
        f"beat 3 holds {worst:.1f}s with nothing new on screen (from +{where:.1f}s); "
        f"the acceptance line is {SIDE_BRANCH_MAX_GAP_SECONDS}s")


# -- (3) the branch is marked --------------------------------------------------

def test_the_side_branch_carries_its_own_tag():
    """The `must` is not only "split the reveal": a beginner needs a mark saying THIS block
    is where the identity comes from, i.e. it can be set aside and the main line resumed."""
    from animations.ch03_trig_derivatives_hooks import _DRAFT_TAG

    scene, _total = _run_beat()
    entered = [t for e in _new_content_events(scene) for a in e[2] for t in _anim_tex(a)]
    assert any(_DRAFT_TAG.upper() in t.upper() for t in entered), (
        f"beat 3's draft column has no side-branch tag on screen (looking for {_DRAFT_TAG!r})")


# -- (4) the branch leaves as one ----------------------------------------------

def test_the_side_branch_leaves_as_one_block_shrinking():
    """SPEC-motion-language 規則 1: a temporary annotation leaves by shrinking as it fades --
    and the tag leaves WITH the draft, so the branch closes instead of being cleared piecemeal."""
    from animations.ch03_trig_derivatives_hooks import _DRAFT_TAG

    scene, _total = _run_beat()
    exits = [a for _t, _rt, anims in scene.events for a in anims
             if type(a).__name__ == "FadeOut" and (getattr(a, "scale_factor", 1) or 1) < 1.0]
    assert exits, "the draft does not shrink as it fades out (規則 1: 臨時標註縮小加淡出)"
    assert any(_DRAFT_TAG.upper() in t.upper() for a in exits for t in _anim_tex(a)), (
        "the side-branch tag does not leave with the block it heads")


if __name__ == "__main__":
    import sys, traceback
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS {name}")
            except Exception:
                fails += 1; print(f"FAIL {name}"); traceback.print_exc()
    sys.exit(1 if fails else 0)

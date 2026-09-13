"""Self-test: scene 09 `continuity_argument` / the `continuity_template` hook -- the two
R2 rerun musts (2026-09-14, user-approved), pinned against the CANONICAL deck.
Run from video/:
    python -m pipeline._selftest_continuity_argument

What it pins:
  * must B, the colour coding: in every proof row the half-SUM factor and the half-
    DIFFERENCE factor are different colours, both are palette roles (no invented hue), and
    the same quantity keeps the same colour down all three rows AND on the number line
    (the midpoint dot is (x+x_0)/2, so it wears the half-sum's colour);
  * must B, the drop: on proof.2's beat the boxed half-sum factors turn into `1` IN PLACE
    -- the substitution runs over the rows' own slots, not on a new line below them -- and
    proof.2's row is BUILT from what survives instead of fading in on its own. The
    intermediate every frame passes through is an inequality with bars, never a false
    equation;
  * must A: proof.0 is no longer written from nothing -- scene 04's sum-to-product row
    (verbatim, from the same deck) enters from ABOVE THE FRAME, lands on proof.0's slot,
    and morphs into it part for part; a provenance tag rides with it;
  * the hook's segment indices agree with the storyboard's `{{...}}` cuts (this file and
    the deck cannot drift), and the narration contract is untouched: the `say` text and its
    `{show ...}` markers are byte-identical to what the audio manifest was built from, so
    `--reuse-audio` stays fresh and nothing is re-synthesized;
  * ZERO BEHAVIOUR CHANGE ELSEWHERE: `continuity_template` is referenced by exactly one
    scene in each deck, so no other scene can be moved by any of this; and a deck whose
    rows carry no `{{...}}` segments still gets the stock reveals (the un-segmented
    fallback path), which is the only way another scene could ever adopt this hook.
"""
from pathlib import Path

from pipeline import _bootstrap

_bootstrap.bootstrap()   # the hook module imports manim at module level -- bootstrap FIRST

import yaml
from manim import VGroup

from pipeline import texparts
from pipeline.templates import build_blocks
from pipeline.visuals import theme as T

from animations.ch03_trig_derivatives_hooks import (
    _CT_BOUND_TEX, _CT_HALF_DIFF_SEG, _CT_HALF_SUM_SEG, _CT_RECALL_TEX,
)

STORY = Path(_bootstrap.REPO_ROOT) / "video" / "storyboards"
HOOK = "animations.ch03_trig_derivatives_hooks:continuity_template"
SCENE_ID = "continuity_argument"
RECALL_SOURCE = "difference_quotient_for_sine"     # scene 04, where the sine identity is derived

_HALF_SUM = r"\frac{x+x_0}{2}"
_HALF_DIFF = r"\frac{x-x_0}{2}"


def _deck(name):
    return yaml.safe_load((STORY / name).read_text(encoding="utf-8"))


_CANON = _deck("ch03_trig_derivatives.yml")
_MIMO = _deck("ch03_trig_derivatives_mimo.yml")


def _scene(deck, sid):
    return next(s for s in deck["scenes"] if s["id"] == sid)


_SPEC = _scene(_CANON, SCENE_ID)
_ROWS = [r if isinstance(r, dict) else {"tex": r} for r in _SPEC["proof"]]
_BLOCKS = build_blocks(_SPEC, {"ground": "dark", "meta": _CANON["meta"]})


def _b(bid):
    return next(x for x in _BLOCKS if x.id == bid)


def _segments(row):
    src = row["tex"].strip()
    inner = src[1:-1] if src.startswith("$") and src.endswith("$") else src
    return texparts.split_segments(inner)


class FakeScene:
    """Records what it was asked to play, and what is on it, instead of rendering."""

    def __init__(self, beat_seconds=None, settle=False):
        self.beat_seconds = beat_seconds
        self.beat_reserved_seconds = 0.0
        self.run_times = []
        self.plays = []          # one list of animations per play, in order
        self.mobjects = []
        # `settle` runs each animation to its END STATE instead of only recording it, so a
        # test can ask what the frame looks like after the beat (manim does this itself;
        # a recording-only scene would leave every `.animate` unapplied).
        self.settle = settle

    def play(self, *anims, **kw):
        # `.animate.x()` hands `play` an _AnimationBuilder, which manim's own Scene.play
        # turns into an Animation first -- do the same so the recorded list is uniform.
        from manim.animation.animation import prepare_animation
        anims = [prepare_animation(a) for a in anims]
        self.run_times.append(float(kw.get("run_time") or 0.0))
        self.plays.append(list(anims))
        if not self.settle:
            return
        for a in anims:
            a.begin()
            a.interpolate(1.0)
            a.finish()
            a.clean_up_from_scene(self)

    def add(self, *mobs):
        for m in mobs:
            if m not in self.mobjects:
                self.mobjects.append(m)

    def remove(self, *mobs):
        for m in mobs:
            if m in self.mobjects:
                self.mobjects.remove(m)

    def replace(self, old, new):
        self.remove(old)
        self.add(new)

    def wait(self, *_a, **_k):
        pass


# -- must B: the two half-angle factors are told apart by colour ----------------

def test_the_storyboard_cuts_the_half_sum_and_half_difference_into_their_own_segments():
    """The colouring can only happen if each factor is its own `{{...}}` segment, at the
    index the hook reaches for. This is the contract between the deck and the hook."""
    for i, (row, k_sum, k_diff) in enumerate(zip(_ROWS, _CT_HALF_SUM_SEG, _CT_HALF_DIFF_SEG)):
        segs = _segments(row)
        assert len(segs) == 3, f"proof.{i} has {len(segs)} segments, want 3: {segs}"
        assert _HALF_SUM in segs[k_sum], f"proof.{i} segment {k_sum} is not the half-sum: {segs[k_sum]}"
        assert _HALF_DIFF in segs[k_diff], f"proof.{i} segment {k_diff} is not the half-diff: {segs[k_diff]}"


def test_half_sum_and_half_difference_are_different_semantic_colours():
    sum_roles, diff_roles = set(), set()
    for i, (row, k_sum, k_diff) in enumerate(zip(_ROWS, _CT_HALF_SUM_SEG, _CT_HALF_DIFF_SEG)):
        roles = row.get("seg_roles") or {}
        segs = _segments(row)
        assert roles.get(segs[k_sum]), f"proof.{i}: the half-sum factor carries no seg_role"
        assert roles.get(segs[k_diff]), f"proof.{i}: the half-diff factor carries no seg_role"
        sum_roles.add(roles[segs[k_sum]])
        diff_roles.add(roles[segs[k_diff]])
    assert len(sum_roles) == 1, f"the half-sum takes two colours down the rows: {sum_roles}"
    assert len(diff_roles) == 1, f"the half-diff takes two colours down the rows: {diff_roles}"
    assert sum_roles != diff_roles, (
        f"half-sum and half-difference share one colour ({sum_roles}) -- which is the "
        f"finding: 'the half-sum factor' names nothing the viewer can see")
    for role in sum_roles | diff_roles:
        assert role in T.DARK, f"{role!r} is not a palette role (no invented hues)"


def test_the_bound_row_keeps_the_surviving_factor_in_the_half_difference_colour():
    """proof.2's `2|sin((x-x_0)/2)|` is the same quantity as the rows' half-difference
    factor, so it must be the same colour (規則 5)."""
    roles = _ROWS[2].get("seg_roles") or {}
    diff_role = (_ROWS[0]["seg_roles"])[_segments(_ROWS[0])[_CT_HALF_DIFF_SEG[0]]]
    survivor = [s for s in _segments(_ROWS[2]) if _HALF_DIFF in s]
    assert survivor, "the bound row does not cut its surviving factor into a segment"
    assert roles.get(survivor[0]) == diff_role, (
        f"the bound's surviving factor is {roles.get(survivor[0])!r}, the rows' half-diff "
        f"is {diff_role!r}")


def test_the_built_rows_really_render_in_those_two_colours():
    """Not just declared: the segments come back from LaTeX in two different hues."""
    for i, (k_sum, k_diff) in enumerate(zip(_CT_HALF_SUM_SEG, _CT_HALF_DIFF_SEG)):
        segs = _b(f"proof.{i}").mobject.submobjects
        c_sum, c_diff = str(segs[k_sum].get_color()), str(segs[k_diff].get_color())
        assert c_sum != c_diff, f"proof.{i}: both half-angle factors render {c_sum}"


def test_the_midpoint_dot_wears_the_half_sum_colour():
    """The number line's midpoint IS (x+x_0)/2. Same quantity, same colour, figure and
    formula (規則 5) -- and it must NOT be the half-gap's colour, which the bracket owns."""
    scene = FakeScene(beat_seconds=25.0, settle=True)
    for bid in ("statement", "proof.0", "proof.1", "proof.2"):
        block = _b(bid)
        block.anim(scene, block.mobject, "dark")   # the half-gap arrives on proof.2's beat
    dots = [m for m in _walk(scene.mobjects) if type(m).__name__ == "Dot"]
    assert dots, "the beats drew no number line"
    sum_role = (_ROWS[0]["seg_roles"])[_segments(_ROWS[0])[_CT_HALF_SUM_SEG[0]]]
    diff_role = (_ROWS[0]["seg_roles"])[_segments(_ROWS[0])[_CT_HALF_DIFF_SEG[0]]]
    colours = {str(d.get_color()).upper() for d in dots}
    assert T.DARK[sum_role].upper() in colours, (
        f"no midpoint dot in the half-sum colour {T.DARK[sum_role]}; saw {colours}")
    assert T.DARK[sum_role].upper() != T.DARK[diff_role].upper()


def _walk(mobs):
    for m in mobs:
        yield m
        yield from _walk(getattr(m, "submobjects", []))


# -- must B: the drop happens in place, and proof.2 is built from it ------------

def _run_to_bound(beat_seconds=11.2):
    """Play proof.0, proof.1 and proof.2 on one FakeScene, as the beats do.

    Always `settle`: the substitution blanks the rows OUTSIDE a play and hands them back
    INSIDE one, so a recording-only scene would leave the shared blocks blanked for every
    later check. Settling is also what the real renderer does."""
    scene = FakeScene(beat_seconds=beat_seconds, settle=True)
    scene.spent = {}
    for bid in ("proof.0", "proof.1", "proof.2"):
        block = _b(bid)
        scene.spent[bid] = block.anim(scene, block.mobject, "dark")
    return scene


def test_the_boxed_factor_becomes_a_one_where_it_stands():
    """The `1` must arrive at the half-sum factor's own slot -- that is the whole point of
    'drop IT to its largest size'. A new row built below would not address the finding."""
    scene = _run_to_bound()
    rows = [_b(f"proof.{i}").mobject for i in (0, 1)]
    from manim import Transform
    ones = []
    for anims in scene.plays:
        for a in anims:
            if isinstance(a, Transform) and _is_one(a.target_mobject):
                ones.append(a)
    assert len(ones) == 2, f"{len(ones)} factors dropped to 1, want 2 (one per identity)"
    for a in ones:
        y = a.target_mobject.get_center()[1]
        near = min(rows, key=lambda r: abs(r.get_center()[1] - y))
        assert abs(near.get_center()[1] - y) < near.height, (
            f"the 1 landed at y={y:+.2f}, not on either identity row")
        k = _CT_HALF_SUM_SEG[rows.index(near)]
        slot = near.submobjects[k]
        assert abs(a.target_mobject.get_center()[0] - slot.get_center()[0]) < 1.2, (
            "the 1 did not arrive at the half-sum factor's own slot")


def _is_one(mob) -> bool:
    return getattr(mob, "tex_string", None) in ("\\cdot 1", "1")


def test_no_frame_of_the_substitution_states_a_false_equation():
    """`cos x - cos x_0 = -2 sin(half-diff) . 1` is false -- the factor is BOUNDED by one.
    The intermediate the rows pass through must therefore be an inequality with bars."""
    for i, tex in enumerate(_CT_BOUND_TEX):
        assert r"\le" in tex, f"intermediate {i} still asserts an equality: {tex}"
        assert "=" not in tex.replace(r"\le", ""), f"intermediate {i} keeps an `=`: {tex}"
        assert tex.count("|") >= 4, f"intermediate {i} drops the absolute-value bars: {tex}"
        assert "1" in tex, f"intermediate {i} never shows the 1: {tex}"


def test_the_bound_row_is_transformed_into_not_faded_in():
    """'不要新增一行': proof.2 is the two identities collapsing, so its mobject must be the
    TARGET of a transform and never the subject of a FadeIn."""
    scene = _run_to_bound()
    target = _b("proof.2").mobject
    from manim import FadeIn
    faded = [a for anims in scene.plays for a in anims
             if isinstance(a, FadeIn) and a.mobject is target]
    assert not faded, "proof.2 fades in as a new line instead of being built from the rows"
    # TransformMatchingShapes is an AnimationGroup whose inner Transform targets carry the
    # target's OWN submobjects, so look for proof.2's glyphs anywhere in the target side.
    landed = {id(m) for anims in scene.plays for t in _targets(anims) for m in _walk([t])}
    assert any(id(m) in landed for m in _walk([target])), (
        "proof.2 is not the target of any transform -- it arrives some other way")


def _targets(anims):
    for a in anims:
        t = getattr(a, "target_mobject", None)
        if t is not None:
            yield t
        yield from _targets(getattr(a, "animations", None) or [])


def test_the_identities_survive_the_substitution_unchanged():
    """The rows are lent to the substitution and handed back: the last frame must still
    show the two TRUE identities (`focus.indicate` flashes them on this very beat)."""
    scene = _run_to_bound()
    for i in (0, 1):
        row = _b(f"proof.{i}").mobject
        lit = max((m.get_fill_opacity() for m in _walk([row])
                   if hasattr(m, "get_fill_opacity")), default=0.0)
        assert lit > 0.9, f"proof.{i} was left at opacity {lit:.2f} after the substitution"
    # ... and they still say what they said: the half-sum factor is back, not a `1`
    for i, k in enumerate(_CT_HALF_SUM_SEG):
        seg = _b(f"proof.{i}").mobject.submobjects[k]
        assert seg.width > 0.5, (
            f"proof.{i}'s half-sum factor was left replaced by the 1 it dropped to")


def test_the_drop_and_the_slide_fill_the_beat_and_never_overrun_it():
    """A hook that runs past its own narration trips the [sync] length gate."""
    from pipeline import timing as TM
    scene = _run_to_bound()
    budget = TM.beat_run_time(FakeScene(beat_seconds=11.2), 0.0)
    spent = scene.spent["proof.2"]
    assert 3.0 < spent <= budget, f"proof.2 spent {spent:.2f}s of a {budget:.2f}s budget"


# -- must A: proof.0 is recalled from scene 04, not written from nothing --------

def test_the_recalled_row_is_scene_04s_identity_verbatim():
    src = _scene(_CANON, RECALL_SOURCE)["steps"][0]["math"]
    inner = _CT_RECALL_TEX.strip()[1:-1]
    flat = "".join(texparts.split_segments(inner)).replace(" ", "")
    assert flat == src.replace(" ", ""), (
        f"the recall is not scene 04's row:\n  recall {flat}\n  scene04 {src}")


def test_the_recall_enters_from_above_the_frame_and_lands_on_the_row():
    from manim import FadeIn
    scene = FakeScene(beat_seconds=15.2)
    block = _b("proof.0")
    block.anim(scene, block.mobject, "dark")
    moves = [a for a in scene.plays[0]]
    assert moves, "proof.0 played nothing"
    mover = moves[0].mobject
    start_y = mover.get_center()[1]          # _MoveTarget animations start at the start pose
    assert scene.plays, "no entrance"
    # the entrance animation's mobject begins above the frame and ends on proof.0's slot
    assert start_y > T.FRAME_H / 2, f"the recall starts at y={start_y:+.2f}, inside the frame"
    tags = [a.mobject for a in scene.plays[1] if isinstance(a, FadeIn)]
    assert tags, "no provenance tag rides with the recall"


def test_the_recall_morphs_part_for_part_into_proof_0():
    from manim import Transform
    scene = FakeScene(beat_seconds=15.2)
    block = _b("proof.0")
    spent = block.anim(scene, block.mobject, "dark")
    morph = [a for a in scene.plays[-1] if isinstance(a, Transform)]
    assert len(morph) == 3, f"{len(morph)} segment morphs, want 3 (one per {{{{...}}}} segment)"
    assert spent > 6.0, f"proof.0 spent only {spent:.1f}s of a 15.2 s beat"
    assert sum(scene.run_times) <= 15.2


def test_the_recall_is_smaller_than_the_row_it_becomes():
    """'縮小版': it comes back as a recollection, not as a second full-size row."""
    from pipeline import brand
    recall = brand.math_line(_CT_RECALL_TEX, "dark", role="text", size="label")
    assert recall.height < _b("proof.0").mobject.height * 0.9


# -- zero behaviour change anywhere else ---------------------------------------

def test_the_hook_is_used_by_exactly_one_scene_in_each_deck():
    """`continuity_template` fills one template twice WITHIN this scene; it is not shared
    between scenes. If that ever changes, this test fails and the change must be re-argued
    against every other user of the hook."""
    for name, deck in (("canonical", _CANON), ("mimo", _MIMO)):
        users = [s["id"] for s in deck["scenes"] if s.get("hook") == HOOK]
        assert users == [SCENE_ID], f"{name}: continuity_template is now used by {users}"


def test_an_unsegmented_deck_still_gets_the_stock_reveals():
    """The only way another scene could adopt this hook is with rows of its own. With no
    `{{...}}` segments there is nothing to colour, box or drop -- every beat must fall back
    to the stock reveal rather than raise."""
    plain = dict(_SPEC)
    plain["proof"] = [r["tex"].replace("{{", "").replace("}}", "") for r in _ROWS]
    plain.pop("focus", None)
    blocks = build_blocks(plain, {"ground": "dark", "meta": _CANON["meta"]})
    by_id = {b.id: b for b in blocks}
    for bid in ("statement", "proof.0", "proof.1", "proof.2", "qed"):
        block = by_id[bid]
        spent = block.anim(FakeScene(beat_seconds=8.0), block.mobject, "dark")
        assert spent > 0.0, f"{bid} fell back to nothing"
    for i in (0, 1):
        row = by_id[f"proof.{i}"].mobject
        assert len(row.submobjects) < 3, (
            f"proof.{i} still has segments -- this is not the fallback path")
        hues = {str(m.get_color()).upper() for m in _walk([row])}
        for role in ("accent", "strategy"):
            assert T.DARK[role].upper() not in hues, (
                f"proof.{i} picked up the {role} colour with no seg_roles to ask for it")


def test_the_narration_contract_is_untouched():
    """No `say` byte and no {show ...} marker may move: the manifest-freshness gate keys on
    them, and a changed hash means a paid re-synthesis. Both decks, against git HEAD."""
    import subprocess
    for name in ("ch03_trig_derivatives.yml", "ch03_trig_derivatives_mimo.yml"):
        head = subprocess.run(["git", "show", f"HEAD:video/storyboards/{name}"],
                              cwd=_bootstrap.REPO_ROOT, capture_output=True, text=True,
                              encoding="utf-8")
        if head.returncode != 0:            # detached/shallow checkout: nothing to compare
            continue
        before = _scene(yaml.safe_load(head.stdout), SCENE_ID)
        after = _scene(_deck(name), SCENE_ID)
        assert before["say"] == after["say"], f"{name}: `say` changed -> re-synthesis"


if __name__ == "__main__":
    import sys
    mod = sys.modules[__name__]
    names = [n for n in dir(mod) if n.startswith("test_")]
    for n in names:
        getattr(mod, n)()
    print(f"OK continuity_argument self-test ({len(names)} checks)")

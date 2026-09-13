"""Self-test: the scene-06 hook `sector_inequality` -- the two six-lens `must`s the
2026-09-13 milestone review approved for it.
Run from video/:
    python -m pipeline._selftest_sector_inequality

What it pins (and why each one exists):

  * must A -- the `ineq` beat (+39.8 -> +62.5 s) used to be ONE paced walk of the
    inequality's three terms, which spreads three fades over ~21 s and therefore leaves
    ~6.5 s of frozen picture between them (measured still: +48.8 -> +57.0, the longest in
    the film at the 0.05% threshold). The narration in that gap names two regions by name
    ("the corner piece A B C", "the sliver between the chord A B and the arc") and neither
    reacts. So: two traced outlines (SPEC-motion-language rule 3 -- frame / brighten / dim,
    never a camera move) land on those two phrases, each paired with a flash of the SAME
    colour cell on the right (rule 5, semantic colour across figure and formula), and no
    gap in the beat may exceed the 6 s stillness line (rule 4).

  * must B -- the `sector` beat states the sector's area as a finished label (1/2 theta)
    with no derivation anywhere on screen, even though it is the one region of the three
    that has to be COMPUTED, and the one place in the whole film where the radian
    convention is actually load-bearing. So: (theta/2pi).pi.1^2 = 1/2 theta is written
    under the second peeled glyph, in two stages, inside the same beat.

Render-free: the hook's reveals are driven against a FakeScene that records what it was
asked to play, and the layout assertions read the BUILT (un-rendered) snapshot -- the same
snapshot sizecheck measures.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # the hook module imports manim at module level -- bootstrap FIRST

from pathlib import Path  # noqa: E402

import yaml  # noqa: E402
from manim import Create, Indicate, MathTex, SingleStringMathTex, Tex  # noqa: E402

from pipeline import focus as F  # noqa: E402
from pipeline.templates import build_blocks  # noqa: E402
from pipeline.visuals import theme as T  # noqa: E402

DECK = Path(__file__).resolve().parents[1] / "storyboards" / "ch03_trig_derivatives_mimo.yml"
SCENE_ID = "sector_inequality"

# Beat lengths measured off the locked §3.1 narration (rewatch pack, 2026-09-13):
# beat 7 `{show ineq}` = +39.8 -> +62.5 s, beat 5 `{show sector}` = +26.4 -> +32.7 s.
# `reserved` is what scene.py sets on `beat_reserved_seconds` before the reveal: the
# rule-3 indicate (0.8) plus a focus fade (0.4) for `ineq`, the focus fade alone for
# `sector` -- both beats declare a `focus:` entry that changes the dim set.
INEQ_BEAT_SECONDS, INEQ_RESERVED = 22.7, F.INDICATE_SECONDS + F.FADE_SECONDS
SECTOR_BEAT_SECONDS, SECTOR_RESERVED = 6.3, F.FADE_SECONDS
STILL_LIMIT_SECONDS = 6.0        # SPEC-motion-language rule 4 authoring line
TRACE_SECONDS = 0.8              # rule 3: "約 1 s" -- the same length as focus.INDICATE
# A play only counts as MOTION for rule 4 if a viewer -- and the 0.05%-of-pixels still
# detector `rewatch_pack` measures with -- can see it. This is why the `ineq` beat read as
# 8.2 s of frozen picture while its paced walk was firing every 4 s: the walk steps
# through the inequality's two `\le` operators as parts of their own, and one operator
# glyph is ~0.04 u^2 of a 14.2 x 8.0 frame, under that threshold. The bar here is the
# still detector's own, 0.06% of the frame (a bounding box OVER-states the pixels a glyph
# actually paints, so a hair above 0.05%): a lone `\le` falls under it, the smallest real
# term (1/2 theta, ~0.098) clears it, and a traced region (~7) is far above.
VISIBLE_AREA = 0.0006 * T.FRAME_W * T.FRAME_H


def _deck():
    doc = yaml.safe_load(DECK.read_text(encoding="utf-8"))
    return doc["meta"], {s["id"]: s for s in doc["scenes"]}


def _build():
    meta, by_id = _deck()
    return build_blocks(by_id[SCENE_ID], {"ground": "dark", "meta": meta, "scenes_by_id": by_id})


_BLOCKS = _build()


def _b(bid):
    return next(x for x in _BLOCKS if x.id == bid)


class FakeScene:
    """Records what it was asked to play / wait instead of rendering. `beat_seconds` and
    `beat_reserved_seconds` are what the real LessonScene sets before each beat."""

    def __init__(self, beat_seconds=None, reserved=0.0):
        self.beat_seconds = beat_seconds
        self.beat_reserved_seconds = reserved
        self.run_times = []
        self.anims = []
        self.waits = []
        self.timeline = []       # ("play"|"wait", seconds, screen area the play touches)

    def play(self, *anims, **kw):
        seconds = float(kw.get("run_time") or 0.0)
        self.run_times.append(seconds)
        self.anims.append(anims)
        self.timeline.append(("play", seconds, max((_area(a) for a in anims), default=0.0)))

    def wait(self, seconds=1.0):
        self.waits.append(float(seconds))
        self.timeline.append(("wait", float(seconds), 0.0))

    def add(self, *mobs):
        pass


def _drive(bid, beat_seconds, reserved):
    block, scene = _b(bid), FakeScene(beat_seconds=beat_seconds, reserved=reserved)
    spent = block.anim(scene, block.mobject, "dark")
    return scene, spent


def _flat_anims(scene):
    return [a for group in scene.anims for a in group]


def _tex_of(mob) -> str:
    """Every tex string under *mob*, joined -- what the viewer would read off the glyphs."""
    out = []
    if isinstance(mob, (Tex, MathTex, SingleStringMathTex)):
        out.append(str(getattr(mob, "tex_string", "")))
    for sub in getattr(mob, "submobjects", []) or []:
        out.append(_tex_of(sub))
    return " ".join(out)


def _box(mob):
    return (float(mob.get_left()[0]), float(mob.get_right()[0]),
            float(mob.get_bottom()[1]), float(mob.get_top()[1]))


def _area(anim) -> float:
    """Screen area (u^2) of what one animation touches -- see VISIBLE_AREA."""
    mob = getattr(anim, "mobject", None)
    if mob is None:
        return 0.0
    try:
        x0, x1, y0, y1 = _box(mob)
    except Exception:  # noqa: BLE001
        return 0.0
    return max(x1 - x0, 0.0) * max(y1 - y0, 0.0)


def _worst_visible_gap(scene) -> float:
    """The longest stretch of a beat with no visible motion in it (rule 4)."""
    worst, run = 0.0, 0.0
    for kind, seconds, area in scene.timeline:
        if kind == "play" and area >= VISIBLE_AREA:
            worst, run = max(worst, run), 0.0
        else:
            run += seconds
    return max(worst, run)


# -- must B: the sector's area is DERIVED on screen, not asserted ---------------

def test_the_sector_glyph_carries_the_area_derivation():
    """(theta/2pi).pi.1^2 must be somewhere in the `sector` block -- and only there."""
    tex = _tex_of(_b("sector").mobject)
    assert r"2\pi" in tex, f"no (theta/2pi) step under the sector glyph; got {tex!r}"
    assert "1^{2}" in tex or "1^2" in tex, f"no unit-radius factor in the step; got {tex!r}"
    for bid in ("tri_inner", "tri_outer"):
        other = _tex_of(_b(bid).mobject)
        assert r"2\pi" not in other, f"{bid} grew an area derivation it does not need"


def test_the_derivation_arrives_in_two_stages_inside_the_sector_beat():
    """The peel is three plays (region appears / copy flies / label+badge+chip); the
    derivation adds its two stages ON TOP of those, inside the same beat."""
    scene, spent = _drive("sector", SECTOR_BEAT_SECONDS, SECTOR_RESERVED)
    assert len(scene.run_times) >= 5, (
        f"sector beat played {len(scene.run_times)} times; want the 3 peel plays plus "
        "2 derivation stages")
    budget = SECTOR_BEAT_SECONDS - SECTOR_RESERVED
    assert spent <= budget + 1e-6, (
        f"the sector reveal spends {spent:.2f}s of a {budget:.2f}s budget -- it would "
        "overrun the beat and trip the [sync] hard gate")


def test_the_derivation_sits_under_the_sector_glyph_and_clear_of_the_inequality():
    dst2, ineq = _box(_b("sector").mobject), _box(_b("ineq").mobject)
    # it is INSIDE the sector block (so `exit:` and `focus:` move it with the glyph)
    assert dst2[2] < _box(_b("tri_inner").mobject)[2] - 0.10, (
        "the sector glyph's box did not grow downward -- the derivation is not part of it")
    assert dst2[2] > ineq[3], (
        f"the sector glyph (bottom {dst2[2]:.2f}) reaches into the inequality "
        f"(top {ineq[3]:.2f})")


def test_the_scene_still_fits_the_safe_area():
    right, top = T.FRAME_W / 2 - T.SAFE_MARGIN, T.FRAME_H / 2 - T.SAFE_MARGIN
    for b in _BLOCKS:
        if getattr(b, "layer", "content") in ("decoration", "background"):
            continue
        x0, x1, y0, y1 = _box(b.mobject)
        assert -right - 0.04 <= x0 and x1 <= right + 0.04, f"{b.id} spills in x: [{x0:.2f},{x1:.2f}]"
        assert -top - 0.04 <= y0 and y1 <= top + 0.04, f"{b.id} spills in y: [{y0:.2f},{y1:.2f}]"


# -- must A: the corner piece and the sliver are traced on their own phrases ----

def test_the_inequality_beat_traces_two_regions_and_flashes_their_cells():
    scene, _ = _drive("ineq", INEQ_BEAT_SECONDS, INEQ_RESERVED)
    anims = _flat_anims(scene)
    creates = [a for a in anims if isinstance(a, Create)]
    flashes = [a for a in anims if isinstance(a, Indicate)]
    assert len(creates) == 2, (
        f"want 2 traced outlines (corner piece A B C, then the sliver), got {len(creates)}")
    assert len(flashes) == 2, (
        f"each trace must flash the same-coloured cell on the right; got {len(flashes)}")
    traced = [round(t, 3) for t in scene.run_times if abs(t - TRACE_SECONDS) < 1e-6]
    assert len(traced) == 2, (
        f"the two traces must each run {TRACE_SECONDS}s (rule 3); run_times={scene.run_times}")


def test_the_sliver_sits_inside_the_corner_piece():
    """The narration's own claim -- "inside it sits the sliver" -- has to be true of the
    two shapes we draw, or the trace teaches the wrong containment."""
    scene, _ = _drive("ineq", INEQ_BEAT_SECONDS, INEQ_RESERVED)
    creates = [a for a in _flat_anims(scene) if isinstance(a, Create)]
    corner, sliver = (_box(a.mobject) for a in creates)
    assert (corner[0] - 0.02 <= sliver[0] and sliver[1] <= corner[1] + 0.02
            and corner[2] - 0.02 <= sliver[2] and sliver[3] <= corner[3] + 0.02), (
        f"sliver {sliver} is not inside corner piece {corner}")
    # both live in the MAIN figure, left of the three peeled glyphs
    assert corner[1] < _box(_b("tri_inner").mobject)[0], (
        "the traced regions must be on the source construction, not on the peeled row")


def test_no_gap_in_the_inequality_beat_exceeds_the_stillness_line():
    scene, _ = _drive("ineq", INEQ_BEAT_SECONDS, INEQ_RESERVED)
    worst = _worst_visible_gap(scene)
    assert worst < STILL_LIMIT_SECONDS, (
        f"the ineq beat still holds a frozen picture for {worst:.1f}s "
        f"(rule 4 line is {STILL_LIMIT_SECONDS}s); timeline="
        f"{[(k, round(s, 2), round(a, 2)) for k, s, a in scene.timeline]}")


def test_the_inequality_beat_does_not_overrun_its_beat():
    scene, spent = _drive("ineq", INEQ_BEAT_SECONDS, INEQ_RESERVED)
    budget = INEQ_BEAT_SECONDS - INEQ_RESERVED
    assert spent <= budget + 1e-6, (
        f"the ineq reveal spends {spent:.2f}s of a {budget:.2f}s budget -- the rule-3 "
        "indicate that follows it would then push the scene past its narration")
    played = sum(scene.run_times) + sum(scene.waits)
    assert abs(played - spent) < 1e-6, (
        f"the beat's choreography ({played:.2f}s) does not add up to what it reports "
        f"({spent:.2f}s)")


def test_the_inequality_beat_falls_back_off_beat():
    """Off-beat (the end-of-scene sweep-up, a selftest driving it bare) beat_seconds is
    None: the choreography must still terminate at a sane length, not run for a beat it
    does not have."""
    scene, spent = _drive("ineq", None, 0.0)
    assert 2.0 < spent < 12.0, f"off-beat fallback spent {spent:.1f}s"


if __name__ == "__main__":
    test_the_sector_glyph_carries_the_area_derivation()
    test_the_derivation_arrives_in_two_stages_inside_the_sector_beat()
    test_the_derivation_sits_under_the_sector_glyph_and_clear_of_the_inequality()
    test_the_scene_still_fits_the_safe_area()
    test_the_inequality_beat_traces_two_regions_and_flashes_their_cells()
    test_the_sliver_sits_inside_the_corner_piece()
    test_no_gap_in_the_inequality_beat_exceeds_the_stillness_line()
    test_the_inequality_beat_does_not_overrun_its_beat()
    test_the_inequality_beat_falls_back_off_beat()
    print("OK sector_inequality self-test")

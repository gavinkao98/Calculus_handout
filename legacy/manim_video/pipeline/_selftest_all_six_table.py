"""Self-test: the six-derivatives table -- the two scenes the six-lens milestone review
sent back, fixed by one shared object.

Run from video/:
    python -m pipeline._selftest_all_six_table

What it pins (and why each one exists):

  * the OBJECT -- the section's deliverable is six rows, in one canonical order, carrying the
    approved provenance colours: rows 1-2 (sin'=cos, cos'=-sin) in `result` blue, the colour
    of the two theorem scenes that proved them; rows 3-6 in `practice` green, scene 22's own
    accent. A "six derivatives" table that silently grew a seventh row, lost one, or drifted
    to a different palette axis would still render, so the count, the order and the two roles
    are asserted, not eyeballed. Every row goes through `brand.math_line`
    (CONTENT_METHODOLOGY §5), so it is a `MathTex`, not a hand-built one.

  * scene 22 beat 5 -- the film's LONGEST still (measured 11.0 s at +27.0-38.0 on the
    shared-layer-v1 cut): `{show result}` landed the row and the screen then froze through
    "and all six are done, every one built on sin'=cos and cos'=-sin". So: the beat must play
    the six rows as six separate visible reveals on top of its own row transform, and no gap
    inside it may exceed the 6 s stillness line of SPEC-motion-language 規則 4.

  * scene 26 beat 5 -- the film's second-longest still (10.5 s at +36.2-46.8) and its last
    substantive picture. Nothing new is said there (the degrees formula is already in
    point.3's text), so the test pins that the ONE reveal became several separated visible
    moments and that the same 6 s line holds. point.2's beat must land all six rows, so the
    recap answers "what was sec' again?" without a rewind.

  * the layout -- both tables have to sit inside the broadcast-safe area and clear of the
    blocks they were squeezed in beside (scene 22's retreated chain, the recap's points).

Render-free: the reveals are driven against a FakeScene that records what it was asked to
play, and the layout assertions read the BUILT (un-rendered) snapshot -- the same snapshot
sizecheck measures.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # the hook module imports manim at module level -- bootstrap FIRST

from pathlib import Path  # noqa: E402

import yaml  # noqa: E402
from manim import MathTex, Tex, SingleStringMathTex  # noqa: E402

from pipeline import pacing  # noqa: E402
from pipeline.templates import build_blocks  # noqa: E402
from pipeline.visuals import theme as T  # noqa: E402

from animations import ch03_trig_derivatives_hooks as H  # noqa: E402

DECK = Path(__file__).resolve().parents[1] / "storyboards" / "ch03_trig_derivatives_mimo.yml"
TABLE_ID = "all_six"

# Beat lengths read off the LOCKED narration's own manifest
# (output/ch03/s3.1/audio_mimo/manifest.json, beats[4] of each scene) and what scene.py sets
# on `beat_reserved_seconds` before the reveal -- 0 for both, neither beat declares a
# `focus:` entry or carries a `reveal_with` rider.
S22_RESULT_BEAT = 11.86      # 22 all_six_cot_csc, beat 5 (+24.46 -> +36.32)
S26_POINT2_BEAT = 7.42       # 26 recap, beat 4 (+17.66 -> +25.08)
S26_POINT3_BEAT = 20.20      # 26 recap, beat 5 (+25.08 -> +45.28)
STILL_LIMIT_SECONDS = 6.0    # SPEC-motion-language 規則 4 authoring line
# A play only counts as MOTION for rule 4 if a viewer -- and the 0.05%-of-pixels still
# detector `rewatch_pack` measures with -- can see it. Same bar as
# `_selftest_sector_inequality`: 0.06% of the frame, a hair above the detector's own
# threshold because a bounding box OVER-states the pixels a glyph actually paints.
VISIBLE_AREA = 0.0006 * T.FRAME_W * T.FRAME_H


def _deck():
    doc = yaml.safe_load(DECK.read_text(encoding="utf-8"))
    return doc["meta"], {s["id"]: s for s in doc["scenes"]}


def _build(scene_id):
    meta, by_id = _deck()
    return build_blocks(by_id[scene_id], {"ground": "dark", "meta": meta, "scenes_by_id": by_id})


_S22 = _build("all_six_cot_csc")
_S26 = _build("recap")


def _b(blocks, bid):
    return next(x for x in blocks if x.id == bid)


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

    def remove(self, *mobs):
        pass


def _drive(blocks, bid, beat_seconds, reserved=0.0):
    block, scene = _b(blocks, bid), FakeScene(beat_seconds=beat_seconds, reserved=reserved)
    spent = block.anim(scene, block.mobject, "dark")
    return scene, spent


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


def _visible_plays(scene) -> int:
    return sum(1 for kind, _s, area in scene.timeline if kind == "play" and area >= VISIBLE_AREA)


def _worst_visible_gap(scene) -> float:
    """The longest stretch of a beat with no visible motion in it (rule 4)."""
    worst, run = 0.0, 0.0
    for kind, seconds, area in scene.timeline:
        if kind == "play" and area >= VISIBLE_AREA:
            worst, run = max(worst, run), 0.0
        else:
            run += seconds
    return max(worst, run)


def _tex_of(mob) -> str:
    out = []
    if isinstance(mob, (Tex, MathTex, SingleStringMathTex)):
        out.append(str(getattr(mob, "tex_string", "")))
    for sub in getattr(mob, "submobjects", []) or []:
        out.append(_tex_of(sub))
    return " ".join(out)


# -- the object ----------------------------------------------------------------

def test_the_table_is_six_rows_in_the_canonical_order():
    for layout in ("column", "banner"):
        table = H.six_derivatives_table("dark", layout=layout)
        assert len(table.rows) == 6, f"{layout}: {len(table.rows)} rows, want the six derivatives"
        for row, (tex, _role) in zip(table.rows, H._SIX_DERIVATIVES):
            assert isinstance(row, MathTex), (
                f"{layout}: row {tex!r} is a {type(row).__name__}, not a brand.math_line MathTex "
                "-- a bare MathTex bypasses the deck colour table (CONTENT_METHODOLOGY §5)")
        got = _tex_of(table)
        for name in (r"\sin'", r"\cos'", r"\tan'", r"\cot'", r"\sec'", r"\csc'"):
            assert name in got, f"{layout}: {name} missing from the table; got {got!r}"


def test_the_two_first_principle_rows_wear_the_theorem_colour():
    """Provenance colouring, not function colouring: sin'/cos' carry `result` (the accent of
    the two theorem scenes that proved them), the quotient-rule four carry `practice` (scene
    22's own accent). Both are calcbook hues -- no new colour is invented."""
    table = H.six_derivatives_table("dark", layout="column")
    want_blue, want_green = T.color("dark", "result"), T.color("dark", "practice")
    for i in H.FROM_FIRST_PRINCIPLES:
        got = table.rows[i].get_color().to_hex().lower()
        assert got == want_blue.lower(), (
            f"row {i} ({H._SIX_DERIVATIVES[i][0]}) is {got}, want result blue {want_blue}")
    for i in H.FROM_QUOTIENT_RULE:
        got = table.rows[i].get_color().to_hex().lower()
        assert got == want_green.lower(), (
            f"row {i} ({H._SIX_DERIVATIVES[i][0]}) is {got}, want practice green {want_green}")


# -- scene 22: the film's longest still ----------------------------------------

def test_scene22_declares_the_table_block():
    table = _b(_S22, TABLE_ID).mobject
    assert len(getattr(table, "rows", [])) == 6, (
        "scene 22 has no six-row table block -- the scene that says 'all six are done' still "
        "never shows all six")


def test_scene22_result_beat_lands_all_six_rows():
    scene, _spent = _drive(_S22, "result", S22_RESULT_BEAT)
    played = {id(m) for group in scene.anims for a in group
              for m in [getattr(a, "mobject", None)] if m is not None}
    rows = _b(_S22, TABLE_ID).mobject.rows
    missing = [H._SIX_DERIVATIVES[i][0] for i, r in enumerate(rows) if id(r) not in played]
    assert not missing, f"these rows never enter in the beat that declares them done: {missing}"
    assert _visible_plays(scene) >= 7, (
        f"the beat plays {_visible_plays(scene)} visible animations; want the row's own "
        "transform plus one per derivative")


def test_scene22_result_beat_has_no_frozen_stretch():
    scene, spent = _drive(_S22, "result", S22_RESULT_BEAT)
    gap = _worst_visible_gap(scene)
    assert gap <= STILL_LIMIT_SECONDS, (
        f"beat 5 still freezes for {gap:.1f}s (was 11.0 s measured) -- rule 4 line is "
        f"{STILL_LIMIT_SECONDS:.0f}s")
    assert spent <= S22_RESULT_BEAT + 1e-6, (
        f"the reveal spends {spent:.2f}s of an {S22_RESULT_BEAT:.2f}s beat -- it would overrun "
        "and trip the [sync] hard gate")


def test_scene22_table_clears_the_retreated_chain_and_the_frame():
    table = _b(_S22, TABLE_ID).mobject
    x0, x1, y0, y1 = _box(table)
    eqs = [_b(_S22, rid).mobject.submobjects[0] for rid in ("step.0", "step.1", "step.2", "result")]
    left = min(float(e.get_left()[0]) for e in eqs)
    width = max(float(e.get_right()[0]) for e in eqs) - left
    chain_right = left + width * H._RETREAT_SCALE      # where the retreat leaves the chain
    assert x0 > chain_right, (
        f"the table's left edge {x0:.2f} sits on the retreated chain (right edge "
        f"{chain_right:.2f}) -- they would collide on screen")
    safe_x, safe_y = T.FRAME_W / 2 - T.SAFE_MARGIN, T.FRAME_H / 2 - T.SAFE_MARGIN
    assert -safe_x - 0.04 <= x0 and x1 <= safe_x + 0.04, f"table spills in x: [{x0:.2f},{x1:.2f}]"
    assert -safe_y - 0.04 <= y0 and y1 <= safe_y + 0.04, f"table spills in y: [{y0:.2f},{y1:.2f}]"


# -- scene 26: the recap --------------------------------------------------------

def test_recap_point2_beat_lands_all_six_rows():
    """"From those two ... tangent, cotangent, secant, cosecant" -- the six are on screen from
    the beat that indexes them, and stay there to the end of the film."""
    scene, spent = _drive(_S26, "point.2", S26_POINT2_BEAT)
    played = {id(m) for group in scene.anims for a in group
              for m in [getattr(a, "mobject", None)] if m is not None}
    rows = _b(_S26, TABLE_ID).mobject.rows
    missing = [H._SIX_DERIVATIVES[i][0] for i, r in enumerate(rows) if id(r) not in played]
    assert not missing, f"the recap never shows {missing} -- sec' still needs a rewind"
    assert spent <= S26_POINT2_BEAT + 1e-6, (
        f"point.2 spends {spent:.2f}s of a {S26_POINT2_BEAT:.2f}s beat")


def test_recap_point3_beat_is_cut_into_separate_moments():
    scene, spent = _drive(_S26, "point.3", S26_POINT3_BEAT)
    assert _visible_plays(scene) >= 5, (
        f"the 20.2 s closing beat plays {_visible_plays(scene)} visible animations; it used to "
        "be one fade followed by 10.5 s of frozen picture")
    gap = _worst_visible_gap(scene)
    assert gap <= STILL_LIMIT_SECONDS, (
        f"the closing beat still freezes for {gap:.1f}s (was 10.5 s measured) -- rule 4 line is "
        f"{STILL_LIMIT_SECONDS:.0f}s")
    assert spent <= S26_POINT3_BEAT + 1e-6, (
        f"point.3 spends {spent:.2f}s of a {S26_POINT3_BEAT:.2f}s beat")


def test_the_radian_caution_lands_on_the_factor_alone():
    """`\\tfrac{\\pi}{180}` is found by geometry (the fraction rule), so the caution ink goes on
    that factor and not on the whole sentence."""
    row = _b(_S26, "point.3").mobject
    parts = pacing.block_parts(row)
    assert len(parts) > 1, "point.3 no longer wraps -- the degrees clause has no line of its own"
    factor = H._tfrac_cluster(parts[-1])
    assert factor is not None, "no fraction rule found on the degrees line"
    tail = _box(parts[-1])
    box = _box(factor)
    assert box[1] - box[0] < 0.35 * (tail[1] - tail[0]), (
        f"the located factor spans {box[1] - box[0]:.2f}u of a {tail[1] - tail[0]:.2f}u line -- "
        "that is the sentence, not pi/180")


def test_recap_banner_sits_in_the_empty_bottom_band():
    table = _b(_S26, TABLE_ID).mobject
    x0, x1, y0, y1 = _box(table)
    points_bottom = min(float(_b(_S26, f"point.{i}").mobject.get_bottom()[1]) for i in range(4))
    assert y1 < points_bottom, (
        f"the banner's top {y1:.2f} reaches into the points (lowest {points_bottom:.2f})")
    # ... and so does the caution frame that closes round its first row at the very end of the
    # beat, which sits ABOVE that row: the first cut of this hook left 0.05u of daylight
    # between the frame and point.3's last line, which reads on screen as a collision.
    frame_top = y1 + H._CAUTION_BUFF
    assert points_bottom - frame_top > 0.12, (
        f"the radian-caution frame's top {frame_top:.2f} grazes point.3 "
        f"(bottom {points_bottom:.2f})")
    safe_x, safe_y = T.FRAME_W / 2 - T.SAFE_MARGIN, T.FRAME_H / 2 - T.SAFE_MARGIN
    assert -safe_x - 0.04 <= x0 and x1 <= safe_x + 0.04, f"banner spills in x: [{x0:.2f},{x1:.2f}]"
    assert -safe_y - 0.04 <= y0 and y1 <= safe_y + 0.04, f"banner spills in y: [{y0:.2f},{y1:.2f}]"


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in tests:
        try:
            fn()
            print(f"  ok   {fn.__name__}")
        except Exception as exc:  # noqa: BLE001, PERF203
            # Exception, not just AssertionError: with the `hook:` line deleted the table
            # block is simply absent, and "no such block" has to read as a red test rather
            # than a traceback that stops the run at the first one.
            failed += 1
            print(f"  FAIL {fn.__name__}: {type(exc).__name__}: {exc}")
    print(f"[selftest all_six_table] {len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

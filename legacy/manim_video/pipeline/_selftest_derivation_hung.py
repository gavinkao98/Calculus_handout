"""Self-test: a HUNG reason may not push its chain past the bottom safe margin. Run from video/:
    python -m pipeline._selftest_derivation_hung
    python -m pipeline._selftest_derivation_hung --emit-fixture   # re-record contract 3

Background. r1 Task E (`_rail_plan`, commit bb2f1e5) gave the row whose reason cannot keep a
full leader somewhere to go: it leaves the shared rail and, if its own equation is too wide
even for that, HANGS its reason on the line under the equation (``HANG_GAP`` below it). That
bought the leader back, but the hang is pure extra HEIGHT, and `_common._biased_y` deliberately
top-anchors a chain too tall for its body zone -- so the extra height went straight out of the
bottom of the frame: ``difference_quotient_for_sine``'s tag landed 0.23 u (~31 px) below the
broadcast-safe margin, next to the corner motif (sizecheck: "block 'result' spills past the
safe margin").

Three contracts:

  1. BOTTOM CLAMP -- a chain that WOULD HAVE FIT without the hang must not cross the bottom
     safe line because of it. (Red before the fix: the fixture below is
     ``difference_quotient_for_sine``, measured bottom -3.6825 vs safe -3.4519.)
  2. THE HANG STILL READS -- the hung reason may not touch its own equation, the row above it
     or the row below it. The clamp moves the whole chain, so this is what pins that it did
     not move rows INTO each other. Checked with a hung row in the MIDDLE of a chain (a
     `check` row follows the hung `result`), which is the only shape where "the row below"
     exists.
  3. NOTHING ELSE MOVES -- a chain with no hung row keeps the exact coordinates it had before
     the clamp existed (fixture recorded on the pre-change tree, 2026-09-14).

Manim-backed (it builds real Tex to measure it) -- same class as _selftest_derivation_rail.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # the template imports manim at module level -- bootstrap FIRST

import logging  # noqa: E402

logging.disable(logging.INFO)

from manim import MathTex, Tex, VGroup  # noqa: E402

from pipeline.templates import build_blocks  # noqa: E402
from pipeline.visuals import theme as T  # noqa: E402

_META = {"id": "_d", "chapter": "Demo", "section": "0.0", "title": "T", "theme": "midnight"}
SAFE_BOTTOM = -T.FRAME_H / 2 + T.SAFE_MARGIN
_TOL = 0.04          # the same tolerance sizecheck._overflow_issues allows
_FIX_TOL = 1e-3

_ROW_IDS = ("step.0", "step.1", "step.2", "result", "check")

# ``difference_quotient_for_sine`` (ch03_trig_derivatives scene 04) inlined, so the test does
# not depend on a deck: 4 rows, the result's 8.34 u equation against its 3.87 u tag -- the one
# shape in all 23 decks that hangs. The scaffold motive is kept because it sets the body
# zone's top edge, which is half of the budget this test is about.
_HUNG = {
    "id": "hung", "kind": "content", "template": "derivation", "accent": "derivation",
    "title": "The Difference Quotient for Sine",
    "scaffold": {"motive": "Sum-to-product turns the difference of sines into a product."},
    "say": "A. {show step.0} B. {show step.1} C. {show step.2} D. {show result} E.",
    "steps": [
        {"math": r"\sin A-\sin B = 2\cos\frac{A+B}{2}\,\sin\frac{A-B}{2}",
         "reason": "sum-to-product"},
        {"math": r"\sin(x+h)-\sin x = 2\cos\!\left(x+\frac h2\right)\sin\frac h2",
         "reason": r"$A=x+h,\ B=x$"},
        {"math": r"\frac{\sin(x+h)-\sin x}{h} = \cos\!\left(x+\frac h2\right)"
                 r"\cdot\frac{\sin(h/2)}{h/2}",
         "reason": r"write $h=2\cdot(h/2)$"},
    ],
    "result": {"math": r"\cos\!\left(x+\frac h2\right)\to\cos x\quad\text{and}\quad "
                       r"\frac{\sin(h/2)}{h/2}\to 1",
               "reason": "continuity + the limit"},
}

# the same chain with a `check` row after the hung result: the only shape where a hung row has
# a row BELOW it, which is what contract 2 needs to see.
_HUNG_MID = dict(_HUNG, id="hung_mid",
                 say=_HUNG["say"][:-2] + " {show check} F.",
                 check={"math": r"\lim_{h\to0}\frac{\sin(x+h)-\sin x}{h} = \cos x",
                        "reason": "both factors settled"})

# the same chain with a short result tag: nothing leaves the rail, nothing hangs -- the
# untouched path contract 3 pins.
_PLAIN = dict(_HUNG, id="plain",
              result=dict(_HUNG["result"], reason="both limits"))


def _blocks(spec):
    return build_blocks(spec, {"ground": "dark", "meta": _META})


def _rows(blocks):
    return [b for b in blocks if b.id in _ROW_IDS]


def _tex_leaves(mob, out=None):
    """Every Tex / MathTex leaf under *mob*, in build order."""
    out = [] if out is None else out
    if isinstance(mob, (Tex, MathTex)):
        out.append(mob)
        return out
    for sub in getattr(mob, "submobjects", []):
        _tex_leaves(sub, out)
    return out


def _box(m):
    return (float(m.get_left()[0]), float(m.get_right()[0]),
            float(m.get_bottom()[1]), float(m.get_top()[1]))


def _is_equation(m) -> bool:
    """In this manim, ``Tex`` SUBCLASSES ``MathTex`` (tex_mobject.py:607), so "is it the
    equation?" has to exclude Tex explicitly -- a reason (prose or eyebrow) is a Tex and
    would otherwise be counted as an equation."""
    return isinstance(m, MathTex) and not isinstance(m, Tex)


def _hung_rows(blocks):
    """Row ids whose reason sits BELOW its equation (that is what hanging looks like from
    outside the template): a Tex leaf whose top is under the row's MathTex bottom."""
    out = []
    for b in _rows(blocks):
        eqs = [m for m in _tex_leaves(b.mobject) if _is_equation(m)]
        prose = [m for m in _tex_leaves(b.mobject) if not _is_equation(m)]
        if not eqs or not prose:
            continue
        eq_bottom = min(float(m.get_bottom()[1]) for m in eqs)
        if any(float(p.get_top()[1]) <= eq_bottom + 1e-9 for p in prose):
            out.append(b.id)
    return out


def _overlap(a, b) -> float:
    return (max(0.0, min(a[1], b[1]) - max(a[0], b[0]))
            * max(0.0, min(a[3], b[3]) - max(a[2], b[2])))


# -- 1. the hang may not cost the chain its bottom safe margin ------------------

def test_a_hung_chain_that_would_have_fit_stays_inside_the_safe_margin():
    blocks = _blocks(_HUNG)
    hung = _hung_rows(blocks)
    assert hung == ["result"], f"fixture no longer hangs a row (got {hung}) -- test is vacuous"
    worst = min(_rows(blocks), key=lambda b: float(b.mobject.get_bottom()[1]))
    low = float(worst.mobject.get_bottom()[1])
    assert low >= SAFE_BOTTOM - _TOL, (
        f"hung chain spills {SAFE_BOTTOM - low:.4f} u past the bottom safe margin "
        f"({low:.4f} vs {SAFE_BOTTOM:.4f}); lowest row {worst.id}")


def test_the_clamp_does_not_lift_the_chain_into_its_title():
    """The clamp buys its room from the title gap, so it has to leave a block boundary there:
    at least `HANG_GAP`, the template's own smallest legible separation."""
    from pipeline.templates.derivation import HANG_GAP

    blocks = _blocks(_HUNG)
    head = [b for b in blocks if b.id in ("scaffold.motive", "title")]
    assert head, [b.id for b in blocks]
    ref_bottom = min(float(b.mobject.get_bottom()[1]) for b in head)
    top = max(float(b.mobject.get_top()[1]) for b in _rows(blocks))
    assert ref_bottom - top >= HANG_GAP - _FIX_TOL, (
        f"chain top {top:.4f} left only {ref_bottom - top:.4f} u under the line above it "
        f"({ref_bottom:.4f}); floor is HANG_GAP = {HANG_GAP}")


# -- 2. the hung reason still reads as its own line ----------------------------

def test_the_hung_reason_touches_neither_its_equation_nor_its_neighbours():
    blocks = _blocks(_HUNG_MID)
    hung = _hung_rows(blocks)
    assert hung == ["result"], f"fixture no longer hangs a middle row (got {hung})"
    rows = {b.id: b for b in _rows(blocks)}
    assert "check" in rows, "the fixture must keep a row BELOW the hung one"
    row = rows["result"]
    eqs = [m for m in _tex_leaves(row.mobject) if _is_equation(m)]
    reason = next(m for m in _tex_leaves(row.mobject) if not _is_equation(m))
    rbox = _box(reason)
    for eq in eqs:
        assert _overlap(rbox, _box(eq)) <= 0.0, "hung reason overlaps its own equation"
    for other in ("step.2", "check"):
        assert _overlap(rbox, _box(rows[other].mobject)) <= 0.0, (
            f"hung reason overlaps row '{other}'")


# -- 3. a chain with no hung row is byte-identical to the pre-clamp tree --------

# Recorded on the PRE-CHANGE tree (2026-09-14, `--emit-fixture`): every drawn part of every
# row block of _PLAIN, as (block id, part index, left, right, bottom, top). Part 1 of each row
# is the dotted leader (zero height); the rail sits at x = 2.9157, pinned by step.2's
# MIN_LEADER. If the clamp ever moves a chain that does not hang, these numbers move.
_PLAIN_FIXTURE = [
    ('step.0', 0, -6.3703, -0.559, 0.6193, 1.3419),
    ('step.0', 1, -0.339, 2.7357, 0.9806, 0.9806),
    ('step.0', 2, 2.9157, 5.5186, 0.8189, 1.1423),
    ('step.1', 0, -6.3703, -0.3792, -0.6149, 0.2193),
    ('step.1', 1, -0.1592, 2.7357, -0.1978, -0.1978),
    ('step.1', 2, 2.9157, 5.0439, -0.3229, -0.0727),
    ('step.2', 0, -6.3703, 0.1955, -1.849, -1.0149),
    ('step.2', 1, 0.4155, 2.7357, -1.4319, -1.4319),
    ('step.2', 2, 2.9157, 5.6734, -1.6074, -1.2565),
    ('result', 0, -6.3703, 1.9657, -3.3264, -2.249),
    ('result', 1, 2.1857, 2.7357, -2.7877, -2.7877),
    ('result', 2, 2.9157, 4.8223, -2.894, -2.6814),
]


def test_a_chain_with_no_hung_row_is_unmoved():
    blocks = _blocks(_PLAIN)
    assert _hung_rows(blocks) == [], "the no-hang fixture started hanging a row"
    got = _fixture_rows(blocks)
    assert len(got) == len(_PLAIN_FIXTURE), (
        f"{len(got)} leaves vs {len(_PLAIN_FIXTURE)} recorded -- re-record with --emit-fixture "
        f"only if the change was MEANT to move an unhung chain")
    bad = []
    for now, was in zip(got, _PLAIN_FIXTURE):
        assert now[0] == was[0] and now[1] == was[1], f"leaf order changed: {now} vs {was}"
        for k, name in ((2, "left"), (3, "right"), (4, "bottom"), (5, "top")):
            if abs(now[k] - was[k]) > _FIX_TOL:
                bad.append(f"{now[0]}#{now[1]} {name} {was[k]:.4f} -> {now[k]:.4f}")
    assert not bad, "an unhung chain moved:\n  " + "\n  ".join(bad)


def _all_leaves(mob, out=None):
    """Every drawn part under *mob* -- equation, dotted leader and reason -- so the fixture
    sees a leader that moved or vanished, not only the glyphs. Only VGroups are containers
    here (`text_glow` wraps a row in one); a MathTex or a DashedLine IS the part."""
    out = [] if out is None else out
    if not isinstance(mob, VGroup):
        out.append(mob)
        return out
    for sub in mob.submobjects:
        _all_leaves(sub, out)
    return out


def _fixture_rows(blocks):
    out = []
    for b in _rows(blocks):
        for i, leaf in enumerate(_all_leaves(b.mobject)):
            x0, x1, y0, y1 = _box(leaf)
            out.append((b.id, i, round(x0, 4), round(x1, 4), round(y0, 4), round(y1, 4)))
    return out


if __name__ == "__main__":
    import sys
    import traceback

    if "--emit-fixture" in sys.argv:
        for row in _fixture_rows(_blocks(_PLAIN)):
            print(f"    {row!r},")
        raise SystemExit(0)

    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except Exception:
                fails += 1
                print(f"FAIL {name}")
                traceback.print_exc()
    sys.exit(1 if fails else 0)

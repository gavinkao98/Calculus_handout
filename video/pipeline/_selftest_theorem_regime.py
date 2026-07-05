"""Self-test: theorem_proof statement-card measure-driven regime. Run from video/:
    python -m pipeline._selftest_theorem_regime

Locks the rail-vs-band decision + short-card shrink-wrap + the sizecheck promotion
advisory against the _demo_theorem_regime.yml fixture (short prose -> rail/shrink,
long prose -> full-width band, wide formula -> band without shrinking). See
DESIGN "字卡定位" and the Codex read-only review (2026-07-05).
"""
import pathlib

import yaml

from pipeline import _bootstrap

_bootstrap.bootstrap()   # theorem_proof top-level imports manim -- bootstrap FIRST (repo rule)

from manim import MathTex, VGroup

from pipeline import brand, sizecheck
from pipeline.templates import build_blocks
from pipeline.templates import theorem_proof as TP
from pipeline.templates._common import CONTENT_W, RAIL_W, SPINE_X

_DEMO = pathlib.Path(__file__).resolve().parent.parent / "storyboards" / "_demo_theorem_regime.yml"
_DATA = yaml.safe_load(_DEMO.read_text(encoding="utf-8"))
_META = _DATA["meta"]
_SCENES = {s["id"]: s for s in _DATA["scenes"]}
_INNER_W = RAIL_W - 2 * TP._CARD_PAD_X


def _build(sid: str):
    return build_blocks(_SCENES[sid], {"ground": "dark", "meta": _META})


def _block(blocks, bid: str):
    return next(b.mobject for b in blocks if b.id == bid)


def _widest_math(mob):
    best = None
    stack = [mob]
    while stack:
        m = stack.pop()
        if isinstance(m, MathTex) and (best is None or m.width > best.width):
            best = m
        stack.extend(getattr(m, "submobjects", []))
    return best


# -- SHORT prose: right rail, shrink-wrapped ---------------------------------

def test_short_regime_not_promoted():
    promote, n_lines, is_formula = TP.statement_regime(_SCENES["theorem_regime_short"], "dark")
    assert promote is False and is_formula is False and n_lines <= TP.RAIL_MAX_LINES


def test_short_card_in_rail_shrinkwrapped():
    card = _block(_build("theorem_regime_short"), "statement")
    assert card.get_center()[0] > 0                       # right half (the rail)
    assert card.width < RAIL_W - 0.15                     # shrink-wrapped, not full rail
    assert abs(card.get_right()[0] - (SPINE_X + CONTENT_W)) < 0.12   # right edge on the gutter


# -- LONG prose: full-width band, proof stacks below -------------------------

def test_long_regime_promoted():
    promote, n_lines, is_formula = TP.statement_regime(_SCENES["theorem_regime_long"], "dark")
    assert promote is True and is_formula is False and n_lines > TP.RAIL_MAX_LINES


def test_long_band_full_width_proof_below():
    blocks = _build("theorem_regime_long")
    card = _block(blocks, "statement")
    assert abs(card.get_left()[0] - SPINE_X) < 0.15       # band left edge on the spine
    assert card.width > 0.85 * CONTENT_W                  # genuinely full-width
    proof0 = _block(blocks, "proof.0")
    assert proof0.get_top()[1] < card.get_bottom()[1]     # proof stacks BELOW the band


# -- WIDE formula: band, natural size (NOT shrunk into the rail) -------------

def test_wide_formula_regime():
    promote, _n, is_formula = TP.statement_regime(_SCENES["theorem_regime_wide_formula"], "dark")
    assert promote is True and is_formula is True


def test_wide_formula_band_not_shrunk():
    stmt = _SCENES["theorem_regime_wide_formula"]["statement"]
    ref = brand.prose(stmt, "dark", role="primary", size="h3")   # natural, unclamped
    assert ref.width > _INNER_W                            # it IS wider than the rail interior
    card = _block(_build("theorem_regime_wide_formula"), "statement")
    assert abs(card.get_left()[0] - SPINE_X) < 0.15 and card.width > 0.85 * CONTENT_W
    glyph = _widest_math(card)
    assert glyph is not None and abs(glyph.width - ref.width) < 0.05   # not scaled down


# -- WRAPS but proof too long: aesthetic prefers band, capacity forces a rail fallback ------

def test_tall_proof_prefers_band_but_falls_back_to_rail():
    scene = _SCENES["theorem_regime_tall_proof"]
    promote_pref, n_lines, is_formula = TP.statement_regime(scene, "dark")
    assert promote_pref is True and is_formula is False and n_lines > TP.RAIL_MAX_LINES
    card = _block(_build("theorem_regime_tall_proof"), "statement")
    # capacity fallback: a band would overflow, so the built card is the RAIL, not a full-width band.
    # (a wrapping statement fills the rail measure, so its card ~= RAIL_W -- test "not a band", i.e.
    # clearly narrower than CONTENT_W and hung on the right gutter, NOT "< RAIL_W".)
    assert card.width < 0.6 * CONTENT_W
    assert abs(card.get_right()[0] - (SPINE_X + CONTENT_W)) < 0.12


# -- sizecheck promotion advisory (reads the built band geometry, no drift) ------

def _band_warns():
    issues = sizecheck.check_scenes(_META, list(_DATA["scenes"]))
    return {sid: any(sev == "warn" and sid in msg and "band" in msg.lower()
                     for sev, msg in issues)
            for sid in _SCENES}


def test_sizecheck_advises_on_promotion_only():
    warns = _band_warns()
    assert warns["theorem_regime_long"] and warns["theorem_regime_wide_formula"]
    assert not warns["theorem_regime_short"]
    # a scene that fell back to rail (band would overflow) is NOT a band -> no band advisory
    assert not warns["theorem_regime_tall_proof"]


def test_regime_demos_have_no_overflow_error():
    issues = sizecheck.check_scenes(_META, list(_DATA["scenes"]))
    errs = [m for s, m in issues if s == "error"]
    assert not errs, errs


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

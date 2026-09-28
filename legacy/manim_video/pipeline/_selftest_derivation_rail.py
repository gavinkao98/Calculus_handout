"""Self-test: the `derivation` reason rail always has somewhere to go. Run from video/:
    python -m pipeline._selftest_derivation_rail

Three contracts, all from the shared-layer v1 backlog (items 3 / 4 / 13 -- "Instrument Sans
is wider than Plex Sans, and the rail is where that shows up"):

  * FALLBACK (backlog 4) -- ``MIN_LEADER`` is a FLOOR, and before this test nothing happened
    when the floor could not be met: the rail was simply capped at the frame edge and the
    widest row got whatever leader was left (17.9 px == about two dots on
    ``difference_quotient_for_sine``'s result row, measured 2026-09-14). The fallback is
    ``_rail_plan``: a row that cannot get a full leader AND leave the reason column its
    right-edge tolerance leaves the SHARED column and stops driving the rail, so every row
    still on the rail gets >= MIN_LEADER; it keeps its own line if a full leader fits there
    and otherwise hangs its reason on the line under its own equation.
  * RIGHT-EDGE TOLERANCE (backlog 13) -- the reason column must keep ``RIGHT_SLACK`` of
    clear space at ``SPINE_X + CONTENT_W``; scenes were landing flush on it (0.0 px).
  * BOLD WIDTH (backlog 3) -- the bold interword space was retuned in the TeX preamble, so
    the estimator's coverage of BOLD text is pinned here the same way
    ``_selftest_text_metrics`` pins it for regular text.

Manim-backed (it builds real Tex to measure it) -- same class as _selftest_worked_example.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # the template imports manim at module level -- bootstrap FIRST

import logging  # noqa: E402

logging.disable(logging.INFO)

from manim import MathTex, Tex  # noqa: E402

from pipeline import brand  # noqa: E402
from pipeline.templates import build_blocks, derivation as D  # noqa: E402
from pipeline.templates._common import CONTENT_W, RAIL_X, SPINE_X  # noqa: E402
from pipeline.visuals import theme as T  # noqa: E402

RIGHT = SPINE_X + CONTENT_W
_META = {"id": "_d", "chapter": "Demo", "section": "0.0", "title": "T", "theme": "midnight"}
_EPS = 1e-6

# A reason so long that no chain of usable width can host it on the rail as well.
_LONG_REASON = ("differentiate the outer function first and only then the inner one, "
                "keeping the argument untouched throughout")


def _spec(**over):
    spec = {
        "id": "d", "kind": "content", "template": "derivation", "accent": "derivation",
        "title": "A chain that reaches the rail",
        "say": "A. {show step.0} B. {show step.1} C. {show result} D.",
        "steps": [
            {"math": r"\frac{d}{dx}\sin x = \lim_{h\to 0}\frac{\sin(x+h)-\sin x}{h}",
             "reason": "definition of the derivative"},
            {"math": r"= \lim_{h\to 0}\frac{\sin x\cos h + \cos x\sin h - \sin x}{h}",
             "reason": "angle-addition formula"},
        ],
        "result": {"math": r"\frac{d}{dx}\sin x = \cos x", "reason": "the two limits"},
    }
    spec.update(over)
    return spec


def _blocks(spec=None):
    return build_blocks(spec or _spec(), {"ground": "dark", "meta": _META})


def _right_edges(mob) -> list[float]:
    out = []

    def walk(m):
        if isinstance(m, (Tex, MathTex)):
            out.append(m.get_right()[0])
        for s in getattr(m, "submobjects", []):
            walk(s)
    walk(mob)
    return out


# -- 1. the fallback fires and keeps everything inside the frame ---------------

def test_long_reason_hangs_and_stays_in_frame():
    """A reason too long to share a line with its equation drops to the line under it --
    and every piece of the scene still ends left of the content edge."""
    spec = _spec(result={"math": r"\frac{d}{dx}\sin x = \cos x", "reason": _LONG_REASON})
    blocks = _blocks(spec)
    rowb = [b for b in blocks if b.id in ("step.0", "step.1", "result")]
    assert rowb, [b.id for b in blocks]
    over = [(b.id, x) for b in rowb for x in _right_edges(b.mobject) if x > RIGHT + _EPS]
    assert not over, f"content past SPINE_X+CONTENT_W ({RIGHT:.3f}): {over}"


def test_rail_plan_takes_the_row_that_cannot_keep_a_leader_off_the_rail():
    """_rail_plan is the fallback's decision function: widths in, (reason_x, off_rail) out."""
    # the measured difference_quotient_for_sine shape (2026-09-14): 8.34u result equation
    # against a 3.87u reason -- 12.61u of the 12.74u content width, no room for a leader.
    eqs = [5.81, 5.99, 6.57, 8.34]
    rsn = [2.60, 2.13, 2.76, 3.87]
    reason_x, off_rail = D._rail_plan(eqs, rsn)
    assert off_rail == {3}, off_rail
    for i, (e, _r) in enumerate(zip(eqs, rsn)):
        if i in off_rail:
            continue
        lead = (reason_x - D.LEAD_PAD_R) - (SPINE_X + e + D.LEAD_PAD_L)
        assert lead >= D.MIN_LEADER - _EPS, f"row {i} leader {lead:.3f} < {D.MIN_LEADER}"
    widest = max(r for i, r in enumerate(rsn) if i not in off_rail)
    assert RIGHT - (reason_x + widest) >= D.RIGHT_SLACK - _EPS


def test_an_off_rail_row_keeps_its_own_line_when_the_leader_still_fits():
    """companion_limit's shape: the 4.60u result tag is what the shared column cannot host,
    but its own 3.36u equation leaves room for a full leader on its own line -- dropping it
    a line for nothing pushed the chain past the bottom safe margin (measured 2026-09-14).
    So the rows still on the rail keep MIN_LEADER, and the off-rail row keeps its line."""
    eqs = [7.32, 5.02, 3.36]
    rsn = [3.11, 2.13, 4.60]
    reason_x, off_rail = D._rail_plan(eqs, rsn)
    assert off_rail == {2}, off_rail
    lead = (reason_x - D.LEAD_PAD_R) - (SPINE_X + eqs[0] + D.LEAD_PAD_L)
    assert lead >= D.MIN_LEADER - _EPS, lead
    own_x = min(reason_x, RIGHT - D.RIGHT_SLACK - rsn[2])
    assert SPINE_X + eqs[2] + D.LEAD_PAD_L + D.MIN_LEADER + D.LEAD_PAD_R <= own_x, (
        "the off-rail row should still fit a full leader on its own line")


def test_reasons_keep_the_right_edge_tolerance():
    """Backlog 13: the reason column may not land flush on the content edge."""
    spec = _spec(result={"math": r"\frac{d}{dx}\sin x = \cos x", "reason": _LONG_REASON})
    for blocks in (_blocks(), _blocks(spec)):
        rowb = [b for b in blocks if b.id in ("step.0", "step.1", "result")]
        worst = max(x for b in rowb for x in _right_edges(b.mobject))
        assert worst <= RIGHT - D.RIGHT_SLACK + 0.02, (
            f"reason column within {RIGHT - worst:.3f}u of the content edge "
            f"(RIGHT_SLACK = {D.RIGHT_SLACK})")


# -- 2. a normal chain is untouched -------------------------------------------

def test_normal_chain_keeps_min_leader_and_does_not_fall_back():
    """The fallback must be invisible on chains that fit -- nothing leaves the rail, every
    leader at or above the floor."""
    eqs = [1.48, 1.48, 1.48, 5.54]        # measured ch01 invert_a_rational
    rsn = [2.17, 2.29, 0.85, 1.74]
    reason_x, off_rail = D._rail_plan(eqs, rsn)
    assert off_rail == set(), off_rail
    for e in eqs:
        lead = (reason_x - D.LEAD_PAD_R) - (SPINE_X + e + D.LEAD_PAD_L)
        assert lead >= D.MIN_LEADER - _EPS, f"leader {lead:.3f} < {D.MIN_LEADER}"


def test_a_reasonless_row_never_pins_the_rail():
    """A row with no reason needs no leader, so its width must not push the rail right --
    that was what starved ch03_chain_rule/example_chain_times_quotient's reason column of
    its right-edge tolerance (rail at 3.51u, 0.0 px of slack)."""
    eqs = [7.06, 6.65, 10.39]
    rsn = [2.86, 2.03, None]
    reason_x, off_rail = D._rail_plan(eqs, rsn)
    assert off_rail == set(), off_rail
    assert RIGHT - (reason_x + 2.86) >= D.RIGHT_SLACK - _EPS


# -- 3. the bold face after the interword-space retune -------------------------

# Bold advances are wider than regular (measured 2026-09-14: lowercase alphabet 142.740 pt
# vs 135.890 pt at 10 pt = +5.04 %, and the preamble now scales the bold interword space by
# the same factor). brand._WIDTH_K is calibrated on REGULAR prose -- it is the width source
# for wrap_text/body_text, and nothing wraps bold -- so what is pinned here is the same
# band _selftest_text_metrics pins for regular: the estimate may not fall more than 6 %
# below the real bold advance. Going strictly above bold instead would mean raising
# _WIDTH_K ~4 %, which re-wraps every prose line in every deck for text that is never
# measured by the estimator.
_BOLD_FLOOR = 0.94
_BOLD_CASES = (
    "A function is one-to-one when different inputs",
    "Derivatives of the six trigonometric functions",
    "Why the difference quotient for sine needs two limits",
    "Continuity and the sine limit",
)
_FS = 100.0


def test_estimate_width_covers_bold_titles():
    bad = []
    for s in _BOLD_CASES:
        measured = Tex(r"\textbf{" + s.replace(" ", r"\ ") + "}", font_size=_FS).width
        ratio = brand.estimate_text_width(s, _FS) / measured
        if ratio < _BOLD_FLOOR:
            bad.append(f"{ratio:.4f}  {s!r}")
    assert not bad, (
        f"brand.estimate_text_width under-estimates BOLD by more than "
        f"{(1 - _BOLD_FLOOR) * 100:.0f}%:\n  " + "\n  ".join(bad))


# Word-space density, measured THROUGH the renderer: the word gap of a real sentence as a
# fraction of that series' own lowercase advance. A two-letter probe (`x\ x` minus `xx`) is
# dominated by one kern pair and reads 1.5 % high on bold, so the metric averages three
# sentences. Measured 2026-09-14 with the retuned \fontdimen2: bold sits +0.5 % / +1.2 % /
# +1.7 % on the three, mean +1.1 %; before the retune it was about -8 %.
_DENSITY_SAMPLES = (
    ("The squeeze theorem", "Thesqueezetheorem", 2),
    ("Derivatives of the six trigonometric functions",
     "Derivativesofthesixtrigonometricfunctions", 5),
    ("A function is one-to-one when different inputs",
     "Afunctionisone-to-onewhendifferentinputs", 6),
)


def test_bold_interword_space_matches_regular_density():
    """Backlog 3: bold shipped a NARROWER word space than regular while its glyphs are
    wider, so bold titles read as clumped words. The two series must now spend the same
    fraction of their own advance on a word gap."""
    def w(s: str, bold: bool) -> float:
        return Tex((r"\textbf{" + s + "}") if bold else s, font_size=_FS).width

    alphabet = {b: w("abcdefghijklmnopqrstuvwxyz", b) for b in (False, True)}
    ratios, detail = [], []
    for natural, nospace, gaps in _DENSITY_SAMPLES:
        d = {}
        for b in (False, True):
            d[b] = (w(natural.replace(" ", r"\ "), b) - w(nospace, b)) / gaps / alphabet[b]
        ratios.append(d[True] / d[False])
        detail.append(f"{natural[:28]!r} {d[True] / d[False] * 100 - 100:+.1f}%")
    mean = sum(ratios) / len(ratios)
    assert abs(mean - 1.0) <= 0.02, (
        f"bold word gap is {mean * 100 - 100:+.1f}% off regular's relative density "
        f"({'; '.join(detail)}) -- retune \\fontdimen2 in _bootstrap.apply_tex_template")


def test_cap_height_is_unchanged_by_the_bold_retune():
    """The T1 invariant the fontdimen change must not disturb: TEXT cap height stays on
    the 0.006624 u/px anchor (regular; \\fontdimen2 is word space, not glyph height)."""
    h_per_fs = Tex("H", font_size=_FS).height / _FS
    cap_per_px = h_per_fs * T.PX_TO_FS * T.TEXT_SCALE
    assert abs(cap_per_px - 0.006624) / 0.006624 <= 0.02, cap_per_px


if __name__ == "__main__":
    import sys
    import traceback

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

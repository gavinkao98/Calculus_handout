"""Self-test: the two text-metric constants stay calibrated to the text font. Run from video/:
    python -m pipeline._selftest_text_metrics

Swapping the on-screen TEXT family (Plex Sans -> Instrument Sans, 2026-09-13) changes both
of the numbers that translate an authored px into rendered geometry, and NEITHER is derivable
from the other:

  * ``theme.TEXT_SCALE`` -- the cap height of ``_text_fs(size)`` text must stay at the Times
    anchor 0.006624 u/px, or every zone the layout was tuned against shifts.
  * ``brand._WIDTH_K``   -- ``estimate_text_width`` is the ONLY width source for ``wrap_text``
    (Route A dropped real measurement), so it must track the true advance from just above;
    a font whose advances are wider than the constant overflows every wrapped line.

This test turns "a font swap MUST recalibrate both constants" from a convention into a gate:
it goes red on the old constants under a new font, whichever font that is. ``theme.PX_TO_FS``
is the MATH anchor and is deliberately NOT covered -- math did not change family.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()

from manim import Tex

from pipeline import brand
from pipeline.visuals import theme as T

CAP_ANCHOR = 0.006624          # manim units of cap height per authored px (Times anchor)
CAP_TOL = 0.02                 # +-2%
FS = 100.0                     # measure at a large font_size; everything here is linear in fs

# The sentence brand._WIDTH_K is calibrated on (same one Route A used for Plex). The
# constant is "measured advance + 2%", so on THIS string the estimate must not be short.
_CALIBRATION = "A function is one-to-one when different inputs"

# Representative wrapped prose. A single character-count knob cannot bound every letter
# mix, so the guard here is a floor on how far below the real advance it may fall; the
# worst case measured at calibration time was -5.31% (Plex) / -4.56% (Instrument Sans).
_PROSE_CASES = (
    _CALIBRATION,
    "The squeeze theorem pins the quotient between two bounds.",
    "Every continuous function on a closed interval attains its maximum",
    "Differentiate the quotient and simplify the numerator.",
    "This limit is the derivative of sine at zero.",
    "Read the chain rule outward: differentiate the outer function first.",
)
WIDTH_FLOOR = 0.94             # estimate >= 94% of measured on every prose case


def test_cap_height_anchor():
    """_text_fs(px) must render cap height at the Times anchor (-> fixes TEXT_SCALE)."""
    h_per_fs = Tex(r"H", font_size=FS).height / FS
    cap_per_px = h_per_fs * T.PX_TO_FS * T.TEXT_SCALE
    rel = abs(cap_per_px - CAP_ANCHOR) / CAP_ANCHOR
    assert rel <= CAP_TOL, (
        f"cap height {cap_per_px:.6f} u/px is {rel * 100:.1f}% off the {CAP_ANCHOR} anchor; "
        f"retune theme.TEXT_SCALE = round({CAP_ANCHOR} / ({h_per_fs:.6f} * {T.PX_TO_FS}), 4)"
    )


def _measured(s: str) -> float:
    return Tex(s.replace(" ", r"\ "), font_size=FS).width


def test_estimate_width_covers_calibration_sentence():
    """On the sentence _WIDTH_K is calibrated on, the estimate carries its +2% margin."""
    measured = _measured(_CALIBRATION)
    estimated = brand.estimate_text_width(_CALIBRATION, FS)
    assert estimated >= measured, (
        f"brand._WIDTH_K is short on its own calibration sentence: estimate "
        f"{estimated:.3f} < measured {measured:.3f}; retune _WIDTH_K = "
        f"round({measured / (sum(0.5 if c == ' ' else 1 for c in _CALIBRATION) * FS):.6f}"
        f" * 1.02, 5)"
    )


def test_estimate_width_not_systematically_short():
    """Across real prose the estimate may not fall far below the advance (-> wrap overflow)."""
    bad = []
    for s in _PROSE_CASES:
        measured = _measured(s)
        ratio = brand.estimate_text_width(s, FS) / measured
        if ratio < WIDTH_FLOOR:
            bad.append(f"{ratio:.4f}  {s!r}")
    assert not bad, (
        f"brand._WIDTH_K under-estimates by more than {(1 - WIDTH_FLOOR) * 100:.0f}% -- "
        "wrapped lines will overflow:\n  " + "\n  ".join(bad)
    )


def test_preamble_names_the_text_family():
    """The TeX template must actually load the vendored Instrument Sans style file."""
    from manim import config

    _bootstrap.apply_tex_template()
    preamble = config.tex_template.preamble
    assert r"\usepackage{InstrumentSans}" in preamble, preamble
    assert "plex-sans" not in preamble, preamble
    assert r"\usepackage{lmodern}" in preamble, preamble        # math stays Latin Modern
    assert r"\usepackage{plex-mono}" in preamble, preamble      # eyebrow mono stays Plex Mono


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

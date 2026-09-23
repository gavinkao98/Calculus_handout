"""Self-test: graph single mode -- regressions from the 2026-09-23 code review
(D1-09 default axes). Run from video/:
    python -m pipeline._selftest_graph_single
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # graph.py imports manim at module level -- bootstrap FIRST

from pipeline.templates import build_blocks

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}
_DEFAULT_AXES = {"x_range": [-1.45, 1.45, 0.5], "y_range": [-0.28, 1.55, 0.25]}
_PARABOLA = {"kind": "function", "expression": "x*x", "label": "$y=x^2$"}


def _spec(**over):
    spec = {"id": "g", "kind": "content", "template": "graph", "mode": "single",
            "title": "A Graph", "say": "Look. {show plot.0} curve.",
            "plots": [dict(_PARABOLA)]}
    spec.update(over)
    return spec


def _by_id(spec):
    return {b.id: b for b in build_blocks(spec, {"ground": "dark", "meta": _META})}


def _bbox(mob):
    return tuple(round(float(v), 6) for v in (mob.get_left()[0], mob.get_right()[0],
                                               mob.get_bottom()[1], mob.get_top()[1]))


# -- D1-09: single mode fills in the default axes it already builds with ---------------

def test_single_mode_without_axes_uses_the_default_axes():
    """No `axes:` at all: _build_single already draws the default axes -- the plots must be
    laid on them too (was KeyError: 'axes'), exactly as if the defaults had been written."""
    implicit = _by_id(_spec())
    explicit = _by_id(_spec(axes=dict(_DEFAULT_AXES)))
    for bid in ("axes", "plot.0", "label.0"):
        assert _bbox(implicit[bid].mobject) == _bbox(explicit[bid].mobject), bid


def test_single_mode_axes_without_ranges_uses_the_default_ranges():
    """`axes: {x_length: 6}` -- the ranges fall back to the defaults (was KeyError: 'x_range')."""
    implicit = _by_id(_spec(axes={"x_length": 6}))
    explicit = _by_id(_spec(axes=dict(_DEFAULT_AXES, x_length=6)))
    for bid in ("axes", "plot.0"):
        assert _bbox(implicit[bid].mobject) == _bbox(explicit[bid].mobject), bid


def test_single_mode_with_neither_plots_nor_axes_builds():
    """A hook-led graph scene with no plots and no axes (was KeyError: 'axes')."""
    by = _by_id(_spec(plots=[], say="Look."))
    assert "axes" in by and "title" in by


def test_single_mode_inset_without_axes_builds():
    """The inset reads the same axes: no `axes:` must not break it either."""
    by = _by_id(_spec(say="Look. {show plot.0} curve. {show inset} closer.",
                      inset={"x": [0.5, 1.0], "y": [0.25, 1.0], "corner": "top_right"}))
    assert "inset" in by


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

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


# -- D1-07: label_x is honoured on a y_clip curve, and a bad one says so ------------------

_BLOWUP = {"kind": "function", "expression": "1/x**2", "x_range": [0.3, 2.2],
           "color_role": "secondary", "label": "$y=1/x^2$", "label_x": 0.6}
_BLOWUP_AXES = {"x_range": [-0.2, 2.4, 0.5], "y_range": [-0.3, 6, 1]}


def _label_and_anchor(plot, lx):
    by = _by_id(_spec(axes=dict(_BLOWUP_AXES), plots=[plot], say="x"))
    lab, axes = by["label.0"].mobject, by["axes"].mobject
    return lab, axes.c2p(lx, 1 / lx ** 2)


def test_label_x_is_honoured_on_a_y_clip_curve():
    """y_clip builds the curve as a VGroup of segments; label_x used to go through
    input_to_graph_point, which needs a ParametricFunction -- the exception was swallowed and
    the label silently landed at the curve's tail (x=2.2) instead of beside x=0.6."""
    lab, anchor = _label_and_anchor(dict(_BLOWUP, y_clip=True), 0.6)
    assert abs(float(lab.get_center()[0]) - float(anchor[0])) < 1e-3, (lab.get_center(), anchor)
    gap = float(lab.get_bottom()[1]) - float(anchor[1])   # label_side up: sits just above
    assert 0 < gap < 0.3, (gap, lab.get_center(), anchor)


def test_label_x_without_y_clip_is_unchanged():
    """Control: the plain axes.plot curve placed label_x correctly all along."""
    lab, anchor = _label_and_anchor(dict(_BLOWUP, x_range=[0.45, 2.2]), 0.6)
    assert abs(float(lab.get_center()[0]) - float(anchor[0])) < 1e-3, (lab.get_center(), anchor)


def test_label_x_with_no_point_on_the_curve_warns():
    """label_x where the expression has no value (a pole): the default placement is used,
    but not silently -- the author's position did not take."""
    import contextlib, io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _by_id(_spec(axes=dict(_BLOWUP_AXES), say="x",
                     plots=[dict(_BLOWUP, y_clip=True, label_x=0)]))
    out = [ln for ln in buf.getvalue().splitlines() if ln.startswith("[graph]")]
    assert out and "label_x" in out[0], buf.getvalue()[-500:]


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

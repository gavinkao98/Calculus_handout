"""Self-test: graph `inset:` lens -- the pieces the 2026-09-23 code review found wrong
(D1-01 late-bound sweep closures). Run from video/:
    python -m pipeline._selftest_inset_lens

The base contract (panel in its corner, clipping, follow: true riding the main tracker) is
_selftest_inset; this file pins the regressions on top of it.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # graph.py imports manim at module level -- bootstrap FIRST

from pipeline.templates import build_blocks
from pipeline.visuals import theme as T

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}

_AXES = {"x_range": [-0.3, 1.4, 0.5], "y_range": [-0.3, 1.4, 0.5],
         "x_length": 5.4, "y_length": 5.4}
_BX, _BY = 0.8253, 0.5646          # (cos 0.6, sin 0.6)
_ARC = {"kind": "function", "expression": "sqrt(1 - x*x)", "x_range": [0, 1],
        "color_role": "result"}
_CEIL = {"kind": "function", "expression": "1.2 - 0.3*x", "x_range": [0, 1.2],
         "color_role": "result"}
_SWEEP = {"kind": "sweep", "x_from": 1.0, "x_to": _BX, "seconds": 2.0, "follow": [0],
          "gap": [1, 0], "color_role": "accent"}
_POINT = {"kind": "point", "point": [_BX, _BY], "color_role": "concept", "reveal": True}
_INSET = {"x": [0.7, 1.05], "y": [0.35, 0.95], "corner": "top_right", "follow": True}


def _spec(plots, inset=_INSET, **over):
    spec = {"id": "g", "kind": "content", "template": "graph", "mode": "single",
            "accent": "definition", "title": "A Graph",
            "say": "Look. {show inset} Closer. {show plot.2} Sweep. {show plot.3} B.",
            "axes": dict(_AXES), "plots": [dict(p) for p in plots]}
    if inset is not None:
        spec["inset"] = dict(inset)
    spec.update(over)
    return spec


def _by_id(spec, meta=_META):
    return {b.id: b for b in build_blocks(spec, {"ground": "dark", "meta": meta})}


def _moving(panel):
    """The follow: true sweep pieces of the lens, in build order (band, rule, dots ...)."""
    return [m for m in panel.submobjects if m.get_updaters()]


def _drawn_colours(mob) -> set[str]:
    """Hex colours of everything in *mob*'s family that actually draws (fill or stroke)."""
    out = set()
    for s in mob.get_family():
        if not len(s.points):
            continue
        if s.get_fill_opacity() > 0:
            out.add(s.get_fill_color().to_hex().upper())
        if s.get_stroke_width() > 0 and s.get_stroke_opacity() > 0:
            out.add(s.get_stroke_color().to_hex().upper())
    return out


def _go_live(sweep_mob, x):
    """What the render does once {show plot.N} has played: the main sweep is live and its
    tracker moves; the lens pieces are redrawn by their updaters."""
    sweep_mob._sweep_live = True
    sweep_mob._sweep_tracker.set_value(x)


# -- D1-01: the lens sweep keeps ITS OWN colour / tracker, wherever it sits in `plots` ----

def test_lens_sweep_colour_when_sweep_is_not_the_last_plot():
    """plots: [arc, ceiling, sweep(accent), point(concept)] -- the lens cursor, band and dot
    must stay accent after an update, not turn into the LAST plot's concept colour."""
    by = _by_id(_spec([_ARC, _CEIL, _SWEEP, _POINT]))
    panel = by["inset"].mobject._inset_panel
    moving = _moving(panel)
    assert len(moving) == 3, f"expected band + rule + one dot, got {len(moving)}"
    _go_live(by["plot.2"].mobject, 0.9)
    panel.update()
    want = T.color("dark", "accent").upper()
    for m in moving:
        cols = _drawn_colours(m)
        assert cols == {want}, (type(m).__name__, cols, "want", want,
                                "concept is", T.color("dark", "concept"))


def test_lens_sweep_colour_matches_when_sweep_is_last():
    """Control: the order the live decks happen to use (sweep last) -- also accent."""
    by = _by_id(_spec([_ARC, _CEIL, _POINT, _SWEEP],
                      say="Look. {show inset} Closer. {show plot.2} B. {show plot.3} Sweep."))
    panel = by["inset"].mobject._inset_panel
    _go_live(by["plot.3"].mobject, 0.9)
    panel.update()
    want = T.color("dark", "accent").upper()
    for m in _moving(panel):
        assert _drawn_colours(m) == {want}, (type(m).__name__, _drawn_colours(m))


def test_two_lens_sweeps_each_ride_their_own_tracker():
    """Two sweeps: the first one's lens cursor must follow the FIRST main tracker (it used to
    call the last-defined x_of and ride the second sweep's tracker instead)."""
    a = {"kind": "sweep", "x_from": 1.0, "x_to": 0.9, "seconds": 2.0, "follow": [0],
         "color_role": "accent"}
    b = {"kind": "sweep", "x_from": 1.0, "x_to": 0.75, "seconds": 2.0, "follow": [0],
         "color_role": "concept"}
    by = _by_id(_spec([_ARC, _CEIL, a, b],
                      say="Look. {show inset} Closer. {show plot.2} A. {show plot.3} B."))
    panel = by["inset"].mobject._inset_panel
    lens = panel.submobjects[1]
    moving = _moving(panel)
    assert len(moving) == 4, f"expected rule + dot per sweep, got {len(moving)}"
    _go_live(by["plot.2"].mobject, 0.9)
    _go_live(by["plot.3"].mobject, 0.75)
    panel.update()
    rule_a, _, rule_b, _ = moving
    xa, xb = float(lens.c2p(0.9, 0.5)[0]), float(lens.c2p(0.75, 0.5)[0])
    assert abs(float(rule_a.get_center()[0]) - xa) < 1e-3, ("sweep A rule", rule_a.get_center(), xa)
    assert abs(float(rule_b.get_center()[0]) - xb) < 1e-3, ("sweep B rule", rule_b.get_center(), xb)
    assert _drawn_colours(rule_a) == {T.color("dark", "accent").upper()}, _drawn_colours(rule_a)
    assert _drawn_colours(rule_b) == {T.color("dark", "concept").upper()}, _drawn_colours(rule_b)


# -- D1-06: the lens draws a curve in the same meta.color_map colour as the main plot ------

def test_lens_curve_takes_the_color_map_default_role():
    """A plot with no colour of its own whose label names a colour-mapped token is drawn in
    that token's role on the main axes (SPEC rule 5) -- and must be in the lens too."""
    meta = dict(_META, color_map={"\\sin": "concept"})
    sine = {"kind": "function", "expression": "sin(x)", "label": "$y=\\sin x$", "reveal": True}
    spec = _spec([sine], inset={"x": [1.2, 1.9], "y": [0.8, 1.05], "corner": "top_right"},
                 say="Look. {show plot.0} curve. {show inset} closer.",
                 axes={"x_range": [0, 3.2, 0.5], "y_range": [-0.2, 1.2, 0.5]})
    by = _by_id(spec, meta)
    want = T.color("dark", "concept").upper()
    main_curve = by["plot.0"].mobject[1]                   # VGroup(glow, curve, label)
    assert main_curve.get_stroke_color().to_hex().upper() == want, main_curve.get_stroke_color()
    lens_curve = by["inset"].mobject._inset_panel[2][1]   # panel: border, lens, VGroup(glow, curve)
    assert _drawn_colours(lens_curve) == {want}, (_drawn_colours(lens_curve), "want", want)


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

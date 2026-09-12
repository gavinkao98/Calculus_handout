"""Self-test: graph `inset:` (the magnifier; SPEC-motion-language rule 3, kickoff T2-3).
Run from video/:
    python -m pipeline._selftest_inset

An inset is a SECOND set of axes over a data-coordinate rectangle of the main plot, drawn at
a fixed 3.2 x 2.0 u panel in one corner of the frame, holding the same plots clipped to that
rectangle. The main graph is neither scaled nor moved by it (it is outside the group
`_fit_graph_to_safe_zone` sees), and the built (un-rendered) state already has the panel
in its corner, so the layout gates measure the frame the film ends on.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # graph.py imports manim at module level -- bootstrap FIRST

from pipeline.templates import build_blocks
from pipeline.visuals import theme as T

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}

_AXES = {"x_range": [-0.3, 1.4, 0.5], "y_range": [-0.3, 1.4, 0.5],
         "x_length": 5.4, "y_length": 5.4}
_TH = 0.6
_BX, _BY = 0.8253, 0.5646          # (cos 0.6, sin 0.6)
_ARC = {"kind": "function", "expression": "sqrt(1 - x*x)", "x_range": [0, 1],
        "color_role": "result", "label": "$x^2+y^2=1$"}
_RADIUS = {"kind": "line", "start": [0, 0], "end": [_BX, _BY], "color_role": "concept"}
_HEIGHT = {"kind": "line", "start": [_BX, 0], "end": [_BX, _BY], "color_role": "practice",
           "dashed": True}
_B = {"kind": "point", "point": [_BX, _BY], "color_role": "concept", "label": "$B$",
      "reveal": True}
_SWEEP = {"kind": "sweep", "x_from": 1.0, "x_to": _BX, "seconds": 2.0, "follow": [0]}
_PLOTS = [_ARC, _RADIUS, _HEIGHT, _B, _SWEEP]
_INSET = {"x": [0.7, 1.05], "y": [0.35, 0.7], "corner": "top_right", "follow": True}


def _spec(plots=_PLOTS, inset=_INSET, **over):
    spec = {"id": "g", "kind": "content", "template": "graph", "mode": "single",
            "accent": "definition", "title": "A Graph",
            "say": "Look. {show plot.3} B. {show inset} Closer. {show plot.4} Sweep.",
            "axes": dict(_AXES), "plots": [dict(p) for p in plots]}
    if inset is not None:
        spec["inset"] = dict(inset)
    spec.update(over)
    return spec


def _blocks(**kw):
    return build_blocks(_spec(**kw), {"ground": "dark", "meta": _META})


def _b(blocks, bid):
    return next(x for x in blocks if x.id == bid)


def _bbox(mob):
    return (float(mob.get_left()[0]), float(mob.get_right()[0]),
            float(mob.get_bottom()[1]), float(mob.get_top()[1]))


def _raises(**kw):
    try:
        _blocks(**kw)
    except ValueError as exc:
        return str(exc)
    raise AssertionError("expected a ValueError from build")


# -- opt-in + block shape ------------------------------------------------------

def test_inset_is_opt_in():
    assert "inset" not in {b.id for b in _blocks(inset=None)}


def test_inset_block_shape():
    b = _b(_blocks(), "inset")
    assert b.static is False and b.anim == "fade" and b.layer == "graph"


# -- geometry ------------------------------------------------------------------

def test_panel_is_fixed_size_in_the_named_corner():
    from pipeline.templates import graph as G
    right, top = T.FRAME_W / 2 - T.SIDE_GUTTER, T.FRAME_H / 2 - T.SAFE_MARGIN
    panel = _b(_blocks(), "inset").mobject._inset_panel
    l, r, btm, tp = _bbox(panel)
    tol = 0.06                                   # stroke width of the white border
    assert abs((r - l) - G._INSET_W) < tol and abs((tp - btm) - G._INSET_H) < tol, _bbox(panel)
    assert abs(r - right) < tol and abs(tp - top) < tol, _bbox(panel)

    panel = _b(_blocks(inset={**_INSET, "corner": "bottom_left"}), "inset").mobject._inset_panel
    l, r, btm, tp = _bbox(panel)
    assert abs(l + right) < tol and abs(btm + top) < tol, _bbox(panel)


def test_main_graph_is_neither_scaled_nor_moved_by_the_inset():
    """The inset is outside the group _fit_graph_to_safe_zone sees: same spec with and
    without `inset:` must leave every main-graph block exactly where it was."""
    with_, without = _blocks(), _blocks(inset=None)
    for bid in ("axes", "plot.0", "plot.1", "plot.2", "plot.3", "plot.4"):
        a, b = _bbox(_b(with_, bid).mobject), _bbox(_b(without, bid).mobject)
        assert all(abs(x - y) < 1e-6 for x, y in zip(a, b)), (bid, a, b)


def test_frame_marks_the_region_on_the_main_axes():
    blocks = _blocks()
    axes = _b(blocks, "axes").mobject
    frame = _b(blocks, "inset").mobject._inset_frame
    l, r, btm, tp = _bbox(frame)
    p00, p11 = axes.c2p(0.7, 0.35), axes.c2p(1.05, 0.7)
    tol = 0.03
    assert abs(l - p00[0]) < tol and abs(btm - p00[1]) < tol, (l, btm, p00)
    assert abs(r - p11[0]) < tol and abs(tp - p11[1]) < tol, (r, tp, p11)


def test_lens_content_stays_inside_the_panel():
    """Every magnified piece is clipped to the data rectangle -- nothing leaks past the
    white border (the arc spans x in [0,1] on the main axes, the radius starts at the
    origin: both cross the rectangle's edges)."""
    panel = _b(_blocks(), "inset").mobject._inset_panel
    L, R, B, Tp = _bbox(panel)
    tol = 0.12                                   # dot radius / glow stroke
    for piece in panel.submobjects[1:]:          # [0] is the border itself
        if not piece.has_points():
            continue
        l, r, btm, tp = _bbox(piece)
        assert l >= L - tol and r <= R + tol and btm >= B - tol and tp <= Tp + tol, (piece, _bbox(piece))


def test_pieces_outside_the_rectangle_are_dropped():
    inside = _b(_blocks(), "inset").mobject._inset_panel
    far = {**_B, "point": [0.2, 0.2]}            # B moved out of the lens rectangle
    outside = _b(_blocks(plots=[_ARC, _RADIUS, _HEIGHT, far, _SWEEP]), "inset").mobject._inset_panel
    assert len(outside.submobjects) == len(inside.submobjects) - 1
    assert len(inside.submobjects) >= 2 + len(_PLOTS)   # border + lens axes + one per plot at least


# -- follow: the lens sweep rides the MAIN sweep's tracker ----------------------

def _moving_pieces(panel):
    return [m for m in panel.submobjects if m.get_updaters()]


def _visible(m) -> bool:
    """Does anything in *m*'s family draw? (An emptied always_redraw wrapper keeps a
    degenerate VectorizedPoint -- points but zero stroke and zero fill.)"""
    return any(len(s.points) and (s.get_fill_opacity() > 0
                                  or (s.get_stroke_width() > 0 and s.get_stroke_opacity() > 0))
               for s in m.get_family())


class _FakeScene:
    def __init__(self):
        self.added, self.played = [], []

    def add(self, *mobs):
        self.added.extend(mobs)

    def play(self, *anims, **kw):
        self.played.append((anims, kw))


def test_follow_reads_the_main_sweep_tracker():
    blocks = _blocks()
    sweep = _b(blocks, "plot.4")
    tracker = sweep.mobject._sweep_tracker
    panel = _b(blocks, "inset").mobject._inset_panel
    moving = _moving_pieces(panel)
    assert moving, "follow: true must leave always_redraw pieces in the lens"

    def snapshot():
        for m in moving:
            m.update(0)
        return [tuple(round(float(v), 4) for v in m.get_center()) if _visible(m) else None
                for m in moving]

    # before the MAIN sweep has played, the lens must not hold a cursor the main picture
    # lacks (the un-played block is not on screen; a follow: true lens revealed earlier
    # would otherwise show the cursor parked at x_to)
    assert all(p is None for p in snapshot()), "lens cursor drawn before the sweep played"
    sweep.anim(_FakeScene(), sweep.mobject, "dark")     # the sweep's own reveal flips it live
    tracker.set_value(0.9)
    at_09 = snapshot()
    assert any(p is not None for p in at_09), "lens cursor missing after the sweep played"
    tracker.set_value(0.75)
    at_075 = snapshot()
    assert at_09 != at_075, "lens cursor did not move with the main tracker"
    tracker.set_value(0.2)                      # outside the lens rectangle -> nothing drawn
    assert all(p is None for p in snapshot())
    tracker.set_value(_BX)                      # leave the tracker at its terminal value
    snapshot()
    # the lens pieces must stay ABOVE the panel's opaque ground after every redraw -- an
    # emptied wrapper re-populates into a fresh submobject that would otherwise sit at z 0
    from pipeline.templates import graph as G
    assert all(s.z_index == G._INSET_Z for m in moving for s in m.get_family()), \
        [(type(s).__name__, s.z_index) for m in moving for s in m.get_family()]


def test_follow_false_is_a_static_terminal_state():
    panel = _b(_blocks(inset={**_INSET, "follow": False}), "inset").mobject._inset_panel
    assert not _moving_pieces(panel)
    assert len(panel.submobjects) >= 2 + len(_PLOTS)


def test_sizecheck_sees_the_inset_in_its_corner_and_no_overflow():
    from pipeline.sizecheck import check_scenes
    issues = check_scenes(_META, [_spec()])
    assert not [m for s, m in issues if s == "error"], issues


# -- authoring mistakes are build errors (sizecheck turns them into gate errors) ---

def test_missing_x_or_y_raises():
    assert "inset.x" in _raises(inset={"y": [0, 1]})
    assert "inset.y" in _raises(inset={"x": [0, 1]})
    assert "inset.x" in _raises(inset={"x": [1, 1], "y": [0, 1]})


def test_bad_corner_raises():
    assert "corner" in _raises(inset={**_INSET, "corner": "middle"})


def test_inset_in_2up_mode_raises():
    spec = {"id": "g2", "kind": "content", "template": "graph", "mode": "2up",
            "accent": "definition", "title": "T", "say": "A. {show left.plot.0} B.",
            "left": {"axes": dict(_AXES), "plots": [dict(_ARC)]},
            "right": {"axes": dict(_AXES), "plots": [dict(_ARC)]},
            "inset": dict(_INSET)}
    try:
        build_blocks(spec, {"ground": "dark", "meta": _META})
    except ValueError as exc:
        assert "inset" in str(exc) and "single" in str(exc)
    else:
        raise AssertionError("2up + inset must not build silently")


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

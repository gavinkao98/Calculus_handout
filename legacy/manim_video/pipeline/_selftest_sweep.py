"""Self-test: graph `kind: sweep` (the cursor-scan primitive) + the dashed-function fix.
Run from video/:
    python -m pipeline._selftest_sweep

`sweep` is a plot like any other -- it takes the next `plot.N` id, so `{show plot.N}` and
sizecheck's target cross-check need no special case -- but its reveal is a callable that
runs a ValueTracker along the x axis, dragging a cursor, a dot on each followed curve and
(optionally) a shaded band between two of them.

The terminal state is the END of the sweep: sizecheck builds scenes without rendering, so a
tracker parked at its start value would hand the layout gates a frame the film never ends on.

Also pins the `dashed: true` fix: it used to apply to `kind: line` only and was silently
dropped for `kind: function`, so an authored dashed reference curve rendered solid.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # graph.py imports manim at module level -- bootstrap FIRST

from manim import DashedVMobject, VMobject

from pipeline.templates import build_blocks
from pipeline.templates import graph as G

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}

_AXES = {"x_range": [-1.85, 1.85, 0.5], "y_range": [0, 1.18, 0.5],
         "x_length": 6.4, "y_length": 3.6}
_COS = {"kind": "function", "expression": "cos(x)", "x_range": [-1.5708, 1.5708],
        "color_role": "muted", "label": r"$\cos\theta$", "reveal": True}
_ONE = {"kind": "line", "start": [-1.72, 1], "end": [1.72, 1], "color_role": "secondary",
        "reveal": True}
_RATIO = {"kind": "function", "expression": "sin(x)/x", "x_range": [-1.72, 1.72],
          "color_role": "accent", "reveal": True}


def _spec(plots, say="Look. {show plot.0} One."):
    return {"id": "g", "kind": "content", "template": "graph", "mode": "single",
            "accent": "definition", "title": "A Graph", "say": say,
            "axes": dict(_AXES), "plots": plots}


def _blocks(plots, **kw):
    return build_blocks(_spec(plots, **kw), {"ground": "dark", "meta": _META})


def _b(blocks, bid):
    return next(x for x in blocks if x.id == bid)


def _sweep(**over):
    s = {"kind": "sweep", "x_from": 1.7, "x_to": 0.0, "seconds": 3.0, "follow": [0, 1, 2],
         "leave": "cursor"}
    s.update(over)
    return s


# -- dashed function ---------------------------------------------------------

def _has_dashed(mob):
    if isinstance(mob, DashedVMobject):
        return True
    return any(_has_dashed(s) for s in getattr(mob, "submobjects", []))


def test_dashed_function_renders_dashed():
    plain = _b(_blocks([dict(_COS)]), "plot.0").mobject
    dashed = _b(_blocks([{**_COS, "dashed": True}]), "plot.0").mobject
    assert not _has_dashed(plain)
    assert _has_dashed(dashed), "`dashed: true` on a function must reach the curve"


def test_dashed_function_keeps_its_label_and_extent():
    plain = _b(_blocks([dict(_COS)]), "plot.0").mobject
    dashed = _b(_blocks([{**_COS, "dashed": True}]), "plot.0").mobject
    assert abs(plain.width - dashed.width) < 0.25 and abs(plain.height - dashed.height) < 0.25


def test_dashed_line_still_dashed():
    mob = _b(_blocks([{**_ONE, "dashed": True}]), "plot.0").mobject
    assert _has_dashed(mob) or "Dashed" in type(mob).__name__


# -- sweep: block shape ------------------------------------------------------

def test_sweep_takes_the_next_plot_id_and_is_dynamic():
    blocks = _blocks([_COS, _ONE, _RATIO, _sweep()])
    b = _b(blocks, "plot.3")
    assert b.static is False and callable(b.anim)
    assert b.layer == "graph"


def test_sweep_advertises_its_authored_seconds():
    b = _b(_blocks([_COS, _ONE, _RATIO, _sweep(seconds=2.5)]), "plot.3")
    assert b.anim_seconds == 2.5


def test_sweep_terminal_state_is_the_end_of_the_scan():
    """The built (un-rendered) geometry is what sizecheck measures, so it must be the frame
    the sweep ENDS on -- cursor at x_to, not x_from."""
    axes = None
    for b in _blocks([_COS, _ONE, _RATIO, _sweep()]):
        if b.id == "axes":
            axes = b.mobject
    b = _b(_blocks([_COS, _ONE, _RATIO, _sweep()]), "plot.3")
    # rebuild axes in the same scene to compare in screen space
    blocks = _blocks([_COS, _ONE, _RATIO, _sweep()])
    axes = _b(blocks, "axes").mobject
    sweep = _b(blocks, "plot.3").mobject
    x_to_screen = axes.c2p(0.0, 0.0)[0]
    x_from_screen = axes.c2p(1.7, 0.0)[0]
    assert abs(sweep.get_center()[0] - x_to_screen) < abs(sweep.get_center()[0] - x_from_screen)


def test_sweep_gap_band_is_built_when_asked():
    without = _b(_blocks([_COS, _ONE, _RATIO, _sweep()]), "plot.3").mobject
    with_gap = _b(_blocks([_COS, _ONE, _RATIO, _sweep(gap=[0, 1])]), "plot.3").mobject
    assert len(with_gap.submobjects) > len(without.submobjects)


def test_sweep_without_follow_is_just_a_cursor():
    b = _b(_blocks([_COS, _sweep(follow=[])]), "plot.1")
    assert callable(b.anim) and b.mobject.submobjects


# -- sweep: authoring mistakes are build errors ------------------------------

def _raises(plots):
    try:
        _blocks(plots)
    except ValueError as exc:
        return str(exc)
    raise AssertionError("expected a ValueError from build")


def test_follow_pointing_past_the_plot_list_raises():
    assert "9" in _raises([_COS, _sweep(follow=[9])])


def test_follow_pointing_at_a_non_curve_raises():
    dot = {"kind": "point", "point": [0, 1], "color_role": "accent"}
    assert "follow" in _raises([dot, _sweep(follow=[0])]).lower()


def test_gap_needs_two_curves():
    assert "gap" in _raises([_COS, _ONE, _sweep(gap=[0])]).lower()


def test_sweep_needs_its_endpoints():
    s = _sweep()
    del s["x_from"]
    assert "x_from" in _raises([_COS, s])


# -- the animation itself ----------------------------------------------------

class _FakeScene:
    def __init__(self):
        self.added, self.played = [], []

    def add(self, *mobs):
        self.added.extend(mobs)

    def play(self, *anims, **kw):
        self.played.append((anims, kw))


def test_sweep_callable_runs_for_its_authored_seconds_and_leaves_the_cursor():
    b = _b(_blocks([_COS, _ONE, _RATIO, _sweep(seconds=2.0)]), "plot.3")
    scene = _FakeScene()
    secs = b.anim(scene, b.mobject, "dark")
    assert secs == 2.0
    assert len(scene.played) == 1 and scene.played[0][1]["run_time"] == 2.0
    assert b.mobject in scene.added


def test_sweep_leave_none_fades_out_and_charges_for_it():
    b = _b(_blocks([_COS, _ONE, _RATIO, _sweep(seconds=2.0, leave="none")]), "plot.3")
    scene = _FakeScene()
    secs = b.anim(scene, b.mobject, "dark")
    assert len(scene.played) == 2 and secs > 2.0


def test_sweep_is_not_a_kind_other_templates_choke_on():
    """`sweep` must survive the same _plot_blocks used by the 2-up compare mode."""
    spec = {"id": "g2", "kind": "content", "template": "graph", "mode": "2up",
            "accent": "definition", "title": "T", "say": "A. {show left.plot.0} B.",
            "left": {"axes": dict(_AXES), "plots": [_COS, _sweep(follow=[0])]},
            "right": {"axes": dict(_AXES), "plots": [dict(_COS)]}}
    ids = {b.id for b in build_blocks(spec, {"ground": "dark", "meta": _META})}
    assert "left.plot.1" in ids


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

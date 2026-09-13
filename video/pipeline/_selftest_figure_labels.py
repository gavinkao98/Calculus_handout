"""Self-test: no label in a figure scene is crossed by a line.
Run from video/:
    python -m pipeline._selftest_figure_labels

Why this exists. A label with an axis, a curve or a tangent running straight through its
glyphs is unreadable, and NOTHING in the pipeline could see it: `sizecheck` compares BLOCK
bounding boxes, so a label that lives inside the same block as the curve crossing it (a
plot and its own label, a tangent segment and its `m=` tag) is invisible to it, and the
font-floor gate only measures type size. The 2026-09-13 visual audit found four such
labels in `slope_equals_height` by eye, after five gates and 33 self-tests had passed it.

So this test measures the thing directly: for every Tex in the scene, take its bounding
box; for every Line / DashedLine / Arrow / ParametricFunction, take its path, densified
(bezier control points alone step over a small box); assert no path point lands inside a
box, and that no two label boxes overlap.

Scope. Only scenes whose layout is FINAL at build time -- what `build_blocks` returns is
what the viewer sees. `sector_inequality` and `continuity_statement_sin_limit` are built
in one place and animated to another (zoom out, dock, peel), so a static box test reports
their transit positions, not their frames; they are checked by frame audit instead.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # the hook module imports manim at module level -- bootstrap FIRST

from pathlib import Path

import numpy as np
import yaml
from manim import Arrow, DashedLine, Line, MathTex, ParametricFunction, SingleStringMathTex, Tex

from pipeline.templates import build_blocks

DECK = Path(__file__).resolve().parents[1] / "storyboards" / "ch03_trig_derivatives.yml"
# Scenes whose built layout IS their final layout (see "Scope" above).
STATIC_FIGURE_SCENES = ("squeeze_graph", "slope_equals_height", "shm_stacked_graphs")
SAMPLES_PER_SEGMENT = 12


def _deck():
    doc = yaml.safe_load(DECK.read_text(encoding="utf-8"))
    return doc["meta"], {s["id"]: s for s in doc["scenes"]}


def _walk(mob, path):
    yield mob, path
    for i, sub in enumerate(getattr(mob, "submobjects", []) or []):
        yield from _walk(sub, f"{path}[{i}]")


def _outermost(items):
    """Drop nested hits: a Tex's glyphs are Tex, a DashedLine's dashes are Lines."""
    paths = {p for p, _ in items}
    return [(p, m) for p, m in items if not any(p != q and p.startswith(q + "[") for q in paths)]


def _labels_and_strokes(scene_id):
    meta, by_id = _deck()
    blocks = build_blocks(by_id[scene_id],
                          {"ground": "dark", "meta": meta, "scenes_by_id": by_id})
    labels, strokes = [], []
    for b in blocks:
        for m, path in _walk(b.mobject, b.id):
            if isinstance(m, (Tex, MathTex, SingleStringMathTex)):
                if m.get_num_points() or m.submobjects:
                    labels.append((path, m))
            elif isinstance(m, (Line, DashedLine, Arrow, ParametricFunction)):
                strokes.append((path, m))
    return _outermost(labels), _outermost(strokes)


def _box(mob):
    return (mob.get_left()[0], mob.get_right()[0], mob.get_bottom()[1], mob.get_top()[1])


def _points(mob):
    p = mob.points
    if len(p) < 2:
        return p
    t = np.linspace(0.0, 1.0, SAMPLES_PER_SEGMENT)[:, None]
    return np.vstack([p] + [a + t * (b - a) for a, b in zip(p[:-1], p[1:])])


def _crossings(scene_id):
    labels, strokes = _labels_and_strokes(scene_id)
    assert labels, f"{scene_id}: no labels found -- the test is measuring nothing"
    out = []
    for lp, lm in labels:
        x0, x1, y0, y1 = _box(lm)
        for sp, sm in strokes:
            pts = _points(sm)
            if len(pts) == 0:
                continue
            inside = ((pts[:, 0] >= x0) & (pts[:, 0] <= x1)
                      & (pts[:, 1] >= y0) & (pts[:, 1] <= y1))
            if inside.any():
                out.append(f"{scene_id}: line {sp} runs through label {lp}")
    return out


def _overlaps(scene_id):
    labels, _ = _labels_and_strokes(scene_id)
    out = []
    for i, (ap, am) in enumerate(labels):
        ax0, ax1, ay0, ay1 = _box(am)
        for bp, bm in labels[i + 1:]:
            bx0, bx1, by0, by1 = _box(bm)
            if ax0 < bx1 and bx0 < ax1 and ay0 < by1 and by0 < ay1:
                out.append(f"{scene_id}: labels {ap} and {bp} overlap")
    return out


def test_no_line_runs_through_a_label():
    bad = [m for s in STATIC_FIGURE_SCENES for m in _crossings(s)]
    assert not bad, "\n".join(bad)


def test_no_two_labels_overlap():
    bad = [m for s in STATIC_FIGURE_SCENES for m in _overlaps(s)]
    assert not bad, "\n".join(bad)


def test_the_measurement_can_actually_fail():
    """Move one label onto the x-axis and the crossing test must see it -- otherwise a
    green run proves nothing (the 2026-09-13 lesson: five gates passed a 10 px label)."""
    labels, strokes = _labels_and_strokes("slope_equals_height")
    axis = next(m for p, m in strokes if p.startswith("axes["))
    victim = next(m for p, m in labels if p.startswith("tan_"))
    victim.move_to(axis.get_center())
    x0, x1, y0, y1 = _box(victim)
    pts = _points(axis)
    hit = ((pts[:, 0] >= x0) & (pts[:, 0] <= x1) & (pts[:, 1] >= y0) & (pts[:, 1] <= y1))
    assert hit.any(), "the crossing measurement does not detect a label sitting on an axis"


if __name__ == "__main__":
    test_no_line_runs_through_a_label()
    test_no_two_labels_overlap()
    test_the_measurement_can_actually_fail()
    print("OK figure-label self-test")

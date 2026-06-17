"""§1.1 Inverse Functions -- custom hook animations (5 cues from the LOCKED
content script / storyboard `# HOOK(第二輪)` markers).

Each factory follows the hook contract (pipeline/templates/__init__._apply_hook):
it receives the TEMPLATE's blocks and returns the final list. It replaces the
mobject of an existing reveal id (so the storyboard's {show ...} markers and the
approved narration stay untouched) and/or attaches a CALLABLE anim that
choreographs the bespoke manim inside that beat (pipeline/blocks.py:play_block
just reports the seconds spent, preserving the audio-driven alignment).

Deleting a scene's `hook:` line restores the stock template scene -- the
template payload in the storyboard is kept as the no-hook fallback.

Per CONTENT_METHODOLOGY §5, this generated code is treated like narration:
the user reviews the rendered result before it is final.

The five hooks (scene id -> cue):
  can_we_run_it_backwards      two-in / one-out mapping (x clean, x^2 collides)
  horizontal_line_test         a horizontal line sweeps each panel down
  composition_identities       x rides f to B and f^{-1} back to A (round trip)
  reflection_across_y_equals_x fold x^3 over y=x; it lands on the cube root
  repair_by_restricting        drop the left arm of x^2, reflect the right -> sqrt
"""
from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    ArcBetweenPoints,
    Create,
    DashedLine,
    Dot,
    Ellipse,
    FadeIn,
    Flash,
    GrowArrow,
    GrowFromCenter,
    Indicate,
    MathTex,
    MoveAlongPath,
    ReplacementTransform,
    VGroup,
    smooth,
)

from pipeline import brand
from pipeline.blocks import Block
from pipeline.visuals import theme as T

UP = np.array([0.0, 1.0, 0.0])
DOWN = np.array([0.0, -1.0, 0.0])
RIGHT = np.array([1.0, 0.0, 0.0])
LEFT = np.array([-1.0, 0.0, 0.0])


# ---------------------------------------------------------------- helpers


def _by_id(blocks: list[Block]) -> dict[str, Block]:
    return {b.id: b for b in blocks}


def _centre_in_zone(title_mob, group: VGroup, *, bottom_pad: float = 0.45) -> None:
    """Centre *group* vertically in the zone between the title and the bottom
    safe margin (the definition_math balance rule, reused by hooks that rebuild
    a scene's visual body)."""
    zone_top = title_mob.get_bottom()[1] - 0.55
    zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN + bottom_pad
    group.move_to([0, (zone_top + zone_bottom) / 2, 0])


def _mirror_xy(centre):
    """Reflection across y=x in axes screen space: swap the (x,y) offset from the
    axes origin. Used by the fold/reflect hooks -- this is the exact geometric
    operation an inverse performs on a graph.

    NOTE: a raw screen-space coordinate swap equals a true reflection across the
    *data* line y=x only when the axes are ISOTROPIC (equal screen-units per
    data-unit on both axes). Both §1.1 reflection scenes satisfy this -- scene 11
    x/y_range [-2.2,2.2] @ length 5.6, scene 12 span 3.1 @ length 5.4 -- so the
    swap is exact here. If a future scene uses anisotropic axes, reflect in DATA
    space instead (axes.p2c -> swap -> axes.c2p)."""
    def f(p):
        v = p - centre
        return centre + np.array([v[1], v[0], 0.0])
    return f


# ================================================================ hook 1
# can_we_run_it_backwards -- 左 f(x)=x 各輸入各入各位;右 x^2 兩箭頭匯聚 1/4,
# 匯聚瞬間 Indicate 一下強調(「兩進一出——回不去」)。


def _mapping_column(ground, ins, outs, pairs, caption, arrow_role):
    """A small input->output mapping diagram: value labels in two columns and
    one arrow per (in, out) pair. Returns (group, arrows, out_mobs, in_mobs,
    caption_mob) -- pieces the callable animates individually."""
    in_x, out_x = -1.35, 1.35
    rows_in = [0.7 - 0.7 * i for i in range(len(ins))] if len(ins) > 1 else [0.0]
    rows_out = [0.7 - 0.7 * i for i in range(len(outs))] if len(outs) > 1 else [0.0]

    in_mobs = [MathTex(s, color=T.color(ground, "text"), font_size=T.fs("math_sm")) for s in ins]
    out_mobs = [MathTex(s, color=T.color(ground, "text"), font_size=T.fs("math_sm")) for s in outs]
    for m, y in zip(in_mobs, rows_in):
        m.move_to([in_x, y, 0])
    for m, y in zip(out_mobs, rows_out):
        m.move_to([out_x, y, 0])

    col = T.color(ground, arrow_role)
    arrows = []
    for i, j in pairs:
        a = Arrow(in_mobs[i].get_right(), out_mobs[j].get_left(), buff=0.18,
                  stroke_width=3.0, color=col, max_tip_length_to_length_ratio=0.12)
        arrows.append(a)

    cap = brand.math_line(caption, ground, role="text", size="math_sm")
    body = VGroup(*in_mobs, *out_mobs, *arrows)
    cap.next_to(body, UP, buff=0.42)
    group = VGroup(cap, *in_mobs, *out_mobs, *arrows)
    return group, arrows, out_mobs, in_mobs, cap


def can_we_run_it_backwards(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    title = ids["title"].mobject
    statement = ids["statement"].mobject

    left_grp, left_arrows, left_outs, left_ins, left_cap = _mapping_column(
        ground, ins=["0", r"\tfrac12", r"\tfrac18"], outs=["0", r"\tfrac12", r"\tfrac18"],
        pairs=[(0, 0), (1, 1), (2, 2)], caption=r"$f(x)=x$ on $[0,1]$", arrow_role="secondary")
    right_grp, right_arrows, right_outs, right_ins, right_cap = _mapping_column(
        ground, ins=[r"\tfrac12", r"-\tfrac12"], outs=[r"\tfrac14"],
        pairs=[(0, 0), (1, 0)], caption=r"$g(x)=x^2$ on $[-1,1]$", arrow_role="accent")
    left_grp.move_to([-3.1, 0, 0])
    right_grp.move_to([3.1, 0, 0])
    right_grp.align_to(left_grp, UP)
    diagrams = VGroup(left_grp, right_grp)

    layout = VGroup(statement, diagrams).arrange(DOWN, buff=0.8)
    _centre_in_zone(title, layout)

    def play_left(scene, mob, g):
        scene.play(FadeIn(left_cap, shift=0.1 * UP), *[FadeIn(m) for m in left_ins], run_time=0.5)
        spent = 0.5
        for a, o in zip(left_arrows, left_outs):
            scene.play(GrowArrow(a), FadeIn(o), run_time=0.4)
            spent += 0.4
        scene.add(mob)
        return spent

    def play_right(scene, mob, g):
        scene.play(FadeIn(right_cap, shift=0.1 * UP), *[FadeIn(m) for m in right_ins], run_time=0.5)
        scene.play(GrowArrow(right_arrows[0]), FadeIn(right_outs[0]), run_time=0.45)
        scene.play(GrowArrow(right_arrows[1]), run_time=0.45)
        # the convergence pause: one output, two claimants
        scene.play(Indicate(right_outs[0], color=T.color(g, "warning"), scale_factor=1.25), run_time=0.6)
        scene.add(mob)
        return 2.0

    ids["math.0"].mobject = left_grp
    ids["math.0"].anim = play_left
    ids["math.1"].mobject = right_grp
    ids["math.1"].anim = play_right
    return blocks


# ================================================================ hook 2
# horizontal_line_test -- graph_compare 模板已給兩格曲線;水平虛線自上而下滑入
# 各格,左 y=x 交一點(綠 Flash「一次」),右拋物線交兩點(紅 Flash「兩次」)。


def _slide_line_down(scene, mob, g, *, drop=1.7, rt=0.85):
    """Reveal a horizontal guide line by sweeping it down into place (a
    horizontal line scanning the graph), instead of a flat fade."""
    final = mob.get_center().copy()
    mob.shift(UP * drop)
    scene.add(mob)
    scene.play(mob.animate.move_to(final), run_time=rt, rate_func=smooth)
    return rt


def _pop_crossing(role):
    def _f(scene, mob, g):
        scene.play(GrowFromCenter(mob), run_time=0.35)
        scene.play(Flash(mob.get_center(), color=T.color(g, role), line_length=0.18,
                         num_lines=12, flash_radius=0.34), run_time=0.5)
        scene.add(mob)
        return 0.85
    return _f


def horizontal_line_test(spec, ctx, blocks):
    ids = _by_id(blocks)
    # left panel: dashed guide (plot.1) sweeps down, one crossing (plot.2) -> green
    ids["left.plot.1"].anim = _slide_line_down
    ids["left.plot.2"].anim = _pop_crossing("success")
    # right panel: dashed guide (plot.1) sweeps down, two crossings -> warning
    ids["right.plot.1"].anim = _slide_line_down
    ids["right.plot.2"].anim = _pop_crossing("warning")
    ids["right.plot.3"].anim = _pop_crossing("warning")
    return blocks


# ================================================================ hook 3
# composition_identities -- 點 x 沿上弧(f)到 B 的 f(x),沿下弧(f⁻¹)回原點 Flash;
# 第二趟由 B 的 y 反向走一輪。


def composition_identities(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    title = ids["title"].mobject
    statement = ids["statement"].mobject

    text_col = T.color(ground, "text")
    cyan = T.color(ground, "secondary")
    gold = T.color(ground, "accent")

    ellA = Ellipse(width=2.1, height=2.4, color=text_col, stroke_width=2.0)
    ellB = ellA.copy()
    ellA.move_to([-2.7, 0, 0])
    ellB.move_to([2.7, 0, 0])
    labA = MathTex("A", color=text_col, font_size=T.fs("math_sm"))
    labB = MathTex("B", color=text_col, font_size=T.fs("math_sm"))
    labA.next_to(ellA, UP, buff=0.14)
    labB.next_to(ellB, UP, buff=0.14)

    px = Dot([-2.7, 0.0, 0.0], radius=0.075, color=cyan)
    py = Dot([2.7, 0.0, 0.0], radius=0.075, color=gold)
    labx = MathTex("x", color=text_col, font_size=T.fs("math_sm"))
    laby = MathTex("f(x)", color=text_col, font_size=T.fs("math_sm"))
    labx.next_to(px, LEFT, buff=0.15)
    laby.next_to(py, RIGHT, buff=0.15)

    arc_f = ArcBetweenPoints(px.get_center() + np.array([0.12, 0.12, 0]),
                             py.get_center() + np.array([-0.12, 0.12, 0]),
                             angle=-0.9, color=cyan, stroke_width=3.0)
    arc_b = ArcBetweenPoints(py.get_center() + np.array([-0.12, -0.12, 0]),
                             px.get_center() + np.array([0.12, -0.12, 0]),
                             angle=-0.9, color=gold, stroke_width=3.0)
    lab_f = MathTex("f", color=cyan, font_size=T.fs("math_sm"))
    lab_b = MathTex("f^{-1}", color=gold, font_size=T.fs("math_sm"))
    lab_f.next_to(arc_f, UP, buff=0.12)
    lab_b.next_to(arc_b, DOWN, buff=0.12)

    diagram = VGroup(ellA, ellB, labA, labB, arc_f, arc_b, lab_f, lab_b, px, py, labx, laby)

    eq0 = ids["math.0"].mobject.scale(0.85)
    eq1 = ids["math.1"].mobject.scale(0.85)
    eqs = VGroup(eq0, eq1).arrange(RIGHT, buff=0.9)

    layout = VGroup(statement, diagram, eqs).arrange(DOWN, buff=0.45)
    _centre_in_zone(title, layout, bottom_pad=0.1)

    def round_trip(scene, g, *, start_dot, fwd_arc, back_arc, flash_col):
        tracer = start_dot.copy().set_z_index(3)
        scene.add(tracer)
        scene.play(MoveAlongPath(tracer, fwd_arc), run_time=1.0)
        scene.play(MoveAlongPath(tracer, back_arc), run_time=1.0)
        scene.play(Flash(start_dot.get_center(), color=flash_col, line_length=0.22,
                         num_lines=12, flash_radius=0.45), run_time=0.55)
        scene.remove(tracer)
        return 2.55

    def play_first(scene, mob, g):
        scene.play(Create(ellA), Create(ellB), FadeIn(labA), FadeIn(labB), run_time=0.7)
        scene.play(FadeIn(px), FadeIn(py), FadeIn(labx), FadeIn(laby),
                   Create(arc_f), Create(arc_b), FadeIn(lab_f), FadeIn(lab_b), run_time=0.8)
        spent = 1.5
        spent += round_trip(scene, g, start_dot=px, fwd_arc=arc_f, back_arc=arc_b,
                            flash_col=T.color(g, "secondary"))
        scene.play(FadeIn(eq0, shift=0.1 * UP), run_time=0.5)
        scene.add(diagram, eq0)
        return spent + 0.5

    def ensure_diagram(scene, mob, g):
        scene.add(mob)
        return 0.0

    def play_second(scene, mob, g):
        # second identity f(f^{-1}(y)) = y: start at y in B, ride f^{-1} (arc_b: B->A),
        # then f back (arc_f: A->B).
        spent = round_trip(scene, g, start_dot=py, fwd_arc=arc_b, back_arc=arc_f,
                           flash_col=T.color(g, "accent"))
        scene.play(FadeIn(eq1, shift=0.1 * UP), run_time=0.5)
        scene.add(eq1)
        return spent + 0.5

    # math.0 carries ONLY eq0 as its measurable mobject (the diagram rides in a
    # separate graph-layer block) -- bundling diagram+eq0 made one huge bbox that
    # falsely "overlapped" eq1 beside it.
    ids["math.0"].mobject = eq0
    ids["math.0"].anim = play_first
    ids["math.1"].mobject = eq1
    ids["math.1"].anim = play_second
    out = list(blocks)
    out.insert(out.index(ids["math.0"]),
               Block("hookdiagram", diagram, anim=ensure_diagram, static=False, layer="graph"))
    return out


# ================================================================ hook 4
# reflection_across_y_equals_x -- 反射揭示:plot.2(∛x)由 x^3 沿 y=x 翻摺生成;
# plot.3/plot.4 鏡射點對 Flash;收在兩曲線＋鏡線並存。
# template plot 順序(storyboard): 0 y=x line, 1 x^3, 2 cbrt(reveal), 3 (a,b),
# 4 (b,a).


def reflection_across_y_equals_x(spec, ctx, blocks):
    ids = _by_id(blocks)
    axes = ids["axes"].mobject
    centre = axes.c2p(0, 0)

    x3_mob = ids["plot.1"].mobject   # VGroup(glow, graph) -- the x^3 curve
    x3_curve = x3_mob[1]
    cbrt_blk = ids["plot.2"]

    def play_fold(scene, mob, g):
        # mob == cbrt block's VGroup(glow, graph, label). Fold a ghost of x^3 over
        # y=x; it lands on the cube root, then bring in cbrt's own (brighter) curve.
        ghost = x3_curve.copy().set_stroke(opacity=0.9)
        scene.add(ghost)
        target = x3_curve.copy().apply_function(_mirror_xy(centre))
        scene.play(ReplacementTransform(ghost, target), run_time=1.5)
        scene.play(FadeIn(mob), run_time=0.4)
        scene.remove(target)
        scene.add(mob)
        return 1.9

    def play_point(scene, mob, g):
        scene.play(GrowFromCenter(mob), run_time=0.35)
        scene.play(Flash(mob.get_center(), color=T.color(g, "text"), line_length=0.16,
                         num_lines=10, flash_radius=0.3), run_time=0.45)
        scene.add(mob)
        return 0.8

    cbrt_blk.anim = play_fold
    ids["plot.3"].anim = play_point
    ids["plot.4"].anim = play_point
    return blocks


# ================================================================ hook 5
# repair_by_restricting -- 先閃現整條拋物線、左臂(x<0)淡出丟棄,留右臂;plot.2(√x)
# 由保留的右臂沿 y=x 鏡射生成。
# template plot 順序: 0 y=x line, 1 f(x)=x^2 (right arm, static), 2 sqrt(reveal).


def repair_by_restricting(spec, ctx, blocks):
    ids = _by_id(blocks)
    axes = ids["axes"].mobject
    centre = axes.c2p(0, 0)

    x2_mob = ids["plot.1"].mobject       # VGroup(glow, graph) -- the right arm x>=0
    x2_curve = x2_mob[1]

    # The scene's axes show the nonnegative domain only (x_range starts at -0.4),
    # so a full "discard the left arm" gesture would draw almost entirely
    # off-frame -- the narration carries the restriction. The effective visual is
    # the inversion itself: reflect the kept right arm across y=x to get sqrt.
    def play_reflect(scene, mob, g):
        # reflect the kept (restricted) right arm across y=x -> the square root
        # (mob == sqrt block's VGroup(glow, graph, label)).
        ghost = x2_curve.copy().set_stroke(opacity=0.9)
        scene.add(ghost)
        target = x2_curve.copy().apply_function(_mirror_xy(centre))
        scene.play(ReplacementTransform(ghost, target), run_time=1.5)
        scene.play(FadeIn(mob), run_time=0.4)
        scene.remove(target)
        scene.add(mob)
        return 1.9

    ids["plot.2"].anim = play_reflect
    return blocks

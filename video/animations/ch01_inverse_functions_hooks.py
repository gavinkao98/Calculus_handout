"""§1.1 Inverse Functions -- custom hook animations (4 cues from 內容稿 v2).

Each factory follows the hook contract (pipeline/templates/__init__._apply_hook):
it receives the TEMPLATE's blocks and returns the final list. It replaces the
mobject of an existing reveal id (so the storyboard's {show ...} markers and the
approved narration stay untouched) and attaches a CALLABLE anim that
choreographs the bespoke manim inside that beat (pipeline/blocks.py:play_block
just reports the seconds spent, preserving the audio-driven alignment).

Deleting a scene's `hook:` line restores the stock template scene -- the
template payload in the storyboard is kept as the no-hook fallback.

Per CONTENT_METHODOLOGY §5, this generated code is treated like narration:
the user reviews the rendered result before it is final.
"""
from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    ArcBetweenPoints,
    Axes,
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
    ValueTracker,
    VGroup,
    always_redraw,
)

from pipeline import brand
from pipeline.blocks import Block
from pipeline.visuals import theme as T

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


# ================================================================ hook 1
# can_we_go_backwards -- 左 f(x)=x 各輸入箭頭各入各位;右 x² 兩箭頭匯聚 1/4,
# 匯聚瞬間頓一下強調(「兩進一出——回不去」)。


def _mapping_column(ground, ins: list[str], outs: list[str], pairs: list[tuple[int, int]],
                    caption: str, arrow_role: str):
    """A small input->output mapping diagram: value labels in two columns and
    one arrow per (in, out) pair. Returns (group, arrows, out_labels, in_labels,
    caption_mob) -- pieces the callable animates individually."""
    in_x, out_x = -1.45, 1.45
    rows_in = [0.7 - 0.7 * i for i in range(len(ins))] if len(ins) > 1 else [0.0]
    rows_out = [0.7 - 0.7 * i for i in range(len(outs))] if len(outs) > 1 else [0.0]

    in_mobs = [MathTex(s, color=T.color(ground, "text"), font_size=T.fs("math_sm"))
               for s in ins]
    out_mobs = [MathTex(s, color=T.color(ground, "text"), font_size=T.fs("math_sm"))
                for s in outs]
    for m, y in zip(in_mobs, rows_in):
        m.move_to([in_x, y, 0])
    for m, y in zip(out_mobs, rows_out):
        m.move_to([out_x, y, 0])

    col = T.color(ground, arrow_role)
    arrows = []
    for i, j in pairs:
        a = Arrow(in_mobs[i].get_right(), out_mobs[j].get_left(),
                  buff=0.18, stroke_width=3.0, color=col,
                  max_tip_length_to_length_ratio=0.12)
        arrows.append(a)

    cap = brand.math_line(caption, ground, role="text", size="math_sm")
    body = VGroup(*in_mobs, *out_mobs, *arrows)
    cap.next_to(body, np.array([0.0, 1.0, 0.0]), buff=0.42)
    group = VGroup(cap, *in_mobs, *out_mobs, *arrows)
    return group, arrows, out_mobs, in_mobs, cap


def can_we_go_backwards(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    title = ids["title"].mobject
    statement = ids["statement"].mobject

    left_grp, left_arrows, left_outs, left_ins, left_cap = _mapping_column(
        ground,
        ins=["0", r"\tfrac12", r"\tfrac18"],
        outs=["0", r"\tfrac12", r"\tfrac18"],
        pairs=[(0, 0), (1, 1), (2, 2)],
        caption=r"$f(x)=x$ on $[0,1]$",
        arrow_role="secondary",
    )
    right_grp, right_arrows, right_outs, right_ins, right_cap = _mapping_column(
        ground,
        ins=[r"\tfrac12", r"-\tfrac12"],
        outs=[r"\tfrac14"],
        pairs=[(0, 0), (1, 0)],
        caption=r"$f(x)=x^2$ on $[-1,1]$",
        arrow_role="accent",
    )
    left_grp.move_to([-3.0, 0, 0])
    right_grp.move_to([3.0, 0, 0])
    # top-align the two captions: centre-alignment let the shorter right group
    # ride low beside the taller left one (seen in the first hooked frame)
    right_grp.align_to(left_grp, np.array([0.0, 1.0, 0.0]))
    diagrams = VGroup(left_grp, right_grp)

    layout = VGroup(statement, diagrams).arrange(np.array([0.0, -1.0, 0.0]), buff=0.85)
    _centre_in_zone(title, layout)

    def play_left(scene, mob, g):
        scene.play(FadeIn(left_cap, shift=0.1 * np.array([0.0, 1.0, 0.0])),
                   *[FadeIn(m) for m in left_ins], run_time=0.5)
        spent = 0.5
        for a, o in zip(left_arrows, left_outs):
            scene.play(GrowArrow(a), FadeIn(o), run_time=0.4)
            spent += 0.4
        scene.add(mob)
        return spent

    def play_right(scene, mob, g):
        scene.play(FadeIn(right_cap, shift=0.1 * np.array([0.0, 1.0, 0.0])),
                   *[FadeIn(m) for m in right_ins], run_time=0.5)
        scene.play(GrowArrow(right_arrows[0]), FadeIn(right_outs[0]), run_time=0.45)
        scene.play(GrowArrow(right_arrows[1]), run_time=0.45)
        # the convergence pause: one output, two claimants
        scene.play(Indicate(right_outs[0], color=T.color(g, "warning"),
                            scale_factor=1.25), run_time=0.6)
        scene.add(mob)
        return 2.0

    ids["math.0"].mobject = left_grp
    ids["math.0"].anim = play_left
    ids["math.1"].mobject = right_grp
    ids["math.1"].anim = play_right
    return blocks


# ================================================================ hook 2
# horizontal_line_test -- 兩圖並排(單調 x³ vs x²),同一條水平線同步下掃;
# 左圖恆一交點(綠),右圖兩交點(紅)停住、拉虛線回 x 軸。


def _small_axes(x_range, y_range, ground):
    ax = Axes(
        x_range=x_range, y_range=y_range,
        x_length=4.3, y_length=3.3, tips=False,
        axis_config={"color": T.color(ground, "text"), "stroke_width": 2.0,
                     "include_ticks": False, "include_numbers": False},
    )
    ax.x_axis.add_tip(tip_length=0.14, tip_width=0.14)
    ax.y_axis.add_tip(tip_length=0.14, tip_width=0.14)
    return ax


def horizontal_line_test(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    title = ids["title"].mobject

    # drop the template's single-graph payload (kept in the storyboard only as
    # the no-hook fallback); keep title / annotation / motif
    keep = [b for b in blocks
            if not (b.id == "axes" or b.id == "ticks"
                    or b.id.startswith("plot.") or b.id.startswith("label."))]

    axL = _small_axes([-1.45, 1.45, 0.5], [-1.95, 1.95, 0.5], ground)
    axR = _small_axes([-1.55, 1.55, 0.5], [-0.35, 2.05, 0.5], ground)

    colL = T.color(ground, "secondary")
    colR = T.color(ground, "secondary")
    curveL = axL.plot(lambda x: x ** 3, x_range=[-1.22, 1.22, 0.005],
                      color=colL, stroke_width=3.2)
    curveR = axR.plot(lambda x: x ** 2, x_range=[-1.4, 1.4, 0.005],
                      color=colR, stroke_width=3.2)
    labL = brand.math_line("y=x^3", ground, role="text", size="math_sm")
    labL.move_to(axL.c2p(-1.05, 1.45))
    labR = brand.math_line("y=x^2", ground, role="text", size="math_sm")
    labR.move_to(axR.c2p(-0.85, 1.78))   # clear of the y-axis (centred on it before)

    grpL = VGroup(axL, curveL, labL)
    grpR = VGroup(axR, curveR, labR)
    panels = VGroup(grpL, grpR).arrange(np.array([1.0, 0.0, 0.0]), buff=1.5)
    annotation_mob = ids.get("annotation.0").mobject if "annotation.0" in ids else None
    # centre panels in the band between title and annotation
    zone_top = title.get_bottom()[1] - 0.45
    zone_bottom = (annotation_mob.get_top()[1] + 0.35) if annotation_mob is not None \
        else (-T.FRAME_H / 2 + T.SAFE_MARGIN + 0.75)
    panels.move_to([0, (zone_top + zone_bottom) / 2, 0])

    for i, panel in enumerate(panels):
        keep.insert(2 + i, Block(f"hookpanel.{i}", panel, anim="create",
                                 static=True, layer="graph"))

    C = 0.64  # the stopping height on the right graph: x = ±0.8

    def play_sweep(scene, mob, g):
        green = T.color(g, "success")
        red = T.color(g, "warning")
        tr = ValueTracker(0.0)
        yL = lambda: 1.55 - 1.05 * tr.get_value()          # 1.55 -> 0.50
        yR = lambda: 1.85 - (1.85 - C) * tr.get_value()    # 1.85 -> 0.64

        lineL = always_redraw(lambda: DashedLine(
            axL.c2p(-1.4, yL()), axL.c2p(1.4, yL()),
            color=red, stroke_width=2.4, dash_length=0.12))
        lineR = always_redraw(lambda: DashedLine(
            axR.c2p(-1.5, yR()), axR.c2p(1.5, yR()),
            color=red, stroke_width=2.4, dash_length=0.12))
        dotL = always_redraw(lambda: Dot(
            axL.c2p(np.cbrt(yL()), yL()), radius=0.07, color=green))
        dotR1 = always_redraw(lambda: Dot(
            axR.c2p(-np.sqrt(max(yR(), 0.0)), yR()), radius=0.07,
            color=T.color(g, "accent")))
        dotR2 = always_redraw(lambda: Dot(
            axR.c2p(np.sqrt(max(yR(), 0.0)), yR()), radius=0.07,
            color=T.color(g, "accent")))

        scene.add(lineL, lineR, dotL, dotR1, dotR2)
        scene.play(tr.animate.set_value(1.0), run_time=3.2,
                   rate_func=lambda t: t)
        for m in (lineL, lineR, dotL, dotR1, dotR2):
            m.clear_updaters()

        # the verdict: left always one crossing (green nod), right two (red)
        scene.play(Indicate(dotL, color=green, scale_factor=1.4), run_time=0.55)
        scene.play(Flash(dotR1.get_center(), color=red, line_length=0.2,
                         num_lines=12, flash_radius=0.4),
                   Flash(dotR2.get_center(), color=red, line_length=0.2,
                         num_lines=12, flash_radius=0.4), run_time=0.6)
        drop1 = DashedLine(axR.c2p(-0.8, C), axR.c2p(-0.8, 0),
                           color=red, stroke_width=2.2, dash_length=0.1)
        drop2 = DashedLine(axR.c2p(0.8, C), axR.c2p(0.8, 0),
                           color=red, stroke_width=2.2, dash_length=0.1)
        scene.play(Create(drop1), Create(drop2), run_time=0.7)
        scene.play(FadeIn(mob, shift=0.1 * np.array([0.0, 1.0, 0.0])), run_time=0.5)
        return 5.6

    if "annotation.0" in ids:
        ids["annotation.0"].anim = play_sweep
    return keep


# ================================================================ hook 3
# composition_identities -- 點 x 沿上弧(f)到 B 的 f(x),沿下弧(f⁻¹)回原點閃一下;
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
    labA.next_to(ellA, np.array([0.0, 1.0, 0.0]), buff=0.14)
    labB.next_to(ellB, np.array([0.0, 1.0, 0.0]), buff=0.14)

    px = Dot([-2.7, 0.0, 0.0], radius=0.075, color=cyan)
    py = Dot([2.7, 0.0, 0.0], radius=0.075, color=gold)
    labx = MathTex("x", color=text_col, font_size=T.fs("math_sm"))
    laby = MathTex("f(x)", color=text_col, font_size=T.fs("math_sm"))
    labx.next_to(px, np.array([-1.0, 0.0, 0.0]), buff=0.15)
    laby.next_to(py, np.array([1.0, 0.0, 0.0]), buff=0.15)

    arc_f = ArcBetweenPoints(px.get_center() + np.array([0.12, 0.12, 0]),
                             py.get_center() + np.array([-0.12, 0.12, 0]),
                             angle=-0.9, color=cyan, stroke_width=3.0)
    arc_b = ArcBetweenPoints(py.get_center() + np.array([-0.12, -0.12, 0]),
                             px.get_center() + np.array([0.12, -0.12, 0]),
                             angle=-0.9, color=gold, stroke_width=3.0)
    lab_f = MathTex("f", color=cyan, font_size=T.fs("math_sm"))
    lab_b = MathTex("f^{-1}", color=gold, font_size=T.fs("math_sm"))
    lab_f.next_to(arc_f, np.array([0.0, 1.0, 0.0]), buff=0.12)
    lab_b.next_to(arc_b, np.array([0.0, -1.0, 0.0]), buff=0.12)

    diagram = VGroup(ellA, ellB, labA, labB, arc_f, arc_b, lab_f, lab_b,
                     px, py, labx, laby)

    eq0 = ids["math.0"].mobject.scale(0.85)
    eq1 = ids["math.1"].mobject.scale(0.85)
    eqs = VGroup(eq0, eq1).arrange(np.array([1.0, 0.0, 0.0]), buff=0.9)

    layout = VGroup(statement, diagram, eqs).arrange(np.array([0.0, -1.0, 0.0]),
                                                     buff=0.45)
    _centre_in_zone(title, layout, bottom_pad=0.1)

    def round_trip(scene, mob, g, *, start_dot, fwd_arc, back_arc, flash_col):
        tracer = start_dot.copy().set_z_index(3)
        scene.add(tracer)
        scene.play(MoveAlongPath(tracer, fwd_arc), run_time=1.0)
        scene.play(MoveAlongPath(tracer, back_arc), run_time=1.0)
        scene.play(Flash(start_dot.get_center(), color=flash_col,
                         line_length=0.22, num_lines=12, flash_radius=0.45),
                   run_time=0.55)
        scene.remove(tracer)
        return 2.55

    def play_first(scene, mob, g):
        scene.play(Create(ellA), Create(ellB), FadeIn(labA), FadeIn(labB),
                   run_time=0.7)
        scene.play(FadeIn(px), FadeIn(py), FadeIn(labx), FadeIn(laby),
                   Create(arc_f), Create(arc_b), FadeIn(lab_f), FadeIn(lab_b),
                   run_time=0.8)
        spent = 1.5
        spent += round_trip(scene, mob, g, start_dot=px, fwd_arc=arc_f,
                            back_arc=arc_b, flash_col=T.color(g, "secondary"))
        scene.play(FadeIn(eq0, shift=0.1 * np.array([0.0, 1.0, 0.0])), run_time=0.5)
        scene.add(diagram, eq0)
        return spent + 0.5

    def ensure_diagram(scene, mob, g):
        # End-of-scene sweep for unrevealed dynamics calls this; the diagram is
        # already on screen (play_first drew it), so this is a zero-cost no-op
        # that just guarantees presence. The block exists so sizecheck measures
        # the diagram's bbox (graph layer: exempt from the overlap guard).
        scene.add(mob)
        return 0.0

    def play_second(scene, mob, g):
        # second identity f(f^{-1}(y)) = y: start at y in B, ride f^{-1} down
        # the lower arc to A, then f back along the upper arc -- the existing
        # arcs already point the right way (arc_b: B->A, arc_f: A->B).
        spent = round_trip(scene, mob, g, start_dot=py, fwd_arc=arc_b,
                           back_arc=arc_f, flash_col=T.color(g, "accent"))
        scene.play(FadeIn(eq1, shift=0.1 * np.array([0.0, 1.0, 0.0])), run_time=0.5)
        scene.add(eq1)
        return spent + 0.5

    # math.0 carries ONLY eq0 as its measurable mobject (the diagram rides in a
    # separate graph-layer block) -- bundling diagram+eq0 made one huge bbox
    # that falsely "overlapped" eq1 beside it (rectangles, not shapes).
    ids["math.0"].mobject = eq0
    ids["math.0"].anim = play_first
    ids["math.1"].mobject = eq1
    ids["math.1"].anim = play_second
    out = list(blocks)
    out.insert(out.index(ids["math.0"]),
               Block("hookdiagram", diagram, anim=ensure_diagram,
                     static=False, layer="graph"))
    return out


# ================================================================ hook 4
# graphs_mirror_across_y_x -- x³ 沿 y=x 翻摺生成 ∛x;點對 (a,b)→(b,a) 跨鏡線
# 對應閃示;收在兩曲線＋鏡線並存的全圖。


def graphs_mirror_across_y_x(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    axes = ids["axes"].mobject

    # template plot order (storyboard): 0 x^3, 1 cbrt, 2 y=x, 3 connector,
    # 4 (a,b) point, 5 (b,a) point; labels: 0 x^3, 1 cbrt, 2 y=x, 3 (a,b), 4 (b,a)
    cbrt_blk = ids["plot.1"]
    conn_blk = ids["plot.3"]
    pb_blk = ids["plot.5"]
    lab_cbrt_blk = ids["label.1"]
    lab_pb_blk = ids["label.4"]
    x3_mob = ids["plot.0"].mobject          # VGroup(glow, graph)
    x3_curve = x3_mob[1]

    # these enter inside the beat, choreographed by the callable
    deferred = [cbrt_blk, conn_blk, pb_blk, lab_cbrt_blk, lab_pb_blk]
    kept = [b for b in blocks if b not in deferred]
    annotation = ids["annotation.0"]

    centre = axes.c2p(0, 0)

    def play_fold(scene, mob, g):
        ghost = x3_curve.copy().set_stroke(opacity=0.9)
        scene.add(ghost)

        def mirror(p):
            v = p - centre
            return centre + np.array([v[1], v[0], 0.0])

        target = x3_curve.copy().apply_function(mirror)
        scene.play(ReplacementTransform(ghost, target), run_time=1.6)
        scene.play(FadeIn(cbrt_blk.mobject), run_time=0.45)
        scene.remove(target)
        scene.play(FadeIn(lab_cbrt_blk.mobject), run_time=0.35)

        scene.play(Create(conn_blk.mobject), run_time=0.55)
        scene.play(GrowFromCenter(pb_blk.mobject), run_time=0.4)
        scene.play(Flash(pb_blk.mobject.get_center(), color=T.color(g, "accent"),
                         line_length=0.2, num_lines=12, flash_radius=0.4),
                   FadeIn(lab_pb_blk.mobject), run_time=0.55)
        scene.play(FadeIn(mob, shift=0.1 * np.array([0.0, 1.0, 0.0])), run_time=0.5)
        return 4.4

    annotation.anim = play_fold
    return kept

"""§3.1 Derivatives of Sine and Cosine -- custom hook animations (3 cues from
the LOCKED content script / storyboard `animation_cue` specs).

Each factory follows the hook contract (pipeline/templates/__init__._apply_hook):
it receives the TEMPLATE's blocks and returns the final list. It may drop the
stock graph's `axes` block, build a bespoke figure, and append new reveal
blocks whose ids match the storyboard's {show ...} markers. Deleting a scene's
`hook:` line restores the stock template scene.

Per CONTENT_METHODOLOGY §5, this generated code is treated like narration: the
user reviews the rendered result before it is final; render failures are
patched smallest-first.

The three hooks (scene id -> Figure -> cue):
  sector_inequality   Figure 3.1  nested unit-circle areas  (tri_inner, sector,
                                  tri_outer, ineq)
  slope_equals_height Figure 3.3  sin tangents vs cos heights (tan_0,
                                  tan_halfpi, tan_pi, cos_dots)
  shm_stacked_graphs  Figure 3.4  s/s'/s'' over one time axis, s''=-s
                                  (g_s, g_v, g_a, mirror)
"""
from __future__ import annotations

import numpy as np
from manim import (
    AnnularSector,
    Arc,
    Axes,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    Line,
    MathTex,
    Polygon,
    VGroup,
)

from pipeline import brand
from pipeline.blocks import Block
from pipeline.visuals import theme as T

PI = np.pi
UP = np.array([0.0, 1.0, 0.0])
DOWN = np.array([0.0, -1.0, 0.0])
LEFT = np.array([-1.0, 0.0, 0.0])
RIGHT = np.array([1.0, 0.0, 0.0])
DL = np.array([-1.0, -1.0, 0.0])
DR = np.array([1.0, -1.0, 0.0])
UL = np.array([-1.0, 1.0, 0.0])


def _by_id(blocks: list[Block]) -> dict[str, Block]:
    return {b.id: b for b in blocks}


def _centre_in_zone(title_mob, group, *, bottom_pad: float = 0.45) -> None:
    """Centre *group* vertically in the zone between the title and the bottom
    safe margin (shared with the §1.1 hooks)."""
    zone_top = title_mob.get_bottom()[1] - 0.55
    zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN + bottom_pad
    group.move_to([0, (zone_top + zone_bottom) / 2, 0])


def _fade(scene, mob, g):
    scene.play(FadeIn(mob), run_time=0.55)
    scene.add(mob)
    return 0.65


def _draw(scene, mob, g):
    scene.play(Create(mob), run_time=0.65)
    scene.add(mob)
    return 0.75


# ================================================================ hook 1
# sector_inequality (Figure 3.1) -- on the unit circle, the inscribed triangle
# OAB sits inside the sector OAB, which sits inside the outer triangle OAC;
# revealing the three regions builds 1/2 sin t <= 1/2 t <= 1/2 tan t.


def sector_inequality(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    title = ids["title"].mobject
    out = [b for b in blocks if b.id != "axes"]   # we draw the circle ourselves

    R = 2.3
    th = 0.72                                       # representative angle (~41 deg)
    O = np.array([0.0, 0.0, 0.0])
    A = np.array([R, 0.0, 0.0])
    B = np.array([R * np.cos(th), R * np.sin(th), 0.0])
    C = np.array([R, R * np.tan(th), 0.0])

    text = T.color(ground, "text")
    mut = T.color(ground, "muted")
    blue = T.color(ground, "secondary")
    amber = T.color(ground, "accent")
    green = T.color(ground, "success")

    quarter = Arc(radius=R, start_angle=0.0, angle=PI / 2, arc_center=O,
                  color=mut, stroke_width=2.0)
    xaxis = Line(O + 0.25 * LEFT, A + 0.6 * RIGHT, color=mut, stroke_width=1.5)
    yaxis = Line(O + 0.25 * DOWN, np.array([0.0, R + 0.6, 0.0]), color=mut, stroke_width=1.5)
    tangent = DashedLine(A, C, color=mut, stroke_width=2.0, dash_length=0.1)
    radius_OC = Line(O, C, color=text, stroke_width=2.0)
    chord_OA = Line(O, A, color=text, stroke_width=2.0)

    dots = VGroup(*[Dot(p, radius=0.05, color=text) for p in (O, A, B, C)])
    lO = MathTex("O", color=text, font_size=T.fs("label")).next_to(O, DL, buff=0.12)
    lA = MathTex("A", color=text, font_size=T.fs("label")).next_to(A, DR, buff=0.10)
    lB = MathTex("B", color=text, font_size=T.fs("label")).next_to(B, UL, buff=0.08)
    lC = MathTex("C", color=text, font_size=T.fs("label")).next_to(C, RIGHT, buff=0.12)
    arc_th = Arc(radius=0.48, start_angle=0.0, angle=th, arc_center=O, color=text, stroke_width=2.0)
    lth = MathTex(r"\theta", color=text, font_size=T.fs("label")).move_to(
        O + 0.72 * np.array([np.cos(th / 2), np.sin(th / 2), 0.0]))

    for m in (radius_OC, chord_OA, dots, lO, lA, lB, lC, arc_th, lth):
        m.set_z_index(5)
    scaffold = VGroup(quarter, xaxis, yaxis, tangent, radius_OC, chord_OA,
                      dots, lO, lA, lB, lC, arc_th, lth)

    tri_inner = Polygon(O, A, B, color=blue, fill_opacity=0.40, stroke_width=2.5).set_z_index(2)
    lab_inner = brand.math_line(r"\tfrac12\sin\theta", ground, role="secondary", size="label")
    lab_inner.move_to(0.46 * A + 0.16 * B)          # interior, clear of the theta vertex label
    g_inner = VGroup(tri_inner, lab_inner)

    sector = AnnularSector(inner_radius=0.0, outer_radius=R, angle=th, start_angle=0.0,
                           arc_center=O, color=amber, fill_opacity=0.30,
                           stroke_width=2.0).set_z_index(1)
    lab_sector = brand.math_line(r"\tfrac12\theta", ground, role="accent", size="label")
    lab_sector.move_to(O + (R + 0.5) * np.array([np.cos(th / 2), np.sin(th / 2), 0.0]))
    g_sector = VGroup(sector, lab_sector)

    tri_outer = Polygon(O, A, C, color=green, fill_opacity=0.0, stroke_width=3.0).set_z_index(3)
    lab_outer = brand.math_line(r"\tfrac12\tan\theta", ground, role="success", size="label")
    lab_outer.next_to(C, RIGHT, buff=0.55).shift(0.25 * DOWN)
    g_outer = VGroup(tri_outer, lab_outer)

    ineq = brand.math_line(r"\tfrac12\sin\theta \;\le\; \tfrac12\theta \;\le\; \tfrac12\tan\theta",
                           ground, role="text", size="math_sm")

    figure = VGroup(scaffold, g_inner, g_sector, g_outer)
    ineq.next_to(figure, DOWN, buff=0.55)
    _centre_in_zone(title, VGroup(figure, ineq))

    out.append(Block("scaffold", scaffold, static=True, layer="graph"))
    out.append(Block("tri_inner", g_inner, anim=_fade, static=False, layer="graph"))
    out.append(Block("sector", g_sector, anim=_fade, static=False, layer="graph"))
    out.append(Block("tri_outer", g_outer, anim=_fade, static=False, layer="graph"))
    out.append(Block("ineq", ineq, anim=_fade, static=False, layer="graph"))
    return out


# ================================================================ hook 2
# slope_equals_height (Figure 3.3) -- tangents to y=sin x at 0, pi/2, pi have
# slopes 1, 0, -1, exactly the heights of y=cos x there. The base graph already
# carries plot.0 (sin) and plot.1 (cos); the hook adds the tangents + cos dots.


def slope_equals_height(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    axes = ids["axes"].mobject

    amber = T.color(ground, "accent")
    green = T.color(ground, "success")

    marks = [(0.0, 1.0, "1"), (np.pi / 2, 0.0, "0"), (np.pi, -1.0, "-1")]  # (x0, cos x0, label)

    def tangent(x0, slope):
        d = 0.62
        p1 = axes.c2p(x0 - d, np.sin(x0) - d * slope)
        p2 = axes.c2p(x0 + d, np.sin(x0) + d * slope)
        seg = Line(p1, p2, color=green, stroke_width=5.0)
        lab = brand.math_line("m=%s" % ("1" if slope == 1 else "0" if slope == 0 else "-1"),
                              ground, role="success", size="label")
        anchor = axes.c2p(x0, np.sin(x0))
        lab.move_to(anchor + (0.62 * UP if slope >= 0 else 0.62 * DOWN))
        return VGroup(seg, lab)

    tan_0 = tangent(0.0, 1.0)
    tan_halfpi = tangent(np.pi / 2, 0.0)
    tan_pi = tangent(np.pi, -1.0)

    cos_dots = VGroup()
    for x0, h, lab in marks:
        dot = Dot(axes.c2p(x0, h), radius=0.07, color=amber)
        ml = brand.math_line(lab, ground, role="accent", size="label")
        ml.next_to(dot, UP if h >= 0 else DOWN, buff=0.14)
        cos_dots.add(VGroup(dot, ml))

    out = list(blocks)
    out.append(Block("tan_0", tan_0, anim=_draw, static=False, layer="graph"))
    out.append(Block("tan_halfpi", tan_halfpi, anim=_draw, static=False, layer="graph"))
    out.append(Block("tan_pi", tan_pi, anim=_draw, static=False, layer="graph"))
    out.append(Block("cos_dots", cos_dots, anim=_fade, static=False, layer="graph"))
    return out


# ================================================================ hook 3
# shm_stacked_graphs (Figure 3.4) -- height s=sin t, velocity s'=cos t,
# acceleration s''=-sin t stacked over one shared time axis; dashed verticals
# at the peaks/troughs (where velocity passes zero); s''=-s = top flipped.


def shm_stacked_graphs(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    title = ids["title"].mobject
    out = [b for b in blocks if b.id != "axes"]

    amber = T.color(ground, "accent")
    blue = T.color(ground, "secondary")
    green = T.color(ground, "success")
    mut = T.color(ground, "muted")

    rows = [(np.sin, amber, r"s=\sin t"),
            (np.cos, blue, r"s'=\cos t"),
            (lambda t: -np.sin(t), green, r"s''=-\sin t")]

    groups = []
    axes_list = []
    for i, (func, color, label_tex) in enumerate(rows):
        ax = Axes(x_range=[0, 2 * PI, PI / 2], y_range=[-1.2, 1.2, 1],
                  x_length=6.0, y_length=1.0, tips=False,
                  axis_config={"color": mut, "stroke_width": 1.4, "include_ticks": False})
        curve = ax.plot(func, x_range=[0, 2 * PI], color=color, stroke_width=3.5)
        # move axes AND curve together (the curve is not a child of the axes, so
        # moving the axes alone leaves the curve behind on the origin band).
        plot_grp = VGroup(ax, curve).move_to([0.6, (1 - i) * 1.55, 0.0])
        lab = brand.math_line(label_tex, ground, role="text", size="label")
        lab.next_to(ax, LEFT, buff=0.3)
        groups.append(VGroup(lab, plot_grp))
        axes_list.append(ax)
    ax_top, _, ax_bot = axes_list

    stack = VGroup(*groups)
    _centre_in_zone(title, stack)

    def vline(t):
        top = ax_top.c2p(t, 1.2)
        bot = ax_bot.c2p(t, -1.2)
        return DashedLine(np.array([top[0], top[1], 0.0]), np.array([bot[0], bot[1], 0.0]),
                          color=mut, stroke_width=1.8, dash_length=0.09)

    mirror = VGroup(vline(PI / 2), vline(3 * PI / 2))
    mlab = brand.math_line(r"s''=-s", ground, role="success", size="label")
    mlab.next_to(groups[2], DOWN, buff=0.22)
    g_mirror = VGroup(mirror, mlab)

    out.append(Block("g_s", groups[0], anim=_draw, static=False, layer="graph"))
    out.append(Block("g_v", groups[1], anim=_draw, static=False, layer="graph"))
    out.append(Block("g_a", groups[2], anim=_draw, static=False, layer="graph"))
    out.append(Block("mirror", g_mirror, anim=_fade, static=False, layer="graph"))
    return out

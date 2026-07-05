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

The four hooks (scene id -> Figure -> cue):
  sector_inequality    Figure 3.1  nested unit-circle areas  (tri_inner, sector,
                                   tri_outer, ineq)
  slope_equals_height  Figure 3.3  sin tangents vs cos heights (tan_0,
                                   tan_halfpi, tan_pi, cos_dots)
  shm_stacked_graphs   Figure 3.4  s/s'/s'' over one time axis, s''=-s
                                   (g_s, g_v, g_a, mirror)
  toward_the_chain_rule  end-of-section trio -> three chip cards, solved vs
                                   not-yet (math.0; Task 14 #6)
"""
from __future__ import annotations

import numpy as np
from manim import (
    AnnularSector,
    Arc,
    Axes,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    Line,
    MathTex,
    Polygon,
    ReplacementTransform,
    VGroup,
    smooth,
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
# sector_inequality (Figure 3.1) -- on the unit circle the inscribed triangle
# OAB sits inside the sector OAB, which sits inside the outer triangle OAC. The
# source figure (left) builds that nested picture as narration names each region;
# a congruent copy of each region then peels off and slides onto a shared
# baseline on the right at true relative size, turning 1/2 sin t <= 1/2 t <=
# 1/2 tan t into a visible ordering of three SEPARATED shapes (not three
# overlapping fills). Reveal ids are unchanged (tri_inner, sector, tri_outer,
# ineq), so the LOCKED narration + {show ...} cues need no edit.


def sector_inequality(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    title = ids["title"].mobject
    out = [b for b in blocks if b.id != "axes"]   # we draw the circle ourselves

    R = 2.4                                          # was 1.45 -- enlarged to fill the empty
                                                      # band under the old (smallish) figure;
                                                      # the right-side glyphs are CONGRUENT
                                                      # copies of the same R (see docstring),
                                                      # so their baseline spacing below widens
                                                      # to match instead of letting them touch
    th = 0.72                                       # representative angle (~41 deg)
    B_off = R * np.array([np.cos(th), np.sin(th), 0.0])   # apex of triangle OAB
    C_off = np.array([R, R * np.tan(th), 0.0])            # apex of triangle OAC

    text = T.color(ground, "text")
    mut = T.color(ground, "muted")
    blue = T.color(ground, "secondary")
    amber = T.color(ground, "accent")
    green = T.color(ground, "success")

    def _tri(o, apex_off, col, fop, z):
        return Polygon(o, o + np.array([R, 0.0, 0.0]), o + apex_off,
                       color=col, fill_opacity=fop, stroke_width=2.5).set_z_index(z)

    def _sec(o, fop, z):
        return AnnularSector(inner_radius=0.0, outer_radius=R, angle=th,
                             start_angle=0.0, arc_center=o, color=amber,
                             fill_opacity=fop, stroke_width=2.5).set_z_index(z)

    # Main-figure fills stack OPAQUE (not translucent): OAB (blue) sits inside
    # the sector (amber), which sits inside OAC (green), so painting largest-
    # first at increasing z-index (outer=1 -> sector=2 -> inner=3) lets each
    # later fill fully mask the part of the one below it -- three clean colour
    # bands (the ring between sector/outer edges) instead of the old low-alpha
    # stack (0.10/0.30/0.45) whose overlaps blended into a muddy teal.
    MAIN_FOP = 0.88

    # -- left: source figure (scaffold static; regions revealed in place) --------
    O = np.array([-4.55, -0.40, 0.0])
    A = O + np.array([R, 0.0, 0.0])
    B = O + B_off
    C = O + C_off

    quarter = Arc(radius=R, start_angle=0.0, angle=PI / 2, arc_center=O,
                  color=mut, stroke_width=2.0)
    xaxis = Line(O + 0.25 * LEFT, A + 0.5 * RIGHT, color=mut, stroke_width=1.5)
    yaxis = Line(O + 0.25 * DOWN, O + np.array([0.0, R + 0.5, 0.0]),
                 color=mut, stroke_width=1.5)
    tangent = DashedLine(A, C, color=mut, stroke_width=2.0, dash_length=0.08)
    radius_OC = Line(O, C, color=text, stroke_width=2.0)
    chord_OA = Line(O, A, color=text, stroke_width=2.0)

    dots = VGroup(*[Dot(p, radius=0.045, color=text) for p in (O, A, B, C)])
    lO = MathTex("O", color=text, font_size=T.fs("label")).next_to(O, DL, buff=0.10)
    lA = MathTex("A", color=text, font_size=T.fs("label")).next_to(A, DR, buff=0.08)
    lB = MathTex("B", color=text, font_size=T.fs("label")).next_to(B, UL, buff=0.06)
    lC = MathTex("C", color=text, font_size=T.fs("label")).next_to(C, RIGHT, buff=0.10)
    arc_th = Arc(radius=0.34, start_angle=0.0, angle=th, arc_center=O,
                 color=text, stroke_width=2.0)
    lth = MathTex(r"\theta", color=text, font_size=T.fs("label")).move_to(
        O + 0.55 * np.array([np.cos(th / 2), np.sin(th / 2), 0.0]))

    # dimension labels on the source construction so a paused viewer can see WHY
    # each area is 1/2 sin, 1/2 theta, 1/2 tan: shared base = 1, the inner height
    # sin(theta) (dropped from B to OA), the outer height tan(theta) (segment AC).
    mid_OA = (O + A) / 2.0
    l_base = MathTex("1", color=text, font_size=T.fs("label")).next_to(mid_OA, DOWN, buff=0.14)
    footB = np.array([B[0], O[1], 0.0])
    drop_sin = DashedLine(B, footB, color=mut, stroke_width=1.6, dash_length=0.06)
    l_sin = MathTex(r"\sin\theta", color=text, font_size=T.fs("label")).next_to(drop_sin, LEFT, buff=0.05)
    # sits on AC's outer (right) edge, below C's own label so the two never
    # crowd each other -- 0.62*(A->C) instead of the true midpoint leaves lC
    # (near the top, at C) and l_tan clearly separated.
    tan_anchor = A + 0.62 * (C - A)
    l_tan = MathTex(r"\tan\theta", color=text, font_size=T.fs("label")).next_to(tan_anchor, RIGHT, buff=0.12)
    dim = (l_base, drop_sin, l_sin, l_tan)

    for m in (radius_OC, chord_OA, dots, lO, lA, lB, lC, arc_th, lth, *dim):
        m.set_z_index(5)
    scaffold = VGroup(quarter, xaxis, yaxis, tangent, radius_OC, chord_OA,
                      dots, lO, lA, lB, lC, arc_th, lth, *dim)

    # z-order LARGEST region first (bottom) so each later, smaller, opaque fill
    # fully covers the part of the bigger one it sits inside -- outer (z=1)
    # under sector (z=2) under inner (z=3) leaves three distinct colour rings:
    # green (OAC-only) / amber (sector-only) / blue (OAB), not a translucent blend.
    src_outer = _tri(O, C_off, green, MAIN_FOP, 1)
    src_sector = _sec(O, MAIN_FOP, 2)
    src_inner = _tri(O, B_off, blue, MAIN_FOP, 3)

    # ①②③ chips anchored IN the main figure's three regions (not just the right
    # glyphs), so a paused viewer can map region -> formula directly on the
    # source construction. Anchors are fractions of R (hand-tuned by numeric
    # point-in-region search, then expressed R-relative so they track a resize):
    # the sector-only sliver between chord AB and the arc is genuinely thin
    # (~0.15u regardless of R), so its chip sits astride the arc itself rather
    # than buried in a sliver too narrow to hold a legible ring; the other two
    # sit well inside their own region, clear of the scaffold's O/A/B/C/
    # dimension labels.
    def _chip(anchor_off, col, n, radius=0.14):
        ring = Circle(radius=radius, color=col, stroke_width=2.0,
                      fill_color=T.color(ground, "bg"), fill_opacity=0.9).set_z_index(7)
        ring.move_to(O + anchor_off)
        num = MathTex(str(n), color=text, font_size=T.fs("label") * 0.68 * (radius / 0.14))
        num.move_to(ring.get_center()).set_z_index(8)
        return VGroup(ring, num)

    chip_inner = _chip(R * np.array([0.605, 0.158, 0.0]), blue, 1)
    # smaller radius: the sector-only sliver between chord AB and the arc is only
    # ~0.12u deep regardless of R, so a full-size chip would bleed equally into
    # both neighbours; a tighter ring keeps it legibly "on the amber band."
    chip_sector = _chip(R * np.array([np.cos(0.52 * th), np.sin(0.52 * th), 0.0]),
                        amber, 2, radius=0.10)
    chip_outer = _chip(R * np.array([0.947, 0.716, 0.0]), green, 3)

    # -- right: three peeled shapes on one baseline (true relative size) ---------
    yb = O[1]                                        # share the source baseline
    GLYPH_GAP = 0.45                                 # air between adjacent congruent shapes
    O1 = np.array([-1.30, yb, 0.0])
    O2 = O1 + np.array([R + GLYPH_GAP, 0.0, 0.0])
    O3 = O2 + np.array([R + GLYPH_GAP, 0.0, 0.0])
    badge_y = yb + R * np.tan(th) + 0.34             # one row, above the tallest apex

    def _badge(n, x, col):
        ring = Circle(radius=0.16, color=col, stroke_width=2.0)
        num = MathTex(str(n), color=text, font_size=T.fs("label") * 0.75)
        return VGroup(ring, num).move_to(np.array([x, badge_y, 0.0])).set_z_index(6)

    def _slot(o, shape, lab_tex, role, n, badge_col):
        lab = brand.math_line(lab_tex, ground, role=role, size="label")
        lab.next_to(shape, DOWN, buff=0.28)
        badge = _badge(n, o[0] + R / 2, badge_col)   # centred over the slot, equal height
        return VGroup(shape, lab, badge)

    dst1 = _slot(O1, _tri(O1, B_off, blue, 0.50, 2),
                 r"\tfrac12\sin\theta", "secondary", 1, blue)
    dst2 = _slot(O2, _sec(O2, 0.42, 2),
                 r"\tfrac12\theta", "accent", 2, amber)
    dst3 = _slot(O3, _tri(O3, C_off, green, 0.40, 2),
                 r"\tfrac12\tan\theta", "success", 3, green)

    ineq = brand.math_line(
        r"\tfrac12\sin\theta \;\le\; \tfrac12\theta \;\le\; \tfrac12\tan\theta",
        ground, role="text", size="math_sm")
    row = VGroup(dst1, dst2, dst3)
    ineq.next_to(row, DOWN, buff=0.55)

    full = VGroup(scaffold, src_inner, src_sector, src_outer,
                  chip_inner, chip_sector, chip_outer, dst1, dst2, dst3, ineq)
    _centre_in_zone(title, full)

    def _peel(src, chip):
        def anim(scene, mob, ground):
            shape, label, badge = mob[0], mob[1], mob[2]
            scene.play(FadeIn(src), run_time=0.4)            # region appears on the left
            scene.add(src)
            flyer = src.copy()
            scene.add(flyer)
            # congruent copy slides out to its slot on the right (rigid motion)
            scene.play(ReplacementTransform(flyer, shape), run_time=0.8, rate_func=smooth)
            # right-side glyph brightens (label + badge) the SAME beat the main
            # figure's own ①②③ chip appears, tying the two halves together.
            scene.play(FadeIn(label, shift=0.08 * UP), FadeIn(badge), FadeIn(chip), run_time=0.32)
            return 1.52
        return anim

    out.append(Block("scaffold", scaffold, static=True, layer="graph"))
    out.append(Block("tri_inner", dst1, anim=_peel(src_inner, chip_inner), static=False, layer="graph"))
    out.append(Block("sector", dst2, anim=_peel(src_sector, chip_sector), static=False, layer="graph"))
    out.append(Block("tri_outer", dst3, anim=_peel(src_outer, chip_outer), static=False, layer="graph"))
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
    mut = T.color(ground, "muted")

    # (x0, cos x0, full-identity label) -- the label reads the identity, not a
    # bare number, so it does not collide in meaning with the sin curve's own
    # "0" tick at the origin (two unrelated "0"s next to each other read as a
    # mistake to a paused viewer).
    marks = [(0.0, 1.0, r"\cos 0 = 1"), (np.pi / 2, 0.0, r"\cos\tfrac{\pi}{2} = 0"),
             (np.pi, -1.0, r"\cos\pi = -1")]

    # x-axis teaching ticks at the three named angles the narration reads, so a
    # paused viewer can tell which x each slope/height belongs to (house style: a
    # few labelled ticks, not a full number line). No tick glyph at x=0 -- it would
    # sit on the y-axis; the "0" label alone anchors the origin.
    xticks = VGroup()
    for xv, xlab, draw_tick in [(0.0, "0", False), (np.pi / 2, r"\tfrac{\pi}{2}", True), (np.pi, r"\pi", True)]:
        p = axes.c2p(xv, 0.0)
        if draw_tick:
            xticks.add(Line(p + 0.09 * UP, p + 0.09 * DOWN, color=mut, stroke_width=2.0))
        xticks.add(MathTex(xlab, color=mut, font_size=T.fs("label")).next_to(p, DOWN, buff=0.20))

    # Screen length, not data-space half-width, is held fixed across the three
    # tangents: at this axes' aspect ratio a slope-0 segment of the old fixed
    # data-width d=0.62 rendered visibly SHORTER on screen than the +-1 diagonal
    # ones. Solve d per-slope so the drawn segment is the same length in scene
    # units for all three, matching the "three equal tangents" reading the
    # figure wants.
    TARGET_LEN = 3.0
    x_scale = axes.x_axis.get_unit_size()
    y_scale = axes.y_axis.get_unit_size()

    def tangent(x0, slope):
        dir_len = np.hypot(x_scale, slope * y_scale)
        d = TARGET_LEN / (2.0 * dir_len)
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

    # Dashed connector ties each tangent point on sin (x0, sin x0) straight down
    # (same x0) to its read-off dot on cos (x0, cos x0) -- "slope here = height
    # there" made literal. Drawn together with cos_dots so it appears at the
    # exact beat the narration reads the matching heights, not before.
    DOT_R = 0.07
    cos_dots = VGroup()
    for x0, h, lab in marks:
        sin_pt = axes.c2p(x0, np.sin(x0))
        cos_pt = axes.c2p(x0, h)
        # trim both ends past the dot radius (and off the curve point) so the
        # dash pattern doesn't terminate a partial dash inside the dot itself.
        gap = DOT_R + 0.03
        v = cos_pt - sin_pt
        v_hat = v / np.linalg.norm(v)
        connector = DashedLine(sin_pt + gap * v_hat, cos_pt - gap * v_hat,
                               color=mut, stroke_width=1.6, dash_length=0.07)
        dot = Dot(cos_pt, radius=DOT_R, color=amber)
        ml = brand.math_line(lab, ground, role="accent", size="label")
        if x0 == 0.0:
            # this dot sits ON the y-axis; a centred label above it would have
            # the axis line run straight through the text, so offset sideways
            # (up and clear to the right) instead of stacking straight up.
            ml.next_to(dot, UP + RIGHT, buff=0.12)
        else:
            ml.next_to(dot, UP if h >= 0 else DOWN, buff=0.14)
        cos_dots.add(VGroup(connector, dot, ml))

    out = list(blocks)
    out.append(Block("xticks", xticks, static=True, layer="graph"))
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

    rows = [(np.sin, amber, r"s=\sin t", r"\text{Height}"),
            (np.cos, blue, r"s'=\cos t", r"\text{Velocity}"),
            (lambda t: -np.sin(t), green, r"s''=-\sin t", r"\text{Acceleration}")]

    groups = []
    axes_list = []
    for i, (func, color, label_tex, word_tex) in enumerate(rows):
        ax = Axes(x_range=[0, 2 * PI, PI / 2], y_range=[-1.2, 1.2, 1],
                  x_length=6.0, y_length=1.0, tips=False,
                  axis_config={"color": mut, "stroke_width": 1.4, "include_ticks": False})
        curve = ax.plot(func, x_range=[0, 2 * PI], color=color, stroke_width=3.5)
        # move axes AND curve together (the curve is not a child of the axes, so
        # moving the axes alone leaves the curve behind on the origin band).
        plot_grp = VGroup(ax, curve).move_to([0.6, (1 - i) * 1.55, 0.0])
        # left label = physical name (Height/Velocity/Acceleration) over the formula,
        # so the row reads as physics, not just symbols.
        word = brand.math_line(word_tex, ground, role="text", size="label")
        formula = brand.math_line(label_tex, ground, role="text", size="label")
        lab = VGroup(word, formula).arrange(DOWN, buff=0.10, aligned_edge=RIGHT)
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

    guide_ts = [PI / 2, 3 * PI / 2]
    mirror = VGroup(*(vline(t) for t in guide_ts))

    # guide labels, once each, tucked under the bottom axis where they sit clear
    # of all three curves (no per-panel repetition needed -- one shared time axis).
    guide_labels = VGroup()
    for t, tex in zip(guide_ts, [r"t=\tfrac{\pi}{2}", r"t=\tfrac{3\pi}{2}"]):
        glab = brand.math_line(tex, ground, role="text", size="label")
        glab.next_to(ax_bot.c2p(t, -1.2), DOWN, buff=0.22)
        guide_labels.add(glab)

    # dots where each curve crosses a guide -- the read-off the narration asks for
    # (height peaks/troughs <-> velocity crosses zero <-> acceleration mirrors height).
    # These can only sit on a guide that already spans all three panels, so, like the
    # guide lines themselves, they ride the `mirror` beat rather than their own panel.
    guide_dots = VGroup()
    for (func, color, _, _), ax in zip(rows, axes_list):
        for t in guide_ts:
            guide_dots.add(Dot(ax.c2p(t, func(t)), radius=0.07, color=color))

    mlab = brand.math_line(r"s''=-s", ground, role="success", size="label")
    mlab.next_to(groups[2][1], RIGHT, buff=0.35)  # anchored to the accel panel's right side
    g_mirror = VGroup(mirror, guide_labels, guide_dots, mlab)

    out.append(Block("g_s", groups[0], anim=_draw, static=False, layer="graph"))
    out.append(Block("g_v", groups[1], anim=_draw, static=False, layer="graph"))
    out.append(Block("g_a", groups[2], anim=_draw, static=False, layer="graph"))
    out.append(Block("mirror", g_mirror, anim=_fade, static=False, layer="graph"))
    return out


# ================================================================ hook 4
# toward_the_chain_rule -- the section closer's trio ($\sin x$ vs $\sin(x^2)$
# vs $\sin(3x+1)$) was one flat math line ("checkmark ... ? ... ?"), which
# buries the point the narration is making: one of the three is already solved,
# the other two are not (yet). Three chip cards say that at a glance -- a
# green-accent-bar card for the solved bare form, two amber-accent-bar cards
# (matching the "?" ink) for the composed ones still waiting on the chain rule.
# Single reveal id `math.0` is kept (the storyboard's {show math.0} cue and
# narration are untouched); only the block's mobject is swapped.


def toward_the_chain_rule(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    old_math = ids["math.0"].mobject   # old line's LEFT edge == SPINE_X (statement's own left-flush axis)

    chips_spec = [
        (r"\sin x", "check", "success"),
        (r"\sin(x^{2})", "query", "accent"),
        (r"\sin(3x+1)", "query", "accent"),
    ]

    def _chip(tex, glyph_name, role):
        formula = brand.math_line(tex, ground, role="primary", size="math_sm")
        # glyph() has no ready-made "?"; a direct MathTex keeps the actual question
        # mark the storyboard math reads, styled the same accent colour glyph() uses.
        mark = (brand.glyph("check", ground, role=role, size="math_sm") if glyph_name == "check"
               else MathTex("?", color=T.color(ground, role), font_size=T.fs("math_sm")))
        row = VGroup(formula, mark).arrange(RIGHT, buff=0.30)
        return brand.accent_panel(row, ground, bar_role=role, pad=0.32, pad_x=0.42)

    chips = [_chip(tex, gname, role) for tex, gname, role in chips_spec]
    trio = VGroup(*chips).arrange(RIGHT, buff=0.55)
    # Left-flush to the old line's left edge (== SPINE_X), matching the statement
    # above it -- old_math.get_center() would be wrong here: it is the centre of a
    # short single line, not of this much wider row, and would push the row's left
    # edge off-frame.
    trio.move_to(old_math.get_left(), aligned_edge=LEFT)

    ids["math.0"].mobject = trio
    return blocks

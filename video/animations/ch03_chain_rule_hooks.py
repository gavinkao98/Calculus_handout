"""§3.2 The Chain Rule -- custom hook animations (2 cues from the LOCKED content
script / storyboard `animation_cue` specs).

Each factory follows the hook contract (pipeline/templates/__init__._apply_hook):
it receives the TEMPLATE's blocks and returns the final list. It drops the stock
graph's `axes` block, builds a bespoke figure, and appends reveal blocks whose
ids match the storyboard's {show ...} markers. Deleting a scene's `hook:` line
restores the stock template scene.

Per CONTENT_METHODOLOGY §5, this generated code is treated like narration: the
user reviews the rendered result before it is final; render failures are patched
smallest-first.

The two hooks (scene id -> Figure -> cue):
  composed_mapping   Figure 3.5  h stretched by g'(x0), then by f'(g(x0)); the
                                 two stretches multiply  (inc_h, stretch_g,
                                 stretch_f, product)
  remainder_tangent  Figure 3.6  curve hugs its tangent; gap R(h) shrinks far
                                 faster than h  (gap_Rh, gap_halved, local_fact)
"""
from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Axes,
    DashedLine,
    Dot,
    FadeIn,
    Line,
    MathTex,
    VGroup,
)

from pipeline import brand
from pipeline.blocks import Block
from pipeline.visuals import theme as T

UP = np.array([0.0, 1.0, 0.0])
DOWN = np.array([0.0, -1.0, 0.0])
LEFT = np.array([-1.0, 0.0, 0.0])
RIGHT = np.array([1.0, 0.0, 0.0])


def _by_id(blocks: list[Block]) -> dict[str, Block]:
    return {b.id: b for b in blocks}


def _centre_in_zone(title_mob, group, *, bottom_pad: float = 0.45) -> None:
    """Centre *group* vertically in the zone between the title and the bottom
    safe margin (shared with the §3.1 hooks)."""
    zone_top = title_mob.get_bottom()[1] - 0.55
    zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN + bottom_pad
    group.move_to([0, (zone_top + zone_bottom) / 2, 0])


def _fade(scene, mob, g):
    scene.play(FadeIn(mob), run_time=0.55)
    scene.add(mob)
    return 0.65


# ================================================================ hook 1
# composed_mapping (Figure 3.5) -- three stacked lines x, u, y. A small increment
# h on the x-line is carried by g to an increment g'(x0)h on the u-line, then by
# f to f'(g(x0))g'(x0)h on the y-line. The increments are drawn at TRUE relative
# width (0.7 -> 1.15 -> 1.9), so the two stretches -- and their product -- are
# literally visible as a growing segment. Reveal ids: inc_h, stretch_g,
# stretch_f, product.


def composed_mapping(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    title = ids["title"].mobject
    out = [b for b in blocks if b.id != "axes"]   # we draw the lines ourselves

    text = T.color(ground, "text")
    mut = T.color(ground, "muted")
    blue = T.color(ground, "secondary")
    amber = T.color(ground, "accent")
    green = T.color(ground, "success")

    L, Rgt = -3.4, 3.0
    y_of = {"x": 1.55, "u": 0.0, "y": -1.55}
    arrow_x = 2.2          # arrows on the right, away from the increments
    base_x = -1.5          # left end of every increment (the base point)
    width = {"x": 0.7, "u": 1.15, "y": 1.9}   # h, g'(x0)h, f'(g(x0))g'(x0)h

    def hline(y):
        return Line([L, y, 0.0], [Rgt, y, 0.0], color=mut, stroke_width=1.6)

    lines = VGroup(hline(y_of["x"]), hline(y_of["u"]), hline(y_of["y"]))
    letters = VGroup(
        MathTex("x", color=text, font_size=T.fs("label")).next_to([Rgt, y_of["x"], 0.0], RIGHT, buff=0.18),
        MathTex("u", color=text, font_size=T.fs("label")).next_to([Rgt, y_of["u"], 0.0], RIGHT, buff=0.18),
        MathTex("y", color=text, font_size=T.fs("label")).next_to([Rgt, y_of["y"], 0.0], RIGHT, buff=0.18),
    )
    base_dots = VGroup(*[Dot([base_x, y_of[k], 0.0], radius=0.05, color=text)
                         for k in ("x", "u", "y")])
    base_labels = VGroup(
        brand.math_line("x_0", ground, role="text", size="label").next_to([base_x, y_of["x"], 0.0], DOWN, buff=0.16),
        brand.math_line("u_0=g(x_0)", ground, role="text", size="label").next_to([base_x, y_of["u"], 0.0], DOWN, buff=0.16),
        brand.math_line("y_0", ground, role="text", size="label").next_to([base_x, y_of["y"], 0.0], DOWN, buff=0.16),
    )
    scaffold = VGroup(lines, letters, base_dots, base_labels)

    def increment(y, w, col):
        return Line([base_x, y, 0.0], [base_x + w, y, 0.0], color=col, stroke_width=6.0)

    def down_arrow(y_top, y_bot, lab_tex):
        ar = Arrow([arrow_x, y_top - 0.16, 0.0], [arrow_x, y_bot + 0.16, 0.0],
                   buff=0.0, color=text, stroke_width=3.0,
                   max_tip_length_to_length_ratio=0.22)
        lab = brand.math_line(lab_tex, ground, role="text", size="label").next_to(ar, RIGHT, buff=0.14)
        return VGroup(ar, lab)

    seg_h = increment(y_of["x"], width["x"], amber)
    inc_h = VGroup(seg_h, brand.math_line("h", ground, role="accent", size="label").next_to(seg_h, UP, buff=0.14))

    seg_u = increment(y_of["u"], width["u"], blue)
    stretch_g = VGroup(
        down_arrow(y_of["x"], y_of["u"], "g"),
        seg_u,
        brand.math_line("g'(x_0)\\,h", ground, role="secondary", size="label").next_to(seg_u, UP, buff=0.14),
    )

    seg_y = increment(y_of["y"], width["y"], green)
    stretch_f = VGroup(
        down_arrow(y_of["u"], y_of["y"], "f"),
        seg_y,
        brand.math_line("f'(g(x_0))\\,g'(x_0)\\,h", ground, role="success", size="label").next_to(seg_y, UP, buff=0.14),
    )

    product = brand.math_line(
        r"\times\, g'(x_0)\ \text{then}\ \times\, f'(g(x_0))\ \Rightarrow\ \times\, f'(g(x_0))\,g'(x_0)",
        ground, role="text", size="math_sm")
    product.move_to([0.0, y_of["y"] - 1.0, 0.0])

    full = VGroup(scaffold, inc_h, stretch_g, stretch_f, product)
    _centre_in_zone(title, full)

    out.append(Block("scaffold", scaffold, static=True, layer="graph"))
    out.append(Block("inc_h", inc_h, anim=_fade, static=False, layer="graph"))
    out.append(Block("stretch_g", stretch_g, anim=_fade, static=False, layer="graph"))
    out.append(Block("stretch_f", stretch_f, anim=_fade, static=False, layer="graph"))
    out.append(Block("product", product, anim=_fade, static=False, layer="graph"))
    return out


# ================================================================ hook 2
# remainder_tangent (Figure 3.6) -- the graph of f hugs its tangent at x0. At
# x0+h the vertical gap to the tangent is the remainder R(h); at x0+h/2 the gap is
# ~1/4 as tall (R ~ 1/2 f'' h^2), the geometric content of R(h)/h -> 0. Reveal
# ids: gap_Rh, gap_halved, local_fact.


def remainder_tangent(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    title = ids["title"].mobject
    out = [b for b in blocks if b.id != "axes"]

    text = T.color(ground, "text")
    mut = T.color(ground, "muted")
    blue = T.color(ground, "secondary")
    amber = T.color(ground, "accent")
    green = T.color(ground, "success")

    ax = Axes(x_range=[-0.15, 2.35, 1], y_range=[-0.2, 3.0, 1],
              x_length=7.2, y_length=4.0, tips=False,
              axis_config={"color": mut, "stroke_width": 1.4, "include_ticks": False})

    def f(x):
        return 0.6 * x * x

    def fp(x):
        return 1.2 * x

    x0 = 0.4
    h = 1.2

    def tan(x):
        return f(x0) + fp(x0) * (x - x0)

    curve = ax.plot(f, x_range=[0.0, 2.2], color=amber, stroke_width=3.5)
    tangent = DashedLine(ax.c2p(0.0, tan(0.0)), ax.c2p(2.2, tan(2.2)),
                         color=mut, stroke_width=2.5, dash_length=0.10)
    x0dot = Dot(ax.c2p(x0, f(x0)), radius=0.05, color=text)
    x0lab = brand.math_line("x_0", ground, role="text", size="label").next_to(ax.c2p(x0, 0.0), DOWN, buff=0.14)
    flab = brand.math_line("f", ground, role="accent", size="label").next_to(ax.c2p(2.2, f(2.2)), RIGHT, buff=0.12)
    tlab = brand.math_line("\\text{tangent}", ground, role="muted", size="label").next_to(ax.c2p(2.2, tan(2.2)), RIGHT, buff=0.12)
    scaffold = VGroup(ax, curve, tangent, x0dot, x0lab, flab, tlab)

    def gap(dh, col, role, lab_tex, lab_dir=RIGHT):
        xh = x0 + dh
        top = ax.c2p(xh, f(xh))
        bot = ax.c2p(xh, tan(xh))
        seg = Line(bot, top, color=col, stroke_width=5.0)
        foot = DashedLine(ax.c2p(xh, 0.0), bot, color=mut, stroke_width=1.2, dash_length=0.07)
        lab = brand.math_line(lab_tex, ground, role=role, size="label").next_to(seg, lab_dir, buff=0.12)
        return VGroup(foot, seg, lab)

    gap_Rh = gap(h, blue, "secondary", "R(h)")
    # label ABOVE its (short) segment, clear of the rising dashed tangent on the right
    gap_halved = gap(h / 2, green, "success", "R(h/2)", lab_dir=UP)
    local_fact = brand.math_line(
        r"\tfrac{R(h)}{h}\to 0:\ \text{up close, } f \text{ is its tangent line}",
        ground, role="accent", size="math_sm")

    full = VGroup(scaffold, gap_Rh, gap_halved)
    _centre_in_zone(title, full)
    local_fact.next_to(ax, DOWN, buff=0.40)
    everything = VGroup(full, local_fact)
    _centre_in_zone(title, everything)

    out.append(Block("scaffold", scaffold, static=True, layer="graph"))
    out.append(Block("gap_Rh", gap_Rh, anim=_fade, static=False, layer="graph"))
    out.append(Block("gap_halved", gap_halved, anim=_fade, static=False, layer="graph"))
    out.append(Block("local_fact", local_fact, anim=_fade, static=False, layer="graph"))
    return out

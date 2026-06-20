"""procedure_steps template -- Direction B (dark teaching frame).

Matches screenshots/04-procedure_steps.png + B_Procedure:
  eyebrow "[ PROCEDURE ]" + title;
  centred list of rows, each: a large display numeral (cyan, glow) | thin
  vertical rule | step text | the step's resulting math (right);
  a bottom "Worked" strip card: example chained with arrows.

Each row's math is the dynamic reveal (math.0/1/2); the numeral+text+rule come
with the static frame.

YAML shape:
  template: procedure_steps
  accent: procedure
  title: "..."
  steps:
    - { text: "...", math: "..." }
  worked: ["f(x)=2x+3", "y=2x+3", "f^{-1}(x)=\\tfrac{x-3}{2}"]   # optional chain
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT, RIGHT, RoundedRectangle, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T
from ._common import scene_head, motif_corner


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []
    blocks += scene_head(spec, ctx, label="[ procedure ]")
    title = blocks[1].mobject

    left = -T.FRAME_W / 2 + T.SIDE_GUTTER
    steps = spec.get("steps", [])
    row_gap = 1.4        # designed rhythm = MINIMUM pitch
    min_clear = 0.35     # air kept between tall rows (pitch expands, never collides)
    title_clear = 0.2    # air a tall FIRST row keeps below the title
    top = 1.5

    from manim import Text
    right_edge = T.FRAME_W / 2 - T.SIDE_GUTTER
    math_rows = []
    y = top
    prev_half = None
    for i, st in enumerate(steps):
        # zero-padded blue numeral (01/02/03) with a soft blue glow, Times New Roman bold.
        numeral = brand.text_glow(
            Text(f"{i + 1:02d}", font=T.FONT_DISPLAY, weight="BOLD",
                 font_size=T.fs("numeral"), color=T.color(ground, "secondary")),
            ground, role="secondary", width=3.0, opacity=0.4)
        rule = brand.vrule(64 / T.PX_PER_UNIT_Y, ground, role="hairline", width=2)
        txt = brand.prose(st.get("text", ""), ground, role="text", size="prose",
                          max_width=5.0, align="LEFT")
        # numeral | rule | text as one left-anchored row (move_to+aligned_edge,
        # the proven pattern); the step's math sits at the right gutter edge, same y.
        row = VGroup(numeral, rule, txt).arrange(RIGHT, buff=0.5)
        m = brand.math_line(st.get("math", ""), ground, role="blue_ink", size=44)

        half = max(row.height, m.height) / 2
        if prev_half is None:
            # a tall FIRST row also grows upward -- keep it clear of the title
            y = min(y, title.get_bottom()[1] - title_clear - half)
        else:
            y -= max(row_gap, prev_half + min_clear + half)
        row.move_to([left, y, 0], aligned_edge=LEFT)
        m.move_to([right_edge, y, 0], aligned_edge=RIGHT)
        prev_half = half

        blocks.append(Block(f"row.{i}", row, anim="fade", static=True))
        math_rows.append(m)

    for i, m in enumerate(math_rows):
        blocks.append(Block(f"math.{i}", m, anim="write", static=False))

    # bottom worked-example strip: a rounded outline box (no left bar) with an
    # amber-ink WORKED tag, then the example chained with CM arrows.
    worked = spec.get("worked", [])
    if worked:
        tag = brand.eyebrow("worked", ground, role="amber_ink")
        chain = []
        for j, piece in enumerate(worked):
            chain.append(brand.math_line(piece, ground, role="blue_ink", size="math_sm"))
            if j < len(worked) - 1:
                chain.append(brand.math_line(r"\to", ground, role="muted", size="math_sm"))
        row = VGroup(tag, *chain).arrange(RIGHT, buff=0.4)
        box = RoundedRectangle(
            corner_radius=T.RADIUS_MD, width=row.width + 0.9, height=row.height + 0.7,
            stroke_color=T.color(ground, "hairline"), stroke_width=1.5,
            fill_color=T.color(ground, "bg_soft"), fill_opacity=1.0)
        box.move_to(row.get_center())
        strip = VGroup(box, row)
        strip.move_to([0, -T.FRAME_H / 2 + T.SAFE_MARGIN + box.height / 2 + 0.1, 0])
        blocks.append(Block("worked", strip, anim="fade", static=False))

    blocks.append(motif_corner(ground))
    return blocks

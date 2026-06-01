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

from manim import DOWN, LEFT, RIGHT, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T
from ._common import scene_head, motif_corner


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []
    blocks += scene_head(spec, ctx, label="[ procedure ]")

    left = -T.FRAME_W / 2 + T.SIDE_GUTTER
    steps = spec.get("steps", [])
    row_gap = 1.4
    top = 1.5

    from manim import Text
    math_rows = []
    for i, st in enumerate(steps):
        numeral = Text(str(i + 1), font=T.FONT_DISPLAY, weight="BOLD",
                       font_size=T.fs(72), color=T.color(ground, "secondary"))
        rule = brand.vrule(0.9, ground, role="hairline", width=2)
        txt = brand.prose(st.get("text", ""), ground, size="step",
                          max_width=4.6, align="LEFT")
        # numeral | rule | text as one left-anchored row (move_to+aligned_edge,
        # the proven pattern); the step's math sits at a fixed right column, same y.
        row = VGroup(numeral, rule, txt).arrange(RIGHT, buff=0.5)
        y = top - i * row_gap
        row.move_to([left, y, 0], aligned_edge=LEFT)

        m = brand.math_line(st.get("math", ""), ground, role="math", size="math")
        m.move_to([T.FRAME_W / 2 - T.SIDE_GUTTER - 1.4, y, 0])

        blocks.append(Block(f"row.{i}", row, anim="fade", static=True))
        math_rows.append(m)

    for i, m in enumerate(math_rows):
        blocks.append(Block(f"math.{i}", m, anim="write", static=False))

    # bottom worked-example strip
    worked = spec.get("worked", [])
    if worked:
        from manim import Text
        tag = brand.eyebrow("worked", ground, role="accent")
        chain = []
        for j, piece in enumerate(worked):
            chain.append(brand.math_line(piece, ground, role="math", size="math_sm"))
            if j < len(worked) - 1:
                chain.append(Text("→", font=T.FONT_BODY, font_size=T.fs("math_sm"),
                                  color=T.color(ground, "muted")))
        row = VGroup(tag, *chain).arrange(RIGHT, buff=0.35)
        card = brand.math_card(row, ground, pad=0.4)
        strip = VGroup(card, row)
        strip.move_to([0, -T.FRAME_H / 2 + T.SAFE_MARGIN + card.height / 2 + 0.1, 0])
        blocks.append(Block("worked", strip, anim="fade", static=False))

    blocks.append(motif_corner(ground))
    return blocks

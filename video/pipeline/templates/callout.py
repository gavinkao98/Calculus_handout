"""callout template -- Direction D (NEW). Remark / Caution / Note.

The recurring named boxed aside the handouts use constantly ((fg)'!=f'g',
f^{-1}!=1/f, power-rule domain, ...). One template, colour-swapped by `type`:
  remark -> blue, caution -> red, note -> amber.

A single raised panel (surface + a 6px coloured left bar) centred vertically; a
glyph box on the left (! caution / star remark / i note), then a mono kicker in
the type colour (+ optional number) and a large prose body with inline math.

YAML shape:
  template: callout
  type: caution            # remark | caution | note   (default caution)
  number: "1.1"            # optional
  body: "The superscript $-1$ in $f^{-1}$ means the inverse function --- not a reciprocal."
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT, RIGHT, UP, MathTex, RoundedRectangle, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T
from ._common import motif_corner

_TYPE_ROLE = {"remark": "secondary", "caution": "warning", "note": "accent"}
_TYPE_INK = {"remark": "blue_ink", "caution": "red_ink", "note": "amber_ink"}
_TYPE_LABEL = {"remark": "Remark", "caution": "Caution", "note": "Note"}


def _mark(ctype: str, ground: str, role: str) -> VGroup:
    """The 74px glyph box: a rounded square outlined in the type colour, with the
    type's glyph centred, and a soft same-colour glow."""
    side = 74 / T.PX_PER_UNIT_X
    box = RoundedRectangle(width=side, height=side, corner_radius=16 / T.PX_PER_UNIT_X,
                           stroke_color=T.color(ground, role), stroke_width=3,
                           fill_opacity=0)
    if ctype == "remark":
        glyph = brand._four_point_star(side * 0.26, T.color(ground, role), 1.0)
    else:
        ch = "!" if ctype == "caution" else "i"
        glyph = brand.heading(ch, ground, role=role, size=46)
    glyph.move_to(box.get_center())
    return brand.text_glow(VGroup(box, glyph), ground, role=role, width=4.0, opacity=0.4)


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    ctype = str(spec.get("type", "caution")).lower()
    if ctype not in _TYPE_ROLE:
        ctype = "caution"
    role = _TYPE_ROLE[ctype]
    ink = _TYPE_INK[ctype]
    blocks: list[Block] = []

    mark = _mark(ctype, ground, role)

    # kicker: mono uppercase label in the type ink, + optional number in ink-3
    label = brand.eyebrow(_TYPE_LABEL[ctype], ground, role=ink)
    kicker_parts = [label]
    if spec.get("number"):
        num = brand.eyebrow(str(spec["number"]), ground, role="muted")
        kicker_parts.append(num)
    kicker = VGroup(*kicker_parts).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)

    body = brand.prose(str(spec.get("body", "")), ground, role="primary", size="prose",
                       max_width=8.4, align="LEFT")

    content = VGroup(kicker, body).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    row = VGroup(mark, content).arrange(RIGHT, buff=0.55, aligned_edge=UP)

    panel = brand.accent_panel(row, ground, bar_role=role, fill_role="panel",
                               radius=T.RADIUS_LG, bar_px=6, pad=0.6, pad_x=0.75)
    panel.move_to([0, 0, 0])

    blocks.append(Block("panel", VGroup(panel[0], panel[1]), anim="fade",
                        static=True, layer="background"))
    blocks.append(Block("mark", mark, anim="fade", static=True))
    blocks.append(Block("kicker", kicker, anim="fade", static=True))
    blocks.append(Block("body", body, anim="write_glow", static=False))
    blocks.append(motif_corner(ground))
    return blocks

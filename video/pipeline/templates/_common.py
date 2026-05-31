"""Shared template helpers for Direction B dark teaching frames.

scene_head: the eyebrow tag + title block every teaching template opens with
(mirrors B_SceneHead in the design, minus the grid -- grids are disabled
project-wide, see theme.SHOW_GRID). Returns a list[Block] (eyebrow, title) all
static.

motif_corner: the faint summit-bars mark bottom-right.

These exist so the six dark templates don't each re-implement the same header.
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT

from .. import brand
from ..blocks import Block, accent_role
from ..visuals import theme as T


def scene_head(spec: dict[str, Any], ctx: dict[str, Any], *, label: str) -> list[Block]:
    ground = ctx["ground"]
    role = accent_role(spec)
    left = -T.FRAME_W / 2 + T.SIDE_GUTTER
    top = T.FRAME_H / 2 - T.SAFE_MARGIN

    blocks = []

    eyebrow = brand.eyebrow(label, ground, role=role)
    eyebrow.move_to([left + eyebrow.width / 2, top - eyebrow.height / 2, 0])
    blocks.append(Block("eyebrow", eyebrow, anim="fade", static=True))

    title = brand.heading(spec.get("title", ""), ground, role="primary", size="h1")
    title.next_to(eyebrow, DOWN, buff=0.28).align_to(eyebrow, LEFT)
    blocks.append(Block("title", title, anim="fade", static=True))

    return blocks


def motif_corner(ground: str) -> Block:
    motif = brand.summit_bars(ground, height=0.45, color_role="muted", opacity=0.4)
    motif.move_to([T.FRAME_W / 2 - T.SAFE_MARGIN - motif.width / 2,
                   -T.FRAME_H / 2 + T.SAFE_MARGIN + motif.height / 2, 0])
    return Block("motif", motif, anim="fade", static=True)

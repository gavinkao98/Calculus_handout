"""recap_cards template -- Direction D (dark teaching frame).

Matches screenshots/06-recap_cards.png + B_Recap. NOTE this is the DARK,
in-content recap (distinct from the LIGHT brand `outro`): a teaching summary,
not a brand bookend.

  eyebrow "[ RECAP ]" + title;
  single full-width column of numbered key points (01/02/03 + text).

Reveal: points reveal one by one (point.0/1/2).
All on the static header (grids disabled, see theme.SHOW_GRID).

YAML shape:
  template: recap_cards
  accent: recap
  title: "Section 1.1 — Recap"
  points: ["...", "...", "..."]
"""
from __future__ import annotations

from typing import Any

from manim import LEFT, UL, UP, VGroup

from .. import brand
from ..blocks import Block
from ._common import scene_head, motif_corner, center_in_zone, ColumnPlan, SPINE_X, CONTENT_W


def capacity_meta(spec: dict[str, Any]) -> list[ColumnPlan]:
    """Capacity contract (L2): points sit at fixed gaps (non-elastic), so measure the
    column's actual span. min_pitch unused by the span model."""
    return [ColumnPlan(min_pitch=0.0, model="span")]


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []
    blocks += scene_head(spec, ctx, label="[ recap ]")
    title = blocks[1].mobject
    content: list = []

    left = SPINE_X
    points = spec.get("points", [])

    # -- numbered points (full width) --
    pt_gap = 0.35
    y_cursor = 1.95
    max_w = CONTENT_W - 1.2   # full content width minus numeral + buffer
    for i, t in enumerate(points):
        idx = brand.text_glow(
            brand.heading(f"{i+1:02d}", ground, role="accent", size="h3"),
            ground, role="accent", width=1.6, opacity=0.3)
        txt = brand.prose(t, ground, role="text", size="prose", max_width=max_w, align="LEFT")
        first_line = txt.submobjects[0] if isinstance(txt, VGroup) and txt.submobjects else txt
        idx.next_to(first_line, LEFT, buff=0.34)
        row = VGroup(idx, txt)
        row.move_to([left, y_cursor, 0], aligned_edge=UL)
        y_cursor -= row.height + pt_gap
        blocks.append(Block(f"point.{i}", row, anim="fade", static=False))
        content.append(row)

    center_in_zone(content, title)
    blocks.append(motif_corner(ground))
    return blocks

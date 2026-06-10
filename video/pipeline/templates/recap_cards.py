"""recap_cards template -- Direction B (dark teaching frame).

Matches screenshots/06-recap_cards.png + B_Recap. NOTE this is the DARK,
in-content recap (distinct from the LIGHT brand `outro`): a teaching summary,
not a brand bookend.

  eyebrow "[ RECAP ]" + title;
  two columns --
    LEFT  : numbered key points (01/02/03 + dot + text);
    RIGHT : a "Remember" eyebrow + boxed formula cards (cyan left border).

Reveal: points reveal one by one (point.0/1/2); formula cards reveal after
(formula.0/1). All on the static header (grids disabled, see theme.SHOW_GRID).

YAML shape:
  template: recap_cards
  accent: recap
  title: "Section 1.1 — Recap"
  points: ["...", "...", "..."]
  formulas: ["f(x_1)=f(x_2) \\implies x_1=x_2", "(f^{-1}\\circ f)(x)=x"]
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT, RIGHT, UL, UP, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T
from ._common import scene_head, motif_corner


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []
    blocks += scene_head(spec, ctx, label="[ recap ]")

    left = -T.FRAME_W / 2 + T.SIDE_GUTTER
    points = spec.get("points", [])
    formulas = spec.get("formulas", [])

    # -- left column: numbered points --
    # Advance by each row's REAL height (top-anchored), not a fixed row pitch:
    # with pitch 1.2 a point that wrapped to three lines overran the slot and
    # visually fused with the next bullet (v2 frame critique, recap scene).
    pt_gap = 0.5
    y_cursor = 1.75
    for i, t in enumerate(points):
        idx = brand.eyebrow(f"0{i+1}", ground, role="accent")
        dot = brand.plot_dot(ground, role="accent", r=0.06)
        txt = brand.prose(t, ground, size="step", max_width=5.0, align="LEFT")
        dot.next_to(txt, LEFT, buff=0.25, aligned_edge=UP)
        idx.next_to(dot, LEFT, buff=0.25, aligned_edge=UP)
        row = VGroup(idx, dot, txt)
        row.move_to([left, y_cursor, 0], aligned_edge=UL)
        y_cursor -= row.height + pt_gap
        blocks.append(Block(f"point.{i}", row, anim="fade", static=False))

    # -- right column: "Remember" + formula cards --
    # right_x sets the cards' left edge. Kept left enough that a full-width
    # two-term formula card (e.g. "f(x_1)=f(x_2) => x_1=x_2") clears the
    # broadcast-safe edge -- at 2.2 it spilled off-frame (caught by the overflow
    # guard); the points column ends near x=0.5, so this still reads as two columns.
    right_x = 1.15
    rem = brand.eyebrow("remember", ground, role="secondary")
    rem.move_to([right_x, 2.0, 0], aligned_edge=LEFT)
    blocks.append(Block("remember", rem, anim="fade", static=True))

    card_gap = 1.4
    card_top = 0.9
    for i, f in enumerate(formulas):
        m = brand.math_line(f, ground, role="math", size="math")
        card = brand.math_card(m, ground, pad=0.45)
        # cyan left border accent, flush to the card's left edge
        accent_bar = brand.vrule(card.height, ground, role="secondary", width=4)
        accent_bar.move_to([card.get_left()[0], card.get_center()[1], 0])
        grp = VGroup(card, accent_bar, m)
        grp.move_to([right_x, card_top - i * card_gap, 0], aligned_edge=LEFT)
        blocks.append(Block(f"formula.{i}", grp, anim="fade", static=False))

    blocks.append(motif_corner(ground))
    return blocks

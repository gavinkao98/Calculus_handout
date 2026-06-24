"""recap_cards template -- Direction D (dark teaching frame).

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
from ._common import scene_head, motif_corner, center_in_zone, ColumnPlan, SPINE_X, RAIL_X


def capacity_meta(spec: dict[str, Any]) -> list[ColumnPlan]:
    """Capacity contract (L2): points (left) and formula cards (right) sit at fixed gaps
    (non-elastic), so measure each column's actual span -- the taller column (usually the
    wrapped points) binds. min_pitch unused by the span model."""
    return [ColumnPlan(min_pitch=0.0, model="span")]


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []
    blocks += scene_head(spec, ctx, label="[ recap ]")
    title = blocks[1].mobject
    content: list = []   # both columns, centred in the zone at the end

    left = SPINE_X
    points = spec.get("points", [])
    formulas = spec.get("formulas", [])

    # -- left column: numbered points --
    # Advance by each row's REAL height (top-anchored), not a fixed row pitch:
    # with pitch 1.2 a point that wrapped to three lines overran the slot and
    # visually fused with the next bullet (v2 frame critique, recap scene).
    pt_gap = 0.42  # keep the 4-point column inside the bottom safe margin (sizecheck)
    y_cursor = 1.95
    for i, t in enumerate(points):
        # numbered-item language shared with procedure_steps: a bold display-serif numeral
        # in the section accent with a soft glow (was a tiny mono eyebrow + a redundant
        # accent dot -- a different vocabulary from procedure's glowing numerals, 2026-06-21
        # A3). Smaller than a procedure step numeral: here the number is a LIST MARKER, not
        # the structural anchor, and it replaces the dot (one marker, not two).
        idx = brand.text_glow(
            brand.heading(f"{i+1:02d}", ground, role="accent", size="h3"),
            ground, role="accent", width=1.6, opacity=0.3)
        txt = brand.prose(t, ground, role="text", size="prose", max_width=5.6, align="LEFT")
        idx.next_to(txt, LEFT, buff=0.34, aligned_edge=UP)
        row = VGroup(idx, txt)
        row.move_to([left, y_cursor, 0], aligned_edge=UL)
        y_cursor -= row.height + pt_gap
        blocks.append(Block(f"point.{i}", row, anim="fade", static=False))
        content.append(row)

    # -- right column: "Remember" + formula cards --
    # Cards' left edge snaps to the shared Lectern rail column (was a bare 1.15 magic
    # number; RAIL_X 1.06 is the same column derivation reasons / procedure results use,
    # so all three templates' right column aligns). Still clears the points column
    # (which ends near x=0.5) and keeps full-width two-term cards inside the safe edge.
    right_x = RAIL_X
    rem = brand.eyebrow("remember", ground, role="blue_ink")
    rem.move_to([right_x, 2.0, 0], aligned_edge=LEFT)
    blocks.append(Block("remember", rem, anim="fade", static=True))
    content.append(rem)

    card_gap = 1.55
    card_top = 1.0
    for i, f in enumerate(formulas):
        # blue-ink LaTeX on a raised card with a blue 6px left bar (the `.fcard`). The card
        # was undersized next to the points column (thin bar, tight pad -- 2026-06-21 B3):
        # more padding + a 6px bar + the lifted `panel` fill give it equal visual weight.
        m = brand.math_line(f, ground, role="blue_ink", size="math_sm")
        grp = brand.accent_panel(m, ground, bar_role="secondary", fill_role="panel",
                                 radius=T.RADIUS_MD, bar_px=6, pad=0.46, pad_x=0.62)
        grp.move_to([right_x, card_top - i * card_gap, 0], aligned_edge=LEFT)
        blocks.append(Block(f"formula.{i}", grp, anim="fade", static=False))
        content.append(grp)

    center_in_zone(content, title)
    blocks.append(motif_corner(ground))
    return blocks

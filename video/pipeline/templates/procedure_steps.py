"""procedure_steps template -- Direction D (dark teaching frame).

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
from ._common import scene_head, motif_corner, center_in_zone, ColumnPlan, SPINE_X, RAIL_X


def capacity_meta(spec: dict[str, Any]) -> list[ColumnPlan]:
    """Capacity contract (L2): procedure places rows at a fixed centre-to-centre rhythm
    (not the elastic fill derivation does), so measure the rows' actual span. A worked
    strip pinned at the bottom reserves ~1.6u (its height + clearance) that the steps must
    clear. min_pitch is unused by the span model."""
    return [ColumnPlan(min_pitch=0.0, model="span",
                       extra_bottom=1.6 if spec.get("worked") else 0.0)]


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []
    blocks += scene_head(spec, ctx, label="[ procedure ]")
    title = blocks[1].mobject

    left = SPINE_X
    content: list = []   # step rows + result maths, centred in the zone (above the strip)
    steps = spec.get("steps", [])
    row_gap = 1.4        # designed rhythm = MINIMUM pitch
    min_clear = 0.35     # air kept between tall rows (pitch expands, never collides)
    title_clear = 0.2    # air a tall FIRST row keeps below the title
    top = 1.5

    from manim import Text
    # the result formula snaps to the shared Lectern rail column (was right-aligned at
    # the far gutter, which Codex flagged both rounds as a detached RHS with a "wide
    # dead band"). Left-aligned at RAIL_X it sits next to its instruction AND lines up
    # with the derivation reason rail / recap formula cards -- one right column system.
    math_rows = []
    y = top
    prev_half = None
    for i, st in enumerate(steps):
        # zero-padded blue numeral (01/02/03) with a soft blue glow, Times New Roman bold.
        numeral = brand.text_glow(
            Text(f"{i + 1:02d}", font=T.FONT_DISPLAY, weight="BOLD",
                 font_size=T.fs("numeral"), color=T.color(ground, "secondary")),
            ground, role="secondary", width=2.4, opacity=0.34)  # softer glow: Codex found the numerals over-glowing
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
        m.move_to([RAIL_X, y, 0], aligned_edge=LEFT)
        prev_half = half

        # a faint dotted leader ties each step to its result math across the gap to the
        # shared rail (mirrors derivation's reason rail). Without it the RHS read as a
        # detached column floating off to the right (2026-06-21 B2). Skip when the step
        # text nearly reaches the rail (no room for a readable leader).
        lead_start = row.get_right()[0] + 0.28
        lead_end = m.get_left()[0] - 0.22
        if lead_end - lead_start > 0.4:
            leader = brand.dotted_leader(lead_end - lead_start, ground,
                                         role="hairline_strong", opacity=0.5)
            leader.move_to([(lead_start + lead_end) / 2, y, 0])
            blocks.append(Block(f"lead.{i}", leader, anim="fade", static=True,
                                layer="decoration"))
            content.append(leader)

        blocks.append(Block(f"row.{i}", row, anim="fade", static=True))
        math_rows.append(m)
        content.append(row)
        content.append(m)

    for i, m in enumerate(math_rows):
        blocks.append(Block(f"math.{i}", m, anim="write", static=False))

    # bottom worked-example strip: a rounded outline box (no left bar) with an
    # amber-ink WORKED tag, then the example chained with CM arrows.
    worked = spec.get("worked", [])
    strip_h = 0.0
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
        strip_h = strip.height

    # centre the step rows in the zone above the (bottom-pinned) worked strip, so a
    # short procedure no longer floats high with an empty band above the strip.
    center_in_zone(content, title, extra_bottom=(strip_h + 0.35 if strip_h else 0.0))
    blocks.append(motif_corner(ground))
    return blocks

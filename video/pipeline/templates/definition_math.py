"""definition_math template -- Direction B (dark teaching frame).

Matches screenshots/02-definition_math.png (minus the grid -- grids are
disabled project-wide, see theme.SHOW_GRID):
  eyebrow "[ DEFINITION ]" top-left (accent hue) + title beneath it;
  centred English statement (wrapped, never mid-word);
  a math card holding the math lines, the key line in gold;
  faint summit-bars motif bottom-right.

Static: eyebrow, title, statement, card, motif.
Dynamic ({show math.N}): each math line.
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT, VGroup

from .. import brand
from ..blocks import Block, accent_role
from ..visuals import theme as T

LABEL = {
    "definition": "[ definition ]", "theorem": "[ theorem ]",
    "proposition": "[ proposition ]", "example": "[ example ]",
    "warning": "[ note ]", "procedure": "[ procedure ]", "recap": "[ recap ]",
}


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    role = accent_role(spec)
    left = -T.FRAME_W / 2 + T.SIDE_GUTTER
    top = T.FRAME_H / 2 - T.SAFE_MARGIN
    content_w = T.FRAME_W - 2 * T.SIDE_GUTTER
    blocks: list[Block] = []

    # `kicker` overrides the accent-derived eyebrow word -- e.g. a motivation
    # scene keeps the definition colour family but reads "[ MOTIVATION ]".
    kicker = spec.get("kicker")
    label = f"[ {kicker} ]" if kicker else LABEL.get(spec.get("accent", "definition"),
                                                     "[ definition ]")
    eyebrow = brand.eyebrow(label, ground, role=role)
    eyebrow.move_to([left + eyebrow.width / 2, top - eyebrow.height / 2, 0])
    blocks.append(Block("eyebrow", eyebrow, anim="fade", static=True))

    title = brand.heading_rich(spec.get("title", ""), ground, role="primary", size="h1",
                               max_width=content_w)
    title.next_to(eyebrow, DOWN, buff=T.EYEBROW_GAP).align_to(eyebrow, LEFT)
    blocks.append(Block("title", title, anim="fade", static=True))

    statement = None
    if spec.get("statement"):
        # prose() routes on content: inline $math$ / a \\ break -> Tex (so it
        # never prints "$f$" literally); plain prose -> wrapped, left-aligned Text.
        # The lead statement is ink-1 (`.f-prose.lead`).
        statement = brand.prose(spec["statement"], ground, role="primary", size="prose",
                                max_width=content_w, align="LEFT")

    math_mobs, anims = [], []
    for entry in spec.get("math", []):
        if isinstance(entry, dict):
            tex, anim = entry["tex"], entry.get("anim", "write")
        else:
            tex, anim = entry, "write"
        # Pass the raw string to math_line; it auto-detects pure-math vs mixed
        # text+inline-$math$ and picks MathTex / Tex. Do NOT strip the $ here --
        # that turned "$a$ whenever $b$" into broken nested math mode.
        is_key = anim == "highlight"
        if is_key:
            # `.math.key` -- amber + persistent text-shadow glow, revealed with a flash.
            mob = brand.text_glow(brand.math_line(tex.strip(), ground, role="accent"),
                                  ground, role="accent")
            anim = "write_glow"
        else:
            mob = brand.math_line(tex.strip(), ground, role="primary")
        math_mobs.append(mob)
        anims.append(anim)

    # Statement + math stack centre as ONE LEFT-FLUSH group in the zone between the
    # title and the bottom safe margin (`.f-body.center`: vertically centred, content
    # flush to the left gutter). Closes the old dead band above the content.
    parts = []
    if statement is not None:
        parts.append(statement)
    if math_mobs:
        stack = VGroup(*math_mobs)
        # Left-flush by default (Direction D); opt-in `math_align: center` for the
        # rare scene where the lines read as centred display equations.
        if spec.get("math_align") == "center":
            stack.arrange(DOWN, buff=0.36)
        else:
            stack.arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        parts.append(stack)
    if parts:
        content = VGroup(*parts).arrange(DOWN, buff=0.71, aligned_edge=LEFT)
        zone_top = title.get_bottom()[1] - T.TITLE_GAP
        zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN
        content.move_to([left + content.width / 2, (zone_top + zone_bottom) / 2, 0])
    if statement is not None:
        blocks.append(Block("statement", statement, anim="fade", static=True))
    for i, (mob, anim) in enumerate(zip(math_mobs, anims)):
        blocks.append(Block(f"math.{i}", mob, anim=anim, static=False))

    motif = brand.summit_bars(ground, height=0.45, color_role="muted", opacity=0.4)
    motif.move_to([T.FRAME_W / 2 - T.SAFE_MARGIN - motif.width / 2,
                   -T.FRAME_H / 2 + T.SAFE_MARGIN + motif.height / 2, 0])
    blocks.append(Block("motif", motif, anim="fade", static=True, layer="decoration"))

    return blocks

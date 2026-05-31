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

    eyebrow = brand.eyebrow(LABEL.get(spec.get("accent", "definition"), "[ definition ]"),
                            ground, role=role)
    eyebrow.move_to([left + eyebrow.width / 2, top - eyebrow.height / 2, 0])
    blocks.append(Block("eyebrow", eyebrow, anim="fade", static=True))

    title = brand.heading(spec.get("title", ""), ground, role="primary", size="h1")
    title.next_to(eyebrow, DOWN, buff=0.28).align_to(eyebrow, LEFT)
    blocks.append(Block("title", title, anim="fade", static=True))

    ref = title
    if spec.get("statement"):
        statement = brand.body_text(spec["statement"], ground, size="body",
                                    max_width=content_w, align="CENTER")
        statement.move_to([0, title.get_bottom()[1] - 0.95, 0])
        blocks.append(Block("statement", statement, anim="fade", static=True))
        ref = statement

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
        math_mobs.append(brand.math_line(tex.strip(), ground,
                                         role="accent" if is_key else "math"))
        anims.append(anim)

    if math_mobs:
        stack = VGroup(*math_mobs).arrange(DOWN, buff=0.5)
        stack.move_to([0, (ref.get_bottom()[1] - 3.3) / 2, 0])
        card = brand.math_card(stack, ground, pad=0.55)
        blocks.append(Block("card", card, anim="fade", static=True))
        for i, (mob, anim) in enumerate(zip(math_mobs, anims)):
            blocks.append(Block(f"math.{i}", mob, anim=anim, static=False))

    motif = brand.summit_bars(ground, height=0.45, color_role="muted", opacity=0.4)
    motif.move_to([T.FRAME_W / 2 - T.SAFE_MARGIN - motif.width / 2,
                   -T.FRAME_H / 2 + T.SAFE_MARGIN + motif.height / 2, 0])
    blocks.append(Block("motif", motif, anim="fade", static=True))

    return blocks

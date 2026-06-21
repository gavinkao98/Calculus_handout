"""definition_math template -- Lectern dark teaching frame.

A definition / statement / note frame: the eyebrow + title masthead (built by the
shared scene_head, fixed Lectern anchor) over a SINGLE left-flush column -- the prose
statement at full measure (natural line length, never forced into a narrow column),
then the symbolic math lines; the key line (`anim: highlight`) is amber + persistent
glow. The whole block is CENTRED in the body zone (place_body), so a light definition
gets balanced breathing room instead of floating high.

(An earlier two-column "words left | symbols right" layout was dropped, 2026-06-21: a
definition's prose and symbols are NOT paired per row -- unlike derivation's step↔reason
rail -- so splitting them only forced one-line statements to wrap into two. Two columns
are reserved for templates with a genuine per-row second stream; place_body centring now
fixes the vertical waste that the two-column was reaching for.)

Static: eyebrow, title, statement. Dynamic ({show math.N}): each math line.
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T
from ._common import scene_head, motif_corner, place_body, SPINE_X, CONTENT_W

LABEL = {
    "definition": "[ definition ]", "theorem": "[ theorem ]",
    "proposition": "[ proposition ]", "example": "[ example ]",
    "warning": "[ note ]", "procedure": "[ procedure ]", "recap": "[ recap ]",
}

MIN_PITCH = 0.36  # tightest inter-line gap (the math stack arrange buff); sizecheck capacity trigger


def _math_blocks(spec: dict[str, Any], ground: str):
    """Build the math line mobjects + their reveal anims.

    The key line (`anim: highlight`) is amber + persistent text-shadow glow, revealed
    with a flash; everything else is bright ink. The raw string goes to math_line
    unstripped of `$` -- it auto-detects pure-math vs mixed text+inline `$math$` and
    picks MathTex / Tex (stripping `$` broke "$a$ whenever $b$")."""
    math_mobs, anims = [], []
    for entry in spec.get("math", []):
        if isinstance(entry, dict):
            tex, anim = entry["tex"], entry.get("anim", "write")
        else:
            tex, anim = entry, "write"
        if anim == "highlight":
            mob = brand.text_glow(brand.math_line(tex.strip(), ground, role="accent"),
                                  ground, role="accent")
            anim = "write_glow"
        else:
            mob = brand.math_line(tex.strip(), ground, role="primary")
        math_mobs.append(mob)
        anims.append(anim)
    return math_mobs, anims


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []

    head = scene_head(spec, ctx,
                      label=LABEL.get(spec.get("accent", "definition"), "[ definition ]"))
    blocks += head
    title = head[1].mobject

    math_mobs, anims = _math_blocks(spec, ground)

    # single left-flush column: prose statement at full measure, then the math lines,
    # centred in the body zone (place_body) for balanced breathing room.
    statement = None
    if spec.get("statement"):
        statement = brand.prose(spec["statement"], ground, role="primary", size="prose",
                                max_width=CONTENT_W, align="LEFT")
    parts = []
    if statement is not None:
        parts.append(statement)
    if math_mobs:
        stack = VGroup(*math_mobs)
        if spec.get("math_align") == "center":
            stack.arrange(DOWN, buff=MIN_PITCH)
        else:
            stack.arrange(DOWN, buff=MIN_PITCH, aligned_edge=LEFT)
        parts.append(stack)
    if parts:
        content = VGroup(*parts).arrange(DOWN, buff=0.71, aligned_edge=LEFT)
        place_body(content, title, SPINE_X)

    if statement is not None:
        blocks.append(Block("statement", statement, anim="fade", static=True))
    for i, (mob, anim) in enumerate(zip(math_mobs, anims)):
        blocks.append(Block(f"math.{i}", mob, anim=anim, static=False))

    blocks.append(motif_corner(ground))
    return blocks

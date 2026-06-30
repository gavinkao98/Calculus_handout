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
from ._common import (scene_head, motif_corner, place_body, body_zone, build_aside,
                      render_scaffold, ColumnPlan, SPINE_X, CONTENT_W, PRIMARY_W, RAIL_X, RAIL_W)

LABEL = {
    "definition": "[ definition ]", "theorem": "[ theorem ]",
    "proposition": "[ proposition ]", "example": "[ example ]",
    "warning": "[ note ]", "procedure": "[ procedure ]", "recap": "[ recap ]",
}

MIN_PITCH = 0.36  # tightest inter-line gap (the math stack arrange buff); sizecheck capacity trigger


def capacity_meta(spec: dict[str, Any]) -> list[ColumnPlan]:
    """Capacity contract: definition_math is FIXED-rhythm, not elastic -- it arranges the
    statement + math stack at fixed buffs (0.71 between them, MIN_PITCH within the math)
    and place_body only POSITIONS that block (no fill expansion). So measure its actual
    span (span model), not a uniform-MIN_PITCH estimate, which would under-count the wider
    statement->math gap. (derivation, by contrast, uses fill_gap to expand, so it stays the
    stack model -- the tightest-pitch question.) min_pitch is unused by the span model."""
    return [ColumnPlan(min_pitch=0.0, model="span")]


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

    scaffold_blocks = render_scaffold(spec.get("scaffold"), ground, ctx.get("meta"))
    for sb in scaffold_blocks:
        sb.mobject.next_to(title, DOWN, buff=T.TITLE_GAP).align_to(title, LEFT)
        title = sb.mobject
    blocks += scaffold_blocks

    math_mobs, anims = _math_blocks(spec, ground)
    center_math = spec.get("math_align") == "center"

    def assemble(stmt_width: float):
        """Prose statement (at *stmt_width*) over the math stack, as one left-flush group."""
        statement = None
        if spec.get("statement"):
            statement = brand.prose(spec["statement"], ground, role="primary", size="prose",
                                    max_width=stmt_width, align="LEFT")
        parts = []
        if statement is not None:
            parts.append(statement)
        if math_mobs:
            stack = VGroup(*math_mobs)
            if center_math:
                stack.arrange(DOWN, buff=MIN_PITCH)
            else:
                stack.arrange(DOWN, buff=MIN_PITCH, aligned_edge=LEFT)
            parts.append(stack)
        content = VGroup(*parts).arrange(DOWN, buff=0.71, aligned_edge=LEFT) if parts else None
        return content, statement

    # Optional right-rail enrichment aside (L3): a sparse definition can opt a supporting
    # note / key-idea into the rail. When present, narrow the prose to the primary column
    # and place the aside at RAIL_X; collapse back to a full-width single column (no aside)
    # if the narrowed primary would overflow the zone or a math line is too wide for it --
    # the aside never crowds real content (it is enrichment, not a competing stream).
    aside_spec = spec.get("aside")
    use_aside = bool(aside_spec)
    if use_aside:
        content, statement = assemble(PRIMARY_W)
        zt, zb = body_zone(title)
        too_tall = content is not None and content.height > (zt - zb)
        too_wide = any(m.width > PRIMARY_W + 0.05 for m in math_mobs)
        if too_tall or too_wide:
            use_aside = False
    if not use_aside:
        content, statement = assemble(CONTENT_W)

    if content is not None:
        place_body(content, title, SPINE_X)

    if statement is not None:
        blocks.append(Block("statement", statement, anim="fade", static=True))
    for i, (mob, anim) in enumerate(zip(math_mobs, anims)):
        blocks.append(Block(f"math.{i}", mob, anim=anim, static=False))

    if use_aside and content is not None:
        aside = build_aside(aside_spec, ground, max_width=RAIL_W)
        aside.move_to([RAIL_X, content.get_center()[1], 0], aligned_edge=LEFT)
        blocks.append(Block("aside", aside, anim="fade", static=True, layer="decoration"))

    blocks.append(motif_corner(ground))
    return blocks

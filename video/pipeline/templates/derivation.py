"""derivation template -- Direction B (dark teaching frame).

A FULL-WIDTH multi-line derivation chain: the template for continuous algebraic
transformation (derivative-from-definition computations, limit-law rewrites,
identity proofs), where the narration carries the "why" of each step and the
screen gives the math the whole frame width.

This is the capacity answer to the two-column walkthrough templates: their
right column tops out around ~5 manim units of math width, while a real chain
line (e.g. the ch02 slope-from-definition computation) needs 7-9. Here a line
gets ~11.

Layout:
  eyebrow + title (scene_head; `kicker` override supported);
  optional centred prose `statement` (the problem being computed);
  the chain -- line 0 carries the LHS; every later line written in the
  "= ..." continuation style has its relation symbol x-aligned under line 0's
  (one anchor column, like a hand-written derivation); lines without the
  symbol fall back to the chain's left edge;
  the statement + chain centre vertically as one group below the title.

Reveal: statement is static; each chain line is dynamic ({show line.N}).
`anim: highlight` renders that line in the accent colour (use it for the
result line).

Capacity (sizecheck enforces the frame; the SPLIT decision is the content
layer's): ~5 fraction-height lines or ~7 single-height lines. Longer chains
are split into scenes -- see DESIGN.md "Template selection".

YAML shape:
  template: derivation
  accent: example
  title: "Slope at a Point, from the Definition"
  statement: "Find the slope of $y=x^2-3x$ at $(2,-2)$."   # optional
  align_on: "="                                            # optional, default "="
  lines:
    - "m = \\lim_{h \\to 0} \\frac{f(2+h)-f(2)}{h}"
    - "= \\lim_{h \\to 0} \\frac{(4+4h+h^2-6-3h)-(-2)}{h}"
    - { tex: "= 1", anim: highlight }
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, UL, MathTex, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T
from ._common import scene_head, motif_corner

_LINE_BUFF = 0.30


def _chain_line(tex: str, ground: str, *, role: str, rel: str) -> MathTex:
    """One chain line as MathTex with the relation symbol isolated so
    get_part_by_tex can find it for column alignment. Chain lines are pure
    math by convention (no '$'), so MathTex is always the right path --
    brand.math_line is bypassed because it cannot isolate substrings."""
    return MathTex(tex, substrings_to_isolate=[rel],
                   color=T.color(ground, role), font_size=T.fs("math"))


def _rel_left_offset(mob: MathTex, rel: str) -> float | None:
    """x-offset of the first `rel` glyph's left edge from the line's left edge,
    or None when the line does not carry the symbol."""
    try:
        part = mob.get_part_by_tex(rel)
    except Exception:
        return None
    if part is None:
        return None
    return float(part.get_left()[0]) - float(mob.get_left()[0])


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []
    head = scene_head(spec, ctx, label="[ derivation ]")
    blocks += head
    title = head[1].mobject

    content_w = T.FRAME_W - 2 * T.SIDE_GUTTER

    statement = None
    if spec.get("statement"):
        statement = brand.prose(spec["statement"], ground, size="body",
                                max_width=content_w, align="LEFT")

    rel = str(spec.get("align_on", "="))
    line_mobs: list[MathTex] = []
    anims: list[str] = []
    for entry in spec.get("lines", []):
        if isinstance(entry, dict):
            tex, anim = entry["tex"], entry.get("anim", "write")
        else:
            tex, anim = entry, "write"
        is_key = anim == "highlight"
        line_mobs.append(_chain_line(str(tex).strip(), ground,
                                     role="accent" if is_key else "math", rel=rel))
        anims.append(anim)

    parts = []
    if statement is not None:
        parts.append(statement)

    if line_mobs:
        # Horizontal: line 0's left edge is the chain origin (x=0 relative).
        # A continuation line starting at the relation symbol shifts so its
        # symbol sits exactly under line 0's; a line without the symbol (or a
        # chain whose first line lacks it) keeps the left edge.
        anchor = _rel_left_offset(line_mobs[0], rel)
        lefts = [0.0]
        for m in line_mobs[1:]:
            off = _rel_left_offset(m, rel)
            lefts.append(anchor - off if anchor is not None and off is not None else 0.0)

        # Vertical: top-anchored cursor over REAL line heights -- a fraction
        # line is ~2x a plain one, so a fixed pitch would collide (same lesson
        # as the recap_cards fix).
        y = 0.0
        for m, lx in zip(line_mobs, lefts):
            m.move_to([lx, y, 0], aligned_edge=UL)
            y -= m.height + _LINE_BUFF
        parts.append(VGroup(*line_mobs))

    # Statement + chain centre as ONE group in the zone between the title and
    # the bottom safe margin (same balance rule as definition_math). The zone
    # reaches deeper than definition_math's (+0.15 vs +0.45): a full 5-line
    # chain needs the room, and the centred chain never overlaps the corner
    # motif on the right.
    if parts:
        content = VGroup(*parts).arrange(DOWN, buff=0.55)
        zone_top = title.get_bottom()[1] - 0.55
        zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.15
        content.move_to([0, (zone_top + zone_bottom) / 2, 0])

    if statement is not None:
        blocks.append(Block("statement", statement, anim="fade", static=True))
    for i, (mob, anim) in enumerate(zip(line_mobs, anims)):
        blocks.append(Block(f"line.{i}", mob, anim=anim, static=False))

    blocks.append(motif_corner(ground))
    return blocks

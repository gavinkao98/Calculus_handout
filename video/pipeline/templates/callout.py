"""callout template -- Lectern dark teaching frame. Remark / Caution / Note.

The recurring named aside the handouts use constantly ((fg)'!=f'g', f^{-1}!=1/f,
power-rule domain, ...). One template, colour-swapped by `type`:
  remark -> blue, caution -> red, note -> amber.

REDESIGN (2026-06-29): dropped the centred card panel + glyph box. A callout now
reads like every other teaching frame -- the shared `scene_head` masthead (eyebrow
`[ CAUTION 1.1 ]` in the type colour + the scene title), the centrally-added navy
spine with a TYPE-COLOURED cap (see templates.build_blocks), and the body flowing
LEFT-FLUSH BELOW the title (place_body, upper-bias), exactly as definition_math does.
The type is signalled by colour (eyebrow + spine cap + bullet markers) and the eyebrow
word -- no box. (The accent colour is wired by setting spec["accent"]=type up front so
BOTH this template's scene_head AND the central scene_spine read the right role.)

YAML shape:
  template: callout
  type: caution            # remark | caution | note   (default caution)
  number: "1.1"            # optional -> folded into the eyebrow label
  title: "A Notation Trap" # rendered as the masthead title
  body: "..."              # a string -> prose;  a LIST -> bullet rows (type-colour dot)
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT, Dot, VGroup

from .. import brand
from ..blocks import Block, accent_role
from ..visuals import theme as T
from ._common import (scene_head, motif_corner, place_body, ColumnPlan,
                      SPINE_X, CONTENT_W)

_TYPES = ("remark", "caution", "note")
_TYPE_LABEL = {"remark": "remark", "caution": "caution", "note": "note"}


def capacity_meta(spec: dict[str, Any]) -> list[ColumnPlan]:
    """Capacity contract (L2): like definition_math, the callout places a single
    left-flush block (prose or bullet rows) at a fixed rhythm and place_body only
    POSITIONS it (no fill expansion). Measure its actual span, not a min-pitch estimate,
    so the predictive split audit covers callouts too (was excluded as a card scene)."""
    return [ColumnPlan(min_pitch=0.0, model="span")]


def _bullets(items: list, ground: str, role: str) -> VGroup:
    """A stacked bullet list: each row is a small type-colour dot aligned to the first
    text line + the item prose (left-flush). Returns the rows as one left-aligned group."""
    ref = brand.prose("X", ground, role="primary", size="prose")
    radius = ref.height * 0.13
    measure = CONTENT_W - 0.5                      # leave room for the dot + its gap
    rows = []
    for item in items:
        text = brand.prose(str(item), ground, role="primary", size="prose",
                           max_width=measure, align="LEFT")
        dot = Dot(radius=radius, color=T.color(ground, role))
        dot.next_to(text, LEFT, buff=0.3)
        # drop the dot from the block's vertical centre to the FIRST line's centre
        dot.move_to([dot.get_x(), text.get_top()[1] - ref.height / 2, 0])
        rows.append(VGroup(dot, text))
    return VGroup(*rows).arrange(DOWN, buff=T.ROW_GAP, aligned_edge=LEFT)


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    ctype = str(spec.get("type", "caution")).lower()
    if ctype not in _TYPES:
        ctype = "caution"

    # Wire the accent family from `type` so BOTH scene_head (below) and the centrally
    # added scene_spine (templates.build_blocks, after this returns) colour to the type.
    # ACCENT_ROLE already maps caution->warning / remark->secondary / note->accent.
    spec["accent"] = ctype
    role = accent_role(spec)

    label = _TYPE_LABEL[ctype]
    if spec.get("number"):
        label = f"{label} {spec['number']}"
    blocks: list[Block] = scene_head(spec, ctx, label=f"[ {label} ]")
    title = next(b.mobject for b in blocks if b.id == "title")

    body_spec = spec.get("body", "")
    if isinstance(body_spec, (list, tuple)):
        content = _bullets(list(body_spec), ground, role)
        anim = "fade"
    else:
        content = brand.prose(str(body_spec), ground, role="primary", size="prose",
                              max_width=CONTENT_W, align="LEFT")
        anim = "write"

    place_body(content, title, SPINE_X)
    blocks.append(Block("body", content, anim=anim, static=False))
    blocks.append(motif_corner(ground))
    return blocks

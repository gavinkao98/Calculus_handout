"""divider template -- Direction D chapter / section opener (also the video intro).

A full-frame opener on the dark teaching ground: a faint glowing hero curve sweeps
bottom-left -> top-right and bleeds off the right; a huge ghost numeral (5% opacity)
sits right; left-stacked and vertically centred are a mono eyebrow, a big title, an
optional one-line subtitle, and a progress-dots row (first dot elongated + accent).

Silent like intro/outro (kind: divider). YAML shape:
  - id: divider
    kind: divider
    accent: definition           # optional -> dot/eyebrow hue (default blue)
    eyebrow: "Chapter 2"         # or `kicker`; falls back to "Section {section}"
    title: "Derivatives"
    subtitle: "How fast is it changing --- and what the slope really means."
    ghost: "2"                   # the huge background numeral (default: chapter number)
    progress: { current: 1, total: 5 }   # optional dots; falls back to meta.sections
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT, UP, VGroup

from .. import brand
from ..blocks import Block, accent_role
from ..visuals import theme as T


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx.get("ground", "dark")
    meta = ctx["meta"]
    role = accent_role(spec)
    left_x = -T.FRAME_W / 2 + T.SIDE_GUTTER
    content_w = T.FRAME_W - 2 * T.SIDE_GUTTER
    blocks: list[Block] = []

    # huge faint ghost numeral on the right, behind everything
    section = str(meta.get("section", ""))
    ghost_text = str(spec.get("ghost", section.split(".")[0] if section else ""))
    if ghost_text:
        ghost = brand.ghost_numeral(ghost_text, ground)
        ghost.move_to([T.FRAME_W / 2 - T.SIDE_GUTTER - ghost.width / 2, 0, 0])
        blocks.append(Block("ghost", ghost, anim="fade", static=True, layer="background"))

    # glowing hero curve bleeding off the right
    curve = brand.hero_curve(ground, role="secondary")
    blocks.append(Block("curve", curve, anim="create", static=True, layer="decoration"))

    # left-stacked, vertically centred content
    eyebrow_text = spec.get("kicker") or spec.get("eyebrow") or (f"Section {section}" if section else "")
    eyebrow = brand.eyebrow(eyebrow_text, ground, role=role)
    title = brand.heading_rich(str(spec.get("title", meta.get("title", ""))), ground,
                               role="primary", size=92, max_width=content_w * 0.72)

    sub = spec.get("subtitle") or spec.get("sub") or spec.get("tagline")
    subtitle = None
    if sub:
        subtitle = brand.prose(str(sub), ground, role="text", size=40,
                               max_width=content_w * 0.62, align="LEFT")

    prog = spec.get("progress") or {}
    sections = meta.get("sections") or []
    total = int(prog.get("total", len(sections) or 1))
    if "current" in prog:
        current = int(prog["current"])
    else:
        ids = [str(s.get("id", "")) for s in sections]
        current = (ids.index(section) + 1) if section in ids else 1
    dots = brand.progress_dots(current, max(total, current), ground, role=role)

    # left-flush vstack, anchored to the title then vertically centred in the frame
    eyebrow.next_to(title, UP, buff=0.34).align_to(title, LEFT)
    below = title
    if subtitle is not None:
        subtitle.next_to(title, DOWN, buff=0.42).align_to(title, LEFT)
        below = subtitle
    dots.next_to(below, DOWN, buff=0.6).align_to(title, LEFT)
    members = [eyebrow, title] + ([subtitle] if subtitle is not None else []) + [dots]
    stack = VGroup(*members)
    stack.move_to([left_x + stack.width / 2, 0, 0])

    blocks.append(Block("eyebrow", eyebrow, anim="fade", static=True))
    blocks.append(Block("title", title, anim="fade", static=True))
    if subtitle is not None:
        blocks.append(Block("subtitle", subtitle, anim="fade", static=True))
    blocks.append(Block("dots", dots, anim="fade", static=True))

    motif = brand.summit_bars(ground, height=0.45, color_role="muted", opacity=0.4)
    motif.move_to([T.FRAME_W / 2 - T.SAFE_MARGIN - motif.width / 2,
                   -T.FRAME_H / 2 + T.SAFE_MARGIN + motif.height / 2, 0])
    blocks.append(Block("motif", motif, anim="fade", static=True, layer="decoration"))
    return blocks

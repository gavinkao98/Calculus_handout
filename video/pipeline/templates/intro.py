"""intro template -- reusable Section Gate opener.

Every section video opens with the same orientation pattern:
1. Chapter map: show all sections in the chapter.
2. Focus: mark the current section in that map.
3. Section Gate: fade to the familiar logo / section / title / tagline slate.

The map reads from ``meta.sections`` and highlights ``meta.section``. If a new
storyboard omits the chapter map metadata, the template gracefully falls back to
the current section only.
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT, RIGHT, Rectangle, RoundedRectangle, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T


def _sections(meta: dict[str, Any]) -> list[dict[str, str]]:
    items = meta.get("sections") or []
    if not items:
        return [{"id": str(meta.get("section", "")), "title": str(meta.get("title", ""))}]
    return [{"id": str(item.get("id", "")), "title": str(item.get("title", ""))} for item in items]


def _chapter_map(spec: dict[str, Any], meta: dict[str, Any], ground: str) -> list[Block]:
    blocks: list[Block] = []
    section = str(meta.get("section", ""))
    chapter = str(meta.get("chapter", "Chapter"))
    chapter_title = str(meta.get("chapter_title", ""))
    left = -T.FRAME_W / 2 + T.SIDE_GUTTER
    top = T.FRAME_H / 2 - T.SAFE_MARGIN

    eyebrow = brand.eyebrow("course map", ground, role="accent")
    title = brand.heading(chapter, ground, role="heading", size="h2")
    subtitle = brand.body_text(chapter_title, ground, role="subtitle", size="intro_subtitle",
                               max_width=T.FRAME_W - 2 * T.SIDE_GUTTER)
    header = VGroup(eyebrow, title, subtitle).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    header.move_to([left, top - header.height / 2 - 0.1, 0], aligned_edge=LEFT)
    blocks.append(Block("map.header", header, anim="fade", static=False))

    rows = []
    focus_row = None
    for item in _sections(meta):
        is_current = item["id"] == section
        num = brand.eyebrow(item["id"], ground, role="accent" if is_current else "muted")
        dot = brand.plot_dot(ground, role="accent" if is_current else "muted",
                             r=0.065 if is_current else 0.045)
        label = brand.body_text(item["title"], ground,
                                role="heading" if is_current else "text",
                                size="step", max_width=8.6)
        row = VGroup(num, dot, label).arrange(RIGHT, buff=0.28)
        if is_current:
            focus = RoundedRectangle(
                corner_radius=0.08,
                width=max(row.width + 0.75, 6.2),
                height=row.height + 0.36,
                stroke_color=T.color(ground, "accent"),
                stroke_width=2.0,
                fill_color="#ffffff",
                fill_opacity=0.38,
            )
            focus.move_to(row.get_center())
            row = VGroup(focus, row)
            focus_row = row
        rows.append(row)

    row_group = VGroup(*rows).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    row_group.move_to([left + 0.25, 0.0, 0], aligned_edge=LEFT)
    blocks.append(Block("map.sections", row_group, anim="fade", static=False))

    if focus_row is not None:
        scan = brand.hrule(focus_row.width + 0.2, ground, role="accent", stroke=3)
        scan.next_to(focus_row, DOWN, buff=0.14).align_to(focus_row, LEFT)
        blocks.append(Block("map.focus", scan, anim="grow", static=False))

    return blocks


def _section_gate(spec: dict[str, Any], meta: dict[str, Any], ground: str) -> list[Block]:
    section = str(meta.get("section", ""))
    title = str(meta.get("title", ""))
    tagline = spec.get("tagline", "")
    content_w = T.FRAME_W - 2 * T.SIDE_GUTTER

    logo = brand.logo_lockup(height=1.45)
    eyebrow = brand.eyebrow(f"// section {section}", ground, role="accent")
    headline = brand.heading(title, ground, role="heading", size="intro_headline",
                             max_width=content_w)

    items = [logo, eyebrow, headline]
    if tagline:
        items.append(brand.body_text(tagline, ground, role="subtitle", size="intro_subtitle",
                                     max_width=content_w, align="CENTER"))
    group = VGroup(*items).arrange(DOWN, buff=0.48).move_to([0, 0.02, 0])

    blocks: list[Block] = []
    for i, mob in enumerate(group):
        anim = "write_glow" if mob is headline else "fade"
        blocks.append(Block(f"gate.{i}", mob, anim=anim, static=False))
    return blocks


def _dark_handoff(meta: dict[str, Any]) -> list[Block]:
    ground = "dark"
    section = str(meta.get("section", ""))
    title = str(meta.get("title", ""))

    dark_bg = Rectangle(
        width=T.FRAME_W,
        height=T.FRAME_H,
        stroke_width=0,
        fill_color=T.color(ground, "bg"),
        fill_opacity=1.0,
    )
    dark_grid = dark_bg
    eyebrow = brand.eyebrow(f"section {section}", ground, role="secondary")
    headline = brand.heading(title, ground, role="primary", size="h1",
                             max_width=T.FRAME_W - 2 * T.SIDE_GUTTER)
    rule = brand.heading_rule(2.4, ground, role="secondary")
    marker = VGroup(eyebrow, headline, rule).arrange(DOWN, buff=0.22)
    marker.move_to([0, 0.08, 0])

    motif = brand.summit_bars(ground, height=0.45, color_role="muted", opacity=0.38)
    motif.move_to([T.FRAME_W / 2 - T.SAFE_MARGIN - motif.width / 2,
                   -T.FRAME_H / 2 + T.SAFE_MARGIN + motif.height / 2, 0])

    return [
        Block("transition.ground", dark_grid, anim="fade", static=False),
        Block("transition.marker", marker, anim="fade", static=False),
        Block("transition.motif", motif, anim="fade", static=False),
    ]


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = "light"
    meta = ctx["meta"]
    blocks: list[Block] = []
    blocks.extend(_chapter_map(spec, meta, ground))
    blocks.extend(_section_gate(spec, meta, ground))
    blocks.extend(_dark_handoff(meta))
    return blocks

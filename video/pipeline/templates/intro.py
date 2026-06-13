"""intro template -- reusable Section Gate opener (pulse-timeline variant).

Every section video opens with the same three-stage pattern:
1. Brand opening: logo lockup + section number / title / tagline on light ground.
2. Pulse timeline: vertical chapter map with a light pulse that scans from
   top to the current section, which enlarges on hit. Rail endpoints are
   fixed; node spacing scales proportionally with section count (max 8).
3. Dark handoff: gradual light-to-dark crossfade, then section marker + summit
   bars on dark ground -- ready for the first teaching scene.

The timeline reads from ``meta.sections`` and highlights ``meta.section``. If
the storyboard omits the chapter map metadata, the template falls back to the
current section only.
"""
from __future__ import annotations

from typing import Any

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    Circle,
    Line,
    Rectangle,
    VGroup,
)

from .. import brand
from ..blocks import Block
from ..visuals import theme as T


def _sections(meta: dict[str, Any]) -> list[dict[str, str]]:
    items = meta.get("sections") or []
    if not items:
        return [{"id": str(meta.get("section", "")), "title": str(meta.get("title", ""))}]
    return [{"id": str(item.get("id", "")), "title": str(item.get("title", ""))} for item in items]


# -- stage 1: brand opening ------------------------------------------------

def _brand_opening(spec: dict[str, Any], meta: dict[str, Any], ground: str) -> list[Block]:
    logo = brand.logo_lockup_outlined(height=1.45)
    logo.move_to([0, 0, 0])
    return [Block("brand.0", logo, anim="fade", static=False)]


# -- stage 2: pulse timeline -----------------------------------------------

def _pulse_timeline(spec: dict[str, Any], meta: dict[str, Any], ground: str) -> list[Block]:
    blocks: list[Block] = []
    section = str(meta.get("section", ""))
    chapter = str(meta.get("chapter", "Chapter"))
    chapter_title = str(meta.get("chapter_title", ""))
    sections = _sections(meta)

    # -- layout constants for vertical timeline --
    rail_x = -T.FRAME_W / 2 + T.SIDE_GUTTER + 0.8
    label_max_w = T.FRAME_W - 2 * T.SIDE_GUTTER - 2.0
    RAIL_TOP = 1.8
    RAIL_BOTTOM = -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.3

    # header: eyebrow + "Chapter 1  Inverse Functions and Limits" on one line
    eyebrow = brand.eyebrow("course map", ground, role="accent")
    title = brand.heading(chapter, ground, role="heading", size="h2")
    subtitle = brand.body_text(chapter_title, ground, role="subtitle", size="intro_subtitle",
                               max_width=label_max_w)
    title_row = VGroup(title, subtitle).arrange(RIGHT, buff=0.35)
    header = VGroup(eyebrow, title_row).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    header.move_to([rail_x, T.FRAME_H / 2 - header.height / 2 - T.SAFE_MARGIN - 0.1, 0],
                   aligned_edge=LEFT)
    blocks.append(Block("timeline.header", header, anim="fade", static=False))

    n = len(sections)
    if n == 1:
        center_y = (RAIL_TOP + RAIL_BOTTOM) / 2
        top_y = center_y
        bottom_y = center_y
        row_gap = 0.0
    else:
        top_y = RAIL_TOP
        bottom_y = RAIL_BOTTOM
        row_gap = (top_y - bottom_y) / (n - 1)

    # vertical rail line
    rail = Line(
        [rail_x, top_y, 0], [rail_x, bottom_y, 0],
        stroke_color=T.color(ground, "muted"),
        stroke_width=2.0,
    )
    rail.set_opacity(0.5)

    # all dots (muted) + section numbers only — no titles
    nodes = VGroup()
    focus_idx = 0
    focus_num = None
    for i, item in enumerate(sections):
        is_current = item["id"] == section
        if is_current:
            focus_idx = i
        y = top_y - i * row_gap

        dot = Circle(
            radius=0.06,
            stroke_color=T.color(ground, "muted"),
            stroke_width=1.5,
            fill_color=T.color(ground, "muted"),
            fill_opacity=0.3,
        )
        dot.move_to([rail_x, y, 0])

        num = brand.eyebrow(item["id"], ground, role="muted")
        num.scale(0.85)
        num.next_to(dot, RIGHT, buff=0.25)

        if is_current:
            focus_num = num

        node = VGroup(dot, num)
        nodes.add(node)

    rail_group = VGroup(rail, nodes)
    blocks.append(Block("timeline.rail", rail_group, anim="fade", static=False))

    # pulse line from top to current node (skip if current is at top)
    pulse_y = top_y - focus_idx * row_gap
    if focus_idx > 0:
        pulse = Line(
            [rail_x, top_y, 0], [rail_x, pulse_y, 0],
            stroke_color=T.color(ground, "accent"),
            stroke_width=3.5,
        )
        blocks.append(Block("timeline.pulse", pulse, anim="create", static=False))

    # activate: morph the gray dot in-place to accent color
    focus_dot = nodes[focus_idx][0]

    def _activate(scene, _mob, ground):
        accent = T.color(ground, "accent")
        scene.play(
            focus_dot.animate.set_fill(accent, opacity=1.0).set_stroke(accent, width=2.5),
            run_time=0.5,
        )
        return 0.5

    blocks.append(Block("timeline.activate", VGroup(), anim=_activate, static=False))

    # current section title — revealed after dot activates
    current_title = brand.body_text(
        sections[focus_idx]["title"], ground,
        role="heading", size="step",
        max_width=label_max_w,
    )
    current_title.scale(0.9)
    if focus_num is not None:
        current_title.next_to(focus_num, RIGHT, buff=0.2)
    blocks.append(Block("timeline.title", current_title, anim="create", static=False))

    return blocks


# -- stage 3: dark handoff (with gradual crossfade) -------------------------

def _dark_handoff(spec: dict[str, Any], meta: dict[str, Any]) -> list[Block]:
    ground = "dark"
    section = str(meta.get("section", ""))
    title = str(meta.get("title", ""))
    tagline = spec.get("tagline", "")

    dark_bg = Rectangle(
        width=T.FRAME_W,
        height=T.FRAME_H,
        stroke_width=0,
        fill_color=T.color(ground, "bg"),
        fill_opacity=1.0,
    )
    eyebrow = brand.eyebrow(f"section {section}", ground, role="secondary")
    headline = brand.heading(title, ground, role="primary", size="h1",
                             max_width=T.FRAME_W - 2 * T.SIDE_GUTTER)
    rule = brand.heading_rule(2.4, ground, role="secondary")
    items = [eyebrow, headline, rule]
    if tagline:
        tag = brand.body_text(tagline, ground, role="text", size="intro_subtitle",
                              max_width=T.FRAME_W - 2 * T.SIDE_GUTTER, align="CENTER")
        items.append(tag)
    marker = VGroup(*items).arrange(DOWN, buff=0.22)
    marker.move_to([0, 0.08, 0])

    motif = brand.summit_bars(ground, height=0.45, color_role="muted", opacity=0.38)
    motif.move_to([T.FRAME_W / 2 - T.SAFE_MARGIN - motif.width / 2,
                   -T.FRAME_H / 2 + T.SAFE_MARGIN + motif.height / 2, 0])

    return [
        Block("transition.ground", dark_bg, anim="fade", static=False),
        Block("transition.marker", marker, anim="fade", static=False),
        Block("transition.motif", motif, anim="fade", static=False),
    ]


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = "light"
    meta = ctx["meta"]
    blocks: list[Block] = []
    blocks.extend(_brand_opening(spec, meta, ground))
    blocks.extend(_pulse_timeline(spec, meta, ground))
    blocks.extend(_dark_handoff(spec, meta))
    return blocks

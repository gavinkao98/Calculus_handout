"""outro template -- Direction B (light final brand slate).

Two-stage: dark-to-light bridge, then the final brand slate.
Takeaways belong in the preceding recap content scene (with narration),
not in the outro.
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, Rectangle, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T


def _format_meta(text: str, meta: dict[str, Any]) -> str:
    return text.format(
        section=str(meta.get("section", "")),
        title=str(meta.get("title", "")),
        id=str(meta.get("id", "")),
    )


def _dark_landing_stage(ctx: dict[str, Any]) -> list[Block]:
    meta = ctx["meta"]
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
    dark_ground = dark_bg

    eyebrow = brand.eyebrow(f"section {section} complete", ground, role="secondary")
    headline = brand.heading(title, ground, role="primary", size="h1")
    rule = brand.heading_rule(2.4, ground, role="secondary")
    marker = VGroup(eyebrow, headline, rule).arrange(DOWN, buff=0.22)
    marker.move_to([0, 0.08, 0])

    motif = brand.summit_bars(ground, height=0.45, color_role="muted", opacity=0.38)
    motif.move_to([T.FRAME_W / 2 - T.SAFE_MARGIN - motif.width / 2,
                   -T.FRAME_H / 2 + T.SAFE_MARGIN + motif.height / 2, 0])

    return [
        Block("transition.ground", dark_ground, anim="fade", static=True),
        Block("transition.marker", marker, anim="fade", static=False),
        Block("transition.motif", motif, anim="fade", static=False),
    ]



def _end_slate_stage(spec: dict[str, Any], ctx: dict[str, Any], ground: str) -> list[Block]:
    meta = ctx["meta"]
    end = spec.get("end_slate", {}) or {}
    label = _format_meta(str(end.get("label", "end of section {section}")), meta)
    title = _format_meta(str(end.get("title", "{title}")), meta)
    logo_height = float(end.get("logo_height", 1.55))

    logo = brand.logo_lockup_outlined(height=logo_height)
    end_label = brand.eyebrow(label, ground, role="accent")
    end_title = brand.heading(title, ground, role="heading", size="h2")
    end_rule = brand.heading_rule(2.8, ground, role="accent")

    slate = VGroup(logo, end_rule, end_label, end_title).arrange(DOWN, buff=0.38)
    slate.move_to([0, 0.08, 0])

    return [
        Block("end.logo", logo, anim="fade", static=False),
        Block("end.rule", end_rule, anim="grow", static=False),
        Block("end.label", end_label, anim="fade", static=False),
        Block("end.title", end_title, anim="fade", static=False),
    ]


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = "light"
    blocks: list[Block] = []
    blocks.extend(_dark_landing_stage(ctx))
    blocks.extend(_end_slate_stage(spec, ctx, ground))
    return blocks

"""outro template -- Direction D paper end slate.

A single warm-paper brand slate: NTU logo lockup, a brand-red rule, a red mono
"END OF SECTION x.x" label, the navy section title, and a small red "> Next sx.x"
hint. (The old dark landing stage is gone -- the redesign ends on one paper frame.)
Takeaways belong in the preceding recap content scene, not here.

YAML shape:
  - id: outro
    kind: outro
    end_slate:                    # all optional
      label: "end of section {section}"
      title: "{title}"
      logo_height: 1.3
    next_section: "1.2"           # optional -> the "> Next §1.2 ..." hint
    next_title: "Inverse Trigonometric Functions"
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, RIGHT, Polygon, Rectangle, Text, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T


def _format_meta(text: str, meta: dict[str, Any]) -> str:
    return text.format(section=str(meta.get("section", "")),
                       title=str(meta.get("title", "")), id=str(meta.get("id", "")))


def _caret(ground: str):
    """A small right-pointing brand-red triangle (the > Next marker)."""
    s = 0.13
    tri = Polygon([-s * 0.7, s, 0], [-s * 0.7, -s, 0], [s * 0.8, 0, 0],
                  color=T.color(ground, "brand_red"),
                  fill_color=T.color(ground, "brand_red"), fill_opacity=1.0, stroke_width=0)
    return tri


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = "light"
    meta = ctx["meta"]
    end = spec.get("end_slate", {}) or {}
    blocks: list[Block] = []

    # full-frame warm paper ground (covers the prior dark teaching frame at compose)
    bg = Rectangle(width=T.FRAME_W, height=T.FRAME_H, stroke_width=0,
                   fill_color=T.color(ground, "bg"), fill_opacity=1.0)
    blocks.append(Block("ground", bg, anim="fade", static=True, layer="background"))

    logo = brand.logo_lockup_outlined(height=float(end.get("logo_height", 1.3)))
    rule = brand.hrule(0.9, ground, role="accent", stroke=4.0)
    label = brand.eyebrow(_format_meta(str(end.get("label", "end of section {section}")), meta),
                          ground, role="accent")
    title = brand.heading(_format_meta(str(end.get("title", "{title}")), meta), ground,
                          role="heading", size=72, max_width=T.FRAME_W - 2 * T.SIDE_GUTTER)

    slate = VGroup(logo, rule, label, title)
    slate.arrange(DOWN, buff=0.0)
    # bespoke gaps (logo->rule s6, rule->label s5, label->title small, then the hint)
    rule.next_to(logo, DOWN, buff=0.48)
    label.next_to(rule, DOWN, buff=0.32)
    title.next_to(label, DOWN, buff=0.18)
    slate = VGroup(logo, rule, label, title)

    parts = [slate]
    next_section = spec.get("next_section") or end.get("next_section")
    next_title = spec.get("next_title") or end.get("next_title")
    hint = None
    if next_section:
        caret = _caret(ground)
        nxt = Text("Next", font=T.FONT_BODY, font_size=T.fs("caption"), color=T.color(ground, "muted"))
        sec = brand.eyebrow(f"§{next_section}", ground, role="accent")
        ntitle = Text(str(next_title or ""), font=T.FONT_BODY, weight="SEMIBOLD",
                      font_size=T.fs("caption"), color=T.color(ground, "text"))
        hint = VGroup(caret, nxt, sec, ntitle).arrange(RIGHT, buff=0.22)
        parts.append(hint)

    group = VGroup(*parts).arrange(DOWN, buff=0.64)
    group.move_to([0, 0.05, 0])

    blocks.append(Block("end.logo", logo, anim="fade", static=False))
    blocks.append(Block("end.rule", rule, anim="fade", static=False))
    blocks.append(Block("end.label", label, anim="fade", static=False))
    blocks.append(Block("end.title", title, anim="fade", static=False))
    if hint is not None:
        blocks.append(Block("end.next", hint, anim="fade", static=False))

    motif = brand.summit_bars(ground, height=0.45, color_role="muted", opacity=0.5)
    motif.move_to([T.FRAME_W / 2 - T.SAFE_MARGIN - motif.width / 2,
                   -T.FRAME_H / 2 + T.SAFE_MARGIN + motif.height / 2, 0])
    blocks.append(Block("motif", motif, anim="fade", static=True, layer="decoration"))
    return blocks

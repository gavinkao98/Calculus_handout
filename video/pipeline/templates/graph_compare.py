"""graph_compare template -- two graph panels side by side.

The comparison IS the teaching move this template serves: one-to-one vs not
(the horizontal line test), f vs f', continuous vs broken, converges vs
diverges. Before this template the dual-panel layout had to be hand-built in
a hook (~90 lines for the §1.1 line-test scene, most of it panel plumbing);
now the panels are payload and a hook only carries actual animation.

Each of `left` / `right` takes the SAME plot payload as graph_focus
(function / line / point / band, ticks, `reveal: true`), drawn on its own
small axes. Under each panel an optional `caption` (prose, may carry $math$)
with an optional `verdict: ok | bad` -> a green check / coral cross beside it.

Layout: graph-family scene, so a graph_focus-style title (no eyebrow); the
two panels centre in the band between title and captions; optional bottom
`annotations` exactly like graph_focus.

Reveal: panel graphics are static frame by default; a plot marked
`reveal: true` waits for {show left.plot.N} / {show right.plot.N}; each
caption (with its verdict glyph) waits for {show caption.left} /
{show caption.right}; annotations are {show annotation.N}.

YAML shape:
  template: graph_compare
  accent: example
  title: "One Output per Height?"
  left:
    axes: { x_range: [-1.45, 1.45, 0.5], y_range: [-1.95, 1.95, 0.5] }
    plots:
      - { kind: function, expression: "x**3", label: "$y=x^3$" }
    caption: "Every horizontal line crosses once."
    verdict: ok
  right: { ... }
  annotations: ["..."]      # optional
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, RIGHT, Axes, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T
from . import graph_focus as gf
from ._common import motif_corner

_PANEL_GAP = 1.2          # air between the two panels
_TITLE_PANEL_GAP = 0.45
_PANEL_CAPTION_GAP = 0.35
_VERDICT = {"ok": ("check", "success"), "bad": ("cross", "warning")}


def _panel(side_spec: dict[str, Any], ground: str, prefix: str) -> tuple[list[Block], VGroup]:
    """Build one panel's axes + plots, ids prefixed left./right. -- reuses the
    graph_focus plot machinery, so plot kinds and `reveal: true` behave
    identically to a full-frame graph scene."""
    ac = {
        "x_range": [-1.45, 1.45, 0.5],
        "y_range": [-0.28, 1.55, 0.25],
        **side_spec.get("axes", {}),
    }
    side = dict(side_spec)
    side["axes"] = ac
    axes = Axes(
        x_range=gf._range(ac["x_range"], 0.5),
        y_range=gf._range(ac["y_range"], 0.25),
        x_length=float(ac.get("x_length", 4.6)),
        y_length=float(ac.get("y_length", 3.2)),
        tips=False,
        axis_config={
            "color": T.color(ground, "text"),
            "stroke_width": 2.0,
            "include_ticks": False,
            "include_numbers": False,
        },
    )
    if bool(ac.get("tips", True)):
        axes.x_axis.add_tip(tip_length=0.14, tip_width=0.14)
        axes.y_axis.add_tip(tip_length=0.14, tip_width=0.14)

    panel_blocks: list[Block] = [Block("axes", axes, anim="create", static=True)]
    plot_blocks, _ = gf._plot_blocks(side, axes, ground)
    panel_blocks += plot_blocks
    ticks = gf._axis_ticks(axes, ac, ground)
    if ticks is not None:
        panel_blocks.append(Block("ticks", ticks, anim="fade", static=True))
    for b in panel_blocks:
        b.id = f"{prefix}.{b.id}"
        b.layer = "graph"
    group = VGroup(*[b.mobject for b in panel_blocks])
    return panel_blocks, group


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []

    title = gf._title(spec.get("title", ""), ground)
    left_edge = -T.FRAME_W / 2 + T.SAFE_MARGIN
    top = T.FRAME_H / 2 - T.SAFE_MARGIN
    title.move_to([left_edge + title.width / 2, top - title.height / 2, 0])
    blocks.append(Block("title", title, anim="fade", static=True))

    content_w = T.FRAME_W - 2 * T.SIDE_GUTTER
    half_w = (content_w - _PANEL_GAP) / 2
    centers = {"left": -(half_w / 2 + _PANEL_GAP / 2), "right": half_w / 2 + _PANEL_GAP / 2}

    # -- bottom annotations (graph_focus rules: prose, wraps, never shrinks) --
    annotations = []
    for entry in spec.get("annotations", []):
        text = entry.get("text", "") if isinstance(entry, dict) else str(entry)
        ann = brand.prose(text, ground, role="text", size="step",
                          max_width=content_w, align="LEFT")
        annotations.append(ann)
    ann_group = None
    if annotations:
        ann_group = VGroup(*annotations).arrange(DOWN, buff=0.25)
        ann_group.move_to([0, -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.25, 0])

    # -- captions reserve their band above the annotations --------------------
    captions: dict[str, VGroup] = {}
    cap_h = 0.0
    for key in ("left", "right"):
        side_spec = spec.get(key, {}) or {}
        if not side_spec.get("caption"):
            continue
        cap = brand.prose(side_spec["caption"], ground, role="text", size="step",
                          max_width=half_w - 0.2, align="CENTER")
        parts = [cap]
        verdict = str(side_spec.get("verdict", "")).lower()
        if verdict in _VERDICT:
            name, vrole = _VERDICT[verdict]
            gm = brand.glyph(name, ground, role=vrole, size="math_sm")
            gm.next_to(cap, RIGHT, buff=0.25)
            parts.append(gm)
        grp = VGroup(*parts)
        captions[key] = grp
        cap_h = max(cap_h, grp.height)

    if ann_group is not None:
        cap_y = ann_group.get_top()[1] + _PANEL_CAPTION_GAP + cap_h / 2
    else:
        cap_y = -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.3 + cap_h / 2
    for key, grp in captions.items():
        grp.move_to([centers[key], cap_y, 0])

    # -- panels fill the band between title and captions ----------------------
    zone_top = title.get_bottom()[1] - _TITLE_PANEL_GAP
    if captions:
        zone_bottom = cap_y + cap_h / 2 + _PANEL_CAPTION_GAP
    elif ann_group is not None:
        zone_bottom = ann_group.get_top()[1] + _PANEL_CAPTION_GAP
    else:
        zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.75
    zone_h = max(zone_top - zone_bottom, 1.5)

    for key in ("left", "right"):
        side_spec = spec.get(key, {}) or {}
        panel_blocks, group = _panel(side_spec, ground, key)
        scale = min(half_w / group.width, zone_h / group.height, 1.0)
        if scale < 1.0:
            group.scale(scale)
        group.move_to([centers[key], (zone_top + zone_bottom) / 2, 0])
        blocks.extend(panel_blocks)

    for key, grp in captions.items():
        blocks.append(Block(f"caption.{key}", grp, anim="fade", static=False))
    if ann_group is not None:
        for i, ann in enumerate(annotations):
            blocks.append(Block(f"annotation.{i}", ann, anim="fade", static=False))

    blocks.append(motif_corner(ground))
    return blocks

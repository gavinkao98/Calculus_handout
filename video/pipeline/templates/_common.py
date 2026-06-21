"""Shared template helpers for Direction B dark teaching frames.

scene_head: the eyebrow tag + title block every teaching template opens with
(mirrors B_SceneHead in the design, minus the grid -- grids are disabled
project-wide, see theme.SHOW_GRID). Returns a list[Block] (eyebrow, title) all
static.

motif_corner: the faint summit-bars mark bottom-right.

These exist so the six dark templates don't each re-implement the same header.
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT

from .. import brand
from ..blocks import Block, accent_role
from ..visuals import theme as T


def body_zone(title) -> tuple[float, float]:
    """(zone_top, zone_bottom) y-coords of the body area under *title* -- the band
    place_body centres content into. Shared so templates can size content to it."""
    return (title.get_bottom()[1] - T.TITLE_GAP, -T.FRAME_H / 2 + T.SAFE_MARGIN)


def fill_gap(heights: list[float], base_buff: float, zone_h: float, *,
             fill_frac: float | None = None, cap_mult: float = 1.5) -> float:
    """Inter-row buff that spreads short content to ~fill_frac of the body zone.

    Short content (a 3-line definition, a 4-step chain) leaves a dead band under the
    title AND an empty lower third. Pulling it up only swaps which band is empty, so
    instead we open the gaps between rows until the block occupies ~fill_frac*zone_h,
    then centre as usual -- the block reads as filling the frame rather than floating.
    Returns base_buff unchanged once content already meets the target (tall content),
    and never adds more than cap_mult*base_buff per gap (so rows never fly apart).
    """
    if fill_frac is None:
        fill_frac = T.BODY_FILL_FRAC
    n = len(heights)
    if n < 2:
        return base_buff
    natural = sum(heights) + (n - 1) * base_buff
    target = fill_frac * zone_h
    if natural >= target:
        return base_buff
    add = (target - natural) / (n - 1)
    return base_buff + min(add, base_buff * cap_mult)


def place_body(content, title, left_x: float, *, top_gap_max: float | None = None):
    """Position a left-flush content group in the body zone below *title*.

    The body zone is (title bottom - TITLE_GAP) down to the bottom safe margin.
    Pure vertical centring in that zone drifts short content to ~y=-0.6 (below the
    frame centre), reading as disconnected from the title -- the old "dead band
    above the content" we kept hitting. Instead we centre, then CLAMP the gap
    between the title and the content top to *top_gap_max*: short content lifts to
    near the frame centre (a touch high, to stay anchored to the title), medium
    content centres, and tall content that needs the room still fills the full zone.
    A bottom guard keeps over-tall content inside the safe margin. Mutates and
    returns *content*. (top_gap_max default BODY_TOP_GAP_MAX was tuned 0.71->1.0
    after a gate-1 audit found 0.71 left short scenes reading top-heavy.)
    """
    if top_gap_max is None:
        top_gap_max = T.BODY_TOP_GAP_MAX
    zone_top = title.get_bottom()[1] - T.TITLE_GAP
    zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN
    center_y = (zone_top + zone_bottom) / 2
    half = content.height / 2
    gap = zone_top - (center_y + half)            # leftover air above, if centred
    if gap > top_gap_max:                          # short content -> pull up
        center_y = zone_top - top_gap_max - half
    center_y = max(center_y, zone_bottom + half)   # never overflow the bottom margin
    content.move_to([left_x + content.width / 2, center_y, 0])
    return content


def scene_head(spec: dict[str, Any], ctx: dict[str, Any], *, label: str) -> list[Block]:
    ground = ctx["ground"]
    role = accent_role(spec)
    left = -T.FRAME_W / 2 + T.SIDE_GUTTER
    top = T.FRAME_H / 2 - T.SAFE_MARGIN

    blocks = []

    # `kicker` overrides the template's default eyebrow word (e.g. a motivation
    # scene reading "[ MOTIVATION ]" while keeping its accent colour family).
    if spec.get("kicker"):
        label = f"[ {spec['kicker']} ]"
    eyebrow = brand.eyebrow(label, ground, role=role)
    eyebrow.move_to([left + eyebrow.width / 2, top - eyebrow.height / 2, 0])
    blocks.append(Block("eyebrow", eyebrow, anim="fade", static=True))

    content_w = T.FRAME_W - 2 * T.SIDE_GUTTER
    title = brand.heading_rich(spec.get("title", ""), ground, role="primary", size="h1",
                               max_width=content_w)
    title.next_to(eyebrow, DOWN, buff=T.EYEBROW_GAP).align_to(eyebrow, LEFT)
    blocks.append(Block("title", title, anim="fade", static=True))

    return blocks


def motif_corner(ground: str) -> Block:
    motif = brand.summit_bars(ground, height=0.45, color_role="muted", opacity=0.4)
    motif.move_to([T.FRAME_W / 2 - T.SAFE_MARGIN - motif.width / 2,
                   -T.FRAME_H / 2 + T.SAFE_MARGIN + motif.height / 2, 0])
    return Block("motif", motif, anim="fade", static=True, layer="decoration")

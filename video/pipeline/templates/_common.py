"""Shared template helpers for Direction D dark teaching frames.

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


# -- The Lectern: one shared horizontal grid every template aligns to --------
#
# Until now each template chose its own left x (scene_head's gutter, derivation's
# equation edge, callout's centre, ...) and any "second column" -- derivation
# reasons, procedure results, recap formula cards -- floated with the PRIMARY
# column's width, so no two scene types aligned and the right ~half of the frame
# was used inconsistently (the #1 finding of the 2026-06-21 design audit). The
# Lectern replaces that with ONE 12-column grid derived from the frame metrics:
#   * SPINE_X -- the single left alignment axis (masthead + every primary column)
#   * RAIL_X  -- a FIXED right-rail column the second stream snaps to
# so every scene shares a vertical spine and the rail lands in the same place.
# Tokens here are DERIVED from theme metrics (no new magic numbers); RAIL_COL is
# the one knob that rebalances primary-vs-rail width across all templates at once.

CONTENT_W = T.FRAME_W - 2 * T.SIDE_GUTTER     # usable width between the side gutters
SPINE_X = -T.FRAME_W / 2 + T.SIDE_GUTTER      # left alignment axis (== old scene_head left)
GRID_COLS = 12
_COL_W = CONTENT_W / GRID_COLS


def col_x(n: float) -> float:
    """Absolute x of the left edge of grid column *n* (0 == SPINE_X, 12 == right edge)."""
    return SPINE_X + n * _COL_W


# The reason/result/card rail starts at column 7: the primary column keeps 7/12 of
# the width (room for short equations or a prose measure), the rail 5/12 (a reason
# phrase or a formula card). Move RAIL_COL to rebalance every template together.
RAIL_COL = 7
RAIL_X = col_x(RAIL_COL)
RAIL_W = CONTENT_W - RAIL_COL * _COL_W         # rail width (RAIL_X -> right gutter edge)
PRIMARY_W = RAIL_COL * _COL_W                  # primary width (SPINE_X -> RAIL_X)

# Masthead vertical anchor: the eyebrow's TOP edge sits here in EVERY title-bearing
# template (via scene_head), and the title is pinned a fixed gap below it. Because the
# eyebrow font size is constant, the title's top lands at a fixed y too -- so the
# heading never drifts scene-to-scene. Content flows BELOW the title into body_zone;
# a taller/wrapped title grows downward, never upward past this line. The cure for the
# "title floats around between scenes" report is making scene_head the ONLY masthead
# (templates that re-implemented or skipped it are what drifted).
MASTHEAD_TOP = T.FRAME_H / 2 - T.SAFE_MARGIN


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
    """Position a left-flush content group CENTRED in the body zone below *title*.

    The body zone is (title bottom - TITLE_GAP) down to the bottom safe margin. Content
    is CENTRED in it, so short content gets BALANCED top/bottom breathing room (the
    "對稱留白" the user asked for, 2026-06-21). This replaced an earlier clamp that
    pulled short content UP toward the title (top_gap_max), which stranded the lower
    zone empty -- the "light content floats high / wasted space" failure the density
    survey confirmed. Tall content top-anchors at the zone top and overflows the bottom,
    where sizecheck's capacity trigger (_capacity_issues) flags it for splitting. The
    comfortable-band spread (stack_layout / fill_gap) opens light rows first; this then
    balances the block. *top_gap_max* is accepted for call-site compatibility but no
    longer pulls content up. Mutates and returns *content*.
    """
    zone_top = title.get_bottom()[1] - T.TITLE_GAP
    zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN
    half = content.height / 2
    center_y = (zone_top + zone_bottom) / 2
    center_y = min(center_y, zone_top - half)      # tall content: top-anchor (overflow flagged)
    content.move_to([left_x + content.width / 2, center_y, 0])
    return content


def center_in_zone(mobs, title, *, extra_bottom: float = 0.0) -> None:
    """Shift *mobs* (as a group) so their combined bounding box is CENTRED in the body
    zone below *title*. For templates that hand-place content from a fixed HIGH anchor
    (procedure/theorem/recap) -- which stranded the lower zone when content was light
    (the "floats high / wasted space" failure) -- call this after placing so the block
    sits balanced instead. *extra_bottom* reserves room at the bottom (e.g. procedure's
    worked strip is pinned there). Clamps so a tall group never pokes above the zone top
    (it then top-anchors and overflows the bottom, which sizecheck's _overflow_issues
    catches). Mutates the mobs in place."""
    from manim import VGroup

    mobs = [m for m in mobs if m is not None]
    if not mobs:
        return
    grp = VGroup(*mobs)
    zt = title.get_bottom()[1] - T.TITLE_GAP
    zb = -T.FRAME_H / 2 + T.SAFE_MARGIN + extra_bottom
    half = grp.height / 2
    target = min((zt + zb) / 2, zt - half)        # tall group: top-anchor at zone top
    grp.shift([0, target - grp.get_center()[1], 0])


# How far a stack's inter-row gap may open past its min pitch -- an ABSOLUTE cap
# (the survey found fill_gap's only guard was relative, so light content could either
# over-stretch into ugly gaps OR under-fill and float high). Light content spreads to
# min_pitch+COMFORT_SPREAD then CENTRES (balanced breathing room, not floating high).
COMFORT_SPREAD = 0.5


def stack_layout(heights: list[float], min_pitch: float, body_ref, *,
                 extra_bottom: float = 0.0) -> tuple[float, float]:
    """Comfortable-band vertical layout for ONE stacked column. Returns (pitch, top_y):
    the inter-row GAP to use and the y of the first row's TOP edge, so the column is
    CENTRED in the body zone with a capped gap.

    - LIGHT  (even at the comfortable max it doesn't fill): use max pitch, centre ->
      balanced top/bottom breathing room, NOT anchored high with an empty lower zone.
    - FIT    (fits between min and max): open the gap to fill the zone, centred.
    - OVERFLOW (won't fit even at min): min pitch, top-anchored (sizecheck's capacity
      trigger flags it for splitting).

    The body zone is (body_ref.bottom - TITLE_GAP) down to the bottom safe margin, minus
    *extra_bottom* (room a caller reserves at the bottom, e.g. a pinned worked strip).
    Templates place rows top-down from top_y, each row's centre at the running y, then
    `y -= prev_half + pitch + half` -- the fused-rows pitch, so tall rows never collide.
    """
    zt = body_ref.get_bottom()[1] - T.TITLE_GAP
    zb = -T.FRAME_H / 2 + T.SAFE_MARGIN + extra_bottom
    zone_h = zt - zb
    n = len(heights)
    total = sum(heights)
    if n < 2:
        pitch, block_h = min_pitch, total
    else:
        nat_min = total + (n - 1) * min_pitch
        max_pitch = min_pitch + COMFORT_SPREAD
        nat_max = total + (n - 1) * max_pitch
        if nat_max <= zone_h:
            pitch = max_pitch
        elif nat_min >= zone_h:
            pitch = min_pitch
        else:
            pitch = min_pitch + (zone_h - nat_min) / (n - 1)
        block_h = total + (n - 1) * pitch
    top_y = min((zt + zb) / 2 + block_h / 2, zt)
    return pitch, top_y


def scene_head(spec: dict[str, Any], ctx: dict[str, Any], *, label: str) -> list[Block]:
    ground = ctx["ground"]
    role = accent_role(spec)
    left = SPINE_X
    top = MASTHEAD_TOP

    blocks = []

    # `kicker` overrides the template's default eyebrow word (e.g. a motivation
    # scene reading "[ MOTIVATION ]" while keeping its accent colour family).
    if spec.get("kicker"):
        label = f"[ {spec['kicker']} ]"
    eyebrow = brand.eyebrow(label, ground, role=role)
    eyebrow.move_to([left + eyebrow.width / 2, top - eyebrow.height / 2, 0])
    blocks.append(Block("eyebrow", eyebrow, anim="fade", static=True))

    # multi-page part indicator (e.g. '2 / 3'), top-right -- generalises the example_head
    # mechanism to EVERY scene_head template, so any long scene (a split proof, a long
    # table) can paginate: the author repeats the title on each page and sets `part`.
    part = spec.get("part")
    if part:
        pind = brand.eyebrow(_part_text(part), ground, role=role)
        pind.move_to([SPINE_X + CONTENT_W - pind.width / 2, top - pind.height / 2, 0])
        blocks.append(Block("part", pind, anim="fade", static=True, layer="decoration"))

    content_w = CONTENT_W
    title = brand.heading_rich(spec.get("title", ""), ground, role="primary", size="h1",
                               max_width=content_w)
    title.next_to(eyebrow, DOWN, buff=T.EYEBROW_GAP).align_to(eyebrow, LEFT)
    blocks.append(Block("title", title, anim="fade", static=True))

    return blocks


def _part_text(part) -> str:
    """'1 / 2' from {current, total} (or pass a ready string)."""
    if isinstance(part, dict):
        return f"{part.get('current', '')} / {part.get('total', '')}"
    return str(part)


def example_head(spec: dict[str, Any], ctx: dict[str, Any]) -> tuple[list[Block], Any]:
    """Worked-example header (Stewart-style example + solution).

    A true worked example shows its PROBLEM, not a vague descriptive title:
      [ EXAMPLE ]  (eyebrow, left)            (part indicator '1 / 2', right -- multi-page)
      <the prompt as the headline>            (statement-weight prose, never a towering bold title)
      ----------------------------------------(hairline)
      SOLUTION                                (the lead that opens the worked solution)
    Returns (blocks, body_ref): the solution body sits below body_ref (the SOLUTION lead).
    Used by solution templates when the scene carries a `prompt:` field; a continuation
    page (`part.current > 1`) repeats the prompt and reads 'SOLUTION (CONT.)'.
    """
    ground = ctx["ground"]
    role = accent_role(spec)
    blocks: list[Block] = []

    eyebrow = brand.eyebrow("[ example ]", ground, role=role)
    eyebrow.move_to([SPINE_X + eyebrow.width / 2, MASTHEAD_TOP - eyebrow.height / 2, 0])
    blocks.append(Block("eyebrow", eyebrow, anim="fade", static=True))

    part = spec.get("part")
    cont = isinstance(part, dict) and int(part.get("current", 1)) > 1
    if part:
        # part indicator reads in the scene's accent (was muted ink_3 -- too faint to
        # notice top-right); same hue family as the eyebrow, clearly visible.
        pind = brand.eyebrow(_part_text(part), ground, role=role)
        right = SPINE_X + CONTENT_W
        pind.move_to([right - pind.width / 2, MASTHEAD_TOP - pind.height / 2, 0])
        blocks.append(Block("part", pind, anim="fade", static=True, layer="decoration"))

    # the problem itself as the headline -- statement-weight prose (handles inline
    # $math$), NOT a bold display title (a formula-bearing bold title towers over the
    # text; regular-weight prose x-height-matches its math and stays calm).
    prompt = brand.prose(spec.get("prompt", ""), ground, role="primary", size="h3",
                         max_width=CONTENT_W, align="LEFT")
    prompt.next_to(eyebrow, DOWN, buff=T.EYEBROW_GAP).align_to(eyebrow, LEFT)
    blocks.append(Block("prompt", prompt, anim="fade", static=True))

    rule = brand.hrule(CONTENT_W, ground, role="hairline_strong", stroke=1.5, opacity=0.7)
    rule.move_to([SPINE_X + CONTENT_W / 2, prompt.get_bottom()[1] - 0.26, 0])
    blocks.append(Block("solrule", rule, anim="fade", static=True, layer="decoration"))

    sol = brand.eyebrow("solution (cont.)" if cont else "solution", ground, role="muted")
    sol.move_to([SPINE_X + sol.width / 2, rule.get_center()[1] - 0.16 - sol.height / 2, 0])
    blocks.append(Block("sollead", sol, anim="fade", static=True))

    return blocks, sol


def motif_corner(ground: str) -> Block:
    motif = brand.summit_bars(ground, height=0.45, color_role="muted", opacity=0.4)
    motif.move_to([T.FRAME_W / 2 - T.SAFE_MARGIN - motif.width / 2,
                   -T.FRAME_H / 2 + T.SAFE_MARGIN + motif.height / 2, 0])
    return Block("motif", motif, anim="fade", static=True, layer="decoration")

"""Shared template helpers for Direction D dark teaching frames.

scene_head: the eyebrow tag + title block every teaching template opens with
(mirrors B_SceneHead in the design, minus the grid -- grids are disabled
project-wide, see theme.SHOW_GRID). Returns a list[Block] (eyebrow, title) all
static.

motif_corner: the faint summit-bars mark bottom-right.

These exist so the six dark templates don't each re-implement the same header.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from manim import DOWN, LEFT, VGroup

from .. import brand
from ..blocks import Block, accent_role
from ..scene_roles import resolve_chip
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

# Decorative spine axis (2026-06-24 Step 2-B2 prototype): the x of a VISIBLE vertical
# line that makes the Lectern's left axis show. It sits in the LEFT GUTTER, just left of
# SPINE_X (the content edge), so content reads as flush to it and the line never overlaps
# glyphs. Deliberately NOT SPINE_X -- drawing the spine AT SPINE_X would collide with text.
DECOR_SPINE_X = SPINE_X - 0.22

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


# Lectern bias: where short content sits between dead-centre (0.0) and top-anchored
# (1.0) in the body zone. Dead-centre floats content in the void; top-anchor strands the
# whole lower zone (the two failures the 2026-06-21 survey bounced between). ~0.55 sits
# short content in the upper-middle -- tied to the title, with the leftover whitespace
# pooled at the bottom where the corner motif balances it. One knob for every template.
UPPER_BIAS_FRAC = 0.55


def _biased_y(zone_top: float, zone_bottom: float, half: float) -> float:
    """Centre-y for a block of half-height *half* in (zone_bottom, zone_top), biased to
    the upper-middle by UPPER_BIAS_FRAC. Tall content (top-anchor already at/below the
    midpoint) top-anchors unchanged so it overflows the bottom, not the title."""
    mid_y = (zone_top + zone_bottom) / 2
    top_y = zone_top - half                       # top-anchored centre
    if top_y <= mid_y:                            # tall: top-anchor (overflow flagged elsewhere)
        return top_y
    return mid_y + UPPER_BIAS_FRAC * (top_y - mid_y)


def place_body(content, title, left_x: float, *, top_gap_max: float | None = None):
    """Position a left-flush content group in the body zone below *title*, biased to the
    UPPER-middle (the Lectern bias).

    The body zone is (title bottom - TITLE_GAP) down to the bottom safe margin. Dead-
    centring short content (the previous behaviour) left a large void BOTH under the
    title and above the bottom, so a 3-line definition read as floating, disconnected
    from its title (2026-06-21 A1 finding -- worst on single-column definition_math).
    We instead sit short content in the upper-middle via _biased_y: tied to the title,
    with the remaining whitespace pooled at the bottom where the corner motif balances
    it. Tall content still top-anchors and overflows the bottom (sizecheck's capacity
    trigger flags it for splitting). *top_gap_max* is accepted for call-site
    compatibility but unused. Mutates and returns *content*.
    """
    zone_top = title.get_bottom()[1] - T.TITLE_GAP
    zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN
    center_y = _biased_y(zone_top, zone_bottom, content.height / 2)
    content.move_to([left_x + content.width / 2, center_y, 0])
    return content


def center_in_zone(mobs, title, *, extra_bottom: float = 0.0) -> None:
    """Shift *mobs* (as a group) so their combined bounding box sits in the body zone
    below *title*, biased to the UPPER-middle (the Lectern bias, see _biased_y). For
    templates that hand-place content from a fixed HIGH anchor (procedure/theorem/recap),
    call this after placing so a light block is tied to the title instead of floating.
    *extra_bottom* reserves room at the bottom (e.g. procedure's worked strip is pinned
    there). A tall group still top-anchors and overflows the bottom (sizecheck catches
    it). Mutates the mobs in place."""
    from manim import VGroup

    mobs = [m for m in mobs if m is not None]
    if not mobs:
        return
    grp = VGroup(*mobs)
    zt = title.get_bottom()[1] - T.TITLE_GAP
    zb = -T.FRAME_H / 2 + T.SAFE_MARGIN + extra_bottom
    target = _biased_y(zt, zb, grp.height / 2)
    grp.shift([0, target - grp.get_center()[1], 0])


# How far a stack's inter-row gap may open past its min pitch -- an ABSOLUTE cap
# (the survey found fill_gap's only guard was relative, so light content could either
# over-stretch into ugly gaps OR under-fill and float high). Light content spreads to
# min_pitch+COMFORT_SPREAD then CENTRES (balanced breathing room, not floating high).
COMFORT_SPREAD = 0.5


# -- capacity contract: one formula drives BOTH placement and audit -----------
#
# A stacked column's density falls in one of three regimes, decided by its natural
# height at the TIGHTEST pitch (natural_min = Σheights + (n-1)*min_pitch) against the
# body zone. classify_regime is the SINGLE source of that decision, shared by
# stack_layout (placement) and -- via each template's capacity_meta() -- by
# sizecheck._capacity_issues (the predictive split audit), so the two never drift apart
# (the failure the 2026-06-21 design audit flagged: stack_layout and sizecheck each
# re-deriving the same height formula). See DESIGN.md "內容分量變異：容量契約三層架構".
SPARSE = "sparse"   # even opened to the comfort max, the column doesn't fill the zone
FIT = "fit"         # fits between min and comfort-max: open the gap to fill, centred
DENSE = "dense"     # won't fit even at min pitch -> tightest pitch, top-anchor + split


def classify_regime(total_h: float, n: int, zone_h: float, min_pitch: float,
                    comfort_spread: float = COMFORT_SPREAD) -> tuple[str, float]:
    """Classify a column of *n* rows (combined height *total_h*) against *zone_h* and
    return (regime, pitch) -- the inter-row gap to place at. The elastic comfort band is
    [min_pitch, min_pitch+comfort_spread]. DENSE means natural_min >= zone_h: the column
    cannot fit one page even at the tightest pitch (sizecheck warns to split). For n<2
    there is no inter-row gap; the lone row is DENSE iff it alone overflows."""
    nat_min = total_h + max(n - 1, 0) * min_pitch
    if n < 2:
        return (DENSE if nat_min >= zone_h else FIT), min_pitch
    max_pitch = min_pitch + comfort_spread
    nat_max = total_h + (n - 1) * max_pitch
    if nat_max <= zone_h:
        return SPARSE, max_pitch
    if nat_min >= zone_h:
        return DENSE, min_pitch
    return FIT, min_pitch + (zone_h - nat_min) / (n - 1)


@dataclass
class ColumnPlan:
    """One stacked column's capacity parameters -- a template's capacity_meta(spec)
    returns a list of these (one per column). Read by sizecheck._capacity_issues as the
    per-column source, so the predictive split audit reads the same layout placement does
    (single source, no drift).

    *model* selects how a column's natural height is read from its built rows:
    - "stack" (ELASTIC templates -- derivation, definition_math): Σ(row heights) +
      (n-1)*min_pitch. Their placement EXPANDS to fill the zone, so the built positions
      don't reveal the tightest packing -- the capacity question is "does it fit even at
      the tightest pitch?", hence the min-pitch sum.
    - "span" (FIXED-rhythm templates -- procedure, theorem, recap): the actual rendered
      extent (max top - min bottom). Their placement is non-elastic, so the built rows
      already sit at their real centre-to-centre rhythm; a Σh+pitch estimate would
      mis-model that (and double-count middle row heights). The span is MEASURED, not
      estimated, so it sidesteps the row-height-prediction problem entirely.
    *min_pitch* is used only by the "stack" model. *extra_bottom* is room reserved at the
    bottom of the body zone this content must clear (e.g. procedure's pinned worked strip).
    *x_bucket* optionally pins a plan to a measured column's round(left) so a multi-column
    "stack" template can give columns different min_pitch -- None means 'every column'."""
    min_pitch: float
    extra_bottom: float = 0.0
    x_bucket: int | None = None
    model: str = "stack"


def stack_layout(heights: list[float], min_pitch: float, body_ref, *,
                 extra_bottom: float = 0.0) -> tuple[float, float]:
    """Comfortable-band vertical layout for ONE stacked column. Returns (pitch, top_y):
    the inter-row GAP to use and the y of the first row's TOP edge, so the column is
    CENTRED in the body zone with a capped gap. The regime decision (SPARSE max-pitch /
    FIT spread / DENSE min-pitch) is delegated to classify_regime -- the shared source
    sizecheck mirrors.

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
    _regime, pitch = classify_regime(total, n, zone_h, min_pitch)
    block_h = total + max(n - 1, 0) * pitch
    top_y = min((zt + zb) / 2 + block_h / 2, zt)
    return pitch, top_y


def scene_head(spec: dict[str, Any], ctx: dict[str, Any], *, label: str) -> list[Block]:
    ground = ctx["ground"]
    role = accent_role(spec)
    left = SPINE_X
    top = MASTHEAD_TOP

    blocks = []

    # The eyebrow chip is resolved centrally (scene_roles.resolve_chip):
    # kicker > explicit `label` > `scene_role` > the template's default `label`.
    # A chipless scene_role (motivation / intuition / bridge / forward-ref / ...) resolves
    # to None: we still build + position the eyebrow at its default text -- so the title
    # anchor, and thus every downstream body zone, is IDENTICAL to a chipped scene (no
    # drift) -- but render it invisible. Keeping the block at index 0 preserves the
    # head[1] / blocks[1] title contract the other templates rely on.
    chip = resolve_chip(spec, label)
    eyebrow = brand.eyebrow(label if chip is None else chip, ground, role=role)
    if chip is None:
        eyebrow.set_opacity(0)
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


# sentinel default so resolve_chip returns None ONLY for a chipless (exposition)
# scene_role -- lets spine geometry ask "is this scene chipless?" via the one resolver.
_CHIP_SENTINEL = "\x00"


def _spine_cap_top(spec: dict[str, Any], title_mob) -> float:
    """y of the accent cap's TOP edge.

    Normally the masthead top, so the lit cap spans chip + title. But a chipless scene
    (exposition scene_role -> an invisible placeholder eyebrow) has no chip to light --
    the cap would otherwise dangle over the empty masthead band above the title. Start it
    at the title's top instead, so the cap hugs the title it belongs to."""
    if title_mob is not None and resolve_chip(spec, _CHIP_SENTINEL) is None:
        return title_mob.get_top()[1]
    return MASTHEAD_TOP


def scene_spine(spec: dict[str, Any], ctx: dict[str, Any],
                blocks: "list[Block] | None" = None) -> Block:
    """The Lectern's left axis, made visible -- a restrained vertical spine in the left
    gutter (2026-06-24 Step 2-B2 prototype). A quiet full-height hairline carries the
    structure; an accent 'cap' lit at the masthead carries the scene accent (the
    signature) so content reads as flush to a structural axis. Flat solid only -- NO
    gradient (VISUAL-FRAME-RUBRIC house style); the masthead 'lit' look is a text_glow
    halo on the cap, not a fade. Static, on the decoration layer (drawn under content).

    The cap runs from the masthead top down to the TITLE's actual bottom edge (read from
    *blocks*), so the lit length tracks the real title height on every template -- graph's
    Pango title renders ~1.36x taller than the Tex titles, so a fixed fraction under-lit
    it (2026-06-24 fix). Falls back to a fixed band when no title block is present."""
    ground = ctx["ground"]
    role = accent_role(spec)
    top = MASTHEAD_TOP
    bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN
    span = top - bottom
    axis = brand.vrule(span, ground, role="hairline_strong", width=2.0, opacity=0.9)
    axis.move_to([DECOR_SPINE_X, (top + bottom) / 2, 0])
    cap_bottom = top - span * 0.17
    title_mob = None
    if blocks:
        title_mob = next((b.mobject for b in blocks if b.id in ("title", "prompt")), None)
        if title_mob is not None:
            cap_bottom = title_mob.get_bottom()[1]
    cap_top = _spine_cap_top(spec, title_mob)   # title-top for a chipless scene, else masthead
    cap_h = max(cap_top - cap_bottom, 0.2)
    cap = brand.vrule(cap_h, ground, role=role, width=2.4)
    cap.move_to([DECOR_SPINE_X, cap_top - cap_h / 2, 0])
    cap_glow = brand.text_glow(cap, ground, role=role, width=2.4, opacity=0.5)
    return Block("spine", VGroup(axis, cap_glow), anim="fade", static=True, layer="decoration")


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


# -- L3: optional enrichment aside (turn sparse dead-space into teaching) ------
#
# A SPARSE template (a one-line definition) leaves the body's lower band empty even
# after the Lectern upper-bias -- _biased_y only MOVES the whitespace, it can't fill it.
# build_aside lets the author opt a supporting note / key-idea / mini-example into the
# fixed right rail (RAIL_X): a barred panel, sized to RAIL_W, in the section accent. It is
# AUTHOR-AUTHORED and OPTIONAL -- the framework never generates content to fill space (that
# would be the auto-fit speculation the design rejects). A template that adopts it (today
# definition_math) collapses the aside back to a single full-width column when the primary
# content is dense, so the aside never crowds real content. See DESIGN.md.

_ASIDE_INK = {"secondary": "blue_ink", "accent": "amber_ink", "success": "green_ink",
              "warning": "red_ink", "blue": "blue_ink", "amber": "amber_ink",
              "green": "green_ink", "red": "red_ink"}


def build_aside(aside, ground: str, *, max_width: float):
    """An enrichment card for the body's right rail. *aside* is ``{label?, body, accent?}``
    (or a bare body string); *accent* is a bar colour role (default ``secondary``/blue).
    Returns an accent_panel VGroup sized to *max_width* -- place its left edge at RAIL_X."""
    if not isinstance(aside, dict):
        aside = {"body": str(aside)}
    accent = str(aside.get("accent", "secondary"))
    inner_w = max(max_width - 1.1, 1.0)        # room for the 5px bar + horizontal pad
    body = brand.prose(str(aside.get("body", "")), ground, role="text", size="prose_sm",
                       max_width=inner_w, align="LEFT")
    if aside.get("label"):
        label = brand.eyebrow(str(aside["label"]), ground, role=_ASIDE_INK.get(accent, "blue_ink"))
        inner = VGroup(label, body).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    else:
        inner = body
    return brand.accent_panel(inner, ground, bar_role=accent, fill_role="panel",
                              radius=T.RADIUS_MD, bar_px=5, pad=0.42, pad_x=0.5)


def motif_corner(ground: str) -> Block:
    motif = brand.summit_bars(ground, height=0.45, color_role="muted", opacity=0.4)
    motif.move_to([T.FRAME_W / 2 - T.SAFE_MARGIN - motif.width / 2,
                   -T.FRAME_H / 2 + T.SAFE_MARGIN + motif.height / 2, 0])
    return Block("motif", motif, anim="fade", static=True, layer="decoration")


def _assumption_text(meta, flag_id) -> str | None:
    """The human text for an assumption id, from meta.assumptions; None if absent."""
    for a in (meta or {}).get("assumptions", []) or []:
        if isinstance(a, dict) and a.get("id") == flag_id:
            return a.get("text")
    return None


def render_scaffold(scaffold, ground, meta=None) -> list[Block]:
    """Render optional scaffold (motive / divider-problem / first-use flag) as static
    Block(s). Returns [] when scaffold is absent/empty (no-op -> render unchanged).
    motive/problem use role='text' (NEVER 'muted'); flag shows the assumption text."""
    if not isinstance(scaffold, dict):
        return []
    out = []
    motive = scaffold.get("motive")
    if isinstance(motive, str) and motive.strip():
        # CONTENT_W (not the primary-column PRIMARY_W): the motive line sits on the spine
        # with the full width free, so it shouldn't wrap early and leave the right half
        # empty (it read as a too-short right margin next to the wider statement below).
        mob = brand.prose(motive, ground, role="text", size="prose_sm",
                          max_width=CONTENT_W, align="LEFT")
        out.append(Block("scaffold.motive", mob, anim="fade", static=True, layer="content"))
    problem = scaffold.get("problem")
    if isinstance(problem, str) and problem.strip():
        mob = brand.prose(problem, ground, role="text", size="prose",
                          max_width=CONTENT_W, align="LEFT")
        out.append(Block("scaffold.problem", mob, anim="fade", static=True, layer="content"))
    flag = scaffold.get("flag")
    if isinstance(flag, str) and flag.strip():
        body = _assumption_text(meta, flag) or flag
        # PRIMARY_W (not the narrow RAIL_W): the flag sits under the title on the spine,
        # so the full primary column is free -- a short assumption shouldn't wrap when
        # there is ample room to its right. accent_panel still shrink-wraps to content.
        mob = build_aside({"label": "assumes", "body": body}, ground, max_width=PRIMARY_W)
        out.append(Block(f"scaffold.flag.{flag}", mob, anim="fade", static=True, layer="content"))
    return out

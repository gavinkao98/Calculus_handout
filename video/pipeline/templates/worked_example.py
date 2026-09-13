"""worked_example template -- the handout's `workedexample` container on screen.

A classroom worked example: the PROBLEM as the masthead, a SOLUTION step chain on the
spine, an optional strategy / notes rail on the right, and the ANSWER as the heaviest
element in the lower third. 24% of the book's semantic blocks are example+solution, and
until now they had to borrow `derivation` + `prompt:` -- which gives the reasoning rail
to per-row reasons, has no answer band, and so leaves the conclusion no heavier than the
algebra above it. Design source: `_audit/design-template-system/WorkedExample.dc.html`.

Authoring contract:

  template: worked_example
  accent: example                 # optional; DEFAULTS to `example` (practice green)
  number: "3.1"                   # optional -> eyebrow `[ EXAMPLE 3.1 ]`
  title: "the companion limit"    # optional -> small tagline right of the chip
  prompt: "Establish $\\lim\\dots$"  # REQUIRED (schema): no problem, no example
  part: { current: 1, total: 2 }  # optional pager; a NON-final page may omit `result`
  scaffold: { motive: "..." }     # optional, as on derivation
  strategy: "Multiply by the conjugate."     # optional; rail, upper block
  notes_label: "what each factor does"       # optional; defaults to `notes`
  notes:                                     # optional; rail, lower block
    - { math: "\\frac{\\sin\\theta}{\\theta}", text: "$\\to 1$", ref: "Prop 3.2" }
  paced: [step.0, result]
  steps:                          # row grammar is derivation's, VERBATIM (see below)
    - { math: "..." }
    - { math: "= ...", anim: transform, frame: true }
  result: { math: "... = 0", reason: "answer" }   # the answer band; `reason` = its tag
  check:  { math: "..." }         # optional; a green-check row closing the chain

Rows (`steps[]` / `result` / `check`) take `{math, anim, frame, cancel, seg_roles,
color_role, mark}` exactly as `derivation` does, and REUSE derivation's own functions --
`_eq_mob` / `_transform_anim` / `_cancel_anim` / `_eq_core` and its second constants --
so `{{...}}` segments, `meta.color_map`, `seg_roles` and `paced:` behave identically and
a change to the morph mechanism reaches both templates at once. A row does NOT take
`reason:` (schema error): the right rail belongs to `strategy:` / `notes:` here, and the
two cannot share one column. The morph chain is `steps[] -> result` (as in derivation);
`check` keeps its stock reveal.

The corner motif is dropped on a page that HAS an answer band: the motif exists to weigh
an empty bottom-right corner, and the band already fills that corner to both safe margins.

Reveal ids: `step.N` / `result` / `check` / `strategy` / `note.N`. `strategy` and
`note.N` are part of the opening frame unless `say` names `{show strategy}` /
`{show note.0}` (the `_common.reveals` convention, as for `statement`); `result` is
always dynamic. The `notes_label` rides in with `note.0`, the way theorem_proof's PROOF
kicker rides in with `proof.0`.

TWO DELIBERATE DEPARTURES FROM THE MOCKUP (both recorded in DESIGN.md):

  1. Rows are flush-left on SPINE_X; the mockup's separate `=` alignment column is NOT
     built (D3). An `=` column would either need `sizecheck._capacity_issues` to stop
     bucketing columns by `round(left)` -- which moves every existing deck's capacity
     verdict -- or an invisible spacer mobject inside each row, which `paced` and
     derivation's `_rail` would both walk as if it were content. The canonical decks
     already set continuation rows as flush-left `= ...`, so this IS the house look.
  2. A row too wide for the step column RAISES instead of shrinking (D7). Layout rule 3
     only opens the right rail while the primary column stays under ~58% of the width
     (`RAIL_COL = 7` -> 58.3%), and the project has ruled out auto-fit shrinking
     (DESIGN.md, capacity contract): over-width is an authoring decision, so the build
     stops and names the row rather than silently shrinking or clipping it. Without a
     rail the step column is the full `CONTENT_W` and over-width stays reactive
     (`sizecheck._overflow_issues`), as for every other template.
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT, RIGHT, RoundedRectangle, VGroup

from .. import brand
from ..blocks import Block, accent_role
from ..scene_roles import resolve_chip
from ..visuals import theme as T
from . import derivation
from ._common import (MASTHEAD_TOP, CONTENT_W, PRIMARY_W, RAIL_W, RAIL_X, SPINE_X, ColumnPlan,
                      _biased_y, _part_text, fill_gap, motif_corner, render_scaffold, reveals)

# `accent` is optional on this template alone: it IS the handout's `workedexample`
# container, which is always practice green there, so an unmarked scene is not the
# "author claimed nothing" case blocks.DEFAULT_ROLE exists for.
DEFAULT_ACCENT = "example"

# Type sizes read off the shared scale (T2 2026-09-14 promoted D6's raw 62 / 34 into the
# named `math_conclusion` / `math_rail` tokens): MathRules rule 5's three math tiers are
# 62 / 48 / 34, and step rows keep the shared `math` (48) via derivation's _eq_mob. These
# stay bound as px numbers because they are also the _clamp_shrink floors below.
ANSWER_PX = T._SCALE_PX["math_conclusion"]   # the answer band's equation -- the frame's heaviest type
RAIL_MATH_PX = T._SCALE_PX["math_rail"]      # a rail note's formula (rule 5's supporting tier)

ANSWER_PAD_X = 0.34    # answer band inner padding, left/right of box edge
ANSWER_PAD_Y = 0.22    # ... top/bottom (the mockup's 26/30 px)
ANSWER_GAP = 0.5       # clear space kept between the answer equation and its tag
ANSWER_FILL_OPACITY = 0.10    # flat accent wash -- NO gradient (house style)
ANSWER_STROKE_OPACITY = 0.5   # accent hairline border
BAND_GAP = 0.30        # air between the body zone's floor and the answer band's top

RAIL_GAP = 0.30        # min pitch between rail items (the rail column's own MIN_PITCH)
RAIL_GUTTER = 0.42     # step column -> RAIL_X clearance (the mockup's 56px column gap)
RAIL_RULE_PAD = 0.25   # how far left of RAIL_X the rail's vertical hairline sits
RAIL_REF_GAP = 0.25    # clear space between a note's text and its right-flush ref tag


def _accent_role(spec: dict[str, Any]) -> str:
    """This template's palette role, with D9's `example` default applied. `build` also
    writes the default back into the spec (so scene_spine's cap matches); this reader is
    used by capacity_meta too, which must not mutate the scene it is auditing."""
    return accent_role({"accent": spec.get("accent") or DEFAULT_ACCENT})


def _answer_box(spec: dict[str, Any], ground: str):
    """The answer band, built and pinned: bottom edge on the bottom safe margin, width
    `CONTENT_W`, the answer in the scene accent at ANSWER_PX with a mono tag flush right.

    Returns None when the scene has no `result` -- a `part.current < part.total`
    continuation page, the one shape schema lets omit it (D4).

    SINGLE SOURCE for placement and audit: `build` puts this mobject on screen and
    `capacity_meta` measures the very same one for its reserved bottom band, so the
    predictive split check can never disagree with the layout about how much room the
    band takes (the capacity contract's whole point, DESIGN.md).
    """
    res = spec.get("result")
    if res is None:
        return None
    res = res if isinstance(res, dict) else {"math": res}
    role = _accent_role(spec)
    eq = brand.math_line(str(res.get("math", "")).strip(), ground,
                         role=str(res.get("color_role") or role), size=ANSWER_PX,
                         seg_roles=res.get("seg_roles"))
    tag = brand.eyebrow(str(res.get("reason") or "answer"), ground, role=f"{role}_ink",
                        size="tag")
    inner_w = CONTENT_W - 2 * ANSWER_PAD_X - tag.width - ANSWER_GAP
    if eq.width > inner_w > 0:
        brand._clamp_shrink(eq, inner_w, ANSWER_PX)
    height = max(eq.height, tag.height) + 2 * ANSWER_PAD_Y
    box = RoundedRectangle(corner_radius=T.RADIUS_MD, width=CONTENT_W, height=height,
                           stroke_color=T.color(ground, role), stroke_width=1.5,
                           stroke_opacity=ANSWER_STROKE_OPACITY,
                           fill_color=T.color(ground, role),
                           fill_opacity=ANSWER_FILL_OPACITY)
    cy = -T.FRAME_H / 2 + T.SAFE_MARGIN + height / 2
    box.move_to([SPINE_X + CONTENT_W / 2, cy, 0])
    eq.move_to([SPINE_X + ANSWER_PAD_X, cy, 0], aligned_edge=LEFT)
    tag.move_to([SPINE_X + CONTENT_W - ANSWER_PAD_X, cy, 0], aligned_edge=RIGHT)
    return VGroup(box, eq, tag)


def capacity_meta(spec: dict[str, Any]) -> list[ColumnPlan]:
    """Capacity contract (L2): TWO independent stacked columns, not one.

    The step chain on the spine is elastic at derivation's own MIN_PITCH (it is the same
    chain, built by the same code), and the strategy / notes rail is a second stream at
    RAIL_GAP pinned to `round(RAIL_X)` -- so a rail dense enough to overflow is caught on
    its own terms instead of being averaged into the step column. Both reserve the answer
    band's room at the bottom, measured off the band itself (`_answer_box`).
    """
    box = _answer_box(spec, "dark")
    extra_bottom = (box.height + BAND_GAP) if box is not None else 0.0
    return [ColumnPlan(min_pitch=derivation.MIN_PITCH, extra_bottom=extra_bottom),
            ColumnPlan(min_pitch=RAIL_GAP, extra_bottom=extra_bottom,
                       x_bucket=round(RAIL_X))]


def _rows_from_spec(spec: dict[str, Any]) -> list[dict]:
    """The step column's rows: `steps[]` then the optional `check`. Deliberately the same
    dict shape derivation's `_eq_mob` reads, minus `reason` (D2). The answer band is NOT
    a row -- it is pinned at the bottom and built by `_answer_box`."""
    rows: list[dict] = []
    for i, st in enumerate(spec.get("steps") or []):
        st = st if isinstance(st, dict) else {"math": st}
        rows.append({"math": str(st.get("math", "")), "kind": "step", "rid": f"step.{i}",
                     "anim": st.get("anim") or "write", "mark": st.get("mark"),
                     "color_role": st.get("color_role"), "cancel": st.get("cancel"),
                     "frame": st.get("frame"), "seg_roles": st.get("seg_roles")})
    if spec.get("check") is not None:
        c = spec["check"]
        c = c if isinstance(c, dict) else {"math": c}
        rows.append({"math": str(c.get("math", "")), "kind": "check", "rid": "check",
                     "anim": "write", "color_role": c.get("color_role"),
                     "seg_roles": c.get("seg_roles")})
    return rows


def _masthead(spec: dict[str, Any], ctx: dict[str, Any]) -> "tuple[list[Block], Any]":
    """`[ EXAMPLE 3.1 ]` + tagline / pager -> the problem -> hairline -> SOLUTION.

    The same five block ids `_common.example_head` produces (`eyebrow` / `part` /
    `prompt` / `solrule` / `sollead`), so sizecheck's HEADER set and scene_spine's search
    for the title anchor both keep working untouched -- but built here because this
    template adds two things example_head has no place for: the example NUMBER inside the
    chip, and `title` as a quiet tagline beside it (example_head ignores `title`
    entirely). Returns (blocks, body_ref) -- the SOLUTION lead the body hangs under.
    """
    ground = ctx["ground"]
    role = _accent_role(spec)
    blocks: list[Block] = []

    number = spec.get("number")
    default = f"[ example {number} ]" if number else "[ example ]"
    chip = resolve_chip(spec, default)
    eyebrow = brand.eyebrow(default if chip is None else chip, ground, role=role)
    if chip is None:                       # chipless scene_role: keep the anchor, hide the ink
        eyebrow.set_opacity(0)
    eyebrow.move_to([SPINE_X + eyebrow.width / 2, MASTHEAD_TOP - eyebrow.height / 2, 0])
    head = eyebrow
    if spec.get("title"):
        # `title` as a lowercase tagline, NOT a heading: the problem below is the
        # headline, and a second bold line would compete with it. Rides inside the
        # eyebrow block so the masthead keeps its five ids.
        tagline = brand.prose(str(spec["title"]), ground, role="text", size="caption",
                              align="LEFT")
        tagline.next_to(eyebrow, RIGHT, buff=0.3)
        head = VGroup(eyebrow, tagline)
        # the tagline's descenders make the pair taller than the chip alone, so re-seat
        # the pair on MASTHEAD_TOP -- otherwise the masthead creeps past the safe margin.
        head.shift([0, MASTHEAD_TOP - head.get_top()[1], 0])
    blocks.append(Block("eyebrow", head, anim="fade", static=True))

    part = spec.get("part")
    # "(CONT.)" means "this page CONTINUES an earlier one" (current > 1) -- NOT the same
    # question as "may this page omit the answer" (current < total, _may_omit_result).
    cont = _part_nums(part) is not None and _part_nums(part)[0] > 1
    if part:
        pind = brand.eyebrow(_part_text(part), ground, role=role, size="tag")
        pind.move_to([SPINE_X + CONTENT_W - pind.width / 2,
                      MASTHEAD_TOP - pind.height / 2, 0])
        blocks.append(Block("part", pind, anim="fade", static=True, layer="decoration"))

    prompt = brand.prose(str(spec.get("prompt", "")), ground, role="primary", size="h3",
                         max_width=CONTENT_W, align="LEFT")
    prompt.next_to(head, DOWN, buff=T.EYEBROW_GAP).align_to(eyebrow, LEFT)
    blocks.append(Block("prompt", prompt, anim="fade", static=True))

    rule = brand.hrule(CONTENT_W, ground, role="hairline_strong", stroke=1.5, opacity=0.7)
    rule.move_to([SPINE_X + CONTENT_W / 2, prompt.get_bottom()[1] - 0.26, 0])
    blocks.append(Block("solrule", rule, anim="fade", static=True, layer="decoration"))

    sol = brand.eyebrow("solution (cont.)" if cont else "solution", ground, role="muted")
    sol.move_to([SPINE_X + sol.width / 2, rule.get_center()[1] - 0.16 - sol.height / 2, 0])
    blocks.append(Block("sollead", sol, anim="fade", static=True))

    return blocks, sol


def _part_nums(part) -> "tuple[int, int] | None":
    """(current, total) from a `part:` mapping, or None when there is no usable pager.
    Mirrors example_head's tolerant int() read."""
    if not isinstance(part, dict):
        return None
    try:
        return int(part.get("current", 1)), int(part.get("total", 1))
    except (TypeError, ValueError):
        return None


def _note_row(note: dict, ground: str):
    """One rail note: formula + what it does + the result it cites, flush right.

    The ref tag is `result_ink` blue -- it names a proposition, the one thing in the rail
    that is a citation rather than commentary. The left half is clamped (never the tag,
    already the smallest type in the frame) if the two would collide.
    """
    math = brand.math_line(str(note.get("math", "")).strip(), ground, role="primary",
                           size=RAIL_MATH_PX)
    parts = [math]
    if note.get("text"):
        parts.append(brand.prose(str(note["text"]), ground, role="text", size="caption",
                                 align="LEFT"))
    left = VGroup(*parts).arrange(RIGHT, buff=0.22) if len(parts) > 1 else math
    ref = (brand.eyebrow(str(note["ref"]), ground, role="result_ink", size="tag")
           if note.get("ref") else None)
    avail = RAIL_W - ((ref.width + RAIL_REF_GAP) if ref is not None else 0.0)
    if left.width > avail > 0:
        brand._clamp_shrink(left, avail, RAIL_MATH_PX)
    left.move_to([0, 0, 0], aligned_edge=LEFT)
    if ref is None:
        return left
    ref.move_to([RAIL_W, 0, 0], aligned_edge=RIGHT)
    return VGroup(left, ref)


def _rail(spec: dict[str, Any], ground: str, zone_top: float) -> "tuple[list[Block], float]":
    """The right rail: `strategy` over a hairline over the `notes`, top-flush with the
    body zone. Returns (blocks, rail_bottom_y); ([], zone_top) when the scene declares
    neither, which is what makes the step column widen to CONTENT_W (D8).

    `strategy` / `note.N` are part of the opening frame unless `say` reveals them (D11,
    the `_common.reveals` convention) -- the rail frames the solution, so it normally
    wants to be readable before the first step lands.
    """
    strategy = spec.get("strategy")
    notes = [n for n in (spec.get("notes") or []) if isinstance(n, dict)]
    if not strategy and not notes:
        return [], zone_top

    blocks: list[Block] = []
    y = zone_top

    def place(mob, top_y: float) -> float:
        mob.shift([RAIL_X - mob.get_left()[0], top_y - mob.get_top()[1], 0])
        return mob.get_bottom()[1]

    if strategy:
        label = brand.eyebrow("strategy", ground, role="strategy")
        body = brand.prose(str(strategy), ground, role="text", size="prose_sm",
                           max_width=RAIL_W, align="LEFT")
        parts = [label, body]
        if notes:
            # the divider between the rail's two sections rides INSIDE the strategy group
            # rather than standing between them as a block of its own: a zero-height rule
            # with a gap on each side spends 2 x RAIL_GAP that capacity_meta cannot see
            # (a decoration block is not a measured row), so placement would silently
            # outrun the very audit that is supposed to predict it.
            parts.append(brand.hrule(RAIL_W, ground, role="hairline_strong", stroke=1.0,
                                     opacity=0.7))
        group = VGroup(*parts).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        y = place(group, y)
        blocks.append(_rail_block(spec, "strategy", group))

    for i, note in enumerate(notes):
        row = _note_row(note, ground)
        if i == 0:
            # the notes heading rides in with note.0 (theorem_proof's PROOF kicker does
            # the same with proof.0), so a revealed rail never shows a label with nothing
            # under it. Both are still at the x-origin here; `place` moves the pair.
            head = brand.eyebrow(str(spec.get("notes_label") or "notes"), ground,
                                 role="muted")
            head.shift([-head.get_left()[0], -head.get_top()[1], 0])
            row.shift([0, head.get_bottom()[1] - 0.16 - row.get_top()[1], 0])
            row = VGroup(head, row)
        y = place(row, y - RAIL_GAP)
        blocks.append(_rail_block(spec, f"note.{i}", row))

    axis = brand.vrule(max(zone_top - y, 0.2), ground, role="hairline", width=1.5,
                       opacity=0.8)
    axis.move_to([RAIL_X - RAIL_RULE_PAD, (zone_top + y) / 2, 0])
    blocks.append(Block("rail.axis", axis, anim="fade", static=True, layer="decoration"))
    return blocks, y


def _rail_block(spec: dict[str, Any], bid: str, mob) -> Block:
    if reveals(spec, bid):
        return Block(bid, mob, anim="slide", static=False)
    return Block(bid, mob, anim="fade", static=True)


def _too_wide(rows, eqs, limit: float, sid, has_rail: bool) -> None:
    """D7: a step wider than its column stops the build, named. Auto-fit shrinking is
    ruled out project-wide (DESIGN.md capacity contract) and silently clipping the tail
    of an equation is worse than not rendering, so the author gets the number and the
    three ways out. Only guarded when the rail is open -- without one the column is the
    full CONTENT_W and over-width stays reactive, as on every other template."""
    if not has_rail:
        return
    for row, eq in zip(rows, eqs):
        if eq.width > limit + 1e-6:
            raise ValueError(
                f"Scene '{sid}': worked_example row {row['rid']} is {eq.width:.2f}u wide, "
                f"but the step column is only {limit:.2f}u once the strategy / notes rail "
                f"takes its {RAIL_W:.2f}u (layout rule 3). Split the row into two steps, "
                f"shorten the maths, or drop `strategy:` / `notes:` so the chain gets the "
                f"full {CONTENT_W:.2f}u.")


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    # D9: write the default back, so the centrally-drawn spine cap (templates.build_blocks
    # -> _common.scene_spine, which reads the spec, not this template) is the same green.
    spec.setdefault("accent", DEFAULT_ACCENT)
    blocks, body_ref = _masthead(spec, ctx)

    scaffold_blocks = render_scaffold(spec.get("scaffold"), ground, ctx.get("meta"))
    for sb in scaffold_blocks:
        sb.mobject.next_to(body_ref, DOWN, buff=T.TITLE_GAP).align_to(body_ref, LEFT)
        body_ref = sb.mobject
    blocks += scaffold_blocks

    band = _answer_box(spec, ground)

    zone_top = body_ref.get_bottom()[1] - T.TITLE_GAP
    zone_bottom = (band.get_top()[1] + BAND_GAP if band is not None
                   else -T.FRAME_H / 2 + T.SAFE_MARGIN)

    rail_blocks, _rail_bottom = _rail(spec, ground, zone_top)
    has_rail = bool(rail_blocks)
    blocks += rail_blocks

    rows = _rows_from_spec(spec)
    eqs = [derivation._eq_mob(r, ground, role=_accent_role(spec)) for r in rows]
    step_w = (PRIMARY_W - RAIL_GUTTER) if has_rail else CONTENT_W
    _too_wide(rows, eqs, step_w, spec.get("id"), has_rail)

    # vertical layout: gap-spaced rows, spread to fill the zone between the SOLUTION lead
    # and the answer band (fill_gap caps the spread so a long chain keeps its pitch), then
    # the whole chain sits upper-biased in that zone -- derivation's rhythm exactly.
    heights = [e.height for e in eqs]
    row_gap = fill_gap(heights, derivation.MIN_PITCH, max(zone_top - zone_bottom, 1.5))
    row_mobs: list[Any] = []
    y = 0.0
    prev_half = None
    for r, eq, h in zip(rows, eqs, heights):
        half = h / 2
        if prev_half is not None:
            y -= prev_half + row_gap + (0.12 if r["kind"] == "check" else 0.0) + half
        eq.move_to([SPINE_X, y, 0], aligned_edge=LEFT)
        row_mobs.append((r, VGroup(eq), eq))
        prev_half = half
    if row_mobs:
        chain = VGroup(*[g for _, g, _ in row_mobs])
        target = _biased_y(zone_top, zone_bottom, chain.height / 2)
        chain.shift([0, target - chain.get_center()[1], 0])

    paced_ids = set(spec.get("paced") or [])
    for i, (r, group, eq) in enumerate(row_mobs):
        prev_eq = derivation._eq_core(row_mobs[i - 1][2]) if i else None
        blocks.append(_row_block(r, group, eq, prev_eq,
                                 row_mobs[i - 1][1] if i else None, paced_ids))

    if band is not None:
        # the answer is ALWAYS dynamic (D11): it is the payoff, so it must land on its own
        # beat rather than sitting in the opening frame under the problem it answers.
        res = spec["result"] if isinstance(spec.get("result"), dict) else {}
        # `anim: transform` on the result morphs the LAST STEP into the answer (the chain
        # is steps -> result, as in derivation); a `check` row, if any, is not its source.
        src = next((m for m in reversed(row_mobs) if m[0]["kind"] == "step"), None)
        row = {"rid": "result", "kind": "result", "anim": res.get("anim") or "fade",
               "frame": res.get("frame"), "cancel": res.get("cancel")}
        blocks.append(_row_block(row, band, band[1],
                                 derivation._eq_core(src[2]) if src else None,
                                 src[1] if src else None, paced_ids, default_anim="fade"))

    # The corner motif balances an EMPTY bottom-right; the answer band fills that corner
    # edge to edge (it is pinned to the same safe margin), so with a band the motif would
    # simply sit on top of the answer. Continuation pages, which have no band yet, keep it.
    if band is None:
        blocks.append(motif_corner(ground))
    return blocks


def _row_block(r: dict, group, eq, prev_eq, prev_row, paced_ids: "set[str]",
               *, default_anim: "str | None" = None) -> Block:
    """One row -> one Block, with derivation's transform / cancel dispatch verbatim: a
    morph row becomes a callable that rewrites the row above into this one and advertises
    its nominal seconds; everything else keeps its stock reveal. A `cancel` whose previous
    row has no `{{...}}` segments degrades to a plain transform (schema reports it), and
    the first row -- nothing to morph FROM -- silently keeps its stock reveal, as there."""
    this_eq = derivation._eq_core(eq)
    anim = r["anim"]
    if anim == "cancel" and not getattr(prev_eq, "_ml_parts", False):
        anim = "transform"
    if anim in ("transform", "cancel") and prev_eq is not None and this_eq is not None:
        frame = bool(r.get("frame"))
        paced = r["rid"] in paced_ids
        if anim == "cancel":
            fn = derivation._cancel_anim(prev_eq, prev_row, this_eq,
                                         list(r.get("cancel") or []), frame=frame, paced=paced)
            seconds = derivation.CANCEL_SECONDS
        else:
            fn = derivation._transform_anim(prev_eq, prev_row, this_eq, frame=frame, paced=paced)
            seconds = derivation.TRANSFORM_SECONDS
        return Block(r["rid"], group, anim=fn, static=False,
                     anim_seconds=seconds + (derivation.FRAME_SECONDS if frame else 0.0))
    if anim in ("transform", "cancel"):
        anim = default_anim or derivation._DEFAULT_ANIM[r["kind"]]
    return Block(r["rid"], group, anim=anim, static=False)

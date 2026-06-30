"""derivation template -- Direction D UNIFIED math system (the headline redesign).

A step chain where equations share a left edge and an optional reasoning RAIL on
the right annotates each step (e.g. "subtract 2", "cube root both sides") with a
faint dotted leader. The result line glows amber with a leading therefore; an
optional final check line carries a green checkmark verdict. Scales from 2 to ~7
rows by gap-spacing rows (not glyph size), and carries the reasoning the old
two-column walkthrough needed a whole column for -- so example_walkthrough folds
into this one template.

Two authoring shapes (both supported):

  # structured (preferred):
  template: derivation
  title: "Inverting $f(x)=x^3+2$"
  steps:
    - { math: "y = x^3 + 2", reason: "write $y=f(x)$" }
    - { math: "x^3 = y - 2", reason: "subtract 2" }
    - { math: "x = \\sqrt[3]{y-2}", reason: "cube root both sides" }
  result: { math: "\\therefore\\; f^{-1}(x) = \\sqrt[3]{x-2}", reason: "swap names" }
  check:  { math: "f(f^{-1}(x)) = x", reason: "verified" }    # optional, gets a green check

  # back-compat (the old full-width chain; each line -> a reason-less step,
  # `anim: highlight` -> the amber result):
  lines:
    - "m = \\lim_{h\\to 0} \\frac{f(2+h)-f(2)}{h}"
    - { tex: "= 1", anim: highlight }

Reveal: each row is dynamic. ids: structured -> step.0..N / result / check;
back-compat lines -> line.0..N (so existing storyboards keep working).
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT, RIGHT, MathTex, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T
from ._common import (scene_head, example_head, motif_corner, place_body, body_zone,
                      fill_gap, render_scaffold, ColumnPlan, SPINE_X, CONTENT_W, RAIL_X)

_ROW_GAP = 0.40       # between rows (min pitch; expands for tall rows)
MIN_PITCH = _ROW_GAP  # tightest inter-row gap -- sizecheck's split-capacity trigger reads this


def capacity_meta(spec: dict[str, Any]) -> list[ColumnPlan]:
    """Capacity contract (L1): the chain is one column at MIN_PITCH. Equivalent to the
    scalar MIN_PITCH sizecheck already reads -- declared so the audit reads the same
    source placement does and so the heterogeneous templates (L2) follow one interface."""
    return [ColumnPlan(min_pitch=MIN_PITCH)]


def _rows_from_spec(spec: dict[str, Any]) -> list[dict]:
    """Normalise either schema into a list of {math, reason, kind, rid, anim}."""
    rows: list[dict] = []
    if spec.get("steps") is not None or spec.get("result") is not None:
        for i, st in enumerate(spec.get("steps", [])):
            st = st if isinstance(st, dict) else {"math": st}
            rows.append({"math": str(st.get("math", "")), "reason": st.get("reason"),
                         "kind": "step", "rid": f"step.{i}", "anim": "write",
                         "mark": st.get("mark")})
        if spec.get("result") is not None:
            r = spec["result"]
            r = r if isinstance(r, dict) else {"math": r}
            rows.append({"math": str(r.get("math", "")), "reason": r.get("reason"),
                         "kind": "result", "rid": "result", "anim": "write_glow"})
        if spec.get("check") is not None:
            c = spec["check"]
            c = c if isinstance(c, dict) else {"math": c}
            rows.append({"math": str(c.get("math", "")), "reason": c.get("reason"),
                         "kind": "check", "rid": "check", "anim": "write"})
    else:  # back-compat `lines`
        for i, entry in enumerate(spec.get("lines", [])):
            if isinstance(entry, dict):
                tex, anim, reason = entry.get("tex", ""), entry.get("anim", "write"), entry.get("reason")
            else:
                tex, anim, reason = entry, "write", None
            kind = "result" if anim == "highlight" else "step"
            rows.append({"math": str(tex), "reason": reason, "kind": kind,
                         "rid": f"line.{i}", "anim": "write_glow" if kind == "result" else anim})
    return rows


def _eq_mob(row: dict, ground: str):
    """The equation mobject for a row, coloured + sized by kind; check rows get a
    trailing green checkmark."""
    if row["kind"] == "result":
        eq = MathTex(row["math"].strip(), color=T.color(ground, "accent"), font_size=T.fs(54))
        # crisper halo (was 3.0/0.45): Codex read the heavy amber glow as fuzzy/embossed.
        return brand.text_glow(eq, ground, role="accent", width=2.2, opacity=0.38)
    # a check row is a PASS, not a struck-out aside: render it as bright as the steps
    # (was role="muted"/ink_3, which read as disabled/greyed-out -- 2026-06-21 A2 finding).
    eq = MathTex(row["math"].strip(), color=T.color(ground, "primary"), font_size=T.fs("math"))
    # a trailing verdict glyph: check rows + steps marked ok -> green check; bad -> red cross.
    # The ok check is the verdict marker, so it reads at full math size with a soft green
    # glow (was scale 0.8, too small to register as the "it works" payoff).
    verdict = "ok" if row["kind"] == "check" else row.get("mark")
    if verdict in ("ok", "bad"):
        name, vrole = ("check", "success") if verdict == "ok" else ("cross", "warning")
        mark = brand.glyph(name, ground, role=vrole, size="math")
        mark.next_to(eq, RIGHT, buff=0.3)
        if verdict == "ok":
            mark = brand.text_glow(mark, ground, role="success", width=2.0, opacity=0.42)
        return VGroup(eq, mark)
    return eq


def _reason_mob(row: dict, ground: str):
    """The rail reason: result -> mono uppercase amber-ink tag; else faded upright prose."""
    reason = row.get("reason")
    if not reason:
        return None
    if row["kind"] == "result":
        return brand.eyebrow(str(reason), ground, role="amber_ink")
    # role="text" (ink_2), not "muted" (ink_3): the rail carries the reasoning the old
    # two-column walkthrough spent a whole column on -- it is teaching content, so it
    # must be readable. The smaller size + the dotted leader keep it subordinate to the
    # bright equations (ink_1) without dimming it into the "too faint" zone the lint flags.
    # Plain text and $math$-bearing reasons both render upright via prose() (Plex text +
    # Latin Modern math), so a math-bearing reason never looks different from a plain one
    # in the same rail (2026-06-21 A2 finding).
    return brand.prose(str(reason), ground, role="text", size="prose_sm")


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []
    # A worked example (scene with a `prompt:`) opens with example_head -- the problem
    # as the headline + a SOLUTION lead -- instead of a vague descriptive title; the
    # solution body sits below that lead. A scene WITHOUT a prompt is a plain derivation
    # (the template's namesake), so its eyebrow defaults to `[ derivation ]` -- NOT
    # `[ example ]`: the old default silently mislabelled every proof-step chain as an
    # example (the 2026-06-29 fix; `kicker:` still overrides the word). A scene that
    # DEPICTS a handout Example must therefore carry a `prompt:` -- lint's
    # _example_missing_prompt warns when one forgets. body_ref is whatever the body
    # sits under (SOLUTION lead or title).
    if spec.get("prompt"):
        head, body_ref = example_head(spec, ctx)
    else:
        head = scene_head(spec, ctx, label="[ derivation ]")
        body_ref = head[1].mobject
    blocks += head

    scaffold_blocks = render_scaffold(spec.get("scaffold"), ground, ctx.get("meta"))
    for sb in scaffold_blocks:
        sb.mobject.next_to(body_ref, DOWN, buff=T.TITLE_GAP).align_to(body_ref, LEFT)
        body_ref = sb.mobject
    blocks += scaffold_blocks

    content_w = CONTENT_W
    left_x = SPINE_X

    statement = None
    if spec.get("statement"):
        statement = brand.prose(spec["statement"], ground, role="primary", size="prose",
                                max_width=content_w, align="LEFT")

    rows = _rows_from_spec(spec)
    eqs = [_eq_mob(r, ground) for r in rows]
    reasons = [_reason_mob(r, ground) for r in rows]

    # Reasons snap to the FIXED Lectern rail column (was: floating at
    # left_x + eq_col_w, so the rail x drifted scene-to-scene and never aligned
    # with the other templates' right column). The dotted leader becomes a
    # TOC-style connector spanning each equation's right edge to the reason column
    # (set per row in the layout loop), so a short equation gets a long leader and
    # the link always reads. eq_col_w now only guards the rare chain wide enough to
    # reach the rail -- then that row's leader is skipped.
    eq_col_w = max((e.width for e in eqs), default=0.0)
    reason_x = RAIL_X
    reason_max_w = (SPINE_X + CONTENT_W) - reason_x

    # pre-pass: clamp reason widths, collect row heights (needed to size the chain to
    # the body zone before placing).
    heights: list[float] = []
    for r, eq, reason in zip(rows, eqs, reasons):
        if reason is not None and reason.width > reason_max_w > 0:
            reason.scale_to_fit_width(reason_max_w)
        heights.append(max(eq.height, reason.height if reason is not None else 0.0))

    # spread rows so a short chain fills the body zone rather than stranding a dead band
    # under the title + an empty lower third (Codex 2026-06-21). A statement, if present,
    # eats one slot of the zone budget. fill_gap caps the spread so tall chains keep pitch.
    zt, zb = body_zone(body_ref)
    stmt_h = (statement.height + 0.55) if statement is not None else 0.0
    row_gap = fill_gap(heights, _ROW_GAP, max(zt - zb - stmt_h, 1.5))

    # vertical layout: gap-spaced rows (fused-rows pitch so tall rows never collide)
    row_mobs: list[Any] = []
    y = 0.0
    prev_half = None
    for r, eq, reason, h in zip(rows, eqs, reasons, heights):
        half = h / 2
        if prev_half is not None:
            extra = row_gap + (0.12 if r["kind"] == "check" else 0.0)
            y -= prev_half + extra + half
        eq.move_to([left_x, y, 0], aligned_edge=LEFT)
        group = [eq]
        if reason is not None:
            reason.move_to([reason_x, y, 0], aligned_edge=LEFT)
            # TOC-style leader: spans the gap from this equation's right edge to the
            # reason column, so the connection holds whatever the equation's width
            # (was a fixed 0.67u stub anchored to the floating rail). A chain wide
            # enough to reach the rail leaves no room -> skip the leader, keep the link
            # implicit by row alignment. opacity 0.6/0.7 (Codex read 0.5/0.55 too faint).
            lead_start = eq.get_right()[0] + 0.22
            lead_end = reason_x - 0.18
            if lead_end - lead_start > 0.12:
                leader = brand.dotted_leader(
                    lead_end - lead_start, ground,
                    role="accent" if r["kind"] == "result" else "hairline_strong",
                    opacity=0.6 if r["kind"] == "result" else 0.7)
                leader.move_to([(lead_start + lead_end) / 2, y, 0])
                group += [leader, reason]
            else:
                group += [reason]
        row_mobs.append((r, VGroup(*group), eq))
        prev_half = half

    # centre statement + chain as one group in the body zone, flush left
    chain = VGroup(*[g for _, g, _ in row_mobs]) if row_mobs else None
    parts = ([statement] if statement is not None else []) + ([chain] if chain is not None else [])
    if parts:
        content = VGroup(*parts).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        place_body(content, body_ref, left_x)
        # A pure equation chain (no reason rail, no statement, no prompt header)
        # left-flush would hug the left third and strand the right ~60% empty (Codex
        # flagged cubic/rational/app as "left-heavy, large dead field"). Centre it
        # horizontally; rows stay mutually left-aligned, so it reads as a centred
        # display-equation block. A worked example with a prompt header instead anchors
        # the chain left under the SOLUTION lead (the header gives the frame balance).
        no_rail = all(not r.get("reason") for r in rows)
        if no_rail and statement is None and not spec.get("prompt"):
            content.move_to([0.0, content.get_center()[1], 0])
        else:
            content.align_to(body_ref, LEFT)

    if statement is not None:
        blocks.append(Block("statement", statement, anim="fade", static=True))
    for r, group, _eq in row_mobs:
        blocks.append(Block(r["rid"], group, anim=r["anim"], static=False))

    blocks.append(motif_corner(ground))
    return blocks

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

from manim import DOWN, LEFT, RIGHT, MathTex, Text, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T
from ._common import scene_head, motif_corner, place_body, body_zone, fill_gap

_COL_GAP = 0.36       # equation column -> reason rail
_LEADER_W = 0.67      # dotted leader length (90px)
_ROW_GAP = 0.40       # between rows (min pitch; expands for tall rows)


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
    role = "muted" if row["kind"] == "check" else "primary"
    eq = MathTex(row["math"].strip(), color=T.color(ground, role), font_size=T.fs("math"))
    # a trailing verdict glyph: check rows + steps marked ok -> green check; bad -> red cross
    verdict = "ok" if row["kind"] == "check" else row.get("mark")
    if verdict in ("ok", "bad"):
        name, vrole = ("check", "success") if verdict == "ok" else ("cross", "warning")
        mark = brand.glyph(name, ground, role=vrole, size="math")
        mark.scale(0.8).next_to(eq, RIGHT, buff=0.28)
        return VGroup(eq, mark)
    return eq


def _reason_mob(row: dict, ground: str):
    """The rail reason: result -> mono uppercase amber-ink tag; else faded italic."""
    reason = row.get("reason")
    if not reason:
        return None
    if row["kind"] == "result":
        return brand.eyebrow(str(reason), ground, role="amber_ink")
    # role="text" (ink_2), not "muted" (ink_3): the rail carries the reasoning the old
    # two-column walkthrough spent a whole column on -- it is teaching content, so it
    # must be readable. Italic + the dotted leader keep it subordinate to the bright
    # equations (ink_1) without dimming it into the "too faint" zone the lint flags.
    if "$" in str(reason):
        return brand.prose(str(reason), ground, role="text", size="prose_sm")
    return Text(str(reason), font=T.FONT_BODY, font_size=T.fs("prose_sm"),
                color=T.color(ground, "text"), slant="ITALIC")


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []
    head = scene_head(spec, ctx, label="[ example ]")
    blocks += head
    title = head[1].mobject

    content_w = T.FRAME_W - 2 * T.SIDE_GUTTER
    left_x = -T.FRAME_W / 2 + T.SIDE_GUTTER

    statement = None
    if spec.get("statement"):
        statement = brand.prose(spec["statement"], ground, role="primary", size="prose",
                                max_width=content_w, align="LEFT")

    rows = _rows_from_spec(spec)
    eqs = [_eq_mob(r, ground) for r in rows]
    reasons = [_reason_mob(r, ground) for r in rows]

    eq_col_w = max((e.width for e in eqs), default=0.0)
    rail_x = left_x + eq_col_w + _COL_GAP
    reason_x = rail_x + _LEADER_W + 0.16
    reason_max_w = (left_x + content_w) - reason_x

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
    zt, zb = body_zone(title)
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
            leader = brand.dotted_leader(
                _LEADER_W, ground,
                role="accent" if r["kind"] == "result" else "hairline_strong",
                opacity=0.6 if r["kind"] == "result" else 0.7)  # was 0.5/0.55: Codex read the rail as too faint
            leader.move_to([rail_x + _LEADER_W / 2, y, 0])
            group += [leader, reason]
        row_mobs.append((r, VGroup(*group), eq))
        prev_half = half

    # centre statement + chain as one group in the body zone, flush left
    chain = VGroup(*[g for _, g, _ in row_mobs]) if row_mobs else None
    parts = ([statement] if statement is not None else []) + ([chain] if chain is not None else [])
    if parts:
        content = VGroup(*parts).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        place_body(content, title, left_x)
        # A pure equation chain (no reason rail, no statement) left-flush would hug the
        # left third and strand the right ~60% empty (Codex flagged cubic/rational/app as
        # "left-heavy, large dead field"). Centre it horizontally; rows stay mutually
        # left-aligned, so it reads as a centred display-equation block.
        no_rail = all(not r.get("reason") for r in rows)
        if no_rail and statement is None:
            content.move_to([0.0, content.get_center()[1], 0])
        else:
            content.align_to(title, LEFT)

    if statement is not None:
        blocks.append(Block("statement", statement, anim="fade", static=True))
    for r, group, _eq in row_mobs:
        blocks.append(Block(r["rid"], group, anim=r["anim"], static=False))

    blocks.append(motif_corner(ground))
    return blocks

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
back-compat lines -> line.0..N (so existing storyboards keep working). The optional
`statement` line is part of the opening frame unless `say` names {show statement}.

A row may ask for `anim: transform` (steps[i] / result): instead of fading the finished
line in, it morphs the PREVIOUS row's equation into this one glyph by glyph, and mutes the
row it came from -- so an algebraic rewrite reads as one line changing rather than a new
line appearing.
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT, RIGHT, FadeIn, MathTex, TransformMatchingShapes, VGroup

from .. import brand
from ..blocks import Block, accent_role
from ..timing import STOCK_ANIM_SECONDS
from ..visuals import theme as T
from ._common import (scene_head, example_head, motif_corner, place_body, body_zone,
                      fill_gap, render_scaffold, reveals, ColumnPlan, SPINE_X, CONTENT_W, RAIL_X)

_ROW_GAP = 0.40       # between rows (min pitch; expands for tall rows)
MIN_PITCH = _ROW_GAP  # tightest inter-row gap -- sizecheck's split-capacity trigger reads this
_REASON_PX = T._SCALE_PX["prose_sm"]   # 一般 reason 的 authored px（A/B 開放值：35 或 38）


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
                         "kind": "step", "rid": f"step.{i}", "anim": st.get("anim") or "write",
                         "mark": st.get("mark"), "color_role": st.get("color_role")})
        if spec.get("result") is not None:
            r = spec["result"]
            r = r if isinstance(r, dict) else {"math": r}
            rows.append({"math": str(r.get("math", "")), "reason": r.get("reason"),
                         "kind": "result", "rid": "result", "anim": r.get("anim") or "write_glow",
                         "color_role": r.get("color_role")})
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


def _eq_mob(row: dict, ground: str, *, role: str):
    """The equation mobject for a row, coloured + sized by kind; check rows get a
    trailing green checkmark.

    A row MAY override its colour with `color_role:` -- that is motion primitive 5
    (跨場延續) in its cheapest form: the figure that motivated this algebra already names
    its parts by colour role (`graph` plots have had `color_role` all along), so a row can
    carry the SAME name and the viewer sees that this line is about the orange half-chord
    they were just shown. The rewatch review's complaint was exactly this: "三個區域用
    藍/橘/綠標好了，到不等式鏈全變回白字."
    """
    override = row.get("color_role")
    if row["kind"] == "result":
        role = str(override) if override else role
        eq = MathTex(row["math"].strip(), color=T.color(ground, role), font_size=T.fs(54))
        # crisper halo (was 3.0/0.45): Codex read the heavy amber glow as fuzzy/embossed.
        return brand.text_glow(eq, ground, role=role, width=2.2, opacity=0.38)
    # a check row is a PASS, not a struck-out aside: render it as bright as the steps
    # (was role="muted"/ink_3, which read as disabled/greyed-out -- 2026-06-21 A2 finding).
    eq = MathTex(row["math"].strip(), color=T.color(ground, str(override) if override else "primary"),
                 font_size=T.fs("math"))
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


TRANSFORM_SECONDS = STOCK_ANIM_SECONDS["transform"]
MUTED_OPACITY = 0.55     # what the row a transform came FROM fades back to
_DEFAULT_ANIM = {"step": "write", "result": "write_glow", "check": "write"}


def _eq_core(mob):
    """The MathTex inside a row's equation mob. `_eq_mob` wraps some rows (a result in a
    glow group, a marked row with its verdict glyph), and the morph has to run on the glyphs
    themselves, not the wrapper."""
    if isinstance(mob, MathTex):
        return mob
    for sub in getattr(mob, "submobjects", []):
        found = _eq_core(sub)
        if found is not None:
            return found
    return None


def _transform_anim(prev_eq, prev_row, this_eq):
    """An in-place rewrite: the previous row's equation morphs into this one, and the row it
    came from dims. Glyph-matching (TransformMatchingShapes), not term-matching: splitting the
    tex with `substrings_to_isolate` to get named parts breaks any row using `\\frac` (the macro
    is cut from its arguments and LaTeX refuses to compile), and it would perturb the spacing of
    the very rows it touched. Shape matching needs no change to how the row is built, so the
    terminal frame is byte-identical to the un-transformed one.

    The WHOLE previous row dims -- equation, leader and reason together. Dimming only the
    equation inverted the hierarchy: a spent row's rail annotation stayed at full ink and so
    read brighter than the equation it annotates (visual-frame audit, 2026-09-12)."""
    def anim(scene, mob, ground) -> float:
        ghost = prev_eq.copy()
        scene.add(ghost)
        rail = VGroup(*[m for m in mob.submobjects if m is not this_eq])
        scene.play(
            TransformMatchingShapes(ghost, this_eq),
            prev_row.animate.set_opacity(MUTED_OPACITY),
            *([FadeIn(rail)] if rail.submobjects else []),
            run_time=TRANSFORM_SECONDS,
        )
        return TRANSFORM_SECONDS
    return anim


def _reason_mob(row: dict, ground: str, *, role: str = "concept"):
    """The rail reason: result -> mono uppercase tag in the scene's accent ink; else faded
    upright prose.

    The tag's ink follows `accent:` like the result row and its leader already do. It used
    to be a hardcoded amber regardless of the scene's accent -- the last of the four
    written-in accents Direction B (quality round ⑨) set out to remove, and invisible until
    §3.1's derivations stopped being tagged `definition` (ochre) in the 2026-09-13 accent
    review: a blue result line under an amber tag reads as two different claims."""
    reason = row.get("reason")
    if not reason:
        return None
    if row["kind"] == "result":
        return brand.eyebrow(str(reason), ground, role=f"{role}_ink", size="tag")
    # role="text" (ink_2), not "muted" (ink_3): the rail carries the reasoning the old
    # two-column walkthrough spent a whole column on -- it is teaching content, so it
    # must be readable. The smaller size + the dotted leader keep it subordinate to the
    # bright equations (ink_1) without dimming it into the "too faint" zone the lint flags.
    # Plain text and $math$-bearing reasons both render upright via prose() (Plex text +
    # Latin Modern math), so a math-bearing reason never looks different from a plain one
    # in the same rail (2026-06-21 A2 finding).
    return brand.prose(str(reason), ground, role="text", size=_REASON_PX)


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
        statement = brand.prose(spec["statement"], ground, role="primary", size="statement",
                                max_width=content_w, align="LEFT")

    rows = _rows_from_spec(spec)
    eqs = [_eq_mob(r, ground, role=accent_role(spec)) for r in rows]
    reasons = [_reason_mob(r, ground, role=accent_role(spec)) for r in rows]

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
            # px dispatched by row kind, SAME SOURCE as the authored sizes above: a result
            # reason is an eyebrow at "tag", everything else at _REASON_PX -- keeps the clamp
            # floor equal to the authored px (closes the SP2 note; and an A/B re-tune of
            # _REASON_PX can never drift away from this guard).
            floor_px = T._SCALE_PX["tag"] if r["kind"] == "result" else _REASON_PX
            brand._clamp_shrink(reason, reason_max_w, floor_px)
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
                    role=accent_role(spec) if r["kind"] == "result" else "hairline_strong",
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
        # `{show statement}` in `say` makes the motive line enter on that beat (slide in);
        # with no marker it stays part of the opening frame, as before.
        if reveals(spec, "statement"):
            blocks.append(Block("statement", statement, anim="slide", static=False))
        else:
            blocks.append(Block("statement", statement, anim="fade", static=True))
    for i, (r, group, eq) in enumerate(row_mobs):
        # `anim: transform` morphs the row ABOVE into this one. The first row has nothing to
        # morph from, so it keeps its stock reveal -- silently, since "transform the opening
        # line" is a reasonable thing for an author to write and there is nothing to fix.
        prev_eq = _eq_core(row_mobs[i - 1][2]) if i else None
        this_eq = _eq_core(eq)
        if r["anim"] == "transform" and prev_eq is not None and this_eq is not None:
            blocks.append(Block(r["rid"], group,
                                anim=_transform_anim(prev_eq, row_mobs[i - 1][1], this_eq),
                                anim_seconds=TRANSFORM_SECONDS, static=False))
        else:
            anim = _DEFAULT_ANIM[r["kind"]] if r["anim"] == "transform" else r["anim"]
            blocks.append(Block(r["rid"], group, anim=anim, static=False))

    blocks.append(motif_corner(ground))
    return blocks

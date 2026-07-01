"""theorem_proof template -- Direction D (dark teaching frame).

Layout (2026-07-01 redesign): the statement sits in a rail card at the TOP-RIGHT
(freeing the wide band under the title), and the proof reads as a left-spine
equation chain (was a dot-led bullet list) closing on a green boxed QED:
  eyebrow "[ THEOREM ]" + title + optional motive;
  a statement card with a thick accent left bar, in the RIGHT rail;
  a "Proof" eyebrow, then the proof steps as a chain on the Lectern spine;
  a closing "Therefore ..." line in success-green with a boxed QED mark.

A proof row wide enough to reach the rail card's column drops the whole chain
BELOW the card (full width); a narrow proof sits to the LEFT of the card (two
columns). The statement-only proposition path (no proof) keeps the balanced
card+aside two-column layout unchanged.

Reveal: statement is static (the frame); each proof step and the QED line are
dynamic (proof.0/1/2, qed) so narration walks the argument via {show ...}.

YAML shape:
  template: theorem_proof
  accent: theorem
  label: "[ proposition ]"               # optional masthead eyebrow (default "[ theorem ]");
  #                                        use for propositions/lemmas/corollaries that carry a proof
  title: "..."
  statement: "If $f$ is strictly increasing ... then $f$ is one-to-one ..."
  proof: ["Take any $x_1 < x_2$ ...", "...", "..."]
  qed: "Therefore $f$ is one-to-one."     # optional closing line
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT, RIGHT, UP, Rectangle, RoundedRectangle, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T
from ._common import (scene_head, motif_corner, center_in_zone, build_aside, render_scaffold,
                      ColumnPlan, SPINE_X, CONTENT_W, PRIMARY_W, RAIL_X, RAIL_W)


_ROW_GAP = 0.5   # proof-chain min inter-row pitch (edge-to-edge); tall rows keep it


def capacity_meta(spec: dict[str, Any]) -> list[ColumnPlan]:
    """Capacity contract: the proof is now an ELASTIC equation chain on one column
    (like derivation), so it is a "stack" model at the chain's min pitch -- the audit
    reads the same tightest-packing question placement does. (Was "span": that measured
    the expanded rendered gaps and would over-warn once the chain spreads.)"""
    return [ColumnPlan(min_pitch=_ROW_GAP, model="stack")]


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []
    head = scene_head(spec, ctx, label=spec.get("label", "[ theorem ]"))
    blocks += head
    # The title block by id -- NOT head[1]: scene_head inserts a `part` indicator before
    # the title for multipage (`part:`) scenes, so head[1] is the part indicator there.
    title = next(b.mobject for b in head if b.id == "title")

    # scaffold (motive) sits under the title at full width; body content flows below it.
    # body_ref tracks the lowest header element (title, or the motive if present) so the
    # card + proof anchor below the REAL header, never colliding with a wrapped title/motive.
    scaffold_blocks = render_scaffold(spec.get("scaffold"), ground, ctx.get("meta"))
    body_ref = title
    for sb in scaffold_blocks:
        gap = 0.22 if sb.id == "scaffold.motive" else T.TITLE_GAP
        sb.mobject.next_to(body_ref, DOWN, buff=gap).align_to(body_ref, LEFT)
        body_ref = sb.mobject
    blocks += scaffold_blocks

    left = SPINE_X
    content_w = CONTENT_W
    steps = spec.get("proof", [])
    qed_text = spec.get("qed")

    # -- statement-only proposition (no proof) + enrichment aside: balanced two-column,
    #    UNCHANGED. The aside path keeps the card in the PRIMARY column with the note in
    #    the rail, the pair centred (Lectern bias). --
    use_aside = bool(spec.get("aside")) and not steps and not qed_text
    if use_aside:
        statement = brand.prose(spec.get("statement", ""), ground, role="primary",
                                size="h2", max_width=PRIMARY_W - 0.3)
        card = brand.accent_panel(statement, ground, bar_role="accent", fill_role="panel",
                                  pad=0.42, pad_x=0.6)
        aside = build_aside(spec["aside"], ground, max_width=RAIL_W)
        card.move_to([left + card.width / 2, 0, 0])
        aside.move_to([RAIL_X, 0, 0], aligned_edge=LEFT)
        center_in_zone([card, aside], body_ref)
        blocks.append(Block("statement", card, anim="fade", static=True))
        blocks.append(Block("aside", aside, anim="fade", static=True, layer="decoration"))
        blocks.append(motif_corner(ground))
        return blocks

    # -- statement card -> TOP-RIGHT rail (the redesign). The old card sat full-width
    #    directly under the title and ate the band the proof needed, leaving the right
    #    half empty; moving it into the rail frees the wide band for the proof chain.
    #    Sized to the rail interior (RAIL_W minus the panel's own horizontal pad) so it
    #    never spills past the right gutter. Kept static -- reveal timing is unchanged. --
    zone_top = body_ref.get_bottom()[1] - T.TITLE_GAP
    card_pad_x = 0.5
    inner_w = RAIL_W - 2 * card_pad_x
    stmt_text = spec.get("statement", "")
    is_formula = (stmt_text.strip().startswith("$") and stmt_text.strip().endswith("$")
                  and stmt_text.count("$") == 2)
    statement = brand.prose(stmt_text, ground, role="primary", size="h3",
                            max_width=inner_w, align="LEFT")
    # Consistent rail-width card: pad a narrow (short-formula) statement out to the rail
    # interior via a transparent spacer, so EVERY card spans the full rail (right edge on
    # the gutter) instead of a small card drifting at RAIL_X. A display formula centres in
    # the card; wrapped prose left-aligns (2026-07-01 visual polish, Codex-confirmed).
    spacer = Rectangle(width=inner_w, height=statement.height, stroke_width=0, fill_opacity=0)
    if is_formula:
        statement.move_to(spacer)
    else:
        statement.move_to(spacer.get_left(), aligned_edge=LEFT)
    card = brand.accent_panel(VGroup(spacer, statement), ground, bar_role="accent",
                              fill_role="panel", pad=0.34, pad_x=card_pad_x)
    card.move_to([RAIL_X + card.width / 2, zone_top - card.height / 2, 0])
    blocks.append(Block("statement", card, anim="fade", static=True))

    # -- proof: an equation chain on the Lectern spine (was a dot-led bullet list). Rows
    #    share the spine's left edge and flow like a derivation, closing on the green QED.
    #    A row wide enough to reach the rail card's column drops the whole chain BELOW the
    #    card (full width); otherwise the chain sits to the LEFT of the card (two columns).
    #    The chain stays flush-left on the spine -- it is NOT centred horizontally (that
    #    would fight the top-right card and break the theorem/proof grammar). --
    proof_left = left + 0.4
    proof_label = brand.eyebrow("proof", ground, role="muted")
    step_mobs = [brand.prose(p, ground, role="text", size="step",
                             max_width=content_w - 1.0) for p in steps]
    reaches_rail = any(proof_left + m.width > RAIL_X - 0.25 for m in step_mobs)

    proof_label.move_to([proof_left, zone_top - proof_label.height / 2, 0], aligned_edge=LEFT)
    blocks.append(Block("proof_label", proof_label, anim="fade", static=True))

    chain: list = []
    y = 0.0
    prev_half = None
    for i, m in enumerate(step_mobs):
        half = m.height / 2
        if prev_half is not None:
            y -= prev_half + _ROW_GAP + half
        m.move_to([proof_left, y, 0], aligned_edge=LEFT)
        blocks.append(Block(f"proof.{i}", m, anim="fade", static=False))
        chain.append(m)
        prev_half = half

    # -- QED line: a green closing line + boxed QED mark, folded into the chain rhythm
    #    (was floating low). A theorem/proposition proof CLOSES -- the green boxed QED is
    #    the right idiom, NOT derivation's amber "result". --
    if qed_text:
        line = brand.prose(qed_text, ground, role="success", size="step")
        box = RoundedRectangle(width=0.46, height=0.46, corner_radius=T.RADIUS_SM,
                               color=T.color(ground, "success"), stroke_width=3)
        mark = brand.glyph("qed", ground, role="success", size="math_sm")
        mark.scale_to_fit_height(box.height * 0.46)
        mark.move_to(box.get_center())
        qbox = VGroup(box, mark)
        qbox.next_to(line, RIGHT, buff=0.3)
        row = VGroup(line, qbox)
        half = row.height / 2
        if prev_half is not None:
            y -= prev_half + _ROW_GAP + half
        row.move_to([proof_left, y, 0], aligned_edge=LEFT)
        blocks.append(Block("qed", row, anim="flash_in", static=False))
        chain.append(row)

    # anchor the chain just below the PROOF label instead of centring it in the whole band
    # (a short 2-step proof otherwise floats mid-frame, detached from its label -- the
    # 2026-07-01 visual polish). A wide proof that reaches the rail drops below the card so
    # it still clears it. The calm lower whitespace is intentional (Lectern bias).
    if chain:
        anchor_top = proof_label.get_bottom()[1] - 0.5
        if reaches_rail:
            anchor_top = min(anchor_top, card.get_bottom()[1] - 0.4)
        dy = anchor_top - chain[0].get_top()[1]
        for m in chain:
            m.shift([0, dy, 0])
    blocks.append(motif_corner(ground))
    return blocks

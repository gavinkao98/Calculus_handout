"""theorem_proof template -- Direction D (dark teaching frame).

Matches screenshots/05-theorem_proof.png + B_Theorem:
  eyebrow "[ THEOREM ]" + title;
  a statement card with a thick gold left bar (theorem accent);
  a "Proof" eyebrow, then dot-led proof steps;
  a closing "Therefore ..." line in success-green with a boxed QED mark.

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

from manim import DOWN, LEFT, RIGHT, UP, RoundedRectangle, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T
from ._common import (scene_head, motif_corner, center_in_zone, build_aside, ColumnPlan,
                      SPINE_X, CONTENT_W, PRIMARY_W, RAIL_X, RAIL_W)


def capacity_meta(spec: dict[str, Any]) -> list[ColumnPlan]:
    """Capacity contract (L2): the statement card + proof steps + QED form one fixed-rhythm
    cascade in the left column, so measure its actual span (span model). min_pitch unused."""
    return [ColumnPlan(min_pitch=0.0, model="span")]


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []
    blocks += scene_head(spec, ctx, label=spec.get("label", "[ theorem ]"))
    title = blocks[1].mobject

    left = SPINE_X
    content_w = CONTENT_W

    steps = spec.get("proof", [])
    qed_text = spec.get("qed")
    # An enrichment aside (L3) applies only to a STATEMENT-ONLY proposition (no proof
    # cascade to fill the zone); with a proof present the proof IS the content and the
    # aside collapses (ignored). For it the statement narrows to the primary column.
    use_aside = bool(spec.get("aside")) and not steps and not qed_text

    # -- statement in a gold-barred panel (the textbook "theorem frame") --
    # prose(): a pure-prose statement (no $) must NOT go to math_line -- that
    # routes to MathTex and renders the whole sentence as run-together math
    # italic. prose() sends it to Text instead, and still handles inline $math$.
    stmt_w = (PRIMARY_W - 0.3) if use_aside else (content_w - 1.4)
    statement = brand.prose(spec.get("statement", ""), ground,
                            role="primary", size="h2", max_width=stmt_w)
    card = brand.accent_panel(statement, ground, bar_role="accent", fill_role="panel",
                              pad=0.42, pad_x=0.6)

    if use_aside:
        # balanced two-column: card left + enrichment aside in the rail, the pair centred
        # (Lectern bias), instead of the pinned-high card the proof path uses over empty space.
        aside = build_aside(spec["aside"], ground, max_width=RAIL_W)
        card.move_to([left + card.width / 2, 0, 0])
        aside.move_to([RAIL_X, 0, 0], aligned_edge=LEFT)
        center_in_zone([card, aside], title)
        blocks.append(Block("statement", card, anim="fade", static=True))
        blocks.append(Block("aside", aside, anim="fade", static=True, layer="decoration"))
        blocks.append(motif_corner(ground))
        return blocks

    # The card sits at its designed y; a tall (wrapped) statement grows upward,
    # so cap its top below the title -- the label/steps/qed cascade follows.
    card_y = min(1.55, title.get_bottom()[1] - 0.32 - card.height / 2)
    card.move_to([left + card.width / 2, card_y, 0])
    blocks.append(Block("statement", card, anim="fade", static=True))

    # -- proof label + steps --
    # The label sits at its designed y unless a tall (wrapped) statement card
    # reaches down into it -- then label and steps shift down together.
    proof_label = brand.eyebrow("proof", ground, role="muted")
    label_y = min(0.3, card.get_bottom()[1] - 0.35)
    proof_label.move_to([left + 0.4, label_y, 0], aligned_edge=LEFT)
    blocks.append(Block("proof_label", proof_label, anim="fade", static=True))
    proof_content: list = []   # steps + qed, centred below the label (card+label stay put)

    step_gap = 0.95     # designed rhythm = MINIMUM pitch
    min_clear = 0.35    # air kept between tall (wrapped) steps -- pitch expands,
    #                     steps never collide (the recap_cards fused-rows class)
    y = label_y - 0.7
    prev_half = None
    for i, p in enumerate(steps):
        dot = brand.text_glow(brand.plot_dot(ground, role="secondary", r=0.07),
                              ground, role="secondary", width=5, opacity=0.45)
        # prose() wraps a long step instead of shrinking it, so the steps keep a
        # uniform size -- a scaled-down long step beside a short one is the same
        # mismatch class as the recap points.
        txt = brand.prose(p, ground, role="text", size="step", max_width=content_w - 1.0)
        first_line = txt.submobjects[0] if isinstance(txt, VGroup) and txt.submobjects else txt
        dot.next_to(first_line, LEFT, buff=0.3)
        row = VGroup(dot, txt)
        half = row.height / 2
        if prev_half is None:
            # first step: clear the label too, if the step wraps tall
            y = min(y, label_y - (0.2 + proof_label.height / 2 + half))
        else:
            y -= max(step_gap, prev_half + min_clear + half)
        row.move_to([left + 0.4, y, 0], aligned_edge=LEFT)
        blocks.append(Block(f"proof.{i}", row, anim="fade", static=False))
        proof_content.append(row)
        prev_half = half

    # -- QED line --
    if qed_text:
        line = brand.prose(qed_text, ground, role="success", size="step")
        box = RoundedRectangle(width=0.46, height=0.46, corner_radius=T.RADIUS_SM,
                               color=T.color(ground, "success"), stroke_width=3)
        mark = brand.glyph("qed", ground, role="success", size="math_sm")
        mark.scale_to_fit_height(box.height * 0.46)
        mark.move_to(box.get_center())
        qbox = brand.text_glow(VGroup(box, mark), ground, role="success", width=7, opacity=0.4)
        qbox.next_to(line, RIGHT, buff=0.3)
        row = VGroup(line, qbox)
        half = row.height / 2
        if prev_half is None:
            y_qed = y - 0.1  # no steps: legacy position below the label zone
        else:
            y_qed = y - max(step_gap, prev_half + min_clear + half) - 0.1
        row.move_to([left + 0.4, y_qed, 0], aligned_edge=LEFT)
        blocks.append(Block("qed", row, anim="flash_in", static=False))
        proof_content.append(row)

    # centre the proof (steps + qed) in the zone below the label, so a short proof
    # no longer floats high under the statement card with an empty lower zone.
    center_in_zone(proof_content, proof_label)
    blocks.append(motif_corner(ground))
    return blocks

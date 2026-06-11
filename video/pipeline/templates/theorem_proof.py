"""theorem_proof template -- Direction B (dark teaching frame).

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
  title: "..."
  statement: "If $f$ is strictly increasing ... then $f$ is one-to-one ..."
  proof: ["Take any $x_1 < x_2$ ...", "...", "..."]
  qed: "Therefore $f$ is one-to-one."     # optional closing line
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT, RIGHT, UP, Square, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T
from ._common import scene_head, motif_corner


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []
    blocks += scene_head(spec, ctx, label="[ theorem ]")
    title = blocks[1].mobject

    left = -T.FRAME_W / 2 + T.SIDE_GUTTER
    content_w = T.FRAME_W - 2 * T.SIDE_GUTTER

    # -- statement card with gold left bar --
    # prose(): a pure-prose statement (no $) must NOT go to math_line -- that
    # routes to MathTex and renders the whole sentence as run-together math
    # italic ("Afunction...one-to-one"). prose() sends it to Text instead, and
    # still handles a statement that does carry inline $math$.
    statement = brand.prose(spec.get("statement", ""), ground,
                            role="primary", size="h2", max_width=content_w - 0.6)
    bar = brand.vrule(statement.height + 0.3, ground, role="accent", width=6)
    bar.next_to(statement, LEFT, buff=0.35)
    card = VGroup(bar, statement)
    # The card sits at its designed y; a tall (wrapped) statement grows upward,
    # so cap its top below the title -- the label/steps/qed cascade follows.
    card_y = min(1.4, title.get_bottom()[1] - 0.2 - card.height / 2)
    card.move_to([left, card_y, 0], aligned_edge=LEFT)
    blocks.append(Block("statement", card, anim="fade", static=True))

    # -- proof label + steps --
    # The label sits at its designed y unless a tall (wrapped) statement card
    # reaches down into it -- then label and steps shift down together.
    proof_label = brand.eyebrow("proof", ground, role="muted")
    label_y = min(0.3, card.get_bottom()[1] - 0.35)
    proof_label.move_to([left + 0.4, label_y, 0], aligned_edge=LEFT)
    blocks.append(Block("proof_label", proof_label, anim="fade", static=True))

    steps = spec.get("proof", [])
    step_gap = 0.95     # designed rhythm = MINIMUM pitch
    min_clear = 0.35    # air kept between tall (wrapped) steps -- pitch expands,
    #                     steps never collide (the recap_cards fused-rows class)
    y = label_y - 0.7
    prev_half = None
    for i, p in enumerate(steps):
        dot = brand.plot_dot(ground, role="secondary", r=0.06)
        # prose() wraps a long step instead of shrinking it, so the steps keep a
        # uniform size -- a scaled-down long step beside a short one is the same
        # mismatch class as the recap points.
        txt = brand.prose(p, ground, role="text", size="step", max_width=content_w - 1.0)
        dot.next_to(txt, LEFT, buff=0.3, aligned_edge=UP)
        row = VGroup(dot, txt)
        half = row.height / 2
        if prev_half is None:
            # first step: clear the label too, if the step wraps tall
            y = min(y, label_y - (0.2 + proof_label.height / 2 + half))
        else:
            y -= max(step_gap, prev_half + min_clear + half)
        row.move_to([left + 0.4, y, 0], aligned_edge=LEFT)
        blocks.append(Block(f"proof.{i}", row, anim="fade", static=False))
        prev_half = half

    # -- QED line --
    qed_text = spec.get("qed")
    if qed_text:
        line = brand.prose(qed_text, ground, role="success", size="step")
        box = Square(side_length=0.42, color=T.color(ground, "success"), stroke_width=3)
        mark = brand.glyph("qed", ground, role="success", size="math_sm")
        mark.scale_to_fit_height(box.height * 0.5)
        mark.move_to(box.get_center())
        qbox = VGroup(box, mark)
        qbox.next_to(line, RIGHT, buff=0.3)
        row = VGroup(line, qbox)
        half = row.height / 2
        if prev_half is None:
            y_qed = y - 0.1  # no steps: legacy position below the label zone
        else:
            y_qed = y - max(step_gap, prev_half + min_clear + half) - 0.1
        row.move_to([left + 0.4, y_qed, 0], aligned_edge=LEFT)
        blocks.append(Block("qed", row, anim="flash_in", static=False))

    blocks.append(motif_corner(ground))
    return blocks

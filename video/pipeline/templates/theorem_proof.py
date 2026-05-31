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

    left = -T.FRAME_W / 2 + T.SIDE_GUTTER
    content_w = T.FRAME_W - 2 * T.SIDE_GUTTER

    # -- statement card with gold left bar --
    statement = brand.math_line(spec.get("statement", ""), ground,
                                role="primary", size="h2")
    # math_line auto-routes to Tex when it sees '$', so a mixed sentence renders.
    if statement.width > content_w - 0.6:
        statement.scale_to_fit_width(content_w - 0.6)
    bar = brand.vrule(statement.height + 0.3, ground, role="accent", width=6)
    bar.next_to(statement, LEFT, buff=0.35)
    card = VGroup(bar, statement)
    card.move_to([left, 1.4, 0], aligned_edge=LEFT)
    blocks.append(Block("statement", card, anim="fade", static=True))

    # -- proof label + steps --
    proof_label = brand.eyebrow("proof", ground, role="muted")
    proof_label.move_to([left + 0.4, 0.3, 0], aligned_edge=LEFT)
    blocks.append(Block("proof_label", proof_label, anim="fade", static=True))

    steps = spec.get("proof", [])
    step_gap = 0.85
    proof_top = -0.4
    for i, p in enumerate(steps):
        dot = brand.plot_dot(ground, role="secondary", r=0.06)
        txt = brand.math_line(p, ground, role="text", size="step")
        if txt.width > content_w - 1.0:
            txt.scale_to_fit_width(content_w - 1.0)
        dot.next_to(txt, LEFT, buff=0.3)
        row = VGroup(dot, txt)
        row.move_to([left + 0.4, proof_top - i * step_gap, 0], aligned_edge=LEFT)
        blocks.append(Block(f"proof.{i}", row, anim="fade", static=False))

    # -- QED line --
    qed_text = spec.get("qed")
    if qed_text:
        line = brand.math_line(qed_text, ground, role="success", size="step")
        box = Square(side_length=0.42, color=T.color(ground, "success"), stroke_width=3)
        mark = brand.glyph("qed", ground, role="success", size="math_sm")
        mark.scale_to_fit_height(box.height * 0.5)
        mark.move_to(box.get_center())
        qbox = VGroup(box, mark)
        qbox.next_to(line, RIGHT, buff=0.3)
        row = VGroup(line, qbox)
        row.move_to([left + 0.4, proof_top - len(steps) * step_gap - 0.1, 0], aligned_edge=LEFT)
        blocks.append(Block("qed", row, anim="flash_in", static=False))

    blocks.append(motif_corner(ground))
    return blocks

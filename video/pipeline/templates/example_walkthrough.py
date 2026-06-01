"""example_walkthrough template -- Direction B (dark teaching frame).

Matches screenshots/03-example_walkthrough.png + B_Example in dir-b-templates:
  eyebrow "[ EXAMPLE ]" + title (B_SceneHead);
  two columns separated by a vertical hairline --
    LEFT  : numbered reasoning steps (01/02/03 + text);
    RIGHT : the worked math for each step, vertically aligned to its step,
            with a trailing  marker per step;
  bottom: a one-line takeaway with a short coral/accent rule.

Each step's right-hand math is a dynamic block (math.0, math.1, ...) so the
narration reveals the algebra line by line via {show math.N}. The left text and
the markers come in with their row (static frame), matching the reveal model of
the other templates.

YAML shape:
  template: example_walkthrough
  accent: example
  title: "..."
  steps:
    - { text: "...", math: "...", mark: ok|bad|none, hot: true|false }
  takeaway: "..."          # optional bottom line
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, LEFT, RIGHT, UP, VGroup

from .. import brand
from ..blocks import Block, accent_role
from ..visuals import theme as T
from ._common import scene_head, motif_corner

_MARK = {"ok": ("check", "success"), "bad": ("cross", "warning")}


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []

    blocks += scene_head(spec, ctx, label="[ example ]")

    steps = spec.get("steps", [])
    left_x = -T.FRAME_W / 2 + T.SIDE_GUTTER          # left column anchor
    right_x = 1.2                                      # right column anchor
    col_top = 1.4                                      # below the header
    row_gap = 1.25

    left_rows, right_rows = [], []
    for i, st in enumerate(steps):
        # left: 0N index + reasoning text
        idx = brand.eyebrow(f"0{i+1}", ground, role="secondary")
        # prose() routes markup ($math$ / \\ break) to Tex, plain text to wrapped
        # Text -- so a step like "Identity is its\\ own inverse." breaks instead
        # of printing the "\\" literally.
        txt = brand.prose(st.get("text", ""), ground, role="text", size="step",
                          max_width=4.7, align="LEFT")
        idx.next_to(txt, LEFT, buff=0.3, aligned_edge=UP)
        left_rows.append(VGroup(idx, txt))

        # right: worked math (+ optional mark), coloured by state
        hot = st.get("hot")
        mark = st.get("mark", "none")
        role = "accent" if hot else ("warning" if mark == "bad" else "math")
        m = brand.math_line(st.get("math", ""), ground, role=role, size="math")
        parts = [m]
        if mark in _MARK:
            glyph_name, crole = _MARK[mark]
            gm = brand.glyph(glyph_name, ground, role=crole, size="math")
            gm.next_to(m, RIGHT, buff=0.3)
            parts.append(gm)
        right_rows.append(VGroup(*parts))

    # vertically place rows in lockstep so left text & right math share a baseline.
    # move_to(..., aligned_edge=LEFT) is the positioning pattern proven to work in
    # definition_math/intro/outro; set_y/align_to combos were the failing path.
    for i, (lr, rr) in enumerate(zip(left_rows, right_rows)):
        y = col_top - i * row_gap
        lr.move_to([left_x, y, 0], aligned_edge=LEFT)
        rr.move_to([right_x, y, 0], aligned_edge=LEFT)

    # centre divider between the columns
    if steps:
        div = brand.vrule(row_gap * len(steps) - 0.2, ground, role="hairline")
        div.move_to([(left_x + 4.9 + right_x) / 2 - 0.2, col_top - (len(steps) - 1) * row_gap / 2, 0])
        blocks.append(Block("divider", div, anim="fade", static=True))

    # left rows are static (the frame); right math reveals per beat
    for i, lr in enumerate(left_rows):
        blocks.append(Block(f"step.{i}", lr, anim="fade", static=True))
    for i, rr in enumerate(right_rows):
        blocks.append(Block(f"math.{i}", rr, anim="write", static=False))

    # bottom takeaway
    take = spec.get("takeaway")
    if take:
        rule = brand.hrule(0.5, ground, role="warning", stroke=2.5)
        cap = brand.prose(take, ground, role="warning", size="step",
                          max_width=T.FRAME_W - 2 * T.SIDE_GUTTER - 0.8)
        rule.next_to(cap, LEFT, buff=0.25)
        grp = VGroup(rule, cap)
        grp.move_to([left_x, -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.3, 0], aligned_edge=LEFT)
        blocks.append(Block("takeaway", grp, anim="fade", static=False))

    blocks.append(motif_corner(ground))
    return blocks

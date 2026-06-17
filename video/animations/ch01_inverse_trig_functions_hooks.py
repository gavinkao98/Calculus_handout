"""§1.2 Inverse Trigonometric Functions -- custom hook animations (5 cues from the
content script / storyboard `# HOOK(第二輪)` markers).

Each factory follows the hook contract (pipeline/templates/__init__._apply_hook):
it receives the TEMPLATE's blocks and returns the final list. It replaces the
mobject of an existing reveal id (so the storyboard's {show ...} markers and the
approved narration stay untouched) and/or attaches a CALLABLE anim that
choreographs the bespoke manim inside that beat (pipeline/blocks.py:play_block
just reports the seconds spent, preserving the audio-driven alignment).

Deleting a scene's `hook:` line restores the stock template scene -- the
template payload in the storyboard is kept as the no-hook fallback.

Per CONTENT_METHODOLOGY §5, this generated code is treated like narration:
the user reviews the rendered result before it is final.

The five hooks (scene id -> cue):
  sine_is_not_one_to_one    a horizontal line sweeps down; the crossings flash
  restrict_sine_branch      the central branch lights up; a dot rides -1 -> 1
  evaluating_arcsin         Pythagoras fills in the adjacent side of the triangle
  principal_value_trap      a ball bobs along h = cos t (one value recurs)
  restrict_tangent_branch   the tangent is drawn climbing -inf -> +inf
"""
from __future__ import annotations

import numpy as np
from manim import (
    Create,
    Dot,
    FadeIn,
    Flash,
    GrowFromCenter,
    MoveAlongPath,
    VGroup,
    smooth,
)

from pipeline.blocks import Block
from pipeline.visuals import theme as T

UP = np.array([0.0, 1.0, 0.0])
DOWN = np.array([0.0, -1.0, 0.0])
RIGHT = np.array([1.0, 0.0, 0.0])
LEFT = np.array([-1.0, 0.0, 0.0])


# ---------------------------------------------------------------- helpers


def _by_id(blocks: list[Block]) -> dict[str, Block]:
    return {b.id: b for b in blocks}


def _slide_line_down(scene, mob, g, *, drop=1.7, rt=0.85):
    """Reveal a horizontal guide line by sweeping it down into place (a horizontal
    line scanning the graph), instead of a flat fade. Reused from the §1.1 HLT
    hook -- same gesture, here scanning the sine wave."""
    final = mob.get_center().copy()
    mob.shift(UP * drop)
    scene.add(mob)
    scene.play(mob.animate.move_to(final), run_time=rt, rate_func=smooth)
    return rt


def _pop_crossing(role):
    """A crossing point grows in, then flashes in `role` colour -- marks where the
    sweep line meets the curve (a repeated output, an endpoint of the branch)."""
    def _f(scene, mob, g):
        scene.play(GrowFromCenter(mob), run_time=0.35)
        scene.play(Flash(mob.get_center(), color=T.color(g, role), line_length=0.18,
                         num_lines=12, flash_radius=0.34), run_time=0.5)
        scene.add(mob)
        return 0.85
    return _f


# ================================================================ hook 1
# sine_is_not_one_to_one -- 水平虛線(plot.1)自上而下滑入 y=1/2,沿 sine 波閃示
# 多個同高交點(plot.2..5,往兩側無窮),凸顯「一個輸出 → 無窮多角度」。


def sine_is_not_one_to_one(spec, ctx, blocks):
    ids = _by_id(blocks)
    ids["plot.1"].anim = _slide_line_down
    for pid in ("plot.2", "plot.3", "plot.4", "plot.5"):
        ids[pid].anim = _pop_crossing("warning")
    return blocks


# ================================================================ hook 2
# restrict_sine_branch -- 中央分支(plot.1,accent)Create 點亮,一點沿分支由 (-π/2,-1)
# 滑到 (π/2,1)(單調掃過 [-1,1]);端點(plot.2/3)pop。完整 sine(plot.0,muted)在底襯。


def restrict_sine_branch(spec, ctx, blocks):
    ids = _by_id(blocks)

    def play_branch(scene, mob, g):
        # mob = VGroup(glow, graph, label) for the highlighted central branch.
        curve = mob[1]
        scene.play(Create(mob), run_time=0.8)
        tracer = Dot(curve.get_start(), radius=0.085, color=T.color(g, "accent")).set_z_index(3)
        scene.add(tracer)
        scene.play(MoveAlongPath(tracer, curve), run_time=1.3, rate_func=smooth)
        scene.remove(tracer)
        scene.add(mob)
        return 2.1

    ids["plot.1"].anim = play_branch
    ids["plot.2"].anim = _pop_crossing("accent")
    ids["plot.3"].anim = _pop_crossing("accent")
    return blocks


# ================================================================ hook 3
# evaluating_arcsin -- 參考三角形建構:對邊(plot.0)、斜邊(plot.1)、角 θ(plot.3)先給,
# 鄰邊(plot.2)由 Pythagoras「填入」——Create 畫出 + Flash 強調是算出來的。


def evaluating_arcsin(spec, ctx, blocks):
    ids = _by_id(blocks)

    def play_adjacent(scene, mob, g):
        # mob = VGroup(adjacent line, "2√2" label). Draw the computed base, then a
        # flash: the Pythagorean theorem just handed us the missing side.
        line = mob[0]
        scene.play(Create(line), run_time=0.7)
        scene.play(Flash(line.get_center(), color=T.color(g, "accent"), line_length=0.16,
                         num_lines=12, flash_radius=0.3), run_time=0.45)
        scene.add(mob)
        return 1.15

    ids["plot.2"].anim = play_adjacent
    return blocks


# ================================================================ hook 4
# principal_value_trap -- 小球沿 h=cos t(plot.0)上下 bob(MoveAlongPath),顯示高度
# 反覆達 1;真正達 1 的時刻(plot.2,t=2πn)Flash。arccos(1)=0(plot.3)以 stock 進場。


def principal_value_trap(spec, ctx, blocks):
    ids = _by_id(blocks)

    def play_bob(scene, mob, g):
        # mob = VGroup(glow, graph, label) for h(t)=cos t over t in [10, 15.5].
        curve = mob[1]
        scene.play(Create(mob), run_time=0.8)
        ball = Dot(curve.get_start(), radius=0.1, color=T.color(g, "secondary")).set_z_index(3)
        scene.add(ball)
        scene.play(MoveAlongPath(ball, curve), run_time=1.7, rate_func=smooth)
        scene.remove(ball)
        scene.add(mob)
        return 2.5

    ids["plot.0"].anim = play_bob
    ids["plot.2"].anim = _pop_crossing("accent")
    return blocks


# ================================================================ hook 5
# restrict_tangent_branch -- tangent(plot.2,y_clip)以 Create 由左下(趨 -∞)畫到
# 右上(趨 +∞)即為「攀升」本身;clip 後曲線為多段,故用 Create(非 MoveAlongPath)穩健。


def restrict_tangent_branch(spec, ctx, blocks):
    ids = _by_id(blocks)

    def play_climb(scene, mob, g):
        # The y_clip tangent is a multi-segment VGroup; Create draws it in point
        # order (bottom-left -> top-right) = the climb. (A MoveAlongPath dot would
        # need a single-path mobject, which the clipped curve is not.)
        scene.play(Create(mob), run_time=1.8, rate_func=smooth)
        scene.add(mob)
        return 2.0

    ids["plot.2"].anim = play_climb
    return blocks

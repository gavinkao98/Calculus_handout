"""§3.1 Derivatives of Sine and Cosine -- custom hook animations (3 cues from
the LOCKED content script / storyboard `animation_cue` specs).

Each factory follows the hook contract (pipeline/templates/__init__._apply_hook):
it receives the TEMPLATE's blocks and returns the final list. It may drop the
stock graph's `axes` block, build a bespoke figure, and append new reveal
blocks whose ids match the storyboard's {show ...} markers. Deleting a scene's
`hook:` line restores the stock template scene.

Per CONTENT_METHODOLOGY §5, this generated code is treated like narration: the
user reviews the rendered result before it is final; render failures are
patched smallest-first.

The four hooks (scene id -> Figure -> cue):
  sector_inequality    Figure 3.1  nested unit-circle areas  (tri_inner, sector,
                                   tri_outer, ineq)
  chord_vs_arc         (no book figure) half-chord vs arc on the unit circle, laid
                                   down side by side (circle, nudge, chord_arc,
                                   straighten)
  slope_equals_height  Figure 3.3  sin tangents vs cos heights (tan_0,
                                   tan_halfpi, tan_pi, cos_dots)
  shm_stacked_graphs   Figure 3.4  s/s'/s'' over one time axis, s''=-s
                                   (g_s, g_v, g_a, mirror)
  toward_the_chain_rule  end-of-section trio -> three chip cards, solved vs
                                   not-yet (math.0; Task 14 #6)
  derivative_cycle       Remark 3.1 -> 4-node ring diagram, linear chain closed
                                   into a cycle (math.0; Task 14 #3)
"""
from __future__ import annotations

import numpy as np
from manim import (
    AnnularSector,
    Arc,
    Arrow,
    Axes,
    BackgroundRectangle,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    Polygon,
    Rectangle,
    ReplacementTransform,
    SurroundingRectangle,
    TransformMatchingShapes,
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
    linear,
    smooth,
    there_and_back,
)

from pipeline import brand
from pipeline import focus
from pipeline import pacing
from pipeline import timing as TM
from pipeline.blocks import Block, play_block
from pipeline.visuals import theme as T

PI = np.pi
UP = np.array([0.0, 1.0, 0.0])
DOWN = np.array([0.0, -1.0, 0.0])
LEFT = np.array([-1.0, 0.0, 0.0])
RIGHT = np.array([1.0, 0.0, 0.0])
DL = np.array([-1.0, -1.0, 0.0])
DR = np.array([1.0, -1.0, 0.0])
UL = np.array([-1.0, 1.0, 0.0])


def _by_id(blocks: list[Block]) -> dict[str, Block]:
    return {b.id: b for b in blocks}


def _centre_in_zone(title_mob, group, *, bottom_pad: float = 0.45) -> None:
    """Centre *group* vertically in the zone between the title and the bottom
    safe margin (shared with the §1.1 hooks)."""
    zone_top = title_mob.get_bottom()[1] - 0.55
    zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN + bottom_pad
    group.move_to([0, (zone_top + zone_bottom) / 2, 0])


# Both report the renderer's clock (see `_spent`), not a constant. They used to claim
# 0.65 / 0.75 s for a 0.55 / 0.65 s play -- 0.10 s of OVER-report each, the opposite sign
# to the frame-quantisation loss, which the beat's hold then had to give back: measured on
# slope_equals_height (three _draw plus one _fade) the scene ran 0.41 s SHORT of its
# narration. Nothing in the history or the comments makes that 0.10 s deliberate, so it is
# read as a slip, not padding.
def _fade(scene, mob, g):
    t0 = _elapsed(scene)
    scene.play(FadeIn(mob), run_time=0.55)
    scene.add(mob)
    return _spent(scene, t0, 0.55)


def _draw(scene, mob, g):
    t0 = _elapsed(scene)
    scene.play(Create(mob), run_time=0.65)
    scene.add(mob)
    return _spent(scene, t0, 0.65)


# ================================================================ hook 1
# sector_inequality (Figure 3.1) -- on the unit circle the inscribed triangle
# OAB sits inside the sector OAB, which sits inside the outer triangle OAC. The
# source figure (left) builds that nested picture as narration names each region;
# a congruent copy of each region then peels off and slides onto a shared
# baseline on the right at true relative size, turning 1/2 sin t <= 1/2 t <=
# 1/2 tan t into a visible ordering of three SEPARATED shapes (not three
# overlapping fills). Reveal ids are unchanged (tri_inner, sector, tri_outer,
# ineq), so the LOCKED narration + {show ...} cues need no edit.


def sector_inequality(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    title = ids["title"].mobject
    out = [b for b in blocks if b.id != "axes"]   # we draw the circle ourselves

    R = 2.4                                          # was 1.45 -- enlarged to fill the empty
                                                      # band under the old (smallish) figure;
                                                      # the right-side glyphs are CONGRUENT
                                                      # copies of the same R (see docstring),
                                                      # so their baseline spacing below widens
                                                      # to match instead of letting them touch
    th = 0.72                                       # representative angle (~41 deg)
    B_off = R * np.array([np.cos(th), np.sin(th), 0.0])   # apex of triangle OAB
    C_off = np.array([R, R * np.tan(th), 0.0])            # apex of triangle OAC

    text = T.color(ground, "text")
    mut = T.color(ground, "muted")
    amber = T.color(ground, "accent")
    green = T.color(ground, "success")
    strategy = T.color(ground, "strategy")

    def _tri(o, apex_off, col, fop, z):
        return Polygon(o, o + np.array([R, 0.0, 0.0]), o + apex_off,
                       color=col, fill_opacity=fop, stroke_width=2.5).set_z_index(z)

    def _sec(o, col, fop, z):
        return AnnularSector(inner_radius=0.0, outer_radius=R, angle=th,
                             start_angle=0.0, arc_center=o, color=col,
                             fill_opacity=fop, stroke_width=2.5).set_z_index(z)

    # Main-figure fills stack OPAQUE (not translucent): OAB (amber) sits inside
    # the sector (strategy), which sits inside OAC (green), so painting largest-
    # first at increasing z-index (outer=1 -> sector=2 -> inner=3) lets each
    # later fill fully mask the part of the one below it -- three clean colour
    # bands (the ring between sector/outer edges) instead of the old low-alpha
    # stack (0.10/0.30/0.45) whose overlaps blended into a muddy teal.
    MAIN_FOP = 0.88

    # -- left: source figure (scaffold static; regions revealed in place) --------
    O = np.array([-4.55, -0.40, 0.0])
    A = O + np.array([R, 0.0, 0.0])
    B = O + B_off
    C = O + C_off

    quarter = Arc(radius=R, start_angle=0.0, angle=PI / 2, arc_center=O,
                  color=mut, stroke_width=2.0)
    xaxis = Line(O + 0.25 * LEFT, A + 0.5 * RIGHT, color=mut, stroke_width=1.5)
    yaxis = Line(O + 0.25 * DOWN, O + np.array([0.0, R + 0.5, 0.0]),
                 color=mut, stroke_width=1.5)
    tangent = DashedLine(A, C, color=mut, stroke_width=2.0, dash_length=0.08)
    # O->C split at B: the narration introduces B ("the point at angle theta") and only
    # THEN extends the radius to the tangent ("...gives C"). Two collinear segments of the
    # same colour/width render identically to the old single line once both are up.
    radius_OB = Line(O, B, color=text, stroke_width=2.0)
    ext_BC = Line(B, C, color=text, stroke_width=2.0)
    chord_OA = Line(O, A, color=text, stroke_width=2.0)

    dots = VGroup(*[Dot(p, radius=0.045, color=text) for p in (O, A, B, C)])
    lO = MathTex("O", color=text, font_size=T.fs("label")).next_to(O, DL, buff=0.10)
    lA = MathTex("A", color=text, font_size=T.fs("label")).next_to(A, DR, buff=0.08)
    # B's label goes UL of B -- above the OC line, the one direction with no fill under it --
    # and far enough out (0.14, was 0.06) that it no longer reads as painted on the arc (R2).
    lB = MathTex("B", color=text, font_size=T.fs("label")).next_to(B, UL, buff=0.14)
    lC = MathTex("C", color=text, font_size=T.fs("label")).next_to(C, RIGHT, buff=0.10)
    arc_th = Arc(radius=0.34, start_angle=0.0, angle=th, arc_center=O,
                 color=text, stroke_width=2.0)
    # the three theta-carrying labels go through brand.math_line so the deck's
    # meta.color_map (theta -> concept) reaches them -- a bare MathTex(color=text) left the
    # figure's theta white while every equation's theta was ochre (V10 blocking, 2026-09-13).
    lth = brand.math_line(r"\theta", ground, role="text", size="label").move_to(
        O + 0.55 * np.array([np.cos(th / 2), np.sin(th / 2), 0.0]))

    # dimension labels on the source construction so a paused viewer can see WHY
    # each area is 1/2 sin, 1/2 theta, 1/2 tan: shared base = 1, the inner height
    # sin(theta) (dropped from B to OA), the outer height tan(theta) (segment AC).
    mid_OA = (O + A) / 2.0
    l_base = MathTex("1", color=text, font_size=T.fs("label")).next_to(mid_OA, DOWN, buff=0.14)
    footB = np.array([B[0], O[1], 0.0])
    drop_sin = DashedLine(B, footB, color=mut, stroke_width=1.6, dash_length=0.06)
    l_sin = brand.math_line(r"\sin\theta", ground, role="text", size="label").next_to(drop_sin, LEFT, buff=0.05)
    # sits on AC's outer (right) edge, below C's own label so the two never
    # crowd each other -- 0.62*(A->C) instead of the true midpoint leaves lC
    # (near the top, at C) and l_tan clearly separated.
    tan_anchor = A + 0.62 * (C - A)
    l_tan = brand.math_line(r"\tan\theta", ground, role="text", size="label").next_to(tan_anchor, RIGHT, buff=0.12)
    dim = (l_base, drop_sin, l_sin, l_tan)

    for m in (radius_OB, ext_BC, chord_OA, dots, lO, lA, lB, lC, arc_th, lth, *dim):
        m.set_z_index(5)
    # The construction is no longer one static slab. Beat 0 of this scene used to be 37.6
    # seconds of narration over a finished picture -- the longest still in the whole film
    # (six-lens review, level (1)). It is now built in the order the narration builds it:
    #   stage_circle : "we compare three areas on a circle of radius one"
    #   stage_frame  : "A is at (1,0), B is the point at angle theta"
    #   stage_apex   : "extending the radius to the tangent at A gives C"
    #   ... the three regions, the inequality, then LAST the evenness aside (below):
    #   it used to sit second and stood between "here is the new tool" and the figure.
    # `scaffold` stays assembled for layout (centring + the gates measure the same figure).
    dotO, dotA, dotB, dotC = dots
    stage_circle = VGroup(quarter, xaxis, yaxis)
    stage_frame = VGroup(chord_OA, radius_OB, dotO, dotA, dotB, lO, lA, lB,
                         arc_th, lth, l_base, drop_sin, l_sin)
    stage_apex = VGroup(ext_BC, tangent, dotC, lC, l_tan)
    scaffold = VGroup(stage_circle, stage_frame, stage_apex)

    # z-order LARGEST region first (bottom) so each later, smaller, opaque fill
    # fully covers the part of the bigger one it sits inside -- outer (z=1)
    # under sector (z=2) under inner (z=3) leaves three distinct colour rings:
    # green (OAC-only) / strategy (sector-only) / amber (OAB), not a translucent blend.
    src_outer = _tri(O, C_off, green, MAIN_FOP, 1)
    src_sector = _sec(O, strategy, MAIN_FOP, 2)
    src_inner = _tri(O, B_off, amber, MAIN_FOP, 3)

    # ①②③ chips anchored IN the main figure's three regions (not just the right
    # glyphs), so a paused viewer can map region -> formula directly on the
    # source construction. Anchors are fractions of R (hand-tuned by numeric
    # point-in-region search, then expressed R-relative so they track a resize):
    # the sector-only sliver between chord AB and the arc is genuinely thin
    # (~0.15u regardless of R), so its chip sits astride the arc itself rather
    # than buried in a sliver too narrow to hold a legible ring; the other two
    # sit well inside their own region, clear of the scaffold's O/A/B/C/
    # dimension labels.
    def _chip(anchor_off, col, n, radius=0.14):
        ring = Circle(radius=radius, color=col, stroke_width=2.0,
                      fill_color=T.color(ground, "bg"), fill_opacity=0.9).set_z_index(7)
        ring.move_to(O + anchor_off)
        num = MathTex(str(n), color=text, font_size=T.fs("label") * 0.68 * (radius / 0.14))
        num.move_to(ring.get_center()).set_z_index(8)
        return VGroup(ring, num)

    chip_inner = _chip(R * np.array([0.605, 0.158, 0.0]), amber, 1)
    # smaller radius: the sector-only sliver between chord AB and the arc is only
    # ~0.12u deep regardless of R, so a full-size chip would bleed equally into
    # both neighbours; a tighter ring keeps it legibly "on the strategy band."
    chip_sector = _chip(R * np.array([np.cos(0.52 * th), np.sin(0.52 * th), 0.0]),
                        strategy, 2, radius=0.10)
    chip_outer = _chip(R * np.array([0.947, 0.716, 0.0]), green, 3)

    # -- right: three peeled shapes on one baseline (true relative size) ---------
    yb = O[1]                                        # share the source baseline
    GLYPH_GAP = 0.45                                 # air between adjacent congruent shapes
    O1 = np.array([-1.30, yb, 0.0])
    O2 = O1 + np.array([R + GLYPH_GAP, 0.0, 0.0])
    O3 = O2 + np.array([R + GLYPH_GAP, 0.0, 0.0])
    badge_y = yb + R * np.tan(th) + 0.34             # one row, above the tallest apex

    def _badge(n, x, col):
        ring = Circle(radius=0.16, color=col, stroke_width=2.0)
        num = MathTex(str(n), color=text, font_size=T.fs("label") * 0.75)
        return VGroup(ring, num).move_to(np.array([x, badge_y, 0.0])).set_z_index(6)

    # Each peeled glyph is NESTED, not a single flat shape: glyph ② is the inner triangle
    # sitting inside the sector, glyph ③ is both sitting inside the outer triangle -- the
    # same opaque stack, at the same MAIN_FOP, as the source figure on the left.
    #
    # Why (2026-09-13 visual audit): the source figure's opaque stacking leaves each region
    # showing only its own RING, so strategy on the left is the crescent -- what the sector
    # ADDS -- while glyph ② was the WHOLE sector, and badges ①②③ asserted the two were the
    # same thing. Rollout T2-2 then painted the inequality's three terms in the same three
    # colours, which makes the mismatch load-bearing: the strategy term is 1/2 theta, the whole
    # sector. Nesting the glyphs makes both readings true at once -- the colour is still the
    # increment, the badge and the outline are the whole area, and "each region sits inside
    # the next" (the narration's own words) becomes something the row SHOWS rather than
    # asserts. `nested` layers fade in with the label, on top of the flown shape.
    def _slot(o, shape, lab_tex, role, n, badge_col, nested=()):
        whole = VGroup(shape, *nested)
        lab = brand.math_line(lab_tex, ground, role=role, size="label")
        lab.next_to(whole, DOWN, buff=0.28)
        badge = _badge(n, o[0] + R / 2, badge_col)   # centred over the slot, equal height
        return VGroup(shape, *nested, lab, badge)

    dst1 = _slot(O1, _tri(O1, B_off, amber, MAIN_FOP, 3),
                 r"\tfrac12\sin\theta", "accent", 1, amber)
    dst2 = _slot(O2, _sec(O2, strategy, MAIN_FOP, 2),
                 r"\tfrac12\theta", "strategy", 2, strategy,
                 nested=[_tri(O2, B_off, amber, MAIN_FOP, 3)])
    dst3 = _slot(O3, _tri(O3, C_off, green, MAIN_FOP, 1),
                 r"\tfrac12\tan\theta", "success", 3, green,
                 nested=[_sec(O3, strategy, MAIN_FOP, 2), _tri(O3, B_off, amber, MAIN_FOP, 3)])

    # the three terms in the three regions' colours (SPEC rule 5 "same quantity, same
    # colour"; rollout T2-2; 2026-09-13 colour-axis unification, second call: sin=accent/amber,
    # theta=strategy/violet (was concept/ochre -- too close in hue to accent/amber),
    # tan=success/green): each `{{...}}` segment is one term and seg_roles paints it whole --
    # over the deck's theta token colour -- so a term reads as ONE tinted unit matching the
    # shape above it, instead of the chain falling back to white.
    ineq = brand.math_line(
        r"{{\tfrac12\sin\theta}} \;\le\; {{\tfrac12\theta}} \;\le\; {{\tfrac12\tan\theta}}",
        ground, role="text", size="math_sm",
        seg_roles={r"\tfrac12\sin\theta": "accent", r"\tfrac12\theta": "strategy",
                   r"\tfrac12\tan\theta": "success"})
    row = VGroup(dst1, dst2, dst3)
    ineq.next_to(row, DOWN, buff=0.55)

    full = VGroup(scaffold, src_inner, src_sector, src_outer,
                  chip_inner, chip_sector, chip_outer, dst1, dst2, dst3, ineq)
    _centre_in_zone(title, full)

    # legibility pads under the three dimension labels that land on the 0.88-opaque fills
    # (theta on strategy, sin theta on amber, tan theta on green: 1.1-1.5:1 contrast, A6). A
    # bg-coloured BackgroundRectangle goes into the label's own stage group right before the
    # label (same z-index 5 -> drawn under it, revealed with it). Built AFTER _centre_in_zone
    # so a pad can never move the figure: `full` is already placed (its centre measured
    # unchanged before/after, 2026-09-13).
    for stage, label in ((stage_frame, lth), (stage_frame, l_sin), (stage_apex, l_tan)):
        pad = BackgroundRectangle(label, color=T.color(ground, "bg"), fill_opacity=0.72,
                                  buff=0.04).set_z_index(5)
        stage.insert(stage.submobjects.index(label), pad)

    # -- the evenness aside (LAST beat; motion primitives 6 + 4) ------------------
    # 19 seconds of narration explaining that sin(theta)/theta is EVEN used to play over a
    # finished, motionless picture -- part of what made this scene's first beat the longest
    # still in the film (37.6 s). Here the angle actually swings from +theta to -theta and
    # back with both half-chords tracking it, so "both flip sign, so the ratio does not" is
    # something the viewer WATCHES. Built after _centre_in_zone and kept OUT of `full`, so
    # it hangs off the final layout without being able to move the main figure.
    #
    # It plays LAST now (R6 and four rewatch lenses: a 19-second digression standing between
    # "here is the new tool" and the figure itself; the handout can put it first because a
    # reader can skip a sentence, a viewer cannot -- 2026-09-13 user call). By then nothing
    # on the frame is empty, so the aside is an OVERLAY: the storyboard's `focus:` entry dims
    # the finished figure for this beat and restores it at the end, and the little circle
    # sits over the middle of that figure rather than in a corner.
    # Centred on the MAIN FIGURE, not the whole layout: the aside is about the same unit
    # circle, and over the figure it hides only the thing it is restating -- the three
    # peeled glyphs and the inequality stay readable underneath it. (Centred on `full` it
    # landed between the figure and glyph (2), covering neither and colliding with both.)
    # r 0.92 -> 1.15: with the figure underneath now fully covered (see the panel below),
    # the aside had a third of the frame to itself and was still drawn at inset size. R2
    # asked for 1.4x on the main circle; this is the same move on the circle that is
    # actually on screen, stopped where the panel would start eating the glyph (1) column.
    er = 1.15
    eO = np.array([scaffold.get_center()[0], scaffold.get_center()[1] + 0.25, 0.0])
    e_circle = Circle(radius=er, color=mut, stroke_width=1.8).move_to(eO)
    e_axis = Line(eO + (er + 0.35) * LEFT, eO + (er + 0.35) * RIGHT,
                  color=mut, stroke_width=1.4)
    e_ang = ValueTracker(th)

    def _e_point():
        a = e_ang.get_value()
        return eO + er * np.array([np.cos(a), np.sin(a), 0.0])

    def _e_radius():
        return Line(eO, _e_point(), color=text, stroke_width=2.2)

    def _e_height():
        pt = _e_point()
        foot = np.array([pt[0], eO[1], 0.0])
        # both half-chords are sin values (+theta and -theta), so they share the sin
        # colour (accent) and split on brightness instead of borrowing an unrelated
        # role (2026-09-13 colour-axis unification).
        col = amber if e_ang.get_value() >= 0 else mut
        return Line(foot, pt, color=col, stroke_width=4.0)

    def _e_dot():
        return Dot(_e_point(), radius=0.05, color=text)

    e_live = VGroup(always_redraw(_e_radius), always_redraw(_e_height),
                    always_redraw(_e_dot))
    # Inline slashes, not two \dfrac stacks. The TeX preamble sets \everymath{\displaystyle},
    # so a stacked fraction renders at DISPLAY size even inside a small line -- measured 4.97u
    # wide, which pushed the overlay panel past the left safe margin once the aside was
    # anchored on the figure. (Same reason the rail tags dropped their \tfrac this round.)
    e_caption = brand.math_line(
        r"\sin(-\theta)/(-\theta) \;=\; \sin\theta/\theta",
        ground, role="text", size="label")
    e_caption.next_to(e_circle, DOWN, buff=0.34)
    # An overlay has to COVER what it sits on. Dimming the finished figure (the storyboard's
    # `focus:` entry for this beat) drops its contrast but leaves its glyph labels behind the
    # aside's own caption -- measured: the caption's box lands on glyph (1)'s "1/2 sin theta".
    # A ground-coloured panel under the whole aside settles it, the same move the rollout
    # used for labels crossed by lines. Built LAST and inserted FIRST so it is behind.
    # fill_opacity 1.0, and sized to the FIGURE, not to the aside. Both halves of that
    # were measured off the render, not guessed: at 0.95 the region fills under the panel
    # kept 4.1% of their signal, which on a 270-unit teal over a 30-unit ground is a
    # perfectly legible second figure (R2 must ML1, "ghosting"); and the parts of the
    # construction that reached past the aside's own bounding box -- the y-axis, the O/1/A
    # labels, the top-left arc -- were never under the panel at all. The right-hand glyphs
    # and the inequality stay OUTSIDE it and stay readable at the storyboard's dim.
    # buff 0.12, not the usual 0.28: the construction's own `tan theta` label already sits
    # 0.24 u from glyph (1)'s left tip, so anything wider would clip the glyph the panel is
    # supposed to leave alone. Padding costs nothing here -- a ground-coloured slab at full
    # opacity is INVISIBLE except where it covers something, so there is no edge to breathe.
    e_panel = BackgroundRectangle(VGroup(scaffold, src_inner, src_sector, src_outer,
                                         chip_inner, chip_sector, chip_outer,
                                         e_circle, e_axis, e_caption),
                                  color=T.color(ground, "bg"), fill_opacity=1.0, buff=0.12)
    # ABOVE the figure, or it is not an overlay: the regions are z 1-3 and the chips z 7-8,
    # so a panel at the default z=0 sits behind everything it is supposed to cover (first
    # render showed the aside's circle drawn straight over glyph (1), caption on top of two
    # other labels). Panel 9, contents 10.
    e_panel.set_z_index(9)
    for _m in (e_circle, e_axis, e_live, e_caption):
        _m.set_z_index(10)
    evenness = VGroup(e_panel, e_circle, e_axis, e_live, e_caption)

    IN_SECONDS, OUT_SECONDS = 0.7, 0.35     # entrance (circle+axis, caption) / exit fade
    # The three peeled glyphs and the inequality are the only content the panel does NOT
    # cover, and for the aside to own the frame they have to fall back (R2: "三個複本與
    # 不等式降亮到 30%"). It is done HERE rather than by the storyboard's `focus:` because
    # scene.py applies a focus after the beat's reveal -- correct for a half-second fade,
    # useless for a reveal that IS the beat: the dim landed after the aside had already
    # faded out (measured: the glyph fills held 100% of their brightness for the whole
    # aside, then flickered for 0.8 s at the end of the scene). Folded into the entrance
    # and exit plays, so it costs the beat nothing. `fade` in and save_state/restore out,
    # never set_opacity either way -- the (1)(2)(3) badges are hollow rings and a flat
    # opacity fills them in (see focus.apply).
    backdrop = VGroup(dst1, dst2, dst3, ineq)

    def _evenness_anim(scene, mob, _ground) -> float:
        """Swing +theta -> -theta -> +theta, twice, filling whatever beat this lands on.

        Everything is budgeted INSIDE `total`, exit fade included: the old version added
        the 0.35 s fade after the beat's budget and returned `total + 0.35`, so the scene ran
        long by that much every time -- harmless while this was a middle beat that later
        beats absorbed, a real `[sync] render/audio length` warning now that it is the LAST
        beat (measured: scene 06 went from -0.27 s under to +0.53 s over)."""
        total = TM.beat_run_time(scene, 6.0)
        t0 = _elapsed(scene)
        backdrop.save_state()
        scene.play(FadeIn(e_panel), FadeIn(e_circle), FadeIn(e_axis),
                   backdrop.animate.fade(1.0 - focus.DIM_OPACITY), run_time=0.4)
        scene.add(e_live)
        scene.play(FadeIn(e_caption), run_time=0.3)
        swing = max((total - IN_SECONDS - OUT_SECONDS) / 2.0, 0.8)
        for _ in range(2):
            scene.play(e_ang.animate.set_value(-th), run_time=swing,
                       rate_func=there_and_back)
        # the aside has done its job; the figure underneath gets the frame back
        scene.play(FadeOut(mob), backdrop.animate.restore(), run_time=OUT_SECONDS)
        return _elapsed(scene) - t0

    def _peel(src, chip):
        def anim(scene, mob, ground):
            # [shape, *nested, label, badge] -- `nested` is the smaller regions this glyph
            # contains (empty for glyph ①); they arrive with the label, so the flown copy
            # is still the one region this beat is about.
            shape, label, badge = mob[0], mob[-2], mob[-1]
            nested = list(mob[1:-2])
            t0 = _elapsed(scene)
            scene.play(FadeIn(src), run_time=0.4)            # region appears on the left
            scene.add(src)
            flyer = src.copy()
            scene.add(flyer)
            # congruent copy slides out to its slot on the right (rigid motion)
            scene.play(ReplacementTransform(flyer, shape), run_time=0.8, rate_func=smooth)
            # right-side glyph brightens (label + badge) the SAME beat the main
            # figure's own ①②③ chip appears, tying the two halves together.
            scene.play(FadeIn(label, shift=0.08 * UP), FadeIn(badge), FadeIn(chip),
                       *[FadeIn(m) for m in nested], run_time=0.32)
            return _spent(scene, t0, 1.52)
        return anim

    out.append(Block("circle", stage_circle, anim=_draw, static=False, layer="graph"))
    out.append(Block("evenness", evenness, anim=_evenness_anim, static=False, layer="graph"))
    out.append(Block("frame", stage_frame, anim=_draw, static=False, layer="graph"))
    out.append(Block("apex", stage_apex, anim=_draw, static=False, layer="graph"))
    out.append(Block("tri_inner", dst1, anim=_peel(src_inner, chip_inner), static=False, layer="graph"))
    out.append(Block("sector", dst2, anim=_peel(src_sector, chip_sector), static=False, layer="graph"))
    out.append(Block("tri_outer", dst3, anim=_peel(src_outer, chip_outer), static=False, layer="graph"))
    # The inequality lands on a beat that grew to ~22 s when the corner-piece sentence
    # was added (Task D), and a single fade left 20.8 s of still picture -- over the 12 s
    # line. Its three terms are already `{{...}}` segments, so primitive 7 can walk them
    # across the beat: each term arrives as the narration names it. (`pacing.apply` only
    # upgrades STOCK reveals, and this one is a callable, so it is wired here by hand.)
    out.append(Block("ineq", ineq, anim=pacing.paced_reveal, static=False, layer="graph"))
    return out


# ================================================================ hook 2
# slope_equals_height (Figure 3.3) -- tangents to y=sin x at 0, pi/2, pi have
# slopes 1, 0, -1, exactly the heights of y=cos x there. The base graph already
# carries plot.0 (sin) and plot.1 (cos); the hook adds the tangents + cos dots.


def slope_equals_height(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    axes = ids["axes"].mobject

    blue = T.color(ground, "secondary")
    green = T.color(ground, "success")
    mut = T.color(ground, "muted")

    # (x0, cos x0, full-identity label) -- the label reads the identity, not a
    # bare number, so it does not collide in meaning with the sin curve's own
    # "0" tick at the origin (two unrelated "0"s next to each other read as a
    # mistake to a paused viewer).
    marks = [(0.0, 1.0, r"\cos 0 = 1"), (np.pi / 2, 0.0, r"\cos\tfrac{\pi}{2} = 0"),
             (np.pi, -1.0, r"\cos\pi = -1")]

    # x-axis teaching ticks at the three named angles the narration reads, so a
    # paused viewer can tell which x each slope/height belongs to (house style: a
    # few labelled ticks, not a full number line). No tick glyph at x=0 -- it would
    # sit on the y-axis; the "0" label alone anchors the origin.
    xticks = VGroup()
    # pi's buff 0.20->0.30（2026-09-13 合併版視覺幀稽核）：m=-1 的綠切線在 x=pi 附近下探，0.20 時
    # 劃過標籤；其餘兩刻度不在任何切線的路徑上，維持原 buff。
    for xv, xlab, draw_tick, buff in [(0.0, "0", False, 0.20), (np.pi / 2, r"\tfrac{\pi}{2}", True, 0.20),
                                       (np.pi, r"\pi", True, 0.30)]:
        p = axes.c2p(xv, 0.0)
        if draw_tick:
            xticks.add(Line(p + 0.09 * UP, p + 0.09 * DOWN, color=mut, stroke_width=2.0))
        t = MathTex(xlab, color=mut, font_size=T.fs("label")).next_to(p, DOWN, buff=buff)
        if xv == 0.0:
            # the origin's label sits under the y-AXIS, which then runs straight through
            # the glyph. Slide it clear -- to the RIGHT, not to the usual left: the m=1
            # tangent leaves the origin down-to-the-left and crosses that spot instead.
            t.shift(0.26 * RIGHT)
        xticks.add(t)

    # Screen length, not data-space half-width, is held fixed across the three
    # tangents: at this axes' aspect ratio a slope-0 segment of the old fixed
    # data-width d=0.62 rendered visibly SHORTER on screen than the +-1 diagonal
    # ones. Solve d per-slope so the drawn segment is the same length in scene
    # units for all three, matching the "three equal tangents" reading the
    # figure wants.
    TARGET_LEN = 3.0
    x_scale = axes.x_axis.get_unit_size()
    y_scale = axes.y_axis.get_unit_size()

    # The slope label goes PERPENDICULAR to its own tangent, on the side the sine curve is
    # not (sine is concave here, so that is always the upper side). Straight up/down put
    # m=1 on top of the y-axis and stacked m=-1 under the pi tick; perpendicular also
    # spaces the three labels the way the three tangents are angled, so each one reads as
    # belonging to its segment (2026-09-13 visual audit).
    LABEL_OFF = 0.95

    def tangent(x0, slope):
        dir_len = np.hypot(x_scale, slope * y_scale)
        d = TARGET_LEN / (2.0 * dir_len)
        p1 = axes.c2p(x0 - d, np.sin(x0) - d * slope)
        p2 = axes.c2p(x0 + d, np.sin(x0) + d * slope)
        seg = Line(p1, p2, color=green, stroke_width=5.0)
        lab = brand.math_line("m=%s" % ("1" if slope == 1 else "0" if slope == 0 else "-1"),
                              ground, role="success", size="label")
        anchor = axes.c2p(x0, np.sin(x0))
        normal = np.array([-slope * y_scale, x_scale, 0.0]) / dir_len   # y-component > 0
        lab.move_to(anchor + LABEL_OFF * normal)
        return VGroup(seg, lab)

    tan_0 = tangent(0.0, 1.0)
    tan_halfpi = tangent(np.pi / 2, 0.0)
    tan_pi = tangent(np.pi, -1.0)

    # Dashed connector ties each tangent point on sin (x0, sin x0) straight down
    # (same x0) to its read-off dot on cos (x0, cos x0) -- "slope here = height
    # there" made literal. Drawn together with cos_dots so it appears at the
    # exact beat the narration reads the matching heights, not before.
    DOT_R = 0.07
    cos_dots = VGroup()
    for x0, h, lab in marks:
        sin_pt = axes.c2p(x0, np.sin(x0))
        cos_pt = axes.c2p(x0, h)
        # trim both ends past the dot radius (and off the curve point) so the
        # dash pattern doesn't terminate a partial dash inside the dot itself.
        gap = DOT_R + 0.03
        v = cos_pt - sin_pt
        v_hat = v / np.linalg.norm(v)
        connector = DashedLine(sin_pt + gap * v_hat, cos_pt - gap * v_hat,
                               color=mut, stroke_width=1.6, dash_length=0.07)
        # The read-off dot and its label take the COSINE curve's own colour: they report
        # cosine's heights, and wearing sine's amber made one hue mean two functions
        # (2026-09-13 visual audit; SPEC-motion-language 規則 5). Blue is already cosine
        # in shm_stacked_graphs, so the section now says cosine the same way three times.
        dot = Dot(cos_pt, radius=DOT_R, color=blue)
        ml = brand.math_line(lab, ground, role="secondary", size="label")
        if h == 0.0 or x0 == 0.0:
            # this dot sits ON an axis (x=0 -> the y-axis; cos x0 = 0 -> the x-axis, where
            # the cosine curve also crosses); a label stacked straight above it would have
            # a line run through the text, so offset diagonally into the clear quadrant.
            ml.next_to(dot, UP + RIGHT, buff=0.12)
        else:
            ml.next_to(dot, UP if h > 0 else DOWN, buff=0.14)
        cos_dots.add(VGroup(connector, dot, ml))

    out = list(blocks)
    out.append(Block("xticks", xticks, static=True, layer="graph"))
    out.append(Block("tan_0", tan_0, anim=_draw, static=False, layer="graph"))
    out.append(Block("tan_halfpi", tan_halfpi, anim=_draw, static=False, layer="graph"))
    out.append(Block("tan_pi", tan_pi, anim=_draw, static=False, layer="graph"))
    out.append(Block("cos_dots", cos_dots, anim=_fade, static=False, layer="graph"))
    return out


# ================================================================ hook 3
# shm_stacked_graphs (Figure 3.4) -- height s=sin t, velocity s'=cos t,
# acceleration s''=-sin t stacked over one shared time axis; dashed verticals
# at the peaks/troughs (where velocity passes zero); s''=-s = top flipped.


def shm_stacked_graphs(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    title = ids["title"].mobject
    out = [b for b in blocks if b.id != "axes"]

    amber = T.color(ground, "accent")
    blue = T.color(ground, "secondary")
    green = T.color(ground, "success")
    mut = T.color(ground, "muted")

    rows = [(np.sin, amber, r"s=\sin t", r"\text{Height}"),
            (np.cos, blue, r"s'=\cos t", r"\text{Velocity}"),
            (lambda t: -np.sin(t), green, r"s''=-\sin t", r"\text{Acceleration}")]

    groups = []
    axes_list = []
    for i, (func, color, label_tex, word_tex) in enumerate(rows):
        ax = Axes(x_range=[0, 2 * PI, PI / 2], y_range=[-1.2, 1.2, 1],
                  x_length=6.0, y_length=1.0, tips=False,
                  axis_config={"color": mut, "stroke_width": 1.4, "include_ticks": False})
        curve = ax.plot(func, x_range=[0, 2 * PI], color=color, stroke_width=3.5)
        # move axes AND curve together (the curve is not a child of the axes, so
        # moving the axes alone leaves the curve behind on the origin band).
        plot_grp = VGroup(ax, curve).move_to([0.6, (1 - i) * 1.55, 0.0])
        # left label = physical name (Height/Velocity/Acceleration) over the formula,
        # so the row reads as physics, not just symbols.
        word = brand.math_line(word_tex, ground, role="text", size="label")
        formula = brand.math_line(label_tex, ground, role="text", size="label")
        lab = VGroup(word, formula).arrange(DOWN, buff=0.10, aligned_edge=RIGHT)
        lab.next_to(ax, LEFT, buff=0.3)
        groups.append(VGroup(lab, plot_grp))
        axes_list.append(ax)
    ax_top, _, ax_bot = axes_list

    stack = VGroup(*groups)
    _centre_in_zone(title, stack)

    def vline(t):
        top = ax_top.c2p(t, 1.2)
        bot = ax_bot.c2p(t, -1.2)
        return DashedLine(np.array([top[0], top[1], 0.0]), np.array([bot[0], bot[1], 0.0]),
                          color=mut, stroke_width=1.8, dash_length=0.09)

    guide_ts = [PI / 2, 3 * PI / 2]
    mirror = VGroup(*(vline(t) for t in guide_ts))

    # guide labels, once each, tucked under the bottom axis where they sit clear
    # of all three curves (no per-panel repetition needed -- one shared time axis).
    guide_labels = VGroup()
    for t, tex in zip(guide_ts, [r"t=\tfrac{\pi}{2}", r"t=\tfrac{3\pi}{2}"]):
        glab = brand.math_line(tex, ground, role="text", size="label")
        glab.next_to(ax_bot.c2p(t, -1.2), DOWN, buff=0.22)
        guide_labels.add(glab)

    # dots where each curve crosses a guide -- the read-off the narration asks for
    # (height peaks/troughs <-> velocity crosses zero <-> acceleration mirrors height).
    # These can only sit on a guide that already spans all three panels, so, like the
    # guide lines themselves, they ride the `mirror` beat rather than their own panel.
    guide_dots = VGroup()
    for (func, color, _, _), ax in zip(rows, axes_list):
        for t in guide_ts:
            guide_dots.add(Dot(ax.c2p(t, func(t)), radius=0.07, color=color))

    mlab = brand.math_line(r"s''=-s", ground, role="success", size="label")
    mlab.next_to(groups[2][1], RIGHT, buff=0.35)  # anchored to the accel panel's right side
    g_mirror = VGroup(mirror, guide_labels, guide_dots, mlab)

    out.append(Block("g_s", groups[0], anim=_draw, static=False, layer="graph"))
    out.append(Block("g_v", groups[1], anim=_draw, static=False, layer="graph"))
    out.append(Block("g_a", groups[2], anim=_draw, static=False, layer="graph"))
    out.append(Block("mirror", g_mirror, anim=_fade, static=False, layer="graph"))
    return out


# ================================================================ hook 4
# toward_the_chain_rule -- the section closer's trio ($\sin x$ vs $\sin(x^2)$
# vs $\sin(3x+1)$) was one flat math line ("checkmark ... ? ... ?"), which
# buries the point the narration is making: one of the three is already solved,
# the other two are not (yet). Three chip cards say that at a glance -- a
# green-accent-bar card for the solved bare form, two amber-accent-bar cards
# (matching the "?" ink) for the composed ones still waiting on the chain rule.
# Single reveal id `math.0` is kept (the storyboard's {show math.0} cue and
# narration are untouched); only the block's mobject is swapped.


def toward_the_chain_rule(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    old_math = ids["math.0"].mobject   # old line's LEFT edge == SPINE_X (statement's own left-flush axis)

    chips_spec = [
        (r"\sin x", "check", "success"),
        (r"\sin(x^{2})", "query", "accent"),
        (r"\sin(3x+1)", "query", "accent"),
    ]

    def _chip(tex, glyph_name, role):
        formula = brand.math_line(tex, ground, role="primary", size="math_sm")
        # glyph() has no ready-made "?"; a direct MathTex keeps the actual question
        # mark the storyboard math reads, styled the same accent colour glyph() uses.
        mark = (brand.glyph("check", ground, role=role, size="math_sm") if glyph_name == "check"
               else MathTex("?", color=T.color(ground, role), font_size=T.fs("math_sm")))
        row = VGroup(formula, mark).arrange(RIGHT, buff=0.30)
        return brand.accent_panel(row, ground, bar_role=role, pad=0.32, pad_x=0.42)

    chips = [_chip(tex, gname, role) for tex, gname, role in chips_spec]
    trio = VGroup(*chips).arrange(RIGHT, buff=0.55)
    # Left-flush to the old line's left edge (== SPINE_X), matching the statement
    # above it -- old_math.get_center() would be wrong here: it is the centre of a
    # short single line, not of this much wider row, and would push the row's left
    # edge off-frame.
    trio.move_to(old_math.get_left(), aligned_edge=LEFT)

    ids["math.0"].mobject = trio
    return blocks


# ================================================================ hook 5
# derivative_cycle (Remark 3.1) -- the old math.0 was a LINEAR chain,
# $\sin x \to \cos x \to -\sin x \to -\cos x \to \sin x$, which visually
# restates "and back to sin x" as a fifth node identical to the first (the
# repetition IS the point -- "after 4 steps you are home" -- but a straight
# line cannot show a closed loop, only imply one by repeating a label). A
# 4-node ring closes the loop for real: one node per function, four short
# clockwise arrows, the fourth looping back into the first -- so "four
# derivatives and you are home" is a shape, not a repeated symbol. Reveal id
# is unchanged (`math.0`), so the LOCKED narration + {show math.0} cue needs
# no edit; only the block's mobject is swapped (same contract as hook 4).


def derivative_cycle(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    old_math = ids["math.0"].mobject
    statement = ids["statement"].mobject
    math_1 = ids["math.1"].mobject

    mut = T.color(ground, "muted")

    # The old single LINE sat in a wide/short gap (statement above, math.1
    # below), so the ring must be landscape (wide, short) rather than the
    # tall diamond a "square" reading would suggest -- a diamond this tall
    # collides with both neighbours. Four corners of a wide rectangle:
    # sin (top-left) -> cos (top-right) -> -sin (bottom-right) -> -cos
    # (bottom-left) -> back to sin (top-left), i.e. clockwise.
    #
    # Node panels use the smaller "label" size + tight padding (not math_sm):
    # the gap this ring lives in is short enough that a math_sm-sized node is
    # itself nearly as tall as the whole gap, leaving no room for the
    # vertical connector arrows to have any visible length -- they collapsed
    # to zero in an earlier pass. label-size keeps all four formulas legible
    # while leaving an actual gap between the top and bottom row to draw
    # into.
    # 2026-09-13: the gap is no longer short (math.1 drops into the dead band below, see
    # MATH1_DROP), so the nodes get the readable math_sm size and the two rows get a real
    # arrow run between them instead of the stubs the old cramped band forced.
    NODE_SIZE, NODE_PAD, NODE_PAD_X = "math_sm", 0.16, 0.26

    def _node(tex, role):
        label = brand.math_line(tex, ground, role="primary", size=NODE_SIZE)
        return brand.accent_panel(label, ground, bar_role=role, pad=NODE_PAD, pad_x=NODE_PAD_X)

    # The bar says WHICH FUNCTION, never the sign: amber = sine, blue = cosine, the same
    # two colours the graphs use (slope_equals_height, shm_stacked_graphs). The old table
    # made `sin x` green while amber meant sine everywhere else in the film, and it changed
    # colour for `-sin x` but not for `-cos x` -- a rule that is not a rule (2026-09-13
    # visual audit). Alternating amber/blue around the ring is also the remark's own
    # sentence: differentiation sends the two INTO EACH OTHER, and the minus signs carry
    # the sign flip on their own.
    node_specs = [
        (r"\sin x", "TL", "accent"),    # seed of the cycle
        (r"\cos x", "TR", "secondary"),
        (r"-\sin x", "BR", "accent"),
        (r"-\cos x", "BL", "secondary"),
    ]
    nodes = [_node(tex, role) for tex, _, role in node_specs]
    node_h = max(n.height for n in nodes)

    HALF_W = 4.30                         # the ring is the scene's subject: span the frame
    ARROW_GAP = 0.78                       # vertical-arrow run, and the d/dx label's home
    HALF_H = (node_h + ARROW_GAP) / 2
    corners = {
        "TL": np.array([-HALF_W, HALF_H, 0.0]),
        "TR": np.array([HALF_W, HALF_H, 0.0]),
        "BR": np.array([HALF_W, -HALF_H, 0.0]),
        "BL": np.array([-HALF_W, -HALF_H, 0.0]),
    }
    for node, (_, corner, _) in zip(nodes, node_specs):
        node.move_to(corners[corner])

    # Straight arrows tracing the RECTANGLE'S PERIMETER (top edge L->R, right
    # edge T->B, bottom edge R->L, left edge B->T) -- each pulled back off
    # both nodes' facing edges so it never touches a panel. This reads as one
    # unambiguous clockwise loop (unlike corner-to-corner diagonals, which
    # cut through the centre and cross each other visually). The 4th arrow
    # (left edge, bottom-left -> top-left) is the SAME straight-arrow style
    # as the other three -- it closes the cycle instead of singling it out.
    #
    # get_edge_center(direction) reads each node's OWN bounding-box edge in
    # the direction of travel -- unlike hand-computing "centre +/- half_size"
    # (an earlier pass), it cannot overshoot past the midpoint and swap the
    # two endpoints when the nodes sit close together (as the top/bottom rows
    # here do), which is exactly the bug that flipped the vertical arrows'
    # direction.
    def _edge_arrow(a, b):
        pa, pb = a.get_center(), b.get_center()
        v_hat = (pb - pa) / np.linalg.norm(pb - pa)
        gap = 0.10
        start = a.get_edge_center(v_hat) + gap * v_hat
        end = b.get_edge_center(-v_hat) - gap * v_hat
        return Line(start, end, color=mut, stroke_width=3.0).add_tip(tip_length=0.18, tip_width=0.16)

    pairs = [(0, 1), (1, 2), (2, 3), (3, 0)]
    arrows = VGroup(*(_edge_arrow(nodes[i], nodes[j]) for i, j in pairs))

    # one d/dx label on the top edge (sin -> cos) suffices to name what every
    # arrow means without crowding all four edges with the same tag.
    #
    # It is `\frac` in TEXT ink, not `\tfrac` in muted: this
    # label is the ONLY thing on the frame that says what an arrow means ("Writing an
    # arrow for one derivative"), and it was being shrunk three times over -- \tfrac
    # inside an already label-sized MathTex, then again by the ring's fit clamp --
    # landing at ~10 px per row, under half the 26 px font floor, in the dimmest ink on
    # the frame. The visual-frame audit (2026-09-13) read it as a blocking V4: the ring
    # degenerates into four boxes and some arrows.
    # It sits in the MIDDLE of the loop, not above the top edge: centred it names every
    # arrow at once (which is what the narration says -- "writing an arrow for one
    # derivative"), and it costs the ring no extra height, so all of the band goes to the
    # diagram instead of to a label stacked on top of it.
    # math_sm, the node size: it was the smallest ink inside the ring at `label`, and the
    # first thing to fail at phone width (regression audit, A6 med).
    ddx = brand.math_line(r"\frac{d}{dx}", ground, role="text", size="math_sm")
    ddx.move_to(VGroup(*nodes).get_center())

    # ddx is deliberately OUTSIDE the group the fit clamp below measures and scales. It
    # adds no height (it lives in the loop's empty middle), and it is the one element whose
    # size is load-bearing -- letting the clamp shrink it is exactly how it ended up under
    # the font floor in the first place. The same audit flagged the durability: the ring
    # cleared the clamp by only 0.02u, so a three-line statement would have shrunk it again.
    ring = VGroup(arrows, *nodes)

    # The ring is this scene's subject, and it was living in the thinnest band on the
    # frame while ~1.3u sat empty BELOW math.1 (same audit, A7: "主角最小最暗、配角最大").
    # Drop math.1 into that dead space to widen the ring's gap; it still clears the
    # bottom safe margin with room to spare.
    MATH1_DROP = 0.95
    math_1.shift(MATH1_DROP * DOWN)

    # Hard clamp to whatever room actually exists between statement's bottom
    # and math.1's top (measured on the REAL, already-built neighbours, not
    # guessed): the node panels' font metrics make the ring's natural height
    # a moving target, so shrink-to-fit is the robust guard against
    # overlapping either neighbour, with a fixed margin breathing on both
    # sides of the gap.
    gap_top, gap_bottom = statement.get_bottom()[1], math_1.get_top()[1]
    MARGIN = 0.16
    available_h = (gap_top - gap_bottom) - 2 * MARGIN
    if ring.height > available_h:
        ring.scale_to_fit_height(available_h)

    # Left-flush to the old line's left edge (== SPINE_X), matching the
    # statement/math.1 above and below it; vertically centred in the gap.
    ring.move_to(old_math.get_left(), aligned_edge=LEFT)
    ring.set_y((gap_top + gap_bottom) / 2)
    ddx.move_to(ring.get_center())          # re-centre after the ring has been placed

    ids["math.0"].mobject = VGroup(ring, ddx)
    return blocks


# ================================================================ hook 6
# chord_vs_arc (scene 08) -- the picture the narration talks about but never showed.
# Beat 0 is 26.7 s of spoken geometry ("on the unit circle the half-chord sin theta is
# always shorter than the arc theta above it") over an EMPTY body zone: the statement
# card, the proof chain and the QED are all {show}-timed and land later, so nothing at
# all is on screen while that sentence is read. The hook puts the unit circle back and
# walks it in the order the narration walks it:
#   circle     : the circle, the axes, the radius at angle theta, the angle mark
#   nudge      : the two legs appear and theta actually wobbles (+-0.15 rad) -- this is
#                "nudge the angle a little ... they never jump", paced to fill its beat
#   chord_arc  : the half-chord thickens as it is named, then the arc traces over it
#   straighten : congruent copies of both peel off, lie down on one baseline, and the
#                length ordering becomes |sin theta| <= |theta|
# The figure is built in the empty RIGHT-HAND region theorem_proof leaves (under the
# statement band, right of the proof chain) and is zoomed out to the middle of the body
# zone for the opening act, docking back home on {show statement} -- R2's "perform it
# big, then keep it in the corner as evidence". Zoom/dock is a pure similarity transform,
# so nothing is re-typeset and the FINAL frame is exactly the built layout.


def chord_vs_arc(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    out = list(blocks)

    text = T.color(ground, "text")
    mut = T.color(ground, "muted")
    blue = T.color(ground, "secondary")
    amber = T.color(ground, "accent")
    strategy = T.color(ground, "strategy")

    R = 2.00
    TH = 1.25            # resting angle (~72 deg): chord/arc differ by 24%, which reads
                         # as "shorter" once the two lie side by side
    NUDGE = 0.20         # the "little" nudge; the swing stays inside [1.05, 1.45] so the
                         # foot never reaches the static sin label
    ZOOM = 1.60          # opening size; capped by the bars' (still invisible) slot having
                         # to stay on frame while the circle holds OPEN_X
    OPEN_X = -1.20       # where the circle sits while it is alone on screen

    def _u(a):
        return np.array([np.cos(a), np.sin(a), 0.0])

    # -- stage 1: the circle, the radius, the angle ------------------------------------
    # First quadrant only -- the same idiom scene 06 uses two scenes earlier (motion
    # primitive 5: the viewer recognises the picture), and the lower half would be dead
    # space that costs the radius 40% of its size in this height budget.
    circ = Arc(radius=R, start_angle=0.0, angle=PI / 2, color=mut, stroke_width=2.0)
    xax = Line(0.30 * LEFT, (R + 0.55) * RIGHT, color=mut, stroke_width=1.4)
    yax = Line(0.30 * DOWN, (R + 0.45) * UP, color=mut, stroke_width=1.4)
    dotA = Dot(R * RIGHT, radius=0.05, color=text)
    labA = brand.math_line("1", ground, role="muted", size="label").next_to(dotA, DR, buff=0.12)
    radius = Line(np.zeros(3), R * _u(TH), color=text, stroke_width=2.4)
    dotP = Dot(R * _u(TH), radius=0.055, color=text)
    ang = Arc(radius=0.36, start_angle=0.0, angle=TH, color=text, stroke_width=2.0)
    lab_th = brand.math_line(r"\theta", ground, role="text", size="label")
    lab_th.move_to(0.58 * _u(TH / 2))
    stage_circle = VGroup(xax, yax, circ, dotA, labA, radius, dotP, ang, lab_th)

    # -- stage 2: the two legs, live under the theta tracker ---------------------------
    th = ValueTracker(TH)
    foot = np.array([R * np.cos(TH), 0.0, 0.0])
    # 2026-09-13 colour-axis unification (11/18/24): sin=accent/amber, cos=secondary/blue,
    # theta objects=strategy/violet -- was sin=secondary/blue, cos=success/green, theta=accent;
    # theta then briefly concept/ochre, moved to strategy/violet same day (second call) because
    # ochre sat too close in hue to accent/amber.
    sin_leg = Line(foot, R * _u(TH), color=amber, stroke_width=6.0)
    cos_leg = Line(np.zeros(3), foot, color=blue, stroke_width=6.0)
    # both labels sit where NO swing position can reach them (right of the widest foot /
    # below the axis), so they never need an updater and never cross the arc.
    lab_sin = brand.math_line(r"\sin\theta", ground, role="accent", size="label")
    lab_sin.move_to(np.array([R * np.cos(TH - NUDGE) + 0.42, 0.80, 0.0]))
    lab_cos = brand.math_line(r"\cos\theta", ground, role="secondary", size="label")
    lab_cos.move_to(np.array([0.50, -0.40, 0.0]))
    stage_nudge = VGroup(cos_leg, sin_leg, lab_sin, lab_cos)

    # -- stage 3: the arc above the chord ----------------------------------------------
    arc = Arc(radius=R, start_angle=0.0, angle=TH, color=strategy, stroke_width=6.0)
    lab_arc = brand.math_line(r"\theta", ground, role="strategy", size="label")
    lab_arc.move_to((R + 0.40) * _u(TH / 2))
    stage_arc = VGroup(arc, lab_arc)

    # -- stage 4: both laid down on one baseline, at their true lengths -----------------
    BAR_X = 2.95
    base = DashedLine(np.array([BAR_X, 1.70, 0.0]), np.array([BAR_X, 0.30, 0.0]),
                      color=mut, stroke_width=1.4, dash_length=0.06)
    bar_chord = Line(np.array([BAR_X, 1.34, 0.0]),
                     np.array([BAR_X + R * np.sin(TH), 1.34, 0.0]),
                     color=amber, stroke_width=7.0)
    bar_arc = Line(np.array([BAR_X, 0.68, 0.0]),
                   np.array([BAR_X + R * TH, 0.68, 0.0]), color=strategy, stroke_width=7.0)
    lab_bc = brand.math_line(r"|\sin\theta|", ground, role="accent", size="label")
    lab_bc.next_to(bar_chord, RIGHT, buff=0.16)
    lab_ba = brand.math_line(r"|\theta|", ground, role="strategy", size="label")
    lab_ba.next_to(bar_arc, RIGHT, buff=0.16)
    ineq = brand.math_line(r"|\sin\theta| \le |\theta|", ground, role="text", size="math_sm")
    ineq.next_to(bar_arc, DOWN, buff=0.55).align_to(base, LEFT)
    stage_bars = VGroup(base, bar_chord, bar_arc, lab_bc, lab_ba, ineq)

    # -- placement: home slot, and the zoomed-out opening position ----------------------
    parts = (stage_circle, stage_nudge, stage_arc, stage_bars)
    full = VGroup(*parts)
    card = ids["statement"].mobject
    proof_right = max(ids[k].mobject.get_right()[0]
                      for k in ids if k.startswith("proof.") or k == "qed")
    box_l, box_r = proof_right + 0.55, T.FRAME_W / 2 - T.SIDE_GUTTER
    box_b, box_t = -T.FRAME_H / 2 + T.SAFE_MARGIN, card.get_bottom()[1] - 0.35
    full.move_to([(box_l + box_r) / 2, (box_b + box_t) / 2, 0])
    home_c = full.get_center().copy()
    body_ref = ids["scaffold.motive"].mobject if "scaffold.motive" in ids else ids["title"].mobject
    big_c = np.array([0.0, (body_ref.get_bottom()[1] - T.TITLE_GAP + box_b) / 2, 0.0])

    # Opening staging. For the ~26 s before the statement card exists the figure owns the
    # frame: zoomed up, and centred on the CIRCLE (the bars' half of it is still empty, so
    # centring the whole group would park the drawing in the left third). `straighten`
    # slides that offset back out as the bars arrive, and the statement's own reveal docks
    # the figure home. All of it is cued by {show statement}; without that marker the card
    # is part of the opening frame, there is no beat to dock on, and the figure simply
    # stays home at full size.
    docks = not ids["statement"].static
    stage_shift = np.zeros(3)
    if docks:
        for p in parts:
            p.scale(ZOOM, about_point=home_c).shift(big_c - home_c)
        stage_shift = np.array([OPEN_X, big_c[1], 0.0]) - stage_circle.get_center()
        for p in parts:
            p.shift(stage_shift)

    # The live geometry reads its frame off mobjects that do NOT move with theta: the two
    # axes give the origin and dotA gives the current radius. (Not circ.get_center()/width
    # -- circ is a quarter Arc, whose bounding box is neither centred on O nor 2R wide.)
    def _O():
        return np.array([yax.get_center()[0], xax.get_center()[1], 0.0])

    def _r():
        return dotA.get_center()[0] - _O()[0]  # R at the current zoom, so updaters track it

    def _s():
        return _r() / R

    def _P():
        return _O() + _r() * _u(th.get_value())

    def _F():
        p = _P()
        return np.array([p[0], _O()[1], 0.0])

    def _circle_anim(scene, mob, _ground) -> float:
        total = TM.beat_run_time(scene, 2.6)
        a, b = total * 0.45, total * 0.32
        c = max(total - a - b, 0.3)
        t0 = _elapsed(scene)
        scene.play(FadeIn(VGroup(xax, yax)), Create(circ), run_time=a)
        scene.play(Create(radius), FadeIn(dotP), FadeIn(dotA), FadeIn(labA), run_time=b)
        scene.play(Create(ang), FadeIn(lab_th), run_time=c)
        scene.add(mob)
        return _spent(scene, t0, total)

    def _nudge_anim(scene, mob, _ground) -> float:
        """Swing theta about its resting value for the whole beat -- the narration's
        'nudge the angle a little ... they never jump' actually happens on screen."""
        total = TM.beat_run_time(scene, 6.0)
        t0 = _elapsed(scene)
        scene.play(FadeIn(mob), run_time=0.5)
        radius.add_updater(lambda m: m.put_start_and_end_on(_O(), _P()))
        dotP.add_updater(lambda m: m.move_to(_P()))
        sin_leg.add_updater(lambda m: m.put_start_and_end_on(_F(), _P()))
        cos_leg.add_updater(lambda m: m.put_start_and_end_on(_O(), _F()))
        ang.add_updater(lambda m: m.become(
            Arc(radius=0.34 * _s(), start_angle=0.0, angle=th.get_value(),
                arc_center=_O(), color=text, stroke_width=2.0)))
        lab_th.add_updater(lambda m: m.move_to(_O() + 0.58 * _s() * _u(th.get_value() / 2)))
        swing = max((total - 0.5) / 3.0, 0.8)
        for delta in (-NUDGE, NUDGE, -NUDGE):
            scene.play(th.animate.set_value(TH + delta), run_time=swing,
                       rate_func=there_and_back)
        for m in (radius, dotP, sin_leg, cos_leg, ang, lab_th):
            m.clear_updaters()                 # the geometry beats need a still figure
        return _spent(scene, t0, 0.5 + 3 * swing)

    def _arc_anim(scene, mob, _ground) -> float:
        total = TM.beat_run_time(scene, 3.6)
        a, b = total * 0.26, total * 0.46
        c = max(total - a - b, 0.3)
        t0 = _elapsed(scene)
        scene.play(sin_leg.animate.set_stroke(width=8.0), run_time=a)   # "the half-chord"
        scene.play(Create(arc), run_time=b)                             # "...than the arc"
        scene.play(FadeIn(lab_arc), run_time=c)
        scene.add(mob)
        return _spent(scene, t0, total)

    def _straighten_anim(scene, mob, _ground) -> float:
        """Congruent copies of the chord and the arc lie down on one baseline: same
        lengths, now directly comparable, and the inequality reads straight off them."""
        total = TM.beat_run_time(scene, 4.2)
        slide = total * 0.16 if docks else 0.0
        a, b = total * 0.40, total * 0.16
        c = max(total - slide - a - b, 0.4)
        t0 = _elapsed(scene)
        if docks:
            mob.shift(-stage_shift)      # still invisible: the slot travels with the rest
            scene.play(*[p.animate.shift(-stage_shift)
                         for p in (stage_circle, stage_nudge, stage_arc)], run_time=slide)
        scene.play(FadeIn(base),
                   ReplacementTransform(sin_leg.copy(), bar_chord),
                   ReplacementTransform(arc.copy(), bar_arc), run_time=a, rate_func=smooth)
        scene.play(FadeIn(lab_bc), FadeIn(lab_ba), run_time=b)
        scene.play(FadeIn(ineq, shift=0.1 * UP), run_time=c)
        scene.add(mob)
        return _spent(scene, t0, total)

    def _dock(scene, mob, _ground) -> float:
        """The statement card's own reveal, doubling as the figure's cue to shrink back
        into its home slot and stay there as evidence under the proof."""
        t0 = _elapsed(scene)
        scene.play(FadeIn(mob, shift=0.35 * RIGHT),
                   *[p.animate.scale(1.0 / ZOOM, about_point=big_c).shift(home_c - big_c)
                     for p in parts], run_time=0.9)
        scene.add(mob)
        return _spent(scene, t0, 0.9)

    if docks:
        stmt = ids["statement"]
        out[out.index(stmt)] = Block("statement", stmt.mobject, anim=_dock,
                                     anim_seconds=0.9, static=False, layer=stmt.layer)
    out.append(Block("circle", stage_circle, anim=_circle_anim, static=False, layer="graph"))
    out.append(Block("nudge", stage_nudge, anim=_nudge_anim, static=False, layer="graph"))
    out.append(Block("chord_arc", stage_arc, anim=_arc_anim, static=False, layer="graph"))
    out.append(Block("straighten", stage_bars, anim=_straighten_anim, static=False, layer="graph"))
    return out


# ================================================================ hook 7
# difference_quotient_for_sine (scene 04) -- the film's longest still (21.0 s) and the one
# the six-lens review flags hardest: three `must`s on the same two beats.
#   beat 3 (39.7 s, step.0) is where Task D's narration rewrite (2026-09-13) put the identity's
#     OWN derivation -- "put u=(A+B)/2 and v=(A-B)/2 ... expand sin(u+v)-sin(u-v) with the
#     angle-sum formulas, and the sin u cos v terms cancel, leaving exactly 2 cos u sin v" --
#     spoken over a screen that shows the one finished row and then holds: 25.8 s of measured
#     stillness (rewatch_pack_after17, fine threshold) against a 12 s acceptance line. The
#     derivation now happens where the narration puts it, as a TEMPORARY draft in the band
#     step.1 / step.2 / result will occupy, which is empty for the whole of this beat.
#   beat 4 (20.9 s, step.2) is "the decisive step" -- write h as 2*(h/2) so the denominator
#     carries the very h/2 that is inside the sine. The stock row posts the FINISHED line
#     and holds: "畫面把它當成又一行結果貼出來，再停 20 秒，觀眾沒有機會看到中間發生了什麼"
#     (R2 D-carry must; R1b L-why must: "為什麼要把 h 換成 2*(h/2)？"). So the row now arrives
#     as the intermediate the narration actually describes and the 2s cancel on screen.
#   beat 5 (20.2 s, result) names two factors in turn ("The first slides to cos x ... the
#     second is exactly sin theta / theta") over one finished line (R2 D-focus). The row is
#     rebuilt as three addressable parts so each factor lands on the words that name it.
# All three are paced across their beat (motion primitive 6). `anim: transform` in the
# storyboard is overridden here: a 1.2 s glyph morph is the right length for a 5 s beat and
# invisible in a 20 s one, which is the finding this hook exists to close.

# The draft is scratch work beside the chain, not a fourth row of it: `text` ink at math_sm,
# one indent in from the chain's left edge, and no semantic hue (the deck's axis -- blue cos,
# amber sin, ochre theta -- stays reserved for the rows themselves). It is built inside the
# hook, never becomes a Block, and is faded out before {show step.1} needs the space, so every
# layout gate still measures exactly the terminal frame it measured before.
_DRAFT_X = -5.85                      # the chain's left edge (-6.37) plus one indent
_DRAFT_Y = (-0.55, -1.30, -2.25)      # the empty band between step.0 and the bottom margin
# The substitution line is split at the narration's own comma ("put u equals ... AND v equals
# ..." is 9 s of speech), so the two halves arrive on the two clauses instead of together.
_DRAFT_SUBS = (r"{{u=\frac{A+B}{2},}} {{\quad v=\frac{A-B}{2}}}",
               r"A=u+v,\quad B=u-v")
_DRAFT_START = r"\sin(u+v)-\sin(u-v)"
# `{{...}}` segments so the two `\sin u\cos v` are addressable as one unit for the cancel
# (SPEC-motion-language 規則 2 的兩段式消去); the expand itself is glyph-matched, which is
# `derivation._matching`'s own choice when only one side is segmented.
_DRAFT_EXPANDED = (r"{{(}} {{\sin u\cos v}} {{+\cos u\sin v)-(}} "
                   r"{{\sin u\cos v}} {{-\cos u\sin v)}}")
_CANCEL_SEGS = (1, 3)
_DRAFT_PRODUCT = r"2\cos u\sin v"
_DRAFT_RHS = r"2\cos\frac{A+B}{2}\,\sin\frac{A-B}{2}"   # step.0's own right-hand side
# The beat's own words, from the forced alignment (`audio_mimo/manifest.json` -> words_file),
# as a FRACTION of the beat so the draft tracks the narration rather than a metronome:
# beat-relative seconds / 39.14 s of beat run time.
_CUE = {
    "u":        0.108,   # 4.22  "put u equals the quantity A plus B, all over two,"
    "v":        0.224,   # 8.76  "and v equals the quantity A minus B, all over two,"
    "back":     0.341,   # 13.36 "so that A equals u plus v and B equals u minus v;"
    "expand":   0.489,   # 19.14 "expand sine of u plus v, minus sine of u minus v,"
    "formulas": 0.603,   # 23.60 "... with the angle-sum formulas,"
    "terms":    0.676,   # 26.44 "and the sine u cosine v terms"
    "cancel":   0.725,   # 28.36 "cancel,"
    "leaving":  0.756,   # 29.58 "leaving exactly two cosine u sine v."
    "handoff":  0.815,   # 31.90 the product IS step.0's right-hand side; hand it over
    "clear":    0.920,   # 36.01 "A product is also exactly what we want ..." -- draft spent
}


def _draft_line(tex: str, ground: str, y: float):
    """One line of the scene-04 draft, left-flush in the indented draft column."""
    mob = brand.math_line(tex, ground, role="text", size="math_sm")
    mob.move_to([_DRAFT_X, y, 0], aligned_edge=LEFT)
    return mob


def difference_quotient_for_sine(spec, ctx, blocks):
    from pipeline.templates.derivation import MUTED_OPACITY

    ground = ctx["ground"]
    ids = _by_id(blocks)
    FADE = 0.5

    def _core(mob):
        """The MathTex inside a row's equation mob (mirrors derivation._eq_core)."""
        if isinstance(mob, MathTex):
            return mob
        for sub in getattr(mob, "submobjects", []):
            found = _core(sub)
            if found is not None:
                return found
        return None

    def _rail(row, eq_wrap):
        return VGroup(*[m for m in row.submobjects if m is not eq_wrap])

    # -- beat 3: write step.0, then draft its derivation in the band below it -----------
    step0_row = ids["step.0"].mobject
    step0_eq = _core(step0_row)
    step0_rail = _rail(step0_row, step0_row.submobjects[0])

    subs = [_draft_line(tex, ground, y) for tex, y in zip(_DRAFT_SUBS, _DRAFT_Y)]
    work = _draft_line(_DRAFT_START, ground, _DRAFT_Y[2])
    expanded = _draft_line(_DRAFT_EXPANDED, ground, _DRAFT_Y[2])
    product = _draft_line(_DRAFT_PRODUCT, ground, _DRAFT_Y[2])
    # Where the draft's product belongs: step.0's own right-hand side. Built at the row's ink
    # and size and right-aligned to the row, so the flown copy lands ON the line it justifies
    # (move_to(..., aligned_edge=RIGHT) matches the right edge AND the vertical centre).
    landed = brand.math_line(_DRAFT_RHS, ground, role="primary", size="math")
    landed.move_to(step0_eq.get_right(), aligned_edge=RIGHT)

    def _step0_anim(scene, mob, g) -> float:
        """The row, then the draft, cut to the narration's own cue words (`_CUE`)."""
        total = TM.beat_run_time(scene, 18.0)
        # `t` stays the NOMINAL cue clock the `hold(...)` calls schedule against: the cut
        # points are fractions of `total`, so they must not drift with the frame rounding.
        # What the BEAT is told is the renderer's own clock instead (see `_elapsed`).
        t = 0.0
        t0 = _elapsed(scene)

        def at(cue):
            return total * _CUE[cue]

        def play(*anims, run_time):
            nonlocal t
            rt = max(run_time, 0.25)
            scene.play(*anims, run_time=rt)
            t += rt

        def hold(until):
            nonlocal t
            if until > t:
                scene.wait(until - t)
                t = until

        # (1) "Here it is." -- the row, written while it is read (pacing's atomic-write rate,
        #     capped so it is finished by the time the narration starts deriving it).
        w = max(at("u") - pacing.FADE_SECONDS - 0.4, 1.0)
        play(Write(step0_eq), run_time=min(pacing.write_seconds(step0_eq, w), w))
        if step0_rail.submobjects:
            play(FadeIn(step0_rail), run_time=pacing.FADE_SECONDS)
        scene.add(mob)
        hold(at("u"))

        # (2) "put u = (A+B)/2, and v = (A-B)/2, so that A = u+v and B = u-v"
        for part, cue in zip(subs[0].submobjects, ("u", "v")):
            hold(at(cue))
            play(FadeIn(part, shift=0.1 * UP), run_time=pacing.FADE_SECONDS)
        scene.add(subs[0])
        hold(at("back"))
        play(FadeIn(subs[1], shift=0.1 * UP), run_time=pacing.FADE_SECONDS)

        # (3) "expand sin(u+v) - sin(u-v) ... with the angle-sum formulas" -- the same line
        #     rewriting itself, not a second line arriving finished.
        hold(at("expand"))
        play(Write(work), run_time=2.2)
        hold(at("formulas"))
        play(TransformMatchingShapes(work, expanded), run_time=1.6)

        # (4) "... and the sin u cos v terms cancel, leaving exactly 2 cos u sin v": the two
        #     terms are framed (WHICH two), dimmed, then gone, and only then do the survivors
        #     close up -- the two-stage elimination of SPEC rule 2, in place.
        scene.remove(expanded)
        gone = VGroup(*[expanded.submobjects[i] for i in _CANCEL_SEGS])
        keep = VGroup(*[m for i, m in enumerate(expanded.submobjects)
                        if i not in _CANCEL_SEGS])
        scene.add(keep, gone)
        boxes = VGroup(*[SurroundingRectangle(s, color=T.color(g, "hairline_strong"),
                                              buff=0.07, stroke_width=2.0) for s in gone])
        hold(at("terms"))
        play(Create(boxes), run_time=0.7)
        hold(at("cancel"))
        play(gone.animate.set_color(T.color(g, "muted")), run_time=0.45)
        play(FadeOut(gone), FadeOut(boxes), run_time=0.45)
        hold(at("leaving"))
        play(TransformMatchingShapes(keep, product), run_time=1.2)

        # (5) The product is step.0's right-hand side, so a copy goes and says so. The
        #     substitution lines leave first: they are spent, and they sit on the flight path.
        hold(at("handoff"))
        play(FadeOut(subs[0]), FadeOut(subs[1]), run_time=0.7)
        flyer = product.copy()
        scene.add(flyer)
        play(TransformMatchingShapes(flyer, landed), run_time=1.1)
        play(FadeOut(landed), run_time=0.4)     # step.0's own RHS is underneath, untouched

        # (6) "A product is also exactly what we want ..." -- clear the band well before
        #     {show step.1} needs it.
        hold(at("clear"))
        play(FadeOut(product), run_time=0.8)
        hold(total)
        return _spent(scene, t0, max(total, t))

    ids["step.0"].anim = _step0_anim
    # The forced plays alone (the write, six fades, three morphs, the flight): what make.py's
    # short-beat warning should compare against if this beat is ever re-cut shorter.
    ids["step.0"].anim_seconds = 12.0

    # -- beat 4: the intermediate line, then the 2s cancel ------------------------------
    step1_row, step2_row = ids["step.1"].mobject, ids["step.2"].mobject
    step2_eq = _core(step2_row)
    step2_wrap = step2_row.submobjects[0]
    # Exactly the line the narration dictates -- "write h as 2 times h/2, so the denominator
    # carries the very h/2 inside the sine" -- so nothing new is asserted, only shown.
    inter = MathTex(r"\frac{\sin(x+h)-\sin x}{h} = "
                    r"\frac{2\cos\!\left(x+\frac h2\right)\sin\frac h2}{2\cdot\frac h2}",
                    color=step2_eq.get_color(), font_size=step2_eq.font_size)
    if inter.height > step2_eq.height * 1.7:      # a two-storey fraction must not reach the
        inter.scale_to_fit_height(step2_eq.height * 1.7)   # rows above and below it
    inter.move_to(step2_eq.get_left(), aligned_edge=LEFT)

    def _step2_anim(scene, mob, _ground) -> float:
        total = TM.beat_run_time(scene, 4.2)
        a, b = total * 0.36, total * 0.34
        c = max(total - a - b, 0.6)
        t0 = _elapsed(scene)
        scene.play(FadeIn(inter, shift=0.1 * UP),
                   step1_row.animate.set_opacity(MUTED_OPACITY), run_time=FADE)
        scene.wait(max(a - FADE, 0.0))
        morph = min(1.4, b)
        scene.play(ReplacementTransform(inter, step2_eq), run_time=morph)   # the 2s cancel
        scene.wait(max(b - morph, 0.0))
        rail = _rail(mob, step2_wrap)
        if rail.submobjects:
            scene.play(FadeIn(rail), run_time=FADE)
        scene.wait(max(c - FADE, 0.0))
        scene.add(mob)
        return _spent(scene, t0, total)

    # -- beat 5: one factor per clause --------------------------------------------------
    result_row = ids["result"].mobject
    result_wrap = result_row.submobjects[0]
    result_eq = _core(result_row)
    # Same LaTeX, split at the clause the narration splits it at: MathTex concatenates its
    # args, so the rendered line is identical to the single-string one it replaces.
    parts_eq = MathTex(r"\cos\!\left(x+\frac h2\right)\to\cos x",
                       r"\quad\text{and}\quad",
                       r"\frac{\sin(h/2)}{h/2}\to 1",
                       color=result_eq.get_color(), font_size=result_eq.font_size)
    parts_eq.move_to(result_eq.get_left(), aligned_edge=LEFT)
    result_wrap.submobjects = [parts_eq]

    def _result_anim(scene, mob, _ground) -> float:
        rail = _rail(mob, result_wrap)
        slots = len(parts_eq.submobjects) + (1 if rail.submobjects else 0)
        total = TM.beat_run_time(scene, FADE * slots)
        share = total / slots
        t0 = _elapsed(scene)
        scene.play(FadeIn(parts_eq[0], shift=0.1 * UP),
                   step2_row.animate.set_opacity(MUTED_OPACITY), run_time=FADE)
        scene.wait(max(share - FADE, 0.0))
        for part in parts_eq.submobjects[1:]:
            scene.play(FadeIn(part, shift=0.1 * UP), run_time=FADE)
            scene.wait(max(share - FADE, 0.0))
        if rail.submobjects:
            scene.play(FadeIn(rail), run_time=FADE)
            scene.wait(max(share - FADE, 0.0))
        scene.add(mob)
        return _spent(scene, t0, total)

    ids["step.2"].anim, ids["step.2"].anim_seconds = _step2_anim, FADE * 3
    ids["result"].anim, ids["result"].anim_seconds = _result_anim, FADE * 4
    return blocks


# ================================================================ hook 8
# why_trig_is_different (scene 03) -- the film's first teaching beat, and 17.6 s of it is
# spoken over an empty right half. The narration contrasts two difference quotients ("the
# binomial theorem handed us a factor of h to cancel ... the trigonometric functions refuse
# to play along") and the screen shows neither: four lenses land on it (R1a L-attention
# must, R2 D-carry must "17.6 秒、52 個字…畫面一個字都沒給", R4 T-dwell must, plus R2
# D-composition "一整場都在浪費一半畫面"). The hook puts the polynomial case in that empty
# half and CANCELS the h on screen, so the trig row that follows (math.0, already there,
# already ending in 0/0) reads as the contrast it is meant to be. Same device as hook 7's
# step.2: the line the narration describes, morphed into the line it becomes.


def why_trig_is_different(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    out = list(blocks)

    # The band above the statement is free all scene; the ASSUMES pill lands in its LEFT
    # half at the very last beat, so the exhibit sits right of centre and the two balance
    # instead of colliding.
    MAX_W = 7.2
    CENTRE = np.array([2.55, 1.25, 0.0])

    tag = brand.eyebrow("polynomial", ground, role="muted", size="tag")
    before = brand.math_line(r"\frac{(x+h)^n-x^n}{h}=\frac{h\left[nx^{n-1}+\cdots\right]}{h}",
                             ground, role="text", size="math")
    after = brand.math_line(r"\frac{(x+h)^n-x^n}{h}=nx^{n-1}+\cdots",
                            ground, role="text", size="math")
    for m in (before, after):
        if m.width > MAX_W:
            m.scale_to_fit_width(MAX_W)
    # `after` is what stays on screen, so IT owns the slot; `before` is a transient that
    # occupies the same left edge and baseline so the cancellation reads as one line
    # rewriting itself rather than two lines swapping places.
    body = VGroup(tag, after).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
    body.move_to(CENTRE)
    before.move_to(after.get_left(), aligned_edge=LEFT)

    def _cancels_anim(scene, mob, _ground) -> float:
        """Write the quotient the binomial theorem hands us, then let the h cancel."""
        total = TM.beat_run_time(scene, 4.0)
        a = total * 0.42
        morph = min(1.3, total * 0.22)
        t0 = _elapsed(scene)
        scene.play(FadeIn(tag), FadeIn(before, shift=0.1 * UP), run_time=0.55)
        scene.wait(max(a - 0.55, 0.0))
        scene.play(ReplacementTransform(before, after), run_time=morph)
        scene.wait(max(total - a - morph, 0.0))
        scene.add(mob)
        return _spent(scene, t0, total)

    out.append(Block("cancels", body, anim=_cancels_anim, static=False))
    return out


# ================================================================ hook 6
# limit_not_identity (Caution) -- the ratio curve, carried in from squeeze_graph,
# opens out past pi/2 to pi so the two values the caution names can be READ OFF it.
#
# R2 director lens, 2026-09-13 (a `must` on the rerun): this is the scene whose whole job
# is to stop a misreading -- "the limit is 1" heard as "the ratio is 1" -- and it was the
# scene with the least picture behind it, while the one curve that settles the question in
# a second had been drawn 20 s earlier in squeeze_graph and thrown away. `carry:` (rollout
# T4) now brings that curve across the cut as a corner inset. What it cannot do is show
# theta = pi: squeeze_graph is a CLOSE-UP, x in [-1.85, 1.85], and pi is off its right edge.
#
# So the inset opens back out. Zooming out is not decoration here, it IS the argument: the
# close-up is the picture that makes the ratio look like 1, and stepping back is what shows
# it is not. The wide view keeps the same curve, the same y = 1 ceiling and the same hollow
# circle at theta = 0, drops cos (which leaves the frame past pi/2 and has no part in this
# caution), and gains the two read-offs the narration names, one per beat.


def ratio_readouts(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    inset = ids["carried.graph"].mobject       # the close-up carried across the cut
    body = ids["body"].mobject

    amber = T.color(ground, "accent")
    mut = T.color(ground, "muted")

    X0, X1 = -0.25, 3.45                        # far enough right to hold theta = pi

    def _ratio(t):
        return 1.0 if abs(t) < 1e-9 else float(np.sin(t) / t)

    # y top 1.18 -> 1.32: at 1.18 the axis ARROW TIP sat directly over the open circle at
    # (0, 1) -- the one mark this scene cannot afford to obscure, since "undefined at
    # theta = 0" is its whole point (visual frame audit). Keeping the tips and moving the
    # ceiling up is better than dropping the tips, which every other graph in the deck has.
    axes = Axes(x_range=[X0, X1, 1.0], y_range=[0.0, 1.32, 0.5],
                x_length=7.6, y_length=2.0, tips=True,
                axis_config={"color": mut, "stroke_width": 1.6, "include_ticks": False})
    # stop at pi exactly: past it the ratio goes negative, off the bottom of this y range
    # and straight through the theta label at the axis tip -- and pi is where the
    # narration stops too ('at theta = pi it is zero').
    curve = axes.plot(_ratio, x_range=[0.015, float(PI)], color=amber, stroke_width=4.0)
    ceiling = DashedLine(axes.c2p(X0, 1.0), axes.c2p(X1, 1.0), color=mut,
                         stroke_width=2.0, dash_length=0.09)
    # the same open circle squeeze_graph carries: the ratio is undefined AT zero, and this
    # scene is precisely about not confusing "the limit" with "the value".
    hollow = Circle(radius=0.075, color=amber, stroke_width=3.0,
                    fill_color=T.color(ground, "bg"), fill_opacity=1.0)
    hollow.move_to(axes.c2p(0.0, 1.0))
    ticks = VGroup()
    for xv, tex in [(PI / 2, r"\tfrac{\pi}{2}"), (PI, r"\pi")]:
        p = axes.c2p(xv, 0.0)
        ticks.add(Line(p + 0.08 * UP, p + 0.08 * DOWN, color=mut, stroke_width=2.0))
        ticks.add(MathTex(tex, color=mut, font_size=T.fs("label")).next_to(p, DOWN, buff=0.18))
    one_lab = brand.math_line("1", ground, role="muted", size="label")
    one_lab.next_to(axes.c2p(X0, 1.0), LEFT, buff=0.12)
    th_lab = brand.math_line(r"\theta", ground, role="text", size="label")
    th_lab.next_to(axes.x_axis.get_right(), DOWN, buff=0.12)
    ratio_lab = brand.math_line(r"\tfrac{\sin\theta}{\theta}", ground, role="accent", size="label")
    ratio_lab.move_to(axes.c2p(2.25, 0.62))    # under the curve's falling arm, clear of it
    wide = VGroup(axes, ceiling, one_lab, ticks, th_lab, curve, hollow, ratio_lab)

    # the empty lower band the caution's own `sparse_ok` whitespace leaves free
    zone_top = body.get_bottom()[1] - 0.50
    zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.15
    wide.move_to([0.0, (zone_top + zone_bottom) / 2, 0.0])

    def _readout(xv, tex, above):
        """A dot on the curve at *xv* with the value the narration reads out."""
        p = axes.c2p(xv, _ratio(xv))
        foot = axes.c2p(xv, 0.0)
        dot = Dot(p, radius=0.075, color=amber)
        lab = brand.math_line(tex, ground, role="accent", size="label")
        lab.next_to(dot, UP + RIGHT if above else DOWN + RIGHT, buff=0.16)
        # at theta = pi the point IS on the axis, so there is no drop to draw
        if abs(p[1] - foot[1]) < 0.05:
            return VGroup(dot, lab)
        drop = DashedLine(foot, p, color=mut, stroke_width=1.6, dash_length=0.07)
        return VGroup(drop, dot, lab)

    half = _readout(PI / 2, r"\tfrac{2}{\pi}\approx 0.64", True)

    # theta = pi: a dot WALKS down the curve from pi/2 and the label lands when it arrives.
    # Built at the terminal position (the gates measure the last frame); the reveal rewinds
    # the tracker and runs it across the beat.
    walk_t = ValueTracker(float(PI))
    at_pi_dot = always_redraw(
        lambda: Dot(axes.c2p(walk_t.get_value(), _ratio(walk_t.get_value())),
                    radius=0.075, color=amber))
    at_pi_lab = brand.math_line("0", ground, role="accent", size="label")
    at_pi_lab.next_to(axes.c2p(float(PI), 0.0), UP + RIGHT, buff=0.16)
    at_pi = VGroup(at_pi_dot, at_pi_lab)

    def _walk_to_pi(scene, mob, _ground) -> float:
        """Send the dot from pi/2 to pi across whatever the beat has, then label it."""
        t0 = _elapsed(scene)
        walk_t.set_value(float(PI) / 2.0)
        scene.add(at_pi_dot)
        budget = TM.beat_run_time(scene, 2.0)
        run = max(budget - 1.0, 0.6)
        scene.play(walk_t.animate.set_value(float(PI)), run_time=run, rate_func=linear)
        scene.play(FadeIn(at_pi_lab), run_time=0.45)
        scene.add(mob)
        return _elapsed(scene) - t0

    def _open(scene, mob, _ground) -> float:
        """The corner close-up grows back out into the full picture."""
        t0 = _elapsed(scene)
        scene.play(ReplacementTransform(inset, mob),
                   run_time=min(max(TM.beat_run_time(scene, 1.4) * 0.6, 0.9), 1.8))
        scene.add(mob)
        return _elapsed(scene) - t0

    def _land(scene, mob, _ground) -> float:
        """Draw the read-off one part at a time, spread over the beat it is read on."""
        parts = list(mob)
        # an equal share of the beat, capped so a long beat is not crawled out;
        # never MORE than the share, or the scene outruns its own narration.
        each = min(TM.beat_run_time(scene, 0.9) / len(parts), 1.1)
        t0 = _elapsed(scene)
        for part in parts:
            scene.play(Create(part) if isinstance(part, DashedLine) else FadeIn(part),
                       run_time=each)
        scene.add(mob)
        return _elapsed(scene) - t0

    out = list(blocks)
    out.append(Block("opened", wide, anim=_open, static=False, layer="graph"))
    out.append(Block("at_half_pi", half, anim=_land, static=False, layer="graph"))
    out.append(Block("at_pi", at_pi, anim=_walk_to_pi, static=False, layer="graph"))
    return out


def _elapsed(scene) -> float:
    """The renderer's own clock. A reveal must report what it ACTUALLY consumed, not the
    sum of its `run_time`s: manim rounds every `play` up to a whole frame, so a reveal made
    of several plays under-reports by a frame each, the beat then holds for a remainder that
    is too long, and the scene ends up longer than its narration ([sync] render/audio length).
    Measured on continuity_argument: 3 plays instead of 1 put the scene 0.23-0.33 s over.
    Reads 0 on a scene with no renderer (the selftests' FakeScene); `_spent` turns that
    into the caller's nominal budget."""
    return float(getattr(getattr(scene, "renderer", None), "time", 0.0))


def _spent(scene, t0: float, nominal: float) -> float:
    """What a reveal reports to its beat: the renderer's clock where there is one, and
    *nominal* where there is none. The pipeline selftests drive these hooks with a
    FakeScene that records `run_time`s but has no renderer, and they assert on the
    returned seconds -- so the nominal budget stays the answer off a real render."""
    if getattr(scene, "renderer", None) is None:
        return nominal
    return _elapsed(scene) - t0


def _play_stock(scene, anim, mob, ground) -> float:
    """Run a block's stock reveal (an anim NAME or a callable) and report what it cost --
    so a hook can wrap a reveal instead of replacing it."""
    if callable(anim):
        return float(anim(scene, mob, ground))
    return float(play_block(scene, Block("_", mob, anim=anim, static=False), ground))


# ================================================================ hook 7
# continuity_argument (Proposition 3.1, proof part 2/2) -- the second sum-to-product
# identity is the FIRST one with only the changed tokens flipped, and the half-gap that
# both of them hang on gets a picture.
#
# R2 director lens, 2026-09-13 (a `must` on the rerun): the most abstract scene in the
# film, 70 seconds, not one figure -- four rows of symbols, revealed one at a time. Two
# things are actually happening in it and neither was visible:
#
#   1. The two identities are ONE template filled twice. Writing the second from scratch
#      hides that; morphing the first into it (SPEC-motion-language 規則 2, 只動變的 token)
#      shows cos flip to sin, the leading minus leave, and the two half-angle factors trade
#      places, while everything they share simply glides. No on-screen text changes.
#   2. Everything collapses because the HALF-GAP (x - x_0)/2 goes to zero. That is a
#      number line: x_0 fixed, x sliding into it, the bracket between them closing. The qed
#      beat says "let x -> x_0: the half-angle goes to zero" -- now it happens on screen,
#      paced to the beat, in the empty lower-right quadrant the proof column never uses.
def continuity_template(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    row0 = ids["proof.0"].mobject
    qed_block = ids["qed"]

    amber = T.color(ground, "accent")
    mut = T.color(ground, "muted")
    ink = T.color(ground, "text")

    # -- the second identity: the first one with the changed tokens flipped ------
    def _fill_second(scene, mob, _ground) -> float:
        total = TM.beat_run_time(scene, 1.6)
        t0 = _elapsed(scene)
        ghost = row0.copy()
        scene.add(ghost)
        # Let the morph actually UNFOLD. A 1.4 s cap left 15.2 s of frozen picture on a
        # 16.6 s beat -- the film's real worst dead zone, and mine. The narration over this
        # beat is reading the sine identity aloud, so a morph that takes most of the reading
        # is well matched: you watch cos turn into sin while you hear it.
        scene.play(TransformMatchingShapes(ghost, mob),
                   run_time=min(max(total * 0.55, 1.2), 8.0))
        scene.add(mob)
        _mark_factors(scene)
        return _elapsed(scene) - t0

    ids["proof.1"].anim = _fill_second

    # -- proof.0 keeps its WRITE ------------------------------------------------
    # The row was split into {{...}} segments so the box below has something to surround.
    # `pacing.block_parts` reads two submobjects as "a block with parts to walk", which
    # would turn "the row is written as it is read" into two fades -- so name the write.
    ids["proof.0"].anim = lambda scene, mob, _g: pacing.paced_write(scene, mob)

    # -- the half-sum factor, marked (R2 round-18 must, ML3) ---------------------
    # Segment 1 of each row IS the half-sum factor (see the storyboard's {{...}}). The beat
    # says "in each, the half-sum factor never exceeds one in size" and nothing on screen
    # said WHICH piece that was: box both, drop the rest of each row back, and hang one
    # shared bound off the pair. Built at play time, not here, because the rows are still
    # being positioned while hooks run.
    #
    # R2 asked for the boxed factors to "become 1" on the next beat. Not done, deliberately:
    # replacing them in place would leave `cos x - cos x_0 = -2 sin(half-diff) . 1` on screen,
    # which is false -- the factor is BOUNDED by one, not equal to it. The boxes instead
    # leave as proof.2's genuine inequality row arrives, and the existing `focus.indicate`
    # flashes both rows there, so the beat still points back at them.
    marks: list = []

    def _mark_factors(scene) -> None:
        rows = [ids["proof.0"].mobject, ids["proof.1"].mobject]
        if any(len(r.submobjects) < 2 for r in rows):
            return                                   # un-segmented: nothing to address
        boxes = VGroup(*[SurroundingRectangle(r.submobjects[1], color=amber,
                                              stroke_width=2.4, buff=0.09) for r in rows])
        bound = brand.math_line(r"|\,\cdot\,|\le 1", ground, role="accent", size="label")
        bound.next_to(boxes, RIGHT, buff=0.34)
        rest = VGroup(*[s for r in rows for i, s in enumerate(r.submobjects) if i != 1])
        # multiplicative fade in, snapshot/restore out -- focus.apply's contract, for the
        # same reason: a flat opacity paints over anything deliberately transparent.
        rest.save_state()
        marks.extend((boxes, bound, rest))
        scene.play(*[Create(b) for b in boxes],
                   rest.animate.fade(0.55), run_time=1.1)
        scene.play(FadeIn(bound), run_time=0.5)

    def _release_factors(scene) -> None:
        if not marks:
            return
        boxes, bound, rest = marks
        scene.play(FadeOut(boxes), FadeOut(bound), rest.animate.restore(), run_time=0.6)

    # -- the half-gap number line (lower right; the proof column keeps the left) --
    HALF_W = 2.15                       # half the line's length
    CENTRE = np.array([3.65, -1.95, 0.0])
    x0_pt = CENTRE + HALF_W * LEFT      # x_0 stays put
    gap = ValueTracker(1.0)             # 1 = x at the right end, 0 = x has arrived

    axis = Line(CENTRE + (HALF_W + 0.35) * LEFT, CENTRE + (HALF_W + 0.35) * RIGHT,
                color=mut, stroke_width=1.6)

    def _x_pt():
        return x0_pt + 2.0 * HALF_W * gap.get_value() * RIGHT

    def _mid_pt():
        return (x0_pt + _x_pt()) / 2.0

    def _dot_x():
        return Dot(_x_pt(), radius=0.075, color=amber)

    def _dot_mid():
        return Dot(_mid_pt(), radius=0.06, color=ink)

    def _bracket():
        """The half-gap itself: midpoint -> x, the argument of every sine in the bound."""
        a, b = _mid_pt() + 0.30 * DOWN, _x_pt() + 0.30 * DOWN
        if b[0] - a[0] < 0.04:
            return VGroup()
        return VGroup(Line(a, b, color=amber, stroke_width=3.0),
                      Line(a + 0.07 * UP, a + 0.07 * DOWN, color=amber, stroke_width=2.0),
                      Line(b + 0.07 * UP, b + 0.07 * DOWN, color=amber, stroke_width=2.0))

    def _x_label():
        # Once x has arrived, its label would sit exactly on top of x_0's and the two
        # would render as a permanent glyph pile in the scene's LAST frame (visual frame
        # audit, V2 blocking). x and x_0 coincide by then, so one label is the honest
        # picture: drop this one as the gap closes.
        if gap.get_value() < 0.08:
            return VGroup()
        return brand.math_line("x", ground, role="text", size="label").next_to(
            _x_pt(), UP, buff=0.16)


    dot_x0 = Dot(x0_pt, radius=0.075, color=ink)
    lab_x0 = brand.math_line("x_0", ground, role="text", size="label").next_to(
        x0_pt, UP, buff=0.16)
    lab_half = brand.math_line(r"\tfrac{x-x_0}{2}", ground, role="accent", size="label")
    lab_half.next_to(CENTRE + 0.30 * DOWN, DOWN, buff=0.22)
    # Two stages, because the narration introduces them two beats apart: the LINE (x_0, x,
    # and x moving) belongs to the statement beat, the HALF-gap (midpoint, bracket, the
    # (x-x_0)/2 label) to proof.2, where the bound first names it.
    line_group = VGroup(axis, dot_x0, lab_x0,
                        always_redraw(_dot_x), always_redraw(_x_label))
    half_group = VGroup(lab_half, always_redraw(_dot_mid), always_redraw(_bracket))

    # -- statement: draw the line, then let x ASK the question ------------------
    # 25 s of narration over one card was the last scene above the 12 s line. This beat
    # says "fix a point x_0, and ask how much they can change as x moves toward it" --
    # so x probes toward x_0 and back, twice, across whatever the beat has left. It
    # returns to where it started, so proof.2 and qed still open on a full gap.
    stmt_block = ids["statement"]
    stock_stmt = stmt_block.anim

    def _pose_question(scene, mob, _ground) -> float:
        t0 = _elapsed(scene)
        _play_stock(scene, stock_stmt, mob, _ground)
        scene.play(Create(axis), FadeIn(dot_x0), FadeIn(lab_x0), run_time=0.7)
        scene.add(line_group)
        used = _elapsed(scene) - t0
        left = TM.beat_run_time(scene, used + 1.2) - used - 0.4
        # One brisk probe, not a slow drift: x slides most of the way in and back so
        # "as x moves toward it" is something you see, then the line rests as a scaffold
        # until proof.2 adds the half-gap and qed closes it. (A drift spread over the
        # whole beat moved the dot ~0.2 u/s -- under a pixel per frame, and unreadable.)
        if left >= 3.0:
            scene.play(gap.animate.set_value(0.15), run_time=min(left * 0.45, 3.0),
                       rate_func=there_and_back)
        return _elapsed(scene) - t0

    stmt_block.anim = _pose_question

    # -- proof.2: the bound names the half-angle, so the half-gap arrives here ---
    p2_block = ids["proof.2"]
    stock_p2 = p2_block.anim

    def _show_half(scene, mob, _ground) -> float:
        t0 = _elapsed(scene)
        _release_factors(scene)
        _play_stock(scene, stock_p2, mob, _ground)
        scene.add(half_group)
        scene.play(FadeIn(lab_half), run_time=0.45)
        return _elapsed(scene) - t0

    p2_block.anim = _show_half

    # -- qed: the payoff beat draws the gap and then closes it ------------------
    # The figure is revealed from INSIDE this reveal rather than by a {show halfgap}
    # marker of its own: a new marker splits a beat, and this scene sits on the fallback
    # ladder's BEATS rung, where reuse is keyed by each beat's output FILE -- so the split
    # shifts every later beat and bills three MiMo calls. The qed beat is where the
    # narration says "let x -> x_0" anyway, so the whole figure lives in this one beat.
    # (Price of not being a Block: sizecheck's overlap pass does not see it. Measured by
    # hand instead -- x [+1.15, +6.15], y [-2.70, -1.66], inside the safe area and clear
    # of the proof column, whose widest row ends at +0.30.)
    stock_qed = qed_block.anim

    def _close_gap(scene, mob, _ground) -> float:
        """Reveal the qed line, then walk x into x_0 across whatever is left of the beat --
        the narration's own 'let x -> x_0' happening rather than being asserted. The line
        and the half-gap are already on screen (statement / proof.2)."""
        t0 = _elapsed(scene)
        _play_stock(scene, stock_qed, mob, _ground)
        # whatever the beat has left, never more: a floor here would run the scene
        # past its own narration and trip the [sync] render/audio length gate.
        used = _elapsed(scene) - t0
        walk = TM.beat_run_time(scene, used + 1.2) - used - 0.4
        if walk >= 0.25:
            scene.play(gap.animate.set_value(0.0), run_time=walk, rate_func=smooth)
        else:
            gap.set_value(0.0)
        # the bracket has collapsed to nothing, so its label is naming an object that is no
        # longer there -- take it with it (visual frame audit advisory)
        scene.play(FadeOut(lab_half), run_time=0.4)
        return _elapsed(scene) - t0

    qed_block.anim = _close_gap
    return blocks


# ================================================================ hook: shm_device
# shm_device (Example 3.3, scene shm_compute) -- R2 must (2026-09-13 鋪滿輪盲審): "全片
# 唯一一個具體的物理情境，畫面上完全不存在那個物件；'每一刻都被推回平衡點' 是本場的教學點，
# 卻只能靠文字宣稱." The weight-on-a-spring is named four times in the narration and never
# drawn. A small schematic (ceiling, spring, weight, equilibrium line) rides beside the
# four derivation rows, to their right (clear of the reason rail, safe-area checked):
#   {show step.0}  the device fades in and the weight starts oscillating as s(t)=sin t
#                  (TM.beat_run_time fills the rest of this beat; a dt updater on the
#                  ValueTracker keeps it swinging through every later beat, including the
#                  plain scene.wait()s _play_content adds -- it is never re-started).
#   {show step.1}  a velocity arrow joins (secondary/blue, s'(t)=cos t).
#   {show step.2}  an acceleration arrow joins (success/green, s''(t)=-sin t), ALWAYS
#                  pointing at the equilibrium line -- toward rest, never away.
#   {show result}  the displacement itself is drawn in amber (accent, sin's colour
#                  elsewhere in this section), so "acceleration opposite displacement" --
#                  s''=-s -- is something the viewer watches for the rest of the beat, not
#                  a claim taken on faith.
# Reveal ids are unchanged; each row's EXISTING anim (a plain "write", or result's
# transform+frame+paced rail) is run first via `_play_stock` (continuity_argument's
# helper, above) and still plays exactly as it did -- the device stages on top of it.
# Skeleton (ceiling/spring/weight outline) is muted/text; only the three taught
# quantities (s, s', s'') carry colour, matching Figure 3.4's palette one scene later.


def shm_device(spec, ctx, blocks):
    ground = ctx["ground"]
    ids = _by_id(blocks)
    anchor = ids.get("scaffold.motive") or ids.get("sollead") or ids["title"]

    amber = T.color(ground, "accent")      # displacement / s(t) = sin t
    blue = T.color(ground, "secondary")    # velocity / s'(t) = cos t
    green = T.color(ground, "success")     # acceleration / s''(t) = -sin t
    mut = T.color(ground, "muted")
    text = T.color(ground, "text")

    row_ids = [r for r in ("step.0", "step.1", "step.2", "result") if r in ids]
    rows_right = max(ids[r].mobject.get_right()[0] for r in row_ids)

    AMP = 0.8          # weight's vertical swing, scene units -- s(t) = sin t
    BOX = 0.4          # weight square side
    REST_LEN = 1.7     # spring's natural length, ceiling -> equilibrium
    ARROW_LEN = 0.6    # arrow length at |value| = 1
    ARM = 0.4          # horizontal offset of the velocity/accel arrows off the spring's column
    dev_half_w = ARM + ARROW_LEN + 0.35

    right_safe = T.FRAME_W / 2 - T.SAFE_MARGIN
    dev_x = min(rows_right + 0.55 + dev_half_w, right_safe - dev_half_w)

    zone_top = anchor.mobject.get_bottom()[1] - 0.55
    zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.15
    dev_height = REST_LEN + AMP + BOX / 2 + ARROW_LEN + 0.3
    ceiling_y = zone_top - max((zone_top - zone_bottom - dev_height) / 2, 0.05)
    equilibrium_y = ceiling_y - REST_LEN
    CEIL = np.array([dev_x, ceiling_y, 0.0])
    EQ = np.array([dev_x, equilibrium_y, 0.0])

    t_track = ValueTracker(0.0)
    OMEGA = 1.6   # rad/s -- a few visible cycles across the scene, not frantic

    def _s():
        return float(np.sin(t_track.get_value()))

    def _weight_pt():
        return EQ + AMP * _s() * UP

    ceiling = Line(CEIL + 0.6 * LEFT, CEIL + 0.6 * RIGHT, color=mut, stroke_width=3.0)
    hatch = VGroup(*[
        Line(CEIL + x * RIGHT, CEIL + x * RIGHT + 0.16 * LEFT + 0.26 * DOWN,
             color=mut, stroke_width=1.6)
        for x in np.linspace(-0.45, 0.45, 5)
    ])
    equilibrium = DashedLine(EQ + 0.85 * LEFT, EQ + 0.85 * RIGHT, color=mut,
                             stroke_width=1.6, dash_length=0.08)

    def _spring():
        """Zigzag ceiling -> current weight top, rebuilt every frame (weight moves)."""
        top, bot = CEIL, _weight_pt() + (BOX / 2) * UP
        n = 6
        pts = [top]
        for i in range(1, n):
            side = 0.16 if i % 2 else -0.16
            pts.append(top + (i / n) * (bot - top) + side * RIGHT)
        pts.append(bot)
        return VGroup(*[Line(pts[i], pts[i + 1], color=mut, stroke_width=2.2)
                       for i in range(len(pts) - 1)])

    def _weight():
        return Rectangle(width=BOX, height=BOX, color=text,
                         fill_color=T.color(ground, "bg"), fill_opacity=1.0,
                         stroke_width=2.6).move_to(_weight_pt())

    def _vel_arrow():
        """Velocity s'=cos t: vertical, signed length -- shrinks to nothing at the
        swing's ends, longest passing through equilibrium (exactly where cos peaks)."""
        v = float(np.cos(t_track.get_value()))
        if abs(v) < 0.05:
            return VGroup()
        base = _weight_pt() + ARM * RIGHT
        return Arrow(base, base + v * ARROW_LEN * UP, color=blue, buff=0.0,
                    stroke_width=4.0, max_tip_length_to_length_ratio=0.3)

    def _acc_arrow():
        """Acceleration s''=-sin t: always signed toward the equilibrium line -- this
        is the arrow the R2 must exists for (it visibly never points away from rest)."""
        a = -_s()
        if abs(a) < 0.05:
            return VGroup()
        base = _weight_pt() + ARM * LEFT
        return Arrow(base, base + a * ARROW_LEN * UP, color=green, buff=0.0,
                    stroke_width=4.0, max_tip_length_to_length_ratio=0.3)

    def _displacement():
        return Line(EQ, _weight_pt(), color=amber, stroke_width=5.5)

    spring = always_redraw(_spring)
    weight = always_redraw(_weight)
    vel_arrow = always_redraw(_vel_arrow)
    acc_arrow = always_redraw(_acc_arrow)
    displacement = always_redraw(_displacement)

    # size "label"(30px)->"math_sm"(40px)（2026-09-13 合併版視覺幀稽核）：s/s'/s'' 三個裝置標籤
    # 單一字母的有效字級只有約 18-22 px，升一階讀得到。
    vel_label = brand.math_line("s'", ground, role="secondary", size="math_sm")
    vel_label.move_to(CEIL + ARM * RIGHT + 0.32 * UP)
    acc_label = brand.math_line("s''", ground, role="success", size="math_sm")
    acc_label.move_to(CEIL + ARM * LEFT + 0.32 * UP)
    s_label = brand.math_line("s", ground, role="accent", size="math_sm")
    s_label.next_to(EQ + 0.85 * RIGHT, RIGHT, buff=0.12)

    device = VGroup(ceiling, hatch, equilibrium, spring, weight, vel_arrow, acc_arrow,
                    displacement, vel_label, acc_label, s_label)

    def _freeze():
        """Stop every updater before the scene's own `exit:` FadeOut runs -- an
        always_redraw block still ticking would `become()` back to full opacity
        each frame and fight the fade (house gotcha; see sector_inequality's
        _evenness_anim, which sidesteps it by never fading a live block at all)."""
        for m in (spring, weight, vel_arrow, acc_arrow, displacement, t_track):
            m.clear_updaters()

    def _stage_step0(scene, ground, base):
        scene.play(FadeIn(VGroup(ceiling, hatch, equilibrium)), run_time=0.5)
        t_track.add_updater(lambda m, dt: m.increment_value(dt * OMEGA))
        scene.add(spring, weight, t_track)    # always_redraw: pop in, not faded (house style)
        remaining = max(TM.beat_run_time(scene, 3.0) - base - 0.5, 0.6)
        scene.wait(remaining)

    def _stage_step1(scene, ground, base):
        scene.add(vel_arrow)                  # always_redraw: pop in, not faded
        scene.play(FadeIn(vel_label), run_time=0.3)

    def _stage_step2(scene, ground, base):
        scene.add(acc_arrow)
        scene.play(FadeIn(acc_label), run_time=0.3)

    def _stage_result(scene, ground, base):
        scene.add(displacement)
        scene.play(FadeIn(s_label), run_time=0.3)
        _freeze()

    def _wrap(rid, stage):
        orig = ids[rid].anim

        def _anim(scene, mob, ground):
            t0 = _elapsed(scene)
            base = _play_stock(scene, orig, mob, ground)
            stage(scene, ground, base)
            return _elapsed(scene) - t0
        return _anim

    ids["step.0"].anim = _wrap("step.0", _stage_step0)
    ids["step.1"].anim = _wrap("step.1", _stage_step1)
    ids["step.2"].anim = _wrap("step.2", _stage_step2)
    ids["result"].anim = _wrap("result", _stage_result)

    out = list(blocks)
    # Never revealed through a `{show ...}` marker (the device rides the four rows'
    # own beats above) -- this Block exists only so `exit:` and sizecheck's overflow
    # guard can find it by id. `static=False` + unrevealed means scene.py's own
    # end-of-beats sweep (_play_content's final `for block in blocks: ... play_block`,
    # which forces any block nobody showed) WILL call this anim once, so it must be a
    # true no-op -- a real stock reveal here (e.g. "fade") would fade the whole live
    # device in a second time right before `exit:` fades it back out, visibly blinking
    # it (found via the +end-1.5s mock-render frame, first cut of this hook).
    out.append(Block("device", device, static=False,
                     anim=lambda scene, mob, ground: 0.0, layer="graph"))
    return out

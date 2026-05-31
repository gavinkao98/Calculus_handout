"""Custom hooks for Chapter 1 precise-limit (epsilon-delta) scenes."""

from __future__ import annotations

import math

from manim import (
    Axes,
    Create,
    DashedLine,
    Dot,
    DOWN,
    FadeIn,
    LEFT,
    MathTex,
    RIGHT,
    Tex,
    UP,
    VGroup,
    Write,
)

from manim_templates.helpers import theme_color


def epsilon_delta_picture(
    scene, scene_spec: dict[str, object], context: dict[str, object]
) -> None:
    """Geometric reading of the epsilon-delta definition.

    Builds the figure progressively so that the storyboard's voiceover beats line up:
    curve -> limit point -> epsilon band -> delta strip projected down ->
    box-corner boundary dots. The function is f(x) = 2^x, with a = 3, L = 8,
    epsilon ~ 1.5, delta ~ 0.20 (chosen so that the graph over (a-delta, a+delta)
    sits comfortably inside the (L-epsilon, L+epsilon) band).

    Note on the box corners. The two boundary dots sit at the *corners* of the
    epsilon-delta rectangle, (a +/- delta, L +/- epsilon), not on the curve at
    (a +/- delta, f(a +/- delta)). For any function with f''(a) != 0 (the convex
    f(x) = 2^x is one), no single delta makes the curve pass through both corners
    simultaneously: f(a + delta) - L != L - f(a - delta) for delta > 0. The
    corner-placement choice keeps the picture symmetric about the band lines and
    accepts that the curve is visibly inside the box at both boundaries -- which
    is exactly the message of "the graph over the delta-strip lies inside the
    epsilon-band". A linear f would let the corners triple-coincide with the
    curve, but loses the curvature that makes "epsilon-delta on a curve" the
    pedagogical point.
    """
    theme = context["theme"]
    scene.clear()

    a = 3.0
    L = 8.0
    epsilon = 1.5
    delta = 0.20

    title = Tex(
        rf"\textbf{{{scene_spec['title']}}}",
        color=theme_color(theme, "primary"),
        font_size=float(theme["typography"]["title_size"]),
    )
    title.to_edge(UP, buff=0.4)

    axis_config = {"color": theme_color(theme, "grid"), "stroke_width": 1.5}
    axes = Axes(
        x_range=[0, 4, 1],
        y_range=[0, 14, 2],
        x_length=8.5,
        y_length=4.6,
        axis_config=axis_config,
        tips=True,
    )
    axes.next_to(title, DOWN, buff=0.5)

    def f(x: float) -> float:
        return math.pow(2.0, x)

    curve_left = axes.plot(
        f,
        x_range=[0.45, a - 0.04],
        color=theme_color(theme, "secondary"),
        stroke_width=3,
    )
    curve_right = axes.plot(
        f,
        x_range=[a + 0.04, 3.45],
        color=theme_color(theme, "secondary"),
        stroke_width=3,
    )

    # Function label, placed in the upper-left wedge between the curve and the
    # L-epsilon line. This is close enough to the curve that the eye reads the
    # label as "this is the curve's name", but high enough above the rising
    # curve that the label's horizontal box does not cross the curve at any x
    # in the label's footprint. (At label_x = 1.5 the curve is at y = 2.83;
    # the label centre at y = 5.5 leaves ~0.7 chart-y clearance even at the
    # right edge of the label where the curve has risen to y = 4.59.)
    f_label = MathTex(
        "f(x) = 2^{x}",
        color=theme_color(theme, "secondary"),
        font_size=float(theme["typography"]["small_size"]),
    )
    f_label.move_to(axes.c2p(1.5, 5.5))

    # The limit value (a, L). Drawn solid because this f is continuous at a (f(a) = L);
    # a hollow circle would falsely suggest f(a) is undefined or differs from L.
    L_dot = Dot(
        axes.c2p(a, L),
        color=theme_color(theme, "muted_text"),
        radius=0.09,
    )
    L_label = MathTex(
        "L",
        color=theme_color(theme, "muted_text"),
        font_size=float(theme["typography"]["body_size"]),
    )
    L_label.next_to(axes.c2p(0, L), LEFT, buff=0.15)

    # Epsilon band (two horizontal dashed lines bounding y = L plus or minus epsilon).
    eps_top = DashedLine(
        axes.c2p(0, L + epsilon),
        axes.c2p(3.8, L + epsilon),
        color=theme_color(theme, "warning"),
        stroke_width=2,
    )
    eps_bot = DashedLine(
        axes.c2p(0, L - epsilon),
        axes.c2p(3.8, L - epsilon),
        color=theme_color(theme, "warning"),
        stroke_width=2,
    )
    eps_top_label = MathTex(
        r"L + \varepsilon",
        color=theme_color(theme, "warning"),
        font_size=float(theme["typography"]["small_size"]),
    )
    eps_top_label.next_to(axes.c2p(0, L + epsilon), LEFT, buff=0.15)
    eps_bot_label = MathTex(
        r"L - \varepsilon",
        color=theme_color(theme, "warning"),
        font_size=float(theme["typography"]["small_size"]),
    )
    eps_bot_label.next_to(axes.c2p(0, L - epsilon), LEFT, buff=0.15)

    # Delta strip (two vertical dashed lines bounding x = a plus or minus delta).
    delta_left = DashedLine(
        axes.c2p(a - delta, 0),
        axes.c2p(a - delta, 13.5),
        color=theme_color(theme, "accent"),
        stroke_width=2,
    )
    delta_right = DashedLine(
        axes.c2p(a + delta, 0),
        axes.c2p(a + delta, 13.5),
        color=theme_color(theme, "accent"),
        stroke_width=2,
    )
    a_label = MathTex(
        "a",
        color=theme_color(theme, "muted_text"),
        font_size=float(theme["typography"]["small_size"]),
    )
    a_label.next_to(axes.c2p(a, 0), DOWN, buff=0.15)
    delta_left_label = MathTex(
        r"a - \delta",
        color=theme_color(theme, "accent"),
        font_size=float(theme["typography"]["small_size"]),
    )
    delta_left_label.next_to(axes.c2p(a - delta, 0), DOWN, buff=0.15)
    delta_right_label = MathTex(
        r"a + \delta",
        color=theme_color(theme, "accent"),
        font_size=float(theme["typography"]["small_size"]),
    )
    delta_right_label.next_to(axes.c2p(a + delta, 0), DOWN, buff=0.15)

    # Box-corner dots at (a-delta, L-epsilon) and (a+delta, L+epsilon).
    # On a convex f the curve passes visibly above the lower corner and below
    # the upper corner -- that is the "graph stays inside the box" message.
    # See the docstring for why these corners cannot also lie on the curve.
    boundary_dots = VGroup(
        Dot(
            axes.c2p(a - delta, L - epsilon),
            color=theme_color(theme, "accent"),
            radius=0.06,
        ),
        Dot(
            axes.c2p(a + delta, L + epsilon),
            color=theme_color(theme, "accent"),
            radius=0.06,
        ),
    )

    caption = Tex(
        r"\parbox{12cm}{\centering The graph over the $\delta$-strip lies inside the $\varepsilon$-band.}",
        color=theme_color(theme, "muted_text"),
        font_size=float(theme["typography"]["small_size"]),
    )
    caption.next_to(axes, DOWN, buff=1.0)

    # Animation sequence aligned with the voiceover beats.
    scene.play(FadeIn(title, shift=0.12 * DOWN), run_time=0.4)
    scene.play(Create(axes), run_time=0.6)
    scene.play(Create(curve_left), Create(curve_right), run_time=1.0)
    scene.play(Write(f_label), run_time=0.4)
    scene.play(FadeIn(L_dot), Write(L_label), run_time=0.4)
    scene.play(
        Create(eps_top),
        Create(eps_bot),
        Write(eps_top_label),
        Write(eps_bot_label),
        run_time=0.7,
    )
    scene.wait(0.2)
    scene.play(
        Create(delta_left),
        Create(delta_right),
        Write(a_label),
        Write(delta_left_label),
        Write(delta_right_label),
        run_time=0.7,
    )
    scene.play(FadeIn(boundary_dots), run_time=0.3)
    scene.play(FadeIn(caption, shift=0.05 * UP), run_time=0.4)

    scene.wait(float(theme["transitions"]["section_pause"]))

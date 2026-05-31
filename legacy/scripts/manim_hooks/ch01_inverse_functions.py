"""Custom hooks for Chapter 1 inverse-functions scenes."""

from __future__ import annotations

from manim import (
    Axes,
    Create,
    DashedLine,
    Dot,
    DOWN,
    FadeIn,
    LEFT,
    Line,
    MathTex,
    RIGHT,
    Tex,
    UP,
    VGroup,
    Write,
)

from manim_templates.helpers import theme_color


def horizontal_line_test_comparison(
    scene, scene_spec: dict[str, object], context: dict[str, object]
) -> None:
    """Side-by-side comparison: one-to-one vs non-one-to-one."""
    theme = context["theme"]
    scene.clear()

    title = Tex(
        rf"\textbf{{{scene_spec['title']}}}",
        color=theme_color(theme, "primary"),
        font_size=float(theme["typography"]["title_size"]),
    )
    title.to_edge(UP, buff=0.4)

    subtitle = Tex(
        r"\parbox{11cm}{\centering One side passes the test; the other fails"
        r" because one output comes from two inputs.}",
        color=theme_color(theme, "muted_text"),
        font_size=float(theme["typography"]["small_size"]),
    )
    subtitle.next_to(title, DOWN, buff=0.3)

    axis_config = {"color": theme_color(theme, "grid"), "stroke_width": 1.5}
    left_axes = Axes(
        x_range=[-2, 2, 1],
        y_range=[-2, 2, 1],
        x_length=4.5,
        y_length=3.8,
        axis_config=axis_config,
    )
    right_axes = Axes(
        x_range=[-2, 2, 1],
        y_range=[-0.5, 3, 1],
        x_length=4.5,
        y_length=3.8,
        axis_config=axis_config,
    )
    pair = VGroup(left_axes, right_axes).arrange(RIGHT, buff=1.2)
    pair.next_to(subtitle, DOWN, buff=0.5)

    left_graph = Line(
        left_axes.c2p(-1.35, -1.35),
        left_axes.c2p(1.3, 1.3),
        color=theme_color(theme, "secondary"),
        stroke_width=3,
    )
    left_hline = DashedLine(
        left_axes.c2p(-1.9, 1.0),
        left_axes.c2p(1.3, 1.0),
        color=theme_color(theme, "warning"),
        stroke_width=2,
    )
    left_dot = Dot(left_axes.c2p(1.0, 1.0), color=theme_color(theme, "success"), radius=0.08)
    # Function label: upper-left of left chart, above the line, far from the
    # dashed y=1 line and the success-coloured caption below.
    left_func_label = MathTex(
        "f(x) = x",
        color=theme_color(theme, "secondary"),
        font_size=float(theme["typography"]["small_size"]),
    )
    left_func_label.move_to(left_axes.c2p(-1.3, 1.6))
    left_label = Tex(
        "One intersection",
        color=theme_color(theme, "success"),
        font_size=float(theme["typography"]["small_size"]),
    )
    left_label.next_to(left_axes, DOWN, buff=0.25)

    right_graph = right_axes.plot(
        lambda x: x * x,
        x_range=[-1.55, 1.55],
        color=theme_color(theme, "secondary"),
        stroke_width=3,
    )
    right_hline = DashedLine(
        right_axes.c2p(-1.8, 1.25),
        right_axes.c2p(1.8, 1.25),
        color=theme_color(theme, "warning"),
        stroke_width=2,
    )
    # Intersection dots solve x^2 = 1.25, i.e. x = +/- sqrt(1.25) ~ +/- 1.118.
    right_dots = VGroup(
        Dot(right_axes.c2p(-1.118, 1.25), color=theme_color(theme, "warning"), radius=0.08),
        Dot(right_axes.c2p(1.118, 1.25), color=theme_color(theme, "warning"), radius=0.08),
    )
    # Function label: upper-centre, above the dashed y=1.25 line and well clear
    # of the parabola's arms (parabola at x=+/-0.6 is y=0.36, so a label at
    # y=2.7 with half-width <= 0.6 chart-x is safely above the curve).
    right_func_label = MathTex(
        "f(x) = x^{2}",
        color=theme_color(theme, "secondary"),
        font_size=float(theme["typography"]["small_size"]),
    )
    right_func_label.move_to(right_axes.c2p(0.0, 2.7))
    right_label = Tex(
        "Two intersections --- not invertible",
        color=theme_color(theme, "warning"),
        font_size=float(theme["typography"]["small_size"]),
    )
    right_label.next_to(right_axes, DOWN, buff=0.25)

    scene.play(FadeIn(title, shift=0.12 * DOWN), run_time=0.5)
    scene.play(FadeIn(subtitle, shift=0.08 * UP), run_time=0.4)
    scene.play(Create(left_axes), Create(right_axes), run_time=0.7)

    scene.play(Create(left_graph), run_time=0.6)
    scene.play(Write(left_func_label), run_time=0.3)
    scene.play(FadeIn(left_hline, shift=0.05 * UP), run_time=0.3)
    scene.play(FadeIn(left_dot), run_time=0.2)
    scene.play(FadeIn(left_label, shift=0.06 * UP), run_time=0.3)

    scene.wait(0.2)

    scene.play(Create(right_graph), run_time=0.7)
    scene.play(Write(right_func_label), run_time=0.3)
    scene.play(FadeIn(right_hline, shift=0.05 * UP), run_time=0.3)
    scene.play(FadeIn(right_dots), run_time=0.2)
    scene.play(FadeIn(right_label, shift=0.06 * UP), run_time=0.3)

    scene.wait(float(theme["transitions"]["section_pause"]))

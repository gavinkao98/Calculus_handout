"""Visual components for the improved storyboard template system.

These replace the single ``make_card`` approach with content-type-specific
visual elements: accent bars, type badges, timeline dots, highlight boxes,
progress indicators, and callout labels.
"""

from __future__ import annotations

from typing import Any

from manim import (
    Circle,
    Dot,
    DOWN,
    LEFT,
    Line,
    MathTex,
    Rectangle,
    RIGHT,
    RoundedRectangle,
    SurroundingRectangle,
    Tex,
    UP,
    VGroup,
)

from .helpers import parbox_tex, theme_color


# -- content-type visual markers -----------------------------------------

def make_accent_bar(height: float, theme: dict[str, Any], color_name: str = "secondary") -> Rectangle:
    """Create a thin vertical accent bar for definition/theorem scenes."""
    return Rectangle(
        width=0.07,
        height=height,
        fill_color=theme_color(theme, color_name),
        fill_opacity=1.0,
        stroke_width=0,
    )


def make_type_badge(label: str, theme: dict[str, Any], color_name: str = "secondary") -> VGroup:
    """Create a small label badge like 'DEFINITION' or 'THEOREM'.

    Uses small-caps styling with a subtle rounded background pill.
    """
    font_size = float(theme["typography"].get("section_label_size", 18))
    text = Tex(
        rf"\textsc{{{label}}}",
        color="white",
        font_size=font_size,
    )
    pill = RoundedRectangle(
        corner_radius=0.1,
        width=text.width + 0.3,
        height=text.height + 0.18,
        stroke_width=0,
        fill_color=theme_color(theme, color_name),
        fill_opacity=1,
    )
    text.move_to(pill.get_center())
    return VGroup(pill, text)


def make_numbered_badge(number: int | str, theme: dict[str, Any], color_name: str = "warning") -> VGroup:
    """Create a filled circle with a number/label inside (e.g. 'Ex 1', '1')."""
    font_size = float(theme["typography"].get("section_label_size", 18))
    label = Tex(
        rf"\textbf{{{number}}}",
        color="white",
        font_size=font_size,
    )
    circle = Circle(
        radius=max(label.width, label.height) / 2 + 0.14,
        fill_color=theme_color(theme, color_name),
        fill_opacity=1,
        stroke_width=0,
    )
    label.move_to(circle.get_center())
    return VGroup(circle, label)


# -- timeline elements ---------------------------------------------------

def make_timeline_dot(theme: dict[str, Any], color_name: str = "secondary") -> Dot:
    """Small filled dot for the example walkthrough vertical timeline."""
    return Dot(
        radius=0.07,
        color=theme_color(theme, color_name),
    )


def make_timeline_connector(dot_a: Dot, dot_b: Dot, theme: dict[str, Any]) -> Line:
    """Vertical line connecting two timeline dots."""
    return Line(
        dot_a.get_center(),
        dot_b.get_center(),
        color=theme_color(theme, "grid"),
        stroke_width=2,
    )


# -- highlight / emphasis -------------------------------------------------

def make_highlight_box(mobject, theme: dict[str, Any]) -> SurroundingRectangle:
    """Create a pale yellow background rectangle around *mobject* to draw attention."""
    return SurroundingRectangle(
        mobject,
        color=theme_color(theme, "highlight") if "highlight" in theme.get("colors", {}) else "#FEF3C7",
        fill_color=theme_color(theme, "highlight") if "highlight" in theme.get("colors", {}) else "#FEF3C7",
        fill_opacity=0.35,
        stroke_width=0,
        buff=0.12,
        corner_radius=0.08,
    )


# -- progress indicator ---------------------------------------------------

def make_progress_dots(current: int, total: int, theme: dict[str, Any]) -> VGroup:
    """Row of dots showing which scene out of *total* is currently active.

    - Past scenes: small filled dots (muted_text colour).
    - Current scene: slightly larger filled dot (accent colour).
    - Future scenes: small outlined dots (grid colour).
    """
    dots = []
    for i in range(1, total + 1):
        if i < current:
            dot = Dot(radius=0.04, color=theme_color(theme, "muted_text"))
        elif i == current:
            dot = Dot(radius=0.06, color=theme_color(theme, "accent"))
        else:
            dot = Dot(radius=0.04, color=theme_color(theme, "grid"))
            dot.set_fill(opacity=0)
            dot.set_stroke(color=theme_color(theme, "grid"), width=1)
        dots.append(dot)
    return VGroup(*dots).arrange(RIGHT, buff=0.12)


# -- callout labels for graphs -------------------------------------------

def make_callout_label(
    text: str,
    theme: dict[str, Any],
    *,
    color_name: str = "text",
    width_cm: float = 4.0,
) -> VGroup:
    """Small annotation label for positioning near graph features.

    Returns a VGroup of (background_rect, text_label) so it can be
    placed with ``.next_to(graph_feature, direction)``.
    """
    font_size = float(theme["typography"].get("caption_size", 20))
    label = Tex(
        parbox_tex(text, width_cm),
        color=theme_color(theme, color_name),
        font_size=font_size,
    )
    bg = RoundedRectangle(
        corner_radius=0.08,
        width=label.width + 0.2,
        height=label.height + 0.14,
        stroke_color=theme_color(theme, "grid"),
        stroke_width=0.8,
        fill_color=theme_color(theme, "surface"),
        fill_opacity=0.92,
    )
    label.move_to(bg.get_center())
    return VGroup(bg, label)


# -- divider line ---------------------------------------------------------

def make_divider_line(width: float, theme: dict[str, Any]) -> Line:
    """Horizontal thin line for separating content sections."""
    color = theme_color(theme, "divider") if "divider" in theme.get("colors", {}) else "#E2E8F0"
    return Line(
        LEFT * width / 2,
        RIGHT * width / 2,
        color=color,
        stroke_width=1.0,
    )

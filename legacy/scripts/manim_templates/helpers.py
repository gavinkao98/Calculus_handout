from __future__ import annotations

from typing import Any

from manim import DOWN, FadeIn, LaggedStart, LEFT, MathTex, RoundedRectangle, Tex, UP, VGroup

from manim_storyboard_workflow import to_mathtex_body, to_tex_text


def theme_color(theme: dict[str, Any], name: str) -> str:
    return str(theme["colors"][name])


def parbox_tex(text: str, width_cm: float) -> str:
    return rf"\parbox{{{width_cm:.2f}cm}}{{{to_tex_text(text)}}}"


def make_title(title: str, theme: dict[str, Any], width_cm: float | None = None) -> Tex:
    layout = theme["layout"]
    typography = theme["typography"]
    width = width_cm or float(layout["content_width"])
    title_tex = Tex(
        parbox_tex(rf"\raggedright \textbf{{{title}}}", width),
        color=theme_color(theme, "primary"),
        font_size=float(typography["title_size"]),
    )
    title_tex.to_edge(UP, buff=0.45)
    return title_tex


def make_bullet_list(
    items: list[str],
    theme: dict[str, Any],
    *,
    width_cm: float,
    numbered: bool = False,
    align_buff: float = 0.28,
) -> VGroup:
    typography = theme["typography"]
    rendered = []
    for index, text in enumerate(items, start=1):
        prefix = rf"\textbf{{{index}.}}" if numbered else r"\textbullet"
        bullet = Tex(
            parbox_tex(f"{prefix} {text}", width_cm),
            color=theme_color(theme, "text"),
            font_size=float(typography["body_size"]),
        )
        rendered.append(bullet)
    group = VGroup(*rendered).arrange(DOWN, aligned_edge=LEFT, buff=align_buff)
    return group


def make_math_stack(lines: list[str], theme: dict[str, Any], *, max_width: float = 5.6) -> VGroup:
    typography = theme["typography"]
    rendered = []
    for line in lines:
        math = MathTex(
            to_mathtex_body(line),
            color=theme_color(theme, "math"),
            font_size=float(typography["math_size"]),
        )
        if math.width > max_width:
            math.scale_to_fit_width(max_width)
        rendered.append(math)
    return VGroup(*rendered).arrange(DOWN, aligned_edge=LEFT, buff=0.34)


def make_card(content, theme: dict[str, Any], *, corner_radius: float = 0.18, buff: float = 0.22) -> VGroup:
    card = RoundedRectangle(
        corner_radius=corner_radius,
        width=content.width + 2 * buff,
        height=content.height + 2 * buff,
        stroke_color=theme_color(theme, "grid"),
        stroke_width=1.2,
        fill_color=theme_color(theme, "surface"),
        fill_opacity=0.96,
    )
    content.move_to(card.get_center())
    return VGroup(card, content)


def make_chip(text: str, theme: dict[str, Any], *, color_name: str = "accent", width_cm: float = 3.8) -> VGroup:
    label = Tex(
        parbox_tex(rf"\centering {text}", width_cm),
        color="white",
        font_size=float(theme["typography"]["small_size"]),
    )
    chip = RoundedRectangle(
        corner_radius=0.16,
        width=label.width + 0.4,
        height=label.height + 0.28,
        stroke_width=0,
        fill_color=theme_color(theme, color_name),
        fill_opacity=1,
    )
    label.move_to(chip.get_center())
    return VGroup(chip, label)


def fade_in_group(scene, items: list, *, lag_ratio: float, shift=None, run_time: float = 0.9) -> None:
    if not items:
        return
    animations = [FadeIn(item, shift=shift) for item in items]
    scene.play(LaggedStart(*animations, lag_ratio=lag_ratio), run_time=run_time)

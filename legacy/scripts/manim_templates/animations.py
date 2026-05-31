"""Animation utilities for the improved storyboard template system.

Provides wrappers around Manim animation primitives that give
math-education-specific behaviour: writing equations, progressive
reveal of grouped elements, scene exits, and curve tracing.
"""

from __future__ import annotations

from typing import Any

from manim import (
    Create,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    GrowFromEdge,
    LaggedStart,
    Write,
    DOWN,
    RIGHT,
    UP,
)


def write_math(scene, mobject, *, run_time: float | None = None, theme: dict[str, Any] | None = None) -> None:
    """Animate a MathTex/Tex object with Write (glyph tracing).

    Falls back to a shorter FadeIn for very wide expressions that
    would look sluggish with full Write tracing.
    """
    default_speed = 0.7
    if theme is not None:
        default_speed = float(theme["transitions"].get("write_speed", 0.7))
    rt = run_time or default_speed

    # Very wide expressions look better with FadeIn
    if mobject.width > 8.0:
        scene.play(FadeIn(mobject, shift=0.1 * UP), run_time=rt)
    else:
        scene.play(Write(mobject), run_time=rt)


def fade_in_element(scene, mobject, *, shift=None, run_time: float = 0.45) -> None:
    """Simple FadeIn with an optional directional shift."""
    if shift is None:
        shift = 0.12 * RIGHT
    scene.play(FadeIn(mobject, shift=shift), run_time=run_time)


def grow_from_edge_down(scene, mobject, *, run_time: float = 0.35) -> None:
    """Grow a mobject downward from its top edge (accent bars)."""
    scene.play(GrowFromEdge(mobject, UP), run_time=run_time)


def grow_from_center(scene, mobject, *, run_time: float = 0.25) -> None:
    """Scale a mobject from centre (badges, dots)."""
    scene.play(GrowFromCenter(mobject), run_time=run_time)


def create_plot(scene, graph, *, run_time: float = 0.8) -> None:
    """Trace out a graph/curve from left to right using Create."""
    scene.play(Create(graph), run_time=run_time)


def fade_in_group(scene, items: list, *, lag_ratio: float = 0.2, shift=None, run_time: float = 0.9) -> None:
    """Staggered FadeIn for a list of mobjects."""
    if not items:
        return
    if shift is None:
        shift = 0.1 * RIGHT
    animations = [FadeIn(item, shift=shift) for item in items]
    scene.play(LaggedStart(*animations, lag_ratio=lag_ratio), run_time=run_time)


def scene_exit(scene, style: str = "fade", *, run_time: float | None = None, theme: dict[str, Any] | None = None) -> None:
    """Perform a clean exit animation at the end of a scene.

    *style* is one of:
    - ``"fade"`` (default): FadeOut all mobjects.
    - ``"hold"``: keep everything on screen (just wait).
    - ``"none"``: do nothing.
    """
    if style == "none":
        return
    if style == "hold":
        pause = 0.45
        if theme is not None:
            pause = float(theme["transitions"].get("section_pause", 0.45))
        scene.wait(pause)
        return

    # "fade" (default)
    rt = run_time
    if rt is None and theme is not None:
        rt = float(theme["transitions"].get("exit_fade", 0.4))
    if rt is None:
        rt = 0.4
    if scene.mobjects:
        scene.play(FadeOut(*scene.mobjects), run_time=rt)


def reveal_groups(scene, groups: list[dict[str, Any]], built_elements: dict[str, Any]) -> None:
    """Progressively reveal named element groups with pauses.

    *groups* is a list of dicts like::

        [
            {"elements": ["statement"], "pause_after": 2.0},
            {"elements": ["math_line_0", "math_line_1"], "pause_after": 1.5},
        ]

    *built_elements* maps element names to ``(mobject, animation_fn)``
    tuples.  ``animation_fn`` is called as ``animation_fn(scene, mobject)``
    and should play the appropriate animation.  If the name is missing
    from *built_elements* it is silently skipped.
    """
    for group in groups:
        for name in group.get("elements", []):
            entry = built_elements.get(name)
            if entry is None:
                continue
            mob, anim_fn = entry
            anim_fn(scene, mob)
        pause = float(group.get("pause_after", 0.3))
        if pause > 0:
            scene.wait(pause)

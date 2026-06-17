"""Block layer -- the unit the reveal mechanism operates on.

Heart of the "B" architecture (unchanged across the visual redesign): templates
only assemble and position a list of Block objects and mark each static vs
dynamic; the one player (scene.py) reveals them uniformly.

  static=True   -> shown at scene start (grid, eyebrow, title, axes)
  static=False  -> revealed when narration reaches {show <id>}

Visual primitives live in brand.py; this module carries the Block container, the
accent-role mapping, and the single reveal code path.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from manim import Create, FadeIn, Flash, GrowFromCenter, Indicate, RIGHT, UP, Write

from .visuals import theme as T


@dataclass
class Block:
    id: str
    mobject: Any
    # A string picks a stock reveal below; a CALLABLE is a custom hook
    # animation: anim(scene, mobject, ground) -> seconds consumed. Hook
    # factories (video/animations/, wired via the scene's `hook:` field)
    # use this to choreograph bespoke manim while keeping the audio-driven
    # beat alignment -- play_block just reports what the animation spent.
    anim: Any = "write"      # write|fade|create|grow|slide|highlight|flash_in|write_glow|slide_pop|callable
    static: bool = False
    # Overlap-guard scope (sizecheck._overlap_issues): only "content" blocks are
    # tested for screen-space collision against each other. "graph" = axes-space
    # geometry whose coincidence is intentional (point on a curve, guide through
    # an intersection, label hugging its curve); "decoration" = motif / column
    # rules / reference guides that deliberately sit beside content; "background"
    # = a full card behind content. The last three are exempt from the check.
    layer: str = "content"   # content|graph|decoration|background


ACCENT_ROLE = {
    "definition": "secondary",   # cyan
    "theorem": "accent",         # gold
    "proposition": "secondary",
    "example": "math",           # electric blue
    "warning": "warning",        # coral
    "procedure": "primary",
    "recap": "secondary",
}


def accent_role(spec: dict[str, Any]) -> str:
    return ACCENT_ROLE.get(spec.get("accent", "definition"), "secondary")


def play_block(scene, block: Block, ground: str) -> float:
    """The single reveal code path. *ground* selects the palette for emphasis.

    Returns the wall-clock animation time consumed, so the caller can subtract it
    from a beat's target duration and hold for exactly the remainder (keeping each
    beat's video length equal to its narration clip).
    """
    mob = block.mobject
    anim = block.anim
    accent = T.color(ground, "accent")

    if callable(anim):
        return float(anim(scene, mob, ground) or 0.0)

    if anim == "fade":
        scene.play(FadeIn(mob, shift=0.1 * UP), run_time=0.5)
        return 0.5
    elif anim == "create":
        scene.play(Create(mob), run_time=0.8)
        return 0.8
    elif anim == "grow":
        scene.play(GrowFromCenter(mob), run_time=0.45)
        return 0.45
    elif anim == "slide":
        scene.play(FadeIn(mob, shift=0.35 * RIGHT), run_time=0.5)
        return 0.5
    elif anim == "highlight":
        scene.play(Write(mob), run_time=0.7)
        return 0.7
    elif anim == "flash_in":
        scene.play(FadeIn(mob, scale=1.05), run_time=0.5)
        scene.play(Flash(mob.get_center(), color=accent, line_length=0.25,
                         num_lines=14, flash_radius=0.6), run_time=0.6)
        return 1.1
    elif anim == "write_glow":
        scene.play(Write(mob), run_time=0.8)
        scene.play(Flash(mob.get_center(), color=accent, line_length=0.3, num_lines=16,
                         flash_radius=max(getattr(mob, "width", 1.0) * 0.55, 0.6)), run_time=0.6)
        return 1.4
    elif anim == "slide_pop":
        scene.play(FadeIn(mob, shift=0.4 * RIGHT), run_time=0.45)
        scene.play(Indicate(mob, color=accent, scale_factor=1.06), run_time=0.4)
        return 0.85
    else:  # "write"
        if getattr(mob, "width", 0) > 9.0:
            scene.play(FadeIn(mob, shift=0.1 * UP), run_time=0.6)
            return 0.6
        scene.play(Write(mob), run_time=0.7)
        return 0.7

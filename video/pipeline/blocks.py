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

from manim import Create, FadeIn, RIGHT, UP, Write

from . import timing as TM
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
    # Nominal seconds for a CALLABLE anim. A hook's cost is invisible to
    # timing.stock_animation_seconds (it can only read the stock table), so make.py's
    # short-beat warning silently skips callables; a template that knows how long its
    # custom animation runs declares it here and the warning keeps working.
    anim_seconds: float | None = None
    static: bool = False
    # Overlap-guard scope (sizecheck._overlap_issues): only "content" blocks are
    # tested for screen-space collision against each other. "graph" = axes-space
    # geometry whose coincidence is intentional (point on a curve, guide through
    # an intersection, label hugging its curve); "decoration" = motif / column
    # rules / reference guides that deliberately sit beside content; "background"
    # = a full card behind content. The last three are exempt from the check.
    layer: str = "content"   # content|graph|decoration|background
    # Opening-frame rewind for a DYNAMIC block that is on screen from t=0 in a state
    # other than the one it was built in: scene.py calls pre_play(mobject) and then adds
    # the mobject before the lead wait. The one user is `carry: to: {corner, scale}`
    # (templates._apply_carry): the copy is BUILT at its corner so the layout gates
    # measure the frame the scene ends on, and pre_play restores it to where the previous
    # scene left it; the reveal then flies it to the corner. None for every other block.
    pre_play: Any = None


# Direction D: 4 semantic accents. The role names map (via theme aliases) to hues:
# secondary->blue, accent->amber, warning->red, success->green.
# 2026-09-12 Direction B ("對位"): the semantic axis is now the handout's own
# (handout/latex/template/calcbook.sty), so a concept carries the same hue in the PDF and
# on screen. The targets are the semantic role keys in theme.DARK / theme.LIGHT.
# What moved: definition was blue and theorem amber -- i.e. SWAPPED relative to the
# handout, which says definition=ochre and theorem=blue. caution / remark / note also
# stop sharing their colours with unrelated families.
ACCENT_ROLE = {
    "definition":  "concept",    # ochre  -- calcbook aConcept
    "theorem":     "result",     # blue   -- calcbook aResult
    "proposition": "result",
    "corollary":   "result",
    "proof":       "result",
    "recap":       "result",     # a recap restates results
    # A derivation is the handout's PLAIN BODY -- calcbook.sty:96 calls aResult the
    # "主色", the colour the running text's kickers, rules and bullets already carry, and a
    # derivation's payoff row is a result even though no environment wraps it. Added
    # 2026-09-13 for the §3.1 accent review: that section contains no `envdefinition` at
    # all (the first one is in §3.2), so its 7 `accent: definition` scenes were all
    # mis-tagged -- a leftover from when `definition` WAS the neutral blue.
    "derivation":  "result",
    "example":     "practice",   # green  -- calcbook aPractice
    "solution":    "practice",
    "procedure":   "strategy",   # violet -- calcbook aStrategy
    "strategy":    "strategy",
    "caution":     "caution",    # red    -- calcbook aCaution
    "warning":     "caution",
    "remark":      "aside",      # slate  -- calcbook aAside
    "note":        "aside",
}

# An unmarked (or unrecognised) scene gets NEUTRAL furniture, not a semantic claim. It
# used to fall back to blue via `accent="definition"`, which was harmless while definition
# WAS the neutral blue; definition is now a marked ochre, so inheriting it would assert a
# semantics the author never wrote. This is a resolved palette role, not an accent value.
DEFAULT_ROLE = "aside"


def accent_role(spec: dict[str, Any]) -> str:
    return ACCENT_ROLE.get(spec.get("accent"), DEFAULT_ROLE)


def play_block(scene, block: Block, ground: str) -> float:
    """The single reveal code path. *ground* selects the palette for emphasis.

    Returns the wall-clock animation time consumed, so the caller can subtract it
    from a beat's target duration and hold for exactly the remainder (keeping each
    beat's video length equal to its narration clip).

    MEASURED, not summed: `_reveal` below returns each path's NOMINAL seconds (the stock
    table's constants; whatever a callable reports), and manim rounds every `play` up to a
    whole frame, so a reveal made of several plays costs more than its nominal. Measuring
    here makes all three paths -- stock name, paced walk, hook callable -- honest in one
    place instead of asking each of them to do it (DESIGN.md, "Reveal 的耗時回報契約").
    The §3.1 hooks measure themselves too; that is harmless, since the outer measurement
    spans exactly the same interval and therefore returns the same number.
    """
    t0 = TM.elapsed(scene)
    return TM.spent(scene, t0, _reveal(scene, block, ground))


def _reveal(scene, block: Block, ground: str) -> float:
    """Play one block's reveal; returns its NOMINAL seconds (see `play_block`)."""
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
        # Direction D: entrances are fades/writes, never bounces. (Was GrowFromCenter.)
        scene.play(FadeIn(mob, shift=0.1 * UP), run_time=0.45)
        return 0.45
    elif anim == "slide":
        scene.play(FadeIn(mob, shift=0.35 * RIGHT), run_time=0.5)
        return 0.5
    elif anim == "highlight":
        scene.play(Write(mob), run_time=0.7)
        return 0.7
    elif anim == "flash_in":
        # was FadeIn + a glow Flash burst; the burst removed project-wide per user
        # request (2026-06-29 -- "no explosion effect"). Kept as a distinct name so
        # callers (theorem_proof qed) need not change; now a plain fade reveal.
        scene.play(FadeIn(mob), run_time=0.5)
        return 0.5
    elif anim == "write_glow":
        # was Write + a glow Flash burst; the burst removed project-wide per user
        # request (2026-06-29). The key/result line keeps its colour + persistent
        # text_glow halo (set in the templates); only the reveal burst is gone.
        scene.play(Write(mob), run_time=0.8)
        return 0.8
    elif anim == "slide_pop":
        # was slide in + a glow Flash burst; the burst removed project-wide per user
        # request (2026-06-29). Now a plain slide-in (no bounce, no flash).
        scene.play(FadeIn(mob, shift=0.4 * RIGHT), run_time=0.45)
        return 0.45
    else:  # "write"
        if getattr(mob, "width", 0) > 9.0:
            scene.play(FadeIn(mob, shift=0.1 * UP), run_time=0.6)
            return 0.6
        scene.play(Write(mob), run_time=0.7)
        return 0.7

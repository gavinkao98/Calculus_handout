"""Template registry.

A template is a function ``build(spec, ctx) -> list[Block]`` that assembles and
positions a scene's content but does NOT animate it -- the player in
``scene.py`` handles reveal. This is the "B" split: declarative templates,
one shared reveal loop.

``content`` scenes pick their template by ``spec["template"]``; ``intro`` /
``outro`` scenes are themselves templates keyed by ``kind`` (defined once,
reused for every section).
"""
from __future__ import annotations

from typing import Any, Callable

from ..blocks import Block
from . import (
    callout,
    definition_math,
    derivation,
    divider,
    graph,
    intro,
    outro,
    procedure_steps,
    recap_cards,
    sign_chart,
    theorem_proof,
    value_table,
)

Builder = Callable[[dict[str, Any], dict[str, Any]], "list[Block]"]

REGISTRY: dict[str, Builder] = {
    "callout": callout.build,
    "definition_math": definition_math.build,
    "derivation": derivation.build,
    "divider": divider.build,
    "graph": graph.build,
    "procedure_steps": procedure_steps.build,
    "sign_chart": sign_chart.build,
    "theorem_proof": theorem_proof.build,
    "recap_cards": recap_cards.build,
    "value_table": value_table.build,
    "intro": intro.build,
    "outro": outro.build,
}


def build_blocks(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    kind = spec.get("kind", "content")
    if kind in ("intro", "outro", "divider"):
        return REGISTRY[kind](spec, ctx)
    template = spec.get("template")
    if template not in REGISTRY:
        raise KeyError(
            f"Scene '{spec.get('id')}' uses unknown template '{template}'. "
            f"Known: {sorted(REGISTRY)}"
        )
    blocks = REGISTRY[template](spec, ctx)
    # Step 2-B2 prototype: prepend the made-visible Lectern spine on dark teaching scenes
    # (drawn UNDER content -- decoration layer). One shared component for every content
    # template; isolate-one-variable A/B. Remove this block to revert to no spine.
    if ctx.get("ground") != "light":
        from ._common import scene_spine
        blocks = [scene_spine(spec, ctx, blocks)] + blocks
    return _apply_hook(spec, ctx, blocks)


def _apply_hook(spec: dict[str, Any], ctx: dict[str, Any], blocks: "list[Block]") -> "list[Block]":
    """Scene-level custom-animation escape hatch (the gen-1 `hook` concept,
    formalised). `hook: "<module>:<fn>"` names a factory importable from the
    video/ root (e.g. "animations.ch01_inverse_functions_hooks:can_we_go_backwards").

    The factory receives the TEMPLATE's blocks and returns the final list --
    it may replace a block's mobject (keeping its reveal id, so storyboard
    {show ...} markers and narration stay untouched), flip static to dynamic,
    or attach a callable anim (see blocks.Block). The template remains the
    no-hook fallback: deleting the `hook:` line restores the stock scene."""
    hook_path = spec.get("hook")
    if not hook_path:
        return blocks
    import importlib

    module_name, _, attr = str(hook_path).partition(":")
    if not attr:
        raise ValueError(
            f"Scene '{spec.get('id')}': hook '{hook_path}' must be '<module>:<function>'."
        )
    fn = getattr(importlib.import_module(module_name), attr)
    return fn(spec, ctx, blocks)

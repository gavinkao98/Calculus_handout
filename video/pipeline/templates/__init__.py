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
    definition_math,
    derivation,
    example_walkthrough,
    graph_focus,
    intro,
    outro,
    procedure_steps,
    recap_cards,
    theorem_proof,
)

Builder = Callable[[dict[str, Any], dict[str, Any]], "list[Block]"]

REGISTRY: dict[str, Builder] = {
    "definition_math": definition_math.build,
    "derivation": derivation.build,
    "example_walkthrough": example_walkthrough.build,
    "graph_focus": graph_focus.build,
    "procedure_steps": procedure_steps.build,
    "theorem_proof": theorem_proof.build,
    "recap_cards": recap_cards.build,
    "intro": intro.build,
    "outro": outro.build,
}


def build_blocks(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    kind = spec.get("kind", "content")
    if kind in ("intro", "outro"):
        return REGISTRY[kind](spec, ctx)
    template = spec.get("template")
    if template not in REGISTRY:
        raise KeyError(
            f"Scene '{spec.get('id')}' uses unknown template '{template}'. "
            f"Known: {sorted(REGISTRY)}"
        )
    return REGISTRY[template](spec, ctx)

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

from manim import DL, DR, UL, UR

from .. import narration
from ..blocks import Block
from ..timing import STOCK_ANIM_SECONDS
from ..visuals import theme as T
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
    # `carry:` (motion primitive 5, object side) runs BEFORE the hook, so a hook can still
    # replace or re-animate the carried block.
    blocks = _apply_carry(spec, ctx, blocks)
    # `paced:` (motion primitive 7) runs AFTER the hook, so a hook that replaces a block's
    # mobject with a multi-part one still gets its parts walked across the beat.
    from .. import pacing
    return pacing.apply(spec, _scaffold_reveal_timing(spec, _apply_hook(spec, ctx, blocks)))


# `carry: to: {corner: ...}` targets (manim corner vectors), buffered to the safe margin.
_CARRY_CORNERS = {"top_left": UL, "top_right": UR, "bottom_left": DL, "bottom_right": DR}


def _apply_carry(spec: dict[str, Any], ctx: dict[str, Any], blocks: "list[Block]") -> "list[Block]":
    """`carry:` -- put a block the previous content scene built into this scene's opening
    frame (SPEC-motion-language rule 1, 一場一張畫布).

        carry:
          - from: sector_inequality   # the content scene right before this one (schema)
            block: plot.0             # a block id THAT scene builds (hook-replaced ones too)
            as: carried.circle        # this scene's id for it; {show carried.circle} may name it
            to: keep                  # keep = static, where it was; or {corner, scale}

    Nothing is serialised between renders: the source scene is REBUILT here (hook and all)
    and the block's mobject copied. Layout is deterministic, so the copy sits exactly where
    the previous scene's last frame left it, and make.py hard-cuts that boundary
    (_segment_fades), so the object simply persists across the cut. The copy is a snapshot
    (updaters cleared): a sweep's always_redraw parts would otherwise keep redrawing from the
    previous scene's tracker at the previous scene's axes.

    A carried scene may itself carry (a chain across an act): `from` must be EARLIER in the
    deck, so the recursion always terminates; each hop rebuilds one more scene, the price of
    not caching mobjects across scenes. One rebuild per source scene, not per entry.

    `to: {corner, scale}`: the copy is BUILT at its terminal place (corner, scaled) so the
    layout gates measure the frame the scene ends on (same reasoning as sweep's tracker);
    Block.pre_play rewinds it to the carried-in position before the scene starts, and the
    reveal at `{show <as>}` flies it there (STOCK_ANIM_SECONDS["carry"]). With no marker
    the flight happens in the end-of-scene sweep-up, like any unrevealed block."""
    entries = spec.get("carry")
    if not entries:
        return blocks
    sid = spec.get("id")
    scenes_by_id = ctx.get("scenes_by_id")
    if scenes_by_id is None:
        raise ValueError(f"Scene '{sid}' declares carry: but ctx has no 'scenes_by_id' -- "
                         f"the caller must pass the whole deck so the carried scene can be built")
    order = list(scenes_by_id)
    ids = {b.id for b in blocks}
    out = list(blocks)
    built: dict[str, list[Block]] = {}
    for j, item in enumerate(entries):
        where = f"{sid}.carry[{j}]"
        src, block_id, as_id = item["from"], item["block"], item["as"]
        if src not in scenes_by_id:
            raise ValueError(f"{where}.from {src!r}: not a scene of this deck")
        if sid not in scenes_by_id or order.index(src) >= order.index(sid):
            raise ValueError(f"{where}.from {src!r}: must be a scene earlier than '{sid}' in the deck")
        if src not in built:
            built[src] = build_blocks(scenes_by_id[src], ctx)
        source = next((b for b in built[src] if b.id == block_id), None)
        if source is None:
            raise ValueError(f"{where}.block {block_id!r}: '{src}' builds no such block "
                             f"(built ids: {sorted(b.id for b in built[src])})")
        if as_id in ids:
            raise ValueError(f"{where}.as {as_id!r}: this scene already builds a block with that id")
        ids.add(as_id)
        mob = source.mobject.copy().clear_updaters()
        to = item.get("to", "keep")
        if to == "keep":
            out.append(Block(as_id, mob, anim="fade", static=True, layer=source.layer))
            continue
        scale = float(to.get("scale", 1.0))
        seconds = STOCK_ANIM_SECONDS["carry"]
        mob.save_state()          # the carried-in state: where the previous scene left it
        mob.scale(scale).to_corner(_CARRY_CORNERS[to["corner"]], buff=T.SAFE_MARGIN)
        target = mob.get_center()

        def flight(scene, m, _ground, *, s=scale, c=target, t=seconds) -> float:
            scene.play(m.animate.scale(s).move_to(c), run_time=t)
            return t

        out.append(Block(as_id, mob, anim=flight, anim_seconds=seconds, static=False,
                         layer=source.layer, pre_play=lambda m: m.restore()))
    return out


def _scaffold_reveal_timing(spec: dict[str, Any], blocks: "list[Block]") -> "list[Block]":
    """Motion primitive 1 (揭示時序) for the scaffold line, centrally for every template.

    `scaffold.motive` / `scaffold.problem` / `scaffold.flag.<id>` are part of the opening
    frame by default -- which means a motive that states the scene's conclusion ("Bank a
    companion limit: (1-cos t)/t -> 0") and an ASSUMES pill are on screen from t=0, up to a
    minute before the narration reaches them (rewatch R2 2026-09-12, D-focus: "最重要的前提
    被提前一分鐘擺出來…pill 因此退化成裝飾"). A scene whose `say` names the block instead has
    it slide in on that beat. Opt-in by marker, so every existing deck is unchanged; the
    LAYOUT is untouched either way (the line always occupies its slot, it only arrives late).
    """
    targets = set(narration.list_reveal_targets(spec.get("say", "")))
    for b in blocks:
        if b.id.startswith("scaffold.") and b.static and b.id in targets:
            b.static = False
            b.anim = "slide"
    return blocks


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

"""Reveal strategies for storyboard scenes.

A reveal strategy decides *when* each visual element of a scene appears in
relation to the narration. Three strategies are supported per
MANIM_VOICEOVER_MIGRATION_PLAN.md §1:

- ``all_at_once``  : every element shown before narration starts.
- ``beat_paced``   : every element waits for a bookmark in the narration.
- ``hybrid``       : static elements shown up front, dynamic elements
                     either wait for bookmarks or are time-sliced evenly
                     across the narration when bookmarks are absent.
- ``hybrid_auto``  : like ``hybrid`` but, in the absence of bookmarks,
                     resolves dynamic-element trigger times by matching
                     anchor tokens against the narration. See ``anchors``
                     and ``latex_speech`` for the heuristics.

Each scene picks its strategy via:

    1. ``scene_spec["reveal_strategy"]`` (explicit), else
    2. ``TEMPLATE_REVEAL_DEFAULTS[template]["strategy"]``.

Static / dynamic element lists are resolved similarly:

    1. ``scene_spec["reveal_static"]`` / ``reveal_dynamic`` (explicit), else
    2. ``TEMPLATE_REVEAL_DEFAULTS[template]["static"]`` /
       ``TEMPLATE_REVEAL_DEFAULTS[template]["dynamic"]``,
       expanded against the actual element ids present in the scene
       (e.g. ``math_lines`` -> ``math_line_0``, ``math_line_1`` ...).
"""
from __future__ import annotations

import re
from typing import Any, Callable, Iterable

RevealFn = Callable[[], float]


# ─── Template defaults ─────────────────────────────────────────────────────
# The lists are *patterns* against the live revealers dict:
#   - exact id  ("title", "header", "statement", "qed")
#   - prefix    ("math_line_*", "step_*", "plot_*")
#   - alias     ("math_lines"   resolves to all "math_line_*")
# Patterns ending in "*" expand to every concrete id matching the prefix.

TEMPLATE_REVEAL_DEFAULTS: dict[str, dict[str, Any]] = {
    "title_bullets": {
        "strategy": "all_at_once",
        "static": ["title", "bullet_*"],
        "dynamic": [],
    },
    "section_transition": {
        "strategy": "all_at_once",
        "static": ["title", "subtitle", "rule", "upcoming_*"],
        "dynamic": [],
    },
    "definition_math": {
        "strategy": "hybrid",
        # supporting_bullets behave like extra statement context — show them
        # together with the statement, dynamic only for the math derivation.
        "static": ["header", "statement", "support_*"],
        "dynamic": ["math_line_*"],
    },
    "theorem_proof": {
        "strategy": "hybrid",
        "static": ["header", "statement", "proof_label"],
        "dynamic": ["proof_step_*", "qed"],
    },
    "example_walkthrough": {
        "strategy": "beat_paced",
        "static": ["header"],
        "dynamic": ["step_*", "math_line_*", "takeaway"],
    },
    "procedure_steps": {
        "strategy": "beat_paced",
        "static": ["header"],
        "dynamic": ["step_*", "equation_*"],
    },
    "graph_focus": {
        "strategy": "hybrid",
        # plots/labels are part of the figure backdrop — they appear with
        # the axes so the narration can reference the picture as a whole.
        # Only annotations (callouts) wait for the narration to mention them.
        "static": ["title", "rule", "axes", "plot_*", "label_*"],
        "dynamic": ["annotation_*"],
    },
    "recap_cards": {
        "strategy": "hybrid",
        "static": ["header", "point_*"],
        "dynamic": ["identity_*"],
    },
    "comparison": {
        "strategy": "hybrid",
        "static": ["title", "rule", "left_label", "right_label"],
        "dynamic": ["left_math_*", "right_math_*"],
    },
}


VALID_STRATEGIES = ("all_at_once", "beat_paced", "hybrid", "hybrid_auto")


# ─── Pattern expansion ─────────────────────────────────────────────────────

def expand_patterns(patterns: Iterable[str], available_ids: Iterable[str]) -> list[str]:
    """Resolve a list of pattern strings against the concrete revealer ids.

    Wildcard patterns ending with ``*`` match any id sharing the prefix
    before the asterisk. Exact patterns must appear in ``available_ids`` to
    be retained (silently dropped otherwise — templates may omit elements).
    """
    resolved: list[str] = []
    seen: set[str] = set()
    available = list(available_ids)

    for pattern in patterns:
        if pattern.endswith("*"):
            prefix = pattern[:-1]
            matches = sorted(
                (eid for eid in available if eid.startswith(prefix)),
                key=lambda e: _natural_sort_key(e),
            )
            for eid in matches:
                if eid not in seen:
                    resolved.append(eid)
                    seen.add(eid)
        else:
            if pattern in available and pattern not in seen:
                resolved.append(pattern)
                seen.add(pattern)
    return resolved


_NATURAL_RE = re.compile(r"(\d+)")


def _natural_sort_key(value: str) -> list:
    return [int(part) if part.isdigit() else part for part in _NATURAL_RE.split(value)]


# ─── Strategy resolution ───────────────────────────────────────────────────

def resolve_strategy_name(spec: dict[str, Any], template: str) -> str:
    explicit = spec.get("reveal_strategy")
    if explicit:
        if explicit not in VALID_STRATEGIES:
            raise ValueError(
                f"Scene '{spec.get('scene_id')}' has invalid reveal_strategy "
                f"'{explicit}'. Valid options: {VALID_STRATEGIES}."
            )
        return explicit
    default = TEMPLATE_REVEAL_DEFAULTS.get(template, {}).get("strategy")
    if not default:
        # Templates we did not enumerate fall back to hybrid — safest choice.
        return "hybrid"
    return default


def resolve_static_dynamic(
    spec: dict[str, Any],
    template: str,
    revealers: dict[str, RevealFn],
) -> tuple[list[str], list[str]]:
    """Return (static_ids, dynamic_ids) for the scene.

    When ``voiceover_beats`` are present, the beat reveal lists define the
    dynamic order verbatim — this lets aliases (``math_lines``) and template
    elements that the default patterns would not match still drive the scene
    timing. Otherwise explicit ``reveal_static`` / ``reveal_dynamic`` on the
    scene override the template default; either accepts wildcard patterns.
    """
    available = list(revealers.keys())
    defaults = TEMPLATE_REVEAL_DEFAULTS.get(template, {})

    if spec.get("voiceover_beats"):
        seen: set[str] = set()
        dynamic_ids: list[str] = []
        for beat in spec["voiceover_beats"]:
            for eid in beat.get("reveal", []) or []:
                if eid not in seen and eid in revealers:
                    dynamic_ids.append(eid)
                    seen.add(eid)
        static_patterns = spec.get("reveal_static") or defaults.get("static") or []
        static_ids = [
            eid
            for eid in expand_patterns(static_patterns, available)
            if eid not in seen
        ]
        return static_ids, dynamic_ids

    static_patterns = spec.get("reveal_static") or defaults.get("static") or []
    dynamic_patterns = spec.get("reveal_dynamic") or defaults.get("dynamic") or []

    static_ids = expand_patterns(static_patterns, available)
    dynamic_ids = expand_patterns(dynamic_patterns, available)

    # An element cannot be both static and dynamic. Static wins so the author
    # can promote a normally-dynamic element to up-front display by listing it
    # in reveal_static.
    static_set = set(static_ids)
    dynamic_ids = [eid for eid in dynamic_ids if eid not in static_set]

    return static_ids, dynamic_ids


# ─── Strategy implementations ──────────────────────────────────────────────

class RevealStrategy:
    name = ""

    def render(
        self,
        scene,
        spec: dict[str, Any],
        ctx: dict[str, Any],
        revealers: dict[str, RevealFn],
        narration: str,
        static_ids: list[str],
        dynamic_ids: list[str],
    ) -> None:
        raise NotImplementedError


def _run_revealers(revealers: dict[str, RevealFn], ids: Iterable[str]) -> float:
    elapsed = 0.0
    seen: set[str] = set()
    for eid in ids:
        if eid in seen:
            continue
        fn = revealers.get(eid)
        if fn is None:
            continue
        elapsed += max(float(fn() or 0.0), 0.0)
        seen.add(eid)
        seen.update(getattr(fn, "_reveals", set()))
    return elapsed


def _lead_in(scene, spec: dict[str, Any]) -> None:
    lead_in = float(spec.get("timing", {}).get("lead_in_seconds", 0.0))
    if lead_in > 0:
        scene.wait(lead_in)


def _hold_after(scene, spec: dict[str, Any]) -> None:
    hold = float(spec.get("timing", {}).get("hold_after_seconds", 0.0))
    if hold > 0:
        scene.wait(hold)


class AllAtOnceStrategy(RevealStrategy):
    name = "all_at_once"

    def render(self, scene, spec, ctx, revealers, narration, static_ids, dynamic_ids):
        all_ids = static_ids + dynamic_ids
        _lead_in(scene, spec)
        _run_revealers(revealers, all_ids)
        if narration:
            with scene.voiceover(text=narration, slide_id=spec["scene_id"]):
                pass  # tracker waits for audio to finish on context exit
        _hold_after(scene, spec)


class BeatPacedStrategy(RevealStrategy):
    name = "beat_paced"

    def render(self, scene, spec, ctx, revealers, narration, static_ids, dynamic_ids):
        _lead_in(scene, spec)
        # Static elements still shown first — beat_paced just means EVERY
        # dynamic element waits for a bookmark.
        _run_revealers(revealers, static_ids)

        if not narration:
            _run_revealers(revealers, dynamic_ids)
            _hold_after(scene, spec)
            return

        bookmarks = _bookmarks_in(narration)
        # No bookmarks at all — without anchors there is no "beat" to pace
        # against, so we fall back to even time-slicing across the audio
        # the same way HybridStrategy does. This keeps beat_paced safe to
        # set as a template default even on storyboards that have not yet
        # adopted bookmarks.
        if not bookmarks and dynamic_ids:
            with scene.voiceover(text=narration, slide_id=spec["scene_id"]) as tracker:
                slots = max(len(dynamic_ids), 1)
                slot_duration = max(tracker.duration / (slots + 1), 0.0)
                for idx, eid in enumerate(dynamic_ids, start=1):
                    target = slot_duration * idx
                    remaining = max(target - (scene.renderer.time - tracker.start_t), 0.0)
                    if remaining > 0:
                        scene.safe_wait(remaining)
                    _run_revealers(revealers, [eid])
            _hold_after(scene, spec)
            return

        with scene.voiceover(text=narration, slide_id=spec["scene_id"]):
            for eid in dynamic_ids:
                if eid in bookmarks:
                    scene.wait_until_bookmark(eid)
                _run_revealers(revealers, [eid])
        _hold_after(scene, spec)
        _hold_after(scene, spec)


class HybridStrategy(RevealStrategy):
    name = "hybrid"

    def render(self, scene, spec, ctx, revealers, narration, static_ids, dynamic_ids):
        _lead_in(scene, spec)
        _run_revealers(revealers, static_ids)
        bookmarks = _bookmarks_in(narration)

        if not narration:
            _run_revealers(revealers, dynamic_ids)
            _hold_after(scene, spec)
            return

        # If no bookmarks at all, time-slice dynamic elements evenly across
        # the audio so the scene does not freeze before the WAV ends.
        if not bookmarks and dynamic_ids:
            with scene.voiceover(text=narration, slide_id=spec["scene_id"]) as tracker:
                slots = max(len(dynamic_ids), 1)
                slot_duration = max(tracker.duration / (slots + 1), 0.0)
                for idx, eid in enumerate(dynamic_ids, start=1):
                    target = slot_duration * idx
                    remaining = max(target - (scene.renderer.time - tracker.start_t), 0.0)
                    if remaining > 0:
                        scene.safe_wait(remaining)
                    _run_revealers(revealers, [eid])
            _hold_after(scene, spec)
            return

        with scene.voiceover(text=narration, slide_id=spec["scene_id"]):
            for eid in dynamic_ids:
                if eid in bookmarks:
                    scene.wait_until_bookmark(eid)
                _run_revealers(revealers, [eid])
        _hold_after(scene, spec)


class HybridAutoStrategy(HybridStrategy):
    """Hybrid + anchor-driven heuristic for dynamic-element placement.

    The anchors module decides where each dynamic element should fire
    inside the narration. This strategy injects synthetic bookmarks at
    those anchor positions before delegating back to the bookmark path.

    Concrete anchor extraction lives in ``anchors.py``; that module is
    queried lazily so this file does not pull anchor extractors when the
    strategy is unused.
    """

    name = "hybrid_auto"

    def render(self, scene, spec, ctx, revealers, narration, static_ids, dynamic_ids):
        from .anchors import inject_auto_bookmarks  # late import; avoids cycles

        bookmarks_present = _bookmarks_in(narration)
        if bookmarks_present:
            # Author already wrote bookmarks — fall through to plain hybrid.
            super().render(scene, spec, ctx, revealers, narration, static_ids, dynamic_ids)
            return

        narration_with_bookmarks, plan = inject_auto_bookmarks(
            narration=narration,
            spec=spec,
            ctx=ctx,
            dynamic_ids=dynamic_ids,
            template=spec["template"],
        )
        # Stash the resolution plan for --explain-reveals.
        ctx.setdefault("auto_reveal_plans", {})[spec["scene_id"]] = plan
        super().render(scene, spec, ctx, revealers, narration_with_bookmarks, static_ids, dynamic_ids)


STRATEGY_REGISTRY: dict[str, type[RevealStrategy]] = {
    "all_at_once": AllAtOnceStrategy,
    "beat_paced": BeatPacedStrategy,
    "hybrid": HybridStrategy,
    "hybrid_auto": HybridAutoStrategy,
}


def get_strategy(name: str) -> RevealStrategy:
    cls = STRATEGY_REGISTRY.get(name)
    if cls is None:
        raise ValueError(f"Unknown reveal strategy '{name}'.")
    return cls()


# ─── Bookmark scanning ─────────────────────────────────────────────────────

_BOOKMARK_RE = re.compile(r"<bookmark\s*mark\s*=['\"](\w+)[\"\']\s*/>")


def _bookmarks_in(text: str) -> set[str]:
    return {match.group(1) for match in _BOOKMARK_RE.finditer(text or "")}

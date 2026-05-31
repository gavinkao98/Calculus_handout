"""Hybrid-auto anchor extraction and bookmark injection.

Given a scene's narration string (no bookmarks) and the list of dynamic
element ids, this module decides where each dynamic element should fire
and rewrites the narration to contain ``<bookmark mark='<id>'/>`` tags at
those positions.

The extraction is template-aware: the ``ANCHOR_EXTRACTORS`` registry maps
``(template, element_kind)`` to a function that, given the scene data and
element index, returns a list of plausible search tokens.
"""
from __future__ import annotations

import re
from typing import Any, Callable

from .latex_speech import (
    find_earliest_match,
    latex_to_speech_tokens,
    ordinal_phrases,
    text_to_anchor_tokens,
)


# ─── Per-template anchor extractors ────────────────────────────────────────

AnchorExtractor = Callable[[dict[str, Any], int], list[str]]


def _math_line_anchors(data: dict[str, Any], idx: int) -> list[str]:
    lines = data.get("math_lines") or []
    if idx >= len(lines):
        return []
    entry = lines[idx]
    text = entry.get("text") if isinstance(entry, dict) else entry
    return latex_to_speech_tokens(text or "")


def _step_anchors(data: dict[str, Any], idx: int) -> list[str]:
    steps = data.get("steps") or []
    if idx >= len(steps):
        return []
    step = steps[idx]
    if isinstance(step, dict):
        text = step.get("text", "")
    else:
        text = str(step)
    tokens = text_to_anchor_tokens(text)
    tokens.extend(ordinal_phrases(idx))
    return tokens


def _equation_anchors(data: dict[str, Any], idx: int) -> list[str]:
    equations = data.get("worked_equations") or []
    if idx >= len(equations):
        return []
    entry = equations[idx]
    if isinstance(entry, dict):
        return latex_to_speech_tokens(entry.get("text", "")) + ordinal_phrases(idx)
    return latex_to_speech_tokens(str(entry)) + ordinal_phrases(idx)


def _takeaway_anchors(data: dict[str, Any], idx: int) -> list[str]:
    text = data.get("takeaway") or ""
    tokens = text_to_anchor_tokens(text)
    tokens = list(tokens) + [
        "takeaway",
        "in summary",
        "to recap",
        "key idea",
        "the upshot",
        "the move",
        "the lesson",
    ]
    return tokens


def _proof_step_anchors(data: dict[str, Any], idx: int) -> list[str]:
    steps = data.get("proof_steps") or []
    if idx >= len(steps):
        return []
    entry = steps[idx]
    if isinstance(entry, dict):
        text = entry.get("text", "")
    else:
        text = str(entry)
    tokens = text_to_anchor_tokens(text)
    tokens.extend(ordinal_phrases(idx))
    return tokens


def _qed_anchors(data: dict[str, Any], idx: int) -> list[str]:
    return ["qed", "complete", "this completes the proof", "we are done"]


def _identity_anchors(data: dict[str, Any], idx: int) -> list[str]:
    identities = data.get("identities") or []
    if idx >= len(identities):
        return []
    entry = identities[idx]
    text = entry.get("text") if isinstance(entry, dict) else entry
    return latex_to_speech_tokens(text or "")


def _plot_anchors(data: dict[str, Any], idx: int) -> list[str]:
    plots = data.get("plots") or []
    if idx >= len(plots):
        return []
    plot = plots[idx]
    tokens: list[str] = []
    label = plot.get("label") if isinstance(plot, dict) else None
    if label:
        # Strip $...$ and the surrounding LaTeX, then add as anchor.
        cleaned = re.sub(r"\$([^$]*)\$", r"\1", label)
        tokens.extend(latex_to_speech_tokens(cleaned))
        tokens.append(cleaned.strip())
    expression = plot.get("expression") if isinstance(plot, dict) else None
    if expression:
        tokens.append(str(expression))
    kind = plot.get("kind") if isinstance(plot, dict) else None
    if kind == "function":
        tokens.append("the curve")
        tokens.append("the graph")
    elif kind == "point":
        tokens.append("the point")
    elif kind == "line":
        tokens.append("the line")
    return tokens


def _annotation_anchors(data: dict[str, Any], idx: int) -> list[str]:
    annotations = data.get("annotations") or []
    if idx >= len(annotations):
        return []
    entry = annotations[idx]
    text = entry.get("text") if isinstance(entry, dict) else entry
    return text_to_anchor_tokens(text or "")


# Element id pattern -> extractor.
ANCHOR_EXTRACTORS: dict[str, AnchorExtractor] = {
    "math_line_": _math_line_anchors,
    "step_": _step_anchors,
    "equation_": _equation_anchors,
    "takeaway": _takeaway_anchors,
    "proof_step_": _proof_step_anchors,
    "qed": _qed_anchors,
    "identity_": _identity_anchors,
    "plot_": _plot_anchors,
    "annotation_": _annotation_anchors,
}


def extract_anchors(element_id: str, data: dict[str, Any]) -> list[str]:
    """Return the anchor token candidates for one dynamic element id."""
    for prefix, extractor in ANCHOR_EXTRACTORS.items():
        if not prefix.endswith("_"):
            if element_id == prefix:
                return extractor(data, 0)
            continue
        if element_id.startswith(prefix):
            tail = element_id[len(prefix) :]
            try:
                idx = int(tail)
            except ValueError:
                continue
            return extractor(data, idx)
    return []


# ─── Bookmark injection ────────────────────────────────────────────────────

def inject_auto_bookmarks(
    *,
    narration: str,
    spec: dict[str, Any],
    ctx: dict[str, Any],
    dynamic_ids: list[str],
    template: str,
) -> tuple[str, dict[str, Any]]:
    """Find anchor positions for each dynamic element and rewrite narration
    to contain bookmarks at those positions.

    Returns ``(narration_with_bookmarks, plan)`` where ``plan`` is a dict
    suitable for inclusion in ``auto_reveal_plan.json``.
    """
    data = spec.get("data") or {}
    matches: list[dict[str, Any]] = []

    cursor = 0  # enforces monotonic ordering
    pending_fallback: list[str] = []

    for element_id in dynamic_ids:
        candidates = extract_anchors(element_id, data)
        if not candidates:
            matches.append({
                "element_id": element_id,
                "anchor_token": None,
                "narration_offset": None,
                "matched": False,
                "reason": "no anchor candidates",
            })
            pending_fallback.append(element_id)
            continue

        offset, token = find_earliest_match(narration, candidates, min_offset=cursor)
        if offset < 0:
            matches.append({
                "element_id": element_id,
                "anchor_token": None,
                "narration_offset": None,
                "matched": False,
                "reason": "no narration match",
            })
            pending_fallback.append(element_id)
            continue

        matches.append({
            "element_id": element_id,
            "anchor_token": token,
            "narration_offset": offset,
            "matched": True,
        })
        cursor = offset + (len(token) if token else 1)

    # Distribute unmatched elements evenly across the narration tail.
    if pending_fallback:
        _assign_fallback_positions(matches, narration, pending_fallback)

    rewritten = _splice_bookmarks(narration, matches)

    plan = {
        "scene_id": spec.get("scene_id"),
        "template": template,
        "dynamic_ids": list(dynamic_ids),
        "matches": matches,
        "fallback_count": sum(1 for m in matches if not m["matched"]),
        "narration_length": len(narration),
    }
    return rewritten, plan


def _assign_fallback_positions(
    matches: list[dict[str, Any]],
    narration: str,
    fallback_ids: list[str],
) -> None:
    matched_offsets = sorted(m["narration_offset"] for m in matches if m["matched"])
    last_anchor = matched_offsets[-1] if matched_offsets else 0
    tail_start = last_anchor
    tail_end = len(narration)
    span = max(tail_end - tail_start, 1)
    slot = span / (len(fallback_ids) + 1)

    by_id = {m["element_id"]: m for m in matches}
    for i, eid in enumerate(fallback_ids, start=1):
        m = by_id[eid]
        m["narration_offset"] = int(tail_start + slot * i)
        m["fallback"] = True


def _splice_bookmarks(narration: str, matches: list[dict[str, Any]]) -> str:
    """Insert each matched bookmark just before its narration_offset.

    Multiple bookmarks at the same offset are emitted in declaration order.
    """
    points = [
        (m["narration_offset"], m["element_id"])
        for m in matches
        if m["narration_offset"] is not None
    ]
    if not points:
        return narration
    # Sort by offset, then by original declaration order (stable sort).
    indexed = list(enumerate(points))
    indexed.sort(key=lambda p: (p[1][0], p[0]))
    pieces: list[str] = []
    last = 0
    for _, (offset, eid) in indexed:
        clamped = max(min(offset, len(narration)), last)
        pieces.append(narration[last:clamped])
        pieces.append(f"<bookmark mark='{eid}'/>")
        last = clamped
    pieces.append(narration[last:])
    return "".join(pieces)

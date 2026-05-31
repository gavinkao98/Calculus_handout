"""Compile a scene's narration into a single bookmark-aware string.

Input shapes a scene may take:

1. ``voiceover_beats`` (list of {id, text, reveal})
   Each reveal element's id becomes a ``<bookmark mark='<id>'/>`` placed at
   the beat boundary so ``wait_until_bookmark`` can fire on it.

2. ``voiceover`` (plain string, possibly already containing bookmarks)
   Used verbatim — the author is in control of bookmark placement.

3. Neither
   Returns an empty string. The caller's reveal strategy must cope (the
   ``hybrid`` strategy time-slices dynamic elements when no narration is
   present; ``all_at_once`` simply skips the voiceover context).

Compiler behaviour notes
------------------------
- Beat-level ``id`` is intentionally NOT emitted as a bookmark by default.
  The beat id is a structural label, not a reveal target. We only emit
  bookmarks for the reveal element ids referenced in each beat's
  ``reveal`` list.
- Multiple reveal ids in the same beat all anchor to the same time point
  (the start of that beat). The reveal strategy will iterate them in the
  beat's declared order, which matches the legacy behaviour of
  ``_run_voiceover_beats``.
- Beats whose ``reveal`` list is empty still emit their text — they may
  carry narration that bridges between visual events.
"""
from __future__ import annotations

import re
from typing import Any


_BOOKMARK_RE = re.compile(r"<bookmark\s*mark\s*=['\"](\w+)[\"\']\s*/>")


def has_bookmarks(text: str) -> bool:
    return bool(_BOOKMARK_RE.search(text or ""))


def list_bookmarks(text: str) -> list[str]:
    return [m.group(1) for m in _BOOKMARK_RE.finditer(text or "")]


def compile_narration(spec: dict[str, Any]) -> str:
    """Return the narration string the reveal strategy should feed into the
    voiceover context. Idempotent: passing already-compiled text through
    again returns the same string.
    """
    beats = spec.get("voiceover_beats")
    if beats:
        return _compile_from_beats(beats)
    return spec.get("voiceover") or ""


def _compile_from_beats(beats: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for beat in beats:
        reveal_ids = beat.get("reveal") or []
        for eid in reveal_ids:
            parts.append(f"<bookmark mark='{eid}'/>")
        text = (beat.get("text") or "").strip()
        if text:
            parts.append(text)
    return " ".join(parts)


def strip_bookmarks(text: str) -> str:
    """Return the narration text with all ``<bookmark .../>`` tags removed."""
    return _BOOKMARK_RE.sub("", text or "").strip()

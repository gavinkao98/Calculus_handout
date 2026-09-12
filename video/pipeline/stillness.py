"""SPEC-motion-language rule 4 -- undeclared stillness.

    Every still stretch longer than 6 s MUST be intentional: either a `pauses:` hold, or
    a beat filled by `paced:` / a sweep / `seconds: beat`. An undeclared long still is a
    defect.

This is the pure judge behind make.py's `[stillness]` advisory (warn-only, never blocks a
render), so an author sees "one reveal, then 18 s of nothing" / "first beat, no reveal,
37.6 s" BEFORE spending a render on it. Manim-free: make.py feeds it the same beat table
and block table `_warn_short_beats` reads.
"""
from __future__ import annotations

from typing import Any, Iterable

UNDECLARED_STILL_SECONDS = 6.0


def undeclared_still_beats(beats: Iterable[dict[str, Any]], anim_seconds: dict[str, float | None],
                           paced: set[str], pauses_after: set[str],
                           threshold: float = UNDECLARED_STILL_SECONDS) -> list[tuple[int, float, Any]]:
    """beats: list of {"index": int, "reveal": str|None, "seconds": float}
    anim_seconds: dict reveal_id -> float|None  (None = callable/paced-by-code, i.e. motion fills the beat)
    paced: set of reveal ids declared in `paced:`
    pauses_after: set of reveal ids that have a `pauses:` entry
    returns list of (index, seconds, reveal) for beats whose screen is still > threshold with nothing declared

    A beat with no reveal (reveal None) is still for its whole length; a reveal missing
    from *anim_seconds* (static / unknown block) animates nothing and counts the same way.
    """
    out: list[tuple[int, float, Any]] = []
    for beat in beats:
        reveal = beat.get("reveal")
        if reveal is not None:
            if reveal in paced or reveal in pauses_after:
                continue
            if reveal in anim_seconds and anim_seconds[reveal] is None:
                continue
        still = float(beat["seconds"]) - float(anim_seconds.get(reveal) or 0.0)
        if still > threshold:
            out.append((int(beat["index"]), still, reveal))
    return out

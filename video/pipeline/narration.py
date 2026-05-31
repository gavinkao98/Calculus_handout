"""Narration compiler: split a `say` field into reveal-timed beats.

This replaces gen-1's three overlapping fields (`voiceover` + `voiceover_beats`
+ `bookmark`/`reveal_groups`) with one. A `say` string carries the spoken words
*and* inline `{show <id>}` markers. Each marker means "reveal block <id> now,
at the start of the text that follows".

    say = "A is true. {show math.0} Here is why. {show math.1} And so."

splits into beats:

    Beat(text="A is true.",   reveal=None)     # spoken while static content holds
    Beat(text="Here is why.", reveal="math.0") # reveal math.0, then speak this
    Beat(text="And so.",      reveal="math.1")

When TTS is wired (last), each beat is synthesized as one clip and its measured
duration is the reveal hold. Until then, `estimate_seconds` stands in by word
count. Either way the alignment model is identical -- TTS just swaps the clock.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_SHOW = re.compile(r"\{\s*show\s+([A-Za-z0-9_.]+)\s*\}")


@dataclass
class Beat:
    text: str
    reveal: str | None


def _clean(text: str) -> str:
    """Collapse YAML block-scalar whitespace/newlines into one spoken line."""
    return " ".join(text.split())


def parse_say(say: str) -> list[Beat]:
    """Split *say* at each ``{show <id>}`` marker into ordered beats."""
    if not say:
        return []

    beats: list[Beat] = []
    cursor = 0
    prev_reveal: str | None = None
    for match in _SHOW.finditer(say):
        beats.append(Beat(_clean(say[cursor:match.start()]), prev_reveal))
        prev_reveal = match.group(1)
        cursor = match.end()
    beats.append(Beat(_clean(say[cursor:]), prev_reveal))

    # Drop a beat only if it carries neither words nor a reveal.
    return [b for b in beats if b.text or b.reveal]


def list_reveal_targets(say: str) -> list[str]:
    """All block ids named by ``{show ...}`` in *say* (for validation/lint)."""
    return [m.group(1) for m in _SHOW.finditer(say or "")]


def estimate_seconds(text: str, *, wpm: float = 150.0, floor: float = 1.2) -> float:
    """Stand-in beat duration by word count, until real audio is measured."""
    words = len(text.split())
    return max(words / (wpm / 60.0), floor)

"""Scene-level forced alignment: one storyboard content scene -> aligned beat timeline.

Ports the validated experiment core (video/experiments/forced_alignment_dean/) into
the production pipeline. Everything here is a pure function EXCEPT align_scene(),
the single seam that calls the aligner (stable-ts). That isolation lets us swap in
torchaudio CTC forced alignment without touching gates/mapping -- stable-ts upstream
was archived 2026-05-30 (see ENVIRONMENT.md 5c).

Offline-testable: build_scene_plan / explode_to_plan_tokens / map_to_beats /
run_gates / qa_diff / build_scene_aligned_entry operate on plain dicts, so
_selftest_scene_align.py needs no whisper model.
"""
from __future__ import annotations

import re
from typing import Any

from pipeline.narration import parse_say
from pipeline.timing import text_hash

# Canonical tokenizer -- single home. The experiment scripts each carried a copy
# (prepare_scene / run_stable_ts_align / map_alignment_to_beats); production takes
# exactly one. A-Z0-9 runs, with internal hyphen/apostrophe compounds ("sum-to",
# "cosine's") kept whole; every other char is a separator.
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")


class AlignmentError(RuntimeError):
    """Raised when alignment must abort (aborted aligner, or token-index break)."""


def tokenize(text: str) -> list[str]:
    return WORD_RE.findall(text)


def build_scene_plan(scene: dict[str, Any]) -> dict[str, Any]:
    """transcript = space-join of beat texts; each beat gets its [word_start,
    word_end) token range over that transcript. WORD_RE splits on the join spaces,
    so tokenize(transcript)[word_start:word_end] == tokenize(beat.text) exactly --
    that identity is what makes index-based beat mapping sound (verified in
    _selftest, enforced at align time by verify_plan_index)."""
    beats = parse_say(scene.get("say", ""))
    plan_beats: list[dict[str, Any]] = []
    parts: list[str] = []
    cursor = 0
    for index, beat in enumerate(beats, start=1):
        n = len(tokenize(beat.text))
        plan_beats.append({
            "index": index,
            "id": f"beat_{index:02d}",
            "reveal": beat.reveal,
            "text": beat.text,
            "text_hash": text_hash(beat.text),
            "word_start": cursor,
            "word_end": cursor + n,
        })
        if beat.text:
            parts.append(beat.text)
        cursor += n
    transcript = " ".join(parts).strip()
    return {
        "scene_id": scene["id"],
        "transcript": transcript,
        "scene_text_hash": text_hash(transcript),
        "word_count": len(tokenize(transcript)),
        "beats": plan_beats,
    }

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


def explode_to_plan_tokens(
    aligned_words: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[int, dict[str, Any]]]:
    """Split aligner words into plan WORD_RE tokens, interpolating timestamps by
    character share. Both aligner and plan read the same transcript text, so
    exploding each aligner word with WORD_RE reproduces the plan token sequence.

    Punctuation-only aligner words (e.g. a standalone "--") yield no token; their
    span survives as an inter-word gap, and beat starts always sit on the next real
    word's onset, so no reveal timing is lost by dropping them.

    Returns (tokens, multi) where multi maps token index -> parent info for tokens
    from a multi-token parent word (their timestamps are interpolated, not measured).
    """
    out: list[dict[str, Any]] = []
    multi: dict[int, dict[str, Any]] = {}
    for word in aligned_words:
        tokens = WORD_RE.findall(word["text"])
        if not tokens:
            continue  # punctuation-only word
        for ordinal in range(len(tokens)) if len(tokens) > 1 else ():
            multi[len(out) + ordinal] = {
                "parent": word["text"].strip(), "ordinal": ordinal, "tokens": len(tokens),
            }
        start, end = float(word["start"]), float(word["end"])
        span = max(end - start, 0.0)
        total_chars = sum(len(t) for t in tokens)
        cursor = start
        for token in tokens:
            share = (len(token) / total_chars) if total_chars else 1.0 / len(tokens)
            token_end = min(cursor + span * share, end)
            out.append({
                "word": token, "start": round(cursor, 3), "end": round(token_end, 3),
                "probability": word.get("probability"),
            })
            cursor = token_end
        out[-1]["end"] = end  # avoid rounding drift on the last token
    return out, multi


def verify_plan_index(words: list[dict[str, Any]], plan: dict[str, Any]) -> None:
    """Raise AlignmentError unless exploded aligner tokens == plan tokens, position
    by position. This is the contract that makes index-based beat mapping sound;
    by construction it should always hold, so a break means a real defect."""
    plan_tokens = tokenize(plan["transcript"])
    got = [w["word"] for w in words]
    if got == plan_tokens:
        return
    for i, (g, want) in enumerate(zip(got, plan_tokens)):
        if g != want:
            raise AlignmentError(
                f"token mismatch at index {i}: aligned={g!r} plan={want!r}; "
                "index-based beat mapping would be unsound"
            )
    raise AlignmentError(f"token count mismatch: aligned={len(got)} plan={len(plan_tokens)}")

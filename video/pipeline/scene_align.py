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
from difflib import SequenceMatcher
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


def _start_for_word(words: list[dict[str, Any]], index: int, audio_seconds: float) -> float:
    """Onset of plan token `index`; 0.0 for index<=0; audio end when index runs past
    the last word (last beat's end)."""
    if not words or index <= 0:
        return 0.0
    if index < len(words):
        return float(words[index]["start"])
    return audio_seconds


def map_to_beats(
    plan: dict[str, Any],
    words: list[dict[str, Any]],
    audio_seconds: float,
    *,
    multi: dict[int, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Reveal boundary = beat's first-word onset; a beat runs to the next beat's
    start, and the last beat runs to the audio end (inter-beat pause belongs to the
    preceding beat -- design §14, matches the beat-level clock). Emits the shared
    beats[] shape plus word_start/word_end and a boundary-quality record."""
    multi = multi or {}
    starts = [_start_for_word(words, int(b["word_start"]), audio_seconds) for b in plan["beats"]]
    out: list[dict[str, Any]] = []
    for i, beat in enumerate(plan["beats"]):
        start = starts[i]
        end = starts[i + 1] if i + 1 < len(starts) else audio_seconds
        end = max(end, start)
        wi = int(beat["word_start"])
        # 0 <= wi (not 0 < wi): a spoken beat immediately after a leading/consecutive
        # reveal-only beat legitimately has word_start==0 and IS a boundary beat that
        # gate 3 must inspect. beats[0] also gets a prob here but run_gates skips it
        # (iterates beats[1:]), so no false gate. wi==len(words) (trailing reveal-only)
        # stays None.
        prob = words[wi].get("probability") if 0 <= wi < len(words) else None
        out.append({
            "index": beat["index"], "id": beat["id"], "reveal": beat["reveal"],
            "text": beat["text"], "text_hash": beat["text_hash"],
            "word_start": beat["word_start"], "word_end": beat["word_end"],
            "start_seconds": round(start, 3), "end_seconds": round(end, 3),
            "audio_seconds": round(end - start, 3),
            "boundary": {"prob": prob, "interpolated": wi in multi and multi[wi]["ordinal"] > 0},
        })
    return out


# 3-scene pilot (2026-07-05) initial thresholds. Every gate value + its rationale
# lives here so tuning is one edit.
# RECALIBRATION 1 (2026-07-05, ch03 batch-1, 10 real Dean scenes): thresholds HELD --
# zero false fails; every correctly-aligned beat-2..N boundary sat above 0.15, the
# lowest being 0.176 (slope_equals_height) / 0.209 (shm_stacked_graphs), both in the
# 0.15-0.35 WARN band. Kept as-is; the ~0.03 margin between the lowest real boundary
# (0.176) and boundary_prob_fail (0.15) is thin -- if a future deck shows a correct
# boundary at/under 0.15, lower boundary_prob_fail then.
GATES = {
    "boundary_prob_fail": 0.15,   # observed normal boundary min 0.53 ("Look"); << this = untrustworthy
    "boundary_prob_warn": 0.35,   # 0.15-0.35 -> WARN
    "interior_low_prob": 0.5,     # run threshold for interior words
    "interior_low_prob_min_run": 2,
    "prob_mean_warn": 0.7,        # informational only (never fails: no discriminative power)
    "interior_gap_fail": 2.0,     # legal inter-sentence pause maxed at 0.89s in pilot
    "zero_dur_ratio_fail": 0.05,  # or >=2 consecutive zero-duration tokens
    "char_share_warn": (0.6, 1.6),  # beat duration vs char-share ratio band
    "char_share_fail": (0.4, 2.2),
    "short_beat_warn": 0.05,      # existing mapper convention
}


def _zero_runs(words):
    runs, cur = [], []
    for i, w in enumerate(words):
        if float(w["end"]) - float(w["start"]) <= 0.0:
            cur.append(i)
        else:
            if cur:
                runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return runs


def run_gates(plan, words, beats, audio_seconds):
    """Return {"status": pass|pass_with_warnings|fail, "failures": [...],
    "warnings": [...], "metrics": {...}}. FAIL -> scene goes to the fallback ladder;
    status is never written to a manifest as "fail" (a failed scene is retried or
    demoted to beats), so consumers only ever see pass / pass_with_warnings."""
    failures: list[str] = []
    warnings: list[str] = []
    probs = [w["probability"] for w in words if w.get("probability") is not None]

    # 1. monotonic AND non-overlapping word timestamps (design §5 row 3: either fails).
    #    Trailing silence (last word end -> audio end) is intentionally NOT gated here:
    #    §5's char-share gate excludes tail silence, so the design tolerates it.
    for i in range(1, len(words)):
        if float(words[i]["start"]) + 1e-6 < float(words[i - 1]["start"]):
            failures.append(f"non-monotonic word timestamps at index {i}")
            break
    for i in range(1, len(words)):
        if float(words[i]["start"]) + 1e-6 < float(words[i - 1]["end"]):
            failures.append(f"overlapping word timestamps at index {i} "
                            f"(token {i-1} ends {words[i-1]['end']:.3f} > token {i} starts {words[i]['start']:.3f})")
            break

    # 2. zero-duration tokens: >=2 consecutive, or >5% total -> FAIL (isolated -> ignore)
    zruns = _zero_runs(words)
    total_zero = sum(len(r) for r in zruns)
    if any(len(r) >= 2 for r in zruns) or (words and total_zero / len(words) > GATES["zero_dur_ratio_fail"]):
        failures.append(f"zero-duration tokens: {total_zero} in {len(zruns)} run(s)")

    # 3. boundary-word probability (beats 2..N first word)
    for b in beats[1:]:
        p = (b.get("boundary") or {}).get("prob")
        if p is None:
            continue
        if p < GATES["boundary_prob_fail"]:
            failures.append(f"{b['id']} boundary word probability {p:.2f} < {GATES['boundary_prob_fail']}")
        elif p < GATES["boundary_prob_warn"]:
            warnings.append(f"{b['id']} boundary word probability {p:.2f} (soft)")

    # 4. unexplained interior gap (between consecutive words, not a beat boundary)
    boundary_word_idx = {int(b["word_start"]) for b in beats}
    for i in range(1, len(words)):
        gap = float(words[i]["start"]) - float(words[i - 1]["end"])
        if gap > GATES["interior_gap_fail"] and i not in boundary_word_idx:
            failures.append(f"unexplained {gap:.2f}s gap before token {i} (not a beat boundary)")

    # 5. beat duration vs character-share sanity (last beat uses last-word end, not tail silence)
    total_chars = sum(len(b["text"]) for b in beats) or 1
    speech_end = float(words[-1]["end"]) if words else audio_seconds
    for i, b in enumerate(beats):
        share = len(b["text"]) / total_chars
        dur = b["audio_seconds"] if i + 1 < len(beats) else max(speech_end - b["start_seconds"], 0.0)
        span = speech_end or 1.0
        ratio = (dur / (share * span)) if share else 1.0
        lo_f, hi_f = GATES["char_share_fail"]
        lo_w, hi_w = GATES["char_share_warn"]
        if ratio < lo_f or ratio > hi_f:
            failures.append(f"{b['id']} duration/char-share ratio {ratio:.2f} out of {GATES['char_share_fail']}")
        elif ratio < lo_w or ratio > hi_w:
            warnings.append(f"{b['id']} duration/char-share ratio {ratio:.2f} (soft)")
        if b["audio_seconds"] < GATES["short_beat_warn"]:
            warnings.append(f"{b['id']} very short duration {b['audio_seconds']:.3f}s")

    # 6. interior low-prob runs + prob_mean -> informational WARN only (never fail)
    runs, cur = [], []
    for i, w in enumerate(words):
        p = w.get("probability")
        if p is not None and p < GATES["interior_low_prob"] and i not in boundary_word_idx:
            cur.append(i)
        else:
            if len(cur) >= GATES["interior_low_prob_min_run"]:
                runs.append(cur)
            cur = []
    if len(cur) >= GATES["interior_low_prob_min_run"]:
        runs.append(cur)
    for r in runs:
        warnings.append(f"interior low-prob run tokens {r[0]}-{r[-1]}: "
                        + " ".join(words[i]["word"] for i in r))
    prob_mean = round(sum(probs) / len(probs), 3) if probs else None
    if prob_mean is not None and prob_mean < GATES["prob_mean_warn"]:
        warnings.append(f"prob_mean {prob_mean} < {GATES['prob_mean_warn']} (informational)")

    status = "fail" if failures else ("pass_with_warnings" if warnings else "pass")
    return {"status": status, "failures": failures, "warnings": warnings,
            "metrics": {"prob_mean": prob_mean,
                        "low_prob_words": sum(1 for p in probs if p < GATES["interior_low_prob"])}}


def qa_diff(plan_tokens, asr_tokens, fa_probs, *, weak_spans=(), min_cluster=3,
            weak_prob=0.5, window=2):
    """Grade the free-ASR-vs-transcript diff (design §6). transcript-constrained FA
    cannot see words the TTS dropped/repeated -- the ASR probe can. A dropped/inserted/
    replaced cluster of >= min_cluster tokens is:
      - FAIL (suspect TTS misspeak) if it CO-LOCATES with weakness -- either low FA
        probability inside the cluster's plan-token WINDOW, or overlap with a gate
        weak_span (plan-token ranges the gates flagged). Co-location is LOCAL, not
        global: an unrelated weak span elsewhere does not condemn the cluster.
      - INFO (ASR artifact) otherwise -- the derivation pilot was exactly this: ASR
        skipped a repeated formula, the audio was innocent.

    Deletions/replacements span [i1,i2) on the plan side; an INSERTION has i1==i2, so
    its co-location window is [i1-window, i1+window) (fa_probs[i1:i2] would be empty).
    weak_spans: iterable of (start, end) plan-token index ranges from the gate pass
    (e.g. a soft/failed boundary word's index, an interior-gap location).
    Returns {"verdict": clean|info|fail, "clusters": [...]}."""
    spans = list(weak_spans)
    n = len(plan_tokens)

    def _overlaps_weak_span(lo, hi):
        return any(not (hi <= s or lo >= e) for s, e in spans)

    sm = SequenceMatcher(a=plan_tokens, b=asr_tokens, autojunk=False)
    clusters = []
    verdict = "clean"
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        size = max(i2 - i1, j2 - j1)
        if size < min_cluster:
            continue
        lo, hi = (i1, i2) if i2 > i1 else (max(0, i1 - window), min(n, i1 + window))
        local_weak = any(p is not None and p < weak_prob for p in fa_probs[lo:hi])
        gate_weak = _overlaps_weak_span(lo, hi)
        is_fail = local_weak or gate_weak
        clusters.append({"tag": tag, "plan_span": [i1, i2], "asr_span": [j1, j2],
                         "window": [lo, hi], "size": size,
                         "fa_weak": local_weak, "gate_weak": gate_weak,
                         "verdict": "fail" if is_fail else "info"})
        if is_fail:
            verdict = "fail"
        elif verdict != "fail":
            verdict = "info"
    return {"verdict": verdict, "clusters": clusters}


def boundary_weak_spans(beats, *, warn=0.35):
    """Plan-token weak spans for qa_diff co-location: each boundary beat (beats[1:])
    whose boundary prob is below `warn` contributes a 1-wide span at its word_start.
    Kept separate so the tts caller can also add interior-gap spans if needed."""
    spans = []
    for b in beats[1:]:
        p = (b.get("boundary") or {}).get("prob")
        if p is not None and p < warn:
            spans.append((int(b["word_start"]), int(b["word_start"]) + 1))
    return spans


def low_prob_runs(words, threshold, min_run):
    """Runs of >= min_run consecutive words below `threshold` (ported verbatim from
    run_stable_ts_align.py so the persisted summary matches the experiment)."""
    runs, cur = [], []
    for i, w in enumerate(words):
        p = w.get("probability")
        if p is not None and p < threshold:
            cur.append(i)
        else:
            if len(cur) >= min_run:
                runs.append(cur)
            cur = []
    if len(cur) >= min_run:
        runs.append(cur)
    return runs


def align_scene(wav_path, plan, *, model="base.en", device="cpu", language="en",
                nonspeech_skip=5.0, failure_threshold=0.2, prob_threshold=0.5, min_run=2):
    """THE aligner seam -- the only stable-ts caller. Constrained to plan["transcript"],
    explodes to plan tokens, verifies the plan-token index. Returns a dict
    {"words", "summary", "segments", "multi"}:
      - words:   plan-token list [{word,start,end,probability}], the beat-mapping input
      - summary: SAME shape the experiment (run_stable_ts_align.py) persists -- aligner,
                 word_count, beat_boundary_in_multi_token_word, prob_min, prob_mean,
                 low_prob_words, low_prob_runs (so Task 12 regression is meaningful)
      - segments: raw stable-ts segments (persisted for QA/debug parity)
      - multi:   token-index -> multi-token-parent map, for map_to_beats boundary flags
                 (NOT persisted; the experiment stores its beat-keyed projection in
                 summary.beat_boundary_in_multi_token_word instead)
    Raises AlignmentError on aligner abort or token-index break. Swapping to torchaudio
    CTC means reimplementing only this function.

    remove_instant_words stays False: dropping zero-duration words would break the 1:1
    plan-token indexing that beat mapping depends on."""
    try:
        import stable_whisper
    except ImportError as exc:  # pragma: no cover - env guard
        raise AlignmentError("stable-ts not installed; see ENVIRONMENT.md 5c") from exc
    model_obj = stable_whisper.load_model(model, device=device)
    result = model_obj.align(str(wav_path), plan["transcript"], language=language,
                             nonspeech_skip=nonspeech_skip, failure_threshold=failure_threshold,
                             remove_instant_words=False)
    if result is None:
        raise AlignmentError(f"stable-ts aborted: > {failure_threshold:.0%} of words failed to align")
    raw = result.to_dict()
    segments = raw.get("segments", [])
    aligned_words = [{"text": w.get("word", ""), "start": w.get("start"),
                      "end": w.get("end"), "probability": w.get("probability")}
                     for seg in segments for w in seg.get("words", [])]
    words, multi = explode_to_plan_tokens(aligned_words)
    verify_plan_index(words, plan)
    boundary_in_multi = [{"beat": b["id"], **multi[int(b["word_start"])]}
                         for b in plan["beats"]
                         if int(b["word_start"]) in multi and multi[int(b["word_start"])]["ordinal"] > 0]
    probs = [w["probability"] for w in words if w.get("probability") is not None]
    runs = low_prob_runs(words, prob_threshold, min_run)
    summary = {
        "aligner": {"tool": "stable-ts", "version": stable_whisper.__version__, "model": model,
                    "nonspeech_skip": nonspeech_skip, "failure_threshold": failure_threshold},
        "word_count": len(words),
        "beat_boundary_in_multi_token_word": boundary_in_multi,
        "prob_min": round(min(probs), 3) if probs else None,
        "prob_mean": round(sum(probs) / len(probs), 3) if probs else None,
        "low_prob_words": sum(1 for p in probs if p < prob_threshold),
        "low_prob_runs": [
            {"indices": [r[0], r[-1]], "start": words[r[0]]["start"], "end": words[r[-1]]["end"],
             "text": " ".join(words[i]["word"] for i in r),
             "probs": [round(words[i]["probability"], 3) for i in r]}
            for r in runs
        ],
    }
    return {"words": words, "summary": summary, "segments": segments, "multi": multi}


def build_scene_aligned_entry(*, scene_number, plan, beats, audio_seconds, audio_file,
                              summary, gates, words_file, aligned_file, chunks=None,
                              fallback_history=None):
    """Assemble a schema-2 scene_aligned manifest entry (design §3). Same beats[]
    shape as beats mode + scene-level audio_file + alignment/validation blocks."""
    return {
        "scene_number": scene_number,
        "scene_id": plan["scene_id"],
        "kind": "content",
        "narration_mode": "scene_aligned",
        "audio_file": str(audio_file),
        "audio_seconds": round(float(audio_seconds), 3),
        "scene_text_hash": plan["scene_text_hash"],
        "script": " ".join(b["text"] for b in beats if b["text"]).strip(),
        "beat_count": len(beats),
        "beats": beats,
        "alignment": {
            "words_file": str(words_file),
            "aligned_file": str(aligned_file),
            "aligner": summary["aligner"],
            "chunks": chunks,
        },
        "validation": {"status": gates["status"], "warnings": gates["warnings"],
                       "metrics": gates["metrics"]},
        "fallback_history": fallback_history or [],
    }


# --- sentence-chunk fallback (design §7 rung 3) --------------------------------
# Split only on whitespace that FOLLOWS sentence-ending punctuation, so no WORD_RE
# token is ever cut: flatten(tokenize(c) for c in chunks) == tokenize(transcript).
# That tiling identity is what keeps the merged, re-indexed word list sound.
_SENT_BOUNDARY = re.compile(r"(?<=[.!?])\s+")


def split_sentence_chunks(transcript: str) -> list[str]:
    """Partition `transcript` into sentence substrings that tile its WORD_RE tokens
    exactly (see note above). Over-splitting (e.g. an "e.g. " abbreviation) is
    harmless -- it only shortens a chunk; the tiling invariant holds because every
    split point sits on whitespace. Returns a single-element list when there is no
    interior sentence break (the caller then declines to chunk)."""
    parts = [p.strip() for p in _SENT_BOUNDARY.split(transcript.strip()) if p.strip()]
    return parts or ([transcript.strip()] if transcript.strip() else [])


def merge_chunk_alignments(
    chunk_results: list[dict[str, Any]],
    chunk_durations: list[float],
    chunk_texts: list[str],
    plan: dict[str, Any],
) -> dict[str, Any]:
    """Merge per-sentence-chunk align_scene outputs into ONE align_scene-shaped result
    over the whole scene (design §7 rung 3). Each chunk was aligned against its own WAV
    with local timestamps; here every chunk's word times are offset by the cumulative
    chunk-WAV duration and its multi-token indices by the cumulative token count, so the
    concatenated WAV and the merged word list share one clock. verify_plan_index against
    the FULL plan is the soundness gate -- a tiling/count break raises AlignmentError and
    the caller routes to the beats terminal. Returns the align_scene shape
    {"words","summary","segments","multi"} plus per-chunk `chunks` metadata."""
    merged_words: list[dict[str, Any]] = []
    merged_multi: dict[int, dict[str, Any]] = {}
    merged_segments: list[dict[str, Any]] = []
    chunks_meta: list[dict[str, Any]] = []
    time_offset = 0.0
    token_offset = 0
    for i, (res, dur, text) in enumerate(zip(chunk_results, chunk_durations, chunk_texts)):
        words = res["words"]
        for w in words:
            merged_words.append({**w, "start": round(float(w["start"]) + time_offset, 3),
                                 "end": round(float(w["end"]) + time_offset, 3)})
        for k, v in (res.get("multi") or {}).items():
            merged_multi[int(k) + token_offset] = v
        for seg in (res.get("segments") or []):
            merged_segments.append({**seg, "chunk": i, "time_offset": round(time_offset, 3)})
        probs = [w["probability"] for w in words if w.get("probability") is not None]
        chunks_meta.append({
            "index": i, "text": text,
            "word_start": token_offset, "word_end": token_offset + len(words),
            "audio_seconds": round(float(dur), 3),
            "prob_min": round(min(probs), 3) if probs else None,
        })
        time_offset += float(dur)
        token_offset += len(words)
    verify_plan_index(merged_words, plan)   # soundness: merged tokens must equal plan tokens
    boundary_in_multi = [{"beat": b["id"], **merged_multi[int(b["word_start"])]}
                         for b in plan["beats"]
                         if int(b["word_start"]) in merged_multi
                         and merged_multi[int(b["word_start"])]["ordinal"] > 0]
    all_probs = [w["probability"] for w in merged_words if w.get("probability") is not None]
    runs = low_prob_runs(merged_words, 0.5, 2)
    base_aligner = chunk_results[0]["summary"]["aligner"] if chunk_results else {}
    summary = {
        "aligner": {**base_aligner, "mode": "sentence_chunk", "chunks": len(chunk_results)},
        "word_count": len(merged_words),
        "beat_boundary_in_multi_token_word": boundary_in_multi,
        "prob_min": round(min(all_probs), 3) if all_probs else None,
        "prob_mean": round(sum(all_probs) / len(all_probs), 3) if all_probs else None,
        "low_prob_words": sum(1 for p in all_probs if p < 0.5),
        "low_prob_runs": [
            {"indices": [r[0], r[-1]], "start": merged_words[r[0]]["start"],
             "end": merged_words[r[-1]]["end"],
             "text": " ".join(merged_words[i]["word"] for i in r),
             "probs": [round(merged_words[i]["probability"], 3) for i in r]}
            for r in runs
        ],
    }
    return {"words": merged_words, "summary": summary, "segments": merged_segments,
            "multi": merged_multi, "chunks": chunks_meta}

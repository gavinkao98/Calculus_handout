> **Status: archived / completed（2026-07-07 歸檔）** — 本計畫已全數落地（執行紀錄見 `video/_archive/REBUILD_LOG-2026-05-to-07.md` 對應節）。活的權威見 `video/REVIEW_GATES.md`／`video/DESIGN.md`／`video/SPEC-pedagogy-firstlearner-*.md`。本檔為歷史施工紀錄，內含相對路徑可能已過時。

# Scene-level TTS + Forced Alignment — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Productionize the validated scene-level TTS + `stable-ts` forced-alignment experiment (`video/experiments/forced_alignment_dean/`) into the `video/` pipeline: synthesize one WAV per content *scene*, recover per-beat reveal timing by transcript-constrained forced alignment, validate per-scene, and fall back to the existing beat-level route whenever validation fails — so there is always a shippable path.

**Architecture:** New module `video/pipeline/scene_align.py` holds the alignment core as pure functions (tokenize → build scene plan → explode aligner words to plan tokens → map to beat boundaries → validation gates → ASR QA probe → manifest v2 assembly), plus a single `align_scene()` seam that is the only code touching the aligner (`stable-ts`, swappable for torchaudio CTC). Manifest gains `"schema": 2` and a third `narration_mode` value `"scene_aligned"` whose per-scene entry keeps the **same `beats[]` shape** as `"beats"` mode plus a scene-level `audio_file`; this makes 6 of 7 consumers a one-line condition relaxation and only `make.py._validate_reuse_manifest` a real new branch. `tts.py` gains `--unit beat|scene|auto` and drives synth → align → gates → fallback ladder. Everything except the billed real-audio A/B is offline and zero-cost.

**Tech Stack:** Python 3.12, `stable-ts 2.19.1` (`stable_whisper.align`, transcript-constrained), `openai-whisper` (`whisper-timestamped` for the QA probe), manim (render, deferred import), ffmpeg/ffprobe (mux/probe), stdlib `wave`/`difflib`/`hashlib`. Tests are stdlib-`assert` selftests (project convention: `video/pipeline/_selftest_*.py`, standalone `__main__` runner).

**Authoritative design:** [`video/experiments/forced_alignment_dean/REVIEW-scene-tts-production-design.html`](experiments/forced_alignment_dean/REVIEW-scene-tts-production-design.html) (all `§N` references below point there). Approved by user 2026-07-05; batch-1 scope = design §10 staged rollout (four templates first, derivation/theorem_proof in batch 2).

---

## Phase boundary (billed-API discipline, CLAUDE.md)

- **Phase A (Tasks 1–13) is entirely offline and zero-cost:** selftests, mock scene-WAV integration, and real-data regression against the three experiment WAVs already on disk. No API calls. Execute the whole of Phase A without stopping for cost approval.
- **Phase B (Task 14) is billed** (real MiMo synthesis of the §3.1 deck, 21 scenes, for the acceptance A/B). Per CLAUDE.md, **STOP at the end of Task 13 and issue a quote** (model, scene/beat count, estimated audio seconds, and the §7 fallback retry budget of ≤2 extra calls/scene) and get explicit consent before running Task 14.

---

## File Structure

| File | Responsibility |
|------|----------------|
| `video/pipeline/scene_align.py` **(new, ~260 lines)** | Alignment core. Pure functions: `tokenize`/`WORD_RE` (canonical home), `build_scene_plan`, `explode_to_plan_tokens`, `verify_plan_index`, `map_to_beats`, `GATES` dict + `run_gates`, `qa_diff`, `build_scene_aligned_entry`. One impure seam: `align_scene` (the only stable-ts caller). No manim import. |
| `video/pipeline/tts.py` **(modify)** | Add `--unit beat\|scene\|auto` + scene code path (synth scene WAV → `align_scene` → `run_gates` → fallback ladder → schema-2 entry), reuse per §3 freshness matrix, top-level `"schema": 2`. Beat path unchanged. |
| `video/pipeline/scene_fallback.py` **(new, ~90 lines)** | Fallback ladder (§7): `small.en` arbiter → resynth → sentence-chunk → beat-level. Kept out of `tts.py` to isolate the billed-retry logic and its budget guard. |
| `video/make.py` **(modify, ~40 lines)** | 4 consumer condition-relaxations (`_beat_durations`, `_audit_render_sync`, `compose`, `_warn_short_beats` auto) + `_validate_reuse_manifest` scene_aligned branch + `sum(beats)≈audio_seconds` assertion + entry `schema>2` guard. `synth_scene` (mock) untouched. |
| `video/pipeline/critic.py` **(modify, ~2 lines)** | `plan_frames`: accept `scene_aligned` alongside `beats`. |
| `video/pipeline/_selftest_scene_align.py` **(new, ~200 lines)** | Offline selftest for all pure functions (no whisper model). |
| `video/pipeline/_selftest_scene_align_integration.py` **(new, ~90 lines)** | Offline integration: mock scene WAV (silence + linear words) through tts scene path → make render/compose stubs; fallback ladder driven by injected gate failures. |
| `video/DESIGN.md`, `video/RUNBOOK-mimo-narration-route.md`, `video/REBUILD_STATUS.md`, `ENVIRONMENT.md` **(modify)** | Manifest v2 contract, lock-gated scene synth step, landing record. |

**Aligner-output word dict (the shared fixture shape).** Every pure function below consumes/produces plain dicts, so selftests need no model:
```python
# a "plan-token word" (output of explode_to_plan_tokens / align_scene):
{"word": "sine", "start": 12.34, "end": 12.71, "probability": 0.87}
# a "manifest beat" (output of map_to_beats, consumed by render/compose):
{"index": 1, "id": "beat_01", "reveal": "math.0", "text": "...", "text_hash": "...",
 "audio_seconds": 15.58, "start_seconds": 0.0, "end_seconds": 15.58,
 "word_start": 0, "word_end": 30, "boundary": {"prob": 0.83, "interpolated": False}}
```

---

## Task 1: `scene_align.py` scaffold + canonical `tokenize` + `build_scene_plan`

**Files:**
- Create: `video/pipeline/scene_align.py`
- Create: `video/pipeline/_selftest_scene_align.py`
- Reference (do not edit): `video/experiments/forced_alignment_dean/prepare_scene.py:23-80`, `video/pipeline/narration.py:39-54`, `video/pipeline/timing.py:26-27`

- [ ] **Step 1: Write the failing test** — in `_selftest_scene_align.py`:

```python
"""Offline self-test for scene_align.py. Run: python video/pipeline/_selftest_scene_align.py
Needs no whisper model: every function under test consumes plain dicts/fixtures."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import scene_align as SA  # noqa: E402


def test_tokenize_matches_word_re():
    # canonical tokenizer: hyphen/apostrophe compounds are one token, punctuation splits
    assert SA.tokenize("sum-to-product, cosine's") == ["sum-to", "product", "cosine's"]
    assert SA.tokenize("") == []


def test_build_scene_plan_token_ranges_and_transcript():
    scene = {"id": "s", "say": "A is true. {show m.0} Here is why. {show m.1} And so."}
    plan = SA.build_scene_plan(scene)
    # transcript = join of beat texts; scene_text_hash covers it
    assert plan["transcript"] == "A is true. Here is why. And so."
    assert plan["word_count"] == len(SA.tokenize(plan["transcript"]))
    beats = plan["beats"]
    assert [b["reveal"] for b in beats] == [None, "m.0", "m.1"]
    # contiguous, non-overlapping [word_start, word_end) covering the whole transcript
    assert beats[0]["word_start"] == 0
    for a, b in zip(beats, beats[1:]):
        assert a["word_end"] == b["word_start"]
    assert beats[-1]["word_end"] == plan["word_count"]
    # the transcript slice for each beat equals that beat's own tokenization (the invariant)
    toks = SA.tokenize(plan["transcript"])
    for b in beats:
        assert toks[b["word_start"]:b["word_end"]] == SA.tokenize(b["text"])
    # per-beat text_hash present (freshness), scene_text_hash present
    assert all(b["text_hash"] for b in beats)
    assert plan["scene_text_hash"]


def test_build_scene_plan_reveal_only_beat_has_zero_width_range():
    # a {show} with no following words -> reveal-only beat: contributes no tokens
    scene = {"id": "s", "say": "Look here. {show m.0}"}
    plan = SA.build_scene_plan(scene)
    assert plan["beats"][-1]["reveal"] == "m.0"
    assert plan["beats"][-1]["word_start"] == plan["beats"][-1]["word_end"]


if __name__ == "__main__":
    test_tokenize_matches_word_re()
    test_build_scene_plan_token_ranges_and_transcript()
    test_build_scene_plan_reveal_only_beat_has_zero_width_range()
    print("OK scene_align self-test (Task 1)")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python video/pipeline/_selftest_scene_align.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'pipeline.scene_align'`

- [ ] **Step 3: Write minimal implementation** — create `video/pipeline/scene_align.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python video/pipeline/_selftest_scene_align.py`
Expected: PASS — `OK scene_align self-test (Task 1)`

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/scene_align.py video/pipeline/_selftest_scene_align.py
git commit -m "feat(video/scene_align): scene plan + canonical tokenizer (Task 1)"
```

---

## Task 2: `explode_to_plan_tokens` + strict plan-index verification

**Files:**
- Modify: `video/pipeline/scene_align.py`
- Modify: `video/pipeline/_selftest_scene_align.py`
- Reference: `video/experiments/forced_alignment_dean/run_stable_ts_align.py:32-79,170-180`

- [ ] **Step 1: Write the failing test** — append to `_selftest_scene_align.py`:

```python
def test_explode_splits_multitoken_words_by_char_share():
    # stable-ts follows transcript whitespace: "sum-to-product." is ONE aligner word;
    # WORD_RE gives ["sum-to", "product"]. Explode splits the span by character share.
    aligned = [{"text": "sum-to-product.", "start": 0.0, "end": 1.0, "probability": 0.9}]
    words, multi = SA.explode_to_plan_tokens(aligned)
    assert [w["word"] for w in words] == ["sum-to", "product"]
    assert words[0]["start"] == 0.0 and words[-1]["end"] == 1.0   # last token snaps to parent end
    assert words[0]["end"] == words[1]["start"]                   # contiguous
    assert 1 in multi and multi[1]["ordinal"] == 1 and multi[1]["tokens"] == 2


def test_explode_drops_punctuation_only_words():
    aligned = [{"text": "here", "start": 0.0, "end": 0.5, "probability": 0.9},
               {"text": "--", "start": 0.5, "end": 0.7, "probability": None},
               {"text": "there", "start": 0.7, "end": 1.0, "probability": 0.9}]
    words, multi = SA.explode_to_plan_tokens(aligned)
    assert [w["word"] for w in words] == ["here", "there"]   # "--" drops; its span is inter-word gap
    assert multi == {}


def test_verify_plan_index_raises_on_mismatch():
    plan = SA.build_scene_plan({"id": "s", "say": "alpha beta gamma."})
    ok = [{"word": w, "start": i, "end": i + 1, "probability": 0.9}
          for i, w in enumerate(["alpha", "beta", "gamma"])]
    SA.verify_plan_index(ok, plan)  # no raise
    bad = [{"word": w, "start": i, "end": i + 1, "probability": 0.9}
           for i, w in enumerate(["alpha", "GONE", "gamma"])]
    try:
        SA.verify_plan_index(bad, plan)
    except SA.AlignmentError as exc:
        assert "index 1" in str(exc)
    else:
        raise AssertionError("expected AlignmentError on token mismatch")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python video/pipeline/_selftest_scene_align.py`
Expected: FAIL with `AttributeError: module 'pipeline.scene_align' has no attribute 'explode_to_plan_tokens'`

- [ ] **Step 3: Write minimal implementation** — append to `scene_align.py` (adapted verbatim from `run_stable_ts_align.py`, the reviewed+regressed experiment code):

```python
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
```

- [ ] **Step 4: Run test to verify it passes** — add the three new calls to the `__main__` block first, then:

Run: `python video/pipeline/_selftest_scene_align.py`
Expected: PASS — `OK scene_align self-test (Task 1)` (rename the print to `(Tasks 1-2)`)

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/scene_align.py video/pipeline/_selftest_scene_align.py
git commit -m "feat(video/scene_align): explode aligner words to plan tokens + index verify (Task 2)"
```

---

## Task 3: `map_to_beats` — boundary policy (first-word onset; last beat to file end)

**Files:**
- Modify: `video/pipeline/scene_align.py`
- Modify: `video/pipeline/_selftest_scene_align.py`
- Reference: `video/experiments/forced_alignment_dean/map_alignment_to_beats.py:72-104`; design §14 (reveal = beat first-word onset; inter-beat pause归前 beat)

- [ ] **Step 1: Write the failing test** — append:

```python
def test_map_to_beats_boundaries_and_shape():
    # 3 beats over 6 tokens [0,2)[2,4)[4,6); words linear at 1s each, audio=6.0s
    plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d {show m.1} e f"})
    words = [{"word": w, "start": float(i), "end": float(i) + 0.9, "probability": 0.8}
             for i, w in enumerate(["a", "b", "c", "d", "e", "f"])]
    beats = SA.map_to_beats(plan, words, audio_seconds=6.0)
    # start = first-word onset of each beat; end = next beat start; last -> audio end
    assert [b["start_seconds"] for b in beats] == [0.0, 2.0, 4.0]
    assert [b["end_seconds"] for b in beats] == [2.0, 4.0, 6.0]
    assert [b["audio_seconds"] for b in beats] == [2.0, 2.0, 2.0]
    # beats[] shape shared with beats mode + word_start/word_end + boundary
    b0 = beats[0]
    assert set(b0) >= {"index", "id", "reveal", "text", "text_hash",
                       "audio_seconds", "start_seconds", "end_seconds",
                       "word_start", "word_end", "boundary"}
    assert beats[1]["boundary"]["prob"] == 0.8            # boundary word's probability
    assert beats[1]["boundary"]["interpolated"] is False  # not from a multi-token parent


def test_map_to_beats_leading_reveal_only_then_spoken_boundary_has_prob():
    # Consecutive {show} => a real leading reveal-only beat (word_start==word_end==0),
    # then a spoken beat that ALSO starts at word_start==0. parse_say drops only the
    # very first empty+no-reveal beat, so beat[0] here keeps reveal m.0 (0 words) and
    # beat[1] is spoken from word 0. (A single leading {show} would be dropped, which
    # is why the earlier draft's "{show m.0} hello world" tested the wrong thing.)
    plan = SA.build_scene_plan({"id": "s", "say": "{show m.0} {show m.1} hello world"})
    assert plan["beats"][0]["word_start"] == plan["beats"][0]["word_end"] == 0   # reveal-only
    assert plan["beats"][1]["word_start"] == 0                                    # spoken from word 0
    words = [{"word": "hello", "start": 0.3, "end": 0.8, "probability": 0.9},
             {"word": "world", "start": 0.8, "end": 1.2, "probability": 0.9}]
    beats = SA.map_to_beats(plan, words, audio_seconds=1.2)
    assert beats[0]["start_seconds"] == 0.0
    # beat[1] is a boundary beat starting at word 0 -> its boundary prob must be set
    # (0 <= word_start), so run_gates gate 3 can inspect it. 0<word_start would drop it.
    assert beats[1]["boundary"]["prob"] == 0.9


def test_map_to_beats_interpolated_boundary_flagged():
    # boundary token that came from a multi-token parent -> interpolated True
    plan = SA.build_scene_plan({"id": "s", "say": "sum-to {show m.0} product now"})
    # aligner emitted "sum-to-product" as ONE word; explode makes token 1 ("product") a boundary
    aligned = [{"text": "sum-to-product", "start": 0.0, "end": 1.0, "probability": 0.7},
               {"text": "now", "start": 1.0, "end": 1.4, "probability": 0.9}]
    words, multi = SA.explode_to_plan_tokens(aligned)
    beats = SA.map_to_beats(plan, words, audio_seconds=1.4, multi=multi)
    assert beats[1]["boundary"]["interpolated"] is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python video/pipeline/_selftest_scene_align.py`
Expected: FAIL — `has no attribute 'map_to_beats'`

- [ ] **Step 3: Write minimal implementation** — append to `scene_align.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes** — wire the three calls into `__main__`, then run.

Run: `python video/pipeline/_selftest_scene_align.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/scene_align.py video/pipeline/_selftest_scene_align.py
git commit -m "feat(video/scene_align): map alignment to beat boundaries (Task 3)"
```

---

## Task 4: `GATES` dict + `run_gates` (boundary-focused validation, §5)

**Files:**
- Modify: `video/pipeline/scene_align.py`
- Modify: `video/pipeline/_selftest_scene_align.py`
- Reference: design §5 (thresholds + rationale), `RESULTS-2026-07-05.md` (pilot calibration)

**Gate policy (design §5):** reveal timing depends only on each beat's first word, so gates watch **boundaries**; interior low-probability words only WARN. Any FAIL routes the scene to the fallback ladder (Task 9). All thresholds live in one `GATES` dict, tagged as 3-scene-pilot initial values to recalibrate after batch-1.

- [ ] **Step 1: Write the failing test** — append:

```python
def _linear_words(tokens, per=1.0, prob=0.9):
    return [{"word": t, "start": i * per, "end": i * per + per * 0.9, "probability": prob}
            for i, t in enumerate(tokens)]


def test_run_gates_pass_clean_scene():
    plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d {show m.1} e f"})
    words = _linear_words(SA.tokenize(plan["transcript"]))
    beats = SA.map_to_beats(plan, words, audio_seconds=6.0)
    v = SA.run_gates(plan, words, beats, audio_seconds=6.0)
    assert v["status"] == "pass"


def test_run_gates_fail_nonmonotonic_timestamps():
    plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d"})
    words = _linear_words(SA.tokenize(plan["transcript"]))
    words[2]["start"] = 0.1  # token 2 (beat 2 boundary) jumps back before token 1
    beats = SA.map_to_beats(plan, words, audio_seconds=4.0)
    v = SA.run_gates(plan, words, beats, audio_seconds=4.0)
    assert v["status"] == "fail"
    assert any("monotonic" in w.lower() for w in v["failures"])


def test_run_gates_fail_overlapping_word_timestamps():
    # design §5 row 3 is "non-monotonic OR overlapping". Starts stay ordered but a word
    # ends AFTER the next word starts -> overlap -> FAIL (aligner anomaly).
    plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d"})
    words = _linear_words(SA.tokenize(plan["transcript"]))
    words[1]["end"] = words[2]["start"] + 0.5   # token 1 overruns token 2's onset
    beats = SA.map_to_beats(plan, words, audio_seconds=4.0)
    v = SA.run_gates(plan, words, beats, audio_seconds=4.0)
    assert v["status"] == "fail"
    assert any("overlap" in w.lower() for w in v["failures"])


def test_run_gates_tolerates_trailing_silence():
    # design §5: the char-share gate computes the LAST beat from "last word end,
    # excluding tail silence" -- trailing silence is deliberately NOT a fail gate.
    plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d"})
    words = _linear_words(SA.tokenize(plan["transcript"]))   # speech ends ~3.6s
    beats = SA.map_to_beats(plan, words, audio_seconds=12.0)  # 8s+ of trailing silence
    v = SA.run_gates(plan, words, beats, audio_seconds=12.0)
    assert v["status"] in ("pass", "pass_with_warnings")     # not failed by tail silence


def test_run_gates_fail_low_boundary_probability():
    plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d"})
    words = _linear_words(SA.tokenize(plan["transcript"]))
    words[2]["probability"] = 0.05  # beat-2 boundary word far below 0.15
    beats = SA.map_to_beats(plan, words, audio_seconds=4.0)
    v = SA.run_gates(plan, words, beats, audio_seconds=4.0)
    assert v["status"] == "fail"
    assert any("boundary" in w.lower() for w in v["failures"])


def test_run_gates_fail_large_interior_gap():
    plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d"})
    words = _linear_words(SA.tokenize(plan["transcript"]))
    words[3]["start"] = words[2]["end"] + 3.0  # 3s hole not at a beat boundary
    words[3]["end"] = words[3]["start"] + 0.5
    beats = SA.map_to_beats(plan, words, audio_seconds=8.0)
    v = SA.run_gates(plan, words, beats, audio_seconds=8.0)
    assert v["status"] == "fail"
    assert any("gap" in w.lower() for w in v["failures"])


def test_run_gates_warn_only_interior_low_prob_run():
    plan = SA.build_scene_plan({"id": "s", "say": "a b c {show m.0} d e f"})
    words = _linear_words(SA.tokenize(plan["transcript"]))
    words[1]["probability"] = 0.2  # interior (not a boundary) low-prob run
    words[2]["probability"] = 0.2
    beats = SA.map_to_beats(plan, words, audio_seconds=6.0)
    v = SA.run_gates(plan, words, beats, audio_seconds=6.0)
    assert v["status"] == "pass_with_warnings"
    assert v["failures"] == []
    assert any("low-prob" in w.lower() for w in v["warnings"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python video/pipeline/_selftest_scene_align.py`
Expected: FAIL — `has no attribute 'run_gates'`

- [ ] **Step 3: Write minimal implementation** — append to `scene_align.py`:

```python
# 3-scene pilot (2026-07-05) initial thresholds -- RECALIBRATE after the first real
# deck rollout (design §5, acceptance clause §10). Every gate value + its rationale
# lives here so tuning is one edit.
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
```

- [ ] **Step 4: Run test to verify it passes** — wire all five calls into `__main__`, then run.

Run: `python video/pipeline/_selftest_scene_align.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/scene_align.py video/pipeline/_selftest_scene_align.py
git commit -m "feat(video/scene_align): boundary-focused validation gates (Task 4)"
```

---

## Task 5: `qa_diff` — ASR QA probe grading (§6)

**Files:**
- Modify: `video/pipeline/scene_align.py`
- Modify: `video/pipeline/_selftest_scene_align.py`
- Reference: design §6 (grading table: FAIL when ASR cluster ≥3 tokens AND co-located FA weakness; else INFO)

`qa_diff` takes the plan transcript tokens and a free-ASR token list (from `whisper-timestamped`, already normalized) and returns graded clusters. It does NOT call the ASR model (the caller does); this is the pure diff+grade so it selftests offline.

- [ ] **Step 1: Write the failing test** — append:

```python
def test_qa_diff_info_when_fa_region_healthy():
    plan_tokens = "the quantity x plus one half h times sine".split()
    asr_tokens = "the quantity x plus sine".split()   # ASR dropped a cluster (>=3)
    # FA says that region is high-probability and no gate flagged it -> ASR artifact, INFO
    fa_probs = [0.9] * len(plan_tokens)
    res = SA.qa_diff(plan_tokens, asr_tokens, fa_probs, weak_spans=[])
    assert res["verdict"] == "info"
    assert res["clusters"]


def test_qa_diff_fail_on_deletion_over_fa_weakness():
    plan_tokens = "alpha beta gamma delta epsilon zeta".split()
    asr_tokens = "alpha zeta".split()                  # dropped 4-token cluster [1,5)
    fa_probs = [0.9, 0.1, 0.1, 0.1, 0.1, 0.9]          # FA weak exactly there
    res = SA.qa_diff(plan_tokens, asr_tokens, fa_probs, weak_spans=[])
    assert res["verdict"] == "fail"                    # local FA weakness inside the cluster


def test_qa_diff_insertion_uses_neighborhood_window():
    # ASR INSERTED tokens -> opcode span is empty on the plan side (i1==i2). Co-location
    # must look at a WINDOW around the insertion point, not the empty slice fa_probs[i1:i2].
    plan_tokens = "alpha beta gamma delta".split()
    asr_tokens = "alpha beta XXX YYY ZZZ gamma delta".split()   # 3-token insertion after "beta"
    fa_probs = [0.9, 0.1, 0.1, 0.9]                    # FA weak around the insertion point (idx ~2)
    res = SA.qa_diff(plan_tokens, asr_tokens, fa_probs, weak_spans=[], window=2)
    assert res["verdict"] == "fail"


def test_qa_diff_gate_weakness_must_be_colocated_not_global():
    # A weak span FAR from the diff cluster must NOT make the cluster fail (design §6:
    # "同區" = same region, local; the earlier draft's bool(gate_failures) was global).
    plan_tokens = "alpha beta gamma delta epsilon zeta eta theta".split()
    asr_tokens = "alpha beta gamma delta eta theta".split()      # drop cluster [4,6)
    fa_probs = [0.9] * len(plan_tokens)                          # FA healthy everywhere
    far = SA.qa_diff(plan_tokens, asr_tokens, fa_probs, weak_spans=[(0, 1)])   # weak span at token 0
    assert far["verdict"] == "info"                             # not co-located -> not fail
    near = SA.qa_diff(plan_tokens, asr_tokens, fa_probs, weak_spans=[(4, 5)])  # weak span in cluster
    assert near["verdict"] == "fail"


def test_qa_diff_ignores_small_clusters():
    plan_tokens = "alpha beta gamma".split()
    asr_tokens = "alpha gamma".split()                 # single-token drop (<3)
    res = SA.qa_diff(plan_tokens, asr_tokens, [0.9, 0.9, 0.9], weak_spans=[])
    assert res["verdict"] == "clean"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python video/pipeline/_selftest_scene_align.py`
Expected: FAIL — `has no attribute 'qa_diff'`

- [ ] **Step 3: Write minimal implementation** — append to `scene_align.py` (add `from difflib import SequenceMatcher` to the imports at the top of the file):

```python
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
```

- [ ] **Step 4: Run test to verify it passes** — wire all five `test_qa_diff_*` calls into `__main__`, run.

Run: `python video/pipeline/_selftest_scene_align.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/scene_align.py video/pipeline/_selftest_scene_align.py
git commit -m "feat(video/scene_align): ASR QA probe diff grading, local co-location (Task 5)"
```

---

## Task 6: `align_scene` — the aligner seam + `build_scene_aligned_entry`

**Files:**
- Modify: `video/pipeline/scene_align.py`
- Modify: `video/pipeline/_selftest_scene_align.py`
- Reference: `run_stable_ts_align.py:114-207` (the `align()` call + summary), design §3 (manifest entry shape)

`align_scene` is the only impure function; it is verified by real-data regression in Task 12 (not by the model-free selftest). `build_scene_aligned_entry` assembles the schema-2 entry and IS selftested (pure).

- [ ] **Step 1: Write the failing test** — append (tests the pure assembler; `align_scene` is exercised in Task 12):

```python
def test_build_scene_aligned_entry_shape():
    plan = SA.build_scene_plan({"id": "difference_quotient_for_sine",
                                "say": "a b {show m.0} c d {show m.1} e f"})
    words = _linear_words(SA.tokenize(plan["transcript"]))
    beats = SA.map_to_beats(plan, words, audio_seconds=6.0)
    gates = SA.run_gates(plan, words, beats, audio_seconds=6.0)
    entry = SA.build_scene_aligned_entry(
        scene_number=7, plan=plan, beats=beats, audio_seconds=6.0,
        audio_file="/x/scenes/07_difference_quotient_for_sine.wav",
        summary={"aligner": {"tool": "stable-ts", "version": "2.19.1", "model": "base.en",
                             "nonspeech_skip": 5.0, "failure_threshold": 0.2}},
        gates=gates,
        words_file="/x/align/07.words.json", aligned_file="/x/align/07.aligned.json")
    assert entry["narration_mode"] == "scene_aligned"
    assert entry["kind"] == "content"
    assert entry["scene_text_hash"] == plan["scene_text_hash"]
    assert entry["beat_count"] == len(beats) == len(entry["beats"])
    assert entry["audio_seconds"] == 6.0
    assert entry["alignment"]["aligner"]["tool"] == "stable-ts"
    assert entry["alignment"]["chunks"] is None
    assert entry["validation"]["status"] in ("pass", "pass_with_warnings")
    assert entry["fallback_history"] == []
    # script == space-join of beat texts (same field beats mode exposes to critic)
    assert entry["script"] == "a b c d e f"
    # no per-beat audio_file (beat WAVs do not exist in scene_aligned)
    assert all("audio_file" not in b for b in entry["beats"])
    # sum(beat durations) ~= audio_seconds (make.py asserts this)
    assert abs(sum(b["audio_seconds"] for b in entry["beats"]) - entry["audio_seconds"]) < 0.01
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python video/pipeline/_selftest_scene_align.py`
Expected: FAIL — `has no attribute 'build_scene_aligned_entry'`

- [ ] **Step 3: Write minimal implementation** — append to `scene_align.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes** — wire the call into `__main__`, run.

Run: `python video/pipeline/_selftest_scene_align.py`
Expected: PASS — update final print to `OK scene_align self-test (Tasks 1-6)`

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/scene_align.py video/pipeline/_selftest_scene_align.py
git commit -m "feat(video/scene_align): aligner seam + schema-2 entry assembly (Task 6)"
```

---

## Task 7: Fallback ladder module (`scene_fallback.py`, §7)

**Files:**
- Create: `video/pipeline/scene_fallback.py`
- Modify: `video/pipeline/_selftest_scene_align.py` (add a ladder-policy test with injected outcomes)
- Reference: design §7 (four rungs, lazy, verify-before-overwrite, retry budget)

The ladder is a policy function that, given a scene plan + a set of injectable "attempt" callables, walks the rungs until one passes gates, recording `fallback_history`. Keeping the rung callables injectable lets the selftest drive the whole ladder to rungs 3/4 with zero API and zero model.

- [ ] **Step 1: Write the failing test** — append to `_selftest_scene_align.py`:

```python
from pipeline import scene_fallback as FB  # add near the top import


def test_fallback_ladder_stops_at_first_pass():
    calls = []
    def rung(name, status):
        def _f(ctx):
            calls.append(name)
            return {"status": status, "entry": {"narration_mode": "scene_aligned", "rung": name}}
        return _f
    # rung spec is (name, billed, callable): billedness is explicit up front (no name
    # convention, no self-report). arbiter is free; resynth/chunk billed; beats exempt.
    result = FB.run_ladder(
        scene_id="s",
        rungs=[("arbiter", False, rung("arbiter", "fail")),
               ("resynth", True, rung("resynth", "pass")),
               ("chunk", True, rung("chunk", "pass")),
               ("beats", False, rung("beats", "pass"))],
        budget=FB.RetryBudget(max_billed=2))
    assert calls == ["arbiter", "resynth"]           # stopped at first pass
    assert result["entry"]["rung"] == "resynth"
    assert [h["rung"] for h in result["history"]] == ["arbiter", "resynth"]


def test_fallback_ladder_budget_stops_before_overrun():
    def billed_fail(ctx):
        return {"status": "fail", "entry": None}
    def beats_ok(ctx):
        return {"status": "pass", "entry": {"narration_mode": "beats"}}
    result = FB.run_ladder(
        scene_id="s",
        rungs=[("resynth", True, billed_fail), ("chunk", True, billed_fail),
               ("beats", False, beats_ok)],      # beats is the always-allowed terminal
        budget=FB.RetryBudget(max_billed=1))     # only 1 billed retry allowed
    # resynth consumes the 1 billed retry and fails; chunk is billed but over budget -> skipped;
    # ladder falls straight to the beats terminal (free, always runs).
    assert result["entry"]["narration_mode"] == "beats"
    assert any(h.get("skipped_over_budget") for h in result["history"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python video/pipeline/_selftest_scene_align.py`
Expected: FAIL — `No module named 'pipeline.scene_fallback'`

- [ ] **Step 3: Write minimal implementation** — create `video/pipeline/scene_fallback.py`:

```python
"""Per-scene fallback ladder for scene-level alignment (design §7).

Rungs, in order: (1) small.en arbiter re-align [free], (2) resynthesize the scene
once [billed], (3) sentence-chunk resynth+merge [billed], (4) beat-level TTS
[billed, but the always-available terminal]. Lazy: a rung runs only when reached.
Verify-before-overwrite and the billed-retry budget are enforced here so the
billed-cost surface stays in one auditable place (CLAUDE.md).

Rung callables are injected (tts.py wires the real ones; the selftest injects
outcome stubs), so the ladder policy is testable with zero API and zero model.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class RetryBudget:
    """max_billed = extra billed calls allowed across rungs 2-3 for THIS scene
    (design §7: the consent quote pre-approves <=2/scene). Rung 4 (beats) is the
    guaranteed terminal and is always allowed even at budget 0."""
    max_billed: int = 2
    spent: int = 0

    def can_bill(self) -> bool:
        return self.spent < self.max_billed


Rung = Callable[[dict[str, Any]], dict[str, Any]]  # ctx -> {"status", "entry", "reason"?}


def run_ladder(*, scene_id: str, rungs: list[tuple[str, bool, Rung]], budget: RetryBudget,
               ctx: dict[str, Any] | None = None) -> dict[str, Any]:
    """Walk rungs until one returns status=="pass". Each rung is (name, billed,
    callable) -- billedness is DECLARED, not inferred by name or self-reported. A
    billed rung is skipped (recorded) when the budget is exhausted; the non-billed
    'beats' terminal is never skipped. The chosen entry carries the full history in
    its fallback_history (design §7). Returns {"entry", "history"}."""
    ctx = ctx or {}
    history: list[dict[str, Any]] = []
    for name, billed, rung in rungs:
        if billed and not budget.can_bill():
            history.append({"rung": name, "skipped_over_budget": True})
            continue
        result = rung(ctx)
        if billed:
            budget.spent += 1
        history.append({"rung": name, "status": result.get("status"),
                        "reason": result.get("reason")})
        if result.get("status") == "pass":
            entry = result["entry"]
            if isinstance(entry, dict):     # stamp the path taken onto the manifest entry
                entry.setdefault("fallback_history", [])
                entry["fallback_history"] = list(entry["fallback_history"]) + history
            return {"entry": entry, "history": history}
    # Exhausted without a pass -> caller must ensure the last rung is the free beats
    # terminal (always passes); reaching here means a wiring bug -- surface it.
    return {"entry": history[-1].get("entry") if history else None, "history": history}
```

> Implementation note for Task 8 wiring: pass rungs in order `("arbiter", False, ...), ("resynth", True, ...), ("chunk", True, ...), ("beats", False, ...)`; the `beats` rung re-uses `tts.synthesize_scene`'s existing beat path and always returns `status="pass"`, so the exhaustion branch is a safety net, not a normal exit. Because `run_ladder` already stamps `fallback_history` onto the winning entry, Task 8 does NOT re-wrap it.

- [ ] **Step 4: Run test to verify it passes** — wire the two calls into `__main__`, run.

Run: `python video/pipeline/_selftest_scene_align.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/scene_fallback.py video/pipeline/_selftest_scene_align.py
git commit -m "feat(video/scene_fallback): per-scene fallback ladder with retry budget (Task 7)"
```

---

## Task 8: `tts.py` — `--unit`, scene code path, reuse matrix, schema 2

**Files:**
- Modify: `video/pipeline/tts.py` (`parse_args` ~259, `synthesize_scene` ~424, `main`/manifest ~547, reuse helpers ~313)
- Reference: design §3 (freshness matrix), §10 (`--unit auto` allowlist), §8 (storage layout)

- [ ] **Step 1: Write the failing test** — create `video/pipeline/_selftest_tts_unit.py`:

```python
"""Offline self-test for tts.py scene-unit routing (no API, no model).
Run: python video/pipeline/_selftest_tts_unit.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import tts  # noqa: E402

SCENE_ALLOWLIST = tts.SCENE_UNIT_TEMPLATES


def test_unit_auto_allowlist_is_batch1():
    # design §10 batch 1: four templates go scene; derivation/theorem_proof stay beats
    assert {"definition_math", "graph", "callout", "recap_cards"} <= SCENE_ALLOWLIST
    assert "derivation" not in SCENE_ALLOWLIST
    assert "theorem_proof" not in SCENE_ALLOWLIST


def test_resolve_unit_for_scene():
    assert tts.resolve_unit("beat", {"template": "graph"}) == "beat"
    assert tts.resolve_unit("scene", {"template": "derivation"}) == "scene"   # explicit override
    assert tts.resolve_unit("auto", {"template": "graph"}) == "scene"
    assert tts.resolve_unit("auto", {"template": "derivation"}) == "beat"
    assert tts.resolve_unit("auto", {}) == "beat"                             # unknown template -> conservative


def test_atomic_write_and_promote(tmp=Path(__file__).parent / "_tmp_tts_unit"):
    from pipeline import atomicio
    tmp.mkdir(exist_ok=True)
    p = tmp / "sub" / "x.json"
    atomicio.atomic_write_json(p, {"a": 1})
    assert p.exists() and not p.with_name(p.name + ".tmp").exists()   # tmp cleaned by os.replace
    import json as _j
    assert _j.loads(p.read_text(encoding="utf-8"))["a"] == 1
    src = tmp / "y.tmp"; src.write_text("hi", encoding="utf-8")
    atomicio.promote(src, tmp / "y.txt")
    assert (tmp / "y.txt").read_text(encoding="utf-8") == "hi" and not src.exists()


def test_scene_reuse_ok_freshness(tmp=Path(__file__).parent / "_tmp_tts_unit"):
    import argparse
    from pipeline.audio import write_pcm_wav, silence_pcm
    from pipeline import scene_align as SA
    tmp.mkdir(exist_ok=True)
    plan = SA.build_scene_plan({"id": "s", "say": "a b {show m.0} c d"})
    wav = tmp / "07_s.wav"; write_pcm_wav(wav, silence_pcm(4.0))
    args = argparse.Namespace(model="mimo-v2.5-tts", style="STY", aligner_model="base.en", voice="Dean")
    prior = {"backend": "mimo", "model": "mimo-v2.5-tts", "voice": "Dean", "style": "STY",
             "scene_text_hash": plan["scene_text_hash"], "audio_file": str(wav),
             "audio_seconds": round(__import__("pipeline.audio", fromlist=["wav_duration"]).wav_duration(wav), 3)}
    assert tts.scene_reuse_ok(prior, plan, wav, backend_name="mimo", voice="Dean", args=args) is True
    # each WAV-affecting field, mutated, flips the verdict to False:
    assert tts.scene_reuse_ok({**prior, "scene_text_hash": "X"}, plan, wav, backend_name="mimo", voice="Dean", args=args) is False
    assert tts.scene_reuse_ok({**prior, "voice": "Mia"}, plan, wav, backend_name="mimo", voice="Dean", args=args) is False
    assert tts.scene_reuse_ok(None, plan, wav, backend_name="mimo", voice="Dean", args=args) is False
    # aligner-model change does NOT force resynth (§3: reuse WAV, re-align only) -> still True
    assert tts.scene_reuse_ok(prior, plan, wav, backend_name="mimo", voice="Dean",
                              args=argparse.Namespace(**{**vars(args), "aligner_model": "small.en"})) is True


if __name__ == "__main__":
    test_unit_auto_allowlist_is_batch1()
    test_resolve_unit_for_scene()
    test_atomic_write_and_promote()
    test_scene_reuse_ok_freshness()
    print("OK tts unit-routing self-test (Task 8)")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python video/pipeline/_selftest_tts_unit.py`
Expected: FAIL — `has no attribute 'SCENE_UNIT_TEMPLATES'`

- [ ] **Step 3: Write minimal implementation** in `tts.py`:

(a) Near the module constants (after `MIMO_STYLE`, ~line 51), add:
```python
# design §10 batch-1 rollout allowlist for --unit auto. Recalibrate/extend to
# derivation+theorem_proof (batch 2) after the first real deck's gates are checked.
SCENE_UNIT_TEMPLATES = frozenset({"definition_math", "graph", "callout", "recap_cards"})


def resolve_unit(unit: str, scene: dict[str, Any]) -> str:
    """beat|scene forced; auto -> scene iff the scene's template is in the batch-1
    allowlist, else beat (conservative default for unknown/heavy templates)."""
    if unit in ("beat", "scene"):
        return unit
    return "scene" if scene.get("template") in SCENE_UNIT_TEMPLATES else "beat"
```

(b) In `parse_args` (after `--reuse-existing`, ~line 273), add:
```python
    parser.add_argument("--unit", choices=("beat", "scene", "auto"), default="auto",
                        help="TTS synthesis unit: beat (legacy), scene (scene-level + "
                             "forced alignment), auto (scene for batch-1 templates, else beat)")
    parser.add_argument("--skip-qa", action="store_true",
                        help="skip the whisper-timestamped ASR QA probe (design §6)")
    parser.add_argument("--aligner-model", default="base.en")
    parser.add_argument("--aligner-device", default="cpu")
    parser.add_argument("--fallback-budget", type=int, default=2,
                        help="max extra BILLED retries per scene across ladder rungs 2-3 "
                             "(design §7; the consent quote pre-approves this)")
```

(c) Create `video/pipeline/atomicio.py` (design §3 atomic writes — no more "old words.json + new WAV"):
```python
"""Atomic file writes: write to <name>.tmp then os.replace (atomic on the same
filesystem). Used for words/aligned/manifest JSON and promoting a verified scene WAV."""
from __future__ import annotations
import json, os
from pathlib import Path
from typing import Any


def atomic_write_text(path: Path, text: str, *, encoding: str = "utf-8") -> None:
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding=encoding)
    os.replace(tmp, path)


def atomic_write_json(path: Path, obj: Any) -> None:
    atomic_write_text(path, json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def promote(tmp_path: Path, final_path: Path) -> None:
    """Move a verified temp artifact onto its canonical path (verify-before-overwrite):
    the canonical file is replaced only after validation passed."""
    Path(final_path).parent.mkdir(parents=True, exist_ok=True)
    os.replace(tmp_path, final_path)
```

(d) Make the top-level manifest schema 2 and `write_manifest` atomic:
```python
    manifest: dict[str, Any] = {"schema": 2, "storyboard": str(args.storyboard.resolve()), ...}
```
```python
def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    from pipeline.atomicio import atomic_write_json
    atomic_write_json(path, manifest)
```

(e) Build the scene-level reuse index in `main` (the existing per-beat `build_reuse_index` cannot serve scene_aligned, which has NO per-beat `audio_file` — BLOCKING per design §3) and thread it to `synthesize_scene` as a new kwarg `scene_reuse_index` (the beat path ignores it):
```python
def build_scene_reuse_index(manifest: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    """Reuse index keyed by scene_id, from a prior manifest's scene_aligned entries.
    Carries what §3 freshness needs so TTS can be skipped when only downstream
    (reveal/beat-count) changed. (Per-beat build_reuse_index stays for the beat path.)"""
    if not manifest:
        return {}
    shared = {k: manifest.get(k) for k in ("backend", "model", "voice", "style")}
    out: dict[str, dict[str, Any]] = {}
    for s in manifest.get("scenes", []):
        if s.get("narration_mode") != "scene_aligned":
            continue
        out[s.get("scene_id")] = {
            **shared,
            "scene_text_hash": s.get("scene_text_hash"),
            "audio_file": s.get("audio_file"),
            "audio_seconds": s.get("audio_seconds"),
        }
    return out


def scene_reuse_ok(prior: dict[str, Any] | None, plan: dict[str, Any], scene_wav: Path,
                   *, backend_name: str, voice: str, args: argparse.Namespace) -> bool:
    """True iff the prior scene WAV can be reused WITHOUT re-synthesis (§3 rows 2-3):
    backend/model/voice/style + scene_text_hash unchanged, WAV present with a matching
    duration. Deliberately does NOT check the aligner: §3 says an aligner change reuses
    the WAV and only re-aligns -- which the sync path (_align_and_gate on the existing
    WAV) does for free. Reveal/beat-count-only edits also pass here; the re-map handles
    them. A True here means 'skip TTS'; the caller still always re-aligns+re-validates."""
    from pipeline.timing import SYNC_TOLERANCE_SECONDS
    if not prior:
        return False
    if (prior.get("backend"), prior.get("model"), prior.get("voice"), prior.get("style")) != \
       (backend_name, args.model, voice, args.style):
        return False
    if prior.get("scene_text_hash") != plan["scene_text_hash"]:
        return False
    if not scene_wav.exists():
        return False
    return abs(wav_duration(scene_wav) - float(prior.get("audio_seconds") or 0.0)) <= SYNC_TOLERANCE_SECONDS
```

(f) In `synthesize_scene`, after the `kind != "content"` early return, branch on unit. Refactor the existing beat body into `_synthesize_scene_beats(...)` (unchanged logic, same return) and add the scene path:
```python
    unit = resolve_unit(getattr(args, "unit", "beat"), scene)
    if unit == "beat":
        return _synthesize_scene_beats(backend=backend, meta=meta, scene=scene,
            scene_number=scene_number, output_dir=output_dir, args=args, reuse_index=reuse_index)
    return _synthesize_scene_aligned(backend=backend, meta=meta, scene=scene,
        scene_number=scene_number, output_dir=output_dir, args=args,
        reuse_index=reuse_index, scene_reuse_index=scene_reuse_index)
```
`_synthesize_scene_aligned` (new; §3 storage + verify-before-overwrite + §7 ladder). The WAV is synthesized to a **temp path** and promoted onto the canonical path ONLY after gates pass, so a prior good WAV is never clobbered by a bad re-synth (`reuse_index` is only used by the beats fallback rung):
```python
def _synthesize_scene_aligned(*, backend, meta, scene, scene_number, output_dir, args,
                              reuse_index, scene_reuse_index):
    from pipeline import scene_align as SA, scene_fallback as FB
    voice = args.voice or default_voice_for_model(args.model, meta)
    scene_id = scene["id"]
    plan = SA.build_scene_plan(scene)
    scenes_dir, align_dir = output_dir / "scenes", output_dir / "align"
    scene_wav = scenes_dir / f"{scene_number:02d}_{scene_id}.wav"
    words_file = align_dir / f"{scene_number:02d}_{scene_id}.words.json"
    aligned_file = align_dir / f"{scene_number:02d}_{scene_id}.aligned.json"

    # (§3) reuse: if the existing WAV is fresh, skip TTS and just re-map+re-validate (free).
    if scene_reuse_ok(scene_reuse_index.get(scene_id), plan, scene_wav,
                      backend_name=backend.name, voice=voice, args=args):
        entry = _align_and_gate(plan, scene_wav, scene_number, words_file, aligned_file,
                                args, audio_file=scene_wav, promote_from=None)
        if entry["validation"]["status"] in ("pass", "pass_with_warnings"):
            return entry   # else fall through to resynth

    # synthesize to a TEMP wav, align+gate, promote onto scene_wav only if gates pass.
    tmp_wav = scene_wav.with_name(scene_wav.name + ".tmp")
    _synth_scene_wav(backend, plan, tmp_wav, voice, args)           # 1 TTS call (billed for mimo)
    entry = _align_and_gate(plan, tmp_wav, scene_number, words_file, aligned_file,
                            args, audio_file=scene_wav, promote_from=tmp_wav)
    if entry["validation"]["status"] in ("pass", "pass_with_warnings"):
        return entry

    # gates FAILED -> fallback ladder (§7). Keep tmp_wav: the arbiter rung re-aligns
    # THIS audio with small.en (rung 1 does not re-synthesize). scene_wav stays untouched.
    budget = FB.RetryBudget(max_billed=getattr(args, "fallback_budget", 2))
    ctx = {"plan": plan, "primary_wav": tmp_wav, "scene_wav": scene_wav,
           "scene_number": scene_number, "words_file": words_file, "aligned_file": aligned_file}
    rungs = _build_fallback_rungs(backend, meta, scene, scene_number, output_dir, args, plan, reuse_index)
    result = FB.run_ladder(scene_id=scene_id, rungs=rungs, budget=budget, ctx=ctx)
    tmp_wav.unlink(missing_ok=True)   # clean the primary temp after the ladder settles
    return result["entry"]
```

> Task-8 remaining wiring functions (each gets a focused `--backend mock` test in `_selftest_tts_unit.py`, with `SA.align_scene` monkeypatched to return linear words so no model is needed):
> - `_synth_scene_wav(backend, plan, out_path, voice, args)` — one `backend.synthesize(TTSRequest(text=plan["transcript"], model=args.model, voice=voice, style=args.style))` call; writes PCM to `out_path` via `write_pcm_wav` (already writing to a `.tmp` path, so no extra atomic wrapper needed for the WAV — promotion is the atomic step).
> - `_align_and_gate(plan, wav, scene_number, words_file, aligned_file, args, *, audio_file, promote_from, aligner_model=None)` — `model = aligner_model or args.aligner_model` (the arbiter rung passes `aligner_model="small.en"`; everyone else inherits the `base.en` default). `res = SA.align_scene(wav, plan, model=model, device=args.aligner_device)` → `SA.map_to_beats(plan, res["words"], wav_duration(wav), multi=res["multi"])` → `SA.run_gates(...)` → unless `--skip-qa`, run the whisper-timestamped probe and `SA.qa_diff(SA.tokenize(plan["transcript"]), asr_tokens, [w["probability"] for w in res["words"]], weak_spans=SA.boundary_weak_spans(beats))`, folding a `qa_diff` FAIL into the gate status. **Only on PASS** (`status in {pass, pass_with_warnings}`): if `promote_from`, `atomicio.promote(promote_from, audio_file)`, then `atomicio.atomic_write_json` the `{summary,words,segments}` words_file (its `summary.aligner.model` is whatever model ran — so an arbiter win persists `small.en`, which make.py does NOT re-check) and the aligned_file (design §3 "verify before overwrite" — canonical artifacts are written together, after validation). On gate FAIL it returns the entry with `validation.status=="fail"` WITHOUT promoting the WAV or writing canonical words/aligned (the ladder produces the real artifacts). Returns `SA.build_scene_aligned_entry(...)` either way.
> - `_build_fallback_rungs(backend, meta, scene, scene_number, output_dir, args, plan, reuse_index)` returns the four `(name, billed, callable)` rungs in order `("arbiter", False, ...)`, `("resynth", True, ...)`, `("chunk", True, ...)`, `("beats", False, ...)`; each rung callable takes the `ctx` dict from `_synthesize_scene_aligned`. The **arbiter** rung (free) re-runs `_align_and_gate` on `ctx["primary_wav"]` with `aligner_model="small.en"` — it does NOT re-synthesize; two models agreeing on the boundaries raises FA confidence. `resynth`/`chunk` (billed) synthesize to their OWN temp paths and promote only on pass. The `beats` rung calls the existing `_synthesize_scene_beats(..., reuse_index=reuse_index)` and returns `{"status": "pass", "entry": <that entry>}` (its entry already has `narration_mode=="beats"`); `run_ladder` stamps `fallback_history` onto whichever entry wins.

(g) In `main`, build the scene reuse index next to the existing per-beat one and thread it through:
```python
    reuse_index = build_reuse_index(prior_manifest)                 # existing (beat path)
    scene_reuse_index = build_scene_reuse_index(prior_manifest)     # new (scene path)
    ...
    synthesize_scene(..., reuse_index=reuse_index, scene_reuse_index=scene_reuse_index)
```
Add `scene_reuse_index: dict[str, Any] | None = None` to `synthesize_scene`'s signature (default `{}` inside); the beat path never reads it, so the signature change is backward-compatible.

- [ ] **Step 4: Run test to verify it passes**

Run: `python video/pipeline/_selftest_tts_unit.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/tts.py video/pipeline/atomicio.py video/pipeline/_selftest_tts_unit.py
git commit -m "feat(video/tts): --unit scene path, schema-2 manifest, scene reuse + atomic writes (Task 8)"
```

---

## Task 9: `make.py` consumer migration (4 relaxations + validate branch + guards)

**Files:**
- Modify: `video/make.py` (`_beat_durations:164`, `_validate_reuse_manifest:176`, `_audit_render_sync:367`, `compose:506`, main entry ~676)
- Reference: design §9 (7-site migration table)

- [ ] **Step 1: Write the failing test** — create `video/pipeline/_selftest_make_scene_aligned.py`:

```python
"""Offline self-test for make.py scene_aligned consumers (no render, no ffmpeg).
Run: python video/pipeline/_selftest_make_scene_aligned.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import make  # noqa: E402  (video/ is on sys.path via _bootstrap in make)

def _scene_aligned_entry():
    return {"scene_number": 7, "scene_id": "s", "kind": "content",
            "narration_mode": "scene_aligned", "audio_file": "/x/07_s.wav",
            "audio_seconds": 6.0, "scene_text_hash": "h",
            "script": "a b c d e f", "beat_count": 3,
            "beats": [{"index": i + 1, "id": f"beat_{i+1:02d}", "reveal": None,
                       "text": "a b", "text_hash": "t", "audio_seconds": 2.0,
                       "start_seconds": 2.0 * i, "end_seconds": 2.0 * (i + 1),
                       "word_start": 2 * i, "word_end": 2 * (i + 1),
                       "boundary": {"prob": 0.8, "interpolated": False}} for i in range(3)]}

def test_beat_durations_accepts_scene_aligned():
    m = {"scenes": [_scene_aligned_entry()]}
    assert make._beat_durations(m) == {"s": [2.0, 2.0, 2.0]}

def test_schema_guard_rejects_future_schema():
    try:
        make._check_manifest_schema({"schema": 3, "scenes": []})
    except SystemExit:
        pass
    else:
        raise AssertionError("expected SystemExit on schema>2")
    make._check_manifest_schema({"schema": 2, "scenes": []})   # ok
    make._check_manifest_schema({"scenes": []})                # missing -> schema 1, ok

def test_validate_scene_aligned_freshness(tmp=Path(__file__).parent / "_tmp_make_sa"):
    # a FRESH scene_aligned entry passes _validate_scene_aligned with NO problems, and
    # each mutated freshness field produces exactly one problem (and NO per-beat
    # audio_file is ever required).
    from pipeline.narration import parse_say
    from pipeline.timing import text_hash
    from pipeline.audio import write_pcm_wav, silence_pcm, wav_duration
    tmp.mkdir(exist_ok=True)
    say = "a b. {show m.0} c d."
    scene = {"id": "s", "kind": "content", "say": say}
    beats = parse_say(say)
    transcript = " ".join(b.text for b in beats if b.text).strip()
    wav = tmp / "07_s.wav"; write_pcm_wav(wav, silence_pcm(4.0))
    words_f = tmp / "07_s.words.json"; words_f.write_text("{}", encoding="utf-8")
    aligned_f = tmp / "07_s.aligned.json"; aligned_f.write_text("{}", encoding="utf-8")
    def entry():
        return {"scene_id": "s", "narration_mode": "scene_aligned", "audio_file": str(wav),
                "audio_seconds": round(wav_duration(wav), 3), "scene_text_hash": text_hash(transcript),
                "beats": [{"reveal": b.reveal, "text_hash": text_hash(b.text)} for b in beats],
                "alignment": {"words_file": str(words_f), "aligned_file": str(aligned_f),
                              "aligner": {"model": "base.en"}},
                "validation": {"status": "pass"}}
    p = []; make._validate_scene_aligned("s", scene, beats, entry(), p); assert p == [], p
    # each mutation -> at least one problem, no per-beat audio_file demanded. (Aligner
    # model is intentionally NOT checked by make.py -- it is tts.py's freshness job.)
    for mutate in (
        lambda e: e.update(scene_text_hash="STALE"),
        lambda e: e.update(audio_file="/nope.wav"),
        lambda e: e["alignment"].update(words_file="/nope.json"),
        lambda e: e.__setitem__("validation", {"status": "fail"}),
        lambda e: e["beats"][1].update(reveal="m.999"),
    ):
        e = entry(); mutate(e); p = []; make._validate_scene_aligned("s", scene, beats, e, p)
        assert p, f"expected a freshness problem after mutation, got none"
    # aligner-model change must NOT be flagged by make.py (whatever produced the alignment renders)
    e = entry(); e["alignment"]["aligner"]["model"] = "small.en"
    p = []; make._validate_scene_aligned("s", scene, beats, e, p); assert p == [], p

if __name__ == "__main__":
    test_beat_durations_accepts_scene_aligned()
    test_schema_guard_rejects_future_schema()
    test_validate_scene_aligned_freshness()
    print("OK make scene_aligned self-test (Task 9)")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python video/pipeline/_selftest_make_scene_aligned.py`
Expected: FAIL — `_beat_durations` returns `{}` (only accepts `"beats"`), or `AttributeError: _check_manifest_schema`

- [ ] **Step 3: Write minimal implementation** in `make.py`:

(a) `_beat_durations` (line 167) — accept both modes:
```python
        if s.get("narration_mode") in ("beats", "scene_aligned"):
```
(b) `_audit_render_sync` (line 379) — accept both + add the sum assertion:
```python
        if not entry or entry.get("narration_mode") not in ("beats", "scene_aligned") or video is None:
            continue
        audio_seconds = float(entry.get("audio_seconds") or 0.0)
        if entry.get("narration_mode") == "scene_aligned":
            beat_sum = sum(float(b.get("audio_seconds") or 0.0) for b in entry.get("beats", []))
            if abs(beat_sum - audio_seconds) > SYNC_TOLERANCE_SECONDS:
                fatals.append(f"{sid}: sum(beat durations)={beat_sum:.3f}s != audio_seconds={audio_seconds:.3f}s "
                              "(hand-edited manifest?)")
```
(c) `compose` (line 511) — accept both:
```python
        if s.get("narration_mode") in ("beats", "scene_aligned") and s.get("audio_file"):
```
(d) `_validate_reuse_manifest` (line 196) — replace the flat `!= "beats"` reject with a per-mode branch. The `scene_aligned` branch fully delegates to a self-contained helper and `continue`s (so the existing beats-only per-beat loop is untouched):
```python
        mode = entry.get("narration_mode")
        if mode not in ("beats", "scene_aligned"):
            problems.append(f"{sid}: manifest narration_mode={mode!r}, expected 'beats' or 'scene_aligned'")
            continue
        if mode == "scene_aligned":
            _validate_scene_aligned(sid, scene, beats, entry, problems)   # new helper below
            continue
        # ... existing beats-mode checks (beat count, reveal, text_hash, scene+beat WAVs) unchanged ...
```
`_validate_scene_aligned` (new, self-contained — does NOT require any per-beat `audio_file`, since scene_aligned beats have none):
```python
def _validate_scene_aligned(sid: str, scene: dict, beats: list, entry: dict, problems: list) -> None:
    """Render-time freshness for a reused scene_aligned entry (design §3/§9 row 2):
    scene WAV present + duration matches, alignment artifacts present, validation passed,
    scene_text_hash + per-beat reveal/text_hash unchanged. NO per-beat audio_file
    (scene_aligned stores one scene WAV). Deliberately does NOT check the aligner model:
    make.py has no aligner config to compare against, and aligner freshness (§3 row 3) is
    tts.py's job -- whatever model produced the persisted alignment (base.en normally,
    small.en if the arbiter won) is fine to render."""
    manifest_beats = entry.get("beats", [])
    if len(manifest_beats) != len(beats):
        problems.append(f"{sid}: beat count changed ({len(manifest_beats)} manifest, {len(beats)} storyboard)")
        return
    transcript = " ".join(b.text for b in beats if b.text).strip()
    if entry.get("scene_text_hash") != text_hash(transcript):
        problems.append(f"{sid}: scene_text_hash stale (storyboard text changed) -> resynthesize")
    af = entry.get("audio_file"); ap = Path(af) if af else None
    audio_seconds = float(entry.get("audio_seconds") or 0.0)
    if ap is None or not ap.exists():
        problems.append(f"{sid}: scene audio file missing: {af!r}")
    elif abs(wav_duration(ap) - audio_seconds) > SYNC_TOLERANCE_SECONDS:
        problems.append(f"{sid}: scene audio WAV duration differs from manifest")
    if audio_seconds <= 0.0:
        problems.append(f"{sid}: scene audio_seconds is not positive")
    align = entry.get("alignment") or {}
    for key in ("words_file", "aligned_file"):
        p = align.get(key)
        if not p or not Path(p).exists():
            problems.append(f"{sid}: alignment {key} missing: {p!r}")
    if (entry.get("validation") or {}).get("status") not in ("pass", "pass_with_warnings"):
        problems.append(f"{sid}: validation.status={ (entry.get('validation') or {}).get('status')!r }")
    for i, (b, mb) in enumerate(zip(beats, manifest_beats), start=1):
        if mb.get("reveal") != b.reveal:
            problems.append(f"{sid} beat {i:02d}: reveal changed (manifest={mb.get('reveal')!r}, storyboard={b.reveal!r})")
        stored = mb.get("text_hash")
        if stored and stored != text_hash(b.text):
            problems.append(f"{sid} beat {i:02d}: text_hash changed")
```
(e) Add `_check_manifest_schema` and call it right after loading a reuse manifest (~line 676):
```python
def _check_manifest_schema(manifest: dict) -> None:
    schema = int(manifest.get("schema", 1))
    if schema > 2:
        raise SystemExit(f"audio manifest schema {schema} is newer than this make.py supports "
                         "(max 2); upgrade the pipeline.")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python video/pipeline/_selftest_make_scene_aligned.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add video/make.py video/pipeline/_selftest_make_scene_aligned.py
git commit -m "feat(video/make): scene_aligned consumers + reuse branch + schema guard (Task 9)"
```

---

## Task 10: `critic.py` — accept `scene_aligned` in `plan_frames`

**Files:**
- Modify: `video/pipeline/critic.py:175`
- Reference: design §9 (row 7); `beats[]`/`script` shape identical, so zero further change.

- [ ] **Step 1: Write the failing test** — create `video/pipeline/_selftest_critic_scene_aligned.py`:

```python
"""Run: python video/pipeline/_selftest_critic_scene_aligned.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import critic  # noqa: E402

def test_plan_frames_includes_scene_aligned():
    storyboard = {"meta": {}, "scenes": [{"id": "s", "title": "T"}]}
    manifest = {"scenes": [{"scene_id": "s", "scene_number": 7,
                            "narration_mode": "scene_aligned", "script": "hello",
                            "beats": [{"index": 1, "id": "beat_01", "reveal": None,
                                       "text": "hello", "end_seconds": 1.0}]}]}
    plan = critic.plan_frames(storyboard, manifest, "all", per="scene")
    assert len(plan) == 1 and plan[0]["scene_id"] == "s"

if __name__ == "__main__":
    test_plan_frames_includes_scene_aligned()
    print("OK critic scene_aligned self-test (Task 10)")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python video/pipeline/_selftest_critic_scene_aligned.py`
Expected: FAIL — `plan` is empty (entry skipped by `!= "beats"`)

- [ ] **Step 3: Write minimal implementation** — `critic.py:175`:
```python
        if entry is None or entry.get("narration_mode") not in ("beats", "scene_aligned"):
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python video/pipeline/_selftest_critic_scene_aligned.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/critic.py video/pipeline/_selftest_critic_scene_aligned.py
git commit -m "feat(video/critic): plan_frames accepts scene_aligned (Task 10)"
```

---

## Task 11: Integration — mock scene-WAV path end to end (offline)

**Files:**
- Create: `video/pipeline/_selftest_scene_align_integration.py`
- Reference: design §11 (integration bullet: mock scene WAV + linear words → tts scene path → make render/compose; ladder driven by injected gate failures)

- [ ] **Step 1: Write the failing test** — the integration test actually DRIVES `tts.synthesize_scene`'s scene path (not a hand-built entry): it stubs the aligner + `_synth_scene_wav` (so no model, no API, controlled WAV length), runs the scene path to a real schema-2 entry with promoted WAV + written words/aligned files, then feeds that entry to `make._validate_reuse_manifest` (fresh → no raise), `make._audit_render_sync` (stubbed probe → True, incl. the `sum(beats)≈audio_seconds` assertion), and finally forces a gate FAIL with `--fallback-budget 0` to prove the ladder demotes the scene to `narration_mode=="beats"`.

```python
"""Offline end-to-end: tts.synthesize_scene scene path (stubbed aligner + synth) ->
schema-2 entry -> make.py reuse-validation + render-sync + ladder demotion. No API,
no whisper model, no ffmpeg. Run: python video/pipeline/_selftest_scene_align_integration.py"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import scene_align as SA           # noqa: E402
from pipeline import tts                          # noqa: E402
from pipeline.audio import write_pcm_wav, silence_pcm, wav_duration  # noqa: E402
import make                                       # noqa: E402

SCENE = {"id": "slope_equals_height", "kind": "content", "template": "graph",
         "say": "First point. {show g.0} Second point here now. {show g.1} Third and final point."}
META = {"id": "demo_mimo"}

def _args(**over):
    base = dict(backend="mock", model="mimo-v2.5-tts", voice="Dean", style="STY", unit="scene",
                skip_qa=True, aligner_model="base.en", aligner_device="cpu",
                fallback_budget=2, empty_beat_seconds=0.45, reuse_existing=False)
    base.update(over); return argparse.Namespace(**base)

def _fake_align(wav_path, plan, **kw):
    dur = wav_duration(wav_path); toks = SA.tokenize(plan["transcript"]); step = dur / max(len(toks), 1)
    words = [{"word": t, "start": round(i * step, 3), "end": round(min((i + 1) * step, dur), 3),
              "probability": 0.85} for i, t in enumerate(toks)]
    summary = {"aligner": {"tool": "stable-ts", "version": "stub", "model": kw.get("model", "base.en"),
               "nonspeech_skip": 5.0, "failure_threshold": 0.2}, "word_count": len(words),
               "beat_boundary_in_multi_token_word": [], "prob_min": 0.85, "prob_mean": 0.85,
               "low_prob_words": 0, "low_prob_runs": []}
    return {"words": words, "summary": summary, "segments": [], "multi": {}}

def _fake_synth(seconds):
    def _f(backend, plan, out_path, voice, args):
        write_pcm_wav(out_path, silence_pcm(seconds))
    return _f

def test_tts_scene_path_and_make_consumers(tmp=Path(__file__).parent / "_tmp_integ"):
    out = tmp / "audio_mimo"
    saved = (SA.align_scene, tts._synth_scene_wav, make._probe_duration)
    SA.align_scene, tts._synth_scene_wav = _fake_align, _fake_synth(12.0)
    try:
        entry = tts.synthesize_scene(backend=tts.MockTTSBackend(0.45), meta=META, scene=SCENE,
            scene_number=7, output_dir=out, args=_args(), reuse_index={}, scene_reuse_index={})
        assert entry["narration_mode"] == "scene_aligned"
        assert entry["validation"]["status"] in ("pass", "pass_with_warnings")
        assert Path(entry["audio_file"]).exists()                        # WAV promoted
        assert not Path(entry["audio_file"] + ".tmp").exists()           # temp gone
        assert Path(entry["alignment"]["words_file"]).exists()
        assert Path(entry["alignment"]["aligned_file"]).exists()
        manifest = {"schema": 2, "deck_id": META["id"], "backend": "mimo", "model": "mimo-v2.5-tts",
                    "voice": "Dean", "style": "STY", "scenes": [entry]}
        make._check_manifest_schema(manifest)
        make._validate_reuse_manifest(META, [SCENE], manifest)           # raises if stale
        make._probe_duration = lambda p: 1.0 + entry["audio_seconds"] + 1.0
        assert make._audit_render_sync([SCENE], manifest,
                                       {SCENE["id"]: Path(entry["audio_file"])}, lead=1.0) is True
    finally:
        SA.align_scene, tts._synth_scene_wav, make._probe_duration = saved

def test_gate_fail_demotes_to_beats(tmp=Path(__file__).parent / "_tmp_integ2"):
    out = tmp / "audio_mimo"
    saved = (SA.align_scene, tts._synth_scene_wav, SA.run_gates)
    SA.align_scene, tts._synth_scene_wav = _fake_align, _fake_synth(12.0)
    SA.run_gates = lambda *a, **k: {"status": "fail", "failures": ["forced"], "warnings": [], "metrics": {}}
    try:
        # budget 0: resynth/chunk skipped over budget; arbiter (free, also fails) -> beats terminal
        entry = tts.synthesize_scene(backend=tts.MockTTSBackend(0.45), meta=META, scene=SCENE,
            scene_number=7, output_dir=out, args=_args(fallback_budget=0),
            reuse_index={}, scene_reuse_index={})
        assert entry["narration_mode"] == "beats"
        assert any(h.get("rung") == "beats" for h in entry.get("fallback_history", []))
    finally:
        SA.align_scene, tts._synth_scene_wav, SA.run_gates = saved

if __name__ == "__main__":
    test_tts_scene_path_and_make_consumers()
    test_gate_fail_demotes_to_beats()
    print("OK scene_align integration self-test (Task 11)")
```

- [ ] **Step 2: Run test to verify it fails** — before the Task 8 scene path exists, `tts.synthesize_scene` has no scene branch (`resolve_unit`/`_synth_scene_wav`/`_synthesize_scene_aligned` missing).

Run: `python video/pipeline/_selftest_scene_align_integration.py`
Expected: FAIL — `AttributeError` on `tts._synth_scene_wav` / no scene path.

- [ ] **Step 3: Make it pass** — no new production code beyond Tasks 1-10; fix any wiring gaps the real scene-path integration surfaces (this is the task's purpose — e.g. the arbiter-needs-primary-WAV handoff and the `fallback_history` stamping are both exercised here).

- [ ] **Step 4: Run all selftests green**

Run:
```bash
python video/pipeline/_selftest_scene_align.py
python video/pipeline/_selftest_tts_unit.py
python video/pipeline/_selftest_make_scene_aligned.py
python video/pipeline/_selftest_critic_scene_aligned.py
python video/pipeline/_selftest_scene_align_integration.py
```
Expected: five `OK ...` lines.

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/_selftest_scene_align_integration.py
git commit -m "test(video/scene_align): offline end-to-end integration (Task 11)"
```

---

## Task 12: Real-data regression — identical to the experiment's stable-ts output

**Files:**
- Create: `video/pipeline/_regression_scene_align.py` (guarded: skips cleanly if the experiment WAVs/model are absent)
- Reference: design §11 (real-data regression: production module must reproduce the experiment line); `RESULTS-2026-07-05.md` (three scenes: 197/197, 209/209, 99/99)

This is the one task that touches the real aligner. It is **still zero-cost** (local CPU, WAVs already on disk from the approved experiment; no API). It proves `scene_align.align_scene` + `map_to_beats` reproduce `run_stable_ts_align.py` + `map_alignment_to_beats.py`.

> **Regression target — use the `_stable` files, verified on disk 2026-07-05.** Each scene dir has BOTH `aligned_beats.json` (the whisper-timestamped/free-ASR timeline; for `difference_quotient_for_sine` that is only 185 words) AND `aligned_beats_stable.json` (the stable-ts timeline, 197 words). The stable-ts word list is `words_stable_ts.json` (`{summary, words, segments}`). Compare against the **`_stable`** artifacts, never `aligned_beats.json`.

- [ ] **Step 1: Write the regression harness** — for each of the three experiment scenes, if `video/output/experiments/forced_alignment_dean/<scene>/scene_dean.wav` and `words_stable_ts.json` exist: build the plan from `ch03_trig_derivatives_mimo.yml`, run `res = SA.align_scene(wav, plan)`, and assert:
>   1. `res["words"]` equals `words_stable_ts.json["words"]` — same token sequence, same `start`/`end` (3 dp), same `probability`.
>   2. `res["summary"]` matches `words_stable_ts.json["summary"]` on the port-relevant fields — `word_count`, `prob_min`, `prob_mean`, `low_prob_words`, `low_prob_runs`, `beat_boundary_in_multi_token_word` (ignore `aligner.version` drift only if the installed stable-ts differs).
>   3. `SA.map_to_beats(plan, res["words"], wav_duration(wav), multi=res["multi"])` start/end equals `aligned_beats_stable.json["beats"]` start/end to 3 dp.
>
> Skip with a printed notice if inputs are missing (keeps CI/new-env green without the model). This is a faithful-port check, not a whole-file byte compare (the persisted file adds `segments`; a byte compare would be brittle to stable-ts internal fields).

- [ ] **Step 2: Run it**

Run: `python video/pipeline/_regression_scene_align.py`
Expected: `OK regression: 3/3 scenes match stable-ts output` (or `SKIP: experiment WAVs not on disk` on a machine without them).

- [ ] **Step 3: If mismatch** — diff the token lists / summary fields; the port must reproduce the experiment. Fix `scene_align.py` (not the test) until it matches. Re-run.

- [ ] **Step 4: Commit**

```bash
git add video/pipeline/_regression_scene_align.py
git commit -m "test(video/scene_align): real-data regression vs experiment stable-ts output (Task 12)"
```

---

## Task 13: Docs + batch-1 mock dry-run acceptance (offline §10 gate ①)

**Files:**
- Modify: `video/DESIGN.md` (manifest v2 contract §), `video/RUNBOOK-mimo-narration-route.md` (lock-gated scene synth step), `video/REBUILD_STATUS.md` (landing record under a new 2026-07-05 sub-node), `ENVIRONMENT.md` (confirm ⑤c aligner pin referenced by `scene_align`)
- Reference: design §3/§8/§10; CLAUDE.md (cross-conversation knowledge → git docs; landing record in `REBUILD_STATUS.md`)

- [ ] **Step 1: DESIGN.md** — add the schema-2 manifest contract: top-level `schema`, the three `narration_mode` values, the scene_aligned entry shape (beats[] + alignment + validation + fallback_history), and the freshness matrix (verbatim from design §3). State that schema-1 manifests need no migration.

- [ ] **Step 2: RUNBOOK-mimo-narration-route.md** — insert the scene-level synth step after narration lock + NFA: `tts.py --unit auto` (or `--unit scene`) for the deck, note that pre-lock iteration stays `make.py --backend mock` (beats, zero cost), and that the billed quote must include the §7 fallback retry budget.

- [ ] **Step 3: REBUILD_STATUS.md** — record what landed (module, consumers, gates, tests), the durable lessons, and that Phase B (billed A/B) is pending a quote. Follow the existing 2026-07-05 node's style.

- [ ] **Step 4: Offline acceptance gate ① (design §10)** — run the §3.1 deck through mock to prove render/sync/compose are green with the new consumer code (mock always writes `"beats"`, so this confirms no regression on the untouched path):
```bash
python video/make.py --storyboard video/storyboards/ch03_trig_derivatives_mimo.yml --backend mock --quality low
```
Expected: `[sync] beat timing clean` (or only within-frame advisories) and `[done] ...mp4`. Zero cost.

- [ ] **Step 5: Full selftest sweep + doctor**
```bash
for t in scene_align tts_unit make_scene_aligned critic_scene_aligned scene_align_integration; do python video/pipeline/_selftest_$t.py; done
python video/pipeline/_regression_scene_align.py
python tools/doctor.py --json   # forced-alignment probe still PASS/WARN as before
```

- [ ] **Step 6: Commit**

```bash
git add video/DESIGN.md video/RUNBOOK-mimo-narration-route.md video/REBUILD_STATUS.md ENVIRONMENT.md
git commit -m "docs(video): schema-2 manifest contract, lock-gated scene synth, landing record (Task 13)"
```

**END OF PHASE A — everything above is offline and zero-cost.**

---

## Task 14 (PHASE B — BILLED, STOP FOR QUOTE FIRST)

> **Do not start Task 14 without an explicit cost-approval from the user** (CLAUDE.md 付費 API). At the end of Task 13, present a quote: backend `mimo`, model `mimo-v2.5-tts`, the §3.1 deck's batch-1 scene count and their transcript word/second estimate, plus the §7 fallback retry budget (≤2 extra billed calls per scene, pre-approved by the same quote). Only after consent:

- [ ] **Step 1:** `python video/pipeline/tts.py --storyboard video/storyboards/ch03_trig_derivatives_mimo.yml --backend mimo --unit auto` (batch-1 templates go scene; derivation/theorem_proof stay beats). Watch `fallback_history` for any scene that needed rungs 2-3; stop and report if a scene exhausts its retry budget.
- [ ] **Step 2:** `python video/make.py --storyboard ... --reuse-audio --quality high` → 1080p render; confirm `[sync]` clean and compose routes scene_aligned scenes through `_mux_content`.
- [ ] **Step 3:** A/B vs the existing beat-level MiMo cut (voice continuity, reveal sync) — VLM frame critique via `critic.py`, extract stills at beat boundaries.
- [ ] **Step 4:** Recalibrate `scene_align.GATES` against the real deck's metrics (design §5/§10 acceptance clause); record the recalibration in `REBUILD_STATUS.md`.
- [ ] **Step 5:** If A/B is clean, extend `SCENE_UNIT_TEMPLATES` to include `derivation`/`theorem_proof` (batch 2) — one constant edit + a re-run under a fresh quote.

---

## Self-Review (spec coverage vs design §§1-14)

- §2 data flow → Tasks 1-8 (plan→align→explode→map→gates→qa→entry) + 14 (render/compose). ✓
- §3 schema 2 + freshness matrix → Task 6 (entry), Task 8 (top-level schema + reuse), Task 9 (`_validate_scene_aligned`), Task 13 (DESIGN.md). ✓
- §4 module inventory → `scene_align.py` (T1-6), `scene_fallback.py` (T7), `tts.py` (T8), `make.py` (T9), `critic.py` (T10), selftests (T1-11). ✓ (Design put the ladder inside tts.py at ~150 lines; this plan factors it into `scene_fallback.py` to isolate the billed-retry budget — a decomposition improvement, surfaced here per Karpathy §1.)
- §5 gates (every row) → Task 4 `GATES` + `run_gates`, one RED→GREEN test per FAIL row; interior-low-prob WARN-only covered. ✓
- §6 ASR probe grading (3 rows) → Task 5 `qa_diff`. ✓
- §7 fallback ladder (4 rungs, lazy, budget, verify-before-overwrite) → Task 7 + Task 8 wiring. ✓
- §8 storage layout → Task 8 (`scenes/`, `align/*.words.json`/`*.aligned.json`), atomic writes. ✓
- §9 7-site migration → Tasks 9 (5 make sites) + 10 (critic); `synth_scene` mock untouched, `_warn_short_beats` auto via `_beat_durations`. ✓
- §10 rollout/acceptance → Task 8 (`--unit auto` allowlist), Task 13 step 4 (offline gate ①), Task 14 (billed gate ②). ✓
- §11 test plan (selftest / integration / real-data regression) → Tasks 1-6, 11, 12. ✓
- §12 risks → aligner isolated behind `align_scene` (T6, swap-to-CTC), ladder per-scene blast radius (T7), QA probe (T5), GATES central (T4). ✓
- §13 rejected alternatives → encoded as gate choices (no scene-avg confidence gate; index-verify not 5% delta). ✓
- §14 defaults → reveal=first-word onset (T3), QA on by default `--skip-qa` (T8), aligner `base.en` (T6/T8). ✓

**Placeholder scan:** no TBD/TODO; every code step shows real code ported from the read experiment scripts or the read consumer functions. **Type consistency:** `build_scene_plan`→`plan["beats"][].word_start`; `explode_to_plan_tokens`→`(words, multi)`; `map_to_beats(plan, words, audio_seconds, *, multi)`→shared beats[] shape + `boundary`; `run_gates(plan, words, beats, audio_seconds)`→`{status,failures,warnings,metrics}`; `qa_diff(plan_tokens, asr_tokens, fa_probs, *, weak_spans, ...)`→`{verdict,clusters}`; `align_scene(...)`→`{words, summary, segments, multi}`; `build_scene_aligned_entry(...)`→schema-2 entry; consumed consistently across Tasks 6-11. ✓

**One decomposition deviation from the design, flagged for the reviewer:** the design estimated the fallback ladder as ~150 lines inside `tts.py`; this plan puts it in a separate `scene_fallback.py` so the billed-retry budget lives in one auditable place and the ladder policy is unit-testable with injected rungs. Net line count is the same; the seam is cleaner. If the reviewer prefers the design's single-file layout, collapse Task 7 into Task 8.

---

## Codex adversarial review dispositions (2026-07-05, read-only, standing consent)

The first draft of this plan was reviewed by Codex (`gpt-5.5/xhigh`, read-only) before any code. Verdict on the draft: *not safe to execute as written*. All 12 findings verified against source/disk (not blindly accepted); dispositions below. This revision incorporates every accepted fix.

| # | Sev | Finding | Disposition |
|---|-----|---------|-------------|
| B1 | BLOCKING | `run_gates` missed non-overlap; also "missing trailing-silence FAIL gate" | **Split.** Non-overlap gate **added** (design §5 says "non-monotonic *or* overlap") + RED test. Trailing-silence gate **rejected** — not in design; §5's char-share row deliberately excludes tail silence, so the design tolerates it. Added a positive test that trailing silence does not fail. |
| B2 | BLOCKING | `align_scene` dropped `low_prob_words`/`low_prob_runs`/`segments`; "bit-identical" unprovable | **Accepted.** `align_scene` now returns `{words, summary, segments, multi}` with the experiment's full summary shape (verified on disk); Task 12 compares words+summary+beat timeline and the "bit-identical" wording is narrowed to "faithful-port match". |
| B3 | BLOCKING | Regression compared `aligned_beats.json` (185-word ASR) not `aligned_beats_stable.json` (197-word stable-ts) | **Accepted, verified on disk.** Task 12 now targets the `_stable` artifacts + `words_stable_ts.json`. |
| B4 | BLOCKING | `fallback_history` discarded (`run_ladder(...)["entry"]`) | **Accepted.** `run_ladder` now stamps `fallback_history` onto the winning entry. |
| B5 | BLOCKING | Atomic writes/verify-before-overwrite only prose | **Accepted.** New `atomicio.py` (`atomic_write_json`/`promote`); `write_manifest` made atomic; scene WAV synthesized to a temp path and promoted only after gates pass; fallback rungs write to own temps. |
| B6 | BLOCKING | Per-beat reuse index can't serve scene_aligned (no per-beat WAV) | **Accepted.** New scene-level `build_scene_reuse_index` + `scene_reuse_ok`, threaded through `main`→`synthesize_scene`. |
| B7 | BLOCKING | `qa_diff`: insertions get empty FA window; `bool(gate_failures)` is global | **Accepted.** Rewrote to a per-cluster window (insertions use a neighbourhood) and local `weak_spans` overlap, not a global flag; added `boundary_weak_spans` + insertion/co-location RED tests. |
| B8 | BLOCKING | Task 11 test didn't test what its prose claimed | **Accepted.** Rewrote as a real end-to-end: drives `tts.synthesize_scene` scene path with a stubbed aligner, then `_validate_reuse_manifest` + `_audit_render_sync` + ladder→beats demotion. |
| A1 | ADVISORY | `map_to_beats` boundary prob dropped when `word_start==0` after a reveal-only beat | **Accepted.** `0 <= wi` (was `0 < wi`). |
| A2 | ADVISORY | Task 3 reveal-only test passed for the wrong reason (`parse_say` drops a single leading `{show}`) | **Accepted.** Test uses consecutive `{show}` to create a real leading reveal-only beat + asserts the next boundary's prob. |
| A3 | ADVISORY | Fallback billed-rung contract contradictory (dead code) | **Accepted.** Rung spec is now explicit `(name, billed, callable)`; no name convention, no self-report. |
| A4 | ADVISORY | Task 9 test didn't cover `_validate_scene_aligned` | **Accepted.** `_validate_scene_aligned` made a concrete function + a freshness test that mutates each field and asserts a problem. |

**Codex-confirmed sound:** tokenizer + explode-by-char-share match the experiment (punctuation drops, last-token end snap); no `narration_mode=="beats"` consumer site was missed beyond the reuse-index issue (B6).

### Regression re-review (round 2, 2026-07-05, read-only)

A scoped Codex re-review of the revised plan confirmed the B1 pushback is legitimate (no trailing-silence FAIL gate exists in design §5) and that all 11 accepted fixes are correctly applied — but found **one new BLOCKING the revision itself introduced**, now fixed:

| # | Sev | Finding | Disposition |
|---|-----|---------|-------------|
| R2-1 | BLOCKING | Arbiter aligner-model threading inconsistent: `_align_and_gate` had no `aligner_model` param but the arbiter rung passed `aligner_model="small.en"` (→ TypeError); and if forced through, a persisted `small.en` alignment would be rejected as stale by make.py's hardcoded-`base.en` check. | **Fixed, and fixed the same-root second bug.** `_align_and_gate` now takes `aligner_model=None` (→ `aligner_model or args.aligner_model`); the arbiter passes `small.en` cleanly. **make.py `_validate_scene_aligned` no longer checks the aligner model at all** (make.py has no aligner config; aligner freshness is tts.py's job) — so an arbiter-`small.en` manifest renders fine. And **`scene_reuse_ok` no longer checks the aligner** either (§3: an aligner change reuses the WAV + re-aligns for free, it must NOT force a billed resynth). Tests updated: aligner-model change now asserts *reusable/valid*, not stale. |
| R2-2 | NIT | `_align_and_gate` sketch wrote `qa_diff(tokenize(transcript), ...)` | **Fixed** → `SA.qa_diff(SA.tokenize(plan["transcript"]), ...)`. |

**Round-2 verdict:** with R2-1/R2-2 applied and manual re-grep of all `aligner` references confirming consistency, Phase A is safe to execute. Task 1 is the next action.

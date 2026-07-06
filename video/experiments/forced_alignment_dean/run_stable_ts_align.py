"""Run transcript-constrained forced alignment (stable-ts) for one Dean experiment scene.

Unlike ``run_whisper_timestamped.py`` (free ASR: can drop/rewrite words, so word
indices may not match the plan), ``stable_whisper.align()`` is constrained to the
plan transcript: every word gets a timestamp + probability, so index-based beat
mapping is sound by construction. Output words are re-tokenized with the plan's
WORD_RE so index i here == plan word index i (verified before writing).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

VIDEO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(VIDEO_ROOT))

from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")


def load_plan(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def explode_to_plan_tokens(
    aligned_words: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[int, dict[str, Any]]]:
    """Split aligner words into plan WORD_RE tokens, interpolating timestamps.

    stable-ts words follow the transcript's whitespace (e.g. ``sum-to-product.``
    is one word) while the plan tokenizes with WORD_RE (``sum-to`` + ``product``).
    Both read the same transcript text, so exploding each aligner word with
    WORD_RE reproduces the plan token sequence exactly.

    Punctuation-only aligner words (e.g. a standalone ``--``) yield no token;
    their span survives as an inter-word gap, and beat starts always sit on the
    next real word's onset, so no reveal timing is lost by dropping them.

    Returns ``(tokens, multi)`` where ``multi`` maps token index -> parent info
    for tokens that came from a multi-token parent word (their timestamps are
    interpolated by character share, i.e. estimated rather than measured).
    """
    out: list[dict[str, Any]] = []
    multi: dict[int, dict[str, Any]] = {}
    for word in aligned_words:
        tokens = WORD_RE.findall(word["text"])
        if not tokens:
            continue  # punctuation-only word (e.g. standalone "--")
        for ordinal in range(len(tokens)) if len(tokens) > 1 else ():
            multi[len(out) + ordinal] = {
                "parent": word["text"].strip(),
                "ordinal": ordinal,
                "tokens": len(tokens),
            }
        start, end = float(word["start"]), float(word["end"])
        span = max(end - start, 0.0)
        total_chars = sum(len(t) for t in tokens)
        cursor = start
        for token in tokens:
            share = (len(token) / total_chars) if total_chars else 1.0 / len(tokens)
            token_end = min(cursor + span * share, end)
            out.append(
                {
                    "word": token,
                    "start": round(cursor, 3),
                    "end": round(token_end, 3),
                    "probability": word.get("probability"),
                }
            )
            cursor = token_end
        out[-1]["end"] = end  # avoid rounding drift on the last token
    return out, multi


def low_prob_runs(words: list[dict[str, Any]], threshold: float, min_run: int) -> list[list[int]]:
    runs: list[list[int]] = []
    current: list[int] = []
    for i, word in enumerate(words):
        prob = word.get("probability")
        if prob is not None and prob < threshold:
            current.append(i)
        else:
            if len(current) >= min_run:
                runs.append(current)
            current = []
    if len(current) >= min_run:
        runs.append(current)
    return runs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--audio", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--model", default="base.en")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--language", default="en")
    parser.add_argument("--prob-threshold", type=float, default=0.5)
    parser.add_argument("--min-run", type=int, default=2)
    parser.add_argument("--nonspeech-skip", type=float, default=5.0,
                        help="stable-ts default; skip nonspeech sections longer than this")
    parser.add_argument("--failure-threshold", type=float, default=0.2,
                        help="abort if this fraction of words fails to align")
    args = parser.parse_args()

    try:
        import stable_whisper
    except ImportError as exc:
        raise SystemExit(
            "stable-ts is not installed; run `python -m pip install --upgrade stable-ts`."
        ) from exc

    plan = load_plan(args.plan)
    audio = (args.audio or (args.plan.resolve().parent / "scene_dean.wav")).resolve()
    output = (args.output or (args.plan.resolve().parent / "words_stable_ts.json")).resolve()
    transcript = plan.get("transcript") or ""
    if not transcript:
        raise SystemExit("plan has no transcript")
    print(
        f"[stable-ts] scene={plan['scene_id']} audio={audio} "
        f"model={args.model} device={args.device}",
        flush=True,
    )

    model = stable_whisper.load_model(args.model, device=args.device)
    # remove_instant_words must stay False: dropping zero-duration words would
    # break the 1:1 plan-token indexing that beat mapping depends on.
    result = model.align(
        str(audio),
        transcript,
        language=args.language,
        nonspeech_skip=args.nonspeech_skip,
        failure_threshold=args.failure_threshold,
        remove_instant_words=False,
    )
    if result is None:
        raise SystemExit(
            f"stable-ts aborted: more than {args.failure_threshold:.0%} of words "
            "failed to align (audio likely does not match the transcript)"
        )
    raw = result.to_dict()
    aligned_words = [
        {
            "text": word.get("word", ""),
            "start": word.get("start"),
            "end": word.get("end"),
            "probability": word.get("probability"),
        }
        for segment in raw.get("segments", [])
        for word in segment.get("words", [])
    ]
    words, multi = explode_to_plan_tokens(aligned_words)

    # A beat boundary inside a multi-token parent word means its start time is
    # interpolated, not measured -- report it so validation can decide.
    boundary_in_multi = [
        {"beat": beat["id"], **multi[int(beat["word_start"])]}
        for beat in plan.get("beats", [])
        if int(beat["word_start"]) in multi and multi[int(beat["word_start"])]["ordinal"] > 0
    ]

    plan_tokens = WORD_RE.findall(transcript)
    if [w["word"] for w in words] != plan_tokens:
        for i, (got, want) in enumerate(zip((w["word"] for w in words), plan_tokens)):
            if got != want:
                raise SystemExit(
                    f"token mismatch at index {i}: aligned={got!r} plan={want!r}; "
                    "index-based beat mapping would be unsound"
                )
        raise SystemExit(
            f"token count mismatch: aligned={len(words)} plan={len(plan_tokens)}"
        )

    probs = [w["probability"] for w in words if w.get("probability") is not None]
    runs = low_prob_runs(words, args.prob_threshold, args.min_run)
    summary = {
        "aligner": {
            "tool": "stable-ts",
            "version": stable_whisper.__version__,
            "model": args.model,
            "nonspeech_skip": args.nonspeech_skip,
            "failure_threshold": args.failure_threshold,
        },
        "word_count": len(words),
        "beat_boundary_in_multi_token_word": boundary_in_multi,
        "prob_min": round(min(probs), 3) if probs else None,
        "prob_mean": round(sum(probs) / len(probs), 3) if probs else None,
        "low_prob_words": sum(1 for p in probs if p < args.prob_threshold),
        "low_prob_runs": [
            {
                "indices": [run[0], run[-1]],
                "start": words[run[0]]["start"],
                "end": words[run[-1]]["end"],
                "text": " ".join(words[i]["word"] for i in run),
                "probs": [round(words[i]["probability"], 3) for i in run],
            }
            for run in runs
        ],
    }
    output.write_text(
        json.dumps({"summary": summary, "words": words, "segments": raw.get("segments", [])},
                   indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"[stable-ts] wrote {output}")
    print(
        f"[stable-ts] words={summary['word_count']} plan_words={plan.get('word_count')} "
        f"prob_min={summary['prob_min']} prob_mean={summary['prob_mean']} "
        f"low_prob_words={summary['low_prob_words']} low_prob_runs={len(runs)}",
        flush=True,
    )
    for run in summary["low_prob_runs"]:
        print(f"  LOW-PROB RUN {run['start']:.2f}-{run['end']:.2f}s: {run['text']!r} probs={run['probs']}")
    for item in boundary_in_multi:
        print(
            f"  WARN {item['beat']} starts inside multi-token word {item['parent']!r} "
            f"(token {item['ordinal'] + 1}/{item['tokens']}); start time is interpolated"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

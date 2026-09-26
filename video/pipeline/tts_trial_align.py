"""Offline Chinese scene alignment for a MiMo trial, never an audio lock.

Run with the global Python that has stable-ts installed. Only explicit local
Whisper weights are accepted; this tool never synthesizes or downloads audio.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import sys
import time
import unicodedata
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.timing import text_hash
from pipeline.narration import parse_say

SMALL_SHA256 = "9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794"
ALIGN_OPTIONS = {"language": "zh", "nonspeech_skip": 5.0, "regroup": False,
                 "failure_threshold": 0.2, "remove_instant_words": False, "verbose": False}


class TrialAlignmentError(ValueError):
    pass


def sha256_file(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def spoken_chars(text: str) -> str:
    """Remove only spacing/punctuation, retaining letters, digits and symbols.

    No case-folding, transliteration, simplified/traditional conversion or fuzzy
    matching: repeated words remain distinguished by their sequential positions.
    """
    return "".join(c for c in text if not c.isspace() and not unicodedata.category(c).startswith("P"))


def map_cues(beats: list[dict], transcript: str, words: list[dict], duration: float) -> list[dict]:
    """Map exact character spans to native stable-ts word onsets.

    A cue inside a native word is an explicitly estimated interpolation, never a
    measured per-character timestamp. First/last scene boundaries follow policy.
    """
    if not math.isfinite(duration) or duration <= 0:
        raise TrialAlignmentError("invalid WAV duration")
    target = spoken_chars(transcript)
    if not target or "".join(spoken_chars(b["text"]) for b in beats) != target:
        raise TrialAlignmentError("beat/transcript character sequence mismatch")
    spans, cursor, previous_end = [], 0, 0.0
    for index, word in enumerate(words):
        start, end = float(word["start"]), float(word["end"])
        if not all(math.isfinite(v) for v in (start, end)) or not 0 <= start <= end <= duration + 1e-6:
            raise TrialAlignmentError(f"word {index}: timestamps outside WAV bounds")
        if start + 1e-6 < previous_end:
            raise TrialAlignmentError(f"word {index}: non-monotonic/overlapping timestamps")
        previous_end = end
        chars = spoken_chars(word["word"])
        if not chars:
            continue
        if target[cursor:cursor + len(chars)] != chars:
            raise TrialAlignmentError(f"word {index}: exact character sequence mismatch at {cursor}")
        spans.append((cursor, cursor + len(chars), index, word))
        cursor += len(chars)
    if cursor != len(target):
        raise TrialAlignmentError("aligned words do not cover the complete transcript")

    out, cursor = [], 0
    for index, beat in enumerate(beats):
        quality = {"human_verified_100ms": False, "estimated": False}
        if index == 0:
            onset = 0.0
            quality["source"] = "scene_start_policy"
        elif cursor == len(target):
            onset = duration
            quality["source"] = "scene_end_policy"
        else:
            lo, hi, wi, word = next(s for s in spans if s[0] <= cursor < s[1])
            offset = cursor - lo
            onset = float(word["start"])
            quality.update(source="stable_ts_word_onset", word_index=wi,
                           parent_word=word["word"], parent_start=word["start"],
                           parent_end=word["end"], probability=word.get("probability"))
            if offset:
                onset += (float(word["end"]) - onset) * offset / (hi - lo)
                quality.update(source="character_share_within_word", estimated=True)
            if word["start"] == word["end"]:
                quality.update(source="stable_ts_zero_duration_boundary", estimated=True)
        length = len(spoken_chars(beat["text"]))
        out.append({"index": index + 1, "id": f"beat_{index + 1:02d}",
                    "text": beat["text"], "text_hash": text_hash(beat["text"]),
                    "reveal": beat.get("reveal"), "char_start": cursor, "char_end": cursor + length,
                    "start_seconds": round(onset, 6), "boundary": quality})
        cursor += length
    for index, beat in enumerate(out):
        end = out[index + 1]["start_seconds"] if index + 1 < len(out) else duration
        if end < beat["start_seconds"]:
            raise TrialAlignmentError("non-monotonic beat cues")
        if spoken_chars(beat["text"]) and end <= beat["start_seconds"]:
            raise TrialAlignmentError("unresolved zero-duration spoken beat")
        beat.update(end_seconds=round(end, 6), audio_seconds=round(end - beat["start_seconds"], 6))
    return out


def checked_file(root: Path, relative: str, digest: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise TrialAlignmentError(f"missing or external trial file: {relative}")
    if sha256_file(path) != digest:
        raise TrialAlignmentError(f"SHA256 mismatch: {relative}")
    return path


def wav_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as audio:
        return audio.getnframes() / audio.getframerate()


def validate_trial(trial_dir: Path) -> tuple[dict, dict]:
    """Verify the complete immutable ledger before loading any model."""
    from pipeline.tts_scene_trial import read_plan, read_ledger, wav_info
    stored = read_json(trial_dir / "plan.json")
    plan = read_plan(trial_dir, stored["plan_snapshot_hash"])
    _, completed = read_ledger(trial_dir, plan)
    if set(completed) != {r["scene_id"] for r in plan["requests"]}:
        raise TrialAlignmentError("all planned scenes must have successful verified takes before alignment")
    for request in plan["requests"]:
        receipt = completed[request["scene_id"]]
        if receipt["plan_snapshot_hash"] != plan["plan_snapshot_hash"]:
            raise TrialAlignmentError("receipt belongs to another plan")
        info = receipt["files"]["raw_audio"]
        audio = checked_file(trial_dir, info["path"], info["sha256"])
        if wav_info(audio.read_bytes()) != receipt["audio"]:
            raise TrialAlignmentError("WAV measurements disagree with receipt")
        segment = request["segment"]
        parsed = [(b.text, b.reveal) for b in parse_say(segment["source_say"])]
        if parsed != [(b["text"], b["reveal"]) for b in segment["cues"]]:
            raise TrialAlignmentError("cues disagree with parse_say")
    return plan, completed


def align_trial(trial_dir: Path, output_dir: Path, model_path: Path) -> dict:
    trial_dir, output_dir, model_path = trial_dir.resolve(), output_dir.resolve(), model_path.expanduser().resolve()
    plan, completed = validate_trial(trial_dir)
    if not model_path.is_file() or sha256_file(model_path) != SMALL_SHA256:
        raise TrialAlignmentError("explicit local multilingual small.pt is missing or has an invalid SHA256")
    if output_dir == trial_dir or output_dir.is_relative_to(trial_dir):
        raise TrialAlignmentError("export directory must be separate from immutable trial directory")
    manifest_path = output_dir / "manifest.json"
    if manifest_path.exists() and read_json(manifest_path).get("trial_plan_hash") != plan["plan_snapshot_hash"]:
        raise TrialAlignmentError("output directory already belongs to a different trial")

    import stable_whisper
    import torch
    torch.set_num_threads(8)
    model = None
    by_id = {r["scene_id"]: r for r in plan["requests"]}
    scenes, report = [], []
    for number, source in enumerate(plan["source_snapshot"]["scenes"], start=1):
        scene_id = source["id"]
        if scene_id not in by_id:
            scenes.append({"scene_number": number, "scene_id": scene_id,
                           "kind": source.get("kind", "silent"), "duration": source["duration"]})
            continue
        request, receipt = by_id[scene_id], completed[scene_id]
        segment = request["segment"]
        file_info = receipt["files"]["raw_audio"]
        audio = checked_file(trial_dir, file_info["path"], file_info["sha256"])
        duration = wav_seconds(audio)
        stem = f"{number:02d}_{scene_id}"
        cache = output_dir / "_alignment" / f"{stem}.json"
        identity = {"plan_hash": plan["plan_snapshot_hash"], "take_id": receipt["take_id"],
                    "request_hash": request["request_hash"], "audio_sha256": file_info["sha256"],
                    "transcript": segment["text"], "model_sha256": SMALL_SHA256,
                    "stable_ts_version": stable_whisper.__version__, "options": ALIGN_OPTIONS}
        saved = read_json(cache) if cache.exists() else None
        reused = bool(saved and saved.get("identity") == identity)
        if reused:
            raw = saved["raw"]
            if saved.get("raw_sha256") != hashlib.sha256(json.dumps(raw, sort_keys=True).encode()).hexdigest():
                raise TrialAlignmentError(f"corrupt alignment cache: {scene_id}")
        else:
            if model is None:
                # Supplying a verified file path, not a model name, disables download lookup.
                model = stable_whisper.load_model(str(model_path), device="cpu")
            started = time.monotonic()
            result = model.align(str(audio), segment["text"], **ALIGN_OPTIONS)
            if result is None:
                raise TrialAlignmentError(f"stable-ts aborted for {scene_id}; no export or TTS retry")
            raw = result.to_dict()
            saved = {"identity": identity, "raw": raw,
                     "raw_sha256": hashlib.sha256(json.dumps(raw, sort_keys=True).encode()).hexdigest(),
                     "elapsed_seconds": round(time.monotonic() - started, 3)}
            write_json(cache, saved)
        words = [w for s in raw.get("segments", []) for w in s.get("words", [])]
        beats = map_cues(segment["cues"], segment["text"], words, duration)
        for cue, beat in zip(segment["cues"], beats):
            beat["cue_id"] = cue["cue_id"]
        estimated = [b["cue_id"] for b in beats if b["boundary"]["estimated"]]
        low_probability = [b["cue_id"] for b in beats
                           if b["boundary"].get("probability") is not None
                           and b["boundary"]["probability"] < 0.35]
        zero_words = [i for i, w in enumerate(words) if spoken_chars(w["word"]) and w["start"] == w["end"]]
        report.append({"scene_id": scene_id, "audio_seconds": duration, "reused_alignment": reused,
                       "zero_duration_word_indices": zero_words, "estimated_cues": estimated,
                       "low_probability_cues": low_probability,
                       "cues": beats, "audio_locked": False,
                       "status": "trial_requires_human_cue_review", "raw_alignment": cache.name})
        scenes.append({"scene_number": number, "scene_id": scene_id, "kind": "content",
                       "narration_mode": "scene_aligned", "audio_file": f"scenes/{stem}.wav",
                       "audio_seconds": duration, "scene_text_hash": text_hash(segment["text"]),
                       "script": segment["text"], "beat_count": len(beats), "beats": beats,
                       "take_id": receipt["take_id"], "audio_sha256": file_info["sha256"],
                       "trial": True, "audio_locked": False,
                       "validation": {"status": "trial_unverified", "estimated_cues": estimated,
                                      "human_verified_100ms": False}})
        print(f"aligned {scene_id}: {duration:.2f}s, estimated cues={len(estimated)}, reuse={reused}", flush=True)

    # Publish only after every scene maps correctly. Copy raw WAV bytes unchanged.
    for scene in scenes:
        if scene["kind"] != "content":
            continue
        info = completed[scene["scene_id"]]["files"]["raw_audio"]
        source = checked_file(trial_dir, info["path"], info["sha256"])
        target = output_dir / scene["audio_file"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if sha256_file(target) != info["sha256"]:
            raise TrialAlignmentError("exported WAV hash mismatch")
    quality = {"trial": True, "audio_locked": False, "nfa_status": "not_verified",
               "note": "試片；必要 cue 尚未人工確認至 ±0.1 秒。estimated 是估計，非量測精度。",
               "scenes": report}
    write_json(output_dir / "cue-quality.json", quality)
    manifest = {"schema": 2, "deck_id": plan["source_snapshot"]["meta"]["id"],
                "backend": "mimo", "model": plan["model"], "voice": plan["voice"],
                "language": "zh", "trial": True, "audio_locked": False, "nfa_status": "not_verified",
                "trial_plan_hash": plan["plan_snapshot_hash"], "scenes": scenes,
                "alignment_model_sha256": SMALL_SHA256, "cue_quality_file": "cue-quality.json"}
    write_json(manifest_path, manifest)
    return manifest


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trial-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model-path", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        manifest = align_trial(args.trial_dir, args.output_dir, args.model_path)
    except (OSError, ValueError, KeyError, RuntimeError, ImportError) as exc:
        parser.exit(1, f"alignment/export stopped: {exc}\n")
    print(f"trial manifest: {args.output_dir / 'manifest.json'}; audio_locked=false; scenes={len(manifest['scenes'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

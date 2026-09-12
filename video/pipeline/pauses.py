"""`pauses:` -- an authored silent hold on screen, right after a reveal.

    pauses:                      # scene-level, opt-in
      - after: step.2            # the reveal to hold on
        seconds: 1.5             # picture stays, narration does not speak

Why it lives here and not in the player: a beat's video length is already "however long
that beat's narration runs", and the player spends the remainder of it doing nothing. So a
hold is fully expressed by splicing `seconds` of silence into the scene WAV at that beat's
onset and growing the beat by the same amount -- the reveal animation then plays into
silence, the picture sits, and the sentence starts after the hold. render (beat durations),
compose (the muxed WAV) and the sidecars (timeline.json / .vtt) all read that one
transformed manifest, so nothing can drift out of step; `scene.py` needs no new concept.

The ON-DISK manifest is never rewritten: it is the TTS record of what was actually
synthesized, and the reuse/freshness contract hashes off it. This transform is applied to
the in-memory copy make.py renders and composes from.

The narration text is untouched, so a pause costs no TTS call.
"""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from pipeline import audio


def scene_pauses(scene: dict[str, Any]) -> list[tuple[str, float]]:
    """`(after, seconds)` pairs for one scene spec; empty when the field is absent."""
    out: list[tuple[str, float]] = []
    for item in scene.get("pauses") or []:
        if isinstance(item, dict) and item.get("after") and item.get("seconds"):
            out.append((str(item["after"]), float(item["seconds"])))
    return out


def _splice_silence(src: Path, dst: Path, at_seconds: list[tuple[float, float]]) -> None:
    """Copy *src* to *dst* with silence inserted at each `(offset_seconds, hold_seconds)`.

    Offsets are on the ORIGINAL timeline -- the whole file is rebuilt in one pass, so an
    earlier insert never moves a later offset.
    """
    pcm, rate, channels, width = audio.read_wav_pcm(src)
    frame = channels * width
    parts: list[bytes] = []
    cursor = 0
    for offset, hold in sorted(at_seconds):
        cut = min(max(int(round(offset * rate)), 0), len(pcm) // frame) * frame
        parts.append(pcm[cursor:cut])
        parts.append(audio.silence_pcm(hold, sample_rate=rate, channels=channels,
                                       sample_width=width))
        cursor = cut
    parts.append(pcm[cursor:])
    audio.write_pcm_wav(dst, b"".join(parts), sample_rate=rate, channels=channels,
                        sample_width=width)


def _apply_to_entry(entry: dict[str, Any], holds: list[tuple[str, float]],
                    out_dir: Path) -> dict[str, Any]:
    """One scene's manifest entry, with the holds folded into its beats + scene WAV."""
    beats = entry.get("beats") or []
    by_reveal = {b.get("reveal"): i for i, b in enumerate(beats) if b.get("reveal")}
    splices: list[tuple[float, float]] = []
    shift = 0.0
    grow: dict[int, float] = {}
    for after, seconds in holds:
        if after not in by_reveal:
            raise KeyError(
                f"{entry.get('scene_id')}: pauses[].after {after!r} names no revealed beat "
                f"(this scene reveals {sorted(k for k in by_reveal)})"
            )
        i = by_reveal[after]
        splices.append((float(beats[i]["start_seconds"]), seconds))
        grow[i] = grow.get(i, 0.0) + seconds

    for i, beat in enumerate(beats):
        beat["start_seconds"] = round(float(beat["start_seconds"]) + shift, 3)
        shift += grow.get(i, 0.0)
        beat["audio_seconds"] = round(float(beat["audio_seconds"]) + grow.get(i, 0.0), 3)
        beat["end_seconds"] = round(float(beat["end_seconds"]) + shift, 3)
    entry["audio_seconds"] = round(float(entry["audio_seconds"]) + shift, 3)

    src = Path(entry["audio_file"])
    dst = out_dir / src.name
    _splice_silence(src, dst, splices)
    entry["audio_file"] = str(dst.resolve())
    return entry


def apply_pauses(scenes: list[dict[str, Any]], manifest: dict[str, Any],
                 out_dir: Path) -> dict[str, Any]:
    """A copy of *manifest* with every scene's `pauses:` folded in. Returns the manifest
    unchanged (same object) when no selected scene declares any."""
    holds_by_scene = {s["id"]: scene_pauses(s) for s in scenes if scene_pauses(s)}
    if not holds_by_scene:
        return manifest

    out = copy.deepcopy(manifest)
    out_dir.mkdir(parents=True, exist_ok=True)
    for entry in out.get("scenes", []):
        holds = holds_by_scene.get(entry.get("scene_id"))
        if not holds or entry.get("narration_mode") not in ("beats", "scene_aligned"):
            continue
        _apply_to_entry(entry, holds, out_dir)
        total = sum(s for _a, s in holds)
        print(f"[pauses] {entry['scene_id']}: +{total:.2f}s hold "
              f"({', '.join(f'{a}+{s:g}s' for a, s in holds)})", flush=True)
    return out

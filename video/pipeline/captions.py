"""Sidecar subtitle (.vtt) + YouTube chapters (.chapters.txt) from a manifest + a
compose-emitted timeline. Manim-free; no rendering.

Timing contract (B6): a cue's absolute time is scene.start (the segment's offset in
the final concat, from the timeline) + timeline.lead_seconds (the real silence before
narration) + the beat's own start_seconds. lead_seconds is READ FROM THE TIMELINE, not
the render's hard-coded SCENE_LEAD_SECONDS, so a non-default --lead can't silently
desync the subtitles. Blank-text beats (pure reveal splits) emit no cue.

Chapters read each divider/intro scene's chapter_title -- which compose() resolved and
wrote into the timeline (NB3: neither the manifest nor the timeline scene carries a raw
title; only compose, holding the storyboard, can resolve it)."""
from __future__ import annotations

from typing import Any


def chapter_title(scene: dict, meta: dict) -> str:
    """Resolve a brand frame's chapter title (NB3 order): explicit scene title, else
    the scene tagline (an intro often has only this), else the deck title, else the id.
    Used by compose() to bake the title into the timeline before captions read it."""
    return str(scene.get("title") or scene.get("tagline")
               or meta.get("title") or scene.get("id") or "")


def beat_spans(entry: dict) -> list[tuple[str, float, float]]:
    """(text, start_seconds, end_seconds) per NON-EMPTY beat -- same shape for both
    narration modes (beats + scene_aligned both key on start_seconds/end_seconds).
    Blank-text beats and beats missing a timestamp are dropped (no blank cue)."""
    spans: list[tuple[str, float, float]] = []
    for b in entry.get("beats", []) or []:
        text = (b.get("text") or "").strip()
        start, end = b.get("start_seconds"), b.get("end_seconds")
        if not text or start is None or end is None:
            continue
        spans.append((text, float(start), float(end)))
    return spans


def _vtt_ts(seconds: float) -> str:
    seconds = max(float(seconds), 0.0)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def _chapter_ts(seconds: float) -> str:
    total = int(max(float(seconds), 0.0))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def to_vtt(manifest: dict, timeline: dict) -> str:
    """WEBVTT string: one cue per non-empty beat, absolute-timed off the timeline."""
    entries = {e.get("scene_id"): e for e in manifest.get("scenes", [])}
    lead = float(timeline.get("lead_seconds", 0.0))
    blocks: list[str] = []
    n = 0
    for sc in timeline.get("scenes", []):
        entry = entries.get(sc.get("scene_id"))
        if not entry:
            continue
        base = float(sc.get("start", 0.0)) + lead
        for text, bs, be in beat_spans(entry):
            n += 1
            blocks.append(f"{n}\n{_vtt_ts(base + bs)} --> {_vtt_ts(base + be)}\n{text}\n")
    return "WEBVTT\n\n" + "\n".join(blocks)


def to_chapters(timeline: dict) -> str:
    """YouTube chapters ('M:SS Title' / 'H:MM:SS Title'), one per divider/intro scene
    that carries a chapter_title. A 0:00 chapter is guaranteed (YouTube requires it):
    if the first titled frame starts later, prepend a 0:00 using its title."""
    marks: list[tuple[float, str]] = [
        (float(sc.get("start", 0.0)), str(sc["chapter_title"]))
        for sc in timeline.get("scenes", [])
        if sc.get("kind") in ("divider", "intro") and sc.get("chapter_title")
    ]
    if marks and marks[0][0] > 0.0:
        marks.insert(0, (0.0, marks[0][1]))
    return "".join(f"{_chapter_ts(t)} {title}\n" for t, title in marks)


def build_timeline_scene(scene: dict, meta: dict, *, start: float, end: float,
                         narration_mode: str | None) -> dict[str, Any]:
    """One timeline.scenes[] record. chapter_title is filled only for brand frames
    (divider/intro) -- that's all the chapters consumer needs (NB3)."""
    rec: dict[str, Any] = {"scene_id": scene["id"], "kind": scene.get("kind", "content"),
                           "start": round(float(start), 3), "end": round(float(end), 3),
                           "narration_mode": narration_mode}
    if rec["kind"] in ("divider", "intro"):
        rec["chapter_title"] = chapter_title(scene, meta)
    return rec

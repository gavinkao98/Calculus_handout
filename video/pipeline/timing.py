"""Shared timing constants and sync helpers for narrated video renders."""
from __future__ import annotations

import hashlib
from typing import Any

SCENE_LEAD_SECONDS = 1.0
SCENE_TAIL_SECONDS = 1.0
MIN_BEAT_HOLD_SECONDS = 0.3

SYNC_TOLERANCE_SECONDS = 0.12

STOCK_ANIM_SECONDS = {
    "fade": 0.5,
    "create": 0.8,
    "grow": 0.45,
    "slide": 0.5,
    "highlight": 1.2,
    "flash_in": 1.1,
    "write_glow": 1.4,
    "slide_pop": 0.85,
    "write": 0.7,
    # in-place rewrite (derivation `anim: transform`): morphs the previous row into this
    # one. Played by a Block CALLABLE, so this entry is the single source of its nominal
    # length -- the template reads it into Block.anim_seconds.
    "transform": 1.2,
    # `carry: to: {corner, scale}` flight (templates._apply_carry): the carried copy flies to
    # its corner on `{show <as>}`. A Block CALLABLE, like transform, so this entry is the
    # single source of its nominal length.
    "carry": 0.8,
    # two-stage elimination (derivation `anim: cancel`): 0.4 s the cancelled segments fade in
    # place, then 0.8 s the survivors morph into the new row. Same callable contract as transform.
    "cancel": 1.2,
}

# `exit: [<block id>...]` (scene.py _tail): the named blocks fade out INSIDE the
# SCENE_TAIL_SECONDS hold, so the clip length is unchanged and the sync audit sees no
# difference. Must stay below SCENE_TAIL_SECONDS.
EXIT_FADE_SECONDS = 0.5


# "圖跟旁白長" (motion primitive 6). A stock reveal is 0.45-1.4 s, which is the right
# length for "a thing appeared" and the wrong length for a 20-second beat: the §3.1 pilot
# measured that the only primitive to move the needle was the one that ran for a whole
# beat (sweep, 8.1 s), while a 1.2 s transform left the water level untouched.
BEAT_PACED_TAIL_SECONDS = 0.6    # let the finished figure sit before the beat ends
BEAT_PACED_MIN_SECONDS = 0.8     # never compress a paced animation below a readable speed


def beat_run_time(scene: Any, fallback: float) -> float:
    """How long an animation should run to last its beat.

    *fallback* is used whenever the beat length is unknown -- outside a beat (the
    end-of-scene sweep-up), or when a caller plays a block directly (selftests, the
    timed intro/outro path). Reserves BEAT_PACED_TAIL_SECONDS so the completed figure
    holds for a moment instead of finishing exactly as the narration stops.
    """
    seconds = getattr(scene, "beat_seconds", None)
    if seconds is None:
        return float(fallback)
    return max(float(seconds) - BEAT_PACED_TAIL_SECONDS, BEAT_PACED_MIN_SECONDS)


def elapsed(scene: Any) -> "float | None":
    """The renderer's own wall-clock, or None on a scene that has no renderer.

    A reveal must report what it ACTUALLY consumed, not the sum of its `run_time`s:
    manim rounds every `play` up to a whole frame, so a reveal made of several plays
    under-reports by a frame each, the beat then holds for a remainder that is too long,
    and the scene ends up longer than its narration ([sync] render/audio length).

    None (not 0.0) for "no clock here", so a caller can tell a scene at t=0 apart from
    the selftests' FakeScene and fall back to a nominal figure. See `spent`.

    PREREQUISITE: `make.py`'s `disable_caching: True`. manim's `renderer.time` advances by
    the NOMINAL `scene.duration` when an animation is served from cache and only accumulates
    per rendered frame otherwise, so the whole measure-don't-guess contract silently
    degrades to nominal values if that flag is ever turned off (DESIGN.md, "Reveal 的耗時
    回報契約").
    """
    clock = getattr(getattr(scene, "renderer", None), "time", None)
    return float(clock) if isinstance(clock, (int, float)) else None


def spent(scene: Any, t0: "float | None", nominal: float) -> float:
    """What a reveal reports to its beat: measured where there is a clock, *nominal* where
    there is none. The pipeline selftests drive reveals with a FakeScene that records
    `run_time`s but has no renderer, and they assert on the returned seconds -- so the
    nominal budget has to stay the answer off a real render."""
    t1 = elapsed(scene)
    if t0 is None or t1 is None:
        return nominal
    return t1 - t0


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def stock_animation_seconds(anim: Any) -> float | None:
    """Return known stock animation time. A callable reports the fixed length it advertises
    as `fixed_seconds` (derivation transform / cancel, the carry flight -- rollout T1-2), else
    None: a hook, sweep, `seconds: beat` or paced walk really does fill its beat."""
    if callable(anim):
        return getattr(anim, "fixed_seconds", None)
    return STOCK_ANIM_SECONDS.get(str(anim), STOCK_ANIM_SECONDS["write"])


def rendered_beat_seconds(audio_seconds: float, animation_seconds: float) -> float:
    """How long scene.py will spend on a beat after reveal + hold."""
    return animation_seconds + max(audio_seconds - animation_seconds, MIN_BEAT_HOLD_SECONDS)


def beat_extra_padding_seconds(audio_seconds: float, animation_seconds: float) -> float:
    """Extra video time inserted when a reveal animation is longer than its audio."""
    return max(rendered_beat_seconds(audio_seconds, animation_seconds) - audio_seconds, 0.0)


def expected_content_video_seconds(
    audio_seconds: float,
    *,
    lead_seconds: float = SCENE_LEAD_SECONDS,
    tail_seconds: float = SCENE_TAIL_SECONDS,
) -> float:
    return lead_seconds + audio_seconds + tail_seconds

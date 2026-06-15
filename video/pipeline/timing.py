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
}


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def stock_animation_seconds(anim: Any) -> float | None:
    """Return known stock animation time, or None for custom hook callables."""
    if callable(anim):
        return None
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

"""Generate the in-repo house audio cues for lesson videos.

The cues are deliberately simple, procedural, and sample-free. This keeps the
project's default music clear of third-party licensing and Content ID risk.
"""
from __future__ import annotations

import math
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 48_000
CHANNELS = 2
SAMPLE_WIDTH = 2
ROOT = Path(__file__).resolve().parent


def midi_to_hz(note: float) -> float:
    return 440.0 * (2.0 ** ((note - 69.0) / 12.0))


def blank(seconds: float) -> list[float]:
    return [0.0] * (int(seconds * SAMPLE_RATE) * CHANNELS)


def add_tone(
    buf: list[float],
    *,
    start: float,
    duration: float,
    freq: float,
    amp: float,
    pan: float = 0.0,
    attack: float = 0.08,
    release: float = 0.25,
    phase: float = 0.0,
    vibrato_hz: float = 0.0,
    vibrato_depth: float = 0.0,
    harmonics: tuple[tuple[float, float], ...] = ((1.0, 1.0),),
) -> None:
    start_i = max(int(start * SAMPLE_RATE), 0)
    n = max(int(duration * SAMPLE_RATE), 0)
    end_i = min(start_i + n, len(buf) // CHANNELS)
    if end_i <= start_i:
        return
    pan = max(min(pan, 1.0), -1.0)
    left_gain = math.cos((pan + 1.0) * math.pi / 4.0)
    right_gain = math.sin((pan + 1.0) * math.pi / 4.0)
    attack_n = max(int(attack * SAMPLE_RATE), 1)
    release_n = max(int(release * SAMPLE_RATE), 1)
    total = end_i - start_i

    for frame in range(start_i, end_i):
        j = frame - start_i
        t = j / SAMPLE_RATE
        if j < attack_n:
            env = j / attack_n
        elif j > total - release_n:
            env = max((total - j) / release_n, 0.0)
        else:
            env = 1.0
        env = env * env * (3.0 - 2.0 * env)
        vib = vibrato_depth * math.sin(2.0 * math.pi * vibrato_hz * t) if vibrato_hz else 0.0
        sample = 0.0
        for multiple, weight in harmonics:
            sample += weight * math.sin(2.0 * math.pi * freq * multiple * (t + vib) + phase)
        idx = frame * CHANNELS
        value = sample * amp * env
        buf[idx] += value * left_gain
        buf[idx + 1] += value * right_gain


def add_bell(
    buf: list[float],
    *,
    start: float,
    note: float,
    amp: float,
    pan: float,
    decay: float = 1.4,
) -> None:
    freq = midi_to_hz(note)
    partials = ((1.0, 1.0), (2.01, 0.33), (3.01, 0.14), (4.2, 0.08))
    for k, (multiple, weight) in enumerate(partials):
        add_tone(
            buf,
            start=start,
            duration=decay * (1.0 + 0.08 * k),
            freq=freq * multiple,
            amp=amp * weight,
            pan=pan,
            attack=0.012,
            release=decay,
            phase=0.4 * k,
        )


def add_pad_chord(
    buf: list[float],
    *,
    start: float,
    duration: float,
    notes: tuple[int, ...],
    amp: float,
) -> None:
    if not notes:
        return
    spread = (-0.45, -0.18, 0.08, 0.36, -0.32, 0.24, 0.0)
    for i, note in enumerate(notes):
        add_tone(
            buf,
            start=start,
            duration=duration,
            freq=midi_to_hz(note),
            amp=amp / len(notes),
            pan=spread[i % len(spread)],
            attack=0.9,
            release=1.6,
            vibrato_hz=0.12 + i * 0.015,
            vibrato_depth=0.0015,
            harmonics=((1.0, 1.0), (2.0, 0.22), (3.0, 0.07)),
        )


def add_noise_swell(buf: list[float], *, start: float, duration: float, amp: float) -> None:
    # Tiny deterministic pseudo-noise swell for divider motion. It is filtered by
    # averaging adjacent samples so it reads as air, not hiss.
    state = 0x1234ABCD
    start_i = max(int(start * SAMPLE_RATE), 0)
    n = max(int(duration * SAMPLE_RATE), 0)
    prev = 0.0
    for j in range(n):
        frame = start_i + j
        if frame >= len(buf) // CHANNELS:
            break
        state = (1664525 * state + 1013904223) & 0xFFFFFFFF
        raw = ((state / 0xFFFFFFFF) * 2.0 - 1.0)
        smooth = prev * 0.92 + raw * 0.08
        prev = smooth
        x = j / max(n - 1, 1)
        env = math.sin(math.pi * x) ** 2
        idx = frame * CHANNELS
        buf[idx] += smooth * amp * env * 0.55
        buf[idx + 1] += smooth * amp * env * 0.55


def apply_delay(buf: list[float], *, delay_seconds: float, feedback: float) -> None:
    delay = int(delay_seconds * SAMPLE_RATE) * CHANNELS
    if delay <= 0:
        return
    for i in range(delay, len(buf)):
        buf[i] += buf[i - delay] * feedback


def fade(buf: list[float], *, fade_in: float = 0.0, fade_out: float = 0.0) -> None:
    frames = len(buf) // CHANNELS
    in_n = int(fade_in * SAMPLE_RATE)
    out_n = int(fade_out * SAMPLE_RATE)
    for frame in range(frames):
        gain = 1.0
        if in_n and frame < in_n:
            x = frame / in_n
            gain *= x * x * (3.0 - 2.0 * x)
        if out_n and frame > frames - out_n:
            x = (frames - frame) / out_n
            gain *= max(x * x * (3.0 - 2.0 * x), 0.0)
        idx = frame * CHANNELS
        buf[idx] *= gain
        buf[idx + 1] *= gain


def write_wav(path: Path, buf: list[float], *, target_peak: float) -> None:
    peak = max(max(abs(v) for v in buf), 1e-9)
    gain = target_peak / peak
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(CHANNELS)
        handle.setsampwidth(SAMPLE_WIDTH)
        handle.setframerate(SAMPLE_RATE)
        frames = bytearray()
        for value in buf:
            shaped = math.tanh(value * gain * 1.15)
            frames.extend(struct.pack("<h", int(max(min(shaped, 0.98), -0.98) * 32767)))
        handle.writeframes(frames)


def intro_bed() -> list[float]:
    buf = blank(8.0)
    add_pad_chord(buf, start=0.0, duration=4.6, notes=(48, 55, 60, 64, 67, 71, 74), amp=0.28)
    add_pad_chord(buf, start=3.8, duration=4.2, notes=(41, 48, 55, 60, 64, 67, 72), amp=0.23)
    for start, note, pan in ((0.9, 72, -0.24), (1.8, 79, 0.28), (3.0, 76, 0.1), (5.6, 74, -0.18)):
        add_bell(buf, start=start, note=note, amp=0.045, pan=pan, decay=1.2)
    apply_delay(buf, delay_seconds=0.34, feedback=0.16)
    fade(buf, fade_in=0.45, fade_out=1.2)
    return buf


def outro_bed() -> list[float]:
    buf = blank(8.0)
    add_pad_chord(buf, start=0.0, duration=4.5, notes=(41, 48, 55, 60, 64, 67, 72), amp=0.24)
    add_pad_chord(buf, start=3.7, duration=4.3, notes=(48, 55, 60, 64, 67, 69, 74), amp=0.26)
    for start, note, pan in ((0.7, 74, -0.22), (2.1, 79, 0.2), (4.8, 76, -0.05), (6.1, 72, 0.18)):
        add_bell(buf, start=start, note=note, amp=0.04, pan=pan, decay=1.45)
    apply_delay(buf, delay_seconds=0.37, feedback=0.15)
    fade(buf, fade_in=0.4, fade_out=1.7)
    return buf


def divider_stinger() -> list[float]:
    buf = blank(1.8)
    add_noise_swell(buf, start=0.0, duration=1.15, amp=0.018)
    add_tone(buf, start=0.08, duration=1.2, freq=midi_to_hz(43), amp=0.07, attack=0.06, release=0.55)
    for start, note, pan in ((0.25, 67, -0.25), (0.37, 74, 0.1), (0.49, 79, 0.28)):
        add_bell(buf, start=start, note=note, amp=0.075, pan=pan, decay=0.9)
    apply_delay(buf, delay_seconds=0.21, feedback=0.18)
    fade(buf, fade_in=0.03, fade_out=0.55)
    return buf


def caution_ping() -> list[float]:
    buf = blank(0.72)
    add_bell(buf, start=0.02, note=76, amp=0.09, pan=-0.08, decay=0.5)
    add_bell(buf, start=0.07, note=83, amp=0.05, pan=0.14, decay=0.45)
    fade(buf, fade_in=0.01, fade_out=0.24)
    return buf


def candidate_b_intro_bed() -> list[float]:
    buf = blank(8.0)
    add_pad_chord(buf, start=0.0, duration=5.0, notes=(45, 52, 57, 60, 64, 69), amp=0.24)
    add_pad_chord(buf, start=4.2, duration=3.8, notes=(43, 50, 55, 59, 62, 67), amp=0.21)
    for start, note, pan in ((1.1, 69, -0.18), (2.7, 76, 0.16), (5.3, 72, 0.06)):
        add_bell(buf, start=start, note=note, amp=0.032, pan=pan, decay=1.35)
    apply_delay(buf, delay_seconds=0.42, feedback=0.13)
    fade(buf, fade_in=0.55, fade_out=1.4)
    return buf


def candidate_b_outro_bed() -> list[float]:
    buf = blank(8.0)
    add_pad_chord(buf, start=0.0, duration=4.6, notes=(43, 50, 55, 59, 62, 67), amp=0.21)
    add_pad_chord(buf, start=3.9, duration=4.1, notes=(45, 52, 57, 60, 64, 69), amp=0.23)
    for start, note, pan in ((0.9, 72, -0.12), (3.5, 76, 0.18), (5.9, 69, -0.08)):
        add_bell(buf, start=start, note=note, amp=0.03, pan=pan, decay=1.55)
    apply_delay(buf, delay_seconds=0.45, feedback=0.12)
    fade(buf, fade_in=0.5, fade_out=1.8)
    return buf


def candidate_b_divider_stinger() -> list[float]:
    buf = blank(1.65)
    add_tone(buf, start=0.02, duration=1.1, freq=midi_to_hz(40), amp=0.055, attack=0.08, release=0.7)
    for start, note, pan in ((0.22, 60, -0.2), (0.36, 67, 0.1), (0.52, 72, 0.24)):
        add_bell(buf, start=start, note=note, amp=0.06, pan=pan, decay=0.85)
    apply_delay(buf, delay_seconds=0.24, feedback=0.13)
    fade(buf, fade_in=0.03, fade_out=0.58)
    return buf


def candidate_b_caution_ping() -> list[float]:
    buf = blank(0.8)
    add_bell(buf, start=0.02, note=69, amp=0.075, pan=-0.1, decay=0.55)
    add_bell(buf, start=0.09, note=76, amp=0.045, pan=0.16, decay=0.46)
    fade(buf, fade_in=0.01, fade_out=0.27)
    return buf


def candidate_c_intro_bed() -> list[float]:
    buf = blank(8.0)
    add_pad_chord(buf, start=0.0, duration=8.0, notes=(48, 55, 60, 67), amp=0.15)
    for start, note, pan in ((1.2, 76, -0.2), (3.7, 79, 0.22), (6.0, 72, 0.02)):
        add_bell(buf, start=start, note=note, amp=0.04, pan=pan, decay=1.7)
    apply_delay(buf, delay_seconds=0.5, feedback=0.1)
    fade(buf, fade_in=0.8, fade_out=1.6)
    return buf


def candidate_c_outro_bed() -> list[float]:
    buf = blank(8.0)
    add_pad_chord(buf, start=0.0, duration=8.0, notes=(48, 55, 60, 64), amp=0.14)
    for start, note, pan in ((1.0, 79, 0.18), (3.2, 76, -0.16), (5.7, 72, 0.08)):
        add_bell(buf, start=start, note=note, amp=0.038, pan=pan, decay=1.8)
    apply_delay(buf, delay_seconds=0.52, feedback=0.1)
    fade(buf, fade_in=0.7, fade_out=2.0)
    return buf


def candidate_c_divider_stinger() -> list[float]:
    buf = blank(1.35)
    add_noise_swell(buf, start=0.0, duration=0.72, amp=0.01)
    add_bell(buf, start=0.12, note=72, amp=0.075, pan=-0.08, decay=0.72)
    add_bell(buf, start=0.25, note=79, amp=0.04, pan=0.14, decay=0.6)
    apply_delay(buf, delay_seconds=0.18, feedback=0.13)
    fade(buf, fade_in=0.02, fade_out=0.45)
    return buf


def candidate_c_caution_ping() -> list[float]:
    buf = blank(0.58)
    add_bell(buf, start=0.01, note=81, amp=0.07, pan=0.0, decay=0.42)
    fade(buf, fade_in=0.01, fade_out=0.2)
    return buf


def main() -> None:
    cues = {
        "calculus_intro_bed.wav": (intro_bed(), 0.17),
        "calculus_outro_bed.wav": (outro_bed(), 0.17),
        "calculus_divider_stinger.wav": (divider_stinger(), 0.30),
        "calculus_caution_ping.wav": (caution_ping(), 0.26),
        "candidate_b_intro_bed.wav": (candidate_b_intro_bed(), 0.16),
        "candidate_b_outro_bed.wav": (candidate_b_outro_bed(), 0.16),
        "candidate_b_divider_stinger.wav": (candidate_b_divider_stinger(), 0.27),
        "candidate_b_caution_ping.wav": (candidate_b_caution_ping(), 0.24),
        "candidate_c_intro_bed.wav": (candidate_c_intro_bed(), 0.14),
        "candidate_c_outro_bed.wav": (candidate_c_outro_bed(), 0.14),
        "candidate_c_divider_stinger.wav": (candidate_c_divider_stinger(), 0.24),
        "candidate_c_caution_ping.wav": (candidate_c_caution_ping(), 0.21),
    }
    for name, (buf, peak) in cues.items():
        write_wav(ROOT / name, buf, target_peak=peak)


if __name__ == "__main__":
    main()

"""Small WAV helpers for the gen-2 video pipeline.

Gemini TTS returns raw 16-bit PCM in the public API examples. Keeping the audio
helpers here avoids pulling in numpy/soundfile just to wrap, measure, and join
short narration clips.
"""
from __future__ import annotations

import wave
from pathlib import Path


DEFAULT_SAMPLE_RATE = 24_000
DEFAULT_CHANNELS = 1
DEFAULT_SAMPLE_WIDTH = 2


def write_pcm_wav(
    path: Path,
    pcm: bytes,
    *,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    channels: int = DEFAULT_CHANNELS,
    sample_width: int = DEFAULT_SAMPLE_WIDTH,
) -> None:
    """Write signed little-endian PCM bytes to a WAV file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(channels)
        handle.setsampwidth(sample_width)
        handle.setframerate(sample_rate)
        handle.writeframes(pcm)


def silence_pcm(
    seconds: float,
    *,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    channels: int = DEFAULT_CHANNELS,
    sample_width: int = DEFAULT_SAMPLE_WIDTH,
) -> bytes:
    """Return WAV-ready zero PCM for *seconds* of silence."""
    frame_count = max(int(round(seconds * sample_rate)), 0)
    return b"\x00" * frame_count * channels * sample_width


def wav_duration(path: Path) -> float:
    """Measure a WAV file duration in seconds."""
    with wave.open(str(path), "rb") as handle:
        return handle.getnframes() / float(handle.getframerate())


def read_wav_pcm(path: Path) -> tuple[bytes, int, int, int]:
    """Return ``(pcm, sample_rate, channels, sample_width)`` for a WAV file."""
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        sample_width = handle.getsampwidth()
        sample_rate = handle.getframerate()
        pcm = handle.readframes(handle.getnframes())
    return pcm, sample_rate, channels, sample_width


def concat_wavs(paths: list[Path], output_path: Path) -> float:
    """Concatenate compatible WAV files and return the combined duration."""
    if not paths:
        write_pcm_wav(output_path, b"")
        return 0.0

    rendered: list[bytes] = []
    expected: tuple[int, int, int] | None = None
    for path in paths:
        pcm, sample_rate, channels, sample_width = read_wav_pcm(path)
        current = (sample_rate, channels, sample_width)
        if expected is None:
            expected = current
        elif current != expected:
            raise ValueError(
                f"Cannot concatenate WAV files with different formats: "
                f"{path} has {current}, expected {expected}."
            )
        rendered.append(pcm)

    assert expected is not None
    sample_rate, channels, sample_width = expected
    write_pcm_wav(
        output_path,
        b"".join(rendered),
        sample_rate=sample_rate,
        channels=channels,
        sample_width=sample_width,
    )
    return wav_duration(output_path)

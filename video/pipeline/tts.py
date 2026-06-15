"""Storyboard beat TTS interface.

This command turns content-scene ``say`` fields into one WAV per reveal beat and
a manifest that later render/mux stages can consume. The backend boundary is
small on purpose: swap model names or providers without changing storyboard or
scene-player code.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()

import yaml  # noqa: E402

from pipeline.audio import concat_wavs, pcm_duration, silence_pcm, trim_silence, wav_duration, write_pcm_wav  # noqa: E402
from pipeline.narration import estimate_seconds, parse_say  # noqa: E402
from pipeline.timing import text_hash  # noqa: E402


DEFAULT_MODEL = "gemini-3.1-flash-tts-preview"
DEFAULT_VOICE = "Charon"
DEFAULT_STYLE = (
    "Read in a clear, calm calculus lecture voice. Keep the pacing steady. "
    "Read inline LaTeX in natural language."
)

# MiMo platform (Xiaomi): OpenAI-compatible /chat/completions, same as the vision
# critic (see pipeline/critic.py). MiMo-V2.5-TTS does NOT read LaTeX -- callers
# must pass spoken-form text (the *_narration_spoken.md versions).
MIMO_BASE_URL = "https://api.xiaomimimo.com/v1"
MIMO_MODEL = "mimo-v2.5-tts"
MIMO_VOICE = "Mia"
MIMO_STYLE = (
    "Read like the narrator of a polished YouTube science explainer: clear, "
    "engaging, and conversational, at a normal talking pace -- natural momentum, "
    "not slow or drawn out, and no long dramatic pauses, just ordinary pauses at "
    "sentence ends. Warm and lightly energetic, curious rather than solemn, like "
    "explaining an idea to a smart friend. Pronounce every mathematical "
    "expression clearly and correctly."
)


@dataclass(frozen=True)
class TTSRequest:
    text: str
    model: str
    voice: str
    style: str


@dataclass(frozen=True)
class TTSResult:
    pcm: bytes
    sample_rate: int = 24_000
    channels: int = 1
    sample_width: int = 2
    raw_audio_seconds: float | None = None
    trimmed_audio_seconds: float | None = None
    trimmed_silence_seconds: float | None = None


@dataclass(frozen=True)
class SynthesizedBeat:
    duration: float
    raw_audio_seconds: float | None = None
    trimmed_audio_seconds: float | None = None
    trimmed_silence_seconds: float | None = None


class TTSBackend(Protocol):
    name: str

    def synthesize(self, request: TTSRequest) -> TTSResult:
        """Return raw PCM for one narration beat."""


class MockTTSBackend:
    """Offline backend for validating manifests and timing plumbing."""

    name = "mock"

    def __init__(self, empty_seconds: float) -> None:
        self.empty_seconds = empty_seconds

    def synthesize(self, request: TTSRequest) -> TTSResult:
        seconds = self.empty_seconds if not request.text else estimate_seconds(request.text)
        return TTSResult(silence_pcm(seconds))


_RETRY_AFTER = re.compile(r"retry in ([0-9.]+)s", re.IGNORECASE)
_RETRY_DELAY = re.compile(r"retrydelay['\"]?\s*[:=]\s*['\"]?([0-9.]+)s", re.IGNORECASE)


def _retry_delay(exc: Exception) -> float | None:
    """Seconds to wait before retrying a rate-limited (429) call, else None.

    Free-tier TTS quota is only a few requests per minute; on 429 the server
    reports how long to wait. Parse that out and honor it (plus headroom).
    Non-429 errors -- bad key, bad model, malformed request -- return None so
    they surface immediately instead of being retried.
    """
    code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
    text = str(exc)
    if code != 429 and "RESOURCE_EXHAUSTED" not in text and "429" not in text:
        return None
    # A per-day quota does not reset within any retry window. Retrying it just
    # burns minutes to fail anyway -- treat it as fatal so the caller stops fast.
    if "PerDay" in text or "RequestsPerDay" in text:
        return None
    for pattern in (_RETRY_AFTER, _RETRY_DELAY):
        match = pattern.search(text)
        if match:
            return float(match.group(1)) + 2.0  # clear the server window
    return 30.0  # no delay advertised: back off conservatively


class GeminiTTSBackend:
    """Gemini native TTS backend using the google-genai SDK.

    Adds client-side pacing (``min_interval``) and 429-aware retry on top of the
    raw SDK call, so ``--scene all`` completes unattended even against the free
    tier's few-requests-per-minute TTS quota.
    """

    name = "gemini"

    def __init__(self, *, max_retries: int = 6, min_interval: float = 0.0) -> None:
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise RuntimeError(
                "Gemini TTS requires google-genai. Install it into the project "
                "environment, then rerun this command."
            ) from exc
        self._genai = genai
        self._types = types
        self._client = genai.Client()
        self._max_retries = max_retries
        self._min_interval = min_interval
        self._last_call = 0.0

    def _throttle(self) -> None:
        """Space consecutive API calls by at least ``min_interval`` seconds."""
        if self._min_interval > 0:
            wait = self._min_interval - (time.monotonic() - self._last_call)
            if wait > 0:
                time.sleep(wait)
        self._last_call = time.monotonic()

    def synthesize(self, request: TTSRequest) -> TTSResult:
        prompt = request.text
        if request.style:
            prompt = f"{request.style}\n\n{request.text}"

        config = self._types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=self._types.SpeechConfig(
                voice_config=self._types.VoiceConfig(
                    prebuilt_voice_config=self._types.PrebuiltVoiceConfig(
                        voice_name=request.voice,
                    )
                )
            ),
        )

        for attempt in range(self._max_retries + 1):
            self._throttle()
            try:
                response = self._client.models.generate_content(
                    model=request.model,
                    contents=prompt,
                    config=config,
                )
                return TTSResult(pcm=self._extract_audio(response))
            except Exception as exc:  # noqa: BLE001 -- inspect, then retry or reraise
                delay = _retry_delay(exc)
                if delay is None or attempt == self._max_retries:
                    if "RESOURCE_EXHAUSTED" in str(exc) or "429" in str(exc):
                        print(
                            "[tts] giving up: free-tier quota exhausted (this TTS model "
                            "allows ~10 requests/day). Upgrade to a paid tier, or resume "
                            "later with --reuse-existing to keep finished beats.",
                            flush=True,
                        )
                    raise
                print(
                    f"[tts] rate-limited (429); waiting {delay:.0f}s then retrying "
                    f"(attempt {attempt + 1}/{self._max_retries})",
                    flush=True,
                )
                time.sleep(delay)
        raise RuntimeError("unreachable: Gemini retry loop exited without a result")

    @staticmethod
    def _extract_audio(response: Any) -> bytes:
        candidates = getattr(response, "candidates", None) or []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            for part in getattr(content, "parts", None) or []:
                inline_data = getattr(part, "inline_data", None)
                data = getattr(inline_data, "data", None)
                if isinstance(data, bytes):
                    return data
                if isinstance(data, str):
                    return base64.b64decode(data)
        raise RuntimeError("Gemini TTS response did not contain inline audio data.")


class MimoTTSBackend:
    """Xiaomi MiMo-V2.5-TTS backend (OpenAI-compatible /chat/completions).

    Mirrors the auth + retry shape pipeline/critic.py already uses for the MiMo
    vision model: custom ``api-key`` header (Bearer also sent, harmless if
    ignored), stdlib ``urllib`` so no extra deps. Text to speak goes in the
    ``assistant`` message; the style instruction goes in the ``user`` message.
    Unlike Gemini, MiMo does NOT read LaTeX -- callers must pass spoken-form text.
    """

    name = "mimo"

    def __init__(self, *, base_url: str, api_key: str, max_retries: int = 4,
                 timeout: int = 180, trim: bool = True, trim_pad: float = 0.08) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._max_retries = max_retries
        self._timeout = timeout
        self._trim = trim          # MiMo pads each clip with ~0.4s trailing silence
        self._trim_pad = trim_pad

    def synthesize(self, request: TTSRequest) -> TTSResult:
        import urllib.error
        import urllib.request

        messages: list[dict[str, str]] = []
        if request.style:
            messages.append({"role": "user", "content": request.style})
        messages.append({"role": "assistant", "content": request.text})
        body = json.dumps(
            {
                "model": request.model,
                "messages": messages,
                "audio": {"format": "wav", "voice": request.voice},
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            f"{self._base_url}/chat/completions", data=body, method="POST",
            headers={
                "Content-Type": "application/json",
                "api-key": self._api_key,                   # MiMo platform custom header
                "Authorization": f"Bearer {self._api_key}",  # also send Bearer (harmless)
            },
        )
        data: Any = None
        for attempt in range(self._max_retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as exc:
                if exc.code in (429, 500, 502, 503, 504) and attempt < self._max_retries:
                    wait = (2 ** attempt) * 2
                    print(
                        f"[tts] mimo {exc.code}; waiting {wait}s then retrying "
                        f"(attempt {attempt + 1}/{self._max_retries})",
                        flush=True,
                    )
                    time.sleep(wait)
                    continue
                raise
            except (urllib.error.URLError, TimeoutError):
                if attempt < self._max_retries:
                    time.sleep((2 ** attempt) * 2)
                    continue
                raise
        result = self._extract_audio(data)
        raw_seconds = pcm_duration(
            result.pcm, sample_rate=result.sample_rate, channels=result.channels,
            sample_width=result.sample_width,
        )
        trimmed_seconds = raw_seconds
        if self._trim:
            pcm = trim_silence(
                result.pcm, sample_rate=result.sample_rate, channels=result.channels,
                sample_width=result.sample_width, pad_seconds=self._trim_pad,
            )
            trimmed_seconds = pcm_duration(
                pcm, sample_rate=result.sample_rate, channels=result.channels,
                sample_width=result.sample_width,
            )
            result = TTSResult(pcm=pcm, sample_rate=result.sample_rate,
                               channels=result.channels, sample_width=result.sample_width,
                               raw_audio_seconds=raw_seconds,
                               trimmed_audio_seconds=trimmed_seconds,
                               trimmed_silence_seconds=max(raw_seconds - trimmed_seconds, 0.0))
        else:
            result = TTSResult(pcm=result.pcm, sample_rate=result.sample_rate,
                               channels=result.channels, sample_width=result.sample_width,
                               raw_audio_seconds=raw_seconds,
                               trimmed_audio_seconds=trimmed_seconds,
                               trimmed_silence_seconds=0.0)
        return result

    @staticmethod
    def _extract_audio(data: Any) -> TTSResult:
        import io
        import wave

        message = ((data or {}).get("choices") or [{}])[0].get("message") or {}
        audio = message.get("audio")
        b64 = None
        if isinstance(audio, dict):
            b64 = audio.get("data")
        elif isinstance(audio, list) and audio:
            b64 = (audio[0] or {}).get("data")
        if not b64:
            raise RuntimeError(
                "MiMo TTS response did not contain audio data "
                f"(message keys: {list(message.keys())}); raw head: {str(data)[:300]}"
            )
        wav_bytes = base64.b64decode(b64)
        with wave.open(io.BytesIO(wav_bytes), "rb") as wav:
            return TTSResult(
                pcm=wav.readframes(wav.getnframes()),
                sample_rate=wav.getframerate(),
                channels=wav.getnchannels(),
                sample_width=wav.getsampwidth(),
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--storyboard", required=True, type=Path)
    parser.add_argument("--scene", default="all", help="id, comma-separated ids, or 'all'")
    parser.add_argument("--backend", choices=("gemini", "mimo", "mock"), default="gemini")
    parser.add_argument("--model", default=os.environ.get("GEMINI_TTS_MODEL", DEFAULT_MODEL))
    parser.add_argument("--voice", default=os.environ.get("GEMINI_TTS_VOICE"))
    parser.add_argument("--style", default=os.environ.get("GEMINI_TTS_STYLE", DEFAULT_STYLE))
    parser.add_argument("--base-url", default=os.environ.get("MIMO_BASE_URL", MIMO_BASE_URL),
                        help="MiMo platform base URL (--backend mimo)")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--empty-beat-seconds", type=float, default=0.45)
    parser.add_argument("--reuse-existing", action="store_true")
    parser.add_argument("--max-retries", type=int, default=6,
                        help="retries per beat on 429 rate-limit (honors server retryDelay)")
    parser.add_argument("--min-request-interval", type=float, default=0.0,
                        help="min seconds between API calls; free-tier TTS ~21 avoids most 429s")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def load_storyboard(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.resolve().read_text(encoding="utf-8"))


def wanted_scenes(scenes: list[dict[str, Any]], selector: str) -> list[dict[str, Any]]:
    by_id = {scene["id"]: scene for scene in scenes}
    if selector == "all":
        return scenes

    ids = [item.strip() for item in selector.split(",") if item.strip()]
    missing = [scene_id for scene_id in ids if scene_id not in by_id]
    if missing:
        available = ", ".join(sorted(by_id))
        raise SystemExit(f"Unknown scene(s) {missing}. Available: {available}")
    return [by_id[scene_id] for scene_id in ids]


def safe_stem(value: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in value)
    safe = "_".join(part for part in safe.split("_") if part)
    return safe or "beat"


def build_backend(args: argparse.Namespace) -> TTSBackend:
    if args.backend == "mock":
        return MockTTSBackend(args.empty_beat_seconds)
    if args.backend == "mimo":
        api_key = os.environ.get("MIMO_API_KEY")
        if not api_key:
            raise SystemExit("[tts] --backend mimo needs the API key in env MIMO_API_KEY.")
        return MimoTTSBackend(
            base_url=args.base_url, api_key=api_key, max_retries=args.max_retries
        )
    return GeminiTTSBackend(
        max_retries=args.max_retries,
        min_interval=args.min_request_interval,
    )


def scene_beats(scene: dict[str, Any]) -> list[dict[str, Any]]:
    beats = []
    for index, beat in enumerate(parse_say(scene.get("say", "")), start=1):
        beats.append(
            {
                "index": index,
                "id": f"beat_{index:02d}",
                "text": beat.text,
                "reveal": beat.reveal,
            }
        )
    return beats


def synthesize_beat(
    backend: TTSBackend,
    request: TTSRequest,
    output_path: Path,
    *,
    reuse_existing: bool,
    empty_seconds: float,
) -> SynthesizedBeat:
    if output_path.exists() and reuse_existing:
        return SynthesizedBeat(duration=wav_duration(output_path))

    if not request.text:
        result = TTSResult(silence_pcm(empty_seconds))
    else:
        result = backend.synthesize(request)
    write_pcm_wav(
        output_path,
        result.pcm,
        sample_rate=result.sample_rate,
        channels=result.channels,
        sample_width=result.sample_width,
    )
    return SynthesizedBeat(
        duration=wav_duration(output_path),
        raw_audio_seconds=result.raw_audio_seconds,
        trimmed_audio_seconds=result.trimmed_audio_seconds,
        trimmed_silence_seconds=result.trimmed_silence_seconds,
    )


def synthesize_scene(
    *,
    backend: TTSBackend,
    meta: dict[str, Any],
    scene: dict[str, Any],
    scene_number: int,
    output_dir: Path,
    args: argparse.Namespace,
) -> dict[str, Any]:
    voice = args.voice or meta.get("voice") or DEFAULT_VOICE
    scene_id = scene["id"]
    kind = scene.get("kind", "content")
    entry: dict[str, Any] = {
        "scene_number": scene_number,
        "scene_id": scene_id,
        "kind": kind,
    }

    if kind != "content":
        entry.update(
            {
                "narration_mode": "silent",
                "duration": float(scene.get("duration", 0.0)),
                "bgm": scene.get("bgm"),
            }
        )
        return entry

    beats = scene_beats(scene)
    beat_dir = output_dir / "beats" / f"{scene_number:02d}_{scene_id}"
    scene_audio = output_dir / "scenes" / f"{scene_number:02d}_{scene_id}.wav"
    beat_paths: list[Path] = []
    manifest_beats: list[dict[str, Any]] = []
    timeline = 0.0

    for beat in beats:
        beat_path = beat_dir / f"{beat['index']:02d}_{safe_stem(beat['reveal'] or beat['id'])}.wav"
        synth = synthesize_beat(
            backend,
            TTSRequest(
                text=beat["text"],
                model=args.model,
                voice=voice,
                style=args.style,
            ),
            beat_path,
            reuse_existing=args.reuse_existing,
            empty_seconds=args.empty_beat_seconds,
        )
        duration = synth.duration
        beat_paths.append(beat_path)
        beat_entry = {
            **beat,
            "audio_file": str(beat_path.resolve()),
            "audio_seconds": round(duration, 3),
            "start_seconds": round(timeline, 3),
            "end_seconds": round(timeline + duration, 3),
            "text_hash": text_hash(beat["text"]),
        }
        if synth.raw_audio_seconds is not None:
            beat_entry["raw_audio_seconds"] = round(synth.raw_audio_seconds, 3)
        if synth.trimmed_audio_seconds is not None:
            beat_entry["trimmed_audio_seconds"] = round(synth.trimmed_audio_seconds, 3)
        if synth.trimmed_silence_seconds is not None:
            beat_entry["trimmed_silence_seconds"] = round(synth.trimmed_silence_seconds, 3)
        manifest_beats.append(beat_entry)
        timeline += duration

    scene_seconds = concat_wavs(beat_paths, scene_audio)
    entry.update(
        {
            "narration_mode": "beats",
            "audio_file": str(scene_audio.resolve()),
            "audio_seconds": round(scene_seconds, 3),
            "beat_count": len(manifest_beats),
            "script": " ".join(beat["text"] for beat in beats if beat["text"]).strip(),
            "beats": manifest_beats,
        }
    )
    return entry


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    if args.backend == "mimo":
        # the --model/--style defaults are Gemini's; use MiMo's unless overridden.
        if args.model == DEFAULT_MODEL:
            args.model = MIMO_MODEL
        if args.style == DEFAULT_STYLE:
            args.style = MIMO_STYLE
    data = load_storyboard(args.storyboard)
    meta = data["meta"]
    scenes = wanted_scenes(data["scenes"], args.scene)
    sec_dir = _bootstrap.section_output_dir(meta)
    default_audio_subdir = "audio_mimo" if meta["id"].endswith("_mimo") else "audio"
    output_dir = (
        args.output_dir
        or (sec_dir / default_audio_subdir)
    ).resolve()
    manifest_path = (args.manifest or (output_dir / "manifest.json")).resolve()
    voice = args.voice or meta.get("voice") or DEFAULT_VOICE

    content_count = sum(1 for scene in scenes if scene.get("kind", "content") == "content")
    beat_count = sum(len(scene_beats(scene)) for scene in scenes if scene.get("kind", "content") == "content")
    if args.dry_run:
        print(
            f"Would synthesize {beat_count} beat(s) across {content_count} content scene(s) "
            f"with backend={args.backend}, model={args.model}, voice={voice}."
        )
        return 0

    backend = build_backend(args)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "storyboard": str(args.storyboard.resolve()),
        "deck_id": meta["id"],
        "backend": backend.name,
        "model": args.model,
        "voice": voice,
        "style": args.style,
        "sample_rate": 24_000,
        "channels": 1,
        "sample_width": 2,
        "output_dir": str(output_dir),
        "scenes": [],
    }

    all_scenes = data["scenes"]
    scene_numbers = {scene["id"]: index for index, scene in enumerate(all_scenes, start=1)}
    print(
        f"synthesizing {beat_count} beat(s) across {content_count} content scene(s) "
        f"with backend={backend.name}, model={args.model}, voice={voice}",
        flush=True,
    )
    for scene in scenes:
        print(f"[tts] {scene['id']} ...", flush=True)
        manifest["scenes"].append(
            synthesize_scene(
                backend=backend,
                meta=meta,
                scene=scene,
                scene_number=scene_numbers[scene["id"]],
                output_dir=output_dir,
                args=args,
            )
        )

    write_manifest(manifest_path, manifest)
    print(f"[done] wrote {manifest_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

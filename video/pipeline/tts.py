"""Storyboard beat TTS interface (MiMo route).

This command turns content-scene ``say`` fields into one WAV per reveal beat and
a manifest that ``make.py --reuse-audio`` consumes. The real backend is Xiaomi
MiMo-V2.5-TTS (the project's sole TTS route as of 2026-06-16; the former Gemini
route was retired). ``mock`` (silence) stays for offline manifest/timing checks.

MiMo does NOT read LaTeX, so callers pass the spoken-form storyboard
(``storyboards/<deck>_mimo.yml`` from ``derive_spoken.py``), not the canonical one.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
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


# MiMo platform (Xiaomi): OpenAI-compatible /chat/completions, same as the vision
# critic (see pipeline/critic.py). MiMo-V2.5-TTS does NOT read LaTeX -- callers
# must pass spoken-form text (the *_narration_spoken.md / *_mimo.yml versions).
# This is the project's sole TTS route (Gemini retired 2026-06-16).
MIMO_BASE_URL = "https://api.xiaomimimo.com/v1"
MIMO_BUILTIN_MODEL = "mimo-v2.5-tts"
MIMO_VOICE_DESIGN_MODEL = "mimo-v2.5-tts-voicedesign"
MIMO_MODEL = MIMO_VOICE_DESIGN_MODEL
MIMO_BUILTIN_VOICE = "Mia"
MIMO_VOICE = "Calm Professor"
MIMO_STYLE = (
    "A mature American university professor in his early 50s, clear baritone "
    "voice, calm and authoritative without sounding stiff. Warm but precise, "
    "measured medium pace, careful articulation of mathematical expressions, "
    "with short natural pauses at clause boundaries."
)


# design §10 batch-1 rollout allowlist for --unit auto. Recalibrate/extend to
# derivation+theorem_proof (batch 2) after the first real deck's gates are checked.
SCENE_UNIT_TEMPLATES = frozenset({"definition_math", "graph", "callout", "recap_cards"})


def resolve_unit(unit: str, scene: dict[str, Any]) -> str:
    """beat|scene forced; auto -> scene iff the scene's template is in the batch-1
    allowlist, else beat (conservative default for unknown/heavy templates)."""
    if unit in ("beat", "scene"):
        return unit
    return "scene" if scene.get("template") in SCENE_UNIT_TEMPLATES else "beat"


def is_voice_design_model(model: str) -> bool:
    return model == MIMO_VOICE_DESIGN_MODEL or model.endswith("-voicedesign")


def default_voice_for_model(model: str, meta: dict[str, Any] | None = None) -> str:
    if is_voice_design_model(model):
        return MIMO_VOICE
    voice = (meta or {}).get("voice")
    if voice and voice != MIMO_VOICE:
        return voice
    return MIMO_BUILTIN_VOICE


def load_dotenv() -> None:
    """Load repo-local .env into this process without printing secrets."""
    env_path = _bootstrap.REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip()
        value = value.strip()
        if ((value.startswith('"') and value.endswith('"'))
                or (value.startswith("'") and value.endswith("'"))):
            value = value[1:-1]
        os.environ.setdefault(name, value)


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


class MimoTTSBackend:
    """Xiaomi MiMo-V2.5-TTS backend (OpenAI-compatible /chat/completions).

    Mirrors the auth + retry shape pipeline/critic.py already uses for the MiMo
    vision model: custom ``api-key`` header (Bearer also sent, harmless if
    ignored), stdlib ``urllib`` so no extra deps. Text to speak goes in the
    ``assistant`` message; the style/voice-design instruction goes in the
    ``user`` message.
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
        audio: dict[str, Any] = {"format": "wav"}
        if is_voice_design_model(request.model):
            audio["optimize_text_preview"] = False
        else:
            audio["voice"] = request.voice or MIMO_BUILTIN_VOICE
        body = json.dumps(
            {
                "model": request.model,
                "messages": messages,
                "audio": audio,
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
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--storyboard", required=True, type=Path)
    parser.add_argument("--scene", default="all", help="id, comma-separated ids, or 'all'")
    parser.add_argument("--backend", choices=("mimo", "mock"), default="mimo")
    parser.add_argument("--model", default=os.environ.get("MIMO_TTS_MODEL", MIMO_MODEL))
    parser.add_argument("--voice", default=os.environ.get("MIMO_TTS_VOICE"))
    parser.add_argument("--style", default=os.environ.get("MIMO_TTS_STYLE", MIMO_STYLE))
    parser.add_argument("--base-url", default=os.environ.get("MIMO_BASE_URL", MIMO_BASE_URL),
                        help="MiMo platform base URL (--backend mimo)")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--empty-beat-seconds", type=float, default=0.45)
    parser.add_argument("--reuse-existing", action="store_true")
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
    parser.add_argument("--max-retries", type=int, default=4,
                        help="retries per beat on 429/5xx (MiMo backend)")
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


def load_prior_manifest(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"[tts] cannot read prior manifest for reuse ({path}): {exc}", flush=True)
        return None


def build_reuse_index(manifest: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not manifest:
        return {}
    shared = {
        "backend": manifest.get("backend"),
        "model": manifest.get("model"),
        "voice": manifest.get("voice"),
        "style": manifest.get("style"),
    }
    index: dict[str, dict[str, Any]] = {}
    for scene in manifest.get("scenes", []):
        for beat in scene.get("beats", []):
            audio_file = beat.get("audio_file")
            if not audio_file:
                continue
            index[str(Path(audio_file).resolve())] = {
                **shared,
                "text_hash": beat.get("text_hash"),
            }
    return index


def build_scene_reuse_index(manifest: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    """Reuse index keyed by scene_id, from a prior manifest's scene_aligned entries.
    Carries what §3 freshness needs so TTS can be skipped when only downstream
    (reveal/beat-count) changed. (Per-beat build_reuse_index stays for the beat path.)"""
    if not manifest:
        return {}
    shared = {k: manifest.get(k) for k in ("backend", "model", "voice", "style")}
    out: dict[str, dict[str, Any]] = {}
    for scene in manifest.get("scenes", []):
        if scene.get("narration_mode") != "scene_aligned":
            continue
        out[scene.get("scene_id")] = {
            **shared,
            "scene_text_hash": scene.get("scene_text_hash"),
            "audio_file": scene.get("audio_file"),
            "audio_seconds": scene.get("audio_seconds"),
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


def reusable_existing_beat(
    output_path: Path,
    request: TTSRequest,
    *,
    backend_name: str,
    reuse_index: dict[str, dict[str, Any]],
) -> tuple[bool, str]:
    prior = reuse_index.get(str(output_path.resolve()))
    if prior is None:
        return False, "no matching prior manifest entry"
    expected = {
        "backend": backend_name,
        "model": request.model,
        "voice": request.voice,
        "style": request.style,
        "text_hash": text_hash(request.text),
    }
    for key, value in expected.items():
        if prior.get(key) != value:
            return False, f"{key} changed"
    return True, ""


def build_backend(args: argparse.Namespace) -> TTSBackend:
    if args.backend == "mock":
        return MockTTSBackend(args.empty_beat_seconds)
    load_dotenv()
    api_key = os.environ.get("MIMO_API_KEY")
    if not api_key:
        raise SystemExit("[tts] --backend mimo needs the API key in env MIMO_API_KEY.")
    return MimoTTSBackend(
        base_url=args.base_url, api_key=api_key, max_retries=args.max_retries
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
    backend_name: str,
    reuse_index: dict[str, dict[str, Any]],
) -> SynthesizedBeat:
    if output_path.exists() and reuse_existing:
        reusable, reason = reusable_existing_beat(
            output_path,
            request,
            backend_name=backend_name,
            reuse_index=reuse_index,
        )
        if reusable:
            return SynthesizedBeat(duration=wav_duration(output_path))
        print(f"[tts] not reusing {output_path.name}: {reason}; synthesizing", flush=True)

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
    reuse_index: dict[str, dict[str, Any]],
    scene_reuse_index: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Dispatch a content scene to the beat- or scene-level synthesis path (--unit).
    Non-content scenes stay silent. The beat path ignores scene_reuse_index."""
    scene_id = scene["id"]
    kind = scene.get("kind", "content")
    if kind != "content":
        return {
            "scene_number": scene_number, "scene_id": scene_id, "kind": kind,
            "narration_mode": "silent",
            "duration": float(scene.get("duration", 0.0)),
            "bgm": scene.get("bgm"),
        }
    unit = resolve_unit(getattr(args, "unit", "beat"), scene)
    if unit == "beat":
        return _synthesize_scene_beats(
            backend=backend, meta=meta, scene=scene, scene_number=scene_number,
            output_dir=output_dir, args=args, reuse_index=reuse_index)
    return _synthesize_scene_aligned(
        backend=backend, meta=meta, scene=scene, scene_number=scene_number,
        output_dir=output_dir, args=args, reuse_index=reuse_index,
        scene_reuse_index=scene_reuse_index or {})


def _synthesize_scene_beats(
    *,
    backend: TTSBackend,
    meta: dict[str, Any],
    scene: dict[str, Any],
    scene_number: int,
    output_dir: Path,
    args: argparse.Namespace,
    reuse_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    voice = args.voice or default_voice_for_model(args.model, meta)
    scene_id = scene["id"]
    entry: dict[str, Any] = {
        "scene_number": scene_number,
        "scene_id": scene_id,
        "kind": "content",
    }

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
            backend_name=backend.name,
            reuse_index=reuse_index,
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


def _synth_scene_wav(backend: TTSBackend, plan: dict[str, Any], out_path: Path,
                     voice: str, args: argparse.Namespace) -> None:
    """Synthesize the whole scene transcript in ONE TTS call; write PCM to out_path
    (a .tmp path -- promotion onto the canonical WAV is the atomic step, done only
    after gates pass in _align_and_gate)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    result = backend.synthesize(TTSRequest(
        text=plan["transcript"], model=args.model, voice=voice, style=args.style))
    write_pcm_wav(out_path, result.pcm, sample_rate=result.sample_rate,
                  channels=result.channels, sample_width=result.sample_width)


def _asr_probe_tokens(wav: Path, args: argparse.Namespace) -> list[str] | None:
    """Free ASR (whisper-timestamped) -> normalized token list for the QA probe
    (design §6). Advisory: returns None if the probe cannot run (missing dep/model),
    so a probe failure never blocks synthesis."""
    from pipeline import scene_align as SA
    try:
        import whisper_timestamped as wt
    except ImportError:
        return None
    try:
        model = wt.load_model(args.aligner_model, device=args.aligner_device)
        result = wt.transcribe(model, str(wav), language="en")
    except Exception:  # noqa: BLE001 - probe is advisory, never fatal
        return None
    text = " ".join(seg.get("text", "") for seg in result.get("segments", []))
    return SA.tokenize(text)


def _align_and_gate(plan: dict[str, Any], wav: Path, scene_number: int,
                    words_file: Path, aligned_file: Path, args: argparse.Namespace, *,
                    audio_file: Path, promote_from: Path | None,
                    aligner_model: str | None = None) -> dict[str, Any]:
    """Align `wav` to the plan, map to beats, run gates (+ optional ASR QA probe),
    and assemble the scene_aligned entry. Verify-before-overwrite: only on PASS does
    it promote the WAV and atomically write the canonical words/aligned artifacts."""
    from pipeline import scene_align as SA
    from pipeline import atomicio
    model = aligner_model or args.aligner_model
    try:
        res = SA.align_scene(wav, plan, model=model, device=args.aligner_device)
    except SA.AlignmentError as exc:
        # aligner aborted (>failure_threshold words unaligned) or token-index broke.
        # Do NOT crash the deck: return a fail-status entry so the caller routes to the
        # fallback ladder -> beats terminal (design "always a shippable path"). Never
        # becomes the final entry, since the beats rung always passes.
        return {"scene_id": plan["scene_id"], "narration_mode": "scene_aligned",
                "validation": {"status": "fail", "warnings": [], "metrics": {},
                               "error": f"alignment aborted: {exc}"},
                "fallback_history": []}
    words = res["words"]
    audio_seconds = wav_duration(wav)
    beats = SA.map_to_beats(plan, words, audio_seconds, multi=res["multi"])
    gates = SA.run_gates(plan, words, beats, audio_seconds)
    if not getattr(args, "skip_qa", False):
        asr = _asr_probe_tokens(wav, args)
        if asr is not None:
            fa_probs = [w.get("probability") for w in words]
            qa = SA.qa_diff(SA.tokenize(plan["transcript"]), asr, fa_probs,
                            weak_spans=SA.boundary_weak_spans(beats))
            gates = {**gates, "qa": qa}
            if qa["verdict"] == "fail":
                gates["status"] = "fail"
                gates["failures"] = gates["failures"] + ["QA probe: suspect TTS misspeak"]
    entry = SA.build_scene_aligned_entry(
        scene_number=scene_number, plan=plan, beats=beats, audio_seconds=audio_seconds,
        audio_file=audio_file, summary=res["summary"], gates=gates,
        words_file=words_file, aligned_file=aligned_file)
    if gates["status"] in ("pass", "pass_with_warnings"):
        if promote_from is not None:
            atomicio.promote(promote_from, Path(audio_file))
        atomicio.atomic_write_json(words_file, {
            "summary": res["summary"], "words": words, "segments": res["segments"]})
        atomicio.atomic_write_json(aligned_file, {
            "scene_id": plan["scene_id"], "audio_seconds": round(audio_seconds, 3), "beats": beats})
    return entry


def _build_fallback_rungs(backend, meta, scene, scene_number, output_dir, args, plan, reuse_index):
    """Design §7 ladder rungs for one failed scene. Batch-1 ladder is
    arbiter (free) -> resynth (billed) -> beats (free terminal). Rung 3 (sentence
    chunk) is deferred to batch-2 -- the pilot showed all scene types pass FA, so it
    is rarely reached; when a real deck needs it, add a ("chunk", True, ...) rung
    here. Each rung callable takes the ctx dict from _synthesize_scene_aligned."""
    scene_id = scene["id"]
    scenes_dir, align_dir = output_dir / "scenes", output_dir / "align"
    scene_wav = scenes_dir / f"{scene_number:02d}_{scene_id}.wav"
    words_file = align_dir / f"{scene_number:02d}_{scene_id}.words.json"
    aligned_file = align_dir / f"{scene_number:02d}_{scene_id}.aligned.json"
    voice = args.voice or default_voice_for_model(args.model, meta)

    def _ok(entry):
        return entry["validation"]["status"] in ("pass", "pass_with_warnings")

    def arbiter(ctx):
        # re-align the SAME primary WAV with small.en (no re-synthesis, no billing)
        entry = _align_and_gate(plan, ctx["primary_wav"], scene_number, words_file, aligned_file,
                                args, audio_file=scene_wav, promote_from=ctx["primary_wav"],
                                aligner_model="small.en")
        return {"status": "pass" if _ok(entry) else "fail", "entry": entry,
                "reason": "small.en arbiter re-align"}

    def resynth(ctx):
        tmp = scene_wav.with_name(scene_wav.name + ".resynth.tmp")
        _synth_scene_wav(backend, plan, tmp, voice, args)
        entry = _align_and_gate(plan, tmp, scene_number, words_file, aligned_file, args,
                                audio_file=scene_wav, promote_from=tmp)
        if not _ok(entry):
            tmp.unlink(missing_ok=True)
        return {"status": "pass" if _ok(entry) else "fail", "entry": entry,
                "reason": "resynthesize scene once"}

    def beats(ctx):
        entry = _synthesize_scene_beats(backend=backend, meta=meta, scene=scene,
            scene_number=scene_number, output_dir=output_dir, args=args, reuse_index=reuse_index)
        return {"status": "pass", "entry": entry, "reason": "beat-level fallback (terminal)"}

    return [("arbiter", False, arbiter), ("resynth", True, resynth), ("beats", False, beats)]


def _synthesize_scene_aligned(*, backend, meta, scene, scene_number, output_dir, args,
                              reuse_index, scene_reuse_index):
    """Scene-level path (design §3 storage + verify-before-overwrite + §7 ladder). The
    WAV is synthesized to a temp path and promoted onto the canonical path ONLY after
    gates pass, so a prior good WAV is never clobbered by a bad re-synth."""
    from pipeline import scene_align as SA
    from pipeline import scene_fallback as FB
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
    ctx = {"plan": plan, "primary_wav": tmp_wav, "scene_wav": scene_wav}
    rungs = _build_fallback_rungs(backend, meta, scene, scene_number, output_dir, args, plan, reuse_index)
    result = FB.run_ladder(scene_id=scene_id, rungs=rungs, budget=budget, ctx=ctx)
    tmp_wav.unlink(missing_ok=True)   # clean the primary temp after the ladder settles
    return result["entry"]


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    from pipeline.atomicio import atomic_write_json
    atomic_write_json(path, manifest)


def main() -> int:
    args = parse_args()
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
    voice = args.voice or default_voice_for_model(args.model, meta)
    prior_manifest = load_prior_manifest(manifest_path) if args.reuse_existing else None
    reuse_index = build_reuse_index(prior_manifest)                 # per-beat (beat path)
    scene_reuse_index = build_scene_reuse_index(prior_manifest)     # per-scene (scene path)
    if args.reuse_existing and prior_manifest is None:
        print(
            "[tts] --reuse-existing requested but no prior manifest was found; "
            "existing WAV files will not be trusted blindly.",
            flush=True,
        )

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
        "schema": 2,
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
                reuse_index=reuse_index,
                scene_reuse_index=scene_reuse_index,
            )
        )

    write_manifest(manifest_path, manifest)
    print(f"[done] wrote {manifest_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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
import shutil
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
from pipeline.derived_check import check_derived_freshness  # noqa: E402  (manim-free, F11-safe)
from pipeline.narration import estimate_seconds, parse_say  # noqa: E402
from pipeline.template_names import CONTENT_TEMPLATES  # noqa: E402  (manim-free single source, F11-safe)
from pipeline.timing import text_hash  # noqa: E402


# MiMo platform (Xiaomi): OpenAI-compatible /chat/completions, same as the vision
# critic (see pipeline/critic.py). MiMo-V2.5-TTS does NOT read LaTeX -- callers
# must pass spoken-form text (the *_narration_spoken.md / *_mimo.yml versions).
# This is the project's sole TTS route (Gemini retired 2026-06-16; the MiMo
# voice-design model + the "Calm Professor" persona retired 2026-07-05 -- the route
# is now built-in voice "Dean" only, selected via audio.voice, no style/persona prompt).
MIMO_BASE_URL = "https://api.xiaomimimo.com/v1"
MIMO_MODEL = "mimo-v2.5-tts"   # built-in voice model (sole model)
MIMO_VOICE = "Dean"            # default built-in voice
MIMO_STYLE = ""                # no persona/style prompt on the built-in route


# --unit auto routes every KNOWN content template to scene-level TTS. History:
# batch-1 four (2026-07-05), batch-2 six (2026-07-06); 2026-07-11 the hand-kept
# list was found missing procedure_steps/value_table/sign_chart vs the registry,
# so it now derives from pipeline/template_names.py (parity selftest guards it).
# Unknown templates still fall back to beat. An over-broad allowlist is bounded but
# NOT free: a scene whose FA fails demotes down the ladder to the beats terminal,
# which under MiMo bills once PER non-empty beat (not "one attempt"); dry-run's
# worst-case column already accounts for that fan-out.
SCENE_UNIT_TEMPLATES = frozenset(CONTENT_TEMPLATES)


def resolve_unit(unit: str, scene: dict[str, Any]) -> str:
    """beat|scene forced; auto -> scene iff the scene's template is in the rollout allowlist
    (batch-2: all content templates), else beat (conservative default for unknown templates)."""
    if unit in ("beat", "scene"):
        return unit
    return "scene" if scene.get("template") in SCENE_UNIT_TEMPLATES else "beat"


def default_voice_for_model(meta: dict[str, Any] | None = None) -> str:
    """Built-in voice: the storyboard's meta.voice if set, else the default (Dean)."""
    return (meta or {}).get("voice") or MIMO_VOICE


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
        self.stats = {"calls": 0, "retries": 0}

    def synthesize(self, request: TTSRequest) -> TTSResult:
        self.stats["calls"] += 1
        seconds = self.empty_seconds if not request.text else estimate_seconds(request.text)
        return TTSResult(silence_pcm(seconds))


class BudgetedBackend:
    """``--max-billed-calls N`` (``--no-billing`` == 0): a hard cap on synthesis calls.

    Why a cap and not just care: a run that "should" cost nothing has several ways to cost
    something, and none of them announce themselves up front. Measured 2026-09-12: a
    marker-only re-map of five scenes, every text hash verified unchanged, billed 13 calls
    -- because `--reuse-existing` was omitted, so `use_reuse` was False, the reuse index
    was empty and `scene_reuse_ok` was never even consulted; one scene then demoted to the
    beats terminal, which `--fallback-budget` does not bound (it bounds ladder rungs 2-3
    only). A cap bounds the WHOLE run, terminal included: the call that would exceed it
    aborts, and since a scene's WAV is only promoted after its gates pass, an abort leaves
    the prior manifest and audio untouched, so the run can be fixed and retried.
    """

    def __init__(self, inner, limit: int) -> None:
        self._inner = inner
        self._limit = limit
        self._spent = 0
        self.name = inner.name
        self.stats = inner.stats

    def synthesize(self, request: "TTSRequest") -> "TTSResult":
        if self._spent >= self._limit:
            raise SystemExit(
                f"[tts] --max-billed-calls {self._limit}: this run needed synthesis call "
                f"#{self._spent + 1} and stopped before making it. Either the existing "
                f"audio could not be reused / re-aligned against the current beat "
                f"boundaries (typically a {{show ...}} marker that now splits a beat "
                f"mid-phrase -- move it to a boundary the aligner can place), or the cap "
                f"is simply lower than this run needs. Nothing was promoted, so the prior "
                f"manifest and WAVs are untouched."
            )
        self._spent += 1
        return self._inner.synthesize(request)


class MimoTTSBackend:
    """Xiaomi MiMo-V2.5-TTS backend (OpenAI-compatible /chat/completions).

    Mirrors the auth + retry shape pipeline/critic.py already uses for the MiMo
    vision model: custom ``api-key`` header (Bearer also sent, harmless if
    ignored), stdlib ``urllib`` so no extra deps. Text to speak goes in the
    ``assistant`` message; the built-in voice is selected via ``audio.voice``.
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
        self.stats = {"calls": 0, "retries": 0}

    def synthesize(self, request: TTSRequest) -> TTSResult:
        import urllib.error
        import urllib.request

        self.stats["calls"] += 1
        messages: list[dict[str, str]] = []
        if request.style:
            messages.append({"role": "user", "content": request.style})
        messages.append({"role": "assistant", "content": request.text})
        audio: dict[str, Any] = {"format": "wav", "voice": request.voice or MIMO_VOICE}
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
                    self.stats["retries"] += 1
                    time.sleep(wait)
                    continue
                raise
            except (urllib.error.URLError, TimeoutError):
                if attempt < self._max_retries:
                    self.stats["retries"] += 1
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
    parser.add_argument("--backend", choices=("mimo", "mock"), required=True,
                        help="TTS backend; REQUIRED (no default) so a bare run can neither "
                             "silently bill MiMo nor silently clobber real WAVs with mock")
    parser.add_argument("--force-backend-switch", action="store_true",
                        help="allow overwriting a manifest whose backend differs (only with --scene all)")
    parser.add_argument("--force-clobber", action="store_true",
                        help="overwrite a corrupt manifest or orphan WAVs (only with --scene all)")
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
    parser.add_argument("--no-billing", action="store_true",
                        help="abort instead of making ANY synthesis call (== "
                             "--max-billed-calls 0): for marker-only edits, where the "
                             "intent is to re-map beats onto existing audio")
    parser.add_argument("--max-billed-calls", type=int, default=None,
                        help="hard cap on synthesis calls for the WHOLE run, beats "
                             "terminal included (--fallback-budget bounds only ladder "
                             "rungs 2-3). The call that would exceed it aborts before it "
                             "is made; nothing is promoted, so prior audio is untouched")
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


_IDENTITY_KEYS = ("deck_id", "backend", "model", "voice", "style",
                  "sample_rate", "channels", "sample_width", "output_dir")


def read_manifest_status(path: Path) -> tuple[dict | None, str]:
    """('ok'|'absent'|'corrupt'). 'ok' is a PROMISE that every prior-manifest consumer
    runs without crashing on a shape it assumed. Beyond the top level (dict + str
    'backend' + list-of-dict 'scenes') we validate exactly the per-scene fields those
    consumers dereference by TYPE (R3-B1, Codex option a -- bounded to real derefs,
    not speculative):
      - scene_id: str                    -> dict key in build_scene_reuse_index / merged_manifest
      - beats (only if the KEY exists):  -> build_reuse_index does `for beat in scene["beats"]`
          list of dicts, and each beat's audio_file (if present) a str  (Path(audio_file))
          (test `"beats" in s`, NOT .get() -- explicit null must fail, since
           scene.get("beats", []) returns None for a present-but-null key)
      - audio_seconds (scene_aligned only, if present): a real number   (scene_reuse_ok float())
    Anything else -- truncation, non-dict JSON, a wrong type above -- is 'corrupt'
    (fail CLOSED). Beat text/hash/timing are NOT validated (nothing keys on their
    type). Keep this in sync if a consumer starts dereferencing a new field."""
    if not path.exists():
        return None, "absent"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None, "corrupt"
    scenes = data.get("scenes") if isinstance(data, dict) else None
    if (not isinstance(data, dict) or not isinstance(data.get("backend"), str)
            or not isinstance(scenes, list) or not all(isinstance(e, dict) for e in scenes)):
        return None, "corrupt"
    for s in scenes:
        if not isinstance(s.get("scene_id"), str):
            return None, "corrupt"
        if "beats" in s:
            beats = s["beats"]
            if (not isinstance(beats, list) or not all(isinstance(b, dict) for b in beats)
                    or any(b.get("audio_file") is not None
                           and not isinstance(b.get("audio_file"), str) for b in beats)):
                return None, "corrupt"
        if s.get("narration_mode") == "scene_aligned":
            secs = s.get("audio_seconds")
            if secs is not None and (isinstance(secs, bool) or not isinstance(secs, (int, float))):
                return None, "corrupt"
    return data, "ok"


def _has_audio(output_dir: Path) -> bool:
    return any((output_dir / "scenes").glob("*.wav")) or any((output_dir / "beats").rglob("*.wav"))


def overwrite_guard(*, status: str, existing: dict | None, intended: dict, scene_sel: str,
                    output_dir: Path, force_backend_switch: bool, force_clobber: bool) -> str | None:
    """Abort message (else None), computed BEFORE any synthesis/write so a bad run
    never bills a call or clobbers a WAV first (NB1). `intended` = the identity this
    run would write. Recovering a corrupt/orphaned output needs --force-clobber AND
    --scene all (a forced subset would leave un-accounted WAVs; NB2)."""
    need_full = "recovery needs --force-clobber AND --scene all"
    if status == "corrupt":
        if not force_clobber:
            return ("manifest present but corrupt/semantically invalid; refusing to overwrite "
                    "(it may still shadow real WAVs). Re-synthesize the whole deck or --force-clobber.")
        return None if scene_sel == "all" else need_full
    if status == "absent" and _has_audio(output_dir):
        if not force_clobber:
            return ("no valid manifest but WAVs already exist under the output dir; refusing to "
                    "overwrite unmanaged audio. Pass --force-clobber (with --scene all).")
        return None if scene_sel == "all" else need_full
    if status == "ok":
        diff = [k for k in _IDENTITY_KEYS if (existing or {}).get(k) != intended.get(k)]
        if diff and scene_sel != "all":
            return (f"this run's identity differs from the existing manifest on {diff}; a --scene "
                    f"subset can't safely merge into it. Re-run --scene all to rebuild.")
        if "backend" in diff and not force_backend_switch:
            return (f"existing manifest backend={(existing or {}).get('backend')!r} != "
                    f"{intended.get('backend')!r}; pass --force-backend-switch (with --scene all).")
    return None


def merged_manifest(prior: dict[str, Any] | None, fresh: dict[str, Any],
                    storyboard_scene_ids: list[str]) -> dict[str, Any]:
    """--scene subset merges INTO the prior manifest: fresh entries win per
    scene_id, untouched prior entries survive, order follows the storyboard.
    Backstop only (T2a preflight already blocked identity mismatch before any
    synthesis): if identity somehow still differs, REFUSE rather than merge.
    No prior manifest -> just the fresh subset."""
    if not prior:
        return fresh
    mismatch = [k for k in _IDENTITY_KEYS if prior.get(k) != fresh.get(k)]
    if mismatch:
        raise SystemExit(
            f"[tts] refusing to merge a --scene subset into a manifest that differs on "
            f"{mismatch}; re-run the whole deck (--scene all) to rebuild it consistently.")
    by_id = {e["scene_id"]: e for e in prior.get("scenes", []) if e.get("scene_id")}
    by_id.update({e["scene_id"]: e for e in fresh.get("scenes", []) if e.get("scene_id")})
    out = {**prior, **{k: v for k, v in fresh.items() if k != "scenes"}}
    out["scenes"] = [by_id[sid] for sid in storyboard_scene_ids if sid in by_id]
    return out


# (scene_id, beat text_hash, occurrence of that hash within the scene) -- see build_reuse_index.
BeatReuseKey = tuple[str, str, int]


def _prune_empty_dir(directory: Path) -> None:
    """rmdir the directory iff it is now empty. Never an error otherwise: a sibling beat
    may still live there, and a leftover directory is cosmetic, not a failure."""
    try:
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()
    except OSError:
        pass


def _relocate(src: Path, dst: Path) -> bool:
    """Move one audio artifact onto the path today's deck wants. True iff it moved.

    Copy-then-delete rather than ``os.replace``: the copy is what protects BILLED audio
    (there is no instant at which zero copies exist, even across a crash), and the delete
    is what keeps the old scene-number directory from lingering as unmanaged audio --
    an orphan WAV under a stale ``NN_`` prefix is exactly what ``overwrite_guard``'s
    "WAVs exist but no manifest accounts for them" branch refuses to run over. The delete
    only happens once the copy is on disk at the same size.

    A missing source is a no-op: the recorded path is still rewritten so the manifest stays
    internally consistent, and ``make.py --reuse-audio``'s freshness check reports the
    missing WAV either way (it would have been missing under the old name too)."""
    if not src.exists() or src.resolve() == dst.resolve():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    if dst.exists() and dst.stat().st_size == src.stat().st_size:
        src.unlink()
        _prune_empty_dir(src.parent)
    return True


def _renumber_path(value: Any, scene_id: str, old_number: int, new_number: int) -> Any:
    """Rewrite the ``NN_<scene_id>`` prefix in every component of a recorded artifact path
    (``beats/17_sceneA/01_x.wav``, ``scenes/17_sceneA.wav``, ``align/17_sceneA.words.json``).
    Rewriting the RECORDED string rather than rebuilding from output_dir keeps a run that
    used ``--output-dir`` in its own layout. Non-strings and non-matches pass through."""
    if not isinstance(value, str) or not value:
        return value
    old_prefix, new_prefix = f"{old_number:02d}_{scene_id}", f"{new_number:02d}_{scene_id}"
    parts, hit = list(Path(value).parts), False
    for i, part in enumerate(parts):
        if part == old_prefix or part.startswith(old_prefix + "."):
            parts[i], hit = new_prefix + part[len(old_prefix):], True
    return str(Path(*parts)) if hit else value


def _renumber_entry(entry: dict[str, Any], scene_id: str, old_number: int, new_number: int,
                    *, relocate: bool) -> dict[str, Any]:
    """A copy of `entry` stamped with `new_number`, with every path-encoded artifact
    (scene WAV, align sidecars, beat WAVs) renamed -- and moved, unless `relocate` is off."""
    updated = {**entry, "scene_number": new_number}

    def fix(container: dict[str, Any], key: str) -> None:
        old = container.get(key)
        new = _renumber_path(old, scene_id, old_number, new_number)
        if new == old:
            return
        container[key] = new
        if relocate:
            _relocate(Path(old), Path(new))

    fix(updated, "audio_file")
    if isinstance(updated.get("alignment"), dict):
        alignment = dict(updated["alignment"])
        fix(alignment, "words_file")
        fix(alignment, "aligned_file")
        updated["alignment"] = alignment
    if isinstance(updated.get("beats"), list):
        beats = []
        for beat in updated["beats"]:
            beat = dict(beat)
            fix(beat, "audio_file")
            beats.append(beat)
        updated["beats"] = beats
    print(f"[tts] renumbered {scene_id}: scene {old_number:02d} -> {new_number:02d} "
          f"(current storyboard order)", flush=True)
    return updated


def renumber_scenes(manifest: dict[str, Any], scene_numbers: dict[str, int],
                    *, relocate: bool = True) -> dict[str, Any]:
    """Re-stamp every entry's ``scene_number`` from the CURRENT storyboard's full-deck
    order -- 1-based over every scene, intro/divider/content/outro all taking a number,
    the same counting ``rewatch_pack.py`` and ``critic.py`` use -- and move any artifact
    whose path encodes the old number.

    Fresh entries already carry today's numbering; entries CARRIED OVER by a ``--scene``
    subset merge carry whatever the deck looked like when they were last synthesized. On
    2026-09-13 that left ``derivative_of_cosine`` and ``slope_equals_height`` both numbered
    17 in one manifest and the critic's frame extractor collided on the number. A scene id
    is part of every artifact name, so renumbering can never make two scenes collide on a
    path, and the order in which entries are processed does not matter."""
    out: list[dict[str, Any]] = []
    for entry in manifest.get("scenes", []):
        new_number = scene_numbers.get(entry.get("scene_id"))
        old_number = entry.get("scene_number")
        if new_number is None or not isinstance(old_number, int) or old_number == new_number:
            out.append(entry)
        else:
            out.append(_renumber_entry(entry, entry["scene_id"], old_number, new_number,
                                       relocate=relocate))
    return {**manifest, "scenes": out}


def build_reuse_index(manifest: dict[str, Any] | None) -> dict[BeatReuseKey, dict[str, Any]]:
    """Beat reuse index keyed by CONTENT: ``(scene_id, beat text_hash, occurrence)`` ->
    the prior WAV plus the identity it was synthesized under.

    This used to be keyed by the beat's OUTPUT PATH, which is
    ``beats/<NN scene_number>_<scene_id>/<NN index>_<reveal>.wav`` -- a name that encodes
    the deck's scene ORDER and the beat's reveal id, neither of which has anything to do
    with what the voice says. So two edits that changed not one spoken word still shifted
    every path and re-billed whole scenes (both measured 2026-09-13): (a) reordering
    scenes bumps <NN scene_number> for everything after the move, (b) adding or removing a
    ``{show}`` marker renames that beat and renumbers the ones after it. Content-addressing
    makes "same scene, same words, same voice" the reuse test it was always meant to be;
    the WAV is then moved onto whatever path today's deck wants (``_relocate``).

    ``occurrence`` settles the rare case of two beats with identical text inside one scene:
    prior beats are numbered in manifest order, new ones in storyboard order, so the n-th
    such beat pairs with the n-th prior one and no WAV is handed out twice.
    """
    if not manifest:
        return {}
    shared = {k: manifest.get(k) for k in ("backend", "model", "voice", "style")}
    index: dict[BeatReuseKey, dict[str, Any]] = {}
    for scene in manifest.get("scenes", []):
        scene_id = scene.get("scene_id")
        seen: dict[str, int] = {}
        for beat in scene.get("beats", []):
            audio_file, beat_hash = beat.get("audio_file"), beat.get("text_hash")
            if not scene_id or not audio_file or not beat_hash:
                continue
            occurrence = seen.get(beat_hash, 0)
            seen[beat_hash] = occurrence + 1
            index[(scene_id, beat_hash, occurrence)] = {**shared, "audio_file": audio_file}
    return index


def build_scene_reuse_index(manifest: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    """Reuse index keyed by scene_id, from a prior manifest's scene_aligned entries.
    Carries what §3 freshness needs so TTS can be skipped when only downstream
    (reveal/beat-count) changed. (Per-beat build_reuse_index stays for the beat path.)

    It also carries the alignment sidecar paths, because the scene WAV and both sidecars
    are named ``<NN scene_number>_<scene_id>`` -- the same scene-order-encoding naming the
    beat path had. Keying by scene_id was always right about WHICH audio belongs to this
    scene; adopt_prior_scene_artifacts is what moves it onto today's number so the
    freshness check can find it after a deck reorder."""
    if not manifest:
        return {}
    shared = {k: manifest.get(k) for k in ("backend", "model", "voice", "style")}
    out: dict[str, dict[str, Any]] = {}
    for scene in manifest.get("scenes", []):
        if scene.get("narration_mode") != "scene_aligned":
            continue
        alignment = scene.get("alignment")
        alignment = alignment if isinstance(alignment, dict) else {}
        out[scene.get("scene_id")] = {
            **shared,
            "scene_text_hash": scene.get("scene_text_hash"),
            "audio_file": scene.get("audio_file"),
            "audio_seconds": scene.get("audio_seconds"),
            "words_file": alignment.get("words_file"),
            "aligned_file": alignment.get("aligned_file"),
        }
    return out


def adopt_prior_scene_artifacts(
    prior: dict[str, Any] | None, *, scene_wav: Path, words_file: Path, aligned_file: Path,
) -> tuple[dict[str, Any] | None, str | None]:
    """Move a prior scene_aligned scene's artifacts onto TODAY's scene number.
    Returns (prior with its recorded paths rewritten, the WAV's old path or None).

    Why this is needed even though the index is keyed by scene_id: the WAV lives at
    ``scenes/<NN scene_number>_<scene_id>.wav`` and the sidecars at
    ``align/<NN>_<scene_id>.{words,aligned}.json``, and scene_reuse_ok used to be handed
    today's path. So a reordered deck found nothing there and re-synthesized a scene whose
    words had not changed -- the same class of re-bill the beat path had, one level up.
    Relocating first makes the freshness check ask about the audio that actually exists.

    Unconditional (not gated on the reuse verdict): when the text DID change, the scene is
    re-synthesized to a temp and promoted onto scene_wav only after gates pass, so the
    moved file is never lost before a good replacement exists -- and moving it means no
    orphan WAV is left behind under the stale number. Same copy -> verify size -> delete ->
    prune rule as the beat path. Paths that are not non-empty strings are skipped (the
    manifest's own output, but an alignment block is not type-validated by
    read_manifest_status, so this stays defensive)."""
    if not prior:
        return prior, None
    updated, moved_from = dict(prior), None
    for key, dst in (("audio_file", scene_wav), ("words_file", words_file),
                     ("aligned_file", aligned_file)):
        src = prior.get(key)
        if not isinstance(src, str) or not src:
            continue
        if _relocate(Path(src), dst) and key == "audio_file":
            moved_from = src
        updated[key] = str(dst)
    return updated, moved_from


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
    request: TTSRequest,
    *,
    backend_name: str,
    reuse_index: dict[BeatReuseKey, dict[str, Any]],
    key: BeatReuseKey,
) -> tuple[Path | None, str]:
    """(prior WAV this beat can adopt, "") or (None, reason). The text hash is IN the key,
    so a hit already means "same scene, same words"; what is left to check is the synthesis
    identity and that the file is still on disk. Where that WAV must end up is the caller's
    business -- reuse no longer depends on it already being at the right path."""
    prior = reuse_index.get(key)
    if prior is None:
        return None, "no prior beat with this text in this scene (text changed, or new beat)"
    expected = {
        "backend": backend_name,
        "model": request.model,
        "voice": request.voice,
        "style": request.style,
    }
    for field, value in expected.items():
        if prior.get(field) != value:
            return None, f"{field} changed"
    src = Path(prior["audio_file"])
    if not src.exists():
        return None, f"prior WAV is gone ({src})"
    return src, ""


def build_backend(args: argparse.Namespace) -> TTSBackend:
    if args.backend == "mock":
        return MockTTSBackend(args.empty_beat_seconds)
    load_dotenv()
    api_key = os.environ.get("MIMO_API_KEY")
    if not api_key:
        raise SystemExit("[tts] --backend mimo needs the API key in env MIMO_API_KEY.")
    backend = MimoTTSBackend(
        base_url=args.base_url, api_key=api_key, max_retries=args.max_retries
    )
    cap = 0 if getattr(args, "no_billing", False) else getattr(args, "max_billed_calls", None)
    return BudgetedBackend(backend, cap) if cap is not None else backend


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
    reuse_index: dict[BeatReuseKey, dict[str, Any]],
    reuse_key: BeatReuseKey | None = None,
) -> SynthesizedBeat:
    if reuse_existing and reuse_key is not None:
        src, reason = reusable_existing_beat(
            request,
            backend_name=backend_name,
            reuse_index=reuse_index,
            key=reuse_key,
        )
        if src is not None:
            moved = _relocate(src, output_path)
            # consume the entry: one prior WAV is handed out at most once, so two beats
            # with identical text in a scene pair off by index instead of sharing a take.
            reuse_index.pop(reuse_key, None)
            if moved:
                print(f"[tts] reused {output_path.name} (moved from {src})", flush=True)
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
    reuse_index: dict[BeatReuseKey, dict[str, Any]],
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
    reuse_index: dict[BeatReuseKey, dict[str, Any]],
) -> dict[str, Any]:
    voice = args.voice or default_voice_for_model(meta)
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

    seen_hashes: dict[str, int] = {}
    for beat in beats:
        beat_path = beat_dir / f"{beat['index']:02d}_{safe_stem(beat['reveal'] or beat['id'])}.wav"
        beat_hash = text_hash(beat["text"])
        occurrence = seen_hashes.get(beat_hash, 0)
        seen_hashes[beat_hash] = occurrence + 1
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
            reuse_key=(scene_id, beat_hash, occurrence),
        )
        duration = synth.duration
        beat_paths.append(beat_path)
        beat_entry = {
            **beat,
            "audio_file": str(beat_path.resolve()),
            "audio_seconds": round(duration, 3),
            "start_seconds": round(timeline, 3),
            "end_seconds": round(timeline + duration, 3),
            "text_hash": beat_hash,
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


def _asr_probe_tokens(wav: Path, args: argparse.Namespace) -> tuple[list | None, str]:
    """Free ASR (whisper-timestamped) -> (normalized tokens, reason) for the QA probe
    (design §6). Advisory: (None, reason) if the probe cannot run (missing dep/model),
    so a probe failure never blocks synthesis -- but the reason is RECORDED (F8) so a
    silent skip is never mistaken for a pass. success -> (tokens, "ran")."""
    from pipeline import scene_align as SA
    try:
        import whisper_timestamped as wt
    except ImportError:
        return None, "skipped: whisper_timestamped not installed"
    try:
        model = wt.load_model(args.aligner_model, device=args.aligner_device)
        result = wt.transcribe(model, str(wav), language="en")
    except Exception as exc:  # noqa: BLE001 - probe is advisory, never fatal
        return None, f"error: {exc}"
    text = " ".join(seg.get("text", "") for seg in result.get("segments", []))
    return SA.tokenize(text), "ran"


def _finalize_aligned(*, plan: dict[str, Any], words: list[dict[str, Any]],
                      multi: dict[int, dict[str, Any]], segments: list[dict[str, Any]],
                      summary: dict[str, Any], audio_seconds: float, scene_number: int,
                      words_file: Path, aligned_file: Path, audio_file: Path,
                      args: argparse.Namespace, qa_wav: Path | None, promote_from: Path | None,
                      chunks: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Shared tail for both scene paths (single-shot + sentence-chunk): map to beats,
    run gates (+ optional ASR QA probe over `qa_wav`), assemble the entry, and -- only on
    PASS -- promote the WAV and atomically write the words/aligned artifacts. Both paths
    gate by the SAME rules, so chunk output can never ship under a looser bar."""
    from pipeline import scene_align as SA
    from pipeline import atomicio
    beats = SA.map_to_beats(plan, words, audio_seconds, multi=multi)
    gates = SA.run_gates(plan, words, beats, audio_seconds)
    # QA probe outcome ALWAYS lands in gates["qa"] as one of ran/skipped/error (F8:
    # previously the verdict was dropped and a missing dep skipped silently). Adv2
    # policy: only an intentional --skip-qa is silent; any other "should have run but
    # didn't" (no dep, exception, unexpectedly no qa wav) prints a loud "NOT a pass".
    if getattr(args, "skip_qa", False):
        gates = {**gates, "qa": {"status": "skipped", "reason": "--skip-qa (intentional)"}}
    else:
        asr, note = (None, "skipped: no qa wav on this path") if qa_wav is None \
            else _asr_probe_tokens(qa_wav, args)
        if asr is None:
            status = "error" if note.startswith("error") else "skipped"
            gates = {**gates, "qa": {"status": status, "reason": note}}
            print(f"[tts] WARN {plan['scene_id']}: ASR QA probe did not run ({note}) -- "
                  f"this is NOT a pass", flush=True)
        else:
            fa_probs = [w.get("probability") for w in words]
            qa = SA.qa_diff(SA.tokenize(plan["transcript"]), asr, fa_probs,
                            weak_spans=SA.boundary_weak_spans(beats))
            gates = {**gates, "qa": {"status": "ran", **qa}}
            if qa["verdict"] == "fail":
                gates["status"] = "fail"
                gates["failures"] = gates["failures"] + ["QA probe: suspect TTS misspeak"]
    entry = SA.build_scene_aligned_entry(
        scene_number=scene_number, plan=plan, beats=beats, audio_seconds=audio_seconds,
        audio_file=audio_file, summary=summary, gates=gates,
        words_file=words_file, aligned_file=aligned_file, chunks=chunks)
    if gates["status"] in ("pass", "pass_with_warnings"):
        if promote_from is not None:
            atomicio.promote(promote_from, Path(audio_file))
        atomicio.atomic_write_json(words_file, {
            "summary": summary, "words": words, "segments": segments})
        atomicio.atomic_write_json(aligned_file, {
            "scene_id": plan["scene_id"], "audio_seconds": round(audio_seconds, 3), "beats": beats})
    return entry


def _align_and_gate(plan: dict[str, Any], wav: Path, scene_number: int,
                    words_file: Path, aligned_file: Path, args: argparse.Namespace, *,
                    audio_file: Path, promote_from: Path | None,
                    aligner_model: str | None = None) -> dict[str, Any]:
    """Single-shot path: align the whole-scene `wav` to the plan, then finalize
    (map/gate/build/verify-before-overwrite). On aligner abort, return a fail-status
    entry so the caller routes to the fallback ladder -> beats terminal (design "always
    a shippable path") instead of crashing the deck."""
    from pipeline import scene_align as SA
    model = aligner_model or args.aligner_model
    try:
        res = SA.align_scene(wav, plan, model=model, device=args.aligner_device)
    except SA.AlignmentError as exc:
        return {"scene_id": plan["scene_id"], "narration_mode": "scene_aligned",
                "validation": {"status": "fail", "warnings": [], "metrics": {},
                               "error": f"alignment aborted: {exc}"},
                "fallback_history": []}
    return _finalize_aligned(
        plan=plan, words=res["words"], multi=res["multi"], segments=res["segments"],
        summary=res["summary"], audio_seconds=wav_duration(wav), scene_number=scene_number,
        words_file=words_file, aligned_file=aligned_file, audio_file=audio_file,
        args=args, qa_wav=wav, promote_from=promote_from)


def _synth_align_chunks(backend, plan, chunk_texts, voice, args, chunk_dir, concat_tmp):
    """Rung 3 core: synth each sentence chunk to its OWN WAV (one TTS call each -- billed for
    mimo), align each independently (short spans align more reliably than the full scene),
    concat the WAVs into concat_tmp, and merge the alignments onto one clock. chunk_dir and
    concat_tmp are supplied by the caller so it can clean them in a finally on ANY failure.
    Returns (merged, total_seconds). May raise AlignmentError (chunk abort / merged-token
    break) or a synth/IO error -- the caller catches broadly and demotes to the beats terminal."""
    from pipeline import scene_align as SA
    chunk_dir.mkdir(parents=True, exist_ok=True)
    chunk_wavs: list[Path] = []
    chunk_results: list[dict[str, Any]] = []
    chunk_durations: list[float] = []
    for i, text in enumerate(chunk_texts):
        cwav = chunk_dir / f"chunk_{i:02d}.wav"
        _synth_scene_wav(backend, {"transcript": text}, cwav, voice, args)       # 1 TTS call
        res = SA.align_scene(cwav, {"transcript": text, "beats": []},
                             model=args.aligner_model, device=args.aligner_device)
        chunk_wavs.append(cwav)
        chunk_results.append(res)
        chunk_durations.append(wav_duration(cwav))
    total = concat_wavs(chunk_wavs, concat_tmp)
    merged = SA.merge_chunk_alignments(chunk_results, chunk_durations, chunk_texts, plan)
    return merged, total


def _cleanup_chunk_temps(chunk_dir: Path, concat_tmp: Path) -> None:
    """Remove every chunk temp on ANY exit path (design §3 verify-before-overwrite). concat_tmp
    is already gone when it was promoted onto the canonical WAV, so the unlink is a no-op there;
    it never touches the canonical scene WAV (a different path)."""
    concat_tmp.unlink(missing_ok=True)
    if chunk_dir.exists():
        for f in chunk_dir.iterdir():
            f.unlink(missing_ok=True)
        try:
            chunk_dir.rmdir()
        except OSError:
            pass


def _build_fallback_rungs(backend, meta, scene, scene_number, output_dir, args, plan, reuse_index):
    """Design §7 ladder rungs for one failed scene: arbiter (free small.en re-align) ->
    resynth (1 billed call) -> chunk (sentence-chunk resynth+merge) -> beats (budget-exempt
    terminal -- still bills once per non-empty beat under MiMo, NOT free).
    Each rung callable takes the ctx dict from _synthesize_scene_aligned, which carries the
    RetryBudget. The chunk rung is declared NOT billed to run_ladder because it fans out to ONE
    TTS call per sentence and must account for that itself: it RESERVES N units of the budget up
    front and DECLINES (routing to beats) when N would exceed the quote, so the budget still
    bounds real billed calls (Codex R-item2). Consequence: under the default budget of 2 a
    multi-sentence scene declines chunk and demotes to beats; chunk engages only when the operator
    raises --fallback-budget to cover the fan-out (quoted per CLAUDE.md)."""
    from pipeline import scene_align as SA
    scene_id = scene["id"]
    scenes_dir, align_dir = output_dir / "scenes", output_dir / "align"
    scene_wav = scenes_dir / f"{scene_number:02d}_{scene_id}.wav"
    words_file = align_dir / f"{scene_number:02d}_{scene_id}.words.json"
    aligned_file = align_dir / f"{scene_number:02d}_{scene_id}.aligned.json"
    voice = args.voice or default_voice_for_model(meta)

    def _ok(entry):
        return entry["validation"]["status"] in ("pass", "pass_with_warnings")

    def _fail(error):
        return {"scene_id": scene_id, "narration_mode": "scene_aligned",
                "validation": {"status": "fail", "warnings": [], "metrics": {}, "error": error},
                "fallback_history": []}

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

    def chunk(ctx):
        # split the scene into sentences; a scene with no interior break has nothing to gain
        # over the resynth already tried, so decline and let the beats terminal run.
        chunk_texts = SA.split_sentence_chunks(plan["transcript"])
        if len(chunk_texts) < 2:
            return {"status": "fail", "entry": _fail("single sentence -- no chunk benefit"),
                    "reason": "chunk declined: one sentence"}
        # each chunk is a billed sub-synth: RESERVE N budget units up front and decline (->
        # beats) rather than overrun the consent quote (Codex R-item2 blocking 1).
        budget = ctx["budget"]
        need = len(chunk_texts)
        left = budget.max_billed - budget.spent
        if need > left:
            return {"status": "fail",
                    "entry": _fail(f"chunk needs {need} sub-synths, only {left} of billed budget left"),
                    "reason": f"chunk declined: {need} sub-synths > {left} budget "
                              f"(raise --fallback-budget with a quote to enable)"}
        budget.spent += need
        chunk_dir = scene_wav.with_name(scene_wav.stem + ".chunks")
        concat_tmp = scene_wav.with_name(scene_wav.name + ".chunk.tmp")
        try:
            merged, total = _synth_align_chunks(backend, plan, chunk_texts, voice, args,
                                                chunk_dir, concat_tmp)
            entry = _finalize_aligned(
                plan=plan, words=merged["words"], multi=merged["multi"], segments=merged["segments"],
                summary=merged["summary"], audio_seconds=total, scene_number=scene_number,
                words_file=words_file, aligned_file=aligned_file, audio_file=scene_wav,
                args=args, qa_wav=concat_tmp, promote_from=concat_tmp, chunks=merged["chunks"])
            ok = _ok(entry)
            reason = f"sentence-chunk resynth+merge: {need} chunks ({need} billed sub-synths)"
        except Exception as exc:   # noqa: BLE001 -- a fallback rescue must NEVER crash the deck:
            entry, ok = _fail(f"chunk failed: {exc}"), False   # any synth/align/concat error -> beats
            reason = f"chunk failed: {exc}"
        finally:
            _cleanup_chunk_temps(chunk_dir, concat_tmp)
        return {"status": "pass" if ok else "fail", "entry": entry, "reason": reason}

    def beats(ctx):
        entry = _synthesize_scene_beats(backend=backend, meta=meta, scene=scene,
            scene_number=scene_number, output_dir=output_dir, args=args, reuse_index=reuse_index)
        return {"status": "pass", "entry": entry, "reason": "beat-level fallback (terminal)"}

    return [("arbiter", False, arbiter), ("resynth", True, resynth),
            ("chunk", False, chunk), ("beats", False, beats)]


def _synthesize_scene_aligned(*, backend, meta, scene, scene_number, output_dir, args,
                              reuse_index, scene_reuse_index):
    """Scene-level path (design §3 storage + verify-before-overwrite + §7 ladder). The
    WAV is synthesized to a temp path and promoted onto the canonical path ONLY after
    gates pass, so a prior good WAV is never clobbered by a bad re-synth."""
    from pipeline import scene_align as SA
    from pipeline import scene_fallback as FB
    voice = args.voice or default_voice_for_model(meta)
    scene_id = scene["id"]
    plan = SA.build_scene_plan(scene)
    scenes_dir, align_dir = output_dir / "scenes", output_dir / "align"
    scene_wav = scenes_dir / f"{scene_number:02d}_{scene_id}.wav"
    words_file = align_dir / f"{scene_number:02d}_{scene_id}.words.json"
    aligned_file = align_dir / f"{scene_number:02d}_{scene_id}.aligned.json"

    # Bring the prior scene's artifacts onto TODAY's number FIRST: their names encode the
    # scene order, so after a reorder the freshness check below would otherwise look at an
    # empty path and re-bill a scene whose words never changed.
    prior_scene, moved_from = adopt_prior_scene_artifacts(
        scene_reuse_index.get(scene_id), scene_wav=scene_wav,
        words_file=words_file, aligned_file=aligned_file)

    # (§3) reuse: if the existing WAV is fresh, skip TTS and just re-map+re-validate (free).
    if scene_reuse_ok(prior_scene, plan, scene_wav,
                      backend_name=backend.name, voice=voice, args=args):
        if moved_from:
            print(f"[tts] reused {scene_wav.name} (moved from {moved_from})", flush=True)
        entry = _align_and_gate(plan, scene_wav, scene_number, words_file, aligned_file,
                                args, audio_file=scene_wav, promote_from=None)
        if entry["validation"]["status"] in ("pass", "pass_with_warnings"):
            return entry   # else fall through to resynth
    elif moved_from:
        print(f"[tts] {scene_id}: prior scene audio moved onto {scene_wav.name} "
              f"(from {moved_from}) but is not reusable; synthesizing", flush=True)

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
    ctx = {"plan": plan, "primary_wav": tmp_wav, "scene_wav": scene_wav, "budget": budget}
    rungs = _build_fallback_rungs(backend, meta, scene, scene_number, output_dir, args, plan, reuse_index)
    result = FB.run_ladder(scene_id=scene_id, rungs=rungs, budget=budget, ctx=ctx)
    tmp_wav.unlink(missing_ok=True)   # clean the primary temp after the ladder settles
    return result["entry"]


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    from pipeline.atomicio import atomic_write_json
    atomic_write_json(path, manifest)


def main() -> int:
    args = parse_args()
    if args.fallback_budget < 0:                       # NA2: unconditional, not just in dry-run
        raise SystemExit("[tts] --fallback-budget must be >= 0")
    data = load_storyboard(args.storyboard)
    stale = check_derived_freshness(args.storyboard.resolve(), data)
    if stale:
        raise SystemExit(f"[freshness] {stale}")
    meta = data["meta"]
    scenes = wanted_scenes(data["scenes"], args.scene)
    sec_dir = _bootstrap.section_output_dir(meta)
    default_audio_subdir = "audio_mimo" if meta["id"].endswith("_mimo") else "audio"
    output_dir = (
        args.output_dir
        or (sec_dir / default_audio_subdir)
    ).resolve()
    manifest_path = (args.manifest or (output_dir / "manifest.json")).resolve()
    voice = args.voice or default_voice_for_model(meta)
    existing, status = read_manifest_status(manifest_path)
    intended = {"deck_id": meta["id"], "backend": args.backend, "model": args.model,
                "voice": voice, "style": args.style, "sample_rate": 24_000, "channels": 1,
                "sample_width": 2, "output_dir": str(output_dir)}
    abort = overwrite_guard(status=status, existing=existing, intended=intended,
                            scene_sel=args.scene, output_dir=output_dir,
                            force_backend_switch=args.force_backend_switch,
                            force_clobber=args.force_clobber)
    identity_diff = status == "ok" and any((existing or {}).get(k) != intended.get(k)
                                           for k in _IDENTITY_KEYS)
    # Reuse index only when asked AND identity unchanged (R3-B2). A DRY-RUN builds it too
    # -- read-only, nothing written or moved -- because the whole point of dry-run is to
    # answer "does this edit cost anything?" BEFORE the call is made, and with the
    # content key that answer is now "no" for a pure {show}/scene-order edit. The dry-run
    # branch below says loudly when that zero depends on --reuse-existing being passed.
    use_reuse = (args.reuse_existing or args.dry_run) and not identity_diff
    reuse_index = build_reuse_index(existing) if use_reuse else {}              # per-beat (beat path)
    scene_reuse_index = build_scene_reuse_index(existing) if use_reuse else {}  # per-scene (scene path)
    if args.reuse_existing and existing is None:
        print(
            "[tts] --reuse-existing requested but no valid prior manifest was found; "
            "existing WAV files will not be trusted blindly.",
            flush=True,
        )

    content_count = sum(1 for scene in scenes if scene.get("kind", "content") == "content")
    beat_count = sum(len(scene_beats(scene)) for scene in scenes if scene.get("kind", "content") == "content")
    all_scenes = data["scenes"]
    scene_numbers = {scene["id"]: index for index, scene in enumerate(all_scenes, start=1)}
    if args.dry_run:
        # dry-run is read-only: never enforce the guard (R3-A1 -- the quote flow needs
        # dry-run to still print an estimate), but surface that a real run WOULD abort.
        if abort:
            print(f"[dry-run] NOTE: a real run WOULD abort -> {abort}")
        # `plan` = first-round calls, reuse APPLIED: the reuse test is now content-addressed
        # (scene_id + text hash + identity), so "I only moved a {show} marker / reordered
        # scenes" shows up here as 0 before any money moves. `reuse` = billable units the
        # existing audio already covers; `no-reuse` on the TOTAL line is the same count with
        # reuse ignored, so the pessimistic quote is still on screen. `worst` stays
        # reuse-BLIND for scene-unit scenes (a reused WAV can still fail re-alignment and
        # fall down the ladder) and equals `plan` for beat-unit scenes (no ladder there).
        # Empty beats write silence without hitting the backend, so they count 0 calls.
        # Scene unit: 1 synth + budget billed rungs 2-3 + one billed beat per NON-EMPTY
        # beat at the terminal (F6/T3-2).
        from pipeline import scene_align as SA     # manim-free; pure functions on this path
        sim_index = dict(reuse_index)              # consumed like the real run, on a copy
        rows, planned, worst, est_secs, no_reuse = [], 0, 0, 0.0, 0
        for scene in scenes:
            if scene.get("kind", "content") != "content":
                continue
            unit = resolve_unit(args.unit, scene)
            beats = scene_beats(scene)
            nonempty = [b for b in beats if (b.get("text") or "").strip()]
            est_secs += sum(estimate_seconds(b["text"]) if (b.get("text") or "").strip()
                            else args.empty_beat_seconds for b in beats)
            if unit == "scene":
                # A real run relocates the prior WAV onto today's number before its
                # freshness check; dry-run moves nothing, so it asks about the path the
                # WAV is at NOW -- otherwise a reordered deck would be quoted for calls
                # the real run will not make.
                prior_scene = scene_reuse_index.get(scene["id"]) or {}
                scene_wav = Path(prior_scene.get("audio_file") or (
                    output_dir / "scenes" / f"{scene_numbers[scene['id']]:02d}_{scene['id']}.wav"))
                covered = int(scene_reuse_ok(
                    prior_scene or None, SA.build_scene_plan(scene), scene_wav,
                    backend_name=args.backend, voice=voice, args=args))
                p, wc, p0 = 1 - covered, 1 + args.fallback_budget + len(nonempty), 1
            else:
                covered, seen = 0, {}
                for beat in beats:
                    beat_hash = text_hash(beat["text"])
                    occurrence = seen.get(beat_hash, 0)
                    seen[beat_hash] = occurrence + 1
                    if not (beat.get("text") or "").strip():
                        continue
                    key = (scene["id"], beat_hash, occurrence)
                    src, _ = reusable_existing_beat(
                        TTSRequest(text=beat["text"], model=args.model, voice=voice,
                                   style=args.style),
                        backend_name=args.backend, reuse_index=sim_index, key=key)
                    if src is not None:
                        sim_index.pop(key, None)
                        covered += 1
                p = wc = len(nonempty) - covered
                p0 = len(nonempty)
            planned += p; worst += wc; no_reuse += p0
            rows.append((scene["id"], unit, len(beats), len(nonempty), covered, p, wc))
        print(f"[dry-run] backend={args.backend} model={args.model} voice={voice} unit={args.unit} "
              f"(prior manifest: {'reusable' if reuse_index or scene_reuse_index else 'none/unusable'})")
        print(f"[dry-run] {'scene':<30}{'unit':<7}{'beats':>6}{'calls':>6}{'reuse':>6}{'plan':>5}{'worst':>7}")
        for sid, unit, nb, nc, rc, p, wc in rows:
            print(f"[dry-run] {sid:<30}{unit:<7}{nb:>6}{nc:>6}{rc:>6}{p:>5}{wc:>7}")
        print(f"[dry-run] TOTAL content-scenes={len(rows)}  planned first-round calls={planned}  "
              f"(no-reuse: {no_reuse})  worst-case incl. fallback ladder={worst}  "
              f"est narration ~{est_secs/60:.1f} min")
        if planned < no_reuse and not args.reuse_existing:
            print(f"[dry-run] NOTE: planned={planned} ASSUMES --reuse-existing. Without that "
                  f"flag the reuse index is empty and this run bills {no_reuse} calls "
                  f"(2026-09-12: that omission is exactly how 13 calls got spent).")
        return 0
    if abort:
        raise SystemExit(f"[tts] {abort}")

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

    # Billing receipt for THIS run (added to the fresh manifest BEFORE any merge, so
    # merged_manifest's fresh-top-level-wins keeps this run's numbers). beat mode:
    # backend_calls == non-empty beats (empty beats never reach the backend).
    manifest["receipt"] = {
        "backend_calls": getattr(backend, "stats", {}).get("calls", 0),
        "backend_retries": getattr(backend, "stats", {}).get("retries", 0),
        "modes": {m: sum(1 for e in manifest["scenes"] if e.get("narration_mode") == m)
                  for m in ("scene_aligned", "beats", "silent")},
        "fallback_scenes": [e["scene_id"] for e in manifest["scenes"] if e.get("fallback_history")],
    }
    print(f"[tts] receipt: {json.dumps(manifest['receipt'], ensure_ascii=False)}", flush=True)

    if args.scene != "all":
        # F5: a subset run must merge into the prior manifest, not overwrite it whole
        # (identity already vetted by the T2a preflight guard; merged_manifest re-checks
        # as a backstop). `existing` is the prior manifest read at the top of main().
        manifest = merged_manifest(existing, manifest, [s["id"] for s in all_scenes])
    # Every entry gets TODAY's full-deck scene number: the freshly synthesized ones already
    # have it, the ones a subset merge carried over from the prior manifest may not (that
    # is how two scenes both ended up numbered 17 on 2026-09-13).
    manifest = renumber_scenes(manifest, scene_numbers)
    write_manifest(manifest_path, manifest)
    print(f"[done] wrote {manifest_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

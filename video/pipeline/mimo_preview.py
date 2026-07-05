"""Synthesize a spoken-narration markdown (Version B) with MiMo-V2.5-TTS.

This is the "hear the effect" driver for the dual-version narration route: it
reads the per-unit spoken text from a ``*_narration_spoken.md`` file (math already
spelled out -- MiMo cannot read LaTeX), synthesizes one WAV per unit via the MiMo
backend, and concatenates them (with a small gap) into a single preview WAV.

It deliberately does NOT go through the storyboard/beat machinery: the spoken
versions are per-unit prose, not beat-split, and the goal here is to audition the
voice, not to drive a timed render.

    # validate parsing with no API key / no calls:
    python video/pipeline/mimo_preview.py --spoken video/content_scripts/ch01_inverse_functions_narration_spoken.md --dry-run
    # one billed/real call (first unit) to confirm the API shape:
    python video/pipeline/mimo_preview.py --spoken ...spoken.md --smoke
    # full preview (needs env MIMO_API_KEY; defaults to built-in voice Dean):
    python video/pipeline/mimo_preview.py --spoken ...spoken.md
    # audition a different built-in voice:
    python video/pipeline/mimo_preview.py --spoken ...spoken.md --voice Mia
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()

from pipeline.audio import concat_wavs, silence_pcm, wav_duration, write_pcm_wav  # noqa: E402
from pipeline.tts import (  # noqa: E402
    MIMO_MODEL,
    MIMO_STYLE,
    MimoTTSBackend,
    TTSRequest,
    default_voice_for_model,
    load_dotenv,
    safe_stem,
)

_HEADING = re.compile(r"^###\s+(u\d+)\s+·\s+(.+?)\s*$")


def parse_spoken(path: Path) -> list[dict[str, str]]:
    """Pull (unit_id, label, text) out of a *_narration_spoken.md file.

    Each spoken unit is a ``### uNN · id`` heading followed by one prose
    paragraph. Lines starting with ``>`` (per-unit style notes) and anything
    after a blank line are not part of the spoken text.
    """
    units: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    buffer: list[str] = []

    def flush() -> None:
        if current is not None:
            text = " ".join(buffer).strip()
            if text:
                units.append({**current, "text": text})

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        heading = _HEADING.match(line)
        if heading:
            flush()
            current = {"id": heading.group(1), "label": heading.group(2)}
            buffer = []
            continue
        if current is None:
            continue
        if not line.strip():
            flush()
            current = None  # paragraph ended; ignore later notes for this unit
            buffer = []
            continue
        if line.lstrip().startswith((">", "#", "-", "|", "```")):
            continue
        buffer.append(line.strip())
    flush()
    return units


def parse_args() -> argparse.Namespace:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spoken", required=True, type=Path,
                        help="path to a *_narration_spoken.md (Version B)")
    parser.add_argument("--voice", default=os.environ.get("MIMO_TTS_VOICE"),
                        help="MiMo preset voice, or logical label for voice design")
    parser.add_argument("--model", default=MIMO_MODEL)
    parser.add_argument("--style", default=MIMO_STYLE)
    parser.add_argument("--base-url", default=os.environ.get("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1"))
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--units", help="comma-separated unit ids (e.g. u2,u5); default all")
    parser.add_argument("--gap", type=float, default=0.6, help="seconds of silence between units")
    parser.add_argument("--smoke", action="store_true", help="synthesize only the first selected unit")
    parser.add_argument("--reuse-existing", action="store_true", help="skip units whose WAV already exists")
    parser.add_argument("--dry-run", action="store_true", help="parse + print plan; never calls the API")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    units = parse_spoken(args.spoken)
    if args.units:
        wanted = {u.strip() for u in args.units.split(",") if u.strip()}
        units = [u for u in units if u["id"] in wanted]
    if args.smoke:
        units = units[:1]
    if not units:
        print("[mimo] no spoken units parsed -- check --spoken / --units.", flush=True)
        return 1

    deck = args.spoken.stem.replace("_narration_spoken", "")
    out_dir = (args.output_dir
               or (_bootstrap.REPO_ROOT / "video" / "output" / "audio" / f"{deck}_mimo_preview")).resolve()
    unit_dir = out_dir / "units"

    voice = args.voice or default_voice_for_model()
    total_words = sum(len(u["text"].split()) for u in units)
    print(f"[mimo] {deck}: {len(units)} unit(s), ~{total_words} words, "
          f"voice={voice}, model={args.model}", flush=True)

    if args.dry_run:
        for u in units:
            print(f"  {u['id']:>4} · {u['label']:<24} {len(u['text'].split()):>3}w  "
                  f"{u['text'][:70]}...", flush=True)
        print(f"[dry-run] would write {len(units)} unit WAV(s) + preview.wav under {out_dir}",
              flush=True)
        print("[dry-run] no key used, no request sent.", flush=True)
        return 0

    api_key = os.environ.get("MIMO_API_KEY")
    if not api_key:
        print("[mimo] needs the API key in env MIMO_API_KEY (never pass it as a flag).", flush=True)
        return 2

    backend = MimoTTSBackend(base_url=args.base_url, api_key=api_key)
    unit_dir.mkdir(parents=True, exist_ok=True)

    gap_path = out_dir / "_gap.wav"
    if args.gap > 0:
        write_pcm_wav(gap_path, silence_pcm(args.gap))

    sequence: list[Path] = []
    for index, unit in enumerate(units, start=1):
        wav_path = unit_dir / f"{index:02d}_{safe_stem(unit['id'])}.wav"
        if wav_path.exists() and args.reuse_existing:
            dur = wav_duration(wav_path)
        else:
            print(f"[mimo] {unit['id']} ({unit['label']}) ...", flush=True)
            result = backend.synthesize(
                TTSRequest(text=unit["text"], model=args.model, voice=voice, style=args.style)
            )
            write_pcm_wav(wav_path, result.pcm, sample_rate=result.sample_rate,
                          channels=result.channels, sample_width=result.sample_width)
            dur = wav_duration(wav_path)
        print(f"       -> {wav_path.name}  {dur:.1f}s", flush=True)
        if sequence and args.gap > 0:
            sequence.append(gap_path)
        sequence.append(wav_path)

    preview = out_dir / "preview.wav"
    total = concat_wavs(sequence, preview)
    print(f"[done] {len(units)} unit(s) -> {preview}  ({total:.1f}s total)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import wave
from importlib.resources import files
from pathlib import Path

from shared_media_paths import (
    DEFAULT_DECK_ID,
    audio_dir_path,
    audio_manifest_path,
    deck_json_path,
)
from shared_runtime_bootstrap import (
    F5_DEPS_DIR,
    HF_CACHE_DIR,
    REPO_ROOT,
    bootstrap_repo_deps,
    ensure_directory,
    require_path,
)
from slides_script_workflow import final_script_path, load_slide_scripts

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

bootstrap_repo_deps(F5_DEPS_DIR)

import numpy as np
import soundfile as sf
import torch
import yaml
import imageio_ffmpeg
from huggingface_hub import hf_hub_download
from transformers import pipeline

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
os.environ.setdefault("IMAGEIO_FFMPEG_EXE", FFMPEG_EXE)
os.environ["PATH"] = str(Path(FFMPEG_EXE).parent) + os.pathsep + os.environ.get("PATH", "")

from f5_tts.infer.utils_infer import infer_process, load_model, load_vocoder, preprocess_ref_audio_text
from f5_tts.model.backbones.dit import DiT
from f5_tts.model.backbones.mmdit import MMDiT
from f5_tts.model.backbones.unett import UNetT


DEFAULT_REFERENCE = REPO_ROOT / "artifacts" / "voice" / "reference_30s.wav"
DEFAULT_MODEL = "F5TTS_v1_Base"
DEFAULT_CONFIG = Path(files("f5_tts").joinpath(f"configs/{DEFAULT_MODEL}.yaml"))
DEFAULT_VOCAB = Path(files("f5_tts").joinpath("infer/examples/vocab.txt"))
DEFAULT_EXAMPLE_REFERENCE = Path(files("f5_tts").joinpath("infer/examples/basic/basic_ref_en.wav"))
DEFAULT_EXAMPLE_TEXT = "Some call me nature, others call me mother nature."
LOCAL_WHISPER_SNAPSHOT_ROOT = HF_CACHE_DIR / "hub" / "models--openai--whisper-large-v3-turbo" / "snapshots"

BACKBONES = {
    "DiT": DiT,
    "MMDiT": MMDiT,
    "UNetT": UNetT,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synthesize per-slide narration audio with F5-TTS from the section deck JSON and final narration markdown."
    )
    parser.add_argument("--deck-id", default=DEFAULT_DECK_ID)
    parser.add_argument("--deck-json", type=Path)
    parser.add_argument("--script-file", type=Path)
    parser.add_argument("--reference-mode", choices=("clone", "example"), default="clone")
    parser.add_argument("--reference-wav", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--reference-text", default="")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--model-name", default=DEFAULT_MODEL)
    parser.add_argument("--config-path", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--vocab-file", type=Path, default=DEFAULT_VOCAB)
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--max-slides", type=int)
    parser.add_argument("--nfe-step", type=int, default=32)
    parser.add_argument("--cfg-strength", type=float, default=2.0)
    parser.add_argument("--sway-sampling-coef", type=float, default=-1.0)
    parser.add_argument("--cross-fade-duration", type=float, default=0.15)
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--fix-duration", type=float)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def resolve_device(requested: str) -> str:
    if requested == "cpu":
        return "cpu"
    if requested == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA was requested but torch.cuda.is_available() is false.")
        return "cuda"
    return "cuda" if torch.cuda.is_available() else "cpu"


def load_deck(path: Path) -> dict:
    with require_path(path.resolve(), "slide deck JSON").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_model_config(path: Path) -> dict:
    with require_path(path.resolve(), "F5 model config YAML").open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def resolve_model_checkpoint(model_name: str, mel_spec_type: str) -> tuple[str, str]:
    if model_name == "F5TTS_v1_Base":
        return "SWivid/F5-TTS", "F5TTS_v1_Base/model_1250000.safetensors"
    if model_name == "F5TTS_Base":
        filename = "F5TTS_Base/model_1200000.pt"
        if mel_spec_type == "bigvgan":
            filename = "F5TTS_Base_bigvgan/model_1200000.pt"
        return "SWivid/F5-TTS", filename
    if model_name == "E2TTS_Base":
        return "SWivid/E2-TTS", "E2TTS_Base/model_1200000.pt"
    raise ValueError(f"Unsupported F5-TTS model_name: {model_name}")


def find_local_whisper_snapshot() -> Path | None:
    if not LOCAL_WHISPER_SNAPSHOT_ROOT.exists():
        return None
    snapshots = sorted(path for path in LOCAL_WHISPER_SNAPSHOT_ROOT.iterdir() if path.is_dir())
    return snapshots[-1] if snapshots else None


def transcribe_reference_locally(reference_wav: Path, device: str) -> str:
    model_path = find_local_whisper_snapshot()
    if model_path is None:
        raise RuntimeError(
            "No local whisper-large-v3-turbo snapshot was found. "
            "Provide --reference-text or cache the Whisper ASR model first."
        )

    asr = pipeline(
        "automatic-speech-recognition",
        model=str(model_path),
        tokenizer=str(model_path),
        feature_extractor=str(model_path),
        device=device,
    )
    with wave.open(str(reference_wav), "rb") as handle:
        frame_count = handle.getnframes()
        sample_rate = handle.getframerate()
        channel_count = handle.getnchannels()
        sample_width = handle.getsampwidth()
        raw = handle.readframes(frame_count)

    dtype_map = {1: np.int8, 2: np.int16, 4: np.int32}
    if sample_width not in dtype_map:
        raise RuntimeError(f"Unsupported WAV sample width: {sample_width}")
    audio = np.frombuffer(raw, dtype=dtype_map[sample_width]).astype(np.float32)
    if channel_count > 1:
        audio = audio.reshape(-1, channel_count).mean(axis=1)
    peak = float(np.iinfo(dtype_map[sample_width]).max)
    audio = audio / peak
    result = asr(
        {"raw": audio, "sampling_rate": sample_rate},
        generate_kwargs={"task": "transcribe", "language": "en"},
        return_timestamps=True,
    )
    text = result["text"].strip()
    if not text:
        raise RuntimeError(f"Local Whisper transcription returned empty text for {reference_wav}.")
    return text


def build_reference(args: argparse.Namespace) -> tuple[Path, str]:
    if args.reference_mode == "example":
        return require_path(DEFAULT_EXAMPLE_REFERENCE.resolve(), "F5 example reference WAV"), DEFAULT_EXAMPLE_TEXT
    reference_wav = require_path(args.reference_wav.resolve(), "voice reference WAV")
    if args.reference_text.strip():
        print(
            "Using caller-provided reference text. It must be the verbatim transcript of the reference WAV "
            "or clone-mode outputs may leak extra words from the prompt."
        )
        return reference_wav, args.reference_text
    print("No reference text provided; transcribing the reference WAV locally for F5 clone mode.")
    return reference_wav, transcribe_reference_locally(reference_wav, resolve_device(args.device))


def default_output_suffix(reference_mode: str) -> str:
    return f"f5_{reference_mode}"


def normalize_script(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def silence(sample_rate: int, seconds: float) -> np.ndarray:
    sample_count = max(int(round(sample_rate * seconds)), 0)
    return np.zeros(sample_count, dtype=np.float32)


def safe_audio_stem(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip())
    return cleaned.strip("_") or "beat"


def script_from_slide_beats(slide: dict) -> str | None:
    beats = slide.get("voiceover_beats") or []
    if not beats:
        return None
    return normalize_script(" ".join(str(beat["text"]) for beat in beats))


def synthesize_f5_text(
    script: str,
    processed_reference_wav: str,
    processed_reference_text: str,
    model_obj,
    vocoder,
    mel_spec_type: str,
    args: argparse.Namespace,
    device: str,
) -> tuple[np.ndarray, int]:
    audio, sample_rate, _ = infer_process(
        ref_audio=processed_reference_wav,
        ref_text=processed_reference_text,
        gen_text=script,
        model_obj=model_obj,
        vocoder=vocoder,
        mel_spec_type=mel_spec_type,
        show_info=print,
        progress=None,
        nfe_step=args.nfe_step,
        cfg_strength=args.cfg_strength,
        sway_sampling_coef=args.sway_sampling_coef,
        cross_fade_duration=args.cross_fade_duration,
        speed=args.speed,
        fix_duration=args.fix_duration,
        device=device,
    )
    if audio is None:
        raise RuntimeError("F5-TTS returned no audio.")
    return audio, sample_rate


def synthesize_slide_beats(
    slide: dict,
    output_dir: Path,
    processed_reference_wav: str,
    processed_reference_text: str,
    model_obj,
    vocoder,
    mel_spec_type: str,
    args: argparse.Namespace,
    device: str,
) -> tuple[np.ndarray, int, list[dict], str]:
    slide_number = int(slide["slide_number"])
    slide_id = slide["slide_id"]
    beats = slide.get("voiceover_beats") or []
    if not beats:
        raise ValueError(f"Slide {slide_number} ({slide_id}) has no voiceover beats.")

    beat_dir = ensure_directory(output_dir / "beats" / f"{slide_number:02d}_{slide_id}")
    rendered_parts: list[np.ndarray] = []
    manifest_beats: list[dict] = []
    sample_rate: int | None = None
    timeline = 0.0

    for beat_index, beat in enumerate(beats, start=1):
        audio, current_sample_rate = synthesize_f5_text(
            script=beat["text"],
            processed_reference_wav=processed_reference_wav,
            processed_reference_text=processed_reference_text,
            model_obj=model_obj,
            vocoder=vocoder,
            mel_spec_type=mel_spec_type,
            args=args,
            device=device,
        )
        if sample_rate is None:
            sample_rate = current_sample_rate
        elif sample_rate != current_sample_rate:
            raise RuntimeError(f"F5-TTS sample rate changed within slide {slide_number}.")

        beat_audio_seconds = len(audio) / sample_rate
        hold_after = float(beat.get("hold_after_seconds", 0.0))
        beat_wav = beat_dir / f"{beat_index:02d}_{safe_audio_stem(beat['id'])}.wav"
        sf.write(str(beat_wav), audio, sample_rate)

        rendered_parts.append(audio)
        if hold_after > 0:
            rendered_parts.append(silence(sample_rate, hold_after))

        manifest_beats.append(
            {
                "id": beat["id"],
                "text": beat["text"],
                "reveal": beat.get("reveal", []),
                "audio_file": str(beat_wav),
                "audio_seconds": round(beat_audio_seconds, 3),
                "hold_after_seconds": round(hold_after, 3),
                "start_seconds": round(timeline, 3),
                "end_seconds": round(timeline + beat_audio_seconds + hold_after, 3),
            }
        )
        timeline += beat_audio_seconds + hold_after

    if sample_rate is None:
        raise RuntimeError(f"Slide {slide_number} ({slide_id}) produced no beat audio.")
    combined = np.concatenate(rendered_parts) if rendered_parts else silence(sample_rate, 0)
    return combined, sample_rate, manifest_beats, script_from_slide_beats(slide) or ""


def main() -> int:
    args = parse_args()
    deck_json = (args.deck_json or deck_json_path(REPO_ROOT, args.deck_id)).resolve()
    deck = load_deck(deck_json)
    resolved_deck_id = deck["deck_id"]
    script_file = (args.script_file or final_script_path(REPO_ROOT, resolved_deck_id)).resolve()
    scripts = load_slide_scripts(script_file, deck)
    suffix = default_output_suffix(args.reference_mode)
    output_dir = ensure_directory((args.output_dir or audio_dir_path(REPO_ROOT, resolved_deck_id, suffix)).resolve())
    manifest_path = (args.manifest or audio_manifest_path(REPO_ROOT, resolved_deck_id, suffix)).resolve()
    ensure_directory(manifest_path.parent)

    slides = deck["slides"]
    if args.max_slides is not None:
        slides = slides[: args.max_slides]
        scripts = scripts[: args.max_slides]

    if args.dry_run:
        beat_count = sum(len(slide.get("voiceover_beats") or []) for slide in slides)
        print(f"Validated {len(slides)} slide narrations from {script_file} ({beat_count} beat narrations).")
        return 0

    model_config = load_model_config(args.config_path)
    vocab_file = require_path(args.vocab_file.resolve(), "F5 vocabulary file")
    reference_wav, reference_text = build_reference(args)
    device = resolve_device(args.device)

    model_settings = model_config["model"]
    backbone_name = model_settings["backbone"]
    if backbone_name not in BACKBONES:
        raise ValueError(f"Unsupported backbone '{backbone_name}'.")
    arch_config = model_settings["arch"]
    mel_spec_type = model_settings["mel_spec"]["mel_spec_type"]

    repo_id, filename = resolve_model_checkpoint(args.model_name, mel_spec_type)
    checkpoint_path = hf_hub_download(repo_id=repo_id, filename=filename, cache_dir=str(HF_CACHE_DIR))

    model_obj = load_model(
        model_cls=BACKBONES[backbone_name],
        model_cfg=arch_config,
        ckpt_path=checkpoint_path,
        mel_spec_type=mel_spec_type,
        vocab_file=str(vocab_file),
        device=device,
    )
    vocoder = load_vocoder(mel_spec_type, is_local=False, local_path="", device=device, hf_cache_dir=str(HF_CACHE_DIR))

    processed_reference_wav, processed_reference_text = preprocess_ref_audio_text(
        str(reference_wav),
        reference_text,
        show_info=print,
    )

    manifest = {
        "deck_id": deck["deck_id"],
        "script_file": str(script_file),
        "model_name": args.model_name,
        "reference_mode": args.reference_mode,
        "reference_wav": str(reference_wav),
        "reference_text": processed_reference_text,
        "device": device,
        "nfe_step": args.nfe_step,
        "cfg_strength": args.cfg_strength,
        "sway_sampling_coef": args.sway_sampling_coef,
        "cross_fade_duration": args.cross_fade_duration,
        "speed": args.speed,
        "slides": [],
    }

    for slide, script in zip(slides, scripts):
        slide_number = int(slide["slide_number"])
        slide_id = slide["slide_id"]
        output_wav = output_dir / f"{slide_number:02d}_{slide_id}.wav"

        beat_manifest: list[dict] = []
        narration_mode = "single"
        script_text = script
        if slide.get("voiceover_beats"):
            narration_mode = "beats"
            audio, sample_rate, beat_manifest, script_text = synthesize_slide_beats(
                slide=slide,
                output_dir=output_dir,
                processed_reference_wav=processed_reference_wav,
                processed_reference_text=processed_reference_text,
                model_obj=model_obj,
                vocoder=vocoder,
                mel_spec_type=mel_spec_type,
                args=args,
                device=device,
            )
        else:
            audio, sample_rate = synthesize_f5_text(
                script=script,
                processed_reference_wav=processed_reference_wav,
                processed_reference_text=processed_reference_text,
                model_obj=model_obj,
                vocoder=vocoder,
                mel_spec_type=mel_spec_type,
                args=args,
                device=device,
            )

        sf.write(str(output_wav), audio, sample_rate)
        slide_entry = {
            "slide_number": slide_number,
            "slide_id": slide_id,
            "audio_file": str(output_wav),
            "script": script_text,
            "narration_mode": narration_mode,
            "audio_seconds": round(len(audio) / sample_rate, 3),
        }
        if beat_manifest:
            slide_entry["beats"] = beat_manifest
        manifest["slides"].append(slide_entry)
        print(f"Synthesized slide {slide_number}: {output_wav.name}")
        if device == "cuda":
            torch.cuda.empty_cache()

    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote synthesis manifest to {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

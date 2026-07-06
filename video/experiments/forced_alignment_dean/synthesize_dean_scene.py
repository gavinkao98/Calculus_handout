"""Synthesize one full scene as a single Dean clip for alignment experiments."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

VIDEO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(VIDEO_ROOT))

from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()

from pipeline.audio import silence_pcm, wav_duration, write_pcm_wav  # noqa: E402
from pipeline.narration import estimate_seconds  # noqa: E402
from pipeline.tts import MIMO_BASE_URL, MimoTTSBackend, TTSRequest, load_dotenv  # noqa: E402

DEAN_STYLE = (
    "Use a consistent built-in Dean voice. Neutral General American accent, "
    "clear university lecture delivery, steady medium pace, no regional accent "
    "shift, no character acting, and careful pronunciation of mathematical terms."
)


def load_plan(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--backend", choices=("mock", "mimo"), default="mock")
    parser.add_argument("--model", default="mimo-v2.5-tts")
    parser.add_argument("--voice", default="Dean")
    parser.add_argument("--style", default=DEAN_STYLE)
    parser.add_argument("--base-url", default=MIMO_BASE_URL)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    plan = load_plan(args.plan)
    transcript = plan["transcript"]
    out_dir = args.plan.resolve().parent
    output = (args.output or (out_dir / "scene_dean.wav")).resolve()
    meta_path = out_dir / "scene_dean.meta.json"
    estimated = estimate_seconds(transcript)
    print(
        f"[dean-tts] scene={plan['scene_id']} words={plan['word_count']} "
        f"model={args.model} voice={args.voice} backend={args.backend} "
        f"estimated={estimated:.1f}s",
        flush=True,
    )
    if args.dry_run:
        return 0

    if args.backend == "mock":
        write_pcm_wav(output, silence_pcm(estimated))
    else:
        load_dotenv()
        import os

        api_key = os.environ.get("MIMO_API_KEY")
        if not api_key:
            raise SystemExit("[dean-tts] --backend mimo needs MIMO_API_KEY in env or .env")
        backend = MimoTTSBackend(base_url=args.base_url, api_key=api_key)
        result = backend.synthesize(
            TTSRequest(text=transcript, model=args.model, voice=args.voice, style=args.style)
        )
        write_pcm_wav(
            output,
            result.pcm,
            sample_rate=result.sample_rate,
            channels=result.channels,
            sample_width=result.sample_width,
        )

    duration = wav_duration(output)
    meta = {
        "plan": str(args.plan.resolve()),
        "audio_file": str(output),
        "backend": args.backend,
        "model": args.model,
        "voice": args.voice,
        "style": args.style,
        "duration": round(duration, 3),
        "word_count": plan["word_count"],
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[dean-tts] wrote {output}")
    print(f"[dean-tts] duration={duration:.3f}s")
    print(f"[dean-tts] wrote {meta_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Run local Whisper Timestamped word alignment for one Dean experiment scene."""
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


def load_plan(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [jsonable(v) for v in value]
    if hasattr(value, "item"):
        return value.item()
    return value


def flatten_words(result: dict[str, Any]) -> list[dict[str, Any]]:
    words: list[dict[str, Any]] = []
    for segment in result.get("segments", []):
        for word in segment.get("words", []):
            if "start" in word and "end" in word:
                words.append(word)
    return words


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--audio", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--model", default="base.en")
    parser.add_argument("--model-dir", type=Path)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--language", default="en")
    parser.add_argument("--no-initial-prompt", action="store_true")
    parser.add_argument("--accurate", action="store_true",
                        help="use beam/best-of decoding; slower but steadier")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    try:
        import whisper_timestamped as whisper
    except ImportError as exc:
        raise SystemExit(
            "whisper-timestamped is not installed; run "
            "`python -m pip install --upgrade whisper-timestamped`."
        ) from exc

    plan = load_plan(args.plan)
    audio = (args.audio or (args.plan.resolve().parent / "scene_dean.wav")).resolve()
    output = (args.output or (args.plan.resolve().parent / "words_whisper_timestamped.json")).resolve()
    transcript = plan.get("transcript") or ""
    initial_prompt = None if args.no_initial_prompt else transcript
    print(
        f"[whisper-ts] scene={plan['scene_id']} audio={audio} "
        f"model={args.model} device={args.device}",
        flush=True,
    )

    model = whisper.load_model(
        args.model,
        device=args.device,
        download_root=str(args.model_dir.resolve()) if args.model_dir else None,
    )
    kwargs: dict[str, Any] = {
        "language": args.language,
        "initial_prompt": initial_prompt,
        "verbose": args.verbose,
        "fp16": False if args.device == "cpu" else None,
    }
    if args.accurate:
        kwargs.update({"beam_size": 5, "best_of": 5})
    result = whisper.transcribe(model, str(audio), **kwargs)
    result = jsonable(result)
    words = flatten_words(result)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[whisper-ts] wrote {output}")
    print(
        f"[whisper-ts] asr_words={len(words)} plan_words={plan.get('word_count')} "
        f"segments={len(result.get('segments', []))}",
        flush=True,
    )
    if result.get("text"):
        print(f"[whisper-ts] text={str(result['text'])[:220]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

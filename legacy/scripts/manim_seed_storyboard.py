from __future__ import annotations

import argparse
from pathlib import Path

from shared_media_paths import DEFAULT_DECK_ID, deck_json_path, manim_storyboard_path
from manim_storyboard_workflow import (
    build_seed_storyboard,
    load_deck_json,
    load_seed_voiceovers,
    load_storyboard,
    write_storyboard,
)
from shared_runtime_bootstrap import REPO_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed a Manim storyboard YAML file from an existing slide deck JSON."
    )
    parser.add_argument("--deck-id", default=DEFAULT_DECK_ID)
    parser.add_argument("--deck-json", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    deck_json = (args.deck_json or deck_json_path(REPO_ROOT, args.deck_id)).resolve()
    deck = load_deck_json(deck_json)
    voiceovers, source = load_seed_voiceovers(deck)
    storyboard = build_seed_storyboard(deck, voiceovers)
    output = (args.output or manim_storyboard_path(REPO_ROOT, deck["deck_id"])).resolve()

    if output.exists() and not args.force:
        raise FileExistsError(
            f"Refusing to overwrite existing storyboard: {output}. Re-run with --force to replace it."
        )

    write_storyboard(output, storyboard)
    validated = load_storyboard(output)
    print(
        f"Seeded Manim storyboard for '{validated['deck_id']}' with {len(validated['scenes'])} scenes: {output}"
    )
    print(f"Voiceover source: {source}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        raise SystemExit(str(exc))

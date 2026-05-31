from __future__ import annotations

import argparse
from pathlib import Path

from manim_runtime import render_storyboard_scene
from manim_storyboard_workflow import (
    find_scene,
    load_render_manifest,
    load_storyboard,
    resolve_storyboard_path,
    scene_visual_fingerprint,
    write_render_manifest,
)
from shared_media_paths import DEFAULT_DECK_ID, manim_scene_output_path
from shared_runtime_bootstrap import REPO_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render or reuse a single storyboard scene preview."
    )
    parser.add_argument("--deck-id", default=DEFAULT_DECK_ID)
    parser.add_argument("--storyboard", type=Path)
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--quality", choices=("preview", "final"), default="preview")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    storyboard_path = resolve_storyboard_path(args.deck_id, args.storyboard)
    storyboard = load_storyboard(storyboard_path)
    scene = find_scene(storyboard, args.scene_id)
    output = (
        args.output
        or manim_scene_output_path(REPO_ROOT, storyboard["deck_id"], scene["scene_number"], scene["scene_id"])
    ).resolve()
    fingerprint = scene_visual_fingerprint(storyboard, scene, args.quality)
    manifest = load_render_manifest(storyboard["deck_id"])
    cached = manifest["scenes"].get(scene["scene_id"], {})
    cached_fingerprint = cached.get("visual_fingerprint") or cached.get("fingerprint")

    if args.dry_run:
        print(
            f"Validated scene '{scene['scene_id']}' ({scene['template']}) at quality '{args.quality}'. "
            f"Output path: {output}"
        )
        return 0

    if (
        not args.force
        and output.exists()
        and cached_fingerprint == fingerprint
        and cached.get("quality") == args.quality
    ):
        print(f"Reused cached scene preview: {output}")
        return 0

    rendered = render_storyboard_scene(storyboard_path, storyboard, scene, output, args.quality)
    manifest.setdefault("scenes", {})[scene["scene_id"]] = {
        "fingerprint": fingerprint,
        "visual_fingerprint": fingerprint,
        "quality": args.quality,
        "output_file": str(rendered),
    }
    write_render_manifest(storyboard["deck_id"], manifest)
    print(f"Rendered scene preview to {rendered}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, KeyError, RuntimeError, ValueError) as exc:
        raise SystemExit(str(exc))

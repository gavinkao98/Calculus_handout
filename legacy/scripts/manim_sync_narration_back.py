#!/usr/bin/env python3
"""Sync edited narration from narration.md back into the storyboard YAML.

Usage
-----
    python tools/manim_sync_narration_back.py --deck-id ch01_inverse_functions

Workflow
--------
1. Run ``manim_render_lesson.py --with-audio`` (or the export step) to produce
   ``artifacts/manim/<deck_id>/narration.md``.
2. Edit the narration text under each scene's ``Narration:`` heading.
3. Run this script to push changed narration back into the storyboard YAML.

The script is intentionally conservative:

- It only updates ``voiceover`` fields.
- It refuses to run if a scene ID in the markdown is not found in the YAML.
- It detects stale narration exports by comparing hidden voiceover hashes.
- It creates a ``.bak`` copy of the YAML before writing.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

# ---- bootstrap so sibling modules are importable ----
_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

from manim_storyboard_workflow import normalize_narration_text, voiceover_content_hash
from shared_media_paths import manim_narration_path, manim_storyboard_path
from shared_runtime_bootstrap import REPO_ROOT

try:
    from manim_templates.narration_markers import (
        MarkerCountMismatch,
        has_descriptor_comment,
        has_markers,
        parse_marked_narration,
    )
    _MARKERS_AVAILABLE = True
except ImportError:
    _MARKERS_AVAILABLE = False


_SLIDE_HEADER_RE = re.compile(r"^## Slide \d+:\s+.+$")
_SLIDE_ID_RE = re.compile(r"^Slide ID:\s*`([^`]+)`")
_VOICEOVER_HASH_RE = re.compile(r"^<!--\s*voiceover-hash:\s*([0-9a-f]{64})\s*-->$")


ParsedNarration = dict[str, dict[str, str | None]]


def parse_narration_md(text: str) -> ParsedNarration:
    """Return ``{scene_id: {narration, source_hash}}`` from narration markdown."""
    lines = text.splitlines()
    scenes: ParsedNarration = {}
    current_id: str | None = None
    current_hash: str | None = None
    collecting = False
    narration_lines: list[str] = []

    def flush_current_scene() -> None:
        nonlocal current_id, current_hash, narration_lines
        if current_id is None:
            return
        scenes[current_id] = {
            "narration": normalize_narration_text("\n".join(narration_lines)),
            "source_hash": current_hash,
        }

    for line in lines:
        if _SLIDE_HEADER_RE.match(line):
            flush_current_scene()
            current_id = None
            current_hash = None
            collecting = False
            narration_lines = []
            continue

        id_match = _SLIDE_ID_RE.match(line)
        if id_match:
            current_id = id_match.group(1)
            continue

        hash_match = _VOICEOVER_HASH_RE.match(line.strip())
        if hash_match and current_id is not None and not collecting:
            current_hash = hash_match.group(1)
            continue

        if line.strip() == "Narration:":
            collecting = True
            continue

        if line.strip() == "Voiceover Beats:" and collecting:
            collecting = False
            continue

        if collecting:
            narration_lines.append(line)

    flush_current_scene()
    return scenes


def render_voiceover_scalar(text: str, indent: str) -> list[str]:
    normalized = normalize_narration_text(text)
    if "\n" not in normalized:
        return [f"{indent}voiceover: {json.dumps(normalized, ensure_ascii=False)}\n"]

    rendered = [f"{indent}voiceover: |-\n"]
    for line in normalized.split("\n"):
        rendered.append(f"{indent}  {line}\n")
    return rendered


def skip_existing_scalar(lines: list[str], start_index: int, key_indent: int) -> int:
    stripped = lines[start_index].lstrip()
    remainder = stripped.split(":", 1)[1].lstrip()
    next_index = start_index + 1
    if not remainder.startswith(("|", ">")):
        return next_index

    block_indent = key_indent + 2
    while next_index < len(lines):
        candidate = lines[next_index]
        if not candidate.strip():
            next_index += 1
            continue
        candidate_indent = len(candidate) - len(candidate.lstrip(" "))
        if candidate_indent < block_indent:
            break
        next_index += 1
    return next_index


def update_voiceovers_in_yaml(yaml_text: str, updates: dict[str, str]) -> str:
    """Return *yaml_text* with voiceover values replaced for the given scene IDs."""
    lines = yaml_text.splitlines(keepends=True)
    result: list[str] = []
    current_scene_id: str | None = None
    remaining = dict(updates)

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()

        if stripped.startswith("scene_id:"):
            value = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            current_scene_id = value
            result.append(line)
            i += 1
            continue

        if stripped.startswith("voiceover:") and current_scene_id in remaining:
            indent = line[: len(line) - len(stripped)]
            new_voiceover = remaining.pop(current_scene_id)
            result.extend(render_voiceover_scalar(new_voiceover, indent))
            i = skip_existing_scalar(lines, i, len(indent))
            continue

        result.append(line)
        i += 1

    return "".join(result)


def extract_current_voiceovers(yaml_text: str) -> dict[str, str]:
    from shared_simple_yaml import load_yaml

    current_storyboard = load_yaml(yaml_text)
    current_voiceovers: dict[str, str] = {}
    for scene in current_storyboard.get("scenes", []):
        scene_id = str(scene.get("scene_id", ""))
        voiceover = normalize_narration_text(scene.get("voiceover", ""))
        current_voiceovers[scene_id] = voiceover
    return current_voiceovers


def extract_beat_scene_ids(yaml_text: str) -> set[str]:
    from shared_simple_yaml import load_yaml

    current_storyboard = load_yaml(yaml_text)
    beat_scene_ids: set[str] = set()
    for scene in current_storyboard.get("scenes", []):
        if scene.get("voiceover_beats"):
            beat_scene_ids.add(str(scene.get("scene_id", "")))
    return beat_scene_ids


def print_change_summary(scene_id: str, old_text: str, new_text: str) -> None:
    old_preview = old_text[:60].replace("\n", " ")
    new_preview = new_text[:60].replace("\n", " ")
    print(f"  [{scene_id}]")
    print(f"    old: {old_preview}...")
    print(f"    new: {new_preview}...")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync edited narration from narration.md back into the storyboard YAML."
    )
    parser.add_argument(
        "--deck-id",
        required=True,
        help="Deck identifier, e.g. ch01_inverse_functions.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing the YAML.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite YAML voiceover changes even if the narration export is stale.",
    )
    parser.add_argument(
        "--script-file",
        type=Path,
        default=None,
        help="Override the path to the edited narration.md file.",
    )
    parser.add_argument(
        "--storyboard-file",
        type=Path,
        default=None,
        help="Override the path to the storyboard YAML.",
    )
    args = parser.parse_args()

    script_path = (args.script_file or manim_narration_path(REPO_ROOT, args.deck_id)).resolve()
    storyboard_path = (args.storyboard_file or manim_storyboard_path(REPO_ROOT, args.deck_id)).resolve()

    if not script_path.exists():
        print(f"ERROR: narration file not found: {script_path}", file=sys.stderr)
        print("Run manim_render_lesson.py first to export the narration file.", file=sys.stderr)
        sys.exit(1)
    if not storyboard_path.exists():
        print(f"ERROR: storyboard not found: {storyboard_path}", file=sys.stderr)
        sys.exit(1)

    md_text = script_path.read_text(encoding="utf-8")
    md_narrations = parse_narration_md(md_text)
    if not md_narrations:
        print("No narration sections found in the markdown file.")
        sys.exit(0)

    yaml_text = storyboard_path.read_text(encoding="utf-8")
    current_voiceovers = extract_current_voiceovers(yaml_text)
    beat_scene_ids = extract_beat_scene_ids(yaml_text)

    unknown_ids = set(md_narrations) - set(current_voiceovers)
    if unknown_ids:
        print(
            "ERROR: the following scene IDs in the markdown are not in the storyboard: "
            + ", ".join(sorted(unknown_ids)),
            file=sys.stderr,
        )
        sys.exit(1)

    legacy_ids = [scene_id for scene_id, entry in md_narrations.items() if entry.get("source_hash") is None]
    if legacy_ids:
        print(
            "Warning: some narration sections do not contain hidden voiceover hashes. "
            "Stale-file conflict detection is disabled for: "
            + ", ".join(sorted(legacy_ids))
        )

    changes: dict[str, str] = {}
    conflicts: list[dict[str, Any]] = []
    marker_errors: list[tuple[str, str]] = []
    for scene_id, entry in md_narrations.items():
        if scene_id in beat_scene_ids:
            continue
        raw_md = entry["narration"] or ""
        # Reverse 〔顯示...〕 markers back into <bookmark .../> form before
        # comparing or writing. If the markers and the hidden descriptor
        # comment disagree we abort: the proofreader needs to fix one of
        # the two before sync can proceed safely.
        if _MARKERS_AVAILABLE and (has_markers(raw_md) or has_descriptor_comment(raw_md)):
            try:
                restored = parse_marked_narration(raw_md)
            except MarkerCountMismatch as exc:
                marker_errors.append((scene_id, str(exc)))
                continue
            new_text = normalize_narration_text(restored)
        else:
            new_text = normalize_narration_text(raw_md)
        current_text = current_voiceovers.get(scene_id, "")
        if not new_text:
            print(f"ERROR: narration for scene '{scene_id}' is empty after editing.", file=sys.stderr)
            sys.exit(1)
        if new_text == current_text:
            continue

        source_hash = entry.get("source_hash")
        current_hash = voiceover_content_hash(current_text)
        if source_hash is not None and source_hash != current_hash:
            conflicts.append(
                {
                    "scene_id": scene_id,
                    "expected_hash": source_hash,
                    "current_hash": current_hash,
                    "current_preview": current_text[:60].replace("\n", " "),
                    "edited_preview": new_text[:60].replace("\n", " "),
                }
            )
            continue

        changes[scene_id] = new_text

    if marker_errors:
        print("ERROR: narration sync aborted because some scenes have inconsistent reveal markers.", file=sys.stderr)
        print("Reconcile the 〔顯示...〕 markers and the hidden bookmark-marks comment before re-running.\n", file=sys.stderr)
        for scene_id, msg in marker_errors:
            print(f"  [{scene_id}] {msg}", file=sys.stderr)
        sys.exit(1)

    if conflicts and not args.force:
        print("ERROR: narration sync aborted because the storyboard changed after narration.md was exported.", file=sys.stderr)
        print("Re-export narration.md or rerun with --force if you want to overwrite the YAML anyway.\n", file=sys.stderr)
        for conflict in conflicts:
            print(f"  [{conflict['scene_id']}]", file=sys.stderr)
            print(f"    YAML now: {conflict['current_preview']}...", file=sys.stderr)
            print(f"    markdown: {conflict['edited_preview']}...", file=sys.stderr)
            print(file=sys.stderr)
        sys.exit(1)

    if conflicts and args.force:
        print("Force mode enabled: overwriting YAML voiceovers despite stale narration hashes.\n")
        for conflict in conflicts:
            changes[conflict["scene_id"]] = normalize_narration_text(
                md_narrations[conflict["scene_id"]]["narration"] or ""
            )

    if not changes:
        if beat_scene_ids:
            print(
                "No narration changes detected. Scenes with voiceover_beats must be edited in the storyboard YAML."
            )
        else:
            print("No narration changes detected. Storyboard is already up to date.")
        sys.exit(0)

    print(f"Detected {len(changes)} narration change(s):\n")
    for scene_id, new_text in changes.items():
        print_change_summary(scene_id, current_voiceovers.get(scene_id, ""), new_text)

    if args.dry_run:
        print("Dry run — no files modified.")
        sys.exit(0)

    backup_path = storyboard_path.with_suffix(".yml.bak")
    shutil.copy2(storyboard_path, backup_path)
    print(f"Backup saved: {backup_path.name}")

    updated_yaml = update_voiceovers_in_yaml(yaml_text, changes)
    storyboard_path.write_text(updated_yaml, encoding="utf-8")
    print(f"Storyboard updated: {storyboard_path.name}")
    print(f"\nDone. {len(changes)} scene(s) synced.")


if __name__ == "__main__":
    main()

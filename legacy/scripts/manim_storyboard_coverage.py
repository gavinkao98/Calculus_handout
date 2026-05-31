"""Print a side-by-side inventory of chapter environments versus storyboard scenes.

Purpose: catch the "did we forget to storyboard this definition?" failure mode without
making any automatic mapping claims. Each storyboard's leading-comment source range
(e.g. "chapters/ch01_foundations.tex, Section 1.1 (lines 7-315)") is parsed and the
matching chapter segment is scanned for must-include environments (definition, theorem,
proposition, workedexample, figure, strategy). The tool prints both lists side by side
and reports their counts; the human reader does the per-environment coverage check.

Automatic fuzzy matching by scene_id substrings was considered and rejected -- it
produces false-positive matches that hide real gaps. The inventory format makes the
gaps visible without pretending to resolve them.

Usage:
    python tools/manim_storyboard_coverage.py --all
    python tools/manim_storyboard_coverage.py --storyboard inputs/manim_storyboards/foo.yml
    python tools/manim_storyboard_coverage.py --deck-id ch01_precise_limit
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

from manim_storyboard_workflow import load_storyboard, resolve_storyboard_path
from shared_media_paths import DEFAULT_DECK_ID
from shared_runtime_bootstrap import REPO_ROOT

INCLUDE_ENVIRONMENTS = (
    "definition",
    "theorem",
    "proposition",
    "lemma",
    "corollary",
    "workedexample",
    "figure",
    "strategy",
)

ENV_BEGIN_RE = re.compile(
    r"^\\begin\{(" + "|".join(INCLUDE_ENVIRONMENTS) + r")\}(\[(?P<title>[^\]]*)\])?",
)
SOURCE_RANGE_RE = re.compile(
    r"chapters/(?P<chapter>[a-z0-9_]+\.tex).*?lines?\s+(?P<start>\d+)\s*[-–]\s*(?P<end>\d+)",
    re.IGNORECASE,
)


def find_source_range(storyboard_path: Path) -> tuple[Path, int, int] | None:
    """Parse the storyboard's leading YAML comments for a 'chapters/X.tex lines A-B' hint."""
    comment_lines: list[str] = []
    with storyboard_path.open(encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if stripped.startswith("#"):
                comment_lines.append(stripped.lstrip("#").strip())
                continue
            if not stripped:
                if comment_lines:
                    continue
                continue
            break
    blob = " ".join(comment_lines)
    match = SOURCE_RANGE_RE.search(blob)
    if not match:
        return None
    chapter_path = REPO_ROOT / "chapters" / match.group("chapter")
    if not chapter_path.exists():
        return None
    return chapter_path, int(match.group("start")), int(match.group("end"))


def list_chapter_environments(
    chapter_path: Path, line_start: int, line_end: int
) -> list[tuple[int, str, str]]:
    """Return (line, env_type, optional_title) for each must-include environment in range."""
    results: list[tuple[int, str, str]] = []
    with chapter_path.open(encoding="utf-8") as fh:
        for index, line in enumerate(fh, start=1):
            if index < line_start or index > line_end:
                continue
            match = ENV_BEGIN_RE.match(line)
            if not match:
                continue
            env_type = match.group(1)
            title = match.group("title") or ""
            results.append((index, env_type, title))
    return results


def list_storyboard_scenes(
    storyboard: dict,
) -> list[tuple[int, str, str, str]]:
    """Return (scene_number, scene_id, template, content_type) for each scene."""
    out: list[tuple[int, str, str, str]] = []
    for scene in storyboard.get("scenes", []):
        out.append((
            scene.get("scene_number", 0),
            scene.get("scene_id", ""),
            scene.get("template", ""),
            scene.get("content_type", ""),
        ))
    return out


def collect_storyboard_paths(args: argparse.Namespace) -> list[Path]:
    if args.all:
        return sorted((REPO_ROOT / "inputs" / "manim_storyboards").glob("*.yml"))
    if args.storyboard:
        return [args.storyboard.resolve()]
    return [resolve_storyboard_path(args.deck_id, None)]


def print_report(storyboard_path: Path) -> None:
    rel = (
        storyboard_path.relative_to(REPO_ROOT)
        if storyboard_path.is_relative_to(REPO_ROOT)
        else storyboard_path
    )
    print(f"=== {rel} ===")

    storyboard = load_storyboard(storyboard_path)
    deck_id = storyboard.get("deck_id", "<no deck_id>")
    scenes = list_storyboard_scenes(storyboard)
    source = find_source_range(storyboard_path)

    if source is None:
        print(
            "  (no chapter source range found in leading comments; expected a comment of the form\n"
            "   '# Source: chapters/<file>.tex, Section X.Y (lines A-B).' near the top of the YAML)"
        )
        envs: list[tuple[int, str, str]] = []
    else:
        chapter_path, line_start, line_end = source
        chapter_rel = chapter_path.relative_to(REPO_ROOT)
        print(f"  deck_id            : {deck_id}")
        print(f"  source range       : {chapter_rel} L{line_start}-L{line_end}")
        envs = list_chapter_environments(chapter_path, line_start, line_end)

    print()
    print(f"  {len(envs)} chapter environment(s) in range:")
    if envs:
        for line_num, env_type, title in envs:
            label = f"[{title}]" if title else ""
            print(f"    L{line_num:<5d}  {env_type:<14s}  {label}")
    else:
        print("    (none -- check that the source-range comment is correctly formatted)")

    print()
    print(f"  {len(scenes)} storyboard scene(s):")
    for scene_number, scene_id, template, content_type in scenes:
        ct = f"[{content_type}]" if content_type else ""
        print(f"    {scene_number:02d}  {scene_id:<35s}  {template:<22s}  {ct}")

    print()
    if envs:
        print(
            f"  count comparison   : {len(envs)} env(s) in chapter range vs "
            f"{len(scenes)} scene(s) in storyboard"
        )
        print(
            "  (manual coverage check still required: confirm every must-include\n"
            "   environment is either rendered as a scene or has a documented skip\n"
            "   comment near the affected scene; see MANIM_STORYBOARD.md.)"
        )
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Inventory comparison: chapter environments in a storyboard's source range "
            "versus the storyboard's scenes."
        )
    )
    parser.add_argument("--deck-id", default=DEFAULT_DECK_ID)
    parser.add_argument("--storyboard", type=Path)
    parser.add_argument(
        "--all",
        action="store_true",
        help="report on every storyboard under inputs/manim_storyboards/",
    )
    args = parser.parse_args()

    paths = collect_storyboard_paths(args)
    if not paths:
        print("No storyboard files found.")
        return 0

    for path in paths:
        print_report(path)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, KeyError, RuntimeError, ValueError) as exc:
        raise SystemExit(str(exc))

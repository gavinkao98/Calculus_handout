from __future__ import annotations

import re
from pathlib import Path
from typing import Any


SLIDE_HEADING_RE = re.compile(r"^## Slide (?P<slide_number>\d+): .+$", re.MULTILINE)
SLIDE_ID_RE = re.compile(r"^Slide ID: `(?P<slide_id>[^`]+)`$", re.MULTILINE)
NARRATION_MARKER_RE = re.compile(r"^Narration:\s*$", re.MULTILINE)
VOICEOVER_BEATS_MARKER_RE = re.compile(r"^Voiceover Beats:\s*$", re.MULTILINE)
RAW_LATEX_RE = re.compile(r"(\\\(|\\\)|\\[A-Za-z]+)")


def draft_script_path(repo_root: Path, deck_id: str) -> Path:
    return repo_root / "artifacts" / "scripts" / f"{deck_id}_draft.md"


def final_script_path(repo_root: Path, deck_id: str) -> Path:
    return repo_root / "artifacts" / "scripts" / f"{deck_id}_final.md"


def assert_no_raw_latex_narration(text: str, label: str) -> None:
    match = RAW_LATEX_RE.search(text)
    if not match:
        return

    start = max(0, match.start() - 40)
    end = min(len(text), match.end() + 40)
    snippet = text[start:end].replace("\n", " ")
    raise ValueError(
        f"{label} contains raw LaTeX markup near '{snippet}'. "
        "Narration must use spoken math, not TeX source."
    )


def render_script_markdown(deck: dict[str, Any], variant: str) -> str:
    if variant not in {"draft", "final"}:
        raise ValueError(f"Unsupported script variant: {variant}")

    title = "Draft Narration" if variant == "draft" else "Final Narration"
    guidance = (
        "This file is regenerated from the lecture notes. Revise the final file instead of editing this draft."
        if variant == "draft"
        else "This file is seeded from the draft once. After that, it is user-owned and the generator preserves it."
    )
    sections = [
        f"# {deck['source_section']} {title}",
        "",
        f"Source file: `{deck['source_file']}`",
        f"Deck ID: `{deck['deck_id']}`",
        "",
        guidance,
        "The narration may be more conversational than the textbook, but definitions, assumptions, and conclusions should remain mathematically correct.",
        "",
    ]

    for slide in deck["slides"]:
        narration = slide["script_draft"].strip()
        assert_no_raw_latex_narration(
            narration,
            f"deck slide {slide['slide_number']} ({slide['slide_id']}) draft narration",
        )
        sections.extend(
            [
                f"## Slide {slide['slide_number']}: {slide['title']}",
                "",
                f"Slide ID: `{slide['slide_id']}`",
                f"Learning goal: {slide['learning_goal']}",
                f"Slide type: `{slide['slide_type']}`",
                "",
                "Narration:",
                "",
                narration,
                "",
            ]
        )

    return "\n".join(sections).strip() + "\n"


def load_slide_scripts(path: Path, deck: dict[str, Any], enforce_spoken_math: bool = True) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"Missing narration markdown file: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Expected a narration markdown file: {path}")

    text = path.read_text(encoding="utf-8")
    matches = list(SLIDE_HEADING_RE.finditer(text))
    if not matches:
        raise ValueError(f"No slide sections were found in narration file: {path}")

    sections: dict[tuple[int, str], str] = {}
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section_text = text[start:end].strip()
        slide_number = int(match.group("slide_number"))

        slide_id_match = SLIDE_ID_RE.search(section_text)
        if not slide_id_match:
            raise ValueError(
                f"Slide {slide_number} in {path} is missing a 'Slide ID' line."
            )
        slide_id = slide_id_match.group("slide_id").strip()

        narration_marker = NARRATION_MARKER_RE.search(section_text)
        if not narration_marker:
            raise ValueError(
                f"Slide {slide_number} in {path} is missing a 'Narration:' marker."
            )
        narration_end = len(section_text)
        beats_marker = VOICEOVER_BEATS_MARKER_RE.search(section_text, narration_marker.end())
        if beats_marker:
            narration_end = beats_marker.start()
        narration = section_text[narration_marker.end() : narration_end].strip()
        sections[(slide_number, slide_id)] = narration

    expected_keys = [
        (int(slide["slide_number"]), slide["slide_id"]) for slide in deck["slides"]
    ]
    expected_key_set = set(expected_keys)
    section_keys = set(sections.keys())
    missing = [key for key in expected_keys if key not in section_keys]
    extra = [key for key in sections if key not in expected_key_set]
    if missing or extra:
        raise ValueError(
            "Narration markdown does not match the current deck. "
            f"Missing slides: {missing or 'none'}. Extra slides: {extra or 'none'}."
        )

    scripts: list[str] = []
    for slide_number, slide_id in expected_keys:
        narration = sections[(slide_number, slide_id)].strip()
        if not narration:
            raise ValueError(
                f"Slide {slide_number} ({slide_id}) has empty narration in {path}."
            )
        if enforce_spoken_math:
            assert_no_raw_latex_narration(
                narration,
                f"slide {slide_number} ({slide_id}) narration in {path}",
            )
        scripts.append(narration)
    return scripts

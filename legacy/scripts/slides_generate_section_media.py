from __future__ import annotations

import argparse
import json
import locale
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from shared_runtime_bootstrap import REPO_ROOT, ensure_directory, require_path
from slides_script_workflow import (
    assert_no_raw_latex_narration,
    draft_script_path,
    final_script_path,
    load_slide_scripts,
    render_script_markdown,
)


SCHEMA_FILE = REPO_ROOT / "schemas" / "slide_deck.schema.json"
PLAN_DIR = REPO_ROOT / "inputs" / "media_plans"
DEFAULT_PLAN = PLAN_DIR / "ch01_inverse_functions.json"
DEFAULT_RENDER_HINTS = {
    "tikz_scale_mode": "none",
    "max_width": r"\textwidth",
    "max_height_ratio": 0.58,
    "allow_frame_breaks": False,
}
ALLOWED_SLIDE_TYPES = {
    "motivation",
    "overview",
    "definition",
    "example",
    "figure",
    "theorem",
    "warning",
    "procedure",
    "recap",
}
ALLOWED_TIKZ_SCALE_MODES = {"none", "fit_width"}
ENV_BLOCK_RE = re.compile(
    r"\\begin\{(?P<kind>[A-Za-z*]+)\}(?:\[(?P<title>[^\]]+)\])?\s*(?P<body>.*?)\\end\{(?P=kind)\}",
    re.DOTALL,
)
DISPLAY_MATH_RE = re.compile(r"\\\[(.*?)\\\]", re.DOTALL)
CAPTION_RE = re.compile(r"\\caption(?:\[[^\]]*\])?\{.*?\}", re.DOTALL)
LABEL_RE = re.compile(r"\\label\{.*?\}", re.DOTALL)


@dataclass(frozen=True)
class SourceBlock:
    kind: str
    index: int
    title: str | None
    body: str

    @property
    def display_math(self) -> list[str]:
        return [match.group(0).strip() for match in DISPLAY_MATH_RE.finditer(self.body)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate slide deck JSON, Beamer source, and narration markdown from a section media plan."
        )
    )
    parser.add_argument(
        "--plan",
        type=Path,
        help="Path to a section media plan JSON file. Defaults to inputs/media_plans/ch01_inverse_functions.json.",
    )
    parser.add_argument(
        "--deck-id",
        help="Deck id to resolve under inputs/media_plans/<deck-id>.json when --plan is omitted.",
    )
    parser.add_argument(
        "--compile",
        choices=("auto", "never", "require"),
        default="auto",
        help="Compile the generated Beamer .tex into PDF if LaTeX tools are available.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plan_path = resolve_plan_path(args.plan, args.deck_id)
    plan = load_json(require_path(plan_path, "section media plan"))
    validate_plan(plan, plan_path)

    source_file = require_path((REPO_ROOT / plan["source_file"]).resolve(), "source LaTeX file")
    section_text = extract_section_text(source_file, plan["source_section"])
    blocks = parse_source_blocks(section_text)
    deck = build_deck(plan, blocks)
    validate_deck(deck)

    output_paths = write_outputs(deck)
    warnings = collect_density_warnings(deck)

    print(
        "Generated deck JSON, Beamer source, and draft narration markdown from "
        f"{plan_path.relative_to(REPO_ROOT)}."
    )
    print(f"Deck JSON: {output_paths['deck_json']}")
    print(f"Beamer source: {output_paths['slide_tex']}")
    print(f"Draft narration: {output_paths['draft_script']}")

    preserve_or_seed_final_script(deck, output_paths["final_script"])

    if warnings:
        print("Slide density warnings:")
        for warning in warnings:
            print(f"- {warning}")

    if args.compile != "never":
        compile_beamer(output_paths["slide_tex"], args.compile)

    return 0


def resolve_plan_path(plan_path: Path | None, deck_id: str | None) -> Path:
    if plan_path is not None:
        return plan_path.resolve()
    if deck_id:
        return (PLAN_DIR / f"{deck_id}.json").resolve()
    return DEFAULT_PLAN.resolve()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string.")
    return value.strip()


def require_bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be a boolean.")
    return value


def require_int(value: Any, label: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{label} must be an integer.")
    return value


def require_float(value: Any, label: str) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a number.")
    return float(value)


def validate_plan(plan: dict[str, Any], plan_path: Path) -> None:
    if not isinstance(plan, dict):
        raise ValueError(f"Plan file must contain a JSON object: {plan_path}")

    for key in ("deck_id", "source_file", "source_section", "language", "slides"):
        if key not in plan:
            raise ValueError(f"Plan file is missing required key '{key}': {plan_path}")

    require_text(plan["deck_id"], "plan.deck_id")
    require_text(plan["source_file"], "plan.source_file")
    require_text(plan["source_section"], "plan.source_section")
    require_text(plan["language"], "plan.language")

    defaults = plan.get("defaults", {})
    if defaults:
        if not isinstance(defaults, dict):
            raise ValueError("plan.defaults must be an object when provided.")
        if "render_hints" in defaults:
            normalize_render_hints(defaults["render_hints"], DEFAULT_RENDER_HINTS, "plan.defaults.render_hints")

    slides = plan["slides"]
    if not isinstance(slides, list) or not slides:
        raise ValueError("plan.slides must be a non-empty array.")

    seen_slide_ids: set[str] = set()
    for index, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            raise ValueError(f"plan.slides[{index}] must be an object.")
        slide_id = require_text(slide.get("slide_id"), f"plan.slides[{index}].slide_id")
        if slide_id in seen_slide_ids:
            raise ValueError(f"Duplicate slide_id '{slide_id}' in plan.")
        seen_slide_ids.add(slide_id)
        require_text(slide.get("title"), f"plan.slides[{index}].title")
        require_text(slide.get("learning_goal"), f"plan.slides[{index}].learning_goal")
        slide_type = require_text(slide.get("slide_type"), f"plan.slides[{index}].slide_type")
        if slide_type not in ALLOWED_SLIDE_TYPES:
            raise ValueError(
                f"Unsupported slide_type '{slide_type}' in plan.slides[{index}]. Allowed values: {sorted(ALLOWED_SLIDE_TYPES)}"
            )
        require_text(slide.get("script_draft"), f"plan.slides[{index}].script_draft")

        bullets = slide.get("bullets", [])
        if not isinstance(bullets, list) or not all(isinstance(item, str) for item in bullets):
            raise ValueError(f"plan.slides[{index}].bullets must be an array of strings.")

        math_blocks = slide.get("math_blocks", [])
        if not isinstance(math_blocks, list):
            raise ValueError(f"plan.slides[{index}].math_blocks must be an array.")
        for math_index, entry in enumerate(math_blocks):
            validate_math_entry(entry, f"plan.slides[{index}].math_blocks[{math_index}]")

        validate_tikz_entry(slide.get("tikz_code"), f"plan.slides[{index}].tikz_code")

        render_hints = slide.get("render_hints")
        if render_hints is not None:
            normalize_render_hints(render_hints, DEFAULT_RENDER_HINTS, f"plan.slides[{index}].render_hints")

        source_refs = slide.get("source_refs", [])
        if not isinstance(source_refs, list):
            raise ValueError(f"plan.slides[{index}].source_refs must be an array when provided.")
        for ref_index, selector in enumerate(source_refs):
            validate_block_selector(selector, f"plan.slides[{index}].source_refs[{ref_index}]")


def validate_math_entry(entry: Any, label: str) -> None:
    if isinstance(entry, str):
        return
    if not isinstance(entry, dict):
        raise ValueError(f"{label} must be either a string or an object.")
    validate_block_selector(entry.get("block"), f"{label}.block")
    require_int(entry.get("math_index"), f"{label}.math_index")


def validate_tikz_entry(entry: Any, label: str) -> None:
    if entry is None or isinstance(entry, str):
        return
    if not isinstance(entry, dict):
        raise ValueError(f"{label} must be null, a string, or an object.")
    validate_block_selector(entry.get("block"), f"{label}.block")


def validate_block_selector(selector: Any, label: str) -> None:
    if not isinstance(selector, dict):
        raise ValueError(f"{label} must be an object.")
    require_text(selector.get("kind"), f"{label}.kind")
    require_int(selector.get("index"), f"{label}.index")
    title = selector.get("title")
    if title is not None:
        require_text(title, f"{label}.title")


def normalize_render_hints(value: Any, defaults: dict[str, Any], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object.")

    hints = {**defaults, **value}
    mode = require_text(hints.get("tikz_scale_mode"), f"{label}.tikz_scale_mode")
    if mode not in ALLOWED_TIKZ_SCALE_MODES:
        raise ValueError(
            f"{label}.tikz_scale_mode must be one of {sorted(ALLOWED_TIKZ_SCALE_MODES)}, got '{mode}'."
        )
    max_width = require_text(hints.get("max_width"), f"{label}.max_width")
    max_height_ratio = require_float(hints.get("max_height_ratio"), f"{label}.max_height_ratio")
    if not (0 < max_height_ratio <= 1):
        raise ValueError(f"{label}.max_height_ratio must be between 0 and 1.")
    allow_frame_breaks = require_bool(hints.get("allow_frame_breaks"), f"{label}.allow_frame_breaks")

    return {
        "tikz_scale_mode": mode,
        "max_width": max_width,
        "max_height_ratio": max_height_ratio,
        "allow_frame_breaks": allow_frame_breaks,
    }


def extract_section_text(source_file: Path, section_title: str) -> str:
    text = source_file.read_text(encoding="utf-8")
    escaped_title = re.escape(section_title)
    pattern = re.compile(
        rf"\\section\{{{escaped_title}\}}(?P<body>.*?)(?=\\section\{{|\Z)",
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise ValueError(f"Could not find section '{section_title}' in {source_file}")
    return match.group("body").strip()


def parse_source_blocks(section_text: str) -> dict[str, list[SourceBlock]]:
    blocks: dict[str, list[SourceBlock]] = {}
    for match in ENV_BLOCK_RE.finditer(section_text):
        kind = match.group("kind")
        if kind not in {"definition", "remark", "example", "solution", "theorem", "proposition", "figure", "proof"}:
            continue
        title = match.group("title")
        body = match.group("body").strip()
        block_list = blocks.setdefault(kind, [])
        block_list.append(SourceBlock(kind=kind, index=len(block_list), title=title, body=body))
    return blocks


def build_deck(plan: dict[str, Any], blocks: dict[str, list[SourceBlock]]) -> dict[str, Any]:
    default_render_hints = normalize_render_hints(
        plan.get("defaults", {}).get("render_hints", DEFAULT_RENDER_HINTS),
        DEFAULT_RENDER_HINTS,
        "plan.defaults.render_hints",
    )
    slides: list[dict[str, Any]] = []

    for slide_number, slide_plan in enumerate(plan["slides"], start=1):
        for selector in slide_plan.get("source_refs", []):
            resolve_block(blocks, selector)

        slide = {
            "slide_number": slide_number,
            "slide_id": slide_plan["slide_id"],
            "source_section": plan["source_section"],
            "title": slide_plan["title"],
            "learning_goal": slide_plan["learning_goal"],
            "slide_type": slide_plan["slide_type"],
            "bullets": list(slide_plan.get("bullets", [])),
            "math_blocks": [
                resolve_math_entry(entry, blocks) for entry in slide_plan.get("math_blocks", [])
            ],
            "tikz_code": resolve_tikz_entry(slide_plan.get("tikz_code"), blocks),
            "script_draft": slide_plan["script_draft"].strip(),
            "render_hints": normalize_render_hints(
                slide_plan.get("render_hints", {}),
                default_render_hints,
                f"slide[{slide_number}].render_hints",
            ),
        }
        assert_no_raw_latex_narration(
            slide["script_draft"],
            f"plan slide {slide_number} ({slide['slide_id']}) script_draft",
        )
        slides.append(slide)

    return {
        "deck_id": plan["deck_id"],
        "source_file": plan["source_file"],
        "source_section": plan["source_section"],
        "language": plan["language"],
        "slides": slides,
    }


def resolve_math_entry(entry: Any, blocks: dict[str, list[SourceBlock]]) -> str:
    if isinstance(entry, str):
        return entry
    block = resolve_block(blocks, entry["block"])
    math_index = entry["math_index"]
    display_math = block.display_math
    if math_index < 0 or math_index >= len(display_math):
        raise ValueError(
            f"Block {describe_block_selector(entry['block'])} only has {len(display_math)} display math blocks; "
            f"requested math_index={math_index}."
        )
    return display_math[math_index]


def resolve_tikz_entry(entry: Any, blocks: dict[str, list[SourceBlock]]) -> str | None:
    if entry is None:
        return None
    if isinstance(entry, str):
        return entry
    block = resolve_block(blocks, entry["block"])
    if block.kind != "figure":
        raise ValueError(
            f"tikz_code block selector must point to a figure block, got {describe_block_selector(entry['block'])}."
        )
    return extract_figure_body(block.body)


def resolve_block(blocks: dict[str, list[SourceBlock]], selector: dict[str, Any]) -> SourceBlock:
    kind = selector["kind"]
    index = selector["index"]
    if kind not in blocks:
        raise ValueError(f"No source blocks of kind '{kind}' were found in the selected section.")
    candidates = blocks[kind]
    title = selector.get("title")
    if title is not None:
        candidates = [block for block in candidates if (block.title or "").strip() == title.strip()]
    if index < 0 or index >= len(candidates):
        raise ValueError(
            f"Selector {describe_block_selector(selector)} is out of range. "
            f"Matched {len(candidates)} block(s) of kind '{kind}'."
        )
    return candidates[index]


def describe_block_selector(selector: dict[str, Any]) -> str:
    title = selector.get("title")
    if title:
        return f"{selector['kind']}[{selector['index']}] title='{title}'"
    return f"{selector['kind']}[{selector['index']}]"


def extract_figure_body(body: str) -> str:
    figure_body = CAPTION_RE.sub("", body)
    figure_body = LABEL_RE.sub("", figure_body)
    return figure_body.strip()


def validate_deck(deck: dict[str, Any]) -> None:
    require_text(deck.get("deck_id"), "deck.deck_id")
    require_text(deck.get("source_file"), "deck.source_file")
    require_text(deck.get("source_section"), "deck.source_section")
    require_text(deck.get("language"), "deck.language")

    slides = deck.get("slides")
    if not isinstance(slides, list) or not slides:
        raise ValueError("deck.slides must be a non-empty array.")

    seen_ids: set[str] = set()
    for expected_number, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            raise ValueError(f"deck.slides[{expected_number}] must be an object.")
        slide_number = require_int(slide.get("slide_number"), f"deck.slides[{expected_number}].slide_number")
        if slide_number != expected_number:
            raise ValueError(
                f"Slide numbering must be sequential starting at 1. Expected {expected_number}, got {slide_number}."
            )
        slide_id = require_text(slide.get("slide_id"), f"deck.slides[{expected_number}].slide_id")
        if slide_id in seen_ids:
            raise ValueError(f"Duplicate slide id '{slide_id}' in deck.")
        seen_ids.add(slide_id)

        require_text(slide.get("title"), f"deck.slides[{expected_number}].title")
        require_text(slide.get("learning_goal"), f"deck.slides[{expected_number}].learning_goal")
        slide_type = require_text(slide.get("slide_type"), f"deck.slides[{expected_number}].slide_type")
        if slide_type not in ALLOWED_SLIDE_TYPES:
            raise ValueError(f"Unsupported slide_type '{slide_type}' in deck.")

        bullets = slide.get("bullets")
        if not isinstance(bullets, list) or not all(isinstance(item, str) for item in bullets):
            raise ValueError(f"deck.slides[{expected_number}].bullets must be an array of strings.")
        math_blocks = slide.get("math_blocks")
        if not isinstance(math_blocks, list) or not all(isinstance(item, str) for item in math_blocks):
            raise ValueError(f"deck.slides[{expected_number}].math_blocks must be an array of strings.")
        tikz_code = slide.get("tikz_code")
        if tikz_code is not None and not isinstance(tikz_code, str):
            raise ValueError(f"deck.slides[{expected_number}].tikz_code must be null or a string.")
        require_text(slide.get("script_draft"), f"deck.slides[{expected_number}].script_draft")
        normalize_render_hints(
            slide.get("render_hints"),
            DEFAULT_RENDER_HINTS,
            f"deck.slides[{expected_number}].render_hints",
        )


def collect_density_warnings(deck: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    for slide in deck["slides"]:
        bullets = slide["bullets"]
        math_blocks = slide["math_blocks"]
        tikz_code = slide["tikz_code"]
        heavy_elements = int(bool(tikz_code)) + int(len(math_blocks) >= 2)

        if len(bullets) > 4:
            warnings.append(
                f"Slide {slide['slide_number']} ({slide['slide_id']}) has {len(bullets)} bullets; consider trimming to 3-4."
            )
        if len(math_blocks) > 3:
            warnings.append(
                f"Slide {slide['slide_number']} ({slide['slide_id']}) has {len(math_blocks)} display-math blocks."
            )
        if heavy_elements > 1:
            warnings.append(
                f"Slide {slide['slide_number']} ({slide['slide_id']}) mixes multiple heavy elements "
                "(large figure and/or multi-step math)."
            )
    return warnings


def write_outputs(deck: dict[str, Any]) -> dict[str, Path]:
    deck_id = deck["deck_id"]
    deck_json_path = REPO_ROOT / "artifacts" / "slide_spec" / f"{deck_id}.json"
    slide_tex_path = REPO_ROOT / "artifacts" / "slides" / f"{deck_id}.tex"
    draft_path = draft_script_path(REPO_ROOT, deck_id)
    final_path = final_script_path(REPO_ROOT, deck_id)

    ensure_directory(deck_json_path.parent)
    ensure_directory(slide_tex_path.parent)
    ensure_directory(draft_path.parent)

    deck_json_path.write_text(json.dumps(deck, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    slide_tex_path.write_text(render_beamer_tex(deck), encoding="utf-8")
    draft_path.write_text(render_script_markdown(deck, "draft"), encoding="utf-8")

    return {
        "deck_json": deck_json_path,
        "slide_tex": slide_tex_path,
        "draft_script": draft_path,
        "final_script": final_path,
    }


def preserve_or_seed_final_script(deck: dict[str, Any], final_path: Path) -> None:
    if not final_path.exists():
        final_path.write_text(render_script_markdown(deck, "final"), encoding="utf-8")
        print(f"Seeded final narration file at {final_path}")
        return

    try:
        load_slide_scripts(final_path, deck, enforce_spoken_math=False)
    except Exception as exc:
        print(
            "Warning: preserved final narration file does not match the current deck. "
            f"Manual update needed: {final_path}\n{exc}"
        )
        return

    print(f"Preserved existing final narration file at {final_path}")


def render_beamer_tex(deck: dict[str, Any]) -> str:
    slides = "\n\n".join(render_frame(slide) for slide in deck["slides"])
    return (
        r"\documentclass[aspectratio=169]{beamer}" "\n\n"
        r"\usetheme{Madrid}" "\n"
        r"\usecolortheme{default}" "\n"
        r"\setbeamertemplate{navigation symbols}{}" "\n"
        r"\setbeamertemplate{footline}[frame number]" "\n"
        r"\setbeamercolor{structure}{fg=blue!60!black}" "\n"
        r"\setbeamercolor{frametitle}{fg=black,bg=blue!8}" "\n"
        r"\setbeamersize{text margin left=0.8cm, text margin right=0.8cm}" "\n\n"
        r"\usepackage[T1]{fontenc}" "\n"
        r"\usepackage[utf8]{inputenc}" "\n"
        r"\usepackage{lmodern}" "\n"
        r"\usepackage{amsmath}" "\n"
        r"\usepackage{amssymb}" "\n"
        r"\usepackage{mathtools}" "\n"
        r"\usepackage{graphicx}" "\n"
        r"\usepackage{tikz}" "\n"
        r"\usetikzlibrary{arrows.meta}" "\n"
        r"\usepackage{xcolor}" "\n\n"
        f"\\title{{{deck['source_section']}}}\n"
        r"\author{Section Media Workflow}" "\n"
        r"\date{}" "\n\n"
        r"\begin{document}" "\n\n"
        f"{slides}\n\n"
        r"\end{document}" "\n"
    )


def render_frame(slide: dict[str, Any]) -> str:
    frame_options = ["t"]
    if slide["render_hints"]["allow_frame_breaks"]:
        frame_options.append("allowframebreaks")

    parts = [f"\\begin{{frame}}[{','.join(frame_options)}]{{{slide['title']}}}"]
    parts.append(f"\\textbf{{Goal.}} {slide['learning_goal']}")

    bullets = slide["bullets"]
    if bullets:
        parts.extend(["", r"\begin{itemize}"])
        parts.extend(f"  \\item {bullet}" for bullet in bullets)
        parts.append(r"\end{itemize}")

    math_blocks = slide["math_blocks"]
    if math_blocks:
        for math_block in math_blocks:
            parts.extend(["", math_block])

    tikz_code = slide["tikz_code"]
    if tikz_code:
        parts.extend(["", render_tikz_block(tikz_code, slide["render_hints"])])

    parts.append(r"\end{frame}")
    return "\n".join(parts)


def render_tikz_block(tikz_code: str, render_hints: dict[str, Any]) -> str:
    if render_hints["tikz_scale_mode"] == "fit_width":
        cleaned_tikz = re.sub(r"^\\centering\s*", "", tikz_code).strip()
        return (
            r"\begin{center}" "\n"
            f"\\resizebox{{{render_hints['max_width']}}}{{!}}{{%\n"
            f"{cleaned_tikz}\n"
            r"}" "\n"
            r"\end{center}"
        )
    return tikz_code.strip()


def compile_beamer(tex_path: Path, compile_mode: str) -> None:
    latexmk_path = shutil.which("latexmk")
    if not latexmk_path:
        message = "latexmk was not found on PATH."
        if compile_mode == "auto":
            print(f"Skipped PDF compilation: {message}")
            return
        raise RuntimeError(message)

    beamer_cls = find_beamer_class()
    if not beamer_cls:
        message = "beamer.cls could not be located with kpsewhich."
        if compile_mode == "auto":
            print(f"Skipped PDF compilation: {message}")
            return
        raise RuntimeError(message)

    command = [
        str(latexmk_path),
        "-g",
        "-pdf",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-pdflatex=pdflatex --enable-installer %O %S",
        tex_path.name,
    ]
    result = subprocess.run(
        command,
        cwd=tex_path.parent,
        capture_output=True,
        text=True,
        encoding=locale.getpreferredencoding(False),
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "Beamer compilation failed.\n"
            f"Command: {' '.join(command)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    pdf_path = tex_path.with_suffix(".pdf")
    if not pdf_path.exists():
        raise RuntimeError(f"Beamer compilation completed without producing a PDF: {pdf_path}")

    print(f"Compiled PDF successfully with beamer at {beamer_cls}.")


def find_beamer_class() -> str | None:
    kpsewhich = shutil.which("kpsewhich")
    if not kpsewhich:
        return None
    result = subprocess.run(
        [kpsewhich, "beamer.cls"],
        capture_output=True,
        text=True,
        encoding=locale.getpreferredencoding(False),
        errors="replace",
        check=False,
    )
    path = result.stdout.strip()
    return path or None


if __name__ == "__main__":
    raise SystemExit(main())

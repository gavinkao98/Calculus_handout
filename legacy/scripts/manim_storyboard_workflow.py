from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

from shared_media_paths import (
    DEFAULT_DECK_ID,
    deck_json_path,
    manim_narration_path,
    manim_render_manifest_path,
    manim_storyboard_path,
    manim_tts_deck_path,
)
from shared_runtime_bootstrap import REPO_ROOT, ensure_directory, require_path
from shared_simple_yaml import dump_yaml, load_yaml_path
from slides_script_workflow import final_script_path, load_slide_scripts


TEMPLATE_NAMES = {
    "title_bullets",
    "definition_math",
    "example_walkthrough",
    "graph_focus",
    "procedure_steps",
    "recap_cards",
    "section_transition",
    "theorem_proof",
    "comparison",
}
SLIDE_TYPE_TO_TEMPLATE = {
    "motivation": "title_bullets",
    "overview": "title_bullets",
    "definition": "definition_math",
    "theorem": "definition_math",
    "example": "example_walkthrough",
    "warning": "example_walkthrough",
    "figure": "graph_focus",
    "procedure": "procedure_steps",
    "recap": "recap_cards",
    "transition": "section_transition",
    "proof": "theorem_proof",
    "comparison": "comparison",
}
# Map templates to default content_type when not explicitly specified.
TEMPLATE_TO_CONTENT_TYPE = {
    "definition_math": "definition",
    "example_walkthrough": "example",
    "graph_focus": "example",
    "procedure_steps": "procedure",
    "recap_cards": "recap",
    "title_bullets": "definition",
    "section_transition": "definition",
    "theorem_proof": "theorem",
    "comparison": "example",
}
DEFAULT_THEME = {
    "name": "midnight",
    "colors": {
        "background": "#0b0c10",
        "surface": "#1a1a2e",
        "primary": "#e8e8f0",
        "secondary": "#4cc9f0",
        "accent": "#f9a825",
        "text": "#c8c8d8",
        "muted_text": "#6e6e82",
        "context": "#505060",
        "math": "#7df9ff",
        "warning": "#ff6b6b",
        "grid": "#2a2a3e",
        "highlight": "#f9a825",
        "divider": "#2a2a3e",
        "success": "#06d6a0",
    },
    "typography": {
        "title_size": 44,
        "body_size": 30,
        "small_size": 24,
        "math_size": 38,
        "section_label_size": 20,
        "math_display_size": 42,
        "caption_size": 22,
    },
    "layout": {
        "top_y": 3.05,
        "side_margin": 1.2,
        "content_width": 10.6,
    },
    "transitions": {
        "element_fade": 0.4,
        "bullet_lag": 0.22,
        "quick_step": 0.35,
        "section_pause": 0.6,
        "write_speed": 0.8,
        "hero_write": 1.6,
        "context_decay": 0.25,
        "reveal_pause": 0.4,
        "exit_fade": 0.5,
    },
    "content_type_colors": {
        "definition": "secondary",
        "theorem": "accent",
        "lemma": "accent",
        "proposition": "secondary",
        "example": "highlight",
        "warning": "warning",
        "procedure": "secondary",
        "recap": "accent",
    },
}
DEFAULT_VIDEO = {
    "aspect_ratio": "16:9",
    "pixel_width": 1920,
    "pixel_height": 1080,
    "frame_rate": 30,
    "preview_scale": 0.5,
}
DEFAULT_TIMING = {
    "lead_in_seconds": 0.15,
    "hold_after_seconds": 0.45,
    "minimum_duration_seconds": 4.0,
}
DEFAULT_BRIDGE_RENDER_HINTS = {
    "tikz_scale_mode": "none",
    "max_width": r"\textwidth",
    "max_height_ratio": 0.58,
    "allow_frame_breaks": False,
}
INLINE_MATH_RE = re.compile(r"\\\((.*?)\\\)")
DISPLAY_MATH_WRAPPER_RE = re.compile(r"^\\\[(?P<body>.*)\\\]$", re.DOTALL)


def resolve_storyboard_path(deck_id: str | None = None, storyboard_path: Path | None = None) -> Path:
    if storyboard_path is not None:
        return storyboard_path.resolve()
    return manim_storyboard_path(REPO_ROOT, deck_id or DEFAULT_DECK_ID).resolve()


def load_storyboard(path: Path) -> dict[str, Any]:
    raw = load_yaml_path(require_path(path.resolve(), "Manim storyboard"))
    storyboard = normalize_storyboard(raw, path)
    validate_hook_paths(storyboard)
    return storyboard


def normalize_storyboard(storyboard: Any, source_path: Path | None = None) -> dict[str, Any]:
    label = f"storyboard {source_path}" if source_path else "storyboard"
    if not isinstance(storyboard, dict):
        raise ValueError(f"{label} must be a mapping.")

    normalized = {
        "deck_id": require_text(storyboard.get("deck_id"), f"{label}.deck_id"),
        "language": require_text(storyboard.get("language"), f"{label}.language"),
        "theme": normalize_theme(storyboard.get("theme"), f"{label}.theme"),
        "video": normalize_video(storyboard.get("video"), f"{label}.video"),
    }

    scenes = storyboard.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise ValueError(f"{label}.scenes must be a non-empty array.")

    seen_scene_ids: set[str] = set()
    normalized_scenes: list[dict[str, Any]] = []
    for index, raw_scene in enumerate(scenes, start=1):
        if not isinstance(raw_scene, dict):
            raise ValueError(f"{label}.scenes[{index}] must be a mapping.")
        scene_id = require_text(raw_scene.get("scene_id"), f"{label}.scenes[{index}].scene_id")
        if scene_id in seen_scene_ids:
            raise ValueError(f"Duplicate scene_id '{scene_id}' in {label}.")
        seen_scene_ids.add(scene_id)

        template = require_text(raw_scene.get("template"), f"{label}.scenes[{index}].template")
        if template not in TEMPLATE_NAMES:
            raise ValueError(
                f"Unsupported template '{template}' in {label}.scenes[{index}]. "
                f"Allowed values: {sorted(TEMPLATE_NAMES)}"
            )

        # Infer content_type from template if not explicitly set.
        content_type = raw_scene.get("content_type")
        if content_type is not None:
            content_type = require_text(content_type, f"{label}.scenes[{index}].content_type")
        else:
            content_type = TEMPLATE_TO_CONTENT_TYPE.get(template, "definition")

        scene_exit_val = raw_scene.get("scene_exit")
        if scene_exit_val is not None:
            scene_exit_val = require_text(scene_exit_val, f"{label}.scenes[{index}].scene_exit")
            if scene_exit_val not in {"fade", "hold", "none"}:
                raise ValueError(f"{label}.scenes[{index}].scene_exit must be fade, hold, or none.")
        else:
            scene_exit_val = "fade"

        voiceover_beats = raw_scene.get("voiceover_beats")
        normalized_beats = None
        if voiceover_beats is not None:
            normalized_beats = normalize_voiceover_beats(
                voiceover_beats, f"{label}.scenes[{index}].voiceover_beats"
            )
            voiceover = voiceover_text_from_beats(normalized_beats)
        else:
            voiceover = require_text(raw_scene.get("voiceover"), f"{label}.scenes[{index}].voiceover")

        normalized_scene = {
            "scene_number": index,
            "scene_id": scene_id,
            "template": template,
            "content_type": content_type,
            "scene_exit": scene_exit_val,
            "title": require_text(raw_scene.get("title"), f"{label}.scenes[{index}].title"),
            "voiceover": voiceover,
            "data": normalize_scene_data(template, raw_scene.get("data"), f"{label}.scenes[{index}].data"),
            "timing": normalize_timing(raw_scene.get("timing"), f"{label}.scenes[{index}].timing"),
            "disabled": require_optional_bool(raw_scene.get("disabled"), f"{label}.scenes[{index}].disabled", False),
        }
        if normalized_beats is not None:
            normalized_scene["voiceover_beats"] = normalized_beats

        # Optional reveal_groups for progressive reveal.
        reveal_groups = raw_scene.get("reveal_groups")
        if reveal_groups is not None:
            normalized_scene["reveal_groups"] = normalize_reveal_groups(
                reveal_groups, f"{label}.scenes[{index}].reveal_groups"
            )

        hook = raw_scene.get("hook")
        if hook is not None:
            normalized_scene["hook"] = require_text(hook, f"{label}.scenes[{index}].hook")
        normalized_scenes.append(normalized_scene)

    normalized["scenes"] = normalized_scenes
    return normalized


def normalize_theme(value: Any, label: str) -> dict[str, Any]:
    raw = {} if value is None else require_mapping(value, label)
    theme = deep_merge(DEFAULT_THEME, raw)
    require_text(theme.get("name"), f"{label}.name")
    colors = require_mapping(theme.get("colors"), f"{label}.colors")
    for color_name, color_value in colors.items():
        require_text(color_value, f"{label}.colors.{color_name}")
    typography = require_mapping(theme.get("typography"), f"{label}.typography")
    for size_name in ("title_size", "body_size", "small_size", "math_size",
                       "section_label_size", "math_display_size", "caption_size"):
        require_number(typography.get(size_name), f"{label}.typography.{size_name}")
    layout = require_mapping(theme.get("layout"), f"{label}.layout")
    for layout_name in ("top_y", "side_margin", "content_width"):
        require_number(layout.get(layout_name), f"{label}.layout.{layout_name}")
    transitions = require_mapping(theme.get("transitions"), f"{label}.transitions")
    for name in (
        "element_fade",
        "bullet_lag",
        "quick_step",
        "section_pause",
        "write_speed",
        "hero_write",
        "context_decay",
        "reveal_pause",
        "exit_fade",
    ):
        require_number(transitions.get(name), f"{label}.transitions.{name}")
    return theme


def normalize_video(value: Any, label: str) -> dict[str, Any]:
    raw = {} if value is None else require_mapping(value, label)
    video = deep_merge(DEFAULT_VIDEO, raw)
    require_text(video.get("aspect_ratio"), f"{label}.aspect_ratio")
    require_positive_int(video.get("pixel_width"), f"{label}.pixel_width")
    require_positive_int(video.get("pixel_height"), f"{label}.pixel_height")
    require_positive_number(video.get("frame_rate"), f"{label}.frame_rate")
    preview_scale = require_positive_number(video.get("preview_scale"), f"{label}.preview_scale")
    if preview_scale > 1:
        raise ValueError(f"{label}.preview_scale must be <= 1.")
    return video


def normalize_timing(value: Any, label: str) -> dict[str, Any]:
    raw = {} if value is None else require_mapping(value, label)
    timing = deep_merge(DEFAULT_TIMING, raw)
    for key in ("lead_in_seconds", "hold_after_seconds", "minimum_duration_seconds"):
        require_non_negative_number(timing.get(key), f"{label}.{key}")
    return timing


def normalize_voiceover_beats(value: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a non-empty array.")

    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, beat in enumerate(value):
        entry_label = f"{label}[{index}]"
        item = require_mapping(beat, entry_label)
        beat_id = require_text(item.get("id"), f"{entry_label}.id")
        if beat_id in seen_ids:
            raise ValueError(f"Duplicate voiceover beat id '{beat_id}' in {label}.")
        seen_ids.add(beat_id)

        reveal = item.get("reveal", [])
        if reveal is None:
            reveal = []
        if not isinstance(reveal, list) or not all(isinstance(entry, str) and entry.strip() for entry in reveal):
            raise ValueError(f"{entry_label}.reveal must be an array of non-empty strings.")

        if "hold_after" in item and "hold_after_seconds" in item:
            raise ValueError(f"{entry_label} must use only one of hold_after or hold_after_seconds.")
        hold_after = item.get("hold_after_seconds", item.get("hold_after", 0.0))
        duration_override = item.get("duration_seconds")

        normalized_beat = {
            "id": beat_id,
            "text": require_text(item.get("text"), f"{entry_label}.text"),
            "reveal": [entry.strip() for entry in reveal],
            "hold_after_seconds": require_non_negative_number(hold_after, f"{entry_label}.hold_after_seconds"),
        }
        if duration_override is not None:
            normalized_beat["duration_seconds"] = require_positive_number(
                duration_override, f"{entry_label}.duration_seconds"
            )
        normalized.append(normalized_beat)
    return normalized


def voiceover_text_from_beats(beats: list[dict[str, Any]]) -> str:
    return normalize_narration_text(" ".join(beat["text"] for beat in beats))


def normalize_scene_data(template: str, value: Any, label: str) -> dict[str, Any]:
    data = require_mapping(value, label)
    if template == "title_bullets":
        data["bullets"] = require_string_list(data.get("bullets"), f"{label}.bullets")
        return data
    if template == "definition_math":
        data["statement"] = require_text(data.get("statement"), f"{label}.statement")
        data["math_lines"] = normalize_math_lines(data.get("math_lines"), f"{label}.math_lines")
        if "supporting_bullets" in data:
            data["supporting_bullets"] = require_string_list(data.get("supporting_bullets"), f"{label}.supporting_bullets")
        return data
    if template == "example_walkthrough":
        data["steps"] = require_string_list(data.get("steps"), f"{label}.steps")
        data["takeaway"] = require_text(data.get("takeaway"), f"{label}.takeaway")
        data["math_lines"] = normalize_math_lines_optional(data.get("math_lines"), f"{label}.math_lines")
        data["math_layout"] = normalize_math_layout(data.get("math_layout"), f"{label}.math_layout")
        data["decay_previous"] = require_optional_bool(data.get("decay_previous"), f"{label}.decay_previous", True)
        return data
    if template == "graph_focus":
        data["axes"] = normalize_axes(data.get("axes"), f"{label}.axes")
        data["plots"] = normalize_plots(data.get("plots"), f"{label}.plots")
        data["annotations"] = normalize_annotations(data.get("annotations"), f"{label}.annotations")
        if "source_figure_tex" in data:
            data["source_figure_tex"] = require_text(data.get("source_figure_tex"), f"{label}.source_figure_tex")
        return data
    if template == "procedure_steps":
        data["steps"] = require_string_list(data.get("steps"), f"{label}.steps")
        data["worked_equations"] = normalize_math_lines(data.get("worked_equations"), f"{label}.worked_equations")
        data["math_layout"] = normalize_math_layout(data.get("math_layout"), f"{label}.math_layout")
        return data
    if template == "recap_cards":
        data["points"] = require_string_list(data.get("points"), f"{label}.points")
        data["identities"] = normalize_math_lines_optional(data.get("identities"), f"{label}.identities")
        return data
    if template == "section_transition":
        if "subtitle" in data:
            data["subtitle"] = require_text(data.get("subtitle"), f"{label}.subtitle")
        if "upcoming" in data:
            data["upcoming"] = require_string_list(data.get("upcoming"), f"{label}.upcoming")
        return data
    if template == "theorem_proof":
        data["theorem_statement"] = require_text(data.get("theorem_statement"), f"{label}.theorem_statement")
        data["proof_steps"] = require_string_list(data.get("proof_steps"), f"{label}.proof_steps")
        data["qed"] = require_optional_bool(data.get("qed"), f"{label}.qed", True)
        return data
    if template == "comparison":
        for side in ("left", "right"):
            side_data = require_mapping(data.get(side), f"{label}.{side}")
            side_data["label"] = require_text(side_data.get("label"), f"{label}.{side}.label")
            if "color" in side_data:
                side_data["color"] = require_text(side_data.get("color"), f"{label}.{side}.color")
            side_data["items"] = require_string_list(side_data.get("items"), f"{label}.{side}.items")
            if "math" in side_data:
                side_data["math"] = require_text(side_data.get("math"), f"{label}.{side}.math")
            data[side] = side_data
        return data
    raise ValueError(f"Unsupported template '{template}'.")


def normalize_axes(value: Any, label: str) -> dict[str, Any]:
    axes = require_mapping(value, label)
    axes["x_range"] = require_number_list(axes.get("x_range"), f"{label}.x_range", min_length=2, max_length=3)
    axes["y_range"] = require_number_list(axes.get("y_range"), f"{label}.y_range", min_length=2, max_length=3)
    axes["x_length"] = require_positive_number(axes.get("x_length"), f"{label}.x_length")
    axes["y_length"] = require_positive_number(axes.get("y_length"), f"{label}.y_length")
    if "include_numbers" in axes:
        axes["include_numbers"] = require_optional_bool(axes.get("include_numbers"), f"{label}.include_numbers", False)
    if "tips" in axes:
        axes["tips"] = require_optional_bool(axes.get("tips"), f"{label}.tips", True)
    return axes


def normalize_plots(value: Any, label: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array.")
    normalized: list[dict[str, Any]] = []
    for index, plot in enumerate(value):
        entry_label = f"{label}[{index}]"
        item = require_mapping(plot, entry_label)
        kind = require_text(item.get("kind"), f"{entry_label}.kind")
        if kind not in {"function", "line", "point"}:
            raise ValueError(f"{entry_label}.kind must be one of function, line, point.")
        item["kind"] = kind
        if kind == "function":
            item["expression"] = require_text(item.get("expression"), f"{entry_label}.expression")
            if "x_range" in item:
                item["x_range"] = require_number_list(item.get("x_range"), f"{entry_label}.x_range", min_length=2, max_length=3)
        elif kind == "line":
            item["start"] = require_number_list(item.get("start"), f"{entry_label}.start", exact_length=2)
            item["end"] = require_number_list(item.get("end"), f"{entry_label}.end", exact_length=2)
        else:
            item["point"] = require_number_list(item.get("point"), f"{entry_label}.point", exact_length=2)
            if "radius" in item:
                item["radius"] = require_positive_number(item.get("radius"), f"{entry_label}.radius")
        if "color" in item:
            item["color"] = require_text(item.get("color"), f"{entry_label}.color")
        if "label" in item:
            item["label"] = require_text(item.get("label"), f"{entry_label}.label")
        if "dashed" in item:
            item["dashed"] = require_optional_bool(item.get("dashed"), f"{entry_label}.dashed", False)
        if "label_side" in item:
            side = require_text(item.get("label_side"), f"{entry_label}.label_side")
            if side not in {"up", "down", "left", "right"}:
                raise ValueError(f"{entry_label}.label_side must be up, down, left, or right.")
            item["label_side"] = side
        if "label_x" in item:
            item["label_x"] = require_number(item.get("label_x"), f"{entry_label}.label_x")
        normalized.append(item)
    return normalized


def normalize_annotations(value: Any, label: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array.")
    normalized: list[dict[str, Any]] = []
    for index, annotation in enumerate(value):
        entry_label = f"{label}[{index}]"
        item = require_mapping(annotation, entry_label)
        item["text"] = require_text(item.get("text"), f"{entry_label}.text")
        if "anchor" in item:
            item["anchor"] = require_number_list(item.get("anchor"), f"{entry_label}.anchor", exact_length=2)
        if "side" in item:
            side = require_text(item.get("side"), f"{entry_label}.side")
            if side not in {"left", "right", "up", "down", "center"}:
                raise ValueError(f"{entry_label}.side must be left, right, up, down, or center.")
            item["side"] = side
        normalized.append(item)
    return normalized


def normalize_reveal_groups(value: Any, label: str) -> list[dict[str, Any]]:
    """Validate and normalise a ``reveal_groups`` list."""
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array.")
    normalized: list[dict[str, Any]] = []
    for index, group in enumerate(value):
        entry_label = f"{label}[{index}]"
        item = require_mapping(group, entry_label)
        elements = item.get("elements", [])
        if not isinstance(elements, list) or not all(isinstance(e, str) for e in elements):
            raise ValueError(f"{entry_label}.elements must be an array of strings.")
        pause = item.get("pause_after", 0.3)
        if not isinstance(pause, (int, float)):
            raise ValueError(f"{entry_label}.pause_after must be a number.")
        normalized.append({"elements": elements, "pause_after": float(pause)})
    return normalized


def normalize_math_lines(value: Any, label: str) -> list[dict[str, Any]]:
    """Normalise math_lines to the extended format.

    Accepts both plain strings and dicts with ``text`` / ``animation`` keys.
    Plain strings are coerced to ``{"text": str, "animation": "write"}``.
    """
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a non-empty array.")
    normalized: list[dict[str, Any]] = []
    for index, entry in enumerate(value):
        entry_label = f"{label}[{index}]"
        if isinstance(entry, str):
            if not entry.strip():
                raise ValueError(f"{entry_label} must be a non-empty string.")
            normalized.append({"text": entry.strip(), "animation": "write"})
        elif isinstance(entry, dict):
            text = require_text(entry.get("text"), f"{entry_label}.text")
            animation = entry.get("animation", "write")
            if animation not in {"write", "fade", "highlight", "transform_from_previous"}:
                raise ValueError(
                    f"{entry_label}.animation must be one of: write, fade, highlight, transform_from_previous."
                )
            normalized.append({"text": text, "animation": animation})
        else:
            raise ValueError(f"{entry_label} must be a string or mapping.")
    return normalized


def normalize_math_lines_optional(value: Any, label: str) -> list[dict[str, Any]]:
    """Like ``normalize_math_lines`` but returns [] if value is missing/empty."""
    if value is None or (isinstance(value, list) and len(value) == 0):
        return []
    return normalize_math_lines(value, label)


def normalize_math_layout(value: Any, label: str) -> str:
    if value is None:
        return "auto"
    layout = require_text(value, label)
    if layout not in {"auto", "left", "equals_aligned"}:
        raise ValueError(f"{label} must be one of: auto, left, equals_aligned.")
    return layout


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    keys = set(base) | set(override)
    for key in keys:
        base_value = base.get(key)
        override_value = override.get(key)
        if isinstance(base_value, dict) and isinstance(override_value, dict):
            merged[key] = deep_merge(base_value, override_value)
        elif key in override:
            merged[key] = override_value
        else:
            merged[key] = base_value
    return merged


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a mapping.")
    return dict(value)


def require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string.")
    return value.strip()


def require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{label} must be an array of non-empty strings.")
    return [item.strip() for item in value]


def require_number_list(
    value: Any,
    label: str,
    *,
    min_length: int | None = None,
    max_length: int | None = None,
    exact_length: int | None = None,
) -> list[float]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a non-empty array of numbers.")
    if exact_length is not None and len(value) != exact_length:
        raise ValueError(f"{label} must contain exactly {exact_length} numbers.")
    if min_length is not None and len(value) < min_length:
        raise ValueError(f"{label} must contain at least {min_length} numbers.")
    if max_length is not None and len(value) > max_length:
        raise ValueError(f"{label} must contain at most {max_length} numbers.")
    if not all(isinstance(item, (int, float)) for item in value):
        raise ValueError(f"{label} must contain only numbers.")
    return [float(item) for item in value]


def require_number(value: Any, label: str) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a number.")
    return float(value)


def require_positive_number(value: Any, label: str) -> float:
    number = require_number(value, label)
    if number <= 0:
        raise ValueError(f"{label} must be positive.")
    return number


def require_non_negative_number(value: Any, label: str) -> float:
    number = require_number(value, label)
    if number < 0:
        raise ValueError(f"{label} must be non-negative.")
    return number


def require_positive_int(value: Any, label: str) -> int:
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{label} must be a positive integer.")
    return value


def require_optional_bool(value: Any, label: str, default: bool) -> bool:
    if value is None:
        return default
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be a boolean when provided.")
    return value


def load_deck_json(path: Path) -> dict[str, Any]:
    with require_path(path.resolve(), "slide deck JSON").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_seed_voiceovers(deck: dict[str, Any]) -> tuple[list[str], str]:
    script_file = final_script_path(REPO_ROOT, deck["deck_id"]).resolve()
    if script_file.exists():
        try:
            return load_slide_scripts(script_file, deck, enforce_spoken_math=False), str(script_file)
        except Exception:
            pass
    voiceovers = [require_text(slide.get("script_draft"), f"deck slide {slide.get('slide_id')} script_draft") for slide in deck["slides"]]
    return voiceovers, "deck script_draft"


def build_seed_storyboard(deck: dict[str, Any], voiceovers: list[str] | None = None) -> dict[str, Any]:
    slides = deck.get("slides")
    if not isinstance(slides, list) or not slides:
        raise ValueError("Deck JSON must contain a non-empty slides array.")
    chosen_voiceovers = voiceovers or [slide["script_draft"] for slide in slides]
    if len(chosen_voiceovers) != len(slides):
        raise ValueError("Voiceover count does not match slide count while seeding storyboard.")

    return {
        "deck_id": require_text(deck.get("deck_id"), "deck.deck_id"),
        "language": require_text(deck.get("language"), "deck.language"),
        "theme": DEFAULT_THEME,
        "video": DEFAULT_VIDEO,
        "scenes": [
            build_seed_scene_from_slide(slide, chosen_voiceovers[index])
            for index, slide in enumerate(slides)
        ],
    }


def build_seed_scene_from_slide(slide: dict[str, Any], voiceover: str) -> dict[str, Any]:
    slide_type = require_text(slide.get("slide_type"), f"slide {slide.get('slide_id')} slide_type")
    if slide_type not in SLIDE_TYPE_TO_TEMPLATE:
        raise ValueError(f"Unsupported slide_type '{slide_type}' in deck JSON.")
    template = SLIDE_TYPE_TO_TEMPLATE[slide_type]
    bullets = list(slide.get("bullets", []))
    math_blocks = list(slide.get("math_blocks", []))
    return {
        "scene_id": require_text(slide.get("slide_id"), f"slide {slide.get('slide_number')} slide_id"),
        "template": template,
        "title": require_text(slide.get("title"), f"slide {slide.get('slide_number')} title"),
        "voiceover": require_text(voiceover, f"slide {slide.get('slide_number')} voiceover"),
        "timing": DEFAULT_TIMING,
        "data": build_seed_scene_data(template, slide, bullets, math_blocks),
    }


def build_seed_scene_data(template: str, slide: dict[str, Any], bullets: list[str], math_blocks: list[str]) -> dict[str, Any]:
    if template == "title_bullets":
        return {"bullets": bullets}
    if template == "definition_math":
        return {
            "statement": bullets[0] if bullets else slide["learning_goal"],
            "math_lines": math_blocks,
            "supporting_bullets": bullets[1:],
        }
    if template == "example_walkthrough":
        return {
            "steps": bullets or [slide["learning_goal"]],
            "takeaway": slide["learning_goal"],
            "math_lines": math_blocks,
        }
    if template == "graph_focus":
        annotations = [{"text": item} for item in bullets] if bullets else [{"text": slide["learning_goal"]}]
        return {
            "axes": {
                "x_range": [-3, 3, 1],
                "y_range": [-1, 4, 1],
                "x_length": 6.2,
                "y_length": 4.2,
                "include_numbers": False,
                "tips": True,
            },
            "plots": [],
            "annotations": annotations,
            "source_figure_tex": slide.get("tikz_code") or "",
        }
    if template == "procedure_steps":
        return {
            "steps": bullets or [slide["learning_goal"]],
            "worked_equations": math_blocks,
        }
    if template == "recap_cards":
        return {
            "points": bullets or [slide["learning_goal"]],
            "identities": math_blocks,
        }
    raise ValueError(f"Unsupported template '{template}'.")


def write_storyboard(path: Path, storyboard: dict[str, Any]) -> None:
    ensure_directory(path.parent)
    path.write_text(dump_yaml(strip_runtime_fields(storyboard)), encoding="utf-8")


def strip_runtime_fields(storyboard: dict[str, Any]) -> dict[str, Any]:
    cleaned = {
        "deck_id": storyboard["deck_id"],
        "language": storyboard["language"],
        "theme": storyboard["theme"],
        "video": storyboard["video"],
        "scenes": [],
    }
    for scene in storyboard["scenes"]:
        item = {
            "scene_id": scene["scene_id"],
            "template": scene["template"],
            "title": scene["title"],
            "voiceover": scene["voiceover"],
            "timing": scene["timing"],
            "data": scene["data"],
        }
        if scene.get("content_type"):
            item["content_type"] = scene["content_type"]
        if scene.get("scene_exit") and scene["scene_exit"] != "fade":
            item["scene_exit"] = scene["scene_exit"]
        if scene.get("reveal_groups"):
            item["reveal_groups"] = scene["reveal_groups"]
        if scene.get("voiceover_beats"):
            item["voiceover_beats"] = scene["voiceover_beats"]
        if scene.get("disabled"):
            item["disabled"] = True
        if scene.get("hook"):
            item["hook"] = scene["hook"]
        cleaned["scenes"].append(item)
    return cleaned


def find_scene(storyboard: dict[str, Any], scene_id: str) -> dict[str, Any]:
    for scene in storyboard["scenes"]:
        if scene["scene_id"] == scene_id:
            return scene
    raise KeyError(f"Scene '{scene_id}' was not found in storyboard '{storyboard['deck_id']}'.")


def enabled_scenes(storyboard: dict[str, Any]) -> list[dict[str, Any]]:
    return [scene for scene in storyboard["scenes"] if not scene.get("disabled", False)]


def storyboard_to_bridge_deck(storyboard: dict[str, Any], storyboard_path: Path) -> dict[str, Any]:
    slides = []
    for scene in enabled_scenes(storyboard):
        slides.append(
            {
                "slide_number": scene["scene_number"],
                "slide_id": scene["scene_id"],
                "source_section": storyboard["deck_id"],
                "title": scene["title"],
                "learning_goal": scene["title"],
                "slide_type": scene["template"],
                "bullets": [],
                "math_blocks": [],
                "tikz_code": None,
                "script_draft": normalize_narration_text(scene["voiceover"]),
                "voiceover_beats": scene.get("voiceover_beats", []),
                "render_hints": DEFAULT_BRIDGE_RENDER_HINTS,
            }
        )
    return {
        "deck_id": storyboard["deck_id"],
        "source_file": str(storyboard_path.relative_to(REPO_ROOT)),
        "source_section": storyboard["deck_id"],
        "language": storyboard["language"],
        "slides": slides,
    }


def normalize_narration_text(text: str) -> str:
    return str(text).replace("\r\n", "\n").strip()


def voiceover_content_hash(text: str) -> str:
    return hashlib.sha256(normalize_narration_text(text).encode("utf-8")).hexdigest()


def render_storyboard_script_markdown(storyboard: dict[str, Any], storyboard_path: Path) -> str:
    try:
        from manim_templates.narration_compiler import compile_narration as _compile_narration
        from manim_templates.narration_markers import render_marked_narration
    except ImportError:
        _compile_narration = None
        render_marked_narration = None  # type: ignore

    sections = [
        f"# {storyboard['deck_id']} Final Narration",
        "",
        f"Source file: `{storyboard_path.relative_to(REPO_ROOT)}`",
        f"Deck ID: `{storyboard['deck_id']}`",
        "",
        "You may edit the narration text below each **Narration:** heading.",
        "Inline 〔顯示...〕 markers correspond to dynamic reveal elements — please leave them and the hidden bookmark-marks comment in place; the sync tool relies on them to restore bookmark positions.",
        "For scenes with **Voiceover Beats**, edit the beat text/reveal map in the storyboard YAML; the joined beat text is exported here for proofreading.",
        "Do NOT change the hidden hash comment lines — they are used for stale-file conflict detection.",
        "Do NOT change the Slide ID lines — they are used to match edits back to the correct scene.",
        "After editing, run `python tools/manim_sync_narration_back.py --deck-id "
        + storyboard["deck_id"]
        + "` to write changes back to the storyboard YAML.",
        "",
    ]
    for scene in enabled_scenes(storyboard):
        if _compile_narration is not None and render_marked_narration is not None:
            compiled = _compile_narration(scene)
            display_narration = (
                render_marked_narration(compiled) if compiled else normalize_narration_text(scene["voiceover"])
            )
        else:
            display_narration = normalize_narration_text(scene["voiceover"])
        sections.extend(
            [
                f"## Slide {scene['scene_number']}: {scene['title']}",
                "",
                f"Slide ID: `{scene['scene_id']}`",
                f"<!-- voiceover-hash: {voiceover_content_hash(scene['voiceover'])} -->",
                f"Scene template: `{scene['template']}`",
                "",
                "Narration:",
                "",
                display_narration,
                "",
            ]
        )
        if scene.get("voiceover_beats"):
            sections.extend(["Voiceover Beats:", ""])
            for beat in scene["voiceover_beats"]:
                reveal = ", ".join(beat.get("reveal", [])) or "none"
                sections.extend(
                    [
                        f"- `{beat['id']}` reveal: {reveal}",
                        f"  text: {normalize_narration_text(beat['text'])}",
                    ]
                )
            sections.append("")
    return "\n".join(sections).strip() + "\n"


def export_storyboard_bridge_files(
    storyboard: dict[str, Any],
    storyboard_path: Path,
    *,
    script_path: Path | None = None,
    deck_path: Path | None = None,
) -> dict[str, Path]:
    resolved_script_path = (script_path or manim_narration_path(REPO_ROOT, storyboard["deck_id"])).resolve()
    resolved_deck_path = (deck_path or manim_tts_deck_path(REPO_ROOT, storyboard["deck_id"])).resolve()
    ensure_directory(resolved_script_path.parent)
    ensure_directory(resolved_deck_path.parent)

    bridge_deck = storyboard_to_bridge_deck(storyboard, storyboard_path)
    resolved_script_path.write_text(render_storyboard_script_markdown(storyboard, storyboard_path), encoding="utf-8")
    resolved_deck_path.write_text(json.dumps(bridge_deck, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"script_path": resolved_script_path, "deck_path": resolved_deck_path}


def scene_visual_fingerprint(storyboard: dict[str, Any], scene: dict[str, Any], quality: str) -> str:
    """Fingerprint only the rendered visual payload for scene-cache reuse.

    Narration and mux timing are intentionally excluded because they affect the
    bridge/audio pipeline, not the silent Manim scene render itself. Beat maps
    are included because they control progressive reveal order.
    """
    payload = {
        "deck_id": storyboard["deck_id"],
        "scene": strip_visual_scene(scene),
        "theme": storyboard["theme"],
        "video": storyboard["video"],
        "quality": quality,
        "engine": template_engine_fingerprint(),
    }
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def strip_visual_scene(scene: dict[str, Any]) -> dict[str, Any]:
    cleaned = {
        "scene_id": scene["scene_id"],
        "template": scene["template"],
        "content_type": scene.get("content_type", "definition"),
        "scene_exit": scene.get("scene_exit", "fade"),
        "title": scene["title"],
        "data": scene["data"],
    }
    if scene.get("reveal_groups"):
        cleaned["reveal_groups"] = scene["reveal_groups"]
    if scene.get("voiceover_beats"):
        cleaned["voiceover_beats"] = scene["voiceover_beats"]
    if scene.get("hook"):
        cleaned["hook"] = scene["hook"]
    return cleaned


def scene_render_fingerprint(
    storyboard: dict[str, Any],
    scene: dict[str, Any],
    quality: str,
    audio_timing: dict[str, Any] | None = None,
) -> str:
    if not scene.get("voiceover_beats"):
        return scene_visual_fingerprint(storyboard, scene, quality)
    payload = {
        "visual_fingerprint": scene_visual_fingerprint(storyboard, scene, quality),
    }
    payload["timing"] = scene["timing"]
    payload["audio_timing"] = compact_audio_timing(audio_timing)
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def compact_audio_timing(audio_timing: dict[str, Any] | None) -> dict[str, Any] | None:
    if not audio_timing:
        return None
    return {
        "beats": [
            {
                "id": beat.get("id"),
                "audio_seconds": beat.get("audio_seconds"),
                "hold_after_seconds": beat.get("hold_after_seconds"),
            }
            for beat in audio_timing.get("beats", [])
        ]
    }


scene_fingerprint = scene_visual_fingerprint
strip_runtime_scene = strip_visual_scene


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def template_engine_fingerprint() -> str:
    paths = [
        REPO_ROOT / "tools" / "manim_storyboard_workflow.py",
        REPO_ROOT / "tools" / "manim_runtime.py",
    ]
    template_root = REPO_ROOT / "tools" / "manim_templates"
    if template_root.exists():
        paths.extend(sorted(template_root.rglob("*.py")))
    hasher = hashlib.sha256()
    for path in sorted({candidate.resolve() for candidate in paths if candidate.exists()}):
        hasher.update(str(path.relative_to(REPO_ROOT)).encode("utf-8"))
        hasher.update(path.read_bytes())
    return hasher.hexdigest()


def load_render_manifest(deck_id: str) -> dict[str, Any]:
    path = manim_render_manifest_path(REPO_ROOT, deck_id).resolve()
    if not path.exists():
        return {"deck_id": deck_id, "scenes": {}}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or "scenes" not in data or not isinstance(data["scenes"], dict):
        return {"deck_id": deck_id, "scenes": {}}
    return data


def write_render_manifest(deck_id: str, manifest: dict[str, Any]) -> Path:
    path = manim_render_manifest_path(REPO_ROOT, deck_id).resolve()
    ensure_directory(path.parent)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def resolve_hook_path(import_path: str) -> Path | None:
    module_name, _, attribute_name = import_path.rpartition(".")
    if not module_name or not attribute_name:
        return None
    try:
        spec = importlib.util.find_spec(module_name)
    except ModuleNotFoundError:
        fallback = REPO_ROOT / (module_name.replace(".", "/") + ".py")
        return fallback if fallback.exists() else None
    if spec is None or spec.origin is None or spec.origin in {"built-in", "frozen"}:
        fallback = REPO_ROOT / (module_name.replace(".", "/") + ".py")
        return fallback if fallback.exists() else None
    return Path(spec.origin)


def validate_hook_paths(storyboard: dict[str, Any]) -> None:
    for scene in enabled_scenes(storyboard):
        hook = scene.get("hook")
        if not hook:
            continue
        hook_path = resolve_hook_path(hook)
        if hook_path is None or not hook_path.exists():
            raise ValueError(
                f"Hook '{hook}' for scene '{scene['scene_id']}' could not be resolved to a local Python file."
            )


def suggested_seed_source(deck_id: str) -> Path:
    return deck_json_path(REPO_ROOT, deck_id).resolve()


def default_bridge_paths(deck_id: str) -> dict[str, Path]:
    return {
        "storyboard_path": manim_storyboard_path(REPO_ROOT, deck_id).resolve(),
        "deck_json_path": deck_json_path(REPO_ROOT, deck_id).resolve(),
        "bridge_deck_path": manim_tts_deck_path(REPO_ROOT, deck_id).resolve(),
        "bridge_script_path": manim_narration_path(REPO_ROOT, deck_id).resolve(),
    }


def to_tex_text(text: str) -> str:
    return INLINE_MATH_RE.sub(lambda match: f"${match.group(1)}$", text.strip())


def to_mathtex_body(display_math: str) -> str:
    stripped = display_math.strip()
    match = DISPLAY_MATH_WRAPPER_RE.match(stripped)
    body = match.group("body") if match else stripped
    return body.strip()

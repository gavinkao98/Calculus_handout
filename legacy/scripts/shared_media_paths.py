from __future__ import annotations

from pathlib import Path


DEFAULT_DECK_ID = "ch01_inverse_functions"


def deck_json_path(repo_root: Path, deck_id: str) -> Path:
    return repo_root / "artifacts" / "slide_spec" / f"{deck_id}.json"


def slide_tex_path(repo_root: Path, deck_id: str) -> Path:
    return repo_root / "artifacts" / "slides" / f"{deck_id}.tex"


def slide_pdf_path(repo_root: Path, deck_id: str) -> Path:
    return repo_root / "artifacts" / "slides" / f"{deck_id}.pdf"


def audio_dir_path(repo_root: Path, deck_id: str, suffix: str = "") -> Path:
    stem = deck_id if not suffix else f"{deck_id}_{suffix}"
    return repo_root / "artifacts" / "audio" / stem


def audio_manifest_path(repo_root: Path, deck_id: str, suffix: str = "") -> Path:
    return audio_dir_path(repo_root, deck_id, suffix) / "manifest.json"


def video_output_path(repo_root: Path, stem: str) -> Path:
    return repo_root / "artifacts" / "video" / f"{stem}.mp4"


def manim_storyboard_path(repo_root: Path, deck_id: str) -> Path:
    return repo_root / "inputs" / "manim_storyboards" / f"{deck_id}.yml"


def manim_artifact_dir(repo_root: Path, deck_id: str) -> Path:
    return repo_root / "artifacts" / "manim" / deck_id


def manim_scene_cache_dir(repo_root: Path, deck_id: str) -> Path:
    return manim_artifact_dir(repo_root, deck_id) / "scenes"


def manim_segment_dir(repo_root: Path, deck_id: str) -> Path:
    return manim_artifact_dir(repo_root, deck_id) / "segments"


def manim_graph_preview_dir(repo_root: Path, deck_id: str) -> Path:
    return manim_artifact_dir(repo_root, deck_id) / "graph_previews"


def manim_render_manifest_path(repo_root: Path, deck_id: str) -> Path:
    return manim_artifact_dir(repo_root, deck_id) / "render_manifest.json"


def manim_narration_path(repo_root: Path, deck_id: str) -> Path:
    return manim_artifact_dir(repo_root, deck_id) / "narration.md"


def manim_tts_deck_path(repo_root: Path, deck_id: str) -> Path:
    return manim_artifact_dir(repo_root, deck_id) / "tts_deck.json"


def manim_scene_output_path(repo_root: Path, deck_id: str, scene_number: int, scene_id: str) -> Path:
    return manim_scene_cache_dir(repo_root, deck_id) / f"{scene_number:02d}_{scene_id}.mp4"


def manim_segment_output_path(repo_root: Path, deck_id: str, scene_number: int, scene_id: str) -> Path:
    return manim_segment_dir(repo_root, deck_id) / f"{scene_number:02d}_{scene_id}.mp4"


def manim_graph_preview_path(repo_root: Path, deck_id: str, scene_id: str) -> Path:
    return manim_graph_preview_dir(repo_root, deck_id) / f"{scene_id}.png"

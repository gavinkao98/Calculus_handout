"""Put the repo-local vendored dependency dirs on sys.path; derive per-section output dirs.

Some machines carry PyYAML in the repo-local `.deps` / `.deps_voiceover` dirs rather than
in `.venv`; call bootstrap() before importing yaml. (The pre-2026-09-28 version also set
the global TeX template for the archived renderer -- see
legacy/manim_video/pipeline/_bootstrap.py.)
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_DEP_DIRS = (".deps_voiceover", ".deps")


def bootstrap() -> None:
    for name in _DEP_DIRS:
        dep = REPO_ROOT / name
        if dep.exists() and str(dep) not in sys.path:
            sys.path.insert(0, str(dep))


def section_output_dir(meta: dict) -> Path:
    """Derive per-section output directory from storyboard meta.

    e.g. meta.section="1.3" → <REPO_ROOT>/video/output/ch01/s1.3
    """
    section = meta.get("section", "")
    ch_num = section.split(".")[0] if section else "00"
    return (
        REPO_ROOT / "video" / "output" / f"ch{int(ch_num):02d}" / f"s{section}"
    )

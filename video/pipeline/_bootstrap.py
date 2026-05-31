"""Put vendored deps (manim, yaml) on sys.path and register design fonts.

manim/yaml are not in .venv; they live under .deps_voiceover (manim 0.20.1) and
.deps (PyYAML). The CMU fonts (Computer Modern Unicode, OTF) are registered with
manimpango at runtime from assets/fonts/ -- no system install needed. Call
bootstrap() before importing manim or yaml.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_DEP_DIRS = (".deps_voiceover", ".deps")
_FONTS_REGISTERED = False


def bootstrap() -> None:
    for name in _DEP_DIRS:
        dep = REPO_ROOT / name
        if dep.exists() and str(dep) not in sys.path:
            sys.path.insert(0, str(dep))
    register_design_fonts()


def register_design_fonts() -> list[str]:
    """Register bundled design fonts with manimpango (process-local). Idempotent."""
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return []
    font_dir = REPO_ROOT / "video" / "pipeline" / "assets" / "fonts"
    registered: list[str] = []
    try:
        import manimpango
    except Exception:
        return registered
    for ttf in sorted([*font_dir.glob("*.ttf"), *font_dir.glob("*.otf")]):
        try:
            if manimpango.register_font(str(ttf)):
                registered.append(ttf.name)
        except Exception:
            pass
    _FONTS_REGISTERED = True
    return registered

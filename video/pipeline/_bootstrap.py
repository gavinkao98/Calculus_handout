"""Put vendored deps (manim, yaml) on sys.path and configure design fonts.

manim/yaml are not in .venv; they live under .deps_voiceover (manim 0.20.1) and
.deps (PyYAML). Call bootstrap() before importing manim or yaml.
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
    _set_tex_template()


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


def section_output_dir(meta: dict) -> Path:
    """Derive per-section output directory from storyboard meta.

    e.g. meta.section="1.3" → <REPO_ROOT>/video/output/ch01/s1.3
    """
    section = meta.get("section", "")
    ch_num = section.split(".")[0] if section else "00"
    return (
        REPO_ROOT / "video" / "output" / f"ch{int(ch_num):02d}" / f"s{section}"
    )


_TEX_TEMPLATE_SET = False


def _set_tex_template() -> None:
    """Set the global manim TeX template — Computer Modern math (Direction D).

    The redesign (Direction D) pairs Inter-Tight sans headings/prose with
    Computer Modern math (the KaTeX/CM look), for the modern science-explainer
    sans/serif contrast. So we DROP newtxtext/newtxmath (Times clones the earlier
    design used to match the LaTeX handout) and let manim's default template
    render math in CM. Only the inverse-trig operators are kept.
    """
    global _TEX_TEMPLATE_SET
    if _TEX_TEMPLATE_SET:
        return
    try:
        from manim import config, TexTemplate
    except Exception:
        return
    tpl = TexTemplate()
    tpl.add_to_preamble(
        # Inverse-trig operators the book preamble defines but manim's default
        # template lacks. \arcsin/\arccos/\arctan are LaTeX-kernel operators;
        # these three are not, so on-screen math using them failed to compile.
        r"\DeclareMathOperator{\arccsc}{arccsc}" "\n"
        r"\DeclareMathOperator{\arcsec}{arcsec}" "\n"
        r"\DeclareMathOperator{\arccot}{arccot}"
    )
    config.tex_template = tpl
    _TEX_TEMPLATE_SET = True

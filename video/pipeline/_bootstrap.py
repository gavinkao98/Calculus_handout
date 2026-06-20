"""Put vendored deps (manim, yaml) on sys.path and set the global TeX template.

manim/yaml are not in .venv; they live under .deps_voiceover (manim 0.20.1) and
.deps (PyYAML). Call bootstrap() before importing manim or yaml.

Fonts: the video uses Times New Roman / Courier New (Windows system fonts) + newtx
math (LaTeX) -- no fonts are vendored or registered. (The Direction D vendored design
fonts + register_design_fonts() were removed with the 2026-06-20 Times revert.)
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
    _set_tex_template()


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
    """Set the global manim TeX template — newtxtext + newtxmath (Times).

    Times-style math to match the Times New Roman Pango prose/headings (font revert
    from Direction D's Inter Tight + Computer Modern, 2026-06-20 per user request).
    newtxmath is the Times-compatible math font; the three inverse-trig operators the
    book preamble defines but manim's default template lacks are also declared.
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
        r"\usepackage{newtxtext}" "\n"
        r"\usepackage{newtxmath}" "\n"
        # Inverse-trig operators the book preamble defines but manim's default
        # template lacks. \arcsin/\arccos/\arctan are LaTeX-kernel operators;
        # these three are not, so on-screen math using them failed to compile.
        r"\DeclareMathOperator{\arccsc}{arccsc}" "\n"
        r"\DeclareMathOperator{\arcsec}{arcsec}" "\n"
        r"\DeclareMathOperator{\arccot}{arccot}"
    )
    config.tex_template = tpl
    _TEX_TEMPLATE_SET = True

"""Put vendored deps (manim, yaml) on sys.path and set the global TeX template.

manim/yaml are not in .venv; they live under .deps_voiceover (manim 0.20.1) and
.deps (PyYAML). Call bootstrap() before importing manim or yaml.

Type (Route A, 2026-06-24): all on-screen text AND math render through LaTeX
(pdflatex). Text = IBM Plex Sans (body/headings) + IBM Plex Mono (eyebrows/labels);
math = Latin Modern (`lmodern`). The fonts are set in the TeX preamble
(_set_tex_template); nothing is registered with Pango, because manim Text (Pango)
no longer carries the type -- Pango does not apply kerning ("AVAVAV" came out as the
sum of the glyph advances), LaTeX does. Exact `newcomputermodern` needs lualatex/
xelatex (fontspec), which breaks manim's `\\special{dvisvgm:raw}` math sub-part
addressing, so math stays on pdflatex-compatible `lmodern`. (Was NewComputerModern10
via Pango, the 2026-06-24 NCM spike; before that Times New Roman + newtx.)
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
    """Set the global manim TeX template — Plex Sans/Mono text + Latin Modern math.

    Route A (2026-06-24): on-screen TEXT moves off Pango onto LaTeX so it gets real
    kerning (manim Text/Pango does not kern -- "AVAVAV" rendered as the sum of the
    glyph advances). Text is IBM Plex Sans (`plex-sans`, made the default family via
    \\sfdefault) with IBM Plex Mono (`plex-mono`) for eyebrows/labels; math stays on
    Latin Modern (`lmodern`) -- pdflatex-compatible (exact `newcomputermodern` needs
    lualatex/xelatex, which breaks manim's `\\special{dvisvgm:raw}` math sub-part
    addressing). microtype adds kerning/protrusion. The three inverse-trig operators
    the book preamble defines but manim's default template lacks are also declared.
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
        r"\usepackage{lmodern}" "\n"          # math = Latin Modern (locked)
        r"\usepackage{plex-sans}" "\n"        # text = IBM Plex Sans
        r"\usepackage{plex-mono}" "\n"        # mono (eyebrow) = IBM Plex Mono
        r"\renewcommand{\familydefault}{\sfdefault}" "\n"   # body default -> Plex Sans
        r"\usepackage{microtype}" "\n"        # kerning / protrusion
        # Inverse-trig operators the book preamble defines but manim's default
        # template lacks. \arcsin/\arccos/\arctan are LaTeX-kernel operators;
        # these three are not, so on-screen math using them failed to compile.
        r"\DeclareMathOperator{\arccsc}{arccsc}" "\n"
        r"\DeclareMathOperator{\arcsec}{arcsec}" "\n"
        r"\DeclareMathOperator{\arccot}{arccot}"
    )
    config.tex_template = tpl
    _TEX_TEMPLATE_SET = True

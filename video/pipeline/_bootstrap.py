"""Put vendored deps (manim, yaml) on sys.path and set the global TeX template.

manim/yaml are not in .venv; they live under .deps_voiceover (manim 0.20.1) and
.deps (PyYAML). Call bootstrap() before importing manim or yaml.

Type (Route A, 2026-06-24): all on-screen text AND math render through LaTeX
(pdflatex). Text = IBM Plex Sans (body/headings) + IBM Plex Mono (eyebrows/labels);
math = Latin Modern (`lmodern`). The fonts are set in the TeX preamble
(apply_tex_template); nothing is registered with Pango, because manim Text (Pango)
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
    apply_tex_template()


def section_output_dir(meta: dict) -> Path:
    """Derive per-section output directory from storyboard meta.

    e.g. meta.section="1.3" → <REPO_ROOT>/video/output/ch01/s1.3
    """
    section = meta.get("section", "")
    ch_num = section.split(".")[0] if section else "00"
    return (
        REPO_ROOT / "video" / "output" / f"ch{int(ch_num):02d}" / f"s{section}"
    )


def apply_tex_template() -> None:
    """(Re)assign the global manim TeX template — Plex Sans/Mono text + Latin Modern math.

    Route A (2026-06-24): on-screen TEXT moves off Pango onto LaTeX so it gets real
    kerning (manim Text/Pango does not kern -- "AVAVAV" rendered as the sum of the
    glyph advances). Text is IBM Plex Sans (`plex-sans`, made the default family via
    \\sfdefault) with IBM Plex Mono (`plex-mono`) for eyebrows/labels; math stays on
    Latin Modern (`lmodern`) -- pdflatex-compatible (exact `newcomputermodern` needs
    lualatex/xelatex, which breaks manim's `\\special{dvisvgm:raw}` math sub-part
    addressing). microtype adds kerning/protrusion. The three inverse-trig operators
    the book preamble defines but manim's default template lacks are also declared.

    Must be (re)applied PER SCENE, not once: manim's ``tempconfig`` (make.py and
    scratch_frames both render as ``with tempconfig(cfg): LessonScene().render()`` in a
    per-scene loop) does NOT preserve ``config.tex_template`` across its save/restore --
    exiting ANY tempconfig block drops it back to manim's default (serif Computer Modern,
    no \\sfdefault, missing \\arccsc/\\arcsec/\\arccot). So without re-applying, only the
    FIRST scene of a batch would get this template and every later scene would build its
    Tex in the default serif. LessonScene.construct() calls this before building blocks,
    so each scene re-applies it. (Latent pre-Route-A: text was Pango and CM ~ Latin Modern,
    so the drop was invisible for text and harmless for §1.1 math; Route A made on-screen
    text depend on this template and exposed it.)
    """
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
        r"\everymath{\displaystyle}" "\n"     # all inline $..$ render display-style;
        #                                       \tfrac still overrides to text-style
        # Inverse-trig operators the book preamble defines but manim's default
        # template lacks. \arcsin/\arccos/\arctan are LaTeX-kernel operators;
        # these three are not, so on-screen math using them failed to compile.
        r"\DeclareMathOperator{\arccsc}{arccsc}" "\n"
        r"\DeclareMathOperator{\arcsec}{arcsec}" "\n"
        r"\DeclareMathOperator{\arccot}{arccot}"
    )
    config.tex_template = tpl

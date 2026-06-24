"""Put vendored deps (manim, yaml) on sys.path and set the global TeX template.

manim/yaml are not in .venv; they live under .deps_voiceover (manim 0.20.1) and
.deps (PyYAML). Call bootstrap() before importing manim or yaml.

Fonts (NCM, 2026-06-24): prose/headings use New Computer Modern (Pango family
"NewComputerModern10") to match the handout's 2026-06-22 NCM switch; math uses
Latin Modern (LaTeX `lmodern`), the pdflatex-compatible CM-family closest to NCM
(exact `newcomputermodern` needs lualatex/xelatex, which breaks manim's dvisvgm
sub-part addressing). The NCM10 OTFs are LOCATED via kpsewhich from the MiKTeX
`newcomputermodern` package (already required for math) and registered with Pango --
not vendored. Eyebrows/labels stay Courier New. (Was Times New Roman + newtx, the
2026-06-20 Times revert.)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_DEP_DIRS = (".deps_voiceover", ".deps")


def bootstrap() -> None:
    for name in _DEP_DIRS:
        dep = REPO_ROOT / name
        if dep.exists() and str(dep) not in sys.path:
            sys.path.insert(0, str(dep))
    _register_ncm_fonts()
    _set_tex_template()


_NCM_STYLES = ("Regular", "Bold", "Italic", "BoldItalic")


def _register_ncm_fonts() -> None:
    """Register the New Computer Modern text OTFs (family "NewComputerModern10") with
    Pango so manim Text (prose/headings) can use them.

    The OTFs ship with the `newcomputermodern` TeX package (which the math template now
    also needs), so we LOCATE them via kpsewhich rather than vendor a copy -- one
    dependency serves both the Pango text font and the LaTeX math font, and it stays
    machine-independent. No-op (text falls back) if kpsewhich / the package is absent;
    tools/doctor.py checks the family is visible to Pango."""
    try:
        import manimpango
    except Exception:
        return
    if "NewComputerModern10" in manimpango.list_fonts():
        return
    try:
        anchor = subprocess.run(["kpsewhich", "NewCM10-Regular.otf"],
                                capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception:
        anchor = ""
    if not anchor:
        return
    base = Path(anchor).parent
    for style in _NCM_STYLES:
        fp = base / f"NewCM10-{style}.otf"
        if fp.exists():
            try:
                manimpango.register_font(str(fp))
            except Exception:
                pass


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
    """Set the global manim TeX template — Latin Modern (`lmodern`), CM-family math.

    NCM switch (2026-06-24): the on-screen math moves off Times (newtx) to the Computer-
    Modern family to match the handout's New Computer Modern. Exact `newcomputermodern`
    needs lualatex/xelatex (fontspec), which breaks manim's `\\special{dvisvgm:raw}`
    sub-part addressing, so we use `lmodern` (Latin Modern) -- pdflatex-compatible and
    visually the closest CM-family to NCM (CM -> Latin Modern -> NCM lineage). The three
    inverse-trig operators the book preamble defines but manim's default template lacks
    are also declared.
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
        r"\usepackage{lmodern}" "\n"
        # Inverse-trig operators the book preamble defines but manim's default
        # template lacks. \arcsin/\arccos/\arctan are LaTeX-kernel operators;
        # these three are not, so on-screen math using them failed to compile.
        r"\DeclareMathOperator{\arccsc}{arccsc}" "\n"
        r"\DeclareMathOperator{\arcsec}{arcsec}" "\n"
        r"\DeclareMathOperator{\arccot}{arccot}"
    )
    config.tex_template = tpl
    _TEX_TEMPLATE_SET = True

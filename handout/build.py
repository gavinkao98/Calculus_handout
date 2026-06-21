#!/usr/bin/env python3
r"""build.py -- Assemble standalone HTML from shell + shared content fragments.

Content lives in fragments/ch{N}/ (one file per section, canonical = print version).
Each standalone HTML has <!-- BEGIN-CONTENT-FRAGMENTS --> / <!-- END-CONTENT-FRAGMENTS -->
markers; this script replaces that region with assembled <template> blocks.

Usage:
    python build.py              # rebuild all chapters
    python build.py ch01         # rebuild chapter 1 only
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRAG_DIR = HERE / "fragments"

MARKER_RE = re.compile(
    r"<!-- BEGIN-CONTENT-FRAGMENTS -->.*?<!-- END-CONTENT-FRAGMENTS -->",
    re.DOTALL,
)

# ── Screen transforms (disabled — screen variants removed) ───────
#
# def _dfrac_in_inline(html):
#     r"""Replace \frac{ with \dfrac{ inside inline math \(...\) only."""
#     def _replace(m):
#         return m.group().replace("\\frac{", "\\dfrac{")
#     return re.sub(r"\\\(.*?\\\)", _replace, html, flags=re.DOTALL)
#
# def _displaystyle_lim(html):
#     r"""Add \displaystyle before \lim_ inside inline math \(...\)."""
#     def _replace(m):
#         inner = m.group()
#         if "\\lim_" not in inner and "\\lim " not in inner:
#             return inner
#         inner = inner.replace("\\lim_", "\\displaystyle\\lim_")
#         inner = inner.replace("\\lim ", "\\displaystyle \\lim ")
#         return inner
#     return re.sub(r"\\\(.*?\\\)", _replace, html, flags=re.DOTALL)
#
# def _mathrm_to_text(html):
#     r"""Replace \mathrm{ with \text{ (safe for content fragments)."""
#     return html.replace("\\mathrm{", "\\text{")
#
# def to_screen(html):
#     """Apply all print → screen transforms."""
#     html = _dfrac_in_inline(html)
#     html = _displaystyle_lim(html)
#     html = _mathrm_to_text(html)
#     return html

# ── Chapter registry ─────────────────────────────────────────────

CHAPTERS = {
    "ch01": {
        "fragments": [
            "sec-intro", "sec-1-1", "sec-1-2", "sec-1-3",
            "sec-1-4", "sec-1-5", "sec-1-6",
        ],
        "target": "chapter1-print-standalone.html",
        # "screen": "chapter1-standalone.html",
    },
    "ch02": {
        "fragments": [
            "sec-2-1", "sec-2-2", "sec-2-3", "sec-2-4", "sec-2-5",
        ],
        "target": "chapter2-print-standalone.html",
        # "screen": "chapter2-standalone.html",
    },
    "ch03": {
        "fragments": [
            "sec-3-1", "sec-3-2", "sec-3-3",
        ],
        "target": "chapter3-print-standalone.html",
        # "screen": "chapter3-standalone.html",
    },
    "ch04": {
        "fragments": [
            "sec-4-1", "sec-4-2",
        ],
        "target": "chapter4-print-standalone.html",
        # "screen": "chapter4-standalone.html",
    },
}

# ── Build logic ──────────────────────────────────────────────────

def read_fragments(ch_id):
    """Read all fragment files for a chapter. Returns {frag_id: content}."""
    frag_dir = FRAG_DIR / ch_id
    cfg = CHAPTERS[ch_id]
    fragments = {}
    for fid in cfg["fragments"]:
        fpath = frag_dir / f"{fid}.html"
        if not fpath.exists():
            raise FileNotFoundError(f"Missing fragment: {fpath}")
        fragments[fid] = fpath.read_text(encoding="utf-8")
    return fragments

def assemble_templates(fragment_ids, fragments, transform=None):
    """Wrap fragments in <template> tags, optionally transforming content."""
    parts = []
    for fid in fragment_ids:
        content = fragments[fid]
        if transform:
            content = transform(content)
        parts.append(f'<template id="frag-{fid}">\n{content.rstrip()}\n</template>')
    return "\n\n".join(parts)

def patch_standalone(html_path, templates_block):
    """Replace the CONTENT-FRAGMENTS region in a standalone file."""
    html = html_path.read_text(encoding="utf-8")
    m = MARKER_RE.search(html)
    if not m:
        raise ValueError(f"No CONTENT-FRAGMENTS markers found in {html_path.name}")
    replacement = (
        "<!-- BEGIN-CONTENT-FRAGMENTS -->\n"
        + templates_block
        + "\n<!-- END-CONTENT-FRAGMENTS -->"
    )
    new_html = html[:m.start()] + replacement + html[m.end():]
    html_path.write_text(new_html, encoding="utf-8")
    return 1

def build_chapter(ch_id):
    """Build the print-standalone for a chapter."""
    cfg = CHAPTERS[ch_id]
    fragments = read_fragments(ch_id)
    frag_ids = cfg["fragments"]

    html_path = HERE / cfg["target"]
    templates = assemble_templates(frag_ids, fragments)
    patch_standalone(html_path, templates)
    print(f"  -> {html_path.name}")

    # Screen variant (disabled — standalone files removed)
    # if "screen" in cfg:
    #     screen_path = HERE / cfg["screen"]
    #     screen_templates = assemble_templates(frag_ids, fragments, to_screen)
    #     patch_standalone(screen_path, screen_templates)
    #     print(f"  -> {screen_path.name}")

def main():
    args = sys.argv[1:]
    ch_filter = args[0] if args else None

    chapters = [ch_filter] if ch_filter else list(CHAPTERS.keys())
    for ch_id in chapters:
        if ch_id not in CHAPTERS:
            print(f"Unknown chapter: {ch_id}")
            sys.exit(1)
        print(f"Building {ch_id}:")
        build_chapter(ch_id)
    print("Done.")

if __name__ == "__main__":
    main()

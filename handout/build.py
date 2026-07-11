#!/usr/bin/env python3
r"""build.py -- Assemble standalone HTML from shell + shared content fragments.

Content lives in fragments/ch{N}/ (one file per section, canonical = print version).
Each standalone HTML has <!-- BEGIN-CONTENT-FRAGMENTS --> / <!-- END-CONTENT-FRAGMENTS -->
markers; this script replaces that region with assembled <template> blocks.

The CHAPTERS registry below is the single source of truth for fragment order:
build_chapter() also rewrites each standalone's paginator `CHAPTER.fragments`
JS array from it, so the two lists can never drift out of sync (add/remove a
section or chapter by editing the registry alone, then rebuild).

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

# The paginator's `CHAPTER.fragments: [...]` array (lives in the trailing
# <script>, after the content region). Rewritten from the registry on build.
FRAGMENTS_JS_RE = re.compile(r"(fragments:\s*)\[[^\]]*\]")

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
            "sec-1-1", "sec-1-2", "sec-1-3",
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
            "sec-4-1", "sec-4-2", "sec-4-3", "sec-4-4", "sec-4-5",
        ],
        "target": "chapter4-print-standalone.html",
        # "screen": "chapter4-standalone.html",
    },
    "ch05": {
        # Fragments are appended as each section reaches draft (incremental build,
        # so a single finished section can be built + render-checked on its own).
        "fragments": [
            "sec-5-1", "sec-5-2", "sec-5-3", "sec-5-4", "sec-5-5", "sec-5-6", "sec-5-7", "sec-5-8", "sec-5-9",
        ],
        "target": "chapter5-print-standalone.html",
    },
    "ch06": {
        # Fragments appended as each section reaches draft (incremental build).
        "fragments": [
            "sec-6-1", "sec-6-2", "sec-6-3", "sec-6-4", "sec-6-5",
        ],
        "target": "chapter6-print-standalone.html",
    },
    "appA": {
        "fragments": [
            "sec-a-1", "sec-a-2", "sec-a-3", "sec-a-4", "sec-a-5", "sec-a-6",
        ],
        "target": "appendixA-print-standalone.html",
    },
    "appB": {
        "fragments": [
            "sec-b-1", "sec-b-2", "sec-b-3", "sec-b-4", "sec-b-5",
        ],
        "target": "appendixB-print-standalone.html",
    },
    "appC": {
        "fragments": [
            "sec-c-1", "sec-c-2", "sec-c-3", "sec-c-4",
        ],
        "target": "appendixC-print-standalone.html",
    },
    "appD": {
        "fragments": [
            "sec-d-1", "sec-d-2", "sec-d-3",
        ],
        "target": "appendixD-print-standalone.html",
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

def patch_standalone(html, templates_block):
    """Return `html` with the CONTENT-FRAGMENTS region replaced (pure transform)."""
    m = MARKER_RE.search(html)
    if not m:
        raise ValueError("No CONTENT-FRAGMENTS markers found")
    replacement = (
        "<!-- BEGIN-CONTENT-FRAGMENTS -->\n"
        + templates_block
        + "\n<!-- END-CONTENT-FRAGMENTS -->"
    )
    return html[:m.start()] + replacement + html[m.end():]

def sync_fragments_js(html, frag_ids):
    """Return `html` with the paginator `CHAPTER.fragments` array rebuilt from the
    registry, so it can never drift from build.py's fragment list (pure transform).

    Only the tail after END-CONTENT-FRAGMENTS is searched, so fragment prose can
    never be matched by accident; `count=1` relies on CHAPTER.fragments being the
    first (and only) `fragments:` token in that tail. The output format matches the
    existing one, so re-running on an already-synced file is a no-op.
    """
    m = MARKER_RE.search(html)
    split = m.end() if m else 0
    head, tail = html[:split], html[split:]
    arr = "[" + ", ".join(f'"{fid}"' for fid in frag_ids) + "]"
    new_tail, n = FRAGMENTS_JS_RE.subn(lambda mm: mm.group(1) + arr, tail, count=1)
    if n == 0:
        raise ValueError("No `CHAPTER.fragments` array found")
    return head + new_tail

def build_chapter(ch_id):
    """Build the print-standalone for a chapter."""
    cfg = CHAPTERS[ch_id]
    fragments = read_fragments(ch_id)
    frag_ids = cfg["fragments"]

    html_path = HERE / cfg["target"]
    templates = assemble_templates(frag_ids, fragments)
    # Apply both edits in memory, then write once: if either step raises, the
    # existing standalone is left untouched (atomic with respect to this build).
    html = html_path.read_text(encoding="utf-8")
    html = patch_standalone(html, templates)
    html = sync_fragments_js(html, frag_ids)
    html_path.write_text(html, encoding="utf-8")
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

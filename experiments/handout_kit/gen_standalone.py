#!/usr/bin/env python3
"""Generate standalone HTML files for chapters 1, 2 and 3.

Chapter 1's own standalone files serve as the chrome skeleton (page CSS, the
print paginator, the MathJax config); for ch1 the generation is a self-rebuild
that re-inlines the example-ch01/ fragments + figures.js and rewrites the config.
Chapters 2 and 3 reuse the same chrome.

Note: per-figure ``--fig-w`` overrides are NOT carried in the source fragments,
so on rebuild ch1 figures fall back to the print defaults (--fig-w-pair /
--fig-w-single). That is intended: the hlt pair defaults to 250px, the mapping
SVG carries its own inline width:340px, and every other figure renders at 100%.

Usage:  python gen_standalone.py
Output: chapter{1,2,3}-standalone.html, chapter{1,2,3}-print-standalone.html
"""
import re, pathlib

HERE = pathlib.Path(__file__).resolve().parent

# ── Chapter definitions ──────────────────────────────────────────────

CHAPTERS = {
    1: {
        "title_screen": "Chapter 1 — Inverse Functions and Limits",
        "title_print":  "Chapter 1 — Print build",
        "brand":        "Chapter 1",
        "running_head": "Chapter 1 · Inverse Functions and Limits",
        "dir":          "example-ch01",
        "fragments":    ["sec-intro", "sec-1-1", "sec-1-2", "sec-1-3",
                         "sec-1-4", "sec-1-5", "sec-1-6", "sec-summary"],
        "fig_css_vars": (
            ':root {\n'
            '  --fig-1-1:  250px;   /* Figure 1.1  horizontal line test (pair) */\n'
            '  --fig-1-2:  340px;   /* Figure 1.2  inverse mapping diagram */\n'
            '  --fig-1-3:  280px;   /* Figure 1.3  restricted x^2, sqrt x, y=x */\n'
            '  --fig-1-4:  100%;    /* Figure 1.4  sine not one-to-one */\n'
            '  --fig-1-5:  100%;    /* Figure 1.5  restricted sine */\n'
            '  --fig-1-6:  100%;    /* Figure 1.6  restricted cosine */\n'
            '  --fig-1-7:  100%;    /* Figure 1.7  restricted tangent */\n'
            '  --fig-1-8:  100%;    /* Figure 1.8  three functions, same limit (triple) */\n'
            '  --fig-1-9:  100%;    /* Figure 1.9  read-off-the-graph example */\n'
            '  --fig-1-10: 100%;    /* Figure 1.10 left/right limits differ */\n'
            '  --fig-1-11: 100%;    /* Figure 1.11 four one-sided infinite limits (grid) */\n'
            '  --fig-1-12: 100%;    /* Figure 1.12 vertical asymptote */\n'
            '  --fig-1-13: 100%;    /* Figure 1.13 epsilon-delta geometry */\n'
            '}'
        ),
    },
    2: {
        "title_screen": "Chapter 2 — Derivatives",
        "title_print":  "Chapter 2 — Print build",
        "brand":        "Chapter 2 — Derivatives",
        "running_head": "Chapter 2 · Derivatives",
        "dir":          "exp-ch02",
        "fragments":    ["sec-2-1", "sec-2-2", "sec-2-3", "sec-2-4", "sec-2-5"],
        "fig_css_vars": (
            ':root {\n'
            '  --fig-2-1:  100%;    /* Figure 2.1  Secant-to-tangent */\n'
            '  --fig-2-2:  100%;    /* Figure 2.2  f and f-prime */\n'
            '  --fig-2-3:  100%;    /* Figure 2.3  |x| corner */\n'
            '  --fig-2-4:  100%;    /* Figure 2.4  Product-rule rectangle (inline SVG) */\n'
            '}'
        ),
    },
    3: {
        "title_screen": "Chapter 3 — Chain Rule and Trigonometric Derivatives",
        "title_print":  "Chapter 3 — Print build",
        "brand":        "Chapter 3 — Chain Rule and Trigonometric Derivatives",
        "running_head": "Chapter 3 · Chain Rule and Trigonometric Derivatives",
        "dir":          "exp-ch03",
        "fragments":    ["sec-3-1", "sec-3-2", "sec-3-3"],
        "fig_css_vars": (
            ':root {\n'
            '  --fig-3-1:  100%;    /* Figure 3.1  Sector inequality */\n'
            '  --fig-3-2:  100%;    /* Figure 3.2  Composed mapping */\n'
            '}'
        ),
    },
}

# ── Helpers ──────────────────────────────────────────────────────────

def read(path):
    return (HERE / path).read_text(encoding="utf-8")

def write(path, content):
    (HERE / path).write_text(content, encoding="utf-8", newline="\n")
    print(f"  wrote {path}  ({len(content):,} chars, {content.count(chr(10))+1:,} lines)")

def build_templates(ch):
    """Read each section HTML and wrap it in a <template> tag."""
    parts = []
    for frag_id in ch["fragments"]:
        html = read(f'{ch["dir"]}/{frag_id}.html')
        parts.append(f'<template id="frag-{frag_id}">\n{html}</template>')
    return "\n\n".join(parts)

def read_figures_js(ch):
    """Read the chapter's figures.js content (the raw JS, no <script> tags)."""
    return read(f'{ch["dir"]}/figures.js')

# ── Template surgery ─────────────────────────────────────────────────

def replace_title(html, new_title):
    return re.sub(r'<title>[^<]*</title>', f'<title>{new_title}</title>', html, count=1)

def replace_templates(html, new_templates):
    """Replace all <template id="frag-*">...</template> blocks and the
    surrounding comments, replacing from the 'Section fragments' area
    through the last </template> before the plot.js comment."""
    first_tpl = html.find('<template id="frag-')
    if first_tpl < 0:
        raise RuntimeError("No <template> blocks found")
    last_tpl_end_idx = html.rfind('</template>')
    if last_tpl_end_idx < 0:
        raise RuntimeError("No </template> found")
    last_tpl_end = last_tpl_end_idx + len('</template>')
    comment_start = html.rfind('<!--', 0, first_tpl)
    if comment_start < 0:
        comment_start = first_tpl
    return (html[:comment_start]
            + "<!-- Section fragments (inlined) -->\n\n"
            + new_templates + "\n\n"
            + html[last_tpl_end:])

def replace_figures_js(html, new_figures_js, ch_num):
    """Replace the figures.js inlined block (between the figures.js comment
    and the closing </script> that follows hydrateFigures)."""
    m = re.search(r'<!-- [= \n]*figures\.js.*?-->\n', html, re.DOTALL)
    if not m:
        raise RuntimeError("Failed to locate figures.js comment")
    start = m.start()
    m2 = re.search(
        r'window\.hydrateFigures\s*=\s*hydrateFigures;\n\}\)\(\);\n</script>',
        html[start:]
    )
    if not m2:
        raise RuntimeError("Failed to locate end of figures.js block")
    end = start + m2.end()
    new_block = (
        f'<!-- ============================================================\n'
        f'     figures.js — inlined (Chapter {ch_num} figure registry)\n'
        f'     ============================================================ -->\n'
        f'<script>\n{new_figures_js}</script>'
    )
    return html[:start] + new_block + html[end:]

def replace_chapter_config_screen(html, ch):
    """Replace the CHAPTER const in the screen version."""
    frags_str = ", ".join(f'"{f}"' for f in ch["fragments"])
    new_config = (
        f'const CHAPTER = {{\n'
        f'  brand: "{ch["brand"]}",\n'
        f'  fragments: [{frags_str}],\n'
        f'}};'
    )
    pattern = r'const CHAPTER = \{[^}]*\};'
    result = re.sub(pattern, new_config, html, count=1)
    if result == html:
        raise RuntimeError("Failed to locate CHAPTER config (screen)")
    return result

def replace_chapter_config_print(html, ch):
    """Replace the CHAPTER var in the print version."""
    frags_str = ", ".join(f'"{f}"' for f in ch["fragments"])
    new_config = (
        f'var CHAPTER = {{\n'
        f'  brand: "{ch["brand"]}",\n'
        f'  runningHead: "{ch["running_head"]}",\n'
        f'  fragments: [{frags_str}],\n'
        f'}};'
    )
    pattern = r'var CHAPTER = \{[^}]*\};'
    result = re.sub(pattern, new_config, html, count=1)
    if result == html:
        raise RuntimeError("Failed to locate CHAPTER config (print)")
    return result

def replace_fig_css_vars(html, new_vars):
    """Replace the :root { --fig-* } block in the print version."""
    pattern = r':root \{\s*--fig-.*?\}'
    result = re.sub(pattern, new_vars, html, count=1, flags=re.DOTALL)
    if result == html:
        raise RuntimeError("Failed to locate figure CSS vars block")
    return result

def replace_fig_comment(html, ch_num):
    """Update the figure width comment block for the chapter."""
    pattern = r'(圖片寬度控制面板[^\n]*\n[^\n]*\n\s*═+\s*-->)'
    result = re.sub(pattern, r'\1', html, count=1)
    return result

# ── Main ─────────────────────────────────────────────────────────────

def generate_screen(ch_num, ch):
    print(f"\n── Chapter {ch_num} screen ──")
    html = read("chapter1-standalone.html")
    templates = build_templates(ch)
    figures_js = read_figures_js(ch)

    html = replace_title(html, ch["title_screen"])
    html = replace_templates(html, templates)
    html = replace_figures_js(html, figures_js, ch_num)
    html = replace_chapter_config_screen(html, ch)

    write(f"chapter{ch_num}-standalone.html", html)

def generate_print(ch_num, ch):
    print(f"\n── Chapter {ch_num} print ──")
    html = read("chapter1-print-standalone.html")
    templates = build_templates(ch)
    figures_js = read_figures_js(ch)

    html = replace_title(html, ch["title_print"])
    html = replace_fig_css_vars(html, ch["fig_css_vars"])
    html = replace_templates(html, templates)
    html = replace_figures_js(html, figures_js, ch_num)
    html = replace_chapter_config_print(html, ch)

    write(f"chapter{ch_num}-print-standalone.html", html)

if __name__ == "__main__":
    print("Generating standalone HTML files …")
    for ch_num, ch in CHAPTERS.items():
        generate_screen(ch_num, ch)
        generate_print(ch_num, ch)
    print("\nDone.")

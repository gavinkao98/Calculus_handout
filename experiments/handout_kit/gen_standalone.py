#!/usr/bin/env python3
"""Generate standalone HTML files for chapters 2 and 3,
modeled after chapter 1's standalone (screen) and print-standalone files.

Usage:  python gen_standalone.py
Output: chapter2-standalone.html, chapter2-print-standalone.html,
        chapter3-standalone.html, chapter3-print-standalone.html
"""
import re, pathlib

HERE = pathlib.Path(__file__).resolve().parent

# ── Chapter definitions ──────────────────────────────────────────────

CHAPTERS = {
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

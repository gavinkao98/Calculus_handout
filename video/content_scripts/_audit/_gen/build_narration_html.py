#!/usr/bin/env python3
"""Compile a §-level content script (.md) into a standalone narration review HTML.

Parses the `### unit: <id>` + fenced-block format defined in
CONTENT_METHODOLOGY.md §6 and emits a double-click-to-open HTML with MathJax
(inline `$...$` / display `$$...$$`). The narration is shown prominently per
unit; source / learning_goal / visual_need / animation_cue ride in a
collapsible <details>. Offline, zero-cost, reproducible.

Usage:
  python video/content_scripts/_audit/_gen/build_narration_html.py \
      video/content_scripts/ch03_trig_derivatives.md \
      video/content_scripts/ch03_trig_derivatives_narration.html
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

FIELD_KEYS = ("id", "source", "learning_goal", "kind",
              "narration", "visual_need", "animation_cue")
_FIELD_RE = re.compile(r"^(" + "|".join(FIELD_KEYS) + r"):\s?(.*)$")


def parse_block(block: str) -> dict[str, str]:
    """Parse one fenced field block (line scanner; tolerant of `: ` in values
    and `|` block scalars with 2-space continuation)."""
    fields: dict[str, str] = {}
    cur: str | None = None
    buf: list[str] = []
    block_scalar = False

    def flush() -> None:
        nonlocal cur, buf
        if cur is not None:
            text = "\n".join(buf) if block_scalar else " ".join(
                s.strip() for s in buf if s.strip())
            fields[cur] = text.strip("\n")
        buf = []

    for raw in block.splitlines():
        m = _FIELD_RE.match(raw)
        if m and not (block_scalar and raw.startswith("  ")):
            flush()
            cur, val = m.group(1), m.group(2)
            if val.strip() == "|":
                block_scalar = True
                buf = []
            else:
                block_scalar = False
                buf = [val]
        else:
            if cur is None:
                continue
            buf.append(raw[2:] if (block_scalar and raw.startswith("  ")) else raw)
    flush()
    return fields


def parse_meta(md: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    block = md.split("## meta", 1)[-1].split("\n---", 1)[0]
    for line in block.splitlines():
        m = re.match(r"^- `([^`]+)`(?:（[^）]*）)?:\s*(.+)$", line.strip())
        if m:
            meta[m.group(1)] = m.group(2).strip()
    return meta


def parse_units(md: str) -> list[dict[str, str]]:
    units: list[dict[str, str]] = []
    parts = md.split("### unit:")[1:]
    for part in parts:
        # stop at the closing-section "## " (e.g. "## §7 …") if it slipped in
        part = part.split("\n## ", 1)[0]
        fence = re.search(r"```(.*?)```", part, re.DOTALL)
        if not fence:
            continue
        units.append(parse_block(fence.group(1)))
    return units


_DETAIL_LABELS = {
    "source": "source",
    "learning_goal": "learning goal",
    "visual_need": "visual need",
    "animation_cue": "animation cue",
}


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def render_unit(i: int, u: dict[str, str]) -> str:
    uid = esc(u.get("id", "?"))
    kind = esc(u.get("kind", ""))
    narration = u.get("narration", "").strip()
    is_empty = narration.startswith("（無") or not narration
    narr_html = ("<p class=\"narr-none\">" + esc(narration) + "</p>") if is_empty \
        else "".join(f"<p>{esc(par)}</p>" for par in re.split(r"\n\s*\n", narration))
    details = []
    for key, label in _DETAIL_LABELS.items():
        val = u.get(key, "").strip()
        if val and not val.startswith("（無") and not val.startswith("（由"):
            details.append(
                f"<div class=\"d-row\"><span class=\"d-key\">{label}</span>"
                f"<span class=\"d-val\">{esc(val)}</span></div>")
        elif val:
            details.append(
                f"<div class=\"d-row d-na\"><span class=\"d-key\">{label}</span>"
                f"<span class=\"d-val\">{esc(val)}</span></div>")
    det_html = ("<details><summary>source · goal · visual · animation</summary>"
                + "".join(details) + "</details>") if details else ""
    return f"""<section class="unit">
  <div class="u-head"><span class="u-num">{i:02d}</span>
    <span class="u-id">{uid}</span><span class="u-kind">{kind}</span></div>
  <div class="u-narr">{narr_html}</div>
  {det_html}
</section>"""


HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — narration review</title>
<script>
window.MathJax = {{ tex: {{ inlineMath: [['$','$']], displayMath: [['$$','$$']] }},
  svg: {{ fontCache: 'global' }} }};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
<style>
:root {{ --ink:#1a2233; --muted:#5a6b85; --line:#dce3ee; --bg:#f6f8fc;
  --navy:#0a1322; --accent:#b0792a; --card:#fff; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink);
  font:16px/1.65 -apple-system,"Segoe UI",Roboto,"Noto Sans TC",sans-serif; }}
.wrap {{ max-width:820px; margin:0 auto; padding:40px 22px 80px; }}
header.top {{ background:var(--navy); color:#fff; border-radius:14px;
  padding:26px 28px; margin-bottom:14px; }}
header.top .eyebrow {{ font:600 12px/1 ui-monospace,monospace; letter-spacing:.14em;
  text-transform:uppercase; color:#8fb0e6; }}
header.top h1 {{ margin:.35em 0 .15em; font-size:26px; }}
header.top .tag {{ color:#c4d2ec; font-style:italic; }}
.meta-grid {{ display:flex; flex-wrap:wrap; gap:6px 18px; margin-top:14px;
  font-size:13px; color:#c4d2ec; }}
.note {{ font-size:13px; color:var(--muted); margin:0 2px 26px;
  padding:10px 14px; border-left:3px solid var(--accent); background:#fff8ec; border-radius:4px; }}
.unit {{ background:var(--card); border:1px solid var(--line); border-radius:12px;
  padding:18px 22px; margin:0 0 14px; }}
.u-head {{ display:flex; align-items:baseline; gap:10px; margin-bottom:8px; }}
.u-num {{ font:700 13px/1 ui-monospace,monospace; color:#fff; background:var(--navy);
  border-radius:6px; padding:4px 7px; }}
.u-id {{ font:600 15px/1.2 ui-monospace,monospace; color:var(--ink); }}
.u-kind {{ margin-left:auto; font:600 11px/1 ui-monospace,monospace; letter-spacing:.08em;
  text-transform:uppercase; color:var(--accent); border:1px solid #e7d3ad;
  background:#fdf6e8; border-radius:20px; padding:4px 10px; }}
.u-narr p {{ margin:.5em 0; }}
.narr-none {{ color:var(--muted); font-style:italic; }}
details {{ margin-top:12px; border-top:1px dashed var(--line); padding-top:10px; }}
summary {{ cursor:pointer; font:600 12px/1.4 ui-monospace,monospace; color:var(--muted);
  letter-spacing:.04em; }}
.d-row {{ display:flex; gap:12px; margin:8px 0; font-size:14px; }}
.d-key {{ flex:0 0 96px; color:var(--accent); font:600 12px/1.5 ui-monospace,monospace;
  text-transform:uppercase; letter-spacing:.04em; }}
.d-val {{ color:#33415c; white-space:pre-wrap; }}
.d-na .d-val {{ color:var(--muted); font-style:italic; }}
</style></head><body><div class="wrap">"""

FOOT = """</div></body></html>"""


def main() -> int:
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    md = src.read_text(encoding="utf-8")
    meta = parse_meta(md)
    units = parse_units(md)

    title = f"§{meta.get('section','?')} {meta.get('title','')}".strip()
    meta_bits = "".join(
        f"<span>{esc(k)}: {esc(meta[k])}</span>"
        for k in ("chapter", "chapter_title", "section", "id") if k in meta)
    head = HEAD.format(title=esc(title))
    top = f"""<header class="top">
  <div class="eyebrow">{esc(meta.get('chapter',''))} · Narration review (DRAFT)</div>
  <h1>§{esc(meta.get('section',''))} {esc(meta.get('title',''))}</h1>
  <div class="tag">{esc(meta.get('tagline',''))}</div>
  <div class="meta-grid">{meta_bits}</div>
</header>
<div class="note">純內容中間產物（source of truth＝.md）。本頁逐單元呈現旁白供 sign-off；
math 由 MathJax 即時渲染。intro／outro 為純動畫無 narration。</div>"""
    body = "\n".join(render_unit(i, u) for i, u in enumerate(units))
    out.write_text(head + top + body + FOOT, encoding="utf-8")
    print(f"[ok] {len(units)} units -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

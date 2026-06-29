"""narration_review.py -- compile a content script (.md) into a standalone
narration-review HTML (MathJax CDN, double-click to open, math renders live).

Why this exists: CONTENT_METHODOLOGY.md §6 "交付形式" requires every content
script to ship alongside a `<deck>_narration.html` review copy; the `.md` inline
LaTeX is hard to read, the rendered HTML is what the user signs off on. §3.1
built this HTML by hand; this generator makes §3.2/§3.3 (and re-builds after each
audit) deterministic and drift-proof.

The parser below MIRRORS the canonical `review_pack.parse_content_script`
contract (CONTENT_METHODOLOGY.md §6 "parser 契約"): `### unit: <id>` header +
a fenced ``` block of `field: value` lines, `field: |` block scalars whose
continuation lines are 2-space indented; the unit region ends at the first `## `
h2. It is re-implemented (not imported) only to stay dependency-free -- importing
review_pack would trigger its module-level manim/TeX bootstrap. Keep in sync.

Run (offline, no key, no deps beyond stdlib):
    python video/pipeline/narration_review.py video/content_scripts/<deck>.md
    python video/pipeline/narration_review.py <deck>.md -o <out>.html
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

_UNIT_HEADER = re.compile(r"^###\s+unit:\s+(\S+)")
_SECTION = re.compile(r"^##\s")
_FENCE = re.compile(r"^```")
_FIELD = re.compile(r"^([A-Za-z_]+):\s?(.*)$")
_FIELD_KEYS = ("id", "source", "learning_goal", "kind", "narration",
               "visual_need", "animation_cue")
# meta bullet:  - `key`（可有括號說明）: value
_META = re.compile(r"^-\s*`(\w+)`[^:：]*[:：]\s*(.+?)\s*$")
# a value that is ENTIRELY one parenthetical note is a "not applicable" placeholder
_PLACEHOLDER = re.compile(r"^（[^（）]*）$")


def parse_content_script(md_path: Path) -> dict:
    """Returns {meta:{...}, units:[{id, source, learning_goal, kind, narration,
    visual_need, animation_cue}]}. Mirrors review_pack.parse_content_script."""
    lines = md_path.read_text(encoding="utf-8").splitlines()

    header_lines: list[str] = []
    for ln in lines:
        if _UNIT_HEADER.match(ln):
            break
        header_lines.append(ln)

    meta: dict[str, str] = {}
    for ln in header_lines:
        m = _META.match(ln)
        if m:
            meta[m.group(1)] = m.group(2)

    units: list[dict] = []
    cur: dict | None = None
    in_fence = False
    scalar: str | None = None

    def _commit() -> None:
        if cur is not None:
            for k, v in list(cur.items()):
                if isinstance(v, list):
                    cur[k] = " ".join(s.strip() for s in v).strip()

    for ln in lines:
        m = _UNIT_HEADER.match(ln)
        if m:
            _commit()
            if cur is not None:
                units.append(cur)
            cur = {k: "" for k in _FIELD_KEYS}
            cur["id"] = m.group(1)
            in_fence = False
            scalar = None
            continue
        if cur is None:
            continue
        if _SECTION.match(ln):
            _commit()
            units.append(cur)
            cur = None
            continue
        if _FENCE.match(ln):
            in_fence = not in_fence
            scalar = None
            continue
        if not in_fence:
            continue
        if scalar is not None:
            if not ln.strip() or ln.startswith("  "):
                cur[scalar].append(ln)
                continue
            scalar = None
        mf = _FIELD.match(ln)
        if mf:
            key, val = mf.group(1).lower(), mf.group(2).strip()
            if key not in cur:
                continue
            if val == "|":
                cur[key] = []
                scalar = key
            else:
                cur[key] = val
    _commit()
    if cur is not None:
        units.append(cur)

    # normalise "not applicable" placeholders to empty (whole-string paren only)
    for u in units:
        for k in ("narration", "visual_need", "animation_cue", "learning_goal"):
            vs = u.get(k, "").strip()
            if not vs or _PLACEHOLDER.match(vs) or vs.startswith("—") or vs == "-":
                u[k] = ""
    return {"meta": meta, "units": units}


# ---- HTML emit ----------------------------------------------------------

_HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_esc} — narration review</title>
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
</style></head><body><div class="wrap"><header class="top">
  <div class="eyebrow">{chapter_esc} · Narration review (DRAFT)</div>
  <h1>§{section_esc} {title_esc}</h1>
  <div class="tag">{tagline_esc}</div>
  <div class="meta-grid">{meta_spans}</div>
</header>
<div class="note">純內容中間產物（source of truth＝.md）。本頁逐單元呈現旁白供 sign-off；
math 由 MathJax 即時渲染。intro／outro 為純動畫無 narration。</div>
"""

_DETAIL_LABELS = [
    ("source", "source"),
    ("learning_goal", "learning goal"),
    ("visual_need", "visual need"),
    ("animation_cue", "animation cue"),
]


def _esc(s: str) -> str:
    # escape for HTML; MathJax tex-svg reads &lt; &gt; &amp; correctly inside $...$
    return html.escape(s, quote=False)


def render_html(parsed: dict) -> str:
    meta = parsed["meta"]
    title = meta.get("title", "")
    section = meta.get("section", "")
    chapter = meta.get("chapter", "Chapter")
    tagline = meta.get("tagline", "")

    span_keys = [("chapter", "chapter"), ("chapter_title", "chapter_title"),
                 ("section", "section"), ("id", "id")]
    meta_spans = "".join(
        f"<span>{k}: {_esc(meta[mk])}</span>" for mk, k in span_keys if meta.get(mk)
    )

    out = [_HEAD.format(
        title_esc=_esc(title), section_esc=_esc(section),
        chapter_esc=_esc(chapter), tagline_esc=_esc(tagline),
        meta_spans=meta_spans,
    )]

    for i, u in enumerate(parsed["units"]):
        num = f"{i:02d}"
        kind = u.get("kind", "")
        narr = u.get("narration", "").strip()
        if narr:
            narr_html = f'<div class="u-narr"><p>{_esc(narr)}</p></div>'
        else:
            narr_html = ('<div class="u-narr"><p class="narr-none">'
                         '（無——純動畫，無 narration）</p></div>')
        rows = []
        for key, label in _DETAIL_LABELS:
            val = u.get(key, "").strip()
            na = "" if val else " d-na"
            disp = _esc(val) if val else "（無）"
            rows.append(f'<div class="d-row{na}"><span class="d-key">{label}</span>'
                        f'<span class="d-val">{disp}</span></div>')
        out.append(
            '<section class="unit">\n'
            f'  <div class="u-head"><span class="u-num">{num}</span>\n'
            f'    <span class="u-id">{_esc(u["id"])}</span>'
            f'<span class="u-kind">{_esc(kind)}</span></div>\n'
            f'  {narr_html}\n'
            f'  <details><summary>source · goal · visual · animation</summary>'
            + "".join(rows) +
            '</details>\n'
            '</section>'
        )
    out.append("\n</div></body></html>\n")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Compile a content-script .md into a narration-review HTML.")
    ap.add_argument("md", type=Path, help="path to content_scripts/<deck>.md")
    ap.add_argument("-o", "--out", type=Path, default=None,
                    help="output HTML path (default: <deck>_narration.html beside the .md)")
    args = ap.parse_args()

    md_path = args.md.resolve()
    parsed = parse_content_script(md_path)
    out_path = args.out or md_path.with_name(md_path.stem + "_narration.html")
    out_path.write_text(render_html(parsed), encoding="utf-8")
    n_narr = sum(1 for u in parsed["units"] if u.get("narration", "").strip())
    print(f"wrote {out_path}  ({len(parsed['units'])} units, {n_narr} with narration)")


if __name__ == "__main__":
    main()

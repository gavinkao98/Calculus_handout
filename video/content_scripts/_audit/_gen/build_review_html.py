#!/usr/bin/env python3
"""Build the §3.1 mock-milestone REVIEW report (standalone HTML).

Embeds every rendered final frame (base64) beside its scene's narration and the
gate-1 visual-audit note, plus the pipeline gate verdicts. Offline, reproducible.

  python video/content_scripts/_audit/_gen/build_review_html.py
"""
from __future__ import annotations

import base64
import html
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
SB = ROOT / "video/storyboards/ch03_trig_derivatives.yml"
FRAMES = ROOT / "video/output/_qa/ch03-frames"
AUDIT = ROOT / "video/content_scripts/_audit/_gen/ch03-visual-audit.json"
OUT = ROOT / "video/content_scripts/_audit/REVIEW-ch03_trig_derivatives-applied.html"

import json

HOOKS = {"sector_inequality", "slope_equals_height", "shm_stacked_graphs"}


def esc(s: str) -> str:
    return html.escape(s or "", quote=False)


def img_tag(sid: str) -> str:
    p = FRAMES / f"{sid}.png"
    if not p.exists():
        return '<div class="noframe">（no frame — intro/outro/divider, template-standard）</div>'
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return f'<img loading="lazy" alt="{esc(sid)}" src="data:image/png;base64,{b64}">'


def main() -> int:
    data = yaml.safe_load(SB.read_text(encoding="utf-8"))
    meta = data["meta"]
    scenes = data["scenes"]
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    notes = audit["notes"]

    cards = []
    n_content = 0
    for i, sc in enumerate(scenes):
        sid = sc["id"]
        kind = sc.get("kind", "content")
        tmpl = sc.get("template", "")
        title = sc.get("title", "")
        say = (sc.get("say") or "").strip()
        is_hook = sid in HOOKS
        if kind == "content":
            n_content += 1
        badge = tmpl or kind
        hook_tag = '<span class="hook">⚙️ custom hook</span>' if is_hook else ""
        note = notes.get(sid, "")
        say_html = ""
        if say:
            # strip {show ...} reveal markers for reading; keep $math$ for MathJax
            reading = re.sub(r"\{show [^}]+\}", "", say)
            reading = re.sub(r"[ \t]+", " ", reading).strip()
            say_html = f'<div class="say">{esc(reading)}</div>'
        note_html = f'<div class="note">{esc(note)}</div>' if note else ""
        cards.append(f"""<section class="card">
  <div class="chead"><span class="cnum">{i:02d}</span>
    <span class="cid">{esc(sid)}</span>
    <span class="badge">{esc(badge)}</span>{hook_tag}
    <span class="ctitle">{esc(title)}</span></div>
  <div class="frame">{img_tag(sid)}</div>
  {say_html}
  {note_html}
</section>""")

    adv_rows = "".join(
        f'<li><b>{esc(a["scene"])}</b> <span class="dim">[{esc(a["dim"])}]</span> '
        f'{esc(a["issue"])} — <i>{esc(a["disposition"])}</i></li>'
        for a in audit["advisories"])

    body = "\n".join(cards)
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>§3.1 Derivatives of Sine and Cosine — mock-milestone review</title>
<script>window.MathJax={{tex:{{inlineMath:[['$','$']],displayMath:[['$$','$$']]}},svg:{{fontCache:'global'}}}};</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
<style>
:root{{--ink:#1a2233;--mut:#5a6b85;--line:#dce3ee;--bg:#eef2f8;--navy:#0a1322;--amber:#b0792a;--card:#fff;--ok:#2f7d4f;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,"Segoe UI",Roboto,"Noto Sans TC",sans-serif}}
.wrap{{max-width:1080px;margin:0 auto;padding:36px 20px 90px}}
header.top{{background:var(--navy);color:#fff;border-radius:14px;padding:28px 30px;margin-bottom:16px}}
header.top .eye{{font:600 12px/1 ui-monospace,monospace;letter-spacing:.16em;text-transform:uppercase;color:#8fb0e6}}
header.top h1{{margin:.3em 0 .15em;font-size:27px}}
header.top .sub{{color:#c4d2ec}}
.gates{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin-bottom:14px}}
.gates h2{{margin:0 0 10px;font-size:15px;letter-spacing:.02em}}
.gates ul{{margin:6px 0 0;padding-left:20px}}
.gates li{{margin:5px 0}}
.ok{{color:var(--ok);font-weight:700}}
.dim{{color:var(--mut);font:600 12px ui-monospace,monospace}}
.adv{{background:#fff8ec;border-left:3px solid var(--amber);border-radius:6px;padding:10px 16px;margin-top:10px}}
.adv li{{margin:5px 0;font-size:14px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:0 0 16px}}
.chead{{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-bottom:10px}}
.cnum{{font:700 13px ui-monospace,monospace;color:#fff;background:var(--navy);border-radius:6px;padding:4px 7px}}
.cid{{font:600 15px ui-monospace,monospace}}
.badge{{font:600 11px ui-monospace,monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);border:1px solid var(--line);border-radius:20px;padding:3px 9px}}
.hook{{font:600 11px ui-monospace,monospace;color:var(--amber);border:1px solid #e7d3ad;background:#fdf6e8;border-radius:20px;padding:3px 9px}}
.ctitle{{margin-left:auto;color:var(--mut);font-style:italic}}
.frame img{{width:100%;border-radius:8px;border:1px solid var(--line);display:block}}
.noframe{{color:var(--mut);font-style:italic;padding:18px;text-align:center;background:#f6f8fc;border-radius:8px}}
.say{{margin-top:11px;padding:11px 14px;background:#f6f8fc;border-radius:8px;font-size:15px}}
.note{{margin-top:8px;font-size:13px;color:var(--mut)}}
.note::before{{content:"視覺稽核：";color:var(--ok);font-weight:700}}
</style></head><body><div class="wrap">
<header class="top">
  <div class="eye">{esc(meta['chapter'])} · §{esc(meta['section'])} · mock-milestone review</div>
  <h1>{esc(meta['title'])}</h1>
  <div class="sub">{n_content} 教學單元 + intro / 4 divider / outro = {len(scenes)} 場景 · Route A（Plex+LaTeX）· 1080p mock · 旁白已 sign-off（LOCKED）</div>
</header>

<div class="gates">
  <h2>閘序裁決（全免費；TTS 與外部 gate-2 延後、需另徵同意）</h2>
  <ul>
    <li><b>Stage 1 內容</b> — 六鏡對抗稽核 <span class="ok">raw 0 / blocking 0 / advisory 0</span>（L5 數學盲算重算 11 組全 match）；散文 copyedit 採納 6 條純措辭緊縮；<b>使用者旁白 sign-off → LOCKED</b>。</li>
    <li><b>Stage 2 工程</b> — schema / lint / sizecheck <span class="ok">0 error</span>；視覺幀稽核（19 content 場）<span class="ok">blocking 1 → 0</span>（1 blocking 已修＋複核）＋ 3 advisory（cosmetic）。</li>
    <li><b>模板增強</b> — <code>theorem_proof</code> 加 optional <code>label</code>（Prop 3.1/3.2 正確標 <code>[ PROPOSITION ]</code>，不誤標 Theorem）。</li>
    <li><b>3 客製 hook</b> — Fig 3.1 單位圓三面積 / Fig 3.3 切線=高度 / Fig 3.4 SHM 三層堆疊；生成→render→目視修兩處（sector 標籤碰撞、SHM 曲線定位）→ 全部視覺 clean。</li>
  </ul>
  <div class="adv"><b>殘留 advisory（3，cosmetic，mock 里程碑保留記錄）：</b>
    <ul>{adv_rows}</ul>
  </div>
</div>

{body}
</div></body></html>"""
    OUT.write_text(page, encoding="utf-8")
    size_mb = OUT.stat().st_size / 1e6
    print(f"[ok] {len(scenes)} scenes -> {OUT}  ({size_mb:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

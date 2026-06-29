#!/usr/bin/env python3
"""Build the §3.2 Chain Rule Stage-2 REVIEW report (standalone HTML).

Mirrors build_review_html.py (the §3.1 mock-milestone report): embeds every
rendered final frame (base64) beside its scene's narration and the gate-1
visual-frame-audit note, plus the pipeline gate verdicts. Offline, reproducible.

Frames are the SAME fresh frames the gate-1 audit read, taken from the critic
extraction tree (output/ch03/s3.2/critic/frames/<NN>_<id>/final.png) so the
report shows exactly what was judged.

  python video/content_scripts/_audit/_gen/build_s32_review_html.py
"""
from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
SB = ROOT / "video/storyboards/ch03_chain_rule.yml"
FRAMES = ROOT / "video/output/ch03/s3.2/critic/frames"
AUDIT = ROOT / "video/content_scripts/_audit/_gen/ch03-s32-stage2-audit.json"
OUT = ROOT / "video/content_scripts/_audit/REVIEW-ch03_chain_rule-stage2-applied.html"

HOOKS = {"composed_mapping_figure", "remainder_tangent_figure"}


def esc(s: str) -> str:
    return html.escape(s or "", quote=False)


def frame_for(sid: str) -> Path | None:
    """The critic frame for a content scene lives at <NN>_<id>/final.png; glob the
    number prefix instead of hardcoding scene order."""
    matches = list(FRAMES.glob(f"*_{sid}/final.png"))
    return matches[0] if matches else None


def img_tag(sid: str) -> str:
    p = frame_for(sid)
    if p is None or not p.exists():
        return ('<div class="noframe">（no frame — intro / divider / outro, '
                'silent brand template）</div>')
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return f'<img loading="lazy" alt="{esc(sid)}" src="data:image/png;base64,{b64}">'


def score_chip(scores: dict | None) -> str:
    if not scores:
        return ""
    order = [("A1", "a1"), ("A2", "a2"), ("A3", "a3"), ("A4", "a4"),
             ("A5", "a5"), ("A6", "a6"), ("A7", "a7")]
    cells = "".join(
        f'<span class="sc"><b>{lab}</b> {scores.get(key, "?")}</span>'
        for lab, key in order)
    return f'<div class="scores">{cells}</div>'


def main() -> int:
    data = yaml.safe_load(SB.read_text(encoding="utf-8"))
    meta = data["meta"]
    scenes = data["scenes"]
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    notes = audit.get("notes", {})
    scores = audit.get("scores", {})
    summary = audit.get("summary", {})

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
  {score_chip(scores.get(sid))}
  {say_html}
  {note_html}
</section>""")

    adv_rows = "".join(
        f'<li><b>{esc(a["scene"])}</b> <span class="dim">[{esc(a["dim"])}]</span> '
        f'{esc(a["issue"])} — <i>{esc(a["disposition"])}</i></li>'
        for a in audit.get("advisories", []))
    adv_block = (f'<div class="adv"><b>殘留 advisory（{len(audit.get("advisories", []))}，'
                 f'cosmetic／house-style，記錄不追）：</b><ul>{adv_rows}</ul></div>'
                 if audit.get("advisories") else "")

    refuted = audit.get("raised_then_refuted", [])
    refuted_html = ""
    if refuted:
        rows = "".join(
            f'<li><b>{esc(r["scene"])}</b> <span class="dim">[{esc(r.get("dim",""))}]</span> '
            f'{esc(r.get("issue",""))} — <i>raised then refuted ({esc(str(r.get("refuted_count","")))} /3 votes)</i></li>'
            for r in refuted)
        refuted_html = (f'<div class="adv refu"><b>raised → refuted（對抗複驗駁回，'
                        f'{len(refuted)}）：</b><ul>{rows}</ul></div>')

    blk = summary.get("confirmed_blocking", 0)
    blk_class = "ok" if blk == 0 else "bad"

    body = "\n".join(cards)
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>§3.2 The Chain Rule — Stage 2 engineering review</title>
<script>window.MathJax={{tex:{{inlineMath:[['$','$']],displayMath:[['$$','$$']]}},svg:{{fontCache:'global'}}}};</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
<style>
:root{{--ink:#1a2233;--mut:#5a6b85;--line:#dce3ee;--bg:#eef2f8;--navy:#0a1322;--amber:#b0792a;--card:#fff;--ok:#2f7d4f;--bad:#c0392b;}}
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
.bad{{color:var(--bad);font-weight:700}}
.dim{{color:var(--mut);font:600 12px ui-monospace,monospace}}
.adv{{background:#fff8ec;border-left:3px solid var(--amber);border-radius:6px;padding:10px 16px;margin-top:10px}}
.adv.refu{{background:#eef6f0;border-left-color:var(--ok)}}
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
.scores{{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}}
.scores .sc{{font:600 12px ui-monospace,monospace;color:var(--mut);background:#f1f5fb;border:1px solid var(--line);border-radius:6px;padding:3px 8px}}
.scores .sc b{{color:var(--ink)}}
.say{{margin-top:11px;padding:11px 14px;background:#f6f8fc;border-radius:8px;font-size:15px}}
.note{{margin-top:8px;font-size:13px;color:var(--mut)}}
.note::before{{content:"視覺稽核：";color:var(--ok);font-weight:700}}
</style></head><body><div class="wrap">
<header class="top">
  <div class="eye">{esc(meta['chapter'])} · §{esc(meta['section'])} · Stage 2 engineering review</div>
  <h1>{esc(meta['title'])}</h1>
  <div class="sub">{n_content} 教學單元 + intro / 3 divider / outro = {len(scenes)} 場景 · Route A（Plex+LaTeX）· 1080p mock · 內容稿已 sign-off（LOCKED）</div>
</header>

<div class="gates">
  <h2>Stage 2 閘序裁決（全免費；TTS 與外部 gate-2 延後、需另徵同意）</h2>
  <ul>
    <li><b>乾淨重渲</b> — schema OK / lint clean / sizecheck <span class="ok">consistent（0 error）</span>；27 場 compose → <code>output/ch03/s3.2/ch03_chain_rule.mp4</code>（exit 0）。3 個 within-frame advisory（proof_setup/easy/delicate_choices 的 <code>qed</code> 越安全邊界 ~0.15u、仍在框內可見）＝比照 §3.1 接受、記錄。</li>
    <li><b>視覺幀稽核（gate-1，{summary.get("scenes_audited","?")} content 場並行 refute-by-default，V1–V9 + A1–A7）</b> — confirmed visual blocking <span class="{blk_class}">{blk}</span>{("（" + str(summary.get("raised_then_refuted_count",0)) + " 個 raised→對抗複驗駁回）") if summary.get("raised_then_refuted_count") else ""}。</li>
    <li><b>2 客製 hook</b> — Fig 3.5 composed_mapping（三軸兩段伸縮、真實相對寬度可見相乘）／ Fig 3.6 remainder_tangent（R(h) vs R(h/2)≈¼）；生成→render→目視，本輪重渲後視覺 clean，<b>待使用者 sign-off</b>（CONTENT_METHODOLOGY §5）。</li>
    <li><b>修正回歸</b> — 上輪 3 個視覺修正（example_chain_times_quotient V4 (x&gt;1) garble／example_nested_three_layers step reason 純文字化／remainder_tangent R(h/2) 標籤上移）本輪 fresh 重渲後重審，確認未復發。</li>
  </ul>
  {refuted_html}
  {adv_block}
</div>

{body}
</div></body></html>"""
    OUT.write_text(page, encoding="utf-8")
    size_mb = OUT.stat().st_size / 1e6
    print(f"[ok] {len(scenes)} scenes -> {OUT}  ({size_mb:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

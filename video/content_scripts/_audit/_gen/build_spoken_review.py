#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Standalone HTML review of a section's MiMo spoken-narration round.

Emits a double-click-to-open, MathJax-rendered report that puts each content
scene's approved storyboard ``say:`` (math rendered) next to the derived spoken
form (what MiMo actually reads), plus the round's NFA gate results and the house
audio decision. Satisfies CLAUDE.md "每完成一輪撰寫後也要產 HTML 報告".

Reusable across sections (the MiMo route is the standard TTS path): reads the
canonical storyboard + the spoken single source, so re-running after any
``.spoken.yml`` edit + ``derive_spoken.py`` keeps the report in sync. Per-deck
gate/status text lives in STATUS below (add an entry when running a new deck).

Usage:  python video/content_scripts/_audit/_gen/build_spoken_review.py ch03_trig_derivatives
Output: video/content_scripts/_audit/REVIEW-<deck>-mimo-spoken-applied.html
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))   # video/ (holds pipeline/)
from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()
import yaml  # noqa: E402

REPO = _bootstrap.REPO_ROOT
STORY = REPO / "video" / "storyboards"
CONTENT = REPO / "video" / "content_scripts"
OUT = REPO / "video" / "content_scripts" / "_audit"

_SHOW = re.compile(r"\{show\s+[^}]+\}")

# Per-deck round status (pills + gate cards + house audio). Add an entry per deck.
STATUS: dict[str, dict] = {
    "ch03_trig_derivatives": {
        "section": "3.1",
        "title": "Derivatives of Sine and Cosine",
        "date": "2026-07-02",
        "approved": "yes (LOCKED)",
        "pills": [
            ("ok", "MiMo spoken 就緒"),
            ("ok", "NFA 收斂 · 0 blocking"),
            ("ok", "House audio · Candidate B"),
        ],
        "gates": [
            ("NFA gate-1 (Claude, free)",
             "首輪 <b>0 blocking, 3 advisory</b>（3 條皆非 MiMo 雙版忠實破口："
             "Version A HTML/`.md` 反映較舊較長 narration 的既有 doc-sync 落差 ×2，"
             "＋ u9 念起來稍密但忠實 ×1）。"),
            ("NFA gate-2 (Codex gpt-5.5/xhigh, read-only)",
             "抓到 gate-1 漏掉的 <b>1 blocking [D3]</b>：<code>x+h/2</code> 原念成"
             "「the quantity x plus h over two」會被聽成 <code>(x+h)/2</code>。"
             "修為「the quantity x plus one half h」（3 場 4 處）。"),
            ("回歸複查 (Claude gate-1, scoped)",
             "只複查 3 個修改場 → <b>VERDICT 0 blocking, 0 advisory</b>："
             "「D3 fix confirmed clean, 0 new issue」，數學等價、無新歧義、D2 仍逐字忠實。"),
        ],
        "house_audio": [
            ("整套 house style", "Candidate B（溫暖低調）"),
            ("intro / outro", "candidate_b_intro_bed.wav / candidate_b_outro_bed.wav（一律使用）"),
            ("divider ×4", "candidate_b_divider_stinger.wav（gain 0.6，「音量淡」）"),
            ("caution ping", "不加（§3.1 兩個 caution 皆非 notation trap）"),
            ("content 模板", "全乾聲（narration-first）"),
        ],
        "render": "✅ <code>output/ch03/s3.1/ch03_trig_derivatives_mimo.mp4</code>"
                  "（1080p · 17.75 min · 36 MB · h264+aac 48k stereo）。compose 路由正確："
                  "21 content 場=真 MiMo 旁白、intro/4 divider/outro=Candidate B cue；音訊分層："
                  "intro bed mean −27 dB（軟底）vs 旁白 mean −23 dB/max −3 dB（narration-first）；"
                  "4 幀跨模板抽查 LaTeX 無亂碼；sync beat timing clean（4 條 within-frame length "
                  "advisory，旁白未超框）。全 5 pre-render gate 綠（含修好的 provenance _mimo 解析）。",
    },
}


def content_says(deck: str) -> list[tuple[str, str, str]]:
    """Return [(scene_id, title, say)] for content scenes with a say, in order."""
    data = yaml.safe_load((STORY / f"{deck}.yml").read_text(encoding="utf-8"))
    out = []
    for s in data["scenes"]:
        if s.get("kind", "content") == "content" and "say" in s:
            out.append((s["id"], s.get("title", ""), s["say"]))
    return out


def spoken_map(deck: str) -> dict[str, str]:
    return yaml.safe_load((CONTENT / f"{deck}.spoken.yml").read_text(encoding="utf-8"))


def _clean(text: str) -> str:
    """Collapse a block-scalar say/spoken into one flowed paragraph (keep {show})."""
    return " ".join(text.split())


def _esc(text: str) -> str:
    return html.escape(text, quote=False)


def build(deck: str) -> str:
    st = STATUS.get(deck, {})
    says = content_says(deck)
    spoken = spoken_map(deck)

    pills = " ".join(
        f'<span class="pill {kind}">{_esc(label)}</span>' for kind, label in st.get("pills", [])
    )
    gate_rows = "".join(
        f"<tr><td class='g'>{_esc(name)}</td><td>{body}</td></tr>"
        for name, body in st.get("gates", [])
    )
    ha_rows = "".join(
        f"<tr><td class='g'>{_esc(k)}</td><td>{_esc(v)}</td></tr>"
        for k, v in st.get("house_audio", [])
    )

    units = []
    for i, (sid, title, say) in enumerate(says, start=1):
        sp = spoken.get(sid, "(missing spoken entry)")
        units.append(f"""
      <section class="unit">
        <h3>u{i} · <code>{_esc(sid)}</code> — {_esc(title)}</h3>
        <div class="cols">
          <div class="col">
            <div class="lab">Source · storyboard <code>say:</code>（LOCKED；數學渲染）</div>
            <div class="say">{_esc(_clean(say))}</div>
          </div>
          <div class="col">
            <div class="lab">Spoken · MiMo 照念（數學攤成口語、無符號）</div>
            <div class="spk">{_esc(_clean(sp))}</div>
          </div>
        </div>
      </section>""")

    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>§{st.get('section','')} MiMo Spoken Narration — Applied Review</title>
<script>
window.MathJax = {{ tex: {{ inlineMath: [['$','$']] }}, svg: {{ fontCache: 'global' }} }};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" id="MathJax-script" async></script>
<style>
  :root {{ --ink:#172033; --muted:#5f6b7b; --line:#d7dde8; --paper:#f7f5ef; --panel:#fff;
           --accent:#1f6feb; --ok:#1a7f4b; --warn:#9a6b00; --soft:#eef4ff; --spk:#f3faf5; }}
  body {{ margin:0; background:var(--paper); color:var(--ink);
          font-family:"Segoe UI","Noto Sans TC",Arial,sans-serif; line-height:1.55; }}
  main {{ max-width:1080px; margin:0 auto; padding:34px 24px 60px; }}
  h1 {{ font-size:30px; margin:0 0 4px; }}
  h2 {{ font-size:21px; margin:34px 0 12px; border-top:1px solid var(--line); padding-top:22px; }}
  h3 {{ font-size:16px; margin:0 0 10px; font-weight:600; }}
  .lead {{ color:var(--muted); font-size:16px; margin:6px 0 18px; }}
  .pill {{ display:inline-block; padding:3px 10px; border-radius:999px; font-size:13px;
           margin-right:6px; border:1px solid var(--line); }}
  .pill.ok {{ background:#e7f6ee; color:var(--ok); border-color:#bfe6cf; }}
  .pill.warn {{ background:#fdf3df; color:var(--warn); border-color:#f0dca6; }}
  table {{ width:100%; border-collapse:collapse; background:var(--panel);
           border:1px solid var(--line); border-radius:8px; overflow:hidden; margin:10px 0; }}
  td {{ padding:10px 12px; border-bottom:1px solid var(--line); vertical-align:top; }}
  tr:last-child td {{ border-bottom:0; }}
  td.g {{ width:34%; color:var(--muted); font-weight:600; }}
  code {{ font-family:Consolas,monospace; font-size:.92em; background:#eef0f4;
          padding:1px 4px; border-radius:4px; }}
  .unit {{ background:var(--panel); border:1px solid var(--line); border-radius:8px;
           padding:14px 16px; margin:12px 0; }}
  .cols {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; }}
  @media (max-width:760px) {{ .cols {{ grid-template-columns:1fr; }} }}
  .lab {{ font-size:12px; color:var(--muted); margin-bottom:5px; text-transform:none; }}
  .say {{ background:var(--soft); border:1px solid #cfe0ff; border-radius:6px; padding:10px 12px; }}
  .spk {{ background:var(--spk); border:1px solid #bfe6cf; border-radius:6px; padding:10px 12px; }}
  .note {{ background:var(--soft); border:1px solid #cfe0ff; border-radius:8px; padding:12px 14px; margin:14px 0; }}
</style>
</head>
<body>
<main>
  <h1>§{st.get('section','')} {_esc(st.get('title',''))} — MiMo 旁白（口語版）Applied Review</h1>
  <p class="lead">deck <code>{_esc(deck)}</code> · CONTENT_APPROVED: {_esc(st.get('approved',''))}
     · {_esc(st.get('date',''))} · 分支 video/template-redesign-navy-spine</p>
  <p>{pills}</p>

  <div class="note">本輪產物：口語單一源 <code>{_esc(deck)}.spoken.yml</code>（21 個 content 場，英文散文逐字保留、
  只把 LaTeX 攤成口語、<code>{{show}}</code> 原位保留）→ <code>derive_spoken.py</code> 生成
  <code>{_esc(deck)}_mimo.yml</code>（MiMo 合成用）＋ <code>{_esc(deck)}_narration_spoken.md</code>（閱讀版）。
  機械 parity（id 對映／<code>{{show}}</code> 一致／無 <code>$</code> 洩漏）由 <code>derive_spoken.py --check</code> 守門。</div>

  <h2>NFA 忠實稽核（雙閘 + 回歸）</h2>
  <table>{gate_rows}</table>

  <h2>House audio（Candidate B）</h2>
  <table>{ha_rows}</table>
  <p class="lead">最終 render：{_esc(st.get('render',''))}</p>

  <h2>逐段對照：Source <code>say:</code> → Spoken（MiMo 照念）</h2>
  <p class="lead">左為已認可的 storyboard 旁白（數學以 MathJax 渲染）；右為攤成口語、無符號的實際朗讀文字。
     <code>{{show ...}}</code> 為 beat 揭示標記，與正典對齊。</p>
  {''.join(units)}
</main>
</body>
</html>
"""


def main() -> int:
    deck = sys.argv[1] if len(sys.argv) > 1 else "ch03_trig_derivatives"
    out_path = OUT / f"REVIEW-{deck}-mimo-spoken-applied.html"
    out_path.write_text(build(deck), encoding="utf-8")
    print(f"[build_spoken_review] wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

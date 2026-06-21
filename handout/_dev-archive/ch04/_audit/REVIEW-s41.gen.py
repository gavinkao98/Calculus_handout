#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the §4.1 gate-1 and gate-2 audit reports as TWO independent standalone HTMLs.

  REVIEW-ch04_s41-gate1.html  — gate 1: free 4-lens adversarial audit (Claude, wf_b32c202e)
  REVIEW-ch04_s41-gate2.html  — gate 2: Codex (gpt-5.5 xhigh), read from result_s41*.json

House form mirrors handout/_audit/REVIEW-ch01-*-audit-gate{1,2}.html (separate gate files).
Each report is self-contained: MathJax CDN, a compact "audited units" provenance table, the
gate verdict, and the finding cards. Run:  python REVIEW-s41.gen.py
"""
import json
import html
from pathlib import Path

HERE = Path(__file__).resolve().parent
run1 = json.loads((HERE / "result_s41.json").read_text(encoding="utf-8"))
run2 = json.loads((HERE / "result_s41_r2.json").read_text(encoding="utf-8"))

def esc(s):
    return html.escape(str(s), quote=False)

# ── audited units (compact provenance; shared by both gate reports) ──
UNITS = [
    ("Chapter opener", "章首 chapter-head＋lead＋六條 learning objectives", "brief §B.2（章層，涵蓋 §4.1–§4.5）", ""),
    ("§4.1 opener (intuition)", "§4.1 開頭動機散文", "expansion:intuition（承重直覺）", ""),
    ("Rational exponents → series", "子節 From rational exponents…", "seed（手稿 p.1）", ""),
    ("Irrational a^r motivation", "同子節", "expansion:intuition；fence→§4.5（D6）", ""),
    ("Definition 4.1 (+gloss)", "Definition 4.1", "seed（手稿 p.2）；gloss=expansion:intuition", ""),
    ("Caution（series defines）", "Definition 4.1 之後", "expansion:caution（ROADMAP pitfall）", ""),
    ("Theorem 4.1 Completeness", "子節 completeness", "seed（手稿「Property」p.2）；陳述不證", ""),
    ("Remark 4.1（ℝ vs ℚ）", "Theorem 4.1 之後", "expansion:intuition", "gate-2 run2：根存在加 a>0 條件"),
    ("Strategy 4.1（geometric tail）", "Convergence 子節前", "expansion:strategy（§4.2 重用）", ""),
    ("Theorem 4.2 + Proof", "Theorem 4.2＋Proof", "seed [e1]（手稿 pp.2–3）", ""),
    ("P_k 與尾界 (∗)", "Proof 之後", "seed（手稿 p.3）", "gate-2 run1：補回中間步 L^k/k!"),
    ("value of e ＋ Example 4.1 ＋ Figure 4.1", "子節 The value of e", "expansion:formula/history/example/figure（D5）", "gate-2 run1 BLOCKING：移除 e^0=1"),
    ("Summary（→§4.2）", "節末", "expansion:summary", "gate-2 run2：§4.2 預告精準化"),
]

# ── gate-1: free 4-lens adversarial audit (wf_b32c202e): 0 blocking, 7 advisory ──
GATE1 = [
    ("applied", "prose-typography", "直引號 <code>Rolle's</code> → curly <code>Rolle’s</code>，對齊全書 house style。", "已套"),
    ("kept", "faithfulness", "章 opener 的 \\(|(e^h-1)/h-1|\\le|h|\\)、Rolle/MVT/ln 為 brief §B.2 章層 objectives，非 §4.1 body preview-creep。", "非 finding（sanctioned）"),
    ("kept", "faithfulness", "\\(e\\) irrational/transcendental 標 <code>[source:]</code>、與 legacy ground truth 一致。", "非 finding"),
    ("kept", "faithfulness", "Definition 4.1 informal gloss 的 expansion marker 位置合規（緊接 addition）。", "非 finding"),
    ("kept", "direction-conformance", "opener 涵蓋全章 objectives：brief §B.2 明訂。", "sanctioned"),
    ("kept", "direction-conformance", "\\(a^r\\)／continuity／exponent law／\\((e^x)'\\) 皆單行 fence、未實作。", "conforming"),
    ("kept", "cross-ref", "(∗) 以 inline math \\((*)\\) 引用，與顯示式 <code>\\tag{*}</code> 的渲染 glyph 一致。", "refute-leaning，保留"),
]

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#f7f7f5;color:#1d1d1f;font-family:-apple-system,"Segoe UI",Roboto,"Noto Sans TC","PingFang TC",sans-serif;line-height:1.6;padding:32px 18px 80px}
.wrap{max-width:940px;margin:0 auto}
h1{font-size:1.5rem;margin:0 0 4px}
h2{font-size:1.16rem;margin:30px 0 6px;padding-bottom:6px;border-bottom:2px solid #e4e4e0}
.lede{color:#6b6b70;margin:0 0 16px;font-size:.93rem}
.note{background:#fff;border:1px solid #e4e4e0;border-left:3px solid #2552b3;border-radius:8px;padding:12px 16px;margin:14px 0;font-size:.93rem}
.note.pass{background:#eaf6ed;border-left-color:#1a7f37}
.note.pass b{color:#1a7f37}
.note.warn{background:#fff6e3;border-left-color:#8a5a00}
.zero{color:#1a7f37;font-weight:700}.blkw{color:#a11;font-weight:700}
table.u{width:100%;border-collapse:collapse;margin:10px 0;font-size:.83rem}
table.u th,table.u td{border:1px solid #e4e4e0;padding:6px 8px;text-align:left;vertical-align:top}
table.u th{background:#eef0f4}
table.u td.src{color:#5b3aa8}.table.u td.fx{color:#7a5b00}
td.fx{color:#7a5b00}
.card{background:#fff;border:1px solid #e4e4e0;border-radius:10px;padding:12px 15px;margin:11px 0}
.card.blk{border-left:4px solid #a11}.card.adv{border-left:4px solid #8a5a00}
.card.applied{border-left:4px solid #1a7f37}.card.kept{border-left:4px solid #9aa}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px;align-items:center}
.chip{font-size:.74rem;padding:2px 9px;border-radius:999px;font-weight:600;letter-spacing:.02em}
.c-blk{background:#fdeceb;color:#a11}.c-adv{background:#eef0f4;color:#555}.c-cat{background:#e7eefc;color:#1f49a6}
.c-app{background:#e6f7ea;color:#1a7f37}.c-kept{background:#eef0f4;color:#555}.c-lvl{background:#1d1d1f;color:#fff;font-family:ui-monospace,Menlo,Consolas,monospace}
.where{color:#6b6b70;font-size:.85rem;margin:2px 0 6px}
.issue{margin:2px 0 6px}.ev,.sug{font-size:.84rem;color:#555;margin:3px 0}
.disp{font-weight:700}.disp.applied{color:#1a7f37}.disp.kept{color:#6b6b70}
footer{margin-top:40px;color:#6b6b70;font-size:.85rem;border-top:1px solid #e4e4e0;padding-top:14px}
a{color:#2552b3}
code{background:#f3f4f6;padding:.05rem .3rem;border-radius:3px}
"""

MJ = ("<script>window.MathJax={tex:{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']]},svg:{fontCache:'global'}};</script>"
      "<script src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js\" async></script>")

def units_table():
    rows = ["<tr><th>已寫入單元</th><th>locus</th><th>source</th><th>gate 修正</th></tr>"]
    for label, locus, src, fix in UNITS:
        rows.append(f"<tr><td><b>{esc(label)}</b></td><td>{esc(locus)}</td>"
                    f"<td class='src'>{src}</td><td class='fx'>{fix}</td></tr>")
    return "<table class='u'>" + "".join(rows) + "</table>"

def doc(title, lede, body):
    return (f"<!DOCTYPE html>\n<html lang=\"zh-Hant\">\n<head>\n<meta charset=\"utf-8\">\n"
            f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>{esc(title)}</title>\n"
            f"{MJ}\n<style>{CSS}</style>\n</head>\n<body>\n<div class=\"wrap\">\n"
            f"<h1>{esc(title)}</h1>\n<p class=\"lede\">{lede}</p>\n{body}\n"
            f"<footer>產生器：<code>REVIEW-s41.gen.py</code>　·　成品：<a href=\"../../../chapter4-print-standalone.html\">chapter4-print-standalone.html</a>　·　另一閘：見同目錄 gate1／gate2 檔。</footer>\n"
            f"</div>\n</body>\n</html>")

# ── gate 1 ──
g1_cards = []
for disp, cat, text, verdict in GATE1:
    chip = "c-app" if disp == "applied" else "c-kept"
    g1_cards.append(
        f"<div class='card {disp}'><div class='chips'><span class='chip {chip}'>{disp}</span>"
        f"<span class='chip c-cat'>{esc(cat)}</span></div>"
        f"<div class='issue'>{text}</div><div class='sug'>裁決：<span class='disp {disp}'>{esc(verdict)}</span></div></div>")
g1_body = (
    "<div class='note pass'><b>裁決：<span class='zero'>0 blocking → 通過</span></b>　·　7 advisory（1 已套、6 sanctioned／refute-leaning 非 finding）。"
    "4 lens：math 盲算重算／faithfulness（對 seed）／direction-conformance（對 brief）／prose-kit house rules；每個 blocking 候選皆 refute-by-default 對抗複驗。</div>"
    "<h2>審核對象</h2>" + units_table() +
    "<h2>裁決逐條（7 advisory）</h2>" + "".join(g1_cards))
(HERE / "REVIEW-ch04_s41-gate1.html").write_text(
    doc("§4.1 — gate 1（Claude 4-lens 對抗審）審核稿",
        "第一道閘（免費）：Claude 4-lens 對抗式稽核，workflow <code>wf_b32c202e</code>。blocking = math／faithfulness／direction-conformance；格式 nit = advisory。2026-06-21。",
        g1_body), encoding="utf-8")

# ── gate 2 ──
def g2_cards(findings):
    out = []
    for f in findings:
        blocking = f.get("blocking")
        cls = "blk" if blocking else "adv"
        chip = ("c-blk", "BLOCKING") if blocking else ("c-adv", "advisory")
        out.append(
            f"<div class='card {cls}'><div class='chips'><span class='chip {chip[0]}'>{chip[1]}</span>"
            f"<span class='chip c-cat'>{esc(f.get('category',''))}</span>"
            f"<span class='chip c-lvl'>L{esc(f.get('level','?'))}</span>"
            f"<span class='chip c-adv'>{esc(f.get('severity',''))}</span></div>"
            f"<div class='where'>{esc(f.get('where',''))}</div>"
            f"<div class='issue'>{esc(f.get('issue',''))}</div>"
            f"<div class='ev'>證據：{esc(f.get('evidence',''))}</div>"
            f"<div class='sug'>建議：{esc(f.get('suggestion',''))}</div></div>")
    return "".join(out) or "<p class='lede'>（無 findings）</p>"

r1conv, r2conv = run1.get("converged"), run2.get("converged")
g2_body = (
    f"<div class='note {'warn' if not r1conv else 'pass'}'><b>run 1 — converged：{str(r1conv).lower()}</b>"
    f"（<span class='blkw'>1 blocking</span>＋1 advisory，已全修）。{esc(run1.get('summary',''))}</div>"
    f"<div class='note pass'><b>run 2 — converged：<span class='zero'>{str(r2conv).lower()}</span></b>"
    f"（0 blocking＋2 advisory，已全套）。{esc(run2.get('summary',''))}</div>"
    "<p class='lede'>原始裁決檔（計費產物）：<code>result_s41.json</code>（run1）、<code>result_s41_r2.json</code>（run2）；prompt：<code>prompt_s41.txt</code>（<code>build_prompt_s41.py</code> 產）。</p>"
    "<h2>審核對象</h2>" + units_table() +
    "<h2>run 1 裁決</h2>" + g2_cards(run1.get("findings", [])) +
    "<h2>run 2 裁決</h2>" + g2_cards(run2.get("findings", [])))
(HERE / "REVIEW-ch04_s41-gate2.html").write_text(
    doc("§4.1 — gate 2（Codex gpt-5.5 xhigh）審核稿",
        "第二道閘（計費，使用者同意）：Codex CLI 唯讀 reviewer、<code>--output-schema</code> 結構化輸出，停在一次乾淨 audit（run2 converged）。2026-06-21。",
        g2_body), encoding="utf-8")

print("wrote REVIEW-ch04_s41-gate1.html + REVIEW-ch04_s41-gate2.html",
      f"(units={len(UNITS)} gate1={len(GATE1)} g2r1={len(run1.get('findings',[]))} g2r2={len(run2.get('findings',[]))})")

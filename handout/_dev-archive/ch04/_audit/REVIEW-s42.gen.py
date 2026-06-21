#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the §4.2 gate-1 audit report as a standalone HTML (gate-2 待 Codex 後補).

  REVIEW-ch04_s42-gate1.html  — gate 1: free 4-lens adversarial audit (Claude, wf_3f10e703)

House form mirrors REVIEW-s41.gen.py / handout/_audit/REVIEW-ch01-*-audit-gate1.html.
Self-contained: MathJax CDN, an "audited units" provenance table, the gate verdict, finding
cards. Run:  python REVIEW-s42.gen.py
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
run1 = json.loads((HERE / "result_s42.json").read_text(encoding="utf-8"))
run2 = json.loads((HERE / "result_s42_r2.json").read_text(encoding="utf-8"))

def esc(s):
    return html.escape(str(s), quote=False)

# ── audited units (compact provenance) ──
UNITS = [
    ("§4.2 opener (intuition)", "節首動機散文", "expansion:intuition（承重直覺）", ""),
    ("Theorem 4.3 + Proof", "continuity for x>0", "seed [e2]（手稿 pp.3–4）", "gate-2 run2：區間 (0,x₀+1) 下界明寫 x>x₀/2>0"),
    ("Remark 4.2（why x<0 harder）", "Thm 4.3 之後", "expansion:intuition", ""),
    ("Proposition 4.1（(△) abs-conv⟹conv）", "Remark 4.2 之後（陳述）", "seed (△)（手稿 p.5）", ""),
    ("Definition 4.2（Cauchy）+gloss", "Definition 4.2", "seed（手稿 p.5）；gloss=expansion:intuition", ""),
    ("Theorem 4.4 Bolzano–Weierstrass + Proof", "peak argument", "expansion（D3①；手稿 punt，超出手稿）", "gate-1 對賬 legacy §4.2"),
    ("Theorem 4.5 Cauchy criterion + Proof", "both directions", "seed Thm（手稿 p.6「we shall not prove」）→ 補全證（D3①）", ""),
    ("Caution（BW dependency）", "Thm 4.5 之後", "expansion:caution（ROADMAP pitfall）", "gate-2 run2：e 無理改 cross-ref §4.1"),
    ("Proof of Proposition 4.1", "deferred proof", "seed（手稿 p.6，用 Cauchy）", ""),
    ("Extension to ℝ + (∗∗)", "子節 Extending e^x to all of ℝ", "seed [e3]+(△)；expansion:formula", "gate-1：(∗∗) 為 (∗) 的絕對值版"),
    ("Theorem 4.6（continuity on ℝ）+ Proof", "full-line continuity", "expansion（brief §C-3；手稿僅 Summary 宣告）", ""),
    ("Theorem 4.7 Exponent law + Proof（6 步）", "binomial／(I)(II)／四項拆／雙重極限", "seed（手稿 pp.7–10）；D3② 完整 6 步", "gate-1 對賬 legacy §4.2 全等"),
    ("Corollary 4.1（positivity）+ Proof", "e^x>0", "expansion（brief §C-1；手稿 [e3] 陳述）", ""),
    ("Summary（→§4.3）", "節末", "seed Summary + expansion:summary", "gate-2 run1 BLOCKING：forward-fence 改 generic（移除 (e^h−1)/h）"),
]

# ── gate-1: free 4-lens adversarial audit (wf_3f10e703): 0 blocking, 8 advisory ──
# (disp, lens-category, finding text, 裁決)
GATE1 = [
    ("applied", "math", "<b>M1</b>　Step 2 的 (I) underbrace 原已寫成 post-binomial 的 <code>\\binom</code> 形，比 Step 3「applies the binomial theorem」搶先一步。改寫成自然形 <code>\\sum_\\ell\\sum_m x^m y^{\\ell-m}/(m!(\\ell-m)!)</code>，讓 Step 3 真正執行二項式改寫（邏輯單調、對齊 signed legacy §4.2）。", "已套（數學等價、流暢度↑）"),
    ("applied", "direction-conformance", "<b>D1／F2</b>　brief §A 指定「首次 reuse 處一句回指 Strategy 4.1」；draft 原只引 (∗)、未點名。於 (∗∗) 推導處加「reusing the geometric-tail estimate of \\((*)\\) (Strategy 4.1)」。", "已套（brief §A 要求）"),
    ("applied", "prose", "<b>G1-1</b>　散文混入英式拼寫（recognise／behaviour／reorganises），與 §4.1 全美式基線及 CONTENT_SPEC §15 不一致。改 recognize／behavior／reorganizes。", "已套（章內一致性）"),
    ("applied", "prose", "<b>G1-2</b>　開場末句概念密度高（em-dash＋三動詞並列＋(∗) 回指）。拆成兩句、em-dash 改冒號，降首讀認知負荷。", "已套（可讀性）"),
    ("kept", "faithfulness", "<b>F1</b>　Step 4 的 (II) 幾何尾界 <code>≤ (2L)^{n₀}/n₀!(½)^{k−n₀}</code> 把中間鏈壓成一句。math lens 與 legacy 對賬確認<strong>正確</strong>；seed 標 [請查核] 之處已走乾淨界，且 Strategy 4.1 回指已 signpost 此手法。", "保留（正確；不過度展開）"),
    ("kept", "prose", "<b>G1-3</b>　BW 前「The hinge is a classical existence theorem」刻意懸念、緊接的 Theorem 4.4 即揭曉；動機在位、非記號先用。", "保留（懸念無礙、conf 0.35）"),
    ("kept", "prose", "<b>G1-4</b>　Remark 4.2 末句 relative clause 句構略繞但語意正確、不誤導數學。", "保留（可接受、conf 0.30）"),
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
table.u td.src{color:#5b3aa8}
td.fx{color:#7a5b00}
.card{background:#fff;border:1px solid #e4e4e0;border-radius:10px;padding:12px 15px;margin:11px 0}
.card.applied{border-left:4px solid #1a7f37}.card.kept{border-left:4px solid #9aa}
.card.blk{border-left:4px solid #a11}.card.adv{border-left:4px solid #8a5a00}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px;align-items:center}
.chip{font-size:.74rem;padding:2px 9px;border-radius:999px;font-weight:600;letter-spacing:.02em}
.c-cat{background:#e7eefc;color:#1f49a6}
.c-app{background:#e6f7ea;color:#1a7f37}.c-kept{background:#eef0f4;color:#555}
.c-blk{background:#fdeceb;color:#a11}.c-adv{background:#eef0f4;color:#555}.c-lvl{background:#1d1d1f;color:#fff;font-family:ui-monospace,Menlo,Consolas,monospace}
.where{color:#6b6b70;font-size:.85rem;margin:2px 0 6px}.ev{font-size:.84rem;color:#555;margin:3px 0}
.issue{margin:2px 0 6px}.sug{font-size:.84rem;color:#555;margin:3px 0}
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
            f"<footer>產生器：<code>REVIEW-s42.gen.py</code>　·　成品：<a href=\"../../../chapter4-print-standalone.html\">chapter4-print-standalone.html</a>　·　另一閘：見同目錄 <code>REVIEW-ch04_s42-gate1.html</code>／<code>REVIEW-ch04_s42-gate2.html</code>。</footer>\n"
            f"</div>\n</body>\n</html>")

# lens summaries (verbatim verdict context from wf_3f10e703)
LENS = [
    ("math fidelity", "盲算重算每一步並對賬 signed legacy §4.2：Thm 4.3 連續、Thm 4.4 BW peak、Thm 4.5 Cauchy 兩向、Prop 4.1、Thm 4.7 指數律（(I)/(II) 拆、二項式收 (I)=P_k(x+y)、(II) 尾界 k>n₀>8L、四項拆 telescope、(∗∗) 於 x+y、雙重極限）、Cor 4.1 正性——<b>全部正確，0 blocking</b>。"),
    ("direction-conformance", "對 ③-approved brief 全守：編號 ledger（Def 4.2／Thm 4.3–4.7／Prop 4.1／Cor 4.1／Rem 4.2／Caution 無編號）接 §4.1 無撞號；D3①（完整 BW，非 punt 非 outline）、D3②（完整 6 步）、D8（\\binom＋cross-ref C^n_k）皆守；「刻意不寫」fence 全守（不重證 completeness／(∗)、不碰差分商/(e^x)'、不碰 ln、不證二項式、無 Rolle/MVT、無自創 exercise）。<b>0 blocking</b>。"),
    ("seed/manuscript faithfulness", "對 seed（手稿 pp.3–10）忠實：四大手稿結構保序；所有超出 seed 的 addition（完整 BW、Thm 4.6、Cor 4.1、Rem 4.2、Caution）皆有 <code>expansion:</code> marker 且數學對賬 legacy 無誤；三個 [請查核]（e^y 正性／(II) 收法／全ℝ連續）皆妥善 discharge。<b>0 blocking</b>。"),
    ("prose / readability", "語域與 §4.1 一致、每條 formal result 有動機鋪陳、邏輯橋接齊全、無術語先用後定義；指數律 6 步與 BW peak argument 學生可循。<b>易懂性 0 blocking、prose gate 通過</b>；findings 全為 advisory polish。"),
]

lens_html = "".join(
    f"<div class='card kept'><div class='chips'><span class='chip c-cat'>{esc(name)}</span>"
    f"<span class='chip c-app'>0 blocking</span></div><div class='issue'>{summary}</div></div>"
    for name, summary in LENS)

g1_cards = []
for disp, cat, text, verdict in GATE1:
    chip = "c-app" if disp == "applied" else "c-kept"
    g1_cards.append(
        f"<div class='card {disp}'><div class='chips'><span class='chip {chip}'>{disp}</span>"
        f"<span class='chip c-cat'>{esc(cat)}</span></div>"
        f"<div class='issue'>{text}</div><div class='sug'>裁決：<span class='disp {disp}'>{esc(verdict)}</span></div></div>")

n_applied = sum(1 for d, *_ in GATE1 if d == "applied")
n_kept = sum(1 for d, *_ in GATE1 if d == "kept")
g1_body = (
    "<div class='note pass'><b>裁決：<span class='zero'>0 blocking → 通過</span></b>　·　8 advisory findings（D1 與 F2 為同一議題、兩 lens 各提一次 → 合併為 "
    f"{n_applied + n_kept} 張卡：{n_applied} 已套、{n_kept} 保留）。4 lens 平行對抗審（math 盲算重算對賬 legacy／faithfulness 對 seed／"
    "direction-conformance 對 brief／prose house rules），每個 blocking 候選皆 refute-by-default 對抗複驗（本輪 0 candidates）。"
    "workflow <code>wf_3f10e703</code>。</div>"
    "<h2>四 lens 裁決</h2>" + lens_html +
    "<h2>審核對象（已寫入單元）</h2>" + units_table() +
    "<h2>裁決逐條（8 findings → " + str(n_applied + n_kept) + " 卡：" + str(n_applied) + " 已套、" + str(n_kept) + " 保留）</h2>" + "".join(g1_cards))

(HERE / "REVIEW-ch04_s42-gate1.html").write_text(
    doc("§4.2 — gate 1（Claude 4-lens 對抗審）審核稿",
        "第一道閘（免費）：Claude 4-lens 對抗式稽核，workflow <code>wf_3f10e703</code>。blocking = math／faithfulness／direction-conformance；格式 nit = advisory。§4.2 重跑（舊 POC 已棄），2026-06-21。",
        g1_body), encoding="utf-8")

# ── gate 2 (Codex gpt-5.5 xhigh; result_s42*.json) ──
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
    f"（<span class='blkw'>1 blocking</span>，已修：收尾 forward-fence 移除 \\((e^h-1)/h\\)、改 generic 一句）。{esc(run1.get('summary',''))}</div>"
    f"<div class='note pass'><b>run 2 — converged：<span class='zero'>{str(r2conv).lower()}</span></b>"
    f"（0 blocking＋2 advisory，已全套：Thm 4.3 區間下界明寫、Caution e 無理改 cross-ref §4.1）。{esc(run2.get('summary',''))}</div>"
    "<p class='lede'>原始裁決檔（計費產物）：<code>result_s42.json</code>（run1）、<code>result_s42_r2.json</code>（run2）；prompt：<code>prompt_s42.txt</code>（<code>build_prompt_s42.py</code> 產）。模型 Codex <code>gpt-5.5</code>／reasoning <code>xhigh</code>、唯讀 sandbox、<code>--output-schema schema.json</code>、prompt 由 Bash <code>&lt; file</code> 餵原始 UTF-8。</p>"
    "<h2>審核對象（已寫入單元）</h2>" + units_table() +
    "<h2>run 1 裁決（1 blocking → 已修）</h2>" + g2_cards(run1.get("findings", [])) +
    "<h2>run 2 裁決（converged，2 advisory 已套）</h2>" + g2_cards(run2.get("findings", [])))
(HERE / "REVIEW-ch04_s42-gate2.html").write_text(
    doc("§4.2 — gate 2（Codex gpt-5.5 xhigh）審核稿",
        "第二道閘（計費，使用者同意）：Codex CLI 唯讀 reviewer、<code>--output-schema</code> 結構化輸出，停在一次乾淨 audit（run2 converged）。§4.2 重跑，2026-06-21。",
        g2_body), encoding="utf-8")

print(f"wrote REVIEW-ch04_s42-gate1.html + REVIEW-ch04_s42-gate2.html "
      f"(units={len(UNITS)} gate1={len(GATE1)}: {n_applied} applied / {n_kept} kept; "
      f"g2r1={len(run1.get('findings',[]))} blocking={sum(1 for f in run1.get('findings',[]) if f.get('blocking'))} "
      f"g2r2={len(run2.get('findings',[]))} converged={run2.get('converged')})")

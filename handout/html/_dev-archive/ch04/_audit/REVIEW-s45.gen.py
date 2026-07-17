#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the §4.5 gate-1 + gate-2 audit reports as standalone HTML.

  REVIEW-ch04_s45-gate1.html  — gate 1: free 4-lens adversarial audit (Claude subagents)
  REVIEW-ch04_s45-gate2.html  — gate 2: Codex gpt-5.5 xhigh (reads result_s45.json + _r2/_r3/_r4)

House form mirrors REVIEW-s44.gen.py, extended to FOUR gate-2 runs (reasoning-model
run-to-run drift surfaced fresh marginal findings each pass; union taken, converged at
run4). Self-contained: MathJax CDN, an "audited units" provenance table, gate verdicts,
finding cards. Run:  python REVIEW-s45.gen.py
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
runs = []
for suffix in ["", "_r2", "_r3", "_r4"]:
    runs.append(json.loads((HERE / f"result_s45{suffix}.json").read_text(encoding="utf-8")))

def esc(s):
    return html.escape(str(s), quote=False)

# ── audited units (compact provenance) ──
UNITS = [
    ("§4.5 opener (strict-monotonicity engine; closes both fences)", "節首動機散文", "expansion:intuition", "§C-11：關 Ch3 §3.3 與 §4.1 a^r 兩 forward-fence；gate-1 prose：opener 長句拆兩句（已套）"),
    ("Definition 4.4 — natural logarithm ln x (+ range assertion + gloss)", "子節 Defining the natural logarithm", "seed（手稿 p.18–19 Def）", "§C-1：range (0,∞) <b>斷言不證</b>＋一句依賴（連續＋極限＋IVT）；e^{ln x}=x／ln(e^x)=x 雙恆等"),
    ("Caution — ln defined only for x>0", "Definition 後", "expansion:caution（§C-2，ROADMAP pitfall）", "ln 0／ln(−1) undefined（e^a&gt;0）"),
    ("Figure 4.3 — e^x / ln x reflection across y=x", "Definition 後", "expansion:figure（§C-3，ROADMAP key figure）", "JS FIGS『exp-log-reflection』；新增 .curve-log（紅 ln）＋.idline（灰虛線 y=x）CSS；render 證 (0,1)↔(1,0) 鏡像、等比例尺保 45°"),
    ("Theorem 4.13 — ln continuous + Proof", "子節 Continuity of the logarithm", "seed（手稿 pp.19–20 Property）", "反證、雙 case、ε=min{…}；靠 e^x strict monotonicity；比 legacy WLOG 單邊更完整"),
    ("Theorem 4.14 — (ln x)' = 1/x + Proof", "子節 The derivative of the logarithm", "seed（手稿 pp.21–22）", "inverse-function 技巧：h=e^y−e^{y_0}、商倒置、y→y_0 靠連續、分母→e^{y_0}=x（用 Thm 4.8）"),
    ("Remark 4.5 — rigorous vs Ch3 §3.3 chain-rule (closes loop)", "Theorem 4.14 後", "expansion:intuition（§C-4，ROADMAP prerequisite）", "<b>gate-2 run1+run3 修</b>：刪去過度推廣的 inverse-function 泛化末句（兩輪磁鐵，缺完整 inverse-function 假設）；核心對比＋關 §3.3 迴路保留"),
    ("Corollary 4.4 — f'=0 ⟹ constant + Proof", "子節 Logarithm laws and general powers", "seed HW1（§C-5 升格）", "MVT 推論；置於 Proposition 4.3 前（just-in-time）"),
    ("Proposition 4.3 — logarithm product law ln(ab)=ln a+ln b + Proof", "Corollary 4.4 後", "seed HW2（§C-6 add-on：升格<b>具名 Proposition</b>）", "f(x)=ln(ax)−ln x、f'=0、套 Cor 4.4、ln 1=0"),
    ("Example 4.5 — general powers a^x := e^{x ln a}", "Proposition 4.3 後", "seed HW4（§C-7 升格）", "指數律 (i)(ii)；用 Prop 4.3＋Thm 4.7；<b>收束 §4.1 D6 的 a^r fence</b>"),
    ("Remark 4.6 — Cauchy functional-equation characterisation", "Example 4.5 後", "seed HW3（§C-8 add-on：一句 remark）", "<b>gate-2 run2 修</b>：裁去『pins g on rationals…continuity extends』證明骨架，只留刻畫＋proof omitted"),
    ("Application capstone — growth/decay, half-life", "子節 Why these functions are unavoidable", "expansion:application（§C-10 add-on）", "<b>gate-2 run2 修</b>：反演式 t=(ln y*−ln y(0))/k 補『positive quantities 且 k≠0』條件"),
    ("Chapter summary — 4 strands (exponential / analysis / existence / logarithm)", "子節 Chapter summary（章末）", "expansion:summary（§C-9，CONTENT_SPEC §4）", "<b>gate-2 run2 修</b>：(e^h−1)/h−1 bound 補『|h|&lt;½』限制（無條件即偽）"),
]

# ── gate-1: free 4-lens adversarial audit (parallel subagents): 0 blocking, 6 advisory (prose) ──
# (disp, lens-category, finding text, 裁決)
GATE1 = [
    ("applied", "prose", "<b>prose F4</b>　opener「the continuity of \\(\\ln\\) and its differentiability are not free gifts … — each needs an argument, and both arguments reach back …」單句疊四個動作＋em-dash＋分號，過長。於 em-dash 處拆兩句。", "已套（可讀性）"),
    ("applied", "prose", "<b>prose F3</b>　capstone 半衰期句以裸 and 串接兩個獨立結果（一般反演式／half-life 特例），首讀像同一推導的延續（garden-path）。拆句＋『just the case』標示特例化。", "已套（去 garden-path）"),
    ("applied", "prose", "<b>prose F5</b>　Remark 4.6『we omit the several steps』中『the several steps』對 register 略口語。改『the argument』。", "已套（register 一致；註：該句後於 gate-2 run2 再被裁短）"),
    ("kept", "prose", "<b>prose F2</b>　§C-1 range 句『but the details would detain us』被評為 filler hedge。<b>保留</b>：此句正是 §C-1『斷言不證』的承重信號（說明為何不證＝會岔題），刪去會失去 manuscript-faithful 的『set aside』語義。", "保留（承載 §C-1 斷言不證）"),
    ("kept", "prose", "<b>prose F1</b>　chain-rule-presupposes-differentiability 在 opener／Thm 4.14 lead／Remark 4.5 出現三次。<b>保留</b>：此為本節方法論主軸（可微性可萃取、不必預設），三處措辭已各異（without assuming／silently assumes／presupposes）、各在不同 locus 服務不同功能，屬 §3-protected teaching repetition。（註：Remark 4.5 末句後於 gate-2 因另一理由刪除。）", "保留（teaching repetition、framing 已各異）"),
    ("kept", "prose", "<b>prose F4(opt)</b>　opener 末句『two debts … the informal logarithm of §3.3 and the meaning of a^r …, deferred back in §4.1』後置兩 cross-ref。<b>保留</b>：刻意平行（兩 fence 並列收束），低優先。", "保留（刻意平行、taste）"),
]

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#f7f7f5;color:#1d1d1f;font-family:-apple-system,"Segoe UI",Roboto,"Noto Sans TC","PingFang TC",sans-serif;line-height:1.6;padding:32px 18px 80px}
.wrap{max-width:940px;margin:0 auto}
h1{font-size:1.5rem;margin:0 0 4px}
h2{font-size:1.16rem;margin:30px 0 6px;padding-bottom:6px;border-bottom:2px solid #e4e4e0}
h3{font-size:1rem;margin:20px 0 4px;color:#444}
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
.runstat{font-size:.86rem;margin:8px 0;padding:7px 12px;border-radius:6px;background:#fff;border:1px solid #e4e4e0}
footer{margin-top:40px;color:#6b6b70;font-size:.85rem;border-top:1px solid #e4e4e0;padding-top:14px}
a{color:#2552b3}
code{background:#f3f4f6;padding:.05rem .3rem;border-radius:3px}
"""

MJ = ("<script>window.MathJax={tex:{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']]},svg:{fontCache:'global'}};</script>"
      "<script src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js\" async></script>")

def units_table():
    rows = ["<tr><th>已寫入單元</th><th>locus</th><th>source</th><th>gate 修正／備註</th></tr>"]
    for label, locus, src, fix in UNITS:
        rows.append(f"<tr><td><b>{esc(label)}</b></td><td>{esc(locus)}</td>"
                    f"<td class='src'>{src}</td><td class='fx'>{fix}</td></tr>")
    return "<table class='u'>" + "".join(rows) + "</table>"

def doc(title, lede, body, gen, other):
    return (f"<!DOCTYPE html>\n<html lang=\"zh-Hant\">\n<head>\n<meta charset=\"utf-8\">\n"
            f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>{esc(title)}</title>\n"
            f"{MJ}\n<style>{CSS}</style>\n</head>\n<body>\n<div class=\"wrap\">\n"
            f"<h1>{esc(title)}</h1>\n<p class=\"lede\">{lede}</p>\n{body}\n"
            f"<footer>產生器：<code>{gen}</code>　·　成品：<a href=\"../../../chapter4-print-standalone.html\">chapter4-print-standalone.html</a>　·　另一閘：見同目錄 <code>{other}</code>。</footer>\n"
            f"</div>\n</body>\n</html>")

# lens summaries (verbatim verdict context from the 4-lens gate-1 parallel-subagent run)
LENS = [
    ("math fidelity", "獨立盲算重算每一步並對賬 signed legacy §4.5（def:logarithm／thm:ln-continuous／thm:ln-derivative-rigorous）：Definition 4.4 雙恆等式量詞、Theorem 4.13 連續性反證（雙 case 不等式方向、ε=min&gt;0、y_j=e^{ln y_j} 恆等、矛盾成立——<b>比 legacy WLOG 單邊更完整</b>）、Theorem 4.14 inverse-function（e^y−e^{y_0}=h、商倒置需 y≠y_0、h→0⟹y→y_0 靠連續、分母→e^{y_0}=x、倒數合法因極限=x≠0）、Corollary 4.4（MVT 於 [x_1,x_2]）、Proposition 4.3（chain rule f'=0、ln 1=0、Cor 4.4 套於 1↔x 閉區間合法）、Example 4.5 指數律 (i)(ii)、application 半衰期（kt=−ln2⟹ln2/|k|）、Remark 4.6 刻畫——<b>9 項全正確，0 blocking／0 advisory</b>。"),
    ("seed/manuscript faithfulness", "對 seed（手稿 pp.18–22＋HW pp.23–24）忠實：連續性／可微兩證骨架逐步對映手稿；range (0,∞) 維持<b>斷言不證</b>（未偷渡證明）；四項 HW 升格（Cor 4.4=HW1、Prop 4.3=HW2、Ex 4.5=HW4、Remark 4.6=HW3）皆忠實 manuscript 陳述、且為 ③-approved expansion；無幻覺結果／數值；跨節引用（Thm 4.6/4.7/4.8/4.12、Cor 4.3、Ex 4.4）逐一核對 sibling fragment 全對。<b>0 blocking／0 advisory</b>。"),
    ("direction-conformance", "對 ③-approved brief（『全照提案核可』＋三 add-on）全守：(A) 覆蓋 §C-1…§C-11 全在（range 斷言＋依賴句、ln-domain caution、Figure 4.3、Remark 4.5 關 §3.3 迴路、Cor 4.4 置 Prop 前、<b>HW2→具名 Proposition 4.3</b>、Ex 4.5 收 §4.1 a^r、<b>HW3→一句 Remark 4.6</b>、4-strand 章末 Summary、<b>application capstone</b>、opener 關兩 fence）；(B) 編號 ledger 全對（Def 4.4／Thm 4.13-4.14／Prop 4.3／Cor 4.4／Ex 4.5／Fig 4.3／Rem 4.5-4.6／Caution 無號；無新 Strategy）；(C) do-not-write 全守（無 ∫dt/t 定義、無 log_b／換底、無完整對數律表、range 不證、無複數 log、HW3 不展開、無 Taylor/L'Hôpital、不改寫 Ch3）。<b>0 blocking／0 advisory</b>。"),
    ("prose / readability", "U1–U5 全達（每個 formal result 前皆有動機；Definition 4.4 配 Informally gloss；ε-witness 證前有平白直覺；無術語先用後定義；Caution 具體 unpack x&gt;0）。末節連接組織（opener、proof leads、兩 Remark、capstone、章末 Summary）承重良好。<b>易懂性 0 blocking、prose gate 通過</b>；6 advisory 全 fluency polish（4 tighten＋2 optional）→ 套 3 留 3。house-rule 保護項（單調性主題詞復現、強化散文、lookup-friendly caution）不報。"),
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
    "<div class='note pass'><b>裁決：<span class='zero'>0 blocking → 通過</span></b>　·　4 lens 平行對抗審（並行 subagents）全收斂"
    "（math／faithfulness／direction 各 <b>0 finding</b>；prose 0 blocking）；"
    f"共 6 advisory（全 prose：{n_applied} 已套、{n_kept} 保留）。math 獨立盲算對賬 legacy §4.5／faithfulness 對 seed＋sibling fragments／direction 對 brief 11 §C＋ledger＋do-not-write／prose U1–U5。"
    "修完回歸 render：0 MathJax err／28 頁／0 overflow／0 dangling ref／Figure 4.3 鏡像幾何正確。</div>"
    "<h2>四 lens 裁決（全 0 blocking；math／faith／dir 0 finding）</h2>" + lens_html +
    "<h2>審核對象（已寫入單元）</h2>" + units_table() +
    f"<h2>裁決逐條（6 prose advisory：{n_applied} 已套、{n_kept} 保留）</h2>" + "".join(g1_cards))

(HERE / "REVIEW-ch04_s45-gate1.html").write_text(
    doc("§4.5 — gate 1（Claude 4-lens 對抗審）審核稿",
        "第一道閘（免費）：Claude 4-lens 對抗式稽核（並行 subagents，每 blocking 候選 refute-by-default 複驗）。blocking = math／faithfulness／direction-conformance；格式 nit = advisory。§4.5（全章末節，主風險＝升格範圍與兩證紮實度），2026-06-21。",
        g1_body, "REVIEW-s45.gen.py", "REVIEW-ch04_s45-gate2.html"), encoding="utf-8")

# ── gate 2 (Codex gpt-5.5 xhigh; result_s45.json run1 + _r2/_r3/_r4) ──
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
    return "".join(out) or "<p class='lede'>（無 findings — converged、0 blocking）</p>"

RUN_LABELS = ["run 1", "run 2", "run 3", "run 4"]
RUN_FIX = [
    "→ 修：Remark 4.5 末句『recovers the derivative of <b>any function</b> from … its inverse』過度推廣，補 nonzero-derivative 條件。",
    "→ 修三項：① 章末 Summary 的 (e^h−1)/h−1 bound 補『|h|&lt;½』（h=2 時 LHS≈2.194&gt;2，無條件即偽）；② Remark 4.6 裁去『pins g on rationals…continuity extends』證明骨架；③ capstone 反演式補『positive quantities 且 k≠0』。",
    "→ 修：Remark 4.5 末句仍被抓（更深：nonzero derivative 非充分、尚需可逆＋反函數連續）。此句為 findings 磁鐵（run1+run3），<b>整句刪除</b>——Remark 核心（嚴格 vs chain-rule、關 §3.3 迴路）不靠此句仍完整。",
    "→ <b>converged：0 finding</b>。",
]
TOK = ["≈ 99.5k", "≈ 54.4k", "≈ 55.4k", "≈ 50.4k"]

run_blocks = []
runstat = []
for i, r in enumerate(runs):
    fs = r.get("findings", [])
    nblk = sum(1 for f in fs if f.get("blocking"))
    conv = r.get("converged")
    badge = ("<span class='zero'>converged</span>" if conv else f"<span class='blkw'>{nblk} blocking</span>")
    runstat.append(f"<div class='runstat'><b>{RUN_LABELS[i]}</b>（{TOK[i]} tokens）：{badge} — converged={str(conv).lower()}　{RUN_FIX[i]}</div>")
    run_blocks.append(
        f"<h3>{RUN_LABELS[i]} 裁決（converged={str(conv).lower()}，{len(fs)} finding；{nblk} blocking）</h3>"
        + ("<div class='note pass'>" + esc(r.get('summary', '')) + "</div>" if conv else "<div class='note warn'><b>摘要：</b>" + esc(r.get('summary', '')) + "</div>")
        + g2_cards(fs))

total_blk = sum(sum(1 for f in r.get("findings", []) if f.get("blocking")) for r in runs)
g2_body = (
    "<div class='note pass'><b>最終：<span class='zero'>run 4 converged（0 blocking）</span></b>　·　"
    f"四輪累計 {total_blk} blocking findings（run1:1、run2:3、run3:1、run4:0），跨輪<b>全採納</b>（4 修＋1 刪）。"
    "reasoning 模型 run-to-run 飄、每輪浮不同邊陲 qualification（漏假設／證明骨架／無條件不等式）；取聯集、修到一次乾淨 audit。"
    "core 數學（Def 4.4／Thm 4.13-4.14／Cor 4.4／Prop 4.3／Ex 4.5／圖 caption）四輪皆確認乾淨。修後回歸 render 0 err／28 頁／0 overflow。</div>"
    "<h2>收斂軌跡</h2>" + "".join(runstat) +
    "<p class='lede'>原始裁決檔（計費產物）：<code>result_s45.json</code>／<code>_r2</code>／<code>_r3</code>／<code>_r4</code>；prompt：<code>prompt_s45.txt</code>（<code>build_prompt_s45.py</code> 產，82.6KB）。模型 Codex <code>gpt-5.5</code>／reasoning <code>xhigh</code>、唯讀 sandbox、<code>--output-schema schema.json</code>、prompt 由 Bash <code>&lt; file</code> 餵原始 UTF-8。tokens 四輪合計 ≈ 259.7k。</p>"
    "<h2>審核對象（已寫入單元）</h2>" + units_table() +
    "<h2>逐輪裁決</h2>" + "".join(run_blocks))
(HERE / "REVIEW-ch04_s45-gate2.html").write_text(
    doc("§4.5 — gate 2（Codex gpt-5.5 xhigh）審核稿",
        "第二道閘（計費，使用者同意；含 run2–run4）：Codex CLI 唯讀 reviewer、<code>--output-schema</code> 結構化輸出。§4.5 四輪收斂：run1 1 blocking→run2 3→run3 1→run4 converged（reasoning drift、取聯集、停在一次乾淨 audit）。2026-06-21。",
        g2_body, "REVIEW-s45.gen.py", "REVIEW-ch04_s45-gate1.html"), encoding="utf-8")

print(f"wrote REVIEW-ch04_s45-gate1.html + REVIEW-ch04_s45-gate2.html "
      f"(units={len(UNITS)} gate1={len(GATE1)}: {n_applied} applied / {n_kept} kept; "
      f"gate2 runs={len(runs)} total_blocking={total_blk} final_converged={runs[-1].get('converged')})")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the §4.4 gate-1 + gate-2 audit reports as standalone HTML.

  REVIEW-ch04_s44-gate1.html  — gate 1: free 4-lens adversarial audit (Claude workflow)
  REVIEW-ch04_s44-gate2.html  — gate 2: Codex gpt-5.5 xhigh (reads result_s44.json + _r2.json)

House form mirrors REVIEW-s43.gen.py (two gate-2 runs, as in §4.1/§4.2). Self-contained:
MathJax CDN, an "audited units" provenance table, the gate verdict, finding cards.
§4.4 gate-2: run1 1 blocking (§4.5 scope leak in closer) → fixed → run2 converged.
Run:  python REVIEW-s44.gen.py
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
run1 = json.loads((HERE / "result_s44.json").read_text(encoding="utf-8"))
run2 = json.loads((HERE / "result_s44_r2.json").read_text(encoding="utf-8"))

def esc(s):
    return html.escape(str(s), quote=False)

# ── audited units (compact provenance) ──
UNITS = [
    ("§4.4 opener (existence-bridge + history)", "節首動機散文", "expansion:intuition（承 §4.3 closer 的 forward-fence）＋expansion:history（Rolle 1691／Cauchy 一句，[source: standard note]）", ""),
    ("Definition 4.3 (max/min) + cos x anchor", "子節 Maxima, minima…", "seed（手稿 p.11 Def 1＋Ex）", "對偶 min 折入；cos x 為 inline 具體錨（非編號 Example）"),
    ("Theorem 4.9 — Extreme Value Theorem", "EVT，陳述不證", "seed「Fact」（手稿 p.12）", "§C-3：具名、cross-ref 完備性 Thm 4.1、一句兩條件皆必要"),
    ("Theorem 4.10 — Interior Extremum (Theorem A) + Proof", "interior extremum ⟹ f'=0", "seed（手稿 pp.12–13）", "§C-8 保留手稿名「Theorem A」為副名；§C-6a interior-必要 caution"),
    ("Theorem 4.11 — Rolle + Proof", "Case 1／Case 2", "seed（手稿 pp.13–15）", "<b>§C-1 修 Case 2 (ii) 筆誤</b>：f(X_m)&lt;f(a)（手稿誤作 X_M；對賬 legacy line 612）"),
    ("Theorem 4.12 — Mean Value Theorem + Proof", "輔助 g＝曲線減割線", "seed（手稿 pp.15–17）", "g(a)=g(b)=0 → Rolle → f'(c)=平均斜率；gate-1／gate-2 對賬 legacy 全等"),
    ("Figure 4.2 — MVT secant–tangent", "MVT 後", "expansion:figure（ROADMAP §4.4 key figure）", "JS FIGS『mvt-secant-tangent』；render 證 tangent 與 secant 數值平行、於內部 c 觸線"),
    ("Remark 4.4 — existence-engine synthesis", "MVT 後", "expansion:intuition（§C-10 選配，已取）", "gate-1 prose：拆 which→which 鏈"),
    ("Strategy 4.2 — Applying the MVT", "驗 hypotheses", "expansion:strategy（§C-5，ROADMAP）", "|x| on [−1,1] 反例＋closed/open 不對稱折入；gate-1 prose：step3 措辭去壓縮"),
    ("Corollary 4.3 — Monotonicity (both forms) + Proof", "f'≥0⟹non-decr；f'>0⟹strict", "seed（手稿 p.18）", "<b>§C-2 補 strict 版</b>（手稿僅非嚴格、Example 卻嚴格；§4.5 需單射）"),
    ("Example 4.2 — MVT on x² (c=1)", "套 MVT 找 c", "expansion:example（選配 MVT 數值例，已取）", "x² on [0,2]：avg slope 2、c=1∈(0,2)"),
    ("Example 4.3 — sin on [0,π/4]", "Corollary 應用 (i)", "seed（手稿 p.18）", "§C-9：拆為獨立 Example（選配，已取）"),
    ("Example 4.4 — e^x strictly increasing on ℝ", "Corollary 應用 (ii)；交棒 §4.5", "seed（手稿 pp.18–19）", "§C-7 補 e^x>0 依據、§C-6c every-[a,b]⟹ℝ；gate-1 math：x>0/x=0 精準化；prose：拆雙層括"),
    ("Closer — hand-off to §4.5", "節末", "expansion:summary（§C 交棒）", "<b>gate-2 run1 blocking 修</b>：裁去 §4.5 內容預覽（continuity/derivative），只留最小交棒"),
]

# ── gate-1: free 4-lens adversarial audit (workflow wf_39f59234): 0 blocking, 7 advisory ──
# (disp, lens-category, finding text, 裁決)
GATE1 = [
    ("applied", "math", "<b>math L3</b>　Example 4.4「for \\(x\\ge0\\) ... all terms positive」在 <code>x=0</code> 過度精確（彼時高次項為 0、非嚴格正），結論 <code>e^x&gt;0</code> 仍對。legacy 寫法為「positive when \\(x\\ge0\\) by direct inspection」。改：<code>x&gt;0</code> 每項正、<code>x=0</code> 取 <code>e^0=1&gt;0</code> 分述。", "已套（精準化、對齊 legacy）"),
    ("kept", "faithfulness", "<b>faith L4</b>　Theorem 4.10 略去手稿的「continuous」前提。但 Thm A 證明（雙單邊極限）<b>不用</b>連續性，這是更銳利且正確的陳述，且 signed legacy（thm:interior-extrema, line 573）亦只寫「defined on [a,b]」。非 drift、非弱化。", "保留（更銳利、對賬 legacy；非 finding）"),
    ("kept", "direction-conformance", "<b>dir L3</b>　Strategy 4.2 加了 <code>√x</code> on [0,1] 的正面旁白（端點垂直切線仍 fair game），brief 未逐字列出。但僅一句、已解、數學正確，且<b>直接服務 brief 指派的 closed/open 不對稱</b>——屬 strategy 自身範圍內的 enrichment，非越界；auditor 亦建議保留。", "保留（服務 mandated 不對稱、taste）"),
    ("kept", "direction-conformance", "<b>dir L4</b>　收尾與 Remark 4.4 各有一句 forward-mention 觸及 do-not-write 清單（ln x／Taylor）。經查皆為<b>描述性 forward-fence</b>（「下節將…」「日後…」），非本節實作，且為 brief <b>明令的交棒</b>；記錄以示已查核並 cleared。（註：gate-2 後續指出收尾<b>越界程度</b>仍偏多——見 gate-2，已另修。）", "保留（fence 屬許可；越界部分由 gate-2 另行收斂）"),
    ("applied", "prose", "<b>prose L3</b>　Remark 4.4 階梯以兩個串接 which 描述，第二個 which 鄰接「equal endpoints」但意指 Rolle，強讀者可能瞬間誤判先行詞。拆成各自獨立子句。", "已套（可解析性）"),
    ("applied", "prose", "<b>prose L3</b>　Example 4.4 收尾括號內又含 em-dash 插語（boundedness），單句兩層中斷、認知負荷偏高。拆兩句、去一層巢狀。", "已套（降認知負荷）"),
    ("applied", "prose", "<b>prose L3</b>　Strategy 4.2 step 3「may use that such a c exists」省略受詞、首讀像未完構句。改「may rely on the existence of such a c, but not on any specific value」。", "已套（清晰度）"),
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

# lens summaries (verbatim verdict context from the 4-lens gate-1 workflow run)
LENS = [
    ("math fidelity", "盲算重算每一步並對賬 signed legacy §4.4（sec:rolle-and-mvt＋cor:monotonicity）：Thm 4.10 雙單邊極限符號（h&gt;0 商≤0→右極限≤0；h&lt;0 商≥0→左極限≥0；逼出 0）、Rolle Case 1/2（<b>Case 2 (ii) 用 X_m，已修手稿筆誤、對賬 legacy line 612</b>）、MVT 輔助 g（g(a)=g(b)=0、g'(c)=f'(c)−割線斜率）、Corollary 4.3 雙條（分母&gt;0、分子隨 f'(c) 號）、Example 4.2 x²(c=1)／4.3 sin／4.4 e^x（e^x&gt;0、every-[a,b]⟹ℝ 對 strict 成立）、EVT 黑箱用法、Figure 4.2 caption＝MVT 內容、Strategy 4.2 的 √x／|x| 算術——<b>全部正確，0 blocking</b>。唯一 advisory：Example 4.4 在 x=0 的措辭精準化（L3，已套）。"),
    ("seed/manuscript faithfulness", "對 seed（手稿 pp.11–18）忠實：完整階梯（Def→cos x→EVT 不證→Thm A→Rolle→MVT→Corollary→sin/e^x→『e^x strictly increasing』交棒）保序、無扭曲、無漏；兩處 [請查核] 修正皆正確落地（Case 2 (ii)=f(X_m)&lt;f(a)；Corollary 雙條補 strict）；所有超出 seed 的 addition 皆對映 ③-approved 清單（history／Figure 4.2／Strategy 4.2／Remark 4.4／Example 4.2／caution／e^x&gt;0／every-[a,b]⟹ℝ）。<b>0 blocking</b>；唯一記錄為 L4 非 finding（Thm 4.10 略 continuous＝更銳利、對賬 legacy）。"),
    ("direction-conformance", "對 ③-approved brief 全守：(A) 覆蓋——4 定理階梯（EVT 不證＋Thm A/Rolle/MVT 全證）、Definition 4.3＋cos x、Figure 4.2、Strategy 4.2（含 |x| 反例＋closed/open 不對稱）、Corollary 4.3 雙條、Case-2 修、e^x&gt;0 一行、Thm-A interior caution、every-[a,b]⟹ℝ note，<b>及全部四項選配</b>（history／Remark 4.4 立框／Example 拆 4.3-4.4／MVT 數值 Example 4.2）皆在且 scope 正確；(B) do-not-write 全守（無 EVT 證、無 ln x 建構、無 Taylor/L'Hôpital 實作、(e^x)' 僅援引、單調性走 MVT 非積分、無 concavity、無自創 exercise、無過度展開）。<b>0 blocking</b>、2 非 blocking 觀察。"),
    ("prose / readability", "U1–U5 全達（每個 formal result 前皆有動機；Definition 4.3 配 Informally gloss；reduction 步步有 because/since/so 橋接；無術語先用後定義）；證明密集節的連接組織（opener、定理間橋、Remark 4.4 綜述、Strategy、worked-example 解、closer）承重良好。<b>易懂性 0 blocking、prose gate 通過</b>；3 advisory 全 polish（1 tighten＋2 optional，皆已套）。house-rule 保護項（階梯重複、MVT 復現、連接詞、we 語氣）不報。"),
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
    "<div class='note pass'><b>裁決：<span class='zero'>0 blocking → 通過</span></b>　·　4 lens 平行對抗審（workflow <code>wf_39f59234</code>）全收斂（math／faithfulness／direction／prose 各 0 blocking）；"
    f"共 7 advisory（{n_applied} 已套、{n_kept} 保留）。math 盲算重算對賬 legacy §4.4／faithfulness 對 seed／direction 對 brief／prose house rules，每個 blocking 候選 refute-by-default 對抗複驗（本輪 0 candidates）。"
    "修完回歸驗證：render 0 MathJax err／22 頁／0 overflow／0 dangling ref。</div>"
    "<h2>四 lens 裁決（全 0 blocking）</h2>" + lens_html +
    "<h2>審核對象（已寫入單元）</h2>" + units_table() +
    f"<h2>裁決逐條（7 advisory：{n_applied} 已套、{n_kept} 保留）</h2>" + "".join(g1_cards))

(HERE / "REVIEW-ch04_s44-gate1.html").write_text(
    doc("§4.4 — gate 1（Claude 4-lens 對抗審）審核稿",
        "第一道閘（免費）：Claude 4-lens 對抗式稽核（workflow，每 blocking 候選 refute-by-default 複驗）。blocking = math／faithfulness／direction-conformance；格式 nit = advisory。§4.4（全章最重節，主風險＝證明階梯紮實度），2026-06-21。",
        g1_body, "REVIEW-s44.gen.py", "REVIEW-ch04_s44-gate2.html"), encoding="utf-8")

# ── gate 2 (Codex gpt-5.5 xhigh; result_s44.json run1 + _r2.json run2) ──
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
    return "".join(out) or "<p class='lede'>（無 findings — 0 blocking／0 advisory）</p>"

r1f = run1.get("findings", [])
r2f = run2.get("findings", [])
g2_body = (
    "<div class='note pass'><b>最終：<span class='zero'>run 2 converged（0 blocking）</span></b>　·　"
    f"run 1 出 <span class='blkw'>1 blocking</span>（direction-conformance：收尾越界預覽 §4.5 的 continuity／derivative 內容）→ 裁去多餘預覽、只留最小交棒 → <b>run 2 converged 0 finding</b>（與 §4.1／§4.2 同型：run1 blocking→run2 clean）。"
    "停在一次乾淨 audit。修後回歸 render 0 err／22 頁／0 overflow。</div>"
    "<div class='note warn'><b>run 1 摘要：</b>" + esc(run1.get("summary", "")) + "</div>"
    "<p class='lede'>原始裁決檔（計費產物）：<code>result_s44.json</code>（run1）／<code>result_s44_r2.json</code>（run2）；prompt：<code>prompt_s44.txt</code>（<code>build_prompt_s44.py</code> 產，74.7KB）。模型 Codex <code>gpt-5.5</code>／reasoning <code>xhigh</code>、唯讀 sandbox、<code>--output-schema schema.json</code>、prompt 由 Bash <code>&lt; file</code> 餵原始 UTF-8。tokens：run1 ≈ 48.1k＋run2 ≈ 54.5k ≈ 102.6k。</p>"
    "<h2>審核對象（已寫入單元）</h2>" + units_table() +
    f"<h2>run 1 裁決（{len(r1f)} blocking → 已修）</h2>" + g2_cards(r1f) +
    f"<h2>run 2 裁決（converged：{str(run2.get('converged')).lower()}，{len(r2f)} finding）</h2>"
    "<div class='note pass'>" + esc(run2.get("summary", "")) + "</div>" + g2_cards(r2f))
(HERE / "REVIEW-ch04_s44-gate2.html").write_text(
    doc("§4.4 — gate 2（Codex gpt-5.5 xhigh）審核稿",
        "第二道閘（計費，使用者同意；含 run2）：Codex CLI 唯讀 reviewer、<code>--output-schema</code> 結構化輸出。§4.4 run1 1 blocking（§4.5 scope leak）→ 修 → run2 converged。2026-06-21。",
        g2_body, "REVIEW-s44.gen.py", "REVIEW-ch04_s44-gate1.html"), encoding="utf-8")

print(f"wrote REVIEW-ch04_s44-gate1.html + REVIEW-ch04_s44-gate2.html "
      f"(units={len(UNITS)} gate1={len(GATE1)}: {n_applied} applied / {n_kept} kept; "
      f"g2r1 findings={len(r1f)} blocking={sum(1 for f in r1f if f.get('blocking'))}; "
      f"g2r2 findings={len(r2f)} converged={run2.get('converged')})")

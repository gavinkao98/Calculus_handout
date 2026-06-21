#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the §4.3 gate-1 + gate-2 audit reports as standalone HTML.

  REVIEW-ch04_s43-gate1.html  — gate 1: free 4-lens adversarial audit (Claude)
  REVIEW-ch04_s43-gate2.html  — gate 2: Codex gpt-5.5 xhigh (reads result_s43.json)

House form mirrors REVIEW-s42.gen.py. Self-contained: MathJax CDN, an "audited units"
provenance table, the gate verdict, finding cards. §4.3 gate-2 converged on run 1 (no r2).
Run:  python REVIEW-s43.gen.py
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
run1 = json.loads((HERE / "result_s43.json").read_text(encoding="utf-8"))

def esc(s):
    return html.escape(str(s), quote=False)

# ── audited units (compact provenance) ──
UNITS = [
    ("§4.3 opener (Ch2 cross-ref)", "節首動機散文", "expansion:intuition（D-redundancy；cross-ref Ch2 informal、不動 Ch2）", "gate-1 prose G1-2：末句冒號處拆兩句"),
    ("Difference-quotient setup", "子節 The difference quotient", "seed（手稿 p.10）；expansion:formula", "用 Thm 4.7 指數律因式分解、化約到 lim(e^h−1)/h"),
    ("Proposition 4.2 + Proof（bound）", "|（e^h−1)/h − 1| ≤ |h|", "seed Note（手稿 p.11）", "§C-1 fill：bracket≤1 用 n!≥2^{n−1} 幾何比較＋Strategy 4.1 回指（§C-5）"),
    ("Remark 4.3（explicit rate）", "Prop 4.2 之後", "expansion:intuition（brief §C；legacy 有對應 remark）", ""),
    ("Theorem 4.8 + Proof", "d/dx e^x = e^x", "seed（手稿 p.11）", "gate-1／gate-2 對賬 legacy §4.3 全等"),
    ("Corollary 4.2 + Proof（higher derivatives）", "(e^x)^{(n)} = e^x", "expansion:intuition（§C-3；手稿無、legacy 有；迭代）", ""),
    ("Closer（application hook → §4.4）", "節末", "expansion:summary；§C-4 一句 hook + forward §4.4 monotonicity", "gate-1 direction F1：建模解改 e^{kt}（時間變數）；F2/G1-1：拆 hook 與 fence"),
]

# ── gate-1: free 4-lens adversarial audit: 0 blocking, advisory only ──
# (disp, lens-category, finding text, 裁決)
GATE1 = [
    ("applied", "direction-conformance", "<b>F1</b>　收尾把建模解寫成 <code>y = y(0)e^{kx}</code>（變數 x）——但 x 正是本節微分變數，瞬間讀起來像本節在處理 <code>e^{kx}</code> 這個函數物件；brief（承重直覺／§C-4）一律用時間變數 <code>t</code>。改 <code>y = y(0)e^{kt}</code>。", "已套（消除與微分變數撞義、對齊 brief）"),
    ("applied", "prose", "<b>G1-1／F2</b>　收尾首句過長：建模式 <code>y'=ky</code>＋解＋遞延＋em-dash 插語擠成一句，且 application hook 與 monotonicity forward-fence 黏連。改：逗號→冒號接 hook、分號→句點，拆成兩句，hook 與 fence 分離。", "已套（散文 G1-1 與 direction F2 同 locus、合併）"),
    ("applied", "prose", "<b>G1-2</b>　opener 末句三子句堆疊（re-derive honestly＋gain something＋冒號定義 bound）。冒號處拆成兩句，降首讀認知負荷。", "已套（可讀性）"),
    ("kept", "prose", "<b>G1-3</b>　子節首「a single algebraic move, and that move is the exponent law」重複「move」。agent 標 [Optional]／taste：此為刻意修辭強調（先懸念再揭曉指數律），語意無礙。", "保留（修辭強調、taste）"),
    ("kept", "prose", "<b>G1-4</b>　Remark 4.3 中句 em-dash 插語＋分號密度略高但語意正確、不誤導；屬 [Optional] polish。", "保留（readable、conf 低）"),
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

# lens summaries (verbatim verdict context from the 4-lens gate-1 run)
LENS = [
    ("math fidelity", "盲算重算每一步並對賬 signed legacy §4.3：差分商因式分解（Thm 4.7 指數律）、Prop 4.2 bound（index shift → Σ_{n≥2}h^{n−1}/n!、提 |h|、<b>bracket≤1 用 n!≥2^{n−1} 幾何比較得 Σ1/n!≤Σ1/2^{n−1}=1</b>、鏈確實給 ≤|h|）、Thm 4.8（squeeze→lim=1、提出 h-無關 e^x）、Cor 4.2 induction——<b>全部正確，0 blocking／0 advisory</b>。並指出本稿 bound 論證比 legacy（用 1/(1−|h|)≤2）<b>更自含乾淨</b>。"),
    ("direction-conformance", "對 ③-approved brief 全守：編號（Thm 4.8／Prop 4.2／Cor 4.2／Rem 4.3、不 mint 新 Definition）接 §4.1–§4.2 無撞號；「刻意不寫」fence 全守（無 chain rule／e^{kx} 物件、不碰 ln、無 Rolle/MVT 證、不動 Ch2 檔、ODE 僅一句 hook、不重證 §4.1/§4.2、無自創 exercise、不過度展開）；所有 ③-approved item（Ch2 cross-ref／bracket fill／Cor 4.2／hook／Strategy 4.1 nod）皆在且 scope 正確。<b>0 blocking、2 advisory</b>。"),
    ("seed/manuscript faithfulness", "對 seed（手稿 pp.10–11）忠實：完整鏈（差分商→化約 lim(e^h−1)/h→級數 Note bound≤|h| on (−½,½)→lim=1→d/dx e^x=e^x）保序、無扭曲、無漏；所有超出 seed 的 addition 皆對映 ③-approved 清單（Ch2 opener／bracket≤1 fill／Prop 4.2 naming／Rem 4.3／Cor 4.2／hook／Strategy 4.1 nod）；記號忠實（h 增量、e^h 級數、無新符號）。<b>0 finding</b>。"),
    ("prose / readability", "U1–U5 全達（formal result 前皆有動機、邏輯橋接齊全、無術語先用後定義、無新定義需拆解）；指數律因式分解與 bound 推導學生可循。<b>易懂性 0 blocking、prose gate 通過</b>；findings 全為 advisory polish（2 tighten 已套、2 optional 保留）。"),
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
    "<div class='note pass'><b>裁決：<span class='zero'>0 blocking → 通過</span></b>　·　math／faithfulness 兩 lens <b>0 finding</b>；"
    f"direction／prose 兩 lens 共 6 advisory（direction-F2 與 prose-G1-1 同 locus 合併 → {n_applied + n_kept} 張卡：{n_applied} 已套、{n_kept} 保留）。"
    "4 lens 平行對抗審（math 盲算重算對賬 legacy §4.3／faithfulness 對 seed／direction-conformance 對 brief／prose house rules），每個 blocking 候選 refute-by-default 對抗複驗（本輪 0 candidates）。"
    "修完回歸驗證：render 0 MathJax err／15 頁／0 overflow。</div>"
    "<h2>四 lens 裁決</h2>" + lens_html +
    "<h2>審核對象（已寫入單元）</h2>" + units_table() +
    "<h2>裁決逐條（6 advisory → " + str(n_applied + n_kept) + " 卡：" + str(n_applied) + " 已套、" + str(n_kept) + " 保留）</h2>" + "".join(g1_cards))

(HERE / "REVIEW-ch04_s43-gate1.html").write_text(
    doc("§4.3 — gate 1（Claude 4-lens 對抗審）審核稿",
        "第一道閘（免費）：Claude 4-lens 對抗式稽核。blocking = math／faithfulness／direction-conformance；格式 nit = advisory。§4.3（全章最短節，主風險＝過度展開），2026-06-21。",
        g1_body, "REVIEW-s43.gen.py", "REVIEW-ch04_s43-gate2.html"), encoding="utf-8")

# ── gate 2 (Codex gpt-5.5 xhigh; result_s43.json — converged on run 1, no r2) ──
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
    return "".join(out) or "<p class='lede'>（無 findings — run 1 即 converged、0 blocking／0 advisory）</p>"

r1conv = run1.get("converged")
g2_body = (
    f"<div class='note pass'><b>run 1 — converged：<span class='zero'>{str(r1conv).lower()}</span></b>"
    f"（<span class='zero'>0 blocking／0 finding</span>，run1 即收斂，無需第 2 run——§4.1/§4.2 皆 run1 有 blocking 需修，§4.3 為首個 run1 全清）。{esc(run1.get('summary',''))}</div>"
    "<p class='lede'>原始裁決檔（計費產物）：<code>result_s43.json</code>（run1）；prompt：<code>prompt_s43.txt</code>（<code>build_prompt_s43.py</code> 產）。模型 Codex <code>gpt-5.5</code>／reasoning <code>xhigh</code>、唯讀 sandbox、<code>--output-schema schema.json</code>、prompt 由 Bash <code>&lt; file</code> 餵原始 UTF-8。tokens used ≈ 33.7k。</p>"
    "<h2>審核對象（已寫入單元）</h2>" + units_table() +
    "<h2>run 1 裁決（converged，0 finding）</h2>" + g2_cards(run1.get("findings", [])))
(HERE / "REVIEW-ch04_s43-gate2.html").write_text(
    doc("§4.3 — gate 2（Codex gpt-5.5 xhigh）審核稿",
        "第二道閘（計費，使用者同意）：Codex CLI 唯讀 reviewer、<code>--output-schema</code> 結構化輸出。§4.3 run1 即 converged（0 blocking），停在一次乾淨 audit。2026-06-21。",
        g2_body, "REVIEW-s43.gen.py", "REVIEW-ch04_s43-gate1.html"), encoding="utf-8")

print(f"wrote REVIEW-ch04_s43-gate1.html + REVIEW-ch04_s43-gate2.html "
      f"(units={len(UNITS)} gate1={len(GATE1)}: {n_applied} applied / {n_kept} kept; "
      f"g2r1 findings={len(run1.get('findings',[]))} converged={run1.get('converged')})")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the §3.2 A1 (CONTENT_METHODOLOGY §8) alignment sign-off HTML.

One-shot generator in the shape of build_s32_review_html.py: the verdict data
lives in this file, running it once emits the standalone review page.

    python video/content_scripts/_audit/_gen/build_s32_a1_alignment_html.py

Output: video/content_scripts/_audit/REVIEW-ch03_chain_rule-s32-a1-alignment.html
(standalone, MathJax CDN, double-click to open).

Two authoring conventions used below:
  * «…»  marks a diverging span -> rendered as <mark>…</mark>.
  * Evidence strings are author-written HTML (they carry <b>/<code>/<br>), so
    they go through mark() only; plain-text fields go through esc().
  * Literal LaTeX / shell that must NOT be typeset sits in <code> — MathJax is
    configured to skip that tag.
"""
from __future__ import annotations

import html
from pathlib import Path

OUT = (Path(__file__).resolve().parents[1]
       / "REVIEW-ch03_chain_rule-s32-a1-alignment.html")

DATE = "2026-09-14"
DATE_LOCK = "2026-06-29"
LOCK_COMMIT = "b3860bc"
MAIN_TIP = "6c72163"
TEX = "handout/latex/src/ch03/chapter3.tex"
TEX_SHA = "sha256:acc1feed6c089bbe5745848af4a8483bb76392c55a474c25836e92c32f59cc0a"
OLD_SRC = "legacy/html_handout/fragments/ch03/sec-3-2.html"
OLD_SHA = "sha256:a1cd58673847ef4b2d245ff61f21f3e9e4201c03c05d77af1cf050517837c889"


def mark(s: str) -> str:
    """«…» -> <mark>…</mark>. For author-written HTML fragments."""
    return s.replace("«", "<mark>").replace("»", "</mark>")


def esc(s: str) -> str:
    """Full HTML escape + «…» marks. For plain-text fields only."""
    return mark(html.escape(s, quote=False))


# --------------------------------------------------------------------------
# (A) the two diff ranges
DIFF_COMMITS = [
    ("22b60fc", "純搬家",
     "fragment 由 <code>handout/fragments/</code> 移入 "
     "<code>legacy/html_handout/fragments/</code>，內容零改動。"),
    ("b2fa5ee", "平實化回填",
     "全書平實化回填 66 條；em-dash 密度 14.0 → 1.6 / 1000 字。本節大半變動行出自此 commit。"),
    ("4d7a632", "平實化／同義詞", "承上輪的語域整理。"),
    ("8e2ba61", "平實化／同義詞", "承上輪的語域整理。"),
    ("1f95298", "圖說精簡",
     "Fig 3.5 舊長圖說（含 10 條符號式）精簡成一句；Fig 3.6 舊四句圖說精簡成一句，"
     "並拆成 <code>remainder-tangent-1</code>／<code>-2</code> 兩檔。"),
]

# (B) formula-by-formula comparison
FORMULA_CHANGED = [
    ("<code>.tex:286–290</code>",
     r"P(x_{0}+h) = f\bigl(g(x_{0}+h)\bigr) = f(g(x_{0})) + m_{2}\bigl[m_{1} h + R_{1}(h)\bigr] "
     r"+ R_{2}\bigl(m_{1} h + R_{1}(h)\bigr)",
     "包進 <code>\\begin{aligned}…\\end{aligned}</code>，於 <code>&amp;=</code> 處加 "
     "<code>\\\\[2pt]</code> 折行"),
    ("<code>.tex:294–297</code>",
     r"P(x_{0}+h) = P(x_{0}) + \bigl(g'(x_{0})\,f'(g(x_{0}))\bigr) h + R_{3}(h), \qquad "
     r"R_{3}(h) = m_{2} R_{1}(h) + R_{2}\bigl(m_{1} h + R_{1}(h)\bigr)",
     "包進 <code>\\begin{aligned}…\\end{aligned}</code>，加 <code>\\\\[2pt]</code> 折行"),
]

FORMULA_DELETED = [
    r"f", r"h", r"h", r"x_{0}", r"x_{0}", r"x_{0}+h",
    r"g'(x_{0})\,h", r"f'(g(x_{0}))\,g'(x_{0})\,h",
    r"u_{0} = g(x_{0})", r"y_{0} = f(g(x_{0}))",
]

FORMULA_ADDED = [r"x \mapsto u \mapsto y"]

# (C) the 24 units
KLASS = {
    1: ("類 1", "零 diff", "k1"),
    2: ("類 2", "僅標點平實化", "k2"),
    3: ("類 3", "同義詞替換，主張不變", "k3"),
    4: ("類 4", "無直接對位／圖說精簡／裁決", "k4"),
}

# (id, locus-html, class, evidence-html)
UNITS = [
    ("intro", "（無直接對位——Section Gate 模板場）", 4,
     "純模板場，不引講義散文，沒有可跟改的對象。"),

    ("why_composition_is_missing", "<code>:209</code> 開節 para 1", 2,
     "<b>.tex 現行：</b>「Chapter 2 supplied rules for sums, products, and quotients«, but» "
     "not for <em>composition</em>, the operation of applying one function to the output of "
     "another.」<br>"
     "<b>lock 版：</b>「… and quotients «— but» not for composition …」<br>"
     "<b>旁白 <code>md:58</code>：</b>「We already built rules for sums, for products, for "
     "quotients «—» but never for composition」——主張全同，差的只有破折號語域。"),

    ("rates_multiply_intuition", "<code>:211</code> 開節 para 2（<code>fig:3.5</code> 所指）", 2,
     "<b>.tex 現行：</b>「the two magnifications stack«. The» composite scales \\(h\\) by the "
     "product \\(f'(g(x))\\,g'(x)\\).」，另於句首新增「«, pictured in Figure 3.5,»」"
     "（紙本 cross-ref，影片無對位）。<br>"
     "<b>lock 版：</b>「the two magnifications stack «— the» composite scales …」<br>"
     "<b>旁白 <code>md:84</code>：</b>「the two magnifications stack — the composite scales "
     "\\(h\\) by the product \\(f'(g(x))\\,g'(x)\\)」——數學逐字相同。"),

    ("chain_rule_statement", "<code>thm:3.3</code> @ <code>:215–219</code>", 1,
     "自 lock 起一個字沒動。陳述與 \\(P'(x_{0}) = f'(g(x_{0}))\\, g'(x_{0})\\) 零 diff。"),

    ("composed_mapping_figure", "<code>fig:3.5</code> @ <code>:220–223</code>", 4,
     "舊長圖說（含上表「刪 10 式」的全部符號式）被 <code>1f95298</code> 精簡為一句："
     "「local slope factors accumulate along \\(x \\mapsto u \\mapsto y\\)」。"
     "舊圖說所述事實原封保留在 <code>:211</code> 本文與圖本身，"
     "旁白（兩段 relay of stretches）所依賴的內容一條未失。"),

    ("leibniz_form", "<code>rem:3.2</code> @ <code>:224–230</code>（<code>:229</code>）", 3,
     "<b>.tex 現行 <code>:229</code>：</b>「not fractions with a common factor to «cancel»」<br>"
     "<b>lock 版：</b>「… a common factor to «strike out»」<br>"
     "<b>旁白 <code>md:162</code>：</b>「These are not fractions with a common factor to "
     "«strike out»」——同義詞，「mnemonic-not-proof」主張不變；Leibniz 式本身零 diff。"),

    ("decomposition_strategy",
     "<code>strat:3.1</code> @ <code>:231–242</code>（<code>:237</code>）", 3,
     "<b>.tex 現行 <code>:237</code>：</b>「treat the inside as a single block and «do not "
     "differentiate it yet»」<br>"
     "<b>lock 版：</b>「… as a single block and «leave it untouched for now»」<br>"
     "<b>旁白 <code>md:187–188</code>：</b>「treating the whole inside as a single block you "
     "«leave untouched for now»」——步驟 ①–⑤ 與兩個分解例全同。"),

    ("proof_strategy_bridge",
     "<code>:243–244</code>（<code>\\subsechead</code> ＋導言）", 4,
     "<b>裁決項 #8</b>——<code>.tex:244</code> 新增一句導航句。詳見下方專節；"
     "主對話裁決＝<b>不跟改</b>。"),

    ("remainder_form_definition",
     "<code>def:3.1</code> @ <code>:246–256</code>（informal gloss <code>:254</code>）", 3,
     "<b>定義體本身零 diff</b>（<code>:247</code> 敘述、<code>:249</code> "
     "\\(f(x_{0} + h) = f(x_{0}) + m h + R(h)\\)、\\(\\lim_{h \\to 0} R(h)/h = 0\\)、"
     "<code>:251</code> \\(m = f'(x_{0})\\)）。<br>"
     "<b>gloss <code>:254</code> 現行：</b>「an error \\(R(h)\\) that «shrinks» faster than "
     "\\(h\\) does«. The» tangent line is a good fit to first order」<br>"
     "<b>lock 版：</b>「… that «dies away» faster than \\(h\\) does «— the» tangent line …」<br>"
     "<b>旁白 <code>md:246</code>：</b>「an error $R(h)$ that «dies away» faster than "
     "$h$ itself」"),

    ("remainder_tangent_figure", "<code>fig:3.6</code> @ <code>:257–260</code>", 4,
     "舊四句圖說被 <code>1f95298</code> 精簡成一句，並把圖拆成 "
     "<code>remainder-tangent-1</code>／<code>-2</code> 兩格。"
     "旁白所需的幾何（切線貼合、\\(h\\) 減半時間隙縮得遠比 \\(h\\) 快、"
     "\\(R(h)/h \\to 0\\)）由 <code>:254</code> 的 informal gloss ＋兩格圖共同承載，未失。"),

    ("two_forms_equivalent",
     "<code>prop:3.3</code> @ <code>:263–265</code> ＋ Proof <code>:266–276</code>", 2,
     "<b>.tex 現行 <code>:264</code>：</b>「and the number \\(m\\) is the same in both«, namely» "
     "\\(f'(x_{0})\\).」<br>"
     "<b>lock 版：</b>「… the same in both «— namely» \\(f'(x_{0})\\).」<br>"
     "<b>Proof 本體（雙向論證、兩個 display）零 diff</b>，旁白逐行對位全數保留。"),

    ("proof_setup_substitution",
     "Proof of <code>thm:3.3</code>：lead-in <code>:277</code> ＋ <code>:279–299</code>", 3,
     "<b>.tex 現行 <code>:277</code>：</b>「each as a linear part plus a small remainder; "
     "«substituting the expansion for \\(g\\) into the one for \\(f\\)», the linear parts "
     "multiply … and everything left over «collects» into a single remainder.」<br>"
     "<b>lock 版：</b>「… «feeding one into the other», the linear parts multiply … "
     "everything left over «gathers» into a single remainder.」<br>"
     "<b>旁白未引述該 lead-in 句</b>；兩式 <code>:286–290</code>／<code>:294–297</code> "
     "改包 <code>aligned</code> 屬<b>純排版</b>，數學 token 逐字不變（見上方「改 2 式」）。"),

    ("proof_easy_piece", "<code>:303–304</code>", 1,
     "零 diff。拆兩塊、\\(m_{2} R_{1}(h)/h \\to 0\\)、"
     "附記 \\(m_{1} h + R_{1}(h) \\to 0\\) 全同。"),

    ("proof_delicate_choices", "<code>:305–311</code>（<code>:311</code>）", 2,
     "<code>:311</code> 把原本的破折號插入句拆成兩句（現行：「Now fix \\(h\\) … "
     "«Suppose first that» \\(m_{1} h + R_{1}(h) = 0\\).」）。"
     "\\(\\delta\\)／\\(\\alpha\\) 的選取（<code>:308</code>／<code>:309</code>）與 "
     "\\(R_{2}(0) = 0\\) 的推理<b>全等</b>，旁白 ε-δ 五步逐條仍對得上。"),

    ("proof_delicate_bound", "<code>:313–324</code>", 1,
     "零 diff。乘一除一分解、\\(\\varepsilon\\) 界、三角不等式、\\(\\alpha_{1}\\) 收尾至 "
     "\\((\\lvert m_{1} \\rvert + 1)\\varepsilon\\)、QED 全同。"),

    ("example_single_composition", "<code>ex:3.4</code> @ <code>:327–341</code>", 1,
     "零 diff。題目 \\(\\sqrt{1 + x^{2}}\\)／\\(\\sin(x^{2})\\)、解法、"
     "答案 \\(x/\\sqrt{1 + x^{2}}\\) 與 \\(2x\\cos(x^{2})\\)、"
     "以及結語（\\(2x\\) ＝ inner derivative）全同。"),

    ("caution_inner_derivative",
     "<code>envcaution</code> @ <code>:342–344</code>（<code>:343</code>）", 2,
     "<b>.tex 現行：</b>「… and forget the inner derivative«, writing» "
     "\\(\\frac{d}{dx}\\sin(g(x)) = \\cos(g(x))\\) instead of the correct "
     "\\(\\cos(g(x))\\cdot g'(x)\\).」<br>"
     "<b>lock 版：</b>「… the inner derivative «— writing» …」<br>"
     "後半句「The inner factor \\(g'(x)\\) — the \\(2x\\) in \\(\\sin(x^{2})\\) above — is "
     "never optional.」<b>連破折號都未動</b>，旁白直接對位。"),

    ("example_nested_three_layers",
     "<code>ex:3.5</code> @ <code>:346–361</code>（<code>:359</code>）", 2,
     "<b>.tex 現行 <code>:359</code>：</b>「Their product is the derivative«. The» slopes "
     "multiply down the chain, just as Figure 3.5 pictures.」<br>"
     "<b>lock 版：</b>「Their product is the derivative «— the» slopes multiply …」<br>"
     "三層推導與三個因子 \\(\\tfrac12 u^{-1/2}\\)、\\(2\\sin x\\)、\\(\\cos x\\) 零 diff。"),

    ("example_chain_times_quotient",
     "<code>ex:3.6</code> @ <code>:363–381</code>（<code>:379</code>）", 3,
     "<code>:379</code> 結語改寫為兩句（現行：「The chain rule does not finish the computation "
     "by itself. It requires the derivative of the inside, and here that derivative is itself "
     "a quotient-rule computation.」）。"
     "內導 \\(3/(x + 2)^{2}\\)（<code>:373</code>）與答案 "
     "\\(3 / \\bigl(2\\sqrt{x - 1}\\,(x + 2)^{3/2}\\bigr)\\)（<code>:377</code>）<b>未動</b>。<br>"
     "旁白 <code>md:528</code>「Sometimes the inner derivative is «a small problem of its own»」"
     "——該句在 <code>.tex</code> 已被刪，但其主張完整保留在 <code>:379</code>。"),

    ("example_chain_times_product",
     "<code>ex:3.7</code> @ <code>:383–401</code>（<code>:391</code>）", 2,
     "<b>.tex 現行 <code>:391</code>：</b>「since \\(\\cos^{2} x = [\\cos x]^{2}\\) is a "
     "composition «with» outer function \\((\\,\\cdot\\,)^{2}\\) «and» inner function "
     "\\(\\cos x\\):」<br>"
     "<b>lock 版：</b>「… is a composition «— outer function \\((\\,\\cdot\\,)^{2}\\), "
     "inner function \\(\\cos x\\)»:」<br>"
     "積法則 ＋ 鏈式的三步推導與答案 "
     "\\(y' = 2x\\cos^{2} x - 2(1 + x^{2})\\sin x\\cos x\\) 零 diff。"),

    ("example_leibniz_rates",
     "<code>ex:3.8</code> @ <code>:403–412</code>"
     "（<code>:404</code>／<code>:407</code>／<code>:411</code>）", 3,
     "<code>:404</code> 破折號改「«since» urchins eat kelp」；"
     "<code>:407</code>「«Determine» the sign of each link first」← lock「«Read off» each link …」；"
     "<code>:411</code> 結語重組。<br>"
     "kelp／urchin／otter 的符號推理（\\(dK/dU &lt; 0\\)、\\(dU/dO &lt; 0\\)）、"
     "Leibniz 串接 \\(\\frac{dK}{dO} = \\frac{dK}{dU}\\cdot\\frac{dU}{dO}\\) 與結論 "
     "\\(dK/dO &gt; 0\\) <b>未動</b>。旁白 <code>md:589</code> 仍作「«Read off» each link」。"),

    ("toward_section_3_3", "<code>:414</code> 收尾散文", 4,
     "<b>裁決項 #22</b>——比喻（「the key that unlocks …」）被刻意拿掉。詳見下方專節；"
     "主對話裁決＝<b>不跟改</b>。"),

    ("recap", "全節凝煉（無單一對位 locus）", 4,
     "5 條 takeaway 分別溯源至 <code>thm:3.3</code>（零 diff）、<code>rem:3.2</code> 的 Leibniz 式"
     "（式本身零 diff）、<code>strat:3.1</code>（步驟零 diff）、<code>envcaution</code>"
     "（後半句零 diff）、<code>def:3.1</code>（定義體零 diff）——<b>全部落在零 diff 的環境內</b>。"),

    ("outro", "（無直接對位——節末品牌字卡模板場）", 4,
     "純模板場，不引講義散文。"),
]

# (D) six register-drift spots
REGISTER_DRIFT = [
    ("a", "<code>md:619</code>", "it becomes «a key. It unlocks»",
     "<code>.tex:414</code> 改為「It gives us derivatives we could not otherwise reach」"
     "（比喻拿掉）",
     "＝裁決項 #22（見上）"),
    ("b", "<code>md:528</code>", "«a small problem of its own»",
     "<code>.tex:379</code> 已刪該句",
     "主張（內導本身是商法則計算）仍完整在 <code>:379</code>"),
    ("c", "<code>md:164</code>", "a common factor to «strike out»",
     "<code>.tex:229</code> → 「to «cancel»」",
     "同義詞；mnemonic-not-proof 主張不變"),
    ("d", "<code>md:188</code>", "you «leave untouched for now»",
     "<code>.tex:237</code> → 「«do not differentiate it yet»」",
     "同義詞；步驟語義不變"),
    ("e", "<code>md:589</code>", "«Read off» each link",
     "<code>.tex:407</code> → 「«Determine» the sign of each link first」",
     "同義詞；符號推理不變"),
    ("f", "<code>md:246</code>", "«dies away» faster than $h$ itself",
     "<code>.tex:254</code> → 「«shrinks» faster than \\(h\\) does」",
     "同義詞；\\(R(h)/h \\to 0\\) 的意思不變"),
]

# (7) not done this round
NOT_DONE = [
    ("24 處各單元的 <code>source:</code> 欄位不改指 <code>.tex</code>",
     "24 個單元的 <code>source:</code> 仍寫 <code>chapter3-print-standalone.html §3.2 · …</code>。"
     "閘（<code>schema.py</code>／<code>make.py</code>／<code>derive_spoken.py</code>）"
     "<b>不讀這個欄位</b>，只讀 header 的 <code>source_rev</code> stamp；"
     "且該 standalone 仍在 <code>legacy/html_handout/</code> 可回溯。"
     "屬 discoverability（根 <code>CLAUDE.md</code> 四級 review 的第②級），非矛盾，"
     "不在本輪外科範圍內。"),
    ("storyboard <code>video/storyboards/ch03_chain_rule.yml</code> 不動",
     "跟改 0 筆 ⇒ 沒有任何 <code>say</code>／payload 需要同步。本步<b>零跟改</b>，"
     "storyboard 不需要動。"),
    ("scoped NFA 不跑（A3／A4 不重跑）",
     "NFA 觸發的硬條件是<b>數學記號有改動</b>。上方 (B) 已逐式證明本文數學零改動"
     "（改 2 式純排版、刪 10 式全來自被精簡的 Fig 3.5 舊圖說、增 1 式為新圖說），"
     "故不觸發；旁白也因此不需重念。"),
]


# --------------------------------------------------------------------------
def unit_rows() -> str:
    out = []
    for i, (uid, locus, k, ev) in enumerate(UNITS, 1):
        label, desc, cls = KLASS[k]
        out.append(
            '<tr><td class="n">%02d</td>'
            '<td class="uid"><code>%s</code></td>'
            '<td class="loc">%s</td>'
            '<td class="verdict"><span class="pill-no">不跟改</span></td>'
            '<td class="kls"><span class="k %s">%s</span>'
            '<span class="kdesc">%s</span></td>'
            '<td class="ev">%s</td></tr>'
            % (i, esc(uid), mark(locus), cls, label, esc(desc), mark(ev)))
    return "\n".join(out)


def klass_counts() -> str:
    counts = {1: 0, 2: 0, 3: 0, 4: 0}
    for _, _, k, _ in UNITS:
        counts[k] += 1
    out = []
    for k in (1, 2, 3, 4):
        label, desc, cls = KLASS[k]
        out.append('<div class="cnt %s"><b>%d</b><span class="cl">%s</span>'
                   '<span class="cd">%s</span></div>' % (cls, counts[k], label, esc(desc)))
    return "".join(out)


def diff_rows() -> str:
    return "\n".join(
        '<tr><td><code>%s</code></td><td class="kind">%s</td><td>%s</td></tr>'
        % (c, esc(kind), what) for c, kind, what in DIFF_COMMITS)


def formula_changed_rows() -> str:
    return "\n".join(
        '<tr><td class="loc">%s</td><td class="math">\\[%s\\]</td>'
        '<td class="note">%s<br><span class="ok">數學 token 逐字不變</span></td></tr>'
        % (loc, tex, note) for loc, tex, note in FORMULA_CHANGED)


def drift_rows() -> str:
    return "\n".join(
        '<tr><td class="n">(%s)</td><td class="loc">%s</td><td class="ev">%s</td>'
        '<td class="ev">%s</td><td class="ev">%s</td>'
        '<td class="verdict"><span class="pill-no">不跟改</span></td></tr>'
        % (tag, where, mark(quote), mark(texside), mark(why))
        for tag, where, quote, texside, why in REGISTER_DRIFT)


def not_done_cards() -> str:
    return "\n".join(
        '<div class="card"><h3 style="margin-top:0">%s</h3>'
        '<p style="margin:.2em 0 0">%s</p></div>' % (t, b) for t, b in NOT_DONE)


# --------------------------------------------------------------------------
HTML = r"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>§3.2 A1 §8 對齊 — sign-off</title>
<script>
window.MathJax = {
  tex: { inlineMath: [['$','$'], ['\\(','\\)']],
         displayMath: [['$$','$$'], ['\\[','\\]']] },
  svg: { fontCache: 'global' },
  options: { skipHtmlTags: ['script','noscript','style','textarea','code'] }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
<style>
:root {
  --bg:#f4f6fb; --card:#ffffff; --alt:#f8fafd; --ink:#18202f; --muted:#5c6b84;
  --line:#d8e0ee; --navy:#0b1526; --navy-ink:#e8eefb;
  --accent:#a8701f; --accent-bg:#fdf5e6;
  --ok:#1d6b45; --ok-bg:#e7f4ec; --ask:#7a2f6b; --ask-bg:#fbecf7;
  --warn:#8a4b12; --warn-bg:#fdf0e0;
  --mark:#ffe9a8; --mark-ink:#4a3400;
  --k1:#1d6b45; --k1b:#e7f4ec; --k2:#1b5c86; --k2b:#e5f1f9;
  --k3:#7a4b12; --k3b:#fbf0df; --k4:#5a4a7a; --k4b:#efeaf8;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg:#10151f; --card:#18202e; --alt:#1c2433; --ink:#e6ecf7; --muted:#a3b1c9;
    --line:#2b3648; --navy:#060c16; --navy-ink:#e8eefb;
    --accent:#e8b768; --accent-bg:#2a2113;
    --ok:#7fd6a6; --ok-bg:#14301f; --ask:#e5a6d6; --ask-bg:#2c1628;
    --warn:#efb277; --warn-bg:#2e2113;
    --mark:#6a5210; --mark-ink:#ffeec2;
    --k1:#7fd6a6; --k1b:#14301f; --k2:#8cc7ee; --k2b:#12283a;
    --k3:#e8b768; --k3b:#2a2113; --k4:#bfaee8; --k4b:#241e36;
  }
}
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink);
  font:15px/1.7 -apple-system,"Segoe UI",Roboto,"Noto Sans TC","PingFang TC",sans-serif; }
.wrap { max-width:1180px; margin:0 auto; padding:34px 20px 90px; }
code { font:13px/1.5 ui-monospace,"SF Mono",Consolas,monospace;
  background:var(--accent-bg); color:var(--accent); padding:1px 5px; border-radius:4px;
  word-break:break-word; }
mark { background:var(--mark); color:var(--mark-ink); padding:0 3px; border-radius:3px;
  font-weight:600; }
em { font-style:italic; }
header.top { background:var(--navy); color:var(--navy-ink); border-radius:16px;
  padding:28px 30px; margin-bottom:20px; }
header.top .eyebrow { font:600 12px/1.5 ui-monospace,monospace; letter-spacing:.14em;
  text-transform:uppercase; color:#89a8dd; }
header.top h1 { margin:.4em 0 .25em; font-size:27px; line-height:1.35; color:#fff; }
header.top .lede { font-size:17px; color:#fff; font-weight:600; }
header.top .meta { display:flex; flex-wrap:wrap; gap:6px 22px; margin-top:16px;
  font:13px/1.7 ui-monospace,monospace; color:#a9bfe4; }
header.top code { background:#ffffff1f; color:#cfe0ff; }
h2 { font-size:19px; margin:40px 0 4px; padding-bottom:8px;
  border-bottom:2px solid var(--line); }
h2 .num { color:var(--accent); font:700 14px/1 ui-monospace,monospace; margin-right:9px; }
h3 { font-size:16px; margin:24px 0 8px; }
h4 { font-size:14px; margin:20px 0 6px; color:var(--muted);
  text-transform:uppercase; letter-spacing:.06em; }
p.sub { color:var(--muted); margin:.4em 0 1em; font-size:14px; }
.card { background:var(--card); border:1px solid var(--line); border-radius:12px;
  padding:18px 22px; margin:14px 0; }
.callout { border-left:4px solid var(--accent); background:var(--accent-bg);
  border-radius:0 10px 10px 0; padding:14px 18px; margin:16px 0; }
.callout.ok { border-left-color:var(--ok); background:var(--ok-bg); }
.callout.ask { border-left-color:var(--ask); background:var(--ask-bg); }
table { width:100%; border-collapse:collapse; margin:12px 0; background:var(--card);
  border:1px solid var(--line); border-radius:10px; overflow:hidden; }
th { background:var(--navy); color:var(--navy-ink); text-align:left; padding:10px 12px;
  font:600 13px/1.4 -apple-system,"Segoe UI","Noto Sans TC",sans-serif;
  vertical-align:bottom; }
th code { background:#ffffff1f; color:#cfe0ff; }
td { padding:11px 12px; border-top:1px solid var(--line); vertical-align:top;
  font-size:13.5px; line-height:1.7; }
tr:nth-child(even) td { background:var(--alt); }
td.n { font:600 12px/1.7 ui-monospace,monospace; color:var(--muted); white-space:nowrap; }
td.uid code { font-size:12.5px; }
td.loc { font-size:12.5px; color:var(--muted); }
td.math { font-size:12px; }
td.kind { white-space:nowrap; font-weight:600; }
.scroll { overflow-x:auto; }
.pill-no { display:inline-block; background:var(--ok-bg); color:var(--ok);
  border:1px solid var(--ok); border-radius:20px; padding:2px 10px; white-space:nowrap;
  font:600 12px/1.7 -apple-system,"Noto Sans TC",sans-serif; }
.k { display:inline-block; border-radius:5px; padding:1px 7px; white-space:nowrap;
  font:600 12px/1.7 ui-monospace,monospace; }
.k.k1 { color:var(--k1); background:var(--k1b); }
.k.k2 { color:var(--k2); background:var(--k2b); }
.k.k3 { color:var(--k3); background:var(--k3b); }
.k.k4 { color:var(--k4); background:var(--k4b); }
.kdesc { display:block; color:var(--muted); font-size:11.5px; margin-top:3px; }
.counts { display:flex; flex-wrap:wrap; gap:12px; margin:14px 0; }
.cnt { flex:1 1 190px; border-radius:10px; padding:13px 16px; border:1px solid var(--line); }
.cnt b { display:block; font-size:26px; line-height:1.2; color:inherit; }
.cnt .cl { display:block; font:600 12px/1.6 ui-monospace,monospace; color:inherit; }
.cnt .cd { display:block; color:var(--muted); font-size:11.5px; margin-top:2px; }
.cnt.k1 { color:var(--k1); background:var(--k1b); }
.cnt.k2 { color:var(--k2); background:var(--k2b); }
.cnt.k3 { color:var(--k3); background:var(--k3b); }
.cnt.k4 { color:var(--k4); background:var(--k4b); }
.quote { border-left:3px solid var(--line); padding:8px 0 8px 14px; margin:10px 0;
  font-size:13.5px; }
.quote .lab { display:block; font:600 11.5px/1.7 ui-monospace,monospace; color:var(--muted);
  letter-spacing:.05em; text-transform:uppercase; }
.quote.new { border-left-color:var(--warn); background:var(--warn-bg);
  border-radius:0 8px 8px 0; padding:10px 14px; }
.ba2 { display:grid; grid-template-columns:1fr; gap:10px; margin:10px 0; }
@media (min-width:860px) { .ba2 { grid-template-columns:1fr 1fr; } }
.ba { border:1px solid var(--line); border-radius:10px; padding:12px 14px;
  background:var(--card); min-width:0; }
.ba .lab { display:block; font:600 11.5px/1.7 ui-monospace,monospace; color:var(--muted);
  letter-spacing:.06em; text-transform:uppercase; margin-bottom:6px; }
.ba pre { margin:0; white-space:pre-wrap; word-break:break-word;
  font:12px/1.75 ui-monospace,"SF Mono",Consolas,monospace; color:var(--ink); }
.ba pre code { background:none; color:inherit; padding:0; font-size:12px; }
ul.tight { margin:.5em 0; padding-left:1.3em; }
ul.tight li { margin:.4em 0; }
.ok { color:var(--ok); font-weight:600; }
.qbox { background:var(--card); border:2px solid var(--ask); border-radius:12px;
  padding:18px 22px; margin:14px 0; }
.qbox .qn { font:700 13px/1.6 ui-monospace,monospace; color:var(--ask); letter-spacing:.08em; }
.qbox .qt { font-size:16px; font-weight:600; margin:6px 0; }
footer { margin-top:48px; padding-top:16px; border-top:1px solid var(--line);
  color:var(--muted); font-size:12.5px; line-height:1.8; }
</style></head><body><div class="wrap">

<header class="top">
  <div class="eyebrow">NTU 微積分影片產線 · §3.2 ch03_chain_rule · A1（CONTENT_METHODOLOGY §8 對齊）</div>
  <h1>§3.2 A1 §8 對齊——24 單元全部不跟改，A1 只剩換 stamp</h1>
  <div class="lede">跟改 0 筆。本輪實際寫入的改動＝內容稿 header 的兩行（權威來源＋source_rev）。</div>
  <div class="meta">
    <span>日期：%%DATE%%</span>
    <span>依據：lock <code>%%LOCK%%</code>（%%DATE_LOCK%%）→ main tip <code>%%TIP%%</code></span>
    <span>講義源：<code>%%TEX%%</code> §3.2（<code>:208–416</code>）</span>
  </div>
</header>

<div class="callout ok">
  <b>一句話結論。</b>lock（%%DATE_LOCK%%，commit <code>%%LOCK%%</code>）至今 §3.2 的講義改動，
  全部落在<b>標點平實化／同義詞替換／圖說精簡／紙本動線</b>四類；本文
  （<code>thm:3.3</code>／<code>def:3.1</code>／<code>prop:3.3</code>／<code>strat:3.1</code>／
  <code>envcaution</code>／<code>ex:3.4</code>–<code>ex:3.8</code>／full ε-δ 證明）
  <b>零數學改動</b>。24 個單元逐一判定皆為「不跟改」，因此 A1 實質只剩換 stamp——
  storyboard 不需同步、旁白不需重念、scoped NFA 不需重跑。
</div>

<h2><span class="num">1</span>為什麼可以這樣判</h2>
<p class="sub">以下 (A)(B) 是全篇的承重證據：(A) 圈出講義端到底動了哪些 commit、動了多少；
(B) 把 lock 版與現行版的<b>每一條數學式</b>抽出來逐條比對，證明改動不碰數學。</p>

<h3>(A) 兩段 diff 的範圍</h3>
<div class="card">
  <ul class="tight">
    <li><b>第一段 diff（HTML fragment 自身）：</b>lock commit <code>%%LOCK%%</code> 當時的 fragment
        路徑＝<code>handout/fragments/ch03/sec-3-2.html</code>（現已搬到 <code>%%OLDSRC%%</code>）。
        lock 版 <b>280 行</b> → 現行 <b>291 行</b>，<b>diff 59 個變動行</b>，
        出自下表五個 commit。</li>
    <li><b>第二段 diff（HTML → LaTeX 轉換）：</b><code>%%TEX%%</code> 的 <code>:208–416</code>
        與現行 HTML fragment 做 prose-only 正規化比對<b>逐字相同</b>
        ⇒ <code>ceb92f9</code>／<code>3ebbcc8</code> 的轉換<b>沒帶進任何散文改動</b>，
        只做了 <code>\label</code> 語意化與 Fig 3.6 拆兩檔。</li>
  </ul>
  <div class="scroll"><table>
    <tr><th style="width:100px">commit</th><th style="width:130px">性質</th><th>內容</th></tr>
    %%DIFFROWS%%
  </table></div>
</div>

<h3>(B) 數學式逐條比對（最承重的證據）</h3>
<p class="sub">對 lock 版與現行 HTML fragment 抽出所有 <code>\(…\)</code> 與 <code>\[…\]</code>：
<b>lock 213 式、現行 204 式</b>。差異只有三類，且數目自洽：<code>213 − 10 + 1 = 204</code> ✓</p>

<div class="counts">
  <div class="cnt k3"><b>2</b><span class="cl">改</span>
    <span class="cd">純排版，數學 token 逐字不變</span></div>
  <div class="cnt k4"><b>10</b><span class="cl">刪</span>
    <span class="cd">全部來自被精簡的 Fig 3.5 舊圖說</span></div>
  <div class="cnt k2"><b>1</b><span class="cl">增</span>
    <span class="cd">新 Fig 3.5 圖說</span></div>
  <div class="cnt k1"><b>0</b><span class="cl">本文數學改動</span>
    <span class="cd">Thm／Def／Prop／Strategy／Caution／Ex／證明</span></div>
</div>

<h4>改 2 式——純排版</h4>
<div class="scroll"><table>
  <tr><th style="width:120px">locus</th><th>式</th><th style="width:280px">改了什麼</th></tr>
  %%FCHANGED%%
</table></div>

<h4>刪 10 式——全部出自 <code>1f95298</code> 精簡掉的 Fig 3.5 舊圖說</h4>
<div class="card">
  <p style="margin:.2em 0 .7em; font-size:15px">%%FDELETED%%</p>
  <p class="sub" style="margin:0">這些都是舊圖說裡逐個點名座標與增量的碎片式，
  <b>不是本文推導的任何一步</b>。新圖說改用一條式子概括（見下），資訊未失。</p>
</div>

<h4>增 1 式——新 Fig 3.5 圖說（<code>.tex:222</code>）</h4>
<div class="card">
  <p style="margin:.2em 0; font-size:15px">%%FADDED%%</p>
  <p class="sub" style="margin:.5em 0 0">圖說全文：「The chain rule as a composed mapping:
  local slope factors accumulate along \(x \mapsto u \mapsto y\).」</p>
</div>

<div class="callout ok">
  <b>(B) 的結論：</b><code>thm:3.3</code>、<code>def:3.1</code>、<code>prop:3.3</code>、
  <code>strat:3.1</code>、<code>envcaution</code>、<code>ex:3.4</code>–<code>ex:3.8</code>
  與 full ε-δ 證明，<b>一條數學式都沒變</b>。旁白承載的全部數學內容因此原封有效，
  這也是下方「不跑 scoped NFA」的依據。
</div>

<h2><span class="num">2</span>24 列逐單元判定</h2>
<p class="sub">判定欄一律「不跟改」；類別欄指出理由屬四類中的哪一類。
證據欄以 <mark>標記</mark> 標出 <code>.tex</code> 與內容稿現行句的分歧處。</p>

<div class="counts">%%KCOUNTS%%</div>

<div class="scroll"><table>
  <tr><th style="width:34px">#</th><th style="width:180px">單元 id</th>
      <th style="width:170px">對位 <code>.tex</code> locus</th>
      <th style="width:78px">判定</th><th style="width:145px">類別</th><th>證據</th></tr>
  %%UROWS%%
</table></div>

<div class="callout">
  <b>一處與主對話清單的出入（如實記錄，判定未改）。</b>
  主對話交下來的四類清單逐一點名了 <b>23</b> 個單元，漏列
  <code>rates_multiply_intuition</code>（第 03 列）。本報告依<b>同一套證據</b>
  （lock fragment 對現行 <code>.tex:211</code>）補上它的 locus 與類別：差異為
  em-dash → 句號（「stack <mark>— the</mark> composite」→「stack<mark>. The</mark> composite」）
  ＋新增紙本 Figure 3.5 cross-ref，<b>數學逐字相同</b>，屬標準的類 2 型態。
  主對話已拍板的「24 單元全部不跟改」總判定<b>涵蓋此單元且不受影響</b>。
</div>

<h2><span class="num">3</span>兩個裁決項</h2>
<p class="sub">這兩項不是「沒差異」，而是「有差異、主對話裁決不跟」。理由完整列出，供覆核。</p>

<div class="callout ask">
  <b>成本視窗（請在本次 sign-off 一併決定）。</b>
  這兩項<b>現在改的邊際成本為零</b>——尚未 derive、尚未 TTS 合成，改內容稿即可。
  <b>A5 之後再改就要重念＋重新合成（計費）。</b>
  若使用者要跟改任一項，<b>請在此 sign-off 時提出。</b>
</div>

<h3>裁決項 #8 — <code>proof_strategy_bridge</code>（<code>.tex:244</code>）</h3>
<div class="card">
  <div class="quote new"><span class="lab">.tex:244 新增句（lock 版沒有這一句）</span>
    On a first reading you may jump straight to the subsection “Using the rule” below and
    return to this proof later; none of the examples depend on it.</div>
  <div class="quote"><span class="lab">.tex:244 lock 版全句</span>
    The rule is already usable — the rest of this section earns it. To prove that the two
    slopes really do multiply, we need to handle both functions’ linear approximations at
    once, and for that it helps to repackage what “differentiable” means. …</div>
  <div class="quote"><span class="lab">.tex:244 現行全句（平實化＋新增導航句）</span>
    The rule is already usable. The rest of this section proves it.
    <mark>On a first reading you may jump straight to the subsection “Using the rule” below
    and return to this proof later; none of the examples depend on it.</mark>
    To prove that the two slopes really do multiply, we need to handle both functions’
    linear approximations at once, …</div>
  <div class="quote"><span class="lab">內容稿現行（md:215）</span>
    The rule is already usable — now let's earn it. To prove that the two slopes really do
    multiply, we have to handle both functions' tangent-line approximations at once, and for
    that it helps to repackage what "differentiable" even means. …</div>
  <p style="margin-top:14px"><b>主對話裁決＝不跟改。理由：</b>新增句有兩半。
  <b>導航那半</b>（「jump straight to the subsection … below」）是<b>紙本動線</b>，
  影片 §4 禁則不得報結構，沒有對位可言。
  <b>事實那半</b>（「none of the examples depend on it」）雖然為真，
  但在<b>線性媒介</b>把它放在 4 分鐘 ε-δ 證明的開場，
  等於在最需要注意力的當口<b>邀請觀眾脫離</b>。
  影片的等價可供性是 Act divider（<code>divider_why</code>／<code>divider_use</code>）
  與章節標記，<b>已由結構承擔</b>。</p>
</div>

<h3>裁決項 #22 — <code>toward_section_3_3</code>（<code>.tex:414</code>）</h3>
<div class="card">
  <div class="ba2">
    <div class="ba"><span class="lab">.tex:414 lock 版（有比喻）</span>
      <pre>In the next section the rule does something new — it becomes <mark>the key that unlocks</mark> derivatives we could not otherwise reach, those of the inverse functions \(\ln x\), \(\arcsin x\), and \(\arctan x\), and, through logarithmic differentiation, of expressions such as \(x^{x}\).</pre></div>
    <div class="ba"><span class="lab">.tex:414 現行（比喻被刻意拿掉）</span>
      <pre>In the next section the rule does something new. <mark>It gives us derivatives we could not otherwise reach</mark>, those of the inverse functions \(\ln x\), \(\arcsin x\), and \(\arctan x\), and, through logarithmic differentiation, those of expressions such as \(x^{x}\).</pre></div>
  </div>
  <div class="quote"><span class="lab">內容稿現行（md:619，仍建在比喻上）</span>
    But the rule does something more interesting next: <mark>it becomes a key. It unlocks</mark>
    derivatives we could not otherwise reach at all — the inverse functions $\ln x$,
    $\arcsin x$, and $\arctan x$ — and, through a clever trick called logarithmic
    differentiation, even something like $x^x$.</div>
  <div class="quote"><span class="lab">下游同樣建在比喻上（若要跟改需一併動）</span>
    <code>md:625</code>（<code>visual_need</code>）：標「<mark>a key, not just another rule</mark>」<br>
    <code>storyboards/ch03_chain_rule.yml:597–599</code>（<code>say</code>）：
    「But the rule does something more interesting next -- it <mark>becomes a key, unlocking</mark>
    derivatives we couldn't otherwise reach …」<br>
    <code>…yml:601</code>（<code>statement</code>）：
    「The chain rule isn't just another rule --- <mark>it's a key</mark> to new derivatives.」</div>
  <p style="margin-top:14px"><b>主對話裁決＝不跟改。理由：</b>比喻<b>不承載解釋</b>——
  緊接著就明說「derivatives we could not otherwise reach」，
  屬<b>裝飾</b>而非「修辭藏內容」。影片語域本就允許比講義暖；
  屬根 <code>CLAUDE.md</code> 四級 review 的<b>第③級 editorial drift</b>，不是 finding。</p>
</div>

<h2><span class="num">4</span>六處「旁白仍用被平實化掉的措辭」</h2>
<p class="sub"><b>判準：</b>只有旁白<b>引述講義原句</b>或<b>依賴被刪掉的說法</b>才算跟改。
下列六處的數學主張都原封保留在現行 <code>.tex</code>，被換掉的只是語域——<b>全部不跟改</b>。</p>
<div class="scroll"><table>
  <tr><th style="width:40px"></th><th style="width:95px">內容稿</th>
      <th style="width:230px">旁白現行措辭</th><th style="width:260px">講義端變動</th>
      <th>為何不跟</th><th style="width:78px">判定</th></tr>
  %%DROWS%%
</table></div>

<h2><span class="num">5</span>本輪實際寫入了什麼</h2>
<p class="sub">外科式修改：只有內容稿 header 的兩行。單元本文、24 處 <code>source:</code> 欄位、
storyboard、共用層一律未動。</p>

<h3>(1) <code>ch03_chain_rule.md</code> 第 4 行「權威來源」</h3>
<div class="ba2">
  <div class="ba"><span class="lab">before</span><pre><code>&gt; **權威來源：** [`../../%%OLDSRC%%`](../../%%OLDSRC%%)（建置版 `legacy/html_handout/standalone/chapter3-print-standalone.html` §3.2）。</code></pre></div>
  <div class="ba"><span class="lab">after</span><pre><code>&gt; **權威來源：** [`../../%%TEX%%`](../../%%TEX%%) §3.2（`:208–416`）——2026-08-09 起講義唯一源。原 HTML fragment [`../../%%OLDSRC%%`](../../%%OLDSRC%%)（建置版 `legacy/html_handout/standalone/chapter3-print-standalone.html` §3.2）已封存於 `legacy/html_handout/`，可回溯。</code></pre></div>
</div>

<h3>(2) <code>ch03_chain_rule.md</code> 第 5 行「source_rev」</h3>
<div class="ba2">
  <div class="ba"><span class="lab">before（指向凍結的 legacy HTML）</span><pre><code>&gt; **source_rev：** `%%OLDSRC%%` `%%OLDSHA%%` — lock 時（2026-06-29，commit `%%LOCK%%`）該 fragment 的 LF 正規化 sha256（2026-09-12 依產線評估 F2 補蓋；產生器 `python video/pipeline/source_rev.py &lt;源檔&gt;`）。schema／make／derive preflight 比對現檔，不符即 `[source_rev]` WARN＝「講義已變」→ 走 §8（diff→外科修改→scoped NFA）後重蓋。**現況：lock 後講義已改三輪（2026-07-03／07-06／07-26），且 2026-08-09 起唯一源＝`%%TEX%%`——§8 對齊在解凍（品質補強試點 ④ 裁決後）進 Stage 2 前做；對齊後改 stamp 該 `.tex`。**</code></pre></div>
  <div class="ba"><span class="lab">after（指向 .tex；未來式敘述已刪除、換成對齊結論）</span><pre><code>&gt; **source_rev：** `%%TEX%%` `%%TEXSHA%%` — %%DATE%% 依 [`../CONTENT_METHODOLOGY.md`](../CONTENT_METHODOLOGY.md) §8 完成對齊後重蓋（產生器 `python video/pipeline/source_rev.py &lt;源檔&gt;`）。schema／make／derive preflight 比對現檔，不符即 `[source_rev]` WARN＝「講義已變」→ 走 §8（diff→外科修改→scoped NFA）後重蓋。**對齊結論：lock（2026-06-29，commit `%%LOCK%%`）至今 §3.2 的講義改動全屬標點平實化／同義詞替換／圖說精簡／紙本動線，本文（Thm 3.3／Def 3.1／Prop 3.3／Strategy 3.1／Caution／ex:3.4–3.8／full ε-δ 證明）數學零改動，24 個單元全部「不跟改」（跟改 0 筆）；證據見 [`_audit/REVIEW-ch03_chain_rule-s32-a1-alignment.html`](_audit/REVIEW-ch03_chain_rule-s32-a1-alignment.html)。**</code></pre></div>
</div>
<p class="sub"><code>LOCKED</code>／<code>CONTENT_APPROVED=yes</code> 的階段行<b>未動</b>——
本輪零內容改動，原 2026-06-29 使用者 sign-off 仍然成立。</p>

<h3>(3) 閘的驗收：<code>[source_rev]</code> WARN 消失</h3>
<div class="ba2">
  <div class="ba"><span class="lab">before</span><pre><code>$ python video/pipeline/schema.py video/storyboards/ch03_chain_rule.yml
[schema] ch03_chain_rule.yml: structure OK
[source_rev] ch03_chain_rule.yml: 1 finding(s) (warn-only)
  WARN   ch03_chain_rule.md: handout source legacy/html_handout/fragments/ch03/sec-3-2.html
  changed since the content script was stamped (stamp is the frozen legacy HTML; the live
  source is handout/latex/src/&lt;ch&gt;/*.tex) -- CONTENT_METHODOLOGY.md section 8: diff -&gt;
  surgical edit -&gt; scoped NFA -&gt; re-stamp</code></pre></div>
  <div class="ba"><span class="lab">after</span><pre><code>$ python video/pipeline/schema.py video/storyboards/ch03_chain_rule.yml
[schema] ch03_chain_rule.yml: structure OK</code></pre></div>
</div>
<p class="sub">WARN 消失，且仍印 <code>structure OK</code>。</p>

<h3>(4) <code>_narration.html</code> 重編，旁白正文<b>零差異</b></h3>
<div class="card">
  <p style="margin:.2em 0">以本 repo 的正規產生器重新編譯：</p>
  <div class="ba"><pre><code>$ python video/pipeline/narration_review.py video/content_scripts/ch03_chain_rule.md
wrote …\ch03_chain_rule_narration.html  (24 units, 22 with narration)</code></pre></div>
  <p style="margin:.8em 0 .4em"><b>驗證方式：</b>改 stamp 前先把
  <code>ch03_chain_rule_narration.html</code> 另存一份備份，重編後對兩份做 <code>diff</code>：</p>
  <div class="ba"><pre><code>$ diff &lt;改前備份&gt; video/content_scripts/ch03_chain_rule_narration.html
（無輸出；exit 0）</code></pre></div>
  <p style="margin:.8em 0 0"><b>結果：<span class="ok">逐位元組相同</span></b>——連 header 區都沒有差異。
  原因是 <code>narration_review.py</code> 只讀 <code>## meta</code> 條列與 <code>### unit:</code>
  區塊，<b>不把 header 的「權威來源／source_rev」兩行編進 HTML</b>。
  因此本輪的 header 改動不會、也不該在 <code>_narration.html</code> 留下任何痕跡；
  「旁白正文零差異」因而獲得比「差異只落在 header」更強的證明。<br>
  （附帶確認：現行 <code>_narration.html</code> 確實由 <code>narration_review.py</code> 產出——
  以它重編可得逐位元組相同的檔；<code>_audit/_gen/build_narration_html.py</code>
  的輸出則不同，不是本檔的產生器。）</p>
</div>

<h2><span class="num">6</span>本輪不做（及理由）</h2>
%%NOTDONE%%

<h2><span class="num">7</span>給使用者的兩個問題</h2>

<div class="qbox">
  <div class="qn">問題 ①</div>
  <div class="qt">24 個單元全部判「不跟改」（跟改 0 筆），同意嗎？</div>
  <p style="margin:.3em 0 0">承重證據＝上方 §1 的 (A)(B)：講義端 59 個變動行全屬語域／圖說／動線；
  數學式 213 → 204 的差異逐條可歸因（改 2 純排版、刪 10 全出自被精簡的 Fig 3.5 舊圖說、
  增 1 為新圖說），本文零數學改動。</p>
</div>

<div class="qbox">
  <div class="qn">問題 ②</div>
  <div class="qt">兩個裁決項維持「不跟改」，或要跟改其中哪一項？</div>
  <ul class="tight" style="margin-top:.6em">
    <li><b>#8 <code>proof_strategy_bridge</code></b>：講義新增「可先跳過證明、範例不依賴它」的導航句。
        裁決＝不跟（線性媒介不宜在證明開場邀請脫離；等價可供性已由 Act divider 承擔）。</li>
    <li><b>#22 <code>toward_section_3_3</code></b>：講義把「key that unlocks」的比喻拿掉，內容稿仍用。
        裁決＝不跟（比喻不承載解釋，屬第③級 editorial drift）。若要跟改，需一併動
        <code>md:619</code>、<code>md:625</code> 與
        <code>storyboards/ch03_chain_rule.yml:597–601</code>。</li>
  </ul>
  <p style="margin:.8em 0 0"><b>現在改的邊際成本為零；A5 之後再改要重念＋重新合成（計費）。</b></p>
</div>

<footer>
  產生器：<code>video/content_scripts/_audit/_gen/build_s32_a1_alignment_html.py</code>（跑一次吐本頁）。
  數學由 MathJax 3（CDN）即時渲染；雙擊即開。<br>
  依據：lock <code>%%LOCK%%</code>（%%DATE_LOCK%%）→ main tip <code>%%TIP%%</code>；
  講義源 <code>%%TEX%%</code> <code>%%TEXSHA%%</code>。
</footer>

</div></body></html>
"""


def main() -> int:
    subs = {
        "%%DATE%%": DATE, "%%DATE_LOCK%%": DATE_LOCK,
        "%%LOCK%%": LOCK_COMMIT, "%%TIP%%": MAIN_TIP,
        "%%TEX%%": TEX, "%%TEXSHA%%": TEX_SHA,
        "%%OLDSRC%%": OLD_SRC, "%%OLDSHA%%": OLD_SHA,
        "%%DIFFROWS%%": diff_rows(),
        "%%FCHANGED%%": formula_changed_rows(),
        "%%FDELETED%%": "　".join(r"\(%s\)" % t for t in FORMULA_DELETED),
        "%%FADDED%%": "　".join(r"\(%s\)" % t for t in FORMULA_ADDED),
        "%%KCOUNTS%%": klass_counts(),
        "%%UROWS%%": unit_rows(),
        "%%DROWS%%": drift_rows(),
        "%%NOTDONE%%": not_done_cards(),
    }
    page = HTML
    for key, val in subs.items():
        page = page.replace(key, val)
    if "%%" in page:
        raise SystemExit("unsubstituted placeholder left in template")
    OUT.write_text(page, encoding="utf-8")
    print("[ok] %d units -> %s" % (len(UNITS), OUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

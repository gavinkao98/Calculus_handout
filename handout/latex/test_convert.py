"""convert.py 的 golden tests（KICKOFF-latex-pilot.md M-P1 驗證點）。

    python test_convert.py

純 stdlib unittest。每個 mapping 一組 golden（fragment 片段 -> 預期 LaTeX），
外加最重要的不變式：數學 pass-through 逐位元組相等。
"""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from convert import (  # noqa: E402
    Builder, ConversionError, FragmentParser, LatexEmitter, MathScanError,
    convert_chapter, extract_math,
)

HTML_LINE = Path(__file__).resolve().parent.parent / "html"
FIGS = {
    "panels": [
        {"id": "sector-inequality", "file": "sector-inequality.pdf", "mm": 79.9},
        {"id": "remainder-tangent", "file": "remainder-tangent-1.pdf", "mm": 65.62},
        {"id": "remainder-tangent", "file": "remainder-tangent-2.pdf", "mm": 65.62},
    ]
}


def conv(html):
    """片段 -> LaTeX（測試用的最小驅動）。"""
    stripped, math = extract_math(html)
    p = FragmentParser("<test>")
    p.feed(stripped)
    root = p.close()
    ir = Builder("<test>").articles(root)
    return LatexEmitter(math, FIGS, "ch03").emit(ir).strip()


def wrap(inner):
    return f'<article class="sec" lang="en">{inner}</article>'


# example＋solution 只能成對住在 workedexample 內（CONTRACT：no solo example）
WE_PAIR = ('<div class="workedexample">'
           '<section class="env env-example"><p class="env-head">'
           '<span class="env-kicker">Example</span><span class="env-num">3.1</span></p>'
           '<div class="env-body"><p>Q.</p></div></section>'
           '<section class="env env-solution"><p class="env-head">'
           '<span class="env-kicker">Solution</span></p>'
           '<div class="env-body"><p>A.</p></div></section></div>')


def naive_scan_math(raw):
    """獨立 oracle：只為測試而寫的樸素數學掃描器，刻意不共用 convert.py 的任何程式碼。

    若拿轉換器自己的 scanner（或它的 MATH_RE）當 oracle，就是循環論證：掃描器漏認的段落，
    oracle 也會一起漏認，測試永遠是綠的。故這裡重寫一遍最直白的邏輯，兩者互為對照。
    """
    out, i, n = [], 0, len(raw)
    while i < n:
        if raw.startswith("<!--", i):                 # 註解內的數學不算
            i = raw.find("-->", i + 4)
            i = n if i < 0 else i + 3
            continue
        if raw[i] == "\\" and i + 1 < n and raw[i + 1] in "([":
            close = ")" if raw[i + 1] == "(" else "]"
            j = i + 2
            while j < n:
                if raw[j] == "\\" and j + 1 < n:
                    if raw[j + 1] == close:
                        out.append(raw[i:j + 2])
                        i = j + 2
                        break
                    j += 2
                    continue
                j += 1
            else:
                i = n
            continue
        i += 2 if raw[i] == "\\" else 1
    return out


class MathPassthrough(unittest.TestCase):
    """鐵律：數學區段逐位元組照抄。"""

    def test_inline_with_angle_brackets(self):
        # ch03 有 16 段這種，html.parser 會把 `< \theta` 當標籤吃掉
        out = conv(wrap(r"<p>Take \(0 < \theta < \tfrac{\pi}{2}\) and look.</p>"))
        self.assertIn(r"\(0 < \theta < \tfrac{\pi}{2}\)", out)

    def test_ampersand_in_aligned(self):
        # sec-3-2.html:150 的 `&P(x_{0}+h)`：entity 解碼會吃掉它
        src = r"<p>\[ \begin{aligned} &P(x_{0}+h) = P(x_{0}) + h, \\ &Q = 1. \end{aligned} \]</p>"
        out = conv(wrap(src))
        self.assertIn(r"&P(x_{0}+h)", out)
        self.assertIn(r"&Q = 1.", out)

    def test_no_escaping_inside_math(self):
        # 散文 escape 表的字元在數學裡必須毫髮無傷
        src = r"<p>\(a \% b \_ c \# d ^ e ~ f\)</p>"
        out = conv(wrap(src))
        self.assertIn(r"\(a \% b \_ c \# d ^ e ~ f\)", out)

    def test_display_math_newlines_kept(self):
        src = "<p>\\[ \\begin{aligned}\n  a &= b \\\\\n  &= c.\n\\end{aligned} \\]</p>"
        out = conv(wrap(src))
        self.assertIn("\\begin{aligned}\n  a &= b \\\\\n  &= c.\n\\end{aligned}", out)

    def test_tag_macro_survives(self):
        out = conv(wrap(r"<p>\[ \cos\theta \le 1. \tag{1} \]</p>"))
        self.assertIn(r"\tag{1}", out)

    def test_every_ch03_math_segment_is_byte_identical_in_order(self):
        """全章不變式：每段數學原封、依序、恰好出現一次。

        用**獨立的 oracle**：不呼叫 extract_math，改用一支只為測試而寫的樸素掃描器。
        先前這條測試拿轉換器自己的 MATH_RE 當 oracle，是循環論證——regex 漏認的話兩邊
        會一起錯；而且只驗 `m in tex`，驗不到順序與重複次數。
        """
        tex, _ = convert_chapter("ch03", Path(__file__).parent / "chapters" / "ch03" / "figs" / "figures.json")
        src_math = []
        for f in ("sec-3-1", "sec-3-2", "sec-3-3"):
            src_math += naive_scan_math(
                (HTML_LINE / "fragments" / "ch03" / f"{f}.html").read_text(encoding="utf-8"))
        self.assertEqual(len(src_math), 605, "數學區段數應為 605（M-P0 盤點）")

        # 依序：每段必須出現在前一段之後（驗得到順序，也驗得到遺漏）
        pos = 0
        for k, m in enumerate(src_math):
            j = tex.find(m, pos)
            self.assertGreaterEqual(j, 0, f"第 {k} 段數學未依序出現在 .tex：{m[:60]!r}")
            pos = j + len(m)


class MathScannerClosure(unittest.TestCase):
    """鐵律必須是封閉的不變式，不能靠「ch03 剛好沒有這些情況」成立（Codex gate-2 ①-1）。"""

    def scan_err(self, src, *expect):
        with self.assertRaises(MathScanError) as cm:
            extract_math(src, "t")
        for e in expect:
            self.assertIn(e, str(cm.exception))

    def test_same_kind_inline_nesting_rejected(self):
        # 合法 LaTeX 但轉換器不支援。舊的非貪婪 regex 會提早閉合，靜默排出壞掉的數學。
        self.scan_err(r"\(\text{outer \(x\) tail}\)", "巢狀")

    def test_same_kind_display_nesting_rejected(self):
        self.scan_err(r"\[ a \[ b \] \]", "巢狀")

    def test_unpaired_opener_rejected(self):
        self.scan_err(r"prose \(x with no closer", "沒有配對")

    def test_stray_closer_rejected(self):
        self.scan_err(r"prose \) stray", "游離")

    def test_cross_kind_nesting_allowed(self):
        # \( 在 \[ 內是合法且常見的（\text{} 裡的行內數學），必須放行
        _, store = extract_math(r"\[ \text{if \(x>0\)} \]", "t")
        self.assertEqual(store, [r"\[ \text{if \(x>0\)} \]"])

    def test_escaped_backslash_bracket_is_not_an_opener(self):
        # `\\[` ＝跳脫的反斜線＋普通左括號，不是 display opener（反斜線奇偶）
        _, store = extract_math(r"text \\[ not math", "t")
        self.assertEqual(store, [])

    def test_linebreak_in_aligned_does_not_split_display(self):
        # aligned 的 `\\[2pt]` 曾是最可能切斷外層 display math 的地方
        src = r"\[ \begin{aligned} a &= b \\[2pt] c &= d \end{aligned} \]"
        _, store = extract_math(src, "t")
        self.assertEqual(store, [src])

    def test_math_inside_html_comment_not_extracted(self):
        _, store = extract_math("<!-- \\[ a \\] 註解 -->\n\\(y\\)", "t")
        self.assertEqual(store, [r"\(y\)"])

    def test_entity_encoded_backslash_rejected(self):
        # `&#92;(x&#92;)` 在瀏覽器 DOM／MathJax 是數學，但 scanner 掃未解 entity 的原文，
        # 看不到分隔符 → 會靜默轉成 \textbackslash{}(x…)。HTML 與 LaTeX 語義分岔，硬錯。
        for ent in ("&#92;", "&#x5C;", "&bsol;"):
            self.scan_err(f"<p>{ent}(x{ent})</p>", "反斜線")

    def test_env_name_math_ordering_not_false_positive(self):
        # emitter 曾先算 body 再算 env-name，於是 env-name 帶數學時 used=[1,0]，
        # 輸出明明正確卻被不變式誤擋。ch03 的 13 個 env-name 剛好都沒數學才沒踩到。
        out = conv(wrap('<section class="env env-theorem"><p class="env-head">'
                        '<span class="env-kicker">Theorem</span>'
                        r'<span class="env-name">Name \(a\)</span></p>'
                        r'<div class="env-body"><p>Body \(b\)</p></div></section>'))
        self.assertIn(r"{Name \(a\)}", out)
        self.assertIn(r"Body \(b\)", out)
        self.assertLess(out.index(r"\(a\)"), out.index(r"\(b\)"))

    def test_forged_sentinel_in_prose_is_caught(self):
        # 課文可用 &#xE000; 偽造占位符。不靠「不會有人這樣寫」，靠不變式擋。
        with self.assertRaises(ConversionError) as cm:
            conv(wrap("<p>A&#xE000;9&#xE001;B</p>"))
        self.assertIn("E000", str(cm.exception))


class ProseEscaping(unittest.TestCase):
    def test_specials_escaped(self):
        out = conv(wrap("<p>100% of A&B cost $5 #1 x_1 a^b ~c {d} e\\f</p>"))
        self.assertIn(r"100\% of A\&B cost \$5 \#1 x\_1 a\textasciicircum{}b "
                      r"\textasciitilde{}c \{d\} e\textbackslash{}f", out)

    def test_unicode_kept_not_asciified(self):
        # lualatex＋NCM 原生成立；與 quote_lint.py 的 curly 政策一致
        out = conv(wrap("<p>a — b “c” d – e’f §3.1</p>"))
        self.assertIn("a — b “c” d – e’f §3.1", out)

    def test_entities_decoded_in_prose(self):
        # &amp; 必須先解碼成 & 再 escape 成 \&，否則 LaTeX 會收到裸 `&amp;` 而爆掉。
        # ch03 散文實際沒有任何 entity（唯一的 `&P;` 在 aligned 數學內），這條是 rollout 護欄。
        out = conv(wrap("<p>Bell &amp; Howell &mdash; ok</p>"))
        self.assertIn(r"Bell \& Howell — ok", out)

    def test_angle_brackets_not_escaped(self):
        # 現況：< > 不 escape。ch03 產出的 .tex 在數學外有 0 個 < >（全部 42 處都在數學裡，
        # 由占位符保護），故未在生產中觸發。lualatex＋fontspec 下裸 < > 本來就渲染成該字元。
        out = conv(wrap("<p>a &lt; b</p>"))
        self.assertIn("a < b", out)

    def test_whitespace_collapsed(self):
        out = conv(wrap("<p>a\n   b\t\tc</p>"))
        self.assertIn("a b c", out)


class Mappings(unittest.TestCase):
    def test_chapter_head(self):
        out = conv(wrap('<header class="chapter-head"><div class="ch-kicker">Chapter 3</div>'
                        '<h1 class="ch-title">Chain Rule</h1></header>'))
        self.assertEqual(out, r"\chapteropener{Chapter 3}{Chain Rule}")

    def test_appendix_opener_is_kicker_driven(self):
        # 附錄開場變體（DIALECT-appB §3）：kicker 字面驅動，不開 counter（D7）
        out = conv(wrap('<header class="chapter-head"><div class="ch-kicker">Appendix B</div>'
                        '<h1 class="ch-title">Reading Theorems and Proofs</h1></header>'))
        self.assertEqual(out, r"\appendixopener{Appendix B}{Reading Theorems and Proofs}")

    def test_section_head_number_is_literal(self):
        # D7：編號照抄字面，不開 auto-counter
        out = conv(wrap('<header class="sec-head"><h2 class="sec-title">'
                        '<span class="sec-no">3.1</span>Derivatives of Sine</h2></header>'))
        self.assertEqual(out, r"\sechead{3.1}{Derivatives of Sine}")

    def test_subsec_and_para_head(self):
        out = conv(wrap('<h3 class="subsec-head">A geometric inequality</h3>'
                        '<p class="para-head">By the end:</p>'))
        self.assertIn(r"\subsechead{A geometric inequality}", out)
        self.assertIn(r"\parahead{By the end:}", out)

    def test_lead_and_informal(self):
        out = conv(wrap('<p class="lead">Lead text.</p><p class="informal">Informally, x.</p>'))
        self.assertIn("\\begin{lead}\nLead text.\n\\end{lead}", out)
        self.assertIn("\\begin{informal}\nInformally, x.\n\\end{informal}", out)

    def test_emphasis(self):
        out = conv(wrap("<p>a <em>chain rule</em> b</p>"))
        self.assertIn(r"a \emph{chain rule} b", out)

    def test_itemize(self):
        out = conv(wrap("<ul><li>first</li><li>second</li></ul>"))
        self.assertEqual(out, "\\begin{itemize}\n  \\item first\n  \\item second\n\\end{itemize}")

    def test_ol_steps(self):
        out = conv(wrap('<ol class="steps"><li>one</li></ol>'))
        self.assertEqual(out, "\\begin{steps}\n  \\item one\n\\end{steps}")

    def test_env_with_num_and_name(self):
        out = conv(wrap('<section class="env env-theorem"><p class="env-head">'
                        '<span class="env-kicker">Theorem</span><span class="env-num">3.4</span>'
                        '<span class="env-name">Chain rule</span></p>'
                        '<div class="env-body"><p>Body.</p></div></section>'))
        self.assertEqual(out, "\\begin{envtheorem}{Theorem}{3.4}{Chain rule}\nBody.\n\\end{envtheorem}")

    def test_env_without_num(self):
        # 54 個 env-head 只有 28 個有號（solution 等不編號）。
        # solution 必須與 example 成對住在 workedexample 內（CONTRACT：no solo example）。
        out = conv(wrap(WE_PAIR))
        self.assertIn("\\begin{envsolution}{Solution}{}{}\nA.\n\\end{envsolution}", out)

    def test_worked_example_groups_pair(self):
        out = conv(wrap('<div class="workedexample">'
                        '<section class="env env-example"><p class="env-head">'
                        '<span class="env-kicker">Example</span><span class="env-num">3.1</span></p>'
                        '<div class="env-body"><p>Q.</p></div></section>'
                        '<section class="env env-solution"><p class="env-head">'
                        '<span class="env-kicker">Solution</span></p>'
                        '<div class="env-body"><p>A.</p></div></section></div>'))
        self.assertTrue(out.startswith("\\begin{workedexample}"))
        self.assertTrue(out.endswith("\\end{workedexample}"))
        self.assertIn(r"\begin{envexample}{Example}{3.1}{}", out)
        self.assertIn(r"\begin{envsolution}{Solution}{}{}", out)

    def test_all_nine_env_kinds(self):
        for kind in ("definition", "theorem", "proposition", "proof",
                     "remark", "caution", "strategy"):
            env = (f'<section class="env env-{kind}"><p class="env-head">'
                   f'<span class="env-kicker">K</span></p>'
                   f'<div class="env-body"><p>b</p></div></section>')
            self.assertIn(f"\\begin{{env{kind}}}", conv(wrap(env)))
        # example／solution 只能成對出現在 workedexample 內（CONTRACT：no solo example）
        out = conv(wrap(WE_PAIR))
        self.assertIn(r"\begin{envexample}", out)
        self.assertIn(r"\begin{envsolution}", out)

    def test_figure_single_uses_measured_mm_not_textwidth(self):
        # DIALECT-ch03.md §5：\textwidth 會把圖內標籤放大約一倍
        out = conv(wrap('<figure class="figure" data-fig="sector-inequality"><figcaption>'
                        '<span class="fig-no">Figure 3.1</span> The area comparison.</figcaption>'
                        '</figure>'))
        self.assertIn(r"\begin{figureblock}", out)
        self.assertIn(r"\includegraphics[width=79.9mm]{ch03/sector-inequality}", out)
        self.assertIn(r"\figcaption{Figure 3.1}{The area comparison.}", out)
        self.assertNotIn(r"\textwidth", out)

    def test_figure_pair_puts_two_panels_side_by_side(self):
        out = conv(wrap('<figure class="figure" data-fig="remainder-tangent"><figcaption>'
                        '<span class="fig-no">Figure 3.6</span> Two panels.</figcaption></figure>'))
        self.assertIn(r"\includegraphics[width=65.62mm]{ch03/remainder-tangent-1}", out)
        self.assertIn(r"\includegraphics[width=65.62mm]{ch03/remainder-tangent-2}", out)
        self.assertIn(r"\hspace{6mm}", out)

    def test_figure_caption_keeps_math(self):
        out = conv(wrap('<figure class="figure" data-fig="sector-inequality"><figcaption>'
                        r'<span class="fig-no">Figure 3.1</span> Behind \(\sin\theta \le \theta\).'
                        '</figcaption></figure>'))
        self.assertIn(r"\(\sin\theta \le \theta\)", out)

    def test_comments_dropped(self):
        out = conv(wrap("<!-- expansion:intuition — note ③波 -->\n<p>Body.</p>"))
        self.assertEqual(out, "Body.")
        for ch in "③波":
            self.assertNotIn(ch, out)


class AppBMappings(unittest.TestCase):
    """appB 差集 mapping（M-B2；DIALECT-appB.md §3 凍結）。"""

    def test_strong_is_runin(self):
        out = conv(wrap("<p><strong>Direct.</strong> Assume the hypothesis.</p>"))
        self.assertIn(r"\runin{Direct.} Assume the hypothesis.", out)

    def test_ul_steps_is_bulletsteps(self):
        out = conv(wrap('<ul class="steps"><li><strong>Direct.</strong> a</li></ul>'))
        self.assertEqual(out, "\\begin{bulletsteps}\n  \\item \\runin{Direct.} a\n\\end{bulletsteps}")

    def test_ul_sol_list_is_sollist(self):
        # 散文位置（article 直下）與 env-body 內同一環境（DIALECT-appB §2 #15）
        out = conv(wrap('<ul class="sol-list"><li>x</li></ul>'))
        self.assertEqual(out, "\\begin{sollist}\n  \\item x\n\\end{sollist}")

    def test_center_statement(self):
        out = conv(wrap('<p style="text-align:center;">(i) for every \\(x\\) there is \\(y\\).</p>'))
        self.assertEqual(out, "\\begin{centerstatement}\n(i) for every \\(x\\) there is \\(y\\).\n\\end{centerstatement}")

    def test_center_statement_with_br(self):
        out = conv(wrap('<p style="text-align:center;">line one<br>line two</p>'))
        self.assertIn("line one\\\\\nline two", out)

    def test_ensp_maps_to_enspace(self):
        # &ensp; 解碼成 U+2002；空白收合不得吃掉它，escape 映射 \enspace{}（DIALECT-appB §5）
        out = conv(wrap('<p style="text-align:center;">(i)&ensp;&ensp;for every</p>'))
        self.assertIn(r"(i)\enspace{}\enspace{}for every", out)

    def test_qed_proof_marker(self):
        out = conv(wrap('<section class="env env-proof"><p class="env-head">'
                        '<span class="env-kicker">Proof</span></p>'
                        '<div class="env-body"><p>done. <span class="qed qed-proof"></span></p>'
                        '</div></section>'))
        self.assertIn("done. \\qedmark", out)
        self.assertIn(r"\begin{envproof}{Proof}{}{}", out)

    def test_opener_ul_becomes_objectives(self):
        out = conv(wrap('<header class="chapter-head"><div class="ch-kicker">Appendix B</div>'
                        '<h1 class="ch-title">T</h1></header>'
                        '<p class="para-head">By the end:</p>'
                        '<ul><li>obj one</li></ul>'))
        self.assertIn("\\begin{objectives}\n  \\item obj one\n\\end{objectives}", out)

    def test_non_opener_ul_stays_itemize(self):
        # 只有含 chapter-head 的開場 article 頂層素 ul 才是 objectives
        out = conv(wrap("<ul><li>x</li></ul>"))
        self.assertTrue(out.startswith("\\begin{itemize}"))

    def test_p_page_break_before(self):
        # M-B1 §2（2026-07-17 擴充）：p.page-break-before → \pagebreakbefore 置於該段之前
        out = conv(wrap('<p class="page-break-before">after the break</p>'))
        self.assertIn("\\pagebreakbefore\nafter the break", out)

    def test_p_page_break_before_only_as_sole_class(self):
        # 與 lead／informal／para-head 同紀律：複合 class 不在凍結表內，須硬錯而非靜默丟棄
        with self.assertRaises(ConversionError) as cm:
            conv(wrap('<p class="lead page-break-before">x</p>'))
        self.assertIn("page-break-before", str(cm.exception))

    def test_every_appB_math_segment_is_byte_identical_in_order(self):
        """appB 全篇不變式（擴自 ch03 版）：每段數學原封、依序、恰好一次。"""
        tex, _ = convert_chapter("appB", Path(__file__).parent / "chapters" / "appB" / "figs" / "figures.json")
        src_math = []
        for f in ("sec-b-1", "sec-b-2", "sec-b-3", "sec-b-4", "sec-b-5", "sec-b-6"):
            src_math += naive_scan_math(
                (HTML_LINE / "fragments" / "appB" / f"{f}.html").read_text(encoding="utf-8"))
        # 2026-07-17 定稿後重新盤點（原 317＝inline 308＋display 9，是 M-B0 的五節快照）。
        # 注意：本迴圈原本漏掉 sec-b-6 —— 新一節的數學因此未被逐位元組驗到；已補入。
        # 2026-07-17（r3）545→566：§B.6 新增 Example B.11（歸納法斷鏈），display 13→16＝
        # 該例的宣稱、歸納步驟、與 Prop B.4 的對照式各一。
        self.assertEqual(len(src_math), 566, "數學區段數應為 566＝inline 550＋display 16")
        pos = 0
        for k, m in enumerate(src_math):
            j = tex.find(m, pos)
            self.assertGreaterEqual(j, 0, f"第 {k} 段數學未依序出現在 .tex：{m[:60]!r}")
            pos = j + len(m)

    def test_appB_converts_with_no_hard_errors(self):
        # M-B2 驗證點：appB 全節點 100% 交代（mapped 或硬錯；無表外標記）
        tex, stats = convert_chapter("appB", Path(__file__).parent / "chapters" / "appB" / "figs" / "figures.json")
        self.assertEqual(stats["mapped"], 717)   # 鎖實值（gate-2 A2：>300 太弱）；2026-07-17 定稿後 440→695（新增 §B.6）、695→716（r3 新增 Example B.11）、716→717（r3 二輪：§B.3 指路子句的 <em>if–then</em>）
        self.assertEqual(stats["math"], 566)
        # emitter 重定向的 aggregate 斷言：v1 book-class 詞彙（hk*）不得殘留
        self.assertIsNone(re.search(r"\\hk[a-z]", tex), "輸出殘留 v1 hk* 詞彙")
        for probe in (r"\appendixopener{Appendix B}", r"\begin{objectives}",
                      r"\begin{envstrategy}{Strategy}{B.1}{Taking a statement apart}",
                      r"\begin{bulletsteps}", r"\begin{sollist}",
                      r"\begin{centerstatement}", r"\qedmark",
                      r"\begin{envremark}{Pause}{}{}", r"\enspace{}"):
            self.assertIn(probe, tex)


class FailLoud(unittest.TestCase):
    """mapping 表外一律硬錯，禁止靜默丟棄。"""

    def assertRejects(self, html, *expect):
        with self.assertRaises(ConversionError) as cm:
            conv(wrap(html))
        for e in expect:
            self.assertIn(e, str(cm.exception))

    def test_unknown_tag(self):
        self.assertRejects("<p>a</p><blockquote>b</blockquote>", "blockquote", "未知標記")

    def test_table_rejected_not_silently_dropped(self):
        # ch03 沒有 table，故 mapping 未凍結——遇到必須硬錯而非丟掉
        self.assertRejects('<table class="tbl"><tr><td>x</td></tr></table>', "table")

    def test_unknown_class_on_known_tag(self):
        self.assertRejects('<p class="mystery">a</p>', "未知標記", "mystery")

    def test_strong_with_class_rejected(self):
        # 素 <strong> 自 M-B2 起是 appB 差集的 run-in 標籤；帶 class 的仍屬表外
        self.assertRejects('<p>a <strong class="mystery">b</strong></p>', "inline")

    def test_plain_qed_span_rejected(self):
        # appB 方言只凍結 qed qed-proof（proof 收尾）；素 qed（solution 變體）未凍結，
        # 哪天 fragment 加了要硬錯提醒補 mapping
        self.assertRejects('<p>done <span class="qed"></span></p>', "span")

    def test_qed_span_with_content_rejected(self):
        self.assertRejects('<p>done <span class="qed qed-proof">x</span></p>', "空元素")

    def test_br_outside_center_rejected(self):
        self.assertRejects("<p>a<br>b</p>", "br")

    def test_style_other_value_rejected(self):
        self.assertRejects('<p style="text-align:left;">x</p>', "style")

    def test_style_with_class_rejected(self):
        self.assertRejects('<p class="lead" style="text-align:center;">x</p>', "style")

    def test_style_on_inline_rejected(self):
        self.assertRejects('<p>a <em style="color:red">b</em></p>', "style")

    # ── gate-2 M-B3 blocking 的繞過路徑，逐條鎖住（style 收口移至 parser 層後） ──
    def test_style_on_structural_nodes_rejected(self):
        # 結構節點（env／env-body／li）先前走直接解析路徑、繞過 Builder 的 guard
        self.assertRejects('<section class="env env-remark" style="color:red">'
                           '<p class="env-head"><span class="env-kicker">R</span></p>'
                           '<div class="env-body"><p>b</p></div></section>', "style")
        self.assertRejects('<section class="env env-remark"><p class="env-head">'
                           '<span class="env-kicker">R</span></p>'
                           '<div class="env-body" style="color:red"><p>b</p></div></section>', "style")
        self.assertRejects('<ul><li style="color:red">x</li></ul>', "style")

    def test_style_on_article_rejected(self):
        with self.assertRaises(ConversionError) as cm:
            conv('<article class="sec" style="color:red"><p>x</p></article>')
        self.assertIn("style", str(cm.exception))

    def test_duplicate_attrs_rejected(self):
        # dict(attrs) 折疊讓前值靜默消失：兩個 style 併寫可繞過白名單（gate-2 實證）
        self.assertRejects('<p style="color:red" style="text-align:center;">x</p>', "重複")
        self.assertRejects('<p class="lead" class="informal">x</p>', "重複")

    def test_two_opener_uls_rejected(self):
        # 開場 schema 凍結為恰一個 objectives；多個素 ul 硬錯而非全部改寫（gate-2 A1）
        self.assertRejects('<header class="chapter-head"><div class="ch-kicker">Appendix B</div>'
                           '<h1 class="ch-title">T</h1></header>'
                           '<ul><li>a</li></ul><ul><li>b</li></ul>', "objectives")

    def test_ol_with_start_rejected(self):
        self.assertRejects('<ol class="steps" start="3"><li>a</li></ol>', "start")

    # ── Codex gate-2 ①-2 的靜默繞過反例，逐條鎖住 ──
    def test_unknown_class_on_em_rejected(self):
        self.assertRejects('<p>a <em class="mystery">b</em></p>', "em")

    def test_extra_class_on_env_rejected(self):
        self.assertRejects('<section class="env env-theorem mystery">'
                           '<p class="env-head"><span class="env-kicker">T</span></p>'
                           '<div class="env-body"><p>b</p></div></section>', "class")

    def test_wrong_tag_carrying_known_class_rejected(self):
        # text_of() 曾遞迴攤平任何子元素，於是 <strong class="env-kicker"> 被當成合法 kicker
        self.assertRejects('<section class="env env-remark">'
                           '<p class="env-head"><strong class="env-kicker">Remark</strong></p>'
                           '<div class="env-body"><p>b</p></div></section>', "env-head")

    def test_bare_text_in_list_not_silently_dropped(self):
        self.assertRejects("<ul>DROP<li>kept</li></ul>", "裸文字", "DROP")

    def test_bare_text_in_env_not_silently_dropped(self):
        self.assertRejects('<section class="env env-remark">DROP'
                           '<p class="env-head"><span class="env-kicker">R</span></p>'
                           '<div class="env-body"><p>b</p></div></section>', "DROP")

    def test_extra_node_after_sec_title_not_ignored(self):
        self.assertRejects('<header class="sec-head">'
                           '<h2 class="sec-title"><span class="sec-no">3.1</span>T</h2>'
                           '<blockquote>DROP</blockquote></header>', "sec-head")

    # ── Codex 回歸覆核的新反例 ──
    def test_duplicate_field_overwrite_rejected(self):
        # 重複欄位先前是「後者覆寫前者」＝前者的內容無聲消失
        self.assertRejects('<section class="env env-remark">'
                           '<p class="env-head"><span class="env-kicker">R</span></p>'
                           '<div class="env-body"><p>FIRST</p></div>'
                           '<div class="env-body"><p>SECOND</p></div></section>', "重複")
        self.assertRejects('<section class="env env-remark">'
                           '<p class="env-head"><span class="env-kicker">A</span>'
                           '<span class="env-kicker">B</span></p>'
                           '<div class="env-body"><p>b</p></div></section>', "重複")

    def test_em_class_checked_in_sec_title_and_figcaption(self):
        # <em> 的 class 驗證先前只在 inlines()，這兩條分支漏掉
        self.assertRejects('<header class="sec-head"><h2 class="sec-title">'
                           '<em class="mystery">X</em></h2></header>', "em")
        self.assertRejects('<figure class="figure" data-fig="sector-inequality"><figcaption>'
                           '<span class="fig-no">Figure 3.1</span> <em class="mystery">x</em>.'
                           '</figcaption></figure>', "em")

    def test_half_workedexample_rejected(self):
        # CONTRACT「no solo example」先前只擋 workedexample 外的，沒擋內部只有一半
        self.assertRejects('<div class="workedexample">'
                           '<section class="env env-example"><p class="env-head">'
                           '<span class="env-kicker">Example</span></p>'
                           '<div class="env-body"><p>q</p></div></section></div>',
                           "workedexample", "solo")

    def test_parser_declarations_not_silently_swallowed(self):
        # HTMLParser 預設把這些全部靜默吞掉，裡面的內容就無聲消失
        for bad, why in (("<![CDATA[DROP]]>", "宣告"),
                         ("<!DOCTYPE html>", "宣告"),
                         ("<?php DROP ?>", "processing"),
                         ("</bogus>", "游離")):
            with self.assertRaises(ConversionError, msg=f"未擋下 {bad}") as cm:
                conv(wrap(f"<p>a</p>{bad}"))
            self.assertIn(why, str(cm.exception))

    def test_solo_example_or_solution_rejected(self):
        # preamble 的 hkexample／hksolution 不自畫色條（由 workedexample 畫一條共用的），
        # 所以落單的 example／solution 會靜默少一條色條——必須硬錯而不是默默排出去。
        for kind in ("example", "solution"):
            self.assertRejects(f'<section class="env env-{kind}"><p class="env-head">'
                               f'<span class="env-kicker">K</span></p>'
                               f'<div class="env-body"><p>b</p></div></section>',
                               "workedexample", "靜默")

    def test_env_missing_body(self):
        self.assertRejects('<section class="env env-remark"><p class="env-head">'
                           '<span class="env-kicker">Remark</span></p></section>',
                           "env-body")

    def test_figure_without_datafig(self):
        self.assertRejects('<figure class="figure"><figcaption>x</figcaption></figure>',
                           "data-fig")

    def test_unknown_figure_id_fails(self):
        with self.assertRaises(ConversionError) as cm:
            conv(wrap('<figure class="figure" data-fig="nope"><figcaption>'
                      '<span class="fig-no">Figure 9.9</span> x.</figcaption></figure>'))
        self.assertIn("figures.json", str(cm.exception))

    def test_error_reports_line_number(self):
        # 多行 display math 之後的錯誤，行號仍須精確（占位符補等量換行的理由）
        html = wrap("<p>\\[ a\n  &= b \\\\\n  &= c \\]</p>\n<blockquote>x</blockquote>")
        with self.assertRaises(ConversionError) as cm:
            conv(html)
        self.assertIn(":4:", str(cm.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)

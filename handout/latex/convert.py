#!/usr/bin/env python3
"""HTML fragment -> LaTeX 轉換器（KICKOFF-latex-pilot.md；M-P1 初版、M-B2 重定向）。

    python convert.py appB --out build/appendixB-body.tex
    python convert.py ch03 > chapter3-body.tex

管線：契約方言 -> IR -> emitter。LaTeX 是第一個 emitter；IR 這層是 D4 的 Typst 退路。
純 stdlib（比照 build.py 零 pip 依賴）。

**emitter 目標語言（M-B2 起）＝ template/calcbook.sty 的語意層**，詞彙凍結於
template/M-B1-DECISIONS.md §2；mapping 權威＝chapters/<ch>/DIALECT-<ch>.md（ch03 為基底、appB 為差集）。
v1 的 shell/ book-class 詞彙（hk*）已退場。

三條硬規則：

1. **數學 pass-through 鐵律**：`\\(…\\)`／`\\[…\\]` 內逐字節照抄，禁止 escape／trim／改寫。
   實作上在 HTML 解析「之前」把數學挖成占位符——這不是保險，是必要：ch03 的數學區段裡有
   16 段含 `<`（`\\(0 < \\theta < …\\)`）、9 段含 `&`（aligned 的對齊符），交給 html.parser
   會被當成標籤／entity 吃掉。

2. **fail loud**：mapping 表（DIALECT-ch03.md）以外的 tag／class 一律硬錯，附 fragment＋行號，
   整個 build 失敗。禁止靜默丟棄。

3. **fragment 是唯讀的 canonical 源**，一個字元都不改。

編號照抄字面（D7）：`sec-no`／`env-num`／`fig-no` 當純文字搬運，不開 auto-counter。
"""
import argparse
import html as html_mod
import io
import json
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

HTML_LINE = Path(__file__).resolve().parent.parent / "html"   # 撰稿線（build.py＋fragments）
sys.path.insert(0, str(HTML_LINE))
from build import CHAPTERS  # noqa: E402  —— fragment 順序的單一真實來源

# ── 數學占位符 ────────────────────────────────────────────────────────────────
# 私有使用區字元；escape 表不會碰到它們。占位符不靠「課文不會有這兩個字」的假設——
# 課文能用 &#xE000; 偽造，故另有「每段數學恰好被還原一次、且依源順序」的不變式把關
# （見 LatexEmitter.used 與 convert_chapter 的檢查）。
S_OPEN, S_CLOSE = "", ""
SENTINEL_RE = re.compile(S_OPEN + r"(\d+)" + S_CLOSE)
MATH_RE = re.compile(r"\\\[.*?\\\]|\\\(.*?\\\)", re.S)   # 僅供測試當粗略對照，轉換器不用

OPENERS = {"(": ")", "[": "]"}


class MathScanError(Exception):
    pass


def _line_of(raw, i):
    return raw.count("\n", 0, i) + 1


def extract_math(raw, fname="<input>"):
    """單趟 scanner：把數學挖成占位符。回傳 (帶占位符的 HTML, 數學原文清單)。

    為什麼不用 regex：`\\\\\\(.*?\\\\\\)` 這種非貪婪配對不是封閉的不變式——同類分隔符巢狀
    會提早閉合、未配對不會報錯、`\\\\[` 會被誤認成 display opener、註解裡的數學也會被挖。
    「數學逐位元組照抄」是鐵律，不能靠「ch03 剛好沒有這些情況」成立。故改單趟掃描：

    - HTML 註解整段原樣跳過（不挖裡面的數學，也就不會產生巢狀註解）。
    - 逐字前進時把 `\\X` 當一個單位吃掉，反斜線奇偶自然正確：`\\\\[` 先吃掉 `\\\\`，
      剩下的 `[` 就只是普通字元，不會被當成 display opener。這也讓 aligned 裡的
      `\\\\[2pt]` 不會切斷外層 display math。
    - 同類分隔符巢狀（`\\(…\\(…\\)…\\)`）→ 硬錯。那是合法 LaTeX 但本轉換器不支援，
      寧可報錯也不要靜默排出壞東西；真的遇到再擴充。
    - 未配對的 opener、以及游離的 closer → 硬錯。

    多行 display math 換成單行占位符會讓 getpos() 的行號全部位移、錯誤訊息指錯地方，
    故補一個只含等量換行的 HTML 註解——解析器丟棄它，行號保持精確。
    （fragment 的屬性只有 class/lang/data-fig，都不含數學，注入註解不會壞掉屬性值。）
    """
    # entity 編碼的反斜線會讓 HTML 與 LaTeX 語義分岔：`&#92;(x&#92;)` 在瀏覽器 DOM／MathJax
    # 眼中是數學 `\(x\)`，但 scanner 掃的是尚未解 entity 的原文，看不到分隔符，於是靜默把它
    # 當散文轉成 `\textbackslash{}(x\textbackslash{})`。不屬本方言，硬錯而非默默改語義。
    m = re.search(r"&#0*92;|&#[xX]0*5[cC];|&bsol;", raw)
    if m:
        raise MathScanError(
            f"{fname}:{_line_of(raw, m.start())}: 出現 entity 編碼的反斜線 {m.group(0)!r}——"
            f"瀏覽器會把它還原成 `\\` 並可能構成數學分隔符，但轉換器掃的是未解 entity 的原文，"
            f"兩邊語義會分岔。請在 fragment 直接寫 `\\`。")
    out, store = [], []
    i, n = 0, len(raw)
    while i < n:
        c = raw[i]
        # HTML 註解：原樣抄過，不挖裡面的數學
        if raw.startswith("<!--", i):
            j = raw.find("-->", i + 4)
            if j < 0:
                raise MathScanError(f"{fname}:{_line_of(raw, i)}: HTML 註解沒有收尾 `-->`")
            out.append(raw[i:j + 3])
            i = j + 3
            continue
        if c != "\\":
            out.append(c)
            i += 1
            continue
        nxt = raw[i + 1] if i + 1 < n else ""
        if nxt not in OPENERS:
            if nxt in (")", "]"):
                raise MathScanError(
                    f"{fname}:{_line_of(raw, i)}: 游離的數學收尾 `\\{nxt}`，前面沒有對應的 opener")
            out.append(raw[i:i + 2])       # `\\`、`\%` 等：整組吃掉，反斜線奇偶自然正確
            i += 2
            continue
        # 找同類的收尾
        close = OPENERS[nxt]
        start, k = i, i + 2
        while k < n:
            if raw[k] != "\\":
                k += 1
                continue
            f = raw[k + 1] if k + 1 < n else ""
            if f == close:
                seg = raw[start:k + 2]
                store.append(seg)
                pad = "\n" * seg.count("\n")
                out.append(f"{S_OPEN}{len(store) - 1}{S_CLOSE}")
                if pad:
                    out.append(f"<!--{pad}-->")
                i = k + 2
                break
            if f == nxt:
                raise MathScanError(
                    f"{fname}:{_line_of(raw, k)}: 同類數學分隔符巢狀 `\\{nxt}` … `\\{nxt}`"
                    f"（外層起於第 {_line_of(raw, start)} 行）。這是合法 LaTeX 但轉換器不支援——"
                    f"寧可硬錯也不要靜默排出壞掉的數學。真的需要時再擴充 scanner。")
            k += 2                          # `\\` 等：整組跳過
        else:
            raise MathScanError(
                f"{fname}:{_line_of(raw, start)}: 數學 `\\{nxt}` 沒有配對的 `\\{close}`")
    return "".join(out), store


# ── IR ────────────────────────────────────────────────────────────────────────
@dataclass
class Text:
    s: str


@dataclass
class Emph:
    kids: list


@dataclass
class Strong:
    """run-in 粗體標籤（appB 差集；DIALECT-appB §3）。"""
    kids: list


@dataclass
class Br:
    """手動斷行；僅允許在置中陳述內（appB 差集，sec-b-3 的兩行否定句）。"""


@dataclass
class QedMark:
    """proof 收尾記號（appB 差集）：記號驅動、模板不自動補（DIALECT-appB §7）。"""


@dataclass
class Para:
    kids: list
    variant: str = "normal"          # normal | lead | informal | para-head | center | page-break-before


@dataclass
class ChapterHead:
    kicker: str
    title: list


@dataclass
class SectionHead:
    num: str
    title: list


@dataclass
class SubsecHead:
    kids: list


@dataclass
class Env:
    kind: str                        # definition | theorem | proposition | proof | ...
    kicker: str
    num: str
    name: list
    body: list


@dataclass
class WorkedExample:
    kids: list


@dataclass
class Figure:
    fig_id: str
    fig_no: str
    caption: list


@dataclass
class ListNode:
    ordered: bool
    variant: str
    items: list = field(default_factory=list)


@dataclass
class Block:
    """一個 <article class="sec">：章開場或一節。"""
    kids: list


# ── 解析 ──────────────────────────────────────────────────────────────────────
class ConversionError(Exception):
    pass


@dataclass
class El:
    tag: str
    classes: tuple
    attrs: dict
    line: int
    kids: list = field(default_factory=list)

    @property
    def sel(self):
        return self.tag + ("." + ".".join(self.classes) if self.classes else "")


VOID = {"br", "img", "hr", "meta", "input"}


class FragmentParser(HTMLParser):
    def __init__(self, fname):
        super().__init__(convert_charrefs=True)
        self.fname = fname
        self.root = El("#root", (), {}, 0)
        self.stack = [self.root]
        self.buf = []

    def _flush(self):
        if self.buf:
            s = "".join(self.buf)
            if s.strip():
                self.stack[-1].kids.append(s)
            elif s and self.stack[-1].kids:
                self.stack[-1].kids.append(" ")   # 標籤間的空白仍是字間空白
            self.buf = []

    def handle_starttag(self, tag, attrs):
        self._flush()
        # 重複屬性＝dict(attrs) 折疊時前者靜默消失（gate-2 M-B3 blocking 的實證繞過：
        # style="color:red" style="text-align:center;" 前者被吃掉、整段被當合法置中）。硬錯。
        names = [a for a, _ in attrs]
        dups = sorted({a for a in names if names.count(a) > 1})
        if dups:
            raise ConversionError(
                f"{self.fname}:{self.getpos()[0]}: <{tag}> 屬性重複 {dups}——"
                f"折疊會靜默丟棄前值，屬契約外標記")
        d = dict(attrs)
        # style 白名單的**唯一收口**（DIALECT-appB §2 #7）：只有無 class 的 <p> 允許
        # 字面值 "text-align:center;"。收口放 parser 層＝所有節點（含結構節點 article／
        # env-head／li…）一體適用，不再靠散落在 Builder 各分支的 guard（gate-2 M-B3 blocking）。
        if "style" in d and not (
                tag == "p" and not (d.get("class") or "").split()
                and d["style"] == "text-align:center;"):
            raise ConversionError(
                f"{self.fname}:{self.getpos()[0]}: <{tag}> 帶契約外 style={d['style']!r}——"
                f"只有無 class 的 <p> 允許字面 \"text-align:center;\"（置中陳述）")
        el = El(tag, tuple((d.get("class") or "").split()), d, self.getpos()[0])
        self.stack[-1].kids.append(el)
        if tag not in VOID:
            self.stack.append(el)

    def handle_endtag(self, tag):
        self._flush()
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return
        # 游離的結束標籤：HTMLParser 預設當沒看到。封閉方言不能有靜默修復。
        raise ConversionError(
            f"{self.fname}:{self.getpos()[0]}: 游離的結束標籤 </{tag}>，沒有對應的開始標籤")

    def handle_data(self, data):
        self.buf.append(data)

    # 以下三者 HTMLParser 預設全部靜默吞掉，於是 <![CDATA[DROP]]>、<!DOCTYPE …>、<?pi?>
    # 裡的內容會無聲消失。封閉方言不接受任何一種——fragment 契約裡本來就沒有它們。
    def unknown_decl(self, data):
        raise ConversionError(
            f"{self.fname}:{self.getpos()[0]}: 不支援的宣告 <![{data[:30]}…]>（內容會被靜默丟棄）")

    def handle_decl(self, decl):
        raise ConversionError(
            f"{self.fname}:{self.getpos()[0]}: fragment 不該有 <!{decl[:30]}…> 宣告")

    def handle_pi(self, data):
        raise ConversionError(
            f"{self.fname}:{self.getpos()[0]}: fragment 不該有 processing instruction <?{data[:30]}…>")

    def close(self):
        super().close()
        self._flush()
        return self.root


# ── 方言 -> IR ────────────────────────────────────────────────────────────────
ENV_KINDS = {
    "env-definition", "env-theorem", "env-proposition", "env-proof",
    "env-example", "env-solution", "env-remark", "env-caution", "env-strategy",
}


class Builder:
    """DIALECT-ch03.md＋DIALECT-appB.md 的凍結 mapping 表。表外一律硬錯。"""

    def __init__(self, fname):
        self.fname = fname
        self.n_mapped = 0
        self.n_text = 0
        self.in_we = False        # 目前是否在 div.workedexample 內

    def err(self, el, why):
        raise ConversionError(
            f"{self.fname}:{el.line}: 未知標記 <{el.sel}> — {why}\n"
            f"  轉換器只認 DIALECT-ch03.md／DIALECT-appB.md 的凍結 mapping 表。若這是新方言，"
            f"先更新該表再補 mapping；不要靜默丟棄。"
        )

    def bare(self, parent, k):
        """區塊／容器位置不該有裸文字。靜默丟掉它 ＝ 課文消失卻沒人知道。"""
        if isinstance(k, str) and k.strip():
            self.err(parent, f"此處出現未對映的裸文字 {k.strip()[:40]!r}——"
                             f"靜默丟棄會讓課文無聲消失")
        return isinstance(k, str)

    def once(self, seen, key, el):
        """欄位只能出現一次。

        這些欄位先前都是「後者覆寫前者」——寫兩個 <div class="env-body">，第一個的整段
        內文會無聲消失。重複本身就是契約違反，硬錯即可。
        """
        if key in seen:
            self.err(el, f"<{el.sel}> 重複出現——後者會覆寫前者，前者的內容將無聲消失")
        seen.add(key)

    # ── inline ──
    def inlines(self, kids, parent, allow_br=False):
        out = []
        for k in kids:
            if isinstance(k, str):
                self.n_text += 1
                out.append(Text(k))
                continue
            # style 白名單已在 FragmentParser 收口（parser 層對所有節點一體把關）
            if k.tag == "em" and not k.classes:     # class 也要驗：<em class="x"> 不在契約內
                self.n_mapped += 1
                out.append(Emph(self.inlines(k.kids, k, allow_br)))
            elif k.tag == "strong" and not k.classes:   # appB 差集：run-in 粗體標籤
                self.n_mapped += 1
                out.append(Strong(self.inlines(k.kids, k, allow_br)))
            elif k.tag == "span" and k.classes == ("qed", "qed-proof"):
                # appB 差集：proof 收尾記號。必須是空元素（有內文＝契約外，硬錯）
                if any(isinstance(x, str) and x.strip() or not isinstance(x, str) for x in k.kids):
                    self.err(k, "qed 記號必須是空元素")
                self.n_mapped += 1
                out.append(QedMark())
            elif k.tag == "br" and not k.classes:
                # appB 差集：手動斷行只出現在置中陳述內（sec-b-3:69）；其他位置硬錯
                if not allow_br:
                    self.err(k, "<br> 只允許出現在置中陳述（style=\"text-align:center;\" 的 <p>）內")
                self.n_mapped += 1
                out.append(Br())
            else:
                self.err(k, f"inline 位置（在 <{parent.sel}> 內）只允許文字、無 class 的 "
                            f"<em>／<strong>、qed 記號 span（置中段落內另允許 <br>）")
        return out

    def text_of(self, el):
        """純文字欄位（env-kicker／env-num／sec-no／ch-kicker）。

        嚴格：不遞迴攤平子元素。先前的遞迴版會讓 <strong class="env-kicker"> 這種
        表外標記混進來卻不報錯（其內文被攤平成合法 kicker）。
        """
        parts = []
        for k in el.kids:
            if isinstance(k, str):
                parts.append(k)
            else:
                self.err(k, f"<{el.sel}> 是純文字欄位，不允許子元素 <{k.sel}>")
        return "".join(parts)

    # ── blocks ──
    def blocks(self, kids, parent):
        out = []
        for k in kids:
            if isinstance(k, str):
                if k.strip():
                    self.err(parent, f"區塊位置出現裸文字：{k.strip()[:40]!r}")
                continue
            out.append(self.block(k))
        return out

    def block(self, el):
        self.n_mapped += 1
        t, c = el.tag, el.classes

        # style 白名單已在 FragmentParser 收口；到得了這裡的 style 必為合法置中字面值
        style = el.attrs.get("style")

        if t == "p":
            if style == "text-align:center;":
                return Para(self.inlines(el.kids, el, allow_br=True), variant="center")
            if not c:
                return Para(self.inlines(el.kids, el))
            v = c[0]
            if v in ("lead", "informal", "para-head", "page-break-before") and len(c) == 1:
                return Para(self.inlines(el.kids, el), variant=v)
            self.err(el, "<p> 只允許無 class 或 lead／informal／para-head／page-break-before")

        if t == "h3" and c == ("subsec-head",):
            return SubsecHead(self.inlines(el.kids, el))

        if t in ("ul", "ol"):
            variant = c[0] if c else ""
            if t == "ol" and variant != "steps":
                self.err(el, "<ol> 只允許 class=steps（ch03／appB 未用其他型）")
            if t == "ul" and c not in ((), ("steps",), ("sol-list",)):
                self.err(el, "<ul> 只允許無 class 或 steps／sol-list（appB 差集）")
            if "start" in el.attrs:
                self.err(el, "<ol start> 未在 ch03／appB 出現，mapping 未凍結")
            node = ListNode(ordered=(t == "ol"), variant=variant)
            for k in el.kids:
                if self.bare(el, k):
                    continue
                if k.tag != "li" or k.classes:
                    self.err(k, "清單子元素只允許無 class 的 <li>")
                self.n_mapped += 1
                node.items.append(self.inlines(k.kids, k))
            return node

        if t == "section" and "env" in c:
            kinds = [x for x in c if x in ENV_KINDS]
            if len(kinds) != 1:
                self.err(el, f"env 必須恰有一個環境類別，得到 {c}")
            # class 必須恰好是 {env, env-<kind>}：多餘的 class 代表契約外的樣式，
            # 忽略它就是靜默丟掉作者的意圖
            if set(c) != {"env", kinds[0]}:
                self.err(el, f"env 的 class 必須恰為 env＋env-<kind>，得到 {list(c)}")
            kind = kinds[0][4:]
            # example／solution 只能住在 workedexample 內（CONTRACT「no solo example」；
            # ch03 盤點的 16＋16 個全數如此）。preamble 依賴這個前提：內層不畫色條，
            # 由 workedexample 畫一條共用的。落單的話 LaTeX 會靜默少一條色條，故硬錯。
            if kind in ("example", "solution") and not self.in_we:
                self.err(el, f"env-{kind} 落在 workedexample 之外——"
                             f"calcbook 的 env{kind} 不自畫色條，落單會靜默少畫")
            return self.env(el, kind)

        if t == "div" and c == ("workedexample",):
            self.in_we = True
            try:
                kids = self.blocks(el.kids, el)
            finally:
                self.in_we = False
            # CONTRACT「always paired inside .workedexample — no solo example」。
            # 先前只擋「example/solution 落在 workedexample 外」，沒擋「workedexample 內只有
            # 一半」——那同樣違反契約，且落單的那個會少一條共用色條的語意。
            kinds = [k.kind for k in kids if isinstance(k, Env)]
            if kinds.count("example") != 1 or kinds.count("solution") != 1:
                self.err(el, f"workedexample 必須恰含一個 example 與一個 solution"
                             f"（CONTRACT：no solo example），得到 {kinds}")
            return WorkedExample(kids)

        if t == "figure" and c == ("figure",):
            return self.figure(el)

        if t == "header" and c == ("chapter-head",):
            return self.chapter_head(el)

        if t == "header" and c == ("sec-head",):
            return self.section_head(el)

        self.err(el, "區塊位置的 mapping 表外標記")

    def env(self, el, kind):
        head = body = None
        seen = set()
        for k in el.kids:
            if self.bare(el, k):
                continue
            if k.tag == "p" and k.classes == ("env-head",):
                self.once(seen, "head", k)
                head = k
            elif k.tag == "div" and k.classes == ("env-body",):
                self.once(seen, "body", k)
                body = k
            else:
                self.err(k, "env 內只允許 p.env-head 與 div.env-body")
        if head is None or body is None:
            self.err(el, "env 必須同時有 p.env-head 與 div.env-body")
        self.n_mapped += 2

        kicker = num = ""
        name = []
        seen = set()
        for k in head.kids:
            if self.bare(head, k):
                continue
            if k.tag != "span":
                self.err(k, "env-head 只允許 <span class=env-kicker／env-num／env-name>")
            self.n_mapped += 1
            if k.classes == ("env-kicker",):
                self.once(seen, "kicker", k)
                kicker = self.text_of(k).strip()
            elif k.classes == ("env-num",):
                self.once(seen, "num", k)
                num = self.text_of(k).strip()
            elif k.classes == ("env-name",):
                self.once(seen, "name", k)
                name = self.inlines(k.kids, k)
            else:
                self.err(k, "env-head 只允許 env-kicker／env-num／env-name")
        return Env(kind, kicker, num, name, self.blocks(body.kids, body))

    def figure(self, el):
        if "data-fig" not in el.attrs:
            self.err(el, "figure 必須有 data-fig")
        cap = None
        for k in el.kids:
            if self.bare(el, k):
                continue
            if k.tag == "figcaption" and not k.classes and cap is None:
                cap = k
            else:
                self.err(k, "figure 內只允許恰一個無 class 的 <figcaption>")
        if cap is None:
            self.err(el, "figure 必須有 figcaption")
        self.n_mapped += 1

        fig_no, rest, seen = "", [], set()
        for k in cap.kids:
            if isinstance(k, str):
                rest.append(Text(k))
            elif k.tag == "span" and k.classes == ("fig-no",):
                self.once(seen, "fig-no", k)
                self.n_mapped += 1
                fig_no = self.text_of(k).strip()
            elif k.tag == "em" and not k.classes:      # class 也要驗（漏過的分支之一）
                self.n_mapped += 1
                rest.append(Emph(self.inlines(k.kids, k)))
            else:
                self.err(k, "figcaption 只允許 span.fig-no／文字／無 class 的 <em>")
        return Figure(el.attrs["data-fig"], fig_no, rest)

    def chapter_head(self, el):
        kicker, title, seen = "", [], set()
        for k in el.kids:
            if self.bare(el, k):
                continue
            self.n_mapped += 1
            if k.tag == "div" and k.classes == ("ch-kicker",):
                self.once(seen, "kicker", k)
                kicker = self.text_of(k).strip()
            elif k.tag == "h1" and k.classes == ("ch-title",):
                self.once(seen, "title", k)
                title = self.inlines(k.kids, k)
            else:
                self.err(k, "chapter-head 只允許 div.ch-kicker 與 h1.ch-title")
        return ChapterHead(kicker, title)

    def section_head(self, el):
        # 先前只取第一個元素、其餘不看——sec-head 後面掛任何東西都會被靜默丟掉
        els = [k for k in el.kids if not self.bare(el, k)]
        if len(els) != 1 or els[0].tag != "h2" or els[0].classes != ("sec-title",):
            self.err(el, f"sec-head 必須恰含一個 h2.sec-title，得到 {[e.sel for e in els]}")
        h2 = els[0]
        self.n_mapped += 1
        num, title, seen = "", [], set()
        for k in h2.kids:
            if isinstance(k, str):
                title.append(Text(k))
            elif k.tag == "span" and k.classes == ("sec-no",):
                self.once(seen, "sec-no", k)
                self.n_mapped += 1
                num = self.text_of(k).strip()
            elif k.tag == "em" and not k.classes:      # class 也要驗（漏過的分支之一）
                self.n_mapped += 1
                title.append(Emph(self.inlines(k.kids, k)))
            else:
                self.err(k, "sec-title 只允許 span.sec-no／文字／無 class 的 <em>")
        return SectionHead(num, title)

    def articles(self, root):
        out = []
        for k in root.kids:
            if isinstance(k, str):
                if k.strip():
                    raise ConversionError(f"{self.fname}: fragment 頂層出現裸文字 {k.strip()[:40]!r}")
                continue
            if k.tag != "article" or k.classes != ("sec",):
                self.err(k, "fragment 頂層只允許 <article class=\"sec\">")
            self.n_mapped += 1
            blk = Block(self.blocks(k.kids, k))
            # 開場 article（含 chapter-head）的頂層素 <ul> ＝ objectives 清單
            # （D9／gate-2 B2：獨立語意槽，樣式可單獨調而不動 emitter）。開場結構
            # 已凍結為 chapter-head＋lead＋para-head＋ul（DIALECT-appB §2），此重寫確定。
            if any(isinstance(x, ChapterHead) for x in blk.kids):
                plains = [x for x in blk.kids
                          if isinstance(x, ListNode) and not x.ordered and x.variant == ""]
                # 開場 schema 凍結為「至多一個」objectives 清單；多個素 ul 屬新方言，
                # 硬錯而非全部改寫（gate-2 M-B3 A1：schema 未封閉）
                if len(plains) > 1:
                    raise ConversionError(
                        f"{self.fname}: 開場 article 有 {len(plains)} 個頂層素 <ul>——"
                        f"開場 schema 凍結為恰一個 objectives 清單（M-B1-DECISIONS §2）；"
                        f"新方言先凍結再補 mapping")
                for x in plains:
                    x.variant = "objectives"
            out.append(blk)
        return out


# ── LaTeX emitter ─────────────────────────────────────────────────────────────
ESC = {
    "\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "$": r"\$", "&": r"\&",
    "#": r"\#", "^": r"\textasciicircum{}", "_": r"\_", "~": r"\textasciitilde{}",
    "%": r"\%",
    # U+2002 EN SPACE（appB 的 &ensp;，經 convert_charrefs 解碼而來）：映射間距指令、
    # 不賭 NCM 字型有這個字（DIALECT-appB §5）。
    "\u2002": r"\enspace{}",
}
ESC_RE = re.compile("|".join(re.escape(k) for k in ESC))


def esc(s):
    """散文 escape。Unicode（— § “ ” – ’ …）不轉 ASCII——lualatex＋NCM 原生成立。"""
    return ESC_RE.sub(lambda m: ESC[m.group(0)], s)


class LatexEmitter:
    def __init__(self, math, figs, chapter):
        self.math = math
        self.figs = figs
        self.chapter = chapter
        self.used = []          # 還原過的數學索引，依輸出順序

    # ── inline ──
    def restore(self, s):
        def one(m):
            idx = int(m.group(1))
            if idx >= len(self.math):
                # 只可能來自課文偽造的占位符（例如散文寫了 &#xE000;9&#xE001;）
                raise ConversionError(
                    f"占位符索引 {idx} 超出範圍（共 {len(self.math)} 段數學）——"
                    f"課文疑似含有 U+E000/U+E001 或其 entity 寫法，與轉換器的占位符命名空間衝突")
            self.used.append(idx)
            return self.math[idx]
        return SENTINEL_RE.sub(one, s)

    def inline(self, kids):
        out = []
        for k in kids:
            if isinstance(k, Text):
                # HTML 空白收合——但 U+2002（&ensp; 解碼所得）是承載排版語義的字元，
                # 不能被 \s 吃成普通空格（Python 的 \s 含全部 Unicode 空白），故排除之，
                # 留給 esc() 映射成 \enspace{}。
                s = re.sub(r"[^\S\u2002]+", " ", k.s)
                out.append(self.restore(esc(s)))      # 先 escape 散文，再原樣塞回數學
            elif isinstance(k, Emph):
                out.append(r"\emph{" + self.inline(k.kids) + "}")
            elif isinstance(k, Strong):
                out.append(r"\runin{" + self.inline(k.kids) + "}")
            elif isinstance(k, QedMark):
                out.append(r"\qedmark")
            elif isinstance(k, Br):
                out.append("\\\\\n")
            else:
                raise ConversionError(f"emitter: 未知 inline 節點 {type(k).__name__}")
        return "".join(out)

    def para_text(self, kids):
        return self.inline(kids).strip()

    # ── blocks ──
    def emit(self, blocks):
        return "\n".join(self.block(b) for b in blocks)

    def block(self, b):
        if isinstance(b, Block):
            return self.emit(b.kids)

        if isinstance(b, ChapterHead):
            # 附錄開場變體：kicker 字面驅動（DIALECT-appB §2 #2；不開 counter，D7）
            cmd = "appendixopener" if b.kicker.startswith("Appendix") else "chapteropener"
            return (f"\\{cmd}{{{esc(b.kicker)}}}{{{self.para_text(b.title)}}}")

        if isinstance(b, SectionHead):
            return f"\\sechead{{{esc(b.num)}}}{{{self.para_text(b.title)}}}"

        if isinstance(b, SubsecHead):
            return f"\\subsechead{{{self.para_text(b.kids)}}}"

        if isinstance(b, Para):
            t = self.para_text(b.kids)
            if b.variant == "lead":
                return f"\\begin{{lead}}\n{t}\n\\end{{lead}}"
            if b.variant == "informal":
                return f"\\begin{{informal}}\n{t}\n\\end{{informal}}"
            if b.variant == "para-head":
                return f"\\parahead{{{t}}}"
            if b.variant == "center":
                return f"\\begin{{centerstatement}}\n{t}\n\\end{{centerstatement}}"
            if b.variant == "page-break-before":
                return f"\\pagebreakbefore\n{t}\n"
            return t + "\n"

        if isinstance(b, ListNode):
            if b.variant == "steps":
                envname = "steps" if b.ordered else "bulletsteps"
            elif b.variant == "sol-list":
                envname = "sollist"
            elif b.variant == "objectives":
                envname = "objectives"
            else:
                envname = "enumerate" if b.ordered else "itemize"
            # `\item [x]` 的 `[x]` 會被 LaTeX 當成 optional label 吃掉（bullet 變 x、正文少一截）。
            # 這不是 ESC 表能解的——escape `[` 會讓它在數學外變成別的東西——而是 emitter
            # 要在 \item 之後解除 optional-argument 語境：\relax 一下即可。
            # para_text() 有副作用（記錄數學還原索引），每個 item 只能呼叫一次
            texts = [self.para_text(i) for i in b.items]
            items = "\n".join(
                r"  \item " + (r"\relax " if t.lstrip().startswith("[") else "") + t
                for t in texts)
            return f"\\begin{{{envname}}}\n{items}\n\\end{{{envname}}}"

        if isinstance(b, Env):
            # name 必須在 body **之前**算：兩者都可能含數學，而 used 不變式要求還原順序
            # 等同源順序（env-head 在 env-body 之前）。先算 body 會記成 used=[1,0]，
            # 明明輸出正確卻被不變式誤擋（偽陽性）。ch03 的 13 個 env-name 都沒數學才沒踩到。
            name = self.para_text(b.name) if b.name else ""
            inner = self.emit(b.body).strip()
            return (f"\\begin{{env{b.kind}}}{{{esc(b.kicker)}}}{{{esc(b.num)}}}{{{name}}}\n"
                    f"{inner}\n\\end{{env{b.kind}}}")

        if isinstance(b, WorkedExample):
            inner = self.emit(b.kids).strip()
            return f"\\begin{{workedexample}}\n{inner}\n\\end{{workedexample}}"

        if isinstance(b, Figure):
            return self.figure(b)

        raise ConversionError(f"emitter: 未知區塊節點 {type(b).__name__}")

    def figure(self, f):
        panels = [p for p in self.figs["panels"] if p["id"] == f.fig_id]
        if not panels:
            raise ConversionError(
                f"figure data-fig=\"{f.fig_id}\" 在 figures.json 找不到——"
                f"先跑 export_figs.mjs 產圖")
        # 寬度用實測 mm（DIALECT-ch03.md §5）。不可用 \textwidth：SVG 自帶 inline width，
        # 多數圖只佔約半欄，撐到 \textwidth 會把圖內標籤等比放大。
        art = "\\\\[6pt]\n".join(
            f"  \\includegraphics[width={p['mm']}mm]{{{self.chapter}/{Path(p['file']).stem}}}"
            for p in panels
        ) if len(panels) == 1 else (
            "\\hspace{6mm}".join(
                f"\\includegraphics[width={p['mm']}mm]{{{self.chapter}/{Path(p['file']).stem}}}"
                for p in panels)
        )
        return (f"\\begin{{figureblock}}\n{art}\n"
                f"\\figcaption{{{esc(f.fig_no)}}}{{{self.para_text(f.caption)}}}\n"
                f"\\end{{figureblock}}")


# ── 驅動 ──────────────────────────────────────────────────────────────────────
def convert_chapter(ch_id, figs_path):
    if ch_id not in CHAPTERS:
        sys.exit(f"未知章節 {ch_id}；build.py 的 CHAPTERS 有 {list(CHAPTERS)}")
    # 無圖章節（如 appB）沒有 figures.json——容忍缺檔；一旦遇到 <figure> 仍會
    # 在 emitter 硬錯（「figures.json 找不到——先跑 export_figs.mjs」），fail-loud 不變。
    figs_file = Path(figs_path)
    figs = (json.loads(figs_file.read_text(encoding="utf-8"))
            if figs_file.exists() else {"panels": []})

    parts, stats = [], {"mapped": 0, "text": 0, "math": 0}
    for frag_id in CHAPTERS[ch_id]["fragments"]:
        path = HTML_LINE / "fragments" / ch_id / f"{frag_id}.html"
        raw = path.read_text(encoding="utf-8")
        stripped, math = extract_math(raw, path.name)

        parser = FragmentParser(path.name)
        parser.feed(stripped)
        root = parser.close()

        builder = Builder(path.name)
        ir = builder.articles(root)
        em = LatexEmitter(math, figs, ch_id)
        parts.append(em.emit(ir))

        # 數學 pass-through 鐵律的**封閉不變式**：每段數學恰好被還原一次，且依源順序。
        # 這比「每段都是 .tex 的 substring」強得多——後者驗不到順序、重複次數，
        # 也驗不到「某段根本沒出現在輸出裡」。三種失效各對應一個真 bug：
        #   索引缺席＝該段數學被丟掉；重複＝課文偽造占位符或 emitter 重複輸出；
        #   亂序＝emitter 走訪順序壞了。
        expect = list(range(len(math)))
        if em.used != expect:
            miss = sorted(set(expect) - set(em.used))
            dup = sorted({i for i in em.used if em.used.count(i) > 1})
            raise ConversionError(
                f"{path.name}: 數學 pass-through 不變式失敗——"
                f"應恰好依序還原 {len(math)} 段。"
                + (f" 缺席 {miss[:8]}（該段數學被丟掉了）。" if miss else "")
                + (f" 重複 {dup[:8]}（占位符被偽造或重複輸出）。" if dup else "")
                + ("" if (miss or dup) else " 順序與源順序不符。"))

        stats["mapped"] += builder.n_mapped
        stats["text"] += builder.n_text
        stats["math"] += len(math)

    return "\n\n".join(parts), stats


def _utf8_console():
    """Windows 主控台預設 cp950，一印到數學／繁中就 UnicodeEncodeError。

    文件與交接指令都寫成 `python convert.py ch03`，不該逼每個人自己記得先設
    PYTHONIOENCODING（本輪開發全程手動加，就是這個缺口的現場證據）。
    """
    for s in ("stdout", "stderr"):
        st = getattr(sys, s)
        if hasattr(st, "reconfigure") and (st.encoding or "").lower() not in ("utf-8", "utf8"):
            try:
                st.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, io.UnsupportedOperation):
                pass


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(description="HTML fragment -> LaTeX（pilot）")
    ap.add_argument("chapter", help="章節 id，例如 ch03")
    ap.add_argument("--figs", default=None, help="figures.json 路徑")
    ap.add_argument("--out", default=None, help="輸出 .tex（預設 stdout）")
    a = ap.parse_args()

    figs_path = a.figs or (Path(__file__).parent / "chapters" / a.chapter / "figs" / "figures.json")
    try:
        tex, stats = convert_chapter(a.chapter, figs_path)
    except (ConversionError, MathScanError) as e:
        print(f"\n轉換失敗（fail loud，不靜默丟棄）：\n{e}\n", file=sys.stderr)
        sys.exit(1)

    if a.out:
        Path(a.out).write_text(tex, encoding="utf-8")
    else:
        sys.stdout.write(tex)
    print(f"[convert] {a.chapter}: 元素 {stats['mapped']} mapped / 0 skipped, "
          f"文字節點 {stats['text']}, 數學區段 {stats['math']} pass-through",
          file=sys.stderr)


if __name__ == "__main__":
    main()

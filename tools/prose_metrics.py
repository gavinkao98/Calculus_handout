#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""canonical prose stream 量測器——散文密度指標的單一真實來源。

為什麼存在：本專案有兩條規則線共用「每千詞密度」這把尺——(a) 散文 em-dash
密度（`handout/html/_audit/REPORT-emdash-baseline-and-rollout.md`）、(b) 平實
英文條款的家族命中密度（`CONTENT_SPEC.md` §3）。2026-07-25 實測發現兩線各有
一支腳本、分母定義不同（同一單元 ch07 的 em-dash 數相同、散文詞卻差 3172），
且舊腳本只數字面 `—`、漏掉 appD 的 20 個 `&mdash;` entity，把 appD 誤標為
「無需處理」。本檔把 stream 定義**定版**，兩個指標共用同一個 N。

canonical stream 規則（2026-07-25 與 Codex 議定）：
  納入  正常段落與 environment 正文中的連續自然語言；連結的可見文字。
  排除  行內／display 數學（含 \\text{...}）；標題／env-head／para-head／
        導覽／註解／script／style／隱藏文字；URL 與所有屬性值。
  副表  清單（ul/ol）、表格、figcaption ——主分母排除，另計以供監測。
  entity 只解碼一次：named／decimal／hex 中實際渲染為 U+2014 者計入；
        逸出寫法（`&amp;mdash;`）渲染成字面文字，不計入。
  token  Unicode 字母序列，內部 apostrophe／hyphen 視為同一 token。

用法：
    python tools/prose_metrics.py                 # 全書逐單元（fragments/）
    python tools/prose_metrics.py --unit ch07
    python tools/prose_metrics.py --selftest      # entity／格式回歸測試
    python tools/prose_metrics.py --external      # 外部教材基準（problem_banks/）
"""
from __future__ import annotations

import argparse
import html as _html
import os
import re
import sys
from glob import glob

EM = "\u2014"          # —
EN = "\u2013"          # –
TOKEN_RE = re.compile(r"[^\W\d_]+(?:['\u2019-][^\W\d_]+)*", re.UNICODE)

# ---------------------------------------------------------------- HTML fragment

# 主分母排除的區塊（整段內容不算散文）
_BLOCK_DROP = (
    r"<h[1-6]\b[^>]*>.*?</h[1-6]>",
    r"<p[^>]*class=\"[^\"]*\b(?:env-head|para-head)\b[^\"]*\"[^>]*>.*?</p>",
    r"<figcaption\b[^>]*>.*?</figcaption>",
    r"<(?:ul|ol|table)\b[^>]*>.*?</(?:ul|ol|table)>",
    r"<script\b[^>]*>.*?</script>",
    r"<style\b[^>]*>.*?</style>",
)
_SUB_KEEP = (  # 副表：單獨量測用
    r"<figcaption\b[^>]*>(.*?)</figcaption>",
    r"<(?:ul|ol)\b[^>]*>(.*?)</(?:ul|ol)>",
)


def _strip_math(s: str) -> str:
    """移除 TeX 數學（含 \\text{} 內容）。先 display 再 inline。"""
    s = re.sub(r"\\\[.*?\\\]", " ", s, flags=re.S)
    s = re.sub(r"\\\(.*?\\\)", " ", s, flags=re.S)
    s = re.sub(r"\$\$.*?\$\$", " ", s, flags=re.S)
    s = re.sub(r"(?<!\\)\$.*?(?<!\\)\$", " ", s, flags=re.S)
    return s


def _tags_to_space(s: str) -> str:
    """去標籤（連帶屬性與 URL），保留可見文字。"""
    return re.sub(r"<[^>]+>", " ", s)


def html_streams(src: str) -> tuple[str, str]:
    """回傳 (主 stream, 副 stream)。註解一律先剝除。"""
    body = re.sub(r"<!--.*?-->", " ", src, flags=re.S)

    sub_parts: list[str] = []
    for pat in _SUB_KEEP:
        for m in re.finditer(pat, body, flags=re.S):
            sub_parts.append(m.group(1))

    main = body
    for pat in _BLOCK_DROP:
        main = re.sub(pat, " ", main, flags=re.S | re.I)

    def finish(s: str) -> str:
        s = _strip_math(s)
        s = _tags_to_space(s)
        s = _html.unescape(s)          # 只解碼一次
        return re.sub(r"\s+", " ", s).strip()

    return finish(main), finish(" ".join(sub_parts))


# ------------------------------------------------------------------- PreTeXt/TeX

def pretext_stream(src: str) -> str:
    src = re.sub(r"<!--.*?-->", " ", src, flags=re.S)
    src = re.sub(r"<mdash\s*/>", EM, src)
    src = re.sub(r"<ndash\s*/>", EN, src)
    src = re.sub(r"<(?:m|me|md|mrow|program|input|output|latex-image)\b[^>]*>.*?</(?:m|me|md|mrow|program|input|output|latex-image)>",
                 " ", src, flags=re.S)
    src = re.sub(r"<(?:m|me|md)\s*/>", " ", src)
    src = re.sub(r"<(?:title|idx|xref|url)\b[^>]*>.*?</(?:title|idx|xref|url)>", " ", src, flags=re.S)
    src = _tags_to_space(src)
    src = _html.unescape(src)
    return re.sub(r"\s+", " ", src).strip()


def latex_stream(src: str) -> str:
    src = re.sub(r"(?<!\\)%.*", " ", src)
    src = src.replace("---", EM).replace("--", EN)
    src = re.sub(r"\\begin\{(equation|align|aligned|gather|multline|displaymath|array)\*?\}.*?"
                 r"\\end\{\1\*?\}", " ", src, flags=re.S)
    src = _strip_math(src)
    src = re.sub(r"\\(?:section|subsection|subsubsection|chapter|title|label|ref|cite|index)\s*\*?\s*\{[^}]*\}", " ", src)
    src = re.sub(r"\\text(?:bf|it|rm|sf|tt)?\s*\{([^{}]*)\}", r" \1 ", src)
    src = re.sub(r"\\[A-Za-z@]+\s*\*?", " ", src)
    src = re.sub(r"[{}\\]", " ", src)
    return re.sub(r"\s+", " ", src).strip()


# ---------------------------------------------------------------------- 指標

def metrics(stream: str) -> dict:
    """canonical 指標。tic guard 用的四項標點一併回報。"""
    n_tok = len(TOKEN_RE.findall(stream))
    return {
        "N": n_tok,
        "emdash": stream.count(EM),
        "density": (stream.count(EM) / n_tok * 1000) if n_tok else 0.0,
        # tic guard：de-dash 會把負載推去這些地方
        "colon_clause": len(re.findall(r":\s+[a-z]", stream)),
        "semicolon": stream.count(";"),
        "paren_open": stream.count("("),
        # Codex 2026-07-25 補：成對逗號插入語（總 comma rate 太吵，只抓成對）
        "paired_comma": len(re.findall(r",\s+(?:\w+\s+){1,6}?,\s+", stream)),
    }


def fmt_row(label: str, m: dict, small_unit: bool) -> str:
    dens = f"{m['density']:.1f}" if not small_unit else f"raw {m['emdash']}/{m['N']}"
    return (f"{label:22} {m['N']:>7} {m['emdash']:>6} {dens:>12} "
            f"{m['colon_clause']:>7} {m['semicolon']:>6} {m['paren_open']:>6} {m['paired_comma']:>7}")


HEADER = (f"{'單元／語料':22} {'N':>7} {'—':>6} {'/1000':>12} "
          f"{'冒號':>7} {'分號':>6} {'括號':>6} {'雙逗號':>7}")

SMALL_UNIT_WORDS = 1000  # Codex：<~1000 詞報 raw n/N，不單獨判定通過


# ---------------------------------------------------------------------- selftest

_FIXTURES = [
    # (說明, 輸入, 期望 emdash, 期望 N)
    ("字面 em dash", "<p>alpha \u2014 beta</p>", 1, 2),
    ("named entity", "<p>alpha &mdash; beta</p>", 1, 2),
    ("decimal entity", "<p>alpha &#8212; beta</p>", 1, 2),
    ("hex entity", "<p>alpha &#x2014; beta</p>", 1, 2),
    ("逸出 entity 不計", "<p>alpha &amp;mdash; beta</p>", 0, 3),
    ("en dash 不計", "<p>alpha \u2013 beta</p>", 0, 2),
    ("連字號不計、算一個 token", "<p>well-posed limit</p>", 0, 2),
    ("apostrophe 算一個 token", "<p>Leibniz\u2019s notation</p>", 0, 2),
    ("行內數學排除（含其中的 dash）", "<p>see \\(a \u2014 b\\) here</p>", 0, 2),
    ("display 數學排除", "<p>x</p>\\[ a \u2014 b \\]<p>y</p>", 0, 2),
    ("\\text{} 內容排除", "<p>ok \\(\\text{if alpha \u2014 beta}\\) done</p>", 0, 2),
    ("標題排除", "<h2>Title \u2014 here</h2><p>body word</p>", 0, 2),
    ("env-head 排除", "<p class=\"env-head\">Theorem \u2014 x</p><p>body word</p>", 0, 2),
    ("figcaption 不入主分母", "<figcaption>cap \u2014 tion</figcaption><p>body word</p>", 0, 2),
    ("清單不入主分母", "<ul><li>item \u2014 one</li></ul><p>body word</p>", 0, 2),
    ("屬性與 URL 不計", "<p><a href=\"http://x.example/a\u2014b\" title=\"t \u2014 u\">link text</a></p>", 0, 2),
    ("註解排除", "<!-- note \u2014 hidden --><p>body word</p>", 0, 2),
]

_FIXTURES_TEX = [
    ("LaTeX --- 計為 em dash", "alpha --- beta", 1, 2),
    ("LaTeX -- 為 en dash 不計", "alpha -- beta", 0, 2),
    ("LaTeX $...$ 排除", "see $a --- b$ here", 0, 2),
]

_FIXTURES_PTX = [
    ("PreTeXt <mdash/>", "<p>alpha <mdash/> beta</p>", 1, 2),
    ("PreTeXt <m> 排除", "<p>see <m>a <mdash/> b</m> here</p>", 0, 2),
]


def selftest() -> int:
    bad = 0
    for label, src, want_d, want_n in _FIXTURES:
        m = metrics(html_streams(src)[0])
        ok = (m["emdash"] == want_d and m["N"] == want_n)
        bad += 0 if ok else 1
        print(f"  {'PASS' if ok else 'FAIL'}  {label:34} —={m['emdash']} (期望 {want_d})  N={m['N']} (期望 {want_n})")
    for label, src, want_d, want_n in _FIXTURES_TEX:
        m = metrics(latex_stream(src))
        ok = (m["emdash"] == want_d and m["N"] == want_n)
        bad += 0 if ok else 1
        print(f"  {'PASS' if ok else 'FAIL'}  {label:34} —={m['emdash']} (期望 {want_d})  N={m['N']} (期望 {want_n})")
    for label, src, want_d, want_n in _FIXTURES_PTX:
        m = metrics(pretext_stream(src))
        ok = (m["emdash"] == want_d and m["N"] == want_n)
        bad += 0 if ok else 1
        print(f"  {'PASS' if ok else 'FAIL'}  {label:34} —={m['emdash']} (期望 {want_d})  N={m['N']} (期望 {want_n})")
    print(f"\n{'全部通過' if not bad else str(bad) + ' 項失敗'}（fixture {len(_FIXTURES)+len(_FIXTURES_TEX)+len(_FIXTURES_PTX)} 項）")
    return 1 if bad else 0


# ------------------------------------------------------------------------- main

def read(p: str) -> str:
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def unit_metrics(unit: str) -> tuple[dict, dict]:
    main_parts, sub_parts = [], []
    for f in sorted(glob(f"handout/html/fragments/{unit}/sec-*.html")):
        a, b = html_streams(read(f))
        main_parts.append(a)
        sub_parts.append(b)
    return metrics(" ".join(main_parts)), metrics(" ".join(sub_parts))


def run_units(units: list[str]) -> None:
    print(HEADER)
    print("-" * len(HEADER))
    rows = []
    for u in units:
        m, sub = unit_metrics(u)
        if m["N"] == 0:
            continue
        rows.append((m["density"], u, m, sub))
    for _, u, m, sub in sorted(rows, reverse=True):
        print(fmt_row(u, m, m["N"] < SMALL_UNIT_WORDS))
        print(f"{'  ├ 副表(清單/caption)':22} {sub['N']:>7} {sub['emdash']:>6}")


EXTERNAL = [
    ("mooculus", "problem_banks/mooculus", ("*.tex",), latex_stream),
    ("APEX V5", "problem_banks/APEXCalculusV5", ("*.ptx", "*.xml"), pretext_stream),
    ("CLP1", "problem_banks/CLP1", ("*.ptx", "*.xml"), pretext_stream),
]


def run_external() -> None:
    print(HEADER)
    print("-" * len(HEADER))
    for label, root, pats, fn in EXTERNAL:
        if not os.path.isdir(root):
            print(f"{label:22} (語料不在本機：{root})")
            continue
        parts = []
        for pat in pats:
            for f in glob(os.path.join(root, "**", pat), recursive=True):
                parts.append(fn(read(f)))
        if not parts:
            print(f"{label:22} (找不到符合的檔案 {pats})")
            continue
        m = metrics(" ".join(parts))
        print(fmt_row(label, m, False))


def main() -> int:
    ap = argparse.ArgumentParser(description="canonical prose stream 量測（em-dash 密度＋tic guard）")
    ap.add_argument("--unit", help="只量一個單元，如 ch07")
    ap.add_argument("--selftest", action="store_true", help="entity／格式回歸測試")
    ap.add_argument("--external", action="store_true", help="外部教材基準（problem_banks/）")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.external:
        run_external()
        return 0
    if args.unit:
        run_units([args.unit])
        return 0
    units = sorted({os.path.basename(os.path.dirname(p))
                    for p in glob("handout/html/fragments/*/sec-*.html")})
    run_units(units)
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""方言盤點：掃一章 fragment 的全部 tag/class 組合、數學量、字元用量。

    python dialect_inventory.py ch03

輸出給 DIALECT-<ch>.md 當凍結 mapping 表的依據，也是 rollout 逐章「盤點差集 → 補 mapping」
的工具（KICKOFF-latex-pilot.md §9）。純 stdlib，比照 build.py 零 pip 依賴。

重點：非 ASCII 分「活散文／數學區段／註解」三類統計——只有活散文那類是 LaTeX 的字體風險
（註解會被 convert.py 丟棄，數學走 LaTeX 自己的字型機制）。
"""
import io
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

FRAGROOT = Path(__file__).resolve().parent.parent / "html" / "fragments"
MATH_RE = re.compile(r"\\\[.*?\\\]|\\\(.*?\\\)", re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


class Inventory(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.combos = Counter()
        self.attrs = defaultdict(Counter)
        self.parents = defaultdict(Counter)
        self.stack = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        key = (tag, tuple(sorted((d.get("class") or "").split())))
        self.combos[key] += 1
        for a in d:
            self.attrs[tag][a] += 1
        self.parents[key][self.stack[-1] if self.stack else ("<root>", ())] += 1
        if tag not in ("br", "img", "hr", "meta", "input"):
            self.stack.append(key)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break


def sel(tag, cls):
    return tag + ("." + ".".join(cls) if cls else "")


def _utf8_console():
    """Windows cp950 主控台會在印非 ASCII 盤點結果時 UnicodeEncodeError。"""
    for s in ("stdout", "stderr"):
        st = getattr(sys, s)
        if hasattr(st, "reconfigure") and (st.encoding or "").lower() not in ("utf-8", "utf8"):
            try:
                st.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, io.UnsupportedOperation):
                pass


def main(chapter):
    _utf8_console()
    d = FRAGROOT / chapter
    files = sorted(d.glob("sec-*.html"))
    if not files:
        sys.exit(f"no fragments under {d}")

    inv = Inventory()
    live, mathc, comm = Counter(), Counter(), Counter()
    n_inline = n_display = 0

    for f in files:
        raw = f.read_text(encoding="utf-8")
        inv.feed(raw)
        for c in "".join(COMMENT_RE.findall(raw)):
            if ord(c) > 127:
                comm[c] += 1
        body = COMMENT_RE.sub("", raw)
        for m in MATH_RE.finditer(body):
            n_display += m.group(0).startswith("\\[")
            n_inline += m.group(0).startswith("\\(")
            for c in m.group(0):
                if ord(c) > 127:
                    mathc[c] += 1
        for c in MATH_RE.sub("", body):
            if ord(c) > 127:
                live[c] += 1

    print("=" * 72)
    print(f"{chapter} 方言盤點 — {', '.join(f.name for f in files)}")
    print("=" * 72)

    print(f"\n### tag + class 組合（{len(inv.combos)} 種）\n")
    for (tag, cls), n in sorted(inv.combos.items()):
        parents = ", ".join(sel(*p) for p, _ in inv.parents[(tag, cls)].most_common(3))
        print(f"  {sel(tag, cls):<42} x{n:<5} in: {parents}")

    print("\n### 屬性\n")
    for tag in sorted(inv.attrs):
        print(f"  {tag:<14} {dict(inv.attrs[tag])}")

    print(f"\n### 數學（註解外）\n  inline \\(…\\) x{n_inline}    display \\[…\\] x{n_display}")

    print("\n### 非 ASCII —— 活散文（字體必須有字）\n")
    for c, n in live.most_common():
        print(f"  U+{ord(c):04X}  {c!r}  x{n}")
    print("\n### 非 ASCII —— 數學區段內（走 LaTeX，非字體風險）\n")
    for c, n in mathc.most_common() or [("(無)", 0)]:
        print(f"  {c!r} x{n}" if n else "  （無）")
    print("\n### 非 ASCII —— HTML 註解內（convert.py 丟棄，不進 LaTeX）\n")
    for c, n in comm.most_common():
        print(f"  U+{ord(c):04X}  {c!r}  x{n}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])

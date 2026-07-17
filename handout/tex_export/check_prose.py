#!/usr/bin/env python3
"""完整性閘：fragment 的散文有沒有整段活著抵達 PDF（KICKOFF-latex-pilot.md §4.5 閘 3）。

    python check_prose.py ch03 build/chapter3.pdf

判準＝**依序子序列**：把 fragment 的散文（去註解、去數學、去標籤、解 entity）切成詞流，
檢查每個詞都依原順序出現在 `pdftotext` 的輸出裡。

為什麼不是逐字 diff：數學在兩側是不同的字符流（HTML 走 MathJax，PDF 走 NCM math），
不可能相等；但散文詞必須一個不少、順序不變。這條能抓到**掉段與錯序**；PDF 側合法多出
的東西（頁眉、頁碼、被 pdftotext 當詞的數學字元）是 insert、不在判準內，故**重複輸出
不在本閘範圍**（gate-2 校正原句的過度宣稱）。轉換器側的重複另有把關：數學由
`used == range(N)` 恰一次不變式覆蓋（test_convert.py），散文重複目前無獨立閘。

正規化（兩側都做）：大小寫（env kicker 在 PDF 被 \\MakeUppercase 成大寫）、連字符換行
（LaTeX 斷字產生的 `-\\n`）、Unicode 標點與空白。
"""
import difflib
import io
import json
import html as html_mod
import re
import subprocess
import sys
from pathlib import Path

HANDOUT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HANDOUT))
from build import CHAPTERS  # noqa: E402

MATH_RE = re.compile(r"\\\[.*?\\\]|\\\(.*?\\\)", re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
TAG_RE = re.compile(r"<[^>]*>", re.S)

# 兩側都會做的字元正規化：把排版變體收斂回同一個字
FOLD = {
    "—": " ", "–": " ", "−": " ",      # em/en dash／minus：散文裡一律是有空格的分隔號
    "“": '"', "”": '"', "‘": "'", "’": "'",
    " ": " ", "ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff",
    "ﬃ": "ffi", "ﬄ": "ffl", "­": "",
}


def normalize(s):
    for k, v in FOLD.items():
        s = s.replace(k, v)
    # 連字號在兩側必須同義，否則會冒出假落差。LaTeX 斷字在 PDF 產生 `differen-\n tiable`，
    # 而 fragment 是 `differentiable`；但 fragment 的 `right-hand` 若剛好斷在連字號上，PDF
    # 也是 `right-\n hand`。兩者無法區分，故：先接合行末連字，再把剩下的連字號**刪掉**
    # （不是換成空格）——兩側於是都得到 differentiable／righthand，一致。
    s = re.sub(r"-\s*\n\s*", "", s)
    s = s.replace("-", "")
    s = re.sub(r"[^\w\s]", " ", s)         # 其餘標點不參與比對（斷行會動到它們）
    return [w for w in s.lower().split() if w]


def letters(seq):
    """只留 ASCII 字母——給落差的二次確認用。

    pdftotext 會把行間數學塞進單字中間（實測：`completing` 抽成 `complet𝑑𝑥 𝑑𝑥 ing`）。
    那是抽取假象、不是掉內容，但詞流對齊看不出來；退到「純字母串包含」即可辨識，
    對 1–3 個詞的小落差夠嚴謹。
    """
    return re.sub(r"[^a-z]", "", " ".join(seq).lower())


def fragment_prose(ch_id):
    words = []
    for frag in CHAPTERS[ch_id]["fragments"]:
        raw = (HANDOUT / "fragments" / ch_id / f"{frag}.html").read_text(encoding="utf-8")
        t = COMMENT_RE.sub("", raw)        # 註解不進 LaTeX
        t = MATH_RE.sub(" ", t)            # 數學另有逐位元組保證，不在此閘
        t = TAG_RE.sub(" ", t)
        words += normalize(html_mod.unescape(t))
    return words


def pdf_prose(pdf):
    out = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        sys.exit(f"pdftotext 失敗：{out.stderr}")
    return normalize(out.stdout)


def figure_note_check(figs_json, pdf):
    """圖內文字閘：exporter 申報帶走的 panel note，必須逐條抵達 PDF。

    為什麼要獨立一條：主閘的來源是 fragment，而圖內文字（panel note）住在 standalone 的
    FIGS 物件裡，fragment 一個字都沒有——主閘結構上看不到它們。實際踩過：export_figs 只
    clone <svg>，把 remainder-tangent 兩格的 "larger h"／"smaller h"（<div class="fig-note">，
    svg 的兄弟節點）整個漏掉，主閘卻全綠。

    **這條閘的已知極限（別把它當成它不是的東西）**：oracle 是 exporter 自己申報的 manifest，
    所以它**抓不到 exporter 端的遺漏**——exporter 若又退回只 clone <svg>，它不會申報 notes，
    這裡就會說「無 note 需檢查」然後放行。已實測確認此偽陰性。它能守的是**申報之後**的環節：
    manifest → convert.py → LaTeX → PDF 這段路上把 note 弄丟。

    要真正封閉，oracle 必須獨立於 exporter（例如另一支只讀 live page 的 CDP 探針，
    或拿 HTML 自己印出的 PDF 做逐句 phrase-count 比對）。尚未做，記在 tex_export 的待辦。
    先前試過的兩個做法都被實測否決，留紀錄免得再走一遍：
      (a)「HTML PDF vs LaTeX PDF 詞集比對」——note 是 "larger h"，而 "larger" 在課文散文
         裡也有（the larger triangle OAC…），詞集找得到就誤判成沒掉，放行了要抓的 bug。
      (b) 本函式現行版——oracle 循環，見上。
    """
    figs_file = Path(figs_json)
    if not figs_file.exists():
        # 無圖章節（如 appB）沒有 figures.json——沒有 panel note 可查，非缺漏
        # （與 convert.py 的容忍一致；有 <figure> 的章缺 json 會在轉換階段就硬錯）。
        print("圖內文字閘：本章無 figures.json（無圖章節），略過")
        return True
    figs = json.loads(figs_file.read_text(encoding="utf-8"))
    want = [(p["id"], n) for p in figs["panels"] for n in p.get("notes", [])]
    if not want:
        print("圖內文字閘：無 panel note 需檢查")
        return True
    body = letters(pdf_prose(pdf))
    missing = [(i, n) for i, n in want if letters([n]) not in body]
    if missing:
        print(f"\n圖內文字閘 FAIL：{len(missing)} 條 panel note 沒抵達 PDF")
        for i, n in missing:
            print(f"    {i}: {n!r}")
        return False
    print(f"圖內文字閘 PASS：{len(want)} 條 panel note 全數抵達 PDF"
          + "（" + "、".join(f"{i}:{n!r}" for i, n in want) + "）")
    return True


def _utf8_console():
    """Windows 主控台預設 cp950，一印到數學符號就 UnicodeEncodeError（本閘會印 PDF 抽出的
    數學字元）。文件寫的是 `python check_prose.py …`，不該逼人自己記得設 PYTHONIOENCODING。"""
    for s in ("stdout", "stderr"):
        st = getattr(sys, s)
        if hasattr(st, "reconfigure") and (st.encoding or "").lower() not in ("utf-8", "utf8"):
            try:
                st.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, io.UnsupportedOperation):
                pass


def main():
    _utf8_console()
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    ch_id, pdf = sys.argv[1], Path(sys.argv[2])

    src = fragment_prose(ch_id)
    got = pdf_prose(pdf)
    print(f"fragment 散文詞 {len(src)}    PDF 文字詞 {len(got)}")

    # 用序列對齊而非貪婪子序列：PDF 合法地多出東西（數學符號被 pdftotext 當詞、每頁重複的
    # running header、頁碼），那些是 insert；只有 delete 才是真的掉了散文。
    # autojunk 必須關掉——它會把出現率 >1% 的元素（the／of／is…）當雜訊，整個比對就廢了。
    sm = difflib.SequenceMatcher(None, src, got, autojunk=False)
    deletions = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("delete", "replace"):
            deletions.append((i1, i2, src[i1:i2], got[j1:j2]))

    if not deletions:
        print("完整性閘 PASS：fragment 的散文詞全部出現在 PDF，順序一致")
        # 這裡曾直接 return，於是散文完全乾淨時圖內文字閘根本不會跑（只因目前剛好有
        # 2 處 pdftotext 抽取假象才一直觸發到它）。閘不能因為別的閘過了就跳過。
        if not figure_note_check(Path(__file__).parent / "figs" / ch_id / "figures.json", pdf):
            sys.exit(1)
        return

    # 二次確認：詞流對不上、但純字母串仍包含 → pdftotext 抽取假象，非掉內容。
    real, artifacts = [], []
    for d in deletions:
        (artifacts if letters(d[2]) and letters(d[2]) in letters(d[3]) else real).append(d)

    for i1, i2, lost, ins in artifacts:
        print(f"\n  [抽取假象] src[{i1}:{i2}] {' '.join(lost)!r}")
        print(f"      PDF 抽成: {' '.join(ins)[:90]!r}  —— 純字母串仍含之，內容在")
    for i1, i2, lost, ins in real[:15]:
        ctx = " ".join(src[max(0, i1 - 6):i1])
        print(f"\n  [真落差] src[{i1}:{i2}]  …{ctx}…")
        print(f"      fragment 有: {' '.join(lost)[:110]}")
        print(f"      PDF 對應處 : {' '.join(ins)[:110] or '（空）'}")

    n = sum(i2 - i1 for i1, i2, _, _ in real)
    if real:
        print(f"\n完整性閘 FAIL：{len(real)} 處真落差，共 {n} 個散文詞不在 PDF")
        sys.exit(1)
    print(f"\n完整性閘 PASS：{len(artifacts)} 處 pdftotext 抽取假象（已逐條確認內容在），0 處真落差")
    if not figure_note_check(Path(__file__).parent / "figs" / ch_id / "figures.json", pdf):
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""字形閘：PDF 印出來的字形，是不是它宣稱的那個字（KICKOFF-latex-pilot.md §4.5 閘 4）。

    python check_glyphs.py dist/appB/appendixB.pdf

判準＝**逐 CID 比對輪廓**：PDF 每個嵌入子集的每個 CID，其字形輪廓必須與原始字型同一
GID 的輪廓相同（Identity-H＋CIDFontType0C 的 CID 恰為原字型 GID）。比的是 pen 畫出來的
路徑、不是 charstring 位元組——子集器合法地會重寫 charstring（subroutinize、重排 hint），
那些不該算落差；輪廓才是「印出來長什麼樣」。

為什麼要有一條「看字形」的閘：閘 1–3 結構上都看不到這個維度。閘 1 只問有沒有 missing
character，閘 2 只問 hbox，閘 3 的 check_prose.py 走 `pdftotext`——讀的是 **ToUnicode
文字層**。而 2026-07-17 實際踩到的 bug 正是「文字層全對、印出來是別的字」：Inter 4.001
的 static OTF 其 CFF charset 含重複字形名稱（直立體 123 個、義體 92 個，首見 GID 151
`G.1`），LuaTeX 預設 node mode 以**字形名稱**索引字形，重複名塌陷後輪廓與 charset 錯位。
appB 單頁 30 個 Inter 字形有 22 個印成別的字（頁碼 9 印成 7、EXAMPLE 印成 EWALjŒKE），
CID／ToUnicode／charset 卻全對——四閘全綠。修法是模板給 Inter 指定 `Renderer=HarfBuzz`
（以 GID 索引，不受重複名影響）；本閘是那個 bug 的回歸閘。

比「截圖比對」好在：確定性、不需人眼、且直接斷言因果層（輪廓 vs CID），不是斷言像素
（像素會被 dpi／抗鋸齒／renderer 版本影響，還得養一堆基準圖）。

**這條閘的已知極限（別把它當成它不是的東西）**：
  - 只驗「輪廓對不對」，不驗「擺得對不對」。字距、letterspacing、定位、斷行壞掉，
    本閘一律看不到——那是閘 2 與人眼的範圍。
  - 只驗 CFF（FontFile3／CIDFontType0C）。遇到非 CFF 或非 CID-keyed 的嵌入字型、或
    找不到原始字型檔，一律 **FAIL 並指名**，不默默略過——silent skip 正是
    check_prose.py 的 figure_note_check 記錄過的偽陰性坑，不重蹈。
"""
import io
import re
import subprocess
import sys
from pathlib import Path

import fitz
from fontTools.cffLib import CFFFontSet
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

VENDORED = Path(__file__).resolve().parent / "template" / "fonts" / "inter"
SUBSET_TAG = re.compile(r"^\w{6}\+")            # 子集前綴 `IQGLBE+Inter-Bold`
FONTNAME_RE = re.compile(r"/FontName\s*/([^\s/\[\]<>]+)")
FONTFILE_RE = re.compile(r"/FontFile(\d?)\s+(\d+)\s+0\s+R")

_orig_cache = {}


def find_original(basefont):
    """PostScript name → 原始字型檔。vendored Inter 優先，其次 kpsewhich（NCM 等 TeX 樹字型）。

    兩邊的 PostScript name 都恰好等於檔名主幹（Inter-Bold.otf／NewCM10-Regular.otf），
    故直接接檔名；不成立時回 None，由呼叫端 FAIL 而非猜。
    """
    name = SUBSET_TAG.sub("", basefont)
    vendored = VENDORED / f"{name}.otf"
    if vendored.exists():
        return vendored
    out = subprocess.run(["kpsewhich", f"{name}.otf"], capture_output=True, text=True)
    found = Path(out.stdout.strip()) if out.stdout.strip() else None
    return found if found and found.exists() else None


def original(path):
    """原始字型的 (CharStrings, charset)；charset[gid] 即該 GID 的字形名。"""
    if path not in _orig_cache:
        cff = TTFont(path)["CFF "].cff
        td = cff[cff.fontNames[0]]
        _orig_cache[path] = (td.CharStrings, td.charset)
    return _orig_cache[path]


def outline(charstrings, name):
    """字形畫出來的路徑，座標取到 0.1 單位。

    不能用完全相等：子集器會重新編碼 charstring，座標因定點數往返而帶 ~1e-5 級的浮點噪音
    （實測 NCM 的 `h`：原字型 442.0162353515625 → 子集 442.01625061035156，28 個操作全同、
    形狀無異）。em = 1000 單位、不同字形的差距是幾百單位，取到 0.1 濾得掉噪音又不可能把
    兩個不同的字收斂成一個——2026-07-17 的 Inter bug 是整個字母換掉，照樣抓得到（已實測）。
    """
    pen = RecordingPen()
    charstrings[name].draw(pen)
    return tuple((op, tuple(round(c, 1) for pt in args for c in pt)) for op, args in pen.value)


def embedded_fonts(doc):
    """PDF 裡每個嵌入字型 → (basefont, FontFile 種類, 資料 xref)。"""
    for xref in range(1, doc.xref_length()):
        obj = doc.xref_object(xref)
        name, ff = FONTNAME_RE.search(obj), FONTFILE_RE.search(obj)
        if name and ff:
            yield name.group(1), ff.group(1), int(ff.group(2))


def audit(doc, basefont, data):
    """回傳 (檢查數, 錯誤清單)；錯誤為 (cid, 宣稱字形, 實際看起來是什麼)。"""
    path = find_original(basefont)
    if path is None:
        raise LookupError(f"找不到 {SUBSET_TAG.sub('', basefont)}.otf（vendored 與 kpsewhich 都沒有）")
    cffs = CFFFontSet()
    cffs.decompile(io.BytesIO(data), None)
    td = cffs[cffs.fontNames[0]]
    if not hasattr(td, "ROS"):
        raise LookupError(f"{basefont} 的嵌入子集不是 CID-keyed，CID 不等於 GID，本閘無法驗")

    ocs, ochar = original(path)
    # 反查表：輪廓 → 原字型的字形名。純為了讓 FAIL 訊息能講出「實際畫的是哪個字」——
    # 有重複輪廓的字型（Inter 的 G 與 G.1 輪廓相同）反查會歸給先出現的那個，故僅供診斷。
    by_outline = {}
    for n in ochar:
        by_outline.setdefault(outline(ocs, n), n)

    bad = []
    for name in td.charset[1:]:                  # [0] 恆為 .notdef
        cid = int(name[3:])
        claims = ochar[cid]
        got = outline(td.CharStrings, name)
        if got != outline(ocs, claims):
            looks = by_outline.get(got, "?")
            bad.append((cid, claims, looks))
    return len(td.charset) - 1, bad


def _utf8_console():
    """Windows 主控台預設 cp950，一印到字形名（Œ、ß…）就 UnicodeEncodeError。
    文件寫的是 `python check_glyphs.py …`，不該逼人自己記得設 PYTHONIOENCODING。"""
    for s in ("stdout", "stderr"):
        st = getattr(sys, s)
        if hasattr(st, "reconfigure") and (st.encoding or "").lower() not in ("utf-8", "utf8"):
            try:
                st.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, io.UnsupportedOperation):
                pass


def main():
    _utf8_console()
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    doc = fitz.open(sys.argv[1])

    total, failures, unchecked = 0, [], []
    for basefont, kind, xref in embedded_fonts(doc):
        if kind != "3":
            unchecked.append(f"{basefont}：FontFile{kind}（非 CFF）")
            continue
        try:
            n, bad = audit(doc, basefont, doc.xref_stream(xref))
        except LookupError as e:
            unchecked.append(f"{basefont}：{e}")
            continue
        total += n
        print(f"  {SUBSET_TAG.sub('', basefont):22s} {n:3d} 字形 → {len(bad)} 個輪廓不符")
        failures += [(basefont, *b) for b in bad]

    for u in unchecked:
        print(f"  [未驗] {u}")
    for basefont, cid, claims, looks in failures[:20]:
        print(f"\n  [輪廓不符] {basefont} cid{cid:05d}")
        print(f"      宣稱是: {claims}")
        print(f"      實際畫的看起來是: {looks}")

    if failures or unchecked:
        why = []
        if failures:
            why.append(f"{len(failures)} 個字形的輪廓不是它宣稱的字")
        if unchecked:
            why.append(f"{len(unchecked)} 個嵌入字型無法驗")
        print(f"\n字形閘 FAIL：{'；'.join(why)}")
        sys.exit(1)
    print(f"\n字形閘 PASS：{total} 個嵌入字形的輪廓全數符合其 CID")


if __name__ == "__main__":
    main()

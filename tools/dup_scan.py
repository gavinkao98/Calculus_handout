# -*- coding: utf-8 -*-
"""重複片語掃描：抓「替換字串尾端與後文重複」這類 bug（ch07 的 E-08 實例）。

為什麼需要：verify_edits.py 只證明「替換恰好套用一次」，證不出語意重複；
figcaption 又不入 canonical 主分母，散文閘也掃不到。這個洞是靠 LaTeX 閘 5
（人眼看排版）才發現的，補一支程式化前哨。
"""
import io, os, re, sys, glob, html as H
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, os.path.abspath("tools"))
from prose_metrics import TOKEN_RE, _strip_math, _tags_to_space

N = 6        # 片語長度（連續詞）
WINDOW = 70  # 只看近距離重複；遠距離的是正常的教學重述

def text(src):
    b = re.sub(r"<!--.*?-->", " ", src, flags=re.S)
    return re.sub(r"\s+", " ", H.unescape(_tags_to_space(_strip_math(b)))).strip()

unit = sys.argv[1] if len(sys.argv) > 1 else "ch07"
hits = 0
for f in sorted(glob.glob(f"handout/html/fragments/{unit}/sec-*.html")):
    k = os.path.basename(f)[4:-5]
    w = TOKEN_RE.findall(text(open(f, encoding="utf-8").read()))
    seen = {}
    for i in range(len(w) - N + 1):
        g = " ".join(x.lower() for x in w[i:i + N])
        if g in seen and i - seen[g] < WINDOW:
            print(f"  ★ {k}  間隔 {i - seen[g]} 詞：「{g}」")
            hits += 1
        seen[g] = i
print(f"  命中 {hits} 處" if hits else f"  {unit} clean：{N} 連詞在 {WINDOW} 詞窗口內無重複")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""交易式改動驗證器：證明「工作樹 ＝ 某個 rev ＋ 恰好這些字串替換」。

為什麼存在：散文平實化／de-dash 這類輪次會在一個檔裡動十幾處措辭。光看
`git diff` 能看到改了什麼，但看不出「有沒有順手動到不該動的地方」——尤其
數學、標籤、cross-ref。de-dash 線（2026-07-20）用的 **reverse-apply == HEAD**
byte-for-byte 證明比「數學片段 diff」更強：把改動逆轉後與 HEAD 完全相同，
即證明「HEAD ＋ 恰好這些改動、其餘一字未動」。2026-07-25 合併兩線時，Codex
指出平實線缺這一環，本檔補上。

用法（每筆 old→new 各佔一行，以 tab 或 ` ==> ` 分隔；`#` 開頭為註解）：

    python tools/verify_edits.py <file> <edits.txt> [--rev HEAD]

edits.txt 範例：
    or, far more often, the search ==> or — far more often — the search

判定：
  * 每筆 old 在 rev 版本中 MUST 恰好命中一次（命中 0 或 ≥2 → 判 FAIL，
    因為那代表替換不具確定性）；
  * 全部替換後的結果 MUST 與工作樹當前內容 byte-for-byte 相同；
  * 兩者皆成立才 PASS，並附「未被涵蓋的差異」為 0 的結論。
"""
from __future__ import annotations

import argparse
import subprocess
import sys


def read_rev(rev: str, path: str) -> str:
    p = path.replace("\\", "/")
    r = subprocess.run(["git", "show", f"{rev}:{p}"], capture_output=True)
    if r.returncode != 0:
        sys.exit(f"無法取得 {rev}:{p} —— {r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout.decode("utf-8")


def parse_edits(path: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    with open(path, encoding="utf-8") as fh:
        for ln, raw in enumerate(fh, 1):
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if "\t" in line:
                old, new = line.split("\t", 1)
            elif " ==> " in line:
                old, new = line.split(" ==> ", 1)
            else:
                sys.exit(f"edits 第 {ln} 行無分隔符（用 tab 或 ' ==> '）：{line[:60]}")
            out.append((old, new))
    if not out:
        sys.exit("edits 檔沒有任何替換")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="驗證工作樹 == rev ＋ 恰好這些替換")
    ap.add_argument("file")
    ap.add_argument("edits")
    ap.add_argument("--rev", default="HEAD")
    a = ap.parse_args()

    base = read_rev(a.rev, a.file)
    with open(a.file, encoding="utf-8") as fh:
        current = fh.read()

    edits = parse_edits(a.edits)
    work = base
    bad = 0
    for i, (old, new) in enumerate(edits, 1):
        hits = work.count(old)
        if hits != 1:
            print(f"  FAIL  #{i} old 命中 {hits} 次（須恰好 1）：{old[:70]!r}")
            bad += 1
            continue
        work = work.replace(old, new, 1)
        print(f"  ok    #{i} 命中 1 次 → 已替換")

    if bad:
        print(f"\nFAIL：{bad} 筆替換不具確定性，未做 byte 比對。")
        return 1

    if work == current:
        print(f"\nPASS：{a.file} == {a.rev} ＋ 恰好這 {len(edits)} 筆替換"
              f"（reverse-apply byte-for-byte 相同；未涵蓋的差異 0 處）。")
        return 0

    # 找出第一處未涵蓋的差異，便於定位
    n = min(len(work), len(current))
    at = next((k for k in range(n) if work[k] != current[k]), n)
    print(f"\nFAIL：仍有未涵蓋的差異，首見於 offset {at}")
    print(f"  依 edits 推得: {work[max(0, at-60):at+60]!r}")
    print(f"  工作樹實際  : {current[max(0, at-60):at+60]!r}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/deai/build_seed.py — 組裝去 AI 味種子 reject 清單（PLAN-deai-flavor §4.2）。

從 repo 根跑：

    python tools/deai/build_seed.py            # 產 styles/.../AItexture/reject.txt
    python tools/deai/build_seed.py --check    # 只比對、不寫（CI/守門用，差異則 exit 1）

做什麼：把「保守起步」的內建 banned-starter（§4.2，寧缺勿濫求低誤砍）與**有授權來源**
（berenslab/Wikipedia/stop-slop，由 curator 先抽成純文字行放進 `tools/deai/sources/*.txt`）
合併，**用 accept.txt 過濾掉合法數學詞**，去重＋排序，寫成 Vale vocab `reject.txt`。

設計約束（依 CLAUDE.md「缺套件先問、不造輪子、簡單優先」）：
- **不連網**：不自動下載任何清單；授權來源由人工 curate 後放 `sources/`（避開授權/數學詞誤砍判斷）。
- **accept.txt 是人工 curate 的白名單『輸入』**，本程式只讀它當過濾器，**絕不覆寫**（curation 守門見 check_seed.py）。
- Vale vocab 檔格式：一行一個 term、**不支援註解**——故輸出純 term、無 header；全小寫（Vale 比對 ignorecase）。
- 種子最終組成是 §6-1 使用者 sign-off 項；本檔產的是「待校準的保守初版」，門檻/誤砍率在 Ch1 校準（Task 1.2）定。
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
VOCAB = REPO / "styles" / "config" / "vocabularies" / "AItexture"
SOURCES = Path(__file__).resolve().parent / "sources"

# 保守起步的 banned-starter（§4.2 + Task 0.2 Step 3，寧缺勿濫）。
# 單一連接詞（Moreover/This means that…）刻意**不**放——會在合法數學散文誤砍；
# 那些密度型 tell 由 Vale 自訂 rule（Phrases/Copula/Negative）＋人審維度 C 的密度線管。
BASE_REJECT = [
    "delve into",
    "it is worth noting that",
    "it is important to note that",
    "in this section we will explore",
    "let us turn our attention to",
    "serves as a",
    "stands as a testament to",
    "plays a crucial role in",
    "plays a pivotal role in",
    "the fundamental building block of",
    "rich tapestry",
    "ever-evolving landscape",
    "underscoring the importance of",
    "a powerful and elegant tool",
]


def _norm(lines) -> list[str]:
    """strip、去空白行、去 # 註解行、轉小寫。"""
    out = []
    for ln in lines:
        s = ln.strip().lower()
        if s and not s.startswith("#"):
            out.append(s)
    return out


def load_sources() -> list[str]:
    """讀 tools/deai/sources/*.txt（若有）的額外片語；無此目錄則回空。"""
    if not SOURCES.is_dir():
        return []
    extra: list[str] = []
    for f in sorted(SOURCES.glob("*.txt")):
        extra += _norm(f.read_text(encoding="utf-8").splitlines())
    return extra


def build() -> tuple[list[str], list[str]]:
    """回傳 (reject 排序清單, 被 accept 過濾掉的詞)。"""
    accept = set(_norm((VOCAB / "accept.txt").read_text(encoding="utf-8").splitlines()))
    candidates = _norm(BASE_REJECT) + load_sources()
    kept, filtered = set(), set()
    for c in candidates:
        (filtered if c in accept else kept).add(c)
    return sorted(kept), sorted(filtered)


def main(argv: list[str]) -> int:
    check_only = "--check" in argv[1:]
    reject, filtered = build()
    target = VOCAB / "reject.txt"
    new_text = "\n".join(reject) + "\n"

    if check_only:
        cur = target.read_text(encoding="utf-8") if target.exists() else ""
        if cur != new_text:
            print("DRIFT: reject.txt 與 build_seed.py 產出不一致；跑 `python tools/deai/build_seed.py` 重產。")
            return 1
        print(f"OK(check): reject={len(reject)}")
        return 0

    VOCAB.mkdir(parents=True, exist_ok=True)
    target.write_text(new_text, encoding="utf-8")
    src_note = f"，併入 sources/ {len(load_sources())} 行" if load_sources() else "（無 sources/，純內建 starter）"
    filt_note = f"；accept 過濾掉 {filtered}" if filtered else ""
    print(f"OK: 寫入 {target}（reject={len(reject)}）{src_note}{filt_note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

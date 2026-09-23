#!/usr/bin/env python3
r"""build.py —— LaTeX 統一（U1）後的日常編譯入口：src/<ch>/*.tex → dist/<ch>/*.pdf。

    python build.py ch08          # 編譯一個單元
    python build.py all           # 編譯全部 12 單元

每單元流程：latexmk -lualatex（aux 進 build/aux-<ch>/）→ log 閘（0 error／
0 missing character／0 undefined reference／0 multiply-defined label；overfull 逐條列出
供裁決）→ 字形閘（check_glyphs.py）→
成品 PDF 移入 dist/<ch>/。任何一閘不過即以非零退出碼停下。

沿革：取代 make_dist.py（fragment→轉換→內嵌 的產線，隨 HTML 撰稿線於 P1 退役；
留檔供歷史參照，勿再對已升格單元使用——它會用凍結的 fragment 覆寫 dist）。
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

UNITS = {
    "appA": "appendixA", "appB": "appendixB", "appC": "appendixC", "appD": "appendixD",
    "ch01": "chapter1", "ch02": "chapter2", "ch03": "chapter3", "ch04": "chapter4",
    "ch05": "chapter5", "ch06": "chapter6", "ch07": "chapter7", "ch08": "chapter8",
}


def print_tail(label, text, n=6):
    """FAIL 時印子程序輸出的最後 n 行（capture 起來的輸出，不印就沒人看得到）。"""
    lines = (text or "").strip().splitlines()[-n:]
    if lines:
        print(f"    ── {label}（最後 {len(lines)} 行）")
        for ln in lines:
            print("   ", ln)


def build(ch):
    name = UNITS[ch]
    srcdir = HERE / "src" / ch
    tex = srcdir / f"{name}.tex"
    if not tex.exists():
        sys.exit(f"{ch}: 找不到源 {tex}")

    # nonstopmode＋halt-on-error：不指定時 lualatex 是 errorstopmode，錯誤會停在 `?` 提示等 stdin
    # （提示寫進被 capture 的 stdout，人看不到）；stdin 接 DEVNULL 是第二道保險。
    r = subprocess.run(
        ["latexmk", "-lualatex", "-interaction=nonstopmode", "-halt-on-error",
         f"-auxdir=../../build/aux-{ch}", f"{name}.tex"],
        cwd=srcdir, stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8",
        errors="replace")
    log_path = HERE / "build" / f"aux-{ch}" / f"{name}.log"
    log = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""

    errors = len(re.findall(r"^!", log, re.M))
    missing = log.count("Missing character")
    overfull = [ln for ln in log.splitlines() if ln.startswith("Overfull")]
    pdf = srcdir / f"{name}.pdf"
    # \ref 解析不了、label 重複定義：latexmk 照樣 rc=0，PDF 印著 ?? 或錯號（CONTRACT 要求 log 無
    # undefined reference）。TeX 在 79 字元處硬斷行，長 key 的 warning 會被切開——先接回再抓 key；
    # 抓不到 key 時，LaTeX 的摘要行本身仍算數。
    flat = re.sub(r"^(.{79})\n", r"\1", log, flags=re.M)
    undefined = sorted(set(re.findall(r"Reference `(.+?)' on page \S+ undefined", flat)))
    multiply = sorted(set(re.findall(r"Label `(.+?)' multiply defined", flat)))
    refs_bad = (undefined or multiply or "There were undefined references" in log
                or "There were multiply-defined labels" in log)

    if r.returncode != 0 or errors or missing or refs_bad or not pdf.exists():
        print(f"{ch}: FAIL  latexmk rc={r.returncode} error={errors} missing-char={missing}"
              f" undefined-ref={len(undefined)} multiply-defined={len(multiply)}")
        for ln in re.findall(r"^!.*", log, re.M)[:5]:
            print("   ", ln)
        for key in undefined:
            print("    undefined reference:", key)
        for key in multiply:
            print("    multiply defined label:", key)
        if refs_bad and not (undefined or multiply):
            print(f"    log 有 undefined／multiply-defined 摘要但抓不到 key，見 {log_path}")
        if not errors and not (undefined or multiply):
            # log 沒有 `!` 也沒有 key 可列（例如 latexmk 自己出錯、沒跑到 TeX）：原因只在它的輸出裡
            print_tail("latexmk stdout", r.stdout)
            print_tail("latexmk stderr", r.stderr)
        sys.exit(1)

    g = subprocess.run([sys.executable, "check_glyphs.py", f"src/{ch}/{name}.pdf"],
                       cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if g.returncode != 0 or "字形閘 PASS" not in g.stdout:
        print(f"{ch}: FAIL  字形閘 rc={g.returncode}——")
        print("\n".join(g.stdout.strip().splitlines()[-6:]))
        print_tail("check_glyphs stderr", g.stderr)     # 閘本身崩潰時 traceback 只在這裡
        sys.exit(1)

    dist = HERE / "dist" / ch
    dist.mkdir(parents=True, exist_ok=True)
    shutil.move(str(pdf), str(dist / f"{name}.pdf"))

    note = f"；overfull {len(overfull)} 條待裁決" if overfull else ""
    print(f"{ch}: PASS  0 err／0 missing-char／字形閘綠 → dist/{ch}/{name}.pdf{note}")
    for ln in overfull:
        print("   ", ln)


def main():
    if len(sys.argv) != 2 or (sys.argv[1] != "all" and sys.argv[1] not in UNITS):
        sys.exit(__doc__)
    targets = list(UNITS) if sys.argv[1] == "all" else [sys.argv[1]]
    for ch in targets:
        build(ch)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
r"""產「成品夾」：dist/<ch>/ 裡乾乾淨淨兩個檔——<name>.tex（自足、可直接編譯）＋<name>.pdf。

    python make_dist.py appB

流程：convert.py 確定性轉換 fragment → body 內嵌進單一 .tex（不再 \input gitignored 的
build/ 中間檔）→ 從 dist/<ch>/ 為 CWD 編譯（aux 全部丟 build/aux/<ch>/，資料夾保持兩檔）
→ log 驗收（0 error／0 missing character）。

設計要點：
- dist/<ch>/<name>.tex 是**自動產生的成品源**（比照 html/standalone/ 的「committed 生成物」
  慣例）：內容改了就重跑本工具，重跑必 byte-identical（convert.py 確定性）。勿手改。
- 模板仍是唯一樣式權威（template/calcbook.sty）；成品 .tex 只帶三行定位（input@path＋
  \cbfontsdir 覆蓋），任何支援 lualatex 的環境對它直接編譯即可重現 PDF。
- 圖章節（rollout）：emitter 目前射 `<ch>/<stem>` 形式的 \includegraphics，dist 需配
  \graphicspath 對回 chapters/<ch>/figs/——首個有圖章 rollout 時在此補（KICKOFF §4.4）。
"""
import io
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from convert import convert_chapter  # noqa: E402

HERE = Path(__file__).resolve().parent

# 單元 id → 成品檔名（與 chapters/<ch>/ driver 同名；rollout 逐章加）
NAMES = {
    "appB": "appendixB",
    "ch03": "chapter3",
}

HEADER = """% !TeX program = lualatex
% ============================================================
% {name}.tex — {ch} 出版成品（自動產生，勿手改）
% 產生：cd handout/latex && python make_dist.py {ch}
%   內容源＝handout/html/fragments/{ch}/（fragment 唯讀；數學逐位元組 pass-through）
%   樣式源＝../../template/calcbook.sty（M-B1 拍板模板）
% 直接重編（本資料夾為 CWD；aux 進 build/、資料夾保持兩檔）：
%   latexmk -lualatex -auxdir=../../build/aux-{ch} {name}.tex
% ============================================================
\\documentclass[a4paper,12pt,oneside]{{memoir}}
\\makeatletter\\def\\input@path{{{{../../template/}}}}\\makeatother
\\def\\cbfontsdir{{../../template/fonts/inter/}}
\\usepackage{{calcbook}}
\\begin{{document}}
"""

FOOTER = "\\end{document}\n"


def make(ch_id):
    if ch_id not in NAMES:
        sys.exit(f"未知單元 {ch_id!r}（目前支援：{'、'.join(NAMES)}；rollout 新章先補 NAMES 表）")
    name = NAMES[ch_id]
    figs = HERE / "chapters" / ch_id / "figs" / "figures.json"
    tex_body, stats = convert_chapter(ch_id, figs)

    out_dir = HERE / "dist" / ch_id
    out_dir.mkdir(parents=True, exist_ok=True)
    tex_path = out_dir / f"{name}.tex"
    tex_path.write_text(HEADER.format(name=name, ch=ch_id) + tex_body + FOOTER,
                        encoding="utf-8", newline="\n")
    print(f"[dist] {tex_path.relative_to(HERE)}  （{stats['math']} 段數學 pass-through）")

    # 注意：資料夾不能叫 `aux`——Windows 保留裝置名（AUX/CON/NUL…）建不出來
    aux = HERE / "build" / f"aux-{ch_id}"
    aux.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        ["latexmk", "-lualatex", f"-auxdir={aux}", f"{name}.tex"],
        cwd=out_dir, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-1000:], sep="\n")
        sys.exit(f"latexmk 失敗（exit {r.returncode}）")

    log = (aux / f"{name}.log").read_text(encoding="utf-8", errors="replace")
    pages = re.findall(r"Output written on .* \((\d+) pages", log)
    missing = log.count("Missing character")
    errors = log.count("\n!")
    print(f"[dist] {name}.pdf：{pages[-1] if pages else '?'} 頁、error {errors}、missing char {missing}")
    if errors or missing or not pages:
        sys.exit("編譯驗收未過（見 build/aux 的 log）")

    # 資料夾潔癖：任何落在成品夾的編譯殘渣都清掉（成品夾永遠只有 .tex＋.pdf）
    for p in out_dir.iterdir():
        if p.suffix not in (".tex", ".pdf"):
            p.unlink()
    left = sorted(p.name for p in out_dir.iterdir())
    print(f"[dist] {out_dir.relative_to(HERE)}/ ＝ {left}")


def _utf8_console():
    for s in ("stdout", "stderr"):
        st = getattr(sys, s)
        if hasattr(st, "reconfigure") and (st.encoding or "").lower() not in ("utf-8", "utf8"):
            try:
                st.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, io.UnsupportedOperation):
                pass


if __name__ == "__main__":
    _utf8_console()
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    make(sys.argv[1])

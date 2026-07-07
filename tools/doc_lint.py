"""doc_lint.py — 指引文檔斷鏈 lint（stdlib-only）。

掃描 git 追蹤的 *.md 中的相對 markdown 連結 `[text](path)`，驗證目標檔案存在。
起因：2026-07-07 產線總體檢驗出多起「檔案改名／搬家後指引文檔連結失效」
（如 pipeline/coverage.py → step_coverage.py），全屬機械可抓；本 lint 即其回歸網
（前身＝legacy/tex_handout/tools/book_docs_lint.py 的連結檢查，隨 LaTeX 樹封存）。

規則：
  - 只驗「活文檔」：排除 legacy/、problem_banks/、_archive/、_dev-archive/、.claude/、
    .tmp/、stewart/（封存與第三方各自宣告路徑可能過時，不在此驗）。
  - 只驗相對路徑連結；http(s)/mailto/純 #anchor 略過；目標的 #anchor 片段先剝除。
  - 目標存在（檔或目錄）即過；不驗 anchor 是否存在（保持輕量）。

用法：python tools/doc_lint.py    # exit 0 = 乾淨；exit 1 = 有斷鏈（逐條列出）
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

EXCLUDE_PREFIXES = (
    "legacy/",
    "problem_banks/",
    ".claude/",
    ".tmp/",
    "stewart/",
)
EXCLUDE_PARTS = ("_archive", "_dev-archive", "node_modules", ".venv")

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def tracked_markdown() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "*.md"],
        cwd=REPO, capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    files = []
    for rel in out:
        if rel.startswith(EXCLUDE_PREFIXES):
            continue
        if any(part in EXCLUDE_PARTS for part in Path(rel).parts):
            continue
        if "-raw." in Path(rel).name:  # 模型 raw 轉錄檔：偽連結多，不驗
            continue
        files.append(REPO / rel)
    return files


def check_file(path: Path) -> list[str]:
    problems = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in LINK.finditer(line):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#", "<")):
                continue
            target = target.split("#", 1)[0]
            target = re.sub(r":\d+$", "", target)  # 允許 path:line 形式的行號後綴
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                rel = path.relative_to(REPO)
                problems.append(f"{rel}:{lineno}: broken link -> {m.group(1)}")
    return problems


def main() -> int:
    problems: list[str] = []
    for path in tracked_markdown():
        problems.extend(check_file(path))
    if problems:
        print(f"doc_lint: {len(problems)} broken link(s)")
        for p in problems:
            print("  " + p)
        return 1
    print("doc_lint: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())

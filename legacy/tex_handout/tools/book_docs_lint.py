"""Lint the repo's markdown docs for two classes of stale reference:

1. ``python tools/<name>.py`` or ``python .\\tools\\<name>.py`` command lines
   whose target no longer exists in ``tools/``.
2. Markdown link targets ``](<path>)`` whose file does not exist.

The Phase 1/2 restructure renamed many markdown files and every ``tools/*.py``.
Without an automated check it is easy to miss an occurrence in a code block or
a legacy link, which then silently misleads the reader. This lint is the cheap
prophylactic: run it locally before committing and as a CI step alongside
``book_style_lint`` and ``book_preamble_smoketest``.

Scope:
- Scans every ``*.md`` file under the repository root.
- Skips hidden caches and vendored deps (``.git``, ``.claude``, ``.venv``,
  ``.deps``, ``.deps_f5``, ``.cache``, ``node_modules``).
- Tool invocations are checked regardless of whether the line sits inside a
  fenced code block, because the doc examples live in fenced blocks by
  convention.
- Markdown link targets are checked only outside fenced code blocks, so that
  literal ``](example)`` inside a code sample demonstrating link syntax does
  not produce false positives.
- External URLs (``http://``, ``https://``, ``mailto:``) and pure anchor
  fragments (``#section``) are skipped.

Exit code 0 on success, 1 on any violation. Run via::

    python tools/book_docs_lint.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {
    ".git",
    ".claude",
    ".venv",
    ".deps",
    ".deps_f5",
    ".cache",
    "node_modules",
    # Frozen gen-0/gen-1 media pipelines, archived verbatim. Their docs keep
    # original ``tools/<name>.py`` command examples and cross-links that point
    # at the pre-archive layout; we do not re-lint reference material.
    "legacy",
    # Third-party problem-bank clones (gitignored vendored repos with their own
    # internal READMEs; see problem_banks/README.md).
    "problem_banks",
}

# Pattern: ``python tools/X.py`` or ``python .\tools\X.py`` (with either slash).
# Captures the bare tool name. Anchored on the ``tools`` directory token so
# coincidental ``_.py`` mentions in prose are not picked up.
TOOL_PATTERN = re.compile(r"\btools[\\/]([A-Za-z0-9_]+)\.py\b")

# Pattern: ``](target)`` markdown link body. Captures everything up to the
# first ``)``. Good enough for the project's docs; targets with literal ``)``
# inside are rare and can be handled as exceptions if they ever appear.
LINK_PATTERN = re.compile(r"\]\(([^)]+)\)")

# Prefixes that mark a link as external (do not need to exist on disk).
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "git@", "ftp://")


def _should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts)


def _collect_markdown_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.md") if not _should_skip(p))


def _check_tool_invocation(tool_name: str) -> str | None:
    tool_path = ROOT / "tools" / f"{tool_name}.py"
    if tool_path.exists():
        return None
    return f"missing tool: tools/{tool_name}.py"


def _check_link_target(md_file: Path, raw_target: str) -> str | None:
    target = raw_target.strip()
    if not target:
        return None
    if target.startswith(EXTERNAL_PREFIXES):
        return None
    if target.startswith("#"):
        return None
    # Strip optional title: ``target "Title"``.
    target = target.split(" ", 1)[0]
    # Strip anchor fragment.
    path_part = target.split("#", 1)[0]
    if not path_part:
        return None
    candidate = (md_file.parent / path_part).resolve()
    if candidate.exists():
        return None
    return f"missing link target: {path_part}"


def _lint_file(md_file: Path) -> list[tuple[int, str]]:
    text = md_file.read_text(encoding="utf-8")
    violations: list[tuple[int, str]] = []
    in_fence = False
    for idx, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        for match in TOOL_PATTERN.finditer(line):
            err = _check_tool_invocation(match.group(1))
            if err is not None:
                violations.append((idx, f"invocation: {err}"))
        if in_fence:
            continue
        for match in LINK_PATTERN.finditer(line):
            err = _check_link_target(md_file, match.group(1))
            if err is not None:
                violations.append((idx, f"link: {err}"))
    return violations


def main() -> int:
    total = 0
    for md_file in _collect_markdown_files():
        violations = _lint_file(md_file)
        if not violations:
            continue
        rel = md_file.relative_to(ROOT)
        for line_num, message in violations:
            print(f"{rel}:{line_num}: {message}")
            total += 1

    if total:
        print(f"book_docs_lint: {total} violation(s)")
        return 1
    print("book_docs_lint: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())

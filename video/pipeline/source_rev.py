"""source_rev.py -- content-script <-> handout-source freshness stamp (warn-only).

A LOCKED content script (video/content_scripts/<deck>.md) was written against ONE
version of its handout section, and nothing in the pipeline noticed when the handout
moved on: the 2026-09-07 pipeline assessment (F2) found §3.1/§3.2 sources edited three
times after lock, narration still quoting sentences the handout no longer has, and no
mechanism that would ever say so. This module is the same trick derived_check.py plays
for *_mimo.yml, one layer up: the .md header carries a stamp of the handout file it was
written against, and every preflight (schema.py / make.py / derive_spoken.py) re-hashes
that file and WARNS on drift -- the trigger for CONTENT_METHODOLOGY.md §8 (diff ->
surgical edit -> scoped NFA -> re-stamp). Warn-only by design: drift is a content
decision, never a build error, so it must not gate a render.

Header line (anywhere in the .md header, i.e. before the first `### unit:`):

    > **source_rev：** `handout/latex/src/ch03/chapter3.tex` `sha256:<64 hex>` — <free text>

The path is repo-relative (forward slashes); the hash is the LF-normalized sha256 of the
file (derived_check.text_sha256 -- this repo has core.autocrlf=true). Print a fresh line
for a source file, then paste it into the header:

    python video/pipeline/source_rev.py handout/latex/src/ch03/chapter3.tex

Files whose name starts with `_` (fixtures / demos, repo convention) are never checked.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.derived_check import text_sha256  # noqa: E402

LIVE_SOURCE = "handout/latex/src/<ch>/*.tex"

# `source_rev：` / `source_rev:` (full-width or ASCII colon), optional **bold** markers,
# then the two back-ticked tokens. The 64-hex constraint makes a truncated hash "no stamp".
_STAMP = re.compile(r"source_rev[：:]\**\s*`([^`\n]+)`\s*`sha256:([0-9a-f]{64})`", re.IGNORECASE)
_LOCKED = re.compile(r"\bLOCKED\b")
_UNIT_HEADER = re.compile(r"^###\s+unit:\s+\S+")


def header_of(md_path: Path) -> str:
    """The .md header: every line before the first `### unit:` (same cut as
    review_pack.parse_content_script, duplicated here to stay import-light)."""
    lines: list[str] = []
    for ln in md_path.read_text(encoding="utf-8").splitlines():
        if _UNIT_HEADER.match(ln):
            break
        lines.append(ln)
    return "\n".join(lines)


def parse_stamp(header: str) -> "tuple[str, str] | None":
    """(repo-relative path, sha256 hex) if the header carries a well-formed stamp, else None."""
    m = _STAMP.search(header)
    return (m.group(1).strip(), m.group(2).lower()) if m else None


def stamp_line(source: Path, repo_root: Path) -> str:
    """The header line to paste for `source` (LF-normalized sha of its CURRENT content)."""
    rel = source.resolve().relative_to(repo_root.resolve()).as_posix()
    return (f"> **source_rev：** `{rel}` `sha256:{text_sha256(source)}` — "
            "撰稿／lock 時所依講義源的 LF 正規化 sha256；schema／make／derive preflight 比對現檔，"
            "不符即 `[source_rev]` WARN＝講義已變 → 走 CONTENT_METHODOLOGY.md §8 後重蓋"
            "（產生器：`python video/pipeline/source_rev.py <源檔>`）。")


def md_for_deck(meta: dict, repo_root: Path) -> Path:
    """The content script a storyboard derives from (`<deck>_mimo` -> `<deck>.md`);
    thin alias of provenance.content_script_for so the strip lives in one place."""
    from pipeline.provenance import content_script_for
    return content_script_for(meta, repo_root)


def check_source_rev(md_path: Path, repo_root: Path) -> "list[tuple[str, str]]":
    """(severity, message) findings for one content script -- severity is always 'warn'.
    No file / fixture (`_`-prefixed) / DRAFT-without-stamp -> []. LOCKED-without-stamp,
    stamped-file-missing, hash-drift, and a stamp pointing at frozen legacy HTML all warn."""
    if not md_path.exists() or md_path.name.startswith("_"):
        return []
    name = md_path.name
    header = header_of(md_path)
    stamp = parse_stamp(header)
    if stamp is None:
        if _LOCKED.search(header):
            return [("warn", f"{name}: LOCKED content script has no source_rev stamp -- add one "
                             f"(python video/pipeline/source_rev.py <handout source>)")]
        return []
    rel, sha = stamp
    src = repo_root / rel
    legacy = rel.startswith("legacy/")
    if not src.exists():
        return [("warn", f"{name}: stamped source {rel} not found (moved?) -- re-stamp against "
                         f"{LIVE_SOURCE}")]
    if text_sha256(src) != sha:
        tail = f" (stamp is the frozen legacy HTML; the live source is {LIVE_SOURCE})" if legacy else ""
        # messages stay ASCII: derive_spoken.py prints them on a possibly-cp950 console
        return [("warn", f"{name}: handout source {rel} changed since the content script was "
                         f"stamped{tail} -- CONTENT_METHODOLOGY.md section 8: diff -> surgical edit -> "
                         f"scoped NFA -> re-stamp")]
    if legacy:
        return [("warn", f"{name}: stamped against frozen legacy HTML {rel}; the live handout "
                         f"source is {LIVE_SOURCE} -- re-stamp against the .tex once reconciled (section 8)")]
    return []


def main(argv: "list[str] | None" = None) -> int:
    import argparse

    for stream in (sys.stdout, sys.stderr):   # the stamp line carries CJK; keep cp950 consoles alive
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Print the source_rev header line for a handout source file.")
    ap.add_argument("source", type=Path, help="handout source the content script is written against "
                                              "(repo-relative or absolute)")
    args = ap.parse_args(argv)
    repo_root = Path(__file__).resolve().parents[2]
    src = args.source if args.source.is_absolute() else repo_root / args.source
    if not src.exists():
        print(f"[source_rev] no such file: {src}", file=sys.stderr)
        return 1
    print(stamp_line(src, repo_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

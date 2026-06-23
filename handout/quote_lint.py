#!/usr/bin/env python3
"""Quote linter / fixer for the live HTML handout (CONTENT_SPEC §8).

Enforces: rendered prose uses Unicode curly quotes “…” / ‘…’ and the
curly apostrophe ’ (U+2019); ASCII straight quotes (" and ') are NOT
allowed in prose.

It is deliberately scoped to *rendered prose*. A structural classifier
excludes, and never touches, ASCII quotes that legitimately stay ASCII:

  - math      : the prime in \\(f'\\), \\[f''\\], $f'$ — MathJax notation
  - tag       : HTML attribute values, e.g. class="sec"
  - code/kbd  : literal syntax shown to the reader
  - comment   : <!-- authoring notes --> (not rendered)

Only ASCII ' or " that survive that filter — i.e. sit in running prose —
are reported (or rewritten with --fix). Stdlib-only (matches build.py),
so CI needs no pip install.

Usage:
    python handout/quote_lint.py              # lint handout/fragments/**/*.html
    python handout/quote_lint.py --fix        # rewrite prose ASCII quotes -> curly
    python handout/quote_lint.py PATH ...     # lint/fix specific files or dirs

Conversion (--fix):
    prose '  ->  ’  (U+2019)        apostrophe / closing single — unambiguous
    prose "  ->  “ / ”             alternating per file in document order
                                    (handout prose uses flat, non-nested pairs;
                                    an odd count per file is refused so a stray
                                    quote is never mis-paired — fix it by hand).
After --fix, review the diff and re-run `python handout/build.py`.

Exit code (lint mode) 0 = clean, 1 = violations found.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SPAN_PATTERNS = [
    ("comment", re.compile(r"<!--.*?-->", re.S)),
    ("math", re.compile(r"\\\[.*?\\\]", re.S)),
    ("math", re.compile(r"\\\(.*?\\\)", re.S)),
    ("math", re.compile(r"\$\$.*?\$\$", re.S)),
    ("math", re.compile(r"(?<![\\$])\$(?!\$).+?(?<![\\$])\$(?!\$)", re.S)),
    ("code", re.compile(r"<code[^>]*>.*?</code>", re.S)),
    ("code", re.compile(r"<kbd[^>]*>.*?</kbd>", re.S)),
    ("tag", re.compile(r"<[^>]+>", re.S)),
]
_EXCLUDE_KINDS = ("comment", "math", "code", "tag")
RSQUO, LDQUO, RDQUO = "’", "“", "”"


def _build_spans(text: str) -> list[tuple[int, int, str]]:
    spans = []
    for kind, pat in SPAN_PATTERNS:
        for m in pat.finditer(text):
            spans.append((m.start(), m.end(), kind))
    return spans


def _in_excluded_span(pos: int, spans: list[tuple[int, int, str]]) -> bool:
    for kind in _EXCLUDE_KINDS:
        for s, e, k in spans:
            if k == kind and s <= pos < e:
                return True
    return False


def _prose_positions(text: str, spans):
    """Yield (pos, char) for each ASCII ' or " that sits in rendered prose."""
    for m in re.finditer(r"['\"]", text):
        if not _in_excluded_span(m.start(), spans):
            yield m.start(), m.group()


def lint_text(text: str) -> list[tuple[int, str, str]]:
    """Return [(line_no, char, context), ...] for prose ASCII-quote violations."""
    spans = _build_spans(text)
    out = []
    for pos, ch in _prose_positions(text, spans):
        line_no = text.count("\n", 0, pos) + 1
        ctx = text[max(0, pos - 30):pos + 30].replace("\n", " ")
        out.append((line_no, ch, ctx))
    return out


def fix_text(text: str) -> tuple[str, int]:
    """Rewrite prose ASCII quotes to curly. Returns (new_text, n_changed).

    Raises ValueError if a file has an odd number of prose double quotes
    (a stray " that cannot be paired) so the author can resolve it by hand.
    """
    spans = _build_spans(text)
    prose = list(_prose_positions(text, spans))
    dq = [p for p, ch in prose if ch == '"']
    if len(dq) % 2 != 0:
        raise ValueError(
            f"odd number of prose double quotes ({len(dq)}) — a stray \" cannot "
            f"be paired; fix manually"
        )
    repl = {}
    for p, ch in prose:
        if ch == "'":
            repl[p] = RSQUO
    for i, p in enumerate(dq):
        repl[p] = LDQUO if i % 2 == 0 else RDQUO
    if not repl:
        return text, 0
    buf, last = [], 0
    for p in sorted(repl):
        buf.append(text[last:p])
        buf.append(repl[p])
        last = p + 1
    buf.append(text[last:])
    return "".join(buf), len(repl)


def _iter_html(paths: list[Path]):
    for p in paths:
        if p.is_dir():
            yield from sorted(p.rglob("*.html"))
        elif p.suffix == ".html":
            yield p


def main(argv: list[str]) -> int:
    do_fix = "--fix" in argv
    args = [a for a in argv if a != "--fix"]
    if args:
        targets = [Path(a) for a in args]
    else:
        targets = [Path(__file__).resolve().parent / "fragments"]

    files = list(_iter_html(targets))

    if do_fix:
        total = 0
        for fp in files:
            text = fp.read_text(encoding="utf-8")
            try:
                new_text, n = fix_text(text)
            except ValueError as exc:
                print(f"{fp}: {exc}", file=sys.stderr)
                return 1
            if n:
                fp.write_text(new_text, encoding="utf-8", newline="")
                total += n
                print(f"{fp}: fixed {n} prose ASCII quote(s)")
        if total:
            print(
                f"\nquote_lint --fix: rewrote {total} prose quote(s) across "
                f"{len(files)} file(s). Review the diff and re-run "
                f"`python handout/build.py`."
            )
        else:
            print(f"quote_lint --fix: nothing to fix — {len(files)} file(s) already clean.")
        return 0

    total = 0
    for fp in files:
        text = fp.read_text(encoding="utf-8")
        violations = lint_text(text)
        if violations:
            total += len(violations)
            for line_no, ch, ctx in violations:
                kind = "apostrophe/single" if ch == "'" else "double quote"
                print(f"{fp}:{line_no}: ASCII {kind} in prose — use a curly quote (§8): …{ctx}…")

    if total:
        print(
            f"\nquote_lint: {total} prose ASCII-quote violation(s) in "
            f"{len(files)} file(s). Run `python handout/quote_lint.py --fix` "
            f"to auto-convert, then re-run `python handout/build.py`.",
            file=sys.stderr,
        )
        return 1
    print(f"quote_lint: clean — {len(files)} file(s), no prose ASCII quotes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

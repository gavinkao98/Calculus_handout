"""texparts.py -- the two cuts a math line needs for the motion language, manim-free so
schema.py can count segments without importing manim.

SEGMENTS (kickoff T3-1). An author marks the units of a formula that move as one:
``"{{a}} + {{b}} = {{c}}"``. brand.math_line builds ``MathTex(*segments)`` so each is one
submobject, and derivation's ``anim: transform`` / ``anim: cancel`` key on them. The split
follows manim's own double-brace rule (``MathTex._split_double_braces``, parity pinned in
``_selftest_tex_parts``): ``{{`` opens a group only at the start of the string or right after
whitespace (so ``x^{{2}}`` is ordinary LaTeX), ``}}`` closes it at inner brace depth 0, and
``\\\\`` / ``\\{`` / ``\\}`` are atomic. Text between groups is a segment of its own; segments
are stripped and whitespace-only ones dropped (a zero-glyph part has no SVG group to match).

TOKENS (kickoff T1-2). ``meta.color_map`` keys are matched on a token stream -- ``\\macro``,
``\\x`` (control symbol), or one character -- never as raw substrings: manim's
``tex_to_color_map`` cuts ``h`` out of ``\\theta`` and ``\\right`` and LaTeX refuses to
compile (probe 2026-09-13). A key matches only whole tokens, longest key first.
"""
from __future__ import annotations

import re

_TOKEN = re.compile(r"\\[A-Za-z]+|\\.|.", re.S)


def _split_double_braces(s: str) -> "tuple[list[str], bool]":
    """manim's rule, verbatim: (pieces including empties, whether any group was found)."""
    pieces: list[str] = []
    cur = ""
    i, n = 0, len(s)
    inside, depth, found = False, 0, False
    while i < n:
        if s[i] == "\\" and i + 1 < n and s[i + 1] in "\\{}":
            cur += s[i:i + 2]
            i += 2
            continue
        if not inside:
            if s[i:i + 2] == "{{" and (i == 0 or s[i - 1].isspace()):
                pieces.append(cur)
                cur, inside, depth, found = "", True, 0, True
                i += 2
            else:
                cur += s[i]
                i += 1
        elif s[i] == "{":
            depth += 1
            cur += s[i]
            i += 1
        elif s[i] == "}" and depth == 0 and s[i:i + 2] == "}}":
            pieces.append(cur)
            cur, inside = "", False
            i += 2
        elif s[i] == "}":
            depth -= 1
            cur += s[i]
            i += 1
        else:
            cur += s[i]
            i += 1
    pieces.append(cur)
    return pieces, found


def split_segments(src: str) -> list[str]:
    """The author's ``{{...}}`` segments of *src*, in order; ``[src]`` when it has none."""
    pieces, _ = _split_double_braces(src)
    out = [p.strip() for p in pieces if p.strip()]
    return out or [src.strip()]


def has_segments(src: str) -> bool:
    return _split_double_braces(src)[1]


def tokens(s: str) -> list[str]:
    return _TOKEN.findall(s)


def split_tokens(seg: str, keys: "list[str]") -> "list[tuple[str, str | None]]":
    """Cut *seg* into runs ``(piece, key)``: a piece with a key is exactly one occurrence of
    that key (whole tokens only, longest key first); the rest carry ``None``."""
    toks = tokens(seg)
    wanted = sorted(((tokens(k), k) for k in keys if k), key=lambda kt: -len(kt[0]))
    out: list[tuple[str, str | None]] = []
    buf: list[str] = []
    i = 0
    while i < len(toks):
        hit = next(((kt, k) for kt, k in wanted if toks[i:i + len(kt)] == kt), None)
        if hit is None:
            buf.append(toks[i])
            i += 1
            continue
        if buf:
            out.append(("".join(buf), None))
            buf = []
        out.append((hit[1], hit[1]))
        i += len(hit[0])
    if buf:
        out.append(("".join(buf), None))
    return out

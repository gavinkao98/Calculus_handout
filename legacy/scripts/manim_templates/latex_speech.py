"""LaTeX -> spoken English token approximation.

Used by ``anchors.py`` to predict where in the narration each math element
should fire. The output is **not** a faithful TTS-style verbalisation; it
is a list of token strings to grep for in the narration. Coverage focus:

- Powers: ``x^2`` -> ``"x squared"``, ``x^3`` -> ``"x cubed"``,
  ``x^n`` -> ``"x to the n"``
- Roots: ``\sqrt{x}`` -> ``"square root of x"``,
         ``\sqrt[3]{x}`` -> ``"cube root of x"``
- Greek letters used in calculus: epsilon, delta, alpha, beta, gamma, ...
- Inverse: ``f^{-1}`` -> ``"f inverse"`` / ``"inverse of f"``
- Comparators: ``=``, ``\le``, ``\ge`` -> ``"equals"``, ``"less than or equal"``,
  ``"greater than or equal"``
- Fractions: ``\frac{a}{b}`` -> ``"a over b"``

The acceptance bar (per migration plan §3.2) is >=80% anchor hit rate on
ch01_inverse_functions + ch01_precise_limit. Symbols not covered fall
through to the literal LaTeX string, which the caller may also try as an
anchor before declaring failure.
"""
from __future__ import annotations

import re
from typing import Iterable


# ─── Greek letter map ──────────────────────────────────────────────────────
_GREEK = {
    "alpha": "alpha",
    "beta": "beta",
    "gamma": "gamma",
    "delta": "delta",
    "epsilon": "epsilon",
    "varepsilon": "epsilon",
    "zeta": "zeta",
    "eta": "eta",
    "theta": "theta",
    "lambda": "lambda",
    "mu": "mu",
    "nu": "nu",
    "xi": "xi",
    "pi": "pi",
    "rho": "rho",
    "sigma": "sigma",
    "tau": "tau",
    "phi": "phi",
    "varphi": "phi",
    "chi": "chi",
    "psi": "psi",
    "omega": "omega",
}


_ORDINAL_POWERS = {
    "0": "zero",
    "1": "first power",  # rarely useful
    "2": "squared",
    "3": "cubed",
    "4": "to the fourth",
    "5": "to the fifth",
    "6": "to the sixth",
    "7": "to the seventh",
    "8": "to the eighth",
    "9": "to the ninth",
    "10": "to the tenth",
}


_NUMBER_WORD = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
    "10": "ten",
}


# ─── Token extractors ──────────────────────────────────────────────────────

def latex_to_speech_tokens(latex: str) -> list[str]:
    """Return a deduplicated list of speech-style tokens approximating the
    LaTeX source. The first element is always the cleaned LaTeX itself
    (without delimiters), so callers can fall back to literal matching.
    """
    if not latex:
        return []

    cleaned = _strip_latex_delimiters(latex)
    tokens: list[str] = []
    seen: set[str] = set()

    def add(t: str) -> None:
        t = t.strip()
        if not t or t.lower() in seen:
            return
        tokens.append(t)
        seen.add(t.lower())

    add(cleaned)
    add(_strip_braces(cleaned))

    # Powers: x^2, x^3, x^{2}, etc.
    for m in re.finditer(r"([A-Za-z])\^(?:\{?(\d+)\}?)", cleaned):
        base, exp = m.group(1), m.group(2)
        suffix = _ORDINAL_POWERS.get(exp)
        if suffix:
            add(f"{base} {suffix}")
        else:
            add(f"{base} to the {exp}")

    # Subscripts: x_1 -> "x one", "x sub one"; also "x 1" as fallback
    for m in re.finditer(r"([A-Za-z])_(?:\{?(\d+)\}?)", cleaned):
        base, idx = m.group(1), m.group(2)
        word = _NUMBER_WORD.get(idx, idx)
        add(f"{base} {word}")
        add(f"{base} sub {word}")
        add(f"{base}_{idx}")
    # Subscripts with letters: x_n
    for m in re.finditer(r"([A-Za-z])_(?:\{?([A-Za-z])\}?)", cleaned):
        base, idx = m.group(1), m.group(2)
        add(f"{base} {idx}")
        add(f"{base} sub {idx}")

    # Inverse: f^{-1}
    for m in re.finditer(r"([A-Za-z])\^\{-1\}", cleaned):
        base = m.group(1)
        add(f"{base} inverse")
        add(f"inverse of {base}")

    # Roots
    for m in re.finditer(r"\\sqrt\{([^{}]+)\}", cleaned):
        inner = m.group(1).strip()
        add(f"square root of {inner}")
    for m in re.finditer(r"\\sqrt\[(\d+)\]\{([^{}]+)\}", cleaned):
        n, inner = m.group(1), m.group(2).strip()
        if n == "2":
            add(f"square root of {inner}")
        elif n == "3":
            add(f"cube root of {inner}")
        else:
            add(f"{n}th root of {inner}")

    # Greek letters
    for m in re.finditer(r"\\(var)?([A-Za-z]+)", cleaned):
        full = m.group(0)[1:]  # strip the backslash
        spoken = _GREEK.get(full.lower())
        if spoken:
            add(spoken)

    # Fractions: \frac{a}{b}
    for m in re.finditer(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", cleaned):
        a, b = m.group(1).strip(), m.group(2).strip()
        add(f"{a} over {b}")

    # Comparators
    if re.search(r"\\le\b|\\leq\b", cleaned):
        add("less than or equal")
    if re.search(r"\\ge\b|\\geq\b", cleaned):
        add("greater than or equal")
    if re.search(r"\\ne\b|\\neq\b", cleaned):
        add("not equal")

    # Equality is *very* common; only emit the token when narration would
    # plausibly say "equals" — i.e. the LaTeX has an "=" in a normal arithmetic
    # position.
    if "=" in cleaned and not re.search(r"\\(le|ge|ne)q?\b", cleaned):
        add("equals")

    return tokens


def _strip_latex_delimiters(s: str) -> str:
    s = s.strip()
    for opener, closer in (("\\[", "\\]"), ("\\(", "\\)"), ("$$", "$$"), ("$", "$")):
        if s.startswith(opener) and s.endswith(closer):
            return s[len(opener) : -len(closer)].strip()
    return s


def _strip_braces(s: str) -> str:
    return re.sub(r"[{}]", "", s)


# ─── Plain-text helpers ────────────────────────────────────────────────────

def text_to_anchor_tokens(text: str) -> list[str]:
    """Convert a step description (plain English with embedded LaTeX) into
    a list of search tokens. The strategy: take the first 1-3 words, plus
    any \\(...\\) inline math expanded via latex_to_speech_tokens.
    """
    if not text:
        return []

    tokens: list[str] = []
    seen: set[str] = set()

    def add(t: str) -> None:
        t = t.strip().lower()
        if not t or t in seen:
            return
        tokens.append(t)
        seen.add(t)

    # First few words of the cleaned (LaTeX-stripped) text.
    cleaned = re.sub(r"\\\(([^()]*)\\\)", r"\1", text)
    cleaned = re.sub(r"\\\[([^\[\]]*)\\\]", r"\1", cleaned)
    cleaned = re.sub(r"[{}\\]", " ", cleaned).strip()
    words = cleaned.split()
    if words:
        add(" ".join(words[:3]))
        add(words[0])

    # Any inline math chunks expanded via the LaTeX extractor.
    for m in re.finditer(r"\\\(([^()]*)\\\)|\\\[([^\[\]]*)\\\]", text):
        inner = m.group(1) or m.group(2) or ""
        for tok in latex_to_speech_tokens(inner):
            add(tok)

    return tokens


def ordinal_phrases(index: int) -> list[str]:
    """Return tokens an author might use to refer to a 0-based index."""
    one_based = index + 1
    ordinals = {
        1: ["first", "first step", "step one"],
        2: ["second", "second step", "step two"],
        3: ["third", "third step", "step three"],
        4: ["fourth", "fourth step", "step four"],
        5: ["fifth", "fifth step", "step five"],
        6: ["sixth", "sixth step", "step six"],
    }
    return ordinals.get(one_based, [f"step {one_based}"])


# ─── Search helper ─────────────────────────────────────────────────────────

def find_earliest_match(narration: str, candidates: Iterable[str], min_offset: int = 0) -> tuple[int, str | None]:
    """Return (offset, matched_token) for the earliest case-insensitive
    match of any candidate at or after ``min_offset``. Returns
    (-1, None) if no candidate matches.
    """
    lower = narration.lower()
    best_offset = -1
    best_token: str | None = None
    for cand in candidates:
        c = cand.strip().lower()
        if not c:
            continue
        idx = lower.find(c, min_offset)
        if idx < 0:
            continue
        if best_offset < 0 or idx < best_offset:
            best_offset = idx
            best_token = cand
    return best_offset, best_token

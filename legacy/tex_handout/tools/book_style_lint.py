from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEX_ROOTS = ("chapters", "frontmatter")
TEX_FILES = ("main.tex",)


@dataclass
class Violation:
    path: Path
    line_number: int
    message: str
    line: str


def strip_comments(line: str) -> str:
    escaped = False
    pieces: list[str] = []
    for char in line:
        if char == "%" and not escaped:
            break
        pieces.append(char)
        escaped = (char == "\\") and not escaped
        if char != "\\":
            escaped = False
    return "".join(pieces)


# Per-line regex checks. Each tuple is (human-readable message, compiled pattern).
# A match on any line of a chapter file (after comment-stripping) is a violation.
LINE_CHECKS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "manual cross-reference prefix; use cleveref instead",
        re.compile(
            r"\\(?:Figure|Theorem|Section|Chapter|Lemma|Proposition|Corollary|Definition|Example|Exercise|Remark)~\\ref\{"
        ),
    ),
    (
        "manual page break command is disallowed here",
        re.compile(r"\\(?:newpage|pagebreak|clearpage)\b"),
    ),
    (
        "bold emphasis in prose is disallowed; use \\emph{} instead (CONTENT_SPEC.md \u00a78)",
        re.compile(r"\\textbf\{"),
    ),
    (
        "italic emphasis in prose is disallowed; use \\emph{} instead (CONTENT_SPEC.md \u00a78)",
        re.compile(r"\\textit\{"),
    ),
)


# Expansion-marker check.
# The Mode A drafting policy (see README.md \u00a7 Authoring workflow) requires
# every non-translation addition to the chapter to be prefixed by a comment of
# the form:
#
#     % expansion:<category> [pass: <pass-id>] [source: <brief source>] \u2014 <one-line description>
#
# with <category> drawn from the list below. The bracket hints are optional
# (Mode A drafting may omit both; Mode C enrichment must include
# [pass: enrichment]); when both are present, [pass: ...] precedes
# [source: ...]. This keeps post-hoc review tractable: the user can grep
# "^% expansion:" and see every addition that is not a direct translation of
# the manuscript. An unknown or misspelled category, an unknown bracket key,
# or out-of-order hints would silently hide an expansion (or its provenance)
# from that review; hence the checks below.
_EXPANSION_CATEGORIES = frozenset(
    {
        "history",
        "application",
        "formula",
        "summary",
        "figure",
        "example",
        "intuition",
        "strategy",
        "caution",
    }
)
_EXPANSION_MARKER_RE = re.compile(r"^\s*%\s*expansion:([A-Za-z_]+)\s*(.*)$")
_BRACKET_HINT_RE = re.compile(r"\[\s*([A-Za-z_][A-Za-z0-9_]*)\s*:([^\]]*)\]")
_RECOGNISED_HINT_KEYS = ("pass", "source")  # tuple order is the canonical order
# [pass: ...] takes a value drawn from this allow-list. Today the only legal
# value is "enrichment" (Mode C). Add new entries here when a new mode-pass
# is introduced; do not loosen the check to accept any string, since a typo
# like [pass: enrichmnt] would otherwise silently misclassify an expansion
# in post-hoc review.
_RECOGNISED_PASS_VALUES = ("enrichment",)


# Whole-file structural checks.
# These run on the combined (comment-stripped) text of a chapter file rather
# than line-by-line, because they reason about block structure (definition
# bodies, named-theorem proximity to \index{}, etc.).

_DEFINITION_BLOCK_RE = re.compile(
    r"\\begin\{definition\}(?P<body>.*?)\\end\{definition\}",
    re.DOTALL,
)
_DEFINITION_LABEL_RE = re.compile(r"\\label\{def:([^}]+)\}")
_INDEX_IN_BLOCK_RE = re.compile(r"\\index\{")
_NAMED_THEOREM_RE = re.compile(
    r"\\begin\{theorem\}\[(?P<name>[^\]]+)\]",
)


def _find_line_number(text: str, offset: int) -> int:
    """Return 1-indexed line number for a character offset in ``text``."""
    return text.count("\n", 0, offset) + 1


def check_definitions_have_index(path: Path, text: str) -> list[Violation]:
    """Every \\begin{definition} body MUST contain at least one \\index{...} entry,
    except when the block is a paired *precise* restatement (label ending in
    ``-precise``), since the term was already indexed at its informal first
    occurrence (CONTENT_SPEC.md \u00a711 rule: place index at first
    occurrence only).
    """
    violations: list[Violation] = []
    for match in _DEFINITION_BLOCK_RE.finditer(text):
        body = match.group("body")
        if _INDEX_IN_BLOCK_RE.search(body):
            continue
        # Exempt paired precise restatements.
        label_match = _DEFINITION_LABEL_RE.search(body)
        if label_match and label_match.group(1).endswith("-precise"):
            continue
        line_number = _find_line_number(text, match.start())
        snippet_line = text.splitlines()[line_number - 1].strip() if line_number - 1 < len(text.splitlines()) else ""
        violations.append(
            Violation(
                path=path,
                line_number=line_number,
                message=(
                    "definition body lacks \\index{...}; every defined term must be indexed "
                    "at its first occurrence (CONTENT_SPEC.md \u00a711)"
                ),
                line=snippet_line,
            )
        )
    return violations


def check_named_theorems_have_index(path: Path, text: str) -> list[Violation]:
    """Every \\begin{theorem}[Name] MUST have a matching \\index{...} entry nearby.

    ``Nearby`` is operationalised as: within 400 characters after the theorem
    start. The match is case-insensitive and ignores leading/trailing spaces;
    the index key may contain an ``@`` sort-key split.
    """
    violations: list[Violation] = []
    for match in _NAMED_THEOREM_RE.finditer(text):
        name = match.group("name").strip().lower()
        window = text[match.end() : match.end() + 400]
        # Extract all \index{...} entries in the window and pull out the sort key
        # (portion before ``@``, or the whole argument if no ``@``).
        keys = []
        for idx_match in re.finditer(r"\\index\{([^}]*)\}", window):
            arg = idx_match.group(1)
            key = arg.split("@", 1)[0].strip().lower()
            keys.append(key)
        if any(key == name for key in keys):
            continue
        line_number = _find_line_number(text, match.start())
        snippet_line = text.splitlines()[line_number - 1].strip() if line_number - 1 < len(text.splitlines()) else ""
        violations.append(
            Violation(
                path=path,
                line_number=line_number,
                message=(
                    f"named theorem ``{match.group('name')}'' has no matching \\index{{{name}}} "
                    f"within 400 characters (CONTENT_SPEC.md \u00a76)"
                ),
                line=snippet_line,
            )
        )
    return violations


_CHAPTER_OPEN_RE = re.compile(r"\\chapter\{[^}]*\}", re.DOTALL)
_LEARNING_OUTCOMES_RE = re.compile(
    r"\\paragraph\{By the end of this chapter[^}]*\}\s*\\begin\{itemize\}",
    re.DOTALL,
)


def check_chapter_opening_structure(path: Path, text: str) -> list[Violation]:
    """Every chapter file MUST open with \\chapter{...} followed (eventually) by
    a ``\\paragraph{By the end of this chapter, ...}`` learning-outcomes bullet
    list, and at least one paragraph of overview prose between the two
    (CONTENT_SPEC.md \u00a74).

    The check is structural rather than editorial: we do not police the
    wording of the overview, only that (1) the chapter begins with
    ``\\chapter{...}``, (2) a learning-outcomes bullet list of the prescribed
    shape exists before the first ``\\section{...}``, and (3) at least one
    non-empty line of prose sits between the chapter header and the bullet
    list.
    """
    violations: list[Violation] = []
    chapter_match = _CHAPTER_OPEN_RE.search(text)
    if not chapter_match:
        # Not every file under chapters/ is a chapter (e.g. _scratch is a
        # scratch pad); require \chapter only when there is any \section.
        if re.search(r"\\section\{", text):
            violations.append(
                Violation(
                    path=path,
                    line_number=1,
                    message="chapter file has sections but no \\chapter{...} (CONTENT_SPEC.md \u00a74)",
                    line="",
                )
            )
        return violations

    # Look only at the region between \chapter{...} and the first \section{...};
    # the bullet list must appear there.
    region_start = chapter_match.end()
    first_section = re.search(r"\\section\{", text[region_start:])
    region_end = region_start + (first_section.start() if first_section else len(text) - region_start)
    region = text[region_start:region_end]

    if not _LEARNING_OUTCOMES_RE.search(region):
        line_number = _find_line_number(text, chapter_match.start())
        snippet_line = text.splitlines()[line_number - 1].strip() if line_number - 1 < len(text.splitlines()) else ""
        violations.append(
            Violation(
                path=path,
                line_number=line_number,
                message=(
                    "chapter opening lacks ``\\paragraph{By the end of this chapter, ...}'' "
                    "learning-outcomes bullet list before the first \\section "
                    "(CONTENT_SPEC.md \u00a74)"
                ),
                line=snippet_line,
            )
        )
        return violations

    # Also require at least one non-empty prose line between \chapter and the
    # bullet list, so the overview paragraph is not skipped outright.
    learning_match = _LEARNING_OUTCOMES_RE.search(region)
    overview = region[: learning_match.start()].strip()
    overview_lines = [line for line in overview.splitlines() if line.strip()]
    if not overview_lines:
        line_number = _find_line_number(text, chapter_match.start())
        snippet_line = text.splitlines()[line_number - 1].strip() if line_number - 1 < len(text.splitlines()) else ""
        violations.append(
            Violation(
                path=path,
                line_number=line_number,
                message=(
                    "chapter opening lacks overview prose before the learning-outcomes "
                    "bullet list (CONTENT_SPEC.md \u00a74)"
                ),
                line=snippet_line,
            )
        )

    return violations


BLOCK_CHECKS = (
    check_definitions_have_index,
    check_named_theorems_have_index,
    check_chapter_opening_structure,
)


def iter_tex_files() -> list[Path]:
    files: list[Path] = [ROOT / name for name in TEX_FILES if (ROOT / name).exists()]
    for folder in TEX_ROOTS:
        base = ROOT / folder
        if base.exists():
            files.extend(sorted(base.rglob("*.tex")))
    return files


def is_chapter_file(path: Path) -> bool:
    """Block-level checks only apply to real chapter sources, not main.tex or
    the scratch/template files.
    """
    if path.name.startswith("_"):
        return False
    return path.parent.name == "chapters"


def _strip_all_comments(text: str) -> str:
    return "\n".join(strip_comments(line) for line in text.splitlines())


def lint_file(path: Path) -> list[Violation]:
    violations: list[Violation] = []
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    for line_number, raw_line in enumerate(raw_lines, start=1):
        # Expansion marker check runs on the raw line because the marker *is* a
        # LaTeX comment; comment-stripping would erase it.
        expansion_match = _EXPANSION_MARKER_RE.match(raw_line)
        if expansion_match:
            category = expansion_match.group(1)
            rest = expansion_match.group(2)
            if category not in _EXPANSION_CATEGORIES:
                valid = ", ".join(sorted(_EXPANSION_CATEGORIES))
                violations.append(
                    Violation(
                        path=path,
                        line_number=line_number,
                        message=(
                            f"unknown expansion category '{category}'; "
                            f"valid categories are: {valid} "
                            f"(see README.md \u00a7 Authoring workflow)"
                        ),
                        line=raw_line.strip(),
                    )
                )
            # Em-dash separator is required: it both terminates the bracket-hint
            # region and introduces the description. Missing em-dash is itself
            # a violation; we still run the bracket-hint check on the whole
            # tail in that case so a malformed line surfaces every defect at
            # once (rather than the user fixing the em-dash and then learning
            # about the typo'd hint key on the next run).
            em_dash_idx = rest.find("\u2014")
            if em_dash_idx < 0:
                violations.append(
                    Violation(
                        path=path,
                        line_number=line_number,
                        message=(
                            "malformed expansion marker: missing em-dash ('\u2014') separator "
                            "before the description (see README.md \u00a7 Authoring workflow)"
                        ),
                        line=raw_line.strip(),
                    )
                )
                bracket_region = rest
            else:
                bracket_region = rest[:em_dash_idx]
            hint_pairs = [
                (m.group(1), m.group(2).strip())
                for m in _BRACKET_HINT_RE.finditer(bracket_region)
            ]
            hint_keys = [key for key, _ in hint_pairs]
            for key, value in hint_pairs:
                if key not in _RECOGNISED_HINT_KEYS:
                    valid_keys = ", ".join(_RECOGNISED_HINT_KEYS)
                    violations.append(
                        Violation(
                            path=path,
                            line_number=line_number,
                            message=(
                                f"unknown bracket hint key '{key}' in expansion marker; "
                                f"recognised keys are: {valid_keys} "
                                f"(see README.md \u00a7 Authoring workflow)"
                            ),
                            line=raw_line.strip(),
                        )
                    )
                    continue
                if key == "pass" and value not in _RECOGNISED_PASS_VALUES:
                    valid_values = ", ".join(_RECOGNISED_PASS_VALUES)
                    violations.append(
                        Violation(
                            path=path,
                            line_number=line_number,
                            message=(
                                f"unknown [pass: ...] value '{value}'; "
                                f"recognised values are: {valid_values} "
                                f"(see README.md \u00a7 Authoring workflow)"
                            ),
                            line=raw_line.strip(),
                        )
                    )
            if "pass" in hint_keys and "source" in hint_keys:
                if hint_keys.index("pass") > hint_keys.index("source"):
                    violations.append(
                        Violation(
                            path=path,
                            line_number=line_number,
                            message=(
                                "expansion marker bracket hints out of canonical order; "
                                "[pass: ...] must precede [source: ...] "
                                "(see README.md \u00a7 Authoring workflow)"
                            ),
                            line=raw_line.strip(),
                        )
                    )
        line = strip_comments(raw_line)
        if not line:
            continue
        if '"' in line:
            violations.append(
                Violation(
                    path=path,
                    line_number=line_number,
                    message="straight ASCII quotes are disallowed in TeX source",
                    line=raw_line.strip(),
                )
            )
        for message, pattern in LINE_CHECKS:
            if pattern.search(line):
                violations.append(
                    Violation(
                        path=path,
                        line_number=line_number,
                        message=message,
                        line=raw_line.strip(),
                    )
                )

    # Block-level checks run on the comment-stripped text of real chapter files.
    if is_chapter_file(path):
        stripped_text = _strip_all_comments(path.read_text(encoding="utf-8"))
        for check in BLOCK_CHECKS:
            violations.extend(check(path, stripped_text))

    return violations


def main() -> int:
    violations: list[Violation] = []
    for path in iter_tex_files():
        violations.extend(lint_file(path))

    if not violations:
        print("book_style_lint: ok")
        return 0

    for violation in violations:
        rel_path = violation.path.relative_to(ROOT)
        print(f"{rel_path}:{violation.line_number}: {violation.message}")
        print(f"  {violation.line}")
    print(f"book_style_lint: {len(violations)} violation(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())

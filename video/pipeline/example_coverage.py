"""example_coverage.py -- the EX deterministic layer (例題折疊宣告閘).

EX1 (silent drop): the handout declares a worked example in this section and no unit
either teaches it (`examples:`) or folds it (`folds:`).
EX2 (declaration does not hold): a declared key is not a handout example of this
section, a fold carries no reason, or one key is both taught and folded.

Pure stdlib. warn-default; EX1 flips to 'error' under meta.example_coverage_enforce.

**THIS GATE ONLY CHECKS THAT A DECLARATION EXISTS.** It does NOT judge whether a fold
is legitimate (i.e. whether the folded example really is the same teaching pattern),
and it does NOT judge whether a taught example is taught well. A `covered` verdict here
is book-keeping, not pedagogy: ch03 ex:3.1 has a scene and would pass, while four
review lenses independently judged it an orphan (never re-used in the closing scenes
or the recap). Those judgements belong to gate-1 (PEDAGOGY-FIRSTLEARNER, EX-adv) and
to the REWATCH lecturer lens. Do not read a clean EX report as "the examples are fine".

Model (mirrors step_coverage.py: contract in the `.md`, deterministic layer is a pure
comparison, storyboard is NOT read):

  handout `.tex`  --\\sechead{n.m} intervals--> the section's `ex:` label keys
  content `.md`   --`examples:` / `folds:` on the representative unit--> declarations
  finding         = a handout key with no declaration, or a declaration that fails

The gate does not read the storyboard on purpose: scene order and scene splitting are
the video's business (CONTENT_METHODOLOGY.md §1 分工), so re-ordering a deck must never
move an example in or out of coverage.

`ex:` NUMBERING IS CHAPTER-SERIAL, NOT SECTION-SERIAL -- ch03 §3.1 holds ex:3.1-3.3,
§3.2 holds ex:3.4-3.8, §3.3 holds ex:3.9-3.16, and ch01 runs ex:1.1-1.43 straight
across six sections. Matching on a section-number prefix would mis-assign nearly every
example in the book, so membership is decided ONLY by the \\sechead interval a key
falls in, and comparison is by set (keys are historical and need not be contiguous --
calcbook.sty documents that the label key does not promise to equal the printed value).
"""
from __future__ import annotations

import re
from pathlib import Path

# Same shapes provenance.py matches, narrowed to worked examples. Kept local (a
# 2-line regex) rather than imported so this module stays pure stdlib and provenance
# keeps its single responsibility.
_TEX_SECHEAD = re.compile(r"\\sechead\{(\d+\.\d+)\}")
_TEX_EXAMPLE = re.compile(r"\\begin\{envexample\}\{[^}]*\}\{(ex:[^}\s]+)\}")
# "<ex:key> <reason>", separator optional. A BARE key parses as a fold with an empty
# reason (-> EX2 "no reason") rather than as a malformed line: declaring the fold and
# forgetting the why is the common slip, and naming it precisely beats "unparseable".
_FOLD_LINE = re.compile(r"^\s*(ex:[^\s]+)\s*(?:[-\u2013\u2014:]\s*)?(.*)$")


def tex_examples_by_section(text: str) -> "dict[str, list[str]]":
    """Map "n.m" -> the worked-example label keys declared in that \\sechead interval.

    Keys before the first \\sechead (a chapter opener) belong to no section and are
    dropped. Order within a section is source order.
    """
    marks = [(m.start(), m.group(1), None) for m in _TEX_SECHEAD.finditer(text)]
    marks += [(m.start(), None, m.group(1)) for m in _TEX_EXAMPLE.finditer(text)]
    marks.sort(key=lambda t: t[0])

    by_section: dict[str, list[str]] = {}
    current: str | None = None
    for _pos, sec, key in marks:
        if sec is not None:
            current = sec
            by_section.setdefault(sec, [])
        elif current is not None:
            by_section[current].append(key)
    return by_section


def examples_for_deck(meta: dict, repo_root: Path) -> "list[str]":
    """The handout's worked-example keys for this deck's section, or [] when the
    chapter/section cannot be resolved or the source is missing (never raises --
    a deck with no handout source simply has nothing to check)."""
    m = re.search(r"(\d+)", str(meta.get("chapter", "")))
    section = str(meta.get("section", "")).strip()
    if not m or not section:
        return []
    src_dir = repo_root / "handout" / "latex" / "src" / f"ch{int(m.group(1)):02d}"
    for tex in sorted(src_dir.glob("*.tex")):
        by_section = tex_examples_by_section(
            tex.read_text(encoding="utf-8", errors="replace"))
        if section in by_section:
            return by_section[section]
    return []


def _split_keys(value) -> "list[str]":
    """`examples:` accepts "ex:3.2" or "ex:3.2, ex:3.3".

    Always a string: review_pack's `_commit` only preserves lines for `screen_contract`
    and `folds`; every other field is joined. (`folds` is the one that needs both shapes
    -- see `declarations`.)"""
    return [p.strip() for p in re.split(r"[,\s]+", str(value or "")) if p.strip()]


def declarations(units: "list[dict]") -> "tuple[dict, dict, list]":
    """Read `examples:` / `folds:` off the units.

    Returns (taught, folded, malformed):
      taught   {key: unit_id}
      folded   {key: (unit_id, reason)}
      malformed [(unit_id, raw_line)]  -- a `folds:` line that is not "<ex:key> <reason>"
    """
    taught: dict[str, str] = {}
    folded: dict[str, tuple[str, str]] = {}
    malformed: list[tuple[str, str]] = []

    for unit in units:
        uid = str(unit.get("id", "?"))
        for key in _split_keys(unit.get("examples")):
            taught.setdefault(key, uid)

        raw = unit.get("folds")
        lines = raw if isinstance(raw, (list, tuple)) else str(raw or "").splitlines()
        for line in lines:
            line = str(line).strip()
            if not line:
                continue
            m = _FOLD_LINE.match(line)
            if not m:
                malformed.append((uid, line))
                continue
            folded.setdefault(m.group(1), (uid, m.group(2).strip()))
    return taught, folded, malformed


def example_issues(section: str, handout_keys: "list[str]", units: "list[dict]",
                   enforce: bool) -> "list[tuple[str, str]]":
    """Findings as (severity, message). EX1 honours *enforce*; EX2 is always a warning
    (mirrors step_coverage's orphan-`covers` treatment: a bad declaration is an
    authoring slip to fix, not a reason to block a render)."""
    taught, folded, malformed = declarations(units)
    known = set(handout_keys)
    issues: list[tuple[str, str]] = []
    ex1_sev = "error" if enforce else "warn"

    for key in handout_keys:                                     # EX1, source order
        if key not in taught and key not in folded:
            issues.append((ex1_sev,
                           f"[EX1] {key}: handout worked example in \u00a7{section} is neither "
                           f"taught (examples:) nor folded (folds:) by any unit"))

    for key in sorted(set(taught) | set(folded)):                # EX2
        if key not in known:
            where = taught.get(key) or folded.get(key, ("?",))[0]
            issues.append(("warn",
                           f"[EX2] {key}: declared by unit '{where}' but is not a worked "
                           f"example of \u00a7{section} (ex: keys are chapter-serial -- check "
                           f"the handout)"))
        if key in taught and key in folded:
            issues.append(("warn",
                           f"[EX2] {key}: declared BOTH taught (unit '{taught[key]}') and "
                           f"folded (unit '{folded[key][0]}') -- pick one"))

    for key, (uid, reason) in sorted(folded.items()):
        if not reason:
            issues.append(("warn",
                           f"[EX2] {key}: folded by unit '{uid}' with no reason -- "
                           f"'MUST NOT silently drop' needs the why, in one line"))

    for uid, line in malformed:
        issues.append(("warn",
                       f"[EX2] unit '{uid}': folds: line is not '<ex:key> <reason>': {line!r}"))
    return issues

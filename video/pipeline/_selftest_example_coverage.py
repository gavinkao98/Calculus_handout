"""Stdlib assert self-test for example_coverage.py (the EX layer / 例題折疊宣告閘).

Run: .venv/Scripts/python.exe video/pipeline/_selftest_example_coverage.py

Hermetic: the handout is an in-memory `.tex` string, the content script a tempfile.
Nothing reads the real repo, so this stays green when chapters are re-numbered.
"""
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import example_coverage as EC   # noqa: E402
from pipeline import review_pack as RP        # noqa: E402


# A chapter shaped like the real ones: examples are numbered CHAPTER-serially, so
# §3.1 owns ex:3.1-3.3 and ex:3.2 is NOT in §3.2. This is the trap the gate exists to
# avoid; every assertion below leans on it.
TEX = r"""
\cbchapter{3}
\chapteropener{Chapter 3}{Chain Rule and Trigonometric Derivatives}
\begin{lead}Opening prose, no examples yet.\end{lead}
\sechead{3.1}{Derivatives of the Sine and Cosine Functions}
\begin{workedexample}
\begin{envexample}{Example}{ex:3.1}{}The companion limit.\end{envexample}
\begin{envsolution}{Solution}{}{}Multiply by the conjugate.\end{envsolution}
\end{workedexample}
\begin{workedexample}
\begin{envexample}{Example}{ex:3.2}{}All six derivatives.\end{envexample}
\end{workedexample}
\begin{workedexample}
\begin{envexample}{Example}{ex:3.3}{}Simple harmonic motion.\end{envexample}
\end{workedexample}
\sechead{3.2}{The Chain Rule}
\begin{workedexample}
\begin{envexample}{Example}{ex:3.4}{}A single composition.\end{envexample}
\end{workedexample}
"""


def _units(*specs):
    """[(id, examples, folds), ...] -> parser-shaped unit dicts."""
    return [{"id": i, "examples": e, "folds": f} for i, e, f in specs]


# -- the chapter-serial trap ---------------------------------------------------

def test_examples_are_grouped_by_sechead_interval_not_by_number():
    by_sec = EC.tex_examples_by_section(TEX)
    assert by_sec["3.1"] == ["ex:3.1", "ex:3.2", "ex:3.3"], by_sec["3.1"]
    assert by_sec["3.2"] == ["ex:3.4"], by_sec["3.2"]
    # the whole point: a section-number prefix match would put ex:3.2 in 3.2
    assert "ex:3.2" not in by_sec["3.2"]
    assert "ex:3.4" not in by_sec["3.1"]


def test_keys_before_the_first_sechead_are_dropped():
    tex = "\\begin{envexample}{Example}{ex:9.9}{}orphan\\end{envexample}\n" + TEX
    by_sec = EC.tex_examples_by_section(tex)
    assert all("ex:9.9" not in keys for keys in by_sec.values())


# -- EX1 -----------------------------------------------------------------------

def test_one_undeclared_example_is_exactly_one_ex1():
    keys = EC.tex_examples_by_section(TEX)["3.1"]
    units = _units(("u_a", "ex:3.1", ""), ("u_b", "ex:3.3", ""))
    issues = EC.example_issues("3.1", keys, units, enforce=False)
    ex1 = [m for s, m in issues if "[EX1]" in m]
    assert len(ex1) == 1, issues
    assert "ex:3.2" in ex1[0], ex1[0]


def test_fully_declared_section_is_silent():
    keys = EC.tex_examples_by_section(TEX)["3.1"]
    units = _units(("u_a", "ex:3.1", ""), ("u_b", "ex:3.2, ex:3.3", ""))
    assert EC.example_issues("3.1", keys, units, enforce=False) == []


def test_a_fold_counts_as_declared():
    keys = EC.tex_examples_by_section(TEX)["3.1"]
    units = _units(("u_a", "ex:3.1", ""),
                   ("u_b", "ex:3.2", ["ex:3.3 — same quotient-rule move, left to the book"]))
    assert EC.example_issues("3.1", keys, units, enforce=False) == []


def test_enforce_flips_ex1_to_error_and_leaves_ex2_a_warning():
    keys = EC.tex_examples_by_section(TEX)["3.1"]
    units = _units(("u_a", "ex:3.1 ex:9.1", ""))       # 3.2/3.3 missing + a bad key
    issues = EC.example_issues("3.1", keys, units, enforce=True)
    ex1 = [s for s, m in issues if "[EX1]" in m]
    ex2 = [s for s, m in issues if "[EX2]" in m]
    assert ex1 and set(ex1) == {"error"}, issues
    assert ex2 and set(ex2) == {"warn"}, issues


# -- EX2 -----------------------------------------------------------------------

def test_declared_key_not_in_this_section_is_ex2():
    keys = EC.tex_examples_by_section(TEX)["3.1"]
    units = _units(("u_a", "ex:3.1 ex:3.2 ex:3.3", ""), ("u_b", "ex:3.4", ""))
    msgs = [m for s, m in EC.example_issues("3.1", keys, units, enforce=False)]
    assert any("[EX2]" in m and "ex:3.4" in m for m in msgs), msgs


def test_fold_without_a_reason_is_ex2():
    keys = EC.tex_examples_by_section(TEX)["3.1"]
    units = _units(("u_a", "ex:3.1 ex:3.2", ["ex:3.3"]))
    msgs = [m for s, m in EC.example_issues("3.1", keys, units, enforce=False)]
    assert any("[EX2]" in m and "no reason" in m for m in msgs), msgs


def test_both_taught_and_folded_is_ex2():
    keys = EC.tex_examples_by_section(TEX)["3.1"]
    units = _units(("u_a", "ex:3.1 ex:3.2 ex:3.3", ""),
                   ("u_b", "", ["ex:3.3 — also folded here"]))
    msgs = [m for s, m in EC.example_issues("3.1", keys, units, enforce=False)]
    assert any("[EX2]" in m and "BOTH" in m for m in msgs), msgs


def test_a_reason_containing_an_ex_token_stays_one_entry():
    """The reason is free text; only the LEADING token is the key."""
    keys = EC.tex_examples_by_section(TEX)["3.1"]
    units = _units(("u_a", "ex:3.1 ex:3.2", ["ex:3.3 — same move as ex:3.2, left to the book"]))
    taught, folded, malformed = EC.declarations(units)
    assert set(folded) == {"ex:3.3"}, folded
    assert not malformed
    assert EC.example_issues("3.1", keys, units, enforce=False) == []


# -- the parser must actually keep the two new fields (review_pack._FIELD_KEYS) --

def test_parser_keeps_examples_and_preserves_fold_lines():
    md = (
        "source_rev: handout/latex/src/ch03/chapter3.tex@deadbeef\n"
        "\n"
        "### unit: u_a\n"
        "```\n"
        "id: u_a\n"
        "kind: example\n"
        "examples: ex:3.1, ex:3.2\n"
        "folds: |\n"
        "  ex:3.3 — same quotient-rule move, left to the book\n"
        "  ex:3.9 — second drill of the same pattern\n"
        "narration: Some prose.\n"
        "```\n"
    )
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "deck.md"
        path.write_text(md, encoding="utf-8")
        units = RP.parse_content_script(path)["units"]
    assert len(units) == 1, units
    unit = units[0]
    assert unit["examples"] == "ex:3.1, ex:3.2", unit["examples"]
    # a block scalar must survive as LINES -- the default " ".join would merge the two
    # folds into one string and the second key would be read as part of the first reason
    assert isinstance(unit["folds"], list) and len(unit["folds"]) == 2, unit["folds"]
    taught, folded, malformed = EC.declarations([unit])
    assert set(taught) == {"ex:3.1", "ex:3.2"}, taught
    assert set(folded) == {"ex:3.3", "ex:3.9"}, folded
    assert not malformed


def test_examples_for_deck_resolves_a_real_tree_and_is_not_silently_empty():
    """`examples_for_deck` is the one function here that fails SILENTLY: if meta.chapter
    or meta.section ever changes shape (`section: "§3.1"`, say) it returns [] and the
    gate waves everything through, indistinguishable from "all declared". The other
    failure mode (an unregistered _FIELD_KEYS entry) at least fires EX1 loudly. Pin the
    happy path against a real directory layout so a shape change breaks here."""
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        src = root / "handout" / "latex" / "src" / "ch03"
        src.mkdir(parents=True)
        (src / "chapter3.tex").write_text(TEX, encoding="utf-8")
        meta = {"chapter": "Chapter 3", "section": "3.1"}
        assert EC.examples_for_deck(meta, root) == ["ex:3.1", "ex:3.2", "ex:3.3"]
        assert EC.examples_for_deck({"chapter": "Chapter 3", "section": "3.2"}, root) == ["ex:3.4"]
        # a section the handout does not have, and a deck with no chapter -> empty, no raise
        assert EC.examples_for_deck({"chapter": "Chapter 3", "section": "9.9"}, root) == []
        assert EC.examples_for_deck({"chapter": "", "section": "3.1"}, root) == []
        # a missing tree must not raise either
        assert EC.examples_for_deck(meta, root / "nope") == []


def test_a_malformed_fold_line_is_reported_as_ex2():
    keys = EC.tex_examples_by_section(TEX)["3.1"]
    units = _units(("u_a", "ex:3.1 ex:3.2 ex:3.3", ["this line has no key at all"]))
    issues = EC.example_issues("3.1", keys, units, enforce=False)
    msgs = [m for _s, m in issues]
    assert any("[EX2]" in m and "no key at all" in m for m in msgs), msgs


def test_no_units_fires_ex1_per_example_so_the_caller_must_skip_deckless_decks():
    """Contract note, deliberately asserted: with zero units this module reports one EX1
    per handout example. That is correct for a deck whose .md simply forgot to declare,
    and WRONG for a deck that has no .md at all (ch01_inverse_functions, a gen-1 layout
    regression deck) -- there, "no declarations" means "nobody wrote a content script",
    not "8 examples were dropped". Skipping is the CALLER's job (schema.py checks
    deck_md.exists() first); do not move it in here and make a silent no-op of a real
    missing declaration."""
    keys = EC.tex_examples_by_section(TEX)["3.1"]
    issues = EC.example_issues("3.1", keys, [], enforce=False)
    assert len([m for _s, m in issues if "[EX1]" in m]) == len(keys) == 3, issues


def test_missing_fields_are_simply_no_declarations():
    taught, folded, malformed = EC.declarations([{"id": "u", "examples": "", "folds": ""}])
    assert taught == {} and folded == {} and malformed == []


if __name__ == "__main__":
    test_examples_are_grouped_by_sechead_interval_not_by_number()
    test_keys_before_the_first_sechead_are_dropped()
    test_one_undeclared_example_is_exactly_one_ex1()
    test_fully_declared_section_is_silent()
    test_a_fold_counts_as_declared()
    test_enforce_flips_ex1_to_error_and_leaves_ex2_a_warning()
    test_declared_key_not_in_this_section_is_ex2()
    test_fold_without_a_reason_is_ex2()
    test_both_taught_and_folded_is_ex2()
    test_a_reason_containing_an_ex_token_stays_one_entry()
    test_parser_keeps_examples_and_preserves_fold_lines()
    test_examples_for_deck_resolves_a_real_tree_and_is_not_silently_empty()
    test_a_malformed_fold_line_is_reported_as_ex2()
    test_no_units_fires_ex1_per_example_so_the_caller_must_skip_deckless_decks()
    test_missing_fields_are_simply_no_declarations()
    print("OK example_coverage self-test")

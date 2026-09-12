"""Stdlib assert self-test for source_rev.py. Run: python video/pipeline/_selftest_source_rev.py"""
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import source_rev as S  # noqa: E402
from pipeline.derived_check import text_sha256  # noqa: E402

SRC_REL = "handout/latex/src/ch03/chapter3.tex"
LEGACY_REL = "legacy/html_handout/fragments/ch03/sec-3-1.html"


def _repo(tmp: Path, header: str, src_rel: str = SRC_REL, src_text: "str | None" = "handout\n",
          md_name: str = "deck.md") -> "tuple[Path, Path]":
    """A throwaway repo: video/content_scripts/<md_name> with `header`, and (optionally) the
    stamped source file. The unit region below the header must not confuse the header cut."""
    md = tmp / "video" / "content_scripts" / md_name
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(header + "\n\n### unit: u1\n```\nid: u1\nsource: LOCKED-looking word inside a unit\n```\n",
                  encoding="utf-8")
    src = tmp / src_rel
    if src_text is not None:
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_bytes(src_text.encode("utf-8"))
    return md, src


def _stamp(rel: str, sha: str) -> str:
    return f"> **source_rev：** `{rel}` `sha256:{sha}` — lock-time hash"


def test_parse_stamp():
    sha = "a" * 64
    assert S.parse_stamp(_stamp(SRC_REL, sha)) == (SRC_REL, sha)
    assert S.parse_stamp(f"> source_rev: `{SRC_REL}` `sha256:{sha.upper()}`") == (SRC_REL, sha)  # ascii colon, no bold, case
    assert S.parse_stamp("> **權威來源：** whatever") is None
    assert S.parse_stamp(_stamp(SRC_REL, "a" * 63)) is None      # truncated hash = no stamp
    assert S.parse_stamp("") is None


def test_fresh_is_clean():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        md, src = _repo(tmp, "> **階段：** LOCKED\n" + _stamp(SRC_REL, text_sha256(tmp / SRC_REL) if False else "x" * 64))
        # re-stamp with the real hash now that the source exists
        md.write_text(md.read_text(encoding="utf-8").replace("x" * 64, text_sha256(src)), encoding="utf-8")
        assert S.check_source_rev(md, tmp) == []


def test_drift_warns():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        md, src = _repo(tmp, "LOCKED\n" + _stamp(SRC_REL, "0" * 64))
        src.write_text("the handout moved on\n", encoding="utf-8")
        out = S.check_source_rev(md, tmp)
        assert len(out) == 1 and out[0][0] == "warn"
        assert "changed since" in out[0][1] and "section 8" in out[0][1]
        assert out[0][1].isascii()                              # cp950-safe console output
        assert "legacy" not in out[0][1]                      # .tex stamp -> no legacy tail


def test_missing_source_warns():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        md, _ = _repo(tmp, "LOCKED\n" + _stamp(SRC_REL, "0" * 64), src_text=None)
        out = S.check_source_rev(md, tmp)
        assert len(out) == 1 and "not found" in out[0][1]


def test_locked_without_stamp_warns_draft_does_not():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        md, _ = _repo(tmp, "> **階段：** **LOCKED（2026-06-29 sign-off）**")
        out = S.check_source_rev(md, tmp)
        assert len(out) == 1 and "no source_rev stamp" in out[0][1]
        md2, _ = _repo(tmp, "> **階段：** DRAFT", md_name="draft.md")
        assert S.check_source_rev(md2, tmp) == []
        # the word LOCKED inside a UNIT (not the header) must not count
        md3, _ = _repo(tmp, "> **階段：** DRAFT", md_name="draft2.md")
        assert S.check_source_rev(md3, tmp) == []


def test_fixture_and_absent_md_exempt():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        md, _ = _repo(tmp, "LOCKED", md_name="_fixture_x.md")
        assert S.check_source_rev(md, tmp) == []               # `_` prefix = fixture/demo
        assert S.check_source_rev(tmp / "video" / "content_scripts" / "nope.md", tmp) == []


def test_legacy_stamp_warns_even_when_fresh():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        md, src = _repo(tmp, "LOCKED\n" + _stamp(LEGACY_REL, "0" * 64), src_rel=LEGACY_REL)
        md.write_text(md.read_text(encoding="utf-8").replace("0" * 64, text_sha256(src)), encoding="utf-8")
        out = S.check_source_rev(md, tmp)
        assert len(out) == 1 and "frozen legacy HTML" in out[0][1] and ".tex" in out[0][1]
        src.write_text("drifted\n", encoding="utf-8")         # legacy + drift -> ONE combined message
        out2 = S.check_source_rev(md, tmp)
        assert len(out2) == 1 and "changed since" in out2[0][1] and "legacy" in out2[0][1]


def test_stamp_line_roundtrip_and_crlf():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        md, src = _repo(tmp, "LOCKED", src_text="line one\nline two\n")
        line = S.stamp_line(src, tmp)
        assert S.parse_stamp(line) == (SRC_REL, text_sha256(src))
        md.write_text("LOCKED\n" + line, encoding="utf-8")
        assert S.check_source_rev(md, tmp) == []
        src.write_bytes(b"line one\r\nline two\r\n")           # CRLF checkout of the same text
        assert S.check_source_rev(md, tmp) == []                # LF-normalized hash -> still fresh


def test_md_for_deck_strips_mimo():
    root = Path("/repo")
    assert S.md_for_deck({"id": "ch03_trig_derivatives_mimo"}, root) == root / "video" / "content_scripts" / "ch03_trig_derivatives.md"
    assert S.md_for_deck({"id": "ch03_chain_rule"}, root).name == "ch03_chain_rule.md"
    assert S.md_for_deck({}, root).name == ".md"                # empty id -> non-existent path -> [] downstream
    assert S.md_for_deck(None, root).name == ".md"              # malformed meta never raises


if __name__ == "__main__":
    test_parse_stamp()
    test_fresh_is_clean()
    test_drift_warns()
    test_missing_source_warns()
    test_locked_without_stamp_warns_draft_does_not()
    test_fixture_and_absent_md_exempt()
    test_legacy_stamp_warns_even_when_fresh()
    test_stamp_line_roundtrip_and_crlf()
    test_md_for_deck_strips_mimo()
    print("OK source_rev self-test")

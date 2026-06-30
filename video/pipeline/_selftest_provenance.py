"""Stdlib assert self-test for provenance.py. Run: python video/pipeline/_selftest_provenance.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import provenance as P  # noqa: E402


def test_parse_ref():
    assert P.parse_ref("md:why_trig") == ("md", "why_trig")
    assert P.parse_ref("doc:frag-sec-3-1") == ("doc", "frag-sec-3-1")
    assert P.parse_ref("doc:sector-inequality") == ("doc", "sector-inequality")
    assert P.parse_ref("nope:x") is None
    assert P.parse_ref("plain string") is None
    assert P.parse_ref("") is None
    assert P.parse_ref("md:") is None          # empty token rejected


def test_constants():
    assert "statement" in P.TEACHING_TEXT_FIELDS
    assert "title" not in P.TEACHING_TEXT_FIELDS
    assert P.OTF_EXEMPT_KINDS == frozenset({"intro", "outro"})
    assert P.OTF_KINDS == frozenset({"content", "divider"})


def test_loci(tmp_md, tmp_handout):
    loci = P.Loci(md_unit_ids={"why_trig", "sector"},
                  handout_anchors={"frag-sec-3-1", "sector-inequality"})
    assert loci.resolves("md:why_trig") is True
    assert loci.resolves("md:absent") is False
    assert loci.resolves("doc:frag-sec-3-1") is True
    assert loci.resolves("doc:data-fig-absent") is False
    assert loci.resolves("garbage") is False
    empty = P.Loci(md_unit_ids=set(), handout_anchors=set())
    assert empty.resolves("md:anything") is False   # fail closed


def test_scene_text_refs():
    scene = {"kind": "content", "template": "theorem_proof",
             "ref": "md:scene_src",
             "statement": "$\\sin x$ continuous",
             "scaffold": {"motive": "why we need continuity"},
             "refs": {"scaffold.motive": "doc:frag-sec-3-1"}}
    got = dict(P.scene_text_refs(scene))
    assert got["statement"] == "md:scene_src"            # inherited scene ref
    assert got["scaffold.motive"] == "doc:frag-sec-3-1"  # field override
    # absent fields not reported; non-teaching 'title' never reported
    scene2 = {"kind": "content", "title": "X", "statement": "y"}
    got2 = dict(P.scene_text_refs(scene2))
    assert got2 == {"statement": ""}                      # missing ref -> ""
    assert "title" not in got2
    # list field expands per index
    scene3 = {"kind": "content", "ref": "md:s", "annotations": ["a", "b"]}
    paths = {p for p, _ in P.scene_text_refs(scene3)}
    assert paths == {"annotations.0", "annotations.1"}


if __name__ == "__main__":
    test_parse_ref()
    test_constants()
    test_loci(None, None)
    test_scene_text_refs()
    print("OK provenance self-test")

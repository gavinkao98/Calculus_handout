"""Stdlib assert self-test for check_storyboard.py -- the Remotion storyboard entry
(SPEC-remotion-storyboard-schema.md). Structure rules in-process; the CLI (gate wiring,
arming lines, exit codes) over storyboards/_fixtures/remotion_minimal.yml and the three
content-layer fixtures the archived schema.py used to be tested over.
Run: python video/pipeline/run_selftests.py -k check_storyboard
"""
import subprocess
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import check_storyboard as CS  # noqa: E402

VIDEO = Path(__file__).resolve().parent.parent
FIXTURES = VIDEO / "storyboards" / "_fixtures"


def _run(*paths: Path, extra: "list[str] | None" = None) -> "tuple[int, str]":
    r = subprocess.run([sys.executable, "-m", "pipeline.check_storyboard", *map(str, paths),
                        *(extra or [])],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=VIDEO)
    return r.returncode, r.stdout + r.stderr


def _msgs(issues, sev=None):
    return [m for s, m in issues if sev is None or s == sev]


def test_structure_meta_and_scenes():
    assert _msgs(CS.structure_issues("not a mapping"), "error")
    assert any("meta" in m for m in _msgs(CS.structure_issues({"scenes": []}), "error"))
    assert any("meta.id" in m for m in _msgs(CS.structure_issues({"meta": {}, "scenes": [{}]}), "error"))
    assert any("scenes" in m for m in _msgs(CS.structure_issues({"meta": {"id": "d"}}), "error"))
    # section is optional in the Remotion shape (Q7 has none) -- no finding
    clean = {"meta": {"id": "d"}, "scenes": [{"id": "s", "kind": "content", "say": "hi {show a} there"}]}
    assert CS.structure_issues(clean) == []
    # Manim meta fields are warned, not errored
    legacy_meta = {"meta": {"id": "d", "color_map": {"x": "concept"}, "video": {}}, "scenes": clean["scenes"]}
    warns = _msgs(CS.structure_issues(legacy_meta), "warn")
    assert any("meta.color_map" in m for m in warns) and any("meta.video" in m for m in warns)
    assert _msgs(CS.structure_issues(legacy_meta), "error") == []


def test_structure_scene_rules():
    def sb(*scenes):
        return {"meta": {"id": "d"}, "scenes": list(scenes)}
    # id required + unique; kind required and one of four
    errs = _msgs(CS.structure_issues(sb({"kind": "content", "say": "x"})), "error")
    assert any(".id" in m for m in errs)
    errs = _msgs(CS.structure_issues(sb({"id": "a", "kind": "content", "say": "x"},
                                        {"id": "a", "kind": "content", "say": "y"})), "error")
    assert any("duplicate" in m for m in errs)
    errs = _msgs(CS.structure_issues(sb({"id": "a", "say": "x"})), "error")
    assert any("kind" in m for m in errs)                       # absent kind is an error (tts defaults it silently)
    errs = _msgs(CS.structure_issues(sb({"id": "a", "kind": "montage"})), "error")
    assert any("montage" in m for m in errs)
    # content: say required; malformed {show}; duplicate reveal id within the scene
    errs = _msgs(CS.structure_issues(sb({"id": "a", "kind": "content"})), "error")
    assert any("say" in m for m in errs)
    errs = _msgs(CS.structure_issues(sb({"id": "a", "kind": "content", "say": "t {show} u {show b c}"})), "error")
    assert sum("malformed" in m for m in errs) == 2
    errs = _msgs(CS.structure_issues(sb({"id": "a", "kind": "content", "say": "{show x} p {show x} q"})), "error")
    assert any("duplicate" in m and "'x'" in m for m in errs)
    # silent scenes: duration required positive; say ignored -> warn
    for kind in ("intro", "outro", "divider"):
        errs = _msgs(CS.structure_issues(sb({"id": "a", "kind": kind})), "error")
        assert any("duration" in m for m in errs), kind
        errs = _msgs(CS.structure_issues(sb({"id": "a", "kind": kind, "duration": 0})), "error")
        assert any("duration" in m for m in errs), kind
        out = CS.structure_issues(sb({"id": "a", "kind": kind, "duration": 2.5, "say": "spoken?"}))
        assert _msgs(out, "error") == [] and any("ignored" in m for m in _msgs(out, "warn")), kind
    # pauses: content only; after must be a reveal of this scene; seconds positive
    ok = sb({"id": "a", "kind": "content", "say": "{show x} p", "pauses": [{"after": "x", "seconds": 1}]})
    assert CS.structure_issues(ok) == []
    errs = _msgs(CS.structure_issues(sb({"id": "a", "kind": "content", "say": "{show x} p",
                                         "pauses": [{"after": "y", "seconds": 1}, {"after": "x", "seconds": 0}]})), "error")
    assert any("'y'" in m for m in errs) and any("seconds" in m for m in errs)
    errs = _msgs(CS.structure_issues(sb({"id": "a", "kind": "intro", "duration": 1, "pauses": []})), "error")
    assert any("pauses" in m for m in errs)
    # Manim gen-2 scene fields -> one warn each, never an error
    out = CS.structure_issues(sb({"id": "a", "kind": "content", "say": "x", "template": "derivation",
                                  "carry": [], "focus": [], "scene_role": "proof"}))
    assert _msgs(out, "error") == []
    assert sum("Manim gen-2 field" in m for m in _msgs(out, "warn")) == 4


def test_cli_over_remotion_fixture():
    rc, out = _run(FIXTURES / "remotion_minimal.yml")
    assert rc == 1, out                                     # structure errors -> exit 1
    # [structure]: the planted errors and warns
    assert "dup_show" in out and "duplicate" in out
    assert out.count("malformed {show} marker") == 2, out   # `{show}` + `{show b c}` in bad_marker
    assert "bad_pause.pauses[0].after 'nope'" in out
    assert "no_duration.duration" in out and "no_duration: outro scene has 'say'" in out
    assert "legacy_fields.focus" in out and "legacy_fields.carry" in out and "meta.color_map" in out
    # [provenance]: scene-level check on the Remotion shape; ok_ref resolves via _fixture_otf.md
    assert "no_ref: scene has no `ref:`" in out
    assert "bad_ref: scene `ref:` 'md:does_not_exist' does not resolve" in out
    assert "div: scene has no `ref:`" in out                # divider is OTF-scoped too
    assert "ok_ref:" not in out.split("[provenance]", 1)[1].split("\n[", 1)[0]
    assert "md: 1 unit(s)" in out and "no meta.chapter" in out      # arming line says what resolves
    # [pedagogy]: PD3 fires on the bare divider; PD2 is reported as not armed (no template)
    assert "div: divider should carry scaffold.problem" in out
    assert "PD2 not armed" in out
    # [source_rev] / [coverage] / [example_coverage]: say why they did nothing
    assert "[source_rev]" in out and "fixture" in out.split("[source_rev]", 1)[1].splitlines()[0]
    assert "[coverage]" in out and "0 contract(s)" in out
    assert "[example_coverage]" in out and "cannot resolve handout section" in out
    assert "[check_storyboard] remotion_minimal.yml:" in out


def test_cli_clean_deck_and_exit_codes():
    with tempfile.TemporaryDirectory() as d:
        deck = Path(d) / "clean.yml"
        deck.write_text("meta: {id: _fixture_clean, voice: Dean}\n"
                        "scenes:\n"
                        "  - {id: logo, kind: intro, duration: 4}\n"
                        "  - id: one\n    kind: content\n    say: 'Hello. {show a} World.'\n"
                        "  - {id: outro, kind: outro, duration: 6}\n", encoding="utf-8")
        rc, out = _run(deck)
        assert rc == 0, out                                  # only warns (no ref, nothing to resolve against)
        assert "[structure] clean.yml: structure OK" in out
        assert "not armed" in out                            # no .md, no chapter -> provenance says so
        assert "one: scene has no `ref:`" in out
        assert "0 error(s)" in out
        # --list enumerates the reveal ids the composition keys on
        rc, out = _run(deck, extra=["--list"])
        assert rc == 0 and "one: a" in out
        # unreadable input is exit 2, not 1
        rc, out = _run(Path(d) / "missing.yml")
        assert rc == 2 and "missing.yml" in out
        bad = Path(d) / "bad.yml"
        bad.write_text("meta: [unclosed\n", encoding="utf-8")
        rc, out = _run(bad)
        assert rc == 2
        # multiple decks: exit is the max
        rc, out = _run(deck, FIXTURES / "remotion_minimal.yml")
        assert rc == 1 and "[check_storyboard] clean.yml" in out and "[check_storyboard] remotion_minimal.yml" in out


def test_cli_wires_the_content_layer_over_the_legacy_fixtures():
    """The three fixtures the archived schema.py integration tests ran over: the per-field
    provenance, SC and PD checkers must still be reachable through the new entry. They are
    Manim-shaped (template:, silent scenes with no duration), so the exit code is not
    asserted where the SPEC now makes a structure error of that -- only the wiring is."""
    _, out = _run(FIXTURES / "otf_provenance.yml")
    for s in ("bad_missing.statement", "bad_unresolvable.statement", "bad_divider.problem",
              "bad_nested_reason.steps.0.reason"):
        assert s in out, s
    assert "ok_inherited.statement" not in out and "intro.statement" not in out
    rc, out = _run(FIXTURES / "sc_coverage.yml")
    assert rc == 0 and "[SC2]" in out and "reduced" in out, out     # warn-default never aborts
    _, out = _run(FIXTURES / "scaffold.yml")
    assert "thm_no_motive" in out and "scaffold.motive" in out          # PD2 (template-gated, armed here)
    assert "PD2 armed" in out
    assert "div_no_problem" in out and "scaffold.problem" in out        # PD3


if __name__ == "__main__":
    test_structure_meta_and_scenes()
    test_structure_scene_rules()
    test_cli_over_remotion_fixture()
    test_cli_clean_deck_and_exit_codes()
    test_cli_wires_the_content_layer_over_the_legacy_fixtures()
    print("OK check_storyboard self-test")

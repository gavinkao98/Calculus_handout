"""Self-test: ONE `{show}` grammar for every gate (code-review-2026-09-23 B-04).
Run from video/:
    python -m pipeline._selftest_show_grammar

The player splits beats with `narration.parse_say`. schema.py, sizecheck's target check and
derive_spoken's parity check each had their own regex, and they disagreed with the runtime on
two spellings:
  * a bare `{show}`: schema only warned "reveals nothing" and sizecheck skipped it as "a pure
    beat split" -- but parse_say does not read it at all: it cuts no beat and stays in the beat
    TEXT, so TTS speaks the word "show";
  * `{ show x}` (space after the brace): parse_say reveals x there, while schema and sizecheck
    never saw the marker, so a typo'd target went unchecked.
Now the grammar lives in narration.py only; everything else asks it.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # sizecheck builds real blocks -- bootstrap FIRST

from pipeline import derive_spoken, narration, schema, sizecheck

_META = {"id": "_t", "section": "0.0", "title": "probe"}


def _deck(*scenes):
    return {"meta": dict(_META), "scenes": list(scenes)}


def _callout(say, **extra):
    return {"id": "c", "kind": "content", "template": "callout", "type": "note",
            "title": "Probe", "say": say, "body": "Body text.", **extra}


def _errors(data):
    return [m for s, m in schema.schema_storyboard(data) if s == "error"]


def test_a_bare_show_is_a_schema_error_not_a_warning():
    say = "Hello {show} world {show body} end."
    assert [b.reveal for b in narration.parse_say(say)] == [None, "body"]
    assert "{show}" in narration.parse_say(say)[0].text, "the runtime leaves it in the spoken text"
    issues = schema.schema_storyboard(_deck(_callout(say)))
    errs = [m for s, m in issues if s == "error"]
    assert any("{show}" in m and "parse_say" in m for m in errs), issues
    assert not any("reveals nothing" in m for _s, m in issues), issues


def test_malformed_markers_are_errors():
    for say in ("One {show body two.", "One {show body extra} two."):
        errs = _errors(_deck(_callout(say)))
        assert any("{show" in m for m in errs), (say, errs)


def test_schema_reads_a_spaced_marker_exactly_as_the_runtime_does():
    say = "Hello { show body} world. {show step[2]} more."
    runtime = [b.reveal for b in narration.parse_say(say) if b.reveal]
    assert runtime == ["body", "step.2"], runtime
    assert schema.reveal_targets(say) == runtime
    # a field keyed to that reveal is accepted, as the runtime would honour it
    scene = _callout(say, pauses=[{"after": "body", "seconds": 1.0}])
    assert _errors(_deck(scene)) == [], _errors(_deck(scene))


def test_well_formed_markers_are_silent():
    assert _errors(_deck(_callout("One. {show body} Two."))) == []


def test_sizecheck_checks_the_target_of_a_spaced_marker():
    errs = [m for s, m in sizecheck.check_scenes(_META, [_callout("One. { show bodyy} Two.")])
            if s == "error"]
    assert any("{show bodyy}" in m for m in errs), errs


def test_derive_spoken_parity_uses_the_runtime_grammar():
    canon = {"scenes": [{"id": "c", "kind": "content", "say": "One. { show body} Two."}]}
    # same beat split, different spelling: the runtime reads both as `body` -> parity holds
    assert derive_spoken.check(canon, {"c": "One. {show body} Two."}) == []
    # the spaced marker on the canonical side only: the two tracks cut different beats
    problems = derive_spoken.check(canon, {"c": "One. Two."})
    assert problems and "markers differ" in problems[0], problems


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] show_grammar green")

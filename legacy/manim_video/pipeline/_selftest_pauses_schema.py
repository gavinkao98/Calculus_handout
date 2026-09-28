"""Self-test: schema's gate on the `pauses:` scene field. Run from video/ (pre-archive layout):
    python -m pipeline._selftest_pauses_schema

Split out of video/pipeline/_selftest_pauses.py on 2026-09-28 (section (c)), when schema.py
moved here with the Manim engine and pauses.py stayed in video/ (see
video/KICKOFF-remotion-unification.md). Pins: a `pauses[].after` naming no {show} reveal in
`say` is an ERROR (a typo'd pause would otherwise silently do nothing), and malformed or
misplaced `pauses` entries are errors too. Test code unchanged -- checkout tag
archive/2026-09-28-manim-gen2-final to run it.
"""
from pipeline import schema


def _scene(pauses_field=None):
    s = {
        "id": "s1", "kind": "content", "template": "derivation",
        "say": "One. {show step.0} Two. {show step.1} Three.",
    }
    if pauses_field is not None:
        s["pauses"] = pauses_field
    return s


# -- (c) schema gate ---------------------------------------------------------

def _errors(scene):
    data = {"meta": {"id": "d", "section": "1.1"}, "scenes": [scene]}
    return [m for s, m in schema.schema_storyboard(data) if s == "error"]


def test_schema_accepts_a_well_formed_pause():
    assert not _errors(_scene([{"after": "step.1", "seconds": 1.2}]))


def test_schema_rejects_pause_after_unrevealed_id():
    errs = _errors(_scene([{"after": "step.9", "seconds": 1.2}]))
    assert any("pauses" in e and "step.9" in e for e in errs), errs


def test_schema_rejects_malformed_pause_entries():
    assert any("pauses" in e for e in _errors(_scene([{"seconds": 1.0}])))          # no `after`
    assert any("pauses" in e for e in _errors(_scene([{"after": "step.0"}])))       # no `seconds`
    assert any("pauses" in e for e in _errors(_scene([{"after": "step.0", "seconds": 0}])))
    assert any("pauses" in e for e in _errors(_scene({"after": "step.0"})))         # not a list


def test_schema_pause_on_non_content_scene_is_an_error():
    errs = _errors({"id": "d1", "kind": "divider", "pauses": [{"after": "x", "seconds": 1}]})
    assert any("pauses" in e for e in errs), errs


if __name__ == "__main__":
    import sys, traceback
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS {name}")
            except Exception:
                fails += 1; print(f"FAIL {name}"); traceback.print_exc()
    sys.exit(1 if fails else 0)

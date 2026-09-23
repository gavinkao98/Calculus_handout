"""Self-test: `focus` may not dim / indicate a block a LATER beat reveals
(code-review-2026-09-23 C-08). Run from video/:
    python -m pipeline._selftest_focus_reveal_order

`focus.apply` (`.animate.fade`) and `focus.indicate` (`Indicate`) are not introducer
animations, and manim adds any mobject a non-introducer animation touches that is not on
screen yet. So dimming a block whose own `{show}` comes later puts it on screen early at
35 % opacity (a spoiler), and it then fades in a second time -- still dimmed -- on its own
beat; an early `indicate` leaves it on screen at full strength. The gates only excluded a
beat's OWN reveal (schema) and checked ids exist (sizecheck). Pure dict logic; no manim.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import schema as S   # noqa: E402

_SAY = "{show step.0} First. {show step.1} Second. {show result} So."


def _deck(focus):
    scene = {"id": "der", "kind": "content", "template": "derivation", "say": _SAY,
             "steps": [{"math": "a = b"}, {"math": "b = c"}], "result": {"math": "a = c"},
             "focus": focus}
    return {"meta": {"id": "_t", "section": "0.0"}, "scenes": [scene]}


def _errors(data):
    return [m for s, m in S.schema_storyboard(data) if s == "error"]


def test_dimming_a_block_a_later_beat_reveals_is_an_error():
    errs = _errors(_deck([{"at": "step.1", "dim": ["step.0", "result"]}]))
    assert len(errs) == 1, errs
    assert "der.focus[0].dim 'result'" in errs[0] and "later" in errs[0], errs


def test_indicating_a_block_a_later_beat_reveals_is_an_error():
    errs = _errors(_deck([{"at": "step.0", "dim": [], "indicate": ["step.1"]}]))
    assert len(errs) == 1 and "der.focus[0].indicate 'step.1'" in errs[0], errs


def test_blocks_already_on_screen_are_fine():
    # dim what came before; indicate the beat's own reveal (indicate plays AFTER it) and
    # an earlier one; restore with an empty dim
    assert _errors(_deck([{"at": "step.1", "dim": ["step.0"]},
                          {"at": "result", "dim": [], "indicate": ["result", "step.0"]}])) == []


# A corner `carry` is the one block a later {show} does NOT introduce: templates._apply_carry
# gives it pre_play=restore, scene._stage adds it at t=0 where the previous scene left it, and
# its {show <as>} is the flight to the corner (RG2-01). The algebra enters first here.
_CARRY_SAY = ("The curve is still here. {show step.0} Meanwhile the algebra. "
              "{show carried.curve} Now it flies. {show result} And lands.")


def _carry_deck(focus):
    src = {"id": "src", "kind": "content", "template": "graph", "mode": "single",
           "title": "Src", "say": "A curve. {show plot.0} There.",
           "plots": [{"kind": "function", "expression": "sin(x)", "x_range": [0, 3]}]}
    scene = {"id": "fly", "kind": "content", "template": "derivation", "title": "Fly",
             "carry": [{"from": "src", "block": "plot.0", "as": "carried.curve",
                        "to": {"corner": "top_right", "scale": 0.35}}],
             "say": _CARRY_SAY, "steps": [{"math": "a = b"}], "result": {"math": "a = c"},
             "focus": focus}
    return {"meta": {"id": "_t", "section": "0.0"}, "scenes": [src, scene]}


def test_dimming_a_corner_carry_before_its_flight_is_fine():
    assert _errors(_carry_deck([{"at": "step.0", "dim": ["carried.curve"]},
                                {"at": "carried.curve", "dim": []}])) == []


def test_indicating_a_corner_carry_before_its_flight_is_fine():
    assert _errors(_carry_deck([{"at": "step.0", "dim": [],
                                 "indicate": ["carried.curve"]}])) == []


def test_a_normal_later_reveal_in_a_carry_scene_is_still_an_error():
    errs = _errors(_carry_deck([{"at": "step.0", "dim": ["carried.curve", "result"]}]))
    assert len(errs) == 1 and "fly.focus[0].dim 'result'" in errs[0], errs


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] focus_reveal_order green")

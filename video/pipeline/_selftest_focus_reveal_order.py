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


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] focus_reveal_order green")

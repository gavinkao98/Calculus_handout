"""Self-test: a block the source scene EXITS cannot be carried out of it
(code-review-2026-09-23 F-05). Run from video/:
    python -m pipeline._selftest_carry_exit_conflict

`exit:` fades the named blocks out inside the source scene's tail (scene.py _tail); make.py
hard-cuts every carry boundary; the next scene then opens with the carried copy where the
source left it. A block on BOTH lists therefore fades out and snaps back across the cut --
the exact flicker SPEC-motion-language rule 1 ("objects persist across the cut") rules out.
No gate crossed the two lists (schema checks carry's shape, sizecheck each list's ids
alone), so it is a schema error now. Pure dict logic; no manim.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import schema as S   # noqa: E402


def _deck(src_exit, block, to="keep"):
    src = {"id": "squeeze_graph", "kind": "content", "template": "graph",
           "say": "Look at the curve.", "exit": src_exit}
    say = "Words. {show body} More." if to == "keep" else "Words. {show carried} More."
    dst = {"id": "limit_not_identity", "kind": "content", "template": "callout", "say": say,
           "carry": [{"from": "squeeze_graph", "block": block, "as": "carried", "to": to}]}
    return {"meta": {"id": "_t", "section": "0.0"}, "scenes": [src, dst]}


def _errors(data):
    return [m for s, m in S.schema_storyboard(data) if s == "error"]


def test_carrying_a_block_the_source_scene_exits_is_an_error():
    errs = _errors(_deck(["plot.0", "annotation.0"], "plot.0"))
    assert len(errs) == 1, errs
    assert "limit_not_identity.carry[0]" in errs[0] and "'plot.0'" in errs[0], errs
    assert "squeeze_graph" in errs[0] and "exit" in errs[0], errs


def test_any_id_of_a_carried_group_counts():
    corner = {"corner": "top_right", "scale": 0.4}
    errs = _errors(_deck(["ticks"], ["axes", "ticks", "plot.0"], to=corner))
    assert len(errs) == 1 and "'ticks'" in errs[0], errs


def test_exiting_only_what_is_not_carried_is_fine():
    assert _errors(_deck(["annotation.0", "inset"], ["axes", "ticks", "plot.0"])) == []
    assert _errors(_deck([], "plot.0")) == []


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] carry_exit_conflict green")

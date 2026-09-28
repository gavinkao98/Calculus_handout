"""Self-test: every scene_head template finds its title BY ID, so `part:` moves nothing.

Run from video/:  python -m pipeline._selftest_title_by_id

The defect this locks (code review 2026-09-23, D1-03). `_common.scene_head` puts the
multipage indicator (`part: {current, total}`) in the head list BEFORE the title, so on a
`part:` scene the old `head[1]` / `blocks[1]` lookup handed the template the top-right
'2 / 2' tag instead of the title. derivation (no `prompt:`) then anchored its body zone,
its scaffold and its whole chain to that tag's left edge -- x = 5.52, the chain running off
the right of the frame to x ~ 15 -- and definition_math / procedure_steps / recap_cards /
sign_chart / value_table read the same wrong block. theorem_proof had already switched to
the by-id lookup (theorem_proof.py, "NOT head[1]"); the rest now do too.

The contract: the part indicator is top-right furniture on the decoration layer, so adding
`part:` to a scene changes NOTHING else on screen -- every other block keeps its geometry.
Manim-backed (real Tex is built and measured), so it takes a minute or two.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # templates import manim at module level -- bootstrap FIRST (repo rule)

import logging  # noqa: E402

logging.disable(logging.INFO)

from pathlib import Path  # noqa: E402

import yaml  # noqa: E402

from pipeline.templates import build_blocks  # noqa: E402
from pipeline.templates._common import SPINE_X  # noqa: E402

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}
_STORYBOARDS = Path(__file__).resolve().parent.parent / "storyboards"
_PART = {"current": 2, "total": 2}
_EPS = 1e-6

# The reviewer's repro (r7_derivation_part.py): a plain derivation chain -- no prompt, so
# scene_head, not example_head -- long enough that an author would split it across pages.
_DERIVATION = {
    "id": "d", "kind": "content", "template": "derivation", "accent": "derivation",
    "title": "Inverting a cubic, continued",
    "say": "A. {show step.0} B. {show step.1} C. {show result} D.",
    "steps": [{"math": "y = x^3 + 2", "reason": "write $y=f(x)$"},
              {"math": "x^3 = y - 2", "reason": "subtract 2"}],
    "result": {"math": "f^{-1}(x) = \\sqrt[3]{x-2}", "reason": "swap names"},
}

# One real scene per scene_head template (the capacity demo deck carries a `*_fit` scene for
# each; sign_chart has its own demo deck). theorem_proof and callout already looked the title
# up by id -- they are here as the control that the comparison itself is sound.
_TEMPLATE_SCENES = [
    ("_demo_capacity.yml", "derivation_fit"),
    ("_demo_capacity.yml", "definition_fit"),
    ("_demo_capacity.yml", "procedure_fit"),
    ("_demo_capacity.yml", "recap_fit"),
    ("_demo_capacity.yml", "value_table_fit"),
    ("_demo_sign_chart.yml", "cubic_monotonicity"),
    ("_demo_capacity.yml", "theorem_fit"),
    ("_demo_capacity.yml", "callout_sparse"),
]


def _build(spec, meta=None):
    return {b.id: b for b in build_blocks(dict(spec), {"ground": "dark", "meta": meta or _META})}


def _box(mob):
    return (float(mob.get_left()[0]), float(mob.get_right()[0]),
            float(mob.get_bottom()[1]), float(mob.get_top()[1]))


def _moved(plain, paged):
    """Block ids (other than the part tag itself) whose bbox differs between the two builds."""
    out = []
    for bid, b in plain.items():
        if bid == "part" or bid not in paged:
            continue
        a, c = _box(b.mobject), _box(paged[bid].mobject)
        if any(abs(x - y) > _EPS for x, y in zip(a, c)):
            out.append(f"{bid}: {tuple(round(v, 2) for v in a)} -> {tuple(round(v, 2) for v in c)}")
    return out


def test_derivation_part_without_prompt_keeps_the_chain_on_the_spine():
    plain = _build(_DERIVATION)
    paged = _build({**_DERIVATION, "part": _PART})
    assert "part" in paged, "the fixture must actually carry the part indicator"
    for bid in ("step.0", "step.1", "result"):
        x0 = plain[bid].mobject.get_left()[0]
        x1 = paged[bid].mobject.get_left()[0]
        assert abs(x0 - x1) < _EPS, (
            f"{bid}: left edge {x1:.2f} with part: vs {x0:.2f} without -- the chain must stay "
            f"on the spine (x = {SPINE_X:.2f}), not follow the top-right part tag")
    assert not _moved(plain, paged), _moved(plain, paged)


def test_derivation_scaffold_hangs_under_the_title_not_the_part_tag():
    over = {"scaffold": {"motive": "Finish the inversion."}}
    plain = _build({**_DERIVATION, **over})
    paged = _build({**_DERIVATION, **over, "part": _PART})
    assert "scaffold.motive" in paged
    assert not _moved(plain, paged), _moved(plain, paged)


def test_every_scene_head_template_ignores_the_part_indicator():
    decks: dict = {}
    bad = []
    for deck, sid in _TEMPLATE_SCENES:
        if deck not in decks:
            decks[deck] = yaml.safe_load((_STORYBOARDS / deck).read_text(encoding="utf-8"))
        d = decks[deck]
        spec = next(s for s in d["scenes"] if s.get("id") == sid)
        assert not spec.get("part") and not spec.get("prompt"), f"{sid}: fixture must be a plain scene_head scene"
        plain = _build(spec, d["meta"])
        paged = _build({**spec, "part": _PART}, d["meta"])
        assert "part" in paged, f"{sid}: the part indicator must be built"
        moved = _moved(plain, paged)
        if moved:
            bad.append(f"{spec['template']} ({sid}): " + "; ".join(moved[:3]))
    assert not bad, "adding `part:` moved blocks:\n  " + "\n  ".join(bad)


if __name__ == "__main__":
    import sys
    import traceback

    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}", flush=True)
            except Exception:
                fails += 1
                print(f"FAIL {name}", flush=True)
                traceback.print_exc()
    print(f"[title_by_id] {'all green' if not fails else f'{fails} RED'}", flush=True)
    sys.exit(1 if fails else 0)

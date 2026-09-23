"""Self-test: theorem_proof's aside path keeps the statement card out of the aside's column.

Run from video/:  python -m pipeline._selftest_theorem_aside

The defect this locks (code review 2026-09-23, D1-05). On the statement-only + `aside:` path
the statement wrapped at `PRIMARY_W - 0.3` and the accent panel then added its own 0.6u
padding on EACH side, so a card whose text wrapped could reach PRIMARY_W + 0.9 -- its right
edge up to 0.9u past RAIL_X, where the aside card's left edge sits. A ~100-character
statement already put the two cards 0.61u on top of each other (the aside is on the
decoration layer, so the overlap guard never saw it). The wrap width now subtracts the
card's padding, so the card's right edge stays a column gap (0.3u) short of RAIL_X.

(The aside's layer is deliberately unchanged here; flagging an aside that leaves its box is
sizecheck's job, V3 batch.) Manim-backed: real Tex is built and measured.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # templates import manim at module level -- bootstrap FIRST (repo rule)

import logging  # noqa: E402

logging.disable(logging.INFO)

from pipeline.templates import build_blocks  # noqa: E402
from pipeline.templates._common import RAIL_X, SPINE_X  # noqa: E402

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}
_COL_GAP = 0.3     # clear space between the statement card and the aside column
_EPS = 1e-3

_STATEMENTS = [
    "If $f$ is strictly increasing, then $f$ is one-to-one.",
    # the reviewer's repro (r11_aside.py): ~100 characters, wraps to two or three lines
    "If $f$ is strictly increasing on an interval $I$, then $f$ is one-to-one on $I$, "
    "so it has an inverse there.",
    # markup-free text takes a different wrap route (body_text) than inline-math prose
    "A function that is strictly increasing on an interval never takes the same value "
    "twice there, so every horizontal line meets its graph at most once.",
]


def _build(statement):
    spec = {"id": "ta", "kind": "content", "template": "theorem_proof", "accent": "theorem",
            "title": "Increasing Implies One-to-One", "say": "State it.",
            "statement": statement,
            "aside": {"label": "Key idea", "body": "Monotone means no horizontal line hits twice."}}
    return {b.id: b for b in build_blocks(spec, {"ground": "dark", "meta": _META})}


def test_the_statement_card_stays_left_of_the_aside_column():
    bad = []
    for stmt in _STATEMENTS:
        by = _build(stmt)
        card, aside = by["statement"].mobject, by["aside"].mobject
        right = card.get_right()[0]
        if right > RAIL_X - _COL_GAP + _EPS or right >= aside.get_left()[0]:
            bad.append(f"card right {right:.2f} vs RAIL_X {RAIL_X:.2f} "
                       f"(aside left {aside.get_left()[0]:.2f}) for {stmt[:40]!r}...")
    assert not bad, "the statement card runs into the aside column:\n  " + "\n  ".join(bad)


def test_cards_are_still_on_the_spine_and_the_rail():
    by = _build(_STATEMENTS[1])
    assert abs(by["statement"].mobject.get_left()[0] - SPINE_X) < _EPS
    assert abs(by["aside"].mobject.get_left()[0] - RAIL_X) < _EPS


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
    print(f"[theorem_aside] {'all green' if not fails else f'{fails} RED'}", flush=True)
    sys.exit(1 if fails else 0)

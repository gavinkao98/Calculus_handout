"""Self-test: a `paced:` worked_example answer band brings its frame in WITH the answer.

Run from video/:  python -m pipeline._selftest_answer_band_paced

The defect this locks (code review 2026-09-23, D1-04). `worked_example._answer_box` returns
VGroup(box, eq, tag) and declared no chrome/content split, so once `paced:` named `result`
(the template's own contract example and the demo deck both do) `pacing.block_parts` walked
its three top-level submobjects: the EMPTY answer frame faded in alone and held a third of
the beat, then the answer, then the tag -- on the demo's 6 s beat, 1.8 s of empty box. The
same "chrome alone first" defect `pacing.chrome_of` exists to prevent (recap_cards declares
it). The band now declares `_paced_chrome = box` and `_paced_parts = [eq, tag]`.

Render-free apart from building the real Tex: the reveal runs against a fake scene that
records what each play was asked to show.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # templates import manim at module level -- bootstrap FIRST (repo rule)

import logging  # noqa: E402

logging.disable(logging.INFO)

from pathlib import Path  # noqa: E402

import yaml  # noqa: E402

from pipeline import pacing  # noqa: E402
from pipeline.blocks import play_block  # noqa: E402
from pipeline.templates import build_blocks  # noqa: E402

_DECK = Path(__file__).resolve().parent.parent / "storyboards" / "_demo_worked_example.yml"
_SCENE = "companion_limit_example"      # carries `paced: [step.0, result]`


class FakeScene:
    """Records each play's mobjects and each wait instead of rendering."""

    def __init__(self, beat_seconds):
        self.beat_seconds = beat_seconds
        self.log: list = []

    def play(self, *anims, **kw):
        self.log.append(("play", [getattr(a, "mobject", None) for a in anims]))

    def wait(self, seconds):
        self.log.append(("wait", float(seconds)))

    def add(self, *mobs):
        pass


def _result():
    deck = yaml.safe_load(_DECK.read_text(encoding="utf-8"))
    spec = next(s for s in deck["scenes"] if s["id"] == _SCENE)
    assert "result" in (spec.get("paced") or []), "fixture must pace the result"
    blocks = build_blocks(spec, {"ground": "dark", "meta": deck["meta"]})
    res = next(b for b in blocks if b.id == "result")
    assert res.anim is pacing.paced_reveal, "the paced result must take the paced walk"
    return res


def _plays(res, beat=6.0):
    sc = FakeScene(beat_seconds=beat)
    play_block(sc, res, "dark")
    return [mobs for kind, mobs in sc.log if kind == "play"]


def test_the_first_play_already_carries_the_answer():
    res = _result()
    box, eq = res.mobject[0], res.mobject[1]
    plays = _plays(res)
    assert plays, "the paced result must play something"
    assert eq in plays[0], (
        "the answer equation must enter on the FIRST play -- an empty answer frame must not "
        f"hold the screen first (first play showed {[type(m).__name__ for m in plays[0]]})")
    assert box in plays[0], "the frame rides in together with the answer, not on a later play"


def test_no_play_shows_the_frame_alone():
    res = _result()
    box = res.mobject[0]
    alone = [i for i, mobs in enumerate(_plays(res)) if mobs == [box]]
    assert not alone, f"the empty answer frame was revealed on its own (play {alone})"


def test_the_band_walks_answer_then_tag():
    band = _result().mobject
    box, eq, tag = band[0], band[1], band[2]
    assert pacing.chrome_of(band) is box
    assert pacing.block_parts(band) == [eq, tag]


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
    print(f"[answer_band_paced] {'all green' if not fails else f'{fails} RED'}", flush=True)
    sys.exit(1 if fails else 0)

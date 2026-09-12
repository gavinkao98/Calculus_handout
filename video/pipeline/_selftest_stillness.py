"""Self-test: SPEC-motion-language rule 4 -- undeclared stillness advisory. Run from video/:
    python -m pipeline._selftest_stillness

`stillness.undeclared_still_beats` is the pure judge behind make.py's `[stillness]` warning:
a beat whose screen sits still for more than 6 s with nothing declared (no `paced:`, no
`pauses:`, no callable/beat-filling animation) is the defect the §3.1 six-lens review kept
finding ("one reveal then 18 s of nothing"; "first beat, no reveal, 37.6 s"). This pins:
  (a) a long beat with only a stock reveal is reported, with its still seconds
  (b) the same beat is NOT reported when its reveal is in `paced:`
  (c) ... nor when it has a `pauses:` entry
  (d) ... nor when its animation is a callable (anim_seconds None = motion fills the beat)
  (e) a first beat with no reveal at all is reported for its whole length
  (f) a beat under the threshold is not reported
  (g) exactly the threshold is not reported (strictly greater than)

Manim-free: plain dicts and sets.
"""
from pipeline.stillness import UNDECLARED_STILL_SECONDS, undeclared_still_beats

STOCK = {"step.0": 0.45}


def _judge(beats, anim_seconds=STOCK, paced=(), pauses_after=()):
    return undeclared_still_beats(beats, anim_seconds, set(paced), set(pauses_after))


def test_threshold_is_the_spec_value():
    assert UNDECLARED_STILL_SECONDS == 6.0


# -- (a) the defect ------------------------------------------------------------

def test_long_beat_with_stock_reveal_is_reported():
    hits = _judge([{"index": 2, "reveal": "step.0", "seconds": 8.0}])
    assert len(hits) == 1, hits
    index, still, reveal = hits[0]
    assert index == 2 and reveal == "step.0"
    assert abs(still - 7.55) < 1e-9, still      # 8.0 - 0.45 stock reveal


# -- (b)(c)(d) the three declared ways a long beat is intentional --------------

def test_paced_reveal_is_not_reported():
    assert _judge([{"index": 2, "reveal": "step.0", "seconds": 8.0}], paced={"step.0"}) == []


def test_paused_reveal_is_not_reported():
    assert _judge([{"index": 2, "reveal": "step.0", "seconds": 8.0}],
                  pauses_after={"step.0"}) == []


def test_callable_animation_is_not_reported():
    """anim_seconds None = a hook / sweep / `seconds: beat` -- the picture moves by itself."""
    assert _judge([{"index": 2, "reveal": "step.0", "seconds": 8.0}],
                  anim_seconds={"step.0": None}) == []


# -- (e) the first-beat case from the six-lens review --------------------------

def test_first_beat_without_reveal_is_reported_for_its_whole_length():
    hits = _judge([{"index": 1, "reveal": None, "seconds": 7.0}])
    assert hits == [(1, 7.0, None)], hits


def test_reveal_naming_no_animated_block_counts_as_no_motion():
    """A reveal absent from anim_seconds (static / unknown block) animates nothing."""
    hits = _judge([{"index": 3, "reveal": "ghost", "seconds": 9.0}])
    assert hits == [(3, 9.0, "ghost")], hits


# -- (f)(g) the threshold --------------------------------------------------------

def test_short_beat_is_not_reported():
    assert _judge([{"index": 2, "reveal": "step.0", "seconds": 5.0}]) == []


def test_exactly_the_threshold_is_not_reported():
    assert _judge([{"index": 1, "reveal": None, "seconds": 6.0}]) == []
    assert _judge([{"index": 1, "reveal": None, "seconds": 6.0 + 1e-6}]) != []


def test_only_the_offending_beats_are_listed_in_order():
    beats = [{"index": 1, "reveal": None, "seconds": 4.4},
             {"index": 2, "reveal": "step.0", "seconds": 7.1},
             {"index": 3, "reveal": "step.1", "seconds": 20.9},
             {"index": 4, "reveal": "result", "seconds": 19.4}]
    hits = _judge(beats, anim_seconds={"step.0": 0.45, "step.1": 1.2, "result": 0.5},
                  paced={"result"})
    assert [(i, r) for i, _s, r in hits] == [(2, "step.0"), (3, "step.1")], hits


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

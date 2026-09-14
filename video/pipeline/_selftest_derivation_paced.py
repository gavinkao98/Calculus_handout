"""Self-test: a `paced` derivation morph row with no reason rail. Run from video/:
    python -m pipeline._selftest_derivation_paced

`paced:` on an `anim: transform` / `cancel` row means "leave the rail OUT of the morph play
and walk it across the rest of the beat" (rollout T1-1, templates/derivation). A row with no
`reason:` has no rail, so there is nothing to walk -- but `_rail` used to hand back the
equation's own WRAPPER (a result sits in a glow group) as if it were one rail part. The row
then reported "walkable", took the whole rest of the beat, re-faded the equation the morph
had just drawn, and held; and because `paced:` exempts a beat from the [stillness] advisory,
nothing said so (§8 backlog 16; ch03 22 `all_six_cot_csc.result`, 11.26 s).

This pins the three parts of the fix:
  (1) a paced row WITH a reason still has a rail and still walks it (unchanged)
  (2) a paced row with NO reason has an empty rail -> `_rail_walk_seconds` is None, the
      callable plays its morph and nothing else, and the beat's remainder is a plain hold
  (3) `schema` warns on the declaration itself, so the author sees it without a render
      (the [stillness] advisory cannot: it exempts every reveal named in `paced:`)

Plus the unpaced half of the same defect: without a rail the morph play must not carry a
`FadeIn` of its own target (ch03 20 `all_six_tan_sec.result`).
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # derivation imports manim at module level -- bootstrap FIRST

from manim import FadeIn  # noqa: E402

from pipeline.schema import schema_storyboard  # noqa: E402
from pipeline.templates import build_blocks  # noqa: E402
from pipeline.templates import derivation as D  # noqa: E402

_META = {"id": "_p", "chapter": "Chapter 9", "section": "9.9", "title": "P", "theme": "midnight"}
NO_RAIL_MSG = "has nothing to walk (no reason rail)"


def _spec(*, result_reason, paced=("result",)):
    """A two-step chain whose `result` morphs from the last step. `result_reason=None` is the
    shape under test: `anim: transform` + `paced:` + no rail to walk."""
    result = {"math": r"\frac{d}{dx}\csc x = -\csc x\cot x", "anim": "transform"}
    if result_reason:
        result["reason"] = result_reason
    return {
        "id": "der", "kind": "content", "template": "derivation", "accent": "example",
        "title": "A Derivation",
        "say": "One. {show step.0} Two. {show step.1} Three. {show result} Four.",
        "steps": [{"math": r"\frac{d}{dx}\csc x = \frac{0\cdot\sin x-1\cdot\cos x}{\sin^{2} x}",
                   "reason": "quotient rule"},
                  {"math": r"= -\frac{\cos x}{\sin^{2} x}", "reason": "tidy up",
                   "anim": "transform"}],
        "result": result,
        **({"paced": list(paced)} if paced else {}),
    }


def _deck(**kw):
    return {"meta": {"id": "deck", "section": "9.9"}, "scenes": [_spec(**kw)]}


def _blocks(**kw):
    return build_blocks(_spec(**kw), {"ground": "dark", "meta": _META})


def _b(blocks, bid):
    return next(x for x in blocks if x.id == bid)


def _rail_of(block):
    """The rail the row's own animation will compute, from the same two inputs it uses."""
    return D._rail(block.mobject, D._eq_core(block.mobject))


class _FakeScene:
    """Records what the callable asks for instead of rendering. `beat_seconds` is what the
    real LessonScene sets before each beat (None = off-beat)."""

    def __init__(self, beat_seconds=None):
        self.beat_seconds = beat_seconds
        self.added, self.played, self.waits = [], [], []

    def add(self, *mobs):
        self.added.extend(mobs)

    def play(self, *anims, **kw):
        self.played.append((anims, kw))

    def wait(self, seconds):
        self.waits.append(float(seconds))


# -- (1) a reason rail is still walked ------------------------------------------

def test_a_paced_row_with_a_reason_has_a_rail_and_walks_it():
    block = _b(_blocks(result_reason="the six are done"), "result")
    rail = _rail_of(block)
    assert len(rail.submobjects) == 2, "want the dotted leader + the reason tag"
    secs = D._rail_walk_seconds(_FakeScene(beat_seconds=12.0), rail, D.TRANSFORM_SECONDS, True)
    assert secs is not None and secs > 0.0, secs

    scene = _FakeScene(beat_seconds=12.0)
    spent = block.anim(scene, block.mobject, "dark")
    assert len(scene.played) == 1 + 2, "the morph, then one fade per rail part"
    assert spent > D.TRANSFORM_SECONDS, spent


# -- (2) no reason -> no rail -> no walk ----------------------------------------

def test_a_paced_row_with_no_reason_has_an_empty_rail():
    """The glow group `_eq_mob` wraps a result in is NOT a rail part: walking it walks the
    equation itself."""
    rail = _rail_of(_b(_blocks(result_reason=None), "result"))
    assert rail.submobjects == [], [type(m).__name__ for m in rail.submobjects]


def test_a_paced_row_with_no_reason_reports_no_walk_seconds():
    rail = _rail_of(_b(_blocks(result_reason=None), "result"))
    assert D._rail_walk_seconds(_FakeScene(beat_seconds=12.0), rail,
                                D.TRANSFORM_SECONDS, True) is None


def test_a_paced_row_with_no_reason_plays_only_its_morph():
    """The beat's remainder becomes an ordinary hold that the row does not pretend to fill."""
    block = _b(_blocks(result_reason=None), "result")
    scene = _FakeScene(beat_seconds=12.0)
    spent = block.anim(scene, block.mobject, "dark")
    assert spent == D.TRANSFORM_SECONDS, spent
    assert len(scene.played) == 1 and scene.waits == [], (scene.played, scene.waits)


def test_an_unpaced_row_with_no_reason_does_not_re_fade_its_own_equation():
    """The other half of the same defect: with the wrapper counted as rail, the morph play
    carried `FadeIn(wrapper)` -- a second animation on the morph's own target."""
    block = _b(_blocks(result_reason=None, paced=None), "result")
    scene = _FakeScene(beat_seconds=12.0)
    block.anim(scene, block.mobject, "dark")
    assert len(scene.played) == 1
    assert not [a for a in scene.played[0][0] if isinstance(a, FadeIn)], scene.played[0][0]


def test_the_rail_is_unchanged_for_an_unpaced_row_that_has_one():
    """Zero behaviour change where a rail exists: it still rides the morph play."""
    block = _b(_blocks(result_reason="the six are done", paced=None), "result")
    scene = _FakeScene(beat_seconds=12.0)
    block.anim(scene, block.mobject, "dark")
    assert len(scene.played) == 1
    assert [a for a in scene.played[0][0] if isinstance(a, FadeIn)], "the rail rides the morph"


# -- (3) the author-facing gate -------------------------------------------------

def test_schema_warns_when_a_paced_morph_row_has_no_rail():
    issues = schema_storyboard(_deck(result_reason=None))
    assert not [m for s, m in issues if s == "error"], issues
    hits = [m for s, m in issues if s == "warn" and NO_RAIL_MSG in m]
    assert len(hits) == 1, issues
    assert "'result'" in hits[0], hits[0]


def test_schema_is_quiet_when_the_paced_morph_row_has_a_reason():
    issues = schema_storyboard(_deck(result_reason="the six are done"))
    assert not [m for _s, m in issues if NO_RAIL_MSG in m], issues


def test_schema_is_quiet_when_the_row_is_not_paced_at_all():
    """The warning is about the declaration, not the row: an unpaced morph row without a
    reason is an ordinary reveal and perfectly fine."""
    issues = schema_storyboard(_deck(result_reason=None, paced=None))
    assert not [m for _s, m in issues if NO_RAIL_MSG in m], issues


def test_schema_is_quiet_for_a_paced_row_that_is_not_a_morph():
    """A stock reveal named in `paced:` is walked by pacing.apply over its own parts -- it
    never asks derivation for a rail, so `reason` says nothing about it."""
    deck = _deck(result_reason=None)
    deck["scenes"][0]["result"].pop("anim")
    deck["scenes"][0]["paced"] = ["result"]
    issues = schema_storyboard(deck)
    assert not [m for _s, m in issues if NO_RAIL_MSG in m], issues


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

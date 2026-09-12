"""Self-test: `carry:` / `exit:` -- objects that persist across a cut (motion primitive 5,
object side; SPEC-motion-language rule 1). Run from video/:
    python -m pipeline._selftest_carry

Builds a three-scene mini deck (graph -> derivation -> callout), no render. Pins:
  * zero behaviour change: a scene without `carry` builds the same blocks with or without
    the deck in ctx
  * `to: keep` -> a STATIC copy of the source block, same bbox as in the source scene, same
    layer, a distinct object (the source scene's mobject is never shared)
  * `to: {corner, scale}` -> the block is BUILT at its terminal place (the layout gates
    measure the frame the scene ends on) and `Block.pre_play` rewinds it to the carried-in
    position; the reveal is a callable that plays ONE flight and reports its seconds, which
    `anim_seconds` also carries for make.py's short-beat warning
  * a chain (c carries what b carried from a) resolves through the middle scene
  * the errors are loud: no deck in ctx / unknown block / `as` colliding / `from` not earlier
  * the carry runs BEFORE the hook, so a hook sees (and may edit) the carried block
  * sizecheck turns a build failure into an error and cross-checks `exit` ids
  * scene.py: `_stage` puts pre_play blocks on screen rewound; `_tail` fades `exit` blocks
    inside the SCENE_TAIL_SECONDS hold, leaving the clip length unchanged
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # templates import manim at module level -- bootstrap FIRST

from manim import FadeOut

from pipeline import sizecheck
from pipeline.blocks import Block
from pipeline.scene import LessonScene
from pipeline.templates import build_blocks
from pipeline.timing import EXIT_FADE_SECONDS, SCENE_TAIL_SECONDS, STOCK_ANIM_SECONDS
from pipeline.visuals import theme as T

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}

_GRAPH = {
    "id": "g", "kind": "content", "template": "graph", "mode": "single", "accent": "definition",
    "title": "A Curve", "say": "Look. {show plot.1} A point.",
    "axes": {"x_range": [0, 3.4, 1], "y_range": [-0.2, 1.3, 0.5], "x_length": 7.0, "y_length": 3.6},
    "plots": [{"kind": "function", "expression": "sin(x)", "x_range": [0, 3.14159],
               "color_role": "secondary"},
              {"kind": "point", "point": [1.5708, 1.0], "hollow": False, "color_role": "accent",
               "reveal": True}],
}
_DER = {
    "id": "d", "kind": "content", "template": "derivation", "accent": "derivation",
    "title": "Bounds", "say": "One. {show carried.curve} Two. {show step.0} Three. {show result} Four.",
    "steps": [{"math": r"\sin x \le x", "reason": "given"}],
    "result": {"math": r"\frac{\sin x}{x} \le 1", "reason": "divide"},
    "carry": [{"from": "g", "block": "plot.0", "as": "carried.curve",
               "to": {"corner": "top_right", "scale": 0.35}}],
}
_CALL = {
    "id": "c", "kind": "content", "template": "callout", "type": "note", "title": "Stays",
    "say": "Words. {show body} More.", "body": "The corner copy stays.",
    "carry": [{"from": "d", "block": "carried.curve", "as": "carried.curve", "to": "keep"}],
}
_DECK = [_GRAPH, _DER, _CALL]
_BY_ID = {s["id"]: s for s in _DECK}


def _ctx(deck=_BY_ID):
    ctx = {"ground": "dark", "meta": _META}
    if deck is not None:
        ctx["scenes_by_id"] = deck
    return ctx


def _b(blocks, bid):
    return next(x for x in blocks if x.id == bid)


def _bbox(mob):
    return tuple(round(float(v), 4) for v in (mob.get_left()[0], mob.get_right()[0],
                                                 mob.get_bottom()[1], mob.get_top()[1]))


# -- zero behaviour change -------------------------------------------------------------------

def test_a_scene_without_carry_is_unchanged_by_the_deck_in_ctx():
    plain = build_blocks(_GRAPH, {"ground": "dark", "meta": _META})
    with_deck = build_blocks(_GRAPH, _ctx())
    assert [b.id for b in plain] == [b.id for b in with_deck]
    assert [_bbox(b.mobject) for b in plain] == [_bbox(b.mobject) for b in with_deck]


# -- keep ---------------------------------------------------------------------------------------

def test_keep_is_a_static_copy_at_the_source_position_on_the_source_layer():
    src = _b(build_blocks(_DER, _ctx()), "carried.curve")
    got = _b(build_blocks(_CALL, _ctx()), "carried.curve")
    assert got.static is True
    assert got.layer == src.layer == "graph"
    assert _bbox(got.mobject) == _bbox(src.mobject), (_bbox(got.mobject), _bbox(src.mobject))
    assert got.mobject is not src.mobject
    assert got.pre_play is None


# -- corner ---------------------------------------------------------------------------------------

def test_corner_is_built_at_its_terminal_place_and_pre_play_rewinds_it():
    source = _b(build_blocks(_GRAPH, _ctx()), "plot.0")
    got = _b(build_blocks(_DER, _ctx()), "carried.curve")
    assert got.static is False and callable(got.anim)
    assert got.anim_seconds == STOCK_ANIM_SECONDS["carry"] == 0.8
    assert got.layer == source.layer
    x0, x1, y0, y1 = _bbox(got.mobject)
    sx0, sx1, sy0, sy1 = _bbox(source.mobject)
    assert abs((x1 - x0) - 0.35 * (sx1 - sx0)) < 1e-3, "built at the scaled size"
    assert abs(x1 - (T.FRAME_W / 2 - T.SAFE_MARGIN)) < 1e-3, "flush to the safe margin, right"
    assert abs(y1 - (T.FRAME_H / 2 - T.SAFE_MARGIN)) < 1e-3, "flush to the safe margin, top"
    assert got.pre_play is not None
    got.pre_play(got.mobject)
    assert _bbox(got.mobject) == _bbox(source.mobject), "pre_play must rewind to where the last scene left it"


class _FakeScene:
    def __init__(self, spec=None):
        self.spec = spec or {}
        self.added, self.played, self.waited = [], [], []

    def add(self, *mobs):
        self.added.extend(mobs)

    def play(self, *anims, **kw):
        self.played.append((anims, kw))

    def wait(self, seconds):
        self.waited.append(seconds)


def test_flight_plays_one_animation_and_reports_its_seconds():
    got = _b(build_blocks(_DER, _ctx()), "carried.curve")
    scene = _FakeScene()
    secs = got.anim(scene, got.mobject, "dark")
    assert secs == STOCK_ANIM_SECONDS["carry"]
    assert len(scene.played) == 1 and scene.played[0][1]["run_time"] == secs


# -- chain + errors ---------------------------------------------------------------------------------

def test_chain_resolves_through_the_middle_scene():
    """c carries `carried.curve` from d, which d itself carried from g: building c must
    expand d's carry (else d has no `carried.curve`)."""
    ids = {b.id for b in build_blocks(_CALL, _ctx())}
    assert "carried.curve" in ids


def test_no_deck_in_ctx_is_a_loud_error():
    try:
        build_blocks(_DER, _ctx(deck=None))
    except ValueError as exc:
        assert "scenes_by_id" in str(exc)
    else:
        raise AssertionError("carry without the deck must raise, not silently skip")


def test_unknown_block_lists_what_the_source_builds():
    bad = {**_DER, "carry": [{**_DER["carry"][0], "block": "plot.9"}]}
    try:
        build_blocks(bad, _ctx())
    except ValueError as exc:
        assert "plot.9" in str(exc) and "plot.0" in str(exc), str(exc)
    else:
        raise AssertionError("unknown carry.block must raise")


def test_as_colliding_with_an_own_block_raises():
    bad = {**_DER, "carry": [{**_DER["carry"][0], "as": "step.0"}]}
    try:
        build_blocks(bad, _ctx())
    except ValueError as exc:
        assert "step.0" in str(exc)
    else:
        raise AssertionError("as colliding with a block the scene builds must raise")


def test_from_must_be_earlier_in_the_deck():
    """The recursion terminates because `from` is always strictly earlier; a deck that says
    otherwise (schema catches it first) must not loop."""
    loop_a = {**_GRAPH, "id": "la", "carry": [{"from": "lb", "block": "body", "as": "x"}]}
    loop_b = {**_CALL, "id": "lb", "carry": [{"from": "la", "block": "plot.0", "as": "y"}]}
    try:
        build_blocks(loop_a, _ctx(deck={"la": loop_a, "lb": loop_b}))
    except ValueError as exc:
        assert "earlier" in str(exc), str(exc)
    else:
        raise AssertionError("a forward carry must raise")


# -- carry before hook ------------------------------------------------------------------------------

def _hook(spec, ctx, blocks):
    b = next(x for x in blocks if x.id == "carried.curve")   # would raise if carry ran after
    b.layer = "decoration"
    return blocks


def test_hook_sees_the_carried_block():
    hooked = {**_DER, "hook": "pipeline._selftest_carry:_hook"}
    assert _b(build_blocks(hooked, _ctx()), "carried.curve").layer == "decoration"


# -- sizecheck ---------------------------------------------------------------------------------------

def test_sizecheck_turns_a_carry_build_failure_into_an_error():
    bad = {**_DER, "carry": [{**_DER["carry"][0], "block": "plot.9"}]}
    errs = [m for s, m in sizecheck.check_scenes(_META, [bad], deck=[_GRAPH, bad, _CALL]) if s == "error"]
    assert any("could not build" in m and "plot.9" in m for m in errs), errs


def test_sizecheck_cross_checks_exit_ids():
    bad = {**_GRAPH, "exit": ["axes", "nope"]}
    errs = [m for s, m in sizecheck.check_scenes(_META, [bad]) if s == "error"]
    assert len(errs) == 1 and "exit 'nope'" in errs[0] and "built ids" in errs[0], errs
    good = {**_GRAPH, "exit": ["axes", "plot.1"]}
    assert not [m for s, m in sizecheck.check_scenes(_META, [good]) if s == "error"]


def test_sizecheck_defaults_the_deck_to_the_scenes_it_checks():
    errs = [m for s, m in sizecheck.check_scenes(_META, list(_DECK)) if s == "error"]
    assert errs == [], errs


# -- scene.py: opening frame + tail ------------------------------------------------------------------

def test_stage_adds_statics_and_rewinds_pre_play_blocks():
    calls = []
    blocks = [Block("s", "STATIC", static=True),
              Block("d", "DYN", static=False),
              Block("p", "PRE", static=False, pre_play=lambda m: calls.append(m))]
    fake = _FakeScene()
    LessonScene._stage(fake, blocks)
    assert fake.added == ["STATIC", "PRE"], fake.added
    assert calls == ["PRE"], "pre_play runs on the mobject before it is added"


def test_tail_fades_exit_blocks_inside_the_hold():
    blocks = build_blocks({**_GRAPH, "exit": ["axes", "plot.1", "nope"]}, _ctx())
    by_id = {b.id: b for b in blocks}
    fake = _FakeScene({"exit": ["axes", "plot.1", "nope"]})
    LessonScene._tail(fake, "content", by_id)
    assert len(fake.played) == 1
    anims, kw = fake.played[0]
    assert len(anims) == 2 and all(isinstance(a, FadeOut) for a in anims), "unknown ids skipped"
    assert kw["run_time"] == EXIT_FADE_SECONDS
    assert fake.waited == [SCENE_TAIL_SECONDS - EXIT_FADE_SECONDS]
    assert abs(sum(fake.waited) + kw["run_time"] - SCENE_TAIL_SECONDS) < 1e-9, "clip length unchanged"


def test_tail_without_exit_is_the_plain_hold():
    fake = _FakeScene({})
    LessonScene._tail(fake, "content", {})
    assert fake.played == [] and fake.waited == [SCENE_TAIL_SECONDS]
    fake = _FakeScene({"exit": ["x"]})
    LessonScene._tail(fake, "divider", {"x": Block("x", "M")})
    assert fake.played == [], "exit is a content-scene field; other kinds ignore it"


def test_block_list_is_carried_as_one_group():
    """`block: [a, b]` -> one Block whose mobject groups a copy of each; the group flies as
    one, so the parts keep their relative layout (a figure the hook built as circle + frame +
    apex must not scatter into three corner copies)."""
    spec = {**_DER, "carry": [{**_DER["carry"][0], "block": ["plot.0", "plot.1"]}]}
    got = _b(build_blocks(spec, _ctx()), "carried.curve")
    assert len(got.mobject.submobjects) == 2, "one group holding one copy per listed block"
    src = build_blocks(_GRAPH, _ctx())
    got.pre_play(got.mobject)
    x0, x1, y0, y1 = _bbox(got.mobject)
    boxes = [_bbox(_b(src, bid).mobject) for bid in ("plot.0", "plot.1")]
    assert abs(x0 - min(b[0] for b in boxes)) < 1e-6 and abs(x1 - max(b[1] for b in boxes)) < 1e-6
    assert abs(y0 - min(b[2] for b in boxes)) < 1e-6 and abs(y1 - max(b[3] for b in boxes)) < 1e-6, \
        "rewound group covers exactly the union of the sources' boxes -- internal layout kept"
    bad = {**_DER, "carry": [{**_DER["carry"][0], "block": ["plot.0", "plot.9"]}]}
    try:
        build_blocks(bad, _ctx())
        assert False, "an unknown id inside the list must raise like a bare unknown id"
    except ValueError as e:
        assert "plot.9" in str(e) and "built ids" in str(e)


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] carry green")

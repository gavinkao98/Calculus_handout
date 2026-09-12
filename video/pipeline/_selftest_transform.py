"""Self-test: `anim: transform` derivation rows (the in-place rewrite primitive). Run from video/:
    python -m pipeline._selftest_transform

A row asking for `transform` morphs the PREVIOUS row's equation into its own instead of
fading a finished line in, and mutes the row it came from. The Block.anim becomes a
callable, so this pins the two things the rest of the pipeline reads off it:
  * `Block.anim_seconds` carries the nominal duration a callable cannot advertise, so
    make.py's short-beat warning still sees the reveal cost (it skips callables otherwise)
  * the row's GEOMETRY is untouched -- the frame sizecheck measures is the same either way

Zero behaviour change: a spec that does not say `anim: transform` builds exactly as before.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # derivation imports manim at module level -- bootstrap FIRST

from manim import MathTex

from pipeline.templates import build_blocks
from pipeline.timing import STOCK_ANIM_SECONDS, stock_animation_seconds

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}


def _spec(*, transform: bool):
    def step(math, reason, i):
        st = {"math": math, "reason": reason}
        if transform and i > 0:
            st["anim"] = "transform"
        return st
    return {
        "id": "der", "kind": "content", "template": "derivation", "accent": "definition",
        "title": "A Derivation",
        "say": "One. {show step.0} Two. {show step.1} Three. {show result} Four.",
        "steps": [step(r"\sin(x+h)-\sin x = 2\cos\!\left(x+\frac h2\right)\sin\frac h2",
                       "sum-to-product", 0),
                  step(r"\frac{\sin(x+h)-\sin x}{h} = \cos\!\left(x+\frac h2\right)"
                       r"\cdot\frac{\sin(h/2)}{h/2}", "divide", 1)],
        "result": {"math": r"\cos\!\left(x+\frac h2\right)\to\cos x", "reason": "continuity",
                   **({"anim": "transform"} if transform else {})},
    }


def _blocks(*, transform):
    return build_blocks(_spec(transform=transform), {"ground": "dark", "meta": _META})


def _b(blocks, bid):
    return next(x for x in blocks if x.id == bid)


# -- default path unchanged --------------------------------------------------

def test_default_rows_keep_their_stock_anim():
    blocks = _blocks(transform=False)
    assert _b(blocks, "step.0").anim == "write"
    assert _b(blocks, "step.1").anim == "write"
    assert _b(blocks, "result").anim == "write_glow"
    assert all(_b(blocks, i).anim_seconds is None for i in ("step.0", "step.1", "result"))


# -- transform rows ----------------------------------------------------------

def test_transform_row_becomes_a_callable():
    blocks = _blocks(transform=True)
    assert _b(blocks, "step.0").anim == "write", "the first row has nothing to morph FROM"
    assert callable(_b(blocks, "step.1").anim)
    assert callable(_b(blocks, "result").anim)


def test_transform_row_advertises_its_nominal_seconds():
    blocks = _blocks(transform=True)
    want = STOCK_ANIM_SECONDS["transform"]
    assert _b(blocks, "step.1").anim_seconds == want
    assert _b(blocks, "result").anim_seconds == want
    # a callable is opaque to the stock table -- anim_seconds is what make.py must read
    assert stock_animation_seconds(_b(blocks, "step.1").anim) is None


def test_transform_does_not_move_the_row():
    """Geometry parity: transform is a reveal style, not a layout change, so the terminal
    frame (what sizecheck measures) is identical."""
    plain, trans = _blocks(transform=False), _blocks(transform=True)
    for bid in ("step.0", "step.1", "result"):
        a, b = _b(plain, bid).mobject, _b(trans, bid).mobject
        assert abs(a.get_left()[0] - b.get_left()[0]) < 1e-6, bid
        assert abs(a.get_center()[1] - b.get_center()[1]) < 1e-6, bid
        assert abs(a.width - b.width) < 1e-6 and abs(a.height - b.height) < 1e-6, bid


def test_transform_row_is_still_dynamic_and_keeps_its_id():
    blocks = _blocks(transform=True)
    assert _b(blocks, "step.1").static is False
    assert {b.id for b in blocks} == {b.id for b in _blocks(transform=False)}


def test_back_compat_lines_accept_transform_too():
    spec = {"id": "der2", "kind": "content", "template": "derivation", "accent": "definition",
            "title": "T", "say": "A. {show line.0} B. {show line.1} C.",
            "lines": ["a = b", {"tex": "b = c", "anim": "transform"}]}
    blocks = build_blocks(spec, {"ground": "dark", "meta": _META})
    assert callable(_b(blocks, "line.1").anim)
    assert _b(blocks, "line.1").anim_seconds == STOCK_ANIM_SECONDS["transform"]


# -- the animation itself plays and reports its cost -------------------------

class _FakeScene:
    """Records what a callable anim asks for, without running manim's renderer."""
    def __init__(self):
        self.added, self.played = [], []

    def add(self, *mobs):
        self.added.extend(mobs)

    def play(self, *anims, **kw):
        self.played.append((anims, kw))


def test_transform_callable_plays_one_timed_animation_and_returns_its_seconds():
    blocks = _blocks(transform=True)
    block = _b(blocks, "step.1")
    scene = _FakeScene()
    secs = block.anim(scene, block.mobject, "dark")
    assert secs == STOCK_ANIM_SECONDS["transform"]
    assert len(scene.played) == 1
    anims, kw = scene.played[0]
    assert kw["run_time"] == secs
    assert scene.added, "the ghost of the previous row must be put on screen to morph FROM"
    assert isinstance(scene.added[0], MathTex)


def test_transform_dims_the_whole_previous_row_not_just_its_equation():
    """A spent row's rail annotation must dim WITH its equation -- dimming only the equation
    left the annotation brighter than what it annotates (visual-frame audit, 2026-09-12)."""
    blocks = _blocks(transform=True)
    prev_row = _b(blocks, "step.0").mobject          # equation + dotted leader + reason
    assert len(prev_row.submobjects) >= 2, "the fixture row must carry a reason rail"
    block = _b(blocks, "step.1")
    scene = _FakeScene()
    block.anim(scene, block.mobject, "dark")
    dim = [a for a in scene.played[0][0] if getattr(a, "mobject", None) is prev_row]
    assert dim, "the dim must target the whole previous ROW group"
    eq = next(m for m in prev_row.submobjects if isinstance(m, MathTex))
    assert not [a for a in scene.played[0][0] if getattr(a, "mobject", None) is eq], \
        "dimming the bare equation would leave its rail annotation at full ink"


def test_row_color_role_overrides_the_scene_accent():
    """Motion primitive 5 (跨場延續) in its cheapest form: a row can carry the colour the
    figure that motivated it used, so the algebra visibly belongs to the picture. Without
    it a step is always `primary` ink and a result is always the scene accent -- which is
    what made the rewatch review say '三個區域用藍/橘/綠標好了，到不等式鏈全變回白字'."""
    from pipeline.visuals import theme as T
    spec = _spec(transform=False)
    spec["steps"][1]["color_role"] = "practice"
    spec["result"]["color_role"] = "caution"
    blocks = build_blocks(spec, {"ground": "dark", "meta": _META})

    plain = _colors(_b(blocks, "step.0").mobject)
    tinted = _colors(_b(blocks, "step.1").mobject)
    assert T.color("dark", "primary").lower() in plain, plain
    assert T.color("dark", "practice").lower() in tinted, tinted
    assert T.color("dark", "practice").lower() not in plain, "colour leaked to a plain row"

    result = _colors(_b(blocks, "result").mobject)
    assert T.color("dark", "caution").lower() in result, result

    # and the default is untouched: no color_role -> the scene accent, as before
    dflt = _colors(_b(build_blocks(_spec(transform=False), {"ground": "dark", "meta": _META}),
                      "result").mobject)
    assert T.color("dark", "concept").lower() in dflt, dflt


def _colors(mob) -> "set[str]":
    """Every MathTex colour in a row group. A row holds the equation AND its reason rail
    (and a result row nests the equation one level deeper), so membership is the honest
    assertion -- picking "the first MathTex" would silently read the rail."""
    from manim import MathTex
    out: set[str] = set()

    def walk(m):
        if isinstance(m, MathTex):
            out.add(str(m.get_color()).lower())
        for s in getattr(m, "submobjects", []):
            walk(s)
    walk(mob)
    assert out, "no MathTex found in row mobject"
    return out


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

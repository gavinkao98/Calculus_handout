"""Self-test: theorem_proof `proof[]` dict rows + `anim: transform` (rollout T1-3). Run from video/:
    python -m pipeline._selftest_proof_transform

A proof row may be `{tex, anim: transform, frame}` instead of a plain string; the transform
row morphs the PREVIOUS proof row's MathTex into its own (derivation._transform_anim), the
textbook "rewrite the line above" move that theorem_proof had no entrance for. This pins:
  * dict rows build, and a plain string list builds exactly as before (zero behaviour change)
  * proof.1's anim is a callable advertising TRANSFORM_SECONDS (+FRAME_SECONDS with `frame`)
    through Block.anim_seconds AND timing.stock_animation_seconds (T1-2 `fixed_seconds`)
  * the built geometry is the string list's, token for token
  * proof.0 keeps its stock reveal (nothing to morph from), folded PROOF label included
  * a transform row also listed in `paced:` keeps the transform (a proof row has no rail)
  * schema: cancel is derivation-only; `frame` needs `anim: transform`; `tex` is required
  * lint sees a dict row's tex the way it sees a string row
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # theorem_proof imports manim at module level -- bootstrap FIRST

from manim import FadeIn, MathTex

from pipeline import lint, schema
from pipeline.templates import build_blocks
from pipeline.templates import derivation
from pipeline.templates import theorem_proof as TP
from pipeline.timing import STOCK_ANIM_SECONDS, stock_animation_seconds

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}
_TEX = [r"$\sin(x+h)-\sin x = 2\cos(x+h/2)\sin(h/2)$",
        r"$\frac{\sin(x+h)-\sin x}{h} = \cos(x+h/2)\cdot\frac{\sin(h/2)}{h/2}$",
        r"$\cos(x+h/2)\to\cos x$"]
_SAY = "One. {show proof.0} Two. {show proof.1} Three. {show proof.2} Four. {show qed} Five."
_ROW_IDS = ("proof.0", "proof.1", "proof.2", "qed")


def _spec(proof, say=_SAY, **extra):
    return {"id": "thm", "kind": "content", "template": "theorem_proof", "accent": "theorem",
            "title": "A Theorem", "statement": "Every $f$ is nice.", "proof": proof,
            "qed": "$a = c$", "say": say, **extra}


def _dict_rows(*, frame=False):
    return [_TEX[0], {"tex": _TEX[1], "anim": "transform"},
            {"tex": _TEX[2], "anim": "transform", **({"frame": True} if frame else {})}]


def _blocks(spec):
    return build_blocks(spec, {"ground": "dark", "meta": _META})


def _b(blocks, bid):
    return next(x for x in blocks if x.id == bid)


# -- the helper every proof[] reader goes through -------------------------------

def test_proof_texts_reads_strings_and_dicts_alike():
    assert TP.proof_texts(_spec(_dict_rows())) == _TEX
    assert TP.proof_texts(_spec(list(_TEX))) == _TEX
    assert TP.proof_texts({}) == []


# -- zero behaviour change for a string list -------------------------------------

def test_string_rows_keep_their_stock_reveal():
    blocks = _blocks(_spec(list(_TEX)))
    assert _b(blocks, "proof.1").anim == "fade" and _b(blocks, "proof.2").anim == "fade"
    assert all(_b(blocks, i).anim_seconds is None for i in ("proof.1", "proof.2", "qed"))
    assert {b.id for b in blocks} == {b.id for b in _blocks(_spec(_dict_rows()))}


# -- transform rows ---------------------------------------------------------------

def test_transform_rows_become_callables_that_advertise_their_seconds():
    blocks = _blocks(_spec(_dict_rows()))
    want = STOCK_ANIM_SECONDS["transform"]
    for bid in ("proof.1", "proof.2"):
        blk = _b(blocks, bid)
        assert callable(blk.anim), bid
        assert blk.anim_seconds == want, bid
        # T1-2: the callable itself tells the stillness advisory its fixed length
        assert stock_animation_seconds(blk.anim) == want, bid
        assert blk.static is False


def test_frame_adds_its_seconds():
    blk = _b(_blocks(_spec(_dict_rows(frame=True))), "proof.2")
    want = STOCK_ANIM_SECONDS["transform"] + derivation.FRAME_SECONDS
    assert blk.anim_seconds == want
    assert stock_animation_seconds(blk.anim) == want
    assert _b(_blocks(_spec(_dict_rows(frame=True))), "proof.1").anim_seconds == STOCK_ANIM_SECONDS["transform"]


def _tokens(mob):
    return [(tuple(round(float(v), 6) for v in m.get_center()), round(float(m.width), 6))
            for m in mob.family_members_with_points()]


def test_geometry_matches_the_string_list_token_for_token():
    """transform is a reveal style, not a layout change: the frame sizecheck measures is the
    string list's, glyph for glyph (frame: true included -- the rectangle is play-time only)."""
    plain, trans = _blocks(_spec(list(_TEX))), _blocks(_spec(_dict_rows(frame=True)))
    for bid in _ROW_IDS:
        a, b = _b(plain, bid).mobject, _b(trans, bid).mobject
        assert _tokens(a) == _tokens(b), bid


def test_the_first_row_keeps_its_stock_reveal():
    rows = [{"tex": _TEX[0], "anim": "transform"}, _TEX[1]]
    # no {show proof.0}: the label stays static and proof.0 is the plain stock fade
    blocks = _blocks(_spec(rows, say="One. {show proof.1} Two."))
    assert _b(blocks, "proof.0").anim == "fade" and _b(blocks, "proof.0").anim_seconds is None
    # with the marker the PROOF eyebrow rides in on proof.0 as before, not a morph
    blk = _b(_blocks(_spec(rows)), "proof.0")
    assert callable(blk.anim) and blk.anim_seconds == TP._LABEL_FADE_SECONDS


def test_a_paced_transform_row_keeps_the_transform():
    """`paced:` upgrades stock reveals only; a proof row has no rail to walk after the morph."""
    blk = _b(_blocks(_spec(_dict_rows(), paced=["proof.1"])), "proof.1")
    assert callable(blk.anim) and blk.anim_seconds == STOCK_ANIM_SECONDS["transform"]


# -- the animation itself -------------------------------------------------------------

class _FakeScene:
    """Records what a callable anim asks for, without running manim's renderer."""
    def __init__(self, beat_seconds=None):
        self.beat_seconds = beat_seconds
        self.added, self.played, self.waits = [], [], []

    def add(self, *mobs):
        self.added.extend(mobs)

    def play(self, *anims, **kw):
        self.played.append((anims, kw))

    def wait(self, seconds):
        self.waits.append(float(seconds))


def test_transform_plays_one_morph_with_no_rail_even_on_a_long_beat():
    blocks = _blocks(_spec(_dict_rows(), paced=["proof.1"]))
    block = _b(blocks, "proof.1")
    for scene in (_FakeScene(), _FakeScene(beat_seconds=16.0)):
        secs = block.anim(scene, block.mobject, "dark")
        assert secs == STOCK_ANIM_SECONDS["transform"]
        assert len(scene.played) == 1 and scene.waits == [], (scene.played, scene.waits)
        anims, kw = scene.played[0]
        assert kw["run_time"] == secs
        assert not [a for a in anims if isinstance(a, FadeIn)], \
            "a bare MathTex row has no rail; its glyphs must not be faded in beside the morph"
        assert isinstance(scene.added[0], MathTex), "the ghost of the previous row morphs FROM"


# -- schema -------------------------------------------------------------------------------

def _errs(proof):
    return [m for sev, m in schema._derivation_issues("thm", _spec(proof)) if sev == "error"]


def test_schema_accepts_well_formed_rows():
    assert _errs(_dict_rows(frame=True)) == []
    assert _errs(list(_TEX)) == []


def test_schema_rejects_cancel_as_derivation_only():
    errs = _errs([_TEX[0], {"tex": _TEX[1], "anim": "cancel"}])
    assert len(errs) == 1 and "derivation-only" in errs[0], errs
    errs = _errs([_TEX[0], {"tex": _TEX[1], "anim": "transform", "cancel": [0]}])
    assert len(errs) == 1 and "derivation-only" in errs[0], errs


def test_schema_rejects_frame_without_transform():
    errs = _errs([_TEX[0], {"tex": _TEX[1], "frame": True}])
    assert len(errs) == 1 and "frame" in errs[0], errs


def test_schema_rejects_a_row_without_tex():
    errs = _errs([_TEX[0], {"anim": "transform"}])
    assert len(errs) == 1 and "tex" in errs[0], errs


# -- lint transparency ---------------------------------------------------------------------

def test_lint_reads_a_dict_row_like_a_string_row():
    strings = lint._prose_strings({"scenes": [_spec(_dict_rows())]})
    assert ("thm.proof[1]", _TEX[1]) in strings, strings
    assert strings == lint._prose_strings({"scenes": [_spec(list(_TEX))]})


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

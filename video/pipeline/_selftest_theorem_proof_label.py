"""Self-test: theorem_proof's PROOF eyebrow is its OWN Block, revealed on proof.0's beat.

Run from video/:  python -m pipeline._selftest_theorem_proof_label

The defect this locks (2026-09-14). The eyebrow used to be folded into proof.0's reveal
ANIMATION (`theorem_proof._reveal_with_label`), so the word PROOF only ever reached the
screen if nothing replaced that animation. `animations/ch03_trig_derivatives_hooks.py`'s
`continuity_template` does exactly that -- `ids["proof.0"].anim = lambda scene, mob, _g:
pacing.paced_write(scene, mob)` -- and §3.1 scene 09 therefore rendered its whole proof
with no PROOF card at all. Any hook that REPLACES (rather than wraps) proof.0's anim loses
it the same way, so the fix belongs in the template, not in one hook.

The eyebrow is now a Block of its own carrying `Block.reveal_with = "proof.0"`: the player
reveals it on the same beat as the row it labels, whatever proof.0's anim happens to be.

Not the worked_example route (its `notes_label` rides INSIDE note.0's mobject, D11), for
two reasons specific to this template:
  * §3.1's hooks address proof.0's mobject by position -- `_mark_factors` reads
    `ids["proof.0"].mobject.submobjects[1]` as the row's half-sum `{{...}}` segment, and
    `cosine_identity_draft` runs `derivation._eq_core` over it -- so wrapping the row in a
    VGroup with the eyebrow would silently mis-address those segments.
  * the eyebrow and the chain are NOT adjacent here: `reaches_rail` drops the chain below
    the statement card while the eyebrow stays at the top of the column, so a label-to-row
    VGroup hands the layout gates a box with a hollow middle (the `_demo_tall_rows`
    warning the old fold-into-the-anim comment recorded). worked_example's notes heading
    sits 0.16u above its note inside the rail's own bucket, so neither applies there.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # templates import manim at module level -- bootstrap FIRST (repo rule)

from pipeline import pacing                       # noqa: E402
from pipeline.scene import LessonScene            # noqa: E402
from pipeline.templates import build_blocks       # noqa: E402

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}

_THM = {
    "id": "thm", "kind": "content", "template": "theorem_proof", "accent": "theorem",
    "title": "A Theorem",
    "statement": "Every $f$ is nice.",
    "proof": ["$a = b$", "$b = c$"],
    "qed": "$a = c$",
}
_SAY = "The claim. {show proof.0} The first step. {show proof.1} The second step."


def _spec(say: str, **extra) -> dict:
    return {**_THM, **extra, "say": say}


def _build(say: str, **extra):
    return build_blocks(_spec(say, **extra), {"ground": "dark", "meta": _META})


def _block(blocks, bid: str):
    return next(b for b in blocks if b.id == bid)


def _ids(blocks):
    return {b.id for b in blocks}


class _Player:
    """The bits of LessonScene `_play_content` touches, recording plays and beat ends.

    No renderer, so `timing.elapsed` returns None and every reveal reports its nominal
    seconds -- the same fake-scene contract `_selftest_focus_and_pacing` uses.
    """

    def __init__(self, spec: dict):
        self.spec = spec
        self.beat_durations = None
        self.beat_seconds = None
        self.beat_reserved_seconds = 0.0
        self.events: list = []

    def play(self, *anims, **kwargs):
        self.events.append(("play", [getattr(a, "mobject", None) for a in anims]))

    def wait(self, seconds=0.0):
        self.events.append(("wait", seconds))

    def add(self, *mobs):
        pass

    def remove(self, *mobs):
        pass


def _beats_played(spec: dict, blocks) -> list:
    """[[mobject, ...], ...] -- the mobjects each beat played, in beat order.

    `_play_content` closes every beat with exactly one `wait`, so the waits are the beat
    boundaries; whatever follows the last one is the end-of-scene sweep-up.
    """
    player = _Player(spec)
    LessonScene._play_content(player, blocks, {b.id: b for b in blocks}, "dark")
    beats, current = [], []
    for kind, payload in player.events:
        if kind == "play":
            current += [m for m in payload if m is not None]
        else:
            beats.append(current)
            current = []
    beats.append(current)
    return beats


# -- (1) the eyebrow is a Block of its own, on proof.0's beat ----------------------

def test_proof_label_is_an_independent_block():
    blocks = _build(_SAY)
    assert "proof_label" in _ids(blocks), \
        "the PROOF eyebrow must be a Block of its own, not folded into proof.0's anim"
    label = _block(blocks, "proof_label")
    assert label.static is False, "it must enter with the proof, not sit in the opening frame"
    assert label.reveal_with == "proof.0", \
        "it must declare the beat it rides on (Block.reveal_with), not carry a {show} marker"


def test_proof_label_is_not_hidden_inside_proof0():
    blocks = _build(_SAY)
    label = _block(blocks, "proof_label").mobject
    row = _block(blocks, "proof.0")
    assert label not in row.mobject.family_members_with_points(), \
        "the eyebrow must not be a submobject of proof.0 (hooks address that mobject by position)"
    assert not callable(row.anim), \
        "proof.0 keeps its stock reveal -- the eyebrow no longer makes it a callable"


def test_proof0_geometry_stays_the_bare_row():
    """A VGroup spanning eyebrow-to-row would hand the layout gates a box with a hollow
    middle, and the overlap / capacity guards read that empty span as content."""
    revealed = _block(_build(_SAY), "proof.0").mobject
    plain = _block(_build("Words only, no markers."), "proof.0").mobject
    assert abs(revealed.get_left()[0] - plain.get_left()[0]) < 1e-6
    assert abs(revealed.get_center()[1] - plain.get_center()[1]) < 1e-6
    assert abs(revealed.height - plain.height) < 1e-6
    assert abs(revealed.width - plain.width) < 1e-6


def test_label_and_row_land_on_the_same_beat():
    spec = _spec(_SAY)
    blocks = build_blocks(spec, {"ground": "dark", "meta": _META})
    beats = _beats_played(spec, blocks)
    label = _block(blocks, "proof_label").mobject
    row = _block(blocks, "proof.0").mobject
    hit = [i for i, mobs in enumerate(beats) if row in mobs]
    assert len(hit) == 1, f"proof.0 must be revealed exactly once (beats {hit})"
    assert label in beats[hit[0]], (
        "the eyebrow must land on proof.0's beat, not on "
        f"{[i for i, mobs in enumerate(beats) if label in mobs]}")


# -- (2) a hook that REPLACES proof.0's anim still gets the eyebrow ----------------

def test_label_survives_a_hook_replacing_proof0_anim():
    """`continuity_template` (ch03 scene 09) verbatim: the row's anim is swapped for a
    paced write. Under the old fold the eyebrow lived in the anim that was thrown away."""
    spec = _spec(_SAY)
    blocks = build_blocks(spec, {"ground": "dark", "meta": _META})
    by_id = {b.id: b for b in blocks}
    by_id["proof.0"].anim = lambda scene, mob, _g: pacing.paced_write(scene, mob)

    beats = _beats_played(spec, blocks)
    label, row = by_id["proof_label"].mobject, by_id["proof.0"].mobject
    hit = [i for i, mobs in enumerate(beats) if row in mobs]
    assert len(hit) == 1 and label in beats[hit[0]], \
        "a hook replacing proof.0's anim must not be able to drop the PROOF eyebrow"


def test_paced_proof0_now_takes_the_stock_paced_reveal():
    """`paced: [proof.0]` used to be the one id the primitive could not reach on its own,
    because the eyebrow fold made proof.0's anim a callable. With the fold gone it is an
    ordinary stock reveal and `pacing.apply` upgrades it like any other row."""
    assert _block(_build(_SAY, paced=["proof.0"]), "proof.0").anim is pacing.paced_reveal


# -- (3) no marker: unchanged -- the eyebrow is part of the opening frame ----------

def test_label_static_without_the_marker():
    blocks = _build("Words only, no markers.")
    label = _block(blocks, "proof_label")
    assert label.static is True and label.anim == "fade"
    assert label.reveal_with is None
    assert _block(blocks, "proof.0").static is False


def test_statement_only_proposition_builds_no_label():
    """The aside path (statement, no proof) has no proof chain and so no eyebrow --
    unchanged by this work."""
    spec = {"id": "prop", "kind": "content", "template": "theorem_proof",
            "accent": "proposition", "title": "A Proposition",
            "statement": "Every $f$ is nice.",
            "aside": {"title": "Note", "body": "Only for nice $f$."},
            "say": "Words only."}
    assert "proof_label" not in _ids(build_blocks(spec, {"ground": "dark", "meta": _META}))


if __name__ == "__main__":
    import sys
    import traceback
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except Exception:
                fails += 1
                print(f"FAIL {name}")
                traceback.print_exc()
    sys.exit(1 if fails else 0)

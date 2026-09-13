"""Self-test: the two §3.1 beats round 21 fixed, pinned on the CANONICAL deck
(storyboards/ch03_trig_derivatives_mimo.yml), not on a fixture -- both defects were
authored in that deck and a fixture would let it regress unnoticed.

Run from video/:
    python -m pipeline._selftest_pairing_and_opening

What it pins:

  * scene 18 `slope_equals_height`, beat 7 ("...they match exactly -- the slope of sine
    is the height of cosine"): the reveal of `cos_dots` is THREE pairing moves, not one
    0.55 s fade. Each move draws its own dashed connector and then pulses the tangent and
    the read-off point TOGETHER -- the equals sign the scene title promises, performed.
    Before this round the beat was a single fade followed by 9.8 s of frozen picture.
  * the R2 colour prescription (recolour the three pairs by x) is NOT in: the three
    tangents keep one colour and the three read-off points keep another, per the user's
    2026-09-13 ruling (琥珀=sin / 青=cos / 綠=結論, SPEC-motion-language 規則 5).
  * scene 14 `companion_limit`, beat 1 (+1.0 -> +9.5 s): the opening beat reveals NOTHING
    (`parse_say` gives it `reveal=None`), so no reveal-driven primitive can reach it. The
    statement line is therefore on screen from t=0 carrying a time-based updater that
    writes it out segment by segment while that sentence is read, and the next beat's
    reveal finishes and freezes it.
  * ZERO TTS: every beat's narration text hash in both scenes is unchanged, so
    `make.py --reuse-audio`'s manifest-freshness gate stays fresh and nothing is
    re-synthesized. This is the round's hard budget constraint, pinned as a number.
"""
from pathlib import Path

from pipeline import _bootstrap

_bootstrap.bootstrap()   # the hook module imports manim at module level -- bootstrap FIRST

import yaml
from manim import Create, Indicate

from pipeline import timing as TM
from pipeline.narration import parse_say
from pipeline.templates import build_blocks
from pipeline.visuals import theme as T

_DECK = Path(__file__).resolve().parents[1] / "storyboards" / "ch03_trig_derivatives_mimo.yml"
_META = {"id": "ch03_trig_derivatives_mimo", "chapter": "Chapter 3", "section": "3.1",
         "title": "Derivatives of Sine and Cosine", "theme": "midnight"}

# The narration is LOCKED and this round's budget is zero TTS: every beat's text hash must
# come out of the deck unchanged (captured 2026-09-13, before any edit in this round).
_TEXT_HASHES = {
    "companion_limit": ["f0f6966aff91e9ff", "3b62eb6c619ba9d4", "efa81775e0ebc20c",
                        "8416940c30905241", "42863785835948ee"],
    "slope_equals_height": ["94478d424cbcafb8", "af63d2d7d9a6a615", "9afbf091c443c8fc",
                            "3e818695bb34fbcc", "c7bb586eda982b73", "180f80b8c25ffb64",
                            "79cbb2ce76d572f1"],
}


def _deck():
    return yaml.safe_load(_DECK.read_text(encoding="utf-8"))


def _scene(sid):
    for s in _deck()["scenes"]:
        if s.get("id") == sid:
            return s
    raise AssertionError(f"{sid} is not in {_DECK.name}")


def _blocks(sid):
    spec = _scene(sid)
    meta = dict(_META)
    meta.update({k: v for k, v in (_deck().get("meta") or {}).items()})
    return spec, build_blocks(spec, {"ground": "dark", "meta": meta, "scenes_by_id": None})


def _b(blocks, bid):
    return next(x for x in blocks if x.id == bid)


def _writer(blocks):
    """The block that animates during the reveal-less opening beat: on the opening frame
    (no reveal can reach that beat) and carrying a time-based updater."""
    live = [b for b in blocks if b.static and b.mobject.has_time_based_updater()]
    assert live, ("no block animates during the reveal-less opening beat; "
                  f"static blocks = {[b.id for b in blocks if b.static]}")
    return live[0]


class FakeScene:
    """Records the animations it was asked to play instead of rendering. `beat_seconds`
    and `beat_reserved_seconds` are what the real LessonScene sets before each beat."""

    def __init__(self, beat_seconds=None, beat_reserved_seconds=0.0):
        self.beat_seconds = beat_seconds
        self.beat_reserved_seconds = beat_reserved_seconds
        self.plays = []          # one (run_time, [animation, ...]) per play
        self.waits = []

    def play(self, *anims, **kw):
        self.plays.append((float(kw.get("run_time") or 0.0), list(anims)))

    def wait(self, seconds=1.0):
        self.waits.append(float(seconds))

    def add(self, *mobs):
        pass


def _ink(part):
    """How opaque a segment's GLYPHS are. Not the segment's own `fill_opacity`: a VGroup
    that carries no points of its own defaults to 0 there, so the container attribute says
    nothing about whether the reader can see the segment."""
    return max((m.get_fill_opacity() for m in part.family_members_with_points()), default=0.0)


# -- scene 18: the pairing action ---------------------------------------------

_SPEC18, _B18 = None, None


def _slope():
    global _SPEC18, _B18
    if _B18 is None:
        _SPEC18, _B18 = _blocks("slope_equals_height")
    return _SPEC18, _B18


def test_cos_dots_reveals_as_three_paired_pulses_not_one_fade():
    """The finding: the title says Slope Equals Height and nothing ever drew the equals
    sign. Three pulses, each pairing ONE tangent with ONE read-off point, is the fix."""
    _, blocks = _slope()
    block = _b(blocks, "cos_dots")
    scene = FakeScene(beat_seconds=11.2, beat_reserved_seconds=0.8)
    block.anim(scene, block.mobject, "dark")
    pulses = [p for p in scene.plays if any(isinstance(a, Indicate) for a in p[1])]
    assert len(pulses) >= 3, f"want >= 3 pairing pulses, got {len(pulses)}"
    for i, p in enumerate(pulses[:3]):
        flashed = [a for a in p[1] if isinstance(a, Indicate)]
        assert len(flashed) >= 2, (
            f"pulse {i} flashes {len(flashed)} object(s); a PAIRING must move the tangent "
            "and the read-off point in the same play, or nothing says they are equal")


def test_each_pairing_draws_its_own_connector_before_it_pulses():
    """The dashed line down x=x0 is what makes 'slope here = height there' literal; it has
    to arrive with its pair, not all three at once ahead of the reading."""
    _, blocks = _slope()
    block = _b(blocks, "cos_dots")
    scene = FakeScene(beat_seconds=11.2, beat_reserved_seconds=0.8)
    block.anim(scene, block.mobject, "dark")
    seq = ["create" if any(isinstance(a, Create) for a in p[1])
           else "pulse" if any(isinstance(a, Indicate) for a in p[1])
           else "other" for p in scene.plays]
    for i in range(3):
        assert "create" in seq, f"pairing {i}: no connector drawn ({seq})"
        cut = seq.index("create")
        rest = seq[cut + 1:]
        assert "pulse" in rest, f"pairing {i}: connector drawn but never pulsed ({seq})"
        seq = rest[rest.index("pulse") + 1:]


def test_the_pairing_fits_inside_its_beat_and_leaves_room_for_the_focus_flash():
    """beat 7 is 11.2 s and its `focus[].indicate` costs 0.8 s AFTER this reveal; the
    three pairings must fit in what `timing.beat_run_time` leaves, so the scene cannot
    run long (the [sync] hard gate is 2 frames)."""
    _, blocks = _slope()
    block = _b(blocks, "cos_dots")
    scene = FakeScene(beat_seconds=11.2, beat_reserved_seconds=0.8)
    spent = block.anim(scene, block.mobject, "dark")
    budget = TM.beat_run_time(scene, 3.6)
    assert 3.0 <= spent <= budget, f"spent {spent:.2f}s, budget {budget:.2f}s"


def test_a_short_beat_does_not_overrun():
    _, blocks = _slope()
    block = _b(blocks, "cos_dots")
    scene = FakeScene(beat_seconds=2.5, beat_reserved_seconds=0.8)
    spent = block.anim(scene, block.mobject, "dark")
    assert spent <= TM.beat_run_time(scene, 3.6) + 1e-6, f"overran a 2.5 s beat by {spent:.2f}s"


def test_the_declined_r2_recolour_is_not_applied():
    """R2 also proposed dropping the green/blue split for a per-x three-colour scheme.
    Declined 2026-09-13: it breaks this deck's semantic colour axis (SPEC 規則 5 / V10).
    So all three tangents stay ONE colour and all three read-off dots stay ONE colour."""
    _, blocks = _slope()
    green = T.color("dark", "success")
    blue = T.color("dark", "secondary")
    for bid in ("tan_0", "tan_halfpi", "tan_pi"):
        seg = _b(blocks, bid).mobject[0]
        assert seg.get_color().to_hex().lower() == green.lower(), (
            f"{bid} tangent is {seg.get_color().to_hex()}, want the one success green {green}")
    dots = _b(blocks, "cos_dots").mobject
    hexes = {d[1].get_color().to_hex().lower() for d in dots}
    assert hexes == {blue.lower()}, f"read-off dots wear {hexes}, want one cosine blue {blue}"


# -- scene 14: the reveal-less opening beat ------------------------------------

def test_the_opening_beat_reveals_nothing_so_only_a_hook_can_reach_it():
    """Pins WHY this fix looks the way it does: `{show scaffold.motive}` is the first
    marker, so beat 1 has `reveal=None` and no reveal-driven primitive (`paced:`,
    `pauses:`, a block anim) can attach to it."""
    spec = _scene("companion_limit")
    beats = parse_say(spec["say"])
    assert beats[0].reveal is None, "beat 1 gained a reveal -- a marker was moved (re-TTS!)"
    assert beats[1].reveal == "scaffold.motive"


def test_the_opening_beat_is_not_zero_motion():
    """Something must GROW during those 8.5 s. It is on screen from t=0 (the beat has no
    reveal to hang on) and carries a time-based updater, which is what makes manim render
    the wait frame by frame instead of freezing one frame."""
    _, blocks = _blocks("companion_limit")
    _writer(blocks)


def test_the_opening_write_starts_hidden_walks_its_parts_and_ends_whole():
    """Segment by segment while the sentence is read, and fully opaque when it is done --
    the final frame the visual gates read must be the un-animated one."""
    _, blocks = _blocks("companion_limit")
    group = _writer(blocks).mobject
    parts = list(group.submobjects)
    assert len(parts) >= 2, f"the opening line has {len(parts)} part(s); nothing to walk"
    assert max(_ink(p) for p in parts) < 0.05, "the line is not hidden at t=0"

    seen = []
    for _ in range(600):                      # 10 s at 60 fps
        group.update(1 / 60)
        seen.append(sum(1 for p in parts if _ink(p) > 0.5))
    assert seen[0] == 0 and max(seen) == len(parts), f"walk never completed: {seen[:5]}..."
    assert 1 in seen, "parts arrived all at once, not one at a time"
    assert min(_ink(p) for p in parts) > 0.9, "the finished line is not fully opaque"
    assert not group.has_time_based_updater(), "the writer never froze itself"


def test_the_next_reveal_finishes_the_opening_write():
    """Closed loop: however long the real narration clip turns out to be, the beat-2
    reveal completes and freezes the line, so it can never be caught half-written."""
    _, blocks = _blocks("companion_limit")
    group = _writer(blocks).mobject
    motive = _b(blocks, "scaffold.motive")
    assert callable(motive.anim), "the motive reveal must carry the freeze"
    motive.anim(FakeScene(beat_seconds=4.8), motive.mobject, "dark")
    assert not group.has_time_based_updater(), "the motive reveal did not freeze the writer"
    assert min(_ink(p) for p in group.submobjects) > 0.9, "frozen half-written"


# -- the round's budget: zero TTS ---------------------------------------------

def test_no_narration_text_changed_in_either_scene():
    for sid, want in _TEXT_HASHES.items():
        got = [TM.text_hash(b.text) for b in parse_say(_scene(sid)["say"])]
        assert got == want, (
            f"{sid}: beat text hashes changed -> `make.py --reuse-audio` would judge the "
            f"manifest stale and re-synthesize (BILLED).\n  want {want}\n  got  {got}")


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in tests:
        try:
            fn()
            print(f"  [ok  ] {fn.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"  [FAIL] {fn.__name__}: {exc}")
    print(f"[_selftest_pairing_and_opening] {len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

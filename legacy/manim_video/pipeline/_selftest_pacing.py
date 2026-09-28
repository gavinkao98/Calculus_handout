"""Self-test: motion primitive 7 -- `paced:` (逐段隨讀).
Run from video/:
    python -m pipeline._selftest_pacing

Render-free: `pacing.apply` is list-of-Block surgery and `paced_reveal` is exercised
against a fake scene that records what it was asked to play. The schema validator is pure
dict logic.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # pacing builds real FadeIn animations -- bootstrap manim FIRST

from manim import Dot, VGroup

from pipeline import pacing as P
from pipeline import schema as S
from pipeline import timing as TM


class FakeBlock:
    def __init__(self, bid, mob, static=False, anim="fade"):
        self.id, self.mobject, self.static, self.anim = bid, mob, static, anim
        self.anim_seconds = None


class FakeScene:
    """Records plays and waits instead of rendering."""
    def __init__(self, beat_seconds=None):
        self.beat_seconds = beat_seconds
        self.plays, self.waits = [], []

    def play(self, *anims, **kw):
        self.plays.append(float(kw.get("run_time") or 0.0))

    def wait(self, seconds):
        self.waits.append(float(seconds))

    def add(self, *mobs):
        pass


def _mob(n):
    """A block mobject with *n* parts (real manim mobjects -- FadeIn typechecks them)."""
    return VGroup(*[Dot() for _ in range(n)])


# -- which parts a block is walked in ------------------------------------------

def test_a_paragraph_sized_block_is_walked_part_by_part():
    assert len(P.block_parts(_mob(3))) == 3


def test_a_single_line_is_atomic_not_typed_out_glyph_by_glyph():
    """One Tex line's submobjects are its glyphs; walking those would type it out."""
    mob = _mob(P.PART_LIMIT + 1)
    assert P.block_parts(mob) == [mob]
    lone = _mob(1)
    assert P.block_parts(lone) == [lone]
    bare = Dot()
    assert P.block_parts(bare) == [bare]


# -- the atomic branch: one formula row, written while it is read ---------------

def test_an_atomic_block_is_written_across_its_beat():
    scene = FakeScene(beat_seconds=16.0)
    spent = P.paced_reveal(scene, _mob(1), "dark")
    assert len(scene.plays) == 1 and scene.waits == [], (scene.plays, scene.waits)
    assert spent > 1.0, spent


def test_the_write_rate_is_capped_so_a_short_line_is_not_crawled():
    """A 2-glyph line on a 40 s beat must not be drawn for 40 s."""
    scene = FakeScene(beat_seconds=40.0)
    spent = P.paced_reveal(scene, _mob(1), "dark")
    assert spent < 12.0, spent


def test_the_write_never_outlasts_its_beat():
    scene = FakeScene(beat_seconds=3.0)
    spent = P.paced_reveal(scene, _mob(1), "dark")
    assert spent <= TM.beat_run_time(scene, 0.0) + 1e-6, spent


# -- the reveal itself ---------------------------------------------------------

def test_the_walk_spends_the_whole_beat():
    scene = FakeScene(beat_seconds=18.0)
    spent = P.paced_reveal(scene, _mob(3), "dark")
    assert abs(spent - TM.beat_run_time(scene, 0.0)) < 1e-6, spent
    assert len(scene.plays) == 3, scene.plays


def test_the_longest_still_inside_the_beat_is_the_beat_over_n():
    """The point of the primitive: an 18 s beat with 3 parts must never sit still for
    more than ~6 s, and the hold after the LAST part counts (n gaps, not n-1)."""
    scene = FakeScene(beat_seconds=18.0)
    P.paced_reveal(scene, _mob(3), "dark")
    assert len(scene.waits) == 3, scene.waits
    assert max(scene.waits) < 6.0, scene.waits


def test_a_two_part_block_does_not_strand_the_back_half():
    scene = FakeScene(beat_seconds=18.0)
    P.paced_reveal(scene, _mob(2), "dark")
    assert max(scene.waits) < 9.0, scene.waits


# -- chrome + content blocks (recap_cards.point.N, R2 must round 20) -----------

def _chrome_content_mob(n_parts):
    """A fake "chrome + content" block: a numeral (chrome) plus *n_parts* content lines,
    the way recap_cards builds a point row -- declared via _paced_parts/_paced_chrome so
    block_parts does not see the row's own [chrome, content] as the two parts to walk."""
    chrome = Dot()
    parts = [Dot() for _ in range(n_parts)]
    mob = VGroup(chrome, *parts)     # the row: top-level submobjects are [chrome, *parts]
    mob._paced_chrome = chrome
    mob._paced_parts = parts
    return mob, chrome, parts


def test_block_parts_reads_the_declared_split_not_the_top_level_submobjects():
    """Without the declaration, block_parts would see [chrome, *parts] (2..9 items) and
    walk the chrome as its own segment. With it, only the declared content parts walk."""
    mob, chrome, parts = _chrome_content_mob(2)
    assert P.block_parts(mob) == parts
    assert P.chrome_of(mob) is chrome


def test_chrome_rides_in_with_the_first_content_part_not_alone():
    """The bug (R2 ML4, round 20): a recap point's numeral revealed alone and held for
    half the beat before its text ever appeared. The chrome must be in the SAME play as
    the first content part, and get no play of its own."""
    mob, chrome, parts = _chrome_content_mob(2)
    scene = FakeScene(beat_seconds=18.0)
    P.paced_reveal(scene, mob, "dark")
    assert len(scene.plays) == 2, scene.plays          # one play per content part, no more
    assert scene.plays[0] == P.FADE_SECONDS            # first play is not slower/split


def test_a_single_content_part_with_chrome_stays_on_the_atomic_write_path():
    """One content line (no wrap): the declared split still has exactly 1 part, so this
    goes through paced_write, which draws the WHOLE mob (chrome included) together --
    already the correct "chrome with first content" behaviour, no extra wiring needed."""
    mob, chrome, parts = _chrome_content_mob(1)
    scene = FakeScene(beat_seconds=16.0)
    P.paced_reveal(scene, mob, "dark")
    assert len(scene.plays) == 1 and scene.waits == [], (scene.plays, scene.waits)


def test_a_plain_block_without_the_split_is_unaffected():
    """No _paced_parts/_paced_chrome declared: behaviour is byte-for-byte the pre-existing
    walk (chrome=None is a no-op) -- zero behaviour change for every other deck."""
    scene = FakeScene(beat_seconds=18.0)
    P.paced_reveal(scene, _mob(3), "dark")
    assert len(scene.plays) == 3, scene.plays


def test_off_beat_it_falls_back_to_plain_reveals():
    """No beat context (end-of-scene sweep-up, selftests): no invented hold."""
    scene = FakeScene(beat_seconds=None)
    spent = P.paced_reveal(scene, _mob(3), "dark")
    assert scene.waits == [] or max(scene.waits) < 0.01, scene.waits
    assert abs(spent - P.FADE_SECONDS * 3) < 1e-6, spent


# -- opt-in wiring -------------------------------------------------------------

def test_apply_rewires_only_the_named_dynamic_blocks():
    blocks = [FakeBlock("body", _mob(2)), FakeBlock("other", _mob(2))]
    P.apply({"paced": ["body"]}, blocks)
    assert blocks[0].anim is P.paced_reveal
    assert blocks[1].anim == "fade"
    assert blocks[0].anim_seconds == P.FADE_SECONDS * 2


def test_declared_seconds_are_the_floor_not_the_natural_length():
    """make.py's short-beat warning reads `anim_seconds` and tells the author scene.py
    will PAD the beat. An atomic write is capped at its beat by `write_seconds`, so it can
    never pad -- declaring its uncapped natural length made that warning fire on every
    long written row and name seconds that were never added."""
    blocks = [FakeBlock("row", _mob(1))]
    P.apply({"paced": ["row"]}, blocks)
    assert blocks[0].anim_seconds == TM.BEAT_PACED_MIN_SECONDS
    assert blocks[0].anim_seconds < P.write_seconds(blocks[0].mobject, float("inf"))


def test_apply_is_a_no_op_without_the_field():
    blocks = [FakeBlock("body", _mob(2))]
    P.apply({}, blocks)
    assert blocks[0].anim == "fade", "pacing must be opt-in -- no deck changes by default"


def test_apply_never_touches_a_static_block():
    blocks = [FakeBlock("body", _mob(2), static=True)]
    P.apply({"paced": ["body"]}, blocks)
    assert blocks[0].anim == "fade"


def test_apply_never_overwrites_a_choreography():
    """A callable anim is a hook or `anim: transform`; the generic walk must not eat it."""
    def hook(scene, mob, ground):
        return 1.0
    blocks = [FakeBlock("result", _mob(3), anim=hook)]
    P.apply({"paced": ["result"]}, blocks)
    assert blocks[0].anim is hook


# -- the gate ------------------------------------------------------------------

_SAY = "A. {show body} B. {show tail} C."


def test_schema_accepts_a_paced_id_the_narration_reveals():
    assert S._paced_issues("s", {"paced": ["body", "tail"]}, _SAY) == []


def test_schema_rejects_a_paced_id_nothing_reveals():
    out = S._paced_issues("s", {"paced": ["ghost"]}, _SAY)
    assert len(out) == 1 and out[0][0] == "error", out


def test_schema_rejects_a_malformed_or_duplicated_paced():
    assert S._paced_issues("s", {"paced": "body"}, _SAY)[0][0] == "error"
    assert S._paced_issues("s", {"paced": [""]}, _SAY)[0][0] == "error"
    assert any("duplicate" in m for _, m in S._paced_issues("s", {"paced": ["body", "body"]}, _SAY))


def test_schema_is_silent_without_the_field():
    assert S._paced_issues("s", {}, _SAY) == []


if __name__ == "__main__":
    test_a_paragraph_sized_block_is_walked_part_by_part()
    test_a_single_line_is_atomic_not_typed_out_glyph_by_glyph()
    test_an_atomic_block_is_written_across_its_beat()
    test_the_write_rate_is_capped_so_a_short_line_is_not_crawled()
    test_the_write_never_outlasts_its_beat()
    test_the_walk_spends_the_whole_beat()
    test_the_longest_still_inside_the_beat_is_the_beat_over_n()
    test_a_two_part_block_does_not_strand_the_back_half()
    test_block_parts_reads_the_declared_split_not_the_top_level_submobjects()
    test_chrome_rides_in_with_the_first_content_part_not_alone()
    test_a_single_content_part_with_chrome_stays_on_the_atomic_write_path()
    test_a_plain_block_without_the_split_is_unaffected()
    test_off_beat_it_falls_back_to_plain_reveals()
    test_apply_rewires_only_the_named_dynamic_blocks()
    test_declared_seconds_are_the_floor_not_the_natural_length()
    test_apply_is_a_no_op_without_the_field()
    test_apply_never_touches_a_static_block()
    test_apply_never_overwrites_a_choreography()
    test_schema_accepts_a_paced_id_the_narration_reveals()
    test_schema_rejects_a_paced_id_nothing_reveals()
    test_schema_rejects_a_malformed_or_duplicated_paced()
    test_schema_is_silent_without_the_field()
    print("OK pacing self-test")

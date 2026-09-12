"""Self-test: the scene-08 hook `chord_vs_arc` (the unit-circle figure that fills the
26-second opening beat of continuity_statement_sin_limit).
Run from video/:
    python -m pipeline._selftest_chord_vs_arc

What it pins:
  * the four reveal ids the LOCKED narration's {show ...} markers name actually exist,
    on the graph layer, all dynamic;
  * every stage animation is beat-paced (motion primitive 6) -- a 1-second reveal on a
    26-second beat is what this whole round exists to stop;
  * the statement card's reveal is REPLACED by the dock, so the zoomed-out figure has a
    beat to shrink back on. Without {show statement} there is no such beat, and the hook
    must then leave the figure at its home size instead of stranding it zoomed;
  * the built (terminal) geometry stays inside the frame's safe area and clear of the
    proof column -- the layout gates read the built state, and the final frame is the
    docked one.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # the hook module imports manim at module level -- bootstrap FIRST

from pipeline import timing as TM
from pipeline.templates import build_blocks
from pipeline.visuals import theme as T

_META = {"id": "_t", "chapter": "Chapter 3", "section": "3.1", "title": "T", "theme": "midnight"}
_IDS = ("circle", "nudge", "chord_arc", "straighten")
_OPENING = ("{show circle} One. {show nudge} Two. {show chord_arc} Three. "
            "{show straighten} Four. ")


def _spec(say):
    return {"id": "continuity_statement_sin_limit", "kind": "content",
            "template": "theorem_proof", "accent": "proposition",
            "hook": "animations.ch03_trig_derivatives_hooks:chord_vs_arc",
            "title": "Sine and Cosine Are Continuous",
            "scaffold": {"motive": r"The bound is the key to continuity."},
            "statement": r"At every point $x_0$, both $\sin x$ and $\cos x$ are continuous.",
            "proof": [r"$0\le|\sin\theta|\le|\theta|$ (chord $\le$ arc)",
                      r"$|\theta|\to 0$, squeeze $\Rightarrow\ \sin\theta\to 0$"],
            "qed": r"$\lim_{\theta\to 0}\sin\theta = 0$", "say": say}


def _blocks(say):
    return build_blocks(_spec(say), {"ground": "dark", "meta": _META})


def _b(blocks, bid):
    return next(x for x in blocks if x.id == bid)


_DOCKED = _blocks(_OPENING + "{show statement} Five. {show proof.0} Six. "
                             "{show proof.1} Seven. {show qed} Eight.")


class FakeScene:
    """Records what it was asked to play instead of rendering. `beat_seconds` is what the
    real LessonScene sets before each beat."""
    def __init__(self, beat_seconds=None):
        self.beat_seconds = beat_seconds
        self.run_times = []

    def play(self, *anims, **kw):
        self.run_times.append(float(kw.get("run_time") or 0.0))

    def add(self, *mobs):
        pass


# -- the reveal ids the narration names ---------------------------------------

def test_the_four_marker_targets_exist_as_dynamic_graph_blocks():
    for bid in _IDS:
        b = _b(_DOCKED, bid)
        assert not b.static, f"{bid} must be revealed by narration, not part of the frame"
        assert b.layer == "graph", f"{bid} layer={b.layer!r}, want graph"
        assert callable(b.anim), f"{bid} must carry a hook animation, got {b.anim!r}"


def test_the_stock_template_blocks_survive():
    have = {b.id for b in _DOCKED}
    for bid in ("title", "statement", "proof.0", "proof.1", "qed"):
        assert bid in have, f"the hook dropped {bid}"


# -- motion primitive 6: every stage lasts as long as its beat -----------------

def test_every_stage_animation_is_beat_paced():
    """Each stage, played on a 20-second beat, must spend most of that beat -- not a
    stock 0.5 s fade. (26.7 s of narration over a finished picture is the defect.)"""
    for bid in _IDS:
        block = _b(_DOCKED, bid)
        long_beat = FakeScene(beat_seconds=20.0)
        spent = block.anim(long_beat, block.mobject, "dark")
        assert spent > 12.0, f"{bid} spent only {spent:.1f}s of a 20 s beat"
        assert sum(long_beat.run_times) > 12.0, f"{bid} did not actually play for that long"


def test_stages_fall_back_to_their_own_length_outside_a_beat():
    """Off-beat (selftests, the end-of-scene sweep-up) beat_seconds is None and
    beat_run_time returns the fallback -- nothing may run for 20 s there."""
    for bid in _IDS:
        block = _blocks(_OPENING + "{show statement} Five.")
        b = _b(block, bid)
        spent = b.anim(FakeScene(beat_seconds=None), b.mobject, "dark")
        assert 0.5 < spent < 9.0, f"{bid} fallback spent {spent:.1f}s"


def test_a_short_beat_is_not_compressed_below_the_readable_floor():
    block = _b(_blocks(_OPENING + "{show statement} Five."), "straighten")
    spent = block.anim(FakeScene(beat_seconds=0.4), block.mobject, "dark")
    assert spent >= TM.BEAT_PACED_MIN_SECONDS, f"straighten compressed to {spent:.2f}s"


# -- the dock (zoom out for the opening, shrink home on {show statement}) -------

def test_show_statement_is_rewired_to_the_dock():
    stmt = _b(_DOCKED, "statement")
    assert callable(stmt.anim), "the statement reveal must carry the dock animation"
    assert stmt.anim_seconds, "a callable reveal must declare its nominal length"
    assert not stmt.static


def test_without_the_statement_marker_the_figure_stays_home():
    """No {show statement} -> the card is part of the opening frame, so there is no beat
    to dock on. The figure must then be built at home size, not stranded zoomed."""
    plain = _blocks(_OPENING + "The claim. {show proof.0} Six.")
    assert _b(plain, "statement").static
    assert not callable(_b(plain, "statement").anim)
    docked_w = _b(_DOCKED, "circle").mobject.width
    home_w = _b(plain, "circle").mobject.width
    assert home_w < docked_w * 0.75, (
        f"zoom not applied: home {home_w:.2f} vs opening {docked_w:.2f}")


# -- the built (terminal) layout the gates read --------------------------------

def test_the_built_figure_stays_inside_the_safe_area():
    right, top = T.FRAME_W / 2 - T.SAFE_MARGIN, T.FRAME_H / 2 - T.SAFE_MARGIN
    for bid in _IDS:
        m = _b(_DOCKED, bid).mobject
        assert m.get_left()[0] >= -right and m.get_right()[0] <= right, f"{bid} off-frame in x"
        assert m.get_bottom()[1] >= -top and m.get_top()[1] <= top, f"{bid} off-frame in y"


def test_the_figure_clears_the_proof_column():
    """The docked home is the empty right-hand region; the proof chain keeps the left."""
    proof_right = max(_b(_DOCKED, k).mobject.get_right()[0]
                      for k in ("proof.0", "proof.1", "qed"))
    plain = _blocks(_OPENING + "The claim. {show proof.0} Six.")
    for bid in _IDS:
        left = _b(plain, bid).mobject.get_left()[0]
        assert left > proof_right, f"{bid} starts at {left:.2f}, inside the proof column"


if __name__ == "__main__":
    test_the_four_marker_targets_exist_as_dynamic_graph_blocks()
    test_the_stock_template_blocks_survive()
    test_every_stage_animation_is_beat_paced()
    test_stages_fall_back_to_their_own_length_outside_a_beat()
    test_a_short_beat_is_not_compressed_below_the_readable_floor()
    test_show_statement_is_rewired_to_the_dock()
    test_without_the_statement_marker_the_figure_stays_home()
    test_the_built_figure_stays_inside_the_safe_area()
    test_the_figure_clears_the_proof_column()
    print("OK chord_vs_arc self-test")

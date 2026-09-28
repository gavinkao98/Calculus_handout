"""Self-test: every stock reveal name in `blocks._reveal` must play at exactly the
seconds `timing.STOCK_ANIM_SECONDS` declares for it -- that table is the single source
of truth (KICKOFF-toolline-backlog-r1.md §2.F item 3: `_reveal` used to hardcode its own
run_time per branch, and four of those had drifted out of sync with the table). `_reveal`
builds real manim Animation objects (FadeIn/Create/Write), which type-check their mobject
argument, so this drives real `Dot()`/`Square()` mobjects -- only `scene.play` itself is
faked (records the `run_time` kwarg instead of rendering).

Run: python -m pipeline._selftest_stock_anim
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import _bootstrap                       # noqa: E402

_bootstrap.bootstrap()   # _reveal builds real Fade/Create/Write animations -- bootstrap manim FIRST

from manim import Dot, Square                          # noqa: E402

from pipeline.blocks import Block, play_block          # noqa: E402
from pipeline.timing import STOCK_ANIM_SECONDS          # noqa: E402


class FakeScene:
    """Records what it was asked to play. No renderer, so `timing.elapsed` returns None
    and `play_block` reports `_reveal`'s nominal seconds untouched (see `timing.spent`)."""
    def __init__(self):
        self.plays: list = []

    def play(self, *anims, **kw):
        self.plays.append(kw.get("run_time"))

    def wait(self, seconds):
        pass


# Every stock name `_reveal` maps straight onto a STOCK_ANIM_SECONDS entry (the "write"
# branch's own wide-mobject fallback is the one exception -- see the test below).
_STOCK_NAMES = ("fade", "create", "grow", "slide", "highlight",
                "flash_in", "write_glow", "slide_pop", "write")


def test_every_stock_reveal_plays_the_table_seconds():
    for name in _STOCK_NAMES:
        scene = FakeScene()
        block = Block(id="x", mobject=Dot(), anim=name)   # Dot().width << 9.0u
        spent = play_block(scene, block, "dark")
        want = STOCK_ANIM_SECONDS[name]
        assert scene.plays == [want], (name, scene.plays, want)
        assert spent == want, (name, spent, want)


def test_write_wide_mobject_fallback_is_unaffected():
    """The one `_reveal` branch with no STOCK_ANIM_SECONDS entry: `write` on a mobject
    wider than 9.0u takes a different, unnamed 0.6s fallback. Not part of item 3's
    single-source fix -- pinned here so a later edit cannot silently fold it in."""
    scene = FakeScene()
    block = Block(id="x", mobject=Square(side_length=9.5), anim="write")
    spent = play_block(scene, block, "dark")
    assert scene.plays == [0.6] and spent == 0.6, scene.plays


if __name__ == "__main__":
    import traceback
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS {name}")
            except Exception:
                fails += 1; print(f"FAIL {name}"); traceback.print_exc()
    sys.exit(1 if fails else 0)

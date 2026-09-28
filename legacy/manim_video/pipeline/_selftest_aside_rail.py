"""Self-test: the right-rail `aside` card stays in the body zone, off the content, and in
sight of sizecheck (code review 2026-09-23 D2-02).

Run from video/:  python -m pipeline._selftest_aside_rail

Three gaps stacked on top of each other:
  * definition_math's collapse test looked only at the statement + math -- never at the
    aside's own height -- and the card was centred on the content with no clamp, so a
    three-sentence aside rode up over the title band / a scaffold motive, a four-sentence
    one off the top of the frame.
  * in aside mode the statement wrapped at the full PRIMARY_W, whose right edge IS the
    rail card's left edge (RAIL_X), with zero gutter; the char estimate under-measures a
    line carrying inline math by >10%, so a first line could run 0.5u under the OPAQUE
    card, which is drawn after it.
  * sizecheck saw none of it: the aside is layer="decoration", and the decoration
    exemption in _overflow_issues (meant for hero curves / motifs that bleed on purpose)
    skipped its frame check too, while _overlap_issues only compares content blocks.

Now: definition_math wraps the statement to PRIMARY_W minus a gutter, collapses the aside
when the card is taller than the body zone or a MEASURED statement/math line would reach
the rail, and clamps the card into the body zone. sizecheck checks the aside against the
frame like any content block (definition_math and theorem_proof alike) and reports any
content line the opaque card covers.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # templates import manim at module level -- bootstrap FIRST (repo rule)

from manim import Rectangle, VGroup                 # noqa: E402

from pipeline import sizecheck as S                  # noqa: E402
from pipeline.blocks import Block                    # noqa: E402
from pipeline.templates import build_blocks          # noqa: E402
from pipeline.templates._common import RAIL_X, body_zone   # noqa: E402
from pipeline.visuals import theme as T              # noqa: E402

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}
TOL = 1e-6

_SHORT = "Check every critical number and both endpoints."
_THREE = ("The inverse undoes $f$: feed it an output and it returns the one input that produced it. "
          "This only works when no two inputs share an output. Graphically the inverse is the mirror "
          "image of the graph of $f$ across the line $y=x$.")
_FOUR = ("The inverse undoes $f$: feed it an output and it returns the one input that produced it. "
         "This only works when no two inputs share an output, which is exactly the one-to-one condition. "
         "Graphically the inverse is the mirror image of the graph of $f$ across the line $y=x$. "
         "Domain and range trade places as well.")


def _dm(aside_body: str, **extra) -> dict:
    spec = {"id": "dm", "kind": "content", "template": "definition_math", "accent": "definition",
            "title": "Inverse Function", "say": "probe {show math.0}",
            "statement": "The inverse sends each output of $f$ back to the input it came from.",
            "math": [{"tex": r"$f^{-1}(y)=x \iff f(x)=y$", "anim": "highlight"}],
            "aside": {"label": "Key idea", "body": aside_body}}
    spec.update(extra)
    return spec


def _build(spec):
    return {b.id: b for b in build_blocks(spec, {"ground": "dark", "meta": _META})}


def _zone(by):
    """The body zone definition_math places into: under the last scaffold block, else the title."""
    ref = [b for bid, b in by.items() if bid.startswith("scaffold.")]
    return body_zone((ref[-1] if ref else by["title"]).mobject)


# -- definition_math: the template keeps the card in its lane ------------------------------

def test_aside_never_leaves_the_body_zone():
    for body in (_SHORT, _THREE, _FOUR):
        by = _build(_dm(body))
        if "aside" not in by:
            continue                                   # collapsed: nothing to place
        a = by["aside"].mobject
        zt, zb = _zone(by)
        assert a.get_top()[1] <= zt + TOL and a.get_bottom()[1] >= zb - TOL, (
            f"{len(body.split())}-word aside y[{a.get_bottom()[1]:.2f},{a.get_top()[1]:.2f}] "
            f"outside the body zone ({zb:.2f},{zt:.2f})")


def test_an_aside_taller_than_the_body_zone_collapses():
    by = _build(_dm(_FOUR))
    assert "aside" not in by, "a card taller than the body zone must collapse, not ride off-frame"
    assert by["statement"].mobject.width > 7.5, "collapsed -> the statement is back at full width"


def test_aside_clears_a_scaffold_motive_above_the_body():
    motive = ("We can already spot a one-to-one function; now we build the function that "
              "undoes it, one output at a time.")
    by = _build(_dm("$f$ asks: given the input $x$, what is the output? The inverse asks it "
                    "backwards: given that output, which input produced it?",
                    scaffold={"motive": motive}))
    assert "aside" in by
    m, a = by["scaffold.motive"].mobject, by["aside"].mobject
    assert a.get_top()[1] < m.get_bottom()[1], (
        f"aside top {a.get_top()[1]:.2f} reaches the motive (bottom {m.get_bottom()[1]:.2f})")


def test_statement_never_runs_under_the_rail_card():
    """The finding's case: the char estimate under-measures this line by ~0.8u -- more than
    any gutter absorbs -- so the template must measure, and collapse rather than intrude."""
    by = _build(_dm(_SHORT, accent="theorem", title="Extreme Values",
                    statement="Maximum and minimum values of $f$ on $[a,b]$ occur at critical "
                              "numbers or endpoints."))
    if "aside" in by:
        assert by["statement"].mobject.get_right()[0] <= RAIL_X + TOL, "statement runs under the card"


def test_statement_wraps_short_of_the_rail_with_a_gutter():
    """_demo_aside.aside_sparse: at the full PRIMARY_W this statement ended 0.003u from the
    card; wrapped to PRIMARY_W minus the gutter it leaves clear air."""
    by = _build(_dm("The $-1$ in $f^{-1}$ means the inverse function --- not a reciprocal."))
    assert "aside" in by
    gap = RAIL_X - by["statement"].mobject.get_right()[0]
    assert gap >= 0.3 - TOL, f"statement ends {gap:.3f}u from the rail card"


# -- sizecheck: the aside is measured ------------------------------------------------------

def _rect(w, h, x, y):
    return Rectangle(width=w, height=h).move_to([x, y, 0])


def test_overflow_checks_the_aside_but_still_exempts_other_decoration():
    blocks = [Block("aside", _rect(4.0, 3.0, 3.0, 3.5), layer="decoration"),     # top at 5.0
              Block("motif", _rect(1.0, 1.0, 7.5, -3.8), layer="decoration")]    # bleeds on purpose
    issues = S._overflow_issues({"id": "s"}, blocks)
    assert any(sev == "error" and "'aside'" in m and "clipped" in m for sev, m in issues), issues
    assert not any("'motif'" in m for _, m in issues), issues


def test_content_covered_by_the_aside_card_is_an_error():
    aside = Block("aside", _rect(4.0, 3.0, 3.0, 0.0), layer="decoration")        # x[1,5] y[-1.5,1.5]
    under = Block("statement", _rect(3.0, 0.4, 0.0, 0.5))                        # x[-1.5,1.5]
    clear = Block("math.0", _rect(2.0, 0.4, -1.0, -0.5))                         # x[-2,0]
    issues = S._aside_collision_issues({"id": "s"}, [under, clear, aside])
    assert [sev for sev, _ in issues] == ["error"], issues
    assert "'statement'" in issues[0][1] and "'aside'" in issues[0][1], issues


def test_aside_collision_is_judged_line_by_line():
    """A wrapped block's AABB is as wide as its WIDEST line; a short line beside the card
    must not be blamed for the long line above it."""
    aside = Block("aside", _rect(4.0, 2.0, 3.0, -1.0), layer="decoration")       # x[1,5] y[-2,0]
    long_line = _rect(6.0, 0.4, 0.0, 1.0)        # x[-3,3] y[0.8,1.2]: above the card
    short_line = _rect(2.0, 0.4, -2.0, -0.5)     # x[-3,-1]: beside the card, clear of it
    stmt = Block("statement", VGroup(long_line, short_line))
    assert S._aside_collision_issues({"id": "s"}, [stmt, aside]) == []


def test_theorem_proof_aside_is_frame_checked_too():
    spec = {"id": "tp", "kind": "content", "template": "theorem_proof", "accent": "theorem",
            "title": "Monotonicity Test", "say": "probe",
            "statement": "If $f'(x) > 0$ on an interval, then $f$ is strictly increasing there.",
            "aside": {"label": "Why", "body": _FOUR + " " + _FOUR}}
    by = _build(spec)
    a = by["aside"].mobject
    assert a.get_bottom()[1] < -T.FRAME_H / 2, "fixture: this aside must overflow the frame"
    issues = S.check_scenes(_META, [spec])
    assert any(sev == "error" and "'aside'" in m and "clipped" in m for sev, m in issues), issues


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

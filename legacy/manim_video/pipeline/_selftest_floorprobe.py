"""Self-test: the RUNTIME font-floor probe. Run from video/:
    python -m pipeline._selftest_floorprobe

Four contract cases (KICKOFF-toolline-backlog-r1 §2.B), all built directly after
`_bootstrap.bootstrap()` -- no render, no scene, no manim animation:

  (1) a 48 px `MathTex` that was `.scale(0.4)`d afterwards is reported below the floor
      (this is backlog (11)'s `carry: to: {scale: ...}` and (17)'s run-time scaling: the
      static gate reads the AUTHORED 48 and sees nothing);
  (2) a 34 px label containing `\\tfrac` is reported for its INNER (scriptstyle) size
      (backlog (1): 34 x 0.7 = 23.8 px, under the 26 px floor, and the node itself is
      clean so the static gate has nothing to report);
  (3) a 48 px pure formula is clean -- no finding of either kind;
  (4) a 42 px prose `Tex` is clean, which is the real assertion here: prose carries
      theme.TEXT_SCALE on top of PX_TO_FS, so a probe that forgot to divide it out would
      read 42 px prose as ~54 px and, worse, read a genuinely tiny line as fine.

(3) and (4) are the false-positive half of the contract: they are what stops the probe
from being switched off as noise. A fifth false-positive case was added after the first
real render (a token authored exactly AT the floor), plus three guards on the parts of the
contract that make the probe safe to call from inside a render: the owner attribution, the
message's context, and measure-only.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()

from manim import MathTex, Tex, VGroup  # noqa: E402

from pipeline import floorprobe  # noqa: E402
from pipeline.visuals import theme as T  # noqa: E402

FLOOR = T.MIN_FONT_FLOOR


def _math(px: float, tex: str) -> MathTex:
    """A MathTex authored at *px* on-screen pixels, the way brand.math_line sizes one."""
    return MathTex(tex, font_size=px * T.PX_TO_FS)


def _prose(px: float, text: str) -> Tex:
    """A prose Tex authored at *px*, the way brand's text builders size one (TEXT_SCALE)."""
    return Tex(text, font_size=px * T.PX_TO_FS * T.TEXT_SCALE)


def _kinds(findings) -> list:
    return sorted(f.kind for f in findings)


def test_runtime_scale_is_seen():
    """(1) 48 px scaled to 0.4 renders at 19.2 px -- the static gate reads the authored 48."""
    node = _math(48, r"\sin x + \cos x").scale(0.4)
    findings = floorprobe.probe([node])
    direct = [f for f in findings if f.kind == floorprobe.DIRECT]
    assert direct, f"scaled node must be reported; got {findings}"
    assert abs(direct[0].px - 19.2) < 0.5, direct[0].px
    assert direct[0].px < FLOOR


def test_tfrac_inner_is_seen():
    """(2) a 34 px \\tfrac label: the node is clean, its numerator/denominator are not."""
    node = _math(34, r"\tfrac{\sin x}{x}")
    findings = floorprobe.probe([node])
    assert _kinds(findings) == [floorprobe.INNER], findings
    inner = findings[0]
    assert abs(inner.px - 34 * floorprobe.SCRIPT_RATIO) < 0.5, inner.px
    assert inner.px < FLOOR


def test_plain_formula_is_clean():
    """(3) 48 px with no script markers: nothing to report, at either level."""
    assert floorprobe.probe([_math(48, r"y = mx + b")]) == []


def test_prose_tex_is_clean():
    """(4) 42 px prose: TEXT_SCALE must be divided back out, or this reads as ~54 px."""
    assert floorprobe.probe([_prose(42, "Sine and cosine are continuous.")]) == []


def test_a_token_authored_at_the_floor_is_clean():
    """The `eyebrow` token IS the floor (26 px), and px -> font_size -> px round-trips to
    25.999999999999996, so without sizecheck's `_FLOOR_EPS` every eyebrow on screen is
    reported. Found by the first real render (companion_limit's `[ EXAMPLE ]` eyebrow)."""
    node = _prose(T.MIN_FONT_FLOOR, r"\texttt{[ EXAMPLE ]}")
    assert floorprobe.probe([node]) == [], floorprobe.probe([node])


def test_owner_is_the_block_the_node_belongs_to():
    """The finding names WHERE the node came from: the block id when it is inside a
    block's mobject, `hook` when it is on screen but in no block (backlog (12))."""
    owned = _math(48, r"\tfrac{a}{b}").scale(0.4)
    loose = _math(48, r"\tfrac{c}{d}").scale(0.4)
    group = VGroup(owned)
    owners = {id(part): "result" for part in group.get_family()}
    findings = floorprobe.probe([group, loose], owners=owners)
    origins = {f.origin for f in findings}
    assert origins == {"result", floorprobe.HOOK}, origins


def test_probe_does_not_touch_the_mobjects():
    """MEASURE ONLY: the whole point is that wiring this into scene.py cannot move the
    picture or the clock. Guard the geometry the probe reads through."""
    node = _math(34, r"\tfrac{\sin x}{x}")
    before = (node.font_size, node.width, node.height,
              tuple(node.get_center()), len(node.submobjects))
    floorprobe.probe([node])
    after = (node.font_size, node.width, node.height,
             tuple(node.get_center()), len(node.submobjects))
    assert before == after, (before, after)


def test_message_carries_the_context():
    """The printed line must name scene, beat, origin, effective px and the tex head."""
    node = _math(48, r"\sin x + \cos x").scale(0.4)
    finding = floorprobe.probe([node], owners={id(node): "chain"})[0]
    msg = finding.message("squeeze_graph", "05")
    for piece in ("squeeze_graph", "beat 05", "chain", "19.2px", r"\sin x"):
        assert piece in msg, (piece, msg)


if __name__ == "__main__":
    import sys
    import traceback

    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except Exception:  # noqa: BLE001
                fails += 1
                print(f"FAIL {name}")
                traceback.print_exc()
    sys.exit(1 if fails else 0)

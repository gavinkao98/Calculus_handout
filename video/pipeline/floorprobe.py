"""floorprobe -- the RUN-TIME half of the font floor, next to sizecheck's static half.

`sizecheck._floor_issues` measures the BUILD layout: it walks the blocks a template
returned and recovers each prose node's AUTHORED px. Five of the §8 backlog items in
[`KICKOFF-shared-layer-v1.md`](../KICKOFF-shared-layer-v1.md) are one blind spot wearing
five hats -- what the beat actually puts on screen is not what was authored:

  (1)  a `\\tfrac` label's numerator/denominator render at TeX scriptstyle, ~0.7x the
       node's own size; the gate only ever sees the node's size (`squeeze_graph`'s 34 px
       label measured ~24 px inside);
  (2)  the public `font_size` getter over-reads on `substrings_to_isolate` nodes, so the
       static floor warn is UNDER-reported there;
  (11) `carry: to: {scale: 0.6}` shrinks the flown copy after the build (scene 24's
       carried tag measured ~19-23 px against a 26 px floor, with zero warnings);
  (12) a hook builds its own `MathTex`, which belongs to no block, so the static gate
       never sees it at all;
  (17) run-time `.scale()` / `exit:` move the picture away from the built layout.

This module closes them from the other side: it reads the SCENE's mobject tree while the
scene plays, so whatever chain of `.scale()` calls got a node to its on-screen size is
already baked into manim's `font_size` (`height / initial_height`, so it follows
`.scale()` -- tex_mobject.py:113).

MEASURE ONLY. `probe()` never waits, never plays and never touches a mobject: it reads
`font_size` and `tex_string` and returns findings. That is the whole safety argument for
calling it from inside `scene.py` -- the beat clock the `[sync]` audit measures cannot
move (`_selftest_floorprobe.test_probe_does_not_touch_the_mobjects`).

WARN ONLY, and deliberately no `meta.floorprobe_enforce` twin of `meta.fontfloor_enforce`:
the static gate runs BEFORE the render and can refuse it, while this one only knows what
it knows after the frames are drawn, so an "error" here could not stop anything it was
not already too late to stop. It reports; a human (or the static gate, once the finding is
traced back to an authored size) fixes.

Findings travel back to `make.py` on the channel that already exists for this -- the
`LessonScene` class attributes `make.py` sets around each `LessonScene().render()` (there
is no per-beat sidecar; the render runs in-process). See `scene.py::run_floorprobe`.
"""
from __future__ import annotations

from typing import Any, NamedTuple

# The SAME float-boundary tolerance the static floor check uses, imported rather than
# copied so the two halves of one floor can never drift apart: a token authored AT the
# floor (`eyebrow` = 26 px = MIN_FONT_FLOOR) round-trips through
# px -> font_size -> px as 25.999999999999996, and without this every eyebrow on screen
# would be reported. sizecheck is manim-free at import time, so this costs nothing here.
from .sizecheck import _FLOOR_EPS
from .visuals import theme as T

# TeX sets a \frac's numerator/denominator, and any super/subscript, in scriptstyle:
# 0.7 of the surrounding size in the standard \DefaultMathSizes that lmodern uses. This
# is an ESTIMATE of the inner size, not a measurement of it -- manim gives us the node,
# not its internal math-style tree -- which is why it is reported as its own kind of
# finding and never as an authored px.
SCRIPT_RATIO = 0.7

# tex that puts something in scriptstyle. `\sqrt[` is the index of a root (the radicand
# itself stays at the surrounding size, so a bare `\sqrt{` is NOT in this list).
_SCRIPT_MARKERS = (r"\tfrac", r"\frac", r"\sqrt[", "^", "_")

DIRECT = ""             # the node itself renders below the floor
INNER = "script inner"  # the node is fine, its scriptstyle parts are not
HOOK = "hook"           # on screen but inside no block: built at run time (backlog (12))

_TEX_HEAD = 40          # chars of tex kept for the message


class Finding(NamedTuple):
    """One node measured below the floor. `px` is the effective ON-SCREEN size: for
    `INNER` that is the scriptstyle estimate, not the node's own size."""

    origin: str   # the block id the node belongs to, or HOOK
    kind: str     # DIRECT | INNER
    px: float
    floor: float
    tex: str      # first _TEX_HEAD chars of the node's tex string

    def message(self, scene_id: str, beat: str) -> str:
        what = f"{self.kind} " if self.kind else ""
        return (f"{scene_id}: beat {beat} [{self.origin}] {what}renders at {self.px:.1f}px "
                f"< MIN_FONT_FLOOR {self.floor:.0f}px -- tex {self.tex!r}")


def probe(mobjects, *, floor: float = T.MIN_FONT_FLOOR,
          owners: "dict[int, str] | None" = None) -> "list[Finding]":
    """Findings for every Tex/MathTex under *mobjects* whose on-screen size is below
    *floor*. *owners* maps `id(mobject) -> block id` (scene.py builds it from the beat's
    blocks); anything not in it is reported as HOOK."""
    from manim import MathTex, Tex  # deferred: manim import is slow

    owners = owners or {}
    out: list[Finding] = []
    for node in _tex_nodes(mobjects, MathTex):
        px = _effective_px(node, Tex)
        if px is None:
            continue
        tex = str(getattr(node, "tex_string", "") or "")
        origin = owners.get(id(node), HOOK)
        if px < floor - _FLOOR_EPS:
            out.append(Finding(origin, DIRECT, px, floor, tex[:_TEX_HEAD]))
        if (any(marker in tex for marker in _SCRIPT_MARKERS)
                and px * SCRIPT_RATIO < floor - _FLOOR_EPS):
            out.append(Finding(origin, INNER, px * SCRIPT_RATIO, floor, tex[:_TEX_HEAD]))
    return out


def _tex_nodes(mobjects, MathTex) -> list:
    """Every TOP-LEVEL Tex/MathTex under *mobjects*, stopping at each match: a MathTex's
    own parts are the same string at the same size, so descending into them would report
    the one finding once per glyph group."""
    out: list = []
    for mob in mobjects:
        out += _tex_nodes_one(mob, MathTex)
    return out


def _tex_nodes_one(mob, MathTex) -> list:
    if isinstance(mob, MathTex):
        return [mob]
    out: list = []
    for sub in getattr(mob, "submobjects", []) or []:
        out += _tex_nodes_one(sub, MathTex)
    return out


def _effective_px(node: Any, Tex) -> "float | None":
    """The node's on-screen px, the run-time twin of `sizecheck._effective_font_px`.

    Same two-family arithmetic (prose Tex renders at fs(px) * TEXT_SCALE, math at
    fs(px) = px * PX_TO_FS), and the same ORDER trap: in this manim `Tex` subclasses
    `MathTex` (tex_mobject.py:607), so `Tex` must be tested first or every prose line is
    measured as math and comes out ~27% large. None when the node has no usable size
    (a zero-height mobject: manim's own `font_size` setter documents that those exist).
    """
    try:
        fs = float(node.font_size)
    except Exception:  # noqa: BLE001 -- a mobject with no measurable height, never fatal
        return None
    if fs <= 0:
        return None
    if isinstance(node, Tex):
        return fs / (T.TEXT_SCALE * T.PX_TO_FS)
    return fs / T.PX_TO_FS

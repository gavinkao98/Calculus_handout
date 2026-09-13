"""Motion primitive 7 -- 逐段隨讀: spread ONE block's reveal across its whole beat.

The §3.1 six-lens review's single most repeated finding is a beat that reveals one thing
in 0.5 s and then holds a finished picture for another 12-20 s (24 `must`s, `L-attention`
13 of them; `longest_still_seconds` correlates -0.82 with verdict, quality round ⑧). Most
of those beats do not need a new figure -- the block they reveal ALREADY has natural parts
(a wrapped prose paragraph is one Tex per line, a chip row is one card per chip, a math
grid is one row per line). Revealing those parts one at a time, evenly spaced across the
beat, turns "one reveal then 18 s of nothing" into "a reveal every 5 s" without touching
the narration, the content, or the layout: the final frame is identical, only the path to
it changes.

A block with no parts to walk -- one formula row, the other half of the finding -- is
instead WRITTEN across the beat: drawn glyph by glyph while the narration reads it, at a
capped stroke rate so a short line on a long beat is not crawled out.

Opt-in, per scene, by reveal id::

    paced: [body]            # or several: [math.0, statement]

Anything not named keeps its stock reveal, so no other deck changes behaviour, and a block
whose reveal is already a choreography (a hook, `anim: transform`) is left alone. `schema`
rejects a `paced` id that no `{show ...}` marker reveals.
"""
from __future__ import annotations

from typing import Any

from manim import FadeIn, UP, Write

from . import timing as TM

FADE_SECONDS = 0.45        # one part's entrance; the rest of its share is a hold
PART_LIMIT = 8             # more parts than this and the block is glyphs, not paragraphs
# An ATOMIC block (one formula row) has no parts to walk, so it is WRITTEN instead -- drawn
# glyph by glyph while the narration reads it. The rate is capped so a short line on a long
# beat is not drawn at a crawl; whatever is left of the beat is an ordinary hold.
WRITE_SECONDS_PER_GLYPH = 0.35
WRITE_LEAD_SECONDS = 1.0


def block_parts(mob: Any) -> list:
    """The parts a paced reveal walks: a block's own submobjects when there is a
    paragraph-sized number of them, else the block itself."""
    subs = list(getattr(mob, "submobjects", []) or [])
    return subs if 2 <= len(subs) <= PART_LIMIT else [mob]


def write_seconds(mob: Any, total: float) -> float:
    """How long to draw an atomic block: its own readable stroke rate, never more than the
    beat it has to fill."""
    try:
        glyphs = len(mob.family_members_with_points())
    except AttributeError:
        glyphs = 1
    return min(total, WRITE_LEAD_SECONDS + WRITE_SECONDS_PER_GLYPH * glyphs)


def paced_write(scene, mob) -> float:
    """One formula row, drawn while the narration reads it."""
    total = TM.beat_run_time(scene, 0.0)
    if total <= 0.0:                       # off-beat: the caller wants the stock length
        total = write_seconds(mob, float("inf"))
    secs = write_seconds(mob, total)
    scene.play(Write(mob), run_time=secs)
    scene.add(mob)
    return secs


def paced_reveal(scene, mob, _ground) -> float:
    """Reveal *mob*'s parts one at a time, evenly spaced over the beat.

    The hold goes AFTER each part (n gaps, not n-1): with the gaps between parts only, a
    two-part block would fire both reveals in the first half and leave the whole back half
    still -- which is the defect, moved rather than fixed. Spreading them n ways makes the
    longest still `beat/n` whatever n is."""
    parts = block_parts(mob)
    n = len(parts)
    if n == 1:
        return paced_write(scene, mob)
    spent = walk(scene, parts, TM.beat_run_time(scene, FADE_SECONDS * n))
    scene.add(mob)
    return spent


def walk(scene, parts, total: float) -> float:
    """Fade *parts* in one at a time, evenly spread over *total* seconds: each part's
    FADE_SECONDS entrance, then its share of whatever hold is left (n gaps, see
    paced_reveal). Shared with the transform / cancel rows, which walk their rail across
    the REST of the beat after the morph (rollout T1-1). Returns the seconds spent."""
    n = len(parts)
    gap = max((total - FADE_SECONDS * n) / n, 0.0)
    for part in parts:
        scene.play(FadeIn(part, shift=0.1 * UP), run_time=FADE_SECONDS)
        if gap:
            scene.wait(gap)
    return FADE_SECONDS * n + gap * n


def apply(spec: dict[str, Any], blocks: "list") -> "list":
    """Swap the stock reveal of every block named in ``spec['paced']`` for the paced one.
    Unknown ids are left to the schema/sizecheck reveal-target checks, which already
    report a `{show ...}` that names nothing. A derivation `anim: transform` / `cancel`
    row is a callable and so is skipped here -- it reads `paced` itself in
    derivation.build and walks its rail across the rest of the beat after the morph."""
    want = set(spec.get("paced") or [])
    if not want:
        return blocks
    for b in blocks:
        # A CALLABLE anim is already a choreography (a hook, or `anim: transform`, which
        # handles its own pacing); replacing it with the generic walk would silently delete
        # that, so pacing only ever upgrades a STOCK reveal.
        if b.id in want and not b.static and not callable(b.anim):
            n = len(block_parts(b.mobject))
            b.anim = paced_reveal
            # `anim_seconds` is what make.py's short-beat warning compares against the
            # beat's audio, so it must be the LEAST this reveal can cost, not the most.
            # The walk's floor is its n fades (which a very short beat really can overrun).
            # The atomic write has no floor of its own -- `write_seconds` caps it at the
            # beat -- so its floor is the paced minimum; declaring the uncapped natural
            # length instead made the warning fire on every long written row and claim
            # scene.py was padding seconds it never padded.
            b.anim_seconds = FADE_SECONDS * n if n > 1 else TM.BEAT_PACED_MIN_SECONDS
    return blocks

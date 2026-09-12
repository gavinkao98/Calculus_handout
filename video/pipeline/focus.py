"""`focus:` -- dim what the narration is not talking about right now.

    focus:                        # scene-level, opt-in
      - at: result                # when the beat revealing `result` starts...
        dim: [step.0, step.1]     # ...these fade back; everything else stays lit
      - at: check
        dim: []                   # restore everything

Motion primitive 4 (聚焦). The §3.1 rewatch review kept asking for the same move: a beat
spends twenty seconds on one half of what is on screen, and nothing tells the viewer which
half ("20.2 秒的結論段裡，畫面不告訴觀眾『第一個因子』『第二個因子』分別是哪一塊").

Design follows `pauses:` -- a scene-level list keyed to a reveal id -- for one reason: it
costs NO narration change. A `{focus ...}` marker inside `say` would have to be taught to
`narration.parse_say`, to `derive_spoken`'s parity check, AND to its marker stripper (which
uses `{show ...}` only, so a focus marker would leak straight into the spoken text and get
read aloud). A scene field touches none of that, so a focus is free: no re-derive, no
re-synthesis, no TTS call.

STATE MODEL: each entry replaces the dim-set from its beat onward, so `dim: []` restores.
Everything is restored at the end of the scene, which keeps the LAST frame identical to
the un-focused render -- the layout gates measure the built (un-rendered) snapshot and the
visual gates read the final frame, so neither sees a focus at all.

`indicate:` (SPEC-motion-language rule 3, the flash variant) rides on the same entry:

      - at: ineq
        dim: []
        indicate: [sector, tri_outer]   # these flash once (tint + 15% grow, then back)

It is a one-shot on that beat, not state: nothing to restore, and `dim` keeps its own
meaning (an entry still replaces the dim-set, so repeat the list to keep it). A block
cannot be in both `dim` and `indicate` of one entry (schema error) -- two animations on
one mobject in one beat, the later silently winning.
"""
from __future__ import annotations

from typing import Any

DIM_OPACITY = 0.35       # what a dimmed element fades back to (R2 asked for "40% 壓暗")
FADE_SECONDS = 0.4       # long enough to read as a shift of attention, short enough to
                         # stay inside the beat it belongs to
INDICATE_SECONDS = 0.8   # rule 3: "短暫換高亮色並微放大再回復（約 1 s）"
INDICATE_SCALE = 1.15


def scene_focus(scene: dict[str, Any]) -> "dict[str, list[str]]":
    """`{reveal id: [block ids to dim]}` for one scene spec; empty when absent.

    Last entry wins for a repeated `at` (schema flags that separately).
    """
    out: dict[str, list[str]] = {}
    for item in scene.get("focus") or []:
        if not isinstance(item, dict):
            continue
        at = item.get("at")
        if not isinstance(at, str) or not at:
            continue
        dim = item.get("dim")
        out[at] = [str(d) for d in dim if str(d)] if isinstance(dim, (list, tuple)) else []
    return out


def apply(scene, by_id: "dict[str, Any]", wanted: "list[str]",
          currently_dimmed: "set[str]") -> "set[str]":
    """Fade *wanted* back and restore anything dimmed that is no longer wanted.

    Returns the new dimmed set. Plays at most ONE animation (all the opacity changes go
    into a single `scene.play`), so a focus costs FADE_SECONDS of the beat, not one fade
    per element. Returns without playing when nothing changes.
    """
    target = {b for b in wanted if b in by_id}
    to_dim = target - currently_dimmed
    to_restore = currently_dimmed - target
    if not to_dim and not to_restore:
        return currently_dimmed

    anims = []
    for b in sorted(to_dim):
        mob = by_id[b].mobject
        # Snapshot BEFORE dimming and restore from that, never `set_opacity(1.0)`:
        # set_opacity forces fill AND stroke to the given value on every family member,
        # so restoring to 1.0 would fill in anything deliberately hollow. Caught on the
        # first render of this primitive -- the (1)(2)(3) region badges are rings drawn
        # with fill_opacity=0, and "restoring" them turned two of them into solid discs
        # with their digits buried.
        mob.save_state()
        anims.append(mob.animate.set_opacity(DIM_OPACITY))
    anims += [by_id[b].mobject.animate.restore() for b in sorted(to_restore)]
    scene.play(*anims, run_time=FADE_SECONDS)
    return target


def scene_indicate(scene: dict[str, Any]) -> "dict[str, list[str]]":
    """`{reveal id: [block ids to flash]}` for the entries that carry `indicate`."""
    out: dict[str, list[str]] = {}
    for item in scene.get("focus") or []:
        if not isinstance(item, dict):
            continue
        at, ids = item.get("at"), item.get("indicate")
        if isinstance(at, str) and at and isinstance(ids, (list, tuple)):
            out[at] = [str(i) for i in ids if str(i)]
    return out


def indicate(scene, by_id: "dict[str, Any]", wanted: "list[str]", color: str) -> float:
    """Flash *wanted* once (manim `Indicate`: tint to *color*, grow INDICATE_SCALE, back).

    Its own `scene.play`, played right after `apply`, not folded into it: mixing an
    Indicate with the `.animate` opacity changes in one play works (mock-rendered
    2026-09-13), but a play has ONE run_time and the two moves want different ones
    (FADE_SECONDS vs INDICATE_SECONDS). Returns the seconds spent, 0 when nothing to flash.
    """
    mobs = [by_id[b].mobject for b in wanted if b in by_id]
    if not mobs:
        return 0.0
    from manim import Indicate   # deferred: this module stays importable without manim

    scene.play(*[Indicate(m, scale_factor=INDICATE_SCALE, color=color) for m in mobs],
               run_time=INDICATE_SECONDS)
    return INDICATE_SECONDS

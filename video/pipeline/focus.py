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
"""
from __future__ import annotations

from typing import Any

DIM_OPACITY = 0.35       # what a dimmed element fades back to (R2 asked for "40% 壓暗")
FADE_SECONDS = 0.4       # long enough to read as a shift of attention, short enough to
                         # stay inside the beat it belongs to


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

    anims = [by_id[b].mobject.animate.set_opacity(DIM_OPACITY) for b in sorted(to_dim)]
    anims += [by_id[b].mobject.animate.set_opacity(1.0) for b in sorted(to_restore)]
    scene.play(*anims, run_time=FADE_SECONDS)
    return target

"""graph template -- the unified graph engine (Direction D merge of graph_focus +
graph_compare).

One template, selected by ``mode``:
  - mode: single  (default) -> a single panel  (the old graph_focus payload:
                               top-level ``axes`` / ``plots`` / ``annotations``)
  - mode: 2up    | compare  -> two side-by-side panels (the old graph_compare
                               payload: ``left`` / ``right`` + ``annotations``)

The actual drawing lives in graph_focus (single-panel machinery, reused by
graph_compare for each side), so this is a thin dispatcher -- no logic is
duplicated, and the glow recipe / colours / reveal ids are identical to the
originals. The old ``graph_focus`` / ``graph_compare`` template names remain
registered as deprecated aliases so any un-migrated storyboard still renders.

YAML shape (single):
  template: graph
  mode: single
  axes: {...}
  plots: [...]

YAML shape (2-up):
  template: graph
  mode: 2up
  left:  { axes: {...}, plots: [...] }
  right: { axes: {...}, plots: [...] }
"""
from __future__ import annotations

from typing import Any

from ..blocks import Block
from . import graph_compare as gc
from . import graph_focus as gf

_TWO_UP = {"2up", "two-up", "twoup", "compare", "2-up"}


def graph_mode(spec: dict[str, Any]) -> str:
    """Normalise a graph scene to 'single' or 'compare' (used by the critics too)."""
    return "compare" if str(spec.get("mode", "single")).lower() in _TWO_UP else "single"


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    if graph_mode(spec) == "compare":
        return gc.build(spec, ctx)
    return gf.build(spec, ctx)

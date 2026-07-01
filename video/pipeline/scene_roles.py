"""Central eyebrow-chip resolver + the scene-role vocabulary.

A scene's top-left eyebrow chip (`[ DEFINITION ]`, `[ THEOREM ]`, ...) is decided
here, in ONE place, instead of being scattered across each template's `scene_head`
`label=` argument. The vocabulary is deliberately split from the COLOUR axis:
`accent` (see blocks.ACCENT_ROLE) drives colour; `scene_role` drives the chip.

`scene_role` is a pedagogical BEAT, not a math-object kind. Exposition beats
(motivation / intuition / bridge / forward-ref / setup / roadmap) map to ``None``
-- they render CHIPLESS, because a chip means "this is a genuine formal object"
(the visual rule is one-way: exposition => no chip; a chipless scene need not be
exposition -- graph/figure scenes are chipless too, by a different path).

Kept pure (no Manim import) so `lint.py` can import it cheaply and statically.
"""
from __future__ import annotations

from typing import Any

# scene_role -> chip text, or None for a chipless (exposition) beat.
SCENE_ROLE_CHIP: dict[str, "str | None"] = {
    # exposition / rhetorical beats -- chipless
    "motivation": None,
    "intuition": None,
    "bridge": None,
    "forward-ref": None,
    "setup": None,
    "roadmap": None,
    # formal / semi-formal objects -- explicit chip (lets scene_role become the
    # full chip axis incrementally; only exposition + remark are used this pass)
    "definition": "[ definition ]",
    "theorem": "[ theorem ]",
    "proposition": "[ proposition ]",
    "example": "[ example ]",
    "remark": "[ remark ]",
    "caution": "[ caution ]",
    "note": "[ note ]",
    "procedure": "[ procedure ]",
    "recap": "[ recap ]",
    "derivation": "[ derivation ]",
}

# roles that render chipless (chip is None)
EXPOSITION_ROLES = frozenset(r for r, chip in SCENE_ROLE_CHIP.items() if chip is None)


def resolve_chip(spec: dict[str, Any], default_label: str) -> "str | None":
    """Resolve a scene's eyebrow chip. Returns the chip text, or ``None`` = chipless.

    Precedence (highest first):
      1. ``kicker``        -- explicit per-scene word override (existing behaviour)
      2. ``label``         -- explicit per-scene chip text (e.g. theorem_proof's
                              "[ proof of the chain rule ]"); wins over scene_role so a
                              later scene_role can never silently erase an authored label
      3. ``scene_role``    -- semantic beat -> mapped chip (may be ``None`` = chipless)
      4. ``default_label`` -- the template's default (accent-LABEL / fixed string)

    An unknown ``scene_role`` raises ``ValueError`` (typo guard; lint surfaces it too).
    """
    if spec.get("kicker"):
        return f"[ {spec['kicker']} ]"
    if spec.get("label"):
        return spec["label"]
    role = spec.get("scene_role")
    if role is not None:
        if role not in SCENE_ROLE_CHIP:
            raise ValueError(
                f"unknown scene_role {role!r}; known: {sorted(SCENE_ROLE_CHIP)}")
        return SCENE_ROLE_CHIP[role]
    return default_label

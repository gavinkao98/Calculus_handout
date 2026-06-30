"""provenance.py -- OTF deterministic layer: ref grammar + locus loader + resolver
+ the warn-only storyboard provenance check. Pure stdlib; no model calls.

Grammar (see PLAN-pedagogy-firstlearner-sp1-foundation.md): a resolvable ref is
"md:<unit_id>" (a content-script unit) or "doc:<anchor>" (a handout frag-sec-* /
data-fig anchor). Scene-level `ref:` is inherited by on-screen teaching-text
fields; a `refs:` map overrides per field. This layer checks RESOLUTION only --
text-vs-source faithfulness (OF1) is the gate-1 agent (Plan 3).
"""
from __future__ import annotations

import re

# Fields that render as on-screen TEACHING text (subject to OTF). Brand text
# (title/eyebrow/kicker/subtitle) and data labels (graph axis/curve labels) are
# NOT here; hook-rendered text is out of scope (-> hook-engineering gate).
TEACHING_TEXT_FIELDS = frozenset({
    "statement", "scaffold.motive", "scaffold.problem", "problem",
    "annotations", "body", "reason", "points", "prompt",
})

OTF_KINDS = frozenset({"content", "divider"})
OTF_EXEMPT_KINDS = frozenset({"intro", "outro"})

_REF = re.compile(r"^(md|doc):(\S.*)$")


def parse_ref(s: str) -> "tuple[str, str] | None":
    """('md'|'doc', token) for a well-formed ref, else None. Empty token rejected."""
    if not isinstance(s, str):
        return None
    m = _REF.match(s.strip())
    return (m.group(1), m.group(2).strip()) if m and m.group(2).strip() else None

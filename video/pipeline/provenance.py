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


from dataclasses import dataclass, field
from pathlib import Path

_FRAG = re.compile(r'<template\s+id="(frag-sec-[\w-]+)"')
_DFIG = re.compile(r'data-fig="([\w-]+)"')


@dataclass
class Loci:
    """Resolvable provenance targets for one deck."""
    md_unit_ids: "set[str]" = field(default_factory=set)
    handout_anchors: "set[str]" = field(default_factory=set)

    def resolves(self, ref: str) -> bool:
        parsed = parse_ref(ref)
        if parsed is None:
            return False
        scheme, token = parsed
        if scheme == "md":
            return token in self.md_unit_ids
        return token in self.handout_anchors    # scheme == "doc"

    @classmethod
    def from_deck(cls, meta: dict, repo_root: Path) -> "Loci":
        from pipeline import review_pack
        deck_id = str(meta.get("id", ""))
        md = repo_root / "video" / "content_scripts" / f"{deck_id}.md"
        unit_ids: set[str] = set()
        if md.exists():
            parsed = review_pack.parse_content_script(md)
            unit_ids = {u["id"] for u in parsed.get("units", []) if u.get("id")}
        anchors = cls._handout_anchors(meta, repo_root)
        return cls(md_unit_ids=unit_ids, handout_anchors=anchors)

    @staticmethod
    def _handout_anchors(meta: dict, repo_root: Path) -> "set[str]":
        # chapter "Chapter 3" -> handout/chapter3-print-standalone.html
        m = re.search(r"(\d+)", str(meta.get("chapter", "")))
        if not m:
            return set()
        html = repo_root / "handout" / f"chapter{m.group(1)}-print-standalone.html"
        if not html.exists():
            return set()
        text = html.read_text(encoding="utf-8", errors="replace")
        return set(_FRAG.findall(text)) | set(_DFIG.findall(text))

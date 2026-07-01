"""_screen_contract.py -- parse one `.md` unit's `screen_contract` block scalar.
Pure stdlib + yaml; NO manim/TeX bootstrap, so both content-script parsers
(review_pack, narration_review -- kept in sync) can import it safely.

A screen_contract is:
  required_steps:
    - {id, tex, reason?, depends_on?, recap_required?}
  coverage_exempt: true   # OR this, to opt a scoped proof/derivation unit out

See SPEC-pedagogy-firstlearner-expansion.md §4 and
PLAN-pedagogy-firstlearner-expansion-plan1-coverage.md (grammar LOCKED there).
"""
from __future__ import annotations

import textwrap

import yaml


def parse_block(lines: "list[str]") -> "dict | None":
    """Collected block-scalar lines (as captured by the .md parser, 2-space
    indented) -> dict. Dedent, yaml.safe_load. Malformed / non-dict / empty
    -> None (fail-closed)."""
    text = textwrap.dedent("\n".join(lines)).strip()
    if not text:
        return None
    try:
        val = yaml.safe_load(text)
    except yaml.YAMLError:
        return None
    return val if isinstance(val, dict) else None


def required_steps(contract: "dict | None") -> "list[dict]":
    if not isinstance(contract, dict):
        return []
    steps = contract.get("required_steps")
    if not isinstance(steps, list):
        return []
    return [s for s in steps if isinstance(s, dict) and s.get("id")]


def is_exempt(contract: "dict | None") -> bool:
    return bool(isinstance(contract, dict) and contract.get("coverage_exempt") is True)


def must_show(contract: "dict | None") -> "list[dict]":
    """required_steps minus pure back-references (has depends_on, no recap_required)."""
    out: list[dict] = []
    for s in required_steps(contract):
        if s.get("depends_on") and not s.get("recap_required"):
            continue
        out.append(s)
    return out

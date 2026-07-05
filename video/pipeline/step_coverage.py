"""step_coverage.py -- SC deterministic layer (spec §4): SC1 (a declared must-show
step not covered on screen) + SC2 (a recap_required back-ref not locally
covered) + orphan covers ids + missing-contract-under-enforce. Pure stdlib.
warn-default; severity flips to 'error' under meta.coverage_enforce.

Model: each `.md` unit MAY declare a screen_contract (required_steps + optional
coverage_exempt). Each storyboard scene MAY declare a scene-level `covers: [id]`
of its own ref-ed unit's steps. A unit is covered iff the union of `covers:`
across all scenes ref-ing it includes every must-show step. Merging/re-layout is
free (one reveal may cover many ids); only dropping a must-show step is a finding.
"""
from __future__ import annotations

from pipeline import _screen_contract as _sc
from pipeline.provenance import parse_ref

_SCOPED_TEMPLATES = frozenset({"theorem_proof", "derivation"})


def covers_by_unit(storyboard: dict) -> "dict[str, set[str]]":
    """Union of scene-level `covers:` grouped by the `md:` unit the scene ref-s."""
    if not isinstance(storyboard, dict):
        return {}
    out: dict[str, set[str]] = {}
    for scene in (storyboard.get("scenes") or []):
        if not isinstance(scene, dict):
            continue
        ref = scene.get("ref")
        parsed = parse_ref(ref) if isinstance(ref, str) else None
        if not parsed or parsed[0] != "md":
            continue
        cov = scene.get("covers")
        if isinstance(cov, list):
            out.setdefault(parsed[1], set()).update(c for c in cov if isinstance(c, str))
    return out


def coverage_issues(storyboard: dict, contracts: "dict[str, dict]", enforce: bool) -> "list[tuple[str, str]]":
    """(severity, message) for SC1 (a plain must-show step uncovered), SC2 (a
    recap_required back-ref not re-shown locally), orphan covers ids, and --
    under enforce -- a scoped proof/derivation scene whose unit has no contract.
    severity = 'error' if enforce else 'warn' (orphan is always 'warn')."""
    if not isinstance(storyboard, dict):
        return []          # malformed deck: schema_storyboard reports it; coverage stays quiet (Codex R4)
    sev = "error" if enforce else "warn"
    cov = covers_by_unit(storyboard)
    issues: list[tuple[str, str]] = []
    for unit_id, contract in contracts.items():
        if _sc.is_exempt(contract):
            continue
        req_ids = {s["id"] for s in _sc.required_steps(contract)}
        C = cov.get(unit_id, set())
        for cid in sorted(C - req_ids):
            issues.append(("warn", f"{unit_id}: covers id {cid!r} has no matching "
                                   f"required_step (typo/drift)"))
        for s in _sc.must_show(contract):
            if s.get("recap_required"):
                continue          # recap steps report as SC2 below (avoid double-report)
            if s["id"] not in C:
                issues.append((sev, f"[SC1] {unit_id}.{s['id']}: required on-screen step "
                                    f"not covered by any scene's covers: -- {s.get('tex', '')!r}"))
        for s in _sc.required_steps(contract):
            if s.get("recap_required") and s["id"] not in C:
                issues.append((sev, f"[SC2] {unit_id}.{s['id']}: cash-in result (recap_required) "
                                    f"not re-shown locally -- {s.get('tex', '')!r}"))
    if enforce:
        flagged: set[str] = set()
        for scene in (storyboard.get("scenes") or []):
            if not isinstance(scene, dict) or scene.get("template") not in _SCOPED_TEMPLATES:
                continue
            ref = scene.get("ref")
            parsed = parse_ref(ref) if isinstance(ref, str) else None
            if not parsed or parsed[0] != "md" or parsed[1] in flagged:
                continue
            unit = parsed[1]
            c = contracts.get(unit)
            if c is None or (not _sc.required_steps(c) and not _sc.is_exempt(c)):
                flagged.add(unit)
                issues.append(("error", f"[SC] {unit}: proof/derivation unit under "
                                        f"coverage_enforce has no screen_contract "
                                        f"(add required_steps or coverage_exempt: true)"))
    return issues

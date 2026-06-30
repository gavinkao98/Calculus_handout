"""pedagogy.py -- PD deterministic layer (spec §9.2/§9.3): PD2 motive existence,
PD3 divider-problem existence, PD4 assumptions-registry consistency. Pure stdlib;
no model calls. warn-default; severity flips to 'error' under meta.pedagogy_enforce
(separate from OTF's meta.otf_enforce -- spec §7 keeps PD and OF as separate families).
Absent scaffold/registry => no findings (zero behavior change until opt-in).
"""
from __future__ import annotations


def assumptions_registry_issues(data: dict, enforce: bool) -> "list[tuple[str, str]]":
    """(severity, message) per registry inconsistency. Registry optional: absent -> [].
    Each assumption needs id/text/first_use_unit/source; first_use_unit must be a real
    scene id; that scene must carry scaffold.flag == id; no orphan flags."""
    sev = "error" if enforce else "warn"
    meta = data.get("meta", {}) if isinstance(data, dict) else {}
    assumptions = meta.get("assumptions")
    if not isinstance(assumptions, list):
        return []
    scenes_by_id = {s.get("id"): s for s in (data.get("scenes") or [])
                    if isinstance(s, dict) and s.get("id")}
    issues: list[tuple[str, str]] = []
    seen_ids: set[str] = set()
    for i, a in enumerate(assumptions):
        if not isinstance(a, dict):
            issues.append((sev, f"meta.assumptions[{i}]: not a mapping"))
            continue
        aid = a.get("id")
        if not isinstance(aid, str) or not aid.strip():
            issues.append((sev, f"meta.assumptions[{i}]: missing/empty `id`"))
            continue
        seen_ids.add(aid)
        for key in ("text", "first_use_unit", "source"):
            if not isinstance(a.get(key), str) or not a[key].strip():
                issues.append((sev, f"meta.assumptions[{i}] (id={aid!r}): missing/empty `{key}`"))
        unit = a.get("first_use_unit")
        if isinstance(unit, str) and unit.strip():
            scene = scenes_by_id.get(unit)
            if scene is None:
                issues.append((sev, f"assumption {aid!r}: first_use_unit {unit!r} is not a scene id"))
            else:
                scaf = scene.get("scaffold")
                flag = scaf.get("flag") if isinstance(scaf, dict) else None
                if flag != aid:
                    issues.append((sev, f"{unit}: first_use_unit of {aid!r} must render "
                                        f"scaffold.flag: {aid!r} (found {flag!r})"))
    for sid, scene in scenes_by_id.items():
        scaf = scene.get("scaffold")
        flag = scaf.get("flag") if isinstance(scaf, dict) else None
        if isinstance(flag, str) and flag and flag not in seen_ids:
            issues.append((sev, f"{sid}: scaffold.flag {flag!r} has no meta.assumptions entry"))
    return issues

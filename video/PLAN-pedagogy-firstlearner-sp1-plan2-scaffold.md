# Scaffold Model + Templates — Implementation Plan (SP1, Plan 2 of 5)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add optional `scaffold` on-screen teaching text (motive / divider-problem / first-use flag) + a deck-level `assumptions` registry, with deterministic **warn-default** checks, so first-learner framing renders and "first-use assumptions are flagged" is checkable — all **zero behavior change** until per-deck opt-in.

**Architecture:** A new `video/pipeline/pedagogy.py` (parallel to Plan 1's `provenance.py`) holds the PD2/PD3/PD4 deterministic checks (`pedagogy_issues`, `assumptions_registry_issues`), wired **warn-only** into `schema.py main()` **and** the `make.py` render gate (gating only on `meta.pedagogy_enforce`). A new `render_scaffold()` helper in `templates/_common.py` renders motive (small `text`-role line under the title), divider problem (formula block), and flag (assumption badge); each content/divider template calls it after `scene_head()`. No scalar shape changes; absent `scaffold` = no-op.

**Tech Stack:** Python 3.12 stdlib (`re`, `pathlib`) for the checks; manim + `brand`/`theme`/`Block` for rendering; stdlib `assert` self-tests; mock render + visual gate (`critic.py` + visual-frame-audit) for rendering verification. Run python via `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe`.

## Global Constraints

- **Spec authority:** `video/SPEC-pedagogy-firstlearner-framework.md` — §6 (承載設計), §9.2/§9.3 (deterministic PD checks). This plan implements that deterministic + rendering layer only; the gate-1 *judgment* agent (PD1–PD4 advisory + OF1–OF2) is Plan 3.
- **No new dependency. No pytest.** Logic tests are stdlib `assert` scripts run via the venv python.
- **Warn-default, per-deck opt-in.** PD checks emit `warn` unless `meta.pedagogy_enforce is True`; then `error`. Landing must not change any existing deck's exit code or output (none set the flag). Separate from Plan 1's `meta.otf_enforce` (spec §7: PD and OF are separate families).
- **No scalar shape change.** `scaffold` is a sibling mapping `{motive?, problem?, flag?}`. `statement`/`subtitle`/`body`/`reason`/`points[]` stay scalars/lists. **Absent `scaffold` = render unchanged (no-op).** (Spec §9.5.)
- **motive/problem render `role="text"` (ink_2), NEVER `muted`** — `muted` (ink_3) trips the `sizecheck.py` muted-prose warning and violates DESIGN.md "teaching content uses text/primary". De-emphasis is via size (`prose_sm`), not dimming. (Spec §6a.)
- **Offline, zero-API.** Pure local file reads for checks; mock render + local manim/ffmpeg for visual verification. No billed API.
- **Surgical.** Follow existing `pipeline/` + `templates/` style. Touch only the files named per task.
- **Provenance is already prepared.** Plan 1's `provenance.py` `TEACHING_TEXT_FIELDS` already lists `scaffold.motive` and `scaffold.problem` — no change there; once scaffold fields exist in storyboards, the OTF provenance check covers them automatically.

## Decisions (LOCKED by this plan — review here first)

- **enforce flag = new `meta.pedagogy_enforce`** (separate from `meta.otf_enforce`) gates PD2/PD3/PD4. (User decision; spec §7 PD/OF separate families, separate counts.)
- **New module `pedagogy.py`** (parallel to `provenance.py`) for the PD deterministic checks — *not* extending `provenance.py`. Keeps OTF vs pedagogy single-responsibility and matches the two-family / two-flag split. **(This deviates from the Plan-1 bullet's "extends provenance.py", which predated the separate-flag decision.)**
- **No `text_of()` adapter.** Dropped as YAGNI: Plan 1's grammar puts provenance in sibling `ref:`/`refs:`, so scalars (`statement`/`subtitle`/`body`/scaffold strings) are never wrapped into objects — a string-or-object adapter would have no object case. Add it later only if `{text:, ref:}` object scalars ever become real.
- **render integration = Option A:** each content/divider template calls `render_scaffold()` after `scene_head()` (templates own their layout).
- **scaffold = static Block(s):** shown at scene start (framing context), not `{show}`-revealed.
- **motive/problem:** `brand.prose(role="text", size="prose_sm")` for motive (small line under title); divider `problem` is a formula-capable prose block under the title (stronger than the wrapping `subtitle`, which stays brand).
- **flag:** `render_scaffold` looks up `meta.assumptions[id].text` and renders a small aside/badge (`build_aside` style).
- **pedagogy_profile:** validated (default `first_time`, unknown → warn); SP1 adds **no** profile-conditional rendering (spec §6c YAGNI). The gate-1 agent (Plan 3) reads it from the storyboard directly — no render-ctx plumbing here.
- **registry check:** `assumptions_registry_issues(data, enforce)` — each assumption has `id`/`text`/`first_use_unit`/`source`; `first_use_unit` is a real scene id; that scene carries `scaffold.flag == id`; no orphan flags.

---

## File Structure

- **Create** `video/pipeline/pedagogy.py` — PD2/PD3/PD4 deterministic checks (`assumptions_registry_issues`, `pedagogy_issues`). One responsibility: pedagogy structural/registry checks.
- **Create** `video/pipeline/_selftest_pedagogy.py` — stdlib `assert` self-test (mirrors `_selftest_provenance.py`; run via venv python).
- **Create** `video/storyboards/_fixtures/scaffold.yml` — fixture exercising motive/problem/flag + a (good and bad) registry; used by the schema self-test and the Task 5 mock-render visual gate.
- **Modify** `video/pipeline/schema.py` — call `pedagogy.pedagogy_issues(...)` from `main()` as warn-only (gate on `meta.pedagogy_enforce`), right after Plan 1's `[provenance]` block.
- **Modify** `video/make.py` — same call in the render gate, right after Plan 1's `[provenance]` block.
- **Modify** `video/pipeline/templates/_common.py` — add `render_scaffold()` + `_assumption_text()`.
- **Modify** `video/pipeline/templates/definition_math.py`, `theorem_proof.py`, `derivation.py`, `divider.py` — call `render_scaffold()` after `scene_head()`; position under the title; no-op when absent.

---

### Task 1: assumptions registry consistency check (PD4)

**Files:**
- Create: `video/pipeline/pedagogy.py`
- Create: `video/pipeline/_selftest_pedagogy.py`

**Interfaces:**
- Produces: `assumptions_registry_issues(data: dict, enforce: bool) -> list[tuple[str, str]]`. Registry is optional: absent/non-list `meta.assumptions` → `[]`. severity = `"error" if enforce else "warn"`.

- [ ] **Step 1: Write the failing self-test**

Create `video/pipeline/_selftest_pedagogy.py`:

```python
"""Stdlib assert self-test for pedagogy.py. Run: python video/pipeline/_selftest_pedagogy.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import pedagogy as P  # noqa: E402


def test_registry_ok():
    data = {"meta": {"assumptions": [
        {"id": "radians", "text": "$\\theta$ in radians", "first_use_unit": "u1", "source": "doc:frag-sec-3-1"},
    ]}, "scenes": [{"id": "u1", "kind": "content", "scaffold": {"flag": "radians"}}]}
    assert P.assumptions_registry_issues(data, enforce=False) == []


def test_registry_absent_is_noop():
    assert P.assumptions_registry_issues({"meta": {}, "scenes": []}, enforce=False) == []


def test_registry_findings():
    data = {"meta": {"assumptions": [
        {"id": "radians", "text": "x", "first_use_unit": "missing", "source": "s"},   # unit not found
        {"id": "noflag", "text": "x", "first_use_unit": "u2", "source": "s"},          # scene lacks flag
        {"id": "blank", "text": "", "first_use_unit": "u2", "source": "s"},            # empty text
    ]}, "scenes": [
        {"id": "u2", "kind": "content"},                                               # no scaffold.flag
        {"id": "u3", "kind": "content", "scaffold": {"flag": "orphan"}},               # orphan flag
    ]}
    warns = P.assumptions_registry_issues(data, enforce=False)
    msgs = " | ".join(m for _, m in warns)
    assert all(s == "warn" for s, _ in warns)
    assert "missing" in msgs            # first_use_unit not a scene id
    assert "u2" in msgs                 # scene lacks required flag
    assert "blank" in msgs              # empty text field
    assert "orphan" in msgs             # orphan flag has no registry entry
    errs = P.assumptions_registry_issues(data, enforce=True)
    assert all(s == "error" for s, _ in errs)
    assert len(errs) == len(warns)


if __name__ == "__main__":
    test_registry_ok()
    test_registry_absent_is_noop()
    test_registry_findings()
    print("OK pedagogy self-test")
```

- [ ] **Step 2: Run it to verify it fails**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_pedagogy.py`
Expected: FAIL — `ModuleNotFoundError`/`AttributeError` (no `pedagogy` module / no `assumptions_registry_issues`).

- [ ] **Step 3: Write minimal `pedagogy.py`**

Create `video/pipeline/pedagogy.py`:

```python
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
```

- [ ] **Step 4: Run it to verify it passes**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_pedagogy.py`
Expected: `OK pedagogy self-test`

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/pedagogy.py video/pipeline/_selftest_pedagogy.py
git commit -m "feat(pedagogy): assumptions registry consistency check (PD4)"
```

---

### Task 2: PD2/PD3 structural checks + pedagogy_profile validation

**Files:**
- Modify: `video/pipeline/pedagogy.py`
- Modify: `video/pipeline/_selftest_pedagogy.py`

**Interfaces:**
- Produces: `pedagogy_issues(data: dict, enforce: bool) -> list[tuple[str, str]]` — PD2 (`theorem_proof`/`derivation` should carry `scaffold.motive`), PD3 (`kind: divider` should carry `scaffold.problem`), PD4 (calls `assumptions_registry_issues`), plus a `pedagogy_profile` sanity note. PD2/PD3/PD4 severity = `error if enforce else warn`; profile-unknown is always `warn`. `definition_math` is **not** in the motive set (spec §9.2: its motive is gate-1 advisory, not deterministic).

- [ ] **Step 1: Add the failing self-test**

Append to `_selftest_pedagogy.py` (before `__main__`):

```python
def test_pedagogy_issues():
    data = {"meta": {"pedagogy_profile": "first_time"}, "scenes": [
        {"id": "thm", "kind": "content", "template": "theorem_proof"},          # missing motive
        {"id": "der", "kind": "content", "template": "derivation",
         "scaffold": {"motive": "why"}},                                         # ok
        {"id": "def", "kind": "content", "template": "definition_math"},         # exempt (not deterministic)
        {"id": "div", "kind": "divider"},                                        # missing problem
    ]}
    warns = P.pedagogy_issues(data, enforce=False)
    msgs = " | ".join(m for _, m in warns)
    assert "thm" in msgs and "scaffold.motive" in msgs    # PD2 fires
    assert "div" in msgs and "scaffold.problem" in msgs   # PD3 fires
    assert "der:" not in msgs and "def" not in msgs       # has motive / exempt (":" avoids 'divider' substring collision)
    assert all(s == "warn" for s, _ in warns)
    errs = P.pedagogy_issues(data, enforce=True)
    assert all(s == "error" for s, _ in errs)

def test_pedagogy_profile_unknown_is_warn():
    data = {"meta": {"pedagogy_profile": "nonsense"}, "scenes": []}
    out = P.pedagogy_issues(data, enforce=True)   # even enforced, profile note stays warn
    assert any(s == "warn" and "pedagogy_profile" in m for s, m in out)
```

And call both in `__main__`.

- [ ] **Step 2: Run to verify it fails**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_pedagogy.py`
Expected: FAIL — `AttributeError: ... 'pedagogy_issues'`.

- [ ] **Step 3: Implement `pedagogy_issues`**

Append to `pedagogy.py`:

```python
_PROFILES = frozenset({"first_time", "review", "expert"})
_MOTIVE_TEMPLATES = frozenset({"theorem_proof", "derivation"})  # definition_math NOT deterministic (§9.2)


def pedagogy_issues(data: dict, enforce: bool) -> "list[tuple[str, str]]":
    """All PD deterministic findings: PD2 (motive on theorem_proof/derivation),
    PD3 (problem on divider), PD4 (registry), + a pedagogy_profile sanity note.
    severity = 'error' if enforce else 'warn' (profile note is always 'warn')."""
    sev = "error" if enforce else "warn"
    issues: list[tuple[str, str]] = []
    meta = data.get("meta", {}) if isinstance(data, dict) else {}
    prof = meta.get("pedagogy_profile", "first_time")
    if prof not in _PROFILES:
        issues.append(("warn", f"meta.pedagogy_profile {prof!r} unknown "
                               f"(known: {sorted(_PROFILES)}); treated as first_time"))
    for scene in (data.get("scenes") or []):
        if not isinstance(scene, dict):
            continue
        sid = scene.get("id", "?")
        kind = scene.get("kind", "content")
        scaf = scene.get("scaffold") if isinstance(scene.get("scaffold"), dict) else {}
        if kind == "content" and scene.get("template") in _MOTIVE_TEMPLATES:
            if not (isinstance(scaf.get("motive"), str) and scaf["motive"].strip()):
                issues.append((sev, f"{sid}: {scene.get('template')} should carry "
                                    f"scaffold.motive (on-screen 'why we're doing this')"))
        elif kind == "divider":
            if not (isinstance(scaf.get("problem"), str) and scaf["problem"].strip()):
                issues.append((sev, f"{sid}: divider should carry scaffold.problem "
                                    f"(the concrete problem/expression being solved)"))
    issues += assumptions_registry_issues(data, enforce)
    return issues
```

- [ ] **Step 4: Run to verify it passes**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_pedagogy.py`
Expected: `OK pedagogy self-test`

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/pedagogy.py video/pipeline/_selftest_pedagogy.py
git commit -m "feat(pedagogy): PD2/PD3 structural checks + pedagogy_profile validation"
```

---

### Task 3: Wire `pedagogy_issues` into `schema.py` + `make.py` (warn-default, opt-in)

**Files:**
- Modify: `video/pipeline/schema.py` (`main()`, right after Plan 1's `[provenance]` block)
- Modify: `video/make.py` (render gate, right after Plan 1's `[provenance]` block)
- Modify: `video/pipeline/_selftest_pedagogy.py` (end-to-end fixture assertion)
- Create: `video/storyboards/_fixtures/scaffold.yml`

**Interfaces:**
- Consumes: `pedagogy.pedagogy_issues`. Produces: a `[pedagogy]` findings block in both `schema.py` and `make.py`; exit/abort only when `meta.pedagogy_enforce is True` AND there are error-severity findings. Zero behavior change for existing decks.

- [ ] **Step 1: Create the fixture storyboard**

Create `video/storyboards/_fixtures/scaffold.yml`:

```yaml
meta:
  id: _fixture_scaffold
  section: "0.0"
  chapter: "Chapter 3"
  pedagogy_profile: first_time
  assumptions:
    - id: radians
      text: "$\\theta$ in radians (arc length $=\\theta$)"
      first_use_unit: uses_radians
      source: "doc:frag-sec-3-1"
scenes:
  - id: thm_no_motive
    kind: content
    template: theorem_proof
    say: "{show statement}"
    statement: "theorem_proof with no scaffold.motive -> PD2 finding"
  - id: uses_radians
    kind: content
    template: derivation
    scaffold: { motive: "set up the squeeze", flag: radians }
    say: "{show statement}"
    statement: "has motive + first-use flag for radians"
  - id: div_no_problem
    kind: divider
    say: ""
```

(Exercises: PD2 missing motive on `thm_no_motive`; PD3 missing problem on `div_no_problem`; a satisfied registry — `radians` first-used in `uses_radians`, which carries `scaffold.flag: radians`.)

- [ ] **Step 2: Add the end-to-end failing assertion**

Append to `_selftest_pedagogy.py`:

```python
def test_schema_integration():
    import subprocess
    py = sys.executable
    repo_root = Path(__file__).resolve().parent.parent.parent
    out = subprocess.run(
        [py, "video/pipeline/schema.py", "video/storyboards/_fixtures/scaffold.yml"],
        capture_output=True, text=True, cwd=repo_root)
    assert out.returncode == 0                       # warn-default never aborts
    assert "[pedagogy]" in out.stdout
    assert "thm_no_motive" in out.stdout             # PD2
    assert "div_no_problem" in out.stdout            # PD3
    assert "uses_radians" not in out.stdout          # satisfied -> no finding
```

And call it in `__main__`.

- [ ] **Step 3: Run to verify it fails**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_pedagogy.py`
Expected: FAIL — assertion `"[pedagogy]" in out.stdout` (schema.py doesn't print it yet).

- [ ] **Step 4: Wire into `schema.py`**

In `schema.py` `main()`, immediately AFTER Plan 1's `[provenance]` block (the `if prov:` block) and BEFORE the `--list` block, insert (reuses the existing `meta` and `errors` already in scope):

```python
    # Pedagogy structural checks (warn-default; gates only when meta.pedagogy_enforce is True)
    from pipeline import pedagogy as _ped
    ped_enforce = bool(meta.get("pedagogy_enforce"))
    ped = _ped.pedagogy_issues(data, enforce=ped_enforce)
    if ped:
        ped_err = sum(1 for s, _ in ped if s == "error")
        print(f"[pedagogy] {args.storyboard.name}: {len(ped)} finding(s)"
              f"{' (ENFORCED)' if ped_enforce else ' (warn-only; set meta.pedagogy_enforce to gate)'}")
        for sev, msg in ped:
            print(f"  {'ERROR' if sev == 'error' else 'WARN '}  {msg}")
        if ped_err:
            errors = errors + [m for s, m in ped if s == "error"]
```

- [ ] **Step 5: Wire into `make.py`**

In `make.py` `main()`, immediately AFTER Plan 1's `[provenance]` block and BEFORE the lint gate, insert (reuses the `_meta` already computed by Plan 1's provenance block; `Path` is imported at module top):

```python
    # Pedagogy structural checks (warn-default; gates only when meta.pedagogy_enforce is True)
    from pipeline import pedagogy as _ped
    _ped_enforce = bool(_meta.get("pedagogy_enforce"))
    _ped_issues = _ped.pedagogy_issues(data, enforce=_ped_enforce)
    if _ped_issues:
        _ped_err = sum(1 for s, _ in _ped_issues if s == "error")
        print(f"[pedagogy] {len(_ped_issues)} finding(s)"
              f"{' (ENFORCED)' if _ped_enforce else ' (warn-only; set meta.pedagogy_enforce to gate)'}", flush=True)
        for _sev, _msg in _ped_issues:
            print(f"  {'ERROR' if _sev == 'error' else 'WARN '}  {_msg}", flush=True)
        if _ped_err:
            print(f"[pedagogy] {_ped_err} error(s) -- aborting (fix scaffold/registry or unset meta.pedagogy_enforce):", flush=True)
            return 2
```

- [ ] **Step 6: Run the self-test (incl. integration) to verify it passes**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_pedagogy.py`
Expected: `OK pedagogy self-test`

- [ ] **Step 7: Regression — existing decks unaffected (zero behavior change)**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/schema.py video/storyboards/ch03_trig_derivatives.yml`
Expected: **exit 0**; existing `[schema] ... structure OK`; the Plan 1 `[provenance] ... (warn-only ...)` block; and a new `[pedagogy] ... (warn-only ...)` block (ch03 isn't migrated, so PD2/PD3 will warn) — but **exit code 0**.

- [ ] **Step 8: Commit**

```bash
git add video/pipeline/schema.py video/make.py video/pipeline/_selftest_pedagogy.py video/storyboards/_fixtures/scaffold.yml
git commit -m "feat(pedagogy): wire PD checks into schema.py + make.py (warn-default, opt-in)"
```

---

### Task 4: `render_scaffold()` helper in `_common.py`

**Files:**
- Modify: `video/pipeline/templates/_common.py`

**Interfaces:**
- Produces: `render_scaffold(scaffold, ground, meta=None) -> list[Block]` — returns Block(s) for present scaffold fields, `[]` when scaffold absent/empty/non-dict. `motive` → small `text`/`prose_sm` line (id `"scaffold.motive"`); `problem` → `text`/`prose` formula-capable block (id `"scaffold.problem"`); `flag` → `build_aside`-style badge with the assumption's text looked up from `meta.assumptions` (id `"scaffold.flag.<id>"`). All Blocks `anim="fade", static=True, layer="content"`. Helper `_assumption_text(meta, flag_id) -> str | None`.

> **Note (rendering, not pure logic):** this builds manim mobjects, so the self-test verifies it the way Plan 1 Task 2 verified `from_deck` — a one-off **bootstrap'd** structural check (NOT added to a pure self-test): confirm `render_scaffold(None,...) == []`, `render_scaffold({"motive":"x"},...)` returns one Block whose `id == "scaffold.motive"`, and a `flag` looks up its assumption text. Final visual correctness is verified in Task 5's mock render.

- [ ] **Step 1: Implement `render_scaffold` + `_assumption_text`**

Append to `_common.py` (use the module's existing `brand`, `Block`, `build_aside`, and Lectern widths `PRIMARY_W`/`CONTENT_W`/`RAIL_W` — confirm the exact import names already present in the file and match them):

```python
def _assumption_text(meta, flag_id):
    """The human text for an assumption id, from meta.assumptions; None if absent."""
    for a in (meta or {}).get("assumptions", []) or []:
        if isinstance(a, dict) and a.get("id") == flag_id:
            return a.get("text")
    return None


def render_scaffold(scaffold, ground, meta=None):
    """Render optional scaffold (motive / divider-problem / first-use flag) as static
    Block(s). Returns [] when scaffold is absent/empty (no-op -> render unchanged).
    motive/problem use role='text' (NEVER 'muted'); flag shows the assumption text."""
    if not isinstance(scaffold, dict):
        return []
    out = []
    motive = scaffold.get("motive")
    if isinstance(motive, str) and motive.strip():
        mob = brand.prose(motive, ground, role="text", size="prose_sm",
                          max_width=PRIMARY_W, align="LEFT")
        out.append(Block("scaffold.motive", mob, anim="fade", static=True, layer="content"))
    problem = scaffold.get("problem")
    if isinstance(problem, str) and problem.strip():
        mob = brand.prose(problem, ground, role="text", size="prose",
                          max_width=CONTENT_W, align="LEFT")
        out.append(Block("scaffold.problem", mob, anim="fade", static=True, layer="content"))
    flag = scaffold.get("flag")
    if isinstance(flag, str) and flag.strip():
        body = _assumption_text(meta, flag) or flag
        mob = build_aside({"label": "assumes", "body": body}, ground, max_width=RAIL_W)
        out.append(Block(f"scaffold.flag.{flag}", mob, anim="fade", static=True, layer="content"))
    return out
```

- [ ] **Step 2: Verify (one-off bootstrap'd structural check)**

Run a one-off check (a `python -c` or scratch script under the scratchpad; mirrors Task 5's render env via `_bootstrap`). Do NOT add it to a pure self-test (keeps logic self-tests bootstrap-free):

```python
import sys; sys.path.insert(0, 'video')
from pipeline import _bootstrap; _bootstrap.bootstrap()
from pipeline.templates._common import render_scaffold
assert render_scaffold(None, "dark") == []
assert render_scaffold({}, "dark") == []
bs = render_scaffold({"motive": "why"}, "dark")
assert len(bs) == 1 and bs[0].id == "scaffold.motive"
bs2 = render_scaffold({"flag": "radians"}, "dark", {"assumptions": [{"id": "radians", "text": "T"}]})
assert bs2[0].id == "scaffold.flag.radians"
print("render_scaffold OK")
```
Expected: `render_scaffold OK`.

- [ ] **Step 3: Commit**

```bash
git add video/pipeline/templates/_common.py
git commit -m "feat(scaffold): render_scaffold helper (motive/problem/flag -> static Blocks)"
```

---

### Task 5: Template wiring + mock-render visual gate + sign-off

**Files:**
- Modify: `video/pipeline/templates/definition_math.py`, `theorem_proof.py`, `derivation.py`, `divider.py`

**Interfaces:**
- Consumes: `_common.render_scaffold`. Each content/divider template, after `scene_head()` (title at `head[1].mobject`), calls `render_scaffold(spec.get("scaffold"), ctx["ground"], ctx.get("meta"))`, positions the returned motive/problem mobject(s) directly under the title (`.next_to(title, DOWN, buff=...).align_to(title, LEFT)` on the Lectern spine), pushes its main body content down to clear them, and appends the Block(s) to its returned list. **Absent scaffold → `render_scaffold` returns `[]` → zero layout change (no-op).** `definition_math`/`theorem_proof`/`derivation` consume `motive` (+ optional `flag`); `divider` consumes `problem` (+ optional `flag`); the existing `subtitle` stays as brand text.

> This is rendering work: each template's exact insertion line is in the Plan 2 architecture map (definition_math after the `head`/title at ~line 80; theorem_proof after the statement card ~line 65; derivation after statement ~line 152; divider after subtitle positioning ~line 75). The implementer reads each file and inserts the call + positioning, tuning buffs against the mock render. Keep changes surgical and no-op when scaffold absent.

- [ ] **Step 1: Wire each template (definition_math, theorem_proof, derivation → motive/flag; divider → problem/flag)**

Pattern per template (adapt to each file's variable names + layout; the title mobject comes from `scene_head`/`example_head`):

```python
    # after scene_head(...) and obtaining `title` (e.g. head[1].mobject):
    scaffold_blocks = render_scaffold(spec.get("scaffold"), ctx["ground"], ctx.get("meta"))
    for sb in scaffold_blocks:
        sb.mobject.next_to(title, DOWN, buff=T.TITLE_GAP).align_to(title, LEFT)
        title = sb.mobject   # chain: next scaffold line / body sits below this one
    blocks += scaffold_blocks
    # ... then position the template's main content below `title` as before ...
```

(Import `render_scaffold` from `._common`. For `divider`, position `scaffold.problem` under the title and keep `subtitle` as-is per the brand layout.)

- [ ] **Step 2: Verify the render is clean (offline mock render + gates)**

Run a mock render of the scaffold fixture (offline, free):
`C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/make.py --storyboard video/storyboards/_fixtures/scaffold.yml --backend mock --quality low`
Expected: schema OK; `[provenance]`/`[pedagogy]` warn-only blocks; **lint clean; sizecheck 0 error (NO muted-prose warning on the scaffold lines)**; scenes render. (If the minimal fixture can't fully render, mock-render one real ch03 scene with a temporary `scaffold.motive` added to a scratch copy — never edit a locked deck — to get a real-template frame.)

- [ ] **Step 3: Visual gate — extract frames and audit**

Extract frames (`critic.py --dry-run` after clearing `output/<...>/critic/frames/`, or `scratch_frames.py --scene <id>`), then dispatch the **visual-frame-audit** gate-1 agent on the scaffold frames (V1–V9 + A1–A7): confirm motive reads as a small line under the title (not muted, legible), divider problem reads as a formula block, the flag badge is legible. Fix any blocking finding and re-render. Record results.

- [ ] **Step 4: User sign-off**

Present the rendered scaffold frames (per the project's visual sign-off culture, as with hook animations). Get the user's sign-off on the scaffold appearance before considering Task 5 done.

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/templates/definition_math.py video/pipeline/templates/theorem_proof.py video/pipeline/templates/derivation.py video/pipeline/templates/divider.py
git commit -m "feat(scaffold): render scaffold.motive/problem/flag in content + divider templates"
```

---

## After Plan 2 lands

- Re-confirm zero behavior change: existing decks (ch01 §1.1, ch03 §3.1/§3.2) still `make.py` mock-render to exit 0 (now with warn-only `[pedagogy]` blocks).
- **Plan 3 — Pedagogy gate:** `PEDAGOGY-FIRSTLEARNER-RUBRIC.md` (PD1–PD4 + OF1–OF2) + `pedagogy-firstlearner-audit` gate-1 agent (reads storyboard+.md+handout); OF1 source-adequacy; `CONTENT_APPROVED` lifecycle gating; separate PD/OF blocking counts. (The gate-1 agent reads `meta.pedagogy_profile` directly.)
- **Plan 4 — Visual extension:** A7 figure-prominence sub-criterion, V4/A6 min-size floor in `theme.py`/`sizecheck.py`, mobile yardstick.
- **Plan 5 — Methodology/doc wiring:** `CONTENT_METHODOLOGY.md` (P1/P2/P4 + scaffold authoring), `DESIGN.md` (scaffold承載 + authoring checklist), L1 scaffold exception in `CONTENT-SIXLENS-RUBRIC.md`, `REVIEW_GATES.md` (new gate in sequence), V1-V8→V1-V9 doc-drift.
- **SP2 backfill** then applies Plans 1–4 to the 3 locked decks per spec §11.

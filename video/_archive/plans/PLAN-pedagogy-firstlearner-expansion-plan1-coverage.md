> **Status: archived / completed（2026-07-07 歸檔）** — 本計畫已全數落地（執行紀錄見 `video/_archive/REBUILD_LOG-2026-05-to-07.md` 對應節）。活的權威見 `video/REVIEW_GATES.md`／`video/DESIGN.md`／`video/SPEC-pedagogy-firstlearner-*.md`。本檔為歷史施工紀錄，內含相對路徑可能已過時。

# Expansion Layer — SC Deterministic Foundation (Plan 1 of 4)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the deterministic backbone for M1 step-coverage — a shared `screen_contract` parser, the `.md`/storyboard wiring, and a warn-only `coverage.py` check (SC1 missing step / SC2 missing recap) — so the gate-1 SC codes (Plan 2) can rely on "every declared load-bearing step is covered on screen or the deck is told."

**Architecture:** A new stdlib-only module `video/pipeline/_screen_contract.py` parses the `screen_contract` fenced block (yaml, no manim/TeX bootstrap) and is imported by BOTH content-script parsers (`review_pack.py`, `narration_review.py` — they are re-implemented mirrors kept in sync). A second new module `video/pipeline/coverage.py` computes SC1/SC2 per `.md` unit against the union of storyboard scene `covers:`. `schema.py` calls it warn-only, gating only when a deck sets `meta.coverage_enforce: true`.

**Tech Stack:** Python 3.12 (stdlib + `pyyaml`, already a dep via `_bootstrap`). The venv python is `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe`. Tests are stdlib `assert` self-test scripts (project has no pytest — do not add it).

## Global Constraints

- **Spec authority:** `video/SPEC-pedagogy-firstlearner-expansion.md` (v1, Codex R1→R3 converged). This plan implements its §4 (M1) deterministic layer + §7 only. Gate-1 SC codes = Plan 2; AMP = Plan 3; docs/calibration = Plan 4.
- **No new dependency.** stdlib + existing `yaml`. Tests are stdlib `assert` scripts run via the venv python. Do not add pytest.
- **Warn-default, per-deck opt-in.** Every new finding is `warn` unless `meta.coverage_enforce is True`; then `error`. Landing must not fail any existing deck (zero behavior change — no deck sets the flag, no `.md` has a `screen_contract`).
- **No scalar shape change.** `covers:` is a NEW scene-level sibling list; `screen_contract` is a NEW `.md` unit field. Never wrap `proof:`/`steps:`/`statement` into objects. Absent `screen_contract`/`covers` ⇒ no-op. (Spec §9.5 back-compat.)
- **Shared parser, kept in sync (Codex R2).** `screen_contract` structured parsing lives in ONE stdlib helper imported by both `review_pack.py` and `narration_review.py`; both parsers get a regression test with a `screen_contract`-bearing `.md`. Must NOT break freeform `source:` values (which trip strict YAML — the reason the `.md` uses a line parser).
- **Offline, zero-API.** Pure local file reads. No model calls.
- **Surgical.** Follow existing `pipeline/` style (`from __future__ import annotations`, `(severity, message)` tuples, module docstring). Touch only the files named per task.

## Contract grammar (LOCKED by this plan — review here first)

**`.md` unit** (inside the unit's fenced block) MAY carry a `screen_contract` block scalar:
```
screen_contract: |
  required_steps:
    - id: def
      tex: "\\frac{d}{dx}\\sin x=\\lim_{h\\to0}\\frac{\\sin(x+h)-\\sin x}{h}"
      reason: "定義"
    - id: reduced
      tex: "=\\lim_{h\\to0}\\cos(x+\\tfrac h2)\\frac{\\sin(h/2)}{h/2}"
      depends_on: difference_quotient_for_sine.result
      recap_required: true
```
or, to opt a scoped proof/derivation unit OUT of the requirement: `screen_contract: |` + `coverage_exempt: true`.

**storyboard scene** MAY carry a scene-level `covers: [id, ...]` (sibling to `proof:`/`steps:`), listing ids of ITS OWN `ref:`-ed unit's `required_steps` (cross-unit deps go in the contract's `depends_on`, never in `covers:`).

**must-show** = a `required_step` UNLESS it has `depends_on` and NOT `recap_required` (a pure back-reference).
**SC1** = a must-show id not in the union of `covers:` across all scenes `ref:`-ing that unit. **SC2** = a `recap_required` id not in that union (a distinctly-labelled must-show subcase). **Orphan** = a `covers:` id not in the unit's `required_steps`.

---

## File Structure

- **Create** `video/pipeline/_screen_contract.py` — parse one `screen_contract` block scalar → dict; expose `must_show()` / step accessors. Stdlib + yaml only, NO bootstrap (safe for both parsers to import).
- **Create** `video/pipeline/coverage.py` — `coverage_issues(storyboard, contracts, enforce)` → `[(sev,msg)]` (SC1/SC2/orphan/missing-contract-under-enforce). Stdlib + `provenance.parse_ref`.
- **Create** `video/pipeline/_selftest_coverage.py` — the plan's self-test (run via venv python).
- **Create** `video/storyboards/_fixtures/sc_coverage.yml` + `video/content_scripts/_fixtures/sc_coverage.md` — tiny fixtures exercising covered/missing/recap/merged/exempt.
- **Modify** `video/pipeline/review_pack.py` — seed + parse `screen_contract` via the shared helper (no flatten).
- **Modify** `video/pipeline/narration_review.py` — keep-in-sync: verified to ignore the block; add regression test.
- **Modify** `video/pipeline/schema.py` — call `coverage.coverage_issues(...)` warn-only (gate on `meta.coverage_enforce`).

---

### Task 1: Shared `screen_contract` parser helper

**Files:**
- Create: `video/pipeline/_screen_contract.py`
- Create: `video/pipeline/_selftest_coverage.py`

**Interfaces:**
- Produces: `parse_block(lines: list[str]) -> dict | None` (dedent collected block-scalar lines, `yaml.safe_load`; malformed/empty → `None`, fail-closed); `required_steps(contract: dict | None) -> list[dict]`; `is_exempt(contract: dict | None) -> bool`; `must_show(contract) -> list[dict]` (excludes `depends_on`-without-`recap_required`).

- [ ] **Step 1: Write the failing self-test**

Create `video/pipeline/_selftest_coverage.py`:
```python
"""Stdlib assert self-test for _screen_contract.py + coverage.py.
Run: C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_coverage.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import _screen_contract as SC  # noqa: E402


def test_parse_block():
    lines = [
        "  required_steps:",
        "    - id: def",
        "      tex: \"a=b\"",
        "    - id: reduced",
        "      depends_on: other.result",
        "      recap_required: true",
    ]
    c = SC.parse_block(lines)
    assert [s["id"] for s in SC.required_steps(c)] == ["def", "reduced"]
    assert SC.is_exempt(c) is False
    # must_show excludes pure back-refs (depends_on & not recap_required)
    assert [s["id"] for s in SC.must_show(c)] == ["def", "reduced"]  # reduced has recap_required
    lines2 = lines + []  # a pure back-ref is dropped from must_show
    c2 = SC.parse_block(["  required_steps:", "    - id: x", "      depends_on: y.z"])
    assert [s["id"] for s in SC.must_show(c2)] == []
    # exemption
    assert SC.is_exempt(SC.parse_block(["  coverage_exempt: true"])) is True
    # fail-closed
    assert SC.parse_block(["  : : not yaml ["]) is None or isinstance(SC.parse_block(["x"]), (dict, type(None)))
    assert SC.required_steps(None) == []


if __name__ == "__main__":
    test_parse_block()
    print("OK coverage self-test")
```

- [ ] **Step 2: Run it to verify it fails**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_coverage.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'pipeline._screen_contract'`.

- [ ] **Step 3: Write `_screen_contract.py`**

Create `video/pipeline/_screen_contract.py`:
```python
"""_screen_contract.py -- parse one `.md` unit's `screen_contract` block scalar.
Pure stdlib + yaml; NO manim/TeX bootstrap, so both content-script parsers
(review_pack, narration_review -- kept in sync) can import it safely.

A screen_contract is:
  required_steps:
    - {id, tex, reason?, depends_on?, recap_required?}
  coverage_exempt: true   # OR this, to opt a scoped proof/derivation unit out
"""
from __future__ import annotations

import textwrap
import yaml


def parse_block(lines: "list[str]") -> "dict | None":
    """Collected block-scalar lines (as captured by the .md parser, 2-space
    indented) -> dict. Dedent, yaml.safe_load. Malformed/empty -> None (fail-closed)."""
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
    return [s for s in steps if isinstance(s, dict) and s.get("id")] if isinstance(steps, list) else []


def is_exempt(contract: "dict | None") -> bool:
    return bool(isinstance(contract, dict) and contract.get("coverage_exempt") is True)


def must_show(contract: "dict | None") -> "list[dict]":
    """required_steps minus pure back-references (has depends_on, no recap_required)."""
    out = []
    for s in required_steps(contract):
        if s.get("depends_on") and not s.get("recap_required"):
            continue
        out.append(s)
    return out
```

- [ ] **Step 4: Run it to verify it passes**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_coverage.py`
Expected: `OK coverage self-test`

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/_screen_contract.py video/pipeline/_selftest_coverage.py
git commit -m "feat(sc): shared screen_contract block parser (stdlib, no bootstrap)"
```

---

### Task 2: Wire `screen_contract` into both `.md` parsers (kept in sync)

**Files:**
- Modify: `video/pipeline/review_pack.py` (`parse_content_script`, ~`:98-162`)
- Modify: `video/pipeline/narration_review.py` (add regression only if needed)
- Modify: `video/pipeline/_selftest_coverage.py`
- Create: `video/content_scripts/_fixtures/sc_coverage.md`

**Interfaces:**
- Produces: `review_pack.parse_content_script(md)` units now carry `screen_contract` = dict|None (parsed via `_screen_contract.parse_block`), without flattening. `narration_review.parse_content_script(md)` still returns correct narration for the same `.md` (ignores the block).

- [ ] **Step 1: Create the fixture `.md`**

Create `video/content_scripts/_fixtures/sc_coverage.md`:
```markdown
### unit: proved_here
```
id: proved_here
source: chapter3-print-standalone.html §X · Some Proof (a:b · em—dash "q")
kind: derivation
narration: |
  A one line narration.
visual_need: |
  a chain.
screen_contract: |
  required_steps:
    - id: def
      tex: "a=b"
      reason: "定義"
    - id: reduced
      tex: "b=c"
      depends_on: elsewhere.result
      recap_required: true
```

## notes
(an h2 ends the unit region)
```

- [ ] **Step 2: Add the failing self-test**

Append to `_selftest_coverage.py` (before `__main__`):
```python
def test_parser_wiring():
    from pipeline import review_pack, narration_review
    md = Path(__file__).resolve().parent.parent / "content_scripts" / "_fixtures" / "sc_coverage.md"
    units = review_pack.parse_content_script(md)["units"]
    u = next(x for x in units if x["id"] == "proved_here")
    assert isinstance(u["screen_contract"], dict)
    assert [s["id"] for s in u["screen_contract"]["required_steps"]] == ["def", "reduced"]
    # freeform source: with :, ·, em-dash, quotes survives (NOT yaml-parsed)
    assert "em—dash" in u["source"] and u["source"].startswith("chapter3")
    # narration_review mirror ignores the block and still returns the narration
    nu = next(x for x in narration_review.parse_content_script(md)["units"] if x["id"] == "proved_here")
    assert nu["narration"].strip() == "A one line narration." and "screen_contract" not in nu
```
And call `test_parser_wiring()` in `__main__`.

- [ ] **Step 3: Run to verify it fails**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_coverage.py`
Expected: FAIL — `KeyError: 'screen_contract'` (review_pack doesn't seed/parse it yet).

- [ ] **Step 4: Wire `review_pack.parse_content_script`**

In `review_pack.py`, add the import near the top (with the other imports):
```python
from pipeline import _screen_contract
```
Seed the key: change `cur = {k: "" for k in _FIELD_KEYS}` (at `:115`) to:
```python
            cur = {k: "" for k in _FIELD_KEYS}
            cur["screen_contract"] = None
```
Change `_commit()` (at `:103-107`) to parse the contract instead of flattening it:
```python
    def _commit() -> None:
        if cur is not None:
            for k, v in cur.items():
                if isinstance(v, list):
                    if k == "screen_contract":
                        cur[k] = _screen_contract.parse_block(v)
                    else:
                        cur[k] = " ".join(s.strip() for s in v).strip()
```
(The `if key not in cur: continue` guard at `:141` now admits `screen_contract` because it is seeded; `val == "|"` collects its block scalar as a list, and `_commit` parses it.)

- [ ] **Step 5: Run to verify it passes (review_pack + narration_review mirror)**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_coverage.py`
Expected: `OK coverage self-test`. (If the `narration_review` assertion fails, the mirror mis-parses the block; add a matching skip: seed `cur["screen_contract"] = None` there too and drop it before returning. If it passes as-is, the mirror already ignores unknown keys — no code change, and the test now LOCKS that.)

- [ ] **Step 6: Regression — real decks still parse**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'video'); from pipeline import _bootstrap; _bootstrap.bootstrap(); from pipeline import review_pack; from pathlib import Path; u=review_pack.parse_content_script(Path('video/content_scripts/ch03_trig_derivatives.md'))['units']; print('units:', len(u), '| screen_contract on each:', all('screen_contract' in x for x in u), '| none set yet:', all(x['screen_contract'] is None for x in u))"`
Expected: nonzero units; `screen_contract on each: True`; `none set yet: True` (no real unit has one — zero behavior change).

- [ ] **Step 7: Commit**

```bash
git add video/pipeline/review_pack.py video/pipeline/narration_review.py video/pipeline/_selftest_coverage.py video/content_scripts/_fixtures/sc_coverage.md
git commit -m "feat(sc): parse screen_contract in both .md parsers (kept in sync, no flatten)"
```

---

### Task 3: `coverage.py` — must-show coverage (SC1) + orphan

**Files:**
- Create: `video/pipeline/coverage.py`
- Modify: `video/pipeline/_selftest_coverage.py`

**Interfaces:**
- Consumes: `_screen_contract.{required_steps,must_show,is_exempt}`, `provenance.parse_ref`.
- Produces: `covers_by_unit(storyboard: dict) -> dict[str, set[str]]` (union of `covers:` per `ref:`-ed unit id); `coverage_issues(storyboard: dict, contracts: dict[str, dict], enforce: bool) -> list[tuple[str, str]]` — here implementing SC1 + orphan (SC2 + missing-contract added in Task 4).

- [ ] **Step 1: Add the failing self-test**

Append to `_selftest_coverage.py`:
```python
def test_sc1_and_orphan():
    from pipeline import coverage
    from pipeline import _screen_contract as SC
    contract = SC.parse_block([
        "  required_steps:",
        "    - id: def",
        "      tex: \"a=b\"",
        "    - id: reduced",
        "      depends_on: e.result",
        "      recap_required: true",
    ])
    contracts = {"u": contract}
    sb_missing = {"scenes": [{"id": "s1", "kind": "content", "ref": "md:u", "covers": ["def"]}]}
    warns = coverage.coverage_issues(sb_missing, contracts, enforce=False)
    msgs = " | ".join(m for _, m in warns)
    assert all(sev == "warn" for sev, _ in warns)
    assert "reduced" in msgs and "u" in msgs        # SC1: reduced (must-show via recap) uncovered
    assert "def" not in msgs.split("reduced")[0]     # def IS covered -> not flagged
    sb_ok = {"scenes": [{"id": "s1", "kind": "content", "ref": "md:u", "covers": ["def", "reduced"]}]}
    assert coverage.coverage_issues(sb_ok, contracts, enforce=False) == []
    sb_orphan = {"scenes": [{"id": "s1", "kind": "content", "ref": "md:u", "covers": ["def", "reduced", "typo"]}]}
    assert any("typo" in m for _, m in coverage.coverage_issues(sb_orphan, contracts, enforce=False))
    errs = coverage.coverage_issues(sb_missing, contracts, enforce=True)
    assert all(sev == "error" for sev, _ in errs)
```
And call it in `__main__`.

- [ ] **Step 2: Run to verify it fails**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_coverage.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'pipeline.coverage'`.

- [ ] **Step 3: Write `coverage.py`**

Create `video/pipeline/coverage.py`:
```python
"""coverage.py -- SC deterministic layer (spec §4): SC1 (a declared must-show
step not covered on screen) + SC2 (a recap_required back-ref not locally
covered) + orphan covers ids + missing-contract-under-enforce. Pure stdlib.
warn-default; severity flips to 'error' under meta.coverage_enforce.
"""
from __future__ import annotations

from pipeline import _screen_contract as _sc
from pipeline.provenance import parse_ref


def covers_by_unit(storyboard: dict) -> "dict[str, set[str]]":
    """Union of scene-level `covers:` grouped by the `md:` unit the scene ref-s."""
    out: dict[str, set[str]] = {}
    for scene in (storyboard.get("scenes") or []):
        if not isinstance(scene, dict):
            continue
        parsed = parse_ref(scene.get("ref", "") if isinstance(scene.get("ref"), str) else "")
        if not parsed or parsed[0] != "md":
            continue
        unit = parsed[1]
        cov = scene.get("covers")
        if isinstance(cov, list):
            out.setdefault(unit, set()).update(c for c in cov if isinstance(c, str))
    return out


def coverage_issues(storyboard: dict, contracts: "dict[str, dict]", enforce: bool) -> "list[tuple[str, str]]":
    """(severity, message) for SC1 (missing must-show) + orphan covers ids.
    SC2 + missing-contract-under-enforce are layered in Task 4."""
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
            if s["id"] not in C:
                issues.append((sev, f"[SC1] {unit_id}.{s['id']}: required on-screen step "
                                    f"not covered by any scene's covers: — {s.get('tex','')!r}"))
    return issues
```

- [ ] **Step 4: Run to verify it passes**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_coverage.py`
Expected: `OK coverage self-test`

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/coverage.py video/pipeline/_selftest_coverage.py
git commit -m "feat(sc): coverage.py SC1 must-show coverage + orphan covers ids"
```

---

### Task 4: `coverage.py` — SC2 recap + missing-contract-under-enforce

**Files:**
- Modify: `video/pipeline/coverage.py`
- Modify: `video/pipeline/_selftest_coverage.py`

**Interfaces:**
- Produces: `coverage_issues(...)` now also emits SC2 (a `recap_required` id not covered, distinct message) and, when `enforce` is True, an error for each storyboard scene whose `template` is `theorem_proof`/`derivation` and whose `ref:`-ed unit has NO contract and is not exempt.

- [ ] **Step 1: Add the failing self-test**

Append to `_selftest_coverage.py`:
```python
def test_sc2_and_missing_contract():
    from pipeline import coverage
    from pipeline import _screen_contract as SC
    contract = SC.parse_block([
        "  required_steps:",
        "    - id: reduced",
        "      depends_on: e.result",
        "      recap_required: true",
    ])
    sb = {"scenes": [{"id": "s1", "kind": "content", "ref": "md:u", "covers": []}]}
    msgs = " | ".join(m for _, m in coverage.coverage_issues(sb, {"u": contract}, enforce=False))
    assert "[SC2]" in msgs and "reduced" in msgs      # recap_required, uncovered -> SC2
    # missing contract on a proof/derivation scene, enforce=True -> error
    sb2 = {"scenes": [{"id": "p", "kind": "content", "template": "theorem_proof",
                       "ref": "md:nocontract", "covers": []}]}
    errs = coverage.coverage_issues(sb2, {}, enforce=True)
    assert any(sev == "error" and "nocontract" in m and "screen_contract" in m for sev, m in errs)
    # same, enforce=False -> no missing-contract finding (warn-default zero-noise)
    assert not any("screen_contract" in m for _, m in coverage.coverage_issues(sb2, {}, enforce=False))
    # exempt unit -> no missing-contract error even under enforce
    from pipeline import _screen_contract as SC2m
    exempt = {"nocontract": SC2m.parse_block(["  coverage_exempt: true"])}
    assert not any("nocontract" in m for _, m in coverage.coverage_issues(sb2, exempt, enforce=True))
```
And call it in `__main__`.

- [ ] **Step 2: Run to verify it fails**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_coverage.py`
Expected: FAIL — no `[SC2]` in output / no missing-contract error.

- [ ] **Step 3: Extend `coverage_issues`**

In `coverage.py`, add the SC2 loop inside the `for unit_id, contract` loop (after the SC1 loop), and add a missing-contract pass. Replace the `coverage_issues` body's tail:
```python
        for s in _sc.must_show(contract):
            if s["id"] not in C:
                issues.append((sev, f"[SC1] {unit_id}.{s['id']}: required on-screen step "
                                    f"not covered by any scene's covers: — {s.get('tex','')!r}"))
        for s in _sc.required_steps(contract):
            if s.get("recap_required") and s["id"] not in C:
                issues.append((sev, f"[SC2] {unit_id}.{s['id']}: cash-in result (recap_required) "
                                    f"not re-shown locally — {s.get('tex','')!r}"))
    if enforce:
        _SCOPED = {"theorem_proof", "derivation"}
        for scene in (storyboard.get("scenes") or []):
            if not isinstance(scene, dict) or scene.get("template") not in _SCOPED:
                continue
            parsed = parse_ref(scene.get("ref", "") if isinstance(scene.get("ref"), str) else "")
            if not parsed or parsed[0] != "md":
                continue
            unit = parsed[1]
            c = contracts.get(unit)
            if c is None or (not _sc.required_steps(c) and not _sc.is_exempt(c)):
                issues.append(("error", f"[SC] {unit}: proof/derivation unit under coverage_enforce "
                                        f"has no screen_contract (add required_steps or coverage_exempt: true)"))
    return issues
```
(Keep the SC1 loop; the SC2 loop is added right after it. Dedup missing-contract per unit is unnecessary at this scale; if noisy, collect `unit`s in a set first.)

- [ ] **Step 4: Run to verify it passes**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_coverage.py`
Expected: `OK coverage self-test`

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/coverage.py video/pipeline/_selftest_coverage.py
git commit -m "feat(sc): SC2 recap + missing-contract-under-enforce"
```

---

### Task 5: Wire into `schema.py` (warn-only; gate on `meta.coverage_enforce`)

**Files:**
- Modify: `video/pipeline/schema.py` (`main()`, after the existing `[provenance]` block)
- Modify: `video/pipeline/_selftest_coverage.py`
- Create: `video/storyboards/_fixtures/sc_coverage.yml`

**Interfaces:**
- Consumes: `coverage.coverage_issues`, `review_pack.parse_content_script`, `provenance.Loci` deck→md mapping (reuse `meta.id` → `content_scripts/<id>.md`).
- Produces: `schema.py` prints a `[coverage]` block; exit stays 0 unless `meta.coverage_enforce is True` AND there is an unresolved must-show/contract. Zero behavior change for existing decks.

- [ ] **Step 1: Create the fixture storyboard**

Create `video/storyboards/_fixtures/sc_coverage.yml`:
```yaml
meta: { id: _fixture_sc, section: "0.0", chapter: "Chapter 3" }
scenes:
  - id: s_ok
    kind: content
    template: derivation
    ref: md:proved_here
    covers: [def, reduced]
    say: "{show statement}"
    statement: "covered"
  - id: s_missing
    kind: content
    template: theorem_proof
    ref: md:proved_here
    covers: [def]          # reduced (recap_required) left uncovered -> SC1+SC2 warn
    say: "{show statement}"
    statement: "partial"
```
(Its `.md` is the Task-2 fixture; but `schema.py` maps `meta.id` → `content_scripts/_fixture_sc.md`. Create that alias file next.)

- [ ] **Step 2: Create the deck `.md` the fixture maps to**

Create `video/content_scripts/_fixture_sc.md` with the SAME unit as Task 2's fixture (id `proved_here`, with the `screen_contract`). (A separate file because `schema.py` resolves `<meta.id>.md`; keep it minimal — copy the `### unit: proved_here` block from `_fixtures/sc_coverage.md`.)

- [ ] **Step 3: Add the end-to-end failing assertion**

Append to `_selftest_coverage.py`:
```python
def test_schema_integration():
    import subprocess
    py = sys.executable
    out = subprocess.run(
        [py, "video/pipeline/schema.py", "video/storyboards/_fixtures/sc_coverage.yml"],
        capture_output=True, text=True)
    assert out.returncode == 0                    # warn-default never aborts
    assert "[coverage]" in out.stdout
    assert "reduced" in out.stdout                # SC1/SC2 surfaced as warn
```
And call it in `__main__`.

- [ ] **Step 4: Run to verify it fails**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_coverage.py`
Expected: FAIL — `"[coverage]" in out.stdout` (schema.py doesn't print it yet).

- [ ] **Step 5: Wire the check into `schema.py`**

In `schema.py` `main()`, immediately after the existing `[provenance]` block (before `--list` / the final return), insert:
```python
    # SC coverage (warn-default; gates only when meta.coverage_enforce is True)
    from pipeline import coverage as _cov
    from pipeline import review_pack as _rp
    cov_enforce = bool(meta.get("coverage_enforce"))
    deck_md = repo_root / "video" / "content_scripts" / f"{meta.get('id','')}.md"
    contracts = {}
    if deck_md.exists():
        try:
            for u in _rp.parse_content_script(deck_md).get("units", []):
                if u.get("id") and u.get("screen_contract"):
                    contracts[u["id"]] = u["screen_contract"]
        except Exception:
            contracts = {}     # fail-closed: unreadable .md -> no contracts -> no SC noise
    cov_issues = _cov.coverage_issues(data, contracts, enforce=cov_enforce)
    if cov_issues:
        print(f"[coverage] {args.storyboard.name}: {len(cov_issues)} finding(s)"
              f"{' (ENFORCED)' if cov_enforce else ' (warn-only; set meta.coverage_enforce to gate)'}")
        for sev, msg in cov_issues:
            print(f"  {'ERROR' if sev == 'error' else 'WARN '}  {msg}")
        if cov_enforce:
            errors = errors + [m for s, m in cov_issues if s == "error"]
```
(`repo_root`, `meta`, `errors` already exist in `main()` from the `[provenance]` block wired in the OTF plan; reuse them. The final `return 1 if errors else 0` then gates on enforced coverage errors too.)

- [ ] **Step 6: Run the self-test (incl. integration) to verify it passes**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_coverage.py`
Expected: `OK coverage self-test`

- [ ] **Step 7: Regression — existing decks unaffected (zero behavior change)**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/schema.py video/storyboards/ch03_trig_derivatives.yml`
Expected: exit 0; existing `[schema]`/`[provenance]` output; **no `[coverage]` block** (no unit has a `screen_contract` yet → `contracts` empty → no findings). Exit code 0.

- [ ] **Step 8: Commit**

```bash
git add video/pipeline/schema.py video/pipeline/_selftest_coverage.py video/storyboards/_fixtures/sc_coverage.yml video/content_scripts/_fixture_sc.md
git commit -m "feat(sc): wire coverage.py into schema.py (warn-default, opt-in gating)"
```

---

## Plans 2–4 (to detail after Plan 1 lands + the grammar is exercised)

- **Plan 2 — SC gate-1 codes:** extend `PEDAGOGY-FIRSTLEARNER-RUBRIC.md` with the SC family (SC1/SC2 surfaced as `[Surface SC1-det|SC2-det]`; SC-adv suspected-over-merge-vs-handout advisory; SC-honesty evidence-based, cite `proof.N`/`statement`/`qed`, mandatory before `coverage_enforce` sign-off); extend the `pedagogy-firstlearner-audit` agent to load `screen_contract`, surface SC1/SC2, own SC-adv/SC-honesty; VERDICT line → `<P> PD, <O> OF, <S> SC, <A> advisory` (S = SC-honesty only). Spec §4.2/§9.
- **Plan 3 — M2 AMP:** new `video-amplification-audit` agent + `AMPLIFICATION-RUBRIC.md` (AMP1); enumerate handout `expansion:intuition`/`application`, classify screened/narration-only/visual-only/missing, propose only `missing`; route correctness `expansion:caution` to assumptions. Spec §5.
- **Plan 4 — Docs + §3.1 calibration:** `CONTENT_METHODOLOGY.md` (screen_contract authoring, covers, merge-not-drop, caution→assumption), `DESIGN.md` (covers), `REVIEW_GATES.md` (SC + AMP in sequence); then author `screen_contract` + `covers:` for `derivative_of_sine`/`difference_quotient_for_sine`, dry-run SC to confirm it flags the dropped `def` line + the `reduced` recap, tune, then per-deck opt-in. Spec §10.

> SP2-style backfill of other locked decks follows per spec §11. Billing steps (real TTS / hi-res render) stay consent-gated.

## Self-Review (against spec §4/§7/§9)

- **Spec coverage:** SC1 (Task 3) ✓; SC2 (Task 4) ✓; orphan (Task 3) ✓; missing-contract-under-enforce + `coverage_exempt` (Task 4) ✓; shared parser + both-parsers-in-sync + freeform `source:` intact (Task 2) ✓; warn-default/opt-in + zero-behavior-change (Tasks 4/5, regression steps) ✓; scalar back-compat (`covers`/`screen_contract` are new siblings; absent ⇒ no-op — Tasks 2/5 regression) ✓. SC-honesty/SC-adv/VERDICT are **Plan 2** (gate-1), correctly deferred. AMP is **Plan 3**.
- **Placeholder scan:** none — every step has runnable code/commands + expected output.
- **Type consistency:** `parse_block`/`required_steps`/`must_show`/`is_exempt` (Task 1) used verbatim in Tasks 3–4; `coverage_issues(storyboard, contracts, enforce)` signature stable Tasks 3→5; `covers_by_unit` internal. `parse_ref` from `provenance` returns `(scheme, token)|None` (matches its Plan-1-OTF definition).

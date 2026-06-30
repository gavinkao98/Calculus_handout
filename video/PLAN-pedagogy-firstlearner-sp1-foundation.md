# OTF Provenance Foundation — Implementation Plan (SP1, Plan 1 of 5)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the deterministic provenance backbone for OTF — a ref grammar, a `.md`/handout locus loader, a resolver, and a warn-only storyboard provenance check — so later plans (scaffold, gate, visual) can rely on "every on-screen teaching-text field traces to a resolvable approved source."

**Architecture:** One new stdlib-only module `video/pipeline/provenance.py` holds the grammar primitives, the locus loader (reusing `review_pack.parse_content_script` for `.md` unit ids + a regex scan of the handout HTML for anchors), the inheritance resolver, and the check function. `schema.py` calls the check as **warn-only** (gating only when a deck sets `meta.otf_enforce: true`). No scalar storyboard field changes; absent provenance = no-op.

**Tech Stack:** Python 3.12 (stdlib only — `re`, `pathlib`), the existing `video/pipeline/` package, `pyyaml` (already a dep, loaded via `_bootstrap`). Validation by plain-`assert` self-test scripts run with the repo venv python.

## Global Constraints

- **Spec authority:** `video/SPEC-pedagogy-firstlearner-framework.md` (v3, SHIP). This plan implements its §5/§9 deterministic layer only.
- **No new dependency.** Project has no pytest; tests are stdlib `assert` scripts run via `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe`. Do not add pytest.
- **Warn-default, per-deck opt-in.** Every new check emits `warn` severity unless `meta.otf_enforce is True`; then `error`. Landing must not fail any existing deck (zero behavior change). (Spec §3 D6, §9 header.)
- **No scalar shape change.** Provenance lives in sibling fields (`ref:` scalar, `refs:` map). Never wrap `statement`/`body`/`reason`/`points[]` into objects. (Spec §9.5, Codex C.)
- **No semantic inference in this layer.** Only check ref *resolution* (token exists). "Is the text faithful to the source" is OF1 (Plan 3, gate-1), out of scope here. (Spec §9.4.)
- **Offline, zero-API.** Pure local file reads. No model calls.
- **Surgical.** Follow existing `pipeline/` style (module docstring, `from __future__ import annotations`, `(severity, message)` tuples). Touch only the files named per task.

## Provenance ref grammar (LOCKED by this plan — review here first)

A **resolvable ref** is a string `"<scheme>:<token>"`:
- `md:<unit_id>` — resolves iff `<unit_id>` is a unit id in the deck's content script `content_scripts/<meta.id>.md` (per `review_pack.parse_content_script`).
- `doc:<anchor>` — resolves iff `<anchor>` is a `frag-sec-*` template id OR a `data-fig` slug in the deck's handout HTML.

Placement (no scalar changes):
- **Scene-level** optional `ref:` (scalar). The existing freeform `source:` is unchanged (human descriptor; never parsed).
- **Field-level** optional `refs:` map `{ <field_path>: <ref> }` (e.g. `refs: {statement: "md:foo", "annotations.0": "doc:frag-sec-3-1"}`). A teaching-text field with no `refs` entry **inherits the scene `ref:`** (Codex B).

Coverage matrix — fields that ARE on-screen teaching text (subject to OTF):
`statement`, `scaffold.motive`, `scaffold.problem`, `problem` (divider), `annotations[]`, callout `body`, `reason` (step/result), recap `points[]`, example `prompt`.
NOT subject (exempt): scene `title`/`eyebrow`/`kicker`/`subtitle` brand text, graph axis/curve `label`s (data-derived), and **hook-rendered text** (→ hook-engineering gate, Plan 3 / spec §5.7).

Scene-kind policy (Codex v3 decision a):
- `kind: content` and `kind: divider` → subject to OTF (divider carries on-screen `problem`).
- `kind: intro` / `kind: outro` → **exempt** (brand/transition text).

Lifecycle (Codex v3 decision d): `md:` refs gate only when the deck `.md` is `CONTENT_APPROVED=yes`; `doc:` refs gate once the anchor resolves (handout = authority). This plan implements *resolution* + warn/opt-in; the approval-gating wire is Plan 3 (gate) — here a `md:` ref to a present unit resolves regardless of approval (approval affects gating, not resolution).

---

## File Structure

- **Create** `video/pipeline/provenance.py` — grammar primitives, locus loader, resolver, check. One responsibility: provenance resolution + the storyboard provenance check.
- **Create** `video/pipeline/_selftest_provenance.py` — stdlib `assert` self-test (the project's first test file; run via venv python).
- **Create** `video/storyboards/_fixtures/otf_provenance.yml` — a tiny fixture storyboard exercising resolvable/unresolvable/inherited/exempt cases.
- **Modify** `video/pipeline/schema.py` — call `provenance.provenance_issues(...)` from `main()` as warn-only (gating only on `meta.otf_enforce`).

---

### Task 1: Grammar primitives — `parse_ref`, coverage matrix, exempt kinds

**Files:**
- Create: `video/pipeline/provenance.py`
- Create: `video/pipeline/_selftest_provenance.py`

**Interfaces:**
- Produces: `parse_ref(s: str) -> tuple[str, str] | None` (returns `(scheme, token)` for `"md:x"`/`"doc:x"`, else `None`); `TEACHING_TEXT_FIELDS: frozenset[str]`; `OTF_EXEMPT_KINDS: frozenset[str]` = `{"intro","outro"}`; `OTF_KINDS: frozenset[str]` = `{"content","divider"}`.

- [ ] **Step 1: Write the failing self-test**

Create `video/pipeline/_selftest_provenance.py`:

```python
"""Stdlib assert self-test for provenance.py. Run: python video/pipeline/_selftest_provenance.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import provenance as P  # noqa: E402


def test_parse_ref():
    assert P.parse_ref("md:why_trig") == ("md", "why_trig")
    assert P.parse_ref("doc:frag-sec-3-1") == ("doc", "frag-sec-3-1")
    assert P.parse_ref("doc:sector-inequality") == ("doc", "sector-inequality")
    assert P.parse_ref("nope:x") is None
    assert P.parse_ref("plain string") is None
    assert P.parse_ref("") is None
    assert P.parse_ref("md:") is None          # empty token rejected


def test_constants():
    assert "statement" in P.TEACHING_TEXT_FIELDS
    assert "title" not in P.TEACHING_TEXT_FIELDS
    assert P.OTF_EXEMPT_KINDS == frozenset({"intro", "outro"})
    assert P.OTF_KINDS == frozenset({"content", "divider"})


if __name__ == "__main__":
    test_parse_ref()
    test_constants()
    print("OK provenance self-test")
```

- [ ] **Step 2: Run it to verify it fails**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_provenance.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'pipeline.provenance'`.

- [ ] **Step 3: Write minimal `provenance.py`**

Create `video/pipeline/provenance.py`:

```python
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
```

- [ ] **Step 4: Run it to verify it passes**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_provenance.py`
Expected: `OK provenance self-test`

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/provenance.py video/pipeline/_selftest_provenance.py
git commit -m "feat(otf): provenance ref grammar primitives + coverage matrix"
```

---

### Task 2: Locus loader — resolve `md:`/`doc:` refs against a deck

**Files:**
- Modify: `video/pipeline/provenance.py`
- Modify: `video/pipeline/_selftest_provenance.py`

**Interfaces:**
- Consumes: `review_pack.parse_content_script(md_path) -> {"units": [{"id": str, ...}]}` (existing).
- Produces: `class Loci` with `Loci.from_deck(meta: dict, repo_root: Path) -> Loci` and `Loci.resolves(ref: str) -> bool`. `from_deck` reads `content_scripts/<meta.id>.md` unit ids + the handout HTML anchors; missing files yield empty sets (resolution then fails closed = warn, never crash).

- [ ] **Step 1: Add the failing self-test**

Append to `_selftest_provenance.py` (before `__main__`):

```python
def test_loci(tmp_md, tmp_handout):
    loci = P.Loci(md_unit_ids={"why_trig", "sector"},
                  handout_anchors={"frag-sec-3-1", "sector-inequality"})
    assert loci.resolves("md:why_trig") is True
    assert loci.resolves("md:absent") is False
    assert loci.resolves("doc:frag-sec-3-1") is True
    assert loci.resolves("doc:data-fig-absent") is False
    assert loci.resolves("garbage") is False
    empty = P.Loci(md_unit_ids=set(), handout_anchors=set())
    assert empty.resolves("md:anything") is False   # fail closed
```

And call `test_loci(None, None)` in `__main__`.

- [ ] **Step 2: Run to verify it fails**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_provenance.py`
Expected: FAIL — `AttributeError: module 'pipeline.provenance' has no attribute 'Loci'`.

- [ ] **Step 3: Implement `Loci`**

Append to `provenance.py`:

```python
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
```

- [ ] **Step 4: Run to verify it passes**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_provenance.py`
Expected: `OK provenance self-test`

- [ ] **Step 5: Smoke-test against the real ch03 deck**

Run:
```bash
C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'video'); from pipeline import _bootstrap; _bootstrap.bootstrap(); from pipeline import provenance; from pathlib import Path; L=provenance.Loci.from_deck({'id':'ch03_trig_derivatives','chapter':'Chapter 3'}, Path('.')); print('md units:', len(L.md_unit_ids), '| anchors:', sorted(L.handout_anchors)[:4]); print('resolves md:why_trig_is_different =', L.resolves('md:why_trig_is_different')); print('resolves doc:frag-sec-3-1 =', L.resolves('doc:frag-sec-3-1'))"
```
Expected: nonzero md-unit count, anchors include `frag-sec-3-1`, both `resolves` print `True`.

- [ ] **Step 6: Commit**

```bash
git add video/pipeline/provenance.py video/pipeline/_selftest_provenance.py
git commit -m "feat(otf): locus loader resolving md:/doc: refs against deck .md + handout"
```

---

### Task 3: Per-scene teaching-text extraction with ref inheritance

**Files:**
- Modify: `video/pipeline/provenance.py`
- Modify: `video/pipeline/_selftest_provenance.py`

**Interfaces:**
- Produces: `scene_text_refs(scene: dict) -> list[tuple[str, str]]` returning `(field_path, effective_ref)` for every present teaching-text field in an OTF-subject scene. Effective ref = `refs[field_path]` if present, else the scene-level `ref`, else `""` (missing). Fields absent from the scene are skipped (no-op when scaffold absent).

- [ ] **Step 1: Add the failing self-test**

Append to `_selftest_provenance.py`:

```python
def test_scene_text_refs():
    scene = {"kind": "content", "template": "theorem_proof",
             "ref": "md:scene_src",
             "statement": "$\\sin x$ continuous",
             "scaffold": {"motive": "why we need continuity"},
             "refs": {"scaffold.motive": "doc:frag-sec-3-1"}}
    got = dict(P.scene_text_refs(scene))
    assert got["statement"] == "md:scene_src"            # inherited scene ref
    assert got["scaffold.motive"] == "doc:frag-sec-3-1"  # field override
    # absent fields not reported; non-teaching 'title' never reported
    scene2 = {"kind": "content", "title": "X", "statement": "y"}
    got2 = dict(P.scene_text_refs(scene2))
    assert got2 == {"statement": ""}                      # missing ref -> ""
    assert "title" not in got2
    # list field expands per index
    scene3 = {"kind": "content", "ref": "md:s", "annotations": ["a", "b"]}
    paths = {p for p, _ in P.scene_text_refs(scene3)}
    assert paths == {"annotations.0", "annotations.1"}
```

And call it in `__main__`.

- [ ] **Step 2: Run to verify it fails**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_provenance.py`
Expected: FAIL — `AttributeError: ... 'scene_text_refs'`.

- [ ] **Step 3: Implement `scene_text_refs`**

Append to `provenance.py`:

```python
def _present_text_fields(scene: dict) -> "list[str]":
    """Field paths of present teaching-text fields. Scalars -> the name; lists ->
    name.i per index; scaffold.* -> dotted. Order: stable for readable findings."""
    paths: list[str] = []
    for name in ("statement", "problem", "body", "reason", "prompt"):
        if isinstance(scene.get(name), str) and scene[name].strip():
            paths.append(name)
    scaffold = scene.get("scaffold")
    if isinstance(scaffold, dict):
        for key in ("motive", "problem"):
            if isinstance(scaffold.get(key), str) and scaffold[key].strip():
                paths.append(f"scaffold.{key}")
    for name in ("annotations", "points"):
        seq = scene.get(name)
        if isinstance(seq, list):
            for i, v in enumerate(seq):
                if isinstance(v, str) and v.strip():
                    paths.append(f"{name}.{i}")
    return paths


def scene_text_refs(scene: dict) -> "list[tuple[str, str]]":
    """(field_path, effective_ref) for each present teaching-text field. Effective
    ref = per-field override (refs map) else scene-level ref else '' (missing)."""
    scene_ref = scene.get("ref") if isinstance(scene.get("ref"), str) else ""
    overrides = scene.get("refs") if isinstance(scene.get("refs"), dict) else {}
    out: list[tuple[str, str]] = []
    for path in _present_text_fields(scene):
        ref = overrides.get(path, scene_ref)
        out.append((path, ref if isinstance(ref, str) else ""))
    return out
```

- [ ] **Step 4: Run to verify it passes**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_provenance.py`
Expected: `OK provenance self-test`

- [ ] **Step 5: Commit**

```bash
git add video/pipeline/provenance.py video/pipeline/_selftest_provenance.py
git commit -m "feat(otf): per-scene teaching-text extraction with ref inheritance"
```

---

### Task 4: The provenance check — `provenance_issues`

**Files:**
- Modify: `video/pipeline/provenance.py`
- Modify: `video/pipeline/_selftest_provenance.py`
- Create: `video/storyboards/_fixtures/otf_provenance.yml`

**Interfaces:**
- Produces: `provenance_issues(data: dict, loci: Loci, enforce: bool) -> list[tuple[str, str]]`. For each `kind in OTF_KINDS` scene, every present teaching-text field must have an effective ref that `loci.resolves(...)`. Missing ref or unresolvable ref → one issue at severity `"error" if enforce else "warn"`. `intro`/`outro` skipped. Severity is the gating axis; the finding text states the field + reason.

- [ ] **Step 1: Create the fixture storyboard**

Create `video/storyboards/_fixtures/otf_provenance.yml`:

```yaml
meta: { id: _fixture_otf, section: "0.0", chapter: "Chapter 3" }
scenes:
  - id: ok_inherited
    kind: content
    template: theorem_proof
    ref: md:unit_a
    say: "{show statement}"
    statement: "resolvable via inherited scene ref"
  - id: bad_missing
    kind: content
    template: theorem_proof
    say: "{show statement}"
    statement: "no ref anywhere -> finding"
  - id: bad_unresolvable
    kind: content
    template: derivation
    say: "{show statement}"
    statement: "ref points nowhere"
    refs: { statement: "md:does_not_exist" }
  - id: intro
    kind: intro
    statement: "exempt brand text -> no finding"
```

- [ ] **Step 2: Add the failing self-test**

Append to `_selftest_provenance.py`:

```python
def test_provenance_issues():
    loci = P.Loci(md_unit_ids={"unit_a"}, handout_anchors=set())
    data = {"scenes": [
        {"id": "ok", "kind": "content", "ref": "md:unit_a", "statement": "x"},
        {"id": "miss", "kind": "content", "statement": "x"},
        {"id": "bad", "kind": "content", "statement": "x",
         "refs": {"statement": "md:nope"}},
        {"id": "intro", "kind": "intro", "statement": "x"},
    ]}
    warns = P.provenance_issues(data, loci, enforce=False)
    msgs = " | ".join(m for _, m in warns)
    assert all(s == "warn" for s, _ in warns)
    assert "miss" in msgs and "bad" in msgs
    assert "ok" not in msgs and "intro" not in msgs    # resolvable + exempt skipped
    errs = P.provenance_issues(data, loci, enforce=True)
    assert all(s == "error" for s, _ in errs)
    assert len(errs) == len(warns) == 2
```

And call it in `__main__`.

- [ ] **Step 3: Run to verify it fails**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_provenance.py`
Expected: FAIL — `AttributeError: ... 'provenance_issues'`.

- [ ] **Step 4: Implement `provenance_issues`**

Append to `provenance.py`:

```python
def provenance_issues(data: dict, loci: "Loci", enforce: bool) -> "list[tuple[str, str]]":
    """(severity, message) per teaching-text field whose ref is missing/unresolvable.
    severity = 'error' if enforce else 'warn' (the warn-default/opt-in gating axis).
    intro/outro exempt; resolvable fields produce nothing."""
    sev = "error" if enforce else "warn"
    issues: list[tuple[str, str]] = []
    for scene in data.get("scenes", []) or []:
        if not isinstance(scene, dict) or scene.get("kind") not in OTF_KINDS:
            continue
        sid = scene.get("id", "?")
        for path, ref in scene_text_refs(scene):
            if not ref:
                issues.append((sev, f"{sid}.{path}: on-screen teaching text has no "
                                    f"provenance ref (scene `ref:` or `refs.{path}`)"))
            elif not loci.resolves(ref):
                issues.append((sev, f"{sid}.{path}: provenance ref {ref!r} does not "
                                    f"resolve (no such .md unit / handout anchor)"))
    return issues
```

- [ ] **Step 5: Run to verify it passes**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_provenance.py`
Expected: `OK provenance self-test`

- [ ] **Step 6: Commit**

```bash
git add video/pipeline/provenance.py video/pipeline/_selftest_provenance.py video/storyboards/_fixtures/otf_provenance.yml
git commit -m "feat(otf): warn/error provenance check with intro/outro exemption"
```

---

### Task 5: Wire into `schema.py` as warn-only (gating only on `meta.otf_enforce`)

**Files:**
- Modify: `video/pipeline/schema.py` (imports; `main()` after the existing schema print, ~`:156-166`)
- Modify: `video/pipeline/_selftest_provenance.py` (end-to-end fixture assertion)

**Interfaces:**
- Consumes: `provenance.Loci.from_deck`, `provenance.provenance_issues`.
- Produces: `schema.py` prints provenance findings under a `[provenance]` header; exit code stays 0 unless `meta.otf_enforce is True` AND there are unresolved fields. Zero behavior change for existing decks (none set `otf_enforce`).

- [ ] **Step 1: Add the end-to-end failing assertion**

Append to `_selftest_provenance.py`:

```python
def test_schema_integration():
    import subprocess
    py = sys.executable
    out = subprocess.run(
        [py, "video/pipeline/schema.py", "video/storyboards/_fixtures/otf_provenance.yml"],
        capture_output=True, text=True)
    assert out.returncode == 0                      # warn-default never aborts
    assert "[provenance]" in out.stdout
    assert "bad_missing.statement" in out.stdout
    assert "bad_unresolvable.statement" in out.stdout
    assert "ok_inherited" not in out.stdout and "intro" not in out.stdout
```

And call it in `__main__`.

- [ ] **Step 2: Run to verify it fails**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_provenance.py`
Expected: FAIL — assertion `"[provenance]" in out.stdout` (schema.py doesn't print it yet).

- [ ] **Step 3: Wire the check into `schema.py`**

In `schema.py` `main()`, immediately after the existing schema-result print block (the `if issues: ... else: ...`, before the `--list` block at `:168`), insert:

```python
    # OTF provenance (warn-default; gates only when meta.otf_enforce is True)
    from pathlib import Path as _Path
    from pipeline import provenance as _prov
    repo_root = _Path(__file__).resolve().parent.parent.parent
    meta = data.get("meta", {}) if isinstance(data, dict) else {}
    enforce = bool(meta.get("otf_enforce"))
    loci = _prov.Loci.from_deck(meta, repo_root)
    prov = _prov.provenance_issues(data, loci, enforce=enforce)
    if prov:
        p_err = sum(1 for s, _ in prov if s == "error")
        print(f"[provenance] {args.storyboard.name}: {len(prov)} finding(s)"
              f"{' (ENFORCED)' if enforce else ' (warn-only; set meta.otf_enforce to gate)'}")
        for sev, msg in prov:
            print(f"  {'ERROR' if sev == 'error' else 'WARN '}  {msg}")
        if p_err:
            errors = errors + [m for s, m in prov if s == "error"]
```

(The final `return 1 if errors else 0` at `:174` then gates on enforced provenance errors too.)

- [ ] **Step 4: Run the provenance self-test (incl. integration) to verify it passes**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/_selftest_provenance.py`
Expected: `OK provenance self-test`

- [ ] **Step 5: Regression — existing decks still pass (zero behavior change)**

Run: `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe video/pipeline/schema.py video/storyboards/ch03_trig_derivatives.yml`
Expected: exit 0; existing `[schema] ... structure OK`; a `[provenance] ... (warn-only ...)` block listing un-reffed fields (expected — ch03 isn't migrated yet) but **exit code 0**.

- [ ] **Step 6: Commit**

```bash
git add video/pipeline/schema.py video/pipeline/_selftest_provenance.py
git commit -m "feat(otf): wire provenance check into schema.py (warn-default, opt-in gating)"
```

---

## Plans 2–5 (to detail after Plan 1 lands + grammar is exercised)

- **Plan 2 — Scaffold model + templates:** `scaffold` schema, `render_scaffold` helper in `_common.py` (motive = small `text` role, NOT muted), divider `problem` block, assumptions registry + `first_use_unit` consistency check (extends `provenance.py`), template wiring (`text_of()` adapter, no scalar change, no-op absent).
- **Plan 3 — Pedagogy gate:** `PEDAGOGY-FIRSTLEARNER-RUBRIC.md` (PD1–PD4 + OF1–OF2, structural-blocking/quality-advisory) + `pedagogy-firstlearner-audit` gate-1 agent (reads storyboard+.md+handout); OF1 source-adequacy judgment; `CONTENT_APPROVED` lifecycle gating; separate PD/OF blocking counts.
- **Plan 4 — Visual extension:** A7 figure-prominence sub-criterion (measured), V4/A6 min-size floor constant in `theme.py`/`sizecheck.py`, mobile yardstick in `VISUAL-FRAME-RUBRIC.md`.
- **Plan 5 — Methodology/doc wiring:** `CONTENT_METHODOLOGY.md` (P1/P2/P4 + OTF rules), `DESIGN.md` (scaffold/authoring checklist), L1 scaffold exception in `CONTENT-SIXLENS-RUBRIC.md`, `REVIEW_GATES.md` (gate in sequence), doc-drift V1-V8→V1-V9 in REVIEW_GATES + DESIGN.

> SP2 (backfill of 3 locked decks) follows SP1 per spec §11: dry-run → classify → user-approve migration list → scoped fix. The writing-plans #1 open items (non-content exemption finalization, source-adequacy enforcement, legacy freeform-source migration mapping, CONTENT_APPROVED deck→unit) are addressed in Plans 2–3 and the SP2 migration step.

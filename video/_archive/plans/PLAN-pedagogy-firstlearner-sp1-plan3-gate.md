> **Status: archived / completed（2026-07-07 歸檔）** — 本計畫已全數落地（執行紀錄見 `video/_archive/REBUILD_LOG-2026-05-to-07.md` 對應節）。活的權威見 `video/REVIEW_GATES.md`／`video/DESIGN.md`／`video/SPEC-pedagogy-firstlearner-*.md`。本檔為歷史施工紀錄，內含相對路徑可能已過時。

# Pedagogy-Firstlearner Gate (Rubric + gate-1 Agent) — Implementation Plan (SP1, Plan 3 of 5)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up the SP1 **judgment layer** — a `PEDAGOGY-FIRSTLEARNER-RUBRIC.md` SSOT (PD1–PD4 teaching-quality + OF1–OF2 on-screen-text-faithfulness dimensions) plus a read-only `pedagogy-firstlearner-audit` gate-1 Claude subagent that applies it over storyboard + `.md` + handout — calibrated against a fixture, landing **non-gating** (dry-run/warn) per spec §9.3.

**Architecture:** Mirror the existing audit-gate pattern (NFA, visual-frame): a markdown rubric (the contract / SSOT) + a thin agent definition that **points to it** (no rubric duplication — avoids drift). The deterministic substrate — PD2/PD3/PD4 structural existence, OF2 ref resolution, and the `.md`/handout locus loader — **already exists from Plans 1–2** (`pipeline/pedagogy.py`, `pipeline/provenance.py`); Plan 3 adds only the *judgment* layer + its calibration. **No new Python.**

**Tech Stack:** Markdown (rubric in `content_scripts/_audit/`, agent def in `.claude/agents/`); a fixture storyboard + backing `.md`; calibration by dispatching the agent (Agent tool, `subagent_type: pedagogy-firstlearner-audit`) and diffing findings against an expected table. Offline, zero-API (gate-1 is a free Claude subagent — like NFA gate-1).

---

## Global Constraints

- **Spec authority:** `SPEC-pedagogy-firstlearner-framework.md` — §5 (OTF), §7 (the gate; PD1–PD4 + OF1–OF2; hard discipline), §9 (deterministic split — what is *already* done), §10 (non-overlap boundaries), §12 (change-landing list + the four writing-plans must-defines). This plan implements **only the judgment layer**. The visual extension (A7 / V4·A6 / mobile) is **Plan 4**; the methodology/doc wiring (`CONTENT_METHODOLOGY.md`, `DESIGN.md`, `CONTENT-SIXLENS-RUBRIC.md` L1 exception, `REVIEW_GATES.md` sequence, V1–V8→V1–V9 doc-drift) is **Plan 5**.
- **No new Python / no new dependency.** The deterministic checks already exist: `pedagogy.py` (PD2/PD3/PD4 structural + registry), `provenance.py` (OF2 ref resolution + `Loci.from_deck` locus loading). Plan 3 is **markdown + calibration**. If calibration reveals a genuinely missing deterministic capability, that is a scoped Plan-1/2 follow-up, not new Plan-3 code.
- **Lands non-gating (§9.3 two-axis clarification).** "blocking" is a finding's **severity class**, not "blocks the deck." On landing, every finding (deterministic *and* gate-1 PD/OF) presents as **warn/dry-run** and never gates; per-deck SP2 opt-in flips it to gating later. The rubric's "converge = PD/OF blocking == 0" is the **post-opt-in target**, not a landing gate.
- **Read-only gate.** The agent reports findings, **never edits files** (mirror NFA / visual-frame).
- **Separate PD/OF counts (Codex D, §7).** The rubric output spec and the agent MUST report `PD blocking` and `OF blocking` **separately** — a subjective teaching finding must never mask a hard faithfulness failure.
- **Non-overlap (§10).** The gate never raises a finding owned by six-lens (`L1`/`L2`/`L6`), `NFA`, visual-frame (`V*`/`A*`), or hook-engineering (`E1`). The rubric carries the §10 boundary table verbatim-in-substance.
- **OTF exemptions already encoded.** `provenance.py` `OTF_EXEMPT_KINDS = {intro, outro}` and `OTF_KINDS = {content, divider}`; the gate treats intro/outro as OF-exempt and relies on `kind`/template to exclude recap from PD3 (§10 L6). `subtitle` is brand-exempt (Plan-1 grammar).
- **Provenance grammar is `ref:`/`refs:` (Plan-1 landed), NOT the spec's older `source:`/`from:` wording.** The machine-resolvable provenance is the scene-level `ref:` (inherited by teaching-text fields) + a `refs:` map for **field-level overrides** keyed by field path, each resolving to `md:<unit_id>` or `doc:<handout-anchor>` (`provenance.py`: `scene_text_refs`). The freeform `source:` is a **separate human-readable label** (kept, never parsed — Plan-1 decision; see REBUILD_STATUS «Plan 1» / `_selftest_provenance.py`). The rubric, agent, and fixture MUST speak `ref:`/`refs:` (what the gate actually reads), and treat OF1 "source-adequacy" as judging the resolved source's specificity — not a `source:` string.
- **Surgical.** Create only the files named per task; do not touch templates/pipeline/code or the broader docs (those are Plans 4–5 / done).

## Decisions (LOCKED by this plan — review here first)

- **D-P3-1 — judgment layer only, no code.** PD2/PD3/PD4 + OF2 determinism and the `.md`/handout locus loader landed in Plans 1–2; Plan 3 adds the rubric + agent + calibration. The gate-1 agent's own **blocking** findings are **PD1 (judgment) + OF1 (reads the real source)**; PD2/PD3/PD4 *structural* blocking and OF2 are computed by `pedagogy.py`/`provenance.py` (the agent *surfaces* them with teaching context, it does NOT re-implement them).
- **D-P3-2 — gate-2 not established** (spec §7). SP1 ships gate-1 (free Claude subagent) only. A future Codex gate-2 (as NFA has) is out of SP1 scope.
- **D-P3-3 — OF lifecycle is agent-side (§5.6).** The agent reads the cited content-script's deck-level `CONTENT_APPROVED`; OF findings are **blocking-class only when `CONTENT_APPROVED=yes`**, else dry-run/advisory (you cannot hold text faithful to an unapproved/draft source). **Deck→unit inheritance (§12d):** a `md:<unit>` ref inherits the deck's `CONTENT_APPROVED`; a `doc:<handout-anchor>` ref is gate-able once it resolves (handout anchors are published/stable). No new code — a documented rule the agent follows.
- **D-P3-4 — source-adequacy is an OF1 rubric criterion (§12b).** OF1 also flags when a cited source is **too broad to specifically support the claim** (e.g., a whole-section / recap-synthesis source cited for a specific sub-claim it does not state) — preventing an over-broad inherited source from masking a missing field-level override. The rubric states "when a field-level override is required" + "how OF1 judges specificity."
- **D-P3-5 — non-content scenes (§12a).** intro/outro are OF-exempt (`OTF_EXEMPT_KINDS`, Plan 1); divider teaching text is carried by `scaffold.problem` (Plan 2) and IS auditable (PD3 + OF). No Plan-3 migration of existing decks — SP2 backfill handles per-deck opt-in (§11).
- **D-P3-6 — calibrate on fixtures, never a locked deck (§11 overfit caution); TWO fixture decks for the OF lifecycle.** `Loci.from_deck` resolves a deck's refs only against `content_scripts/<meta.id>.md` (one backing `.md` per deck; deck-level `CONTENT_APPROVED`), so the approved-vs-DRAFT lifecycle needs **two** fixture decks, each `meta.id` matching its own `.md`: `pedagogy_audit` (backing `_fixture_pedagogy.md`, `CONTENT_APPROVED: yes` -> OF blocking-class) and `pedagogy_audit_draft` (backing `_fixture_pedagogy_draft.md`, `CONTENT_APPROVED: no` -> OF dry-run). Never calibrate by editing a real/locked deck.

## File Structure

- **Create** `content_scripts/_audit/PEDAGOGY-FIRSTLEARNER-RUBRIC.md` — the SSOT: scope/boundaries, PD1–PD4 + OF1–OF2 dimensions (blocking/advisory), §10 boundary table, hard discipline (cite-or-advisory, no rewrite loop, separate PD/OF counts), OF lifecycle + source-adequacy, convergence line, output format. One responsibility: the pedagogy/OTF audit contract.
- **Create** `.claude/agents/pedagogy-firstlearner-audit.md` — the gate-1 agent (frontmatter `name`/`description`/`tools: Read, Grep, Glob`/`model: inherit`; body points to the rubric, lists inputs, defers the output format to the rubric — does NOT duplicate the rubric).
- **Create** the calibration fixtures — **two decks, one `.md` per deck via `meta.id`** (D-P3-6): `storyboards/_fixtures/pedagogy_audit.yml` (+ backing `content_scripts/_fixture_pedagogy.md`, `CONTENT_APPROVED: yes`) carrying the deterministic + agent-judgment + clean + boundary cases; and `storyboards/_fixtures/pedagogy_audit_draft.yml` (+ backing `content_scripts/_fixture_pedagogy_draft.md`, `CONTENT_APPROVED: no`) for the OF dry-run lifecycle case.
- **Create** `content_scripts/_audit/CALIBRATION-pedagogy-firstlearner.md` — the expected-findings table (what the gate MUST catch / MUST NOT raise / lifecycle expectation) + the recorded calibration result.

---

### Task 1: Author the rubric SSOT (`PEDAGOGY-FIRSTLEARNER-RUBRIC.md`)

**Files:**
- Create: `video/content_scripts/_audit/PEDAGOGY-FIRSTLEARNER-RUBRIC.md`

**Interface:** the SSOT contract the gate-1 agent obeys. Mirrors the section shape of `NARRATION-FAITHFULNESS-RUBRIC.md` (title → scope → dimensions → boundary → hard-discipline → lifecycle → convergence → output).

- [ ] **Step 1: Write the rubric with these sections (content is specified — not placeholders)**

Author `PEDAGOGY-FIRSTLEARNER-RUBRIC.md` containing, in order:

1. **Title + one-line purpose.** `# 初學者教學＋上畫面文字忠實稽核 — 維度與收斂線（PEDAGOGY-FIRSTLEARNER）`. One line: gate-1, read-only, reads storyboard + cited `.md` + handout; two dimension families PD (teaching quality) + OF (on-screen-text faithfulness); reports only, never edits.

2. **審查對象與邊界 (scope).** Inputs: the section's `storyboards/<deck>.yml`; the cited `.md` units in `content_scripts/<deck>.md`; the handout `chapter<N>-print-standalone.html` anchors. Reads `meta.pedagogy_profile` (default `first_time`) and the deck-level `CONTENT_APPROVED`. **Two-axis note (§9.3):** "blocking" = severity class, NOT "blocks the deck"; on landing everything is warn/dry-run until per-deck opt-in.

3. **PD1–PD4 — teaching quality (§7 i).** A table (`code | blocking (observable, must cite) | advisory | boundary §10`):
   - **PD1** beat granularity — blocking: a single beat/`{show}` reveal compresses **>1 load-bearing** algebraic/logical action; advisory: "could be more segmented for `first_time`". Reads `pedagogy_profile`. Boundary: `L2` owns unit-level **two concepts**; PD1 owns one-**beat**-many-**actions** (incl. intra-single-concept over-compression). **This is the agent's own judgment (no deterministic counterpart).**
   - **PD2** motive — blocking is **deterministic** (`theorem_proof`/`derivation` lacks `scaffold.motive` → `pedagogy.py`); the agent's PD2 job is **advisory**: weak/empty-feeling motive; whether `definition_math` should carry a motive (semantic, §9.2). Boundary: content faithfulness → OF1/L1.
   - **PD3** divider — blocking is **deterministic** (`kind: divider` lacks `scaffold.problem` → `pedagogy.py`); agent advisory: vague / non-concrete problem (not a specific expression). Fires only on `kind: divider`; intro (`kind: intro`) and recap (`kind: content`/`recap_cards`) excluded by kind/template (§10 L6).
   - **PD4** assumptions — blocking is **deterministic** (a registry assumption not flagged at its `first_use_unit` → `pedagogy.py`); agent advisory: flag wording/position. "Used or not / where first-used" is author-declared in the registry; the gate never infers it.
   - Add a sentence: **PD2/PD3/PD4 structural blocking is computed deterministically (`pipeline/pedagogy.py`, Plan 2); the gate-1 agent surfaces it with teaching context and owns the advisory layer. The gate-1 agent's own blocking is PD1 + OF1.**

4. **OF1–OF2 — on-screen-text faithfulness (§5, §7 ii).**
   - **OF1** faithfulness (blocking, **agent judgment**): on-screen teaching text **contradicts or exceeds** its cited source (adds math/conclusions the source lacks; changes a condition). OF1 **reads the real resolved source** (the `md:<unit>` or `doc:<anchor>` that the scene's `ref:` / a field's `refs:` entry points to), not just whether a ref exists. **Source-adequacy (D-P3-4):** also flag when the resolved source is **too broad to specifically support the claim** (e.g., a whole-section / recap-synthesis unit cited for a specific sub-claim it does not state) → a field-level `refs:` override to a more specific locus is required. OF1 does **not** re-compute math correctness (that is `L5`).
   - **OF2** traceability (blocking, **structural/deterministic**): a teaching-text field whose effective `ref` is missing or does not resolve → `provenance.py` `provenance_issues` (Plan 1). The agent surfaces it; it does not re-implement it.
   - **Field-level override rule (§5.1, landed grammar):** all on-screen teaching-text fields inherit the scene-level `ref:`; a field-level `refs.<field_path>` override is required only when the field (a) cites a *different* locus, (b) synthesizes across units, or (c) makes a high-risk math claim. OF1 source-adequacy enforces this. (`source:` is the freeform human label, not the machine ref — see Global Constraints.)

5. **邊界與不重疊 (§10).** The non-overlap table (issue | existing owner | this gate's non-overlapping slice). Carry every row: two concepts→`L2`; one beat many actions→**PD1**; intro tagline / recap takeaway→`L6`; per-scene motive/problem→**PD2/PD3**; `.md` vs handout→`L1`; narration→`NFA`; **storyboard on-screen text vs approved source→OF1/OF2**; scaffold/statement math correctness→`L5` (OF1 only checks "supported by source", never recomputes); figure readability→`V3`; figure prominence→`A7`; unreadable text→`V4`/`A6`; post-render pixels/hook/timing→`V6`/`V8`; hook self-drawn text not in YAML→`E1`. Include the **PD1-vs-L2 tie-breaker**: L2 = cross-unit concept count (unit layer); PD1 = action count inside a single beat.

6. **硬紀律 (§7, write at the top of the dimensions, before seed-drift can creep in).** blocking ONLY for: observable omission / a concrete skipped step / a missing required field / contradiction-with-source. Every "could be more motivated / slower / clearer" = advisory. **Every blocking must cite:** unit id + the exact beat/field + the missing step or contradiction point + one minimal fix. **Forbidden:** auto-rewrite loops; re-litigating already-approved pedagogy. **Separate counts (Codex D):** output `PD blocking` and `OF blocking` summaries separately.

7. **生命週期 (§5.6, D-P3-3).** OF gating only when the cited content-script's `CONTENT_APPROVED=yes`; in DRAFT, OF runs **dry-run** (findings reported as advisory/dry-run, never blocking) — else you are holding text faithful to an unapproved source. Deck→unit inheritance: a `md:<unit>` ref inherits the deck-level `CONTENT_APPROVED`; a `doc:<handout-anchor>` ref is gate-able once it resolves.

8. **收斂線 (§9.3).** converge = **PD blocking == 0 AND OF blocking == 0**, a **post-opt-in** target — NOT a landing gate. Advisories are user-adjudicated, not forced to zero (as in NFA / PROSE-AUDIT rubrics).

9. **不算 finding (non-findings).** Approved-pedagogy restyling; presentation reordering already covered by L1's scaffold carve-out (§5.5); intro/outro brand text; recap takeaways (L6); render-time pixels (V6/V8). Don't over-report — a clean dimension is a valid result.

10. **回報規格 (output).** First line: `VERDICT: <P> PD blocking, <O> OF blocking, <A> advisory` (PD and OF **separate**). Then per-finding: `- [Blocking|Advisory] [PD#|OF#] <unit-id> · <beat/field> — issue (cite source/text) → minimal fix`. Then a one-line note per clean dimension. End: a line on whether **PD blocking and OF blocking each reach 0** (post-opt-in framing). Read-only / propose-not-act guardrail restated.

- [ ] **Step 2: Self-consistency check (no run; structural)**

Re-read the rubric and confirm: (a) every dimension PD1–PD4, OF1–OF2 has a blocking line, an advisory line, and a §10 boundary; (b) the §10 table has no row that lets the gate raise an `L*`/`NFA`/`V*`/`A*`/`E1`-owned finding; (c) the output spec keeps PD and OF counts separate; (d) the lifecycle + source-adequacy paragraphs are present; (e) it states PD2/3/4 structural blocking + OF2 are deterministic (not re-implemented by the agent).

- [ ] **Step 3: Commit**

```bash
git add video/content_scripts/_audit/PEDAGOGY-FIRSTLEARNER-RUBRIC.md
git commit -m "docs(pedagogy): PEDAGOGY-FIRSTLEARNER-RUBRIC SSOT (PD1-PD4 + OF1-OF2)"
```

---

### Task 2: Author the gate-1 agent definition (`pedagogy-firstlearner-audit`)

**Files:**
- Create: `.claude/agents/pedagogy-firstlearner-audit.md`

**Interface:** a read-only Claude subagent, dispatchable as `subagent_type: pedagogy-firstlearner-audit`, that applies the Task-1 rubric. Mirrors `.claude/agents/narration-faithfulness-audit.md` (frontmatter + body that points to the rubric, never duplicates it).

- [ ] **Step 1: Write the agent definition**

Create `.claude/agents/pedagogy-firstlearner-audit.md`:

```markdown
---
name: pedagogy-firstlearner-audit
description: >
  初學者教學＋上畫面文字忠實稽核（gate 1）——讀某節 storyboard＋cited .md＋handout，審 PD1–PD4
  （教學品質：beat 粒度、motive、divider problem、前提 flag）＋ OF1–OF2（上畫面文字 vs 核准源的
  忠實/可回溯），PD 與 OF blocking 分開計數。唯讀：只回報 findings，絕不改檔。當被要求對某節 storyboard
  做初學者教學／OTF 稽核、或 scaffold/provenance opt-in 前後跑 pedagogy gate 時使用。
tools: Read, Grep, Glob
model: inherit
---

你是某節微積分教學影片 storyboard 的 **初學者教學＋上畫面文字忠實稽核員（gate 1）**。你**稽核並回報 findings，不改任何檔案**（唯讀）。這不是六鏡內容審（那審 `.md`）、不是 NFA（那審 narration）、不是視覺幀審（那審 render 後像素）——你只審 storyboard 的**教學結構**與**上畫面文字對核准源的忠實**。

# 開審前先讀（權威依據，勿憑記憶）
1. `video/content_scripts/_audit/PEDAGOGY-FIRSTLEARNER-RUBRIC.md` — PD1–PD4 ＋ OF1–OF2 維度、blocking/advisory 線、§10 不重疊邊界、硬紀律、OF 生命週期＋source-adequacy、PD/OF 分開計數的輸出格式（**本審的契約**）。
本提示**刻意不複述 rubric**，免兩者漂移。

# 你要審什麼（一次讀齊）
1. **storyboard**：`video/storyboards/<deck>.yml`（場 kind/template、scaffold.motive/problem/flag、meta.pedagogy_profile、meta.assumptions、各場 `ref:` ＋ 欄級 `refs:` 覆寫＝Plan 1 的機器可解析文法；freeform `source:` 是人話標籤、非 ref）。
2. **cited 源**：`video/content_scripts/<deck>.md` 被 ref 指到的單元（`md:<unit_id>`），＋ handout `chapter<N>-print-standalone.html` 被指到的 anchor（`doc:<frag-sec-*|data-fig>`）。
3. **核准狀態**：該 `.md` 的 deck-level `CONTENT_APPROVED`（使用者會講；未講時當 `no`）。OF 的生命週期依此（rubric §生命週期）。

# 怎麼做
- **完全依 rubric** 走 PD1–PD4 ＋ OF1–OF2 維度、blocking/advisory 線、§10 不重疊邊界、硬紀律與 source-adequacy——**criteria 一律以 rubric 為準，本提示不複述**（rubric 是 SSOT，免兩者漂移）。
- 操作提醒（皆**已定義於 rubric**，此處只點名免漏、非另立規範）：① **PD blocking 與 OF blocking 分開計數**；② **OF 生命週期**——cited 源 `CONTENT_APPROVED` 非 `yes` 時 OF 走 dry-run；③ **gate-1 自有 blocking ＝ PD1＋OF1**，PD2/3/4 結構存在性＋OF2 由確定性層（`pipeline/pedagogy.py`／`provenance.py`）算、你 surface＋給脈絡、不重算。
- 唯讀、不 over-report（乾淨維度是有效結果）、禁止自動改寫迴圈／re-litigate 已認可教學法——依 rubric 護欄。

# 輸出
完全依 rubric 的輸出格式（首行 `VERDICT: <P> PD blocking, <O> OF blocking, <A> advisory`；逐條 `[Blocking|Advisory] [PD#|OF#] unit · beat/欄位 — issue（引用源/文字）→ 最小修法`；各乾淨維度一行；末行對「PD blocking 與 OF blocking 是否各歸零」給結論，採 opt-in 後框架）。不寫任何檔。
```

- [ ] **Step 2: Verify the agent is well-formed**

Confirm: frontmatter `name: pedagogy-firstlearner-audit` matches the filename; `tools: Read, Grep, Glob` (read-only); `model: inherit`; the body points to the rubric and does NOT duplicate its criteria; the description's trigger phrasing is specific (storyboard pedagogy / OTF audit). (No code to run — this is a definition file; Task 4 exercises it by dispatch.)

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/pedagogy-firstlearner-audit.md
git commit -m "feat(pedagogy): pedagogy-firstlearner-audit gate-1 subagent definition"
```

---

### Task 3: Build the calibration fixture + expected-findings table

**Files:**
- Create: `video/storyboards/_fixtures/pedagogy_audit.yml` (approved deck) + `video/storyboards/_fixtures/pedagogy_audit_draft.yml` (draft deck)
- Create: `video/content_scripts/_fixture_pedagogy.md` (`CONTENT_APPROVED: yes`) + `video/content_scripts/_fixture_pedagogy_draft.md` (`CONTENT_APPROVED: no`)
- Create: `video/content_scripts/_audit/CALIBRATION-pedagogy-firstlearner.md`

**Interface:** two fixture decks (the OF lifecycle needs deck-level `CONTENT_APPROVED`, and `Loci.from_deck` binds one `.md` per deck via `meta.id`) planting the **deterministic track** (PD2/PD3/PD4 structural + OF2, computed by `schema.py`) and the **agent-judgment track** (PD1 + OF1, plus PD2/PD3 advisories) + clean + boundary cases, with a two-section expected-findings table the calibration (Task 4) diffs against. The fixtures are the "test" for the gate family.

- [ ] **Step 1: Create the two backing `.md` cited sources (deck-level `CONTENT_APPROVED`)**

`Loci.from_deck` resolves a deck's refs only against `content_scripts/<meta.id>.md`, so the lifecycle needs two decks (D-P3-6). Create, with real prose so OF1 has actual source text:
- `video/content_scripts/_fixture_pedagogy.md` — `meta.id: _fixture_pedagogy`, `CONTENT_APPROVED: yes`. Units e.g. `unit_squeeze` (states `cos θ ≤ sinθ/θ ≤ 1`, the faithful OF1 source); `unit_narrow` (a *narrow* source that does NOT state a broader claim — for the OF1 **exceeds-source** plant: the on-screen text asserts more than this source); and `unit_broad` (a *broad / cross-unit synthesis* source — for the OF1 **source-adequacy** plant: it loosely "covers" a specific sub-claim it never specifically states, so a field-level `refs:` override to a tighter locus is required — D-P3-4 / §12b).
- `video/content_scripts/_fixture_pedagogy_draft.md` — `meta.id: _fixture_pedagogy_draft`, `CONTENT_APPROVED: no`. One unit cited by the draft storyboard (OF dry-run).

- [ ] **Step 2: Create the main fixture storyboard `pedagogy_audit.yml` (approved)**

`meta.id: _fixture_pedagogy` (refs resolve against `_fixture_pedagogy.md`, `CONTENT_APPROVED: yes`), `meta.pedagogy_profile: first_time`, an `assumptions` registry. Plant BOTH tracks:

**Deterministic track** (computed by `schema.py` -> `[pedagogy]`/`[provenance]`; the agent SURFACES with context, never recomputes):
- **PD2 (det):** a `theorem_proof`/`derivation` scene with NO `scaffold.motive`.
- **PD3 (det):** a `kind: divider` with NO `scaffold.problem`.
- **PD4 (det):** a registry assumption whose `first_use_unit` scene does NOT carry `scaffold.flag: <id>`.
- **OF2 (det):** a teaching-text field with NO resolvable `ref:`/`refs:`.

**Agent-judgment track** (the gate-1 agent's own findings):
- **PD1 blocking:** a `derivation` whose single `{show}` beat compresses >=2 load-bearing algebra steps into one reveal.
- **PD2 advisory:** a `theorem_proof` that HAS a `scaffold.motive` but it is weak/empty (deterministic PD2 satisfied).
- **PD3 advisory:** a `kind: divider` whose `scaffold.problem` is vague/non-concrete.
- **OF1 blocking (exceeds source):** a scene with a resolvable `ref:` to `md:unit_narrow` whose on-screen `statement` asserts MORE than `unit_narrow` states.
- **OF1 blocking (source-adequacy):** a scene inheriting an over-broad scene-level `ref:` for a specific sub-claim the source doesn't state, missing the needed field-level `refs:` override.

**Clean / boundary (must produce NO finding):**
- **Clean:** a PD1-clean segmented derivation; an OF1-clean scene fully supported by its `ref:` source.
- **Boundary (must NOT raise — §10):** (i) a unit with two distinct teaching *concepts* (-> `L2`); (ii) an `intro` scene with a tagline (-> `L6`); (iii) a `recap`/`recap_cards` scene (excluded by kind/template).

- [ ] **Step 3: Create the draft lifecycle storyboard `pedagogy_audit_draft.yml`**

`meta.id: _fixture_pedagogy_draft` (refs resolve against `_fixture_pedagogy_draft.md`, `CONTENT_APPROVED: no`). One scene whose on-screen text exceeds its cited (draft) source — expected **OF dry-run / advisory, NOT blocking** (lifecycle §5.6).

- [ ] **Step 4: Create the two-track expected-findings table**

Create `video/content_scripts/_audit/CALIBRATION-pedagogy-firstlearner.md` with **two separated sections + explicit counts**:
- **Deterministic expected** (from `schema.py` on both decks): the PD2/PD3/PD4 `[pedagogy]` warns + the OF2 `[provenance]` warn, with exact scene ids.
- **Agent-judgment expected** (from dispatching the gate-1 agent): PD1 blocking x1; OF1 blocking x2 (exceeds + source-adequacy); PD2/PD3 advisory x1 each; the draft-deck OF -> **dry-run** (not blocking); an explicit **MUST-NOT-RAISE** list (the clean + three boundary scenes). State the expected `VERDICT` shape (PD/OF counts separated). Leave a "Calibration run result" subsection empty for Task 4.

- [ ] **Step 5: Commit**

```bash
git add video/storyboards/_fixtures/pedagogy_audit.yml video/storyboards/_fixtures/pedagogy_audit_draft.yml video/content_scripts/_fixture_pedagogy.md video/content_scripts/_fixture_pedagogy_draft.md video/content_scripts/_audit/CALIBRATION-pedagogy-firstlearner.md
git commit -m "test(pedagogy): two-deck calibration fixture (deterministic + agent tracks) + expected table"
```

---

### Task 4: Calibrate the gate (dispatch → diff → iterate)

**Files:**
- Modify: `video/content_scripts/_audit/CALIBRATION-pedagogy-firstlearner.md` (record the run)
- Possibly modify: `PEDAGOGY-FIRSTLEARNER-RUBRIC.md` / `.claude/agents/pedagogy-firstlearner-audit.md` (iterate until calibrated)

**Interface:** calibration covers BOTH tracks — (a) `schema.py` on the two fixture decks emits the expected deterministic PD2/PD3/PD4 + OF2 findings; (b) the gate-1 agent emits the expected PD1 + OF1 (catching all planted, surfacing the deterministic ones with context, raising none of the MUST-NOT-RAISE), PD/OF counts separate, OF dry-run on the draft deck.

- [ ] **Step 1: Deterministic pre-step — run `schema.py` on both fixture decks**

Run (venv python) `video/pipeline/schema.py` on `pedagogy_audit.yml` and `pedagogy_audit_draft.yml`. Confirm the `[pedagogy]` block emits the planted PD2/PD3/PD4 structural warns and `[provenance]` emits the planted OF2 warn, matching the **Deterministic expected** section. (Plans 1–2 self-tests already lock the logic; here we confirm the fixtures exercise it — the substrate the agent surfaces.)

- [ ] **Step 2: Dispatch the gate-1 agent on the approved deck**

Dispatch `subagent_type: pedagogy-firstlearner-audit` on `pedagogy_audit.yml` (+ `_fixture_pedagogy.md`, `CONTENT_APPROVED=yes`). Capture its `VERDICT:` + findings (PD1/OF1 + surfacing of the deterministic ones).

- [ ] **Step 3: Dispatch on the draft deck (lifecycle)**

Dispatch the agent on `pedagogy_audit_draft.yml` (`CONTENT_APPROVED=no`). Confirm the exceeds-source scene -> **OF dry-run / advisory, NOT blocking**.

- [ ] **Step 4: Diff both tracks against the expected table**

Deterministic: `schema.py` output matches Deterministic-expected. Agent: catches PD1 + both OF1 blockings; surfaces the deterministic findings with teaching context; raises NONE of the MUST-NOT-RAISE; PD/OF counts separate; draft -> dry-run.

- [ ] **Step 5: Iterate until calibrated**

If the agent misses a planted blocking, over-reports a boundary/clean case, merges PD/OF counts, gates a draft-deck OF, or fails to surface a deterministic finding: tighten the **rubric** and/or **agent body**, re-dispatch. Calibrated = both tracks match expected. Record the final runs (schema.py output + the two agent verdicts + diff) in `CALIBRATION-pedagogy-firstlearner.md`.

- [ ] **Step 6: Commit**

```bash
git add video/content_scripts/_audit/CALIBRATION-pedagogy-firstlearner.md video/content_scripts/_audit/PEDAGOGY-FIRSTLEARNER-RUBRIC.md .claude/agents/pedagogy-firstlearner-audit.md
git commit -m "test(pedagogy): calibrate gate — deterministic + agent tracks, lifecycle, boundaries"
```

---

### Task 5: User sign-off + Plan 3 whole-branch review

**Files:**
- Create (scratchpad, not committed): an "open and read" HTML report of the rubric + calibration result (per CLAUDE.md sign-off culture).

- [ ] **Step 1: Produce the sign-off report**

A standalone HTML (CDN MathJax/KaTeX, double-click to open) summarizing: the rubric's dimensions (PD1–PD4 + OF1–OF2, blocking/advisory), the §10 boundaries, the OF lifecycle + source-adequacy rules, and the **calibration result** (each planted case → what the gate found; the MUST-NOT-RAISE cases stayed silent; PD/OF separated; DRAFT → dry-run). The gate's judgment quality (what it flags / what it lets pass) is a contract the user owns.

- [ ] **Step 2: User sign-off**

Present the report; get the user's sign-off on the rubric + the calibrated gate behavior before considering Plan 3 done. (The rubric is a judgment contract — like Plan 2's visual sign-off, this is a planned human gate.)

- [ ] **Step 3: Plan 3 whole-branch review**

Run an opus whole-branch review of the Plan 3 changeset (rubric + agent + fixture + calibration): does the rubric faithfully encode spec §5/§7/§9/§10? Are the §10 boundaries airtight (no L*/NFA/V*/A*/E1 overlap)? Are PD/OF counts separated? Is the OF lifecycle correct? Does the agent point to (not duplicate) the rubric? Address findings, re-audit.

- [ ] **Step 4: Update progress anchors + finish**

Update `REBUILD_STATUS.md` + `HANDOFF-pedagogy-firstlearner-sp1.md`: Plan 3 ✅ (judgment layer landed, non-gating, calibrated, signed off); next = Plan 4 (visual extension). Then `superpowers:finishing-a-development-branch`.

---

## After Plan 3 lands

- **Plan 4 — Visual extension (§8):** `A7` figure-prominence sub-criterion (measured), `V4`/`A6` min-size floor constants in `theme.py`/`sizecheck.py` + mobile yardstick in `VISUAL-FRAME-RUBRIC.md`.
- **Plan 5 — Methodology/doc wiring (§12):** `CONTENT_METHODOLOGY.md` (P1/P2/P4 + scaffold authoring), `DESIGN.md` (scaffold承載 + authoring checklist), `CONTENT-SIXLENS-RUBRIC.md` L1 scaffold exception (§5.5 exact wording), `REVIEW_GATES.md` (new pedagogy gate in sequence + V1–V8→V1–V9 doc-drift cleanup).
- **SP2 backfill** then applies Plans 1–4 to the 3 locked decks (ch01 §1.1, ch03 §3.1/§3.2) per spec §11 (dry-run → classify → user-approved migration list → scoped fix → re-gate/re-render/re-sign-off), flipping per-deck opt-in to gating.

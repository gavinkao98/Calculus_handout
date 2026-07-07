> **Status: archived / completed（2026-07-07 歸檔）** — 本計畫已全數落地（執行紀錄見 `video/_archive/REBUILD_LOG-2026-05-to-07.md` 對應節）。活的權威見 `video/REVIEW_GATES.md`／`video/DESIGN.md`／`video/SPEC-pedagogy-firstlearner-*.md`。本檔為歷史施工紀錄，內含相對路徑可能已過時。

# Methodology / Doc Wiring — Implementation Plan (SP1, Plan 5 of 5)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire the SP1 framework (Plans 1–4, now landed) into the repo's authoritative prose docs per SPEC §12 — so the methodology / design / rubric / gate-sequence docs describe the as-built pedagogy + OTF + visual-floor system, and the last `V1–V8→V1–V9` doc-drift is cleaned up.

**Architecture:** Pure documentation wiring — **no code, no tests, no render**. Five surgical edits to four 繁體中文 authority docs (`CONTENT_METHODOLOGY.md`, `DESIGN.md`, `CONTENT-SIXLENS-RUBRIC.md`, `REVIEW_GATES.md`) plus one mechanical stale-reference cleanup. Each task documents what Plans 1–4 **already built** (the landed commits are the source of truth), faithful to the SPEC §-numbers, in each doc's existing voice. Lands non-gating (docs only; zero runtime effect).

**Tech Stack:** Markdown only. Authority = `SPEC-pedagogy-firstlearner-framework.md` (§4 規則層分工, §5/§5.5 OTF + L1 例外, §6 scaffold 承載, §8 P5/P6 視覺, §10 不重疊邊界, §12 變更落點清單). As-built references: `pipeline/provenance.py`, `pipeline/pedagogy.py`, `pipeline/templates/_common.py` `render_scaffold`, `pipeline/sizecheck.py`/`brand.py`/`pipeline/visuals/theme.py` floor+clamp, `content_scripts/_audit/PEDAGOGY-FIRSTLEARNER-RUBRIC.md`, `VISUAL-FRAME-RUBRIC.md`, `.claude/agents/pedagogy-firstlearner-audit.md`.

> **Codex (gpt-5.5/xhigh) reviewed this plan in 2 rounds before execution: round 1 raised 4 must-fix + 3 deferrable (all folded in); round 2 regression = READY TO EXECUTE, no new issues.** Key as-built corrections: scaffold provenance = `ref:`/`refs.scaffold.*` (NOT `source:`/`from:`); registry = `meta.assumptions` (not top-level); OTF lifecycle/source-adequacy cross-ref added; `visual-frame-audit` (render-frame, post-render) vs `pedagogy-firstlearner-audit` (storyboard+`.md`+handout, pre-render) stage distinction.

---

## Global Constraints

- **Authority = SPEC §12 「變更落點清單」.** Plan 5 implements only the **修改** rows whose targets are prose docs and that Plans 1–4 did NOT already do. Confirmed Plan-5 scope (the rest of §12 是 Plans 1–4 已落地)：
  - `CONTENT_METHODOLOGY.md` — P1/P2/P4 規則 + OTF provenance 規則 + §5 邊界（§12 line 239；§4 規則層「P1–P4 → CONTENT_METHODOLOGY；OTF → CONTENT_METHODOLOGY + REVIEW_GATES」）。
  - `DESIGN.md` — scaffold 承載 + divider `problem` + P5/P6 視覺規則 + authoring checklist（§12 line 240；§6, §8）。
  - `CONTENT-SIXLENS-RUBRIC.md` — L1 scaffold 例外（§12 line 241；§5.5 精確措辭）。
  - `REVIEW_GATES.md` — pedagogy 閘 + fontfloor 檢查進閘序（§12 line 243）。
  - `V1–V8→V1–V9` stale-doc cleanup（§12 line 243：`REVIEW_GATES.md` line 65/66 ＋ `DESIGN.md` ~671/684；**與新閘無關的純清理**，Codex F）。
- **Document the AS-BUILT, not the spec's wish-list.** Plans 1–4 landed; some spec details shifted in implementation. The landed code/rubrics are the source of truth where they differ from the spec's prose. Examples the implementer MUST honor (Codex-verified against the code):
  - the floor is **`MIN_FONT_FLOOR = 26.0` px** (`pipeline/visuals/theme.py`) with a render-time **clamp** (`brand._clamp_shrink`) + **warn-default check** (`sizecheck.py`, opt-in `meta.fontfloor_enforce`);
  - the OTF provenance fields are **new `ref:` (scene-inherited) / `refs:` (column overrides)**. **CRITICAL — `refs:` is a FLAT YAML map keyed by the dotted field-path STRING, NOT nested objects**: `refs: { scaffold.motive: 'md:…', statement: 'doc:…' }` (the key is the literal string `scaffold.motive`). `provenance.py` does `scene.get("refs").get("scaffold.motive")` — nested YAML (`refs: { scaffold: { motive: … } }`) would silently miss. Grammar `md:<unit_id>` / `doc:<frag-sec-*|data-fig>`, **場級繼承 + 欄級覆寫**, warn-only + intro/outro 豁免 — **`source:` is a freeform human label, NOT parsed for provenance** (`provenance.py`);
  - the assumptions registry is read from **`meta.assumptions`** (NOT a top-level `assumptions:`) (`pedagogy.py`);
  - pedagogy deterministic checks are **warn-default**, opt-in `meta.pedagogy_enforce` (independent of `otf_enforce`/`fontfloor_enforce`);
  - OF1 忠實 is **blocking only when the cited source's `CONTENT_APPROVED=yes`** (DRAFT → dry-run/advisory; `md:<unit>` inherits deck approval; `doc:<anchor>` gateable once resolved);
  - the visual rubric is **V1–V9 / A1–A7** with V4 floor + A6 mobile yardstick + A7 figure-prominence.
  When unsure, read the named source file before writing.
- **繁體中文 voice (CLAUDE.md).** All four docs are authored in 繁體中文. Every addition is 繁中, matching each doc's tone + 全形 punctuation, with technical terms / code / filenames / identifiers in English (`MIN_FONT_FLOOR`, `scaffold.motive`, `pedagogy_profile`, `ref:`/`refs:`, `md:`/`doc:`, `V4`/`A6`/`A7`, `PD1`/`OF1`, `render_scaffold`, etc.). Do NOT translate any doc to English.
- **Surgical (Karpathy).** Touch only the named file + named locus per task. Do NOT reword/reformat adjacent sections, do NOT restructure docs, do NOT "improve" unrelated prose. Each added block is traceable to a SPEC §-row. Match the existing heading depth + bullet/table style at the insertion point.
- **No new claims.** Document only what exists. Do NOT invent new rules, thresholds, or behaviors beyond SPEC + as-built. If the spec and the as-built disagree, document the as-built and note the spec §-anchor.
- **Locate by content, not hardcoded line numbers.** Earlier tasks shift later line numbers. Each task **greps / reads to re-find its insertion locus** by surrounding text (the survey's line numbers are a starting hint, not gospel). The `V1–V8` cleanup (Task 5) greps for the token across both files after the content tasks land.
- **Offline only.** Pure markdown edits — no API, no render, no build. (`git diff`/`grep`/`Read` only.) No billed steps.
- **Per-task review.** Each task: implement → **spec-compliance review** (does it faithfully wire the SPEC §-row + match as-built? no over/under-reach?) → **quality review** (voice, locus fit, surgical, no drift) → fix → commit. (No TDD — these are docs; the "test" is the spec-faithfulness + voice review.)

## Decisions (LOCKED by this plan)

- **D-P5-1 — P1–P4 home = `CONTENT_METHODOLOGY.md`; P5–P6 home = `DESIGN.md`** (SPEC §4 規則層分工). §12 line 239 names P1/P2/P4 explicitly for CONTENT_METHODOLOGY; **P3 (divider 講具體問題) is documented as a one-line principle in CONTENT_METHODOLOGY that cross-refers to `DESIGN.md` divider `problem` rendering + the PD3 gate** (its rendering承載 lives in DESIGN, its enforcement in the pedagogy rubric). Do not duplicate P3's rendering detail into CONTENT_METHODOLOGY.
- **D-P5-2 — L1 scaffold 例外 wording = SPEC §5.5 verbatim** (Task 3 shows the exact text). **Single placement: BESIDE the existing L1「呈現的重排與增補不算 finding」carve-out** (in the L1 paragraph). Only ALSO mirror it as a bullet in the dedicated「不算 finding」section if that can be done WITHOUT duplicating the text (e.g. a one-line pointer back to L1) — default to the single L1-paragraph placement; do not state the full exception twice.
- **D-P5-3 — gate placement = same gate-1 free-Claude-subagent TIER, distinct INPUT/stage (Codex must-fix #4).** In `REVIEW_GATES.md`, the **`pedagogy-firstlearner-audit`** subagent is the SAME *tier* as the existing **`visual-frame-audit`** (both free gate-1 Claude subagents) but a **different stage**: `visual-frame-audit` reads **rendered frames (post-render)**, whereas `pedagogy-firstlearner-audit` reads the **storyboard + cited `.md` + handout (pre-render)**. Document it as a gate-1 subagent at the storyboard-authoring stage — do NOT call it "parallel to visual-frame-audit's input." Its deterministic substrate (`schema.py` provenance/pedagogy warn-checks, Plans 1–2) sits with `lint.py`/`schema.py`. The **fontfloor check** parallels **`sizecheck.py`** (make.py-time deterministic — Codex confirmed). **Also: if `REVIEW_GATES.md` carries a count/summary of gate-1 Claude subagents (e.g. "four ... subagents"), update it to include `pedagogy-firstlearner-audit`.** Read the doc's layer model + the existing rows; do not invent a new layer.
- **D-P5-4 — V1–V8→V1–V9 is mechanical cleanup, its own commit** (Task 5), separate from the substantive content tasks (SPEC §12「與新閘無關的清理」). Grep-driven across `DESIGN.md` + `REVIEW_GATES.md`; change only the version token, nothing else on those lines.

## File Structure

- **Modify** `video/CONTENT_METHODOLOGY.md` — add P1–P4 pedagogy principles + an OTF provenance subsection (under §5 視覺與動畫 and/or §7 內容層品質檢核 checklist).
- **Modify** `video/DESIGN.md` — add a scaffold 承載 contract section (after the Lectern 版面網格 section), P5/P6 enforced-visual rules (near §模板視覺修正), and a Scaffold Authoring Checklist (in §Authoring checklist).
- **Modify** `video/content_scripts/_audit/CONTENT-SIXLENS-RUBRIC.md` — add the L1 scaffold 例外 beside the existing L1 carve-out.
- **Modify** `video/REVIEW_GATES.md` — add the pedagogy + fontfloor gate rows to the gate sequence.
- **Modify** `video/DESIGN.md` + `video/REVIEW_GATES.md` (Task 5) — `V1–V8`→`V1–V9` token cleanup.

---

### Task 1: `CONTENT_METHODOLOGY.md` — P1–P4 pedagogy principles + OTF provenance rules + §5 boundary

**Files:**
- Modify: `video/CONTENT_METHODOLOGY.md`

**Authority:** SPEC §1 (P1–P6 定義), §4 (規則層分工：P1–P4 → 本檔；OTF → 本檔 + REVIEW_GATES), §5 / §5.5 (OTF + L1 例外 + 邊界), §10 (不重疊). As-built: `pipeline/provenance.py` (ref grammar `md:`/`doc:`, 場級繼承, warn-only, intro/outro 豁免), `pipeline/pedagogy.py` (PD2/PD3/PD4 warn-default + `meta.pedagogy_enforce`).

- [ ] **Step 1: Read the loci + sources.** Read `video/CONTENT_METHODOLOGY.md` §5 視覺與動畫 (the opening paragraph, ~line 152) and §7 內容層品質檢核 (the checklist, ~line 270) to absorb voice + structure. Read SPEC §1 (P1–P6), §4 (規則層分工), §5 + §5.5, §10. Skim `pipeline/provenance.py` (the `ref:`/`refs:` grammar `md:<unit_id>` / `doc:<frag-sec-*|data-fig>`, 場級繼承+欄級覆寫, warn-only, intro/outro 豁免) so the OTF prose matches the as-built.

- [ ] **Step 2: Add the P1–P4 pedagogy principles.** As a new subsection (繁中, in-voice — likely a `### 初學者教學原則（P1–P4）` block under §5, or as new checklist items under §7, whichever fits the doc's structure best — read both and choose). Content per SPEC §1 + as-built:
  - **P1 證明/推導粒度：** 對初學者「一個 beat 只扛一個承重動作」，不過度壓縮；拆步粒度讀 `meta.pedagogy_profile`（預設 `first_time`）。對應確定性層無（語意），判斷層 = `PEDAGOGY-FIRSTLEARNER-RUBRIC.md` `PD1`。
  - **P2 動機上畫面：** 每個 proof/子結論場景在**畫面上**有一句「為什麼做這個」（`scaffold.motive`），不只藏旁白。`theorem_proof`/`derivation` 缺 motive → 確定性 `schema.py` warn（`PD2`，opt-in `meta.pedagogy_enforce` 才 gating）；`definition_math` 的 motive 是 gate-1 advisory（語意、非確定性必填）。
  - **P3 divider 講具體問題：** section divider 講出正在解的**問題/式子**（`scaffold.problem`），不只概念標題。承載/渲染契約見 [`DESIGN.md`](DESIGN.md)（divider `problem` formula-block）；判斷/確定性見 `PD3`。（**一行原則 + 交叉引用，不在本檔重述渲染細節**——D-P5-1。）
  - **P4 前提首用即標：** 默默用到的慣例/假設（radians、定義域限制）在**第一次用到**處標 `scaffold.flag: <assumption_id>`；**`meta.assumptions[]`** registry 顯式宣告 `id/text/first_use_unit/source`，閘不推斷（`PD4` 確定性一致性檢查）。

- [ ] **Step 3: Add the OTF provenance rules.** A new subsection (繁中, 例如 `### OTF：上畫面教學文字可回溯核准源`) documenting (SPEC §5 + as-built `provenance.py`):
  - 所有**上畫面教學文字**（statement / scaffold / annotations / reason / …）應可回溯到核准源；用**新欄位** `ref:`（單一）/`refs:`（多筆），**與 freeform `source:` 分離**。
  - 文法：`md:<unit_id>`（指 `.md` narration unit）/ `doc:<frag-sec-*|data-fig>`（指 handout anchor）。
  - **場級繼承 + 欄級覆寫**：場景設一個 `ref:`，欄位可各自覆寫；缺 ref 的場景繼承場級。
  - **落地行為（零行為改變）**：provenance 檢查 **warn-only**，僅 `meta.otf_enforce: true` 才 gating；`intro`/`outro` 場豁免；忠實**語意**比對歸判斷層 `OF1`（gate-1），確定性層只查 ref 可解析。
  - **source-adequacy + 生命週期（Plan 3 鎖定，須一併寫入，勿藏）**：當場景 `ref:` 過寬、藏住欄級該有的覆寫時，`OF1` 要求**更 specific 的 `refs:` 欄級覆寫**；OF 忠實 findings **僅當所引源 `CONTENT_APPROVED=yes` 才 blocking**（`DRAFT` → dry-run/advisory；`md:<unit>` 繼承 deck 核准；`doc:<anchor>` 一旦解析即可 gate）。
  - 指向強制層：見 [`REVIEW_GATES.md`](REVIEW_GATES.md)（OTF → 本檔 + REVIEW_GATES，§4）。

- [ ] **Step 4: Add the §5 boundary (OTF/pedagogy vs six-lens 不重疊).** One short paragraph (per SPEC §10) stating the pedagogy/OTF 閘與 six-lens **不重疊**：`.md` 內容忠實講義 = six-lens `L1`（含 scaffold 例外 §5.5）；上畫面文字 vs 核准源 = `OF1`；scaffold/statement 數學正確 = `L5`（OF1 只查「是否被源支持」，不重算正確性）。指向 `PEDAGOGY-FIRSTLEARNER-RUBRIC.md` §10 的完整邊界表，不在本檔複製整表。

- [ ] **Step 5: Self-consistency check (no run).** (a) P1–P4 present, P3 = one-line + cross-ref (no rendering detail duplicated); (b) OTF rules name `ref:`/`refs:` (NOT freeform `source:`), the `md:`/`doc:` grammar, 場級繼承, warn-only + intro/outro 豁免; (c) boundary paragraph points to §10 / `OF1`/`L1`/`L5` without re-deriving; (d) every claim traces to a SPEC § or an as-built file; (e) 繁中 voice + 全形 + English technical terms; (f) surgical (no adjacent rewrite).

- [ ] **Step 6: Commit.**
```bash
git add video/CONTENT_METHODOLOGY.md
git commit -m "docs(methodology): wire P1-P4 pedagogy principles + OTF provenance rules + six-lens boundary (SPEC §1/§4/§5/§10)"
```

---

### Task 2: `DESIGN.md` — scaffold 承載 contract + P5/P6 enforced-visual rules + scaffold authoring checklist

**Files:**
- Modify: `video/DESIGN.md`

**Authority:** SPEC §6 (承載設計：scaffold 渲染 a–d), §8 (P5/P6 視覺：figure-prominence 量測, min-size floor + mobile). As-built: `pipeline/templates/_common.py` `render_scaffold` (motive/problem/flag → static Block, 缺 scaffold → no-op), `theme.MIN_FONT_FLOOR=26.0`, `brand._clamp_shrink`, `sizecheck.py` floor check, `VISUAL-FRAME-RUBRIC.md` A7/V4/A6.

- [ ] **Step 1: Read the loci + sources.** Read `video/DESIGN.md` around the end of the **Lectern 版面網格** section (~line 318), the **模板視覺修正** section (~line 385), and the **Authoring checklist** section (~line 640) to absorb voice + structure. Read SPEC §6 (a–d) + §8. Read `pipeline/templates/_common.py` `render_scaffold` (the actual signature + what it renders) and confirm `theme.MIN_FONT_FLOOR=26.0` + `brand._clamp_shrink` exist as documented.

- [ ] **Step 2: Add the scaffold 承載 contract section.** A new section (繁中, in-voice, e.g. `## Scaffold 承載與視覺契約`) after the Lectern section, documenting SPEC §6 + the as-built `render_scaffold`:
  - **共用渲染（`_common.render_scaffold`，掛 Lectern）：** content 場（`definition_math`/`theorem_proof`/`derivation`）`scaffold.motive` → 標題下一行**較小的 `text` role**「為什麼」（**不可 `muted`**——違反「教學內容用 text/primary 非 muted」且觸發 sizecheck muted-prose 警告；de-emphasis 靠字級/位置）；`divider` `scaffold.problem` → 標題下公式塊（比會 wrap 的 `subtitle` 更強的 formula-block）；首用場 `scaffold.flag: <assumption_id>` → 小 badge/aside。**缺 `scaffold` 一律 no-op**（render 不變、零行為改變）。
  - **`meta.assumptions` registry：** `meta.assumptions: [{id, text, first_use_unit, source}]`（**`meta.` 之下**，非頂層；`pedagogy.py` 讀 `meta.get("assumptions")`）；每筆必須在 `first_use_unit` 渲出 `scaffold.flag: <id>`，作者顯式宣告、閘不推斷。（此處 registry 的 `source` 是該 assumption 的人讀來源標註，與下方 OTF provenance ref 是不同欄位。）
  - **`meta.pedagogy_profile`（預設 `first_time`，可覆寫）：** PD1 拆步粒度 + PD2 motive 讀此值；SP1 只定義 `first_time`，覆寫語義 YAGNI。
  - **scaffold provenance 走 OTF 的 `ref:`/`refs:`**（場景 `ref:` 繼承；欄級覆寫用 `refs:` **flat map**，key 為欄位路徑字串、**非巢狀物件**，如 `refs: { scaffold.motive: 'md:…' }`）；`source:` 為 freeform 人讀標籤、**不被解析為 provenance**（`provenance.py`）。指向 [`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md) 的 OTF 規則。

- [ ] **Step 3: Add the P5/P6 enforced-visual rules.** Near the 模板視覺修正 section (繁中, in-voice), per SPEC §8 + as-built — **frame these as now-ENFORCED** (Plan 4 landed):
  - **P5 圖凸顯（figure-prominence）：** 核心是幾何直覺的場（hook/graph），圖應主導；維持 `x_length/y_length` 放大圖、**不引入 magic boolean**；凸顯由視覺閘**量測**圖佔幀比例判定（`VISUAL-FRAME-RUBRIC.md` `A7`，advisory magnitude）。
  - **P6 次要文字可讀（min-size floor + mobile）：** reason-rail/註解有最小可讀字級 **`MIN_FONT_FLOOR = 26px`**（`pipeline/visuals/theme.py`）；render-time **clamp**（`brand._clamp_shrink`）縮到合寬但**永不低於 floor**（到 floor 就停、改 wrap/overflow）；**warn-default check**（`sizecheck.py`，opt-in `meta.fontfloor_enforce`）render 前浮現過小文字；判斷層 `V4`（承載值不可讀 → blocking）/`A6`（小但可辨 + 手機寬尺標）。

- [ ] **Step 4: Add the Scaffold Authoring Checklist.** In the Authoring checklist section (繁中, in-voice, mirroring the existing checklist's error/warn severity style), e.g.:
  - scaffold `motive`/`problem`/`flag` 用 `text`/`primary` role，**不可 `muted`**（warn）。
  - `theorem_proof`/`derivation` 場該有 `scaffold.motive`（PD2，opt-in 才 error）。
  - `kind: divider` 場該有 `scaffold.problem`（PD3）。
  - 每筆 `meta.assumptions[]` 必在 `first_use_unit` 有對應 `scaffold.flag`，無孤兒 flag（PD4）。
  - 上畫面教學文字帶 `ref:`/`refs:`（OTF）。

- [ ] **Step 5: Self-consistency check (no run).** (a) scaffold contract matches `render_scaffold`'s actual behavior + the「不可 muted」/「缺 scaffold no-op」invariants; (b) P5 = 量測 (no magic boolean); P6 names `MIN_FONT_FLOOR=26px` + clamp + warn-default + mobile, framed as enforced; (c) checklist items mirror existing severity style; (d) all trace to SPEC §6/§8 or an as-built file; (e) 繁中 voice + 全形 + English terms; (f) surgical.

- [ ] **Step 6: Commit.**
```bash
git add video/DESIGN.md
git commit -m "docs(design): scaffold 承載 contract + enforced P5/P6 visual rules + scaffold authoring checklist (SPEC §6/§8)"
```

---

### Task 3: `CONTENT-SIXLENS-RUBRIC.md` — L1 scaffold 例外 (§5.5 verbatim)

**Files:**
- Modify: `video/content_scripts/_audit/CONTENT-SIXLENS-RUBRIC.md`

**Authority:** SPEC §5.5 (the L1 scaffold exception, exact wording) + §10 (boundary).

- [ ] **Step 1: Read the locus.** Read the L1 definition + its existing「**呈現**的重排與增補（…）**不算** finding」carve-out (in the L1 paragraph), and the dedicated「不算 finding（別誤報）」section. Decide the single best placement (D-P5-2): beside the L1 carve-out, mirrored in「不算 finding」only if the doc's structure clearly invites it (do not double-state in a drifting way).

- [ ] **Step 2: Add the L1 scaffold 例外 — SPEC §5.5 verbatim** (adapt punctuation to the doc's voice but preserve every constraint):
  > **L1 scaffold 例外：** 標記為 `scaffold` 的短文字若只把「已用到的目的／記號／慣例／定義域／前提」講白，**不算** L1「加入講義沒有的數學」；但須 cite locus、**不得**引入新定理／例題／結果、**不得**改條件。

  (SPEC §5.5 verbatim — `須 cite locus` 不加 `source`/`ref` 限定詞，避免 OTF source-vs-ref 歧義。L1 is the six-lens content-faithfulness lens; 「locus」泛指所本的講義/核准源處。)
  Place it immediately beside the existing「呈現的重排與增補不算 finding」carve-out so the two parallel carve-outs read together.

- [ ] **Step 3: Self-consistency check (no run).** (a) the four hard limits are all present — cite locus, no new 定理/例題/結果, no condition change, scope = 已用到的目的/記號/慣例/定義域/前提; (b) it sits beside the existing L1 carve-out, parallel grammar; (c) not double-stated; (d) 繁中 voice + 全形; (e) no other L-code或 carve-out reworded.

- [ ] **Step 4: Commit.**
```bash
git add video/content_scripts/_audit/CONTENT-SIXLENS-RUBRIC.md
git commit -m "docs(sixlens): L1 scaffold carve-out (SPEC §5.5) beside the presentation-reorder carve-out"
```

---

### Task 4: `REVIEW_GATES.md` — pedagogy + fontfloor gates into the gate sequence

**Files:**
- Modify: `video/REVIEW_GATES.md`

**Authority:** SPEC §12 line 243, §7 (pedagogy gate 形態), §8/§9 (fontfloor). As-built: `.claude/agents/pedagogy-firstlearner-audit.md` (gate-1 judgment subagent, reads storyboard+.md+handout), `schema.py` provenance/pedagogy warn-checks (Plans 1–2), `sizecheck.py` floor check (Plan 4). Parallels: the existing `visual-frame-audit` gate-1 row + the `sizecheck.py`/`lint.py`/`schema.py` rows.

- [ ] **Step 1: Read the gate model.** Read `video/REVIEW_GATES.md` 各層表 (層 2–7) + the 貫穿全線 meta-gate section (the `visual-frame-audit` gate1/gate2 rows). Per D-P5-3: `pedagogy-firstlearner-audit` is the **same gate-1 free-Claude-subagent tier** as `visual-frame-audit` but a **different stage** — it reads the **storyboard + cited `.md` + handout (pre-render)**, whereas `visual-frame-audit` reads **rendered frames (post-render)**. Find where a storyboard-stage gate-1 judgment subagent belongs, and where deterministic make.py-time checks belong (with `sizecheck.py`/`lint.py`/`schema.py`). Confirm neither a pedagogy gate nor a fontfloor gate is already present (the survey found none — re-confirm). **Also grep for a count/summary of gate-1 Claude subagents (e.g. "four … subagents") — if one exists, it must grow to include `pedagogy-firstlearner-audit`.**

- [ ] **Step 2: Add the pedagogy gate row(s).** Per the doc's table schema (`閘名 | 執行者 | 性質 | 把關內容 | 權威文檔`):
  - **`pedagogy-firstlearner-audit`** (Claude subagent, 免費, gate-1 judgment) — 把關：PD1–PD4 教學品質（beat 粒度、`scaffold.motive` 動機、divider `scaffold.problem`、前提首用 `scaffold.flag`）＋ OF1–OF2 上畫面文字 vs 核准源忠實；性質 □（warn-default，per-deck opt-in 隨 SP2）；權威 `content_scripts/_audit/PEDAGOGY-FIRSTLEARNER-RUBRIC.md` + agent `.claude/agents/pedagogy-firstlearner-audit.md`。
  - Note its deterministic substrate = the `schema.py` provenance/pedagogy warn-checks (place beside/within the `schema.py` row or as a note, per the doc's style).

- [ ] **Step 3: Add the fontfloor check row.** Beside `sizecheck.py` (make.py-time deterministic, 性質 ■ warn): **fontfloor min-size floor** — `MIN_FONT_FLOOR=26px` enforcement + render-time clamp + mobile yardstick (P6); warn-default, opt-in `meta.fontfloor_enforce`; 權威 `theme.py`/`sizecheck.py`/`brand.py` + `VISUAL-FRAME-RUBRIC.md` V4/A6.

- [ ] **Step 4: Self-consistency check (no run).** (a) pedagogy gate placed as a **storyboard-stage** gate-1 subagent (same free-Claude-subagent tier as `visual-frame-audit`, but NOT described as sharing its render-frame input), fontfloor parallel to `sizecheck.py`; (b) both marked warn-default / opt-in (non-gating on landing); (c) authority-doc column points to the real SSOTs; (d) table columns align with the doc's schema; (e) 繁中 voice; (f) no existing gate row reworded; (g) if a gate-1-subagent count/summary existed, it now includes `pedagogy-firstlearner-audit`.

- [ ] **Step 5: Commit.**
```bash
git add video/REVIEW_GATES.md
git commit -m "docs(gates): add pedagogy-firstlearner-audit + fontfloor checks to the gate sequence (SPEC §12)"
```

---

### Task 5: `V1–V8 → V1–V9` stale-doc cleanup (mechanical)

**Files:**
- Modify: `video/DESIGN.md`, `video/REVIEW_GATES.md`

**Authority:** SPEC §12 line 243 (「順手修既有 stale doc：V1–V8→V1–V9 …與新閘無關的清理」). The visual rubric has been V1–V9 since before Plan 4; these two docs still say V1–V8. (The agent-file locus was already fixed in Plan 4 Task 4.)

- [ ] **Step 1: Grep for the stale token** (line numbers may have shifted after Tasks 2/4):
```bash
grep -n "V1–V8\|V1-V8" video/DESIGN.md video/REVIEW_GATES.md
```
Expected: a handful — `DESIGN.md` ~2 (visual-QA/抽幀 lines, ~671/684) + `REVIEW_GATES.md` **~2–3** (gate1/gate2 rows ~65/66 **AND at least one more, ~line 119** — Codex caught this). **Grep is authoritative: fix EVERY match, not a fixed count.** Record the actual matches.

- [ ] **Step 2: Replace each `V1–V8`→`V1–V9`** (preserve the en-dash `–` exactly; change ONLY the version token on each matched line, nothing else). Use exact-string edits per occurrence.

- [ ] **Step 3: Verify no stragglers.** Re-grep:
```bash
grep -n "V1–V8\|V1-V8" video/DESIGN.md video/REVIEW_GATES.md
```
Expected: no matches. Also `grep -n "V1–V9" …` to confirm the replacements landed.

- [ ] **Step 4: Commit.**
```bash
git add video/DESIGN.md video/REVIEW_GATES.md
git commit -m "docs: V1-V8 -> V1-V9 stale-reference cleanup (DESIGN + REVIEW_GATES; SPEC §12, Codex F)"
```

---

## After Plan 5 lands

- **SP1 (Plans 1–5) complete.** The framework + its docs are wired; everything landed **non-gating** (per-deck opt-in flags `otf_enforce`/`pedagogy_enforce`/`fontfloor_enforce` all default off).
- **Next = SP2 backfill** (SPEC §11): apply SP1 to the 3 locked decks (ch01 §1.1, ch03 §3.1/§3.2) — 乾跑 → 分類 → 使用者核可遷移清單 → scoped 修（補 `ref:`/`scaffold`、OF1 忠實修）→ 重跑 PD/OF + L1/L5 + NFA 回歸 → 重渲 → 重新 sign-off → 翻 per-deck opt-in 為 gating. The recorded surfaces from Plans 1–4 (provenance warn surface, fontfloor surface) are part of the SP2 surface.
- **Deferred follow-ups** (noted, not built): graph-label/axis-tick floor coverage (Plan 4 scope note); the result-eyebrow `prose_sm` clamp px (SP2, `derivation.py` note).

## Self-Review (writing-plans checklist)

- **Spec coverage:** §12「修改」prose-doc rows all mapped — CONTENT_METHODOLOGY (T1), DESIGN (T2), CONTENT-SIXLENS (T3), REVIEW_GATES gates (T4), V1–V8 cleanup (T5). `VISUAL-FRAME-RUBRIC.md` A7/V4/A6 (§12 line 242) was done in Plan 4 — not re-included. §12「新增」rows + schema/lint/theme/sizecheck/templates rows = Plans 1–4 — not re-included. §12 items a–d (ref grammar / source-adequacy / legacy source map / CONTENT_APPROVED inheritance) were locked in Plans 1–3 — not re-included.
- **Placeholder scan:** no TBD/TODO; each task gives the §-anchored content + exact locus + verbatim wording where the spec provides it (§5.5). Doc tasks specify content + voice rather than pre-writing every 繁中 sentence (the Plan-4 Task-4 pattern) — intentional for in-voice fidelity, not a placeholder.
- **Consistency:** the floor (`MIN_FONT_FLOOR=26px`), ref fields (`ref:`/`refs:`), enforce flags (`otf_enforce`/`pedagogy_enforce`/`fontfloor_enforce`), and V1–V9/A1–A7 naming are used identically across all tasks and match the as-built. P3's split (principle in CONTENT_METHODOLOGY, rendering in DESIGN) is stated once (D-P5-1) and honored in T1/T2.

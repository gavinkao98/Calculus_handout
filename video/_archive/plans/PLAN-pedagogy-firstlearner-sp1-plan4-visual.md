> **Status: archived / completed（2026-07-07 歸檔）** — 本計畫已全數落地（執行紀錄見 `video/_archive/REBUILD_LOG-2026-05-to-07.md` 對應節）。活的權威見 `video/REVIEW_GATES.md`／`video/DESIGN.md`／`video/SPEC-pedagogy-firstlearner-*.md`。本檔為歷史施工紀錄，內含相對路徑可能已過時。

# Visual Extension (min-size floor + A7 figure-prominence + mobile yardstick) — Implementation Plan (SP1, Plan 4 of 5)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. All self-tests run with the **repo venv python** `.venv/Scripts/python.exe` (it has `manim-0.20.1` + vendored PyYAML; bare `python` misjudges).
>
> **This plan was independently reviewed by Codex (gpt-5.5/xhigh) against the real code before finalizing; its findings are folded in (esp. the font-unit normalization, the clamp/fixture interaction, coverage scope, and commit ordering).**

**Goal:** Sharpen the **existing** visual-frame gate per spec §8 (P5/P6, Codex C — "sharpen 既有、不立新 code"): add a deterministic **minimum on-screen font-size floor** (a `theme.py` constant + a warn-default `sizecheck.py` check + an unconditional render-time clamp so a single line can't `scale_to_fit_width` below the floor), and extend the `VISUAL-FRAME-RUBRIC.md` **judgment layer** (V4/A6 numeric floor + a phone-width "mobile yardstick", A7 **figure-prominence** sub-criterion). Lands **non-gating** (check is warn-default + opt-in `meta.fontfloor_enforce`; the clamp is an always-correct engineering fix verified to be a **no-op on existing decks before it is committed**).

**Architecture:** Two layers, mirroring Plans 1–3. **(1) Deterministic** — `theme.MIN_FONT_FLOOR` (in **px**); a dedicated `sizecheck._effective_font_px(node)` that recovers a node's true on-screen px from its manim `font_size` (text Tex carries `PX_TO_FS×TEXT_SCALE`; MathTex carries only `PX_TO_FS`); a `sizecheck.py` floor check that flags any **`_brand_prose`** node (reason-rail / annotation / step prose — `_prose_nodes`) whose recovered px is `< MIN_FONT_FLOOR`, warn-by-default and flipped to `error` only under `meta.fontfloor_enforce`; and a shared `brand._clamp_shrink` helper that prevents the single-line `scale_to_fit_width` sites from shrinking past the floor (wrap/overflow instead). **(2) Judgment** — rubric edits the read-only `visual-frame-audit` gate-1 agent applies on rendered-frame PNGs. TDD for the deterministic core (manim-free pure functions + stdlib-assert self-test); offline mock-render for clamp verification + gate-1 audit for visual verification.

**Tech Stack:** Python (stdlib + manim 0.20.1) for `theme.py`/`sizecheck.py`/`brand.py`/templates; markdown for `VISUAL-FRAME-RUBRIC.md`; stdlib-`assert` self-test (new `_selftest_sizecheck.py`, pattern-identical to `_selftest_provenance.py`); offline `make.py --backend mock` / `scratch_frames.py` / `critic.py --dry-run` for verification (all $0).

---

## Global Constraints

- **Spec authority:** `SPEC-pedagogy-firstlearner-framework.md` — **§8** (P5→A7 figure-prominence by **量測**圖佔幀比例; P6→V4/A6 min-size floor + mobile; engineering = floor constant + clamp single-line shrink), **§9** (new checks warn-default + per-deck opt-in enforce), **§12** (`VISUAL-FRAME-RUBRIC.md` A7/V4/A6; `theme.py`/`sizecheck.py` floor constant + clamp), **§14** ("新檢查（warn 模式）綠/紅正確"; "A7/V4 視覺 blocking == 0"; "全程離線可驗"). This plan implements **only §8**. Methodology/doc wiring is **Plan 5**.
- **Sharpen, don't add new codes (§8, Codex C).** No new V/A code. The floor extends V4/A6; figure-prominence extends A7. All three already exist in `VISUAL-FRAME-RUBRIC.md` (V4 line ~23, A6 ~40, A7 ~41).
- **CRITICAL — the floor reasons in true px, recovered per node type (Codex C1).** `theme.fs(size)` returns **manim font units** `= px * PX_TO_FS` (PX_TO_FS≈0.698, `theme.py:47`), NOT px. **Text** Tex renders at `fs(size) * TEXT_SCALE` (TEXT_SCALE≈1.3102, `brand._text_fs`, `brand.py:168`); **MathTex** renders at `fs(size)` with **no** TEXT_SCALE (`brand.math_line`, `brand.py:456`). The existing `sizecheck._norm_size(node, text_scale)` (`sizecheck.py:50`) divides **both** Tex and MathTex by TEXT_SCALE — correct for the *sibling-ratio* TOLERANCE check, but **WRONG as an absolute px floor** (it returns manim units, and over-divides MathTex). **Therefore Plan 4 adds a NEW `_effective_font_px(node)` helper** that recovers the true authored px: a text Tex → `font_size / (TEXT_SCALE * PX_TO_FS)`; a MathTex → `font_size / PX_TO_FS`. `MIN_FONT_FLOOR` is a px constant compared against `_effective_font_px`. **Do NOT feed the px floor to `_norm_size`; leave `_norm_size` untouched for TOLERANCE.** **NB (Codex regression): in this manim `Tex` SUBCLASSES `MathTex`, so `_effective_font_px` MUST test `isinstance(node, Tex)` BEFORE `MathTex` — otherwise every text node is mis-typed as math and Task 1's self-test fails on first run (see Task 1 Step 4).**
- **Coverage scope is `_brand_prose` (reason-rail / annotation / step prose), NOT graph/axis labels (Codex I2).** `_prose_nodes()` (`sizecheck.py:40`) finds only `_brand_prose`-tagged nodes; graph equation labels + axis ticks are a separate `_graph_labels()` path (`sizecheck.py:209`, `graph.py:147`) with their own size metadata. §8 P6 is explicitly about **reason-rail / 註解** secondary text, so the deterministic floor scopes to `_brand_prose` nodes. Graph-label/axis-tick floor coverage is **out of scope** (a possible Plan-5 / SP2 follow-up — note it, don't build it).
- **Deterministic floor lands non-gating (§9 / §14).** The `sizecheck.py` floor check is **warn-default**; it flips to `error` (gating) only when the deck sets `meta.fontfloor_enforce: true` (a NEW key, **independent of** `otf_enforce`/`pedagogy_enforce`). Zero behavior change on landing.
- **The clamp is unconditional but its no-op is verified BEFORE it is committed (Codex I3 + D-P4-3).** The `_clamp_shrink` render-time fix has no opt-in (always-correct "wrap, don't shrink", DESIGN.md §599–609). It must not silently change existing renders: Task 3 mock-renders the 3 locked decks (ch01 §1.1, ch03 §3.1, §3.2) base-vs-HEAD and confirms **byte-identical** frames **before** the clamp commit lands. If a deck differs, a current line shrinks below the floor (a pre-existing too-small-text case) → do NOT commit silently; surface it to the user (fix now vs SP2).
- **TDD for code.** Each code task: write the failing stdlib-`assert` self-test first, run it to fail, implement minimally, run to pass, commit. The unit-tested cores (`_effective_font_px`, `_floor_findings`, `_clamp_scale`) are **pure / render-free**. Note: importing `pipeline.brand` / `pipeline.sizecheck` pulls in manim (top-level imports, e.g. `brand.py:31`) — the `.venv` has `manim-0.20.1`, so the self-test imports fine; the cores themselves do no rendering. "render-free", not "manim-free".
- **Surgical (Karpathy, CLAUDE.md).** Touch only the files named per task; match each file's style; don't "improve" adjacent code. The agent V1–V8→V1–V9 fix is scoped in D-P4-5.
- **Offline only.** Mock render, `scratch_frames.py`, `critic.py --dry-run`, and the gate-1 `visual-frame-audit` subagent are $0. Any billed step (external VLM `critic.py --confirm`, real render, Codex) is consent-gated (CLAUDE.md).

## Decisions (LOCKED by this plan — review here first)

- **D-P4-1 — floor value + units.** `theme.MIN_FONT_FLOOR = 26.0` (**px**), compared against the true authored px recovered by `sizecheck._effective_font_px(node)` (Global Constraints / Codex C1). 26 = the smallest *intentional* named size (`eyebrow`=26 in `theme._SCALE_PX`), so every deliberate size passes (`eyebrow` recovers to exactly 26, and the check is strict `<`) and only genuinely-too-small text is caught. **Calibrated in Task 5** against the 3 real decks (no false positive). One constant — trivially tunable.
- **D-P4-2 — floor CHECK is warn-default + opt-in.** New key `meta.fontfloor_enforce` (bool). `sizecheck.check_scenes` reads it; floor findings are `warn` (default) or `error` (when set). Wired into the existing `make.py` sizecheck block (already prints warns / aborts on errors) and surfaced by `sizecheck.py main()`. **Not** wired into `schema.py` (sizecheck is a make.py-only gate with its own CLI). Zero behavior change on landing.
- **D-P4-3 — CLAMP is unconditional + no-op-verified-before-commit.** A shared `brand._clamp_shrink(mob, max_w, cur_size_px)` (uses `theme.MIN_FONT_FLOOR`) replaces the raw `mob.scale_to_fit_width(max_w)` at the **two primary sites** (`brand.py:398` pure-`$math$` `prose()`; `templates/derivation.py:180` reason-rail) and, for consistency, the **three standalone-title sites** (`brand.py:144` `heading`; `brand.py:440` `heading_rich`; `templates/graph.py:143` `_title`). **The call site passes `cur_size_px`** (the role's authored px, e.g. `26.0` for an `eyebrow` reason) so the helper never has to guess units; for a `VGroup`/no-`font_size` mob (the derivation reason can be a group, `derivation.py:179`) the call site MUST pass the size (the helper does not read `font_size` off a group). Behavior: shrink to fit width **only down to the floor**; below that, stop at the floor and overflow/wrap. The arithmetic is a pure `_clamp_scale(cur_w, max_w, cur_size, floor)` (unit-tested); `_clamp_shrink` applies it.
- **D-P4-4 — A7 prominence + V4/A6 floor + mobile are JUDGMENT (rubric), no new code (§8).** The `visual-frame-audit` agent applies them on rendered frames. **A7 figure-prominence**: for scenes whose core IS geometric intuition (hook / graph-centric), the figure should dominate; the agent makes an **approximate visual measurement of the figure's share of the content area** (honoring §8's "由量測圖佔幀比例判定") — if it is well below ~half when the beat is fundamentally about the figure, deduct A7 (advisory magnitude, **never** a V-blocking). **V4/A6 floor**: name `MIN_FONT_FLOOR` (26px) as the numeric reference — text below it is "too small to read" → V4 blocking if it makes a load-bearing value unreadable, else A6 deduction. **Mobile yardstick**: sanity-check secondary text at phone width (the frame downscaled to ~360–414px wide) — unreadable there → A6 deduction.
- **D-P4-5 — agent V1–V8→V1–V9 staleness fix (scoped-in here).** `.claude/agents/visual-frame-audit.md` says "V1–V8" at **lines 4 / 15 / 25 / 27** while `VISUAL-FRAME-RUBRIC.md` is already V1–V9. Fix those four `V1–V8`→`V1–V9` in **Task 4** (surgical). The other two stale loci the spec §12 names (`REVIEW_GATES.md`, `DESIGN.md`) stay **Plan 5**.

## File Structure

- **Modify** `video/pipeline/visuals/theme.py` — add `MIN_FONT_FLOOR` in the type-scale block (after `_SCALE_PX`/`PX_TO_FS`/`TEXT_SCALE`).
- **Modify** `video/pipeline/sizecheck.py` — add `_effective_font_px(node)` (px recovery); a pure `_floor_findings(scene_id, sizes, floor, enforce)`; a `_floor_issues(scene, blocks, enforce)` that walks `_prose_nodes(...)` and ALSO the pure-inline-math single-line carriers the `_block_prose_size` filter (`sizecheck.py:74–77`) skips (an absolute floor needs no sibling group); call it from `check_scenes` with `enforce = bool(meta.get("fontfloor_enforce"))`. Also fix the stale `check_scenes`/`check_file` return annotation (`list[str]` → `list[tuple[str, str]]`, `sizecheck.py:441,520`).
- **Create** `video/pipeline/_selftest_sizecheck.py` — stdlib-assert self-test for `_effective_font_px` + `_floor_findings` + `_clamp_scale` (render-free), following `_selftest_provenance.py` shape.
- **Modify** `video/pipeline/brand.py` — add `_clamp_scale` (pure) + `_clamp_shrink(mob, max_w, cur_size_px)`; replace raw `scale_to_fit_width` at `:144`, `:398`, `:440` (each call site passes its role px).
- **Modify** `video/pipeline/templates/derivation.py` — use `_clamp_shrink` at `:180` (reason-rail; pass the reason's role px, handle the group case).
- **Modify** `video/pipeline/templates/graph.py` — use `_clamp_shrink` at `:143` (graph title; pass its role px).
- **Modify** `video/make.py` — confirm floor findings flow through the existing sizecheck error/warn split; adjust the printed line wording if it hides them.
- **Modify** `video/content_scripts/_audit/VISUAL-FRAME-RUBRIC.md` — V4/A6 floor + mobile yardstick; A7 figure-prominence (approximate measurement).
- **Modify** `.claude/agents/visual-frame-audit.md` — V1–V8→V1–V9 at lines 4/15/25/27 (D-P4-5).
- **Create** `video/storyboards/_fixtures/fontfloor.yml` — a deck for Task 5 that (a) WOULD shrink a reason below floor (to prove the **clamp** keeps it ≥ floor) and (b) declares an explicit sub-floor px size (to prove the **check** fires) if the schema exposes a per-field px size; else the check's positive case is the unit test + a temporary-raised-floor calibration (Task 5 Step 3).

---

### Task 1: `MIN_FONT_FLOOR` + `_effective_font_px` + the floor check (sizecheck.py) — TDD

**Files:**
- Modify: `video/pipeline/visuals/theme.py`
- Modify: `video/pipeline/sizecheck.py`
- Create: `video/pipeline/_selftest_sizecheck.py`

**Interface:** `_effective_font_px(node) -> float` recovers a node's authored px (MathTex: `font_size/PX_TO_FS`; text Tex: `font_size/(TEXT_SCALE*PX_TO_FS)`). `_floor_findings(scene_id, sizes, floor, enforce)` is pure: for each `(block_id, px)` with `px < floor`, append `(sev, msg)` (`sev = "error" if enforce else "warn"`). `_floor_issues(scene, blocks, enforce)` builds `sizes = [(bid, _effective_font_px(node)) ...]` over the scene's `_brand_prose` nodes (reuse `_prose_nodes`), **including** the pure-inline-math single-line carriers the `_block_prose_size` filter skips, and delegates to `_floor_findings`.

- [ ] **Step 1: Add the constant.** In `video/pipeline/visuals/theme.py`, in the type-scale block after `_SCALE_PX`/`PX_TO_FS`/`TEXT_SCALE`:

```python
# Minimum readable on-screen font size in PX (1920x1080). Compared against the TRUE authored
# px recovered by sizecheck._effective_font_px (NOT _norm_size, which yields manim units and
# over-divides MathTex). Set at the smallest INTENTIONAL named size (eyebrow=26). Plan 4 / SPEC §8.
MIN_FONT_FLOOR = 26.0  # px; calibrated in PLAN-…-plan4 Task 5
```

- [ ] **Step 2: Write the failing self-test.** Create `video/pipeline/_selftest_sizecheck.py`:

```python
"""Stdlib assert self-test for sizecheck.py floor logic. Run: .venv/Scripts/python.exe video/pipeline/_selftest_sizecheck.py
Render-free (imports manim via sizecheck/brand, but renders nothing)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import sizecheck as S          # noqa: E402
from pipeline.visuals import theme as T      # noqa: E402
from manim import MathTex, Tex               # noqa: E402


def test_effective_px_recovers_authored_size():
    # a text Tex authored at 26px renders at fs(26)*TEXT_SCALE; recover -> ~26
    text = Tex("x"); text.font_size = 26 * T.PX_TO_FS * T.TEXT_SCALE
    assert abs(S._effective_font_px(text) - 26.0) < 0.5
    # a MathTex authored at 40px renders at fs(40) (no TEXT_SCALE); recover -> ~40
    math = MathTex("x"); math.font_size = 40 * T.PX_TO_FS
    assert abs(S._effective_font_px(math) - 40.0) < 0.5


def test_floor_findings_flags_below():
    sizes = [("reason.0", 22.0), ("reason.1", 26.0), ("statement", 40.0)]  # only reason.0 < 26
    warns = S._floor_findings("sc", sizes, 26.0, enforce=False)
    msgs = " | ".join(m for _, m in warns)
    assert all(s == "warn" for s, _ in warns) and len(warns) == 1
    assert "reason.0" in msgs and "sc" in msgs
    assert "reason.1" not in msgs and "statement" not in msgs   # at/above floor pass


def test_floor_findings_enforce_is_error():
    errs = S._floor_findings("sc", [("a", 10.0)], 26.0, enforce=True)
    assert errs and all(s == "error" for s, _ in errs)


def test_floor_findings_empty_when_all_pass():
    assert S._floor_findings("sc", [("a", 26.0), ("b", 99.0)], 26.0, enforce=False) == []


def test_floor_uses_theme_constant():
    assert isinstance(T.MIN_FONT_FLOOR, float) and T.MIN_FONT_FLOOR > 0


if __name__ == "__main__":
    test_effective_px_recovers_authored_size()
    test_floor_findings_flags_below()
    test_floor_findings_enforce_is_error()
    test_floor_findings_empty_when_all_pass()
    test_floor_uses_theme_constant()
    print("OK sizecheck self-test")
```

- [ ] **Step 3: Run it to confirm it FAILS.** `.venv/Scripts/python.exe video/pipeline/_selftest_sizecheck.py`
Expected: `AttributeError: module 'pipeline.sizecheck' has no attribute '_effective_font_px'`.

- [ ] **Step 4: Implement.** In `video/pipeline/sizecheck.py`:

```python
def _effective_font_px(node):
    """The node's TRUE authored on-screen px, recovered from its manim font_size.
    text Tex renders at fs(px)*TEXT_SCALE; pure-math MathTex renders at fs(px)=px*PX_TO_FS.
    CRITICAL: in this manim `Tex` SUBCLASSES `MathTex` (.venv .../tex_mobject.py:227,607), so a
    text Tex IS-A MathTex -- you MUST test `Tex` FIRST, else every text node is mis-typed as
    math (and Step-2's `Tex("x")` assert fails on first run)."""
    from manim import MathTex, Tex
    from pipeline.visuals import theme as T
    fs = float(node.font_size)
    if isinstance(node, Tex):                       # text prose (carries TEXT_SCALE) -- Tex FIRST!
        return fs / (T.TEXT_SCALE * T.PX_TO_FS)
    if isinstance(node, MathTex):                   # pure-math carrier (no TEXT_SCALE)
        return fs / T.PX_TO_FS
    return fs / T.PX_TO_FS  # plain Text (no TEXT_SCALE); confirm against brand if such nodes occur


def _floor_findings(scene_id, sizes, floor, enforce):
    """(severity, message) for each (block_id, px) below `floor`. Pure: no manim."""
    sev = "error" if enforce else "warn"
    return [(sev, f"{scene_id}: '{bid}' renders at {px:.1f}px < MIN_FONT_FLOOR {floor:.0f}px "
                  f"-- too small to read (a line shrank below the floor, or an explicit tiny size)")
            for bid, px in sizes if px < floor]
```

Then add `_floor_issues(scene, blocks, enforce)` that collects `(block_id, _effective_font_px(node))` over the scene's `_brand_prose` nodes — **reuse `_prose_nodes(...)`** (read `sizecheck.py:40` for how it walks; do NOT re-implement) and additionally include the pure-inline-math single-line carriers that `_block_prose_size` filters out (`sizecheck.py:74–77`) — then `return _floor_findings(scene.get("id"), sizes, T.MIN_FONT_FLOOR, enforce)`. Call it from `check_scenes(meta, scenes)` after the existing checks:

```python
    enforce = bool(meta.get("fontfloor_enforce"))
    for scene, blocks in <the same (scene, built-blocks) pairs the TOLERANCE walk uses>:
        issues += _floor_issues(scene, blocks, enforce)
```

(Reuse the exact block source `check_scenes` already builds for TOLERANCE — read the function to find it; do not rebuild blocks.) While here, fix the stale return annotation on `check_scenes` and `check_file` (`list[str]` → `list[tuple[str, str]]`).

- [ ] **Step 5: Run to confirm PASS.** `.venv/Scripts/python.exe video/pipeline/_selftest_sizecheck.py` → `OK sizecheck self-test`.

- [ ] **Step 6: Commit.**

```bash
git add video/pipeline/visuals/theme.py video/pipeline/sizecheck.py video/pipeline/_selftest_sizecheck.py
git commit -m "feat(sizecheck): MIN_FONT_FLOOR + _effective_font_px + warn-default floor check (SPEC §8)"
```

---

### Task 2: Opt-in enforce wiring + run the floor check on real decks (pre-clamp surface)

**Files:**
- Modify: `video/make.py` (sizecheck block ~`:617`); `video/pipeline/sizecheck.py` (`main()` if it filters messages); `video/pipeline/_selftest_sizecheck.py` (enforce assertion)

**Interface:** no `meta.fontfloor_enforce` → floor findings are `warn` (printed, never gate). With it → `error` (make.py aborts `return 2`; `sizecheck.py main()` returns 1). Independent of `otf_enforce`/`pedagogy_enforce`.

- [ ] **Step 1: Confirm the standalone CLI + make.py surface the floor.** Read `sizecheck.py main()` (~`:531`) and the `make.py` sizecheck block (~`:617–629`). The floor findings are already in the `check_scenes` return list, so the existing error/warn split prints/gates them. The floor warns already print as `WARN <msg>` lines (`make.py` prints all warns before the `[sizecheck] consistent` line) — **no new `[fontfloor]` block header is needed** (unlike schema.py's `[provenance]`/`[pedagogy]` blocks). Only adjust wording if the warns are genuinely suppressed.

- [ ] **Step 2: Add an enforce assertion** to `_selftest_sizecheck.py` (render-free): assert `_floor_findings(..., enforce=True)` yields `error` (already covered) and that the `meta.fontfloor_enforce` flag is read where `check_scenes` builds `enforce` (a focused assert; keep it render-free — the full render path is exercised in Task 5).

- [ ] **Step 3: Run the floor check on the 3 real decks BEFORE any clamp lands (the pre-clamp surface).** Run, with NO enforce key:
```
.venv/Scripts/python.exe video/pipeline/sizecheck.py video/storyboards/ch01_inverse_functions.yml
.venv/Scripts/python.exe video/pipeline/sizecheck.py video/storyboards/ch03_trig_derivatives.yml
.venv/Scripts/python.exe video/pipeline/sizecheck.py video/storyboards/ch03_chain_rule.yml
```
Expected exit 0 (warn-default). **Record every floor WARN** (scene · block · px). These are the decks' current sub-floor cases — the surface the clamp will fix (and the SP2 backfill surface). If a WARN names a legit `eyebrow`/`caption` node, the unit recovery is off → re-check `_effective_font_px` against `brand`'s actual node type before proceeding (D-P4-1 calibration).

- [ ] **Step 4: Run the self-test.** `.venv/Scripts/python.exe video/pipeline/_selftest_sizecheck.py` → `OK sizecheck self-test`.

- [ ] **Step 5: Commit.**

```bash
git add video/make.py video/pipeline/sizecheck.py video/pipeline/_selftest_sizecheck.py
git commit -m "feat(sizecheck): floor check opt-in via meta.fontfloor_enforce (warn-default, real-deck surface recorded)"
```

(Record the Step-3 per-deck floor surface in the commit body — it is the pre-clamp baseline the next task's no-op check is measured against.)

---

### Task 3: Unconditional clamp (`_clamp_shrink`) — TDD core + no-op verified BEFORE commit

**Files:**
- Modify: `video/pipeline/brand.py`, `video/pipeline/templates/derivation.py`, `video/pipeline/templates/graph.py`, `video/pipeline/_selftest_sizecheck.py`

**Interface:** `_clamp_scale(cur_w, max_w, cur_size, floor) -> float` — pure: `1.0` if `cur_w <= max_w` or `cur_w <= 0`; else `min(1.0, max(max_w/cur_w, floor/cur_size))` (fit, but never below the floor-scale; never enlarge). `_clamp_shrink(mob, max_w, cur_size_px)` — the **call site passes `cur_size_px`** (the role's authored px; required because a `VGroup` reason has no single `font_size`); applies `mob.scale(_clamp_scale(mob.width, max_w, cur_size_px, theme.MIN_FONT_FLOOR))`.

- [ ] **Step 1: Write the failing `_clamp_scale` tests** in `_selftest_sizecheck.py`:

```python
from pipeline import brand as B  # noqa: E402

def test_clamp_no_shrink_when_fits():
    assert B._clamp_scale(3.0, 5.0, 40.0, 26.0) == 1.0

def test_clamp_fits_when_result_above_floor():
    # shrink 5->4 (0.8x); 40*0.8=32 >= 26 -> use fit
    assert abs(B._clamp_scale(5.0, 4.0, 40.0, 26.0) - 0.8) < 1e-9

def test_clamp_stops_at_floor():
    # fit would be 0.5x -> 40*0.5=20 < 26; clamp to floor scale 26/40=0.65
    assert abs(B._clamp_scale(10.0, 5.0, 40.0, 26.0) - 0.65) < 1e-9

def test_clamp_never_enlarges():
    assert B._clamp_scale(2.0, 9.0, 20.0, 26.0) == 1.0

def test_clamp_zero_width_safe():
    assert B._clamp_scale(0.0, 5.0, 40.0, 26.0) == 1.0
```

Add the five calls to `__main__`.

- [ ] **Step 2: Run to confirm FAIL.** → `AttributeError: … '_clamp_scale'`.

- [ ] **Step 3: Implement the helpers** in `video/pipeline/brand.py`:

```python
def _clamp_scale(cur_w, max_w, cur_size, floor):
    """Scale factor to fit max_w without shrinking effective size below `floor`. Never enlarges."""
    if max_w is None or max_w <= 0 or cur_w <= max_w or cur_w <= 0:
        return 1.0
    fit = max_w / cur_w
    floor_scale = floor / cur_size if cur_size > 0 else fit
    return min(1.0, max(fit, floor_scale))


def _clamp_shrink(mob, max_w, cur_size_px):
    """In-place: shrink mob to fit max_w but not below theme.MIN_FONT_FLOOR. The caller passes
    cur_size_px (the role's authored px) -- required for VGroup reasons with no single font_size.
    Drop-in for mob.scale_to_fit_width(max_w) at the single-line sites (SPEC §8)."""
    factor = _clamp_scale(mob.width, max_w, float(cur_size_px), T.MIN_FONT_FLOOR)
    if factor < 1.0:
        mob.scale(factor)
    return mob
```

(Confirm `T` is brand.py's theme alias.)

- [ ] **Step 4: Replace the raw calls, each passing its role px.** At `brand.py:398` (`prose()` pure-`$math$`), `brand.py:144` (`heading`), `brand.py:440` (`heading_rich`), `derivation.py:180` (reason-rail), `graph.py:143` (`_title`): replace `mob.scale_to_fit_width(max_w)` with `brand._clamp_shrink(mob, max_w, <role px>)`, where `<role px>` is the site's ACTUAL effective px — **do not assume a named size** (Codex I1): the reason rail is `prose_sm` → `theme._SCALE_PX['prose_sm']`; the graph `_title` rich (contains `$`) is `_SCALE_PX['h1'] * 0.88` and plain is `_SCALE_PX['h1']` (`graph.py:137–143`), so compute `size_px = T._SCALE_PX['h1'] * 0.88 if '$' in text else T._SCALE_PX['h1']` and pass that; `heading`/`heading_rich` pass their own size role's px. Read each site to pass the correct px; do not read `font_size` off a possibly-grouped mob.

- [ ] **Step 5: Run the self-test → PASS.** `.venv/Scripts/python.exe video/pipeline/_selftest_sizecheck.py` → `OK sizecheck self-test`.

- [ ] **Step 6: Verify the clamp is a no-op on existing decks — BEFORE committing (Codex I3).** For each locked deck: render base (pre-Step-3) vs HEAD (edits applied) and diff final frames. **Path-limit the stash** so unrelated tracked edits (e.g. the self-test from earlier steps) are NOT swept up:
```
git status --short                                                                                      # confirm only the clamp files are dirty
git stash push -- video/pipeline/brand.py video/pipeline/templates/derivation.py video/pipeline/templates/graph.py   # stash ONLY the clamp edits
python video/scratch_frames.py --storyboard video/storyboards/ch03_trig_derivatives.yml --scene all --out video/output/_qa/clamp_base   # base (no clamp)
git stash pop                                                                                            # re-apply the clamp edits
python video/scratch_frames.py --storyboard video/storyboards/ch03_trig_derivatives.yml --scene all --out video/output/_qa/clamp_head   # head (clamp)
```
(If `stash pop` conflicts, the tree had other edits to those files — resolve before continuing.)
Compare the PNGs (byte/pixel diff) for all 3 decks. **Expected: byte-identical** (no current line needed sub-floor shrink → clamp inert; cross-check against Task 2 Step 3 — the decks whose floor surface was empty MUST be byte-identical). If a deck DIFFERS: a scene was shrinking below the floor; capture the scene id, **do NOT commit** — surface to the user (fix now vs SP2). Only commit once no-op is confirmed (or the user accepts the specific render change).

- [ ] **Step 7: Commit** (only after Step 6 passes).

```bash
git add video/pipeline/brand.py video/pipeline/templates/derivation.py video/pipeline/templates/graph.py video/pipeline/_selftest_sizecheck.py
git commit -m "feat(brand): clamp single-line scale_to_fit_width to MIN_FONT_FLOOR (no-op on existing decks; SPEC §8)"
```

---

### Task 4: Rubric extension (V4/A6 floor + mobile yardstick, A7 figure-prominence) + agent V-code refresh

**Files:**
- Modify: `video/content_scripts/_audit/VISUAL-FRAME-RUBRIC.md`; `.claude/agents/visual-frame-audit.md`

- [ ] **Step 1: Extend V4 (Layer 1, rubric line ~23).** Add: a `_brand_prose` text node whose **true on-screen size falls below `MIN_FONT_FLOOR` (26px, the deterministic floor in `theme.py`/`sizecheck.py`)** is "too small to read"; if that makes a **load-bearing value** unreadable → **Blocking** (consistent with V4's existing "小到讀不到值 → Blocking"); merely small-but-legible → defer to A6. Reference the `sizecheck.py` floor (warn-default) as the engineering counterpart that surfaces it pre-render.

- [ ] **Step 2: Extend A6 (Layer 2, rubric line ~40) — mobile yardstick.** Add: secondary text (reason-rail, annotations, captions) should stay readable when the frame is **downscaled to phone width** (~360–414px-wide viewport, i.e. the 1920px frame at ~0.2×); if a reason/annotation would be unreadable there → A6 deduction (severity by how far). State this is a **judgment** yardstick the agent applies by eye on the rendered frame, complementing the deterministic desktop floor.

- [ ] **Step 3: Add the A7 figure-prominence sub-criterion (Layer 2, rubric line ~41).** Append to A7: for scenes whose **core is geometric intuition** (hook / graph-centric, where "look at this shape/graph" IS the beat), the **figure should visually dominate** — the agent makes an **approximate measurement of the figure's share of the content area** (honoring §8's "由量測圖佔幀比例判定"); if it is well below ~half when the beat is fundamentally about the figure → deduct A7 (advisory magnitude, severity by how crowded). State: this is **agent-estimated on the frame** (no new code), **never** a V-blocking, and **never** fires on text-centric scenes (definitions/derivations where the figure is a supporting aside).

- [ ] **Step 4: Self-consistency check (no run).** (a) V4 blocking only when a load-bearing value is unreadable (else A6); (b) A6 mobile yardstick advisory; (c) A7 prominence advisory + approximate-measurement wording + scoped to geometric-core scenes; (d) all name the floor / measurement boundary correctly; (e) no new V/A code (§8).

- [ ] **Step 5: Refresh the agent's stale V-code count (D-P4-5).** In `.claude/agents/visual-frame-audit.md`, change `V1–V8`→`V1–V9` at **lines 4, 15, 25, 27**. Do NOT otherwise edit the agent (it points to the rubric, doesn't restate it).

- [ ] **Step 6: Commit.**

```bash
git add video/content_scripts/_audit/VISUAL-FRAME-RUBRIC.md .claude/agents/visual-frame-audit.md
git commit -m "docs(visual): V4/A6 min-size floor + mobile yardstick, A7 figure-prominence; agent V1-V8->V1-V9"
```

---

### Task 5: Calibration + visual verification + sign-off + whole-branch review

**Files:**
- Create (committed): `video/storyboards/_fixtures/fontfloor.yml`. Create (scratchpad, not committed): an "open and read" HTML sign-off report.
- Possibly modify: `theme.MIN_FONT_FLOOR` / rubric thresholds (if calibration shows a false positive).

- [ ] **Step 1: Verify the CLAMP works (would-shrink fixture).** Create `video/storyboards/_fixtures/fontfloor.yml`: a schema-valid deck with one `derivation` scene whose reason, at its declared `reason_max_w`, WOULD shrink below 26px. Mock-render its final frame (`python video/scratch_frames.py --storyboard video/storyboards/_fixtures/fontfloor.yml --scene all --out video/output/_qa/floor`). Confirm the reason renders at the **floor** (legible, overflowing/wrapping) — NOT tiny. (This proves the clamp; the reason will NOT trip the floor CHECK precisely because the clamp held it at ≥ floor — that is correct, not a failure.)

- [ ] **Step 2: Verify the CHECK fires (clamp-independent).** The floor check's positive case is the **unit test** (Task 1, `_floor_findings` on a synthetic `<floor` size) — that is the authoritative proof. For an end-to-end confirmation of the wiring + message, temporarily set `theme.MIN_FONT_FLOOR` **above a real CHECKED prose size** (Codex C2): the floor only walks `_brand_prose` nodes, and `eyebrow` (26) is NOT one — a reason rail is `prose_sm` (35). So set `MIN_FONT_FLOOR = 36.0` (just above 35), run `sizecheck.py` on a deck with a reason rail (`fontfloor.yml` or `ch03_trig_derivatives.yml`), and confirm a **`WARN` line** naming the reason block + containing `MIN_FONT_FLOOR` appears at exit 0 — sizecheck prints findings as `WARN <msg>`, there is **no `[fontfloor]` block header**, do not expect one. Then **restore `MIN_FONT_FLOOR = 26.0`**. Record both. (Do not leave the floor raised.)

- [ ] **Step 3: Calibrate the floor value + confirm no false positives on real decks.** With `MIN_FONT_FLOOR = 26.0`, the Task-2 Step-3 real-deck run should have shown either no floor WARN or only genuinely-too-small text. If a legit node tripped it, the `_effective_font_px` recovery is wrong for that node type — fix the helper (not the floor) and re-run; only lower the floor if a real intentional size legitimately sits below 26 (record why).

- [ ] **Step 4: Visual gate-1 audit (judgment layer).** Mock-render a geometric-core deck (ch03 §3.1 squeeze/graph scenes) → `python video/pipeline/critic.py --storyboard video/storyboards/ch03_trig_derivatives.yml --dry-run` → dispatch the `visual-frame-audit` gate-1 agent on the extracted frames. Confirm it now applies the V4/A6 floor + mobile yardstick + A7 figure-prominence per the rubric, and that **A7/V4 visual blocking == 0** on the (good) real decks (§14). Capture its VERDICT.

- [ ] **Step 5: Produce the sign-off report.** Standalone HTML (CDN MathJax/KaTeX, double-click) summarizing: `MIN_FONT_FLOOR` + the `_effective_font_px` recovery + the warn-default/opt-in model + the clamp; the rubric V4/A6 floor + mobile yardstick + A7 prominence; and the calibration result (clamp holds the would-shrink reason at floor; check fires under the temporary-raised-floor probe; real decks clean / the recorded sub-floor surface; clamp byte-identical no-op on the 3 decks; gate-1 A7/V4 blocking == 0). Per CLAUDE.md sign-off culture.

- [ ] **Step 6: Commit the fixture + user sign-off.**
```bash
git add video/storyboards/_fixtures/fontfloor.yml
git commit -m "test(sizecheck): fontfloor fixture (clamp-holds-at-floor) + Plan 4 calibration record"
```
Present the report; get sign-off on the floor value + the rubric judgments + the no-op verification before considering Plan 4 done.

- [ ] **Step 7: Plan 4 whole-branch review.** Opus whole-branch review of the changeset (theme/sizecheck/brand/templates/rubric/agent + tests + fixture): is `_effective_font_px` correct per node type? Is the floor check warn-default + correctly opt-in + scoped to `_brand_prose`? Is the clamp arithmetic correct, size-from-call-site, VGroup-safe, and the render no-op verified? Are the rubric edits §8-faithful (no new V/A code; A7 advisory + approximate-measurement)? Address findings, re-audit. (Optionally offer the user a billed Codex independent pass, per the Plan-3 precedent + CLAUDE.md consent.)

- [ ] **Step 8: Update progress anchors + finish.** Update `REBUILD_STATUS.md` + `HANDOFF-pedagogy-firstlearner-sp1.md`: Plan 4 ✅ (visual extension landed — floor constant + `_effective_font_px` + warn-default check + clamp + rubric V4/A6/A7; non-gating; no-op verified; calibrated, signed off); next = Plan 5. Then `superpowers:finishing-a-development-branch`.

---

## After Plan 4 lands

- **Plan 5 — Methodology/doc wiring (§12):** `CONTENT_METHODOLOGY.md` (P1/P2/P4 + scaffold authoring), `DESIGN.md` (scaffold 承載 + authoring checklist + the now-enforced P5/P6 visual rules), `CONTENT-SIXLENS-RUBRIC.md` L1 scaffold exception (§5.5 exact wording), `REVIEW_GATES.md` (pedagogy + fontfloor gates in sequence) + the remaining **V1–V8→V1–V9 doc-drift** (`REVIEW_GATES.md` line 65/66, `DESIGN.md` ~621/636 — the agent locus was fixed in Plan 4 Task 4 / D-P4-5).
- **Graph-label / axis-tick floor coverage** (deliberately out of Plan 4 scope, Codex I2): if wanted, extend the floor check to `_graph_labels()` after resolving label Tex/MathTex size metadata — a scoped Plan-5 / SP2 follow-up.
- **SP2 backfill** applies Plans 1–4 to the 3 locked decks per spec §11 (dry-run → classify → user-approved migration list → scoped fix → re-gate/re-render/re-sign-off), flipping per-deck opt-in (`otf_enforce` / `pedagogy_enforce` / `fontfloor_enforce`) to gating. The fontfloor surface recorded in Task 2 Step 3 is part of that SP2 surface.

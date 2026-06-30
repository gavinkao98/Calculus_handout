# Visual Extension (min-size floor + A7 figure-prominence + mobile yardstick) — Implementation Plan (SP1, Plan 4 of 5)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. All self-tests run with the **repo venv python** `.venv/Scripts/python.exe` (bare `python` lacks vendored PyYAML and misjudges).

**Goal:** Sharpen the **existing** visual-frame gate per spec §8 (P5/P6, Codex C — "sharpen 既有、不立新 code"): add a deterministic **minimum on-screen font-size floor** (a `theme.py` constant + a warn-default `sizecheck.py` check + an unconditional render-time clamp so a single line can't `scale_to_fit_width` below the floor), and extend the `VISUAL-FRAME-RUBRIC.md` **judgment layer** (V4/A6 numeric floor + a phone-width "mobile yardstick", A7 **figure-prominence** sub-criterion). Lands **non-gating** (check is warn-default + opt-in `meta.fontfloor_enforce`; the clamp is an always-correct engineering fix verified to be a **no-op on existing decks**).

**Architecture:** Two layers, mirroring Plans 1–3. **(1) Deterministic** — `theme.MIN_FONT_FLOOR` (px, compared in the canonical scale the existing `sizecheck._norm_size` already produces); a `sizecheck.py` floor check that flags any prose/label node whose effective size falls below the floor (incl. the pure-inline-math reason rails the existing `TOLERANCE` consistency check deliberately skips), warn-by-default and flipped to `error` only under `meta.fontfloor_enforce`; and a shared `brand._clamp_shrink` helper that prevents the single-line `scale_to_fit_width` sites from shrinking past the floor (wrap/overflow instead, consistent with DESIGN.md "wrap, don't shrink"). **(2) Judgment** — rubric edits the read-only `visual-frame-audit` gate-1 agent applies on rendered-frame PNGs. TDD for the deterministic core (a manim-free pure function + stdlib-assert self-test); offline mock-render + gate-1 audit for visual verification.

**Tech Stack:** Python (stdlib + manim) for `theme.py`/`sizecheck.py`/`brand.py`/templates; markdown for `VISUAL-FRAME-RUBRIC.md`; stdlib-`assert` self-test (new `_selftest_sizecheck.py`, pattern-identical to `_selftest_provenance.py`); offline `make.py --backend mock` / `scratch_frames.py` / `critic.py --dry-run` for visual verification (all $0, offline).

---

## Global Constraints

- **Spec authority:** `SPEC-pedagogy-firstlearner-framework.md` — **§8** (the visual extension: P5→A7 figure-prominence; P6→V4/A6 min-size floor + mobile; engineering = floor constant + clamp single-line shrink), **§9** (deterministic layer is warn-default + per-deck opt-in enforce — "所有新檢查預設 warn-only"), **§12** (change-landing: `VISUAL-FRAME-RUBRIC.md` A7/V4/A6; `theme.py`/`sizecheck.py` floor constant + clamp), **§14** (success: "新檢查（warn 模式）綠/紅正確"; convergence "A7/V4 視覺 blocking == 0"; "全程離線可驗"). This plan implements **only §8**. The methodology/doc wiring (`CONTENT_METHODOLOGY.md`, `DESIGN.md`, `REVIEW_GATES.md` gate-sequence, the broader V1–V8→V1–V9 doc-drift) is **Plan 5**.
- **Sharpen, don't add new codes (§8, Codex C).** No new V-code or A-code. The floor extends V4/A6; figure-prominence extends A7. All three already exist in `VISUAL-FRAME-RUBRIC.md` (V4 line 23, A6 line 40, A7 line 41).
- **Deterministic floor lands non-gating (§9 / §14).** The `sizecheck.py` floor check is **warn-default**; it flips to `error` (gating) only when the deck sets `meta.fontfloor_enforce: true` (a NEW key, **independent of** `otf_enforce`/`pedagogy_enforce` — each gate owns its key, per Plan-2 precedent). **Zero behavior change on landing** — no existing deck sets the flag, so render output and exit codes are unchanged.
- **The clamp is unconditional but must be a no-op on existing decks.** Unlike the check, the `_clamp_shrink` render-time fix has no opt-in (it is always-correct "wrap, don't shrink"). But it must not silently change existing renders: Task 5 verifies, by mock-rendering the 3 locked decks (ch01 §1.1, ch03 §3.1, §3.2) base-vs-HEAD, that **no current line shrinks below the floor** → frames byte-identical. If calibration finds a deck that DOES shrink below floor, that is a pre-existing too-small-text case → surface it (the floor warn names it) and raise it with the user (fix now vs SP2), do NOT silently change the render.
- **Floor reasons in effective on-screen size, not raw `font_size` (grounding correction).** `theme.fs(size)` returns manim units `= px * PX_TO_FS` (PX_TO_FS≈0.698); **text** additionally renders at `fs(size) * TEXT_SCALE` (TEXT_SCALE≈1.3102, `brand._text_fs`). The existing `sizecheck._norm_size(node, text_scale)` already recovers the canonical math-anchored size (divides a Tex/MathTex `font_size` by `TEXT_SCALE`). **The floor check MUST compare against `_norm_size(...)`, reusing that helper — do not invent new normalization.** `MIN_FONT_FLOOR` is therefore expressed in the same canonical px units `_norm_size` yields.
- **TDD for code.** Each code task: write the failing stdlib-`assert` self-test first, run it to see it fail, implement the minimal change, run it to see it pass, commit. Keep the unit-tested core **manim-free** (a pure function over `(block_id, size)` pairs), matching how `_selftest_provenance.py` / `_selftest_pedagogy.py` keep logic manim-free and push manim/end-to-end to a subprocess or to manual calibration (see `provenance.py:153–159` note).
- **Surgical (Karpathy, CLAUDE.md).** Touch only the files named per task. Match each file's existing style. Do not "improve" adjacent code. The agent V1–V8→V1–V9 staleness fix is scoped explicitly in D-P4-5 (do not broaden it).
- **Offline only.** Mock render (`--backend mock`), `scratch_frames.py`, `critic.py --dry-run` are $0. The gate-1 `visual-frame-audit` subagent is a free Claude agent. Any billed step (external VLM `critic.py --confirm`, high-res real render, Codex review) is **consent-gated** (CLAUDE.md) — propose + price first.

## Decisions (LOCKED by this plan — review here first)

- **D-P4-1 — floor value + units.** `theme.MIN_FONT_FLOOR` is a **px** constant in the canonical scale `_norm_size` yields. **Initial value = `26.0`** — the smallest *intentional* named size (`eyebrow`=26 in `theme._SCALE_PX`), so every deliberate size (`eyebrow`/`caption`/`prose_sm`/`math_sm`/… ≥26) passes and only sub-floor **shrink** (or an explicit too-small size) is caught. The check fires on `effective_size < MIN_FONT_FLOOR` (strict `<`, so a node exactly at the floor passes). **Calibrated in Task 5**: confirm no false positive on the 3 real decks; if a legit node trips it, lower the floor by the smallest amount that clears it (and record why). The value is one constant — trivially tunable.
- **D-P4-2 — floor CHECK is warn-default + opt-in.** New key `meta.fontfloor_enforce` (bool). `sizecheck.check_scenes` reads it and emits floor findings as `warn` (default) or `error` (when set). Wired into the existing `make.py` sizecheck block (which already prints warns and aborts on errors) and surfaced by `sizecheck.py main()`. **Not** wired into `schema.py` (sizecheck is a separate make.py-only gate; `sizecheck.py` has its own CLI/`main()` for standalone runs). Zero behavior change on landing.
- **D-P4-3 — CLAMP is unconditional + no-op-verified.** A shared `brand._clamp_shrink(mob, max_width)` (uses `theme.MIN_FONT_FLOOR`) replaces the raw `mob.scale_to_fit_width(max_width)` at the **two primary sites** — `brand.py:398` (pure-`$math$` single-line `prose()` branch) and `templates/derivation.py:180` (reason-rail). It also replaces the raw calls at the **three standalone-title sites** for consistency — `brand.py:144` (`heading`), `brand.py:440` (`heading_rich`), `templates/graph.py:143` (`_title`). Behavior: shrink to fit width **only down to the floor**; if fitting would require going below the floor, stop at the floor and let it overflow/wrap (DESIGN.md §599–609 "wrap, don't shrink"; titles already prefer wrapping). The clamp's *arithmetic* is a pure manim-free helper `_clamp_scale(cur_w, max_w, cur_size, floor) -> float` (unit-tested); the mobject application wraps it.
- **D-P4-4 — A7 prominence + V4/A6 floor + mobile are JUDGMENT (rubric), no new code (§8).** The `visual-frame-audit` agent reads `VISUAL-FRAME-RUBRIC.md` as SSOT and applies them on rendered frames. **A7 figure-prominence**: for scenes whose core IS geometric intuition (hook / graph-centric content), the figure should visually dominate; if text/whitespace crowds it so it is **not** the focus (rough guide: figure occupies less than ~half the content area when the beat is "look at this shape/graph"), deduct A7 (advisory magnitude — never a V-blocking). **V4/A6 floor**: name `MIN_FONT_FLOOR` (26px) as the numeric reference — text rendered below it is "too small to read" → V4 blocking if it makes a load-bearing value unreadable, else A6 deduction. **Mobile yardstick**: a one-line rule to sanity-check secondary text (reason-rail / annotations) at phone width (~the frame downscaled to a 360–414px-wide viewport) — if it would be unreadable there, A6 deduction. These are agent judgments, not measured by code.
- **D-P4-5 — agent V1–V8→V1–V9 staleness fix (scoped-in here).** `.claude/agents/visual-frame-audit.md` still says "V1–V8" (lines 5/15/25/27–28/32) while `VISUAL-FRAME-RUBRIC.md` is already V1–V9. Since Plan 4 edits the rubric the agent applies, fix the agent's stale `V1–V8`→`V1–V9` references **in Task 4** (one-locus, surgical). The OTHER two stale loci the spec §12 names (`REVIEW_GATES.md` line 65/66, `DESIGN.md` ~621/636) stay **Plan 5** — do not touch them here.

## File Structure

- **Modify** `video/pipeline/visuals/theme.py` — add `MIN_FONT_FLOOR` constant in the type-scale block (after `_SCALE_PX`/`PX_TO_FS`/`TEXT_SCALE`). One responsibility: own the type-system constant.
- **Modify** `video/pipeline/sizecheck.py` — add a manim-free pure core `_floor_findings(scene_id, sizes, floor, enforce)` + a `_floor_issues(scene, blocks, enforce)` extractor that reuses `_prose_nodes`/`_norm_size` and ALSO checks the pure-inline-math carriers the TOLERANCE filter skips; call it from `check_scenes` with `enforce = bool(meta.get("fontfloor_enforce"))`.
- **Create** `video/pipeline/_selftest_sizecheck.py` — stdlib-assert self-test for the floor pure-core + the clamp pure-core (manim-free), following `_selftest_provenance.py` shape.
- **Modify** `video/pipeline/brand.py` — add `_clamp_scale` (pure) + `_clamp_shrink` (mobject) helpers; replace raw `scale_to_fit_width` at `:144`, `:398`, `:440`.
- **Modify** `video/pipeline/templates/derivation.py` — use `_clamp_shrink` at `:180` (reason-rail).
- **Modify** `video/pipeline/templates/graph.py` — use `_clamp_shrink` at `:143` (graph title).
- **Modify** `video/make.py` — the sizecheck block (~`:617`) prints a `[fontfloor]`-tagged note line; gating already handled by the existing error/warn split (no structural change — confirm the floor findings flow through).
- **Modify** `video/content_scripts/_audit/VISUAL-FRAME-RUBRIC.md` — V4/A6 numeric floor + mobile yardstick; A7 figure-prominence sub-criterion.
- **Modify** `.claude/agents/visual-frame-audit.md` — V1–V8→V1–V9 staleness fix (D-P4-5).
- **Create** `video/storyboards/_fixtures/fontfloor.yml` (+ backing `content_scripts/_fixture_fontfloor.md` if a `md:` ref is needed) — a deck with a deliberately-below-floor scaled line, for Task 5 calibration of the end-to-end floor warn.

---

### Task 1: `MIN_FONT_FLOOR` constant + the deterministic floor check (sizecheck.py) — TDD

**Files:**
- Modify: `video/pipeline/visuals/theme.py` (type-scale block, after `_SCALE_PX`)
- Modify: `video/pipeline/sizecheck.py` (add `_floor_findings` pure core + `_floor_issues` extractor; call from `check_scenes`)
- Create: `video/pipeline/_selftest_sizecheck.py`

**Interface:** `_floor_findings(scene_id: str, sizes: list[tuple[str, float]], floor: float, enforce: bool) -> list[tuple[str, str]]` — pure, manim-free: for each `(block_id, effective_size)` with `effective_size < floor`, append `(sev, msg)` where `sev = "error" if enforce else "warn"`; message names the scene, the block, the size, and the floor. `_floor_issues(scene, blocks, enforce)` walks the scene's prose/label nodes (reuse `_prose_nodes`, `_norm_size`), builds the `sizes` list **including the pure-inline-math reason rails that `_block_prose_size`'s carriers filter (sizecheck.py:74–77) skips** (an absolute floor needs no sibling, so these CAN and SHOULD be checked), and delegates to `_floor_findings`.

- [ ] **Step 1: Add the constant.** In `video/pipeline/visuals/theme.py`, in the type-scale block right after the `_SCALE_PX` dict / `PX_TO_FS` / `TEXT_SCALE`:

```python
# Minimum readable on-screen font size, in the canonical math-anchored px scale that
# sizecheck._norm_size yields (a Tex/MathTex font_size divided back out by TEXT_SCALE).
# Set at the smallest INTENTIONAL named size (`eyebrow`=26) so every deliberate size passes
# and only sub-floor shrink (or an explicit too-small size) is caught. Plan 4 / SPEC §8.
MIN_FONT_FLOOR = 26.0  # px (canonical scale); calibrated in PLAN-…-plan4 Task 5
```

- [ ] **Step 2: Write the failing self-test.** Create `video/pipeline/_selftest_sizecheck.py`:

```python
"""Stdlib assert self-test for sizecheck.py floor logic. Run: .venv/Scripts/python.exe video/pipeline/_selftest_sizecheck.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import sizecheck as S  # noqa: E402
from pipeline.visuals import theme as T  # noqa: E402


def test_floor_findings_flags_below():
    floor = 26.0
    sizes = [("reason.0", 24.0), ("reason.1", 26.0), ("statement", 40.0)]  # only reason.0 < floor
    warns = S._floor_findings("sc", sizes, floor, enforce=False)
    msgs = " | ".join(m for _, m in warns)
    assert all(s == "warn" for s, _ in warns)
    assert len(warns) == 1
    assert "reason.0" in msgs and "sc" in msgs        # names scene + block
    assert "reason.1" not in msgs and "statement" not in msgs   # at/above floor pass


def test_floor_findings_enforce_is_error():
    errs = S._floor_findings("sc", [("a", 10.0)], 26.0, enforce=True)
    assert errs and all(s == "error" for s, _ in errs)


def test_floor_findings_empty_when_all_pass():
    assert S._floor_findings("sc", [("a", 26.0), ("b", 99.0)], 26.0, enforce=False) == []


def test_floor_uses_theme_constant():
    assert isinstance(T.MIN_FONT_FLOOR, float) and T.MIN_FONT_FLOOR > 0


if __name__ == "__main__":
    test_floor_findings_flags_below()
    test_floor_findings_enforce_is_error()
    test_floor_findings_empty_when_all_pass()
    test_floor_uses_theme_constant()
    print("OK sizecheck self-test")
```

- [ ] **Step 3: Run it to confirm it FAILS.** Run: `.venv/Scripts/python.exe video/pipeline/_selftest_sizecheck.py`
Expected: `AttributeError: module 'pipeline.sizecheck' has no attribute '_floor_findings'`.

- [ ] **Step 4: Implement the pure core + the extractor.** In `video/pipeline/sizecheck.py`, add the manim-free `_floor_findings`:

```python
def _floor_findings(scene_id, sizes, floor, enforce):
    """(severity, message) for each (block_id, effective_size) below `floor`. Pure: no manim.
    severity = 'error' if enforce else 'warn' (the warn-default/opt-in gating axis)."""
    sev = "error" if enforce else "warn"
    out = []
    for bid, size in sizes:
        if size < floor:
            out.append((sev, f"{scene_id}: '{bid}' renders at {size:.1f} < MIN_FONT_FLOOR "
                             f"{floor:.0f} -- too small to read (a line was shrunk below the floor)"))
    return out
```

Then add `_floor_issues(scene, blocks, enforce)` that builds the `sizes` list from the scene's prose/label nodes **using the existing `_prose_nodes(...)` + `_norm_size(node, T.TEXT_SCALE)` helpers** (read sizecheck.py:40–77 to match exact node-walking; reuse them, do NOT re-implement normalization), and — unlike the TOLERANCE path — **include the pure-inline-math single-line carriers** that `_block_prose_size` skips (lines 74–77), since an absolute floor needs no sibling group. Call `_floor_findings(scene.get("id"), sizes, T.MIN_FONT_FLOOR, enforce)`. Finally, in `check_scenes(meta, scenes)`, after the existing checks, add:

```python
    enforce = bool(meta.get("fontfloor_enforce"))
    for scene in scenes:
        issues += _floor_issues(scene, <the scene's built blocks>, enforce)
```

(Match how `check_scenes` already iterates scenes and obtains each scene's blocks for the TOLERANCE walk — reuse that same block source so the floor check sees the same nodes.)

- [ ] **Step 5: Run the self-test to confirm it PASSES.** Run: `.venv/Scripts/python.exe video/pipeline/_selftest_sizecheck.py`
Expected: `OK sizecheck self-test`.

- [ ] **Step 6: Commit.**

```bash
git add video/pipeline/visuals/theme.py video/pipeline/sizecheck.py video/pipeline/_selftest_sizecheck.py
git commit -m "feat(sizecheck): MIN_FONT_FLOOR + warn-default floor check (SPEC §8)"
```

---

### Task 2: Opt-in enforce wiring + zero-behavior-change confirmation

**Files:**
- Modify: `video/make.py` (sizecheck block ~`:617` — confirm floor findings print under the gate; add a `[fontfloor]` note only if the existing block does not already surface them clearly)
- Modify: `video/pipeline/sizecheck.py` (`main()` standalone CLI — confirm it prints the floor findings + that `meta.fontfloor_enforce` flips severity)
- Modify: `video/pipeline/_selftest_sizecheck.py` (add an enforce-key integration assertion)

**Interface:** with no `meta.fontfloor_enforce`, floor findings are `warn` → printed but **never gate** (make.py does not abort; `sizecheck.py main()` returns 0). With `meta.fontfloor_enforce: true`, they are `error` → make.py aborts (`return 2`) and `sizecheck.py main()` returns 1. The enforce key is **independent of** `otf_enforce`/`pedagogy_enforce`.

- [ ] **Step 1: Confirm the standalone CLI surfaces the floor.** Read `sizecheck.py main()` (line ~531) and `check_file` (line ~520). The floor findings are already in the `check_scenes` return list, so `main()`'s existing error/warn split prints them. Verify the WARN lines read sensibly (they carry "MIN_FONT_FLOOR"). No code change expected here unless `main()` filters messages — if so, ensure floor warns pass through.

- [ ] **Step 2: Confirm the make.py gate handles it.** Read `make.py` sizecheck block (lines ~617–629). Floor findings flow through the existing `errors`/`warns` partition: warns print as `WARN`, errors abort with `return 2`. Confirm no change needed; if the block hard-prints "[sizecheck] consistent" in a way that hides floor warns, adjust the wording to a `[sizecheck]`/`[fontfloor]` line that lists them (match the `[provenance]`/`[pedagogy]` warn-block idiom in `schema.py:179–197`).

- [ ] **Step 3: Add an enforce integration assertion** to `_selftest_sizecheck.py` (still manim-free — test the enforce **plumbing** at the `check_scenes` meta-reading level using a stub, OR assert the documented behavior via `_floor_findings` enforce param already covered in Task 1; if `check_scenes` can be exercised without manim for a scene with no blocks, assert `bool(meta.get("fontfloor_enforce"))` is read). Keep it manim-free; the end-to-end render-fires-the-warn path is verified in Task 5 (manual mock-render), mirroring the `provenance.py:153–159` rationale for not auto-testing the manim-dependent path.

- [ ] **Step 4: Confirm zero behavior change.** Run `sizecheck.py` on a real deck (no enforce key):
`.venv/Scripts/python.exe video/pipeline/sizecheck.py video/storyboards/ch03_trig_derivatives.yml`
Expected: exit 0 (warns may appear for any genuinely-small text — that is the new visibility, warn-only, non-gating). Note in the commit body whether any real-deck warn appeared (those are the SP2 surface, not regressions).

- [ ] **Step 5: Run the self-test.** `.venv/Scripts/python.exe video/pipeline/_selftest_sizecheck.py` → `OK sizecheck self-test`.

- [ ] **Step 6: Commit.**

```bash
git add video/make.py video/pipeline/sizecheck.py video/pipeline/_selftest_sizecheck.py
git commit -m "feat(sizecheck): floor check opt-in via meta.fontfloor_enforce (warn-default, zero behavior change)"
```

---

### Task 3: Unconditional clamp helper (`_clamp_shrink`) — TDD core + render no-op

**Files:**
- Modify: `video/pipeline/brand.py` (add `_clamp_scale` pure + `_clamp_shrink` mobject helper; replace raw `scale_to_fit_width` at `:144`, `:398`, `:440`)
- Modify: `video/pipeline/templates/derivation.py` (`:180`)
- Modify: `video/pipeline/templates/graph.py` (`:143`)
- Modify: `video/pipeline/_selftest_sizecheck.py` (add `_clamp_scale` unit tests)

**Interface:** `_clamp_scale(cur_w: float, max_w: float, cur_size: float, floor: float) -> float` — pure: the scale factor to apply so the mob fits `max_w` **but its resulting effective size stays ≥ floor**. If `cur_w <= max_w`: return `1.0` (no shrink). Else the fit-scale is `max_w / cur_w`; the floor-scale is `floor / cur_size`; return `max(fit_scale, floor_scale)` capped at `1.0` (never enlarge). `_clamp_shrink(mob, max_w)` reads the mob's current width + effective size, computes `_clamp_scale(..., theme.MIN_FONT_FLOOR)`, and applies `mob.scale(factor)` (replacing the raw `mob.scale_to_fit_width(max_w)`).

- [ ] **Step 1: Write the failing `_clamp_scale` tests** in `_selftest_sizecheck.py`:

```python
from pipeline import brand as B  # noqa: E402

def test_clamp_no_shrink_when_fits():
    assert B._clamp_scale(cur_w=3.0, max_w=5.0, cur_size=40.0, floor=26.0) == 1.0

def test_clamp_fits_when_above_floor():
    # need to shrink 5->4 (0.8x); resulting size 40*0.8=32 >= 26 -> use the fit scale
    assert abs(B._clamp_scale(cur_w=5.0, max_w=4.0, cur_size=40.0, floor=26.0) - 0.8) < 1e-9

def test_clamp_stops_at_floor():
    # fitting would need 0.5x -> size 40*0.5=20 < 26; clamp to floor scale 26/40=0.65
    assert abs(B._clamp_scale(cur_w=10.0, max_w=5.0, cur_size=40.0, floor=26.0) - 0.65) < 1e-9

def test_clamp_never_enlarges():
    assert B._clamp_scale(cur_w=2.0, max_w=9.0, cur_size=20.0, floor=26.0) == 1.0
```

Add these four calls to the `__main__` block.

- [ ] **Step 2: Run to confirm FAIL.** `.venv/Scripts/python.exe video/pipeline/_selftest_sizecheck.py` → `AttributeError: … '_clamp_scale'`.

- [ ] **Step 3: Implement the helpers** in `video/pipeline/brand.py`:

```python
def _clamp_scale(cur_w, max_w, cur_size, floor):
    """Scale factor to fit max_w without shrinking effective size below `floor`.
    Never enlarges (cap at 1.0). Wrap/overflow is preferred over sub-floor shrink."""
    if cur_w <= max_w or cur_w <= 0:
        return 1.0
    fit = max_w / cur_w
    floor_scale = floor / cur_size if cur_size > 0 else fit
    return min(1.0, max(fit, floor_scale))


def _clamp_shrink(mob, max_w):
    """In-place: shrink mob to fit max_w but not below theme.MIN_FONT_FLOOR. Drop-in
    replacement for mob.scale_to_fit_width(max_w) at single-line sites (SPEC §8)."""
    if max_w is None or max_w <= 0:
        return mob
    size = float(getattr(mob, "font_size", T.MIN_FONT_FLOOR))
    factor = _clamp_scale(mob.width, max_w, size, T.MIN_FONT_FLOOR)
    if factor < 1.0:
        mob.scale(factor)
    return mob
```

(Confirm `T` is the theme import alias already used in `brand.py`; if `font_size` is not directly on the mob at a given site, pass the known size in — read each call site. For Tex carrying TEXT_SCALE, `font_size` is already the rendered size, so comparing to a px-canonical floor needs the same `_norm_size` logic — if the site renders text, divide the mob's `font_size` by `T.TEXT_SCALE` before comparing, mirroring `sizecheck._norm_size`. Match each site's actual node type.)

- [ ] **Step 4: Replace the raw calls.** At `brand.py:398` (`prose()` pure-`$math$` branch), `brand.py:144` (`heading`), `brand.py:440` (`heading_rich`), `templates/derivation.py:180` (reason-rail), `templates/graph.py:143` (`_title`): replace `mob.scale_to_fit_width(max_w)` (or the local equivalent) with `brand._clamp_shrink(mob, max_w)` (templates import `brand`). Keep each site's surrounding logic intact.

- [ ] **Step 5: Run the self-test to confirm PASS.** `.venv/Scripts/python.exe video/pipeline/_selftest_sizecheck.py` → `OK sizecheck self-test`.

- [ ] **Step 6: Commit.**

```bash
git add video/pipeline/brand.py video/pipeline/templates/derivation.py video/pipeline/templates/graph.py video/pipeline/_selftest_sizecheck.py
git commit -m "feat(brand): clamp single-line scale_to_fit_width to MIN_FONT_FLOOR (SPEC §8 wrap-don't-shrink)"
```

(Render no-op verification on real decks is Task 5 Step 2 — do NOT claim no-op until that mock-render diff runs.)

---

### Task 4: Rubric extension (V4/A6 floor + mobile yardstick, A7 figure-prominence) + agent V-code refresh

**Files:**
- Modify: `video/content_scripts/_audit/VISUAL-FRAME-RUBRIC.md`
- Modify: `.claude/agents/visual-frame-audit.md` (D-P4-5 staleness fix only)

- [ ] **Step 1: Extend V4 (Layer 1, rubric line ~23).** Append the numeric floor as the concrete reference for "small to read": add that a Tex/text node whose **effective size falls below `MIN_FONT_FLOOR` (26px, the deterministic floor in `theme.py` / `sizecheck.py`)** is "too small to read"; if that makes a **load-bearing value** unreadable → **Blocking** (consistent with V4's existing "小到讀不到值 → Blocking"); if merely small-but-legible → defer to A6. Reference the deterministic check (`sizecheck.py` floor, warn-default) as the engineering counterpart that surfaces it pre-render.

- [ ] **Step 2: Extend A6 (Layer 2, rubric line ~40) with the mobile yardstick.** Add: secondary/subordinate text (reason-rail, annotations, captions) should stay readable when the frame is **downscaled to phone width** (sanity-check at ~360–414px-wide viewport — i.e. the 1920px frame at ~0.2× ); if a reason/annotation would be unreadable there, deduct A6 (severity by how far below). State this is a **judgment** yardstick the gate-1 agent applies by eye on the rendered frame, complementing the deterministic desktop floor.

- [ ] **Step 3: Add the A7 figure-prominence sub-criterion (Layer 2, rubric line ~41).** Append to A7: for scenes whose **core is geometric intuition** (hook / graph-centric content where "look at this shape/graph" IS the beat), the **figure should visually dominate** the content area; if text/whitespace crowds it so the figure is not the focus — rough guide: it occupies **less than ~half** the content area when the beat is fundamentally about the figure — deduct A7 (advisory magnitude, severity by how crowded). State explicitly: this is **measured by the agent's eye on the frame**, never a V-blocking, and never fires on text-centric scenes (definitions/derivations where the figure is a supporting aside).

- [ ] **Step 4: Self-consistency check (no run).** Re-read the three edits: (a) V4 keeps blocking only when a load-bearing value is unreadable (else A6); (b) A6 mobile yardstick is advisory; (c) A7 prominence is advisory and scoped to geometric-core scenes; (d) all three name the deterministic floor / "by eye" boundary correctly; (e) no new V/A code introduced (§8).

- [ ] **Step 5: Refresh the agent's stale V-code count (D-P4-5).** In `.claude/agents/visual-frame-audit.md`, change every `V1–V8` to `V1–V9` (lines ~5/15/25/27–28/32 per grounding). Do NOT otherwise edit the agent (it points to the rubric, doesn't restate it). Confirm the agent still reads `VISUAL-FRAME-RUBRIC.md` as authority.

- [ ] **Step 6: Commit.**

```bash
git add video/content_scripts/_audit/VISUAL-FRAME-RUBRIC.md .claude/agents/visual-frame-audit.md
git commit -m "docs(visual): V4/A6 min-size floor + mobile yardstick, A7 figure-prominence; agent V1-V8->V1-V9"
```

---

### Task 5: Calibration + visual verification + sign-off + whole-branch review

**Files:**
- Create (scratchpad, not committed): a deliberately-below-floor fixture run + an "open and read" HTML sign-off report.
- Possibly modify: `theme.MIN_FONT_FLOOR` (calibrated value) / the rubric thresholds (if calibration shows a false positive).

- [ ] **Step 1: Calibrate the floor CHECK (deterministic).** Create `video/storyboards/_fixtures/fontfloor.yml`: a minimal schema-valid deck with one content scene carrying a reason-rail / single-line that, at its declared width, is forced to shrink below 26px (e.g. a long `$…$` reason in a narrow `reason_max_w`). Run `.venv/Scripts/python.exe video/pipeline/sizecheck.py video/storyboards/_fixtures/fontfloor.yml` → confirm a `WARN` floor finding names that block, exit 0 (warn-default). Add `fontfloor_enforce: true` to its `meta` → confirm it becomes an `error`, exit 1. Record both runs.

- [ ] **Step 2: Verify the CLAMP is a no-op on existing decks (render invariance).** For each locked deck (ch01 §1.1 `ch01_inverse_functions.yml`, ch03 §3.1 `ch03_trig_derivatives.yml`, ch03 §3.2 `ch03_chain_rule.yml`): mock-render base-vs-HEAD final frames and diff. Recipe: `git stash` (or check out base), `python video/scratch_frames.py --storyboard <deck> --scene all --out video/output/_qa/floor_base`, then HEAD, render to `…/floor_head`, and compare PNGs (byte / pixel diff). **Expected: byte-identical** (no current line shrinks below the floor → clamp inert). If a deck DIFFERS: that scene was shrinking below the floor (a pre-existing too-small-text case) — capture the scene id, do NOT silently accept the changed render; surface it to the user (Step 4) as "fix now vs SP2". (Use `--backend mock`/`scratch_frames.py`; all offline. `--quality high` for 1080p per CLAUDE.md.)

- [ ] **Step 3: Run the deterministic floor + real decks; confirm no false positives.** Run `sizecheck.py` (no enforce) on the 3 real decks; confirm any floor warns are genuine too-small text (not legit `eyebrow`/`caption`). If a legit node trips it, lower `MIN_FONT_FLOOR` by the minimum needed and re-run (D-P4-1); record the calibrated value + reason.

- [ ] **Step 4: Visual gate-1 audit (judgment layer).** Mock-render a geometric-core deck (e.g. ch03 §3.1's squeeze/graph scenes) → `python video/pipeline/critic.py --storyboard <deck> --dry-run` to extract frames → dispatch the `visual-frame-audit` gate-1 agent on the frames. Confirm it now applies the new V4/A6 floor + mobile yardstick + A7 figure-prominence per the rubric, and that **A7/V4 visual blocking == 0** on the (good) real decks (§14 convergence). Capture its VERDICT.

- [ ] **Step 5: Produce the sign-off report.** A standalone HTML (CDN MathJax/KaTeX, double-click to open) summarizing: the `MIN_FONT_FLOOR` value + the warn-default/opt-in model + the clamp; the rubric's V4/A6 floor + mobile yardstick + A7 prominence; and the calibration result (floor warn fires on the fixture; clamp is byte-identical no-op on the 3 decks — or the surfaced exceptions; gate-1 A7/V4 blocking == 0). Per CLAUDE.md sign-off culture.

- [ ] **Step 6: User sign-off.** Present the report; get sign-off on the floor value + the rubric judgments + the no-op verification before considering Plan 4 done.

- [ ] **Step 7: Plan 4 whole-branch review.** Opus whole-branch review of the Plan 4 changeset (theme/sizecheck/brand/templates/rubric/agent + tests): is the floor check warn-default + correctly opt-in? Is the clamp arithmetic correct + the render no-op verified? Does the floor check correctly catch the inline-math carriers TOLERANCE skips, without false-positiving legit sizes? Are the rubric edits §8-faithful (no new V/A code; A7 advisory-only)? Address findings, re-audit. (Optionally, per the Plan-3 precedent and CLAUDE.md consent rule, offer the user a billed Codex independent pass.)

- [ ] **Step 8: Update progress anchors + finish.** Update `REBUILD_STATUS.md` + `HANDOFF-pedagogy-firstlearner-sp1.md`: Plan 4 ✅ (visual extension landed — floor constant + warn-default check + clamp + rubric V4/A6/A7; non-gating; no-op verified; calibrated, signed off); next = Plan 5. Then `superpowers:finishing-a-development-branch`.

---

## After Plan 4 lands

- **Plan 5 — Methodology/doc wiring (§12):** `CONTENT_METHODOLOGY.md` (P1/P2/P4 + scaffold authoring), `DESIGN.md` (scaffold 承載 + authoring checklist + the P5/P6 visual rules now enforced), `CONTENT-SIXLENS-RUBRIC.md` L1 scaffold exception (§5.5 exact wording), `REVIEW_GATES.md` (the pedagogy + fontfloor gates in sequence) + the remaining **V1–V8→V1–V9 doc-drift** cleanup (`REVIEW_GATES.md` line 65/66, `DESIGN.md` ~621/636 — the agent locus was already fixed in Plan 4 Task 4 / D-P4-5).
- **SP2 backfill** then applies Plans 1–4 to the 3 locked decks per spec §11 (dry-run → classify → user-approved migration list → scoped fix → re-gate/re-render/re-sign-off), flipping per-deck opt-in (`otf_enforce` / `pedagogy_enforce` / `fontfloor_enforce`) to gating. The fontfloor warns surfaced in Task 2/Task 5 on real decks are part of that SP2 surface.

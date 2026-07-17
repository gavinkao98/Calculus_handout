# Ch6 M1 chapter-closing sweep — audit (raw JSON gitignored; version-controlled record)

The M1 章層收尾 sweep = sympy 全例重算 + hypothesis ledger 覆核 + 章層 Codex review（明列 M1–M8）. 2026-07-10.

## 1. sympy math gate — 29/29 PASS

`scratchpad/sympy_ch6.py` recomputes every worked example and the power-sum import, asserting against the fragment value:
- §6.1: R₄=15/32, L₄=7/32; Rₙ closed form (n+1)(2n+1)/(6n²) and limit ⅓; Σi²=n(n+1)(2n+1)/6; distance table L=30/R=40.
- §6.2: ∫₀¹x²=⅓; ∫₀²(x−1)=0; ∫₁⁴√x=14/3 and 3≤14/3≤6.
- §6.3: d/dx∫₁ˣ√(1+t²)=√(1+x²); d/dx∫₀^{x³}cos t=3x²cos(x³); ∫₀¹x²=⅓; ∫₁⁴√x=14/3; ∫₀^π sin=2.
- §6.4: d/dx(x⁴/4−3x²)=x³−6x; d/dx(2eˣ−5ln x)=2eˣ−5/x; ∫₁²(1/x)=ln2; displacement ∫₀³(t²−4)=−3, segs −16/3 & 7/3, distance 23/3; d/dx ln(−x)=1/x for x<0.
- §6.5: d/dx[⅔(1+x²)^{3/2}]=2x√(1+x²); d/dx[(x³+1)⁶/18]=x²(x³+1)⁵; ∫₀²2x(1+x²)³=156; ∫₋₁¹(x⁴+x³)=2/5.

(One check — ∫₀³|t²−4| — sympy left the Abs-integral unevaluated; recomputed via the sign-split ∫₀²(4−t²)+∫₂³(t²−4)=23/3, exactly the fragment's method. Tooling limitation, not a content error.)

## 2. Hypothesis ledger review — clean

Per-section ⑤ already vetted each; consolidated chapter-wide the load-bearing hypotheses hold and are stated: continuity for integrability (Thm 6.1) & FTC (Thm 6.3/6.4); domains (ln|x| x≠0 two branches; arcsin |x|<1; sec² cos x≠0; negative-power rule x≠0); antiderivative on an **open** interval + FTC-2's F on an open interval containing [a,b], with F−g's continuity/zero-derivative made explicit for Cor 4.4; g′ continuous / f continuous on range for substitution (Thm 6.6/6.7); f continuous on [−a,a] for symmetry (Thm 6.8); speed ≥0 & continuous for total distance (§6.1/§6.4). Integrability (continuous⟹integrable) **fenced on credit** (uniform continuity), no §D.4 written (decision recorded in PLAN §6.2 note).

## 3. Chapter-level Codex review (M1–M8) — 1 blocking + 1 advisory, both fixed (158.7k tok)

Codex read all five fragments. Per-dimension verdicts:
- **M1** definitions (6.1–6.4) — clean. **M2** theorems (6.1–6.8) — clean. **M3** logic/quantifiers in proofs — clean. **M4** examples 6.1–6.16 + answers — clean. **M5** domains/edge cases/sample-point independence/interval scoping — clean. **M6** notation across sections (∫, xᵢ\*, Δx, dummy t vs x, [F]ₐᵇ bar, u, m_h/M_h) — clean. **M8** named imports resolve, hypotheses met — clean.
- **M7 cross-section** — **1 blocking**: §6.3 Example 6.8 cited "§6.6" for the bounding property, but there is no §6.6 — it is **Example 6.6** (in §6.2). A §-vs-Example typo. **Fixed** → "In Example 6.6". Grep confirmed no other §6.6–§6.9 dangling refs chapter-wide. Otherwise numbering ledger continuous (Def 6.1–6.4, Thm 6.1–6.8, Strategy 6.1–6.2, Ex 6.1–6.16, 0 figures) and cross-section statements agree.
- **Advisory**: §6.4 header comment's handoff said "Definition 6.5" (§6.5 mints no Definition) — **fixed** the metadata comment.

Imports verified to exist and be used within hypotheses: Prop A.6; Thm 1.2/1.3/2.1/3.3/4.9(a)/4.14; Cor 4.4; §5.3 differentials; Thm 6.2/6.4. Coverage confirmed: **FTC proved §6.3**; **∫1/x=ln|x|+C ships §6.4** with domain split; Chapter summary present, prose-led, correct recap, no new result.

**Total chapter-level ⑤ cost: 158.7k tok.** Post-fix: build ✔ · linebreak 0 · render katex 0 / math=612 / ready.

## M1 status: COMPLETE

Gate-1 side of M1 fully green. Remaining for chapter definification per PIPELINE: M2 (figures), M3 (prose S·A·V + difficulty learner-sim), M4 (Mode C gap-check), the three gate-2 cross-model passes (math/prose/figure, run after M4), M5 (dashboard + roadmap).

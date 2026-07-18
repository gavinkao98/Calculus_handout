# Ch7 M1 chapter-closing sweep — audit (raw JSON gitignored; version-controlled record)

The M1 章層收尾 sweep = sympy 全例重算 + hypothesis ledger 覆核 + 章層 Codex review（明列 M1–M8）. Started 2026-07-18.

## 1. sympy math gate — 48/48 PASS (2026-07-18)

`scratchpad/sympy_ch7.py` recomputes every worked example (all 22) plus the load-bearing auxiliary identities, asserting against the fragment values:

- **§7.1:** Ex 7.1 area \(e-\tfrac32\) + top-curve positivity (min of \(e^x-x\) on \([0,1]\) > 0); Ex 7.2 intersections \(\{0,1\}\) + area \(\tfrac13\); Ex 7.3 both pieces \(\sqrt2-1\), total \(2\sqrt2-2\); Ex 7.4 intersections \(y=\pm1\), area \(\tfrac83\), symmetry-doubling agreement.
- **§7.2:** Ex 7.5 sphere \(\tfrac43\pi r^3\) (direct + even-doubling); Ex 7.6 \(8\pi\); Ex 7.7 washer \(\tfrac{2\pi}{15}\) + ordering (min of \(x-x^2\ \ge 0\)); Ex 7.8 pyramid \(\tfrac13 b^2h\).
- **§7.3:** midpoint identity \(\pi(x_i^2-x_{i-1}^2)f = 2\pi\bar x_i f\,\Delta x\) (symbolic); Ex 7.9 \(\tfrac{16\pi}{5}\) + nonnegativity of \(x^2(2-x)\) on \([0,2]\); Ex 7.10 \(\tfrac{\pi}{6}\); Ex 7.11 shells \(\tfrac{\pi}{2}\) = washers \(\tfrac{\pi}{2}\) (agreement verified).
- **§7.4:** Ex 7.12 \(k=300\), \(W=4.5\) J, first-stretch comparison \(1.5\) J; Ex 7.13 \(400\) J; Ex 7.14 \(2450\pi\cdot\tfrac{63}{4}\) + numeric ≈ \(1.2\times10^5\) J.
- **§7.5:** Ex 7.15 \(f_{\text{ave}}=2\) + range claim (min 1 / max 5 on \([-1,2]\)); Ex 7.16 \(\tfrac43\); Ex 7.17 attainment set \(\{-1,1\}\).
- **§7.6:** Ex 7.18 \(L=\tfrac{13\sqrt{13}-8}{27}\) + chord sanity (\(L>\sqrt2\)); Ex 7.19 perfect-square identity + bracket positivity on \([1,2]\) + \(L=\tfrac{17}{12}\); Ex 7.20 square identity, \(s(x)=\tfrac{x^2-1}{8}+\ln x\), \(s(1)=0\), \(s'=\sqrt{1+f'^2}\), \(s(2)=\tfrac38+\ln2\).
- **§7.7:** frustum identity \(\pi r_2\ell_2-\pi r_1\ell_1=\pi(r_1+r_2)\ell\) (symbolic, with the similar-triangle slant heights); Ex 7.21 zone integrand \(=r\) (squared identity + numeric spots — sympy declines the direct radical merge without \(r^2-x^2>0\), a branch-caution tooling limitation, cf. ch06's Abs-integral note), zone area \(2\pi r(b-a)\), limiting value \(4\pi r^2\); Ex 7.22 \(\tfrac{\pi}{6}(5\sqrt5-1)\).

Also run: cross-reference lint (`scratchpad/xref_ch7.py`) — **51 prose references, 0 dangling** (imports Thm 4.9/4.12, Thm 6.1–6.5/6.8, Def 6.1/6.2, Ex 6.6 all resolve; all Ch7 self-refs resolve); **per-type counter continuity**: Thm 7.1–7.4, Def 7.1–7.6, Ex 7.1–7.22, Strategy 7.1–7.3 all continuous, no gaps.

## 2. Hypothesis ledger review — clean (2026-07-18, consolidated after per-section ⑤)

Per-section ⑤ vetted each; consolidated chapter-wide, the load-bearing hypotheses hold and are stated in the text:

- **Continuity for existence (Thm 6.1)** cited at every definition/limit point: \(f-g\) (Def 7.1 + the §7.1 horizontal-slice and crossing extensions after the B2 fix); \(A(x)\) (Def 7.2, incl. the washer paragraph after HYP-01); \(2\pi x f(x)\) (Thm 7.1); \(F\) (Def 7.3); the sampled means (§7.5); \(\sqrt{1+f'^2}\) (Thm 7.3); \(2\pi f\sqrt{1+f'^2}\) (Thm 7.4).
- **Order/sign hypotheses**: \(f\ge g\) with splitting at crossings (§7.1, finite-crossings scope stated); \(f\ge0\) for disks (§7.2), shells (Thm 7.1), surfaces (Def 7.6/Thm 7.4); \(0\le a<b\) one-side-of-axis discipline for shells and \(y\)-axis surfaces (with the B1-fixed non-overclaiming rationale); radius = distance to the rotation axis (three cautions, §§7.2/7.3/7.7).
- **\(a<b\) explicit** where reversal would break semantics: Def 7.4/Thm 7.2 (averages import no reversed-limits convention); Def 7.5/Thm 7.3 (length unsigned, degenerate \(L=0\)); Def 7.6/Thm 7.4.
- **Smoothness \(C^1([a,b])\)** minted in §7.6 with one-sided endpoint derivatives; consumed by Thm 7.3/7.4; its failure at the sphere's poles honestly flagged (Ex 7.21 zone + explicitly-labelled limiting preview, fenced to Ch8 improper integrals).
- **Ch4 existence imports within hypotheses**: EVT 4.9(a) for attained \(m, M\) (§7.5) and for \(K=\max\lvert f'\rvert\), \(B=\max\sqrt{1+f'^2}\) (§7.7); IVT 4.9(b) on \([\alpha,\beta]\subseteq[a,b]\) (§7.5); MVT 4.12 per strip with the closed/open bridge sentence (§7.6, reused §7.7).
- **Degenerate cases closed**: \(m=M\) constant case (§7.5); \(r_1=r_2\) cylinder band (§7.7 frustum lemma, separate unrolling check); pyramid apex \(0/0\) (§7.2 after HYP-02); polar blow-up (§7.7).
- **Sign disciplines**: \(\sqrt{q^2}=\lvert q\rvert\) opened with explicit positivity checks (§7.6 ×2); force = signed component along the motion, positive work assigned to the applied (against-gravity) force (§7.4 after B1, §7.7 summary after B3).
- **Modeling tiers stated in daylight, once each**: slab≈cylinder (Def 7.2); shell stack (Thm 7.1 preamble); polygon length (Def 7.5); frustum bands (Def 7.6); \(W=Fd\) constant-force physics input (Def 7.3). No silent modeling steps; no proof debt (the ③-rejected fence never entered the text — Thm 7.4 proved outright).

## 3. Chapter-level Codex review (M1–M8) — PASS: 0 blocking, 0 advisory (213.2k tok)

Codex (gpt-5.6-terra／xhigh) read all seven fragments end to end. Per-dimension verdicts, all explicitly CLEAN:

- **M1 definitions** — Def 7.1–7.6 carry the needed continuity / order / non-negativity / finite-limit / interval conditions, consistent with every later use.
- **M2 theorems** — Thm 7.1's shell-stack modeling tier consistent across preamble, statement, and the summary; Thm 7.2–7.4 statements complete, all three proofs sound step by step.
- **M3 logic/quantifiers** — Thm 7.2's m=M / m<M split exhaustive, α/β without smuggled ordering; Thm 7.4's ξᵢ and global K/B quantifiers consistent.
- **M4 examples** — Ex 7.1–7.22: boundary determinations, slicing models, derivations, physical readings, and answers all agree; no defective reasoning or overclaims around the numbers.
- **M5 domains/edge cases** — apex x=0, r₁=r₂ cylinder, polar C¹ failure, constant f, degenerate arc, √(q²)=|q|, signed force, radius-as-distance, one-side axis, sample-point independence — all handled.
- **M6 notation** — Δx / x_i* / x̄ᵢ / ξᵢ each in role; ρ, ds, f_ave, s(x) defined in scope; compatible with Ch5–6 conventions.
- **M7 cross-section consistency** — all references (into Ch1–6 and within Ch7) resolve to content that supports the use; summary faithfully recaps all seven sections; ledger continuous (Def 7.1–7.6, Thm 7.1–7.4, Strategy 7.1–7.3, Ex 7.1–7.22; cautions unnumbered).
- **M8 imports** — Thm 6.1/6.2/6.8/4.9/4.12/6.3/6.5 all exist and are used within hypotheses; §7.1 velocity-gap paragraph verified post-fix (continuous velocities; absolute-gap vs net difference separated).

**§7.7 four-fix regression riders (a)–(d): ALL CLEAN** (cross-axis rationale no longer contradicted by the y=x cone example; Def 7.6 named in the summary; work-agent wording fixed; "Three theorems" consistent). → `ch07_s7-7-codex5-audit.md` Round 2 = PASS; **§7.7 ⑤ CLOSED = 0 blocking.**

Auditor's summary: 「章級 M1–M8 sweep 與 §7.7 四項回歸均通過；目前樹為 0 blocking、0 advisory。」

## Codex 用量帳（本章 M1 全程，完成的 call）

③ 章層方向 221.1k｜⑤ §7.1 165.4k｜§7.2 105.3k｜§7.3(+7.2reg) 111.9k｜§7.4(+7.1reg) 177.0k｜§7.5 119.3k｜§7.6 128.6k｜§7.7(+7.4reg) 168.4k｜章層 sweep(+7.7reg) 213.2k ＝ **約 1.41M tokens／9 call**。另有 3 個 call（§7.3/§7.4/§7.5 首次）因電腦重開機中斷、用量未計入（已重跑）。

## M1 status: COMPLETE (2026-07-18)

Gate-1 side of M1 fully green: 7/7 sections ⑤ = 0 blocking (with regressions clean) · sympy 48/48 · xref 51/51 resolve + counters continuous · build ✔ · linebreak 0 · quote lint clean ×7 · render math=813 / katex-errors 0 / fragments 7. Remaining for chapter definification per PIPELINE: M2 (figures), M3 (prose S·A·V + difficulty learner-sim), M4 (Mode C gap-check), the three gate-2 cross-model passes (run after M4), M5 (dashboard + roadmap).

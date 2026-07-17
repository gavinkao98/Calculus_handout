# §6.2 Codex ⑤ audit — transcript (raw JSON gitignored; version-controlled record)

Section: **§6.2 The Definite Integral** (Ch6, canon variant). Gate ⑤, gpt-5.6-terra/xhigh, read-only. 2026-07-10.

**Outcome: 0 blocking after one fix round + two scoped regressions.** All arithmetic (Ex 6.4 ∫₀¹x²=⅓; Ex 6.5 ∫₀²(x−1)=0 net signed area; Ex 6.6 3≤∫₁⁴√x≤6, exact 14/3≈4.67) verified correct first pass.

## Round 1 — 4 blocking + 2 advisory (127.5k tok)

| id | cat | issue | verdict | fix |
|---|---|---|---|---|
| M1 | **math_correctness** | additivity "proof" said an arbitrary interior c is a partition point of an *equal-width* Riemann sum — false; the split doesn't follow from Def 6.2's regular partition | valid, real gap | broadened Theorem 6.1 to "every way of slicing into narrowing strips + every sample point"; recast additivity as geometric decomposition + honest sum-proof note (c-as-a-node slicing, Theorem 6.1 slicing-independence) |
| H1 | hypothesis_hygiene | Theorem 6.2 "additivity for c in any position" needs f integrable on the spanning interval; m/M bound false for reversed limits; **+ notation clash** (c = both constant and split point) | valid (+ I caught the clash) | stated for a≤b, c∈[a,b]; renamed constant c→**k**; outside-c extension requires integrability/continuity on the spanning interval |
| H2 | hypothesis_hygiene | Ex 6.6 applied properties to √x without flagging integrability | valid | added "√x continuous on [1,4] ⟹ integrable (Theorem 6.1)" before the bound |
| D1 | direction_conformance | closing paragraph leaked FTC mechanics ("evaluation → search for a single antiderivative") | valid (same class as §6.1 B1) | softened to a one-line payoff fence (connects integral to derivative, makes integrals painless) — no mechanism |
| A1 | advisory/pedagogy | constant + scalar-linearity only "immediate" | adopted | added the one-line computations ΣkΔx=k(b−a), Σkf Δx=kΣf Δx |
| A2 | advisory/math | open decision: on-credit fence vs write App D §D.4 | **adopted → decision** | **keep on-credit fence, no §D.4** (Codex: add §D.4 only when the Proof Track has a concrete later use for the full uniform-continuity proof) |

## Regression 1 — H1/H2/D1 resolved; M1 residual (31.5k tok)

- **M1 residual:** Theorem 6.2 was stated for any *integrable* f, but the additivity sum-proof invokes Theorem 6.1's slicing-independence, which Theorem 6.1 supplies only for *continuous* f. Re-fix: **restrict Theorem 6.2 to continuous f** (the chapter's actual scope — every integrand here is continuous; makes all four parts fully rigorous via Theorem 6.1; avoids the fenced general Riemann-integrability machinery). Changed lead-in prose + theorem statement "integrable" → "continuous"; additivity note now derives sub-interval continuity.

## Regression 2 — 0 blocking (48.2k tok)

Codex confirmed: (a) additivity sum-proof fully entitled under continuous hypothesis; (b) constant/linearity/comparison intact; (c) no residual "integrable"-where-"continuous"-needed; Ch6 never applies the properties to a non-continuous function.

**Total ⑤ cost §6.2: ≈207k tok (subscription).** Gate-1: build ✔ · linebreak 0 · render katex 0 / math=235 / ready.

**Resolved open decision (PLAN-ch06):** Theorem 6.1 (continuous ⟹ integrable) fenced **on-credit, no cross-ref**; App D §D.4 (uniform-continuity proof) **not written** — defer until a later chapter needs the full proof.

**Lesson:** stating theorems at the widest hypothesis ("integrable") tempts proofs that outrun what's been established. Match the theorem's hypothesis to what the chapter can actually prove (here: continuous), especially for a 深理論核心 chapter that promises no fake proofs.

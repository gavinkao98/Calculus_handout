# §6.1 Codex ⑤ audit — transcript (raw JSON gitignored; this is the version-controlled record)

Section: **§6.1 Areas and Distances** (Ch6 Integrals, canon variant). Gate ⑤ (Codex adversarial, direction-conformance + math + hypothesis hygiene), model gpt-5.6-terra/xhigh via codex-cli 0.144.1, read-only (standing consent). 2026-07-10.

**Outcome: 0 blocking after one fix round + two scoped regressions.** All specified arithmetic (Ex 6.1 R₄=15/32, L₄=7/32; Ex 6.2 limit = 1/3; Ex 6.3 L=30/R=40) and the Prop A.6 cross-reference (Σi²=n(n+1)(2n+1)/6) verified correct on the first pass.

## Round 1 — 4 blocking (112.4k tok)

| id | cat | issue | verdict | fix |
|---|---|---|---|---|
| B1 | direction_conformance | chapter opener had the prohibited FTC antiderivative-shortcut teaser ("read off from an antiderivative in a single line") | valid (partial — opener *may* preview FTC per SPEC §4, but not the operational shortcut) | reworded opener to preview FTC conceptually ("two sides of a single coin… link between areas and slopes"), dropped the one-line-shortcut mechanism |
| B2 | **math_correctness** | Caution claimed left- vs right-endpoint sums "really can disagree" for discontinuous f — **false**: for a regular partition Rₙ−Lₙ=((b−a)/n)(f(b)−f(a))→0 telescopes for any finite-endpoint f; disagreement is across *sample-point choices* (Dirichlet-type), not L-vs-R | valid, real error | rewrote caution: disagreement is in the sample-point choice; added parenthetical that the L/R gap is (f(b)−f(a))Δx and closes regardless — consistent with Def 6.1's "any sample point" |
| B3 | hypothesis_hygiene | distance setup/summary stated no non-negativity/continuity for velocity; "distance = area under v–t" needs v≥0 | valid | switched to **speed** (≥0), stated continuity |
| B4 | hypothesis_hygiene | Ex 6.3 asserted strict bracket from 6 sampled readings; sampled-non-decreasing ≠ non-decreasing between readings; strict `<` unearned | valid | stated modelling assumption (continuous, non-decreasing); inclusive bracket |

## Regression 1 — B1/B2 resolved; B3/B4 residual (74.0k tok)

- **B1 ✅**, **B2 ✅** (sample-point mechanism + telescoping gap correct, consistent with Def 6.1).
- **B3 residual:** my "distance covered and net change in position agree" overreached — motion along −axis makes distance = |displacement|, not = displacement. Re-fix: dropped the net-change clause entirely; speed (≥0, any heading, continuous) integrates to total distance (path length) with no orientation assumption.
- **B4 residual:** "left undercounts, right overcounts *every* strip" is strict, but the 10→10 final strip is *exact* under continuous+non-decreasing. Re-fix: weakened to "no lower than / no higher than" (inclusive bounds; the `≤` bracket already claims this).

## Regression 2 — 0 blocking (29.9k tok)

Both re-fixes clean: B3 total-distance-from-continuous-speed = area under speed–time graph, no signed-displacement error; B4 inclusive endpoint bounds valid on every strip incl. the constant one, 30 ≤ distance ≤ 40 holds.

**Total ⑤ cost §6.1: ≈216k tok (subscription quota).** Gate-1 automated: build ✔ · linebreak 0 · render katex 0 / math=95 / ready.

**Lesson (for later sections + the linalg repo):** hypothesis-hygiene fixes on physical-quantity examples (velocity/speed, distance/displacement) are error-prone under time pressure — state the *minimal* honest hypothesis (speed ≥0 ⇒ ∫speed = path length; no orientation needed) rather than bolting on displacement identities that reintroduce signed-area concerns deferred to §6.4.

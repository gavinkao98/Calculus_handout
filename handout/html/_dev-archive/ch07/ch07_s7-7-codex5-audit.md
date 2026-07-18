# §7.7 Surface Area (+ Ch summary) — Codex ⑤ audit record (raw JSON gitignored)

2026-07-18. gpt-5.6-terra／xhigh, read-only, output-schema. This call carried a secondary regression rider on §7.4's round-1 fix (R-74).

## Round 1 — FAIL: 4 blocking, all fixed

| id | sev | category | finding | fix applied |
|---|---|---|---|---|
| 7.7-B1 | blocking | math-correctness | "a curve straddling the axis would sweep the same surface twice" — over-general: \(y=x\) on \([-1,1]\) about the \(y\)-axis generates two distinct cones meeting only at the vertex. Cross-axis curves MAY overlap/double-generate, not necessarily. | reason reworded: signed \(x\) fails, and the two halves CAN overlap or re-cover parts of one surface, so the general case calls for splitting at the axis and tracking each piece; the \(0\le a<b\) theorem scope unchanged |
| 7.7-B2 | blocking | direction-conformance | Chapter summary names Def 7.1–7.5 in order but skipped **Definition 7.6** (only Thm 7.4 named for §7.7) | summary's §7.7 clause now reads "…to define surface area (Definition 7.6) and prove the Surface Area Formula (Theorem 7.4)…" |
| 7.7-B3 | blocking | math-correctness | summary's "work against a varying force is \(W=\int F\,dx\)" re-introduced the force-agent/sign ambiguity that 7.4-B1 had just eliminated (Def 7.3's \(F\) = signed component of the force DOING the work) | "the work done by a varying force — read through its signed component \(F(x)\) along the motion — is \(W=\int_a^b F(x)\,dx\)" |
| 7.7-B4 | blocking | canon-coverage | "Two theorems … proved with the existence machinery of Chapter 4" then lists THREE (Thm 7.2 + the two geometric formulas) — self-contradictory and conflicts with the ledger | "Three theorems in the chapter were proved with the machinery of Chapter 4 — … and the two geometric formulas …" |

## Round 1 — checked clean (auditor-verified)

- **Frustum lemma correct**: sector → \(\pi r\ell\); similar triangles give \(\ell_2-\ell_1=\ell\); subtraction → \(\pi(r_1+r_2)\ell\); \(r_1=r_2\) cylinder verified separately by unrolling; \(2\pi\bar r\ell\) compression.
- **Definition 7.6 conformant** (regular partitions, a<b, continuous \(f\ge0\), finite limit).
- **Theorem 7.4's proof sound step by step**: §7.6 chord-MVT reuse legitimate (ξᵢ in the open strip); EVT legitimately yields K, B; sub-interval MVT + averaging estimate correct; per-band and total error factors correct; Thm 6.1 + Def 6.2 finish complete.
- \(y\)-axis version genuinely provable by the same argument (radius function \(x\) is C¹, derivative bound 1) — only B1's over-generality needed fixing.
- Ex 7.21: smoothness, positive root, integrand collapse, \(2\pi r(b-a)\), full-sphere limiting preview all correct; "hat-box theorem" naming conventional (auditor cross-checked MathWorld).
- Ex 7.22: one-side radius discipline, \(ds\), u-sub, \(\pi(5\sqrt5-1)/6\approx5.3304\); closing three-sections line accurate.
- Chapter summary (apart from B2–B4): placement, unnumbered subsec-head, continuous prose, three SPEC-§4 moves, EIGHT core formulas embedded, Ch8/10/13/15/16 forward fence; Thm 7.1's wording stays within §7.3's published modeling tier; Ex 7.21 polar-flag back-reference contextually clear.
- Reverse check clean: exactly 2 examples; no Pappus / Schwarz lantern / general-parametric surfaces beyond forward refs; counters close at Def 7.1–7.6, Thm 7.1–7.4, Strategy 7.1–7.3, Ex 7.1–7.22.

## Regression rider R-74 (§7.4's force-agent fix) — CLEAN

Transition attributes the positive work to the winch's/pump's upward applied force with gravity's work negative; Ex 7.13/7.14 and the Caution no longer cast weight as the positive-work agent; stems, arithmetic, units, strategy, example count all intact. → **§7.4 ⑤ CLOSED = 0 blocking.**

## Round 2 (regression on B1–B4's fixes) — PASS, all clean (2026-07-18, riders on the chapter-level review)

(a) cross-axis rationale: "CAN overlap or re-cover" + splitting-and-tracking — no longer contradicted by the \(y=x\) two-cones example; \(0\le a<b\) scope retained ✓. (b) summary names Definition 7.6 before Theorem 7.4 ✓. (c) work read through the signed component \(F(x)\) — agent ambiguity gone ✓. (d) "Three theorems" consistent with the list and the ledger ✓. See `ch07_chapter-sweep-audit.md` §3.

**Status: §7.7 ⑤ CLOSED = 0 blocking (round 1: 4 blocking fixed; round 2 regression clean). Build ✔ · linebreak 0 · quote lint clean · xref clean.**

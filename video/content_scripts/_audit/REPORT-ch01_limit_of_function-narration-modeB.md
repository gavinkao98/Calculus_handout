# Mode B narration audit — §1.3 The Limit of a Function (deck `ch01_limit_of_function`)

**Route:** MiMo dual-version (spoken). **CONTENT_APPROVED = no** → D7 (math-content) required.
**Reviewer:** codex `gpt-5.5`, read-only. Raw transcripts: `REPORT-...-modeB.raw.txt` (round 1), `REPORT-...-modeB-v2.raw.txt` (regression).

## Round 1 — VERDICT: 1 blocking, 3 advisory

| # | Sev | D# | unit | Finding | Verdict |
|---|---|---|---|---|---|
| 1 | **Blocking** | D2/D3 | estimate_from_a_table | spoken added `f of x equals` (not in source `$\lim_{x\to1}\frac{x-1}{x^2-1}$`) + weak fraction grouping | **Adopted** — rewrote to "the limit, as x approaches one, of the quantity x minus one, all over the quantity x squared minus one" (spoken only) |
| 2 | Advisory | D3 | ratio_of_changes | `s(t+h)` → "s of t plus h" hearable as `s(t)+h`; denominator grouping light | **Adopted (light)** — "s of **the quantity** t plus h…", "…all over **the quantity** y minus x" (existing `the quantity` convention, not codex's verbose numerator/denominator form) |
| 3 | Advisory | D3 | when_algebra_is_hard | radical-over-fraction scope hearable wrong | **Partially adopted** — added "the quantity" to scope the radical; see round 2 |
| 4 | Advisory | D7 | estimate_from_a_table | narration omitted `0.4762` and listed right side `0.4998, 0.4975` (contradicts "closing in") | **Adopted in ALL versions** (`.md` / `.html` / storyboard `say` / `.spoken.yml`) — "and 0.4762, 0.4975, 0.4998 closing in from the right" (faithful to handout's full 6-value table, genuinely closing in) |

Note: finding 4 is a **canonical** narration precision/faithfulness fix (was present in the user-pending narration); the earlier six-lens math-accuracy lens had blessed that subset — Mode B's adversarial D7 caught the direction/omission. Findings 1–3 were spoken-transformation only.

## Round 2 (regression, after fixes) — VERDICT: 0 blocking, 1 advisory

- Blocking + findings 2, 4 **resolved**. **D7 fully clean** (both tables, both graph examples re-derived correct). D1/D2/D4 clean. The documented `the_limit_defined` collapses ruled **acceptable spoken adaptation**.
- **1 advisory remains (finding 3, escalated to a convention choice):** `when_algebra_is_hard` — codex prefers the explicit "the fraction whose numerator is … and whose denominator is …" form for the nested radical-over-fraction `(√(t²+9)−3)/t²`. Current spoken uses the project's existing light convention ("the quantity …, … all over …"), which is parseable. **This is an editorial taste call (both work) → escalated to user per CLAUDE.md ("有爭議往上拋"); recommendation: keep the light convention for consistency, switch to the explicit form for this one expression only if maximal clarity is preferred.**

**Outcome:** spoken narration is faithful, math 0 errors, no blocking issues. One user taste decision outstanding (above). Narration content itself still pending user approval (CONTENT_APPROVED was no).

# §6.4 Codex ⑤ audit — transcript (raw JSON gitignored; version-controlled record)

Section: **§6.4 Indefinite Integrals and the Net Change Theorem** (Ch6, canon variant). Gate ⑤, gpt-5.6-terra/xhigh, read-only. 2026-07-10.

**Outcome: 0 blocking after one fix round + one regression.** All table formulas and every computation verified correct first pass (Ex 6.10 (a) x⁴/4−3x²+C, (b) 2eˣ−5ln|x|+C; Ex 6.11 ∫₁²1/x=ln2; Ex 6.12 displacement −3 m, distance 23/3 m); Theorem 4.14 confirmed the correct Ch4 reference for (ln x)′=1/x; §6.5 only forward-fenced (not taught).

## Round 1 — 2 blocking (154.1k tok)

| id | cat | issue | fix |
|---|---|---|---|
| H-6.4-01 | hypothesis_hygiene | the antiderivative table gave no domain qualifications for non-global identities (sec² needs cos x≠0; arcsin needs −1<x<1; negative-power rule excludes 0) | added a table-level domain bridge naming the sec², arcsin, and restricted-power-rule intervals |
| M-6.4-01 | **math_correctness** | Ex 6.12 closing "the backward leg is undone and then some" is **wrong** — forward leg 7/3 m < backward 16/3 m, so it undoes only *part* (ends 3 m behind, matching displacement −3); also v(2)=0 so sign intervals are [0,2)/(2,3] | corrected sign intervals ([0,2) neg, v(2)=0, (2,3] pos); rewrote closing: forward 7/3 m undoes only part of backward 16/3 m, leaving it 3 m behind |

## Regression — 0 blocking (19.7k tok)

Codex confirmed: domain bridge correct and not overclaiming; sign intervals correctly isolate v(2)=0; 16/3 back + 7/3 forward = net −3 m. No residual/new defect.

**Total ⑤ cost §6.4: ≈174k tok (subscription).** Gate-1: build ✔ · linebreak 0 (the 2-column antiderivative table did not trigger auto-break) · render katex 0 / math=487 / ready.

**Export confirmed shipped:** ∫(1/x)dx = ln|x|+C with the x<0-branch justification and domain caveat (x≠0, two intervals) — forward export to Ch8/Ch9 per the roadmap seam ledger.

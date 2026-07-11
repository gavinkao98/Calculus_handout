# §6.3 Codex ⑤ audit — transcript (raw JSON gitignored; version-controlled record)

Section: **§6.3 The Fundamental Theorem of Calculus** — the chapter CRUX (深理論核心, both parts proved on the spot). Gate ⑤, gpt-5.6-terra/xhigh, read-only. 2026-07-10.

**Outcome: 0 blocking after ONE fix round + one regression.** The mathematics was correct first pass — Codex verified the h<0 bracket in the FTC-1 proof, both examples' arithmetic (Ex 6.7 √(1+x²) & 3x²cos(x³); Ex 6.8 ⅓ & 14/3; Ex 6.9 = 2), the e^{−t²} no-elementary-antiderivative caution, and that **all four imports exist and are correctly numbered** (EVT Thm 4.9(a), Cor 4.4 constant-difference, chain rule Thm 3.3, Squeeze Thm 1.3, plus additivity/comparison Thm 6.2). The two blockings were honest rigor gaps, not errors.

## Round 1 — 2 blocking (both hypothesis_hygiene) + 1 advisory (159.9k tok)

| id | issue | fix |
|---|---|---|
| B1 | antiderivative scoped to a closed interval; FTC-2 applied Cor 4.4 to F−g without verifying its hypotheses (F−g continuous on [a,b], zero derivative on (a,b)). Cor 4.4 is "continuous on [a,b] + zero derivative on (a,b) ⟹ constant", not directly "two antiderivatives differ by a constant" | Def 6.3 → "on an **open** interval"; FTC-1 conclusion → "antiderivative on **(a,b)**"; FTC-2 hypothesis → "F antiderivative on an **open interval containing [a,b]**"; FTC-2 proof now explicitly records F−g continuous on [a,b] + (F−g)'=0 on (a,b) **before** citing Cor 4.4 |
| B2 | FTC-1 hand-waved g's continuity on [a,b] ("one-sided versions give continuity") | replaced with a Lipschitz bound: f bounded by M (EVT Thm 4.9(a)) ⟹ \|g(x+h)−g(x)\| = \|∫ₓ^{x+h}f\| ≤ M\|h\| → 0, giving continuity at every point of [a,b] incl. endpoints |
| A1 (adv) | "left it **dear** to compute" — wrong idiom | → "laborious" |

## Regression — 0 blocking (111.9k tok)

Codex confirmed: B1 — Cor 4.4 now supplied its exact hypotheses, open-interval scopes consistent; B2 — the Lipschitz bound establishes continuity on all of [a,b] incl. endpoints; Theorem 2.1 (differentiable ⟹ continuous, cited for F) genuinely states that; "laborious" reads well. No new defect.

**Total ⑤ cost §6.3: ≈272k tok (subscription).** Gate-1: build ✔ · linebreak 0 · render katex 0 / math=396 / ready. `env-proof`/`qed-proof` confirmed styled (result accent + QED, in paginator SPLIT_ENVS).

**Note:** the crux section needed only ONE fix round — the FTC-1 (EVT + comparison + squeeze) and FTC-2 (FTC-1 + Cor 4.4) proofs were mathematically sound as drafted; the fixes were interval-scoping rigor (open vs closed) and making the Cor 4.4 / continuity steps explicit, exactly the discipline a 深理論核心 "no fake proofs" chapter demands.

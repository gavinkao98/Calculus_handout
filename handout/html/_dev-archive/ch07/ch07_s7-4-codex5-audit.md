# §7.4 Work — Codex ⑤ audit record (raw JSON gitignored)

2026-07-18. gpt-5.6-terra／xhigh, read-only, output-schema. (First attempt lost to a mid-run machine reboot; relaunched with the identical prompt.) This call carried a secondary regression rider on §7.1's round-1 fixes.

## Round 1 — FAIL: 1 blocking, fixed

| id | sev | category | finding | fix applied |
|---|---|---|---|---|
| 7.4-B1 | blocking | math-correctness | Definition 7.3 frames \(F\) as the SIGNED force component along the motion — but the lifting/pumping prose assigned the positive work to each slice's <em>weight</em> while the slice rises. Weight points down; its work along an upward motion is negative. The positive integrals actually price the upward APPLIED force (magnitude = the slice's weight; steady lifting), i.e. work done <em>against</em> gravity. Numbers correct; force-agent and sign internally inconsistent with the definition. | "Lifting and pumping" transition rewritten: the model computes positive work done against gravity via the upward applied force of weight-equal magnitude (with the one-line note that gravity's own work is the opposite, negative, quantity); Ex 7.13 and Ex 7.14 solutions now attribute the priced work to the winch's / pump's applied force explicitly; Caution reworded ("the force required on each slice … matching its weight"). Example stems were already agent-correct ("work the winch does", "work required to pump") — only the solution/transition prose misassigned the agent. |

## Round 1 — checked clean (auditor-verified)

Definition 7.3 (continuity, signed-component framing, Thm 6.1 existence, W=Fd modeling-input status, §6.4 net-change echo). Hooke paragraph (empirical status, source tag, applied \(kx\) vs restoring \(-kx\), work-against-the-spring). Ex 7.12 recomputed (k=300, 4.5 J, 1.5 J comparison). Ex 7.13 slice choice, N/m weight-density note, 400 J, top-vs-bottom reading (apart from B1's agent wording). Ex 7.14 coordinate convention, Ex 7.8 cross-ref, r(y)=y/2, slab factors, bounds, lift distance, 3-vs-4 note; exact value 38 587.5π ≈ 1.21×10⁵ J. Units SI-primary, J=N·m in place, exactly one ft-lb parenthetical. Exactly 3 examples; prohibited topics absent; numbering matches ledger. Caution + Strategy 7.3 substance correct.

## Regression rider on §7.1 (R-a/R-b) — ALL CLEAN

- R-a: velocity-gap repair satisfies Thm 6.5's hypotheses (positions + continuous velocities) and correctly separates absolute-gap area from the net integral after crossings.
- R-b: horizontal-slicing repair states sufficient continuity, ties the limit argument to it, no second formal definition.

→ **§7.1 ⑤ CLOSED = 0 blocking** (round 1: 2 blocking fixed; regression clean). `ch07_s7-1-codex5-audit.md` updated.

## Round 2 (regression on 7.4-B1's fix) — PASS, clean (2026-07-18, rider R-74 on the §7.7 ⑤ call)

Transition attributes the positive work to the winch's/pump's upward applied force, gravity's own work negative; Ex 7.13/7.14 and the Caution no longer cast weight as the positive-work agent; stems, arithmetic, units, strategy, and the three-example count all intact. See `ch07_s7-7-codex5-audit.md`.

（連帶：§7.7 章末總結第一版曾以「work against a varying force is \(W=\int F\,dx\)」重新引入同型歧義——§7.7 稽核以 7.7-B3 抓到並已修，見該檔。）

**Status: §7.4 ⑤ CLOSED = 0 blocking (round 1: 1 blocking fixed; round 2 regression clean). Build ✔ · linebreak 0 · quote lint clean.**

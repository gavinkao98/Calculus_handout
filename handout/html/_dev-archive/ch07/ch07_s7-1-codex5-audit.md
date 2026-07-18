# §7.1 Areas Between Curves (+ Ch7 opener) — Codex ⑤ audit record (raw JSON gitignored)

2026-07-18. gpt-5.6-terra／xhigh, read-only, output-schema.

## Round 1 — FAIL: 2 blocking, both fixed

| id | sev | category | finding | fix applied |
|---|---|---|---|---|
| B1 | blocking | hypothesis-hygiene | velocity-gap application cited Thm 6.5 with only \(v_A \ge v_B\) assumed — no continuity (Net Change needs a continuous rate), and the closing "whenever two rates…" sentence over-generalized to possibly-crossing rate curves (area between graphs = absolute gap, not net difference) | rewritten with position functions: \(s_A(0)=s_B(0)\), continuous \(v_A=s_A'\), \(v_B=s_B'\); Thm 6.5 applied to \(s_A-s_B\); closing sentence now conditions on "so long as one stays on top" and names the crossing case explicitly (\(\int\lvert v_A-v_B\rvert\) vs the plain integral — §6.4 echo) |
| B2 | blocking | hypothesis-hygiene | horizontal-slicing general formula \(A=\int_c^d[f(y)-g(y)]dy\) stated without continuity of \(f, g\) — "the same limit argument" had no hypothesis to rest on | prose now reads "with \(f\) and \(g\) continuous on \([c,d]\) and \(f(y)\ge g(y)\) there … the same limit argument, resting on the same continuity" (no second formal definition — brief's constraint respected) |

## Round 1 — checked clean (auditor-verified)

Arithmetic: all four answers independently recomputed (\(e-\tfrac32\), \(\tfrac13\), \(2\sqrt2-2\), \(\tfrac83\)). Cross-references: Def 6.1/6.2, Thm 6.1/6.4/6.5/6.8 all resolve and are used within hypotheses. Ex 7.1 top-curve argument and Ex 7.3 crossing-finding argument judged airtight; Ex 7.4 horizontal setup + evenness appeal correct. Chapter opener: lead + exactly FIVE outcome bullets matching PLAN's ③-final list. Canon coverage complete (strip sum, Def 7.1, given-interval, enclosed, crossing/absolute-gap, horizontal, strategy, application). Omit-list respected (no centroids, parametric areas, improper regions, numerical methods, second sideways definition, integrability re-proof, FTC recap). Numbering consistent with ledger.

## Round 2 (regression on B1/B2) — PASS, all clean (2026-07-18, rider on the §7.4 ⑤ call)

R-a: velocity-gap repair satisfies Thm 6.5's hypotheses (positions \(s_A(0)=s_B(0)\) + continuous velocities) and correctly separates the absolute-gap area from the net integral when rate curves cross ✓. R-b: horizontal-slicing repair states sufficient continuity, ties the limit argument to it, and introduces no second formal definition ✓. See `ch07_s7-4-codex5-audit.md`.

**Status: §7.1 ⑤ CLOSED = 0 blocking (round 1: 2 blocking fixed; round 2 regression clean). Build ✔ · linebreak 0 · quote lint clean.**

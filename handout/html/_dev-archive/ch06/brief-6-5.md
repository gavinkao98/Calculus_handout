# Direction brief — §6.5 The Substitution Rule (+ Chapter 6 summary)

Canon variant (Stewart ET 9e §5.5). ⑤ contract. 2026-07-10 per PLAN-ch06. **Last section — also carries the mandatory Chapter summary (SPEC §4).**

- **Canon inventory (§5.5):** the Substitution Rule (indefinite) \(\int f(g(x))g'(x)\,dx=\int f(u)\,du\) as the chain rule reversed, with \(du=g'(x)\,dx\); the definite version by change of limits \(\int_a^b f(g(x))g'(x)\,dx=\int_{g(a)}^{g(b)} f(u)\,du\); integrals of symmetric (even/odd) functions.
- **Thinness:** canon is *enough* on the three rules. *Thin/none*: a Strategy box; the "change limits **or** back-substitute, never mix" caution; graded examples (basic sub → constant adjustment → definite by change of limits → symmetry).
- **Scope & depth:** **PROVE** all three (they are short, canon, and illuminating — SPEC §5): Substitution via the chain rule (Thm 3.3) reversed; definite substitution via FTC-2 (Thm 6.4) + chain rule; symmetry by the substitution \(u=-x\). Tie \(du=g'(x)\,dx\) to §5.3 differentials. Do **not** do integration by parts / trig integrals / partial fractions / trig substitution — **all Ch8** (one-line fence). This is **u-substitution only**.
- **Load-bearing intuition (one):** substitution is the chain rule read backwards — spot an inner function \(g\) whose derivative \(g'\) is also present (up to a constant), rename \(u=g(x)\), and the tangle collapses to a table integral in \(u\).
- **Worked examples (basic → adjust → definite → symmetry):**
  - **Ex 6.13** — \(\int 2x\sqrt{1+x^2}\,dx\): \(u=1+x^2,\ du=2x\,dx\) ⟹ \(\tfrac23(1+x^2)^{3/2}+C\).
  - **Ex 6.14** — constant adjustment: \(\int x^2(x^3+1)^5\,dx\): \(u=x^3+1,\ x^2\,dx=\tfrac13du\) ⟹ \(\tfrac{(x^3+1)^6}{18}+C\).
  - **Ex 6.15** — definite by change of limits: \(\int_0^2 2x(1+x^2)^3\,dx=\int_1^5 u^3\,du=156\).
  - **Ex 6.16** — symmetry: \(\int_{-1}^{1}(x^4+x^3)\,dx = 2\int_0^1 x^4\,dx + 0 = \tfrac25\) (even part doubles, odd part vanishes).
- **Strategy 6.2** — substitution: choose \(u=g(x)\) (inner function with \(g'\) present up to a constant); rewrite the *whole* integral in \(u\) incl. \(dx\); integrate; back-substitute (indefinite) **or** change the limits to \(g(a),g(b)\) (definite) — never keep \(x\)-limits on a \(u\)-integrand.
- **history / application:** none forced; skip (the mechanics carry the section).
- **figure_opportunities** (mark now, draw at M2): possibly a change-of-limits picture (area preserved under \(x\mapsto u\)); low priority — mark for M2 but likely a DEFER candidate.
- **Emphasis / takeaway:** concept pivot = substitution = reverse chain rule; portable skill = execute u-substitution for indefinite and definite integrals, and use even/odd symmetry to shortcut.
- **Deliberately omit (auditor's reverse check):** integration by parts, trig integrals, trig substitution, partial fractions, numerical/improper integration — **all Ch8**; average value (Ch7). No "general technique menu" beyond substitution.
- **CHAPTER SUMMARY (SPEC §4):** unnumbered `<h3 class="subsec-head">Chapter summary</h3>` at the end, continuous prose (not a list): name the arc §6.1 (area/distance as Riemann-sum limits) → §6.2 (the definite integral, integrability Thm 6.1, properties, net signed area) → §6.3 (FTC, both parts **proved** — differentiation and integration are inverse) → §6.4 (indefinite integrals, the table, net change, ∫1/x=ln|x|) → §6.5 (substitution). Recap key results with §-refs (no re-proof); embed 3–8 key formulas (the definite integral limit, both FTC parts, ∫1/x=ln|x|, the substitution rule); close the fence forward (FTC → Ch7–8,11,13,15–16; substitution → Ch8 techniques).
- **Length band:** ~230–280 line fragment (3 proved theorems + Strategy + 4 examples + Chapter summary).
- **Env minted (provisional):** Theorem 6.6 (Substitution Rule), Theorem 6.7 (Substitution in definite integrals), Theorem 6.8 (Integrals of symmetric functions); Strategy 6.2; Examples 6.13–6.16. Cautions unnumbered. Figures deferred to M2.

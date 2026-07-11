# Direction brief — §6.4 Indefinite Integrals and the Net Change Theorem

Canon variant (Stewart ET 9e §5.4). ⑤ contract. 2026-07-10 per PLAN-ch06.

- **Canon inventory (§5.4):** the indefinite-integral notation \(\int f(x)\,dx = F(x)+C\) for the whole family of antiderivatives (a *function*, vs. the definite integral's *number*); the starter table of antiderivatives (reverse of the Ch2–4 derivative rules), including \(\int\frac1x\,dx=\ln\lvert x\rvert+C\); the Net Change Theorem \(\int_a^b F'(x)\,dx = F(b)-F(a)\) with its rate→net-change reading; displacement vs. total distance for a velocity.
- **Thinness:** canon is *enough* on notation + table + net change. *Thin/none*: the \(\ln\lvert x\rvert\) absolute-value justification and domain caution; the indefinite-vs-definite caution; a displacement-vs-distance worked example.
- **Scope & depth:** introduce the indefinite-integral **notation** (Definition 6.4) building on Def 6.3's antiderivative; give the basic table; **justify \(\int\frac1x\,dx=\ln\lvert x\rvert+C\)** (the \(x<0\) branch: \(\frac{d}{dx}\ln(-x)=\frac1x\)) and flag the domain (\(x\ne0\), two branches) — **forward export** to Ch8/Ch9. State the **Net Change Theorem (Theorem 6.5)** as a *rereading of FTC-2* (Theorem 6.4) — do **not** re-prove; it is FTC-2 with \(f=F'\). Do **not** do substitution (→ §6.5) or any Ch8 technique. Displacement (\(\int v\)) vs. total distance (\(\int\lvert v\rvert\)) closes the loop with §6.1's speed framing.
- **Load-bearing intuition (one):** an indefinite integral packages *every* antiderivative at once (the \(+C\)); and the Net Change Theorem says the definite integral of a rate is the net accumulated change — the same fact as FTC-2, now read as an accounting identity.
- **Worked examples (compute → apply):**
  - **Ex 6.10** — indefinite integrals term by term: \(\int(x^3-6x)\,dx\); \(\int\!\bigl(2e^x-\tfrac{5}{x}\bigr)dx = 2e^x-5\ln\lvert x\rvert+C\) (exercises the \(\ln\lvert x\rvert\)).
  - **Ex 6.11** — a definite integral from the table: \(\int_1^2\frac1x\,dx=[\ln\lvert x\rvert]_1^2=\ln 2\) (here \(x>0\)).
  - **Ex 6.12** — Net Change: a particle with velocity \(v(t)=t^2-4\) on \([0,3]\); displacement \(\int_0^3 v\,dt = -3\) m, total distance \(\int_0^3\lvert v\rvert\,dt = \tfrac{23}{3}\) m (split at \(t=2\)). Displacement vs distance, tying back to §6.1.
- **history / application:** none forced — the net-change reading is itself the application. (Optional one-line on Leibniz's \(dx\) as the "\(+C\)" bookkeeping is unnecessary; skip.)
- **figure_opportunities** (mark now, draw at M2): the velocity \(v(t)=t^2-4\) crossing zero at \(t=2\), signed-area regions below (\([0,2]\)) and above (\([2,3]\)) — displacement = net, distance = total. Mark for M2.
- **Emphasis / takeaway:** concept pivot = indefinite integral = antiderivative family (\(+C\)); definite integral of a rate = net change; portable skill = write basic antiderivatives from the reverse table (incl. \(\ln\lvert x\rvert\)) and split \(\int\lvert v\rvert\) at sign changes for total distance.
- **Deliberately omit (auditor's reverse check):** substitution (→ §6.5); any Ch8 technique; a re-proof of the Net Change Theorem (it is FTC-2); improper integrals; average value (Ch7).
- **Length band:** ~150–200 line fragment (Definition + table + Net Change theorem + 3 examples).
- **Env minted (provisional):** Definition 6.4 (Indefinite integral); Theorem 6.5 (Net Change Theorem); Examples 6.10–6.12. Cautions unnumbered. Figures deferred to M2.

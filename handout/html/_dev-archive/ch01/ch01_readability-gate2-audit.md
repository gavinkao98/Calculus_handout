# Ch1 可讀性回填 — gate-2（Codex）原始輸出轉錄 ＋ triage

> 版控紀錄（scratchpad gitignored、換機即失，故轉錄於此，比照 `ch01_example-supplement-audit.md`）。
> gate-2 = Codex `codex-cli 0.136.0`（PATH，ChatGPT 訂閱）獨立跨模型複核同兩條檢查（① reader-persona、② introduce-before-use）。
> 對**現行（已套用 gate-1 7 條後）**的 Ch1 跑；clean inline UTF-8 餵入（非 -C 自讀）；schema-constrained 輸出。2026-06-28。

## 執行參數

- 指令：`codex exec -s read-only -C <repo> --output-schema schema.json -o out-<sec>.json - < prompt-<sec>.txt`
- 用量：sec-1-1 29,109｜sec-1-2 28,872｜sec-1-3 24,875｜sec-1-4 28,729｜sec-1-5 28,405｜sec-1-6 32,725 ≈ **172,715 token**（訂閱配額；遠低於 30–36 萬估上限）。
- raw findings：25（5+5+5+5+3+2）。

## Triage 結論（要點）

- **gate-2 系統性比 gate-1 嚴**，集中在 U4「每個記號／術語都要 gloss」（邏輯箭號 ⟹⟺、映射 ↦ :B→A、非正式動詞 vanish／blows up／branch／signed direction）——典型 reasoning 模型 over-report，多數 side with gate-1 砍除。
- **真交集（最高信心）：** §1.4 `=∞` 先用後定義（gate-2 sec-1-4 #4 ↔ gate-1 G1-7）——兩模型獨立各自抓到，已套用輕量 forward-ref。
- **gate-2 抓到 gate-1＋Mode B 都漏的迴歸：** sec-1-2 #4——我們的 G1-5 edit 掉了 'integers'。**已修復**（'for integer n'）並重建。這是本輪雙閘的最大價值。
- **refine 既有 edit：** sec-1-2 #3——G1-4 gloss 使 Strategy 1.2 step 2 偏長（F4），建議拆兩句。
- 其餘為低優先 advisory（交裁決）或過度回報（砍除，列於下方各條 disposition）。

## sec-1-1 — 1.1 Inverse Functions  (29,109 tok, 5 findings)

### sec-1-1 #1 — `both` · U4 · Slowed · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** Definitions 1.1-1.2, first logical-arrow symbols
- **quote:** \(\implies\) and \(\Longleftrightarrow\)
- **what_stalls:** The central definitions use symbolic logic before the symbols are named; a first-time L2 reader may not know that these mean “implies” and “if and only if.”
- **Codex minimal_unstick:** On first use, write the relation in words: \(f(x_1)=f(x_2)\) implies \(x_1=x_2\); \(f^{-1}(y)=x\) if and only if \(f(x)=y\).
- **→ triage:** CUT — over-report. \implies/\Longleftrightarrow are standard logic notation, semi-glossed by 'Equivalently' / 'defined by' context. Sided with gate-1 (which did not raise it).

### sec-1-1 #2 — `both` · U4 · Slowed · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** Definition 1.1, one-to-one definition
- **quote:** \[ f(x_{1}) \neq f(x_{2}) \qquad \text{whenever } x_{1} \neq x_{2}. \]
- **what_stalls:** The variables \(x_1\) and \(x_2\) are not explicitly identified as inputs from the domain \(A\), so the quantification has to be inferred.
- **Codex minimal_unstick:** Use: “for all \(x_1,x_2\in A\), \(x_1\neq x_2\) implies \(f(x_1)\neq f(x_2)\).”
- **→ triage:** CUT — non-finding. 'whenever x1 != x2' already makes the quantification clear; pedantic.

### sec-1-1 #3 — `introduce-before-use` · U4 · Slowed · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** Theorem 1.1 proof, final sentence
- **quote:** The correspondence \(y \mapsto x\) therefore defines an inverse function \(f^{-1} : B \to A\).
- **what_stalls:** The mapping symbols \(\mapsto\) and \(:B\to A\) have not been introduced; the reader must infer that they mean a rule sending elements of \(B\) to elements of \(A\).
- **Codex minimal_unstick:** Replace with: “The rule that sends each \(y\in B\) to this unique \(x\in A\) therefore defines an inverse function with domain \(B\) and range \(A\).”
- **→ triage:** CUT — gate-1 explicitly considered \mapsto and :B->A and cut them (self-glossed by 'The correspondence ... defines an inverse function'). Side with gate-1.

### sec-1-1 #4 — `both` · U4 · Slowed · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** Example 1.5 prompt
- **quote:** Restrict its domain so that the restricted function is one-to-one, and find the inverse of the restricted function.
- **what_stalls:** “Restrict its domain” is a new technical action; the solution later demonstrates it, but the prompt asks the reader to act before the term is glossed.
- **Codex minimal_unstick:** Use: “Restrict its domain, meaning replace \(\mathbb{R}\) by a smaller domain, so that the restricted function is one-to-one...”
- **→ triage:** CUT — tier-3. 'Restrict its domain' is this section's teaching point and is demonstrated in the very solution; self-explanatory.

### sec-1-1 #5 — `reader-persona` · U3 · Slowed · Codex tier 2 · n/a
- **locus:** Example 1.8 solution, second sentence
- **quote:** Writing \(t = \tfrac{9}{5} f^{-1}(t) + 32\) and solving,
- **what_stalls:** The variable \(t\) changes roles from the Celsius input of \(f(t)\) to a Fahrenheit input of \(f^{-1}(t)\), and the setup is skipped before the equation appears.
- **Codex minimal_unstick:** Use distinct roles first: “Let \(T\) be a Fahrenheit reading and let \(C=f^{-1}(T)\) be the Celsius temperature that produced it. Then \(T=f(C)=\tfrac95C+32\), so...”
- **→ triage:** ADVISORY (new, plausible) — Example 1.8 reuses t for the Celsius input of f and then the Fahrenheit input of f^{-1}; a genuine role-confusion gate-1 missed. Forward for your nod (fix is a small rewrite introducing distinct names).

**Codex notes:** Checked for introduce-before-use: inverse/inversion, one-to-one, domain/range, \(x_1,x_2\), \(\implies\), \(\Longleftrightarrow\), \(f^{-1}\), reciprocal, independent variable, composition/compositions, \(y\mapsto x\), \(:B\to A\), reflection, restrict/restricted domain, \([0,\infty)\), \(\pm\), rational function, and applied inverse notation. Forward-looking opener terms for later sections were signaled as chapter goals and did not create tier 1-2 stalls here. Clean dimensions: U1, U2, U5, F1, F2, F3, F4, F5.

## sec-1-2 — 1.2 Inverse Trigonometric Functions  (28,872 tok, 5 findings)

### sec-1-2 #1 — `both` · U4 · Slowed · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** Opening paragraph
- **quote:** Inverse trigonometric functions arise whenever we know a ratio and want to recover an angle: from the slope of a ramp, we get an angle of inclination via \(\arctan\); from a ratio of sides in a right triangle, we get an angle via \(\arcsin\) or \(\arccos\).
- **what_stalls:** The symbols \(\arctan\), \(\arcsin\), and \(\arccos\) are used before their individual meanings have been introduced; the reader can infer the topic but not which inverse function each symbol names.
- **Codex minimal_unstick:** Inverse trigonometric functions arise whenever we know a ratio and want to recover an angle: from the slope of a ramp, we get an angle of inclination via inverse tangent, written \(\arctan\); from a ratio of sides in a right triangle, we get an angle via inverse sine \(\arcsin\) or inverse cosine \(\arccos\).
- **→ triage:** CUT — tier-3. arcsin/arccos/arctan in the opener are an intentional informal motivation preview, named in the §1.1 goal list; gate-1 judged clean.

### sec-1-2 #2 — `both` · U4 · Slowed · Codex tier 1 · (a) local gloss/forward-ref
- **locus:** Definition 1.3, displayed equivalence
- **quote:** \(\Longleftrightarrow\)
- **what_stalls:** The equivalence arrow is first used in the formal definition without a gloss; a first-time L2 reader may not know that it means “if and only if,” which is needed to parse the definition.
- **Codex minimal_unstick:** At the first use, add: “Here \(\Longleftrightarrow\) means ‘if and only if.’”
- **→ triage:** CUT — \Longleftrightarrow cluster (see sec-1-1 #1).

### sec-1-2 #3 — `reader-persona` · F4 · Slowed · Codex tier 2 · n/a
- **locus:** Strategy 1.2, step 2
- **quote:** Draw a right triangle using positive side lengths for the magnitude of the known ratio; keep track of the sign separately, using the principal-value interval (the range of the inverse function, fixed in its definition) to settle it.
- **what_stalls:** This step asks the reader to handle magnitude, sign, and principal-value interval in one long instruction; the method is recoverable, but the first-read load is high.
- **Codex minimal_unstick:** Draw a right triangle using positive side lengths, using the absolute value of the known ratio for those lengths. Keep the sign separate, and use the principal-value interval (the range fixed in the inverse function's definition) to decide it.
- **→ triage:** ADVISORY (refines applied G1-4) — our G1-4 gloss lengthened Strategy 1.2 step 2, which gate-2 now rates a mild F4 (magnitude + sign + principal-value in one instruction). Consider splitting into two sentences. RECOMMEND.

### sec-1-2 #4 — `both` · U4 · Slowed · Codex tier 1 · (a) local gloss/forward-ref
- **locus:** Example 1.11 solution
- **quote:** The particle does reach height \(1\) at the times \(t = 2\pi n\); because the motion exists only for \(t \ge 10\), this requires \(2\pi n \ge 10\), i.e. \(n \ge 2\), but \(\arccos(1) = 0\) is not one of them.
- **what_stalls:** The parameter \(n\) is introduced without saying that it is an integer; otherwise the description of the times \(t=2\pi n\) is incomplete.
- **Codex minimal_unstick:** The particle does reach height \(1\) at the times \(t = 2\pi n\), where \(n\in\mathbb{Z}\); because the motion exists only for \(t \ge 10\), this requires \(2\pi n \ge 10\), i.e. \(n \ge 2\), but \(\arccos(1) = 0\) is not one of them.
- **→ triage:** FIXED — regression from applied G1-5. Our edit dropped the word 'integers'; restored as 'for integer n' and rebuilt. This is the cross-model catch gate-1 + Mode B both missed.

### sec-1-2 #5 — `introduce-before-use` · U4 · Minor · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** Remark 1.3
- **quote:** In this text we use \(y \in \left[0, \tfrac{\pi}{2}\right) \cup \left[\pi, \tfrac{3\pi}{2}\right)\) because it makes the differentiation formulas for the inverse secant simpler.
- **what_stalls:** “Differentiation formulas” is a calculus term used as a reason before differentiation has been introduced in the listed prior material; the reader does not need the formula here, but needs to know this is a forward reference.
- **Codex minimal_unstick:** In this text we use \(y \in \left[0, \tfrac{\pi}{2}\right) \cup \left[\pi, \tfrac{3\pi}{2}\right)\) because it makes the later derivative formula for inverse secant simpler.
- **→ triage:** ADVISORY (low) — Remark 1.3 'differentiation formulas' is a forward-reference to Ch3; could read 'later derivative formula'. Minor.

**Codex notes:** For introduce-before-use, checked inverse-trig names and notations (arcsin/sin^{-1}, arccos/cos^{-1}, arctan/tan^{-1}, arccsc/csc^{-1}, arcsec/sec^{-1}, arccot/cot^{-1}), \(\Longleftrightarrow\), \(\in\), \(\cup\), \(\pm\), \(|x|\), parameters such as \(\theta\), \(y\), and \(n\), interval notation, principal value/principal range, reference-triangle method, branch/branch convention, asymptote, inner/outer function, and differentiation formulas. No tier 1-2 issues found in U1, U2, U3, U5, F1, F2, F3, or F5.

## sec-1-3 — 1.3 The Limit of a Function  (24,875 tok, 5 findings)

### sec-1-3 #1 — `both` · U4 · Slowed · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** Definition 1.9, limit definition sentence
- **quote:** and say that the <em>limit</em> of \(f(x)\) as \(x\) approaches \(a\) is \(L\) if \(f(x)\) can be made arbitrarily close to \(L\) whenever \(x\) is sufficiently close to \(a\) but not equal to \(a\).
- **what_stalls:** The technical phrases “arbitrarily close” and “sufficiently close” carry the whole definition, but they are first used without a quick L2-friendly gloss.
- **Codex minimal_unstick:** and say that the <em>limit</em> of \(f(x)\) as \(x\) approaches \(a\) is \(L\) if, by taking \(x\) close enough to \(a\) with \(x \ne a\), we can make \(f(x)\) as close to \(L\) as we wish.
- **→ triage:** CUT — tier-3. 'arbitrarily/sufficiently close' are the standard informal-limit phrases and Definition 1.9 itself is the gloss; gate-1 clean. (Also: rewriting a definition is higher-risk.)

### sec-1-3 #2 — `reader-persona` · U3 · Slowed · Codex tier 2 · n/a
- **locus:** Caution 1.5, second paragraph
- **quote:** In truth, near \(0\) the graph keeps oscillating between \(-1\) and \(1\), no matter how closely we zoom in — \(f\) runs through every value in \([-1, 1]\) infinitely often as \(x \to 0\), so the limit does not exist.
- **what_stalls:** After two sample lists, the universal claim that every value in \([-1,1]\) occurs infinitely often is asserted without the small periodicity reason that connects it to \(\sin(\pi/x)\).
- **Codex minimal_unstick:** Because \(\pi/x\) grows without bound as \(x \to 0\), the sine cycle repeats indefinitely. Thus, near \(0\) the graph keeps oscillating between \(-1\) and \(1\), no matter how closely we zoom in.
- **→ triage:** ADVISORY (low) — Caution 1.5 could add 'pi/x -> infinity, so the sine cycle repeats' before 'runs through every value infinitely often'. Mild enrichment; the two conflicting sample lists already imply it.

### sec-1-3 #3 — `reader-persona` · U3 · Slowed · Codex tier 2 · n/a
- **locus:** Instantaneous-velocity paragraph, algebra display
- **quote:** \[ \frac{s(4) - s(t)}{4 - t} = \frac{40 - (30t - 5t^{2})}{4 - t} = \frac{5(t - 2)(t - 4)}{4 - t} = -5(t - 2), \qquad t \neq 4. \]
- **what_stalls:** The cancellation uses \(4-t=-(t-4)\), but that sign change is skipped; a first-read learner may not see why the result is negative.
- **Codex minimal_unstick:** \[ \frac{40 - (30t - 5t^{2})}{4 - t} = \frac{5(t - 2)(t - 4)}{-(t - 4)} = -5(t - 2), \qquad t \neq 4. \]
- **→ triage:** ADVISORY (low, math display) — the cancellation 5(t-2)(t-4)/(4-t) = -5(t-2) skips 4-t = -(t-4); could show the -(t-4) step. Borderline (math display).

### sec-1-3 #4 — `both` · U4 · Minor · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** Instantaneous-velocity paragraph, formula for velocity
- **quote:** \[ v(4) = \lim_{t \to 4} \frac{s(4) - s(t)}{4 - t} = \lim_{t \to 4} \bigl[-5(t - 2)\bigr] = -10 \text{ m/s}. \]
- **what_stalls:** The notation \(v(4)\) appears before the text says that \(v\) denotes velocity; the reader can infer it, but must pause.
- **Codex minimal_unstick:** Writing \(v(4)\) for the instantaneous velocity at \(t=4\),\n\[ v(4) = \lim_{t \to 4} \frac{s(4) - s(t)}{4 - t} = \lim_{t \to 4} \bigl[-5(t - 2)\bigr] = -10 \text{ m/s}. \]
- **→ triage:** ADVISORY (low) — gloss v(4) as 'the instantaneous velocity at t=4' before the display. Tiny.

### sec-1-3 #5 — `both` · U4 · Slowed · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** Instantaneous-velocity paragraph, final sentence
- **quote:** Notice that the original ratio has the indeterminate form \(\tfrac{0}{0}\) at \(t = 4\) — both \(s(4) - s(t)\) and \(4 - t\) tend to \(0\) — so the cancellation that produced \(-5(t - 2)\) was what made the limit accessible.
- **what_stalls:** “Indeterminate form” is a new technical term. The dash explains the zero-over-zero shape, but not that the term means the limit is not determined until more work is done.
- **Codex minimal_unstick:** Notice that, as \(t \to 4\), the original ratio has the indeterminate form \(\tfrac{0}{0}\): both \(s(4)-s(t)\) and \(4-t\) tend to \(0\), so the ratio must be simplified before the limit can be read.
- **→ triage:** NOTED — reinforces gate-1 G1-6 (which the gate-1 verifier CUT). gate-2 independently re-raises 'indeterminate form' used in §1.3 before §1.5. §1.3 already says 'both ... tend to 0'. Optional light forward-ref; partial two-model agreement gives it slight weight.

**Codex notes:** Introduce-before-use scan checked: \(s(t)\), \(h\), average velocity, instantaneous velocity, \(f,y,x\), \(\lim_{x\to a} f(x)=L\), \(f(x)\to L\), \(f(a)\), open dot/solid dot, height, curve, table/sample language, \(\sin(\pi/x)\), ellipsis notation, \([-1,1]\), oscillating, \(v(4)\), indeterminate form \(0/0\), one-sided limits, and infinite limits. Clean dimensions among reported scope: U1, U2, U5, F1, F2, F3, F4, F5.

## sec-1-4 — 1.4 One-Sided and Infinite Limits  (28,729 tok, 5 findings)

### sec-1-4 #1 — `both` · U4 · Slowed · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** Proposition 1.5 display
- **quote:** \Longleftrightarrow
- **what_stalls:** The biconditional arrow is first used without a gloss; an L2 precalculus reader may not know that it means “if and only if.”
- **Codex minimal_unstick:** Add immediately after the display: “Here \(\Longleftrightarrow\) means ‘if and only if.’”
- **→ triage:** CUT — \Longleftrightarrow cluster (see sec-1-1 #1).

### sec-1-4 #2 — `both` · U4 · Minor · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** Example 1.20 solution, first paragraph
- **quote:** From the left we use the branch \(f(x) = x + 1\), so \(\lim_{x \to 2^{-}} f(x) = 3\).
- **what_stalls:** “Branch” is used as a piecewise-function term before being glossed; the reader can infer it, but may pause on the word.
- **Codex minimal_unstick:** From the left we use the branch, the formula valid when \(x<2\), so \(\lim_{x \to 2^{-}} f(x) = 3\).
- **→ triage:** CUT — tier-3. 'branch' for a piecewise formula is context-clear.

### sec-1-4 #3 — `both` · U4 · Slowed · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** Example 1.22 solution, final paragraph
- **quote:** Since the values do not all grow in the <em>same</em> signed direction, we do <strong>not</strong> write \(\lim_{x \to 0} \frac{1}{x} = \infty\).
- **what_stalls:** “Signed direction” is not a standard introduced term, and it carries the key distinction between two-sided infinite behavior and disagreement of one-sided behavior.
- **Codex minimal_unstick:** Since the values do not all become unbounded with the same sign, both toward \(+\infty\) or both toward \(-\infty\), we do <strong>not</strong> write \(\lim_{x \to 0} \frac{1}{x} = \infty\).
- **→ triage:** CUT — tier-3. 'signed direction' is immediately glossed by 'Contrast 1/x^2: both sides grow positively'.

### sec-1-4 #4 — `reader-persona` · U3 · Slowed · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** Example 1.22 solution, final sentence
- **quote:** Contrast \(1/x^{2}\): both sides grow positively, so there we do write \(\lim_{x \to 0} \frac{1}{x^{2}} = \infty\) (Figure 1.16).
- **what_stalls:** The previous example said the ordinary limit of \(1/x^2\) does not exist; this sentence switches to \(=\infty\) before the definition and caution distinguish infinite-limit notation from an ordinary finite limit.
- **Codex minimal_unstick:** Contrast \(1/x^{2}\): both sides grow positively, so, in the infinite-limit notation defined below, we write \(\lim_{x \to 0} \frac{1}{x^{2}} = \infty\) (Figure 1.16).
- **→ triage:** INTERSECTION (<-> gate-1 G1-7, applied) — both gates independently flag '=infinity' used before Definition 1.11. Our light forward-ref (at the -infinity display) is applied; gate-2 suggests also signposting the 1/x^2 contrast sentence. OPTIONAL refinement; the existing forward-ref arguably already covers the notation.

### sec-1-4 #5 — `both` · U4 · Minor · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** Example 1.24 solution, middle sentence
- **quote:** If \(g(x) = 1\), then \(f(x) = \frac{1}{x^{2} - 9}\) blows up near \(-3\), and \(x = -3\) is a vertical asymptote.
- **what_stalls:** “Blows up” is an unintroduced informal term for unbounded behavior; an L2 reader may not connect it immediately to infinite one-sided limits.
- **Codex minimal_unstick:** If \(g(x) = 1\), then \(f(x) = \frac{1}{x^{2} - 9}\) has infinite one-sided limits at \(-3\), so \(x = -3\) is a vertical asymptote.
- **→ triage:** CUT — tier-3. 'blows up' is informal but transparent; Example 1.24 is precisely about asymptote-vs-not.

**Codex notes:** For introduce-before-use, checked: one-sided limit notation \(a^-\), \(a^+\), left-hand/right-hand limit, two-sided limit, \(\Longleftrightarrow\), \(\mathbb R\), piecewise branch, infinite-limit notation \(=\infty\), \(=-\infty\), same signed direction, vertical asymptote, \(\pm\infty\), candidate point, rational function, nonzero/0 form, denominator zero, domain, \(\ln x\), and boundary of the domain. Clean dimensions: U1, U2, U5, F1, F2, F3, F4, F5.

## sec-1-5 — 1.5 Limit Laws and Computational Techniques  (28,405 tok, 3 findings)

### sec-1-5 #1 — `both` · U4 · Minor · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** Direct substitution, paragraph after Proposition 1.6
- **quote:** For polynomials and rational functions where the denominator does not vanish at \(a\), direct substitution is therefore the fastest route to the limit.
- **what_stalls:** “Vanish” is first used here as a mathematical verb; an L2 first-time reader may not immediately parse it as “equals zero.”
- **Codex minimal_unstick:** For polynomials and rational functions where the denominator is not zero at \(a\), direct substitution is therefore the fastest route to the limit.
- **→ triage:** CUT — over-report (vocabulary swap). 'vanish' is standard math English; 'is not zero' is the kind of nitpick the rubric warns against, not a real first-read stall.

### sec-1-5 #2 — `reader-persona` · U3 · Slowed · Codex tier 2 · n/a
- **locus:** Example 1.28 solution, item 2
- **quote:** Replacing \(10\) by any constant \(c\) gives limit \(c\). The choice \(f(x) = x - 3\), \(g(x) = (x - 3)^{3}\) gives \(\infty\), and reversing the sign of \(g\) gives \(-\infty\). Finally, \(f(x) = x - 3\), \(g(x) = |x - 3|\) makes the limit fail to exist.
- **what_stalls:** Several outcomes are asserted without showing the quotient being tested, so the reader must supply multiple algebra and one-sided-limit checks at once.
- **Codex minimal_unstick:** Add: \(\frac{x-3}{(x-3)^3}=\frac{1}{(x-3)^2}\to\infty\), \(\frac{x-3}{-(x-3)^3}=-\frac{1}{(x-3)^2}\to-\infty\), and \(\frac{x-3}{|x-3|}\) has right-hand limit \(1\) and left-hand limit \(-1\).
- **→ triage:** CUT — relates to applied G1-11. Our split already fixed the F3 parseability; adding every worked quotient risks bloating the example whose point is 'can equal anything'.

### sec-1-5 #3 — `reader-persona` · U3 · Slowed · Codex tier 2 · n/a
- **locus:** Example 1.34 solution, opening sentence
- **quote:** We cannot apply the product law because \(\lim_{x \to 0} \sin(1/x)\) does not exist.
- **what_stalls:** The nonexistence of \(\lim_{x \to 0}\sin(1/x)\) is used as a reason before any oscillation explanation in this section.
- **Codex minimal_unstick:** We cannot apply the product law: as \(x \to 0\), \(1/x\) takes arbitrarily large positive and negative values, so \(\sin(1/x)\) oscillates and \(\lim_{x \to 0}\sin(1/x)\) does not exist.
- **→ triage:** CUT — gate-2 cross-section blind spot. The non-existence of lim sin(1/x) was already motivated in §1.3 Caution 1.5; the reason IS available to a linear reader.

**Codex notes:** Ran only the two requested checks. For introduce-before-use I checked: limit laws, \(c,L,M,n\), quotient/product/sum/difference laws, numerator/denominator, \(0/0\), direct substitution, polynomial/rational function, indeterminate form, rationalize, common denominator, piecewise-defined function/branch, \([x]\)/\(\lfloor x\rfloor\), one-sided limits, squeeze theorem/bounds, \(\pm\infty\), vertical asymptote, and the Chapter 3 derivative reference. No tier 1-2 findings in U1, U2, U5, F1, F2, F3, F4, or F5.

## sec-1-6 — 1.6 The Precise Definition of a Limit  (32,725 tok, 2 findings)

### sec-1-6 #1 — `both` · U4 · Minor · Codex tier 2 · (a) local gloss/forward-ref
- **locus:** opening motivation, paragraph 1
- **quote:** The modern resolution, developed in the nineteenth century, is the \(\varepsilon\)-\(\delta\) definition of a limit, which gave calculus the level of rigor used in modern mathematics.
- **what_stalls:** The central notation \(\varepsilon\)-\(\delta\) is named before \(\varepsilon\) and \(\delta\) are identified as tolerances, so a linear first-read has to carry unexplained Greek-letter notation through the historical note.
- **Codex minimal_unstick:** The modern resolution, developed in the nineteenth century, is the \(\varepsilon\)-\(\delta\) definition of a limit (defined below using two positive tolerances, \(\varepsilon\) and \(\delta\)), which gave calculus the level of rigor used in modern mathematics.
- **→ triage:** ADVISORY (low) — the historical opening names 'the epsilon-delta definition' before the tolerance gloss (line 25); could add '(two positive tolerances, epsilon and delta)'. Minor; reads almost as a proper noun there.

### sec-1-6 #2 — `reader-persona` · U3 · Slowed · Codex tier 1 · (a) local gloss/forward-ref
- **locus:** Example 1.41 solution, first bounding step
- **quote:** The factor \(|x - 4|\) depends on \(x\). To control it, first assume \(|x - 1| < 1\).
- **what_stalls:** The proof adds an extra restriction before explaining that \(\delta\) will later be chosen no larger than 1; the reader may think an unproved assumption has been inserted.
- **Codex minimal_unstick:** The factor \(|x - 4|\) depends on \(x\). We may impose a preliminary restriction, say \(|x - 1| < 1\), because we will later choose \(\delta \le 1\).
- **→ triage:** ADVISORY (low) — Example 1.41 'first assume |x-1| < 1': add 'because we will later take delta <= 1'. gate-1 judged not-a-stall; gate-2 rated tier-1; a one-clause aid is reasonable, not blocking.

**Codex notes:** Introduce-before-use scan checked \(\varepsilon,\delta,a,L,M,N\), \(\min\{\cdot\}\), piecewise notation, open interval, punctured interval, neighborhood, target strip, implication, triangle inequality, auxiliary factor/bound/bounded, continuity, inverse/trig summary terms, and the derivative/secant-slope preview. No tier 1-2 findings arose in U1, U2, U5, F1, F2, F3, F4, or F5; only U3 and U4 appear above.

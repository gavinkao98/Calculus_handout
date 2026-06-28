# Ch2 可讀性回填 — gate-2（Codex）原始輸出轉錄 ＋ triage

> 版控紀錄（scratchpad gitignored、換機即失，故轉錄於此，比照 `ch01_readability-gate2-audit.md`）。
> gate-2 = Codex `codex-cli 0.136.0`（PATH，ChatGPT 訂閱）獨立跨模型複核同兩條檢查（① reader-persona、② introduce-before-use）。
> 對**現行（已套用 gate-1 G1-1·G1-2·G1-8 ＋ 3 處圖號 cross-ref 後）**的 Ch2 五節跑；clean inline UTF-8 餵入（非 -C 自讀）；schema-constrained 輸出；輸出 0 個 U+FFFD（編碼乾淨）。2026-06-28。

## 執行參數

- 指令：`codex exec -s read-only -C <repo> --output-schema schema.json -o out-<sec>.json - < prompt-<sec>.txt`（prompt 經 stdin 餵 raw UTF-8）
- 用量：sec-2-1 19,305｜sec-2-2 23,772｜sec-2-3 24,224｜sec-2-4 26,387｜sec-2-5 21,468 ≈ **115,156 token**（訂閱配額；遠低於 30–36 萬上限，亦低於 ~13–17 萬估值）。
- raw findings：9（2+1+2+2+2）。
- 編碼 smoke test（sec-2-1）：JSON 解析 OK、U+FFFD=0、em-dash／§／√／\sin\theta 輸入皆正常 → 通過後續跑其餘 4 節。

## Triage 結論（要點）

- **0 blocking。** 9 raw → **1 迴歸/交集 refine**（G2-8，命中 G1-8 套用）＋ **2 建議**（G2-6 `m` 綁定、G2-9 `linearity` gloss）＋ **4 低優先**（G2-3/4/5/7）＋ **2 砍**（G2-1/2）。
- **本輪 gate-2 最大價值＝G2-8**：命中 gate-1 套用後的迴歸——我把 G1-8 改成「g(x)=x, so that f/g=1/x」時，把原本顯式的 `f=1` 變成隱含；Codex 獨立讀到並點出（對照 Ch1 掉 `integers`）。
- **gate-2 系統性偏嚴**：opener 主題預告（G2-1）、`operator` 自解（G2-2）被 over-report，已 triage 砍。
- 其餘為真實但低優先 advisory（多為單一符號就地綁定／一句 gloss／拆長句），交使用者逐條裁決。

## sec-2-1 — 2.1 The Tangent Line and the Derivative at a Point  (19,305 tok, 2 findings)

### G2-1 — `both` · U4 · Slowed · Codex tier 2 · (a) local
- **locus:** chapter opener, lead paragraph
- **quote:** Geometrically the derivative gives the slope of the tangent line at each point of a curve; physically it gives the instantaneous rate of change of a quantity that varies in time; algebraically it satisfies a small set of arithmetic rules that turn differentiation into a procedure rather than a per-problem invention.
- **what_stalls:** Before the section has introduced tangent lines, instantaneous rate of change, or differentiation, the opener uses all three as if they are already stable ideas. A first-time L2 reader can infer that these are chapter themes, but not what each phrase means yet.
- **Codex minimal_unstick:** Add a brief signal such as: “The meanings of tangent line, instantaneous rate, and differentiation will be developed in this chapter.”
- **→ triage:** CUT — 章開場本就預告全章主題（CONTENT_SPEC §4 opener 的功能），非有害的先用後定義；Codex 建議的「The meanings … will be developed」會加 §3「避免」清單點名的 meta-commentary。gate-1 未提。

### G2-2 — `1 reader-persona` · U2 · Minor · Codex tier 3 · (a) local
- **locus:** chapter opener, lead paragraph
- **quote:** an operator that takes a function and returns another function describing how fast it is changing
- **what_stalls:** “Operator” is a compact formal word at the first introduction of derivative, and the same section later stresses that f'(a) is a number at one point. The prose is recoverable, but a first-read learner may briefly wonder whether a derivative is a number or a function.
- **Codex minimal_unstick:** Add a parenthetical gloss: “operator (a rule acting on functions)” or add “Later in the chapter” before this function-level description.
- **→ triage:** CUT — 就地自解：「operator that takes a function and returns another function」本身即 gloss；建議的括號與既有 gloss 重複。

**Codex notes:** clean dimensions — U1,U3,U5,F1-F5 clean overall; no blocking readability issue found.

notation/terms checked — Checked derivative, operator, tangent line, instantaneous rate of change, differentiation, secant slope/secant line, difference quotient, h-form, increment h, f'(a), f' as a function, local linearity, differentiable, linearization, power rule, constant-multiple rule, sum rule, product rule, quotient rule, higher-order derivatives f'', f''', f^(n), lim forms, P,Q,a,h,m notation.

verdict — Comprehensibility is mostly clean with no blocking issue; introduce-before-use has a mild opener-level forward dependency, but the section proper introduces its main notation in usable order.

## sec-2-2 — 2.2 The Derivative as a Function  (23,772 tok, 1 findings)

### G2-3 — `1 reader-persona` · U3 · Slowed · Codex tier 2 · (a) local
- **locus:** paragraph immediately after Definition 2.2
- **quote:** This is the same limit we met in §2.1: the substitution \(x = a + h\) turns it into \(\lim_{x \to a}\bigl(f(x) - f(a)\bigr)/(x - a)\) with the fixed point renamed.
- **what_stalls:** The current formula uses \(x\) as the symbolic input, while the recalled \(x\to a\) form also uses \(x\) as the moving input. A first-time linear reader must reconstruct the renaming before the substitution feels justified.
- **Codex minimal_unstick:** Add a bridging clause with a spare letter, e.g. “If the fixed point is called \(a\) and the nearby input is \(u=a+h\), then ...”.
- **→ triage:** ADVISORY（低，交裁決）— 真實但小：§2.2 h-form 以 x 為符號基點，回憶句「x=a+h」又把 x 當移動點，同字兩角色；「with the fixed point renamed」已示警、可回神。修法（引入 u=a+h 或改寫）易過度複雜，交你定。

**Codex notes:** clean dimensions — U1,U2,U4,U5,F1-F5 clean; one local U3 slowdown only.

notation/terms checked — Checked f', f'(x), derivative of f as a function, h-form, domain, exists, difference quotient, conjugate/rationalizing, common denominator, horizontal tangent, proper subset, prime notation, y', dy/dx, df/dx, d/dx, Leibniz notation, operator, Delta y / Delta x, increment, differentiate with respect to, v(t), s''(t)/second derivative, P'(t), C'(q), marginal cost, differentiability.

verdict — Comprehensibility is clean except for one non-blocking renaming bridge; introduce-before-use is clean with no blocking findings.

## sec-2-3 — 2.3 Differentiability, Continuity, and Higher Derivatives  (24,224 tok, 2 findings)

### G2-4 — `1 reader-persona` · U3 · Slowed · Codex tier 2 · (a) local
- **locus:** Example 2.13, opening of solution
- **quote:** Away from \(x = 2\) each piece is a polynomial and therefore differentiable, so the only point in question is \(x = 2\).
- **what_stalls:** Before differentiation rules have been developed, “therefore differentiable” invokes a general polynomial fact the first-time reader may not yet feel entitled to use.
- **Codex minimal_unstick:** Add a local bridge: on \(x<2\) and \(x>2\), the formulas are \(x^2\) and a line, whose difference quotients have finite limits; only the joining point can fail.
- **→ triage:** ADVISORY（低，交裁決）— 邊界 hard-but-fair：§2.1–§2.2 已多次由定義算出多項式導數，「each piece is a polynomial and therefore differentiable」是合理歸納；嚴格通則要到 §2.4。honestly Minor。交你定。

### G2-5 — `1 reader-persona` · F4 · Minor · Codex tier 3 · (a) local
- **locus:** Caution after Remark 2.5
- **quote:** So \(d^{2}y\) means “\(d\) applied to \(y\) twice,” not \(d\) times \(2y\); and the \(dx^{2}\) is part of the symbol for differentiating twice with respect to \(x\) — not \(d(x^{2})\), where the \(x\) itself would be squared, and not an algebraic denominator to cancel or split.
- **what_stalls:** The sentence carries several negated misreadings at once, which can force an L2 first-time reader to reread to separate the cases.
- **Codex minimal_unstick:** Keep the same math but split it into shorter sentences: one for \(d^2y\), one for \(dx^2\), and one for the “not a denominator” warning.
- **→ triage:** ADVISORY（低，交裁決）— 真 F4：d²y/dx² caution 一句連串多個「not X」否定誤讀，建議拆短句（純拆句、不改任何內容/數學）。交你定。

**Codex notes:** clean dimensions — U1,U2,U4,U5,F1,F2,F3,F5 clean

notation/terms checked — Checked differentiable/differentiability, finite derivative limit, \(f'(a)\), h-form difference quotient, one-sided limits, corner, vertical tangent, continuity/converse, proper subset, piecewise/cases notation, branch, left-/right-hand derivative, higher derivatives, \(f''\), \(f'''\), \(f^{(n)}\), \(f^{(0)}\), \(d^{2}y/dx^{2}\), \(d^{n}y/dx^{n}\), operator \(d/dx\), acceleration, jerk; no introduce-before-use issue found.

verdict — No blocking issue: introduce-before-use is clean; comprehensibility has two local first-read slowdowns only.

## sec-2-4 — 2.4 Derivatives of Polynomials and the Exponential Function  (26,387 tok, 2 findings)

### G2-6 — `both` · U4 · Minor · Codex tier 2 · (a) local
- **locus:** Caution after the positive-integer power rule
- **quote:** this can be checked by applying the same factorization idea to \(1/x^{m}\)
- **what_stalls:** The text switches from the stated negative integer \(n\) to \(m\) without saying that \(m\) is positive and \(n=-m\). A first-time L2 reader may pause to infer the reindexing.
- **Codex minimal_unstick:** Add a local binding: “where \(m=-n>0\)” or rewrite as “to \(x^{-m}=1/x^m\) with \(m>0\).”
- **→ triage:** 建議採納 — m 確實未定義（n 為負整數，1/x^m 的 m 憑空出現）；補「where m=−n>0」是乾淨綁定、無 dumbing、不軟化。

### G2-7 — `2 introduce-before-use` · U4 · Minor · Codex tier 2 · (a) local
- **locus:** Theorem 2.5 statement on higher derivatives
- **quote:** Consequently every higher derivative is \(e^{x}\) as well: \(f^{(n)}(x) = e^{x}\) for all \(n\).
- **what_stalls:** The symbol \(f\) has not been locally bound to \(e^x\) in this theorem statement, so the higher-derivative notation is momentarily ambiguous.
- **Codex minimal_unstick:** Change to “Consequently, if \(f(x)=e^x\), then every higher derivative is \(e^x\): \(f^{(n)}(x)=e^x\).”
- **→ triage:** ADVISORY（低，交裁決）— Theorem 2.5 敘述中 f 未就地綁為 e^x，f^(n) 暫時無依；惟定理通篇即講 e^x、語境清楚，且動到定理敘述需謹慎。交你定。

**Codex notes:** clean dimensions — U1,U2,U3,U5,F1-F5 clean; only localized U4 binding issues found.

notation/terms checked — Checked: difference quotient, h-form, x->a derivative form, f'(x), d/dx, positive integer n, x^n-a^n factorization, binomial coefficients, constant rule, power rule, negative/fractional/real exponents, sum rule, constant-multiple rule, polynomial coefficients a_k, chain rule and quotient rule forward references, tangent line, power series, convergence, e^x, higher derivatives f'', f^(n), y'=ky, b^x, ln b, x^e, x^r.

verdict — No blocking readability issue; comprehensibility is clean overall, with two minor introduce-before-use/local-binding fixes recommended.

## sec-2-5 — 2.5 The Product and Quotient Rules  (21,468 tok, 2 findings)

### G2-8 — `1 reader-persona` · U3 · Slowed · Codex tier 2 · (a) local
- **locus:** quotient-rule motivation paragraph before the proof
- **quote:** take the simplest denominator, \(g(x) = x\), so that \(f/g = 1/x\)
- **what_stalls:** The numerator has silently become 1. A first linear reader may pause because \(g(x)=x\) alone would make \(f/g=f(x)/x\), not necessarily \(1/x\).
- **Codex minimal_unstick:** Add a bridge such as: “with numerator \(f(x)=1\)” before “so that.”
- **→ triage:** ★ 迴歸／交集（最高信心，建議 refine）— 命中已套用的 G1-8 文字「take the simplest denominator, g(x)=x, so that f/g=1/x」把 f=1 留為隱含（原文有顯式 f=1）。建議補「with numerator f(x)=1」使 g=x 與 f=1 皆顯式。正是 gate-2 抓 gate-1 套用迴歸的價值（對照 Ch1 G2-9 掉 integers）。

### G2-9 — `2 introduce-before-use` · U4 · Minor · Codex tier 3 · (a) local
- **locus:** Chapter summary, rules paragraph
- **quote:** and linearity (Theorem 2.4)
- **what_stalls:** “Linearity” is used as a technical label, but the prior-section ledger introduced the sum rule and constant-multiple rule, not this name for them.
- **Codex minimal_unstick:** Gloss locally as “linearity, meaning the sum and constant-multiple rules (Theorem 2.4).”
- **→ triage:** 建議採納 — 「linearity」是 §2.4 Theorem 2.4（sum＋constant-multiple rules）未用過的新標籤、章末才出現；補一句 gloss「linearity, meaning the sum and constant-multiple rules (Theorem 2.4)」乾淨且接得上。

**Codex notes:** clean dimensions — U1,U2,U5,F1-F5 clean; U3 and U4 have only the two local issues listed.

notation/terms checked — Checked product rule, quotient rule, (fg)', f'g', d/dx, f/g, Delta f, Delta g, h, Delta x, difference quotient, differentiable, continuous, g(x) ne 0, g^2, top/bottom, mnemonic, marginal revenue, genuine quotient/product, outermost structure, composition, chain rule, basepoint, linearity.

verdict — Comprehensibility is mostly clean with no blocking issue; introduce-before-use is clean except the unglossed term “linearity.”

# Ch 1 HTML exercise coverage matrix pilot

日期：2026-06-11  
分支：`experiment/seed-converge`  
工作面：HTML handout kit，內容來源為 `experiments/handout_kit/example-ch01/sec-*.html`。

## Pilot assumptions

- 本檔是 HTML 講義的 coverage matrix 與候選題清單，尚未把題目寫進
  `example-ch01/sec-*.html`。
- `example-ch01/sec-1-1.html` 到 `sec-1-6.html` 目前沒有 `env-exercise` 區塊；
  因此「手稿題已覆蓋」先記為無。
- 既有 worked examples 是教學內容，不拿來抵 end-of-section exercise coverage。
- 題庫候選只做短摘要；完整 question / hint / answer / solution 等到使用者接受後，
  再存進 `experiments/handout_kit/ch01_exercise-imports.md`。
- Ch 1 standalone 目前同時是範本：`gen_standalone.py` 只重生 Ch 2/3，並以
  `chapter1-standalone.html` / `chapter1-print-standalone.html` 當骨架。若 pilot 題目要進
  HTML，建議先讓 Ch 1 也能由 `example-ch01/` 重生，或明確決定手改 standalone；前者較安全。

## HTML insertion model

Accepted exercises should be inserted at the end of each relevant fragment, before `</article>`:

```html
<h3 class="subsec-head">Exercises</h3>

<!-- [source: CLP-1 §1.4 #25] -->
<section class="env env-exercise">
  <p class="env-head"><span class="env-kicker">Exercise</span><span class="env-num">1</span></p>
  <div class="env-body">
    <p>Prompt text.</p>
  </div>
</section>
```

Open display choices for the later HTML-contract update:

- `env-num` should likely restart at `1` in each section, matching `CONTENT_EXERCISES.md`.
- `[source:]` should remain an HTML comment for now, not visible shipped text.
- Difficulty markers remain deferred; do not encode them.
- Type taxonomy can remain in this matrix/import record until the full exercise design round.

## Legend

- `C...`：下方「Candidate bank」中的候選題。
- `open`：本輪題庫沒有乾淨候選；若使用者認為該格必練，再進 AI fallback 或人工出題。
- `optional`：教學點在本節只是 preview / aside，不建議為了矩陣湊題。
- 題型欄使用 `CONTENT_EXERCISES.md` 的四類：`conceptual`, `computational`,
  `reasoning`, `applied`。

## Section 1.1 - Inverse Functions

| Taught item | conceptual | computational | reasoning | applied |
|---|---|---|---|---|
| one-to-one definition | C1.1-A, C1.1-B, C1.1-C | C1.1-D | C1.1-D | C1.1-C |
| horizontal line test | C1.1-E | C1.1-E | C1.1-E | optional |
| inverse function definition and graph reflection | C1.1-F | C1.1-G | C1.1-G | C1.1-H |
| composition identities `f^{-1}(f(x))=x`, `f(f^{-1}(y))=y` | C1.1-F | C1.1-G | C1.1-G | C1.1-H |
| finding an inverse algebraically | C1.1-I | C1.1-G, C1.1-J | C1.1-J | C1.1-H |
| restricting a domain to make an inverse | C1.1-I | C1.1-J | C1.1-E, C1.1-J | optional |

Notes:

- Good pilot target: 8-10 exercises after curation.
- APEX 02.7 has compact algebraic inverse checks; Mooculus has better conceptual/graphical items.

## Section 1.2 - Inverse Trigonometric Functions

| Taught item | conceptual | computational | reasoning | applied |
|---|---|---|---|---|
| trig functions need domain restrictions before inversion | C1.2-A | open | C1.2-C | C1.2-C |
| principal ranges of `arcsin`, `arccos`, `arctan` | C1.2-B | C1.2-D | C1.2-C | C1.2-C |
| `sin^{-1}` notation trap | C1.2-A | C1.2-D | C1.2-A | optional |
| inverse trig identities and their interval restrictions | C1.2-B | C1.2-D | C1.2-C | optional |
| triangle method for expressions such as `tan(arcsin x)` | C1.2-F | C1.2-D, C1.2-F | C1.2-F | optional |
| remaining inverse trig functions and domains | C1.2-E | C1.2-D | C1.2-E | optional |

Notes:

- CLP-1 inverse trig material lives in a later derivative section; use only the non-derivative
  domain / range / triangle parts.
- The Mooculus exact-value list is dense; split it into 3-5 selected items rather than importing the
  whole list.

## Section 1.3 - The Limit of a Function

| Taught item | conceptual | computational | reasoning | applied |
|---|---|---|---|---|
| informal limit definition | C1.3-A, C1.3-B, C1.3-C | C1.3-D | C1.3-C | optional |
| `f(a)` may differ from the limit or be undefined | C1.3-A, C1.3-B, C1.3-C | C1.3-D | C1.3-C | optional |
| estimating limits from graphs / tables | C1.3-D | C1.3-D, C1.3-E | C1.3-A, C1.3-B | optional |
| simple finite limits from nearby values | C1.3-D | C1.3-E, C1.3-F | C1.3-F | optional |

Notes:

- Good pilot target: 6-8 exercises. This section is conceptual; do not overfill with algebra that
  belongs to Section 1.5.

## Section 1.4 - One-Sided and Infinite Limits

| Taught item | conceptual | computational | reasoning | applied |
|---|---|---|---|---|
| left-hand and right-hand limits | C1.4-A | C1.4-C | C1.4-A, C1.4-C | optional |
| two-sided limit criterion | C1.4-A | C1.4-C | C1.4-A, C1.4-C | optional |
| infinite limits and DNE vs `±infty` notation | C1.4-B | C1.4-B, C1.4-D | C1.4-D | optional |
| vertical asymptotes | C1.4-E | C1.4-F | C1.4-E, C1.4-F | optional |
| sign analysis near denominator zero | C1.4-D | C1.4-D, C1.4-F | C1.4-D | optional |

Notes:

- Good pilot target: 8-10 exercises. Avoid horizontal-asymptote-at-infinity tasks unless they are
  clearly marked as outside this section.

## Section 1.5 - Limit Laws and Computational Techniques

| Taught item | conceptual | computational | reasoning | applied |
|---|---|---|---|---|
| limit laws | C1.5-A, C1.5-G | C1.5-B, C1.5-G | C1.5-G | C1.5-H |
| direct substitution | C1.5-B | C1.5-B | C1.5-G | optional |
| factoring and cancellation | C1.5-C | C1.5-C | C1.5-C | optional |
| rationalising radicals | optional | C1.5-D | C1.5-D | optional |
| piecewise / absolute-value limits | C1.5-E | C1.5-E | C1.5-E | optional |
| squeeze theorem | C1.5-F | C1.5-F | C1.5-F | optional |
| choosing the right technique | C1.5-G | C1.5-B to C1.5-F | C1.5-G | C1.5-H |

Notes:

- This is the computationally heaviest section. Good pilot target: 12-15 exercises, with a mixed
  final cluster so students practise method selection.

## Section 1.6 - The Precise Definition of a Limit

| Taught item | conceptual | computational | reasoning | applied |
|---|---|---|---|---|
| order and logic of the epsilon-delta definition | C1.6-A, C1.6-B | optional | C1.6-A | optional |
| choosing `delta` for constant / linear functions | C1.6-B | C1.6-C | C1.6-C | optional |
| choosing `delta` with a bounded auxiliary factor | C1.6-D | C1.6-D | C1.6-D | optional |
| using known inequalities in an epsilon-delta proof | C1.6-E | C1.6-E | C1.6-E | optional |
| uniqueness of limits | optional | n/a | open | n/a |
| precise infinite-limit definition | optional | open | open | optional |
| continuity preview | C1.6-F | optional | C1.6-F | optional |

Notes:

- Good pilot target: 6-8 exercises. The uniqueness proof and precise infinite-limit definition are
  real taught items, but bank coverage is thin. Decide during review whether they need custom
  questions or can remain theorem/prose-only at this chapter level.

## Candidate bank

### Section 1.1 candidates

| ID | Source | Short review summary | Suggested use |
|---|---|---|---|
| C1.1-A | `[source: APEX §2.7 ex 1]` `problem_banks/APEXCalculusV5/exercises/02_07_ex_01.tex` | True/false: every function has an inverse. | Opening conceptual check. |
| C1.1-B | `[source: APEX §2.7 ex 2]` `02_07_ex_02.tex` | Explain in words what one-to-one means. | Definition check. |
| C1.1-C | `[source: Mooculus Inverses of Functions L269]` | Choose which real-world mappings are one-to-one. | Conceptual/applied warm-up. |
| C1.1-D | `[source: Mooculus Inverses of Functions L294]` | Select which listed formulas are one-to-one. | Computational + reasoning. |
| C1.1-E | `[source: Mooculus Inverses of Functions L377]` | From a graph, choose intervals on which `f` is one-to-one. | Horizontal-line-test / restriction. |
| C1.1-F | `[source: Mooculus Inverses of Functions L80, L494]` | Point on graph of `f` gives point/value for `f^{-1}`; restricted graph inverse. | Graph reflection and inverse values. |
| C1.1-G | `[source: APEX §2.7 ex 5-8]` `02_07_ex_05.tex` to `02_07_ex_08.tex` | Verify proposed inverse pairs by composing both directions. | Algebraic inverse check. |
| C1.1-H | `[source: Mooculus Inverses of Functions L186]` | Celsius-to-Fahrenheit function and its inverse. | Applied inverse function. |
| C1.1-I | `[source: Mooculus Inverses of Functions L416-L536]` | Restrict `x^2`, compare with `x^3`, and reflect across `y=x`. | Domain restriction and graphing inverse. |
| C1.1-J | `[source: APEX §2.7 ex 6]` `02_07_ex_06.tex` | Quadratic on restricted domain paired with square-root inverse. | Algebraic check with domain restriction. |

### Section 1.2 candidates

| ID | Source | Short review summary | Suggested use |
|---|---|---|---|
| C1.2-A | `[source: Mooculus Inverses of Functions L103]` | Distinguish inverse sine notation from reciprocal notation. | Notation trap. |
| C1.2-B | `[source: CLP-1 §2.12 #1]` `prob_s2.12.tex:15` | Domains of `arcsin(cos x)`, `arccsc(cos x)`, `sin(arccos x)`. | Domain/range of inverse trig functions. |
| C1.2-C | `[source: CLP-1 §2.12 #2]` `prob_s2.12.tex:38` | `arccos(1)` gives a principal value that need not solve an applied time question. | Principal-range reasoning. |
| C1.2-D | `[source: Mooculus derivativesOfInverseFunctions 10_06_ex_131-154]` | Exact values such as `cos(arctan sqrt(7))`, `tan(arcsin(...))`, `sec(arctan 10)`. | Select a short exact-value set. |
| C1.2-E | `[source: CLP-1 §2.12 #5]` `prob_s2.12.tex:156` | Domain of `arcsin x + arccsc x`; omit differentiability part for this chapter. | Remaining inverse trig domains. |
| C1.2-F | `[source: CLP-1 §2.12 #16-17]` `prob_s2.12.tex:375,435` | Triangle simplification inside derivative prompts; adapt only the simplification part. | Triangle method, if accepted. |

### Section 1.3 candidates

| ID | Source | Short review summary | Suggested use |
|---|---|---|---|
| C1.3-A | `[source: CLP-1 §1.3 #4]` `prob_s1.3.tex:119` | Draw a curve with `lim_{x->3} f(x)=f(3)=10`. | Limit vs value at point. |
| C1.3-B | `[source: CLP-1 §1.3 #5]` `prob_s1.3.tex:147` | Draw a curve with `lim_{x->3} f(x)=10` and `f(3)=0`. | Removable point mismatch. |
| C1.3-C | `[source: CLP-1 §1.3 #6-7]` `prob_s1.3.tex:184,195` | True/false: limit determines value, value determines limit. | Conceptual reasoning. |
| C1.3-D | `[source: CLP-1 §1.3 #1-3]` `prob_s1.3.tex:12,45,71` | Read values and limits from graphs. | Graph/table style limit practice. |
| C1.3-E | `[source: CLP-1 §1.3 #10,#12,#16]` `prob_s1.3.tex:244,264,311` | Simple finite limits, including constant and polynomial examples. | Light computation. |
| C1.3-F | `[source: CLP-1 §1.3 #17]` `prob_s1.3.tex:325` | Limit of a piecewise-defined function near the joining point. | Transition toward one-sided limits. |

### Section 1.4 candidates

| ID | Source | Short review summary | Suggested use |
|---|---|---|---|
| C1.4-A | `[source: CLP-1 §1.3 #8-9]` `prob_s1.3.tex:209,222` | Relationship between two-sided and one-sided limits. | Criterion check. |
| C1.4-B | `[source: CLP-1 §1.3 #11,#13-15]` `prob_s1.3.tex:254,275,285,299` | Basic `log x`, `1/x`, `1/x^2` infinite/DNE behavior. | Infinite-limit notation. |
| C1.4-C | `[source: CLP-1 §1.4 #39]` `prob_s1.4.tex:778` | Evaluate `lim_{x->0}(3+|x|/x)`. | One-sided disagreement. |
| C1.4-D | `[source: CLP-1 §1.4 #29,#31]` `prob_s1.4.tex:572,609` | Rational limits with denominator tending to zero; sign-sensitive `±infty`/DNE. | Sign analysis near asymptotes. |
| C1.4-E | `[source: CLP-1 §3.6.1 #1]` `prob_s3.6.1.tex:11` | True/false: denominator zero factor does not automatically force a vertical asymptote. | Conceptual vertical-asymptote caution. |
| C1.4-F | `[source: CLP-1 §3.6.1 #4]` `prob_s3.6.1.tex:155` | Find asymptotes of a rational function; adapt to vertical asymptote only. | Vertical-asymptote computation. |

### Section 1.5 candidates

| ID | Source | Short review summary | Suggested use |
|---|---|---|---|
| C1.5-A | `[source: CLP-1 §1.4 #1]` `prob_s1.4.tex:11` | Use given limits of `f` and `g` to evaluate combined limits. | Limit laws conceptual/computational. |
| C1.5-B | `[source: CLP-1 §1.4 #6-8,#19]` `prob_s1.4.tex:90,103,114,297` | Direct substitution for rational/product/power/polynomial limits. | Early computational cluster. |
| C1.5-C | `[source: CLP-1 §1.4 #15-18,#28,#36]` `prob_s1.4.tex:225,240,259,279,547,717` | Factor and cancel `0/0` forms. | Algebraic simplification. |
| C1.5-D | `[source: CLP-1 §1.4 #20-24]` `prob_s1.4.tex:310,339,367,396,424` | Rationalise radical expressions. | Radical limits. |
| C1.5-E | `[source: CLP-1 §1.4 #39-41]` `prob_s1.4.tex:778,825,866` | Absolute-value limits with one-sided behavior. | Piecewise/absolute-value cluster. |
| C1.5-F | `[source: CLP-1 §1.4 #25,#27,#34]` `prob_s1.4.tex:450,492,666` | Bound oscillating trig factors by squeeze-style estimates. | Squeeze theorem. |
| C1.5-G | `[source: CLP-1 §1.4 #42-43]` `prob_s1.4.tex:884,898` | Evaluate an expression from a known limit; choose a constant to make a limit hold. | Method selection and reasoning. |
| C1.5-H | `[source: CLP-1 §1.4 #47]` `prob_s1.4.tex:1198` | Velocity scaling application using a limit expression. | Applied limit law, optional. |
| C1.5-I | `[source: CLP-1 §1.4 #45]` `prob_s1.4.tex:957` | Sketch `1/f(x)` from the graph of `f`. | Graph reasoning, optional. |

### Section 1.6 candidates

| ID | Source | Short review summary | Suggested use |
|---|---|---|---|
| C1.6-A | `[source: APEX §1.2 ex 1]` `01_02_ex_01.tex` | Identify what is wrong with a reversed/incorrect limit definition. | Logic of epsilon-delta. |
| C1.6-B | `[source: APEX §1.2 ex 2]` `01_02_ex_02.tex` | Which tolerance is given first, `x` or `y`? | Definition order. |
| C1.6-C | `[source: APEX §1.2 ex 3,4,12]` `01_02_ex_03.tex`, `01_02_ex_04.tex`, `01_02_ex_12.tex` | Constant and linear epsilon-delta proofs. | First proof cluster. |
| C1.6-D | `[source: APEX §1.2 ex 5,11,13]` `01_02_ex_05.tex`, `01_02_ex_11.tex`, `01_02_ex_13.tex` | Quadratic epsilon-delta proofs requiring a local bound. | Main proof cluster. |
| C1.6-E | `[source: APEX §1.2 ex 8]` `01_02_ex_08.tex` | Prove `lim_{x->0} sin x=0` using `|sin x| <= |x|`. | Inequality-based proof. |
| C1.6-F | `[source: CLP-1 §1.6 #7-9]` `prob_s1.6.tex:110,125,141` | Continuity at a point vs existence/value of the limit. | Optional continuity preview. |

## Current gaps for human review

1. Section 1.6 uniqueness of limits has no clean bank exercise in the connected sources. If this
   theorem should be practised, write a custom reasoning exercise after review.
2. Section 1.6 precise infinite-limit definition has examples in text sources but no compact
   exercise with official answer. Decide whether the informal infinite-limit exercises in Section
   1.4 are enough, or whether to add a custom threshold-style exercise.
3. Section 1.2 triangle simplification candidates C1.2-F originate inside derivative prompts. They
   are mathematically useful before derivatives, but require adaptation; reject them if that feels
   too far from source.
4. Section 1.3 applied coverage is intentionally light. The section motivates limits with velocity,
   but real velocity-limit practice fits better after derivatives.
5. Ch 1 build ownership is unresolved: either make `gen_standalone.py` generate Ch 1 from
   `example-ch01/`, or accept hand-editing `chapter1-standalone.html` and
   `chapter1-print-standalone.html` after fragment edits.

## Proposed next review pass

> **2026-06-12 update (framing corrected):** the pilot's target changed — bank problems
> supplement **in-body worked examples**, not end-of-section exercises (the handout ships no
> exercise blocks; exercises move to a future separate workbook, per user decision recorded in
> `CONTENT_EXERCISES.md`). This matrix's taught-item rows remain valid; its exercise-specific
> assumptions (no-exercise baseline, env-exercise insertion model, per-section exercise targets)
> are superseded. Live documents: [`ch01_candidate-review.md`](ch01_candidate-review.md) =
> full-text source pantry (C-ID index; three matrix errata recorded there), and
> [`ch01_example-supplement-review.md`](ch01_example-supplement-review.md) = the decision
> document (existing-example inventory, gaps, proposed insertions).

For each section, choose one of:

- `accept shortlist`: select candidate IDs to adapt into the first exercise block.
- `thin out`: keep fewer candidates and leave the section mostly conceptual.
- `custom gap-fill`: authorize hand-authored/AI-authored exercises for the `open` cells only.

After acceptance, the import pass should:

1. write real `Exercises` blocks with `env-exercise` into
   `experiments/handout_kit/example-ch01/sec-*.html`;
2. create `experiments/handout_kit/ch01_exercise-imports.md` with official hints/answers/solutions
   for accepted bank items;
3. preserve per-exercise provenance comments such as `[source: CLP-1 §1.4 #25]`;
4. adapt notation to house style (`\arcsin`, `\arccos`, `\arctan`, `\arcsec`) and Stewart register;
5. decide the Ch 1 standalone regeneration path before editing standalone output.

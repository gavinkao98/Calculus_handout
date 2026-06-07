# Content Roadmap

This file carries the **course arc** of the handout: which chapters exist, in what order, what each chapter is responsible for, and how concepts thread across chapters. It is the curricular companion to [`CONTENT_SPEC.md`](CONTENT_SPEC.md) (which governs *how* to write) and [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md) (daily author rules).

When you begin a new chapter, update the entry below **before** drafting. When you close a chapter, mark it done and revisit downstream prereq statements.

The book is assembled from **manuscripts written by different teachers**. Each chapter entry records its manuscript source under the **Manuscript source** field so the drafting origin and conversion status are visible at a glance. The manuscript-to-LaTeX workflow and the anti-hallucination rule that governs Claude's expansion of manuscripts both live in [`README.md`](README.md) §*Authoring workflow*; this file is where per-chapter manuscript tracking lands.

---

## Audience and positioning

Repeated from [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §1 so authors of any chapter can calibrate quickly:

- motivated high-school student preparing for or self-studying college calculus.
- has strong precalculus; some exposure to mathematical reasoning; not yet an undergraduate-math-major.
- reads the handout as the primary channel. **The handout is self-sufficient**; the companion video is reinforcement, not prerequisite.

Two cross-cutting targets sit above any chapter-specific content:

- **self-sufficiency** — a student who never watches the video can still learn from the handout alone.
- **lookup-friendliness** — a student who forgets a definition in Chapter 5 can find it again via the index, the chapter opening, or the summary.

---

## Chapter list

> **Status legend**: `draft` = actively being written. `skeleton` = structure planned but content not drafted. `planned` = on the roadmap, not yet started. `done` = meets the §15 consistency checklist.

| # | Title | Status | Sections |
|---|---|---|---|
| 1 | Inverse Functions and Limits | draft | 1.1 Inverse Functions and One-to-One Functions; 1.2 Inverse Trigonometric Functions; 1.3 Limits; 1.4 One-Sided and Infinite Limits; 1.5 Limit Laws; 1.6 The Precise Definition of a Limit |
| 2 | Derivatives | draft | 2.1 The Tangent Line and the Derivative at a Point; 2.2 The Derivative as a Function; 2.3 Differentiability, Continuity, and Higher Derivatives; 2.4 Derivatives of Polynomials and the Exponential Function; 2.5 The Product and Quotient Rules |
| 3 | Chain Rule and Trigonometric Derivatives | draft | 3.1 Derivatives of the Sine and Cosine Functions; 3.2 The Chain Rule; 3.3 Applications of the Chain Rule |
| 4 | The Exponential and Logarithmic Functions | draft | 4.1 Construction of the Exponential Function; 4.2 Continuity and the Exponent Law for $e^x$; 4.3 The Derivative of $e^x$; 4.4 Rolle's Theorem and the Mean Value Theorem; 4.5 Monotonicity and the Logarithmic Function |
| 5-14 | *(TBD — titles added as each chapter is drafted)* | planned | — |

Target scope: Calc I + II + III (single-variable through multivariable vector calculus). Loose Stewart / Rogawski TOC as the reference arc. The natural full arc at this scope runs roughly 14 chapters:

- **Calc I** (Ch 1-4): Inverse Functions and Limits → Derivatives → Applications of Differentiation → Integrals.
- **Calc II** (Ch 5-9): Applications of Integration → Techniques of Integration → Differential Equations → Parametric and Polar Coordinates → Infinite Sequences and Series.
- **Calc III** (Ch 10-14): Vectors and the Geometry of Space → Vector Functions → Partial Derivatives → Multiple Integrals → Vector Calculus.

Titles for Ch 3 onward are **not committed** until the preceding chapter's draft stabilises. The per-workflow decision is explicit: we fill a chapter's full roadmap entry (role, prereqs, core skills, key figures, notation, cautions, open questions) at the moment its immediate predecessor reaches the `draft` status bar — not earlier, since upstream decisions in the predecessor chapter shift what the successor needs to teach.

---

## Per-chapter entry template

Copy this block into the chapter list area when beginning a new chapter.

```
### Chapter N: Title

**Status**: draft | skeleton | planned | done
**Source file**: chapters/chNN_<slug>.tex
**Estimated length**: N pages printed (12 pt, 3.3 cm margins)
**Manuscript source**: <teacher name | "pre-manuscript working hypothesis" | "pre-existing LaTeX — entry reverse-engineered">
 — <pending | received YYYY-MM-DD | converted YYYY-MM-DD>. <optional note on coverage, gaps, or register hints from the teacher>.

**Role in the arc**
- One paragraph on what this chapter does for the reader.
- Why it sits at position N and not earlier/later.

**Prerequisites**
- Chapters this chapter relies on (by section).
- Precalculus facts the reader is expected to bring.
- Notation or environments introduced earlier that this chapter reuses.

**Core skills**
Each item MUST match a bullet in the chapter's "By the end of this chapter, you will be able to:" list.
- skill 1
- skill 2
- skill 3-5

**Key figures**
- figure that every section-opening motivation depends on (one bullet each).

**Handout self-sufficiency vs. video reinforcement**
- What the handout teaches alone.
- What the video adds on top (intuition visualisations, alternative worked examples, pacing).
  The video never carries a fact that the handout does not also state.

**Strategy boxes expected**
- Problem-type → strategy name. E.g. "computing a limit → §1.5 Limit-computation strategy."

**Notation introduced**
- New symbols, macros, or notational conventions. Each one needs an `\index{...}` at first use.

**Common pitfalls (caution boxes)**
- Notation traps.
- Branch-choice or domain-restriction pitfalls.
- Identities that only hold on a subdomain.

**Open questions**
- Decisions not yet made. Flag here and close before declaring the chapter `done`.
```

---

## Chapter 1 (filled exemplar)

### Chapter 1: Inverse Functions and Limits

**Status**: draft
**Source file**: [`chapters/ch01_foundations.tex`](chapters/ch01_foundations.tex) — the filename slug `foundations` is the arc-level tag (Chapter 1 is the *foundations* phase of the arc), not part of the printed chapter title.
**Estimated length**: *(fill in after first full compile)*
**Manuscript source**: pre-existing LaTeX — entry reverse-engineered from the already-committed `chapters/ch01_foundations.tex`. Treat the LaTeX source as canonical; this entry is a description of existing content, not a plan for future drafting. When Chapter 1 receives further edits, update both the LaTeX and this entry together.

**Role in the arc**
Chapter 1 is the **foundations** phase of the course arc. It sets up the two foundational machines of calculus: inverse functions (the algebraic machine for "running a rule backward") and limits (the analytic machine for "approaching without equalling"). The chapter intentionally pairs these because both force the reader to reason about correspondences and approximations rather than about formulas in isolation.

**Prerequisites**
- Precalculus functions: domain, range, composition, graphs.
- Trigonometric functions and their graphs on standard intervals.
- Basic algebra manipulations (factoring, rationalising, completing the square).

**Core skills** (matches the chapter opening bullet list)
- determine whether a function is one-to-one, and find its inverse when it is;
- work with inverse trigonometric functions, their principal-interval restrictions, and the identities that follow;
- compute limits of the forms encountered in Ch. 1 and 2 using substitution, factoring, rationalising, and one-sided analysis;
- decide when a limit fails to exist;
- state and, where required, verify a limit using the $\varepsilon$–$\delta$ definition.

**Key figures**
- inverse-composition diagram (§1.1).
- reflection across $y = x$ for invertible graphs (§1.1).
- restricted-domain trig graphs with principal intervals shaded (§1.2).
- one-sided-limit disagreement example (§1.4).
- $\varepsilon$–$\delta$ tube-and-interval diagram (§1.6).

**Handout self-sufficiency vs. video reinforcement**
- The handout alone carries every definition, every theorem statement, every worked example, and every strategy box.
- The companion videos (one per section, currently exemplified by §1.1) add animated reflection-across-$y=x$ demonstrations, animated $\varepsilon$–$\delta$ tubes that the printed page cannot convey, and a slower verbal walkthrough of notation traps.
- Nothing in the video substitutes for reading the handout — video scenes are marked as reinforcement in [`legacy/MANIM_STORYBOARD.md`](legacy/MANIM_STORYBOARD.md).

**Strategy boxes present**
- finding an inverse function (§1.1).
- computing a limit (§1.5).
- verifying an $\varepsilon$–$\delta$ limit (§1.6).

**Notation introduced**
- `\arcsin`, `\arccos`, `\arctan`, `\arccsc`, `\arcsec`, `\arccot` (house inverse-trig operators).
- `\lim_{x \to a} f(x)`, `\lim_{x \to a^-} f(x)`, `\lim_{x \to a^+} f(x)`, `\lim_{x \to \infty} f(x)`.
- $\varepsilon$, $\delta$.

**Common pitfalls (caution boxes present)**
- $\sin^{-1} x$ denotes the inverse sine, not $1/\sin x$.
- $\arcsin(\sin x) = x$ holds only on the principal interval $[-\pi/2, \pi/2]$.

**Open questions**
- End-of-section exercises are still `% TODO` placeholders in all six sections. See [`CONTENT_EXERCISES.md`](CONTENT_EXERCISES.md) for the minimum exercise skeleton that should land before the chapter is declared `done`.

---

## Chapter 2 (filled entry)

### Chapter 2: Derivatives

**Status**: draft — LaTeX `chapters/ch02_derivatives.tex` not yet built. Manuscript coverage is **complete in the HTML handout-kit experiment** (`experiments/handout_kit/exp-ch02/`): §2.1–§2.5 authored via the `direction_layer` six-stage flow, each Codex-audited to blocking=0 (2026-06).
**Source file**: `chapters/ch02_derivatives.tex`
**Estimated length**: *(fill in after first full compile)*
**Manuscript source**: received 2026-04-27 (13-page handwritten manuscript by the chapter author). The manuscript covers the foundational portion of the differentiation chapter: tangent-line motivation, the derivative at a point, the derivative as a function, differentiability vs continuity, higher derivatives, derivatives of constants / power functions / the exponential, and the product / quotient rules. It does **not** include the trigonometric, chain-rule, implicit, inverse-function, or logarithmic-derivative material that the pre-manuscript working hypothesis listed as §2.4–§2.8. Whether those topics will arrive as a follow-up manuscript (extending Ch 2) or shift to a later chapter is an Open question below.

**Role in the arc**
Chapter 2 is the **development** phase of Calc I. It converts the limit machinery from Chapter 1 into a working operator: given a function, produce another function describing its instantaneous rate of change. Ch 1 did the heavy conceptual lifting (what does it mean to approach without equalling?); Ch 2 cashes that in algorithmically. As scoped by the current manuscript, Ch 2 covers the definition of the derivative and the rules needed to differentiate polynomials, the natural exponential, and any product or quotient of differentiable functions. Trigonometric, chain-rule, implicit, inverse, and logarithmic differentiation are deferred (see Open questions).

**Prerequisites**
- **From Chapter 1**: all six sections, especially §1.3 (limits), §1.4 (one-sided and infinite limits), and §1.5 (limit laws). The derivative is defined as a limit; students who are shaky on limit manipulation will not survive the definition in §2.1. §1.6 (ε-δ) is not strictly prerequisite — the derivative is phrased through the algebraic limit, not the ε-δ form — but a student who has seen §1.6 will find §2.1's rigour less jarring.
- **Precalculus**: polynomial and rational manipulation; the binomial theorem (used in the §2.4 power-rule proof).
- **No prior exposure to derivatives needed** — the chapter assumes the derivative is new.

**Core skills** (will match the chapter opening bullet list)
- state the limit definition of the derivative $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$ and apply it to compute derivatives from first principles for polynomial and root functions;
- use the power, constant-multiple, sum, product, and quotient rules to differentiate algebraic and exponential combinations;
- differentiate the natural exponential function $e^x$ using its series definition;
- recognise where a function fails to be differentiable (e.g.\ corners) and connect differentiability to continuity;
- compute higher-order derivatives.

**Key figures**
- secant-to-tangent limit diagram (§2.1): a curve with a sequence of secant lines converging to a tangent line as the second point approaches the first.
- derivative as a function (§2.2): a pair of graphs showing $f$ above and $f'$ below, aligned on the $x$-axis so zeros, extrema, and sign changes line up visually.
- non-differentiability at a corner (§2.3): the graph of $|x|$ near $0$, with the left and right secant slopes labelled to show the one-sided limits disagree.

**Handout self-sufficiency vs. video reinforcement**
- The handout alone carries the limit definition, every differentiation rule with a proof, every worked example, and every strategy box.
- The companion videos add: (a) animated secant-to-tangent convergence that is hard to convey on a static page; (b) a dynamic slope-of-tangent-line demo where the tangent point sweeps across a curve and the slope is plotted below in real time, showing $f'$ emerging as a function.
- Nothing in the video substitutes for reading the handout; promotion direction stays *video → handout*, never the reverse.

**Strategy boxes expected**
- *Computing a derivative from the limit definition* (§2.2): a 3-step procedure — (1) write the difference quotient $(f(x+h) - f(x))/h$; (2) simplify algebraically until $h$ cancels from the denominator; (3) take $h \to 0$.
- *Selecting among the basic rules* (§2.5): when to use power rule vs product vs quotient; the test is the syntactic shape of the expression.

**Notation introduced**
- $f'(x)$, $\dfrac{dy}{dx}$, $\dfrac{df}{dx}$, $\dfrac{d}{dx}[f(x)]$, $f''(x)$, $f^{(n)}(x)$ — the conventional derivative notations, introduced with explicit guidance on when each is most natural. Index entries at first use for each of prime notation and Leibniz notation.
- $\Delta x$, $h$ — increment notation; the manuscript uses $h$ exclusively after introducing the substitution $x = a + h$. Flag in a caution that $\Delta x$ and $h$ are synonymous in derivative contexts.

**Common pitfalls (caution boxes)**
- *Power rule domain*: $\frac{d}{dx}[x^n] = n x^{n-1}$ is proved in §2.4 for positive integer $n$; the negative-integer case is left as a manuscript exercise. A caution flags this and defers the full real-exponent statement to a later chapter.
- *Quotient rule asymmetry*: $\frac{d}{dx}\left[\frac{f}{g}\right] = \frac{f'g - fg'}{g^2}$ is not symmetric in $f$ and $g$; order of terms in the numerator matters.
- *Differentiable implies continuous, but not conversely*: the §2.3 theorem is one-directional. The function $|x|$ at $0$ is the standard counterexample; both the manuscript and the chapter make this explicit.
- *(fg)' is not f'g'*: the manuscript's opening counterexample for the product rule (`f = x`, `g = x^2`, `fg = x^3`); a caution preserves it as the headline pitfall.

**Open questions**
- ~~*Manuscript scope vs original 9-section hypothesis*~~ — **resolved 2026-04-27**: two follow-up manuscripts (`2023-10-28-chainRule` and `2023-11-4-ExponentialFunction`) cover the missing topics (trig derivatives, chain rule, ln/arcsin/x^x via chain rule, rigorous $e^x$, MVT, ln). The 4 missing topics did not extend Ch 2; they became Ch 3 (*Chain Rule and Trigonometric Derivatives*) and Ch 4 (*The Exponential and Logarithmic Functions*). Implicit differentiation is not in either manuscript and remains deferred to a later chapter.
- ~~*Treatment of $e^x$ derivative*~~ — **resolved 2026-06-08**: confirmed at §2.4 ⑥ convergence gate. The chapter follows the manuscript's series-based derivation of $(e^x)' = e^x$ (factor out $e^x$, then $(e^h-1)/h = 1 + h/2! + h^2/3! + \dots \to 1$ from the term-by-term series), kept at the manuscript's intuitive level rather than the Stewart "$\lim_{h \to 0}(e^h-1)/h = 1$ as the defining property" route. Rigorous convergence and the construction of $e^x$ are deferred to Ch 4 §4.3, which re-derives the derivative and cross-references back. Implemented in §2.4 as Theorem 2.5 + a series proof, with a one-line forward fence to Ch 4 and a Codex audit (4 runs, blocking=0).
- ~~*Higher derivatives placement*~~ — **resolved 2026-06-08**: higher derivatives ($f''$, $f'''$, $f^{(n)}$) stay as a subsection of §2.3 (following the manuscript). Confirmed at §2.3 ⑥ convergence gate; brief and HTML both implement this as a `<h3>` subsection rather than a standalone `<article class="sec">`.
- ~~*§2.5 product/quotient rules — figure choice & section completion*~~ — **resolved 2026-06-08** at the §2.5 ⑥ convergence gate (the final manuscript section, so this completes Ch 2's manuscript coverage). Implemented as Theorem 2.6 (product rule) and Theorem 2.7 (quotient rule) with the manuscript's add-and-subtract proofs — domain hypotheses made explicit ($g$ continuous via §2.3 Theorem 2.1; $g(x)\neq 0$ for the quotient) — plus Strategy 2.2 (*selecting among the basic rules*, by syntactic shape + "simplify first"), the three pitfall cautions ($(fg)'\neq f'g'$ with the manuscript counterexample, $\Delta x \equiv h$, quotient-rule asymmetry), and Examples 2.15–2.17. **Figure decision**: the user added **Figure 2.4**, a product-rule rectangle-area diagram (area increment = strips $f\,\Delta g$, $g\,\Delta f$ + second-order corner $\Delta f\,\Delta g$), overriding the brief's default "no figure for a rules section"; rendered as inline schematic SVG (no `figures.js` entry — `buildPlot` has no fill primitive). Keeping it label-light spawned a new authoritative rule, [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §10 "Label economy" (mirrored in the kit's `CONTRACT-html-writing.md` §Figures), that later chapters follow. Codex audit converged (2 runs; run 1 caught one real notation conflict in an added $1/x$ inline check, fixed → run 2 blocking=0).

---

## Chapter 3 (filled entry)

### Chapter 3: Chain Rule and Trigonometric Derivatives

**Status**: draft
**Source file**: `chapters/ch03_chain_rule.tex`
**Estimated length**: *(fill in after first full compile)*
**Manuscript source**: `2023-10-28-chainRule` (handwritten manuscript dated 2023-10-28, received 2026-04-27). The manuscript covers (i) derivatives of $\sin x$ and $\cos x$ via the squeezing lemma + sector geometry, (ii) the chain rule with a proof using the remainder-form definition of differentiability ($f(x_0 + h) = f(x_0) + mh + R(h)$ with $R(h)/h \to 0$), and (iii) chain-rule applications including $d/dx \ln x$, $d/dx x^x$, and $d/dx \arcsin y$. The manuscript also re-states the product rule and the differentiable-implies-continuous lemma; both are treated as cross-references back to Ch 2 rather than re-derived in Ch 3.

**Role in the arc**
Chapter 3 is the **rules continuation** of Calc I. Chapter 2 built the limit definition of the derivative and the basic algebraic rules (constant, power, sum, product, quotient, $e^x$); Chapter 3 adds the rule for compositions (chain rule) and applies it to introduce the trigonometric derivatives and to extract the derivatives of inverse and implicitly-defined functions. Together with Ch 4's rigorous treatment of $e^x$ and $\ln x$, Ch 3 closes out the differentiation toolkit.

**Prerequisites**
- **From Chapter 1**: §1.5 (the squeeze theorem in particular — used directly for $\lim_{\theta \to 0} \sin \theta / \theta = 1$). §1.2 (inverse trig — $\arcsin$ is one of the chain-rule example targets).
- **From Chapter 2**: all five sections, especially §2.5 product rule (the chain-rule manuscript re-derives this; we cross-ref instead) and §2.3 differentiable $\Rightarrow$ continuous (used inside the chain-rule proof and the trigonometric continuity proofs).
- **Trigonometric identities**: the sum-to-product identity $\sin(x + h) - \sin(x) = 2 \sin(h/2) \cos(x + h/2)$ is the chapter's main algebraic device. Pythagorean identity $1 + \tan^2 = \sec^2$ also appears in worked examples.

**Core skills**
- compute $d/dx \sin x$, $d/dx \cos x$, $d/dx \tan x$, and (via chain rule) $d/dx \sin(g(x))$, $d/dx \cos(g(x))$, etc.;
- apply the chain rule to differentiate compositions of two or more functions, including $f(g(h(x)))$-type nestings;
- use the chain rule + log differentiation to differentiate $x^x$, $f(x)^{g(x)}$, and similar non-standard exponential expressions;
- derive $d/dx \arcsin x$, $d/dx \arctan x$, and $d/dx \ln x$ from the inverse-function relations $\sin(\arcsin y) = y$, etc., applied chain rule.

**Key figures**
- secant inequality figure (§3.1): unit circle with sector $OAB$ and triangles $\triangle OAB$, $\triangle ABC$ to ground the bound $\cos \theta \le \sin \theta / \theta \le 1$.
- chain rule as composed mapping (§3.2): stacked input–intermediate–output axes showing how a small $h$ at the input propagates to a change at the output, scaled by the product of the intermediate slopes.

**Strategy boxes expected**
- *Chain-rule decomposition* (§3.2): given a complicated expression, identify the outermost operation; write the expression as $f(g(x))$; differentiate as $f'(g(x)) \cdot g'(x)$. Iterate for nested compositions.
- *Logarithmic differentiation* (§3.3): when an expression has the form $f(x)^{g(x)}$ or a product/quotient with many factors, take $\ln$ of both sides, apply chain rule and product rule, then solve for $y'$.

**Notation introduced**
- The remainder-form definition of differentiability $f(x_0 + h) = f(x_0) + m h + R(h)$ with $R(h)/h \to 0$. This is Def 2 in the manuscript; equivalent to the standard limit definition but more convenient for the chain-rule proof.
- $\arcsin'$, $\arccos'$, $\arctan'$ are introduced in §3.3 via the chain-rule technique on $\sin(\arcsin y) = y$ etc.

**Common pitfalls (caution boxes)**
- *Chain rule is one identity, not two fractions*: $\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$ is the chain rule, not the cancellation $du / du = 1$. The Leibniz form's apparent fraction-cancellation is a useful mnemonic but not the proof.
- *Forgetting the inner derivative*: the most common chain-rule error is $\frac{d}{dx}[\sin(g(x))] = \cos(g(x))$ instead of $\cos(g(x)) \cdot g'(x)$. A worked example flags this.
- *Domain issues for $\arcsin$ derivative*: the formula $1/\sqrt{1 - y^2}$ is valid only for $y \in (-1, 1)$ (open interval — the endpoints have vertical tangents). A caution flags this.
- *$\ln$ used informally before rigorous construction*: §3.3 treats $\ln$ as "the inverse of $e^x$" and uses the relation $e^{\ln x} = x$ to extract $d/dx \ln x = 1/x$. The rigorous construction is deferred to Ch 4. A note flags this dependence.

**Open questions**
- *Trig derivatives placement vs squeeze-theorem location*: $\lim_{\theta \to 0} \sin \theta / \theta = 1$ is the central limit of §3.1 and uses the squeeze theorem from §1.5. The chain-rule manuscript actually restates the squeeze theorem at the start (with two formulations: $x \to \infty$ and $x \to x_0$). The Ch 3 draft will cross-reference the §1.5 statement and only restate the additional formulation if needed; sign-off: confirm this rather than duplicating the squeeze statement.
- *Two equivalent definitions of differentiability*: Def 2 (remainder form) is introduced in §3.2 because the chain-rule proof uses it. Def 1 was established in §2.2. The draft proves equivalence in §3.2 and then uses Def 2 only for the chain-rule proof; sign-off: confirm this is the right place to introduce Def 2.
- *Implicit differentiation*: the chain-rule manuscript's $\arcsin$ and $x^x$ examples are essentially implicit-differentiation arguments dressed up as chain rule on composition identities. A future chapter on implicit differentiation could revisit these as canonical motivating examples, or stay separate. Decision deferred until that chapter is drafted.

---

## Chapter 4 (filled entry)

### Chapter 4: The Exponential and Logarithmic Functions

**Status**: draft
**Source file**: `chapters/ch04_exponential_logarithm.tex`
**Estimated length**: *(fill in after first full compile)*
**Manuscript source**: `2023-11-4-ExponentialFunction` (handwritten manuscript dated 2023-11-04, received 2026-04-27). The manuscript covers (i) the rigorous construction of $e^x$ via the power series $\sum x^n / n!$, with completeness of $\mathbb{R}$ used to prove convergence; (ii) continuity of $e^x$ and the exponent law $e^x e^y = e^{x+y}$ via a careful series-multiplication argument and Cauchy convergence; (iii) the derivative $d/dx \, e^x = e^x$ (a more rigorous re-derivation than the one given in Ch 2 §2.4, with an explicit bound on $(e^h - 1)/h - 1$); (iv) Rolle's theorem and the Mean Value Theorem; (v) the corollary $f' \ge 0 \Rightarrow f$ increasing; (vi) the logarithm $\ln x$ as the inverse of $e^x$, its continuity, and $d/dx \ln x = 1/x$ via the inverse-function technique.

**Role in the arc**
Chapter 4 closes out the rigour foundation for Calc I's differentiation chapters. Ch 2 introduced $e^x$ informally and proved $(e^x)' = e^x$ from a casual term-by-term argument; Ch 4 builds $e^x$ from scratch as a power series, proves the convergence and continuity that Ch 2 took for granted, and re-derives the derivative with full rigour. The chapter then introduces the Mean Value Theorem --- the central existence theorem that drives the derivative-to-monotonicity argument needed to construct $\ln x$ as the inverse of the strictly increasing $e^x$. Chapter 5 onward (applications of differentiation: extrema, optimisation, related rates, L'Hôpital) will reuse the MVT machinery introduced here.

**Prerequisites**
- **From Chapter 1**: §1.5 (limit laws and basic continuity arguments), §1.6 (precise $\varepsilon$-$\delta$ definition --- §4.2's continuity proof for $e^x$ is essentially $\varepsilon$-$\delta$ in spirit and will be familiar to students who saw §1.6).
- **From Chapter 2**: §2.4 (the informal $(e^x)' = e^x$ derivation; §4.3 re-does this rigorously and cross-references back), §2.3 (differentiable $\Rightarrow$ continuous, used in MVT setup).
- **From Chapter 3**: §3.3 used $\ln x$ informally with a forward reference to this chapter for the rigorous construction; §4.5 closes that loop.
- **Real analysis prerequisites**: completeness of the reals (monotone bounded sequences converge); Bolzano--Weierstrass (proved in §4.2 from completeness via the monotone-subsequence lemma); the binomial theorem (already used in Ch 2 §2.4 for the power-rule proof). Cauchy sequences and the equivalence convergent $\Leftrightarrow$ Cauchy are introduced and **proved** in §4.2.

**Core skills**
- state the power-series definition of $e^x$ and bound its tail to establish convergence on $\mathbb{R}$;
- prove that $e^x$ is continuous on $\mathbb{R}$ and satisfies $e^x e^y = e^{x+y}$ via a series-multiplication argument;
- compute $d/dx \, e^x = e^x$ rigorously using the bound $\lvert (e^h - 1)/h - 1 \rvert \le \lvert h \rvert$ on a small interval;
- state and prove Rolle's theorem and the Mean Value Theorem;
- use the MVT to prove that $f' \ge 0$ on $(a, b)$ implies $f$ is increasing on $[a, b]$;
- define $\ln x$ as the inverse of $e^x$, prove its continuity, and derive $d/dx \ln x = 1/x$.

**Key figures**
- partial-sum convergence figure (§4.1): plot of $\sum_{n=0}^{k} x^n / n!$ for $k = 1, 2, 3, 4$ on $[-2, 2]$, showing convergence to the smooth $e^x$ curve.
- secant–tangent figure for the MVT (§4.4): a curve with a secant from $(a, f(a))$ to $(b, f(b))$ drawn dashed, and a parallel tangent at the interior point $c$ drawn solid.
- $e^x$ and $\ln x$ as reflections (§4.5): reuse Ch 1's reflection-across-$y = x$ setup with $e^x$ in blue and $\ln x$ in red.

**Strategy boxes expected**
- *Tail-bound argument* (§4.1, §4.2): bound $\sum_{n = n_0 + 1}^{\infty} x^n/n!$ by a geometric series when $n_0 > 2x$. The same template is reused several times in the chapter and is worth distilling.
- *Verifying the MVT hypotheses before applying* (§4.4): check continuity on $[a, b]$ and differentiability on $(a, b)$ separately. A common error is to apply MVT on a closed interval where the function is not actually differentiable at an endpoint.

**Notation introduced**
- $e^x$ as a power-series definition (the manuscript's choice). Index entry $\ln x$ at first use in §4.5; index entry $e$ (the constant) and $e^x$ (the function) at first use in §4.1.
- $C_k^n$ for binomial coefficients (the manuscript's notation). The book uses $\binom{n}{k}$ throughout; cross-reference both notations when the manuscript's appears.
- $P_k(x) = \sum_{n=0}^{k} x^n / n!$ for the partial sum (manuscript's notation, kept in §4.1–§4.2).

**Common pitfalls (caution boxes)**
- *Series defines, doesn't derive*: the series $e^x = \sum x^n / n!$ is the **definition** of $e^x$ in this chapter. The familiar exponent law, continuity, and derivative are then theorems to prove. Students who saw $e^x$ informally in Ch 2 may try to use familiar properties before they have been re-established; flag this.
- *Bolzano--Weierstrass dependency*: the proof of convergent $\Leftrightarrow$ Cauchy in §4.2 routes through Bolzano--Weierstrass (proved from completeness via the monotone-subsequence peak argument). Caution flag in the chapter notes the dependency chain so that students see Cauchy $\Leftrightarrow$ convergent as logically equivalent to completeness.
- *MVT continuity vs differentiability*: the function must be continuous on the **closed** interval $[a, b]$ and differentiable on the **open** interval $(a, b)$; differentiability at the endpoints is not required. A caution flags this asymmetry.
- *$\ln$ defined only for $x > 0$*: every formula involving $\ln x$ implicitly carries $x > 0$. Flag in §4.5; same convention as Ch 3 §3.3.

**Open questions**
- ~~*Cauchy / convergent equivalence proof*~~ — **resolved 2026-04-27 (user-directed)**: the proof was supplied in §4.2 via the Bolzano--Weierstrass theorem and the monotone-subsequence lemma, going beyond what the manuscript itself supplied. The chapter now proves both directions in full.
- ~~*Exponent law proof level of detail*~~ — **resolved 2026-04-27 (user-directed)**: §4.2's exponent-law proof was originally drafted as a 4-step outline; on user direction it was rewritten as the full 6-step proof matching the manuscript's level of detail (full binomial-theorem reorganisation, explicit (II)-piece tail-bound estimate, telescoped error in step 5).
- *MVT placement*: the manuscript bundles MVT inside the exponential / logarithm chapter because $\ln$'s rigorous construction needs the monotonicity corollary. When a future chapter on applications of differentiation (extrema, optimisation) is drafted, it will be natural to **propose-only** in Mode B that MVT moves to that chapter. For now, MVT lives in Ch 4.
- *§4.3 redundancy with §2.4*: Ch 2's informal derivation of $(e^x)' = e^x$ and §4.3's rigorous re-derivation differ mainly in the explicit bound on $(e^h - 1)/h - 1$. Possible refactor: replace Ch 2's casual version with a forward-reference to §4.3, eliminating the duplication. Decision deferred until both chapters are signed off.

---

## Cross-chapter notation threading

A calculus handout that students flip back through needs notation to remain stable once introduced. Record decisions here the first time they are made; later chapters cite this section rather than re-deciding.

- `\arcsin` / `\arccos` / `\arctan` are the operators in the book. `\sin^{-1}`, `\cos^{-1}`, `\tan^{-1}` appear only inside a caution box when first warning against the reciprocal misreading.
- Domain restrictions are written inline inside `conditiondisplay` when they apply to one formula; moved to a `caution` when they are easy to forget.
- Equation numbers are per-chapter (`(1.3)`, `(2.7)`) and appear only when the equation is referenced later or is a formal statement (see spec §6).

*(Extend this list as later chapters introduce new convention decisions.)*

---

## Handout–video boundary (repeating rule)

For every chapter, the author **MUST** verify:

- the handout stands alone. A student without video access can still complete the chapter.
- the video does not introduce a fact, definition, or theorem not present in the handout.
- the video is free to add visual intuition, pacing, or alternative worked examples; these are reinforcement, not prerequisites.

When in doubt, promote a fact from video into the handout, not the other way around.

---

## Reviewing the roadmap

Revisit this file after every chapter reaches `done`. Typical updates:

- close the chapter's `Open questions` block or move remaining items into a follow-up issue.
- update cross-references that reach forward from earlier chapters to this chapter.
- check whether later chapters' `Prerequisites` blocks still list the right earlier sections after any restructuring.

If the overall arc changes — e.g. two chapters should merge, or a chapter should move earlier in the book — update this file **before** editing chapter sources. The roadmap is the plan; the chapter sources are the implementation.

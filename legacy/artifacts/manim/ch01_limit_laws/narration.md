# ch01_limit_laws Final Narration

Source file: `inputs\manim_storyboards\ch01_limit_laws.yml`
Deck ID: `ch01_limit_laws`

You may edit the narration text below each **Narration:** heading.
For scenes with **Voiceover Beats**, edit the beat text/reveal map in the storyboard YAML; the joined beat text is exported here for proofreading.
Do NOT change the hidden hash comment lines either — they are used for stale-file conflict detection.
Do NOT change the Slide ID lines — they are used to match edits back to the correct scene.
After editing, run `python tools/manim_sync_narration_back.py --deck-id ch01_limit_laws` to write changes back to the storyboard YAML.

## Slide 1: Limit Laws and Computational Techniques

Slide ID: `opening_hook`
<!-- voiceover-hash: ecc5b9df9df6b7cfa7c049194404cccea68ec750f3723ec32d3433d846fcd254 -->
Scene template: `title_bullets`

Narration:

Up to now, we have guessed limits from tables and graphs. Today we get systematic. A handful of algebraic limit laws lets us combine known limits into new ones the same way we combine numbers. With those laws and a few standard maneuvers, almost every elementary limit becomes routine. We will build up the laws, then practice direct substitution, factor-and-cancel, rationalization, piecewise splitting, and the squeeze theorem.

## Slide 2: The Limit Laws

Slide ID: `limit_laws_theorem`
<!-- voiceover-hash: fb269dedf6e4f8bc1542cd5ae7c4cdeae31a583d2d9c3effbe803d203ef16b86 -->
Scene template: `definition_math`

Narration:

Suppose c is a constant and both the limit of f and the limit of g exist at a. Then the limit of a sum or difference is the sum or difference of the limits, and the limit of a constant times f is the constant times the limit of f. The limit of a product is the product of the limits, and the limit of a quotient is the quotient as long as the denominator's limit is nonzero. The limit of an integer power is the corresponding power of the limit. In short, limits commute with all the basic algebraic operations as long as everything stays defined.

## Slide 3: Polynomials Substitute Cleanly

Slide ID: `direct_substitution_proposition`
<!-- voiceover-hash: 5651479fd23cf2696cbec4c583a8de27a59759b033634cc4d3104bbdd70024db -->
Scene template: `definition_math`

Narration:

The simplest application of the laws is also the most useful. The limit of the identity function at a is just a. By the product law, the limit of x to the n at a is a to the n. Apply the sum law and the constant-multiple law: the limit of any polynomial at a is the polynomial evaluated at a. By the quotient law, the limit of any rational function at a is the rational function evaluated at a, as long as the denominator is not zero there. So for polynomials and well-behaved rationals, direct substitution gives the answer.

## Slide 4: Direct Substitution on a Rational

Slide ID: `direct_substitution_example`
<!-- voiceover-hash: 088674491a3aaad6670fc1a16731f451d3943c57e51873664c284caab3a96e1d -->
Scene template: `example_walkthrough`

Narration:

Take the rational function x cubed plus two x squared minus one over five minus three x, and find its limit as x approaches one. Numerator and denominator are both polynomials. The limit of the numerator at one is one plus two minus one, which is two. The limit of the denominator at one is five minus three, which is also two. The denominator's limit is not zero, so the quotient law applies. The answer is two over two, which is one.

## Slide 5: When Substitution Fails

Slide ID: `transition_to_indeterminate`
<!-- voiceover-hash: 277b2e03ce7fd5dd9be08861cd9e846464a0aec6fb5a5e0beadf3a3f84afcc12 -->
Scene template: `section_transition`

Narration:

Direct substitution sometimes lands on the indeterminate form zero over zero. That is not an answer; it is a signal that the expression hides a removable cancellation. Three standard tools handle the common cases.

## Slide 6: Factor and Cancel

Slide ID: `factor_cancel_example`
<!-- voiceover-hash: 4b320e1fcc0348bb94d421f64e79c41fab88edc0a8200197fef8ad42b929be54 -->
Scene template: `example_walkthrough`

Narration:

The limit of x minus one over x squared minus one as x approaches one. Direct substitution gives zero over zero. Factor the denominator as x minus one times x plus one. Now the numerator and denominator share a factor of x minus one. Since x is approaching one but never equal to one, x minus one is nonzero, and we may cancel. What is left is one over x plus one. The limit of one over x plus one at one is one half. So the original limit is one half, agreeing with our table-based guess from earlier.

## Slide 7: Rationalize the Numerator

Slide ID: `rationalize_example`
<!-- voiceover-hash: f63fa8d61ac3c672400f0dea5bc08daa2779fdfe76738f953da3651681a60465 -->
Scene template: `example_walkthrough`

Narration:

The limit of square root of t squared plus nine minus three over t squared, as t goes to zero. Direct substitution gives zero over zero. Multiply top and bottom by the conjugate of the numerator: square root of t squared plus nine plus three. The numerator becomes a difference of squares: t squared plus nine minus nine, which collapses to t squared. The t squared on the new numerator cancels the t squared on the denominator. We are left with one over square root of t squared plus nine plus three. Direct substitution at t equals zero gives one over three plus three, which is one sixth. Same answer as our table-based guess from earlier.

## Slide 8: Piecewise: $\lim_{x \to 0} |x|$

Slide ID: `abs_value_example`
<!-- voiceover-hash: efdd4e8f0f8852989ab8b6a0ec99df9acd6fd79be87d1f83202b69b056177dda -->
Scene template: `example_walkthrough`

Narration:

The absolute value function has the piecewise definition x for nonnegative x, and minus x for negative x. To take a limit at zero, evaluate each one-sided limit on its own branch. From the right, the active branch is x itself, and the limit is zero. From the left, the active branch is minus x, and the limit is also zero. Both one-sided limits equal zero, so the two-sided limit exists and equals zero.

## Slide 9: Piecewise: $\lim_{x \to 3} [x]$

Slide ID: `greatest_integer_example`
<!-- voiceover-hash: 87bc2c5f6774b64df5c4b0f11a4e7a812b010822403eb463b384036060d4a115 -->
Scene template: `example_walkthrough`

Narration:

The greatest integer function returns the largest integer no greater than x. So the bracket of four is four, the bracket of four point one is four, the bracket of four point eight is four. To take the limit at three, examine each side. From the right, x is just above three, so the bracket is three; the right limit is three. From the left, x is just below three, so the bracket is two; the left limit is two. Three is not equal to two, so the two-sided limit does not exist.

## Slide 10: When the Laws Are Not Enough

Slide ID: `transition_to_squeeze`
<!-- voiceover-hash: ac31afdcba1f00723ba568d2b12edd5a08f079d2aa2c6e67989a95cf11c2d757 -->
Scene template: `section_transition`

Narration:

The product law needs both factors to have a limit. Sometimes one factor oscillates wildly. The squeeze theorem rescues such cases by trapping the value we want between two friendly functions.

## Slide 11: The Squeeze Theorem

Slide ID: `squeeze_theorem`
<!-- voiceover-hash: eb29385b94b85f45e53ceac09e801d9c3b132b50dcd785b6728ce522dbdab7c2 -->
Scene template: `definition_math`

Narration:

Suppose g of x is at most f of x is at most h of x for all x near a, possibly excluding a itself. Suppose further that g and h have the same limit L at a. Then f also has limit L at a. The picture is exactly the name: f is squeezed between g and h, and as g and h close in on the same value, f has nowhere else to go. The hypothesis only needs to hold near a, not globally.

## Slide 12: Squeezing Oscillating Products

Slide ID: `squeeze_examples`
<!-- voiceover-hash: ec4f3426b9a6695152414a3c65e520ae4100b04cbf341da5d7c660a1ea086d99 -->
Scene template: `example_walkthrough`

Narration:

Take the limit of x squared times sine of one over x at zero. The product law fails because sine of one over x oscillates between minus one and one and has no limit there. Use the squeeze instead: since sine is bounded between minus one and one, multiplying by the nonnegative x squared gives the chain minus x squared at most x squared sine one over x at most x squared. Both bounds tend to zero, so the squeeze pins the middle quantity to zero. The companion limit, x times cosine of one over x at zero, runs the same argument with the cosine bound: minus absolute value of x at most x cosine one over x at most absolute value of x. Again both bounds go to zero, so this limit is also zero.

## Slide 13: How to Compute $\lim_{x \to a} f(x)$

Slide ID: `computing_limit_strategy`
<!-- voiceover-hash: 4f5189b105b21c7c11c06c5b697cd42d51ac58431ff4d223b6bebb490fb226ab -->
Scene template: `procedure_steps`

Narration:

Here is the order to attempt computational techniques. First, try direct substitution; if f of a is defined and the function is a polynomial or rational with nonzero denominator there, that is the answer. Second, if substitution gives an indeterminate form like zero over zero, simplify algebraically by factoring and cancelling, rationalizing a square-root, or combining fractions. Third, if the function is piecewise, split into one-sided limits on each branch. Fourth, if the function is trapped between two simpler functions whose limits agree, apply the squeeze theorem. Fifth, if the values grow without bound, the limit is plus or minus infinity and you have a vertical asymptote.

## Slide 14: Key Takeaways

Slide ID: `recap`
<!-- voiceover-hash: 85729d80f5a97fc559c38856157fbfeac206b37701cc0e4885c7b9ffd3804f9f -->
Scene template: `recap_cards`

Narration:

Six things to take away. First, limits commute with sums, differences, scalar multiples, products, integer powers, and quotients with nonzero denominator limit. Second, polynomials and well-behaved rationals submit to direct substitution. Third, when substitution gives zero over zero, simplify. Fourth, on piecewise definitions, split into one-sided limits and check whether they agree. Fifth, the squeeze theorem rescues bounded oscillation. Sixth, follow the strategy in order: substitute first, simplify second, split third, squeeze fourth, and otherwise read off plus or minus infinity.

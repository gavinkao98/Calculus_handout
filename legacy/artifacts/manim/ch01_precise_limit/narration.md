# ch01_precise_limit Final Narration

Source file: `inputs\manim_storyboards\ch01_precise_limit.yml`
Deck ID: `ch01_precise_limit`

You may edit the narration text below each **Narration:** heading.
For scenes with **Voiceover Beats**, edit the beat text/reveal map in the storyboard YAML; the joined beat text is exported here for proofreading.
Do NOT change the hidden hash comment lines either — they are used for stale-file conflict detection.
Do NOT change the Slide ID lines — they are used to match edits back to the correct scene.
After editing, run `python tools/manim_sync_narration_back.py --deck-id ch01_precise_limit` to write changes back to the storyboard YAML.

## Slide 1: The Precise Definition of a Limit

Slide ID: `opening_hook`
<!-- voiceover-hash: 463dafc4c382fa810638fb101ec38513386696c24a8103db0c0cb7e56299f0db -->
Scene template: `title_bullets`

Narration:

For two centuries after Newton and Leibniz, calculus did extraordinary work in physics and astronomy, but its foundations were under suspicion. Arguments leaned on infinitesimals, quantities thought of as extremely small without ever being defined precisely. The nineteenth century gave the answer we still use today: the epsilon-delta definition. Today we will replace the informal phrase "x is close to a" with a precise inequality, and we will see what that buys us.

## Slide 2: When the Function's Value Disagrees With Its Limit

Slide ID: `piecewise_motivation`
<!-- voiceover-hash: a4aa5c09948819be5a8617e0caff80c19567160620881aa7caba7c7baab390b2 -->
Scene template: `graph_focus`

Narration:

Consider a function that is two x minus one almost everywhere, but jumps to six at x equals three. As x approaches three, the linear part is heading toward five, not six. The value at three itself is irrelevant -- the limit looks at the neighborhood around the point, not the point. So we should expect the limit to be five. Our job today is to make that "should expect" into a proof.

## Slide 3: How Close Is Close Enough?

Slide ID: `tolerance_example`
<!-- voiceover-hash: 9ae05dc5c4bc8d671938bcb327975cc76e6e3708af6490398b867b1878cabae2 -->
Scene template: `example_walkthrough`

Narration:

Let us make close numerical. Suppose we demand that f of x differ from five by less than a tenth. The absolute value of f of x minus five simplifies to the absolute value of two x minus six. That is twice the absolute value of x minus three. So the tolerance one tenth on the output corresponds to a window of one twentieth on the input. If x is within zero point zero five of three, then f of x is within a tenth of five.

Voiceover Beats:

- `set_output_tolerance` reveal: header, step_0
  text: Let us make close numerical. Suppose we demand that f of x differ from five by less than a tenth.
- `simplify_output_error` reveal: step_1, math_line_0
  text: The absolute value of f of x minus five simplifies to the absolute value of two x minus six.
- `factor_distance` reveal: math_line_1
  text: That is twice the absolute value of x minus three.
- `solve_input_window` reveal: step_2, math_line_2
  text: So the tolerance one tenth on the output corresponds to a window of one twentieth on the input.
- `state_guarantee` reveal: takeaway
  text: If x is within zero point zero five of three, then f of x is within a tenth of five.

## Slide 4: From Specific Tolerances to Every Tolerance

Slide ID: `tolerance_to_general`
<!-- voiceover-hash: 8d8c9b740144a9274a553520fff41ff6e65ed9c1cd0e9664379108691097977e -->
Scene template: `section_transition`

Narration:

The same calculation works for tolerance one hundredth, or one thousandth. Whatever the tolerance is, we just halve it to get the input window. So in fact, for any positive epsilon whatsoever, we can take delta equal to epsilon over two and the guarantee holds. The word "arbitrarily" in the informal definition means exactly this: we can answer the question for every epsilon, not just for a chosen few.

## Slide 5: The $\varepsilon$-$\delta$ Definition

Slide ID: `epsilon_delta_definition`
<!-- voiceover-hash: abc469430beb54b1a8a7fdeb85afe4f84a22a8b6f1d3651b721836d9bf8e5514 -->
Scene template: `definition_math`

Narration:

Here is the definition. The limit of f of x as x approaches a equals L. For every positive epsilon, there exists a positive delta. Whenever x is within delta of a but not equal to a, the value f of x is within epsilon of L. Two quantifiers, in this order: for every epsilon, there exists a delta. The order matters. Delta is allowed to depend on epsilon, but every epsilon must get its delta.

Voiceover Beats:

- `introduce_definition` reveal: header, statement, math_line_0
  text: Here is the definition. The limit of f of x as x approaches a equals L.
- `epsilon_first` reveal: math_line_1
  text: For every positive epsilon, there exists a positive delta.
- `implication` reveal: math_line_2
  text: Whenever x is within delta of a but not equal to a, the value f of x is within epsilon of L.
- `quantifier_order` reveal: none
  text: Two quantifiers, in this order: for every epsilon, there exists a delta. The order matters.
- `delta_depends` reveal: none
  text: Delta is allowed to depend on epsilon, but every epsilon must get its delta.

## Slide 6: What the Definition Looks Like

Slide ID: `epsilon_delta_picture`
<!-- voiceover-hash: f84ee21489c27b8f9f5f378aa4c693b5c4dc8f952fae850e7a129114f43c8f47 -->
Scene template: `graph_focus`

Narration:

Here is the geometric reading. Pick a target tolerance epsilon: this draws a horizontal band around L of half-width epsilon. The definition demands a delta -- a vertical strip around a of half-width delta -- such that every graph point whose x-coordinate lies inside this strip, except possibly at x equals a itself, must land inside the horizontal band. The limit does not look at f of a. Now picture a smaller epsilon: the band squeezes, and we are forced to choose a smaller delta to keep the graph inside. The phrase "for every epsilon" means: no matter how thin the band gets, a matching delta exists.

## Slide 7: First Payoff: The Limit Is Unique

Slide ID: `uniqueness_statement`
<!-- voiceover-hash: 6d11d25f464524ed5b07583f88b0aa7824a35312b709e7ba42c5455747cb9859 -->
Scene template: `definition_math`

Narration:

Here is the first thing the definition buys us. If a limit exists, it is unambiguous. There is no second value the function could also be approaching. With the precise definition, this is a theorem we can prove.

Voiceover Beats:

- `payoff` reveal: header, statement
  text: Here is the first thing the definition buys us. If a limit exists, it is unambiguous.
- `two_limits` reveal: math_line_0
  text: There is no second value the function could also be approaching.
- `conclusion` reveal: math_line_1
  text: With the precise definition, this is a theorem we can prove.

## Slide 8: Proof: Two Limits Force a Contradiction

Slide ID: `uniqueness_proof`
<!-- voiceover-hash: 21579275d9557f158846f25d27c116d97824d3adc0267b19998d2d89551e7063 -->
Scene template: `example_walkthrough`

Narration:

Suppose for contradiction that the same function had two limits, L and M, with L different from M. Set epsilon to half the distance between them. The definition gives a delta one for L and a delta two for M. Take x within the smaller of the two deltas, so f of x is within epsilon of both L and M. Now bound the absolute value of L minus M by inserting f of x. The triangle inequality splits it into the distance from L to f of x plus the distance from f of x to M. Each term is less than epsilon, so the total is less than two epsilon, which equals the original distance. We have shown the distance is strictly less than itself, a contradiction. Therefore L equals M.

Voiceover Beats:

- `assume_two_limits` reveal: header, step_0
  text: Suppose for contradiction that the same function had two limits, L and M, with L different from M.
- `choose_epsilon` reveal: none
  text: Set epsilon to half the distance between them.
- `get_two_deltas` reveal: step_1
  text: The definition gives a delta one for L and a delta two for M.
- `smaller_delta` reveal: step_2
  text: Take x within the smaller of the two deltas, so f of x is within epsilon of both L and M.
- `insert_fx` reveal: step_3, math_line_0
  text: Now bound the absolute value of L minus M by inserting f of x.
- `triangle_inequality` reveal: math_line_1
  text: The triangle inequality splits it into the distance from L to f of x plus the distance from f of x to M.
- `contradiction_chain` reveal: step_4, math_line_2
  text: Each term is less than epsilon, so the total is less than two epsilon, which equals the original distance.
- `therefore` reveal: takeaway
  text: We have shown the distance is strictly less than itself, a contradiction. Therefore L equals M.

## Slide 9: How to Verify $\lim f(x) = L$ from the Definition

Slide ID: `verification_procedure`
<!-- voiceover-hash: 5f607ccc3fafdc92f93152b48fd0a91355e1053630155369009cdddefa5f7afb -->
Scene template: `procedure_steps`

Narration:

Verifying a limit from the definition is a four-step routine. Start with a generic positive epsilon, not a specific number, and treat it as the input. Work with the absolute value of f of x minus L, and bound it by an expression involving the absolute value of x minus a. Choose delta so that the bound is less than epsilon. If another factor depends on x, pre-restrict x near a, then take delta to be the minimum of the radius and the epsilon-based bound. The final write-up must read forward: given epsilon, choose delta, then verify the implication.

Voiceover Beats:

- `routine` reveal: header
  text: Verifying a limit from the definition is a four-step routine.
- `generic_epsilon` reveal: step_0
  text: Start with a generic positive epsilon, not a specific number, and treat it as the input.
- `bound_error` reveal: step_1
  text: Work with the absolute value of f of x minus L, and bound it by an expression involving the absolute value of x minus a.
- `choose_delta` reveal: step_2
  text: Choose delta so that the bound is less than epsilon.
- `min_trick` reveal: step_3
  text: If another factor depends on x, pre-restrict x near a, then take delta to be the minimum of the radius and the epsilon-based bound.
- `write_implication` reveal: equation_0
  text: The final write-up must read forward: given epsilon, choose delta, then verify the implication.

## Slide 10: Worked Example: $\lim_{x \to 3}(4x - 5) = 7$

Slide ID: `linear_epsilon_delta`
<!-- voiceover-hash: 116779d47ddb15d3046e9d56f29e8bae00a88bedd4e82aed49ca41719df5e7e8 -->
Scene template: `example_walkthrough`

Narration:

Given a positive epsilon, we want four x minus five to be within epsilon of seven whenever x is close enough to three. Compute the absolute value of four x minus five minus seven. It simplifies to four times the absolute value of x minus three. To force this below epsilon, require x minus three to be less than epsilon over four. So delta equals epsilon over four, and the implication holds for every epsilon.

Voiceover Beats:

- `state_goal` reveal: header, step_0
  text: Given a positive epsilon, we want four x minus five to be within epsilon of seven whenever x is close enough to three.
- `compute_error` reveal: math_line_0
  text: Compute the absolute value of four x minus five minus seven.
- `constant_multiple` reveal: step_1, math_line_1
  text: It simplifies to four times the absolute value of x minus three.
- `choose_delta` reveal: step_2, math_line_2
  text: To force this below epsilon, require x minus three to be less than epsilon over four.
- `linear_takeaway` reveal: takeaway
  text: So delta equals epsilon over four, and the implication holds for every epsilon.

## Slide 11: Worked Example: $\lim_{x \to 1}(x^{2} - 5x + 6) = 2$

Slide ID: `quadratic_epsilon_delta`
<!-- voiceover-hash: 94dc3b8b8737938d06a0757d674de9dbf033b04a33103f5e2fc736a641424a4e -->
Scene template: `example_walkthrough`

Narration:

Same goal as before, but the algebra is more delicate. The expression simplifies to the product of x minus one and x minus four, so we have two factors to handle. The first factor is the small quantity we control; the second factor depends on x. Pre-restrict by demanding x is within one of one. Then x lies between zero and two, so the absolute value of x minus four is at most four. Now the product is at most four times the absolute value of x minus one. To push this below epsilon, force the absolute value of x minus one below epsilon over four. The new feature is the min trick: delta must satisfy both the pre-restriction and the epsilon-based bound. So we take delta to be the minimum of one and epsilon over four.

Voiceover Beats:

- `delicate_algebra` reveal: header
  text: Same goal as before, but the algebra is more delicate.
- `factor_expression` reveal: step_0, math_line_0
  text: The expression simplifies to the product of x minus one and x minus four, so we have two factors to handle.
- `controlled_factor` reveal: none
  text: The first factor is the small quantity we control; the second factor depends on x.
- `pre_restrict` reveal: step_1
  text: Pre-restrict by demanding x is within one of one. Then x lies between zero and two, so the absolute value of x minus four is at most four.
- `bound_product` reveal: math_line_1
  text: Now the product is at most four times the absolute value of x minus one.
- `epsilon_bound` reveal: step_2
  text: To push this below epsilon, force the absolute value of x minus one below epsilon over four.
- `minimum_delta` reveal: step_3, math_line_2
  text: The new feature is the min trick: delta must satisfy both the pre-restriction and the epsilon-based bound.
- `quadratic_takeaway` reveal: takeaway
  text: So we take delta to be the minimum of one and epsilon over four.

## Slide 12: Infinite Limits, Made Precise

Slide ID: `infinite_limit_precise`
<!-- voiceover-hash: 59b22f898d755268eaca8600fad8fd8a4f99235ff5b78e18312b9c0a63cfad72 -->
Scene template: `definition_math`

Narration:

The same machinery upgrades the informal infinite-limit definition. The limit is plus infinity if, for every positive threshold M, there exists a delta. Whenever x is within delta of a but not equal to a, f of x exceeds M. The minus-infinity version is the mirror: for any negative threshold N, f of x is less than N. The threshold can be pushed arbitrarily far, and close enough to a, the function eventually clears it in the appropriate direction.

Voiceover Beats:

- `same_machinery` reveal: header, statement
  text: The same machinery upgrades the informal infinite-limit definition.
- `positive_infinity_quantifiers` reveal: math_line_0
  text: The limit is plus infinity if, for every positive threshold M, there exists a delta.
- `positive_infinity_implication` reveal: math_line_1
  text: Whenever x is within delta of a but not equal to a, f of x exceeds M.
- `negative_infinity` reveal: math_line_2
  text: The minus-infinity version is the mirror: for any negative threshold N, f of x is less than N.
- `threshold_intuition` reveal: none
  text: The threshold can be pushed arbitrarily far, and close enough to a, the function eventually clears it in the appropriate direction.

## Slide 13: A Glimpse Ahead: Continuity

Slide ID: `continuity_preview`
<!-- voiceover-hash: 6d8f3aceaeb3bd4d83fb59ed25f411fb82336d154290b60759917cc190721d66 -->
Scene template: `definition_math`

Narration:

Before we close, a one-line preview. If the function is defined at a, and the limit at a equals the value at a, then the function is called continuous at a. Continuity is a property of well-behaved functions that we will study later, and many theorems about derivatives and integrals rest on it.

Voiceover Beats:

- `one_line_preview` reveal: header, statement
  text: Before we close, a one-line preview.
- `continuity_equation` reveal: math_line_0
  text: If the function is defined at a, and the limit at a equals the value at a, then the function is called continuous at a.
- `why_it_matters` reveal: none
  text: Continuity is a property of well-behaved functions that we will study later, and many theorems about derivatives and integrals rest on it.

## Slide 14: Key Takeaways

Slide ID: `recap`
<!-- voiceover-hash: f0f0b93fb94a790bd441bda545b9b0f94a33095a183571332534e66f0e404395 -->
Scene template: `recap_cards`

Narration:

Five things to take away. First, the precise definition replaces close with two inequalities, and the order of quantifiers matters. Second, the geometric reading is a horizontal epsilon band and a vertical delta strip. Third, limits are unique by a clean triangle-inequality argument. Fourth, verification means bounding the error, and using the minimum when an x-dependent factor appears. Fifth, infinite limits and continuity both speak the same language now.

Voiceover Beats:

- `recap_intro` reveal: header
  text: Five things to take away.
- `recap_definition` reveal: point_0, identity_0
  text: First, the precise definition replaces close with two inequalities, and the order of quantifiers matters.
- `recap_geometry` reveal: point_1
  text: Second, the geometric reading is a horizontal epsilon band and a vertical delta strip.
- `recap_unique` reveal: point_2
  text: Third, limits are unique by a clean triangle-inequality argument.
- `recap_verification` reveal: point_3
  text: Fourth, verification means bounding the error, and using the minimum when an x-dependent factor appears.
- `recap_next` reveal: point_4, identity_1
  text: Fifth, infinite limits and continuity both speak the same language now.

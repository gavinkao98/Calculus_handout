# ch01_one_sided_infinite_limits Final Narration

Source file: `inputs\manim_storyboards\ch01_one_sided_infinite_limits.yml`
Deck ID: `ch01_one_sided_infinite_limits`

You may edit the narration text below each **Narration:** heading.
For scenes with **Voiceover Beats**, edit the beat text/reveal map in the storyboard YAML; the joined beat text is exported here for proofreading.
Do NOT change the hidden hash comment lines either — they are used for stale-file conflict detection.
Do NOT change the Slide ID lines — they are used to match edits back to the correct scene.
After editing, run `python tools/manim_sync_narration_back.py --deck-id ch01_one_sided_infinite_limits` to write changes back to the storyboard YAML.

## Slide 1: One-Sided and Infinite Limits

Slide ID: `opening_hook`
<!-- voiceover-hash: 5a9b70f396e462b1d0c3b9f750734e9765854254c51e16e756b5882bbe22884b -->
Scene template: `title_bullets`

Narration:

The basic limit asks how a function behaves as x approaches a from any direction. Two extensions of this idea earn their own machinery. First, a function may approach different values depending on which side x is coming from. Second, a function may not approach any finite number at all, but instead grow without bound. Today we make both of these precise and tie infinite limits to vertical asymptotes.

## Slide 2: Left- and Right-Hand Limits

Slide ID: `one_sided_definition`
<!-- voiceover-hash: 9fb684e4367a6754d4285daf0011255d9b23d4c49825e2cbe6b6833846e3b801 -->
Scene template: `definition_math`

Narration:

The left-hand limit of f at a, written limit as x approaches a minus, is the value L that f of x approaches when x comes in from the left, that is, through values less than a. The right-hand limit, written limit as x approaches a plus, uses values greater than a. The minus and plus superscripts are not algebraic signs; they tell you which side of a we approach from. Everything else from the basic limit definition is unchanged: the value f of a is still ignored, and the arbitrarily-close-by-going-sufficiently-close idea is the same.

## Slide 3: Left and Right Limits Can Differ

Slide ID: `one_sided_figure`
<!-- voiceover-hash: b654117ac62e8b525a6a737809bacbaee55e469302c3b8444e9796647fdd453b -->
Scene template: `graph_focus`

Narration:

Here is a function with a jump at x equals a. From the left, the curve is heading up toward L one. From the right, the curve is heading up toward L two, a strictly higher value. Both one-sided limits exist: limit from the minus side is L one, limit from the plus side is L two. But the two-sided limit, the one without a sign on the arrow, does not exist, because the values from the two sides do not agree. The hollow circles signal that the function value at a itself is not part of either limit.

## Slide 4: When the Two-Sided Limit Exists

Slide ID: `two_sided_criterion`
<!-- voiceover-hash: f7488a8e3e29a420500cf0f846dd31eabc10765b15461daca8c0fbcec62163b9 -->
Scene template: `definition_math`

Narration:

Here is the bridge between one-sided and two-sided limits. The two-sided limit equals L if and only if both one-sided limits equal L. Both directions of this biconditional are useful. To prove a two-sided limit exists, check that both one-sided limits agree. To prove a two-sided limit fails to exist, find a case where the two one-sided limits disagree. The previous figure was such a case.

## Slide 5: A Piecewise Function at $x = 2$

Slide ID: `piecewise_example`
<!-- voiceover-hash: d0d15eb43e207d56f173c7eafe3c5f1397099f9ac121308257cb4a7d5322b9c6 -->
Scene template: `example_walkthrough`

Narration:

Consider f equal to x plus one when x is less than two, and four minus x when x is at least two. To take the left limit, use the branch that holds for x less than two: x plus one. As x approaches two from the left, x plus one approaches three. To take the right limit, use the branch for x at least two: four minus x. As x approaches two from the right, four minus x approaches two. The two one-sided limits are three and two. They are different, so the two-sided limit does not exist.

## Slide 6: When the Limit Is Not Finite

Slide ID: `transition_to_infinite`
<!-- voiceover-hash: c85b2d478309c0f50209fce8b656277764701100aff037552c9ef30f4bfc20e1 -->
Scene template: `section_transition`

Narration:

Sometimes the values do not crowd toward a finite L at all. Instead they grow without bound. We need a notation and a definition for that case.

## Slide 7: $y = 1/x^{2}$ Near $0$

Slide ID: `one_over_x_squared_motivation`
<!-- voiceover-hash: 3f804a9661d56fb95abfe3db97033697d26a2ffef93b8ce2832e5abac1c6b8ec -->
Scene template: `graph_focus`

Narration:

Look at one over x squared near zero. As x gets close to zero from either side, x squared is a very small positive number, so its reciprocal is enormous. At x equals zero point one, the value is one hundred. At x equals zero point zero one, the value is ten thousand. The values shoot up faster than any number you could pick. There is no finite L the function approaches; the limit in the ordinary sense does not exist. We capture this growth with a new notation: limit equals plus infinity.

## Slide 8: Infinite Limits

Slide ID: `infinite_limit_definition`
<!-- voiceover-hash: 7d6c57d905adb81c70d6d00e6e0f408a523b970cf72acb5bf7430b0a4eeecae7 -->
Scene template: `definition_math`

Narration:

Here is the informal definition. We write limit equals plus infinity if the values of f of x can be made arbitrarily large by taking x sufficiently close to a, with x not equal to a. The phrase "arbitrarily large" is doing the work: any threshold you set, the function will eventually exceed it once x is close enough to a. The minus infinity version is the mirror image: the values are arbitrarily large in the negative direction. The symbol infinity does not name a real number; it records the unbounded growth.

## Slide 9: Two Sides, Two Infinities

Slide ID: `typical_infinite_limits`
<!-- voiceover-hash: 95de1de6a3e2291bcc760be42fbecdc563be3770e2d0df50bf034c163b958c0d -->
Scene template: `graph_focus`

Narration:

Here is a curve that already shows two of the four typical infinite-limit cases. The function one over x minus two has a vertical line at x equals two where the denominator vanishes. Approach two from the right: x minus two is small and positive, so the reciprocal blows up to plus infinity. Approach two from the left: x minus two is small and negative, so the reciprocal blows down to minus infinity. The other two cases, where the curve goes to plus infinity from the left or to minus infinity from the right, look the same with the signs flipped.

## Slide 10: Vertical Asymptotes

Slide ID: `vertical_asymptote_definition`
<!-- voiceover-hash: b999dd377f1c30a98b7e7b6e416e594930e15e7eef920fde2d36bf747dab1440 -->
Scene template: `definition_math`

Narration:

The line x equals a is called a vertical asymptote of the curve y equals f of x if at least one of the four one-sided infinite limits at a holds. The qualifier "at least one" matters: the curve does not have to blow up on both sides for x equals a to count as an asymptote. So the test for a vertical asymptote at x equals a is to check the four one-sided limits and see if any one of them is plus or minus infinity.

## Slide 11: Asymptote of $y = \dfrac{2x}{x - 3}$

Slide ID: `rational_asymptote_example`
<!-- voiceover-hash: efb6b4eba3516db4b7bbc2b72ba66ad385316090961fc7421ed072c2425cd800 -->
Scene template: `example_walkthrough`

Narration:

The denominator vanishes only at x equals three, so the only candidate for a vertical asymptote is x equals three. Take the right limit. As x approaches three from the right, x minus three is a small positive number, while two x is close to six. The ratio is six over a small positive number, which goes to plus infinity. Now the left limit. As x approaches three from the left, x minus three is a small negative number, while two x is still close to six. The ratio goes to minus infinity. At least one one-sided limit is infinite, so the line x equals three is a vertical asymptote.

## Slide 12: Asymptote of $y = \ln x$ at $0$

Slide ID: `ln_x_asymptote_example`
<!-- voiceover-hash: 80639ec37789f5ac7700077f0722e6fdd74b9889cf0d039b771424c7782b3dd8 -->
Scene template: `example_walkthrough`

Narration:

Now a non-rational example. The natural logarithm is defined only for positive x, so we cannot take a left limit at zero; only the right limit makes sense. As x approaches zero from the right, ln x decreases without bound. So the right limit of ln x at zero is minus infinity. One one-sided limit is infinite, so x equals zero is a vertical asymptote of the natural logarithm.

## Slide 13: Key Takeaways

Slide ID: `recap`
<!-- voiceover-hash: 27628fea6864e7f67dcca90ca0c667ad1f832a7d0a6bb4b09a794de71e280584 -->
Scene template: `recap_cards`

Narration:

Six things to remember. First, one-sided limits look at the approach from one side only and are written with a minus or plus superscript. Second, the two-sided limit exists if and only if both one-sided limits exist and agree. Third, when the values of f grow without bound near a, write the limit as plus or minus infinity. Fourth, infinity is a notational marker, not a number. Fifth, the line x equals a is a vertical asymptote when at least one of the four one-sided infinite limits holds. Sixth, on a rational function, vertical asymptotes can occur only where the denominator vanishes.

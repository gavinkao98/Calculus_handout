# ch01_limit_of_function Final Narration

Source file: `inputs\manim_storyboards\ch01_limit_of_function.yml`
Deck ID: `ch01_limit_of_function`

You may edit the narration text below each **Narration:** heading.
For scenes with **Voiceover Beats**, edit the beat text/reveal map in the storyboard YAML; the joined beat text is exported here for proofreading.
Do NOT change the hidden hash comment lines either — they are used for stale-file conflict detection.
Do NOT change the Slide ID lines — they are used to match edits back to the correct scene.
After editing, run `python tools/manim_sync_narration_back.py --deck-id ch01_limit_of_function` to write changes back to the storyboard YAML.

## Slide 1: The Limit of a Function

Slide ID: `opening_hook`
<!-- voiceover-hash: 4dfae9d9f76ce350468383ff1b22e3b6616c87b9e8174187c47f37d1866679e3 -->
Scene template: `title_bullets`

Narration:

A central question in calculus: how does a quantity behave as something else gets arbitrarily small? The average velocity over an interval is a clean example. As the time interval shrinks toward zero, what does the average velocity approach? That target value, when it exists, is the instantaneous velocity. Today we formalize this idea as the limit of a function and start guessing limits from tables and graphs.

## Slide 2: Secants Sweeping Toward the Tangent

Slide ID: `secant_to_tangent`
<!-- voiceover-hash: 61904492e92ea173ab22129c4a3b0da5b94d1ad86eafe7fb77157a83618b2856 -->
Scene template: `graph_focus`

Narration:

Here is the picture behind the limit. Take a curve, fix a base point on it, and draw secant lines through that base point and another point further along the curve. As the second point slides toward the base point, each secant gets steeper, then less steep, eventually leveling out. The slopes of those secants approach a single number: the slope of the tangent line at the base point. The same machinery that finds this tangent slope is what defines a limit in general.

## Slide 3: The Limit (Informal)

Slide ID: `limit_definition`
<!-- voiceover-hash: 14f84d28e41bf396d88cf3795d1d120552d7a32cf921f6ca107264910e42199e -->
Scene template: `definition_math`

Narration:

Here is the informal definition we will use today. Suppose f is defined for every x near a, except possibly at a itself. We say the limit of f of x as x approaches a is L if we can make f of x arbitrarily close to L by taking x sufficiently close to a, but not equal to a. The phrase "arbitrarily close" carries the weight: any target tolerance on the output can be achieved by choosing x close enough to a. The phrase "not equal to a" is the technical caveat that lets the limit ignore the value of f at a itself.

## Slide 4: An Equivalent Notation

Slide ID: `notation_variants`
<!-- voiceover-hash: ba8d8913ab61aa0cb1d1b7d540eb3fddd6e5a6e803394aceca02d679fd56596e -->
Scene template: `definition_math`

Narration:

A second notation says the same thing in different symbols. Instead of writing limit of f of x as x approaches a equals L, you may write f of x arrow L as x arrow a. We read this aloud as f of x tends to L as x tends to a. The two notations are interchangeable, and you will see both freely in textbooks. We will use whichever reads most cleanly in context.

## Slide 5: The Limit Ignores $f(a)$

Slide ID: `value_at_a_irrelevant`
<!-- voiceover-hash: d42093f29b5ae666b0ccdc0c41a623b1f70588431a3e87099b135c41bb53ea96 -->
Scene template: `graph_focus`

Narration:

Here is the most important consequence. The limit looks at the values of f near a, not the value at a. Three different functions can share the same limit at a even when their values at a disagree. The function might equal L at a, it might equal something else, or it might not be defined at a at all. The hollow circle marks that we are taking x toward three but excluding three itself. The limit, traced by the curve, is eight regardless.

## Slide 6: Guessing $\lim_{x \to 1} \dfrac{x - 1}{x^{2} - 1}$

Slide ID: `tabular_example_rational`
<!-- voiceover-hash: 4bef1be3a0ab82eb967cdc61119bd0fab6474e7a77e6a6d6ec8d8028c910535f -->
Scene template: `example_walkthrough`

Narration:

The expression x minus one over x squared minus one is undefined at x equals one, because the denominator vanishes. So we cannot just plug in. Build a small table of values. From below: at x equals zero point nine, the ratio is about zero point five two six. At zero point nine nine, it is about zero point five zero three. From above: at one point zero one, about zero point four nine eight; at one point one, about zero point four seven six. The values are crowding toward one half. So we guess that the limit equals one half. We are not proving it yet, only conjecturing from the data.

## Slide 7: Guessing $\lim_{t \to 0} \dfrac{\sqrt{t^{2} + 9} - 3}{t^{2}}$

Slide ID: `tabular_example_radical`
<!-- voiceover-hash: 916dd7f9b0405d1117b6e494c6e964ff6004ba2aa60550d3c018cd926aa0e3d4 -->
Scene template: `example_walkthrough`

Narration:

Same idea, different shape. The expression is undefined at t equals zero. Tabulate values near zero. At t equals minus zero point one and at t equals zero point one, the ratio is roughly zero point one six six six two. At t equals plus or minus zero point zero one, it is closer to zero point one six six six six six. The values are settling on one sixth, which is zero point one six six six and so on. So we guess that the limit equals one sixth. Notice the two-sided agreement: the values from the left and from the right are heading to the same number, which makes the conjecture more credible.

## Slide 8: What Comes Next

Slide ID: `forward_to_techniques`
<!-- voiceover-hash: e7e9152ebaf0741833ab69747d84073ec4878eb818656903a5bd30435469c4ff -->
Scene template: `section_transition`

Narration:

Tables are unreliable: they can lie if the function does something subtle very close to a. Coming up, we will get systematic. One-sided and infinite limits, then algebraic limit laws, and finally the precise definition that makes every claim provable.

## Slide 9: Key Takeaways

Slide ID: `recap`
<!-- voiceover-hash: e7e5bac52f698839ef00e893a587137855cf63fa3620b8e2b5169ef809c54d49 -->
Scene template: `recap_cards`

Narration:

Five things to take away. First, the informal limit says f of x can be made arbitrarily close to L by taking x close to a but not equal to a. Second, two notations: limit of f equals L, or f arrow L as x arrow a. Third, and most important, the limit ignores f of a entirely; what happens at the point itself is invisible. Fourth, when direct substitution fails, build a small two-sided table of values to guess the limit. Fifth, a tabular guess is a conjecture, not a proof.

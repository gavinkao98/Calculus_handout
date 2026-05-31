# ch01_inverse_trig_functions Final Narration

Source file: `inputs\manim_storyboards\ch01_inverse_trig_functions.yml`
Deck ID: `ch01_inverse_trig_functions`

You may edit the narration text below each **Narration:** heading.
For scenes with **Voiceover Beats**, edit the beat text/reveal map in the storyboard YAML; the joined beat text is exported here for proofreading.
Do NOT change the hidden hash comment lines either — they are used for stale-file conflict detection.
Do NOT change the Slide ID lines — they are used to match edits back to the correct scene.
After editing, run `python tools/manim_sync_narration_back.py --deck-id ch01_inverse_trig_functions` to write changes back to the storyboard YAML.

## Slide 1: Inverse Trigonometric Functions

Slide ID: `opening_hook`
<!-- voiceover-hash: 4040078ff9f769a62e52c41d61fa4b3c29471872dcefdff83dbdacfb48dd0400 -->
Scene template: `title_bullets`

Narration:

The trig functions take an angle and return a ratio. Often we need the reverse: we know a ratio and want the angle. The slope of a ramp gives an angle of inclination; the ratio of sides in a right triangle gives one of its acute angles. None of the trig functions are one-to-one on the whole real line, so to invert them we have to restrict each one to an interval where it is one-to-one. Today we build the inverse sine, cosine, and tangent, and then list the three less common inverses.

## Slide 2: $\sin x$ Is Not One-to-One on $\mathbb{R}$

Slide ID: `sine_not_one_to_one`
<!-- voiceover-hash: f8d38bbd7d2aed605266b881e04a4b0ba52e7411ec59d223e428d913a43ef7b6 -->
Scene template: `graph_focus`

Narration:

Here is the sine function on the interval from minus two pi to two pi. A horizontal line at height one half slices through the curve in five places inside this window alone, and infinitely many places on the full real line. Five different inputs all have sine equal to one half. So if we tried to define the inverse globally, asking for the angle whose sine is one half would give us infinitely many answers. To get a function back, we must pick out exactly one of these answers by restricting the domain.

## Slide 3: The Principal Branch: $\sin x$ on $[-\pi/2, \pi/2]$

Slide ID: `restricted_sine`
<!-- voiceover-hash: c3f9d977b8f14275143e5cfb075392ec2d661fd4e21d7de5723875e3f536a79a -->
Scene template: `graph_focus`

Narration:

Now restrict to the closed interval from minus pi over two to pi over two. On this interval, sine climbs strictly from minus one up to one. Strictly increasing means one-to-one, and the values cover the entire interval from minus one to one. Inside this window every horizontal line at a height between minus one and one hits the curve exactly once, so we can invert. This restricted piece is what defines arcsin.

## Slide 4: The Inverse Sine

Slide ID: `arcsin_definition`
<!-- voiceover-hash: 9f226420f4474ac6f99329bd677d53583dbd0a4ce02a119106ffb750ab890792 -->
Scene template: `definition_math`

Narration:

The inverse sine of x, written arcsin x or sine to the minus one of x, is the angle y in the closed interval from minus pi over two to pi over two whose sine equals x. Its domain, the set of legal inputs, is the closed interval from minus one to one, because that is the range of sine. Its range, the set of outputs, is the principal interval. The composition identities follow: applying sine to arcsin gives back x, and applying arcsin to sine gives back x as long as the angle stays inside the principal interval.

## Slide 5: Two Common Traps

Slide ID: `arcsin_cautions`
<!-- voiceover-hash: d72b45a5a8632bbfec51c042e5d95594037a691b2d609c4dd86ec5371cb8d89c -->
Scene template: `definition_math`

Narration:

Two warnings before we use arcsin. First, the notation sine to the minus one of x means arcsin of x; it does not mean one over sine of x, because the exponent minus one is a function-inverse symbol here, not a power. Second, arcsin of sine of x equals x only on the principal interval. Outside, it returns whatever value in the principal interval has the same sine. For example, arcsin of sine of pi is arcsin of zero, which is zero, not pi. Always read identities like this with their domain restrictions attached.

## Slide 6: Evaluating $\arcsin(1/2)$

Slide ID: `arcsin_eval_simple`
<!-- voiceover-hash: 79adf84d0a284b38fbcb7ea5cd5ca1cb1523938a5dd4ab20a44245952de871bb -->
Scene template: `example_walkthrough`

Narration:

First a quick evaluation. We want the angle y in the principal interval whose sine is one half. Pi over six is in the principal interval, and sine of pi over six is one half by the standard thirty-sixty-ninety triangle. So arcsin of one half equals pi over six. Notice that five pi over six also has sine one half, but it sits outside the principal interval, so arcsin does not return it.

## Slide 7: Computing $\tan(\arcsin(1/3))$

Slide ID: `arcsin_triangle`
<!-- voiceover-hash: aef7a50f989373e6f6d0c34ca91a8d0afe1cad9242e68fe65d894c0e73ea6501 -->
Scene template: `example_walkthrough`

Narration:

Here is the standard trick when one trig function is composed with the inverse of another. Set theta equal to arcsin of one third, so by definition sine of theta is one third and theta sits in the principal interval. Draw a right triangle with angle theta, opposite side one, hypotenuse three. Pythagoras gives the adjacent side: square root of nine minus one, which is two root two. Tangent is opposite over adjacent, so tan of theta is one over two root two. The triangle picture turns a composition of arcsin and tan into pure right-triangle geometry.

## Slide 8: The Inverse Cosine

Slide ID: `arccos_definition`
<!-- voiceover-hash: fbac74f0d9a83b5a131847a54a27c02343265a8c6036aa9392e5ae277d241e78 -->
Scene template: `definition_math`

Narration:

Cosine on the closed interval from zero to pi is one-to-one: it descends strictly from one down to minus one. So arccos of x is the angle y in zero to pi whose cosine is x. The domain is again minus one to one, but the range is now zero to pi instead of the symmetric interval. The composition identities mirror the arcsin ones: cosine of arccos returns x for inputs in minus one to one, and arccos of cosine returns x for angles in zero to pi.

## Slide 9: Inverting Tangent

Slide ID: `transition_to_arctan`
<!-- voiceover-hash: d088f3c45c683d36e55c5813e647bdaa19167f3820af95199a5e49ec76574dd5 -->
Scene template: `section_transition`

Narration:

Tangent is a different beast: its restricted branch is bounded in the input but unbounded in the output. That changes the shape of arctan in two important ways.

## Slide 10: $\tan x$ on $(-\pi/2, \pi/2)$

Slide ID: `restricted_tangent`
<!-- voiceover-hash: 7d28249ac441084c35bd9ae9c089acef9778c7415a457aba2c6a03f0bc659f4a -->
Scene template: `graph_focus`

Narration:

The restricted branch of tangent runs over the open interval from minus pi over two to pi over two. Inside that window tangent climbs from negative infinity at the left edge up through zero to positive infinity at the right edge. So the domain of arctan is the entire real line: every real number is the tangent of some angle in this interval. The range of arctan is the open interval, with the endpoints missing because tangent never actually attains plus or minus infinity.

## Slide 11: The Inverse Tangent

Slide ID: `arctan_definition`
<!-- voiceover-hash: 671aa08b70975e57dd817d717539fbaf2b8dcecd3aba9d478e4c84ca18c3404e -->
Scene template: `definition_math`

Narration:

Arctan of x is the angle y in the open interval from minus pi over two to pi over two whose tangent is x. The domain is the whole real line; the range is the open principal interval. The composition identities take the same form as before: tangent of arctan returns x for every real x, and arctan of tangent returns x for angles strictly inside the principal interval.

## Slide 12: Simplifying $\cos(\arctan x)$

Slide ID: `arctan_simplify`
<!-- voiceover-hash: 3c5eb2915c3aeb46fe6cefac8bf878441d1b4555ed95aaf1b5cffeb7e2416e3e -->
Scene template: `example_walkthrough`

Narration:

Let y equal arctan x, so tan of y is x and y lies in the open principal interval. We want cos of y. Use the Pythagorean identity one plus tan squared equals secant squared. So secant squared of y is one plus x squared. Since y is in the open interval from minus pi over two to pi over two, cosine is positive there, so secant is positive. Take the positive square root: secant of y is the square root of one plus x squared. Cosine is the reciprocal of secant, so cos of arctan x is one over the square root of one plus x squared. The branch choice on arctan was the load-bearing step: it forced the positive sign.

## Slide 13: Three More: $\operatorname{arccsc}$, $\operatorname{arcsec}$, $\operatorname{arccot}$

Slide ID: `remaining_inverses`
<!-- voiceover-hash: 3d8324f89c5f96d21718739c0ea43dbdab08e3dfdf8e5590def0d7ac9b4ff3c1 -->
Scene template: `definition_math`

Narration:

The remaining three inverses come up less often, but the recipe is identical: restrict to a principal interval, then invert. Arccsc and arcsec take inputs of absolute value at least one, since cosecant and secant never produce values strictly between minus one and one. Arccot is defined for all real inputs. Be warned: textbooks differ on which principal interval to use for arcsec and arccsc. We use the convention that makes later derivative formulas cleanest, but always check which branch a source is using before plugging in numbers.

## Slide 14: Key Takeaways

Slide ID: `recap`
<!-- voiceover-hash: 23383268cd04b61c0e2ec50bff59789a5f915c28d91fe6b8daf4a4744df21eaa -->
Scene template: `recap_cards`

Narration:

Six things to remember. First, no trig function is one-to-one on the real line. Second, restrict each one to a principal interval, then invert. Third, the principal intervals are the closed interval minus pi over two to pi over two for arcsin, the closed interval zero to pi for arccos, and the open principal interval for arctan. Fourth, sine to the minus one means inverse, never reciprocal. Fifth, a composition like arcsin of sine of x equals x only inside the principal interval. Finally, when a trig function meets an inverse trig function, draw the implied right triangle.

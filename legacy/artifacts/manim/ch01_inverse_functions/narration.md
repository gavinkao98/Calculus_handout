# ch01_inverse_functions Final Narration

Source file: `inputs\manim_storyboards\ch01_inverse_functions.yml`
Deck ID: `ch01_inverse_functions`

You may edit the narration text below each **Narration:** heading.
Inline 〔顯示...〕 markers correspond to dynamic reveal elements — please leave them and the hidden bookmark-marks comment in place; the sync tool relies on them to restore bookmark positions.
For scenes with **Voiceover Beats**, edit the beat text/reveal map in the storyboard YAML; the joined beat text is exported here for proofreading.
Do NOT change the hidden hash comment lines — they are used for stale-file conflict detection.
Do NOT change the Slide ID lines — they are used to match edits back to the correct scene.
After editing, run `python tools/manim_sync_narration_back.py --deck-id ch01_inverse_functions` to write changes back to the storyboard YAML.

## Slide 1: Inverse Functions

Slide ID: `opening_hook`
<!-- voiceover-hash: cfffa8762086beb99d75db5d48a4acf8c75ff648e78b23164a42c1986dae94e7 -->
Scene template: `title_bullets`

Narration:

A function is a one-way process: you put in a number, you get one back. But a lot of the time, we also want to run the process in reverse. A formula turns Celsius into Fahrenheit; we want the formula that turns Fahrenheit back. A formula turns a radius into a volume; we want the formula that recovers the radius from the volume. So here is the question we will answer today: when can we actually reverse a function, and when is it impossible?

## Slide 2: One-to-One Functions

Slide ID: `one_to_one_definition`
<!-- voiceover-hash: 2849a65be101594365dd702842a058640b0923372a6bc796f7ab19ebf39841bf -->
Scene template: `definition_math`

Narration:

The property we need is called one-to-one. A function is one-to-one when different inputs always give different outputs. No two distinct x-values ever land on the same y-value. There is an equivalent way to state this that is often easier in a proof: if f of x one equals f of x two, then x one must equal x two. The two forms say exactly the same thing; the second is the contrapositive of the first.

## Slide 3: A Real-World Check

Slide ID: `real_world_one_to_one`
<!-- voiceover-hash: 4958364c037bed8ff67db75f715d084bd0943c3179ea6991d7dd8a00b956a659 -->
Scene template: `example_walkthrough`

Narration:

Before we try any algebra, here is a test you can do in a room full of people. Assign each student their student ID number. No two students share an ID, so different students always come out with different IDs. That function is one-to-one. Now assign each student their blood type. Alice is Type O, Bob is Type O -- two different students, same output. That function is not one-to-one. The move is always the same: ask whether a single output could have come from two different inputs.

## Slide 4: Testing with Algebra

Slide ID: `algebraic_one_to_one_test`
<!-- voiceover-hash: 30cc6ad994fd932a670eabed17bb5ee34177df65c2a9c660bc7686e406be3cd2 -->
Scene template: `example_walkthrough`

Narration:

Now two mathematical functions. First, f of x equals x on the interval zero to one. If x one is different from x two, then f of x one, which is just x one, is obviously different from f of x two, which is just x two. So this one is one-to-one. Second, g of x equals x squared on minus one to one. Watch what happens at one half and minus one half -- two different inputs, but they both square to one fourth. One counterexample is enough: g is not one-to-one on this interval.

## Slide 5: Why $x^2$ Cannot Be Inverted on $[-1, 1]$

Slide ID: `why_x_squared_fails`
<!-- voiceover-hash: 0d8f6a8f35fcbbafc59f087a0f1f371e48fba34bda4c28f576d4bd66d1feeae5 -->
Scene template: `graph_focus`

Narration:

Let us see that failure on a graph. Here is the parabola y equals x squared on the interval minus one to one. The output one fourth sits at this horizontal level. A dashed line at that level crosses the curve in two places -- at x equals one half on the right and x equals minus one half on the left. If we tried to define g inverse of one fourth, we would have to pick between two equally good answers. A function cannot return two answers at once. So g inverse of one fourth is simply not defined.

## Slide 6: The Horizontal Line Test

Slide ID: `horizontal_line_test_statement`
<!-- voiceover-hash: 807bf6a2bb9236d42c5c9ea6d9ea712479529bf57fe945a11c5124e001ba544c -->
Scene template: `definition_math`

Narration:

There is a clean visual rule that captures all of this. A horizontal line has equation y equals c, so it represents one fixed output value. If that line crosses the graph more than once, two different x-values are producing the same output and the function is not one-to-one. If every horizontal line you can draw hits the graph at most once, then every output corresponds to a unique input, and the function is one-to-one. That is the horizontal line test.

## Slide 7: The Test in Action

Slide ID: `horizontal_line_test_figure`
<!-- voiceover-hash: b9e9ebc6f017513977d27824a86e1fc12144de620da2ed36cf99b0acf0986ce1 -->
Scene template: `graph_focus`

Narration:

On the left, a straight line. Every horizontal level crosses it exactly once, so this graph passes the test. On the right, a parabola. A horizontal line at the right height crosses it twice, once on each side of the axis of symmetry, so this graph fails the test. When you are looking at a graph and wondering whether an inverse can exist, the sweeping horizontal line is the fastest check you have.

## Slide 8: Defining the Inverse

Slide ID: `transition_to_inverses`
<!-- voiceover-hash: 08db89cf615657d45a99bfc8779e7f536868c3461e651ed653bceca3f272fc84 -->
Scene template: `section_transition`

Narration:

Now that we know what one-to-one means, we can define the inverse function itself.

## Slide 9: The Inverse Function

Slide ID: `inverse_definition`
<!-- voiceover-hash: f5a76c778158a82a745422b744ec5bcf5c00decb25eda7e74f06be8126719921 -->
Scene template: `definition_math`

Narration:

Here is the definition. Suppose f is one-to-one with domain A and range B. Its inverse, written f inverse, has domain B and range A, and the rule is: f inverse of y equals x exactly when f of x equals y. So the inverse just reverses the direction. The outputs of f become the inputs of f inverse, and the inputs of f become the outputs. By convention, when we focus on the inverse itself, we switch back to writing its independent variable as x.

## Slide 10: When Does an Inverse Exist?

Slide ID: `existence_theorem`
<!-- voiceover-hash: 0ffcd3080847af2f8c6318f0ac0151abb79b9044fd5e22b07e913a9aa01c83a3 -->
Scene template: `theorem_proof`

Narration:

The central theorem is tight: a function has an inverse if and only if it is one-to-one. Forward direction first. Suppose f has an inverse. If f of x one equals f of x two, apply f inverse to both sides; the compositions collapse and we are left with x one equals x two. So f is one-to-one. Conversely, suppose f is one-to-one. For each y in the range, there is exactly one x that maps to it -- the one-to-one property guarantees uniqueness. That rule, y back to its unique x, is the inverse function.

## Slide 11: Two Quick Inverses

Slide ID: `basic_inverse_examples`
<!-- voiceover-hash: 743c04b31a59468eeb5efccc2358e2997ff9dd3ba952ae33acc81d6a670d6109 -->
Scene template: `example_walkthrough`

Narration:

Before doing any real algebra, two inverses you should be able to see at a glance. The identity function f of x equals x sends every number to itself, so its inverse is also the identity: f inverse of x equals x. Now g of x equals x cubed. To invert it, ask: what sends the output back? The cube root. So g inverse of x equals the cube root of x. No procedure needed when the algebra is this direct.

## Slide 12: The Cancellation Equations

Slide ID: `composition_identities`
<!-- voiceover-hash: 70b91824b05dfc88a50bc184953f14e123f3b6ec81a3eaef80911e0fb133ae5f -->
Scene template: `definition_math`

Narration:

The inverse literally undoes the original. That gives two composition identities worth memorizing. First: f inverse of f of x equals x, for every x in the domain of f. Apply f, then undo it with f inverse, and you land back where you started. Second: f of f inverse of x equals x, for every x in the range of f. Apply f inverse, then f, and again you return to where you started. These two identities are also your verification tool: if you think you have found f inverse, check that both round-trips give back x.

## Slide 13: Finding the Inverse

Slide ID: `transition_to_procedure`
<!-- voiceover-hash: e565db7044543d7f1211eaeb83fdc3bdaf406ec677b09cc7b4fa4b1328b6c0ee -->
Scene template: `section_transition`

Narration:

We know when an inverse exists. Now we need a procedure for actually computing one.

## Slide 14: How to Find an Inverse

Slide ID: `finding_inverse_procedure`
<!-- voiceover-hash: 9dbda37a97356b2bb6ac2d466bc006fff26bfb2d054c9579dc8f05993b93a21f -->
Scene template: `procedure_steps`

Narration:

When you already know f is one-to-one, finding its inverse is mechanical. Step one: write y equals f of x. Step two: solve that equation for x in terms of y. This is usually the hardest step, because the difficulty depends entirely on the algebra of f. Step three: interchange x and y. That last swap is not cosmetic -- it rewrites the inverse as a function of x, which is the standard convention.

## Slide 15: Worked Example: $f(x) = x^3 + 2$

Slide ID: `example_cubic`
<!-- voiceover-hash: 0e6a33b612e49beff501c3c5dec96260daa0002915626d0024e4b56bb9050912 -->
Scene template: `example_walkthrough`

Narration:

Apply the procedure to f of x equals x cubed plus two. Step one: write y equals x cubed plus two. Step two: subtract two from both sides, then take the cube root. That gives x equals the cube root of y minus two. Step three: interchange x and y. So f inverse of x equals the cube root of x minus two. Always close with a check. Plug f inverse into f: cube the cube root, which brings back x minus two, then add two, which brings back x. The cancellation equation holds, so the inverse is correct.

## Slide 16: Graphs of $f$ and $f^{-1}$

Slide ID: `cubic_graph_reflection`
<!-- voiceover-hash: 7fc18f4d6ec59d12b147e01d5e7472711641d871d1a1c1310784ce899b153446 -->
Scene template: `graph_focus`

Narration:

Here is the geometric punchline. The graph of f of x equals x cubed plus two is an S-shaped curve shifted up by two. The graph of its inverse, the cube root of x minus two, is the mirror image reflected across the dashed line y equals x. Every point a comma b that sits on f corresponds to the point b comma a sitting on f inverse. This reflection property works for every invertible function paired with its inverse -- it is not special to cubics.

## Slide 17: Restricting the Domain of $x^2$

Slide ID: `domain_restriction_idea`
<!-- voiceover-hash: 9fba487a4ec6185bbebd0dd92c779ee1be701e1895f9faca7b59385580aaac7a -->
Scene template: `example_walkthrough`

Narration:

Earlier we saw that x squared on minus one to one is not one-to-one. But what if we trim the domain? On the interval x greater than or equal to zero, the parabola is strictly increasing -- larger inputs always give strictly larger outputs. So on that smaller domain, x squared is one-to-one. Now we can invert it. Write y equals x squared with x at least zero. Solve: x equals the square root of y, where we pick the nonnegative root because the original domain required x at least zero. Swap x and y: f inverse of x equals the square root of x, with x at least zero.

## Slide 18: $x^2$ and $\sqrt{x}$ as Reflections

Slide ID: `restricted_parabola_graph`
<!-- voiceover-hash: 1ef2d2e2e68a0f42d7ad2cea6cb750cd128efe7f73bc7fbd302f35e025c71546 -->
Scene template: `graph_focus`

Narration:

On the restricted domain, the graph of x squared is the right half of a parabola. Its inverse, the square root function, is the reflection across y equals x. Notice how symmetric the two curves sit about the dashed diagonal. This is exactly the same reflection we saw with the cubic. The point of this example is the domain trick: a function that failed the one-to-one test globally becomes invertible once we shrink its domain to a piece where it is one-to-one.

## Slide 19: Key Takeaways

Slide ID: `recap`
<!-- voiceover-hash: 82d47eebe6dd0279cf8848813b6b639041d7247588bffd054612ef97853e14ff -->
Scene template: `recap_cards`

Narration:

Let us pull it all together. A function is one-to-one when no two inputs share an output, and the horizontal line test is the fast visual check. A function has an inverse if and only if it is one-to-one. To find the inverse: write y equals f of x, solve for x, then swap x and y. Verify with the cancellation equations. Geometrically, the graph of f inverse is the reflection of f across the line y equals x. And if a function is not one-to-one globally, restricting its domain can still give you an inverse.

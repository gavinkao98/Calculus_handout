# Inverse Functions and One-to-One Functions Final Narration

Source file: `chapters/ch01_foundations.tex`
Deck ID: `ch01_inverse_functions`

This file is seeded from the draft once. After that, it is user-owned and the generator preserves it.
The narration may be more conversational than the textbook, but definitions, assumptions, and conclusions should remain mathematically correct.

## Slide 1: Why Study Inverse Functions?

Slide ID: `why_inverse_functions_matter`
Learning goal: See why reversing a process leads naturally to one-to-one functions.
Slide type: `motivation`

Narration:

We begin with the practical question of when a function can be reversed. If a formula converts one quantity into another, we often want to go back in the opposite direction. A temperature-conversion formula is a simple example: Celsius to Fahrenheit, then Fahrenheit back to Celsius. But reversal only works if an output identifies one original input. That is why the first idea we need is one-to-one behavior.

## Slide 2: Definition of a One-to-One Function

Slide ID: `one_to_one_definition`
Learning goal: Recognize the formal condition that makes a function invertible.
Slide type: `definition`

Narration:

Here is the formal condition. A function is one-to-one when different inputs never collapse to the same output. Equivalently, if two outputs are equal, then the inputs must already be equal. The second statement is often the better proof tool, but both say the same mathematical thing. This is the point where rigor matters: an inverse function can only be defined if every output leads back to one and only one input.

## Slide 3: A Real-World One-to-One Test

Slide ID: `student_id_example`
Learning goal: Apply the definition to ordinary processes before moving to algebraic functions.
Slide type: `example`

Narration:

This example shows that the definition is about matching, not about algebraic symbols. If each student is matched with a student ID number, the function is one-to-one because each ID belongs to exactly one student. But if each student is matched with a blood type, then many students can share the same output, so the function is not one-to-one. This is the right habit to build early: do not stare at the symbols first. Ask whether one output can be traced back to several different inputs.

## Slide 4: Why \(x^2\) Can Fail To Be Invertible

Slide ID: `square_function_inverse_failure`
Learning goal: See exactly how repeated outputs prevent an inverse from being well defined.
Slide type: `warning`

Narration:

Now we move to a standard mathematical example. The identity function on zero to one is one-to-one because every input keeps its own value. In contrast, the square function on minus one to one is not one-to-one: one half and minus one half both give one fourth. That repeated output is not a minor issue. It means the inverse would have to send one fourth back to two different inputs, which is impossible for a function. Not every function has an inverse. A function can have an inverse only if each output corresponds to exactly one input; in other words, the function must be one-to-one. For g of x equals x squared on the interval from minus one to one, the value one fourth comes from both one half and minus one half. Therefore g inverse of one fourth is not well defined.

## Slide 5: The Horizontal Line Test

Slide ID: `horizontal_line_test_rule`
Learning goal: Connect the definition of one-to-one with a geometric test on the graph.
Slide type: `definition`

Narration:

The horizontal line test is the graph version of the definition. A horizontal line means the output value is fixed at y equals c. If that line meets the graph twice, then the same output c is being produced by two different x-values, so the function cannot be one-to-one. If every horizontal line meets the graph at most once, then every output corresponds to at most one input, which is exactly the condition we need.

## Slide 6: Horizontal Line Test: Visual Check

Slide ID: `horizontal_line_test_figure`
Learning goal: Read the horizontal line test directly from a graph.
Slide type: `figure`

Narration:

This figure lets us read the test directly. On the left, the horizontal line intersects only once, so the graph is still consistent with a one-to-one function. On the right, the horizontal line meets the parabola twice, which tells us immediately that one output value is coming from two inputs. That visual failure is exactly why an inverse cannot be defined on the entire interval.

## Slide 7: Definition of an Inverse Function

Slide ID: `inverse_function_definition`
Learning goal: Describe an inverse as a function that reverses the original correspondence.
Slide type: `definition`

Narration:

Once a function is one-to-one, we can define its inverse. If the original function sends x to y, then the inverse sends y back to x. That is why the domain and range switch roles. The outputs of the original function become the allowed inputs of the inverse. Sometimes the notation is rewritten with x as the input variable for the inverse, but that is only a relabeling. The mathematical content is still that the inverse reverses the original correspondence.

## Slide 8: When Does an Inverse Exist?

Slide ID: `inverse_existence_theorem`
Learning goal: Use the theorem that completely characterizes when an inverse exists.
Slide type: `theorem`

Narration:

This theorem gives the complete criterion: a function has an inverse if and only if it is one-to-one. So the property we studied earlier is not just helpful; it is exactly the right condition. The examples show how the theorem turns into computation. The identity function stays unchanged under inversion, and for x cubed we solve y equals x cubed for x, then interchange x and y to get the cube root function.

## Slide 9: Three Steps For Finding An Inverse

Slide ID: `finding_inverse_procedure`
Learning goal: Use the standard algebraic procedure for computing inverse functions.
Slide type: `procedure`

Narration:

Once we know an inverse exists, there is a standard algebraic procedure for finding it. First write y equals f of x. Next solve that equation for x in terms of y. Then interchange x and y. That final relabeling is not cosmetic; it rewrites the answer with the inverse viewed as a new function of x.

## Slide 10: Example: Finding The Inverse Of \(x^3+2\)

Slide ID: `shifted_cubic_example`
Learning goal: Apply the three-step procedure to a function that is already one-to-one.
Slide type: `example`

Narration:

Here the procedure works cleanly. We start with y equals x cubed plus two, solve for x, and then interchange the variables. That gives the inverse function x minus two under a cube root. Because x cubed is already one-to-one on all real numbers, we do not need any domain restriction first.

## Slide 11: Example: Restricting The Domain Of \(x^2\)

Slide ID: `restricted_parabola_example`
Learning goal: See how a domain restriction can create an inverse for a function that was not invertible before.
Slide type: `example`

Narration:

This example shows why domain restriction matters. On all of the real numbers, x squared is not one-to-one. But once we restrict the domain to x greater than or equal to zero, every output comes from exactly one input. That is why the inverse becomes the nonnegative square root rather than plus or minus square root.

## Slide 12: Checking An Inverse By Composition

Slide ID: `composition_identities_figure`
Learning goal: Use the composition identities to verify that a candidate inverse really works.
Slide type: `recap`

Narration:

To finish the section, we record the identities that certify an inverse. If you apply a function and then its inverse, you must return to the starting point. If you apply the inverse first and then the function, you must also return to the starting point, provided you begin in the correct set. These are the formulas you should check whenever you want to confirm that a proposed inverse is correct.

# Seed — §2.2 The Derivative as a Function

> Transcribed from the handwritten manuscript (pp. 4–5 of 13).
> Faithful to the manuscript: structure, order, notation, and deliberate omissions preserved.
> seed 語法＝輕量可讀（反引號行內＋Unicode；見 RULE.md ①）。

---

## The derivative at a point (general definition)

In general, for `f(x)`, define the derivative of `f` at `a` by `lim_{h→0} (f(a + h) − f(a))/h`, provided the limit exists. We write `f'(a) = lim_{h→0} (f(a + h) − f(a))/h`.

(Equivalent: `f'(a) = lim_{x→a} (f(x) − f(a))/(x − a)`.)

## Example

`f(x) = x² + 4x − 2`. Find the derivative of `f` at `a`.

**Solution.**
`(f(a + h) − f(a))/h = ( ((a + h)² + 4(a + h) − 2) − (a² + 4a − 2) )/h`
`= ( (a² + 2ah + h² + 4a + 4h − 2) − (a² + 4a − 2) )/h`
`= (2ah + h² + 4h)/h = 2a + h + 4`.

Thus `lim_{h→0} (f(a + h) − f(a))/h = 2a + 4`, i.e. the derivative of `f` at `a` `= 2a + 4`.

## The derivative as a function

For each point `a`, the derivative of `f` at `x` is `lim_{h→0} (f(x + h) − f(x))/h`. Using the variable `x` (in place of `a`), we write
`f'(x) = lim_{h→0} (f(x + h) − f(x))/h`,
i.e. `f'(x)` is itself a function of `x` (where the limit exists). We call `f'(x)` the derivative of `f`.

## Example

`f(x) = √x`, `x > 0`. Find `f'(x)`.

**Solution.** `f'(x) = lim_{h→0} (√(x + h) − √x)/h`; rationalise:
`(√(x + h) − √x)/h = ( (√(x + h) − √x)(√(x + h) + √x) ) / ( h(√(x + h) + √x) ) = 1/(√(x + h) + √x)`.
Thus `lim_{h→0} 1/(√(x + h) + √x) = 1/(2√x)`, i.e. `f'(x) = 1/(2√x)`.

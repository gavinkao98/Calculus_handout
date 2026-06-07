# Seed — §2.1 The Tangent Line and the Derivative at a Point

> Transcribed from the handwritten manuscript (pp. 1–3 of 13).
> Faithful to the manuscript: structure, order, notation, and deliberate omissions preserved.
> seed 語法＝輕量可讀（反引號行內＋Unicode；見 RULE.md ①）。

---

## Opening motivation

Consider `y = f(x)`; we want the tangent line to this curve at the point `(a, f(a)) ≡ P`.

[Figure: a curve with a tangent line at a marked point `a`.]

(Finding the tangent line is important and useful — many applications, e.g. approximation …)

Since the line passes through `(a, f(a))`, we only need its slope. So, how to find the slope?

## Secant line and limiting slope

Let `x` be near `a`, so that `(x, f(x))` is near `(a, f(a))`.

[Figure: curve with two nearby points, secant line through them.]

The ratio `m_PQ = (f(x) − f(a)) / (x − a)` is the slope of the secant line `PQ`. Hence when `Q` approaches `P` along the curve, the limiting value is the slope at `P`.

Thus if `m_PQ` has a limit as `Q → P` (i.e. `x → a`), we define that value to be the slope of the tangent line.

## Definition (tangent line)

The tangent line to `y = f(x)` at `(a, f(a))` is the line through `P` with slope
`lim_{x→a} (f(x) − f(a))/(x − a)`, provided the limit exists.

## Remark (zoom-in interpretation)

If we zoom in far enough at `P`, the curve looks like a straight line — so it is useful to find that line.

## Equivalent form (h-substitution)

The limit `(f(x) − f(a))/(x − a)` has an equivalent form used more often. Since `x` is near `a`, write `x = a + h`; then the slope is `lim_{h→0} (f(a + h) − f(a))/h`.

## Example

Curve `y = 3/x`, `x > 0`. Find the tangent line at `(3, 1)`.

**Solution.** `m = lim_{h→0} (f(3 + h) − f(3))/h`
`= lim_{h→0} ( 3/(3+h) − 1 )/h = lim_{h→0} ( −h/(3+h) )/h`
`= lim_{h→0} −1/(3+h) = −1/3`.

So the tangent line is `y − 1 = (−1/3)(x − 3)`, i.e. `x + 3y − 6 = 0`.

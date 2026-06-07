# Seed — §2.5 The Product and Quotient Rules

> Transcribed from the handwritten manuscript (pp. 11–13 of 13).
> Faithful to the manuscript: structure, order, notation, and deliberate omissions preserved.
> seed 語法＝輕量可讀（反引號行內＋Unicode；見 RULE.md ①）。

---

## Product and quotient rules

Recall `d/dx (f ± g) = d/dx f ± d/dx g`. We now learn `d/dx (fg)` and `d/dx (f/g)`.

## Product rule

The derivative of `fg`, i.e. `(fg)'`, is **not** `f'·g'`.

**Counterexample:** `f(x) = x`, `g(x) = x²` ⇒ `fg = x³`, `(fg)' = 3x²`. But `f'(x) = 1`, `g'(x) = 2x`, so `f'·g' = 2x ≠ (fg)'`.

Let us find the correct formula for `(fg)'`.

**Proof.** Use the definition: `( f(x+h)g(x+h) − f(x)g(x) ) / h`. A useful trick:
`f(x+h)g(x+h) − f(x)g(x)`
`= f(x+h)g(x+h) − f(x)g(x+h) + f(x)g(x+h) − f(x)g(x)`
`= (f(x+h) − f(x))·g(x+h) + f(x)·(g(x+h) − g(x))`.
Thus
`[…]/h = ( (f(x+h) − f(x))·g(x+h) )/h + f(x)·( (g(x+h) − g(x))/h )`.
We have learnt: if `lim h(x)` and `lim s(x)` both exist, then `lim h(x)s(x) = lim h(x) · lim s(x)`. Hence
`lim_{h→0} ( (f(x+h) − f(x))/h )·g(x+h) = lim_{h→0} (f(x+h) − f(x))/h · lim_{h→0} g(x+h) = f'(x)·g(x)`,
`lim_{h→0} f(x)·( (g(x+h) − g(x))/h ) = f(x)·g'(x)`.
Therefore
`(f(x)g(x))' = f'(x)·g(x) + f(x)·g'(x)`, i.e. `d/dx (fg) = (d/dx f)·g + f·(d/dx g)`.

### Example

`h(x) = x·e^x` ⇒ `h'(x) = e^x + x·e^x = e^x·(1 + x)`.

## The quotient rule

For `f(x)/g(x)`:
`f(x+Δx)/g(x+Δx) − f(x)/g(x) = ( f(x+Δx)·g(x) − g(x+Δx)·f(x) ) / ( g(x+Δx)·g(x) )`.
Divide by `Δx`. On the numerator, add and subtract `f(x)g(x)`:
`f(x+Δx)·g(x) − g(x+Δx)·f(x) = f(x+Δx)g(x) − f(x)g(x) + f(x)g(x) − g(x+Δx)f(x)`
`= (f(x+Δx) − f(x))·g(x) − (g(x+Δx) − g(x))·f(x)`.
So the difference quotient is
`( (f(x+Δx) − f(x))/Δx )·( g(x) / (g(x+Δx)·g(x)) ) − ( (g(x+Δx) − g(x))/Δx )·( f(x) / (g(x+Δx)·g(x)) )`.
Let `Δx → 0`:
`= f'(x)·g(x)/g(x)² − g'(x)·f(x)/g(x)²`.
Thus `d/dx (f/g) = ( f'(x)·g(x) − f(x)·g'(x) ) / g(x)²`.

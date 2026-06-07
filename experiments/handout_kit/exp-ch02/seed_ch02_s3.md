# Seed — §2.3 Differentiability, Continuity, and Higher Derivatives

> Transcribed from the handwritten manuscript (pp. 6–7 of 13).
> Faithful to the manuscript: structure, order, notation, and deliberate omissions preserved.
> seed 語法＝輕量可讀（反引號行內＋Unicode；見 RULE.md ①）。

---

## Differentiability

In general, for `f(x)`, the limit `lim_{h→0} (f(a + h) − f(a))/h` may or may not exist. Hence the definition.

### Definition (differentiable)

`f` is differentiable at `a` if `f'(a)` exists. When we say `f` is differentiable on an interval `(a, b)`, it means `f` is differentiable at every point of the interval.

## Example (non-differentiability)

An `f` not differentiable at a point: `f(x) = |x|`, looking at its derivative at `x = 0`.
`lim_{h→0} (|0 + h| − |0|)/h = lim_{h→0} |h|/h`, where `lim_{h→0⁺} = 1` and `lim_{h→0⁻} = −1` — so the limit does not exist.

[Figure: V-shaped graph of `|x|`.]

## Differentiable implies continuous

A basic but important result on the relationship of continuity and differentiability.

### Theorem

If `f` is differentiable at `a`, then `f` is continuous at `a`.
(Converse `⇐` not true, as `f(x) = |x|` at `x = 0` shows.)

**Proof.** Goal: prove `lim_{x→a} f(x) = f(a)`, i.e. `lim_{x→a} (f(x) − f(a)) = 0`.
Write `f(x) − f(a) = ( (f(x) − f(a))/(x − a) ) · (x − a)`.
Both `lim_{x→a} (f(x) − f(a))/(x − a)` and `lim_{x→a} (x − a)` exist, so
`lim_{x→a} (f(x) − f(a)) = lim_{x→a} (f(x) − f(a))/(x − a) · lim_{x→a} (x − a) = f'(a) · 0 = 0`.
(By assumption `f'(a) = lim_{x→a} (f(x) − f(a))/(x − a)`.) Hence `lim_{x→a} (f(x) − f(a)) = 0`. ∎

## Higher derivatives

Start with `f(x)`; its derivative `f'(x)` is again a function. So we can ask whether `f'` is differentiable; if it is, `(f')' = f''`, the second derivative. Similarly we continue to `f'''`, …, `f^(n)(x)` — the derivative taken `n` times.

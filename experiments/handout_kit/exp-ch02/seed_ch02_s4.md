# Seed — §2.4 Derivatives of Polynomials and the Exponential Function

> Transcribed from the handwritten manuscript (pp. 8–10 of 13).
> Faithful to the manuscript: structure, order, notation, and deliberate omissions preserved.
> seed 語法＝輕量可讀（反引號行內＋Unicode；見 RULE.md ①）。

---

## Derivatives of polynomials and exponential functions

We learn how to differentiate these functions.

### ① Constant function

If `f(x) = c` (constant), then `lim_{h→0} (f(x + h) − f(x))/h = lim_{h→0} (c − c)/h = 0`. Thus `f'(x) = 0` for every `x`.

### ② Power function

If `f(x) = xⁿ` (power function, `n` a positive integer, `n = 1, 2, …`):

**Formula:** `d/dx (xⁿ) = n·x^(n−1)`.

**Proof.** Use the definition `(f(x) − f(a))/(x − a)`. Note
`xⁿ − aⁿ = (x − a)(x^(n−1) + a·x^(n−2) + … + a^(n−1))`.
Thus `lim_{x→a} (f(x) − f(a))/(x − a) = lim_{x→a} (x^(n−1) + a·x^(n−2) + … + a^(n−1)) = n·a^(n−1)`.

### ③ Alternative proof (binomial expansion)

Use the definition `(f(x + h) − f(x))/h`.
`(x + h)ⁿ = xⁿ + C^n_1·h·x^(n−1) + C^n_2·h²·x^(n−2) + … + hⁿ`.
So `(x + h)ⁿ − xⁿ = C^n_1·h·x^(n−1) + … + hⁿ`.
Divide by `h`: `= n·x^(n−1) + … + h^(n−1)` (the last term being `n·x·h^(n−2)`).
All terms except `n·x^(n−1)` carry an `h`; so as `h → 0`, `= n·x^(n−1)`.

### Exercise

`d/dx (xⁿ) = n·x^(n−1)` also when `n` is a negative integer, `n = −1, −2, …`.

### Sum and constant-multiple rules

Directly from the definition: if `f` and `g` are both differentiable, then
① `d/dx (f + g) = d/dx f + d/dx g`
② `d/dx (c·f) = c · d/dx f`

### Corollary (polynomial derivative)

If `f` is a polynomial `f(x) = aₙ·xⁿ + … + a₀`, then
`d/dx f = aₙ·n·x^(n−1) + a_(n−1)·(n−1)·x^(n−2) + … + a₁`.

## Exponential function

**Note:** we have defined `e^x` before, as `e^x = 1 + x + x²/2! + x³/3! + … + xⁿ/n! + …`.

Let `f(x) = e^x`; study its derivative.
`f'(x) = lim_{h→0} (e^(x+h) − e^x)/h = lim_{h→0} e^x·(e^h − 1)/h = e^x · lim_{h→0} (e^h − 1)/h`.
Since `e^h = 1 + h + h²/2! + …`, we have `(e^h − 1)/h = 1 + h/2! + h²/3! + …`, so as `h → 0`, `lim_{h→0} (e^h − 1)/h = 1`.
Hence `f'(x) = e^x`, i.e. the derivative of `e^x` is still itself. Moreover `f^(n)(x) = e^x`.

### Remark

For `f(x) = b^x`, `b > 1`: with the chain rule (later) we can easily find `f'(x) = b^x · log_e b`.

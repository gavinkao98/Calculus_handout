# Seed — §4.1 Construction of the Exponential Function

> stage ① 產物。Transcribed from the handwritten manuscript `2023-11-4-ExponentialFunction`,
> **pp.1–3** (up to the partial-sum tail bound that closes the x>0 convergence result;
> the next item `[e2]` "e^x is continuous for x>0" begins §4.2).
> Manuscript's own section title: "§ Construction of the Exponential function".
> Faithful to the manuscript: structure, order, notation, and deliberate omissions preserved.
> seed 語法＝輕量可讀（反引號行內＋Unicode；見 CONTENT_DIRECTION ① / `seed_ch03_s1.md`）。漂亮 KaTeX 留給 ④。可疑／非標準處標 **[請查核]**。
> **數學 cross-check（非手稿）**：legacy `ch04_exponential_logarithm.tex` §4.1 (L17–166)；§4.2 seed `seed_s42.md` 的「§4.1 依賴」段（已 ①-verify 2026-06-03）與本 seed 末尾的尾界一致。

---

## From rational exponents to the series definition

For `n ∈ ℕ` (當 n 為正整數) and `a > 0`, we define
`aⁿ = a × a × ⋯ × a` (**n copies**),
and we define `x = a^(1/n) > 0` to be the positive root of
`xⁿ − a = 0`.

Then for `q = n/m`, `m, n ∈ ℕ`, we define
`a^q = (a^(1/m))ⁿ`.

It is no[t] hard to see, for `n₁, n₂ ∈ ℕ`,
- `a^(n₁) × a^(n₂) = a^(n₁+n₂)`,
- `(a^(n₁))^(n₂) = a^(n₁·n₂)`.

[指數律 = exponent law]

**Q: How about `a^r` for `r ∉ ℚ`, `a > 0`?**
(手稿在此拋出「無理數指數怎麼定義」的問題，**未在本節作答**——直接跳到用 power series 定義 `e^x`。`a^r` 的一般建構手稿延到後面 `a^x = e^(x ln a)`。)

---

## Definition of e^x (for x > 0)

**Define:** For `x > 0`,
`e^x = Σ_{n=0}^∞ xⁿ/n!`   …(1),
where `0! := 1`, `n! = 1 × 2 × 3 × ⋯ × n`.

---

## Property — The completeness of real numbers [實數完備性]

1. Suppose `a₁ ≤ a₂ ≤ ⋯ ≤ aₙ ≤ ⋯ ≤ M` is a non-decreasing sequence with an upper bound `M ∈ ℝ`. Then `lim_{n→∞} aₙ` exists.
   [一個遞增有上界的數列有極限]
2. Suppose `a₁ ≥ a₂ ≥ ⋯ ≥ aₙ ≥ ⋯ ≥ L` is a non-increasing sequence with a lower bound `L ∈ ℝ`. Then `lim_{n→∞} aₙ` exists.
   [一個遞減有下界的數列有極限]

---

## [e1] e^x < +∞ for all x > 0

For fixed `x > 0`, let `n₀ ∈ ℕ` such that `n₀ > 2x`.

We observe that
`e^x = Σ_{n=0}^{n₀} xⁿ/n!  +  Σ_{n=n₀+1}^∞ xⁿ/n!  = (I) + (II)`.

`(II) = (x^(n₀)/n₀!) · Σ_{n=n₀+1}^∞ [ x/(n₀+1) · x/(n₀+2) · ⋯ · x/n ]`
`     ≤ (x^(n₀)/n₀!) · Σ_{n=n₀+1}^∞ (1/2)^(n−n₀)`
`     ≤ x^(n₀)/n₀!`.

(每個因子 `x/(n₀+j) ≤ x/n₀ < 1/2`，因 `n₀ > 2x`；幾何尾和 `Σ_{n>n₀}(1/2)^(n−n₀) = 1`。)

Hence,
`e^x ≤ Σ_{n=0}^{n₀} xⁿ/n!  +  x^(n₀)/n₀!  < +∞`   …(3).

**Note:** (3) holds true for any `x > 0`, `n₀ ∈ ℕ` such that `n₀ > 2x`.

In particular, we see that for `0 < x < L` and `k > n₀ > 2L`, we have
`0 ≤ e^x − Σ_{n=0}^{k} xⁿ/n!  ≤  L^k/k!  ≤  (L^(n₀)/n₀!)·(1/2)^(k−n₀)`.

(這條部分和尾界是 §4.2 連續性／指數律證明反覆援用的依賴；`Σ_{n=0}^{k} xⁿ/n!` 手稿後文記為 `P_k(x)`。)

---

## §4.1 / §4.2 boundary

手稿接著寫 **[e2] `e^x` is a continuous function for x > 0**（`lim_{x→x₀} e^x = e^{x₀}`）——**這是 §4.2 的開頭**，不屬本 seed。§4.2 seed 見 [`seed_s42.md`](../../../authoring/direction_layer/test/seed_s42.md)。

---

## 手稿刻意省略／特徵（忠實記錄）

- **`a^r`（無理數指數）只提問、未建構**：手稿拋出問題後改以 series 定義 `e^x`，一般指數 `a^x = e^(x ln a)` 留到後面（→ handout §4.5）。
- **`e` 的數值（≈2.71828）、部分和表、收斂圖：無。** 手稿不算 `e`、不畫圖。
- **`e^0 = 1` / `x = 0` / `x < 0`：本節不處理**（定義只對 `x > 0`；`x < 0` 延拓在 §4.2 經絕對收斂）。
- worked example：**0 個**。圖：**0**。動機散文：**極少**。caution／strategy／named-result 索引：**無**。
- 記號：有理數指數 `a^q = (a^(1/m))ⁿ`；二項式尚未出現（§4.2 才用，手稿記 `Cⁿ_k`）；部分和在 §4.1 以 `Σ_{n=0}^{k}` 寫出、§4.2 起記 `P_k`。

---

## 對照 ground truth（評分用，非手稿）

已簽核 `legacy/tex_handout/chapters/ch04_exponential_logarithm.tex` §4.1（L17–166）對同一手稿做了以下 **expansion**（非手稿原有，方向由 brief §③ 決定是否採）：
- `a^x = e^(x ln a)` 的「limit-of-rationals 較笨重 → 改走 series」動機散文；
- **The case `x = 0` and the value of `e`** 子節：`e^0 = 1`、`e = e¹ = Σ 1/n! ≈ 2.71828`、**部分和 worked example**（`P_k(1)`, k=0…5）；
- **partial-sum 收斂 figure**（`P_k(x)`, k=1…4 → 光滑 `e^x`）；
- **completeness** 升格具名 Theorem＋一個 `ℝ` vs `ℚ` 的 remark；
- **geometric-tail strategy box**；**"series defines, doesn't derive" caution**。

本 seed 是手稿原貌（pp.1–3）；上述加法皆「待 ③ 方向閘核可」的提案（見 PLAN D5/D6）。

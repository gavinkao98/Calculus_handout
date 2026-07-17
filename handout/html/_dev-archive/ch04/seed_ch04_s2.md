# Seed — §4.2 Continuity and the Exponent Law for e^x

> stage ① 產物。Transcribed from the handwritten manuscript `2023-11-4-ExponentialFunction`,
> **pp.3–10** (from `[e2]` "e^x is continuous for x>0", through the boxed exponent law
> `e^x e^y = e^{x+y}` and the Summary; the next item "§ The derivative of the exponential
> function" begins §4.3).
> Manuscript has **no separate section title** here — it is the continuation of the exponential
> construction (handout splits it into §4.2 per ROADMAP).
> Faithful to the manuscript: structure, order, notation, and deliberate omissions preserved.
> seed 語法＝輕量可讀（反引號行內＋Unicode；見 CONTENT_DIRECTION ① / `seed_ch04_s1.md`）。漂亮 KaTeX 留給 ④。可疑／非標準處標 **[請查核]**。
> **數學 cross-check（非手稿）**：legacy `ch04_exponential_logarithm.tex` 的 §4.2 段（LaTeX→HTML 轉移前已簽核的整章；D1：僅盲算對賬，不照抄散文／結構）。
> **重跑註記（2026-06-21）**：舊 §4.2 POC `sec-4-2.html` 與舊 seed `seed_s42.md` 已刪除；本 seed 為從手稿重新轉錄、併進正式 ch04 章流程的全新 ① 產物（取代舊 test-pipeline 首跑）。

---

## §4.1 依賴（承前；非本節新內容，僅備援引）

§4.1 在 x>0 收斂結尾建立的**部分和尾界**，§4.2 全程反覆援用：
記 `P_k(x) := Σ_{n=0}^{k} xⁿ/n!`（手稿自 §4.2 起以 `P_k` 標部分和）。
對 `0 < x < L` 與 `k > n₀ > 2L`，
`0 ≤ e^x − P_k(x) ≤ L^k/k! ≤ (L^(n₀)/n₀!)·(1/2)^(k−n₀)`   …(∗)。

(因子比較 `L/j < 1/2`（`j > n₀ > 2L`）給出幾何衰減 `(1/2)^(k−n₀)`。)

---

## [e2] e^x is a continuous function for x > 0

To show `lim_{x→x₀} e^x = e^{x₀}`, `x₀ > 0`:

For given `ε > 0`, choose `k > n₀ > 2(x₀+1)` such that
`((x₀+1)^(n₀)/n₀!)·(1/2)^(k−n₀) < ε`.

Since `P_k(x) := Σ_{n=0}^{k} xⁿ/n!` is a continuous function
[any polynomial is a continuous function], `∃ δ > 0` with `δ < min{x₀/2, 1/2}` such that
`|P_k(x) − P_k(x₀)| < ε`   provided   `|x − x₀| < δ`.

Now:
`e^x − e^{x₀} = (e^x − P_k(x)) + (P_k(x) − P_k(x₀)) + (P_k(x₀) − e^{x₀})`.

Hence, for `|x − x₀| < δ = min{x₀/2, 1/2}`,
`|e^x − e^{x₀}|`
` ≤ |e^x − P_k(x)| + |P_k(x) − P_k(x₀)| + |P_k(x₀) − e^{x₀}|`
` ≤ ((x₀+1)^(n₀)/n₀!)·(1/2)^(k−n₀)  +  ε  +  ((x₀+1)^(n₀)/n₀!)·(1/2)^(k−n₀)`
` < 3ε`.

This proves that `lim_{x→x₀} e^x = e^{x₀}`. Hence, `e^x` is a continuous function for `x > 0`.

(兩個端點項用 (∗) 控制：`x`, `x₀` 均落在 `(0, x₀+1)` 內，故 `L = x₀+1`、`n₀ > 2(x₀+1)`，兩處 `|e^· − P_k(·)|` 各 `< ε` 的尾界部分。中間項用 `P_k` 的多項式連續。)

---

## [e3] 0 < e^y < +∞ for y < 0

(手稿以此標明：對 `y < 0`，`e^y` 仍有定義且有限、為正。其有限性／收斂由下方 (△) 絕對收斂性質提供——見後文「We observe that (1)」一步 `|e^y| ≤ e^(|y|) < +∞`。)

**[請查核]**：手稿在此僅陳述 `0 < e^y < +∞`；正性 `e^y > 0`（y<0）手稿未在此處單獨證明（落地時可由指數律 `e^y e^(−y) = e^0` 或級數逐項補述——屬 ④ 方向）。

---

## (△) Property — absolute convergence implies convergence

**(△) Property:** If `Σ_{n=1}^∞ |aₙ| < +∞`, then `Σ_{n=1}^∞ aₙ` converges.

**Note:** when we say `Σ_{n=1}^∞ aₙ` converges, this means `Sₖ = Σ_{n=1}^{k} aₙ` is a convergent
sequence, i.e. `lim_{k→∞} (Σ_{n=1}^{k} aₙ)` exists.

### Def — Cauchy sequence

A sequence `{aₙ}_{n=1}^∞` is called a **Cauchy sequence** if for any `ε > 0`, `∃ N₀ ∈ ℕ`
such that `|aₘ − aₙ| < ε` for any `m, n ≥ N₀`.

### Thm — convergent ⟺ Cauchy

A sequence `{aₙ}_{n=1}^∞` is a convergent sequence **if and only if** `{aₙ}_{n=1}^∞` is a
Cauchy sequence.

> **手稿明寫 punt：** "For the moment, we shall not prove this theorem."
> （ROADMAP resolved 方向 D3①：handout 版**展開**成完整 Bolzano–Weierstrass ＋ monotone-subsequence
> 證明——超出手稿、user-directed 2026-04-27。屬 ② brief／④ draft 的擴增，非本 seed 轉錄範圍。）

### Proof of (△) using Cauchy

To show (△) property, set `Sₙ = Σ_{k=1}^{n} aₖ`, where `Σ_{k=1}^∞ |aₖ| < +∞`.

Since `Σ_{k=1}^∞ |aₖ| < +∞`, for any `ε > 0`, `∃ N₀ ∈ ℕ` such that
`Σ_{k=N₀+1}^∞ |aₖ| < ε`.

Therefore for `m > n > N₀`,
`|Sₘ − Sₙ| ≤ Σ_{k=n+1}^{m} |aₖ| ≤ Σ_{k=N₀+1}^∞ |aₖ| < ε`.

This proves that `{Sₙ}_{n=1}^∞` is a Cauchy sequence. Hence, `Σ_{k=1}^∞ aₖ` converges. ∎

---

## Exponent law: e^x · e^y = e^{x+y}

> 以下假設 `x, y ∈ [−L, L]`，`k > n₀ > 8L`。

### We observe that

**(1)** `|e^y| ≤ |Σ_{n=0}^∞ yⁿ/n!| ≤ Σ_{n=0}^∞ |y|ⁿ/n! ≤ e^(|y|) < +∞`,   and
`|e^y − P_k(y)| ≤ Σ_{n=k+1}^∞ |y|ⁿ/n! ≤ |y|^k/k!`   if `k > n₀ > 2|y|`.

(此步同時給出 [e3] 的有限性：`Σ|y|ⁿ/n! = e^(|y|) < ∞` ⟹ 由 (△) 級數絕對收斂 ⟹ `e^y` 對 `y<0` 有定義。)

**(2)** `P_k(x)·P_k(y) = (Σ_{n=0}^{k} xⁿ/n!)(Σ_{n=0}^{k} yⁿ/n!)`
` = Σ_{ℓ=0}^{k} Σ_{m=0}^{ℓ} [1/(m!(ℓ−m)!)] xᵐ y^(ℓ−m)`   … (I)
` + Σ_{j=1}^{k} Σ_{m=j}^{k} [1/(m!(k+j−m)!)] xᵐ y^(k+j−m)`   … (II)

### 二項式定理 (Binomial Theorem)

**Notation:** `Cⁿ_k := n!/(k!(n−k)!)`, `k, n ∈ ℕ` and `k ≤ n`.
（D8：本書全程改用 `\binom{n}{k}`；首見處 cross-ref 手稿記號 `Cⁿ_k`。）

`(x + y)ⁿ = Σ_{k=0}^{n} Cⁿ_k · xᵏ y^(n−k)`.

### (I) = P_k(x+y)

`(I) = Σ_{ℓ=0}^{k} Σ_{m=0}^{ℓ} [1/(m!(ℓ−m)!)] xᵐ y^(ℓ−m)`
`    = Σ_{ℓ=0}^{k} (1/ℓ!) Σ_{m=0}^{ℓ} [ℓ!/(m!(ℓ−m)!)] xᵐ y^(ℓ−m)`
`    = Σ_{ℓ=0}^{k} (1/ℓ!) Σ_{m=0}^{ℓ} C^ℓ_m xᵐ y^(ℓ−m)`
`    = Σ_{ℓ=0}^{k} (1/ℓ!) (x+y)^ℓ  =  P_k(x+y)`.

### (II) tail bound

`|(II)| = |Σ_{j=1}^{k} Σ_{m=j}^{k} [1/(m!(k+j−m)!)] xᵐ y^(k+j−m)|`
`      ≤ Σ_{ℓ=k+1}^{2k} Σ_{m=0}^{ℓ} [1/(m!(ℓ−m)!)] |x|ᵐ |y|^(ℓ−m)`
`      ≤ Σ_{ℓ=k+1}^{2k} (1/ℓ!) (|x|+|y|)^ℓ`
`      ≤ (1/k!) (|x|+|y|)^k`
`      ≤ (2L)^(n₀)/n₀! · (1/2)^(k−n₀)`.

（末步用 `|x|+|y| ≤ 2L` 與 `k > n₀ > 8L`。**[請查核]** 中間步 `Σ_{ℓ=k+1}^{2k}(1/ℓ!)(|x|+|y|)^ℓ ≤ (1/k!)(|x|+|y|)^k` 的係數收法手稿較簡略。）

Hence,
`|P_k(x)·P_k(y) − P_k(x+y)| ≤ (2L)^(n₀)/n₀! · (1/2)^(k−n₀)`.

**Note also** (同 (∗)，對 `|x| ≤ L`):
`|e^x − P_k(x)| ≤ L^k/k! ≤ (L^(n₀)/n₀!) · (1/2)^(k−n₀)`.

### Four-term split → limit

`e^x e^y − e^{x+y}`
` = (e^x − P_k(x)) e^y  +  P_k(x) (e^y − P_k(y))  +  (P_k(x) P_k(y) − P_k(x+y))  +  (P_k(x+y) − e^{x+y})`

implies
`|e^x e^y − e^{x+y}|`
` ≤ (L^(n₀)/n₀!)(1/2)^(k−n₀) · e^L`
` + e^L · (L^(n₀)/n₀!)(1/2)^(k−n₀)`
` + (2L)^(n₀)/n₀! · (1/2)^(k−n₀)`
` + (2L)^(n₀)/n₀! · (1/2)^(k−n₀)`.

By taking the limit `k → ∞`, we see that `e^x · e^y = e^{x+y}` for `x, y ∈ [−L, L]`.

Let `L → ∞`, we see that
**`e^x · e^y = e^{x+y}` holds for all `x, y ∈ ℝ`.**

---

## Summary (手稿原文)

`e^x := Σ_{n=0}^∞ xⁿ/n!`,  `x ∈ ℝ`  is a continuous function and `e^x · e^y = e^{x+y}`
for all `x, y ∈ ℝ`.

（注意：Summary 把 `e^x` 的定義域由 §4.1 的 `x>0` **延拓到整個 ℝ**——`x<0` 經 (△) 絕對收斂取得定義，連續性與指數律隨之對全 ℝ 成立。手稿在 §4.2 內只顯式證了 x>0 的連續，全 ℝ 連續性在 Summary 處一併宣告。**[請查核]**：是否要在 handout 補一條全 ℝ 連續的明說 Theorem，屬 ② brief 方向。）

---

## §4.2 / §4.3 boundary

手稿接著寫 **§ The derivative of the exponential function**：差分商
`(e^{x+h} − e^x)/h = ((e^h − 1)/h) e^x`——**這是 §4.3 的開頭**，不屬本 seed。

---

## 手稿刻意省略／特徵（忠實記錄）

- **收斂⟺Cauchy 定理手稿不證**（"we shall not prove"）。handout 版依 ROADMAP resolved 展開完整 Bolzano–Weierstrass（D3①，屬 ②/④ 擴增）。
- **指數律手稿走完整推導**（二項式 + 雙和拆 (I)(II) + 四項拆 + 雙重取極限 k→∞、L→∞），非 outline。ROADMAP D3② 亦要求 handout 寫**完整 6 步**，與手稿一致。
- **x<0 的連續性無獨立證明**：手稿只證 x>0 連續（[e2]），`x<0` 經 (△) 取得 `e^y` 定義與有限性，全 ℝ 連續在 Summary 一併宣告。
- **`e^y > 0`（y<0）的正性**手稿未在 [e3] 處單獨證（見上 [請查核]）。
- worked example：**0 個**。圖：**0**。動機散文：**極少**。caution／strategy／named-result 索引：**無**（具名化 Theorem/Def 屬 ④ 落地）。
- 記號：部分和 `P_k(x)`；二項式手稿記 `Cⁿ_k`（→ 本書 `\binom`，D8）；尾界常數型態 `(C^(n₀)/n₀!)(1/2)^(k−n₀)`，`C ∈ {L, x₀+1, 2L}` 視場景。

---

## 對照 ground truth（評分用，非手稿）

已簽核 `legacy/tex_handout/chapters/ch04_exponential_logarithm.tex` 的 §4.2 段是同一手稿的 LaTeX→HTML 前簽核版，**僅作盲算對賬的 ground truth**（D1），不照抄其散文／結構。落地時新具名結果（Bolzano–Weierstrass、收斂⟺Cauchy 等價）一律人工查核。

**ROADMAP 已 resolved 的 §4.2 方向（待 ③ 方向閘確認沿用，PLAN D3）：**
- ① 收斂⟺Cauchy **展開**成完整 Bolzano–Weierstrass ＋ monotone-subsequence（超出手稿）。
- ② 指數律寫**完整 6 步**（與手稿一致，已是完整推導）。

**§4.1 落地後的編號接續（PLAN §5 ledger）：** §4.1 已用到 Definition 4.1、Theorem 4.1（Completeness）／4.2（convergence x>0）、Strategy 4.1、Example 4.1、Figure 4.1、Remark 4.1。**§4.2 因此自 Theorem 4.3、Definition 4.2 起編號。** 本 seed 為手稿原貌（pp.3–10）；具名化與編號落在 ④。

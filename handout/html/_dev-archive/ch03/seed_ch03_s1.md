# Seed — §3.1 Derivatives of the Sine and Cosine Functions

> Transcribed from the handwritten manuscript `2023-10-28-chainRule` (pp. 1–9, up to
> "This proves `d/dx cos x = −sin x`"; the next section 「§ 乘法規則與連鎖規則」= §3.2 starts mid-p.9).
> Manuscript's own section title: 「§ 三角函數的微分」(Differentiation of trigonometric functions).
> Faithful to the manuscript: structure, order, notation, and deliberate omissions preserved.
> seed 語法＝輕量可讀（反引號行內＋Unicode；見 RULE.md ①）。漂亮 KaTeX 留給 ④。可疑／非標準處標 **[請查核]**。

---

## Opening — the difference quotient for sin

Recall `f'(x₀) := lim_{h→0} (f(x₀+h) − f(x₀))/h`, if the limit exists.

Formal calculation. Consider the difference quotient [差分商] for `sin`:
`(sin(x+h) − sin(x))/h = 2 sin(h/2) cos(x + h/2) / h = (sin(h/2)/(h/2)) · cos(x + h/2)`.

To evaluate `lim_{h→0} (sin(x+h) − sin(x))/h`, we must calculate
- (i) `lim_{h→0} sin(h/2)/(h/2)`
- (ii) `lim_{h→0} cos(x + h/2)`

## Part (i) — even function reduction + the Squeezing Lemma

Set `θ = h/2`. Since `g(θ) := sin θ / θ` (θ≠0) is an even function, to evaluate `lim_{θ→0} g(θ)`
we only need the case `θ > 0`, `θ ↘ 0`.

**Squeezing Lemma [夾擠原理].** Suppose `g₁(x) ≤ g(x) ≤ g₂(x)` for either
- (1) `x > M`, or
- (2) `x ∈ (x₀ − r, x₀ + r)`, `r > 0`;

and either
- (1) `lim_{x→∞} g₁(x) = lim_{x→∞} g₂(x) = L`, or
- (2) `lim_{x↘x₀} g₁(x) = lim_{x↘x₀} g₂(x) = Q`.

then
- (1) `lim_{x→∞} g(x) = L`, or
- (2) `lim_{x↘x₀} g(x) = Q`.

> 手稿在此**完整重述**夾擠原理（兩種形式：`x→∞` 與 `x↘x₀`）。[ROADMAP open question：§1.5 已有 squeeze 定理 → 是否重述／只 cross-ref，待 ③ 決定]

**Geometric inequality (unit circle).** Figure: unit circle centered `O`, radius `1`; `A` on the
circle at the x-axis; `B` on the circle at angle `θ`; `C` on the tangent line at `A`. The line
⟷AB is the tangent that contacts circle `O` at `A` [AB 是圓 O 的切線]. Denote areas
`a_{sector OAB}`, `a_{△ABC}`, `a_{△OAB}`.

From the nesting of the three regions:
`½ sin θ ≤ ½ θ ≤ ½ tan θ = ½ · (sin θ / cos θ)`
`⟹ 0 ≤ cos θ ≤ sin θ / θ ≤ 1` ... (1)

> **[請查核]** 手稿把面積關係寫成 `△ABC ⊃ Sector OAB ⊃ △OAB`，並列 `a_{△ABC} ≤ a_{sector OAB} ≤ a_{△OAB}`。
> 但「包含」方向與 `≤` 方向、以及哪個三角形對應 `½ sin θ`／哪個對應 `½ tan θ`，標示看來**不一致**
> （標準是：內接 `△OAB = ½ sin θ` ≤ 扇形 `½ θ` ≤ 含切線的外三角形 `½ tan θ`）。**最終不等式
> `cos θ ≤ sin θ / θ ≤ 1` 為標準且正確。** 請你對掃描核對三角形命名與面積排序的書寫。

In particular: `0 ≤ |sin θ| ≤ |θ|`.

## A continuity example (squeeze)

**Example.** Show that `lim_{x→0} sin x = 0`.
Set `g₁(x) = 0`, `g(x) = |sin x|`, `g₂(x) = |x|`. Since `lim_{x→0} |x| = 0` and `lim_{x→0} 0 = 0`,
by the squeezing lemma `lim_{x→0} |sin x| = 0`. Hence `lim_{x→0} sin x = 0`.

## [Concept] Continuous function

We say `f(x)` is **continuous at `x₀`** if `lim_{x→x₀} f(x) = f(x₀)`.

Examples:
- ① `f(x) = 1 if x ∈ ℚ, 0 if x ∉ ℚ` (ℚ = 有理數) is **nowhere continuous** (對任何實數點 `x₀`，`f` 在 `x₀` 都不連續).
- ② `f(x) = x` is continuous at every `x₀ ∈ ℝ`.
- ③ `f(x) = cos x` is continuous at every `x₀ ∈ ℝ`.

**Proof of ③.** `cos x − cos x₀ = −2 sin((x − x₀)/2) sin((x + x₀)/2)`
`⟹ |cos x − cos x₀| ≤ |−2 sin((x − x₀)/2) sin((x + x₀)/2)| ≤ 2 |sin((x − x₀)/2)|`.
Set `θ = (x − x₀)/2`: `lim_{x→x₀} |sin((x − x₀)/2)| = lim_{θ→0} |sin θ| = 0`.
By the squeezing lemma `lim_{x→x₀} |cos x − cos x₀| = 0`, so `lim_{x→x₀} cos x = cos x₀` for any
`x₀ ∈ ℝ`. Hence `cos x` is continuous for all `x ∈ ℝ`.

## Back to (1) — the fundamental limit `sin θ / θ → 1`

Back to (1): `cos θ ≤ sin θ / θ ≤ 1` for `θ ∈ (0, π/2)`.

> Note: `sin θ / θ` is an even function, since both `θ` and `sin θ` are odd.

**[Concept] odd / even function.** `f` is odd if `f(−x) = −f(x)`; `f` is even if `f(−x) = f(x)`.

By the continuity of cosine, `lim_{θ→0} cos θ = cos 0 = 1`. Again by the squeezing lemma:
`lim_{θ→0} sin θ / θ = 1`.

## Assemble `d/dx sin x`

`lim_{h→0} (sin(x+h) − sin(x))/h = lim_{h→0} (sin(h/2)/(h/2)) · cos(x + h/2) = 1 · cos x = cos x`,
where we used `lim_{θ→0} sin θ / θ = 1` and that `cos x` is continuous at every `x ∈ ℝ`.

To sum up: **`d/dx sin x = cos x`** for all `x ∈ ℝ`.

## `d/dx cos x`

Consider `(cos(x+h) − cos x)/h = −2 sin(h/2) sin(x + h/2) / h = −(sin(h/2)/(h/2)) · sin(x + h/2)`.

**Claim: `sin x` is continuous at every `x ∈ ℝ`.**
Proof. `sin(x+h) − sin x = 2 sin(h/2) cos(x + h/2)`
`0 ≤ |sin(x+h) − sin x| ≤ 2 |sin(h/2)| |cos(x + h/2)| ≤ 2 |sin(h/2)|`.
Note `lim_{h→0} |sin(h/2)| = 0`. By the squeezing lemma `lim_{h→0} |sin(x+h) − sin x| = 0`. This
proves `sin x` is continuous at every `x ∈ ℝ`.

Now
`lim_{h→0} (cos(x+h) − cos x)/h = lim_{h→0} −(sin(h/2)/(h/2)) · sin(x + h/2)`
`= −lim_{h→0} sin(h/2)/(h/2) · lim_{h→0} sin(x + h/2) = −1 · sin x = −sin x`.

This proves **`d/dx cos x = −sin x`**.

---

## 手稿盤點摘要 / 刻意省略（給 ②③，非手稿正文）

手稿 §3.1 **有**：sin 差分商 → 夾擠原理（全述）→ 扇形/三角形幾何不等式 `(1)` → `lim sin x = 0` 例 →
連續定義＋三例（Dirichlet 處處不連續、`x`、`cos x` 含證明）→ odd/even 定義 → `lim sin θ/θ = 1`
→ `sin′ = cos` → sin 連續性 Claim ＋證 → `cos′ = −sin`。

手稿 §3.1 正文**無**（待 ③ 決定是否補；詳見 `PLAN-ch03.md` D1/D2）：
- **`d/dx tan x`** —— §3.1 正文無，但**手稿 Homework (2)(i) 有**（`d/dx tan x`, `x ∈ [0, π/2)`）。ROADMAP 列為 §3.1 core skill「derive d/dx tan x using the quotient rule」→ 把手稿 HW 的 tan′ **升格為 §3.1 worked example**（manuscript-faithful、非杜撰）。
- **`lim_{θ→0} (1 − cos θ)/θ = 0`** —— 全手稿（含 HW）皆無；ROADMAP 學習目標列了 → 真 expansion 候選。
- worked example（除上述極限/連續證明外，無「給函數求導」型例題）、strategy box、`sin(g(x))` 等鏈鎖應用（屬 §3.2）、具名人物／歷史。

> **轉錄忠實度待你核對（①-verify）**：請逐字對掃描 pp.1–9，特別是上面 **[請查核]** 的面積排序。確認後才進 ② 方向 brief。

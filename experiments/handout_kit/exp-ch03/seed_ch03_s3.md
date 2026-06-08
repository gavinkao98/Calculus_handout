# Seed — §3.3 Applications of the Chain Rule

> Transcribed from the handwritten manuscript `2023-10-28-chainRule`:
> **pp. 12–14** (the three worked applications ①②③, placed in the manuscript *before*
> the chain-rule proof) and **pp. 21–22** (Homework). The manuscript has no section
> title of its own for these; they sit under 「§ 乘法規則與連鎖規則」(= §3.2/§3.3).
> Faithful to the manuscript: structure, order, notation, and deliberate omissions preserved.
> seed 語法＝輕量可讀（反引號行內＋Unicode；見 RULE.md ①）。漂亮 KaTeX 留給 ④。可疑／非標準處標 **[請查核]**。
>
> **轉錄忠實度交叉檢查（① intake）：** 三份獨立盲讀（各自重讀 PDF pp.11–15＋20–22）＋我自己的讀法對賬。
> 應用①②③ 與 Homework (1)(2)(3) **四方一致、無歧異**；唯一高不確定項 HW(4) 多項式次方，已於 ①-verify 釐清為手稿筆誤（見該處註）。**①-verify 已過（2026-06-08）。**

---

## Application ① — `d/dx ln x = 1/x`  (x > 0)

We know `d/dx eˣ = eˣ`, and `x = ln eˣ = e^(ln x)`.

Let `g(x) = ln x` and `f(y) = eʸ`; set `P(x) = f(g(x))`.

By the chain rule:
`1 = d/dx x = dP/dx = g'(x) · f'(g(x)) = g'(x) · e^(ln x) = x · g'(x)`   (x > 0)
`⟹ d/dx ln x = g'(x) = 1/x`   (x > 0).

## Application ② — `d/dx xˣ = (1 + ln x) xˣ`  (x > 0)  [logarithmic differentiation]

Let `W(x) = xˣ`  (x > 0). Find `dW/dx`.

Set `g(x) = ln W(x) = x ln x`. Taking the derivatives on both sides, by the chain rule:
`(d/dx W(x)) · (d/dy ln y)|_{y = W(x)} = d/dx (x ln x)`
`⟹ W'(x) · 1/W(x) = ln x + 1`
`⟹ W'(x) = (1 + ln x) xˣ`   (x > 0).

## Application ③ — `d/dy arcsin y = 1/√(1 − y²)`  (y ∈ (−1, 1))

> **Figure (手稿附圖):** left, `y = sin x` restricted to `x ∈ [−π/2, π/2]`; right, the inverse
> `x = sin⁻¹ y` obtained by reflecting / swapping axes (y on the horizontal axis, `−1 ≤ y ≤ 1`;
> x on the vertical axis, `−π/2 ≤ x ≤ π/2`).

For `−1 ≤ y ≤ 1`, we define `sin⁻¹ y = arcsin y = x`  if  `y = sin x`  and  `x ∈ [−π/2, π/2]`.
So `arcsin y` is the inverse function of `sin x`.

You may check that `sin(sin⁻¹ y) = y`  and  `sin⁻¹(sin x) = x`,  for `y ∈ [−1, 1]`, `x ∈ [−π/2, π/2]`.

Set `f(x) = sin x`, `g(y) = sin⁻¹ y`; then `x = g(f(x)) = sin⁻¹(sin x)`.

Taking the derivatives on both sides:
`1 = f'(x) · g'(f(x)) = cos x · (d/dy sin⁻¹ y)|_{y = sin x}`
`⟹ (d/dy sin⁻¹ y)|_{y = sin x} = 1/cos x = 1/√(1 − sin²x) = 1/√(1 − y²)`.

Note `cos x ≥ 0` for `x ∈ [−π/2, π/2]`. Hence for `y ∈ (−1, 1)`:
`d/dy arcsin y = 1/√(1 − y²)`.

---

## Homework  (手稿 pp. 21–22)

**(1)**
> **Figure (手稿附圖):** left, `y = cos x` on `x ∈ [0, π]` (from `1` down to `−1`); right, the inverse
> `x = cos⁻¹ y` by axis swap (y on the horizontal axis, `−1 ≤ y ≤ 1`; x on the vertical axis,
> `0 ≤ x ≤ π`, with `π/2` marked).

For `y ∈ [−1, 1]`, we define `arccos y` to be the number `x ∈ [0, π]` such that `cos x = y`.
We denote `cos⁻¹ y = x`. So `cos⁻¹ y = arccos y` is the inverse function of cosine.
`cos(cos⁻¹ y) = y = cos⁻¹(cos y)`.

> **①-verify 已決（2026-06-08，掃描確認）：** 手稿右側逐字即 `cos(cos⁻¹ y) = y = cos⁻¹(cos y)`
> （變數用 `y`、未標限定域）——使用者重送掃描確認，**忠實轉錄無誤、逐字保留手稿原文**。唯
> `cos⁻¹(cos y) = y` 僅在 `y ∈ [0, π]` 成立（嚴格應作 `cos⁻¹(cos x) = x`, `x ∈ [0, π]`，對應 arcsin 例的
> `sin⁻¹(sin x) = x`, `x ∈ [−π/2, π/2]`）。此域微妙處留待 ④ 擴寫以散文／caution 補正，不改手稿轉錄。

Now, you find `d/dy cos⁻¹ y`  for `y ∈ (−1, 1)`.

**(2)** Find
- (i)   `d/dx tan x`  for `x ∈ [0, π/2)`.
- (ii)  `d/dx sec x`  for `x ∈ [0, π/2)`.
- (iii) `d/dx (x ln x − x)`  for `x > 0`.
- (iv)  `d/dx (2ˣ)`  for `x ∈ ℝ`.

**(3)** `f(x) = x³ − 3x² + 2`. Find `f'(x)`. Find all the roots of `f'(x) = 0`.

**(4)** `f(x) = x⁴ − 4x³ + 6x² − 4x + 1 = (x − 1)⁴`. Find `f'(x)`. Find all the roots of `f(x) = 0`. Find all the roots of `f'(x) = 0`.

> **①-verify 已決（2026-06-08，使用者授權更正手稿筆誤）：** 手稿此處逐字寫成 `x³ − 4x² + 6x² − 4x + 1`
> （首項 `x³`、且重複 `x²` 項；三份獨立轉錄＋我的讀法一致），為書寫筆誤。係數序列 `1, −4, 6, −4, 1` 即 `(x−1)⁴`
> 的二項式係數；使用者確認本意為 `f(x) = x⁴ − 4x³ + 6x² − 4x + 1 = (x−1)⁴`，已據此更正（保留本記錄以存稽核軌跡）。
> 與本題「同時求 `f=0` 與 `f'=0` 的根」一致：`(x−1)⁴` 的 `f` 與 `f'` 皆唯一根 `x = 1`（呼應 (3) 只問 `f'` 根）。

---

## 手稿盤點摘要 / 刻意省略（給 ②③，非手稿正文）

手稿 §3.3（應用）**有**：
- 應用① `d/dx ln x = 1/x` (x>0)，經 `x = e^(ln x)` ＋ chain rule（用 `(eˣ)' = eˣ`）。
- 應用② `d/dx xˣ = (1 + ln x) xˣ` (x>0)，log differentiation（`g = ln W = x ln x` 兩邊取導）。
- 應用③ `d/dy arcsin y = 1/√(1 − y²)` (y∈(−1,1))，經 composition identity `sin⁻¹(sin x) = x` 取導，配 `cos x ≥ 0` on `[−π/2, π/2]`。
- Homework：arccos 定義 ＋ `d/dy arccos y`；`tan x`、`sec x`、`(x ln x − x)'`、`2ˣ'`；兩個多項式 `f'`／求根。

**手稿頁序：** 應用①②③ 置於 chain rule **證明之前**（pp.12–14，證明在 pp.15–20）。handout 依 **D7** 重排到 §3.2 證明**之後**（§3.3 才應用）——屬 ④ 排版決策，**本 seed 僅忠實轉錄、保留手稿原順序**。

**刻意省略 / 待 ② 決定（依 PLAN-ch03.md D8/D9/D10）：**
- **D8**：`ln x` 在此**非正式當「eˣ 的反函數」用**（`e^(ln x) = x` 取導）；嚴謹建構延 **Ch4 §4.5**，一句 forward-note 標依賴。
- **D10**：arcsin／xˣ 本質是 implicit-diff 包裝成 composition-identity chain rule——**照手稿走 composition identity，不引入 implicit-diff 框架**。
- **D9（升格 worked example 候選，③ 逐一批准）**：HW 的 `arccos'`、`(x ln x − x)' = ln x`、`2ˣ' = 2ˣ ln 2`（`2ˣ = e^(x ln 2)` ⟹ `2ˣ ln 2`）。
  - `d/dx tan x` 已歸 **§3.1**（D1）；`d/dx sec x` 已歸 **§3.1 Example 3.2(b)**（③ 移入）——**§3.3 不重做**。
  - 多項式 `f'`／求根（HW 3,4）屬代數練習，可作 chain/power 計算錨或 deferred 習題；**不自創 bare your-turn／無解練習**。
- **arcsin 域 caution（ROADMAP pitfall）**：`1/√(1 − y²)` 僅在 `y ∈ (−1, 1)` 成立（端點 `±1` 為垂直切線）。
- **strategy（ROADMAP 指派）**：chain-rule decomposition、logarithmic differentiation 兩個 strategy box（後者承 ② log-diff）。

> **①-verify 已過（2026-06-08）：** 使用者對掃描核對 **pp.12–14**（應用①②③）＋ **pp.21–22**（Homework）。
> HW(4) 多項式經授權更正手稿筆誤為 `(x−1)⁴`；HW(1) arccos 恆等式確認逐字無誤（域微妙處留待 ④）。
> 其餘四方一致、無歧異。已進 ② 方向 brief。

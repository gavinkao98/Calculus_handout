# Seed — §4.4 Rolle's Theorem and the Mean Value Theorem

> stage ① 產物。Transcribed from the handwritten manuscript `2023-11-4-ExponentialFunction`,
> **pp.11–18** (the section the manuscript heads "§ Rolle's Theorem", beginning right after
> `d/dx e^x = e^x` on p.11 and running through the monotonicity Corollary + Examples ending
> with "[e^x is strictly increasing for all x ∈ ℝ]" on p.18; the next item "§ Logarithmic
> function" begins §4.5).
> Manuscript heads this block with its own title "§ Rolle's Theorem" (handout maps it to
> §4.4 "Rolle's Theorem and the Mean Value Theorem" per ROADMAP/PLAN §1).
> Faithful to the manuscript: structure, order, notation, and deliberate omissions preserved.
> seed 語法＝輕量可讀（反引號行內＋Unicode；見 CONTENT_DIRECTION ① / `seed_ch04_s3.md`）。漂亮 KaTeX 留給 ④。可疑／非標準處標 **[請查核]**。
> **數學 cross-check（非手稿）**：legacy `ch04_exponential_logarithm.tex` §4.4 段（`\section{Rolle's Theorem and the Mean Value Theorem}`，`sec:rolle-and-mvt`，lines 538–696）＋其 §4.5 開頭的 monotonicity corollary（`cor:monotonicity`，lines 705–727；legacy 把推論放 §4.5，手稿＋PLAN 放 §4.4——見下）。D1：僅盲算對賬，不照抄散文／結構。

---

## §4.3 依賴（承前；非本節新內容，僅備援引）

§4.4 用到前一節一件既成事實，及 Ch2 的導數定義：

1. **導數定義（Ch2）**：`f'(x) = lim_{h→0} (f(x+h)−f(x))/h`。Thm A 的證明把這個 difference quotient 拆成單邊極限。
2. **§4.3（Theorem 4.8）**：`d/dx e^x = e^x`。本節**最後一個 Example** 用它（`(e^x)' = e^x > 0`）推出 `e^x` strictly increasing——這正是 §4.5 建構 `ln x`（`e^x` 反函數）所需的單調性。
3. **§4.4 → §4.5 交棒**：本節結尾證得「`e^x` strictly increasing on ℝ」。§4.5 從這裡接手定義 `ln x`，**不重證**單調性。

（連續性 Theorem 4.6（`e^x` 在 ℝ 上連續）是 EVT「Fact」可套用到 `e^x`-型函數的背景前提，本節證明本身用的是抽象 `f` 的連續／可微假設，非 `e^x` 專屬。）

---

## § Rolle's Theorem（手稿原文，pp.11–18）

> 手稿標題即 "§ Rolle's Theorem"；其下依序為 max/min 定義、`cos x` 例、EVT「Fact」、Thm A、Rolle、MVT、monotonicity Corollary、兩個 Example。handout 標題改為 §4.4「Rolle's Theorem and the Mean Value Theorem」。

### Def 1（maximum / minimum point）

For `f(x)` defined on a domain `D`, we say that `f(x_0)` is a **maximum** of `f` on `D` if `x_0 ∈ D` and

`f(x_0) ≥ f(x)`   `∀ x ∈ D`.

（手稿以紅筆標出對偶的 **minimum**：把 `maximum` 換成 `minimum`、`≥` 換成 `≤`，即 `f(x_0) ≤ f(x) ∀ x ∈ D`。）

### Ex（`cos x`）

For `f(x) = cos x`, `x ∈ ℝ`, we see that `0 ∈ ℝ` and

`1 = cos 0 ≥ cos x`,   `∀ x ∈ ℝ`.

Hence, `0` is a **maximum point** of `cos x` and the **maximum value** is `1`.

### Fact（Extreme Value Theorem，陳述不證）

If `f` is a continuous function defined on a closed interval `[a, b]`, then `f` has a maximum point `X_M ∈ [a, b]` and a minimum point `X_m ∈ [a, b]`.

> 手稿括註原文：「This fact can be derived from the completeness of real numbers. The whole argument is lengthy. We do not prove it for the moment.」——**明言不證**（依完備性，論證冗長）。

### Thm A（interior extremum ⟹ `f' = 0`）

**Suppose** `X_M ∈ (a, b)` is a maximum point of a continuous function `f(x)` defined on `[a, b]` and `f'(X_M)` exists. **Then** `f'(X_M) = 0`.

（手稿以紅筆標對偶 minimum 版：`X_m ∈ (a, b)`、minimum、`f'(X_m)`、`f'(X_m) = 0`。）

**證（手稿）：**
Since `f(X_M) ≥ f(x)` for all `x ∈ [a, b]`,

`f(X_M + h) − f(X_M) ≤ 0`.

⟹

`(f(X_M + h) − f(X_M)) / h ≤ 0`   for `h > 0`,

and

`(f(X_M + k) − f(X_M)) / k ≥ 0`   for `k < 0`.

Hence,

`f'(X_M) = lim_{h→0⁺, h>0} (f(X_M + h) − f(X_M)) / h ≤ 0`,

and

`f'(X_M) = lim_{k→0⁻, k<0} (f(X_M + k) − f(X_M)) / k ≥ 0`.

This implies `f'(X_M) = 0`.

> 手稿只顯式做 maximum case；minimum case 由紅筆對偶標注，視為平行（把 `≥`↔`≤`、`h>0`↔`k<0` 對調）。`h>0` 時分子 `≤0`、分母 `>0` ⟹ 商 `≤0`；`k<0` 時分子 `≤0`、分母 `<0` ⟹ 商 `≥0`。兩單邊極限一個 `≤0` 一個 `≥0`，逼出 `=0`。

### Rolle's Thm

**Suppose** `f` is continuous on `[a, b]` and is differentiable on `(a, b)`. **If** `f(a) = f(b)`, **then** there exists a point `c ∈ (a, b)` s.t. `f'(c) = 0`.

**證（手稿）：**
Suppose `X_m, X_M ∈ [a, b]` s.t.

`m = f(X_m) ≤ f(x) ≤ f(X_M) = M`   `∀ x ∈ [a, b]`.

（`X_m, X_M` 由 Fact〔EVT〕保證存在。）

**Case 1.** If `m = M = f(a) = f(b)`, then `f(x) = f(a)` for all `x ∈ (a, b)` and `f'(c) = 0` `∀ c ∈ (a, b)`.

**Case 2.** If Case 1 does not hold, then either

(i) `f(X_M) > f(a)`   or   (ii) `f(X_m) < f(a)`.

**[請查核]**：手稿 p.14 的 (ii) 寫成「`f(X_M) < f(a)`」——下標應為 `X_m`（手稿筆誤）。p.15 解 (ii) 時用的是 `X_m`（「`X_m ∈ (a,b)`、`c = X_m`」），且 legacy `cor`/Rolle 證（line 612）亦作 `f(x_m) < f(a)`。故此處取 **`f(X_m) < f(a)`**（min 落在端點值之下）。

If (i) holds, `X_M ∈ (a, b)`, and we may choose `c = X_M` so that

`f'(c) = f'(X_M) = 0`.

If (ii) holds, then `X_m ∈ (a, b)` and we may choose `c = X_m`. We then see that

`f'(c) = f'(X_m) = 0`.

This completes the proof.

> 邏輯：Case 2 中 `m < M`（否則退回 Case 1）；又 `f(a)=f(b)`，故 max 與 min 不能都等於端點值——至少一個嚴格在端點值之外，那一個（極值點）必在開區間 `(a,b)` 內部，由 Thm A 得 `f'=0`。

### The mean value theorem（MVT）

**Suppose** `f` is continuous on `[a, b]` and is differentiable on `(a, b)`. **Then** there exists a point `c ∈ (a, b)` s.t.

`f'(c) = (f(b) − f(a)) / (b − a)`.

> 手稿一句：「We shall use the Rolle's theorem to prove the mean value theorem.」

**證（手稿）：**
Set

`g(x) = f(x) − [ f(a) + ((f(b) − f(a)) / (b − a)) (x − a) ]`.

Observe: Since `f` is differentiable on `(a, b)` and continuous on `[a, b]`, so is `g(x)`.

`g(a) = 0 = g(b)`.

By the Rolle's theorem, `∃ c ∈ (a, b)` s.t.

`0 = g'(c) = f'(c) − (f(b) − f(a)) / (b − a)`,

which implies

`f'(c) = (f(b) − f(a)) / (b − a)`.

This completes the proof of the mean value theorem.

> 中括號 `[ f(a) + ((f(b)−f(a))/(b−a))(x−a) ]` 是過 `(a, f(a))`、`(b, f(b))` 的割線；`g` 是曲線與割線的垂直差。`g(a)=f(a)−f(a)=0`、`g(b)=f(b)−f(b)=0`（手稿直接給 `g(a)=0=g(b)`，未展開兩步）；`g'(x)=f'(x)−(f(b)−f(a))/(b−a)`（中括號對 `x` 微分，常數項 `f(a)` 消失、線性項斜率為割線斜率）。

### Corollary（`f' ≥ 0 ⟹ increasing`）

**Suppose** `f` is continuous on `[a, b]` and is differentiable on `(a, b)`. **If** `f'(c) ≥ 0` for all `c ∈ (a, b)`, **then**

`f(x_2) ≥ f(x_1)`   for all `a ≤ x_1 < x_2 ≤ b`.

**證（手稿）：**
Applying the mean value theorem on `[x_1, x_2]`, `∃ c ∈ (x_1, x_2)` s.t.

`(f(x_2) − f(x_1)) / (x_2 − x_1) = f'(c) ≥ 0`.

Hence `f(x_2) ≥ f(x_1)`.

### Example

**(i)** `d/dx sin x = cos x > 0` for `x ∈ [0, π/4]`.
Hence, `sin x_2 > sin x_1` for `0 ≤ x_1 < x_2 ≤ π/4`.

**(2)** `d/dx e^x = e^x > 0` for all `x ∈ ℝ`.
Hence, `e^{x_2} > e^{x_1}` for all `x_1 < x_2`.

`[ e^x is strictly increasing for all x ∈ ℝ ]`   （手稿以紅筆方括註，標重點）。

> **[請查核]（strict vs non-strict）**：手稿 Corollary 只陳述 `f' ≥ 0 ⟹ f(x_2) ≥ f(x_1)`（**非嚴格**），但兩個 Example 都下 **strict**（`sin x_2 > sin x_1`、`e^{x_2} > e^{x_1}`、"strictly increasing"）。手稿是直接重跑 MVT 商式 `(f(x_2)−f(x_1))/(x_2−x_1)=f'(c)`：當 `f'(c) > 0`（嚴格正）時分子嚴格正，得 strict。即 strict 結論來自「`f' > 0`」而非那條非嚴格 Corollary。**legacy 把 Corollary 寫成雙條（`f'≥0 ⟹` non-decreasing；`f'>0 ⟹` strictly increasing）**（line 705–710）——這是乾淨補法，且 §4.5 需要「`e^x` strictly increasing」（單射）才能定義 `ln x`。屬 ④ 方向（建議 Corollary 補 strict 版；見 ② brief §C）。

---

## §4.4 / §4.5 boundary

手稿在 `[e^x is strictly increasing for all x ∈ ℝ]` 後緊接 **§ Logarithmic function**：「Since `e^x` is strictly increasing for all `x ∈ ℝ`, we can define `ln x` to be the inverse function of `e^x` for `x ∈ (a, b)` where `a = lim_{x→−∞} e^x = 0` and `b = lim_{x→∞} e^x = +∞`」——**這是 §4.5 的開頭**，不屬本 seed。§4.4 收在「`e^x` strictly increasing on ℝ」（交棒給 §4.5）。

---

## 手稿刻意省略／特徵（忠實記錄）

- **無圖**：手稿全程純文字，無 MVT 割線–切線圖。**ROADMAP §4.4 key figure ＝ MVT secant–tangent 圖**（割線 dashed、內部 `c` 處平行 tangent solid）——屬 handout 加法（legacy 有 `fig:mvt`）。② brief 提案 Figure 4.2。
- **無 strategy box**：手稿不給「套用 MVT 前先驗 hypotheses」程序。**ROADMAP §4.4 指派此 strategy**（[a,b] 連續 vs (a,b) 可微的不對稱）——屬 handout 加法（legacy 有對應 strategy；`|x|` on `[−1,1]` 為 hypothesis-fail 反例）。② brief 提案 Strategy 4.2。
- **無 caution**：手稿不標 (a) Thm A 的「internal」必要性（端點極值不必 `f'=0`，如 `f(x)=x` on `[0,1]`）、(b) MVT 的 closed/open 不對稱、(c) `|x|` 反例——皆 legacy 加法、② brief 候選。
- **EVT 不證**：手稿明言「依完備性、論證冗長、暫不證」。handout 具名 Theorem（Extreme Value Theorem）、陳述不證、cross-ref 完備性（Theorem 4.1）。legacy `thm:evt` 同此用法（並補「closed＋continuous 兩條件皆必要」的 remark／反例）。
- **Corollary 的 strict 缺口**（見上 [請查核]）：陳述非嚴格、Example 用嚴格。④ 建議補 strict 版（§4.5 需 `e^x` 單射）。
- **`e^x > 0 ∀x` 的依據**：Example (2) 直接寫 `e^x > 0`，未重述理由。依據：`x ≥ 0` 由級數逐項正；`x < 0` 由指數律 `e^x = 1/e^{−x} > 0`（Theorem 4.7）。④ 可補一行（legacy `ex:exp-strictly-increasing` 即如此補）。
- **Thm A 只顯式做 max case**：min case 由紅筆對偶標注、視為平行。
- **「Theorem A」命名**：手稿把 interior-extremum 結果命名為「Thm A」（無教科書通名）。handout 編號為 Theorem `4.10`，可在 env-name 保留「Theorem A」或「Interior extremum」為副名（④/② 決定）。legacy 用 `[Theorem A]` 為名、`thm:interior-extrema` 為 label。
- **「strictly increasing on every [a,b] ⟹ on ℝ」的跳步**：Example (2) 由「任意 `x_1<x_2` 上嚴格增」推「on ℝ 嚴格增」。legacy 加一條 caution（line 730）：此延拓對 strict monotonicity 成立（任取 `[x_1,x_2]` 套 Corollary），但非所有區間性質都可這樣延拓（如 boundedness、attaining max）。④ 可選一句 note。
- worked example：手稿 **1 個 Example 區塊（含 (i)(ii) 兩小項）**。圖：**0**。動機散文：**極少**（僅 "We shall use the Rolle's theorem to prove the mean value theorem." 一句承轉）。named-result 索引：max/min Def、Fact〔EVT〕、Thm A、Rolle、MVT、Corollary（具名化／編號屬 ④）。
- 記號：極值點 `X_M`（max）／`X_m`（min）；端點增量 `h>0`／`k<0`；極值 `m=f(X_m)`／`M=f(X_M)`；MVT 輔助函數 `g(x)`；單調性區間端點 `x_1<x_2`、`c`。無新巨集。

---

## 對照 ground truth（評分用，非手稿）

已簽核 `legacy/tex_handout/chapters/ch04_exponential_logarithm.tex` §4.4 段（`\section{Rolle's Theorem and the Mean Value Theorem}`，`sec:rolle-and-mvt`，lines 538–696）是同一手稿的 LaTeX→HTML 前簽核版，**僅作盲算對賬的 ground truth**（D1），不照抄其散文／結構。盲算對賬結果：

- **Def（max/min）**：legacy `def:max-min` 同義（雙列 itemize）。✓
- **`cos x` example**：legacy 同（並補 `x=π` minimum、週期點）。✓
- **EVT**：legacy `thm:evt`「continuous on `[a,b]` ⟹ attains max & min」＋ remark「completeness 依賴、closed＋continuous 兩條件皆必要、附 `f(x)=x` on `(0,1)`／rationals-indicator 反例」。手稿只給 Fact＋「暫不證」。✓（math 一致；legacy 反例為加法）
- **Thm A（interior extremum）**：legacy `thm:interior-extrema` 證法逐字一致（`f(X_M+h)−f(X_M)≤0`；`h>0` 商 `≤0` ⟹ 右極限 `≤0`；`h<0` 商 `≥0` ⟹ 左極限 `≥0`；兩者 ⟹ `=0`）。legacy 補 caution「interior 必要、端點 `f(x)=x` on `[0,1]` 反例」。✓
- **Rolle**：legacy `thm:rolle` 證法一致（Case 1 `m=M` ⟹ 常數；Case 2 `m<M` ⟹ max 或 min 嚴格在端點值外 ⟹ 該極值點 interior ⟹ Thm A 得 `f'=0`）。legacy Case 2 寫「`f(x_M)>f(a)=f(b)` 或 `f(x_m)<f(a)=f(b)`」——**證實手稿 (ii) 的 `X_M` 為 `X_m` 筆誤**。✓
- **MVT**：legacy `thm:mvt` 證法逐字一致（輔助 `g(x)=f(x)−[f(a)+((f(b)−f(a))/(b−a))(x−a)]`；`g` 連續可微、`g(a)=g(b)=0`；Rolle ⟹ `g'(c)=0=f'(c)−(f(b)−f(a))/(b−a)`）。legacy 補 `fig:mvt`（割線–切線圖）、MVT hypothesis-asymmetry caution、`Applying the MVT` strategy（`|x|` on `[−1,1]` 反例）。✓
- **Monotonicity Corollary**：**legacy 把它放 §4.5 開頭（`cor:monotonicity`，line 705），手稿＋PLAN §1 放 §4.4**（手稿頁序：MVT 後緊接 Corollary＋Example，再 § Logarithmic function）。legacy Corollary 寫**雙條**（`f'≥0 ⟹` non-decreasing；`f'>0 ⟹` strictly increasing），證即套 MVT 於 `[x_1,x_2]`（與手稿同）。兩個 Example（sin on `[0,π/4]`、`e^x` on ℝ）legacy 亦在 §4.5 開頭、內容一致。✓
  - **placement 裁決（PLAN §1/§2 已定）**：§4.4 **含** Corollary＋兩 Example，收在「`e^x` strictly increasing on ℝ」；§4.5 從此接手定義 `ln x`、**不重證**單調性。auditor 勿把 §4.4 收 Corollary 判為「越界／與 §4.5 重複」（手稿頁序如此、PLAN 已裁）。

**編號接續（PLAN §5 ledger）：** §4.1–§4.3 已 mint 到 Definition 4.2、Theorem 4.8、Proposition 4.2、Corollary 4.2、Strategy 4.1、Example 4.1、Figure 4.1、Remark 4.3。**§4.4 因此自 Definition 4.3、Theorem 4.9、Corollary 4.3、Strategy 4.2、Example 4.2、Figure 4.2、Remark 4.4 起編號**（Proposition 本節未必新增）。本 seed 為手稿原貌（pp.11–18）；具名化與編號落在 ④。

**ROADMAP 已標的 §4.4 方向（待 ③ 方向閘確認）：**
- **key figure ＝ MVT secant–tangent**（割線 dashed、內部 `c` 平行 tangent solid）。
- **strategy ＝「套用 MVT 前先驗 hypotheses」**（[a,b] 連續 vs (a,b) 可微的不對稱；`|x|` on `[−1,1]` 反例）。
- **MVT 留在本章**（D4：手稿把 Rolle/MVT 夾在指數章，因 `ln` 建構需單調性 corollary；本章不移走，未來 applications 專章再於 Mode B 僅提議移動）。

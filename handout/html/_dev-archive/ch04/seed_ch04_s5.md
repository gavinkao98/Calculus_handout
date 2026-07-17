# Seed — §4.5 Monotonicity and the Logarithmic Function

> stage ① 產物。Transcribed from the handwritten manuscript `2023-11-4-ExponentialFunction`,
> **pp.18–22** (the section the manuscript heads "§ Logarithmic function", beginning right after
> the red-boxed "[e^x is strictly increasing for all x ∈ ℝ]" mid-p.18, running through the
> Def of `ln x`, the continuity "Property", and "§ The differentiability of ln x", ending with
> `d/dx ln x = 1/x` on p.22) **plus the chapter Homework pp.23–24** (4 items, promotion
> candidates per D7).
> Manuscript heads this block "§ Logarithmic function"; handout maps it to §4.5
> "Monotonicity and the Logarithmic Function" per ROADMAP/PLAN §1. **This is the chapter's
> final section** (manuscript content ends at p.24).
> Faithful to the manuscript: structure, order, notation, and deliberate omissions preserved.
> seed 語法＝輕量可讀（反引號行內＋Unicode；見 CONTENT_DIRECTION ① / `seed_ch04_s4.md`）。漂亮 KaTeX 留給 ④。可疑／非標準處標 **[請查核]**。
> **數學 cross-check（非手稿）**：legacy `ch04_exponential_logarithm.tex` §4.5 段（`\subsection{Defining $\ln x$}`／`{Continuity of $\ln x$}`／`{The derivative of $\ln x$}`，`def:logarithm` line 738、`thm:ln-continuous` line 758、`thm:ln-derivative-rigorous` line 776、`fig:exp-and-log-reflection` line 812）。**注意 placement**：legacy 把 monotonicity Corollary＋兩 Example 放 §4.5 開頭（`cor:monotonicity` line 705），但手稿頁序＋PLAN §1 已把它們歸 §4.4（`sec-4-4.html` 已含 Corollary 4.3＋Example 4.3/4.4）；故 **§4.5 不重收 Corollary**，自「§ Logarithmic function」（定義 `ln x`）起。D1：僅盲算對賬，不照抄散文／結構。

---

## §4.1–§4.4 依賴（承前；非本節新內容，僅備援引）

§4.5 建構 `ln x` 用到前四節的既成事實：

1. **§4.4 結尾（Example 4.4）**：`e^x` **strictly increasing on ℝ**。這是 §4.5 的起點——嚴格遞增 ⟹ 單射（one-to-one）⟹ `e^x` 在其值域上有反函數。**§4.5 不重證單調性**，直接接手。
2. **§4.3（Theorem 4.8）**：`d/dx e^x = e^x`。可微性證明的分母極限 `lim_{y→y_0}(e^y−e^{y_0})/(y−y_0) = e^{y_0}` 即套用此導數定義／值。
3. **§4.2（Theorem 4.7 指數律＋Corollary 4.1 positivity）**：`e^x > 0 ∀x`、`e^{x+y}=e^x e^y`。連續性反證裡「`e^z` strictly increasing」與正性、指數律算式（`e^{ln x_0−δ}` 等）皆依此。
4. **Ch1（反函數／一對一）**：`ln x` 定義為 `e^x` 反函數——「strictly increasing ⟹ one-to-one ⟹ invertible」用 Ch1 的反函數 setup（ROADMAP key figure 重用 Ch1 reflection；§4.5 圖＝`e^x`/`ln x` 對 `y=x` 反射）。
5. **Ch3 §3.3（chain-rule applications）**：曾**非正式**用 chain rule 在 `e^{ln x}=x` 上算得 `d/dx ln x = 1/x`（假設 `ln` 可微）。§4.5 是**嚴格重做**：不預設可微，用 inverse-function 技巧從差分商萃取。**forward-loop close**：Ch3 §3.3 forward-ref 到此 → §4.5 關閉迴路。

---

## § Logarithmic function（手稿原文，pp.18–22）

> 手稿標題即 "§ Logarithmic function"；其下依序為 §4.5 opener（由 strict monotonicity 定義 `ln x` 的值域）、Def（`ln x`）、Property（連續性）＋反證、§ The differentiability of ln x（可微＋導數）。handout 標題改為 §4.5「Monotonicity and the Logarithmic Function」。

### §4.5 opener（手稿，承 §4.4 結尾）

`[ e^x is strictly increasing for all x ∈ ℝ ]`   （p.18，手稿紅筆方括，§4.4 收尾句；§4.5 由此接手）

**§ Logarithmic function.**
Since `e^x` is strictly increasing for all `x ∈ ℝ`, we can define `ln x` to be the inverse function of `e^x` for `x ∈ (a, b)` where

`a = lim_{x→−∞} e^x = 0`   and   `b = lim_{x→∞} e^x = +∞`.

> 手稿筆跡：「the **in** inverse function」有一個贅字 `in`（劃寫殘留），實為「the inverse function」。值域端點 `(a,b)=(0,+∞)` 由兩個極限給出。**[斷言不證]**：手稿直接寫 `lim_{x→−∞}e^x=0`、`lim_{x→∞}e^x=+∞`（即 `e^x` 的值域＝`(0,∞)`），**未證這兩個極限、也未證滿射**。legacy line 736 明言「we will not prove this explicitly; it follows from continuity and the limits …, which can be derived from the series」——同樣斷言不證。屬手稿刻意省略（見下「刻意省略」）。

### Def（`ln x`，手稿方框標 "Def"）

For `x ∈ (0, ∞)`, we define `ln x = a ∈ ℝ` to be the unique value that satisfies

`e^a = x`.

i.e.,   `e^{ln x} = x`.

It is not hard to see that

`ln(e^x) = x`   for all `x ∈ ℝ`.

> 手稿筆跡：「ln x = a ∈ ℝ **be** the unique value」（文法 `be`→`to be`／`is`）、「It is **no** hard to see」（`no`→`not`）——皆筆誤、數學無歧義。兩條反函數恆等式：`e^{ln x}=x`（x>0，`ln` 為右作用的反）與 `ln(e^x)=x`（x∈ℝ，左作用的反）。唯一性來自 `e^x` strict monotonicity；存在性（對每個 x>0 都有 a）來自值域＝`(0,∞)`（上面斷言不證的那條）。legacy `def:logarithm`（line 738）同：「the unique real number `a` satisfying `e^a=x`；equivalently the inverse of `e^x` on `(0,∞)`：`e^{ln x}=x` ∀x>0、`ln(e^x)=x` ∀x∈ℝ」。✓

### Property（`ln x` 連續，手稿方框標 "Property"）

**`ln x` is a continuous function.**

**證（手稿，proof by contradiction）：**
Suppose `∃ x_0 > 0` s.t. `lim_{x→x_0} ln x ≠ ln x_0`.

Either `lim_{x→x_0} ln x` does not exist, or `lim_{x→x_0} ln x = μ ≠ ln x_0`.

In either case, `∃ δ > 0` and `y_j → x_0` s.t.

`|ln y_j − ln x_0| ≥ δ`   for `j = 1, 2, 3, …`.

**Case 1.** `ln x_0 ≥ ln y_j + δ`
⟹ `e^{ln x_0} − e^{ln y_j} ≥ e^{ln x_0} − e^{ln x_0 − δ} > 0`
  (since `e^z` is a strictly increasing function).

**Case 2.** `ln x_0 + δ ≤ ln y_j`
⟹ `e^{ln y_j} − e^{ln x_0} ≥ e^{ln x_0 + δ} − e^{ln x_0} > 0`.

Let `ε = min{ e^{ln x_0} − e^{ln x_0 − δ},  e^{ln x_0 + δ} − e^{ln x_0} }`.

We see that

`|y_j − x_0| = |e^{ln y_j} − e^{ln x_0}| ≥ ε`   for all `j = 1, 2, …`.

This violates `lim_{j→∞} y_j = x_0`.

Hence, `ln x` is a continuous function.

> 邏輯：否定連續 ⟹ 存在序列 `y_j→x_0` 但 `|ln y_j − ln x_0|≥δ`（sequential continuity 的反面）。每個 `j` 落入 Case 1（`ln y_j ≤ ln x_0−δ`）或 Case 2（`ln y_j ≥ ln x_0+δ`）。對 `e^z`（strict increasing）作用，兩 case 各給一個**嚴格正**的下界；`ε`＝兩者較小。關鍵恆等式 `y_j = e^{ln y_j}`、`x_0 = e^{ln x_0}`（`e^{ln(·)}` 為恆等）⟹ `|y_j−x_0| = |e^{ln y_j}−e^{ln x_0}| ≥ ε > 0`，與 `y_j→x_0` 矛盾。legacy `thm:ln-continuous`（line 758）同骨架，但寫 **WLOG 單邊**（`ln y_j ≥ ln x_0+δ` for infinitely many j），得 `y_j ≥ e^δ·x_0 > x_0`、gap 阻止收斂。手稿顯式雙 case＋`ε=min` 更完整。math 一致。✓ **無 [請查核]。**

### § The differentiability of ln x（手稿小節標題）

For `x > 0` and `x + h > 0` with `h ≠ 0`, we have

`h = (x + h) − x = e^{ln(x+h)} − e^{ln x}`
` = [ (e^{ln(x+h)} − e^{ln x}) / (ln(x+h) − ln x) ] · (ln(x+h) − ln x)`.

**Note:** Since `h ≠ 0`, `ln(x+h) ≠ ln x`

⟹   `(ln(x+h) − ln x) / h = 1 / [ (e^{ln(x+h)} − e^{ln x}) / (ln(x+h) − ln x) ]`.

Set `y_0 = ln x`,  `y = ln(x+h)`.

Since `ln x` is a continuous and strictly increasing function,

`lim_{h→0} y = y_0`   and   `y ≠ y_0` for `h ≠ 0`.

We then see that

`lim_{h→0, h≠0} (e^{ln(x+h)} − e^{ln x}) / (ln(x+h) − ln x)`
` = lim_{y→y_0, y≠y_0} (e^y − e^{y_0}) / (y − y_0) = e^{y_0} = e^{ln x} = x`.

**Finally, we conclude**

`lim_{h→0} (ln(x+h) − ln x) / h = lim_{h→0}  1 / [ (e^{ln(x+h)} − e^{ln x}) / (ln(x+h) − ln x) ]`
` = 1 / [ lim_{h→0} (e^{ln(x+h)} − e^{ln x}) / (ln(x+h) − ln x) ] = 1/x`.

This proves that

`d/dx ln x = 1/x`   for `x > 0`.

> inverse-function 技巧：用 `e^{ln(x+h)}=x+h`、`e^{ln x}=x` 把 `h` 寫成 `e^y−e^{y_0}`（`y=ln(x+h)`, `y_0=ln x`），再把差分商倒置成「`e^y` 在 `y_0` 的差分商」的倒數。`h→0` 時 `y→y_0`（`ln` 連續，剛證），分母 → `lim_{y→y_0}(e^y−e^{y_0})/(y−y_0) = (d/dy e^y)|_{y_0} = e^{y_0} = e^{ln x} = x`（套 §4.3 Theorem 4.8）。`y≠y_0`（`ln` strict ⟹ 單射，`h≠0` ⟹ `y≠y_0`）確保分母差分商分母不為 0。倒數 ⟹ `1/x`。legacy `thm:ln-derivative-rigorous`（line 776）逐步一致（legacy 直接用 `y,y_0` 代換、手稿先寫滿 `ln(x+h)` 再 `Set y=…`，等價）。✓ **無 [請查核]。**

---

## Homework（手稿 pp.23–24，4 題；D7 升格候選）

> 手稿章末附 4 道 homework。**bare your-turn exercise 一律不入 handout body**（root README §防護欄、CONTENT_SPEC §14）；但 **manuscript-faithful 的具名結果可升格 worked example（含解）**（D7，待 ③）。逐題原文＋升格定位：

1. **Show that if `f'(x) = 0` for `x ∈ (a, b)`, then `f(x)` is a constant for `x ∈ (a, b)`.**  `[Hint: mean value theorem]`
   - → **§4.4 MVT 的直接推論**。但 §4.4 已 ⑥ 簽核完成；此題若升格應在 §4.5 開頭當「MVT 推論的另一面」一句帶過或小 worked example（與 Corollary 4.3「`f'≥0⟹`遞增」對偶：`f'=0⟹`常數）。**待 ③ 定位**：放 §4.5 還是略過。
2. **Prove that for `a, b > 0`, `ln a + ln b = ln(ab)`.**  `[Hint: Set f(x) = ln(ax) − ln x]`
   - → **§4.5 核心對數律**，manuscript-faithful。升格 worked example：用 hint 設 `f(x)=ln(ax)−ln x`，`f'(x)= a·(1/(ax)) − 1/x = 1/x − 1/x = 0`（套剛證的 `d/dx ln x=1/x`＋chain rule），故 `f` 常數 ⟹ `f(x)=f(1)=ln a − ln 1 = ln a`（`ln 1=0`，因 `e^0=1`）；代 `x=b`：`ln(ab)−ln b = ln a` ⟹ `ln a + ln b = ln(ab)`。**強升格候選**（D7 點名；既示範 `(ln)'=1/x` 又示範 HW1 的「`f'=0⟹const`」）。
3. **Suppose `g(x): ℝ → ℝ⁺` is a continuous function s.t. `g(x)g(y) = g(x+y)` `∀ x,y ∈ ℝ` and `g(1) = e`. Show that `g(x) = e^x` for `x ∈ ℝ`.**  `Rmk: ℝ⁺ = {x ∈ ℝ | x > 0}`.
   - → **Cauchy 函數方程刻畫 `e^x`**。較進階（需從有理數逐步逼近＋連續性延拓），多步。**D7 提案：略過或降為 remark**（低優先；非單一技巧示範，篇幅大）。**待 ③**。
4. **For `a > 0`, define `a^x = e^{x ln a}` for `x ∈ ℝ`. Show that, for `a, b > 0`:**  **(i)** `a^x · b^x = (ab)^x`,  **(ii)** `(a^x)^y = a^{xy} = (a^y)^x`.
   - → **一般指數 `a^x` 的定義＋指數律**，manuscript-faithful。升格 worked example：(i) `a^x b^x = e^{x ln a} e^{x ln b} = e^{x(ln a+ln b)} = e^{x ln(ab)} = (ab)^x`（用 HW2 的 `ln a+ln b=ln(ab)` ＋ §4.2 指數律 Theorem 4.7）；(ii) `(a^x)^y = e^{y ln(a^x)} = e^{y·(x ln a)} = e^{xy ln a} = a^{xy}`（用 `ln(a^x)=ln(e^{x ln a})=x ln a`），對稱得 `=(a^y)^x`。**升格候選**（D7 點名；定義一般指數、收束全章「`a^r` for r∉ℚ」的 §4.1 forward-fence）。

> **升格鏈依賴**：HW4 用 HW2（`ln(ab)=ln a+ln b`），HW2 用本節 `(ln)'=1/x`＋HW1（`f'=0⟹const`）。若升格，順序須 HW1/HW2 → HW4。**§4.1 D6 forward-fence**（`a^x:=e^{x ln a}` 留到 §4.5）正落在 HW4——§4.5 是收束點。

---

## §4.5 邊界（章末）

§4.5 是 Chapter 4 **最後一節**。手稿 §4.5 內容止於 p.22 `d/dx ln x = 1/x`；pp.23–24 為 Homework（章末，非新節）。其後無更多手稿內容。handout 的章末 **Summary**（CONTENT_SPEC §4 要求）屬 handout 結構件、非手稿——legacy 有 `\section*{Summary}`（line 841，四段 distillation：exponential／analysis machinery／existence theorems／logarithm）。**章末 Summary 待 ③ 決定是否本節產出**（屬章層收尾，非 §4.5 手稿內容）。

---

## 手稿刻意省略／特徵（忠實記錄）

- **`e^x` 值域＝`(0,∞)`、`lim_{x→±∞}e^x` 斷言不證**：手稿 opener 直接寫 `a=lim_{x→−∞}e^x=0`、`b=lim_{x→∞}e^x=+∞`，未證這兩個極限、未證滿射（存在性所需）。legacy line 736 同樣斷言不證（「follows from continuity and the limits …, which can be derived from the series」）。④ 可選一句 note 指出此處依賴連續＋極限＋（IVT-型）滿射，留作斷言（forward-fence 到更系統的極限處理，或就近 cross-ref §4.2 連續性）。**屬手稿刻意省略，非 [請查核]。**
- **連續性證走 sequential（序列）層級**：手稿從「`lim ln x ≠ ln x_0`」直接取得「∃ `δ>0` 與 `y_j→x_0` 使 `|ln y_j−ln x_0|≥δ`」（否定 ε-δ 連續 ⟹ 序列見證）。此一步是標準 sequential-continuity 等價，手稿未展開。④ 比照 legacy 維持 sketch/sequence 層級即可（不需補 ε-δ 全套）。
- **無圖**：手稿 §4.5 全程純文字，無 `e^x`/`ln x` 反射圖。**ROADMAP §4.5 key figure ＝ `e^x`/`ln x` 對 `y=x` 反射**（`e^x` blue、`ln x` red、標 `(0,1)`／`(1,0)`、`y=x` 虛線）——屬 handout 加法（legacy `fig:exp-and-log-reflection` line 812）。② brief 提案 Figure 4.3。
- **無 strategy box**：手稿不給操作程序。ROADMAP §4.5 未硬性指派 strategy（§4.4 才指派 MVT strategy）；②可選提案「用 inverse-function 技巧求反函數導數」strategy（Strategy 4.3，低優先）或不設。**待 ③。**
- **無 caution**：手稿不標 (a) `ln x` 只對 x>0（`ln 0`／`ln(−1)` undefined）、(b) range 斷言。legacy 補兩條 caution（domain restriction line 750、range-extension line 730——後者已隨 Corollary 歸 §4.4）。② brief 候選：`ln` domain caution（`x>0`，`ln 0`／負數 undefined）。
- **`ln 1 = 0`、`ln e = 1` 等具體值未列**：手稿只給定義＋連續＋導數，未列特殊值表。④ 若升格 HW2 worked example 會自然用到 `ln 1=0`（`e^0=1`）；可順帶一句，非獨立 example。
- **Ch3 重複**：`d/dx ln x=1/x` 在 Ch3 §3.3 已**非正式**算過（假設可微、用 chain rule 於 `e^{ln x}=x`）。§4.5 是嚴格重做（不設可微、inverse-function 技巧）。④ 開頭／Remark cross-ref Ch3、點明「這次不預設 `ln` 可微、改從差分商萃取」（legacy `remark` line 807 即此用法）。重構（Ch3 改 forward-ref）**延後至兩章都簽核後**——本章不動 Ch3。
- worked example：手稿 §4.5 本體 **0 個 worked example**（純定義＋兩證）；example 全在 Homework（待 D7 升格）。圖：**0**。動機散文：**極少**。named-result 索引：`ln x` Def、連續 Property、可微（`(ln)'=1/x`）。
- 記號：對數 `ln x`（x>0）；反函數恆等 `e^{ln x}=x`／`ln(e^x)=x`；連續性反證序列 `y_j→x_0`、gap `δ`、`ε=min{…}`；可微代換 `y_0=ln x`、`y=ln(x+h)`。無新巨集。

---

## 對照 ground truth（評分用，非手稿）

已簽核 `legacy/tex_handout/chapters/ch04_exponential_logarithm.tex` §4.5 段是同一手稿的 LaTeX→HTML 前簽核版，**僅作盲算對賬的 ground truth**（D1），不照抄其散文／結構。盲算對賬結果：

- **§4.5 opener / 值域**：legacy line 736 同手稿——`e^x` strict increasing ⟹ one-to-one（`def:one-to-one`）⟹ 有反函數；range `(0,∞)` 斷言不證。✓
- **Def（`ln x`）**：legacy `def:logarithm`（line 738）逐字同義（unique `a` s.t. `e^a=x`；`e^{ln x}=x` ∀x>0、`ln(e^x)=x` ∀x∈ℝ）。legacy 補 domain caution（`ln` 只 x>0）＋informal gloss。✓
- **連續性**：legacy `thm:ln-continuous`（line 758，proof sketch）同骨架（反證、`y_j→x_0` 但 `|ln y_j−ln x_0|≥δ`、套 `e^x` strict increasing 得 gap、矛盾）。legacy WLOG 單邊；手稿顯式雙 case＋`ε=min`。math 一致。✓
- **可微 / 導數**：legacy `thm:ln-derivative-rigorous`（line 776）逐步一致（`y_0=ln x`、`y=ln(x+h)`、`e^y−e^{y_0}=h`、商倒置、`h→0`⟹`y→y_0` by continuity、分母→`e^{y_0}=x`、故 `1/x`；用 `thm:exp-derivative-rigorous`＝§4.3 Theorem 4.8）。✓ legacy 補 remark（與 Ch3 chain-rule 版的異同）。
- **Figure**：legacy `fig:exp-and-log-reflection`（line 812）＝`e^x`/`ln x` 對 `y=x` 反射、`(0,1)`/`(1,0)` 標點——即 ROADMAP §4.5 key figure。✓（手稿無圖，屬加法）
- **Homework**：legacy line 874–877 NOTE 完整列 4 題（與手稿一致），註明「講義本體不收習題（CONTENT_SPEC §14）；保留給獨立習題本」。**D7 政策**：manuscript-faithful 的具名結果（HW1 `f'=0⟹const`、HW2 `ln(ab)=ln a+ln b`、HW4 `a^x` 指數律）可升格 **worked example（含解）**；HW3 Cauchy 函數方程較進階、提案略過／降 remark。**待 ③ 裁。**
- **章末 Summary**：legacy `\section*{Summary}`（line 841）四段。手稿無（屬 handout 結構件）。**待 ③ 決定本節是否產出。**

**編號接續（PLAN §5 ledger）：** §4.1–§4.4 已 mint 到 Definition 4.3、Theorem 4.12、Proposition 4.2、Corollary 4.3、Strategy 4.2、Example 4.4、Figure 4.2、Remark 4.4。**§4.5 因此自 Definition 4.4（`ln x`）、Theorem 4.13、Proposition 4.3、Corollary 4.4、Strategy 4.3、Example 4.5、Figure 4.3、Remark 4.5 起編號**（PLAN §5 已預登）。本 seed 為手稿原貌（pp.18–22＋HW）；具名化與編號落在 ④。

**ROADMAP 已標的 §4.5 方向（待 ③ 方向閘確認）：**
- **承重直覺 ＝「strict monotonicity 是定義反函數的引擎」**：`e^x` 嚴格遞增（§4.4 收割）⟹ 單射 ⟹ 可逆 ⟹ `ln x` 良定義；continuity／differentiability 兩證又都**回頭依賴** `e^x` 的 strict monotonicity（連續性反證的 gap、可微的 `y≠y_0`）。一個性質撐起整節。
- **key figure ＝ `e^x`/`ln x` 對 `y=x` 反射**（重用 Ch1 reflection setup；`e^x` blue、`ln x` red）→ Figure 4.3。
- **forward-loop close**：Ch3 §3.3 非正式用 `ln`／forward-ref 到此 → §4.5 關閉迴路（④ cross-ref，本章不改 Ch3）。
- **D7 Homework 升格**：HW1/HW2/HW4 → worked example（含解，manuscript-faithful）；HW3 略過／降 remark。**待 ③。**
- **章末 Summary**：CONTENT_SPEC §4 要求章末 Summary；§4.5 為末節 → 可能由本節產出整章 Summary。**待 ③。**
- **`a^r`(r∉ℚ) 收束（§4.1 D6 forward-fence）**：若升格 HW4，`a^x:=e^{x ln a}` 正是 §4.1 拋出「how about a^r?」的收束點。

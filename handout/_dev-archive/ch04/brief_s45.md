# Direction Brief — §4.5 Monotonicity and the Logarithmic Function

> ② 方向提案（CONTENT_DIRECTION §2 九欄）。**狀態：待 ③ 方向閘核可**（③ 拍板後本 brief 成 ④/⑤ 契約）。
> 輸入：[`seed_ch04_s5.md`](seed_ch04_s5.md)（手稿 pp.18–22＋HW pp.23–24）＋ [`PLAN-ch04.md`](PLAN-ch04.md) 章層決策（D7 Homework 升格、編號 ledger 自 Definition 4.4／Theorem 4.13 起）＋ ROADMAP「Chapter 4」條目（core skill「定義 `ln x` 為 `e^x` inverse／證連續／推導 `(ln x)'=1/x`」、key figure＝`e^x`/`ln x` 對 `y=x` 反射、caution＝`ln` 只 x>0、§3.3 forward-loop 在此關閉、**§4.5 無指派 strategy**）。
> §4.5 **是 Chapter 4 最後一節**。核心手稿內容**短**（opener 定值域 → Def `ln x` → 連續 Property＋證 → 可微＋證），但**加法決策多**：D7 三道 HW 升格（HW1/2/4）、Figure 4.3（反射）、章末 Summary、`ln` domain caution、Ch3 §3.3 迴路關閉、值域斷言處理。**風險側寫與 §4.4 相反**——不是證明階梯紮實度，而是**「升格哪些 HW、加多少、章末怎麼收」的方向取捨**：升太多 → 末節膨脹；升太少 → §4.1 的 `a^r` fence（D6）與 Ch3 迴路懸空。沿用 §4.1–§4.4 已建骨架，續編號（自 Definition 4.4、Theorem 4.13 起）。
> ①-verify：使用者選「開跑 §4.5」即視為 seed accepted-by-proceeding（§4.5 數學乾淨、無 [請查核] 級疑點）。數學 cross-check：legacy `ch04_exponential_logarithm.tex` §4.5 段（`def:logarithm` line 738、`thm:ln-continuous` line 758、`thm:ln-derivative-rigorous` line 776、`fig:exp-and-log-reflection` line 812、`remark` line 807、application line 834、Summary line 841）。

---

## 手稿盤點（照原順序，pp.18–22＋HW pp.23–24）
- **§ Logarithmic function**（手稿標題；handout 改 §4.5「Monotonicity and the Logarithmic Function」）。
- **opener**：`e^x` strictly increasing on ℝ（承 §4.4）⟹ 可定義 `ln x` 為 `e^x` 反函數 on `(a,b)`，`a=lim_{x→−∞}e^x=0`、`b=lim_{x→∞}e^x=+∞`（值域＝`(0,∞)`；**兩極限＋滿射斷言不證**）。
- **Def（`ln x`）**：x∈(0,∞)，`ln x = a` 為滿足 `e^a=x` 的唯一值，即 `e^{ln x}=x`；且 `ln(e^x)=x ∀x∈ℝ`。
- **Property（連續）＋證**：`ln x` 連續。反證：否定連續 ⟹ ∃`δ>0`、`y_j→x_0` 使 `|ln y_j−ln x_0|≥δ`；Case 1（`ln x_0≥ln y_j+δ`）／Case 2（`ln x_0+δ≤ln y_j`）對 `e^z`（strict increasing）作用得嚴格正 gap；`ε=min{…}`；`|y_j−x_0|=|e^{ln y_j}−e^{ln x_0}|≥ε`，矛盾於 `y_j→x_0`。
- **§ The differentiability of ln x＋證**：`h=e^{ln(x+h)}−e^{ln x}`，商倒置成「`e^y` 在 `y_0` 的差分商」倒數；`y_0=ln x`、`y=ln(x+h)`；`ln` 連續＋strict ⟹ `y→y_0`、`y≠y_0`；分母 → `e^{y_0}=x`；故 `d/dx ln x=1/x`（x>0）。
- **Homework（pp.23–24，4 題；D7 升格候選）**：(1) `f'=0 on (a,b)⟹f` const（hint MVT）；(2) `ln a+ln b=ln(ab)`（hint `f(x)=ln(ax)−ln x`）；(3) 連續 `g:ℝ→ℝ⁺`、`g(x)g(y)=g(x+y)`、`g(1)=e` ⟹ `g=e^x`（Cauchy 函數方程）；(4) `a^x:=e^{x ln a}`，證 (i) `a^x b^x=(ab)^x`、(ii) `(a^x)^y=a^{xy}=(a^y)^x`。
- 具名人物／史實：**無**。worked example（§4.5 本體）：**0**（example 全在 HW）。圖：**無**。strategy／caution：**無**。

## 薄度剖析
| 區塊 | 狀態 |
|---|---|
| opener／值域斷言 | **夠但須框斷言**：`lim_{x→±∞}e^x`、range`=(0,∞)`、滿射手稿斷言不證；④ 應一句點明此依賴連續＋極限＋（IVT-型）滿射、留作斷言（§C-1） |
| Def（`ln x`）＋兩恆等式 | **夠**（標準反函數定義；④ 升格 Definition 4.4、補 informal gloss「`ln x`＝把 `e` 升到幾次方得 `x`」） |
| **`ln` domain caution** | **無**：手稿不標。**ROADMAP pitfall ＝「`ln` 只對 x>0」**（`ln 0`／`ln(−1)` undefined）→ §C-2（roadmap-mandated caution） |
| 連續性 Property＋證 | **夠**（手稿完整、雙 case＋`ε=min`；④ 具名 Theorem 4.13、維持 sequential sketch 層級） |
| 可微＋證 | **夠**（inverse-function 技巧完整；④ 具名 Theorem 4.14）。**薄在「為何不直接 chain rule」的動機**：Ch3 §3.3 已用 chain rule（假設可微）算過；④ 須點明「這次不預設 `ln` 可微、從差分商萃取」→ §C-4 Remark 4.5（關 §3.3 迴路） |
| **`e^x`/`ln x` 反射圖** | **無**：手稿純文字。**ROADMAP key figure ＝ 對 `y=x` 反射**（`e^x` blue、`ln x` red、標 `(0,1)`/`(1,0)`、`y=x` 虛線）→ §C-3（Figure 4.3，ROADMAP mandate） |
| **HW1 `f'=0⟹const`** | **薄／在 HW**：MVT 直接推論、且升格 HW2 worked example 時需用它。→ §C-5（提案 Corollary 4.4，just-in-time 置於 Example 4.5 前） |
| **HW2 `ln(ab)=ln a+ln b`** | **薄／在 HW**：§4.5 核心對數律、manuscript-faithful。→ §C-6（升格 Example 4.5；示範 `(ln)'=1/x`＋`f'=0⟹const`） |
| **HW4 `a^x` 指數律** | **薄／在 HW**：定義一般指數、收束 §4.1 D6 的 `a^r` fence。→ §C-7（升格 Example 4.6；用 HW2） |
| **HW3 Cauchy 函數方程** | **薄／在 HW、較進階**：多步（有理數逼近＋連續延拓）。→ §C-8（提案略過或降 remark） |
| **章末 Summary** | **無**：手稿無（屬 handout 章層結構件）。§4.5＝末節 → §C-9（提案產出 4-block 章末 Summary，CONTENT_SPEC §4 要求） |
| application（為何 `e^x`/`ln x` 重要） | **無**：手稿無。legacy 有（growth/decay/half-life capstone）。→ §C-10（③ 選配；章層 capstone，預設精簡或略） |

## 範圍與深度
- **吃手稿這一叢**：opener（定值域）→ Def `ln x` → 連續（證）→ 可微（證，`(ln x)'=1/x`）＋ D7 升格的 HW worked example＋ROADMAP 指派的反射圖＋章末 Summary。
- **末節、加法決策為主軸**：核心三件（Def／連續／可微）手稿全給、紮實、保留全證；**真正的方向工作在「升格哪些 HW、章末怎麼收」**（§C-5～§C-10）。
- **保留證明**（手稿全給、標準、本節主軸）：連續性反證（雙 case＋`ε`）、可微 inverse-function 技巧。兩證都**回頭依賴 `e^x` strict monotonicity**（承重直覺）。
- **斷言不證**：`e^x` range`=(0,∞)`、`lim_{x→±∞}e^x`、滿射——手稿＋legacy 皆斷言（§C-1，留作斷言＋一句依賴說明）。
- **陳述／援引不重證**：`e^x` strictly increasing（§4.4 Example 4.4，opener cross-ref、不重證）；`(e^x)'=e^x`（§4.3 Theorem 4.8，可微證的分母極限援引）；指數律 `e^{x+y}=e^x e^y`（§4.2 Theorem 4.7，HW4 升格用）；MVT（§4.4 Theorem 4.12，HW1 升格 Corollary 4.4 的根據）。
- **forward-fence（一行帶過）**：一般對數 `log_b x`／換底、`ln` 的積分定義（`∫1/t dt`，與本書「`ln`＝`e^x` 反函數」路線不同，不寫）、複數對數（out of scope）、Taylor/L'Hôpital for `ln` → 後章。
- **關 Ch3 §3.3 迴路**（ROADMAP prerequisite）：§3.3 非正式用 `ln`（Example 3.6，假設可微、chain rule 於 `e^{ln x}=x`）→ §4.5 嚴格重做（不設可微）；④ cross-ref＋Remark 4.5 點明差異。**本章不改 Ch3**（重構延後至兩章簽核後）。
- **收束 §4.1 D6**：§4.1 拋出「`a^r` for r∉ℚ?」即跳 series、把 `a^x:=e^{x ln a}` fence 到 §4.5 → HW4 升格（Example 4.6）正是收束點。

## 承重直覺（一節一個，領頭）
**Strict monotonicity 是同時「建造」與「驅動」反函數的那根槓桿。** 要把 `e^x` 反過來得到 `ln`，天真想法是「反函數自動存在、而且自動跟原函數一樣乖」——兩個都要打臉。**建造**面：反函數要良定義，需 (1) 單射（每個 `x>0` 對到唯一的 `a`，這來自 `e^x` **strict** monotonicity，§4.4 剛收割）＋(2) 滿射到 `(0,∞)`（每個正數都被打到，這來自連續＋極限，斷言）。**驅動**面更關鍵也更反直覺：`ln` 一旦定義，它的**連續性與可微性都不是免費的**——各需一個證明，而**兩個證明都回頭扳同一根槓桿**：`e^x` 的 strict monotonicity。連續性反證裡，若 `ln y_j` 不逼近 `ln x_0`，strict monotonicity 把它放大成 `e^{ln y_j}` 與 `e^{ln x_0}` 之間一道**撐開的 gap**，與 `y_j→x_0` 矛盾。可微性裡，inverse-function 技巧把差分商**倒置**成 `e^y` 的差分商倒數，而「能除」靠的是 `y≠y_0`——又是單射。**最該打臉的天真期待**：Ch3 §3.3 當時「假設 `ln` 可微、用 chain rule 在 `e^{ln x}=x` 上一步得 `1/x`」。§4.5 的整個重點是：**你不必預設可微**——可微性可以從差分商裡**萃取**出來，只用連續（剛證）＋`(e^x)'`（§4.3 證）。這就是本節的可攜技能：**inverse-function 技巧——把反函數的導數從一條代換 + 倒置的差分商裡逼出來，不靠 chain rule、不預設可微。**

## worked example 清單（提案，待 ③）
| # | 內容 | 取捨 |
|---|---|---|
| **Example 4.5** | `ln(ab)=ln a+ln b`（a,b>0）：設 `f(x)=ln(ax)−ln x`，`f'(x)=a/(ax)−1/x=0`（套 Theorem 4.14＋chain rule）⟹ `f` 常數（Corollary 4.4）⟹ `f(x)=f(1)=ln a`（`ln1=0`）⟹ 代 `x=b`：`ln(ab)−ln b=ln a` | **收（HW2 升格）**。manuscript-faithful（hint 即手稿給）；一例同時示範新導數＋`f'=0⟹const`＋對數律。**強升格候選**（D7 點名） |
| **Example 4.6** | `a^x:=e^{x ln a}`（a>0）指數律：(i) `a^x b^x=e^{x ln a}e^{x ln b}=e^{x(ln a+ln b)}=e^{x ln(ab)}=(ab)^x`（用 Example 4.5＋Theorem 4.7）；(ii) `(a^x)^y=e^{y ln(a^x)}=e^{y·x ln a}=e^{xy ln a}=a^{xy}`，對稱得 `=(a^y)^x` | **收（HW4 升格）**。manuscript-faithful；**收束 §4.1 D6 的 `a^r` fence**（D7 點名） |
| —（HW1）— | `f'=0 on (a,b)⟹f` const | **不獨立成 Example，升格為 Corollary 4.4**（§C-5）——MVT 推論、被 Example 4.5 使用、是 §4.4 monotonicity corollary 的 `f'=0` 對偶。just-in-time 置於 Example 4.5 前 |
| —（提案略過）— | HW3 Cauchy 函數方程 `g(x)g(y)=g(x+y),g(1)=e⟹g=e^x` | **提案：略過或降 remark**（§C-8）。多步（有理數逼近＋連續延拓）、非單一技巧示範、篇幅大；末節已有兩升格 example＋章末 Summary，密度足 |

> **自創題政策**：上述 Example 4.5/4.6 皆**手稿 HW 原題升格**、非自創；不產 bare your-turn exercise（root README §防護欄）。**升格鏈依賴**：Example 4.6 用 Example 4.5（`ln(ab)`）；Example 4.5 用 Corollary 4.4（`f'=0⟹const`）＋Theorem 4.14（`(ln)'`）。順序須 Corollary 4.4 → Example 4.5 → Example 4.6。

## history / application
- **history**：**提案略**（與 §4.4 一致）。對數史（Napier 1614、`e` 的故事）手稿無；末節已收尾繁重，史實在此為裝飾，留白勝 padding。③ 若要，限一句、標 `[source: standard calculus-textbook historical note]`。
- **application**：**§C-10，③ 選配**。legacy 有一段 capstone（`y'=ky⟹y=y₀e^{kt}`；growth/decay/continuously-compounded interest；half-life `t_{1/2}=ln2/|k|`），把整章機器接回「為何值得建」。**ROADMAP 未指派**（key figure/strategy 表無 application）。**提案：精簡版一段或略**——本節已有 Def＋兩證＋兩 example＋圖＋章末 Summary，full capstone 有膨脹風險；但作為**全章**收尾，一段「為何 `e^x`/`ln x` 在應用中無可迴避」確能升華。③ 取捨（建議：短版一段，或併入章末 Summary 前的一句）。

## 強調 / takeaway
- **概念樞紐**：**反函數的良好性質不是天上掉下來的——strict monotonicity 一根槓桿同時保證 `ln` 存在（單射＋滿射）、連續、可微**。三件事（定義／連續／可微）都扳同一根槓桿。
- **可攜技能**：**inverse-function 技巧**——求反函數導數時，把差分商用 `e^{ln(x+h)}=x+h` 代換、倒置成原函數的差分商倒數，取極限（靠反函數連續）得 `1/(原函數導數)`。不預設反函數可微。學生帶得走（求任何可逆函數的反函數導數）。
- **依賴鏈 takeaway（全章收束）**：`完備性(§4.1)→級數定義 e^x→連續/指數律(§4.2)→(e^x)'=e^x(§4.3)→MVT(§4.4)→e^x 嚴格遞增→ln x 定義/連續/(ln x)'=1/x(§4.5)`。本節是全章終點，把「Ch2/Ch3 非正式用過的 `e^x`/`ln x`」全部補成定理。

## 刻意不寫（餵 auditor 作 direction-conformance 反向檢查）
| 不寫什麼 | 理由 | 它該去哪 |
|---|---|---|
| **`ln` 的積分定義 `∫₁ˣ dt/t`** | 與本書路線（`ln`＝`e^x` 反函數）不同的替代建構；混用兩路線會矛盾 | —（不寫；本書走反函數路線） |
| **一般對數 `log_b x`／換底公式** | 超出手稿（只 `ln`）；HW4 的 `a^x` 是定義一般指數、非一般對數 | 後章／不寫 |
| **完整對數律表（`ln(a/b)`、`ln(a^r)=r ln a`）** | 手稿 HW 只給 `ln(ab)=ln a+ln b`；不自造完整律表 | 只升格 HW2（`ln(ab)`）；其餘至多一句「同法可得」 |
| **`e^x` range`=(0,∞)`／`lim_{x→±∞}e^x` 的嚴格證明** | 手稿＋legacy 皆斷言不證（依連續＋極限＋IVT） | 留作斷言（§C-1 一句依賴說明） |
| **複數對數 `ln(−1)`** | out of scope（實值設定）；caution 至多一句帶過 undefined | 不寫（複分析） |
| **HW3 Cauchy 函數方程完整證** | 多步、非單一技巧、末節已密 | 略過或降 remark（§C-8） |
| **Taylor for `ln`／L'Hôpital／`ln` 的積分** | 超出本節 | 後章 |
| **改寫 Ch3 §3.3 的 informal `ln`** | 重構延後至兩章簽核後；本章只 cross-ref | 未來（兩章簽核後） |
| **`ln` 的單調／凹凸／圖形完整分析** | 反射圖示意即可；完整曲線分析超出 | 不寫（圖示足） |
| 自創 bare your-turn exercise | README §防護欄禁 | —（HW 原題升格為含解 worked example） |
| **過度堆 caution／重複散文** | 末節易因「收尾」而灌水；caution 取必要者（domain `x>0`） | 保持精煉 |

## 篇幅帶（護欄非預算）
**4–6 A4 print 頁**（末節：核心短、加法 example/圖/Summary 撐起）。§4.5 ≈ opener（承 §4.4 closer：`e^x` 嚴格遞增⟹單射；strict monotonicity 是建造＋驅動反函數的槓桿）＋ Definition 4.4（`ln x`，含值域斷言§C-1＋informal gloss）＋ `ln` domain Caution（§C-2）＋ Figure 4.3（反射§C-3）＋ Theorem 4.13（連續＋證）＋ Theorem 4.14（`(ln)'=1/x`＋證）＋ Remark 4.5（vs Ch3 chain-rule，關§3.3 迴路§C-4）＋ Corollary 4.4（`f'=0⟹const`§C-5）＋ Example 4.5（`ln(ab)`§C-6）＋ Example 4.6（`a^x` 指數律§C-7）＋ （§C-10 選配 application）＋ 章末 Summary（§C-9）。**明顯超出 6 頁 → 回查是否 HW 升格過度展開／application 灌水**（末節風險＝收尾膨脹，非缺料）。ch04 數學含多行 aligned 差分商、巢狀分式（`1/[(e^y−e^{y_0})/(y−y_0)]`）→ ④ 後查 print overflow（PLAN §6）。

---

## A. 編號 ledger 提案（§4.5；接 §4.4 ledger，自 Definition 4.4／Theorem 4.13 起；④ 落定後回填 PLAN §5）

> §4.1–§4.4 已 mint：Definition 4.1–4.3、Theorem 4.1–4.12、Proposition 4.1–4.2、Corollary 4.1–4.3、Strategy 4.1–4.2、Example 4.1–4.4、Figure 4.1–4.2、Remark 4.1–4.4。各型獨立 counter、跨節連續。Caution 無編號。

| 型別 | §4.5 提案 | 說明 |
|---|---|---|
| **Definition** | `4.4`＝natural logarithm `ln x`（`e^a=x` 的唯一 `a`；`e^{ln x}=x`、`ln(e^x)=x`） | 手稿 Def；本節唯一 Definition |
| **Theorem** | `4.13`＝`ln x` continuous（反證） | 手稿 Property；維持 sequential sketch |
| | `4.14`＝`d/dx ln x = 1/x`（x>0，inverse-function 技巧） | 手稿可微小節 |
| **Corollary** | `4.4`＝`f'=0 on (a,b) ⟹ f` constant（HW1 升格） | §C-5；MVT 推論、`f'≥0⟹遞增`的 `=0` 對偶；被 Example 4.5 用 |
| **Example** | `4.5`＝`ln(ab)=ln a+ln b`（HW2 升格） | §C-6 |
| | `4.6`＝`a^x:=e^{x ln a}` 指數律 (i)(ii)（HW4 升格） | §C-7；收束 §4.1 D6 |
| **Figure** | `4.3`＝`e^x`/`ln x` 對 `y=x` 反射（`e^x` blue、`ln x` red、`(0,1)`/`(1,0)`、`y=x` 虛線） | §C-3（ROADMAP key figure；重用 Ch1 reflection setup） |
| **Remark** | `4.5`＝rigorous（本節）vs Ch3 §3.3 chain-rule 版的異同（關迴路） | §C-4（forward-loop close） |
| **Caution** | 無編號＝`ln` 只對 x>0（`ln 0`／`ln(−1)` undefined） | §C-2（ROADMAP pitfall mandate） |
| **Strategy** | **§4.5 不 mint 新 Strategy**（ROADMAP 未指派；inverse-function 技巧由 Theorem 4.14 證本身示範） | Strategy `4.3` 留給後章 |
| **Proposition** | **§4.5 不 mint 新 Proposition**（`ln(ab)` 走 Example 升格、非 Proposition——D7 default；③ 可改 Proposition 4.3，見 §C-6） | Proposition `4.3` 留給後章（或 §C-6 改判） |

> **編號自查（④）**：寫完逐一確認跨節引用都對得到存在的 `env-num`——opener「`e^x` strictly increasing（§4.4 Example 4.4）」、可微證「`(e^x)'=e^x`（Theorem 4.8）」、Corollary 4.4「MVT（Theorem 4.12）」、Example 4.5「Theorem 4.14＋Corollary 4.4」、Example 4.6「Example 4.5＋指數律 Theorem 4.7」、Remark 4.5「Ch3 §3.3 Example 3.6」。Figure 4.3 為 ch04 第三張圖（接 Figure 4.2）。

## B. 章基礎建設
**N/A** —— §4.5 非首節。chapter standalone／`fragments/ch04/` 骨架／figures（inline FIGS registry）／`build.py` ch04 entry 皆 §4.1 已建、§4.2–§4.4 沿用。§4.5 落地＝新增 `fragments/ch04/sec-4-5.html`、`build.py` 的 `CHAPTERS["ch04"].fragments` append `"sec-4-5"`、`chapter4-print-standalone.html` 嵌入式 `fragments:[…]` 同步 append（PLAN §6／§4.2–§4.4 整合實證：build.py 與 standalone 內嵌清單**須手動雙同步**）、續用手動編號 ledger。**動手前先讀 `sec-4-4.html` 末尾**確認各型 counter 收在哪（PLAN §5：Theorem 收 4.12、Definition 4.3、Corollary 4.3、Proposition 4.2、Strategy 4.2、Example 4.4、Figure 4.2、Remark 4.4）。**Figure 4.3** 照 ch04 figure 慣例（inline FIGS registry append 不覆蓋、`buildPlot` helper、label economy；反射圖含 `e^x`（blue `.curve`）＋`ln x`（red）＋`y=x`（虛線 `.refline`）＋`(0,1)`/`(1,0)` 標點）——**Figure 4.2（§4.4）已示範新增 FIGS entry＋CSS 的流程，Figure 4.3 比照**（可能需新 `.curve-log` 之類紅色 class，④ 視 CSS 現況定）。**章末 Summary**（§C-9）若收，為章層結構件、放 §4.5 fragment 末（或 standalone 章末），CONTENT_SPEC §4 格式。

## C. 待核對／存疑（③ 一併裁示）
1. **【建議：斷言＋一句依賴】`e^x` 值域＝`(0,∞)`**（seed「斷言不證」）：手稿 opener 直接寫 `lim_{x→−∞}e^x=0`、`lim_{x→∞}e^x=+∞`、range`=(0,∞)`，未證。**提案：④ 照手稿斷言，但補一句**「值域為 `(0,∞)` 來自 `e^x` 連續（Theorem 4.6）＋兩端極限＋中間值，細節從略」（legacy line 736 即此處理）。③ 確認（建議：斷言＋一句依賴說明，不展開證明）。
2. **【建議收】`ln` domain Caution（無編號）**：ROADMAP pitfall mandate——`ln x` 只對 `x>0` 定義，`ln 0`／`ln(−1)` undefined（`e^a=0`／`e^a=−1` 對實 `a` 不可能，因 `e^a>0`）；本章每個 `ln` 公式隱含 `x>0`。**提案：收為 caution**（ROADMAP 點名；與 Ch3 §3.3 同慣例）。③ 確認（建議收）。
3. **【建議收】Figure 4.3（`e^x`/`ln x` 反射）**：ROADMAP §4.5 key figure。`e^x`（blue）、`ln x`（red）對 `y=x`（虛線）反射；標 `(0,1)`（在 `e^x` 上）、`(1,0)`（在 `ln x` 上）。**提案：收**（ROADMAP mandate；視覺化反函數關係 `ln(e^x)=x`），放 Definition 4.4 後。③ 確認（建議收）。
4. **【建議收】Remark 4.5（vs Ch3 chain-rule；關 §3.3 迴路）**：Ch3 §3.3 Example 3.6 曾**非正式**用 chain rule 於 `e^{ln x}=x` 算得 `(ln x)'=1/x`（**假設** `ln` 可微）。本節嚴格重做**不預設可微**、從差分商萃取。**提案：收 Remark 4.5**，點明兩路線異同（chain-rule 快但假設可微；inverse-function 慢但附帶給出可微存在性），明文「關閉 §3.3 forward-ref 的迴路」（legacy `remark` line 807 即此）。③ 確認（建議收；ROADMAP prerequisite 要求關迴路）。
5. **【建議升格＋定位】Corollary 4.4（HW1 `f'=0⟹const`）**：HW1 是 MVT 直接推論，且 Example 4.5 升格需用它（`f'=0 ⟹ f` 常數）。**提案：升格為 Corollary 4.4**（`f` 連續 `[a,b]`、可微 `(a,b)`、`f'(c)=0 ∀c∈(a,b)` ⟹ `f` 在 `[a,b]` 常數；證：套 monotonicity Corollary 4.3 兩向，`f'≥0⟹`non-decreasing 且 `f'≤0⟹`non-increasing ⟹ 常數，或直接 MVT）。**定位：just-in-time 置於 Example 4.5 前**（不在 opener，以免延後 `ln` 焦點）。③ 裁（建議升格為 Corollary 4.4、置 Example 4.5 前）。
6. **【建議升格 Example；③ 可改 Proposition】Example 4.5（HW2 `ln(ab)=ln a+ln b`）**：manuscript-faithful（hint 即手稿給：`f(x)=ln(ax)−ln x`）。**提案：升格 worked Example 4.5**（D7 default「升格 worked example 含解」）。**③ 替代選項**：若偏好「可被後章 cite 的具名律」，改判 **Proposition 4.3「Logarithm product law」**（同一證、改 env 型別）。**建議：Example 4.5**（D7 明示 worked example；單一律未成完整律表、Example 較稱）。③ 裁型別。
7. **【建議升格】Example 4.6（HW4 `a^x` 指數律）**：manuscript-faithful；`a^x:=e^{x ln a}`，證 (i) `a^x b^x=(ab)^x`、(ii) `(a^x)^y=a^{xy}=(a^y)^x`（用 Example 4.5＋Theorem 4.7）。**收束 §4.1 D6 的 `a^r`(r∉ℚ) fence**。**提案：升格 Example 4.6**。③ 確認（建議收；D7 點名、收束 §4.1）。
8. **【建議略/降】HW3 Cauchy 函數方程**：`g:ℝ→ℝ⁺` 連續、`g(x)g(y)=g(x+y)`、`g(1)=e` ⟹ `g=e^x`。多步（有理 `g(n)=eⁿ`→`g(p/q)`→連續延拓到 ℝ）、非單一技巧、篇幅大。**提案：略過**（或至多降為一句 remark「函數方程亦可刻畫 `e^x`，從略」）。③ 裁（建議略過；末節已密）。
9. **【建議產出】章末 Summary（§4.5＝末節）**：CONTENT_SPEC §4 要求章末 Summary。**提案：§4.5 fragment 末產出 4-block 章末 Summary**——(i) exponential（級數定義／連續／指數律／導數）、(ii) real-analysis machinery（完備性／Cauchy⟺收斂／EVT）、(iii) existence theorems（Thm A／Rolle／MVT／monotonicity）、(iv) logarithm（定義／連續／導數）（legacy line 841 即四段 distillation）。③ 確認（建議產出；末節責任）。**注意 placement**：放 §4.5 fragment 末、或 standalone 章層收尾——④ 視 build 慣例定（先讀既有章是否已有 Summary 結構）。
10. **【選配】application capstone**：legacy 有一段「為何 `e^x`/`ln x` 在應用中無可迴避」（`y'=ky⟹y=y₀e^{kt}`、growth/decay/interest、half-life）。**ROADMAP 未指派**。**提案：③ 選配**——(a) 收精簡一段（章層 capstone，把 rigor 接回 why-we-care）、(b) 略（保持末節精煉）。**建議：短版一段或略**（傾向略，除非要章層升華）。③ 取捨。
11. **【方向】opener 措辭**：承 §4.4 closer（「`e^x` 嚴格遞增 ⟹ 單射 ⟹ 下節定義 `ln x`」）。**提案：opener 一段**——strict monotonicity 是同時建造（單射＋滿射⟹`ln` 良定義）與驅動（連續/可微兩證都扳此槓桿）反函數的引擎；本節定義 `ln x`、證連續、嚴格推導 `(ln x)'=1/x`，關閉 Ch3 §3.3 與 §4.1 `a^r` 兩條 forward-ref（legacy opener line 701 即此 framing）。③ 確認方向。

## D. 章層決策落地（§4.5 相關；提案＋理由，待 ③ 拍板）
- **D7 — Homework 升格 worked example。** HW1（`f'=0⟹const`）→ Corollary 4.4（§C-5）；HW2（`ln(ab)`）→ Example 4.5（§C-6）；HW4（`a^x` 指數律）→ Example 4.6（§C-7）；HW3（Cauchy 函數方程）→ 略/降 remark（§C-8）。皆 manuscript-faithful；**bare your-turn exercise 不自創**（root README §防護欄、CONTENT_SPEC §14）。
- **D6 收束 — `a^x:=e^{x ln a}`（§4.1 fence 的收束點）。** §4.1 拋出「`a^r` for r∉ℚ?」即跳 series、fence 到 §4.5；HW4 升格（Example 4.6）正式定義一般指數、收束此 fence。
- **D1 — legacy tex 當 signed 數學 cross-check。** §4.5 的 Def／連續／可微一律以 legacy §4.5 段盲算對賬（已對：逐步一致、無筆誤），不照抄散文／結構。
- **Ch3 §3.3 迴路關閉（ROADMAP prerequisite）— 只 cross-ref、不改 Ch3。** §3.3 informal `ln` forward-ref 到此；§4.5 嚴格重做＋Remark 4.5 點明差異（§C-4）。**本章不動 Ch3**（重構延後至兩章簽核後）。
- **章末 Summary（CONTENT_SPEC §4）— §4.5 末節責任。** 提案本節產出 4-block 章末 Summary（§C-9）。

---

### 結構草圖（④ 照此寫；待 ③ 定案）
§4.5 opener（承 §4.4 closer：`e^x` 嚴格遞增⟹單射；strict monotonicity 是建造＋驅動反函數的槓桿；本節定義 `ln x`、證連續、嚴格推 `(ln)'=1/x`、關 Ch3 §3.3＋§4.1 `a^r` 兩 fence〔§C-11〕）→ **Definition 4.4**（`ln x`：`e^a=x` 唯一 `a`；`e^{ln x}=x`、`ln(e^x)=x`；值域`(0,∞)`斷言＋一句依賴〔§C-1〕＋informal gloss）＋ **Caution**（`ln` 只 x>0〔§C-2〕）＋ **Figure 4.3**（`e^x`/`ln x` 反射〔§C-3〕）→ **Theorem 4.13**（`ln x` 連續＋證：反證、雙 case、`ε=min`、靠 `e^x` strict monotonicity）→ **Theorem 4.14**（`(ln x)'=1/x`＋證：inverse-function 技巧，`h=e^y−e^{y_0}`、倒置、`y→y_0` 靠連續、分母→`e^{y_0}=x`〔用 Theorem 4.8〕）＋ **Remark 4.5**（vs Ch3 chain-rule、關 §3.3 迴路〔§C-4〕）→ **Corollary 4.4**（`f'=0⟹const`，HW1〔§C-5〕，置此為 Example 4.5 鋪墊）→ **Example 4.5**（`ln(ab)=ln a+ln b`，HW2〔§C-6〕，用 Corollary 4.4＋Theorem 4.14）→ **Example 4.6**（`a^x` 指數律，HW4〔§C-7〕，用 Example 4.5＋Theorem 4.7；收束 §4.1 D6）→ （〔§C-10 選配 application capstone〕）→ **章末 Summary**（4-block〔§C-9〕；exponential／analysis machinery／existence theorems／logarithm）→ 收尾（全章閉環：Ch2/Ch3 非正式用過的 `e^x`/`ln x` 已全補成定理）。

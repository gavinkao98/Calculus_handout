# Direction Brief — §4.2 Continuity and the Exponent Law for e^x

> ② 方向提案（CONTENT_DIRECTION §2 九欄）。**狀態：待 ③ 方向閘核可**（③ 拍板後本 brief 成 ④/⑤ 契約）。
> 輸入：[`seed_ch04_s2.md`](seed_ch04_s2.md)（手稿 pp.3–10）＋ [`PLAN-ch04.md`](PLAN-ch04.md) 章層決策 D2/D3/D8/D9 ＋ ROADMAP「Chapter 4」條目（core skill #2、Bolzano–Weierstrass pitfall、兩條 resolved open question）。
> §4.2 **非首節**：不再建章基礎建設；沿用 §4.1 已建的 chapter standalone／fragments／figures.js，續編號（自 Theorem 4.3、Definition 4.2 起）。
> ①-verify：使用者選「繼續 §4.2」即視為 seed accepted-by-proceeding（pending §C 的 [請查核] 更正）。數學 cross-check：legacy `ch04_exponential_logarithm.tex` 的 §4.2 段。
> **重跑脈絡**：舊 POC `sec-4-2.html` 與舊 test-pipeline seed 已刪，本 brief 為從手稿重轉錄、併進正式章流程的全新 ②（取代首跑）。

---

## 手稿盤點（照原順序）
- **[e2]** `e^x` is continuous for `x>0`：證 `lim_{x→x₀} e^x = e^{x₀}`（x₀>0）。三段拆 `e^x−e^{x₀} = (e^x−P_k(x)) + (P_k(x)−P_k(x₀)) + (P_k(x₀)−e^{x₀})`；兩端用 §4.1 尾界 (∗)（`L=x₀+1`、`n₀>2(x₀+1)`）各 `<ε`，中項用 `P_k` 多項式連續 `<ε` → `<3ε`。
- **[e3]** `0 < e^y < +∞` for `y<0`（陳述；有限性由 (△)＋後文「observe (1)」`|e^y|≤e^(|y|)<∞` 供給）。
- **(△) Property**：`Σ|aₙ|<∞ ⟹ Σaₙ converges`。附「converges＝部分和 `Sₖ` 收斂」之定義澄清。
- **Def** Cauchy sequence：`∀ε>0 ∃N₀ s.t. |aₘ−aₙ|<ε ∀m,n≥N₀`。
- **Thm** convergent `⟺` Cauchy。**手稿明寫 punt：「we shall not prove this theorem」。**
- **(△) 的證**：用 Cauchy——`Sₙ=Σ_{1}^{n}aₖ`，`Σ_{N₀+1}^∞|aₖ|<ε ⟹ m>n>N₀ 時 |Sₘ−Sₙ|≤Σ_{n+1}^{m}|aₖ|≤Σ_{N₀+1}^∞|aₖ|<ε ⟹ {Sₙ} Cauchy ⟹ 收斂`。
- **指數律** `e^x e^y = e^{x+y}`（假設 `x,y∈[−L,L]`、`k>n₀>8L`）：
  - obs (1)：`|e^y|≤e^(|y|)<∞`、`|e^y−P_k(y)|≤|y|^k/k!`（k>n₀>2|y|）；
  - obs (2)：`P_k(x)P_k(y) = (I) + (II)`（雙和）；
  - **二項式定理**（`Cⁿ_k:=n!/(k!(n−k)!)`、`(x+y)ⁿ=Σ Cⁿ_k xᵏ y^{n−k}`）→ `(I) = P_k(x+y)`；
  - `(II)` 尾界 `≤ (2L)^(n₀)/n₀!·(1/2)^(k−n₀)` → `|P_k(x)P_k(y)−P_k(x+y)| ≤ (2L)^(n₀)/n₀!·(1/2)^(k−n₀)`；
  - 四項拆 `e^x e^y − e^{x+y} = (e^x−P_k(x))e^y + P_k(x)(e^y−P_k(y)) + (P_k(x)P_k(y)−P_k(x+y)) + (P_k(x+y)−e^{x+y})` → bound → `k→∞` 得 `[−L,L]`、`L→∞` 得全 ℝ。
- **Summary**：`e^x:=Σxⁿ/n!`（x∈ℝ）continuous 且 exponent law 對全 ℝ 成立（定義域由 §4.1 的 x>0 延拓到 ℝ）。
- 具名人物／史實：**無**。worked example：**無**。圖：**無**。

## 薄度剖析
| 區塊 | 狀態 |
|---|---|
| [e2] continuity(x>0) 證 | **夠**（手稿全證，三段拆＋(∗)＋多項式連續，標準且本節主軸） |
| **conv `⟺` Cauchy** | **手稿 punt（不證）** → ROADMAP resolved（D3①）要求 handout **展開**成完整 **Bolzano–Weierstrass ＋ monotone-subsequence** 證明（超出手稿，user-directed 2026-04-27）。**＝本節最大 expansion。** |
| (△) abs-conv⟹conv 證 | **夠**（手稿用 Cauchy 全證；但依賴鏈「(△)←conv⟺Cauchy←BW←completeness」的**直覺**薄）→ caution |
| [e3] `0<e^y<∞`（y<0）| **薄**：有限性有（(△)）；**正性 `e^y>0` 手稿未在此證**（見 §C-1） |
| `x<0`／全 ℝ 連續 | **薄**：手稿只顯證 x>0 連續，全 ℝ 連續在 Summary 一句宣告（見 §C-3：是否補具名 Theorem） |
| 指數律證 | **夠且完整**（手稿走完整二項式重組＋雙和＋四項拆＋雙重極限；ROADMAP D3② 亦要求完整 6 步——與手稿一致，**不縮成 outline**） |
| series-multiplication 的**動機**（為何要拆 (I)(II)）| **薄**（手稿直接代數展開，未說「(I) 收成 `P_k(x+y)`、(II) 是可丟的尾」的策略視角）→ 一句 strategy/prose |
| 具體計算 worked example | **無**（手稿純證明節） |

## 範圍與深度
- **吃手稿這一叢**：[e2] continuity(x>0) → [e3] → (△)＋Cauchy＋（conv⟺Cauchy）→ x<0 延拓 → 指數律。
- **保留證明**（手稿全證、標準、本節主軸）：continuity(x>0)、(△) via Cauchy、指數律（完整 6 步，D3②）。
- **核心 expansion（D3①，user-directed、超出手稿）**：把手稿 punt 的 conv⟺Cauchy **補成完整證**——completeness（§4.1 Thm 4.1）→ **Bolzano–Weierstrass**（monotone-subsequence peak argument）→ Cauchy⟹convergent（用 BW 取收斂子列）＋ convergent⟹Cauchy（易向）。深度＝把「收斂⟺Cauchy」的依賴鏈接回 §4.1 的 completeness，讓學生看到兩者**邏輯等價**（ROADMAP pitfall「Bolzano–Weierstrass dependency」）。
- **陳述不證**：completeness（§4.1 已陳述為 Theorem 4.1，本節**只援引**、不重述不重證）。二項式定理（Ch2 §2.4 已用；本節陳述記號＋直接用，不另證）。
- **forward-fence（一行帶過）**：嚴格 `(e^x)'=e^x` → §4.3（本節指數律＋連續是其前置，但**不碰差分商**）；`ln`／無理指數 → §4.5。
- **不重做 §4.1**：尾界 (∗) 直接以「§4.1 的部分和尾界」援引，**不重證**；`P_k` 記號沿用。

## 承重直覺（一節一個，領頭）
**用多項式逼近超越級數，再用幾何尾界把誤差一致壓小——多項式會的事（連續、相乘、二項式），就能搬到無窮級數上。** §4.1 掙到了 `e^x` 的存在；§4.2 要證它「行為良好」（連續、乘法相加）。兩證**同一引擎**：把 `e^x` 換成部分和 `P_k(x)`（一個多項式），用 §4.1 尾界 (∗) 讓 `|e^x−P_k(x)|` 一致地小，於是多項式的已知性質（多項式連續、`P_k(x)P_k(y)` 可用二項式重組成 `P_k(x+y)`）逐一過渡到 `e^x`，残差隨 `k→∞` 消失。continuity 的三段拆與指數律的四項拆是**同一招的兩次施展**。（對齊 ROADMAP strategy「tail-bound argument，本章多次重用」。）

## worked example 清單（提案，待 ③）
| # | 內容 | 取捨 |
|---|---|---|
| —— | §4.2 為**純證明節**，手稿無例題；證明本身（continuity、指數律）即承重 beat。 | **提案：0 個 worked example。** 多塞數值例會稀釋三條主證。③ 若要一個「具體感」錨，可考慮極小的 `e^1·e^1 = e^2`（即 `(Σ1/n!)²` 部分和 ≈ `Σ2ⁿ/n!` 部分和）數值對照 remark——**低優先、預設不收**。 |

## history / application
- **history**：**留白**（手稿無；Cauchy/Bolzano–Weierstrass 的史實註可一句帶過，**低優先、預設不放**，放則標 `[source: standard real-analysis historical note]`）。
- **application**：**留白**。§4.2 是地基證明節，無自然真實應用錨。

## 強調 / takeaway
- **概念樞紐**：**絕對收斂 ⟹ 收斂（(△)）是通往 `x<0` 的閘門**——`x<0` 時級數正負交錯、部分和不再單調，§4.1 的單調有界論證失效；(△)（其底層＝completeness 經 BW 給出的 conv⟺Cauchy）把收斂救回來，連續與指數律才能延拓到全 ℝ。
- **可攜技能**：(1) 對交錯／一般級數，用絕對收斂判收斂；(2) **partial-sum 逼近 + 尾界過渡**：要證超越函數的某性質，先對其多項式部分和證、再用 (∗) 讓誤差消失。
- **依賴鏈 takeaway**：`completeness → Bolzano–Weierstrass → (convergent ⟺ Cauchy) → (△) → e^x 在 ℝ 上 well-behaved`。

## 刻意不寫（餵 auditor 作 direction-conformance 反向檢查）
| 不寫什麼 | 理由 | 它該去哪 |
|---|---|---|
| completeness 的**重述／重證** | §4.1 Theorem 4.1 已陳述；本節只援引 | §4.1（本節 cross-ref） |
| §4.1 尾界 (∗) 的**重證** | §4.1 已證；本節一句援引 `P_k`／(∗) | §4.1 |
| 差分商 `(e^{x+h}−e^x)/h`、`lim(e^h−1)/h`、`(e^x)'=e^x` | 屬導數節 | §4.3（本節 forward-fence 一句） |
| `ln x`、無理指數 `a^x=e^{x ln a}` | 需 `e^x` 反函數＋ monotonicity | §4.5 |
| 二項式定理的**證明** | 已知工具（Ch2 §2.4 用過）；本節陳述記號＋直接用 | 陳述即可 |
| Rolle／MVT／monotonicity corollary | 屬 §4.4 | §4.4 |
| 自創 bare your-turn exercise | README §防護欄禁、deferred | —（自創一律寫成含解 worked example） |
| 把 conv⟺Cauchy 留成「不證」 | **反向**：手稿 punt，但 D3① user-directed 要**補全證**——auditor 應確認 BW＋monotone-subsequence 在場、非 outline | 本節（expansion，必寫） |

## 篇幅帶（護欄非預算）
**6–9 A4 print 頁**（比 §4.1 重：三條主證＋BW expansion；無 figure）。§4.2 ≈ 1 Theorem(continuity x>0＋證)＋1 Proposition((△)＋證)＋1 Definition(Cauchy)＋1–2 Theorem(BW＋conv⟺Cauchy＋證)＋（選配）1 Theorem(全ℝ continuity)＋1 Theorem(exponent law＋完整 6 步證)＋1 Caution(BW dependency)＋1 Strategy(援引 4.1)。**ch04 數學重（多行 aligned 級數、雙和、`\binom`）→ ④ 後特別查 print overflow**（PLAN §6）。明顯超出 9 頁 → 回查 BW 是否過度展開、或四項拆是否可收緊排版。

---

## A. 編號 ledger 提案（§4.2；接 §4.1 ledger，自 Theorem 4.3／Definition 4.2 起；④ 落定後回填 PLAN §5）

> §4.1 已 mint：Definition 4.1、Theorem 4.1（Completeness）／4.2（convergence x>0）、Strategy 4.1、Example 4.1、Figure 4.1、Remark 4.1。各型獨立 counter、跨節連續。Caution 無編號（ch02/ch03 慣例）。

| 型別 | §4.2 提案 | 說明 |
|---|---|---|
| **Definition** | `4.2`＝Cauchy sequence | 本節唯一定義 |
| **Theorem** | `4.3`＝`e^x` continuous for x>0；`4.4`＝Bolzano–Weierstrass（completeness ⟹，monotone-subsequence；**D3① expansion**）；`4.5`＝convergent ⟺ Cauchy；`4.6`＝`e^x` continuous on ℝ（延拓；**見 §C-3 取捨**）；`4.7`＝exponent law `e^x e^y=e^{x+y}` | BW/conv⟺Cauchy 的**切分顆粒度待 ③**（可合可分；提案分立以凸顯依賴鏈） |
| **Proposition** | `4.1`＝(△) absolute convergence ⟹ convergence | 手稿稱「(△) Property」；升格 Proposition（§4.1 無 Proposition，故起 4.1） |
| **Corollary** | （選配）`4.1`＝`0<e^y<∞` for y<0（[e3]） | 或降為 Remark；**見 §C-1** |
| **Strategy** | **援引 Strategy 4.1**（geometric tail）；不新增 | §4.2 兩證皆 reuse；首次 reuse 處一句回指 |
| **Caution** | 無編號＝**Bolzano–Weierstrass dependency**（conv⟺Cauchy 邏輯上等價於 completeness） | ROADMAP pitfall；高價值依賴鏈警示 |
| **Remark** | （選配）`4.2`＝為何 `x<0` 需絕對收斂（單調論證失效） | expansion；承載概念樞紐 |
| **Example / Figure** | §4.2 **無**（無 ROADMAP key figure；純證明節） | — |

> **編號自查（④）**：寫完逐一確認每個「by Theorem 4.x／Proposition 4.1／§4.1 的尾界 (∗)」都對得到一個存在的 `env-num`；跨 §4.1↔§4.2 引用尤其查（continuity 用 §4.1 (∗)、指數律用 (∗)）。**不再有舊 POC 的 renumber 問題**（POC 已刪）。

## B. 章基礎建設
**N/A** —— §4.2 非首節。chapter standalone／`fragments/ch04/` 骨架／figures.js／`build.py` ch04 entry 皆 §4.1 已建。§4.2 落地＝新增 `fragments/ch04/sec-4-2.html`、`build.py` 的 `CHAPTERS["ch04"].fragments` append `"sec-4-2"`、續用手動編號 ledger。**動手前先讀 `sec-4-1.html` 末尾**確認各型 counter 收在哪（接續機制，PLAN §5）。

## C. 待核對／存疑（③ 一併裁示）
1. **[e3] 正性 `e^y>0`（y<0）**：手稿在 [e3] 只陳述 `0<e^y<∞`，**正性未在此單獨證**。落地選項：(a) 由指數律 `e^y·e^{−y}=e^0=1>0` 得（須先有指數律與 `e^0=1`——次序上指數律在後，且 `e^0=1` 屬 §4.1 刻意不寫範圍）；(b) 由級數逐項：y<0 時無法逐項判正，故宜走 (a) 或一句「由 `e^y e^{−y}=1` 故 `e^y≠0`，連續＋`e^0=1`⟹恆正」。**提案 (a) 變體，置於指數律之後一句**。③ 確認。
2. **conv⟺Cauchy 的 BW 展開深度（D3①）**：提案完整寫 Bolzano–Weierstrass（monotone-subsequence peak argument）＋兩向 conv⟺Cauchy。**顆粒度**：分立 Theorem 4.4（BW）／4.5（conv⟺Cauchy），或合成單一帶 lemma 的 Theorem？提案**分立**（凸顯依賴鏈、對齊 ROADMAP caution）。③ 確認深度與切分。
3. **全 ℝ 連續是否升格具名 Theorem 4.6**：手稿只在 Summary 宣告全 ℝ 連續。提案補一條 **Theorem 4.6（`e^x` continuous on ℝ）**，證法＝x>0 的 [e2] 論證對任意 x₀∈ℝ 同樣成立（用 `|x₀|+1` 當 L、(∗) 對 |x| 版本）。③ 確認收或併入 Summary prose。
4. **(II) 係數收法**（seed [請查核]）：`Σ_{ℓ=k+1}^{2k}(1/ℓ!)(|x|+|y|)^ℓ ≤ (1/k!)(|x|+|y|)^k` 手稿較簡略；④ 呈現時補一句「首項主導＋幾何尾」或直接走 `≤ (2L)^(n₀)/n₀!(1/2)^{k−n₀}` 的乾淨界。④ 處理、cross-check legacy §4.2。

## D. 章層決策落地（§4.2 相關；提案＋理由，待 ③ 拍板）
- **D3① — conv⟺Cauchy 展開完整 Bolzano–Weierstrass（必做，user-directed）。** 手稿 punt；handout 補 completeness→BW（monotone-subsequence）→conv⟺Cauchy。**提案：寫**（見 §A、§C-2）。
- **D3② — 指數律完整 6 步（必做，user-directed）。** 與手稿一致（手稿本就完整）：二項式重組、(I)=`P_k(x+y)`、(II) explicit tail、四項拆、雙重極限。**不縮成 outline。**
- **D8 — 二項式記號。** 手稿 `Cⁿ_k`；本書 `\binom{n}{k}`（ROADMAP）。**提案：用 `\binom`，首見處一句 cross-ref 手稿 `Cⁿ_k`。**
- **D9 — `P_k` 部分和記號沿用**（手稿記號，§4.1–§4.2）。
- **Caution（BW dependency）＋ Remark 4.2（x<0 需絕對收斂）** 為 expansion，承載依賴鏈與概念樞紐。**提案：收**（③ 取捨）。

---

### 結構草圖（④ 照此寫；待 ③ 定案）
§4.2 開場（承 §4.1：`e^x` 在 x>0 已定義且收斂；本節證「行為良好」＝連續、乘法相加，並延拓到全 ℝ）→ **Thm 4.3** `e^x` continuous(x>0)（證：三段拆＋§4.1 尾界 (∗)＋`P_k` 多項式連續）→ **Remark 4.2** 為何 x<0 較難（交錯、單調失效）→ **Strategy（援引 4.1）** partial-sum＋tail 過渡 → **Prop 4.1** (△) abs-conv⟹conv（陳述）→ **Def 4.2** Cauchy → **Thm 4.4** Bolzano–Weierstrass（completeness⟹，monotone-subsequence）→ **Thm 4.5** convergent⟺Cauchy（用 BW）→ **Caution** BW dependency（邏輯等價 completeness）→ **Prop 4.1 的證**（用 Cauchy）→ `x<0` 延拓（由 (△)：`Σ|y|ⁿ/n!=e^{|y|}<∞`⟹`e^y` 定義）→ **Thm 4.6** `e^x` continuous on ℝ（選配）→ **Thm 4.7** exponent law（完整 6 步：obs(1)(2)、二項式、(I)=`P_k(x+y)`、(II) tail、四項拆、`k→∞`/`L→∞`）→ `e^y>0`(y<0) 一句（§C-1）→ Summary（全 ℝ：continuous＋exponent law）→ forward-ref §4.3（嚴格導數）。

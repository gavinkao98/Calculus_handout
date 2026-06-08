# Direction Brief — §3.1 Derivatives of the Sine and Cosine Functions

> ② 方向提案（RULE.md §2 九欄）。**③ 方向閘已核可（含調整），2026-06-08**——本 brief 為 ④/⑤ 契約。
> 輸入：`seed_ch03_s1.md`（手稿 pp.1–9）＋ `PLAN-ch03.md` 章層決策 D1–D4 ＋ ROADMAP「Chapter 3」條目。
> §3.1 是 ch03 **首節**：另負責建章基礎建設（見 §B）。
> ✅ ①-verify 已收（p.3 掃描）：Figure 3.1 構造／面積排序定案見 §C①。**③ 八項裁示**：tan′ 採 Example；引入 Proposition 型；面積排序見 §C①；Ch1 cross-ref 用泛指；`(1−cosθ)/θ→0` 以標準 companion limit 收；**sec′ 連帶拉進 §3.1**；Example 3.3（SHM）核准；Remark 3.1（導數四循環）收入。

---

## 手稿盤點（照原順序）
- sin 差分商 → 用 sum-to-product 化為 `(sin(h/2)/(h/2))·cos(x+h/2)`，拆成兩個子極限 (i)(ii)
- 偶函數約化（`θ=h/2`，`sinθ/θ` 為偶）→ 只需 `θ↘0`
- 夾擠原理（squeezing lemma）—— 手稿**完整重述兩形式**（`x→∞`、`x↘x₀`）
- 單位圓扇形幾何不等式 → `cosθ ≤ sinθ/θ ≤ 1` … (1)〔含 **[請查核]** 面積排序，見 §C①〕
- Example：`lim_{x→0} sin x = 0`（squeeze，`g₁=0 ≤ |sin x| ≤ |x|=g₂`）
- 連續定義 ＋ 三例：① Dirichlet 處處不連續、② `f(x)=x`、③ `f(x)=cos x`（**含證明**）
- odd/even 定義
- `lim_{θ→0} sinθ/θ = 1`（用 cos 連續 + squeeze）
- **`d/dx sin x = cos x`**（組裝）
- Claim：`sin x` 連續（**含證明**）→ **`d/dx cos x = −sin x`**
- 具名人物／史實：**無**。worked example（給函數求導型）：**無**（手稿只有上述極限/連續證明）

## 薄度剖析
| 區塊 | 狀態 |
|---|---|
| sin′／cos′ 推導與證明 | **夠**（手稿全證、標準、具啟發） |
| 承重直覺（為何代數失效、需幾何） | **薄**（手稿直接進 sum-to-product，沒點破「`sinθ/θ` 是代數破不了的 0/0」） |
| 扇形不等式圖 | **無→薄**（手稿只用文字描述圖、無實圖，且面積排序書寫不一致待查） |
| squeezing lemma | **夠**（完整重述）→ 但與 §1.5 重疊 → cross-ref（D4） |
| 連續性素材 | **過滿**（Dirichlet／`f=x`／連續定義／odd-even 定義皆 Ch1 風味）→ 瘦身（D3） |
| `d/dx tan x` | **無**（僅手稿 HW(2)(i)）→ 升格 worked example（D1） |
| `(1−cosθ)/θ → 0` | **無**（全手稿含 HW 皆無）→ expansion（D2，見 §C③ 依據存疑） |
| 用導數做計算的 worked example | **無**（無「微分這個函數」型）→ tan′ ＋（選配）一個組合計算 |
| application／takeaway 錨 | **無**（手稿純推導）→ 選配 SHM／導數循環 bookend |

## 範圍與深度
- **吃手稿這一叢**：sin′、cos′ 兩個基本三角導數，連同其所需的 `sinθ/θ→1` 與 sin/cos 連續性；加 tan′（D1）、companion limit（D2）。
- **保留證明**（短、標準、具啟發，屬 §3.1 主軸）：扇形不等式、`sinθ/θ→1`、sin/cos 連續、sin′、cos′。深度＝手稿的**直覺-嚴謹層**（幾何 squeeze，非 ε-δ）。
- **cross-ref 不重述**：squeezing lemma → §1.5（D4，只帶用到的 `θ↘0` 形式一句）；連續性「定義」與 odd/even「定義」→ Ch1（D3，不重新定義）；quotient rule（tan′ 用）→ §2.5。
- **forward-fence（一行帶過、不 preview-creep）**：`sin(g(x))`／chain rule → §3.2；`sec′`／`arcsin′`／`arctan′` → §3.3。
- **首節基礎建設**（見 §B）：章 opener、`chapter3-screen/print.html`、`figures.js` 起手。

## 承重直覺（一節一個，領頭）
**代數失效 → 幾何破局。** 多項式差分商可展開消 `h`、`eˣ` 靠級數，但 sin 差分商經 sum-to-product 後，命運全壓在 `lim_{θ→0} sinθ/θ` 上——這是個**純代數無從化簡的 `0/0`**（`sinθ` 對 `θ` 沒有可約的代數形）。要破它，必須引入**全新工具：單位圓的扇形面積夾擠**（Figure 3.1）。整節即圍繞「這道牆，與翻牆的幾何」組織：先用「代數到此為止」打臉，再用扇形不等式 + squeeze 翻過去。

## worked example 清單（③ 定案）
| # | 內容 | 技巧 | 來源 |
|---|---|---|---|
| **Example 3.1** | `lim_{θ→0} (1−cosθ)/θ = 0` | 乘 `(1+cosθ)` 共軛 → `(sinθ/θ)·(sinθ/(1+cosθ))→1·0` | **expansion（D2，標準 companion limit）** |
| **Example 3.2** | (a) `d/dx tan x = sec²x`、(b) `d/dx sec x = sec x tan x`（`x≠π/2+kπ`） | quotient rule（§2.5）on `sin/cos`、`1/cos`；(b) 重用 (a) 的 setup | **手稿 HW 升格：tan′=D1、sec′=③ 拉進** |
| **Example 3.3** | `s(t)=sin t` 簡諧運動：速度 `s′=cos t`、加速度 `s″=−sin t = −s` | sin′/cos′（只用 §3.1 導數，無 chain rule） | **expansion（③ 核准；不同題型，含解）** |
- 序：companion limit（接 `sinθ/θ→1`，同屬三角極限）→ tan & sec′（延伸導數表）→ SHM 組合（用導數）。
- tan′／sec′／companion limit 屬**忠實內容/低風險**（tan′、sec′ 皆手稿 HW）；Example 3.3 為自創 worked example（③ 已批准）。
- Example 3.2 收尾一句點明 `csc′=−csc·cot`、`cot′=−csc²` 同技巧可得（**僅敘述結果、不展開**；非手稿，避免杜撰式 worked derivation）。
- 連續性與 `sinθ/θ→1` **不**寫成 worked example，走 Proposition（見 §A 編號）。

## history / application
- **history**：無可考起源／記號故事自然觸發 → **留白**（不為 padding 硬塞；扇形 squeeze 若要一句「古典標準路徑」須帶 `[source: standard calculus-textbook]`，傾向不放）。
- **application**：選配 **bookend Remark 3.1**——sin/cos 的**導數四循環** `sin → cos → −sin → −cos → sin`，繫到簡諧運動 `s=sin t ⟹ 加速度 = −s`（**只用 §3.1 導數、不需 chain rule**；與 §2.4「eˣ 自我複製」Remark 同手法）。低風險、標準、具動機。**待 ③ 取捨**。

## 強調 / takeaway
- **概念樞紐**：`lim_{θ→0} sinθ/θ = 1` 是整節基石——所有三角導數都壓在它上，而它是**幾何（扇形面積夾擠）掙來的、非代數**。
- **可攜技能**：微分 sin、cos、tan（`→ cos, −sin, sec²`）並與 Ch2 規則組合；遇三角差分商會 reach for `sinθ/θ→1` 這個標準極限。

## 刻意不寫（餵 auditor 作 direction-conformance 反向檢查）
| 不寫什麼 | 理由 | 它該去哪 |
|---|---|---|
| `sin(g(x))`／`cos(g(x))` 等 chain-rule 應用 | chain rule 未引入（本章下一節才 state＋prove） | §3.2 |
| `sec′`／`csc′`／`cot′` | 同 tan′ 技巧但 PLAN 配置於 §3.3（D9）；§3.1 只示範 tan′ 一個 | §3.3（見 §C④） |
| `arcsin′`／`arctan′`／`ln′` | 反函數＋chain rule | §3.3 |
| 重新**定義**連續性／odd-even | Ch1 已建立 → cross-ref，不重定義（D3） | Ch1 |
| Dirichlet 處處不連續例 | Ch1 風味離題，與 §3.1 主軸無關（D3） | 降一句 remark 或略 |
| 完整重貼 squeezing lemma 兩形式 | 與 §1.5 重疊（D4） | cross-ref §1.5 |
| ε-δ 嚴格化各極限 | 超出手稿/本節深度 | Ch1 §1.6／附錄 |
| 自創 bare your-turn exercise | 受 README §防護欄禁、deferred | —（自創一律寫成含解 worked example） |
| sin/cos 高階導數做成系統小節 | 過度推廣 | 至多 Remark 3.1 的循環一句帶過 |

## 篇幅帶（護欄非預算）
**5–7 A4 print 頁**（含章 opener ≈0.5 頁）。§3.1 是全章最密（2 Prop + 2 Thm + 5–6 證明 + 1 圖 + 2–3 例 + 1 Caution + 選配 Remark），與 §2.4 同量級。明顯超出 → 回查是否某證明過度展開或漏 fence 的 forward 主題。

---

## A. 編號 ledger 提案（§3.1；④ 落定後回填 PLAN §5）
> 與 PLAN §5 提案的**兩處出入**，請 ③ 一併裁示：

| 型別 | §3.1 提案 | 說明 |
|---|---|---|
| **Theorem** | `3.1`= sin′=cos、`3.2`= cos′=−sin | Theorem 保留給本節**標題級成品**（節名即「sin/cos 導數」） |
| **Proposition** | `3.1`= sin & cos 連續於 ℝ、`3.2`= `lim sinθ/θ=1` | **新型別**（PLAN §5 ledger 無 Proposition 列）。連續性與基本極限屬**支撐結果**→ Proposition，不佔 Theorem。需在 PLAN §5 加一列。 |
| **Example** | `3.1`= companion limit、`3.2`= tan′ & sec′（兩 part）、`3.3`= SHM 組合計算 | sec′ ③ 拉進、SHM ③ 核准 |
| **Figure** | `3.1`= 扇形不等式 | |
| **Remark** | `3.1`= 導數四循環/SHM bookend | ③ 收入 |
| **Caution** | 無編號：**radian 慣例**——`sinθ/θ→1` 與 sin′=cos **只在弧度制成立**；度數制 `d/dx sin(x°)=(π/180)cos(x°)` | 標準高價值陷阱（手稿默認弧度） |
| Definition / Strategy / Corollary | §3.1 無 | 連續/odd-even 走 cross-ref（D3）；Strategy 留 §3.2/§3.3 |

- **出入①**：PLAN §5 把 tan′ 列為「(`Theorem 3.3`? 視 D1)」；本 brief 採 **Example（非 Theorem）**——忠於 D1「worked example」與手稿（HW 計算，非陳述定理）。⟹ §3.2 自 **Theorem 3.3** 起。
- **出入②**：本 brief 引入 **Proposition** 型別承載連續性與基本極限。若 ③ 不採，退路＝把兩者併入證明流程當 inline lemma（但失去可引用編號）。
- 交叉引用一律純文字；④ 寫完自查每個「Proposition/Theorem N.M」都對得到存在 `env-num`。

## B. 首節基礎建設（§3.1 session 建一次，後續節沿用；PLAN §4）
1. **`chapter3-screen.html` / `chapter3-print.html`**：複製 `template-screen/print.html`，改 CHAPTER 區塊（`dir:"exp-ch03"`、`fragments:["sec-3-1"]`、brand/runningHead＝「Chapter 3 · Chain Rule and Trigonometric Derivatives」）。`macros:{}` 視需要加 `\sec`（KaTeX 內建 `\sec`/`\tan` 有，多半免）。**PowerShell `[IO.File]::WriteAllText` UTF-8 無 BOM**。
2. **章 opener**（併入 `sec-3-1.html` 開頭，`chapter-head`+`.lead`+learning objectives）。**learning objectives 涵蓋全章**（對齊 ROADMAP core skills），草案待 ③ 核可：
   - differentiate `sin`, `cos`, `tan` and combine them with the rules of Chapter 2;
   - state the chain rule and use it to differentiate compositions `f(g(x))`, including nested ones;〔§3.2〕
   - apply logarithmic differentiation to `xˣ` and similar expressions;〔§3.3〕
   - derive the derivatives of `arcsin`, `arctan`, and `ln` from inverse-function relations via the chain rule.〔§3.3〕
   - lead 段：本章從 Ch2 的基本規則，推進到**合成**（chain rule）與其在三角／反函數導數上的應用。
3. **`exp-ch03/figures.js`** 起手：Figure 3.1 扇形不等式（inline SVG 較合適——`buildPlot` 無填充/扇形原語，比照 §2.5 Figure 2.4 schematic SVG）。label economy：圖內只留 `O, A, B`、半徑 `1`、角 `θ`、切線交點；面積/不等式進 caption 與散文。

## C. 待核對／存疑（**③ 已回覆，定案**）
1. **p.3 扇形面積排序（①-verify ✅）**：使用者提供 p.3 掃描。**定案構造**：O 圓心、`A=(1,0)`（圓∩x 軸）、`B=(cosθ,sinθ)`（圓上張角 θ）、`C=(1,tanθ)`（A 點切線 `x=1` 上，`OB` 延伸交此點，故 B 在線段 OC 上）；半徑 `OB=1`。**三面積**：`a_{△OAB}=½sinθ`、`a_{sector OAB}=½θ`、`a_{△ABC}=½(tanθ−sinθ)`（弦/弧與切線間的角落片）；整外三角 `a_{△OAC}=½tanθ=a_{△OAB}+a_{△ABC}`。**正確排序**：`½sinθ ≤ ½θ ≤ ½tanθ ⟹ cosθ ≤ sinθ/θ ≤ 1`。seed 轉錄的 `a_{△ABC} ≤ a_{sector} ≤ a_{△OAB}` **為筆誤/轉錄滑誤**（會推出 `½θ≤½sinθ`，錯）；正解 `a_{△OAB} ≤ a_{sector} ≤ a_{△OAB}+a_{△ABC}`。④ Figure 3.1 保留手稿 O,A,B,C 與 △ABC 命名，散文用標準排序（外界用 △OAC=△OAB+△ABC，或等價地「圓弓形 segment ⊆ △ABC」）。
2. **Ch1 cross-ref 目標**：③ 同意 ④ 以「**Chapter 1**」泛指（連續性定義／odd-even），不寫確切節號，待 Ch1 HTML 落地再補。
3. **D2 依據**：③ 拍板以「**標準 companion limit、低風險 expansion**」為由收錄（不引「ROADMAP 要求」）。
4. **sec′ 配置**：③ 拍板**把 sec′ 連帶拉進 §3.1**（與 tan′ 同 quotient-rule 技巧）→ Example 3.2(b)。連帶：§3.3 的 D9 清單移除 sec′（PLAN §7／§3.3 kickoff 待此 session ⑥ 後同步註記）。csc′/cot′ 非手稿、不展開，僅 Example 3.2 收尾敘述結果。

## D. 章層決策 D1–D4 落地（提案＋理由，待 ③ 拍板）
- **D1 tan′ → 收（Example 3.2a）。** ROADMAP core skill 明列「derive `d/dx tan x` using the quotient rule」；手稿 HW(2)(i) 有。寫成 worked example（`tan=sin/cos`、quotient rule、`=sec²x`），作 Example 而非 Theorem（§A 出入①，③ 核可）。**③ 加：sec′ 連帶收為 Example 3.2b**（`sec=1/cos`，手稿 HW）。
- **D2 `(1−cosθ)/θ→0` → 收（Example 3.1）。** 標準短證（共軛 `1+cosθ`）。**提案：收**；唯依據措辭見 §C③。
- **D3 連續性瘦身 → 瘦。** 保留 cos/sin 連續性**證明**（sin′/cos′ 的極限真的需要）；連續性「定義」與 odd/even「定義」**cross-ref Ch1、不重定義**；**Dirichlet 例略去（或降一句 remark）**。**提案：如述瘦身**（連續性合併為 Proposition 3.1，一次證、兩處用，避免重貼近乎相同的證明）。
- **D4 squeeze → cross-ref §1.5。** 不整段重貼夾擠原理兩形式；只在用到處一句「by the squeeze theorem (§1.5), as `θ↘0` …」。**提案：cross-ref。**

---

### 結構草圖（④ 照此寫；③ 定案）
章 opener → 開場直覺（代數失效→需幾何）→ sin 差分商拆兩子極限 → **Figure 3.1** 扇形不等式 `cosθ≤sinθ/θ≤1` ＋ `|sinθ|≤|θ|` →（squeeze cross-ref §1.5）→ **Prop 3.1** sin & cos 連續（證）→ **Prop 3.2** `lim sinθ/θ=1`（證，squeeze 收口）→ **Caution** radian 慣例 → **Thm 3.1** sin′=cos（證）→ **Thm 3.2** cos′=−sin（證）→ **Ex 3.1** companion limit `(1−cosθ)/θ→0`（D2）→ **Ex 3.2** tan′ & sec′（D1＋③ 拉進）→ **Ex 3.3** SHM 組合計算（③ 核准）→ **Remark 3.1** sin/cos 導數四循環 bookend（③ 收入）→ forward-ref §3.2 chain rule。

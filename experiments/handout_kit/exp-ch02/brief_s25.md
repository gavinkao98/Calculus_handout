# Direction Brief — §2.5 The Product and Quotient Rules

> 待 ③ direction gate 核可。輸入：`seed_ch02_s5.md`（手稿 pp. 11–13，**手稿最後一節**）＋ §2.1–§2.4 成品（校準基準，特別 `sec-2-4.html`／`sec-2-3.html` 的規則＋證明密集處理）＋ `CONTENT_ROADMAP.md` Ch2 條目。
> **ROADMAP 對齊（引用、不複述）：** core skill「use the power, constant-multiple, sum, **product, and quotient** rules to differentiate algebraic and exponential combinations」；strategy box「**Selecting among the basic rules** (§2.5)：when to use power rule vs product vs quotient；the test is the **syntactic shape** of the expression」；notation pitfall「`Δx, h` — increment notation；flag in a caution that `Δx` and `h` are synonymous in derivative contexts」（§2.2 brief 已刻意把此 caution 留到 §2.5）；pitfall「**Quotient rule asymmetry**：`(f/g)' = (f'g − fg')/g²` 對 `f,g` 不對稱、分子項序要緊」；pitfall「**`(fg)'` is not `f'g'`**：手稿開場反例 `f=x, g=x², fg=x³`，a caution preserves it as the **headline** pitfall」。Chapter 3 prereq 註記「§2.5 product rule — the chain-rule manuscript re-derives this；we cross-ref instead」→ 收尾一行 forward-fence 到 Ch3 chain rule（不偷跑）。

---

## 手稿盤點
（照原順序）
- **開場一句**：`Recall d/dx(f ± g) = d/dx f ± d/dx g`；本節學 `d/dx(fg)` 與 `d/dx(f/g)`。
- **Product rule — 打臉**：`(fg)'` **不是** `f'·g'`。**Counterexample（手稿自帶）**：`f=x, g=x²` ⇒ `fg=x³, (fg)'=3x²`；但 `f'=1, g'=2x`，故 `f'·g'=2x ≠ (fg)'`。
- **Product rule — Proof（定義法＋加減同項）**：差商分子 `f(x+h)g(x+h) − f(x)g(x)` 加減 `f(x)g(x+h)` → `= (f(x+h)−f(x))·g(x+h) + f(x)·(g(x+h)−g(x))`；除以 `h`，用極限乘法法則＋`lim_{h→0} g(x+h)=g(x)` → `(fg)' = f'g + fg'`，即 `d/dx(fg) = (d/dx f)·g + f·(d/dx g)`。
- **Product rule — Example（手稿）**：`h(x)=x·eˣ` ⇒ `h'(x)=eˣ + x·eˣ = eˣ(1+x)`（**用到 §2.4 Theorem 2.5 的 `(eˣ)'=eˣ`**）。
- **Quotient rule — Proof（定義法＋加減同項；手稿改用 `Δx` 記號）**：`f(x+Δx)/g(x+Δx) − f(x)/g(x) = (f(x+Δx)g(x) − g(x+Δx)f(x)) / (g(x+Δx)g(x))`；除以 `Δx`，分子加減 `f(x)g(x)` → `= (f(x+Δx)−f(x))g(x) − (g(x+Δx)−g(x))f(x)`；取 `Δx→0` → `d/dx(f/g) = (f'·g − f·g') / g²`。
- **無**：quotient rule 的 worked example（手稿零例）、strategy box、圖、具名人物／歷史、應用、Definition、Corollary、Remark。

## 薄度剖析
| 區塊 | 狀態 | 指向 |
|---|---|---|
| 開場「recall sum/difference rule → 轉向 product/quotient」 | **薄** | 手稿一句帶過；補 1 段承重直覺：加法／差微分乾淨地逐項拆（§2.4 已證），但乘法**不行**——天真猜 `(fg)'=f'g'` 會壞 |
| Product rule 反例（`(fg)'≠f'g'`）| **夠（內容）/ 需升格** | 手稿有完整反例；§2.4 已用**一句** prose fence 預告，本節**展成正式 env-caution**（headline pitfall）|
| Product rule Theorem + Proof | **夠** | 手稿證明完整、標準；忠實照加減同項技巧。**需補定義域前提**：`f,g` 在 `x` 可微；證明中 `lim g(x+h)=g(x)` 要點明係 `g` 可微 ⇒ 連續（§2.3 Theorem 2.1）——§2.4 audit 教訓：規則陳述別漏前提 |
| Product rule worked example | **夠（一例）** | 手稿 `x·eˣ` 照收為 Example 2.15；規則後另補**行內小示例**即時錨定 |
| Quotient rule Theorem + Proof | **夠** | 手稿證明完整；忠實照加減同項＋`Δx`。**需補定義域前提**：`f,g` 可微且 `g(x)≠0`；證明中分母 `g(x+Δx)g(x)→g(x)²≠0` 靠 `g` 連續＋`g(x)≠0` |
| `Δx ≡ h` 記號 | **薄/政策處理** | 手稿在 quotient 突然改用 `Δx`；用一句 env-caution 點明 `Δx` 與 `h` 同義（ROADMAP notation pitfall，§2.2 brief 已 defer 到此）|
| Quotient rule asymmetry | **無（需補）** | 手稿未強調；ROADMAP 指定 caution：`(f'g−fg')/g²` 對 `f,g` 不對稱、分子項序不可顛倒（符號錯置是最常見錯誤）|
| **Quotient rule worked example** | **無** | 手稿 quotient **零例題** → 教科書密度必補：至少 1 例真分式微分（見清單；須批准）|
| Strategy「selecting among the basic rules」| **無** | ROADMAP 指派本節；手稿無 → 新增 env-strategy（依 syntactic shape 選 power/product/quotient，含「先化簡再微分」的判斷）|
| 應用／歷史 | **無** | 本節為規則機制，無忠實真實錨、無可考史料 → 留白（見 history/application 欄）|

## 範圍與深度
- 吃 seed 這叢：recall sum/difference（§2.4）→ product rule（反例 caution → Theorem 2.6 ＋ proof → 例）→ quotient rule（`Δx≡h` caution → Theorem 2.7 ＋ proof → asymmetry caution → 例）→ Strategy 2.2（選規則）→ 收尾 forward-fence 到 Ch3。
- 嚴謹度：**本節證的兩條規則都「短、標準、具啟發」**，忠實照手稿的**加減同項技巧**——不另創證法、不發明引理、不引未證材料。所用工具皆已備：極限乘法法則（Ch1 §1.5）、`g` 可微 ⇒ 連續（§2.3 Theorem 2.1）、`(eˣ)'=eˣ`（§2.4 Theorem 2.5）、power rule（§2.4 Theorem 2.3）。
- forward-fence（各一行，不展開）：
  - **chain rule／合成函數的微分** → Ch3（**嚴禁偷跑**；本節只證 product/quotient）
  - trigonometric / inverse / implicit / logarithmic derivatives → Ch3–Ch4
  - product rule 的**幾何（矩形面積）詮釋** → 不放（手稿無、屬 addition；見決策 D）
  - 三個以上因子的廣義 product rule、logarithmic differentiation → 不放（over-generalization；後章）
- **嚴守**：不重證 §2.4 已證的 sum/difference/power/`eˣ` 規則（散文 recall＋交叉引用即可）；example 只用已證規則；不為了「對稱」而杜撰 quotient 的第二形式。

## 承重直覺
**一個承重直覺領頭：「乘法不逐項微分——天真的 `(fg)'=f'g'` 是錯的；正確規則是把每個函數配上**另一個**的導數（交叉項 `f'g + fg'`）。」**
- 失敗例先打臉（手稿自帶）：`f=x, g=x²` ⇒ `fg=x³`，`(fg)'=3x²`；但 `f'·g'=1·2x=2x`。`3x² ≠ 2x`——逐項相乘的猜法直接被反例堵死。這是**本章 headline pitfall**。
- 關鍵動作：用**加減同項**的代數技巧（`±f(x)g(x+h)`）把差商拆成兩塊，各自收斂到一個交叉項 → `(fg)' = f'g + fg'`。同一技巧（分子 `±f(x)g(x)`）再導出 quotient rule `(f/g)' = (f'g − fg')/g²`。
- 為它服務的次要心像：兩條規則都帶**交叉結構**（每項是「一個的導數 × 另一個」），且 quotient 的分子**不對稱**（`f'g` 在前、`fg'` 在後、帶減號）——這就是 asymmetry caution 的由來。

## worked example 清單
| # | 內容 | 技巧 | 來源 |
|---|---|---|---|
| Ex 2.15 | `h(x)=x·eˣ` ⇒ `h'(x)=eˣ(1+x)` | 套 product rule（Theorem 2.6）＋ `(eˣ)'=eˣ`（§2.4）| **手稿**（忠實照收）|
| Ex 2.16 | `f(x)=x/(x²+1)` ⇒ `f'(x)=(1−x²)/(x²+1)²` | 套 quotient rule（Theorem 2.7）；純有理、彰顯分子 `f'g−fg'` 的**項序／不對稱** | expansion:example（**新增；須批准**。新題型：quotient-rule 計算，手稿 quotient 零例。替代見決策 F）|
| Ex 2.17 *(選配)* | 三式各判該用哪條規則再微分：(a) `x³eˣ`→product；(b) `(x⁴−x)/x` **先化簡**成 `x³−1`→power（非 quotient）；(c) `x²/eˣ`→quotient | 套 Strategy 2.2（依 syntactic shape 選規則＋「先化簡」判斷）| expansion:example（**新增；須批准**。新題型：rule-selection/diagnosis，與 2.15/2.16 的單一規則計算**不同**；錨定 Strategy box）|

> **題目政策（使用者 2026-06-07 定）：** Ex 2.15 來自手稿（忠實內容）。Ex 2.16／2.17 為自創新題——依政策須 (1) **經你批准**（即此 ③ 閘）、(2) 題型與既有 example **不同**（2.16＝quotient 計算、2.17＝rule-selection；皆非換數字的同型題）、(3) 一律寫成 **worked example**（env-example＋env-solution，含完整解＋講解）。**不寫 bare your-turn exercise**。每技巧 ≥1 例：product→Ex 2.15、quotient→Ex 2.16、選規則→Ex 2.17。
> 序（預設「具體錨→診斷→建構→反思」）：product 規則後 Ex 2.15（建構）；quotient 規則後 Ex 2.16（建構，帶不對稱反思）；Strategy 後 Ex 2.17（診斷/選規則）。規則後另用**行內小示例**即時錨定（如 `d/dx(x²eˣ)=2xeˣ+x²eˣ`），打散公式牆。

## history / application
- **歷史**：無自然可考人物史觸發 → 留白。（product/quotient rule 屬標準微積分結果；Leibniz 記號史已於 §2.2 一句帶過，不重提。硬塞史料＝padding。）
- **應用**：本節為規則機制，無忠實真實錨 → 留白。`x·eˣ`、`x/(x²+1)` 等以**純數學示例**呈現即可；不硬接物理／成長模型（會重複 §2.2 的 velocity bookend，且工具未備）。

## 強調 / takeaway
- **概念樞紐**：乘法／除法**不逐項微分**——product/quotient rule 的**交叉項結構**（`f'g+fg'`、`(f'g−fg')/g²`）來自同一個加減同項技巧；quotient 分子**不對稱**。
- **可攜技能**：(1) 正確套 product rule 與 quotient rule 微分任意可微函數的積與商（含 `eˣ`／多項式組合）；(2) 面對一個算式，能依其 **syntactic shape**（並先看能否化簡）選對 power／product／quotient 規則。

## 刻意不寫
| 不寫 | 理由 | 去哪 |
|---|---|---|
| chain rule／合成函數微分 | 未引入；本節僅 product/quotient | Ch3（收尾一句 forward-fence、不 preview 內容）|
| trig / inverse / implicit / logarithmic derivatives | 未引入 | Ch3–Ch4 |
| 為 `(fg)'=f'g'` 的錯誤猜法做任何「修補式辯護」 | 它就是錯的，反例堵死即可 | 反例 caution 收掉 |
| product rule 的幾何（矩形面積增量）證明／圖 | 手稿純代數證、無圖；屬 addition，§2.4 已立「規則節不放圖」先例 | 不放（決策 D 提供選配）|
| 三因子以上廣義 product rule、logarithmic differentiation | over-generalization、需 chain/ln | 後章 |
| 重證 sum/difference/power/`eˣ` 規則 | §2.4 已證 | §2.4（recall＋交叉引用）|
| 把 quotient 寫成 `f·(1/g)` 用 product+chain 推導 | 需 chain rule（未證）；手稿用定義法直推 | 照手稿定義法；chain 版屬 Ch3 |
| **bare your-turn exercise** | README §防護欄、CONTENT_SPEC §14 | 習題設計回合 |

> 餵 auditor：以上即 direction-conformance 的反向檢查——寫進任一項＝違反方向（多寫）；漏掉「`(fg)'≠f'g'` 反例 caution／product Theorem＋proof（含 `g` 連續前提）／`x·eˣ` 例／quotient Theorem＋proof（含 `g(x)≠0` 前提）／`Δx≡h` caution／asymmetry caution／Strategy 2.2／≥1 quotient 例」＝違反方向（漏寫）。

## 篇幅帶
- 軟帶 **3–4 print 頁**（實測 §2.5 落在整章 print 的 p20–p26）。本節規則密（**2 Theorem＋2 proof＋3 Caution＋1 Strategy＋3 worked example＋1 Figure**），可讀性是寫作挑戰。比照 §2.4 的處理：每條規則前 1 段直覺、規則後行內小示例、worked example 打散公式牆；三個 caution **分散**在兩個子節（不擠在一起）。
- 明顯超出 → 回查：是否偷跑 chain rule、或把幾何詮釋／廣義 product rule 展開、或 Strategy box 過度膨脹。

---

### Numbering 銜接（承 §2.4 末尾，手動；kit 無自動 counter）
- `<h3 class="subsec-head">The product rule</h3>`
  - Caution（**headline pitfall** `(fg)'≠f'g'`；手稿反例 `f=x,g=x²`；**無編號**，比照 §2.3/§2.4 Caution）
  - Theorem **2.6**（the Product Rule：`(fg)'=f'g+fg'`；前提 `f,g` 在 `x` 可微）
    - env-proof（定義法＋加減同項 `±f(x)g(x+h)`；`lim g(x+h)=g(x)` 引 §2.3 Theorem 2.1）
  - Example **2.15**（`x·eˣ`；手稿）
- `<h3 class="subsec-head">The quotient rule</h3>`
  - Caution（`Δx ≡ h` 同義；ROADMAP notation pitfall；**無編號**）
  - Theorem **2.7**（the Quotient Rule：`(f/g)'=(f'g−fg')/g²`；前提 `f,g` 可微且 `g(x)≠0`）
    - env-proof（定義法＋加減同項 `±f(x)g(x)`；`Δx` 記號；分母 `→g(x)²≠0`）
  - Caution（**quotient asymmetry**；分子 `f'g−fg'` 對 `f,g` 不對稱、項序不可顛倒；**無編號**）
  - Example **2.16**（`x/(x²+1)`；expansion:example 新增）
- Strategy **2.2**（Selecting among the basic rules；env-strategy＋`<ol class="steps">`；接 §2.2 Strategy 2.1）
  - Example **2.17**（rule-selection；expansion:example 新增；**選配**）
- Figure **2.4**（product rule 矩形面積詮釋；**決策 D 核可加入**；inline schematic SVG，非 figures.js entry）。
- 收尾：expansion:summary 段，一句 forward-fence 到 Ch3 chain rule，並點明本節結束本章微分法則（手稿最後一節）。
- **不新增**：Definition（停 2.3）、Corollary（停 2.1）、Remark（停 2.6）。Exercise = 0。

### ③ 核可結果（2026-06-08，已回填為實際成品）
> 使用者於 ③ 方向閘核可。逐項裁決：**A/B/C/G 照 recommended**；**D → 加 Figure 2.4**（矩形面積詮釋；改我原建議「不放」）；**E → 三例全收**（2.15 手稿、2.16/2.17 新增批准）；**F → Ex 2.16 用 `x/(x²+1)`**。下方原始建議保留供追溯。

### ③ 待簽核決策（原始建議，供追溯）
- **A — 兩條規則各自的定義域前提（忠實補強）：** ✅建議 Theorem 2.6 陳述「`f,g` 在 `x` 可微」、Theorem 2.7 陳述「`f,g` 在 `x` 可微且 `g(x)≠0`」；兩證明中把手稿默用的 `lim g(x+Δx)=g(x)` **明寫**為「`g` 可微 ⇒ 連續（§2.3 Theorem 2.1）」。理由：忠實於手稿方法、補上手稿默認的前提（§2.4 audit 教訓），且用到本章自己的定理（漂亮的內部交叉引用）。不改手稿數學，只把隱含前提顯化。
- **B — 三個 caution 全做且分散：** ✅建議三個都進（皆 ROADMAP 指定 pitfall）：① `(fg)'≠f'g'`（product 子節領頭，收手稿反例）② `Δx≡h`（quotient 子節領頭，一句）③ quotient asymmetry（quotient 證後）。理由：三者都是 ROADMAP 點名的本節 pitfall，且分散在兩子節、不擠。（替代：把 `Δx≡h` 降成 prose 一句而非 box——但 ROADMAP 明寫「in a caution」，故維持 box。）
- **C — Strategy 2.2「selecting among the basic rules」內容：** ✅建議 `<ol class="steps">` 三步：(1) 看算式的**外層結構**（積？商？冪／和？）；(2) **能化簡就先化簡**（如 `(x⁴−x)/x → x³−1`，省去 quotient rule）；(3) 對應套 power/product/quotient。理由：忠實 ROADMAP「test is the syntactic shape」，並補「先化簡」這個學生常漏的判斷。
- **D — 是否放圖：** ✅建議**不放**（Figure 停 2.3）。理由：手稿無圖、product/quotient 為代數規則、§2.4 已立規則節不放圖先例、ROADMAP 未指派本節 key figure。（替代：若你要視覺紓解，唯一夠格的是 **Figure 2.4 = product rule 的矩形面積詮釋**（`Δ(fg)≈f·Δg+g·Δf` 的 L 形增量）——標準但屬 addition、且引入手稿沒用的幾何敘事；要的話我追加進 figures.js。）
- **E — worked example 批准（核心）：** Ex 2.15（手稿，product）必收。**Ex 2.16（quotient，新）建議必加**（手稿 quotient 零例，密度硬需）。**Ex 2.17（rule-selection，新）建議加但可砍**（錨定 Strategy 2.2；若你要精簡，可只留 2.15＋2.16，Strategy box 改用行內小示例示範選規則）。請逐一核可。
- **F — Ex 2.16 函數選擇：** ✅建議 `f(x)=x/(x²+1)`（純有理，與 product 例的 `eˣ` 主題區隔、最標準的第一個 quotient 例、不對稱彰顯清楚）。（替代：`eˣ/x`——串起 `eˣ` 主題、亦為真分式；你偏好哪個告訴我。）
- **G — 收尾 forward-fence 範圍：** ✅建議一句帶到 Ch3 chain rule（合成函數），**只說「下一個工具是合成函數的微分」級別、不 preview 公式或內容**；並點明 §2.5 結束本章微分法則。（ROADMAP 已記 Ch3 會 re-derive product rule 並 cross-ref 回本節，方向一致。）

### ROADMAP Open question 回填（待 ⑥ 後）
- Chapter 2 條目的三個 Open questions **皆已 resolved**；§2.5 無新增方向叉路待記。⑥ 簽核後若無新叉路，僅需（經你確認）把 Chapter 2 **Status** 由 `draft` 更新為「manuscript coverage complete（§2.1–§2.5 全數落地、各過六階＋Codex audit）」，並可在 §2.5 行補一句實作註記（比照 §2.3／§2.4 的 resolved 註記格式）。是否更新由你在 ⑥ 後拍板。

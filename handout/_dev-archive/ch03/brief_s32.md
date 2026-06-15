# Direction Brief — §3.2 The Chain Rule

> ② 方向提案（RULE.md §2 九欄）。輸入：[`seed_ch03_s2.md`](seed_ch03_s2.md)（手稿 pp.11,14–20，①-verify ✅）
> ＋ [`PLAN-ch03.md`](PLAN-ch03.md) 章層決策 D5/D6/D7/D10 ＋ ROADMAP「Chapter 3」條目。
> 設計經 3-lens design panel（pedagogy／faithfulness+numbering／ROADMAP-alignment）壓測、本檔為綜合稿。
> **③ 方向閘已核可（2026-06-08）**——本檔為 ④/⑤ 契約。§3.1 已過六階，為風格／密度／編號基準；§3.2 不負責章基礎建設（§3.1 已建）。
> **③ 四項裁示（皆採建議案）：** (1) Definition＝**Option B**（limit form cross-ref §2.2、只編 Definition 3.1＝remainder form）；
> (2) 敘事順序＝**intuition-first**（見結構草圖）；(3) **收 Figure 3.2**（composed mapping，inline SVG）；
> (4) **批准 Example 3.4＋3.5**（自創、含解、§3.2 導數庫內）。低風險預設全照 B 末段。

---

## 手稿盤點（照原順序）
- **chain rule 陳述**（p.11）：`g` 在 `x₀` 可微、`f` 在 `y=g(x₀)` 可微 ⟹ `P=f∘g` 在 `x₀` 可微、`P′(x₀)=f′(g(x₀))·g′(x₀)`。
- **Def 1**（limit form，p.14）＝§2.2 既有定義之重述；**Def 2**（remainder form，p.15）`f(x₀+h)=f(x₀)+mh+R(h)`, `R(h)/h→0`。
- **等價**：手稿只「easy to see」，**無論證**。
- **chain rule 證明**（pp.15–20）：remainder-form 串接（`m₁=g′`、`m₂=f′(g(x))`、`R₃=m₂R₁+R₂(m₁h+R₁(h))`）＋ ε-δ 推 `R₃(h)/h→0`。
- 具名人物／史實：**無**。§3.2 區塊內 worked example：**無**（手稿的應用 ln/xˣ/arcsin 置於證明前，已由 D7 移 §3.3）。
- 手稿 pp.9–11 重證 product rule＋diff⇒cont：D6 只 cross-ref Ch2、**不轉正文**。

## 薄度剖析
| 區塊 | 狀態 |
|---|---|
| chain rule 陳述＋證明 | **夠**（手稿全證、remainder-form 串接標準且具啟發） |
| 承重直覺（為何答案是乘積、naive 證法為何壞） | **薄**（手稿直接進 Def2 串接，沒點破「rates multiply＝linear approximations compose」、也沒講 naive 除以 `g(x+h)−g(x)` 遇增量為零會壞） |
| Def1⇔Def2 等價 | **薄**（手稿「easy to see」留白）→ 補忠實雙向短證 |
| composed-mapping 圖 | **無**（ROADMAP key figure、手稿無圖）→ expansion 候選 |
| 用 chain rule 的 worked example | **無**（手稿 §3.2 區塊無；應用在 §3.3）→ decomposition example 候選 |
| Leibniz form／decomposition strategy | **無**（ROADMAP 指派）→ expansion |
| ε-δ 尾段的兩個跳步 | **薄**（手稿跳步）→ 補標準補步（`expansion:formula`），seed 已標 |

## 範圍與深度
- **吃手稿這一叢**：chain rule 陳述、Def2（remainder form）、Def1⇔Def2 等價、remainder-form 證明（ε-δ tail）。深度＝手稿的**直覺-嚴謹層**（只跑手稿那一個 tail bound 估計，**不**額外 ε-δ 化）。
- **cross-ref 不重述（D6）**：product rule→Ch2 §2.5；diff⇒continuous→Ch2 §2.3 Theorem 2.1。開節一句帶過、不重證。
- **forward-fence（一行、D7）**：ln/xˣ/arcsin/arctan → §3.3（含 logarithmic differentiation）。不做任何應用、不引入 implicit-diff（D10）。
- **加法（待 ③）**：composed-mapping **Figure 3.2**、**Strategy 3.1**（decomposition）、**Example 3.4–3.5**（decomposition worked examples）、**Remark 3.2**（Leibniz form）、**Caution**（忘內層導數）。

## 承重直覺（一節一個，領頭）
**Rates multiply, because local linear approximations compose.** 在一點附近，可微函數≈其切線（把增量乘上斜率），誤差比增量更快趨零（這正是 remainder form）。把 `g` 餵進 `f`：`g` 把 `h` 放大 `g′(x)` 倍，`f` 再把 `g` 的輸出增量放大 `f′(g(x))` 倍——兩段放大相乘＝`f′(g(x))·g′(x)`。整個證明就是「兩段誤差 R 串接後仍比 `h` 更快趨零（`R₃(h)/h→0`）」的記帳。此單一心像**三用**：(a) 解釋答案為何是乘積、(b) 預先解釋 Leibniz `dy/dx=dy/du·du/dx`、(c) 即 remainder-form 證明的策略（R＝線性近似忽略的誤差）。Leibniz「約掉 du」看似證明其實不是——這是**警示**（收 Remark），不當領頭。

## worked example 清單（**待 ③ 批准**；皆自創 worked example、含解；數學已核）
| # | 內容 | 技巧 | 來源／範圍 |
|---|---|---|---|
| **Example 3.4** | (a) `√(1+x²)`、(b) `sin(x²)` | 單層 composition（Strategy 3.1）：outer-at-inner × inner。(a) `½(1+x²)^(−1/2)·2x = x/√(1+x²)`；(b) `cos(x²)·2x = 2x cos(x²)` | 自創；兌現章 opener／§3.1 收尾承諾的 `√(1+x²)`、`sin(x²)`。(b) 即「忘內層導數」陷阱現場。只用 power（Ch2）＋sin′（§3.1） |
| **Example 3.5** | `√(1+sin²x)`（三層巢狀） | iterated chain rule（Strategy 3.1 step 5）：`½(1+sin²x)^(−1/2)·2sin x·cos x = (sin x cos x)/√(1+sin²x)` | 自創；**不同題型**（≥3 層巢狀，兌現 ROADMAP core skill「f(g(h(x)))」）。只用 sqrt/power（Ch2）＋sin′（§3.1） |
- 序：單層（兌現承諾＋陷阱）→ 三層巢狀（迭代）。皆嚴格在 **§3.2 導數庫**內（sin/cos §3.1、power/product/quotient/eˣ Ch2）——**零** ln/arcsin/xˣ 滲漏（D7）。
- 自創題政策（2026-06-07）：須 ③ 批准、題型與既有 example 不同、寫成含解 worked example、**不產 bare exercise**。**兩例皆待你 ③ 批准。**
- 替代選項（待 ③）：Example 3.4 也可改 `sin(x²+1)`／`(x²+1)⁵`；Example 3.5 也可改 `cos((x²+1)⁴)`／`sin³(2x)`。

## history / application
- **history**：chain rule 的 Leibniz 記號可一句帶（`dy/dx=dy/du·du/dx`），但屬記號非可考史實 → 把它當 **Remark 3.2 的工作記號**處理（非 history）。**留白勝 padding**（同 §3.1）。
- **application**：chain rule 本身即工具，worked example 即其應用；無另設真實情境錨之需。**留白**。

## 強調 / takeaway
- **概念樞紐**：chain rule＝「rates multiply」，由 **remainder form** 嚴格化（線性近似可串接）。remainder form 把「可微」轉成「可線性近似且誤差受控」，而線性近似乾淨地串接。
- **可攜技能**：把任何 composition 拆成 outer∘inner、微分為 `f′(g(x))·g′(x)`、巢狀則迭代；認得野生的 composition、**永不漏內層導數**。

## 刻意不寫（餵 auditor 作 direction-conformance 反向檢查）
| 不寫什麼 | 理由 | 它該去哪 |
|---|---|---|
| product rule 重新陳述／重證 | 已 Ch2 §2.5；手稿 pp.9–11 重證了，我們只一句 cross-ref（D6） | Ch2 §2.5 |
| diff⇒continuous 重新陳述／重證 | 已 Ch2 §2.3 Thm 2.1；證明用到時只 cross-ref（D6） | Ch2 §2.3 Thm 2.1 |
| ln x／xˣ／arcsin/arctan 的**任何**應用 | chain rule 的應用屬下一節（D7） | §3.3（至多一句 forward） |
| logarithmic differentiation | 同上（D7） | §3.3 |
| implicit-differentiation 框架／詞彙 | 照手稿 composition-identity，不引入（D10） | 未來專章 |
| 另創 chain rule 證法（如 naive 乘除 `g(x+h)−g(x)`，遇增量為零會壞） | 須照手稿 remainder-form 串接（m₁/m₂/R₁/R₂/R₃），忠實 | — |
| 重新編號 limit form 為 Ch3 新 Definition | §2.2 已有；只 cross-ref（見 A. Option B） | §2.2 |
| 額外 ε-δ 化（等價、極限律） | 超出手稿/本節深度（只跑手稿那個 tail bound） | Ch1 §1.6／附錄 |
| bare your-turn exercise | README §防護欄禁、deferred | 自創一律含解 worked example |
| 高階／多變數 chain rule、Faà di Bruno | 過度推廣 | — |

## 篇幅帶（護欄非預算）
**4–6 A4 print 頁**（無章 opener，比 §3.1 的 7 頁輕：1 Theorem＋1 長證明＋1 Definition＋1 Proposition（短證）＋1 Figure＋1 Strategy＋2 worked example＋1 Remark＋1 Caution）。密度風險＝chain rule 證明的 ε-δ tail（≈1–1.5 頁）；明顯超出 → 回查 tail 是否過度展開、或 §3.3 應用滲漏。砍 Example 3.5 → 約 4 頁低端。

---

## A. 編號 ledger 提案（§3.2；④ 落定後回填 PLAN §5）
> 續編自 §3.1 末尾（讀 `sec-3-1.html` header ledger 確認）。**與 PLAN §5 一處出入**，請 ③ 裁示（見 B.1）：

| 型別 | §3.2 提案 | 說明 |
|---|---|---|
| **Theorem** | `3.3`＝chain rule | headline；接 §3.1 Theorem 3.2 |
| **Proposition** | `3.3`＝Def1⇔Def2 等價 | 接 §3.1 Proposition 3.2；編號讓證明可引用 |
| **Definition** | `3.1`＝remainder form（**只此一個**） | **出入**：PLAN §5 暫列「Def 3.1/3.2（Def1/Def2）」；本提案採 **Option B**——limit form 只 cross-ref §2.2、不重新編號，只把 remainder form 編 Definition 3.1。理由：ROADMAP 註明 Def 1 已建於 §2.2，重編＝複製既有結果（違 D6 精神）。**待 ③ 裁 A/B。** |
| **Example** | `3.4`＝單層、`3.5`＝三層巢狀 | 接 §3.1 Example 3.3；皆自創、待 ③ 批准 |
| **Figure** | `3.2`＝composed mapping | 接 §3.1 Figure 3.1；待 ③ 取捨 |
| **Remark** | `3.2`＝Leibniz form | 接 §3.1 Remark 3.1 |
| **Strategy** | `3.1`＝chain-rule decomposition | 本章首個 Strategy（ROADMAP 指派） |
| **Caution** | 無編號＝忘內層導數 | 沿用 ch02 慣例 |

- 交叉引用一律純文字（"by Theorem 3.3"、"§2.2 的 limit 定義"、"Ch2 §2.5 product rule"、"Ch2 §2.3 Theorem 2.1"、"§3.1 的 sin′"）；④ 寫完自查每個引用都對得到存在 `env-num`。seed 已標 [請查核] cross-ref 確切號（§2.2/§2.3/§2.5），④ 對 Ch2 成品再核。

## B. 待 ③ 裁示（design panel 三視角綜合；附建議）
> **✅ ③ 已核可（2026-06-08）：四項皆採建議案——B.1 Option B、B.2 intuition-first、B.3 收 Figure 3.2、B.4 批准 3.4+3.5；低風險預設全照末段。**

1. **Definition 處理（A/B）**：**建議 Option B**（limit form cross-ref §2.2、只編 Definition 3.1＝remainder form），替代 Option A（兩個 Definition 3.1 limit／3.2 remainder＝PLAN §5 原列）。三視角一致選 B。
2. **敘事順序**：**建議「intuition-first」**——opener →（**Thm 3.3 陳述 → Figure → Remark → Strategy**，先讓規則可用）→ bridge →（**Def 3.1 → Prop 3.3 → Proof**，把 ε-δ tail 隔離）→（**Ex 3.4＋Caution → Ex 3.5**，練習）→ forward。手稿 statement→def→proof 主軸保持**連續**（忠實），usability（圖/記號/recipe）前置、練習殿後。替代＝§3.1 嚴格式（def＋proof 全先、其餘後）。
3. **Figure 3.2（composed mapping）**：**建議收**（ROADMAP key figure、畫出承重直覺；inline SVG，比照 §3.1 Fig 3.1／§2.5 Fig 2.4，`buildPlot` 無三軸放大原語）。替代＝純散文（rules 節可無圖，如 §2.5 原本、後經你 override 加 Fig 2.4）。
4. **Worked examples**：**建議批准 Example 3.4（`√(1+x²)`, `sin(x²)`）＋ 3.5（`√(1+sin²x)` 巢狀）**，皆自創、皆在 §3.2 導數庫內。或只留 3.4（§3.2 更輕）。

**低風險預設（如你不另指，④ 照此走）：** 等價收 **Proposition 3.3**（非 inline）；Leibniz 收 **Remark 3.2**（非 Caution）；ε-δ tail **補手稿略去的兩步**（`expansion:formula`、自足）；陳述用 `f′(g(x))·g′(x)` 序、證明保手稿 `(g′(x)f′(g(x)))` 序並一句註交換律；Example 3.4 **先寫錯解 `cos(x²)` 再更正**以釘陷阱。

## C. 章層決策 D5/D6/D7/D10 落地（確認）
- **D5**：Def2（remainder form）在 §3.2 引入（chain rule 證明所需）、證 Def1⇔Def2 等價後只用 Def2 證 chain rule。→ 落 Definition 3.1＋Proposition 3.3。ROADMAP open question「Def2 placement」於此 **resolved**（⑥ 回填）。
- **D6**：product rule（§2.5）／diff⇒continuous（§2.3 Thm 2.1）只 cross-ref、**不重證**。→ 開節一句、刻意不寫第 1–2 條。
- **D7**：應用（ln/xˣ/arcsin）留 §3.3，§3.2 至多一句 forward。→ 刻意不寫第 3–4 條。
- **D10**：不引入 implicit-diff 框架。→ 刻意不寫第 5 條。

---

## 結構草圖（④ 照此寫；待 ③ 定案；以下為 B.2 建議的 intuition-first 序）
opener（composition wall＋rates-multiply 直覺；一句 D6 cross-ref §2.5/§2.3；一句 D7 forward §3.3）
→ **Thm 3.3** chain rule 陳述（`P′(x₀)=f′(g(x₀))·g′(x₀)`）
→ **Figure 3.2** composed mapping（三軸：小 h 經 `g′` 再經 `f′` 放大，斜率相乘）
→ **Remark 3.2** Leibniz form `dy/dx=(dy/du)(du/dx)`（＋「約 du 是助記非證明」）
→ **Strategy 3.1** chain-rule decomposition（5 步：認外層→寫 f(g(x))→`f′(g(x))`→×`g′(x)`→巢狀迭代）
→ bridge（「規則已可用；接下來賺到它——需要可乾淨相乘的 differentiable 形式」）
→ **Def 3.1** remainder form（一句 cross-ref §2.2 limit form，不重編）
→ **Prop 3.3** Def1⇔Def2 等價（雙向短證，`expansion:formula`）
→ **Proof of Thm 3.3**（remainder-form 串接 S1–S6：expand g→expand f→collect R₃→Step① `m₂R₁/h→0`→Step② ε-δ→conclude；補兩跳步）
→ **Ex 3.4** 單層（`√(1+x²)`, `sin(x²)`）＋ **Caution** 忘內層導數
→ **Ex 3.5** 三層巢狀（`√(1+sin²x)`）
→ 收尾 forward §3.3（ln/arcsin/xˣ 解鎖）。
> **替代序（§3.1 嚴格式，待 ③）**：opener →（Def 3.1＋Prop 3.3）→ Thm 3.3 → Strategy → Proof → Figure → Ex 3.4/3.5 → Remark/Caution → forward。

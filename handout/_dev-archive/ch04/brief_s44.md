# Direction Brief — §4.4 Rolle's Theorem and the Mean Value Theorem

> ② 方向提案（CONTENT_DIRECTION §2 九欄）。**狀態：待 ③ 方向閘核可**（③ 拍板後本 brief 成 ④/⑤ 契約）。
> 輸入：[`seed_ch04_s4.md`](seed_ch04_s4.md)（手稿 pp.11–18）＋ [`PLAN-ch04.md`](PLAN-ch04.md) 章層決策（D4 MVT 留本章、編號 ledger）＋ ROADMAP「Chapter 4」條目（core skill「state and prove Rolle/MVT；用 MVT 證 `f'≥0⟹increasing`」、key figure＝MVT secant–tangent、strategy＝套 MVT 前驗 hypotheses）。
> §4.4 **非首節，且為全章最重、最多證明的節**（4 條 Theorem＋1 Definition＋1 Corollary＋key figure＋strategy＋2 Example）：核心風險與 §4.3 **相反**——不是過度展開，而是**這條 Thm A → Rolle → MVT → Corollary 的證明階梯每一階都要紮實、不可跳步**。沿用 §4.1–§4.3 已建的 chapter standalone／fragments／figures.js，續編號（自 Definition 4.3、Theorem 4.9 起）。
> ①-verify：使用者選「現在開跑 §4.4」即視為 seed accepted-by-proceeding（pending §C-1／§C-2 兩處 [請查核] 更正）。數學 cross-check：legacy `ch04_exponential_logarithm.tex` §4.4 段（`sec:rolle-and-mvt`，lines 538–696）＋ §4.5 開頭 monotonicity corollary（`cor:monotonicity`，lines 705–727）。

---

## 手稿盤點（照原順序，pp.11–18）
- **§ Rolle's Theorem**（手稿標題；handout 改 §4.4「Rolle's Theorem and the Mean Value Theorem」）。
- **Def 1（max/min point）**：`f(x_0)` 為 `f` 在 `D` 上的 maximum 若 `x_0∈D` 且 `f(x_0)≥f(x) ∀x∈D`（紅筆對偶 minimum／`≤`）。
- **Ex（`cos x`）**：`0` 是 `cos x` 的 maximum point、maximum value `=1`（`1=cos0≥cos x ∀x∈ℝ`）。
- **Fact（EVT）**：`f` 連續 on `[a,b]` ⟹ 有 max point `X_M∈[a,b]`、min point `X_m∈[a,b]`。手稿明言「依完備性、論證冗長、暫不證」。
- **Thm A（interior extremum）**：`X_M∈(a,b)` 為 max、`f'(X_M)` 存在 ⟹ `f'(X_M)=0`。證：`f(X_M+h)−f(X_M)≤0` ⟹ `h>0` 商 `≤0`、`k<0` 商 `≥0` ⟹ 兩單邊極限逼出 `f'(X_M)=0`。
- **Rolle**：`f` 連續 `[a,b]`、可微 `(a,b)`、`f(a)=f(b)` ⟹ `∃c∈(a,b), f'(c)=0`。證：EVT 取 `X_m,X_M`；Case 1（`m=M=f(a)=f(b)` ⟹ 常數）／Case 2（`m<M` ⟹ max 或 min 嚴格在端點值外 ⟹ 該極值點 interior ⟹ Thm A）。
- **MVT**：`f` 連續 `[a,b]`、可微 `(a,b)` ⟹ `∃c∈(a,b), f'(c)=(f(b)−f(a))/(b−a)`。證：輔助 `g(x)=f(x)−[f(a)+((f(b)−f(a))/(b−a))(x−a)]`（割線差）；`g(a)=g(b)=0` ⟹ Rolle ⟹ `g'(c)=0` ⟹ 結論。
- **Corollary（monotonicity）**：`f'≥0 on (a,b)` ⟹ `f(x_2)≥f(x_1)` for `a≤x_1<x_2≤b`。證：MVT 於 `[x_1,x_2]`。
- **Example**：(i) `(sin x)'=cos x>0` on `[0,π/4]` ⟹ `sin x_2>sin x_1`；(2) `(e^x)'=e^x>0 ∀x∈ℝ` ⟹ `e^{x_2}>e^{x_1}` ⟹ **`e^x` strictly increasing on ℝ**（紅筆方括重點；交棒 §4.5）。
- 具名人物／史實：**無**（Rolle/MVT 皆有可考史，手稿未提）。worked example：**1 個 Example 區塊（i/ii 兩項）**。圖：**無**。strategy／caution：**無**。

## 薄度剖析
| 區塊 | 狀態 |
|---|---|
| Def（max/min）＋`cos x` 例 | **夠**（標準定義＋具體錨；④ 升格 Definition 4.3） |
| EVT「Fact」 | **夠但須具名＋框邊界**：手稿陳述不證即可，但 ④ 應具名 Theorem 4.9、cross-ref 完備性（Theorem 4.1）、一句點明「closed＋continuous 兩條件皆必要」（legacy remark 有反例）→ §C-3 |
| Thm A＋證 | **夠**（手稿全給、標準雙單邊極限論證；④ 具名 Theorem 4.10、補一句「interior 必要」caution＝§C-6a） |
| Rolle＋證 | **夠**（手稿 Case 1/2 完整；④ 修 §C-1 的 (ii) `X_M→X_m` 筆誤、具名 Theorem 4.11） |
| MVT＋證 | **夠**（輔助 `g` 標準；④ 具名 Theorem 4.12）。**薄在「為何要這個 `g`」的動機**：手稿直接寫出 `g`，未說「`g` 是曲線減割線、把 MVT 化約成 Rolle」→ ④ 補一句幾何動機（§C-4 圖＋一句散文） |
| **MVT 幾何圖** | **無**：手稿純文字。**ROADMAP key figure ＝ 割線–切線圖**（割線 dashed、內部 `c` 平行 tangent solid）→ §C-4（ROADMAP 指派、Figure 4.2） |
| **套 MVT 的 hypotheses 驗證程序** | **無**：手稿不給。**ROADMAP strategy ＝「套 MVT 前驗 [a,b] 連續＋(a,b) 可微」**（不對稱）→ §C-5（Strategy 4.2；`|x|` on `[−1,1]` 反例） |
| Corollary 的 **strict 版** | **薄／有缺口**：手稿陳述非嚴格（`≥`）、Example 卻下嚴格（`>`）。§4.5 需 `e^x` **strictly** increasing（單射）→ §C-2（補 strict 條，legacy 即雙條） |
| `e^x>0 ∀x` 的依據 | **薄**：Example (2) 直接寫 `e^x>0` 未述理由（`x≥0` 級數正、`x<0` 指數律 `1/e^{−x}`）→ §C-7（補一行） |
| 「on every `[a,b]` ⟹ on ℝ」的跳步 | **薄**：Example (2) 由任意閉區間嚴格增推 ℝ 上嚴格增 → §C-6c（一句 note，legacy 有對應 caution） |

## 範圍與深度
- **吃手稿這一叢**：max/min Def → EVT（陳述不證）→ Thm A → Rolle → MVT → monotonicity Corollary → 兩 Example（sin、`e^x`），**收在「`e^x` strictly increasing on ℝ」**（交棒 §4.5）。
- **全章最重節、證明階梯為主軸**：Thm A → Rolle → MVT 三條環環相扣（每條都化約成前一條），**所有證明都保留、都要紮實**——這正是 ROADMAP core skill「state and prove Rolle/MVT」。不可把任一證明降為「陳述不證」（EVT 例外，手稿本就不證）。
- **保留證明**（手稿全給、標準、本節主軸）：Thm A 雙單邊極限、Rolle Case 1/2、MVT 輔助 `g`、Corollary 套 MVT。
- **EVT 唯一陳述不證**：手稿明言、完備性依賴、論證冗長——具名 Theorem 4.9、cross-ref 完備性、當 black box 用。
- **陳述／援引不重證**：導數定義（Ch2，Thm A 證用之）、§4.3 `(e^x)'=e^x`（Theorem 4.8，`e^x` example 援引）、§4.2 指數律（`e^x>0` for `x<0` 的根據，§C-7 一行）、§4.1 完備性（Theorem 4.1，EVT 的根據，cross-ref）。
- **forward-fence（一行帶過）**：`ln x` 建構（需 `e^x` 單射）→ §4.5；Taylor／高階 MVT／L'Hôpital → 後章；本節**只交棒「`e^x` strictly increasing」給 §4.5**。
- **不移走 MVT**（D4）：手稿把 Rolle/MVT 夾在指數章因 `ln` 需單調性；本章保留，未來 applications 專章再於 Mode B 僅提議移動——本節不動此決定。

## 承重直覺（一節一個，領頭）
**MVT 是「逐點導數資訊」通往「整段函數行為」的橋——而且是一條 existence 定理（只保證有個 `c`、不告訴你 `c` 在哪）。** 你不能光盯著導數值就斷言「`f'≥0 ⟹ f` 遞增」：導數是**一點**的資訊，遞增是**一整段**的性質，中間缺一座橋。MVT 就是那座橋：`(f(b)−f(a))/(b−a)=f'(c)` 把「兩端點的平均變化率」釘在「某內部點的瞬時變化率」上。幾何上——**某條內部切線必與割線平行**（§C-4 圖）。而整個證明是一招漂亮的化約階梯：**MVT「減掉割線」化約成 Rolle（兩端等高）→ Rolle 化約成「內部極值點導數為 0」（Thm A）→ Thm A 是雙單邊極限一逼即得**。三條定理像三節階梯，每節踩在前一節上。**這座橋一旦架好，立刻收割：`f'≥0 ⟹ 遞增`（Corollary），再套到 `e^x`（`(e^x)'=e^x>0`）就得 `e^x` 嚴格遞增——正是 §4.5 定義 `ln x` 所缺的最後一塊。** existence（不指明 `c`）這點要先打臉天真期待：MVT 不是給你 `c` 的公式，是保證 `c` 存在，後續論證**只能用存在性、不能用某個特定 `c`**（§C-5 strategy 第 3 條）。

## worked example 清單（提案，待 ③）
| # | 內容 | 取捨 |
|---|---|---|
| **Example 4.2(i)** | `sin x` on `[0,π/4]`：`(sin x)'=cos x>0` ⟹ `sin x_2>sin x_1`（strictly increasing） | **收**（手稿原有；Corollary 的第一個應用、低風險具體錨） |
| **Example 4.2(ii)** | `e^x` on ℝ：`(e^x)'=e^x>0` ⟹ `e^{x_2}>e^{x_1}` ⟹ **`e^x` strictly increasing on ℝ** | **收（承重）**（手稿原有；本節**通往 §4.5 的交棒點**，必收。§C-7 補一行 `e^x>0` 依據；§C-6c 一句「every `[a,b]`⟹ℝ」） |
| —（提案略過）— | 額外的「直接套 MVT」數值 worked example（如某 `f` 在 `[a,b]` 找 `c`） | **提案：不加**。本節已 3 證＋Corollary＋圖＋strategy＋2 例，密度足；strategy 的 `|x|` on `[−1,1]` 反例已示範 hypothesis-checking。加數值例有 over-expansion 風險。③ 若要一個「正面套 MVT」錨，可考慮極小一例（如 `f(x)=x²` on `[0,2]`，`c=1`）——**低優先、預設不收**。 |

> **自創題政策**：上述兩 Example 皆手稿原有、非自創；不產 bare your-turn exercise（root README §防護欄）。

## history / application
- **history**：**提案一句、可選**。Rolle's theorem 名出 Michel Rolle（1691，原為多項式情形）；MVT 的現代形式由 Cauchy 形式化。**手稿無此**——若收，須標 `[source: standard calculus-textbook historical note]`、限一句、不展開。**預設：略**（本節已密、史實在此為裝飾，留白勝 padding）。③ 取捨。
- **application**：**本節的 application 就是 Corollary 本身**（`f'≥0⟹遞增`）＋兩 Example——MVT 的「真實用途」是內部的單調性收割，非外部情境。**不另放裝飾性 real-world application**（避免稀釋證明階梯）。

## 強調 / takeaway
- **概念樞紐**：**existence 定理把逐點導數翻成整段行為**——MVT 是微分學「由量化導數資訊抽取定性函數資訊」的中央引擎（後續 Taylor、L'Hôpital、單調性／凹凸全經它）。Thm A→Rolle→MVT 是「化約到更簡單情形」的範例階梯。
- **可攜技能**：(1) **套 MVT/Rolle 前先驗 hypotheses**（[a,b] 連續、(a,b) 可微，兩者不對稱；§C-5 strategy）；(2) **「減掉割線」把一般情形化約成對稱情形**（MVT→Rolle 的 `g` 技巧，後續證明常用）；(3) **existence 結論只能用存在性**（MVT 不給特定 `c`）。
- **依賴鏈 takeaway**：`完備性（§4.1）→ EVT → Thm A → Rolle → MVT → (f'≥0⟹遞增) → (e^x)'=e^x>0（§4.3）⟹ e^x 嚴格遞增 → §4.5 定義 ln x`。本節是這條鏈的中段樞紐。

## 刻意不寫（餵 auditor 作 direction-conformance 反向檢查）
| 不寫什麼 | 理由 | 它該去哪 |
|---|---|---|
| **`ln x` 的建構／定義／導數** | 需 `e^x` 單射（本節交棒「strictly increasing」即止） | §4.5 |
| **EVT 的證明** | 完備性依賴、論證冗長；手稿＋legacy 皆陳述不證 | 留白（當 black box，cross-ref 完備性） |
| **Taylor 定理／高階 MVT／Cauchy MVT** | 超出本節；MVT 的推廣 | 後章 |
| **L'Hôpital 法則** | 用 MVT/Cauchy MVT，屬後章 | 後章 |
| **§4.3 `(e^x)'=e^x` 的重證** | Theorem 4.8 已證；`e^x` example 只援引 | §4.3（cross-ref） |
| **把 MVT 移出 Ch4** | D4：本章保留；移動只在未來 applications 專章 Mode B 提議 | 未來 Mode B |
| **積分／反導數框架的單調性** | 本節單調性走 MVT，非積分（積分未建） | —（不寫） |
| **凹凸／二階導數判別法** | 超出本節（一階單調性即止） | 後章 |
| 自創 bare your-turn exercise | README §防護欄禁 | —（自創一律寫成含解 worked example） |
| **過度堆 caution／重複散文** | 本節已密；caution 取必要者（§C-6），勿每個假設都加框 | 保持精煉 |

## 篇幅帶（護欄非預算）
**4–6 A4 print 頁**（全章最重節）。§4.4 ≈ opener（承 §4.3 closer 的 forward-fence：單調性需 `(e^x)'>0、下節 Rolle/MVT）＋ Definition 4.3（max/min）＋`cos x` 例 ＋ Theorem 4.9（EVT，陳述不證）＋ Theorem 4.10（Thm A＋證）＋ Theorem 4.11（Rolle＋證）＋ Theorem 4.12（MVT＋證）＋ **Figure 4.2**（割線–切線）＋ Strategy 4.2（套 MVT）＋ Corollary 4.3（monotonicity，雙條）＋ Example 4.2（sin、`e^x`）＋ 收尾（交棒 §4.5）。**明顯超出 6 頁 → 回查是否堆了過多 caution／重複散文**（本節風險＝證明階梯不紮實 vs caution 灌水兩端，非缺料）。ch04 數學含多行 aligned 單邊極限、分式割線 → ④ 後查 print overflow（PLAN §6；多行 `aligned` 易裂頁）。

---

## A. 編號 ledger 提案（§4.4；接 §4.3 ledger，自 Definition 4.3／Theorem 4.9 起；④ 落定後回填 PLAN §5）

> §4.1–§4.3 已 mint：Definition 4.1–4.2、Theorem 4.1–4.8、Proposition 4.1–4.2、Corollary 4.1–4.2、Strategy 4.1、Example 4.1、Figure 4.1、Remark 4.1–4.3。各型獨立 counter、跨節連續。Caution 無編號。

| 型別 | §4.4 提案 | 說明 |
|---|---|---|
| **Definition** | `4.3`＝maximum / minimum point（含對偶 min） | 手稿 Def 1；本節第一個具名 Definition |
| **Theorem** | `4.9`＝Extreme Value Theorem（陳述不證） | 手稿「Fact」具名；cross-ref 完備性（Theorem 4.1） |
| | `4.10`＝Interior Extremum（手稿「Theorem A」）＋證 | env-name 提案「Interior Extremum (Theorem A)」保留手稿名（§C-8） |
| | `4.11`＝Rolle's Theorem＋證 | Case 1/2；§C-1 修 (ii) 筆誤 |
| | `4.12`＝Mean Value Theorem＋證 | 輔助 `g`；§C-4 圖 |
| **Corollary** | `4.3`＝Monotonicity from `f'`（雙條：`≥0⟹`non-decreasing、`>0⟹`strictly increasing） | §C-2 補 strict 版（legacy 雙條） |
| **Strategy** | `4.2`＝Applying the MVT（驗 hypotheses；`|x|` on `[−1,1]` 反例） | §C-5（ROADMAP 指派） |
| **Figure** | `4.2`＝MVT secant–tangent（割線 dashed、`c` 平行 tangent solid） | §C-4（ROADMAP key figure） |
| **Example** | `4.2`＝(i) `sin` on `[0,π/4]`＋(ii) `e^x` on ℝ（單一 Example 區塊兩項，忠實手稿） | §C-9（可選拆成 4.2/4.3；建議合一） |
| **Remark** | （選配）`4.4`＝conceptual（Rolle＝MVT 平均斜率為 0 的特例／MVT 是中央 existence 引擎） | §C-10（可選；或併入 opener 散文） |
| **Caution** | 無編號＝(a) Thm A interior 必要；(b) MVT closed/open 不對稱（與 Strategy 4.2 互補，擇一主述）；(c) 「every `[a,b]`⟹ℝ」延拓 | §C-6（取必要者，勿灌水） |
| **Proposition** | **§4.4 不 mint 新 Proposition**（EVT/Thm A/Rolle/MVT 皆 Theorem） | Proposition `4.3` 留給 §4.5（如需） |

> **編號自查（④）**：寫完逐一確認每個「by Theorem 4.1（完備性）／Theorem 4.8（`(e^x)'`）／Theorem 4.7（指數律）／Thm A／Rolle／MVT／Corollary 4.3」都對得到一個存在的 `env-num`；跨節引用（EVT→完備性 Theorem 4.1、`e^x` example→Theorem 4.8、`e^x>0`→Theorem 4.7）尤其查。Figure 4.2 為 ch04 第二張圖（接 Figure 4.1）。

## B. 章基礎建設
**N/A** —— §4.4 非首節。chapter standalone／`fragments/ch04/` 骨架／figures.js／`build.py` ch04 entry 皆 §4.1 已建、§4.2–§4.3 已沿用。§4.4 落地＝新增 `fragments/ch04/sec-4-4.html`、`build.py` 的 `CHAPTERS["ch04"].fragments` append `"sec-4-4"`、`chapter4-print-standalone.html` 嵌入式 `fragments:[…]` 同步 append（PLAN §6／§4.2–§4.3 整合實證：build.py 與 standalone 內嵌清單**須手動雙同步**）、續用手動編號 ledger。**動手前先讀 `sec-4-3.html` 末尾**確認各型 counter 收在哪（接續機制，PLAN §5：Theorem 收 4.8、Definition 4.2、Corollary 4.2、Proposition 4.2、Strategy 4.1、Example 4.1、Figure 4.1、Remark 4.3）。**Figure 4.2** 須照 ch04 figure 慣例（figures.js append 不覆蓋、SVG/inline、label economy；MVT 圖含曲線＋割線 dashed＋內部 `c` 平行 tangent solid＋`a`/`b`/`c` 標記）。

## C. 待核對／存疑（③ 一併裁示）
1. **【建議修】Rolle Case 2 (ii) 的筆誤**（seed §C-1 [請查核]）：手稿 p.14 (ii) 寫「`f(X_M)<f(a)`」，下標應為 `X_m`（p.15 解 (ii) 用 `X_m`、legacy line 612 亦作 `f(x_m)<f(a)`）。**提案：④ 照正確版寫 `f(X_m)<f(a)`**（min 在端點值之下 ⟹ min 內部）。③ 確認（建議修）。
2. **【建議補】Corollary 4.3 的 strict 版**（seed §C-2 [請查核]）：手稿 Corollary 只給 `f'≥0⟹f(x_2)≥f(x_1)`（非嚴格），但 Example 下嚴格、且 §4.5 需 `e^x` **strictly** increasing（單射）。**提案：Corollary 4.3 寫雙條**——`f'(c)≥0 ∀c ⟹ f` non-decreasing（`f(x_1)≤f(x_2)`）；`f'(c)>0 ∀c ⟹ f` strictly increasing（`f(x_1)<f(x_2)`）（legacy line 705–710 即雙條，證即同一 MVT 商式分非嚴格/嚴格兩判）。③ 確認（建議補；否則 Example 的 strict 結論懸空）。
3. **【建議】EVT（Theorem 4.9）的呈現**：具名「Extreme Value Theorem」、**陳述不證**（手稿明言）、cross-ref 完備性（Theorem 4.1）、一句「為何不證（完備性論證冗長、當 black box）」＋**一句「closed 區間＋continuous 兩條件皆必要」**（legacy remark 有 `f(x)=x` on `(0,1)` 無 max、不連續函數可失 max 的反例——提案至多一句帶過，不全展開兩反例以免膨脹）。③ 確認呈現深度（建議：具名＋不證＋cross-ref＋一句必要性）。
4. **【建議收】Figure 4.2（MVT secant–tangent）**：ROADMAP §4.4 key figure。割線過 `(a,f(a))`、`(b,f(b))`（dashed），內部 `c` 處 tangent（solid）平行割線；標 `a`、`b`、`c`。**提案：收**（ROADMAP 指派、MVT 的承重幾何直覺）＋ MVT 陳述後一句散文點明「圖示：某內部切線平行割線」。③ 確認（建議收，ROADMAP mandate）。
5. **【建議收】Strategy 4.2（Applying the MVT）**：ROADMAP §4.4 指派。三步——(1) 驗 `[a,b]` 連續（含端點）、(2) 驗 `(a,b)` 可微（端點不算）、(3) 結論只給存在性、不給特定 `c`。**反例**：`|x|` on `[−1,1]` 連續但 `0` 不可微，割線斜率 `0` 卻無 `c` 使 `|x|'(c)=0`（導數恆 `±1`）——示範 hypothesis-fail。③ 確認（建議收，ROADMAP mandate）。
6. **【建議取必要者】Caution 清單**（無編號）：
   - **(a) Thm A 的「interior」必要**：端點極值不必 `f'=0`（`f(x)=x` on `[0,1]` 端點取極值、`f'=1≠0`）。**建議收**（Thm A 的關鍵邊界、低成本）。
   - **(b) MVT 的 closed/open 不對稱**：與 Strategy 4.2 重疊——**建議併入 Strategy 4.2**（不另開 caution，避免重複）。
   - **(c)「every `[a,b]` ⟹ on ℝ」延拓**：`e^x` 由任意閉區間嚴格增推 ℝ 上嚴格增——**建議一句 note 附在 Example 4.2(ii)**（legacy 有對應 caution；不另開框）。
   ③ 裁示收哪些（建議：(a) 收為 caution；(b) 併 Strategy；(c) 一句 note）。
7. **【建議補一行】`e^x>0 ∀x` 的依據**（Example 4.2(ii)）：`x≥0` 級數逐項正、`x<0` 由指數律 `e^x=1/e^{−x}>0`（Theorem 4.7）。**提案：補一行**（否則 `(e^x)'=e^x>0` 的 `>0` 懸空）。③ 確認（建議補）。
8. **【取捨】「Theorem A」命名**：手稿命名 interior-extremum 結果為「Thm A」（無通名）。**提案：env-name「Interior Extremum (Theorem A)」**（保留手稿名為副、補通用描述名）。③ 取捨（建議保留手稿名為副名）。
9. **【取捨】Example 結構**：手稿單一「Example」含 (i)(ii)。**提案：合為 Example 4.2（兩項 (i) sin、(ii) `e^x`）**，忠實手稿；`e^x` 項為交棒 §4.5 的承重點。③ 可選拆成 Example 4.2/4.3（建議合一）。
10. **【選配】Remark 4.4**：一句 conceptual——「Rolle 是 MVT 平均斜率為 0 的特例；MVT 是微分學中央 existence 引擎，後續單調性／Taylor 皆經它」。**提案：可收為 Remark 4.4，或併入 opener／MVT 後散文**（不另立框）。③ 取捨（建議：併入散文、不另開 Remark，除非要顯式索引）。
11. **【方向】opener 措辭**：承 §4.3 closer 已 forward-fence「單調性需 `(e^x)'=e^x>0`、下節 Rolle/MVT」。**提案：opener 一段承接——本節暫離指數主線、建立 MVT 這座 existence 橋（逐點導數→整段行為），終點是 `f'≥0⟹遞增`、套到 `e^x` 收割嚴格單調、交棒 §4.5 的 `ln`**（legacy opener line 540–541 即此 framing）。③ 確認方向。

## D. 章層決策落地（§4.4 相關；提案＋理由，待 ③ 拍板）
- **D4 — MVT 留在 §4.4（不移走）。** 手稿把 Rolle/MVT 夾在指數章因 `ln` 建構需單調性 corollary；本章保留。未來 applications-of-differentiation 專章草擬時，再於 Mode B **僅提議**移走——**本節不動此決定、不自行移**。
- **D1 — legacy tex 當 signed 數學 cross-check。** §4.4 的 Thm A／Rolle／MVT／Corollary 一律以 legacy §4.4＋§4.5-開頭段盲算對賬（已對：證法逐字一致；Case 2 筆誤經 legacy 證實），不照抄散文／結構。
- **placement（PLAN §1/§2 已定）— Corollary＋兩 Example 收在 §4.4。** legacy 把 monotonicity corollary 放 §4.5 開頭；手稿頁序＋PLAN 放 §4.4（收在「`e^x` strictly increasing」）。§4.5 從此接手、**不重證**單調性。auditor 勿判「§4.4 收 Corollary＝越界／與 §4.5 重複」。

---

### 結構草圖（④ 照此寫；待 ③ 定案）
§4.4 opener（承 §4.3 closer 的 forward-fence：單調性需 `(e^x)'=e^x>0`；本節暫離指數主線、建 MVT 這座「逐點導數→整段行為」的 existence 橋，終點 `f'≥0⟹遞增`、套 `e^x` 收割嚴格單調、交棒 §4.5。〔§C-11〕）→ **Definition 4.3**（max/min point，含對偶 min）＋`cos x` 例（具體錨）→ **Theorem 4.9**（EVT，陳述不證；cross-ref 完備性 Theorem 4.1；一句必要性〔§C-3〕）→ **Theorem 4.10**（Interior Extremum「Theorem A」〔§C-8〕＋證：`f(X_M+h)−f(X_M)≤0` → `h>0`/`k<0` 雙單邊極限 → `f'=0`；〔§C-6a〕一句 interior-必要 caution）→ **Theorem 4.11**（Rolle＋證：EVT 取 `X_m,X_M`；Case 1 常數／Case 2 內部極值〔§C-1 修筆誤〕）→ **Theorem 4.12**（MVT＋證：輔助 `g`＝曲線減割線、`g(a)=g(b)=0` → Rolle → `f'(c)=`平均斜率）＋ **Figure 4.2**（割線–切線〔§C-4〕＋一句幾何散文）＋ **Strategy 4.2**（套 MVT 驗 hypotheses〔§C-5〕，含 `|x|` 反例＋〔§C-6b〕closed/open 不對稱併此）→ **Corollary 4.3**（monotonicity 雙條〔§C-2〕＋證套 MVT 於 `[x_1,x_2]`）→ **Example 4.2**（(i) sin on `[0,π/4]`；(ii) `e^x` on ℝ〔§C-7 補 `e^x>0`、§C-9 合一、§C-6c 一句 every-`[a,b]`⟹ℝ〕→ **`e^x` strictly increasing on ℝ**）→ 收尾（〔§C-10 選配 Remark 4.4 或散文〕conceptual 一句；交棒 §4.5：`e^x` 嚴格遞增 ⟹ 單射 ⟹ 下節定義 `ln x`）。

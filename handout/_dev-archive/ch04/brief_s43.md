# Direction Brief — §4.3 The Derivative of e^x

> ② 方向提案（CONTENT_DIRECTION §2 九欄）。**狀態：待 ③ 方向閘核可**（③ 拍板後本 brief 成 ④/⑤ 契約）。
> 輸入：[`seed_ch04_s3.md`](seed_ch04_s3.md)（手稿 pp.10–11）＋ [`PLAN-ch04.md`](PLAN-ch04.md) 章層決策（§4.3 redundancy open Q、編號 ledger）＋ ROADMAP「Chapter 4」條目（core skill「rigorous derivative with explicit bound」、§4.3 redundancy open question）。
> §4.3 **非首節、且為全章最短節**（手稿 ~1 頁純推導）：不建章基礎建設；沿用 §4.1–§4.2 已建的 chapter standalone／fragments／figures.js，續編號（自 Theorem 4.8、Proposition 4.2 起）。
> ①-verify：使用者選「現在開跑 §4.3」即視為 seed accepted-by-proceeding（pending §C 的 [請查核] 更正）。數學 cross-check：legacy `ch04_exponential_logarithm.tex` 的 §4.3 段（`sec:rigorous-derivative-of-exp`）。

---

## 手稿盤點（照原順序）
- **§ The derivative of the exponential function**（標題即手稿原文）。
- **difference quotient**：`(e^{x+h}−e^x)/h = ((e^h−1)/h) e^x`（手稿直接寫出；中間步 `e^{x+h}=e^x e^h`（§4.2 指數律）⟹ `e^{x+h}−e^x=e^x(e^h−1)` 未顯式寫）。
- **化約**：「To find `d/dx e^x`, we only need to find the limit `lim_{h→0}(e^h−1)/h`」（`e^x` 與 h 無關，提出）。
- **Note（bound 推導）**：`e^h=1+h+h²/2!+⋯`（§4.1 級數代 x=h）⟹ `(e^h−1)/h−1 = h/2+h²/3!+⋯+h^{n−1}/n!+⋯` ⟹ `|(e^h−1)/h−1| ≤ |h|[1/2+|h|/3!+⋯+|h|^{n−2}/n!+⋯] ≤ |h|` for `h∈(−1/2,1/2)`。
- **結論**：`lim_{h→0}((e^h−1)/h−1)=0` ⟹ **`d/dx e^x=e^x`**。
- 具名人物／史實：**無**。worked example：**無**。圖：**無**。caution／strategy：**無**。higher-derivative corollary：**無**（手稿止於 `d/dx e^x=e^x`）。

## 薄度剖析
| 區塊 | 狀態 |
|---|---|
| difference-quotient setup | **夠**（手稿直接給因式分解；補一句中間步 `e^{x+h}=e^x e^h` 即完整） |
| 化約到 `lim(e^h−1)/h` | **夠**（手稿一句點明 `e^x` 提出） |
| bound `|(e^h−1)/h−1|≤|h|` | **夠但有一處從略**：手稿給出級數逐項＋提 `|h|`，但**中括號 `[1/2+|h|/3!+⋯]≤1`（當 `|h|<1/2`）手稿只給結論未證**（見 §C-1）→ ④ 補一句尾界 |
| `lim(e^h−1)/h=1` ⟹ `d/dx e^x=e^x` | **夠**（bound ⟹ squeeze 至 1，直接得） |
| **Ch2 §2.4 redundancy 的處理** | **薄**：手稿不知 Ch2（手稿是獨立講義）；handout 須開頭 cross-ref Ch2 informal 版、點明「這次補 explicit bound」（legacy opener 即如此）→ §C-2／D1 |
| bound 的**意義**（為何要 explicit rate） | **薄**：手稿只給 bound、未說「這把 Ch2『高次項 vanish』量化成 explicit linear rate」→ 一句 Remark（legacy 有對應 remark） |
| higher derivatives | **無**：手稿止於一階；`(e^x)^{(n)}=e^x` 是 legacy 加的 Corollary（低風險、設定後續 Taylor）→ §C-3 |
| 「slope = height」直覺／application | **無**：手稿純推導；`(e^x)'=e^x` 的建模意義（`y'=ky⟹y=y₀e^{kt}`）legacy 置於章末 → §C-4（提案：本節只一句 forward-hook，全 treatment 留章末/§4.5） |

## 範圍與深度
- **吃手稿這一叢**：difference quotient → 化約到 `lim(e^h−1)/h` → bound `≤|h|` → `d/dx e^x=e^x`。**全章最短節，核心風險是過度展開**——務必保持精煉、不灌水。
- **保留證明**（手稿全給、標準、本節主軸）：difference-quotient 因式分解、`(e^h−1)/h−1` 的級數 bound、極限 ⟹ 導數。
- **小幅 expansion（低風險、提案）**：① 開頭 Ch2 cross-ref 一段（legacy 做法、PLAN §2 指定）；② 把 bound 升格具名 **Proposition 4.2**＋補 §C-1 的「中括號 ≤1」一句；③ **Remark 4.3**（bound＝Ch2 casual 論證的嚴格版、explicit linear rate）；④（選配）**Corollary 4.2**（higher derivatives，迭代一行）。
- **陳述／援引不重證**：§4.1 級數定義（`e^h=Σhⁿ/n!`，本節代用、不重述）；§4.2 指數律（Theorem 4.7，差分商因式分解的根據，**只援引**）；導數定義（Ch2 已給，本節用 difference-quotient → limit、不重述定義）。
- **forward-fence（一行帶過）**：monotonicity（`(e^x)'=e^x>0⟹e^x` strictly increasing）→ §4.4 corollary／§4.5；`ln x` 導數 → §4.5；`y'=ky` 建模全 treatment → 章末／§4.5。
- **不重做 Ch2**：Ch2 §2.4 的 informal 版**不改**（改 forward-ref 延後至兩章簽核後，PLAN §2）；本節只 cross-ref、不動 Ch2 檔。

## 承重直覺（一節一個，領頭）
**`e^x` 的導數還是 `e^x`，因為差分商一拆就分離成 `((e^h−1)/h)·e^x`——`e^x` 只是「搭便車」被提出去，整節的全部內容濃縮成一個極限 `lim_{h→0}(e^h−1)/h=1`；而級數讓這個極限變透明：`(e^h−1)/h = 1 +（高次項）`，高次項以 explicit 線性速率 `≤|h|` 消失。** §4.1 掙到 `e^x` 存在、§4.2 證它連續＋乘法相加；§4.3 收割：用指數律把 `e^{x+h}` 拆成 `e^x e^h`，導數計算就塌縮成「`(e^h−1)/h` 跑去 1 有多快」這一個問題，級數＋尾界（同 §4.1–§4.2 的 partial-sum/tail 引擎）給出 explicit bound。**這是 Ch2 那個 casual term-by-term 論證的嚴格補完——差別正在這個 explicit bound。**

## worked example 清單（提案，待 ③）
| # | 內容 | 取捨 |
|---|---|---|
| —— | §4.3 為**純推導節**，手稿無例題；推導本身（bound＋導數）即承重 beat。 | **提案：0 個 worked example。** §4.3 已是全章最短節、塞數值例會稀釋單一主線。③ 若要一個「具體感」錨，可考慮極小的「`d/dx e^x` 在 `x=0` 給 slope `=e^0=1`」一句對照——**低優先、預設不收**（且 `e^0=1` 屬 §4.1 刻意不寫範圍，需小心）。 |

## history / application
- **history**：**留白**（手稿無；導數公式無自然史實錨）。
- **application**：**提案一句 forward-hook，全 treatment 留章末／§4.5**。`(e^x)'=e^x`（slope=value）是「任何變化率正比於自身的量都由 `e^x` 建模（`y'=ky⟹y(t)=y₀e^{kt}`：人口、放射衰變、連續複利）」的根。legacy 把這段 application 置於**章末**（`ln` 之後）。**提案：§4.3 只在 Remark／收尾一句點到「slope=value 是 `e^x` 成為建模函數的根」並 forward 到章末**，不在本短節展開 ODE/half-life（避免過度膨脹最短節）。③ 確認收一句或全略。

## 強調 / takeaway
- **概念樞紐**：**導數計算靠指數律塌縮**——`e^{x+h}=e^x e^h` 把「在 x 處的導數」化約成「在 0 處的導數 `lim(e^h−1)/h`」一個普適常數（=1）。指數函數的「自我複製」性質（導數＝自身）正源於此乘法結構。
- **可攜技能**：(1) 差分商遇指數型，先用指數律分離出與 h 無關的因子；(2) **explicit bound > 定性 vanish**：把「高次項趨於 0」量化成 `≤|h|` 的 explicit rate，是後續誤差分析（Taylor remainder）的基礎。
- **依賴鏈 takeaway**：`§4.2 指數律 → 差分商分離 → §4.1 級數給 (e^h−1)/h 的 explicit bound → d/dx e^x = e^x`。三節環環相扣，§4.3 是收割。

## 刻意不寫（餵 auditor 作 direction-conformance 反向檢查）
| 不寫什麼 | 理由 | 它該去哪 |
|---|---|---|
| §4.2 指數律的**重證** | Theorem 4.7 已證；本節只援引（差分商因式分解的根據） | §4.2（本節 cross-ref） |
| §4.1 級數收斂／定義的**重述** | §4.1 已給；本節代 `e^h=Σhⁿ/n!` 直接用 | §4.1 |
| **chain rule／`d/dx e^{kx}`、`d/dx e^{g(x)}`** | 屬 Ch2/Ch3 chain rule；本節只做 base `d/dx e^x` | Ch2/Ch3（已有） |
| **`ln x` 的導數** | 需 `e^x` 反函數＋ monotonicity | §4.5 |
| **Rolle／MVT／monotonicity corollary** | 屬 §4.4 | §4.4 |
| **改寫 Ch2 §2.4**（informal 版改 forward-ref） | 延後至兩章簽核後；本章不動 Ch2 | 兩章簽核後的 Mode B |
| **`y'=ky` ODE／half-life 完整 treatment** | 最短節不宜膨脹；建模全 treatment 在章末 | 章末／§4.5（本節至多一句 hook） |
| 自創 bare your-turn exercise | README §防護欄禁、deferred | —（自創一律寫成含解 worked example） |
| **過度展開**（把短節灌成長節） | §4.3 是全章最短純推導節；單一主線＋一個 bound＋一個 Theorem 即足 | 保持精煉 |

## 篇幅帶（護欄非預算）
**2–3 A4 print 頁**（全章最短節）。§4.3 ≈ opener（承 §4.2＋Ch2 cross-ref）＋difference-quotient setup＋**Proposition 4.2**（bound＋證）＋**Remark 4.3**（explicit rate 的意義）＋**Theorem 4.8**（`d/dx e^x=e^x`＋證）＋（選配）**Corollary 4.2**（higher derivatives）＋收尾（forward §4.4 monotonicity）。**明顯超出 3 頁 → 回查是否過度展開**（本節最大風險＝灌水，非缺料）。ch04 數學含級數省略號／絕對值不等式 → ④ 後查 print overflow（PLAN §6）。

---

## A. 編號 ledger 提案（§4.3；接 §4.2 ledger，自 Theorem 4.8／Proposition 4.2 起；④ 落定後回填 PLAN §5）

> §4.1–§4.2 已 mint：Definition 4.1–4.2、Theorem 4.1–4.7、Proposition 4.1、Corollary 4.1、Strategy 4.1、Example 4.1、Figure 4.1、Remark 4.1–4.2。各型獨立 counter、跨節連續。Caution 無編號。

| 型別 | §4.3 提案 | 說明 |
|---|---|---|
| **Theorem** | `4.8`＝`d/dx e^x = e^x`（rigorous derivative） | 本節主結果 |
| **Proposition** | `4.2`＝`|(e^h−1)/h − 1| ≤ |h|` for `h∈(−1/2,1/2)`（bound） | 升格具名（承載 explicit rate；證在其下） |
| **Corollary** | （選配）`4.2`＝`(e^x)^{(n)} = e^x` ∀n（higher derivatives） | 手稿無；legacy 有；迭代一行。**見 §C-3** |
| **Remark** | `4.3`＝此 bound＝Ch2 casual 論證的嚴格版（explicit linear rate） | legacy 有對應 remark；承載「為何要 bound」 |
| **Strategy** | **援引 Strategy 4.1**（series/tail bound）；不新增 | bound 推導同 §4.1–§4.2 的尾界引擎；首次 reuse 處一句回指（選配，見 §C-5） |
| **Definition** | **§4.3 不 mint 新 Definition**（導數定義 Ch2 已給；本節用 difference-quotient→limit） | Definition `4.3` 留給 §4.4/§4.5（如 `ln x`） |
| **Example / Figure** | §4.3 **無**（無 ROADMAP key figure；純推導節） | — |

> **編號自查（④）**：寫完逐一確認每個「by Theorem 4.7（指數律）／Proposition 4.2／§4.1 級數／Strategy 4.1」都對得到一個存在的 `env-num`；跨 §4.2↔§4.3 引用（差分商用指數律 Theorem 4.7、bound 用 §4.1 級數）尤其查。

## B. 章基礎建設
**N/A** —— §4.3 非首節。chapter standalone／`fragments/ch04/` 骨架／figures.js／`build.py` ch04 entry 皆 §4.1 已建、§4.2 已沿用。§4.3 落地＝新增 `fragments/ch04/sec-4-3.html`、`build.py` 的 `CHAPTERS["ch04"].fragments` append `"sec-4-3"`、`chapter4-print-standalone.html` 嵌入式 `fragments:[…]` 同步 append（PLAN §6／§4.2 整合實證：build.py 與 standalone 內嵌清單**須手動雙同步**）、續用手動編號 ledger。**動手前先讀 `sec-4-2.html` 末尾**確認各型 counter 收在哪（接續機制，PLAN §5：Theorem 收在 4.7、Proposition 4.1、Corollary 4.1、Remark 4.2）。

## C. 待核對／存疑（③ 一併裁示）
1. **中括號 `[1/2+|h|/3!+⋯]≤1`（`|h|<1/2`）的細節**（seed [請查核]）：手稿只給結論。**提案：④ 補一句尾界**——`對 |h|<1/2，括號 = 1/2 + Σ_{n≥3}|h|^{n−2}/n! ≤ 1/2 + Σ_{n≥3}(1/2)^{n−2}/n! < 1`（首項 1/2＋階乘尾界 < 1/2）。cross-check legacy §4.3 對應 Proposition 的證法。③ 確認補（建議補，否則 bound 是斷言）。
2. **Ch2 cross-ref opener 的措辭**（D1）：手稿不提 Ch2；handout 開頭須 cross-ref Ch2 §2.4 informal `(e^x)'=e^x`、點明「當時 casual term-by-term、假設了收斂/連續/指數律，本節以 explicit bound 補完」。**提案：照 legacy opener 寫一段**（純文字 cross-ref，不動 Ch2 檔）。③ 確認措辭方向。
3. **higher-derivative Corollary 4.2 收否**：手稿無；legacy 有（`(e^x)^{(n)}=e^x`，迭代一行）。**價值**：設定後續 Taylor／高階導數、近乎零成本。**提案：收**（低風險、一行證）。③ 確認。
4. **application forward-hook 收否**：`(e^x)'=e^x`（slope=value）⟹ `y'=ky` 建模。**提案：本節只一句 forward-hook（點到「slope=value 是 `e^x` 成為建模函數的根」、forward 章末）**，全 ODE/half-life treatment 留章末／§4.5（避免膨脹最短節）。③ 確認收一句或全略。
5. **Strategy 4.1 回指收否**：bound 推導同 §4.1–§4.2 尾界引擎。**提案：在 bound 證的尾界步一句回指 Strategy 4.1**（或省略——§4.3 的 bound 是直接級數逐項，與 partial-sum tail 略異）。③ 取捨（建議輕量一句或略）。
6. **`(e^h−1)/h−1` 記號型態**：手稿用省略號通項 `h/2+⋯+h^{n−1}/n!+⋯`。**提案：④ 以乾淨 Σ 形 `(e^h−1)/h−1 = Σ_{n≥2} h^{n−1}/n!` 為主、省略號為輔 gloss**。③ 排版偏好（建議 Σ 形）。

## D. 章層決策落地（§4.3 相關；提案＋理由，待 ③ 拍板）
- **D-redundancy（§4.3 open Q）— Ch2 §2.4 cross-ref、不動 Ch2。** §4.3 開頭 cross-ref Ch2 informal `(e^x)'=e^x`、點明本節補 explicit bound（legacy opener 做法）。**重構（Ch2 改 forward-ref）延後至兩章簽核後**——本章**不動 Ch2 檔**（PLAN §2、§C-2）。
- **D1 — legacy tex 當 signed 數學 cross-check。** §4.3 的 bound、導數、higher-derivative corollary 一律以 legacy §4.3 段盲算對賬，不照抄散文／結構。
- **D9 — 記號沿用。** `e^h` 級數沿用 §4.1 `Σhⁿ/n!`；差分商變數 `h`；無新記號。

---

### 結構草圖（④ 照此寫；待 ③ 定案）
§4.3 開場（承 §4.2：`e^x` 在 ℝ 上已定義、連續、滿足指數律；本節收割導數。**Ch2 cross-ref**：Ch2 §2.4 曾 casual 算過 `(e^x)'=e^x`、假設了收斂/連續/指數律，本節以 explicit bound 補完——不動 Ch2）→ **difference-quotient setup**：`(e^{x+h}−e^x)/h = ((e^h−1)/h)e^x`（用 §4.2 指數律 `e^{x+h}=e^x e^h` 因式分解；`e^x` 與 h 無關提出 → 化約到 `lim(e^h−1)/h`）→ **Proposition 4.2**（bound `|(e^h−1)/h−1|≤|h|`，`h∈(−1/2,1/2)`；證：`e^h` 級數逐項 → `(e^h−1)/h−1=Σ_{n≥2}h^{n−1}/n!` → 提 `|h|`＋中括號 ≤1 尾界〔§C-1〕；〔§C-5 選配〕一句回指 Strategy 4.1）→ **Remark 4.3**（此 bound＝Ch2 casual 論證的嚴格版：把「高次項 vanish」量化成 explicit linear rate `≤|h|`）→ **Theorem 4.8**（`d/dx e^x=e^x`；證：bound ⟹ `lim(e^h−1)/h=1` ⟹ 差分商 → `1·e^x`）→〔§C-3 選配〕**Corollary 4.2**（`(e^x)^{(n)}=e^x` ∀n，迭代）→ 收尾（〔§C-4 選配〕slope=value 一句 forward-hook；forward §4.4：monotonicity 需 `(e^x)'=e^x>0`，下節 Rolle/MVT）。

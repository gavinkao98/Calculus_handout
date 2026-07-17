# Direction Brief — §4.1 Construction of the Exponential Function

> ② 方向提案（CONTENT_DIRECTION §2 九欄）。**狀態：待 ③ 方向閘核可**（③ 拍板後本 brief 成 ④/⑤ 契約）。
> 輸入：[`seed_ch04_s1.md`](seed_ch04_s1.md)（手稿 pp.1–3）＋ [`PLAN-ch04.md`](PLAN-ch04.md) 章層決策 D1/D5/D6/D9 ＋ ROADMAP「Chapter 4」條目。
> §4.1 是 ch04 **首節**：另負責建章基礎建設（見 §B）。
> ①-verify：使用者選「§4.1 先跑到底」即視為 seed 接受（pending 任何更正）。數學 cross-check：legacy §4.1 (L17–166)。

---

## 手稿盤點（照原順序）
- 有理數指數建立：`aⁿ`（n copies）、`a^(1/n)`＝`xⁿ−a=0` 的正根、`a^q=(a^(1/m))ⁿ`（`q=n/m`）
- 有理指數律：`a^(n₁)·a^(n₂)=a^(n₁+n₂)`、`(a^(n₁))^(n₂)=a^(n₁·n₂)`
- **Q: `a^r` for `r∉ℚ`?**（提問、**未作答**——直接跳到 series 定義）
- **Def** `e^x = Σ_{n≥0} xⁿ/n!`（**只對 x>0**）；`0!:=1`
- **Property**（completeness）：(1) 遞增有上界 → lim 存在；(2) 遞減有下界 → lim 存在（**陳述、不證**）
- **[e1]** `e^x<+∞ ∀x>0`：固定 x>0、取 `n₀>2x`、拆 `(I)+(II)`、`(II)≤x^(n₀)/n₀!` → `e^x ≤ Σ_{0}^{n₀} xⁿ/n! + x^(n₀)/n₀! < ∞`
- 部分和尾界：`0<x<L, k>n₀>2L` 時 `0 ≤ e^x − P_k(x) ≤ L^k/k! ≤ (L^(n₀)/n₀!)(1/2)^(k−n₀)`
- 具名人物／史實：**無**。worked example：**無**。圖：**無**。

## 薄度剖析
| 區塊 | 狀態 |
|---|---|
| 有理指數 → series 的**動機過渡** | **薄**（手稿一句「Q: a^r?」就跳到 series，未說「為何不用 rational-limit 建構、為何改以 series 定義」） |
| series 定義本身 | **夠**（清楚、含 `0!:=1`） |
| completeness 陳述 | **夠**；但**無「為何需要它」的直覺**（ℝ vs ℚ）→ 薄 |
| 收斂(x>0) 證明 | **夠**（手稿全證、標準、geometric-tail，屬本節主軸） |
| `e` 的數值／具體感 | **無**（手稿不算 `e`、無數值錨、無部分和） |
| partial-sum 收斂圖 | **無**（ROADMAP §4.1 key figure 指定） |
| 「series 是**定義**、不是性質」的觀念警示 | **無**（學生在 Ch2 非正式用過 `e^x`，易把其性質當已知）→ caution |
| geometric-tail 手法**命名**（§4.2 反覆重用） | **無** → strategy box |
| 用定義做**具體計算**的 worked example | **無** |

## 範圍與深度
- **吃手稿這一叢**：有理指數建立 → 以 power series **定義** `e^x`（x>0）→ completeness（陳述）→ 收斂(x>0)＋部分和尾界。
- **保留證明**（短、標準、具啟發、本節主軸）：收斂(x>0) 的 geometric-tail 證。深度＝手稿的**直覺-嚴謹層**（geometric 比較＋完備性，非從零建構實數）。
- **陳述不證**：completeness（手稿不證；其證屬實分析地基、超出本書範圍——legacy 也只陳述為 Theorem）。
- **forward-fence（一行帶過、不 preview-creep）**：`x<0` 延拓 → §4.2（絕對收斂）；continuity／exponent law → §4.2；二項式／`Cⁿ_k` → §4.2；`a^x=e^(x ln a)`、無理指數的真正建構 → §4.5；嚴格 `(e^x)'=e^x` → §4.3。
- **首節基礎建設**（見 §B）：章 opener、chapter4 standalone／fragments、figures 起手。

## 承重直覺（一節一個，領頭）
**series 是「定義」，存在性必須掙來。** 學生在 Ch2 非正式見過 `e^x`、用過它的性質；本章把那條 series 從「推導出的結果」翻轉成**出發點的定義**——於是「這個無窮多正項的和到底等不等於一個**有限**實數？」變成第一個非問不可的問題。承重動作＝**用一條幾何級數把無窮的尾巴關進一個有限上界**（`x/(n₀+1)·…·x/n ≤ (1/2)^(n−n₀)`），部分和遂單調有界，完備性把極限交出來。整節圍繞「定義 → 它真的存在嗎 → geometric-tail＋完備性把存在性掙到手」組織。（對齊 ROADMAP pitfall「series defines, doesn't derive」。）

## worked example 清單（提案，待 ③）
| # | 內容 | 技巧 | 來源 |
|---|---|---|---|
| **Example 4.1** | 算 `e` 的前幾項部分和 `P_k(1)=Σ_{0}^{k}1/n!`（k=0…5）→ `e≈2.7183`，並指出收斂之快由尾界保證 | 直接代入＋觀察 | **expansion（D5；非手稿，低風險數值錨）** |
- 序：定義 → completeness → 收斂定理 → **Example 4.1**（把抽象收斂落到 `e` 的具體數值）→ Figure 4.1。
- 只提一個 worked example：§4.1 本質是奠基，手稿無例題；多塞會稀釋主軸（geometric-tail 證才是 beat）。**待 ③ 取捨是否收 Example 4.1**。
- **不**寫成 worked example 的：收斂定理走 Theorem＋proof（非 example）。

## history / application
- **history**：可在 Example 4.1 收尾或一句 remark 提 `e` 為 **irrational & transcendental（不證）**（手稿無、legacy 帶過）。若放，標 `[source: standard calculus-textbook historical note]`。**低優先、待 ③**。
- **application**：**留白**。§4.1 是奠基節，無自然真實應用錨；硬塞弱錨不如不放（應用在後續章節）。

## 強調 / takeaway
- **概念樞紐**：**完備性 ＋ geometric-tail bound** ＝ 收斂引擎——把級數尾巴用幾何級數關進有限上界，單調有界 ⟹ 極限存在。
- **可攜技能**：對正項級數做 geometric-tail 比較、援引完備性得收斂（§4.2 連續性／指數律證明反覆 reach for 這招）。

## 刻意不寫（餵 auditor 作 direction-conformance 反向檢查）
| 不寫什麼 | 理由 | 它該去哪 |
|---|---|---|
| `x<0`／`x≤0` 的收斂、`e^0=1` 系統處理 | 手稿本節只定義 x>0；x<0 需絕對收斂 | §4.2 |
| `e^x` 的 continuity | 手稿 [e2] 起＝§4.2 | §4.2 |
| exponent law `e^x e^y=e^{x+y}` | §4.2 | §4.2 |
| 二項式定理／`Cⁿ_k`／`\binom` | 指數律才需要 | §4.2 |
| `a^x=e^(x ln a)`、無理指數 `a^r` 的真正建構 | 需 `ln`（`e^x` 反函數） | §4.5（§4.1 只 forward-fence 一句） |
| 嚴格 `(e^x)'=e^x` | 需 `(e^h−1)/h` bound | §4.3 |
| **completeness 的證明** | 實數地基、超出本書範圍 | 陳述即可（手稿/legacy 皆不證） |
| Bolzano–Weierstrass／Cauchy 等價 | §4.2 機器 | §4.2 |
| 自創 bare your-turn exercise | README §防護欄禁、deferred | —（自創一律寫成含解 worked example） |

## 篇幅帶（護欄非預算）
**4–6 A4 print 頁**（含章 opener ≈0.5 頁）。§4.1 ＝ 1 Def＋1 Caution＋1 Theorem(completeness 陳述)＋1 Remark＋1 Strategy＋1 Theorem(收斂＋證)＋（選配）1 Example＋1 Figure。證明只一條（收斂），比 §3.1 略輕。明顯超出 → 回查是否 completeness 誤展成證明、或 forward 主題漏 fence。

---

## A. 編號 ledger 提案（§4.1；④ 落定後回填 PLAN §5）

| 型別 | §4.1 提案 | 說明 |
|---|---|---|
| **Definition** | `4.1`＝natural exponential function（power series, x>0） | 本節唯一定義 |
| **Theorem** | `4.1`＝Completeness（單調有界收斂；**陳述不證**）、`4.2`＝`Σ xⁿ/n!` converges for x>0（**含證**） | 手稿稱 completeness 為「Property」；本書升格具名 Theorem（legacy/ROADMAP 一致），首見處 cross-ref 手稿「Property」用語 |
| **Strategy** | `4.1`＝bounding a series by a geometric tail | D5 expansion；§4.2 重用 |
| **Example** | `4.1`＝partial sums of `e`（≈2.7183） | D5 expansion；③ 取捨 |
| **Figure** | `4.1`＝partial-sum 收斂圖（`P_k`, k=1…4 → 光滑 `e^x`） | D5 expansion；ROADMAP key figure |
| **Remark** | `4.1`＝completeness 區分 ℝ/ℚ（`3,3.1,3.14,…` 在 ℚ 無極限） | expansion；給 completeness 一個「為何需要」 |
| **Caution** | 無編號＝**series defines, doesn't derive** | ROADMAP pitfall；高價值觀念警示 |
| Proposition / Corollary | §4.1 無 | — |

> **⚠️ 跨節連動（PLAN §5）**：§4.1 mint 了 Theorem **4.1/4.2**、Definition 4.1 → **§4.2 POC（`sec-4-2.html`）現用的 Thm 4.1–4.5、Def 4.1 全部須往後 renumber**（§4.2 自 **Theorem 4.3** 起；Def 4.1 Cauchy → Def 4.2 等）。④ 落定 §4.1 編號後立即回填 PLAN §5，§4.2 併入時據此 renumber（D2）。

## B. 首節基礎建設（§4.1 session 建一次，後續節沿用；PLAN §4）
> ⚠️ **動手前先讀 [`../../build.py`](../../build.py) ＋一個既有章（ch03 的 `chapter3-print-standalone.html` 與 [`../../fragments/ch03/`](../../fragments/ch03/)）確認當前 standalone／fragments 組裝慣例**，勿照本節臆測。

1. **章 standalone**：比照 `chapter3-print-standalone.html` 建 `chapter4` standalone（由 `build.py` 從 `fragments/ch04/sec-4-*.html` 組裝）。runningHead／brand＝「Chapter 4 · The Exponential and Logarithmic Functions」。寫檔 UTF-8 無 BOM。math `macros` 區塊按需（`\binom` KaTeX 內建；三反三角本章用不到）。
2. **章 opener**（併入 `sec-4-1.html` 開頭，`chapter-head`＋`.lead`＋learning objectives）。**learning objectives 涵蓋全章**（對齊 ROADMAP ch04 core skills），草案待 ③ 核可：
   - state the power-series definition of `e^x` and bound the tail to prove convergence on ℝ;
   - prove `e^x` is continuous on ℝ and satisfies `e^x e^y = e^{x+y}`;〔§4.2〕
   - re-derive `d/dx e^x = e^x` rigorously via the bound `|(e^h−1)/h − 1| ≤ |h|`;〔§4.3〕
   - state and prove Rolle's theorem and the Mean Value Theorem;〔§4.4〕
   - use the MVT to show `f' ≥ 0` on an interval implies `f` is increasing;〔§4.4〕
   - define `ln x` as the inverse of `e^x`, prove its continuity, and derive `d/dx ln x = 1/x`.〔§4.5〕
   - lead 段：Ch2 非正式用過 `e^x`；本章從 power-series 定義開始，把當時視為理所當然的 convergence／continuity 一一證成定理。
3. **figures**：Figure 4.1 partial-sum 收斂——`buildPlot` 畫 `e^x` 與 `P_k`(k=1…4)；label economy（圖內只留 `e^x`、`P_k` 最小標註，數值/說明進 caption）。比照 ch03 figures.js 慣例 append。

## C. 待核對／存疑（③ 一併裁示）
1. **①-verify**：使用者選「先跑到底」＝接受 seed；若對掃描比對發現轉錄誤差（尤其 p.3 尾界 `L^k/k!` 那條），請指出、④ 修正。注：`L^k/k!` 為手稿原貌（與已 ①-verified 的 `seed_s42.md` §4.1 依賴段一致）；④ 呈現時以**乾淨界** `(L^(n₀)/n₀!)(1/2)^(k−n₀)` 為主、中間步忠實附註。
2. **completeness 名目**：手稿稱「Property」、不證。提案升格 **Theorem 4.1（Completeness）陳述不證**＋首見 cross-ref 手稿用語。③ 確認。
3. **`a^r`(r∉ℚ) 讀法**：手稿 p.1 提問「無理數指數」（legacy 證實為 irrational）。§4.1 **不建構**、一句 forward-fence 到 §4.5（D6）。③ 確認。

## D. 章層決策落地（§4.1 相關；提案＋理由，待 ③ 拍板）
- **D5 — 收 `e` 數值＋部分和（Example 4.1）＋ partial-sum 圖（Figure 4.1）。** 手稿無；ROADMAP key figure 指定收斂圖。低風險 `expansion:example`/`figure`，給抽象收斂一個數值/視覺錨。**提案：收**（③ 可單獨否決 Example 或 Figure）。
- **D6 — `a^r`(無理指數) 一句 forward-fence 到 §4.5。** 照 legacy 框架（「rational-limit 較笨重 → 改走 series；一般 `a^x=e^(x ln a)` 留到 §4.5」），§4.1 不真的建構 `a^r`。**提案：一句帶過。**
- **D9 — `P_k` 部分和記號保留（手稿記號）；`e`（常數）／`e^x`（函數）在 §4.1 首見加 index entry。**
- **Caution（series defines, doesn't derive）＋ Strategy 4.1（geometric tail）＋ Remark 4.1（ℝ vs ℚ）** 為 expansion，承載承重直覺與手法命名。**提案：收**（③ 取捨）。

---

### 結構草圖（④ 照此寫；待 ③ 定案）
章 opener（全章 learning objectives）→ 開場直覺（Ch2 非正式用過 `e^x`；本章把 series 翻成**定義**、性質變待證）→ 有理指數回顧（`aⁿ → a^(1/m) → a^q` ＋有理指數律）→ `a^r`(r∉ℚ) 提問＋forward-fence（→§4.5）→ **Def 4.1** `e^x` series（x>0）＋ **Caution** series defines not derives → **Thm 4.1** Completeness（陳述）＋ **Remark 4.1** ℝ vs ℚ → **Strategy 4.1** geometric tail → **Thm 4.2** 收斂(x>0)（證：`n₀>2x`、拆 (I)(II)、尾界）＋部分和尾界（一句標明「§4.2 反覆援用」）→ **Example 4.1** partial sums of `e`（≈2.7183）→ **Figure 4.1** 部分和收斂 → forward-ref §4.2（x<0、continuity、exponent law）。

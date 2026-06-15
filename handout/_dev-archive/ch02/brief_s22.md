# Direction Brief — §2.2 The Derivative as a Function

> 待 ③ direction gate 核可。輸入：`seed_ch02_s2.md`（手稿 pp. 4–5）＋ §2.1 成品（`sec-2-1.html`，校準基準）＋ `CONTENT_ROADMAP.md` Ch2 條目。
> **ROADMAP 對齊（引用、不複述）：** core skill「state the limit definition … apply … polynomial and root functions」；key figure「derivative as a function: f above / f′ below, aligned x-axis」；strategy box「computing a derivative from the limit definition (3-step)」；notation「`f'(x), dy/dx, df/dx, d/dx[f(x)]`」。

---

## 手稿盤點
（照原順序）
- 「導數於一點」一般定義 `f'(a) = lim_{h→0} (f(a+h)−f(a))/h`，附等價式 `lim_{x→a} (f(x)−f(a))/(x−a)`
- Worked example（多項式）：`f(x)=x²+4x−2`，求在 `a` 的導數 → `2a+4`
- 「導函數」`f'(x) = lim_{h→0} (f(x+h)−f(x))/h`，明說 `f'(x)` 本身是 `x` 的函數
- Worked example（根式，rationalise）：`f(x)=√x, x>0` → `f'(x)=1/(2√x)`
- **無**：圖、exercise、Leibniz/operator 記號（純 prime）、應用、strategy box
- 具名結果／歷史：無

## 薄度剖析
| 區塊 | 狀態 | 指向 |
|---|---|---|
| `f'(a)` 一般定義（變化率） | **夠（但與 §2.1 重疊）** | 不重證；散文 recall §2.1 並 reframe 為「瞬時變化率」，一段帶過 |
| 「為何要 `f'(x)` 函數」的動機 | **無** | 補承重直覺：逐點重算 vs 留符號算一次 |
| `f'(x)` 作為函數（定義＋圖像關係） | **薄** | 補 Definition 2.2 ＋ f/f′ 堆疊圖 |
| f ↔ f′ 圖像關係＋圖 | **無** | 新增 Figure 2.2（f 上、f′ 下、x 軸對齊；ROADMAP key figure）|
| worked examples | **薄**（2 例、0 exercise）| 保留兩例；新增 graphical worked example；rational `1/x` 選配（未納入）。**不自創 exercise**（見「刻意不寫」）|
| 記號 `dy/dx`、`d/dx[·]` | **無** | 新增記號小節（ROADMAP；§2.4–§2.5 seed 已在用 `d/dx`，卻無處引入）— flag |
| strategy（3 步定義法） | **無** | 新增 strategy box（ROADMAP 指派本節）|
| 應用／rate of change | **無** | 開場 velocity 錨（expansion:application）— flag |
| `f'` 的定義域 | **無** | 一句（√x → f′ 僅 x>0；f′ 定義域可比 f 小）|

## 範圍與深度
- 吃 seed 這叢：一點導數一般定義（recall）→ 導函數 `f'(x)` → 由定義求 `f'`（多項式／根式／有理）→ 使用 f′（解 `f'=k`）→ 由 f 圖讀 f′ → 記號。
- 嚴謹度：§2.2 **無定理可證**；「證明」即 worked example 的極限計算。兩種極限式（`h→0` 與 `x→a`）等價已在 §2.1 示，recall 不重證。
- forward-fence（各一行）：微分法則（power/sum/product/quotient/`e^x`）→ §2.4–§2.5「先用定義，捷徑稍後」；不可微／f′ 何時不存在（`|x|` corner）→ §2.3；高階導數 `f''`、`f^(n)` → §2.3。
- **嚴守**：§2.2 一律 first principles，不得用任何尚未證的法則算導數。

## 承重直覺
**一個承重直覺領頭：「一次計算，無窮多斜率。」**
- 失敗例先打臉：§2.1 只能逐點求斜率，每點都要重跑極限——「算 `f'(2)`，再算 `f'(3)`，再算 `f'(3.5)`… 永遠算不完」，而且逐點算只給孤立數字、看不出**規律**。
- 關鍵動作：把點留成符號 `x`，極限只跑**一次**，輸出是一條公式＝一個**新函數** `f'`，同時給出每一點的斜率（也揭露規律）。
- 為它服務的次要心像：`f'` 是有自己圖形／定義域的真函數（Figure 2.2 把回報視覺化）。
- Ex 2.6 把此動作具體化：在一般 `a` 算得 `2a+4` → 因 `a` 任意，replace `a→x` → `f'(x)=2x+4`。

## worked example 清單
| # | 函數 | 技巧 | 來源 |
|---|---|---|---|
| Ex 2.6 | `f(x)=x²+4x−2` | 多項式（展開）→ `f'(x)=2x+4` | 手稿 |
| Ex 2.7 | `f(x)=√x` (x>0) | 根式共軛 → `1/(2√x)`；f′ 定義域 x>0；連 §2.1 Remark 2.2 的 `f'(4)=1/4` | 手稿 |
| Ex 2.8 | `f(x)=1/x` → `−1/x²` | 有理（通分）；補齊 poly/root/rational 三型；伏筆 §2.4/§2.5 | expansion:example（新增，批准 2026-06-07）|
| Ex 2.9 | `f(x)=x²+4x−2`：求切線斜率=2 之點 → `(−1,−5)` | **使用** f′（解 `f'(x)=k`，非計算 f′）——不同題型 | expansion:example（新增，批准 2026-06-07）|
| Ex 2.10 | 由 Figure 2.2 的 f 圖判讀 f′ 正負／零 | 圖像判讀（ROADMAP core skill）| expansion:example（新增）|

> 編號：§2.1 新增 Example 2.4／2.5（數值、近似）後，§2.2 例題序整體 **+2**（poly 由 2.4 變 2.6，… graphical 由 2.6 變 2.10）。

> **題目政策（使用者 2026-06-07 修定）：** 不寫 bare your-turn（無解練習題）——習題設計仍 deferred（README §防護欄、`CONTENT_SPEC.md` §14）。**但**可**自創新題、經使用者批准**後，當成 **worked example**（含完整 solution＋講解）寫入；硬條件：**題型須與既有 example 不同**（非改數字／係數）。

序：computation（poly → root）建立 routine → graphical（讀 f′）強化「f′ 是函數」→ 選配 rational 補型。同型不重講已建立的 setup。

## history / application
- **開場錨**（expansion:application）：rate of change / velocity——「若知道每一刻的位置 `s(t)`，每一刻的速度 `v(t)=s'(t)` 本身是一個函數」。這是「導數即函數」最忠實的真實實例（速度＝位置的導數，bedrock，非杜撰）。**保持概念性框架，不展成數值題**（數值應用屬後續「微分應用」章）。— flag 待核。
- **歷史**：無自然可考人物史觸發 → 留白。Leibniz `dy/dx` 的記號由來可在記號小節一句帶過（標 `[source: standard calculus-textbook historical note]`），不展開。

## 強調 / takeaway
- **概念樞紐**：導數是一個**函數**——把極限以符號點跑一次製造出來；`f'` 有自己的圖、定義域與行為。
- **可攜技能**：3 步 first-principles（寫差商 → 化簡消 `h` → 取 `h→0`），輸出**`x` 的公式**；外加由 f 圖之斜率正負／零讀出 f′。

## 刻意不寫
| 不寫 | 理由 | 去哪 |
|---|---|---|
| 微分法則（power/const/sum/product/quotient/`e^x`）| §2.2 嚴守定義法；法則未證 | §2.4–§2.5 |
| 一般指數冪法則（負／分數冪）| 未證 | §2.4＋後章 |
| 不可微／f′ 不存在（`|x|` corner）| 屬可微性 | §2.3 |
| differentiable ⇒ continuous | 屬可微性定理 | §2.3 |
| 高階導數 `f''`、`f^(n)` 與其記號 | 手稿置於 §2.3 | §2.3 |
| `Δx ≡ h` 的正式 caution | `Δx` 在 §2.5 才出現；§2.2 僅一句提「增量也寫 `Δx`」 | §2.5 caution（ROADMAP pitfall）|
| ε-δ 嚴格極限 | 超出本節 | Ch1／附錄 |
| 切線幾何當主敘事 | §2.1 已建立；§2.2 僅 recall | §2.1 |
| **bare your-turn exercise（無 solution 的練習題）** | README §防護欄「自創習題」deferred 到習題設計回合——§2.2 不放無解練習題。（自創新題若經批准，一律當 worked example 寫，含 solution；見上方「題目政策」） | 習題設計回合 |

> 餵 auditor：以上即 direction-conformance 的反向檢查——寫進任一項＝違反方向（多寫）；漏掉承重直覺／指定例子／strategy／圖＝違反方向（漏寫）。

## 篇幅帶
- 軟帶 **5–6 print 頁**（加入 2 個經批准的新型 worked example 後）。含 1 Definition、1 strategy box、1 figure、**5 worked example**（2.4–2.8）、記號小節、velocity 錨。bare your-turn exercise 無（自創題一律當 worked example）。
- 明顯超出 → 回查：rate-of-change 是否展成數值題、或誤入法則／可微性（皆應 fence）。

---

### Numbering 銜接（承 §2.1，手動；已回填為實際成品）
Definition **2.2**（the derivative as a function）；Strategy box **2.1**（本章首個，3 步定義法）；Figure **2.2**（f／f′ 堆疊，單圖；未用選配第二圖）；**Notation 為 `subsec-head` 小節**（非 remark）；Remark **2.3**（f′ 的定義域）、**2.4**（derivative as rate of change／velocity bookend）；Example **2.6**（多項式）、**2.7**（根式）、**2.8**（有理 `1/x`）、**2.9**（使用 f′）、**2.10**（圖像判讀）〔§2.1 新增 2.4/2.5 後整體 +2〕。**無 bare exercise**（自創題經批准後一律當 worked example，見上方「題目政策」）。

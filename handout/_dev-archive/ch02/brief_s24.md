# Direction Brief — §2.4 Derivatives of Polynomials and the Exponential Function

> 待 ③ direction gate 核可。輸入：`seed_ch02_s4.md`（手稿 pp. 8–10）＋ §2.1–§2.3 成品（校準基準）＋ `CONTENT_ROADMAP.md` Ch2 條目。
> **ROADMAP 對齊（引用、不複述）：** core skills「use the power, constant-multiple, sum … rules to differentiate algebraic and exponential combinations」「differentiate the natural exponential function `e^x` using its series definition」；prerequisite「the binomial theorem (used in the §2.4 power-rule proof)」；pitfall「Power rule domain：positive integer `n` 在 §2.4 證、negative-integer case 留 manuscript exercise、full real-exponent 版 deferred；a caution flags this」；pitfall「(fg)' ≠ f'g'（headline，屬 §2.5）」；Open question「Treatment of `e^x` derivative：series-based derivation 是 manuscript 的選擇、chapter 照走、flag for sign-off」（另 §4.3 會 rigorous 重推並 cross-ref 回本節）。

---

## 手稿盤點
（照原順序）
- 開場一句：本節學會微分這些函數（polynomial、exponential）
- **① Constant function**：`f(x)=c` → 由定義 `lim_{h→0}(c−c)/h = 0` → `f'(x)=0`
- **② Power function**：`f(x)=xⁿ`（`n` 正整數）→ **Formula** `d/dx(xⁿ)=n·x^(n−1)`；**Proof（因式分解法）** 用 `x→a` 式，`xⁿ−aⁿ=(x−a)(x^(n−1)+a·x^(n−2)+…+a^(n−1))` → 極限 `= n·a^(n−1)`
- **③ Alternative proof（二項展開法）**：用 `x+h` 式，`(x+h)ⁿ = xⁿ + C^n_1·h·x^(n−1) + …+ hⁿ`；除以 `h` 後除首項外皆帶 `h` → `h→0` 得 `n·x^(n−1)`
- **Exercise**：`d/dx(xⁿ)=n·x^(n−1)` 在 `n` 為負整數（`−1,−2,…`）時也成立
- **Sum / constant-multiple rules**（由定義直接得）：① `(f+g)'=f'+g'` ② `(c·f)'=c·f'`
- **Corollary（polynomial derivative）**：`f(x)=aₙxⁿ+…+a₀` → `f'(x)=aₙ·n·x^(n−1)+a_{n−1}·(n−1)·x^(n−2)+…+a₁`
- **Exponential**：Note `e^x` 先前已定義為級數 `e^x=1+x+x²/2!+…`；`f(x)=e^x` → `f'(x)=e^x·lim_{h→0}(e^h−1)/h`，因 `(e^h−1)/h=1+h/2!+h²/3!+…→1`，故 `f'(x)=e^x`；且 `f^(n)(x)=e^x`
- **Remark**：`f(x)=b^x`（`b>1`）→ chain rule（後）可得 `f'(x)=b^x·log_e b`
- **無**：worked example（全節零例題，只有規則＋證明＋一個 exercise）、圖、strategy box、歷史、應用、具名人物

## 薄度剖析
| 區塊 | 狀態 | 指向 |
|---|---|---|
| 「為何要規則」的動機 | **薄** | 手稿直接列規則；補 1 段承重直覺：§2.1–§2.3 每個導數都從定義硬算（慢、易錯），本節把規則「證一次、之後永遠當捷徑用」 |
| Constant rule | **夠** | 手稿有完整定義法導出；boxed 成 Theorem 2.2 |
| Power rule（正整數）＋兩證法 | **夠** | 手稿兩證法都完整、標準；**兩證並列保留**（手稿的教學選擇，硬約束）|
| 負整數冪 exercise | **薄/政策處理** | 見下「決策 B」與「刻意不寫」：不放 bare your-turn；以 ROADMAP-pitfall caution 處理 |
| Sum / constant-multiple rules | **夠** | 手稿有；合併為 Theorem 2.4（兩部分），證明用極限法則 |
| Polynomial corollary | **夠** | 手稿有；Corollary 2.1，逐項套用前述規則 |
| **worked example（套規則計算）** | **無** | 手稿零例題 → 教科書密度必補：至少 1 例多項式微分（套規則）、1 例 `e^x`＋多項式組合（見清單；須批准）|
| `e^x` 導數（級數論證） | **夠（直覺層級）** | 手稿照搬；rigor（收斂、逐項微分正當性）**不在本節**，一行 fence 到 Ch4 §4.3 |
| `b^x` remark | **夠** | Remark 2.6，預告 chain rule、不證 |
| 應用／歷史 | **無** | 無自然觸發（見 history/application 欄）；`e^x` 的成長應用、`e` 的嚴格構造皆 deferred |

## 範圍與深度
- 吃 seed 這叢：constant rule → power rule（正整數，兩證）→ sum / constant-multiple → polynomial corollary → 套規則的 worked example → `e^x` 導數（級數）→ `b^x` 預告。
- 嚴謹度：**本節證的都是「短、標準、具啟發」的定義法／級數證明**，忠實照手稿方法，不另創引理、不換證法。power rule 兩證法**並列保留**。
- forward-fence（各一行，不展開）：
  - product / quotient rules、`(fg)'≠f'g'` → §2.5
  - chain rule（含 `b^x`、一般 `a^x` 的導數）→ Ch3
  - 一般實數冪 `x^r`（`r∈ℝ`）的 power rule → 後章（需 log/chain）
  - `e^x` 級數的收斂性、逐項微分的嚴格正當性、`e` 的構造 → Ch4 §4.2–§4.3
  - `e^x` 的成長／衰減應用（微分方程 `y'=y`）→ 後續應用章
- **嚴守**：本節證完的規則才可在後續 example 使用；不偷跑 product/quotient/chain rule。`e^x` 沿用手稿「已定義為級數」的前提（這是 ROADMAP 已認可的 manuscript 選擇，見決策 G）。

## 承重直覺
**一個承重直覺領頭：「證一次，永遠當捷徑——把極限機器換成代數。」**
- 失敗例先打臉：要微分 `f(x)=3x⁴−5x²+2x−7`，照 §2.1–§2.3 的定義法得展開 `(x+h)⁴`、逐項消 `h`、取極限——對每個多項式都重跑一次，又長又易錯。我們不想為每個多項式重證一次。
- 關鍵動作：對每一類函數，把定義法的極限**證成一條通用規則**（constant、power、sum、constant-multiple），之後微分只剩**代數的 pattern-matching**，再也不碰極限。多項式微分因此塌縮成「逐項套 power rule」一行完成。
- 為它服務的次要亮點（exponential 半段的標誌）：`e^x` 是**自己的導數**——`d/dx e^x = e^x`，反覆微分永遠回到自己。這正是它被稱作 *natural* exponential 的理由，也是規則威力的最戲劇化展示。

## worked example 清單
| # | 內容 | 技巧 | 來源 |
|---|---|---|---|
| Ex 2.13 | 微分多項式 `f(x)=3x⁴−5x²+2x−7` → `f'(x)=12x³−10x+2` | 套 power + constant-multiple + sum（逐項），**不碰極限** | expansion:example（新增；須批准。新題型：rule-application，與 §2.1–§2.2 的 first-principles 計算題型**不同**）|
| Ex 2.14 | 微分 `g(x)=4e^x−x³+2x`：(a) `g'(x)=4e^x−3x²+2`；(b) 連算 `g''`, `g'''`, `g^(4)` 觀察 `e^x` 項不死、多項式項逐次歸零 | 套 `e^x` 規則 + linearity + 高階導數（接 §2.3）| expansion:example（新增；須批准。新題型：`e^x`＋多項式組合 + 高階導數交互，與 Ex 2.13 與既有例題皆**不同**）|

> **題目政策（使用者 2026-06-07 定）：** 手稿本節**零** worked example，故 Ex 2.13/2.14 皆為自創新題——依政策須 (1) **經你批准**（即此 ③ 閘）、(2) 題型與既有 example **不同**（均為 rule-application，相對 §2.1–§2.2 的 first-principles；兩例彼此也不同型）、(3) 一律寫成 **worked example**（env-example＋env-solution，含完整解＋講解）。**不寫 bare your-turn exercise**（含手稿的負整數冪 exercise，見決策 B）。每技巧 ≥1 例：多項式規則→Ex 2.13、`e^x` 規則→Ex 2.14。

序：先在每條規則 boxed 後用**行內小示例**（如 `d/dx x⁵=5x⁴`、`d/dx 7=0`）即時錨定；綜合 worked example 放在規則群之後（Ex 2.13 多項式）與 `e^x` 定理之後（Ex 2.14 組合＋高階）。同型不重講已建立 setup。

## history / application
- **歷史**：無自然可考人物史觸發 → 留白。`e` 的命名／級數的來歷屬 Ch4 的構造脈絡，本節不開（硬塞 Euler 軼事＝padding）。可在 `e^x` 處用**一句**點出「*natural* 之名來自 `d/dx e^x=e^x` 這個自我複製性質」——這是概念釐清（takeaway），非史料，不標 source。
- **應用**：本節為規則機制，無忠實真實錨。`e^x` 的成長／衰減應用需微分方程（`y'=y`），工具未備 → 留白，僅以 forward-fence 一句帶到後續應用章。硬接物理只會重複 §2.2 的 velocity bookend。

## 強調 / takeaway
- **概念樞紐**：每條微分規則都是**從定義證一次**、之後**當代數捷徑反覆用**——微分對 polynomial / exponential 這些函數類從此「機械化」，不再回到極限。
- **可攜技能**：(1) 用 power + sum + constant-multiple 規則**逐項**瞬間微分任意多項式；(2) 微分 `e^x` 並認得它是自己的導數（高階亦然）。

## 刻意不寫
| 不寫 | 理由 | 去哪 |
|---|---|---|
| product / quotient rule、`(fg)'≠f'g'` 的完整 caution | 本節未證；headline pitfall 屬 §2.5 | §2.5（本節僅以**一句** fence 預告乘法不像加法那麼乖，見決策 C）|
| chain rule、`b^x`/`a^x` 一般導數的證明 | 未引入 | Ch3（`b^x` 僅 Remark 2.6 預告結果、不證）|
| 一般實數冪 `x^r`（`r∈ℝ`）power rule | 需 log/chain | 後章 |
| `e^x` 級數收斂、逐項微分的嚴格正當性、`e` 的構造 | 本節照手稿直覺層級即可（ROADMAP 認可）| Ch4 §4.2–§4.3（會 rigorous 重推並 cross-ref 回本節）|
| `e^x` 成長／衰減的微分方程應用 | 工具未備 | 後續應用章 |
| 把負整數冪 exercise 展成完整定理／證明，或留成 bare exercise | 手稿為 exercise 提示、非定理；且政策禁 bare your-turn | 以 caution 點出結果＋同法可驗（見決策 B）|
| sin/cos/ln 等其他超越函數導數 | 非本節 | Ch3/Ch4 |
| strategy box | 多項式微分＝逐項套 power rule，Corollary 2.1 已涵蓋；ROADMAP 未指派本節 strategy（指派在 §2.2、§2.5）| 不放 |
| **bare your-turn exercise** | README §防護欄、CONTENT_SPEC §14 | 習題設計回合 |

> 餵 auditor：以上即 direction-conformance 的反向檢查——寫進任一項＝違反方向（多寫）；漏掉 constant/power（兩證）/sum/constant-multiple/polynomial corollary/`e^x` 導數＋級數論證/`b^x` remark/power-rule-domain caution＝違反方向（漏寫）。

## 篇幅帶
- 軟帶 **3.5–4.5 print 頁**。本節規則密（4 Theorem＋1 Corollary＋5 段證明＋1 Caution＋2 worked example＋1 Remark），比 §2.3 長、與 §2.2 相當。可讀性靠：每條規則前 1 段直覺、規則後行內小示例、2 個 worked example 打散公式牆。
- 明顯超出 → 回查：是否誤入 product/quotient/chain rule、或把 `e^x` 級數展成 Ch4 等級的 rigor、或負整數冪過度展開。

---

### Numbering 銜接（承 §2.3 末尾，手動）
- Theorem **2.2**（derivative of a constant：`(c)'=0`）
- Theorem **2.3**（the Power Rule：`(xⁿ)'=n x^{n−1}`，正整數 `n`）
  - env-proof（factorisation；`x→a` 式）
  - env-proof（alternative — binomial expansion；`x+h` 式）← 兩證並列
- Caution（power rule domain；ROADMAP pitfall；**無編號**，比照 §2.3 Caution）
- Theorem **2.4**（the Sum Rule and the Constant Multiple Rule；兩部分）
  - env-proof（極限的加法／常數倍法則）
- Corollary **2.1**（derivative of a polynomial；章內**首個** corollary → 新 counter 起 2.1）
  - 短證或 prose（逐項套 Theorem 2.2–2.4）
- Example **2.13**（多項式微分；expansion:example 新增）
- Theorem **2.5**（derivative of the natural exponential：`(e^x)'=e^x`；且 `f^{(n)}=e^x`）
  - env-proof（級數；`(e^h−1)/h→1`）
- Example **2.14**（`e^x`＋多項式組合 + 高階導數；expansion:example 新增）
- Remark **2.6**（derivative of `b^x`：`b^x·\ln b`，chain rule 預告、不證）
- Figure：**預設不放**（見決策 D）。Strategy：不放（仍停在 2.1）。

### ③ 待簽核決策（請逐項核可／改）
- **A — Power rule 兩證法擺放：** ✅建議**並列兩個 env-proof**（factorisation 為主、binomial 為 alternative，env-name 標明），都進正文。理由：kit 無 appendix 機制、§2.1–§2.3 證明一律 inline；兩證並列最忠於手稿教學選擇。（替代：正文一證＋另一證壓成 Remark——較不忠實，不建議。）
- **B — 手稿「負整數冪 exercise」處置：** ✅建議**做成一個 unnumbered Caution**（ROADMAP pitfall「power rule domain」）：本節證的是正整數 `n`；負整數 `n` 同樣成立（手稿留作 exercise，可用同一因式分解／二項法套到 `1/x^m` 驗證）；一般實數冪版 deferred 到後章。理由：直接落實 ROADMAP 指定的 caution、不產 bare your-turn、不為已夠密的節再加證明。（替代：展成 Ex 2.x worked example 證負整數冪——更示範但加密度；若你要我會改寫成含解例題。）
- **C — sum rule 處的 `(fg)'≠f'g'` 預告：** ✅建議**加一句** prose fence（標 expansion:caution）：加法微分乾淨地拆開，但乘法不會——`(fg)'≠f'g'`，故 §2.5 的 product rule 較微妙。**只一句**、不開 caution box（完整 caution 屬 §2.5）。（替代：完全不提，留給 §2.5。）
- **D — 是否放圖：** ✅建議**不放**（Figure 仍停 2.3）。理由：手稿無圖、ROADMAP 未指派 §2.4 key figure、本節內容偏代數（規則＋證明），密度由 2 例題與直覺段消化即可。（替代：若你要視覺紓解，可加 **Figure 2.4 = `y=e^x` 在某點切線斜率＝該點高度**，視覺化「自己的導數」——這是唯一夠格、最能體現本節亮點的圖；要的話我追加進 figures.js。）
- **E — Corollary 編號：** Corollary 為章內**首個** → **Corollary 2.1**（你的續編清單未列 corollary，特此確認）。
- **F — 兩個 worked example（Ex 2.13、2.14）批准：** 二者皆自創新題（手稿零例題），題型為 rule-application（與既有 first-principles 例題不同型）、彼此亦不同型，均寫成含解 worked example。請批准；若你只要一個或要調整函數/題型，告訴我。
- **G — `e^x` 級數前提 sign-off：** 本節沿用手稿「`e^x` 已定義為級數」的前提、用級數做直覺層級的導數論證（ROADMAP Open question 已記為 manuscript 選擇、待 sign-off；Ch4 §4.3 會 rigorous 重推並 cross-ref 回本節）。請確認照走。

### ROADMAP Open question 回填（待 ⑥ 後）
- 「Treatment of `e^x` derivative」：⑥ 簽核後，把本節「照 manuscript 級數論證、rigor 留 §4.3」的裁決標記為 confirmed（比照 §2.3 已 resolve「higher derivatives placement」的回填方式）。

# Direction Brief — §2.3 Differentiability, Continuity, and Higher Derivatives

> 待 ③ direction gate 核可。輸入：`seed_ch02_s3.md`（手稿 pp. 6–7）＋ §2.1–§2.2 成品（校準基準）＋ `CONTENT_ROADMAP.md` Ch2 條目。
> **ROADMAP 對齊（引用、不複述）：** core skill「recognise where a function fails to be differentiable (e.g. corners) and connect differentiability to continuity; compute higher-order derivatives」；key figure「non-differentiability at a corner (§2.3): the graph of |x| near 0, with the left and right secant slopes labelled to show the one-sided limits disagree」；pitfall「Differentiable implies continuous, but not conversely」；Open question「Higher derivatives placement: subsection of §2.3 vs standalone section」。

---

## 手稿盤點
（照原順序）
- 開場引言：`lim_{h→0} (f(a+h)−f(a))/h` may or may not exist → hence the definition
- Definition (differentiable)：`f` is differentiable at `a` if `f'(a)` exists；differentiable on `(a, b)` = differentiable at every point of the interval
- Example (non-differentiability)：`f(x) = |x|` at `x = 0`；`lim_{h→0} |h|/h`，左極限 `−1`、右極限 `+1` → limit DNE
- Figure：V-shaped graph of `|x|`（手稿標註）
- Theorem（無命名）：differentiable at `a` ⇒ continuous at `a`；converse not true（|x| at 0）
- Proof：goal `lim_{x→a} (f(x)−f(a)) = 0`；分解 `f(x)−f(a) = [(f(x)−f(a))/(x−a)] · (x−a)`；兩個極限分別存在 → 乘積 = `f'(a) · 0 = 0`
- Higher derivatives（短段落）：`f'` 本身是函數 → 可再求導 → `f'' = (f')'`；同理 `f'''`、…、`f^(n)(x)`
- **無**：worked example（除 `|x|` 反例）、exercise、strategy box、歷史、應用

## 薄度剖析
| 區塊 | 狀態 | 指向 |
|---|---|---|
| 「為何需要 differentiability 概念」的動機 | **薄** | 手稿一句帶過「limit may or may not exist, hence the definition」；可補 1 段：§2.2 整節假設極限存在，但有些點就是不行——引出「什麼時候 f' 存在？」的問題 |
| Definition (differentiable) | **夠** | 手稿已清楚 |
| 不可微的判別（|x| 例子＋圖） | **夠** | 手稿有完整推演（左右極限不等）；Figure 照 ROADMAP spec 擴充標注 |
| Theorem + Proof | **夠** | 手稿有標準完整證明，忠實照搬 |
| Converse 反例說明 | **薄** | 手稿一行「|x| at 0」；可用 env-caution 強調「⇒ 是單向」（ROADMAP pitfall） |
| Higher derivatives 記號 | **薄** | 只有文字一段；需引入 Leibniz 記號 `d²y/dx²`、`dⁿy/dxⁿ` 與 prime 記號對照（§2.2 已建記號慣例） |
| Worked example（計算 higher derivative）| **無** | 手稿無任何計算例；最低限度 1 例 |
| 應用／歷史 | **無** | 本節無自然觸發（見 history/application 欄）|

## 範圍與深度
- 吃 seed 這叢：differentiable 的定義 → 不可微判別（|x|）→ differentiable ⇒ continuous（定理＋證明）→ higher derivatives 子節（記號＋1 例）。
- 嚴謹度：**本節有且僅有一個定理及其證明**（Theorem 2.1）——照手稿方法走（乘積分解＋極限乘法法則），不另創引理、不換證法。
- forward-fence（各一行）：
  - 處處連續但處處不可微的函數（Weierstrass）→ 後章
  - 單邊可微／piecewise differentiability 的系統處理 → 後節
  - 高階導數的**應用**（曲率、Taylor）→ 後章
  - 微分法則（power/product/quotient）→ §2.4–§2.5
- **嚴守**：不偷跑未在 §2.1–§2.2 已證的微分法則；高階導數的 example 只用已建的定義法結果（如 `f'(x)=2x+4` → `f''(x)=2`）。

## 承重直覺
**一個承重直覺領頭：「有切線（可微）≠ 連續，但可微保證了連續——保險槓桿只朝一邊倒。」**
- 碰撞先打臉：§2.2 全程假設 `f'(x)` 存在就取極限——但在 `|x|` 的尖角處，左右割線分別收斂到 slope −1 和 +1，根本沒有共同極限；「可以算斜率」不是免費的。
- 承重定理帶來的安心：可微蘊含連續，意味著「只要 `f'(a)` 存在，函數在 `a` 絕不可能跳或斷」——可微是比連續更強的保證。但反過來不成立：`|x|` 在 0 連續卻不可微。
- 為它服務的次要心像：Figure 2.3 的左右割線不收攏 = 「沒有共同切線方向」= 不可微的幾何圖像。

## worked example 清單
| # | 內容 | 技巧 | 來源 |
|---|---|---|---|
| Ex 2.11 | `f(x) = |x|` at `x = 0`：用定義判不可微 | 分左右極限 → 不等 → limit DNE | 手稿 |
| Ex 2.12 | `f(x) = x² + 4x − 2`：求 `f''(x)` | 已知 `f'(x) = 2x + 4`（Ex 2.6）→ 再用定義或已知結果得 `f''(x) = 2`；附 `f'''(x) = 0` 說明 | expansion:example（新增；不同題型：higher derivative 計算，本節新引入）|

> **題目政策：** Ex 2.11 來自手稿（忠實內容）。Ex 2.12 是新增 worked example（經批准才寫），題型為「高階導數計算」——本節新引入、與 §2.1–§2.2 的一階計算題型不同。不寫 bare your-turn exercise。

序：不可微判別（Ex 2.11，衝接 Definition + Figure）→ Theorem 2.1 ＋ Proof → Caution → Higher derivatives 記號 → 計算例（Ex 2.12）。

## history / application
- **歷史**：無自然可考人物史觸發 → 留白。（Weierstrass 處處連續處處不可微的函數屬後章，不在此引入。）
- **應用**：本節性質偏理論（定義＋定理＋判別）；無忠實的真實應用錨 → 留白。硬塞 velocity 或物理只會重複 §2.2 的率-of-change bookend。

## 強調 / takeaway
- **概念樞紐**：differentiable ⇒ continuous 是**單向**蘊含——可微是比連續更強的正則性保證；反向用 `|x|` 堵死。
- **可攜技能**：分左右極限判不可微（`lim_{h→0⁺}` vs `lim_{h→0⁻}` 的差商若不等 → 不可微）；形成 `f''`、`f^(n)` 的基本能力。

## 刻意不寫
| 不寫 | 理由 | 去哪 |
|---|---|---|
| 處處連續處處不可微的函數（Weierstrass） | 超出本節深度、非手稿內容 | 後章進階專題 |
| 一般 piecewise 函數的分段可微性判準 | 手稿不含；可自然延伸但非必要 | 必要時後節或習題 |
| 高階導數的應用（Taylor、曲率、加速度） | 尚未引入工具 | 後章 |
| 微分法則（power/product/quotient） | 未證 | §2.4–§2.5 |
| 除 `|x|` 以外的不可微例子（cusp `x^(2/3)`、vertical tangent `x^(1/3)`） | 手稿只用 `|x|`；過多反例分散焦點 | 選配：若需第二例可加 cusp，但預設不加 |
| ε-δ 形式的連續性證明 | §2.3 的 continuous 用極限語言、不開 ε-δ | Ch1 / 附錄 |
| **bare your-turn exercise** | README §防護欄、CONTENT_SPEC §14 | 習題設計回合 |

> 餵 auditor：以上即 direction-conformance 的反向檢查——寫進任一項＝違反方向（多寫）；漏掉 Definition / |x| 例 / Figure 2.3 / Theorem + Proof / Caution / Higher-derivative 記號＝違反方向（漏寫）。

## 篇幅帶
- 軟帶 **2.5–3.5 print 頁**。本節結構緊湊（1 Definition、1 Example-as-非微、1 Figure、1 Theorem + Proof、1 Caution、1 子節 + 1 worked example）。比 §2.1–§2.2 短，因無 strategy box、無長串計算例。
- 明顯超出 → 回查：是否誤入微分法則計算、或 Weierstrass 函數展開。

---

### Numbering 銜接（承 §2.2 末尾，手動）
- Definition **2.3**（differentiable at a point / on an interval）
- Example **2.11**（|x| at 0 — 不可微判別；手稿）
- Figure **2.3**（|x| 的 V 形，標左右割線斜率；ROADMAP key figure）
- Theorem **2.1**（differentiable ⇒ continuous；本章首個定理）
- env-proof（Theorem 2.1 的證明；結尾 `<span class="qed qed-proof"></span>`）
- Caution（differentiable ⇒ continuous 是單向；ROADMAP pitfall；無編號）
- Remark **2.5**（higher-derivative notation：`f''`, `d²y/dx²`, `f^(n)`）
- Example **2.12**（higher derivative 計算：`f''(x)=2`；expansion:example 新增）

### ROADMAP Open question 待簽核
> **Higher derivatives 放置：** 手稿將 higher derivatives 作為 §2.3 的短尾子節（而非獨立 §2.4）。本 brief 依手稿：以 `<h3 class="subsec-head">` 子節收進 §2.3 尾部。**待你簽核：維持手稿安排（子節） vs 提升為獨立節。**

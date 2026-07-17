# 微積分講義排版指引

本指引適用於以 HTML + MathJax 製作、分頁輸出為 A4 的微積分講義系列。
所有規則以「學生能在 1.5 秒內解讀該行」為最高判準。

---

## 1. 行內公式 vs 行間公式

### 1.1 使用行內公式 `\(...\)` 的場合

| 類型 | 範例 |
|---|---|
| 變數、短符號 | `\(x\)`, `\(f(x)\)`, `\(\varepsilon\)`, `\(\delta\)` |
| 短等式 / 不等式 | `\(a = b\)`, `\(x > 0\)`, `\(n \ge 2\)` |
| 集合與區間 | `\([0, 1]\)`, `\(\mathbb{R}\)`, `\(x \in A\)` |
| 簡單分數（用 `\tfrac`） | `\(\tfrac{1}{2}\)`, `\(\tfrac{\pi}{6}\)` |
| 函數值 / 短運算 | `\(f(2) = -2\)`, `\(\sin(\pi/6) = \tfrac{1}{2}\)` |
| 行內極限（下標在側邊） | `\(\lim_{x \to a} f(x) = L\)` |

### 1.2 使用行間公式 `\[...\]` 的場合

- **定義中的核心公式**（如 ε-δ 定義的主不等式）
- **含有分數線高度超過一行的表達式**（分式、巢狀分式）
- **多步推導**（搭配 `aligned` 環境）
- **定理或命題中的主要等式**
- **含有下標極限、求和、積分作為主角的表達式**
- **分段函數**（`cases` 環境）
- **需要讀者駐足細讀的結果**

### 1.3 嚴禁事項

| 禁止 | 原因 | 替代方案 |
|---|---|---|
| 行內 `\dfrac{a}{b}` | 撐開行距，破壞段落節奏 | `\frac{a}{b}`（行內自動縮小）或 `\tfrac{a}{b}` |
| 行內 `\displaystyle` | 同上；極限下標移至正下方 | 直接寫 `\lim_{...}`；若覺得太小，移至行間 |
| 行間只放 `a = b` | 浪費垂直空間，打斷閱讀流 | 收入行內 |
| 括號內用 `\text{word}` | `\text{}` 結尾與數學括號之間會產生多餘間距 | 改用 `\mathrm{word}`，全程留在數學模式 |

> **範例：** `\(f(\text{student})\)` ✗ → `\(f(\mathrm{student})\)` ✓
> `\text{}` 僅用於行間公式的連接詞（如 `\quad\text{so}\quad`），不放在數學括號內。

### 1.4 分數記法速查

| 場景 | 指令 | 說明 |
|---|---|---|
| 行內簡單分數 | `\tfrac{a}{b}` | 小號分數，不撐行距 |
| 行內比值 | `a/b` | 最緊湊：`1/2`, `3/x`, `1/x^{2}` |
| 行內一般分數 | `\frac{a}{b}` | MathJax 行內自動縮小，可接受 |
| 行間公式 | `\frac{a}{b}` | 自動 display size |
| 巢狀分式 | 外層 `\frac`，內層 `\tfrac` | 避免層層放大 |
| **絕對禁止** | `\dfrac` 出現在 `\(...\)` 中 | — |

### 1.5 極限、積分等大型算子

| 場景 | 寫法 | 效果 |
|---|---|---|
| 行內 | `\(\lim_{x \to a}\)` | 下標在 lim 右側，行距正常 |
| 行間 | `\[ \lim_{x \to a} \]` | 下標在 lim 正下方 |
| 行內覺得太小 | 整個搬到行間公式 | 不要加 `\displaystyle` |

**一律不在 `\(...\)` 中使用 `\displaystyle`。**

---

## 2. 行間公式的換行

### 2.1 使用 `aligned` 環境的時機

- 多步推導，每步一行，以 `&=` 或 `&\implies` 對齊
- 兩組以上的獨立等式需要並列比較時

### 2.2 單行寬度上限

- 每行排版後不超過**版心寬度的 85%**（A4 頁面約 45–55 個 TeX 字元）
- 超過時必須換行

### 2.3 換行位置（優先順序）

1. 在 `=` 號前換行（新行以 `&=` 開頭）
2. 在 `\implies`、`\Longleftrightarrow` 前換行
3. 在 `+`、`-` 等二元運算符前換行
4. 在逗號後換行（多個獨立表達式並列時）

### 2.4 同行並列規則

| 數量 | 處理方式 |
|---|---|
| 2 個短表達式 | 可用 `\qquad` 分隔於同一行 |
| 3 個以上 | 一律用 `aligned` 分行，或每行最多 2 個 |
| 鏈等式 | 同一行最多 **3 個** `=` 號；超過則換行 |

### 2.5 範例

**不好** — 兩組驗算擠在一行，超出版心：
```html
\[ f(f^{-1}(x)) = \frac{3}{(5+\tfrac{3}{x})-5} = \frac{3}{3/x} = x, \qquad f^{-1}(f(x)) = 5+\frac{3}{3/(x-5)} = 5+(x-5) = x. \]
```

**改進** — 一組一行，`aligned` 對齊：
```html
\[ \begin{aligned}
f\!\bigl(f^{-1}(x)\bigr) &= \frac{3}{\bigl(5+\tfrac{3}{x}\bigr)-5} = \frac{3}{3/x} = x, \\
f^{-1}\!\bigl(f(x)\bigr) &= 5+\frac{3}{3/(x-5)} = 5+(x-5) = x.
\end{aligned} \]
```

---

## 3. 段落中的數學表達式密度

### 3.1 原則

一個段落中**不宜連續出現 3 個以上含分數的行內公式**。
如果推導步驟多到需要一連串行內等式，應將關鍵步驟搬到行間公式。

### 3.2 範例

**不好** — 三個 `\frac` 擠在一句話裡：
```
Let \(y = \frac{3}{x-5}\). Solving for \(x\): \(x-5 = \frac{3}{y}\), so \(x = 5+\frac{3}{y}\).
```

**改進** — 保留第一個行內，其餘搬到行間：
```
Let \(y = \frac{3}{x-5}\). Solving for \(x\):
\[ x - 5 = \frac{3}{y}, \quad\text{so}\quad x = 5 + \frac{3}{y}. \]
```

---

## 4. 換頁（分頁）控制

### 4.1 禁止斷裂處

- 標題（`sec-head`、`subsec-head`）之後的第一段不可斷開
- 環境（定義、定理）的**頭部**與**本體第一行**不可分離
- 範例的**題目**與**解答開頭**盡量在同一頁

### 4.2 孤立標題防護（Orphan Heading Prevention）

分頁器 `place()` 函數中內建主動偵測：當一個標題放入頁面後，**測量頁底剩餘空間**，若不足以容納後續內容，則將標題移至下一頁。

| 標題類型 | 對應 class | 頁底最低剩餘空間 |
|---|---|---|
| 章節標題 | `.chapter-head` | ≥ 160px |
| 大節標題（如 §1.5） | `.sec-head` | ≥ 160px |
| 小節標題 | `.subsec-head`, `.para-head` | ≥ 100px |

**實作邏輯**（在 `place()` 的 `if (fits())` 分支內）：
```js
if (isHeading(block) && body.childElementCount > 1) {
  var remaining = (bodyRect.top + body.clientHeight) - blockRect.bottom;
  var threshold = block.matches(".sec-head, .chapter-head") ? 160 : 100;
  if (remaining < threshold) {
    body.removeChild(block);
    newSheet();
    body.appendChild(block);
  }
}
```

- 僅在頁面**已有其他內容**時觸發（避免空頁再推）
- 此邏輯適用於所有章節，無須逐章手動調整

### 4.3 減少頁底留白的手段

| 手段 | 效果 |
|---|---|
| 將不必要的行間公式改為行內 | 每處省下約 1.5–2 行高 |
| 移除 `\dfrac`、`\displaystyle` 造成的行距膨脹 | 段落整體高度縮減 |
| 適當壓縮行間公式 margin（`.6em` → `.5em`）| 全域微縮 |
| 短環境（如 Remark）不跨頁 | 避免 0.5 行內容佔一整頁頂部 |

### 4.4 分頁演算法配合

- 確保 `workedexample` 容器只包含 example + solution 兩個子元素，方便分頁器拆分
- `env-body` 內部以 `<p>`、`<ol>`、`<ul>` 為最小單位，避免巨大的單一 `<p>` 塊

---

## 5. 圖片尺寸控制

### 5.1 CSS 變數系統

每章在 `:root` 中為每張圖定義獨立的寬度變數，格式為 `--fig-{章}-{圖號}`：

```css
:root {
  --fig-1-1:  250px;   /* Figure 1.1  pair 佈局每張 */
  --fig-1-2:  340px;   /* Figure 1.2  單張 SVG */
  --fig-1-5:  340px;   /* Figure 1.5  受限正弦 */
  ...
}
```

`hydrateFigures()` 會自動從 `<figcaption>` 讀取圖號（如 "Figure 1.5"），並對該 `<figure>` 設定：
```js
el.style.setProperty("--fig-w", "var(--fig-1-5)");
```
如此 `:root` 的數值即可生效，且所有圖的寬度都可從同一處集中調整。

### 5.2 圖片寬度設定原則

| 佈局類型 | 預設寬度策略 | 說明 |
|---|---|---|
| `pair`（並排兩圖） | `--fig-w-pair`（全域）或逐圖設定 | 兩張圖各佔一半，用 `--fig-w-pair` 統一控制 |
| `single`（單圖） | 依 SVG 原始寬度設定 px 值 | **禁止使用 100%**，應依 SVG 尺寸給合理上限 |
| `triple`（三圖並列） | `100%`（容器自動分配） | 容器內部自行均分 |
| `grid`（2×2 等）| `100%`（容器自動分配） | 容器內部自行均分 |

### 5.3 單圖寬度速查表

依 SVG 原始尺寸建議對應的 `--fig-N-M` 值：

| SVG 寬度 | 建議 CSS 寬度 | 備註 |
|---|---|---|
| ≤ 280px | 250–280px | 小圖，如限制函數 |
| 280–400px | 300–380px | 中型圖，如函數圖 |
| 400–500px | 380–420px | 較寬圖，如 ε-δ 幾何 |
| 500–650px | 450–520px | 寬幅圖，如橫跨座標軸 |
| > 650px | `100%` 或 520px | 極寬圖才允許 100% |

### 5.4 核對要點

- [ ] 每張新圖都在 `:root` 中有對應 `--fig-{ch}-{n}` 變數
- [ ] 單圖佈局**不使用 100%**，除非 SVG 寬度 > 650px
- [ ] `hydrateFigures()` 自動映射生效（不需手動加 style）
- [ ] 並排圖使用 `--fig-w-pair` 全域控制，或逐圖覆寫

---

## 6. 標點符號

| 位置 | 規則 | 範例 |
|---|---|---|
| 行間公式結尾 | 句號／逗號寫在 `\]` 之前 | `\[ x = 1. \]` |
| 行內公式結尾 | 標點寫在 `\)` 之後 | `\(\ldots = 1\).` |
| `aligned` 最後一行 | 末尾加句號或逗號 | `&= \varepsilon.` |
| 多行 `aligned` 中間行 | 逗號或不加（視語境） | `&= 2x - 6,\\` |

---

## 7. 表格中的公式

- 表頭的函數表達式使用 `\frac`（表格行距較鬆，可容納）
- 若表達式過高（巢狀分式），考慮在表格外以行間公式呈現函數定義，表格內僅放數值

---

## 8. 核對清單

每一節撰寫完成後，逐項檢查：

- [ ] **無行內 `\dfrac`** — 全文搜尋 `\dfrac`，確認全部在 `\[...\]` 中
- [ ] **無行內 `\displaystyle`** — 全文搜尋 `\displaystyle`，確認全部在 `\[...\]` 中
- [ ] **單行行間公式不超寬** — 目視檢查無水平溢出
- [ ] **鏈等式 ≤ 3 個 `=`** — 超過者用 `aligned` 拆行
- [ ] **並列表達式 ≤ 2 組 / 行** — 超過者分行
- [ ] **段落內無連續 3+ 個含分數的行內公式** — 密集處搬到行間
- [ ] **無孤立標題** — 標題後至少跟一段文字才換頁（分頁器自動處理，但目視確認）
- [ ] **範例題目與解答開頭同頁** — 視覺確認
- [ ] **頁底留白 < 1/4 頁** — 若超過，檢查前方內容是否可壓縮
- [ ] **行間公式結尾標點正確** — 句號在 `\]` 之內
- [ ] **每張圖有 `:root` 寬度變數** — `--fig-{ch}-{n}` 皆已設定
- [ ] **單圖佈局不使用 100%** — 除非 SVG 寬度 > 650px
- [ ] **`hydrateFigures()` 映射生效** — figcaption 圖號 → `--fig-w` 自動連結

---

## 9. 全域字體與版心系統（2026-06-22 拍板）

本節記錄整套講義的字體與版心決策，以及一個**容易踩雷的分頁耦合**。

### 9.1 字體

| 角色 | 字體 | 設定處 | 備註 |
|---|---|---|---|
| 內文／散文（prose） | **New Computer Modern** | `--serif` | 與數學字體同源，達成 prose／math 字形一致 |
| 數學（math） | **New Computer Modern** | MathJax 4 預設 `mathjax-newcm` | 不需設定，是 MathJax 4 內建預設；**勿改 MathJax `output.font`** |
| UI／標籤／表格／圖說 | Inter | `--ui` | kicker、figcaption、`table.tbl`、SVG 標籤 |

- **內文 NCM 來源：** webfont `web-computer-modern@1.1.0-new-cm-7-0-2`（npm，jsDelivr CDN），10pt 視覺尺寸（"Serif 10"），GUST Font License。
  `@font-face` 寫在各 standalone 的 `<head>`（緊接 Inter 的 `<link>` 之後）。
- **檔名含空白，URL 必須以 `%20` 編碼**（如 `WebCM%20Serif%2010%20Regular.woff2`）。用生空白或改名會 404，並**靜默退回 Times**——務必保留 `%20`。
- `--serif` 退路鏈：`"New Computer Modern", "Latin Modern Roman", "Times New Roman", Times, Georgia, serif`。
- 字級：`.sheet-body.paper { font-size: 12pt; line-height: 1.55; }`。改 `line-height` 須同步改 `.qed` 的負 margin（綁定 `1.55em`）。

### 9.2 版心（measure）

- **版心寬 150mm**（講義型取向）：A4 210mm，`.sheet { padding: 20mm 28mm 20mm 32mm; }`（左 32／右 28，留 4mm 裝訂偏移）。
- 配 12pt NCM 約 **73–77 字元／行**——刻意比書籍最佳值（66）寬一點，換取講義要的密度（每頁多塞、頁數少、長 `aligned` 推導少斷行），仍在可讀上限（~75–80）內。
- running header 對齊版心：`.sheet-header { left: 32mm; right: 28mm; }`。
- **沿革：** 168mm／11pt Times（約 98 cpc，過寬）→ 一度收到 140mm（約 68 cpc，偏書籍級寬邊）→ 定案 150mm（講義密度與可讀的折衷，使用者 2026-06-22 拍板）。若改回更窄（如 140mm）追求閱讀舒適或留寬邊供手寫註記，見 §9.3／§9.4 的連動。

### 9.3 ⚠️ 分頁耦合：改版心必同步改 `#source`（踩雷點）

分頁器在離屏的 `#source > .paper > #page` 量測 MathJax 的**行內／行間公式斷行**，再把 block 搬進真正的 `.sheet-body`（垂直 fit 在真 sheet 量測，但**水平斷行沿用 staging 的結果**）。因此：

> **staging 的文字寬必須等於 sheet 版心寬，否則行間公式可能溢出較窄的頁面。**

staging 文字寬 = `#source` 寬 − `.paper .page` 左右 padding（2×58px = 116px）。所以：

```
#source width = 版心寬(px) + 116
```

目前 150mm = 567px → `#source { width: 683px; }`（換算：567 + 116）。**任何時候改了 `.sheet` 的左右 padding（版心寬），就要照上式重算並改 `#source` 寬**，否則含長公式的頁面會在列印時被裁切。改完務必瀏覽器實測：`mjx-container[display="true"]` 無 `scrollWidth > clientWidth`。

### 9.4 表格在窄版心的配合

`table.tbl` 儲存格水平 padding 維持原設計 `.8em`（`padding: .3em .8em`）；在 150mm 版心下，多欄數值表（如 7 欄極限值表，約 521px）仍能容納於縮排環境內，無需收窄。**但若版心再收窄（如曾測試的 140mm），這類表會溢出**——當時的解法是把儲存格水平 padding 收為 `.65em`。所以：**收窄版心時務必重測表格** `.tbl-wrap` 是否 `scrollWidth > clientWidth`；若溢出，先收 `.8em → .65em`，仍不夠再考慮縮表格字級。新增寬表時一律目視確認。

### 9.5 四章 standalone 各自帶一份相同 CSS

全部 `standalone/chapter{N}-print-standalone.html` 的 `<head>` CSS 是**各自獨立的副本**（無共用樣式表）。上述任一全域樣式（字體、版心、`#source`、表格 padding）變更時，**全部 standalone 檔都要一起改**，否則章節間排版不一致。`build.py` 只替換內容區、不動 CSS shell。


## 10. Reading-track 標示（2026-07-03 拍板）

主線／證明補充的**閱讀路徑標示**系統。緣起：作者提議把「主線學習」與「嚴格補債」拆成兩軌（拆章重排）；經兩輪 Codex 仲裁定案為**不動章界、不動編號的文字層標示**（全程紀錄見 `handout/html/_audit/REVIEW-ch01-ch04-difficulty-mitigation-applied.html`）。

### 10.1 兩種標示與統一措辭

- **`First reading:`**——節級，標「初讀可整節後補」的嚴格化層。措辭型：說明本節在做什麼＋後文用到的是什麼＋何時回來（指出第一個真正需要它的位置）。
- **`Proof track:`**——證明塊級，標「初讀可先取結論」的長證明。措辭型：`Proof track: this argument earns the theorem. <後文用的是陳述而非證明> — on a first reading you may take the result and move on.`（"earns" 呼應 §3.2 既有橋接句的聲音；「後文用什麼」子句依落點事實微調，不得套用不實的統一句）。

### 10.2 HTML 形式與落點

一律用普通段落 `<p><em>…</em></p>`：**不進 env、不編號、不觸發任何 counter**。落點：節級標示放 `<header class="sec-head">` 之後；證明塊級放對應 `<section class="env env-proof">` 之前；章級路線圖（僅 foundation 章）放 chapter opener 的 "By the end of this chapter" 清單之後。

### 10.3 掛標原則：主線預設隱形、寧缺勿濫

- 只標非主線單元；mainline 不掛標（徽章噪音會稀釋導航價值、侵蝕本書「誠實構造」的身份）。標示是**導航**，不是內容降級。
- 已有 skip 路標／signpost 的單元不重貼（§3.2 證明塊、§4.2 節首 signpost 屬前一輪難度緩解，功能等價）。
- 不做 badge 系統、不做雙目錄、不改 `build.py`。

### 10.4 現行掛標清單（Ch1–Ch4，2026-07-03）

| 落點 | 標示 |
|------|------|
| §1.6 節首 | `First reading:`（ε-δ 嚴格化層；Ch2 只用 limit laws——已 grep 驗證 ch02 零 ε-δ；第一個需要處為 §3.2 證明） |
| Ch4 opener | 章級路線圖（全書唯一 foundation 章） |
| §4.1 Theorem 4.2 證明前 | `Proof track:`（後文用收斂事實＋尾項 bound (*)） |
| §4.4 Theorem 4.10 證明前 | `Proof track:` 一則涵蓋 Theorem A → Rolle → MVT 三連證明梯 |
| §4.5 Theorem 4.13 證明前 | `Proof track:`（後文只用 ln 連續性的陳述） |
| §2.4 e^x 級數段 | 不編號 Caution box 標「on credit」（credit fence 的醒目化，非 reading-track 句型但同屬本輪） |

Ch2 全章、§3.1／§3.3、§4.2（已有 signpost）、§4.3（短、核心 payoff）**不掛**。後續新章沿用本節原則；新增掛標時更新上表。

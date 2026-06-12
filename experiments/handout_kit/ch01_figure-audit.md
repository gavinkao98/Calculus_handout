# Ch 1 圖的數學正確性稽核

> **審查者：** Claude（本對話內直接比對 `figures.js` vs 課文 HTML）。
> **被審物：** [`example-ch01/figures.js`](example-ch01/figures.js)（13 幅圖）。
> **基準：** [`example-ch01/sec-1-1.html`](example-ch01/sec-1-1.html) …
> [`sec-1-6.html`](example-ch01/sec-1-6.html) 的散文、figcaption、定義、範例。
> **日期：** 2026-06-12。
> **稽核維度：** 即 [`PROMPT-ch01-example-selection-audit.md`](PROMPT-ch01-example-selection-audit.md) 新增的
> dimension E（圖的數學正確性）。

---

## 結果摘要

**blocking = 5（Claude 手動 3 + Codex 獨立 2），advisory = 1。全數已修。**

---

## Blocking findings

### B1. Figure 1.13 `precise-limit` — ε-strip 不對稱

**結論：** 標為 "L−ε" 和 "L+ε" 的兩條水平線到 L 的距離不相等，違反 ε-δ 定義中 ε 為單一正數的語義。

**證據：**
- `figures.js:268–269`：`Lm = 6.498019`、`Lp = 9.849155`；L = 2³ = 8（`pow2(3)`）。
- L − Lm = 1.501981；Lp − L = 1.849155——兩者不相等。
- Lm、Lp 實為 2^(a−δ) = 2^2.7 和 2^(a+δ) = 2^3.3 的精確值，不是 L ± 同一個 ε。
- 標記文字（`figures.js:290–292`）寫 `L-\varepsilon` 和 `L+\varepsilon`，暗示對稱，與數值矛盾。

**為何 blocking：** 高中自學者看到的幾何解讀是「ε-strip 由兩條等距水平線構成」；
非等距的圖會給出錯誤心智模型——以為 ε 在上下兩側可以不同。

**建議修法：** 取 ε = max(Lp − L, L − Lm) = 1.849155，讓下方水平線改為
L − ε = 8 − 1.849155 = **6.150845**。如此：
- 上方 hline 保持 y = 9.849155（曲線在 x = a+δ 恰觸上界）。
- 下方 hline 移至 y = 6.150845（曲線在 x = a−δ 處 y ≈ 6.498，在 strip 內部、不觸下界）。
- 圖正確呈現「δ-鄰域的像落在 ε-strip 之內，但不一定兩端都貼邊」。

改動：`figures.js:268` → `const Lm = 6.150845`；其餘 dot 座標可保留或移除
`(2.7, Lm)` 的小圓點（因曲線不再觸下界）。

---

### B2. Figure 1.9 `read-limit-graph` — 曲線只有單側，但範例要求雙側極限

**結論：** 曲線 domain 在 x ≈ 1.98 截止，x > 2 完全無曲線。Example 1.15(c) 問
lim_{x→2} f(x)（雙側），解答宣稱極限為 2——但學生從圖上看不到右側趨近行為。

**證據：**
- `figures.js:207`：`domain: [-2.8, 1.98]`——只有一段曲線，到 x = 1.98 為止。
- `sec-1-3.html:49`：Example 1.15(c) 問 `\lim_{x \to 2} f(x)`（雙側）。
- `sec-1-3.html:59`：解答寫 "As x approaches 2, the curve approaches height 2"——
  「approaches 2」暗示雙側，但圖上 x > 2 無曲線可讀。
- 圖的 xmax = 2.9（`figures.js:202`），plot 區域延伸到 x > 2 但該區空白。

**為何 blocking：** 「看圖讀極限」的題目中，圖即命題的一部分。圖上缺右側曲線，
學生無法判斷右側極限是否存在（甚至可能解讀為函式在 x > 2 無定義），與解答矛盾。

**建議修法：** 加一段右側曲線，讓同一多項式從 x > 2 也趨近 (2, 2)。
多項式 f(x) = −0.0375x³ + 0.375x² + 0.4x 在 x = 2 處值為 2.0，右側自然延續。
改動 `figures.js:207`：

```js
{ type: "curve", fn: (x) => -0.0375*x*x*x + 0.375*x*x + 0.4*x,
  domain: [-2.8, 1.98], samples: 200, cls: "curve" },
{ type: "curve", fn: (x) => -0.0375*x*x*x + 0.375*x*x + 0.4*x,
  domain: [2.02, 2.7], samples: 50, cls: "curve" },
```

這讓曲線從雙側趨近 (2, 2) 的 hollow dot，右側到 x ≈ 2.7 足以讓學生讀出右側極限。

---

### B3. Figure 1.12 `vertical-asymptote` — y-range 過大，曲線形狀不可讀

**結論：** `ymin: -66, ymax: 66` 讓 y = 2x/(x−3) 的曲線在大部分區間貼死在 x 軸上，
水平漸近線 y = 2 不可辨識，函式的彎曲與 x 截距 (0, 0) 均不可見。

**證據：**
- `figures.js:253`（修前）：`ymin: -66, ymax: 66`。
- 函式在 x ∈ [−1, 2.5] 的值域為 [−10, 0.42]，佔 y-range 的 8%——視覺上是一條平線。
- 水平漸近線 y = 2 佔 y-range 的 1.5%——與 x 軸不可區分。
- 無 ytick，讀者無刻度參照。

**為何 blocking：** 教學圖的功能是讓學生讀出函式的定性行為。
viewing window 過大導致「曲線形狀不可讀」等同於圖畫錯——學生無法從中辨識
漸近線、截距、方向，與文字描述脫節。

**修法：** `ymin` → −20、`ymax` → 20，加 `yticks: [{ y: 2, tex: "2" }]`。
曲線在漸近線附近自然超出可視區域（SVG 裁剪），其餘區段的形狀、水平漸近線 y = 2、
x 截距 (0, 0) 均可辨識。

---

### B4. Figure 1.5 `restricted-sine` / Figure 1.6 `restricted-cosine` — ytick 缺文字標籤（Codex 發現）

**結論：** `yticks: [{ y: -1 }, { y: 1 }]` 缺 `tex` 欄位；`plot.js` 的 fallback `piTex()` 只認 π 的倍數，
整數 −1, 1 不在 map 中 → 刻度線畫了但沒有文字。學生看不到 ±1 的數值標籤。

**證據：**
- `figures.js:100`（restricted-sine）、`figures.js:114`（restricted-cosine）。
- `plot.js:85,92`：`tex` 為 null 且非 π 倍數時不產出任何文字。

**為何 blocking：** range [−1, 1] 是反三角函式的核心教學資訊；缺標籤時讀者無法確認刻度值。

**修法：** 改為 `{ y: -1, tex: "-1" }, { y: 1, tex: "1" }`。已同步 figures.js + 兩份 standalone。

---

### B5. Figure 1.9 `read-limit-graph` — xtick / ytick 缺文字標籤（Codex 發現）

**結論：** `xticks: [{ x: -2 }, { x: 2 }]` 缺 `tex`，`piTex()` 不認整數 → 無文字。
且完全沒有 `yticks`——讀圖題要學生讀出 y 值但圖上無 y 刻度。

**證據：**
- `figures.js:205`：xticks 無 tex；無 yticks。
- `sec-1-3.html:45–59`：Example 1.15 要求從 Figure 1.9 讀出 x = −2, 0, 2 的極限值。

**為何 blocking：** 讀圖題的圖等同命題的一部分，缺可讀座標時學生無法作答。

**修法：** xticks 加 `tex: "-2"` / `tex: "2"`；新增 `yticks: [{ y: -2, tex: "-2" }, { y: 1, tex: "1" }, { y: 2, tex: "2" }]`。
已同步 figures.js + 兩份 standalone。

---

### A1（advisory）. `arcsin-triangle` — 三角形頂點比例與標籤不完全吻合（Codex 發現）

頂點 (0,0),(3,0),(3,1) 畫出邊長 3-1-√10，但標籤寫 2√2-1-3。
**不影響教學正確性**——標籤數學完全正確（1² + (2√2)² = 9 = 3² ✓），三角形是示意圖。
教科書中三角形示意圖常用近似比例。降為 advisory，不修。

---

## Codex 審核紀錄

- **審核者：** Codex（gpt-5.5, xhigh reasoning, read-only sandbox）
- **prompt：** `PROMPT-ch01-figure-audit.md`
- **日期：** 2026-06-12
- **token 用量：** 175,587
- **原始輸出：** `.tmp/ch01-figure-audit-output2.txt`
- **Codex 報告 blocking 4 條；Claude triage 後認定 2 條真 blocking（B4, B5）、1 條 advisory（A1）、
  1 條非 finding（precise-limit 使用 2^x 是刻意的泛型示意，非課文 f(x)=2x−1）。**

---

## 回歸審核（修復後驗證）

- **日期：** 2026-06-12
- **審核者：** Claude（手動比對 figures.js + plot.js 渲染邏輯 + 三份檔案同步性）
- **範圍：** B4（restricted-sine / restricted-cosine ytick）、B5（read-limit-graph xtick / ytick）

| Finding | 驗證項目 | 結果 |
|---------|---------|------|
| B4 | `tex` 欄位存在 → `plot.js:92` 走 `t.tex != null` 分支渲染文字 | ✓ |
| B4 | 三份檔案（figures.js + 兩份 standalone）一致 | ✓ |
| B4 | 數學正確性：sin/cos restricted range = [−1,1]，標 ±1 正確 | ✓ |
| B5 | xticks `tex: "-2"` / `tex: "2"` 存在且三份檔案一致 | ✓ |
| B5 | yticks `tex: "-2"` / `tex: "1"` / `tex: "2"` 存在且三份檔案一致 | ✓ |
| B5 | 數學正確性：Example 1.15 答案值 (1, 0, 2, −2) 被 yticks 涵蓋 | ✓ |
| 全域 | 修改未引入新問題 | ✓ |

**結論：B4、B5 修復正確，無回歸問題。**

---

## 通過的圖（8 幅，無 finding）

| 圖 ID | Figure # | §  | 驗證項目 |
|--------|----------|-----|---------|
| `hlt` | 1.1 | 1.1 | 恒等函式 1-to-1 ✓；縮放拋物線 not-1-to-1 ✓；交點座標一致 ✓ |
| `restrict-x2` | 1.3 | 1.1 | x², √x 互逆 ✓；y=x 對稱線 ✓；標記 ✓ |
| `sine-not-1to1` | 1.4 | 1.2 | sin x 全域 ✓；y=0.5 的 5 個交點 x 座標驗算皆為 sin⁻¹(0.5) 的各分支 ✓ |
| `restricted-sine` | 1.5 | 1.2 | domain [−π/2, π/2] ✓；range [−1, 1] ✓；**ytick 標籤另列 B4** |
| `restricted-cosine` | 1.6 | 1.2 | domain [0, π] ✓；range [−1, 1] ✓；**ytick 標籤另列 B4** |
| `restricted-tangent` | 1.7 | 1.2 | domain (−π/2, π/2)，曲線於 ±1.37 截止（在漸近線之內）✓；vline 標漸近線 ✓ |
| `arcsin-triangle` | — | 1.2 | 直角三角形 opp=1, adj=2√2, hyp=3；1²+(2√2)²=9=3² ✓；θ=arcsin(1/3) ✓ |
| `limit-same-near-a` | 1.8 | 1.3 | 三面板 f(a)=L / f(a)≠L / f(a) undef，皆趨近 L=8=2³ ✓；hollow/solid 正確 ✓ |
| `one-sided-limits` | 1.10 | 1.4 | 左側極限 1 ✓；右側極限 2 ✓；兩側 hollow ✓ |
| `one-sided-infinite` | 1.11 | 1.4 | 四個面板方向全正確（1/(2−x)→+∞ from left 等）✓ |
| `vertical-asymptote` | 1.12 | 1.4 | 函式 2x/(x−3) ✓、漸近線 x=3 ✓、方向（左→−∞、右→+∞）✓；**viewing window 另列 B3** |

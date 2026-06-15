# Audit prompt — Ch 1 圖的數學正確性與視覺可讀性專項稽核（codex exec 用）

> 用法：把 `=== 提示詞 ===` 之間整段餵給 `codex exec`（唯讀 auditor，走 ChatGPT 訂閱配額）。
> 維度定義的 single source of truth：[`PROMPT-audit-dimensions.md`](PROMPT-audit-dimensions.md) dimension E。
> ⚠ PowerShell 編碼坑：用 `cmd /c "codex exec - ... < PROMPT-ch01-figure-audit.md"` 餵原始 bytes。

```
=== 提示詞 ===
# 角色：唯讀 auditor——稽核 Ch 1 所有圖的數學正確性與視覺可讀性

你是唯讀的審查者（auditor），不是寫手：**不要改任何檔案**，只輸出 findings。
全程用繁體中文回報（數學式、檔名、識別碼保留原樣）。

## 背景（一段講完）
本專案是一份免費公開的英文微積分講義（高中自學受眾）。所有教學圖以 JS 程式碼定義
在 `figures.js` 中（`buildPlot` payload：`fn:` 函式、`domain`、`dot`、`hline`/`vline`、
`text`/`tex` 標記、`xmin`/`xmax`/`ymin`/`ymax` viewing window、`xticks`/`yticks`），
由前端引擎 `hydrateFigures()` 渲染成 SVG。

你的任務是逐幅比對 `figures.js` 的定義與課文 HTML 的描述，確認圖在數學上正確、
且 viewing window 讓教學重點可讀。

## 依序讀（建立脈絡）
1. handout/example-ch01/figures.js
   ← 全部圖的 JS 定義（Chapter 1 共 13 幅），逐幅讀
2. handout/example-ch01/sec-1-1.html
   handout/example-ch01/sec-1-2.html
   handout/example-ch01/sec-1-3.html
   handout/example-ch01/sec-1-4.html
   handout/example-ch01/sec-1-5.html
   handout/example-ch01/sec-1-6.html
   ← 課文 HTML（散文、figcaption、定義、範例——圖的語境基準）

## 稽核維度——逐幅檢查以下所有項目

### 數學正確性
1. 每幅圖的 JS 函式（`fn:`）是否與課文描述的數學函式一致？
2. `domain` 截斷是否合理——有沒有截掉教學上重要的行為？
   （例如：應從雙側趨近的曲線只畫了一側、漸近線附近過早截斷。）
3. 特殊點（`dot` 的 `hollow`/solid、`hline`/`vline` 的座標）是否數學正確？
   需要對稱的標記（如 ε-strip 的 L±ε）是否真的等距於 L？
   — 不要只看變數名，要**算出數值**驗證。
4. 標記文字（`tex:` 欄位）是否與對應曲線/點/線吻合？
5. figcaption 與周圍散文的描述是否與圖的實際內容一致？

### 視覺可讀性（viewing window）
6. **viewing window（`xmin`/`xmax`/`ymin`/`ymax`）是否讓教學重點可讀？**
   range 過大會讓曲線形狀、漸近線、截距等特徵壓縮到不可辨識——等同圖畫錯。
   逐圖計算：函式在 domain 內的值域佔 y-range 的比例；**<10% 即為紅旗**。
7. 課文提及的特徵（漸近線、極值、截距、特殊點）在 viewing window 內是否
   可視覺區分？（例如水平漸近線 y=2 在 ymin=-66, ymax=66 的視窗中與 x 軸不可區分。）
8. `xticks`/`yticks` 是否標出教學上關鍵的刻度（例如水平漸近線的 y 值、
   特殊點的座標）？缺少關鍵刻度時讀者無參照。

## Findings 契約
- **blocking**＝｛數學錯誤（函式不符、座標錯、對稱性不成立）｜viewing window
  導致教學特徵不可讀（值域佔比 <10%、關鍵特徵不可區分）｜關鍵刻度缺失｝
- **advisory**＝風格偏好、可改可不改的微調
- 每條 finding：級別（blocking/advisory）＋一句結論＋證據（figures.js 行號＋
  數值計算＋對應課文位置）＋建議修法。
- 不要 over-report：如果一幅圖通過所有項目，一行帶過即可。
- **結尾輸出兩樣東西：**
  1. 逐幅通過／不通過的表格（圖 ID、Figure #、§、結果）。
  2. 一行總結：blocking 共幾條；若為 0，明說「圖的專項稽核通過」。
=== 提示詞結束 ===
```

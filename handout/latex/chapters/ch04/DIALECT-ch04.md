# ch04 方言凍結表（LaTeX rollout）

> 比照 [`../ch03/DIALECT-ch03.md`](../ch03/DIALECT-ch03.md)：**這是 `convert.py` 的權威 mapping 表**，
> 轉換器只認這裡列的節點，其餘一律硬錯（[`../../KICKOFF-latex-pilot.md`](../../KICKOFF-latex-pilot.md) §4.2 fail-loud）。
> 盤點對象＝`../../../html/fragments/ch04/sec-4-{1..5}.html`。
> 盤點日：2026-07-26。重跑：`python handout/latex/dialect_inventory.py ch04`。

## 1. 摘要

- **39 種 tag＋class 組合**，其中 **3 項是 ch04 首次出現的差集**（見 §2），其餘沿用 ch03／appB 已凍結的 mapping。
- **數學：inline `\(…\)` ×982、display `\[…\]` ×70**（註解外的活數學）。
- **圖：6 個 `<figure data-fig>` ／ 6 個 SVG panel**（皆單格）。
- 活散文的非 ASCII 6 種（`§ — ’ – “ ”`），NCM 全數有字；**數學區段內零非 ASCII**。

## 2. ch04 的三項差集（本次 rollout 新凍結）

| # | 標記／現象 | 次數 | 處置 | 為什麼是 ch04 才遇到 |
|---|---|--:|---|---|
| D1 | 數學區段內的 HTML entity `&lt;`／`&gt;` | 12／30 | `convert.py` 的 `MATH_ENTITIES` 白名單解碼；表外 entity 硬錯 | HTML 文字節點不能寫裸 `<`，故 fragment 寫 `\(m &lt; M\)` 是**正確**寫法，MathJax 拿到的是解碼後的 `m < M`。數學是逐位元組 pass-through，不解碼的話 LaTeX 收到字面 `&`，被當成 alignment tab 直接編譯失敗。appB／ch01／ch03 的真數學區段內**零 entity**，ch04 是第一個。 |
| D2 | 裸 `<span class="qed">`（非 `qed qed-proof`） | 7 | inline（6，句尾）與 block（1，`env-body` 直接子元素）兩種位置都映到 `\qedmark`；仍要求空元素 | appB 只凍結了 proof 收尾的 `qed qed-proof`。worked-solution 的收尾記號用裸 `qed`，ch04 是第一個帶進來的章。原 `test_plain_qed_span_rejected` 就是為此設的哨兵（註解：「哪天 fragment 加了要硬錯提醒補 mapping」），本輪觸發後改為正面測試。 |
| D3 | `section.env.env-corollary` | 4 | 加進 `ENV_KINDS` → `\begin{envcorollary}` | 模板 [`../../template/calcbook.sty`](../../template/calcbook.sty) §env 家族早已備妥 `envcorollary`（rollout 時預留），只是轉換器白名單還沒放行。 |

## 3. 圖：全書第一個把襯線標籤帶進 LaTeX 的章

ch04 的 Figure 4.5／4.4／4.6 面板上有襯線／數學標籤，用的是 standalone `@font-face` 宣告的
web 版 New Computer Modern。那份 woff2 是 **TrueType-flavored**，所以 headless Chrome 匯出
圖 PDF 時嵌的是 **FontFile2**（非 CFF）。

字形閘（[`../../check_glyphs.py`](../../check_glyphs.py)）原本只驗 CFF、遇到別的一律 FAIL 並指名。
本次 rollout 為它加了 glyf 比對路徑（實測 Chrome 子集器**保留原字型 GID 編號**，故判準與 CFF 路徑
同源：同一 GID 比輪廓）。比對基準是 vendored 的 woff2，見
[`../../template/fonts/webcm/README.md`](../../template/fonts/webcm/README.md)。

> ch01 的 26 張圖沒有襯線文字（其 dist PDF 裡零 WebCM 字型），所以在 ch04 之前沒踩到。

**排除過的兩條路（別再重試）：**

- 讓圖改用 TeX 樹的 `NewCM10-*.otf`（如此嵌出來就是 CFF、現有閘直接可驗）——**不可行**：
  Chrome 拒絕載入該字型。實測原檔、剝掉 FontForge 私有表（`FFTM`／`PfEd`）、再剝 `MATH`、
  再剝 `GSUB`/`GPOS`/`GDEF`、再剝 `post`，五個變體全部 `NetworkError`；同一條管線餵
  `template/fonts/inter/Inter-Regular.otf`（同為 OTTO/CFF）則 OK。拒收點在 CFF 本體或核心表。
- 改用 CFF 版的 web 字型——**不存在**：`web-computer-modern@1.1.0-new-cm-7-0-2` 全套件 45 個檔案
  只有 woff2／css／txt／json／md，**零 OTF／TTF**，且 woff2 檔頭 flavor 欄位是 `\x00\x01\x00\x00`（glyf）。

## 4. 四閘驗收（2026-07-26）

```
[dist] chapter4.tex（1052 段數學 pass-through）
[dist] chapter4.pdf：32 頁、error 0、missing char 0      ← 閘 1
[gate] 完整性閘 PASS：8 處 pdftotext 抽取假象，0 處真落差   ← 閘 3
[gate] 字形閘 PASS：549 個嵌入字形的輪廓全數符合其 CID      ← 閘 4
```

重跑 `make_dist.py ch04` 產出的 `.tex` byte-identical（確定性成立）。

# DIALECT-ch06 — ch06 的方言差集與 LaTeX mapping（rollout 第四個單元）

> 基底＝[`../ch03/DIALECT-ch03.md`](../ch03/DIALECT-ch03.md)（30 列 mapping）＋ [`../appB/DIALECT-appB.md`](../appB/DIALECT-appB.md)（附錄差集）＋ [`../ch01/DIALECT-ch01.md`](../ch01/DIALECT-ch01.md)（27 列）。
> 本檔只記 **ch06 相對於這三者的差集**、圖資產清單、以及本輪對工具的改動。
> 流程權威＝[`../../KICKOFF-latex-pilot.md`](../../KICKOFF-latex-pilot.md) §4.5 四閘；樣式權威＝[`../../template/calcbook.sty`](../../template/calcbook.sty)。
> **狀態（2026-07-26）：四閘全綠、`dist/ch06/` 成品已產出。**

## 1. 盤點結果

`python dialect_inventory.py ch06`：五個 fragment、**33 種 tag+class 組合**（ch01 是 62）、行內數學 657＋display 66（轉換器實測 pass-through **723 段**）、圖 **9 個 `<figure>`／12 個 panel**、表 **0 張**。

**ch06 是目前最單純的單元**：沒有表格、沒有 inline SVG、沒有 `page-break-before`、沒有 `ol.warmup`／`ol.prompt-list`／`ol.sol-list`／`p.ragged`、沒有「`figure` 出現在 `li` 內」。33 種組合中 **32 種**已由既有 mapping 覆蓋，**只有 1 種**是新的。

## 2. ch06 專屬 mapping（本輪新增，僅 1 列）

| # | fragment 標記 | 次數 | LaTeX 語意 | 備註 |
|---|---|--:|---|---|
| 1 | `span.qed`（裸 class，無 `qed-proof`） | 21 | `\qedmark` | worked-solution 的收尾記號。appB 只有 `span.qed.qed-proof`（proof 變體，本章另有 5 個）。**HTML 側兩者都是空心方框，只差框線色**（`.qed::after` 用 `--ink-soft`；`.skin-hs .qed-proof::after` 覆寫為 `--ink`），LaTeX 同映到 `\qedmark`＝amsthm 的 `\qedsymbol`。模板該巨集本來就註明「`span.qed` 記號驅動」，語意槽早已備妥 |

**這一列是被絆線接住的**：`test_convert.py::FailLoud::test_plain_qed_span_rejected` 原本明文斷言裸 `span.qed` 必須硬錯，註解寫著「素 qed（solution 變體）未凍結，哪天 fragment 加了要硬錯提醒補 mapping」。ch06 正是那個「哪天」。絆線已改寫為 `test_other_qed_variant_rejected`（守住「第三種 class 組合仍要硬錯」）＋兩條正向／空元素測試。

**數學巨集對等**：ch06 的 standalone `macros` 表＝`arccsc`／`arcsec`／`arccot`，與 ch01 相同，`calcbook.sty` 早已以 `\providecommand` 提供，**無新增**。（此為 DIALECT-ch01 §2 定下的每章 Gate 0 例行對照。）

## 3. 圖資產（12 panel）

`node export_figs.mjs ../html/standalone/chapter6-print-standalone.html chapters/ch06/figs` → `figs/*.pdf` ＋ `figs/figures.json`（皆 gitignored）。版心實測 566.94px、`liveWidthMm` 150。

- 9 個 `<figure>`；多 panel 者：`riemann-lr-x2`×2（HTML `pair`）、`refinement-rn-x2`×3（HTML `triple`）。
- mm 寬區間 53.80–85.64（最寬 `ftc-trap`、最窄 `semicircle-area`）。

### 3.1 `refinement-rn-x2`：HTML 宣告 `triple`，LaTeX 排成 2＋1（照規則，非缺陷）

`panel_grid()` 的 docstring 明訂：「現有各圖的排法與 HTML 的 `--pair`／`--triple`／`--grid` 恰好一致；**若日後有圖不一致，以本函式的寬度判斷為準（版心放不下就是放不下），並在該章 DIALECT 記一筆**」。ch06 是第一個不一致的案例，本節即該筆紀錄。

- 三格併排需 `3 × 57.41 + 2 × MIN_GAP(2.0) = 176.2mm`，版心可用 `150 − SAFETY(1.0) = 149mm`，**差 27mm，放不下**。
- 依凍結政策**縮間距不縮圖**（縮圖會等比改變圖內標籤字級，DIALECT-ch03 §5 明文禁止），故貪婪填列的結果是 2＋1（第三格置中）。
- 目檢（PDF 第 4 頁）：n=4／n=8 同列、n=16 置中於次列，遞進順序仍照閱讀順序（左→右→換列），caption 緊接其下，無跨頁。**判定為可接受**。
- ch01 的 `limit-same-near-a`×3 之所以能併成一列，是因為它每格只有 42.86mm（`3 × 42.86 + 2 × 6 = 140.6mm`，塞得下）。

## 4. 本輪對工具的改動

| 檔 | 改動 | 為什麼 |
|---|---|---|
| `convert.py` | inline 的 qed 分支由 `classes == ("qed","qed-proof")` 放寬為 `classes in (("qed",), ("qed","qed-proof"))` | §2 的唯一差集。**空元素檢查對兩個變體都保留** |
| `make_dist.py` | `NAMES` 加 `ch06: chapter6`；字形閘多帶第二參數 `chapters/<ch>/figs` | rollout 新章例行；第二參數見下 |
| `check_glyphs.py` | 新增 `figure_font_programs()` 與**圖內字型 pass-through 判準** | 見 §5 |
| `test_convert.py` | 絆線改寫（見 §2）＋ 新增裸 qed 的正向與空元素測試 | 契約已變，測試跟著變。85 passed |

## 5. 字形閘的新判準：圖帶進來的字型（本輪唯一擋稿項，已解）

**症狀**：閘 4 FAIL——`AAAAAA+WebCM-Serif-10-Regular：FontFile2（非 CFF）`，1 個嵌入字型無法驗。

**根因**：`velocity-distance-steps`（Figure 6.3）的軸標是 `t\,(\text{s})` 與 `v\,(\text{m/s})`。MathJax 的 `\text{…}` 走**文字體**的 `@font-face`（New CM 的 WebCM-Serif-10），Chrome 把它嵌成 **CID TrueType**；純數學標籤則走 `mjx-ncm-*` 的 **Type 3**（Type 3 沒有 `/FontFile`，本來就不在閘 4 視野內）。**ch01 全 24 張圖都沒用過 `\text{}`，所以三輪 rollout 都沒撞到**；ch06 是第一例。這是通用缺口，**ch05／ch07 只要圖標籤帶單位就會再撞**。

**為什麼不能照原邏輯驗**：閘 4 的判準是「逐 CID 比對嵌入子集與**原始字型檔**的輪廓」。這個字型按定義沒有本機原始檔（MathJax webfont 走 CDN），而且是 TrueType 不是 CFF。

**為什麼不該直接放行**：`check_glyphs.py` 的 docstring 明寫「silent skip 正是 check_prose.py 的 figure_note_check 記錄過的偽陰性坑，不重蹈」。

**採用的解法——改判 pass-through，而不是豁免**：這類字型改問「**它的字型程式是否與該章某個圖 PDF 裡的逐位元組相同**」。相同即證明 LuaTeX 只是原封轉貼、未經字形名索引重新編碼——而閘 4 要防的因果層（LuaTeX 以字形名索引 → 重複名塌陷 → 輪廓錯位，即 2026-07-17 的 Inter bug）正是發生在「LaTeX 自己嵌字型」那條路上，對 `\includegraphics` 帶進來的字型根本不適用。不同或找不到來源則**照舊 FAIL**。仍逐個列名（印成 `[圖內字型]`），不是 silent skip；圖內文字另有閘 3c 守著。

**實測結果**：`AAAAAA+WebCM-Serif-10-Regular` 與 `figs/velocity-distance-steps.pdf` 內的字型程式**逐位元組相同** → pass-through。回歸：appB 362 字形、ch01 489 字形，兩者輸出與改動前**完全不變**。

## 6. 四閘現況（2026-07-26，全綠）

| 閘 | 結果 |
|---|---|
| 1 編譯 | **PASS**：`chapter6.pdf` **28 頁**、0 error、0 missing character |
| 3 完整性（`check_prose.py`） | **PASS**：11 處 `pdftotext` 抽取假象（逐條確認內容在），**0 處真落差** |
| 3b 表格 | **略過**：本章無 `table.tbl` |
| 3c 圖內文字 | **PASS**：6 條 panel note 全數抵達 PDF（`riemann-lr-x2` 的 Left／Right endpoints、`refinement-rn-x2` 的 n=4／8／16、`accumulation-sliver` 的 "The strip is drawn wide — not to scale."） |
| 4 字形（`check_glyphs.py`） | **PASS**：**504** 個嵌入字形的輪廓全數符合其 CID；另 **1** 個圖內字型逐位元組 pass-through（見 §5） |

**成品**：`dist/ch06/` ＝ `chapter6.tex` ＋ `chapter6.pdf`（恰兩檔）。

## 7. 目檢紀錄

- 第 3 頁 Figure 6.1（pair，2×66.67mm 併排）、第 4 頁 Figure 6.2（triple → 2＋1，見 §3.1）、第 7 頁 Figure 6.3（含 `\text{}` 標籤）皆正常。
- Figure 6.3 的 `v (m/s)` 標籤與 y 軸箭頭僅相鄰不重疊（600 dpi 放大確認）。
- 本輪散文改動（[`../../../html/_audit/REVIEW-ch06-plain-applied.html`](../../../html/_audit/REVIEW-ch06-plain-applied.html)）在 PDF 上落地正確，例如 §6.1 收尾的 “The next section names this common limit the *definite integral* and introduces its symbol.” 與 §6.2 開場的 “Here we name the common limit the *definite integral* and introduce its symbol.”

# DIALECT-ch06 — ch06 的方言差集與 LaTeX mapping（rollout 第四個單元）

> 基底＝[`../ch03/DIALECT-ch03.md`](../ch03/DIALECT-ch03.md)（30 列 mapping）＋ [`../appB/DIALECT-appB.md`](../appB/DIALECT-appB.md)（附錄差集）＋ [`../ch01/DIALECT-ch01.md`](../ch01/DIALECT-ch01.md)（27 列）。
> 本檔只記 **ch06 相對於這三者的差集**、圖資產清單、以及本輪對工具的改動。
> 流程權威＝[`../../KICKOFF-latex-pilot.md`](../../KICKOFF-latex-pilot.md) §4.5 四閘；樣式權威＝[`../../template/calcbook.sty`](../../template/calcbook.sty)。
> **狀態（2026-07-26）：四閘全綠、`dist/ch06/` 成品已產出。**
>
> ⚠ **本檔在 rollout 分支上寫成，合併 main 後有實質修訂。** ch06 的工作在 `handout/plain-ch06` 上進行時，main 同日並行完成了 ch02／ch03／ch04／ch05 四章 rollout；合併後發現**本輪原本以為的兩項「新增」其實 main 都已做過，且做得更好**——裸 `span.qed` 的 mapping（ch04 差集已補）與圖內字型的驗證（ch02 立具名白名單、ch04 vendored woff2 並加 glyf 比對路徑）。**§2／§4／§5 已依合併後的事實重寫**；本輪對工具的實際淨改動只剩 `NAMES` 一列。教訓＝PIPELINE「通用紀律」的「**開長閘前先從 main 更新**」（該條正是 ch04 實證後加的），本輪未照做。

## 1. 盤點結果

`python dialect_inventory.py ch06`：五個 fragment、**33 種 tag+class 組合**（ch01 是 62）、行內數學 657＋display 66（轉換器實測 pass-through **723 段**）、圖 **9 個 `<figure>`／12 個 panel**、表 **0 張**。

**ch06 是目前最單純的單元**：沒有表格、沒有 inline SVG、沒有 `page-break-before`、沒有 `ol.warmup`／`ol.prompt-list`／`ol.sol-list`／`p.ragged`、沒有「`figure` 出現在 `li` 內」。33 種組合**全部**已由既有 mapping 覆蓋（見 §2）。

## 2. ch06 專屬 mapping：**0 列**

合併 main 後，ch06 的 33 種 tag+class 組合**全部**已被既有 mapping 覆蓋，本章沒有任何專屬差集。

分支上原本記為「唯一新增」的裸 `span.qed`（21 處，worked-solution 收尾記號），**main 的 ch04 rollout 同日已經補上**（`convert.py` 的 `k.classes in (("qed","qed-proof"), ("qed",))`），而且比分支版完整——main 另外處理了 **block-level** 的 `span.qed`（`env-body` 直接掛一個 qed span，非 `<p>` 句尾），分支版只做了 inline。故合併時 `convert.py`／`test_convert.py` 整檔取 main。

兩邊是各自獨立撞到同一條絆線的：`test_convert.py::FailLoud::test_plain_qed_span_rejected` 原本明文斷言裸 `span.qed` 必須硬錯，註解寫著「哪天 fragment 加了要硬錯提醒補 mapping」。ch04 與 ch06 在同一天各自成為那個「哪天」，兩邊的修法與註解幾乎逐字相同。**這條絆線的設計是有效的**。

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

## 4. 本輪對工具的實際改動：`NAMES` 一列

| 檔 | 改動 | 為什麼 |
|---|---|---|
| `make_dist.py` | `NAMES` 加 `ch06: chapter6` | rollout 新章例行。**這是本輪對工具的全部淨改動** |

分支上另外改過 `convert.py`／`test_convert.py`／`check_glyphs.py`／`.gitignore`，合併 main 時**四者全部整檔取 main**——見 §2（qed mapping）與 §5（字形閘）。

## 5. 圖帶進來的字型：分支上撞到、但 main 早已解掉（且解得更好）

**分支上的症狀**：閘 4 FAIL——`AAAAAA+WebCM-Serif-10-Regular：FontFile2（非 CFF）`，1 個嵌入字型無法驗。

**根因**：`velocity-distance-steps`（Figure 6.3）的軸標是 `t\,(	ext{s})` 與 `v\,(	ext{m/s})`。MathJax 的 `	ext{…}` 走**文字體**的 `@font-face`（New CM 的 WebCM-Serif-10），Chrome 把它嵌成 **CID TrueType**；純數學標籤則走 `mjx-ncm-*` 的 **Type 3**（Type 3 沒有 `/FontFile`，本來就不在閘 4 視野內）。ch01 全 24 張圖都沒用過 `	ext{}`，所以早期 rollout 沒撞到。

**main 早已解掉，而且是兩層**（皆 2026-07-26，與本輪並行）：

1. **ch02 rollout** 立 `FIG_IMPORTED_OK` 具名白名單——裡面就明確列著 `WebCM-Serif-10-`。當天即證明這條抓得到真缺陷：Figure 2.7 的 `√` 因 Inter 缺 U+221A 被 Chrome 退回 `MicrosoftJhengHeiUI`（Windows 系統 CJK 字型），字形本身沒錯、**退錯字型**才是缺陷。
2. **ch04 rollout** 把 WebCM 的原始 woff2 vendored 進 `template/fonts/webcm/`，並加**glyf（TrueType）逐 GID 輪廓比對**路徑。白名單自此降為 fallback——**能驗的一定要驗**。

**分支版的做法為何該丟**：分支上改判「字型程式是否與該章某個圖 PDF 逐位元組相同」。那只證明 LuaTeX 沒有重新編碼，**完全不管 Chrome 一開始有沒有挑對字型**——上面 ch02 的 `√` 退成 CJK 字型那個真缺陷，在分支版判準下會**靜默通過**（它確實是從圖 PDF 原封帶進來的）。main 的具名白名單擋得住，分支版擋不住。故合併時 `check_glyphs.py` 整檔取 main，`make_dist.py` 的字形閘呼叫也還原成單參數形式。

**合併後實測**：ch06 的 WebCM 走 main 的 glyf 路徑**真的比對了輪廓**——字形閘由「504 驗過 ＋ 1 未驗 pass-through」變成 **507 個全數驗過、零 fallback**。

## 6. 四閘現況（2026-07-26 合併 main 後重跑，全綠）

| 閘 | 結果 |
|---|---|
| 1 編譯 | **PASS**：`chapter6.pdf` **28 頁**、0 error、0 missing character |
| 3 完整性（`check_prose.py`） | **PASS**：9 處 `pdftotext` 抽取假象（逐條確認內容在），**0 處真落差**（分支上為 11 處；main 的抽取假象偵測更準） |
| 3b 表格 | **略過**：本章無 `table.tbl` |
| 3c 圖內文字 | **PASS**：6 條 panel note 全數抵達 PDF（`riemann-lr-x2` 的 Left／Right endpoints、`refinement-rn-x2` 的 n=4／8／16、`accumulation-sliver` 的 "The strip is drawn wide — not to scale."） |
| 4 字形（`check_glyphs.py`） | **PASS**：**507** 個嵌入字形的輪廓全數符合其 CID，**零未驗、零 fallback**（含圖內的 WebCM，走 main 的 glyf 路徑；見 §5） |

**成品**：`dist/ch06/` ＝ `chapter6.tex` ＋ `chapter6.pdf`（恰兩檔）。

## 7. 目檢紀錄

- 第 3 頁 Figure 6.1（pair，2×66.67mm 併排）、第 4 頁 Figure 6.2（triple → 2＋1，見 §3.1）、第 7 頁 Figure 6.3（含 `\text{}` 標籤）皆正常。
- Figure 6.3 的 `v (m/s)` 標籤與 y 軸箭頭僅相鄰不重疊（600 dpi 放大確認）。
- 本輪散文改動（[`../../../html/_audit/REVIEW-ch06-plain-applied.html`](../../../html/_audit/REVIEW-ch06-plain-applied.html)）在 PDF 上落地正確，例如 §6.1 收尾的 “The next section names this common limit the *definite integral* and introduces its symbol.” 與 §6.2 開場的 “Here we name the common limit the *definite integral* and introduce its symbol.”

# DIALECT-ch01 — ch01 的方言差集與 LaTeX mapping（rollout 第三個單元）

> 基底＝[`../ch03/DIALECT-ch03.md`](../ch03/DIALECT-ch03.md)（30 列 mapping）＋ [`../appB/DIALECT-appB.md`](../appB/DIALECT-appB.md)（附錄差集）。
> 本檔只記 **ch01 相對於這兩者的差集**、圖資產清單、以及本輪對工具與模板的改動。
> 流程權威＝[`../../KICKOFF-latex-pilot.md`](../../KICKOFF-latex-pilot.md) §4.5 四閘；樣式權威＝[`../../template/calcbook.sty`](../../template/calcbook.sty)（詞彙凍結表見 [`../../template/M-B1-DECISIONS.md`](../../template/M-B1-DECISIONS.md) §2）。
> **狀態（2026-07-25）：閘 1（編譯）＋閘 3（完整性）已過；閘 3b（圖內文字）有 1 個真缺陷 → 尚未產 dist 成品。** 見 §5。

## 1. 盤點結果

`python dialect_inventory.py ch01`：六個 fragment、**62 種 tag+class 組合**、行內數學 1001＋display 119（轉換器實測 pass-through **1120 段**）、圖 **25 個 `<figure>`／33 個 panel**、表 **2 張**。
其中 **35 種**已由 ch03／appB 的 mapping 覆蓋，**27 種**是 ch01 專屬（下表；SVG 子元素合併為一列）。

## 2. ch01 專屬 mapping（本輪新增）

| # | fragment 標記 | 次數 | LaTeX 語意 | 備註 |
|---|---|--:|---|---|
| 1 | `div.tbl-wrap` > `table.tbl`（`thead`／`tbody`／`tr`／`th`／`td`／`td.rowlab`） | 2 | **`\begin{datatable}{<colspec>}`**（booktabs 三線表、置中、`\small`） | kickoff §4.2 早已列 `table.tbl → booktabs`，ch03 用不到故未實作。`colspec`＝首欄 `r`（對映 `.rowlab{text-align:right}`）＋其餘 `c`；`thead`／`tbody` 之間射 `\midrule` |
| 2 | `figure.figure[id]` > `div.figure-art` > `svg.fig-svg`（＋`defs`／`marker`／`path`／`ellipse`／`circle`／`text.*`） | 1 | `figureblock` ＋ `\includegraphics`，**圖鍵改用 `id`** | 全書唯一寫在 fragment 裡的 inline SVG（Figure 1.2 `#fig-map`）。整塊由 `export_figs.mjs` 匯成向量 PDF，**convert.py 不轉譯 SVG 內容**；parser 的 style 白名單對 `div.figure-art` 子樹豁免（該子樹的 presentation 屬性不在方言管轄內） |
| 3 | `figure.figure` 出現在 `li` 內 | 2 | 項目內就地 `figureblock` | ch01 §1.2 Example 1.9／1.12 的解法把 Figure 1.6／1.10 放進清單項目 → `li` 內容改為「inline 段落 ＋ Figure 交錯」（`Builder.li_content`／`LatexEmitter.item_text`），純 inline 項目的輸出不變 |
| 4 | `ol.warmup` | 1 | **`warmuplist`**（`label=(\alph*)`） | 對映 HTML `counter(wu, lower-alpha)` 的 `(a)(b)` |
| 5 | `ol.prompt-list` | 7 | `enumerate` | HTML 無專屬 CSS ⇒ 預設十進位 `ol` |
| 6 | `ol.sol-list` | 7 | `enumerate` | **同名 class 兩種標記**：appB 是 `ul.sol-list`（bullet ⇒ `sollist`），ch01 是 `ol`（十進位 ⇒ `enumerate`）。emitter 依 `ordered` 分流 |
| 7 | `p.ragged` | 2 | **`raggedpara`**（`\raggedright`） | 對映 `.ragged{text-align:left}`（HTML 對窄 measure 的讓步；ch01 Caution 1.5） |
| 8 | `h3.page-break-before.subsec-head` | 1 | `\pagebreakbefore` ＋ `\subsechead` | `page-break-before` 從此可與 `h3`／`section.env` 併用（模板指令 2026-07-17 已有） |
| 9 | `section.env.env-theorem.page-break-before` | 1 | `\pagebreakbefore` ＋ `envtheorem` | 同上；env 的 class 檢查放寬為「恰為 env＋env-<kind>，可加 page-break-before」 |

**數學巨集對等（新增，非 tag mapping）**：HTML 側由各 standalone 的 `window.MathJax.tex.macros` 提供 `\arccsc`／`\arcsec`／`\arccot`；數學區段逐位元組照抄，故模板必須提供同名巨集，否則 `Undefined control sequence`（ch01 §1.2 三個反三角餘函數）。已在 `calcbook.sty` 以 `\providecommand{…}{\operatorname{…}}` 補上。**此後每章 Gate 0 都要對照該章 standalone 的 `macros` 表**。

## 3. 圖資產（33 panel，`export_figs.mjs` 全數匯出）

`node export_figs.mjs ../html/standalone/chapter1-print-standalone.html chapters/ch01/figs` → `figs/*.pdf` ＋ `figs/figures.json`（皆 gitignored，`*.pdf`）。版心實測 566.94px、`liveWidthMm` 150。

- 25 個 `<figure>`；多 panel 者：`hlt`×2、`limit-same-near-a`×3、`recip-x-vs-x2`×2、`one-sided-infinite`×4、`epsilon-delta-dynamic`×2。
- mm 寬區間 42.86–132.82（最寬 `sine-not-1to1`、最窄 `limit-same-near-a-*`）。
- **exporter 的選擇器擴充**：原本只掃 `figure.figure[data-fig]`，現為 `figure.figure[data-fig], figure.figure[id]`，圖鍵 `data-fig ?? id` —— 否則 Figure 1.2 不會被匯出（它沒有 `data-fig`）。

## 4. 本輪對工具與模板的改動（含一個潛伏 bug 的修正）

| 檔 | 改動 | 為什麼 |
|---|---|---|
| `convert.py` | §2 的九條 mapping；`figure` 的 `id` 圖鍵；parser style 白名單對 `figure-art` 子樹豁免；`li` 混合內容 | ch01 差集 |
| `convert.py` | **`\includegraphics{<ch>/<stem>}` → `{<ch>/figs/<stem>}`** | **潛伏 bug**：舊形式沿用 2026-07-17 目錄重整**前**的 `figs/<ch>/` 佈局；資產現在在 `chapters/<ch>/figs/`。appB 無圖、ch03 從未 dist 過，故一直沒爆。連帶更新 `test_convert.py` 三條 golden |
| `make_dist.py` | `NAMES` 加 `ch01: chapter1`；HEADER 加 `\graphicspath{{../../chapters/}}` | graphicspath 是 docstring 自己標的 TODO（「首個有圖章 rollout 時在此補」），本輪即該場合 |
| `calcbook.sty` | `booktabs`＋`datatable`、`warmuplist`、`raggedpara`、三個反三角巨集 | §2 對映所需的語意槽 |
| `check_prose.py` | 主閘剝除 `div.figure-art`（inline SVG）與 `div.tbl-wrap`（表格）；新增 **`table_check()`** 以無序判準守表格內容 | 兩者都是**假紅**：圖內文字本來就不在 PDF 文字層（`data-fig` 圖的標籤同理，從來不在期望串裡）；表格則因 `pdftotext` 對窄 tabular 是**欄優先**抽取（實測抽成「0.9 0.5263 / 0.99 0.5025 …」），與 fragment 的列優先詞流不可能依序對上（實測誤報 11 個詞掉字，還讓後續比對錯位）。拆閘後兩邊都保有力量：主閘守散文順序、`table_check` 守表格不掉 |

## 5. 四閘現況（2026-07-25）

| 閘 | 結果 |
|---|---|
| 閘 1 編譯（log） | **PASS**：44 頁、0 error、0 missing character |
| 閘 3 完整性（`check_prose.py`） | **PASS**：0 處真落差（6 處 `pdftotext` 抽取假象已逐條確認內容在） |
| 閘 3b 圖內文字（`figure_note_check`） | **FAIL — 1 個真缺陷**：`recip-x-vs-x2` 兩格的 panel note `y = 1/x²`／`y = 1/x` 沒抵達 PDF。已獨立驗證非比對假象：`figs/recip-x-vs-x2-1.pdf` 的文字層只有 1 個字元（對照 `hlt-1.pdf` 75、`precise-limit.pdf` 56）。**診斷**：該 panel 的匯出 page box（202px）比 panel 本身（261.97px）**窄**，note 被裁掉——`export_figs.mjs` 的墨水框聯集（svg ∪ `.fig-lbl` ∪ `.fig-note`）在 **pair layout** 下沒把 note 算進去。其餘 32 panel 的 page box 都 ≥ panel。 |
| 閘 4 字形（`check_glyphs.py`） | 未執行（閘 3b 先擋） |

**因此 `dist/ch01/` 未產出**（`make_dist.py` 契約：三閘任一不過就不產成品；本輪產生的中間 `.tex`／`.pdf` 已刪）。下一步＝修 `export_figs.mjs` 的 pair-layout 墨水框，重匯 `recip-x-vs-x2`，再跑 `python make_dist.py ch01` 收閘 3b／閘 4。

## 6. 已知極限（誠實記錄）

- `test_convert.py` 有 **2 個先前就紅的 appB 測試**（`mapped` 718→722、`math` 566→571），與 ch01 無關：appB 的 fragment 在 2026-07-25 的平實化兩輪被改過，golden 數字沒同步更新。已用 `git stash` 驗證：把本輪改動全部收起後仍紅。**本輪未動它們**（不是我的輪次的債，且更新 golden 需確認那兩輪的改動意圖）。
- `table_check()` 是無序判準 ⇒ 抓不到「表格值排錯位」。表格數值另有數學 pass-through 與人眼閘（閘 4／gate-2 人眼）覆蓋。
- ch01 尚未做**人眼閘**（kickoff §4.5 閘 2）與書級組裝；HTML 側 53 頁 vs LaTeX 44 頁的密度差尚未逐頁比對。

---
*本檔 2026-07-25 建立（ch01 rollout 第一輪）。mapping 變更一律更新本檔；判準變更改 kickoff 或模板決策紀錄，不在本檔另立規則。*

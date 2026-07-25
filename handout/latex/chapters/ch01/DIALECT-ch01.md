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
| 閘 1 編譯（log） | **PASS**：44 頁、0 error、0 missing character、0 Overfull hbox |
| 閘 3 完整性（`check_prose.py`） | **PASS**：0 處真落差（6 處 `pdftotext` 抽取假象已逐條確認內容在） |
| 閘 3b 表格（`table_check`，本輪新增） | **PASS**：18 個表格格子全數抵達 PDF |
| 閘 3c 圖內文字（`figure_note_check`） | **PASS**：13 條 panel note 全數抵達 PDF |
| 閘 4 字形（`check_glyphs.py`） | **PASS**：489 個嵌入字形的輪廓全數符合其 CID |

**`dist/ch01/` 已產出**＝恰兩檔（`chapter1.tex` 84.6KB ＋ `chapter1.pdf` 1.79MB，44 頁）。

### 5.1 為了收這兩道閘修掉的兩個真缺陷

1. **panel 內的 `.fig-note` 被裁掉（閘 3c 抓到）。** 症狀：`recip-x-vs-x2` 兩格的 `y = 1/x²`／`y = 1/x` 沒抵達 PDF，該 panel 的 PDF 文字層只有 1 個字元。**真因不是墨水框**——墨水框（202×188px＝svg ∪ note）其實正確；問題在 wrapper 只把 **panel** 重申為實測尺寸，**沒重申 svg 自己的尺寸**。活頁面用 per-figure 自訂屬性（`hydrateFigures` 把 `--fig-N-M` 寫成 `<figure>` 的 **inline style**）把該 svg 壓到 `max-width:200px`（inline 卻寫 `width:244px`、viewBox 244×196）；wrapper 複製祖先鏈時**只保留 class／data-fig**，那個變數不在，於是 svg 以 244px 寬重繪、高約多 35px，把 note 推到 page box 之外。**修法**：clone 的 svg 加 `.fx-svg`，並以實測 `width`／`height` 釘死（與既有「panel 重申實測尺寸」同一原則）。修後兩格文字層 8／6 字元、視覺確認 note 回來且圖形回到 1:1。
2. **`fig-map` 嵌入無法驗的 Times New Roman（閘 4 抓到）。** 字形閘只驗 CFF 輪廓，`DAAAAA+TimesNewRomanPSMT`（CID TrueType）判「無法驗」而擋稿。**真因**：Figure 1.2 的標籤 `f⁻¹` 用了 **U+207B／U+00B9**（全書活散文各僅此一處），而圖內標籤實際走的是 `--ui`＝**Inter**，Inter 沒有這兩個字 → Chrome 逐字 fallback 到系統 Times。**注意這代表 HTML 預覽本來也是用系統字型在畫這兩個字**。**修法（改源頭）**：`f⁻¹` → `f<tspan dy="-5" font-size="0.72em">-1</tspan>`（`handout/html/fragments/ch01/sec-1-1.html:224`），視覺等價、字元全在 Inter 字集內。修後 `fig-map.pdf` 只含 Inter 子集，全 33 panel 無任何 Times。
   - 途中試過、**已撤除**的做法（留紀錄免得再走）：用 `kpsewhich` 找模板的 NewCM OTF、注入 `@font-face` 給 wrapper。(a) `file://` 的字型抓取被 Chrome 當跨 opaque origin 擋掉（加 `--allow-file-access-from-files` 仍 `document.fonts.check==false`）；(b) 改 data: URI 後 face 狀態仍 `error`；(c) 而且方向本來就錯——那些標籤是 Inter、不是 serif。三次實測後改回源頭修。

### 5.2 多 panel 圖的 grid 版面（2026-07-26 已修）

`convert.py` 的 figure emitter 對多 panel 圖是 `\hspace{6mm}` 併排，沒有 grid／minipage 版面（DIALECT-ch03 §3 早列 `figure-art--triple`／`--grid → minipage` 為「ch03 用不到、rollout 逐章補」）。ch01 實測：

| 圖 | panel | 併排寬 | 判定 |
|---|--:|--:|---|
| `hlt`（Figure 1.1） | 2 × 72.35mm | **150.7mm** | 超出 150mm 版心 0.7mm → 第二格換行，**p.3／p.4 被拆開、p.4 幾乎空白** |
| `one-sided-infinite`（Figure 1.17） | 4 × 64.03mm | **274.1mm** | 遠超 → 自動折行成 2＋2 |
| `limit-same-near-a` | 3 × 42.86mm | 140.6mm | 放得下 |
| `epsilon-delta-dynamic` | 2 × 64.03mm | 134.1mm | 放得下 |
| `recip-x-vs-x2` | 2 × 53.45mm | 112.9mm | 放得下 |

LaTeX **不報 Overfull**（`figureblock` 的 center 允許在 `\hspace` 處斷行），所以閘 1 全綠也看不到——這是人眼閘才抓得到的一類。

**修法（`LatexEmitter.panel_grid`）：寬度驅動的貪婪填列。**

1. 一列裝得下就繼續裝，裝不下換列；判斷時用 `MIN_GAP_MM = 2mm`（不是預設的 6mm），好讓「只差一點就滿」的列留在同一列。
2. 該列的實際間距 `gap = min(6mm, 剩餘空間/(n−1))`——**縮間距、不縮圖**。縮圖會等比改變圖內標籤字級，是 DIALECT-ch03 §5 明文禁止的。
3. **版心安全邊 `SAFETY_MM = 1mm`**：一列**剛好等於** 150mm 時 LaTeX 仍會折行（需嚴格小於，且 mm→pt 有捨入、圖檔另有 side bearing）。實測 Figure 1.1 排到 150.00mm 仍被折成兩列，扣掉 1mm 後（間距 4.3mm、列寬 149.0mm）才真正併成一列。
4. **多列圖整塊（含圖說）包進 `minipage` 禁止分頁**：模板 `figureblock` 的 `\cb@needspace{6\baselineskip}` 是按單列圖估的，兩列圖高一倍——實測 Figure 1.17 的 2×2 落在 p.24 而圖說被推到 p.25（孤立圖說）。單列圖仍走原路徑。

**單 panel 圖與「本來就放得下的整列」輸出逐字元不變**，故 ch03 的 golden 不動（`remainder-tangent` 2×65.62＋6＝137.2mm 仍是一列、間距仍 6mm；`test_convert.py` 的 figure 相關 5 項全綠）。

修後實測（`convert.py ch01` → `make_dist.py ch01`）：

| 圖 | 排法 | 間距 | 最寬列 | 版面 |
|---|---|--:|--:|---|
| `hlt`（Figure 1.1） | 1 列 × 2 格 | 4.3mm | 149.0mm | 兩格＋兩個 note＋圖說同在 p.3 |
| `limit-same-near-a`（1.12） | 1 列 × 3 格 | 6mm | 140.6mm | 不變 |
| `recip-x-vs-x2`（1.16） | 1 列 × 2 格 | 6mm | 112.9mm | 不變 |
| `one-sided-infinite`（1.17） | **2 列 × 2 格** | 6mm | 134.1mm | 四格＋四個 note＋圖說同在 p.25 |
| `epsilon-delta-dynamic`（1.25） | 1 列 × 2 格 | 6mm | 134.1mm | 不變 |

各圖的排法與 HTML 的 `figure-art--pair`／`--triple`／`--grid` 恰好一致（pair→1列2格、triple→1列3格、grid→2列2格）。四閘仍全綠、0 Overfull hbox、43→44 頁（Figure 1.17 改為不可分頁後多佔一頁，換掉的是原本被拆圖與孤立圖說）。

## 6. 已知極限（誠實記錄）

- `test_convert.py` 有 **2 個先前就紅的 appB 測試**（`mapped` 718→722、`math` 566→571），與 ch01 無關：appB 的 fragment 在 2026-07-25 的平實化兩輪被改過，golden 數字沒同步更新。已用 `git stash` 驗證：把本輪改動全部收起後仍紅。**本輪未動它們**（不是我的輪次的債，且更新 golden 需確認那兩輪的改動意圖）。
- `table_check()` 是無序判準 ⇒ 抓不到「表格值排錯位」。表格數值另有數學 pass-through 與人眼閘（閘 4／gate-2 人眼）覆蓋。
- ch01 尚未做**人眼閘**（kickoff §4.5 閘 2）與書級組裝；HTML 側 53 頁 vs LaTeX 44 頁的密度差尚未逐頁比對。

---
*本檔 2026-07-25 建立（ch01 rollout 第一輪）。mapping 變更一律更新本檔；判準變更改 kickoff 或模板決策紀錄，不在本檔另立規則。*

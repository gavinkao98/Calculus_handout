# DIALECT-ch02 — ch02 的方言差集與 LaTeX mapping（rollout 第四個單元）

> 基底＝[`../ch03/DIALECT-ch03.md`](../ch03/DIALECT-ch03.md)（30 列 mapping）＋ [`../appB/DIALECT-appB.md`](../appB/DIALECT-appB.md)（附錄差集）＋ [`../ch01/DIALECT-ch01.md`](../ch01/DIALECT-ch01.md)（27 列 ch01 專屬）。
> 本檔只記 **ch02 相對於這三者的差集**、圖資產清單、以及本輪對工具與內容的改動。
> 流程權威＝[`../../KICKOFF-latex-pilot.md`](../../KICKOFF-latex-pilot.md) §4.5 四閘；樣式權威＝[`../../template/calcbook.sty`](../../template/calcbook.sty)。
> **狀態（2026-07-26）：五閘全過（編譯／版面／完整性／字形／人眼）＋轉換器測試，`dist/ch02/` 已產出（`chapter2.pdf` 35 頁＋自足 `chapter2.tex`）；§6 的兩項數學待辦亦已結清。****ch02 於本線收尾完成。** 見 §5、§6。

## 1. 盤點結果

`python dialect_inventory.py ch02`：五個 fragment、**50 種 tag+class 組合**、行內數學 747＋display 89（轉換器實測 pass-through **836 段**，恰為 747+89）、圖 **10 個 `<figure>`／12 個 panel**、表 **1 張**。

**差集只有一種**——49 種已由 ch03／appB／ch01 的 mapping 覆蓋，ch02 專屬僅下表第 1 列。這是 rollout 至今差集最小的一章（ch01 是 27 種），符合預期：ch01 那輪已把表格、inline SVG、chapter opener 這些重型結構打通。

**MathJax 巨集對照**（ch01 DIALECT 立的規矩：每章 Gate 0 對照該章 standalone 的 `macros` 表）：ch02 為 `arccsc`／`arcsec`／`arccot`，與 ch01 相同，`calcbook.sty` 已有，**無新增**。

## 2. ch02 專屬 mapping（本輪新增）

| # | fragment 標記 | 次數 | LaTeX 語意 | 備註 |
|---|---|--:|---|---|
| 1 | `section.env.env-corollary` | 1 | **`envcorollary`** | §2.4 Corollary 2.1（多項式逐項微分）。**模板早已有 `envcorollary`**（`calcbook.sty` 註解寫明「env 家族（10 類，含 rollout 的 theorem/corollary）」）——缺的只是 `convert.py` 的 `ENV_KINDS` 白名單漏列，補一個字串即可。這是「模板先行」的設計在 rollout 時真的省到工的例子 |

**沒有新增的**（原以為會有，實測已覆蓋）：`div.tbl-wrap > table.tbl`（ch01 #1 的 `datatable`）、`figure.figure[id] > div.figure-art > svg.fig-svg`（ch01 #2 的 `id` 圖鍵＋style 白名單豁免）、`ol.steps`（appB）、`p.informal`／`p.lead`／`p.para-head`／`header.chapter-head`／`h1.ch-title`／`div.ch-kicker`（ch01 chapter opener）。
ch02 的兩個 inline SVG 帶了 ch01 沒有的子元素（`rect`／`line`／`tspan`），**不需 mapping**——`div.figure-art` 子樹整塊由 `export_figs.mjs` 匯成向量 PDF，convert.py 不轉譯 SVG 內容。

## 3. 圖資產（12 panel，`export_figs.mjs` 全數匯出）

`node export_figs.mjs ../html/standalone/chapter2-print-standalone.html chapters/ch02/figs` → `figs/*.pdf` ＋ `figs/figures.json`（皆 gitignored）。版心實測 566.94px。

- 10 個 `<figure>`；多 panel 者：`f-and-fprime`×2、`quotient-example-graph`×2。
- **inline SVG 兩個**（全書第二、三個，前一個是 ch01 Figure 1.2）：`fig-diff-cont`（Figure 2.7 可微⊂連續的包含關係圖）、`fig-product-area`（Figure 2.9 乘法法則的矩形面積模型）。兩者都靠 exporter 的 `figure.figure[id]` 選擇器（ch01 那輪擴充的）匯出。
- mm 寬區間 87.84–122.24（最寬 `secant-to-tangent`、最窄 `fig-product-area`）。

> **⚠️ 單張重匯會覆蓋整份 manifest。**`node export_figs.mjs <html> <outDir> <figId>` 只寫該張 PDF，但 `figures.json` 會被重寫成**只含那一張**，接著 `make_dist.py` 會在別張圖上硬錯（`figure data-fig="…" 在 figures.json 找不到`）。改完單張圖仍要**跑一次全量匯出**。本輪實地踩到，記於此。

## 4. 本輪修掉的真缺陷：Figure 2.7 的 `√` 被退回系統 CJK 字型

- **病灶**：`sec-2-3.html` 的 Figure 2.7 內嵌 SVG，標籤 `x², √x, eˣ` 走 `.fig-svg text { font-family: var(--ui) }`＝Inter。**Inter 沒有 U+221A（`√`）**，瀏覽器於是逐字退回系統字型——Windows 實測退到 **Microsoft JhengHei UI**（正黑體 UI）。
- **後果**：① 那個根號的字面不是本書任何一套字型，與相鄰字形不搭；② **換機器會變**（沒裝正黑體的機器會退到別的字），匯出的向量 PDF 因此不可重現；③ 該 CJK 子集以 TrueType 嵌進成品 PDF，字形閘無法驗。
- **怎麼發現的**：**只有字形閘看得到**。閘 1 沒有 missing character（字有印出來）、閘 3 走 `pdftotext` 讀 ToUnicode 文字層（`√` 一字不差）。這正是 KICKOFF §4.5 立閘 4 時說的「文字層全對、印出來是別的字」那個維度——這次是「印出來是對的字、但來自不該來的字型」。
- **修法**：該 `<text>` 加 `style="font-family:var(--serif)"`，讓數學例示清單走本書正文數學同一套 NCM（`--serif` 有 `√`）。原文一字未改，只換字族；`div.figure-art` 子樹本來就豁免於 parser 的 style 白名單（ch01 mapping #2），不需改 convert.py。
- **回歸**：重匯後 `fig-diff-cont.pdf` 的字型由 `Inter-Medium`／`Inter`／**`MicrosoftJhengHeiUIRegular`** 變成 `Inter-Medium`／`Inter`／**`WebCM-Serif-10-Italic`**，CJK 字型消失。

## 5. 四閘現況（2026-07-26）

| 閘 | 結果 |
|---|---|
| 閘 1 編譯（log） | **PASS**：**35 頁**、0 error、0 missing character |
| 閘 2 版面（log，人工） | **PASS**：Overfull \hbox 0、Underfull \hbox 0、Overfull \vbox 0（2026-07-26 補驗——首次交付時漏記此閘） |
| 閘 3 完整性（`check_prose.py`） | **PASS**：fragment 散文 7944 詞 vs PDF 12020 詞，**0 處真落差**（9 處 `pdftotext` 抽取假象已逐條確認內容在） |
| 閘 3b 表格（`table_check`） | **PASS**：1 個表格詞全數抵達 PDF（Example 2.4 的割線斜率表） |
| 閘 3c 圖內文字（`figure_note_check`） | n/a：ch02 無 panel note |
| 閘 4 字形（`check_glyphs.py`） | **PASS**：**467 個嵌入字形的輪廓全數符合其 CID**（NCM／Inter 共 12 個子集）；另有 8 個圖匯入子集在 `FIG_IMPORTED_OK` 白名單內——判準的沿革與理由見 §5.1／§5.2 |
| 轉換器測試 | **PASS**：`pytest test_convert.py` 83/83 |
| **閘 5 人眼（KICKOFF §4.5）** | **✅ PASS**（2026-07-26 使用者過目 `dist/ch02/chapter2.pdf` 35 頁後回報通過）。本質需人判斷，機器側只做到結構性驗證：分頁 45→45 頁不變（HTML 側；兩處 8px 溢出 p.13／p.39 在平實化前即存在）、PDF 35 頁 0 error、10 張圖全 render、MathJax 908 容器 0 個未渲染 |

`dist/ch02/` ＝恰兩檔（`chapter2.tex` 76.4KB ＋ `chapter2.pdf` 1.40MB，35 頁）。

### 5.1 閘 4 一度卡住的原因：圖裡的 `WebCM Serif 10` 沒有本機原始檔

- 無法驗的 8 個全是 **`WebCM-Serif-10-Regular`×7 ＋ `WebCM-Serif-10-Italic`×1**，型別 `CID TrueType`（`FontFile2`）。
- 來源是 **`buildPlot` 的 HTML 標籤層**：standalone 的 `.paper .fig-lyr { font-family: var(--serif) }` 讓圖上的文字標註走本書襯線；`--serif` 的第一順位 `"New Computer Modern"` 由 `@font-face` 從 **jsdelivr CDN** 載入（`web-computer-modern@1.1.0-new-cm-7-0-2`）。Chrome 匯出圖時把該 webfont 以 TrueType 子集嵌進去。**這是設計如此、不是缺陷**——圖上文字與正文用同一個字體家族才對。
- `check_glyphs.py` 驗不了的原因有二，缺一不可：① 它只讀 CFF（`FontFile3`／`CIDFontType0C`）；② 它比對的原始檔靠 vendored `template/fonts/inter/` 或 `kpsewhich`，而 **WebCM woff2 兩處都沒有**（在 CDN 上）。
- **為什麼 ch01 沒踩到**：ch01 圖上的標籤全是 MathJax 產物（`mjx-ncm-*`）與 Inter，Chrome 都輸出成 **Type 3** 字型（無 `/FontFile`），閘 4 的 `embedded_fonts()` 根本掃不到它們。ch02 是第一個在圖標籤層出現**純文字散文標註**的章，才第一次把 CDN 襯線 webfont 帶進成品 PDF。
- **不可默默略過**：`check_glyphs.py` docstring 明文「找不到原始字型檔一律 FAIL 並指名，不默默略過——silent skip 正是 check_prose.py 的 figure_note_check 記錄過的偽陰性坑」。故本輪停下來交使用者裁決，未自行放寬。

### 5.2 裁決結果（2026-07-26 使用者選 A）：閘 4 對「圖匯入的字型」改用具名 allow-list

考慮過三案：**A** 收窄斷言改具名白名單；**B** 把 WebCM Serif 10 從 jsdelivr vendored 進 repo 並擴充閘 4 驗 `FontFile2`（需先徵下載同意，且 woff2 解壓要 `brotli` 套件、webfont 與 TeX 樹 NCM 是兩個 build、GID 對應未驗證）；**C** 維持現狀不產成品（LaTeX 線就此卡在 ch02，ch05 起若也有圖標註會一併卡住）。**使用者選 A。**

**改了什麼**（`check_glyphs.py`，34 行）：

- **LaTeX 自己嵌的字型（CFF）判準完全不動**——逐 CID 輪廓比對；非 CID-keyed 或找不到原始檔仍是硬 FAIL。
- **非 CFF 的嵌入字型改問另一個問題**：「它在不在 `FIG_IMPORTED_OK` 具名白名單內」。目前白名單只有一條 `WebCM-Serif-10-`（理由寫在該常數的註解裡）。**白名單外一律 FAIL 並指名**——新增條目等同新增一個「這套字型可以出現在成品裡」的裁決，要連理由一起寫進去。
- PASS 訊息分開報兩個數（驗過輪廓的字形數／白名單內的圖匯入子集數），不把兩者混成一個數字。

**為什麼 A 站得住**：閘 4 是 2026-07-17 那個 bug 的回歸閘，而那個 bug 是 **LuaTeX node mode 以字形名稱索引字形**的病——Chrome 的 print-to-PDF 匯出路徑沒有這個失效模式。圖 PDF 真正的風險是**字型被替換掉**（今天的 `√` 就是），而白名單正是針對這個風險的斷言。

**回歸驗證（三正一負）**：

| 測試 | 結果 |
|---|---|
| `dist/appB/appendixB.pdf` | PASS，362 個字形（與改前同數） |
| `dist/ch01/chapter1.pdf` | PASS，489 個字形（與改前同數） |
| `dist/ch02/chapter2.pdf` | PASS，467 個字形 ＋ 8 個白名單內圖匯入子集 |
| **負向**：把 §4 的 `--serif` 修正退掉、重匯 Figure 2.7 | **FAIL 並指名 `CAAAAA+MicrosoftJhengHeiUIRegular：FontFile2（非 CFF），且不在 FIG_IMPORTED_OK 白名單內`，exit code 1**——證明新判準不是放行，真的抓得到今天這個缺陷 |

---
*2026-07-26 建立。本輪的 HTML 內容側改動見 [`../../../html/_audit/REVIEW-ch02-plain-applied.html`](../../../html/_audit/REVIEW-ch02-plain-applied.html)（散文平實化回填 109 條）；§4 的圖字型修正與 §5.2 的閘 4 判準調整都是本 rollout 獨立發現、與平實化無關。*

## 6. 收尾輪：兩項數學待辦結案（2026-07-26）

ch02 平實化輪的 Codex gate-2 指出兩處屬數學內容、當時未執行，掛在 `PIPELINE.md` 的 Ch2 列。本輪逐條複查後結案。

| # | locus | 複查結論 | 處置 |
|---|---|---|---|
| ① | §2.3 Theorem 2.1 後的直覺段末句 | **非缺陷。** 原句 `an unbroken curve is still free to have a sharp corner, where no single tangent direction exists` 只斷言「**角點**沒有單一切線方向」，這個方向的推論成立；它並未主張逆命題。Definition 2.3 的白話重述本就寫明「no sharp corner, **no vertical spike**, and no break」，全書一致。先前把 Codex 對 `S20` **原句**（`to be differentiable is to have one definite tangent direction` 這種 iff 式刻畫）的指正外推到了下一句 | 真正的缺口是**完整性**：該段緊接 Example 2.12（\(\sqrt[3]{x}\) 垂直切線）之後，講反向失敗卻只提角點。改為 `a sharp corner or a vertical tangent. In neither case does the difference quotient approach one finite value.`——用的是本章 `C06` 已定的措辭（`approach one finite value`），維持 R3 指稱一致；**不新增數學片段、不新增破折號** |
| ② | §2.4 `\(y' = ky\)` 應用段 | 真有小缺口：`\(k\)` 從未說明是常數 | 補為 `for a constant \(k\)`。**未採** Codex 一併給 `\(Ce^{kx}\)` 的建議——微分 \(e^{kx}\) 需鏈鎖法則（Ch3），本章對 \(e^{x}\) 已有明示的 on-credit 借貸紀律，再塞一個當下無法驗證的斷言會抵銷該設計 |

**驗收**：`verify_edits.py` 兩節皆 PASS（各 1 筆替換，reverse-apply byte-for-byte、未涵蓋差異 0 處）；
散文 N 6992→7004、em-dash 維持 6、密度 0.86，tic guard 四項**零變動**；
數學片段 §2.3 **零差異**、§2.4 **+1 個 `\(k\)`**（即本次刻意補的），其餘三節零差異、cross-ref 全在位；
LaTeX 成品重產後四閘仍全綠（35 頁、0 error／0 missing char、Overfull 與 Underfull 皆 0、完整性 0 處真落差、
字形 467+8）；HTML 分頁 45 頁不變。

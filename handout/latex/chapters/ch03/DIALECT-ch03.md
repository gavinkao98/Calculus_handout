# M-P0 盤點：ch03 方言凍結表

> LaTeX pilot（[`../../KICKOFF-latex-pilot.md`](../../KICKOFF-latex-pilot.md)）M-P0 的落檔產物。
> **這是 `convert.py` 的權威 mapping 表**：轉換器只認這裡列的節點，其餘一律硬錯（kickoff §4.2 fail-loud）。
> 盤點對象＝`../../../html/fragments/ch03/sec-3-{1,2,3}.html`（880 行）＋ `../../../html/standalone/chapter3-print-standalone.html` 的 `FIGS`。
> 盤點日：2026-07-15。重跑：`python handout/latex/dialect_inventory.py ch03`。

## 1. 摘要

- **34 種 tag＋class 組合**，全部落在 [`../../../html/CONTRACT-html-writing.md`](../../../html/CONTRACT-html-writing.md) 的封閉方言內，**零意外標記**。
- **數學：inline `\(…\)` ×544、display `\[…\]` ×61**（皆為註解外的活數學）。數學區段內**零非 ASCII 字元**。
- **圖：7 個 `<figure data-fig>` ／ 8 個 SVG panel**（`remainder-tangent` 是 pair，兩格）。
- **活散文只用 6 個非 ASCII 字元**（見 §4），NCM 全數有字。

## 2. 凍結 mapping 表

「次數」為 ch03 三個 fragment 的實際出現數。父元素以盤點結果為準。

| # | Fragment 標記 | 次數 | LaTeX 目標 |
|---|---|---|---|
| 1 | `article.sec`（章開場變體，sec-3-1 第一個） | 1 | `\chapter*` 開場區塊 |
| 2 | `article.sec`（節） | 3 | 節容器（無 wrapper，直接展開） |
| 3 | `header.chapter-head` ＋ `div.ch-kicker` ＋ `h1.ch-title` | 1 | `\chapter*{…}`＋kicker 樣式 |
| 4 | `p.lead` | 1 | lead 段落（略大、softer） |
| 5 | `header.sec-head` ＋ `h2.sec-title` ＋ `span.sec-no` | 3 | `\section*`；`sec-no` **照抄字面**（D7） |
| 6 | `h3.subsec-head` | 10 | `\subsection*` 級樣式 |
| 7 | `p.para-head` | 1 | `\paragraph*` 級樣式 |
| 8 | `p` | 187 | 段落（散文 escape，數學 pass-through） |
| 9 | `p.informal` | 1 | 「Informally, …」gloss（斜體、softer） |
| 10 | `em` | 25 | `\emph{…}` |
| 11 | `ul` | 3 | `itemize` |
| 12 | `ol.steps` | 2 | `enumerate`（method steps 樣式） |
| 13 | `li` | 18 | `\item` |
| 14 | `section.env.env-definition` | 1 | definition 環境（teal） |
| 15 | `section.env.env-theorem` | 3 | theorem（blue，body 斜體） |
| 16 | `section.env.env-proposition` | 3 | proposition（blue，body 斜體） |
| 17 | `section.env.env-proof` | 6 | proof（從屬） |
| 18 | `section.env.env-example` | 16 | example（green） |
| 19 | `section.env.env-solution` | 16 | solution（green） |
| 20 | `section.env.env-remark` | 3 | remark（gray、較小） |
| 21 | `section.env.env-caution` | 4 | caution（紅實框） |
| 22 | `section.env.env-strategy` | 2 | strategy（紫實框） |
| 23 | `p.env-head` | 54 | 環境標頭列 |
| 24 | `span.env-kicker` | 54 | 環境名（Theorem／Definition…） |
| 25 | `span.env-num` | 28 | **照抄字面編號**（D7）。54 個標頭中僅 28 個有號——solution 等不編號 |
| 26 | `span.env-name` | 13 | 選用斜體描述名（含 qualified proof 的限定語） |
| 27 | `div.env-body` | 54 | 環境內文 |
| 28 | `div.workedexample` | 16 | example＋solution 群組＋`needspace` 級 keep-together |
| 29 | `figure.figure[data-fig]` | 7 | **就地 non-float**（D8）：`center`＋`\includegraphics[width=<mm>]` |
| 30 | `figcaption` ＋ `span.fig-no` | 7 | `\captionof*` 式字面圖說；`fig-no` 照抄字面 |

補充規則：

- **〔M-B2 修訂，2026-07-17〕開場 article 的頂層素 `<ul>` → `objectives` 語意槽**（非 `itemize`）：
  M-B1 拍板 objectives 為獨立槽位（`template/M-B1-DECISIONS.md` §2，D9 分層），emitter 對含
  chapter-head 的 article 一體適用——上表第 11 列的 3 個 `ul` 中，屬章開場者（sec-3-1 的
  objectives 清單）自 M-B2 起射 `objectives`，其餘正文 `ul` 仍為 `itemize`。開場 schema 凍結為
  至多一個素 `ul`，多於一個硬錯。
- **HTML 註解 → 全部丟棄。** ch03 註解含撰稿溯源筆記（`expansion:*` ×51、`③`／`波` 等），皆不進 LaTeX。
- **`article` 的 `lang="en"` 屬性 → 忽略**（pilot 全書英文，無 `babel` 切換需求）。
- **`figure` 的 `data-fig` → 查 `figs/ch03/figures.json` 取檔名與 mm 寬**。

## 3. Kickoff §4.2 列了、但 ch03 用不到（pilot 不實作）

依 kickoff §6「只覆蓋 ch03 實際用到的方言（M-P0 盤點為準）」，以下**不寫進 `convert.py`**；rollout 逐章補。遇到即照 fail-loud 硬錯。

| kickoff 列的 mapping | ch03 實況 |
|---|---|
| `table.tbl`／`tbl-wrap` → `booktabs` | **ch03 完全沒有 `<table>`**。§6 擔心的「反三角總表寬表溢出 150mm」不存在——那是 display math `aligned`（`sec-3-3.html:267`），散文的 “running table” 只是比喻 |
| `.qed` → `\qedhere` | **ch03 零 qed 標記**（6 個 proof、16 個 solution 都沒有），雖然 CONTRACT 說 proof 應以 `<span class="qed qed-proof">` 收尾 |
| `page-break-before` → `\clearpage` | ch03 未使用 |
| `code`／`kbd`／`strong` | ch03 未使用（散文只用 `<em>`，符合 CONTRACT） |
| `ol[start]` → `\setcounter` | ch03 的 `ol` 只有 `ol.steps`，無 `start` |
| `env-corollary` | ch03 未使用 |
| `p em`「First reading:／Proof track:」 | ch03 無 reading-track 段落（只在 `../../../html/fragments/ch01/sec-1-6.html`） |
| `figure-art--triple`／`--grid` → minipage | ch03 只有 `--pair` ×1 |

## 4. 字元盤點（「log 0 missing character」DoD 的依據）

**活散文（註解外、數學外）的非 ASCII 只有 6 個**，NewComputerModern 全數有字：

| 字元 | Unicode | 次數 |
|---|---|---|
| `—` em dash | U+2014 | 58 |
| `§` section sign | U+00A7 | 19 |
| `“` `”` curly quotes | U+201C／U+201D | 3／3 |
| `–` en dash | U+2013 | 1 |
| `’` right single quote | U+2019 | 1 |

- 依 kickoff §4.2，這些**不轉 ASCII**（lualatex＋NCM 原生成立，與 `quote_lint.py` 的 curly 政策一致）。
- **圈號 `①②③` 與 CJK `波` 全部在 HTML 註解裡**（撰稿溯源筆記），註解丟棄後不進 LaTeX → **不需要 CJK 字體、不需要圈號字符**。
- **數學區段內零非 ASCII** → 數學 pass-through 不涉及字元轉換風險。

## 5. 圖：實測清單

**7 個 figure／8 個 panel**（kickoff §3 DoD 寫「約 17 張」，實測為 7；DoD 原文即言「以 M-P0 盤點為準」）。

| data-fig | panel | 版面 | page px | mm 寬 | 內容路徑 |
|---|---|---|---|---|---|
| `sector-inequality` | 1 | single | 302×302 | 79.90 | 手刻 SVG |
| `squeeze-limit` | 1 | single | 309.64×198 | 81.92 | `buildPlot`＋MathJax 標籤 |
| `sin-cos-slope` | 1 | single | 208.13×123.45 | 55.07 | `buildPlot`＋MathJax 標籤 |
| `shm-triple` | 1 | single | 302×302 | 79.90 | 手刻 SVG（三疊 panel 共一 t 軸） |
| `composed-mapping` | 1 | single | 302×277 | 79.90 | 手刻 SVG＋`<defs><marker>` |
| `remainder-tangent` | **2** | **pair** | 248×188 ×2 | 65.62 ×2 | `buildPlot`＋note；並排 |
| `arcsin-vertical-tangent` | 1 | single | 242×338 | 64.03 | `buildPlot`＋MathJax 標籤 |

**尺寸換算的重要修正（與 kickoff §4.3 不同）**：kickoff 說「沿用各章 `--fig-3-*` px 值 → mm（px÷567×150mm）」。**公式的分母正確**（實測版心＝566.94px），**但 `--fig-3-*` 在 ch03 全是 `100%`，不是 px**。真正的 px 來源是 SVG 自帶的 inline `width`（例：`shm-triple` 是 `width:300px`）。

> **⚠ 若照 kickoff §4.1 的 `width=…\textwidth` 直接落地會出錯**：`shm-triple` 在 567px 版心裡實際只佔 300px（約半欄）。放大到 `\textwidth`（150mm）會把圖內 13px 標籤放大成約 18pt。**故 `.tex` 一律用上表的 mm 絕對寬**，由 `figures.json` 供給。

## 6. 圖匯出管線：M-P0 驗證結果

工具＝[`../../export_figs.mjs`](../../export_figs.mjs)（headless Chrome CDP → `Page.printToPDF`，零新依賴）。**8/8 panel 通過**，四種最難的序列化路徑都打通：

1. **手刻多 panel SVG**（`shm-triple`）：三疊曲線、紅虛線對齊、刻度標籤全對。
2. **`<defs><marker>` 內的 CSS 變數**（`stroke="var(--c-axis)"`）：箭頭正確著色——kickoff §6 最擔心的失真點不成立。
3. **MathJax NCM 標籤（`<foreignObject>`）**：`sin θ/θ`、`cos θ`、`R(h)` 皆完整，500 DPI 下向量清晰。
4. **pair 版面**：兩 panel 各 65.62mm，＋26px gap ＝ 約 137mm，塞得進 150mm 版心。

**做法與 kickoff §4.3 的差異（刻意）**：kickoff 說「把用到的 CSS＋resolved 變數內嵌進 `<style>`／inline style」。改為**照抄頁面 `<style>` 整塊＋重建祖先鏈 class**，descendant selector 與 CSS 變數原封生效，免去「逐項列舉 SVG presentation property」的漏一個就靜默走樣。祖先鏈的**版面幾何**另以 `.fx-neutral` 中和。

**開發過程中打掉的三個真 bug（留紀錄，避免 rollout 重蹈）**：

1. **祖先鏈把 `.sheet`（A4 頁框）帶進來** → 圖被推到 x≈254px，被 panel 尺寸的 viewport 裁成近乎空白。修法＝`.fx-neutral` 剝掉鏈上的 box 幾何。
2. **`await document.fonts.ready` 不足以載入 webfont** → 實測（控制組）拿掉強制載入後 `fonts.check()` 對 NCM／Inter 皆回 false，print 會靜默烤進系統後備字體。修法＝先 `Promise.all([...document.fonts].map(f => f.load()))` 再印，**並加 fail-loud 斷言**。
3. **panel 的墨水框 ≠ SVG 框** → `buildPlot` 刻意用 `<foreignObject x="-52" width="w+104">` 把 MathJax 標籤掛在 viewBox 外（`.fig-svg{overflow:visible}` 顯示之）。只量 SVG 框會裁掉標籤（實測 `squeeze-limit` 的 `θ` 消失）。修法＝page box ＝ SVG 框 ∪ 各 `.fig-lbl` 框（不可用 `.fig-fo`，那是整個 52px margin 框、大半是空白）。

## 7. 待裁決／待處理事項（非 M-P0 blocker）

| 項 | 內容 | 何時處理 |
|---|---|---|
| F1 | **`composed-mapping` 的 Times New Roman**：標籤用 Unicode 下標零 `x₀`（U+2080），Inter 無此字符 → Chrome 單獨對該字符掉到 Times。已用 CDP `CSS.getPlatformFontsForNode` 逐節點比對，**真實 HTML 頁面與匯出完全一致**（Inter×7 + Times×1），故**非匯出失真，是既有 HTML 的既存瑕疵**。依 D6「HTML 留檔不修」未動。但這會原樣進入「出版級」PDF | **M-P5 GO/NO-GO 一併裁決** |
| F2 | **proof 的 QED 記號**：ch03 的 HTML proof 無 qed 標記，而 LaTeX `proof` 環境預設自動補 `□`。要跟隨 HTML（拿掉）還是取「書的樣子」（保留）？ | M-P3 樣式定案 |
| F3 | **pair 圖的置中基準**：匯出的 page box 含標籤溢出，溢出左右不對稱；LaTeX 置中的是墨水框，HTML 置中的是 SVG 框 → 圖可能有數 px 級的視覺位移 | M-P4 人眼閘確認是否可見 |

## 8. 環境結論（kickoff §8 的 open items 已收斂）

| kickoff §8 列的「可能新安裝」 | 實測結果 |
|---|---|
| `pdftotext`／`pymupdf`（完整性閘） | **不必裝**——poppler 已在機上（`pdftoppm`／`pdftocairo`／`pdftotext` 皆有；另有 MiKTeX 的 `mgs`） |
| `inkscape`／`cairosvg`（圖匯出 fallback） | **不必裝**——首選路線（headless Chrome）8/8 通過，fallback 不啟用 |
| Inter 桌面字體（圖說 sans 對映） | **圖內文字不需要**——Inter 由 CDN 載入並已嵌入匯出的 PDF。LaTeX **本文側**的 sans（圖說、表頭）是否裝 Inter 仍待 M-P3 裁決 |

已驗環境：LuaHBTeX 1.24.0（MiKTeX 26.2）、latexmk 4.88、node v22.19.0、Chrome（桌面版）、poppler。legacy 六件式 preamble 完整在 `legacy/tex_handout/preamble/`。

## 9. Codex gate-2 覆核紀錄（兩輪，2026-07-16）

read-only 對抗式覆核，兩輪都判 **不能 sign-off**；ch03 成品本身經兩輪確認完整正確
（24 頁、0 error／0 missing char／0 overfull、note 在、fresh 轉換與樹上 `.tex` 逐字相同）。
真正的價值在它戳破的**方法論錯誤**——都記在這裡，免得 rollout 重犯：

| # | 它戳破的東西 | 狀態 |
|---|---|---|
| 1 | **數學保護層不是封閉的不變式**：非貪婪 regex 遇同類分隔符巢狀會提早閉合、未配對不報錯、`\\[` 誤判、註解內數學被挖 | 已修：改單趟 scanner（跳註解、`\X` 當單位吃掉故反斜線奇偶自然正確、巢狀／未配對／游離 closer 硬錯） |
| 2 | **「605 段都是 .tex 的 substring」是弱保證**：驗不到順序、重複、遺漏 | 已修：改**封閉不變式**——`LatexEmitter.used` 記錄還原索引，斷言 `used == range(N)`（恰好一次＋依源順序）。**它上線後第一件事就是抓到自己人寫的 bug**（`\item` 修法對同一 item 呼叫兩次 `para_text()`） |
| 3 | **測試 oracle 循環論證**：拿轉換器自己的 `MATH_RE` 當 oracle，regex 漏認就兩邊一起錯 | 已修：測試改用獨立重寫的 `naive_scan_math()`。**但 Codex 第二輪指出它仍非「獨立語義模型」**（同樣漏 entity delimiter），列為未關閉 |
| 4 | **fail-loud 有靜默繞過**：`<ul>DROP<li>` 的裸文字被丟、`<em class="x">` 不驗、`<strong class="env-kicker">` 靠 `text_of()` 遞迴攤平混入、sec-head 多餘節點被忽略 | 已修（`bare()`／嚴格 `text_of()`／各分支驗 class／`section_head` 驗 cardinality） |
| 5 | **重複欄位覆寫＝靜默掉文**：兩個 `div.env-body` 時前者整段消失 | 已修：`once()` 對 env-head／env-body／kicker／num／name／ch-title／sec-no／fig-no 一律硬錯 |
| 6 | **`\item [x]` 的 optional-argument 洞** | 已修：`[` 開頭的 item 前插 `\relax` |
| 7 | **`export_figs` 漏掉 `.fig-note`**（Figure 3.6 的 “larger h”／“smaller h”，`<svg>` 的兄弟節點） | 已修：改匯出整個 `.fig-panel`，墨水框 ＝ svg ∪ `.fig-lbl` ∪ `.fig-note` |
| 8 | **`used` 不變式有偽陽性**：emitter 先算 body 再算 env-name，env-name 帶數學時記成 `used=[1,0]`，**輸出正確卻被誤擋**（ch03 的 13 個 env-name 剛好都沒數學才沒踩到） | 已修：name 在 body 之前算 |
| 9 | **`check_prose.py` 散文全乾淨時提早 return**，圖內文字閘根本不會跑 | 已修 |
| 10 | **entity 編碼的分隔符讓 HTML 與 LaTeX 語義分岔**：`&#92;(x&#92;)` 瀏覽器當數學，scanner 掃未解 entity 的原文看不到 | 已修：偵測到 `&#92;`／`&#x5C;`／`&bsol;` 即硬錯 |
| 11 | **CONTRACT 的「no solo example」沒真的執行**：workedexample 內只有一半也接受 | 已修：要求恰一個 example ＋一個 solution |
| 12 | **HTMLParser 靜默吞掉 CDATA／DOCTYPE／PI／游離結束標籤** | 已修：四者皆硬錯 |
| 13 | **Windows cp950 主控台**：文件寫的指令會 `UnicodeEncodeError` | 已修：三支工具自行 reconfigure stdout/stderr |

**尚未關閉（rollout 前必補，見 §10）**：PUA 代位偽陰性（重複欄位覆寫已修，複合繞過大幅收斂但未證明封閉）、
測試 oracle 非 exact-once 且與 production 共用語義盲點、圖內文字閘的 oracle 循環。

golden tests：36 →（修回歸）37 →（鎖 Codex 第一輪反例）52 →（鎖第二輪反例）**58**。

## 10. rollout 前的待辦

1. **圖內文字閘要獨立於 exporter**：現行 `figure_note_check` 的 oracle 是 exporter 自己申報的
   `figures.json`——exporter 若再漏 note，manifest 也沒 note，閘就放行（**已實測此偽陰性**）。
   另一個做法（HTML PDF vs LaTeX PDF 詞集比對）也被實測否決：note 是 “larger h”，而 “larger”
   在課文散文裡也有（*the larger triangle OAC…*），詞集找得到就誤判成沒掉。
   可行方向：只讀 live page 的 CDP 探針列舉 figure 內全部文字節點，或對 HTML 印出的 PDF 做
   exact-phrase count 比對。
2. **測試 oracle 補 exact-once**：現行 `find`/advance 只是 ordered subsequence，會接受額外副本。
3. **`\relax` 缺專屬 golden test**（`[` 開頭的 item）。
4. **single-layout 的 `.fig-panel` 路徑未被 fixture 覆蓋**：ch03 的 single 圖實際走 bare-SVG
   fallback（`offX=offY=1px`），負 offset 只有 pair panel 真的走到。公式經 Codex 覆核為正確。

---

*M-P0 完成。M-P1–P4 見 [`REVIEW-latex-pilot-ch03.html`](REVIEW-latex-pilot-ch03.html)。*

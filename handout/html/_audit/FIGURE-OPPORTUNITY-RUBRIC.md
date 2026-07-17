# 講義圖機會稽核 — 鏡頭與裁決維度（FIGURE-OPPORTUNITY-RUBRIC）

> 本檔是「**圖機會稽核**」的契約與**單一真相來源**。`handout-figure-opportunity-audit` subagent 讀本檔判斷；鏡頭／維度／輸出格式**只在這裡改一次**。從 ch03 圖機會稽核（2026-06-21）的實證蒸餾，產物見 [`REVIEW-ch03-figure-opportunity.html`](REVIEW-ch03-figure-opportunity.html)（提案）／[`REVIEW-ch03-figure-opportunity-applied.html`](REVIEW-ch03-figure-opportunity-applied.html)（成品）。
>
> **權威規範**見 [`CONTENT_SPEC.md`](../../../CONTENT_SPEC.md) §10（何時加圖、`[FIGURE-OPPORTUNITY]` 佔位符 schema、label economy、工具選擇與 kit 能力）。本檔只定「用哪些鏡頭掃、怎麼裁決一個候選、哪些不算機會、怎麼回報」，**不重述** §10 的規範本身。
>
> **本審 vs correctness 審（別混為一談）：** 本檔審「**該不該加圖**」（opportunity，出圖**之前**、Mode A／C 擴增稽核）；[`FIGURE-AUDIT-RUBRIC.md`](FIGURE-AUDIT-RUBRIC.md) 審「**畫出來對不對、讀不讀得懂**」（D1–D8 correctness，render 成 PNG **之後**）。兩者互補，是同一張圖生命週期的兩端。

## 審查對象與邊界

- **審**：講義單節 fragment（`handout/html/fragments/ch{NN}/sec-*.html`）的散文＋環境＋既有圖——找「目前純文字、用圖會更直覺」的位置。
- **不審**：已畫好的圖對不對（→ correctness 審）、散文易懂性（→ `handout-prose-audit`）、數學正確性、example 選題。
- **枚舉先對齊既有圖**：開審 `Grep '<figure'` 該節＋查該章 PLAN 的 figure ledger；既有圖與手稿已有的圖**不重複提案**，只找缺口。

## 鏡頭（兩個都要走）

- **L1 幾何直觀／視覺化證明思路**：面積／長度比較、單位圓、反函數對 \(y=x\) 鏡射、參考直角三角形、切線與線性近似（餘項 \(R(h)\) 比 \(h\) 更快趨零）、mapping／箭頭 diagram。問：哪個定理／定義／證明步驟，用一張幾何圖會比逐字散文更快讓讀者「看見」為何成立？
- **L2 函數行為／coordinate graph ＋密度**：導數即切線斜率（如 sin 斜率＝cos 高度）、漸近線、垂直切線、夾擠（squeeze）、振盪曲線、凹凸。並做 §10 密度檢查：哪些計算型段落／example 圖太稀疏（**零圖的節是明顯缺口**；Stewart 密度＝視覺豐富主題近每頁一張）。問：哪段在描述函數的形狀／行為／趨勢，畫成 graph 會比文字更直覺？

> 同一個機會常被兩鏡頭各提一次（如「sin 斜率＝cos 高度」）——合併為一筆，別當兩條。

## 提案 schema（每個候選，對齊 §10 `[FIGURE-OPPORTUNITY]`）

- **locus** — 在該節哪裡：標題／環境／Example 編號 ＋ 引一句原文錨點（要可定位）。
- **teaching_function** — 這張圖**教什麼**（如「幾何直觀：squeeze 把 \(\sin\theta/\theta\) 夾到 1」），**不是**「畫個圖」。
- **figure_type** — `graph`（coordinate graph，buildPlot）／`diagram`（schematic／mapping，inline SVG）／`multi-panel`。
- **why** — 為何此處**圖 > 純文字**（散文承載不了的二維對應／形狀／趨勢）。
- **domain_facts**（§10 硬要求）— 若散文宣告**定義域限制／間斷／未定義點**，**MUST** 記下及其圖示後果（如「\(y=\pm1\) 導數不存在 → 端點空心、不收邊」「\(\theta=0\) 未定義 → 空心點」）。無則填「無」。
- **priority** — `high`／`medium`／`low`。
- **relation** — 與既有圖（Figure N.x）或既往刻意決策（如某節 no-figure）的關係。

## 裁決維度（每個候選逐項過，**預設駁回**——只有顯著優於散文才 keep）

- **D1 散文已自足？** 該處散文已把概念說清、加圖只是錦上添花 → **drop／low**。（最常見的駁回理由。）
- **D2 重複既有圖？** 與本章既有 figure 或手稿已有的圖重疊 → drop（除非提「強化／補充」且講清差異）。
- **D3 違背既往刻意決策？** 如某節 ③ 決定 no-figure、某章 D-decision 排除某框架。**違背要明講「這推翻了 X 決定」並評估 override 是否有理**（窄義、有獨立理由可 keep；否則 drop）。
- **D4 manuscript-faithful？** 圖只視覺化講義**既有**內容、**不引入講義沒有的新數學／新方法**（如本節走 composition-identity 卻畫 reciprocal-slope，即不忠）→ drop。
- **D5 kit 畫得出？** `buildPlot` graph（曲線／漸近線／刻度／實心-空心 dot）或 inline SVG（三角形／鏡射線／箭頭／mapping）能落地 → 否則註明不可行。
- **D6 no-spoiler？** worked-example 圖不可洩露學生要算的量（已給完整解的 example 通常風險低，但仍須判）。

> **收斂判準**：本 gate 無「blocking 歸零」概念——它是**提議清單**，由使用者逐條裁決要不要生成。乾淨（0 候選）是有效結果。

## 不算機會（別硬提；§10）

- 純代數操作、無幾何／圖形直覺可言的段落（§10：不必硬標）。
- 裝飾性圖、為填半空頁的圖（§10 明文禁止）。
- 既有手稿圖或已繪好的圖（只標「應有圖但目前沒有」）。
- 重述既有圖的同一概念、無新教學角度者。

## 護欄

- 稽核員**唯讀**：只回報候選清單，**不畫圖、不改任何檔**。
- 提「加圖」是**提議，不是行動**——一律交回使用者裁決；核可後才進落地（fragment `<figure data-fig>` ＋ standalone `FIGS`，見 [`handout/CLAUDE.md`](../../CLAUDE.md)「圖表系統」），落地後 render 自驗再跑 correctness 審。
- **不 over-report**：硬湊裝飾圖會稀釋真正的機會。寧缺勿濫。

## 回報規格

- 首行：`VERDICT: <N> 候選（high <h> / medium <m> / low <l>）；駁回 <d>`
- 逐條候選卡（keep）：`[priority] <sec> <figure_type>｜<title> — locus｜teaching_function｜why｜domain_facts｜relation`
- 駁回項各一行：`[DROP] <title> — <維度 D?>：理由`
- 末行：本節（或全章）圖機會掃描結論。

**分工（唯讀 gate 回文字、orchestrator 落 HTML）：** `handout-figure-opportunity-audit` subagent 唯讀（無 Write），**只回傳上述文字格式的 findings**，不自貼 HTML 原始碼。給使用者裁決的 **standalone HTML 交付稿由父代理／orchestrator** 彙整 findings 後落檔——檔名 `REVIEW-ch{NN}-figure-opportunity.html`（多節彙整一檔、逐節分塊；單節亦可 `…-sec-N-M-…`），MathJax／KaTeX CDN、雙擊即開、數學即渲染、頂部裁決總表、逐條卡片，比照 [`REVIEW-ch01-figure-opportunity.html`](REVIEW-ch01-figure-opportunity.html)／[`REVIEW-ch03-figure-opportunity.html`](REVIEW-ch03-figure-opportunity.html)。核可生成圖後，另產 `REVIEW-ch{NN}-figure-opportunity-applied.html`（成品報告，內嵌實際 render 截圖），比照 [`REVIEW-ch03-figure-opportunity-applied.html`](REVIEW-ch03-figure-opportunity-applied.html)。

## 規模升級（subagent ↔ workflow）

- **標準 per-section gate ＝本 subagent 單次 run**（雙鏡頭＋對抗式自核，足以涵蓋單節）。
- **整章一次性掃描或要更高信心**時，可升級為**多代理 workflow**（逐節 × 雙鏡頭提案 → 合併去重 → 每候選一個對抗式複核 → 完整性批判 → 補件複核）——ch03 即用此 workflow（19 agents），擋下了完整性批判自稱「最高價值」但不忠實的假陽性。subagent 是日常閘、workflow 是深掃，兩者判準同出本檔。

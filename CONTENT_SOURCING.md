# 題源與選題流程（課文範例）

服務對象：**講義課文內的 worked examples**（`example`＋`solution`，[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §5；
HTML 線為 `env-example`＋`env-solution`，見 [`experiments/handout_kit/CONTRACT-html-writing.md`](experiments/handout_kit/CONTRACT-html-writing.md)）。

> **講義本體不收習題**（使用者 2026-06-12 定案，[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §14）。
> 習題將以**獨立的習題本**呈現，屆時另立規格、沿用本檔的題源與授權框架；
> 舊的習題骨架（`CONTENT_EXERCISES.md`）與 Ch 1 習題候選文件可從 git 歷史取回（commit `7d6fde9` 前的樹）。

## 流程（manuscript 優先 → 題庫補缺 → AI 備援）

範例從三個來源進入課文，按優先順序，每筆追蹤 provenance：

1. **手稿範例——必要核心。** 教師手稿中的每個例子都出貨，經 Mode A 擴寫成正式 worked example。
2. **開放題庫——示範缺口填補。** 該節主要內容寫好之後：
   1. 盤點該節**既有的 worked examples**；缺口＝「該節教過的 definition／theorem／strategy
      沒有對應示範」（不是「題目不夠多」——數量克制，每節通常補 1–3 個）。
   2. 在本地題庫（[`problem_banks/README.md`](problem_banks/README.md)）搜尋候選，
      產出**可直接閱讀的審核文件**（standalone HTML，數學即渲染）供使用者裁決。
      題庫的分類法只是搜尋索引——缺口永遠由講義自身內容定義。
   3. **官方完整 solution 是硬條件**：worked example 必須附解，只收解材完整的源
      （只有最終答案的題不合格，除非解由我們撰寫並標記為改作）。
   4. 通過裁決後改寫為本書語域與記號（[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §3、§9），
      插入課文中教學上正確的位置（緊跟相關 definition／theorem／strategy）。
3. **AI 出題——備援。** 僅用於題庫填不了的缺口（如緊扣手稿 running example 的延伸、
   或為本書特有約定量身打造的示範）。出題後一律經使用者審核。

## Provenance 與標記

- 沿用既有的 expansion-marker 慣例：每筆題庫來源的範例前加註
  `% expansion:example — <一行說明> [source: CLP-1 §1.4 #25]`（LaTeX）或
  `<!-- expansion:example — … [source: …] -->`（HTML）。三分類：手稿／`[source: 題庫…]`／`[source: AI]`。
- **匯入當下**把題源的官方 hint／answer／solution 全文、授權標記、改寫差異說明存入該章旁的
  `chNN_example-imports.md`（如 `experiments/handout_kit/ch01_example-imports.md`）。
  改寫若更動數學實質（例如依本書 principal-range 約定重算），必須在 import record 中逐筆說明。

## 授權

- 已接入與候選題庫全為 **CC BY／CC BY-NC／CC BY-NC-SA** 家族（逐源清單與紅線見
  [`problem_banks/README.md`](problem_banks/README.md)），可合法 remix 進
  **免費發布、整體掛 CC BY-NC-SA 4.0** 的講義，附 credits 頁。
- **不收**：CC BY-SA 來源（與 NC-SA remix 不相容，如 Active Calculus）、
  「免費瀏覽但保留版權」來源（如 Paul's Online Math Notes）、College Board AP 歷屆題。
- 講義正式發布前需落地：全書授權聲明＋credits 頁（每筆題庫來源列出處與授權）。

## 審核交付物的形式（2026-06-12 使用者要求）

給使用者裁決的候選文件**不要**用塞滿生 LaTeX 的 `.md`——產出 standalone HTML
（MathJax／KaTeX CDN，雙擊即開、數學即渲染），裁決表放文件開頭、可直接複製回填。

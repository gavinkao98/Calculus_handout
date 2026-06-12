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
   4. **裁決前先過一輪選題稽核（2026-06-12 新增）**：以 `codex exec` 唯讀 auditor
      （走 ChatGPT 訂閱配額——動用前徵得使用者同意）對照課文片段覆核：缺口判定是否成立、
      候選是否對症且程度合適、自寫／改作之解的數學正確性、來源與授權標示是否屬實。
      契約沿用 [`experiments/direction_layer/RULE.md`](experiments/direction_layer/RULE.md) ⑤
      （數學／忠實度／對症性為 blocking；格式為 advisory），收斂到 blocking=0 再交使用者裁決。
      **findings 必須留版控**：Codex 原始輸出落在 `.tmp/`（gitignored、換機即失、使用者看不到），
      因此每輪稽核的 findings 原文＋Claude 的 triage 處置要存進該章旁的
      `chNN_<artifact>-audit.md`（範例：`ch01_example-supplement-audit.md`），不可只留在 commit message 摘要。
   5. 通過裁決後改寫為本書語域與記號（[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §3、§9），
      插入課文中教學上正確的位置（緊跟相關 definition／theorem／strategy）。
3. **AI 出題——備援。** 僅用於題庫填不了的缺口（如緊扣手稿 running example 的延伸、
   或為本書特有約定量身打造的示範）。出題後一律經使用者審核。

## 選題標準（缺口成立後，在候選之間怎麼挑）

**硬條件**（不滿足即不入候選）：

1. **對症**：候選必須示範該缺口的教學點本身，不是「同主題的另一題」。
2. **解材完整**：官方 solution 全文可得；僅有最終答案的源，解須由我們撰寫，
   並在審核文件中逐筆標明「解為本次撰寫」。
3. **授權**：BY／BY-NC／BY-NC-SA 家族（見下方授權一節）。
4. **程度貼齊受眾**：高中自學者讀得動；超綱或過難者降為「選收」或不收。

**排序偏好**（多個候選滿足硬條件時）：

- **教新動作**：優先選能示範課文尚未出現之「動作」（新技巧、新表徵、概念辨析）的題；
  已有同型示範就不再加——範例是教學，不是 drill。
- **經典誤解優先**：直接針對已知學生誤區的題價值最高（如 \(1/x\) 與 \(1/x^2\) 的
  DNE／∞ 之分、0/0 可為任何值、分母為零≠漸近線、ε-δ 量詞順序）。
- **結構對位**：能緊跟一個明確的 definition／theorem／strategy 插入、或能縫接相鄰節
  （forward reference）者優先。
- **改作幅度最小**：照搬可用 > 輕改 > 重算／重寫；幅度大者（如依本書 principal-range
  約定重算）必須在審核文件中單獨點名請使用者過目。
- **附圖成本**：同等教學價值下，不需新圖者優先；需新圖者計入成本一併揭露。

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

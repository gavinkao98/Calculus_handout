# handout —— 講義產線（HTML 撰稿線＋LaTeX 出版線）

> 本資料夾是**生產用講義**（2026-06-15 自 `experiments/handout_kit/` 升格為頂層正式版；
> 2026-07-17 依兩線分工重整為 `html/`＋`latex/`）。
> 完成一章的閘序與各章狀態見 [`PIPELINE.md`](PIPELINE.md)；撰稿模式見 [`../CONTENT_AUTHORING_WORKFLOW.md`](../CONTENT_AUTHORING_WORKFLOW.md)；
> 本資料夾特有的架構約束（fragment 為源、registry、圖表兩處同改）見 [`CLAUDE.md`](CLAUDE.md)。

## 兩線分工（2026-07-17 使用者拍板）

- **[`html/`](html/)＝HTML 撰稿製作線（工作線）**：內容撰寫、QA 閘鏈、圖系統都在這裡推進；
  standalone 是撰稿預覽＋圖閘 render 載體。**整體先做 HTML 講義。**
- **[`latex/`](latex/)＝LaTeX 出版排版線（定稿轉換）**：「為了好看，最後定稿的講義把 HTML
  轉成 LaTeX」——確定性轉換（fragment 唯讀、數學逐位元組）出出版級 A4 PDF。
  appB pilot 已 GO（HTML 20 頁 → LaTeX 14 頁，四閘全綠；沿革與 rollout 計畫見
  [`latex/KICKOFF-latex-pilot.md`](latex/KICKOFF-latex-pilot.md)）。
- fragment 永遠是唯一內容源；轉出的 `.tex` 是 build 產物（gitignored），不是第二份源。

## 目錄結構

```
handout/
  README.md / CLAUDE.md / PIPELINE.md   # 樞紐、架構約束、閘序＋dashboard
  html/                                 # ── HTML 撰稿製作線 ──
    build.py                            #   組裝腳本（唯一建置工具）
    quote_lint.py                       #   散文引號 lint（CONTENT_SPEC §8，CI 會跑）
    CONTRACT-html-writing.md            #   權威性 HTML 標記契約
    TYPESETTING_GUIDE.md                #   排版指南
    fragments/                          #   內容源（每章一資料夾、每小節一檔）
      ch01/ … ch06/  appA/ … appD/
    standalone/                         #   build 產出的列印版（每單元一檔）
      chapter{1..6}-print-standalone.html
      appendix{A..D}-print-standalone.html
    _render/                            #   shot.mjs（截圖餵圖閘）、linebreak-gate.mjs（斷行閘）
    _audit/                             #   稽核 rubric＋REVIEW-*.html 裁決／完工報告
    _dev-archive/                       #   各章開發過程文件（歷史紀錄，路徑不回改）
  latex/                                # ── LaTeX 出版排版線 ──
    README.md                           #   線導覽＋章節狀態表（哪章在哪、怎麼建置）
    KICKOFF-latex-pilot.md              #   pilot 沿革＋rollout 計畫（權威）
    make_dist.py                        #   產成品夾（轉換＋內嵌＋編譯＋驗收）
    convert.py / test_convert.py        #   確定性轉換器＋golden tests
    dialect_inventory.py                #   方言盤點器（逐章差集）
    check_prose.py                      #   pdftotext 散文子序列閘
    export_figs.mjs / print_html.mjs    #   圖匯出（向量 PDF）／HTML 印 PDF（對照報告用）
    dist/                               #   ★ 成品夾：每單元一夾、夾內只有 <name>.pdf＋<name>.tex
    template/                           #   共用模板：calcbook.sty（語意＋樣式層）、sampler、fonts/inter
    chapters/                           #   章節工作資產各住一夾（DIALECT＋driver＋對照報告＋figs）
      ch03/  appB/                      #   已有；rollout 逐章新增
    build/                              #   lualatex 工作目錄（gitignored；含 aux-<ch>/ 殘渣）
    _dev-archive/                       #   v1 book-class shell 歸檔
```

## 架構（HTML 線）

內容唯一存放在 `html/fragments/ch{NN}/`，每個小節一個 HTML 檔（canonical = print 版格式）。

`html/build.py` 讀取 fragment，包進 `<template>` 標籤，插入各 standalone 檔的
`<!-- BEGIN-CONTENT-FRAGMENTS -->` / `<!-- END-CONTENT-FRAGMENTS -->` 標記區間；
fragment 順序的**單一真實來源＝`build.py` 的 `CHAPTERS` registry**（詳見 [`CLAUDE.md`](CLAUDE.md)）。

Standalone 檔自帶全部 CSS/JS，**雙擊即開**（需連網載 MathJax v4 CDN）。
MathJax v4 啟用了 inline line-breaking（`linebreaks.inline: true`），
搭配 `text-align: justify` 可大幅改善行內公式造成的字距不均。

## 日常操作

```powershell
# 改完 fragment 後重新組裝（全部章節＋附錄；在 handout/ 下執行）
python html/build.py

# 只重建某一章
python html/build.py ch01

# 顯示式自動斷行閘（預設掃 standalone/ 全部檔案）
node html/_render/linebreak-gate.mjs

# LaTeX 線：產成品（dist/<ch>/ 兩檔：pdf＋自足 tex；詳見 latex/README.md）
cd latex && python make_dist.py appB
```

## 環境

- `html/build.py` 組裝 HTML 是**純 Python stdlib**，任何 python 都能跑、無額外依賴。
- standalone HTML 雙擊即開，但**檢視時需連網**載 MathJax/KaTeX CDN。
- `html/_render/shot.mjs`（render 成 PNG 餵 figure 稽核）需要 **Node ≥21** ＋ **Google Chrome**
  （Chrome 路徑先讀 `CHROME` 環境變數、再退回常見安裝位置）。
- `latex/` 線需 MiKTeX（lualatex＋latexmk）＋poppler（pdftotext）；vendored Inter 隨 repo 走。
- 整 repo 環境統一見根目錄 [`../ENVIRONMENT.md`](../ENVIRONMENT.md)；換機跑 `python ../tools/doctor.py` 檢查。

## 新增章節（HTML 線）

1. 在 `html/fragments/ch{NN}/` 放好小節 HTML（照既有格式撰寫；無手稿章 fragment 頂部帶 `<!-- section-source: -->` header）。
2. 在 `html/build.py` 的 `CHAPTERS` dict 加一筆：

   ```python
   "ch07": {
       "fragments": ["sec-7-1", "sec-7-2", ...],
       "target": "chapter7-print-standalone.html",
   },
   ```

3. 準備列印版 standalone shell 檔（放 `html/standalone/`，從既有章節複製，替換 chrome 設定，
   內容區留 `<!-- BEGIN-CONTENT-FRAGMENTS -->` / `<!-- END-CONTENT-FRAGMENTS -->` 標記）。
4. 跑 `python html/build.py ch07`。
5. 瀏覽器開檔驗證：數學式渲染、圖片 hydrate、分頁器皆正常（另跑 `node html/_render/linebreak-gate.mjs` 驗顯示式無自動斷行）。

## 現有章節

| 章／附錄 | 列印版（`html/standalone/`） | 節數 | 狀態（詳見 [`PIPELINE.md`](PIPELINE.md) dashboard） |
|---|---|---|---|
| Ch 1–4 | `chapter{1..4}-print-standalone.html` | 6／5／3／5 | 全閘完成（手稿章 gate 0–8） |
| Ch 5 | `chapter5-print-standalone.html` | 9（§5.1–§5.9） | 全閘完成・三閘 gate-2 定版（canon 首例） |
| Ch 6 | `chapter6-print-standalone.html` | 5（§6.1–§6.5） | 全閘完成・首個全程 5-milestone 試點章 |
| App A–D | `appendix{A..D}-print-standalone.html` | 6／5／4／3 | 自撰服務性附錄，按需維護 |

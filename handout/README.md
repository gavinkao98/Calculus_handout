# handout —— HTML 講義排版工具（生產版）

> 本資料夾是**生產用講義**（2026-06-15 自 `experiments/handout_kit/` 升格為頂層正式版）。
> 完成一章的閘序與各章狀態見 [`PIPELINE.md`](PIPELINE.md)；撰稿模式見 [`../CONTENT_AUTHORING_WORKFLOW.md`](../CONTENT_AUTHORING_WORKFLOW.md)；
> 本資料夾特有的架構約束（fragment 為源、registry、圖表兩處同改）見 [`CLAUDE.md`](CLAUDE.md)。

## 這資料夾是什麼

一套 **HTML/CSS/JS handout kit**：用語意標記寫內容，由小節檔產出
**A4 列印版**（MathJax v4、自動分頁、存 PDF）。

## 目錄結構

```
handout/
  build.py                           # 組裝腳本（唯一建置工具）
  CONTRACT-html-writing.md           # 權威性 HTML 標記契約
  PIPELINE.md                        # 完成一章的閘序＋各章狀態 dashboard
  TYPESETTING_GUIDE.md               # 排版指南
  fragments/
    ch01/  (6 檔: sec-1-1 … sec-1-6；章開場併入 sec-1-1)
    ch02/  (5 檔: sec-2-1 … sec-2-5)
    ch03/  (3 檔: sec-3-1 … sec-3-3)
    ch04/  (5 檔: sec-4-1 … sec-4-5)
    ch05/  (9 檔: sec-5-1 … sec-5-9；首個無手稿 canon 章)
    appA/…appD/                      # 附錄 A–D（自撰，無手稿先例）
  chapter{1..5}-print-standalone.html    # 列印版（build 產出）
  appendix{A..D}-print-standalone.html   # 附錄列印版（build 產出）
  _render/                           # shot.mjs（截圖餵圖閘）、linebreak-gate.mjs（顯示式斷行閘）
  _audit/                            # 稽核 rubric（4 份）＋ REVIEW-*.html 裁決／完工報告
  _dev-archive/                      # 各章開發過程文件（PLAN / seed / brief / audit 等，歷史紀錄）
```

## 架構

內容唯一存放在 `fragments/ch{NN}/`，每個小節一個 HTML 檔（canonical = print 版格式）。

`build.py` 讀取 fragment，包進 `<template>` 標籤，插入各 standalone 檔的
`<!-- BEGIN-CONTENT-FRAGMENTS -->` / `<!-- END-CONTENT-FRAGMENTS -->` 標記區間；
fragment 順序的**單一真實來源＝`build.py` 的 `CHAPTERS` registry**（詳見 [`CLAUDE.md`](CLAUDE.md)）。

Standalone 檔自帶全部 CSS/JS，**雙擊即開**（需連網載 MathJax v4 CDN）。
MathJax v4 啟用了 inline line-breaking（`linebreaks.inline: true`），
搭配 `text-align: justify` 可大幅改善行內公式造成的字距不均。

## 日常操作

```powershell
# 改完 fragment 後重新組裝（全部章節＋附錄）
python build.py

# 只重建某一章
python build.py ch01
```

## 環境

- `build.py` 組裝 HTML 是**純 Python stdlib**，任何 python 都能跑、無額外依賴。
- standalone HTML 雙擊即開，但**檢視時需連網**載 MathJax/KaTeX CDN。
- `_render/shot.mjs`（把 `.sheet` render 成 PNG 餵 figure 稽核）需要 **Node ≥21** ＋ **Google Chrome**
  （Chrome 路徑先讀 `CHROME` 環境變數、再退回常見安裝位置）。
- 整 repo 環境統一見根目錄 [`../ENVIRONMENT.md`](../ENVIRONMENT.md)；換機跑 `python ../tools/doctor.py` 檢查。

## 新增章節

1. 在 `fragments/ch{NN}/` 放好小節 HTML（照既有格式撰寫；無手稿章 fragment 頂部帶 `<!-- section-source: -->` header）。
2. 在 `build.py` 的 `CHAPTERS` dict 加一筆：

   ```python
   "ch06": {
       "fragments": ["sec-6-1", "sec-6-2", ...],
       "target": "chapter6-print-standalone.html",
   },
   ```

3. 準備列印版 standalone shell 檔（從既有章節複製，替換 chrome 設定，
   內容區留 `<!-- BEGIN-CONTENT-FRAGMENTS -->` / `<!-- END-CONTENT-FRAGMENTS -->` 標記）。
4. 跑 `python build.py ch06`。
5. 瀏覽器開檔驗證：數學式渲染、圖片 hydrate、分頁器皆正常（另跑 `node _render/linebreak-gate.mjs` 驗顯示式無自動斷行）。

## 現有章節

| 章／附錄 | 列印版 | 節數 | 狀態（詳見 [`PIPELINE.md`](PIPELINE.md) dashboard） |
|---|---|---|---|
| Ch 1 | `chapter1-print-standalone.html` | 6（§1.1–§1.6，開場併入 §1.1） | 全閘完成 |
| Ch 2 | `chapter2-print-standalone.html` | 5（§2.1–§2.5） | 全閘完成 |
| Ch 3 | `chapter3-print-standalone.html` | 3（§3.1–§3.3） | 全閘完成 |
| Ch 4 | `chapter4-print-standalone.html` | 5（§4.1–§4.5） | 全閘完成 |
| Ch 5 | `chapter5-print-standalone.html` | 9（§5.1–§5.9） | M1 完成，M2–M5 待收 |
| App A–D | `appendixA..D-print-standalone.html` | 6／5／4／3 | 自撰服務性附錄 |

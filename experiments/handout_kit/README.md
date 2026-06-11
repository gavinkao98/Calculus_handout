# handout_kit —— 新排版規範（HTML kit）實驗

> 隔離實驗，`experiment/seed-converge` 分支。與 [`../seed_converge/`](../seed_converge/)、
> [`../direction_layer/`](../direction_layer/) 並列。**不碰** `chapters/*.tex`、正式 pipeline、
> 未 push 的 commit。

## 這資料夾是什麼

使用者第二次找人設計的**排版規範**——這次不是 LaTeX，而是一套 **HTML/CSS/JS handout kit**：
語意標記寫內容、`shared/` 引擎自動套樣式，同一份小節檔同時出**線上閱讀版**（可即時調樣式）與
**A4 列印版**（自動分頁、存 PDF）。本資料夾在隔離沙盒裡驗證它能不能用、好不好用。

## 哪些是 designer 的、哪些是實驗的

| | 檔 | 來源 |
|---|---|---|
| **designer 原樣** | `讀我-排版指南.md`、`template-screen.html`、`template-print.html`、`new-chapter-preview.html`、`shared/`、`new-chapter/`、`example-ch01/` | 解壓自 `latex.zip`，**未改動** |
| **寫作契約** | [`CONTRACT-html-writing.md`](CONTRACT-html-writing.md)、[`RESULT-s42-html-poc.md`](RESULT-s42-html-poc.md) | POC 驗證後制訂 |
| **standalone 產線** | `gen_standalone.py`、`chapter{1,2,3}-standalone.html`、`chapter{1,2,3}-print-standalone.html` | ch1 手工製作為範本；ch2/ch3 由 `gen_standalone.py` 從 ch1 範本生成 |
| **章節內容** | `exp-ch02/`（§2.1–§2.5 + figures.js）、`exp-ch03/`（§3.1–§3.3 + figures.js） | seed → direction → 六階收斂 |

> 舊的範本版 HTML（`chapter*-screen.html`、`chapter*-print.html`、`poc-*.html`）已移除，
> 統一使用 standalone 版。

## 跑到哪了（狀態）

1. **冒煙測試 ✅** — designer 附的 `example-ch01`（即現有 ch01 內容）螢幕＋列印兩版都正確渲染。
   證明引擎端到端可用。
2. **真內容壓測 ✅** — 把 §4.2（e^x 連續＋指數律，高風險證明節）**從 seed 直接生成** kit 的語意
   HTML（非轉 `.tex`），渲染兩版。**244 個 KaTeX、0 錯誤、8 頁 A4**。
   完整發現見 [`RESULT-s42-html-poc.md`](RESULT-s42-html-poc.md)。
3. **Standalone 化 ✅** — Ch 1–3 全部產出 standalone 版（MathJax 3、自帶 CSS/JS、零依賴），
   舊範本版 HTML 已移除。

權威產物：
- **[`CONTRACT-html-writing.md`](CONTRACT-html-writing.md)** —— 讓模型「直接生 HTML」要遵的寫作契約
  （`../seed_converge/rules.md` 的 HTML 版）。是把生成步驟接到這套 kit 的那根槓桿。
- **[`gen_standalone.py`](gen_standalone.py)** —— 從 ch1 範本自動生成各章 standalone HTML 的腳本。

## 怎麼渲染（零設定）

Standalone 版已把所有 CSS/JS/內容內嵌，**雙擊 HTML 檔用瀏覽器開就能看**（需連網載 MathJax CDN）。
不需要 HTTP server、不需要 `shared/`。

```powershell
# 重新生成（改了小節內容或 figures.js 之後）
cd handout_kit
python gen_standalone.py
```

> `_render/` 的 PNG 是可重生的截圖，已 `.gitignore`；`_render/shot.mjs` 工具有進版控。

## Standalone HTML（正式產物）

每一章產出兩個 standalone 檔：

| 檔案 | 用途 |
|---|---|
| `chapterN-standalone.html` | **螢幕閱讀版**：React + Babel 客端 JSX、MathJax 3、Tweaks 面板 |
| `chapterN-print-standalone.html` | **A4 列印版**：vanilla JS 分頁器、MathJax 3、Print 按鈕 |

### 產生方式

用 [`gen_standalone.py`](gen_standalone.py) 一次產生全部章節。
腳本以 `chapter1-standalone.html` / `chapter1-print-standalone.html` 為骨架範本，
把每章的 `<template>` 區塊、`figures.js`、`CHAPTER` 設定替換後寫出。

### 新增章節的步驟

1. **寫好小節 HTML**：在 `exp-chNN/` 下照 [`CONTRACT-html-writing.md`](CONTRACT-html-writing.md)
   撰寫 `sec-N-1.html`、`sec-N-2.html` ……
2. **寫好 figures.js**：在同一資料夾放 `figures.js`，匯出 `hydrateFigures()`。
3. **在 `gen_standalone.py` 加章節定義**：在 `CHAPTERS` dict 裡加一筆，填好：
   - `title_screen` / `title_print`：`<title>` 標籤內容
   - `brand`：螢幕版導覽列顯示的章名
   - `running_head`：列印版頁首的 running head
   - `dir`：該章資料夾名（如 `"exp-ch04"`）
   - `fragments`：小節檔名列表（不含 `.html`）
   - `fig_css_vars`：列印版圖片寬度 CSS 變數（`:root { --fig-N-M: ... }`）
4. **跑 `python gen_standalone.py`**，自動產生該章的螢幕版＋列印版。
5. **驗證**：用瀏覽器開檔確認——小節載入、數學式渲染（MathJax 3）、圖片 hydrate、
   螢幕版 Tweaks 面板、列印版 A4 分頁器皆正常。

### 現有章節

| 章 | 螢幕版 | 列印版 | 小節數 | 圖數 |
|---|---|---|---|---|
| Ch 1 | `chapter1-standalone.html` | `chapter1-print-standalone.html` | 8（含 intro + summary） | 11 |
| Ch 2 | `chapter2-standalone.html` | `chapter2-print-standalone.html` | 5（§2.1–§2.5） | 3 |
| Ch 3 | `chapter3-standalone.html` | `chapter3-print-standalone.html` | 4（opener + §3.1–§3.3） | 2 |

## 下一步（待使用者定）

見 [`RESULT-s42-html-poc.md`](RESULT-s42-html-poc.md) 末節：補編號／交叉引用 linter、
或把 HTML 草稿丟進既有的**訂閱制審查迴圈**閉環。

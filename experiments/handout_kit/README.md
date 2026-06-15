# handout_kit —— HTML 講義排版工具

> 隔離實驗，`experiment/seed-converge` 分支。

## 這資料夾是什麼

一套 **HTML/CSS/JS handout kit**：用語意標記寫內容，同一份小節檔同時產出
**螢幕閱讀版**（React + MathJax v4、可調樣式）與 **A4 列印版**（自動分頁、存 PDF）。

## 目錄結構

```
handout_kit/
  build.py                           # 組裝腳本（唯一建置工具）
  fragments/
    ch01/  (7 files: sec-intro … sec-1-6)
    ch02/  (5 files: sec-2-1 … sec-2-5)
    ch03/  (3 files: sec-3-1 … sec-3-3)
  chapter{1,2,3}-standalone.html     # 螢幕版（build 產出）
  chapter{1,2,3}-print-standalone.html  # 列印版（build 產出）
  _dev-archive/                      # 各章開發過程文件（seed / brief / audit 等）
  TYPESETTING_GUIDE.md               # 排版指南
```

## 架構

內容唯一存放在 `fragments/ch{N}/`，每個小節一個 HTML 檔（canonical = print 版格式）。

`build.py` 讀取 fragment，包進 `<template>` 標籤，插入各 standalone 檔的
`<!-- BEGIN-CONTENT-FRAGMENTS -->` / `<!-- END-CONTENT-FRAGMENTS -->` 標記區間。

- **Print 版**：fragment 原封不動插入。
- **Screen 版**：自動套用三項 transform 提升小螢幕可讀性：
  - `\frac` → `\dfrac`（僅 inline math `\(...\)` 內）
  - `\lim` 前補 `\displaystyle`（僅 inline math 內）
  - `\mathrm` → `\text`（僅 inline math 內）

Standalone 檔自帶全部 CSS/JS，**雙擊即開**（需連網載 MathJax v4 CDN）。
MathJax v4 啟用了 inline line-breaking（`linebreaks.inline: true`），
搭配 `text-align: justify` 可大幅改善行內公式造成的字距不均。

## 日常操作

```powershell
# 改完 fragment 後重新組裝（全部章節）
python build.py

# 只重建某一章
python build.py ch01

# 只重建某一章的某個版本
python build.py ch01 print
```

## 新增章節

1. 在 `fragments/ch{NN}/` 放好小節 HTML（照既有格式撰寫）。
2. 在 `build.py` 的 `CHAPTERS` dict 加一筆：

   ```python
   "ch04": {
       "fragments": ["sec-4-1", "sec-4-2", ...],
       "print": "chapter4-print-standalone.html",
       "screen": "chapter4-standalone.html",
   },
   ```

3. 準備兩個 standalone shell 檔（從既有章節複製，替換 chrome 設定，
   內容區留 `<!-- BEGIN-CONTENT-FRAGMENTS -->` / `<!-- END-CONTENT-FRAGMENTS -->` 標記）。
4. 跑 `python build.py ch04`。
5. 瀏覽器開檔驗證：數學式渲染、圖片 hydrate、分頁器皆正常。

## 現有章節

| 章 | 螢幕版 | 列印版 | 小節數 | 圖數 |
|---|---|---|---|---|
| Ch 1 | `chapter1-standalone.html` | `chapter1-print-standalone.html` | 7（intro + §1.1–§1.6） | 13 |
| Ch 2 | `chapter2-standalone.html` | `chapter2-print-standalone.html` | 5（§2.1–§2.5） | 3 |
| Ch 3 | `chapter3-standalone.html` | `chapter3-print-standalone.html` | 3（§3.1–§3.3） | 2 |

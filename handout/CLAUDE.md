# CLAUDE.md — handout 子目錄指引

本檔案補充根目錄 [`../CLAUDE.md`](../CLAUDE.md) 的專案層級指引，僅涵蓋 `handout/` 特有的架構約束。

## Fragment 架構：改課文一律改 fragment

課文內容存放在 `fragments/ch{NN}/sec-*.html`，由 `build.py` 組裝成 `chapter{N}-print-standalone.html`（列印版）。

**改課文（文字、公式、圖表 `<figure data-fig="…">`）時，一律編輯 `fragments/` 下的原始片段檔案，不要直接改 print-standalone HTML 的內容區塊。** 改完後執行 `python build.py` 重新組裝。

直接改 standalone 的內容區塊（`<!-- BEGIN-CONTENT-FRAGMENTS -->` 至 `<!-- END-CONTENT-FRAGMENTS -->`）會在下次 build 時被覆蓋。目前只維護 print 版（`chapter{N}-print-standalone.html`），螢幕版已移除。

## 圖表系統

- Fragment 放 `<figure class="figure" data-fig="id">` 標記。
- 對應的繪圖函數寫在 standalone HTML 的 `FIGS` 物件中（搜尋 `const FIGS`）。
- `hydrateFigures()` 在頁面載入時，把 `data-fig` 對應到 `FIGS` 函數，呼叫 `buildPlot()` 產生 SVG 並插入。
- **新增圖表需要改兩處：** fragment（加 `<figure>` 元素）和 print standalone（加 FIGS 函數）。

## Build 指令

```bash
python build.py              # 全部章節
python build.py ch01          # 只重建第一章
```

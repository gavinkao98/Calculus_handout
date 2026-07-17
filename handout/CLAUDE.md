# CLAUDE.md — handout 子目錄指引

本檔案補充根目錄 [`../CLAUDE.md`](../CLAUDE.md) 的專案層級指引，僅涵蓋 `handout/` 特有的架構約束。

內容撰寫規則（用語、密度、數學排版、圖表規範等）以 [`../CONTENT_SPEC.md`](../CONTENT_SPEC.md) 為準。

## 兩線結構（2026-07-17 重整）

- [`html/`](html/)＝**HTML 撰稿製作線**（工作線）：fragment 內容源、`build.py` 組裝、`standalone/` 列印版、`_render/` 自驗工具、`_audit/` rubric 與報告、`_dev-archive/` 歷史紀錄。
- [`latex/`](latex/)＝**LaTeX 出版排版線**（定稿轉換）：`convert.py` 確定性轉換、`template/calcbook.sty`、`chapters/<ch>/` 章節工作資產（DIALECT 方言凍結表等）、四閘驗收（見 [`latex/KICKOFF-latex-pilot.md`](latex/KICKOFF-latex-pilot.md)）。**成品在 `latex/dist/<ch>/`**——每單元恰兩檔（`<name>.pdf`＋自足 `<name>.tex`），由 `make_dist.py` 產生，勿手改；中間物一律不放 dist。
- 分工拍板（2026-07-17）：**整體先做 HTML 講義；定稿時把 HTML 轉成 LaTeX 出版**。fragment 仍是唯一內容源，`.tex` 是 build 產物（gitignored）、不是第二份源。

## Fragment 架構：改課文一律改 fragment

課文內容存放在 `html/fragments/ch{NN}/sec-*.html`，由 `html/build.py` 組裝成 `html/standalone/chapter{N}-print-standalone.html`（列印版）。

**改課文（文字、公式、圖表 `<figure data-fig="…">`）時，一律編輯 `html/fragments/` 下的原始片段檔案，不要直接改 print-standalone HTML 的內容區塊。** 改完後執行 `python html/build.py` 重新組裝。

直接改 standalone 的內容區塊（`<!-- BEGIN-CONTENT-FRAGMENTS -->` 至 `<!-- END-CONTENT-FRAGMENTS -->`）會在下次 build 時被覆蓋。目前只維護 print 版（`chapter{N}-print-standalone.html`），螢幕版已移除。

## 章節與小節結構：registry 為單一真實來源

- **fragment 順序只在 `html/build.py` 的 `CHAPTERS` registry 維護。** 新增/刪除一個小節、或新增一整章，只改 registry 一處；`build.py` 組裝時會自動把每個 standalone 裡分頁器用的 `CHAPTER.fragments` JS 陣列改寫成與 registry 一致（單一真實來源，兩份清單不會再各自漂移）。**不要手改 standalone 的 `CHAPTER.fragments`**——下次 build 會覆蓋。
- **章開場併入該章第一節的 fragment**（`sec-N-1.html`）：檔內第一個 `<article>` 為開場（`chapter-head` ＋ lead ＋「By the end of this chapter」清單），第二個 `<article>` 才是該節本身。**不設獨立的 `sec-intro` fragment**（四章一致；範例見 [`html/fragments/ch04/sec-4-1.html`](html/fragments/ch04/sec-4-1.html)）。開場/結尾的撰寫規範見 [`../CONTENT_SPEC.md`](../CONTENT_SPEC.md) §4 與 [`../CONTENT_QUICKSTART.md`](../CONTENT_QUICKSTART.md)。

## 圖表系統

- Fragment 放 `<figure class="figure" data-fig="id">` 標記。
- 對應的繪圖函數寫在 standalone HTML 的 `FIGS` 物件中（搜尋 `const FIGS`）。
- `hydrateFigures()` 在頁面載入時，把 `data-fig` 對應到 `FIGS` 函數，呼叫 `buildPlot()` 產生 SVG 並插入。
- **新增圖表需要改兩處：** fragment（加 `<figure>` 元素）和 print standalone（加 FIGS 函數）。

## Build 指令

```bash
python html/build.py              # 全部章節
python html/build.py ch01          # 只重建第一章
```

建好的 `html/standalone/chapter{N}-print-standalone.html` 直接用瀏覽器開啟即可預覽（純靜態 HTML，不需 dev server）。

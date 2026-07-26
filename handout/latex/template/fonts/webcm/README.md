# `template/fonts/webcm/` —— 字形閘的比對基準（非排版用）

這裡的字型**不參與 LaTeX 排版**（正文的 New Computer Modern 走 TeX 樹，見
`template/calcbook.sty`）。它們只是 [`../../check_glyphs.py`](../../check_glyphs.py)
驗證圖裡嵌入字形時的**原始字型基準**。

## 為什麼需要

圖是由 [`../../export_figs.mjs`](../../export_figs.mjs) 用 headless Chrome 把
`handout/html/standalone/` 的面板重繪成向量 PDF。面板上的襯線／數學標籤用的是 standalone
`@font-face` 宣告的 web 版 New Computer Modern（CDN `web-computer-modern` 套件），
Chrome 於是把**那份 web 字型的子集**嵌進圖 PDF，最後隨圖進到出版 PDF。

字形閘要比對「印出來的輪廓 vs 原字型同一 GID 的輪廓」，就必須拿得到那份 web 字型本身——
TeX 樹裡的 `NewCM10-Regular.otf` 不能當基準（**不同的字型檔**：web 版是 TrueType-flavored
的 `glyf` 輪廓，TeX 版是 CFF，兩者輪廓表示法不同、無法逐點比對）。

## 版本

`WebCM-Serif-10-Regular.woff2` 取自 standalone 所宣告的同一個 CDN 版本：

    https://cdn.jsdelivr.net/npm/web-computer-modern@1.1.0-new-cm-7-0-2/woff2/WebCM%20Serif%2010%20Regular.woff2

**檔名改成 PostScript name（`WebCM-Serif-10-Regular`）**，因為 `check_glyphs.py` 的
`find_original()` 以「PostScript name ＝ 檔名主幹」直接接檔（與 `../inter/` 同慣例）。

換 standalone 的 `@font-face` 版本時，這裡要同步換，否則字形閘會把版本差異報成輪廓不符。
目前只有 Regular 一個 face——ch04 的圖只用到它；別的 face 若被用到，字形閘會 fail-loud
指名缺哪一個（不會靜默略過）。

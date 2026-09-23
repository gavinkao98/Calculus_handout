# figkit —— JS 畫圖 kit（縮編後的圖工具）

> **這夾是什麼**：LaTeX 統一拍板（[`../latex/KICKOFF-latex-unification.md`](../latex/KICKOFF-latex-unification.md)
> U2）後，HTML 撰稿線退役，但全書 105 張圖仍由 standalone 內的 JS `FIGS` 函數繪製——本夾把圖繪製
> 從撰稿線抽離成獨立工具：**figs-only harness 頁**（每章一份、無課文），供既有兩個消費端照舊使用。

## 用法

```powershell
# 1. 生成 harness（從該章 print-standalone 變換；P1 全章建齊後 standalone 凍結）
python make_figs_page.py ../html/standalone/chapter3-print-standalone.html figs-ch03.html

# 2a. LaTeX 嵌圖：匯每 panel 一張向量 PDF（字體同源本地 Inter＋NewCM webfont）
node ../latex/export_figs.mjs figs-ch03.html ../latex/chapters/ch03/figs

# 2b. 圖閘 render：逐圖 2× PNG 餵 handout-figure-audit
node ../html/_render/shot.mjs figs-ch03.html <out/prefix> figures
```

## 檔案

| 檔 | 說明 |
|---|---|
| `make_figs_page.py` | harness 生成器：standalone → figs-only 頁（保留全部 head/CSS/MathJax/`FIGS`/hydrate，內容區換 figure 空殼、paginator 換簡化 boot；`#boot` 移除語義不變，消費端免改） |
| `figs-ch03.html` | ch03 harness（P0 pilot，2026-08-09；驗收＝重匯 8 panel 字型/尺寸與正統路徑一致、字形閘 PASS） |

## 已知事項（P0 pilot 實測）

- **量測寬度僅供新圖初值**：`figures.json` 的 mm 是 harness 量測值；**已有圖的權威寬度寫死在
  `latex/src/<ch>/*.tex` 的 `\includegraphics[width=…]`**，重匯不改變成品。已知差異一例：ch03
  `sin-cos-slope` 在 harness 量 89.42mm、成品用 55.07mm——正統路徑的 55mm 來自 HTML paginator 的
  fit-scaling（`FIG_MIN_SCALE` zoom，塞頁尾的偶然），兩版 PDF 長寬比一致、向量縮放無損，`.tex`
  的 width 固定即視覺不變。
- **匯出圖 PDF 不進版控**（`.gitignore` 的 `handout/latex/chapters/*/figs/`）：可重現中間物，
  換機後用上述指令重匯即可；**pull 進別台改過的 `figs-<ch>.html` 後也要重匯**（`build.py` 不比
  新鮮度，本機舊圖會照樣編進有版控的 dist PDF）。`figures.json` 同在 `figs/` 下、一併不進版控（mm 僅供新圖初值，
  隨重匯重生）。
- `export_figs.mjs` 的 FILE_PORT 已避開 Chrome restricted port（2026-08-09 實測 10080＝
  `ERR_UNSAFE_PORT` 會把錯誤頁印成「圖」；已加 location.href 斷言 fail-loud）。

# 影片模板系統設計畫布 — 工作檔

> 2026-09-12（品質補強輪 ⑨）。這裡是**設計畫布的源**，不是成品。
> 裁決與依據見 [`../../REBUILD_STATUS.md`](../../REBUILD_STATUS.md) 品質補強輪 ⑨；
> 未竟項見 [`../../KICKOFF-s31-amplify.md`](../../KICKOFF-s31-amplify.md) §7.1。

**已發布的畫布：** <https://claude.ai/code/artifact/b6bbb677-135e-48fc-8d0d-9ff13cca05ca>

## 這是什麼

2026-09-12 使用者問「模板當初設計沒特別考慮，要不要用 Claude Design 重新設計一次」，
並要求先看過定稿講義再給意見。盤點全書 12 章後產出的設計畫布，3 頁 9 個 artboard：

| 頁 | artboard | 內容 |
|---|---|---|
| 依據與模板集 | `Main.dc.html` | 內容型別盤點：全書 935 個語意塊 × 現有 12 模板的覆蓋矩陣（**39%**） |
| | `TemplateSet.dc.html` | 新模板集合提案：13 個而非 20 個（語意從模板抽出來當參數），覆蓋率 39%→89% |
| 識別方向 | `Palettes.dc.html` | 三方向的色盤與字體，軸＝「影片與講義的關係」 |
| | `DirectionA/B/C.dc.html` | 同語／對位／分工，**同一場**（§3.1 Proposition 3.1）三種識別 |
| 排版規範 | `LayoutRules.dc.html` | 版面構成 4 條規則（含現況 before/after） |
| | `MathRules.dc.html` | 數學排版 5 條規則 |
| | `WorkedExample.dc.html` | `worked_example` 新模板 mockup（全書 220 單元、最大缺口） |

**使用者裁決＝方向 B「對位」**，已落地到 `theme.py`／`blocks.py`／模板層
（commit `de3004c`）。**版面 4 條、數學 5 條、`worked_example` 模板、字體都還沒做**
（KICKOFF §7.1）。

## 為什麼只有工作檔、沒有成品

發布用的 `video-template-system.html` 是 **2.5 MB**（內含整個畫布編輯器），
而且可以從這些工作檔重生 —— 照 [`../../README.md`](../../README.md)
「可重生的成品不進版控」，故不追蹤。這 10 個檔是**人寫的源**，加起來 100 KB。

## 怎麼改、怎麼重新發布

1. 在新對話裡跑 `/design`（把 skill 的 base directory 重新解出來——那是帶版號的暫存路徑，
   每次不同，不能寫死）。
2. 改這裡的 `.dc.html`／`canvas.json`。
3. 用 skill 的 `seed-canvas.mjs` 重新 seed 一份成品，再用 `Artifact` 工具**帶上面那個 URL**
   發布回同一個畫布（不帶 URL 會另開一個新的）。

> **注意：** 使用者若在畫布上自己編輯過並存檔，線上版就比這裡新。改之前先
> `action: "read"` 把線上版讀回來、`--extract` 解成工作檔，在那個基礎上改，
> 不要直接拿這裡的舊檔覆蓋掉別人的編輯。

## 已知限制（寫在設計本身裡的）

畫布是 HTML/CSS，數學是**手工排的**（CSP 擋外部 script，沒有 KaTeX）。跟 pdflatex 的
Latin Modern **字度量不同**，所以這份是**規範**不是像素預覽：規則層（層級、混排、佔比）
可以直接搬，行距數值落地時要重測。

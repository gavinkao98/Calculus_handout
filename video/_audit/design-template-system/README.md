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
（commit `de3004c`）。四項未竟項**全部落地**（2026-09-14 更新；契約與驗收＝
[`../../KICKOFF-shared-layer-v1.md`](../../KICKOFF-shared-layer-v1.md)，
進度紀錄＝[`../../REBUILD_STATUS.md`](../../REBUILD_STATUS.md)「工具線・共用層 v1 凍結」）：

| 項目 | 狀態 |
|---|---|
| **`worked_example` 模板**（`WorkedExample.dc.html`） | ✅ **已落地**（commit `c79372c`，2026-09-13 併入 main；2026-09-14 對 v1 字體字級回歸 `50bf2fa`）。契約與兩處刻意偏離 mockup 見 [`../../KICKOFF-worked-example-template.md`](../../KICKOFF-worked-example-template.md)，驗收報告 [`../REVIEW-worked-example-template-applied.html`](../REVIEW-worked-example-template-applied.html) |
| **版面 4 條規則**（`LayoutRules.dc.html`）能自動的寫進 `sizecheck` | ✅ **已落地**（commit `8a81530`，2026-09-14 併入 main）。L1／L2／L3 三條落成 `sizecheck` 規則、**全部 warn-default**（`meta.layout_enforce` 開才升 error）；**L4 判「只能人審」**（見下方已知限制）。契約見 [`../../REVIEW_GATES.md`](../../REVIEW_GATES.md) §一 層 6 與 [`../../DESIGN.md`](../../DESIGN.md) §設計系統規則落地 |
| **數學排版 5 條**（`MathRules.dc.html`）＝數學字級收成三階 | ✅ **已落地**（字級三階 commit `f2b0813`、M1–M3 規則 commit `8a81530`，2026-09-14 併入 main）。`math_conclusion 62`／`math 48`／`math_rail 34`，**`math_sm 40` 已刪除不留 alias**；M1／M2／M3 落成 `sizecheck` 規則（`meta.mathtype_enforce`）；**M4（∎）判「只能人審」**、M5 由 `_selftest_type_scale` 覆蓋 |
| **字體**（Instrument Sans） | ✅ **已落地**（commit `74b88ca`，2026-09-14 併入 main；使用者 T1-5 人閘 **go**）。OTF＋`autoinst` 生成的 pdflatex 支援 vendored 在 `video/pipeline/fonts/instrument-sans/`（本機無 CTAN pdflatex 套件）；換機設定與排查見 [`../../../ENVIRONMENT.md`](../../../ENVIRONMENT.md) ③／①b |

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

**落地後查到的五條落差（2026-09-14 補；畫布與 code 的差異，不是畫布的錯）：**

- **數學字體維持 Latin Modern，畫布的 mockup 用的是 Source Serif 4**（`DirectionB.dc.html:12,14`
  文字 Instrument Sans／數學 Source Serif 4）。**使用者 T1-0 裁決只換文字、數學不換**——
  `theme.PX_TO_FS` 是以數學為錨的換算常數，換數學字體會連帶動所有版面 zone，且 `lmodern` 在 preamble 標了 locked。
- **Instrument Sans 的 Medium（500）未 vendoring。** `autoinst` 沒有 500 的 NFSS 權重碼收不進來，
  且現役 code 只用到 upright regular 與 bold；畫布若用了 Medium 字重，落地會退到 Regular 或 SemiBold。
- **`=` 對齊欄未做。** `WorkedExample.dc.html` 的步驟鏈是等號對齊的，落地一律左齊 `SPINE_X`
  （`KICKOFF-worked-example-template.md` D3：`=` 對齊要嘛動 `sizecheck` 的分欄影響既有 deck、
  要嘛塞看不見的幾何進列而被 `paced` 當一段走）。
- **L4 的 `layout:` 宣告欄位未做。** `LayoutRules.dc.html` 的三種佔比（`single`／`major_minor`／`figure_led`）
  是 authoring 選擇不是幾何事實，storyboard **目前沒有這個欄位**，所以「宣告了就要跟宣告一致」這條也無從查起；
  歸 VISUAL-FRAME 的 A1／A7 人審。
- **M4「∎ 是字形不是元件」未做。** `brand.glyph("qed")` 現在仍渲成綠色圓角方框；
  這是視覺做法問題、不是可量的幾何，歸 VISUAL-FRAME 的 A2／A4 人審。

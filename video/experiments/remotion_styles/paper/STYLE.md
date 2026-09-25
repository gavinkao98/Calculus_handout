# 紙本編輯排版（`paper`）

**概念：** 畫面就是一頁印好的教科書，鏡頭是架在紙上的翻拍台（rostrum camera）。暖米色紙張帶靜態纖維紋理，墨黑細線，EB Garamond 襯線字（追蹤過的小型大寫作書眉與圖號、斜體作圖說）加 MathJax Pagella 數學；版面走 Tufte 式左側旁註欄＋主欄格線，Tufte range-frame 座標軸、圖號（Figure 3.3）、式號（3.3）、booktabs 表格、腳註編號都是真的排版元件。動態的語彙全部從「印刷」來：線條像筆尖上墨（有筆頭墨點）、文字以左→右的墨跡遮罩「排上去」、標註字沿著切線刻印、鏡頭推拉就是把紙整張搬到鏡頭下（紙紋跟著移動）。唯一的強調色是品牌深紅（紅字 rubric），所以 logo 與版面是同一套色。

## Token（`src/theme.ts`）

| 類別 | 名稱 | 值 |
|---|---|---|
| 紙 | `paper` / `paperShade` | `#F4EFE4` / `#E9E1CF` |
| 墨 | `ink` / `ink2` / `ink3` / `rule` | `#1F1B16` / `#5A5249` / `#948A7C` / `#C9BFAD` |
| 強調（導數、切線） | `accent` | `#BA0C2F`（＝品牌 crimson） |
| 語意 | sin / cos / derivative / tangent | `ink` / `#1F5E9E`（藍鉛筆）/ `accent` / `accent` |
| 字型 | 內文、標題、小型大寫 | EB Garamond 400/500/600＋斜體（@fontsource，OFL，打包進 bundle） |
| 字型 | 數學 | MathJax 4 SVG＋Pagella，`mathScale 0.9` 對齊 Garamond x-height |
| 字級（px@1080p） | display / title / h2 / formula / body / caption / label / smallCaps | 300 / 104 / 64 / 112 / 40 / 31 / 29 / 21（大寫＋0.18em 字距） |
| 格線 | 邊界 / 旁註欄 / 主欄 | 120 / x120 w280 / x460 w1340；書眉基線 74、書眉線 94 |
| 線寬 | hairline / axis / curve / tangent / emphasis | 1.5 / 1.8 / 4.2 / 3.4 / 5 |
| 緩動 | ink / camera / out | bezier(.3,0,.12,1) / (.65,0,.3,1) / (.16,1,.3,1) |
| 彈簧 | tangent / token / pop | damping 11·stiff 150·mass .7 / 15·120·.9 / 13·180·.6 |

色彩檢核：crimson↔cobalt 以 dataviz validator 在紙色上通過（CVD ΔE 18.0、一般 ΔE 28.9、對比 ≥3:1）；墨黑是刻意的「文字墨」中性色，不算類別色（validator 對它的亮度帶／彩度警告屬預期）。

## 元件（`src/components/`）

- `Shell.tsx`：`Page`（紙＋書眉＋頁碼＋品牌 device）、`SceneShell`（整幀）、`Camera`（cx, cy, s；對數空間插值縮放）、`BrandIcon`／`BrandLockup`（原檔 SVG，不改色）。
- `Paper.tsx`：確定性種子產生的紙紋 tile＋大尺度斑駁；`Vignette` 固定在螢幕上（燈光，不隨紙動）。
- `Formula.tsx`：token 化排版（TeX 片段或 Garamond 字詞，各帶 `key`），同步版面計算；`FormulaG`、`AlignedEq`（以等號對齊）、`FormulaMorph`（共用 key 以彈簧滑行、左移者上拱右移者下潛兩條車道、不同內容飛行中交叉淡化、可指定出發順序）。
- `Plot.tsx`：`PlotFrame`、`RangeAxes`、`Curve`（筆頭上墨）、`Tangent`（彈簧長出）、`TangentNote`（沿切線刻字）、`SlopeTriangle`、`Dot`（紙色描邊環）、`Label`；`.halo` 紙色鏤空讓標籤壓在線上仍可讀。
- `Type.tsx`／`Marginalia.tsx`：`SmallCaps`、`Rule`（由左畫出）、`InkReveal`、`InlineTex`、`Para`、`FigureCaption`、`Sidenote`、`NoteRef`、`EqNumber`。
- 場景：`scenes/F0Title` `F1Theorem` `F2Slope` `F3Cycle` `MotionTest`；共用 token 清單在 `src/content.ts`。

指令：`npm ci` → `npm run stills`（4 張 PNG 到 `out/frames/`）、`npm run motion`（`out/motion_test.mp4`，本機 bundle＋render 約 20 秒）、`npx remotion studio` 預覽。

## 做成整幕的下一步

1. 把「一頁」升格為版型：節首頁（F0）、定理頁（F1）、圖版頁（F2/F3）、跨頁（motion test 的 2400×1350 spread）四種 `Page` 預設，場景只填內容。
2. 翻頁轉場：紙張沿書口微捲翻過（或鏡頭橫移到下一個跨頁），取代淡入淡出。
3. 旁白同步：`InkReveal` 與 token morph 接 beats 時鐘；圖說與旁註可直接吃 storyboard 文字。
4. 補 `\cssId` 式 token 標註，讓整條 TeX 也能拆 token（目前 token 需手動切）。
5. 加一套深色「夜讀」變體（同 token 結構，換紙與墨）以備需要。

## 誠實的弱點

- **安靜。** 米色＋細線在手機小螢幕、或和 3B1B 式高對比片並排時顯得低能量；刻意的留白有時會被讀成「空」。
- **細字在影片壓縮下吃虧。** 1.5px 髮絲線、小型大寫書眉（約 16px@0.8 縮放）在低碼率串流會糊；紙紋雜訊也讓檔案變大（15 秒 crf16 約 42 MB）。
- **小型大寫是「假」的。** @fontsource 的 EB Garamond 沒有 `smcp`，目前用縮小大寫＋字距模擬，筆畫比真小型大寫細。
- **Pagella 數學＋Garamond 內文**是兩個家族，x-height 用 `mathScale` 對過，但混排的行內數學仍略重。
- 「書」的隱喻很強，若整部片都是頁面，長時間可能單調；需要翻頁與跨頁版型變化來撐節奏。

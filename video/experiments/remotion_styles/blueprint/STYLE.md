# 藍圖工程（`blueprint`）風格說明

**概念：** 每一場都是一張「會自己畫出來的工程圖」。深普魯士藍圖紙上有隨鏡頭縮放的世界格線，外圍是固定的雙線圖框、分區編號（1–8／A–D）與下緣標題列；數學物件用製圖語彙交代：函數＝輪廓線、切線與導數＝唯一的琥珀亮色、斜率三角＝尺寸線、點與點的對應＝一長一短的投影中心線、項目＝編號氣球、負號函數＝隱藏線（虛線）。上下兩個視圖（sin 在上、cos 在下）用正投影排列，「sin 的斜率＝cos 的高度」直接變成同一條鉛直投影線上的兩段等長線。品牌 lockup 住在右下角的 title block 裡，片尾由 title block「簽核」收束。

## Token（`src/theme.ts`）

| 類別 | 名稱 | 值 |
|---|---|---|
| 底色 | `paper` / `paperLift` / `paperDeep` | `#0B2446` / `#133563`（暈影中心）/ `#061934`（邊緣） |
| 格線 | `gridMinor` / `gridMajor` | `rgba(150,190,255,.075)` / `.16`（1/4 單位細格、1 單位粗格；推近時淡入 1/8 格） |
| 墨色 | `ink` / `ink2` / `ink3` | `#F2F6FC` / `#B4C8E4` / `#7C97BE` |
| 語意 | `sin` / `cos` / `derivative`＝`tangent` | `#F2F6FC`（白墨）/ `#5CC8F2`（青藍）/ `#FFAE3A`（琥珀，全片唯一亮色） |
| 負號函數 | `negDash` | 同家族色＋`14 10` 虛線（隱藏線慣例） |
| 字型 | display / text / mono / math | Barlow Condensed（300/500/600）/ Barlow / IBM Plex Mono / KaTeX（皆本地 npm 套件，OFL） |
| 字級 px | hero / h1 / h2 / mathLg / math / body / label / note / micro | 138 / 92 / 60 / 112 / 84 / 40 / 28 / 24 / 17 |
| 線寬 px | object / tangent / axis / thin / hair | 4 / 3 / 2 / 1.35 / 1 |
| 虛線 | hidden / center / construction | `14 10` / `26 7 4 7` / `3 6` |
| 時長（幀@30） | fast / base / slow | 10 / 18 / 34 |
| easing | draft（筆畫）/ camera / settle | `bezier(.6,.05,.3,1)` / `bezier(.65,0,.25,1)` / `bezier(.16,1,.3,1)` |
| spring | springy（切線彈入，一次回彈）/ soft | `damping 11, stiffness 170, mass .9` / `damping 200` |

色盤用 dataviz validator 驗過（dark、surface `#0B2446`、all pairs）：CVD ΔE ≥ 16、一般視覺 ΔE ≥ 21、對比全過；「白墨彩度過低」是刻意的（白是底稿墨色，不是類別色），另以線型＋直接標籤做第二編碼。

## 元件

- `Sheet`（SceneShell）：紙面暈影＋纖維雜訊、`WorldGrid`（隨鏡頭）、內框裁切、`TitleStrip`（icon bug＋節名＋比例＋張次）、`overlay` 層、雙線圖框與分區編號。
- `TitleBlock`：右下 title block，放 `lockup-white.svg`；`reveal` 讓底板擦出、表格線依序畫出（片尾簽核）。
- `lib/view.tsx`：`View`／`project`／`cameraAt`（關鍵幀＋對數縮放插值）＝鏡頭推拉平移；所有幾何在 JS 端投影，推近時線寬、字級不變。
- `Plot.tsx`：`Axes`（軸與刻度隨描繪出現）、`FunctionPlot`（截斷定義域的 draw-on，虛線不亂）、`Tangent`（可吃 spring 超過 1 的彈性長度）、`SlopeTriangle`、`ProjectionLine`、`Node`。
- `Draft.tsx`：`Arrowhead`（3:1 細長箭頭）、`DimensionLine`（延伸線＋中斷處水平讀數）、`Callout`（引線＋擱板）、`Balloon`、`Reticle`（繪圖頭＋座標讀數）、`CornerFrame`。
- `MathTex.tsx`：`Tex`／`MathAt`、`Formula`（token 排版並回報每個 token 的方框，供引線對位）、`TokenMorph`（同 id 滑行帶弧、內容不同者交叉淡化、無對應者淡出／淡入）。
- `scenes/slopeRig.tsx`：「斜率＝高度」探針（F2 與動態測試共用）。

## 指令

`npm ci` → `npm run stills`（四張 PNG）／`npm run motion`（`out/motion_test.mp4`，h264 CRF 16）／`node render-stills.mjs --frames 60,150`（抽動態測試單幀檢查）。本機 450 幀 1080p30 牆鐘時間約 14–22 秒（含 bundle）。

## 做完整一幕的下一步

1. 把 `MotionTest` 的時間表抽成 beat 資料（對齊旁白時鐘），每個 beat 只宣告「畫哪個零件、鏡頭去哪」。
2. 補轉場：用 title block／分區編號當「翻到下一張圖」的換場（圖號 02→03 的翻頁或向下平移到下一張圖紙）。
3. `derivative_cycle` 做成動態：四個 VIEW 依序以 draw-on 出現，d/dx 弧箭頭順時針逐段畫出，第四段回到起點時整圈亮一次。
4. 公式也走製圖語彙：token 變形時從來源 token 拉一條投影線到目標位置，而不是只滑行。

## 誠實的弱點

- 圖框、分區、標題列這層「製圖外框」固定吃掉約 7% 畫面，內容區較 3Blue1Brown 式滿版小；長片可能嫌重複，需要在內容場降低外框存在感（例如只留內框）。
- KaTeX 的 Computer Modern 與 Barlow Condensed 並置時有兩種字體語氣；目前靠「數學一律 KaTeX、敘述一律 Barlow」切分，混排的標題（如 F2）改用 display 字寫函數名，嚴格說不是數學排版。
- 白墨＋青藍＋琥珀三色之外沒有餘裕：若一場需要第四個語意（例如二階導數），只能靠線型或透明度，不能再加色。
- 深藍底上細線（1–1.35 px 尺寸線、格線）在 YouTube 低碼率下可能糊掉；正式片應把 thin 提到 1.6 px 左右並實測壓縮後效果。
- TokenMorph 目前是 token 中心滑行＋交叉淡化，不是字形輪廓變形；`slope of` → `d/dx` 這種形狀差很大的配對仍是「淡出換淡入」。

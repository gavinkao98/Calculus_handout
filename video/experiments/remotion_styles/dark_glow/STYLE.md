# dark_glow「Nocturne」：深色極簡發光

**概念。** 夜裡的觀測台：深藍黑的夜空底上，函數是一條自己會發光的光絲。每條光絲是近白的細芯，外面包著自己顏色的光暈；切線是一道暖白的光刃。關鍵點是一顆四角星，取自 logo 上那顆星的幾何。文字刻意克制：片名用電影片名感的 Cormorant Garamond，數學用 Pagella（Palatino 系，避開 3B1B 的 Computer Modern），讀數與眉標用 DM Mono 大寫加寬字距，像儀器上的刻字。畫面只放一個主角，四周留大片黑。

## Token（`src/theme.ts`）

| 類別 | 名稱 | 值 |
|---|---|---|
| 底色 | `bg`／`bgLift`（焦點微光） | `#07080C`／`#141A2A` |
| 文字 | `ink`／`ink2`／`ink3` | `#EEEAE2`／`#A8A59D`／`#6B6964` |
| sin（ember） | `sin`／芯 `sinCore` | `#FF8676`／`#FFD9D0` |
| cos（lumen） | `cos`／芯 `cosCore` | `#8C9EFF`／`#DCE2FF` |
| 導數 d/dx、斜率 | `deriv`／`derivCore` | `#E4CF8C`／`#FFF3D6` |
| 切線（光刃） | `tangent` | `#FFF2DE` |
| 字型 | 片名／讀數數字；數學；眉標與標籤 | Cormorant Garamond 400–500（含斜體）；MathJax 4 + Pagella；DM Mono 300–400 |
| 字級 px | display／title／lead／eyebrow／readout | 124／64／46／22（字距 0.34em）／44–56 |
| 數學字級 px | XL／L／M／S／刻度 | 128／96／68／48／34 |
| 間距 | s1…s7；安全區 | 8／16／24／40／64／104／168；左右 128、上 104、下 96 |
| 發光 | bloom／halo／core | 寬 20 模糊 20 不透明 .26／寬 7 模糊 5 不透明 .6／芯 2.8px |
| 緩動 | glide／camera／draw／slide | bezier(.16,1,.3,1)／(.6,0,.25,1)／(.45,.05,.2,1)／(.5,0,.5,1) |
| 彈簧 | pop／settle／morph | damping 11 stiffness 150 mass .7／22·110·1／16·90·1 |

配色已用 dataviz 的 `validate_palette.js` 檢查（對 `#07080C`，all pairs）：CVD 最差 ΔE 10.0、常態視覺最差 ΔE 17.2，兩項都通過。亮度帶檢查刻意不過：這三個顏色是發光筆畫，不是圖表填色，所以比圖表建議的亮度帶亮。

## 元件（`src/components/`）

- `SceneShell`：夜空底（焦點微光、暗角、每 2 幀換種子的細顆粒，用來防止暗部色帶）、全畫面 Stage SVG、HTML 疊層、右下角品牌角標（`icon-white`）
- `Glow`：`GlowDefs`（濾鏡蓋滿全畫面，避免水平切線因外框高度為 0 而消失）、`GlowPath`（三層發光）、`Sparkle`（四角星）、`FadeMask`
- `Camera`：世界座標到畫面 px 的映射，不是 CSS scale，所以推拉時線寬、光暈、字級都不變；zoom 用對數內插
- `Plot`：`Axes`（髮絲軸，兩端淡出）、`FunctionPlot`（依 x 描出，筆頭帶星光）、`Tangent`
- `MathTex`：建置期 MathJax 產生的 SVG；可用 `\class{tok-KEY}` 定址 token，上色、單獨顯示、依 token 對齊（例如以 `=` 對齊）
- `MorphTex`：token 級公式變形。配對的 token 用彈簧滑行並交叉淡化，沒配對的 token 淡出或淡入；token 外框在建置期由字形路徑算好，執行時不量 DOM
- `Type`：`Eyebrow`、`Title`、`GlowWord`、`Readout`（標籤用 DM Mono；數字用 Cormorant 的 lining＋tabular 數字，因為 DM Mono 的 0 帶斜線，在數學畫面上會被讀成 ∅）、`Connector`
- `Cycle`：`CycleRing`（軌道、漸層弧、箭頭，加上沿軌道走的彗星）
- `Logo`：原樣 inline `video/pipeline/assets/brand/*-white.svg`

## 建置

`npm ci` → `npm run prebuild`（TeX 與 logo 轉成 `src/**/generated.ts`）→ `npm run stills`／`npm run motion`。1080p30 的 15 秒動態測試在本機約需 62–70 秒（Windows，Remotion 預設併發）。

## 若選這個方向，做完整一幕的下一步

1. 把 MotionTest 的節拍拆成 `Scene` 元件，每個 beat 都綁旁白時間碼；加入轉場元件（光絲收束成一個點再炸開成下一場的主角）。
2. `MorphTex` 補上多行推導（`align` 以 `=` 對齊列）與「框住」強調（光暈脈衝，取代方框）。
3. 做節標題卡的進場（logo 星光→光絲描出→片名淡入）與片尾（lockup 收尾）。
4. `Readout` 加上數字滾動的彈簧，`Tangent` 加上移動時的速度拖尾（motion blur）。

## 誠實的弱點

- **光暈昂貴、也吃壓縮**：H.264 在暗部漸層與模糊光暈上容易出現色帶與方塊（目前用顆粒和 CRF 16 壓住，檔案因此偏大，15 秒約 13 MB）；上傳平台再壓一次可能會變髒。
- **暗色投影／明亮教室不友善**：近黑底在投影機上會變灰，細髮絲軸與 `ink3` 註記可能看不見。
- **發光本身會變成語彙疲勞**：一幕 10 分鐘全都在發光，容易顯得單調或「霓虹」。需要紀律，只讓主角發光，配角降成 `strength` 0.4 左右。
- **襯線＋深底的小字**：Cormorant 細筆畫在 1080p 經壓縮後，小於約 36px 就會發虛，所以讀數與說明不能再縮小。
- **與 3B1B 仍有家族相似**：深底配彩色曲線的大框架相同；區隔靠字型、光絲芯＋光暈、星形語彙與儀器式讀數。如果使用者要更遠離，得改底色（例如深墨綠）或構圖。
- 公式變形的交叉淡化在字形不同的配對（slope of → d/dx）上，是溶接而不是真正的路徑變形；需要時可再引入 flubber。

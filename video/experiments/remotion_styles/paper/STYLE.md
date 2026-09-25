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
| 字級（px@1080p，鏡頭縮放前） | display / title / h2 / formula / proof / body / caption / label / smallCaps / micro | 300 / 108 / 64 / 112 / 70 / 44 / 36 / 34 / 28 / 28（第三幕起：凡要讀的字 ≥ 28，見下「字級下限」） |
| 格線 | 邊界 / 旁註欄 / 主欄 | 120 / x120 w280 / x460 w1340；書眉基線 74、書眉線 94 |
| 線寬 | hairline / axis / curve / tangent / emphasis | 1.5 / 1.8 / 4.2 / 3.4 / 5 |
| 緩動 | ink / camera / out | bezier(.3,0,.12,1) / (.65,0,.3,1) / (.16,1,.3,1) |
| 彈簧 | tangent / token / pop | damping 11·stiff 150·mass .7 / 15·120·.9 / 13·180·.6 |

色彩檢核：crimson↔cobalt 以 dataviz validator 在紙色上通過（CVD ΔE 18.0、一般 ΔE 28.9、對比 ≥3:1）；墨黑是刻意的「文字墨」中性色，不算類別色（validator 對它的亮度帶／彩度警告屬預期）。

## 字級下限（第三幕起，模板規則）

- **畫面上任何要讀的字 ≥ 28 px（1080p）＝ token 字級 × 當下鏡頭倍率。** token 表的最小值就是 28，所以只要鏡頭 s ≥ 1 一律安全；s < 1 的鏡頭（例如跨頁全景 s≈0.52）只能用在「焦點是大字」的時刻，其餘內容要罩紙色薄紗（`Spread veil`）退成背景，不能讓小字當焦點。
- 證明列 70（實際 66）、旁註數學 42、刻度與讀數 34、圖說 36、書眉小型大寫 28；鏡頭推近時（s 1.2–1.75）這些字在螢幕上是 45–120 px。
- 手機實測標準：把 1080p 幀縮到 390 px 寬時，28 px 的字約 10 px 高——仍可辨識；再小就不行。

## 版型（第三幕的五種頁）

| 版型 | 用在 | 要點 |
|---|---|---|
| 節首頁 | `intro` | 左大章號＋花飾（活切線），右標題＋問句＋目錄（40 px、點狀引導線、頁碼）；頁腳 lockup。冷開場貼近花飾，拉遠揭露整頁。 |
| 定理頁（verso／recto） | `derivative_of_sine`、`derivative_of_cosine` | 旁註欄在**外側**（左頁在左、右頁在右）：定理標籤＋rubric 豎線、sum-to-product 旁註；主欄：定理式（104）、*Proof.*、證明列（66）、極限箭頭與註、結論列＋∎。版面在 `src/act3/ProofPage.tsx`，兩頁共用、只換 variant。 |
| 跨頁（書攤在桌上） | `derivative_of_cosine` 的 `compare` | 兩頁並排、書溝陰影、書的投影、深色桌面 `#2F2A24`；鏡頭可以拉離紙面到 s≈0.5。 |
| 全幅圖版頁 | `slope_equals_height` | 頁面比畫面寬（2700 px）：圖占滿左邊一個畫面寬，右側欄（圖說、In words／In symbols、式號）先在畫面外，鏡頭橫移過去才出現。 |
| 表格頁 | `derivative_cycle` | booktabs 三線表（粗 2.6／細 1.4），列隨旁白排入；表格內容可以飛出成為別的圖（導數環）。 |
| 收尾頁 | `outro` | 全片唯一置中排版：END OF SECTION、Next、§3.2 標題、置中 lockup。 |

## 轉場與鏡頭（第三幕起）

- **翻頁**（`src/act3/PageTurn.tsx`）：前一場最後 28 幀＝一張以左緣（書脊）為軸、`perspective(3200px) rotateY(0→−96°)` 翻起的紙；翻起時受光、過 90° 前轉暗，下一頁上有一道隨紙移動的陰影。兩場在時間軸上重疊 28 幀（`TURN`），前一場畫在上層。
- **滑到對頁**（`derivative_of_sine → derivative_of_cosine`）：不剪接。下一場的第一幀就是上一場的最後一幀（左頁以「時鐘超過結尾」的方式重現，所有筆畫都已定格），鏡頭再越過書溝橫移到右頁。
- **鏡頭**：`camPath(frame, start, bounds, moves)`——一串「在第 f 幀出發、len 幀後到達」的移動，對數空間縮放、`ease.camera`；`keepOnPage` 會在畫面小於紙面的軸上把鏡頭夾在紙內（不露桌面），刻意拉離紙面（畫面比紙大）時才放行。
- **禁止長靜止**：每拍都有東西在動（墨跡、token 滑行、切線滑動、筆尖繞環），但「動」指內容在動，**不是鏡頭在動**（見下節）。

## 鏡頭紀律（2026-09-25 使用者裁決，模板規則；取代舊的「每場至少推近一次、焦點隨拍移動」）

使用者看過 §3.1 後的判定：平移、聚焦用得太多，推導時鏡頭一直動，觀眾會忘記前面的式子，版面也失衡。

1. **推導時鏡頭鎖定。** 一段推導從第一列到最後一列鏡頭不動，前面的列全部留在畫面上，新列往下接。空間不夠時事先規劃版面（縮排、分欄、把已用完的列收成一行摘要），不能靠平移追著新列走。
2. **強調不用鏡頭。** 要指出某一項，用變色、底線、框選、其餘部分淡化，不用推近。
3. **鏡頭只在換區塊時動。** 例如圖 ↔ 文、換頁、進入新的圖版。一場最多兩次，而且不在書寫或變形進行中移動。
4. **推近要克制。** 一般的構圖縮放在 1.0–1.15 之間；超過 1.15 的推近全片只保留給少數幾個主角瞬間，而且要推得回來。
5. **靜止構圖要平衡。** 鏡頭停下來的位置要落在版面網格上，主要內容大致置中、左右留白相當，不能停在偏一邊的位置。
6. **推近時不可裁到正在閱讀的字。** 頁眉、旁註若會被畫面邊緣切到，就讓它們先淡出，或乾脆不推。

## 公式排版（2026-09-25 模板規則，比照講義慣例）

1. **主角公式一律行間（display）**：推導列、定理、框起來的結果。
2. **旁註、說明、表格裡的公式一律行內（inline）**。
3. **分數大小照講義**：函數參數或上下標裡的分數用 `\tfrac`，例如 $\cos\bigl(x+\tfrac h2\bigr)$；獨立的分數用 `\dfrac`／`\frac`，例如 $\dfrac{\sin(h/2)}{h/2}$。$\frac{d}{dx}$ 在行間公式中一律用全尺寸。
4. **同一個東西前後大小一致。** 空間不夠時改排版面，不縮小公式或改用 `\tfrac` 來擠。

## MathStage（token 級公式編舞，`src/components/Stage.tsx`）

- 一個 stage＝一袋有名字的 piece（TeX 片段／Garamond 字詞／分數線）＋一串 keyframe；每個 keyframe 是「此刻存在的 piece 各自的姿勢」（左緣 x、基線 y、字級、不透明度、色、分數線長度、延遲）。
- 兩個 keyframe 間：兩邊都有的 piece 走 token 彈簧（左移者上拱、右移者下潛，避免互撞）；新出現的上墨淡入；消失的上浮淡出；分數線由左畫出、之後可伸縮。
- 版面用 `row()`（含一層分數 `{num, den, bar}`，以數學軸對齊）算，寬度來自 MathJax 度量與 canvas 字寬，**不寫死座標**；`extent()` 取任一 piece 的左右緣掛註解。
- 第三幕所有推導都是它：定理式複本飛下成證明列、分子飛進旁註、旁註乘積飛回分子、「2」滑到分母成 h/2、極限值升上來組成結論列、表格各列飛成導數環。

## 旁白同步（`src/act3/timing.ts`、`clock.tsx`）

- 場長與每拍起點只來自 tts.py 的 `manifest.json`：場長＝lead＋旁白秒數＋tail，拍起點＝lead＋`start_seconds`。場景只寫 `at("<拍 id>", 拍內比例)`，不寫秒數。換成真 MiMo manifest（`--props='{"manifest":"audio/act3_mimo/manifest.json"}'`）即全片重新對時。
- 每場一個 `<Audio>`（manifest 的場音檔）；無旁白場（`kind: outro`）用 manifest 的 `duration`。

### 把動畫釘在某個字上（word-level alignment）

scene-aligned 的旁白（`manifest.json` 每場帶 `alignment.words_file`）有逐字對時（`src/lib/words.ts`，泛用、不綁第三幕）。比起「拍內第幾成比例」的猜測時間點，這能讓某個視覺事件精準卡在某個字被念出來的那一刻。

- `useBeats()`（`clock.tsx`）多一個 `atWord(phrase, { occurrence?, afterFrame? })`：回傳該場旁白裡第 N 次出現 `phrase`（一個字或幾個字的片語，不分大小寫、忽略標點）的**幀**；`afterFrame` 通常傳某拍的 `at("<拍 id>")`，用來跳過同一個字在更早處的出現。
- **mock manifest 沒有 `alignment`，`atWord` 會回傳 `undefined`**——這是唯一允許的 fallback，寫法固定是 `atWord(...) ?? at("<拍 id>", 拍內比例)`，讓沒有對時資料時退回原本的固定比例，行為不變。
- 找不到字（有對時資料、但這個字真的不在裡面）會直接 throw，不會默默吃掉——寫錯字或片語會在 render 時立刻爆炸，不會悄悄退化成沒對準。
- 範例（`scenes/SlopeHeight.tsx` 的 `heights` 拍，旁白「...one, zero, negative one...」）：
  ```ts
  const heightsStart = at("heights");
  const from = atWord("one", { afterFrame: heightsStart }) ?? at("heights", 0.4);
  ```

## 檔案大小（第三幕的紙紋調整）

- 動態測試 15 s crf16 是 42 MB（2.8 MB/s）：全解析度的逐像素紙紋跟著鏡頭移動，x264 無法預測。
- 現在：斑點雜訊改在半解析度（256 px tile 放大成 512 px）生成、強度約降到三分之一、纖維 140→40 條且更短更細；輸出改 crf 20。實測（2026-09-25，mock 時序）：第三幕 192 s、1080p30、crf 20＝**52.6 MB（約 0.27 MB/s，比動態測試小約 10 倍）**，本機 render 約 2 分 40 秒。紙感保留在大尺度斑駁與稀疏纖維上。

## 元件（`src/components/`）

- `Shell.tsx`：`Page`（紙＋書眉＋頁碼＋品牌 device）、`SceneShell`（整幀）、`Camera`（cx, cy, s；對數空間插值縮放）、`BrandIcon`／`BrandLockup`（原檔 SVG，不改色）。
- `Paper.tsx`：確定性種子產生的紙紋 tile＋大尺度斑駁；`Vignette` 固定在螢幕上（燈光，不隨紙動）。
- `Formula.tsx`：token 化排版（TeX 片段或 Garamond 字詞，各帶 `key`），同步版面計算；`FormulaG`、`AlignedEq`（以等號對齊）、`FormulaMorph`（共用 key 以彈簧滑行、左移者上拱右移者下潛兩條車道、不同內容飛行中交叉淡化、可指定出發順序）。
- `Plot.tsx`：`PlotFrame`、`RangeAxes`、`Curve`（筆頭上墨）、`Tangent`（彈簧長出）、`TangentNote`（沿切線刻字）、`SlopeTriangle`、`Dot`（紙色描邊環）、`Label`；`.halo` 紙色鏤空讓標籤壓在線上仍可讀。
- `Type.tsx`／`Marginalia.tsx`：`SmallCaps`、`Rule`（由左畫出）、`InkReveal`、`InlineTex`、`Para`、`FigureCaption`、`Sidenote`、`NoteRef`、`EqNumber`。
- `Stage.tsx`：`MathStage`、`row`、`extent`、`withPose`（見上）。
- 場景：`scenes/F0Title` `F1Theorem` `F2Slope` `F3Cycle` `MotionTest`（風格幀與動態測試，保留供對照）；第三幕在 `src/act3/`（`Act3.tsx` 串場、`timing.ts` manifest→幀、`clock.tsx` 拍時鐘與鏡頭、`PageTurn.tsx`、`ProofPage.tsx`、`scenes/*`）；共用 token 清單在 `src/content.ts`。

指令：`npm ci` → `npm run stills`（4 張 PNG 到 `out/frames/`）、`npm run motion`（`out/motion_test.mp4`）、`npx remotion studio` 預覽。第三幕：先跑 `act3/SCRIPT.md` 的 mock 指令產生 `public/audio/act3_mock/`，再 `npm run act3`（`out/act3_mock.mp4`）、`npm run act3:stills`（關鍵幀到 `out/act3_stills/`）；任意幀：`node scripts/frames.mjs <輸出夾> <compId>:<幀或秒s>,…`（需先 `npx remotion bundle`）。

## 做成整幕的下一步（第三幕前的清單；1–3 已在第三幕做到，見上）

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

## §3.1 無指引生成版（`src/s31/`，2026-09-25）

- 一場一張紙（`kit.tsx` 的 `Sheet`：`Page`＋鏡頭，`keepOnPage` 自動把鏡頭夾在紙內）；下一張從右側斜斜滑上來蓋住上一張（`S31.tsx`，重疊 22 幀），紙可以比畫面長（1240–1560 px），鏡頭沿紙下移。
- 時序全由 tts.py manifest 決定（`timing.ts`；lead 15、tail 27 幀），場景只用 `useS().at("<beat id>")`。
- 新增 token：`color.ochre = #A07C10`＝「角 θ／弧長／扇形」（validator 全配對通過）；`Hatches`（45° 墨斜線、金色點描、135° 淡斜線）區分巢狀面積；`Ledger`（旁註欄 OWED 帳本，付清時劃線＋PAID IN FULL）；`M`（整條 TeX、左→右墨跡、`bg` 紙色鏤空）。
- 腳本與逐拍畫面說明見 [`s31/SCRIPT.md`](s31/SCRIPT.md)。

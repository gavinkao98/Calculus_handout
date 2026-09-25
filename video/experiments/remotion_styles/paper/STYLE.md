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
| 字型 | 中文（Q7 片頭；Q7ZH 全片） | Noto Serif TC 思源宋體 400/500/600（`@fontsource/noto-serif-tc` 5.3.0，OFL）；只打包字串用到的 unicode-range 分片，見下「中文字型」 |
| 字級（px@1080p，鏡頭縮放前） | display / title / h2 / formula / proof / body / caption / label / smallCaps / micro | 300 / 108 / 64 / 112 / 70 / 44 / 36 / 34 / 28 / 28（第三幕起：凡要讀的字 ≥ 28，見下「字級下限」） |
| 格線 | 邊界 / 旁註欄 / 主欄 | 120 / x120 w280 / x460 w1340；書眉基線 74、書眉線 94 |
| 線寬 | hairline / axis / curve / tangent / emphasis | 1.5 / 1.8 / 4.2 / 3.4 / 5 |
| 緩動 | ink / camera / out | bezier(.3,0,.12,1) / (.65,0,.3,1) / (.16,1,.3,1) |
| 彈簧 | tangent / token / pop | damping 11·stiff 150·mass .7 / 15·120·.9 / 13·180·.6 |

色彩檢核：crimson↔cobalt 以 dataviz validator 在紙色上通過（CVD ΔE 18.0、一般 ΔE 28.9、對比 ≥3:1）；墨黑是刻意的「文字墨」中性色，不算類別色（validator 對它的亮度帶／彩度警告屬預期）。

## 中文字型（2026-09-26，Q7 片頭）

- **只打包用得到的字。** 畫面上的中文字串集中在 `src/q7/i18n/zh.ts`（中文版全部字串）與 `src/q7/i18n/card.ts`（兩版共用的考卷卡）；`node scripts/cjk-subsets.mjs` 讀它們、從 @fontsource 的 unicode-range 分片裡挑出涵蓋這些字的 woff2，產生 `src/q7/cjkFaces.ts`（靜態 import → 只有這些檔進 bundle）。改了字串就重跑。只挑 Garamond 拉丁分片畫不到的字（`$…$` 內的 TeX 由 MathJax 畫，不算）；含中文的字串缺字就報錯，純英文的佔位字串只警告。現況（2026-09-26，zh 表多數仍是英文佔位）：195 字 → 400／500／600 各 13 片，共 39 檔、約 1.7 MiB。
- **不准缺字、不准退回系統字型。** `src/q7/cjk.ts` 的 `useCjkReady()` 用 `delayRender` 擋住 render，直到：⓪ zh 表的 TeX（`…Tex` 欄位與 `$…$`）裡沒有中文；① 每個中文字串的每個字都落在已打包的分片範圍內；② 各字面 `FontFace.load()` 完成、`document.fonts.load()` 對實際字串載入；③ 用 canvas 量字寬證明畫字的是 Noto（size-adjust 後每字 0.86 em，系統字型會是 1 em）。任一條不成立就 `cancelRender`，不會默默出豆腐或換字型。英文版只有呼叫 `useCjkReady` 的片頭兩場會載；中文版（`Q7ZH`）每一張紙都等它（`Q7.tsx` 的 `CjkGate`），render log 會印 `[cjk] Noto Serif TC 400/500/600 in use`。
- **與 Garamond 混排：** 字族堆疊 `'EB Garamond', 'Noto Serif TC'`——數字與拉丁字走 Garamond（設 `lnum` 等高數字），漢字與全形標點落到 Noto。同字級下漢字看起來大一號，所以 Noto 字面加 `size-adjust: 86%`（`CJK_SCALE`），漢字約為 Garamond 大寫高的 1.2 倍。標題用 500、其餘 400（漢字本身比 Garamond 重，不用 600）；中文不用斜體（瀏覽器只會假斜），小型大寫的角色改成加字距（0.24–0.3 em）的小字。
- **字級下限照舊，以有效字級計：** font-size × 0.86 ≥ 28 px，所以中文最小設 34 px。右齊欄位若以全形「）」收尾，要讓它右懸（`marginRight −0.36em`），否則右緣會比數字內縮約半個字身。

## 中文版排版（2026-09-26，Q7 雙語，模板規則）

Q7 是「單一來源、雙語」：動畫、幾何、版面座標只有一份（`src/q7/scenes/*`），上畫面的字串抽在 `src/q7/i18n/en.ts`／`zh.ts`（同形狀，`Strings` 型別強制 key 一致），`Q7` composition 的 `lang` 決定用哪張表；`Q7ZH`＝`lang: "zh"`＋`audio/q7zh_mock/manifest.json`。場景一律透過 `useT()` 取字串，文字元件用 `src/q7/kit.tsx` 的語系版 `Txt`／`Kicker`／`Caps`／`Sheet`——英文時它們原樣轉給 §3.1 的元件（英文輸出逐像素不變），中文時才套下列規則。

1. **中文沒有斜體。** 英文版用 italic 的地方，中文分兩種處理：
   - **整段斜體**（圖說、旁註、標籤等「次要語域」）→ 直立的 Noto，靠原本的次要墨色（`ink2`／`ink3`）或語意色區分層級，不另加效果。
   - **句中強調**（字串標記 `{i:…}`，例如 *mirror image*、*Unfolding*）→ **600 字重＋原本的語意色**（無色時就是墨黑 600）。
   - 全片 zh 範圍掛 `font-synthesis: none`，瀏覽器不能假斜、假粗；Noto 打包 400／500／600 三個真字重。
2. **字族與字級。** 所有中文走 `'EB Garamond', 'Noto Serif TC', serif`（`ZH_FONT`；zh 範圍另有 `!important` 的保險，Page 書眉等共用元件也不會落到系統字型）。字級低於 34 的一律抬到 34（有效 29 px）；英文 30 px 的圖說在中文就是 34。中文散文設等高數字（`lnum`），Garamond 的舊式數字在漢字旁會往下沉。
3. **小型大寫的角色（kicker、書眉、SHOT 1、BOUNCES）** → 34 px、500 字重、加字距：kicker 0.24 em、書眉這種長行 0.12 em。字距只加在漢字上：標籤裡的拉丁字與數字（「(a)」「115」）維持原字距（`Caps` 自動處理），不會排成「( a )」。
4. **換行。** 中文任兩字之間都能斷，`Txt` 在中文用 `line-break: strict`（行首不放「，。）」等）。另外兩條自動處理：① 段尾最後 3 字綁在一起（`nowrap`），不留一字孤行（「個。」）；② 標點擠壓——全形收尾標點後面緊接另一個標點（「）。」「。」」）時前者收回半個字身（打包的 Noto 分片沒有 `halt`，`text-spacing-trim` 不作用）。需要控制斷行位置（例如把長問句按語意切三行）時在字串裡寫 `\n`。圖說若以全形「（」起頭，讓它左懸半字身（`textIndent −0.5em`），漢字對齊圖框左緣。
5. **中文夾數學。** 數學一律寫成 `$…$`（Pagella TeX，`InlineTex` 以 TeX 自己的深度對齊基線），不要用 Garamond 斜體字母代替；`$…$` 前後不手動加空格——與漢字相鄰時自動留 0.18 em，挨著全形標點時不留（標點本身有空）。數字與漢字之間照台灣慣例手打半形空格（「115 學年度」「寬 2 個單位」）。整條 TeX（`…Tex` 欄位）的 `\text{}` 裡不能放中文（MathJax 量不到寬度，渲染時擋下）：要把字拆成文字＋公式兩塊。Q7 的做法是中文專屬的 `…Line` 欄位（`foldback.countLine`、`angles.dirLine`、`twist.testLine`，英文為空字串）：整行寫成「中文＋`$…$`」交給 `Txt` 排，場景見到非空就用它取代英文的整條 TeX。行內兩段 TeX 相鄰時（例如 `=` 後接上色的 `{edge:$3$}`），關係符號右側的空白要自己補 `\;`。Garamond 沒有的符號（∞）不要放在文字裡，改用 TeX（`recap.infTex = "\infty"`）。
6. **標籤守門照常生效。** `useT().tLbl` 在中文用實際畫字的字族堆疊、實際字級（抬到 34 後）量寬，框的上下緣也放寬一點（Noto 的漢字比 Garamond 占滿 em 框），不拿 Garamond 量中文。
7. **逐字對時錨點。** 中文旁白用 `--unit beat` 合成、沒有逐字對齊，所以英文版靠 `atWord("…")` 卡字的三個點在中文分鏡裡是獨立的拍（angles 的 `tan`／`vert`、halfway 的 `list`）；場景寫法 `has("tan") ? at("tan") : atWord(...) ?? at(...)`，`has()` 查不到不 throw。英文分鏡沒有這三拍，行為不變。

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

## 圖上標籤（2026-09-25 使用者裁決，模板規則）

使用者在 §3.1 04:05 抓到：`y = cos θ` 標籤掛在 cos 曲線上，底下的紙色底色（`bg`）把那段曲線蓋掉，曲線看起來斷了一截。

1. **標籤不碰任何圖形。** 曲線、座標軸、刻度、陰影區的邊界都算。標籤外框和圖形之間至少留一段固定間距。
2. **放在空白處。** 離要標的東西太遠時，用細引線連過去；不要為了貼近而壓在線上。
3. **禁止用底色蓋掉曲線或軸。** 紙色底色只能用在「字落在淡色填色或斜線陰影上」的情況，而且底下不能有任何線條經過。
4. **自動檢查擋下違規。** 渲染時會檢查標籤外框與圖形的距離，太近就報錯、不出片，不靠肉眼抓。
   - 實作（§3.1，`src/s31/kit.tsx` 的 `checkLabels`，場景裡用 `useS().guard(marks, labels)`）：每一幀把畫好的圖形（曲線取樣成折線、軸與刻度是線段、點含紙色外圈、填色區只算邊界）和標籤的字形外框（`mLbl`／`tLbl`，與 `M`／`Txt` 同一組參數）逐一量距離；間距小於 `theme.ts` 的 `labelGuard.clearance`（10 px，1080p 頁面座標）就 throw，訊息寫明場景、幀、標籤、圖形名。
   - 會移動的東西只在靜止姿勢檢查（例如轉動的點停下之後）；引線與刻度帶 `owner`，只對它自己的標籤豁免；沿切線刻的字用 `rot` 在旋轉座標裡量。

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

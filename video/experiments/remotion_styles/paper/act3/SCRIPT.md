# §3.1 第三幕「Derivatives of Sine and Cosine」——紙本編輯排版版腳本

**狀態（2026-09-25）：** 設計輪（無稽核閘）。旁白依畫面重寫，教學內容同原 storyboard 的 `intro`／`derivative_of_sine`／`derivative_of_cosine`／`slope_equals_height`／`derivative_cycle`／`outro`。目前只有 **mock 時序**（`tts.py --backend mock`：150 wpm 估長的靜音 WAV）；真 MiMo 配音要先經使用者同意（見文末指令）。

- 旁白唯一來源：[`act3.yml`](act3.yml)（`say:` 已是口語形，無 LaTeX；`{show <id>}` 切拍）。下表的英文逐字與它相同，改旁白請改 yml、再重跑 mock，**不要只改這份**。
- 時序唯一來源：`public/audio/<run>/manifest.json`（tts.py 產出）。Remotion 讀它排每場長度（lead 30 幀＋旁白＋tail 30 幀；片頭 lead 12 幀）與每拍起點，換成真 MiMo manifest 不必改程式。
- 場景程式：`src/act3/scenes/*`；拍 id 必須與 yml 的 `{show}` 一致（缺拍會在 render 時直接報錯）。

## 總覽（mock 時序）

| 場 | 版面 | 旁白字數 | mock 旁白秒數 | 場長（幀＠30） | 交接 |
|---|---|---:|---:|---:|---|
| `intro` | 節首頁（章號＋標題＋目錄＋品牌 lockup） | 35 | 14.0 | 462 | 翻頁 |
| `derivative_of_sine` | 定理頁（verso，旁註在外側左欄） | 138 | 55.2 | 1716 | 滑到對頁（無剪接） |
| `derivative_of_cosine` | 定理頁（recto）→ 桌上攤開的跨頁 | 92 | 36.8 | 1164 | 翻頁 |
| `slope_equals_height` | 全幅圖版頁（Figure 3.3，比畫面寬） | 110 | 44.0 | 1380 | 翻頁 |
| `derivative_cycle` | 表格頁（Table 3.2）→ 導數環 | 76 | 30.4 | 972 | 翻頁 |
| `outro` | 版權頁式收尾（無旁白） | 0 | 6.0 | 180 | — |
| **合計** | | **451** | **186.4** | **5762（192.1 s，扣 4 次翻頁重疊各 28 幀）** | |

## 逐拍腳本

欄位：拍 id（`_`＝第一個 `{show}` 之前那句）｜英文旁白（逐字）｜畫面上發生什麼。

### intro — 節首頁

| 拍 | 旁白 | 畫面 |
|---|---|---|
| `_` | How fast does sine change? | 冷開場：鏡頭貼近（s≈2）一條正弦花飾正被「上墨」畫出，一條紅色切線沿著它滑、切線上刻著即時斜率讀數（slope 0.58…）——問題本身用圖問出來。 |
| `title` | That's our question: the derivatives of sine and cosine. | 鏡頭拉遠成整頁：大號「§3.1」、節標題 *Derivatives of Sine and Cosine*、紅短線、斜體問句依序墨跡排入；書眉、頁腳細線、品牌 lockup 同時出現。切線持續滑動（整場不停）。 |
| `contents` | We'll prove both from the definition, see them on the graph, and find the loop of four that ties them together. | 目錄四列隨子句逐列排入（i. The derivative of sine … 113 等，40 px、點狀引導線、舊體頁碼）。場尾整頁像書頁一樣翻過去。 |

### derivative_of_sine — 定理頁（113 頁）

| 拍 | 旁白 | 畫面 |
|---|---|---|
| `_` | Start with sine. | 翻頁後的新頁：書眉、左欄「THEOREM 3.1 / Derivative of sine」與紅色 rubric 豎線已在。 |
| `statement` | The claim: the derivative of sine x is cosine x, for every real x. | 鏡頭推近（s≈1.75）；定理式 d/dx sin x = cos x（紅 d/dx、黑 sin、藍 cos）逐 token 排入，下方斜體 *for every real number x (in radians)*。 |
| `definition` | Go back to the definition: the limit, as h goes to zero, of sine of x plus h, minus sine x, over h. | 鏡頭退到證明區；定理式左邊的「d/dx sin x」**複本沿弧線飛下**成為證明第一列的開頭，接著「= lim」、分數線（由左畫出）、分子、分母 h 依序排入。左側 *Proof.* |
| `identity` | The top is a difference of sines, and a sum-to-product identity turns it into a product: two cosine of x plus h over two, times sine of h over two. | 鏡頭平移到左側旁註欄（旁註特寫）：分子「sin(x+h) − sin x」**從第一列飛進旁註**，標題 SUM TO PRODUCT；「= 2cos(x+h/2)」「· sin(h/2)」逐項寫出。拍尾這三個因子**從旁註飛回主欄**，組成第二列「= lim (2cos(x+h/2) sin(h/2))/h」，第一列退淡。 |
| `rewrite` | Slide the two down under the h, and the quotient splits into two factors: cosine of x plus h over two, times sine of h over two, over h over two. | token 變形：分子裡的「2」**滑到分母 h 後面**變成 h/2（補上「/」），cos 因子移出分數到左邊，分數線縮短到只蓋住 sin(h/2)。 |
| `limits` | Now let h go to zero. The first factor tends to cosine x, since cosine is continuous. The second is the fundamental limit: it goes to one. | 兩支紅色箭頭依序由上往下畫出：cos 因子下方彈出藍色「cos x」＋斜體註 *cos is continuous*；半拍後分數下方彈出「1」＋ *the fundamental limit*。 |
| `qed` | Cosine x, times one. The derivative of sine is cosine. | 箭頭與註解讓位，「cos x」「1」兩個值**升上來**組成結論列「= cos x · 1 = cos x ∎」；紅筆在定理式的 cos x 外畫一圈；鏡頭拉回整頁（這一幀正是下一場的起點）。 |

### derivative_of_cosine — 對頁（114 頁）→ 跨頁

| 拍 | 旁白 | 畫面 |
|---|---|---|
| `_` | Now turn to the facing page. | 無剪接：從剛完成的 113 頁（右緣是書溝陰影）橫移越過書溝到右頁 114。右頁的旁註欄在**外側（右邊）**，像真的書。 |
| `statement` | Cosine works the same way. Its derivative is negative sine x. | 推近；d/dx cos x = −sin x 排入（紅 d/dx、藍 cos、負號單獨一個 token）。 |
| `identity` | Only the identity changes: cosine of x plus h, minus cosine x, equals negative two, sine of x plus h over two, sine of h over two. | 同一套機制但更快：定義列排入、分子飛進右側旁註、旁註寫出「= −2 sin(x+h/2) · sin(h/2)」、拍尾因子飛回組成第二列。 |
| `rewrite` | Divide by h as before: negative sine of x plus h over two, times the same fraction. | 同樣的 token 變形：「2」滑到 h 下、負號與 sin 因子移出分數。 |
| `limits` | As h goes to zero: negative sine x, times one. | 兩支箭頭與「−sin x」「1」較快依序出現。 |
| `qed` | So the derivative of cosine is negative sine x. | 結論列「= −sin x · 1 = −sin x ∎」，紅筆圈住定理式的 −sin x。 |
| `compare` | Side by side: the same two tools, and one extra minus sign. | 鏡頭從頁面**拉離到桌面**：整本攤開的書（深色桌面、書的投影、書溝）；兩頁證明區罩上一層紙色薄紗，只留兩條定理式清楚；紅筆在右頁那個唯一的負號上再加一個小圈。場尾右頁翻過去。 |

### slope_equals_height — 圖版頁（116 頁，Figure 3.3）

| 拍 | 旁白 | 畫面 |
|---|---|---|
| `_` | What does this look like on a graph? | 兩個面板的 range-frame 座標軸畫出（上：sin，下：cos 的軸稍後）。 |
| `sine` | Here's y equals sine x. Let's check the slope of its tangent at a few points. | sin 曲線以筆尖上墨畫出；鏡頭推近上面板（s≈1.6）；面板標題 (a) y = sin x。 |
| `tan0` | At zero, it's climbing, with slope one. | x=0 的點彈出、紅色切線彈簧式長出、斜率三角形（虛線 run、紅色 rise）、沿切線刻字 *slope 1*。 |
| `tanhalf` | At pi over two, the top of the hump, the tangent is flat: slope zero. | 同一條切線**沿曲線滑到 π/2**（讀數連續變化），鏡頭跟著走；原位置留下一條淡墨「印記」。停下時 *slope 0*。 |
| `tanpi` | At pi, it's falling, with slope negative one. | 再滑到 π，*slope −1*，又留下一個印記。 |
| `cosine` | Now draw cosine x underneath, | 鏡頭拉回整幅；下面板座標軸與藍色 cos 曲線畫出。 |
| `heights` | and read its heights at those same points: one, zero, negative one. They match the slopes exactly. | 隨「one, zero, negative one」：虛線鉛垂線從 sin 的點落到 cos，紅色高度棒彈出（*height 1 / 0 / −1*）；「match exactly」時上下的紅棒一起脈動加粗。 |
| `sweep` | And not just there. Wherever the tangent goes, its slope is the height of cosine right below it. | 印記退淡；活切線從 π 一路掃到 2π，下面板的活高度棒與讀數同步（slope −0.54 ↔ height −0.54）。 |
| `words` | In words: the slope of sine equals the height of cosine. | 鏡頭橫移到頁面右側欄（原本在畫面外）：Figure 3.3 圖說、「IN WORDS」小標、句子 *the slope of sin at x = the height of cos at x* 逐字排入。 |
| `symbols` | In symbols, that's our theorem. | 句子的 token 滑行變形成 d/dx sin x = cos x（句子本身淡留在上方），「IN SYMBOLS」小標、式號 (3.1)；鏡頭輕推。場尾翻頁。 |

### derivative_cycle — 表格頁（118 頁，Table 3.2）

| 拍 | 旁白 | 畫面 |
|---|---|---|
| `_` | Now step back and look at the pattern. | 鏡頭貼近表格；booktabs 粗細線畫出、表頭 n ｜ dⁿ/dxⁿ sin x、第 0 列 sin x。 |
| `d1` | Differentiate sine: you get cosine. | 第 1 列 cos x 排入，右側一支紅色 d/dx 小弧箭頭從上一列跳到這列。 |
| `d2` | Again: negative sine. | 第 2 列 −sin x ＋弧箭頭。 |
| `d3` | Again: negative cosine. | 第 3 列 −cos x ＋弧箭頭。 |
| `d4` | And once more: back to sine. | 第 4 列 sin x ＋弧箭頭，表格底線畫出。 |
| `ring` | Bend that list into a circle, and it becomes a cycle, one quarter turn per derivative. | 鏡頭拉遠；表格退淡，**每一列的式子依序飛出表格到環上的四個站**，最後一列的 sin x 落在第一個 sin x 上合而為一；四段紅色弧箭頭依序畫出，外側標 d/dx。 |
| `fourth` | Four derivatives and you're home: the fourth derivative of sine is sine. | 鏡頭推近環；一顆紅色筆尖點沿環走四個四分之一圈，每到一站該站微微發光；環心排入 d⁴/dx⁴ sin x = sin x。 |
| `compare` | e to the x renews itself in one step; sine and cosine take four. That endless loop is what lets them oscillate forever. | 表格完全退場，左邊出現同款但只有一站的小環：e^x 與一整圈的 d/dx 箭頭，下註 *one step*；大環下註 *four steps*。場尾翻頁。 |

### outro — 收尾頁（無旁白，6 s）

正弦花飾（切線持續滑動）、紅色小型大寫 END OF SECTION 3.1、斜體 *Next*、大字「§3.2 The Chain Rule」、紅短線、置中的品牌 lockup；鏡頭緩慢拉遠。

## 驗證與重跑

離線 mock（不計費、可逕行；在 repo 根目錄）：

```bash
python video/pipeline/tts.py --storyboard video/experiments/remotion_styles/paper/act3/act3.yml \
  --scene all --backend mock --unit beat \
  --output-dir video/experiments/remotion_styles/paper/public/audio/act3_mock
```

真 MiMo 配音（**付費外部 API，須先經使用者同意**；5 個有旁白的場、35 個 beat、mock 估約 186 s 音訊）：

```bash
python video/pipeline/tts.py --storyboard video/experiments/remotion_styles/paper/act3/act3.yml \
  --scene all --backend mimo --unit beat \
  --output-dir video/experiments/remotion_styles/paper/public/audio/act3_mimo
```

然後在 `paper/` 下：

```bash
npx remotion bundle
npx remotion render build Act3 out/act3.mp4 --codec=h264 --crf=20 --props='{"manifest":"audio/act3_mimo/manifest.json"}'
```

`public/audio/` 不進版控（WAV 與含絕對路徑的 manifest）；換機時先重跑上面的 mock 指令。

# 2026 臺大北區科學人才培育計畫數學組入學考 第 7 題（正方形撞球桌）——解題影片腳本（紙本編輯排版）
> 2026-09-26，motion-designer 子代理。旁白為英文（原文照登），框架說明為繁體中文。旁白源＝[`q7.yml`](q7.yml)（tts.py 格式，`{show <id>}` 切 beat）；畫面＝`../src/q7/`。時長為 mock（150 wpm 估算），換真 MiMo manifest 後全片自動重新對時。題目出處：115 學年度國立臺灣大學北區高中學生科學研究人才培育計畫－數學組入學考試（2026-09-06 舉行）第 7 題；片頭（`logo` 副標與 `exam` 上半頁考卷卡）用中文、排 Noto Serif TC 思源宋體；其餘畫面英文。畫面字串抽在 `../src/q7/i18n/`（en／zh 同形狀）；中文版 composition 為 `Q7ZH`（見 STYLE.md「中文版排版」）。
## 敘事取向
照使用者核准的教學計畫走：先把題目交代清楚（考試身分＋題目＋重畫的三張原圖），用四發試射勾起「哪些球會回家」，再用「反射＝鏡像」一拍鋪好唯一的工具，然後**慢慢展開桌子**（一次反射一拍，下一張桌子像書頁一樣以那面牆為軸翻過來，被反彈的那段路徑隨之翻成直線的延續）。展開後把平面上的格點依奇偶上色（藍＝(偶,偶)＝中心的複本＝回家；紅圈＝(奇,奇)＝角洞的複本），題目就變成「從原點出發的直線先碰到另一個藍點還是紅圈」。核心論證是**中點測試**：瞄準射線上第一個 (偶,偶) 點 (2p, 2q)，gcd(p, q) = 1，線段上只有起點、終點與中點 (p, q) 三個格點（畫面明寫，不跳過）；p、q 皆奇則中點是角洞、半路落袋，一奇一偶則中點安全、回家。之後把 (1,0) 與 (2,1) 摺回真桌，計數器逐次反彈跳號（|p| + |q|），回到 θ（方向 (p, q)；p ≠ 0 時 tan θ = q/p，p = 0 是鉛直射擊；tan θ = 2k 的家族→無窮多個），再加入邊中點洞做 (b)：中點永遠是洞，答案 0。收在並排回顧、考場寫法、以及「無理斜率的軌跡任意接近桌上每一點（稠密）」的延伸（只展示不證明）。
## 設計語彙（本片新增）
- **語意色（沿用紙本系統的三種已驗證墨色）：** 藍 cobalt＝中心與它的複本（回家）；紅 crimson 空心圈＝角洞；金 ochre 空心圈＝邊中點洞（(b) 才出現），同時也是「鏡子」色——翻頁時被當成軸的那面牆、鏡像的那段路徑、中點 (p, q)、反彈計數器都用金色。球與路徑一律墨黑。
- **翻頁式展開（`src/q7/kit.tsx` 的 `Unfold`）：** `stage ∈ [0, n]`，整數時是「已反射 k 次」的狀態；小數部分是下一張桌子以牆為軸翻過來的進度（沿法向壓縮成 cos，洞被壓成橢圓、紙色加深），路徑剩下的部分跟著一起翻。同一個元件倒著跑就是「摺回真桌」。所有路徑都是精確的：`src/q7/geo.ts` 用三角波把平面摺回 [−1,1]²，路徑是經過各反彈點的折線，不取樣。
- **圖上標籤守門：** 沿用 §3.1 的 `checkLabels`（`useS().guard`），考卷圖、鏡像圖、字典、中點測試、(b) 等有標籤的圖每一幀都檢查標籤與圖形的距離（≥ 10 px）。
- **時序：** 與 §3.1 同一套 manifest 讀法（lead 15、tail 27、重疊 22 幀），另外 `timing.ts` 的 `HOLD` 在 epilogue（+4 s）、recap、writeup 後面加停留，讓畫面有時間跑完。
## 逐場逐拍
### 1. `logo`——品牌開場（無旁白）（4.0 s）
- **畫面：** 空白紙頁正中央，lockup 以墨跡由左到右排上，下方紅色短線與中文副標「115 學年度北區人才培育計畫入學考第七題」（思源宋體，加字距）；鏡頭從 1.05 緩緩退到 1.0。
### 2. `exam`——考卷卡（mock 47.8 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | This is problem seven from the twenty twenty-six math entrance exam of National Taiwan University's Northern Taiwan High School Science Talent Program, held on September sixth. | 上半頁（像書名頁，中文：思源宋體＋Garamond 數字）：頂線左側「入學考試・數學組」；左邊紅字「題號」、下面大字 7，再下面的花飾是一張小球桌、球沿 (2,1) 的菱形路徑一圈圈回家；右欄紅字「國立臺灣大學」、標題「北區高中學生／科學研究人才培育計畫」、紅色短線、「數學組・115 學年度入學考試」，點狀引導線列出 學年度 115／測驗日期 115 年 9 月 6 日（星期日）／題號 第 7 題（共 7 題）。 |
| `setup` | A square billiard table has a pocket at each corner. A ball, treated as a point, starts at the exact center. It rolls in straight lines, bounces off the edges by the law of reflection, and stops once it falls into a pocket. | 鏡頭下移到下半頁（全場唯一一次移動）：題目英文全文排入；右側重畫考卷的兩張圖（球的路徑、落袋結束，虛點線加箭頭），圖例「● start (center)　○ pocket」；左下頁腳註 *Translated from the Chinese original.*（這一頁才是翻譯）。 |
| `theta` | Theta is the angle between the shot and the bottom edge. | 「Let θ be the angle…」排入；圖一的起點畫出水平參考線與金色角弧、標 θ。 |
| `parta` | Part a. Prove that infinitely many angles bring the ball back to the center before it falls into any pocket. | (a) 題文排入（θ ∈ [0, 2π)）。 |
| `partb` | Part b. Add a pocket at the midpoint of every edge. How many angles work now? | (b) 題文排入；右下重畫 (b) 的八洞球桌（角洞紅、邊洞金），圖說 the table in (b): eight pockets。 |

### 3. `hook`——四發試射（mock 27.8 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Let's try a few shots. | 四張小桌並排（SHOT 1–4），依序以筆畫描出。 |
| `corner` | Aim at a corner, and the ball drops straight in. Aim a little steeper, and it bounces once, then finds a corner anyway. | Shot 1：對角線直接落入右上角洞（球縮小消失、紅色閃圈、洞被填紅）；Shot 2：斜率 3，碰上緣一次後落入右下角。圖說 straight into a corner／one bounce, then a corner。 |
| `wander` | This one bounces, and bounces, and never settles. | Shot 3：斜率為黃金比的球一直彈，軌跡變淡變密，持續到場末；圖說 still going …。 |
| `home` | But this one hits three walls, and rolls right back to the center. | Shot 4：(2,1) 的菱形路徑，三次反彈回到中心，藍色閃圈＋藍圈；圖說 home, after three bounces。 |
| `question` | So which shots come home? Chasing bounces one by one is hopeless. We need a better picture. | 大字斜體 Which shots come home?（home 藍），下一行 Chasing bounces one by one is hopeless — we need a better picture.。 |

### 4. `mirror`——反射＝鏡像（mock 20.6 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Start with a single bounce. | 一面粗牆，牆外鋪淡色（beyond the wall）；球沿入射線滾到牆上。 |
| `equal` | The angle coming in equals the angle going out. | 反射段畫出，牆上下兩個金色角弧各標 α；左欄 Angle in = angle out.。 |
| `image` | So the bounced path is the mirror image of where the ball would have gone if the wall were not there. Flip it across the wall, and it lines up with the straight line. | 牆外畫出灰色虛線的「直線延續」；反射段的複本以牆為軸翻過去（金色），剛好落在虛線上。左欄 So the bounced path is the *mirror image* of the path with no wall.／Turn it over the wall, and it lands exactly on the straight line.。 |

### 5. `unfold`——展開桌子（關鍵，一拍一次反射）（mock 40.2 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Here is the shot that came home. Bounces are hard to follow. Straight lines are easy. | 鏡頭貼近真桌（s 1.6）：Shot 4 的菱形路徑再跑一次，球回到中心。 |
| `first` | At the first bounce, mirror the whole table across the right wall. The bounced segment flips over, and becomes the straight continuation. | 鏡頭退回整頁（本場唯一一次鏡頭移動），左欄出現 UNFOLDING、Bounces are hard. Straight lines are easy.、At each bounce, mirror the table across 1. the right wall；右牆亮金色，第二張桌子像書頁一樣翻過來，路徑剩下的部分跟著翻成直線。真桌下標 the real table。 |
| `second` | Next bounce, the top wall. Mirror again. | 第二次翻頁（上牆），清單 2. the top wall。 |
| `third` | And once more, across the next wall. | 第三次翻頁，清單 3. the next wall；此時是一條橫跨四張桌子的直線。 |
| `line` | No bounces are left. Just one straight line across four copies of the table, ending at the center of a copy. That is the ball, home. | 球沿直線從原點跑到 (4,2) 那張桌子的中心，藍色閃圈、標 home；左欄 One straight line, ending at the center of a copy: the ball is home.。 |
| `plane` | Mirror in every direction, and the copies tile the plane. Every shot becomes a straight line from the origin. | 整片平面的牆線（奇數座標線）淡入、四邊羽化；直線往外延伸，另有三條灰色虛線代表其他射擊方向。 |

### 6. `dictionary`——座標字典（mock 32.6 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Put coordinates on it. The real table runs from minus one to one, so every copy is two units wide. | 右側平面（羽化視窗）與粗框真桌；左欄 The real table is [−1,1]×[−1,1] so every copy is 2 units wide.；真桌上方尺寸線標 2。 |
| `centers` | Copies of the center sit where both coordinates are even. Land on one, and the ball is home. | 所有 (偶,偶) 點以彈簧由近而遠冒出藍點，標 (0,0)、(2,0)、(2,2)、(−2,2)；左欄 ● (even, even) — a copy of the center: the ball is home。 |
| `corners` | Copies of the corners sit where both coordinates are odd. Land on one, and the ball falls in. | 所有 (奇,奇) 點冒出紅圈，標 (1,1)、(3,1)、(−3,−1)；左欄 ○ (odd, odd) — a copy of a corner: the ball falls in。 |
| `question` | So here is the whole problem. Does the line from the origin hit another even, even point before an odd, odd point? | 座標標籤退淡；兩條示範射線：一條到 (4,2)（藍閃），一條到 (1,1)（紅閃）；左欄 Does the ray from the origin hit another blue point before a red one?。 |

### 7. `halfway`——中點測試 → (a)（mock 50.6 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | To come home, aim at an even, even point. Call it two p, two q. | 右側格點平面（藍點、紅圈，另把其餘格點畫成小灰點）；一條線段從原點畫到 (6,4)（示意 p=3, q=2），標 (2p, 2q)；左欄 To come home, aim at a blue point (2p, 2q)。 |
| `first` | Take the first one on the ray. Then p and q share no common factor. | 左欄 first blue point on the ray: gcd(p, q) = 1。 |
| `only` | So the first lattice point along the ray is p, q, and the next one is two p, two q. The only lattice points on the segment are the start, the midpoint p, q, and the end. | 線段外的格點全部退淡；只有 (0,0)、(3,2)、(6,4) 保持全亮，中點標金色 (p, q)；左欄斜體 first lattice point on the ray: (p, q)／the next: (2p, 2q)，第二句時接 Only lattice points on the segment: (0,0), (p,q), (2p,2q)。 |
| `mid` | Everything hangs on that midpoint. | 中點外一圈金色呼吸光環；左欄 Everything hangs on the midpoint (p, q).。 |
| `odd` | If p and q are both odd, the midpoint is a corner, and the ball is pocketed halfway. The diagonal shot, one, one, does exactly this. | 示範 (1,1)：球從原點滾向 (2,2)，在中點 (1,1) 的紅圈落袋（紅閃），之後的一段只剩灰虛線；左欄 p, q both odd → a corner: pocketed halfway。 |
| `mixed` | If one is odd and the other is even, the midpoint is harmless, and the ball makes it home. And they can't both be even. | 示範 (1,2)：球經過中點 (1,2)（金圈，安全）到 (2,4) 回家（藍閃）；左欄 one odd, one even → safe: the ball comes home、both even → impossible, as gcd = 1。 |

### 8. `foldback`——摺回真桌＋反彈計數（mock 39.8 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Try one, zero. The line runs to two, zero. | 兩張桌子、直線從原點到 (2,0)，中點 (1,0) 金圈；左欄 (p,q) = (1,0)、aim at (2, 0); the midpoint (1, 0) is safe，BOUNCES 計數器 0（金色大數字）。 |
| `fold1` | Fold it back onto the real table. One bounce off the right wall, and home. | 第二張桌子以右牆為軸翻回真桌，計數器跳 1（彈一下）；球在真桌上往右撞牆再回到中心（藍閃）。 |
| `next` | Now two, one. The line runs to four, two. | 換成 (p,q) = (2,1)：四張桌子、直線到 (4,2)，中點 (2,1) 金圈，計數器歸 0。 |
| `fold2` | Fold it back, one wall at a time. Three folds, three bounces. It is the shot we saw come home. | 三次摺回（右上那張→上面那張→右邊那張），計數器 1、2、3；最後球在真桌上跑出 Shot 4 的菱形、回家。 |
| `count` | In general, for a shot that makes it home, the line crosses the absolute value of p vertical walls and the absolute value of q horizontal walls. So the ball bounces the absolute value of p, plus the absolute value of q, times. | 再展開一次，被穿過的牆（x=1、x=3 兩道直牆與 y=1 一道橫牆）亮成金色；左欄斜體 For a shot that makes it home:、It crosses \|p\| vertical and \|q\| horizontal walls:、bounces = \|p\| + \|q\| = 2 + 1 = 3。 |

### 9. `angles`——回到 θ（mock 37.4 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Back to the angle. The shot goes in the direction p, q, with no common factor, one odd and one even. When p is not zero, tangent theta is q over p. And p equal to zero is the straight up-and-down shot. | 左欄先出 direction (p, q)、no common factor; one odd, one even；唸到 When p is not zero 時接 tan θ = q/p (p ≠ 0)；右側大真桌上一條斜率 2 的射線，金色角弧標 θ；唸到 p equal to zero 時藍色虛線鉛直射擊淡入並標 (0, 1) works too。 |
| `family` | Take p equal to one, and q any even number, two k. Every k gives a different angle, so there are infinitely many. That proves part a. | (p,q) = (1, 2k)，列表 k = 0,1,2,3 → tan θ = 0, 2, 4, 6, ⋮；桌上射線依序彈出（k = 0, ±1, ±2, ±3, ±4, ±6, ±9 及反方向），越來越擠向鉛直方向（藍色虛線鉛直射擊已在上一拍出現）；藍框 Infinitely many angles. (a) is proved.。 |
| `irrational` | And an irrational slope never hits any other lattice point. The ball never falls in, but it never comes home either. | 桌下斜體註 An irrational slope never meets another lattice point: never pocketed, never home.。 |

### 10. `twist`——(b)：加上邊中點洞（mock 38.6 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Now part b. Add a pocket at the middle of every edge. | 左下真桌四個邊中點冒出金圈；右側格點平面淡入（含真桌粗框）。 |
| `copies` | Their copies have one odd and one even coordinate. Now every lattice point is a pocket, except the even, even ones. | 平面上所有 (奇,偶)、(偶,奇) 點冒出金圈；左欄 Their copies: (odd, even) and (even, odd). Now every lattice point is a pocket, except (even, even).。 |
| `test` | The halfway test: the midpoint p, q is never even, even, so it is always a pocket. Every trip home is cut off halfway. | gcd(p,q) = 1 ⇒ (p,q) ≠ (even, even)；紅斜體 The midpoint is always a pocket: every trip home is cut halfway.。 |
| `revisit` | Our easiest success, one, zero, now drops into the pocket on the right edge. And two, one folds back onto the pocket at the top. | 真桌上 (1,0) 的球直接落進右邊中點洞（金閃，標 (1, 0)）；再來 (2,1) 的球彈右牆後落進上邊中點洞（標 (0, 1)），平面上同步畫出到 (2,1) 的線段（金閃，標 (2, 1)），之後到 (4,2) 的部分只剩灰虛線。 |
| `answer` | So in part b, no angle works. The answer is zero. | 兩圖之間：angles in (b): 大紅字 0。 |

### 11. `recap`——並排回顧（mock 16.9 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | So, part a has infinitely many angles. Part b has none. | 左右兩欄：(a) FOUR CORNER POCKETS 小桌＋菱形回家路徑，藍色大字 ∞、infinitely many angles；(b) EIGHT POCKETS 小桌＋同一發在上邊中點落袋，紅色大字 0、no angle at all。 |
| `ideas` | Two ideas did all the work. Unfolding turns bounces into a straight line. The halfway test turns that line into a question of even and odd. | 下方細線後兩行：*Unfolding* turns bounces into a straight line.／*The halfway test* turns the line into a question of even and odd.。 |

### 12. `writeup`——考場寫法（mock 23.7 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | On the exam, four lines are enough. | HOW TO WRITE IT ON THE EXAM、斜體 *Solution.*，左側紅色豎線。 |
| `s1` | Unfold the table into a plane of copies. | 1. **Unfold.** Reflect the table across its walls. The path becomes a straight ray from the origin, in direction (cos θ, sin θ), across a plane tiled by copies of [−1,1]². |
| `s2` | Centers sit at even, even points, and corner pockets at odd, odd points. | 2. **Name the points.** Copies of the center: (2m, 2n). Corner pockets: (odd, odd). In (b), the edge pockets add (odd, even) and (even, odd). |
| `s3` | Aim at two p, two q, and check the midpoint, p, q. | 3. **Check the midpoint.** Coming home means reaching some (2p, 2q), gcd(p, q) = 1, first. The only lattice point strictly between is (p, q). |
| `s4` | Conclude. Infinitely many angles in part a, and none in part b. | 4. **Conclude.** (a) If p + q is odd, (p, q) is no pocket; tan θ = 2k for every integer k gives infinitely many θ. (b) (p, q) is never (even, even), so it is always a pocket: no angle works. ∎ |

### 13. `epilogue`——題外：無理斜率的路徑在桌面上稠密（mock 24.2 s，含 4 s 停留）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | One more thing, beyond this problem. | BEYOND THIS PROBLEM；右側大真桌。 |
| `dense` | Shoot at a slope of the square root of two. The line never hits another lattice point, so with ideal point pockets the ball never stops. Let it run, and its path comes arbitrarily close to every point on the table. | tan θ = √2；球由慢到快（加速）一直彈，淡墨軌跡越疊越密、幾乎鋪滿整張桌子；左欄 Irrational: the line never meets another lattice point, so the ball never stops.、即時計數 bounces so far、Left to run, the path comes arbitrarily close to every point of the table.、小字 (Unfolded, it is one straight line on a torus. Shown here, not proved.)。 |

### 14. `outro`——片尾（無旁白）（6.0 s）
- **畫面：** 置中排版（沿用第三幕 outro 慣例）：小球桌花飾（菱形路徑一圈圈回家）、END OF PROBLEM 7、Square Billiards、(a) infinitely many · (b) none、紅色短線、置中 lockup。

## 重現
```bash
# mock 時序（離線、不計費）
python video/pipeline/tts.py --storyboard video/remotion/q7/q7.yml \
  --scene all --backend mock --unit beat --output-dir video/remotion/public/audio/q7_mock
# 在 video/remotion/ 下
npm ci
npm run q7          # out/q7_mock.mp4
npm run q7:stills   # out/q7_stills/
```
真配音（MiMo，**需先徵得使用者同意**）：`--backend mimo --unit scene --output-dir …/public/audio/q7_scene`，再 `npx remotion render build Q7 out/q7.mp4 --codec=h264 --crf=20 --props='{"manifest":"audio/q7_scene/manifest.json"}'`，最後 `python scripts/loudnorm.py`。

## 中文版（`Q7ZH`，2026-09-26）
- **同一套動畫、另一張字串表：** 畫面字串在 `../src/q7/i18n/zh.ts`（與 `en.ts` 同形狀），排版規則見 [`../STYLE.md`](../STYLE.md)「中文版排版」；用字照 [`GLOSSARY.zh.md`](GLOSSARY.zh.md)（回到中心、鏡像桌、偶數偶數點／奇數奇數點、洞／掉進洞裡、中點測試），每拍畫面文字對照中文旁白 [`q7.zh.yml`](q7.zh.yml)。（`zh.ts` 裡的 `writeup` 是台灣考卷的中文證明寫法，2026-09-26 起中文版不再播這場，字串留著給 `Strings` 型別。）
- **場景清單與英文版不同（2026-09-26 使用者裁決：只改中文版）：**

  | | 共同段 | 結尾 |
  |---|---|---|
  | en（`Q7`） | logo, exam, hook, mirror, unfold, dictionary, halfway, foldback, angles, twist, recap | writeup, epilogue, outro |
  | zh（`Q7ZH`） | 同左（`angles` 少了 `irrational` 拍，停在「a 小題就證完了」） | ext_design, ext_room, ext_family, ext_dense, outro |

  延伸段四場（為什麼偏偏是角落和邊中點／照不亮的房間／同一招的家族／無理斜率）的逐拍畫面設計、事實來源與自驗＝[`EXTENSION.zh.md`](EXTENSION.zh.md)；實作在 `../src/q7/scenes/ExtDesign.tsx`、`ExtRoom.tsx`、`ExtFamily.tsx`，`ext_dense` 是原 `Epilogue.tsx` 的縮短版（`ExtDense`，同一張 √2 畫面、時鐘壓到 `HOLD` 之前跑完）。延伸段的精確幾何（三角形摺疊、紙張三摺的動畫、長方形桌路徑）在 `../src/q7/extGeo.ts`，全是分段線性映射先切斷點再映射，不取樣。延伸段的畫面字串在 `../src/q7/i18n/ext.zh.ts`（中文專屬表，場景用 `useT().ext` 取）。
- **同一來源下只改單一語系的做法（之後其他題目沿用）：**
  1. **語系場景清單：** `Q7_SCENES` 是兩種語言用到的所有場景元件；順序由 `Q7_ORDER[lang]` 決定。manifest 的場景必須與該語系清單逐一相同（`Root.tsx` 的 `calculateMetadata` 會擋），單場 composition 各語系各一組（`Q7-<id>`、`Q7ZH-<id>`，id 的 `_` 換成 `-`，Remotion 不收底線）。
  2. **可選 beat：** 某語系刪掉的拍，場景裡用 `useS().has(id)` 判斷再畫（`Angles.tsx` 的 `irrational`）；`at()`／`p()` 對不存在的拍會擲錯，不會默默跳過。
  3. **語系 HOLD：** `timing.ts` 的 `HOLD` 依語系分表（`HOLD.en`、`HOLD.zh`），`loadShow(manifest, lang)` 套用；語系專屬的停留（例如 zh 的 `ext_dense: 90`）不影響另一語系的時間軸。
  4. **語系專屬字串：** 只有一個語系有的場景，字串放獨立的表（`i18n/ext.zh.ts`，型別＝該表形狀），掛在 `i18n/index.ts` 的 `EXT`；不要為此在另一語系塞空字串。字型分片腳本 `scripts/cjk-subsets.mjs` 與 `cjk.ts` 的字形閘都要把這張表納入。
  5. **驗收：** 另一語系跑一次靜幀逐像素比對（改動前後 diff 全為 0）。
- **中文專屬欄位：** 英文 TeX 裡帶 `\text{bounces}`／`\text{direction}`／`(\text{even},\text{even})` 的三條，中文改排「中文＋行內 TeX」（`foldback.countLine`、`angles.dirLine`、`twist.testLine`）；`recap` 的大 ∞ 用 TeX `\infty`（Pagella），不落到系統字型。`exam` 中文題目頁的段落間距另算（3＋1＋3＋3 行、段距一律 48 px）；`unfold` 的「回到中心」標在鏡像桌中心的正上方（中文比 home 寬，放右下會壓到桌框）。英文版逐像素不變。
- **配音：** MiMo `mimo-v2.5-tts`、voice 冰糖、`--unit beat`（中文沒有逐字對齊；英文版靠 `atWord` 卡字的三處，在中文分鏡是獨立的拍：angles 的 `tan`／`vert`、halfway 的 `list`）。首輪 54 次＋延伸段 19 次，累計 73 次、0 次重試；之後依審核改了延伸段六拍旁白，冰糖重配 6 次（manifest receipt：6 次呼叫、0 次重試）。2026-09-26 含延伸段的成品：1080p、loudnorm −19 LUFS（TP −2.8 dBTP），全片 9 分 09 秒（16483 幀），`out/q7zh_final.mp4`（音訊在 `public/audio/q7zh_beat/`，不進版控）。
```bash
# 真配音（MiMo 計費，需先徵得使用者同意）
python video/pipeline/tts.py --storyboard video/remotion/q7/q7.zh.yml \
  --scene all --backend mimo --unit beat --output-dir video/remotion/public/audio/q7zh_beat
# 在 video/remotion/ 下
npx remotion bundle
npx remotion render build Q7ZH out/q7zh_raw.mp4 --codec=h264 --crf=20 --props='{"manifest":"audio/q7zh_beat/manifest.json"}'
python scripts/loudnorm.py out/q7zh_raw.mp4 out/q7zh_final.mp4
# 任意幀（帶 props）
PROPS='{"manifest":"audio/q7zh_beat/manifest.json"}' node scripts/frames.mjs out/q7zh_stills Q7ZH:1768,2568
```
改了 `zh.ts` 要先跑 `node scripts/cjk-subsets.mjs`（重挑 Noto Serif TC 分片）。render log 的 `[cjk] Noto Serif TC 400/500/600 in use` 證明是打包的字型在畫字；標籤守門與英文版同一套，違規就不出片。

### 局部重渲（只改後段時不必整片重渲，2026-09-26 實測）
改動只影響某幾場、且**場景時長不變**（旁白沒改、`HOLD` 沒改）時，只渲改動那段再接回成品，音軌沿用原成品（已 loudnorm）：
1. 算出受影響第一場的起始幀（`timing.ts` 的 buildShow＋`HOLD` 規則：`from = 前一場結束 − OVER`），在它之前找原成品的關鍵幀：`ffprobe -v error -select_streams v -skip_frame nokey -show_entries frame=pts_time -of csv=p=0 out/q7zh_final.mp4`（×30 換成幀號）。
2. 從那個關鍵幀渲到片尾、不帶音：`npx remotion render build Q7ZH out/seg_tail.mp4 --codec=h264 --crf=20 --muted --frames=<K>-<總幀數−1> --props='{"manifest":"audio/q7zh_beat/manifest.json"}'`。
3. 原成品前段 stream copy 取 K 幀（`-an -c:v copy -frames:v <K>`），與新段用 concat demuxer `-c copy` 接起，再 `-map 0:v -map 1:a -c copy` 套回原成品音軌。
4. 驗收：總幀數與原成品相同、接縫前後幀連續、改動處抽幀確認。
實例：刪 `ext_family` 的「m+n=230」＋修 `ext_dense` 片尾停頓，從關鍵幀 14033 渲到 16482（2450 幀，約 1 分多鐘，整片重渲約 10 分鐘）。若旁白或 `HOLD` 改了導致時長變動，後段音訊也會變，就回到整片渲染＋loudnorm。

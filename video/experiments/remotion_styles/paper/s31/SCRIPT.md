# §3.1 Derivatives of Sine and Cosine——無指引生成版腳本（紙本編輯排版）
> 2026-09-25，motion-designer 子代理。旁白為英文（原文照登），框架說明為繁體中文。旁白源＝[`s31.yml`](s31.yml)（tts.py 格式，`{show <id>}` 切 beat）；畫面＝`../src/s31/`。時長為 mock（150 wpm 估算），換真 MiMo manifest 後全片自動重新對時。
## 敘事取向
我用「先猜、再欠債、再還債」的三段結構來講。開場不講定義，先讓一個點在單位圓上轉，觀眾自己看到高度畫出 sine，再用「弧長＝角度（弧度）所以速度是 1、速度箭頭的垂直分量是 cos」直接**猜出**答案——這是 3Blue1Brown 式的直覺先行，也順手把「為什麼一定要用弧度」埋成伏筆。接著誠實地說「圖只是猜測」，進入正式證明：和差化積把差商拆成兩個因子後，我把「cos 要連續」與「sin θ/θ → 1」寫成旁註欄裡的一本**帳本（OWED）**，之後單位圓面積、夾擠、連續性每付清一筆就在帳本上劃掉蓋章。這個道具把一條容易迷路的長證明變成有進度感的「兩筆債」，也正好利用紙本風格的 Tufte 旁註欄。證完兩個定理後，再回到圖（斜率＝高度，並讓冷開場的小圓回來「對答案」），最後是應用：伴隨極限、其餘四個函數、彈簧、導數循環，並以 s″ = −s 把彈簧和循環串起來，收在連鎖律的預告。
## 設計語彙（本片新增）
- **金色 ochre `#A07C10`**＝「角 θ／弧長／扇形」專用色（dataviz validator：與 crimson、cobalt 全配對通過，deutan ΔE 10.1），讓「弧度＝弧長」在冷開場、面積證明、提醒頁都是同一個顏色。藍＝cos、紅＝導數／切線／強調、墨＝sin 照原設計系統。
- **三種印刷紋理**（45° 墨斜線、金色點描、135° 淡斜線）區分三個巢狀面積，色盲與列印下也分得開。
- **帳本 `Ledger`**：旁註欄的 OWED 清單，付清時紅線劃掉＋PAID IN FULL。
- **轉場**：每場是一張紙，下一張從右邊斜斜滑上來蓋住上一張（帶投影），上一張微微變暗後退——「桌上疊紙」而不是翻頁。部分場景的紙比畫面長（1240–1560 px），鏡頭沿紙往下移。
- **時序**：場長＝0.5 s lead＋旁白秒數＋0.9 s tail，兩場重疊 22 幀；所有揭示用 `at("<beat id>")` 取 manifest 的 beat 起點，程式裡沒有寫死秒數。
## 逐場逐拍
### 1. `circle`——冷開場：圓上的點（C9 預告、C6b 伏筆）（mock 47.6 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Here is a point riding around a circle of radius one. | 無書眉的圖版頁。鏡頭貼近單位圓，圓以筆尖描出，一個點沿圓等速轉動（半徑細線跟著轉）。 |
| `height` | Watch only its height. | 點到橫軸拉出一條粗墨「高度」線，標 *height*。 |
| `trace` | Plotted against the angle, that height traces out the sine curve. | 鏡頭拉遠，右側座標軸畫出；虛線把點的高度水平連到右圖，點轉一圈的同時筆尖畫出 y = sin θ（兩邊縱向同一比例）。 |
| `question` | So here is the question for this whole section. How fast does sine change? | 頁首排出大字斜體標題 *How fast does sine change?*，鏡頭退到整頁。 |
| `speed` | The picture already hints at an answer. Measure the angle in radians, and the angle is exactly the distance travelled along the circle. So the point moves at speed one, and its velocity is an arrow of length one, tangent to the circle. | 右圖淡出、點減速停在 θ≈0.9；從 A 到點的弧以金色（ochre，本片「角＝弧長」的專用色）加粗，標 θ；高度改標 sin θ。右欄旁註 RADIANS：「角 θ 就是金色弧長」；接著切線方向長出單位長的紅色速度箭頭，標 *speed 1*，旁註「速度是單位箭頭、切於圓」。 |
| `vertical` | The vertical part of that arrow is the cosine of the angle. | 鏡頭推近箭頭。箭頭分解：紅色垂直分量、灰虛線水平分量；垂直分量旁標藍色 cos θ；旁註「垂直分量長 cos θ」。 |
| `guess` | So the height should change at the rate cosine. | 右欄 THE GUESS：大式 d/dθ sin θ ≟ cos θ（d/dθ 紅、cos θ 藍，等號上加問號）。 |
| `caveat` | But that is a guess read off a picture. In this section, we earn it. | 紅色斜體註「A prediction read off a picture — not yet a proof.」，鏡頭退回全景。 |

### 2. `title`——節首頁（無旁白）（mock 6.0 s）
- **畫面：** 仿章首頁：左上 §3.1 大號數字，下方以冷開場的小圓（點在轉、紅色速度箭頭）當花飾；右欄標題 *Derivatives of Sine and Cosine*、紅線、斜體副題、四項目錄（點狀引導線、頁碼）；頁腳細線＋品牌 lockup。
### 3. `stuck`——為什麼 sine 不一樣（C1）（mock 53.2 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Every derivative so far came from one recipe. Write the difference quotient, then let h shrink to zero. | 書眉「Why sine resists algebra」。鏡頭貼近上方的導數定義式 f′(x) = lim (f(x+h)−f(x))/h（f′ 紅）。 |
| `square` | For x squared, algebra does the work. Expand, and every term left on top carries a factor of h. | 鏡頭移到左欄 (a) f(x)=x²：差商展開成 (2xh+h²)/h。 |
| `cancel` | Cancel it, and setting h to zero is harmless. The answer is two x. | 下一列兩個 h 被紅線劃掉（\cancel），得 2x+h，再 →(h→0) 紅色 2x；旁註「algebra removed the h」。 |
| `sine` | Now try sine. | 鏡頭移到右欄 (b) f(x)=sin x：寫出 (sin(x+h)−sin x)/h。 |
| `plug` | Set h to zero, and we get zero over zero. And there is no h to pull out of sine of x plus h. | →(h=0) (sin x − sin x)/0 = 紅色 0/0；紅色斜體註「and there is no factor of h to pull out of sin(x + h)」。 |
| `funnel` | As we will see, the whole problem comes down to a single limit: sine theta over theta, as theta goes to zero. It is zero over zero too, and no algebra will crack it. The new tool will be geometry, on the unit circle. | 上半頁變淡，鏡頭沿長紙往下；紅箭頭從 (b) 指向雙線框內的 lim_{θ→0} sin θ/θ（小型大寫「EVERYTHING COMES DOWN TO」）；右側依序排入「Also 0/0 — algebra can’t crack it.」、「The new tool: geometry on the unit circle.」與一個畫了斜線陰影扇形的小單位圓。 |
| `radians` | One rule for the entire section: every angle is in radians. | 左下旁註 CONVENTION：「Every angle in this section is measured in *radians*.」（radians 紅）。 |

### 4. `rewrite`——和差化積改寫差商，欠下兩筆債（C2）（mock 57.2 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | First, a rewrite. One identity turns a difference of sines into a product. | 書眉「Two debts」，小型大寫 SUM TO PRODUCT。 |
| `identity` | Sine A minus sine B equals two, times cosine of the average, times sine of half the difference. It comes straight from the angle addition formulas. | 鏡頭近拍：sin A − sin B = 2 cos((A+B)/2) sin((A−B)/2)（cos 因子藍）；下方灰字「from sin(u+v) − sin(u−v) = 2 cos u sin v」。 |
| `substitute` | Take A equal to x plus h, and B equal to x. The average is x plus h over two. Half the difference is h over two. | 灰字 A = x+h, B = x；鏡頭下移，排出 (sin(x+h)−sin x)/h = 2cos(x+h/2) sin(h/2) / h（token 級 MathStage）。 |
| `split` | Now slide the two down under the h. The difference quotient splits into two factors. | token 動畫：分子的「2」滑到分母 h 後面成 h/2，cos(x+h/2) 滑出分數外，得 cos(x+h/2) · sin(h/2)/(h/2)。 |
| `owe1` | As h goes to zero, the first factor goes to cosine x, as long as cosine is continuous. | cos 因子下方藍箭頭 → cos x，斜體「if cos is continuous ¹」。 |
| `owe2` | The second factor is sine theta over theta, with theta equal to h over two, and theta goes to zero as well. | 比值上方註 θ = h/2 → 0；下方紅箭頭 → sin θ/θ → 紅色「?」，斜體「we need this to be 1 ²」。 |
| `ledger` | So we owe two things. Cosine must be continuous, and sine theta over theta must go to one. Let's pay both debts. | 鏡頭退出，左側旁註欄寫入「OWED」帳本：¹ cos is continuous、² sin θ/θ → 1。這個帳本是全片的主線道具，之後每付清一筆就用紅線劃掉並蓋「PAID IN FULL」。 |

### 5. `areas`——單位圓上的三個面積（C3）（mock 71.2 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Draw the unit circle, and an angle theta between zero and a right angle. | 書眉「Paying the debts: areas」。鏡頭近拍：座標軸、四分之一單位圓描出，角 θ 從小角度張開到約 45°，金色角弧。 |
| `points` | Mark A at the point one, zero. B on the circle, at cosine theta, sine theta. And C straight above A, on the tangent line, at height tangent theta. | 標出 A=(1,0)、B=(cos θ, sin θ)、C=(1, tan θ) 三點，x=1 的切線以虛線畫出。 |
| `tri1` | The triangle O A B has base one and height sine theta. Its area is one half sine theta. | 三角形 OAB 填 45° 墨色斜線，B 的鉛垂虛線標 sin θ、底標 *base 1*；右欄 THREE NESTED AREAS 第一列：斜線色票＋△OAB: ½·1·sin θ。 |
| `sector` | The sector O A B contains that triangle. Because theta is in radians, the sector's area is one half theta. | 扇形 OAB 填金色點描；右欄第二列 sector OAB: ½θ（θ 金色），金色斜體註「true in radians」。 |
| `tri2` | And the big triangle O A C contains the sector. Its area is one half tangent theta. | 大三角形 OAC 填 135° 淡斜線，標 tan θ；右欄第三列 △OAC: ½·1·tan θ。三種印刷紋理對應三個面積，不靠顏色辨識。 |
| `chain` | Three nested shapes, three ordered areas. Double everything. Sine theta is at most theta, which is at most tangent theta. | 鏡頭推到右欄：½sin θ ≤ ½θ ≤ ½tan θ，紅字「× 2」，下一列 sin θ ≤ θ ≤ tan θ。 |
| `divide` | Divide through by sine theta, and flip. Cosine theta is at most sine theta over theta, which is at most one. | 灰斜體「divide by sin θ, then take reciprocals:」→ 1 ≤ θ/sin θ ≤ 1/cos θ → 紅框 cos θ ≤ sin θ/θ ≤ 1，式號 (1)。 |
| `even` | We took theta positive. But sine theta over theta is an even function, so negative theta gives the same bounds. | 鏡頭沿長紙下移，左下 NEGATIVE θ：sin(−θ)/(−θ) = −sin θ/(−θ) = sin θ/θ，斜體「an even function: the same bounds hold on both sides」。 |
| `bonus` | And there is a bonus. The size of sine theta is never more than the size of theta. | 右下 BONUS：|sin θ| ≤ |θ|。 |

### 6. `continuity`——第一筆債：連續性（C4）（mock 35.6 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | That bonus pays the first debt. | 書眉「Debt 1: continuity」。左側帳本第 1 筆有紅色焦點條；主欄 FROM THE BONUS：|sin θ| ≤ |θ|。 |
| `squeeze` | The size of sine theta sits between zero and the size of theta. As theta goes to zero, it is squeezed to zero. | 帳本淡出（鏡頭要推近）。右上小圖：|θ| 的 V 形（淡墨）、|sin θ| 的曲線、兩者之間灰色帶；紅色豎線在 θ 處量出 |sin θ|，θ 一路滑向 0 被夾扁。主欄排入 0 ≤ |sin θ| ≤ |θ| ⟹ lim sin θ = 0。 |
| `gap` | Now compare sine at two nearby points. The same product identity bounds the gap. It is at most twice the size of sine of half the distance. | TWO NEARBY POINTS：|sin x − sin x₀| = 2|cos((x+x₀)/2)||sin((x−x₀)/2)|，下一列 ≤ 2|sin((x−x₀)/2)|，灰註「since |cos| ≤ 1」。 |
| `shrink` | As x approaches x naught, that bound shrinks to zero. So sine x approaches sine x naught. | 同列接上 ≤ |x−x₀| →(x→x₀) 紅色 0；下一列 lim_{x→x₀} sin x = sin x₀。 |
| `cosgap` | Cosine obeys the very same bound. | 藍色 cos 版本：|cos x − cos x₀| ≤ 2|sin((x−x₀)/2)| ⟹ lim cos x = cos x₀。 |
| `paid` | So sine and cosine are continuous, everywhere. First debt paid. | 鏡頭退回全頁，帳本回來，第 1 筆被紅線劃掉、蓋 PAID IN FULL。 |

### 7. `limit`——第二筆債：基本極限（C5）（mock 32.8 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Now the second debt. Here is the graph of sine theta over theta. | 書眉「Debt 2: the key limit」，THE SQUEEZE。θ ∈ [−π, π] 的座標，墨色 y = sin θ/θ 畫出，θ=0 處是空心圈（該點無定義）。 |
| `bounds` | And here are the two bounds from the areas. Above it, the constant one. Below it, cosine theta. | y = 1 灰線與藍色 y = cos θ 畫出，|θ| < π/2 範圍內兩者之間鋪灰色帶。 |
| `pinch` | Cosine is continuous, so as theta goes to zero, it climbs to one. The ratio is trapped between two things that both go to one. | 鏡頭推近 θ=0（×2.3）。±θ 兩處各一條紅色豎線從 cos θ 量到 1，比值的點夾在中間，隨 θ → 0 一起被壓扁；紅字 *trapped*。 |
| `value` | So the limit of sine theta over theta, as theta goes to zero, is one. | 鏡頭拉回；頁首排出 lim_{θ→0} sin θ/θ = 1（1 紅），空心圈外加紅圈；灰斜體「cos θ → 1 because cosine is continuous — the debt we paid first」。 |
| `paid` | The ratio is even, so both sides agree. Second debt paid. | 左側帳本出現，第 2 筆劃掉、PAID IN FULL（兩筆都付清）。 |

### 8. `warnings`——兩個提醒（C6）（mock 40.4 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Two warnings, before we cash this in. | 書眉「Two cautions」，頁面中間一條細豎線分兩欄。左欄 CAUTION 1「A limit, not an identity」。 |
| `identity` | First, this is a limit, not an identity. At theta equal to pi over two, the ratio is two over pi, about zero point six four. At pi, it is zero. Only near zero is the ratio close to one. | 鏡頭推左欄：θ ∈ [0, π] 的 sin θ/θ 小圖，θ=0 空心圈、y=1 虛線；π/2 處紅色高度線標 2/π ≈ 0.64，π 處紅點；下方式子 sin(π/2)/(π/2) = 2/π ≈ 0.64、sin π/π = 0，斜體「Only near 0 is the ratio close to 1.」。 |
| `degrees` | Second, radians are not optional. The sector area, one half theta, only holds in radians. | 鏡頭橫移右欄 CAUTION 2「Radians are not optional」：一個金色弧的小扇形，sector area = ½θ，斜體「holds only when θ is the arc length — radians」。 |
| `factor` | Measure in degrees, and the limit comes out as pi over one hundred eighty. That factor follows you into the derivative. The derivative of sine of x degrees is pi over one hundred eighty, times cosine of x degrees. | lim_{x→0} sin(x°)/x = π/180（紅），斜體「and the factor follows you into the derivative:」，d/dx sin(x°) = (π/180) cos(x°)。最後退回兩欄全景。 |

### 9. `payoff`——兩個定理（C7、C8）（mock 32.4 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Now we collect. Here is the difference quotient, split in two. | 書眉「The two derivatives」，COLLECTING：重寫 (sin(x+h)−sin x)/h = cos(x+h/2) · sin(h/2)/(h/2)。 |
| `limits` | As h goes to zero, the first factor goes to cosine x, by continuity. The second goes to one, by the key limit. | 兩因子下方各一支箭頭：藍 → cos x「by continuity ¹」，紅 → 1「by the key limit ²」（上標呼應帳本編號）。 |
| `theorem` | So the derivative of sine x is cosine x. | 鏡頭拉開；紅色豎線＋THEOREM 1：d/dx sin x = cos x（大字，d/dx 紅、cos x 藍）。 |
| `cosine` | Cosine goes the same way. Its product identity carries a minus sign, so the quotient becomes minus sine of x plus h over two, times the same ratio. | 鏡頭下移：灰字「with cos A − cos B = −2 sin((A+B)/2) sin((A−B)/2):」，再排 (cos(x+h)−cos x)/h = −sin(x+h/2) · sin(h/2)/(h/2) ⟶ −sin x。 |
| `theorem2` | So the derivative of cosine x is minus sine x. | THEOREM 2：d/dx cos x = −sin x，鏡頭退回全頁。 |

### 10. `slope`——斜率＝高度（C9）（mock 28.0 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Here is what the first theorem means in a picture. | 書眉「Slope equals height」。上圖 y = sin x（0 到 2π，Tufte range-frame 軸）畫出。 |
| `tangent` | Slide a tangent line along the sine curve, and read off its slope. | 紅色切線以彈簧長出，沿曲線滑動；切線上刻字 *slope 0.xx* 即時讀數。 |
| `cosine` | Underneath, draw cosine. | 下圖 y = cos x（藍）畫出。 |
| `match` | At every x, the slope of sine equals the height of cosine. | 上圖出現斜率三角形（單位水平虛線＋紅色升高），下圖在同一 x 畫出等長紅色高度條，讀數 *height 0.xx*；兩圖間鉛垂點線；左旁註 FIGURE 3.1 說明「紅色升高與下方紅條永遠等長」。 |
| `peak` | Where sine peaks, its tangent is flat, and cosine crosses zero. | 切點停在 π/2：切線水平，紅字 *flat tangent*；下圖 cos 過零，紅字 *cos = 0*。 |
| `circle` | It is the same fact the circle suggested at the start. The height of the point changes at the rate cosine. | 左旁註欄出現冷開場的小圓：同一角度的點、淡紅速度箭頭與紅色垂直分量（＝cos x）；斜體「The circle agrees: the point’s height changes at rate cos x.」；切點繼續滑到 2π 附近。 |

### 11. `companion`——伴隨極限（C10）（mock 26.8 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | The key limit unlocks others. Take one minus cosine theta, over theta. | 書眉「A companion limit」，THE KEY LIMIT, REUSED：(1 − cos θ)/θ，等號對齊成一欄。 |
| `conj` | Multiply top and bottom by one plus cosine theta. | = (1 − cos θ)/θ · (1 + cos θ)/(1 + cos θ)（乘上的因子紅）。 |
| `pythag` | The top becomes one minus cosine squared, which is sine squared. | = (1 − cos²θ)/(θ(1 + cos θ)) = 紅色 sin²θ/(θ(1 + cos θ))，左註「sin² + cos² = 1」。 |
| `factor` | Split it. Sine theta over theta, times sine theta over one plus cosine theta. | = sin θ/θ · sin θ/(1 + cos θ)。 |
| `evaluate` | The first factor goes to one. The second goes to zero over two, which is zero. So this limit is zero. | 兩因子下箭頭：紅 → 1，灰 → 0/2 = 0；紅框結論 lim_{θ→0} (1 − cos θ)/θ = 0。 |

### 12. `four`——其餘四個三角函數（C11）（mock 35.2 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | With sine and cosine in hand, the other four follow from the quotient rule. | 書眉「The other four」，QUOTIENT RULE。 |
| `tan` | Tangent is sine over cosine. | d/dx tan x = d/dx (sin x / cos x)。 |
| `quotient` | The quotient rule gives cosine times cosine, minus sine times minus sine, all over cosine squared. | = (cos x · cos x − sin x · (−sin x)) / cos²x（cos 藍）。 |
| `one` | The top is cosine squared plus sine squared, which is one. | = (cos²x + sin²x)/cos²x（分子紅）= 1/cos²x。 |
| `sec` | So the derivative of tangent is secant squared. | = sec²x，灰註「wherever cos x ≠ 0」；右側 booktabs 三線表 TABLE 3.1 出現第一列 tan x | sec²x。 |
| `table` | The same steps give the other three: secant, cotangent and cosecant. Each holds wherever its denominator is not zero. | 鏡頭橫移到表：依序排入 sec x | sec x tan x、cot x | −csc²x、csc x | −csc x cot x，表下註「each wherever its denominator is not zero」。 |
| `co` | Notice the pattern. Every function whose name starts with co picks up a minus sign. | cot、csc 的「co」下加紅底線、導數的負號轉紅；紅色斜體「Every co-function picks up a minus sign.」，鏡頭退回全頁。 |

### 13. `spring`——彈簧上的重物（C12）（mock 27.6 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Now hang a weight on a spring, and let it bob. | 書眉「A weight on a spring」。左側：斜線天花板、鋸齒彈簧、黑色重物上下擺動（真的依 sin t 運動），靜止位置虛線。 |
| `position` | Say its height is sine t. | 右側第一張小圖 s(t) = sin t（墨），有時間游標與點跟著重物同步；標 *height*。 |
| `velocity` | Its velocity is the derivative, cosine t. | 第二張 s′(t) = cos t（藍），標 *velocity*。 |
| `accel` | Its acceleration is the derivative again, minus sine t. | 第三張 s″(t) = −sin t（紅），標 *acceleration*。 |
| `law` | That is minus the height itself. | 鏡頭推到下方：紅框 s″ = −s。 |
| `arrow` | So the acceleration always points back toward the rest position, and it grows with the distance from it. This is simple harmonic motion, and sine and cosine both obey it. | 重物旁長出紅色加速度箭頭，永遠指回靜止位置、長度與位移成正比；左下 SIMPLE HARMONIC MOTION 與說明文字；鏡頭退回全頁。 |

### 14. `cycle`——導數循環（C13）（mock 29.6 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | Keep differentiating sine. | 書眉「The derivative cycle」，DIFFERENTIATE AGAIN, AND AGAIN；圓環頂端 sin x。 |
| `step1` | Sine goes to cosine. | 順時針紅色彎箭頭（小 d/dx 標記）通往右側藍色 cos x。 |
| `step2` | Cosine goes to minus sine. | → 下方 −sin x。 |
| `step3` | Minus sine goes to minus cosine. | → 左側藍色 −cos x。 |
| `step4` | And minus cosine comes back to sine. Four steps, and we are home. The fourth derivative of sine is sine. | → 回到 sin x；環中央 d⁴/dx⁴ sin x = sin x，斜體「four steps, and home」；鏡頭拉開。 |
| `compare` | Compare e to the x, which returns to itself in a single step. Sine and cosine reach their own negatives in two steps. That is the spring law again. The second derivative is minus the function. | 右側：e^x 上方一個紅色自我迴圈「one step back to itself」；環外一道金色半圈從 sin x 繞到 −sin x，金色 d²/dx² sin x = −sin x，斜體「half a turn: two steps give the negative — the spring law s″ = −s」。 |

### 15. `next`——往下一節（C14）＋片尾 lockup（mock 17.2 s）
| beat | 旁白（英文原文） | 畫面 |
|---|---|---|
| `start` | So now we can differentiate sine x itself. | 無書眉的收尾頁。灰斜體「We can differentiate」＋大字 d/dx sin x。 |
| `inside` | But what about sine of x squared, or sine of three x plus one? A function inside a function. | 紅斜體「but what about」，兩側 sin(x²)、sin(3x+1)，內層函數以金色標出；斜體「a function inside a function」。 |
| `chain` | That needs one more tool, the chain rule. It is the subject of the next section. | 上半淡去，細線下排 NEXT · SECTION 3.2、*The Chain Rule*、置中品牌 lockup、END OF SECTION 3.1。 |

合計旁白音訊（mock）約 541 s；成片長度見 render 回報。

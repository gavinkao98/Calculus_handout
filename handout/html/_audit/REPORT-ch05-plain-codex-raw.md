# ch05 平實化回填 — Codex gate-2 裁決（raw 照登）

> 產出：`codex exec -s read-only`（gpt-5.6-terra，reasoning effort max），2026-07-26。
> 材料全部 inline 進 prompt（66.4 KB；本機讓 Codex 自讀 fragment 會把 UTF-8 解成亂碼——2026-06-28 實證）。
> 送審材料＝`REVIEW-ch05-plain-walk.html` 抽出的 115 條候選 ＋ 判準節錄 ＋ KEEP／不報清單。
> **本檔為 raw 照登，未經整理。** 整合結果見 `REVIEW-ch05-plain-applied.html`。

```text
VERDICT: 90 ADOPT, 24 MODIFY, 1 REJECT

（計數只對應 115 條有 AFTER 的候選；K1–K7 與「不報」項為額外複核，均維持不動。）

§5.1

A1 ADOPT — 冒號只引出清單，scope 與列舉均未變。

A4 ADOPT — 兩個教學動作分開，乘法法則與 \(dy/dx\) 的來源都清楚。

A5 MODIFY — 逗號後的方法名稱成了鬆散、近乎懸空的同位語。
改寫: by following the composition-identity route and differentiating the identity \(\arcsin(\sin x) = x\).

A7 ADOPT — 垂直切線與無法寫成 \(y=f(x)\) 的結論均保留。

A2 ADOPT — 例子與「無單一 \(y=f(x)\)」是兩個可獨立理解的教學動作，拆開正確。

A3 ADOPT — `agrees with` 直白，且負倒數的數學關係完整保留。

A6 MODIFY — `a relation that its defining function satisfies` 指涉不清，也未明說要解的是導數。
改寫: Implicit differentiation is the general framework behind that method. For an inverse function, differentiate the relation that defines the inverse and solve for its derivative. This works on any branch where the inverse is differentiable and the division that solving requires is legitimate.

A8 MODIFY — AFTER 仍有 `goes infinite`、`turns into`、`has broken down`；警告句應完全字面化，並保留 branch 限定。
改寫: Use this as a practical check. A formula for \(dy/dx\) that is unbounded or has the form \(0/0\) is a warning that the branch assumption needs separate analysis. It may indicate a vertical tangent, a self-crossing, or another singular point, where the chosen branch may no longer be described by \(y\) as a function of \(x\).

A9 ADOPT — concave down 的前向術語說明具有獨立用途，拆句正確。

AL1 ADOPT — 已把擬人化的 `feeds on` 改成直接描述。

AL2 ADOPT — `simplify` 與 `typical` 均平實且語意未漂移。

AL3 MODIFY — 第二句的 `That` 比原本的 `That liberty` 更不明確。
改寫: Implicit differentiation is less a new rule than a new way to use an old one: the chain rule, applied to an equation instead of a formula. This use of the chain rule is what the next section needs.

AL4 ADOPT — `locate` 是適當的字面動詞。

§5.2

B1 ADOPT — 因果關係前置後仍保留與 §5.1 的平行。

B2 ADOPT — 破折號內的 chain-rule 說明可獨立作為失敗原因，三句重寫合理。

B3 ADOPT — 時點限制仍附著在同一指令上。

B4 ADOPT — 速率結果與其位置無關的說明分開，節奏較好。

B5 ADOPT — 橋接的兩個問題分句後仍保有導航功能。

BL1 ADOPT — 物理意義改為字面描述，薄殼的理由未失。

BL2 ADOPT — 明確指出以 \(t\) 微分。

BL3 ADOPT — `records the geometry` 足夠直白且保留符號意義。

BL4 ADOPT — 已明說 differentiating gives rates，而非以 ferrying/hiding 載意。

§5.3

C1 ADOPT — 那條線的識別本來就是獨立定義資訊，拆句正確。

C4 ADOPT — remainder 的精確差量與小 \(dx\) 下的近似關係都保留。

C5+C7 ADOPT — 末句的結論已由前句「genuine ratio…equals the derivative exactly」完整承載，刪除不失教學論點。

C6 MODIFY — `The upgrade works forward, not backward` 仍把時間 scope 藏在修辭中。
改寫: This definition applies from this point onward, but it does not justify the earlier chain-rule manipulations that looked like cancelling \(dx\)'s. Those manipulations were licensed by Theorem 3.3, not by this definition. From here on, \(dx\) may be treated as a real quantity when a computation is written out, and integral calculus uses this fact when a change of variable is expressed entirely through the differential.

C9 MODIFY — AFTER 漏掉了原文的 local 限定，容易讀成把函數整體等同於切線。
改寫: Reading a function locally as its tangent line recurs throughout calculus and is generalized to curved approximations in Chapter 11 and to surfaces in Chapter 14.

C2 ADOPT — 條件與結果仍在同一論述動作中，無數學漂移。

C3 ADOPT — 經典記號與 differentials 的關係更直接。

C8 MODIFY — `surfaces` 與 `the same holds` 沒把一般化內容明說。
改寫: three times the relative error in the radius, with the exponent \(3\) as the multiplier. For any power law, the corresponding relative-error approximation uses the exponent as the multiplier.

CL1 ADOPT — 已刪除不透明的 `at face value` 與 `puts it to work`。

CL2 ADOPT — `reliable only locally` 是精確且平實的 caution。

CL3 ADOPT — 保留 slope 與 nearby prediction 的雙重作用。

CL4 REJECT — 原句短、動機與理由是一個完整教學動作；僅為去分號而拆句屬過度處置。

§5.4

D3 ADOPT — 單破折號 gloss 改為逗號同位語合適。

D5 ADOPT — 補出 \(0\) 後，曲線通過的位置更明確。

D6 ADOPT — domain 與 critical number 的推論完整保留。

D7 ADOPT — endpoint lesson 獨立成句，清楚且自然。

D11 ADOPT — `require` 是合適的中性動詞。

D13 ADOPT — 對 \(x^3\) 的對比與 vertical tangency 都未丟失。

D14 ADOPT — 下一節的 optimization 對象與 modelling 都保留。

D1 MODIFY — `can occur only at` 必須明確受前述假設限制；`the derivative is built to find them` 也仍偏擬人。
改寫: Of all the questions calculus answers, the one that comes up most often in practice is: where is a quantity largest or smallest? Maximum profit, minimum cost, least material, and greatest range all ask for an extreme value of a function, and the derivative helps us find them. … Under these conditions, an extreme can occur only at one of a short list of places, and the work is to list and test them.

D2 MODIFY — a notion 不會 `call a value`；改成直接定義較清楚。
改寫: Alongside these is the local notion of a value that is largest or smallest only in comparison with nearby points.

D4 MODIFY — 這裡應直接點名 Fermat’s theorem，避免 `This` 在關鍵轉折處回指含混。
改寫: Fermat’s theorem is the main tool for locating extrema. It reduces the search from a whole interval to a finite list of candidates.

D8 ADOPT — 正確保留「不判定 character」：只說 Closed Interval Method 不告訴我們 local max、local min 或 neither。

D10 ADOPT — 先辨識同兩個 interior values，再由 First Derivative Test 說明角色，順序正確。

D15 ADOPT — 條件前置後，第二導數符號作為分類工具的角色更清楚。

DL1 ADOPT — 修正 `engine`，且不因 cleft 形式誤報。

DL2 ADOPT — larger/smaller 的字面比較正確給出 local extremum。

§5.5

E1 MODIFY — `a more extreme value` 沒有說清 maximization 與 minimization 的比較方向。
改寫: When that interval is open, as it is for a radius ranging over \(r > 0\), the Closed Interval Method does not apply directly. Instead, use the sign of the derivative around the single interior critical number to confirm that the extremum occurs there. Finally, check that, as the variable approaches either end of its range, the quantity does not approach a value larger than the value at that critical number when maximizing or smaller than it when minimizing.

E2 ADOPT — EVT 的存在性與 endpoints/interior 的比較鏈完整。

E3 ADOPT — 長度分配與一般 balance 分成兩個動作，數學未變。

E4 ADOPT — 括號適合簡短的 `that is` 釋義。

E5 ADOPT — 兩個 parenthetical 句子仍構成同一個模型限制提醒。

E6 ADOPT — 面積比較與長寬比清楚分開。

E7 ADOPT — 第二導數的角色已直接說出。

EL1 ADOPT — 正確說明兩端都不能提供較小面積。

§5.6

F1 ADOPT — 直接引入 concavity，消除模糊的 `That distinction`。

F3 MODIFY — `the derivative can test` 與 `by the sign` 不如直接說明操作。
改寫: We can test whether \(f'\) is increasing by looking at the sign of \((f')' = f''\). Thus concavity is determined from the second derivative.

F2 ADOPT — slope increases 是 counter-clockwise turning 的直接解釋。

F4 ADOPT — 定義條件與兩種方向均保留。

F5 ADOPT — `no inflection point there` 比殘句更清楚。

F6 ADOPT — `has the same sign as` 是直接且數學正確的說法。

F7 ADOPT — 第一個句子已字面說明 test gives no information。

F8 ADOPT — Second Derivative Test 的優勢與條件均保留。

F9 MODIFY — AFTER 的 `all of it` 回指較鬆，且把原有主從關係倒置。
改寫: The first two derivatives provide the full vocabulary for the shape of a graph: rise and fall, peak and valley, cupping and inflection.

F10 ADOPT — L’Hôpital’s rule 與其用途分開後清楚。

FL1 MODIFY — `turns` 不說明是 concavity 的變化，且破壞本節術語一致性。
改寫: Near the origin, the curve is concave up, flattens, and becomes concave down. It remains concave down through the middle and is concave up once more past \(x = 2\).

§5.7

G1 ADOPT — \(f'/g'\) 的資訊角色改為字面說明，無數學變更。

G2 MODIFY — 結論方向正確，但應明示 Rolle 產生的矛盾及 \(g'(c)\ne0\) 的來源。
改寫: For the ratio form, if \(g'(x) \ne 0\) on \((a, b)\), then \(g(b) \ne g(a)\). If \(g(b) = g(a)\), Rolle’s theorem applied to \(g\) would give a point in \((a, b)\) where \(g'\) is zero, contradicting the hypothesis. Since \(c\) lies in \((a, b)\), both \(g(b) - g(a)\) and \(g'(c)\) are nonzero, so dividing by \([g(b) - g(a)]\,g'(c)\) is legitimate.

G4 MODIFY — 「兩者有有限極限」還不足；分母極限必須非零，否則仍可能是 \(0/0\)。
改寫: If the numerator and denominator have finite limits and the denominator’s limit is nonzero, the limit is not indeterminate. Applying the rule is then unjustified and may give a wrong answer.

G6 MODIFY — `large` 與 `small` 沒有字面表達所需的極限關係。
改寫: This is not an indeterminate form at all. As the numerator becomes arbitrarily negative while the denominator remains positive and approaches zero, the quotient becomes arbitrarily negative:

G10 ADOPT — 清單是章節結論的實質內容，前置後不再失去 `the last of these` 的先行詞。

G3 ADOPT — proof fence 與 §D.3 的數學政策均未動。

G5 ADOPT — failed application 的不充分性說得正確。

G7 ADOPT — `not merely … but …` 是清楚的對比，不需額外改寫。

G8 MODIFY — rule 不會 `accept` 一個 form；操作指令應直說 applicability。
改寫: Recast it as a quotient to obtain a form to which the rule applies. Put the \(\ln x\) on top and \(1/x\) below:

G9 MODIFY — \(0^0\) 的重點是無法決定極限值，不是「不能預測」。
改寫: thus approaches \(1\) as \(x \to 0^{+}\). The bare form \(0^{0}\) alone does not determine that value.

GL1 ADOPT — `cannot be read off directly` 直接且自然。

GL2 ADOPT — `tend to \(\infty\)` 取代 race 的比喻。

GL3 ADOPT — `useful in itself` 平實。

GL4 ADOPT — `come with the rule` 清楚。

GL5 ADOPT — 每次 application 的效果正確。

GL6 ADOPT — 與前句的 growth vocabulary 一致。

GL7 ADOPT — 清楚要求檢查 hypotheses。

GL8 ADOPT — `systematic procedure` 合適。

§5.8

H1 ADOPT — 三種 asymptote 的獨立教學動作正確拆開，數學條件完整。

H7 ADOPT — 章節問題的清單具有獨立 recap 用途，改寫正確。

H8 MODIFY — `no formula gives` 過度絕對；應限於已給定的公式無法直接提供解。
改寫: Instead of describing a known function, the section asks how to find a solution of \(f(x) = 0\) when the formula does not give that solution directly. It uses the tangent line as a tool for approximation.

H2 ADOPT — even 的 gloss 可用逗號附著。

H3 ADOPT — odd 的 gloss 與 H2 平行。

H4 ADOPT — local maximum/minimum 值的反直覺比較已獨立說明。

H5 ADOPT — `suggest a false rule` 平實且保留 caution。

H6 ADOPT — vertical asymptote 的 nearby-value 性質與 isolated value 的無關性均清楚。

HL1 ADOPT — 過渡句仍有明確導航作用。

HL2 ADOPT — 去除 machinery 後不失「由描述轉為求根」的方向轉換。

§5.9

J1 MODIFY — `roots that no explicit formula gives` 對該 cubic 過強；Cardano 公式存在，只是不是 simple factoring。
改寫: Many equations \(f(x) = 0\) have roots that are not given by a simple formula. The cubic \(x^{3} - x - 1 = 0\) cannot be solved by simple factoring, and a transcendental equation like \(\cos x = x\) has no elementary closed form at all. Yet the roots are real and can be located to any precision. Newton’s method is how they are located, and it rests on the linear approximation of §5.3…

J6 MODIFY — `its` 可回指 derivative 或 function；章摘要應直接點名 function。
改寫: the derivative, a statement about one instant, controls the behaviour of a function across whole intervals, including the function’s rise and fall, its extremes, its bends, and its roots.

J7 ADOPT — 反向問題與 FTC 的 inverse 結論分開後更清楚。

J3 ADOPT — 在此 elementary Newton procedure 中，\(f'(x_n)=0\) 的確使下一步無法照公式取得。

J4 ADOPT — rapid doubling 的語意與 simple root 條件都保留。

J5 ADOPT — simple factoring 的限制沒有擴張為「完全不能解」。

JL1 ADOPT — `not always reliable` 是適當的平實 caution。

JL2 ADOPT — `gives no next iterate` 正確描述水平切線的問題。

JL3 MODIFY — 直接刪除會少掉一種失敗機制；應把「turns the wrong way」換成可檢查的切線幾何描述。
改寫: If the starting guess is too far from a root, or is in a region where the curve bends so that the tangent line crosses the \(x\)-axis beyond the root, the iterates can overshoot…

JL4 ADOPT — `move away from the root instead` 直接保留 divergence 的意思。

JL5 ADOPT — 已去除 `blind`，而 sketch 的教學價值仍在。

副表

S1 ADOPT — 輸出型態與數值代入指令分開正確。

S2 ADOPT — 含清單的插入語改括號符合規則。

S3 ADOPT — caption 的比較指令獨立成句自然。

S4 ADOPT — `the feasible domain` 作逗號同位語可讀且無歧義。

S5 MODIFY — `until an answer emerges` 沒有說明重複操作的停止條件。
改寫: apply it again, differentiating repeatedly until the quotient is no longer an indeterminate form.

S6 ADOPT — 冒號引出公式，屬 tic guard 的豁免類型。

S7 ADOPT — caption 中的 `all read off the checklist` 可由前項清楚回指。

S8 ADOPT — 起始猜測與其兩個取得方法分句後清楚。

KEEP 複核

K1 REJECT — 應維持 KEEP；區間記號只是同一連續／可微條件的規格。

K2 REJECT — 應維持 KEEP；正負兩側只是「不變號」的必要條件說明。

K3 REJECT — 應維持 KEEP；good starting guess 是收斂的時點／必要條件修飾。

K4 REJECT — 應維持 KEEP；定理條列中的左右號誌是正式條件 gloss。

K5 REJECT — 應維持 KEEP；四個無動詞尾語需保持 proof skeleton 的平行。

K6 REJECT — 應維持 KEEP；與 `— only then —` 的具約束力先例同型。

K7 REJECT — 應維持 KEEP；caption 中的長度規格只修飾同一布局主張。

不報複核

NR1 REJECT — `resists solving for \(y\)` 保留了「不易／不適合」而非錯誤的不可解斷言，且有鄰近字面說明。

NR2 REJECT — cups/water/sheds 是可視化的 informal gloss，不是唯一數學載體。

NR3 REJECT — point/formula 的區分是具體且有用的結論。

NR4 REJECT — derivative 的暖句四條件均通過。

NR5 REJECT — modelling 是本節的實質教學重點，不是空泛氣氛句。

NR6 REJECT — `outruns`、`flat spot`、`pins down` 都有鄰近字面內容，且對 EFL 可推測。

NR7 REJECT — cleft 只是 FLAG，不構成 finding。

NR8 REJECT — 81 詞／19 式的 proof 段是一個論證 skeleton，未達段落 trigger，也不應機械拆分。

Q1：沒有應由 CUT 改判 KEEP 的成對破折號。Gate-1 沒有把步驟②判得過寬。最接近邊界的是 B2，但 `the very thing the chain rule was about to produce` 可獨立說明為何遺失 rate 是致命錯誤；A2、E1、J1 的例子，C1、G1、H8 的定義性內容，以及 G10、H7 的章節回顧清單，也都有獨立教學用途。K1–K7 才是純規格、時點、必要條件或平行 gloss，KEEP 正確。

Q2：K1–K7 全部正確；不報清單也都應維持不動。沒有發現需要新增的、未列出的 BEFORE finding。唯一要補的殘留問題都已在既有 locus 內：G8 的 `the rule accepts` 與 S5 的 `until an answer emerges`，故分別改判 MODIFY，而非新增掃描命中。

Q3：主要風險如下。A6 必須保留「chosen branch、inverse differentiable、legal division」三層條件，且不可引入 seam-guard 禁止的公式。D1 的 `only at` 必須受既有假設限制。D8 的 AFTER 安全，因為它沒有把 Closed Interval Method 說成能判定 interior critical number 的 character。E1 的 `more extreme` 不分最大／最小方向，已補成明確比較。G2 原方向正確，但宜明示 Rolle 的矛盾與 \(c\in(a,b)\)。G4 原 AFTER 漏掉分母極限非零，這是實質數學缺口。G6 必須說明「負到無界、正分母趨零」而非泛稱 large/small。H8 與 J1 的 `no formula gives` 都過度絕對；J1 特別不能否認 cubic 的 Cardano 公式。JL3 不宜直接刪除，因為會少掉曲率／切線導致越根的風險。另有較小但真實的 scope/reference 風險：C9 漏掉 local，J6 的 `its` 可回指兩個不同名詞。

Q4：沒有看到需要合回的段落。H1 是最接近的案例，但它的節奏是中—短—短—中—長，沒有連續三句同長。A8、C6、E1、G2、J1 的拆句也都保有明顯長短差；G2 即使三句相連，仍屬 proof skeleton。無需為節奏把任何兩句重新合併。
tokens used
```

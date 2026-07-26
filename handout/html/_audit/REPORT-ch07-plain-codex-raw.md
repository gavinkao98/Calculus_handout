# Codex gate-2 raw：ch07 散文平實化回填（合併 sweep）逐條裁決

- **調用**：`codex exec -s read-only`（stdin 餵 UTF-8 prompt、`--output-last-message` 收檔；材料**全 inline**、未讓 Codex 讀檔——遵循 2026-06-28 編碼坑紀律），模型走 `~/.codex/config.toml` 預設。
- **日期**：2026-07-26。**授權**：使用者本輪明示「跑 Codex Gate 2」（`CLAUDE.md` 2026-07-01 Codex 唯讀逐次徵詢條款）。
- **受審材料**（prompt 164.7 KB）：gate-1 走查的 **155 條**提案（前→後全句，含 12 條 KEEP／判定不拆）＋ `CONTENT_SPEC.md` §3〈平實英文條款〉RC 條款節錄（含四步仲裁決策序、CUT palette、先例、不換 tic 護欄）＋ `PROSE-AUDIT-RUBRIC.md` 的 R 維度與擋稿線＋ch07 canon-章背景與 Gate 0 基線＋「刻意保留」7 項＋fragment 檔頭的 SEAM GUARD 四條＋**Chapter 7 七節完整散文**（逐段，供判「未改的判斷是否正確」）＋Q1–Q7。
- **走查稿**：[`REVIEW-ch07-plain-walk.html`](REVIEW-ch07-plain-walk.html)；**整合裁決與執行結果**：[`REVIEW-ch07-plain-applied.html`](REVIEW-ch07-plain-applied.html)。
- 本檔為 **raw 輸出照登**（未刪改一字）。折入時的逐條處置見 applied 報告 §4 與該輪 commit body。

**摘要**：`VERDICT: ADOPT 116 / MODIFY 39 / REJECT 0`。最終執行 **146 條**：ADOPT 116 條照原提案；MODIFY 39 條中**採納 38**（16 條照 Codex 原稿、22 條取其抓到的缺陷但改用我的版本，因 Codex 多處順手把語域一起壓平）、**駁回 1**（B-01，理由見 applied §4）。Codex 另**改判 3 條我原判 KEEP 的成對插入語**（B-02／B-25／B-30），四步仲裁複核後全部採納——這是最終密度 1.57 低於走查投影 2.25 的主因。Codex 另抓到一個**本輪範圍外的數學缺口**（§7.7 frustum 推導未涵蓋 \(r_1 = 0\)），已列為待裁決項。

---

VERDICT: ADOPT 116 / MODIFY 39 / REJECT 0

### A 組

A-01 ADOPT — 移除清單前的單破折號後，動詞片語完整且語意不變。  
A-02 ADOPT — 後段是鬆散同位語，逗號合適。  
A-03 ADOPT — 兩個子句是同一因果判讀，逗號加 `and` 合適。  
A-04 ADOPT — `not … but …` 是同位修正，逗號合適。  
A-05 MODIFY — 公式不是「Definition 6.1」本身，而是該定義中的公式；建議：First, when \(g\) is the zero function and \(f \ge 0\), the region is the one under the graph of \(f\), and the formula collapses to \(\int_{a}^{b} f(x)\,dx\), the area formula in Definition 6.1.  
A-06 ADOPT — 指令與其具體作法分句後更清楚，條件 scope 未變。  
A-07 MODIFY — `one piece doubled would have done` 不夠直白；建議：Symmetries like this are useful to notice before integrating. Here, we could compute one piece and double the result.  
A-08 ADOPT — `giving` 正確表達由交點方程得到座標。  
A-09 ADOPT — 尾段是對 \(\Delta t\) 的同位釋義。  
A-10 ADOPT — 尾段是對位置差的同位釋義。  
A-11 MODIFY — 改稿把總結誤轉成突兀祈使句；建議：The section uses one move throughout. After we subtract the boundary graphs, the machinery of Chapter 6 applies to the difference exactly as before: Riemann sums, the existence guarantee of Theorem 6.1, and evaluation by the Fundamental Theorem.  
A-12 ADOPT — `the way a loaf of bread …` 是比較附語，逗號可用。  
A-13 ADOPT — 括號內兩個完整句能清楚區分一般原則與例子。  
A-14 ADOPT — `called` 使術語首見的命名動作明確。  
A-15 MODIFY — `made it … in the open` 指涉和搭配都不夠平實；建議：Geometry gives us the volume of a cylinder. For a curved solid, the modelling step is to define volume as the limit of the volumes of its slab approximations, as was done for area in §6.1.  
A-16 ADOPT — 命名 Cavalieri’s principle 改為獨立句正確。  
A-17 ADOPT — `only a recipe for \(A(x)\)` 是鬆散同位補述。  
A-18 MODIFY — 新句的 `which` 對象不清，旋轉的是線段而不是抽象距離；建議：For rotation about the \(x\)-axis, the disk’s radius at \(x\) is the <em>function value</em> \(f(x)\). It is the vertical distance from the axis to the curve. Rotating that vertical segment around the axis produces the disk.  
A-19 ADOPT — 後段是獨立的歷史／驗證結論。  
A-20 ADOPT — `continuous on \([0,4]\)` 是對 \(\pi x\) 的簡短補述。  
A-21 ADOPT — 逗號加 `and` 保留原本的因果警語。  
A-22 ADOPT — 分句後保留每個半徑都以新軸量起的條件。  
A-23 ADOPT — 後段是回指 Caution 的同位評語。  
A-24 MODIFY — `the same way` 指涉過弱，且應保留連續性前提；建議：For any solid with a continuous cross-sectional area that we can describe, the cross-section method can set up the volume integral. For many classical solids, similar triangles give that description.  
A-25 ADOPT — `, so` 保留了端點驗證到全區間結論的推論鏈。  
A-26 ADOPT — 命名 one-third rule 與解釋 \(\tfrac13\) 是兩個可辨識動作。  
A-27 ADOPT — 後段是同一個定義的類比性補述，逗號足夠。  
A-28 MODIFY — `no pleasant answer` 不夠字面且掩蓋真正困難；建議：Solving \(y = 2x^{2} - x^{3}\) for \(x\) requires inverting a cubic. That inversion does not give a simple description of the region.  
A-29 MODIFY — `comes first, and in the open` 不自然且不夠直白；建議：As in §7.2, we state the modelling assumption explicitly. We take the solid’s volume to be the limit of the volumes of these shell stacks as the strips shrink. This is the same modelling assumption as in Definition 7.2, except that the slices are nested around the axis rather than stacked along it.  
A-30 ADOPT — `of constant height` 直接併入名詞片語，清楚且正確。  
A-31 ADOPT — 兩個子句共同說明同一 Riemann sum 判讀。  
A-32 MODIFY — `that` 會錯指為 \(y\)-axis 本身，而非距離；建議：A shell’s radius is the distance from the strip to the <em>axis of rotation</em>. For rotation about the \(y\)-axis, that distance is the horizontal coordinate \(x\), even though the strip itself stands vertically.  
A-33 MODIFY — `which is … returning in a new role` 不夠直接；建議：When the rotated region lies between <em>two</em> graphs, the shell’s height is the gap between them. This gap is the same quantity that served as the integrand in §7.1.  
A-34 ADOPT — 第二句的 washers／shells 對照仍是一個平行比較動作。  
A-35 MODIFY — `honestly gives` 與 `sideways description` 都偏修辭；建議：Since \(x^{2}\) is increasing on \([0,1]\), solving \(y = x^{2}\) for the boundary gives \(x = \sqrt{y}\), the description of the boundary as \(x\) in terms of \(y\).  
A-36 ADOPT — `as they must if …` 保持同一測量對象的必要結果。  
A-37 MODIFY — `There is` 後接三項並列內容會造成數的一致性問題；建議：The section follows the same pattern as before. It states the modelling commitment once (solids are measured by their shell stacks), computes each approximating piece exactly, and uses Chapter 6’s convergence machinery to take the limit.  
A-38 ADOPT — `first areas and then volumes` 明確補出章節順序。  
A-39 ADOPT — 分句後對 signed component 的說明更明確。  
A-40 ADOPT — 尾段是對 `against the spring` 的同位釋義。  
A-41 ADOPT — 第二句是獨立比較結論。  
A-42 ADOPT — `here gravity` 是短同位補述。  
A-43 ADOPT — 水平切片的指令與理由分開後清楚。  
A-44 ADOPT — 連續變量與有限平均的差異應分句。  
A-45 ADOPT — 連續性的條件仍完整地管轄收斂結論。  
A-46 ADOPT — 定義性比喻與操作性視覺化分開合理。  
A-47 ADOPT — `by the Net Change Theorem` 明確標示依據。  
A-48 ADOPT — 第二句補出平均值偏低的原因。  
A-49 ADOPT — 尾段只是回指前述 Caution。  
A-50 ADOPT — 直接接 `at \(x=\pm1\)` 比破折號自然。  
A-51 MODIFY — 這會違反 SEAM GUARD 的「ONE remark sentence」字面限制；建議：We only note a second route to the same theorem: apply the Mean Value Theorem for derivatives (Theorem 4.12) to the accumulation function \(\int_{a}^{x} f(t)\,dt\), whose derivative is \(f\) by the Fundamental Theorem (Theorem 6.3).  
A-52 ADOPT — 非唯一性與兩個解是不同教學動作，應分句。  
A-53 MODIFY — `payoff from owning proved versions` 對 EFL 讀者不透明；建議：The Mean Value Theorem for Integrals says that a continuous function must take its average value. It is the first result in this book that uses the proved Extreme and Intermediate Value Theorems.  
A-54 ADOPT — 強調性同位語改逗號後仍可讀。  
A-55 ADOPT — 曲線逼近的轉折改分句合適。  
A-56 ADOPT — 尾段是多邊形長度的簡短同位說明。  
A-57 ADOPT — 取樣點來源是對 Riemann sum 的補述。  
A-58 MODIFY — `the Mean Value Theorem’s choices included` 是不完整的附加語；建議：Theorem 6.1 guarantees that the Riemann sums of \(g\) converge to \(\int_{a}^{b} g(x)\,dx\) for <em>every</em> choice of sample points (Definition 6.2), including the points supplied by the Mean Value Theorem.  
A-59 ADOPT — 補上 `and` 後兩個 stretch-factor 性質平行。  
A-60 ADOPT — 尾段是合理的 sanity check 依據。  
A-61 ADOPT — `a result … published` 是可讀的同位補述。  
A-62 ADOPT — `which is why` 正確表達平方結構與結果的關係。  
A-63 ADOPT — `that is` 清楚引入 running quantity 的白話釋義。  
A-64 ADOPT — 不等式的幾何閱讀應與公式語句分開。  
A-65 MODIFY — 兩個連續同位語會形成逗號堆疊；建議：Squaring this equation gives the easily remembered relation <em>\(ds^{2} = dx^{2} + dy^{2}\)</em>. This mnemonic summarizes the right-triangle relation used for the chords in the proof.  
A-66 ADOPT — mnemonic 與真正證明是兩個獨立動作。  
A-67 ADOPT — 工具清單是鬆散同位語。  
A-68 ADOPT — `the rim of the base` 正確指認該弧。  
A-69 ADOPT — `which are` 清楚給出 frustums 的術語釋義。  
A-70 MODIFY — `But that case we can check directly` 不如平實主謂語序；建議：The subtraction divided by \(r_2-r_1\), so it says nothing about the case \(r_1=r_2\). We can check that case directly. Equal radii make the frustum a cylindrical band, which unrolls into a flat rectangle of length \(2\pi r\) and width \(\ell\), so its area is \(2\pi r\ell=\pi(r+r)\ell\).  
A-71 ADOPT — 逗號加 `and` 保留公式可算與論證閉合的連結。  
A-72 ADOPT — `which is the claimed formula` 是正常關係子句。  
A-73 MODIFY — `The integrand rewards a second look` 與結尾縮略語不夠平實；建議：It is useful to examine the integrand again. Here \(2\pi f(x)\) is the circumference of the circle traced by \((x,f(x))\), and \(\sqrt{1+f'^{2}}\,dx\) is the arc element \(ds\) of §7.6. Together, these are the band’s two length scales: one around the axis and one along the curve.  
A-74 ADOPT — 標語式短句後接完整推論，節奏正常。  
A-75 ADOPT — radius discipline 應獨立成明確結論。  
A-76 ADOPT — 平滑性與定理適用性分句後清楚。  
A-77 ADOPT — 對照補述用逗號自然。  
A-78 MODIFY — `trade areas band for band` 是隱喻性主張；建議：This width-only law is ancient. Archimedes knew that a sphere and its circumscribed cylinder have equal areas in corresponding bands. If the same pair of parallel planes cuts both solids, the two bands have equal area; this is why the result is remembered as his <em>hat-box theorem</em>.  
A-79 ADOPT — 尾段正確指認全球表面積。  
A-80 ADOPT — 旋轉半徑與區間條件仍維持同一句推論鏈。  
A-81 ADOPT — 尾段是對三個來源的簡短總結。  
A-82 MODIFY — 新稿的非限定片語並列不夠平行；建議：Section 7.2 promoted the strip to a solid slab and defined volume as the integral of cross-sectional area (Definition 7.2), \(V=\int_a^b A(x)\,dx\). Disks and washers are its applications to solids of revolution, and the method recovers the classical volumes of the sphere and pyramid.  
A-83 MODIFY — `after Example 7.22` 會把原本「在例中提出」誤讀成時間先後；建議：Chapter 8 pays that debt with a systematic account of integration techniques and with improper integrals, which will also address the issue at the poles noted in Example 7.22.  
A-84 MODIFY — `without further comment` 不等於 `without ceremony`；建議：The slicing schema is now complete. It is the method by which integrals are used in applications, and the rest of the book will use it routinely.  

### B 組

B-01 MODIFY — product 的定義應先進入操作句，不宜在命令後補定義；建議：Approximate each piece by multiplying a value that is nearly constant across the slice by the slice’s width. Then sum those products and refine.  
B-02 MODIFY — 原 KEEP 的插入語其實定義本章最核心的 modelling transition；建議：The skill this chapter teaches is the modelling step of representing a quantity by an integral, a skill used throughout the rest of calculus, from differential equations to the geometry of space.  
B-03 ADOPT — `as they are in every example …` 只修飾適用頻率，KEEP 正確。  
B-04 ADOPT — 左右邊界、連續性與 \(f(y)\ge g(y)\) 都在同一假設 scope 內。  
B-05 ADOPT — 先立 \(s_A(0)=s_B(0)\) 再給速度條件，記號與量詞清楚。  
B-06 MODIFY — `running side by side` 與 `stays on top` 應改成字面條件；建議：The same interpretation applies to any two rates, such as flow rates or growth rates, as long as one rate remains at least as large as the other. If the rate curves cross, the area between the graphs accumulates the absolute gap \(\int \lvert v_A-v_B\rvert\), whereas the net difference is the ordinary integral. This is the displacement-versus-distance distinction of §6.4.  
B-07 ADOPT — \(A(x)=A\) 與 \(h=b-a\) 在使用 \(Ah\) 前已立明。  
B-08 ADOPT — disk 的命名已從插入語移為明確術語句。  
B-09 ADOPT — annulus、washer 與面積公式的順序清楚。  
B-10 ADOPT — 錯誤的算式、錯誤性質與後果已分成可辨識動作。  
B-11 ADOPT — 題幹中的區域界定只限制同一個例題對象，KEEP 正確。  
B-12 ADOPT — disk、washer、square 只是同一指令的例示，KEEP 正確。  
B-13 MODIFY — `natural cut` 與 `falls out effortlessly` 不夠平實；建議：Perpendicular slices are not always the simplest choice. For some solids of revolution, every washer requires solving for \(x\) in terms of \(y\), whereas decomposing the solid into thin cylindrical <em>shells</em> gives the needed dimensions directly.  
B-14 ADOPT — `the one that reads \(f\) directly` 只是指定同一條 strip，KEEP 正確。  
B-15 MODIFY — `volume we can compute` 與 `makes it collapse` 都不夠直接；建議：For the annular cylinder, we can compute the volume exactly by subtracting the inner cylinder from the outer cylinder. The midpoint then simplifies that exact volume as follows.  
B-16 MODIFY — `takes it somewhere new` 是不透明的方向隱喻；建議：The next section applies the schema to a quantity from physics that accumulates along a motion rather than across a region. For the first time, the slicing must decide <em>what</em> to slice.  
B-17 ADOPT — 記號、物理設定與 Riemann-sum 操作已依序建立。  
B-18 ADOPT — Hooke’s law 的模型地位與適用範圍已獨立表明。  
B-19 ADOPT — 直接給定 weight density 的理由已成獨立教學動作。  
B-20 ADOPT — 引號內兩個模板屬明示允許保留的節拍式插入語。  
B-21 ADOPT — 機件不變與 slicing 新決策是可分的兩個動作。  
B-22 ADOPT — 三種 total 僅例示同一個平均值操作，KEEP 正確。  
B-23 ADOPT — 移除 `pair` 後與後文 `together with the interval` 一致。  
B-24 ADOPT — 平均值介於極值間的關鍵推理已升為主幹。  
B-25 MODIFY — `hence in \([a,b]\)` 是完成定理所需的域別結論，不只是節拍註記；建議：Since \(f\) is continuous on \([\alpha,\beta]\) and \(f_{\text{ave}}\) lies between its endpoint values, the Intermediate Value Theorem (Theorem 4.9(b)) supplies a point \(c\) in \([\alpha,\beta]\) with \(f(c)=f_{\text{ave}}\). Because \([\alpha,\beta]\subseteq[a,b]\), this point also lies in \([a,b]\).  
B-26 ADOPT — 先給 smooth 的定義、後給 \(C^1\) 記號，數學等價。  
B-27 MODIFY — `First the hypothesis.` 不是完整句；建議：First, check the hypothesis. Here \(f(x)=x^{3/2}\), so \(f'(x)=\tfrac{3}{2}x^{1/2}\), which is continuous on all of \([0,1]\). At the left endpoint, the one-sided derivative is \(0\), and \(f'\) approaches it continuously. Thus \(f\) is smooth there, so Theorem 7.3 applies.  
B-28 ADOPT — sign check 已被提升為明確的條件—結論句。  
B-29 ADOPT — 長度存在、計算值與公式不適用的例外已清楚分開。  
B-30 MODIFY — `the skin, with none of the filling` 是 surface 首見時的術語釋義，不能留在成對 dash 中；建議：Rotating just the curve produces a surface rather than a solid with an interior. The natural question is its area.  
B-31 ADOPT — `all the way around the axis` 只修飾同一個方向尺度，KEEP 正確。  
B-32 ADOPT — 四個 schema 步驟已脫離插入語，適合作章末參考。  
B-33 ADOPT — \(F(x)\) 的意義已在公式後用 `where` 明確給出。  
B-34 MODIFY — `leaning on` 與 `payoff from owning` 仍過於隱喻；建議：Three theorems in the chapter were proved using the machinery of Chapter 4. The Mean Value Theorem for Integrals uses the Extreme and Intermediate Value Theorems, and the two geometric formulas use the Mean Value Theorem. This is the first extended use in the book of those earlier proofs.  

### C 組

C-02 MODIFY — `they` 的先行詞不夠明確；建議：Try to compute a volume with the last section’s tools, and you will sometimes find that those methods do not fit the region.  
C-02b MODIFY — `hard to slice perpendicularly` 應指明是描述方法困難；建議：The region under \(y = 2x^{2} - x^{3}\) is awkward to describe using slices perpendicular to the axis of rotation.  
C-03 MODIFY — `shapes` 仍帶比喻性；建議：Deciding what to slice determines the rest of the solution, and it is the first sentence of each solution below.  
C-06 MODIFY — `straight shortcut` 仍不如 chord 的字面幾何關係；建議：The polygon replaces each curved arc by a straight chord, so it under-measures every arc it spans.  
C-07 ADOPT — `what the next theorem needs` 是直接且準確的替換。  
C-08 MODIFY — `does its work` 仍是含混擬人；建議：The second half of the hypothesis is needed at this step.  
C-09 ADOPT — `extract` 比 `distil` 常見且字面。  
C-11a ADOPT — `deserves some confidence` 已移除交易式擬人。  
C-11b ADOPT — `justified that confidence` 保留驗證關係且不再用償債隱喻。  
C-12 ADOPT — `this cannot happen` 明確回指有限列表的失敗情形。  

### D 組

D-01 ADOPT — 已完成規定的人工作用判定，且章開場單段形式有一致性理由。  
D-02 ADOPT — 動機／教訓與 shell 方法的展開是兩個獨立段落動作。  
D-03 ADOPT — 重力模型與「切材料」的推論應分段。  
D-04 ADOPT — 幾何三節與離開幾何後的總結是自然段界。  
D-05 ADOPT — 定理依賴與後續章節欠缺的工具是兩個論證單位。  

### E 組

E-01 ADOPT — 對照補述改逗號後仍清楚。  
E-02 ADOPT — 操作指令的否定條件以逗號接續合適。  
E-03 ADOPT — slab 外觀是 cylinder 的同位補述。  
E-04 ADOPT — `visibly not` 是短對照補述。  
E-05 ADOPT — 相似三角形關係已成主幹句。  
E-06 ADOPT — 尾段正確指認 shell method 保留的 strip。  
E-07 ADOPT — nested tubes 與 stacked slices 是獨立圖像判讀。  
E-08 MODIFY — 連續名詞片語以逗號串接不成句；建議：Figure 7.12 shows one solid sliced in two ways: the solid of Example 7.12 is a cylinder with a paraboloid bowl carved from its top.  
E-09 ADOPT — `and do` 只強調同一主張，KEEP 正確。  
E-10 ADOPT — `provided` 使單側條件字面可見。  
E-11 ADOPT — 高度遞增是同一 caption 的並列觀察。  
E-12 ADOPT — water surface 與 rim 的兩個角色應分句。  
E-13 ADOPT — newton-metres 與 joules 的同義關係已明說。  
E-14 ADOPT — 切片所在地與終點的對照是鬆散補述。  
E-15 ADOPT — 面積相等與 deficit/surplus 解釋應分句。  
E-16 ADOPT — Theorem 4.12 的圖像是同位指認。  
E-17 ADOPT — 改為兩句後不再有 X—Y—Z 的結構歧義。  
E-18 MODIFY — `what … whether` 的搭配不自然；建議：Look for a structure that makes the root tractable, such as a substitution (as in Example 7.19) or a perfect square (Example 7.20); most other integrands require the techniques of Chapter 8.  
E-19 ADOPT — annular sector 與邊長差異是兩個動作。  
E-20 ADOPT — chord／arc 的對照與 endpoint radii 已分開。  
E-21 ADOPT — 兩片 slab 的位置是正常並列補述。  
E-22 ADOPT — `one principle and not a memorized pair` 是可讀的總結同位語。  

### Q1

34 對成對插入語中，沒有一對「本應 KEEP 卻被重寫」。但有三對原判 KEEP 應改為重寫：B-02、B-25、B-30。逐項四步仲裁如下；表中「重寫」表示應維持／改成無 dash 的實質重寫。

| ID | 結論 | step 2／3 的決定性理由 |
|---|---|---|
| B-01 | 重寫 | product 的內容是獨立定義。 |
| B-02 | 重寫 | `from a quantity to its integral` 是本章核心 transition 的定義。 |
| B-03 | KEEP | 只是頻率／範圍修飾。 |
| B-04 | 重寫 | 邊界、連續性、序關係是完整假設組。 |
| B-05 | 重寫 | 建立記號與條件，且後文立刻使用。 |
| B-06 | 重寫 | 例示、適用條件與 crossing 後果各有教學功能。 |
| B-07 | 重寫 | \(A(x)=A\) 與 \(h=b-a\) 是結論所需記號。 |
| B-08 | 重寫 | disk 的術語首見釋義。 |
| B-09 | 重寫 | washer 的術語首見釋義。 |
| B-10 | 重寫 | 錯誤來源與其後果是獨立診斷。 |
| B-11 | KEEP | 只限定該例題的既定區域。 |
| B-12 | KEEP | 三種截面只是同一指令的例示。 |
| B-13 | 重寫 | shells 的分解方式是新方法的實質引入。 |
| B-14 | KEEP | 只指定「直接讀 \(f\)」的那條 strip。 |
| B-15 | 重寫 | outer-minus-inner 是計算理由。 |
| B-16 | 重寫 | 新物理量與首次決定切什麼是兩個動作。 |
| B-17 | 重寫 | 符號與物理設定須先立。 |
| B-18 | 重寫 | 模型地位與小形變適用範圍不可埋入。 |
| B-19 | 重寫 | weight density 的理由是獨立論證。 |
| B-20 | KEEP | 引號內模板為規則明示允許的節拍式插入。 |
| B-21 | 重寫 | machinery 不變與新策略結論分屬不同動作。 |
| B-22 | KEEP | 只列舉同一種 total 的例子。 |
| B-23 | 重寫 | `pair` 的定義性釋義應直接表述。 |
| B-24 | 重寫 | 平均值位於極值間是關鍵推理步。 |
| B-25 | 重寫 | `hence in \([a,b]\)` 是必要的域別結論。 |
| B-26 | 重寫 | 正式定義與 \(C^1\) 記號應分開。 |
| B-27 | 重寫 | endpoint continuity 是獨立檢查。 |
| B-28 | 重寫 | 絕對值的 sign check 必須顯式。 |
| B-29 | 重寫 | 長度存在、計算與公式例外皆獨立。 |
| B-30 | 重寫 | `skin, with none of the filling` 是 surface 的術語釋義。 |
| B-31 | KEEP | 只是同一尺度的方向／延伸修飾。 |
| B-32 | 重寫 | 四步 schema 是章末可獨立使用的指令。 |
| B-33 | 重寫 | \(F(x)\) 的定義與切片選項都是獨立內容。 |
| B-34 | 重寫 | 定理依賴對應與其總結各自成立。 |

沒有重寫項只是把成對 dash 表面換成逗號：B-13 是把插入語改為名詞的直接補語；其餘皆已拆句、提升條件／定義、或重組主幹。E-09 的 KEEP 也正確，因為 `and do` 只確認同一個測量主張。

### Q2

84 個單尾的 CUT 原則正確，且我沒有發現採納項改動數學片段、量詞 scope 或條件—結論關係。需要修正的替代形式就是上列 22 項 MODIFY，主要問題是：

- 語意或指涉：A-05、A-18、A-24、A-32、A-83、A-84。
- 不夠平實的剩餘修辭：A-07、A-28、A-29、A-35、A-53、A-73、A-78。
- 句法／標點負載：A-11、A-37、A-58、A-65、A-70、A-82。
- SEAM GUARD：A-51。

其餘逗號化的項目是短同位語、關係子句或單一因果鏈，沒有為了縮短而拆散 scope，也不會造成連續三句同長的機械節奏。

### Q3

三筆都保持數學正確與等價。

- B-04：新稿仍假設 \(f,g\) 在 \([c,d]\) 連續，且 \(f(y)\ge g(y)\) 對該區間內的 \(y\) 成立；「水平切」仍只在這整組條件下推出。量詞與條件 scope 沒有擴張或縮小。
- B-26：先定義 smooth，再說此條件記作 \(f\in C^1([a,b])\)，只是記號建立順序調整，沒有改變端點 one-sided derivative 的要求。
- B-33：把 \(F(x)\) 的 signed-component 說明由插入語移到 `where` 子句，公式 \(W=\int_a^b F(x)\,dx\) 及其物理意義完全不變。

### Q4

七項刻意保留中，需更正的是第 1 項與第 3 項：B-02、B-25、B-30 不應 KEEP；其中 B-25 位於 Theorem 7.2 證明內，但應只做上列很小的域別結論改寫，不需要重拆整段證明。

其餘判斷正確：

- `pays that debt` 應保留，因為它是已 gloss、全書貫穿且已有先例的機制隱喻。
- Notice that／Observe that／In other words 不應當作 findings。
- radius discipline 是必要的 topic-term recurrence。
- 符號密集段的處置沒有機械按詞切句。
- 197 詞 lead 已完成人工判定；以全書統一的 `<p class="lead">` 結構為理由不拆，成立。

我沒有判任何一筆為純粹 over-report 的 REJECT。C-11a／C-11b 與 C-12 都只是 advisory，不是 blocking，但在 canon 章與 EFL 基線下仍是比例適當的平實化。

### Q5

算違反字面上的 SEAM GUARD。

A-51 沒有另跑完整證明，所以沒有違反該約束的主要目的；但它把原定的「ONE remark sentence」拆成兩句，仍違反明示的形式限制。應採用上列單一句的 MODIFY 版本。

### Q6

理由大致站得住，但不能把「冒號、分號下降」當成成對逗號上升的抵銷理由；不換 tic 護欄要求每種標點負載各自可辯護。

真正站得住的理由是：新增逗號確實主要落在鬆散同位語，屬 CUT palette 的指定落點，且沒有把成對 dash 假裝改成逗號。建議把每一筆新增成對逗號列入交付 ledger，逐筆標成「短同位語／必要關係子句／平行補述」。

我會改用分句以避免逗號堆疊的主表項目是 A-33、A-65、A-82；E-08 也應改成完整 caption 句。套用這些 MODIFY 後，`32 → 43` 不應再視為最終值，必須重新跑 canonical metrics。

### Q7

符合規定，但前提是例外要明示保留在報告中，且不是以「全章達標」默默豁免小節。

§7.2 的 B-11／B-12 與 §7.4 的 B-20／B-22 都通過四步仲裁，沒有安全的機械改點；因此把 3.13 與 3.20 記為明示節級例外，並維持全章 2.25/1000 的綁定閘，符合「另找安全改點、重寫多動作句，或明示節級例外」中的第三條路徑。應在最終報告寫明：例外來自已審核的 KEEP，而非由密度目標反推 KEEP。

### 範圍外發現

§7.7 的 frustum 推導只寫 \(r_1<r_2\)，但隨即使用 \(\ell_1/r_1=\ell_2/r_2\)。若 \(r_1=0\)，這個比值無定義，該帶其實退化為 cone。建議在推導前寫 \(0<r_1<r_2\)，並另說公式在 \(r_1=0\) 的 cone 情形仍成立。
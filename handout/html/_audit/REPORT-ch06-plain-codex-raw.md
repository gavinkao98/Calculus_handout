# Codex gate-2 raw：ch06 散文平實化回填（合併 sweep）逐條裁決

- **調用**：`codex exec -s read-only -o <file> -`（stdin 餵 UTF-8 prompt；材料**全 inline**、未讓 Codex 讀檔——遵循 2026-06-28 編碼坑紀律），codex-cli 0.144.1，模型走 `~/.codex/config.toml` 預設 **gpt-5.6-terra**（`model_reasoning_effort = "max"`）。
- **日期**：2026-07-26。**授權**：使用者本輪明示「P-3 跑 Codex gate-2」（`CLAUDE.md` 2026-07-01 Codex 唯讀逐次徵詢條款）。耗時約 16 分鐘（背景執行）。
- **受審材料**（prompt 91.5 KB）：gate-1 走查的 59 張卡片（前→後全句）＋ `CONTENT_SPEC.md` §3〈平實英文條款〉RC 條款節錄 ＋ `PROSE-AUDIT-RUBRIC.md` 四維度與擋稿線 ＋ ch06 變體背景（canon 章、無手稿；§6.2／§6.3 已結案的兩層範圍切法）＋ Gate 0 量測前值與段落層三個觸發器的判定 ＋ 刻意保留清單（4 處 DASH-KEEP＋非 finding 清單＋段落放行）＋ §6.1／§6.4／§6.5 **完整散文** ＋ §6.2／§6.3 含 dash 的段落全文 ＋ Q1–Q7。
- **走查稿**：[`REVIEW-ch06-plain-walk.html`](REVIEW-ch06-plain-walk.html)。
- 本檔為 **raw 輸出照登**（未刪改一字）。逐條折入時的處置（含我未完全照抄 Codex 措辭的理由）記在 applied 報告與該輪 commit body。

**摘要**：`VERDICT: ADOPT 38 / MODIFY 21 / REJECT 0`。**零 REJECT**——59 張卡片的方向全部獲認可，四處 `DASH-KEEP` 的四步判定與 §6.5 明示節級例外都被確認站得住（Q4）。21 條 MODIFY 中，Codex 抓到**兩個真實的數學／表述不精確**：A-5 的 `filling them with polygons` 會誤稱曲邊區域可被填滿（與同節「no way to tile a curved region exactly」自相矛盾），D-10 的 `the table no longer applies` 過度絕對（arctan 那一列本身就是「內函數套內函數卻仍在表上」的反例）。另外糾正了我的 tic 估計：冒號接子句實際只 +1（不是 +2）。

---

VERDICT: ADOPT 38 / MODIFY 21 / REJECT 0

A-1 ADOPT — 逗號同位語完整保留導數的字面定義，沒有額外論述動作。
A-2 ADOPT — 建構極限與揭示互逆關係是兩個獨立教學動作，拆開合理。
A-3 ADOPT — 評價性「summit」與硬幣隱喻都不再承載必要內容。
A-4 MODIFY — `where we build it` 仍是模糊建構隱喻；改為：That link between areas and slopes connects the two halves of calculus, and this chapter explains it.
A-5 MODIFY — `filling them with polygons` 會誤稱可把曲邊區域填滿；改為：The Greeks computed areas of curved regions by approximating them ever more closely with polygons.
A-6 ADOPT — `say` 引出的例子用逗號即可，問句的範圍未變。
A-7 ADOPT — 前兩句已明說近似再取極限，`same method` 的指涉足夠清楚。
A-8 ADOPT — 後段只是對 rectangle sum 的同位說明，逗號合適。
A-9 ADOPT — 三句分別處理遞增、遞減、非單調三種情況，並非機械拆句。
A-10 MODIFY — 四個矩形本身不構成 bracket，應明說左右和；改為：With four rectangles, the left and right sums bracket the area only loosely. The bracket will narrow as \(n\) grows, and the next example takes \(n\) all the way to infinity.
A-11 ADOPT — `comfortably inside` 是鬆散同位補述，逗號不損數學內容。
A-12 ADOPT — 原段同時含定理內容、用途、證明去處與不連續反例，三段分組合理。
A-13 MODIFY — `It` 缺少清楚先行詞，且把一個條件—結論定理拆得過碎；改為：The theorem here says that continuity of \(f\) guarantees that the approximating sums converge to one limit, regardless of the sample points chosen.
A-14 ADOPT — 主張、造成分歧的機制、結論各自獨立，三句節奏也有變化。
A-15 MODIFY — `well posed` 與 `is carried` 仍不夠平實；改為：We rely on this guarantee here so that the definition gives one unambiguous value, and the next section states the theorem precisely (continuity guarantees the limit). Its proof, which uses the fact that a continuous function changes by only a small amount on sufficiently short subintervals, is given in the Proof-Track appendix.
A-16 MODIFY — `control` 仍未說明 continuity 實際保證什麼；改為：Continuity ensures that any choice of sample points gives the same limit. The choice between left and right endpoints is not the issue.
A-17 MODIFY — `squeezing them together` 的指涉與方法都不夠清楚；改為：In the third century BCE, Archimedes found the area of a parabolic segment by bounding it between inscribed and circumscribed straight-sided figures and making the two bounds approach each other. This is the same bracketing method that Examples 6.1 and 6.2 refine into a limit.
A-18 ADOPT — `straight-sided` 比未定義的 `rectilinear` 可預測。
A-19 ADOPT — 非負的理由與連續性假設是兩個教學動作，拆開清楚。
A-20 ADOPT — 常速近似的條件與估算結果仍是同一個局部近似動作。
A-21 ADOPT — `a Riemann sum again` 是純同位說明。
A-22 ADOPT — 與 Example 6.2 的連結有獨立教學價值，分句自然。
A-23 ADOPT — 分句移除 `nothing but` 的否定歧義，非負條件仍在場。
A-24 MODIFY — 原提案仍混淆名稱與符號，且 `keeps the promise` 不平實；改為：The next section names this common limit the *definite integral* and introduces its symbol. It also states the theorem that guarantees the limit for every continuous function.

B-1 MODIFY — `both` 沒有重新說明名稱與符號，`free it` 也不夠字面；改為：Here we name the common limit the *definite integral* and introduce its symbol. We also remove the assumption that \(f\) is non-negative.
B-2 ADOPT — 括號避免與前方並列清單混淆，且保留既有凍結措辭。
B-3 ADOPT — 刪除無資訊的 `natural` 後，因果理由直接而完整。
B-4 ADOPT — 逗號後的補語仍完整限定「所有分割與所有 sample point」的同一極限。
B-5 ADOPT — 先介紹 uniform continuity，再說其證明用途；這不是過拆。
B-6 ADOPT — 非負條件與 signed area 的結論沒有被拆散。
B-7 ADOPT — 用途總結與一般實務說明是兩個動作，分句合適。
B-8 ADOPT — `either ... or ...` 清楚標出兩種來源；既有詞彙不必在本輪重開。

C-1 ADOPT — 面積增量估計與導數結論分開後，推理更可追蹤。
C-2 ADOPT — `so` 把 dummy variable 的改名與函數不變的關係說明白。
C-3 ADOPT — `0 will do` 只是同一指令中的具體取值，成對 dash 應保留。
C-4 ADOPT — `the accumulation function` 是純命名同位語。
C-5 MODIFY — 提案把「any antiderivative serves」與 `since it cancels` 重複地作兩次理由；改為：Any added constant is pointless here because it cancels in the subtraction. We therefore take the simplest antiderivative available.
C-6 MODIFY — `They` 指涉不穩，首句與次句也重複互逆結論；改為：Differentiation and integration are inverse processes. The derivative of an accumulated area is the height, and an area can therefore be recovered from an antiderivative. Recognizing this connection turned a collection of clever area computations into a method.
C-7 ADOPT — 收束句中的 `the central fact of the subject` 是合法的句末同位補述。

D-1 MODIFY — `antiderivatives now need` 與 `rereads` 仍偏擬人／文學化；改為：The Fundamental Theorem reduces the evaluation of a definite integral to finding an antiderivative, so we now need notation and a working table for antiderivatives. This section provides both and restates the theorem as a statement about accumulated change, the form most useful in practice.
D-2 ADOPT — 逗號仍明確說明 \(C\) 就是 constant of integration。
D-3 ADOPT — 冒號後提供 Fundamental Theorem 如何連結兩者的 payload，正當且不改 scope。
D-4 ADOPT — 一句總述、一句例示，條理清楚。
D-5 ADOPT — 插入語只是第三個表項的必要條件，成對 dash 保留正確。
D-6 ADOPT — 缺例與接下來要解釋的 absolute value 是兩個合理動作。
D-7 MODIFY — 第二句的 `\(\pi\) arrives` 仍是擬人化表述；改為：Here a rational integrand with no area to read off has an integral whose value is \(\tfrac{\pi}{4}\). This is a standard example of an integral whose value involves \(\pi\).
D-8 ADOPT — displacement 先被定義，再由 Net Change Theorem 給出公式，位置正確。
D-9 MODIFY — 讓 total distance 當作主語去 `integrate`，且 `recovering the reading` 都不夠字面；改為：The *total distance travelled*, which never subtracts, is found by integrating the *speed* \(\lvert v(t)\rvert\), as in §6.1:
D-10 MODIFY — 提案的三個短句節奏過齊，且 `the table no longer applies` 過度絕對；改為：The table above applies directly only to functions that are visibly derivatives read backwards, but an inner function nested inside another may require a different method. The next section reverses the chain rule to introduce substitution for such integrals.

E-1 MODIFY — `the derivative is hidden` 與 `undoes the composition` 沒有充分說出 substitution 的操作關係；改為：The table of §6.4 antidifferentiates a function directly only when the function is visibly a derivative written plainly. Many integrands contain an inner function inside another function, the pattern to which the chain rule applies. To integrate \(\int 2x\sqrt{1 + x^{2}}\,dx\), there is no direct table entry, yet \(2x\) is exactly the derivative of the inner expression \(1 + x^{2}\), and that is no accident. Applying the chain rule in reverse gives the substitution method.
E-2 ADOPT — `honest` 改為 `correct` 正確；`usually cleaner` 只是第二選項的偏好修飾，成對 dash 應保留。
E-3 MODIFY — `one the table covers` 仍是較不直接的搭配；改為：The expression inside the square root is \(1 + x^{2}\), and its derivative \(2x\) is already present in the integrand. Put \(u = 1 + x^{2}\), so \(du = 2x\,dx\). The resulting integral is listed in the table:
E-4 ADOPT — `mark` 與 `reduces` 都比原本的隱喻詞字面。
E-5 ADOPT — 禁令獨立成句，醒目且不改操作順序。
E-6 ADOPT — `if it has any` 是同一主張的條件修飾；後一句純評價可刪。
E-7 MODIFY — `partner on the right of the same height` 句法鬆散；改為：For an even function, the graph on \([-a, 0]\) is the graph on \([0, a]\) reflected across the vertical axis. Each thin strip on the left therefore has a matching strip on the right with the same height and the same sign, so the matched signed areas *add*: the integral is twice the integral over \([0, a]\).
E-8 MODIFY — `and` 只並列兩件事，未標出後者是前者的實務後果；改為：The odd term contributes nothing at all, so recognizing this saves the work of integrating it.
E-9 MODIFY — `reaches`／`hides` 較不字面，也漏掉 constant-factor 條件；改為：Substitution applies to integrands with a single inner function whose derivative is present, up to a constant factor. This is a wide class, but it does not include all integrands.
E-10 MODIFY — 拆段正確，但原提案仍把 notation 與 indefinite integral 混為一談；改為：Section 6.4 introduced the notation \(\int f(x)\,dx\) for the *indefinite integral* (Definition 6.4) and a working table, singled out \(\int \tfrac{1}{x}\,dx = \ln\lvert x\rvert + C\), and reread the theorem as the Net Change Theorem (Theorem 6.5). The rest of the book uses the integral as a central tool.

Q1. 有兩處拆得稍過頭：A-13 應維持為一個「continuity 條件保證共同極限」的定理句；D-10 的三句長度過齊，前兩個限制性動作可合併。A-9、A-14、B-5、C-6、E-7 都沒有機械拆碎：它們分別拆開不同情形、機制與結論、術語與用途、數學事實與歷史結果、幾何與符號面積結論。

Q2. B-4 的量詞 scope 安全；逗號後仍修飾同一個 `single limit`。D-2 仍明確把 `the constant of integration` 指向 \(C\)。D-8 的 `it` 清楚指 displacement，前句的速度／位置條件仍在其說明範圍內。A-13 需採我的單句版本以避免 `It` 無先行詞；E-7 的原提案數學因果正確，但我的版本更清楚地保留「鏡射 → 同高同號 → 相加」。真正的微小數學問題是 A-5 的 `filling` 與 D-10 的絕對化 `no longer applies`，已在 MODIFY 修正。

Q3. 站得住，但不是因為 dash 本身不合法。兩處的 `— the definite integral —` 單獨看都是 KEEP 候選；真正使重寫合理的是主句同時做了命名／引入符號與另一個獨立教學動作。A-24 的另一動作是說明連續函數的存在保證；B-1 的另一動作是拿掉非負假設。因此應拆，但要用我給的版本明說名稱、符號與定理，不能只把 dash 換成逗號。

Q4. 四處 KEEP 都通過四步判定：C-3 是具體取值，D-5 是清單項目的域條件，E-2 是偏好程度，E-6 是條件限制。§6.5 的 \(4/1028 \approx 3.9/1000\) 因而可採明示例外；全章仍約 \(8/5770 \approx 1.4/1000\)，而且沒有值得為湊額度而破壞的 canonical KEEP。補充：Strategy 6.2 兩個條列中的單 dash 可另做副表清理，但條列不進 canonical 分母，不能當作解除 3.9 例外的理由。

Q5. A-13 的 `It makes two claims: ...` 是引清單型，確實不計入「冒號接子句」。依 inline 卡片重算：冒號接子句應為 \(41 \to 42\)（只 D-3 淨增一處；A-9 是一處搬到另一處），不是 \(43\)。以 5,770 詞比較，約 \(+0.17/1000\)。分號為 \(37 \to 35\)，左括號為 \(52 \to 53\)，成對逗號淨變化為 0。B-4、E-1、E-7 的既有解釋型冒號不變；D-9 的公式引介冒號不計。

Q6. 此範圍切法成立：已通過的 §6.2／§6.3 詞彙閘不因未改字串而自動失效，所以 `come the hard way`、`obeying the … rules` 不應重開。不過 B-5、C-5、C-6 已不只是純標點，應列為「dash 驅動的局部重寫」，對改句跑局部語意等價、術語先後、量詞／因果與數學檢查；不需要重跑整節的 R 詞彙掃描。

Q7. 另有少量 advisory R finding：§6.1 的 `the total accumulated from a rate` 可改為 `the total amount accumulated from a rate`，`close on a single value` 可改為 `converge to the same value`；§6.4 的 `The term \(5/x\) draws on the logarithm` 與 `Its value is in the reading` 都較不透明；§6.5 的 `need their own device`／`the business of Chapter 8` 宜改為 `require different techniques`／`Chapter 8 begins with those techniques`。未見額外 R3 漂移。套用上述 MODIFY 後，未見 U 維度 blocking：關鍵術語均已有定義、相鄰 gloss 或前章依據。

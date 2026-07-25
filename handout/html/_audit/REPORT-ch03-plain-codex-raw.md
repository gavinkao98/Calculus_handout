# Codex gate-2 raw：ch03 散文平實化回填（合併 sweep）逐條裁決

- **調用**：`codex exec -s read-only --output-last-message`（stdin 餵 UTF-8 prompt；材料**全 inline**、未讓 Codex 讀檔——遵循 2026-06-28 編碼坑紀律），codex-cli 0.144.1，模型走 `~/.codex/config.toml` 預設。
- **日期**：2026-07-25。**授權**：使用者本輪明示「跑 Codex Gate 2」（`CLAUDE.md` 2026-07-01 Codex 唯讀逐次徵詢條款）。
- **受審材料**（prompt 123.3 KB）：gate-1 走查的 50 條改點（前→後全句＋理由）＋ 3 對逐例 KEEP ＋ `CONTENT_SPEC.md` §3〈平實英文條款〉RC 全文節錄（MUST／SHOULD／FLAG＋四步仲裁＋暖句四條件）＋ `PROSE-AUDIT-RUBRIC.md` R 維度與擋稿線 ＋ **Gate 0 的 provenance 事實**（ch03 對手稿 6-gram 重疊 0.7%、54 個 dash 零命中手稿）＋ 量測前後值 ＋ 段落層觸發器 ＋「刻意未改」清單 ＋ 三節完整原文 ＋ Q1–Q7。
- **走查稿**：[`REVIEW-ch03-plain-walk.html`](REVIEW-ch03-plain-walk.html)；**整合裁決與執行結果**：[`REVIEW-ch03-plain-applied.html`](REVIEW-ch03-plain-applied.html)。
- 本檔為 **raw 輸出照登**（未刪改一字）。折入時的逐條處置（含 12 條 MODIFY 我如何取捨、Q6 第二波 16 採 7 退的理由）記在 applied 報告與本輪 commit body。

**摘要**：`VERDICT: ADOPT 38 / MODIFY 12 / REJECT 0`。

Codex 在 **Q7（數學安全）** 抓到三處實質問題，其中 **W-09 是既有課文本身的錯誤**（原句說「continuity 是兩個因子都需要的」，實際上 continuity 管第一個因子、fundamental limit 管第二個），與 ch01 那輪抓到的 `arccos` 端點同一等級。**Q6** 另提 16 項本輪漏掉的詞彙層 finding，triage 後採 9 退 7（退的多為「示範規則不誤傷」：`squeezed to a limit` 是 squeeze theorem 的術語、`Two debts remain` 是全書 credit／debt 機制用語）。

---

VERDICT: ADOPT 38 / MODIFY 12 / REJECT 0

W-01 ADOPT — 定義已字面化；章首的並列回顧仍是一個導覽動作。  
W-02 MODIFY — `settle it with a piece of geometry` 仍不夠字面。改稿：“First we establish the limit needed to differentiate the trigonometric functions. Algebra alone cannot evaluate this limit, so we use a geometric comparison.”  
W-03 ADOPT — 將擬人化的 `yielded to algebra` 改為直接的計算敘述。  
W-04 MODIFY — 改稿仍保留 `break into pieces` 的隱喻，且應直接說明缺少可約的 \(h\) 因子。改稿：“No algebraic identity cancels the \(h\) in the denominator against the numerator. Expanding \(\sin(x + h) - \sin x\) does not produce a factor of \(h\) that can be canceled.”  
W-05 MODIFY — 應補回導數推導還需要 continuity，避免把單一極限說成唯一充分條件。改稿：“With this limit and continuity established, we can find the derivatives of <em>both</em> \(\sin\) and \(\cos\), and then those of the other trigonometric functions.”  
W-06 ADOPT — 來源、代換、展開是三個獨立教學動作；量詞與等式鏈均完整保留。  
W-07 MODIFY — 原改稿有小寫開頭，且仍把命名與後續限制黏在一起。改稿：“Because both \(\theta\) and \(\sin\theta\) reverse sign when \(\theta\) is replaced by \(-\theta\), the ratio \(\sin\theta/\theta\) is unchanged. A function with this property is called an <em>even</em> function. It is therefore enough to consider \(\theta > 0\) as \(\theta\) approaches \(0\).”  
W-08 ADOPT — 逗號後為單純同位語，`use repeatedly below` 直接且可預測。  
W-09 MODIFY — continuity 直接處理第一因子；第二因子靠 fundamental limit，原改稿仍混淆兩者。改稿：“We need continuity for the first factor of the difference quotient and for the proof of the fundamental limit, so we establish it now.”  
W-10 ADOPT — 將 sector-area formula 與極限依賴 radians 分成兩個可獨立檢查的命題。  
W-11 ADOPT — 移除 `all but evaluates itself`，而不改變推導狀態。  
W-12 ADOPT — 同一方法與 companion identity 的來源仍緊密相連，未多黏一個獨立論證。  
W-13 MODIFY — `the functions`／`the ones` 容易錯稱只有 sine、cosine 滿足 \(s''=-s\)。改稿：“This relation \(s'' = -s\) is the signature of <em>simple harmonic motion</em> (Figure 3.4). Both sine and cosine have this relation, so they can be used to describe oscillation.”  
W-14 MODIFY — 改稿仍有 `reproduces itself`，且沒有字面說出二階導數為負函數本身。改稿：“One differentiation of \(e^{x}\) gives \(e^{x}\) again (§2.4). For sine and cosine, four differentiations return to the original function. After two differentiations, each function is its negative, which gives the relation \(s'' = -s\) in Example 3.3.”  
W-15 ADOPT — `bare form` 已由緊鄰的 \(\sin x\)／\(\sin(x^2)\) 對比明確釋義；逗號對比自然。  
W-16 ADOPT — composition 的定義仍在同句，單破折號改逗號恰當。  
W-17 ADOPT — 直觀的 scaling 與正式的乘積結論可各自成立，分句不是機械拆分。  
W-18 ADOPT — 後段是兩項既有結果的同位清單，逗號足夠。  
W-19 ADOPT — `proves it` 準確取代交易隱喻，且 proof 導覽功能保留。  
W-20 ADOPT — formal definition 未動；error behavior 與 first-order gloss 分開後更易讀。  
W-21 ADOPT — `namely \(f'(x_0)\)` 是單純同位說明。  
W-22 ADOPT — 零值分支、\(R_2(0)=0\) 的理由、非零分支與 factorization 的順序均正確。  
W-23 ADOPT — 分詞片語只是錯誤寫法的例示，不是第二個論證。  
W-24 ADOPT — 導數乘積的結論與 Figure 3.5 的直觀說明可分開閱讀。  
W-25 MODIFY — `small problem of its own, here a quotient rule` 仍含不透明搭配且黏合兩個動作。改稿：“The chain rule does not finish the computation by itself. It also requires the derivative of the inside. In this example, that derivative is found with the quotient rule.”  
W-26 ADOPT — outer／inner function 的資訊被併入 composition 的規格，且結尾冒號只引出公式。  
W-27 ADOPT — 兩條生態依賴關係是同一個平行的 dependency-chain setup，不是違規黏接。  
W-28 ADOPT — 非形式因果鏈與符號符號鏈的對應是兩個獨立教學動作，拆分正確。  
W-29 ADOPT — 首句為合法導航句，次句立即字面交代可得到哪些導數。  
W-30 ADOPT — 分號是對稱的章節對比，`uses it` 已移除交易隱喻。  
W-31 ADOPT — 拆開「沒有可微分公式」與「作為 inverse 使用」兩個命題，指涉清楚。  
W-32 ADOPT — 方法陳述已改為可直接執行的字面指令。  
W-33 MODIFY — `run backward`、`pushing ... forward`、`read off` 仍是關鍵方法位置的隱喻。改稿：“The method uses the chain rule in the reverse direction. In Strategy 3.1, we start with known derivatives and apply the chain rule to a composition. Here we apply the chain rule to a known relation and solve for the derivative that is not yet known.”  
W-34 ADOPT — 修正修飾語誤掛，並以 `That is` 直接給出 inverse 的字面說明。  
W-35 ADOPT — outer/inner decomposition 與套用 chain rule 是不同操作，拆分合理。  
W-36 ADOPT — 已去除 `trapped`／`set it free` 的戲劇化表述，`isolated` 是中性數學動詞。  
W-37 ADOPT — 將 `powers a technique` 改為明確的功能敘述。  
W-38 ADOPT — `long` 是對 EFL 可預測的直接替代。  
W-39 ADOPT — 逗號後為 strategy heading 的限定條件，結尾冒號引出步驟清單。  
W-40 ADOPT — 後段是 composition 的單純同位描述。  
W-41 ADOPT — `remembering for when we turn to integration` 保留了有用的前向導航，且已移除 `filing away`。  
W-42 ADOPT — `same method works` 字面且與後句的 trigonometric identity 明確相接。  
W-43 MODIFY — 不能暗示「是 inverse」本身就足以推出可微；應說明實際使用的 relation。改稿：“To differentiate the logarithm, we differentiate its inverse relation with \(e^{x}\): \(e^{\ln x} = x\).”  
W-44 ADOPT — 在前文已限定 arcsine branch 的脈絡中，open interior 與 \(\cos x\neq0\) 的關係正確。  
W-45 ADOPT — 正根的選擇條件 \(\cos x>0\) 完整保留。  
W-46 ADOPT — 直接微分的總結與「沒有規則」的理由是可分離的兩個動作。  
W-47 MODIFY — `matching identities` 仍不足以字面交代 branches，且不如列出實際 identities。改稿：“In every case, we found a known identity that the function satisfies, differentiated it by the chain rule, and solved for the one unknown. For \(x > 0\), the identities were \(e^{\ln x} = x\) and \(\ln(x^{x}) = x\ln x\). For the inverse trigonometric functions, they were \(\arcsin(\sin x) = x\) for \(-\tfrac{\pi}{2} \le x \le \tfrac{\pi}{2}\), \(\arccos(\cos x) = x\) for \(0 \le x \le \pi\), and \(\arctan(\tan x) = x\) for \(-\tfrac{\pi}{2} < x < \tfrac{\pi}{2}\).”  
W-48 ADOPT — 鄰近 examples 已使 `same method` 有明確指涉，屬合法導航句。  
W-49 MODIFY — 改稿仍留下 `pushing ... forward`、`turned on`、`reach` 等承載結論的隱喻。改稿：“The chain rule can be used to differentiate a composition. It can also be applied to a known identity to find derivatives for which no direct differentiation rule is available.”  
W-50 ADOPT — `rigorously` 直接取代 `on solid ground`，所有 Chapter 4 的數學依賴保留。  

Q1. 沒有。修正後的拆句都對應獨立的定義、理由、操作、結果或清單。W-27 雖保留兩條 dependency links 於同句，但它們構成一個平行的 setup，屬條款允許的平行列舉；W-25 是唯一原改稿仍有重新黏接風險者，已在上方改為三句。

Q2. 沒有 scope、條件—結論或先行詞被拆散。W-22 先固定 \(0<|h|<\alpha\)，再分零值／非零值情況，`Otherwise` 的範圍正確。W-07 依序保留符號反轉、ratio 不變、even 命名與 \(\theta>0\) 的限制。W-10 保留 unit-circle arc length、radian measure 與極限依賴關係。W-09 則須依我的改稿分清 continuity 與 fundamental limit 的功能。

Q3. K-1、K-2、K-3 都應 KEEP。K-1 是必要條件；K-2 是同一主張內的對比；K-3 只是指回剛算出的 \(2x\)，沒有另立理由、定義或結論。反查所有判為整句重寫的成對插入語，我沒有找到應反轉為 KEEP 的一對；尤其 W-25 雖短，仍在界定 chain rule 所要求的量，具有獨立教學用途，不能當作純節拍插入。

Q4. 正確。章首的 `unlock` 有明確 antecedent、導航功能與後文的字面內容；Remark 3.3 標題不承載數學條件。W-06 與 W-22 只動散文外框，未動推導。cleft 例句不應僅因句型處理。段落層沒有觸發 MUST 人工判定，且兩段略長段落均是一主題，故不拆段。

Q5. 就「不是手稿逐字」而言，推論成立：極低的 6/8-gram 重疊與 em-dash 零存活，已足以否定逐字手稿例外；ch01 對照進一步支持此結論。這些量測本身無法邏輯上區分 LLM 重寫與人類大幅改寫，但不影響作業結論：fragment 不是可受逐字手稿保護的文本，因此本輪不保留手稿例外是恰當的。

Q6. 有。以下是具 R1／R2／R3 證據、建議補入 sweep 的項目：

- §3.1 lead、§3.2 opening 的 `where one function is fed into another`（R1/R2）：composition 的早期 gloss 使用隱喻；改為 `where the output of one function is the input of another`。
- §3.1 的 `the entire computation funnels down`、`squeezed to a limit`（R1/R2）：核心方法應明說是 area inequalities 與 the squeeze theorem，而非只靠漏斗／擠壓隱喻。
- §3.1 Example 3.1 的 `something \(\sin\) can handle`，以及 Example 3.2 的 `identity ... collapses the numerator`（R1）：分別改為 `a form involving \(\sin\theta\)` 與 `reduces the numerator to \(1\)`。
- §3.1 Example 3.3 的 `how far it has strayed`，以及 Remark 3.1 的 `Differentiation sends ...`／`sign ... turns over`（R1）：應直接說距離 rest level 與微分後得到另一函數、符號每兩步改變。
- §3.2 Remark 3.2 的 `strike out`（R1）：此為關鍵警告，改為 `cancel`；Strategy 3.1 的 `work from the outside in`、`leave it untouched`、`Peeling` 也應改成可執行的 `start with the outermost operation`、`do not differentiate it yet`。
- §3.2 proof bridge 的 `comes out by substitution`、`feeding one into the other`、`gathers into a single remainder`（R1/R2）：應明說 substitute the expansion for \(g\) into that for \(f\)，其餘項 form one remainder。
- §3.2 Example 3.8 的 `Read off the sign`、`chains the two rates`（R1）：操作指令宜改為 `Determine the sign` 與 `gives the product of the two rates`。
- §3.3 的 `no rule of Chapter 2 can touch directly`（R1/R3）：應與 W-32 對齊為 `no rule of Chapter 2 can differentiate directly`。
- §3.3 的 `The same move`、`its parent`（R1/R3）：應穩定用 `the same method` 與 `the original trigonometric function`。
- §3.3 Example 3.13 的 `trades one hard ... for`，以及最終 summary 的 `breaking ... touch ... read off ... turned loose`、`Two debts remain`／`taken on`（R1/R2）：前者是交易隱喻，後者在章節結論承載實際方法與未完成的 rigor；應改為 `replaces`、`evaluating/deriving/using`、`Two earlier steps still require rigorous justification`。

Q7（題面另列）. 有三項需特別修正。W-13 的 supplied AFTER 有過度斷言風險：\(\sin\)、\(\cos\) 的線性組合也滿足 \(y''=-y\)，故採我給的非排他改稿。W-09 需區分 continuity 對第一因子的作用與 fundamental limit 對第二因子的作用。W-43 不應把 inverse 性質單獨說成可微的充分理由。W-10 本身數學安全；W-44／W-45 保留了 arcsine branch 內的 open-interval 與正根條件；W-47 應採我的完整 identities 與 branches，才是對 `their kin` 的忠實、可檢查替換。

---

## 折入時的處置（本輪 gate-3 裁決）

| Codex 條目 | 我的處置 | 理由 |
|---|---|---|
| W-02 | **MODIFY-調整** | 採「geometric comparison」的字面化，但保留章 lead 的 `First we … / Then we …` 平行結構（Codex 版拆成兩句會斷掉與下一句的對仗）。 |
| W-04 | **MODIFY-調整** | 採 Codex 的字面說法，但避免 `cancels … canceled` 的同詞複現。 |
| W-05 | **MODIFY-調整** | 接受「單一極限不足以推出導數」的糾正，但不在節開場前置提及 continuity（該詞要到下一小節才引入）；改用「is the main step toward」表達非充分性。 |
| W-07 | **ADOPT-調整** | 採 Codex 三句版，但保留原文 `shrinking to \(0\)` 的措辭（無理由改）。 |
| W-09 | **ADOPT（Codex 版）** | Codex 抓到的是**既有課文的錯誤**（continuity 並非兩個因子都需要），逐字採用其改稿。 |
| W-13 | **ADOPT-調整** | 採非排他敘述；動詞由 `have this relation` 改為數學英文慣用的 `satisfy this relation`。 |
| W-14 | **MODIFY-調整** | 採「兩步即得 \(s''=-s\)」的字面補充，但不重述前一句已說過的「四次導數回到原函數」（F1 局部冗餘）；保留與 §2.4 `e^{x}` 的對照書擋。 |
| W-25 | **MODIFY-調整** | 採三句版，末句改用本例前文已用過的 `quotient-rule computation`（R3 一致）。 |
| W-33 | **MODIFY-調整** | 採 Codex 的字面化與 `solve for`（與斜體方法陳述同詞，R3 一致），但保留 `It is the chain rule run backward.` 作為有明確先行詞的短導航句。 |
| W-43 | **MODIFY-調整** | 接受「不得暗示 inverse ⇒ 可微」；改寫為「differentiating the relation … that expresses \(\ln\) as the inverse of \(e^{x}\)」，同時保留與下句 `The same method works …` 的銜接（Codex 版會斷掉）。順帶消去一個冒號接子句。 |
| W-47 | **MODIFY-部分採用** | 採「列出實際 identities」而非模糊的 `their kin`；**未採**逐一列出三個 branch 區間——三個區間在 Example 3.14–3.16 與 Caution 已各自明訂，於 Remark 重列會把摘要撐成清單，且新增 6 個行內式。折衷為列出三個 identity ＋「each on the branch fixed in its example」指路。 |
| W-49 | **MODIFY-調整** | 採字面化，但併為一句以免 Remark 結尾出現連續三句同長（SPEC SHOULD 的節奏條）。 |

**Q6 第二波 triage（16 項提名 → 採 9 退 7）**

採納：`fed into`（§3.1 lead）、`funnels down`、`something \(\sin\) can handle`、`collapses the numerator`、`how far it has strayed`、`sign … turns over`、`strike out`、`leave it untouched`、`feeding one into the other`／`gathers into`、`Read off the sign`、`touch directly`、`The same move`、`its parent`、`trades … for`、`breaking … read off`、`turned loose`。

退回（**示範規則不誤傷**）：

1. **`squeezed to a limit`（§3.1）** — 這不是隱喻，是 **squeeze theorem（§1.5）的術語**，證明段落逐字使用該定理名。SPEC 的術語豁免適用。
2. **`Two debts remain … both were taken on informally`（章末）** — credit／debt／repay 是**全書刻意貫穿的機制用語**（SPEC §16.1，首見已 gloss；ch04 kickoff 明令「一律保留，只動周邊贅飾」，ch06 §6.2 W-13(a) 為既有前例）。屬 ⛳ 政策題，本輪維持現狀、不動。
3. **`fed into`（§3.2）** — 同一段的下一個子句就是字面 gloss（`the operation of applying one function to the output of another`），非唯一載體；且 `<em>into</em>` 的強調是刻意的。§3.1 lead 那處無鄰近 gloss，故只改那處。
4. **`work from the outside in`／`Peeling`** — Strategy 3.1 的**方法名稱**，步驟 1 立即字面化為「Identify the outermost operation」。名稱可記憶且已釋義。
5. **`chains the two rates`** — 呼應規則名稱 chain rule，對讀者透明。
6. **`comes out by substitution`** — 透明且該段末句已字面說出證明的實質內容。
7. **`Differentiation sends sine and cosine into each other`** — `send`／`map` 是標準數學英文，非戲劇動詞。

*本檔 2026-07-25 建立。*

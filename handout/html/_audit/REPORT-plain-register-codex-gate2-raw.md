# Codex gate-2 raw：課文英文平實化研究與方案的第二意見

- 調用：`codex exec -s read-only`（stdin 餵 UTF-8 prompt，材料全 inline、未讓 Codex 讀檔——遵循 2026-06-28 編碼坑紀律），codex-cli 0.144.1，模型走 `~/.codex/config.toml` 預設（gpt-5.6-terra／max）。
- 日期：2026-07-25。授權：使用者本輪明示「把想法跟 Codex 討論一下」（CLAUDE.md 2026-07-01 Codex 唯讀逐次徵詢條款）。
- 受審材料：`REVIEW-plain-register-research.html` 的診斷＋研究發現＋方案 A–E（inline 摘要版）。
- 本檔為 **raw 輸出照登**（未刪改）；整合裁決見 `REVIEW-plain-register-research.html` §7。

---

## Q1

部分成立，但「病灶在修辭句法而非句長詞頻」切得太二分。較準確的診斷是：Flesch/FK 量不到「目標讀者熟悉的詞義、搭配、慣用語、隱含推論與資訊結構」。這正是 EFL 自學生的主要負荷。

- `"rescues"` 本身不罕見，但 `continuity rescues functions` 的擬人搭配不直白。
- `"coincidence too strong to be one"` 的問題不只文學，而是沒有說出究竟是哪個數學模式。
- `"a great deal"`、`"earned in full"` 都是短而不透明的慣用式。

不過，不能把 `cleft` 視為病因。例如：`What matters here is the sign of f'(x).` 是常見且清楚的焦點標示。問題是「cleft + 隱喻 + 懸念式敘事」的組合，不是 cleft 本身。

題列研究可支持「模型有風格漂移傾向」這個先驗，但不足以證明本案必然由 RLHF house style 單獨造成；也可能是 §3 的「溫暖」、範文選取、V1 的單向獎勵，或近期章節 prompt 的局部變動所致。

更省的第一步不是立即建完整五層，而是做小型對照試驗：選 12–20 段、涵蓋開場、定義、推導、例題、收尾，比較「只換範文」「每次附短 style card＋正反例」「style card＋獨立 plain pass」三種版本，再用盲讀理解題、數學正確性與編輯判定比較。單句 system prompt 的泛泛「write simply」不可靠；每次在場的短規格加對照例，則可能已拿到大部分收益。換模型或改 agent 策略應是此試驗的一個組別，不應先驗假定必要。

## Q2

整體裁決：A、B、D、E 為「修改後同意」；C 為「先儀表板、後規則化」，反對一開始就做 blocking gate。

A 的規格應分成 `MUST / SHOULD / FLAG` 三類，而非把所有語法現象都禁掉。

`MUST`：

- 數學命題、量詞、條件、例外與操作步驟不得只靠隱喻或慣用語傳達。
- 一個概念在局部說明範圍內使用穩定術語與代稱；這是「同義概念同措辭」，不是禁止正常的文法變化。
- 在定義、首度出現、指令、結論等關鍵位置，陌生的非術語詞必須改成直白詞，或緊鄰平實釋義。
- 非正式散文句達 35 詞時，必須人工判定「保留或拆分」並留理由；不應機械拆句。

`SHOULD`：

- 剝除公式、標題、列表後，散文平均句長可暫定以 18–22 詞為目標；它應是監測值，不是全球硬門檻。
- 以第 90 百分位句長監測長尾，比平均值更有用；可先暫定 32–35 詞為審查區。
- 優先使用常見、字面、可預測的搭配；優先主動語態，但被動語態不可當成錯誤。
- 一句有一個主要教學動作，並可攜帶必要條件；不是「一句只能有一個邏輯子句」。

`FLAG`，只送人工看：

- cleft、尾掛 `-ing`、被動、`not X but Y`、數學物件作主詞。
- 這些形式的假陽性很高，不能直接判壞。

「非術語高頻詞天花板」的措辭也要改。可測的是「低頻風險詞的下限」或「未說明低頻內容詞的比例上限」；若直接做 NGSL/NAWL token coverage ≥95%，大量功能詞會把數字灌高，幾乎失去意義。

B 的方向正確，但 plain pass 應是「有標記、定向的一輪」，不是再叫同一模型泛泛重寫。鎖住公式、術語、標籤、cross-ref 和定義編號；輸出應有可審查 diff。每次嵌入規格可行，但應是短且版本化的 style card，加 2–3 個數學散文正反例，而不是塞入長篇政策使重點稀釋。

C 可做，但先當報告，不當裁判。wordfreq、spaCy 與 textstat 最適合找候選句，不適合判定 EFL 可讀性。尤其 `rescues` 可能頻率不低，而真正難的是其搭配與語用。

D 應提前到 pilot 前。R 維度可保留，但建議改成：

- R1：非術語詞彙與慣用語的可推測性。
- R2：字面傳達與明確指涉。
- R3：術語、代名詞與概念指稱的一致性。

「承載解釋只靠隱喻」應 blocking；但關鍵定義或指令中出現一個不透明慣用語，也可 blocking。另一方面，零星 advisory 若在一頁累積很多，應觸發頁面級複查，否則會形成「每句都不夠嚴重、整頁仍難讀」的漏洞。V1 不應獎勵「更暖」本身，而應獎勵讀者導航是否更清楚。

E 同意，但 pilot 不宜只測 §6.2 的一種文體。至少要含動機段、正式定義、推導說明與例題。成功條件應預先寫下：數學內容無退化、EFL 理解題不降、清晰度上升、版面仍符合 A4 限制。

## Q3

真正的「暖」不是替數學物件加人格，而是替讀者補上方向、目的與連接。因此，應採「邏輯內容平實；教學導航可溫暖」的雙層規則。

一個暖句只有同時通過下列條件才保留：

1. 讀者能在本句或相鄰句找到明確指涉。
2. 它說明「為何現在做這一步」或「剛剛得到什麼」，不是只製造氣氛。
3. 刪掉它會損失導航或動機，而不只是少了一句漂亮話。
4. 任何數學條件都已有字面、可檢查的表述。

可允許的結構性暖意包括：

- `To describe [phenomenon], we need a more precise definition.`
- `The next example shows why this condition is necessary.`
- `We now have a test that lets us decide whether [property] holds.`
- 在剛完成明確推導後：`This gives our first example of a limit.`

`This is our first limit!` 若前一句已明確寫出極限關係，它是對成果的標記，不是承載數學內容，可以保留在章節敘事區。它不應取代定義、證明或操作指令，也不應變成每段都有的感嘆句。

五句可改成下列方向；方括號必須換成實際數學內容，不能再用模糊代詞掩蓋：

| 原句問題 | 平實改寫方向 |
|---|---|
| `coincidence too strong to be one` | `Section 6.1 revealed a pattern: [state the pattern]. In this section, we determine when it holds.` |
| `outlived the shaky infinitesimals...` | `Early work used informal ideas about infinitesimals. Here we use a limit-based definition of the notation.` |
| `What rescues...` | `For the functions in this section, continuity ensures [the required property].` |
| `Definition 6.2 asks a great deal...` | `Definition 6.2 requires every allowed choice of sample points to lead to the same limiting number.` |
| `honest boundary... earned in full` | `This chapter establishes [specific result]. Later results require additional assumptions or tools.` |

這樣不會變成乾巴巴的 Spivak 腔，前提是保留「目的先行、過渡明示、成果命名、例子跟進」；該刪的是文學性的懸念與擬人，不是讀者導向的聲音。

## Q4

若把 pattern 偵測當判決器，假陽性會高到不可用；若把它當候選清單，則很有價值。

| Pattern | 判定 | 反例／風險 | 建議 |
|---|---|---|---|
| cleft | 假陽性高 | `What matters here is the sign of f'(x).` 很清楚 | 僅提示，絕不 blocking |
| 數學主詞＋動詞 | 取決於動詞 | `The graph shows...`、`The definition requires...` 都正常 | 只標記情緒性、戲劇性動詞，如 `rescues`、`longs for` |
| 尾掛 `-ing` | 假陽性高 | `The interval becomes shorter, making the error smaller.` 可很順 | 檢查懸垂修飾或壓縮因果，不以形式判錯 |
| negative parallelism | 假陽性極高 | `The derivative gives a rate of change, not a total change.` 是好教學句 | 不應列為 AI 癖規則 |
| AI 癖詞表 | 中低精度 | 單字可能在正當語境出現 | 優先抓多詞搭配與戲劇性組合，人工複核 |

建議每條規則先以人工標註的命中樣本測「可採納率」與「每千詞警報量」。一條規則若編輯常常忽略，就應降級或刪除；blocking 規則必須有遠高於一般儀表板的精度。

OpenStax 與 CLP 可以作為「可接受分布」的參考，不能合成一個單一金標。兩者文體不同，且目標讀者是台灣 EFL 自學生，不是原作者的母語讀者。正確作法是按功能分層比較：開場、解釋、定義、例題、證明、習題文字各自取樣；排除或一致處理公式、標題、caption、列表。基線用來發現自己突然偏離，不用來要求平均值完全相同。

更省的替代是先做 Vale 的高精度 phrase rules、術語白名單與人工詞彙報告。先驗證 HTML/LaTeX 剝除後的句子切分沒有破壞公式、`\ref`、環境與巨集，再考慮 spaCy 依存分析。NGSL/NAWL 應只看內容詞 lemma，並把「每百詞未說明風險詞」當提示，不要設 95% 硬閘。

## Q5

原順序接近正確，但 D 不應排在 C 後面。沒有人工已裁決的 R rubric 與 pilot 標註資料，C 會把偏好直接硬化為規則。

建議順序是：

`A + D 最小規格與判定準則 → B 重寫多類型 pilot → E 盲讀／數學／版面驗證 → C 最小 linter 與基線校準 → 修訂 A/D → 新章採用 → 分批回填舊章`

C 的資料蒐集可提早開始，但完整規則庫應等 pilot 後再做。pilot 要記錄每千詞接受了多少改動、每千詞審查花多久、哪些規則誤報最多；這些才是估算 ch01–ch06 加附錄工作量的可靠基礎。沒有總字數、圖表與 cross-ref 密度，現在給工時數字會是假精確；可以確定的是，舊章回填與再驗證會是主工期，不是規格撰寫。

回填的主要風險如下：

- 既有 audit 結論綁定的是舊文字版本；改過的段落必須重新過相關閘，不能沿用舊的 pass。
- 改寫若動到標題、display math、caption、列表或 theorem/definition 環境，可能引發編號、cross-ref、目錄與頁碼連鎖變化。
- 短句化會增加行數，可能改變 single-sided A4 的溢頁、孤行與圖文相鄰關係。
- 平實化很容易在條件、量詞、因果方向上引入微小數學錯誤，因此 prose gate 後仍要再跑 math gate。
- 應保留變更帳：改了哪一句、為何改、是否重跑過數學／圖／出版驗證。

不要全書一鍵重寫。先回填章節開場、正式定義前後、跨章過渡、例題說明等讀者負荷最高處，再以章為單位發布可回溯版本。

## Q6

幾個重要盲點：

- 高頻不等於好懂。`only if`、`unless`、`respectively`、`arbitrary`、`at most` 可能不低頻，卻是 EFL 數學理解的高風險詞；應教它們、固定用法、給例子，而非只靠詞表淘汰。
- 過度拆句會提高整合負荷。數學讀者常需要在同一句看到條件與結論的作用域；「短」必須配合明確連接詞與段落結構。
- 最好的平實化常不是換詞，而是補一個具體數值例子、圖上指涉或 formal statement 後的白話重述。文學腔有時是在掩蓋缺少中間解釋。
- Claude gate 與 Codex gate 即使都通過，也不等於對 EFL 真正獨立。題列的 LLM–人類相關係數不足以直接支撐 blocking 決策；需要少量真實目標讀者與人工校準。
- 正式定義、證明、例題、敘事過渡應有不同 linter 模式。把同一套 STE 式規則套到所有段落，會傷害證明和精確定義。
- 詞表、白名單、例外與模型 prompt 都需要版本治理：誰可新增例外、何時淘汰規則、如何做 regression corpus。否則一年後會形成不可解釋的規則堆。
- HTML→LaTeX 線必須把 linter 設計成「報告、不寫入」優先，並在最終 PDF 做視覺驗證。公式剝除與句切分若錯，統計值會系統性失真。
- 影片旁白不應逐字套用出版稿。兩線應共享術語、邏輯次序與禁忌，但旁白另需考慮可朗讀性、公式念法、停頓與語速。
- 以 OpenStax/CLP 作 few-shot 時要避免近似改寫或無意重用句子；使用風格標註與自製對照例，比貼長篇原文更安全。
- S·A·V 與 R 必須有優先序：數學正確性與字面可理解性優先於流暢、聲音與「溫暖」。任何暖意不得用來抵銷不透明表達。

## 總裁決

GO-with-changes。方向正確，尤其是承認可讀性公式抓不到語域問題、把約束放回每次生成、以及先做 pilot；但最重要的三項修改是：(1) 把「全面禁 cleft／擬人／低頻詞」改成「數學內容必須字面化」的 MUST，加上情境化 FLAG，避免把正常教材句法一起殺掉；(2) 把 D 與真實 EFL 盲讀提前，先用多類型 pilot 決定何者真有讀者效益；(3) C 先做高精度候選報告與分功能基線，絕不可把詞頻覆蓋率或粗糙 pattern 直接升格成 blocking gate。

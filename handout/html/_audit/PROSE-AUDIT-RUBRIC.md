# 講義散文稽核 — 維度與擋稿線（PROSE-AUDIT-RUBRIC）

> 本檔是「散文稽核」兩道閘——**Claude subagent（gate 1）**與 **Codex 獨立（gate 2）**——共用的契約與**單一真相來源（single source of truth）**。兩道閘都讀本檔判斷；維度／擋稿線**只在這裡改一次**。
>
> 語域與結構的**權威規範**見 [`CONTENT_SPEC.md`](../../../CONTENT_SPEC.md) §3（語域與語聲）、§15（最終一致性檢查）。本檔只定「審哪些維度、哪些擋稿、哪些不算 finding、怎麼回報」，**不重述** §3 的規範本身。

## 審查對象與邊界

- **審**：講義單節 fragment（`handout/html/fragments/ch{NN}/sec-*.html`）裡的**英文說明散文**——`<p>` 等敘述／動機／解釋文字。
- **不審**：數學正確性、圖、example 選題、編號／排版——這些有各自的 audit（見 [`_dev-archive/general/PROMPT-audit-dimensions.md`](../_dev-archive/general/PROMPT-audit-dimensions.md)）。math 公式只當語境，**不評對錯**。

## 四個維度

### A. 易懂性 Comprehensibility（§3 結構規則；部分 BLOCKING）

讀者「跟不跟得上」。據 CONTENT_SPEC §3。

- **判讀視角 reader persona（2026-06-28 定）：** 易懂性以「**讀完高中先修、用英文（非母語）自學、第一次線性讀**」的讀者為錨判，不用審稿者的後見之明。實證（外部模型 first-read 校準，見下「可選：跨模型 first-read」節）顯示：同一節改用此 persona 讀，才抓得到審稿視角會略過的首讀摩擦——首次未定義詞、跳一行代數、沒鋪動機的戰術選擇（如憑空挑 ε = |L−M|/2）、L2 讀不動的長句。這些摩擦多半早已落在下列 U／F 維度（U3 跳步、U4 先用後定義、F3／F4 句構句長）——persona 只是把判讀對準真讀者，**不新增維度、不放寬下方 no-dumbing 護欄**。

- **U1 動機缺位** — formal statement（definition／theorem／…）前面沒有動機散文說明「為何引入、直覺上是什麼」（§3：formal 前該有 1–2 段；純計算短節可只用一句承接句，為合法例外）。
- **U2 重型形式無 gloss** — 語法重的定義（巢狀量詞、ε-δ、符號密）沒有「*Informally, …*」白話重述（§3 規則）。形式已近英語、僅一兩個符號者**不需要** gloss，別反向挑剔。
  - **白話重述可在 inline gloss、或定義前後相鄰散文任一處。只有當附近完全找不到任何白話重述、讀者被卡在純符號上，才算 blocking。** inline 缺、但相鄰散文已充分解拆 → 至多 advisory（可建議補 inline gloss，但不擋稿）。
- **U3 未解釋的邏輯跳躍** — 自學讀者無法自行重建的一步，缺 *because*／*therefore*／*since* 等橋接（§3 明文禁止「未解釋的邏輯跳躍」）。
- **U4 術語／記號先用後定義** — 術語或 notation 在被引入前就使用，把讀者晾住（forward dependency）。
  - **blocking 限於「讀者被晾住、無法從使用處的散文重建其義」。** 若記號在使用處當場以散文 gloss、讀者可重建其義 → 降為 advisory（建議調整順序，但不擋稿）。
  - **結構性排序（需 reorder）優先往上游：** 若修法是「**把一個定義／介紹段搬到它首次被用之前**」（非在使用處補一句 gloss）——例如新記號在 example 用掉後才正式定義（ch01 §1.4 `=∞` 即此型）——這是**結構**問題，最便宜的修點在 Mode A 方向層（[`CONTENT_DIRECTION.md`](../../../CONTENT_DIRECTION.md) §2「範圍與深度」之 introduce-before-use），**編號鎖定後才搬會 cascade 編號與 cross-ref**。散文閘照報此 U4，但**標明「需 reorder＝結構，宜上游處理」**，別在定稿期硬搬。
- **U5 定義後未拆解** — 重定義之後沒有散文解拆「這條件排除了什麼／該怎麼讀」（§3：definition 後的散文解拆）。

### B. 流暢性 Fluency（copyedit；全 ADVISORY）

「寫得順不順」。保留語意，只收緊。

- **F1 局部冗餘** — 一個詞／概念在 1–2 句內無新意地重述（命名後緊接重述的老毛病）。
- **F2 贅字** — filler／疊字（*the fact that*、*in order to*、*basically*、*actually*…），刪了零語意損失。
- **F3 句構可解析** — garden-path、子句堆疊、動詞前鋪陳過長、修飾語誤掛，讓人一眼解析不出。
- **F4 句長／認知負荷** — 一句塞太多概念，超出自學讀者一次能扛的量；給切點。
  - **黏接句判準（2026-07-25 新增，同日經 Codex 覆核修訂；CONTENT_SPEC §3 平實英文條款連動）：** 對 EFL 讀者，殘餘難度的主要來源是「一句內塞兩個可獨立成立的推論或教學動作」。**判準是論述動作數，不是長度也不是子句數**——定義、條件＋結果、公式說明、平行列舉各自都算**一個**動作，這類長句**不算 finding**（不得因長度報 F4）。觸發器（≥30 詞＋黏接訊號：冒號接子句／分號／破折號／and-while-which 串接）只是**要人工看一眼**，不是拆句命令。
  - **不得報為 finding**：正式定義與定理陳述、平行列舉、路線圖句、引文；冒號後引清單／公式／標籤者不算「冒號接子句」。
  - **反向護欄**：改寫 MUST NOT 拆散量詞 scope、條件—結論、代名詞與先行詞；MUST NOT 造出連續三句長度相近的連續散文（以朗讀聽感判，排除列表與刻意平行）；MUST NOT 為維持句數而用任何標點把兩個獨立推論黏回一句。符號密集段落優先改 display／分行 skeleton／先立記號，而非按詞數切句。
- **F5 語域** — hedge、過度口語（*super easy*、*you guys*）、黑板縮寫（*iff*、*w.r.t.*、*s.t.*）、代名詞策略（*we* 預設；*you* 僅用於溫和提醒或 forward reference）。

### C. 語意／聲音 Substance／Altitude／Voice（S/A/V 語意層 critic；部分 BLOCKING）

讀者「會不會覺得這是機器寫的」——但**不是數 tell／密度，是讀意思**。**中性 ≠ AI；中性＋空才是 AI**（[`PLAN-deai-semantic-critic.md`](../../../authoring/_archive/deai/PLAN-deai-semantic-critic.md) §0）。對每個候選句/段跑下面三組診斷，**每條 finding 強制附證據**。

**S — Substance（這句掙得它的位置嗎？）**
- **S1 資訊** — 相對前句、相對數學式本身，有沒有加**新洞見**？（只把算式翻成英文卻沒加東西＝空）
- **S2 具體性** — 斷言針對**這個**物件/問題，還是「貼到任何節都成立」的通用填充？
- **S3 刪除測試** — 刪掉讀者有損失嗎？**沒有→建議刪，不是改寫。**

**A — Altitude（對自學者高度對嗎？）**
- **A1 嘮叨** — 顯而易見的步驟被長篇解釋？（過高）
- **A2 跳步** — 真正難的一步被略過/揮手帶過？（過低）
- **高度 self-relative：** A1/A2 對著「**這節在教什麼、這一步本身多難**」判，**不**對著範本判（避免引進別人的教法）。範本只示範「好高度的形狀」。

**V — Voice（§3 那點暖到位嗎？）**
- **V1 平** — 某處只機械陳述、缺了 §3 要的動機/直覺鋪陳？（**不是**叫它灌人格/加笑話——只問「§3 本來就要的那點暖在不在」）
  - **V1 寬報校準（2026-06-26 使用者拍板）：** V1 **永遠 advisory、never blocking**，且採**寬報**——不只「該暖全無」要報，連「**中性但可更暖**」（某句本身偏平、§3 可更暖，即便鄰句已補上直覺）也列為 advisory，交使用者逐條裁。下方防呆 2「中性不扣分」只約束 S/A 的 blocking 判定，**不豁免** V1 的「可更暖」提示。
  - **V1 邊界（2026-07-25，平實英文條款連動）：** V1 獎勵的「暖」＝**教學導航更清楚**（動機、過渡、成果標記——CONTENT_SPEC §3 暖句四條件），**不是** lexical 修辭。V1 建議 **MUST NOT** 以提高語域為手段（不得建議加隱喻／擬人／警句收尾）。與 R 維度分工：R 砍不透明、V1 補導航，兩者不衝突。

**兩個防呆（避免重蹈 metric/tell 覆轍）：**
1. **真人範本當錨 ＋ 強制附證據** — gate 跑 S/A/V 時，**prompt 末尾掛 [`anchors/svc-exemplars.md`](anchors/svc-exemplars.md)（固定 2 正 1 負真人範本）**，標為「言之有物的真人數學散文」，**對著正面 bar 判、把負面當「該 flag 長這樣」**。每條 finding **必附**：問題句＋踩哪個測試（S1/S2/S3/A1/A2/V1）＋一行為什麼＋改寫（或「刪」）。→ 可稽核，不是憑感覺。
2. **中性不扣分** — 純粹平實、中性但言之有物的句子**不准 flag**（指 S/A：不因「中性」就判它空／錯高度——那正是目標）。只抓空（S）/錯高度（A）/該暖沒暖或可更暖（V1 寬報 advisory，見上）。

**擋稿線（從嚴、寧少報）：** BLOCKING = ① **空句佔位**——某句踩 S1（無新洞見）／S3（刪無損失）且**佔著承載教學功能的位置（動機／直覺／解拆）卻無實質**；或 ② **高度錯**——A2（真正難的一步被揮手帶過，讀者會卡）。其餘 S/A/V（單純 S2、A1 嘮叨、V1 平、非承載位的可刪 filler）一律 **ADVISORY**。
**收斂判準：** 該節 C 通過 = **S/A 的 blocking findings = 0**；advisory（含 V）不強制歸零。

唯讀、propose-only、**保語意、不動數學、不碰教學順序與選題**（copyedit 級硬護欄，同 A/B 維度）。Vale lint 的 flag 仍當零成本預標餵入（**降級護欄、預期 ~0**，非 gate）。

### R. 語域平實 Plain register（2026-07-25 新增；部分 BLOCKING）

EFL 讀者「查不查得出這句在說什麼」。據 CONTENT_SPEC §3〈平實英文條款〉（MUST／SHOULD／FLAG 三層）；緣起與研究證據見 [`REVIEW-plain-register-research.html`](REVIEW-plain-register-research.html)＋Codex 覆核 [`REPORT-plain-register-codex-gate2-raw.md`](REPORT-plain-register-codex-gate2-raw.md)。判讀視角沿用 A 維度的 reader persona（高中先修、英文非母語、第一次線性讀）。

- **R1 可推測性** — 非術語詞彙／慣用語／搭配對 EFL 讀者是否可推測？抓：不透明慣用式（*asks a great deal*、*earned in full*）、情緒／戲劇動詞配數學主語（*continuity rescues functions*）、罕見搭配。**單詞頻率不是判準**——*rescues* 不罕見，罕的是這個搭配。
- **R2 字面傳達與明確指涉** — 數學 pattern／條件／結論是否被字面說出，還是藏在修辭裡（懸念、悖論式措辭、模糊代詞——*a coincidence too strong to be one* 沒說出是哪個 pattern）？**補解釋優先於換詞**：若病根其實是缺一步中間解釋（文學腔在遮缺口），開 U 維度 finding 並標「補解釋優先」，不要只提詞彙替換。
- **R3 指稱一致性** — 同一概念在說明範圍內是否穩定用同一術語／代稱？抓 elegant variation（為變化而換同義詞）與代稱漂移；正常文法變化不算。

**FLAG 句式（掃描線索，非缺陷）：** cleft、尾掛 *-ing*、被動、數學物件作主詞、*not just X, but Y*——只當候選掃描線，判定一律回到 R1–R3 語義測試；**MUST NOT 僅因形式報 finding**（*What matters here is the sign of \(f'(x)\).* 是好句；*The definition requires …* 正常）。

**暖句四條件**（CONTENT_SPEC §3）：動機／過渡／成果標記句同時過「有明確指涉／說明為何這步或剛得到什麼／刪之有損導航／數學條件另有字面表述」四條即保留——合法的結構性暖**不是** R finding（與「§3-protected non-findings」同理）。

**擋稿線（R）：** BLOCKING = ① 承載教學功能的解釋（動機／直覺／解拆／指令）**只靠**隱喻、擬人或不透明慣用語傳達，字面表述缺席；② 定義、指令等**關鍵位置**出現不透明慣用語或陌生非術語詞且無緊鄰釋義。其餘 R（零星罕見搭配、可更直白的措辭、R3 漂移）→ **ADVISORY**。
**頁級累積規則：** 一節內 R advisory 密集（≳5 條）SHOULD 另升一條「節級複查」finding——防「每句都不夠嚴重、整頁仍難讀」的漏洞。
**詞彙替換不算吹毛求疵的條件：** 帶 R1／R2 證據（指出不透明處＋給改寫）的詞彙 finding 是正常 R finding；無證據的純同義詞美化才砍。

## 擋稿線（blocking vs advisory）

- **BLOCKING（讀者會卡住或被誤導）**：`U1` 嚴重（全無動機就丟形式）、`U2`、`U3`、`U4`；`F3` 中**會導致誤解、進而誤算**的真歧義句；**C 維度的 S/A blocking**（空句佔承載位＝S1/S3＋無實質，或 `A2` 揮手帶過真難步）；以及 **R 維度的 blocking**（承載解釋只靠隱喻／不透明慣用語、或關鍵位置不透明詞無緊鄰釋義——見 R 節擋稿線）。
- **ADVISORY（polish；讀者仍懂）**：`F1`、`F2`、`F4`、`F5`、`U5`、輕微 `U1`（動機偏薄但有）、`F3` 一般彆扭；C 維度的 `S2`／`A1`／`V1`／非承載位的可刪 filler；以及 R 維度的其餘（零星罕見搭配、可更直白措辭、`R3` 漂移）。
- **收斂判準**：該節 prose gate 通過 = **blocking findings = 0**。advisory 由使用者逐條裁決，**不強制歸零**。

## 不算 finding（§3-protected；別誤砍）

下列是**特性**，不是缺陷，絕不可當 finding 砍掉：

- §3 鼓勵的連接詞（*Notice that*、*Let us now*、*In other words*…）；
- 服務清晰度的「囉嗦」——§3 第一目標是 **clarity > compactness**；
- 「*Informally, …*」白話 gloss；
- *we* 代名詞、刻意的教學重複、章末／回查用的重述（§1 lookup-friendliness）；
- topic-term recurrence（該節就是在講那個詞，自然反覆出現，**不算** F1）；
- 語意等價的用詞差異。

## 護欄

- **流暢性 findings**：必須**保留語意**，只能收緊措辭（copyedit 護欄，同 video 潤稿模板）。
- **易懂性 findings**：**可以**提議「加」一句動機／一個 gloss／一條橋接（踩進 Mode B 的 Rewrite／擴充地帶），但一律是**提議，不是行動**——交回使用者裁決。
- 稽核員**唯讀**：只回報，不改任何檔案。

## 可選：跨模型 first-read 第二讀者（每章定稿前一次）

易懂性 A 的 reader-persona 校準，可由**一個外部模型**（DeepSeek／Codex／Gemini 等，不同訓練分布＝fresh eyes）跑一輪 first-read 補強——這是 [`CONTENT_DIRECTION.md`](../../../CONTENT_DIRECTION.md) §5 floated 的「偶爾請第三模型抽查」的具體落地。定位：**選用、每章定稿前一次**（非每次編輯都跑），且**外部 raw 輸出一律過本檔 U／F 維度＋四級 triage 後才交裁決**——不直接吃。

兩條硬紀律（2026-06-28 實證，ch01 校準）：

1. **餵乾淨 inline 文字，別讓模型自己讀檔。** Codex 在本機用 `-C <repo>` 自讀 fragment 會把 UTF-8 解成亂碼（`—`→`??`、`§`→`禮`、彎引號→`?`），整批「編碼 bug」全是假陽性、甚至誤判 worst stall。把 fragment 預先以 UTF-8 解好、**inline 進 prompt**（DeepSeek 路線）即免疫。（與 [`CONTENT_DIRECTION.md`](../../../CONTENT_DIRECTION.md) §5 工程坑「prompt 餵入 CJK 重編碼」是**兩個相關但不同**的坑：一個在輸入端、一個在模型自讀端。）
2. **reasoning 模型 run-to-run 會飄、且偏 over-report**（實測 severity 灌水成 Lost、夾帶吹毛求疵的詞彙替換）→ raw 不可直接吃，必接四級 triage（核 no-dumbing、重評嚴重度、砍 non-finding）。（2026-07-25 起的界線：帶 R1／R2 證據的詞彙 finding 屬正常 R 維度 finding、不算吹毛求疵；無證據的純同義詞美化才砍。）**多跑取聯集、優先採兩模型交集**（交集＝最低後悔）。

## 回報規格

四級，只報 tier 1–2、tier 3 至多一行、tier 4 略（專案 review 慣例，**不 over-report**；**乾淨的章節是有效結果**）：

1. 明確缺陷（blocking 易懂性，或 careful editor 會修的流暢性）→ 報；
2. 值得提的收緊（advisory）→ 報；
3. taste／voice drift → ≤1 行，低優先；
4. non-finding（見上節）→ 略。

**輸出格式：**

- 首行：`VERDICT: <B> blocking, <T> tighten, <O> optional, <V> voice`
- 逐條（一行一筆）：
  `- [Blocking|Tighten|Optional] [U#|F#|S#|A#|V#|R#] <sec>:<locus> — <issue>（原文：「…」）→ 建議：「…」或【刪】`
  - **S/A/V 條必附**：踩哪個測試（S1/S2/S3/A1/A2/V1）＋一行為什麼；S3 成立時建議用【刪】而非改寫。
  - **R 條必附**：踩哪個測試（R1/R2/R3）＋一行「為何對 EFL 讀者不透明」＋平實改寫（保語意、不動數學）；病根是缺解釋時改開 U 維度並標「補解釋優先」。
- 每個**乾淨**的維度各一行（如 `F2 贅字: clean`、`S/A/V: clean`、`R: clean`）。
- 末行：對「**易懂性＋S/A＋R 的 blocking 是否歸零**」給一句明確結論（prose gate 收斂判準）。

**交付給使用者裁決時**：**每道閘各產一份** standalone HTML 審核稿（MathJax CDN、雙擊即開、數學即渲染、頂部摘要表、逐條卡片含 `<del>`／`<ins>` diff）。正常流程：gate 1（Claude）審完交 `REVIEW-ch{NN}-prose-audit-gate1.html`，再換 gate 2（Codex）審完交 `REVIEW-ch{NN}-prose-audit-gate2.html`——**兩份各自獨立、不合併**（對應 Claude 先審、Codex 再審的兩步）。格式參照 [`REVIEW-ch01-prose-audit-gate1.html`](REVIEW-ch01-prose-audit-gate1.html)／[`REVIEW-ch01-prose-audit-gate2.html`](REVIEW-ch01-prose-audit-gate2.html)（版型最初源自 video 線 ch01 copyedit 審核稿；該練習產物已刪，樣式由前述兩份 gate HTML 承繼）。**不要**交塞滿生 LaTeX 的 `.md`（CLAUDE.md 規則）。純版控紀錄（如本 rubric、驗證報告）不在此限。每條 finding 標**穩定編號**（gate 1 用 `G1-1…`、gate 2 用 `G2-1…`），方便使用者逐條報編號討論與回覆裁決。

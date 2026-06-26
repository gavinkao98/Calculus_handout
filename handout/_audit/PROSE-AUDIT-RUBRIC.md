# 講義散文稽核 — 維度與擋稿線（PROSE-AUDIT-RUBRIC）

> 本檔是「散文稽核」兩道閘——**Claude subagent（gate 1）**與 **Codex 獨立（gate 2）**——共用的契約與**單一真相來源（single source of truth）**。兩道閘都讀本檔判斷；維度／擋稿線**只在這裡改一次**。
>
> 語域與結構的**權威規範**見 [`CONTENT_SPEC.md`](../../CONTENT_SPEC.md) §3（語域與語聲）、§15（最終一致性檢查）。本檔只定「審哪些維度、哪些擋稿、哪些不算 finding、怎麼回報」，**不重述** §3 的規範本身。

## 審查對象與邊界

- **審**：講義單節 fragment（`fragments/ch{NN}/sec-*.html`）裡的**英文說明散文**——`<p>` 等敘述／動機／解釋文字。
- **不審**：數學正確性、圖、example 選題、編號／排版——這些有各自的 audit（見 [`_dev-archive/general/PROMPT-audit-dimensions.md`](../_dev-archive/general/PROMPT-audit-dimensions.md)）。math 公式只當語境，**不評對錯**。

## 三個維度

### A. 易懂性 Comprehensibility（§3 結構規則；部分 BLOCKING）

讀者「跟不跟得上」。據 CONTENT_SPEC §3。

- **U1 動機缺位** — formal statement（definition／theorem／…）前面沒有動機散文說明「為何引入、直覺上是什麼」（§3：formal 前該有 1–2 段；純計算短節可只用一句承接句，為合法例外）。
- **U2 重型形式無 gloss** — 語法重的定義（巢狀量詞、ε-δ、符號密）沒有「*Informally, …*」白話重述（§3 規則）。形式已近英語、僅一兩個符號者**不需要** gloss，別反向挑剔。
  - **白話重述可在 inline gloss、或定義前後相鄰散文任一處。只有當附近完全找不到任何白話重述、讀者被卡在純符號上，才算 blocking。** inline 缺、但相鄰散文已充分解拆 → 至多 advisory（可建議補 inline gloss，但不擋稿）。
- **U3 未解釋的邏輯跳躍** — 自學讀者無法自行重建的一步，缺 *because*／*therefore*／*since* 等橋接（§3 明文禁止「未解釋的邏輯跳躍」）。
- **U4 術語／記號先用後定義** — 術語或 notation 在被引入前就使用，把讀者晾住（forward dependency）。
  - **blocking 限於「讀者被晾住、無法從使用處的散文重建其義」。** 若記號在使用處當場以散文 gloss、讀者可重建其義 → 降為 advisory（建議調整順序，但不擋稿）。
- **U5 定義後未拆解** — 重定義之後沒有散文解拆「這條件排除了什麼／該怎麼讀」（§3：definition 後的散文解拆）。

### B. 流暢性 Fluency（copyedit；全 ADVISORY）

「寫得順不順」。保留語意，只收緊。

- **F1 局部冗餘** — 一個詞／概念在 1–2 句內無新意地重述（命名後緊接重述的老毛病）。
- **F2 贅字** — filler／疊字（*the fact that*、*in order to*、*basically*、*actually*…），刪了零語意損失。
- **F3 句構可解析** — garden-path、子句堆疊、動詞前鋪陳過長、修飾語誤掛，讓人一眼解析不出。
- **F4 句長／認知負荷** — 一句塞太多概念，超出自學讀者一次能扛的量；給切點。
- **F5 語域** — hedge、過度口語（*super easy*、*you guys*）、黑板縮寫（*iff*、*w.r.t.*、*s.t.*）、代名詞策略（*we* 預設；*you* 僅用於溫和提醒或 forward reference）。

### C. 語意／聲音 Substance／Altitude／Voice（S/A/V 語意層 critic；部分 BLOCKING）

讀者「會不會覺得這是機器寫的」——但**不是數 tell／密度，是讀意思**。**中性 ≠ AI；中性＋空才是 AI**（[`PLAN-deai-semantic-critic.md`](../../PLAN-deai-semantic-critic.md) §0）。對每個候選句/段跑下面三組診斷，**每條 finding 強制附證據**。

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

**兩個防呆（避免重蹈 metric/tell 覆轍）：**
1. **真人範本當錨 ＋ 強制附證據** — gate 跑 S/A/V 時，**prompt 末尾掛 [`anchors/svc-exemplars.md`](anchors/svc-exemplars.md)（固定 2 正 1 負真人範本）**，標為「言之有物的真人數學散文」，**對著正面 bar 判、把負面當「該 flag 長這樣」**。每條 finding **必附**：問題句＋踩哪個測試（S1/S2/S3/A1/A2/V1）＋一行為什麼＋改寫（或「刪」）。→ 可稽核，不是憑感覺。
2. **中性不扣分** — 純粹平實、中性但言之有物的句子**不准 flag**（指 S/A：不因「中性」就判它空／錯高度——那正是目標）。只抓空（S）/錯高度（A）/該暖沒暖或可更暖（V1 寬報 advisory，見上）。

**擋稿線（從嚴、寧少報）：** BLOCKING = ① **空句佔位**——某句踩 S1（無新洞見）／S3（刪無損失）且**佔著承載教學功能的位置（動機／直覺／解拆）卻無實質**；或 ② **高度錯**——A2（真正難的一步被揮手帶過，讀者會卡）。其餘 S/A/V（單純 S2、A1 嘮叨、V1 平、非承載位的可刪 filler）一律 **ADVISORY**。
**收斂判準：** 該節 C 通過 = **S/A 的 blocking findings = 0**；advisory（含 V）不強制歸零。

唯讀、propose-only、**保語意、不動數學、不碰教學順序與選題**（copyedit 級硬護欄，同 A/B 維度）。Vale lint 的 flag 仍當零成本預標餵入（**降級護欄、預期 ~0**，非 gate）。

## 擋稿線（blocking vs advisory）

- **BLOCKING（讀者會卡住或被誤導）**：`U1` 嚴重（全無動機就丟形式）、`U2`、`U3`、`U4`；`F3` 中**會導致誤解、進而誤算**的真歧義句；以及 **C 維度的 S/A blocking**（空句佔承載位＝S1/S3＋無實質，或 `A2` 揮手帶過真難步）。
- **ADVISORY（polish；讀者仍懂）**：`F1`、`F2`、`F4`、`F5`、`U5`、輕微 `U1`（動機偏薄但有）、`F3` 一般彆扭；以及 C 維度的 `S2`／`A1`／`V1`／非承載位的可刪 filler。
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

## 回報規格

四級，只報 tier 1–2、tier 3 至多一行、tier 4 略（專案 review 慣例，**不 over-report**；**乾淨的章節是有效結果**）：

1. 明確缺陷（blocking 易懂性，或 careful editor 會修的流暢性）→ 報；
2. 值得提的收緊（advisory）→ 報；
3. taste／voice drift → ≤1 行，低優先；
4. non-finding（見上節）→ 略。

**輸出格式：**

- 首行：`VERDICT: <B> blocking, <T> tighten, <O> optional, <V> voice`
- 逐條（一行一筆）：
  `- [Blocking|Tighten|Optional] [U#|F#|S#|A#|V#] <sec>:<locus> — <issue>（原文：「…」）→ 建議：「…」或【刪】`
  - **S/A/V 條必附**：踩哪個測試（S1/S2/S3/A1/A2/V1）＋一行為什麼；S3 成立時建議用【刪】而非改寫。
- 每個**乾淨**的維度各一行（如 `F2 贅字: clean`、`S/A/V: clean`）。
- 末行：對「**易懂性＋S/A 的 blocking 是否歸零**」給一句明確結論（prose gate 收斂判準）。

**交付給使用者裁決時**：**每道閘各產一份** standalone HTML 審核稿（MathJax CDN、雙擊即開、數學即渲染、頂部摘要表、逐條卡片含 `<del>`／`<ins>` diff）。正常流程：gate 1（Claude）審完交 `REVIEW-ch{NN}-prose-audit-gate1.html`，再換 gate 2（Codex）審完交 `REVIEW-ch{NN}-prose-audit-gate2.html`——**兩份各自獨立、不合併**（對應 Claude 先審、Codex 再審的兩步）。格式參照 [`REVIEW-ch01-prose-audit-gate1.html`](REVIEW-ch01-prose-audit-gate1.html)／[`REVIEW-ch01-prose-audit-gate2.html`](REVIEW-ch01-prose-audit-gate2.html)（源自 [`../../video/content_scripts/_audit/REVIEW-ch01-narration-copyedit.html`](../../video/content_scripts/_audit/REVIEW-ch01-narration-copyedit.html)）。**不要**交塞滿生 LaTeX 的 `.md`（CLAUDE.md 規則）。純版控紀錄（如本 rubric、驗證報告）不在此限。每條 finding 標**穩定編號**（gate 1 用 `G1-1…`、gate 2 用 `G2-1…`），方便使用者逐條報編號討論與回覆裁決。

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

### C. 語聲 AI-texture（密度觸發；分兩階段上線）

讀者「會不會覺得這是機器寫的」。§3 語域權威不變，本維度只審 AI-tell 的**密度**，不審個別合法用法。**單一合法用法不算 finding；觸發擋稿的是密度。**

- **C1 空心 signposting / 連接詞超量** — signpost 開頭（It is worth/important to note、Recall that[無可回查]、In this section we will、Now let us turn our attention to）與「敘述顯而易見步驟」的連接詞（This means that、From this we can see、It follows naturally that）。§3 鼓勵的連接詞仍是特性，**但帶密度天花板**：同一節超過約每 500 字 3 個 distinct → C1。
- **C2 copula-avoidance** — 以 serves as / represents / marks / stands as 取代可用的 is/are。
- **C3 裝飾性 negative parallelism** — `not X but Y` / `not only…but also`，純為節奏、對比可隱含時。
- **C4 強迫性 rule-of-three** — 三形容詞／三子句堆疊為 cadence 而非真有三項。
- **C5 puffery / 借來的宏大** — powerful tool、elegant、profound、fundamental building block、rich tapestry，斷言而非由內容掙得；及無新意的 `In summary, we have seen…` 重述。
- **C6 em-dash 密度** — 散文中 em-dash 作插入語的頻率（§8 已要求謹慎）。**密度線（Ch1 校準）：advisory ≥4 個/~500 字**（在已簽核 Ch1 上界 ~4.0 之上，故基準不誤判）；**單句內 ≥3 個 em-dash 作插入語＝ advisory 局部熱點**（即使全節未超線）。em-dash 僅在與其他 C-tell 合計達高密度叢集時才貢獻 blocking。

**擋稿線（Ch1 校準定案，N=3）：** BLOCKING = 任一節 C1–C6 **高密度叢集**＝合計 **≥3 個 distinct 真 tell**（genuine；content-bearing／§3-protected 邊緣**不計入**密度）落在約 500 字內，**且**該節 distinct 真 tell 絕對數 **≥3**（短節絕對下限：免 <~400 字節以 1–2 項外插假觸發，例 sec-intro）。單一 tell＝ADVISORY。
**收斂判準補一條：** 該節 AI-texture 通過 = 高密度叢集（依上式）= 0。advisory（單一 tell）不強制歸零。

**不算 finding（§3-protected，但加密度天花板）：** §3 鼓勵連接詞、刻意教學重複、章末回查重述、Informally gloss、topic-term recurrence —— 仍是特性，**但任一者在單節內超過密度門檻即轉 C# finding**；舊版「絕不可當 finding」的無上限保護到此為止（這正是 AI scaffolding 過去被積極辯護而存活的漏洞）。密度門檻：signposting／連接詞比照 C1（distinct >3/~500 字），em-dash 比照 C6（≥4/~500 字）；其餘受保護特性（刻意教學重複／章末回查重述／Informally gloss／topic-term recurrence）僅在**貢獻高密度叢集**（上述擋稿線）時才轉 finding，無獨立 per-item 數（Ch1 校準：此四類在已簽核章節從未逼近任何門檻）。

唯讀、提議不行動，與 A/B 維度同護欄。Vale lint 的 flag 當預標餵入。

## 擋稿線（blocking vs advisory）

- **BLOCKING（讀者會卡住或被誤導）**：`U1` 嚴重（全無動機就丟形式）、`U2`、`U3`、`U4`；`F3` 中**會導致誤解、進而誤算**的真歧義句；以及 **C 維度的高密度叢集**（≥3 個 distinct 真 tell / ~500 字，含短節絕對下限）。
- **ADVISORY（polish；讀者仍懂）**：`F1`、`F2`、`F4`、`F5`、`U5`、輕微 `U1`（動機偏薄但有）、`F3` 一般彆扭。
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

- 首行：`VERDICT: <B> blocking, <T> tighten, <O> optional, <X> AI-texture`
- 逐條（一行一筆）：
  `- [Blocking|Tighten|Optional] [U#|F#|C#] <sec>:<locus> — <issue>（原文：「…」）→ 建議：「…」`
- 每個**乾淨**的維度各一行（如 `F2 贅字: clean`）。
- 末行：對「**易懂性 blocking 是否歸零**」給一句明確結論（prose gate 收斂判準）。

**交付給使用者裁決時**：**每道閘各產一份** standalone HTML 審核稿（MathJax CDN、雙擊即開、數學即渲染、頂部摘要表、逐條卡片含 `<del>`／`<ins>` diff）。正常流程：gate 1（Claude）審完交 `REVIEW-ch{NN}-prose-audit-gate1.html`，再換 gate 2（Codex）審完交 `REVIEW-ch{NN}-prose-audit-gate2.html`——**兩份各自獨立、不合併**（對應 Claude 先審、Codex 再審的兩步）。格式參照 [`REVIEW-ch01-prose-audit-gate1.html`](REVIEW-ch01-prose-audit-gate1.html)／[`REVIEW-ch01-prose-audit-gate2.html`](REVIEW-ch01-prose-audit-gate2.html)（源自 [`../../video/content_scripts/_audit/REVIEW-ch01-narration-copyedit.html`](../../video/content_scripts/_audit/REVIEW-ch01-narration-copyedit.html)）。**不要**交塞滿生 LaTeX 的 `.md`（CLAUDE.md 規則）。純版控紀錄（如本 rubric、驗證報告）不在此限。每條 finding 標**穩定編號**（gate 1 用 `G1-1…`、gate 2 用 `G2-1…`），方便使用者逐條報編號討論與回覆裁決。

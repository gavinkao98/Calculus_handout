> **Status: archived / completed（2026-07-07 歸檔）** — 本計畫已落地：Vale lane＝advisory 預標（`ENVIRONMENT.md` §⑤b）、語意/聲音 S·A·V critic＝`handout/_audit/PROSE-AUDIT-RUBRIC.md` Dimension C。本檔為歷史施工紀錄，勿當現行流程；內含相對路徑可能已過時。

# PLAN-deai-flavor — 去「AI 味」完整方案計畫書

> ⚠️ **偵測層已 SUPERSEDED（2026-06-26）。** 本檔的「Vale 清單＋Dimension C 數 tell／密度」偵測設計，因真人語料校準證明其在「數學教科書」這個窄語域天花板過低（真人 em-dash 跨度 10×、講義落在人類區間內），已由 [`PLAN-deai-semantic-critic.md`](PLAN-deai-semantic-critic.md)（語意/聲音 S/A/V critic）取代。本檔保留作**決策史**與**仍有效的部分**（三層架構框架、不用 AI-detector 鐵律、授權政策、§3 語域權威）。

> **這份文件是什麼：** 一份自足的、可交給「全新對話」執行的計畫書。目的是在這個雙語（中文團隊／英文輸出）的 Calculus 講義＋Manim 影片產線裡，系統性地降低成稿散文的「AI 味」（讀起來像 LLM 生成的紋理）。
>
> **怎麼用：** 新對話從本檔讀起，按 §5 的 Phase 0→4 逐階執行。每個 Phase 有「目標／步驟／驗收／需使用者 sign-off 的點」。**§6 列出所有要使用者拍板的細項——那些一律提案、不要自己定死。**
>
> **語言：** 本檔依專案慣例以繁體中文撰寫；LaTeX／程式碼、套件名、檔名、技術術語（Vale、Dimension C、Mode A/B、NFA、blocking／advisory 等）保留英文原樣。
>
> **完整診斷（含外部研究與可點擊來源）另見** [`REVIEW-ai-flavor-authoring-audit.html`](REVIEW-ai-flavor-authoring-audit.html)（雙擊即開）。本檔是「要做什麼、怎麼做」；那份 HTML 是「為什麼、證據在哪」。
>
> **本檔性質為純版控紀錄／計畫，** 依 [`CLAUDE.md`](CLAUDE.md) 交付規則不受「審核文件要產 HTML」限制，用 Markdown。

---

## 1. 背景與問題

### 1.1 核心理念（貫穿全案）

**去 AI 味不是新增一套風格，而是更忠實地執行你們既有的 [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §3。** AI 味是「飄離 §3 語域」的漂移，從來不是 §3 想要的東西。你們選定的方向不變：**Stewart／Rogawski 語域、自學高中生（升大學群體）讀得懂、clarity > compactness**。

兩個軸正交，全案都按此假設：

- **數學深度**：可調，per-section，靠 direction brief（`CONTENT_DIRECTION.md §2` 的 rigor／scaffolding 意圖）。難主題給更多鋪陳，不是更 terse。
- **散文可讀性**：恆為 clarity-first，**不**往「艱澀」調——把散文寫複雜只會增加 AI 味，且違反易懂性 gate。

### 1.2 問題診斷：AI 味從哪幾個環節進來（精簡版，全文見 HTML 報告）

| # | 入口 | 一句話 | 產線 |
|---|------|--------|------|
| E1 | Mode A 擴充 + 8 項放大稽核 | 「傾向更多擴充」把開場/收尾/直覺變必填槽位，正是生成 AI 鷹架的工作 | handout |
| E2 | prose gate（`PROSE-AUDIT-RUBRIC.md`） | 兩維度（U1–U5、F1–F5）都不抓 AI 紋理；唯一語域維 F5 是 advisory + 字表封閉 | handout |
| E3 | copyedit gate（`NARRATION-COPYEDIT-RUBRIC.md`） | C1–C5 只抓局部毛病；瀰漫式 cadence 歸 tier-3「至多一行」 | video |
| E4 | 鎖稿後凍結 ⚠ | 去味窗口只有鎖稿前一次；鎖稿後 NFA D2 把去味當違規 | 兩條線 |
| E5 | 具名歷史 +「不要自我審查」+ AI 備援例題 | marker 只稽核 source/math，不稽核 tone；puffery 直接出貨 | 兩條線 |
| E6 | 語聲錨點只有一段 130 字範文 | worked-solution（全書大宗）完全沒有語聲目標 | handout |

**關鍵弔詭：** `PROSE-AUDIT-RUBRIC.md` 的「不算 finding」保護清單，把 §3 鼓勵的連接詞（`Notice that`／`Let us now`）、刻意教學重述列為**絕不可砍、且無密度上限**——而這批正好是 AI 文最濃的 tell。等於 gate 不只沒抓，還主動替它辯護。本案的核心修法就是給這份保護清單**補上密度天花板**。

### 1.3 外部研究的兩條鐵律（約束全案設計）

1. **AI 味分四層 tell**：lexical（delve/crucial/underscore…）、syntactic（tricolon、`not just X, it's Y`、copula avoidance）、structural（signposting、`In summary` 總結重述、listicle）、statistical（low burstiness 句長均勻、low perplexity）。可靠的偵測是「詞彙/結構 checklist + 人審」。
2. **絕對不要用 AI detector 分數當 gate**：OpenAI 自家 classifier 26%/9% 已下架；對非母語寫作 61% 偽陽性（本團隊正中此風險區）；paraphrase 一下 DetectGPT 70%→4.6%。**自動 lint 只能 flag-only，永遠不當判官。**

---

## 2. 已拍板的決策（新對話請勿 re-litigate）

這些是使用者在 brainstorming 中明確拍板的，連同理由記錄於此，避免新對話重開：

1. **範圍＝完整方案一次到位**：gate（兩條線）+ 預防層（Output Style + voice corpus）+ 回填，全包；但切成 Phase 內部增量，可一階一階執行。
2. **Dimension C ＝密度觸發 blocking、兩階段上線**：第一階段全 advisory 校準門檻；門檻可信後把「高密度叢集」升 blocking。理由：跟易懂性 blocking 同層級才有牙齒，但密度門檻避免誤砍合法數學散文。
3. **回填政策（依產線實況重塑）**：
   - **video**：目前全為實驗性質，流程跑通後會**整批刪除重做**→ **零回填**，gate 只需在重建時就位（forward-only）。
   - **Ch1**：唯一定稿、且已過 prose audit → **當校準基準**，不是回填目標；除非掃出真熱點且使用者要動，否則不改。
   - **Ch2–Ch4**：大致做完、尚未定稿 → **搭使用者既定的定稿 Mode B 便車**，Dimension C 在那輪一起收，**不另開回填活動**。
4. **R3 lint 引擎＝Vale**（使用者同意裝此新依賴）：理由是 markup-aware（自動排除 `$...$`／LaTeX／code）、單一 Go binary、CI 友善、零 detector 風險。
5. **voice corpus 建法＝由 AI 從已簽核 Ch1 提候選、使用者審定**（四型別各 1–2 段，使用者裁定入選）。
6. **落地位置＝repo 根目錄單一跨產線檔**（本檔 `PLAN-deai-flavor.md`）；產出的 rubric/設定/Output Style 各歸其產線目錄。

**另一個架構決策（前序討論已定）：本案不做成 Skill。** 穩態 gate ＝ rubric 改一塊（你既有的 `handout-prose-audit` subagent + Codex gate-2 自動繼承，因 rubric 是單一真相來源、prompt 只引用不複述）＋ Vale 工具 ＋ Output Style ＋ 文檔編輯。**Workflow 只用在一次性的唯讀密度掃描**（Ch1 校準、Ch2–4 分流），跑完不留常駐物。理由：比照你們既有 gate 形態（subagent + rubric 文檔），不引入第二種 gate 範式（Karpathy 簡單優先 + 比照既有風格）。

---

## 3. 架構

### 3.1 三層（預防 → 決定性 lint → 人審 gate）

```
┌─ 預防層（Mode A／撰寫時）─────────────────────────────┐
│ voice corpus R5（正面標靶）                          │
│ Claude Code Output Style（inference-side 引導）        │
│ Mode A 8 項稽核 + 第 9 項「AI-texture sweep」（自查）    │
└───────────────────────────────────────────────────┘
                      ↓ 草稿
┌─ 決定性 lint（R3）─────────────────────────────────┐
│ Vale 引擎（markup-aware）+ rule-pack + reject.txt      │
│ 種子＝授權清單，curate 過數學詞；flag-only、不 auto-reject │
│ 接進 CONTENT_DIRECTION ⑤ 既有 linter lane             │
│ Mode A 自查跑、Mode B 預標跑——同一個                   │
└───────────────────────────────────────────────────┘
                      ↓ flag 當預標
┌─ 人審 gate（R1/R4）───────────────────────────────┐
│ handout：PROSE-AUDIT-RUBRIC 加 Dimension C（C1–C6）     │
│   密度觸發 blocking、兩階段；§3 保護清單加密度天花板        │
│ video：NARRATION-COPYEDIT 加 C6、移出 tier-3 上限         │
│ gate 1（Claude subagent）+ gate 2（Codex）共用 rubric    │
└───────────────────────────────────────────────────┘
```

**正交護欄：** 難度旋鈕（數學深度 + 鋪陳厚度，走 direction brief）與本案 gate 互不衝突——只要「難」＝數學更嚴謹、不是散文更囉嗦。本案不改難度旋鈕，僅在 §6 註記其交集（voice corpus 可含偏密/偏輕兩種範本，皆在 §3 語域內）。

---

## 4. 元件規格

### 4.1 Vale 設定 + rule-pack（R3 引擎）

- **安裝**：Vale（單一 Go binary，跨平台）。進 [`ENVIRONMENT.md`](ENVIRONMENT.md)、[`tools/doctor.py`](tools/doctor.py) 檢查項、必要時 `tools/setup.ps1`。pinned 版本記錄。
- **掃描對象**：只掃**散文**——handout 的 `<p>` 等敘述文字、video 的 `narration` 欄。**務必**設定排除 `$...$`／`\(...\)`／LaTeX 命令／`<code>`／程式碼，否則數學符號會淹沒訊號（Vale 的 markup-aware 排除正是選它的主因）。
- **機制**：`reject.txt`（自動接上 `Vale.Avoid` existence rule）放單詞/片語；多詞與結構 tell 寫成自訂 YAML rule。`accept.txt` 保護合法數學/領域術語。
- **嚴重度**：`Vale.Avoid` 預設 `error`——**降為 `warning`/`suggestion`**，因為本層恆為 advisory／flag-only，決定性「擋不擋」交給 Mode B 的人審維度 C。
- **接點**：接進 `CONTENT_DIRECTION.md ⑤` 既有的 deterministic-linter lane（該 lane 本來就 advisory、不擋收斂 → 零誤砍 blocking 風險）。

### 4.2 種子清單與 curation 政策

**只用有授權的來源當種子（其餘僅作靈感，不 vendor）：**

| 來源 | 授權 | 取什麼 |
|------|------|--------|
| [berenslab/llm-excess-vocab](https://github.com/berenslab/llm-excess-vocab)（Kobak et al., *Science Advances* 2025） | MIT | `results/excess_words.csv`（~900 字，實測詞頻躍升） |
| [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) | CC BY-SA（引用需標示） | 七類 tell taxonomy + banned-phrase 清單 + 「先佐證再 flag、絕不靠 detector 機率」方法論 |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | MIT | phrase/structure 清單 + 五維評分（Directness/Rhythm/Trust/Authenticity/Density）→ 人審維度 |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | MIT | 109 條 3-tier 詞表（Tier 1 always-flag / Tier 2 cluster / Tier 3 density）；其零依賴 JS 偵測引擎可作參考 |
| [matteoroversi/anti-ai-rhetoric](https://github.com/matteoroversi/anti-ai-rhetoric) | （查授權） | 結構型 tell taxonomy（對稱鷹架）→ 人審維度 |

**curation 政策（保守起步、對數學詞特別小心）：**
- **剔除合法 calculus 詞**：`leverage`、`robust`、`comprehensive`、`integral`、`intrinsic`、`examine`、`demonstrate` 等在數學語境是真詞，放進 `accept.txt`。
- **密度啟發式**：同一段 ≥3 個 distinct trigger / ~500 字才視為高密度叢集，單次合法使用不觸發。
- **US 拼寫正規化**（若種子含英式拼寫）。
- **起步從嚴選詞、寧缺勿濫**：先求低誤砍率（高 signal），再逐步加詞。

**banned-starter 種子（可直接貼入 `reject.txt`／rule，執行時再 curate）：**

```
It is worth noting that
It is important to note that
It is important to remember
In this section, we will explore / examine
Now, let us turn our attention to
Let's dive into / Let's explore
This means that          # 僅當敘述顯而易見步驟
From this, we can see that
It follows naturally that
As we can clearly see
In summary / In conclusion / Ultimately / At its core   # 無新意重述
not just X, it's Y / not X, but Y
not only X but also Y
serves as a / stands as a / represents / marks / acts as  # copula 迴避
plays a crucial / pivotal / vital role in
stands as a testament to
a powerful (and elegant) tool
the fundamental building block of
rich tapestry / ever-evolving landscape / in the realm of
delve into
underscore / underscoring the importance of
highlighting / emphasizing / further enhancing            # -ing 意義尾巴
Moreover / Furthermore / Additionally                     # 超人類頻率連接膠
powerful, elegant, and profound                           # 裝飾性三段形容詞
```
（video 另含 `Here's the idea`／`Notice that`／`Watch what happens`——僅當**作為每單元口頭禪重複**時，非首次使用。）

### 4.3 Dimension C（人審 gate 主體，可直接貼入 `PROSE-AUDIT-RUBRIC.md`）

> 加在現有「A. 易懂性」「B. 流暢性」之後，作為第三維度。VERDICT 行增列 `<X> AI-texture`。§3 仍是語域權威；本維度只審 AI-tell 的**密度**，不審個別合法用法。**單一合法用法不算 finding；觸發擋稿的是密度。**

- **C1 空心 signposting / 連接詞超量** — signpost 開頭（It is worth/important to note、Recall that[無可回查]、In this section we will、Now let us turn our attention to）與「敘述顯而易見步驟」的連接詞（This means that、From this we can see、It follows naturally that）。§3 鼓勵的連接詞仍是特性，**但帶密度天花板**：同一節超過約每 500 字 3 個 distinct → C1。
- **C2 copula-avoidance** — 以 serves as / represents / marks / stands as 取代可用的 is/are。
- **C3 裝飾性 negative parallelism** — `not X but Y` / `not only…but also`，純為節奏、對比可隱含時。
- **C4 強迫性 rule-of-three** — 三形容詞／三子句堆疊為 cadence 而非真有三項。
- **C5 puffery / 借來的宏大** — powerful tool、elegant、profound、fundamental building block、rich tapestry，斷言而非由內容掙得；及無新意的 `In summary, we have seen…` 重述（與 §3 章末回查重述的差別：回查重述有 lookup 價值且不堆 puffery）。
- **C6 em-dash 密度** — 散文中 em-dash 作插入語的頻率（§8 已要求謹慎；此處給密度線）。

**擋稿線（接到現有「擋稿線」一節）：** BLOCKING = 任一節 C1–C6 合計 ≥3 個 distinct AI-tell 落在約 500 字內。單一 tell = ADVISORY。收斂判準補一條：該節 AI-texture 通過 = 高密度叢集 = 0。**（兩階段：第一階段此線只報不擋；門檻校準後才啟用 blocking——見 §5 Phase 1/2。）**

**不算 finding（§3-protected，但加密度天花板）：** §3 鼓勵連接詞、刻意教學重複、章末回查重述、Informally gloss、topic-term recurrence —— 仍是特性，**但任一者在單節內超過上述密度即轉 C# finding**；舊版「絕不可當 finding」的無上限保護到此為止（這正是 AI scaffolding 過去被積極辯護而存活的漏洞）。

唯讀、提議不行動，與 A/B 維度同護欄。gate 1（Claude）與 gate 2（Codex）共用本維度。

### 4.4 video：C6 AI-cadence + 移出 tier-3 上限（`NARRATION-COPYEDIT-RUBRIC.md`）

- 加 **C6 — AI-cadence**：跨單元 pattern tell（每單元重複的公式化引導語、句長均勻、裝飾性 `not X but Y`、triadic cadence）——這些是 local C1–C5 漏掉的瀰漫性質。
- **把 voice/cadence 從 tier-3「至多一行」上限移出**，全文報告、逐筆裁決。理由（E4）：copyedit 是**鎖稿前唯一**能去味的窗口，鎖稿後 NFA D2 會把去味當違規。
- 同步把 `CONTENT_METHODOLOGY.md §4` 的軟註「別變口頭禪」改成**具體頻率預算**（某引導語至多每 N 個單元出現一次）。

### 4.5 Output Style（預防層，inference-side）

- 位置：`.claude/output-styles/<name>.md`（專案級）。
- **務必** `keep-coding-instructions: true`，否則 build／Manim 工程行為會掉。
- 內容：house voice 摘要 + 「避免這些 AI-tell」區塊（與 4.2 同一份 banned-list）+ 指向 voice corpus。
- 定位：**只是 Claude Code 內草擬時的預防**，非決定性、Claude-Code-only——不取代 lint 或人審。

### 4.6 voice corpus R5（正面標靶）

- 從**已簽核 Ch1** 提候選，按四型別各 1–2 段：①動機鋪陳、②**worked solution（目前完全缺、優先補）**、③歷史/應用旁註、④直覺 gloss。
- 由 AI 提候選＋理由，**使用者審定入選**（決策 5）。
- 落點：擴充 `CONTENT_SPEC.md §3` 的「語聲參考範文」。標註每段的 burstiness 與具體性特徵。
- 用途：Mode A 草擬錨點、Dimension C 比對目標、`CONTENT_SOURCING` 改寫例題的語聲目標。

### 4.7 Mode A 第 9 項「AI-texture sweep」

- 加進 `README.md` Mode A（及 Mode C）的 8 項放大稽核，成為第 9 項，複用既有「補上或記錄」機制：「對每個 expansion marker 的散文跑 4.2 banned-list 與密度檢查；補上（改寫/砍）**或**記錄為刻意保留」。

---

## 5. 執行 Phase（逐階：目標／步驟／驗收／sign-off）

> 原則：每階先**量、再改**；所有自動 flag 一律 advisory，決定性「擋不擋」只在 Mode B 人審。

### Phase 0 — Scaffolding（裝 Vale + 組裝種子清單）
- **目標**：引擎與種子就位，尚不接任何 gate。
- **步驟**：①裝 Vale，更新 `ENVIRONMENT.md`／`doctor.py`／`setup`。②組裝種子清單（4.2 來源），curate 掉數學詞，建初版 `reject.txt`＋`accept.txt`＋少量結構 YAML rule。③設定散文 scope（排除 LaTeX/code）。
- **驗收**：`python tools/doctor.py` 認得 Vale；Vale 能對一個 `.html` fragment 跑出 flag 且**不**誤觸 `$...$` 內的符號。
- **需 sign-off**：種子清單最終組成、`accept.txt` 的數學詞白名單。

### Phase 1 — handout lint + Dimension C（advisory）+ Ch1 校準
- **目標**：跑通整套、定門檻，全程 advisory。
- **步驟**：①把 Dimension C（4.3）貼進 `PROSE-AUDIT-RUBRIC.md`，**blocking 線先停用、只報**。②對 **Ch1（基準）**唯讀跑 Vale + 跑一次 `handout-prose-audit`（含 C 維度）。③統計密度分布，**定出「高密度叢集」門檻**（讓 Ch1 這種已簽核好散文落在門檻之下）。④量誤砍率。
- **驗收**：Ch1 的誤砍率低到可接受（具體數字由本階段產生並記錄）；門檻有資料支撐、非憑感覺。
- **需 sign-off**：門檻起始值、C1–C6 逐條措辭、是否對 Ch1 任何掃出的真熱點做選擇性小修。

### Phase 2 — 升 blocking + §3 密度天花板 + 預防層 + corpus
- **目標**：gate 長出牙齒、預防層上線。
- **步驟**：①把 Dimension C 的高密度叢集**升為 blocking**，收斂判準補上 AI-texture 軸。②給 `PROSE-AUDIT-RUBRIC.md`「不算 finding」清單**加密度天花板**（4.3 末段）。③加 Mode A 第 9 項（4.7）。④建 Output Style（4.5）。⑤建 voice corpus（4.6，提候選→使用者審定）。
- **驗收**：對 Ch1 重跑，blocking 數合理（不暴衝）；Output Style 套用後 build/Manim 行為不變（`keep-coding-instructions: true` 生效）。
- **需 sign-off**：voice corpus 入選段落、Output Style 內容、Mode A 第 9 項措辭、§3 密度天花板的 N 值。

### Phase 3 — 套進 Ch2–Ch4 定稿
- **目標**：存量 handout 在既定定稿流程裡一起收 AI 味，**不另開回填活動**。
- **步驟**：當使用者為 Ch2/Ch3/Ch4 跑定稿 Mode B 時，該輪自動含 Dimension C（lint flag 當預標）。逐條 propose-only，使用者裁決；改完依既定規則（2026-06-12）跑回歸審核。
- **驗收**：每章定稿時 AI-texture 高密度叢集歸零（或經使用者明確裁決保留）。
- **需 sign-off**：逐章逐條的 Rewrite 裁決（本就是 Mode B 常態）。

### Phase 4 — video gate 元件（forward-only）
- **目標**：video 重建時 gate 即就位；**不碰現有實驗素材**。
- **步驟**：①把 C6 加進 `NARRATION-COPYEDIT-RUBRIC.md`、移出 tier-3 上限。②`§4` 引導語改頻率預算。③備一份對 `content_scripts/<deck>.md` 的 narration scope Vale 設定。
- **驗收**：規格文件就緒；待 video 正式重建時於 copyedit（鎖稿前）窗口套用。
- **需 sign-off**：C6 措辭、引導語頻率預算的 N 值。

---

## 6. 執行時需使用者拍板的細項（清單）

新對話遇到這些**一律提案＋推薦值，交使用者定，不要自己定死**：

1. 種子清單最終組成 + `accept.txt` 數學詞白名單（Phase 0）。
2. 「高密度叢集」門檻起始值（Phase 1，由 Ch1 校準資料支撐）。
3. C1–C6 逐條措辭定稿（Phase 1）。
4. §3「不算 finding」清單各項的密度天花板 N 值（Phase 2）。
5. voice corpus 四型別的入選段落（Phase 2，從 Ch1 提候選）。
6. Output Style 內容（Phase 2）。
7. Mode A 第 9 項措辭（Phase 2）。
8. video C6 措辭、引導語頻率預算 N 值（Phase 4）。

---

## 7. 護欄與「不做什麼」（YAGNI / 避免）

- **永不**用 AI detector 機率分數當 gate（GPTZero/CatchGPT 類）——硬約束。
- 自動 lint **永不** auto-reject；只 flag、advisory。決定性「擋」只在 Mode B 人審維度 C。
- **不**做成 Skill；走 rubric + subagent + Vale 工具（決策見 §2）。
- **不**碰數學/數值/區間/例題選題/教學順序——去味是 copyedit 級、保留語意（同 F/C 維度硬護欄）。
- **不**回填 video（全將重做）；**不**另開獨立 handout 回填活動（Ch2–4 搭定稿便車）。
- 種子清單**必對數學詞 curate**；無授權清單（如 rossmann、FareedKhan）**不 vendor**，只作靈感。
- 不把散文往「艱澀」調——那違反 §3 且增加 AI 味；真正的「難」走數學深度（direction brief），不在本案範圍。

---

## 8. 參考與既有檔案錨點

**要編輯/新增的檔：**
- [`handout/_audit/PROSE-AUDIT-RUBRIC.md`](handout/_audit/PROSE-AUDIT-RUBRIC.md) — 加 Dimension C（4.3）
- [`video/content_scripts/_audit/NARRATION-COPYEDIT-RUBRIC.md`](video/content_scripts/_audit/NARRATION-COPYEDIT-RUBRIC.md) — 加 C6、移 tier-3（4.4）
- [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §3 — 擴 voice corpus（4.6）
- [`CONTENT_DIRECTION.md`](CONTENT_DIRECTION.md) ⑤ — 接 Vale lint lane（4.1）
- [`README.md`](README.md) Mode A — 加第 9 項（4.7）
- [`video/CONTENT_METHODOLOGY.md`](video/CONTENT_METHODOLOGY.md) §4 — 引導語頻率預算（4.4）
- [`ENVIRONMENT.md`](ENVIRONMENT.md)／[`tools/doctor.py`](tools/doctor.py) — 登記 Vale（4.1, Phase 0）
- 新增：`.claude/output-styles/<name>.md`（4.5）、Vale 設定檔（`.vale.ini` + styles + `reject.txt`/`accept.txt`）

**驗證過的工具/資料來源（含授權）：** 見 §4.2 表。完整外部研究與來源連結見 [`REVIEW-ai-flavor-authoring-audit.html`](REVIEW-ai-flavor-authoring-audit.html)。

**官方生態現況：** Anthropic 官方無「去 AI 味」skill；社群有（stop-slop、avoid-ai-writing 等）但全為 LLM prompt（非決定性、多為 rewriter），只當種子內容來源，不當 gate。Claude Code Output Styles 是官方功能，作預防層用。

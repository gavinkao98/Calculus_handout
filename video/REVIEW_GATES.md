# video 產線審核閘一覽（review gates map）

> **本檔是地圖／索引，不是權威。** 每道閘的權威定義仍在它的「home doc」（見各列「權威文檔」欄）；
> 這裡只把散落在 [README.md](README.md)、[DESIGN.md](DESIGN.md)、[CONTENT_METHODOLOGY.md](CONTENT_METHODOLOGY.md)、
> [RUNBOOK-mimo-narration-route.md](RUNBOOK-mimo-narration-route.md)、[REBUILD_STATUS.md](REBUILD_STATUS.md) 與
> 根目錄 [`../CLAUDE.md`](../CLAUDE.md)／[`../README.md`](../README.md) 的審核機制收斂成一張表，方便一眼看全貌。
> 整理日期：2026-06-15。內容若與 home doc 牴觸，以 home doc 為準，並回頭修本檔。

## 總綱

產線分**七個產物層**，每層各有審核閘。能真正**擋住 render** 的只有 storyboard/timing 與兩軌 parity 的幾個**自動腳本閘**；
內容／旁白／視覺層全為 **advisory**——模型（Codex / MiMo / Claude）或人提案，最後由人裁決，**稽核者一律唯讀、不自己改檔**。
**2026-09-13 補**：層 7 另有一道確定性硬閘 `rewatch_pack --gate-still`（POST-render），它擋的不是 render，而是**該輪的完成**（見 §六）。

流向：講義散文 →（Stage-1）內容稿 → 旁白稿 → 口語版 → manim hook code → storyboard/timing → render 成品。（「Mode」一詞專留講義 A/B/C；影片內容稿階段稱 **Stage-1**——見 [REVIEW_MODEL_DECISIONS.md](REVIEW_MODEL_DECISIONS.md) 詞彙紀律。）

**Phase 索引**（同一條線的四段粗分，方便對話指稱；不是新狀態機）：

| Phase | 涵蓋層 | 主要閘 |
|---|---|---|
| Content | 層 2–3 | six-lens、copyedit、旁白 sign-off（lock） |
| Derivation | 層 4 | derive parity、NFA |
| Storyboard | 層 5–6 | 工程鏡、schema/lint/sizecheck、pedagogy/OTF/SC、amplification |
| Render | 層 7 | 視覺 gate1/gate2、人工驗收 |

圖例：**■ 自動腳本・可擋 render**　**□ LLM 稽核・advisory**　**◆ 人工閘**　**◷ 未建（TODO）**

> **gate 1 具名 subagent（2026-06-17；2026-06-30 補 pedagogy）：** 五道判斷閘的 gate1 已可用 `.claude/agents/` 具名 subagent 跑（唯讀 `Read/Grep/Glob`、薄提示引用各 SSOT rubric，比照講義 `handout-prose-audit`）：[`narration-faithfulness-audit`](../.claude/agents/narration-faithfulness-audit.md)（NFA）、[`narration-copyedit`](../.claude/agents/narration-copyedit.md)、[`visual-frame-audit`](../.claude/agents/visual-frame-audit.md)、[`hook-engineering-audit`](../.claude/agents/hook-engineering-audit.md)、[`pedagogy-firstlearner-audit`](../.claude/agents/pedagogy-firstlearner-audit.md)（讀 storyboard＋cited `.md`＋handout，PRE-render；與讀 render 後幀的 `visual-frame-audit` 同 gate1 tier、不同 stage）。**另有 [`video-amplification-audit`](../.claude/agents/video-amplification-audit.md)（敘述放大機會稽核、propose-not-act、永不 blocking；2026-07-01）。** 六鏡維持 multi-agent Workflow；gate2（Codex／外部 VLM）是外部模型、**不是** subagent（仍走 `codex exec`／`critic.py --confirm`，thin-prompt 模板 `PROMPT-narration-*.template.md` 留給 Codex gate2）。

---

## 一、各產物層的審核閘

### 層 2｜Stage-1 內容稿（`content_scripts/<deck>.md`）

| 閘 | 執行者 | 性質 | 把關內容 | 權威文檔 |
|---|---|---|---|---|
| 六-lens 對抗式稽核 | multi-agent workflow ＋ Claude 逐條複驗（refute-by-default；**無 Codex gate2**） | □（收斂＝**blocking==0**） | 六維 L1–L6：忠實／拆解／語域／不重複／**數學正確（獨立重算每個例題、隔離盲算）**／完整；每條過四級分級，回報 raw→actionable、查過度 triage 與幻覺（0-hallucination 為目標） | **SSOT [CONTENT-SIXLENS-RUBRIC.md](content_scripts/_audit/CONTENT-SIXLENS-RUBRIC.md)**；方法論 [CONTENT_METHODOLOGY.md](CONTENT_METHODOLOGY.md) |
| §7 作者 checklist ＋ faithful-to-handout | 作者自查（12 項） | ◆（定稿前 blocking） | 覆蓋每種 def／thm／example、無習題外洩、intro/outro、幾何宣稱要有視覺單元、旁白 3–7 句；每個數學單元 **MUST** 經 `source` 欄回溯到講義環境，違反則 stage-2 前出局 | [CONTENT_METHODOLOGY.md](CONTENT_METHODOLOGY.md) §7、L34 |

### 層 3｜旁白稿（`narration`）

| 閘 | 執行者 | 性質 | 把關內容 | 權威文檔 |
|---|---|---|---|---|
| 散文潤稿 copyedit pass（lock 前） | gate1 Claude subagent（免費）→ gate2 Codex（計費、近定稿時單次、需同意） | □（`Tighten`／`Optional`；**blocking 結構上恆 0**、逐筆人裁） | C1–C5 贅字／冗餘／朗讀流暢／句長／跨單元回音。**硬護欄：語義不得改**（不增刪步驟、不動任何數值／區間）。是 lock **前**唯一能改冗餘的地方 | **SSOT [NARRATION-COPYEDIT-RUBRIC.md](content_scripts/_audit/NARRATION-COPYEDIT-RUBRIC.md)**；thin prompt [PROMPT-narration-copyedit.template.md](content_scripts/_audit/PROMPT-narration-copyedit.template.md)；方法論 [CONTENT_METHODOLOGY.md](CONTENT_METHODOLOGY.md) |
| 旁白 sign-off ＋ readable HTML | 人工（使用者讀 `<deck>_narration.html` 拍板） | ◆（鎖稿 blocking） | 核可才能 lock／derive／TTS；`CONTENT_APPROVED` 決定 NFA 的 D7 是否必跑（=no 時開隔離重算 reader）。**2026-06-14 放寬**：可先用乾淨草稿建 storyboard＋無聲影片，邊看邊一起審旁白（故 storyboard 現在可早於核可） | [CONTENT_METHODOLOGY.md](CONTENT_METHODOLOGY.md)；HTML 交付物規則見 [`../CLAUDE.md`](../CLAUDE.md) |

### 層 4｜口語版（`content_scripts/<deck>.spoken.yml`）

| 閘 | 執行者 | 性質 | 把關內容 | 權威文檔 |
|---|---|---|---|---|
| `derive_spoken.py --check` | 確定性腳本（離線、免費） | ■（擋，exit 1） | 兩軌 parity：每個 canonical say 對齊（無漏／多 id）、`{show}` 標記逐一一致、無 `$`／LaTeX 漏進口語。每次改 `spoken.yml` 後重跑 | [README.md](README.md) §MiMo 路線、[DESIGN.md](DESIGN.md)；步驟見 [RUNBOOK-mimo-narration-route.md](RUNBOOK-mimo-narration-route.md) step 2 |
| NFA 旁白忠實稽核（lock 後；原 Mode B） | gate1 Claude subagent（免費、迭代到 blocking==0；reader 拆法見 rubric）→ gate2 Codex（計費、收斂後單次、需同意；ch01 記錄 gpt-5.5 reasoning xhigh） | □（每條標 [Blocking｜Advisory]；收斂＝**blocking==0**） | 七維 D1–D7：D1 HTML 逐字忠實、D2 口語逐字等同（只把數學符號念成字）、D3 數學唸法（`f^{-1}` 須念「f inverse」）、D7 數學正確（`CONTENT_APPROVED=no` 時必跑、獨立重算、開隔離盲 reader）。**不得改已核可 source**；裁決寫進修正 commit body（`git log --grep="NFA"`） | **SSOT [NARRATION-FAITHFULNESS-RUBRIC.md](content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md)**；thin prompt [PROMPT-narration-faithfulness.template.md](content_scripts/_audit/PROMPT-narration-faithfulness.template.md)；commit 慣例 [`../CLAUDE.md`](../CLAUDE.md) |

### 層 5｜manim hook code（生成動畫程式）

| 閘 | 執行者 | 性質 | 把關內容 | 權威文檔 |
|---|---|---|---|---|
| 工程鏡（生成 hook code 稽核） | gate1 Claude subagent（免費、讀 `review_pack.py` 組的 engineering packet）→ gate2 Codex（計費、收斂後單次、需同意） | □（收斂＝**engineering blocking==0**） | **單鏡頭**：只看生成 hook code 的數學保真（E1，blocking）與慣例（E2；theme primitive 不用 hex、實心／空心點語義、SAFE_MARGIN），**不看美學**（歸 VISUAL-FRAME）。與 VISUAL-FRAME **V8 邊界**配對：V8 查幀上可見數學、本鏡查生成它的 code。**2026-06-16**：DeepSeek 退場、改兩讀者；忠實／語域／拆解三鏡已歸 CONTENT-SIXLENS；math context 改吃內容稿動畫單元 narration／`source`（脫離已搬 `legacy/` 的 `.tex`） | **SSOT [HOOK-ENGINEERING-RUBRIC.md](content_scripts/_audit/HOOK-ENGINEERING-RUBRIC.md)**；assembler [pipeline/review_pack.py](pipeline/review_pack.py) |

### 層 6｜storyboard／timing

| 閘 | 執行者 | 性質 | 把關內容 | 權威文檔 |
|---|---|---|---|---|
| `lint.py` | 腳本，make.py render 前跑（`--skip-lint` 可繞） | ■ error／warn | error（abort）：純文字欄出現 `$`／反斜線、`$` 不成對；warn：手動 `\\`、空心點用在已達值 | [DESIGN.md](DESIGN.md)、[README.md](README.md) |
| `sizecheck.py` | 腳本，與 lint 並行（`--skip-sizecheck` 可繞） | ■ error／warn | error（abort）：同層 prose 字級不一、元素出框；warn：教學散文用 muted 色、超安全邊界、內容塊重疊。**盲點**：只查 `brand.prose`，不查直接構造的 `MathTex/Text` | [DESIGN.md](DESIGN.md) |
| `sizecheck.py` fontfloor 最小字級 floor | 腳本，與 sizecheck 同跑（make.py-time、確定性） | ■ warn（warn-default；`meta.fontfloor_enforce` 開才 error／abort，預設關、landing 不擋） | 浮現「真實上螢幕字級 < `MIN_FONT_FLOOR`＝26px」的 `_brand_prose` 節點（render 前的工程對應物）；配 render 期 clamp（把縮過頭的節點托回 floor）＋ agent 在幀上肉眼施作的**手機寬尺標**（P6，~360–414px 視窗仍要讀得到）。與 VISUAL-FRAME V4／A6 配對：floor 浮現「小到讀不到」、V4 升 blocking／A6 扣分 | [pipeline/visuals/theme.py](pipeline/visuals/theme.py)（`MIN_FONT_FLOOR`，SPEC §8）／[pipeline/sizecheck.py](pipeline/sizecheck.py)（floor check）／[pipeline/brand.py](pipeline/brand.py)；rubric [VISUAL-FRAME-RUBRIC.md](content_scripts/_audit/VISUAL-FRAME-RUBRIC.md) V4／A6 |
| `schema.py` | 腳本，make.py render 前跑（`--skip-schema` 可繞） | ■ error／warn | **已建（2026-06-16）**：結構驗證（meta.id／section 必填、scene kind∈intro/content/divider/outro、id 唯一、content 需 template＋say、`{show}` 不閉合→error）＋列舉每場 `{show}` reveal 目標（`--list`）。**不**驗 target 是否存在於模板 payload（需 `reveal_targets()`／manim，屬 task #6）。**2026-06-30 增掛（2026-07-01 加 SC）**：OTF provenance／pedagogy ＋ **SC step-coverage** 結構 warn-checks 在此並跑（warn-default，`meta.otf_enforce`／`meta.pedagogy_enforce`／`meta.coverage_enforce` 開才 abort、預設關），即下方 `pedagogy-firstlearner-audit` 判斷閘的確定性底材。**2026-09-12 增掛 `source_rev`**（LOCKED 內容稿標頭的講義源 stamp vs 現檔；**永遠 warn-only**，WARN＝走 CONTENT_METHODOLOGY §8；`make.py`／`derive_spoken.py` 同掛）；`doc:` 錨池改為凍結 legacy standalone ∪ `.tex` label key（`doc:sec:`／`thm:`／`fig:`…）；`<deck>_mimo` 的 md／SC／source_rev 查找統一走 `provenance.content_script_for`。**2026-09-12 增掛 `example_coverage`（EX 層，例題折疊宣告閘）**：講義該節的 worked example（`\begin{envexample}{…}{ex:…}{}`，按 `\sechead` 區間歸節——**`ex:` 是章序不是節序**）比對內容稿單元的 `examples:`／`folds:` 宣告；EX1＝既沒教也沒折（`meta.example_coverage_enforce` 開才 error）、EX2＝宣告不成立（恆 warn）。**只接在此、不接 `make.py`**（同 SC：例題選材是撰稿期決定，不擋 render）；deck 無 `.md` 整個跳過。**閘只查宣告存不存在，不判折疊對不對**——語意歸下方 `pedagogy-firstlearner-audit` 的 `EX-adv` 與 REWATCH R5。deck 級 smoke＝`python tools/doctor.py --smoke`、模組級＝`python video/pipeline/run_selftests.py` | [DESIGN.md](DESIGN.md)、[README.md](README.md)；source [pipeline/schema.py](pipeline/schema.py)（provenance／pedagogy／coverage／example_coverage 落地 [pipeline/provenance.py](pipeline/provenance.py)／[pipeline/pedagogy.py](pipeline/pedagogy.py)／[pipeline/step_coverage.py](pipeline/step_coverage.py)／[pipeline/example_coverage.py](pipeline/example_coverage.py)） |
| `pedagogy-firstlearner-audit`（初學者教學＋上畫面文字忠實） | gate1 Claude subagent（免費；讀 storyboard＋cited `.md`＋handout，**PRE-render**；同 `visual-frame-audit` 的免費 gate1 tier、但不同 stage——它讀 render 後幀，本閘讀 storyboard 源） | □（PD／OF／SC blocking 分開計數；warn-default、per-deck opt-in，landing 不擋） | PD1–PD4 教學品質（beat 粒度、`scaffold.motive` 動機、divider `scaffold.problem`、前提首用 `scaffold.flag`）＋ OF1–OF2 上畫面文字 vs 核准源忠實／可回溯 ＋ **SC1–SC2／SC-honesty／SC-adv 推導步驟覆蓋**（storyboard `covers:` vs `.md screen_contract`：漏步驟／缺 recap／覆蓋誠實；可合併不可掉）；確定性底材＝上列 `schema.py` 並跑的 provenance／pedagogy／**coverage** warn-checks（gate-1 自有 blocking＝PD1＋OF1＋**SC-honesty**，其餘結構存在性由確定性層算、本閘 surface＋給脈絡） | **SSOT [PEDAGOGY-FIRSTLEARNER-RUBRIC.md](content_scripts/_audit/PEDAGOGY-FIRSTLEARNER-RUBRIC.md)**；agent [`../.claude/agents/pedagogy-firstlearner-audit.md`](../.claude/agents/pedagogy-firstlearner-audit.md) |
| **REWATCH 看片多鏡評審**（成片品質；2026-09-12 首用、**2026-09-13 起＝里程碑審**） | POST-render：`pipeline/rewatch_pack.py` 把成片翻成 pack（逐場 contact sheet＋時間軸＋靜止統計）→ 五鏡獨立盲審（R1 初學者×2／R2 動畫導演／R3 教學設計／R4 節奏剪輯／R5 講師；跨 Gemini／Claude 家族：agy ×3＋subagent ×3）→ orchestrator refute-by-default 合成 | □（advisory；**永不 blocking**；餵重做水位裁決） | 唯一「看過影片本身」的審：時間、停留、畫面是否隨數學演化、跟不跟得上；不重審忠實／數學（歸 NFA／L5／OF）。首用＝§3.1 成片（`REVIEW-ch03_s31-rewatch-multilens.html`）。**2026-09-13 起 finding 可標畫面語法規則代號 `rule: ML1`–`ML5`（R2 MUST；[SPEC-motion-language.md](SPEC-motion-language.md)），digest `by_rule` 按規則計數**。**頻率＝里程碑審（2026-09-13 裁決）：一節收斂時跑一次完整六鏡；輪內不跑，改用上一輪 finding 的回歸清單（見 §六 6.2）** | **SSOT [REWATCH-REVIEW-RUBRIC.md](content_scripts/_audit/REWATCH-REVIEW-RUBRIC.md)**；template [PROMPT-rewatch.template.md](content_scripts/_audit/PROMPT-rewatch.template.md)；schema `rewatch-findings.schema.json`；agy 呼叫紀律見根 CLAUDE.md |
| `video-amplification-audit`（敘述放大機會稽核；expansion 層 M2） | gate1 Claude subagent（免費；讀 storyboard＋cited `.md`＋handout `expansion:*`，**PRE-render**、propose-not-act） | □（AMP1 advisory；**永不 blocking**、只提候選、逐筆人裁） | 掃 handout `expansion:intuition`／`application` 判影片四態（screened／narration-only／visual-only／missing），只提 `missing` 的承重直覺（綁 `doc:` ＋標記短引文）；correctness caution 路由假設機制、example 歸 `example-supplement`。講義線 `mode-c-gapwalk` 的影片側對應，產 standalone HTML 裁決稿 | **SSOT [AMPLIFICATION-RUBRIC.md](content_scripts/_audit/AMPLIFICATION-RUBRIC.md)**；agent [`../.claude/agents/video-amplification-audit.md`](../.claude/agents/video-amplification-audit.md) |
| make.py manifest-freshness（`--reuse-audio`） | 腳本 | ■（fail-fast） | 比對 manifest 與 `<deck>_mimo.yml`（deck id／scene／beat 數／`{show}`／text_hash／WAV 存在與時長），防複用過期音檔；非 reuse 跑時拒絕用 mock 覆蓋真 manifest | [DESIGN.md](DESIGN.md)、[README.md](README.md)；RUNBOOK step 4 |
| sync guard（**2026-09-13 起 render 後＝硬閘**） | 腳本（`pipeline/timing.py` 常數） | ■ | **render 前**：短 beat／純 reveal beat 的啟發式**仍是 warn**（`[sync] short/reveal-only beat`，不擋）。**render 後（硬閘）**：ffprobe 實測每個 content 場的影片長度，與 expected 的偏差 > `SYNC_HARD_GATE_FRAMES`＝**2 影格**（fps 由 ffprobe **對成品實測**、不是猜的；㉑ 成片 30 fps＝0.067 s）→ **ERROR、compose 前 abort**（原為 warn）。旁白長過影片的既有 fatal 不變；手改 manifest 的 beat 總和檢查沿用 `SYNC_TOLERANCE_SECONDS`＝0.12 s。**依據**：㉑ 成片 21 場實測最大偏差剛好 1.0 影格、4 場貼線，1 影格零餘裕 | [DESIGN.md](DESIGN.md)、[README.md](README.md)、**本檔 §六**；RUNBOOK step 4 |

### 層 7｜render 成品

| 閘 | 執行者 | 性質 | 把關內容 | 權威文檔 |
|---|---|---|---|---|
| 視覺 gate1 ＝ Claude 抽幀 subagent | Claude 讀 `critic.py --dry-run` 抽出的幀（多模態、免費、每次 render） | □（收斂＝**視覺 blocking==0**） | 逐場 V1–V10 blocking＋A1–A7 magnitude：數學渲染完整、圖正確、表不溢出、reveal 同步、端點實心／空心、✓／✗ 正確、語意色一致（V10，2026-09-13；同一變數在圖與式子 token 不同色＝blocking）（蓋資訊的相撞／關鍵元素出框／reveal 不同步＝blocking） | SSOT [VISUAL-FRAME-RUBRIC.md](content_scripts/_audit/VISUAL-FRAME-RUBRIC.md)（比照 [`../handout/_audit/FIGURE-AUDIT-RUBRIC.md`](../handout/_audit/FIGURE-AUDIT-RUBRIC.md)）；機制 [pipeline/critic.py](pipeline/critic.py) `--dry-run` |
| 視覺 gate2 ＝ 外部 VLM 信心複核 | ffmpeg 抽幀（免費）→ MiMo-V2.5（外部 API；**公測免費**、間歇、`--confirm`、仍需同意） | □（**不接進 make.py**；定稿前非每輪必跑） | **2026-06-16 已接 VISUAL-FRAME-RUBRIC**：runtime verbatim-inject 整份 rubric body，輸出 V1–V9 blocking findings＋`VERDICT` 行＋A1–A7（每維 0–100，**驅動重 render／排優先的 magnitude**）＋具體缺陷；專抓 sizecheck 漏掉的標籤壓線／碰撞。驅動「判→採→重 render→複驗」迴圈（停止條件＝視覺 blocking==0） | SSOT [VISUAL-FRAME-RUBRIC.md](content_scripts/_audit/VISUAL-FRAME-RUBRIC.md)；[README.md](README.md) §VLM 視覺批改、[DESIGN.md](DESIGN.md)；source [pipeline/critic.py](pipeline/critic.py) |
| **`rewatch_pack.py` 12 s 最長靜止硬閘**（`--gate-still`；2026-09-13 裁決） | 腳本（POST-render、離線、確定性） | ■（擋，exit 1） | 只審 `content` 場，量 **0.05% 細門檻**（`FINE_CHANGE_FRAC`）的**最長靜止**：超過 `--gate-still <seconds>`（**預設 12.0、沒有關閉開關**）→ 印 `[still-gate] FAIL <scene>: … (beat N, <reveal>)`、**exit 1**；全過印 `[still-gate] PASS …`、exit 0。verdict 同時寫進 pack 的 **production view**（**不**給盲審鏡看，免污染盲審）。**不接進 `make.py`**——改由輪次協定規定「render 後必跑」（§六 6.4）。**A/B 同基線**：`--baseline <pack dir>` 比對來源 mp4 的 **fps 與畫面尺寸**（pack 現在會記錄兩者），不同、或舊 pack 沒紀錄 → **拒絕、exit 2、什麼都不寫**（不同 fps 會得出假結論） | 三門檻分工見 [DESIGN.md](DESIGN.md) §`[stillness]`；**驗收定義本檔 §六**；rubric [REWATCH-REVIEW-RUBRIC.md](content_scripts/_audit/REWATCH-REVIEW-RUBRIC.md) |
| 人工 frame-grab 驗收 | 人工（MiMo route step 4） | ◆ | 在 reveal 時間點抽幀確認 reveal 準時、LaTeX 無亂碼，才 compose／交付 | [RUNBOOK-mimo-narration-route.md](RUNBOOK-mimo-narration-route.md) step 4 |

外加 **MiMo route step 0**：確認 `storyboards/<deck>.yml` 存在（含 say＋`{show}`），否則整條視覺路徑停住——進視覺步驟的 blocking 前置（[RUNBOOK-mimo-narration-route.md](RUNBOOK-mimo-narration-route.md) step 0）。

---

## 二、貫穿全線的 meta-gate（不綁特定層）

1. **四級 finding 分級**——①真衝突要修 ②discoverability gap ③editorial-drift ④非 finding；只報 tier 1–2，避免 over-report。內嵌在六-lens／review_pack／NFA／prose gate。權威：[`../CLAUDE.md`](../CLAUDE.md)。
2. **回歸再審**——修完 blocking／advisory 不得直接宣告完成，須對改動項重跑一輪並把結果記回原稽核文檔。[`../CLAUDE.md`](../CLAUDE.md)。
3. **付費 API 先同意**——任何計費呼叫前要使用者明確同意；腳本以 `--dry-run`（估 token／USD、不送請求）＋ `--confirm`（讀 env key）落實。離線路徑（mock TTS、本地 render、ffmpeg）免。[`../CLAUDE.md`](../CLAUDE.md)。
4. **NFA 裁決寫進 commit message**——subject ≤70、body 逐條「原本／為何不妥／改了什麼／證據」，供 `git log --grep="NFA"` 撈回（講義 Mode B 仍用 `git log --grep="Mode B"`）。[`../CLAUDE.md`](../CLAUDE.md)。
5. **交付物用 standalone HTML**——等使用者過目的稽核產物一律出可雙擊渲染的 HTML。[`../CLAUDE.md`](../CLAUDE.md)。
6. **每判斷閘一條收斂線**——所有 LLM 判斷閘（六-lens／copyedit／NFA／視覺／工程鏡）收斂判準＝**blocking findings==0**；advisory 逐筆人裁、不強制歸零。**不** governs Tier 0 確定性腳本（以 exit code 收斂）。散文類兩讀者（gate1 Claude 免費迭代→gate2 Codex 收斂後單次、需同意），**gate2 只套 copyedit／NFA**——six-lens 本身 multi-agent＋對抗複驗，不再疊 Codex。gate2 的**頻率**依下條矩陣分層。
8. **gate 頻率矩陣（2026-07-07 修訂；理由＝規模從數節變 30+ 節，修訂紀錄見 [REVIEW_MODEL_DECISIONS.md](REVIEW_MODEL_DECISIONS.md) §九）：**

   | 閘 | gate-1（免費） | gate-2（計費） |
   |---|---|---|
   | Tier-0 確定性腳本 | 每次 render | — |
   | six-lens | 每節 | 無（維持既有拍板） |
   | copyedit | 每節 | **每章抽樣＋出版前抽查；高風險節全跑**（原：每節單次） |
   | NFA | 每節 | **每節**（§3.1 實證 gate-2 抓到 gate-1 漏的 D3 blocking） |
   | 工程鏡（hook） | 每個有 hook 的節 | 高風險才跑 |
   | pedagogy-firstlearner | 每節（pre-render） | 無 |
   | 視覺 frame audit | 每次 final render | VLM＝高風險／出版前抽樣 |
   | amplification | **每章一次**（原：每節） | 無 |
   | REWATCH 看片多鏡（2026-09-13 新增） | **里程碑：每節收斂時一次**（輪內不跑，改回歸清單；§六 6.2） | agy 外部鏡、**與 gate-1 同一次**跑、需逐次同意 |
7. **撰稿兩階段（phase，非 mode）**——**DRAFT**（pre-lock：寫稿→`_narration.html`→copyedit，唯一能改稿窗口）／**LOCKED**（post-lock：derive→NFA→TTS，source 凍結、稽核唯讀）。綁在 `CONTENT_APPROVED` sign-off 這條不可逆邊界；post-lock 改稿須對動到的單元跑一次 scoped NFA 回歸。「Mode」一詞專留給講義 A/B/C。
   **內容鎖（G0，2026-09-13 裁決；見 §六）：** LOCKED 這條邊界延伸到視覺——**旁白與上畫面文字定稿 → NFA 通過 → TTS 合成完成 → 才進視覺／動作設計**。lock 之後仍要改內容，**視為開新一輪內容階段**，明示「部分視覺工作要重做」，**不混進拋光輪**。理由：**會改拍長的東西（旁白、上畫面文字、講義對齊）必須排在動作設計之前**——§3.1 第 ⑲ 輪的五條 must 全部是 Task D 在四原語鋪滿 27 場**之後**才對齊講義、把拍子拉長 6–35 秒造成的（[`KICKOFF-process-reform.md`](KICKOFF-process-reform.md) §2.1）。

---

## 三、隔壁 handout 線（不在 `video/`，但常被一起講）

講義 HTML 散文有**兩道散文稽核閘**：gate 1 = Claude `handout-prose-audit` subagent（免費）、gate 2 = Codex（計費、需同意），兩者共用同一份
`PROSE-AUDIT-RUBRIC.md`（U1–U5 易懂類為 blocking／F1–F5 流暢類為 advisory），互相獨立、不合併。這條是**講義定稿線**，與 video 旁白的 **NFA（原 Mode B）** 是**不同產物的不同閘**，容易混淆——這正是 2026-06-15 把 video「Mode B」改名 NFA 的理由。權威見根 [`../README.md`](../README.md) §Mode B 與 `../CONTENT_SPEC.md`。

---

## 四、目前各節通過狀況

逐節狀態以 [REBUILD_STATUS.md](REBUILD_STATUS.md) 頂部現況快照為準（本檔不再維護逐節表；舊 §1.x 練習時代快照見 git 歷史）。快照要點（2026-07-07）：**§3.1 `ch03_trig_derivatives`＝首個走完整條 MiMo 真旁白路線的正典節**（六-lens／copyedit／sign-off／parity／NFA 雙閘／視覺迭代全過，clean Dean 成片）；§3.2 `ch03_chain_rule` 內容稿 LOCKED（Stage-1 完成，待 spoken／render）；ch01 舊練習產物已刪、屆時整批重跑（`ch01_inverse_functions.yml` 留作版面回歸 deck）。

---

## 五、已知 stale／覆蓋缺口（現狀，非新發現）

- ✅ **~~`review_pack.py` 的 `.tex` parser 已過時~~（2026-06-16 已解）**：已收斂為 engineering 鏡專用、脫離 `.tex`（math context 改吃內容稿）；忠實／語域／拆解三鏡歸 CONTENT-SIXLENS。工程鏡現可實跑（§1.1 dry-run 驗過 1 packet）。
- ✅ **~~`critic.py` header stale／PLACEHOLDER 定價~~（2026-06-16 已解）**：header 重寫為「gate 2、已接 VISUAL-FRAME」；critic.py 定價改 MiMo 公測免費＝$0（dated，仍印 token＋受同意閘），review_pack.py 定價改標「unverified estimate」。
- ✅ **~~`schema.py` 未建~~（2026-06-16 已建）**：結構驗證＋`{show}` 目標列舉，已接進 make.py render 前閘（`--skip-schema` 可繞）。target-vs-payload 交叉驗證仍待 `reveal_targets()`（task #6、需 manim）。
- **直接構造的 `MathTex/Text` 標籤是 sizecheck 盲點**（只靠 VISUAL-FRAME／人眼）；hook code 的數學保真由 review_pack engineering 鏡（advisory）查。
- **整節合併影片**（§1.2／§1.4／§1.5）因 Defender Tex-cache race 尚未驗（逐場已驗）。
- **TTS 發音正確性無逐字自動 listen-back**（只靠 NFA 上游規約＋人工抽驗）；但**離線 listening pack**（`pipeline/listening_pack.py`，2026-07-11 T6）已補「逐 take 聽感驗收」——讀 manifest 產 standalone HTML（每場 `<audio>`＋WPM＋validation/qa＋fallback＋ebur128 LUFS/TP，依風險排序），正式交付前仍應完整聽一次全片。
- **權威來源（NFA 已收回）**：video NFA 的維度／收斂線權威已從「借根 README §Mode B」收回到 [NARRATION-FAITHFULNESS-RUBRIC.md](content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md)（SSOT）；commit 慣例權威仍在 `../CLAUDE.md`。講義 Mode B 的權威仍在**根 README**（不同產物，不混用）。

> **重構落地狀態：已採用·收尾（2026-06-16）。** [REVIEW_MODEL_DECISIONS.md](REVIEW_MODEL_DECISIONS.md) 的 minimal-unify **全主體＋code 回報層 normalize 皆已落地**：NFA 改名＋五份判斷閘 SSOT rubric（NFA/copyedit/VISUAL-FRAME/SIXLENS/HOOK-ENGINEERING）＋thin prompt＋每閘收斂線＋gate1→gate2＋視覺層 figure-audit 鏡像＋DRAFT/LOCKED phase；**code 收尾**＝critic.py 接 VISUAL-FRAME（runtime inject＋V1–V9＋A1–A7＋抽幀新鮮度＋MiMo 免費定價），review_pack.py 收斂為 engineering 鏡＋脫離 `.tex`，兩者 §1.1 dry-run 驗過。**本重構無 open item**；schema.py、VISUAL-FRAME detection 面驗證屬產線 backlog（見 [REBUILD_STATUS.md](REBUILD_STATUS.md)）。

---

## 六、輪次協定（G0–G7；2026-09-13 使用者裁決）

> **這是所有小節共用的驗收定義，不要每節重新發明。**
> **來源與數據：** [`KICKOFF-process-reform.md`](KICKOFF-process-reform.md)——§3.1 一個小節跑了**二十一輪**才收斂的檢討，
> §1 實際數據、§2 根因、§3 為 G0–G7 原文、§5 為「什麼不是浪費」。**本節是驗收定義的 SSOT**；kickoff 是當時的
> 檢討紀錄，兩者牴觸時以本節為準。落地時與 kickoff 原文的已知差異：`[sync]` 容差 **2 影格**（kickoff 寫 1 影格；
> ㉑ 成片 21 場最大偏差剛好 1.0 影格、4 場貼線，1 影格零餘裕）。
> **G0 內容鎖**寫在 §二 第 7 條（綁 DRAFT/LOCKED 邊界）；**G1 兩道硬閘**寫在 §一（層 6 sync guard／層 7 `--gate-still`）。

### 6.1 一輪的定義（G5：批次化）

**一輪 ＝ 收齊該輪全部 must → 併行派工（各自 worktree、各改各的函式）→ 一次 merge → 一次 render → 一次再審。**

**不要一件一輪。** §3.1 的 ⑭–㉑ 八輪跑掉 **8 次全片 1080p render**、每輪派工到 R2 結果約 2–3 小時牆鐘時間；
派工制本身沒問題（24 件改動 19 件一次過），貴的是輪數。

### 6.2 輪內審 vs 里程碑審（G2）

| | **輪內**（每輪） | **里程碑**（一節收斂時） |
|---|---|---|
| 審什麼 | 上一輪 finding 逐條「**已關／未關**」的回歸清單 | 一次**完整六鏡盲審**（REWATCH 五鏡六份：R1 初學者 ×2／R2–R5） |
| 新 finding | **上限 3 條 must**（見下） | 不設限 |
| 生成式盲審 | **不跑** | 跑一次 |

**理由（kickoff §1.2）：** 生成式 advisory 是**每輪重新生成的**，不是「沒修好」——§3.1 的 blocking 每輪都只有 1 條、
且每次都長在那一輪新改的東西上，advisory 卻是 6＋2 → 9 → 8 → **10**，修完又長回來。片子越好，評審的標準跟著抬高；
**每輪跑生成式盲審＝每輪製造工作。**

**新 finding 上限（G2 假設，2026-09-13 設定）：** 輪內新 must **超過 3 條**，就當成**排序問題**——
**退回內容階段**（§二 第 7 條的內容鎖），不要繼續拋光。依據：⑲ 的五條 must 全是 Task D 拉長旁白後的畫面缺口，
剔除後趨勢是 2 → 2 → 1，本來就是收斂的。

### 6.3 停止條件（G3；**開工前就寫死，不是事後判斷**）

**四條同時滿足即收工**，剩下的 `should` 進 backlog：

1. 視覺 blocking ＝ 0
2. **R2 must ＝ 0** — 輪內的意思是：**上一次里程碑審的 must 全部關閉**、且**輪內回歸清單沒有新 must**；
   節收斂時才跑一次完整六鏡（含 R2）確認。（這樣 6.2「不每輪跑生成式盲審」與本條才不矛盾。）
3. 量測指標**連續兩輪**無實質改善（fine 最長靜止**逐場** |Δ| < 0.5 s）
4. `[sync]` ＝ 0、`run_selftests` 全綠、`sizecheck` 0 error

> 依這條，§3.1 **在第 ㉑ 輪就該停**（㉑ 的 21 場 fine 逐場 ±0.0，沒有動到任何驗收指標）。

### 6.4 開工清單（G4：工具先於內容；**每節開工前逐項打勾再動內容**）

- [ ] `python video/pipeline/run_selftests.py` 全綠（＋`python tools/doctor.py --smoke`）
- [ ] `rewatch_pack` 報得出死區的**位置**與**所在拍**（不只長度）——**已做**
- [ ] A/B 兩包 pack **同 fps／同尺寸**：`rewatch_pack --baseline <pack dir>`（不同就 exit 2）
- [ ] `critic.py --out <dir>` **逐輪隔離留底**（同一目錄同時只能一人跑）——**已做**
- [ ] TTS 依 [RUNBOOK-mimo-narration-route.md](RUNBOOK-mimo-narration-route.md)：`--reuse-existing`／`--no-billing`／`--skip-qa` 的適用範圍
      （reuse key 不含場號——**已做**）
- [ ] **兩道硬閘在**：`[sync]`（§一 層 6）與 `[still-gate]`（§一 層 7），render 後必跑

### 6.5 契約進測試（G6）

任何「**本來就該成立但壞掉**」的事，修之前**一律先寫紅測試**——見根 [`../CLAUDE.md`](../CLAUDE.md) Karpathy §4
（「修 bug」→「先寫能重現的測試再讓它過」）。§3.1 後段做對了（`_selftest_figure_labels`、`focus` 的 hollow 案例先紅後綠），
前段沒有：`focus` 還原、耗時誠實、標籤相交、`DashedLine` 盲點全部是先在幀裡肉眼看到、才回頭補 selftest。

### 6.6 多 session 紀律（G7）

- **一個 session 擁有 `main` 與 render**，其他一律 **worktree 分支＋交 hash**
- worktree 開分支後**先 `git merge main`**（分支點可能落後）
- **輸出目錄各自隔離**：`critic.py --out`、`rewatch_pack --out`
- **根因調查一邊做就好**，另一邊只提供量測
- 其餘照根 [`../CLAUDE.md`](../CLAUDE.md) §任務分派的**並行紀律**（開工先 `git status`、別人 dirty 的 hunk 不碰、
  render／tts 的時間窗互相通知、子代理各自 worktree）

### 6.7 什麼**不是**浪費（避免矯枉過正）

**派工制有效**——24 件改動裡 19 件一次過，問題不在派工，在輪數。**拒絕照單全收值得**——
R2 的兩處處方被否決（會在畫面留下假等式、會破壞跨場 `carry`），這種判斷不能為了省輪次而放棄。
真正不可避免的只有**「一個缺陷遮住另一個缺陷」**（鬼影遮住 `focus` 還原、多報抵銷低報），那是狀態空間的性質，
只能一層一層來；**由排序造成的洋蔥不算在內，那是流程的錯**（kickoff §2.5／§5）。

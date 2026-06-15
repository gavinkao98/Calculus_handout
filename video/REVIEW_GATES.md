# video 產線審核閘一覽（review gates map）

> **本檔是地圖／索引，不是權威。** 每道閘的權威定義仍在它的「home doc」（見各列「權威文檔」欄）；
> 這裡只把散落在 [README.md](README.md)、[DESIGN.md](DESIGN.md)、[CONTENT_METHODOLOGY.md](CONTENT_METHODOLOGY.md)、
> [RUNBOOK-mimo-narration-route.md](RUNBOOK-mimo-narration-route.md)、[REBUILD_STATUS.md](REBUILD_STATUS.md) 與
> 根目錄 [`../CLAUDE.md`](../CLAUDE.md)／[`../README.md`](../README.md) 的審核機制收斂成一張表，方便一眼看全貌。
> 整理日期：2026-06-15。內容若與 home doc 牴觸，以 home doc 為準，並回頭修本檔。

## 總綱

產線分**七個產物層**，每層各有審核閘。能真正**擋住 render** 的只有 storyboard/timing 與兩軌 parity 的幾個**自動腳本閘**；
內容／旁白／視覺層全為 **advisory**——模型（Codex / DeepSeek / MiMo / Claude）或人提案，最後由人裁決，**稽核者一律唯讀、不自己改檔**。

流向：講義散文 →（Mode A）內容稿 → 旁白稿 → 口語版 → manim hook code → storyboard/timing → render 成品。

圖例：**■ 自動腳本・可擋 render**　**□ LLM 稽核・advisory**　**◆ 人工閘**　**◷ 未建（TODO）**

---

## 一、各產物層的審核閘

### 層 2｜Mode A 內容稿（`content_scripts/<deck>.md`）

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
| `review_pack.py` engineering lens | 腳本組包（免費）→ DeepSeek（計費，`--confirm`） | □（**不接進 make.py**） | 四鏡頭（忠實／語域／拆解／工程）；工程鏡只看生成 code 的數學保真與慣例（theme primitive 不用 hex、實心／空心點語義、SAFE_MARGIN），**不看美學**。⚠️ 工程鏡**至今從未實跑**；`.tex` parser 自 2026-06-10 改 HTML 源後已過時 | [README.md](README.md) §內容 cross-review；source [pipeline/review_pack.py](pipeline/review_pack.py) |

### 層 6｜storyboard／timing

| 閘 | 執行者 | 性質 | 把關內容 | 權威文檔 |
|---|---|---|---|---|
| `lint.py` | 腳本，make.py render 前跑（`--skip-lint` 可繞） | ■ error／warn | error（abort）：純文字欄出現 `$`／反斜線、`$` 不成對；warn：手動 `\\`、空心點用在已達值 | [DESIGN.md](DESIGN.md)、[README.md](README.md) |
| `sizecheck.py` | 腳本，與 lint 並行（`--skip-sizecheck` 可繞） | ■ error／warn | error（abort）：同層 prose 字級不一、元素出框；warn：教學散文用 muted 色、超安全邊界、內容塊重疊。**盲點**：只查 `brand.prose`，不查直接構造的 `MathTex/Text` | [DESIGN.md](DESIGN.md) |
| `schema.py` | — | ◷ **TODO，未建** | 規劃：格式驗證 ＋ 列舉 `{show}` reveal 目標。目前不存在 | [DESIGN.md](DESIGN.md)、[README.md](README.md) |
| make.py manifest-freshness（`--reuse-audio`） | 腳本 | ■（fail-fast） | 比對 manifest 與 `<deck>_mimo.yml`（deck id／scene／beat 數／`{show}`／text_hash／WAV 存在與時長），防複用過期音檔；非 reuse 跑時拒絕用 mock 覆蓋真 manifest | [DESIGN.md](DESIGN.md)、[README.md](README.md)；RUNBOOK step 4 |
| sync guard | 腳本（`pipeline/timing.py` 常數） | ■／□ | render 前 warn 短 beat／純 reveal beat；render 後 ffprobe 比對影音時長，旁白超過影片→compose 前 abort | [DESIGN.md](DESIGN.md)、[README.md](README.md)；RUNBOOK step 4 |

### 層 7｜render 成品

| 閘 | 執行者 | 性質 | 把關內容 | 權威文檔 |
|---|---|---|---|---|
| 視覺 gate1 ＝ Claude 抽幀 subagent | Claude 讀 `critic.py --dry-run` 抽出的幀（多模態、免費、每次 render） | □（收斂＝**視覺 blocking==0**） | 逐場：數學渲染完整、圖正確、表不溢出、reveal 同步、端點實心／空心、✓／✗ 正確（蓋資訊的相撞／關鍵元素出框／reveal 不同步＝blocking） | SSOT [VISUAL-FRAME-RUBRIC.md](content_scripts/_audit/VISUAL-FRAME-RUBRIC.md)（已寫；critic.py 接線延後。比照 [`../handout/_audit/FIGURE-AUDIT-RUBRIC.md`](../handout/_audit/FIGURE-AUDIT-RUBRIC.md)）；機制 [pipeline/critic.py](pipeline/critic.py) `--dry-run` |
| 視覺 gate2 ＝ 外部 VLM 信心複核 | ffmpeg 抽幀（免費）→ MiMo-V2.5（計費、間歇、`--confirm`、需同意） | □（**不接進 make.py**；定稿前非每輪必跑） | 五維 AES rubric，每維 0–100（保留當**驅動重 render／排優先的 magnitude**）＋ 具體缺陷（severity＋位置）；專抓 sizecheck 漏掉的標籤壓線／碰撞。驅動「判→採→重 render→複驗」迴圈（停止條件＝視覺 blocking==0） | [README.md](README.md) §VLM 視覺批改、[DESIGN.md](DESIGN.md)；source [pipeline/critic.py](pipeline/critic.py) |
| 人工 frame-grab 驗收 | 人工（MiMo route step 4） | ◆ | 在 reveal 時間點抽幀確認 reveal 準時、LaTeX 無亂碼，才 compose／交付 | [RUNBOOK-mimo-narration-route.md](RUNBOOK-mimo-narration-route.md) step 4 |

外加 **MiMo route step 0**：確認 `storyboards/<deck>.yml` 存在（含 say＋`{show}`），否則整條視覺路徑停住——進視覺步驟的 blocking 前置（[RUNBOOK-mimo-narration-route.md](RUNBOOK-mimo-narration-route.md) step 0）。

---

## 二、貫穿全線的 meta-gate（不綁特定層）

1. **四級 finding 分級**——①真衝突要修 ②discoverability gap ③editorial-drift ④非 finding；只報 tier 1–2，避免 over-report。內嵌在六-lens／review_pack／NFA／prose gate。權威：[`../CLAUDE.md`](../CLAUDE.md)。
2. **回歸再審**——修完 blocking／advisory 不得直接宣告完成，須對改動項重跑一輪並把結果記回原稽核文檔。[`../CLAUDE.md`](../CLAUDE.md)。
3. **付費 API 先同意**——任何計費呼叫前要使用者明確同意；腳本以 `--dry-run`（估 token／USD、不送請求）＋ `--confirm`（讀 env key）落實。離線路徑（mock TTS、本地 render、ffmpeg）免。[`../CLAUDE.md`](../CLAUDE.md)。
4. **NFA 裁決寫進 commit message**——subject ≤70、body 逐條「原本／為何不妥／改了什麼／證據」，供 `git log --grep="NFA"` 撈回（講義 Mode B 仍用 `git log --grep="Mode B"`）。[`../CLAUDE.md`](../CLAUDE.md)。
5. **交付物用 standalone HTML**——等使用者過目的稽核產物一律出可雙擊渲染的 HTML。[`../CLAUDE.md`](../CLAUDE.md)。
6. **每判斷閘一條收斂線**——所有 LLM 判斷閘（六-lens／copyedit／NFA／視覺）收斂判準＝**blocking findings==0**；advisory 逐筆人裁、不強制歸零。**不** governs Tier 0 確定性腳本（以 exit code 收斂）。散文類兩讀者（gate1 Claude 免費迭代→gate2 Codex 收斂後單次、需同意），**gate2 只套 copyedit／NFA**——six-lens 本身 multi-agent＋對抗複驗，不再疊 Codex。
7. **撰稿兩階段（phase，非 mode）**——**DRAFT**（pre-lock：寫稿→`_narration.html`→copyedit，唯一能改稿窗口）／**LOCKED**（post-lock：derive→NFA→TTS，source 凍結、稽核唯讀）。綁在 `CONTENT_APPROVED` sign-off 這條不可逆邊界；post-lock 改稿須對動到的單元跑一次 scoped NFA 回歸。「Mode」一詞專留給講義 A/B/C。

---

## 三、隔壁 handout 線（不在 `video/`，但常被一起講）

講義 HTML 散文有**兩道散文稽核閘**：gate 1 = Claude `handout-prose-audit` subagent（免費）、gate 2 = Codex（計費、需同意），兩者共用同一份
`PROSE-AUDIT-RUBRIC.md`（U1–U5 易懂類為 blocking／F1–F5 流暢類為 advisory），互相獨立、不合併。這條是**講義定稿線**，與 video 旁白的 **NFA（原 Mode B）** 是**不同產物的不同閘**，容易混淆——這正是 2026-06-15 把 video「Mode B」改名 NFA 的理由。權威見根 [`../README.md`](../README.md) §Mode B 與 `../CONTENT_SPEC.md`。

---

## 四、目前各節（§1.x）通過狀況

> 以 [REBUILD_STATUS.md](REBUILD_STATUS.md) 為準；本表為快照（2026-06-15）。**註：講義已再次修訂，舊片全屬練習、將以本次重構後的新流程整批重跑——下表轉為歷史快照，重跑後重填。**

| 節 | 六-lens | 旁白 sign-off | parity | NFA | 抽幀目視 | critic.py VLM |
|---|---|---|---|---|---|---|
| §1.1 | （改用 critic＋review_pack） | ✅ | ✅ | ✅ | ✅ | ✅（4 缺陷修＋複驗） |
| §1.2 | ✅（13→1） | ⏳ | ✅ | ✅ | ✅ | ⏳ |
| §1.3 | ✅ | ⏳ | ✅ | ✅（收斂，commit `cb98ebf`） | ✅ | ⏳ |
| §1.4 | ✅（全乾淨） | ⏳ | spoken 未寫 | ❌ | ✅（480p） | ⏳ |
| §1.5 | ✅（5→0 blocking） | ✅ | spoken 未寫 | ❌ | ✅（480p） | ⏳ |
| §1.6 ε-δ | ❌（legacy，drift 修復中） | legacy 核可 | spoken 未寫 | ❌ | ✅（8 關鍵幀） | ⏳ |

§1.6 是覆蓋最薄的一節（無六-lens、storyboard 未同步、ε-δ 動畫 3 個問題未修、NFA／MiMo 未起步）。

---

## 五、已知 stale／覆蓋缺口（現狀，非新發現）

- **`review_pack.py` 的 `.tex` parser 已過時**：source 早改 HTML，忠實／工程鏡的 `.tex` 切片 context 失效，未重寫前等於跛腳；且工程鏡從未真正跑過。
- **`critic.py` 的 header 還寫「P1 scaffold／TODO: wire」，但計費路徑其實已完整可用**（§1.1 實跑過）——註解本身才是 stale。`critic.py` 與 `review_pack.py` 的**定價常數都還是 PLACEHOLDER**，dry-run 的 USD 估值尚不準。
- **`schema.py` 未建**：storyboard YAML 無結構／格式驗證，也無自動列舉 `{show}` 目標，規劃中的第三道 render 前閘缺席。
- **hook code 只有那個從未實跑的 advisory 鏡**；直接構造的 `MathTex/Text` 標籤是 sizecheck 盲點（只靠 VLM／人眼）。
- **整節合併影片**（§1.2／§1.4／§1.5）因 Defender Tex-cache race 尚未驗（逐場已驗）。
- **TTS 發音正確性無自動 listen-back**，只靠 NFA 上游規約＋人工抽驗。
- **權威來源（NFA 已收回）**：video NFA 的維度／收斂線權威已從「借根 README §Mode B」收回到 [NARRATION-FAITHFULNESS-RUBRIC.md](content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md)（SSOT）；commit 慣例權威仍在 `../CLAUDE.md`。講義 Mode B 的權威仍在**根 README**（不同產物，不混用）。

> **重構落地狀態：** [REVIEW_REDESIGN.md](REVIEW_REDESIGN.md) 的 minimal-unify 已**部分採用（2026-06-15）**：NFA 改名＋抽 NFA/copyedit/VISUAL-FRAME/SIXLENS SSOT rubric＋thin prompt＋每閘收斂線＋gate1→gate2＋視覺層改 figure-audit 鏡像＋DRAFT/LOCKED phase 均已落地（**四份判斷閘 rubric 齊**）。**待續**：code 回報層 normalize（`review_pack`/`critic` buckets 與定價、critic.py 接 `VISUAL-FRAME-RUBRIC` 並加 A6/A7、`review_pack` 工程鏡待 `.tex` parser 修）。

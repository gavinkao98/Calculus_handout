# video 撰稿 mode 與審核模式重構（提案）

> **狀態:提案（尚未採用）。** 整理日期 2026-06-15。本檔記錄一份「參考講義審核模式、重構 video mode／審核」的設計意見，**供裁決用，先不動手**。
> 現況地圖見 [REVIEW_GATES.md](REVIEW_GATES.md)（本提案要改的對象）。講義審核的權威契約見 [`../handout/_audit/PROSE-AUDIT-RUBRIC.md`](../handout/_audit/PROSE-AUDIT-RUBRIC.md)、[`../handout/_audit/FIGURE-AUDIT-RUBRIC.md`](../handout/_audit/FIGURE-AUDIT-RUBRIC.md)；三-mode 狀態機在根 [`../README.md`](../README.md) §撰稿工作流程。
>
> **已拍板的兩個決定（2026-06-15）：**
> 1. 走 **minimal-unify**（統一回報 + 抽 rubric + 解命名衝突），**不重寫、不造狀態機**。
> 2. **Tier 1 散文類判斷閘（copyedit／NFA）在收斂時常跑付費 gate2（Codex 獨立第二讀者）**，比照講義散文閘；接受每節多一筆 Codex 計費，並依 [`../CLAUDE.md`](../CLAUDE.md) 付費 API 規則每次先取得同意。
>
> **尚待裁決：** 見文末 §七。

---

## 〇、一句話結論

video 今天唯一**客觀**的缺口是:五個判斷閘**沒有任何一個寫了收斂判準**（講義有 `blocking==0` 這條線）。其餘大多是**詞彙零散**（六-lens 用四級、NFA 用 D1–D7、copyedit 用 Tighten/Optional、critic 用 0–100、review_pack 又用四級），不是流程壞掉。
→ 該做的是**統一回報 + 抽 SSOT rubric + 解 Mode B 命名衝突**，不是造新流程。最該先做的單一動作是把 video「Mode B」改名 **NFA**。

「參考講義」最大的陷阱是**照抄結構**（造 video 版 A/B/C 狀態機、加 expansion marker、每層配付費第二讀者）。三個獨立角度提案 + 三輪對抗式批判**一致**把這幾項判為過度工程——理由見 §二。

---

## 一、講義模式為什麼乾淨 — 可以直接搬的 6 件事

與產物無關、搬到 video 完全成立:

1. **一個 artifact 一份 SSOT rubric，prompt 只「引用」不「複述」**（防漂移）。講義 `PROSE-AUDIT-RUBRIC.md` 是兩道閘共讀的唯一契約；repo 內已驗證兩次（PROSE + FIGURE）。
2. **單一 severity 軸（Blocking/Advisory）+ 單一收斂判準（`blocking==0`）**；advisory 由使用者逐條裁、不強制歸零（直接搬 `PROSE-AUDIT-RUBRIC.md`:40）。
3. **rubric / spec / prompt 三層分離**:rubric 說「審哪些維度、哪些擋稿、怎麼回報」，規範本身留在 [CONTENT_METHODOLOGY.md](CONTENT_METHODOLOGY.md)／[DESIGN.md](DESIGN.md)，prompt 只是把模型接到 rubric 的薄線。
4. **唯讀、propose-not-act、人裁決**（video 已是此規矩，只是沒寫進每份 rubric）。
5. **明確 non-findings 清單 + 四級回報 + 「乾淨章節是有效結果、不 over-report」**。
6. **兩個獨立讀者、同一把尺、不同模型家族、不合併**——但**只用在散文類閘**，且視覺第二讀者**非每輪必跑**（講義 figure audit 本就 consent-gated 間歇跑，見 `FIGURE-AUDIT-RUBRIC.md` §「非每輪必跑」）。

---

## 二、video 跟講義不一樣 — 所以不能照抄

| 講義 | video | 結論 |
|---|---|---|
| 單一散文產物 + `<!-- expansion: -->` marker | 六種產物；**無 marker**（grep 0 命中），用更強的 per-unit `source` 欄追溯（單元 MUST 回溯到講義環境，否則 stage-2 前出局） | 別引入 marker（平行第二套追溯系統） |
| 無確定性腳本閘 | 5 個 **exit-code 可擋 render** 的腳本 | 這層**別套** Blocking/Advisory，exit code 比任何 rubric 強 |
| 只有 gate2 一個付費點 | lock→derive→**付費 TTS**、VLM、DeepSeek；產物要先**花錢合成**才能審 | 別每層加付費 gate2 |
| 線性 A→B→C | workflow **2026-06-14 刻意放寬成部分並行**（storyboard 可早於核可） | 單一 `state` scalar 表達不了，造狀態機反而退步 |

---

## 三、提案:新結構

### 3.1 Mode（撰稿階段）— 只「命名」既有兩階段，不造狀態機

綁在唯一真實的不可逆邊界:**旁白 sign-off／`CONTENT_APPROVED` lock**。

- **DRAFT（pre-lock）**:寫 content 稿 → `_narration.html` → copyedit pass。**唯一能改稿、刪贅字的窗口**（copyedit 可改 source）。§7 的 12 項 checklist 即收尾的 amplification audit。
- **LOCKED（post-lock）**:`derive_spoken` → NFA → TTS。source 凍結，所有稽核唯讀、不重啟已核可內容。

講義 **Mode C** 不造對應新 mode——對映既有 §8 維護路徑，只加**一句**:「post-lock 改稿必須對動到的單元跑一次 scoped NFA 回歸」（把回歸再審 meta-rule 對此情境講明）。

**詞彙紀律**:`Mode` = 撰稿狀態階段（artifact-agnostic；Mode A/B/C 保留講義原義）；`gate` = 對單一 artifact 跑 rubric。今天被誤標「video Mode B」的東西是一個 **gate**，不是 mode。

### 3.2 審核分三層

| 層 | 性質 | 收斂 | 內容 |
|---|---|---|---|
| **Tier 0 · 確定性 CI** | `■` 可擋 render、exit code、**無 rubric/model** | exit 0 | `derive_spoken --check`、`lint.py`、`sizecheck.py`、`manifest-freshness`、`sync guard`。講義無對應，**完全別碰**、別套 Blocking/Advisory |
| **Tier 1 · 散文類判斷閘** | `□` advisory、**兩獨立讀者**（gate1 Claude 免費／gate2 Codex 付費、不合併） | `blocking==0` | 六-lens content（DRAFT）、copyedit pass（DRAFT・可改稿）、**NFA**（LOCKED・原「Mode B」）。**真正貼合講義兩道閘模式的就是這層** |
| **Tier 2 · 非散文判斷閘** | `□` advisory、**單讀者 + 間歇付費第二讀者**（比照 figure audit） | `blocking==0` | 視覺 AES critic（0–100 保留當驅動重 render 迴圈的 magnitude）、hook-code 工程鏡（◷ 執行器壞著、`.tex` parser 過時、從未實跑 → **先修執行器、rubric 後寫**） |

**全判斷閘共用（Tier 1＋2）**:① 單一 Blocking/Advisory 軸（退掉 Tighten/Optional、四級、low/med/high 當 disposition）② 每閘一條 `blocking==0` 收斂線 ③ 一 artifact 一份 SSOT rubric、引用不複述 ④ 唯讀、propose-not-act ⑤ 明確 non-findings、不 over-report。

**gate2 政策（已拍板）**:Tier 1 散文閘在**收斂時常跑** Codex gate2（獨立第二讀者，補 gate1 的模型盲點）；每次依付費 API 規則先取得同意（`--dry-run` 估值 → `--confirm`）。Tier 2 維持單讀者 + 間歇付費。

### 3.3 命名衝突 → 把 video「Mode B」改名 NFA（最高價值單一動作）

講義 Mode B（走 marker、Keep/Rewrite/**Move**/Cut）與 video「Mode B」（D1–D7 旁白忠實稽核、**無 Move**）**同名、同一份根 README 權威、卻是不同產物的不同閘**。
→ 改名 **NFA（旁白忠實稽核 / Narration Faithfulness Audit）**。維度 D1–D7 原封不動，只:
- rename `PROMPT-narration-modeB.template.md` → `PROMPT-narration-faithfulness.template.md`；
- self-label 改「Narration Faithfulness Auditor」；
- 更新 [REVIEW_GATES.md](REVIEW_GATES.md) 那一列 + §1.x 狀態表頭 + 交叉引用；
- 加一句 lineage（「formerly video Mode B」alias，讓舊 git 史撈得到）；
- 權威從「借根 README §Mode B」收回到新的 `NARRATION-FAITHFULNESS-RUBRIC.md`；
- commit-grep 分流:video 用 `git log --grep="NFA"`、講義保留 `Mode B`。

> 三版提案、三版批判**一致**認定這是全場最高價值、最低風險的一步——**無論其他做不做，這個先 ship。**

---

## 四、別做的事（過度工程陷阱）

- ❌ 造 video 版 A/B/C 狀態機 + `state:` front-matter——憑空多概念、且表達不了並行 workflow。
- ❌ 機器強制狀態轉移（手寫欄位會說謊；真正把關者是 `manifest-freshness`／`derive --check`／`sync guard`，已在做）。
- ❌ 每層加**強制**付費 gate2（疊在已計費的合成之上）。註:Tier 1 散文閘的收斂 gate2 是**已拍板要保留**的例外，但仍走同意閘。
- ❌ 給死工具（工程鏡、`schema.py`）先寫漂亮 rubric——沒有可跑的執行器，rubric 只是儀式。
- ❌ 重新引入 `<!-- expansion: -->` marker（`source` 欄已是更強追溯）。
- ❌ 把 copyedit（可改稿）和 NFA（只讀）merge 成一份 rubric 用 flag 切——那把實體安全牆降級成設定旗標。
- ❌ 壓掉 critic 的 0–100（迴圈靠它排優先）。
- ❌ 讓這件事擋住 §1.4／1.5／1.6 的內容進度（§1.6 最薄，優先把 deck 做完）。

---

## 五、落地順序（漸進，別停內容）

1. **改名 NFA**（獨立、近零風險）。rename 模板 + self-label + REVIEW_GATES 那列 + §1.x 表頭 + 交叉引用；加 lineage／alias；CLAUDE.md 加一句 commit-grep 分流。改前後各 grep `Mode B` 抓 dangler。
2. **加收斂線**（每閘一句）。搬 `PROSE-AUDIT-RUBRIC.md`:40:「gate passes = Blocking==0；Advisory 逐條裁、不強制歸零」。註明**不**governs Tier 0 腳本（exit-code 收斂）；順便給 critic 的「判→採→重 render→複驗」迴圈一個現在沒有的停止條件。
3. **抽 SSOT rubric**（只給**會跑**的閘）:`NARRATION-FAITHFULNESS-RUBRIC.md`（D1–D7 + `CONTENT_APPROVED`→D7 規則）、`NARRATION-COPYEDIT-RUBRIC.md`（C1–C5 + 「blocking 結構上恆 0」註）、`CONTENT-SIXLENS-RUBRIC.md`（六鏡頭）、`VISUAL-AES-RUBRIC.md`（5 AES 維）。內容從現有模板／code 搬，**不發明新維度**。工程鏡 + schema 標 ◷、先不寫。
4. **thin prompts**:prompt 改成引用 rubric、刪掉內嵌維度。
5. **normalize code 回報層**（`review_pack.py`／`critic.py` 只改回報 buckets，不動邏輯；順手修 PLACEHOLDER 定價，讓 `--dry-run` USD 準）。**不碰** derive/lint/sizecheck/manifest/sync。
6. **標 DRAFT/LOCKED phase**（CONTENT_METHODOLOGY §6/§7 既有 lock 點周圍）+ 那句 post-lock scoped NFA 回歸。把 REVIEW_GATES／README 的權威指標收回到這個 in-video phase 權威。
7. **回歸驗證**:對已收斂的 §1.3（commit `cb98ebf`）重跑 reference-only 的 copyedit + NFA，確認 findings／verdict 一致，證明抽 rubric 沒引入漂移，**才**正式刪內嵌維度。結果記回 REVIEW_GATES §五／REBUILD_STATUS。
8. **執行器修復延後**:`review_pack.py` 的 `.tex` parser 重寫（然後才給工程鏡 rubric）、建 `schema.py`——等 §1.x 內容 backlog 清完再做。

---

## 六、講義借來的設計動作 ↔ video 落點對照

| 講義設計動作 | video 落點 |
|---|---|
| SSOT rubric、引用不複述 | §五 步驟 3／4：四份 `*-RUBRIC.md` + thin prompts |
| 單軸 + `blocking==0` | §五 步驟 2：每閘收斂線 |
| 兩獨立讀者、不同模型、不合併 | Tier 1（gate1 Claude／gate2 Codex，收斂時常跑） |
| 視覺第二讀者間歇 | Tier 2（critic VLM 間歇付費） |
| 唯讀、propose-not-act | 寫進每份 rubric 護欄 |
| non-findings、不 over-report、四級 | 每份 rubric 帶 §3-protected 類比清單 |
| 交付 standalone HTML（穩定 finding id） | 沿用既有 CLAUDE.md 交付規則 |

---

## 七、尚待裁決

- **rubric 檔案位置**:`video/content_scripts/_audit/RUBRICS/` 子目錄，還是平鋪在 `_audit/`（完全比照 `handout/_audit/`）?
- **code-rubric 抽取深度**:`critic.py` runtime 載入 `.md`（真 single source、多一點 code）vs header 註解指標（最少改動、易漂移）。建議:`critic.py`（會跑）用 runtime 載入;工程鏡在 parser 修好前**整個不抽**。
- **採用時機**:本提案何時從「提案」轉「採用」、是否要先在 §1.1（唯一全綠節）試點再 roll 到 §1.2/§1.3。

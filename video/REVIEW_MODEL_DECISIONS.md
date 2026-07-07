# video 審核模式重構——決策紀錄（REVIEW_MODEL_DECISIONS）

<!-- 原檔名 REVIEW_REDESIGN.md，2026-06-16 更名為 REVIEW_MODEL_DECISIONS.md（與產線格式契約 DESIGN.md 區隔，免「design/redesign」混淆）。 -->


> **狀態：已採用（收尾於 2026-06-16）。** 本檔原為「參考講義審核模式、重構 video mode／審核」的設計提案；**minimal-unify 全主體＋當初延後的 code 回報層 normalize 皆已落地**——本檔自此轉為**決策紀錄**（不再有待續工程），活的流程地圖以 [REVIEW_GATES.md](REVIEW_GATES.md) 為準、進度錨以 [REBUILD_STATUS.md](REBUILD_STATUS.md) 為準。落地清單見 §八（含 2026-06-16 code 收尾）。講義審核的權威契約見 [`../handout/_audit/PROSE-AUDIT-RUBRIC.md`](../handout/_audit/PROSE-AUDIT-RUBRIC.md)、[`../handout/_audit/FIGURE-AUDIT-RUBRIC.md`](../handout/_audit/FIGURE-AUDIT-RUBRIC.md)；三-mode 狀態機在根 [`../README.md`](../README.md) §撰稿工作流程。
>
> **已拍板的決定（2026-06-15）：**
> 1. 走 **minimal-unify**（統一回報 + 抽 rubric + 解命名衝突），**不重寫、不造狀態機**。✅ 已落地。
> 2. **Tier 1 散文類判斷閘（copyedit／NFA）配付費 gate2（Codex 獨立第二讀者）**，比照講義散文閘。**排序已釐清：gate1（Claude，免費）迭代到 `blocking==0`，gate2（Codex）收斂後跑單次確認**（非進迭代圈——配合 Codex token 額度有限）；每次依 [`../CLAUDE.md`](../CLAUDE.md) 付費 API 規則先取得同意。**範圍：gate2 只套 copyedit／NFA**，six-lens 本身 multi-agent＋對抗複驗，不再疊 Codex（修原 line 65 把 six-lens 算進「兩讀者」的歧義）。✅ 已落地。
> 3. **視覺層（Tier 2）改 figure-audit 鏡像：** gate1 ＝ Claude 抽幀 subagent（免費、每次 render，讀 [`VISUAL-FRAME-RUBRIC.md`](content_scripts/_audit/VISUAL-FRAME-RUBRIC.md)）；gate2 ＝ 外部 VLM（MiMo-V2.5、`critic.py`，間歇、計費、需同意）。0–100 留當 magnitude、收斂＝視覺 blocking==0。✅ 已落地（rubric 已寫：V1–V9 blocking ＋ A1–A7 magnitude；critic.py 接線已於 2026-06-16 完成，見 §八）。
> 4. **影片語域：影片刻意比講義口語**（§4 Register 放寬，已落地）；忠實的是內容不是措辭，NFA 不拿旁白比講義正式度。
>
> **待續：無。** 五份判斷閘 SSOT rubric 已齊（six-lens／copyedit／NFA／VISUAL-FRAME／hook-engineering），code 回報層 normalize 已收尾，engineering 鏡退場 DeepSeek、改 gate1 Claude／gate2 Codex（2026-06-16，見 §八）。本檔不再有 open item；產線後續工作（`schema.py` 已建；剩 VISUAL-FRAME detection 面驗證、task #6 reveal_targets）屬產線 backlog、不屬本重構，追在 [REBUILD_STATUS.md](REBUILD_STATUS.md)。

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

### 3.1 phase（撰稿階段）— 只「命名」既有兩階段，不造狀態機

綁在唯一真實的不可逆邊界:**旁白 sign-off／`CONTENT_APPROVED` lock**。

- **DRAFT（pre-lock）**:寫 content 稿 → `_narration.html` → copyedit pass。**唯一能改稿、刪贅字的窗口**（copyedit 可改 source）。§7 的 12 項 checklist 即收尾的 amplification audit。
- **LOCKED（post-lock）**:`derive_spoken` → NFA → TTS。source 凍結，所有稽核唯讀、不重啟已核可內容。

講義 **Mode C** 不造對應新 mode——對映既有 §8 維護路徑，只加**一句**:「post-lock 改稿必須對動到的單元跑一次 scoped NFA 回歸」（把回歸再審 meta-rule 對此情境講明）。

**詞彙紀律（已採用）**:`phase` = 撰稿狀態階段（DRAFT/LOCKED；artifact-agnostic）；**「Mode」一詞專留給講義 A/B/C**——不再用「Mode」指 video 階段，免得重蹈剛治好的「同名異義」病。`gate` = 對單一 artifact 跑 rubric。今天被誤標「video Mode B」的東西是一個 **gate**，已改名 NFA。

### 3.2 審核分三層

| 層 | 性質 | 收斂 | 內容 |
|---|---|---|---|
| **Tier 0 · 確定性 CI** | `■` 可擋 render、exit code、**無 rubric/model** | exit 0 | `derive_spoken --check`、`lint.py`、`sizecheck.py`、`manifest-freshness`、`sync guard`。講義無對應，**完全別碰**、別套 Blocking/Advisory |
| **Tier 1 · 散文類判斷閘** | `□` advisory；**copyedit／NFA 走兩獨立讀者**（gate1 Claude 免費迭代→gate2 Codex 收斂後單次、不合併）；**six-lens 本身即 multi-agent＋對抗複驗，不再疊 gate2** | `blocking==0` | 六-lens content（DRAFT）、copyedit pass（DRAFT・可改稿）、**NFA**（LOCKED・原「Mode B」）。**真正貼合講義兩道閘模式的是 copyedit／NFA 這兩支** |
| **Tier 2 · 非散文判斷閘** | `□` advisory、**單讀者 + 間歇付費第二讀者**（比照 figure audit） | `blocking==0` | 視覺 AES critic（0–100 保留當驅動重 render 迴圈的 magnitude）、hook-code 工程鏡（◷ 執行器壞著、`.tex` parser 過時、從未實跑 → **先修執行器、rubric 後寫**） |

**全判斷閘共用（Tier 1＋2）**:① 單一 Blocking/Advisory **收斂軸**（blocking vs 其餘；advisory 可像講義 SSOT 那樣再細分 Tighten/Optional 當 disposition——copyedit 即沿用此細分、NFA 用 Blocking/Advisory）② 每閘一條 `blocking==0` 收斂線 ③ 一 artifact 一份 SSOT rubric、引用不複述 ④ 唯讀、propose-not-act ⑤ 明確 non-findings、不 over-report。

**gate2 政策（已拍板）**:copyedit／NFA 的 gate1（Claude，免費）迭代到 `blocking==0`，**gate2（Codex）收斂後跑單次確認**（非進迭代圈；配合 Codex token 額度有限）；每次依付費 API 規則先取得同意（`--dry-run` 估值 → `--confirm`）。**gate2 不套 six-lens**。Tier 2 維持單讀者 + 間歇付費第二讀者（視覺 gate2＝外部 VLM）。

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
3. **抽 SSOT rubric**（只給**會跑**的閘）:`NARRATION-FAITHFULNESS-RUBRIC.md`（D1–D7 + `CONTENT_APPROVED`→D7 規則）、`NARRATION-COPYEDIT-RUBRIC.md`（C1–C5 + 「blocking 結構上恆 0」註）、`CONTENT-SIXLENS-RUBRIC.md`（六鏡頭）、`VISUAL-FRAME-RUBRIC.md`（V1–V9 blocking ＋ A1–A7 magnitude）。內容從現有模板／code 搬，**不發明新維度**。工程鏡 + schema 標 ◷、先不寫。
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

## 七、裁決紀錄與待續

**已裁決（2026-06-15）：**

- **rubric 檔案位置 → 平鋪在 `_audit/`**（比照 `handout/_audit/`），不開 `RUBRICS/` 子目錄。理由：本輪只 4 份 rubric（其中 2 份已寫），不足以撐子目錄；平鋪降低「比照講義」的認知成本；子目錄是投機性結構，等檔案真多再抽。
- **code-rubric 抽取深度 → `critic.py` runtime 載入、且 verbatim-inject**：把整份 `VISUAL-FRAME-RUBRIC.md` body 原文塞進 prompt（不解析 section），既是真 SSOT 又幾乎零增量 code，消掉「多 code」缺點。header 註解指標出局（就是要殺的 drift 陷阱）。工程鏡在 `.tex` parser 修好前**整個不抽**。
- **採用時機 → 重新框定**：rubric 是**全域契約、非 per-section 狀態**，抽出即所有未來節共用，沒有「試點一節再 roll」這回事。NFA 改名全域立即；真正 per-section 的只有**回歸驗證**（拿已收斂節證明抽 rubric 沒漂移）。又因講義已修、舊片全屬練習要整批重跑，原 §五 step 7（拿 §1.3 `cb98ebf` 回歸驗證）**降級為選用**：可在刪練習稿前花十分鐘做一次靜態維度等價檢查（驗 rubric≡原內嵌維度），或直接拿第一個真正重跑的節當驗證。

**已收尾（2026-06-16；原列「待續」項全數落地）：**

- **`VISUAL-FRAME-RUBRIC.md` ✅ 已寫＋已接線（2026-06-16）**：兩層——V1–V9 blocking（出框／相撞蓋字／視窗可讀／Tex 渲染／端點記號／幀↔旁白／reveal 同步／可見數學正確；D8 灰階已砍、V8 限可見）＋ A1–A7 magnitude（原 5 維＋A6 typography/wrapping＋A7 hierarchy/focus）。**critic.py 接線已完成**：runtime verbatim-inject 整份 rubric body（取代 hardcoded 5 維）、JSON schema／`_write_md` 改 V1–V9 blocking findings＋VERDICT 行＋A1–A7 scores、修抽幀新鮮度（ffmpeg 前 unlink）；§1.1 真 `--dry-run` 驗過。
- **`CONTENT-SIXLENS-RUBRIC.md` ✅ 已寫（2026-06-16）**：六鏡 L1–L6（忠實／拆解／語域／不重複／數學正確隔離盲算／完整），無 Codex gate2（multi-agent＋refute 已足），收斂＝blocking==0。維度從 REVIEW_GATES §一 六維列表＋CONTENT_METHODOLOGY 蒸餾、**未發明新維**。
- **code 回報層 normalize ✅ 已收尾（2026-06-16）**：
  - `critic.py`：見上條（接 VISUAL-FRAME、A6/A7＋V 維、抽幀新鮮度）；定價改誠實值（**MiMo-V2.5 公測免費＝$0**，dated，仍印 token 量＋仍受同意閘）；清掉 stale header（「P1 scaffold／TODO: wire」）；stdout 改 UTF-8（Windows cp950 console 不再因注入的中文 rubric 崩）。
  - `review_pack.py`：**收斂為 engineering 鏡專用並脫離 `.tex`**——faithfulness／register／decomposition 三鏡已被 CONTENT-SIXLENS 完全取代（保留即「平行第二套」反模式），故移除；工程鏡的 math context 改吃內容稿動畫單元的 narration／`source`（`chapters/*.tex` 早搬 `legacy/`、原 parser 已失效，故不重建 HTML parser）；定價標籤改「unverified estimate」。§1.1 真 `--dry-run` 驗過（1 packet、content-script math context）。
  - **與原 §七「工程鏡在 `.tex` parser 修好前整個不抽」的差異：** 該決策已被取代——不修 `.tex` parser、改脫鉤＋收斂到工程鏡，因三個內容鏡已歸 six-lens、重建 HTML faithfulness parser 反而是冗餘。

---

## 八、落地紀錄（2026-06-15，本輪實作）

minimal-unify 主體已落地（地圖 [REVIEW_GATES.md](REVIEW_GATES.md) 已同步、進度錨 [REBUILD_STATUS.md](REBUILD_STATUS.md) 已記）：

1. **NFA 改名**：`PROMPT-narration-modeB.template.md` → `PROMPT-narration-faithfulness.template.md`（`git mv`）；self-label、REVIEW_GATES 列／表頭、DESIGN／RUNBOOK／README／REBUILD_STATUS／CONTENT_METHODOLOGY 交叉引用、CLAUDE.md commit-grep 分流均更新；lineage「formerly video Mode B」寫入 rubric。歷史紀錄（per-deck REPORT-*、content_scripts 狀態註記）刻意不改、靠 lineage 撈回。
2. **抽 SSOT rubric＋thin prompt**：新增 [`NARRATION-FAITHFULNESS-RUBRIC.md`](content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md)（D1–D7＋reader 拆法＋gate1→gate2＋conditional D7＋收斂線）、[`NARRATION-COPYEDIT-RUBRIC.md`](content_scripts/_audit/NARRATION-COPYEDIT-RUBRIC.md)（C1–C5＋「blocking 結構恆 0」）；兩支 template 改成引用 rubric、不複述。
3. **收斂線＋兩讀者＋phase**：REVIEW_GATES meta-gate 加「每閘 blocking==0」「gate2 只套 copyedit／NFA」「DRAFT/LOCKED phase」三條。
4. **視覺層** REVIEW_GATES 層 7 改寫成 figure-audit 鏡像兩列。
5. **§4 Register 放寬**＋§8 post-lock scoped NFA 回歸句（CONTENT_METHODOLOGY）。

> **NFA／copyedit 是純文檔抽取**（rubric 維度＝原 template 維度，行為應等價）；`VISUAL-FRAME-RUBRIC.md` 與 `CONTENT-SIXLENS-RUBRIC.md` 已於 2026-06-16 補寫——**四份判斷閘 SSOT rubric（NFA／copyedit／six-lens／VISUAL-FRAME）至此齊備**。

### code 回報層 normalize（2026-06-16 收尾，本輪實作）

原列為「待續・排在內容 backlog 後」，本輪一併落地，至此本重構無 open item：

6. **`critic.py` 接 VISUAL-FRAME-RUBRIC**：runtime verbatim-inject 整份 rubric body（`load_rubric()`；取代原 hardcoded 5 維 `RUBRIC` 常數，dimensions 自此只活在 rubric 檔），JSON schema／`_write_md` 改 V1–V9 blocking findings＋`VERDICT: <n> visual blocking` 行＋A1–A7 0–100 scores，修抽幀新鮮度（ffmpeg 前 `unlink`，失敗不留舊 PNG），定價改 MiMo 公測免費＝$0（dated；仍印 token 量＋受同意閘），stdout 改 UTF-8（防 Windows cp950 console 撞注入的中文 rubric），清 stale header。§1.1 真 `--dry-run` 驗過。
7. **`review_pack.py` 收斂為 engineering 鏡＋脫鉤 `.tex`**：faithfulness／register／decomposition 三鏡已被 CONTENT-SIXLENS 取代故移除（免平行第二套）；工程鏡 math context 改吃內容稿動畫單元的 narration／`source`（不重建 HTML parser）；定價標籤改 unverified estimate。§1.1 真 `--dry-run` 驗過（1 packet）。
8. **文檔同步**：[REVIEW_GATES.md](REVIEW_GATES.md) §五 stale 註記＋層 5／層 7 列已更新；[VISUAL-FRAME-RUBRIC.md](content_scripts/_audit/VISUAL-FRAME-RUBRIC.md) wiring 註改「已接線」；本檔狀態改「已採用·收尾」。

### 後續收尾（2026-06-16 大重設一併完成）

9. **engineering 鏡退場 DeepSeek、改 gate1 Claude／gate2 Codex**：與其餘判斷閘一致。`review_pack.py` 重寫為**離線 packet 組裝器**（無 API/key），新增 SSOT [`HOOK-ENGINEERING-RUBRIC.md`](content_scripts/_audit/HOOK-ENGINEERING-RUBRIC.md)（E1 數學保真 blocking＋E2 慣例、收斂＝engineering blocking==0）；gate1 Claude subagent 讀 packet、gate2 Codex 收斂後單次。**至此每道判斷閘都是 gate1 Claude →（散文/工程）gate2 Codex／（視覺）gate2 VLM 的一致形狀。**
10. **`schema.py` 已建**（render 前第三閘，接進 make.py：schema→lint→sizecheck）——原列產線 backlog，本輪完成。

> **仍屬產線 backlog（非本重構）：** VISUAL-FRAME detection 面驗證（併入第一個真正重跑的節）、`{show}` target-vs-payload 交叉驗證（task #6、需 manim）。續追 [REBUILD_STATUS.md](REBUILD_STATUS.md)。

---

## 九、修訂紀錄

- **2026-07-07 gate-2 頻率矩陣（部分修訂 §八拍板 2）：** 規模前提改變（從數節練習變 30+ 節量產）＋copyedit gate-2 歷史 findings 率低（blocking 結構恆 0 的純潤稿閘），經 Claude 主審＋Codex 兩輪對抗收斂：**copyedit gate-2 從「每節收斂後單次」改「每章抽樣＋出版前抽查、高風險節全跑」；NFA gate-2 維持每節**（§3.1 實證 gate-2 抓到 gate-1 漏的 D3 blocking）；amplification 改每章一次；工程鏡 gate-2 高風險才跑；視覺 VLM gate-2 維持間歇（高風險／出版前抽樣）。權威矩陣見 [REVIEW_GATES.md](REVIEW_GATES.md) meta-gate 8。其餘 §八拍板（copyedit/NFA 分離、six-lens 無 gate-2、不造狀態機）**不變**。

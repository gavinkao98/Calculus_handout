> **Status: archived / completed（2026-07-07 歸檔）** — 本計畫已落地：Vale lane＝advisory 預標（`ENVIRONMENT.md` §⑤b）、語意/聲音 S·A·V critic＝`handout/_audit/PROSE-AUDIT-RUBRIC.md` Dimension C。本檔為歷史施工紀錄，勿當現行流程；內含相對路徑可能已過時。

# 語意/聲音 critic Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL：用 superpowers:subagent-driven-development（推薦）或 superpowers:executing-plans 逐 task 實作。步驟用 `- [ ]` checkbox 追蹤。
>
> **本檔是什麼：** [`PLAN-deai-semantic-critic.md`](PLAN-deai-semantic-critic.md)（設計/決策）的逐 task 實作展開。設計層的「為什麼、判準、護欄」看 spec；本檔是「逐 task 怎麼做、怎麼驗、哪裡停下等 ⛳」。

**Goal：** 把 handout prose-audit 的 Dimension C 從「數 tell／密度」改鑄為「語意/聲音 critic（S/A/V）」，並以盲測驗證它真能分人/AI，再逐章 propose-only 套用。

**Architecture：** 收編進現有 `handout-prose-audit` subagent 的 C 槽（rubric 為單一真相來源，gate-2 Codex 自動繼承）；固定 2 正 1 負真人範本當 few-shot 錨；propose-only、使用者裁決、HTML 報告、回歸審核。Vale 降為免費護欄。

**Tech Stack：** Markdown rubric 契約、Claude subagent（gate 1）＋ Codex（gate 2）、Python stdlib（盲測 tally 腳本）、既有 build/HTML 報告機器。平台 win32（PowerShell 主、Bash 可用）。

---

## 實作進度與結果（2026-06-26，跨對話狀態錨）

> **本輪落地範圍：偵測機制（Tasks 1–7）＋ Task 8 的 Ch1，全部完成並經雙審驗證；Ch2–Ch4 待續。** 下一輪從 Task 8 的 Ch2 接手即可（critic 已凍結、穩定）。

| Task | 狀態 | 重點 |
|---|---|---|
| 1 錨組 | ✅ 完成 | 2 正（OpenStax §2.2 limit、§3.1 derivative）1 負（自撰 AI-default）；⛳ 使用者 bless（derivative 取 A，local-linearity）。檔：`handout/_audit/anchors/svc-exemplars.md` |
| 2 rubric C→S/A/V | ✅ 完成 | `PROSE-AUDIT-RUBRIC.md` Dimension C 改鑄；blocking 線＝空句佔承載位（S1/S3）或 A2。**＋V1 寬報校準（⛳ 拍板：中性但可更暖也報 advisory、never blocking）** |
| 3 agent 收編 | ✅ 完成 | `handout-prose-audit.md` 三維化、載入錨組 |
| 4 盲測分離 ⛳ | ✅ 通過 | 見下「驗證結果」。`tools/deai/separation_tally.py`＋`REVIEW-svc-separation-test.html` |
| 5 pilot ⛳ | ✅ 通過 | §1.4，0 blocking、克制過關 |
| 6 §3 voice corpus 換真人 | ✅ 完成 | ⛳ 採 **option (c)**：四型全換真人（OpenStax/CLP，CC BY-NC-SA），破 Ch1 循環。`CONTENT_SPEC.md` §3＋`REVIEW-svc-voicecorpus-applied.html` |
| 7 退役舊機制 | ✅ 完成 | Vale 降級護欄（`CONTENT_DIRECTION.md` ⑤）、刪 2 過時 voicecorpus html、`REVIEW-ch02-deai-gate1.html` 加退役註 |
| 8 逐章鋪 | 🔶 **Ch1 完成、Ch2–4 待續** | **Ch1：gate-1（Claude）＋gate-2（Codex）雙審皆 0 blocking**；套用 6 條 advisory 改進（§1.2/§1.3/§1.4/§1.5×2/§1.6×2，§1.1 全 keep），逐節回歸通過、build 全綠。per-節 `REVIEW-ch01-svc-gate1-sec-*.html`＋`REVIEW-ch01-svc-gate2.html` |

**驗證結果（核心信任檢查）：**
- **盲測分離 PASS：** empty（刻意空泛 AI-default）vs substantive（真人＋好 AI＋bare vanilla）**29.7× 分離**、blocking-only **完美分離**（11 段實質散文零 blocking、3 段空泛全被 blocking 重咬，踩對 S1/S3/A2/V1）。
- **重要 reframe（修正 spec §5.1 框架）：** vanilla LLM 在「limit/derivative」這類好走主題上**本身就言之有物**，與真人**不可分**（實證 spec §0「中性≠AI」）——所以可驗證、critic 真能分的軸是 **「空 vs 實」**，不是「AI vs 人」。本 critic 驗的是**空泛偵測＋過度-flag 防護**，這正是 Task 8 的職責。
- **Ch1 雙審 0 blocking 的意義：** 推翻舊 metric「Ch1 是 AI 灌水」（em-dash 密度高只是 OpenStax 不愛 em-dash 的假象）；Ch1 一直是好的人類編修內容，新語意 critic 只找到少量暖度/實質 polish。

**下一輪接手：** Task 8 的 Ch2（§2.1–§2.5）→ Ch3 → Ch4，一次一節，同 gate-1（±gate-2）→ ⛳ 逐條裁決 → 回歸 流程。rubric/錨/agent 已凍結，不需再動。

---

## Global Constraints（每個 task 隱含包含）

- **目標＝積極（難以分辨人類），但路徑是語意層編輯、瞄 §3 既定調**；中性≠AI，中性+空才是 AI（spec §0）。
- **critic 唯讀、propose-only**；套用獲准改寫時**保語意、不動數學、不碰教學順序與選題**（copyedit 級硬護欄）。
- **絕不**用 AI-detector 機率分數；Vale 永遠 flag-only。
- **語料只用 BY／BY-NC／BY-NC-SA**，逐段標來源（排除 BY-SA）。
- **Commit 政策**：依 CLAUDE.md，當輪未經要求不擅自 commit；各 task 末 commit step 取得授權後才執行；訊息繁中、結尾加 `Co-Authored-By` trailer。
- **每個 ⛳ 停下等使用者拍板**；門檻/措辭一律提案＋推薦值。

---

## File Structure（先鎖定分解）

**新增：**
- `handout/_audit/anchors/svc-exemplars.md` — 固定錨組（2 正 1 負）＋逐段標來源/授權＋「為何正/負」註解。被 rubric 與 critic prompt 消費。
- `tools/deai/separation_tally.py` — 盲測 tally：吃各 passage 的 critic findings 數＋字數，算 S/A findings per 500，輸出人/AI 分離度。
- `handout/_audit/REVIEW-svc-separation-test.html` — 盲測驗證報告（交付物）。
- `handout/_audit/REVIEW-svc-pilot-<sec>.html` — pilot 單節審核稿。
- `.tmp/svc-benchmark/`（gitignored）— 盲測用 AI-default 正例＋真人負例原文（只量測、不 vendored）。

**修改：**
- `handout/_audit/PROSE-AUDIT-RUBRIC.md` — Dimension C：C1–C6（tell/密度）→ S/A/V。
- `.claude/agents/handout-prose-audit.md` — 描述/指引更新為三維 A/B/C-recast、載入錨組。
- `CONTENT_SPEC.md` §3 — 4 段 Ch1 範文 → 2 段真人正面範本。
- `CONTENT_DIRECTION.md` ⑤ — Vale 標「降級護欄」。

**刪除：**
- `handout/_audit/REVIEW-deai-voicecorpus-candidates.html`、`handout/_audit/REVIEW-deai-voicecorpus-applied.html`（Ch1 voice corpus，已過時）。

---

## Task 1：組裝並 bless 錨組（2 正 1 負）⛳

**Files：** Create `handout/_audit/anchors/svc-exemplars.md`

**Interfaces：** Produces 固定錨組，被 Task 2 rubric 與 critic prompt 引用；2 正同時當 §3 voice corpus 替換（Task 6 消費）。

- [ ] **Step 1：挑 2 段真人正面範本（register 貼 §3、確定真人、NOT Ch1）。** 起手用本輪已抓的 `.tmp/deai-corpus/openstax-limit.md`、`openstax-derivative.md`（OpenStax Calculus Vol.1，CC BY-NC-SA），各取最具代表性的 ~1 paragraph（80–150 字）。為每段寫一句「為何是 substance/altitude/voice 的正面標靶」。
- [ ] **Step 2：寫 1 段負面範本（AI-default 空泛）。** 直接用下列草稿（刻意堆 tell 又空，當對比錨）：

> The derivative is a fundamental and powerful concept that plays a crucial role in calculus. It is important to note that the derivative measures the rate of change of a function. In this section, we will explore how the derivative works and why it is so essential. By understanding the derivative, we unlock a deeper appreciation of how functions behave. Let us now delve into the details — at its core, the derivative captures the essence of change itself.

  附註：標出它踩了哪些測試（S1 空、S2 通用填充、A1 嘮叨顯而易見、V 假暖無實質），當「該被 flag 長這樣」的示範。

- [ ] **Step 3：寫 `svc-exemplars.md`**：頂部一句用途（critic few-shot 錨＋§3 voice 標靶）；三段各含〔來源/授權〕〔正/負〕〔為何〕〔verbatim 內文〕。OpenStax 兩段標 `[source: OpenStax Calculus Vol.1, CC BY-NC-SA, §2.2/§3.1]`。
- [ ] **Step 4：⛳ 使用者 bless 錨組**（範本＝那把尺，spec §3）。等使用者確認三段入選（或要求換更暖/topic-matched）。
- [ ] **Step 5：Commit**（授權後）

```bash
git add handout/_audit/anchors/svc-exemplars.md
git commit -m "feat(deai): 語意 critic 固定錨組（2 正 1 負真人範本）"
```

---

## Task 2：改鑄 PROSE-AUDIT-RUBRIC 的 Dimension C 為 S/A/V

**Files：** Modify `handout/_audit/PROSE-AUDIT-RUBRIC.md`

**Interfaces：** Consumes Task 1 錨組。Produces 新 C 維度契約；gate-1（Claude）＋ gate-2（Codex）因單一真相來源自動繼承。

- [ ] **Step 1：把「### C. 語聲 AI-texture（密度觸發…）」整段（C1–C6＋擋稿線＋密度天花板）刪除**，換成 spec §2 的 **S/A/V** 全文（S1–S3、A1–A2、V1、兩個防呆、self-relative altitude、強制附證據、中性不扣分）。逐字以 spec §2 為準。
- [ ] **Step 2：在 C 維度末加「錨組」一句**：`gate 跑 S/A/V 時，prompt 末尾掛 handout/_audit/anchors/svc-exemplars.md（2 正 1 負），對著正面 bar 判、把負面當「該 flag 長這樣」。`
- [ ] **Step 3：改「擋稿線（blocking vs advisory）」總表**：移除「C 維度的高密度叢集（≥3 distinct…）」；改為「**S/A 的 blocking＝該句空（S1/S3 成立且該句承載教學功能卻無實質）或高度錯（A2 跳過真難步）**；其餘 S/A/V 為 advisory」。（具體 blocking 線以 spec §2 措辭為準；起始從嚴、寧少報。）
- [ ] **Step 4：改「收斂判準」**：該節 C 通過＝S/A 的 blocking findings = 0；advisory 不強制歸零。
- [ ] **Step 5：更新「回報規格」VERDICT 行**：`VERDICT: <B> blocking, <T> tighten, <O> optional, <V> voice`（移除 `<X> AI-texture`）；逐條格式加「踩哪測試（S#/A#/V#）＋一行為什麼＋改寫/刪」。
- [ ] **Step 6：驗證（一致性人讀）**：A/B 維度與護欄段未被破壞；§3-protected 清單仍在（鼓勵連接詞等不誤砍）；無殘留 C1–C6/em-dash/密度字樣。
- [ ] **Step 7：Commit**（授權後）

```bash
git add handout/_audit/PROSE-AUDIT-RUBRIC.md
git commit -m "feat(deai): Dimension C 改鑄為語意/聲音 S/A/V（取代 tell/密度）"
```

---

## Task 3：更新 handout-prose-audit subagent 指引

**Files：** Modify `.claude/agents/handout-prose-audit.md`

- [ ] **Step 1：讀現有 agent 定義**，確認它「讀 PROSE-AUDIT-RUBRIC 判斷」。若其描述/system prompt 明列「易懂性＋流暢性」兩維，補成「易懂性 A＋流暢性 B＋語意/聲音 C（S/A/V）」，並指明「跑 C 時載入 `handout/_audit/anchors/svc-exemplars.md` 當錨」。
- [ ] **Step 2：驗證**：措辭與 rubric 一致、唯讀/propose-only 護欄不變（人讀）。
- [ ] **Step 3：Commit**（授權後）

```bash
git add .claude/agents/handout-prose-audit.md
git commit -m "feat(deai): handout-prose-audit 收編 S/A/V 維度＋錨組"
```

---

## Task 4：盲測分離驗證（核心信任檢查）⛳ gate

**Files：** Create `.tmp/svc-benchmark/`（gitignored 原文）、`tools/deai/separation_tally.py`、`handout/_audit/REVIEW-svc-separation-test.html`

**Interfaces：** Consumes Task 2/3 的 critic。Produces 分離度數據；**不過關＝critic 是噪音 → 回 Task 2 改 rubric/錨**。

- [ ] **Step 1：組 benchmark**（存 `.tmp/svc-benchmark/`，與錨組**不重複**防洩漏）：
  - 正例 3–4 段：vanilla prompt（`Write a short textbook section explaining <topic>.`）生的 AI-default 數學散文（topic 用 limits/derivative/chain rule）。
  - 負例 3–4 段：真人段——OpenStax 其他節＋CLP（`.tmp/deai-corpus/clp-limit.md` 可用），**非錨組那兩段**。
- [ ] **Step 2：寫 `separation_tally.py`（先寫期望斷言）**：吃一個 `{passage_id: {label, words, sa_findings}}` 的 JSON，算各 passage 的 S/A findings per 500，輸出兩組平均並斷言 `mean(AI) > mean(human)` 且分離倍數 ≥2×。先放假資料跑一次確認腳本邏輯對。
- [ ] **Step 3：遮標籤跑 critic**：對 benchmark 每段派 `handout-prose-audit`（只收 S/A findings 數），**prompt 不告知該段是人是 AI**。收集成 JSON 餵 `separation_tally.py`。
- [ ] **Step 4：判定**：
  - 分得開（AI S/A findings 明顯多、真人近 0）→ 過關，進 Task 5。
  - 分不開或誤報真人 → **回 Task 2** 調 S/A 措辭/錨組，重跑本 task。
- [ ] **Step 5：產 `REVIEW-svc-separation-test.html`**：正/負各段、S/A findings、分離倍數、判定。⛳ 使用者看過認可 critic 可信。
- [ ] **Step 6：Commit**（授權後；`.tmp/` 不入版控）

```bash
git add tools/deai/separation_tally.py handout/_audit/REVIEW-svc-separation-test.html
git commit -m "feat(deai): 語意 critic 盲測分離驗證（人/AI 分離度）"
```

---

## Task 5：pilot 單節 ⛳

**Files：** Create `handout/_audit/REVIEW-svc-pilot-<sec>.html`；唯讀不改 fragment。

- [ ] **Step 1：選一節**（建議 Ch2 的某節，或使用者指定），派 `handout-prose-audit`（A/B/C-recast＋錨）跑。
- [ ] **Step 2：產 pilot REVIEW html**，逐條 S/A/V findings（踩哪測試＋為什麼＋改寫/刪）。
- [ ] **Step 3：⛳ 使用者看順**：findings 是否中肯、有無誤傷中性好句、改寫品質。不順→回 Task 2 微調。
- [ ] **Step 4：Commit**（授權後）

```bash
git add handout/_audit/REVIEW-svc-pilot-<sec>.html
git commit -m "chore(deai): 語意 critic pilot 單節審核稿"
```

---

## Task 6：§3 voice corpus 換真人

**Files：** Modify `CONTENT_SPEC.md` §3

**Interfaces：** Consumes Task 1 的 2 段正面範本。

- [ ] **Step 1：撤掉 Task 2.4 放的 4 段 Ch1 範文**（§3「語聲參考範文」），換成 Task 1 的 2 段真人正面範本，各標關鍵特徵（substance/altitude/voice）＋來源/授權。
- [ ] **Step 2：驗證**：verbatim 自來源（核對）；§3 register 規範文字未動（只換範本）。
- [ ] **Step 3：Commit**（授權後）

```bash
git add CONTENT_SPEC.md
git commit -m "feat(deai): §3 voice corpus 換真人範本（撤 Ch1 循環標靶）"
```

---

## Task 7：退役舊機制＋cleanup

**Files：** Delete 2 個 voicecorpus html；Modify `CONTENT_DIRECTION.md` ⑤

- [ ] **Step 1：刪除過時 voice corpus 審核稿**：

```bash
git rm handout/_audit/REVIEW-deai-voicecorpus-candidates.html handout/_audit/REVIEW-deai-voicecorpus-applied.html
```

- [ ] **Step 2：`CONTENT_DIRECTION.md` ⑤** 把 Vale AItexture 那句改標「**降級為免費 pre-flag 護欄（預期 ~0），決定性偵測在 S/A/V 人審 critic，非此 lane**」。
- [ ] **Step 3：（紀錄）** `REVIEW-ch02-deai-gate1.html`：其 A/B findings 仍有效、C 部分（em-dash 等）已退役——於檔頂加一行註記指向本計畫，不刪（保 A/B 紀錄）。
- [ ] **Step 4：Commit**（授權後）

```bash
git add CONTENT_DIRECTION.md handout/_audit/REVIEW-ch02-deai-gate1.html
git commit -m "chore(deai): 退役舊 metric 偵測＋Vale 降級護欄＋清過時 voice corpus"
```

---

## Task 8：逐章鋪 Ch1–Ch4（per-section ⛳ loop）

> 「用 critic」階段。對 Ch1（⛳#1 已重開，入清掃）、Ch2、Ch3、Ch4 逐節重複：

- [ ] **Step 1：派 `handout-prose-audit`（A/B/C-recast＋錨）審該節**，收 S/A blocking ＋ advisory。
- [ ] **Step 2：產 `REVIEW-ch0N-svc-gate1.html`**（比照 pilot 格式）。
- [ ] **Step 3：⛳ 使用者逐條裁決改寫/刪**（propose-only）。套用獲准小修，**保語意/不動數學**。
- [ ] **Step 4：回歸審核**（CLAUDE.md 2026-06-12）：對改過的節重跑，確認未引入新問題，記錄於審核稿。
- [ ] **Step 5：（可選）gate-2 Codex** 同 rubric 再審，出 `REVIEW-ch0N-svc-gate2.html`。
- [ ] **Step 6：重組並 Commit**（授權後）

```bash
python handout/build.py ch0N
git add handout/fragments/ch0N/ handout/_audit/REVIEW-ch0N-svc-gate1.html
git commit -m "fix(deai): ch0N 語意收斂（S/A 空句/高度修，propose-only 裁決）"
```

> 對 Ch1、Ch2、Ch3、Ch4 各跑一次本 task。Ch1 因 ⛳#1 重開納入。

---

## Self-Review（作者自審）

- **Spec coverage：** spec §1→Tasks 全域；§2（S/A/V）→Task 2；§3（錨）→Task 1（＋Task 6 共用正例）；§4（機制）→Task 2/3；§5（驗證）→Task 4（盲測）＋Task 5（pilot）；§6（退役/scope）→Task 6/7；§8 落地→Task 1–8 對應。涵蓋完整。
- **Placeholder 掃描：** `<sec>`／`ch0N` 為刻意的 per-instance 佔位（執行時填實際節/章）；負面範本、`separation_tally.py` 斷言、rubric 改鑄內容均給實質。無漏填。
- **一致性：** `svc-exemplars.md`／`S/A/V`／`S#/A#/V#`／`REVIEW-…-svc-…`／`separation_tally.py` 全檔一致。
- **⛳ 點：** Task 1 Step 4（錨 bless）、Task 4 Step 5（critic 可信）、Task 5 Step 3（pilot 看順）、Task 8 Step 3（逐節裁決）——皆停下等使用者。

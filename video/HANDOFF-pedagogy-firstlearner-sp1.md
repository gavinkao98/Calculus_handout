# 初學者教學＋OTF 框架 — 進度交接

> 交接時間：2026-06-30。分支：`video/template-redesign-navy-spine`。
> 權威 spec：[`SPEC-pedagogy-firstlearner-framework.md`](SPEC-pedagogy-firstlearner-framework.md)（v3, SHIP）。
> 施工計畫：[`PLAN-pedagogy-firstlearner-sp1-foundation.md`](PLAN-pedagogy-firstlearner-sp1-foundation.md)（Plan 1）、[`PLAN-pedagogy-firstlearner-sp1-plan2-scaffold.md`](PLAN-pedagogy-firstlearner-sp1-plan2-scaffold.md)（Plan 2）。
> 跨對話進度錨仍是 [`REBUILD_STATUS.md`](REBUILD_STATUS.md)；本檔是「回家接手」用的單張 resume 卡。
> **全程離線、未動任何計費 API。** 流程：`superpowers:subagent-driven-development`，task-by-task，每 task 過 spec＋品質雙閘 review。

SP1 共 5 個 Plan。目前 **Plan 1 ✅ 完成、Plan 2 邏輯階段 ✅ 完成、Plan 2 渲染階段待做、Plans 3–5＋SP2 未開始**。

---

## 一、已完成（已 commit，在分支上）

### Plan 1 — OTF provenance 基礎 ✅（9 commits，`cd7a01b..b3bf68c`，merge-ready）

確定性 provenance 層：上畫面教學文字可回溯到核准源。

- **`pipeline/provenance.py`**：ref 文法 `md:<unit_id>`／`doc:<frag-sec-*|data-fig>`、locus 載入 `Loci.from_deck`（fail-closed）、resolver `Loci.resolves`、場級繼承＋欄級覆寫的 `scene_text_refs`、warn/error 檢查 `provenance_issues`（intro/outro 豁免）。
- **接線**：warn-only 接進 `pipeline/schema.py main()` ＋ `make.py` render gate；僅 `meta.otf_enforce: true` 才 gating。**零行為改變**（無 deck 設旗標）。
- **測試**：`pipeline/_selftest_provenance.py`（stdlib assert）＋ fixture `storyboards/_fixtures/otf_provenance.yml` ＋ backing `content_scripts/_fixture_otf.md`。
- **文法定案（你過目裁決）**：`ref:`/`refs:` 為新欄位、與 freeform `source:` 分離；`subtitle` 豁免（brand），divider 教學文字走 `problem`/`scaffold.problem`。
- **review**：全分支 opus review = merge **Yes**；過程抓到 1 個 Critical（provenance 原本在 render path 跑不到，已接進 make.py）＋若干 Important，全修＋回歸 clean。
- **durable 教訓**：① 確定性檢查**必須接進 `make.py` render gate**（make.py 呼叫純函式 `schema_storyboard()`、不呼叫 `schema.main()`）。② `repo_root` 深度：`schema.py` 在 `video/pipeline/` 用 `.parent.parent.parent`；`make.py` 在 `video/` 用 `.parent.parent`。③ self-test 一律用 venv python（vendored PyYAML）。

### Plan 2 — scaffold 模型＋模板：邏輯階段 ✅（Tasks 1–3，`b3bf68c..101fd80`，含計畫文件）

PD 確定性層（教學結構檢查），全部 warn-default。

- **`pipeline/pedagogy.py`**（新）：`assumptions_registry_issues`（PD4 registry 一致性）＋ `pedagogy_issues`（PD2 = theorem_proof/derivation 缺 `scaffold.motive`；PD3 = divider 缺 `scaffold.problem`；`pedagogy_profile` 驗證；末了呼叫 PD4）。壞輸入 fail-closed。`definition_math` 的 motive **不**入確定性集（spec §9.2，屬 gate-1 advisory）。
- **接線**：warn-only 接進 `schema.py main()` ＋ `make.py` render gate；僅 `meta.pedagogy_enforce: true` 才 gating（**獨立於** `otf_enforce`，你裁決的）。**零行為改變**——ch03 `schema.py` exit 0，印 `[schema] OK` ＋ `[provenance] 18 warn` ＋ `[pedagogy] 14 warn`。
- **測試**：`pipeline/_selftest_pedagogy.py`（7 個 stdlib assert）＋ fixture `storyboards/_fixtures/scaffold.yml`。
- **review**：每 task 過 spec＋品質雙閘；抓到並修掉 1 個 Important（非 dict 輸入 fail-closed 護欄）。

**Plan 2 commit 對照**：`6d7defa`(T1) · `9c755fc`(T2 impl) · `3f7d56d`(計畫文件) · `e295a58`(T2 fix) · `101fd80`(T3)。

---

## 二、還沒做（Plan 2 渲染階段 — 下一步，已 GATED 等你）

細節在 [`PLAN-pedagogy-firstlearner-sp1-plan2-scaffold.md`](PLAN-pedagogy-firstlearner-sp1-plan2-scaffold.md) 的 Task 4、Task 5（含 exact code／hook 行號／驗證協定）。

- **Task 4 — `render_scaffold()` helper**（改 `pipeline/templates/_common.py`）：把 `scaffold.motive`／`problem`／`flag` 渲成 static Block（motive＝標題下 `role="text" size="prose_sm"` 小行，**不可 muted**；problem＝divider 標題下公式塊；flag＝從 `meta.assumptions` 查 text 的小 badge）。缺 scaffold 一律回 `[]`（no-op）。
- **Task 5 — 模板接線**（改 `definition_math.py`／`theorem_proof.py`／`derivation.py`／`divider.py`）：各模板在 `scene_head()` 後呼 `render_scaffold`、定位於標題下、append Block。**缺 scaffold → no-op → 既有 deck 渲染不變。**
- **驗證（為何 GATED）**：渲染無法純 assert 測 → 走 **mock render（離線免費）→ critic.py 抽幀 → visual-frame-audit gate（V1–V9/A1–A7）→ 你 sign-off**（比照 hook 動畫 sign-off 文化）。這是版面微調的活，計畫裡的 per-template code 是 hook 行號＋pattern，實作時要對著 render 調 buff。

- **Plan 2 final whole-branch review**：Tasks 4–5 落地後，跑一次 Plan 2 全分支 opus review（比照 Plan 1）；屆時一併裁決下方「待 final review 的小項」。

---

## 三、將來要做（Plans 3–5 ＋ SP2；尚未細化成施工計畫）

依 spec §12 ＋ 兩份 plan 文件末尾清單。Plans 3–5 與 Plan 2 一樣，**待前一 Plan 落地後才細化成 task-by-task 施工計畫**（沿用 writing-plans → subagent-driven-development）。

- **Plan 3 — pedagogy gate（判斷層）**：`PEDAGOGY-FIRSTLEARNER-RUBRIC.md`（PD1–PD4 ＋ OF1–OF2）＋ `pedagogy-firstlearner-audit` gate-1 subagent（讀 storyboard＋.md＋handout）；OF1 source-adequacy 判斷；`CONTENT_APPROVED` 生命週期 gating；PD/OF 分開計數。（gate-1 agent 直接讀 `meta.pedagogy_profile`。）
- **Plan 4 — 視覺擴充**：A7 figure-prominence 子準則（量測）、V4/A6 最小字級 floor 常數（`theme.py`/`sizecheck.py`）、手機標尺（`VISUAL-FRAME-RUBRIC.md`）。
- **Plan 5 — methodology／文件接線**：`CONTENT_METHODOLOGY.md`（P1/P2/P4 ＋ scaffold authoring）、`DESIGN.md`（scaffold 承載＋authoring checklist）、`CONTENT-SIXLENS-RUBRIC.md`（L1 scaffold 例外措辭）、`REVIEW_GATES.md`（新閘入序）、V1–V8→V1–V9 doc-drift。
- **SP2 — 回填**：把 SP1（Plans 1–4）套到 3 個既有 deck（ch01 §1.1、ch03 §3.1/§3.2），走 spec §11「乾跑 → 分類 → 你核可遷移清單 → scoped 修」。**注意**：場級繼承讓回填收斂，但 Plan 1 文法決定 `ref:`/`refs:` 是**新欄位**（不沿用 freeform `source:`），故每個 OTF-subject 場仍需新增 `ref:` ＋ 寫 freeform→`md:`/`doc:` 對映。

---

## 四、怎麼接手（resume 指南）

- **流程**：`superpowers:subagent-driven-development`，task-by-task。下一步直接做 Plan 2 Task 4（計畫文件已 ready，BASE = 當前 HEAD）。
- **測試**：一律用 `C:/Users/user/Desktop/Calculus_handout/.venv/Scripts/python.exe`（bare python 缺 vendored PyYAML 會誤判 `test_schema_integration`）。
- **快速健檢**：
  - `…/.venv/…/python.exe video/pipeline/_selftest_provenance.py` → `OK provenance self-test`
  - `…/.venv/…/python.exe video/pipeline/_selftest_pedagogy.py` → `OK pedagogy self-test`
  - `…/.venv/…/python.exe video/pipeline/schema.py video/storyboards/ch03_trig_derivatives.yml` → exit 0 ＋ `[provenance]`／`[pedagogy]` warn block（零行為改變的回歸）。
- **渲染驗證**：mock render（`make.py --backend mock`，離線免費）→ `critic.py` 抽幀 → `visual-frame-audit` gate。**計費 API（真 TTS／高解析渲染）動之前一定先報價徵你同意**（CLAUDE.md 規則）。
- **逐步 blow-by-blow**：SDD 執行 ledger 在 `.superpowers/sdd/progress.md`——**但它是 gitignored、只在本機，不隨 git 走**（換機看不到，本檔才是跨機交接）。

---

## 五、⚠️ 工作樹未提交的東西（換機不會跟著走！）

git 只帶走**已 commit**的東西。以下目前**未 commit**，換到家裡機器前若不處理就會留在這台：

1. **你的「音樂/音效候選包」WIP**：`video/DESIGN.md`、`video/README.md`、`video/REBUILD_STATUS.md` 的改動 ＋ 未追蹤的 `video/pipeline/assets/audio/house/`（4 個 house WAV ＋ `generate_house_cues.py` ＋ README ＋ `REVIEW-house-audio-candidates.html`）。**要保留 → 先 `git add` + `git commit`。** 我全程一字未動。
2. **我幫你貼進 `REBUILD_STATUS.md` 的 Plan 1 ✅ 段（＋下方新增的 Plan 2 段）**：也未 commit——因為同一檔含上述音檔 WIP，**commit 邊界留你**（你決定要不要跟音檔一起提交，或先 stash 音檔讓那段單獨提交）。
3. **本交接文件**（`video/HANDOFF-pedagogy-firstlearner-sp1.md`）＋ **Plan 2 計畫文件**：**已 commit**（乾淨、獨立），會隨 push 到家。

## 六、待 Plan 2 final review 的小項（已記，非 blocking）

- `provenance_issues`（Plan 1）的 `data.get("scenes")` 對非 dict 輸入未 guard（`pedagogy_issues` 已修）→ final review 時兩個 warn-only 檢查的非 dict guard 一起對齊。
- `make.py` 的 `[pedagogy]` abort idiom（`if _ped_err and _ped_enforce:`）與 `[provenance]`（`if _p_err:`）對齊（去掉冗餘 `and _ped_enforce`）。
- 其餘 Plan 1／Plan 2 各 task 的 cosmetic Minor 已逐條記在 `.superpowers/sdd/progress.md`（本機）。

## 七、跨機帶走清單（TL;DR）

1. 要讓家裡機器拿到：**`git push`** 分支 `video/template-redesign-navy-spine`（committed 的 Plan 1/2 ＋ 本交接文件才會過去）。
2. 未 commit 的（音檔 WIP ＋ REBUILD_STATUS 編輯）**先 commit 才會跟著走**，否則留在這台。
3. 回家後：`git pull` → 讀本檔「四、怎麼接手」→ 從 Plan 2 Task 4 續做。

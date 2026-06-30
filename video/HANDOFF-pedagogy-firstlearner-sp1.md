# 初學者教學＋OTF 框架 — 進度交接

> 交接時間：2026-06-30。分支：`video/template-redesign-navy-spine`。
> 權威 spec：[`SPEC-pedagogy-firstlearner-framework.md`](SPEC-pedagogy-firstlearner-framework.md)（v3, SHIP）。
> 施工計畫：[`PLAN-pedagogy-firstlearner-sp1-foundation.md`](PLAN-pedagogy-firstlearner-sp1-foundation.md)（Plan 1）、[`PLAN-pedagogy-firstlearner-sp1-plan2-scaffold.md`](PLAN-pedagogy-firstlearner-sp1-plan2-scaffold.md)（Plan 2）。
> 跨對話進度錨仍是 [`REBUILD_STATUS.md`](REBUILD_STATUS.md)；本檔是「回家接手」用的單張 resume 卡。
> **全程離線、未動任何計費 API。** 流程：`superpowers:subagent-driven-development`，task-by-task，每 task 過 spec＋品質雙閘 review。

SP1 共 5 個 Plan。目前 **Plan 1 ✅、Plan 2 ✅ 完整完成（邏輯＋渲染＋polish，全分支 opus review = merge-ready）、Plan 3 為下一步、Plans 4–5＋SP2 未開始**。

> **2026-06-30 續做完成 Plan 2 渲染階段＋全分支 review＋使用者視覺 sign-off。** 新增 commits（接在 `253fe64` 後）：`c3e0d33`（baseline 修）→ `7e18e09`（T4 helper）→ `a0a29bc`（T5 接線）→ `194a8eb`（polish：孤行 `)`＋divider）→ `a9e5203`（§6 對齊）→ `d05f240`（null-meta fail-closed）→ `d88f137`（進度錨）→ `c879d7e`（sign-off：ASSUMES badge `RAIL_W`→`PRIMARY_W`）→ `58722e1`（sign-off：motive `PRIMARY_W`→`CONTENT_W`，皆解「太早換行、右邊空間沒用上」）。詳見 [`REBUILD_STATUS.md`](REBUILD_STATUS.md)「scaffold 模型＋模板渲染（SP1 Plan 2）完成」段。

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

## 二、Plan 2 渲染階段 ✅ 完成（Tasks 4–5＋polish＋全分支 review = merge-ready）

> 2026-06-30 續做完成。Task 4/5 的 exact code／pattern 仍在 [`PLAN-pedagogy-firstlearner-sp1-plan2-scaffold.md`](PLAN-pedagogy-firstlearner-sp1-plan2-scaffold.md)（歷史參照）。

- **Task 4 `render_scaffold()` helper**（commit `7e18e09`，`pipeline/templates/_common.py`）＋ **Task 5 模板接線**（`a0a29bc`，4 模板）：`scaffold.motive`（標題下 `role="text"` 小行，不 muted）／`problem`（divider 公式塊）／`flag`（ASSUMES badge）渲成 static Block，缺 scaffold → `[]` → no-op。spec＋品質雙閘 review 皆過；**no-op 不變式經全分支 review base-vs-HEAD 全幾何 diff 證實 byte-identical**。
- **視覺 sign-off（比照 hook 動畫文化）：** `scratch_frames.py` mock render 4 模板 1080p 幀 → `visual-frame-audit` gate V1–V9＝0 blocking → 使用者核可「全 polish」→ polish（`brand._wrap_mixed` 推廣尾標點黏合含閉括號 `)]}`，解 ASSUMES badge 孤行 `)`＋divider buff/style，`194a8eb`）→ 回歸 audit 0 blocking、A1 兩幀升。
- **全分支 opus review = merge-ready**；findings 全處理：§6 兩對齊項（`a9e5203`）＋ review 抓到的 null／非 dict `meta` fail-closed bug（4 處 meta 抽取點對齊＋self-test，`d05f240`）。
- **下一步＝Plan 3**（見下節三）。

---

## 三、將來要做（Plans 3–5 ＋ SP2；尚未細化成施工計畫）

依 spec §12 ＋ 兩份 plan 文件末尾清單。Plans 3–5 與 Plan 2 一樣，**待前一 Plan 落地後才細化成 task-by-task 施工計畫**（沿用 writing-plans → subagent-driven-development）。

- **Plan 3 — pedagogy gate（判斷層）**：`PEDAGOGY-FIRSTLEARNER-RUBRIC.md`（PD1–PD4 ＋ OF1–OF2）＋ `pedagogy-firstlearner-audit` gate-1 subagent（讀 storyboard＋.md＋handout）；OF1 source-adequacy 判斷；`CONTENT_APPROVED` 生命週期 gating；PD/OF 分開計數。（gate-1 agent 直接讀 `meta.pedagogy_profile`。）**→ 施工計畫已出（2026-06-30）：[`PLAN-pedagogy-firstlearner-sp1-plan3-gate.md`](PLAN-pedagogy-firstlearner-sp1-plan3-gate.md)（5 task：rubric→agent→fixture→校準→sign-off；純 markdown＋校準、無新 Python，gate-1 blocking＝PD1＋OF1，PD2/3/4＋OF2 為已落地確定性層）。下一步直接跑 Task 1。**
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

## 六、Plan 2 final review 小項 — ✅ 全數處理（2026-06-30）

- ✅ `provenance_issues` 非 dict guard：已對齊 `pedagogy_issues`（commit `a9e5203`，並加 self-test 斷言）。
- ✅ `make.py` `[pedagogy]` abort idiom：去冗餘 `and _ped_enforce`、對齊 `[provenance]` 的 `if _p_err:`（`a9e5203`）。
- ✅ 全分支 review 另抓到 **null／非 dict `meta` 會 crash**（違反模組 fail-closed docstring，不變式 4 部分破口）：4 處 meta 抽取點（`pedagogy.py`×2／`schema.py`／`make.py`）統一 null-safe＋self-test（`d05f240`，順帶關 `schema.py` 同根 Plan-1 gap）。
- 維持 won't-fix（reviewer 判定非 blocking）：PD4 重複 assumption id 靜默接受（opt-in advisory 層、低衝擊）；content 模板「置中 hero」留白（共用 body 擺放＋scratch 內容極簡，硬改破 no-op）。其餘 cosmetic Minor 全集附錄見下方。

## 七、跨機帶走清單（TL;DR）

1. 要讓家裡機器拿到：**`git push`** 分支 `video/template-redesign-navy-spine`（committed 的 Plan 1/2 ＋ 本交接文件才會過去）。
2. 未 commit 的（音檔 WIP ＋ REBUILD_STATUS 編輯）**先 commit 才會跟著走**，否則留在這台。
3. 回家後：`git pull` → 讀本檔「四、怎麼接手」→ 從 Plan 2 Task 4 續做。

---

## 附錄 — Minor findings 全集（cosmetic／低優先，給 Plan 2 final whole-branch review 參考）

> 這些原本只記在本機 gitignored ledger（`.superpowers/sdd/progress.md`）；為免換機遺失，搬進此版控文檔。**多數 won't-fix**（比照既有風格／harmless）；final whole-branch review 也會自行 re-derive。**真正 actionable 的兩項在「六」**（非此附錄）。

**Plan 1（provenance）：**
- `provenance.py` `parse_ref` 正則 `(\S.*)`＋`.strip()` 接受 token 內空白（plan 規定；harmless，這種 ref 永不 resolve）；要收緊改 `(\S+)`。
- `provenance.py` `parse_ref` 回傳註解加引號 `"tuple[str,str]|None"`，在 `from __future__ import annotations` 下冗餘。
- `_selftest_provenance.py` `test_loci(tmp_md,tmp_handout)` 參數未用（vestigial）；`from_deck` 無常駐 unit test（smoke 涵蓋，設計如此）。
- `provenance.py` `from_deck` 中段 import（brief 規定；PEP8 會提到頂）。
- `provenance.py` `from_deck` 的 `except Exception: pass` 靜默——壞 `.md` → 空 md units 無 stderr 提示（spec-correct warn-only；加一行 stderr warn 利除錯）。
- `_selftest_provenance.py` `scene_text_refs` 的 `points` 欄＋list-path ref 值未斷言（只測 `annotations`）。
- `provenance.py` `scene_text_refs` 的 `isinstance(ref,str)` belt-and-suspenders（harmless）。
- `_selftest_provenance.py` `assert "ok" not in msgs` 鬆散 substring（`"ok."` 較穩）。
- `otf_provenance.yml` fixture 無 `divider` 場（membership 由 `test_constants` 護；與 content 同分支）。
- `schema.py` `main()` 內 local import＋`_Path` alias（合既有 deferred-import 風格；alias 或冗餘）。
- `_selftest_provenance.py` 複合否定斷言（`ok_inherited`＋`intro` 同一 assert）。

**Plan 2（pedagogy）：**
- `pedagogy.py` 結尾換行；空-id 場排除（defensible）；docstring 提 PD2/PD3 為 forward-decl。
- `_selftest_pedagogy.py` PEP8 空行。
- `make.py` `[pedagogy]` 的 `if _ped_err and _ped_enforce:` 冗餘（vs `[provenance]` 的 `if _p_err:`）→ 已列「六」的 actionable 對齊項。

> 此附錄落地後，**所有跨機該留的紀錄都在版控文檔內**；`.superpowers/sdd/progress.md` 維持本機 gitignored scratch（不需移出），其逐步 log 僅供同機／同 session 回復用。

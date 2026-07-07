> **Status: archived / completed（2026-07-07 歸檔）** — 本計畫已全數落地（執行紀錄見 `video/_archive/REBUILD_LOG-2026-05-to-07.md` 對應節）。活的權威見 `video/REVIEW_GATES.md`／`video/DESIGN.md`／`video/SPEC-pedagogy-firstlearner-*.md`。本檔為歷史施工紀錄，內含相對路徑可能已過時。

# SP2 回填（ch03 兩 deck）施工計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把已落地的 SP1 框架（OTF provenance `ref:`/`refs:`、PD scaffold `motive`/`problem`/`flag`＋assumptions registry、視覺 font-floor）回填到兩個既有 ch03 deck（§3.1 `ch03_trig_derivatives`、§3.2 `ch03_chain_rule`），把三個 per-deck opt-in flag 從 warn 翻成 gating（`otf_enforce`／`pedagogy_enforce`／`fontfloor_enforce: true`），且不破壞既有視覺與 narration。

**Architecture:** 走 SPEC [§11](SPEC-pedagogy-firstlearner-framework.md) 回填骨架——**共用乾跑＋分類＋使用者核可遷移清單**（Phase A，一次涵蓋兩 deck），再**逐 deck scoped 修 → 回歸 → 視覺 sign-off → 翻 flag**（Phase B＝§3.1、Phase C＝§3.2），最後收文件（Phase D）。每個改動只動**該 deck 的 `.yml`**，不動共用模板／工具／rubric／另一 deck／`.md`／handout。全程離線免費；任何計費 API（真 TTS、高解析渲染、Codex 覆核）動前先報價徵同意。

**Tech Stack:** storyboard YAML、`pipeline/{schema,sizecheck,provenance,pedagogy}.py`（純 stdlib 檢查，**唯讀引用、不改**）、`make.py --backend mock`（離線渲染）、`critic.py --dry-run`／`scratch_frames.py`（抽幀）、gate-1 subagent `pedagogy-firstlearner-audit`＋`visual-frame-audit`＋`narration-faithfulness-audit`（唯讀稽核）。Python 一律用 **repo 內** `.venv/Scripts/python.exe`（換機自動對；本機絕對路徑 `C:/Users/Kao/Downloads/Calculus_handout/.venv/Scripts/python.exe`，找不到先跑 `python tools/doctor.py`）。

> **Shell 慣例（執行紀律，Codex B3 校正）：** 本計畫所有 shell 片段為 **Git Bash（Bash 工具）語法**——POSIX、forward-slash 路徑、`VENV=…`／`"$VENV"`／`rm -rf`。執行者一律**用 Bash 工具**跑（與 REBUILD_STATUS 既有慣例一致）；若改用 PowerShell 需自行轉換（`$VENV = "…/python.exe"`；`& $VENV …`；`Remove-Item -LiteralPath … -Recurse -Force`）。**所有 `make.py`／`critic.py` 呼叫都帶 `--storyboard <deck>.yml`（兩者 `required=True`）。**

---

## 0 · As-built 事實（照 code，勿照 SPEC 舊 prose）

SPEC／部分舊 prose 早於 Plan 1–4 落地，**以下以 landed code 為準**（Plan 5 文件接線時 Codex 已連抓數處 spec-vs-code 落差）：

- **provenance 文法（[`pipeline/provenance.py`](pipeline/provenance.py)）：** 機器可解析欄位是 **`ref:`（場級，被所有上畫面教學文字欄位繼承）/ `refs:`（欄級覆寫，flat map）**。`refs:` 的 key 是**欄位路徑字串**（如 `refs: { scaffold.motive: 'md:foo', 'steps.0.reason': 'doc:bar' }`），**非巢狀物件**——巢狀會被 `scene.refs.get("scaffold.motive")` silently 漏掉。ref 文法＝`md:<unit_id>`（`.md` 單元 id）或 `doc:<anchor>`（handout `id="frag-sec-*"`／`data-fig="*"`）。freeform `source:` 是**人讀標籤、永不解析**，兩 deck 既有的 `source:` 全部留著不動。
- **上畫面教學文字欄位（`TEACHING_TEXT_FIELDS`／`_present_text_fields`）：** `statement`／`problem`／`body`／`reason`／`prompt`／`scaffold.motive`／`scaffold.problem`／`annotations[]`／`points[]`，**以及巢狀** `steps[].reason`／`result.reason`／`check.reason`／`lines[].reason`（derivation rail，真實 deck 大量用，2026-06-30 已補掃）。**不在內**：`math`／`steps[].math`／`result.math`／`proof[]`／`qed`／graph 軸標／曲線 label／`title`／`eyebrow`／`kicker`／`subtitle`（brand），及 hook 自繪文字（歸工程／視覺閘）。
- **OTF 觸發 kind：** `content`＋`divider`；`intro`／`outro` 豁免。divider 若**無** `problem`／`scaffold.problem`，其 OTF 上畫面欄位集合為空（不出 OF2）；但缺 `scaffold.problem` 由 **PD3** 另計。
- **PD 確定性層（[`pipeline/pedagogy.py`](pipeline/pedagogy.py)）：** PD2＝`content`＋`template ∈ {theorem_proof, derivation}` 缺 `scaffold.motive`；PD3＝`kind: divider` 缺 `scaffold.problem`；PD4＝`meta.assumptions[]` registry 一致性（每筆 `{id,text,first_use_unit,source}`、`first_use_unit` 須為真場 id 且該場帶 `scaffold.flag: <id>`、無孤兒 flag）。`meta.assumptions` 缺省→PD4 零發現。`meta.pedagogy_profile` 缺省＝`first_time`（合法值 `first_time`/`review`/`expert`）。`definition_math` **不**入 PD2 確定性必填集。
- **三個 opt-in flag 獨立、預設關（warn/dry-run）：** `meta.otf_enforce`（→ provenance 升 error，[`schema.py`](pipeline/schema.py)）、`meta.pedagogy_enforce`（→ pedagogy 升 error，`schema.py`）、`meta.fontfloor_enforce`（→ font-floor 升 error，[`sizecheck.py`](pipeline/sizecheck.py)）。三者落地當下對既有 deck 零行為改變。`schema.py main()` 任何 error 才 exit 1；`if prov:`／`if ped:` 只在有 finding 時印區塊。
- **gate-1 `pedagogy-firstlearner-audit` 計數約定（rubric 已鎖）：** `VERDICT: <P> PD blocking, <O> OF blocking, <A> advisory` 的整數**只計 gate-1 自有的 PD1＋OF1**；PD2/3/4＋OF2 結構存在性由確定性層（`schema.py`）擁有並各自 gating，agent 以 `[Surface PD#-det|OF2-det]` 列出、**不進整數**。OF lifecycle：cited `.md` `CONTENT_APPROVED=yes` 時 OF 才 blocking；`md:<unit>` 繼承 deck 核准狀態，`doc:<anchor>` 一旦解析即可 gate。
- **font-floor 現況：** `MIN_FONT_FLOOR=26px`；REBUILD_STATUS 記載三 deck（含本 ch03 兩 deck）各 **0 floor false positive**——故 `fontfloor_enforce` 翻 true 預期是 **0-surface no-op**（仍須乾跑複驗）。
- **scaffold 渲染契約（[`DESIGN.md`](DESIGN.md)，[`_common.render_scaffold`](pipeline/templates/_common.py)）：** `scaffold.motive` → 標題下一行較小的 `text` role（**不可 `muted`**，否則違反「教學內容非 muted」＋觸 sizecheck muted-prose warn）；`divider` 的 `scaffold.problem` → 標題下「**純 `$math$` 走顯示公式行**、純文字則 wrap」；`scaffold.flag: <id>` → ASSUMES badge。**缺 `scaffold` 一律 no-op**。⚠️ **加 `scaffold.motive`/`problem`/`flag` 會改變 render**（不是 no-op）→ 必須 mock 重渲＋視覺 sign-off；加 `ref:`/`refs:` 是純 metadata（render no-op）。
- **兩 deck `CONTENT_APPROVED=yes`（locked）：** §3.1 detail-redo（2026-06-29 sign-off）、§3.2（2026-06-29 sign-off）。**NFA 禁止改已認可 source**——OF1 忠實修**只動 storyboard 的上畫面文字欄位，絕不動 `.md`**。

---

## 1 · 範圍（使用者已裁決）

**只做 ch03 兩 deck：**
- §3.1 = [`storyboards/ch03_trig_derivatives.yml`](storyboards/ch03_trig_derivatives.yml)（26 場：1 intro＋4 divider＋20 content＋1 outro）。
- §3.2 = [`storyboards/ch03_chain_rule.yml`](storyboards/ch03_chain_rule.yml)（27 場：1 intro＋**3** divider＋22 content＋1 outro；3 幕結構 progress n/3，故 divider 比 §3.1 少一個）。

**明確不做：** ch01 §1.1（`ch01_inverse_functions.yml`）**完全不動**。

**不得觸碰（scoped 紀律，Karpathy 外科手術式）：** 共用模板（`templates/`）、確定性工具（`provenance.py`/`pedagogy.py`/`schema.py`/`sizecheck.py`/`theme.py`）、rubric／agent 定義、另一 deck、任何 `.md` 內容稿、handout。**每一行改動只能落在被回填那一個 `.yml`**（＋ Phase D 的進度文件）。

---

## 2 · 檔案結構（會建立／修改什麼）

| 路徑 | 動作 | 責任 |
|------|------|------|
| `storyboards/ch03_trig_derivatives.yml` | 修（Phase B） | 加 `ref:`/`refs:`、`scaffold.motive`/`problem`、（若核可）`meta.assumptions`＋`scaffold.flag`、OF1 忠實修、末了翻三 flag |
| `storyboards/ch03_chain_rule.yml` | 修（Phase C） | 同上 |
| `content_scripts/_audit/REVIEW-ch03-sp2-migration.html` | 建（Task 3） | 遷移清單＋四級分類＋決策項，standalone HTML 供使用者核可 |
| `content_scripts/_audit/REVIEW-ch03_trig_derivatives-sp2-applied.html` | 建（Task 5） | §3.1 回填 applied 報告（逐場改動＋閘結果＋末幀） |
| `content_scripts/_audit/REVIEW-ch03_chain_rule-sp2-applied.html` | 建（Task 8） | §3.2 回填 applied 報告 |
| `REBUILD_STATUS.md`／`HANDOFF-pedagogy-firstlearner-sp1.md` | 修（Phase D） | SP2 完成進度錨＋durable 教訓 |

> HTML 報告比照既有 `REVIEW-*-applied.html`（MathJax/KaTeX CDN、雙擊即開、數學即渲染）。產生器若不可廉價重生（含 base64 幀）存 tracked `_gen/`，比照 §3.2 Stage-2 報告慣例。

---

## 3 · 候選 ref 對映（Task 2 的預期產出，已先導出供計畫具體化）

**機械化預設規則（最小化 per-scene 決策）：**
- **content 場 → `ref: md:<scene_id>`**：兩 deck 的**每個** content 場都有**同名 `.md` unit**（已 grep 驗證：§3.1 `.md` 22 unit＝20 content＋intro/outro、§3.2 `.md` 24 unit＝22 content＋intro/outro，scene id ＝ unit id），故場級 `ref: md:<同名>` 一律解析得到。
- **divider 場 → `ref: doc:frag-sec-3-1`（§3.1）/ `doc:frag-sec-3-2`（§3.2）**：divider 不在 `.md`，其待加的 `scaffold.problem` 走 handout section anchor（`doc:<anchor>` 一旦解析即可 gate，不靠 deck 核准）。
- **欄級 `refs:` 覆寫**：只在 OF1 source-adequacy 要求時補（見下「決策項」）——預設**不**逐欄補。

**§3.1（`ch03_trig_derivatives`）— 待動的 content/divider 場：**

| 場 id | kind/template | 上畫面教學欄位 | 場級 `ref:` | 待加 scaffold |
|---|---|---|---|---|
| divider_limit | divider | （加 problem 後） | `doc:frag-sec-3-1` | `scaffold.problem` |
| why_trig_is_different | content/definition_math | statement | `md:why_trig_is_different` | —（definition_math，PD2 不必填） |
| difference_quotient_for_sine | content/derivation | steps.0–2.reason, result.reason | `md:difference_quotient_for_sine` | `scaffold.motive` |
| divider_squeeze | divider | （加 problem 後） | `doc:frag-sec-3-1` | `scaffold.problem` |
| sector_inequality | content/graph | —（無 present OTF 欄；title=brand、曲線 label 非 OTF） | `md:sector_inequality`（選用） | — |
| squeeze_to_the_bound | content/derivation | steps.0–1.reason, result.reason, check.reason | `md:squeeze_to_the_bound` | `scaffold.motive` |
| continuity_statement_sin_limit | content/theorem_proof | statement | `md:continuity_statement_sin_limit` | `scaffold.motive` |
| continuity_argument | content/theorem_proof | statement | `md:continuity_argument` | `scaffold.motive` |
| fundamental_limit | content/theorem_proof | statement | `md:fundamental_limit` | `scaffold.motive` |
| squeeze_graph | content/graph | annotations.0（唯一 OTF 欄；無 statement） | `md:squeeze_graph` | — |
| limit_not_identity | content/callout | body | `md:limit_not_identity` | — |
| radians_essential | content/callout | body | `md:radians_essential` | （決策：radians registry first_use flag） |
| divider_derivatives | divider | （加 problem 後） | `doc:frag-sec-3-1` | `scaffold.problem` |
| derivative_of_sine | content/theorem_proof | statement | `md:derivative_of_sine` | `scaffold.motive` |
| derivative_of_cosine | content/theorem_proof | statement | `md:derivative_of_cosine` | `scaffold.motive` |
| slope_equals_height | content/graph | —（無 present OTF 欄） | `md:slope_equals_height`（選用） | — |
| derivative_cycle | content/definition_math | statement | `md:derivative_cycle` | — |
| divider_apply | divider | （加 problem 後） | `doc:frag-sec-3-1` | `scaffold.problem` |
| companion_limit | content/derivation | prompt, steps.0–1.reason, result.reason | `md:companion_limit` | `scaffold.motive` |
| all_six_trig_derivatives | content/derivation | prompt, steps.0–1.reason, check.reason | `md:all_six_trig_derivatives` | `scaffold.motive` |
| shm_compute | content/derivation | prompt, steps.0–2.reason, result.reason | `md:shm_compute` | `scaffold.motive` |
| shm_stacked_graphs | content/graph | —（無 present OTF 欄） | `md:shm_stacked_graphs`（選用） | — |
| toward_the_chain_rule | content/definition_math | statement | `md:toward_the_chain_rule` | — |
| recap | content/recap_cards | points.0–3 | `md:recap` | —（source-adequacy 決策，見下） |

§3.1 待加：**4 個 `scaffold.problem`**（divider）＋**10 個 `scaffold.motive`**（derivation×5：difference_quotient_for_sine／squeeze_to_the_bound／companion_limit／all_six_trig_derivatives／shm_compute；theorem_proof×5：continuity_statement_sin_limit／continuity_argument／fundamental_limit／derivative_of_sine／derivative_of_cosine）＝符合乾跑預期 PD3=4＋PD2=10＝14 pedagogy warn。

**§3.2（`ch03_chain_rule`）— 待動的 content/divider 場：**

| 場 id | kind/template | 上畫面教學欄位 | 場級 `ref:` | 待加 scaffold |
|---|---|---|---|---|
| divider_rule | divider | （加 problem 後） | `doc:frag-sec-3-2` | `scaffold.problem` |
| why_composition_is_missing | content/definition_math | statement | `md:why_composition_is_missing` | — |
| rates_multiply_intuition | content/definition_math | statement | `md:rates_multiply_intuition` | — |
| chain_rule_statement | content/definition_math | statement | `md:chain_rule_statement` | —（definition_math，雖 kicker:theorem 仍不必填） |
| composed_mapping_figure | content/graph | —（無 present OTF 欄） | `md:composed_mapping_figure`（選用） | — |
| leibniz_form | content/definition_math | statement | `md:leibniz_form` | — |
| decomposition_strategy | content/procedure_steps | —（無 present OTF 欄：`steps[].text` 不掃、無 statement/reason） | `md:decomposition_strategy`（選用） | —（procedure_steps 非 PD2 集） |
| divider_why | divider | （加 problem 後） | `doc:frag-sec-3-2` | `scaffold.problem` |
| proof_strategy_bridge | content/definition_math | statement | `md:proof_strategy_bridge` | — |
| remainder_form_definition | content/definition_math | statement | `md:remainder_form_definition` | — |
| remainder_tangent_figure | content/graph | —（無 present OTF 欄） | `md:remainder_tangent_figure`（選用） | — |
| two_forms_equivalent | content/theorem_proof | statement | `md:two_forms_equivalent` | `scaffold.motive` |
| proof_setup_substitution | content/theorem_proof | statement | `md:proof_setup_substitution` | `scaffold.motive` |
| proof_easy_piece | content/theorem_proof | statement | `md:proof_easy_piece` | `scaffold.motive` |
| proof_delicate_choices | content/theorem_proof | statement | `md:proof_delicate_choices` | `scaffold.motive` |
| proof_delicate_bound | content/theorem_proof | statement | `md:proof_delicate_bound` | `scaffold.motive` |
| divider_use | divider | （加 problem 後） | `doc:frag-sec-3-2` | `scaffold.problem` |
| example_single_composition | content/derivation | prompt, steps.0–1.reason, result.reason | `md:example_single_composition` | `scaffold.motive` |
| caution_inner_derivative | content/callout | body | `md:caution_inner_derivative` | — |
| example_nested_three_layers | content/derivation | prompt, steps.0–1.reason, result.reason | `md:example_nested_three_layers` | `scaffold.motive` |
| example_chain_times_quotient | content/derivation | prompt, steps.0–1.reason | `md:example_chain_times_quotient` | `scaffold.motive` |
| example_chain_times_product | content/derivation | prompt, steps.0–1.reason, result.reason | `md:example_chain_times_product` | `scaffold.motive` |
| example_leibniz_rates | content/derivation | prompt, steps.0–1.reason, result.reason | `md:example_leibniz_rates` | `scaffold.motive` |
| toward_section_3_3 | content/definition_math | statement | `md:toward_section_3_3` | — |
| recap | content/recap_cards | points.0–3 | `md:recap` | —（source-adequacy 決策） |

§3.2 待加：**3 個 `scaffold.problem`**（divider）＋**10 個 `scaffold.motive`**（theorem_proof×5＋derivation×5）＝符合乾跑預期 PD3=3＋PD2=10＝13 pedagogy warn。

> **注（無 present OTF 欄的場 — Codex D1/D2 校正）：** `_present_text_fields`（[`pipeline/provenance.py:86`](pipeline/provenance.py)）只掃**實際存在**的教學文字欄位（statement/problem/body/reason/prompt/scaffold.motive·problem/annotations[]/points[]＋巢狀 reason），**不掃** graph 的 `title`／軸標／曲線 label、`steps[].text`、`math`、`proof[]`、`qed`。故 **graph 場 `sector_inequality`/`slope_equals_height`/`shm_stacked_graphs`/`composed_mapping_figure`/`remainder_tangent_figure`**（皆無 `statement`）與 **`decomposition_strategy`**（steps 為 `{text,math}`、無 reason）目前**無 present OTF 欄 → 不出 OF2、不強制需 `ref:`**；表中標「（選用）」的場級 `ref:` 是 uniform／future-proof（加了 harmless，不加也不出 finding），由 Task 3 裁。**`squeeze_graph` 唯一 OTF 欄是 `annotations.0`**（有別於其他圖場，必須補可解析 ref）。**Task 1 乾跑印出的確切欄位集為準，校正本表。**

**圖場 `md:` vs `doc:` 選擇：** 預設 `md:<scene_id>`（與 narration 源一致、統一）。6 個 figure 場另有 handout `data-fig` anchor 可選（`doc:sector-inequality`/`squeeze-limit`/`sin-cos-slope`/`shm-triple`/`composed-mapping`/`remainder-tangent`）——若某圖場的 `annotations`/`statement` 是**圖專屬斷言**、`md:` unit 講不到，遷移清單可改用或補 `doc:` 欄級覆寫。預設不改。

---

## 4 · 決策項（Task 3 遷移清單須讓使用者裁決）

這些不是確定性閘逼出來的，是**教學增強／忠實判斷**，攤開讓使用者定奪（Karpathy §1）：

- **D-A〔§3.1 radians assumptions registry〕**：§3.1 全節依賴 radians（`sector_inequality` 的 ½θ、`radians_essential` caution）。PD4 registry **缺省＝零發現**，故加它是**選擇**、非閘逼。加 `meta.assumptions:[radians]`＋在 first_use 場渲 `scaffold.flag: radians`（候選 first_use＝`sector_inequality`，最早載重用到 ½θ；或 `why_trig_is_different`，say 最早提 radians）→ 滿足 P4「前提首用即標」，但**會多一個 ASSUMES badge（改 render）**、需視覺 sign-off。**選項：(a) 加 registry＋flag（P4 增強）／(b) 不加（PD4 維持 clean）。** §3.2 無對應的全域隱含前提。
- **D-B〔recap source-adequacy〕**：兩 deck 的 `recap` 場 `ref: md:recap`，而 `md:recap` 是 whole-section synthesis 單元。recap 的 `points` 復述具體已證結果（fundamental limit、兩導數、chain rule 等）。若 OF1 判 `md:recap` 過寬、無法 specifically 支持某 point → 須補**欄級 `refs:`** 指向該結果的本尊 unit（如 `refs: { points.0: 'md:fundamental_limit' }`）。Task 1 gate-1 乾跑會判定；遷移清單列出需覆寫的 points。
- **D-C〔OF1 忠實 findings〕**：上畫面文字多由同源 `.md` 衍生，OF1 預期大致 clean；但乾跑若發現某上畫面文字**超出／矛盾** cited 源 → 遷移清單列出，修法＝**改 storyboard 上畫面文字**（縮回源範圍或改正），**絕不動 `.md`**（NFA 護欄）。
- **D-D〔PD1 beat 粒度〕**：gate-1 自有判斷。兩 deck 經 detail-redo／full-ε-δ-split 精心拆過、已過六鏡＋視覺閘，PD1 預期 clean；若乾跑出 PD1 blocking（單一 reveal 壓 >1 承重動作）→ 屬**較大改動**（要拆 `{show}` beat、可能動 `say:`／narration → 觸 NFA），遷移清單獨立標示、由使用者裁決是否納入本輪 SP2 或另案。
- **D-E〔motive/problem 文字定稿〕**：`scaffold.motive`/`problem` 的**實際英文文字**是內容撰寫（OF1 會查其忠實於 cited 源）。Task 3 遷移清單**逐場附 draft 文字**供使用者過目；Task 4/7 只 apply 已核可文字。品質 bar 見 §6 worked example。

---

## Phase A — 共用乾跑＋分類＋遷移清單（兩 deck，止於使用者核可閘）

### Task 1: 兩 deck 基線乾跑（收集全部 surface）

**Files:**
- 唯讀：`storyboards/ch03_trig_derivatives.yml`、`storyboards/ch03_chain_rule.yml`
- 產出：scratchpad 暫存乾跑輸出（不進 repo）

- [ ] **Step 1: schema.py 乾跑兩 deck（provenance＋pedagogy warn-checks）**

```bash
VENV="C:/Users/Kao/Downloads/Calculus_handout/.venv/Scripts/python.exe"
"$VENV" video/pipeline/schema.py video/storyboards/ch03_trig_derivatives.yml
"$VENV" video/pipeline/schema.py video/storyboards/ch03_chain_rule.yml
```

Expected（**零行為改變回歸**，flag 未翻）：兩者 **exit 0**；印 `[schema] ... structure OK`＋`[provenance] ... (warn-only; set meta.otf_enforce to gate)` 區塊＋`[pedagogy] ... (warn-only; set meta.pedagogy_enforce to gate)` 區塊。§3.1 pedagogy 預期 **14 warn**（PD2×10＋PD3×4）；§3.2 預期 **13 warn**（PD2×10＋PD3×3）。provenance warn 數＝各 deck 全部上畫面教學欄位數（每欄一條「no provenance ref」）。**逐字記下** provenance／pedagogy 每一條 message。

- [ ] **Step 2: sizecheck.py 乾跑兩 deck（font-floor，warn-default）**

```bash
"$VENV" video/pipeline/sizecheck.py video/storyboards/ch03_trig_derivatives.yml
"$VENV" video/pipeline/sizecheck.py video/storyboards/ch03_chain_rule.yml
```

Expected：兩者 **exit 0**（0 error）；**僅**全無 finding 才印 `consistent`，**有**既有 within-frame advisory（§3.1/§3.2 REBUILD_STATUS 記錄的 qed 越界類）則印 `[sizecheck] …: 0 error(s), M warning(s)`＋逐條 `WARN`（仍 exit 0，Codex D4）。**font-floor 預期 0 finding**（三 deck 0 false positive）。若出現任何 `MIN_FONT_FLOOR ... < 26px` 即記下（罕見、與預期不符要查）。**MiKTeX 冷快取若拋 `PermissionError`／「could not build scene」→ 重跑**（暖快取即正常，非真缺幀）。

- [ ] **Step 3: dispatch gate-1 `pedagogy-firstlearner-audit` 兩 deck（PD1–PD4＋OF1–OF2）**

對每個 deck 各 dispatch 一次（Agent tool，subagent_type `pedagogy-firstlearner-audit`）。prompt 須含：deck `.yml` 路徑、cited `.md` 路徑（`content_scripts/<deck>.md`）、handout（`handout/chapter3-print-standalone.html`）、**`CONTENT_APPROVED=yes`**（兩 deck 皆 locked）。

Expected：各回一段 `VERDICT: <P> PD blocking, <O> OF blocking, <A> advisory`。當下 deck **尚無 `ref:`** → OF1 無 cited 源可比（對空集合）、OF2 由確定性層 surface（`[Surface OF2-det]` 逐欄列）；PD2/3/4 以 `[Surface PD#-det]` 列出；gate-1 自有 **PD1／OF1 預期 0 或極少**。**逐條記下** PD1／OF1 findings 與所有 `[Surface ...]`。

- [ ] **Step 4: 把三來源 surface 彙整成一張原始表（scratchpad）**

每個 finding 標：deck、場 id、欄位／beat、來源閘（schema-provenance／schema-pedagogy／sizecheck-floor／gate1-PD1／gate1-OF1／gate1-surface）、原始 message。此表是 Task 3 分類的輸入。**本 task 不改任何檔。**

---

### Task 2: provenance locus 盤點＋候選 ref 對映確認

**Files:**
- 唯讀：兩 `.md`（unit id）、`handout/chapter3-print-standalone.html`（anchor）

- [ ] **Step 1: 列出可解析 locus（與 §3 候選表交叉驗證）**

```bash
# .md unit id（md:<unit_id> 的解析目標）
grep -n "^### unit:" video/content_scripts/ch03_trig_derivatives.md
grep -n "^### unit:" video/content_scripts/ch03_chain_rule.md
# handout anchor（doc:<anchor> 的解析目標）
grep -oE 'id="(frag-sec-3[A-Za-z0-9-]*)"|data-fig="([A-Za-z0-9-]+)"' handout/chapter3-print-standalone.html
```

Expected：§3.1 `.md` 22 unit、§3.2 `.md` 24 unit（皆含 intro/outro）；anchor 含 `frag-sec-3-1`/`frag-sec-3-2`/`frag-sec-3-3`＋`data-fig` sector-inequality/squeeze-limit/sin-cos-slope/shm-triple/composed-mapping/remainder-tangent。確認 §3 候選表每個 `md:<scene_id>` 與 `doc:<anchor>` 都在清單內（即都解析得到）。

- [ ] **Step 2: 確認對映（用 provenance.py resolver 抽驗）**

對每 deck 載入 `Loci.from_deck` 抽驗幾個代表 ref 解析為 True：

```bash
"$VENV" -c "import sys; sys.path.insert(0,'video'); from pipeline import provenance as p; from pathlib import Path; import yaml,io; m={'id':'ch03_trig_derivatives','chapter':'Chapter 3'}; L=p.Loci.from_deck(m, Path('.').resolve()); print('md:sector_inequality',L.resolves('md:sector_inequality')); print('doc:frag-sec-3-1',L.resolves('doc:frag-sec-3-1')); print('doc:sector-inequality',L.resolves('doc:sector-inequality')); print('md:nope',L.resolves('md:nope'))"
```

Expected：前三 `True`、最後 `False`。對 `ch03_chain_rule`（`md:chain_rule_statement`／`doc:frag-sec-3-2`／`doc:composed-mapping`）重複。若任何預期 True 解析為 False → 修正 §3 對映表再進 Task 3。**本 task 不改任何檔。**

---

### Task 3: 四級分類＋遷移清單（standalone HTML）→ 使用者核可閘

**Files:**
- Create: `content_scripts/_audit/REVIEW-ch03-sp2-migration.html`

- [ ] **Step 1: 把 Task 1 原始表分四級**（CLAUDE.md review 四級）

① **真 blocker（migration-required）**：opt-in 後會擋稿者——缺 `ref:`（OF2-det）、缺 `scaffold.motive`/`problem`（PD2/PD3-det）、registry 不一致（PD4-det）、gate-1 OF1 矛盾/超出源、gate-1 PD1 多動作 beat。② **discoverability**：補文件即可、非矛盾（本輪罕見，多已在 Plan 5 接好）。③ **drift 風險**：低優先、非 finding。④ **非 finding**：既有 within-frame advisory（qed 越界）、乾淨維度、brand 文字。**不 over-report。**

- [ ] **Step 2: 產遷移清單**（每個真 blocker 一列）

逐列：deck、場 id、待動欄位、**確切改法**（場級 `ref: md:<id>`／`doc:<anchor>`、欄級 `refs:` 覆寫、`scaffold.motive`/`problem` 的 **draft 文字**、registry entry、OF1 reword 文字）、來源閘、級別。draft motive/problem 文字逐場附上（品質 bar 見 §6）。**含 §4 決策項**（D-A radians registry：給 (a)/(b) 兩案；D-B recap 需覆寫的 points；D-C OF1 reword；D-D 任何 PD1）。

- [ ] **Step 3: 估清回填量＋scoped 邊界聲明**

寫明：§3.1／§3.2 各要加幾個 `ref:`（場級）、幾個欄級 `refs:` 覆寫、幾個 `scaffold.motive`/`problem`、是否加 registry、幾條 OF1 reword。聲明**只動兩 `.yml`**、不動 `.md`/模板/工具/另一 deck。

- [ ] **Step 4: 出 standalone HTML（MathJax/KaTeX CDN）＋ stable finding 編號**

比照 [`REVIEW-ch01_inverse_functions-codex-polish.html`](content_scripts/_audit/REVIEW-ch01_inverse_functions-codex-polish.html) 形式：分 deck、分級、逐 finding 帶穩定編號、draft 文字數學即渲染、決策項以選項呈現。

- [ ] **Step 5: 交付使用者核可（HARD GATE）**

把 HTML 交給使用者裁決遷移清單（哪些 deck、哪些場/欄要動、決策項 D-A~D-E 怎麼定）。**未核可不得進 Phase B/C 的任何編輯。** （可選、計費：經同意後 Codex 覆核遷移清單，比照 SP1。）

---

## Phase B — §3.1 `ch03_trig_derivatives` scoped 修 → 回歸 → sign-off → 翻 flag

> 前置：Task 3 遷移清單**已核可**。只動 `storyboards/ch03_trig_derivatives.yml`。

### Task 4: §3.1 scoped 修（provenance → pedagogy → OF1，逐閘 checkpoint）

**Files:**
- Modify: `storyboards/ch03_trig_derivatives.yml`

- [ ] **Step 1: 加場級 `ref:`（先做，讓後加的 scaffold 欄位也被繼承覆蓋）**

依核可表，對每個 content 場在 `kind:` 附近加一行（content＝`md:<scene_id>`、divider＝`doc:frag-sec-3-1`）。例（`difference_quotient_for_sine`）：

```yaml
  - id: difference_quotient_for_sine
    kind: content
    template: derivation
    accent: definition
    kicker: derivation
    ref: md:difference_quotient_for_sine        # <-- 新增（OTF 場級，被所有上畫面教學文字欄位繼承）
    source: "chapter3-print-standalone.html SS3.1 . The difference quotient for sine (sum-to-product)"  # 既有 freeform，留著
```

對 `divider_limit`/`divider_squeeze`/`divider_derivatives`/`divider_apply` 加 `ref: doc:frag-sec-3-1`。

- [ ] **Step 2: 加核可的欄級 `refs:` 覆寫（若有，flat map）**

只對 D-B/D-C 核可需覆寫者。例（recap 某 point 指本尊 unit）：

```yaml
    refs:
      points.0: md:fundamental_limit
      points.1: md:derivative_of_sine
```

⚠️ **flat map、key 是欄位路徑字串、非巢狀**（`refs: { points.0: ... }`，不可 `refs: { points: { 0: ... } }`）。

- [ ] **Step 3: 驗 provenance 歸零**

```bash
"$VENV" video/pipeline/schema.py video/storyboards/ch03_trig_derivatives.yml
```

Expected：exit 0；**不再印 `[provenance]` 區塊**（0 finding）。`[pedagogy]` 區塊仍在（scaffold 未加）。若仍有 provenance finding → 該欄 ref 缺失/不解析，補齊再驗。

- [ ] **Step 4: 加 `scaffold.motive`（10 場）＋ `scaffold.problem`（4 divider），用核可文字**

content 場（derivation/theorem_proof）標題區加 `scaffold: { motive: "<核可文字>" }`；divider 加 `scaffold: { problem: "<核可文字>" }`。例：

```yaml
  - id: difference_quotient_for_sine
    ...
    ref: md:difference_quotient_for_sine
    scaffold: { motive: "Transform the difference quotient into a product we can take limits of, one factor at a time." }
```

```yaml
  - id: divider_squeeze
    kind: divider
    ...
    ref: doc:frag-sec-3-1
    scaffold: { problem: "$\\tfrac12\\sin\\theta \\le \\tfrac12\\theta \\le \\tfrac12\\tan\\theta$" }
```

`scaffold.motive`/`problem` 繼承場級 `ref:`（Step 1 已加）→ 不另需 `refs:`，除非該文字 cite 不同 locus（OF1）。**motive 不可 muted**（render 契約）。

- [ ] **Step 5:（若 D-A 核可加 radians registry）加 `meta.assumptions`＋first_use flag**

```yaml
meta:
  id: ch03_trig_derivatives
  ...
  assumptions:
    - id: radians
      text: "$\\theta$ in radians (arc length $=\\theta$, sector area $=\\tfrac12\\theta$)"
      first_use_unit: sector_inequality       # 核可的 first_use 場
      source: doc:frag-sec-3-1
```

並在 `sector_inequality` 場加 `scaffold: { flag: radians }`（與既有/新增 motive 並存於 scaffold map）。

- [ ] **Step 6: 驗 pedagogy 歸零**

```bash
"$VENV" video/pipeline/schema.py video/storyboards/ch03_trig_derivatives.yml
```

Expected：exit 0；**不再印 `[provenance]` 也不再印 `[pedagogy]` 區塊**（皆 0 finding）。若仍有 pedagogy finding → 對照訊息補齊（缺 motive/problem、registry flag 不對應）。

- [ ] **Step 7: OF1 忠實修（若 D-C 核可有，storyboard 文字 only）**

只改該上畫面文字欄位（縮回源範圍／改正），**絕不動 `.md`**。改完進 Task 5 由 gate-1 複驗。

- [ ] **Step 8: commit（scoped）**

```bash
git add video/storyboards/ch03_trig_derivatives.yml
git commit -m "video(ch03 §3.1): SP2 backfill -- OTF refs + PD scaffold + OF1 (pre-flip)"
```

---

### Task 5: §3.1 回歸＋mock 重渲＋視覺/忠實稽核 → 使用者 sign-off

**Files:**
- 唯讀稽核；Create: `content_scripts/_audit/REVIEW-ch03_trig_derivatives-sp2-applied.html`

- [ ] **Step 1: 確定性閘回歸**

```bash
"$VENV" video/pipeline/schema.py   video/storyboards/ch03_trig_derivatives.yml   # exit 0、無 prov/ped 區塊
"$VENV" video/pipeline/sizecheck.py video/storyboards/ch03_trig_derivatives.yml   # exit 0、0 error（既有 within-frame advisory warn 會印，非 'consistent'）
"$VENV" video/pipeline/lint.py     video/storyboards/ch03_trig_derivatives.yml    # 既有 lint，clean
```

- [ ] **Step 2: gate-1 `pedagogy-firstlearner-audit` 複驗（PD/OF 收斂）**

重 dispatch（`CONTENT_APPROVED=yes`）。Expected：`VERDICT: 0 PD blocking, 0 OF blocking, <A> advisory`；`[Surface PD#-det/OF2-det]` 應**消失**（scaffold/refs 已補）；advisory 逐條由使用者裁決、不強制歸零。

- [ ] **Step 3: L1/L5／NFA 回歸（SPEC §11 step 4；as-built waiver，Codex B4）**

SPEC §11 step 4 要求 scoped 修後重跑「L1/L5 + NFA + PD/OF」。**as-built 釐清：** L1/L5（六鏡，審 `.md` 內容 vs 講義＋數學正確）與 NFA（審 narration 衍生）的稽核對象都是 **`.md`／narration**；本輪 SP2 **只動 storyboard `.yml`、不動任何 `.md`／`say:`／narration** → L1/L5 與 NFA 的對象未變、結果不可能改 → **本輪 waived（附此理由於 applied 報告）**，非略過 §11、而是 as-built scoped 邊界使其成 no-op。**唯一例外：** 若某 OF1 修不得不牽動 `say:`／narration（NFA 禁改已認可 source，故此情形應已在 Task 3 回報並由使用者裁決、極可能不納入本輪）→ 才對受影響單元跑 scoped `narration-faithfulness-audit`＋（若動到 `.md`）六鏡 L1/L5。PD/OF 收斂由 Step 2 gate-1 複驗涵蓋。

- [ ] **Step 4: mock 重渲（離線免費）**

```bash
"$VENV" video/make.py --storyboard video/storyboards/ch03_trig_derivatives.yml --scene all --backend mock --quality high
```

Expected：exit 0；schema/lint/sizecheck 三閘 0-error（render gate 內含 provenance/pedagogy——flag 未翻仍 warn-only、不擋）；§3.1 全場 compose 成片到 `output/ch03/s3.1/`。MiKTeX 冷快取 transient → 重跑。

- [ ] **Step 5: 抽幀＋visual-frame-audit（含新 scaffold 場）**

```bash
rm -rf output/ch03/s3.1/critic/frames
"$VENV" video/pipeline/critic.py --storyboard video/storyboards/ch03_trig_derivatives.yml --dry-run
```

對含新 `scaffold.motive`/`problem`（及 D-A 的 flag badge）的場 dispatch `visual-frame-audit`（V1–V9＋A1–A7）。重點看：motive 行可讀（≥26px floor）、不 muted、不爆框/不撞 statement；divider problem 公式行正常渲染；ASSUMES badge（若加）不孤行。Expected：**0 confirmed blocking**。單場改動驗證用 `scratch_frames.py --scene <id> --out <dir>`（fresh、ground truth）。

- [ ] **Step 6: 出 applied HTML 報告**

`REVIEW-ch03_trig_derivatives-sp2-applied.html`：逐場列「加了什麼 ref:/refs:/scaffold＋locus＋draft 文字＋本輪 PD/OF/視覺裁決＋末幀」。比照 §3.2 Stage-2 報告。

- [ ] **Step 7: 使用者視覺 sign-off（HARD GATE）**

交報告＋成片。**未 sign-off 不翻 flag。**

---

### Task 6: §3.1 翻三 flag（gating）＋ commit

**Files:**
- Modify: `storyboards/ch03_trig_derivatives.yml`（`meta:` 加三 flag）

- [ ] **Step 1: 翻 flag**

```yaml
meta:
  id: ch03_trig_derivatives
  ...
  otf_enforce: true
  pedagogy_enforce: true
  fontfloor_enforce: true
```

- [ ] **Step 2: 驗 gating（exit 0 代表 surface 已歸零）**

```bash
"$VENV" video/pipeline/schema.py   video/storyboards/ch03_trig_derivatives.yml
"$VENV" video/pipeline/sizecheck.py video/storyboards/ch03_trig_derivatives.yml
```

Expected：schema.py **exit 0**（若 provenance/pedagogy 還有殘留 finding，現在會升 error → exit 1；exit 0 證實已乾淨）；若印 `[provenance]`/`[pedagogy]` 會標 `(ENFORCED)`。sizecheck font-floor `fontfloor_enforce` 下 exit 0（0 surface）。

- [ ] **Step 3: render gate 回歸**

```bash
"$VENV" video/make.py --storyboard video/storyboards/ch03_trig_derivatives.yml --scene all --backend mock --quality high   # exit 0，三閘（含 ENFORCED 的 prov/ped）全過
```

- [ ] **Step 4: commit**

```bash
git add video/storyboards/ch03_trig_derivatives.yml
git commit -m "video(ch03 §3.1): SP2 flip otf/pedagogy/fontfloor enforce -> gating (0 surface)"
```

---

## Phase C — §3.2 `ch03_chain_rule`（同程序）

> 前置：Phase B 完成（§3.1 sign-off＋翻 flag）。只動 `storyboards/ch03_chain_rule.yml`。**§3.1 跑出的程序問題先回饋校正本 phase。**

### Task 7: §3.2 scoped 修（provenance → pedagogy → OF1）

**Files:** Modify `storyboards/ch03_chain_rule.yml`

- [ ] **Step 1:** 加場級 `ref:`——content 場 `md:<scene_id>`（22 場）、divider（`divider_rule`/`divider_why`/`divider_use`）`ref: doc:frag-sec-3-2`。例：

```yaml
  - id: chain_rule_statement
    kind: content
    template: definition_math
    accent: theorem
    kicker: theorem
    ref: md:chain_rule_statement        # <-- 新增
    source: "chapter3-print-standalone.html SS3.2 . Theorem 3.3 (the chain rule)"
```

- [ ] **Step 2:** 加核可欄級 `refs:` 覆寫（D-B recap／D-C，flat map）。
- [ ] **Step 3:** 驗 provenance 歸零：`"$VENV" video/pipeline/schema.py video/storyboards/ch03_chain_rule.yml` → exit 0、無 `[provenance]`。
- [ ] **Step 4:** 加 `scaffold.motive`（10 場：theorem_proof×5＝`two_forms_equivalent`/`proof_setup_substitution`/`proof_easy_piece`/`proof_delicate_choices`/`proof_delicate_bound`；derivation×5＝5 個 example_*）＋`scaffold.problem`（3 divider），用核可文字。例：

```yaml
  - id: proof_setup_substitution
    ...
    ref: md:proof_setup_substitution
    scaffold: { motive: "Let the remainder form do the heavy lifting: substitute both, collect the linear part." }
```

```yaml
  - id: divider_why
    kind: divider
    ...
    ref: doc:frag-sec-3-2
    scaffold: { problem: "Show $P'(x_0)=f'(g(x_0))\\,g'(x_0)$ from local linear fits." }
```

- [ ] **Step 5:** （§3.2 無全域前提，**不加 registry**，除非 Task 3 另有核可。）
- [ ] **Step 6:** 驗 pedagogy 歸零：`schema.py` exit 0、無 `[provenance]`/`[pedagogy]`。
- [ ] **Step 7:** OF1 忠實修（若有，storyboard only，不動 `.md`）。
- [ ] **Step 8:** commit：

```bash
git add video/storyboards/ch03_chain_rule.yml
git commit -m "video(ch03 §3.2): SP2 backfill -- OTF refs + PD scaffold + OF1 (pre-flip)"
```

### Task 8: §3.2 回歸＋mock 重渲＋稽核 → sign-off

**Files:** 唯讀稽核；Create `content_scripts/_audit/REVIEW-ch03_chain_rule-sp2-applied.html`

- [ ] **Step 1:** 確定性閘回歸（schema/sizecheck/lint，同 Task 5 Step 1，對 `ch03_chain_rule.yml`）。
- [ ] **Step 2:** gate-1 `pedagogy-firstlearner-audit` 複驗（`CONTENT_APPROVED=yes`）→ `VERDICT: 0 PD blocking, 0 OF blocking`、`[Surface ...]` 消失。
- [ ] **Step 3:** L1/L5／NFA 回歸（SPEC §11 step 4，as-built waiver，同 Task 5 Step 3）：本輪只動 storyboard `.yml`、不動 `.md`／narration → L1/L5（審 `.md` vs 講義）與 NFA（審 narration 衍生）對象未變 → waived 並附理由；唯有某 OF1 修牽動 `say:`／`.md` 時（應已於 Task 3 回報裁決）才跑 scoped NFA＋L1/L5。PD/OF 由 Step 2 gate-1 複驗涵蓋。
- [ ] **Step 4:** mock 重渲 `"$VENV" video/make.py --storyboard video/storyboards/ch03_chain_rule.yml --scene all --backend mock --quality high` → exit 0、`output/ch03/s3.2/`。
- [ ] **Step 5:** 抽幀（`rm -rf output/ch03/s3.2/critic/frames` → `"$VENV" video/pipeline/critic.py --storyboard video/storyboards/ch03_chain_rule.yml --dry-run`）＋`visual-frame-audit` 對含新 scaffold 場（含 §3.2 已知 4 場 proof `qed` within-frame advisory，比照接受）→ 0 confirmed blocking。
- [ ] **Step 6:** 出 `REVIEW-ch03_chain_rule-sp2-applied.html`。
- [ ] **Step 7:** 使用者視覺 sign-off（HARD GATE）。

### Task 9: §3.2 翻三 flag＋commit

**Files:** Modify `storyboards/ch03_chain_rule.yml`（`meta:` 加 `otf_enforce`/`pedagogy_enforce`/`fontfloor_enforce: true`）

- [ ] **Step 1:** 翻 flag（同 Task 6 Step 1）。
- [ ] **Step 2:** 驗 gating：`schema.py` exit 0、`sizecheck.py` exit 0。
- [ ] **Step 3:** render gate 回歸：`"$VENV" video/make.py --storyboard video/storyboards/ch03_chain_rule.yml --scene all --backend mock --quality high` exit 0。
- [ ] **Step 4:** commit `video(ch03 §3.2): SP2 flip otf/pedagogy/fontfloor enforce -> gating (0 surface)`。

---

## Phase D — 收尾（文件＋全分支 review）

### Task 10: 進度文件＋全分支 review

**Files:** Modify `REBUILD_STATUS.md`、`HANDOFF-pedagogy-firstlearner-sp1.md`

- [ ] **Step 1:** `REBUILD_STATUS.md` 最上方加「✅ SP2 回填（ch03 §3.1/§3.2）完成」段：兩 deck 翻 gating、回填量（refs/scaffold/registry/OF1 數）、決策裁決（D-A~D-E）、durable 教訓（如 scene-id==unit-id 機械對映、scaffold 改 render 需視覺 sign-off、fontfloor 0-surface）。比照既有段落格式。
- [ ] **Step 2:** `HANDOFF-pedagogy-firstlearner-sp1.md` 更新「下一步」：SP2 ch03 完成；ch01 §1.1 仍未回填（範圍外，註明）。
- [ ] **Step 3:** 全分支 opus review（merge-readiness：scoped 紀律無越界、no-op 不變式、flag 正確）。findings 全處理＋回歸。
- [ ] **Step 4:**（可選、計費）Codex（gpt-5.5/xhigh）獨立覆核——**先報價徵同意**。
- [ ] **Step 5:** commit 文件；（依使用者）`finishing-a-development-branch` 決定 merge/PR。

---

## 5 · 成功標準 / 驗證（goal-driven）

每 deck 收斂判準（**翻 flag 後**）：
1. `schema.py <deck>` **exit 0**（`otf_enforce`＋`pedagogy_enforce` 下 provenance/pedagogy 0 error）。
2. `sizecheck.py <deck>` **exit 0**（`fontfloor_enforce` 下 font-floor 0 error；既有 within-frame advisory 接受）。
3. gate-1 `pedagogy-firstlearner-audit` **`VERDICT: 0 PD blocking, 0 OF blocking`**，`[Surface ...]` 消失。
4. `make.py --storyboard <deck>.yml --backend mock --quality high` **exit 0**、全場 compose 成片。
5. `visual-frame-audit` 對新 scaffold 場 **0 confirmed blocking**＋使用者視覺 sign-off。
6. NFA：未動 `.md`／narration（或受影響單元 scoped NFA clean）。
7. 改動可逐行追溯回核可遷移清單；**未動**模板/工具/rubric/另一 deck/`.md`/handout。

全程離線可驗；計費步驟（真 TTS、高解析渲染、Codex 覆核）另徵同意。

## 6 · scaffold 文字品質 bar（worked examples，供 Task 3 draft 對齊）

`scaffold.motive` ＝ 標題下一句「**為什麼現在做這個**」，**忠實於 cited 源**（OF1 會查）、不引入源沒有的數學、簡短（一行、滿 `CONTENT_W` 不孤行）：

- `difference_quotient_for_sine`（源 say：「let us transform that difference quotient instead of fighting it head-on」）→ `motive: "Transform the difference quotient into a product we can take limits of, one factor at a time."`
- `continuity_statement_sin_limit`（源：續 difference_quotient「the whole derivative hangs on … continuity … We secure both now」）→ `motive: "The derivative reduction owes two debts -- continuity and the limit; pay the first."`
- `fundamental_limit`（源 say：「Now we can finally close the limit that started all of this」）→ `motive: "Close the $\\sin\\theta/\\theta\\to1$ limit the whole section has been building toward."`

`scaffold.problem`（divider）＝**一條具體式子/問題**（PD3 advisory 要具體、非概念標題），純 `$math$` 走顯示公式行：

- `divider_squeeze` → `problem: "$\\tfrac12\\sin\\theta \\le \\tfrac12\\theta \\le \\tfrac12\\tan\\theta$"`（接著要 trap 的面積鏈）。
- `divider_why`（§3.2）→ `problem: "Show $P'(x_0)=f'(g(x_0))\\,g'(x_0)$ from local linear fits."`

> draft 文字皆 Task 3 列入遷移清單供使用者過目；Task 4/7 只 apply 已核可文字。

---

## Self-Review（writing-plans 自檢）

- **Spec coverage（SPEC §11 a–f）：** ① 乾跑→Task 1；② 分類（migration-required vs advisory）→Task 3 Step 1–2；③ 使用者核可遷移清單→Task 3 Step 5（HARD GATE）；④ scoped 修（provenance/scaffold/OF1）→Task 4/7；重跑 **PD/OF（gate-1）＋schema/sizecheck/lint** ＋重渲＋視覺 sign-off→Task 5/8；**L1/L5 與 NFA 因本輪不動 `.md`／narration 而 waived-with-rationale（Task 5/8 Step 3）——稽核對象未變、非略過 §11**；⑤ HTML 報告→Task 5/8 Step 6。翻 per-deck opt-in→Task 6/9。✔ 全覆蓋（§11 step 4 的 L1/L5/NFA 以 as-built waiver 對齊 scoped 邊界）。
- **As-built 對齊：** `refs:` flat dotted-key map（非巢狀）、`meta.assumptions`（非頂層）、三 flag 獨立、OF1 lifecycle、scene-id==unit-id 對映、scaffold 改 render（非 no-op）、fontfloor 0-surface——全以 code 為準寫入，非 spec 舊 prose。✔
- **Placeholder 掃描：** ref 對映表逐場填實（§3）、編輯有 worked YAML、驗證有確切指令＋expected exit/輸出。motive/problem 的**實際文字**刻意延到 Task 3 遷移清單（內容撰寫＋OF1 審＋使用者核可），§6 給品質 bar＋3 個 worked example 定錨——這是 §11「人核可後才動」的必要結構，非 placeholder。✔
- **型別一致：** 全程 `ref:`（場級 str）/`refs:`（flat map，key＝欄位路徑字串）/`scaffold: {motive,problem,flag}`/`meta.assumptions[{id,text,first_use_unit,source}]`/三 flag bool，與 fixture（`otf_provenance.yml`/`scaffold.yml`）＋code 一致。✔
- **缺口：** D-D（PD1）若乾跑出 blocking 屬較大改動（動 beat/narration→NFA），Task 3 獨立標示由使用者決定納入或另案——已在 §4 攤開。

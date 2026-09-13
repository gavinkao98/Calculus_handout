# KICKOFF — §3.2 `ch03_chain_rule`（首個全程照輪次協定走的節）

> **立檔：2026-09-13**（使用者第二次裁決當日）。**這一節有兩個交付目標**：
> ① 把 §3.2 做成片；② 順便把「一節怎麼做」變成可複製的 **SOP v1**（`KICKOFF-section-template.md`）
> 與 [`REBUILD_STATUS.md`](REBUILD_STATUS.md)「每節成本量測」表的一列。
> §3.1 是在協定還沒寫出來之前跑掉二十一輪的節；**§3.2 是第一個從第 0 步就照
> [`REVIEW_GATES.md`](REVIEW_GATES.md) §六「輪次協定」走的節**——協定跑不通的地方要回寫 §六，不要私下繞過。
>
> **驗收定義的權威在 [`REVIEW_GATES.md`](REVIEW_GATES.md) §六，不在本檔。** 本檔是這一節的執行計畫；
> 兩者牴觸以 §六為準，並回頭修本檔。

---

## 0. 給新 session 的啟動提示（可整段貼）

```
你負責 NTU 微積分影片產線（repo Calculus_handout，video/ 子樹）的 §3.2 The Chain Rule
（deck: ch03_chain_rule）。全程繁體中文溝通。

開工前依序讀：
  video/KICKOFF-s32-chain-rule.md          ← 本檔，執行計畫
  video/REVIEW_GATES.md §六                ← 輪次協定 G0–G7（驗收定義 SSOT）
  video/RUNBOOK-mimo-narration-route.md    ← MiMo 路線 step 0–4、TTS 旗標紀律
  video/CONTENT_METHODOLOGY.md §7／§8      ← 內容層檢核、講義變動時的維護
  video/content_scripts/ch03_chain_rule.md ← 已 LOCKED 的內容稿（source of truth）

這一節分兩個 phase，順序不可逆（G0 內容鎖）：
  Phase A 內容線 —— 立即可開，零計費直到 A5。對齊 .tex → sign-off → derive → NFA → TTS。
  Phase B 視覺線 —— 前置條件＝共用層 v1（KICKOFF-shared-layer-v1.md）merge 進 main 才開工。

紀律三條，違反任一條就停下來問：
  1. 任何計費／外部 API（MiMo TTS、Codex、agy）呼叫前先報量徵同意（根 CLAUDE.md）。
  2. 不改共用層（theme／brand／templates／字體／字級）——那是工具線的檔，發現需要就記進 §8 backlog。
  3. 一個 session 擁有 main 與 render；有檔案改動的派工一律各自 worktree、一 task 一 commit。
```

---

## 1. 目標與裁決（2026-09-13 使用者第二次裁決）

### 1.1 裁決原文（照抄，不要重新詮釋）

| # | 裁決 | 對本節的意思 |
|---|---|---|
| 1 | **§3.2 直接解凍** | 2026-07-19 的「凍結至品質補強試點 A/B 裁決」作廢，本檔即開工檔 |
| 2 | **原語路線（motion primitive 鋪滿）推廣到全部小節、教義定案** | Phase B 不需要再證明原語有用；照 §3.1 的做法鋪，不做 A/B |
| 3 | **原訂的新舊 A/B 裁決稿取消** | 不產 `REVIEW-…-ab.html`，不重跑 ⑬ 成片對照 |
| 4 | **先用 §3.2 串行把流程走一遍變成熟，再並行處理後面的章節** | §3.2 是唯一在跑的節；§3.3 起要等 SOP v1 |
| 5 | 並行之後＝**每節一個 session＋自己的 worktree＋自己的 output 目錄**，一個指揮 session 只 merge | 本節要順便驗證這個形狀跑不跑得動，把摩擦寫進 §7 |
| 6 | 並行之前**凍結共用層 v1** | 見 §1.2 |
| 7 | **§3.1 收尾另開對話**：里程碑六鏡審（agy 三次呼叫徵同意）；4K final 等共用層 v1 落地後重 render | 不要在本節的 session 裡做 §3.1 的事 |

### 1.2 共用層 v1 的四項（另一份開工檔 [`KICKOFF-shared-layer-v1.md`](KICKOFF-shared-layer-v1.md)）

1. 字體 **Instrument Sans**
2. 字級**三階**＋**取消 `math_sm 40`**
3. **版面／排版規則進 `sizecheck`**
4. **`worked_example` 模板**

**依賴關係（本節最重要的一條排程事實）：**

- **§3.2 的視覺階段（Phase B）要等 v1 落地。** 四項裡有三項會改變畫面幾何（字體換掉 `brand.py`
  的 `_WIDTH_K` 校準、字級三階動到每一個 block 的高度預算、版面規則會改 `sizecheck` 的紅線），
  在 v1 前鋪原語＝鋪在會被推翻的版面上。
- **§3.2 的內容階段（Phase A）不等。** Phase A 動的是 `.md`／`.spoken.yml`／`_mimo.yml`／音檔，
  與共用層零交集。**這是本節能立刻開工的全部理由。**
- Phase A 的 A2（storyboard 更新）是**灰區**：**可以先寫 storyboard 欄位、等模板落地再 render**。
  例題場宣告 `template: worked_example` 但該模板還不存在時，`schema.py` 會擋——所以 A2 的
  例題場**最後再切**，切的時候 v1 應該已經 merge（見 §4 A2 的做法）。

### 1.3 本節的兩個交付目標

- **產品：** §3.2 成片（1080p 過閘＋4K final）。
- **制度：** **一節 SOP v1**——跑完後從本檔抽出 `video/KICKOFF-section-template.md`（把 §3.2 專屬的
  數字換成佔位），並在 `REBUILD_STATUS.md` 的「每節成本量測」表填滿 §3.2 那一列。

---

## 2. 現況與已驗證 code 事實（2026-09-13 實跑快照；行號會漂，用 grep）

> 下列每一條都是本檔立檔當日親自跑過／打開過的，不是轉述。**與開工指示不符的四處標 ⚠️。**

### 2.1 內容稿 `content_scripts/ch03_chain_rule.md`（719 行）

| 事實 | 證據 |
|---|---|
| **LOCKED、`CONTENT_APPROVED=yes`**，2026-06-29 使用者 sign-off | `ch03_chain_rule.md:9`（標頭「階段」行）；commit `b3860bc`「內容稿 sign-off → LOCKED（Stage 1 完成）」 |
| **`source_rev` stamp 指向凍結的 HTML fragment，不是 `.tex`** | `ch03_chain_rule.md:5`：`legacy/html_handout/fragments/ch03/sec-3-2.html` `sha256:a1cd5867…`；標頭自己寫明「2026-08-09 起唯一源＝`handout/latex/src/ch03/chapter3.tex`——§8 對齊在解凍後做」 |
| **`[source_rev]` 目前是 WARN（warn-only，不擋）** | `python video/pipeline/schema.py video/storyboards/ch03_chain_rule.yml` → `[schema] structure OK` ＋ `[source_rev] 1 finding(s) (warn-only)`：`handout source … changed since the content script was stamped` |
| 教學單元 **24 個**（含 intro／outro；22 個有旁白） | `grep -c "^### unit: " ch03_chain_rule.md` ＝ 24 |
| **`examples:` 宣告 5 筆、`folds:` 0 筆** | `ch03_chain_rule.md:445/498/526/556/584` ＝ `ex:3.4`／`3.5`／`3.6`／`3.7`／`3.8` |
| **`example_coverage` 閘目前 0 EX1／0 EX2（全過）** | `schema.py` 跑完不印 `[example_coverage]` 區塊；另以 `example_coverage.tex_examples_by_section()` 直接驗算，`3.2` 區間＝`{ex:3.4, ex:3.5, ex:3.6, ex:3.7, ex:3.8}`，與宣告集合相同 |
| §3.2 在 `chapter3.tex` 的 **`envexample` 有 5 個：`ex:3.4`–`ex:3.8`**，全在 `\subsechead{Using the rule}` 之後 | `chapter3.tex:327/346/363/383/403`；節界＝`\sechead{3.2}` 在 `chapter3.tex:208`、`\sechead{3.3}` 在 `:417` |

**§3.2 在 `chapter3.tex` 的完整環境清單（A1 的 diff 對象，`:208–416`）：**

| 環境 | label | 行 | 內容稿對應單元 |
|---|---|---|---|
| `envtheorem` | `thm:3.3` The chain rule | `:215` | `chain_rule_statement` |
| `envremark` | `rem:3.2` The Leibniz form | `:224` | `leibniz_form` |
| `envstrategy` | `strat:3.1` Differentiating a composition | `:231` | `decomposition_strategy` |
| `\subsechead{Why the rule is true}` | — | `:243` | `proof_strategy_bridge` |
| `envdefinition` | `def:3.1` Differentiability, remainder form | `:246` | `remainder_form_definition` |
| `envproposition` ＋ `envproof` | `prop:3.3` Equivalence of the two forms | `:263`／`:266` | `two_forms_equivalent` |
| `envproof` | of Theorem 3.3（full ε-δ） | `:279` | `proof_setup_substitution`／`proof_easy_piece`／`proof_delicate_choices`／`proof_delicate_bound`（4 個單元） |
| `\subsechead{Using the rule}` | — | `:325` | — |
| `envexample`＋`envsolution` ×5 | `ex:3.4`–`ex:3.8` | `:327`／`:346`／`:363`／`:383`／`:403` | 5 個 `example_*` 單元 |
| `envcaution` | （無 label） | `:342` | `caution_inner_derivative` |

> **注意 `def:3.1` 是全書第一個 `envdefinition` 出現在影片產線裡的節**——§3.1 一個都沒有
> （⑬ 的 B-3 查證：`chapter3.tex:30–207` 零個 `envdefinition`）。所以 §3.2 的 `accent: definition`
> **有一場是真的**（`remainder_form_definition`），其餘是舊帳，見 §2.3。

### 2.2 ⚠️ 六鏡／copyedit／sign-off **確實做過**，而且 Stage 2 也做過一輪

**與開工指示的「查證是否真的做過」不同：不只做過，證據齊全。**

| 閘 | 狀態 | 證據 |
|---|---|---|
| 六鏡內容稽核（L1–L6） | **blocking == 0**，3 條 tier-3 advisory 逐筆裁決 | [`_audit/REVIEW-ch03_chain_rule-applied.html`](content_scripts/_audit/REVIEW-ch03_chain_rule-applied.html)（multi-agent Workflow `wf_d53afe59-4f2`；L5 隔離盲算重算 Ex 3.4–3.8／Prop 3.3 雙向／Thm 3.3 full ε-δ 全 match） |
| 散文 copyedit（C1–C5） | **6 tighten ＋ 9 optional 全採納** | 同上 HTML「散文 copyedit pass」節 |
| 旁白 sign-off | **2026-06-29 使用者拍板** | `ch03_chain_rule.md:9`；審核稿 [`content_scripts/ch03_chain_rule_narration.html`](content_scripts/ch03_chain_rule_narration.html)（48 KB，存在） |
| **Stage 2 工程輪（2026-06-29～07-01）** | storyboard＋2 hooks＋**27 場 mock compose**＋視覺幀稽核 gate-1 | [`_audit/REVIEW-ch03_chain_rule-stage2-applied.html`](content_scripts/_audit/REVIEW-ch03_chain_rule-stage2-applied.html)；digest [`_audit/_gen/ch03-s32-stage2-audit.json`](content_scripts/_audit/_gen/ch03-s32-stage2-audit.json)（`scenes_audited: 22`、**`confirmed_blocking: 0`**、Workflow `wf_dd28dc9d-f0c`）；產生器 `_audit/_gen/build_s32_review_html.py` |

**⚠️ 所以 §3.2 的起點不是「只有 LOCKED 內容稿」，是「內容稿 LOCKED ＋ 一份七月契約的 storyboard，
而且那份 storyboard 曾經渲得出 0 blocking 的乾淨幀」。** 這改變 Phase B 的性質：
**B1 是升級，不是從零寫 storyboard。**

**沒做過的（照指示核對，全部屬實）：**

- 沒有 `content_scripts/ch03_chain_rule.spoken.yml`——`derive_spoken.py --deck ch03_chain_rule --check`
  印 `[derive_spoken] missing …ch03_chain_rule.spoken.yml`。
- 沒有 `storyboards/ch03_chain_rule_mimo.yml`（`ls storyboards/ | grep chain` 只有 `ch03_chain_rule.yml`）。
- 沒有 NFA：`_audit/` 裡沒有 `PROMPT-ch03_chain_rule-narration-faithfulness.md`、沒有 `REPORT-…`。
- 沒有真 TTS：主 checkout `video/output/ch03/s3.2/` 只有 `audio/`（mock）、`critic/`、
  `ch03_chain_rule.mp4`（9.7 MiB，**2026-07-01 的 mock 成片**），**沒有 `audio_mimo/`**。
  對照 §3.1 的 `output/ch03/s3.1/` 有 `audio_mimo/`。
  **七月 mock 產物不能沿用**（mock 是靜音 WAV、時序是估的；`make.py --reuse-audio` 的 freshness
  閘也會擋——deck 的 `{show}`／beat 數一改就 stale）。

### 2.3 storyboard `storyboards/ch03_chain_rule.yml`（638 行）——七月模板期的契約

**實測結構：**

| 量 | 值 | 怎麼量的 |
|---|---|---|
| 場數 | **27**（intro 1 ＋ divider 3 ＋ **content 22** ＋ outro 1） | `yaml.safe_load` 後數 `kind` |
| 旁白字數 | **1,677 字**（剝掉 `{…}` marker 後） | 同上；§3.1 是 2,229 字／963.6 s ⇒ **138.8 wpm** |
| 推估片長 | 旁白 **≈ 12.1 分**（1677 ÷ 138.8）；加 intro／divider／outro 家具約 **12.5–13 分** | 依 §3.1 實測語速換算 |
| `{show}` marker | **70 個**；content 場的拍數合計 **≈ 92 拍** | `re.findall(r'\{show ')` |
| 客製 hook | **2 個**：`composed_mapping`（Fig 3.5）／`remainder_tangent`（Fig 3.6），都在 `animations/ch03_chain_rule_hooks.py` | storyboard `hook:` 欄 |
| template 分布 | `definition_math` 7／`theorem_proof` 5／`derivation` 5／`graph` 2／`callout` 1／`procedure_steps` 1／`recap_cards` 1 | 同上 |

**現行契約缺的欄位（全部 0 次）：`paced:`／`pauses:`／`carry:`／`focus:`／`exit:`／`seg_roles`／
`meta.color_map`／`covers:`／`meta.coverage_enforce`／`meta.assumptions`。**
（`meta` 只有 `otf_enforce`／`pedagogy_enforce`／`fontfloor_enforce` 三個 enforce 旗標，
2026-07-01 commit `f3a3f4c` 翻開的；§3.1 另有 `coverage_enforce`、`color_map: {\theta: strategy}`、
`assumptions:`。）

**對照 §3.1 現行契約，B1 要更新的項目清單：**

| # | 項目 | §3.2 現況 | 依據 |
|---|---|---|---|
| 1 | `accent:` 語意軸（Direction B，⑨） | ⚠️ **10 場標 `definition`**，但 §3.2 只有 1 個真的 `envdefinition` | `KICKOFF-s31-amplify.md` §2「語意色軸」；§3.1 的 B-3 先例＝散文／Figure 場**不標 accent**、推導場改 `accent: derivation` |
| 1a | ↳ 該拿掉 accent 的散文／Figure 場（6 場） | `why_composition_is_missing`／`rates_multiply_intuition`／`composed_mapping_figure`／`proof_strategy_bridge`／`remainder_tangent_figure`／`toward_section_3_3` 全標 `definition` | 同上 |
| 1b | ↳ 該保留的 | `remainder_form_definition`＝真的 `def:3.1`，赭色正確 | `chapter3.tex:246` |
| 1c | ↳ ⚠️ **缺的：`caution_inner_derivative` 目前 `accent` 未設**（落中性 slate），但它對位 `envcaution` | 應為 `accent: caution`（紅） | `chapter3.tex:342`；`accent`→role 對照見 `KICKOFF-s31-amplify.md` §2 |
| 1d | ↳ ⚠️ **3 個 divider 仍帶 `accent: definition`** | §3.1 已在 ⑰ 拿掉四個 divider 的 `accent: definition`（幕級家具無可對位的講義環境） | `REBUILD_STATUS.md` ⑰ |
| 2 | `scaffold.*` 揭示時序 | 13 筆 `scaffold`，**全部是 `motive`**（11 個 content 場）；⑬ 已讓 `scaffold.*` 吃 `{show}` 時序，零成本生效 | `REBUILD_STATUS.md` ⑬ |
| 2a | ↳ ⚠️ **divider `scaffold.problem` 已經有了**（三個 divider 全有） | `divider_rule`／`divider_why`／`divider_use` 各帶一條 problem 式 | 與開工指示不同：這項**不用做** |
| 3 | `carry:`／`exit:` 跨場延續 | 0 次 | ⑮ T4 落地；`DESIGN.md`「motion primitive」節 |
| 4 | `focus:` 聚焦 | 0 次 | 原語 4；`pipeline/focus.py` |
| 5 | `paced:` 填長拍 | 0 次 | 原語 7；`pipeline/pacing.py`（⑬ 的核心武器） |
| 6 | `pauses:` | 0 次 | `pipeline/pauses.py` |
| 7 | 例題場換 `worked_example` 模板 | 5 個 `example_*` 場現在全用 `derivation` | 共用層 v1 第 4 項；**模板尚未實作** |
| 8 | `meta.color_map` 變數色表 | 無 | ⑮ T1；§3.2 的候選變數＝`u`／`h`／`R` 等，B1 再定 |
| 9 | **原語 1（揭示時序）已免費生效** | **12 個 content 場**已寫 `{show statement}`／`{show proof.0}`——⑦／⑬ 修好 reveal 時序後，這些場不改一個字就會滑入 | `re.findall` 實測 |

**目前閘的狀態（2026-09-13 實跑，全在乾淨 worktree）：**

```
python video/pipeline/schema.py    video/storyboards/ch03_chain_rule.yml
  → [schema] structure OK ; [source_rev] 1 WARN（warn-only）
python video/pipeline/lint.py      video/storyboards/ch03_chain_rule.yml
  → 5 WARN：3 條 display-style math 在 INLINE register（example_chain_times_quotient.prompt／
     example_leibniz_rates.prompt／recap.points[1]）＋2 條 widow line
     （two_forms_equivalent.statement／proof_easy_piece.statement）
python video/pipeline/sizecheck.py video/storyboards/ch03_chain_rule.yml
  → 0 error, 5 warning：qed 越安全邊界 ×2（proof_setup_substitution／proof_delicate_choices）、
     statement 換行變全寬帶 ×2（two_forms_equivalent／proof_delicate_bound）、
     caution_inner_derivative 單塊填充 28% < 35%
python video/pipeline/run_selftests.py  → all 42 green
```

> **`sizecheck` 的 TeX cache race 陷阱（本檔立檔時親踩）：** 同一個 worktree 同時跑兩支
> `sizecheck.py` 會得到 8 個假的 `SIZE: could not build scene (PermissionError/FileNotFoundError)`。
> **量測閘一次只能跑一支**；數字對不上先確認沒有別人在跑（G7 的時間窗紀律）。

### 2.4 已驗證的 code 事實（沿用 §3.1，不重新發明）

**完整版在 [`KICKOFF-s31-amplify.md`](KICKOFF-s31-amplify.md) §2，這裡只列本節會用到的四條：**

1. **六支 motion primitive 怎麼用**（原語 1 揭示時序／2 原地變形 `anim: transform`／3 游標掃描
   `kind: sweep`／4 聚焦 `focus:`／5 跨場延續 `color_role`＋`carry:`／6 圖跟旁白長
   `seconds: beat`）＋原語 7 `paced:`——表在 `KICKOFF-s31-amplify.md:112–134`。
   **`focus` 的還原一律用 `save_state()`/`restore()`，絕不可用 `set_opacity(1.0)`。**
2. **驗 TTS 零成本的唯一正確方法**＝比對 `scene_text_hash`（剝掉 marker 後的口語全文 hash），
   code 片段在 `KICKOFF-s31-amplify.md:150–163`。**離線直接呼叫 `scene_reuse_ok` 會繞過 CLI 閘、
   給出與實際相反的預測**（⑬ 花掉 13 次 billed call 的成因）。
3. **零行為改變的驗收方式**＝`python tools/doctor.py --smoke` 改動前後 diff 必須逐字相同
   （`KICKOFF-s31-amplify.md:165–171`）。
4. **hook 內的文字一律走 `brand.*`**（`CONTENT_METHODOLOGY.md` §5；⑮ 教訓：hook 自建 `MathTex`
   不吃 `meta.color_map`、`inset` 鏡不到 hook 幾何）。
   ⚠️ **`animations/ch03_chain_rule_hooks.py:57` 的 `_fade` 仍是回傳寫死秒數的舊 helper**
   （§3.1 的 hooks 已在 ⑲ 全檔遷成 `_elapsed` 量測值，`REBUILD_STATUS.md` ⑲ 明寫
   「`ch03_chain_rule_hooks.py` 的同款 `_fade`，另開一件」）。它掛在 7 個 Block 上
   （`:149–152`、`:223–225`）。**B1 要順手遷完，否則 `[sync]` 硬閘會吃到假秒數。**

---

## 3. 全域護欄（G0–G7 在本節的具體形狀）

> **權威＝[`REVIEW_GATES.md`](REVIEW_GATES.md) §六。** 本節只寫「在 §3.2 具體是什麼」。

### 3.1 G0 內容鎖——順序不可逆

**旁白與上畫面文字定稿 → NFA 通過 → TTS 合成完成 → 才做視覺／動作設計。**

- lock 之後仍要改內容，**視為開新一輪內容階段**，明示「部分視覺工作要重做」，**不混進拋光輪**。
- 依據＝§3.1 第 ⑲ 輪的五條 must **全部**是 Task D 在四原語鋪滿 27 場**之後**才對齊講義、
  把拍子拉長 6–35 秒造成的（`KICKOFF-process-reform.md` §2.1）。
- **本節的落地方式＝把 §8 對齊排在 A1（最前面），在花任何錢、動任何畫面之前做完。**

### 3.2 計費紀律

- **每次計費／外部生成式 API 呼叫前報量徵同意**（根 `CLAUDE.md`）。本節的三個計費點：
  **A4 gate-2 Codex NFA**、**A5 MiMo TTS**、**§6 里程碑六鏡的 agy ×3**。
- 報量的內容＝**場數／秒數／fallback 預算**，並註明 reuse 後的下限。
- TTS 報價一律先跑 `tts.py … --backend mimo --dry-run` 取 planned／worst 表，
  **`--dry-run` 的 `plan` 欄只有下了 `--reuse-existing` 才算數**（RUNBOOK `:124–128`）。
- **不計費的離線路徑可逕行**：`tts.py --backend mock`、本地 Manim render、ffmpeg mux/concat、
  所有 gate-1 subagent。

### 3.3 一輪的定義（G5 批次化）

**一輪 ＝ 收齊該輪全部 must → 併行派工（各自 worktree、各改各的函式）→ 一次 merge → 一次 render → 一次再審。**

**不要一件一輪。** §3.1 的 ⑭–㉑ 八輪跑掉 8 次全片 1080p render；派工制本身沒問題
（24 件改動 19 件一次過），貴的是輪數。

### 3.4 輪內審 vs 里程碑審（G2）＋新 must 上限

- **輪內：** 只跑上一輪 finding 的**回歸清單**（逐條已關／未關）＋確定性閘。**不跑生成式盲審。**
- **里程碑：** 一節收斂時跑**一次**完整六鏡。
- **輪內新 must 上限 3 條。超過就當成排序問題，退回內容階段（本檔 §3.1 的 G0 內容鎖），不要繼續拋光。**

### 3.5 G6 契約進測試——紅測試先行

任何「本來就該成立但壞掉」的事，**修之前一律先寫紅測試**（根 `CLAUDE.md` Karpathy §4）。
§3.1 前段的四件（`focus` 還原、耗時誠實、標籤相交、`DashedLine` 盲點）全部是先在幀裡肉眼看到、
才回頭補 selftest——本節不要重演。

### 3.6 G7 多 session 紀律

- **一個 session 擁有 `main` 與 render**，其他一律 worktree 分支＋交 hash。
- worktree 開分支後**先 `git merge main`**（分支點可能落後）。
- **輸出目錄各自隔離**：`critic.py --out <round dir>`、`rewatch_pack --out <dir>`。
  ⚠️ `rewatch_pack --scene <子集>` 打進既有 pack 目錄會整個覆寫 `INDEX.md`／`pack.json`，
  **子集一律另給 `--out`**。
- 開工先 `git status`；別人 dirty 的 hunk 不碰、只 commit 自己的路徑。
- **render／tts 的時間窗用 `ListAgents`＋`SendMessage` 互相通知**（並行的另兩條線在跑）。
- ⚠️ **量測閘（`sizecheck`／`schema`）一次只能跑一支**，理由見 §2.3 的 TeX cache race。

### 3.7 共用層不在這裡改

**字體、字級、`theme.py`／`brand.py`／`templates/` 的版面契約、`sizecheck` 的規則——
全部是工具線 [`KICKOFF-shared-layer-v1.md`](KICKOFF-shared-layer-v1.md) 的檔，本節不碰。**
發現需要改，**記進 §8 的工具線 backlog**，不要自己動手——兩條線同時改同一個檔＝⑯ 那種
「兩個 session 搶 `derivation.py`」的場面。

---

## 4. Phase A — 內容線（**立即可開，零計費直到 A5**）

> **A1–A4 全部不花錢。** 唯一的計費點是 A4 的 gate-2（Codex）與 A5 的 TTS，各自單獨徵同意。

### A1 — 內容稿對 `chapter3.tex` §3.2 做 §8 對齊

**為什麼排第一：§3.1 Task D 的學費。** §3.1 是在四原語鋪滿 27 場**之後**才對齊講義，
結果五個場的拍子被拉長 6–35 秒、畫面只有一次 reveal，⑲ 的五條 must 全部由此而來，
外加 15 次 billed TTS call 重合成。**在花錢、動畫面之前做完對齊，這一整類成本就不存在。**

**做法（`CONTENT_METHODOLOGY.md` §8 步驟 0–5）：**

1. **觸發器已經在響**：`[source_rev] WARN`（§2.1）。**不要關掉 WARN 了事。**
2. **Diff**：stamp 指向凍結的 legacy fragment，所以要兩段比——
   `git diff b3860bc HEAD -- legacy/html_handout/fragments/ch03/sec-3-2.html`（lock 後 HTML 的變動），
   再把現行 `handout/latex/src/ch03/chapter3.tex:208–416` 與內容稿逐單元對照。
   §2.1 的環境表就是對照的骨架。
3. **逐單元判「跟改／不跟改」**，每一筆都要寫理由（§3.1 的比例是 21 場裡 5 場跟改、16 場不跟改）。
   **外科式修改，不要整份重寫。** 內容稿是 source of truth，**MUST NOT 從 storyboard 或別處重生**。
4. **重念受影響的 narration**：記號改了，引用該記號的旁白也要改。
5. **`source_rev` stamp 換到 `.tex`**：`python video/pipeline/source_rev.py handout/latex/src/ch03/chapter3.tex`
   → 蓋回 `ch03_chain_rule.md:5`。**驗收＝`schema.py` 的 `[source_rev]` WARN 消失。**

**改動單元跑 scoped 回歸（gate-1 subagent，免費）：**

- **只對動到的單元**跑 scoped six-lens／copyedit 回歸——這一節已經 LOCKED，
  **不得 re-litigate 沒動到的單元**（`REVIEW_GATES.md` §二 第 7 條）。
- copyedit 是 **lock 前唯一能改冗餘的地方**；本次是 post-lock 例外編修
  （`CONTENT_METHODOLOGY.md` §7「已鎖稿的節要補潤稿」），所以**這一輪把措辭問題一次處理完**——
  A4 的 NFA 之後就再也改不動了（D2 會把去重當違規）。

**使用者 sign-off（人閘）：**

- 重新編譯 [`content_scripts/ch03_chain_rule_narration.html`](content_scripts/ch03_chain_rule_narration.html)，
  **使用者在 HTML 上拍板**，才算重新 LOCKED。
- **這是 Phase A 的第一個停等點。**

**A1 完成的判準：** `[source_rev]` WARN 消失｜逐單元跟改／不跟改表寫完｜scoped 回歸 blocking 0｜
`_narration.html` 重新 sign-off。

---

### A2 — storyboard 更新到現行契約

> **可以先寫 storyboard 欄位、等模板落地再 render。** 本步只要通過 **pre-render 的閘**，
> 不需要 render 出畫面。

**做什麼：**

1. **把 A1 動過的單元同步進 storyboard 的 `say`／payload**（內容稿是源，storyboard 跟著改）。
2. **`accent:` 依語意軸全面複審**——照 §2.3 的表 1a/1b/1c/1d 做：
   6 個散文／Figure 場拿掉 `accent`、`caution_inner_derivative` 改 `accent: caution`、
   3 個 divider 拿掉 `accent: definition`、`remainder_form_definition` 維持 `definition`。
3. **補 `examples:`／`folds:` 宣告**——`.md` 已有 5 筆 `examples:`，`example_coverage` 已 0 finding；
   A1 若動了例題單元要重驗（`schema.py` 不印 `[example_coverage]` 就是過）。
4. **例題場改 `worked_example` 模板——最後做，且要等共用層 v1 merge。**
   在 v1 落地前，5 個 `example_*` 場**維持 `derivation`**；v1 merge 進 main 之後，
   同一個 commit 裡把 `template:` 切過去、payload 改成模板的欄位形狀，再跑一次 pre-render 閘。
   **切模板之前不要開始鋪原語**（payload 形狀會變，`paced:`／`focus:` 指的 block id 也會變）。
5. `meta` 補齊：`coverage_enforce`（跟 §3.1 齊）、`color_map`（B1 再定變數，A2 先留空）。

**pre-render 閘（全部免費、離線）：**

```
python video/pipeline/schema.py                  video/storyboards/ch03_chain_rule.yml   # structure OK、source_rev 無 WARN
python video/pipeline/lint.py                    video/storyboards/ch03_chain_rule.yml   # 現有 5 WARN 順手清掉
python video/pipeline/sizecheck.py               video/storyboards/ch03_chain_rule.yml   # 0 error（現況已 0）
# gate-1 subagent（免費）：pedagogy-firstlearner-audit（PD1–PD4 ＋ OF1–OF2 ＋ SC1–SC2），PRE-render
```

**A2 完成的判準：** 四支確定性閘 0 error｜`pedagogy-firstlearner-audit` 的 PD1／OF1／SC-honesty
blocking ＝ 0｜`accent` 複審表逐場有結論。

---

### A3 — `derive_spoken.py` 產口語版與 `_mimo.yml`

```
# 1. 手寫口語單一源（RUNBOOK step 1；念法慣例權威＝NARRATION-FAITHFULNESS-RUBRIC.md）
video/content_scripts/ch03_chain_rule.spoken.yml
# 2. parity 檢查（確定性、擋 exit 1）
python video/pipeline/derive_spoken.py --deck ch03_chain_rule --check   # 必須印 "parity OK"
# 3. 生成（兩個生成檔標 DO NOT EDIT；要改旁白改 .spoken.yml 重生）
python video/pipeline/derive_spoken.py --deck ch03_chain_rule
#    → storyboards/ch03_chain_rule_mimo.yml ＋ content_scripts/ch03_chain_rule_narration_spoken.md
```

**§3.2 特別要小心的念法（⑰ 的 NFA 第一輪抓到四條 blocking，三條同類——
新寫的句子沒套本片既有的去歧義慣例，漏了就會被合成進付費音檔）：**

- `f^{-1}` → "f inverse"，**絕不** "f to the minus one"
- 分數／和的邊界：`A plus B over two` 會被聽成 $A+\frac B2$ ⇒ 要補 "the quantity"
- 合成的邊界：`sine of u plus v` 會被聽成 $(\sin u)+v$ ⇒ 同上
- §3.2 的高風險字串：$f'(g(x_0))\,g'(x_0)$、$R_3(h)/h$、$\sqrt{1+\sin^2 x}$、
  $\sqrt{(x-1)/(x+2)}$、$(|m_1|+1)\varepsilon$ —— **這一節是 full ε-δ，符號密度比 §3.1 高**。

**A3 完成的判準：** `parity OK`｜`_mimo.yml` 生成｜口語版通讀一遍沒有 LaTeX 漏出。

---

### A4 — NFA 旁白忠實稽核

**gate-1（`narration-faithfulness-audit` subagent，免費）：**

- 1 個 narration reader 跑 D1–D6；`CONTENT_APPROVED=yes`（已 sign-off），所以 **D7 不必跑**
  ——但 A1 動過的單元屬 post-lock 改稿，**對動到的單元另開隔離盲 reader 跑 D7 重算**
  （`CONTENT_METHODOLOGY.md` §8 步驟 5）。
- **迭代到 blocking == 0。**

**gate-2（Codex，計費，需逐次徵同意）：**

- 頻率矩陣（`REVIEW_GATES.md` §二 第 8 條）：**NFA 的 gate-2 是「每節」**——
  依據就是 §3.1 的實證：**gate-2 抓到 gate-1 漏掉的一條 D3 blocking**。這一節照跑。
- 指令：`codex exec -s read-only < video/content_scripts/_audit/PROMPT-ch03_chain_rule-narration-faithfulness.md`
  →**raw 輸出落 scratchpad、不進版控**，findings 與裁決轉錄進版控的
  `REPORT-ch03_chain_rule-narration-faithfulness.md`。
- **NFA 裁決寫進該次修正 commit 的 message body**（`git log --grep="NFA"`）。

**A4 完成的判準：** gate-1 blocking 0｜gate-2 blocking 0｜回歸再審確認沒改過頭／漏檔｜
版控 REPORT 寫完。

---

### A5 — TTS（**唯一的大額計費點**）

**A5-0 先用 mock 走通 manifest／時序（零計費，可逕行）：**

```
python video/pipeline/tts.py  --storyboard video/storyboards/ch03_chain_rule_mimo.yml --backend mock
python video/make.py          --storyboard video/storyboards/ch03_chain_rule_mimo.yml --reuse-audio --quality high
```

**目的＝在花錢之前把 `{show}` 對映、beat 切分、`[sync]` 全部弄乾淨。**
mock 是靜音 WAV、beats 模式、離線；`make.py` 會拒絕用 mock 覆蓋真 manifest。

**A5-1 報價（徵同意的內容）：**

| 欄 | §3.2 的數字（依 §2.3 實測推算，執行前以 `--dry-run` 實跑覆蓋） |
|---|---|
| 合成單位 | `--unit auto` ⇒ 全部 9 個 content template 走 **scene-level＋forced alignment** |
| 場數 | **22 個 content 場** |
| 音訊秒數 | **≈ 725 s**（1,677 字 ÷ 138.8 wpm × 60；§3.1 實測語速） |
| 預期 billed call | **22**（一場一次，reuse 為 0） |
| fallback 預算 | `--fallback-budget 2`＝只夠 resynth。**要開 chunk 救援得調到 1＋該場句數，句數即 billed sub-synth 數、須併入報價**；chunk 會自檢 budget、不足即 decline 退 beats |
| worst case | `--dry-run` 的 `worst` 欄（已把 ladder 每非空 beat 計入）——**報價時兩個數字都給** |
| 上限 | **`--max-billed-calls N` 一律帶**，N ＝ 核准的數字 |

**A5-2 合成（同意後）：**

```
python video/pipeline/tts.py --storyboard video/storyboards/ch03_chain_rule_mimo.yml \
       --backend mimo --reuse-existing --skip-qa --max-billed-calls <核准數>
```

**四條旗標紀律（RUNBOOK；每一條都是真金白銀換來的）：**

1. **`--reuse-existing` 漏掉就整批重合成**——`tts.py:1054` 的 `use_reuse = args.reuse_existing and …`
   才會建 reuse index，沒有它 index 是空的、`scene_reuse_ok` 根本不會被問到。⑬ 的代價＝13 次 billed call。
2. **`--skip-qa` 一律下**（2026-09-13 訂正，不是特例）——ASR QA 探針對**所有被 spell out 的數學**
   誤判 misspeak ⇒ 場判 fail ⇒ 重合成。⑰ 實測：只給一場下旗標時四場跑下來三場重試、
   7 次呼叫 0 場 promote；六場全下之後 5 場 5 次、0 retry。**QA 改成事後離線看 `manifest.json` 的 `gates.qa`。**
3. **`--no-billing`／`--max-billed-calls N`** 把「這次應該不花錢」變成保證——上限涵蓋整個 run
   （含 beats 終端），超過的那次呼叫在打出去前中止；WAV 要等閘全過才 promote，**中止時 manifest
   與既有音檔原封不動、可安全重試**。
4. **beats 模式的場一律 `--unit beat`**（`--unit auto` 會把它們路由去 scene-level ＝ 1 次計費，
   然後才可能一路掉回 beats 終端，更貴）。§3.2 開工時**還沒有**已知的 beats 場——
   第一次真合成後看 `manifest.json` 哪幾場降級，記進 §7 成本表。

**A5-3 `listening_pack` 人閘（使用者聽一遍）：**

```
python video/pipeline/listening_pack.py --manifest video/output/ch03/s3.2/audio_mimo/manifest.json
```

產 standalone HTML（每場 `<audio>`＋WPM＋validation/qa＋fallback＋ebur128 LUFS/TP，依風險排序）。
**Phase A 的第二個、也是最後一個停等點。**

> **MiMo 非決定性**——同文字每次合成是不同 take（±~10% 長度）。**滿意的 take 不要重合成。**

**A5 完成的判準：** `manifest.json` 生成且 freshness 過｜billed call 數 ≤ 核准數｜
`listening_pack` 使用者聽過並認可。

**⇒ Phase A 結束。此時旁白、上畫面文字、音檔全部凍結；G0 的門關上，Phase B 才能開。**

---

## 5. Phase B — 視覺線（**前置條件：共用層 v1 merge 進 main**）

> **開工前先確認：** `git log main --oneline | grep shared-layer` 找得到 v1 的 merge，
> 且 `KICKOFF-shared-layer-v1.md` 的四項都打勾。**沒有就不要開始鋪原語**——理由見 §1.2。

### B1 — 原語 1–7 鋪滿 22 場

**照 §3.1 的做法（⑬／⑯ 的鋪法，不重新發明）：**

1. **先把 stock reveal 升級**——原語 1 的揭示時序對 **12 個已寫 `{show statement}`／`{show proof.0}`
   的場零成本生效**（§2.3 第 9 列），先確認這些場真的動了再往下鋪。
2. **`paced:` 填長拍**——⑬ 的核心武器，也是唯一能跟著一整拍長的通用走法。
   **`paced` 切 n 個間隔而不是 n−1**（只切段間的話兩段的 block 會在前半拍放完、後半拍整片靜止＝
   把病灶搬家）。⚠️ **改成 `anim: transform` 的列會失去 `paced`**（callable 免檢，
   `[stillness]` 抓不到）——⑮ 的教訓，07 首跑 result 拍靜止 15 s 而閘沒響。
3. **hook 只給真的需要的場**——⑧ 的數據：`corr(verdict, hook) = −0.11`，
   hook 場與純模板場的 verdict 均值幾乎相同，全片最差的一場正是最自由的那一場。
   §3.2 已有的 2 個 hook（Fig 3.5／3.6）繼續用；**要不要加第三個，等 B2 的量測說話。**
4. **`carry:`／`focus:`／`seg_roles`／`meta.color_map`** 依 §2.3 的表補。
   §3.2 的天然 carry 候選＝證明四場之間（`R_3(h)/h` 這條主線橫跨 `proof_setup_substitution`
   → `proof_easy_piece` → `proof_delicate_choices` → `proof_delicate_bound`）。
5. **例題場用 `worked_example`**（A2 第 4 點已切好模板，這裡鋪它的動作）。
6. ⚠️ **順手把 `animations/ch03_chain_rule_hooks.py` 的 `_fade` 遷成 `_elapsed` 量測值**
   （§2.4 第 4 點）——**前提是 `make.py` 的 `disable_caching: True`**，快取開著時
   `renderer.time` 是標稱值、`_elapsed` 會無聲退化。

**紅測試先行（G6）：** 這一批只要碰到「本來就該成立但壞掉」的事（例如 `_fade` 報假秒數），
**先寫紅測試再修**。

### B2 — 一次 1080p render ＋ 兩道硬閘

```
python video/make.py --storyboard video/storyboards/ch03_chain_rule_mimo.yml \
       --reuse-audio --quality high
```

**硬閘 ①（`[sync]`，render 後、compose 前，`make.py` 自己 abort）：**
影片短於旁白、或 |video − expected| 超過 `SYNC_HARD_GATE_FRAMES` ＝ **2 影格**
（fps 由 ffprobe **對成品實測**）⇒ **ERROR、abort**。`[sync] render/audio lengths clean` **必須**出現。

**硬閘 ②（`rewatch_pack --gate-still`）：**

```
python video/pipeline/rewatch_pack.py --deck ch03_chain_rule --out <round dir> [--baseline <上一輪 pack dir>]
```

- `[still-gate] PASS` 才算該輪完成；**exit 1** ＝ 有 content 場的 0.05% 細門檻最長靜止
  超過 **12 s**（預設，沒有關閉開關），FAIL 行帶所在拍；**exit 2** ＝ 基線 fps／尺寸不同、拒絕 A/B。
- ⚠️ **`--scene` 子集一律另給 `--out`**，否則整個覆寫 `INDEX.md`／`pack.json`。
- ⚠️ **定位死區看 fine（0.05%）不看 coarse（0.2%）**——一個字形在 192×108 灰階下只有 2×3 px，
  coarse 看不見字形書寫，會把死區指到錯的拍（⑱ 的場 09 連改兩次的成因）。

**其餘閘：**

```
python video/pipeline/run_selftests.py     # 全綠（開工基線 42）
python video/pipeline/schema.py   …        # structure OK、0 error
python video/pipeline/sizecheck.py …       # 0 error
python video/pipeline/critic.py --dry-run --out <round dir>   # 抽幀，逐輪隔離留底
# gate-1 subagent（免費）：visual-frame-audit（V1–V10 blocking ＋ A1–A7 magnitude）→ blocking == 0
```

### B3 — 輪內回歸清單（G2）

**每一輪產一張表，只有三欄：**

| 上一輪 finding | 已關／未關 | 證據（幀／量測／commit） |
|---|---|---|

- **新 must 上限 3 條。超過 ⇒ 退回內容階段**（本檔 §3.1 的 G0 內容鎖），不要繼續拋光。
- **輪內不跑生成式盲審。** 理由（`KICKOFF-process-reform.md` §1.2）：§3.1 的視覺 advisory
  是 6＋2 → 9 → 8 → 10，**修完又長回來、數量幾乎不變**——不是沒修好，是每輪重新生成；
  片子越好評審標準跟著抬高。
- 需要就再一輪，**照 G5 批次化**：收齊 must → 併行派工 → 一次 merge → 一次 render → 一次再審。

---

## 6. 停止條件與里程碑審

### 6.1 停止條件（**開工前就寫死在這裡，不是事後判斷**）

**四條同時滿足即收工，剩下的 `should` 進 backlog：**

1. **視覺 blocking ＝ 0**
2. **R2 must ＝ 0** —— 輪內的意思是：上一次里程碑審的 must 全部關閉，且輪內回歸清單沒有新 must；
   節收斂時才跑一次完整六鏡（含 R2）確認。
3. **量測指標連續兩輪無實質改善**（fine 最長靜止**逐場** |Δ| < 0.5 s）
4. **`[sync]` ＝ 0、`run_selftests` 全綠、`sizecheck` 0 error**

> 依這條，§3.1 **在第 ㉑ 輪就該停**（㉑ 的 21 場 fine 逐場 ±0.0，沒有動到任何驗收指標）。
> **§3.2 不要重演。**

### 6.2 里程碑審（達標後跑一次，只跑一次）

```
python video/pipeline/rewatch_pack.py --deck ch03_chain_rule --out <milestone pack>
```

- **完整六鏡盲審：R1 初學者 ×2／R2 動畫導演／R3 教學設計／R4 節奏剪輯／R5 講師**
  （契約＝[`REWATCH-REVIEW-RUBRIC.md`](content_scripts/_audit/REWATCH-REVIEW-RUBRIC.md)）。
- **跨模型家族：agy ×3（外部 API，逐次徵同意）＋ subagent ×3。**
  agy 的 headless 用法與盲審隔離（cwd 設 repo 外、`--add-dir` 圈定可讀範圍）見根 `CLAUDE.md`。
- finding 可標畫面語法規則代號 `rule: ML1`–`ML5`（R2 MUST），digest 的 `by_rule` 按規則計數。
- **R1a 的模型要換**——⑬ 的紀錄：Gemini 3.1 Pro 在初學者鏡上模板化套門檻、已降權。
- **must 一個批次輪關掉**（G5）；**should 進 backlog**，不在本節處理。

### 6.3 4K final

停止條件四條全滿足、里程碑審的 must 全關之後：`make.py … --quality 4k`。
**共用層 v1 已經是前置條件，所以不會再有「v1 落地要重 render」的問題。**

---

## 7. 每節成本表與 SOP v1（**這一節的第二個交付目標**）

### 7.1 成本表——每個 phase 結束填一次

**表在 [`REBUILD_STATUS.md`](REBUILD_STATUS.md) 的「每節成本量測」節，§3.2 那一列現在全是「待記」。**
**不要等收工才回填**——§3.1 的那一列是事後估的，所以只能寫「單景打磨 8 項×80–216k」這種沒法比較的數字。

| 欄位 | 怎麼量 | 填的時機 |
|---|---|---|
| audit／撰稿 tokens | 每個 gate-1 subagent 回報的 token 數累加；Codex／agy 的 `usage` 欄 | 每個 phase 結束 |
| render 次數 | 1080p 全片 render 的次數（mock 的另計） | 每輪 +1 |
| 客製 hook 數 | storyboard `hook:` 欄的場數（開工基線＝2） | B1 結束 |
| 真 TTS calls | `manifest.json` 的計費收據 `backend_calls` 累加（含重合成與 fallback） | A5 結束、之後每次重合成 |
| 回歸輪數 | §5 B3 的輪數 | 收工 |

**另外記三個 §3.1 沒有的數字**（給並行階段排程用）：

- **牆鐘時間**：Phase A／Phase B 各自的日曆天數與實際工作時數。
- **停等點的等待時間**：A1 sign-off、A5-1 報價同意、A5-3 聽感人閘、§6 agy 同意——四個。
- **並行摩擦**：merge 衝突次數、等別人 render／tts 時間窗的次數、TeX cache race 撞車次數。

### 7.2 SOP v1 —— `video/KICKOFF-section-template.md`

**跑完 §3.2 之後，從本檔抽出模板：**

1. **把 §3.2 專屬的數字換成佔位**：`<DECK>`／`<SECTION>`／`<場數>`／`<字數>`／`<秒數>`／
   `<.tex 行區間>`／`<hook 數>`／`<核准 call 數>`。
2. **保留的是結構與紀律**：§0 啟動提示、§3 護欄（G0–G7 的具體形狀）、§4 A1–A5 的順序與判準、
   §5 B1–B3、§6 四條停止條件、§7 成本表欄位、§8／§9。
3. **§2「現況與已驗證 code 事實」改成一張待填的查證清單**——每節開工的第一件事就是照著跑一遍
   （這一節的 §2 就是那份清單的實例）。
4. **把「這一節踩到的坑」獨立成一節**，比照 `KICKOFF-s31-amplify.md` §1「本輪學到、下一輪會再踩的三個坑」。

### 7.3 協定跑不通的地方要回寫 `REVIEW_GATES.md` §六

**本節是 §六的第一次實測。** 任何一條 G0–G7 在實際執行時「做不到」「意思不清楚」「與別的條款打架」，
**當場記下來，收工時回寫 §六**——§六是驗收定義的 SSOT，kickoff 只是當時的檢討紀錄。

**已知的三個觀察點（本檔立檔時就看得到，收工時回答）：**

- **6.4 開工清單第 1 項**（`run_selftests` 全綠）在本節開工時就綠（42），
  **但 §2.3 發現的 TeX cache race 不在清單上**——要不要加一條「量測閘一次只跑一支」？
- **6.2 的「輪內新 must 上限 3」在 Phase A 沒有對應物**——內容階段的 must 怎麼算？
  （A1 的跟改單元數？NFA 的 blocking 數？）§六沒寫。
- **6.3 停止條件第 2 條依賴「上一次里程碑審」**，但**第一節沒有上一次**——
  §3.2 的第一輪要怎麼判？（本檔的答案：第一輪只看第 1、3、4 條，第 2 條從第二輪起生效；
  若 §六同意，回寫進去。）

---

## 8. 明確不做（連同理由）

| 不做 | 理由 |
|---|---|
| **不改共用層** | 字體／字級／`theme.py`／`brand.py`／`templates/`／`sizecheck` 規則是工具線 [`KICKOFF-shared-layer-v1.md`](KICKOFF-shared-layer-v1.md) 的檔；兩條線同時改同一個檔＝⑯ 那種搶檔面。**發現需要就記進下方 backlog。** |
| **不做畫面語法缺口 T2–T4** | [`KICKOFF-motion-language-gaps.md`](KICKOFF-motion-language-gaps.md) 的 T2（inset＋框選＋閃爍）／T3（token 級變形＋兩段式消去）／T4（跨場攜帶）已在 ⑮ 落地，**沒落地的部分屬工具線**，本節只「用」不「改」。 |
| **不並行開 §3.3** | 裁決 4：先用 §3.2 把流程走成熟、產出 SOP v1，**之後**才並行。§3.3 的 `envexample` 有 8 個（`ex:3.9`–`ex:3.16`，`chapter3.tex:426–579`），體質與 §3.2 不同，不要在流程還沒定型時開。 |
| **不做新舊 A/B** | 裁決 3 取消。 |
| **不碰 §3.1** | 收尾（里程碑六鏡＋4K final）**另開對話**（裁決 7）。 |
| **不自行重試 §3.1 的 3 場 FA 降級** | 使用者裁決「先不用」修，重試會燒 billed API。 |

**工具線 backlog（本節發現、寫給 [`KICKOFF-shared-layer-v1.md`](KICKOFF-shared-layer-v1.md) 或另案）：**

- ⚠️ `animations/ch03_chain_rule_hooks.py:57` 的 `_fade` 仍回傳寫死秒數（§2.4 第 4 點）——
  **B1 順手遷**，但 `pipeline/` 裡的同款殘餘（`pacing.walk`／`play_block` 標稱值、每拍 wait 整幀進位）
  屬工具線。
- ⚠️ 量測閘的 TeX cache race（§2.3）——`sizecheck.py` 同時跑兩支會吐假 error，
  要不要加檔案鎖或在 `REVIEW_GATES.md` §六 6.4 加一條紀律。
- `rewatch_pack` 的 `_beat_at` 對跨拍靜止段回空字串、FAIL 行尾無所在拍（流程改革輪已記）。

---

## 9. 完成定義（DoD）

**全部滿足才算 §3.2 做完：**

- [ ] **成片**：`output/ch03/s3.2/ch03_chain_rule_mimo.mp4` 1080p 過**兩道硬閘**
      （`[sync]` clean、`[still-gate] PASS`）＋ **4K final**（§6.3）
- [ ] **§6.1 四條停止條件同時滿足**（視覺 blocking 0／R2 must 0／量測連兩輪 |Δ| < 0.5 s／
      `[sync]` 0 ＋ selftest 全綠 ＋ sizecheck 0 error）
- [ ] **里程碑六鏡審跑過一次**，must 全部關閉（should 進 backlog）
- [ ] **REVIEW HTML：每個 phase 一份 applied 報告**（根 `CLAUDE.md` 規定：凡完成一輪內容撰寫
      都要對實際寫入的內容產 standalone HTML、MathJax/KaTeX CDN、雙擊即開）
      —— 至少 `REVIEW-ch03_chain_rule-s32-phaseA-applied.html`／`…-phaseB-applied.html`
- [ ] **NFA 版控 REPORT** 寫完，裁決在 commit body（`git log --grep="NFA"`）
- [ ] **`[source_rev]` WARN 消失**（stamp 換到 `chapter3.tex`）
- [ ] **`REBUILD_STATUS.md` 的「每節成本量測」表 §3.2 那一列填滿**（§7.1 的五欄＋三個新數字）
- [ ] **SOP v1 產出**：`video/KICKOFF-section-template.md`（§7.2）
- [ ] **`REVIEW_GATES.md` §六回寫**：協定跑不通的地方已記（§7.3 的三個觀察點至少要有答案）
- [ ] **`REBUILD_STATUS.md` 更新**：§3.2 狀態列改成完成、Open items 的「下一步」推進到並行階段

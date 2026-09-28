# video 產線審核閘一覽（review gates map）

> **本檔是地圖／索引，不是權威。** 每道閘的權威定義仍在它的「home doc」（見各列「權威文檔」欄）；
> 這裡只把散落在 [README.md](README.md)、[DESIGN.md](DESIGN.md)、[CONTENT_METHODOLOGY.md](CONTENT_METHODOLOGY.md)、
> [RUNBOOK-mimo-narration-route.md](RUNBOOK-mimo-narration-route.md)、[REBUILD_STATUS.md](REBUILD_STATUS.md) 與
> 根目錄 [`../CLAUDE.md`](../CLAUDE.md)／[`../README.md`](../README.md) 的審核機制收斂成一張表，方便一眼看全貌。
> 整理日期：2026-06-15。內容若與 home doc 牴觸，以 home doc 為準，並回頭修本檔。
>
> **2026-09-28 Remotion 統一後的狀態標記**（契約＝[`KICKOFF-remotion-unification.md`](KICKOFF-remotion-unification.md)）：Manim gen-2 引擎已封存到
> [`../legacy/manim_video/`](../legacy/manim_video/)。本檔各閘加標——**〔Manim gen-2 閘，已封存〕**＝閘的程式隨引擎進了 legacy，表列內容只存歷史；
> **〔沿用，待接 Remotion〕**＝內容層閘，契約不變，但它讀的 storyboard／成片佈局是 Manim 時代的，接 Remotion 分鏡／成片另開輪次
> （KICKOFF §6）。**層 5（manim hook code）整層退役。** Remotion 版的 `[sync]` 對等閘尚未定義，由 §3.2 Phase B 的 Remotion 版 KICKOFF 定。
> **2026-09-28 晚：KICKOFF §6 第 3 條已完成**——Remotion 分鏡的 render 前結構閘＋內容層確定性檢查器入口＝[`pipeline/check_storyboard.py`](pipeline/check_storyboard.py)
> （層 6 新列；欄位契約 SSOT＝[`SPEC-remotion-storyboard-schema.md`](SPEC-remotion-storyboard-schema.md)），`tools/doctor.py --smoke` 同日重掛為對 `paper/*/*.yml` 全跑。

## 總綱

產線分**七個產物層**，每層各有審核閘。能真正**擋住 render** 的只有 storyboard/timing 與兩軌 parity 的幾個**自動腳本閘**（其中 storyboard/timing 的 schema／lint／sizecheck／`[sync]` 已隨 Manim 封存；Remotion 分鏡的結構閘＝`check_storyboard.py`，2026-09-28）；
內容／旁白／視覺層全為 **advisory**——模型（Codex / MiMo / Claude）或人提案，最後由人裁決，**稽核者一律唯讀、不自己改檔**。
**2026-09-13 補**：層 7 另有一道確定性硬閘 `rewatch_pack --gate-still`（POST-render），它擋的不是 render，而是**該輪的完成**（見 §六）。

流向：講義散文 →（Stage-1）內容稿 → 旁白稿 → 口語版 → 分鏡／timing → render 成品（2026-09-28 起渲染＝Remotion；Manim 時代在口語版與 storyboard 之間另有「manim hook code」一層＝層 5，已退役）。（「Mode」一詞專留講義 A/B/C；影片內容稿階段稱 **Stage-1**——見 [REVIEW_MODEL_DECISIONS.md](REVIEW_MODEL_DECISIONS.md) 詞彙紀律。）

**Phase 索引**（同一條線的四段粗分，方便對話指稱；不是新狀態機）：

| Phase | 涵蓋層 | 主要閘 |
|---|---|---|
| Content | 層 2–3 | six-lens、copyedit、旁白 sign-off（lock） |
| Derivation | 層 4 | derive parity、NFA |
| Storyboard | 層 6（層 5 已退役） | `check_storyboard.py`（結構＋provenance/pedagogy/SC/EX 確定性層，2026-09-28 接 Remotion）、pedagogy/OTF/SC 判斷閘、amplification（沿用，待接 Remotion）；工程鏡與 schema/lint/sizecheck 已封存 |
| Render | 層 7 | 視覺 gate1、REWATCH、`--gate-still`（沿用，待接 Remotion）、人工驗收；VLM gate2（`critic.py`）已封存 |

圖例：**■ 自動腳本・可擋 render**　**□ LLM 稽核・advisory**　**◆ 人工閘**　**◷ 未建（TODO）**

> **gate 1 具名 subagent（2026-06-17；2026-06-30 補 pedagogy）：** 五道判斷閘（2026-09-28 工程鏡退役後剩四道）的 gate1 已可用 `.claude/agents/` 具名 subagent 跑（唯讀 `Read/Grep/Glob`、薄提示引用各 SSOT rubric，比照講義 `handout-prose-audit`）：[`narration-faithfulness-audit`](../.claude/agents/narration-faithfulness-audit.md)（NFA）、[`narration-copyedit`](../.claude/agents/narration-copyedit.md)、[`visual-frame-audit`](../.claude/agents/visual-frame-audit.md)、`hook-engineering-audit`（2026-09-28 隨層 5 退役、定義檔已刪）、[`pedagogy-firstlearner-audit`](../.claude/agents/pedagogy-firstlearner-audit.md)（讀 storyboard＋cited `.md`＋handout，PRE-render；與讀 render 後幀的 `visual-frame-audit` 同 gate1 tier、不同 stage）。**另有 [`video-amplification-audit`](../.claude/agents/video-amplification-audit.md)（敘述放大機會稽核、propose-not-act、永不 blocking；2026-07-01）。** 六鏡維持 multi-agent Workflow；gate2（Codex／外部 VLM）是外部模型、**不是** subagent（仍走 `codex exec`；外部 VLM 的 `critic.py --confirm` 已隨 Manim 封存；thin-prompt 模板 `PROMPT-narration-*.template.md` 留給 Codex gate2）。

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
| **〔沿用；只適用「正典＋口語」雙軌的節——正典 storyboard 已隨 Manim 封存，Remotion 分鏡直接寫口語時沒有這道〕** `derive_spoken.py --check` | 確定性腳本（離線、免費） | ■（擋，exit 1） | 兩軌 parity：每個 canonical say 對齊（無漏／多 id）、`{show}` 標記逐一一致、無 `$`／LaTeX 漏進口語。每次改 `spoken.yml` 後重跑 | [README.md](README.md) §MiMo 路線、[DESIGN.md](DESIGN.md)；步驟見 [RUNBOOK-mimo-narration-route.md](RUNBOOK-mimo-narration-route.md) step 2 |
| NFA 旁白忠實稽核（lock 後；原 Mode B） | gate1 Claude subagent（免費、迭代到 blocking==0；reader 拆法見 rubric）→ gate2 Codex（計費、收斂後單次、需同意；ch01 記錄 gpt-5.5 reasoning xhigh） | □（每條標 [Blocking｜Advisory]；收斂＝**blocking==0**） | 七維 D1–D7：D1 HTML 逐字忠實、D2 口語逐字等同（只把數學符號念成字）、D3 數學唸法（`f^{-1}` 須念「f inverse」）、D7 數學正確（`CONTENT_APPROVED=no` 時必跑、獨立重算、開隔離盲 reader）。**不得改已核可 source**；裁決寫進修正 commit body（`git log --grep="NFA"`） | **SSOT [NARRATION-FAITHFULNESS-RUBRIC.md](content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md)**；thin prompt [PROMPT-narration-faithfulness.template.md](content_scripts/_audit/PROMPT-narration-faithfulness.template.md)；commit 慣例 [`../CLAUDE.md`](../CLAUDE.md) |

### 層 5｜manim hook code（生成動畫程式）——**已退役（2026-09-28）**

> Manim gen-2 的 `hook:` 機制隨引擎封存；工程鏡 rubric 在 [`HOOK-ENGINEERING-RUBRIC.md`](../legacy/manim_video/content_scripts/_audit/HOOK-ENGINEERING-RUBRIC.md)（legacy），
> `hook-engineering-audit` agent 已刪。Remotion 場景 code 的稽核閘待定（見 [`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md) §5）。下表只存歷史。

| 閘 | 執行者 | 性質 | 把關內容 | 權威文檔 |
|---|---|---|---|---|
| **〔已退役〕** 工程鏡（生成 hook code 稽核） | gate1 Claude subagent（免費、讀 `review_pack.py` 組的 engineering packet）→ gate2 Codex（計費、收斂後單次、需同意） | □（收斂＝**engineering blocking==0**） | **單鏡頭**：只看生成 hook code 的數學保真（E1，blocking）與慣例（E2；theme primitive 不用 hex、實心／空心點語義、SAFE_MARGIN），**不看美學**（歸 VISUAL-FRAME）。與 VISUAL-FRAME **V8 邊界**配對：V8 查幀上可見數學、本鏡查生成它的 code。**2026-06-16**：DeepSeek 退場、改兩讀者；忠實／語域／拆解三鏡已歸 CONTENT-SIXLENS；math context 改吃內容稿動畫單元 narration／`source`（脫離已搬 `legacy/` 的 `.tex`） | **SSOT [HOOK-ENGINEERING-RUBRIC.md](../legacy/manim_video/content_scripts/_audit/HOOK-ENGINEERING-RUBRIC.md)**；assembler [pipeline/review_pack.py](pipeline/review_pack.py) |

### 層 6｜storyboard／timing

| 閘 | 執行者 | 性質 | 把關內容 | 權威文檔 |
|---|---|---|---|---|
| **〔Manim gen-2 閘，已封存〕** `lint.py` | 腳本，make.py render 前跑（`--skip-lint` 可繞） | ■ error／warn | error（abort）：純文字欄出現 `$`／反斜線、`$` 不成對；warn：手動 `\\`、空心點用在已達值 | [DESIGN.md](../legacy/manim_video/DESIGN.md)、[README.md](README.md) |
| **〔Manim gen-2 閘，已封存〕** `sizecheck.py` | 腳本，與 lint 並行（`--skip-sizecheck` 可繞） | ■ error／warn | error（abort）：同層 prose 字級不一、元素出框；warn：教學散文用 muted 色、超安全邊界、內容塊重疊。**盲點**：**這幾項**只查 `brand.prose`，不查直接構造的 `MathTex/Text`（2026-09-14 T3 起，新增的 L1 結論字級規則走全樹 `_type_nodes`、不受此限；下一列）。**並行安全（2026-09-14 r2 Task H）**：本閘建 Tex 的整段由 [`pipeline/texlock.py`](../legacy/manim_video/pipeline/texlock.py) 的 per-cwd 檔案鎖（`<media_dir>/Tex.lock`）互斥，同一 cwd 的第二支**等待**（每 10 s 印 `[texlock] waiting for pid N …`）而不再吐假的 `ERROR … could not build scene`；`make.py` 的 preflight 與 render、`critic.py --per scene`、`scratch_frames.py` 同掛，跨 worktree／跨 cwd 天然不互斥 | [DESIGN.md](../legacy/manim_video/DESIGN.md)；source [pipeline/texlock.py](../legacy/manim_video/pipeline/texlock.py)＋測試 [pipeline/_selftest_texlock.py](../legacy/manim_video/pipeline/_selftest_texlock.py) |
| **〔Manim gen-2 閘，已封存〕** `sizecheck.py` fontfloor 最小字級 floor | 腳本，與 sizecheck 同跑（make.py-time、確定性） | ■ warn（warn-default；`meta.fontfloor_enforce` 開才 error／abort，預設關、landing 不擋） | 浮現「真實上螢幕字級 < `MIN_FONT_FLOOR`＝26px」的 `_brand_prose` 節點（render 前的工程對應物）；配 render 期 clamp（把縮過頭的節點托回 floor）＋ agent 在幀上肉眼施作的**手機寬尺標**（P6，~360–414px 視窗仍要讀得到）。與 VISUAL-FRAME V4／A6 配對：floor 浮現「小到讀不到」、V4 升 blocking／A6 扣分。**執行期＝`floorprobe`**（2026-09-14）：本列量的是 **build 佈局的 authored px**，`carry: to.scale`／hook 自建 `MathTex`／`\tfrac` scriptstyle 內縮／執行期 `.scale()` 它都看不到；`pipeline/floorprobe.py` 掛在 `scene.py` 每拍末與 `_tail` 前走 scene 的 mobject 樹補量，render 後由 `make.py` 印 `[floorprobe] …`，**永遠 warn-only**（幀已畫完，無可擋者）、無 `_enforce` 旗標 | [pipeline/visuals/theme.py](../legacy/manim_video/pipeline/visuals/theme.py)（`MIN_FONT_FLOOR`，SPEC §8）／[pipeline/sizecheck.py](../legacy/manim_video/pipeline/sizecheck.py)（floor check）／[pipeline/floorprobe.py](../legacy/manim_video/pipeline/floorprobe.py)＋[pipeline/_selftest_floorprobe.py](../legacy/manim_video/pipeline/_selftest_floorprobe.py)（執行期）／[pipeline/brand.py](../legacy/manim_video/pipeline/brand.py)；rubric [VISUAL-FRAME-RUBRIC.md](content_scripts/_audit/VISUAL-FRAME-RUBRIC.md) V4／A6 |
| **〔Manim gen-2 閘，已封存〕** `sizecheck.py` 設計系統規則（LayoutRules L1–L3／MathRules M1–M3；**2026-09-14 T3 新增**） | 腳本，與 sizecheck 同跑（build-only、確定性、不 render） | ■ warn（**六條全部 warn-default**；`meta.layout_enforce` 開才把 L 系升 error／abort、`meta.mathtype_enforce` 開才升 M 系，兩者預設關、landing 不擋） | 把設計畫布九條規則裡**可確定性判定的六條**落成閘。**L1** 結論（`result`／`qed` 區塊）字級被鋪陳元素壓過 ≥ `L1_WEIGHT_RATIO`=1.15 倍（量的是**全樹** `_effective_font_px`，不是只看 `brand.prose`——結論多半是 `math_line` 的 `MathTex`；masthead 與 decoration 層不算鋪陳）／**L2** 下三分之一的 bbox 聯集覆蓋 < `L2_MIN_FILL`=15%／**L3** 主內容寬 < `L3_MAIN_W_FRAC`=58% 又沒開 `aside:`、也沒置中／**M1** 數學欄位含 `\text{}`／`\mbox{}` 或連續兩個以上裸英文字／**M2** 同一個 `reason` 同時有 `$…$` 與裸英文（語域混用）／**M3** 已知運算元名寫成裸字母（`sin` 而非 `\sin`）。**L 系讀 build 出的幾何、M 系讀 storyboard 原文。** 分流表見下方。**升硬閘的條件**＝某節自行開 `meta.<flag>_enforce: true` 跑完一輪零誤報，**下一輪才討論改預設**（T3 本輪明確不改預設） | [DESIGN.md](../legacy/manim_video/DESIGN.md) §設計系統規則落地；規則原文 [`_audit/design-template-system/LayoutRules.dc.html`](../legacy/manim_video/_audit/design-template-system/LayoutRules.dc.html)／[`MathRules.dc.html`](../legacy/manim_video/_audit/design-template-system/MathRules.dc.html)；source [pipeline/sizecheck.py](../legacy/manim_video/pipeline/sizecheck.py)；測試 [pipeline/_selftest_layout_rules.py](../legacy/manim_video/pipeline/_selftest_layout_rules.py)＋fixture [storyboards/_fixtures/layout_rules.yml](../legacy/manim_video/storyboards/_fixtures/layout_rules.yml) |
| **〔Manim gen-2 閘，已封存；它掛的 provenance／pedagogy／coverage／source_rev／example_coverage 檢查器留在 `pipeline/`，2026-09-28 起改由下一列 `check_storyboard.py` 掛〕** `schema.py` | 腳本，make.py render 前跑（`--skip-schema` 可繞） | ■ error／warn | **已建（2026-06-16）**：結構驗證（meta.id／section 必填、scene kind∈intro/content/divider/outro、id 唯一、content 需 template＋say、`{show}` 不閉合→error）＋列舉每場 `{show}` reveal 目標（`--list`）。**不**驗 target 是否存在於模板 payload（需 `reveal_targets()`／manim，屬 task #6）。**2026-06-30 增掛（2026-07-01 加 SC）**：OTF provenance／pedagogy ＋ **SC step-coverage** 結構 warn-checks 在此並跑（warn-default，`meta.otf_enforce`／`meta.pedagogy_enforce`／`meta.coverage_enforce` 開才 abort、預設關），即下方 `pedagogy-firstlearner-audit` 判斷閘的確定性底材。**2026-09-12 增掛 `source_rev`**（LOCKED 內容稿標頭的講義源 stamp vs 現檔；**永遠 warn-only**，WARN＝走 CONTENT_METHODOLOGY §8；`make.py`／`derive_spoken.py` 同掛）；`doc:` 錨池改為凍結 legacy standalone ∪ `.tex` label key（`doc:sec:`／`thm:`／`fig:`…）；`<deck>_mimo` 的 md／SC／source_rev 查找統一走 `provenance.content_script_for`。**2026-09-12 增掛 `example_coverage`（EX 層，例題折疊宣告閘）**：講義該節的 worked example（`\begin{envexample}{…}{ex:…}{}`，按 `\sechead` 區間歸節——**`ex:` 是章序不是節序**）比對內容稿單元的 `examples:`／`folds:` 宣告；EX1＝既沒教也沒折（`meta.example_coverage_enforce` 開才 error）、EX2＝宣告不成立（恆 warn）。**只接在此、不接 `make.py`**（同 SC：例題選材是撰稿期決定，不擋 render）；deck 無 `.md` 整個跳過。**閘只查宣告存不存在，不判折疊對不對**——語意歸下方 `pedagogy-firstlearner-audit` 的 `EX-adv` 與 REWATCH R5。**2026-09-14 增掛 `paced` 無 rail warn**（`_paced_no_rail_issues`）：`paced:` 列出的 derivation `anim: transform`／`cancel` 列若沒有 `reason`，它沒有 rail 可隨讀——morph 播完、整拍 hold；恆 warn，不擋 render。**這條只能由 schema 出聲**：`make.py` 的 `[stillness]` 對列在 `paced:` 的 reveal 一律免檢，看不到這種「宣告 paced、實際整拍靜止」的拍（§8 backlog ⑯）。**2026-09-14 r2 Task I 補閘覆蓋（兩個模板盲區）**：(a) provenance 的 `_present_text_fields` 加掃 **`procedure_steps` 的 `steps[].text`**（該模板把每個 step 的 text 以 `brand.prose` 上畫面，在此之前它一個文字欄都沒被掃——OF2 對該模板等於空跑，`ch03_chain_rule` 的 `decomposition_strategy` 整場無 `ref:` 也沒被報）；`math`／`worked[]` 是數學不掃，且**以 `template:` 為閘**（`steps[]` 與 derivation／worked_example 共用）。(b) `step_coverage._SCOPED_TEMPLATES` 加 **`procedure_steps`**（`coverage_enforce` 下「單元必須有 `screen_contract`」的模板集；SC1／SC2 本身與模板無關）；**`definition_math` 本輪不加**——單一陳述框不是步驟序列、全 23 deck 無一個 definition 單元宣告 `required_steps`，且 `ch03_trig_derivatives{,_mimo}` 已開 `coverage_enforce`，加了會立刻多 6 條 `[SC]` error（r3 再議）。(c) **`screen_contract` 解不開不再靜默**：`_screen_contract.parse_block` 對 YAML 語法錯回 `ParseError`（非 `None`），SC 印成獨立的 `[SC] <unit>: screen_contract failed to parse -- <err>`，**恆 error、不吃 `coverage_enforce`**（契約壞掉是撰稿 bug，不是可 opt-out 的覆蓋政策），且該單元不再同時被報成「沒寫契約」——原本一個非法轉義（§3.2 實踩雙引號 `tex:` 裡的 `\c`）會讓整份契約從閘視野消失、訊息把人導向「去寫一份」。deck 級 smoke＝`python tools/doctor.py --smoke`、模組級＝`python video/pipeline/run_selftests.py` | [DESIGN.md](../legacy/manim_video/DESIGN.md)、[README.md](README.md)；source [pipeline/schema.py](../legacy/manim_video/pipeline/schema.py)（provenance／pedagogy／coverage／example_coverage 落地 [pipeline/provenance.py](pipeline/provenance.py)／[pipeline/pedagogy.py](pipeline/pedagogy.py)／[pipeline/step_coverage.py](pipeline/step_coverage.py)／[pipeline/example_coverage.py](pipeline/example_coverage.py)） |
| **〔2026-09-28 新建：Remotion 分鏡的 render 前結構閘＋內容層閘入口〕** `check_storyboard.py` | 腳本（離線、免費、零 Manim）：`python video/pipeline/check_storyboard.py <片>.yml [--list]`；deck 級 smoke＝`python tools/doctor.py --smoke`（對 `remotion/*/*.yml` 全跑） | ■ error／warn（exit 0＝無 error、1＝有 error、2＝檔讀不到／非法 YAML） | 契約＝**SSOT [SPEC-remotion-storyboard-schema.md](SPEC-remotion-storyboard-schema.md)**。**結構（error）：** `meta.id` 必填、scene `id` 唯一、`kind` 必寫且 ∈ intro/content/outro/divider、content 場 `say` 非空且 `{show}` 不 malformed、**同場 reveal id 不重複**（composition 以 id 查拍）、silent 場 `duration` 正數、`pauses.after` 指向本場揭示過的 id；Manim 遺留欄位（`template`／`focus`／`carry`／`scene_role`…、`meta.color_map`／`meta.video`…）出現＝WARN。**內容層：** 串 provenance（逐欄 OF2＋**場級 `ref:`**——Remotion 場的上畫面文字在 composition、yml 沒有文字欄，場級 `ref:` 是唯一 provenance 把手，缺／解不開＝warn，`meta.otf_enforce` 升 error）、source_rev（恆 warn）、pedagogy（PD3／PD4 武裝；**PD2 以 `template` 為閘，Remotion 上不武裝**）、step_coverage、example_coverage；旗標與嚴重度沿用（warn-default、per-deck opt-in）。**每閘一行武裝狀態**（載了幾個 md 單元／doc 錨／契約、掃了幾場、內容稿在不在）——「clean」與「空轉」分得開（§六 6.2 的武裝前提）。**2026-09-28 對現行四支分鏡實跑（不改分鏡）：** `s31.yml` 0 error／**14 warn**（14 個 content 場全無 `ref:`；`meta.id: s31_unguided` 對不到內容稿、無 `meta.chapter` ⇒ provenance **not armed**）；`q7.yml` 0／12（解題片，本無講義出處）；`act3.yml` 0／5（有 `chapter: "Chapter 3"` ⇒ doc 錨池 49 個已武裝，5 場仍無 `ref:`；`meta.id: ch03_act3_paper` 對不到 `ch03_trig_derivatives.md`）；`q7.zh.yml` 0／14。四支 structure OK、pedagogy clean 但 PD2 不武裝、coverage／example_coverage／source_rev 皆因無內容稿跳過。**待裁決（SPEC §6）：** 場級 `ref:` 缺失 WARN 或 ERROR；PD2／SC 的 Remotion 場角色欄 | **SSOT [SPEC-remotion-storyboard-schema.md](SPEC-remotion-storyboard-schema.md)**；source [pipeline/check_storyboard.py](pipeline/check_storyboard.py)＋測試 [pipeline/_selftest_check_storyboard.py](pipeline/_selftest_check_storyboard.py)＋fixture [storyboards/_fixtures/remotion_minimal.yml](storyboards/_fixtures/remotion_minimal.yml)；場級 ref 落地 [pipeline/provenance.py](pipeline/provenance.py) `scene_ref_issues` |
| **〔沿用，待接 Remotion；確定性底材已於 2026-09-28 接上（上列）〕** `pedagogy-firstlearner-audit`（初學者教學＋上畫面文字忠實） | gate1 Claude subagent（免費；讀 storyboard＋cited `.md`＋handout，**PRE-render**；同 `visual-frame-audit` 的免費 gate1 tier、但不同 stage——它讀 render 後幀，本閘讀 storyboard 源） | □（PD／OF／SC blocking 分開計數；warn-default、per-deck opt-in，landing 不擋） | PD1–PD4 教學品質（beat 粒度、`scaffold.motive` 動機、divider `scaffold.problem`、前提首用 `scaffold.flag`）＋ OF1–OF2 上畫面文字 vs 核准源忠實／可回溯 ＋ **SC1–SC2／SC-honesty／SC-adv 推導步驟覆蓋**（storyboard `covers:` vs `.md screen_contract`：漏步驟／缺 recap／覆蓋誠實；可合併不可掉）；確定性底材＝上列 `check_storyboard.py` 串跑的 provenance／pedagogy／**coverage** warn-checks（gate-1 自有 blocking＝PD1＋OF1＋**SC-honesty**，其餘結構存在性由確定性層算、本閘 surface＋給脈絡；**Remotion 分鏡上確定性層只剩場級 `ref:`＋PD3／PD4——逐欄 OF2 與 PD2 因 yml 無文字欄／無 `template` 而不武裝，agent 要自己讀 composition 的上畫面文字**）。**確定性層看不見的仍要本閘自己看**：`procedure_steps` 的 `steps[].text` 與 `_SCOPED_TEMPLATES` 於 2026-09-14（r2 Task I）才入確定性層，`definition_math` 至今不在 SC 的 contract-必要模板集內 | **SSOT [PEDAGOGY-FIRSTLEARNER-RUBRIC.md](content_scripts/_audit/PEDAGOGY-FIRSTLEARNER-RUBRIC.md)**；agent [`../.claude/agents/pedagogy-firstlearner-audit.md`](../.claude/agents/pedagogy-firstlearner-audit.md) |
| **〔沿用，待接 Remotion〕** **REWATCH 看片多鏡評審**（成片品質；2026-09-12 首用、**2026-09-13 起＝里程碑審**） | POST-render：`pipeline/rewatch_pack.py` 把成片翻成 pack（逐場 contact sheet＋時間軸＋靜止統計）→ 五鏡獨立盲審（R1 初學者×2／R2 動畫導演／R3 教學設計／R4 節奏剪輯／R5 講師；跨 Gemini／Claude 家族：agy ×3＋subagent ×3）→ orchestrator refute-by-default 合成 | □（advisory；**永不 blocking**；餵重做水位裁決） | 唯一「看過影片本身」的審：時間、停留、畫面是否隨數學演化、跟不跟得上；不重審忠實／數學（歸 NFA／L5／OF）。首用＝§3.1 成片（`REVIEW-ch03_s31-rewatch-multilens.html`）。**2026-09-13 起 finding 可標畫面語法規則代號 `rule: ML1`–`ML5`（R2 MUST；[SPEC-motion-language.md](SPEC-motion-language.md)），digest `by_rule` 按規則計數**。**頻率＝里程碑審（2026-09-13 裁決）：一節收斂時跑一次完整六鏡；輪內不跑，改用上一輪 finding 的回歸清單（見 §六 6.2）** | **SSOT [REWATCH-REVIEW-RUBRIC.md](content_scripts/_audit/REWATCH-REVIEW-RUBRIC.md)**；template [PROMPT-rewatch.template.md](content_scripts/_audit/PROMPT-rewatch.template.md)；schema `rewatch-findings.schema.json`；agy 呼叫紀律見根 CLAUDE.md |
| **〔沿用，待接 Remotion〕** `video-amplification-audit`（敘述放大機會稽核；expansion 層 M2） | gate1 Claude subagent（免費；讀 storyboard＋cited `.md`＋handout `expansion:*`，**PRE-render**、propose-not-act） | □（AMP1 advisory；**永不 blocking**、只提候選、逐筆人裁） | 掃 handout `expansion:intuition`／`application` 判影片四態（screened／narration-only／visual-only／missing），只提 `missing` 的承重直覺（綁 `doc:` ＋標記短引文）；correctness caution 路由假設機制、example 歸 `example-supplement`。講義線 `mode-c-gapwalk` 的影片側對應，產 standalone HTML 裁決稿 | **SSOT [AMPLIFICATION-RUBRIC.md](content_scripts/_audit/AMPLIFICATION-RUBRIC.md)**；agent [`../.claude/agents/video-amplification-audit.md`](../.claude/agents/video-amplification-audit.md) |
| **〔Manim gen-2 閘，已封存〕** make.py manifest-freshness（`--reuse-audio`） | 腳本 | ■（fail-fast） | 比對 manifest 與 `<deck>_mimo.yml`（deck id／scene／beat 數／`{show}`／text_hash／WAV 存在與時長），防複用過期音檔；非 reuse 跑時拒絕用 mock 覆蓋真 manifest | [DESIGN.md](../legacy/manim_video/DESIGN.md)、[README.md](README.md)；RUNBOOK step 4 |
| **〔Manim gen-2 閘，已封存〕** sync guard（**2026-09-13 起 render 後＝硬閘**） | 腳本（`pipeline/timing.py` 常數） | ■ | **render 前**：短 beat／純 reveal beat 的啟發式**仍是 warn**（`[sync] short/reveal-only beat`，不擋）。**render 後（硬閘）**：ffprobe 實測每個 content 場的影片長度，與 expected 的偏差 > `SYNC_HARD_GATE_FRAMES`＝**2 影格**（fps 由 ffprobe **對成品實測**、不是猜的；㉑ 成片 30 fps＝0.067 s）→ **ERROR、compose 前 abort**（原為 warn）。旁白長過影片的既有 fatal 不變；手改 manifest 的 beat 總和檢查沿用 `SYNC_TOLERANCE_SECONDS`＝0.12 s。**依據**：㉑ 成片 21 場實測最大偏差剛好 1.0 影格、4 場貼線，1 影格零餘裕 | [DESIGN.md](../legacy/manim_video/DESIGN.md)、[README.md](README.md)、**本檔 §六**；RUNBOOK step 4 |

**〔Manim gen-2，已封存〕設計系統九規則的分流（2026-09-14 T3 定案）。** 規則原文＝設計畫布的
[`LayoutRules.dc.html`](../legacy/manim_video/_audit/design-template-system/LayoutRules.dc.html)（L1–L4）與
[`MathRules.dc.html`](../legacy/manim_video/_audit/design-template-system/MathRules.dc.html)（M1–M5）。**判「只能人審」的都寫出它歸哪個既有判斷閘**——沒有一條是「就這樣算了」：

| # | 規則 | 分流 | 落腳處／理由 |
|---|---|---|---|
| L1 | 結論必須是畫面上最重的元素 | **可自動（T3 落地）** | `sizecheck._conclusion_weight_issues`。**字級那半可量**；「**且必須帶語意色**」那半**歸 VISUAL-FRAME `A7`**（用 accent 凸顯這個 beat 的重點）與 `V10`（語意色一致）——哪個 role 算「語意色」是撰稿判斷，不是幾何事實。實作要點：`_prose_nodes` 只收 `brand.prose` 標記的節點，而結論多半是 `math_line` 出來的 `MathTex`，所以 L1 走**新的全樹 `_type_nodes`**；**既有 muted／floor 檢查維持原路徑不動**（要不要一起改是另案，見 [`KICKOFF-shared-layer-v1.md`](../legacy/manim_video/KICKOFF-shared-layer-v1.md) §8） |
| L2 | 下三分之一不得長期空置 | **可自動（T3 落地）** | `sizecheck._bottom_band_issues`。用 bbox 聯集近似墨覆蓋：bbox **恆 ≥** 框內的墨，所以「連 bbox 都低於門檻」是比規則更強的宣稱——**只會少報，不會誤報** |
| L3 | 右欄有條件展開 | **可自動（T3 落地）** | `sizecheck._main_width_issues`。規則給的兩個出口（開 `aside:`／主內容置中）都可量；圖與表天生置中，因此自動豁免 |
| L4 | 三種佔比依章體質選 | **只能人審（本輪不做）** | 這是 authoring 選擇不是幾何事實，而且 storyboard **目前沒有 `layout:` 欄位**可供比對「宣告 vs 實際」。歸 VISUAL-FRAME `A1`（版面平衡）／`A7`（圖佔比）；欄位本身進 [`KICKOFF-shared-layer-v1.md`](../legacy/manim_video/KICKOFF-shared-layer-v1.md) §8 backlog |
| M1 | 數學行內不得混入散文 | **可自動（T3 落地）** | `sizecheck._math_register_issues`，讀 storyboard 原文（LaTeX 排完之後散文與數學都只是字形，量不回來） |
| M2 | 註解 rail 只有兩種語域 | **可自動（T3 落地）** | `sizecheck._rail_register_issues`。**正典 deck 會大量命中——那是真違反、不是誤報**（`reason: "cancel $h$"`／`"write $h=2\cdot(h/2)$"` 就是規則卡畫的反例） |
| M3 | 正斜體照數學慣例 | **半自動（T3 落地「可判定的那半」）** | `sizecheck._operator_upright_issues` 只查**已知運算元名寫成裸字母**（`sin` vs `\sin`）——那是 LaTeX 原文唯一可判定的部分。**完整的正／斜體判斷（每個變數該斜、每個常數該正）不可從原文判定**，歸 VISUAL-FRAME `V8`（幀上可見數學）與工程鏡 `E1` |
| M4 | ∎ 是字形不是元件 | **只能人審** | 「讀起來像按鈕」是視覺做法問題（`brand.glyph("qed")` 的呈現），不是可量的幾何。歸 VISUAL-FRAME `A2`（吸引力）／`A4`（一致性）；改法進 §8 backlog |
| M5 | 數學字級只有三階 | **已由 T2 覆蓋，不重寫** | [`pipeline/_selftest_type_scale.py`](../legacy/manim_video/pipeline/_selftest_type_scale.py)（AST 掃 `templates/` 的 `size=`）比 sizecheck 更早、更根本地擋住；再寫一條 sizecheck 規則是重複 |

### 層 7｜render 成品

| 閘 | 執行者 | 性質 | 把關內容 | 權威文檔 |
|---|---|---|---|---|
| **〔沿用，待接 Remotion：抽幀來源改 `rewatch_pack` contact sheet 或 ffmpeg 抽幀；`critic.py --dry-run` 已封存〕** 視覺 gate1 ＝ Claude 抽幀 subagent | Claude 讀 `critic.py --dry-run` 抽出的**最滿幀（ink 最大；2026-09-14 起 `--per scene` 不再抽末幀，改抽整場 ink 量最大的一幀，`exit:` 清空畫面的場才不會抽到空幀）**（多模態、免費、每次 render） | □（收斂＝**視覺 blocking==0**） | 逐場 V1–V10 blocking＋A1–A7 magnitude：數學渲染完整、圖正確、表不溢出、reveal 同步、端點實心／空心、✓／✗ 正確、語意色一致（V10，2026-09-13；同一變數在圖與式子 token 不同色＝blocking）（蓋資訊的相撞／關鍵元素出框／reveal 不同步＝blocking） | SSOT [VISUAL-FRAME-RUBRIC.md](content_scripts/_audit/VISUAL-FRAME-RUBRIC.md)（比照 [`../handout/_audit/FIGURE-AUDIT-RUBRIC.md`](../handout/_audit/FIGURE-AUDIT-RUBRIC.md)）；機制 [pipeline/critic.py](../legacy/manim_video/pipeline/critic.py) `--dry-run` |
| **〔Manim gen-2 閘（`critic.py`），已封存〕** 視覺 gate2 ＝ 外部 VLM 信心複核 | ffmpeg 抽幀（免費）→ MiMo-V2.5（外部 API；**公測免費**、間歇、`--confirm`、仍需同意） | □（**不接進 make.py**；定稿前非每輪必跑） | **2026-06-16 已接 VISUAL-FRAME-RUBRIC**：runtime verbatim-inject 整份 rubric body，輸出 V1–V9 blocking findings＋`VERDICT` 行＋A1–A7（每維 0–100，**驅動重 render／排優先的 magnitude**）＋具體缺陷；專抓 sizecheck 漏掉的標籤壓線／碰撞。驅動「判→採→重 render→複驗」迴圈（停止條件＝視覺 blocking==0） | SSOT [VISUAL-FRAME-RUBRIC.md](content_scripts/_audit/VISUAL-FRAME-RUBRIC.md)；[README.md](README.md) §VLM 視覺批改、[DESIGN.md](DESIGN.md)；source [pipeline/critic.py](../legacy/manim_video/pipeline/critic.py) |
| **〔沿用，待接 Remotion〕** **`rewatch_pack.py` 12 s 最長靜止硬閘**（`--gate-still`；2026-09-13 裁決） | 腳本（POST-render、離線、確定性） | ■（擋，exit 1） | 只審 `content` 場，量 **0.05% 細門檻**（`FINE_CHANGE_FRAC`）的**最長靜止**：超過 `--gate-still <seconds>`（**預設 12.0、沒有關閉開關**）→ 印 `[still-gate] FAIL <scene>: … (beat N, <reveal>)`、**exit 1**；全過印 `[still-gate] PASS …`、exit 0。verdict 同時寫進 pack 的 **production view**（**不**給盲審鏡看，免污染盲審）。**不接進 `make.py`**——改由輪次協定規定「render 後必跑」（§六 6.4）。**A/B 同基線**：`--baseline <pack dir>` 比對來源 mp4 的 **fps 與畫面尺寸**（pack 現在會記錄兩者），不同、或舊 pack 沒紀錄 → **拒絕、exit 2、什麼都不寫**（不同 fps 會得出假結論） | 三門檻分工見 [DESIGN.md](../legacy/manim_video/DESIGN.md) §`[stillness]`；**驗收定義本檔 §六**；rubric [REWATCH-REVIEW-RUBRIC.md](content_scripts/_audit/REWATCH-REVIEW-RUBRIC.md) |
| **〔沿用〕** 人工 frame-grab 驗收 | 人工（MiMo route step 4） | ◆ | 在 reveal 時間點抽幀確認 reveal 準時、LaTeX 無亂碼，才 compose／交付 | [RUNBOOK-mimo-narration-route.md](RUNBOOK-mimo-narration-route.md) step 4 |

外加 **MiMo route step 0**：確認該節分鏡存在（含 say＋`{show}`；Manim 時代＝`storyboards/<deck>.yml`，Remotion 現行＝`remotion/<片>/<片>.yml`），否則整條視覺路徑停住——進視覺步驟的 blocking 前置（[RUNBOOK-mimo-narration-route.md](RUNBOOK-mimo-narration-route.md) step 0）。

---

## 二、貫穿全線的 meta-gate（不綁特定層）

1. **四級 finding 分級**——①真衝突要修 ②discoverability gap ③editorial-drift ④非 finding；只報 tier 1–2，避免 over-report。內嵌在六-lens／review_pack／NFA／prose gate。權威：[`../CLAUDE.md`](../CLAUDE.md)。
2. **回歸再審**——修完 blocking／advisory 不得直接宣告完成，須對改動項重跑一輪並把結果記回原稽核文檔。[`../CLAUDE.md`](../CLAUDE.md)。
3. **付費 API 先同意**——任何計費呼叫前要使用者明確同意；腳本以 `--dry-run`（估 token／USD、不送請求）＋ `--confirm`（讀 env key）落實。離線路徑（mock TTS、本地 render、ffmpeg）免。[`../CLAUDE.md`](../CLAUDE.md)。
4. **NFA 裁決寫進 commit message**——subject ≤70、body 逐條「原本／為何不妥／改了什麼／證據」，供 `git log --grep="NFA"` 撈回（講義 Mode B 仍用 `git log --grep="Mode B"`）。[`../CLAUDE.md`](../CLAUDE.md)。
5. **交付物用 standalone HTML**——等使用者過目的稽核產物一律出可雙擊渲染的 HTML。[`../CLAUDE.md`](../CLAUDE.md)。
6. **每判斷閘一條收斂線**——所有 LLM 判斷閘（六-lens／copyedit／NFA／視覺；工程鏡已於 2026-09-28 隨層 5 退役）收斂判準＝**blocking findings==0**；advisory 逐筆人裁、不強制歸零。**不** governs Tier 0 確定性腳本（以 exit code 收斂）。散文類兩讀者（gate1 Claude 免費迭代→gate2 Codex 收斂後單次、需同意），**gate2 只套 copyedit／NFA**——six-lens 本身 multi-agent＋對抗複驗，不再疊 Codex。gate2 的**頻率**依下條矩陣分層。
8. **gate 頻率矩陣（2026-07-07 修訂；理由＝規模從數節變 30+ 節，修訂紀錄見 [REVIEW_MODEL_DECISIONS.md](REVIEW_MODEL_DECISIONS.md) §九）：**

   | 閘 | gate-1（免費） | gate-2（計費） |
   |---|---|---|
   | Tier-0 確定性腳本 | 每次 render | — |
   | six-lens | 每節 | 無（維持既有拍板） |
   | copyedit | 每節 | **每章抽樣＋出版前抽查；高風險節全跑**（原：每節單次） |
   | NFA | 每節 | **每節**（§3.1 實證 gate-2 抓到 gate-1 漏的 D3 blocking） |
   | ~~工程鏡（hook）~~（2026-09-28 隨層 5 退役） | — | — |
   | pedagogy-firstlearner | 每節（pre-render） | 無 |
   | 視覺 frame audit | 每次 final render | VLM（`critic.py`）已隨 Manim 封存 |
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
- **〔Manim gen-2，隨引擎封存〕** ✅ **~~`schema.py` 未建~~（2026-06-16 已建）**：結構驗證＋`{show}` 目標列舉，已接進 make.py render 前閘（`--skip-schema` 可繞）。target-vs-payload 交叉驗證仍待 `reveal_targets()`（task #6、需 manim）。
- **〔Manim gen-2，隨引擎封存〕** **直接構造的 `MathTex/Text` 標籤對 sizecheck 的 muted／floor／sibling 三項仍是盲點**（只靠 VISUAL-FRAME／人眼；2026-09-14 T3 的 L1 結論字級規則例外，它走全樹 `_type_nodes`）；hook code 的數學保真由 review_pack engineering 鏡（advisory）查。
- **〔Manim gen-2，隨引擎封存〕** **整節合併影片**（§1.2／§1.4／§1.5）因 Defender Tex-cache race 尚未驗（逐場已驗）。
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
> **2026-09-28：** 層 6 的 `[sync]` 隨 `make.py` 封存；`--gate-still` 沿用、待接 Remotion。§六 的輪次協定本身（批次化、輪內／里程碑審、停止條件、多 session）與渲染器無關，照舊有效；
> 6.4 開工清單已拿掉 Manim 專屬項（`critic.py --out`、TeX 互斥、schema／lint／sizecheck 手動四閘）。

### 6.1 一輪的定義（G5：批次化）

**一輪 ＝ 收齊該輪全部 must → 併行派工（各自 worktree、各改各的函式）→ 一次 merge → 一次 render → 一次再審。**

**不要一件一輪。** §3.1 的 ⑭–㉑ 八輪跑掉 **8 次全片 1080p render**、每輪派工到 R2 結果約 2–3 小時牆鐘時間；
派工制本身沒問題（24 件改動 19 件一次過），貴的是輪數。

**一輪裡的人閘要簽在對的那一份（G0 相關；2026-09-14 §3.2 實測）：** 內容稿 `.md` 的 `narration:` **不是出片旁白**，
storyboard 的 `say:` 才是——Stage 2 會為口說重新撰寫，兩者措辭**全節不同**（NFA N1-01；§3.1 已裁定這是
known pre-existing doc-sync advisory、非 blocking，**忠實度一律對 `say:` 判**）。由此有兩個後果：

- **把停等點寫成「`_narration.html` 重新 sign-off」是不夠的**：使用者以為簽的是出片旁白，實際上簽的是內容稿。
  而且 `narration_review.py` 只讀 `## meta` 條列與 `### unit:` 區塊、**不讀 header**——§3.2 的 A1 是零跟改、
  只動 header 兩行，`_narration.html` 重編後**逐位元組相同**（連 `git status` 都列不到它），對它 sign-off 是空的。
  ⇒ **零跟改時 sign-off 的對象是對齊報告**，不是 narration HTML。
- **真正的旁白人閘有兩個，兩個都要排進輪次**：① **合成前**的 storyboard `say:` 簽核稿（§3.2 新增；由 A4 gate-2
  的框架層反對促成、使用者裁決採納，見 6.2），② **A5-3 的 `listening_pack` 聽感**（聽到的就是出片的）。
  §3.2 實測有三處「由耳移到眼」（Definition 3.1 的式子、`m_2=f'(g(x_0))`、`alpha_1` 之名都不再被念出），
  這種改動只有在 `say:` 那一份上才看得見。

### 6.2 輪內審 vs 里程碑審（G2）

| | **輪內**（每輪） | **里程碑**（一節收斂時） |
|---|---|---|
| 審什麼 | 上一輪 finding 逐條「**已關／未關**」的回歸清單 | 一次**完整六鏡盲審**（REWATCH 五鏡六份：R1 初學者 ×2／R2–R5） |
| 新 finding | **上限 3 條 must**（見下） | 不設限 |
| 生成式盲審 | **不跑** | 跑一次 |

**理由（kickoff §1.2）：** 生成式 advisory 是**每輪重新生成的**，不是「沒修好」——§3.1 的 blocking 每輪都只有 1 條、
且每次都長在那一輪新改的東西上，advisory 卻是 6＋2 → 9 → 8 → **10**，修完又長回來。片子越好，評審的標準跟著抬高；
**每輪跑生成式盲審＝每輪製造工作。**

**鏡頭產出驗收（lens QA；2026-09-13 §3.1 里程碑審實跑補）：** 收到每一鏡的輸出後，**進合成之前**先驗四件事——
① `lens` 欄與派出去的鏡一致；② `findings[].dim` 的維度代碼屬於該鏡（R1＝`L-`／R2＝`D-`／R3＝`A-`／R4＝`T-`／R5＝`I-`）；
③ `scenes[].id` 是場 id 字串（不是場號）且 27 場齊全；④ 抽驗一條 finding 的數字對得上 pack。
**任一不符＝該鏡作廢重派，不要把錯鏡的 finding 併進 digest**（外部模型重跑要重新徵同意）。
依據：該次三個 agy 鏡有**兩個審了不是自己的鏡頭**（R3 輸出 `L-` 維度、R1a 輸出 `T-` 維度），
根因是工作區佈局而非模型，見 [REWATCH-REVIEW-RUBRIC.md](content_scripts/_audit/REWATCH-REVIEW-RUBRIC.md)「編排」的 agy 隔離條。

**新 finding 上限（G2 假設，2026-09-13 設定）：** 輪內新 must **超過 3 條**，就當成**排序問題**——
**退回內容階段**（§二 第 7 條的內容鎖），不要繼續拋光。依據：⑲ 的五條 must 全是 Task D 拉長旁白後的畫面缺口，
剔除後趨勢是 2 → 2 → 1，本來就是收斂的。

**Phase A（內容階段）的 must 怎麼算（2026-09-14 定案；答 [`KICKOFF-s32-chain-rule.md`](KICKOFF-s32-chain-rule.md)
§7.3 觀察點 2「內容階段的 must 怎麼算，§六沒寫」）：** **Phase A 的 must ＝ 該輪 gate-1 的 blocking 數**；
**advisory 由指揮者逐條裁決，不計入上限。** 依據（§3.2 實測）：pedagogy gate 跑四輪，
blocking **3 → 1 → 1 → 0**、advisory **5 → 5 → 1 → 2**——advisory 每輪重新生成，與上文「生成式 advisory
是每輪重新生成的」是同一個現象，拿它當上限會誤觸退回。
**另一個代價要先知道：** 有些 gate-1 blocking 只能靠**改場結構**關閉，而場結構會動到 TTS 計費——§3.2 的 PD1-2
`decomposition_strategy` 在凍結的 `procedure_steps` 容量下四條出路全堵，唯一出路是 `part:` 分頁＝content 場 +1
＝ **billed call 22 → 23**。⇒ **這類「只能用分場修」的 blocking 必須在 A5（TTS）之前關完**，
否則代價從「多一次呼叫」變成「整場重合成」。

**「某閘 blocking ＝ 0」不等於驗過——武裝前提要一起寫（§3.2 實測）：** A2 的判準寫「SC-honesty blocking ＝ 0」，
但那時 deck 一份 `screen_contract` 都沒有，SC1／SC2／SC-honesty **全部空轉**，綠燈是 **vacuous pass**。
⇒ **凡以「某閘 blocking ＝ 0」為判準，必須同時寫明該閘的武裝前提**（契約已撰寫／旗標已開／有負向對照證明閘會噴，
見 6.5），否則每一節都會拿到假綠。

**gate-2 的 prompt 必須含一個「反對這份 brief 的框架本身」的欄位（§3.2 實測；SOP v1 的 gate-2 模板固定含這一欄）：**
§3.2 的 gate-2（agy Gemini 3.1 Pro High）就是從 `disagreements_with_premise` 那一欄提出**框架層**反對
（內容稿 vs storyboard `say:` 的 SSOT 問題），直接促成使用者新增一個簽核關卡（裁決＝選 B：合成前補 `say:` 簽核點，
見 6.1）。**只會附和第一讀者的第二讀者沒有價值。**

**gate-2 的價值不只是「抓 gate-1 的遺漏」，是「不接受第一讀者與指揮者共同的灰區」（§3.2 實測）：**
N2-01 那條 D2 blocking，gate-1（Claude Opus 5）判 **0 blocking**，而**主對話看過同一處、判為灰區放過**；
gate-2 判它是 blocking，且給的修法（修根因、把指數搬進 LaTeX）比主對話原本採用的（在口語端繞過）**更好**
（修完 23 場 `scene_text_hash` 零變動，commit `201281d`）。⇒ **異家族第二讀者每節必跑是對的。**

### 6.3 停止條件（G3；**開工前就寫死，不是事後判斷**）

**四條同時滿足即收工**，剩下的 `should` 進 backlog：

1. 視覺 blocking ＝ 0
2. **R2 must ＝ 0** — 輪內的意思是：**上一次里程碑審的 must 全部關閉**、且**輪內回歸清單沒有新 must**；
   節收斂時才跑一次完整六鏡（含 R2）確認。（這樣 6.2「不每輪跑生成式盲審」與本條才不矛盾。）
3. **（護欄，不是要件；2026-09-14 修訂）** 量測指標已經不是驅動這一輪的理由。判法分兩種：
   **(a) 本輪是被量測指標驅動的**（為了把靜止壓下去而開）→ 指標**連續兩輪**無實質改善（fine 最長靜止**逐場** |Δ| < 0.5 s）才停。
   **(b) 本輪是被 must 驅動的**，且條件 2 已成立（must 全關、輪內無新 must）→ **指標剛剛改善不構成繼續跑的理由，本條視為滿足**。
   **為什麼要分**（§3.1 里程碑審實跑觸發，使用者裁決）：照原本的字面讀，「這一輪把指標改善了」會導致「尚未連續兩輪無改善」→ 再跑一輪 → 但 must 已全關、那一輪無事可做 → Δ 全 0 → 這時才算收斂。**協定會自己製造一輪空轉，而消滅空轉正是本節寫出來的理由。**
4. `run_selftests` 全綠＋該節分鏡 `check_storyboard.py` **0 error**（2026-09-28 起；原條文還有 `[sync]` ＝ 0、`sizecheck` 0 error——兩者是 Manim gen-2 閘，已封存；Remotion 版的 `[sync]` 對等閘由 §3.2 Phase B 的 Remotion 版 KICKOFF 定義）

> 依這條，§3.1 **在第 ㉑ 輪就該停**（㉑ 的 21 場 fine 逐場 ±0.0，沒有動到任何驗收指標）。

> **一節的第一輪沒有「上一次里程碑審」怎麼判（2026-09-14 定案；答
> [`KICKOFF-s32-chain-rule.md`](KICKOFF-s32-chain-rule.md) §7.3 觀察點 3「第一節沒有上一次」）：**
> **第一輪只看第 1、3、4 條；第 2 條從第二輪起生效。** 理由：第 2 條的字面要件是「上一次里程碑審的 must
> 全部關閉」，第一節／第一輪根本沒有上一次，照字面讀永遠無法滿足——與上面條件 3 分 (a)/(b) 的修訂是同一個毛病：
> **協定不該自己製造一輪空轉。**

### 6.4 開工清單（G4：工具先於內容；**每節開工前逐項打勾再動內容**）

> 〔2026-09-28〕下列 `rewatch_pack` 相關項＝沿用，待接 Remotion（pack 目前還讀 Manim 時代的 storyboard／`output/` 佈局）。

- [ ] `python video/pipeline/run_selftests.py` 全綠（＋`python tools/doctor.py`）
- [ ] `python video/pipeline/check_storyboard.py <片>.yml` **0 error**，且 `[provenance]` 那行不是 `not armed`（該節要有 `meta.chapter` 或內容稿，場級 `ref:` 才解得開；2026-09-28 起）
- [ ] `rewatch_pack` 報得出死區的**位置**與**所在拍**（不只長度）——**已做**
- [ ] A/B 兩包 pack **同 fps／同尺寸**：`rewatch_pack --baseline <pack dir>`（不同就 exit 2）
      **⚠ 基線包必須是 `2124a32` 之後產生的**——`--baseline` 要讀基線包 `pack.json` 裡的 fps／size，
      而那個欄位是該 commit 才加的，**任何更早的留底包一律 exit 2、永遠當不了基線**（2026-09-14
      實跑：`rewatch_pack_after21` 就是這樣被拒的）。留底包的用途就是當基線，這條等於自相矛盾。
      解法：**留底成片**（例如 `<deck>__pre_<milestone>.mp4`）比留底 pack 重要——用現在的工具對
      舊成片重生一包合格基線即可。手上只有舊 pack 時，退而求其次是兩包 `INDEX.md` 逐場比
      `fine longest still`（2026-09-14 §3.1 就是這樣做的）。
- [ ] TTS 依 [RUNBOOK-mimo-narration-route.md](RUNBOOK-mimo-narration-route.md)：`--reuse-existing`／`--no-billing`／`--skip-qa` 的適用範圍
      （reuse key 不含場號——**已做**）
- [ ] **`[still-gate]`（§一 層 7）在**，render 後必跑（原列的 `[sync]` 隨 `make.py` 封存）
- [ ] `rewatch_pack --scene <子集>` **一律另給 `--out`**（2026-09-14 起：不給 exit 2；`--out` 已存在
      且其 `pack.json` 非 subset 也 exit 2——子集一律不得覆寫全包的 `INDEX.md`／`pack.json`）
- [ ] **閘的輸出完整落檔再讀，禁止 `| tail -N`**（實例：已封存的 `sizecheck` 把摘要印在**最前面**，見下）
- [ ] 本節 kickoff §2「現況快照」已標明**量測當日的 main tip hash**（見下）

> **〔2026-09-28 拿掉〕** 原本這裡有兩段 Manim 專屬說明（worktree 裡 `doctor --smoke` 的 deck 閘會略過、改手動跑 schema／lint／sizecheck；
> TeX 建置互斥鎖 `texlock.py`），隨引擎封存；原文見 tag `archive/2026-09-28-manim-gen2-final` 的本檔。其中「**§六 描述別條線的工具行為時，
> 要附『當日 main tip』與可自驗的 grep**，不要只寫結論」這條教訓與渲染器無關，照舊適用。

> **`| tail -N` 為什麼寫成硬規則（2026-09-14 一天內兩次誤讀）：** `sizecheck.py` 先印
> `[sizecheck] <deck>: N error(s), M warning(s)`，**再**逐條印 `SIZE `／`WARN ` 明細——`tail` 只留得到尾巴。
> 主對話一度把「32 warning」誤讀成「掉到 8」；同一天 A4 的執行代理用 `tail -12` 踩了同一個坑（它自己發現並更正）。
> **一天內兩次＝該進協定的訊號。**

> **kickoff §2「現況快照」必須標量測當日的 main tip hash（2026-09-14 實測）：** 別條線的 merge 會讓整段快照作廢——
> 共用層 v1 動了字體／字級與 `sizecheck` 六條規則，2026-09-13 量的 `run_selftests` 支數（當時 42）與 sizecheck 基線
> **全部過期**。沒有 hash，讀者無從判斷快照還算不算數（§3.2 的護欄也吃過同類的虧：kickoff §5 要求
> `git log main | grep shared-layer`，但共用層 v1 的 commit subject 全是中文「共用層」⇒ 護欄回報「未 merge」，
> 實際已凍結於 `6c72163`。**護欄的判準不要綁 commit message 的英文字串**，綁 kickoff 的 checkbox 或 tag）。

### 6.5 契約進測試（G6）

任何「**本來就該成立但壞掉**」的事，修之前**一律先寫紅測試**——見根 [`../CLAUDE.md`](../CLAUDE.md) Karpathy §4
（「修 bug」→「先寫能重現的測試再讓它過」）。§3.1 後段做對了（`_selftest_figure_labels`、`focus` 的 hollow 案例先紅後綠），
前段沒有：`focus` 還原、耗時誠實、標籤相交、`DashedLine` 盲點全部是先在幀裡肉眼看到、才回頭補 selftest。

**契約類宣告（`screen_contract` 等）寫完，必須做兩件事才算「閘看得到」（2026-09-14 §3.2 親踩）：**

1. **正向**——用**閘走的同一條路**解析一次並**數條數**：`review_pack.parse_content_script(<md>)`
   ＋ `_screen_contract.required_steps()`（§3.2 收斂在契約 **11 份**、`required_steps` **36 條**）。
2. **負向對照**——故意從 storyboard 拿掉一個 `covers` id，**必須噴 `ERROR [SC1]`**。沒噴就是閘沒武裝。

**理由：`_screen_contract.parse_block()` 是 fail-closed。** 契約只要有一個 YAML 語法錯誤（§3.2 實例：`tex:` 用**雙引號**
而值裡有 `\c` 這種非法轉義）→ `yaml.safe_load` 拋錯 → `parse_block` 回 `None` → 閘看到的是「這個 unit **沒有**契約」，
在 enforce 下吐 `has no screen_contract`，訊息把人導向「**去寫一份**」而不是「**你寫的那份解不開**」。
**「我寫了契約」與「閘看得到契約」因此脫鉤。** 工具線 r2 Task I 已加分流（解析失敗回 `ParseError`，`step_coverage`
印獨立的 `[SC] <unit>: screen_contract failed to parse -- <原始例外>`，**恆 error**、不受 `enforce` 旗標影響；
紅測試 `_selftest_coverage.test_unparseable_contract`）——**但上面兩步仍是撰稿端的義務**，
不能因為工具現在會報就省掉負向對照。

**連帶的順序（§3.2 實測）：`coverage_enforce` 不是一行 meta，是「先寫完 `screen_contract` 才能開」的最後一步。**
`step_coverage.coverage_issues(..., enforce=True)` 對每個 `theorem_proof`／`derivation` 場所屬、
而內容稿沒寫 `screen_contract` 的 unit **直接吐 error**；§3.2 有 10 個這類場、契約 0 份 ⇒ 照原 kickoff
把它當「一行 meta 補齊」做會當場炸 10 個 error。**派工契約要把「寫契約 → 正向數條數 → 負向對照 → 才開 `enforce`」
的順序寫死。**

### 6.6 多 session 紀律（G7）

- **一個 session 擁有 `main` 與 render**，其他一律 **worktree 分支＋交 hash**
- worktree 開分支後**先 `git merge main`**（分支點可能落後）
- **輸出目錄各自隔離**：`rewatch_pack --out`（原並列的 `critic.py --out` 隨 Manim 封存）
- **根因調查一邊做就好**，另一邊只提供量測
- 其餘照根 [`../CLAUDE.md`](../CLAUDE.md) §任務分派的**並行紀律**（開工先 `git status`、別人 dirty 的 hunk 不碰、
  render／tts 的時間窗互相通知、子代理各自 worktree）

**§3.2 × 工具線 r1／r2 併行實測補（2026-09-14）：**

- **上游線 merge 時有義務附「影響清單」**——說明哪一類閘會被作廢：哪些只是規劃值（不必重驗）、哪些會動版面
  （`sizecheck`／`[stillness]` 要重驗）、哪些是新 warn。工具線 r1／r2 都主動列了，下游才能**只重驗會被作廢的那幾類**：
  r1 併入後下游據此判定「`[sync]` 不受影響、`sizecheck`／`[stillness]` 要重驗」，再用**三場定點 render**
  （而不是 15 分鐘整片）驗掉「`run_time` 不變」那句話；實測 §3.2 四支閘數字全部相同、兩條新規則未觸發、`[sync]` clean。
  **沒有那份清單，下游只剩「全部重跑」。**
- **`main` ≠ 最新。** 工具線 Task I 併入後 **main 紅、下游分支綠**——因為下游早在 A2 就補了 `ref:`、
  在補綠輪寫了 `screen_contract` 與 `coverage_enforce`。**上游只對 main 驗收自己的改動時，會看到下游早已解決的問題，
  也可能漏看只有下游才踩得到的問題。** ⇒ 上游驗收時要順手對**至少一個活躍下游分支**跑一次。
- **審子代理的改動用 `git show <commit>`，不要用 `git diff HEAD..<branch>`**：兩點 diff 會把「該分支單純**沒有**
  你的某個 commit」誤顯成「它**還原**了你的改動」。主對話一度據此誤判 A2b 會回退 A1 的 `source_rev` stamp。
  正解＝看該 commit 自己的 diff（`git show <sha> -- <path>`）或 merge base。並行多分支時這個陷阱會反覆出現。
- **下游先做了上游改動所需的前置工作時，要主動告知上游並承擔 merge 衝突。** 實例：main 加一行 `ref:`
  與下游同一位置的三行（`part:`／`ref:`／`covers:`）⇒ add/add 衝突，下游宣告「**取超集、衝突由我吸收**」。
  同時**明確擋掉**「把 `ref:` 加到 scene 尾端避開衝突」這種繞法——那會造成同一 scene 兩個 `ref:` 鍵，
  而 `yaml.safe_load` 對重複鍵是**後者覆蓋、不報錯**，一個看得見的衝突會變成靜默的錯值。
- **含反引號／`$` 的中文 commit body 一律 `git commit -F <檔>`**，不要用 `-m "..."`——shell 的命令替換會把整段吃掉。
  本節主對話踩過一次（merge commit 的 G0 驗證那三行被吃掉），事後 `--amend` 補回。

### 6.7 什麼**不是**浪費（避免矯枉過正）

**派工制有效**——24 件改動裡 19 件一次過，問題不在派工，在輪數。**拒絕照單全收值得**——
R2 的兩處處方被否決（會在畫面留下假等式、會破壞跨場 `carry`），這種判斷不能為了省輪次而放棄。
真正不可避免的只有**「一個缺陷遮住另一個缺陷」**（鬼影遮住 `focus` 還原、多報抵銷低報），那是狀態空間的性質，
只能一層一層來；**由排序造成的洋蔥不算在內，那是流程的錯**（kickoff §2.5／§5）。

### 6.8 派工契約紀律（2026-09-14 §3.2 首次實測；含工具線 r1／r2 教訓）

> **前提在別處：** 根 [`../CLAUDE.md`](../CLAUDE.md) §任務分派已訂「契約先於派工」「主模型只做拍板／審核／難題」
> 「有檔案改動一律 `isolation: worktree`、一個 task 一個 commit」。**本節只補 §3.2 實跑後才看得見的失效模式。**

**① 指揮者寫錯的契約會被子代理忠實放大。** §3.2 兩次實例：(a) A4 gate-2 的 prompt 把「核准源」填成**內容稿**——
**付費**閘因此拿到與 `.md` 檔頭相反的指示（R2-01，回歸輪才抓到）；(b) `screen_contract` 的 `tex:` 引號風格寫成雙引號
——會讓契約**靜默失效**（見 6.5）。**兩次都是子代理實測後停手回報才沒釀事。**
⇒ **派工契約裡要子代理「逐字照抄」的內容，指揮者必須先自己驗一次可解析**，尤其 YAML／LaTeX 混排的字串。

**② 契約裡要明確授權「與實況不符就停下來回報，不要自行改判」，並在驗收時把「停手回報」視為正確行為、不是未完成。**
§3.2 靠這一條避免做錯三次：

- `worked_example` **不遷移**——[`DESIGN.md`](../legacy/manim_video/DESIGN.md)「既有 9 個 `derivation`＋`prompt:` 例題場（§3.1 四場、
  §3.2 五場）＝不遷移」（2026-09-13 裁決：遷移要重 derive `_mimo`、reveal id 改名會讓 beat 級 TTS reuse 失配），
  而 §3.2 kickoff §4 A2 第 4 點寫的是「例題場改 `worked_example` 模板」——**兩份同日 kickoff 對同一件事給相反指示**。
  ⇒ 凍結一份共用層／模板時，**要回頭改受影響的節 kickoff**，或在 kickoff 之間寫明誰 supersede 誰。
- `meta.assumptions` 只能寫一筆——`scaffold.flag` 是**純量**，`pedagogy` 要求 flag 與 scene 1:1（`flag` 有值就必須
  對得到一筆 `meta.assumptions`，反之亦然）。
- `tex:` 的引號風格（同 ①(b)）。

**③ 擋路的交付物不要與不擋路的文件綁在同一輪。** §3.2 實例：把「NFA 版控 REPORT ＋ ledger 修正 ＋ 旁白簽核 HTML」
包成一輪，結果**唯一擋住付費 TTS 的簽核 HTML 被兩份文件拖了 3.5 小時**（子代理三件都寫完了，卻卡在重跑重閘）。
⇒ **G5 的批次化邊界要按「擋不擋路」切，不是按「是不是同一個步驟」切。**

**④ 子代理卡住時，先看它的 worktree 有沒有已完成但未 commit 的成果，能搶救就搶救，不要直接重派一輪。**
§3.2 上面那一輪的收場方式（比重派省得多）：`git -C <worktree> status` 確認三個交付物其實都已寫完（未 commit）→
`TaskStop` → 從它的 worktree `cp` 出三個新檔與一個改動檔 → 在主分支重跑 `derive_spoken.py` 重生衍生檔 →
指揮者自己複驗閘與 `scene_text_hash` → **由指揮者 commit**。**重派一輪會把已完成的工作整份重做。**

**⑤ 派工時明說「哪些閘我已經驗過、你不用跑」。** 否則子代理會出於謹慎重跑 `sizecheck`（cold TeX 約 6 分）
與 `run_selftests`（約 9 分），而且**每個子代理各付一次**。

**⑥ 子代理各自用 scratchpad 的子目錄，不要共用根目錄**（出處＝**工具線 r1**，記於
[`KICKOFF-toolline-backlog-r2.md`](../legacy/manim_video/KICKOFF-toolline-backlog-r2.md) §1；非本節量測）——r1 六個 task 共用根目錄時
**互撞過檔名**。產物一律放 `<scratchpad>/task<X>/`。

**⑦ 背景長工作寫成單一 Python 驅動器，不要 `bash "<path>.sh"` 包一層**（出處同 ⑥，工具線 r1 實測）——
那種形式**偶發會啟兩份 process tree**。

### 6.9 口徑與量測紀律（2026-09-14 §3.1／§3.2 實測）

**① TTS 報價的字數與語速必須是同一個口徑。** §3.1 實測：canonical **2,229 字**／口語版 **2,731 字**
（膨脹 **1.225×**）／實際音訊 **963.6 s** ⇒ **canonical 138.8 wpm、口語 170.1 wpm**。
**交叉使用**（拿口語版字數去配 canonical wpm）會**高估約 24%**。
⇒ **報價表必須標明用的是哪一個口徑。** §3.2 兩路交叉驗證一致：canonical 路 **722.8 s** vs 口語路 **730.9 s**。

**② mock 的 `modes` 是假象，不是對真合成的預測。** `tts.py --backend mock` 寫的是**靜音**，forced alignment
無從對齊 ⇒ manifest 會顯示 `scene_aligned: 0 / beats: N`、**全部降級**。§3.2 的 `--backend mimo --dry-run`
顯示 23 場**全走 scene-level**。**驗 manifest／時序可以用 mock，判 alignment 模式不行。**

**③ `--backend mock` 會污染真音檔目錄。** 它預設把靜音 WAV 與 mock manifest 寫進 `audio_mimo/`
（`_mimo` deck 的預設音訊子目錄）——**真合成要去的同一個目錄**。
⇒ **真合成前必須先清掉該目錄，或帶 `--force-backend-switch`**（不帶會被 backend 不符擋下）。

**④ `[still-gate]` 不在 `make.py`，在 `rewatch_pack.py`。** 6.4 把「兩道硬閘」並列，容易讓人以為 render 完
就兩道都有；實際 `make.py` 只給 `[sync]`，**`[still-gate]` 要另外跑一包 `rewatch_pack`** 才會出現。

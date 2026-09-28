# KICKOFF — §3.2 `ch03_chain_rule` Phase B（Remotion 版視覺線）

> **立檔：2026-09-28**（影片線統一走 Remotion 當日；契約＝[`KICKOFF-remotion-unification.md`](KICKOFF-remotion-unification.md) §6 第 2 條）。
> **本檔取代 [`KICKOFF-s32-chain-rule.md`](KICKOFF-s32-chain-rule.md) 的 §5 Phase B 與 §6**（Manim 共用層 v1 版，已作廢）。
> 該檔的 **§4 Phase A（A1–A5）維持有效**：內容稿 LOCKED、口語版、NFA 雙閘、旁白簽核、成本量測全部照抄沿用，本檔不重述，只寫「Phase A 的產物怎麼餵進 Remotion」與「Remotion 版的閘序、派工、停止條件、成本欄位」。
>
> **驗收定義的權威仍在 [`REVIEW_GATES.md`](REVIEW_GATES.md) §六。** 本檔是這一節視覺線的執行計畫；牴觸以 §六為準，並回頭修本檔。
> **這一輪只寫計畫**：不做片、不呼叫任何付費／外部 API。§1 的裁決表等使用者拍板後，Phase B 才開工。
>
> **路徑口徑：** 本檔依 **main 現況**（`aec2f86`）寫路徑，Remotion 製作處＝`video/experiments/remotion_styles/paper/`。同日另一條線
> （分支 `claude/charming-varahamihira-80f7df`，commit `cffc8bf`，**未併入**）已把它 `git mv` 成 `video/remotion/`、內部佈局不變；
> **併入後本檔所有 `experiments/remotion_styles/paper/` 一律讀成 `video/remotion/`**，§7 待建表的路徑同樣平移。詳 §2.5。

---

## 0. 給新 session 的啟動提示（可整段貼）

```
你負責 NTU 微積分影片產線（repo Calculus_handout，video/ 子樹）§3.2 The Chain Rule
（deck: ch03_chain_rule）的 Remotion 版視覺線（Phase B）。全程繁體中文溝通。

開工前依序讀：
  CLAUDE.md（根）                                   ← 派工分級、付費 API 先同意、Remotion 設計派 motion-designer
  video/KICKOFF-s32-remotion-phaseB.md              ← 本檔，執行計畫（§1 裁決表必須已由使用者填完）
  video/REVIEW_GATES.md §一（各層閘的沿用／封存標記）＋ §六（輪次協定 G0–G7，驗收 SSOT）
  video/KICKOFF-s32-chain-rule.md §4               ← Phase A 的產物與判準（有效，照抄）
  video/DESIGN.md                                   ← Remotion 資料流、say／{show} 契約、manifest 時序契約
  video/RUNBOOK-mimo-narration-route.md             ← tts.py 旗標紀律（--unit scene／--reuse-existing／--skip-qa／--max-billed-calls）
  video/experiments/remotion_styles/README.md       ← 現役製作處、§3.1／Q7 怎麼做的
  video/experiments/remotion_styles/paper/STYLE.md  ← 畫面契約（token、字級下限、鏡頭紀律、圖上標籤守門、公式排版）
  video/experiments/remotion_styles/paper/s31/SCRIPT.md ← 分鏡腳本的格式範本（逐場逐拍表）
  video/content_scripts/ch03_chain_rule.md          ← LOCKED 內容稿（visual_need／animation_cue／screen_contract）
  video/content_scripts/ch03_chain_rule.spoken.yml  ← 口語單一源（出片旁白的文字）
  legacy/manim_video/storyboards/ch03_chain_rule_mimo.yml ← Phase A 的 beat 切分（只讀參考）

順序不可逆（G0 內容鎖）：
  B0 派生 s32.yml（零計費）→ B1 音檔到位（§3.3：重對映或重配音，執行前徵同意）→ B2 分鏡設計＋風格幀（人閘）
  → B3 三幕實作（各自 worktree）→ B4 一次 merge、一次 render、一次審（G5）→ 里程碑六鏡 → final。

紀律四條，違反任一條就停下來問：
  1. 任何計費／外部 API（MiMo TTS、Codex、agy）呼叫前先報量徵同意（根 CLAUDE.md）。
  2. 旁白文字（say）一字不改；只准改 {show} marker 的位置與名字。要改字＝退回 Phase A（§二 第 7 條 G0）。
  3. 畫面設計與動畫製作派 motion-designer 子代理（不另傳 model）；有檔案改動一律 isolation: worktree、一 task 一 commit。
  4. 一個 session 擁有 main 與 render；render 用的 manifest 必須是這次 tts.py 寫出的那一份（不拿 mock 或舊批次出正式片）。
```

---

## 1. 裁決表（開工前等使用者拍板；每列先給本檔的預設與理由）

> 依根 `CLAUDE.md` Karpathy §1：有多種解讀時全部攤開，不默默選。下列五項**互不獨立**（D1 決定 D3 的 `meta.id`；D2 決定要不要重開 NFA），請一起看。

| # | 分歧 | 選項 | 本檔預設（理由） | 使用者裁決 |
|---|---|---|---|---|
| **D1** | **§3.2 的 MiMo 音檔怎麼來**（§2.2：本機找不到 Phase A 合成的 30 次音檔） | **R 重對映**：使用者在別台電腦／備份找得到 `output/ch03/s3.2/audio_mimo/` 整夾（`manifest.json`＋`scenes/`＋`align/`＋`beats/`）→ 搬回同一絕對路徑或依 §3.3 R 的步驟接回，`--reuse-existing` 0 次計費。**S 重配音**：找不到 → `--unit scene` 重合成 23 場，預估 23 次、核准上限 35、約 705 s 音訊（§3.3 S）。 | **先問 R、找不到就 S。** S 的代價可接受：A5-3 聽感人閘當時**尚未**由使用者完成，所以沒有任何「已認可的 take」會因重合成而作廢；MiMo 非決定性只影響 take、不影響文字忠實（NFA 不必重跑）。 | ☐ R ☐ S |
| **D2** | **旁白是否允許配合 Remotion 畫面改寫**（[`experiments/remotion_styles/README.md`](experiments/remotion_styles/README.md) 的設計前提允許「內容不變、說法可改」；§3.1 Remotion 版就是重寫的） | **鎖死**：`say` 逐字＝Phase A 的口語版，只動 `{show}`。**開放**：允許改寫 → 視為重開 Phase A（copyedit → 簽核 → NFA gate-1＋gate-2 → 重配音），§3.3 R 分支作廢、S 分支的 23 次照付。 | **鎖死。** 理由：§六 6.1「人閘要簽在對的那一份」——使用者已在 [`REVIEW-ch03_chain_rule-s32-narration-signoff.html`](content_scripts/_audit/REVIEW-ch03_chain_rule-s32-narration-signoff.html) 簽過這 23 場的 `say`；改字就把 Phase A 的 7 輪稽核與 167.5k 外部 token 作廢。畫面要「配合旁白」而不是反過來。 | ☐ 鎖死 ☐ 開放 |
| **D3** | **分鏡放哪、deck id 叫什麼** | (a) 製作處下的 `s32/s32.yml`（main 現況＝`experiments/remotion_styles/paper/s32/`，升格併入後＝`video/remotion/s32/`）、`meta.id: ch03_chain_rule_mimo`（沿 Phase A 的 deck 身分，R 分支才能 reuse；`provenance.content_script_for` 會剝 `_mimo` 找到 `ch03_chain_rule.md`）；(b) 同路徑、`meta.id: s32`（乾淨，但 R 分支的 reuse 因 `deck_id` 不同一定失效，內容稿也對不上）；(c) 等升格線（§2.5）併入再開工 | **(a)，且不必等 (c)**——升格是純 `git mv`、佈局不變，本節開工時它在哪就寫哪。`tts.py` 的 reuse 身分含 `deck_id`（§2.3），改 id 就等於放棄 R 分支。 | ☐ a ☐ b ☐ c |
| **D4** | **派工批次形狀**（§5） | (i) 先一個 motion-designer 做「分鏡腳本＋7 張風格幀」給使用者看過（人閘），再三幕並行實作；(ii) 跳過風格幀人閘，直接三幕並行 | **(i)。** §3.1 的教訓＝鏡頭紀律與圖上標籤兩條模板規則都是使用者**看片後**才裁決的；§3.2 是 full ε-δ、23 場、比 §3.1 多一幕證明，先用 7 張靜幀把版型定下來，比做完 8 分鐘片再改便宜一個量級。 | ☐ i ☐ ii |
| **D5** | **里程碑六鏡的外部鏡**（agy ×3，逐次徵同意） | 照 §六 6.2 跑（agy R1a／R3／R5 ＋ subagent ×3）；或本節只跑 subagent ×6（零外部） | **照 §六。** 異家族第二讀者的價值在 §3.2 Phase A 已實證（gate-2 抓到 gate-1 與主對話共同放過的 D2 blocking）。呼叫時另行報量徵同意，本檔不預先取得。 | ☐ 照 §六 ☐ 只 subagent |

---

## 2. 現況與已驗證事實（2026-09-28 快照；**main tip `aec2f86`**，本 worktree 已 merge）

> 每一條都是立檔當日在本機親自跑過／打開過的，不是轉述（§六 6.4：快照要標 main tip hash）。

### 2.1 Phase A 產物（有效，Remotion 版直接吃）

| 產物 | 路徑 | 實測 |
|---|---|---|
| 內容稿（source of truth，LOCKED） | [`content_scripts/ch03_chain_rule.md`](content_scripts/ch03_chain_rule.md) | 24 單元（intro／outro 無旁白）；`source_rev` 已換 `chapter3.tex`；**11 份 `screen_contract`／36 條 `required_steps`**；`examples:` 5 筆＝`ex:3.4`–`3.8`（`example_coverage` 0 finding） |
| 口語單一源（出片旁白的文字） | [`content_scripts/ch03_chain_rule.spoken.yml`](content_scripts/ch03_chain_rule.spoken.yml) | **23 個 content 場、2,070 字**（剝 marker 後）；檔頭有整節的「唸法帳本」（LaTeX → 唯一口語形） |
| 口語版人讀投影（生成檔） | [`content_scripts/ch03_chain_rule_narration_spoken.md`](content_scripts/ch03_chain_rule_narration_spoken.md) | `derive_spoken.py` 生成；DO NOT EDIT |
| **beat 切分**（Manim 時代的 `_mimo` deck；`say` 就是口語版） | [`legacy/manim_video/storyboards/ch03_chain_rule_mimo.yml`](../legacy/manim_video/storyboards/ch03_chain_rule_mimo.yml) | **28 場＝intro 1／divider 3／content 23／outro 1**；`{show}` marker **76 個**、content 首拍＋marker 拍合計 **99 拍**；`meta.derived_from` 蓋了正典 `ch03_chain_rule.yml`＋`.spoken.yml` 的 sha256 |
| NFA 版控結案 | [`content_scripts/_audit/REPORT-ch03_chain_rule-narration-faithfulness.md`](content_scripts/_audit/REPORT-ch03_chain_rule-narration-faithfulness.md) | gate-1 0 blocking、gate-2（agy Gemini 3.1 Pro）1 blocking → 修根因 → 0；**判準對 `say:`**（不對 `.md` 的 `narration:`） |
| 旁白簽核稿（合成前人閘，使用者已簽） | [`content_scripts/_audit/REVIEW-ch03_chain_rule-s32-narration-signoff.html`](content_scripts/_audit/REVIEW-ch03_chain_rule-s32-narration-signoff.html) | 23 場 `say` 逐場 |
| Phase A applied 總帳 | [`content_scripts/_audit/REVIEW-ch03_chain_rule-s32-phaseA-applied.html`](content_scripts/_audit/REVIEW-ch03_chain_rule-s32-phaseA-applied.html) | A1–A5 全部收案；A5 真 TTS 數字見下 |
| 對齊報告（A1） | [`content_scripts/_audit/REVIEW-ch03_chain_rule-s32-a1-alignment.html`](content_scripts/_audit/REVIEW-ch03_chain_rule-s32-a1-alignment.html) | 24 單元零跟改 |
| 成本量測（Phase A 那一列） | [`REBUILD_STATUS.md`](REBUILD_STATUS.md)「每節成本量測」 | 真 TTS **30 次／核准 35／0 retry**；23 場中 **22 場 `scene_aligned`、1 場降級 beats**（`composed_mapping_figure`：arbiter fail → resynth fail → chunk 因 `--fallback-budget 2` 被拒 → beats 終端）；**音訊 704.5 s**（mock 估 828 s，高估 15%）；Manim 成片 786.5 s |

### 2.2 ⚠️ 音檔實況：Phase A 的 30 次 MiMo 音檔**本機找不到**

- 2026-09-28 在使用者家目錄下的 Downloads、Desktop、.claude、.codex、Temp/claude 五處全樹搜尋名為 audio_mimo 的目錄與 deck 含 chain_rule 的 manifest：**只有 §3.1 的 `video/output/ch03/s3.1/audio_mimo/`**（主 checkout）；主 checkout 的 `video/output/ch03/s3.2/` 只剩 2026-07-01 的 mock manifest（backend mock、27 場、669 s 靜音）、critic 抽幀夾與 mock 成片。
- 推定原因：§3.2 Phase A 的 session 在自己的 worktree 跑 A5（[`KICKOFF-s32-chain-rule.md`](KICKOFF-s32-chain-rule.md) §3.6「每節一個 session＋自己的 worktree＋自己的 output 目錄」），`video/output/` 是 gitignored（`.gitignore:45`），2026-09-28 清掉「兩個已併入 main 的 locked 舊 worktree」（[`KICKOFF-remotion-unification.md`](KICKOFF-remotion-unification.md) §5 本機清理）時音檔一併消失。unification 收案寫的「`video/output/`（含付費 TTS 原音）未動」指的是主 checkout，主 checkout 從來沒有 §3.2 的真音檔。
- **沒有任何已認可的 take 因此作廢**：REBUILD_STATUS 記「A5-3 聽感人閘收工時仍待使用者」，聽感人閘從未完成。
- ⇒ **D1 的答案取決於使用者在別台電腦有沒有那個資料夾。** 沒有就走 S（重配音）；§3.3 兩個分支都寫好了。
- **教訓（回寫 §六 6.6 候選）：** 付費音檔不能只活在 worktree 的 gitignored 目錄；合成完成後要立刻複製到主 checkout 的 `video/output/`（或 `paper/public/audio/`）並記路徑進 REBUILD_STATUS。本檔 §7 把這條寫進 Task 0 的驗收。

### 2.3 Remotion 現役工具的已驗證事實（本節會用到的、不重新發明）

1. **`tts.py` 對 Remotion 分鏡的三條規則**（[`RUNBOOK-mimo-narration-route.md`](RUNBOOK-mimo-narration-route.md)、[`DESIGN.md`](DESIGN.md)「Manifest schema 2」）：
   - Remotion 分鏡沒有 `template` 欄位，`--unit auto` 一律退回逐 beat ⇒ **整場合成必須明寫 `--unit scene`**；mock 一律 `--backend mock --unit beat`。
   - **reuse 身分＝`_IDENTITY_KEYS`＝`deck_id`／`backend`／`model`／`voice`／`style`／`sample_rate`／`channels`／`sample_width`／`output_dir`**（`pipeline/tts.py` 第 400 行附近）。任一不同 ⇒ `identity_diff` ⇒ reuse index 不建、整批重合成；`--scene` 子集還會被 `overwrite_guard` 直接擋。**`output_dir` 是絕對路徑字串**——搬過機器就不同。
   - scene 級 reuse 的判準＝`scene_reuse_ok`：backend／model／voice／style 同＋**`scene_text_hash` 同**（＝各拍文字以空白串接的 transcript 的 hash，**與 `{show}` 的名字、位置無關**）＋WAV 在、時長對。所以**只改 marker 名字或位置，不花錢**；改一個字，整場重合成。
2. **Remotion 時序全由 manifest 決定**（`paper/src/s31/timing.ts`）：30 fps、`LEAD 15`／`TAIL 27`／`OVER 22` 幀；場長＝LEAD＋⌈旁白秒×fps⌉＋TAIL；拍起點＝LEAD＋round(start_seconds×fps)；首拍 id＝`"start"`；`scenes[].alignment.words_file` 有值時 `atWord()` 可用（mock 沒有，`atWord(...) ?? at(...)` 是唯一允許的 fallback）。**composition 的 `durationInFrames` 由 `calculateMetadata` 從 manifest 算出**，所以「影片短於旁白」這一類 `[sync]` 錯誤在 Remotion 結構上不會發生；會發生的是「render 指到錯的 manifest」（RUNBOOK 2026-09-28 註）。
3. **場序守門的先例**：`paper/src/Root.tsx` 的 `q7Meta` 把 manifest 的場 id 序列與 `Q7_ORDER` 逐字比對、不符即 throw。§3.2 的 composition 照做（§4.3）。
4. **圖上標籤守門已是 render 期硬閘**：`paper/src/s31/kit.tsx` 的 `checkLabels`／`useS().guard()`，間距 < 10 px 即 throw、不出片（[`paper/STYLE.md`](experiments/remotion_styles/paper/STYLE.md)「圖上標籤」）。
5. **抽幀工具**：`node scripts/frames.mjs <outDir> <compId>:<幀或秒s>,…`（先 `npx remotion bundle`；`PROPS='{"manifest":…}'` 可換 manifest）。**每一場都有自己的 composition**（`S31-<id>` 形式），可單場 render、單場抽幀。
6. **後製兩步**：`python scripts/loudnorm.py <raw> <final>`（house −19 LUFS，實作＝[`pipeline/loudnorm.py`](pipeline/loudnorm.py)）；`python scripts/chapters.py <manifest> <txt> --embed <mp4>`（章節點，常數從 `timing.ts` 讀）。
7. **本機狀態（會被別的 session 動，開工前自己再量）**：立檔當日 08:5x 量到主 checkout 的 `paper/` 下有 `node_modules/`、`out/`（§3.1／Q7 成片）、`public/audio/`（`s31_scene`／`q7_scene` 等 7 個批次）、`build/`；09:15 再量，四夾已被升格線（§2.5）搬到主 checkout的 `video/remotion/`（untracked、ignored），`paper/` 下只剩 tracked 檔。**任何 worktree 都沒有這四夾**（gitignored；子代理 worktree 要先 `npm ci`，音檔要從主 checkout 複製或重跑 TTS）。

### 2.4 沿用工具的現況（哪裡還綁著 Manim）

| 工具 | 現況（2026-09-28 讀碼） | 對本節的意思 |
|---|---|---|
| [`pipeline/rewatch_pack.py`](pipeline/rewatch_pack.py)（12 s 硬閘＋REWATCH pack） | 讀死 `video/storyboards/<deck>.yml`、`output/_av/<deck>/<scene>.mp4`、`section_output_dir(meta)/audio_mimo/manifest.json`；reveal 時間用 `pipeline/timing.py` 的 `SCENE_LEAD_SECONDS`＝1.0（Remotion 是 15 幀＝0.5 s）；折 `pauses:`（Remotion 不讀） | **不改就跑不起來**——§5 Task 0 給它三個輸入旗標＋時序常數注入，紅測試先行 |
| [`pipeline/provenance.py`](pipeline/provenance.py)／[`pedagogy.py`](pipeline/pedagogy.py)／[`step_coverage.py`](pipeline/step_coverage.py)／[`example_coverage.py`](pipeline/example_coverage.py) | **main 上都沒有 CLI**（沒有 `argparse`／`__main__`），只被已封存的 `schema.py` 呼叫；它們讀 storyboard 的 `ref:`／`covers:`／`scaffold`／`template`。**schema 線（§2.5，未併入）的 `check_storyboard.py` 正是給它們的新入口** | 本節**不自建**入口：schema 線併入前，由 gate-1 agent 讀分鏡腳本人工覆蓋（§4.1 寫明武裝前提）；併入後 `s32.yml` 必須過 `check_storyboard.py` 0 error（§5 Task 0、§5.4）。`example_coverage` 不讀 storyboard，`.md` 未動 ⇒ Phase A 的 0 finding 沿用 |
| [`pipeline/run_selftests.py`](pipeline/run_selftests.py) | **24 支全綠**（本 worktree、主 checkout 的 `.venv`；約 10 s） | 開工基線＝24 |
| [`tools/doc_lint.py`](../tools/doc_lint.py) | 主 checkout clean；本 worktree 報 2 條既有斷鏈（`paper/out/q7zh_gemini_iapetus_scene_trial_20260926.mp4`，gitignored 成片、只在主 checkout 存在） | 非本輪造成；本檔不碰 |
| `.claude/launch.json` 的 `remotion-review` | 指向舊 session 的 scratchpad 路徑（unification §6 第 4 條） | 本節 render 驗收不靠它；修它是另案 |

### 2.5 同日並行、**尚未併入 main** 的兩條姊妹線（本檔立檔時 `git log --all` 看到；影響清單依 §六 6.6 附上）

| 線 | 分支／commit（09:09–09:17） | 做什麼 | 併入後對本檔的影響 |
|---|---|---|---|
| **升格線**（unification §6 第 1 條） | `claude/charming-varahamihira-80f7df` `cffc8bf` | 純 `git mv video/experiments/remotion_styles/paper → video/remotion`（102 檔、佈局不變）；路徑引用修正在下一個 commit | 本檔所有 `experiments/remotion_styles/paper/…` 讀成 `video/remotion/…`；`tools/doctor.py --smoke`、RUNBOOK 的 `--output-dir` 例同樣平移。**沒有閘被作廢**（純搬移） |
| **schema 線**（unification §6 第 3 條） | `claude/youthful-tu-32346e` `6c866b8`＋`d7dd64f` | 立 `SPEC-remotion-storyboard-schema.md`（Remotion 分鏡欄位 SSOT：`ref:`／`refs:`／`covers:`／`scaffold:`／`pauses:` 是 **Remotion 欄位**；`template`／`accent`／`scene_role`／`hook`／`part`／`focus`／`paced`／`carry`／`exit`／`layout`／`aside`／`anim` 與 `meta.video`／`color_map*`／`fontfloor_enforce`／`layout_enforce`／`mathtype_enforce` 是 Manim 遺留、出現即 WARN）＋新入口 `pipeline/check_storyboard.py`（結構驗證＋串 provenance／source_rev／pedagogy／step_coverage／example_coverage，每閘印武裝狀態；selftest 24→25）；另在 `KICKOFF-s32-chain-rule.md` 加頂註 | ① §3.1 的派生規則已改成**與 SPEC 一致**（保留 `ref:`／`covers:`／`scaffold:`，只拿掉 Manim 遺留欄位）；② §4.2「schema 退役」的替代物＝`check_storyboard.py [structure]`，`s32_derive.py --check` 只留它不做的 say 逐字 parity；③ pedagogy 閘的確定性底材＝它（PD2／SC「必須有契約」因無 `template` 在 Remotion 上**不武裝**，agent 要自己看——SPEC §6 待裁決 2）；④ §5.4 停止條件 4 加「`check_storyboard` 0 error」；⑤ 兩線都動 `KICKOFF-s32-chain-rule.md` 頂註，merge 時會有一次 add/add 衝突，取超集 |

> 依審查紀律，本檔**不把未併入的分支當既成事實**：正文以 main 現況寫，凡依賴這兩線的地方都標「併入後」。

---

## 3. Phase A 產物怎麼餵進 Remotion（問題 1）

### 3.1 `s32.yml` 的派生規則（從 `ch03_chain_rule_mimo.yml`；零計費、確定性）

**目標檔：** `video/experiments/remotion_styles/paper/s32/s32.yml`（待建；tts.py 格式，比照 [`paper/s31/s31.yml`](experiments/remotion_styles/paper/s31/s31.yml)）。

| 來源欄位（`_mimo.yml`） | 處置 | 理由 |
|---|---|---|
| `scenes[].id`、場序、`kind` | **原樣保留**（28 場、同序、同 id） | `rewatch_pack`／manifest／R 分支的 reuse 全以 `scene_id` 定址；`decomposition_strategy`＋`_repeat` 的 `part:` 分頁保留為兩場 |
| content 場的 `say` | **逐字保留**（D2 鎖死），只把 `{show <id>}` 的 **id 改名**（下一列） | `scene_text_hash` 與 marker 無關 ⇒ 0 計費；NFA 判準不變 |
| `{show}` marker id（`math.0`／`statement`／`proof.1`／`step.2`／`point.3`／`scaffold.flag.borrowed_ch2`／`qed`…＝Manim payload 的 dotted 文法） | **改為場內語意名**（`s31.yml` 慣例：`identity`／`substitute`／`ledger`…），**位置先不動**；同場唯一、無 `.`。改名表寫進 `paper/s32/SCRIPT.md` 每場的拍表（舊 id → 新 id） | Remotion 的 id 是場景元件自訂的查表鍵（[`DESIGN.md`](DESIGN.md)「旁白 `say` 文法」）；dotted 名在 TSX 裡沒有意義 |
| marker **位置**（拍的切點） | B2 分鏡設計時**可以移動、增刪**（設計上需要更細的 reveal 就多切一拍），但**不改任何字** | scene 級：免費（只重對映）；**唯一的 beats 場 `composed_mapping_figure` 例外**——beat 級 reuse 以 `(scene_id, 拍文字 hash, 第幾個)` 定址，移切點＝拍文字變＝該拍重合成（R 分支才有這個成本；S 分支本來就要合成） |
| `kind: intro` 的 `tagline`、`duration: 6.0`；`kind: divider` 的 `eyebrow`／`title`／`subtitle`／`scaffold.problem`／`progress`／`duration: 4.0`；`kind: outro` 的 `next_section`／`next_title`／`duration: 8.0` | **保留為家具文字**（Remotion 的 intro／divider／outro 元件讀它們；`duration` 給 manifest 的 silent 場） | 這些是 Phase A 已簽核的上畫面文字；三個 divider 的 `scaffold.problem` 是 PD3「分段問題」的契約 |
| `ref:`／`refs:`／`covers:`／`scaffold.{motive,problem,flag}`／`source`（人話標籤） | **保留**（Phase A 的 A2／A2b 已把 11 份契約對到 `covers:`、`scaffold.flag.borrowed_ch2` 對到 `meta.assumptions`） | 這些是 Remotion 分鏡的內容層欄位（schema 線 SPEC §2；§2.5）：Remotion 場的上畫面文字寫在 composition、不在 yml，場級 `ref:` 是這一場唯一的 provenance 把手，`covers:` 是 SC 覆蓋宣告。拍表（`SCRIPT.md`）另外逐拍列上畫面 TeX 當 OF1 對照源（§4.1） |
| `template`／`scene_role`／`accent`／`part`／`hook`／模板 payload（`statement`／`math`／`proof`／`steps`／`points`／`prompt`／`body`／`plot`…） | **全部拿掉**，不進 `s32.yml` | Manim 引擎欄位（SPEC 的遺留清單，出現即 WARN）；但**上畫面文字的內容**（定理陳述、證明列、例題步驟）要搬進 `SCRIPT.md` 的拍表 |
| `meta` | 留 `id`／`section: "3.2"`／`chapter`／`chapter_title`／`title`／`language: en`／`voice: Dean`／`assumptions`（PD4 registry，1 筆 `borrowed_ch2`）／`otf_enforce`／`pedagogy_enforce`／`coverage_enforce`（Phase A 已開的三個 opt-in，Remotion 上沿用）；拿掉 `theme`／`video`／`fontfloor_enforce`／`sections`。**`id` 依 D3**（預設 `ch03_chain_rule_mimo`）。**`derived_from` 重新蓋**：inputs＝legacy 的 `ch03_chain_rule_mimo.yml` 與 `ch03_chain_rule.spoken.yml`（以 `s32.yml` 所在目錄為基準的相對路徑＋LF 正規化 sha256，由 [`pipeline/derived_check.py`](pipeline/derived_check.py) 的 `stamp_for` 產生，不手寫） | `tts.py` 開跑前驗 `derived_from`：口語版或 legacy 切分一動、`s32.yml` 沒重生就 `[freshness]` abort——治「改了源、沒重派生就合成」 |

**檔頭註解**照 `q7.yml`／`s31.yml`：「Spoken English only (no LaTeX: MiMo reads the text literally). Each `{show <id>}` starts a beat; Remotion scenes look beats up by these ids (src/s32/). Timing comes from tts.py's manifest.」＋mock 指令一行。

### 3.2 派生腳本＋parity 檢查（Task 0 交付；零計費）

`video/pipeline/s32_derive.py`（待建；**不是**通用工具，就做這一節；通用化等第二節再說——Karpathy §2）：

1. 讀 legacy `_mimo.yml`＋一張 **marker 改名表**（YAML：`scene_id: {舊 id: 新 id}`，由 B2 分鏡設計產出、B0 先用「舊 id 原樣」跑一遍）→ 寫 `s32.yml`。
2. **`--check`（parity，擋 exit 1）**：對每個 content 場，`s32.yml` 的 `say` 剝掉 marker 後**逐字等於** `.spoken.yml` 該場文字剝掉 marker；28 場 id 與序與 legacy 一致；intro／divider／outro 的 `duration` 一致；`ref:`／`covers:`／`scaffold` 與 legacy 逐場相同。**這一支就是 Remotion 版的 `derive_spoken.py --check`**，也是「NFA 沿用」的前提（§4.1）。結構規則（`say` 無 `$`、marker 文法、同場 id 唯一、Manim 遺留欄位）**不在這裡重寫**：schema 線的 `check_storyboard.py` 併入後由它管，併入前暫由本支代管、併入當日移除重複的那幾條。
3. 紅測試先行（G6）：`pipeline/_selftest_s32_derive.py`——改一個字必紅、改 marker 名必綠、marker 帶 `.` 必紅。

### 3.3 音檔：兩個分支（D1；**兩個都在執行前徵同意**——R 分支雖然預期 0 次，`--dry-run` 才能證明）

**共同前置：** `.env` 有 `MIMO_API_KEY`；`stable-ts` 在（`--unit scene` 開跑前 `tts.py` 會自檢，缺即中止，不會先花錢）；`s32_derive.py --check` 綠；目標音訊目錄＝`video/experiments/remotion_styles/paper/public/audio/s32_scene/`（gitignored，與 §3.1 的 `s31_scene` 並列）。

**分支 R（重對映；前提＝找回 `output/ch03/s3.2/audio_mimo/` 整夾）：**

1. 把整夾（`manifest.json`、`scenes/`、`align/`、`beats/`）複製到 `paper/public/audio/s32_scene/`。
2. **身分對齊**：manifest 記錄的 `output_dir` 是舊 worktree 的絕對路徑，與新目錄不同 ⇒ `identity_diff` ⇒ reuse 失效。兩種解法，**擇一、先講清楚再做**：(a) 用一支一次性腳本把 manifest 頂層 `output_dir` 與每場 `audio_file`／`words_file`／`aligned_file`／beat `audio_file` 的目錄前綴改寫成新目錄（只改字串，不動 WAV；比照 `tts.py` 的 `_renumber_path` 只改路徑前綴），(b) 工具線把 `output_dir` 從 `_IDENTITY_KEYS` 拿掉（改 `tts.py` 契約＋紅測試，屬另案）。**本檔預設 (a)**：一次性、不改共用層。
3. 報價：`tts.py --storyboard …/s32/s32.yml --scene all --backend mimo --unit scene --output-dir …/s32_scene --reuse-existing --dry-run` ⇒ `plan` 欄應為 **0**（`(no-reuse: 23)`），`prior manifest: reusable`。**不是 0 就停下來報**，不要硬跑。
4. 同意後：同一指令去掉 `--dry-run`、加 `--skip-qa --no-billing`（把 0 次變成保證）。scene 級命中會印 `reused … (moved from …)` 並重對位（免費）；`composed_mapping_figure`（beats 場）加 `--unit beat` 另跑一次子集（`--scene composed_mapping_figure --unit beat --reuse-existing --no-billing`）。
5. 之後每次移 marker 都照 3→4 重跑；`plan` 0 就是免費的證明。

**分支 S（重配音；找不到音檔時）：**

| 欄 | 數字（依 Phase A 實測推算；**執行前以 `--dry-run` 實跑覆蓋**） |
|---|---|
| 合成單位 | `--unit scene`（Remotion 分鏡沒有 template，auto 會退回 beat） |
| 場數 | **23 個 content 場** |
| 音訊秒數 | **≈ 705 s**（Phase A 實測 704.5 s；同文字、同 voice，MiMo 非決定性 ±10%） |
| 預期 billed call | **23**（一場一次；Phase A 實跑 23 場用了 30 次＝3 場走 fallback ladder） |
| fallback 預算 | `--fallback-budget 2`（只夠 resynth；`composed_mapping_figure` 上次就是在這裡掉到 beats 終端＝該場 5 拍各一次） |
| worst case | `--dry-run` 的 `worst` 欄（1＋budget＋非空拍數，逐場加總）——報價時 planned／worst 兩個數字都給 |
| 上限 | **`--max-billed-calls 35`**（與 Phase A 核准上限相同；0 次重做的先例） |
| 指令 | `python video/pipeline/tts.py --storyboard video/experiments/remotion_styles/paper/s32/s32.yml --scene all --backend mimo --unit scene --skip-qa --reuse-existing --max-billed-calls 35 --output-dir video/experiments/remotion_styles/paper/public/audio/s32_scene` |
| 合成後 | `listening_pack.py --manifest …/s32_scene/manifest.json` 產 HTML → **使用者聽一遍**（Phase A 沒完成的 A5-3 人閘在這裡補）；同時把整夾複製一份到主 checkout 的 `video/output/ch03/s3.2/audio_mimo/`（§2.2 教訓） |

**兩分支共同的紀律**（RUNBOOK 四條，每條都是真金白銀）：`--reuse-existing` 永遠帶；`--skip-qa` 永遠帶（QA 事後離線看 manifest 的 `gates.qa`）；beats 場一律 `--unit beat`；`--max-billed-calls` 一律帶、N＝核准數。**mock 與真音檔不共用目錄**（mock 寫 `s32_mock/`）。

### 3.4 mock 路徑（零計費、可逕行；B2／B3 全程用它）

```
python video/pipeline/tts.py --storyboard video/experiments/remotion_styles/paper/s32/s32.yml \
    --scene all --backend mock --unit beat \
    --output-dir video/experiments/remotion_styles/paper/public/audio/s32_mock
```

mock 估時比真音檔**高 15%**（§2.1）——用 mock 量的最長靜止只能當上界，12 s 硬閘的正式判定一律對真音檔的 render 做。

---

## 4. 閘序：哪些沿用、哪些退役、由什麼取代（問題 2）

> [`REVIEW_GATES.md`](REVIEW_GATES.md) §一 已把各閘標成「沿用，待接 Remotion」或「已封存」；本節寫的是**在 §3.2 具體接成什麼**。判準（blocking==0 等）不在此重述。

### 4.1 直接沿用的閘（含 Remotion 版的輸入與**武裝前提**——§六 6.2：「某閘 blocking＝0」必須同時寫明前提，否則是 vacuous pass）

| 閘 | Remotion 版的輸入 | 武裝前提（沒滿足＝綠燈不算數） | 何時跑 |
|---|---|---|---|
| **NFA**（層 4；已收斂） | **不重跑**。前提＝`s32_derive.py --check` 綠（`say` 逐字＝Phase A 口語版） | `--check` 在 B0 與每次 merge 後都跑；一旦 D2 改為開放或任何 `say` 字變，對動到的場跑 scoped NFA gate-1，並依 §二 第 8 條每節一次 gate-2（外部、徵同意） | B0、每輪 |
| **copyedit**（層 3；lock 前閘） | 不跑（旁白已 lock） | 同上；D2 開放才重開 | — |
| **旁白簽核人閘** | 已簽（§2.1）；marker 改名／移位不需重簽 | `say` 一字不改 | — |
| **pedagogy-firstlearner（PD／OF／SC）**（層 6，PRE-render，gate-1 subagent） | `s32.yml`（場級 `ref:`／`covers:`／`scaffold`＝與 Phase A A2b 相同的宣告）＋ **`paper/s32/SCRIPT.md`**（待建）的逐場逐拍表：每拍寫「畫面上出現的文字／TeX（逐字）＋回溯到哪個 `.md` 單元或講義 label＋覆蓋哪些 `screen_contract.required_steps` id」；cited `.md`＋`chapter3.tex:208–416` 照舊 | **SCRIPT.md 的拍表必須逐拍列上畫面 TeX 與 `covers` id**——Remotion 場的上畫面文字在 composition 裡，yml 沒有文字欄，OF1 只能對拍表判；確定性底材＝`check_storyboard.py`（schema 線併入後；PD3／PD4／SC1／SC2／場級 `ref:` 解析由它算，**PD2 與「單元必須有契約」因無 `template` 不武裝**，agent 對 36 條 `required_steps` 人工核對）；agent 另抽 3 場對照 `src/s32/scenes/*.tsx` 的字串，確認 SCRIPT.md 沒有與實作脫鉤 | B2 結束（設計稿）跑一次；B3 merge 後對實作抽查一次 |
| **provenance（OF2 可回溯）** | `s32.yml` 場級 `ref:`（`md:`／`doc:`；Phase A 已對齊）＋SCRIPT.md 的 `source` 欄 | 併入前人工；併入後 `check_storyboard.py [provenance]` 的場級檢查（`scene_ref_issues`）＋`meta.otf_enforce: true`（Phase A 已開）⇒ 缺 `ref:` 即 error | B0、每輪 |
| **example coverage（EX）** | 不讀分鏡；`.md` 未動 ⇒ Phase A 的 0 EX1／0 EX2 沿用 | `.md` 的 `examples:` 五筆未動（`git diff` 為空） | B0 確認一次 |
| **REWATCH 多鏡**（里程碑審） | Task 0 改好的 `rewatch_pack.py` 對真音檔 render 產的 pack（contact sheet＋逐場 md＋INDEX） | pack 的旁白字來自 `s32_scene` manifest 的逐字對時（scene_aligned 場）；`composed_mapping_figure` 若仍是 beats 模式，該場字級標籤是拍內線性內插（rubric 的 `~`） | 收斂時一次；agy ×3 逐次徵同意（D5） |
| **12 s 最長靜止硬閘**（層 7，`rewatch_pack --gate-still`） | 同上，`[still-gate] PASS` 才算該輪完成 | Task 0 的紅測試證明 FAIL／PASS 兩向；LEAD／TAIL 用 Remotion 常數 | 每次 1080p render 後 |
| **視覺 gate-1（visual-frame-audit）** | `rewatch_pack` 的逐場 contact sheet＋取樣幀，或 `scripts/frames.mjs` 抽的 PNG（每場至少：首拍後、每個 reveal 後、最滿幀） | 幀是**這次 render** 的（rubric 要新鮮幀）；抽幀清單寫進輪次紀錄 | 每次 render 後 |
| **人工 frame-grab 驗收** | 同上，在 reveal 時間點抽幀確認 reveal 準時、MathJax 無亂碼 | — | final 前 |
| **amplification**（每章一次） | 不在本節 | — | — |

### 4.2 退役的閘與它們的替代物

| 退役（Manim gen-2） | 它原本擋什麼 | Remotion 版由什麼取代 |
|---|---|---|
| `schema.py` 結構驗證＋它掛的內容層檢查器 | meta 必填、kind 合法、id 唯一、`{show}` 不閉合；provenance／pedagogy／coverage／source_rev／example_coverage | **schema 線的 `check_storyboard.py`**（§2.5；併入後）＝同一組檢查器的 Remotion 入口，Manim 遺留欄位出現即 WARN；併入前由 `s32_derive.py --check` 代管結構規則；composition 另有場序守門（§4.3 ②） |
| `lint.py`（純文字欄含 `$`） | LaTeX 漏進旁白 | 口語版本來就無 LaTeX；`s32_derive.py --check` 併入前代管「`say` 無 `$`」，併入後歸 `check_storyboard.py` |
| `sizecheck.py`／fontfloor／LayoutRules L1–L3／MathRules M1–M3 | 字級、出框、字級下限、版面規則 | **沒有確定性替代**。畫面契約在 [`paper/STYLE.md`](experiments/remotion_styles/paper/STYLE.md)（字級下限 28 px、鏡頭紀律、公式排版），由 motion-designer 自審迴圈＋visual-frame-audit V4／A6 在幀上判；render 期唯一的硬守門是圖上標籤 `checkLabels`。**確定性字級／出框閘記進 §8 backlog**，不在本節做 |
| `critic.py --dry-run` 抽最滿幀 | 視覺 gate-1 的幀來源 | `rewatch_pack` contact sheet／`frames.mjs` |
| `critic.py --confirm`（MiMo VLM gate-2） | 外部視覺複核 | 退役；里程碑審的 agy 鏡（多模態，讀 contact sheet）是最接近的替代，仍屬 advisory |
| `make.py --reuse-audio` manifest freshness | 過期音檔配新分鏡 | ① `meta.derived_from`（`tts.py` 開跑前驗）；② **render 前的凍結證明**：`tts.py … --backend mimo --reuse-existing --dry-run` 的 `plan` 為 0 ＝ 分鏡文字與 manifest 一致（不需 API key，dry-run 只讀）；③ render 時把 `--props` 的 manifest 路徑與該 manifest 的 sha256 記進 `paper/s32/RENDER.md`（待建；比照 Q7 的 `*.props.json`） |
| `[sync]` 硬閘（render 後影片長 vs 旁白長） | 影片短於旁白、偏差 > 2 幀 | 結構上由 `calculateMetadata` 保證；**殘餘風險**（錯 manifest、`<Audio>` 被 Sequence 截斷）由 §4.3 ① 的 `remotion_sync_check.py` 對成品 ffprobe 實測 |
| `[stillness]` 6 s authoring advisory | 未宣告的長靜止 | 無對應（Remotion 沒有 `paced:`／`pauses:` 宣告層）；12 s 硬閘＋REWATCH R4 兩層仍在。設計上以 STYLE.md「禁止長靜止：每拍都有東西在動」為規則 |
| hook-engineering-audit（層 5） | Manim hook code 數學保真 | 退役；Remotion 場景 code 的稽核＝pedagogy gate 對 SCRIPT.md↔TSX 的抽查（§4.1）＋visual-frame-audit V1–V3 在幀上看數學對錯 |

### 4.3 本節新增的三個確定性檢查（Task 0；全部離線、零計費；紅測試先行）

1. **`video/pipeline/remotion_sync_check.py`（待建）**：讀 manifest＋Remotion 常數（`FPS`／`LEAD`／`TAIL`／`OVER` 從 `src/s32/timing.ts` 讀，比照 `scripts/chapters.py` 的做法）算出 composition 總幀數，與成品 mp4 的 ffprobe 幀數比對，|Δ| ≤ 2 幀才 PASS；另對每個 content 場檢查 `audio_seconds×fps ≤ 場長−LEAD−TAIL`（音軌不被截）。exit 1＝FAIL。**這是 `[sync]` 硬閘的 Remotion 對等物。**
2. **composition 場序守門**（在 `src/s32/S32.tsx`／`Root.tsx` 的 `calculateMetadata`，待建）：manifest 的場 id 序列 ≠ `S32_ORDER` 即 throw（先例＝`q7Meta`）。這是「錯 manifest」的第一道擋。
3. **`rewatch_pack.py` 接 Remotion**：新增 `--storyboard <yml>`／`--manifest <json>`／`--av-dir <dir>`／`--lead-seconds`／`--tail-seconds`（預設值＝現行 Manim 行為，零行為改變）；per-scene mp4 由 `npx remotion render build S32-<id> <av-dir>/<id>.mp4 --props=…` 逐場產出（每場一個 composition，先例 `S31-<id>`）；`pauses:` 缺席即不折。紅測試：`_selftest_rewatch_pack_remotion.py` 用 ffmpeg 合成兩段小片（一段 3 s 靜止、一段 14 s 靜止）＋手寫 manifest，證明 exit 0／exit 1 兩向；既有 `_selftest_rewatch_pack*.py`（若有）維持綠。

---

## 5. 派工形狀（問題 3；依根 `CLAUDE.md`「Remotion 影片的設計與動畫製作 → motion-designer」）

> **共同紀律：** 各自 worktree、先 `git merge main`、一 task 一 commit（subject ≤70 字、body 繁中逐條、`Co-Authored-By`）；回報＝改了哪些檔、測試數字、沒做到的條款；子代理各用 `<scratchpad>/task<X>/`；派工時明說「哪些閘我驗過、你不用跑」（§六 6.8 ⑤）。**motion-designer 呼叫時不傳 `model`**。所有 task **零計費**——TTS 只由主對話在 B1 做一次。

### B0／Task 0 — 工具線（`subagent_type: general-purpose`、`model: opus`；先於一切）

改：`pipeline/s32_derive.py`＋`_selftest_s32_derive.py`（§3.2）、`pipeline/remotion_sync_check.py`＋selftest（§4.3 ①）、`rewatch_pack.py` 三旗標＋`_selftest_rewatch_pack_remotion.py`（§4.3 ③）、第一版 `paper/s32/s32.yml`（marker 舊名原樣）、`paper/s32/SCRIPT.md` 骨架（28 場標題＋每場的舊 marker 清單，畫面欄留空給 Task 1）。
驗收：① `run_selftests.py` 開工基線（main 現況 24；schema 線併入後 25）＋3 全綠；② `s32_derive.py --check` 綠、`tts.py … --backend mock --unit beat` 對 `s32.yml` exit 0（28 場：silent 5／beats 23）；**schema 線已併入時另加 `check_storyboard.py s32.yml` 0 error、且 WARN 裡沒有「Manim gen-2 field」**（＝派生沒把遺留欄位抄過來）；③ `rewatch_pack.py` 對 `s31`（主 checkout 有 `s31_scene` 音檔與 composition）跑通一包（證明 Remotion 佈局讀得動）；④ 舊路徑（Manim 參數）的 `rewatch_pack` selftest 不變；⑤ `tools/doc_lint.py` 主 checkout clean。
不准動：`paper/src/`（除 `timing.ts` 常數的讀取方式不動）、任何 `.md` 內容稿、`tts.py`。

### B1 — 音檔到位（主對話；D1）

依 §3.3 分支 R 或 S；報量 → 同意 → 執行 → `listening_pack` HTML → 使用者聽感人閘 → 音檔備份到主 checkout `video/output/ch03/s3.2/audio_mimo/`。**B2 可與 B1 並行**（設計稿不需音檔），**B3 要等 B1**（G0：TTS 完成才動畫面時序；`atWord()` 要真對時）。

### B2／Task 1 — 分鏡設計＋風格幀（`subagent_type: motion-designer`；D4 (i)）

輸入：`s32.yml`（mock manifest）、`ch03_chain_rule.md` 的 `visual_need`／`animation_cue`／`screen_contract`、`chapter3.tex:208–416`（Fig 3.5 合成映射、Fig 3.6 餘項幾何）、`paper/STYLE.md`、`s31/SCRIPT.md` 格式。
交付：
1. **`paper/s32/SCRIPT.md`**：28 場逐場逐拍表（旁白英文原句照登＋畫面＋上畫面 TeX 逐字＋`source`＋`covers`），marker 改名表，敘事取向與新增設計語彙（比照 s31 SCRIPT 開頭兩節）。**§3.2 的版型需求**：定理頁（Thm 3.3）、策略卡（Strategy 3.1 五步）、**兩張圖版頁**（Fig 3.5 三軸合成映射動畫、Fig 3.6 切線餘項 h 減半動畫——內容稿兩個有 `animation_cue` 的單元）、定義頁（Def 3.1）、**證明四連頁**（`proof_setup_substitution` → `proof_delicate_bound`，鏡頭鎖定、前列留在畫面上——STYLE.md 鏡頭紀律第 1 條；$R_3(h)/h$ 主線跨四場要有視覺連續物，對應 Manim 版的 `carry` 候選）、例題頁 ×5（含 caution 紅字 rubric）、依賴鏈圖（`example_leibniz_rates` 的 $O\to U\to K$）、recap、片尾。
2. **7 張風格幀**（`npm run s32:stills` 到 `out/s32_stills/`，PNG 進回報、不進版控）：節首頁、定理頁、Fig 3.5、Fig 3.6、證明頁（第 3 頁 ε-δ）、例題頁（ex:3.6 三層）、recap。
3. 第一版 `src/s32/`：`timing.ts`／`kit`（沿用 `s31/kit.tsx`，只加 §3.2 需要的元件）／`S32.tsx` 場序守門／7 張幀對應的場景骨架。
成功標準：`npm run lint`（tsc）clean；7 張幀在手機寬尺標下可讀（STYLE.md 字級下限）；pedagogy gate-1 對 SCRIPT.md **PD／OF／SC blocking＝0**（武裝前提見 §4.1）；**使用者看過 7 張幀＋SCRIPT.md 拍板**（人閘；停等點 ①）。
不准動：`say` 文字；`src/s31/`、`src/q7/`、`src/components/`（要改共用元件先回報，不擅改——§3.1 與 Q7 的成片逐像素不可變）。

### B3／Task 2–4 — 三幕實作（`subagent_type: motion-designer` ×3，**Task 2 先、3 與 4 並行**）

| Task | 場（依 `_mimo.yml` 序） | 為何這樣切 |
|---|---|---|
| **2 第一幕「The Rule You Can Use」** | intro、divider_rule、why_composition_is_missing … decomposition_strategy_repeat（9 場，含 Fig 3.5） | 先做的一幕要把 `s32` 的版型與共用元件定型（定理頁、策略卡、圖版頁），3 與 4 只加場景檔 |
| **3 第二幕「Why the Rule Is True」** | divider_why、proof_strategy_bridge … proof_delicate_bound（9 場，含 Fig 3.6、Def 3.1、Prop 3.3、四頁證明） | 最難的一幕（full ε-δ）；證明四連頁的鏡頭鎖定與跨頁連續物是本節最可能出 must 的地方 |
| **4 第三幕「Using the Rule」** | divider_use、5 例題、caution、toward_section_3_3、recap、outro（10 場） | 版型重複度高（例題頁 ×5），適合並行 |

每個 task 的成功標準（一樣）：① 該幕每場的 `S32-<id>` composition 可 render（真音檔 manifest）；② 自審迴圈至少兩輪（agent 定義檔的必做）；③ `tsc` clean、render 全程無 `[label-guard]` throw；④ 該幕逐場抽幀（每拍一張）附在回報；⑤ SCRIPT.md 該幕拍表與實作一致（改了拍就回寫表）；⑥ 只動 `src/s32/scenes/<該幕>` 與 `S32.tsx` 的登記行；⑦ 一個 commit。**不跑生成式盲審**（輪內不跑，§六 6.2）。

### B4 — 一輪（G5 批次化）：一次 merge → 一次 1080p render → 一次審

```
# 主對話（擁有 main 與 render）
git merge <task2> <task3> <task4>                                   # 各自 worktree 交 hash
cd video/experiments/remotion_styles/paper && npx remotion bundle
npx remotion render build S32 out/s32_raw.mp4 --codec=h264 --crf=20 --props='{"manifest":"audio/s32_scene/manifest.json"}'
for id in <28 場>: npx remotion render build S32-<id> out/s32_av/<id>.mp4 --props=…     # rewatch_pack 的 per-scene 輸入
python video/pipeline/remotion_sync_check.py --manifest …/s32_scene/manifest.json --mp4 out/s32_raw.mp4          # ≤2 幀
python video/pipeline/rewatch_pack.py --storyboard …/s32/s32.yml --manifest …/s32_scene/manifest.json \
       --av-dir …/out/s32_av --lead-seconds 0.5 --tail-seconds 0.9 --out <round dir>                      # [still-gate] PASS
python video/pipeline/run_selftests.py                                                                   # 全綠
# gate-1 subagent（免費）：visual-frame-audit 讀 <round dir> 的 contact sheet → 視覺 blocking == 0
```

輪內回歸清單（§六 6.2 三欄表：上一輪 finding｜已關／未關｜證據）；**新 must 上限 3 條**，超過退回內容階段。需要再一輪就照同一形狀：收齊 must → 併行派工 → 一次 merge → 一次 render → 一次審。**閘的輸出完整落檔再讀，禁止 `| tail -N`**（§六 6.4）。

### 5.4 停止條件（G3；Remotion 形，開工前寫死）

四條同時滿足即收工，剩下的 should 進 backlog：

1. **視覺 blocking＝0**（visual-frame-audit）。
2. **R2 must＝0**（第二輪起生效；第一輪只看 1、3、4——§六 6.3 定案）。
3. **量測護欄**：本輪若是被 12 s 靜止指標驅動的，fine 最長靜止逐場 |Δ| < 0.5 s 連續兩輪才停；若是被 must 驅動且條件 2 已成立，本條視為滿足（§六 6.3 (a)/(b)）。
4. **確定性全綠**：`run_selftests` 全綠＋`remotion_sync_check` PASS＋`[still-gate] PASS`＋`tsc` clean＋render 無 label-guard throw＋（schema 線併入後）`check_storyboard.py s32.yml` 0 error（＝ Manim 版「`[sync]` 0＋sizecheck 0 error」的對等物）。

### 5.5 里程碑審與 final

- 達標後 **一次**完整六鏡（R1 初學者 ×2／R2 動畫導演／R3 教學設計／R4 節奏剪輯／R5 講師；契約 [`REWATCH-REVIEW-RUBRIC.md`](content_scripts/_audit/REWATCH-REVIEW-RUBRIC.md)），agy ×3 逐次徵同意（D5），鏡頭產出先過 lens QA 四件事（§六 6.2）；`must` 一個批次輪關掉。
- final：`python scripts/loudnorm.py out/s32_raw.mp4 out/s32_final.mp4`（house −19 LUFS）→ `python scripts/chapters.py …/s32_scene/manifest.json out/s32_chapters.txt --embed out/s32_final.mp4` → 成片＋`RENDER.md`（manifest 路徑與 sha256、render 指令、時長、LUFS）。**4K 不在本節**（Remotion 版的解析度政策由 README／CLAUDE.md 的 1080p 規則管，未要求 4K）。
- **Phase B applied HTML**：`content_scripts/_audit/REVIEW-ch03_chain_rule-s32-phaseB-applied.html`（待建；根 `CLAUDE.md`「每完成一輪都要產 HTML」），逐場並列：拍表、抽幀、閘結果、輪次回歸表。

---

## 6. 成本量測欄位（問題 4；填 [`REBUILD_STATUS.md`](REBUILD_STATUS.md)「每節成本量測」的 **§3.2 Phase B** 一列＋分項）

既有五欄在 Remotion 版的定義（**同一張表加一列，不另開表**；「客製 hook 數」這一欄的欄名不改，表下加註 Remotion 的量法）：

| 欄位 | Remotion 版怎麼量 | 填的時機 |
|---|---|---|
| audit／撰稿 tokens | 每個子代理回報的最終累計 token（Task 0／1／2／3／4、pedagogy gate-1、visual-frame-audit 每輪、REWATCH subagent ×3）＋外部計費分列（agy 三鏡的 `usage`） | 每個 task／每輪結束即記，不事後估 |
| render 次數 | 全片 1080p `S32` render 的次數（mock 的另計；per-scene `S32-<id>` 的 batch 算 1 次） | 每輪 +1 |
| 客製 hook 數 → **客製場景元件數** | `src/s32/scenes/*.tsx` 的檔數（基線＝28，每場一個）＋ `src/s32/kit` 新增的共用元件數（另列）；與 §3.1 Remotion 版比較用 | B3 結束 |
| 真 TTS calls | manifest `receipt.backend_calls` 累加（R 分支預期 0、S 分支預期 23–35）；含之後移 marker 造成的 beats 場重合成 | B1 結束、之後每次 tts |
| 回歸輪數 | B4 的輪數（＝全片 render 次數－1，若沒有無 render 的輪） | 收工 |

Phase A 已在記的三個數字**續記**（§3.1 沒有）：**牆鐘**（Phase B 日曆天＋各 task 的 render 時間；motion-designer 回報含 render 時間）；**停等點**（① 7 張風格幀人閘、② B1 報價同意、③ 聽感人閘、④ agy 同意——預計 4 個）；**並行摩擦**（merge 衝突次數——預期熱點＝`S32.tsx` 登記行；等 render 時間窗次數；`npm ci` 各 worktree 一次）。

Remotion 版**新增兩個**：**render 牆鐘／片長比**（§3.1 第三幕 192 s 片 render 2 分 40 秒 ≈ 0.83×；本節 ≈ 13 分片預估 10–12 分）與 **檔案大小**（crf 20 的 MB/s；紙紋是主要成本，STYLE.md「檔案大小」）。

---

## 7. 本檔的驗收（立檔輪）與 Phase B 的完成定義

**立檔輪（本輪，2026-09-28）：**

- [x] 本檔內每一個路徑用腳本逐條檢查：既有路徑必須存在；下表「待建」路徑必須**不存在**（存在＝有人先做了，要回頭對齊）。
- [x] `python tools/doc_lint.py` 主 checkout clean（本 worktree 的 2 條既有斷鏈屬 gitignored 成片，非本輪）。
- [x] [`KICKOFF-s32-chain-rule.md`](KICKOFF-s32-chain-rule.md) 頂註加一行指向本檔。
- [x] [`REBUILD_STATUS.md`](REBUILD_STATUS.md) §3.2 那列更新（音檔遺失事實＋本檔）。
- [x] [`KICKOFF-remotion-unification.md`](KICKOFF-remotion-unification.md) §6 第 2 條標已完成。
- [x] 一個 commit，零 API 呼叫。

**待建路徑（Phase B 開工後才會出現；立檔時檢查為不存在）：**

| 路徑（一列一個，供腳本逐條檢查） | 誰建 |
|---|---|
| `video/experiments/remotion_styles/paper/s32/s32.yml` | Task 0 |
| `video/experiments/remotion_styles/paper/s32/SCRIPT.md` | Task 0 骨架、Task 1 填 |
| `video/experiments/remotion_styles/paper/s32/RENDER.md` | 主對話（final） |
| `video/experiments/remotion_styles/paper/src/s32/` | Task 1 起（含 `timing.ts`／`kit`／`S32.tsx`／`scenes/`） |
| `video/pipeline/s32_derive.py` | Task 0 |
| `video/pipeline/_selftest_s32_derive.py` | Task 0 |
| `video/pipeline/remotion_sync_check.py` | Task 0 |
| `video/pipeline/_selftest_remotion_sync_check.py` | Task 0 |
| `video/pipeline/_selftest_rewatch_pack_remotion.py` | Task 0 |
| `video/experiments/remotion_styles/paper/public/audio/s32_scene/` | B1（gitignored） |
| `video/experiments/remotion_styles/paper/public/audio/s32_mock/` | B0（gitignored） |
| `video/experiments/remotion_styles/paper/out/s32_stills/` | Task 1（gitignored） |
| `video/experiments/remotion_styles/paper/out/s32_av/` | B4（gitignored；per-scene render） |
| `video/experiments/remotion_styles/paper/out/s32_raw.mp4` | B4（gitignored） |
| `video/experiments/remotion_styles/paper/out/s32_final.mp4` | final（gitignored） |
| `video/output/ch03/s3.2/audio_mimo/` | B1 備份目標（主 checkout，gitignored；§2.2 教訓） |
| `video/content_scripts/_audit/REVIEW-ch03_chain_rule-s32-phaseB-applied.html` | 收工 |
| `video/KICKOFF-section-template.md` | 收工（SOP v1） |

**Phase B 的完成定義（全部滿足才算 §3.2 做完）：**

- [ ] 成片 `paper/out/s32_final.mp4`（1080p30、loudnorm −19 LUFS、章節點嵌入）＋`RENDER.md`
- [ ] §5.4 四條停止條件同時滿足
- [ ] 里程碑六鏡跑過一次，must 全關（should 進 backlog）
- [ ] Phase B applied HTML 寫完
- [ ] REBUILD_STATUS「每節成本量測」§3.2 Phase B 一列填滿（§6 的五欄＋三個續記＋兩個新增）
- [ ] 音檔備份在主 checkout `video/output/ch03/s3.2/audio_mimo/`（§2.2 教訓）；REBUILD_STATUS 記路徑
- [ ] 協定跑不通的地方回寫 [`REVIEW_GATES.md`](REVIEW_GATES.md) §六（至少：6.4 開工清單的 Remotion 版、6.6 付費音檔備份紀律、6.3 條件 4 的 Remotion 對等物）
- [ ] SOP v1（`KICKOFF-section-template.md`）從本檔＋[`KICKOFF-s32-chain-rule.md`](KICKOFF-s32-chain-rule.md) §4 抽出（原 §7.2 的交付目標，改以 Remotion 版為底）

---

## 8. 明確不做（連同理由）與 backlog

| 不做 | 理由 |
|---|---|
| **不改旁白文字**（D2 預設） | G0 內容鎖；Phase A 的簽核與 NFA 都綁在這 23 場 `say` 上 |
| **不自己升格 `paper/`**（D3 預設） | 升格線（§2.5）在做；本節在製作處下的 `s32/` 做，它在哪就寫哪 |
| **不自建內容層確定性檢查器的入口** | schema 線（§2.5）在做 `check_storyboard.py`；併入前由 gate-1 agent 讀 SCRIPT.md 人工覆蓋（武裝前提寫在 §4.1），併入後直接用 |
| **不做 Remotion 版的 `sizecheck`／字級確定性閘** | 沒有現成量測層；先靠 STYLE.md 契約＋幀審。若 visual-frame-audit 連兩輪抓到同類字級／出框 blocking，再立案 |
| **不改 `src/s31/`、`src/q7/`、`src/components/`** | 兩支成片逐像素不可變（README 的先例：s31／act3 不載中文字型、開場幀逐像素不變）；共用元件要改先回報 |
| **不重跑 NFA、copyedit、六鏡內容審** | 文字未動；重跑＝每輪製造工作（§六 6.2） |
| **不做 4K** | Remotion 線未定 4K 政策；1080p 是現行規則 |
| **不並行開 §3.3** | 2026-09-13 裁決 4：先用 §3.2 把流程走成熟、產 SOP v1，之後才並行 |
| **不修 `.claude/launch.json` 的 `remotion-review`** | unification §6 第 4 條另案 |

**backlog（本輪發現、寫給後續輪次）：**

- `tts.py` 的 `_IDENTITY_KEYS` 含 `output_dir` 絕對路徑 ⇒ 音檔換機／換目錄就失去 reuse（§3.3 R 的 (b) 選項）；要不要改成相對路徑或拿掉，屬工具線契約變更＋紅測試。
- Remotion 版的 authoring 層靜止 advisory（Manim 的 6 s `[stillness]` 沒有對應物）；可在 `rewatch_pack` 的 pack 裡加一個 6 s 的 warn 行（不擋）。
- `derive_spoken.py`／`.spoken.yml` 雙軌在 Remotion 線的去留（DESIGN.md「MiMo 口語軌」留白）：§3.2 因為 Phase A 已走完雙軌所以沿用；從 §3.3 起若分鏡直接寫口語，`.spoken.yml` 就是分鏡本身，`s32_derive.py` 這類派生腳本不需要。
- 付費音檔備份紀律（§2.2）回寫 §六 6.6。

# 講義 → 影片產線重建 — 進度與待辦

> 本檔是跨對話的進度錨。完整施工計畫在 `.claude/plans/`(gitignored,撈不回),故重點留存於此。

> ⚠️（2026-06-03 預告 → **2026-06-10 已發生**）講義生成流程重構已落地為 HTML handout kit（`experiments/handout_kit/`，experiment/seed-converge 分支），影片產線輸入已隨之換源——決策與影響見下方「**2026-06-10 輸入換源**」節。gen-2 工具鏈主體沿用；`review_pack.py` 的 `.tex` parser 如預期作廢待改 HTML，「四 lens ＋ advisory ＋ 四級人工過濾 ＋ 計費閘門」的**做法**不變。

## 🔄 2026-06-10 輸入換源（HTML 講義）＋ §1.1 正式版啟動

**研究結論（流程體檢）：** gen-2 產線主體（make.py／lint／sizecheck／音訊驅動對齊／intro·outro 模板／Direction B／critic.py／narration 方法論）皆與輸入格式無關，**不需重建**；需要改的只有輸入契約層，已同步：[`README.md`](README.md)「輸入」、[`DESIGN.md`](DESIGN.md) data flow 首格、[`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md)（§1 忠實對象、§2 略過清單、§3 對應表換鍵成 kit 語意 class＋新增 `env-caution` 列、§6 `source` 欄格式、§8）。

**使用者拍板（2026-06-10）三項：**
1. **§1.1 從零重走全流程**——不繼承校準原型的 16 段已認可 narration；內容稿 v2 以 HTML 權威檔重新拆解、重寫、重新認可。連帶：`output/audio/ch01_inverse_functions/` 的舊真旁白 WAV 不可重用，真 TTS 屆時全節重新計費（先報價徵求）。
2. **本輪先靜態版成片，客製動畫第二輪接入**——先出模板靜態 mock 驗收格局，認可後再建正式 hook 機制（task #6）＋生成動畫。
3. **ch01 內容權威檔 = [`chapter1-standalone.html`](../experiments/handout_kit/chapter1-standalone.html)**（非 example-ch01/ 片段；ch02+ 權威檔屆時另定）。

**現況事實核對：** ch01 HTML 與 `ch01_foundations.tex` 內容 verbatim 同源（抽查多處逐字一致；HTML 僅剝 `\index`、交叉引用改手寫編號）。§1.1 的 5 個動畫 hook code **未落檔**（repo 無檔、工程稿全標 `# HOOK(待補)`——下方舊待辦「已於先前 session 完成」實為 cue 層面，code 未進版控），第二輪需重新生成。

**§1.1 v2 進度（同日完成至 mock）：**
- ✅ 內容稿 v2（[`content_scripts/ch01_inverse_functions.md`](content_scripts/ch01_inverse_functions.md) 覆寫，沿用 deck id）：17 單元（v1 為 16；Remark 1.2 變數改名升格獨立單元，有偏離註記）、4 個 animation_cue（u2 兩進一出、u6 水平線 sweep、u12 往返、u13 翻摺）。**15 段 narration 已於 2026-06-10 經使用者認可。**
- ✅ 工程稿 v2（[`storyboards/ch01_inverse_functions.yml`](storyboards/ch01_inverse_functions.yml) 覆寫）：17 場景，say＝認可 narration 原文＋`{show}` 標記；4 處 `# HOOK(第二輪)` 註記動畫接入點；graph 場景座標沿用 v1 已調校資產（工程層經驗，非內容繼承）。
- ✅ 守門員＋mock 成片：lint clean、sizecheck consistent，480p mock 全 17 場景 compose 成功（`output/ch01_inverse_functions.mp4`，≈8'42"）。1080p 預覽版同日 render。
- ⚠️ 踩坑記錄：make.py 背景 render 時**不可並行**再跑 sizecheck/manim——兩程序搶 `media\Tex\` 快取，會互相打出 PermissionError／dvisvgm ValueError 假錯（單跑即消失）。
- ✅ **視覺批改第一輪（2026-06-10，Claude 親自當 critic）**：用 `critic.py --dry-run` 免費抽幀、Claude 直接讀幀（不送外部 VLM、零計費），依 DESIGN 五維提 7 findings，使用者全採納並已修复重渲複驗：①`definition_math` statement+math 改整組垂直置中（原錨點式佈局內容少時拉出大片死帶，影響 7 場景）②`recap_cards` bullet 間距改按實際 wrap 高度累進（原固定 pitch 1.2 三行條目擠壓黏連，sizecheck 盲區）③`example_walkthrough` takeaway 色改語意制（`takeaway_tone: warn|ok|neutral`，原固定 warning 紅把正面驗證染成錯誤色）④`heading_rich`／graph_focus `_title` 的標題 inline math 補乘 `TEX_TEXT_SCALE`（原縮水 ~25%）⑤`brand._wrap_prose_tex` 把 math span 後的標點黏回（原「$y$ .」「$x$ ,」浮標點）⑥模板 `kicker` 覆寫欄（motivation 場景不再掛 DEFINITION eyebrow）⑦場景 06/13 圖元修正（parabola 平頭、兩標籤撞線、`y=x` 標籤 label_role 改 muted——line label 預設 warning 是個坑、(a,b)/(b,a) 點補名）。
- ⬜ 下一步：使用者看 1080p mock 驗收格局 → 第二輪（hook 機制 task #6＋4 動畫生成接入）→ 真旁白 TTS（計費，先報價）→ VLM critic（計費）→ 4K 定版。

**待辦（換源遺留）：** `review_pack.py` faithfulness lens parser 改吃 HTML（§1.1 v2 先人工對照，parser 後補）。

## ✅ 已完成

### 設計 brief 同步
- [`design_handoff/DESIGN_BRIEF.md`](design_handoff/DESIGN_BRIEF.md):從舊「Midnight Canvas（全暗）」同步成現行 **Direction B（雙 ground:暗底教學 / 淺底品牌）**,真實 tokens、8 模板對應、SummitBars/logo 規則。原標的兩個 token-vs-實作分歧(字體、格線)**已定案**——見下。

### 設計分歧定案(2026-06-02)
- ✅ **字體**:全 **Computer Modern**(`CMU Serif`/`CMU Typewriter Text`),刻意不採 tokens 的 sans 提案(Space Grotesk/Hanken/JetBrains)。理由:body 與 math 同族、字型可內嵌免連網、無 `✓✗∎` tofu。
- ✅ **格線**:不露出(`theme.py` `SHOW_GRID=False`),要乾淨深藍底;`grid_line` 色留作潛在 motif。「Blueprint Grid」名字保留為調性,非字面格線。
- 文件已同步:`DESIGN_BRIEF.md`(§3、§5、§7)、`theme.py` 與 `brand.py` docstring。`tokens.json` 為設計師交付原件,不改;偏離由本專案文件記錄。

### 第一階段:內容方法論
- [`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md):萃取 gen-1 `legacy/MANIM_STORYBOARD.md` 教學精神、剝離 gen-1 工程、適配 gen-2。決議:**內容/範圍緊跟講義,但場景順序為教學自由重排**;Gemini 直讀 LaTeX(無 spoken-math 表);動畫 code 由 Claude 依內容稿的自然語言 `animation_cue` 生成(內容稿本身只給自然語言、不寫 manim)。含**內容稿格式**(`id/source/learning_goal/kind/narration/visual_need/animation_cue`)。
- [`content_scripts/ch01_inverse_functions.md`](content_scripts/ch01_inverse_functions.md):§1.1 內容稿(16 單元,校準樣本)。**16 段 narration 已認可。**
- 兩條校準細則已補進方法論(§3 規則+圖合拆;§5 視覺用具體函數示範)。

### 第二階段:重建工程 —— 里程碑「§1.1 mock 成片」**達成**
- [`make.py`](make.py):**單一 orchestrator**(`parse→synth→render→compose`),取代 gen-2 三 CLI 手動串。mock backend(靜音)。
- [`storyboards/ch01_inverse_functions.yml`](storyboards/ch01_inverse_functions.yml):§1.1 工程稿(16 場景,gen-2 格式 + `source` + `# HOOK` 動畫接入註記)。
- **mock 成片產出**:`output/ch01_inverse_functions.mp4`(16 場景,≈5'45",靜音、動畫模板頂著版)。`output/` 為 gitignored。
- **底層資產零重寫沿用**:`scene.py` 對齊核心、`theme`/`brand`、`audio`、`blocks`、`narration`、ffmpeg mux/concat。

### 第二節:§1.6 symbol-heavy 壓力測試 —— 里程碑「§1.6 mock 成片」**達成**
- [`content_scripts/ch01_precise_limit.md`](content_scripts/ch01_precise_limit.md):§1.6 內容稿(16 單元)。**narration 已認可。** 套 §5 symbol-heavy 例外(~90% 符號 → 只 2 視覺:ε-δ 管狀圖 anchor + 動機圖);首次實跑 theorem/proof 拆單元、repeat-pattern、對齊鏈 narration。
- [`storyboards/ch01_precise_limit.yml`](storyboards/ch01_precise_limit.yml):§1.6 工程稿(16 場景)。ε-δ 管狀圖用 4 條 dashed line + function + hollow point 重現(忠於講義 fig:precise-limit,書本亦用虛線界線);收緊 ε 動畫以 `# HOOK` 註記待接入。
- **mock 成片產出**:`output/ch01_precise_limit.mp4`(16 場景,≈9'18",靜音、動畫模板頂著版)。8 張關鍵 frame 已逐一目視驗收(anchor/定義/證明/procedure/recap/例題)。
- **render 階段抓到 2 個 lint+sizecheck 都漏的 bug**(已修,詳見內容稿校準筆記 §7-8):(a) prose sibling 內嵌 math 被縮小觸發 sizecheck → step text/points 改純英文;(b) recap formula 過寬靜默出框 → 改短(ε-δ 兩半式)。✅ **已實作 overflow guard**:`sizecheck` 對每個 scene 量 bbox(off-frame=error／超安全區=warn,見 `sizecheck.py`),DESIGN.md checklist 亦增一列;guard 一上線就抓到 `ch01_inverse_functions` recap formula 出框,已用 `recap_cards` 右欄左移修掉。

### pipeline-hardening 線（2026-06-02）：守門員 + VLM 視覺批改

mock 成片之後,在 `video/pipeline-hardening` 分支做了一輪產線加固（採納 Code2Video 機制,見 [`CODE2VIDEO_STUDY.md`](CODE2VIDEO_STUDY.md)）,皆已 commit：

- **P0 重疊偵測 guard（`bfbbc04`）**：`sizecheck.py` 加 `_overlap_issues()`——確定性、零 API,測兩個螢幕空間 content block 有沒有撞。`Block` 多了 `layer` 欄位（content|graph|decoration|background），只有 content 參與。**新模板規則**：graph 場景的 axes/plot/label/ticks 標 `layer="graph"`、motif/分隔線標 `decoration`,否則誤報。
- **M1 文件（`5392017`）**：P2 修補階梯寫進 [`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md) §5、P3 AES 五維 QA 表寫進 [`DESIGN.md`](DESIGN.md)。
- **解析度慣例（`b38200f`）**：測試／預覽用 1080p（`make.py --quality high`,預設）、正式交付才 4K（`--quality 4k`）。⚠️ make.py tier 語義變了：`high` 從 4K 改成 1080p@30、新增 `4k`。
- **P1 VLM 視覺批改（`8b722dd`、`2a2e752`）**：`pipeline/critic.py`——抽每場景最滿幀 → MiMo-V2.5 → `output/critic/<id>/critique.{json,md}`（純建議、計費,key 走 env `MIMO_API_KEY`）。用法見 [`README.md`](README.md)「VLM 視覺批改」、**迭代流程見 [`DESIGN.md`](DESIGN.md)「The review loop」**。MiMo 接入：小米官方 `api.xiaomimimo.com/v1`（OpenAI 相容、`mimo-v2.5`、auth header `api-key`）。兩個雷：① 推理模型,`max_completion_tokens` 要設大（8000）否則 content 空;② 回的 JSON 內含 LaTeX,反斜線非法 escape,parser 要容錯。其餘坑見 README「踩過的坑」。
- **§1.1 review loop 實戰**：VLM 抓到並修掉 4 個 lint/sizecheck/P0 看不到的語意/位置缺陷,每條都 VLM 複驗過：example 結論提前曝光（`d4f1af1`,左右欄綁一起漸進揭示）、graph 定義域沒畫（`d4f1af1`）、y=x 標籤跑到 y 軸頂（`04a56ce`,graph_focus line 加 `label_point` 支援）、reflection 缺 (a,b)→(b,a) 對應點（`a35b873`,加兩點+鏡射連接器）。

### 內容 cross-review 線（2026-06-03）：DeepSeek 文字審 + review_pack.py

把 Code2Video P1 的「模型提案、人定奪」從**視覺層**延伸到**內容層**。新增 [`pipeline/review_pack.py`](pipeline/review_pack.py)——critic.py 的文字版姊妹，四 lens 對 content script / storyboard / `.tex` 做 cross-review：

- **四 lens**：`faithfulness`（`.tex`↔narration 忠實度）、`register`（旁白口語化 §4）、`decomposition`（拆解 §3/§5）、`engineering`（生成 hook code 的數學保真＋慣例，需 `animations/<deck>_hooks.py`，§1.1 無 code 故自動跳過）。用法見 [`README.md`](README.md)「內容 cross-review」。
- **模型**：DeepSeek `deepseek-v4-pro`（OpenAI 相容、Bearer、key 走 env `DEEPSEEK_API_KEY`，**不寫檔不進 git**）。推理模型，out ≫ in、`max_tokens` 設大；JSON 容錯沿用 critic.py（回的 JSON 內嵌 LaTeX 反斜線）。成本閘門同 critic：`--dry-run` 免費、`--confirm` 計費、`--smoke` 驗一發。
- **§1.1 首跑（已採納）**：28 calls（faithfulness 13 + register 14 + decomposition 1；engineering 跳過）、~19.8k in + 48k out tok、~$0.058（placeholder 價）。7 條 actionable，**人依四級紀律過濾後採 2 條**——`student_id_is_one_to_one` 的軟性視覺指涉「the condition we just wrote down」改成自足、`composition_identities` 的「The defining relation」改「The definition of the inverse」（content script + storyboard 同步、lint 過）。
- **過濾層實證必要**：7 條裡 2 條過度 triage 成 L1（其實由累積語境承載／前提錯誤）、1 條幻覺（指不存在的拼錯）；decomposition 正確 0 finding。**模型自我 triage 不可盡信、advisory + 人定奪不可省**。推理模型 run-to-run 會飄（smoke 抓到的 §3 開場散文取捨，整批跑就消失）。
- **待**：engineering lens 尚未實跑（§1.1 無 hook code；§1.6 有 [`animations/ch01_precise_limit_hooks.py`](animations/ch01_precise_limit_hooks.py)，可跑四層全貌）。增量／多輪取聯集、把 review_pack 寫進 DESIGN.md 的 review loop 為後續。

## ⬜ 待辦

### 待你定案(視覺 / 內容)
- **看 mock 成片** `output/ch01_inverse_functions.mp4`:確認視覺/順序/版面。
- (字體、格線分歧已定案,移至上方「設計分歧定案」。)

### 重建後續(工程)
- 🕒 **review #8(hook 接入)—— 使用者決定晚點做(deferred 2026-06-02)。** 把客製 ε-δ／approach 曲線動畫經正式 hook 機制接進 `make.py` 成片(即下面的 task #6 ＋「客製動畫生成＋接入」,不重複細節)。**前置(blocker)**:使用者曾說 §1.6 ε-δ 動畫「還是有點問題」(具體未明)——接入前先請使用者講清楚要調什麼(見下方「待討論」§1.6 動畫)。**現況**:review #1–#7 已於 2026-06-02 處理完(8 條只剩本條);靜態 scene 7 已升級成 teaching-mode(ε/δ 半透明帶＋`a`/`L` 刻度,函數仍線性 $2x-1$),wiring 後由凸函數 $\tfrac12x^2$ 曲線動畫([`animations/ch01_precise_limit_hooks.py`](animations/ch01_precise_limit_hooks.py))取代。
- **task #6 介面精煉**(唯一未完成的里程碑 task):templates 加 `reveal_targets()` 驗 `{show}`、正式 hook 機制、`scene.py` 去 class-attribute 副作用。
- **客製動畫生成＋接入**(Claude 負責,依 `animation_cue` 自然語言生成 manim、認可後於工程稿 `# HOOK` 接入):
  - §1.1：5 個 cue(motivation 兩進一出、why-x²-fails 水平線掃描、line-test 並排 sweep、composition 往返、reflection 翻摺)—— ✅ **已於先前 session 完成**。
  - §1.6：anchor ε-δ 管狀圖 + unit 3 動機圖 —— ✅ **已生成獨立可 render scene**([`animations/ch01_precise_limit_hooks.py`](animations/ch01_precise_limit_hooks.py))。anchor 採**凸函數 $\tfrac12x^2$**(非直線):ε 一縮、舊 δ 失守 → 曲線戳出帶子(端點轉紅)→ 縮 δ 收回(轉綠),把「δ 必須回應 ε」演出來(直線做不到);unit 3 維持線性(值≠極限)。8 張 frame 已驗收。**待**:正式 hook 接入(task #6) + 使用者認可。
  - **前置**:gen-2 正式 hook 機制尚未建(見 task #6);第一支可先以**獨立可 render 的 manim scene** 產出供認可,整合接入隨 task #6 落地。
- **真旁白**:Gemini TTS(**計費**;依 CLAUDE.md 先報 beat 數/秒數/估算成本經同意才跑)。
- scaffold(內容稿→工程稿半自動)、schema/lint 獨立指令、增量快取(接 `text_hash`)。
- `output/_av/` 有舊測試殘留(21 vs 16 場景),可清。

### 內容擴展
- §1.2+ 內容稿(用方法論逐節)。
- ✅ §1.6 symbol-heavy 第二校準節 —— **已完成**(內容稿+工程稿+mock 成片);壓測通過,findings 已回饋內容稿校準筆記與本檔第二節里程碑。

## 🧊 凍結 / 棄用
- gen-2 舊上層 `pipeline/tts.py`、`build.py`、`mux.py`:被 `make.py` 取代,**暫留未刪**(底層 `scene/theme/brand/audio/blocks/narration` 仍沿用)。
- §1.1 舊 8-scene storyboard:已被 16-scene 工程稿覆寫。

## 💬 待討論 / 換機後接續錨點（2026-06-01 收尾）

今天進度已 commit;以下為**換新電腦後從這裡接**（新機先依 [`README.md`](README.md) §環境 建 `.venv` + ffmpeg shim，`output/`/`.venv`/`.deps*` 都不進版控、需重建）：

- **§1.6 動畫待續（最高優先）**:ε-δ tube（凸函數 $\tfrac12x^2$、逃脫→收回紅/綠端點）與 unit 3 逼近圖已生成獨立可 render scene（[`animations/ch01_precise_limit_hooks.py`](animations/ch01_precise_limit_hooks.py)）、8 frame 驗收過,但使用者表示**「還是有點問題」（具體未明說）**。下次續:**先請使用者講清楚動畫哪裡有問題**,再調。
- **動畫整合**:gen-2 正式 hook 機制(task #6)未建,曲線動畫尚未接進 `make.py` 成片;靜態 storyboard scene 7 現為 teaching-mode 線性版(ε/δ 帶＋`a`/`L` 刻度,2026-06-02 升級),整合時由凸函數曲線動畫取代。詳見「待辦 → 重建後續」的 review #8 條(使用者已決定晚點做)。
- **下一節候選**:§1.3（極限＋數值表＋帶洞圖）——壓 pipeline 不同面向（可能缺 table scene 型態）。
- 動畫分工新規則已生效（Claude 依 `animation_cue` 生成 manim;見 CONTENT_METHODOLOGY §5）。

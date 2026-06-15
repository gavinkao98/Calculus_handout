# 講義 → 影片產線重建 — 進度與待辦

> 本檔是跨對話的進度錨。完整施工計畫在 `.claude/plans/`(gitignored,撈不回),故重點留存於此。

> ⚠️（2026-06-03 預告 → **2026-06-10 已發生**）講義生成流程重構已落地為 HTML handout kit（`handout/`，experiment/seed-converge 分支），影片產線輸入已隨之換源——決策與影響見下方「**2026-06-10 輸入換源**」節。gen-2 工具鏈主體沿用；`review_pack.py` 的 `.tex` parser 如預期作廢待改 HTML，「四 lens ＋ advisory ＋ 四級人工過濾 ＋ 計費閘門」的**做法**不變。

## 🔬 2026-06-16 新 rubric 實跑：§1.6 六鏡＋§1.1 視覺 dogfood

用上一輪建好的四份 SSOT rubric 實跑兩個閘，順帶驗證 rubric 能當 SSOT。

**§1.6 全節六鏡（`CONTENT-SIXLENS` 首次規模實跑）：** Workflow `wf_5a8ec085-4ef`，全 19 單元（六鏡並行→refute-by-default 複驗）。**1 blocking＋2 advisory（去重自跨鏡重複；1 refuted）**；L3 語域／L4 不重複／**L5 數學 clean（0 錯，每條 ε-δ 獨立盲算過）**。
- **SL-1**（blocking｜工程公差 enrichment 散文 silent-drop）→ 使用者選方案 (a)，已折進 u2 一句 symbol-free Incorporative lead-in（不用 ε/δ、避前向引用）。
- **SL-2**（advisory｜u11 `Strategy 1.3`→`1.4`，與 §1.5 真實 Strategy 1.3 撞號）→ 已修。
- **refuted**：u9 `kind: theorem`（Prop 1.7 帶證明、適用 §3 theorem+proof 列，標 theorem 正確）。
- 紀錄：內容稿 §「六-lens 全節稽核（2026-06-16）」＋審核稿 [`_audit/REVIEW-ch01_precise_limit-sixlens.html`](content_scripts/_audit/REVIEW-ch01_precise_limit-sixlens.html)。**§1.6 內容已過六鏡閘、卡在「旁白 sign-off」人工閘。**

**§1.1 視覺閘 dogfood（`VISUAL-FRAME` gate1 首次規模實跑）：** Workflow `wf_b5e31d1e-5ed`，17 幀（`critic.py --dry-run` 抽每場景最滿幀 → 每幀一個 Claude subagent 對照 V1–V8＋A1–A7）。**0 blocking、9 advisory**，A 分均值 89–93。抽驗 2 幀（scene 14 `y=x` label 被虛線穿過、scene 5 紅色 callout 置中）確認屬實、定位準、正確判 advisory 而非 blocking。**結論：VISUAL-FRAME 當 gate1 可用——不 over-report、escalation/non-findings 正確；惟 §1.1 太乾淨，detection（抓真 blocking）那面尚未驗。**

### 待辦清單（接續用）

1. **§1.6 旁白 sign-off（使用者）：** 讀 [`content_scripts/ch01_precise_limit_narration.html`](content_scripts/ch01_precise_limit_narration.html)（重點看 u2「SL-1 補」、u8/u12/u16「新增」）。認可後才進第二階段工程：storyboard 同步成 19 場景、scene 7 凸曲線整合、3 個 ε-δ 動畫修正（挖空點誤導／曲線與 running example 不連貫／ε 過小擁擠）。
2. **視覺 polish punch-list（重跑影片時套用）：** §1.1 那 9 條（`y=x` label 挪離虛線、scene 5 callout 與 scene 15 右欄數學左對齊、scene 13 鏡射點精確化＋減交會擁擠、recap 補「mirror across y=x」子點）。
3. **模板對齊補掃：** `example_walkthrough`（callout 置中）與 `procedure_steps`（右欄數學鋸齒）——先前 `CENTER`→`LEFT` 那輪未掃到這兩個模板，視覺閘撈出，待查改。
4. **code 回報層 normalize（redesign 待續）：** `critic.py` 接 VISUAL-FRAME（runtime verbatim-inject rubric＋schema 補 A6/A7 與 V 維）＋**修抽幀新鮮度**（`--dry-run` 曾端出舊 `final.png`，視覺閘需新鮮幀才準）；`review_pack` 工程鏡待 `.tex` parser 重寫；critic/review_pack 的 PLACEHOLDER 定價。
5. **VISUAL-FRAME detection 驗證：** 挑粗節（§1.6 舊 mock，有已知 3 個 ε-δ 動畫問題）跑視覺閘，補驗「抓得到真 blocking」那面。

## 🧭 2026-06-15 審核模式重構落地（minimal-unify，部分採用）

**觸發：** 參考講義審核模式，把 video 五閘的零散（零收斂判準、severity 詞彙不一、命名衝突）收斂。決策與全圖見 [`REVIEW_REDESIGN.md`](REVIEW_REDESIGN.md)（已標部分採用）、地圖見 [`REVIEW_GATES.md`](REVIEW_GATES.md)。**本輪已落地：**

- **「Mode B」→「NFA」（旁白忠實稽核）改名**：解與講義 Mode B 的同名異義衝突。維度 D1–D7 原封不動；template `PROMPT-narration-modeB.template.md` → `PROMPT-narration-faithfulness.template.md`；commit-grep 分流（video 用 `git log --grep="NFA"`、講義保留 `Mode B`）。
- **抽 SSOT rubric＋thin prompt**：新增 [`_audit/NARRATION-FAITHFULNESS-RUBRIC.md`](content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md)、[`_audit/NARRATION-COPYEDIT-RUBRIC.md`](content_scripts/_audit/NARRATION-COPYEDIT-RUBRIC.md)，兩支 prompt template 改成「引用 rubric、不複述」。
- **每判斷閘一條收斂線**＝blocking==0；**散文閘兩讀者** gate1 Claude（免費迭代）→gate2 Codex（收斂後單次、需同意），gate2 只套 copyedit／NFA。
- **NFA reader 拆法**：穩態 1 個 narration reader（D1–D6）；`CONTENT_APPROVED=no` 才 +1 個隔離盲 reader 跑 D7 獨立重算。
- **視覺層改 figure-audit 鏡像**：gate1 Claude 抽幀 subagent（免費、每次 render）＋gate2 外部 VLM（MiMo-V2.5，間歇、計費），0–100 留當 magnitude、收斂＝視覺 blocking==0。
- **撰稿兩階段命名 DRAFT/LOCKED phase**（非 mode；「Mode」專留講義 A/B/C）；§4 Register 放寬為偏口語（允許縮寫＋引導語，守 lecture 底線）。

**待續（下一輪再做）：** code 回報層 normalize（`review_pack`/`critic` buckets 與 PLACEHOLDER 定價、critic.py 接 `VISUAL-FRAME-RUBRIC` 並加 A6/A7、抽幀新鮮度、`review_pack` 工程鏡待 `.tex` parser 修）。**講義已再次修訂——舊片全屬練習，將用本流程整批重跑。**（**四份判斷閘 SSOT rubric 已齊：NFA／copyedit／six-lens／VISUAL-FRAME**，均 2026-06-15～16 落地。`VISUAL-FRAME`＝V1–V8 blocking＋A1–A7 magnitude；`CONTENT-SIXLENS`＝六鏡 L1–L6、無 gate2、收斂 blocking==0。brand.prose 句子級散文已從多處 `align="CENTER"` 改回 `LEFT`、修「續行置中」、抽幀實測左對齊。）

## 🗣️ 2026-06-14 MiMo 旁白雙版路線落地（§1.1，已可規模化）

**觸發：** 使用者要試新路線——旁白做兩版（HTML 閱讀版＋口語 TTS 版）＋Mode B 給 codex 審＋收斂拍板，並改用 **MiMo TTS**（小米 `mimo-v2.5-tts`，公測免費）。§1.1 已 end-to-end 走通並出 1080p MiMo 成片。

**雙版旁白（§1.1）：** 版本 A＝[`ch01_inverse_functions_narration.html`](content_scripts/ch01_inverse_functions_narration.html)（MathJax 渲染、給人讀）；版本 B＝[`ch01_inverse_functions_narration_spoken.md`](content_scripts/ch01_inverse_functions_narration_spoken.md)（數學攤成口語、供不能讀 LaTeX 的 TTS）。**Mode B（codex `gpt-5.5`、read-only）** 稽核兩版＋收斂：1 blocking（內嵌 `⟨breath⟩` 標記＝非源文字，Cut）＋念法裁定（`x sub one/two`、`the point with coordinates`、`f inverse` 絕不念 reciprocal）。紀錄 [`_audit/REPORT-ch01-narration-modeB.md`](content_scripts/_audit/REPORT-ch01-narration-modeB.md)。

**MiMo backend 落地：** [`tts.py`](pipeline/tts.py) 加 `MimoTTSBackend`＋`--backend mimo`（OpenAI 相容、urllib、雙 header `api-key`＋`Bearer`、比照 `critic.py`；共用 gitignored `.env` 的 `MIMO_API_KEY`）。voice `Mia`、style＝YT 科普風（正常語速；初版「calm/慢」~120 wpm 被使用者否決、改 ~164 wpm）。**§1.1 MiMo 影片**＝`output/ch01_inverse_functions_mimo.mp4`（1080p、~12:49），reveal 對齊 MiMo beat、抽幀驗證同步＋無亂碼。**MiMo 共用既有 `MIMO_API_KEY`（原 critic VLM 用）。**

**P1–P4 改進（使用者要求一起改）＝這條路線的「最新方法」：**
- **P1 單一真相源：** [`content_scripts/<deck>.spoken.yml`](content_scripts/ch01_inverse_functions.spoken.yml)＝口語唯一源；[`pipeline/derive_spoken.py`](pipeline/derive_spoken.py)` --deck <deck>` 生成 `storyboards/<deck>_mimo.yml`＋`<deck>_narration_spoken.md`（皆標 DO NOT EDIT）；退役一次性 `_gen_mimo_storyboard.py`。
- **P2 驗證：** `derive_spoken.py --check` 守 scene/`{show}`/無 `$` parity；render 後抽幀驗 reveal 同步（我用多模態看圖）。
- **P3 音訊：** [`audio.py`](pipeline/audio.py) 加 `trim_silence`；`MimoTTSBackend` 預設裁 beat 頭尾靜音（實測 0.42s→0.08s）。
- **P4 footgun/模板：** [`make.py`](make.py) 加 `--reuse-audio`（render 讀 `tts.py` 真 manifest）＋**拒絕用 mock 覆蓋真 manifest**；NFA（旁白忠實稽核，原 Mode B；2026-06-15 改名）可重用模板 [`_audit/PROMPT-narration-faithfulness.template.md`](content_scripts/_audit/PROMPT-narration-faithfulness.template.md)、契約 [`_audit/NARRATION-FAITHFULNESS-RUBRIC.md`](content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md)（含「數學內容正確性」維度，**未認可內容的章節必跑**）。
- **P5 同步 guard（2026-06-14，Codex 本輪）：** 新增 [`pipeline/timing.py`](pipeline/timing.py) 作為 scene lead/tail、最小 beat hold、hash 與短 beat 計算的單一來源；`scene.py`、`make.py`、`mux.py`、`critic.py` 共用 `SCENE_LEAD_SECONDS`，避免 mux offset／critic 抽幀時間漂移。`make.py --reuse-audio` 現在 fail-fast 驗 manifest freshness（deck id、scene、beat count、`{show}` target、`text_hash`、WAV 存在與 WAV 時長），render 前警告短/reveal-only beat，render 後用 ffprobe 做 video duration vs `lead + narration (+ tail)` audit。`tts.py` 新 manifest 會記錄每 beat `raw_audio_seconds`／`trimmed_audio_seconds`／`trimmed_silence_seconds` 供 MiMo padding debug。離線驗證：compileall OK；§1.1/§1.2/§1.3 derive parity OK；stale hash 測試能擋；現有 §1.1 `recap beat 04 (formula.0)` 被 sync warning 抓出（0.450s audio vs 0.500s reveal anim，約 +0.350s padding）。未呼叫外部 API。

**關鍵發現：MiMo 非決定性**——同文字每次合成是不同 take（±~10% 長度），重跑不保證同長度；要定版就別重合成。

**規模化到其他節（前提：該節已有 storyboard `<deck>.yml`）：** 寫 `<deck>.spoken.yml`（依念法慣例把已認可 narration 的數學攤成口語、`{show}` 對齊正典）→ `derive_spoken.py --deck <deck>` → NFA（旁白忠實稽核，原 Mode B；gate1 Claude→gate2 Codex，未認可內容打開 D7 隔離重算 reader）→ 收斂 → `tts.py --backend mimo` → `make.py --reuse-audio`。命令見 [`README.md`](README.md)「MiMo 旁白／影片路線」、契約見 [`DESIGN.md`](DESIGN.md) 與 [`_audit/NARRATION-FAITHFULNESS-RUBRIC.md`](content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md)。**MiMo TTS 雖免費仍屬外部 API，批次合成前依 CLAUDE.md 報用量徵同意。** 注：與 2026-06-13 的 Gemini/Charon 路線並存（`make.py` mock 與 `tts.py→build.py→mux.py` Gemini 路徑不變）；MiMo 是評估中的替代音源。

## 🎬 2026-06-13 第一章 HTML 定稿 → 全章影片計畫

**觸發：** 使用者宣告 ch1 HTML 講義定稿（[`chapter1-print-standalone.html`](../handout/chapter1-print-standalone.html)，當日 import 後重生），啟動「整章做影片」。本節為跨對話錨點。

**實況校準（2026-06-14，依工作樹/`ffprobe` 核對）：** 頂層 `video/output/ch01*.mp4` 是 gitignored 工作產物，可能是測試殘件，不能只看檔名判斷完成度。當前可視為完整可看片的輸出：§1.1 Gemini 有聲 master（`ch01_inverse_functions.mp4`，2560×1440，約 14:47）、§1.1 MiMo 版（`ch01_inverse_functions_mimo.mp4`，1080p，約 12:49）、§1.3 mock preview（`ch01_limit_of_function.mp4`，480p，約 6:59）、§1.4 完整無聲 preview（`ch01_one_sided_infinite_preview.mp4`，480p，約 10:56）、§1.6 舊版 mock（`ch01_precise_limit.mp4`，1080p，約 9:19，僅作歷史預覽）。目前**不應拿來審整節**的殘件：`ch01_inverse_trig.mp4` 只有約 51 秒，且 `_media` 缺 `when_arcsin_sin_breaks`；`ch01_limit_laws.mp4` 只有約 51 秒；`ch01_one_sided_infinite.mp4` 也只有約 54 秒，請看 `_preview`。

**全章盤點（6 節，grep 核實）：** 14 定義、3 定理、7 命題、43 例題、3 strategy、21 圖；難度先抑後揚（1.3 直覺低谷 → 1.6 ε-δ 高峰）。

| 節 | 主題 | 複雜度 | 符號% | 建議單元 | 影片素材現況 |
|---|---|---|---|---|---|
| 1.1 | Inverse Functions | 中 | 55 | 16–20 | 內容稿(19 場景)＋工程稿＋4動畫＋Gemini Charon 有聲 master＋MiMo 版皆已產出；待 AV 審核與 4K/critic 決策 |
| 1.2 | Inverse Trig Functions | 高 | 55 | 18–22 | 內容稿＋六-lens＋narration HTML＋工程稿(18 場景)＋MiMo 口語軌(68 beat, derive parity OK)＋Mode B clean；reference-triangle/branch/動畫待第二輪；目前輸出殘缺，需補 render `when_arcsin_sin_breaks` 後重合整節 |
| 1.3 | The Limit of a Function | 低 | 45 | 10–14 | **已 commit `cb98ebf`**：內容稿＋六-lens、工程稿(11 場景)、mock 11/11、MiMo spoken＋Mode B 收斂；旁白本體仍待使用者正式認可，MiMo TTS 未跑 |
| 1.4 | One-Sided / Infinite Limits | 中 | 50 | 14–18 | 內容稿(16 單元)＋六-lens clean＋narration HTML＋工程稿(16 場景)＋`y_clip` plot-kind＋完整無聲 preview；待看片並連旁白一起審 |
| 1.5 | Limit Laws & Techniques | 高 | 75 | 20–24 | 內容稿(19 單元)＋六-lens clean＋可讀 narration HTML；**旁白已認可**；工程稿(19 場景)＋19 個 per-scene mock 已完成，合併成片目前是殘件，需乾淨窗口重合 |
| 1.6 | Precise Definition (ε-δ) | 高 | 80 | 16–20→19 | 舊版內容稿/工程稿/mock/動畫皆在；**HTML drift 修復已啟動於內容稿**：provenance 重指、採 3 新例題、折疊 Ex 1.42；新增/改動旁白待認可，storyboard 尚未同步 19 場景 |

**使用者拍板（2026-06-13）：例題採「代表式涵蓋」**——每個不同模式的 example 收代表單元、同型重複折疊＋註明＋指回講義（非全收、非固定幾個）。已寫進 [`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md) §2／§7。

**Drift 稽核（定稿 HTML vs 既有素材）：**
- **§1.1 = minor，已外科修復**：filename 全面改 `chapter1-print-standalone.html`；u11 例題 1.3→**1.4**、u15 例題 1.4→**1.6**（commit `eb5c53e` 重編號）；narration／圖錨（`hlt`、`inverse-mapping`）／4 動畫全數仍對得上，**不需重新認可**。import 新增 Example 1.3/1.5/1.7/1.8＋Figure 1.3：依代表式涵蓋，1.3／1.7 折疊；**1.5、1.8 已採納為新單元 u14 `repair_by_restricting`／u17 `temperature_conversion`、旁白 2026-06-13 認可**（lint clean、sizecheck consistent、兩新場景 1080p 幀驗收、整片重渲）。
- **§1.6 = significant，修復中**：內容稿已由舊 `.tex` provenance 重指定稿 HTML §1.6（~L1655–1884），並記錄現行編號 Def 1.13/1.14、Prop 1.7、Strategy 1.3、Ex 1.37/1.40/1.41。已採納三個 HTML import 新例題：Ex 1.38 wrong-definition 診斷→新 u8、Ex 1.39 常數函數任意 δ→新 u12、Ex 1.43 M-δ 證 $1/x^2=\infty$→新 u16；Ex 1.42 $\sin x$ 同型折疊於線性例。仍待：①新增單元＋兩處既有 narration 改字（recipe 收尾、linear 例開場）給使用者認可；②工程稿同步到 19 場景；③scene 7 靜態圖/動畫與 HTML Figure 1.21 拋物線一致化；④ε-δ 動畫三個已診斷問題（挖空點誤導、曲線/參數與 running example 不連貫、ε 過小構圖擁擠）修完再接入。

**產線節奏（建議）：**
- **Phase 0（免費）**：§1.1 drift 修復＋依代表式涵蓋新增 u14/u17（旁白認可、整片重渲）【✅ 2026-06-13】；使用者過目 mock 成片＋4 動畫。
- **Phase 1（§1.1 收尾）**：報價→真 TTS（計費，先報 beat 數/秒數/估算）→mux→VLM critic 複核（計費）→4K master。第一支定版、打通含計費全流程。
- **Phase 2（其餘節，難度遞增）**：§1.3 → §1.4 → §1.2 → §1.5 → §1.6。每節走完整方法論：內容稿→認可旁白→工程稿→lint/sizecheck→mock→補缺模板/plot-kind→動畫→認可→critic→TTS→4K。§1.6 殿後（最難＋drift 修復＋動畫釐清）。

**§1.3 stage-2＋MiMo Step 1–3 完成（2026-06-14，commit `cb98ebf`）：** 內容稿 [`content_scripts/ch01_limit_of_function.md`](content_scripts/ch01_limit_of_function.md)（11 單元＝9 教學＋intro/outro）補齊六-lens 稽核（math 0 錯、無 L1）與可讀 narration HTML；工程稿 [`storyboards/ch01_limit_of_function.yml`](storyboards/ch01_limit_of_function.yml)（11 場景）已落地，u2/u4/u5 標 `# HOOK(第二輪)`，u4 三圖以 `graph_compare` 兩 panel＋annotation 頂著，真正三 panel 同步逼近留 hook。lint clean、sizecheck 0-error、11/11 mock render 抽幀驗收；`output/ch01_limit_of_function.mp4` 為 480p mock preview（約 6:59）。MiMo 路線：[`ch01_limit_of_function.spoken.yml`](content_scripts/ch01_limit_of_function.spoken.yml) → `_mimo.yml`＋`_narration_spoken.md`，derive parity OK；Mode B（CONTENT_APPROVED=no → D7 必跑）round 1 = 1 blocking＋3 advisory，round 2 = 0 blocking＋1 advisory，所有數學內容 clean。採納的 canonical fix：Ex 1.17 表格右側值補齊 `0.4762, 0.4975, 0.4998` 並改正「closing in」順序；spoken-only fix：`s(t+h)`／複雜分式 grouping 加 `the quantity`。**旁白本體仍 pending 使用者正式認可；Step 4 MiMo TTS（外部 API/計費閘門）未跑。**

**§1.2 stage-1 完成（2026-06-14，使用者指示先做 §1.2）：** 內容稿 [`content_scripts/ch01_inverse_trig.md`](content_scripts/ch01_inverse_trig.md)（deck id `ch01_inverse_trig`，18 單元＝16 教學＋intro/outro）依 HTML 權威檔 §1.2 從零拆解、撰寫。三段平行（arcsin 全展開／arccos／arctan 以「same idea」承接、只講差異點）以 spiral 紀律避免炒冷飯；6 例題各帶新模式全收、3 命題 fold 進定義單元、2 caution＋2 remark 依 §3 安置；參考三角形為招牌手法（u8 建、u13/u14 重用）。撰稿後跑**六-lens 對抗式稽核**（faithfulness／decomposition／register／no-repeat／math-accuracy／completeness，Workflow `w7pmoproz`）＋逐 finding 獨立驗證：13 raw → 1 actionable → **math 0 錯、無 L1、0 幻覺**；採納修 u11（補回 particle 結論）＋u3 cue＋u9 備註（紀錄見內容稿 §7）。可讀審核稿 [`ch01_inverse_trig_narration.html`](content_scripts/ch01_inverse_trig_narration.html)（MathJax，比照 §1.3 `_narration.html`）。**待使用者認可旁白** → 認可後才進工程稿；reference-triangle 視覺（新模板或 hook）為第二階段工程缺口。**未動計費 API。**

**§1.2 stage-2 完成（2026-06-14，使用者選「先建 storyboard 再走 MiMo」）：** 工程稿 [`storyboards/ch01_inverse_trig.yml`](storyboards/ch01_inverse_trig.yml)（18 場景；`say`＝narration 逐字＋`{show}` marker，68 beat）依內容稿映射：定義→`definition_math`、例題→`example_walkthrough`、非一對一／限定分支圖／cos 波→`graph_focus`、六函數對照→`value_table`、recap→`recap_cards`。**lint clean＋sizecheck consistent＋mock 1080p 全 18 場景逐幀驗收**（math 全渲、graph 正確、6 列表入框、arc 運算子正確、step 列等寬）。**工程缺口（本版既有模板靜態頂著，標 STAGE-2）：** reference-triangle 圖（u8/u13/u14；`graph_focus` 無三角/角弧 primitive 且強制畫軸）以建構步驟承載、標籤化三角形圖待新模板或 hook；cosine/tangent 分支圖、動畫（u3/u4/u7/u11 cue）亦待第二階段。**MiMo 口語軌：** [`content_scripts/ch01_inverse_trig.spoken.yml`](content_scripts/ch01_inverse_trig.spoken.yml)（數學攤口語、`{show}` 鏡像正典）→ `derive_spoken --check` parity OK → 生成 `_mimo.yml`＋`_narration_spoken.md`。**Mode B（codex read-only，CONTENT_APPROVED=no 故 D7 必跑）：2 blocking＋1 advisory 全採納**——D7 數學全 clean（codex 獨立重算每值）、D1 clean；2 個 D3 口語歧義（$\tfrac{1}{2\sqrt2}$／$\tfrac{\sqrt3}{2}$／$-\tfrac{2\sqrt5}{5}$）改「the quantity／all over」、header「已認可」advisory 修；regression 過（[`_audit/REPORT-ch01_inverse_trig-narration-modeB.md`](content_scripts/_audit/REPORT-ch01_inverse_trig-narration-modeB.md)）。**產線修復（三項，皆複驗）：** ① video Tex 模板補 `\arccsc`/`\arcsec`/`\arccot`（[`pipeline/_bootstrap.py`](pipeline/_bootstrap.py)——書 preamble 有、manim 預設無，原致 u15/u16 latex error）；② `brand.prose` wrap-vs-scale 修隱性 bug（[`pipeline/brand.py`](pipeline/brand.py)：只對字面 `\\` 換行縮放，含 inline LaTeX 指令（`\arcsin` 等）的長 step／point 改換行不縮小——三 deck sizecheck 複驗 §1.2/§1.1 consistent、§1.6 無新 error）；③ `derive_spoken` 念法慣例表補「複雜分數」列。**Windows 環境坑（記錄供後續節）：** manim render／sizecheck 受 Defender 掃 `media\Tex` 鎖檔，隨機噴 PermissionError／「dvi→svg 不支援」假錯（同 README 既有警告，與並行無關、`.log` 常缺；單跑 retry 即過，flake-prone 場景如 when_arcsin_sin_breaks 需多次）。**待 MiMo TTS 同意（計費閘門＝步驟 4）；未動任何外部 API。**

**§1.4 stage-1 完成（2026-06-14，使用者指示做 §1.4）：** 內容稿 [`content_scripts/ch01_one_sided_infinite.md`](content_scripts/ch01_one_sided_infinite.md)（deck id `ch01_one_sided_infinite`，16 單元＝14 教學＋intro/outro）於先前 session 依 HTML 權威檔 §1.4 從零撰寫，本 session 補齊 §1.2 已建立的兩道交付閘門——**對抗式稽核**＋**可讀 narration HTML**。撰稿涵蓋：三定義一命題全收（Def 1.10/1.11/1.12、Prop 1.5）、七例各帶不同模式全收（1.19 判準純邏輯／1.20 分段跳斷／1.21 無界增長／1.22 方向決定 $\infty$／1.23 找漸近線正例／1.24 零分母反例 `counterexample`／1.25 超越函數單邊漸近線）、五圖全覆蓋（Fig 1.13–1.17）；兩條主線（單邊→無限）以 u2 motivation 開場，repeat-pattern u8 接 u7、u14 接 u12。**六-lens 對抗式稽核**（faithfulness／decomposition／register／no-repeat／math-accuracy／completeness，Workflow `wnjdeyacd`）＋逐 finding refute-by-default 驗證：raw 1 → **六個內容維度全 clean（math 0 錯、無 L1、0 幻覺）**，唯一 confirmed＝缺 `_narration.html` 交付物（已補，14 段旁白逐字核對 14/14 一致、結構驗證通過；紀錄見內容稿 §7）。可讀審核稿 [`ch01_one_sided_infinite_narration.html`](content_scripts/ch01_one_sided_infinite_narration.html)（MathJax，比照 §1.3 `_narration.html`）。**待使用者認可旁白** → 認可後才進工程稿；§1.4 工程缺口＝漸近線虛線＋開/閉端點 jump plot（graph_focus plot-kind）為第二階段。**未動計費 API。**

**§1.4 stage-2 工程稿＋無聲成片（2026-06-14，使用者放寬閘門「先影片後旁白」）：** 使用者問「是否先做無聲影片版、拍板後再處理旁白」——釐清此產線旁白文字是 storyboard 骨幹（`say`＋`{show}`）、無聲 mock 即旁白驅動，且唯一計費步驟（TTS/MiMo）本就排最後；故**把「認可旁白才進工程稿」閘門放寬為「以已稽核乾淨的草稿旁白建 storyboard＋無聲影片、看片時連旁白一起審」**（改字成本極低、重渲 mock 免費）。
- **工程稿** [`storyboards/ch01_one_sided_infinite.yml`](storyboards/ch01_one_sided_infinite.yml)（16 場景）：u2 motivation／u4/u9/u11 定義／u5 example_walkthrough／u3/u6/u7/u12/u14 graph_focus／u8/u10/u13 graph_compare／u15 recap_cards。`say`＝草稿 narration 原文＋`{show}`；5 個 animation_cue（u3/u6/u7/u10/u12）標 `# HOOK(第二輪)` 待接入，本版靜態頂著。
- **§1.4 plot-kind 缺口已補：graph_focus 的 `y_clip`**（[`templates/graph_focus.py`](pipeline/templates/graph_focus.py)`._clipped_function_curve`）——標 `y_clip: true`/`[lo,hi]` 的 function 改「自取樣＋逐點 c2p、遇 non-finite/出界即斷段」路徑，解極點 ZeroDivisionError 當機＋跨漸近線假連接線＋±∞ 撐爆 bbox 三病；**預設不變**（`axes.plot`），§1.1/§1.6 零影響。`graph_compare` 共用 `gf._plot_blocks` 故一併受惠。跳斷用 hollow point＋`hollow_reason`。demo [`storyboards/_demo_asymptote.yml`](storyboards/_demo_asymptote.yml)（1/x²、2x/(x-3)、跳斷）三場景驗收過。
- **守門＋成片：** lint clean、sizecheck consistent（修 recap：4 point 含寬 inline-math 不 wrap 致字級不一→改窄 math＋縮 2 行；補 2 張 formula card 填空的 Remember 欄）。mock 全 16 場景 480p 成片、**逐場景抽幀 16/16 視覺驗收通過**（y_clip 八圖乾淨、跳斷開/閉端點正確、graph_compare ✓/✗ verdict 正確）。
- **踩坑：`media\Tex\` 快取競爭（Defender 鎖剛寫的 .dvi → PermissionError/dvisvgm 假錯）** 在 `--scene all`（`disable_caching` 每輪重渲）下隨機 1–9 場景失敗、retry 不穩收斂。**解法：所有 per-scene mp4 已各自渲妥（逐幀驗證），直接 ffmpeg concat 既有渲染繞過 render race**——完整無聲預覽 `output/ch01_one_sided_infinite_preview.mp4`（854×480、~10:56、16 場景）。
- **待使用者看無聲片** → 連旁白一起審（看片時改 narration 字＝改 `say`、重渲免費）→ 鎖定後旁白最後 polish → MiMo TTS（計費/外部，排最後、先報用量徵同意）。動畫第二輪（5 個 `# HOOK`）。**未動計費 API。**

**§1.5 stage-1 完成＋旁白認可（2026-06-14，使用者指示做 §1.5）：** 內容稿 [`content_scripts/ch01_limit_laws.md`](content_scripts/ch01_limit_laws.md)（deck id `ch01_limit_laws`，**19 單元＝17 教學＋intro/outro**）依 HTML 權威檔 §1.5 從零拆解、撰寫。**~75% 符號 → 套 §5 symbol-heavy 條件化視覺**：squeeze 幾何＝anchor（u13）＋其 in-action $x^2\sin(1/x)$ 包絡（u14）；floor 跳斷＝唯一對比視覺（u12，破壞「兩側一致」假設→DNE）；代數例題（u4/u6/u8/u9/u10/u17）與 squeeze 第二例（u15）一律不配圖、符號即 beat。涵蓋：2 定理（Th 1.2 極限律／Th 1.3 squeeze）＋1 命題（Prop 1.6 直接代入）＋11 例題各帶不同模式（1.26 抽象套律／1.27 直接代入／1.28 $\tfrac00$ 不定概念反例／1.29 factor／1.30 rationalise／1.31 combine／1.32 piecewise 一致／1.33 piecewise 相異 DNE／1.34 squeeze $x^2\sin$／**1.35 squeeze 第二例 $x\cos$（$|x|$ 變體，u15）**／1.36 存在性反推常數）＋Strategy 1.2（判斷型不拆分）＋3 圖全覆蓋。三招化簡 repeat-pattern（u9/u10 不重述 u8 setup）；u15 以「once more」承接 u14、只演 $|x|$ 變體。**六-lens 對抗式稽核**（faithfulness／decomposition／register／no-repeat／math-accuracy／completeness，Workflow `wf_546d3acb-9b5`，11 agents）＋逐 finding refute-by-default 驗證：5 raw → **0 blocking、0 L1、0 幻覺**；**math-accuracy 0 錯**（11 例題＋1.35＋定理/命題/strategy 全獨立重算一致）；3 條 raise 被 reject/refute（faithfulness 中文 meta 欄、decomposition forward-ref 範圍、no_repeat recap-vs-strategy 分層），2 條 confirmed advisory（u14 指回講義口語感／單元數 18-vs-19）。紀錄見內容稿 §7。**使用者 2026-06-14 認可旁白＋兩條 advisory 全採納：① Ex 1.35 由 u14 折疊句拆回獨立 u15 `squeeze_abs_value_bound`（演 $|x|$ 變體、強化「同手法、不同界」，18→19 單元）；② u15 末句採口語收尾「you can check it for yourself — it runs exactly the same way」。** .md＋[`ch01_limit_laws_narration.html`](content_scripts/ch01_limit_laws_narration.html)＋§7／audit record 同步重編號、回歸審核（拆分未引入新問題）。**旁白已認可 → 進工程稿**；§1.5 工程缺口＝floor 階梯／squeeze 三曲線包絡（$\pm x^2$＋$x^2\sin\frac1x$）／squeeze 示意圖（多半 `graph_focus`＋`reveal` 可吃）。**未動計費 API。**

**§1.5 stage-2 工程稿（2026-06-14，承 §1.4「先影片後旁白」放寬閘門＋使用者指示走 MiMo 路線）：** 工程稿 [`storyboards/ch01_limit_laws.yml`](storyboards/ch01_limit_laws.yml)（19 場景）依認可的 19 單元正典旁白模板化。模板對應：u2 motivation／u5 命題 `definition_math`；u3 極限律／u7 $\tfrac00$ 四分岔／u16 strategy 五步 `value_table`（reveal rows）；u4/u6/u11/u15/u17 `example_walkthrough`；u8/u9/u10 三招化簡 `derivation`（align_on `=`、結果行 highlight）；u12 floor／u13 squeeze anchor／u14 $x^2\sin$ 包絡 `graph_focus`；u18 `recap_cards`。`say`＝認可 narration 原文＋`{show}`；5 個 animation_cue（u2/u7/u12/u13/u14）標 `# HOOK(第二輪)` 待接入、本版靜態頂著。**守門員＋驗收：lint clean、sizecheck consistent**（修兩處：u16 5 步 `procedure_steps` 底溢→改 `value_table` 5 列；u18 recap 一點 shrink＋formula 過寬→四點縮短均一＋formula 改 quotient law）。**逐場景 mock render（480p）＋抽幀目視 15 場景全驗收**：三圖（squeeze 鉗合收於 $(a,L)$、$x^2\sin$ 被 $\pm x^2$ 包絡捏到原點、floor 跳階實心/空心端點）正確清晰；三表（極限律 gold quotient 列、$\tfrac00$ red DNE 列、strategy）無溢；三化簡鏈對齊乾淨；recap 四點均一＋quotient 卡。u13 anchor 微調：移除擠在交會點的 $(a,L)$ 標籤、改於 x 軸標 `$x=a$`。**踩坑：合併 mock 成片屢遭平行 session 的 §1.x manim/make 進程搶 `media\Tex` 快取打出 dvisvgm/PermissionError 假錯（README 已記「單跑即消失」）——逐場景已驗，合併 mp4 待無平行 manim 的乾淨窗口重渲（或由 MiMo render 直接產出）。** **下一步＝MiMo 旁白雙版路線**（步驟 0 前提 storyboard 已落地）：寫 `ch01_limit_laws.spoken.yml`（數學攤口語、`{show}` 對齊正典）→ `derive_spoken --check` → Mode B（codex）→ 收斂 →（報用量徵同意）MiMo TTS＋`make --reuse-audio`。**未動計費 API。**

**§1.1 review-loop（2026-06-13，看 mock 成片後）：** ①scene 4 mapping 箭頭 `\longmapsto`→`\longrightarrow`（↦ 尾豎線在此 setting 既怪又語義不符——student 非函數求值，plain 箭頭貼「對應」）；②`example_walkthrough` 的 ✓/✗（`mark`）語義一致化——只標**真正的判定／檢查**（one-to-one 測試、compose 驗證），移除推導／setup 步驟上的裝飾勾（first_inverses ×2、temperature_conversion ×1）；已寫進 [`DESIGN.md`](DESIGN.md) authoring checklist。

**產線新功能（2026-06-13）：場景間過渡＝compose 階段淡出黑場再淡入。** `make.py` 每個場景 av 在 mux 時加 `fade in/out`（`--transition`，預設每側 0.2s、太短的場景自動跳過），串接後每個邊界自然形成 ~0.4s 黑場過渡，全片開頭從黑淡入、結尾淡出到黑——呼應 intro/outro 暗場交接、消除硬切突兀。**全節自動套用**（§1.2+ 免費獲得）；`--transition 0` 回硬切。同步 [`README.md`](README.md)、[`DESIGN.md`](DESIGN.md) data flow。（fade ffmpeg 濾鏡已於既有 render 上驗證：t=0 幀全黑。）

**TTS 設定定案（2026-06-13）：固定 voice＝`Charon`、style＝「Read in a clear, calm calculus lecture voice. Keep the pacing steady. Read inline LaTeX in natural language.」** 寫進 [`tts.py`](pipeline/tts.py) `DEFAULT_VOICE`／`DEFAULT_STYLE`（全 deck 預設）＋ ch01_inverse_functions／ch01_precise_limit 的 `meta.voice`；README／DESIGN 範例同步（`_demo_*.yml` 佈局測試 deck 不動）。Charon 試聽（`one_to_one_definition`、3 beat、41.4s 真 TTS）已跑、使用者採納為固定預設。**Voice clone（`ReplicatedVoiceConfig`）暫緩**：SDK 支援（需 voice sample＋consent 錄音、24kHz 16-bit mono wav；屬預覽功能、可能未在金鑰開通），錄音指引留 `output/_voice/HOW_TO_RECORD.txt`，要做再接。金鑰存在 gitignored 的 `.env`（`GEMINI_API_KEY`）。

**Phase 1 進度（2026-06-13，使用者授權真 TTS）：** 目標 Gemini `gemini-3.1-flash-tts-preview`、Charon、60 beat（~10 min）。**踩大坑：首跑加了 `--reuse-existing`，但音訊路徑（`output/audio/<id>/beats`、`scenes`）早被多次 `make.py --backend mock` 寫滿靜音 WAV，於是 reuse 沿用 16 場景的靜音檔、幾乎沒真合成（首跑超快＝幾乎免費）——成片只有 `one_to_one_definition`（試聽時被真音覆蓋）有聲，volumedetect 證實其餘 −91dB 純靜音。** 教訓：**真 TTS 前先清 `beats/`+`scenes/`+`manifest.json`、且不要 `--reuse-existing`**（mock 與真音共用同一路徑）；未來可讓 `tts.py` 拒絕 reuse 來自 mock-backend manifest 的 WAV、或 mock／real 分目錄。已清空、重跑真 TTS（無 reuse，60 beat、854.7s 真 narration、全場景 volumedetect ~−20dB 證實有聲）＋真 timing 重渲＋重 mux **完成**。**narrated master：`output/ch01_inverse_functions.mp4`，2560×1440、887s（14'47"）、Charon 真旁白全程、含過渡與 4 動畫，待使用者 AV 審核。** 註：真旁白比 mock 字數估計長（854.7s vs 598.7s），故成片 14'47"＞先前 mock 10'20"；若嫌長可調 style 加速或精簡 narration。驗收紀律：mux 後一律 volumedetect＋逐場景解析度核對，不靠 exit code。**踩坑＋已修：真旁白成片走 `tts.py→build.py→mux.py`，但場景過渡 fade 原本只加在 `make.py` compose（mock 路徑）——已把同套 `_probe_duration`/`_fade_vf`＋`--transition` 補進 [`mux.py`](pipeline/mux.py)（標 `KEEP IN SYNC with make.py`）。** 兩 compose 路徑的 fade 邏輯重複＝小 tech-debt，未來可抽到 `pipeline/ffmpeg_util.py` 共用。`build.py --quality high`＝`production_quality`＝**1440p60**（非 1080p；build.py 無 1080p 檔位，與 make.py「high＝1080p30」不一致，可日後統一）。**narrated master 已產出**：`output/ch01_inverse_functions.mp4`，**2560×1440、631s（10'31"）、Charon AAC 立體聲音軌、含過渡與 4 動畫**，待 AV 審核（旁白＋語速＋動畫＋過渡一起看），認可後上 4K。**踩坑＋已修：`build.py`／`mux.py` 原以檔名排序挑 scene mp4（`sorted(...)[-1]`），_media 跨解析度子夾下會挑到 stale 低解析度——首次 mux 出 720p 混雜片（480p/720p/1080p/1440p 拼接）。改用 mtime 挑最新（比照 [`make.py`](make.py).render 早有的註記），`build.py` 兩處＋`mux.py` 一處皆修。** 抓到的方法：mux 後 ffprobe 串流／逐 scene 解析度核對（光看 exit 0 會漏）。

**各節新工程缺口（lazy build，到該節前才做）：** §1.2 reference-triangle 視覺（新模板或 hook）；§1.4 漸近線虛線＋開/閉端點 jump plot（graph_focus plot-kind）；§1.5 floor 階梯／squeeze 三曲線／$x^2\sin(1/x)$（多半 graph_focus 可吃）；§1.6 ε-δ tube 動畫已生成（待修＋hook 接入，task #6）。

**文件 staleness 修復（2026-06-13）：** 權威檔名 `chapter1-standalone.html`→`chapter1-print-standalone.html` 已同步 [`README.md`](README.md)、本檔、[`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md)、§1.1 content_script／storyboard（kit `README.md` 的 old→new 遷移表為刻意保留、不動）。

## 🔄 2026-06-10 輸入換源（HTML 講義）＋ §1.1 正式版啟動

**研究結論（流程體檢）：** gen-2 產線主體（make.py／lint／sizecheck／音訊驅動對齊／intro·outro 模板／Direction B／critic.py／narration 方法論）皆與輸入格式無關，**不需重建**；需要改的只有輸入契約層，已同步：[`README.md`](README.md)「輸入」、[`DESIGN.md`](DESIGN.md) data flow 首格、[`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md)（§1 忠實對象、§2 略過清單、§3 對應表換鍵成 kit 語意 class＋新增 `env-caution` 列、§6 `source` 欄格式、§8）。

**使用者拍板（2026-06-10）三項：**
1. **§1.1 從零重走全流程**——不繼承校準原型的 16 段已認可 narration；內容稿 v2 以 HTML 權威檔重新拆解、重寫、重新認可。連帶：`output/audio/ch01_inverse_functions/` 的舊真旁白 WAV 不可重用，真 TTS 屆時全節重新計費（先報價徵求）。
2. **本輪先靜態版成片，客製動畫第二輪接入**——先出模板靜態 mock 驗收格局，認可後再建正式 hook 機制（task #6）＋生成動畫。
3. **ch01 內容權威檔 = [`chapter1-print-standalone.html`](../handout/chapter1-print-standalone.html)**（2026-06-13 重組後檔名；原 `chapter1-standalone.html` 已不存，編輯源在 `fragments/ch01/sec-*.html`，影片產線讀組裝後的 standalone；非 example-ch01/ 片段；ch02+ 權威檔屆時另定）。

**現況事實核對：** ch01 HTML 與 `ch01_foundations.tex` 內容 verbatim 同源（抽查多處逐字一致；HTML 僅剝 `\index`、交叉引用改手寫編號）。§1.1 的 5 個動畫 hook code **未落檔**（repo 無檔、工程稿全標 `# HOOK(待補)`——下方舊待辦「已於先前 session 完成」實為 cue 層面，code 未進版控），第二輪需重新生成。

**§1.1 v2 進度（同日完成至 mock）：**
- ✅ 內容稿 v2（[`content_scripts/ch01_inverse_functions.md`](content_scripts/ch01_inverse_functions.md) 覆寫，沿用 deck id）：17 單元（v1 為 16；Remark 1.2 變數改名升格獨立單元，有偏離註記）、4 個 animation_cue（u2 兩進一出、u6 水平線 sweep、u12 往返、u13 翻摺）。**15 段 narration 已於 2026-06-10 經使用者認可。**
- ✅ 工程稿 v2（[`storyboards/ch01_inverse_functions.yml`](storyboards/ch01_inverse_functions.yml) 覆寫）：17 場景，say＝認可 narration 原文＋`{show}` 標記；4 處 `# HOOK(第二輪)` 註記動畫接入點；graph 場景座標沿用 v1 已調校資產（工程層經驗，非內容繼承）。
- ✅ 守門員＋mock 成片：lint clean、sizecheck consistent，480p mock 全 17 場景 compose 成功（`output/ch01_inverse_functions.mp4`，≈8'42"）。1080p 預覽版同日 render。
- ⚠️ 踩坑記錄：make.py 背景 render 時**不可並行**再跑 sizecheck/manim——兩程序搶 `media\Tex\` 快取，會互相打出 PermissionError／dvisvgm ValueError 假錯（單跑即消失）。
- ✅ **視覺批改第一輪（2026-06-10，Claude 親自當 critic）**：用 `critic.py --dry-run` 免費抽幀、Claude 直接讀幀（不送外部 VLM、零計費），依 DESIGN 五維提 7 findings，使用者全採納並已修复重渲複驗：①`definition_math` statement+math 改整組垂直置中（原錨點式佈局內容少時拉出大片死帶，影響 7 場景）②`recap_cards` bullet 間距改按實際 wrap 高度累進（原固定 pitch 1.2 三行條目擠壓黏連，sizecheck 盲區）③`example_walkthrough` takeaway 色改語意制（`takeaway_tone: warn|ok|neutral`，原固定 warning 紅把正面驗證染成錯誤色）④`heading_rich`／graph_focus `_title` 的標題 inline math 補乘 `TEX_TEXT_SCALE`（原縮水 ~25%）⑤`brand._wrap_prose_tex` 把 math span 後的標點黏回（原「$y$ .」「$x$ ,」浮標點）⑥模板 `kicker` 覆寫欄（motivation 場景不再掛 DEFINITION eyebrow）⑦場景 06/13 圖元修正（parabola 平頭、兩標籤撞線、`y=x` 標籤 label_role 改 muted——line label 預設 warning 是個坑、(a,b)/(b,a) 點補名）。
- ✅ **新模板 `derivation`（2026-06-11，使用者拍板「A+B+C＋立即實作」）**：全寬推導鏈模板，回應「左右並列模板塞不下長計算鏈」的前瞻問題（walkthrough 右欄實測 ~5.2u、3–4 步上限；ch02 導數定義鏈單行需 7–9u，sec-2-2 有 7 處 aligned 鏈——連續變形鏈是中後段主形態）。設計哲學：敘述進旁白、畫面全寬給數學。`=` 對齊欄（`align_on` 可換）、逐行 `{show line.N}`、highlight 結果行、statement 可選。demo 實測容量：statement＋4 分數行＋結果行超載 ~0.5（滿載鏈應把題目讓給旁白首拍）；無 statement 5 分數行 ✓、6 行混合 ✓。判準與容量寫進 [`DESIGN.md`](DESIGN.md)「Template selection」；demo 稿 [`storyboards/_demo_derivation.yml`](storyboards/_demo_derivation.yml)（ch02 真實鏈＋6 行壓測）留作範例。既有左右模板不動（離散短式步驟仍是它的地盤）。
- ✅ **模板缺口研究＋兩項落地（2026-06-11）：graph_focus 漸進揭示＋三模板列距修繕。** 研究結論（對照大一微積分全程的模板缺口盤點，詳見對話紀錄；建議按章節進度 lazy 建：§1.3 前 `value_table`、ch02 前 `graph_compare`＋tangent/secant kinds、§4.5 前 sign chart、積分章前 area/Riemann kinds）。本輪落地兩項：
  - **graph_focus `reveal: true`**：plot 預設仍 static（整圖第一幀亮），標 `reveal: true` 的 plot 改等 `{show plot.N}`——ε-帶→δ-帶的教學順序從此是旁白決策、不必寫 hook；revealed plot 的 label 併入同 block（一個 marker 圖元帶名字一起亮，也避免漏 `{show}` 的 label 拖到場景尾才冒出）。demo：[`storyboards/_demo_graph_reveal.yml`](storyboards/_demo_graph_reveal.yml)。
  - **列距語義「固定節奏為最小 pitch」**：`example_walkthrough`（1.25）/`procedure_steps`（1.4）/`theorem_proof`（0.95）原為純固定 pitch——recap_cards 2026-06-10 已付學費的黏連 bug 同類仍埋在三處。改為：相鄰列過高時 pitch 撐開保 ≥0.35 淨空；過高的首列／statement 對 title 保 0.2 淨空往下推（theorem 的 statement→label→steps→qed 全鏈 cascade）。**驗證**：red→green（壓測稿修前 5 條 overlap 28–64%、修後 0）；layout probe 證實 11 個已認可場景 10 個逐位元零漂移、僅 `procedure_in_action` 首列 −0.028u（其 inline-math 標題較高、原淨空 0.17<0.2，≈4px@1080p 不可察覺）；兩正式稿 sizecheck 與修前一致（§1.6 的 3 條 warn 為既有）。壓測稿 [`storyboards/_demo_tall_rows.yml`](storyboards/_demo_tall_rows.yml) 留作回歸樣本（revert 列距即重新報 overlap）。容量後果寫進 [`DESIGN.md`](DESIGN.md)「Template selection」：高內容吃列數，3–4 步容量以單行步驟為前提。
- ✅ **三個新靜態模板（2026-06-11，使用者拍板「靜態模板先做齊看效果」）：`value_table`／`graph_compare`／`sign_chart`。** 上一條研究盤點的 Tier 1/2 靜態缺口提前落地（原建議按章節 lazy 建；plot-kind 擴充 area/Riemann/tangent 與 hook 類仍照原計畫後做）：
  - **`value_table`**：通用表格，一個模板吃三型——數值逼近表（`reveal: cols` 逐欄、§1.3 節奏）、公式總表（`reveal: rows`、header 靜態）、性質對照表；`accent_col`/`accent_row` 標 punchline；cell 走 `$` 路由（math_line vs prose）不踩 garble。demo：[`storyboards/_demo_value_table.yml`](storyboards/_demo_value_table.yml)。
  - **`graph_compare`**：雙圖並排——panel 收 graph_focus 同款 plots payload（**全套機制重用**，含 `reveal: true`），caption＋`verdict: ok|bad`（✓/✗）、底部 annotations。§1.1 水平線測試的 hook 版面（~90 行手寫）從此是 payload。demo：[`storyboards/_demo_graph_compare.yml`](storyboards/_demo_graph_compare.yml)。
  - **`sign_chart`**：數線符號表（§4.5 單調性／curve sketching 的 workhorse）——等距 critical points（`excluded: true` 空心圈＝漸近線）、多列 marks 逐區間 `{show mark.R.I}`、`+`/`-` 自動著色 success/warning、tick 垂直導線。demo：[`storyboards/_demo_sign_chart.yml`](storyboards/_demo_sign_chart.yml)。
  - 三 demo lint clean＋sizecheck consistent＋mock 低畫質成片抽幀驗過；catalog 正式落地 [`DESIGN.md`](DESIGN.md)「Template catalog」（open question 已結案）。**待使用者看 demo 成片認可版面。**
- ✅ **第二輪動畫（2026-06-11）：正式 hook 機制＋4 客製動畫接入。** 機制（task #6 核心項）：場景級 `hook: "<module>:<fn>"` 欄→`_apply_hook`（`pipeline/templates/__init__.py`）；factory 拿模板 blocks 增刪改、**保留 reveal id**（storyboard `{show}` 與已認可 narration 全不動）；`Block.anim` 可為 callable `(scene, mob, ground)->秒數`（`blocks.py`），與音訊 beat 對齊無縫。模板 payload 留作無 hook fallback（刪 hook 行即回靜態版）。4 動畫（[`animations/ch01_inverse_functions_hooks.py`](animations/ch01_inverse_functions_hooks.py)）：u2 兩進一出映射、u6 雙圖（x³ vs x²）水平線同步 sweep＋紅綠判定、u12 A↔B 雙趟往返、u13 沿 y=x 翻摺生成 ∛x。逐場景 render＋抽幀（含動畫中途幀）驗過；修了 3 個首跑 bug（bbox 誤報重組 graph-layer block、y=x² 標籤穿軸、趟 2 反向弧端點建反）。**待使用者看片認可動畫（生成 code 視同 narration）。** task #6 其餘兩項（`reveal_targets()` 驗證、scene.py class-attribute 清理）仍待。
- ⬜ 下一步：使用者認可 4 段動畫 → 真旁白 TTS（計費，先報價）→ VLM critic 複核（計費）→ 4K 定版。§1.6 的 hook 接入可循同機制補做（舊獨立 scene 改 factory）。

**待辦（換源遺留）：** `review_pack.py` faithfulness lens parser 改吃 HTML（§1.1 v2 先人工對照，parser 後補）。

## ✅ 已完成

### 設計 brief 同步
- [`design_handoff/DESIGN_BRIEF.md`](design_handoff/DESIGN_BRIEF.md):從舊「Midnight Canvas（全暗）」同步成現行 **Direction B（雙 ground:暗底教學 / 淺底品牌）**,真實 tokens、8 模板對應、SummitBars/logo 規則。原標的兩個 token-vs-實作分歧(字體、格線)**已定案**——見下。

### 設計分歧定案(2026-06-02)
- ✅ **字體**:全 **Times New Roman / newtx**——body text 走 LaTeX `\text{}` (newtxtext) 以獲得正確 kerning；heading 走 Pango Times New Roman SEMIBOLD；mono Courier New；數學走 newtxmath。與 LaTeX 講義字體統一,刻意不採 tokens 的 sans 提案。
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

把 Code2Video P1 的「模型提案、人定奪」從**視覺層**延伸到**內容層**。新增 [`pipeline/review_pack.py`](pipeline/review_pack.py)——critic.py 的文字版姊妹，四 lens 對 content script / storyboard / `.tex` 做 cross-review（`.tex` 來源已換 HTML standalone，見頂部「2026-06-10 輸入換源」節；此 parser 待改 HTML）：

- **四 lens**：`faithfulness`（`.tex`↔narration 忠實度；忠實對象 2026-06-10 起已換 HTML standalone，見頂部換源節）、`register`（旁白口語化 §4）、`decomposition`（拆解 §3/§5）、`engineering`（生成 hook code 的數學保真＋慣例，需 `animations/<deck>_hooks.py`，§1.1 無 code 故自動跳過）。用法見 [`README.md`](README.md)「內容 cross-review」。
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

# KICKOFF — Remotion 製作流程檢討（2026-09-29 立檔，待開工）

> **裁決稿已產出（2026-09-29）：[`_audit/REVIEW-remotion-process-review-2026-09-29.html`](_audit/REVIEW-remotion-process-review-2026-09-29.html)，待使用者裁決。** 四題各附證據表、可選方案與勾選格，§5 文檔處置清單、§5.1／5.2 建議流程總圖在內。三個契約前提被證據推翻（Q7 稽核在付費 TTS **之前**、12 s 靜止非 Manim 特有、s31 非單一子代理），見其 §0。裁決後另開執行輪（§5 第 4 條）。
> **同日稍後使用者裁決：四題改由 A/B 對比回答**——A 繼承線（平移版原樣）與 B 重設線（從講義起、只沿用視覺素材、流程自訂）同做 §3.2，收線後交叉審再裁四題。契約＝[`KICKOFF-remotion-process-ab.md`](KICKOFF-remotion-process-ab.md)；§7 凍結清單延續到對比收線。

> **起因（使用者，2026-09-29）：** 「Remotion 我打算重新檢討一下整個製作流程……這些製作流程我記得是沿用 manim 的嗎？
> remotion 的路線應該可以考慮重新檢討一下。」主對話核對後確認：**現行寫給 Remotion 的流程，基本上是 Manim gen-2
> 的流程原樣平移**（§2 有逐項對照）。2026-09-28 的三個接線輪次（[`KICKOFF-remotion-unification.md`](KICKOFF-remotion-unification.md) §6）
> 都是照契約「接線」，沒有一輪被授權重新設計流程，所以它們忠實地把舊流程搬到新引擎上。
>
> **本輪只回答 §4 的四個問題並產出裁決稿；不做片、不改分鏡、不呼叫任何付費／外部 API。**
> 答案出來之前，§7 列的東西全部凍結（含 §3.2 Phase B 的 D1–D5、SPEC §6 的四項待裁決）——使用者已裁決「那些可以先不決定」。

---

## 0. 給新 session 的啟動提示（可整段貼）

```
你負責 NTU 微積分影片線（repo Calculus_handout，video/ 子樹）的「Remotion 製作流程檢討」輪。全程繁體中文溝通。
只寫檢討與裁決稿，不做片、不改分鏡、不呼叫付費／外部 API（Codex／agy 唯讀 review 也要逐次徵同意）。

開工前依序讀：
  video/KICKOFF-remotion-process-review.md   ← 本檔（四個問題＋證據去處＋交付物）
  video/KICKOFF-remotion-unification.md      ← 2026-09-28 Manim 封存的契約與收案（§2 邊界表、§5 收案、§6 後續）
  video/KICKOFF-process-reform.md            ← Manim §3.1 跑 21 輪的檢討（根因、輪次協定 G0–G7 的來歷）
  video/REVIEW_GATES.md                      ← 現行閘地圖（哪些標「已封存」、哪些標「沿用，待接 Remotion」）
  video/experiments/remotion_styles/README.md ← Remotion 原生做法的紀錄（三方向探索、s31 無指引生成、Q7）
  video/remotion/STYLE.md、s31/SCRIPT.md、q7/SCRIPT.md ← Remotion 實際怎麼做出片的
  video/KICKOFF-s32-remotion-phaseB.md       ← 平移版流程的具體樣子（本輪要裁定它的去留）

交付：§5 的裁決稿（standalone HTML）＋建議改寫／廢止的文檔清單。裁決是使用者的，你只攤開取捨。
```

---

## 1. 檢討的對象是什麼

「製作流程」＝從**定稿講義的一節**到**一支可發布的影片**之間的所有步驟、產物、閘與人閘。現在 repo 裡同時記載著**兩種**做法：

| | Manim 平移版（現行文檔寫的） | Remotion 原生版（實際做出片的） |
|---|---|---|
| 代表 | [`KICKOFF-s32-remotion-phaseB.md`](KICKOFF-s32-remotion-phaseB.md)、[`REVIEW_GATES.md`](REVIEW_GATES.md) §一／§六、[`RUNBOOK-mimo-narration-route.md`](RUNBOOK-mimo-narration-route.md) | [`experiments/remotion_styles/README.md`](experiments/remotion_styles/README.md)「無指引生成實驗」、[`remotion/s31/SCRIPT.md`](remotion/s31/SCRIPT.md)、[`remotion/q7/SCRIPT.md`](remotion/q7/SCRIPT.md) |
| 形狀 | Stage-1 內容稿 → sign-off → 口語版 derive → NFA → TTS → **內容鎖 G0** → 從 Manim 分鏡的 beat 切分派生 `s32.yml` → 分幕派工 → 一輪＝一 merge 一 render 一審 → REWATCH 六鏡里程碑 → final | 主對話從講義提煉 [`OUTLINE-s31.md`](experiments/remotion_styles/OUTLINE-s31.md)（只列要教的內容）→ **一個 motion-designer 子代理**在不讀舊稿的隔離下寫出整節（旁白＋畫面＋TSX）→ 自審迴圈 → MiMo `--unit scene` 配音 → render → 使用者看片 → 事後找 Codex 做一次 NFA 式稽核（Q7：5 條措辭修正） |
| 實績 | Manim §3.1：**21 輪**才收斂（[`KICKOFF-process-reform.md`](KICKOFF-process-reform.md)）；§3.2 Phase A：7 輪稽核、約 167.5k 外部 token，音檔還在清 worktree 時遺失 | Remotion §3.1（約 8 分）：一個子代理一天；Q7 英文版 5:42＋中文版 9:09 兩天做完含審核修正 |
| 使用者當時的裁決 | 2026-09-13：「先用 §3.2 串行把流程走一遍變成熟，再並行」 | 2026-09-25：「這一輪不跑任何稽核閘……定為模板、進正式產線前再補回閘序」 |

第二列的「補回閘序」從來沒有人做過裁決：**補回哪些、以什麼形式、哪些 Remotion 根本不需要**。這一輪就是做這件事。

## 2. 現況盤點：哪些是平移、哪些是原生

| 層 | 現行 Remotion 線用的 | 來源 | 綁 Manim 的程度 |
|---|---|---|---|
| 內容層 | Stage-1 內容稿（[`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md)）、`[source:]`、`visual_need`／`animation_cue`／`screen_contract`、sign-off、NFA、`source_rev` stamp | Manim gen-2 | 與渲染器無關；但 `animation_cue`／`screen_contract` 的格式是為 Manim 模板與 hook 設計的 |
| 口語雙軌 | `<deck>.spoken.yml` → [`derive_spoken.py`](pipeline/derive_spoken.py) → `<deck>_mimo.yml` 與閱讀版 | Manim gen-2 | 派生的對象是 Manim 正典分鏡；Remotion 三支現行分鏡都**直接寫口語**、沒有雙軌（[`SPEC-remotion-storyboard-schema.md`](SPEC-remotion-storyboard-schema.md) §6 第 4 項） |
| 分鏡格式 | `say` 加 `{show <id>}` 切 beat 的 yml | Manim 的 Block reveal 模型 | Remotion 只因 `tts.py` 吃這格式而沿用；Remotion 自己的對時是 [`words.ts`](remotion/src/lib/words.ts) 的 `atWord()` 逐字卡點，比 beat 更細 |
| 配音與對時 | scene-level MiMo TTS＋stable-ts 逐字對齊、fallback ladder | Manim 時代開發 | 與渲染器無關；Remotion 用得比 Manim 順 |
| 閘序 | REVIEW_GATES 七層（現六份 rubric：six-lens／copyedit／NFA／VISUAL-FRAME／pedagogy-firstlearner／amplification）、REWATCH 多鏡、12 秒最長靜止硬閘（[`rewatch_pack.py --gate-still`](pipeline/rewatch_pack.py)）、輪次協定 G0–G7、Phase A／B 內容鎖 | 全部是 Manim §3.1 的病長出來的 | VISUAL-FRAME 的 V1–V10 對著 Manim 幀寫；12 秒靜止是 Manim 模板靜態場的病；hook-engineering 已封存；G0–G7 是為「一次 render 要 40 分鐘、改一處要重跑全片」設計的批次紀律 |
| 畫面語法 | [`SPEC-motion-language.md`](SPEC-motion-language.md) 五條規則 | 參考影片逐幀拆解（2026-09-13） | 規則本身與引擎無關；實作契約層（motion primitive）已封存 |
| 今天新接的 | [`check_storyboard.py`](pipeline/check_storyboard.py)（結構閘＋內容層檢查器入口）、`doctor --smoke`、Phase B 開工檔、REVIEW_GATES 的「沿用，待接 Remotion」標記 | 2026-09-28 平移 | 忠實搬運，warn-only，沒有人裁決過該不該存在 |
| Remotion 原生 | 三方向風格探索→`paper`、[`STYLE.md`](remotion/STYLE.md)（token／元件／鏡頭紀律／圖上標籤 render 期硬閘 `kit.tsx`）、[`motion-designer`](../.claude/agents/motion-designer.md) 子代理＋自審迴圈、無指引生成整節、mock 150 wpm 時序、局部重渲、i18n 雙語、`loudnorm.py`、章節點嵌入 | 2026-09-25～26 | 只在 Remotion 存在；**沒有任何文檔把它寫成流程** |

## 3. 為什麼現在要檢討，而不是先做 §3.2 再說

- 平移版把 Manim 的成本結構當前提：一輪 2–3 小時牆鐘、render 不可局部、模板容量是硬牆。Remotion 局部重渲一段一分多鐘（[`q7/SCRIPT.md`](remotion/q7/SCRIPT.md)「局部重渲」）、沒有模板容量、畫面由 code 直接畫；G5 批次化與 G3 停止條件要防的浪費在 Remotion 上可能根本不存在，或以完全不同的形式存在。
- 平移版要求 §3.2 從 Manim 分鏡的 beat 切分派生（[`KICKOFF-s32-remotion-phaseB.md`](KICKOFF-s32-remotion-phaseB.md) §3.1），等於把 Manim 的 reveal 粒度帶進 Remotion；而 Remotion §3.1 是從 OUTLINE 重寫旁白做出來的，使用者看了滿意。**兩者對「旁白是誰的」答案相反**（D2）。
- 原生版沒有任何內容層閘，Q7 的數學正確性靠事後一次 Codex 稽核。若 Remotion 要做正式課程節（不是解題片），內容忠實與教學覆蓋還是要有人擋，但不必是 Manim 那七層。
- 不先裁決，§3.2 會照平移版跑，D1–D5 的每一項都在為平移版服務；做完再改流程，等於再付一次 §3.1 的 21 輪學費。

## 4. 四個問題（本輪要回答的全部）

每題寫明**要回答什麼**、**證據去哪找**、**答案的形式**。四題答完，§7 凍結的每一件都會有處置。

### Q1 Manim 時代的閘序裡，哪些是在防 Manim 特有的病，Remotion 已經不需要

- 要回答：逐閘判定「病因是否隨引擎消失」。候選：12 秒最長靜止硬閘、VISUAL-FRAME V1–V10 裡針對 Tex 渲染／模板擠壓／`accent` 語意色的條目、hook-engineering（已封存）、sizecheck／capacity（已封存）、`[sync]` render 長度對音檔長度（Remotion 由 manifest 決定場長，結構上不會漂）、G5「一輪一 render」的批次紀律。
- 證據：[`KICKOFF-process-reform.md`](KICKOFF-process-reform.md) §0–§2 每輪的病因；[`REVIEW_GATES.md`](REVIEW_GATES.md) §一各閘的「為何存在」欄；[`legacy/manim_video/KICKOFF-pipeline-hardening.md`](../legacy/manim_video/KICKOFF-pipeline-hardening.md) 的 T 清單（每個 T 對應一個 Manim 病）；Remotion 端的對照＝[`remotion/STYLE.md`](remotion/STYLE.md) 已內建的 render 期硬閘（標籤間距、場序比對、字型載入驗證）。
- 答案形式：一張表，每閘一列：病因｜Manim 特有？｜Remotion 是否已有結構性保證｜處置（廢止／保留／改形）。

### Q2 哪些是在防與渲染器無關的病，該保留但可以換更輕的形式

- 要回答：旁白不忠實（NFA）、教學漏步（pedagogy PD／SC）、出處斷鏈（provenance／source_rev）、例題被默默丟掉（example coverage）、去 AI 味（copyedit／six-lens）、放大機會（amplification）——各自在 Remotion 上的**最輕可行形式**是什麼：是 render 前的確定性檢查（`check_storyboard.py` 那種）、是 gate-1 subagent 讀分鏡、還是看片後一次 Codex／agy 稽核（Q7 模式）。
- 證據：六份 rubric 各自的「blocking 定義」；§3.2 Phase A 的 7 輪稽核到底抓到什麼（[`content_scripts/_audit/REVIEW-ch03_chain_rule-s32-phaseA-applied.html`](content_scripts/_audit/REVIEW-ch03_chain_rule-s32-phaseA-applied.html)、gate-2 抓到 gate-1 放過的 D2 blocking 那件事）；Q7 的 Codex 稽核 5 條是什麼等級（`git log --grep=NFA`，commit `a1caa63`）。
- 答案形式：每個病一列：Remotion 上的形式｜什麼時候跑（寫分鏡前／render 前／看片後）｜誰跑（確定性腳本／subagent／外部鏡）｜blocking 還是 advisory。

### Q3 Remotion 的 §3.1 與 Q7 那種一次做完的做法，品質靠什麼撐住，正式化時缺什麼

- 要回答：拆解原生版的隱性品質機制——motion-designer 的自審迴圈、`STYLE.md` 的 render 期硬閘、mock 時序先看版型、使用者看片人閘、事後 Codex 稽核——哪些是可複製的流程、哪些只是那兩支片碰巧順利。正式化（做成課程節、可並行多節）時缺什麼：內容忠實的前置擋（不是事後）、覆蓋度、多節一致的視覺語彙、成本帳、換機重現。
- 證據：[`experiments/remotion_styles/README.md`](experiments/remotion_styles/README.md) 各片的紀錄（呼叫數、重試、時長、Codex 修正）；[`remotion/s31/SCRIPT.md`](remotion/s31/SCRIPT.md) 與 [`remotion/q7/SCRIPT.md`](remotion/q7/SCRIPT.md) 的做法段；[`motion-designer.md`](../.claude/agents/motion-designer.md) 的自審條款；`REBUILD_STATUS.md` 對 Q7 的驗收數字（12 秒停格門檻兩處待裁決）。
- 答案形式：原生流程的「步驟表」（第一次把它寫成流程），每步標「已有／缺／碰巧」。

### Q4 內容稿到分鏡的路徑要不要保留 `{show}` beat 切分，還是改成 Remotion 自己的場景腳本加 `atWord()` 對時

- 要回答：`{show <id>}` 在 Remotion 上剩下什麼功能（TTS 的 beat 切分、fallback ladder 的單位、字幕 cue、pedagogy 閘的 reveal 順序）；`atWord()` 逐字卡點能否取代 beat 當「畫面與旁白的契約」；口語雙軌（`spoken.yml`／`derive_spoken`）要不要留；Stage-1 內容稿的 `animation_cue`／`screen_contract` 對 Remotion 場景腳本（`SCRIPT.md` 逐場逐拍表）是不是重複。
- 證據：[`DESIGN.md`](DESIGN.md)「旁白 `say` 文法與 beat 契約」與「Manifest schema 2」；[`words.ts`](remotion/src/lib/words.ts)；[`SPEC-remotion-storyboard-schema.md`](SPEC-remotion-storyboard-schema.md) §3–§4；`tts.py --unit scene` 對 `{show}` 的實際用法（`grep -n "show" video/pipeline/tts.py`）；§3.2 Phase A 的 `ch03_chain_rule_mimo.yml`（[`legacy/manim_video/storyboards/`](../legacy/manim_video/storyboards/)）與 Remotion `s31.yml` 的並排對照。
- 答案形式：一條「內容稿 → 分鏡 → 配音 → 畫面」的資料流圖（Remotion 版），標出每個產物的唯一源與誰消費它；被判多餘的產物列廢止。

## 5. 交付物與驗收

1. **裁決稿**：standalone HTML（依根 `CLAUDE.md`「給使用者審核的交付物要用打開就能讀的形式」；繁中框架、引文與識別碼原文），放 `video/_audit/REVIEW-remotion-process-review-<日期>.html`，內容＝§4 四題的答案表＋**每題的取捨攤開**（不默默選；Karpathy §1）＋一張「建議的 Remotion 正式流程」總圖。使用者在裁決稿上勾選。
2. **文檔處置清單**：裁決後哪些檔改寫、哪些廢止、哪些搬 legacy——至少要對下列每一件給處置：[`KICKOFF-s32-remotion-phaseB.md`](KICKOFF-s32-remotion-phaseB.md)（含 D1–D5）、[`SPEC-remotion-storyboard-schema.md`](SPEC-remotion-storyboard-schema.md) §6 四項、[`check_storyboard.py`](pipeline/check_storyboard.py)＋`doctor --smoke`、[`REVIEW_GATES.md`](REVIEW_GATES.md) 六份 rubric 與 §六 G0–G7、[`RUNBOOK-mimo-narration-route.md`](RUNBOOK-mimo-narration-route.md)、[`derive_spoken.py`](pipeline/derive_spoken.py) 與 `spoken.yml` 雙軌、[`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md) 的 `animation_cue`／`screen_contract`、[`SPEC-motion-language.md`](SPEC-motion-language.md)。
3. **驗收**：裁決稿每個結論都能指到 §4 列的證據（路徑＋行號或 commit）；沒有一題用「沿用既有做法」帶過；四題各至少列出兩個可選方案與代價；`python tools/doc_lint.py` clean。
4. 使用者裁決後**另開執行輪**改文檔與工具；本輪不動任何 `.py`／`.yml`／`.tsx`。

## 6. 邊界（本輪不做）

- 不做片、不改三支現行分鏡、不呼叫付費 TTS／VLM；Codex／agy 唯讀 review 要逐次徵同意（若要拉異家族第二讀者審這份檢討，先報量）。
- 不重開 2026-09-25 已定的視覺方向（`paper` 紙本編輯排版）與品牌 logo 唯一固定元素的前提。
- 不碰講義線。

## 7. 本輪結束前凍結的東西

| 凍結項 | 現況 | 解凍條件 |
|---|---|---|
| §3.2 Phase B 開工（含 D1–D5） | [`KICKOFF-s32-remotion-phaseB.md`](KICKOFF-s32-remotion-phaseB.md) 是平移版流程的產物 | Q1–Q4 裁決後改寫或廢止 |
| SPEC §6 四項待裁決 | [`SPEC-remotion-storyboard-schema.md`](SPEC-remotion-storyboard-schema.md) | Q4 決定分鏡格式後一併定 |
| `check_storyboard.py`／`doctor --smoke` | warn-only，留著無害 | Q2 決定內容層閘的形式後改寫或廢止 |
| REVIEW_GATES 的「沿用，待接 Remotion」標記 | 標記而已，沒有實作 | Q1／Q2 |
| §3.2 Phase A 遺失音檔的處置（D1） | 主 checkout 的 `output/ch03/s3.2/audio` 是 mock | Q4 決定旁白是誰的之後才知道要不要重配 |

## 8. 相關紀錄

- Manim 封存契約與收案：[`KICKOFF-remotion-unification.md`](KICKOFF-remotion-unification.md)（§6 第 5 條＝本輪）。
- Manim §3.1 的流程檢討（本輪的前身，結論 G0–G7 落在 REVIEW_GATES §六）：[`KICKOFF-process-reform.md`](KICKOFF-process-reform.md)。
- 歷史輪次全文：[`_archive/REBUILD_LOG-2026-05-to-07.md`](_archive/REBUILD_LOG-2026-05-to-07.md)；Manim 時代設計全文：[`legacy/manim_video/DESIGN.md`](../legacy/manim_video/DESIGN.md)。

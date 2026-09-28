# 影片產線——資料流與旁白契約（Remotion 時代）

> **定位（2026-09-28 立檔）：** 2026-09-28 使用者拍板「以後影片都走 Remotion」，Manim gen-2 引擎整包封存到
> [`../legacy/manim_video/`](../legacy/manim_video/)（契約與逐檔清單＝[`KICKOFF-remotion-unification.md`](KICKOFF-remotion-unification.md)；
> 回退錨點＝tag `archive/2026-09-28-manim-gen2-final`）。原本 183 KB 的 `DESIGN.md` 整份搬到
> [`../legacy/manim_video/DESIGN.md`](../legacy/manim_video/DESIGN.md)；本檔是**精簡新版**，只承接與渲染器無關的四塊：
> **資料流**、**旁白 `say`／`{show}` beat 文法與 TTS manifest 的時序契約**、**配音工作流設計**、**語意色軸的講義對照**。
>
> **不在本檔：** 畫面契約（token、字型、版面、動態語彙）在 [`remotion/STYLE.md`](remotion/STYLE.md)；
> 各片的分鏡與重現指令在 `remotion/<片>/SCRIPT.md`（例：[`q7/SCRIPT.md`](remotion/q7/SCRIPT.md)）；
> 現役製作處的導覽在 [`experiments/remotion_styles/README.md`](experiments/remotion_styles/README.md)。Manim 時代的模板 payload、`accent`／`scene_role`、
> Lectern 版面、容量契約、motion primitive 等**一律不承接**，要查去 legacy 那份。
>
> 每節開頭一行註明它承自舊檔的哪一節；承接時已把只屬 Manim 引擎（`make.py`／`scene.py`／`schema.py`／`critic.py`）的敘述拿掉或改寫成歷史註記。

---

## 資料流（目標）

> 承自 `legacy/manim_video/DESIGN.md` §〈Data flow（目標）〉。

```
handout/latex/src/chNN/chapterN.tex   （定稿講義的一節；閱讀版＝dist/chNN/chapterN.pdf）
   │  （作者閱讀該節，手寫內容稿——非自動生成）
   ▼
video/content_scripts/<deck>.md       Stage-1 內容稿（方法論＝CONTENT_METHODOLOGY.md；內容層閘見 REVIEW_GATES.md）
   │  （作者依內容稿寫分鏡；旁白直接寫口語，見下方「旁白 `say` 文法」）
   ▼
Remotion 分鏡 <id>.yml                 tts.py 格式：meta＋scenes[]；content 場的 `say` 以 {show <id>} 切 beat
   │                                   （現行位置：remotion/<片>/<片>.yml）
   ▼
pipeline/tts.py                       每 scene（--unit scene＋forced alignment）或每 beat 合成；       (DONE)
   │                                   mock＝靜音、不計費；mimo 等真 backend＝外部 API，逐次徵同意
   │                                   → public/audio/<批次>/manifest.json＋WAV（manifest schema 2）
   ▼
Remotion composition                  timing.ts 讀 manifest（§3.1／Q7＝src/s31/timing.ts 的 buildShow）：(DONE)
   │                                   場長＝LEAD＋旁白秒數＋TAIL；beat 起點＝LEAD＋start_seconds，
   │                                   以 {show} id 查拍；src/lib/words.ts 的 atWord() 對到逐字時間
   ▼
npx remotion render                   → out/<片>_raw.mp4（1920×1080、30 fps）                           (DONE)
   ▼
scripts/loudnorm.py                   兩段式 loudnorm 到 house −19 LUFS／TP −1.5 dBTP                   (DONE)
   │                                   （實作＝pipeline/loudnorm.py，自封存的 make.py 抽出）
   ▼
out/<片>_final.mp4                    （選用）scripts/chapters.py 產章節點並嵌入 mp4
```

**沒有單一 orchestrator。** Manim 時代的 `make.py`（parse → synth → render → compose 一條指令）已隨引擎封存；Remotion 線目前是
「`tts.py` → `remotion render` → `loudnorm.py`」三步手動串，每支片的確切指令寫在它的 `SCRIPT.md`（mock 版與真配音版各一段）。
**換 manifest 就整片重新對時**：mock（依字數估的靜音）與真配音的 manifest 形狀相同，Remotion 只換 `--props` 裡的 manifest 路徑。

**已建（2026-09-28）：** Remotion 分鏡 yml 的 schema＝[`SPEC-remotion-storyboard-schema.md`](SPEC-remotion-storyboard-schema.md)（SSOT），render 前的結構閘＋內容層確定性檢查器
（`provenance`／`source_rev`／`pedagogy`／`step_coverage`／`example_coverage`）的入口＝[`pipeline/check_storyboard.py`](pipeline/check_storyboard.py)
（`python video/pipeline/check_storyboard.py <片>.yml`；`tools/doctor.py --smoke` 對 `remotion/*/*.yml` 全跑）。Manim 時代的 `schema.py`／`lint.py`／`sizecheck.py` 仍封存。`paper/` 升格為正式目錄 `remotion/` 亦於 2026-09-28 完成。
**尚未建（TODO，另開輪次；見 KICKOFF-remotion-unification §6）：** render 前的 manifest freshness 檢查（Manim 時代由 `make.py --reuse-audio` 做，Remotion 端目前沒有）。

### Alignment：音訊長度就是畫面長度

> 承自 `legacy/manim_video/DESIGN.md` §〈Alignment，重述（避免在重寫中遺失）〉。

第一代的洞見沿用：alignment **不依賴** TTS 回傳 word-level timestamp。每個 beat（或每個 scene）合成一段音訊、**量它的真實長度**，
那個長度**就是**畫面停留的長度。換 synthesizer 不換 alignment model（mock → MiMo 只是換了把尺）。scene-level 合成時，
beat 的起訖由 `stable-ts` transcript-constrained forced alignment 回推（見下方「Manifest schema 2」）。

**時序常數屬於渲染端。** Remotion 的 LEAD／TAIL／OVER（場間疊接）是 composition 自己的常數（§3.1 與 Q7 共用
`src/s31/timing.ts`：30 fps 下 LEAD 15、TAIL 27、OVER 22 幀；Q7 另有每場 `HOLD` 加停留）。`pipeline/timing.py` 的
`SCENE_LEAD_SECONDS`／`SCENE_TAIL_SECONDS` 是 Manim player 與 compose 的常數，仍留在 `pipeline/` 供 `rewatch_pack.py` 等工具使用；
兩邊要不要統一由之後的輪次決定。

### MiMo 口語軌（single-source）＋非決定性

> 承自 `legacy/manim_video/DESIGN.md` §〈MiMo 口語軌（single-source）＋非決定性（2026-06-14）〉。

MiMo（`mimo-v2.5-tts`）**不讀 inline LaTeX**，旁白必須「把數學攤成口語」。Manim 時代的做法是雙軌 single-source：正典 storyboard 的 `say`
內嵌 LaTeX，口語版的唯一源是 `content_scripts/<deck>.spoken.yml`，由 `pipeline/derive_spoken.py` 生成 `storyboards/<deck>_mimo.yml`
與閱讀視圖 `content_scripts/<deck>_narration_spoken.md`，`--check` 守 parity（scene／`{show}` 結構一致、口語無 `$`）。
**2026-09-28 起：** `derive_spoken.py` 留在 `pipeline/`，但它讀的正典 storyboard 已隨 Manim 封存到 `legacy/manim_video/storyboards/`；
Remotion 線現行做法是**分鏡 yml 直接寫口語**（見 `remotion/q7/q7.yml` 檔頭：「Spoken English only (no LaTeX: MiMo reads the text literally)」）。
Remotion 線要不要恢復「正典＋口語」雙軌，隨分鏡 schema 一起定。

**MiMo 非決定性：** 同文字重合成＝不同 take、長度約 ±10%，影片長度不可重現；**要定版就別重合成**。
**NFA（旁白忠實稽核，原 video「Mode B」）** 稽核口語版對核准源的忠實度，契約見 SSOT
[`content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md`](content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md)。

### TTS 資料契約與旗標

> 承自 `legacy/manim_video/DESIGN.md` §〈產線硬化：新增資料契約與旗標（2026-07-11）〉的 TTS 部分（`make.py` 的旗標、sidecar、場間轉場不承接）。

- **`meta.derived_from`（生成分鏡的 freshness stamp）：** `derive_spoken.py` 產 `<deck>_mimo.yml` 時把兩個輸入的 **LF-正規化 sha256**
  蓋進 `meta.derived_from.inputs`；`tts.py` 開跑前 preflight 驗章，不符即 `[freshness]` abort。治「正典改了、生成檔沒重 derive 就合成」的漂移。
- **manifest `receipt`（計費收據）：** `{backend_calls, backend_retries, modes{scene_aligned/beats/silent}, fallback_scenes}`，反映本次執行。
- **manifest `scenes[].validation.qa`（ASR QA 三態）：** `{status: ran|skipped|error, …}`。只有 `--skip-qa` 靜默；其餘「該跑沒跑」印 WARN「NOT a pass」。
- **`tts.py` 旗標：** `--backend`（**必填**，無預設，防裸跑誤燒／誤蓋）、`--force-backend-switch`（僅 `--scene all`）、`--force-clobber`（覆寫損壞／孤兒音檔）。
- **計費更正（B8）：** fallback ladder 的 `beats` terminal **不受 rungs 2–3 的 `RetryBudget` 限制（budget-exempt）**，但 MiMo 下**每個非空 beat
  仍是一次 backend call**（不是免費）；dry-run 的 worst-case 欄已計入。（`arbiter`＝`small.en` 本地重對位，確實免費、無 API。）

### Manifest schema 2：scene-level TTS＋forced alignment

> 承自 `legacy/manim_video/DESIGN.md` §〈Manifest schema 2：scene-level TTS＋forced alignment（2026-07-05）〉。

設計權威＝`experiments/forced_alignment_dean/REVIEW-scene-tts-production-design.html`。核心：TTS 合成單位可由 beat 升到 content scene，一個 scene
一次合成、用 `stable-ts` transcript-constrained forced alignment 回推每 beat 時序；per-scene validation 決定該 scene 走 scene-level 或回退 beat-level，
**永遠有可出片的路**。

- **頂層 `"schema": 2`。** 無 `schema` 欄位的舊 manifest 視為 schema 1（全 beats），照舊可用，不需遷移；消費端對 `schema>2` 應明確報錯、拒絕靜默誤讀
  （前例＝已封存 `make.py` 的 `_check_manifest_schema`；Remotion 的 `buildShow` 目前沒做這項檢查）。
- **`narration_mode` 三值：** `"silent"`（intro／outro／divider）｜`"beats"`（每 beat 一 WAV）｜`"scene_aligned"`（一場一 WAV）。同一 manifest 允許混用（per-scene 決定）。
- **`scene_aligned` 條目與 `beats` 模式共用 `beats[]` 形狀**（`index`／`id`／`reveal`／`text`／`text_hash`／`audio_seconds`／`start_seconds`／`end_seconds`），
  另加 per-beat `word_start`／`word_end`／`boundary{prob,interpolated}`，以及 scene 級 `audio_file`（唯一音檔，無 per-beat WAV）、`scene_text_hash`、
  `alignment{words_file,aligned_file,aligner{tool,version,model,…},chunks}`、`validation{status,warnings,metrics}`（`status ∈ {pass, pass_with_warnings}`；
  fail 即回退，不會落進 manifest）、`fallback_history[]`。
- **兩層獨立 freshness（scene-level 紅利）：** 文字改＝重合成（計費）＋重對位；reveal／beat 數改（文字沒改）＝沿用 WAV、只重跑映射＋驗證（免費）；
  aligner 換 model／調參＝沿用 WAV、只重對位（免費）；backend／model／voice／style 改＝重合成。判定依 `scene_text_hash`＋per-beat `text_hash`＋
  top-level 四欄＋WAV 實際時長。aligner freshness 是 `tts.py` 的職責，渲染端不檢查 aligner model。
- **原子寫入＋verify-before-overwrite：** words／aligned／manifest 一律 `.tmp`＋rename（`pipeline/atomicio.py`）；scene WAV 先寫 temp、gates 過才 promote 到正檔，
  杜絕「舊 words.json 配新 WAV」與「壞 re-synth 蓋掉好 WAV」。
- **reuse 以內容定址、不以輸出路徑定址（2026-09-13 修）：** beat 級 reuse index 的 key＝`(scene_id, beat text_hash, 同場同 hash 的第幾個)`＋頂層
  backend／model／voice／style（`build_reuse_index`）；scene 級以 `scene_id` 為 key（`build_scene_reuse_index`），另把 `alignment` 的
  `words_file`／`aligned_file` 一併帶進 index。理由：兩層的輸出路徑都把場序嵌進檔名，「搬場」或「加／移一個 `{show}` marker」會讓路徑全部位移、
  導致整場重合成。修法：beat 命中後若新舊路徑不同就把 WAV **搬**到新路徑再登記；scene 層在 freshness 檢查**之前**用
  `adopt_prior_scene_artifacts` 把舊 scene WAV＋兩個 sidecar 搬到今天的號（無條件搬：re-synth 走 temp＋gates 過才 promote）。兩層共用同一個
  `_relocate`（copy→驗大小→刪舊→空目錄剪掉；log `reused … (moved from …)`）。
- **交易與計費安全（code review 2026-09-23 A-01～A-04；⑸⑹＝RG1-01）：** ⑴ 一整場 beats 是一筆交易——所有 take 先放進 `.staging/`，全部備妥才
  promote，不會覆寫還沒被自己 owner 取用的舊 take。⑵ `main()` 每完成一場就寫一次 checkpoint manifest，被搬走的來源要等 checkpoint 記下新位置才刪；
  中止（`--max-billed-calls`、斷網）後重試不會對已完成的場重複計費。⑶ 待合成的場裡只要有 scene unit，`main()` 在任何合成呼叫之前就先檢查 `stable-ts`；
  缺件直接中止。⑷ scene-level reuse 命中但重新對位失敗時，付費重新合成前先免費用 `small.en` 對同一份 WAV 重跑一次對位。⑸ **失敗留下的 staged take：**
  beats 場在全部 promote 完成之前失敗，`.staging/` 會保留 `<beat>.wav.staged`——已付費、不在 manifest 裡、可能是僅存的一份；刻意不用 `.wav` 結尾，
  免得絆到 `overwrite_guard`。免費取回＝把 staged 檔複製到「磁碟上 manifest 為這句話記錄的 `audio_file` 路徑」再跑 `--reuse-existing`；**不要**照字面
  去掉 `.staged` 放回 beat 資料夾（詳細步驟與 2026-09-23 離線實測數字見 legacy 那份原文）。⑹ **beat reuse 另驗 take 時長：** WAV 實測時長與 manifest
  記錄的 `audio_seconds` 相差不超過 `BEAT_TAKE_TOLERANCE_SECONDS`（1 ms）才 reuse，不符就印 `prior WAV content changed` 並重新合成（計費）。
  `--dry-run` 的 `plan` 走同一個判斷。
- **`scene_number` 由當前分鏡全 deck 序號重算（`renumber_scenes`，manifest 寫出前）：** intro／divider 也佔號（與 `rewatch_pack.py` 同一套數法），
  換號者的 scene WAV／`alignment` sidecar／beat WAV 一併搬到新號；scene_id 進每個檔名，重新編號永遠不會讓兩場撞到同一路徑。
- **`--dry-run` 把 reuse 算進 `plan`：** 多一個 `reuse` 欄，TOTAL 行另印 `(no-reuse: N)` 保留悲觀報價；`plan` 只有真的下了 `--reuse-existing` 才成立。
  `worst` 對 scene-level 仍 reuse-blind。
- **模組：** 核心 `pipeline/scene_align.py`（單一 aligner seam `align_scene`）；fallback ladder `pipeline/scene_fallback.py`；
  `tts.py --unit beat|scene|auto`。**`--unit auto` 依 Manim 模板名單（`pipeline/template_names.py`）判定，Remotion 分鏡沒有 `template` 欄位，一律會退回逐 beat——
  Remotion 線要整場合成必須明確寫 `--unit scene`**（experiments/remotion_styles/README.md 2026-09-25 實測）。
  **ladder＝arbiter（`small.en`，免費）→ resynth（計費 1 call）→ chunk（sentence-chunk，N 個 billed sub-synth）→ beats（budget-exempt 終點，但 MiMo 下每非空 beat 仍一次 call）**；
  chunk 對 `RetryBudget` 自檢，`need > 剩餘 budget` 即 decline 退 beats；預設 `--fallback-budget 2` 只夠 resynth，chunk 要調高 budget（併入報價）才啟用。

---

## 旁白 `say` 文法與 beat 契約

> 承自 `legacy/manim_video/DESIGN.md` §〈Storyboard 格式〉之〈`say`：narration + inline reveal（核心變更）〉。模板 payload、`accent`、`scene_role`、
> 容量契約、Lectern 版面一律不承接。**整份分鏡的欄位契約（必填／選填／不再接受的 Manim 欄位、各閘讀什麼）＝[`SPEC-remotion-storyboard-schema.md`](SPEC-remotion-storyboard-schema.md)；本節只講 `say` 的文法。**

分鏡是 `meta`＋`scenes[]` 的 YAML，形狀以 `pipeline/tts.py` 讀得懂的為準（Remotion 分鏡目前只被 `tts.py` 讀；Remotion 本身只讀 `tts.py` 寫出的 manifest，
場序與拍 id 靠兩邊對得上，對不上時 composition 會直接報錯，如 `src/act3/timing.ts` 的「manifest has no scene …」）：

```yaml
meta:
  id: q7_billiards          # deck id，也是 manifest 的 deck_id
  title: Square Billiards
  language: en
  voice: Dean               # MiMo builtin voice
scenes:
  - id: logo
    kind: intro             # 非 content 場：無旁白，以 duration 定長（manifest 記為 silent）
    duration: 4.0
  - id: hook
    kind: content           # 有 say、會合成
    say: |
      Let's try a few shots.
      {show corner} Aim at a corner, and the ball drops straight in.
      {show wander} This one bounces, and bounces, and never settles.
```

規則：

- **`say` 是被朗讀的內容**，`{show <id>}` 是穿插其中的 **reveal marker**。一個 **beat** 是從一個 marker（或場開頭）到下一個 marker 之間的文字段。
  場開頭到第一個 marker 那一段是沒有 reveal 的首拍（manifest `reveal: null`；Remotion 的 `buildShow` 把它的 id 記成 `"start"`）。
- **marker id 是渲染端的查表鍵。** Manim 時代 id 指向模板 payload 的元素（`math.0`、`step.2`、`plot.1`，dotted 文法）；Remotion 時代 id 是**場內自訂**的拍名，
  由該場的元件用 id 查它的起訖時間（例：`src/q7/` 的場景以 `setup`／`theta`／`parta` 查拍）。同一場內 id 必須唯一。
- **換 marker 不換字不花錢：** reuse 以 `(scene_id, beat text_hash, 第幾個)` 定址（見上方 Manifest schema 2），只搬移／重切 `{show}`、文字一字不改時，
  帶 `--reuse-existing` 重跑 `tts.py` 是 0 次計費。**沒帶 `--reuse-existing` 就整批重合成**——計費前一律先 `--dry-run` 看 `plan`。
- **`say` 裡不寫 LaTeX。** MiMo 照字面唸（見上方「MiMo 口語軌」）；數學一律攤成口語，念法慣例的權威＝
  [`NARRATION-FAITHFULNESS-RUBRIC.md`](content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md) 的念法慣例節。

### 與 TTS manifest 的時序契約

> 承自 `legacy/manim_video/DESIGN.md` §〈Storyboard 格式〉與 §〈Data flow（目標）〉中「音訊長度驅動 reveal」的部分，改寫為 Remotion 消費端。

渲染端**只讀 manifest，不重算音訊**。Remotion 讀到的欄位（`src/s31/timing.ts` 的 `MScene`／`MBeat`）：

| manifest 欄位 | 用途 |
|---|---|
| `scenes[].scene_id`／`kind` | 場 id 與是否有旁白 |
| `scenes[].duration` | 無旁白場（silent）的長度（秒） |
| `scenes[].audio_file`／`audio_seconds` | 該場音檔與旁白總長；場長＝LEAD＋⌈旁白秒數×fps⌉＋TAIL |
| `scenes[].beats[].reveal`／`start_seconds`／`end_seconds` | 以 `{show}` id 查拍；拍起點＝LEAD＋round(start_seconds×fps) |
| `scenes[].alignment.words_file` | scene-level 的逐字時間（mock manifest 沒有）；`src/lib/words.ts` 的 `atWord()` 用它把動畫卡到某個字 |

manifest 裡的音檔路徑是跑 `tts.py` 那台機器的絕對路徑，Remotion 只取路徑的最後兩段、接在 manifest 所在資料夾之下（`src/s31/timing.ts` 的 `relAudio`，
例：`scenes/NN_id.wav`），所以 manifest 與音檔要一起搬、維持原本的子資料夾結構。
音訊在 `remotion/public/audio/`，**不進版控**；換機要重跑 TTS（真 backend 先徵同意）。

### `pauses:`——揭示之後讓畫面靜靜停一下

> 承自 `legacy/manim_video/DESIGN.md` §〈motion primitive：`pauses:`／`anim: transform`／`kind: sweep`（2026-09-12 首輪）〉之 `pauses:` 段（`anim: transform`、`kind: sweep` 與 `[stillness]` 的 `make.py` 接線不承接）。

```yaml
pauses:                      # content 場專用，opt-in
  - after: step.2            # 這個 reveal（必須是 say 裡出現過的 `{show}` 目標）
    seconds: 1.5             # 畫面停住、旁白不出聲
```

實作是**純旁白變換**（[`pipeline/pauses.py`](pipeline/pauses.py)）：在該 beat 的音訊起點插入 `seconds` 的靜音，同一個 beat 的時長加上同樣的秒數，
所以 reveal 播在靜音裡、畫面接著停住、旁白才進來。**落在磁碟上的 `manifest.json` 不會被改寫**——它是 TTS 的紀錄，reuse／freshness 都對它做雜湊；
變換只作用於記憶體中的副本。任何重讀磁碟 manifest 來對成片時間的工具（如 `rewatch_pack.py`）必須先用 `apply_pauses_timing` 折入同樣的停頓。
旁白文字不動，所以一個 pause 不花 TTS 呼叫。

**2026-09-28 現況：** 套用 `apply_pauses` 的是已封存的 `make.py`；「`after` 指到沒揭示過的 id」的檢查原在已封存的 `schema.py`，**同日起由
[`pipeline/check_storyboard.py`](pipeline/check_storyboard.py) 接手（error；見 [`SPEC-remotion-storyboard-schema.md`](SPEC-remotion-storyboard-schema.md) §2）**。Remotion 線目前**不讀**
`pauses:`，改在 composition 的 timing 裡加停留（Q7 的 `HOLD`：每場旁白後多留的幀數）。要不要讓 Remotion 改吃 `pauses:`（好讓 `rewatch_pack` 與渲染端
共用同一份停頓宣告）＝SPEC §6 待裁決項 3；schema 本身只保證宣告合法。

---

<a id="tts-workflow-proposal-2026-09-26"></a>
## 配音工作流設計（2026-09-26；三家 pilot 準備／MiMo 全片試聽）

> 承自 `legacy/manim_video/DESIGN.md` §〈配音工作流設計（2026-09-26；三家 pilot 準備／MiMo 全片試聽）〉，整節照錄。

**2026-09-26 開工更新：** 離線 `pipeline/tts_pilot_plan.py` 的三家 × 三段＝9 次計畫仍未執行；[試驗入口](experiments/tts_workflow/README.md)與[批次報量頁](_audit/REVIEW-tts-pilot-plan-2026-09-26.html)保存候選語段、voice／參數、估價限制與 hash。使用者同日另指示先用原本 MiMo 跑 Q7 中文全片，另立 14 個完整 scene 的試聽批次；新增 `tts_scene_trial.py` 與離線中文 `tts_trial_align.py`，不共用或冒用 9 次 pilot 授權。正式 `tts.py`／fallback 契約不變，完整多供應商 take 管理、選音、音鎖引擎仍待後續。

**MiMo scene trial 的已實作邊界：** `plan.json` 凍結完整來源、含無旁白場景的順序、文字／cue、HTTP payload、voice／model／參數與 plan hash；`run --approve-plan` 核對既有同意綁定的 hash，每場最多一次 HTTP、無 retry／redirect。`ledger.jsonl` 在送出前 fsync `started`，每個 UUID take 保存原始回應、原 WAV、payload 與含檔案 hash／取樣資訊的 receipt，完成後才 fsync `completed`。未知結果封鎖整批續送；成功重跑須驗檔，只重用不重配。這是單批試聽帳本，尚不是跨試音／正式／重配的完整總帳。

**中文試片匯出邊界：** 明確本機多語 Whisper `small` 權重 SHA256 驗證後，以 stable-ts `language=zh` 對完整 take 對齊。逐字序列須一致；詞內 cue 插值標 `estimated`，低機率／零時長詞留品質紀錄。全部場景成功才寫 schema 2 manifest，WAV 位元不改，保留既有 Remotion `Q7ZH` manifest prop 接口。所有產物標 `trial`／`audio_locked=false`／`nfa_status=not_verified`；人耳試看不等於正式鎖稿、音鎖或必要 cue 已人工驗到 ±0.1 秒。

**以下保留原設計範圍，不取代上方正式 MiMo／manifest schema 2 契約，也不改動現行 fallback 行為。** 完整候選契約與八種可操作情境見 [配音工作流審閱稿](_audit/REVIEW-tts-workflow-2026-09-26.html)。最初設計／離線報量階段零生成式 API 呼叫；其後 MiMo 全片試聽的授權、用量與產物另記於[試驗入口](experiments/tts_workflow/README.md)。使用者偏好＝口音不限，像真人優先。

- **範圍**：從已認可內容的旁白口語化，到可跨機取回的鎖定音軌；不設計「丟 LaTeX 自動生成整部影片」。
- **流程**：共用念法／lint → NFA＋稿鎖 → 該批計畫與費用同意 → 自然語段合成並立即存 take → 獨立念法 QA／對齊／選 take → 剪裁／停頓／音量處理 → 核對最後交付音檔時序 → 音鎖與既有 manifest 相容匯出。
- **人工接觸點**：確認稿、同意該批用量與費用、鎖音前完整試聽一次（最後一項尚待拍板）。外部 NFA／第二意見仍須逐次報量同意。
- **狀態語義**：提案為 `draft → script_locked → reviewing → audio_locked`；入口保留既有 `CONTENT_APPROVED`／source lock。`script_locked` 指口語合成輸入通過 NFA 的快照，不改既有 NFA 在 source 鎖稿後審查的契約。
- **三種單位**：自然語段負責合成；語言專屬文字 span／穩定 cue ID 負責定位；scene／beat 負責相容匯出。短 scene 可整段，長 scene 自然斷；中英各自分段，不強制相同 beat 數。show marker 不自動成為 TTS 切點。
- **重用身分**：request identity 包含實際送出的文字（保留標點）、供應商／模型／voice／參數，排除畫面順序與 cue 位置。詞庫版次記來源，但展開後輸入不變不付費重配。
- **Take 保存**：take ID／原始 hash 與 request identity 分開，同請求可多 take；每個成功 take 與 receipt 立即保存，對齊失敗不丟音檔。預設重用，新增 take 明確選擇；ASR／對齊失敗不自動合成，鎖音檔遺失先取回。
- **版本邊界**：處理配方／交付 hash／timing 各有版本。cue 映射只更新時序與匯出、重驗必要 cue；新 take 或任何音訊後製使舊音鎖失效。改時長後重新變換／對齊並驗證，只改音量也更新交付 hash。
- **QA 與時序**：先驗供應商時間，再選本機限稿 FA；自由 ASR 只找疑點，不當數學／字幕真相。正規化不得抹去負號、變數、分子分母與否定詞。插值標 `estimated`，必要 cue 可人工校點並留來源。
- **鎖音條件**：附 NFA、念法、聽感與時序裁決；可豁免項目需記人與理由。未裁決錯讀或必要 cue `unresolved` 不得鎖音，不能以泛用豁免繞過。
- **批次同意**：plan 快照綁定文字、語段、模型、voice、參數與上限，內容變更即重新報量；使用者不必手抄 hash。列重用命中、字數／估計分鐘、計費單位／單價來源日期、請求數與上限；本提案費用待報價。
- **帳本**：初版無自動付費重試；HTTP 嘗試也納入硬上限。結果不明標 `unknown`、查 receipt／帳務，不假裝零費用。試音／正式／重配共用累計帳本，不以最後 manifest receipt 冒充總帳；mock／live 隔離。0 次 TTS 不等於零外部費用，雲端 ASR／外部 NFA 另報。
- **音鎖交付物**：spoken revision／語言／段 ID／scene 映射；選定 take、原始／交付 hash、時長與採樣資訊；文字 span／詞句／cue 時序與 source／quality；後製配方／offset；QA 證據與 receipts；相對路徑與跨機資產索引。音檔可不進 Git，但須另存可恢復位置，不靠 TTS 重生。
- **Remotion 接口**：沿用 `buildShow`／`words.ts` 與 manifest 消費端，只讀鎖音產物；預覽／render 不直接合成。不先造完整 visual events DSL。
- **Q7 候選試驗**：MiniMax Speech 2.8 HD、ElevenLabs v3、MiMo 基準；Fish S2.1 Pro／Gemini 候補。先選 voice／相同口語語段，以 `mirror`（或 `hook`）、`halfway`、`recap` 各試一段。候選最多 3 家 × 3 段 × 1 take＝9 次初始合成；voice 試音／重試另報，字數與估計秒數待量稿，尚未執行／未獲該批同意。已有 MiMo beat 音檔只作現況 baseline；公平同語段比較的新 MiMo 呼叫算進這 9 次。
- **試驗驗收建議**：等響度、無 BGM 盲聽；錯讀硬門檻，記自然度、接續、人工修改工時與 cue 誤差。暫提必要 cue 人工確認 ≤0.10s（待審、非模型保證）；勝出後長段穩定試驗另報。沒有捏造品質分數或勝出結果。
- **三階段落地**：先評聲音／時序來源；再做 plan／reuse／take／review／lock；最後補中文詞庫／span／cue 與 manifest adapter。既有工具責任映射詳見 HTML，允許人工校點，不先造全自動引擎。
- **依賴**：缺套件／模型先提方案徵同意，不自裝或手刻替代；批准新增後同步 `ENVIRONMENT.md`、`tools/doctor.py` 與版本鎖。本輪零依賴變更。
- **來源**：HTML 列官方能力文件與 repo 現況，查核日 2026-09-26；文件能力不是 Q7 實測，所選模型的參數相容性與費用仍待執行前核對。

---

## 語意色軸：六個語意族 ↔ 講義色

> 承自 `legacy/manim_video/DESIGN.md` §〈語意色軸＝講義的色軸（Direction B「對位」；2026-09-12 使用者裁決）〉，只承接對照表與對位原則。
> 模板家具怎麼上色、`accent` 欄位、hook 物件色慣例、`_selftest_semantic_palette.py` 閘都屬 Manim gen-2，見 legacy 原文。

**對位原則（2026-09-12 使用者裁決）：同一個概念在 PDF 與影片是同一個色相。** 影片的語意色不自訂，對位到講義
[`handout/latex/template/calcbook.sty`](../handout/latex/template/calcbook.sty) 的 `\definecolor` 軸：淺底（與 PDF 同為紙張底）逐字沿用講義 hex；
深底只為對比提亮、**色相不變**。沒有對應講義有色環境的內容（散文、圖）＝中性，不替作者宣告他沒寫的語意。

| 語意族 | 講義色名 | 涵蓋的講義環境／卡類型 | 淺底（＝講義 hex） | 深底提亮（Manim gen-2 用值） |
|---|---|---|---|---|
| concept | `aConcept` | definition | `#994a00` 赭 | `#d98f3c` |
| result | `aResult` | theorem／proposition／corollary／proof／recap；正文主色（derivation 的結論行） | `#0068a7` 藍 | `#4fa6de` |
| practice | `aPractice` | example／solution | `#04773b` 綠 | `#3ebe7c` |
| caution | `aCaution` | caution／warning | `#aa3333` 紅 | `#d96b6b` |
| strategy | `aStrategy` | procedure／strategy | `#6453a7` 紫 | `#a493e6` |
| aside | `aAside` | remark／note；未標記內容的中性色 | `#5d646f` 灰 | `#96a0ae` |

**Remotion 線是否沿用本軸，由設計輪決定。** 現役 `remotion/`（紙本編輯排版）風格用的是自己的 token（`src/theme.ts`：墨黑＋品牌深紅 `accent`＋藍鉛筆 cobalt，見
[`remotion/STYLE.md`](remotion/STYLE.md)），尚未對位到上表。要定為模板時，再決定是整套採用、只取部分族群，
或維持紙本風格自己的語意色；決定後回寫本節。

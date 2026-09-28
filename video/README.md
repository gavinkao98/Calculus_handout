# video/ 課程影片產線

將一節講義轉成一支帶旁白的課程影片。**2026-09-28 起 Remotion 是唯一正式渲染器**（使用者拍板；契約與逐檔清單＝
[`KICKOFF-remotion-unification.md`](KICKOFF-remotion-unification.md)）。沿革：

1. **gen-1 Manim**（`tools/manim_*` 一族）——已凍結，封存在 [`../legacy/scripts/`](../legacy/scripts/)（`manim_*`）與 `../legacy/MANIM_*.md`。
2. **gen-2 Manim**（2026-05～09：`make.py` orchestrator＋模板引擎＋storyboard＋hook）——2026-09-28 整包封存到
   [`../legacy/manim_video/`](../legacy/manim_video/)（`git mv`，相對路徑不變，`git log --follow` 追得到）；回退錨點＝tag `archive/2026-09-28-manim-gen2-final`。
3. **Remotion**（2026-09-25 起風格探索、2026-09-28 升為唯一路線）——現役製作處＝[`remotion/`](remotion/STYLE.md)
   （2026-09-28 自 `experiments/remotion_styles/paper/` 升格，選定風格＝紙本編輯排版；風格探索紀錄與另兩個方向留在 [`experiments/remotion_styles/`](experiments/remotion_styles/README.md)）。

- **資料流與旁白契約：** [DESIGN.md](DESIGN.md)（Remotion 時代的精簡版；Manim 時代的完整設計在 [`../legacy/manim_video/DESIGN.md`](../legacy/manim_video/DESIGN.md)）
- **畫面契約（token、字型、版面、動態語彙）：** [`remotion/STYLE.md`](remotion/STYLE.md)
- **所有審核閘一覽（各層閘＋meta-gate＋輪次協定）：** [REVIEW_GATES.md](REVIEW_GATES.md)
- **跨對話進度錨：** [REBUILD_STATUS.md](REBUILD_STATUS.md)
- **輸入：** 講義 **LaTeX 線**（[`../handout/latex/`](../handout/latex/)）的各節（由人閱讀、手寫產出內容稿）。**各章權威檔＝`../handout/latex/src/<ch>/<name>.tex`（唯一內容源；閱讀版＝`dist/<ch>/<name>.pdf`）**——2026-08-09 LaTeX 統一拍板（U5，[`../handout/latex/KICKOFF-latex-unification.md`](../handout/latex/KICKOFF-latex-unification.md)）。沿革：2026-06-10 前輸入為第一代 `../chapters/*.tex`（§1.1/§1.6 原型基於它）→ 2026-06-10 換 HTML standalone（ch01 拍板檔＝`chapter1-print-standalone.html`，其 `source:` 錨沿用於既有內容稿，屬歷史紀錄不改）→ 2026-08-09 換回 LaTeX（源升格）。既有內容稿的 `source:` 錨照舊；**新內容稿一律錨 `<name>.tex`**（格式見 [`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md) §6）。**機器可解析的錨文法（2026-09-12 收尾）：** `ref:`／`refs:` 的 `doc:` 對 `.tex` 用 calcbook label key——`doc:sec:3.1`／`doc:thm:3.1`／`doc:def:3.1`／`doc:fig:3.1`（`pipeline/provenance.py` 直接讀 `.tex` 解析；既有 deck 的 `doc:frag-sec-*`／`data-fig` 仍解析到凍結 `legacy/` standalone）；**LOCKED 內容稿標頭 MUST 帶 `source_rev` 講義源 stamp**（`python video/pipeline/source_rev.py <源檔>` 產生；比對不符即 `[source_rev]` WARN＝走 CONTENT_METHODOLOGY §8）。
- **輸出：** Remotion 成片在 `remotion/out/`（gitignored）；TTS 試驗與工具輸出在 `output/`（gitignored）。

## 結構

```
video/
  README.md              你在這裡
  DESIGN.md              資料流＋旁白 `say`／`{show}` 契約＋配音工作流＋語意色對照（先讀這個）
  CONTENT_METHODOLOGY.md Stage-1 內容稿撰寫方法論（拆解、narration、來源標註）
  REBUILD_STATUS.md      跨對話進度錨（逐節狀態以此為準）
  REVIEW_GATES.md / REVIEW_MODEL_DECISIONS.md / RUNBOOK-mimo-narration-route.md   審核層／決策／流程
  SPEC-motion-language.md   畫面語法五條規則（設計語言層；實作契約層隨 Manim 封存）
  SPEC-pedagogy-firstlearner-{framework,expansion}.md / PROPOSAL-scope-packaging-coverage.md   教學規格
  KICKOFF-remotion-unification.md   2026-09-28 Remotion 統一的契約與紀錄
  KICKOFF-s32-chain-rule.md / KICKOFF-process-reform.md              節與流程的開工檔（歷史＋仍有效部分見各檔頂註）
  requirements.txt       pinned 依賴
  remotion/              ★ 現役製作處：Remotion 專案（紙本編輯排版；2026-09-28 自 experiments/remotion_styles/paper/ 升格）
    STYLE.md             畫面契約（token、字型、版面、動態語彙）
    src/                 Root.tsx（composition 註冊）、共用元件、各片場景（act3/、s31/、q7/）
    act3/ s31/ q7/       各片分鏡 yml＋SCRIPT.md（重現指令）＋審核頁
    scripts/             loudnorm.py（house −19 LUFS）、chapters.py（章節點）、frames.mjs（靜幀）、cjk-subsets.mjs（中文字型分片）
    public/brand/        logo 複本（進版控）；public/audio/＝TTS manifest＋WAV、out/＝成片（皆 gitignored）
  pipeline/              共用層（渲染器無關；全部進版控）
    tts.py               TTS 入口（MiMo 為正式路線；--backend mock 離線靜音）
    tts_*.py             配音工作流試驗工具（pilot 報量、MiMo scene trial、Gemini 試驗與數學探針、阿里雲 SSML、中文離線對齊）
    scene_align.py / scene_fallback.py   scene-level forced alignment（stable-ts）與 fallback ladder
    narration.py / audio.py / timing.py / atomicio.py   `{show}` 解析、WAV 輔助、同步常數、原子寫入
    derive_spoken.py / derived_check.py / template_names.py   口語軌派生與 freshness stamp
    pauses.py / stillness.py / captions.py   `pauses:` 旁白變換、靜止判定、字幕
    loudnorm.py          兩段式 loudnorm（house −19 LUFS；自封存的 make.py 抽出）
    mimo_preview.py / listening_pack.py / loudness_ab.py / house_audio.py   試聽與聽感驗收
    rewatch_pack.py      看片評審 pack＋12 s 靜止硬閘（沿用，待接 Remotion）
    provenance.py / pedagogy.py / step_coverage.py / example_coverage.py / source_rev.py /
      review_pack.py / _screen_contract.py / narration_review.py   內容層確定性檢查器（待接 Remotion 分鏡）
    _bootstrap.py        sys.path 與輸出目錄 helper（精簡版）
    run_selftests.py / _selftest_*.py / _regression_scene_align.py   離線自測
    assets/              品牌 logo（Remotion 唯一固定元素）＋ house audio cue
  content_scripts/       逐節內容稿（Stage 1 產物，進版控）
    <deck>.md            內容稿（教學單元拆解、`[source:]` 標註）
    <deck>.spoken.yml    口語單一源（Manim 時代的雙軌產物，保留）
    <deck>_narration.html   旁白 sign-off 稿（淺色、MathJax、雙擊即開）
    _audit/              稽核資產（進版控）
      *-RUBRIC.md        六份判斷閘 SSOT（six-lens／copyedit／NFA／VISUAL-FRAME／pedagogy-firstlearner／amplification）＋ REWATCH rubric
      PROMPT-*.md        thin prompt（template + per-deck）
      REPORT-*.html / REVIEW-*.html   稽核／完工報告（self-contained，圖 base64 內嵌）
      _gen/              報告產生器＋資料（進版控；見下節「版控策略」）
  storyboards/
    _fixtures/           內容層 selftest 的 fixture（otf_provenance／sc_coverage／scaffold／pedagogy_audit{,_draft}）
  experiments/           實驗線
    remotion_styles/     Remotion 風格探索紀錄（blueprint/、dark_glow/ 未選定方向；paper/ 已升格為 ../remotion/）
    remotion_pilot/      Remotion 前置評估與第三幕規劃稿
    tts_workflow/        配音工作流試驗（Q7 中文 MiMo／Gemini 全片試聽、三家 pilot 報量）
    reference_frames/    YouTube 參考影片抓幀／拆解／對照表工具
    forced_alignment_dean/   整段音訊＋alignment 的歷史起源（已結案）
  _audit/                產線層的審閱頁（TTS 試聽、loudness A/B、code review 2026-09-23…）
  _archive/              歷史輪次全文與舊計畫
  output/                ★ TTS／工具輸出（gitignored，可重生）
```

`animations/`、`make.py`、`pipeline/` 的渲染側（`scene.py`／`blocks.py`／`brand.py`／`templates/`／`visuals/`／`fonts/`／`schema.py`／`lint.py`／`sizecheck.py`／`critic.py`…）、
五支正典 storyboard 與 `_demo_*.yml` 都已不在 `video/`——在 `../legacy/manim_video/` 同一相對路徑下。

### 資料夾架構與版控策略（哪些進 git、哪些不進）

**原則：可重生的成品不進版控；人寫的源、稽核裁決、不可重生的證據進版控。** 因為作者常換電腦，
凡「換機後還要讀得到」的東西（尤其**含圖的 HTML 報告**）都必須能隨 git 走到每台機器。

| 類別 | 範例 | 進 git？ | 規則 / 位置 |
|---|---|:---:|---|
| 文檔・共用層・源 | `*.md`、`pipeline/**`、`content_scripts/*.md`／`*.html`、Remotion 專案的 `src/**`、分鏡 `*.yml`、`SCRIPT.md` | ✅ 進 | 預設追蹤 |
| 稽核資產 | `_audit/*-RUBRIC.md`、`PROMPT-*.md`、`REPORT-*.{md,html}`、`REVIEW-*.html` | ✅ 進 | HTML 報告須 **self-contained**（見下） |
| 模型 raw 輸出 | `*.raw.txt`（Codex／VLM 原始 dump） | ❌ 不進 | 落 gitignored scratchpad；findings 與裁決**轉錄**進版控 REPORT／REVIEW（2026-07-07 與講義線統一） |
| 報告產生器＋資料 | `_audit/_gen/*.gen.py`、`*.digest.json`、`frames_before/` | ✅ 進 | 放在 tracked 位置，**不要**留在 `output/` 內 |
| 品牌 logo 資產 | `pipeline/assets/brand/*.svg`、`pipeline/assets/lockup-color-outlined.svg` | ✅ 進 | NTU logo 向量源＋`_outline_text.py` 產的 outlined 版 |
| 成片與音訊 | Remotion 的 `out/`、`public/audio/`（manifest＋WAV）；`output/**` | ❌ 不進 | `remotion/.gitignore`：`out/`、`public/audio/`；根 `.gitignore`：`/video/output/`。付費 TTS 原音換機要重跑（先徵同意） |
| 依賴與快取 | `node_modules/`、`**/__pycache__/`、ad-hoc `*.log` | ❌ 不進 | `npm ci` 還原 Remotion 依賴 |

**含圖 HTML 報告的鐵則 —— 一律 self-contained（圖 base64 內嵌）。** render 幀／截圖在 gitignored 的輸出夾，
新 clone 的機器上不存在；報告若用相對路徑引用那些幀，換機開啟就**整片空白**。因此凡含圖的報告：

1. **產生器把每張幀讀進來、base64 內嵌成 `data:image/png;base64,...`**（用 `.venv` 的 Pillow 縮到約 1100px 寬，兼顧清晰與檔案大小），輸出**零外部圖片引用**的 HTML。驗證：`grep -c 'src="\.\./' report.html` 應為 `0`。
2. **產生器、digest、不可重生的 `frames_before/` 一律放 `_audit/_gen/`（進版控）**，不要留在會被清掉的輸出夾內——否則輸出夾一清，committed HTML 就永久 dangling、且無從重生。
3. 可重生的幀仍由輸出夾供應（重跑即重生）；產生器在幀缺席時退回 placeholder，不會壞掉。

範式：[`content_scripts/_audit/_gen/build_spoken_review.py`](content_scripts/_audit/_gen/build_spoken_review.py)。

## 狀態

逐節進度與跨對話狀態以 [REBUILD_STATUS.md](REBUILD_STATUS.md) 頂部現況快照為準（本檔不重複）。要點（2026-09-28）：

- **渲染器＝Remotion，唯一正式路線。** Manim gen-2 引擎、模板、storyboard、hook 已封存；§3.1 的 Manim 成片（`output/ch03/s3.1/…_mimo.mp4`，本機 gitignored）隨引擎封存、不再迭代。
- **Remotion 已交付的片（`remotion/`）：** §3.1 第三幕（`act3/`）、§3.1 無指引全節（`s31/`，約 8 分）、解題影片 Q7 英文版與中文版 `Q7ZH`（`q7/`）。
  逐片紀錄、呼叫數與重現指令在 [`experiments/remotion_styles/README.md`](experiments/remotion_styles/README.md)。
- **TTS＝MiMo `mimo-v2.5-tts`**（英文 voice Dean、中文 voice 冰糖）；Remotion 線用 `tts.py --unit scene`＋stable-ts forced alignment，失敗自動回退逐 beat。
  配音工作流試驗（Gemini 中文試片、三家 × 三段 pilot 報量）見 [`experiments/tts_workflow/README.md`](experiments/tts_workflow/README.md)；9 次 pilot 仍未執行。
- **內容層不變：** `content_scripts/`（內容稿、口語版、rubric、稽核報告）全部留在原位；§3.2 Phase A（內容線）成果有效，Phase B（視覺線）作廢、待 Remotion 版 KICKOFF。
- **待辦（另開輪次）：** §3.2 Phase B 的 Remotion 版 KICKOFF；內容層檢查器接 Remotion 分鏡 schema；`.claude/launch.json` 的 `remotion-review` 路徑修正（[KICKOFF-remotion-unification](KICKOFF-remotion-unification.md) §6）。

## 指令

**Remotion 成片（重現）：** 每支片的完整指令（mock 版、真配音版、loudnorm、局部重渲）寫在它自己的 `SCRIPT.md`，權威＝
各片 `remotion/<片>/SCRIPT.md`（例 [`remotion/q7/SCRIPT.md`](remotion/q7/SCRIPT.md)）；逐片紀錄與呼叫數在 [`experiments/remotion_styles/README.md`](experiments/remotion_styles/README.md)。
流程是三步：`tts.py` 產 manifest → 在 `remotion/` 下 `npx remotion render`（1920×1080、30 fps）→ `python scripts/loudnorm.py`。最快的離線 mock（不計費）：

```powershell
python video\pipeline\tts.py --storyboard video\remotion\q7\q7.yml --scene all --backend mock --unit beat --output-dir video\remotion\public\audio\q7_mock
cd video\remotion; npm ci; npm run q7      # → out/q7_mock.mp4；npx remotion studio 可即時預覽
```

**離線 manifest／beats 時鐘檢查**（寫出無聲 WAV，不計費）：`tts.py --backend mock --unit beat`。

> **`--unit beat` 必帶**（2026-09-23 程式碼審查 A-06）：`--unit auto` 會把該送 scene-level 的場送去 stable-ts 對齊，mock 的靜音對不上 → fallback ladder → 每場都落到 beats 終端；沒有 model cache 時還會下載 whisper，不是離線；缺 stable-ts 則直接中止。這一步**只驗 beats 時鐘**，**不代表 scene_aligned 的 beat 時序**。另注意 `--unit auto` 依 Manim 模板名單判定，Remotion 分鏡沒有 `template`，**真配音要整場合成必須明確寫 `--unit scene`**。

**離線自測（零計費、不 render）**——改 code 後跑、換機後跑：

```powershell
.venv\Scripts\python video\pipeline\run_selftests.py          # 全部 pipeline/_selftest_*.py；任一紅即 exit 1
.venv\Scripts\python video\pipeline\run_selftests.py -k tts   # 只跑名字含 tts 的
python tools\doctor.py                                        # 環境健檢
```

Remotion 端的型別檢查：在 `remotion/` 下 `npm run lint`（`tsc`）。

**看片評審（REWATCH）**——以觀眾的方式審成片（時間、停留、畫面有沒有動、跟不跟得上）。契約＝
[`content_scripts/_audit/REWATCH-REVIEW-RUBRIC.md`](content_scripts/_audit/REWATCH-REVIEW-RUBRIC.md)，里程碑審的定位見 [`REVIEW_GATES.md`](REVIEW_GATES.md) §六。
**沿用，待接 Remotion：** `pipeline/rewatch_pack.py`（contact sheet＋時間軸＋12 s 最長靜止硬閘 `--gate-still`）目前以 `--deck` 讀 `storyboards/<deck>.yml`
與 `output/<ch>/<sec>/` 的佈局，Remotion 成片要接上另開輪次；接上之前可直接對 `out/*.mp4` 用 ffmpeg 抽幀或 `remotion/scripts/frames.mjs` 出靜幀。

**解析度：** 一律 1080p（Remotion composition 皆 1920×1080、30 fps；見根 [`CLAUDE.md`](../CLAUDE.md)「影片渲染解析度」）。

## MiMo 旁白路線（口語 · 念法 · 計費）

MiMo（小米 `mimo-v2.5-tts`，公測免費、OpenAI 相容、key＝`MIMO_API_KEY`）是正式旁白路線，但它**不讀 inline LaTeX**，旁白要「把數學攤成口語」。
Remotion 線的分鏡 `say` 直接寫口語（見 [DESIGN.md](DESIGN.md)「旁白 `say` 文法」）；Manim 時代的雙軌 single-source（`content_scripts/<deck>.spoken.yml`
＋`derive_spoken.py` 生成 `_mimo.yml`）仍在 `pipeline/`，但它讀的正典 storyboard 已封存到 legacy。

```powershell
$env:MIMO_API_KEY = "<key>"   # 或放 .env；批次合成前依 CLAUDE.md 報用量、徵同意
python video\pipeline\tts.py --storyboard <分鏡.yml> --scene all --backend mimo --unit scene --output-dir <video\remotion\public\audio\批次> --dry-run   # 先報價
python video\pipeline\tts.py --storyboard <分鏡.yml> --scene all --backend mimo --unit scene --output-dir <video\remotion\public\audio\批次>
```

- `tts.py --backend mimo`：OpenAI 相容 `/chat/completions`，待唸文字放 `assistant`；預設 `MIMO_MODEL=mimo-v2.5-tts`、`MIMO_VOICE=Dean`（經 `audio.voice` 選定）、`MIMO_STYLE`＝空（builtin 路線不送 persona／style prompt）。`MimoTTSBackend` 預設裁 beat 頭尾靜音（留 0.08s），manifest 記錄 `raw_audio_seconds`／`trimmed_audio_seconds`／`trimmed_silence_seconds`。**`--backend` 必填**。
- 計費紀律（`--dry-run` 報價、`--reuse-existing`、`--no-billing`／`--max-billed-calls`、`--skip-qa`、fallback budget）的操作細節＝[`RUNBOOK-mimo-narration-route.md`](RUNBOOK-mimo-narration-route.md)。
- 只想聽聲音不要影片：`python video\pipeline\mimo_preview.py --spoken <..._narration_spoken.md>`（`--dry-run` 不呼叫 API、`--smoke` 只合首段；`--voice Mia` 等可試別的 builtin voice）。離線聽感驗收：`python video\pipeline\listening_pack.py --manifest <…\manifest.json>`。
- **MiMo 非決定性**：同文字每次合成是不同 take（±~10% 長度）；要鎖定某 take 就別重合成。
- 念法慣例（`f inverse` 不念 reciprocal、`x sub one`、和／差根號加 “the quantity”、座標 “the point with coordinates a and b”…）**權威＝NFA 契約 [`content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md`](content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md) 的念法慣例節**。

**forced alignment 是正式路線**：計時源＝`pipeline/scene_align.py` 的 `stable-ts` transcript-constrained forced alignment（一場一次合成、回推每 beat 時序），
`whisper-timestamped` 降級為 ASR QA 探針；過不了自動回退 beat。第一次跑 aligner model（`base.en`）會下載約 139 MB model cache。中文（Q7ZH）走 `--unit beat`
或離線 `tts_trial_align.py`（多語 Whisper `small`），見 [`experiments/tts_workflow/README.md`](experiments/tts_workflow/README.md)。

## Manim gen-2 專屬節（已封存）

原本的「文字渲染（避免亂碼：Route A／`brand.prose`）」「VLM 視覺批改（`critic.py`）」「工程鏡 cross-review（`review_pack.py` 的 hook packet）」「踩過的坑」
「`make.py` 指令與自動守門員（schema／lint／sizecheck）」「模板與 motion primitive 目錄」都只屬 Manim 引擎，已隨引擎封存；要查請讀
tag `archive/2026-09-28-manim-gen2-final` 上的 `video/README.md`（`git show archive/2026-09-28-manim-gen2-final:video/README.md`）與 [`../legacy/manim_video/DESIGN.md`](../legacy/manim_video/DESIGN.md)。

## 環境

> 📌 **環境統一的權威清單在 repo 根 [`ENVIRONMENT.md`](../ENVIRONMENT.md)；換機後跑 `python tools/doctor.py` 一行看出缺什麼、`tools/setup.ps1` 備妥 Python 端。** 本節僅補 video/ 特有細節。

- **Python 端（TTS／對齊／自測）：** 用 **repo 根的 `.venv`**（`tools/setup.ps1` 從 `requirements.lock` 建）；全域 python 可能缺 PyYAML 等套件。
- **Remotion 端：** Node（版本見 `ENVIRONMENT.md`）；各 Remotion 專案在自己的資料夾 `npm ci` 還原依賴（`node_modules/` 不進版控）。
- **ffmpeg：** 裝 Gyan.FFmpeg 全套（`ffmpeg`＋`ffprobe` 一起進 PATH；loudnorm 與抽幀都要，策略 A，2026-06-17 定）。
- **MiMo key：** env `MIMO_API_KEY` 或 repo-local `.env`（公測免費，仍屬外部 API，依 CLAUDE.md 批次前徵同意）。

```powershell
powershell -ExecutionPolicy Bypass -File tools\setup.ps1   # 建 .venv＋裝 requirements.lock＋自動跑 doctor
winget install --id Gyan.FFmpeg -e                          # 真 ffmpeg＋ffprobe 進 PATH
python tools\doctor.py                                       # 確認全綠
```

> ⚠️ **環境依機器而定——換機後先驗證、別照搬（使用者常換電腦）。** 單機偵錯歷史帳見 `video/_archive/` 的 REBUILD 歸檔。

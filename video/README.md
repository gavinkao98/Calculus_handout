# video/ 課程影片產線（第二代）

將一節 HTML 講義（handout kit）轉成一支帶旁白課程影片的單一進入點。取代第一代的
`tools/manim_*` 產線（現已凍結）。

- **改了什麼、為什麼：** [DESIGN.md](DESIGN.md)
- **所有審核閘一覽（七層 + meta-gate + 各節狀態）：** [REVIEW_GATES.md](REVIEW_GATES.md)
- **輸入：** HTML 講義（handout kit，[`../handout/`](../handout/)）的各節（由人閱讀、手寫產出內容稿）。**各章權威檔**——ch01：[`chapter1-print-standalone.html`](../handout/chapter1-print-standalone.html)（2026-06-10 拍板；原 `chapter1-standalone.html`，2026-06-13 重組後改此名，編輯源在 `fragments/ch01/sec-*.html`）；ch02+ 屆時在此補。2026-06-10 前的輸入源為 `../chapters/*.tex`（已換源，§1.1/§1.6 原型基於它）。
- **輸出：** `output/`（gitignored）

## 結構

```
video/
  README.md            你在這裡
  DESIGN.md            格式 + 資料流契約（先讀這個）
  CONTENT_METHODOLOGY.md   內容稿撰寫方法論（Mode A／C 散文密度、來源標註）
  REBUILD_STATUS.md    跨對話進度錨（逐節狀態以此為準）
  REVIEW_GATES.md / REVIEW_MODEL_DECISIONS.md / RUNBOOK-*.md   審核層／決策／流程
  make.py              單一入口 orchestrator：parse → synth → render → compose（離線、不計費）
  requirements.txt     pinned 依賴
  pipeline/            產線引擎（全部進版控）
    assets/fonts/      在執行期註冊的內附設計字型
    visuals/           移植並驗證過的素材（colors、graph eval、layout）
    templates/         Direction B 場景模板
    blocks.py          可揭示的 Block 抽象 + 動畫派發
    brand.py           grid、字體排印、卡片、logo 與 motif
    narration.py       `{show ...}` 解析器 + 後備時長估計（無 manifest 時）
    audio.py           供 PCM 輸出、時長與串接用的 WAV 輔助程式
    timing.py          旁白同步常數/檢查 helper（lead、tail、短 beat、hash）
    scene.py           所有模板共用的 Manim player（reveal 時序由音訊時長驅動）
    lint.py            render 前守門員：亂碼／不平衡 `$`／散文手動 `\\`／空心點
    sizecheck.py       render 前守門員：並排字級、出框、安全邊界、content 區塊重疊
    schema.py          render 前守門員：storyboard 結構驗證＋列舉 `{show}` 目標
    critic.py          render 後視覺 gate2：抽幀 → MiMo-V2.5 依 VISUAL-FRAME 判定（外部 API、公測免費）
    review_pack.py     工程鏡 packet 組裝（gate1 Claude／gate2 Codex 讀；離線、無 API）
    tts.py             MiMo TTS（唯一真旁白路線；Gemini 已退場 2026-06-16）
  content_scripts/     逐節內容稿（Stage 1 產物，進版控）
    <deck>.md          內容稿（教學單元拆解、`[source:]` 標註）
    <deck>_narration.html   旁白 sign-off 稿（淺色、MathJax、雙擊即開）
    _audit/            稽核資產（進版控）
      *-RUBRIC.md      五份判斷閘 SSOT（six-lens／copyedit／NFA／VISUAL-FRAME／hook-engineering）
      PROMPT-*.md      thin prompt（template + per-deck）
      REPORT-*.html / REVIEW-*.html   稽核／完工報告（self-contained，圖 base64 內嵌）
      _gen/            報告產生器 + 資料（進版控；見下節「版控策略」）
        *.gen.py       產生器：讀 .digest.json + 幀 → 輸出 self-contained HTML
        *.digest.json  稽核裁決資料（workflow digest；不可廉價重生，故進版控）
        frames_before/ 修改前 bug-state 幀（不可重生的證據；唯一進版控的 render 幀）
  animations/          客製動畫 hook code（`# HOOK` 接入點；進版控）
  storyboards/         Stage 2 工程稿（進版控）
    _demo_*.yml        模板示範／回歸樣本（asymptote／derivation／graph_compare／sign_chart／…）
    <deck>.yml         逐節正式 storyboard（依方法論產生）
  design_handoff/      設計交付參考（進版控；DESIGN_BRIEF、from_designer/、tokens、參考截圖）
  output/              ★ render 成品（gitignored，可重生），按 ch<NN>/s<X.Y>/ 歸類
    ch01/s1.1/         一節成品——mp4、audio/、critic/frames/、review/packets/
    _media/ media/ __pycache__/   manim／python 快取（gitignored）
```

### 資料夾架構與版控策略（哪些進 git、哪些不進）

**原則：可重生的成品不進版控；人寫的源、稽核裁決、不可重生的證據進版控。** 因為作者常換電腦，
凡「換機後還要讀得到」的東西（尤其**含圖的 HTML 報告**）都必須能隨 git 走到每台機器。

| 類別 | 範例 | 進 git？ | 規則 / 位置 |
|---|---|:---:|---|
| 文檔・引擎・源 | `*.md`、`make.py`、`pipeline/**`、`storyboards/*.yml`、`content_scripts/*.md`／`*.html`、`animations/**` | ✅ 進 | 預設追蹤 |
| 稽核資產 | `_audit/*-RUBRIC.md`、`PROMPT-*.md`、`REPORT-*.html`、`REVIEW-*.html`、`*.raw.txt` | ✅ 進 | HTML 報告須 **self-contained**（見下） |
| 報告產生器＋資料 | `_audit/_gen/*.gen.py`、`*.digest.json`、`frames_before/` | ✅ 進 | 放在 tracked 位置，**不要**留在 `output/` 內 |
| 設計參考截圖 | `design_handoff/**/*.png`、`tokens.json` | ✅ 進（例外） | 不可重生的設計底稿；非 pipeline 產物 |
| render 成品 | `output/**`：`*.mp4`、`*.wav`、`critic/frames/*.png`、`manifest.json`、`review/packets/` | ❌ 不進 | `.gitignore`：`/video/output/` |
| 渲染／快取 | `media/`、`pipeline/**/media/`、`**/__pycache__/`、ad-hoc `*.log` | ❌ 不進 | `.gitignore`：`media/`、`__pycache__/` |

**含圖 HTML 報告的鐵則 —— 一律 self-contained（圖 base64 內嵌）。** render 幀／截圖在 `output/`（gitignored），
新 clone 的機器上不存在；報告若用相對路徑 `../../output/...` 引用，換機開啟就**整片空白**。因此凡含圖的報告：

1. **產生器把每張幀讀進來、base64 內嵌成 `data:image/png;base64,...`**（用 `.venv` 的 Pillow 縮到約 1100px 寬，兼顧清晰與檔案大小），輸出**零外部圖片引用**的 HTML。驗證：`grep -c 'src="\.\./' report.html` 應為 `0`。
2. **產生器、digest、不可重生的 `frames_before/` 一律放 `_audit/_gen/`（進版控）**，不要留在會被清掉的 `output/` 內——否則 `output/` 一清，committed HTML 就永久 dangling、且無從重生。
3. 可重生的 `final.png` 仍由 `output/` 供應（重跑該節即重生）；產生器在 `output/` 被清空時，對缺幀的 `final.png` 退回 SVG placeholder，不會壞掉。

範式：[`content_scripts/_audit/_gen/REVIEW-ch01_inverse_functions-visualframe.gen.py`](content_scripts/_audit/_gen/REVIEW-ch01_inverse_functions-visualframe.gen.py)。

## 狀態

**目前檢查點（2026-06-16）：產線工具鏈穩定；第一章舊練習產物已全數廢棄，將從講義逐節重跑。**
逐節進度與跨對話狀態以 [REBUILD_STATUS.md](REBUILD_STATUS.md) 為準（本檔不重複）。

- **TTS 收斂為 MiMo/Mia 單一路線**（Gemini/Charon 已退場 2026-06-16）。
- **舊 `ch01_*` 內容稿／工程稿／旁白／hooks／per-deck 稽核報告與整個 `output/` 已刪除**——當時純為累積方法論經驗的練習；正式版從 HTML 講義 [`chapter1-print-standalone.html`](../handout/chapter1-print-standalone.html) 逐節重跑。
- 引擎完整：`make.py` orchestrator、**三道 render 前閘（schema → lint → sizecheck）**、模板 catalog、`hook:` 機制、MiMo TTS、`timing.py` 同步守衛、五份判斷閘 SSOT rubric（six-lens／copyedit／NFA／VISUAL-FRAME／hook-engineering）。
- 音訊驅動對齊（每 beat 影片長度＝該 beat 音檔長度）為產線核心；mock 路徑（`make.py --backend mock`）離線、不計費，供版面／時序迭代。`video/output/` 是 gitignored。

`storyboards/` 目前只餘 `_demo_*.yml` 模板示範／回歸樣本；逐節正式 storyboard 於重跑時依方法論產生。

已實作的可重用模板：

- **`intro`**：可重用的 Section Gate 開場。流程：章節地圖、聚焦至當前
  節、logo／節／標題／slogan 字卡，接著一段短暫的暗場交接，再進入第一個
  教學場景。使用 `meta.chapter`、`meta.chapter_title`、
  `meta.sections`、`meta.section`、`meta.title`，以及選用的 `tagline`。
- **`graph_focus`**：供以圖形為中心的解說使用的暗色教學框。它支援繪製
  函數、輔助線、點、標籤、註解，以及 safe-zone 適配，使圖形不與標題或文字
  碰撞。
- **`outro`**：可重用的節末模板。**兩段式**：暗轉亮的橋接，接著由
  `meta.section` 與 `meta.title` 產生的最終 logo 字卡。**Key Takeaways 不在
  outro**——它在前一個 `recap_cards` 教學場景（有旁白）。僅在需要時透過
  `end_slate` 覆寫。
- **`derivation`**（2026-06-11 新增）：全寬多行推導鏈，服務連續代數變形
  （導數定義計算、極限律改寫、恆等式證明）——「敘述進旁白、畫面全寬給
  數學」。逐行揭示（`{show line.N}`），後續行的關係符對齊到首行同一欄
  （`align_on`，預設 `=`）；`anim: highlight` 標結果行。與左右並列模板的
  選用判準、容量上限見 [DESIGN.md](DESIGN.md)「Template selection」；demo
  稿 `storyboards/_demo_derivation.yml`。

目前生效的設計決策：

- intro/outro 使用淺色紙張底；教學場景使用暗色藍圖底。
- 因為底色變化在視覺上很大，intro 以一段暗場交接作結，outro 以一段暗轉亮
  的橋接開場。
- **場景間過渡：** compose 階段每個場景邊界淡出黑場再淡入（`make.py --transition`，
  預設每側 ~0.2s），全片開頭從黑淡入、結尾淡出到黑——比照 intro/outro 的暗場交接，
  消除教學場景硬切的突兀。`--transition 0` 回復硬切。
- 節末回顧（`recap_cards`）刻意不放 logo；logo 只出現在 intro/outro 的品牌字卡上。
- 章節地圖在 Section Gate 之前。地圖讓學生定位；gate 宣告當前的節。
- 預期沒有章節會超過 10 節，因此目前的地圖版面是圍繞該上限設計的。

**最快：用 `make.py` 跑一支 mock 成片**（單一 orchestrator：parse → synth（mock 靜音）→ render → compose，全程不計費）：

```powershell
python video\make.py --storyboard video\storyboards\<deck>.yml --scene all --quality low --backend mock
```

只跑部分場景（`--scene` 接單一 id、`a,b,c` 或 `all`）：

```powershell
python video\make.py --storyboard video\storyboards\<deck>.yml --scene intro --quality low --backend mock
python video\make.py --storyboard video\storyboards\<deck>.yml --scene <scene_id> --quality low --backend mock
```

> 真旁白路線是 **MiMo**（`tts.py --backend mimo` → `make.py --reuse-audio`），見下方專節。`make.py` 本身只跑 mock、刻意不接計費路徑（見 [`CLAUDE.md`](../CLAUDE.md)）。

離線時序／manifest 檢查（寫出與 TTS 輸出同形狀的無聲 WAV，不計費）：

```powershell
python video\pipeline\tts.py --storyboard video\storyboards\<deck>_mimo.yml --backend mock
```

產生的音訊／manifest 存於 `video/output/ch<NN>/s<X.Y>/audio_mimo/`。

manifest 為每 reveal beat 記一個 WAV、每內容場景記一個串接旁白 WAV；intro/outro 為無聲條目（`bgm` 占位、待 BGM 回合）。`video/output/` 為 gitignored。內容場景長度由旁白音訊驅動（每 beat 影片長度＝該 beat 音檔長度）；intro/outro 由 `duration` 加動畫時間決定。**完整有聲成片走下方「MiMo 旁白／影片路線」**（`tts.py --backend mimo` → `make.py --reuse-audio`）。

**自動守門員**（`make.py` render 前依序執行；兩級 **error 擋下 / warn 提示**）：

- `pipeline/schema.py` — error：meta.id/section 缺、scene kind 不合法、id 重複、content 缺 template/say、`{show}` 不閉合；`--list` 另印每場 reveal 目標。
- `pipeline/lint.py` — error：純文字欄含標記、`$` 不平衡；warn：散文手動 `\\`、空心點畫在曲線上。
- `pipeline/sizecheck.py` — error：並排散文字級不一致、元素出框；warn：教學散文用 `muted`、超安全邊界、content 區塊重疊。

**解析度慣例**：測試／預覽用 1080p（`make.py --quality high`，預設），正式交付才 4K（`--quality 4k`，依 `meta.video`，未設預設 4K60）。版面與解析度無關，1080p 測試與 4K master 構圖逐像素相同。

**仍待**：intro/outro 的 BGM 來源／授權／ducking；視覺方向定後為 intro/outro 做最終節奏調整；`{show}` target-vs-payload 交叉驗證（task #6，需 manim）。

## MiMo 旁白／影片路線（口語雙版 · single-source · 2026-06-14）

MiMo（小米 `mimo-v2.5-tts`，公測免費、OpenAI 相容、與 `critic.py` 共用 `MIMO_API_KEY`）是**唯一**
真旁白路線，但它**不讀 inline LaTeX**，需要「數學攤成口語」的旁白。此路線從**單一源**
`content_scripts/<deck>.spoken.yml`（口語＋`{show}` 標記）派生兩件產物，杜絕手抄 drift。
（內容稿正典 narration 仍內嵌 LaTeX，供閱讀版與 storyboard `say`；口語攤平只發生在本路線。）

```powershell
# 由 spoken.yml + 正典 storyboard 生成 _mimo.yml（影片用）+ _narration_spoken.md（閱讀用）。
# --check：守 parity（scene/{show} 結構與正典 <deck>.yml 一致、口語無 $），不寫檔。
python video\pipeline\derive_spoken.py --deck <deck> --check
python video\pipeline\derive_spoken.py --deck <deck>

# 合成 beat 級真 MiMo 音訊（邊緣靜音自動裁）＋ render（reuse 真 manifest、不碰計費 gate）。
$env:MIMO_API_KEY = "<key>"   # 或放 .env；批次合成前依 CLAUDE.md 報用量、徵同意
python video\pipeline\tts.py  --storyboard video\storyboards\<deck>_mimo.yml --backend mimo --voice Mia
python video\make.py          --storyboard video\storyboards\<deck>_mimo.yml --reuse-audio --quality high
# → output/<deck>_mimo.mp4
```

- `tts.py --backend mimo`：OpenAI 相容 `/chat/completions`，待唸文字放 `assistant`、風格放 `user`；預設 `MIMO_VOICE=Mia`、`MIMO_STYLE`＝YouTube 科普風（正常語速）；`MimoTTSBackend` 預設裁 beat 頭尾靜音（留 0.08s）。新 manifest 會記錄每 beat 的 `raw_audio_seconds`、`trimmed_audio_seconds`、`trimmed_silence_seconds`，方便追查 MiMo padding/裁切。
- `make.py --reuse-audio`：跳過 mock synth、直接讀 `tts.py` 的真 manifest render。非 reuse 但偵測到真 manifest 會**拒絕用 mock 覆蓋**；reuse 時也會 fail fast 檢查 deck id、scene、beat count、`{show}` target、`text_hash`、WAV 存在與 WAV 時長，避免 storyboard 改了卻沿用舊 take。
- 同步 guard：`make.py` render 前會警告短 beat / reveal-only beat（例如連續 `{show a} {show b}` 造成 0.45s 靜音 beat，但 reveal 動畫本身較長）；render 後會用 ffprobe 檢查每個 content scene 的 video 長度是否足以容納 `lead + narration`，並提示 video 與 `lead + audio + tail` 的偏差。
- 同步常數集中在 `pipeline/timing.py`：`SCENE_LEAD_SECONDS` 同時供 `scene.py`、`make.py`、`critic.py` 使用，避免 compose offset / critic 抽幀時間與實際場景 lead 漂移。
- 只想聽聲音不要影片：`python video\pipeline\mimo_preview.py --spoken <..._narration_spoken.md>`（逐單元串成 `preview.wav`；`--dry-run` 不呼叫 API、`--smoke` 只合首段）。
- **MiMo 非決定性**：同文字每次合成是不同 take（±~10% 長度），重跑不保證同長度；要鎖定某 take 就別重合成。
- 念法慣例（`f inverse` 不念 reciprocal、`x sub one`、和/差根號加 “the quantity”、座標 “the point with coordinates a and b”…）見生成的 `_narration_spoken.md` §2，或 NFA 契約 `content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md`（旁白忠實稽核，原 Mode B）。

## 文字渲染（避免亂碼）

畫面上的字走兩條渲染路徑，**兩者都是 Computer Modern，但 manim 對相同 `font_size`
的呈現大小不同**（`Text` 約比 `Tex` 大 1.34 倍，已由 `theme.TEX_TEXT_SCALE` 校準對齊）：

- **`Text`（Pango，OTF 字型）** —— 純文字，**不認得 LaTeX**。`$f$`、`\\` 會被原樣印出（亂碼）。
- **`Tex` / `MathTex`（LaTeX）** —— 認得 inline `$math$` 與 `\\` 換行。

> **鐵則:任何作者可能填入 `$` 或 `\` 的散文／標題欄位，模板一律用 `brand.prose`
> 或 `brand.heading_rich` 渲染，不要直接用 `body_text` / `heading`。**

這兩個共用渲染器會依內容自動路由（有標記→Tex，否則→可換行的 Text），是「Text vs Tex」
判斷的**唯一**決策點。`math:` / `formulas:` 等純數學欄位仍走 `brand.math_line`。

render 前會自動跑 lint 擋下亂碼（純文字欄位含標記、不平衡的 `$`）；也可獨立執行：

```powershell
python video\pipeline\lint.py video\storyboards\<deck>.yml
# make.py 預設自動 lint；--skip-lint 可跳過
```

## VLM 視覺批改（critic.py）

render 後的視覺 QA（視覺 **gate 2**）：抽每場景最滿的一幀，送 vision 模型（MiMo-V2.5）依
**[VISUAL-FRAME-RUBRIC.md](content_scripts/_audit/VISUAL-FRAME-RUBRIC.md)** 判定——runtime
**verbatim-inject 整份 rubric body**，輸出 **V1–V8 blocking findings＋`VERDICT` 行＋A1–A7 0–100
magnitude** 與具體缺陷。**純建議**——只寫報告
`output/ch<NN>/s<X.Y>/critic/critique.{json,md}`，不改 storyboard；採納與否由人判斷。

```powershell
# 免費：抽幀 + 印出要送的計畫／prompt／估算，不呼叫 API
python video\pipeline\critic.py --storyboard video\storyboards\<deck>.yml --dry-run

# 計費：真送 VLM。key 走環境變數（不要當參數、不要寫進檔／git）。
$env:MIMO_API_KEY = "<your key>"
python video\pipeline\critic.py --storyboard video\storyboards\<deck>.yml --scene all --confirm
```

- **`--per scene`（預設）** 每場景抽**最滿幀**；`--per beat` 每 beat 一張（看漸進、較貴）。
- **MiMo-V2.5 公測免費（估值＝$0）**，但仍屬外部 API，依 [CLAUDE.md](../CLAUDE.md) 批次前須先報量徵同意；`--dry-run` 看幀數＋token 量（不送請求）。
- provider＝小米官方 `api.xiaomimimo.com/v1`（OpenAI 相容、model `mimo-v2.5`、auth header `api-key`）。
- **A1 Element Layout / V2 相撞** 要特別看 graph label：`$y=f(x)$`、`$y=x$`、座標標籤等不可壓在線、點、空心點或 guide marker 上（蓋住資訊＝V2 blocking）；這類圖內 label collision 即使 `sizecheck` 不一定自動抓到。

**迭代驗證迴圈**（完整見 [DESIGN.md](DESIGN.md)「The review loop」）：

1. **批改** —— 跑 critic，讀分數 + defects + 建議。
2. **判斷採納** —— 由你決定哪些採納。**不限於 bug**：凡你判斷能讓影片更好的建議都採納
   （清晰度、節奏、教學）；只有會傷跨場景一致性、或撞既有設計決定（刻意扁平無格線、
   刻意保留的字級）的才不採。**有爭議的（兩面都說得通、或屬作者本人該拍板的設計取捨）
   就交人工定奪，別自己決定。** VLM 提案、你定奪、拿不準的往上拋。
3. **修改** —— 改 storyboard／模板，重渲該場景。
4. **再驗** —— **再用 VLM 跑一次那張幀**，確認該 defect 消失、沒冒新的。抓 bug 的判官
   親自確認修掉，光人眼不算數。
5. **最後檢查** —— 你自己看一遍。
6. **迭代** —— 重複到 critic 沒有值得採納的建議為止。

## 工程鏡 cross-review（review_pack.py）

critic.py 的**文字版姊妹**，**2026-06-16 收斂為 engineering 鏡專用、改兩讀者、退場 DeepSeek**：critic.py 把 render 出來的**幀**送 VLM 抓視覺缺陷；review_pack.py 把**生成的 hook code**＋animation_cue 意圖＋它該畫的數學**組成一個 packet**，供工程鏡審——抓守門員與 VLM 結構上看不到的：生成動畫 code 的數學／慣例錯（座標／反射／端點在 code 裡畫錯、但畫面看起來還行）。與 VISUAL-FRAME **V8 邊界**配對：V8 查幀上可見數學、本鏡查生成它的 code。

> **為何只剩一鏡＋退場 DeepSeek：** 原 `faithfulness`／`register`／`decomposition` 三鏡已被 **CONTENT-SIXLENS**（L1–L6 multi-agent 對抗式稽核）取代，保留即「平行第二套」；故移除。剩下唯一非冗餘的 engineering 鏡改走與其餘判斷閘一致的**兩讀者**：**gate1 Claude subagent（免費）／gate2 Codex（計費、收斂後單次）**，不再用 DeepSeek。math context 改吃內容稿動畫單元的 narration／`source`（不依賴已搬 `legacy/` 的 `.tex`）。

`review_pack.py` 現在是**離線 packet 組裝器**（無 API、無 key）：組好 packet（rubric verbatim ＋ hook code ＋ cue ＋ math context）寫到檔，交給讀者。

```powershell
python video\pipeline\review_pack.py --storyboard video\storyboards\<deck>.yml
# → output/ch<NN>/s<X.Y>/review/engineering-packet.md
```

- **gate1**：把 `engineering-packet.md` 交給 Claude subagent（免費），對照 [`HOOK-ENGINEERING-RUBRIC.md`](content_scripts/_audit/HOOK-ENGINEERING-RUBRIC.md)（packet 已內嵌該 rubric）判定——E1 數學保真（blocking）＋E2 慣例；收斂＝engineering blocking==0。
- **gate2**：收斂後 Codex 單次確認（計費，依 [CLAUDE.md](../CLAUDE.md) 徵同意），比照 NFA／copyedit。
- **需要 `video/animations/<deck>_hooks.py`** 且有 animated unit；否則自動跳過（印訊息）。
- **純建議**：packet 唯讀，findings 交回人裁決，不改 content script／storyboard／hook code。

**過濾紀律（實測重要）**：模型自我 triage 不可盡信，依 CLAUDE.md 四級紀律過濾（§1.1 四-lens 舊跑 28 calls／7 actionable，過濾後真正可動約 1.5 條，其餘過度 triage 成 L1、甚至 1 條幻覺）。模型提案 → 你裁決 → 改 hook code（收斂後重生動畫）→ 有爭議往上拋。

## 踩過的坑（接 VLM 批改學到的）

- **MiMo-V2.5 是推理模型**：completion token 先被隱藏 reasoning 吃掉，`max_completion_tokens`
  太小（1200）→ `content` 回空、JSON 解不出。設 8000；計費看實際用量，高上限不額外花錢。
- **VLM 回的 JSON 內嵌 LaTeX**（`\sqrt`、`\to`），單一反斜線是非法 JSON escape →
  `json.loads` 掛。`critic.py` 解析會把非法反斜線跳脫後重試。
- **逐 beat 抽幀會誤判**：reveal 沒鋪完的中途幀看似「空／失衡／死板」，被當成品扣分。
  預設抽**每場景最滿幀**才準。
- **VLM 建議要過濾、不照抄**：它建議過出界座標的點，也會（違反刻意扁平的設計）要你加
  漸層／格線。prompt 已註明風格扁平以壓制，仍要人判斷。
- **測試解析度用 1080p**：夠清楚判細節（實心 vs 空心點、小下標），又貼近多數 VLM 內部
  downscale 的天花板；直接送 4K 給 VLM 多半浪費 token。
- **render 媒體會 stale**：換機或改 code 後 `output/` 的 mp4 可能是舊版；視覺批改前先用
  當前 code 重渲。
- **`graph_focus` 的斜線標籤**：對角線（如 `y=x`）用 `label_side` 會落在 bbox 邊（y 軸頂）；
  斜線要用 `label_point` 指定座標。

## 環境

重量級依賴（`manim` 0.20.1、`PyYAML`）內嵌於儲存庫根目錄的
`.deps_voiceover` / `.deps`，由 `pipeline/_bootstrap.py` 接上 `sys.path`。

> ⚠️ **這兩個 `.deps*` 目錄是 gitignored —— 新 clone 的機器不會有它們。**
> 換電腦時 `import manim/yaml` 會直接失敗。若它們不在,改建一個本機 venv
> （與 `.deps*` 互不影響,`_bootstrap` 找不到 `.deps*` 時就用 venv 的套件）。

> ⚠️ **環境依機器而定——換機後先驗證、別照搬（使用者常換電腦）。** 各機差異大，**跑前先驗一遍**：`.venv\Scripts\python -c "import yaml, manim"` 與（PowerShell）`Get-Command ffmpeg, ffprobe`。
>
> **本次這台（2026-06-17 實測）：**
> - **用 repo 根的 `.venv`（`.venv\Scripts\python.exe`）跑整條產線**——它有 **manim 0.20.1 ＋ PyYAML 6.0.3**。**全域 `python`（Python 3.12）有 manim 但缺 PyYAML**，故 `python video\make.py …` 會在 `import yaml` 直接掛（本次首跑就是這樣失敗）。MiKTeX（`latex`／`dvisvgm`）在 PATH、可用。
> - **`ffmpeg`／`ffprobe` 都不在 PATH**（連 PowerShell 也 NOT FOUND）。manim render 靠 `.venv` 內 bundled 的 `imageio_ffmpeg` 自帶 ffmpeg，所以**場景 mp4 照常 render**；但 `make.py` 的 compose／`_audit_render_sync` 與 `critic.py` 是用**裸名** `ffmpeg`／`ffprobe` 呼叫——`.venv\ffmpeg_shim\ffmpeg.exe`（真 ffmpeg 7.1）補得了 `ffmpeg`，**但 `ffprobe` 整台都沒有**。後果：(a) mock render 的 19 個場景 mp4 OK；(b) `make.py` 在 render 後的 ffprobe 時長健檢（`_audit_render_sync`）崩、**compose 沒跑→沒有合併成片**；(c) `critic.py --dry-run`（`per=scene` 靠 ffprobe 取時長算最末幀時刻）抽不到幀。
> - **抽幀繞法（本次採用，免 ffprobe）：** 直接用 shim ffmpeg 從檔尾回退抓場景 mp4 最末（最滿）幀：`.venv\ffmpeg_shim\ffmpeg.exe -sseof -0.4 -i <scene>.mp4 -frames:v 1 -q:v 2 <out>.png`。輸出落在 `output/ch01/s1.1/critic/frames/NN_<scene_id>/final.png`（與 critic.py 同位）。
> - **待補（合併成片／真 critic 前的 blocker）：** 要產合併片（含 MiMo 成片）或跑 `critic.py` 都需要 `ffprobe`。imageio_ffmpeg／shim 只給 ffmpeg、**不含 ffprobe**；屆時需在 PATH 放一個真 `ffprobe.exe`（完整 ffmpeg 套件），或把 `make.py`／`critic.py` 的 `_probe_duration`／`_ffprobe_duration` 改用 shim ffmpeg 探時長。

**換新電腦的一次性設定**（`.deps*` 不存在、且全域 python 也沒有 manim 時）:

```powershell
# 1) 建 venv 並裝 pinned 依賴
python -m venv .venv
.venv\Scripts\python -m pip install -r video\requirements.txt

# 2) make.py 的 compose 階段直接呼叫 `ffmpeg`,需在 PATH 上。若無系統 ffmpeg,
#    用 imageio-ffmpeg 自帶的二進位做一個 shim（一次即可）:
$src = .venv\Scripts\python -c "import imageio_ffmpeg as f; print(f.get_ffmpeg_exe())"
New-Item -ItemType Directory -Force .venv\ffmpeg_shim | Out-Null
Copy-Item $src .venv\ffmpeg_shim\ffmpeg.exe
```

**之後每次執行**（把 shim 加進 PATH,用 venv 的 python）:

```powershell
$env:PATH=".venv\ffmpeg_shim;$env:PATH"
.venv\Scripts\python video\make.py --storyboard video\storyboards\<deck>.yml --backend mock --quality low
```

（系統若已有 `ffmpeg` 在 PATH,可略過 shim。`.venv` 與 `.venv\ffmpeg_shim`
本身不進版控。）

MiMo TTS（唯一旁白路線）透過 `--voice`（預設 `Mia`）使用平台預設語音；key 走
env `MIMO_API_KEY`（公測免費，仍屬外部 API，依 CLAUDE.md 批次前徵同意）。TTS CLI
亦有 `--backend mock`，不需網路／API 金鑰，適合驗 manifest 與改模板時的快速無聲預覽。

Render 註記：

- `make.py` 的 render 階段算出的每場景 MP4（在 `output/_media/`）為無聲；compose
  階段才把對應小節旁白混進去、concat 成有聲成片 `output/ch<NN>/s<X.Y>/<id>.mp4`（真旁白走 MiMo route）。
- intro/outro 仍為無聲；分鏡中的 `bgm` 欄位是占位符，待 BGM 回合。
- 無聲預覽 render 期間可能出現 `SoX could not be found` 警告；對目前的
  檢查點而言它是無害的。
- 若 sandbox 阻擋了對內嵌依賴的存取，請以正常的專案權限重新執行 Manim
  render 指令。

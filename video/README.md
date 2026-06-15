# video/ 課程影片產線（第二代）

將一節 HTML 講義（handout kit）轉成一支帶旁白課程影片的單一進入點。取代第一代的
`tools/manim_*` 產線（現已凍結）。

- **改了什麼、為什麼：** [DESIGN.md](DESIGN.md)
- **輸入：** HTML 講義（handout kit，[`../handout/`](../handout/)）的各節（由人閱讀、手寫產出內容稿）。**各章權威檔**——ch01：[`chapter1-print-standalone.html`](../handout/chapter1-print-standalone.html)（2026-06-10 拍板；原 `chapter1-standalone.html`，2026-06-13 重組後改此名，編輯源在 `fragments/ch01/sec-*.html`）；ch02+ 屆時在此補。2026-06-10 前的輸入源為 `../chapters/*.tex`（已換源，§1.1/§1.6 原型基於它）。
- **輸出：** `output/`（gitignored）

## 結構

```
video/
  README.md            你在這裡
  DESIGN.md            格式 + 資料流契約（先讀這個）
  make.py              單一入口 orchestrator：parse → synth → render → compose（離線、不計費）
  pipeline/
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
    critic.py          render 後 VLM 視覺批改（抽幀 → MiMo-V2.5 → 建議報告；計費）
    tts.py/build.py/mux.py   gen-2 舊底層三步（被 make.py 取代，僅真 Gemini 旁白計費路徑仍用）
  storyboards/
    ch01_inverse_functions.yml        §1.1（16 場景；Gemini／MiMo 雙版）
    ch01_inverse_trig.yml             §1.2（18 場景；MiMo storyboard 已派生，輸出待補 scene）
    ch01_limit_of_function.yml        §1.3（11 場景；mock preview／MiMo storyboard 已完成）
    ch01_one_sided_infinite.yml       §1.4（16 場景；no-audio preview 已完成）
    ch01_limit_laws.yml               §1.5（19 場景；per-scene mock 已完成，full compose 待補）
    ch01_precise_limit.yml            §1.6（舊 16 場景；新內容稿 drift repair 中）
  output/              render 成品（gitignored），按章節小節歸類：
    ch01/
      s1.1/            §1.1 成品——mp4、audio/、audio_mimo/、critic/
      s1.2/            §1.2
      ...
    _media/            manim per-scene render 快取（pipeline 內部用）
```

## 狀態

**目前檢查點（2026-06-14）：第一章各節工程進度已重新校準；細節以 [REBUILD_STATUS.md](REBUILD_STATUS.md) 為準。**

- §1.1：Gemini Charon 旁白 master 與 MiMo 口語版皆已產出；待 AV review／critic／4K。
- §1.2：內容稿、storyboard、MiMo spoken、Mode B 已完成；`output/ch01_inverse_trig.mp4` 仍是 partial，需補 `when_arcsin_sin_breaks` 後 full compose。
- §1.3：內容稿、11-scene storyboard、mock preview、MiMo spoken、Mode B 已完成（commit `cb98ebf`）；旁白仍待使用者正式認可，MiMo TTS 尚未跑。
- §1.4：內容稿與 16-scene no-audio preview 完成；目前以 `output/ch01_one_sided_infinite_preview.mp4` 為審看檔，正式 spoken／MiMo 尚未開始。
- §1.5：內容已認可，19-scene storyboard 與 per-scene mock 完成；頂層 mp4 仍是 partial，下一步是 full compose 與 spoken／Mode B。
- §1.6：舊 16-scene ε-δ mock 可作歷史參考；新 HTML drift repair 已進內容稿，storyboard 尚未同步到新版 19 單元。

`video/output/` 是 gitignored，頂層 mp4 可能是舊 compose 或 partial；判讀完成度請先看本段與 [REBUILD_STATUS.md](REBUILD_STATUS.md)，不要只看檔名。

前一檢查點（2026-06-11）：正式 hook 機制落地＋§1.1 四個客製動畫接入。
場景級 `hook:` 欄（契約見 [DESIGN.md](DESIGN.md) content scene fields）讓客製
manim 動畫接進 make.py 產線、與音訊驅動的 beat 對齊共存；§1.1 的四段動畫
（兩進一出映射、雙圖水平線 sweep、A↔B 往返、沿 $y=x$ 翻摺）已生成接入
（[animations/ch01_inverse_functions_hooks.py](animations/ch01_inverse_functions_hooks.py)），
待使用者過目認可。全寬推導鏈模板 `derivation` 同期上線（見上方模板清單）。

前一檢查點（2026-06-10）：輸入換源至 HTML 講義（見上方「輸入」；決策記錄見
[REBUILD_STATUS.md](REBUILD_STATUS.md)「2026-06-10 輸入換源」）。§1.1 以新源
**從零重走**（內容稿 v2；舊 §1.1 成品為方法論校準原型、已棄用）。以下 2026-06-02
檢查點所述的工具鏈與 mock 成片仍有效。

前一檢查點（2026-06-02）：端到端產線打通，並加上 render 前守門員（lint /
sizecheck）與 render 後的 VLM 視覺批改（critic.py）。兩節皆可端到端 render：

- `storyboards/ch01_inverse_functions.yml` —— §1.1（16 場景）
- `storyboards/ch01_precise_limit.yml` —— §1.6（16 場景，symbol-heavy ε-δ）

§1.1 已實證整節真旁白（Gemini TTS）成片；旁白與揭示動畫對齊（每 beat 影片長度
＝該 beat 音檔長度）。mock 路徑（`make.py --backend mock`）離線、不計費，用於
版面／時序／視覺迭代。

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
python video\make.py --storyboard video\storyboards\ch01_inverse_functions.yml --scene all --quality low --backend mock
```

只跑部分場景（`--scene` 接單一 id、`a,b,c` 或 `all`）：

```powershell
python video\make.py --storyboard video\storyboards\ch01_inverse_functions.yml --scene intro --quality low --backend mock
python video\make.py --storyboard video\storyboards\ch01_inverse_functions.yml --scene why_x_squared_fails --quality low --backend mock
```

> 下面的 `tts.py` / `build.py` / `mux.py` 是 gen-2 的底層三步，已被 `make.py` 取代（保留未刪）。**只有真 Gemini 旁白（計費）仍走這三步**——`make.py` 刻意不接計費路徑（見 [`CLAUDE.md`](../CLAUDE.md)）。

合成 beat 音訊：

```powershell
# 離線時序／manifest 檢查：寫出與 TTS 輸出形狀相同的無聲 WAV 檔。
python video\pipeline\tts.py --storyboard video\storyboards\ch01_inverse_functions.yml --scene all --backend mock

# 使用模型內建預設語音的 Gemini TTS。不使用語音克隆或參考音訊；
# `--voice` 選擇模型內建的語音名稱。
$env:GEMINI_API_KEY = "<your key>"
python video\pipeline\tts.py --storyboard video\storyboards\ch01_inverse_functions.yml --scene all --backend gemini --model gemini-3.1-flash-tts-preview --voice Charon
```

產生的音訊存於（按章節小節歸類）：

```text
video/output/ch01/s1.1/audio/          # Gemini 音訊
video/output/ch01/s1.1/audio_mimo/     # MiMo 音訊
```

manifest 為每個 reveal beat 記錄一個 WAV，並為每個內容場景記錄一個串接
後的旁白 WAV。intro/outro 為無聲條目；其 `bgm` 欄位是占位符，待 BGM 回合。

組裝成有聲成片（旁白混進各場景、concat 成一支）：

```powershell
python video\pipeline\mux.py --storyboard video\storyboards\ch01_inverse_functions.yml
```

`mux.py` 把每個內容場景的旁白用 `-itsoffset` 延遲、對齊到首次揭示，混到該場景
影片底下；intro/outro 給靜音軌；再 concat 成 `output/<chNN>/<sX.Y>/<storyboard-id>.mp4`。
`build.py` 會自動讀 manifest 的每 beat 音長來驅動 reveal 時序，所以三步接起來
就是完整有聲產線：

```powershell
# 完整一節有聲影片（合成 → render → 組裝）
python video\pipeline\tts.py   --storyboard video\storyboards\ch01_inverse_functions.yml --scene all --backend gemini --reuse-existing
python video\pipeline\build.py --storyboard video\storyboards\ch01_inverse_functions.yml --scene all --quality low
python video\pipeline\mux.py   --storyboard video\storyboards\ch01_inverse_functions.yml
```

最近檢查過的預覽存於：

```text
video/output/_media/videos/480p15/
```

`video/output/` 為 gitignored。內容場景的長度由旁白音訊驅動（每 beat 影片
長度＝該 beat 音檔長度）；intro/outro 無旁白，長度由 `duration` 加動畫累加
時間決定，故預覽可能比 `duration` 略長，待視覺模式核可後再收緊。

已完成：

- ✅ 以音訊時長驅動的 reveal 時序（`build.py` 讀 manifest、`scene.py` 以每 beat 音長為牆鐘）；
- ✅ 以 ffmpeg mux/concat 成一支有聲最終 MP4（`mux.py`）。
- ✅ 自動守門員（`make.py` render 前執行,兩級:**error 擋下 / warn 只提示**）:
  - `pipeline/lint.py` — error:純文字欄含標記、`$` 不平衡;warn:散文手動 `\\`、空心點畫在曲線上。
  - `pipeline/sizecheck.py` — error:並排散文字級不一致、元素出框;warn:教學散文用 `muted`(太淡)、超出安全邊界、兩個 content 區塊重疊。
- ✅ 解析度慣例：**測試／預覽用 1080p**（`make.py --quality high`，預設），**正式交付才用 4K**（`--quality 4k`，依 `meta.video`，未設時預設 4K60＝3840×2160@60，manim fourk_quality）。版面與解析度無關，1080p 測試與 4K master 構圖逐像素相同，只差取樣密度與 render 時間。

仍待處理：

- schema 驗證作為獨立指令（lint 已完成，見下方「文字渲染」）；
- intro/outro 的 BGM 來源／授權／ducking；
- 視覺方向確定後，為可重用的 intro/outro 做最終節奏調整。

## MiMo 旁白／影片路線（口語雙版 · single-source · 2026-06-14）

Gemini 能直讀 inline LaTeX；MiMo（小米 `mimo-v2.5-tts`，公測免費、OpenAI 相容、與 `critic.py`
共用 `MIMO_API_KEY`）**不能**，需要「數學攤成口語」的旁白。此路線從**單一源**
`content_scripts/<deck>.spoken.yml`（口語＋`{show}` 標記）派生兩件產物，杜絕手抄 drift。

```powershell
# 由 spoken.yml + 正典 storyboard 生成 _mimo.yml（影片用）+ _narration_spoken.md（閱讀用）。
# --check：守 parity（scene/{show} 結構與正典 <deck>.yml 一致、口語無 $），不寫檔。
python video\pipeline\derive_spoken.py --deck ch01_inverse_functions --check
python video\pipeline\derive_spoken.py --deck ch01_inverse_functions

# 合成 beat 級真 MiMo 音訊（邊緣靜音自動裁）＋ render（reuse 真 manifest、不碰計費 gate）。
$env:MIMO_API_KEY = "<key>"   # 或放 .env；批次合成前依 CLAUDE.md 報用量、徵同意
python video\pipeline\tts.py  --storyboard video\storyboards\ch01_inverse_functions_mimo.yml --backend mimo --voice Mia
python video\make.py          --storyboard video\storyboards\ch01_inverse_functions_mimo.yml --reuse-audio --quality high
# → output/ch01_inverse_functions_mimo.mp4
```

- `tts.py --backend mimo`：OpenAI 相容 `/chat/completions`，待唸文字放 `assistant`、風格放 `user`；預設 `MIMO_VOICE=Mia`、`MIMO_STYLE`＝YouTube 科普風（正常語速）；`MimoTTSBackend` 預設裁 beat 頭尾靜音（留 0.08s）。新 manifest 會記錄每 beat 的 `raw_audio_seconds`、`trimmed_audio_seconds`、`trimmed_silence_seconds`，方便追查 MiMo padding/裁切。
- `make.py --reuse-audio`：跳過 mock synth、直接讀 `tts.py` 的真 manifest render。非 reuse 但偵測到真 manifest 會**拒絕用 mock 覆蓋**；reuse 時也會 fail fast 檢查 deck id、scene、beat count、`{show}` target、`text_hash`、WAV 存在與 WAV 時長，避免 storyboard 改了卻沿用舊 take。
- 同步 guard：`make.py` render 前會警告短 beat / reveal-only beat（例如連續 `{show a} {show b}` 造成 0.45s 靜音 beat，但 reveal 動畫本身較長）；render 後會用 ffprobe 檢查每個 content scene 的 video 長度是否足以容納 `lead + narration`，並提示 video 與 `lead + audio + tail` 的偏差。
- 同步常數集中在 `pipeline/timing.py`：`SCENE_LEAD_SECONDS` 同時供 `scene.py`、`make.py`、`mux.py`、`critic.py` 使用，避免 mux offset / critic 抽幀時間與實際場景 lead 漂移。
- 只想聽聲音不要影片：`python video\pipeline\mimo_preview.py --spoken <..._narration_spoken.md>`（逐單元串成 `preview.wav`；`--dry-run` 不呼叫 API、`--smoke` 只合首段）。
- **MiMo 非決定性**：同文字每次合成是不同 take（±~10% 長度），重跑不保證同長度；要鎖定某 take 就別重合成。
- 念法慣例（`f inverse` 不念 reciprocal、`x sub one`、和/差根號加 “the quantity”、座標 “the point with coordinates a and b”…）見生成的 `_narration_spoken.md` §2，或 Mode B 模板 `content_scripts/_audit/PROMPT-narration-modeB.template.md`。

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
python video\pipeline\lint.py video\storyboards\ch01_inverse_functions.yml
# make.py 預設自動 lint；--skip-lint 可跳過
```

## VLM 視覺批改（critic.py）

render 後的視覺 QA：抽每場景最滿的一幀，送 vision 模型（MiMo-V2.5）依五維
（見 [DESIGN.md](DESIGN.md) Visual QA）評分並列出具體缺陷。**純建議**——只寫報告
`output/ch<NN>/s<X.Y>/critic/critique.{json,md}`，不改 storyboard；採納與否由人判斷。

```powershell
# 免費：抽幀 + 印出要送的計畫／prompt／估算，不呼叫 API
python video\pipeline\critic.py --storyboard video\storyboards\ch01_inverse_functions.yml --dry-run

# 計費：真送 VLM。key 走環境變數（不要當參數、不要寫進檔／git）。
$env:MIMO_API_KEY = "<your key>"
python video\pipeline\critic.py --storyboard video\storyboards\ch01_inverse_functions.yml --scene all --confirm
```

- **`--per scene`（預設）** 每場景抽**最滿幀**；`--per beat` 每 beat 一張（看漸進、較貴）。
- **計費，依 [CLAUDE.md](../CLAUDE.md) 須先估算經同意**；`--dry-run` 先看幀數與估算（約 $0.001–0.002／幀）。
- provider＝小米官方 `api.xiaomimimo.com/v1`（OpenAI 相容、model `mimo-v2.5`、auth header `api-key`）。
- Element Layout 要特別看 graph label：`$y=f(x)$`、`$y=x$`、座標標籤等不可壓在線、點、空心點或 guide marker 上；這類圖內 label collision 是 critic finding，即使 `sizecheck` 不一定會自動抓到。

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

## 內容 cross-review（review_pack.py）

critic.py 的**文字版姊妹**：critic.py 把 render 出來的**幀**送 VLM 抓視覺缺陷；
review_pack.py 把**撰寫脈絡**（HTML 講義原文（節切片）、narration、單元拆解、生成的 hook code）
送另一個文字模型（DeepSeek），抓守門員與 VLM 結構上看不到的東西——忠實度漂移、
旁白書面腔、拆解問題、生成動畫 code 的數學／慣例錯。四個 lens：

| lens | 每次送什麼 | 對到 |
|---|---|---|
| `faithfulness` | 每單元 HTML 講義原文切片 ↔ narration | CONTENT_METHODOLOGY §1、§3 |
| `register` | 每單元 narration | CONTENT_METHODOLOGY §4 |
| `decomposition` | 整節單元的 kind/learning_goal | CONTENT_METHODOLOGY §3、§5 |
| `engineering` | 生成 hook code + animation_cue + HTML 講義數學 | DESIGN authoring checklist |

成本閘門與 critic.py 相同：免費組 packet + `--dry-run`（寫 packet、印 token 估算、不連網）；
計費呼叫走 `--confirm`，key 從環境變數 `DEEPSEEK_API_KEY` 讀——**不當參數、不寫檔、不進 git**。
**純建議**：寫報告 `output/ch<NN>/s<X.Y>/review/review.{json,md}`，不改 content script／storyboard，採納與否由人判斷。

```powershell
# 免費：組四層 packet、寫到 output/ch<NN>/s<X.Y>/review/packets/、印估算，不呼叫 API
python video\pipeline\review_pack.py --storyboard video\storyboards\ch01_inverse_functions.yml --dry-run

# 計費：真送 DeepSeek。key 走環境變數（依 CLAUDE.md 須先估算經同意）。
$env:DEEPSEEK_API_KEY = "<your key>"
python video\pipeline\review_pack.py --storyboard video\storyboards\ch01_inverse_functions.yml --confirm
python video\pipeline\review_pack.py --storyboard <yml> --confirm --smoke          # 只送第一個 packet（驗一發）
python video\pipeline\review_pack.py --storyboard <yml> --layers register,faithfulness   # 選 lens
```

- **provider**＝DeepSeek 官方 `api.deepseek.com`（OpenAI 相容、model `deepseek-v4-pro`、Bearer auth）。
- **`deepseek-v4-pro` 是推理模型**：completion 多半是 reasoning token（首跑實測 ~2.5k／call），故 out ≫ in、成本由 reasoning 驅動；`max_tokens` 設大（8000）避免截斷，計費看實際用量。
- **prompt 餵 house rules**（各 lens 的方法論 rubric）+ CLAUDE.md 四級 finding 紀律，壓掉「拿通用 prior 來審」的噪音。
- **engineering lens 需要 `video/animations/<deck>_hooks.py`**；沒有生成 code 的節（如 §1.2）自動跳過該 lens。

**過濾紀律（實測重要）**：模型的自我 triage 不可盡信——§1.1 首跑 28 calls、7 條 actionable，
人依四級紀律過濾後真正可動約 1.5 條（其餘過度 triage 成 L1、甚至 1 條幻覺）；decomposition 正確回 0。
所以**沿用 critic.py 的 review loop**：模型提案 → 你（或 Claude 在你簽核下）裁決 → 改 content script + storyboard（**同步**）→ 有爭議往上拋。推理模型 run-to-run 會飄，單跑一次不窮盡。

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

**換新電腦的一次性設定**（`.deps*` 不存在時）:

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
.venv\Scripts\python video\make.py --storyboard video\storyboards\ch01_inverse_functions.yml --backend mock --quality low
```

（系統若已有 `ffmpeg` 在 PATH,可略過 shim。`.venv` 與 `.venv\ffmpeg_shim`
本身不進版控。）

Gemini TTS 透過 `--voice` 使用模型的預設語音；它不使用語音克隆或參考音訊。
Gemini 後端另需安裝 `google-genai` 並具備 API 金鑰（計費，依 CLAUDE.md 需逐次
核可）。TTS CLI 亦有 `--backend mock`，它不需要網路／API 金鑰，適合用於驗證
manifest 與改模板時的快速無聲預覽。

Render 註記：

- `build.py` 算出的每場景 MP4（在 `output/_media/`）為無聲；`mux.py` 才把
  對應小節子資料夾的旁白混進去、concat 成有聲成片 `output/ch<NN>/s<X.Y>/<id>.mp4`。
- intro/outro 仍為無聲；分鏡中的 `bgm` 欄位是占位符，待 BGM 回合。
- 無聲預覽 render 期間可能出現 `SoX could not be found` 警告；對目前的
  檢查點而言它是無害的。
- 若 sandbox 阻擋了對內嵌依賴的存取，請以正常的專案權限重新執行 Manim
  render 指令。

# video/ 課程影片產線（第二代）

將一節 LaTeX 講義轉成一支帶旁白課程影片的單一進入點。取代第一代的
`tools/manim_*` 產線（現已凍結）。

- **改了什麼、為什麼：** [DESIGN.md](DESIGN.md)
- **輸入：** `../chapters/*.tex` 中的各節（由人閱讀、手寫產出）
- **輸出：** `output/`（gitignored）

## 結構

```
video/
  README.md            你在這裡
  DESIGN.md            格式 + 資料流契約（先讀這個）
  pipeline/
    assets/fonts/      在執行期註冊的內附設計字型
    visuals/           移植並驗證過的素材（colors、graph eval、layout）
    templates/         Direction B 場景模板
    blocks.py          可揭示的 Block 抽象 + 動畫派發
    brand.py           grid、字體排印、卡片、logo 與 motif
    narration.py       `{show ...}` 解析器 + 後備時長估計（無 manifest 時）
    audio.py           供 PCM 輸出、時長與串接用的 WAV 輔助程式
    tts.py             分鏡 beat 的 TTS CLI（Gemini 或離線 mock 後端）
    scene.py           所有模板共用的 Manim player（reveal 時序由音訊時長驅動）
    build.py           render CLI（讀 manifest，以每 beat 音長驅動 reveal 時序）
    mux.py             最終組裝 CLI：把旁白混進各場景、concat 成有聲成片
  storyboards/
    ch01_inverse_functions.yml   可運作的 8 場景 Section 1.1 預覽
  output/              render 出的成品（gitignored）
```

## 狀態

目前檢查點（2026-05-31）：端到端有聲路徑打通。Section 1.1 八個場景可
render，並經 `pipeline/tts.py` → `pipeline/build.py` → `pipeline/mux.py`
產出一支整節真旁白（Gemini TTS）的成片 `output/ch01_inverse_functions.mp4`；
旁白與揭示動畫對齊（每 beat 影片長度＝該 beat 音檔長度）。

可運作的分鏡：

- `storyboards/ch01_inverse_functions.yml`

已 render 的 scene id：

- `intro`
- `one_to_one`
- `testing_with_algebra`
- `why_x_squared_fails`
- `finding_an_inverse`
- `strictly_increasing`
- `recap`
- `outro`

已實作的可重用模板：

- **`intro`**：可重用的 Section Gate 開場。流程：章節地圖、聚焦至當前
  節、logo／節／標題／slogan 字卡，接著一段短暫的暗場交接，再進入第一個
  教學場景。使用 `meta.chapter`、`meta.chapter_title`、
  `meta.sections`、`meta.section`、`meta.title`，以及選用的 `tagline`。
- **`graph_focus`**：供以圖形為中心的解說使用的暗色教學框。它支援繪製
  函數、輔助線、點、標籤、註解，以及 safe-zone 適配，使圖形不與標題或文字
  碰撞。
- **`outro`**：可重用的節末模板。流程：暗轉亮的橋接、無 logo 的 Key
  Takeaways 回顧，接著由 `meta.section` 與 `meta.title` 產生的最終 logo
  字卡。僅在需要時透過 `end_slate` 覆寫。

目前生效的設計決策：

- intro/outro 使用淺色紙張底；教學場景使用暗色藍圖底。
- 因為底色變化在視覺上很大，intro 以一段暗場交接作結，outro 以一段暗轉亮
  的橋接開場。
- Key Takeaways 刻意不放 logo。logo 只出現在最終的結尾字卡上。
- 章節地圖在 Section Gate 之前。地圖讓學生定位；gate 宣告當前的節。
- 預期沒有章節會超過 10 節，因此目前的地圖版面是圍繞該上限設計的。

render 一份低畫質預覽：

```powershell
python video\pipeline\build.py --storyboard video\storyboards\ch01_inverse_functions.yml --scene all --quality low
```

render 單一場景：

```powershell
python video\pipeline\build.py --storyboard video\storyboards\ch01_inverse_functions.yml --scene intro --quality low
python video\pipeline\build.py --storyboard video\storyboards\ch01_inverse_functions.yml --scene why_x_squared_fails --quality low
python video\pipeline\build.py --storyboard video\storyboards\ch01_inverse_functions.yml --scene outro --quality low
```

合成 beat 音訊：

```powershell
# 離線時序／manifest 檢查：寫出與 TTS 輸出形狀相同的無聲 WAV 檔。
python video\pipeline\tts.py --storyboard video\storyboards\ch01_inverse_functions.yml --scene all --backend mock

# 使用模型內建預設語音的 Gemini TTS。不使用語音克隆或參考音訊；
# `--voice` 選擇模型內建的語音名稱。
$env:GEMINI_API_KEY = "<your key>"
python video\pipeline\tts.py --storyboard video\storyboards\ch01_inverse_functions.yml --scene all --backend gemini --model gemini-3.1-flash-tts-preview --voice Kore
```

產生的音訊存於：

```text
video/output/audio/<storyboard-id>/
```

manifest 為每個 reveal beat 記錄一個 WAV，並為每個內容場景記錄一個串接
後的旁白 WAV。intro/outro 為無聲條目；其 `bgm` 欄位是占位符，待 BGM 回合。

組裝成有聲成片（旁白混進各場景、concat 成一支）：

```powershell
python video\pipeline\mux.py --storyboard video\storyboards\ch01_inverse_functions.yml
```

`mux.py` 把每個內容場景的旁白用 `-itsoffset` 延遲、對齊到首次揭示，混到該場景
影片底下；intro/outro 給靜音軌；再 concat 成 `output/<storyboard-id>.mp4`。
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

仍待處理：

- schema/lint 作為獨立指令；
- intro/outro 的 BGM 來源／授權／ducking；
- 製作畫質的 1080p 匯出；
- 視覺方向確定後，為可重用的 intro/outro 做最終節奏調整。

## 環境

重量級依賴（manim 等）內嵌於儲存庫的 `.deps*` 下，並由
`pipeline/_bootstrap.py` 接上 `sys.path`。Gemini TTS 透過 `--voice` 使用
模型的預設語音；它不使用語音克隆或參考音訊。Gemini 後端另需安裝
`google-genai` 並具備 API 金鑰。TTS CLI 亦有 `--backend mock`，它不需要
網路／API 金鑰，適合用於驗證 manifest。

Render 註記：

- `build.py` 算出的每場景 MP4（在 `output/_media/`）為無聲；`mux.py` 才把
  `output/audio/` 的旁白混進去、concat 成有聲成片 `output/<id>.mp4`。
- intro/outro 仍為無聲；分鏡中的 `bgm` 欄位是占位符，待 BGM 回合。
- 無聲預覽 render 期間可能出現 `SoX could not be found` 警告；對目前的
  檢查點而言它是無害的。
- 若 sandbox 阻擋了對內嵌依賴的存取，請以正常的專案權限重新執行 Manim
  render 指令。

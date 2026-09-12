# reference_frames — YouTube 參考影片抓幀／拆解／對照表工具

> 2026-09-12～13 立。用途：把 YouTube 上的精緻教學影片逐幀拆解，對照我方 §3.1 的幀，產出
> [`../../content_scripts/_audit/REVIEW-reference-videos-A1A2B1C1.html`](../../content_scripts/_audit/REVIEW-reference-videos-A1A2B1C1.html)。
> 結論已寫進 [`../../SPEC-motion-language.md`](../../SPEC-motion-language.md)（五條畫面語法規則）。
> 這是實驗線工具，不碰成熟產線；每個腳本 dependency-free（Node ≥21、Chrome、Python 加 Pillow，都在 [`ENVIRONMENT.md`](../../../ENVIRONMENT.md) 既有清單內）。

## 檔案

| 檔 | 作用 |
|---|---|
| `yt_frames.mjs` | headless Chrome 走 CDP 開 YouTube 播放頁，seek 後把 `<video>` 畫到 canvas 存 JPEG。**不下載影片**（所以不觸「下載檔案要徵同意」那條）。改自 `handout/figkit/shot.mjs`。 |
| `sheet.py` | 把資料夾內的 `t_*.jpg`／`at_*.jpg` 拼成帶時間標籤的 contact sheet，給人或子代理用 Read 看。 |
| `page_shots.mjs` | headless Chrome 對本機 HTML 在數個捲動位置截圖（Browser pane 開不了 `file://` 時用來驗版面）。 |
| `build_html.py` | 讀 `<ID>/analysis.json`＋`ours/`＋`synthesis.html` 合成單檔 HTML（圖全內嵌 data URI）。 |
| `A1/ A2/ B1/ C1/analysis.json` | 四個子代理的拆解：每支 8 個時刻（秒數、畫面、手法、維度、對應我方場景、strip 檔名）、五維度總評、給我們的教訓。 |
| `synthesis.html` | 主代理綜合判定（HTML 片段，會嵌進對照表第 0 節）。 |
| `ours/meta.json` | 我方單場重渲動作條的來源檔與秒數（`video/output/ch03/s3.1/` 下的 per-scene mp4）。 |

**幀不進版控**（`.gitignore` 擋 `*.jpg`／`*.png`）：第三方影片截幀只供內部對照；`analysis.json` 帶每個時刻的秒數，隨時可重抓。

## 用法（Git Bash）

```bash
cd video/experiments/reference_frames
export CHROME='C:\Program Files\Google\Chrome\Application\chrome.exe'   # 一定要設；probe 找不到時會直接退出
# 1) 整段抽樣 → contact sheet（挑時刻用）
node yt_frames.mjs S0_qX4VJhMQ A1 sample 756 1016 8 640     # <videoId> <outDir> sample <start> <end> <step> [width]
python sheet.py A1 A1_sheet.jpg 6 320
# 2) 指定時刻抓三幀動作條（t−dt / t / t+dt）
node yt_frames.mjs S0_qX4VJhMQ A1/picks at 810,838,851 1280 1 0.6   # <videoId> <outDir> at <t1,t2,...> [width] [strip 0|1] [dt]
# 3) 我方幀：從 per-scene mp4 用 ffmpeg 抽（見 ours/meta.json 的檔名與秒數）
ffmpeg -ss 38.2 -i ../../output/ch03/s3.1/ch03_trig_derivatives_mimo__difference_quotient_for_sine.mp4 -frames:v 1 -vf scale=1280:-1 ours/difference_quotient_for_sine/at_00038.2_b.jpg
# 4) 合成
python build_html.py ../../content_scripts/_audit/REVIEW-reference-videos-A1A2B1C1.html
```

重抓四支影片全部 strip：對每份 `analysis.json` 取 `moments[].t`，用 `at` 模式、`1280 1 0.6`（B1 有幾組用 dt 0.4～1.0，見該檔 `strip` 檔名）。

## 已知行為（2026-09-12 實測）

- **YouTube 每約 10 次 seek 會卡住一次**（`readyState` 停在 1，接著播放器報錯）。腳本偵測到就 `Page.navigate` 帶 `&t=` 重載播放頁，stderr 印 `[retry …]`，屬正常；每支影片 1–3 分鐘。
- **同一支影片不要同時開兩個 node**；不同影片可平行（port 與 profile 依 pid 分開，四支同跑過）。
- 抓不到的情況：該秒正好插廣告（A1 的 t=820 三次都失敗），換相鄰秒數即可。
- 畫質：腳本會要 `hd1080`，`info.json` 記實際 `videoWidth`。抓到的是 canvas 像素，不含播放器 UI。
- 抓幀後 `_debug_*.jpg` 是 retry 時的整頁截圖副產品，可刪。
- Browser pane（Claude 內建瀏覽器）在沒有 project folder 時開不了 `file://`；驗 HTML 版面用 `page_shots.mjs`。

## 子代理分工（重現時照抄）

一支影片一個 general-purpose 子代理，prompt 要點：工具與用法如上；先 sample 再 Read sheet 挑 6–8 個「畫面正在動」的時刻；抓 strip 後 Read 確認三幀看得出動作，看不出就換時刻或加大 dt；`analysis.json` 只寫幀上看得到的證據、`dims` 只用五個固定詞（motion-language／cross-scene-continuity／visual-metaphor／layout-typography／sound-design）、`maps_to_ours` 只能選我方場景 id 或 null、不確定標「推測」、音效一律「未評估」。主代理逐組 Read picks sheet 核對描述後才進表。

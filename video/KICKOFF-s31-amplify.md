# KICKOFF — §3.1 放大：剩下的原語鋪滿 ＋ 場 08 ＋ 驗收

> **狀態（2026-09-13 收線）：Task A、B 完成，C 除獨立稽核外完成。** 21 個 content 場的
> `longest_still_seconds` 全部 ≤ 12 s（0.05% 門檻，見 §2「量測注意」）。commit：`8e1d5d5`（A）、
> `3fcbf6a`（B）。交付物＝[`content_scripts/_audit/REVIEW-ch03_s31-amplify-applied.html`](content_scripts/_audit/REVIEW-ch03_s31-amplify-applied.html)。
> **剩下的是 C-6 人閘**（看片裁決要不要進 Task D＝計費），以及 §7 的另案。
> 本輪多做的三件（都在 §4 之外）：原語 7 `paced:`、原語 1 補 `definition_math` 與 `scaffold.*`、
> `tts.py --no-billing`／`--max-billed-calls`（起因見 §1.1 的實測事故）。

> 2026-09-12 立檔，**交接用**。上一個對話的上下文快滿了，這份檔把「還沒做的事」全部寫下來，
> 好讓新 session 直接開工。§0 可整段貼進新對話當啟動提示；§2 是已驗證的 code 事實（免重查）；
> §3 起是任務。
>
> **前情**：本輪的裁決與已落地內容在 [`REBUILD_STATUS.md`](REBUILD_STATUS.md) 品質補強輪 ⑦–⑫；
> 首輪原語的 kickoff 是 [`KICKOFF-motion-primitives.md`](KICKOFF-motion-primitives.md)（已完成，
> 但它的 §1 成功定義已被 ⑧ 推翻，見該檔註記）；模板系統設計的依據是
> [`PROPOSAL-scope-packaging-coverage.md`](PROPOSAL-scope-packaging-coverage.md)。

---

## 0. 給新 session 的啟動提示（可整段貼）

> 讀 `video/KICKOFF-s31-amplify.md` 然後照它做。背景：§3.1 成片（16.2 分、27 場）經六份模型
> 盲審，問題集中在「畫面不會動」（content 場靜止 92–97%）。已經做完的是：六支 motion
> primitive 的機制、語意色軸對位講義、例題折疊宣告閘、以及場 06 的 beat 0 重構。**剩下的是把
> 原語鋪滿其餘場次、補場 08 的圖、然後驗收。** 全程零計費（mock render ＋ 現有 Dean 音檔
> reuse）；任何會動到旁白文字的事都要先停下來報量徵同意。中途不要停下來問，除非 §1 護欄被
> 觸發。做完一個 task 就跑 `python video/pipeline/run_selftests.py`。

---

## 1. 全域護欄

1. **旁白一個字不改。** 加減 `{show}` marker 本身不改 `scene_text_hash`，所以**可以**零計費重對映——
   但**必須把 `--reuse-existing` 下下去**，否則整批重合成。改一個字就要重 TTS＝計費。
   **2026-09-12 踩到的坑（代價 13 次 call）：** `tts.py:1054` 的
   `use_reuse = args.reuse_existing and …` 才會去建 reuse index；**漏了這個旗標，index 是空的、
   `scene_reuse_ok` 根本不會被問到**，5 場 hash 逐字未變的場全部從頭合成，其中 `sector_inequality`
   再掉到 beats 終端（`--fallback-budget` 只管 ladder rungs 2–3）。補上旗標後同一個 deck 實測
   `backend_calls: 0`。**正確指令：**
   `tts.py --backend mimo --reuse-existing --scene <ids> --no-billing`
   （`--no-billing`／`--max-billed-calls N` 是本輪新增的硬上限，涵蓋整個 run 含 beats 終端；
   中止時什麼都沒 promote，可安全重試。）
   另：`sector_inequality` 逐字母唸 `O A B`，ASR QA 探針會誤報 misspeak ⇒ 該場要加 `--skip-qa`。
   改完 marker 一定要：`derive_spoken.py --deck <deck> --check`（parity）→
   `derive_spoken.py --deck <deck>`（重生 `_mimo.yml`，不重生 `make.py` 會 STALE 拒跑）。
   **驗證 reuse 的正確方法**：`tts.py --dry-run` 的 planned counts **永遠報最壞情況、不看
   reuse**（表頭自己寫著 IGNORE），要驗就直接比 hash——見 §2「驗 TTS 零成本」。
2. **零計費**：mock render；真旁白只走 `--reuse-audio`；不開 agy／Codex／VLM／MiMo。
3. **零行為改變 for 其他 deck**：所有原語都是 opt-in（storyboard 欄位或 marker 才啟動）。
   驗收方式＝`python tools/doctor.py --smoke` 與改動前**逐字相同**（見 §2）。
4. **Karpathy 紀律**（根 `CLAUDE.md`）：最少 code、不加沒被要求的彈性、外科手術式修改、
   每個 task 先寫會紅的 selftest 再讓它綠。
5. **文檔同輪補齊**：`DESIGN.md`（新欄位／契約）、`README.md`、`REBUILD_STATUS.md`。
6. **卡住就停**：§2 的事實與實況不符、或設計撞上既有契約而需要改契約時，先寫下衝突再問
   使用者，不要默默繞。

### 本輪學到、下一輪會再踩的三個坑

- **heredoc 會吃掉反斜線。** `python - <<'PY'` 裡的 `\theta` 會變成 tab、`\s` 會變成
  SyntaxWarning。本 session 踩了三次。**要改含 LaTeX／regex 的檔，用 Edit 工具或先
  `Write` 成腳本檔再跑，不要用 heredoc。**
- **`rewatch_pack` 的靜止統計會高估。** 它的 docstring 自己寫著「細線／小標籤的 reveal
  抓不到」——0.2% 像素門檻會漏掉細線動畫。場 06 實測：0.2% 門檻報 89%/20.0s，0.05% 門檻
  報 59%/12.2s，逐幀取樣確認畫面一直在變。**報數字時兩個門檻都列，不要只引一個。**
- **selftest 全綠不代表畫面對。** 場 06 的 `(1)(2)(3)` 編號環被 `set_opacity(1.0)` 填成實心
  色塊，30 支 selftest 加五道閘全部沒抓到，是**肉眼對照基線幀**看出來的。
  **每次動畫面都要抽最終幀跟 `output/ch03/s3.1/mimo_fullest_frames/` 的基線比。**

---

## 2. 已驗證的 code 事實（2026-09-12 快照；行號會漂，用 grep）

### 六支 motion primitive 的現況

| # | 原語 | 怎麼用 | 落地在 |
|---|---|---|---|
| 1 | 揭示時序 | `say` 寫 `{show statement}`／`{show proof.0}` 才滑入 | `theorem_proof.py`／`derivation.py` |
| 2 | 原地變形 | `steps[i].anim: transform`／`result.anim: transform` | `derivation.py`（`TransformMatchingShapes`） |
| 3 | 游標掃描 | `plots[]` 加 `kind: sweep` | `graph.py` |
| 4 | **聚焦** | scene 層 `focus: [{at: <reveal id>, dim: [<block ids>]}]` | `pipeline/focus.py` |
| 5 | **跨場延續** | `steps[i].color_role`／`result.color_role`（graph 的 plot 本來就有 `color_role`） | `derivation.py` |
| 6 | **圖跟旁白長** | `plots[].seconds: beat`；hook 內用 `TM.beat_run_time(scene, fallback)` | `timing.py`＋`scene.py` |

- **原語 6 的致能層**：`scene.beat_seconds` 由 `scene._play_content` 在每拍開始前設好
  （拍外為 `None`）；`timing.beat_run_time(scene, fallback)` 讀它，保留
  `BEAT_PACED_TAIL_SECONDS=0.6`、不低於 `BEAT_PACED_MIN_SECONDS=0.8`。**callable 簽章沒變**
  （`(scene, mob, ground)`），既有 hook 逐 token 不受影響。
- **原語 4 的狀態模型**：每筆 entry 取代該拍起的壓暗集合，`dim: []` 還原；場末一律全部還原。
  **還原用 `save_state()`/`restore()`，絕不可用 `set_opacity(1.0)`**（會把刻意透明的部分填實）。
  閘：`schema._focus_issues` 驗 `at` 指到真的有 `{show}` 的 reveal ＋ 重複 `at`；
  `sizecheck` 驗 `dim` 的 block id 存在。
- **刻意沒做 `{focus}` 旁白 marker**：`derive_spoken` 用 `{show}` 專屬 regex 剝 marker
  （`_SHOW.sub`），`{focus ...}` 會整串**漏進 TTS 文字被唸出來**；而且要同時教會
  `narration.parse_say`、`derive_spoken` 的 parity 與 stripper、`sizecheck` 四個模組。

### 語意色軸（Direction B，⑨）

`accent:` → palette role，對位講義 `handout/latex/template/calcbook.sty`：
`definition`→`concept` 赭、`theorem`/`proposition`/`corollary`/`proof`/`recap`→`result` 藍、
`example`/`solution`→`practice` 綠、`caution`/`warning`→`caution` 紅、
`procedure`/`strategy`→`strategy` 紫、`remark`/`note`→`aside` 灰。
未設或不認得＝中性 slate（`blocks.DEFAULT_ROLE`）。
`_selftest_semantic_palette.py` 會**重讀 `calcbook.sty` 比對色相**，兩條線漂開就紅。

### 例題折疊宣告閘（⑩）

`.md` 單元的 `examples:`／`folds:` ↔ 講義該節的 `ex:` label key。**`ex:` 編號是章序不是節序**
（§3.1＝`ex:3.1–3.3`、§3.2＝`ex:3.4–3.8`），歸節按 `\sechead` 區間掃描。只接
`schema.py:main()`，deck 無 `.md` 整個跳過。**閘只查宣告存不存在，不判折疊對不對。**

### 驗 TTS 零成本（唯一正確方法）

```python
# scene_text_hash 是剝掉 marker 後的口語全文；相同＝reuse＝零 call
import re, json, yaml, sys; sys.path.insert(0, "video")
from pipeline.timing import text_hash
_SHOW = re.compile(r"\{show\s+[^}]+\}")
say = {s["id"]: s.get("say", "") for s in
       yaml.safe_load(open("video/storyboards/<deck>_mimo.yml", encoding="utf-8"))["scenes"]}["<scene>"]
now = text_hash(" ".join(_SHOW.sub("", say).split()))
prior = [s for s in json.load(open("video/output/ch03/s3.1/audio_mimo/manifest.json",
         encoding="utf-8"))["scenes"] if s["scene_id"] == "<scene>"][0]["scene_text_hash"]
print(now == prior)
```

### 零行為改變的驗收方式

```bash
python tools/doctor.py --smoke > /tmp/after.txt 2>&1
# 改動前的基線：用 detached worktree 取 HEAD，或改動前先存一份
diff /tmp/before.txt /tmp/after.txt      # 必須逐字相同
```

### 場 06 現在長什麼樣（剛做完，當範本）

`sector_inequality` 的 hook 把 scaffold 拆成 `circle`／`evenness`／`frame`／`apex` 四個
可揭示階段（O→C 的半徑切成 O→B ＋ B→C 兩段共線線段），`evenness` 是一個用
`TM.beat_run_time` 跑滿 19 秒拍子的小單位圓（角度盪 ±θ、半弦變號）。
`say` 加了四個 marker，`focus:` 三筆。**這是原語 6 第一次真的跑在長拍上，照它抄。**

---

## 3. Task A — 場 08 的單位圓 hook（下一步，最貴的一塊）

`continuity_statement_sin_limit`（`theorem_proof`，27 場中的第 8 場）。

**病灶**：beat 1 是 83 個字、27.5 秒，**完全沒有 marker 也完全沒有圖**。旁白明講
「on the unit circle the half-chord $\sin\theta$ is always shorter than the arc $\theta$」，
但畫面上沒有單位圓——那張圖三場之前（場 06）才畫過。六鏡 digest level ①、三鏡判 weak。
而且上一輪把揭示時序修好之後，**這 27 秒比以前更空**（舊版至少有一張提前劇透的 statement
卡佔著版面，新版誠實地讓它空著）——這是使用者已知的取捨。

**R2 導演鏡開的處方**（照做）：
1. `+1.0s` 圓與角 θ 進場，θ 用滑桿左右輕推兩次約 2s，讓 $\sin\theta$ 的高度跟著小幅上下
   ——這就是旁白的 "move only a little, never jump"。
2. 念到 "half-chord" 時把半弦畫成一筆（0.8s）；念到 "the arc" 時把弧畫成另一筆（0.8s），
   兩者用不同顏色。
3. 念到 "shorter than" 時把兩筆**同時拉直、並排、對齊同一基線比長度**（1.5s），比完就地
   長出 $|\sin\theta| \le |\theta|$。
4. 演完讓 statement 方塊進場，圖縮到右下角當佐證留在畫面上。

**怎麼做**：
- [x] **A-1** 新增 hook `animations/ch03_trig_derivatives_hooks.py:chord_vs_arc`。
      `theorem_proof` 模板的 hook 接法見 `templates/__init__.py:_apply_hook`；場 06 的
      `sector_inequality` 是現成範本（尤其「建在 `_centre_in_zone` 之後、不進 `full`，所以
      動不了主圖」那一段）。用 `ValueTracker` ＋ `always_redraw` 做 θ 滑桿（抄 `graph.py`
      的 `kind: sweep` 或場 06 的 `evenness`）。**拉直比長度**那一步用
      `ReplacementTransform`（弧 → 直線段）。
- [x] **A-2** beat 1 加 marker。切點照旁白的語意邊界，大致是：
      `{show circle}` 開場 → `{show nudge}` 在 "nudge the angle a little" → `{show chord_arc}`
      在 "the half-chord … is shorter than the arc" → `{show straighten}` 在 "shorter than"。
      **一個字都不要改**。canonical 與 `spoken.yml` 同步 → `derive_spoken --check` → 重生。
- [x] **A-3** 至少一段用 `TM.beat_run_time` 跑滿它的拍（27.5 秒的拍不可能用 1 秒級動作填滿
      ——這是本輪最核心的教訓）。
- [x] **A-4** selftest：`_selftest_*.py`，斷言 hook 建得出那幾個 block、id 正確、
      `beat_run_time` 有被用到。
- [x] **A-5** 驗收：`schema`／`sizecheck` 0 error；mock render；**抽最終幀跟基線
      `mimo_fullest_frames/07_continuity_statement_sin_limit.png` 對照**；量最長靜止（兩種
      門檻都列）。

---

## 4. Task B — 原語鋪滿其餘場次

27 場裡目前只有 **04**（transform＋pause）、**06**（四階段＋focus）、**08**（Task A）、
**11**（sweep）動過。其餘 23 場照 R2 的 45 條提議鋪。

- [x] **B-1** 讀 `content_scripts/_audit/_gen/rewatch_multilens.digest.json` 的
      `scenes[].findings` 與 `one_change`，逐場列出「該用哪支原語」。R2 的提議多為 1–3 秒
      動作、只落在 5–6 種型態，所以大多是欄位／marker 改動。
- [x] **B-2** **優先處理「首 beat 無 reveal」的 8 場**（digest 的 film patterns 有列，最長
      37.6s）——那是靜止時間最集中的地方，也是原語 6 唯一能發揮的地方。
- [x] **B-3** **全 27 場的 `accent:` 值依新語意軸複審**。已知一個要改：
      `difference_quotient_for_sine` 標 `accent: definition`（→ 赭）但它推導出的是 result
      （→ 藍）。這是 storyboard 的值不是 code，本 session 刻意沒擅改。
- [x] **B-4** **場 20 `companion_limit` 重排**——四鏡認證它是孤兒（21–26 場與 recap 都沒再
      回用），R3／R5／digest 的 `one_change` 三方都指向重排。**零 TTS**（動的是場序與
      `scaffold.motive`，不是旁白）。⑩ 的分工通則已明文授權場級重排「不需要理由」。
      兩個選項的幕長後果不同：移到 $\sin\theta/\theta$ 旁，或移到 `derivative_cycle` 之後。
- [x] **B-5** 每改一場就 mock render ＋ 對基線幀。不要一次改 23 場才 render。

---

## 5. Task C — 驗收

- [x] **C-1** 全片 mock render ＋ `rewatch_pack.py` 產 pack。
- [x] **C-2** **新驗收線（⑧ 拍板）：每個 content 場 `longest_still_seconds` ≤ 12 s**，超過
      為 finding 但可用一句理由豁免。**`static_ratio` 只記錄不設門檻**（它對 verdict 的
      相關性只有 −0.18，而 `longest_still` 是 −0.82）。
- [ ] **C-3** R2 導演鏡以 Opus 5 subagent 重跑 before/after（`rewatch_prompts.py` →
      subagent → `rewatch_merge.py --verify` → `rewatch_multilens.gen.py`）。
- [ ] **C-4** 既有閘全綠：`run_selftests`、`doctor --smoke`、`visual-frame-audit` subagent。
- [x] **C-5** 產 standalone HTML 報告（繁體中文框架、self-contained），比照
      `REVIEW-ch03_s31-pilot-ab.html`。
- [ ] **C-6** **人閘**：把成片交給使用者裁決要不要進計費階段（Task D）。

---

## 6. Task D — 計費的部分（**執行前必須先報量徵同意**）

這兩件都要重 TTS。**建議一次決定範圍、一次報量**，不要分兩次。

- [ ] **D-1 R6 三處外科修改中剩下的兩處**（⑤④ 拍板；20 已在 B-4 免費做掉）：
      - 場 **06** 偶函數對稱論證移到不等式之後（四鏡同指）——**beat 級**，鎖在 LOCKED 旁白內。
        註：本 session 已用 `evenness` 動畫讓那 19 秒有東西看，但**論證順序本身沒動**。
      - 場 **13** 度數導數公式延後到場 15 之後或 recap（R5）——**beat 級**。
      每處＝post-lock 改稿 → scoped NFA → 該場重 TTS。
- [ ] **D-2 §3.1 對 `.tex` 的 §8 對齊**（⑤ 拍板）：全稿對
      `handout/latex/src/ch03/chapter3.tex` 做 diff、逐單元判是否跟改。已知分歧：04 的
      和差化積推導、03 開節兩句已刪。改的場一併 scoped NFA ＋ 重 TTS。完成後
      `source_rev` stamp 換到 `.tex`、現在那個常駐的 `[source_rev] WARN` 才會消失。

---

## 7. 之後（本輪範圍外，另案）

### 7.1 模板系統重新設計的其餘部分（品質補強輪 ⑨ 未竟項）

設計畫布：<https://claude.ai/code/artifact/b6bbb677-135e-48fc-8d0d-9ff13cca05ca>（3 頁 9 artboard）。
**`.dc.html` 工作檔已進版控**：[`_audit/design-template-system/`](_audit/design-template-system/)
（含 README：怎麼改、怎麼重新發布回同一個畫布、為什麼只收源不收 2.5 MB 的成品）。

- **版面構成 4 條規則**（page-3）：① 結論必須是畫面上最重的元素 ② 下三分之一不得長期空置
  ③ 右欄（`aside`）有條件展開——**27 場一次都沒用過** ④ 三種佔比依章的體質選。
  四條都能寫進 `sizecheck` 當確定性檢查。
- **數學排版 5 條規則**：① 數學行內不得混入散文 ② 註解 rail 只有兩種語域 ③ 正斜體照數學
  慣例 ④ ∎ 是字形不是元件（現在渲成綠色圓角方框、像 UI 按鈕）⑤ 數學字級收成三階，
  **取消 `math_sm 40`**（會動到現有 deck，**待使用者裁決**）。
- **`worked_example` 新模板**——全書 **220 個單元、最大的缺口**，影片產線完全沒有。
  §3.1 有 16 個例題、影片一場都沒有。mockup 在畫布 page-3。
- **字體**：Direction B 的 mockup 用 Instrument Sans，但落地要**裝 LaTeX 字型**
  （`CLAUDE.md` 規定先徵詢）且 `brand._WIDTH_K = 0.00507` 是對 Plex 校準的、換字得重測。

### 7.2 其他 open items

- `meta.example_coverage_enforce` 開關（要動正典 yml meta → `_mimo` 需重 derive，
  排在 §3.1 整節重做時順做）。
- **§3.2 解凍**——卡在品質補強試點 ④ 的新舊 A/B 裁決。
- **環境**：`pdftotext` 是 xpdf 版不是 poppler 版，`doctor --smoke` 會紅一項，
  講義線 `build.py` 會踩到。**裝 poppler 前要先問使用者**（`CLAUDE.md` 缺套件先問）。
- **16 個 commit 未 push**（`main` 領先 `origin/main`；2026-09-13 計）。使用者沒說要 push，沒動。

---

## 8. 完成定義（DoD）

1. §3.1 全 27 場的 `longest_still_seconds` 都 ≤ 12 s，或超過者逐條有理由。
2. R2 導演鏡重跑：① 級 finding 關閉、verdict ≥ ok、無新 must。
3. `run_selftests` 全綠、`doctor --smoke` 與本檔立檔時逐字相同（除非有意改變且已記錄）。
4. 全 27 場的 `accent:` 已依新語意軸複審。
5. HTML 報告產出、`REBUILD_STATUS.md` 加本輪一條、本檔各 task 勾選。
6. 人閘：使用者看過成片並裁決是否進 Task D。

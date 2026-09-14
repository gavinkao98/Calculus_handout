# KICKOFF — 工具線 backlog 第 1 輪（凍結後的六個 task）

> 2026-09-14 立檔。共用層 v1 凍結（[`KICKOFF-shared-layer-v1.md`](KICKOFF-shared-layer-v1.md)）之後，
> §8 backlog、[`KICKOFF-motion-language-gaps.md`](KICKOFF-motion-language-gaps.md) §8、流程改革輪的工具
> backlog 三份合計約 30 條。本輪由主對話逐條分類、使用者裁決「A–F 六個 task 全做」，
> 每個 task 一個子代理、一個 worktree、一個 commit；主對話只寫契約、merge、審核。
> **全程離線零計費**：不 render 成片、不碰 TTS／Codex／agy。

---

## 0. 給子代理的啟動提示（派工 prompt 會指到本檔的某一節）

> 你在 repo `Calculus_handout` 的 `video/` 子樹做工具線的一個 task。先讀本檔 §1 全域護欄，
> 再讀你被指派的那一節（§2.A–§2.F），照契約做：**先寫會紅的測試，再讓它綠**；只改契約列的檔；
> 一個 commit；回報照 §4 的格式。中途不要停下來問，除非 §1 的護欄被觸發。

---

## 1. 全域護欄（每個 task 都適用）

1. **開工第一件事：在你的 worktree 裡 `git merge main`**（分支點可能落後），然後 `git status` 確認乾淨。
2. **只動契約列的檔**；發現別的問題記進回報的「新 backlog」，不順手修。
   **一律不動**：`content_scripts/*.md`、任何 storyboard 的 `say:` 文字、任何 `*_mimo.yml`、
   `audio*/`、`pipeline/visuals/theme.py` 的 `_SCALE_PX`／`PX_TO_FS`／`TEXT_SCALE`（E 的 fontdimen 除外）、
   `pipeline/brand.py` 的 `_WIDTH_K`（E 若重校要在 commit body 給量測）。
3. **零計費**：`tts.py` 只准 `--backend mock`；`make.py` 只准 `--backend mock`（它本來也只有 mock）；
   不呼叫 `codex`／`agy`／任何 VLM。mock render 單場：
   `python video/make.py --storyboard video/storyboards/<deck>.yml --backend mock --scene <id> --quality low`
   （建議 `low`，抽幀夠用；`_selftest_*` 已含 Tex 編譯，不必另 render 來驗）。
4. **主 checkout 的 `video/output/` 只准讀不准寫**（絕對路徑
   `C:/Users/Kao/Downloads/Calculus_handout/video/output/`；worktree 裡沒有這些成品）。
   要抽幀、量測，把結果寫到你自己的 worktree `video/output/` 或 scratchpad。
5. **MiKTeX flake**（§8 backlog ⑧）：同一個 worktree **不要並行**跑兩個 build／報表 pass；
   `latex.exe`／`dvisvgm.exe` 靜靜卡住超過 3 分鐘就 kill 掉重跑，那不是你的 bug。
6. **零行為改變的證據做法**（共用層 v1 §2.6 的老規矩）：
   對 23 個 deck（`video/storyboards/*.yml`）跑
   `python video/pipeline/schema.py <yml>`、`python video/pipeline/lint.py <yml>`、`python video/pipeline/sizecheck.py <yml>`，
   改前改後各存一份（scratchpad，不進版控），逐檔 diff。
   **意圖不變的 task（B、C、D、F 的 ⑨⑭）必須逐字相同**；**意圖改變的 task（A、E、F 的 STOCK 校正）**
   逐條解釋每一處差異並附幀對照。`python video/pipeline/run_selftests.py` 改前改後都要全綠（記支數）。
7. **commit**：subject ≤70 字、`<type>(video): [<tag>] …`；body 逐條寫：原本是什麼、為何不妥、改了什麼、
   證據（測試名／數字／幀路徑）。結尾加你自己模型的 `Co-Authored-By:` 行
   （例如 `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`）。**不要 merge 進 main**，主對話做。
8. 文件同 commit 補齊：改了契約就改 [`DESIGN.md`](DESIGN.md) 對應節；改了閘就改
   [`REVIEW_GATES.md`](REVIEW_GATES.md) §一該層那一列；新 selftest 進 `run_selftests.py` 的清單（若它是掃目錄就不用）。

---

## 2. Tasks

### 2.A — `derivation` 的 paced 無 rail 列燒掉整拍（backlog ⑯；派 **opus**；tag `[paced-norail]`）

**現況（已核）**：`pipeline/templates/derivation.py` 的 `_rail()`（約 :201）對**沒有 `reason`** 的列回傳
等式自己的 glow wrapper，`_rail_walk_seconds()`（:209）因此有 n>0，`pacing.walk` 把拍子剩餘秒數
「走」在一個看不見的東西上；該列又因宣告了 `paced:` 而被 `[stillness]` 免檢。結果＝宣告 paced、
實際整拍靜止且閘看不到。實例：`ch03_trig_derivatives` 場 22 `all_six_cot_csc` 的 `result` 靜止 11.26 s
（里程碑審在 hook 裡繞開，stock 未改）。同型宣告：`grep -n "paced:.*result" video/storyboards/*.yml`
（`ch03_trig_derivatives.yml` 4 處、`_demo_worked_example.yml:56`）。

**目標**：
1. **誠實**：沒有 rail 可走的 paced 列，`_rail_walk_seconds` 回 `None`，回報的 `anim_seconds` ＝ morph 本身；
   於是 `[stillness]`（`make.py::_warn_undeclared_stillness`）能看見剩下的靜止。
2. **提早擋**：`schema.py`（或 `lint.py`，選既有 paced 檢查所在的那支）對「`paced:` 列出的列既無 `reason`
   也沒有可走的部件」出 **warn**：`paced row '<rid>' has nothing to walk (no reason rail)`。
3. **不改**任何 storyboard、不改 hook。場 22 的 hook 已自行縮 `beat_seconds`，改後它的行為必須不變
   （`_selftest_all_six_table.py` 10/10）。

**紅測試先行**：`pipeline/_selftest_derivation_paced.py`（新）——① 有 reason 的 paced 列 `_rail_walk_seconds`
回正數；② 無 reason 的 paced 列回 `None`；③ schema/lint 對 `_demo_worked_example.yml:56` 那類宣告出 warn、
對有 reason 的不出。先在現行 code 下讓 ②③ 紅。

**改哪些檔**：`pipeline/templates/derivation.py`、`pipeline/schema.py` 或 `pipeline/lint.py`（擇一）、
新 selftest、`DESIGN.md` 的「motion primitive」節 paced 那段補一句「無 rail 不走、改由 stillness 報」。

**證明**：23 deck 報表 diff——schema／lint **只允許新增**上述 warn（逐條列出是哪些 deck 哪些列），
sizecheck 逐字相同；`run_selftests` 全綠。mock render `_demo_worked_example` 一次，貼 `[stillness]` 輸出
證明該列的靜止現在被報出來。

### 2.B — 執行期字級探針（backlog ①②⑪⑫⑰ 同一家族；派 **opus**；tag `[floorprobe]`）

**現況（已核）**：`sizecheck.py` 量的是 build 佈局的 authored px：`_effective_font_px`（:573）看不到
`\tfrac` 內縮（①）、對 `substrings_to_isolate` 節點用公開 getter 高估（②）、`carry: to.scale` 的縮放（⑪）、
hook 手刻的 `MathTex`（⑫）與執行期縮放／退場（⑰）它一律看不到。五條共同根因＝**靜態閘看不到渲染後的真實字級**。

**目標**：加一條**執行期** advisory 通道，不動既有 `sizecheck`：
1. 新模組 `pipeline/floorprobe.py`：`probe(mobjects, *, floor=T.MIN_FONT_FLOOR) -> list[Finding]`，
   走 scene 的 mobject 樹（不是 storyboard 宣告），對每個 `Tex`／`MathTex` 頂層物件量**有效 px**
   ＝ 公開 `font_size` getter（它跟隨 `.scale()`，所以 carry／hook 縮放都看得到）除以 `PX_TO_FS`
   （文字再除 `TEXT_SCALE`）；tex 字串含 `\tfrac`／`\frac`／`^`／`_`／`\sqrt[` 者，另報**內縮有效 px ＝ 有效 px × 0.7**
   （TeX scriptstyle 比例）。低於 floor 出 warn，訊息帶 scene id、beat、tex 前 40 字、有效 px、來源
   （`carry scale 0.6`／`hook`／`tfrac inner`）。**只量不動**：不 `wait`、不改任何 mobject。
2. 掛進 `pipeline/scene.py::_play_content` 每拍結束處（`self.wait(...)` 之後）與 `_tail` 之前各量一次；
   結果走**既有的**執行期回報通道（`[sync]` 每拍實測秒數用的那條 sidecar／manifest 欄位——先找到它，
   **不要另發明第二條**），由 `make.py` 在 `_warn_undeclared_stillness` 旁邊印 `[floorprobe] …`。
3. warn-only；若既有 `meta.fontfloor_enforce` 的模式可以一行鏡射成 `meta.floorprobe_enforce` 就加，否則不加。

**紅測試先行**：`pipeline/_selftest_floorprobe.py`（新，`_bootstrap.bootstrap()` 後直接建 mobject，不 render）：
① 48 px `MathTex` `.scale(0.4)` → 報 < floor；② 34 px 含 `\tfrac` 標籤 → 報「內縮」< floor；
③ 48 px 純式 → 乾淨；④ 一個 `Tex` 文字 42 px → 乾淨（驗 `TEXT_SCALE` 除法對）。

**改哪些檔**：`pipeline/floorprobe.py`（新）、`pipeline/scene.py`（兩處呼叫）、`make.py`（印出）、
`pipeline/timing.py` 或該 sidecar 的寫入處（加欄位）、新 selftest、`DESIGN.md`「Reveal 的耗時回報契約」
旁加一小節、`REVIEW_GATES.md` §一層 6 的 sizecheck 列加一句「執行期＝floorprobe」。

**證明**：23 deck 三份報表**逐字相同**（靜態閘沒動）；`run_selftests` 全綠；mock render
`ch03_trig_derivatives` 的 `squeeze_graph`＋`companion_limit`＋場 24（backlog ⑪ 的 carried tag）三場，
貼 `[floorprobe]` 輸出，且同一次 render 的 `[sync]` 每拍實測秒數與改前逐拍相同（證明只量不動）。

### 2.C — `critic.py --per scene` 抽最滿幀而非末幀（backlog ⑩；派 **sonnet**；tag `[critic-fullest]`）

**現況（已核）**：`plan_frames()`（:163）`per == "scene"` 時 `ts = 1e9`，`extract_frames` clamp 到
`duration - 0.05`＝末幀。有 `exit:` 的場末幀已清空（場 06、23），gate 1 等於空跑。

**目標**：`per == "scene"` 改抽 **ink 最大**的幀。做法比照 `rewatch_pack.motion_stats`：ffmpeg 以 4 fps、
`scale=192:108,format=gray` 解碼整場，ink ＝ 與背景色差 > 門檻的像素數；取 argmax（**平手取最晚**；
末幀 ink ≥ 最大值的 99% 時仍取末幀，讓純累加場的結果與現況逐幀相同）。`ts` 寫回 plan，
frame 檔名仍是 `final.png`，plan item 加 `fullest_ts`／`ink_ratio_vs_last` 兩欄供報告用。
`--dry-run` 不解碼（維持免費、無 mp4 也能跑）。

**紅測試先行**：`pipeline/_selftest_critic_fullest.py`（新）：用 ffmpeg 合成 3 秒 mp4——前 2 秒畫一段文字、
最後 1 秒全背景色；斷言選到的 `ts` < 2.0；再合成一段純累加（文字只增不減）斷言選到末幀。

**改哪些檔**：`pipeline/critic.py`、新 selftest、`REVIEW_GATES.md` §一 VISUAL-FRAME 那列的「被審物」
改成「最滿幀（ink 最大）」。

**證明**：23 deck 三份報表逐字相同（critic 不在報表鏈裡，這是形式上的）；`run_selftests` 全綠；
對主 checkout 既有 `output/_av/ch03_trig_derivatives_mimo/` 的場 06、23、以及兩個純累加場（自選）
跑 `critic.py --dry-run` 以外的抽幀（離線免費，`--out` 指到 scratchpad），貼四張幀路徑與所選 `ts`，
證明 06／23 抽到有內容的幀、純累加場與末幀相同。

### 2.D — `rewatch_pack` 三缺（backlog ⑱＋流程改革輪兩條；派 **sonnet**；tag `[rewatch-subset]`）

**現況（已核）**：`rewatch_pack.py` (1) `--scene` 子集仍對**全部**場 `raise SystemExit` 若 `_av/<id>.mp4` 缺
（:445–448）；(2) 子集寫進既有 pack 目錄會整個覆寫 `INDEX.md`／`pack.json`（:588／:601）；
(3) `_beat_at`（:151）對跨拍的靜止段回空字串，FAIL 行尾沒有所在拍。

**目標**：
1. `--scene` 非 `all` 時：只要求子集場的 `_av` 存在；缺的場 `durs` 記 `None`、global start 記 `None`，
   `INDEX.md` 首段加一行「subset pack: N of M scenes; global times omitted」，`pack.json` 加 `"subset": true`。
2. `--scene` 非 `all` 時 **必須給 `--out`**，否則 exit 2 並印原因（規則：子集一律另給 `--out`）；
   且 `--out` 若已存在且其 `pack.json` 不是 subset，也 exit 2（不覆寫全包）。
3. `_beat_at` 跨拍：回傳覆蓋秒數最多的那一拍，格式 ` (beat 3, proof.1; spans beats 3–4)`。

**紅測試先行**：在 `pipeline/_selftest_rewatch_pack.py` 加：① 跨拍 span 回主拍並標 spans；② 子集缺 `--out`
→ exit 2（抽 main 的驗證邏輯成可測函式）；③ 子集寫進非 subset 的既有包 → exit 2。

**改哪些檔**：`pipeline/rewatch_pack.py`、其 selftest、`REVIEW_GATES.md` §六 6.4 的 `[still-gate]` 用法補
「子集必給 --out」一句（若那裡已有就不重複）。

**證明**：23 deck 報表逐字相同（形式上）；`run_selftests` 全綠；對主 checkout 的
`output/_av/ch03_trig_derivatives_mimo/` 跑一次 `--scene all_six_cot_csc,recap --out <scratchpad>`
貼 INDEX 首段與 exit code；再跑一次不給 `--out` 貼 exit 2 訊息。

### 2.E — Instrument Sans 的寬度後果（backlog ③④⑬；派 **opus**；tag `[sans-width]`）

**現況（已核）**：T1 換字後 (③) bold 標題詞間距偏緊（3 場幀稽核點名）；(④) `derivation.py:67`
`MIN_LEADER = 0.55`，`:366–370` 算 `reason_x`，下限咬住時（場 04 實測 leader 73 px ≈ 下限）沒有 fallback；
(⑬) 場 21／22 reason 第一列右緣餘裕 60→20 px，仍在框內但無容錯。三條同源＝新字比 Plex 寬。

**目標**（三條各自可獨立落地，但同一個 commit）：
1. ③ 在 `pipeline/_bootstrap.apply_tex_template()` 的 preamble 對 **bold series** 調 `\fontdimen2`
   （interword space）到與 regular 的視覺密度相當；量測方法寫進 commit body。
   **重跑 T1-3 的不變式** `_selftest_text_metrics.py`：cap height 不變、估寬 ≥ 真寬（fixture 加一句 bold 字串）。
   若 `_WIDTH_K` 需要重校，照 [`KICKOFF-shared-layer-v1.md`](KICKOFF-shared-layer-v1.md) §5 T1-2 的配方量，數字進 body。
2. ④ 下限咬住時的 fallback：在 backlog 列的三個選項裡擇一（點改線／reason 併回等式下一行／rail 整體右移），
   **不得新增第四階字級、不得改 `_SCALE_PX`**；選哪個、為什麼，寫進 `DESIGN.md` derivation 節。
3. ⑬ reason 右緣：用現行估寬器算 widest reason 落點，距 `SPINE_X + CONTENT_W` < 0.15 u（≈20 px）時
   走與 ④ 相同的 fallback（同一機制，不另開分支）。

**紅測試先行**：`pipeline/_selftest_derivation_rail.py`（新）：① 構造 reason 很長的列 → fallback 觸發且
所有 mobject 右緣 ≤ `SPINE_X + CONTENT_W`；② 正常列 → leader ≥ `MIN_LEADER` 且不觸發 fallback；
③ bold 標題 `Tex` 的估寬 ≥ 真寬。

**改哪些檔**：`pipeline/_bootstrap.py`、`pipeline/templates/derivation.py`、`pipeline/_selftest_text_metrics.py`、
新 selftest、`pipeline/brand.py`（僅當重校 `_WIDTH_K`）、`DESIGN.md`。

**證明**：這是**意圖改變**——23 deck 報表：schema／lint 逐字相同；sizecheck **error 仍 0**，warn 增減逐條解釋。
mock render `ch03_trig_derivatives` 場 04、21、22 與一場 bold 標題長的場（自選），改前改後幀並排
（放 scratchpad，回報貼路徑），派 `visual-frame-audit` 免費 gate 1 看這四場 → blocking 0。

### 2.F — 衛生四件（backlog ⑨⑭＋動畫時長單一來源＋硬寫數字；派 **sonnet**；tag `[hygiene]`）

1. **⑨ `_selftest_theorem_regime.py:115` 用 `"band" in msg` 撈 finding**：給 `sizecheck` 的 band 升格 advisory
   一個穩定的機器碼放在訊息裡（比照 T3 的 `(LayoutRules L1)` 寫法，例如 `(band promotion)` 固定字串
   或既有的 code 慣例——看 sizecheck 現況選一種），selftest 改比對該碼；`sizecheck.py` 頂部註解記
   「訊息文字可改，碼不可改」。
2. **⑭ 箭頭尺寸進 theme**：`pipeline/visuals/theme.py` 加 `AXIS_TIP = 0.16`、`AXIS_TIP_INSET = 0.14`
   （現值照抄，零行為改變）；`templates/graph.py:826–827`／`:914–915` 改讀 theme；
   `animations/ch03_trig_derivatives_hooks.py:2232` 那個 `tips=True` 的 `Axes` 改成與模板同尺寸
   （**只改這一處 hook，一行參數**）。場 12 因此改變：mock render 場 12 貼改前改後幀。
3. **動畫時長單一來源**：`pipeline/blocks.py::_reveal` 四處 `run_time` 與 `timing.STOCK_ANIM_SECONDS` 不一致
   （highlight 0.7 vs 1.2、flash_in 0.5 vs 1.1、write_glow 0.8 vs 1.4、slide_pop 0.45 vs 0.85）。
   **以實際播放值為真**：表改成 0.7／0.5／0.8／0.45，`_reveal` 改讀表（單一來源），其餘鍵值不動；
   刪掉 `_reveal` 開頭沒用到的 `accent` 區域變數。視覺零改變（run_time 不變）；`anim_seconds` 規劃值變小，
   `[stillness]`／`_warn_short_beats` 可能多報——把 23 deck lint／sizecheck diff 逐條列出。
   新增 `_selftest_stock_anim.py`：對每個 stock 名，`_reveal` 實際 `play` 的 run_time ＝ 表值（monkeypatch `scene.play` 記錄）。
4. **硬寫數字掃一次**：`README.md`、`REVIEW_GATES.md`、`RUNBOOK-mimo-narration-route.md`、`DESIGN.md`、
   `ENVIRONMENT.md`、`tools/doctor.py` 裡宣稱**現況**的 selftest 支數、deck 數、模板數，對現況
   （`run_selftests` 支數、`ls video/storyboards/*.yml | wc -l`＝23、`templates/__init__.py` registry）逐一校正；
   **不改** `REBUILD_STATUS.md`（主對話收尾統一改）與各 `KICKOFF-*.md` 的歷史數字。回報列出每處改動。

**改哪些檔**：上列各檔＋兩支新 selftest。**證明**：23 deck 報表——schema 逐字相同；lint／sizecheck 差異
只能來自第 3 項（逐條解釋）；`run_selftests` 全綠；場 12 幀對照。

---

## 3. 主對話的驗收與 merge 流程

1. 六個分支各自回報後，主對話逐一：看 diff 是否只在契約檔、看測試數字、抽查幀。
2. merge 順序：**C → D → F → A → B → E**（無檔案交集者先；A／B／E 都碰 `derivation.py`／`scene.py` 家族，
   最後依序 merge 並在每次 merge 後跑 `run_selftests`）。
3. 全部併入後在 main 跑一次 23 deck 報表對本輪起點 diff，逐條對得上六份回報的解釋；`doctor --smoke`。
4. `REBUILD_STATUS.md` 記本輪（含 F3／F9 裁決）；`KICKOFF-shared-layer-v1.md` §8 已收條目打勾。

---

## 4. 回報格式（子代理最後一則訊息必含）

- 改了哪些檔（路徑清單）＋ commit hash＋subject。
- 測試：新 selftest 名與條數（先紅哪幾條、後綠）、`run_selftests` 改前／改後支數。
- 23 deck 報表 diff 結論（逐字相同／哪些 deck 哪些行變、為什麼）。
- 幀路徑（若契約要求）與 `visual-frame-audit` 結果（若契約要求）。
- **沒做到的條款**與原因。
- 新 backlog（順手看到但沒修的）。

---

## 5. 本輪裁決紀錄（2026-09-14 使用者）

| 項目 | 裁決 |
|---|---|
| F3 AMP 的錨 | **過渡做法定為正式規則**：ch01–08 候選池＝同節凍結 fragment 的 `<!-- expansion -->`（全書 472 筆）；Ch9 起用 `CONTRACT-latex-writing.md` 的 `% expansion:` 註解；報告明寫池來源。不回填 `.tex`。F3 關閉。 |
| F9 靜默 beat 文法（R5） | **延後**：等 §3.2 出現「畫面要停得比旁白長」的場再加。 |
| F7／F8／F10／F11 | 已由 09-12～13 裁決收掉（原語落地／六鏡里程碑審＋靜止硬閘／R6 三處外科修改／G0–G7），不再列待裁。 |
| F12 的 R7 兩級製作 | 等 §3.2 跑完、成本表填了那一列再議。 |
| agy 定位 | REWATCH rubric 已定：盲審鏡預設 Opus 子代理，agy 只留跨模型家族之需。 |
| palette accent／concept 撞色 | 待看幀裁決；本輪不產對照幀（使用者選 A–F 不含）。 |
| 工具線範圍 | A–F 六個 task 全做。 |

**延後（本輪不做）**：⑥ L4／M4 只能人審；⑦ `worked_example` 九項 polish 等 §3.2 用過一輪；⑧ 環境 flake
已記紀律；`{{}}` 段級 role 等有場需要；hook 自建 MathTex 的規則寫進 METHODOLOGY §5 由主對話收尾時補一句，
§3.1 四個 hook 的遷移歸 §3.1 backlog；9 個 `derivation`＋`prompt:` 例題場遷移與 `meta.example_coverage_enforce`
歸 §3.2 session 的 A2。**已收、只差打勾**：⑤、⑮、`_SCALE_PX` result token、mockup 數學字體已記 README、RUNBOOK 9→10。

---

## 6. r2 候選 backlog（本輪進行中收到、不擴 r1 範圍）

> 來源＝§3.2 Phase A session 2026-09-14 跨 session 訊息（實測依據在該 session）；主對話只登錄，r1 不收。

1. **`pipeline/provenance.py::_present_text_fields` 不掃 `procedure_steps` 的 `steps[].text`。** 那些文字經 `brand.prose`
   上畫面（`templates/procedure_steps.py:68`），確定性 OF2 對該模板等於空的——`decomposition_strategy` 整場沒有 `ref:`
   也不會被報（§3.2 手動補的）。
2. **`step_coverage._SCOPED_TEMPLATES` 只有 `{theorem_proof, derivation, worked_example}`**，不含 `procedure_steps`／
   `definition_math`。Strategy 3.1 五步不受 SC 閘保護（§3.2 因第 5 步沒上畫面吃過一條 PD1 blocking）。
3. **`procedure_steps` 是唯一不吃 `scaffold` 的教學模板**，且四個 step 時 `worked[]` strip 與 row.3 重疊 57%；§3.2 只能用
   `part:` 分頁修（content 場 +1、TTS 多一次呼叫）。模板層缺口，屬 ⑦ 同級的 polish。
4. **`pipeline/derive_spoken.py` 的 `MD_CONFIG_AND_CONVENTIONS` §二慣例摘錄表落後 rubric 一列**（`NARRATION-FAITHFULNESS-RUBRIC.md:51`
   新增 D5「分母整體被平方」念法）。**補的話要連帶重生 §3.1 的 `_narration_spoken.md`**（跨節依賴，另開 chip、不在 r1）。**約束（§3.2 session 2026-09-14 補）：新列的適用範圍限「分母整個被平方」（$rac{A}{(X+Y)^2}$ → "A over the square of the quantity X plus Y"），**不推翻**既有「群組次方」列（§3.1 `ch03_trig_derivatives.spoken.yml:17` 的 "expanded the quantity x plus h, to the n" 仍正確）；抄進摘錄表時兩列並存、不合併——這個區分正是 gate-2 抓到 D2 blocking 的根源。已開 chip。

**來自 r1 子代理回報（2026-09-14，順手看到未修）：**
5. **`sizecheck.py:76` 的 `carriers` 過濾式恆為空**（Task B 發現）：`isinstance(n, Tex) and not isinstance(n, MathTex)` 在此版 manim
   永遠 False（`Tex` 繼承 `MathTex`），`_block_prose_size` 的 sibling 字級比較實際只收 `Text` 節點，而 Route A 之後畫面上已無 `Text`
   ——需確認 sibling 字級閘是否等於空跑。
6. **`floorprobe` 的 `^`／`_` marker 可能放大聲量**（Task B）：34 px rail 數學只要有上下標就報 23.8 px 內縮；warn-only 無害，
   全 deck 首跑後若吵到看不見重點，考慮只留 `	frac`／`rac`。
7. **`companion_limit_opening` 的 dt 累加 updater 讓場 14 不可逐像素重現**（Task B）：同 code 連跑兩次 MD5 不同（影格數／時長相同）；
   任何「改前改後幀比對」型驗收都用不到它，要當回歸基線得改成 frame-count 驅動。
8. **多子代理共用同一個 scratchpad 會撞檔名**（Task B）：本輪 `reports.py`／`before/` 已互撞；下輪派工 prompt 明寫「產物放 `scratchpad/task<X>/`」。

9. **§3.1 場 23 `shm_compute` 的 reason tag `SIMPLE HARMONIC MOTION` 撞進右側彈簧裝置**（主對話抽查 Task C 的最滿幀時看到；舊的末幀抽法因 `exit:` 清空看不到）。**不是工具線項目**，歸 §3.1 backlog、搭 4K final 一起修；收尾時抄進 `REBUILD_STATUS.md`。

**Task A 收尾的裁決與後續（2026-09-14 主對話）：**
- **裁決：不改 `[stillness]` 對 `paced:` 的無條件免檢。** 有 rail 的 paced 列由 `pacing.walk` 鋪滿整拍是構造保證；無 rail 的由 schema `nothing to walk` warn 提早擋。要改免檢得同時動 `_transform_anim`／`_cancel_anim` 的 `fixed_seconds`、`worked_example._row_block`、SPEC-motion-language 規則 4 與 `_selftest_stillness` (b)，而對現有 23 deck 是 no-op（唯二命中列都由 hook 接管）。不列 backlog，免得重議。
10. **§3.1 場 22 `all_six_cot_csc` 的 `paced: [step.1, result]` 應把 `result` 拿掉**（hook `all_six_summary` 已接管該列），否則每次 build 都多一條 schema warn；同場 hook 註解 `ch03_trig_derivatives_hooks.py:3201–3207` 描述的是舊行為（walk 整個 11.26 s），一併更新。**§3.1 側、非工具線**，搭 4K final。
11. **`_demo_worked_example` 預設跑不完 `make.py`**（Task A）：`capacity_over` 是刻意的壓測場（2 條 SIZE error），要 `--skip-sizecheck` 才 render 得動；若要當常態 smoke，把壓測場拆到另一個 deck 或給 `meta` 豁免。

**兩條共識更正（已採信，寫進對應文件）：**
- `sizecheck`／`schema` 的 TeX cache 競態是 **per-cwd**（`config.media_dir = ./media`，各 worktree 各有 `media/Tex`），跨 worktree
  並行零撞車；MiKTeX fndb 鎖才是全域偶發。→ [`KICKOFF-shared-layer-v1.md`](KICKOFF-shared-layer-v1.md) §8 ⑧ 已補註；
  `KICKOFF-s32-chain-rule.md` §2.3「量測閘一次只能跑一支」由 §3.2 session 自行修。
- `tts.py --backend mock --storyboard <deck>_mimo.yml` 會把靜音 WAV 與 mock manifest 寫進 `audio_mimo/`（真 MiMo 音檔的同一目錄）；
  **真合成前要先清掉或帶 `--force-backend-switch`**。→ 待 Task F 併入後補進 `RUNBOOK-mimo-narration-route.md`（避免與 F 的數字校正撞檔）。

**依賴（merge 時要做）：** §3.2 已跑過一次 1080p mock 音檔 render 當 `[sync]` 基線（909.9 s，舊 timing 常數）。r1 的 Task F
（`STOCK_ANIM_SECONDS` 對齊實際 run_time）與 Task A（paced 無 rail）merge 後該基線作廢——**merge 完通知 §3.2 session 重跑**
（只重 render、不重合成）。§3.2 基準線（2026-09-14）：28 場（content 23）、mock 音檔 828 s、成片 909.9 s、28 場全 narration under video；STOCK 對齊若讓畫面變短，最先撐不住的是最長三場 `proof_delicate_choices` 50.0 s／`two_forms_equivalent` 49.2 s／`proof_setup_substitution` 47.6 s。§3.2 會等真合成完再重跑 `[sync]`，不只對 mock 驗。

# KICKOFF — 模板層 motion primitive（品質補強輪 ③ 首輪）＋ §3.1 試點三場

> 2026-09-12 立檔。本檔給**新 session** 直接開工：§0 可整段貼進對話當啟動提示；§2 是已驗證的 code 事實（免重查）；§5–§7 是任務與驗收。裁決全在 [`REBUILD_STATUS.md`](REBUILD_STATUS.md)「品質補強輪」節，本檔只摘要、不重述理由。

## 0. 給新 session 的啟動提示（可整段貼）

> 讀 `video/KICKOFF-motion-primitives.md` 然後照它做。背景：§3.1 成片經六份模型盲審（`video/content_scripts/_audit/REVIEW-ch03_s31-rewatch-multilens.html`），使用者已裁決「模板層普遍有動」、首輪做三種原語（揭示時序／原地變形／游標掃描）、試點三場 04 difference_quotient_for_sine、11 squeeze_graph、08 continuity_statement_sin_limit。全程離線零計費（mock render＋現有 Dean 音檔 reuse），Phase 收尾用 Opus 5 subagent 重跑 R2 導演鏡當機器閘；唯一停點＝三場短片給使用者看。中途不要停下來問，除非 §3 護欄被觸發。

## 1. 目標與裁決摘要

| # | 裁決（2026-09-12） | 內容 |
|---|---|---|
| ② | 水位 | **模板層普遍有動**（否決「現系統內打磨」「每節少數招牌場」） |
| ③ | 原語與順序 | 六種：1 揭示時序、2 原地變形、3 游標掃描、4 聚焦、5 跨場延續、6 圖跟旁白長。**首輪做 1、2、3**（4 視情況隨 2 順做）；試點 **04（測 2）、11（測 3）、08（測 1）**；06 留作第二輪驗收場 |
| ④ | Stage-1 | 不重寫；只做三處外科修改（06 對稱論證後移、20 伴隨極限補動機或移位、13 度數公式延後）——**不在本輪**，放大階段做 |
| ⑤ | 講義對齊 | §3.1 對 `.tex` 的 §8 對齊併入放大階段（本輪不動旁白） |
| ⑥ | 驗收 | 見 §7；R2 重跑用 Opus 5；kickoff 寫完直接開工，人閘只有一個 |

**成功定義（一句話）：** 三場試點在不改一個字旁白、不多一次 TTS 的前提下，靜止比例從 95% 掉到 70% 以下、R2 導演鏡的 ① 級 finding 關閉、verdict 升到 ok 以上，且所有既有閘（schema／lint／sizecheck／23 selftest／doctor --smoke）維持綠。

> **〔2026-09-12 收尾修訂〕上面這條的「靜止比例 < 70%」已被推翻，保留作本輪被判定時所依據的原文。** 六鏡 digest 的相關性分析顯示 `static_ratio` 對 verdict 幾乎無解釋力（r = −0.18），真正的預測因子是 **`longest_still_seconds`（r = −0.82）**；本輪 A/B 自己就是證據——11 升到 `good` 靠的是最長靜止 20.2 s→7.2 s，04 靜止比例動了 3 點但最長靜止 +0.8 s，must 因此沒關。**新驗收線見 §7 第 1 條**，裁決與完整數據見 `REBUILD_STATUS.md` 品質補強輪 ⑧。

## 2. 已驗證的 code 事實（2026-09-12 快照；行號會漂，用 grep）

**揭示模型**
- `pipeline/narration.py` `parse_say`：`say` 依 `{show <id>}` 切成 `Beat(text, reveal)`；marker 之後的文字屬於該 reveal 的 beat。`_SHOW` regex 只認 `{show …}`。
- `pipeline/scene.py` `LessonScene._play_content`：每 beat → 若 `target in by_id and not revealed` 就 `play_block`（回傳動畫秒數）→ `wait(max(audio − consumed, MIN_HOLD))`。**注意它不檢查 `block.static`**：`{show statement}` 指到 static block 會對已在畫面上的 mobject 再播一次 FadeIn（08 的「statement reveal 前後兩幀無差」就是這樣來的）。場末把沒 reveal 的 dynamic block 補揭示。
- `pipeline/blocks.py` `Block(id, mobject, anim, static)`；`play_block` 依 `anim` 字串派發（write／fade／create／grow／slide／highlight／flash_in／write_glow／slide_pop），**或 `anim` 為 callable `(scene, mob, ground) -> seconds`**（hook 用；`timing.stock_animation_seconds` 對 callable 回 None，`make.py _warn_short_beats` 會跳過它）。
- `pipeline/timing.py`：`SCENE_LEAD_SECONDS = 1.0`、`SCENE_TAIL_SECONDS = 1.0`、`MIN_BEAT_HOLD_SECONDS = 0.3`、`STOCK_ANIM_SECONDS` 表、`text_hash`。
- `pipeline/templates/__init__.py` `build_blocks(spec, ctx)` → 各模板 `build` → `_apply_hook`。

**三個試點模板**
- `templates/derivation.py`：`_rows_from_spec` 把 `steps[]`／`result`／`check` 變 rows（rid `step.N`／`result`／`check`，anim `write`／`write_glow`）；`build` 每 row 一個 `Block(rid, group(eq+reason rail), anim, static=False)`；`statement`（motive 行）是 `Block("statement", …, anim="fade", static=True)`。eq mob 由 `brand.math_line` 做（MathTex）。
- `templates/graph.py` `_plot_blocks`：`plots[i]` → `Block(f"plot.{i}", group, anim=create|fade|grow, static=not reveal)`；kind ∈ function／band／line／point；**`dashed: true` 只對 `line` 生效（L324），`function` 忽略它**——11 的 `cos θ` 寫了 `dashed: true` 卻是實線，R2 抓到的就是這個。無 ValueTracker／always_redraw。
- `templates/theorem_proof.py`：statement 卡是 static（docstring「statement is static (the frame)」）；`proof.N`／`qed` 為 dynamic。`PROOF` 小標與 rail 版面見 `statement_regime`／`_rail_card`。

**閘與 TTS（改 storyboard 時會碰到的）**
- `pipeline/sizecheck.py` L576–583（T5）：每個 `{show t}` 的 `t` 必須是 build 出來的 block id，否則 error。新 reveal id（如 `sweep.0`）只要是 Block 就過。
- `pipeline/derive_spoken.py` `check`：canonical 與 `content_scripts/<deck>.spoken.yml` 的 `{show}` marker 序列必須一致。**改 canonical 的 marker 就要同步改 spoken.yml 同一場**，再 `derive_spoken.py --deck ch03_trig_derivatives` 重生 `_mimo.yml`（含 `derived_from` stamp；不重生 make.py 會 STALE 拒跑）。
- `pipeline/tts.py` `scene_reuse_ok`：**scene_text_hash（口語全文、不含 marker）沒變＋WAV 在＋backend/voice 同 → 不重合成，只重 align**（docstring：「Reveal/beat-count-only edits also pass here; the re-map handles them」）。所以**加減 `{show}` 重切 beat 不花錢**；改一個字才花錢。`tts.py --backend mimo` 仍屬計費 CLI：**先 `--dry-run` 確認 planned calls = 0 再跑，若 >0 停下來問**（CLAUDE.md）。
- `make.py _validate_scene_aligned`：reuse 時比 beat 數、`scene_text_hash`、逐 beat `reveal` 名與 `text_hash`；不符就要重跑 tts.py（reuse 路徑）。
- `make.py compose`（L668 起）：scene_aligned 場一場一支 WAV（`narration_by_scene[sid]`）；`pipeline/audio.py` 有 `read_wav_pcm`／`silence_pcm`／`write_pcm_wav`／`concat_wavs`，切接靜音夠用。
- forced alignment 逐字時間在 `output/ch03/s3.1/audio_mimo/align/NN_<id>.words.json`（`{word,start,end,probability}`），beat 邊界＝下一 beat 首字 onset（`scene_align.map_to_beats`）。

**評審工具（本輪驗收用）**
- `pipeline/rewatch_pack.py --deck <deck> [--scene a,b,c] [--out <dir>]`：成片→pack（需 `output/_av/<deck>/<scene>.mp4`，即 make.py compose 產的逐場 A/V 檔）。靜止統計＝4 fps 差分、>0.2% 像素變動算「有動」；細線／小標籤的 reveal 抓不到（會高估靜止）——核實以 manifest reveal 時間為準。
- `content_scripts/_audit/_gen/rewatch_prompts.py --ws <repo 外目錄> --pack <pack> --runs R2 --scenes a,b,c`：組隔離工作區與 prompt；`rewatch_merge.py --ws … --verify verify.json --out …`：合併＋核實 → digest；`rewatch_multilens.gen.py --digest … --out …`：digest → HTML。R2 subagent 跑法見 §7。
- 本輪基線：`output/ch03/s3.1/rewatch_pack/`（2026-07-05 成片；**開工前先複製成 `rewatch_pack_before/`**，pack 目錄 gitignored）。

## 3. 全域護欄（每個 task 都適用）

1. **旁白一個字不改**（LOCKED；NFA 不重開）。只動 storyboard 的非文字欄位、marker 位置、與 code。
2. **零計費**：mock render；真旁白只走 reuse（§2 的 dry-run 規則）；不開 agy／Codex／VLM。R2 重跑＝本 session 的 Opus 5 subagent（使用者已同意）。
3. **零行為改變 for 其他 deck**：所有原語 opt-in（storyboard 欄位或 marker 才啟動），預設路徑逐 token 不變；`_demo_*.yml`、`ch01_inverse_functions.yml`、`ch03_chain_rule.yml` 的 mock render 與 sizecheck 結果不得變。
4. **Karpathy 紀律**（根 CLAUDE.md）：最少 code、不加沒被要求的彈性、外科手術、每個 task 先寫會紅的 selftest 再讓它綠。
5. **selftest 慣例**：`pipeline/_selftest_<name>.py`、平鋪 `assert`、檔尾 runner 迴圈；`python video/pipeline/run_selftests.py` 全綠才算一個 task 完成。
6. **文檔同輪補齊**：`DESIGN.md`（storyboard 新欄位／marker 契約）、`README.md`（模板段）、本檔 task 勾選；Phase 收尾更新 `REBUILD_STATUS.md`。
7. **卡住就停**：§2 事實與實況不符、或原語設計撞上 T5／parity／manifest 契約而需要改契約時，先寫下衝突再問使用者，不要默默繞。

## 4. Phase 0 — 基線（~20 分鐘）

- [ ] **P0-1** `python tools/doctor.py --smoke`、`python video/pipeline/run_selftests.py` 全綠（2026-09-12 基線：smoke 9/9、selftest 23/23）。
- [ ] **P0-2** 複製基線 pack：`output/ch03/s3.1/rewatch_pack` → `rewatch_pack_before`（之後 A/B 用）。
- [ ] **P0-3** 確認 reuse 路徑真的不計費：`python video/pipeline/tts.py --storyboard video/storyboards/ch03_trig_derivatives_mimo.yml --backend mimo --scene difference_quotient_for_sine --dry-run` → 報表 planned calls 應為 0（文字未變）。**若不是 0，停下來報告。**
- [ ] **P0-4** mock render 三場現況一次，確認 `make.py --backend mock --scene difference_quotient_for_sine,squeeze_graph,continuity_statement_sin_limit --quality low` 過全部閘（2026-09-12 已驗 intro 過閘）。

## 5. Phase 1 — 三種原語（code；每個 task：selftest 先紅→綠，mock render 一場驗）

### P1 揭示時序（治「結論先行」「reveal 名存實亡」「難步無停留」）

- [ ] **P1-1 `{show statement}` 讓 statement 卡真的在那一秒進場。** `templates/theorem_proof.py` 與 `templates/derivation.py`：`statement` Block 的 `static` 改為「say 裡沒有 `{show statement}` 才 static」（用 `narration.list_reveal_targets(spec["say"])`）；進場 anim 用 `slide`（0.5 s）。零行為改變：既有 deck 若 say 沒寫 `{show statement}`，一切照舊。08 的 say 已有 `{show statement}`，改完立即生效。selftest：`_selftest_reveal_timing.py`——兩個 spec（有／無 marker）build 後斷言該 block 的 `static`。
- [ ] **P1-2 `PROOF` 小標與第一行證明同時出現。** `theorem_proof.py`：把 `PROOF` 標籤併進 `proof.0` 的 Block group（或給它自己的 dynamic Block、由第一個 `{show proof.0}` 一起揭示）。零行為改變：`{show proof.0}` 不存在時照舊 static。
- [ ] **P1-3 `pauses:` 場級欄位（靜默停留）。** 設計（**不動 `say`、不動 parse_say、不碰 parity／text_hash／FA**）：
  ```yaml
  pauses:                      # 場級，opt-in
    - after: step.2            # 這個 reveal 播完之後
      seconds: 1.5             # 畫面停住、旁白不出聲
  ```
  - `scene.py _play_content`：reveal 播完後，若該 target 在 `pauses` 裡，多 `wait(seconds)`（在 audio hold 之前）。
  - `make.py compose`：scene_aligned／beats 場的 scene WAV 在**該 beat 的 start_seconds**（manifest `beats[i].start_seconds`；reveal 對應的 beat）處切開、插入 `silence_pcm(seconds)`（`audio.py`），寫到 `output/_av/` 前的暫存 WAV；`timeline.json`／`.vtt` 的後續 beat 時間同步 +seconds（T7 的 sidecar 產生器讀同一份偏移）。
  - `sizecheck`／`schema`：`pauses[].after` 必須是 say 裡出現的 reveal id，否則 error（schema.py 新增一條，warn 不擋？——**擋**，指錯的 pause 是 typo）。
  - selftest：`_selftest_pauses.py`——假 manifest＋spec，斷言 (a) scene 端 hold 秒數表，(b) compose 端切接後 WAV 長度＝原長＋seconds、切點前後樣本不變，(c) schema 抓到指錯 id。
  - 零行為改變：無 `pauses` 欄位＝現況。
- [ ] **P1-4（可選，若時間夠）長 beat 拆拍的 authoring 便利：** 無 code；在 §6 的 storyboard 編輯裡直接加 `{show}`（reuse 路徑重 align 不計費，§2）。

### P2 原地變形（治「reveal 只有整塊淡入」；derivation 先做，theorem_proof 順做）

- [ ] **P2-1 `anim: transform` row 選項。** `derivation.py _rows_from_spec`：`steps[i].anim: transform`（`result.anim` 同）→ 該 row 的 Block.anim 改為 callable：`_transform_from(prev_eq_mob, this_eq_mob)`——把上一 row 的 eq mob **複製**一份，`TransformMatchingTex(copy, this_eq, transform_mismatches=True)`（run_time 1.2；MathTex 用 `substrings_to_isolate` 把常見 token 拆開——`=`、`h`、`\frac`、`\sin`、`\cos`、`\theta`，或退而求其次 `TransformMatchingShapes`），同時 reason rail 用 fade 進場；回傳秒數。**前一 row 自動退為 muted**（opacity 0.55；這就是原語 4 的最小形式）。零行為改變：預設 anim 不變。
- [ ] **P2-2 sizecheck 的「最滿幀」不受影響**（終態相同），但 `_warn_short_beats` 對 callable 跳過 → 在 `timing.STOCK_ANIM_SECONDS` 加 `"transform": 1.2`，並讓 derivation 把 callable 的名義秒數掛在 Block 上（例如 `Block.anim_seconds`）供 `stock_animation_seconds` 回傳，短 beat 警告才不漏。
- [ ] **P2-3 selftest `_selftest_transform.py`（manim env）：** 兩 row spec、第二 row `anim: transform` → build 出的 Block.anim 是 callable、名義秒數 1.2；預設 spec 的 Block.anim 仍是 `"write"`。
- [ ] **P2-4 theorem_proof 順做：** `proof[i]` 支援同一 `anim: transform`（proof 行是字串陣列——改成允許 `{tex: …, anim: transform}` 物件，字串仍照舊）。

### P3 游標掃描（治「旁白動詞 vs 凍結畫面」；graph 模板）

- [ ] **P3-1 修 `dashed: true` 對 `function` 無效**（`graph.py` L260 附近：`DashedVMobject(curve, num_dashes=…)`）。11 的 cos θ 立即變虛線。selftest：dashed function 的 Block mobject 型別。
- [ ] **P3-2 `kind: sweep` plot。** 
  ```yaml
  - kind: sweep
    x_from: 1.7         # 游標起點（資料座標）
    x_to: 0.0           # 終點
    seconds: 3.0        # 動畫長度（≤ 該 beat 音檔長度；超過會被 scene.py 補 padding）
    follow: [0, 1, 2]   # 在這些 plot index 的曲線上掛點（function／line 皆可）
    gap: [0, 1]         # 選填：在這兩條曲線之間填半透明色帶，隨游標推進
    leave: cursor       # 終態：cursor（留游標與點）| none（動畫後淡出）
  ```
  實作：`ValueTracker` + `always_redraw` 的垂直線與點；Block.anim 為 callable，`scene.play(tracker.animate.set_value(x_to), run_time=seconds, rate_func=linear)` 後依 `leave` 處理；回傳 seconds。reveal id 沿用 `plot.N`（sweep 也是一個 plot），T5 交叉檢查自然通過。終態要**確定性**（sizecheck 建 scene 不 render，只看終態）：`leave: cursor` 時終態＝游標在 x_to。
- [ ] **P3-3 selftest `_selftest_sweep.py`（manim env）：** sweep block 建得出來、callable、名義秒數＝seconds；`follow` 指到不存在的 plot → build 時 raise（sizecheck 會轉 error）。
- [ ] **P3-4 `tangent` 變體（給 17；本輪可選）：** `kind: sweep` 加 `tangent_on: <plot idx>` 讓一段切線沿曲線滑動。

### Phase 1 收尾
- [ ] `run_selftests.py` 全綠（含三支新 selftest）、`doctor --smoke` 9/9、`_demo_*.yml` 與 ch01 deck mock render／sizecheck 結果與 P0 相同（零行為改變證據）。
- [ ] `DESIGN.md` 補：`pauses:` 欄位、`anim: transform`、`kind: sweep`、dashed function；`README.md` 模板段一行。
- [ ] 對抗 review：依 CLAUDE.md 逐次徵詢——使用者 2026-09-12 說 GPT 額度暫留他用，**優先問要不要用 agy `claude-opus-4-6-thinking --mode plan` 讀 diff**（唯讀、訂閱額度），不要自行呼叫。

## 6. Phase 2 — 試點三場 storyboard（只動 marker 與非文字欄位）

- [ ] **P2-04 `difference_quotient_for_sine`（原語 2＋1）：** `steps[1..2].anim: transform`、`result.anim: transform`；`pauses: [{after: step.2, seconds: 1.5}]`（決定性一步之後停一下）；可選：把 beat 5 的兩個因子聚焦留給原語 4，本輪不做。改 `spoken.yml` 同場 marker（若加了 `{show}`）→ `derive_spoken.py --deck ch03_trig_derivatives`。
- [ ] **P2-11 `squeeze_graph`（原語 3）：** 在 `plots` 末尾加 `kind: sweep`（x_from 1.7 → 0、seconds 3.0、follow [0,1,2]、gap [0,1]、leave cursor），say 裡把「As $\theta$ slides toward zero…」那句前面插 `{show plot.4}`（**只插 marker、不改字**；spoken.yml 同步）。`plots[0]` 的 dashed 生效。
- [ ] **P2-08 `continuity_statement_sin_limit`（原語 1）：** 不改 say（`{show statement}` 已在）；P1-1／P1-2 生效後 statement 卡在 +27.7 s 滑入、PROOF 標籤跟 proof.0 一起出現；加 `pauses: [{after: proof.1, seconds: 1.2}]`（squeeze 那步之後停）。**beat 1 的 27 s 空白需要單位圓縮圖（原語 5／6），本輪不做、記進 §8。**
- [ ] 三場：`derive_spoken.py --deck ch03_trig_derivatives`（重生 `_mimo.yml`）→ `tts.py --backend mimo --scene <三場> --dry-run`（**確認 0 calls**）→ `tts.py --backend mimo --scene <三場>`（reuse＋re-align，本機免費）→ `make.py --storyboard …_mimo.yml --scene <三場> --reuse-audio --quality high`（1080p，真旁白）。

## 7. 驗收迴圈（Phase 2 收尾；機器閘免費、人閘一個）

1. **數字**（2026-09-12 修訂驗收線）：`rewatch_pack.py --deck ch03_trig_derivatives_mimo --scene <三場> --out output/ch03/s3.1/rewatch_pack_after`。對照 `rewatch_pack_before`：
   - **主指標＝`longest_still_seconds`：每個 content 場 ≤ 12 s。** 超過即 finding，但**可用一句理由豁免**（比照 lint／sizecheck 的 warn-default），不自動判死。門檻來源：六鏡 digest 21 個 content 場，`longest_still ≤ 12 s` 放進的 10 個好場（verdict ≥ 2.5）裡命中 6 個、**誤收 0 個差場**；放寬到 14 s 命中 8 個但開始誤收（F1 最佳 0.84，precision 破功）。**閘寧可誤報、不可漏放**，故取 12 s。
   - **次指標＝`static_ratio`（僅記錄、不設門檻）**：它對 verdict 的相關性只有 −0.18，且 `pauses:` 宣告的刻意靜默在它上面是倒扣的。要引用時把 `pauses` 秒數從分母扣掉。
   - 11 的非 reveal 變化 > 0（sweep 確實在動）。
2. **既有閘**：schema／lint／sizecheck 綠；`visual-frame-audit` subagent 看 after 的 fullest frames（V1–V9 0 blocking）。
3. **R2 導演鏡重跑（Opus 5 subagent，使用者已同意）**：`rewatch_prompts.py --ws <scratchpad>/rewatch_ws2 --pack …/rewatch_pack_after --runs R2 --scenes difference_quotient_for_sine,squeeze_graph,continuity_statement_sin_limit`，subagent prompt 比照 2026-09-12（讀 `<ws>/R2/PROMPT.md`、只讀 pack、輸出 JSON 到 `<ws>/R2/result.json`）；before 也跑一次同範圍（或直接用 `_gen/rewatch_lenses/R2.json` 的三場）。驗收線：三場 ① 級 finding 關閉、verdict ≥ ok、無新 must。orchestrator 逐條核實（`rewatch_merge.py --verify` → `rewatch_multilens.gen.py`）→ `REVIEW-ch03_s31-pilot-ab.html`。
4. **人閘（唯一停點）**：把三場真旁白短片（`output/ch03/s3.1/ch03_trig_derivatives_mimo__<scene>.mp4`）交給使用者看，決定要不要放大到全片。

## 8. 明確不做（本輪）＋之後

- 不做：原語 4 獨立標記 `{focus}`／`{hide}`、原語 5 跨場延續、原語 6 圖跟旁白長（06、23、24 的核心改動）、三處內容修改（④）、§3.1 講義 §8 對齊（⑤）、任何重 TTS、六鏡全片再審。
- 之後（人閘通過後的放大階段，另開 kickoff）：三原語鋪滿 27 場 → 原語 4／5／6 → ④ 三處內容修改＋⑤ §8 對齊 → scoped NFA → 重 TTS（先報量）→ 全片 render → 六鏡再審＋新舊 A/B → 教義定案、§3.2 解凍。R7 兩級製作與 R8 停點瘦身在那時一併裁。

## 9. 完成定義（DoD）

三支原語 opt-in 落地、三支新 selftest 綠、`run_selftests.py` 23+3 全綠、`doctor --smoke` 9/9、其他 deck 零行為改變、DESIGN／README 更新、三場試點 after-pack 數字達標、R2 重跑三場 verdict ≥ ok 且 ① 級關閉、`REVIEW-ch03_s31-pilot-ab.html` 產出、三場真旁白 mp4 交給使用者、`REBUILD_STATUS.md` 記本輪。

# KICKOFF — 畫面語法四原語鋪滿 §3.1 27 場（品質補強輪 ⑯）

> **啟動提示（新對話直接貼）：** 讀本檔＋[`SPEC-motion-language.md`](SPEC-motion-language.md)＋[`DESIGN.md`](DESIGN.md) 四個 motion primitive 新節；
> 前一輪＝[`KICKOFF-motion-language-gaps.md`](KICKOFF-motion-language-gaps.md)（T1–T5 已落地、§8 backlog 是本輪的輸入）。
> 全程離線零計費：音檔只重對映（`tts.py --backend mimo --reuse-existing --no-billing`，收據 `backend_calls: 0`）。
> 唯一人閘＝使用者看 27 場 1080p 成片。

## 0. 裁決（2026-09-13）

使用者看完四場試點（04 色表／06 閃爍／07 攜帶＋分段變形／11 放大鏡）後：**「鋪滿 27 場吧，繼續做下一輪」**。
本輪把四原語鋪到 §3.1 全部 21 個 content 場，依 [`SPEC-motion-language.md`](SPEC-motion-language.md) §3 兩級製作：
**規則 4／5 每場零成本一體適用；規則 1–3 每場至少一處**（招牌場做滿）。
前一輪 §8 backlog 裡「放大階段會咬到」的三個 code 缺口一起修（§2），其餘留 backlog。

## 1. 為什麼先修 code 再鋪

試點的三個教訓（REBUILD_STATUS ⑮）決定了鋪滿時的三個必要條件：

1. **transform 1.2 s 填不滿長拍、而且列一改 transform 就失去 `paced`**（`pacing.apply` 跳過 callable）。
   §3.1 的 derivation 拍長 10–16 s（表見 §4），不修就是 21 場裡 8 場「1.2 s 動＋10 s 靜」。
2. **`[stillness]` advisory 對 callable 免檢**——正是上一條的病灶被閘看不見。
3. **`{{}}` 只有 token 級色**：06→07「三塊面積三色」到不等式鏈三項變回單色（R2 ML5 should），規則 5 MUST「同量同色」做不到。

theorem_proof 的 `proof[]` 列沒有 `anim: transform`——16／17（sine／cosine 的證明）與 10 正是「上一列改寫成這一列」的教科書場，
規則 2 在整部片最該出現的地方沒有入口。

## 2. Code 缺口（三個 worktree task；契約定死，實作者不再問）

### T1（agent α）transform 列的 rail 隨讀＋stillness 誠實＋theorem_proof 的 transform

已驗證的 code 事實（2026-09-13，行號會漂）：
- `pipeline/templates/derivation.py:188` `_transform_anim(prev_eq, prev_row, this_eq, *, frame=False)`，morph 那個 `scene.play` 同時 `FadeIn(rail)`（rail＝row VGroup 裡除了 eq 的 leader／reason），回傳 `TRANSFORM_SECONDS (+FRAME_SECONDS)`；`:213` `_cancel_anim` 同型。
  `build` `:398-413` 把 `paced` 完全沒傳進去；`pacing.apply`（`pipeline/pacing.py`）對 `callable(b.anim)` 一律跳過。
- `pipeline/pacing.py` `paced_reveal(scene, mob, _ground)` 用 `TM.beat_run_time(scene, FADE_SECONDS*n)` 取**整拍**當 total——接在 morph 之後直接呼叫會超拍（`scene._play_content` `scene.py:140` 的 `wait(max(target-consumed, MIN_HOLD))` 會被壓到 0.3 s，`_audit_render_sync` 隨即 abort）。
- `pipeline/timing.py:68` `stock_animation_seconds(anim)`：callable → `None`；`make.py:377-380` `_warn_undeclared_stillness` 用它建 `anim_seconds` 表，`None` ＝免檢。
- `pipeline/templates/theorem_proof.py:224` `step_mobs = [brand.prose(p, ground, role="text", size="step", max_width=…) for p in steps]`——`proof[]` 只收字串；`brand.prose` 對 `$…$` 單段走 `math_line` → `_math_tex`，所以 `{{…}}` 分段與色表**已經**在 proof 列生效（`brand.py:406-420`）。
  `:262-279` proof.0 走 `_reveal_with_label(proof_label, inner)`（inner＝paced 時的 `pacing.paced_reveal`），其餘列 `anim="fade"`。
- `definition_math.py:60-74` 是「`math[]` 項可為 `{tex, anim}` dict」的既有寫法，照抄。
- `schema.py:259` `_derivation_issues(sid, scene)` 只對 `template == "derivation"` 跑。

契約：
- **T1-1 `paced` 的 transform／cancel 列：morph 之後 rail 逐段隨讀。** `_transform_anim(..., paced=False)`／`_cancel_anim(..., paced=False)` 加關鍵字參數；
  `paced=True` 時 morph 那個 play **不** FadeIn rail，morph 後把 rail 的 parts（leader、reason，依 VGroup 順序）平均鋪在**拍子剩餘時間**上
  （`remaining = TM.beat_run_time(scene, 0.0) - consumed`；每段 `FadeIn` `pacing.FADE_SECONDS` 再等 gap；n 段切 n 個間隔，同 `paced_reveal` 的理由）；
  `remaining < FADE_SECONDS*n` 或 rail 為空 → 退回現行（rail 跟 morph 同 play）。回傳實際消耗秒數。
  把「切 n 段鋪在 total 上」抽成 `pacing.walk(scene, parts, total) -> float`，`paced_reveal` 改呼叫它（行為逐字不變）。
  `derivation.build` 傳 `paced = r["rid"] in set(spec.get("paced") or [])`。`pacing.apply` 的 docstring 改：transform／cancel 列自己處理 paced。
- **T1-2 stillness 誠實。** transform／cancel 的 closure 設屬性 `anim.fixed_seconds = seconds (+FRAME_SECONDS if frame)`；
  `templates/__init__._apply_carry` 的飛行 callable 設 `fixed_seconds = STOCK_ANIM_SECONDS["carry"]`；
  `timing.stock_animation_seconds(anim)`：callable → `getattr(anim, "fixed_seconds", None)`。
  hook／sweep／`seconds: beat`／paced 走法仍 `None`（真的在填拍）。`make._warn_undeclared_stillness` 註解同步；`DESIGN.md` 「已知盲點」那句改掉。
- **T1-3 theorem_proof 的 `proof[]` 收 dict 列。** `{tex: "$…$", anim: transform, frame: true}`；字串列不變。
  `anim: transform` 且 `i > 0` 且前後兩列都能 `derivation._eq_core` 取到 MathTex → `Block(f"proof.{i}", m, anim=derivation._transform_anim(prev_eq, prev_row_mob, this_eq, frame=…), anim_seconds=…)`；
  proof.0 靜默沿用 stock；不支援 `cancel`（schema error「cancel is derivation-only」）；`paced` 裡同時列了 transform 的 proof 列 → transform 贏（無 rail，文件講明）。
  **所有讀 `proof[]` 的消費端要對 dict 透明**（`grep -rn '"proof"' pipeline/` 逐一看：sizecheck／capacity／provenance／derive_spoken／step_coverage／captions／critic）——比照 `definition_math` 的 `math[]` dict 既有處理；找不到既有 helper 就加一個 `theorem_proof.proof_texts(spec) -> list[str]`。
  `schema._derivation_issues` 擴到 `template == "theorem_proof"` 的 `proof[]` dict 列（`frame` 要配 `anim: transform`；`cancel` → error）。
- **測試：** `_selftest_transform.py` 加 (a) paced transform 在 fake scene 上：morph play 不含 rail、之後 rail 逐段各自一個 play、總秒數 ≤ beat；(b) `stock_animation_seconds(block.anim) == 1.2`／`1.6`（frame）；
  新 `_selftest_proof_transform.py`：dict 列建得出、proof.1 的 anim 是 callable 且 `anim_seconds` 對、**幾何與字串列逐 token 相同**、schema 三條 error、字串列 deck 零行為改變。
  `run_selftests.py` 全綠；`tools/doctor.py --smoke` 與開工前逐字相同（pdftotext 那條 FAIL 是既有環境項）。
- **文件：** `DESIGN.md` `anim: transform` 段補「paced 列的 rail 隨讀」「fixed_seconds」「theorem_proof 的 dict 列」；README 一句。

### T2（agent β）`seg_roles`：`{{…}}` 段級語意色＋06 hook 的三處視覺 advisory

已驗證的 code 事實：
- `brand.py:494` `_math_tex(src, ground, col, fsz)`：分段＋色表 → `MathTex(*pieces)`；色片巢在段內（`MathTexPart` group），頂層一段一個 submobject、`mob._ml_parts=True`。`:543` `math_line(tex, ground, *, role, size)`。
- `derivation.py:71` `_rows_from_spec` 逐列複製 `mark`／`color_role`；`:108` `_eq_mob(row, ground, *, role)` 呼叫 `brand.math_line`。
- 06 hook `animations/ch03_trig_derivatives_hooks.py:265-268` 總結不等式 `ineq = brand.math_line(r"\tfrac12\sin\theta \;\le\; …", role="text")`——單色；三塊區域色＝`secondary`（藍）／`accent`（琥珀）／`success`（綠）（`:118-120`、`:259-264`）。
  `:165` `lB = MathTex("B", …).next_to(B, UL, buff=0.06)`（R2：貼在弧上）；`:182` `l_sin`、`:172` `lth` 落在 0.88 不透明填色上（A6 對比 1.1–1.5:1）。
- schema 對 row 的未知 key 不報錯（`seg_roles` 在 β 合併前只是被忽略）。

契約：
- **T2-1 `seg_roles`**：derivation 的 `steps[i]`／`result`／`check`／`lines[]` 列與 theorem_proof 的 `proof[]` dict 列（T1-3 之後）收
  `seg_roles: {"<段 tex>": <palette role>, …}`——key＝該段 `{{…}}` 內的 tex **原樣去頭尾空白**，value＝theme role（同 `meta.color_map` 的值域）。
  `brand.math_line(..., seg_roles=None)` → `_math_tex(..., seg_roles=None)`：建好後對每個頂層段（`texparts.split_segments(src)` 的順序）比對 key，命中就整段 `set_color(T.color(ground, role))`——**段色蓋過段內色表 token**（作者明寫的段是語意單位；文件講明）。
  沒有 `{{}}` 的列寫 `seg_roles`、或 key 沒對到任何段、或 role 不是 theme key → `schema` **error**（各一條訊息）。幾何逐 byte 不變（selftest 釘）。
  derivation：`_rows_from_spec` 複製 `seg_roles`、`_eq_mob` 傳下去。theorem_proof 的傳遞由主代理在合併 T1 後補（β 不碰 `theorem_proof.py`）。
- **T2-2 06 hook**：`ineq` 改成 `{{\tfrac12\sin\theta}} \;\le\; {{\tfrac12\theta}} \;\le\; {{\tfrac12\tan\theta}}` ＋ `seg_roles` 藍／琥珀／綠（三塊區域同色）；
  `lB` → `next_to(B, UL, buff=0.14)`（離開弧線；UL 在 OC 線之上、是唯一沒填色的方向）；
  `l_sin`／`lth`／`l_tan` 各加一塊 `BackgroundRectangle(label, color=T.color(ground,"bg"), fill_opacity=0.72, buff=0.04)` 墊在標籤下（同 z-index 5 的群組內、bg 在前），對比回到可讀；**`_centre_in_zone` 量到的 `full` 不可因此位移**（bg 不進 `full`，或進 `full` 但 bbox 不變——自己量）。
- **測試：** `_selftest_tex_parts.py` 加：seg_roles 命中的段整段換色、段內 token 被段色蓋過、幾何 parity、schema 三條 error；`_selftest_chord_vs_arc`／既有 selftest 全綠；06 mock render（`make.py --storyboard storyboards/ch03_trig_derivatives.yml --scene sector_inequality --backend mock --quality low`）不炸、`sizecheck` 0 error。
- **文件：** `DESIGN.md` 色表那節加 `seg_roles` 小段；README 一句。

### T3（主代理）鋪 storyboard、驗收、報告

見 §4。

## 3. 護欄

- worktree 內只動自己 task 列的檔；**不動 `storyboards/`**（主代理在 main 上改）；不跑 `tts.py`；不跑 `manim` render 與 sizecheck／selftest 並行（Tex cache race）。
- 每個 task 一個 commit（subject 帶 `[T1]`／`[T2]`），commit 前 `run_selftests.py` 全綠。
- 零行為改變：沒寫新欄位的 deck 逐 byte 同幀（selftest 釘 parity）。
- 回報：改了哪些檔、新 selftest 名、`run_selftests` 數字、任何沒做到的契約條款。

## 4. 鋪法（21 個 content 場；主代理）

拍長（`rewatch_pack_after13`，真 Dean 音檔）與本輪每場的規則落點。「▲」＝本輪新增；未標＝試點已有。
規則代號：ML1 一場一張畫布（carry／exit）、ML2 只動變的 token（transform／`{{}}`）、ML3 框／放大鏡／調暗（focus／indicate／inset／frame）、ML4 靜止是設計的（paced／pauses）、ML5 語意色（color_map／seg_roles）。

| # | 場 | template | 拍長（reveal:秒） | 本輪 |
|---|---|---|---|---|
| 03 | why_trig_is_different | definition_math＋hook | cancels 14.7／math.0 19.2／math.1 12.7／statement 13.5 | ▲ML3 `focus: {at: statement, indicate: [math.1]}`；▲ML1 `exit` 給 04 的 carry 讓路 |
| 04 | difference_quotient_for_sine | derivation＋hook | step.0 7.1／step.1 10.3／step.2 20.9／result 19.5 | ▲ML1 `carry` 03 的 `math.0` 飛右上（旁白「that difference quotient」）；▲ML4 `paced: [step.0, step.1]`（step.1 是 transform → T1-1 rail 隨讀） |
| 06 | sector_inequality | graph＋hook | evenness 17.5／ineq 10.2 | ▲ML5 hook `ineq` seg_roles（T2-2）；▲ML1 `exit` 非攜帶 block |
| 07 | squeeze_to_the_bound | derivation | step.1 12.3／result 16.4／check 13.6 | ▲ML2 step.1 也改 `transform+frame`（T1-1 後 paced 仍有效）；▲ML5 三列 `seg_roles` 藍／琥珀／綠（取倒數＝顏色左右對調，「鏈翻過來」看得見）；▲carry scale 0.35→0.5（縮圖標籤可讀）；▲ML3 `focus: {at: check, indicate: [step.0]}` |
| 08 | continuity_statement_sin_limit | theorem_proof＋hook | proof.0 11.1 | ▲ML3 `focus: {at: proof.0, indicate: [straighten]}`；▲ML4 `paced: [proof.0]` |
| 09 | continuity_argument | theorem_proof | proof.0 15.2／proof.1 16.6／qed 15.4 | ▲ML3 `focus: {at: proof.2, indicate: [proof.0, proof.1]}` |
| 10 | fundamental_limit | theorem_proof | proof.0 12.0／proof.1 10.7／qed 8.0 | ▲ML2 proof.1 `transform+frame`（T1-3）；▲ML4 `paced: [proof.0, qed]`；▲ML3 `focus: {at: qed, indicate: [statement]}` |
| 11 | squeeze_graph | graph | plot.4 8.1／plot.3 6.8 | ▲ML3 `focus: {at: annotation.0, indicate: [plot.3]}`；▲annotation 尾句縮短（孤行）；▲ML1 `exit` 給 12 的 carry 讓路 |
| 12 | limit_not_identity | callout | body 17.9 | ▲ML1 `carry` 11 的 `[axes, plot.0, plot.1, plot.2, plot.3]` 飛右上 0.4（「at θ=π/2 it is 2/π」圖就在旁邊） |
| 13 | radians_essential | callout | body 20.9 | 維持 paced（pull-quote；SPEC §3「其餘比照分段揭示」） |
| 14 | companion_limit | derivation | step.0 9.9／step.1 12.5／result 7.9 | ▲ML2 step.1／result `transform`（step.1 加 `frame`）＋`{{}}`；▲ML4 `paced: [step.0, step.1, result]` |
| 16 | derivative_of_sine | theorem_proof | proof.1 10.0／proof.2 7.6 | ▲ML2 proof.1／proof.2 `transform`（proof.1 `frame`）＋`{{}}`（兩個因子原位各自→極限）；▲ML3 `focus: {at: qed, indicate: [statement]}` |
| 17 | derivative_of_cosine | theorem_proof | proof.1 11.0／proof.2 7.5 | 同 16 |
| 18 | slope_equals_height | graph＋hook | cos_dots 10.4 | ▲ML3 `focus: {at: cos_dots, indicate: [tan_0, tan_halfpi, tan_pi]}` |
| 19 | derivative_cycle | definition_math＋hook | math.1 14.0 | ▲ML3 `focus: {at: math.1, indicate: [math.0]}` |
| 21 | all_six_tan_sec | derivation | step.1 9.6／step.2 7.3 | ▲ML2 step.1 `transform+frame`、result `transform`＋`{{}}`；▲ML4 `paced: [step.1]` |
| 22 | all_six_cot_csc | derivation | step.1 11.5／result 11.9 | 同 21；▲`paced: [step.1, result]`（result 無 rail → 仍靜 10.7 s，< 12 s 閘，advisory 會報、接受） |
| 23 | shm_compute | derivation | result 15.5 | ▲ML2 result `transform+frame`＋`{{}}`（paced 保留→rail 隨讀）；▲ML3 `focus: {at: result, indicate: [step.0]}`；▲ML1 `exit` 給 24 讓路 |
| 24 | shm_stacked_graphs | graph＋hook | g_a 12.3／mirror 11.5 | ▲ML1 `carry` 23 的 `result` 飛右上 0.45（「That is s''=−s, drawn」）；▲ML3 `focus: {at: mirror, dim: [g_v]}` |
| 25 | toward_the_chain_rule | definition_math＋hook | math.0 16.8 | 維持 paced（chips 逐張） |
| 26 | recap | recap_cards | point.* 7–9 | 維持（每拍一張卡） |

不動：intro／outro／4 個 divider；旁白一個字不改（只加 `{show carried.*}` marker → `_mimo` 重 derive、音檔 reuse 重對映）。
`meta.color_map` 維持只有 `\theta`（`h` 仍因 04 hook 自建 MathTex 不進表）。

## 5. 驗收（機器閘全免費；人閘一個）

> **2026-09-13 執行結果：** 1 ✅ T1（`e9226ad`）／T2（`f1bbe6d`）合併後 `run_selftests` **40/40**（38＋T1 的 `_selftest_proof_transform`＋另一 session 的 `_selftest_figure_labels`）、`doctor --smoke` 與開工前逐字相同；2 ✅ schema 0 error、sizecheck 0 error／1 既有 warn、`derive_spoken --check` parity OK；3 ✅ 21 場口語 hash 逐字相同，12（scene_aligned）與 24（beats；beat-1 WAV 依 reveal 改名後才命中 reuse index）重對映收據 `backend_calls: 0`；4 ✅ 27 場 1080p 三次 render（首渲染→24 角落壓 motif、08 V10→回歸），`[stillness]` 誠實後 18 條 advisory 全在 6.3–10.7 s；5 ✅ 視覺幀稽核首輪 **1 blocking**（08 proof 列走 prose 路徑、θ 白 vs 圖赭）→ 改純 math 列後回歸 **0**，advisory 6＋2；6 ✅ `rewatch_pack_after16` 21 場 fine 最長靜止 **全 ≤ 11.5 s**（vs ⑬：04 9.0→7.2、06 9.8→8.2、07 10.0→8.2、08 10.5→7.0、09 11.0→9.8、10 11.8→9.0、14 12.0→9.2、16 9.5→8.2、17 10.8→9.2、21 9.0→6.5、22 11.5→10.8、23 9.8→8.5、24 11.8→11.5）；7 ⚠ R2 Opus 盲審 27 場：**good 9／ok 13／weak 5／bad 0**（試點四場 04／06／07／11 全部 good），must 2／should 22／nice 4，`by_rule` ML1 3／ML2 4／ML3 1／ML4 7／ML5 3——⑬ 的兩條 must（09／12「該有圖」）關掉 12（carry 帶進主圖），09 仍在，**新增 23 shm_compute「彈簧與重物沒畫出來」**（內容提案、同類）；8 ✅ [`REVIEW-ch03_s31-motion-language-rollout.html`](content_scripts/_audit/REVIEW-ch03_s31-motion-language-rollout.html)；9 ⏳ 成片 `output/ch03/s3.1/ch03_trig_derivatives_mimo__rollout16.mp4` 已交使用者（42.5 MiB，只在桌面 app 可見）。
> 執行中的偏離：04 的 carry 放棄（右上無空位）；24 的 carry 改 `bottom_left`（`bottom_right` 壓品牌 motif，sizecheck 不查 decoration 層）；carry 角落水平錨改內容 gutter（`70efe7d`，成片渲染於其前）；theorem_proof dict 列的 `seg_roles` 傳遞未做（無場用到）。

1. T1／T2 合併後 `run_selftests.py` 全綠、`doctor --smoke` 與開工前逐字相同（除既有 pdftotext FAIL）。
2. `schema.py`／`sizecheck.py` 正典 deck 0 error；`derive_spoken --check` parity OK；`_mimo` 重 derive。
3. 零計費證明：改了 marker 的場 `scene_text_hash` 逐字相同 → `tts.py --backend mimo --reuse-existing --scene <ids> --no-billing` 收據 `backend_calls: 0`。
4. `make.py --storyboard storyboards/ch03_trig_derivatives_mimo.yml --reuse-audio --quality high` 27 場；`[stillness]` 清單留檔（T1-2 後它是誠實的）。
5. `critic.py --dry-run` 抽幀（exit 場另抽 exit 前一幀）→ `visual-frame-audit` 子代理 V1–V10：0 blocking（修後回歸）。
6. `rewatch_pack.py --deck ch03_trig_derivatives_mimo --out …/rewatch_pack_after16`：21 場 `fine_longest_still_seconds` ≤ 12 s。
7. R2 導演鏡 Opus 盲審重跑（只讀 pack）：`by_rule` 無新 must、verdict 不降；發現寫進 §7 backlog。
8. HTML 報告 `content_scripts/_audit/REVIEW-ch03_s31-motion-language-rollout.html`（逐場改動＋幀＋數字＋R2 digest）。
9. **人閘**：27 場 1080p 成片交使用者。

## 6. 明確不做

- 09／12 的新 hook（R2 ⑬ 的「這裡該有圖」must，內容提案）；06 主圖放大 2 倍（hook 重排版）；`anim: cancel` 在 §3.1 沒有天然落點（03／04 的消去在 hook 內）；場間真 crossfade；token 級旋轉。

## 7. Backlog（本輪發現）

- **R2 must ×2（皆「這裡該有圖」內容提案）：** 09 `continuity_argument` 全片最長死區、「界塌到 0」只寫不演（另一 session 已認領 `continuity_template` hook）；23 `shm_compute` 全片唯一物理情境沒畫彈簧與重物（未認領）。
- **色軸跨場打架（R2 ML5 pattern）：** 08 hook 藍＝sin 半弦／綠＝cos，而 11／18／24 藍＝cos、琥珀＝sin；08 的 sin 不能改琥珀（弧 θ 已用琥珀，accent≈concept 色相）——這是 Direction B 色軸的取捨，要使用者裁決。
- **prose 行內 θ 不吃色表（視覺閘 advisory 跨 03／07／10／11／12／14 六幀）：** deck 級修法＝在 `$…$` 內對命中 token 注入 dvisvgm `\special{color push/pop}`（不切 part，`Tex(color=None)` 後只補底色），三處入口 `math_line` 混排分支／`_prose_lines`／`heading_rich`。
- **角落複本可讀性：** 07／12 標籤 11–14 px、24 整列 18／12 px（V4／A6 advisory）——`carry` 加「只帶 eq／去標籤」選項或 scale ≥ 0.6；07 carry_in 前 1.4 s 單位圓 y 軸戳進 motive（carry 飛行從 t=0 起或 motive 延後）；24 carried 列整列 success 綠（可加 `seg_roles`）。
- **`[stillness]` 18 條 6.3–10.7 s：** theorem_proof 的 transform 列無 rail 可鋪（16／17／10 morph 後停 8–9 s）、09 proof.2 10.7 s、recap 四卡 7–9 s、25 statement 9.1 s——選項：`pauses:`／statement 閃爍／qed 提早；`_reveal_with_label` 未 paced 時固定 0.5 s 仍回 None（T1 順帶發現）。
- theorem_proof dict 列的 `seg_roles` 傳遞＋`_seg_roles_issues` 擴到 theorem_proof（契約列了、本輪無場用到）。
- 06 主圖太小（⑮ R2 must）仍未動；另一 session 已把右側三個 glyph 改疊層。
- rewatch coarse 0.2% 對書寫動畫盲（R2 引 09「coarse 41.2 s」，fine 9.8 s）：pack 已雙門檻並列，考慮 INDEX 更醒目或 R2 prompt 明講只信 fine。
- 另一 session 的「Tex bbox × 線段取樣求相交」量測已成 `_selftest_figure_labels`（`029ac95`）；建議升成 sizecheck 閘（REVIEW_GATES 自標的盲點）。

## 8. DoD

T1／T2 落地＋selftest 綠＋零行為改變；21 場依 §4 表鋪完；§5 1–8 達標；27 場 1080p mp4＋HTML 交使用者；DESIGN／README／METHODOLOGY §5（hook 內文字一律走 `brand.*`）／SPEC §0／REBUILD_STATUS ⑯ 更新。

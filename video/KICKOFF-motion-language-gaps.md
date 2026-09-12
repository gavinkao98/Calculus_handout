# KICKOFF — 畫面語法五條規則的 code 缺口（motion language gaps）

> 2026-09-13 立檔。本檔給**新 session** 直接開工：§0 可整段貼進對話當啟動提示；§2 是兩個探索代理逐行核過的 code 事實（免重查，行號為 2026-09-13 快照、會漂，用 grep）；§5 是任務、§6 是驗收。規格本體在 [`SPEC-motion-language.md`](SPEC-motion-language.md)（五條規則、證據、驗收信號），裁決在 [`REBUILD_STATUS.md`](REBUILD_STATUS.md) 品質補強輪 ⑭，本檔只摘要、不重述理由。

## 0. 給新 session 的啟動提示（可整段貼）

> 讀 `video/KICKOFF-motion-language-gaps.md` 然後照它做。背景：四支 YouTube 參考影片逐幀拆解（`video/content_scripts/_audit/REVIEW-reference-videos-A1A2B1C1.html`）得出五條畫面語法規則，使用者 2026-09-13 裁決全部進規格（`video/SPEC-motion-language.md`）。規則 4 的 advisory 與規則 5 的 V10 視覺閘、R2 finding 標規則編號已於同日接線；剩下的 code 缺口在本檔 §5：T1 變數色表（規則 5）、T2 inset／框選／閃爍（規則 3）、T3 token 級變形與兩段式消去（規則 2）、T4 跨場攜帶（規則 1）。全程離線零計費（mock render＋現有 Dean 音檔 reuse），每個 task 先寫會紅的 selftest。唯一停點＝§6 的三場短片給使用者看。中途不要停下來問，除非 §3 護欄被觸發。

## 1. 目標與裁決摘要

| # | 裁決 | 內容 |
|---|---|---|
| ⑭ | 規格 | 五條規則進 [`SPEC-motion-language.md`](SPEC-motion-language.md)；本檔只做 SPEC §0 表「缺口」欄的 code |
| ③⑦⑧ | 不動 | 水位「模板層普遍有動」、原語清單 1–7、驗收線 `longest_still_seconds` ≤ 12 s |
| 已接線 | 2026-09-13 | 規則 4 advisory＝`make.py` `_warn_undeclared_stillness`（`pipeline/stillness.py`）；規則 5 視覺閘＝VISUAL-FRAME V10；REWATCH finding 可標規則代號 `rule: ML1`–`ML5`（rubric `rule` 小節＋`rewatch-findings.schema.json`＋merge `by_rule`／gen 小表；R2 MUST 標） |
| 本檔 | 順序 | **T1 → T2 → T3 → T4**（便宜到貴；T4 動到場界，放最後） |

**成功定義（一句話）：** 四個 task 各自 opt-in 落地、selftest 綠、其他 deck 零行為改變；用 §3.1 的三場試點（06 `sector_inequality`、04 `difference_quotient_for_sine`、16 `slope_equals_height`）各示範一條規則，rewatch R2 重跑時規則 1／2／3 對應的 finding 歸零、V10 為 0 blocking。

## 2. 已驗證的 code 事實（2026-09-13 快照）

**顏色（T1 用）**
- `pipeline/visuals/theme.py:258-260` `color(ground, role)`＝`palette(ground).get(role, pal["primary"])`——**未知 role 靜默退回 primary，不報錯**。DARK 六個語意 role `theme.py:124-129`、`*_ink` 提亮版 `:130-131`；LIGHT `:164-169` 逐字沿用講義 hex。palette 只有語意 role、抽象色名、版面色三類，**沒有以數學符號為鍵的顏色**（`templates/`、`brand.py`、`blocks.py` grep `theta` 零命中）。
- `pipeline/brand.py:465-484` `math_line(tex, ground, *, role="math", size="math")`：整個 `MathTex`／`Tex` 一個 `color=`。**`set_color_by_tex`／`tex_to_color_map` 在 `video/` 下 0 次出現**；`substrings_to_isolate` 只在 `templates/derivation.py:151` 的註解（說明為何不用：切 `\frac` 會讓 LaTeX 編譯失敗、擾動間距）。顏色最小顆粒＝一個 mobject。
- `color_role` 讀取點：`templates/derivation.py:71`（steps）、`:77`（result）→ 只套到該列 equation（`_eq_mob` `:95-127`），reason rail（`:173-194`）與 dotted leader（`:286-289`）不吃；`check` 列與 back-compat `lines` 列**沒收 `color_role`**（`:80-91`，刻意或遺漏未確認）。graph：`_role_color(ground, spec, default)` `templates/graph.py:63-66`（`spec["color"]` hex 優先，否則 role），plot 預設 `secondary`（`:396`）、sweep 預設 `accent`（`:317`）；曲線標籤 `_carrier_label_role` `:168-173`；**軸標 `x`／`y` 硬寫 `role="text"`（`:134-135`）、annotations 硬寫 `role="text"`（`:609`、`:703-704`）、刻度 `:87,116,123`——都沒有 per-scene 顏色欄位**。
- deck 級 meta 前例：`schema.py:139-155` 對 meta **沒有 allowlist**（只驗 id／section／title／video）；`meta.assumptions` 的驗證在 `pipeline/pedagogy.py:10-51`（`assumptions_registry_issues(data, enforce)`，severity 隨 `meta.pedagogy_enforce` 升級），讀取在 `templates/_common.py:459-465`；meta 進 template 的路徑＝`scene.py:54` `ctx = {"ground", "meta"}`。

**Block／揭示／focus（T2、T3 用）**
- `pipeline/blocks.py:23-45` `Block(id, mobject, anim="write", anim_seconds=None, static=False, layer="content")`；callable anim 簽章 `anim(scene, mobject, ground) -> seconds`（`:102-103`，None 視為 0）。`play_block` 的實際 run_time 與 `timing.STOCK_ANIM_SECONDS` **有四處不一致**（highlight 0.7 vs 1.2、flash_in 0.5 vs 1.1、write_glow 0.8 vs 1.4、slide_pop 0.45 vs 0.85；`blocks.py:118-137` vs `timing.py:13-27`），成因未確認（疑 Flash 移除後表未同步）。`blocks.py:100` 有個沒用到的 `accent` local。
- `pipeline/focus.py`：`DIM_OPACITY = 0.35`、`FADE_SECONDS = 0.4`（`:29-30`）；`apply(scene, by_id, wanted, currently_dimmed) -> set`（`:51-78`）壓暗前 `save_state()`、還原用 `restore()`（`:74-76`；理由＝`fill_opacity=0` 的空心環會被 `set_opacity(1.0)` 填實），所有動畫塞進**單一** `scene.play(*anims, run_time=FADE_SECONDS)`（`:77`）。套用點 `scene.py:97-101`（reveal 之後、wait 之前），場末 `scene.py:108` 全還原。**`Indicate`／`SurroundingRectangle` 在 `pipeline/` 0 次使用**（只在 `animations/ch01_*_hooks.py:38,163` 手寫 hook）。掛閃爍的自然位置：`focus.py:65-77` 的 `anims` list，或 `scene.py:95-97` 之間。
- `pipeline/pacing.py`：`paced:` 是 reveal id list；`block_parts(mob)` `:42-46` 在 `2 <= len(submobjects) <= PART_LIMIT(8)` 時逐段走；`WRITE_SECONDS_PER_GLYPH = 0.35`、`WRITE_LEAD_SECONDS = 1.0`、`FADE_SECONDS = 0.45`（`:33-39`）；只升級 `not static and not callable(b.anim)` 的 block（`:102`）。
- `templates/__init__.py:51-71` `build_blocks` 順序：intro／outro／divider 直接回傳；content → `REGISTRY[template]` → dark 才前置 `scene_spine` → `_apply_hook`（hook 簽章 `fn(spec, ctx, blocks) -> list[Block]`，`:113-114`）→ `_scaffold_reveal_timing`（`:74-90`）→ `pacing.apply`（最後，`:71`）。
- `templates/derivation.py:148-170` `_transform_anim(prev_eq, prev_row, this_eq)`：`ghost = prev_eq.copy()` → 同一 `scene.play` 內 `TransformMatchingShapes(ghost, this_eq)`＋`prev_row.animate.set_opacity(MUTED_OPACITY=0.55)`＋`FadeIn(rail)`；run_time `TRANSFORM_SECONDS = 1.2`（`timing.py:26`）；第 0 列退回 stock reveal（`:326-328`）。**muted 用 `set_opacity` 且永不還原**（與 `focus.py` 的 save／restore 不一致）。
- `templates/graph.py`：**有 `mode: 2up` 雙面板（`_panel` `:639-679`，id 前綴 `left.`／`right.`）、沒有 inset**（全 repo grep `inset` 只命中兩處無關註解）。`_fit_graph_to_safe_zone(graph_group, title, annotation_group)` `:533-546` 只縮不放、只在 single 模式呼叫一次（`:621`），作用於 `VGroup(axes, *plot mobjects)`。sweep `_sweep_block` `:297-382`：`ValueTracker(x_to)` 建在終點（`:332`）、`band`／`rule`／`dot` 三個 always_redraw 共用同一個 `col`（`:317`）、`leave` 只實作 `"none"`（`:377-380`）、永遠 dynamic（`:382`）。

**場景播放、合成、閘（T4 用）**
- `scene.py:75-111` `_play_content` 每拍：取 `durations[index]`（manifest `audio_seconds`；無 manifest 用 `estimate_seconds`）→ `beat_seconds` 設好（`:93`）→ `play_block`（`:95`）→ focus（`:97-101`）→ `wait(max(target − consumed, MIN_HOLD=0.3))`（`:104`）。場首 `wait(SCENE_LEAD_SECONDS=1.0)` `:62`、場尾 `wait(SCENE_TAIL_SECONDS=1.0)` `:73`（`timing.py:7-9`）。static block 在 build 後全部 `add`（`:62` 之前）。
- `make.py:359-405` **每場各自 `LessonScene().render()`**（class attribute 注入 `spec`／`meta`／`beat_durations`，`:363-365`），mp4 從 `_media/**` 取 mtime 最新（`:396-397`）。compose：先逐段 mux 成 `_av/<output stem>/<sid>.mp4`（`:697-723`），再 `_concat` **stream-copy** `-c copy`（`:655-670`，**不能做 crossfade**）。轉場＝fade-through-black：`_fade_vf` `:518-531`、`_segment_fades(kinds, transition, intra_act)` `:537-548`（brand kinds 用 `transition`，content-content 用 `intra_act`）；`--transition` 預設 0.2（`:807`）、`--intra-act-transition` 預設 None＝同 transition（`:811-814`）。**沒有任何場間 crossfade**；場內只有 intro／outro 的 light↔dark 漸變（`scene.py:164-180`、`:201-215`）。
- **上一場終態座標沒有任何序列化**：`timeline.json` 每場只有 `scene_id／kind／start／end／narration_mode`（`captions.py:86-95`）；`.vtt`、`.chapters.txt` 亦無。→ 跨場攜帶**不靠 sidecar**，靠版面決定性：`sizecheck.check_scenes`（`sizecheck.py:550-571`）本來就對每場 `build_blocks` 而不 render，同一 spec 建出來的 mobject 位置逐次相同。
- 標題釘住：`templates/_common.py:256-293` `scene_head`——eyebrow 上緣 `MASTHEAD_TOP`（`:72`）、title `next_to(eyebrow, DOWN)`（`:290`）、chipless 場也建 `set_opacity(0)` 的 eyebrow 保錨點（`:271-274`）。走 `scene_head` 的 template 標題不漂；沒走的（若有）是漂移來源，未逐一清點 12 個 template。
- `make.py:303-347` `_warn_short_beats(meta, scenes, manifest)`：呼叫點 `:971` 在 `pauses.apply_pauses`（`:969`）之後、`render()`（`:974`）之前，吃的是折入 pauses 的記憶體 manifest；`build_blocks(scene, {"ground": "dark", "meta": meta})`（`:317`，硬寫 dark）；callable 且無 `anim_seconds` 的 block 跳過（`:329-331`）；純 warn。規則 4 advisory `_warn_undeclared_stillness` 在它旁邊（2026-09-13 接線）。
- `schema.py:131-210` `schema_storyboard(data) -> list[(severity, msg)]`，severity ∈ {error, warn}；`_focus_issues` `:43-80`、`_paced_issues` `:82-99`、`_pause_issues` `:102-128` 簽章一致 `(sid, scene, say)`，都只對 `kind == "content"` 跑、都 error。`make.py:840-852` 有 error 即 `return 2`。`sizecheck.py:576-584` 的 `{show}` 目標交叉檢查在 code 裡標 **F9**（不是 kickoff 慣稱的 T5；編號出處未確認）。
- `pipeline/rewatch_pack.py:128-177` `motion_stats` 同時輸出粗（0.2%）與細（0.05%）門檻的 `static_ratio`／`longest_still_seconds`（`fine_*`）；門檻是模組常數不是 CLI 參數（`:57,63`）；CLI 只有 `--deck`／`--scene`／`--out`（`:283-285`）。**另一個 session 2026-09-13 正在改此檔**，開工前 `git log -1 -- video/pipeline/rewatch_pack.py` 看最新。
- REWATCH rubric `REWATCH-REVIEW-RUBRIC.md:45-55` R2 六個維度（`D-motion`／`D-focus`／`D-carry`／`D-composition`／`D-continuity`／`D-dwell`）；R4 `:75-76` 的 `T-still`「超過 15 秒」與 `T-beat`「超過 25 秒沒有 reveal」**與 ⑧ 的 12 s 驗收線、規則 4 的 6 s advisory 三個門檻語意不同**（authoring advisory／量測閘／模型判讀），見 §5 T5。

## 3. 全域護欄（每個 task 都適用）

1. **旁白一個字不改**（LOCKED；NFA 不重開）。只動 storyboard 非文字欄位、marker 位置、與 code。
2. **零計費**：mock render；真旁白只走 reuse（`tts.py --dry-run` 確認 planned calls = 0）；不開 agy／Codex／VLM。R2 重跑＝Opus 5 subagent（使用者 ⑦ 已同意的機器閘）。
3. **零行為改變 for 其他 deck**：所有新欄位 opt-in；`_demo_*.yml`、`ch01_inverse_functions.yml`、`ch03_chain_rule.yml` 的 mock render 與 sizecheck 結果不得變。
4. **Karpathy 紀律**（根 CLAUDE.md）：最少 code、不加沒被要求的彈性、外科手術、每個 task 先寫會紅的 selftest 再讓它綠；`python video/pipeline/run_selftests.py` 全綠才算一個 task 完成（glob 發現 `_selftest_*.py`，`python -m pipeline.<name>`、cwd=video/；manim-backed 的要 `_bootstrap.bootstrap()` 先跑）。
5. **文檔同輪補齊**：`DESIGN.md`（新欄位契約，放「motion primitive」各節旁）、`README.md` 模板段、`SPEC-motion-language.md` §0 表「缺口」欄改「已有」、本檔 task 勾選；收尾更新 `REBUILD_STATUS.md`。
6. **卡住就停**：§2 事實與實況不符、或設計撞上 F9／parity／manifest 契約而需要改契約時，先寫下衝突再問使用者，不要默默繞。
7. **不碰另一個 session 的工作樹**：開工前 `git status`，凡已被修改而非本 kickoff 的檔一律不動。

## 4. Phase 0 — 基線（~20 分鐘）

- [x] **P0-1** `python tools/doctor.py --smoke`、`python video/pipeline/run_selftests.py` 全綠（2026-09-13 基線：smoke 9/9、selftest 33 份含 `_selftest_stillness`）。
- [x] **P0-2** `git log -1 -- video/pipeline/rewatch_pack.py video/pipeline/templates/graph.py video/pipeline/templates/derivation.py` 確認 §2 行號仍對；漂了就 grep 更新本檔。
- [x] **P0-3** 三場試點 mock render 現況：`python video/make.py --storyboard video/storyboards/ch03_trig_derivatives_mimo.yml --backend mock --scene sector_inequality,difference_quotient_for_sine,slope_equals_height --quality low` 過全部閘；把 `[stillness]` 行留底當 before。
- [x] **P0-4** `rewatch_pack_before` 已存在（⑬ 用過）；若被覆寫就重跑一次留底。

## 5. Tasks

### T1 規則 5 — deck 級變數色表（token 級語意色）

- [x] **T1-1 `meta.color_map`（deck 級，opt-in）。**
  ```yaml
  meta:
    color_map:                 # 變數／幾何量 → palette role；值只能是 theme 已有的 role 名
      "\\theta": concept
      "d\\theta": caution
      "\\sin": result
  ```
  `schema.py` 新增 `_color_map_issues(meta)`：mapping、key 非空字串、value 是 `theme.palette("dark")` 的 key（warn-default，`meta.color_map_enforce` 才 error）——比照 `pedagogy.assumptions_registry_issues`。**未知 role 不能再靜默退 primary**：這裡要明說。
- [x] **T1-2 `brand.math_line` 讀色表。** 有 `color_map` 時改建 `MathTex(tex, tex_to_color_map={k: T.color(ground, role)})`（manim 的 `tex_to_color_map` 走 `substrings_to_isolate` 語意，**只能對「不切壞巨集」的 token**——`\frac` 內部不切）。先寫 selftest：`\frac{\sin(h/2)}{h/2}` 加色表後仍能編譯、`\theta` 子 mobject 顏色＝role 色；`\frac` 本身不在色表時整式仍為單色。**編譯失敗就退回單色並 warn**（不炸 render）。呼叫端：`derivation._eq_mob`、`theorem_proof` 的 proof 行、`definition_math` 的 math 行都經 `math_line`，改一處全通。
- [x] **T1-3 graph 讀同一張表。** 軸標 `x`／`y`（`graph.py:134-135`）、annotations（`:609,:703`）改為「文字含色表 key 時逐 token 上色」；plot 的 `color_role` 缺省時若 `label` 含色表 key 就用該 role。填色（band／sweep gap）沿 plot 的 role，不另加欄位。
- [x] **T1-4 selftest `_selftest_color_map.py`**（manim env）：三案例（有表／無表／壞 role），加 schema 案例。`_selftest_semantic_palette.py` 不得受影響。
- [x] **T1-5 試點：** `ch03_trig_derivatives.yml` `meta.color_map` 只放 `\theta`、`h`、`\sin`、`\cos` 四個，render 04 與 16 看 V10 是否成立（同一 θ 在圖與式子同色）。

### T2 規則 3 — inset 放大鏡、變動前框選、強調閃爍

- [x] **T2-1 `focus[].indicate`（閃爍變體）。** `focus:` 每筆新增選填 `indicate: [<block id>…]`：那一拍 reveal 後，對這些 block 播 `Indicate(mob, scale_factor=1.15, color=T.color(ground, accent_role(spec)+"_ink"))` 0.8 s，接在 `focus.apply` 的同一個 `scene.play` 裡（`focus.py:65-77`）或緊接其後（`scene.py:95-97`）；`consumed` 加上秒數。schema：id 必須存在（sizecheck 交叉檢查比照 `dim`）。**Indicate 與 `.animate` 混在同一 `play` 的行為先用 mock render 驗過再定放哪**（§2 未確認項）。
- [x] **T2-2 變動前框選。** `derivation` 的 `anim: transform` 加選填 `frame: true`：morph 前 0.4 s 先在**上一列即將變動的部分**畫 `SurroundingRectangle`（先整列，token 級等 T3），morph 時同步 FadeOut；`anim_seconds` 加 0.4。零行為改變：預設 false。
- [x] **T2-3 graph `inset:`（主圖不縮放的放大鏡）。**
  ```yaml
  inset:                       # graph single 模式，opt-in
    x: [0.0, 0.6]              # 資料座標矩形
    y: [0.0, 0.6]
    corner: top_right          # 放在版面哪個角；大小固定 3.2×2.0 u
    follow: true               # 主圖的 plot／sweep 更新時 inset 跟著（always_redraw）
  ```
  實作：第二組 `Axes` 用同一批 plot spec 重建但 `x_range`／`y_range` 換成矩形、`include_ticks=False`；主圖上畫矩形框（`hairline_strong`）＋兩條虛線導引到 inset；inset 白邊框。整組是 `Block("inset", …, layer="graph", static=False)`，`{show inset}` 才進場。`_fit_graph_to_safe_zone` 要把 inset 排除在 group 外（它固定在角落，不隨主圖縮）。selftest：build 出來、id 對、`_fit` 前後主圖 bbox 不變。
- [x] **T2-4 試點：** 06 `sector_inequality` 加 `inset`（單位圓上 θ 附近的小區域）＋`indicate` 那三塊面積；04 加 `frame: true`。

### T3 規則 2 — token 級變形、兩段式消去

- [x] **T3-1 作者分段語法。** derivation 的 `math` 允許 `{{…}}` 分段（同 Motion Canvas／Manim `MathTex(*parts)` 語意）：`"{{\\sin(x+h) - \\sin x}} = {{2\\cos(x+h/2)}} {{\\sin(h/2)}}"`。`brand.math_line` 遇到 `{{` 就 `MathTex(*parts)`（每段一個 submobject；段內巨集完整，不會切壞 `\frac`）。無 `{{` 時行為不變。selftest：分段數＝submobject 數；混色表（T1）時段內再套 `tex_to_color_map`。
- [x] **T3-2 `anim: transform` 升級為對位。** 兩列都有分段時用 `TransformMatchingTex(ghost, this_eq, transform_mismatches=True)`（key＝段的 tex 字串），否則沿用 `TransformMatchingShapes`。新段 `FadeIn`、消失段 `FadeOut`、其餘平移——這就是 C1 的「只動變的 token、鄰居讓位」。run_time 仍 1.2 s。
- [x] **T3-3 `anim: cancel`（兩段式消去）。** `steps[i]: {math: …, anim: cancel, cancel: [1, 3]}`：先把上一列第 1、3 段 `FadeOut`（0.4 s，位置不動，讓讀者確認是哪兩項互消），再對剩餘段做 T3-2 的對位變形到本列（0.8 s）；`anim_seconds` 1.2。
- [x] **T3-4 graph 曲線「畫出來」。** 純 authoring：SPEC 規則 2 要求 function plot 用 `reveal: true`＋`anim: create`（既有機制，`graph.py` plot anim=create|fade|grow）；本 task 只在 `DESIGN.md` 的 graph 段加一句「新稿預設 create」，並把 `_demo_graph_reveal.yml` 改成 create 當範本。無 code。
- [x] **T3-5 試點：** 04 `difference_quotient_for_sine` 四列改分段＋`transform`，最後一列 `cancel`（消 h/2 那對）。

### T4 規則 1 — 跨場攜帶（物件面的原語 5）

- [x] **T4-1 `carry:`（場級，opt-in）。**
  ```yaml
  carry:                       # content 場；被攜帶的物件在本場開場就在
    - from: sector_inequality  # 前一個 content 場（同一幕內）
      block: plot.0            # 該場 build 出來的 block id
      as: carried.circle       # 本場的 block id（{show carried.circle} 可指；預設 static）
      to: keep                 # keep＝原位；或 {corner: top_right, scale: 0.35}（複本飛去角落當 inset，在 {show as} 那拍飛）
  ```
  實作（`templates/__init__.py` 新的後處理 `_apply_carry(spec, ctx, blocks)`，放在 hook 之前）：`ctx["scenes_by_id"]`（`make.py` 與 `sizecheck` 建 ctx 時塞進整個 deck 的 scenes）→ 對 `from` 場 `build_blocks(prev_spec, ctx)` → 取 `block` 的 mobject `copy()`（終態＝版面決定性，§2）→ `restore()` 到未壓暗（focus 場末已還原；transform 的 muted 0.55 要在複本上 `set_opacity(1)`）→ `to: keep` 時 static 加進 blocks；`to: {corner, scale}` 時 dynamic，anim callable＝`mob.animate.scale(s).to_corner(...)` 0.8 s。**遞迴上限一層**（from 的場不再展開它自己的 carry）。
- [x] **T4-2 場界零淡黑。** `make.py _segment_fades`：若下一段的 spec 有 `carry` 且 `from` 是上一段，這條邊界兩側 fade＝0（硬切；被攜帶物件位置相同就看不出切）。其餘邊界不變。selftest 用 `_selftest_make_transition.py` 既有慣例加案例。
- [x] **T4-3 `exit:`（選填）。** 場級 `exit: [<block id>…]`：場尾 `SCENE_TAIL_SECONDS` 內把這些 block `FadeOut`（0.5 s），讓沒被攜帶的物件在切場前退場、被攜帶的留著。無 `exit` 行為不變。
- [x] **T4-4 schema／sizecheck。** `_carry_issues`：`from` 必須是同一幕（divider 之間）且緊接的前一個 content 場、`as` 不與本場 block 重複、`to` 形狀合法（error）；sizecheck 交叉檢查 `block` 在 `from` 場 build 得出來（error）。這就是 SPEC §4 第四項「攜帶宣告存在性」。
- [x] **T4-5 試點：** 06 → 07 `squeeze_to_the_bound`：把單位圓與三塊面積 `carry` 到 07 並飛去右上角當 inset；07 → 08 再 keep。這正是 A2 65 s 與 C1 675–750 s 的手法。

### T5 三個門檻對齊（純文檔，一次做）

- [x] REWATCH rubric R4 `T-still` 的「超過 15 秒」改「超過 12 秒」（與 ⑧ 驗收線一致；`T-beat` 25 s 維持，它量的是「沒有 reveal」不是靜止）；在 rubric 加一句三層門檻的分工：**6 s＝authoring advisory（未宣告靜止）、12 s＝量測閘（`longest_still_seconds`）、R4 模型判讀沿用 12 s**。同步 `SPEC-motion-language.md` 規則 4 落地段。

## 6. 驗收迴圈（Phase 收尾；機器閘免費、人閘一個）

> **2026-09-13 執行結果：** 1 ✅ selftest 38/38、smoke 9/9、三個非試點 deck 閘報表逐字相同；2 ✅ 視覺閘首輪 1 blocking（06 V10）→ 修後回歸 0；3 ✅ `rewatch_pack_after14` 最長靜止 04 9.0／06 9.0／07 11.2／11 7.2 s；4 ⚠ R2 重跑 06 good／11 good／04 ok／07 ok，`by_rule` ML1 2／ML2 5／ML3 1／ML4 2／ML5 3——規則 finding 未歸零（多為 should，唯一 must 在 04 的 hook lane），DoD 第 4 項只達「無新 must、verdict ≥ ok」；5 ⏳ 四場短片已交使用者。試點場次改為 04／06／07／11（理由見 §8 首段與 commit `9ce0429`）。

1. `run_selftests.py` 全綠、`doctor --smoke` 9/9、三個非試點 deck mock render＋sizecheck 與 P0 相同（零行為改變證據）。
2. 三場試點 mock render → `visual-frame-audit` subagent 看 fullest frames：V1–V10 0 blocking（**V10 必看**：θ 在 04 的式子與 16 的圖同色）。
3. `rewatch_pack.py --deck ch03_trig_derivatives_mimo --scene sector_inequality,difference_quotient_for_sine,slope_equals_height --out …/rewatch_pack_after`：`fine_longest_still_seconds` ≤ 12 s；06 的 `non_reveal_events` > 0（inset／indicate 在動）。
4. R2 導演鏡重跑（Opus 5 subagent，同 ⑦ 流程）：finding 標 `rule: ML1`–`ML5`（2026-09-13 接線）；digest `by_rule` 裡 ML1／ML2／ML3 在三場歸零、verdict ≥ ok、無新 must。
5. **人閘（唯一停點）**：三場真旁白短片（reuse 音檔）交給使用者看，決定要不要鋪滿 27 場。

## 7. 明確不做（本輪）＋之後

- 不做：場間真 crossfade（要重編碼邊界、動 `_concat`；T4-2 的硬切＋同位置已達目的）、鏡頭 zoom 原語（規則 3 明說不是第一選擇）、收尾閉環的自動化（用 `carry` 回 recap 場即可，手工）、`play_block` 與 `STOCK_ANIM_SECONDS` 四處不一致的修正（先記進 §8 backlog，修時要重量所有 deck 的 `_warn_short_beats`）。
- 之後：四 task 鋪滿 §3.1 27 場 → 六鏡再審＋新舊 A/B → 教義定案、§3.2 解凍；R7 兩級製作以 SPEC §3 為分界。

## 8. Backlog（本輪發現、不在本輪修）

**試點驗收（2026-09-13 視覺閘回歸 0 blocking、R2 重跑）留下的 advisory／should，下一輪放大階段處理：**
- 04 `difference_quotient_for_sine`（hook lane）：step.0 列一次寫完後靜止 9 s（ML4，改 paced 或逐 token 亮起）；beat 6 的兩個因式應從上一列複製搬下來而不是重打（ML1）；`write h = 2·h/2` 註記比它指的分母晚 11 s 才出現（ML3）。
- 06 `sector_inequality`（hook lane）：主圖太小（430×400 px），beat 3–4 的 `frame`／`apex` 揭示在變化偵測裡無對應項——R2 must（ML3），處方＝beat 3–4 期間主圖放大約 2 倍再縮回；`sin θ`／`θ` 標籤落在 0.88 不透明青填色上對比 1.1–1.5:1（A6 high，加 `bg` 底板）；點 B 標籤貼在弧上（V2 advisory，`next_to(B, LEFT)`）；總結不等式三項未繼承三區塊色（ML5；需 `{{}}` 段級 role，見下）。
- 07 `squeeze_to_the_bound`：縮圖 0.35 倍下標籤 7–9 px 讀不到（A6 med；carry 只帶幾何或 scale ≥ 0.5，待裁決）；R2 want「三個部位就地取倒數、兩個 ≤ 原地旋轉 180°」（ML4 should，token 級旋轉是 T3 的下一步）。
- 11 `squeeze_graph`：annotation 第二行只剩 `θ = 0.` 孤行（A6 med，改寫尾句）；plot.3 那拍「Notice the open circle」畫面無新動作 6.8 s（ML4 should；空心圈延到該拍才畫）；inset 把 `reveal: true` 的空心圈提早顯示（β 已知限制）。
- **`{{}}` 段級 role**：色表是 token 級，「½ sin θ 青／½ θ 金／½ tan θ 綠」這種「一段一色」需要 `math_line` 收 `roles: [..]` 對段上色（T1 延伸）。
- **hook 自建 MathTex 不吃色表**：06 三個標籤已改走 `brand.math_line`，其他 hook（04 的 `inter`／`parts_eq`、08 chord_vs_arc、16、18）尚未；hook 撰寫規則應寫進 CONTENT_METHODOLOGY §5：凡文字一律經 `brand.math_line`／`brand.prose`。
- **palette 觀察（待裁決）**：`accent` 琥珀 `#f2b13c` 與 `concept` 赭 `#d98f3c` 色相幾乎相同，θ 的專屬色在 accent 物件旁失去辨識力；規則 5 只要求同量同色，這是 Direction B 色軸的取捨問題。
- `[stillness]` advisory 對 callable 免檢的盲點在試點真的咬到（07 首跑 result 拍 16 s 只有 1.2 s transform 沒被抓）：可讓 template 對 transform／cancel／carry 回報真實 `anim_seconds` 而非免檢。

- `blocks.py` `play_block` run_time 與 `timing.STOCK_ANIM_SECONDS` 四處不一致；`blocks.py:100` dead local。
- `derivation.py` `check` 列與 `lines` 列不收 `color_role`。
- `derivation._transform_anim` 的 muted 用 `set_opacity(0.55)` 永不還原，與 `focus.py` save／restore 不一致（T4-1 的複本要手動還原）。
- 12 個 template 是否全走 `scene_head`（標題釘住的全覆蓋性）未清點。
- `graph.py` sweep 的 `leave` 只實作 `none`；cursor／point／gap 共用一個顏色。

## 9. 完成定義（DoD）

T1–T4 各 opt-in 落地、四支新 selftest 綠、`run_selftests.py` 全綠、`doctor --smoke` 9/9、其他 deck 零行為改變、DESIGN／README／SPEC §0 更新、T5 三門檻對齊、三場試點 after-pack 數字達標、R2 重跑三場規則 finding 歸零且 V10 為 0、三場真旁白 mp4 交給使用者、`REBUILD_STATUS.md` 記本輪。

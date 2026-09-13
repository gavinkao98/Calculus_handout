# Runbook — MiMo 旁白雙版／影片路線（指派給單節 session 用）

> 這是「最新方法」的可貼提示詞。把下方 fenced 區塊整段貼給負責**某一節**的 session，
> 填入該節的 `DECK` / `SECTION`。權威細節：`video/README.md` §「MiMo 旁白／影片路線」、
> `video/DESIGN.md` §「MiMo 口語軌」、`video/REBUILD_STATUS.md` 2026-06-14 節。

**前提（重要）：** 此路線需要該節的**正典 storyboard** `video/storyboards/<deck>.yml`（含 `say` ＋ `{show}`）。
`storyboards/` 現況＝`_demo_*.yml`（模板示範／回歸樣本）＋已落地的正典 deck（如 `ch03_trig_derivatives.yml`——
首個走完本路線全程的節）＋版面回歸 deck（`ch01_inverse_functions.yml`）。任一章節在**該節 storyboard 落地前
先別跑本路線的影片步驟**；可先用下方「念法慣例」＋ NFA（旁白忠實稽核，原 Mode B）把口語版納入認可包，
storyboard 落地後再走完整流程。

---

```
你負責 NTU 微積分影片產線（repo Calculus_handout，video/ 子樹）某一節的「MiMo 旁白雙版／影片」產出。
全程用繁體中文溝通；動手前先讀 video/README.md §「MiMo 旁白／影片路線」、video/DESIGN.md §「MiMo 口語軌」、
該節 content_scripts/<deck>.md 與 storyboards/<deck>.yml。

DECK: <填，如 ch01_precise_limit>      SECTION: <填，如 §1.6>

步驟 0（前提檢查，先做）：
- 確認 storyboards/<deck>.yml 存在（含 say + {show}）。不存在就停手回報——本路線在 storyboard 落地後才跑
  （旁白須先認可 → 出 storyboard）。

步驟 1 — 寫口語單一源 content_scripts/<deck>.spoken.yml：
- 每個 content scene 一筆 `scene_id: | <口語旁白>`；把該 scene 已認可 narration 的英文散文「逐字保留」，
  只把每個 LaTeX 數學式攤成口語，並把 {show ...} 標記留在與正典 say 相同的位置（順序/目標一致）。
- 念法慣例（務必遵守；**權威＝NARRATION-FAITHFULNESS-RUBRIC.md 的念法慣例節**，此處為操作摘錄、衝突時以 rubric 為準）：
  · f^{-1} → "f inverse"（絕不 "f to the minus one"；例外：課文刻意對比 sin^{-1} 與 1/sin 時，該處照字面念）
  · 下標 x_1,x_2 → "x sub one / x sub two"
  · 和/差根號 √(y-2) → "the cube root of the quantity y minus two"
  · 群組次方 (∛(x-2))^3 / (f^{-1}(x))^2 → "…, all cubed / all squared"
  · 座標 (a,b) → "the point with coordinates a and b"；區間 [a,b] → "the interval from a to b"
  · 反三角 arcsin → "arcsine of …"；π/2 → "pi over two"；分數念 "one half / nine-fifths" 等
- 只改數學念法，不動英文散文用詞。

步驟 2 — 生成＋parity 檢查（不呼叫任何 API）：
  python video/pipeline/derive_spoken.py --deck <deck> --check   # 必須印 "parity OK"
  python video/pipeline/derive_spoken.py --deck <deck>           # 生成 _mimo.yml + _narration_spoken.md
  （這兩個生成檔標 DO NOT EDIT；要改旁白改 .spoken.yml 後重生。）

步驟 3 — NFA 旁白忠實稽核（原 Mode B；read-only）：
  契約＝ content_scripts/_audit/NARRATION-FAITHFULNESS-RUBRIC.md（維度 D1–D7、收斂線、reader 拆法）。
  gate1（Claude subagent，免費）迭代到 blocking==0：1 個 narration reader 跑 D1–D6；CONTENT_APPROVED=no 時
  另開 1 個隔離盲 reader 跑 D7（獨立重算）。收斂後再跑 gate2（Codex，計費、需同意）單次確認。
- cp content_scripts/_audit/PROMPT-narration-faithfulness.template.md → _audit/PROMPT-<deck>-narration-faithfulness.md，填 {{...}}。
  該節旁白「尚未經使用者認可」就把 CONTENT_APPROVED 設為 no（會打開 D7 數學內容正確性維度）。
  gate2 範例：codex exec -s read-only < video/content_scripts/_audit/PROMPT-<deck>-narration-faithfulness.md \
      > <gitignored scratchpad>/REPORT-<deck>-narration-faithfulness.raw.txt 2>&1
  （**raw 輸出不進版控**——落 scratchpad，findings 與裁決轉錄進下行的版控 REPORT-<deck>-….md；2026-07-07 與講義線統一。）
- 收斂：依 Keep/Rewrite/Cut 改 <deck>.spoken.yml → 重跑 derive --check → 回歸審核 →
  寫乾淨的 REPORT-<deck>-narration-faithfulness.md。NFA 裁決寫進該次修正 commit 的 message body（CLAUDE.md，`git log --grep="NFA"`）。

步驟 4 —（須先徵得使用者同意：MiMo 雖免費仍屬外部 API）合成＋render：
- 確認 .env 有 MIMO_API_KEY。預設走 `mimo-v2.5-tts` 的 builtin voice `Dean`（經 `audio.voice` 選定、
  不送 style/persona prompt；voice-design/Calm Professor 已於 2026-07-05 退役）。先 smoke
  （mimo_preview.py --smoke）確認回應形狀。**報價依據：先跑 `--dry-run` 取「預期／最壞 call 數」**
  （`tts.py … --backend mimo --dry-run` 印逐場 planned/worst 表＋est 分鐘；worst 已把 fallback ladder 每非空 beat
  計入；reuse 可再往下降，報價時註明）。**`--backend` 為必填**（無預設，防裸跑誤燒/誤蓋）。報用量、徵同意後：
  python video/pipeline/tts.py  --storyboard video/storyboards/<deck>_mimo.yml --backend mimo
  python video/make.py          --storyboard video/storyboards/<deck>_mimo.yml --reuse-audio --quality high
  → output/chNN/sX.Y/<deck>_mimo.mp4（1080p 預覽；正式交付才 --quality 4k）
  （成片旁另出 `<stem>.timeline.json`／`.vtt`／`.chapters.txt` sidecar；真音檔路徑另 two-pass loudnorm 到 house
  -19 LUFS；離線聽感驗收＝`python video/pipeline/listening_pack.py --manifest <…/manifest.json>`。）
- **合成單位 `--unit`（scene-level TTS＋forced alignment，2026-07-05；batch-2 全 template＋rung 3 於 2026-07-06；設計見 DESIGN.md「Manifest schema 2」）：**
  `tts.py` 預設 `--unit auto`——**全部 content template（10 個，單一源＝`pipeline/template_names.py:CONTENT_TEMPLATES`）**：
  `callout`／`definition_math`／`derivation`／`graph`／`procedure_steps`／`recap_cards`／`sign_chart`／`theorem_proof`／
  `value_table`／`worked_example`（2026-07-11 T3 補齊 procedure_steps/value_table/sign_chart——原手維護 allowlist 只有 6/9；
  2026-09-13 新增 worked_example，9→10；parity
  selftest 守 registry 一致）走 scene-level（一場一次合成、`stable-ts` 回推 beat 時序、
  per-scene validation，過不了自動回退 beat）。要全走舊路用 `--unit beat`；單一場強制 scene 用 `--unit scene`。
  **紀律：scene-level 真合成只在 narration lock＋NFA 之後**（「改一個字→整場重合成」的 blast radius 由 lock 吃掉）；
  lock 前一律 `make.py --backend mock`（beats、零計費、離線）迭代。**§7 fallback ladder＝arbiter(免費)→resynth(1 call)
  →chunk(sentence-chunk，N 個 billed sub-synth)→beats(budget-exempt 終點——不佔 rungs 2–3 budget，但 MiMo 下每非空
  beat 仍一次 call、非免費)**；scene-level 合成報價時要把 fallback 預算一併列入：
  預設 `--fallback-budget 2` 只夠 resynth，**要啟用 chunk 救援得把 budget 調到覆蓋 fan-out（1＋該場句數），句數即 billed
  sub-synth 數、須併入報價**——chunk 會自檢 budget、不足即 decline 退 beats（不偷跑爆預算）。
- **只改 `{show}` marker、要重對映 beat 時，`--reuse-existing` 是必要的，漏掉就整批重合成。**
  `tts.py:1054` 的 `use_reuse = args.reuse_existing and …` 決定要不要建 reuse index；**沒下這個旗標，
  index 是空的，`scene_reuse_ok` 根本不會被問到**，每一個被 `--scene` 選到的場都會從頭合成——與
  `scene_text_hash` 相不相同無關。2026-09-12 實測代價：5 場（hash 全部逐字未變）**13 次 billed call**，
  其中一場再降到 beats 終端（`--fallback-budget` 只管 rungs 2–3，管不到終端）。正確寫法：
  `tts.py --backend mimo --reuse-existing --scene <ids> --no-billing`——補上 `--reuse-existing` 後
  同一個 deck 實測 `backend_calls: 0`。
- **`--no-billing` / `--max-billed-calls N`（2026-09-12 新增）＝把「這次應該不花錢」變成保證而非預期。**
  上限涵蓋整個 run（含 beats 終端）；超過的那一次呼叫直接中止。因為 WAV 要等該場閘全過才 promote，
  中止時 manifest 與既有音檔原封不動，可以安全重試。
- **ASR QA 探針對「逐字母唸讀」會誤報。** `sector_inequality` 把點唸成 `O A B`／`O A C`，ASR 轉成
  `OAB`／`OAC`（另有 `disc`→`disk`、`one`→`1`），`qa_diff` 讀成 3-token replace ⇒ verdict `fail` ⇒
  整場被判 fail 而去重合成。該場需要 `--skip-qa`（manifest 會誠實記成 `qa.status=skipped,
  reason=--skip-qa (intentional)`）。判斷是不是誤報：離線跑 `SA.align_scene` + `run_gates`，對齊
  本身過就是探針誤報，不是 take 有問題。
- **〔2026-09-13 訂正〕上一條不是某一場的特例——scene-level 重合成一律下 `--skip-qa`。**
  探針誤判的對象是**所有被 spell out 的數學**，不只逐字母唸的點名：“pi over one hundred eighty”、
  “s double prime equals negative s”、“sine prime equals cosine” 一樣會被 ASR 轉回數字與符號、
  一樣變成 replace ⇒ `fail` ⇒ 重合成。實測（Task D，6 場）：**只給場 06 下旗標時，四場跑下來三場
  被退回重試，7 次 billed call 一場都沒 promote**（`--max-billed-calls` 擋住，什麼都沒污染）；
  六場全下 `--skip-qa` 後 **5 場 5 次呼叫、0 retry**。QA 改成事後看：`manifest.json` 的
  `gates.qa` 仍然誠實記錄 skipped，要真做 QA 就離線另跑探針、不要讓它決定要不要重花錢。
- **〔2026-09-13，已修〕beat 級 reuse 的 key 已從「輸出檔路徑」改成「`scene_id` ＋ beat 文字 hash
  ＋ backend/model/voice/style」；搬場與加／移 `{show}` marker 不再計費。**
  舊行為（兩次各花掉計費呼叫的那個坑）：`build_reuse_index` 建的是
  `{該 beat 的 audio_file 絕對路徑: {…, text_hash}}`，而路徑是
  `beats/<兩位數場號>_<scene_id>/<兩位數序>_<reveal>.wav`——**場號與 reveal 都進檔名**。於是
  (a) 任何場序調整（例：Task B-4 把 `companion_limit` 往前搬，`derivative_of_cosine` 由第 16 場
  變第 17 場）、(b) 在場中間加／移一個 `{show}` marker（檔名換、其後每一拍序號位移），都會讓整場
  beat 路徑失配，工具**把整場每一拍重合成**，即使一個字都沒改。
  **現行為：** 命中與路徑無關；命中後若新舊路徑不同就**把 WAV 搬到新路徑再登記**，log 印
  `reused <新檔名> (moved from <舊路徑>)`（搬完舊目錄若空就刪掉，免得變成沒人認領的孤兒 WAV 去
  絆 `overwrite_guard`）。同一場兩拍文字相同時依 index 配對，同一份 take 不會被登記兩次。
  離線實測（`--no-billing`，真音檔）：把 `continuity_argument` 的場號改成 07、第一拍檔名改成別的
  reveal 名（文字一字未改）→ `backend_calls: 0`，五拍全部 `reused (moved from …)` 搬回
  `beats/09_continuity_argument/`。**不必再手動複製 beats 目錄＋改 manifest 了**（上一版教的
  `.bak` 手術做法已作廢）。
  §3.1 目前走 beats 路線的三場是 `continuity_argument`(09)／`derivative_of_cosine`(17)／
  `shm_stacked_graphs`(24)。
- **〔2026-09-13，已修〕`--scene` 子集併回 prior manifest 時，`scene_number` 一律以當前 storyboard
  的全 deck 序號重算**（intro／divider 也佔號，與 `rewatch_pack.py`／`critic.py` 同一套數法），
  換號的場其 WAV／align sidecar／beat 目錄一併搬到新號。舊行為是沒被重跑的場沿用舊值，於是
  §3.1 的 manifest 裡 `derivative_of_cosine` 與 `slope_equals_height` 同為 17（critic 抽幀撞號，
  當時由 critic 改讀 storyboard 序繞過）。離線實測：一次 `--no-billing` 的子集跑就把 5 場
  （`divider_derivatives` 14→15、`derivative_of_sine` 15→16、`slope_equals_height` 17→18、
  `derivative_cycle` 18→19、`divider_apply` 19→20）修正並搬檔，27 場場號唯一且與 storyboard 對齊。
- **`--dry-run` 現在會把 reuse 算進 `plan` 欄**（多一個 `reuse` 欄＝既有音檔已覆蓋的計費單位，
  TOTAL 行另印 `(no-reuse: N)` 保留悲觀報價）。所以「加一個 marker 要不要錢」在 dry-run 就看得出來。
  **但 `plan` 是「有下 `--reuse-existing` 才算數」的數字**——沒下旗標時它會多印一行 NOTE 告訴你
  真正會 billed 幾次（就是 2026-09-12 那 13 次的成因）。`worst` 欄對 scene-level 仍是 reuse-blind
  （reuse 的 WAV 仍可能重對齊失敗而掉 ladder）。
- **〔2026-09-13，已修〕scene-level（`scene_aligned`）的場同樣處理：兩種模式都會自動搬，搬場後的
  第一次真跑就是 0 次。** scene WAV 是 `scenes/<場號>_<scene_id>.wav`、對齊檔是
  `align/<場號>_<scene_id>.{words,aligned}.json`，一樣把場序嵌進檔名；`build_scene_reuse_index`
  以 `scene_id` 為 key 本來就找得到「哪一份音檔屬於這一場」，出問題的是 `scene_reuse_ok` 被餵
  「今天的場號」去找它，搬場後那裡是空的 → 重合成。現在 `adopt_prior_scene_artifacts` 會在
  freshness 檢查**之前**先把舊 WAV＋兩個 sidecar 搬到今天的號（同一套 copy→驗大小→刪舊→空目錄
  rmdir 規則），命中就印 `reused <新檔名> (moved from <舊路徑>)`。
  **搬檔是無條件的**（即使文字改了也搬）：re-synth 走 temp＋gates 過才 promote，所以搬過去的檔在
  有好的替代品之前不會消失；而不搬就會在舊場號下留孤兒 WAV。
  離線實測（`--no-billing`，真音檔）：把 `companion_limit`（B-4 被搬過的 scene_aligned 場）的場號
  與三個檔名改回 20（文字一字未改）→ `--reuse-existing --no-billing --skip-qa --scene companion_limit`
  得 `backend_calls: 0`、log 印 `reused 14_companion_limit.wav (moved from …20_companion_limit.wav)`、
  WAV 與兩個 sidecar 都搬回 `14_`、20_ 的舊檔全部清掉、`validation: pass_with_warnings`。
  （scene-level 重對齊一律記得帶 `--skip-qa`，理由見上面 2026-09-13 那條；不帶的話 ASR 探針誤判
  會判 fail 而去重合成。）
- **beats 模式的場跑 `tts.py` 一律帶 `--unit beat`。** `--unit auto` 只看 template，會把它們路由去
  scene-level ＝ 1 次計費（然後才可能一路掉回 beats 終端，那還更貴）。§3.1 目前走 beats 的三場是
  `continuity_argument`／`derivative_of_cosine`／`shm_stacked_graphs`。實測：
  `--reuse-existing --no-billing --scene shm_stacked_graphs,derivative_of_cosine`（不帶 `--unit beat`）
  在第一次呼叫前就被 `--no-billing` 攔下；補上 `--unit beat` 後 `backend_calls: 0`。
  scene_aligned 的場則用預設 `--unit auto` 即可。
- `make.py --reuse-audio` 會先驗 manifest freshness（deck id、scene、beat count、`{show}`、
  `text_hash`、WAV 存在/時長；`scene_aligned` 另驗 scene WAV＋words/aligned 檔＋`validation.status`），再 render；
  若報 stale/incomplete，不要硬跳過，先重跑該 storyboard 的 `tts.py` 或確認是不是選錯 `<deck>_mimo.yml`。
- 若出現 `[sync] short/reveal-only beat warning`，通常是連續 `{show a} {show b}` 或短空 beat；
  優先把其中一個 reveal 合併到有旁白的 beat，或接受它作為 deliberate visual pause。
- render 後 `[sync] render/audio lengths clean` **必須**出現——2026-09-13 起是硬閘：影片短於旁白、或
  |video − expected| 超過 `SYNC_HARD_GATE_FRAMES`＝2 影格（fps 由 ffprobe 對成品實測），`make.py` 自己就
  ERROR、compose 前 abort，不會有 warn 可以帶過（閘定義見 [`REVIEW_GATES.md`](REVIEW_GATES.md) §一 層 6）。
- render 後跑 `python video/pipeline/rewatch_pack.py --deck <deck>`（要留底就加 `--out <dir>`；要跟
  上一輪比就加 `--baseline <上一輪 pack dir>`）：`[still-gate] PASS` 才算該輪完成，exit 1＝有 content 場
  0.05% 細門檻最長靜止超過 12 s（FAIL 行帶所在拍）、exit 2＝基線 fps／尺寸不同、拒絕 A/B。verdict 在
  pack 的 `PRODUCTION.md`。**注意 `--scene` 子集打進既有 pack 目錄會整個覆寫 `INDEX.md`／`pack.json`，
  子集一律另給 `--out`。**（[`REVIEW_GATES.md`](REVIEW_GATES.md) §六 6.3／6.4）
- 驗收：在幾個 reveal beat 的時間點抽幀，確認 reveal 準時出現＋LaTeX 無亂碼（光看 exit code 不夠）。

規則：
- MiMo 非決定性——同文字每次合成是不同 take（±~10% 長度）；滿意的 take 不要重合成。
- 不要編輯生成檔（_mimo.yml、_narration_spoken.md）；改 .spoken.yml 重生。
- 未經要求不要 commit。任何計費/外部 API 呼叫前先報用量徵同意（CLAUDE.md）。
```

---

**只想聽聲音（不出影片）：** `python video/pipeline/mimo_preview.py --spoken content_scripts/<deck>_narration_spoken.md`
（`--dry-run` 不呼叫 API；`--smoke` 只合首段）。要臨時回到內建音色試聽時，加
`--model mimo-v2.5-tts --voice Dean`（或 `Mia` / `Chloe` / `Milo`）。

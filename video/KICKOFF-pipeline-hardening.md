# 影片產線硬化 — 執行清單（kickoff）

> **狀態：** v6（2026-07-11，經 Codex `gpt-5.6-sol`／max **六輪**回歸複核，**已收斂＝0 blocking，可交付**）。來源＝使用者提供的外部產線 review（9 條建議＋文檔清理）經本 repo 逐條對碼驗證後的收斂版。**v1→v2** 第一輪 8 blocking；**v2→v3** 第二輪 NB1–NB4；**v3→v4** 第三輪 R3-B1–B4；**v4→v5** 第四輪 R3-B1 nested-shape＋advisory；**v5→v6** 第五輪 R3-B1 完整收尾（consumer 對齊）。**第六輪（收斂確認）：Codex 逐 consumer 列 deref 表，判 R3-B1 closed、無下一層、不誤傷合法 manifest（repo 5 份＋§3.1 的 27 場全 `ok`）、0 blocking。** 差異總表見 §2.1；事實主張全數查證屬實（證據見 §2）。
> **用途：** 交給**新 session** 逐項執行的工作清單。每個 task 自帶：改哪些檔（含行號錨點）、目標行為、實作／測試步驟、驗收指令、commit 建議。
> **範圍界定（使用者 2026-07-11 裁決）：** §3.1（`ch03_trig_derivatives`）定性為**實驗品**——本清單**不含**任何 §3.1 補 render／補修工作；產線硬化完成後 §3.1 **整節重做**，屆時作為新產線的全流程驗收 deck。
> **零計費原則：** 本清單**所有** task 均為離線工作（mock TTS、本地 render、ffmpeg、doc 編輯），**不需要**任何真 MiMo TTS／VLM／Gemini 調用。若執行中發現某步驟似乎需要計費 API，停下重新界定，不要調用。
> **⚠️ 換行敏感（Codex B1 查實）：** 本 repo `core.autocrlf=true`、無 `.gitattributes`；正典 storyboard 在 Windows 工作樹是 **CRLF**、git blob 是 **LF**（`git ls-files --eol` 實測 `i/lf w/crlf`）。任何「對檔案內容做 hash」的地方**一律先正規化成 LF 文字**再 hash，**不可** `read_bytes()`——否則跨機（CRLF↔LF）會誤判。T1 已據此設計。

---

## 0. 給新 session 的啟動提示（可整段貼）

```
你負責執行 video/KICKOFF-pipeline-hardening.md（影片產線硬化執行清單）。全程繁體中文溝通。

開工前先讀：根 CLAUDE.md（計費同意閘、Karpathy 工程準則、Codex read-only standing consent）、
本 kickoff 全文、video/DESIGN.md、video/REVIEW_GATES.md、video/RUNBOOK-mimo-narration-route.md。

規則：
- 依 Phase 順序執行；task 內照步驟走（先寫測試、跑紅、實作、跑綠、commit；subject 帶 task id，如 [T1]）。
- 全計畫零計費 API：任何步驟都不需要真 MiMo TTS。測試一律用 storyboards/_demo_*.yml 或
  --output-dir/--manifest 指到 scratch 目錄，不碰 output/ch03/s3.1/ 下的真音檔。
- 標「裁決件」的 task（T9、T10）做到產出 A/B 交付物就停，等使用者裁決後再繼續。
- 每個 Phase 收尾：跑該 Phase 全部 selftest ＋ `codex exec -s read-only` 對抗 review
 （standing consent，逕行），blocking 修完回歸審核再進下一 Phase。
- 完成或中斷時：勾掉本檔對應核取框，並在 video/REBUILD_STATUS.md 補一行進度。
從 Phase 0 開始。
```

---

## 1. 目標與架構

**Goal：** 在 §3.2（chain rule）進 TTS／render 之前，堵掉產線三個結構性缺口——生成稿漂移、計費面不可稽核、QA 靜默略過——並在批量產前補齊聽感驗收、輸出配套與編碼鏈。

**架構取向：** 全部是對既有模組的外科手術式修改＋少量新的 manim-free 小模組；不重做模板、不換 TTS 路線、不引入新框架。每項改動配 `pipeline/_selftest_*.py` 慣例的離線自測（`python video/pipeline/_selftest_X.py` 直接跑、平鋪 `assert`、無 pytest）。

**Tech stack：** 現有 Python 產線（`video/pipeline/`、`video/make.py`）、ffmpeg、stable-ts／whisper-timestamped（既有本地依賴）。

---

## 2. 背景與已驗證事實（免重查；行號為 2026-07-11 快照）

新 session 不必重新考證下列事實，直接引用；行號若因後續 commit 漂移，以描述為準。

| # | 事實 | 證據錨點 |
|---|------|---------|
| F1 | `derive_spoken.py --check` 只驗三件事：scene 覆蓋、spoken 無 `$`、`{show}` marker 對齊；**從不比對已生成的 `_mimo.yml` 是否過期** | `pipeline/derive_spoken.py:83-100` |
| F2 | `ch03_trig_derivatives_mimo.yml` 現況 stale：正典的 `hook:` 行（Task 14 #3 `derivative_cycle`、#6 `toward_the_chain_rule`）與 `sparse_ok`（#7）都不在生成檔裡；成片 mtime（07-05 18:38）早於這些 commit（`e15ecc1` 20:40、`90e6001` 20:54、`354d21c` 20:28）；stale 生成檔還被 `27e95f5`（07-06）進了版控 | `git log -- video/storyboards/ch03_trig_derivatives.yml`；兩檔 grep `hook:`／`sparse_ok` |
| F3 | `tts.py --backend` 預設 `mimo`（裸跑即外部 API）；同意閘只存在於文件流程、不在 code | `pipeline/tts.py:263` |
| F4 | `--dry-run` 只印 beat 總數，不反映 `--unit auto` 的 scene-call 結構與 fallback fan-out；§3.1 實際 ~36 次 billed calls vs 21 場 | `pipeline/tts.py:871-878`；`REBUILD_STATUS.md` §3.1 行 |
| F5 | `--scene` 子集跑完 `main()` 以**全新** manifest dict 覆寫整份 manifest（局部重做會毀掉其餘場的紀錄） | `pipeline/tts.py:882-919` |
| F6 | fallback ladder 的 `beats` 終端 rung 宣告非計費、不受 `RetryBudget` 管，但 mimo backend 下實際逐 beat 呼叫 API | `pipeline/tts.py:793-799`；`pipeline/scene_fallback.py:18-28` |
| F7 | beat 路徑**沒有** scene 路徑的 verify-before-overwrite promote 機制（`_synthesize_scene_beats` 直接寫 beat WAV）→ 誤跑 mock 會把真 Dean WAV 蓋成靜音 | `pipeline/tts.py:507-553` vs `:825-829` |
| F8 | ASR QA probe 結果沒進 manifest：`_finalize_aligned` 把 `qa` 放進 gates（`tts.py:631`），但 `build_scene_aligned_entry` 的 `validation` 只搬 status/warnings/metrics，`qa` 落地即丟；且 `_asr_probe_tokens` 對 ImportError／任何例外 **silent return None**（缺套件＝靜默略過） | `pipeline/tts.py:600-606,625-634`；`pipeline/scene_align.py:431-456` |
| F9 | `{show}` 只驗語法不驗 target 存在（schema.py 明寫 out of scope）；typo target 在 player 端靜默跳過、收尾補播（錯時序不炸 render）；**sizecheck 已對每場 `build_blocks`**（含 hook 後的最終 block ids），cross-check 落點現成 | `pipeline/schema.py:10-14`；`pipeline/scene.py:69-88`；`pipeline/sizecheck.py:557-570` |
| F10 | `--unit auto` allowlist 註解宣稱「full content-template set」但 frozenset 只有 6/9，缺 `procedure_steps`／`value_table`／`sign_chart`（§3.2 很可能用到 `procedure_steps`）；registry 共 9 個 content template | `pipeline/tts.py:48-55`；`pipeline/templates/__init__.py:34-47` |
| F11 | `templates/__init__.py` → `blocks.py` 頂層 `from manim import ...`：**tts.py 必須保持 manim-free**，不能直接 import registry | `pipeline/blocks.py:18` |
| F12 | 每場固定 1s lead＋1s tail；`--transition` 預設 0.2（每邊）→ 每個場景邊界 ~0.4s fade-through-black；此為刻意設計（docstring 明寫呼應 intro/outro dark-handoff motif） | `pipeline/timing.py:7-8`；`pipeline/scene.py:56,67`；`make.py:472-486,617-620` |
| F13 | 編碼鏈：manim render 一次 → fade 時 mux `libx264` 再編一次 → `_concat` **無條件**再編一次；全程 libx264 預設值，無 CRF／BT.709 標記／faststart | `make.py:489-511,513-523,550-563` |
| F14 | word timestamps（`align/*.words.json`）與 per-scene beat 時間戳都有；全片 scene offset 只在 compose 內隱式存在；無 timeline.json／srt／vtt／chapters 輸出 | `make.py` grep 無 srt/vtt/chapter |
| F15 | 文檔 stale（②級，補文件即可，非真衝突）：`DESIGN.md:219`「待使用者裁決」vs `:237-239`「使用裁決出的 bed」；`README.md` 稱 forced alignment「實驗線」但 production 已在 `pipeline/scene_align.py`；1080p/4K 三處敘述可調和。**Codex Adv6 補：此清單不完整**——另有 `README.md:162` house cue 仍稱待裁決（實際 Candidate B 已落地）、RUNBOOK「全部 content template」仍列 6/9、`ENVIRONMENT.md`／`tools/doctor.py` 仍稱 FA 為 optional experiment 且 PASS 路徑指向 experiment script。全部歸 T11 | 各檔對應行 |
| F16 | §3.1 的 3 場 beat-fallback（`continuity_argument`／`derivative_of_cosine`／`shm_stacked_graphs`）有使用者既有裁決「先不用修、**勿自行重試 scene-level**（燒 billed API）」。**Codex Adv4 補：** 另有 `fundamental_limit`／`recap` 兩場經 arbiter rung 救回（仍是 `scene_aligned`），故 manifest 中 `fallback_history` 非空的是 **5 場**（3 beats＋2 arbiter），非 3 場 | `REBUILD_STATUS.md:20`；`output/ch03/s3.1/audio_mimo/manifest.json` |

**與原 review 建議的三處做法修正**（已比對取捨，新 session 不必重議）：

1. 漂移治理**先做 hash freshness gate**（T1），不先做「in-memory overlay 取代 `_mimo.yml`」——後者架構上更乾淨但牽動 `meta.id` 後綴選目錄（`tts.py:854`）、成片命名、RUNBOOK 指令等多處，列入 §7 deferred。
2. **不把 `--backend` 預設改 `mock`**——因 F7，誤跑 mock 會毀真音檔，只是把「誤燒錢」換成「誤毀資料」。改為 `--backend` 必填＋manifest backend 不符拒絕覆寫（T2a）。
3. allowlist **不直接吃 templates registry**——因 F11 會把 manim 拖進 TTS 環境。改共用 manim-free 常數模組＋manim-env parity selftest（T3）。

## 2.1 v1→v2 Codex 回歸修正總表（8 blocking＋advisory）

新 session 只要照 v2 各 task 執行即可；本表僅供追溯「為何這樣改」。每條均經本 repo 對碼查實（`gpt-5.6-sol`／max，唯讀）。

| Codex | 嚴重度 | 問題 | v2 落點 |
|-------|--------|------|---------|
| B1 | blocking | T1 hash 只記 canonical、漏 `.spoken.yml`；且 `read_bytes()` 對 CRLF 敏感、跨機誤判 stale | T1-1/T1-2/T1-4：兩輸入都記、hash 正規化 LF 文字 |
| B2 | blocking | T1 freshness 插在 schema 前、無 `isinstance` 防護，malformed YAML 會先噴 `AttributeError` 蓋掉 schema 診斷 | T1-2：非 dict／meta 非 dict 一律回 `None`，把錯誤讓給 schema |
| B3 | blocking | T1-7／T5-4 驗收直接改 tracked 檔再 `git checkout --`，會丟工作樹既有未提交修改 | P0-3 存 dirty 底＋護欄；T1-7／T5-4 改用 `TemporaryDirectory` 複製 |
| B4 | blocking | T2 仍有洞：損壞 manifest fail-open 放行→mock 蓋真音檔；`merged_manifest` 只比 `deck_id`→混音色/backend 說謊 manifest | T2a：損壞即 abort＋WAV-without-manifest 拒寫；T2c：identity 全同才 merge、force-switch 只准 `--scene all` |
| B5 | blocking | mock「全流程」不可靠：scene mode 仍載入 stable-ts（非全離線）、靜音→beats→無 `validation.qa`，驗不到 T4 | P1-END-1：整合測試固定 `--unit beat`；T4-4：monkeypatch/fake 測控制流 |
| B6 | blocking | T7 字幕硬寫 `SCENE_LEAD_SECONDS`（`--lead` 可調→錯位）、chapters 取不存在的 `title`、不濾空 cue、固定檔名互相覆寫 | T7 全面重寫：名綁 output stem、lead 記進 timeline、title fallback 鏈、跳空 cue、T6/T7 路徑用顯式 `--timeline` |
| B7 | blocking | T9 兩版 A/B 寫同一 deterministic mp4（`make.py` 無 `--output`）→ 互相覆寫；且 output gitignored、無法 commit mp4 | T9-1 先加 `--output`；A/B 用不同檔名；只 commit code/HTML/hash |
| B8 | blocking | beat fallback 計費敘述矛盾：F6 已證逐 beat 計費，但 T3 註解仍寫「免費/at most one billed」 | T3-2 註解改寫；T11 列入所有 docstring/RUNBOOK/DESIGN 同步修正 |
| Adv1 | advisory | dry-run 不讀 reuse index、空 beat 不呼叫 backend、`--fallback-budget` 可負、retry 兩分支 | T2b 欄名改 `planned calls (ignoring reuse)`＋空 beat 分開計＋validate `>=0`；T2d retry 兩處都加 |
| Adv2 | advisory | T4 測試只驗序列化、`--skip-qa`/`qa_wav None` 的 warning 政策不一致 | T4-2 明定 warning 政策；T4-4 加控制流測試 |
| Adv3 | advisory | T5 多加的「未 reveal dynamic block」warning 是未要求的噪音功能；`make.py` 無 sizecheck-only | T5-1 只留 missing-target error；T5-2/T5-4 直接跑 `sizecheck.py`＋temp storyboard |
| Adv4 | advisory | T6-4 驗收數字不精確（fallback 是 5 場非 3；舊 manifest 全無 `qa`） | T6-4 改為「3 terminal-beat＋2 arbiter-recovered」、qa 三態分辨、`html.escape` |
| Adv5 | advisory | T10-3 把過多未定義 mastering 綁一起；`silencedetect` 會誤報設計內建 1s lead/tail | T10-3 首輪只做 target＋two-pass loudnorm＋I/TP；逐場 LU/silence 另立 task |
| Adv6 | advisory | T11 漏本輪新增資料契約（`derived_from`/`receipt`/`validation.qa`/sidecars）與 `--force-backend-switch` 文檔；F15 不完整 | T11 增列；F15 註記補 README house/RUNBOOK/ENV/doctor drift |
| Adv7 | advisory | Phase 3「STOP 等裁決」與「裁決不阻塞其他 task」矛盾（T10 STOP 則 T9 起不了） | §7 順序改：T9、T10 各自產 A/B→標 `awaiting`→一次交裁決 |
| Adv8 | advisory | P0-3 Bash `\|\| echo` 吞失敗、且本環境 shell 是 PowerShell | P0-3 改 PowerShell、累積 `$failed`、非零 exit |
| Nit1/2 | nit | import 需在 `sys.path.insert` 後；`test_..._is_batch2` 名過時；`.srt` 屬額外功能 | 各 task 內註明；`.srt` 降為選用 |

**v2→v3（Codex 第二輪：v2 新 code 引入的 4 blocking＋partial closure＋新 advisory）**

| Codex | 嚴重度 | 問題 | v3 落點 |
|-------|--------|------|---------|
| NB1 | blocking | v2 的 `merged_manifest` identity 檢查在**合成完**才跑——同 backend 但 voice/model/style 不同時，WAV 已改寫、已 billed 才 raise | T2a：identity 檢查移到 **preflight**（`overwrite_guard` 收 `intended`、在 `build_backend`/寫檔前判定）；`merged_manifest` 降為 backstop |
| NB2 | blocking | v2 `read_manifest_status` 只要 `json.loads` 成功就 `ok`——`{}`／`null`／list 會 fail-open 或 `.get()` 噴錯 | T2a：root 非 dict 或缺 `backend`/`scenes` 一律 `corrupt`；corrupt/orphan 復原要 `--force-clobber` **且** `--scene all` |
| NB3 | blocking | v2 T7 chapters 取 `scene["title"]`，但 timeline/manifest 都沒有 title（在 storyboard）；fallback 順序又把 `meta.title` 排在 `tagline` 前 | T7-2：`chapter_title` 由 compose 端算好寫進 timeline；順序改 `title→tagline→meta.title→id`；captions 只讀 timeline |
| NB4 | blocking | v2 T7-6 用 `--lead 2` 產成片當驗收，但 `render()` 不接 lead、`LessonScene` 永遠 wait 1s → A/V 錯位 | T7：不改 render；compose 遇非預設 lead 印 WARN；驗收不跑非預設 lead，lead-awareness 改由 T7-5 單元測試證明 |
| B4 餘 | blocking | 見 NB1/NB2 | 同上 |
| B6 餘 | blocking | 見 NB3/NB4 | 同上 |
| B8 餘 | blocking | v2 T11-11 只列 tts.py/RUNBOOK/DESIGN，漏 `scene_fallback.py:57`／`_selftest_scene_align.py:316` 等 active code | T11-11 改 grep 掃全部；並保留正確的「arbiter 免費」不誤改 |
| NA1 | advisory | `check_derived_freshness` 接受任意 inputs，production 若漏傳 spoken 不會被抓 | T1-6 明確斷言重生 deck 的 `derived_from.inputs` 恰為兩筆 |
| NA2 | advisory | `--fallback-budget>=0` 只在 dry-run 內驗；T2d receipt 說 beat 模式＝beat 總數 | 驗證移 `main()` 開頭無條件；receipt/dry-run 一律**非空 beat 數** |
| NA3 | advisory | T6 `--manifest` 必填 vs fallback 矛盾、`--timeline` 無用途、排序與「terminal-beat 排前」衝突 | `--manifest` 純必填、砍 `--timeline`；排序改 fail＞terminal-beat＞warnings＞qa非ran＞WPM＞clean |
| NA4 | advisory | T9/T10 的說明 HTML 要 commit，但沒指定放 gitignored `/video/output/` 之外 | 說明 HTML 落 tracked `video/_audit/`，mp4/WAV 留 output 用路徑+hash 引 |
| Karpathy | advisory | `text_sha256` 的 `read_bytes()` fallback 違反本檔「不可 read_bytes」規則、且屬未要求彈性 | T1-2 移除 fallback，純 `read_text`（decode error 就該炸） |

**v3→v4（Codex 第三輪：v3 的 partial-closure 收尾＋新 code 回歸）**

| Codex | 嚴重度 | 問題 | v4 落點 |
|-------|--------|------|---------|
| R3-B1 | blocking | `read_manifest_status` 對 `scenes:null`／`scenes:{}`／`scenes:[null]` 仍判 `ok`，下游 `.get()`／iteration 崩潰 | T2a：`backend` 須 str、`scenes` 須 list-of-dict，否則 corrupt（僅頂層 shape，不深驗每 beat） |
| R3-B2 | blocking | full run 換 identity（`sample_*`/`output_dir`）放行後仍沿用 reuse，可能留舊 WAV 卻寫新 header | T2a：任何 identity diff → `use_reuse=False`、空 reuse index 強制全合成 |
| R3-B3 | blocking | v3 T7-2 只給 timeline JSON 範例，沒接線——`compose()` 現況無 `meta`/`quality`/storyboard 路徑，取不到 `chapter_title`/`meta.title` | T7-2：明列 `compose()` 新增 `meta`/`quality`/`storyboard_path`/`manifest_path` 參數＋main wiring；`chapter_title` 抽純函式 |
| R3-B4 | blocking | T11-11 linewise grep 漏跨行 `non-billed 'beats'`（`scene_fallback.py:37-38`）；掃 `_audit` HTML 命中 base64 | T11-11 改 multiline `rg`＋擴詞（non-billed/unbilled/零計費）；明列 :37-38；並保護正確的 `billed=False` code flag 不誤改 |
| R3-A1 | advisory→修 | overwrite guard 擋掉唯讀 dry-run，破壞「先 dry-run 報價」流程 | T2a：dry-run 只印 `WOULD abort` 警示＋估算、不中止；只有真跑 enforce |
| R3-A2 | advisory→修 | NB1 只有純函式測試，未證 main ordering | T2a：加 main-level 整合回歸（voice-diff subset → `build_backend` 未呼叫、sentinel WAV 不變） |

> `text_sha256` 移除 `read_bytes` fallback、以及 v3 各 guard／timeline field 皆經 Codex 第三輪確認**無 Karpathy 過度工程**（25 個 storyboard/spoken YAML 全 UTF-8 可解、guard 分支表無誤放）。

**v4→v5（Codex 第四輪：最後收斂）**

| Codex | 嚴重度 | 問題 | v5 落點 |
|-------|--------|------|---------|
| R3-B1 餘 | blocking | v4 驗到 `scenes` list-of-dict，但 `scenes:[{"beats":null}]`／`[{"beats":[null]}]` 仍判 ok，`build_reuse_index` 的 `for beat in scene["beats"]: beat.get(...)` 崩潰 | T2a `read_manifest_status`：每場 `beats`（若有）須 list-of-dict，否則 corrupt（仍不深驗 beat 內容——那是自家輸出）；補兩個 nested 回歸案 |
| 新 adv | advisory | dry-run 在 return 前就建了用不到的 reuse index（浪費＋malformed crash surface） | T2a：`use_reuse` 加 `and not args.dry_run` |

> **第四輪其餘全 closed、0 新 blocking、0 Karpathy 問題**（Codex 原話：真跑 abort 前無 backend／寫檔、`scenes=[]` 的 `all()==True` 安全、compose 無漏改呼叫點）。

**v5→v6（Codex 第五輪：R3-B1 完整收尾）**

第五輪查出 v5 的 R3-B1 修法**仍不完整**：(a) `s.get("beats")` 把「缺 key」與「`beats:null`」都變 `None`，但 `scene.get("beats", [])` 對 present-but-null 回 `None` → `for beat in None` 仍崩潰；(b) 更下一層 `build_reuse_index` 的 `Path(audio_file)`、`build_scene_reuse_index`／`merged_manifest` 的 `scene_id` dict key、`scene_reuse_ok` 的 `float(audio_seconds)` 都會被目前判 `ok` 的 JSON 觸發。**v6 落點：** `read_manifest_status` 依 Codex option (a) 一次驗**全部 consumer 實際 deref 的欄位型別**（`scene_id:str`、`beats` 用 `"beats" in s` 測 present-but-null＋list-of-dict＋`audio_file:str`、scene_aligned 的 `audio_seconds` 數值），使「ok」成為完整的 crash-safety 承諾；已對真 §3.1 manifest（27 場）驗證仍判 `ok`（不誤傷合法檔）。

**第六輪（收斂確認）：R3-B1 = closed，0 blocking。** Codex 逐一讀 `build_reuse_index`／`build_scene_reuse_index`／`scene_reuse_ok`／`reusable_existing_beat`／`merged_manifest`／`overwrite_guard`／receipt 對 prior manifest 的**每一處 deref**，對照 v6 驗證表確認全數涵蓋、無下一層可型別崩潰的欄位；`"beats" in s`（present-but-null）正確；未深驗的 `model`/`voice`/`style`/`scene_text_hash`/`text_hash`/`narration_mode`/`fallback_history` 都只被比較／搬運／取 truthiness，不 deref。合法 manifest（silent 場無 beats、beats 場、scene_aligned 場、`scenes=[]` 首跑、repo 現有 5 份＋§3.1 的 27 場）全判 `ok`、不誤傷。

> **本清單已收斂（v6，0 blocking）可交付新 session。** 執行時各 Phase 仍依 §0 跑 `codex exec -s read-only` 對**實際落地的 code**（非本清單）回歸（standing consent）——那是必要的下一層防線，因為本輪六輪審的是「計畫」，真正的 bug 只有在 code 寫出來後才驗得到。

---

## 3. 全域護欄（每個 task 都適用）

- **零計費**：全清單只用 `--backend mock`、本地 render、ffmpeg。真 MiMo 調用一律不需要；若某驗收看似需要，停下回報。
- **不碰真音檔**：涉及 `tts.py` 的測試一律 (a) 用 `storyboards/_demo_*.yml`，或 (b) `--output-dir`＋`--manifest` 指到 scratch 目錄。T2a 落地前尤其小心（F7）。
- **Karpathy 準則**（根 `CLAUDE.md`）：最少 code、外科手術式修改、不順手重構、每步可驗證。
- **selftest 慣例**：`video/pipeline/_selftest_<name>.py`，docstring 註明 `Run: python video/pipeline/_selftest_<name>.py`、平鋪 `test_*` 函式＋`assert`、檔尾 runner 迴圈（照抄 `_selftest_tts_unit.py` 的形式）。
- **commit 慣例**：`feat(video)`／`fix(video)`／`docs(video)`＋subject 帶 `[T<n>]`；一個 task 至少一個 commit，測試與實作可同 commit。這是工程線，**不**適用講義 Mode B／NFA 的 commit-body 稽核格式。
- **Codex 覆核**：每 Phase 收尾 `codex exec -s read-only` 對抗 review（standing consent 逕行）；blocking 修完須回歸審核。

---

## 4. Phase 0 — 前置（~15 分鐘）

- [x] **P0-1 讀文件**：根 `CLAUDE.md`、本檔全文、`video/DESIGN.md`（§storyboard 契約）、`video/REVIEW_GATES.md`、`video/RUNBOOK-mimo-narration-route.md`。
- [x] **P0-2 開分支＋存 dirty 底**（B3）：先 `git status --short` 存底並記下**開工前已存在的未提交修改**（本 repo 開工時工作樹通常是 dirty）；`git checkout -b video/pipeline-hardening`。〔完成 2026-07-11：dirty 底存於 scratchpad `DIRTY-BASELINE-DO-NOT-TOUCH.txt`；分支自 `84c2799` 開；工作樹保留。〕**護欄：整份清單任何 task 都不得對這些既有未提交檔案跑 `git checkout --`／`git reset`／`git stash`；所有「改檔再還原」型驗收一律在 `TemporaryDirectory` 內做（見 T1-7／T5-4）。**
- [x] **P0-3 綠基線**〔完成 2026-07-11：**15 個 selftest 全綠、無環境性跳過（manim 0.20.1 可用）、無真紅**。⚠️ 呼叫慣例是混的、無單一 cwd 能跑全部：`_selftest_{graph_labels,lint_registers,theorem_regime,type_scale}` 需從 `video/` 用 `python -m pipeline.<name>` 跑（`_bootstrap` 型）；`_selftest_coverage` 會 shell out `video/pipeline/schema.py` 故須從 repo root 跑；其餘自帶 path。P0-3 下方 PowerShell 片段只用 full-path、對前 4 個誤判紅。已改用 scratchpad `run_selftests.sh`（先試 repo-root full-path、失敗退 `video/ -m`，兩敗才真紅）作 Phase 收尾統一 runner。〕：跑既有離線 selftest，記錄哪些綠、哪些因環境（需 manim/render env）暫跳過。本環境 shell 是 **PowerShell**，用下列版（Adv8：累積失敗、最後非零 exit，不吞紅）：

```powershell
$failed = @()
Get-ChildItem video/pipeline/_selftest_*.py | ForEach-Object {
    Write-Host "== $($_.Name)"
    python $_.FullName
    if ($LASTEXITCODE -ne 0) { $failed += $_.Name }
}
if ($failed) { Write-Host "RED: $($failed -join ', ')"; exit 1 } else { Write-Host "all green" }
```

  **需 manim 環境才跑得動的 selftest**（`_selftest_sizecheck.py`、`_selftest_template_registry.py`、任何 import `pipeline.templates`／`manim` 的）列一份明確 allowlist 記錄為「環境性跳過」；**不得把任何真正的紅測試也稱作「暫跳過」**。`python tools/doctor.py` 查環境。**非環境性的紅就先停**：回報使用者，不在紅基線上疊工作。

---

## 5. Phase 1 — §3.2 TTS 前必做（T1–T4，全是小改）

完成定義：四個 task 落地＋selftest 綠＋demo deck mock 全流程不炸（見 P1 收尾）。此後 §3.2 才允許進真 TTS。

### T1 — `_mimo.yml` freshness gate（治 F1/F2）

**Files:**
- Create: `video/pipeline/derived_check.py`
- Create: `video/pipeline/_selftest_derived_check.py`
- Modify: `video/pipeline/derive_spoken.py`（`main()` 生成段，約 :168-177）
- Modify: `video/pipeline/tts.py`（`main()` 內 `load_storyboard` 之後，約 :850）
- Modify: `video/make.py`（`main()` 內 `load_storyboard` 之後，約 :633）
- Regenerate: `video/storyboards/ch03_trig_derivatives_mimo.yml`

**目標行為：** derive 時把正典檔的 sha256 蓋進生成檔 `meta.derived_from`；`tts.py`／`make.py` 對 `*_mimo` deck 開跑前驗章，不符即 abort 並指示重 derive。無章的舊生成檔也視為 stale。

- [x] **T1-1 寫 selftest（先跑紅）** — `video/pipeline/_selftest_derived_check.py`：

```python
"""Offline self-test for pipeline/derived_check.py (no API, no manim).
Run: python video/pipeline/_selftest_derived_check.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.derived_check import stamp_for, text_sha256, check_derived_freshness  # noqa: E402


def _fixture(d: Path, canon_text="a: 1\n", spoken_text="s: 1\n"):
    """Lay out storyboards/ + content_scripts/ like the real repo and return the
    generated deck path with a fresh two-input stamp."""
    (d / "storyboards").mkdir()
    (d / "content_scripts").mkdir()
    canon = d / "storyboards" / "deck.yml"
    spoken = d / "content_scripts" / "deck.spoken.yml"
    canon.write_text(canon_text, encoding="utf-8")
    spoken.write_text(spoken_text, encoding="utf-8")
    derived = d / "storyboards" / "deck_mimo.yml"
    data = {"meta": {"id": "deck_mimo", "derived_from": stamp_for(derived, canon, spoken)}}
    return derived, canon, spoken, data


def test_non_generated_deck_is_ignored():
    assert check_derived_freshness(Path("x.yml"), {"meta": {"id": "ch99_demo"}}) is None


def test_malformed_data_is_left_for_schema():   # B2: no AttributeError
    assert check_derived_freshness(Path("d_mimo.yml"), ["not", "a", "mapping"]) is None
    assert check_derived_freshness(Path("d_mimo.yml"), None) is None
    assert check_derived_freshness(Path("d_mimo.yml"), {"meta": ["bad"]}) is None


def test_missing_stamp_is_flagged():
    msg = check_derived_freshness(Path("d_mimo.yml"), {"meta": {"id": "d_mimo"}})
    assert msg and "derived_from" in msg


def test_fresh_then_canonical_stale():
    with tempfile.TemporaryDirectory() as d:
        derived, canon, _spoken, data = _fixture(Path(d))
        assert check_derived_freshness(derived, data) is None
        canon.write_text("a: 2\n", encoding="utf-8")          # canonical moves on
        assert "STALE" in (check_derived_freshness(derived, data) or "")


def test_spoken_change_is_stale():   # B1: spoken.yml is a stamped input too
    with tempfile.TemporaryDirectory() as d:
        derived, _canon, spoken, data = _fixture(Path(d))
        spoken.write_text("s: 2\n", encoding="utf-8")         # spoken edited, no re-derive
        assert "STALE" in (check_derived_freshness(derived, data) or "")


def test_crlf_lf_hash_is_stable():   # B1: autocrlf must not false-flag
    with tempfile.TemporaryDirectory() as d:
        crlf = Path(d) / "x_crlf.yml"; crlf.write_bytes(b"a: 1\r\nb: 2\r\n")
        lf = Path(d) / "x_lf.yml";     lf.write_bytes(b"a: 1\nb: 2\n")
        assert text_sha256(crlf) == text_sha256(lf)


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] derived_check green")
```

  Run：`python video/pipeline/_selftest_derived_check.py` → 預期 **ImportError**（模組還不存在）。

- [x] **T1-2 實作** — `video/pipeline/derived_check.py`。**關鍵設計（Codex B1/B2）：** (a) `_mimo.yml` 由 canonical **加** `.spoken.yml` 生成，故 stamp **記錄兩個輸入**——任一改動、未重 derive 都算 stale；(b) hash **先正規化成 LF 文字**再算，避免 `core.autocrlf` 跨機誤判；(c) `data`／`meta` 非 dict 時回 `None`，把 malformed 診斷**讓給下游 `schema_storyboard()`**，不搶先噴 `AttributeError`。

```python
"""Freshness gate for GENERATED storyboards (the *_mimo.yml drift guard).

derive_spoken.py stamps BOTH generation inputs (the canonical storyboard AND the
<deck>.spoken.yml source) into the generated deck's meta.derived_from; make.py /
tts.py refuse to run a generated deck whose stamps no longer match the files on
disk. Kills the drift class found 2026-07-11: canonical gained Task 14 hooks
AFTER _mimo.yml generation, parity --check still passed, and the stale deck
rendered anyway.

Hashing is LF-normalized (this repo has core.autocrlf=true and no .gitattributes,
so the same file is CRLF in a Windows working tree but LF in the git blob -- a
raw byte hash would false-flag a freshly checked-out deck as stale on an LF
machine). check_derived_freshness stays layout-free: it resolves each stamped
path RELATIVE TO the generated deck's own directory, and never touches malformed
top-level/meta (schema.py owns those diagnostics)."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any


def text_sha256(path: Path) -> str:
    """sha256 of the file's content normalized to LF, so CRLF/LF working-tree
    differences never change the hash (this repo has core.autocrlf=true). Text
    only -- storyboards/spoken are always UTF-8; a decode error is a real problem
    we WANT to surface, not paper over with a byte hash."""
    normalized = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def stamp_for(derived_path: Path, *input_paths: Path) -> dict[str, Any]:
    """Build a meta.derived_from stamp: each input's path RELATIVE TO the derived
    file's directory (forward slashes) + its LF-normalized sha256. Relative-to-
    derived keeps the checker free of repo-root detection. Used by BOTH
    derive_spoken.py (to stamp) and the selftest (to build fixtures)."""
    base = derived_path.parent
    return {"inputs": [
        {"path": os.path.relpath(p, base).replace(os.sep, "/"), "sha256": text_sha256(p)}
        for p in input_paths
    ]}


def check_derived_freshness(storyboard_path: Path, data: Any) -> str | None:
    """Error message if `data` (a loaded storyboard) is a stale or unstamped
    generated deck; None when fresh, not a generated deck, or malformed (malformed
    top-level/meta is left for schema_storyboard() to report -- do NOT raise)."""
    if not isinstance(data, dict):
        return None
    meta = data.get("meta")
    if not isinstance(meta, dict):
        return None
    if not str(meta.get("id", "")).endswith("_mimo"):
        return None
    deck = storyboard_path.stem[:-5] if storyboard_path.stem.endswith("_mimo") else storyboard_path.stem
    hint = f"re-run: python video/pipeline/derive_spoken.py --deck {deck}"
    derived = meta.get("derived_from")
    inputs = derived.get("inputs") if isinstance(derived, dict) else None
    if not isinstance(inputs, list) or not inputs:
        return f"{storyboard_path.name}: no derived_from stamp -- {hint}"
    base = storyboard_path.parent
    for item in inputs:
        if not isinstance(item, dict) or "path" not in item or "sha256" not in item:
            return f"{storyboard_path.name}: malformed derived_from stamp -- {hint}"
        src = (base / str(item["path"])).resolve()
        if not src.exists():
            return f"{storyboard_path.name}: stamped source {item['path']} not found -- {hint}"
        if text_sha256(src) != str(item["sha256"]):
            return f"{storyboard_path.name}: STALE -- {src.name} changed since generation; {hint}"
    return None
```

- [x] **T1-3 跑綠**：`python video/pipeline/_selftest_derived_check.py` → 六個 `ok`（含 malformed／spoken-change／CRLF 三個回歸案）。
- [x] **T1-4 接 derive 端** — `derive_spoken.py` `main()` 生成段，用 `stamp_for` 蓋**兩個輸入**的章後 dump。**import 放在檔頭現有 `sys.path.insert(...)` 之後**（Nit1，否則 `ModuleNotFoundError`）：

```python
from pipeline.derived_check import stamp_for   # 檔頭 import 區、sys.path.insert 之後

    mimo = gen_mimo(load(canon_path), spoken, args.deck)
    mimo["meta"]["derived_from"] = stamp_for(mimo_yml, canon_path, spoken_path)
    mimo_yml.write_text(
        f"# GENERATED by pipeline/derive_spoken.py from {args.deck}.spoken.yml + the canonical\n"
        "# storyboard. DO NOT EDIT -- change the .spoken.yml source and regenerate.\n\n"
        + yaml.safe_dump(mimo, allow_unicode=True, sort_keys=False, width=4096),
        encoding="utf-8",
    )
```

  （`canon_path`、`spoken_path`、`mimo_yml` 都是 `main()` 現有變數；`stamp_for` 記的是相對 `mimo_yml.parent`（`storyboards/`）的路徑，spoken 會存成 `../content_scripts/<deck>.spoken.yml`。）
- [x] **T1-5 接消費端**：`tts.py` `main()` 的 `data = load_storyboard(...)` 之後、`make.py` `main()` 的 `data = load_storyboard(...)` 之後，各加（import 同樣放檔頭 `sys.path.insert` 之後）：

```python
from pipeline.derived_check import check_derived_freshness
stale = check_derived_freshness(args.storyboard.resolve(), data)
if stale:
    raise SystemExit(f"[freshness] {stale}")
```

  放在任何 dry-run／schema 檢查**之前**（stale deck 連 dry-run 都不該給數字）。**因 `check_derived_freshness` 對非 dict `data`／`meta` 回 `None`（B2），malformed storyboard 仍會落到 `schema_storyboard()` 拿到清楚診斷，不會先噴 `AttributeError`。**
- [x] **T1-6 重生 ch03 生成檔**（離線、免費）：`python video/pipeline/derive_spoken.py --deck ch03_trig_derivatives` → 必印 `parity OK`＋兩個 wrote。確認新 `_mimo.yml` 現在含兩個 `hook:` 行、`sparse_ok`。**NA1 守門：明確斷言 `meta.derived_from.inputs` 恰為兩筆**（`ch03_trig_derivatives.yml` 與 `../content_scripts/ch03_trig_derivatives.spoken.yml`）——防日後 `derive_spoken` 漏傳 spoken 退化成單一輸入 stamp：

```python
import yaml
d = yaml.safe_load(open("video/storyboards/ch03_trig_derivatives_mimo.yml", encoding="utf-8"))
paths = {i["path"] for i in d["meta"]["derived_from"]["inputs"]}
assert paths == {"ch03_trig_derivatives.yml", "../content_scripts/ch03_trig_derivatives.spoken.yml"}, paths
```

  此步是**正當重生**（修 F2 的既有 stale），非「改檔再還原」，可直接 commit。
- [x] **T1-7 端到端驗收（不碰 tracked 檔；B3）**：
  - 正向：`python video/pipeline/tts.py --storyboard video/storyboards/ch03_trig_derivatives_mimo.yml --backend mock --dry-run` → 通過 freshness、印 dry-run（此時 T2 未做仍是舊格式，正常）。
  - STALE 反向：**在 `TemporaryDirectory` 內**複製 `storyboards/`＋`content_scripts/` 的相關檔，改動副本的 canonical（或 spoken）一個字元，對副本的 `_mimo.yml` 跑 `check_derived_freshness` → 必回 `STALE`。**不要**動工作樹的 tracked 檔、**不要** `git checkout --`（P0-2 護欄）。此案已由 T1-1 的 `test_fresh_then_canonical_stale`／`test_spoken_change_is_stale` 覆蓋，端到端只需確認 consumer 接線有生效即可。
- [x] **T1-8 Commit**：`feat(video): [T1] _mimo.yml freshness gate — dual-input LF-normalized stamp + preflight check`（body 記 F2 漂移事證＋B1 的 CRLF 事證）。

### T2 — `tts.py` 計費面硬化（治 F3/F4/F5/F6）

**Files:**
- Modify: `video/pipeline/tts.py`（`parse_args` :261-286、`main` :848-919、backends :123-136 與 MimoTTSBackend、`merged_manifest` 新函式）
- Modify: `video/pipeline/_selftest_tts_unit.py`（加測試）
- Check: `video/README.md`／`RUNBOOK-mimo-narration-route.md` 內的 `tts.py` 指令範例（RUNBOOK 已明寫 `--backend mimo`，應不需改；grep 確認）

四個子項分開 commit：

- [x] **T2a `--backend` 必填＋preflight fail-closed 覆寫護欄**（B4；NB1：**在任何合成／寫檔之前**判定；NB2：語意損壞也算 corrupt）
  - `parse_args`：`--backend` 拿掉 `default="mimo"` 改 `required=True`；新增 `--force-backend-switch`、`--force-clobber`（皆 `action="store_true"`）。
  - 新增「狀態感知」讀取＋純函式 guard。**NB2：** `json.loads` 成功還不夠——root 非 dict（`{}`/`null`/list）或缺 `backend`／`scenes` 一律算 `corrupt`（否則 `{}`+既有 WAV 會 fail-open、list 會在 `.get()` 噴 `AttributeError`）。**NB1：** guard 收「本次**打算寫入**的完整 identity」`intended`，比對 existing 全欄，**在 `build_backend()`／任何 WAV 寫入之前**判定，mismatch 時 `backend.stats["calls"]` 必為 0、既有 WAV 不動：

```python
_IDENTITY_KEYS = ("deck_id", "backend", "model", "voice", "style",
                  "sample_rate", "channels", "sample_width", "output_dir")


def read_manifest_status(path: Path) -> tuple[dict | None, str]:
    """('ok'|'absent'|'corrupt'). 'ok' is a PROMISE that every prior-manifest consumer
    runs without crashing on a shape it assumed. Beyond the top level (dict + str
    'backend' + list-of-dict 'scenes') we validate exactly the per-scene fields those
    consumers dereference by TYPE (R3-B1, Codex option a -- bounded to real derefs,
    not speculative):
      - scene_id: str                    -> dict key in build_scene_reuse_index:355 / merged_manifest
      - beats (only if the KEY exists):  -> build_reuse_index:333 does `for beat in scene["beats"]`
          list of dicts, and each beat's audio_file (if present) a str  (Path(audio_file):337)
          (test `"beats" in s`, NOT .get() -- explicit null must fail, since
           scene.get("beats", []) returns None for a present-but-null key)
      - audio_seconds (scene_aligned only, if present): a real number   (scene_reuse_ok float():382)
    Anything else -- truncation, non-dict JSON, a wrong type above -- is 'corrupt'
    (fail CLOSED). Beat text/hash/timing are NOT validated (nothing keys on their
    type). Keep this in sync if a consumer starts dereferencing a new field."""
    if not path.exists():
        return None, "absent"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None, "corrupt"
    scenes = data.get("scenes") if isinstance(data, dict) else None
    if (not isinstance(data, dict) or not isinstance(data.get("backend"), str)
            or not isinstance(scenes, list) or not all(isinstance(e, dict) for e in scenes)):
        return None, "corrupt"
    for s in scenes:
        if not isinstance(s.get("scene_id"), str):
            return None, "corrupt"
        if "beats" in s:
            beats = s["beats"]
            if (not isinstance(beats, list) or not all(isinstance(b, dict) for b in beats)
                    or any(b.get("audio_file") is not None
                           and not isinstance(b.get("audio_file"), str) for b in beats)):
                return None, "corrupt"
        if s.get("narration_mode") == "scene_aligned":
            secs = s.get("audio_seconds")
            if secs is not None and (isinstance(secs, bool) or not isinstance(secs, (int, float))):
                return None, "corrupt"
    return data, "ok"


def _has_audio(output_dir: Path) -> bool:
    return any((output_dir / "scenes").glob("*.wav")) or any((output_dir / "beats").rglob("*.wav"))


def overwrite_guard(*, status: str, existing: dict | None, intended: dict, scene_sel: str,
                    output_dir: Path, force_backend_switch: bool, force_clobber: bool) -> str | None:
    """Abort message (else None), computed BEFORE any synthesis/write so a bad run
    never bills a call or clobbers a WAV first (NB1). `intended` = the identity this
    run would write. Recovering a corrupt/orphaned output needs --force-clobber AND
    --scene all (a forced subset would leave un-accounted WAVs; NB2)."""
    need_full = "recovery needs --force-clobber AND --scene all"
    if status == "corrupt":
        if not force_clobber:
            return ("manifest present but corrupt/semantically invalid; refusing to overwrite "
                    "(it may still shadow real WAVs). Re-synthesize the whole deck or --force-clobber.")
        return None if scene_sel == "all" else need_full
    if status == "absent" and _has_audio(output_dir):
        if not force_clobber:
            return ("no valid manifest but WAVs already exist under the output dir; refusing to "
                    "overwrite unmanaged audio. Pass --force-clobber (with --scene all).")
        return None if scene_sel == "all" else need_full
    if status == "ok":
        diff = [k for k in _IDENTITY_KEYS if (existing or {}).get(k) != intended.get(k)]
        if diff and scene_sel != "all":
            return (f"this run's identity differs from the existing manifest on {diff}; a --scene "
                    f"subset can't safely merge into it. Re-run --scene all to rebuild.")
        if "backend" in diff and not force_backend_switch:
            return (f"existing manifest backend={(existing or {}).get('backend')!r} != "
                    f"{intended.get('backend')!r}; pass --force-backend-switch (with --scene all).")
    return None
```

  - `main()`：用 `existing, status = read_manifest_status(manifest_path)` 取代舊 `prior_manifest = load_prior_manifest(...) if args.reuse_existing else None`。組 `intended` identity（manifest header 那幾欄，合成前已知）。**R3-A1：dry-run 是唯讀，不能被 write guard 擋掉**——dry-run 只把「真跑會 abort」當**警示**印出（要能拿到報價），只有真跑才 enforce。**R3-B2：任何 identity diff 的 full rebuild 一律丟棄 reuse**（防「header 宣稱新 identity、WAV 卻沿用舊格式」；realistic 的 backend/model/voice/style 差異 `scene_reuse_ok` 本就會擋，此為 defense-in-depth 補 `sample_*`/`output_dir`）：

```python
intended = {"deck_id": meta["id"], "backend": args.backend, "model": args.model,
            "voice": voice, "style": args.style, "sample_rate": 24_000, "channels": 1,
            "sample_width": 2, "output_dir": str(output_dir)}
abort = overwrite_guard(status=status, existing=existing, intended=intended,
                        scene_sel=args.scene, output_dir=output_dir,
                        force_backend_switch=args.force_backend_switch,
                        force_clobber=args.force_clobber)
identity_diff = status == "ok" and any((existing or {}).get(k) != intended.get(k)
                                       for k in _IDENTITY_KEYS)
# reuse index only when asked AND identity unchanged (R3-B2) AND not a dry-run
# (dry-run writes nothing and never reads these -- don't build unused indexes).
use_reuse = args.reuse_existing and not identity_diff and not args.dry_run
reuse_index = build_reuse_index(existing) if use_reuse else {}
scene_reuse_index = build_scene_reuse_index(existing) if use_reuse else {}

if args.dry_run:
    if abort:
        print(f"[dry-run] NOTE: a real run WOULD abort -> {abort}")
    # ... fall through to the T2b dry-run estimate + return 0 (no writes) ...
elif abort:
    raise SystemExit(f"[tts] {abort}")
```

  （T2b 的 `if args.dry_run:` 估算區塊接在此後；順序＝guard 算完 → dry-run 印警示＋估算後 return → 真跑才 `build_backend()`／合成。）
  - selftest（`_selftest_tts_unit.py`）：純函式 `overwrite_guard` 各狀態——corrupt(含 `{}`/`null`/`[]`/`scenes:null`/`scenes:[null]` 經 `read_manifest_status` 都判 corrupt)→abort；corrupt+`--force-clobber`+`--scene b`→abort、+`--scene all`→放行；absent+有 WAV→abort；ok+**voice 不同**+subset→abort；ok+backend 不同+`--scene all`+force-switch→放行、無 force→abort；乾淨 ok→None。另測 `read_manifest_status` 的完整 shape 契約（R3-B1）——下列全判 **corrupt**：`{}`／`null`／`[]`／`{"backend":1,"scenes":[]}`／`{"backend":"m"}`（無 scenes）／`{...,"scenes":null}`／`{...,"scenes":[null]}`／`{...,"scenes":[{}]}`（無 scene_id）／`scenes:[{"scene_id":["x"]}]`（scene_id 非 str）／`scenes:[{"scene_id":"a","beats":null}]`／`scenes:[{"scene_id":"a","beats":[null]}]`／`scenes:[{"scene_id":"a","beats":[{"audio_file":123}]}]`（audio_file 非 str）／`scenes:[{"scene_id":"a","narration_mode":"scene_aligned","audio_seconds":"x"}]`（非數值）。下列判 **ok**：`{"backend":"m","scenes":[]}`（首跑）／`scenes:[{"scene_id":"a","beats":[{"audio_file":"x.wav","text_hash":"h"}]}]`／`scenes:[{"scene_id":"a","narration_mode":"scene_aligned","audio_seconds":4.2}]`／`scenes:[{"scene_id":"a","narration_mode":"silent","duration":6.0}]`（silent 無 beats）。
  - **R3-A2 main-level 整合回歸**：造一個 prior mock manifest（backend=mock, voice=Dean）＋一個 sentinel WAV（記 bytes/mtime），跑「同 backend、`--voice Mia`、`--scene <單場>`」（非 dry-run）→ 斷言 `SystemExit`、**`build_backend` 未被呼叫**（monkeypatch 成 raise 或用 spy）、sentinel WAV bytes/mtime 不變。這證明 guard 在**任何寫入/合成之前**擋下（純函式測試證不了 main ordering）。
  - 驗收：scratch 先 `--backend mock` 產 manifest；`--backend mimo --dry-run` 同路徑 → **印出估算＋`WOULD abort` 警示、return 0**（R3-A1：dry-run 不中止、可拿報價）；`--backend mimo`（真跑）同路徑 → abort、`build_backend` 前即止（stats.calls==0）；manifest 截半／`{}`／`scenes:null` → 真跑必 abort（corrupt）。
  - Commit：`feat(video): [T2a] tts.py --backend required + preflight fail-closed guard (semantic-corrupt aware, full-identity, dry-run-safe, reuse-invalidating)`。

- [x] **T2b `--dry-run` 真實化（planned／worst call 數）** — 取代 `main()` :873-878 的舊輸出。**Adv1 校正：** (a) 欄名寫明 **ignoring `--reuse-existing`**（dry-run 不讀 reuse index，reuse 可讓實際 call 降到 0，不可謊稱為「預期」）；(b) **只有非空 beat 才呼叫 backend**（空 beat 用 `empty_beat_seconds` 寫靜音、不計 call；Codex 指 `tts.py:455-458`，執行時對 `synthesize_beat` 確認）；(c) **`--fallback-budget >= 0` 的驗證放 `main()` 開頭無條件執行**（NA2：不能只在 dry-run 內驗，正式合成也要擋負值）——即 `if args.fallback_budget < 0: raise SystemExit("[tts] --fallback-budget must be >= 0")` 放在 dry-run／guard 之前。

```python
if args.dry_run:
    rows, planned, worst, est_secs = [], 0, 0, 0.0
    for scene in scenes:
        if scene.get("kind", "content") != "content":
            continue
        unit = resolve_unit(args.unit, scene)
        beats = scene_beats(scene)
        nonempty = [b for b in beats if (b.get("text") or "").strip()]
        est_secs += sum(estimate_seconds(b["text"]) if (b.get("text") or "").strip()
                        else args.empty_beat_seconds for b in beats)
        if unit == "scene":
            p, wc = 1, 1 + args.fallback_budget + len(nonempty)   # synth + billed rungs 2-3 + beats terminal
        else:
            p = wc = len(nonempty)                                # empty beats don't hit the backend
        planned += p; worst += wc
        rows.append((scene["id"], unit, len(beats), len(nonempty), p, wc))
    print(f"[dry-run] backend={args.backend} model={args.model} voice={voice} unit={args.unit} "
          f"(planned counts IGNORE --reuse-existing)")
    print(f"[dry-run] {'scene':<30}{'unit':<7}{'beats':>6}{'calls':>6}{'plan':>5}{'worst':>7}")
    for sid, unit, nb, nc, p, wc in rows:
        print(f"[dry-run] {sid:<30}{unit:<7}{nb:>6}{nc:>6}{p:>5}{wc:>7}")
    print(f"[dry-run] TOTAL content-scenes={len(rows)}  planned first-round calls={planned}  "
          f"worst-case incl. fallback ladder={worst}  est narration ~{est_secs/60:.1f} min")
    return 0
```

  - 先確認 `scene_beats()` 條目的 text 鍵名（`tts.py:420-432`）與 `synthesize_beat` 對空 beat 是否真的 short-circuit，照實際調整。
  - 驗收：對 ch03 deck 跑 `--backend mock --dry-run`，人工核對：21 content scene、scene-unit 場 plan=1、beat-unit 場 plan=非空 beat 數、`beats` 欄≥`calls` 欄（有空 beat 時嚴格大於）、worst 與 `--fallback-budget` 連動。此輸出即**報價徵同意**依據（CLAUDE.md 計費閘）；報價時另註明 reuse 可再往下降。
  - Commit：`feat(video): [T2b] tts.py dry-run reports planned/worst call structure (ignoring reuse, non-empty beats only)`。

- [x] **T2c `--scene` 原子合併回完整 manifest** — 新增純函式＋接線。**分工（NB1 後）：** identity 一致性由 **T2a preflight guard** 在合成前把關（subset+任何 identity diff 直接 abort）；`merged_manifest` 只做「把 fresh 場疊回 prior」，並保留同一 identity 檢查作為**寫檔前的 backstop**（理論上永不觸發，但 raise 比默默合出說謊 manifest 安全）。**重用 T2a 定義的 `_IDENTITY_KEYS`，不要重複定義。**

```python
def merged_manifest(prior: dict[str, Any] | None, fresh: dict[str, Any],
                    storyboard_scene_ids: list[str]) -> dict[str, Any]:
    """--scene subset merges INTO the prior manifest: fresh entries win per
    scene_id, untouched prior entries survive, order follows the storyboard.
    Backstop only (T2a preflight already blocked identity mismatch before any
    synthesis): if identity somehow still differs, REFUSE rather than merge.
    No prior manifest -> just the fresh subset."""
    if not prior:
        return fresh
    mismatch = [k for k in _IDENTITY_KEYS if prior.get(k) != fresh.get(k)]
    if mismatch:
        raise SystemExit(
            f"[tts] refusing to merge a --scene subset into a manifest that differs on "
            f"{mismatch}; re-run the whole deck (--scene all) to rebuild it consistently.")
    by_id = {e["scene_id"]: e for e in prior.get("scenes", []) if e.get("scene_id")}
    by_id.update({e["scene_id"]: e for e in fresh.get("scenes", []) if e.get("scene_id")})
    out = {**prior, **{k: v for k, v in fresh.items() if k != "scenes"}}
    out["scenes"] = [by_id[sid] for sid in storyboard_scene_ids if sid in by_id]
    return out
```

  `main()` 寫檔前：`if args.scene != "all": manifest = merged_manifest(existing, manifest, [s["id"] for s in all_scenes])`。
  - selftest（`_selftest_tts_unit.py` 加）：

```python
def test_scene_subset_merges_into_prior_manifest():
    base = {"deck_id": "d", "backend": "mimo", "model": "m", "voice": "Dean", "style": "",
            "sample_rate": 24000, "channels": 1, "sample_width": 2, "output_dir": "/o"}
    prior = {**base, "scenes": [{"scene_id": "a", "x": 1}, {"scene_id": "b", "x": 2}]}
    fresh = {**base, "scenes": [{"scene_id": "b", "x": 99}]}
    out = tts.merged_manifest(prior, fresh, ["a", "b", "c"])
    assert [e["scene_id"] for e in out["scenes"]] == ["a", "b"]
    assert out["scenes"][0]["x"] == 1 and out["scenes"][1]["x"] == 99
    assert tts.merged_manifest(None, fresh, ["b"]) is fresh                    # 無 prior → fresh

def test_merge_refuses_identity_mismatch():
    base = {"deck_id": "d", "backend": "mimo", "model": "m", "voice": "Dean", "style": "",
            "sample_rate": 24000, "channels": 1, "sample_width": 2, "output_dir": "/o"}
    prior = {**base, "scenes": [{"scene_id": "a", "x": 1}]}
    fresh = {**base, "voice": "Mia", "scenes": [{"scene_id": "b", "x": 2}]}   # voice differs
    try:
        tts.merged_manifest(prior, fresh, ["a", "b"]); assert False, "should have raised"
    except SystemExit:
        pass
```

  - 驗收：scratch 目錄 demo deck 先 `--backend mock` 全跑 → 再 `--scene <單場 id>` 重跑 → manifest 仍含全部場、僅該場更新；另手動改 prior 的 `voice` → subset 重跑必 abort。
  - Commit：`fix(video): [T2c] tts.py --scene merges into prior manifest (identity-checked, refuses mixed)`。

- [x] **T2d manifest 計費收據** —
  - `MockTTSBackend.__init__`／`MimoTTSBackend.__init__` 各加 `self.stats = {"calls": 0, "retries": 0}`；兩者 `synthesize()` 開頭 `self.stats["calls"] += 1`；讀 `MimoTTSBackend` 的 retry 迴圈（`tts.py:136` 起），在**兩個**重試分支各 `self.stats["retries"] += 1`——Adv1：MiMo 有 HTTP 429/5xx **與** `URLError`/`TimeoutError` 兩條 retry 路徑，只埋一處會漏算。
  - `main()` `write_manifest` 前組收據並印出：

```python
manifest["receipt"] = {
    "backend_calls": getattr(backend, "stats", {}).get("calls", 0),
    "backend_retries": getattr(backend, "stats", {}).get("retries", 0),
    "modes": {m: sum(1 for e in manifest["scenes"] if e.get("narration_mode") == m)
              for m in ("scene_aligned", "beats", "silent")},
    "fallback_scenes": [e["scene_id"] for e in manifest["scenes"] if e.get("fallback_history")],
}
print(f"[tts] receipt: {json.dumps(manifest['receipt'], ensure_ascii=False)}", flush=True)
```

  - 注意 T2c 合併語意：receipt 反映**本次執行**，合併寫檔時保留 fresh 的 receipt（`merged_manifest` 的 top-level fresh 覆蓋已處理）。
  - 驗收：demo deck mock 全跑 → receipt 的 `backend_calls` 等於 mock 實際合成次數（beat 模式＝**非空 beat 數**，非 beat 總數；NA2——空 beat 不呼叫 backend，與 T2b 計法一致）；`--scene` 局部重跑 → receipt 只計本次。
  - Commit：`feat(video): [T2d] tts.py billing receipt in manifest (calls/retries/modes/fallbacks)`。

### T3 — `--unit auto` allowlist 單一源（治 F10/F11）

**Files:**
- Create: `video/pipeline/template_names.py`
- Create: `video/pipeline/_selftest_template_registry.py`（manim env）
- Modify: `video/pipeline/tts.py:48-55`
- Modify: `video/pipeline/_selftest_tts_unit.py:15-29`

- [x] **T3-1 常數模組** — `video/pipeline/template_names.py`：

```python
"""Manim-free single source for the content-template name set.

tts.py must stay importable in the TTS env (no manim), so it cannot read
pipeline/templates/__init__.py's REGISTRY (blocks.py imports manim at module
top). Both sides use THIS tuple; _selftest_template_registry.py (manim env)
asserts the REGISTRY still matches it, so the two can't drift apart again."""
CONTENT_TEMPLATES: tuple[str, ...] = (
    "callout", "definition_math", "derivation", "graph", "procedure_steps",
    "recap_cards", "sign_chart", "theorem_proof", "value_table",
)
```

- [x] **T3-2 tts.py 改吃常數** — 取代 :48-55 的註解＋frozenset：

```python
from pipeline.template_names import CONTENT_TEMPLATES

# --unit auto routes every KNOWN content template to scene-level TTS. History:
# batch-1 four (2026-07-05), batch-2 six (2026-07-06); 2026-07-11 the hand-kept
# list was found missing procedure_steps/value_table/sign_chart vs the registry,
# so it now derives from pipeline/template_names.py (parity selftest guards it).
# Unknown templates still fall back to beat. An over-broad allowlist is bounded but
# NOT free: a scene whose FA fails demotes down the ladder to the beats terminal,
# which under MiMo bills once PER non-empty beat (not "one attempt"); dry-run's
# worst-case column already accounts for that fan-out.
SCENE_UNIT_TEMPLATES = frozenset(CONTENT_TEMPLATES)
```

- [x] **T3-3 parity selftest** — `video/pipeline/_selftest_template_registry.py`：

```python
"""Parity guard: templates REGISTRY (manim env) == pipeline/template_names.py.
Run (render/manim env): python video/pipeline/_selftest_template_registry.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.template_names import CONTENT_TEMPLATES  # noqa: E402


def test_registry_matches_template_names():
    from pipeline.templates import REGISTRY
    content = set(REGISTRY) - {"intro", "outro", "divider"}
    assert content == set(CONTENT_TEMPLATES), (
        f"registry={sorted(content)} != template_names={sorted(CONTENT_TEMPLATES)}")


if __name__ == "__main__":
    test_registry_matches_template_names()
    print("[selftest] template registry parity green")
```

- [x] **T3-4 更新既有測試** — `_selftest_tts_unit.py`：把 `test_unit_auto_allowlist_is_batch2` **改名** `test_unit_auto_matches_content_templates`（Nit2：batch-2 特例已過時），斷言 `SCENE_UNIT_TEMPLATES == set(CONTENT_TEMPLATES)`（相等，非子集）；`test_resolve_unit_for_scene` 加三行斷言 `procedure_steps`／`value_table`／`sign_chart` 在 `auto` 下回 `"scene"`。
- [x] **T3-5 驗收**：`python video/pipeline/_selftest_tts_unit.py`（TTS env）＋`python video/pipeline/_selftest_template_registry.py`（manim env）都綠。
- [x] **T3-6 Commit**：`fix(video): [T3] --unit auto allowlist derives from single manim-free source (adds procedure_steps/value_table/sign_chart)`。

### T4 — ASR QA verdict 落 manifest（治 F8）

**Files:**
- Modify: `video/pipeline/tts.py`（`_asr_probe_tokens` :594-608、`_finalize_aligned` :611-646）
- Modify: `video/pipeline/scene_align.py`（`build_scene_aligned_entry` :431-456）
- Modify: `video/pipeline/_selftest_scene_align.py`（或 `_selftest_tts_unit.py`）加 entry 形狀測試

- [x] **T4-1 `_asr_probe_tokens` 回傳原因** — 簽名改 `-> tuple[list | None, str]`：ImportError → `(None, "skipped: whisper_timestamped not installed")`；執行例外 → `(None, f"error: {exc}")`；成功 → `(tokens, "ran")`。
- [x] **T4-2 `_finalize_aligned` 記錄三態**（ran／skipped／error）。**Adv2 政策明定：** 只有**刻意** `--skip-qa` 靜默（intentional opt-out）；其餘任何「該跑而沒跑」（缺套件、例外、意外無 qa_wav）一律 `WARN … NOT a pass`：

```python
if getattr(args, "skip_qa", False):
    gates = {**gates, "qa": {"status": "skipped", "reason": "--skip-qa (intentional)"}}
    # intentional opt-out -> silent by policy
else:
    asr, note = (None, "skipped: no qa wav on this path") if qa_wav is None \
        else _asr_probe_tokens(qa_wav, args)
    if asr is None:
        status = "error" if note.startswith("error") else "skipped"
        gates = {**gates, "qa": {"status": status, "reason": note}}
        print(f"[tts] WARN {plan['scene_id']}: ASR QA probe did not run ({note}) -- "
              f"this is NOT a pass", flush=True)
    else:
        fa_probs = [w.get("probability") for w in words]
        qa = SA.qa_diff(SA.tokenize(plan["transcript"]), asr, fa_probs,
                        weak_spans=SA.boundary_weak_spans(beats))
        gates = {**gates, "qa": {"status": "ran", **qa}}
        if qa["verdict"] == "fail":
            gates["status"] = "fail"
            gates["failures"] = gates["failures"] + ["QA probe: suspect TTS misspeak"]
```

- [x] **T4-3 `build_scene_aligned_entry` 帶出 qa** — `validation` dict 加一鍵：`"qa": gates.get("qa")`。
- [x] **T4-4 selftest（兩層；Adv2/B5：不能只驗序列化）**：
  - **(a) 序列化**：直接呼叫 `build_scene_aligned_entry`（gates 帶 `{"qa": {"status": "skipped", "reason": "x"}}`），斷言 `entry["validation"]["qa"]["status"] == "skipped"`。
  - **(b) 控制流（monkeypatch，無模型無 API）**：monkeypatch `tts._asr_probe_tokens` 依次回 `(["w"], "ran")`／`(None, "skipped: not installed")`／`(None, "error: boom")`，並 monkeypatch `SA.map_to_beats`／`SA.run_gates`／`SA.qa_diff` 為 fake（`run_gates` 回 `{"status":"pass","warnings":[],"metrics":{},"failures":[]}`；`qa_diff` 回 `{"verdict":"fail",...}`），`words_file`／`aligned_file`／`audio_file` 指到 `TemporaryDirectory`。斷言：ran＋fail verdict → `entry["validation"]["status"]=="fail"` 且 `qa.status=="ran"`；error → `qa.status=="error"`＋印出 WARN；skipped(not installed) → `qa.status=="skipped"`＋WARN。**另兩例明確驗政策（Adv2）：** `args.skip_qa=True` → `qa.status=="skipped"` 且**不印 WARN**（intentional）；`qa_wav=None` → `qa.status=="skipped"`＋**印 WARN**（該有卻沒有）。這是真正驗到 `_finalize_aligned` 控制流與「靜默略過會 WARN」的測試（靜音跑真模型驗不到，見 B5）。
- [x] **T4-5 驗收**：selftest 綠；另 grep 確認 `_finalize_aligned` 的兩個呼叫點（single-shot `:666-670`、chunk `:779-783`）都經過新邏輯（同一函式，天然覆蓋）。
- [x] **T4-6 Commit**：`fix(video): [T4] persist ASR QA verdict into manifest validation; loud-warn on silent skip`。

### Phase 1 收尾

- [x] **P1-END-1 demo deck mock 整合驗收**（scratch 目錄；**B5 校正**）：`derive_spoken --check`（用 ch03）→ `tts.py --backend mock --dry-run`（看新報表）→ **`tts.py --backend mock --unit beat`**（demo deck、scratch）→ `--scene` 局部重跑驗合併 → 檢視 manifest 的 `receipt`。**務必 `--unit beat`**：`--unit auto`（T3 後）會走 scene mode → 對 mock 靜音仍載入 stable-ts（非全離線、且靜音必 fallback 到 beats、beats entry 沒有 `validation.qa`），無法 deterministic 驗收。`validation.qa` 的三態行為改由 **T4-4(b) 的 monkeypatch selftest** 驗，不靠這條整合流程。
- [x] **P1-END-2 全 selftest 重跑**〔17/17 綠〕（含 Phase 0 基線清單＋本 Phase 新增）。
- [x] **P1-END-3 Codex 對抗 review**（standing consent）：`codex exec -s read-only` 餵 Phase 1 diff，blocking 修完回歸。〔2026-07-11：因 usage cap 前兩次中斷（僅浮現 null-char edge＝評估非 blocking，見 scratch `codex-phase1-assessment.md`）；quota 回復後改跑**合併 T1–T10 完整複核**（gpt-5.6-terra/max，涵蓋 Phase 1/2/3 的 Codex 閘）——找 **3 條 blocking**（make.py mock fail-open 蓋真 Dean WAV／derived_check 沒強制雙輸入契約／loudness_ab CLI ModuleNotFoundError＋假綠），已修（commit `f8c91ca`）＋**回歸再審確認「3 條已關閉、0 新 blocking」**。null-char edge 經 T1–T10 複核仍判非 blocking。〕
- [x] **P1-END-4 進度回寫**：勾本檔核取框；`REBUILD_STATUS.md` 加一行「pipeline-hardening Phase 1 完成（T1–T4）」。

---

## 6. Phase 2 — 隨 §3.2 storyboard 落地一起（T5）

### T5 — `{show}` target-vs-payload cross-check（治 F9）

**Files:**
- Modify: `video/pipeline/sizecheck.py`（主場景迴圈 :557-570 內、`blocks = build_blocks(...)` 成功之後）
- Modify: `video/pipeline/_selftest_sizecheck.py`（加 typo 案例）

- [x] **T5-1 實作（只做 missing-target error；Adv3）** — 在 blocks 建成後加（`reveal_targets` 從 `pipeline.schema` import，manim-free）。**只驗「`{show}` 指向不存在的 block」這一件事**；**不加**「未被 reveal 的 dynamic block」warning——那是未被要求的噪音功能，且會誤報刻意 end-backfill／custom hook 間接動畫（若日後真要，另立 task）：

```python
ids = {b.id for b in blocks}
for t in reveal_targets(scene.get("say", "")):
    if t and t not in ids:   # 空 {show} 是純分拍，略過
        issues.append(("error", f"{scene.get('id')}: {{show {t}}} has no matching block "
                                f"(built ids: {sorted(ids)})"))
```

- [x] **T5-2 校準（error 必為 0）**〔14 demo＋ch03 canonical 全 0 cross-check error〕：對全部 `storyboards/_demo_*.yml`＋`ch03_trig_derivatives.yml` 跑 sizecheck。**`make.py` 沒有 sizecheck-only 階段**（Adv3），所以**直接跑** `python video/pipeline/sizecheck.py <deck>`（先讀其檔頭 docstring 確認 CLI 用法）或在 manim env 用 `python -c` 呼叫其 top-level 函式。現有正當 deck 的 cross-check error 必須為 0（否則表示某 `{show}` 本來就 typo，屬真 bug、回報）。
- [x] **T5-3 selftest**：`_selftest_sizecheck.py` 加一案：内嵌一個 `{show math.9}` 指向不存在 index 的最小 spec，斷言回報含 `error`；另加一案：合法 deck 的 cross-check error 數為 0。
- [x] **T5-4 驗收（temp copy，不改 tracked demo；B3）**：把一個 `_demo_*.yml` 複製到 `TemporaryDirectory`，在**副本**裡把一個 `{show}` 改成 typo，對副本跑 sizecheck → 回報 `error`。**不要**原地改 tracked demo 檔。主要證明仍是 T5-3 selftest。
- [x] **T5-5 Commit**：`feat(video): [T5] sizecheck cross-checks {show} targets against built block ids`。

---

## 7. Phase 3 — 批量產前（T6–T11）

順序建議（**Adv7 校正**）：T7 → T6（T6 消費 T7 的 timeline）→ T8 → **T9、T10 各自產出 A/B 交付物後標 `awaiting adjudication`、不互相 STOP** → 一次把兩份 A/B 交使用者裁決 → 裁決回來後落 production defaults → T11（收尾統一改文檔）。即：「STOP」指的是**不落 production 預設**，不是停下整個 Phase；A/B 交付物的產出本身不阻塞彼此。

### T6 — 聽感驗收 listening pack（治 REVIEW_GATES 已知缺口「無自動 listen-back」）

**Files:**
- Create: `video/pipeline/listening_pack.py`
- Create: `video/pipeline/_selftest_listening_pack.py`

**目標行為：** 讀某節的 `manifest.json`，**不重新合成、不觸發任何重試**（F16 的既有裁決必須尊重——pack 只報告），產出 standalone HTML（繁中框架）落在 manifest 同目錄：每場一列，含 `<audio controls>` 指向**現有** WAV（相對路徑）、spoken text、`narration_mode`、WPM、`validation.status`＋warnings＋`qa`、`fallback_history`、LUFS／true peak（ffmpeg `ebur128` 量測）。**路徑：** CLI 收**顯式 `--manifest`（必填、無預設 fallback，NA3——避免「必填 vs 兩者省略 fallback」的矛盾）**；T6 只吃 manifest，**不需要 timeline**（NA3：`--timeline` 無實際用途，Karpathy 砍掉不加）。**排序＝風險優先（NA3 校正，讓 terminal-beat 真的排前、與 T6-4 一致）：**
  1. `validation.status == "fail"`
  2. **terminal-beat fallback**（`narration_mode == "beats"` 且 `fallback_history` 非空——FA 放棄、最該聽）
  3. 有 `warnings`
  4. `qa` 非 ran（`skipped`／`error`／`legacy-missing`）
  5. WPM > 175（常數 `WPM_MUST_LISTEN = 175`，超標標「必聽」章）
  6. clean

- [x] **T6-1 資料組裝函式先行**（純函式，好測）：`rows_from_manifest(manifest: dict) -> list[dict]`，WPM＝`len(script.split()) / audio_seconds * 60`（`audio_seconds<=0` 防呆）；風險分數為整數鍵。**qa 三態要分辨（Adv4）**：`validation.qa` 缺鍵（legacy manifest，如 §3.1）標 `qa=legacy-missing`、`status=="skipped"/"error"` 各自成一類，**不要**把「legacy 沒有 qa」與「本次 error」混為同一風險級。selftest 用假 manifest dict 驗排序與 WPM。
- [x] **T6-2 LUFS 量測**：`measure_loudness(wav: Path) -> dict`——`ffmpeg -i x.wav -af ebur128=peak=true -f null -` 解析 stderr summary 的 `I:`／`Peak:`；ffmpeg 缺席或解析失敗回 `{"error": ...}` 不炸。
- [x] **T6-3 HTML 產出**：單檔 `REVIEW-<deck>-listening.html`，表格＋`<audio controls src="scenes/07_xxx.wav">`（相對於 HTML 所在目錄）；框架文字繁中、引文與識別碼原樣（比照 `pipeline/assets/audio/house/REVIEW-house-audio-candidates.html` 的形式）。**所有插入 HTML 的 spoken text／reason／檔名一律 `html.escape()`**（Adv4：旁白含 `<`、`&`、引號會破版或 XSS-lite）。頁首註明：「本 pack 為驗收輔助；正式交付前仍應完整聽一次全片（REVIEW_GATES 慣例）」。
- [x] **T6-4 驗收（Adv4 精確版）**〔18/3/6 模式、3 terminal-beat rank2、qa 全 legacy-missing、21 audio＋ebur128 LUFS ~-19〕：對 `output/ch03/s3.1/audio_mimo/manifest.json`（現成資料，唯讀）產一份 → 雙擊可播；模式計數＝**18 scene_aligned／3 beats／6 silent**；`fallback_history` 非空的是 **5 場**（3 terminal beats：`continuity_argument`／`derivative_of_cosine`／`shm_stacked_graphs`；＋2 場 arbiter 救回仍 scene_aligned：`fundamental_limit`／`recap`）。依上面排序，**3 個 terminal-beat 場排在最前**（rank 2，僅次於 fail）；`fundamental_limit`／`recap` 及其他有 warnings 的 aligned 場落 rank 3（NA3：不強求 arbiter 兩場緊接 beats——現行 manifest 多個 aligned 場也有 warnings）。此 legacy manifest **全無 `validation.qa`**，一律標 `legacy-missing`（rank 4）而非「高風險 error」。
- [x] **T6-5 Commit**：`feat(video): [T6] offline listening pack (per-take audio QC HTML from manifest)`。

### T7 — timeline.json＋sidecar 字幕＋chapters（治 F14；**B6 全面重寫**）

**Files:**
- Modify: `video/make.py`（`compose()` :566 起、arg parser、`_probe_duration`）
- Create: `video/pipeline/captions.py`＋`video/pipeline/_selftest_captions.py`

B6/NB3/NB4 硬點貫穿本 task：**(i)** 字幕時戳用 timeline 實記的 `lead_seconds`（不硬寫 `SCENE_LEAD_SECONDS`）；**(ii)** sidecar 檔名綁 **output stem**（subset／A/B 多輸出不互相覆寫）；**(iii)** chapter title **由 compose 端算好寫進 timeline**（NB3：captions 只吃 manifest＋timeline，兩者都沒有 title；title 在 storyboard，只有 compose 手上有），fallback 順序 `scene.title → scene.tagline → meta.title → scene.id`（NB3：intro 只有 `tagline`，若 `meta.title` 排前會永遠用不到 tagline）；**(iv)** 跳過空文字 cue；**(v)** NB4：`--lead` 目前**耦合**於 render 端固定的 `SCENE_LEAD_SECONDS`（`render()` 不接 lead、`LessonScene` 永遠 wait 1s），故非預設 lead 會造成 A/V 錯位——本 task **不改 render**，改為 compose 端遇 `lead != SCENE_LEAD_SECONDS` 印 WARN、且驗收不跑非預設 lead 的成片。

- [x] **T7-1 先讀再寫**：讀 `pipeline/scene_align.py` 的 `map_to_beats` 輸出與 manifest 兩種模式的 beat 條目，確認**每拍時間鍵名**（實測兩模式都用 `start_seconds`/`end_seconds`，見 F14）。在 `captions.py` 寫 normalize 函式 `beat_spans(entry) -> list[tuple[text, start, end]]` 統一兩模式，並在此**跳過 `text.strip()==""` 的 beat**（B6：demo 如 `_demo_multipage.yml` 17 beats 僅 3 個非空，不濾會產空 cue）。
- [x] **T7-2 timeline**：`compose()` 在 concat 前累積每 segment 的 `_probe_duration`，寫 timeline 到 `<output.stem>.timeline.json`（**綁 output stem**）：

```json
{"deck_id": "...", "output": "<成片檔名>", "quality": "...", "lead_seconds": <compose 實際用的 args.lead>,
 "scenes": [{"scene_id": "...", "kind": "...", "start": 0.0, "end": 6.0, "narration_mode": "...",
             "chapter_title": "<divider/intro 場才有：compose 算好的章名，見下>"}],
 "provenance": {"storyboard_sha256": "<用 pipeline.derived_check.text_sha256>", "manifest_path": "...",
                "git_commit": "<git rev-parse --short HEAD；失敗記 'unknown'>"}}
```

  - **`compose()` signature＋main wiring（R3-B3：不能只給 JSON 範例，要接得到資料）：** 現行 `compose(scenes, manifest, rendered, out_dir, *, lead, abr, output, fade)` **沒有** `meta`／`quality`／storyboard 路徑，產不出上面的 timeline，也做不了 `meta.title` fallback。改為 `compose(scenes, manifest, rendered, out_dir, *, lead, abr, output, fade, meta, quality, storyboard_path, manifest_path)`；`main()` 呼叫處把 `data["meta"]`、`args.quality`、`args.storyboard`、`manifest_path` 一併傳入（這些在 `main()` 都是現成變數）。`chapter_title` 在 compose 內就每個 `divider`／`intro` scene 算（compose 手上有完整 storyboard `scenes` 與 `meta`）。
  - `lead_seconds` **必記**（下游字幕用它）。`chapter_title` fallback：`scene.get("title") or scene.get("tagline") or meta.get("title") or scene["id"]`（NB3 順序修正：tagline 先於 meta.title；ch03 intro 只有 tagline）。此 fallback 抽成純函式 `chapter_title(scene, meta) -> str` 便於單測（T7-5）。
  - **NB4 lead 護欄**：compose 若 `args.lead != SCENE_LEAD_SECONDS`，印 `WARN: --lead != render lead; audio/subtitles will desync from reveals`（render 端未接 lead，不在本 task 動）。
  - concat 成功後才原子寫 sidecar（失敗不留半成品）。
- [x] **T7-3 字幕（`.vtt` 必；`.srt` 選用）**〔.vtt 已產；.srt 選用旗標未做（無 consumer，Nit2）〕：`captions.py` 由 manifest＋timeline 產 `<output.stem>.vtt`。**cue 時間＝`scene.start + timeline.lead_seconds + beat_start`**（用 timeline 記的值，B6-i）；文字＝spoken beat text（`_mimo` deck 無 LaTeX）；空文字 cue 已在 T7-1 濾除。`.srt` 屬額外格式（Nit2），**預設只產 `.vtt`**；`.srt` 加 `--emit-srt` 選用旗標，無 consumer 就先不做。sidecar 落成片旁、**不燒錄**。
- [x] **T7-4 chapters**：`captions.py` 由 timeline 的 `divider`／`intro` 場（**讀其 `chapter_title`**，NB3——title 已由 T7-2 compose 端算好，captions 不碰 storyboard）產 `<output.stem>.chapters.txt`（YouTube `M:SS Title`）；確保**首章為 `0:00`**（第一個 chapter 若不在 0 秒，補一條 0:00）。
- [x] **T7-5 selftest**：假 manifest＋假 timeline（含一場 `lead_seconds=2.0`、一場全空 beat、一場 intro `chapter_title` 由 tagline 得來）進 `captions.py` → 斷言：vtt 時戳單調遞增且＝`start+lead+beat_start`（用 `lead_seconds=2.0` 驗到 lead≠1）、空 beat 不產 cue、chapters 首條 `0:00`＋章名取自 timeline 的 `chapter_title`。**lead-awareness 由此單元測試證明，不靠端到端跑非預設 lead（NB4）。** 另加一個 compose 端 fallback 順序的小測：intro 只有 tagline → `chapter_title == tagline`（非 meta.title）。
- [x] **T7-6 驗收（不跑非預設 lead；NB4）**〔合成影片直測 compose：三 sidecar 皆出、lead_seconds=1.0、NB3 chapter fallback、vtt 首 cue=start+lead+beat、lead=2.0 印 WARN〕：demo deck mock 全跑 `make.py`（**預設 lead**）→ 輸出旁出現 `<stem>.timeline.json`／`.vtt`／`.chapters.txt`；timeline 記錄 `lead_seconds == SCENE_LEAD_SECONDS`、每個 divider/intro 場有 `chapter_title`；vtt 拖進播放器對得上。**不要**用 `--lead 2` 產成片當驗收——render 端未接 lead，那支會 A/V 錯位；改單獨確認「傳非預設 `--lead` 時 compose 印出 NB4 的 WARN」。
- [x] **T7-7 Commit**：`feat(video): [T7] compose emits <stem>.timeline.json + sidecar .vtt + chapters (lead-aware, stem-scoped, empty-cue-safe)`。

### T8 — 單次編碼 compose（治 F13）

**Files:** Modify `video/make.py`（`_mux_content`/`_mux_silent`/`_mux_cue` :489-547、`_concat` :550-563）

- [x] **T8-1 統一編碼參數常數**〔＋x264-params 補齊 bt709 primaries/transfer，libx264 -color_* 只寫 matrix〕：

```python
ENCODE_V = ["-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
            "-color_trc", "bt709", "-colorspace", "bt709"]
```

  三個 `_mux_*` 的 `vcodec = (... if vf else ["-c:v", "copy"])` 改為**一律** `["-vf", vf, *ENCODE_V] if vf else [*ENCODE_V]`（fade=0 也編一次，換取 concat 可 stream-copy 且參數統一）。
- [x] **T8-2 `_concat` 改 stream copy＋faststart**：`["-c", "copy", "-movflags", "+faststart"]` 取代 re-encode 參數。
- [x] **T8-3 驗收**〔合成 testsrc 1080p 直測 _mux_silent＋_concat：full bt709／aac48k stereo／faststart／時長 4.02s〕（demo deck mock、1080p）：改前後各 build 一次——(a) 總時長差 <0.1s；(b) `ffprobe` 最終檔：h264／yuv420p／bt709 標記在、音訊 aac 48k stereo；(c) make.py 既有 `[sync]` 檢查仍 clean；(d) 抽 2-3 幀肉眼比對暗底 banding 不劣化（應更好——少一代編碼）。
- [x] **T8-4 Commit**：`fix(video): [T8] single video encode per segment; concat stream-copies (+bt709 tags, faststart)`。

### T9 — 場景間節奏 A/B（**裁決件**；治 F12，尊重其「刻意設計」性質）

**Files:** Modify `video/make.py`（**新增 `--output`**、`_fade_vf` 拆 in/out、`compose()` per-boundary 決策、新 CLI）

- [x] **T9-1 先加 `--output`（B7 前置，必做）**：`make.py` 現在**沒有** `--output`，成片路徑由 meta deterministic 導出——兩次 A/B build 會寫到**同一個 mp4**、第二次蓋掉第一次。先加 `parser.add_argument("--output", type=Path, default=None)`，`compose(..., output=args.output or <既有 deterministic 路徑>)`。A/B 兩版用**不同** `--output` 檔名。
- [x] **T9-2 機制**：`_fade_vf(video, fade)` → `_fade_vf(video, fade_in, fade_out)`；`compose()` 依相鄰 scene kind 決定每 segment 的 (in, out)：與 `divider`/`intro`/`outro` 相鄰的邊界與片頭片尾用 `--transition`（維持 0.2 預設），content–content 邊界用新 CLI `--intra-act-transition`（**預設 0.2＝行為不變**；A/B 時傳 0）。
- [x] **T9-3 產 A/B 交付物**〔用 _demo_derivation（隔離 1 個 content-content 邊界＠32s）；抽幀證差異；HTML `video/_audit/REVIEW-transition-ab.html`；awaiting adjudication〕（離線、reuse 既有 §3.1 音檔即可）：選一個 act（建議含 3+ 個連續 content 場的段落），render+compose 兩版：現行 vs `--intra-act-transition 0`，用 **T9-1 的 `--output` 給不同檔名**。**產物落點（NA4）：** 兩支 mp4 落 `/video/output/`（gitignored，不進版控）；一頁繁中說明 HTML（兩版差異、看點、建議聽的秒段、兩支 mp4 的相對路徑＋sha256）落**tracked audit 路徑** `video/_audit/REVIEW-<deck>-transition-ab.html`（不要放進 gitignored 的 output，否則說明檔也被 ignore 吃掉）。標 `awaiting adjudication`（Adv7：不 STOP 卡住 T10）。
- [x] **T9-4 裁決後**〔裁決 A：content-content 也淡黑＝現行預設，免改 code；記入 DESIGN.md〕：把選定值設為預設、更新 `DESIGN.md` 轉場節（引裁決日期）、可視需要對 lead/tail 1s/1s 開第二輪 A/B（本輪**只動 fade 一個變數**）。
- [x] **T9-5 Commit**（**B7：mp4 進不了版控**——`/video/output/` 在 `.gitignore`；只 commit code＋說明 HTML＋產物路徑/hash，不要 force-add 大 mp4）：`feat(video): [T9] make.py --output override + per-boundary transition control + act A/B deliverable`。

### T10 — loudness house spec（**裁決件**）

**Files:** Create `video/pipeline/loudness_ab.py`（一次性工具，或放 scratch 由執行 session 判斷）；Modify `video/make.py`（裁決後）

- [x] **T10-1 產 A/B**〔樣本 10_fundamental_limit.wav，two-pass loudnorm 命中 -19.0/-17.1/-15.8；HTML `video/_audit/REVIEW-ch03_s31-loudness-ab.html`〕：取一段代表性 act 音訊，ffmpeg `loudnorm` 兩段式做 -19／-17／-15.5 LUFS（TP 上限 -1.5 dBTP）三版；繁中 HTML A/B 稿（含三版 `<audio>`＋各版實測 I/TP 表＋一句「YouTube 參考位準約 -14 LUFS、只往下 normalize」的脈絡說明）。**HTML 落 tracked 路徑 `video/_audit/REVIEW-<deck>-loudness-ab.html`**（NA4 同 T9：不要放 gitignored 的 `/video/output/`）；三版音訊 WAV 落 scratch/output，HTML 用相對路徑＋sha256 引。
- [x] **T10-2 產 A/B 後標 `awaiting adjudication`**（Adv7：與 T9 一起交裁決，不 STOP 卡住彼此）。
- [x] **T10-3 裁決後定版（首輪只做核心；Adv5）**〔裁決 -19 LUFS；HOUSE_LUFS+_loudnorm_final+compose apply_loudnorm+CLI；commit `4ed34f0`〕：(a) `_concat` 階段加 **two-pass** `loudnorm`（與 T10-1 A/B 同法，非 one-pass dynamic；video 仍 `-c:v copy`，音訊該處編一次——與 T8 相容；別漏 `-ar 48000 -ac 2`）；(b) `compose()` 尾端印整片 **I／TP** 報告，超出裁決容差（預設提案 I ±1 LU、TP ≤ -1.5 dBTP）印 WARN。**逐場 LU 極差與 `silencedetect`／clipping 檢查另立後續 task、不併入首輪**——因 `silencedetect` 會把**設計內建的 1s lead＋1s tail**（F12）報成大量靜音，需先定義「超過設計 gap 多少才算異常」才不會滿屏誤報。
- [x] **T10-4 Commit**〔A/B 產生器＋交付物已 commit；production 接線＝T10-3 待裁決〕：`feat(video): [T10] house loudness target + two-pass loudnorm + integrated I/TP report`（body 記裁決值）。

### T11 — 文檔 stale-line 清理（治 F15；~1 小時，統一收尾做）

**Files:** `video/DESIGN.md`、`video/README.md`、`video/REVIEW_GATES.md`、`video/RUNBOOK-mimo-narration-route.md`、`video/REBUILD_STATUS.md`、`ENVIRONMENT.md`、`tools/doctor.py`

- [x] **T11-1** `DESIGN.md:219`「House cue candidates（**待使用者裁決**）」→ 改為已裁決收錄語（與 :237-239「使用裁決出的 bed」對齊；裁決時間以 `git log -- video/pipeline/assets/audio/house/` 為準）。
- [x] **T11-2** `README.md:53/300/318` forced-alignment 敘述：production 路徑＝`pipeline/scene_align.py`（stable-ts）＋ASR QA（whisper-timestamped）；`experiments/forced_alignment_dean/` 標為歷史起源、僅參照。
- [x] **T11-3** 1080p/4K 一句話交叉引用：`README.md:160` 補「agent 預設行為見根 `CLAUDE.md`（一律 1080p，除非使用者要求）；§3.1 真 4K final 另議見 `REBUILD_STATUS.md`」。根 `CLAUDE.md` **不動**（權威、現述已正確）。
- [x] **T11-4** `REVIEW_GATES.md:129`「無自動 listen-back」行：T6 落地後改寫為「離線 listening pack（`pipeline/listening_pack.py`）＋正式交付前人工完整聽一次」。
- [x] **T11-5** `RUNBOOK-mimo-narration-route.md` 步驟 4：T2a 後 `--backend` 必填的指令樣式核對（現行已明寫 `--backend mimo`，僅確認無遺漏處）；補一句「先跑 `--dry-run` 取得預期／最壞 call 數作為報價」。
- [x] **T11-6** `ENVIRONMENT.md`＋`tools/doctor.py`（Adv6）：`stable-ts`／`whisper-timestamped` 現為 **production** QA／alignment 依賴（非 optional experiment）——列入清單與檢查項，且把仍指向 `experiments/forced_alignment_dean/` 的 PASS 路徑改指 `pipeline/scene_align.py`。
- [x] **T11-7 house cue（Adv6）**〔並入 T11-1 DESIGN house cue 已裁決 Candidate B〕：`README.md`（Codex 指約 :162）仍稱 house cues「待裁決」，但 Candidate B 已落地——改為已裁決語（與 `DESIGN.md` T11-1 同步）。
- [x] **T11-8 RUNBOOK allowlist（Adv6）**：`RUNBOOK-mimo-narration-route.md` 若列「全部 content template」仍是 6/9，改列 9 個或引用 `pipeline/template_names.py:CONTENT_TEMPLATES`（與 T3 對齊）。
- [x] **T11-9 新資料契約進 `DESIGN.md`（Adv6）**：本輪新增的 manifest／檔案契約要在 DESIGN 有記載——`meta.derived_from`（T1）、manifest `receipt`（T2d）、`validation.qa`（T4）、`<stem>.timeline.json`／`.vtt`／`.chapters.txt`（T7）。
- [x] **T11-10 新旗標文檔（Adv6）**〔DESIGN＋RUNBOOK 記全部新旗標〕：`README.md`／`RUNBOOK` 說明 `--backend`（現必填）、`--force-backend-switch`（僅 `--scene all`）、`--force-clobber`（覆寫損壞/孤兒音檔）、`--output`（T9）的用途與限制。
- [x] **T11-11 beats 非「免費」更正（B8，真衝突非 drift；含 active code）**〔改 scene_fallback/tts.py/_selftest_scene_align/DESIGN/RUNBOOK 為 budget-exempt；保留 arbiter-免費＋billed=False flag〕：F6 已證 MiMo 下 beats terminal 逐非空 beat 計費。**用 multiline `rg` 掃全部誤導處**（R3-B4：linewise grep 漏掉跨行的 `non-billed`＋`'beats'`；且要排除 `_audit` HTML 內嵌 base64 巨行）：

```bash
rg -n --multiline --pcre2 -g '*.py' -g '*.md' -g '!**/__pycache__/**' \
  "(free|non-billed|unbilled|免費|零計費)[^.]{0,80}?beat|beat[^.]{0,80}?(free|non-billed|unbilled|免費)" \
  video/pipeline video/*.md
```

  已知命中（2026-07-11 快照，含 R3-B4 補抓的跨行）：`pipeline/scene_fallback.py:37-38`（`non-billed 'beats' terminal`）＋`:57`、`pipeline/tts.py:714`、`pipeline/_selftest_scene_align.py:316`、`DESIGN.md:987`。散文統一改為：「beats terminal 不受 rungs 2–3 的 `RetryBudget` 限制（budget-exempt），但 MiMo 下每個非空 beat 仍是一次 backend call；dry-run 的 worst 欄已計入。」
  - **勿誤改兩類正確敘述：** (i) `arbiter`（small.en 本地重對位）**確實免費**（無 API）——`_selftest_scene_align.py:292`／`_integration.py:102`／`DESIGN.md:987` 的「arbiter 免費／arbiter is free」不動；(ii) **code 的 `billed=False` flag 不動**——`run_ladder` 的 rung 宣告（`("beats", False, beats)`、`RetryBudget` 的 `billed` 判定）是**正確的 budget 分類**（beats 不計入 rungs 2–3 的 billed 配額），改的是把它**寫成「免費/no-cost」的散文/註解**，不是那個布林值。
- [x] **T11-12** `REBUILD_STATUS.md`：加本 kickoff 指針行＋Phase 完成度。
- [x] **T11-13 Commit**〔`7dcc93f`〕：`docs(video): [T11] stale-line cleanup + new data-contract/flag docs + beats-not-free correction`。README 一律繁中（根 CLAUDE.md 規則）。

---

## 8. 明確不做（deferred）＋重啟條件

| 項目 | 為何緩 | 重啟條件 |
|------|--------|---------|
| in-memory overlay 取代 `_mimo.yml`（原建議 #1 首選） | T1 hash gate 已殺掉漂移類 bug；overlay 牽動輸出目錄選擇（`tts.py:854`）、成片命名、RUNBOOK | T1 落地後 derive 流程仍反覆絆到人時 |
| scene fingerprint render cache（原建議 #8 前半） | hash 正確性面大（template/hook/pipeline code 傳遞依賴）；`--scene` 單場重 render 已覆蓋多數迭代 | 單章 render 時間成為實際瓶頸時 |
| motion primitives 共用庫（原建議 #6 後半） | rule of three：同類 hook 出現三次再升級；現各 deck hook 數不足 | 第三次寫出同型 hook 時（在 DESIGN.md hook 節記 tally） |
| §3.1 補 render／補修 | 使用者 2026-07-11 裁決：§3.1＝實驗品 | 產線硬化（Phase 1–3）完成後，§3.1 **整節重做**＝新產線全流程驗收（屆時另開 kickoff，真 TTS 依 CLAUDE.md 報價徵同意） |
| 重度 mastering／音效設計 | T10 只定 target＋自動檢查；現況場間 1.3 LU 無急迫問題 | house target 裁決後仍有聽感問題時 |

---

## 9. 完成定義（DoD）

- **Phase 1 DoD：** T1–T4 落地、新舊 selftest 全綠、demo deck mock 全流程通過、Codex review 0 blocking。**達成後 §3.2 才進真 TTS**（屆時 dry-run 新報表＝報價依據）。
- **Phase 2 DoD：** T5 落地；§3.2 storyboard 過 schema＋sizecheck（含新 cross-check）0 error。
- **Phase 3 DoD：** T6–T8、T11 落地；T9／T10 至少產出 A/B 交付物並取得裁決（裁決本身不阻塞其他 task）。
- **總驗收：** 待使用者發起 §3.1 整節重做，走完 derive → dry-run 報價 → 真 TTS → render → compose（timeline/字幕/chapters 齊出）→ listening pack → 視覺閘，全程無需手動繞道。

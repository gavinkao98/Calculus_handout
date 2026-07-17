# Kickoff：可讀性回填 Ch1–Ch4 —— ① reader-persona first-read ＋ ② introduce-before-use（Claude gate-1 ＋ Codex gate-2）

> 整段貼進**新對話**即可開跑；或對新對話說「讀 `handout/_dev-archive/general/PROMPT-readability-backfill-ch01-04.md` 並執行」。

## 你是誰、要做什麼

你在一個 fresh session（無前對話記憶）。任務：把 **2026-06-28 新增的兩條規則**回填到 **Ch1–Ch4**，採**雙閘**：Claude gate-1（免費）→ Codex gate-2（訂閱、跨模型獨立複核）。兩條是**平起平坐的具名檢查**，不是一主一附：

- **① reader-persona first-read** —— 以「**讀完高中先修、用英文（非母語）自學、第一次線性讀**」的視角，找易懂性摩擦（既有 Gate 6 散文閘「易懂性 A」維度的磨利版）。
- **② introduce-before-use** —— 記號／術語／非正式記法是否「**先用後定義**」（prose 閘 U4 的排序面，**獨立掃一遍**）。

硬性範圍：

- **唯讀、propose-only：在使用者逐條裁決前，不改任何課文（`fragments/`）。**
- **只跑這兩條，不重跑任何既有閘。** 特別是 **不要**做「跨模型專家複核數學／散文／圖」—— 那**就是**你既有的數學閘 M1–M8、S·A·V 散文閘、圖閘 D1–D8 的 gate-2（Claude＋Codex 早已跑過、已過），重跑＝白工。**專家／審稿者角度已由現有雙閘飽和；本關只補「讀者／學生」這一個真缺口。**
- 這不是新開一道關，是把既有 Gate 6「易懂性 A」磨利＋把 U4 排序面拉成具名檢查，回填四章。

## 先讀（權威來源，依序）

1. `CLAUDE.md`（根）＋ `handout/CLAUDE.md` ＋ `handout/PIPELINE.md` — 專案紀律、閘序、付費調用先徵同意、commit 規則、四級分流。
2. `handout/_audit/PROSE-AUDIT-RUBRIC.md` — **本關的 single source of truth**。重點讀：「易懂性 A」開頭的 **reader persona（2026-06-28）**、**U4 的「結構性排序（需 reorder）優先往上游」子條**、文末「**可選：跨模型 first-read 第二讀者**」一節（含兩條編碼／噪音硬紀律）。
3. `CONTENT_DIRECTION.md` §2「範圍與深度」欄的 **introduce-before-use**。
4. `CONTENT_SPEC.md` §3（語域／語聲）— 改寫的 no-dumbing 護欄依據。
5. HTML 報告格式範本：`handout/_audit/REVIEW-ch01-prose-audit-gate1.html` ／ `-gate2.html`。

## 範圍與順序

- Ch1–Ch4，每章每節。**節清單以 `handout/build.py` 的 `CHAPTERS` registry 為準**（單一真實來源，別硬記）。
- 順序：**Ch1 先當 pilot 校準** → 確認判準與 HTML 格式 OK → 再 Ch2 → Ch3 → Ch4。

## 流程（每章；雙閘，每閘 ⛳ 停）

**Gate 1（Claude，免費）** —— 逐節讀 `handout/fragments/ch{NN}/sec-*.html`，**每節各跑下面兩條具名檢查**：

**檢查 ①：reader-persona first-read**
- 以 reader persona（高中生／L2／第一次線性讀）找會卡住／重讀／想放棄的點。
- 每條 finding 一行：`locus`（引原文句／符號）｜什麼讓這讀者卡｜維度（U#／F#；多落在 **U3 跳步、U4 先用後定義、F3／F4 句構句長**）｜severity（**Lost／Slowed／Minor，誠實重評，別灌水成 Lost**）｜`minimal_unstick`（最小、不加水、不降難度）｜四級分流。

**檢查 ②：introduce-before-use（獨立掃一遍，別只靠 ① 順帶）**
- 逐節掃：每個**記號／術語／非正式記法**在**首次被用之前**，是否已被介紹或在使用處當場 gloss。（典型反例：新記號在 example 用掉後才正式定義，如 ch01 §1.4 的 `=∞`。）
- 修法**明確標型**：
  - **(a) 局部** —— 在使用處補一句 gloss／一條 forward-ref（低風險，定稿期可改）。
  - **(b) 結構性 reorder** —— 需搬動定義／介紹段到首次使用前。**對已編號定稿章會 cascade 編號／cross-ref——警示之、別在定稿期硬搬**；如實報「需 reorder＝結構」交裁決（最便宜其實在 Mode A 上游、已不適用於回填，故此處只報不搬）。

- 兩檢查**合併產** `handout/_audit/REVIEW-ch{NN}-readability-gate1.html`（standalone、MathJax CDN、雙擊即開、頂部摘要表、逐條卡片、含 `<del>`／`<ins>` diff、穩定編號 `G1-…`，**每條標明來自 ① 或 ②**）。⛳ 停給使用者過目。

**Gate 2（Codex，訂閱；先說模型／用量／成本徵同意）**
- 對**同樣兩條檢查（①＋②）**做獨立跨模型複核。用 PATH 上的 `codex`（npm `codex-cli 0.136.0`，已登入 ChatGPT、走訂閱）：
  `codex exec -s read-only -C <repo> --output-schema <schema.json> -o <out.json> - < <prompt.txt>`
  （schema 全欄 required、`additionalProperties:false`、enum、無 min／max；prompt 經 stdin 餵 raw UTF-8。）
- **硬紀律（編碼坑，2026-06-28 實證）：把 fragment 文字「乾淨 inline」貼進 prompt**（你先用 UTF-8 讀好再貼），**不要叫 Codex 用 `-C` 自己讀 fragment 檔**——它在本機會把 UTF-8 解成亂碼（`—`→`??`、`§`→`禮`、彎引號→`?`），整批「編碼 bug」全是假陽性、還會誤判 worst stall。
- 產 `REVIEW-ch{NN}-readability-gate2.html`（穩定編號 `G2-…`）。

**Triage／收斂**
- 取**兩閘交集**為最高信心（intersection＝最低後悔）；severity 誠實重評；砍 non-finding 與過度 gloss（吹毛求疵的詞彙替換）；每個修法對 `CONTENT_SPEC §3` 核「**no-dumbing、no-filler、保 formal register**」。
- ⛳ 逐條交使用者裁決。**裁決前不改任何課文。**

## 硬護欄

- **propose-only、唯讀。** 採納須使用者逐條點頭後才改：`fragments/ch{NN}/` → `python handout/build.py ch{NN}` → 對新句跑**範圍限定 Mode B** → 產 `REVIEW-ch{NN}-readability-applied.html` 回歸報告。
- **不加水、不口語化、不降數學難度。** inherent 難度（ε-δ 巢狀量詞、振盪論證等）＝ hard but fair，**別軟化**——只報「**真摩擦**」，不報「這主題很難」。
- **不 over-report：** 四級分流，**乾淨的節是有效結果**，別湊數。
- **不重跑既有閘**（數學／散文 S·A·V 其他維度／圖）——那是已過的專家雙閘，不在本關範圍。
- **付費／訂閱調用（Codex）前**先說模型／用量／成本徵同意（`CLAUDE.md`）。Codex 一輪約 ~5–6 萬 token／節級別，走訂閱配額。
- **commit 經授權才做**；繁中、body 逐條記裁決。

## 產物

每章兩份 HTML（`-readability-gate1/2.html`，各含 ①②兩類）＋交集候選清單，供裁決；採納後出 `-applied.html` 回歸。Ch1 跑完當校準基準，再推 Ch2–4。

---
*本檔由可讀性 lens 校準對話（2026-06-28）產出，作為 Ch1–4 回填的 kickoff。rubric 規則本身以 `handout/_audit/PROSE-AUDIT-RUBRIC.md` 為準，本檔不重述。*

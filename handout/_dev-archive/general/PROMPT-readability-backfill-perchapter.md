# Kickoff：可讀性回填（單章版）—— ① reader-persona ＋ ② introduce-before-use（Claude gate-1 ＋ Codex gate-2）

> **本輪章節（只改這一行）：** `ch02`　← 換成 `ch03` / `ch04`，各開一個新對話並行跑。
>
> 整段貼進**新對話**即可開跑。**Ch1 已完成、為 pilot 基準**：見 git commit `3ca7ca9` 與
> `handout/_audit/REVIEW-ch01-readability-{gate1,gate2,applied}.html`、
> `handout/_dev-archive/ch01/ch01_readability-gate2-audit.md`。本檔流程＝Ch1 跑完後的**定版**，
> 含 Ch1 實證教訓。判準/規則本身以 `handout/_audit/PROSE-AUDIT-RUBRIC.md` 為準，本檔不重述。

## 你是誰、要做什麼

fresh session（無前對話記憶）。把 **2026-06-28 兩條具名檢查**回填到「本輪章節」，採**雙閘**：
Claude gate-1（免費）→ Codex gate-2（訂閱、跨模型獨立複核）。兩條**平起平坐**：

- **① reader-persona first-read** —— 以「讀完高中先修、用英文（非母語）自學、第一次線性讀」的視角找首讀摩擦。
- **② introduce-before-use** —— 記號／術語／非正式記法是否「先用後定義」（U4 排序面，**獨立掃一遍**）。

硬性範圍：

- **唯讀、propose-only：逐條裁決前不改任何課文（`fragments/`）。**
- **只跑這兩條，不重跑任何既有閘**（數學 M1–M8／S·A·V 其他維度／圖 D1–D8 已過，重跑＝白工）。
- 不加水、不口語化、不降數學難度；inherent 難度（ε-δ、振盪）＝hard but fair，只報真摩擦。

## 先讀（權威來源，依序）

1. `CLAUDE.md`（根）＋ `handout/CLAUDE.md` ＋ `handout/PIPELINE.md` — 紀律、閘序、付費先徵同意、commit、四級分流。
2. `handout/_audit/PROSE-AUDIT-RUBRIC.md` — **single source of truth**。重點：「易懂性 A」的 reader persona、U4「結構性排序（需 reorder）優先往上游」、文末「可選：跨模型 first-read」兩條編碼／噪音硬紀律。
3. `CONTENT_DIRECTION.md` §2「範圍與深度」的 **introduce-before-use**。
4. `CONTENT_SPEC.md` §3（語域／語聲）— no-dumbing 護欄。
5. **格式＋方法基準（照抄 Ch1）：** `handout/_audit/REVIEW-ch01-readability-{gate1,gate2,applied}.html`、`handout/_dev-archive/ch01/ch01_readability-gate2-audit.md`。

## 範圍與順序

- 本輪章節**每節**。**節清單以 `handout/build.py` 的 `CHAPTERS` registry 為準**（單一真實來源，別硬記；章開場併入該章第一節 `sec-N-1`，無獨立 `sec-intro`）。
- 逐節跑；先自己用 Read 把全章 fragment 讀過一遍（核對 verbatim 引文、掌握已知 canonical 摩擦）。

## 流程（每閘 ⛳ 停）

### Gate 1（Claude，免費）

用 **Workflow** 並行：

- **每節一個 reader agent** 跑 **①＋②**（餵它本節路徑＋**先前各節路徑**，供 ② 查記號/術語是否更早已介紹；標準高中 precalc 視為已知）。
- 再對**每條 finding** 派一個**對抗 verifier**（預設懷疑：誠實重評 severity＝Lost／Slowed／Minor、查 no-dumbing、確認 ② 真為先用後定義而非當場 gloss／更早已介紹／標準 precalc）。
- 結構化輸出（schema：check／locus／verbatim quote／dimension U#F#／what_stalls／severity／minimal_unstick／fix_type／triage_tier）。
- 產 `handout/_audit/REVIEW-ch{NN}-readability-gate1.html`（standalone、MathJax CDN、頂部摘要表、逐條卡、`<del>`/`<ins>` diff、穩定編號 `G1-…`、**每條標 ① 或 ②**）。**⛳ 停**給使用者過目。

**②結構型（需 reorder）**（如 Ch1 §1.4 `=∞`）：定稿章搬動會 cascade 編號／cross-ref ——**只報不搬**、標「needs reorder＝結構，宜上游」，或改**極輕 forward-ref**（別重述鄰句已說的意思＝過度解釋）。

### 裁決 → 套用 → Mode B 回歸（每輪都要）

- ⛳ 逐條交使用者裁決（採／不採／改修法）。**裁決前不改任何課文。**
- 採納者改 `fragments/ch{NN}/` → `python handout/build.py ch{NN}` → 對**每條新句**跑**範圍限定 Mode B**（每條一個對抗 reviewer：修好摩擦？守語域不灌水不過度 gloss？未引入新 U/F 問題？**若動到數學 display 要驗算**）。
- **⚠ Ch1 實證教訓：套用（改寫）後務必逐句比對原文，確認沒在改寫時掉字**——例如限定詞 `integers`／`for all`／`x≠0`／`>0`。Ch1 套用某條時不慎刪掉 `integers`，gate-1 reader＋verifier＋Mode B **三次 Claude 檢視都沒抓到**，靠 gate-2 跨模型才抓到。
- 產／更新 `handout/_audit/REVIEW-ch{NN}-readability-applied.html`（old→new、每條附 Mode B 結果）。

### Gate 2（Codex，訂閱計費——**先說模型／用量／成本徵同意**）

- 用 **PATH 上的 `codex`**（`codex-cli 0.136.0`，已登入 ChatGPT、走訂閱；**勿**用 alpha 絕對路徑——與 `service_tier="default"` 不相容）。
- **逐節**：用 **Python**（UTF-8 read+write）把 ① 指令文（①＋② 同 gate-1）＋ ② **本節 fragment 全文 clean inline** ＋ ③ **本章先前已介紹之記號/術語 ledger** 拼成 `prompt-<sec>.txt`；另寫 `schema.json`（**全欄 required、`additionalProperties:false`、enum、無 min/max**）。
- 指令（**Bash 工具**、prompt 經 **stdin** 餵 raw UTF-8）：
  `codex exec -s read-only -C <repo> --output-schema schema.json -o out-<sec>.json - < prompt-<sec>.txt`
- **硬紀律（編碼坑）：clean inline 餵入，絕不讓 Codex 用 `-C` 自讀 fragment**——本機會把 UTF-8 解成亂碼（`—`→亂碼、`§`→亂碼、彎引號→`?`），整批「編碼 bug」全是假陽性。**先跑一節 smoke test** 驗 schema 解析、輸出 JSON 0 個 U+FFFD、編碼正常，再續跑其餘節（可循序背景跑，避免訂閱並發限流）。
- 用量參考：Ch1 每節 ~2.5–3.3 萬 token、全章 ~17 萬。**徵同意時據此估本輪。**
- 產 `handout/_audit/REVIEW-ch{NN}-readability-gate2.html`（穩定編號 `G2-…`）＋**轉錄原始輸出**到版控 `handout/_dev-archive/ch{NN}/ch{NN}_readability-gate2-audit.md`（scratchpad gitignored、換機即失）。

### Triage／收斂

- **取兩閘交集為最高信心**（intersection＝最低後悔）。
- **gate-2 系統性偏嚴、會 over-report**（「每個記號都要 gloss」的 `⟹`/`⟺`/`↦`/`vanish`/`blows up` 之類，多為標準記號／就地語境化）——一律過**四級 triage**（核 no-dumbing、誠實重評、砍 non-finding、砍吹毛求疵詞彙替換）。
- **gate-2 的不可取代價值＝抓 gate-1 套用後的迴歸＋跨模型獨立交集**（見上 Ch1 教訓）。即使順序是「先套 gate-1 再 gate-2」仍要跑。
- ⛳ 逐條交裁決；採納者套用 → `build` → Mode B → 更新 `applied` 報告。

## 硬護欄

- **propose-only、唯讀**；採納須使用者逐條點頭後才改。
- 不加水、不口語化、不降難度；不 over-report（**乾淨的節是有效結果**）。
- 不重跑既有閘。
- **付費／訂閱（Codex）前先說模型／用量／成本徵同意**；範圍變更需重新徵得同意。
- **commit 經授權才做**；繁中、subject ≤70 字、body 逐條記裁決（供 `git log --grep` 撈回）、結尾 `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`。
- **commit 前 render 自驗**：`node handout/_render/shot.mjs "file:///<abs>/handout/chapter{N}-print-standalone.html" <out>/verify full` → 須 `ready=true`、`katex-errors=0`。
- **commit 範圍乾淨**：只納本輪 readability 相關檔（`fragments/ch{NN}/*`、`chapter{N}-print-standalone.html`、3 份 `REVIEW-ch{NN}-readability-*.html`、`_dev-archive/ch{NN}/ch{NN}_readability-gate2-audit.md`）；先 `git diff --cached --name-status` 確認沒夾帶無關既有改動。

## 產物

每章：`REVIEW-ch{NN}-readability-{gate1,gate2,applied}.html` ＋ `_dev-archive/ch{NN}/ch{NN}_readability-gate2-audit.md`。

## Ch1 pilot 結果（基準參考）

- gate-1：13 raw → 7 採（**整章 0 blocking**）。canonical：§1.4 `=∞`（②結構，輕量 forward-ref）、§1.6 `ε=|L−M|/2`（①動機 gloss）。對抗 verifier 砍掉 ~46% 過度回報。
- gate-2（Codex，~173k token）：25 raw → **1 迴歸修復**（套用時掉 `integers`）＋**1 真交集**（§1.4 `=∞`）＋**9 advisory 採**＋**14 砍**。
- Mode B 回歸：gate-1 套用 7/7、gate-2 advisory 套用 9/9 pass。render `ready=true math=1286 katex-errors=0`。
- commit `3ca7ca9`（範圍乾淨：12 檔，未碰 ch02／docs／build.py）。

---
*本檔為 Ch1 pilot（2026-06-28）跑完後定版的單章流程，供 Ch2–4 逐章（可並行各開對話）沿用。*

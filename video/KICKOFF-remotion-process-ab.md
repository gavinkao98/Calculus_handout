# KICKOFF — Remotion 製作流程 A/B 對比（2026-09-29 立檔，待開工）

> **起因（使用者，2026-09-29）：** 檢討輪的裁決稿（[`_audit/REVIEW-remotion-process-review-2026-09-29.html`](_audit/REVIEW-remotion-process-review-2026-09-29.html)）
> 攤開了四題的取捨後，使用者裁決**不先紙上裁四題，改成兩條路線做同一節再比**：
> 「我們 remotion 目前分兩個分支，一個是繼承我之前 manim 的，另一個是全部重新開始設計流程的」；
> 「B 重設線就先只沿用紙本風格、STYLE.md、元件、logo，我如果覺得有問題，再去 A 繼承線裡面參考原本的做法」；
> 「內容稿不繼承、不過內容稿一樣是參考講義寫出來的。病清單給 B，照預設立 KICKOFF」。
>
> **本檔是兩條線的契約與量測協定。** 四題（Q1–Q4）的答案改由對比結果回答；裁決稿的處置清單與
> [`KICKOFF-remotion-process-review.md`](KICKOFF-remotion-process-review.md) §7 的凍結清單延續凍結到對比收線。
> 本檔立檔輪不做片、不呼叫任何付費／外部 API。

---

## 0. 給新 session 的啟動提示（A、B 各一段，可整段貼；**兩線各自一個 session、各自 worktree，不互看**）

### A 繼承線

```
你負責 NTU 微積分影片線（repo Calculus_handout，video/ 子樹）§3.2 The Chain Rule 的 Remotion 版視覺線，
路線 A（繼承 Manim gen-2 的流程）。全程繁體中文溝通。

契約＝video/KICKOFF-s32-remotion-phaseB.md 原樣（G0–G7、七層閘、一輪一 merge 一 render 一審、里程碑六鏡），
加上 video/KICKOFF-remotion-process-ab.md §1.1 的四處改寫（目錄／composition／deck id 改 A 版、D1 直接走 S 重配、
量測表照 §3 即時記錄、借用帳照 §2）。開工前依序讀：
  video/KICKOFF-remotion-process-ab.md            ← 本檔（§1.1、§2、§3、§4、§5）
  video/KICKOFF-s32-remotion-phaseB.md            ← 執行計畫（§1 裁決表依本檔 §1.1 預填）
  video/REVIEW_GATES.md §一＋§六                   ← 驗收 SSOT
  video/KICKOFF-s32-chain-rule.md §4              ← Phase A 產物（有效，照抄）
  video/DESIGN.md、video/RUNBOOK-mimo-narration-route.md、video/remotion/STYLE.md、video/remotion/s31/SCRIPT.md
  video/content_scripts/ch03_chain_rule.md、.spoken.yml；legacy/manim_video/storyboards/ch03_chain_rule_mimo.yml（只讀參考）

不准：讀 B 線的 worktree／目錄（video/remotion/s32b/、src/s32b/）；改共用元件；呼叫任何計費／外部 API 前不報量。
```

### B 重設線

```
你負責 NTU 微積分影片線（repo Calculus_handout，video/ 子樹）§3.2 The Chain Rule 的 Remotion 影片，
路線 B（流程從零設計）。全程繁體中文溝通。

你的起點是講義本身：handout/latex/src/ch03/chapter3.tex 的 §3.2（約 208–416 行；閱讀版 handout/latex/dist/ch03/chapter3.pdf）。
你要自己決定：從講義到成片之間要有哪些步驟、產物、檢查與人閘；旁白怎麼寫、怎麼確認它忠於講義；畫面怎麼設計；
什麼時候算做完。先交一頁「B 流程設計稿」給使用者過目（§1.2 第 4 條），再開工。

沿用（可讀、可用）：
  video/remotion/STYLE.md（凍結於本檔 §2.3 記的 commit）、video/remotion/src/components/、src/s31/kit.tsx 等既有元件、
  video/pipeline/assets/（品牌 logo）、video/remotion/s31/SCRIPT.md 與 q7/SCRIPT.md（既有片怎麼做的，設計素材）
  video/pipeline/ 的共用工具當黑盒：tts.py（含 --dry-run／--reuse-existing／--skip-qa／--max-billed-calls）、
  scene_align、loudnorm.py、listening_pack.py、check_storyboard.py；工具用法讀 video/README.md §指令＋§MiMo 旁白路線、
  video/DESIGN.md「與 TTS manifest 的時序契約」「Manifest schema 2」、video/SPEC-remotion-storyboard-schema.md §1–§3
  病清單：video/_audit/REVIEW-remotion-process-review-2026-09-29.html 的 §0–§4（證據表；§5 建議流程與 §6 處置清單不讀）

不繼承、不讀（§2.2）：
  video/content_scripts/ch03_chain_rule.md 與 .spoken.yml（內容稿；你自己從講義寫）、video/CONTENT_METHODOLOGY.md、
  video/REVIEW_GATES.md、video/RUNBOOK-mimo-narration-route.md、video/KICKOFF-s32-remotion-phaseB.md、
  video/KICKOFF-s32-chain-rule.md、video/KICKOFF-process-reform.md、content_scripts/_audit/ 的 rubric、
  legacy/manim_video/、A 線的 worktree／目錄（video/remotion/s32a/、src/s32a/）

借用規則（§2.1）：使用者覺得有問題、指示你去 A 線參考時，每一次記進本檔 §2.4 的借用帳。
不准：呼叫任何計費／外部 API 前不報量；改共用元件與 STYLE.md（要改就複製到自己的目錄）。
```

---

## 1. 兩條線的定義

### 1.1 A 繼承線＝平移版原樣，只改四處

| # | 改寫 | 內容 |
|---|---|---|
| 1 | 目錄與命名 | 分鏡 `video/remotion/s32a/s32a.yml`、腳本 `s32a/SCRIPT.md`、場景 `src/s32a/`、composition `S32A`（單場 `S32A-<id>`）、音檔 `public/audio/s32a_scene/`、成片 `out/s32a_*.mp4`。deck id 依 PB D3 (a)＝`ch03_chain_rule_mimo`（R 分支已作廢，但 `provenance.content_script_for` 剝 `_mimo` 找內容稿仍靠它） |
| 2 | D1 音檔 | 直接走 PB §3.3 **S 分支**（重配 23 場、上限 35 次、`--unit scene`）；R 分支（重對映）作廢——音檔已確認遺失（PB §2.2） |
| 3 | 裁決表預填 | D2 鎖死、D3 (a)、D4 (i)、D5 照 §六——即平移版自己的預設，**不做任何改良**。改良就不是繼承線 |
| 4 | 量測與借用帳 | §3 的量測表每個 task／每輪即時記；A 線也記借用帳（預期為空——A 若去參考 B，同樣要記） |

A 的其餘一切（三個確定性檢查 `s32_derive.py`／`remotion_sync_check.py`／`rewatch_pack` 三旗標、B0–B4 派工、停止條件、里程碑六鏡、final）照 PB 原文。**A 開工前置**＝PB §5 Task 0（工具線）。

### 1.2 B 重設線＝從講義到成片，流程自訂

1. **起點**：講義 `chapter3.tex` §3.2。B 自己從講義寫內容（不管叫內容稿、大綱或分鏡）；「內容稿一樣是參考講義寫出來的」——B 走的是同一條源頭，只是不接 A 的那份。
2. **沿用**（設計素材與工具，見 §0 B 段）：紙本風格、`STYLE.md`（凍結版）、既有元件、logo；`pipeline/` 共用工具當黑盒。
3. **自訂**：內容契約的形式、旁白忠實怎麼擋、分鏡格式（`tts.py` 只吃 `say`＋`{show}` 的 yml——B 若要別的格式，自己寫轉換器，這也是 B 的成本）、閘序、審查節奏、派工形狀、停止條件、成本紀錄。
4. **第一份交付＝「B 流程設計稿」**（一頁，standalone HTML 或 md 皆可）：列步驟、產物、檢查、人閘、預估停等點。使用者過目的目的不是審核內容，是讓使用者知道 B 打算怎麼做，之後才判得出「覺得有問題」；**不需使用者核准才能開工**，過目後即可動。
5. **命名**：`video/remotion/s32b/`、`src/s32b/`、composition `S32B`（單場 `S32B-<id>`）、音檔 `public/audio/s32b_scene/`、成片 `out/s32b_*.mp4`；deck id 由 B 定（不得用 `ch03_chain_rule*`，避免 `provenance` 誤對到 A 的內容稿）。

---

## 2. 隔離與借用規則（三條，缺一條就比不出來）

### 2.1 借用要記帳

使用者覺得有問題、指示 B 去 A 線參考（或反向）的每一次，記一行到 §2.4：**借了什麼做法｜為什麼｜在 B 的第幾步｜借完的結果**。收線時沒有這本帳，就分不出「B 的流程本來就夠」還是「B 靠借 A 撐住」。**借用由使用者觸發**；B 自己不得主動去讀 A 的東西。

### 2.2 分清「工具」與「流程」

- **工具**（可用、可讀其用法說明）：`pipeline/` 共用層（`tts.py` 一族、對齊、`loudnorm.py`、`listening_pack.py`、`check_storyboard.py`、`rewatch_pack.py` 若已接 Remotion）；用法文件＝`README.md` §指令／§MiMo 旁白路線、`DESIGN.md` 的 manifest 時序契約與 schema 2 節、`SPEC-remotion-storyboard-schema.md` §1–§3。理由：聲音層是外部 API 的水電，每一條計費紀律都是真金白銀換的，重造沒有意義。
- **流程**（B 不讀）：`REVIEW_GATES.md`、`RUNBOOK-mimo-narration-route.md`、`CONTENT_METHODOLOGY.md`、`KICKOFF-s32-remotion-phaseB.md`、`KICKOFF-s32-chain-rule.md`、`KICKOFF-process-reform.md`、`content_scripts/_audit/` 的七份 rubric、`legacy/manim_video/`。
- **病清單**（B 讀）：裁決稿 §0–§4（Manim 時代的病與證據、原生版哪些是碰巧、`{show}`／`atWord` 的技術事實）。給的理由：不給，B 會把 Task D 排序病、生成式審查不收斂、12 s 靜止再踩一遍；給了不算借流程，因為 §5 建議流程與 §6 處置清單不給。

### 2.3 STYLE.md 與共用元件凍結

- `video/remotion/STYLE.md`、`src/components/`、`src/s31/kit.tsx`、`src/theme.ts`、`pipeline/assets/` 凍結於本檔立檔時 main tip **`021b78c`**（含 STYLE.md 的 2026-09-26 版）。
- 任一線要改視覺契約或共用元件：**複製到自己的目錄改**（`s32a/STYLE-A.md`／`s32b/STYLE-B.md`、`src/s32x/kit.tsx`），不動共用檔；收線後再合併成一份。
- `s31/`、`q7/`、`act3/` 兩線都不動（成片逐像素不可變，PB §8）。

### 2.4 借用帳（開工後填；一次一列）

| 日期 | 線 | 借了什麼 | 為什麼（使用者的判斷原文） | 在該線第幾步 | 結果 |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

---

## 3. 量測表（兩線各一列，**即時記錄、不事後估**；沿用 [`REBUILD_STATUS.md`](REBUILD_STATUS.md)「每節成本量測」的欄位）

### 3.1 成本

| 欄位 | 怎麼量 | A | B |
|---|---|---|---|
| in-house token | 每個子代理回報的最終累計（含設計、實作、各閘 gate-1、回歸） | **Phase A 的 ≈9×10⁵ 算進 A**（A1–A5 是 A 線的前段） | 從講義起算 |
| 外部 token／呼叫 | Codex／agy 每次的 `usage`；逐次徵同意 | | |
| TTS billed calls | manifest `receipt.backend_calls` 累加；另記 planned／worst／實際／浪費 | 上限 35 | 上限 35 |
| render 次數 | 全片 1080p render 次數（mock 另計；per-scene batch 算 1） | | |
| 輪數 | 該線自己定義的「一輪」次數（A＝PB B4 的輪；B＝自己的定義，要寫明） | ≤5 | ≤5 |
| 牆鐘 | 日曆天＋各 task 的 render 時間＋停等點數與每個停等點的等待時長 | | |
| 並行摩擦 | merge 衝突次數、等 render／tts 時間窗次數、`npm ci` 次數 | | |
| 新建工具 | 為這條線新寫的腳本／檢查器（檔數、行數、紅測試數） | PB Task 0 三支 | B 自報 |

### 3.2 品質

| 欄位 | 怎麼量 | A | B |
|---|---|---|---|
| 自家閘 blocking | 各閘每輪 blocking 數（A＝PB §4.1 的閘；B＝自訂的閘，名稱與判準要寫明） | | |
| 里程碑審 must | A＝六鏡 must 數；B＝自訂審的對應量（沒有就記「無」） | | |
| 12 s 最長靜止 | 若 `rewatch_pack` 已接 Remotion，兩支都量（同工具、同門檻）；沒接就兩支都不量 | | |
| 使用者看片裁決 | must／should 條數（兩支用同一張紙記） | | |

### 3.3 漏網（收線後的交叉審，唯一能證明「哪些閘多餘、哪些不能少」的量）

| 欄位 | 怎麼量 |
|---|---|
| A 閘審 B 片 | 把 A 線用過的每一道閘（NFA、pedagogy、視覺 gate-1、12 s、六鏡）對 B 的成片跑一次；記每閘 blocking 數 |
| B 閘審 A 片 | 把 B 線用過的每一道檢查對 A 的成片跑一次；記每項 finding 數 |
| 漏網率 | 對方閘抓到、自家閘沒抓到的 blocking 數；再逐條判是「真問題」還是「閘的口味」 |
| 盲看 | 使用者看兩支（同風格、順序隨機、不標 A/B），各記 must／should 與「願意發布」的判定 |

---

## 4. 上限、計費與音檔紀律（兩線相同）

- **TTS**：各 ≤35 billed calls（`--max-billed-calls 35` 一律帶）；合成前 `--dry-run` 報量、逐次徵同意；mock 與真音檔不共用目錄；**合成完成後立即把整夾複製到主 checkout 的 `video/output/ch03/s3.2/audio_<線>/`** 並記路徑進 REBUILD_STATUS（PB §2.2 教訓：Phase A 音檔在清 worktree 時遺失）。
- **外部稽核**：各 ≤2 次（Codex 或 agy；A 的六鏡 agy ×3 算 1 次里程碑審），每次逐次報量徵同意，raw 輸出落 scratchpad、裁決轉錄進版控。
- **輪數**：任一線超過 5 輪即停，記錄狀態，不再投入；超過的那條線以「未收線」進 §3。
- **不准**：兩線互讀 worktree；改共用元件；為了省事把對方的產物拿來用（音檔、分鏡、SCRIPT）。

---

## 5. 收線條件與之後

1. **兩線都到 final**（1080p、loudnorm −19 LUFS、成片＋render 紀錄），或任一線觸發 §4 的停止。
2. **交叉審**（§3.3）＋**盲看**。
3. **裁決正式流程**：回到裁決稿的四題逐題填答——每題的答案＝「A 的做法／B 的做法／混合（指明取哪邊的哪一步）」，附 §3 的數字與借用帳；處置清單（裁決稿 §6）同時解凍。
4. 正式流程寫成 SSOT（檔名由裁決定）；§3.3 起每節照它走。

---

## 6. 開工前置（兩線共同；先做完才開 A、B 的 session）

- [ ] **A 線前置＝PB §5 Task 0**（`s32_derive.py`、`remotion_sync_check.py`、`rewatch_pack` 三旗標＋紅測試）。其中 `rewatch_pack` 接 Remotion 是兩線共用的量測器（§3.2 第 3 列）——**做完後 B 也能用，但 B 不必用**。
- [ ] 本機主 checkout 的 `video/remotion/` 有 `node_modules/`（子代理 worktree 各自 `npm ci`）。
- [ ] `.env` 有 `MIMO_API_KEY`；`stable-ts` 在。
- [ ] 兩線的目錄與 composition 名保留（§1.1 第 1 列、§1.2 第 5 條），開工時檢查不存在。
- [ ] §2.3 凍結 hash 已記（`021b78c`）。
- [ ] B 線 session 的啟動提示（§0 B 段）貼進去之前，主對話確認它**沒有**列到 §2.2 的流程文檔。

---

## 7. 邊界（本輪與兩線都不做）

- 本立檔輪不做片、不呼叫任何付費／外部 API。
- 不重開 2026-09-25 已定的視覺方向（紙本編輯排版）與品牌 logo 唯一固定元素的前提。
- 不動 `s31/`、`q7/`、`act3/`；不碰講義線。
- 不並行開 §3.3——兩線收線、正式流程定案後才開。
- 裁決稿的四題與處置清單**延後**到 §5 第 3 條；[`KICKOFF-remotion-process-review.md`](KICKOFF-remotion-process-review.md) §7 的凍結清單延續。

## 8. 相關紀錄

- 檢討輪契約：[`KICKOFF-remotion-process-review.md`](KICKOFF-remotion-process-review.md)；裁決稿：[`_audit/REVIEW-remotion-process-review-2026-09-29.html`](_audit/REVIEW-remotion-process-review-2026-09-29.html)。
- A 線契約：[`KICKOFF-s32-remotion-phaseB.md`](KICKOFF-s32-remotion-phaseB.md)（Phase A 產物＝[`KICKOFF-s32-chain-rule.md`](KICKOFF-s32-chain-rule.md) §4）。
- Manim 封存契約：[`KICKOFF-remotion-unification.md`](KICKOFF-remotion-unification.md)；Manim §3.1 流程檢討：[`KICKOFF-process-reform.md`](KICKOFF-process-reform.md)。

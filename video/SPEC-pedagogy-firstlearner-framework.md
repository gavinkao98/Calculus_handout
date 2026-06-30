# SPEC — First-Learner Pedagogy ＋ On-Screen-Text Faithfulness Framework（video 產線）

> 狀態：設計定案 v3（待 writing-plans 轉施工計畫）。日期：2026-06-30。分支：`video/template-redesign-navy-spine`（commit/branch 待使用者裁決）。
> 來源：使用者對 §3.1（trig derivatives）成片的教學回饋（針對「第一次學微積分的同學」）→ 升級為**可持續複用的框架/流程/模板/規則**，而非單節修補。
> 修訂史：v1 經 Codex（gpt-5.5, xhigh, read-only）對抗式 review；v2 再經 4-agent 對抗式自審（對著真 codebase 查證）後**修正核心機制**——v1 的 §5 前提（scaffold 搬進 .md 即被 NFA/L1/L5 覆蓋）**被證偽**，見 §5、§13。v3 再經 Codex 獨立重攻 v2，採納「場級繼承」等 8 項精修（§13）。

---

## 1 · 背景與動機

§3.1 成片回饋歸納出 **6 條可複用教學原則**，框架目前未強制：

- **P1** 證明/推導粒度：對初學者「一個 beat 只扛一個承重步驟」，不過度壓縮。
- **P2** 動機上畫面：每個 proof/子結論場景在**畫面上**有一句「為什麼做這個」，不只藏旁白。
- **P3** divider 講具體問題：section divider 講出正在解的**問題/式子**，不只是概念標題。
- **P4** 前提首用即標：默默用到的慣例/假設（radians、定義域限制）在**第一次用到**處標出。
- **P5** 圖凸顯：當場景核心**就是**幾何直覺時，圖當主角。
- **P6** 次要文字可讀：reason-rail/註解有最小可讀字級，含手機。

**根因（三產線稽核結論）：框架沒有「audience」概念**，一切校準對象是講義（faithfulness）、證明複雜度、通用密度預設；「第一次學的人」不是被表示的維度。且 **faithfulness 錨定講義**——講義簡略/留白（如 radians 隱含），影片忠實繼承、閘照過。

**自審追加的更大根因（v2）：所有上畫面教學文字都未對核准稿查忠實。** 不只新加的 scaffold——既有的 `statement`、`annotations`、divider `subtitle`、callout `body`、step/result `reason` 等**全部只活在 storyboard `.yml`**，**不被任何忠實閘對著核准 `.md`/講義查**（`lint.py` 只查它們有沒有亂碼 LaTeX）。原因（已驗證）：
- `NFA` 的 source ＝ `<deck>.md` 的 **`narration:` 欄**（`NARRATION-FAITHFULNESS-RUBRIC.md:13`），且只審「narration → HTML/spoken 衍生版」的忠實；intro/divider 等靜音單元 NFA 不審。
- `.md narration:` 與 storyboard `say:`／slide 文字是**兩份各自手寫的 artifact**；`derive_spoken.py` 只做 `say↔spoken` 的 marker/`$`-leak parity，**沒有 `.md→storyboard` 的忠實 derive**。
- `L1`/`L5`（six-lens）審 `.md`、且只在**鎖稿前**跑，其 parser 只吃固定欄位（id/source/learning_goal/kind/narration/visual_need/animation_cue），**不讀 storyboard slide 文字**。

→ 結論：上畫面教學文字目前**前鎖、後鎖都沒有忠實守門**。本框架（依使用者裁決 B）一併補上。

各層覆蓋現況（✅ 有 · 🟡 部分 · ❌ 無）：

| 原則 | 規則(methodology) | 模板 | 閘 |
|---|---|---|---|
| P1 | 🟡 複雜度-only（>4 步拆 statement+proof 單元，非 per-beat） | 🟡 `part:` | 🟡 L2 抓 over-stuffing，不抓 over-compression |
| P2 | ❌ | 🟡 只能 `kicker`+`aside` 湊 | ❌ |
| P3 | 🟡 選填 `tagline`（會 wrap，非硬一行） | 🟡 subtitle 一格 | ❌ |
| P4 | ❌ | (callout 可) | ❌（且 faithfulness 把它藏起來） |
| P5 | 🟡 只有 animate 規則 | ✅ `x_length/y_length` | 🟡 A7 focus，非 prominence |
| P6 | ❌（在工程層） | 🟡 35px、無 floor | 🟡 V4「讀不到」、無 mobile 標尺 |
| **OTF** 上畫面文字忠實 | ❌ | — | ❌（前鎖後鎖皆無） |

---

## 2 · 範圍與分解

本工程天然分兩個子專案，必須**先後**做：

- **SP1（本 spec）= 框架**：規則 + 模板承載 + 新教學閘（PD1–PD4）+ **on-screen-text faithfulness（OTF）機制** + 視覺閘擴充。交付＝閘可跑、規則/模板就位，並在 §3.1 上校準過。
- **SP2 = 回填**：把 SP1 套用到 3 個已完成 deck（ch01 §1.1、ch03 §3.1、§3.2），修 blocking 到過。**注意：選 B 後回填涵蓋所有上畫面教學文字，但經「場級 source 繼承」（§5.1）收斂——常態繼承、只補例外欄位，非逐欄遷移**（§11、§15）。SP2 範圍在 SP1 閘跑過乾跑前無法界定，故 SP1 先行。

**非目標 / YAGNI cuts：**
- 不做可配置的多層 audience 分支系統——只加**一個預設欄位**（§3 D6）。
- 不把語意推斷塞進 schema/lint（「radians 在哪 first-use」「definition_math 有無子結論」皆 → 作者宣告或 gate-1 advisory）。
- 不為 P5/P6 立新 V/A code——sharpen 既有（§8）。
- 不做自動改寫迴圈；不 re-litigate 已認可教學法。

---

## 3 · 決策摘要（使用者已裁決）

- **D1 audience＝預設初學者**：5/6 原則對任何觀眾都是好教學→無條件通用規則；只有 P1 真正 audience-sensitive，預設初學者節奏。
- **D2 強制＝完整自動教學閘**（非僅人工 checklist、非僅結構存在性）。
- **D3 架構＝獨立新教學閘**（自有 rubric + 自有 gate-1 agent），與 six-lens 並列，**界定不重疊切片、重疊處從屬 L-codes**（§10）。P5–P6 改**擴充既有 visual-frame 閘**。
- **D4 回填＝全面**（3 deck 跑＋修到過），走「先乾跑→分類→人核可→範圍化解鎖」（§11）。
- **D5〔v2 修正後的核心〕** 上畫面教學文字的忠實性**不靠 NFA/L1/L5 自動涵蓋**（已證偽）；改由 **OTF 機制**：每段上畫面教學文字帶 provenance ref（沿用既有 `source:` 慣例）+ 新閘自己讀 storyboard 與 `.md`/講義、查其是否被 cited source 支持（§5）。
- **D6〔Codex E，使用者採納〕** 加**預設** `meta.pedagogy_profile: first_time`（可覆寫）。**落地當下零行為改變**——scaffold/provenance 的 blocking 檢查**預設 warn-only**，per-deck 隨 SP2 回填才翻 blocking（§9 修正）。
- **D7〔自審 + 使用者裁決 B〕** OTF 這輪做**通用**：涵蓋 `statement`/`annotations`/`subtitle`/`body`/`reason`/scaffold 全部上畫面教學文字，不只新 scaffold（§5、§9、§10）。

---

## 4 · 架構（三層 + 資料流，v2 修正）

**重要事實修正：** `.md` 與 storyboard **不是**乾淨的 SSOT→derive 關係，而是兩份平行手寫 artifact。`.md narration:` 是「旁白」的核准源（NFA 審其衍生）；storyboard 的 slide 文字（statement/scaffold/annotations…）是**畫面**的源，目前無人對它查忠實。本框架補一條「畫面文字 → 可回溯核准源」的軌。

```
handout（chapter*-print-standalone.html）  ── 數學/內容權威
        │ source ref
content script (.md)  ── narration 核准源（NFA 審其衍生）+ 單元 source/learning_goal
        │ source / locus ref（OTF provenance）
storyboard.yml  ── 畫面文字 SSOT：statement / scaffold(motive·problem·flag) / annotations / …
        │            + meta.pedagogy_profile + assumptions registry
        ▼
schema + lint   ── 確定性：provenance ref 解析 + 結構存在性 + registry 一致性
        ▼  render
 ┌ pedagogy gate-1  讀 storyboard+.md+handout → PD1–PD4（教學品質）+ OF1–OF2（畫面文字忠實）
 └ visual gate-1    讀 frames → A7 prominence / V4·A6 min-size（擴充）
        ▼
findings → 人工處理 / sign-off
```

三層各守本分（沿用 content↔engineering 分界）：規則層（P1–P4 → `CONTENT_METHODOLOGY.md`；P5–P6 → `DESIGN.md`/visual rubric；OTF → `CONTENT_METHODOLOGY.md` + `REVIEW_GATES.md`）、承載層（§6）、強制層（§7–§9）。

---

## 5 · OTF：on-screen-text faithfulness〔v2 核心，取代 v1 §5〕

**問題（已驗證）：** 上畫面教學文字只活在 storyboard、前鎖後鎖都無忠實守門；v1 想「把它搬進 .md 讓 NFA 自動審」**不成立**（NFA 只審 `.md narration:` 欄、且不審 storyboard 文字）。

**解（D5+D7）：**
1. **provenance（場級繼承，欄級覆寫——Codex B 收斂）：** scene 本就有場級 `source:`；**所有上畫面文字欄位預設繼承場級 source**，無需逐欄補 ref。**只有當某欄位 (a) 引用與場級不同的源、(b) 跨單元綜合、或 (c) 提出高風險數學斷言時，才必須帶欄級 `source:`/`from:` 覆寫**。ref 指向核准 `.md` 單元 id 或 handout anchor（沿用既有 `source:` 慣例）。→ 讓 D7 通用化在 SP2 可行（常態無逐欄遷移，只補例外）。
2. **確定性層（schema/lint）：** 該 ref **解析得到**（指到存在的 .md 單元/locus）。不做文字語意比對（避免模糊匹配）。
3. **判斷層（新 gate-1 的 OF 維度）：** 新閘**同時讀** storyboard 文字與其 cited source，判其是否被支持——
   - **OF1 忠實（blocking）：** 上畫面文字**矛盾或超出** cited source（加了 source 沒有的數學/結論、改了條件）。
   - **OF2 可回溯（blocking，結構）：** 缺 provenance ref（→ 下推 schema/lint，見 §9）。
   - 這是「對的相位（隨閘跑、含後鎖）、對的 artifact（讀真正上畫面的文字＋源）」的守門，**不再假裝 NFA 涵蓋**。
4. **與既有 faithfulness 的邊界（§10）：** L1 仍審 `.md` 內容 vs 講義；NFA 仍審 narration 衍生；**OF 只新管「storyboard 上畫面文字 vs 核准源」這條既有未守的軌**，不與 L1/NFA 重疊。
5. **L1 scaffold 例外**（寫進 `CONTENT-SIXLENS-RUBRIC.md`，置於 L1 既有「呈現的重排與增補不算 finding」carve-out 旁）：標記為 scaffold 的短文字若只把「已用到的目的/記號/慣例/定義域/前提」講白，不算 L1「加入講義沒有的數學」；但須 cite locus、不得引入新定理/例題/結果、不得改條件。
6. **生命週期閘（Codex G）：** OF 只在 cited content script `CONTENT_APPROVED=yes`（已 lock）時 **gating**；DRAFT 階段（源未定）一律 **dry-run**——否則是拿未核准的源當忠實基準。
7. **scope 邊界（Codex G）：** OF 讀 storyboard YAML——**hook 自繪、未宣告於 YAML 的教學文字 OF 看不到**；重要的 hook 教學文字須宣告進 YAML payload（帶 provenance），否則歸 hook-engineering `E1` ＋ 視覺閘（§10）。

---

## 6 · 承載設計〔Codex D — 收斂，不疊床架屋〕

不要三個欄位各自為政（與既有 `kicker`/`aside`/`statement`/`subtitle` 疊床）。改：

**(a) 共用 scaffold 渲染。** 一個 shared helper（掛 Lectern，`_common.py`）渲染：
- content 場（`definition_math`/`theorem_proof`/`derivation`）：`scaffold.motive` → 標題下一行**較小的 `text` role**「為什麼」（**不可 `muted`**——違反 DESIGN.md「教學內容用 text/primary 非 muted」且觸發 sizecheck muted-prose 警告；de-emphasis 靠字級/位置，非調暗。Codex E）。
- `divider`：`scaffold.problem` → 標題下一個公式塊（比現有會 wrap 的 `subtitle` 更強的 formula-block 處理）。
- 首用場：`scaffold.flag: <assumption_id>` → 小 badge/aside。
- 每個 scaffold 帶 `source:`/`from:` provenance ref（§5）。

**(b) assumptions registry（deck-level，讓「首用才標」可確定性檢查）。**
```yaml
assumptions:
  - id: radians
    text: "$\\theta$ in radians (arc length $=\\theta$)"
    first_use_unit: sector_inequality
    source: "chapter3-print-standalone.html §3.1 · radians 預告句"
```
規則：每筆 assumption 必須在 `first_use_unit` 渲出 `scaffold.flag: <id>`；「是否用到/何處首用」由作者**顯式宣告**，閘不推斷。

**(c) `meta.pedagogy_profile`（D6）。**
```yaml
meta:
  pedagogy_profile: first_time   # 預設；可覆寫 e.g. prepared / proof_heavy
```
PD1 拆步粒度與 PD2 motive 要求讀此值；SP1 只定義 `first_time` 行為，覆寫語義留 YAGNI 日後。

**(d) 圖凸顯（P5）不靠 magic boolean。** 維持 `x_length/y_length` 放大圖；凸顯由閘**量測**（圖佔幀比例），不引入 `figure_focus: true`。

---

## 7 · 新閘 `PEDAGOGY-FIRSTLEARNER`（兩個維度家族）〔D3；Codex A+C+F；v2 加 OF〕

**形態**：mirror 既有 audit 閘——新 SSOT `content_scripts/_audit/PEDAGOGY-FIRSTLEARNER-RUBRIC.md` + 新 gate-1 Claude subagent（`pedagogy-firstlearner-audit`，read-only，唯回報、絕不改檔；**讀 storyboard＋.md＋handout**）。gate-2 暫不立。與 six-lens 並列、不越界（§10）。

該 agent 一次讀齊 storyboard+源，承載**兩個清楚分開的維度家族**（共用輸入、分開回報）：

**(i) PD1–PD4 — 教學品質（結構 blocking、品質 advisory，Codex F）**

| code | blocking（可觀察、需 cite 證據） | advisory | 邊界（§10） |
|---|---|---|---|
| **PD1** beat 粒度 | 單一 beat/reveal 壓了 >1 個承重的代數/邏輯動作 | 對 `first_time` 可更分段 | 讓 `L2`（unit 兩**概念**）；PD1 管一 **beat** 多**動作**；單一概念單元內部 reveal 過度壓縮歸 PD1 |
| **PD2** 動機 | proof/derivation 場缺 `scaffold.motive`（→ schema/lint，僅 theorem_proof/derivation 確定性必填） | motive 弱；definition_math 是否該有 motive | 內容忠實歸 OF1/L1；definition_math 必填與否＝advisory（語意） |
| **PD3** divider | section divider 缺 `scaffold.problem`（→ schema/lint） | problem 模糊/非具體式 | 只在 `kind: divider` 場觸發；intro（`kind: intro`）、recap（`kind: content`/recap_cards）依 kind/template 模型本就排除（§10 L6） |
| **PD4** 前提 | registry 宣告的 assumption 在其 `first_use_unit` 未渲 flag（→ schema/lint 一致性） | flag 措辭/位置 | 用到與否由作者 registry 宣告 |

**(ii) OF1–OF2 — 上畫面文字忠實（§5）**：OF1 文字矛盾/超出 cited source ＝ blocking；OF2 缺 provenance ref ＝ blocking（→ schema/lint）。

**硬紀律（寫進 rubric 頭，防 seed_converge 的「主觀不收斂＋drift」）：**
- blocking 只給**可觀察遺漏 / 具體被跳過的步驟 / 缺必填欄位 / 與源矛盾**；「可以更有動機/更慢/更清楚」一律 advisory。
- 每條 blocking 必須 cite：unit id ＋ 確切 beat/欄位 ＋ 缺的步驟或矛盾點 ＋ 一個最小修法。
- **禁止**自動改寫迴圈；**禁止** re-litigate 已認可教學法。
- **分開計數（Codex D）：** rubric 必須分別輸出 `PD blocking` 與 `OF blocking` 摘要，不混在一起——免得主觀教學 finding 蓋掉硬忠實失敗。
- **生命週期：** OF gating 僅當 cited `.md` 單元 `CONTENT_APPROVED=yes`；DRAFT 期 dry-run（§5.6）。
- 收斂＝PD/OF blocking == 0（per-deck opt-in 後的目標，見 §9 兩軸澄清）。

---

## 8 · 視覺閘擴充〔P5/P6；Codex C — sharpen 既有、不立新 code〕

改 `VISUAL-FRAME-RUBRIC.md`：
- **P5 → `A7`（hierarchy/focus）加 figure-prominence 子準則**：核心是幾何直覺的場（hook/graph），圖應主導；由**量測**圖佔幀比例判定，低於門檻扣 A7（advisory magnitude），不立新 code。
- **P6 → `V4`/`A6` 加數值最小字級 floor ＋ mobile 標尺**：reason-rail/註解低於 floor → V4 升 blocking 或 A6 扣分；補一條「以手機寬度檢核次要文字」。
- 工程面：`theme.py`/`sizecheck.py` 加最小字級 **floor 常數**，封住單行 `scale_to_fit_width` 縮到 floor 以下。

---

## 9 · 確定性層（schema/lint 增訂）〔Codex H + 自審修正：只查一致性、不推斷、預設 warn〕

`schema.py` / `lint.py` 新增。**啟用模型（解 §3/§6 vs blocking 矛盾）：所有新檢查預設 `warn-only`；per-deck 加一個 opt-in flag（隨 SP2 回填完成翻 `blocking`）→ 落地當下對既有 deck 零行為改變。**

> **兩軸澄清（severity class vs gating）：** 「blocking」是 finding 的**嚴重度類別**，不等於「會擋稿」。落地當下，未回填 deck 上的**所有**新發現——確定性層**與** gate-1 的 PD/OF blocking——一律以 **warn/dry-run** 呈現、不 gating（OF1 另有自然護欄：未補 provenance 的 deck，OF1 無 cited source 可比，對空集合觸發）。per-deck 經 SP2 opt-in 後才成 gating。§7/§14 的「收斂＝PD/OF blocking == 0」是**opt-in 後**的收斂目標，非落地門檻。

1. **OF2 provenance（場級繼承，D7）：** 每個 scene 有可解析的場級 `source:`；上畫面文字欄位**預設繼承**，**只驗欄級覆寫 ref**（若有）。**確定性解析只認兩條路徑：** (a) ref 指向存在的 `.md` 單元 id（該單元再由 L1 對講義把關，鏈條閉合）；(b) ref 指向 handout 既有的 section/figure anchor（`id="frag-sec-*"`／`data-fig="*"`）。handout 自由描述尾巴（如「Proposition 3.1 (statement)」「opening prose」）**無穩定 anchor、不做確定性解析**（會需語意比對，§9 禁）→ 該層只驗 anchor，描述尾巴的忠實歸 OF1 gate-1。
2. **PD2/PD3 結構存在性：** theorem_proof/derivation 場有 `scaffold.motive`；`kind: divider` 場有 `scaffold.problem`（intro/recap 依 kind/template 本就排除，非靠此 qualifier）。**definition_math 不入確定性必填集**（「有無子結論」是語意，違反無推斷原則）→ 改 PD2 gate-1 advisory。
3. **PD4 registry 一致性：** 每筆 assumption 有 `id/text/first_use_unit/source`；`first_use_unit` 存在；該 unit 渲出 `scaffold.flag: <id>`；無孤兒 flag。
4. **新增能力（§12 必含）：** 上述 1 的 ref 解析需 schema/lint **能載入 `.md`/handout locus 表**（現 `lint.py`/`schema.py` 只讀 storyboard YAML）——這是新工具能力，非現有。文字 vs 源的**語意**比對不入確定性層（歸 OF1 gate-1）。
5. **向後相容護欄（Codex C）：** provenance/scaffold **不得改變既有 scalar 欄位形狀**（`statement` 仍 string、`proof[]` 仍 list、`callout.body` 仍 string…）——走 sibling 結構（場級 `source:` ＋ 選用 `source_map:`）或共用 `text_of()` adapter 同吃 string/object；**缺 `scaffold` 一律 no-op**（render 不變）。否則 opt-in 前輸出就變，破「零行為改變」。

---

## 10 · 邊界與不重疊〔Codex A+C + 自審補 L6/OF〕

新閘**獨立但從屬於既有 owner**；永不 raise 下表既有擁有者已擁有的 finding：

| 議題 | 既有擁有者 | 新閘不重疊切片 |
|---|---|---|
| 一個 unit 兩個教學**概念** | six-lens `L2` | — |
| 一個 **beat** 多個承重**動作**（含單一概念單元內部過度壓縮） | — | **PD1** |
| **intro tagline / recap takeaway** 存在性與定位 | `L6` | — |
| 個別 **content/divider** 場的 on-screen motive·problem（PD2 限 theorem_proof/derivation；PD3 限 `kind: divider`；intro/recap 已由 kind 排除） | — | **PD2/PD3** |
| `.md` 內容忠實講義 | `L1`（含 scaffold 例外 §5.5） | — |
| narration → HTML/spoken 衍生忠實 | `NFA` | — |
| **storyboard 上畫面文字 vs 核准源** | —（既有未守） | **OF1/OF2** |
| scaffold/statement 數學正確 | `L5`（.md 內） | OF1 只查「是否被源支持」，不重算正確性 |
| 圖可讀（窗格/爆框） | `V3` | — |
| 圖**凸顯**夠不夠 | — | `A7` 子準則 |
| 文字讀不到 | `V4`/`A6` | min-size floor |
| **render 後**畫面像素/hook 輸出/timing vs beat | `V6`/`V8`（visual-frame） | OF 只查**撰寫期** storyboard 文字的 provenance/忠實，不碰 render 後像素（Codex F） |
| hook 自繪、未宣告於 YAML 的教學文字 | hook-engineering `E1` ＋ 視覺閘 | OF 讀 YAML 看不到；重要 hook 文字須宣告進 YAML payload（§5.7，Codex G） |

> PD1 vs L2 tie-breaker：**L2 ＝ 跨單元的概念計數**（unit 層，含 silent-drop/兩概念同框）；**PD1 ＝ 單一 beat 內的動作計數**（unit 拆對了、但一個 reveal 仍壓多步）。

---

## 11 · 回填流程（SP2 骨架）〔Codex G + 自審：含 OTF provenance 回填〕

§3.1 是回饋來源（最壞案例），單校它會 overfit。SP2 流程：
1. 對 3 deck 跑新閘 **read-only 乾跑**（不解鎖、不改檔）。
2. findings 分類：**migration-required（真 blocking）** vs **advisory**。**注意（選 B 成本，經 Codex B 場級繼承收斂）：** scene 本就有場級 `source:`，OTF **預設繼承**，故回填**不是逐欄補 ref**——只在「欄位引用不同源／跨單元綜合／高風險斷言」處補欄級覆寫。量比 v2 初稿小很多，但仍須在遷移清單估清。
3. **使用者核可遷移清單**（哪些 deck、哪些單元/欄位要動）。
4. 只對真 blocker：scoped 解鎖 → 補 provenance/scaffold（含 OF1 忠實修）→ 重跑該單元 L1/L5 + NFA 回歸 + PD/OF → 重渲 → 重新 sign-off。
5. 出 HTML 報告（比照既有 `REVIEW-*-applied.html`）。

> post-lock 改 beat 須 scoped NFA + 視情況 re-derive/TTS（既有規則）。計費步驟各自 consent-gated。

---

## 12 · 變更落點清單（給 writing-plans）

**新增：**
- `content_scripts/_audit/PEDAGOGY-FIRSTLEARNER-RUBRIC.md`（PD1–PD4 + OF1–OF2 SSOT）。
- `pedagogy-firstlearner-audit` gate-1 subagent 定義（讀 storyboard+.md+handout）。
- `_common.py` 共用 `render_scaffold` helper。
- schema/lint 的 **.md/handout locus 載入＋ref 解析**能力（§9.4，新）。

**修改：**
- `CONTENT_METHODOLOGY.md`：P1（>4 步 statement/proof 拆分 → 收緊為「一 beat 一承重動作」、讀 profile）、P2、P4 規則；OTF provenance 規則；§5 邊界。
- `DESIGN.md`：scaffold 承載、divider `problem`、P5/P6 視覺規則、authoring checklist。
- `CONTENT-SIXLENS-RUBRIC.md`：L1 scaffold 例外（§5.5，置於既有 carve-out 旁）。
- `VISUAL-FRAME-RUBRIC.md`：A7 prominence、V4/A6 min-size + mobile（§8）。
- `REVIEW_GATES.md`：新增 pedagogy 閘進閘序；**順手修既有 stale doc：V1–V8→V1–V9**（與新閘無關的清理；`REVIEW_GATES.md` line 65/66 **與 `DESIGN.md` ~621/636** 皆有，Codex F）。
- `schema.py`/`lint.py`：§9 的 provenance/存在性/registry 檢查 + .md 載入能力 + warn/blocking opt-in flag。
- `theme.py`/`sizecheck.py`：min-size floor 常數 + 封 single-line shrink。
- 模板 `divider.py`/`theorem_proof.py`/`derivation.py`/`definition_math.py`：接 `scaffold` 引用 + 共用 helper。
- storyboard schema：`meta.pedagogy_profile`、`scaffold.*`（含 `source`）、`assumptions[]`、各上畫面文字欄位的 `source`/`from`。
- **writing-plans #1 必先定（Codex E ＋ v3 收尾）：** **provenance ref 文法 ＋ 欄位涵蓋矩陣**——嚴格 ref 語法、source-root 推斷、unit-id 抽取、繼承規則、handout-anchor vs .md-unit-id 路徑、以及「哪些欄位算上畫面教學文字」（title/prompt/graph label/table cell/recap point/hook 各算不算）。**Codex v3 SHIP 附帶、須一併在此定：**
  - (a) **非 content 場**（intro/4 divider/outro，現無 scene `source:`、但 divider 帶 `subtitle` 文字）是**豁免**還是**遷移**為可審 `source`/`scaffold.problem`；
  - (b) **source-adequacy 護欄**——防「過寬的繼承 source」讓漏掉的欄級覆寫蒙混（例 recap 的整節綜合 source 可能「支持」文字卻藏住缺的 override）：定「何時必須欄級覆寫」＋ OF1 如何判 source 夠不夠 specific；
  - (c) **legacy freeform source**（如 `SS3.1 . opening prose`）→ 穩定 anchor（如 `frag-sec-3-1`）的對映/遷移；
  - (d) `CONTENT_APPROVED` 現為 deck-level 字串（非 per-unit）：定「`.md` unit ref 繼承 deck 核准；handout-anchor ref 一旦解析即可 gate」。
  SP1 施工前先定。
- **writing-plans 待落字交付物：** `CONTENT-SIXLENS-RUBRIC.md` 的 L1 scaffold 例外**精確措辭**（§5.5）；schema/lint `text_of()` adapter ＋ no-op-absent-scaffold ＋ warn-until-opt-in 行為（§9.5）。

---

## 13 · Review 採納紀錄

**Codex（v1）：** 採納 B（忠實性，→ v2 §5）、C（邊界 §10、P5/P6 sharpen §8）、D（scaffold 收斂+registry §6）、F（結構 blocking/品質 advisory §7）、G（乾跑優先 §11）、H（doc drift、無推斷 §9）、E（pedagogy_profile，使用者採納 D6）；修正 A（維持獨立閘＋§10 不重疊邊界）。

**4-agent 對抗式自審（v2）：**
- 🔴 **核心修正證偽（faithfulness-fix-soundness）：** NFA 只審 `.md narration:`、`.md`↔storyboard 無忠實 derive、L1/L5 前鎖且不讀 slide 文字 → v1 §5「搬進 .md 自動覆蓋」不成立 → 重設計為 **OTF**（§5）。並採其「整類未審」發現（statement/annotations… 也漏）→ 使用者裁決 B → 通用化（D7）。
- 🔴 **§10 漏 L6**（PD2/PD3 與 intro tagline/recap takeaway double-report）→ 補 L6 列（§10）。
- 🔴 **§3「零行為改變」vs §9 required-blocking 矛盾** → 改 warn-default + per-deck opt-in（§9）。
- 🔴 **§9「含子結論 definition_math」是語意非結構** → definition_math 出確定性必填集、改 advisory（§9.2）。
- 🟡 §9.4 SSOT 檢查需 .md 載入能力（現工具無）→ 列入 §12。PD1/L2 tie-breaker（§10）。§5 placeholder → §12 待落字交付物。

**Codex（v2，獨立重攻 v2 spec）：** 判 v2 方向 SOUND、OF1 與 L1/NFA 確不重疊（別折進 NFA）。採納其精修：**場級繼承**（§5.1/§9.1/§11，把 B 變 tractable）、**生命週期 `CONTENT_APPROVED` gating**（§5.6）、**scalar 向後相容/`text_of()`**（§9.5）、**`muted`→`text` role**（§6a）、**PD/OF 分開計數**（§7）、**V6/V8＋hook 邊界**（§10、§5.7）、**provenance 文法為 writing-plans #1**（§12）、`DESIGN.md` doc-drift（§12）。

**Codex（v3，收尾驗收 v3 spec）：判決 SHIP——無 spec 級 must-fix。** 確認 v2 各項已 substantively 落實、codebase 支撐前提、無新矛盾、scalar-compat/text-role/V6·V8·hook 邊界皆 sound。4 項收尾要求**全歸 writing-plans #1**（已併入 §12）：非 content 場豁免/遷移、source-adequacy 護欄、legacy freeform source 對映、`CONTENT_APPROVED` deck→unit 繼承。

---

## 14 · 成功標準 / 驗證

- SP1 完成＝：新閘可在 §3.1 跑出可讀 PD/OF findings；schema/lint 新檢查（warn 模式）綠/紅正確；共用 helper 渲染 motive/problem/flag 正常（mock render 目視）；六鏡/視覺閘回歸無新 blocking；`tools/doctor.py` 不受影響。
- **校準**：先在 §3.1 跑新閘，人工核 PD/OF findings 假陽性率、調 rubric，再進 SP2。
- **收斂**：PD/OF blocking == 0；A7/V4 視覺 blocking == 0。
- 全程離線可驗（mock render + 本地工具）；計費步驟另徵同意。

## 15 · 風險與緩解

- **主觀閘不收斂**（seed_converge 教訓）→ §7 硬紀律。
- **OTF 把假前提帶進設計**（v1 已踩）→ v2 §5 已改為讀真 artifact 的 OF 維度；**回歸再審**確認新機制成立。
- **選 B 的回填成本**（所有既有上畫面文字補 provenance）→ §11 step 2 估清、人核可、warn-default 緩衝落地衝擊。
- **PD vs L2/L6 double-report** → §10 不重疊切片。
- **provenance ref 退化成形式**（隨便指一個 source 過 OF2 卻 OF1 不實）→ OF1 gate-1 讀真源判支持，非只查 ref 存在。
- **scalar 欄位被 provenance 包成 object → opt-in 前 render 就變** → §9.5 護欄（不改形狀、`text_of()`、no-op-absent）。
- **citing 未 lock 的 `.md` 源** → §5.6 OF 僅 `CONTENT_APPROVED=yes` 才 gating。
- **hook 自繪文字逃過 OTF** → §5.7／§10 歸工程/視覺閘，重要者須宣告進 YAML。
- **profile 覆寫語義未定** → SP1 只定義 `first_time`；其餘 YAGNI 留日後。

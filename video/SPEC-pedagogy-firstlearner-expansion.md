# SPEC — First-Learner **Expansion** Layer（step-coverage ＋ prose-amplification；video 產線）

> 狀態：設計草案 v1（brainstorming → 待 Codex 對抗式 review 收斂 → writing-plans）。日期：2026-07-01。分支：`video/template-redesign-navy-spine`。
> 來源：使用者對 §3.1 成片 `derivative_of_sine`（Theorem 3.1）投影片的教學回饋——**講義推導很詳細，但影片流程把它壓成 2 行 + qed，初學者看不懂**。經實測（`pedagogy-firstlearner-audit` 對該場跑出 **0 PD blocking, 0 OF blocking**）確認：既有框架只守「別超出源」（over-claiming），對「漏掉源的步驟」（under-showing）**結構性盲**，且「不 re-litigate 已認可教學法」反而保護過簡版本。
> 關係：本 spec **擴充**（不取代）[`SPEC-pedagogy-firstlearner-framework.md`](SPEC-pedagogy-firstlearner-framework.md)（v3, SHIP）。沿用其 provenance 文法（`ref:`/`refs:`）、warn-default＋per-deck opt-in、scalar 向後相容、確定性/gate-1 分工、§10 邊界紀律。
> Review：本草案將經 Codex（gpt-5.5, xhigh, read-only）對抗式 review；使用者已授權「Codex 覆核到收斂即直接施工，過程不另徵詢」（2026-07-01），計費 API／裝新套件／不可逆對外動作除外。

---

## 1 · 背景與動機

**病根（統一診斷）：整條 pipeline 天然在「壓縮講義」。** 螢幕文字要精簡、beat 要少、能 cash-in 就不重講——這對「做漂亮影片」是對的；但**初學者要的相反**：更多承重步驟、更多鋪陳、必要的重述。框架兩根支柱——**faithfulness**（守「別超出源」）與 **visual polish**——都把內容往更簡潔推，**沒有任何一股力量往「為初學者展開」推**。

本 spec 補這股缺的力量，分**兩種失效、兩種機制**（見 §2）。凡此皆**非新增內容**：要展開的細節**講義本來就有**，是流程把它弄丟了或沒 surface。

**實證錨（`derivative_of_sine`）：**
- storyboard `proof:`（[`ch03_trig_derivatives.yml`](storyboards/ch03_trig_derivatives.yml:400)）＝ `d/dx sin x = lim cos(x+h/2)·sin(h/2)/(h/2)` → 兩因子 → `cos x`。
- 但 cited `.md` `visual_need`（[`ch03_trig_derivatives.md`](content_scripts/ch03_trig_derivatives.md:396)）**明列 4 行**，第 1 行是定義行 `d/dx sin x = lim (sin(x+h)−sin x)/h`。
- handout（[`sec-3-1.html`](../handout/html/fragments/ch03/sec-3-1.html:181)）也顯示該定義行。
- → **storyboard 在最後一跳 `.md`→yml 掉了定義橋接行**；且它 cash-in 了 ~10 場前 `difference_quotient_for_sine` 的代數而**畫面無 recap**（線性影片翻不回去 → product form 像憑空出現）。

---

## 2 · 範圍與分解

兩種失效、兩種機制，一份 spec、分開落地：

- **M1 — 推導覆蓋（derivation coverage）＝擋稿閘。** 客觀失效：storyboard 漏掉源列的承重步驟。錨＝作者寫下的 **screen contract**（承重步驟清單）。
- **M2 — 敘述放大（prose amplification）＝唯讀機會稽核。** 半客觀失效：講義有承重 `expansion:intuition` 等直覺，影片沒 surface。錨＝講義既有 `expansion:*` 標記（權威定義見 [`README.md`](../README.md) §撰稿工作流程）。是講義線「薄度剖析／承重直覺」（[`CONTENT_DIRECTION.md`](../CONTENT_DIRECTION.md:112)）的影片側對應，比照 `mode-c-gapwalk` 的 propose-not-act。

**非目標 / YAGNI cuts：**
- **不做 generate**（不從 contract 自動生成 storyboard proof 行）——會打死「適度合併／重排」的自由（§3 D3）。M1 走 **check**。
- **不強制與講義 1:1**——影片可合併／重排步驟（§3 D2）。
- **不把「敘述夠不夠豐富」做成擋稿閘**——主觀、不收斂（seed_converge 教訓）；M2 一律 advisory/propose。
- **不強制例題**——`expansion:example` 不入強制集，例題仍由作者「挑經典幾個」（§3 D4）。
- **不自動改寫**；**不 re-litigate 已認可教學法**。

---

## 3 · 決策摘要（brainstorming 已與使用者裁決）

- **D1 目標＝一層「為初學者展開」**，同時涵蓋推導（M1）與敘述（M2）。校準總線：**economical 但 comprehensible**——精簡、例題挑經典幾個，但不可壓到初學者接不上。
- **D2〔核心校準〕合併可、掉不可。** contract 是「承重步驟清單」（非講義照抄）；storyboard **可自由合併／重排／換佈局**，**只有『某承重步驟沒被任何 reveal 蓋到』才擋稿**。
- **D3〔由 D2 導出〕M1 走 check，不走 generate。** generate 會硬生成「一步一行」、打死合併自由；check（宣告 `covers:` + 驗覆蓋）才容得下合併。contract 同時是日後若需 generate 的地基。
- **D4 例題永不強制**、correctness-critical caution（如 radians）**升級為必填假設**（PD4/來源契約），不埋進 advisory。
- **D5〔Codex R1 核心〕contract 是 authored（不 parse freeform `visual_need`）。** 已驗證 `visual_need` 是散文、且 parser [`review_pack.py`](pipeline/review_pack.py:107) `_commit()` 把 list 值 `" ".join` 壓平、抹掉行結構 → 拿它當確定性錨會重演不收斂。故必須有**顯式結構化的必填步驟宣告**。
- **D6 M2「surfaced」定義放寬（Codex R1）：** on-screen／narration／visual／explicit-adapt 皆算 surfaced；回報 `missing`／`narration-only`／`visual-only`／`screened` 四態，**只有真的 `missing` 的承重直覺**才成提議。防過度觸發。
- **D7 全走新 code、不塞 PD1/OF1/NFA（Codex R1）。** M1 → 新 **SC** 家族（併入 pedagogy-firstlearner 閘）；M2 → 新 opportunity-audit agent。

---

## 4 · M1 架構 — 推導覆蓋（SC 家族）

### 4.1 承載：`.md` screen contract ＋ storyboard `covers:`

**（a）`.md` 單元新增結構化 `screen_contract`（content SSOT 側；Codex D5）。** 例：
```yaml
screen_contract:
  required_steps:
    - id: def
      tex: "\\frac{d}{dx}\\sin x=\\lim_{h\\to0}\\frac{\\sin(x+h)-\\sin x}{h}"
      reason: "定義"
    - id: reduced
      tex: "=\\lim_{h\\to0}\\cos(x+\\tfrac h2)\\frac{\\sin(h/2)}{h/2}"
      reason: "前面化簡"
      depends_on: difference_quotient_for_sine.result   # 這步在別場推出
      recap_required: true                               # 引用它的場景須畫面重述
```
- `required_steps` ＝ **承重步驟清單**（作者對本單元宣告的「畫面不可少」動作，細顆粒）。這份清單就是 D1 的「不可太精簡」底線。
- `depends_on` + `recap_required` ＝ 顯式標註跨場依賴（**閘永不推斷**，同 PD4 assumptions 精神）。
- 放在 `.md`（非 storyboard）＝ 讓 contract 對 storyboard **獨立**：storyboard 不能「同時少宣告又少畫」而無人察覺；且該 contract 是否忠實於 handout 由既有 `L1` 把關（§8 邊界）。

**（b）storyboard 場景宣告 `covers:`（presentation 側）。** 用**場級 `covers:` 清單**（sibling 欄位，不改 `proof:`/`steps:` 的 scalar/row 形狀 → 守框架 §9.5 向後相容）。**`covers:` 只能列本場所 `ref:` 單元 `required_steps` 的 id——跨單元的依賴走 `depends_on`，不進 `covers:`（Codex R2）：**
```yaml
- id: derivative_of_sine
  ref: md:derivative_of_sine
  covers: [def, reduced]     # 本場（連同其他 ref 同單元的場）須聯集蓋滿 required_steps
  proof: [ ... ]             # 形狀不變；一個 reveal 可同時承載多個 covered id（＝合併）
```

### 4.2 SC codes（新家族，併入 [`PEDAGOGY-FIRSTLEARNER-RUBRIC.md`](content_scripts/_audit/PEDAGOGY-FIRSTLEARNER-RUBRIC.md)）

| code | 型別 | blocking 條件 | 邊界 |
|---|---|---|---|
| **SC1** 步驟覆蓋 | **確定性**（`step_coverage.py`） | 某 `.md` 單元的**須顯示** `required_steps` id（＝除「有 `depends_on` 且無 `recap_required`」的純回指步驟外）未被「所有 `ref:` 該單元的場景之 `covers:` 聯集」蓋到 → 漏步驟 | 見 §8：非 PD1（PD1＝一 beat 多動作）、非 OF1（OF1＝超出源；SC1＝源的子集） |
| **SC2** cash-in recap | **確定性**（`step_coverage.py`） | 帶 `depends_on`＋`recap_required: true` 的回指步驟（在別場推出）未被**本單元場景**在地覆蓋 → cash-in 缺在地 recap（SC1 的回指子集，另給訊息以利辨識） | 只在 `depends_on`+`recap_required` 標註時觸發；閘不推斷跨場依賴 |
| **SC-adv** 疑似過度合併 | **gate-1 agent 判斷（advisory）** | 不 blocking：拿 `required_steps`／`covers` 對 **handout** 承重步驟比，疑似「併過頭、少了承重動作，初學者恐失去脈絡」→ 建議加 `required_step` | 最終校準是作者的；與 `L1`（`.md` 內容忠實）不同切片：SC-adv 問「screen contract 對初學者夠不夠」，非「`.md` 忠不忠於講義」 |
| **SC-honesty** 覆蓋誠實性 | **gate-1 agent 判斷（evidence-based；opt-in 前必跑，Codex R2）** | 某場 `covers:` 宣告某 id、但其上畫面 payload 語義上**沒有**該步驟 → blocking。**每條 finding 必 cite 確切可見欄位／reveal target（`statement`／`proof.0`／`proof.1`／`qed`…），非泛稱。** 防 `covers:` 變橡皮圖章 | 不重算數學正確（`L5`）；**這是把「convention 當 contract」補實的關鍵——`coverage_enforce` sign-off 前 SC-honesty 不可略過** |

- **確定性 vs 判斷分工（沿用框架）：** SC1/SC2 由新模組 [`pipeline/step_coverage.py`](pipeline/step_coverage.py) 確定性計算；gate-1 agent **只浮現**它們、並自有 SC-adv/SC-honesty 判斷層。
- **warn-default／opt-in：** SC1/SC2 預設 `warn`；per-deck `meta.coverage_enforce: true` 才翻 `error`（比照 `otf_enforce`/`pedagogy_enforce`）。落地零行為改變（無 `screen_contract` 的單元＝no-op）。**但非永遠 no-op（Codex R2/R3）：** `coverage_enforce: true` 時，該 deck 範圍內的 proof/derivation 單元**須有 `screen_contract`**——帶 `required_steps`（受檢）**或** `coverage_exempt: true`（顯式豁免）；**兩者皆無即 `error`**（強迫作者顯式決定，否則 opt-in 形同虛設）。
- **生命週期：** 同 OF——`md:` 契約在 deck `CONTENT_APPROVED=yes` 才 gating；DRAFT 期 dry-run。

### 4.3 確定性演算法（`step_coverage.py`，unit 級）
對每個帶 `screen_contract` 的 `.md` 單元 `U`：
1. 收集所有 `ref: md:U` 的 storyboard 場景（`covers:` 只列本場 `ref` 單元的 id，故按**場級 `ref`** 分組即可；跨單元依賴走 `depends_on`、不進 `covers`），取其 `covers:` 聯集 `C`。
2. **判「須顯示」集：** `required_steps` 中，除「有 `depends_on` 且無 `recap_required`」的純回指步驟（指向別場的引用、不強制在地重畫）外，其餘皆須在地顯示。
3. **SC1：** 「須顯示」集每個 `id` ∈ `C`？缺者逐一 `error/warn`，訊息帶該 step 的 `tex`（修法＝把這步放上某場畫面並加進 `covers:`）。
4. **SC2：** 「須顯示」集中帶 `recap_required` 者（＝被要求在地重述的 cash-in 結果）若未 ∈ `C`，另以「cash-in 缺在地 recap」訊息報（實作上是 SC1 的子情形，分訊息以利作者辨識）。
5. 孤兒防呆：`covers:` 出現 `required_steps` 沒有的 id → warn（打錯字/漂移）。

---

## 5 · M2 架構 — 敘述放大（AMP，opportunity-audit）

**形態：新唯讀 agent `video-amplification-audit`**（mirror `mode-c-gapwalk`：propose-not-act，只提候選、絕不改檔），配輕量 advisory rubric `content_scripts/_audit/AMPLIFICATION-RUBRIC.md`。**不併入 faithfulness 閘**——它是 propose 模式、且主要讀 handout 標記，性質不同。

**輸入：** 某節的 storyboard `.yml` ＋ cited `.md` ＋ handout fragment。
**流程：**
1. 列出該節 handout 的 `expansion:intuition` / `expansion:application`（**correctness-critical `expansion:caution` 不在此——升級假設，§7/§8**）標記及其承載的直覺。
2. 對每個標記判 surfaced 四態（Codex D6）：`screened`（上畫面文字承載）／`narration-only`（旁白承載）／`visual-only`（圖/動畫承載）／`missing`（全都沒有）。
3. **只有 `missing` 的承重直覺**成為**提議**：補一句敘述/一個 beat，綁 `doc:frag-sec-*` provenance（＋標記短引文，因 anchor 是節級非標記級），供使用者裁決。`narration-only`/`visual-only` 僅資訊性列出、**不計入 AMP1 提議**（若判斷顯然該落畫面，可另附非提議的 `[consider-screen]` 註記，不算候選、不計數——Codex R6 去矛盾）。
4. 產 standalone HTML 裁決稿（比照 CLAUDE.md 交付規則、`mode-c-gapwalk`）。

**AMP1（唯一 code，advisory）：** 該節某承重 `expansion:intuition`/`application` 判為 `missing` → 提議候選。永不 blocking。

---

## 6 · 校準線（economical 但 comprehensible）

| 檔位 | 內容 | 機制 |
|---|---|---|
| **強制（blocking）** | cover 每個作者宣告的承重步驟（**可合併、不可掉**）＋ 標註的 recap | SC1/SC2 確定性 ＋ SC-honesty（gate-1，evidence-based，opt-in 前必跑） |
| **提議（advisory）** | 疑似過度合併（對 handout）｜`missing` 承重直覺 | SC-adv（gate-1）｜AMP1（audit） |
| **升級假設** | correctness-critical caution（radians 等，影響公式真假） | PD4 registry / 來源契約 |
| **永不強制** | 例題（`expansion:example`）、一般豐富度、**與講義 1:1** | —（明確排除） |

> 誠實界線：「會不會精簡到看不懂」終究是**判斷**，無純確定性檢查能斷。框架給的是「確定性底線（不掉宣告的步驟）＋ advisory 安全網（對 handout 疑似過度合併就提醒）」，最終校準權在作者。

---

## 7 · 確定性層與 schema/lint 增訂

- **新模組 [`pipeline/step_coverage.py`](pipeline/step_coverage.py)：** `coverage_issues(data, md_contracts, enforce) -> [(sev,msg)]`（SC1/SC2）。純 stdlib、無模型。
- **`.md` parser 擴充（成本比初稿大，Codex R2；已驗證）：** `.md` 用的是**刻意的行解析器**（非 YAML——freeform `source:` 值會讓嚴格 YAML 出錯），且**有鏡像解析器** [`narration_review.py`](pipeline/narration_review.py)（`:15` 明載「Keep in sync」，獨立重實作、同樣 `_commit()` 壓平、`screen_contract` 不在 `_FIELD_KEYS`）。故 `screen_contract` 的結構化解析（fenced 區塊 → `yaml.safe_load`，**不走 `_commit()` 壓平**）**必須**：抽成**共用解析模組**，或**同步改兩個解析器並各自加 test**；且**不得破壞既有 freeform 欄位（尤其 `source:`）**。其餘欄位行為不變。
- **`schema.py` 接線：** 載入各單元 `screen_contract`（經 `Loci`/review_pack）、跑 `coverage_issues`，以 `[coverage]` 標頭印出；`meta.coverage_enforce` 才計入 exit code。零 opt-in deck 行為不變。
- **storyboard schema：** 允許場級 `covers: [str]`（sibling，選用）；`.md` 單元允許 `screen_contract`，內含 `required_steps[]`（`id`/`tex`/`reason?`/`depends_on?`/`recap_required?`）**或** `coverage_exempt: true`（單元級顯式豁免旗標——`coverage_enforce` 下「缺 contract」的唯一合法出口，Codex R3）。
- **向後相容護欄：** 不改 `proof:`/`steps:`/`statement` 等既有形狀；缺 `screen_contract`/`covers` **在未 opt-in 時**一律 no-op（零行為改變）。**唯一例外（Codex R3）：** `coverage_enforce: true` 時，範圍內 proof/derivation 單元缺 `screen_contract`（且未 `coverage_exempt`）→ `error`（見 §4.2）。

---

## 8 · 邊界與不重疊（§10 擴充）

| 議題 | owner | 本層不重疊切片 |
|---|---|---|
| 一個 beat 多個承重動作 | `PD1` | — |
| **storyboard 漏掉源列的承重步驟**（子集/掉步驟） | —（既有未守） | **SC1** |
| **cash-in 缺畫面 recap**（標註依賴） | —（既有未守） | **SC2** |
| 上畫面文字**超出/矛盾**源 | `OF1` | SC 管「漏」，OF1 管「超」——反方向 |
| `.md` 內容忠實 handout | `L1` | SC-adv 問「screen contract 對初學者夠不夠」，非 `.md` vs 講義 |
| 一個 unit 兩概念 | `L2` | — |
| narration 衍生忠實 | `NFA` | AMP 讀 handout 標記提議敘述，非審 narration 忠實 |
| intro tagline / recap takeaway | `L6` | — |
| 講義該不該補例題/圖（**講義側**） | handout `example-supplement`/`figure-opportunity`/`mode-c-gapwalk` | AMP 是**影片側**「該不該把 handout 既有直覺 surface 到片子」，不改講義 |
| correctness caution（radians） | PD4 / 來源契約 | **不歸 AMP**（升級假設） |
| render 後像素/timing | `V6`/`V8` | SC/AMP 只碰撰寫期 storyboard/`.md`/handout |

---

## 9 · 變更落點清單（給 writing-plans）

**新增：**
- [`pipeline/step_coverage.py`](pipeline/step_coverage.py)（SC1/SC2 確定性 + self-test）。
- `video-amplification-audit` gate-1 subagent 定義 + `content_scripts/_audit/AMPLIFICATION-RUBRIC.md`（AMP1）。
- storyboard fixture：覆蓋 covered/missing/merged/recap 案例。

**修改：**
- [`review_pack.py`](pipeline/review_pack.py)：`screen_contract` 結構化解析（不壓平）。
- `schema.py`：接 `coverage_issues`、`meta.coverage_enforce` opt-in。
- [`PEDAGOGY-FIRSTLEARNER-RUBRIC.md`](content_scripts/_audit/PEDAGOGY-FIRSTLEARNER-RUBRIC.md)：新增 SC 家族（SC1/SC2 確定性、SC-adv/SC-honesty gate-1）+ §10 邊界列 + **VERDICT 計數約定（Codex R2，明確不混入 PD/OF）**：首行擴為 `VERDICT: <P> PD, <O> OF, <S> SC, <A> advisory`；`<S>` **只計 gate-1 自有的 SC-honesty blocking**；SC1/SC2 為確定性層（`schema.py`→`step_coverage.py`，`coverage_enforce` gating），以 `[Surface SC1-det|SC2-det]` 前綴列出、**不計入 VERDICT 整數**（同 OF2／PD2-4 待遇）；SC-adv 計入 advisory。
- pedagogy-firstlearner-audit agent 定義：加載 `screen_contract`、surface SC1/SC2、擁有 SC-adv/SC-honesty。
- [`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md)：`screen_contract` authoring 規則、`covers:` 慣例、合併/不掉原則、correctness-caution→假設。
- [`DESIGN.md`](DESIGN.md)：`covers:` 承載、authoring checklist。
- [`REVIEW_GATES.md`](REVIEW_GATES.md)：SC 進閘序、AMP 進 amplification 稽核序。
- `.md` schema／storyboard schema：如 §7。

---

## 10 · 校準 / rollout

1. 先在 §3.1 `derivative_of_sine`（含 `difference_quotient_for_sine`）落 `screen_contract` + `covers:`，**乾跑** SC → 確認 SC1 抓到定義行、SC2 抓到 recap（`derivative_of_sine` 對 `reduced` 標 `recap_required` 時）。
2. 人核假陽性率、調 rubric，再 per-deck opt-in（`coverage_enforce`）。
3. AMP 對 §3.1 跑一輪、出 HTML 候選、使用者裁決。
4. 全程離線可驗（mock render + stdlib self-test）；計費步驟另徵同意。

---

## 11 · 成功標準 / 驗證

- SC：`step_coverage.py` self-test 綠；對未落 contract 的 deck **零行為改變**；對 `derivative_of_sine` 落 contract 後，砍掉 `def` 的 `covers` → SC1 紅、補回 → 綠。
- AMP：對 §3.1 產出可讀 `missing`/`*-only`/`screened` 清單，假陽性可接受。
- 六鏡/OTF/PD 回歸無新 blocking；`tools/doctor.py` 不受影響。
- **收斂＝** SC blocking == 0（opt-in 後）；AMP 提議由使用者逐條裁決、不強制歸零。

---

## 12 · 決策裁定（Codex R2 已收斂）

R2 對原開放點逐一裁定，**全部維持本 spec 選擇**：
1. **contract 落點＝ `.md`**（維持；內容獨立、`L1` 可把關）——**條件：** 需 §7 的共用／同步解析器修正。
2. **`covers:` 粒度＝場級 flat 清單**（維持）——**條件：** 必配 evidence-based SC-honesty（cite 可見 payload path），否則 flat covers 不足以當 contract。
3. **SC-adv 歸屬＝ pedagogy gate-1**（維持；是「`.md` contract vs handout 取捨」，鄰 `L1`/OF 邊界，非 AMP）。
4. **AMP ＝獨立新 agent**（維持；掃 handout 擴增機會，非步驟覆蓋）。
5. **`screen_contract` ＝ opt-in warn-default**（維持）——**但非永遠 no-op：** `coverage_enforce: true` 時，範圍內 proof/derivation 單元須有 `screen_contract`（帶 `required_steps` 或 `coverage_exempt: true`），否則 `error`（§4.2/§7）。

---

## 13 · 風險與緩解

- **把 convention 當 contract**（Codex R1 最大風險）→ D5：不 parse freeform `visual_need`，改 authored `screen_contract`。
- **主觀閘不收斂** → SC1/SC2 確定性；「太精簡」只做 advisory（SC-adv）。
- **`covers:` 變橡皮圖章**（Codex R2 最大殘留風險）→ SC-honesty **evidence-based（cite payload path）且 `coverage_enforce` sign-off 前必跑**；確定性層只查 id、語義誠實由 gate-1 守（同 provenance 只查 ref 解析、忠實交 OF1）。
- **AMP 過度觸發** → D6 四態、只提 `missing`。
- **scalar 形狀被破壞 → opt-in 前 render 就變** → §7 護欄（sibling `covers:`、no-op-absent）。
- **contract 自身過簡**（作者少宣告）→ SC-adv 對 handout 比 + 最終作者校準；`.md` vs handout 由 `L1`。
- **例題被誤強制** → §6 明列永不強制。

---

## 14 · Review 採納紀錄

**Codex（R1，對 Approach A）：判 SHIP-with-changes。** 採納 6 項：① authored screen contract 取代 parse `visual_need`（已驗證 `review_pack.py:107` 壓平、`CONTENT_METHODOLOGY.md:162` 定義 visual_need 為視覺描述非步驟契約）→ D5；② SC 只對宣告的必填步驟 blocking → §4.2；③ recap 僅標註依賴時確定性、否則 advisory → SC2；④ M2「surfaced」放寬四態 → D6；⑤ correctness caution 升級假設、不埋 advisory → D4；⑥ 全走新 code → D7/§8。**Codex（R2，對寫出來的 spec）：判 SHIP-with-changes → 已整合 4 項 must-fix：** ① 解析器成本（共用／同步兩解析器＋test、不破 freeform `source:`，已驗證 `narration_review.py:15` keep-in-sync）→ §7；② `covers:` 需 evidence（SC-honesty cite payload path、opt-in 前必跑）→ §4.2/§6/§13；③ SC2「在地覆蓋」精確化＋禁跨單元 `covers` id → §4.1/§4.2/§4.3；④ VERDICT 計數（加 `<S> SC`、SC1/2 確定性不混入 PD/OF）→ §9。5 個開放決策 R2 全維持本 spec 選（§12）。**R2 明示「上述 spec 編輯後即可進 writing-plans」。**

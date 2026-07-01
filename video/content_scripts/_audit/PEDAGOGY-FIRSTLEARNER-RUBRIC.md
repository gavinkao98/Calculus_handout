# 初學者教學＋上畫面文字忠實稽核 — 維度與收斂線（PEDAGOGY-FIRSTLEARNER）

> 本檔是「初學者教學＋上畫面文字忠實稽核（First-Learner Pedagogy ＋ On-Screen-Text Faithfulness）」的契約與**單一真相來源（single source of truth）**。gate-1 ＝ Claude subagent（`pedagogy-firstlearner-audit`，免費、唯讀），一次讀齊 storyboard＋cited `.md`＋handout，承載**兩個分開回報的維度家族**：**PD（教學品質）** 與 **OF（上畫面文字忠實）**；只回報、絕不改檔（propose-not-act，findings 交回使用者裁決）。維度／收斂線**只在這裡改一次**，gate-1 prompt 只「引用」不「複述」（防漂移）。
>
> **規範權威**見 [`../../SPEC-pedagogy-firstlearner-framework.md`](../../SPEC-pedagogy-firstlearner-framework.md)（§5 OTF 機制、§7 本閘、§9 確定性層與兩軸澄清、§10 不重疊邊界、§12 必定四項），以及 [`../../CONTENT_METHODOLOGY.md`](../../CONTENT_METHODOLOGY.md)（P1–P4 規則、OTF provenance）、[`../../DESIGN.md`](../../DESIGN.md)（scaffold 承載、P5/P6 視覺）。本檔只定「審哪些維度、哪些是 blocking、哪些不算 finding、怎麼回報」，**不重述**方法論本身。
>
> **provenance 文法（Plan 1 已落地）：** 機器可解析的 provenance 文法是 **`ref:` / `refs:`**——scene 級 `ref:` 被所有上畫面教學文字欄位繼承；`refs:` 是一張**欄級覆寫**對映，以欄位路徑為 key，各解析到 `md:<unit_id>` 或 `doc:<handout-anchor>`（[`../../pipeline/provenance.py`](../../pipeline/provenance.py) `scene_text_refs`）。freeform `source:` 是**另一條人讀標籤**，留著、永不解析。本檔全程講 `ref:`/`refs:`（閘真正讀的東西）。

## 審查對象與邊界

本閘在 render 相位跑（隨閘跑、含後鎖），一次讀齊三件：

1. **本節的 `storyboards/<deck>.yml`** — 畫面文字 SSOT：`statement` / `scaffold(motive·problem·flag)` / `annotations` / divider 文字 / callout `body` / step·result `reason` 等全部上畫面教學文字，以及 `meta.pedagogy_profile`、`assumptions` registry、各欄的 `ref:` / `refs:`，以及場級 `covers:`（SC 覆蓋宣告）。
2. **`content_scripts/<deck>.md`** 裡被 cite 的 `.md` 單元 — 上畫面文字的核准源（`md:<unit_id>` 解析到此），**含該單元的 `screen_contract.required_steps`（SC 的承重步驟契約）**。
3. **handout `chapter<N>-print-standalone.html`** 的 anchor — `doc:<handout-anchor>` 解析到此（`id="frag-sec-*"`／`data-fig="*"`）。

讀 `meta.pedagogy_profile`（預設 `first_time`）與 deck 級 `CONTENT_APPROVED`（yes/no）。

- **審**：教學粒度／動機／divider／前提（PD1–PD4）＋上畫面文字對 cited 源的忠實與 source 充分性（OF1–OF2）。
- **不審**：`.md` 內容 vs 講義（歸 `L1`）、narration 衍生（歸 `NFA`）、render 後像素／hook 輸出／timing（歸 `V*`/`A*`），以及 §10 既有 owner 已擁有的任何 finding。

**兩軸澄清（§9.3，severity class vs gating）：** 「blocking」是 finding 的**嚴重度類別**，**不等於「會擋稿（blocks the deck）」**。落地當下，未回填 deck 上的**所有**新發現——確定性層**與** gate-1 的 PD/OF/SC blocking——一律以 **warn/dry-run** 呈現、不 gating；per-deck 經 opt-in 後才翻 gating。下文「收斂＝PD/OF/SC blocking == 0」是 **opt-in 後**的收斂目標，非落地門檻。

## 硬紀律（置於維度之前，防 seed_converge 的「主觀不收斂＋drift」）

- **blocking 只給**：可觀察的遺漏 / 一個具體被跳過的步驟 / 缺必填欄位 / 與 cited 源矛盾。「可以更有動機／更慢／更清楚」**一律 advisory**。
- **每條 blocking 必須 cite**：unit id ＋ 確切的 beat／欄位 ＋ 缺的步驟或矛盾點 ＋ 一個最小修法。
- **禁止**自動改寫迴圈；**禁止** re-litigate 已認可的教學法。
- **分開計數（Codex D）：** 輸出**分別**回報 `PD blocking`／`OF blocking`／`SC blocking` 摘要，**不混在一起**——免得主觀教學 finding 蓋掉硬忠實／覆蓋失敗。
- **確定性／判斷分工（D-P3-1）：** PD2/PD3/PD4 的**結構** blocking、OF2、**SC1/SC2** 由 [`../../pipeline/pedagogy.py`](../../pipeline/pedagogy.py)／[`../../pipeline/provenance.py`](../../pipeline/provenance.py)／[`../../pipeline/coverage.py`](../../pipeline/coverage.py) **確定性計算**；gate-1 agent **不重新實作**它們，只把它們帶教學脈絡**浮現出來（surface）**並擁有 advisory 層。**gate-1 agent 自己的 blocking ＝ PD1＋OF1＋SC-honesty（讀真正解析到的源／payload）。**

## PD1–PD4 — 教學品質（§7 i）

結構 blocking（多為確定性）＋品質 advisory。每條標 blocking／advisory ＋ §10 邊界。

| code | blocking（可觀察、需 cite 證據） | advisory | 邊界（§10） |
|---|---|---|---|
| **PD1** beat 粒度 | 單一 beat／`{show}` reveal 壓了 **>1 個承重的**代數／邏輯動作。讀 `pedagogy_profile`。**這是 agent 自己的判斷（無確定性對應），是 gate-1 自有 blocking 之一。** | 對 `first_time` 可更分段 | 讓 `L2`（unit 兩**概念**）；**PD1 管一 beat 多動作**（含單一概念單元內部 reveal 過度壓縮） |
| **PD2** 動機 | **確定性**：`theorem_proof`／`derivation` 場缺 `scaffold.motive`（→ `pedagogy.py`）。agent 不重算，只浮現 | motive 弱／空洞；`definition_math` 是否該帶 motive（語意，§9.2） | 內容忠實歸 OF1／`L1`；`definition_math` 必填與否＝advisory |
| **PD3** divider | **確定性**：`kind: divider` 場缺 `scaffold.problem`（→ `pedagogy.py`）。agent 不重算，只浮現 | problem 模糊／非具體式（不是一條具體式子） | 只在 `kind: divider` 場觸發；intro（`kind: intro`）、recap（`kind: content`／`recap_cards`）依 kind/template 模型本就排除（§10 `L6`） |
| **PD4** 前提 | **確定性**：registry 宣告的 assumption 在其 `first_use_unit` 未渲 flag（→ `pedagogy.py`）。agent 不重算，只浮現 | flag 措辭／位置 | 「用到與否／何處首用」由作者在 registry 顯式宣告，**閘永不推斷** |

> **PD2/PD3/PD4 的結構 blocking 由 `pipeline/pedagogy.py` 確定性計算；gate-1 agent 帶教學脈絡把它浮現出來、並擁有 advisory 層。gate-1 agent 自己的 blocking ＝ PD1 ＋ OF1 ＋ SC-honesty（SC1/SC2 走確定性層、非此）。**

## OF1–OF2 — 上畫面文字忠實（§5、§7 ii）

- **OF1 忠實（blocking，agent 判斷）。** 上畫面教學文字**矛盾或超出**它 cite 的源（加了源沒有的數學／結論、改了條件）。OF1 **讀真正解析到的源**——scene 的 `ref:`（或某欄 `refs:` entry）指向的 `md:<unit>` 或 `doc:<anchor>` 的**實際內容**，不是只看 ref 存不存在。
  - **source 充分性（D-P3-4）：** 也要 flag 當解析到的源**過寬、無法 specifically 支持該斷言**——例：用整節／recap 綜合單元當源，去 cite 一條它根本沒講的具體子斷言。此時**必須補一個欄級 `refs:` 覆寫**指向更 specific 的 locus。
  - **OF1 不重算數學正確性**（那是 `L5`）；只查「是否被 cited 源支持」。
- **OF2 可回溯（blocking，結構／確定性）。** 某上畫面教學文字欄位的**有效 `ref`** 缺失或無法解析 → [`../../pipeline/provenance.py`](../../pipeline/provenance.py) `provenance_issues`（Plan 1）確定性產出。agent **只浮現、不重新實作**。
  - **OF2 確定性覆蓋現況（巢狀 `reason` 已補，2026-06-30）：** `_present_text_fields()` 掃**頂層**教學文字欄位（`statement`／`problem`／`body`／`reason`／`prompt`／`scaffold.motive`·`problem`／`annotations[]`／`points[]`），**以及 derivation 模板的巢狀 `reason`**（`steps[].reason`／`result.reason`／`check.reason`／`lines[].reason`，見 [`../../pipeline/templates/derivation.py`](../../pipeline/templates/derivation.py)，真實 deck 大量使用）。故巢狀 `reason` 缺 ref 時 OF2 **現在會**觸發（Codex follow-up，2026-06-30 已補：`_present_text_fields` 發 `steps.i.reason`／`result.reason`／`check.reason`／`lines.i.reason` 路徑＋self-test＋一條巢狀-reason 缺 ref 的 fixture `bad_nested_reason`，gap closed）。仍**不**在 OF2 範圍內者：`steps[].math`／`result.math`／`check.math` 等**等式內容**（Codex 只 flag `reason`；等式內容算不算上畫面教學文字另議），by design 留在 OF2 之外。

**欄級覆寫規則（§5.1，已落地文法）：** 所有上畫面教學文字欄位**預設繼承 scene 級 `ref:`**；**只有當該欄位 (a) cite 一個與 scene 級不同的 locus、(b) 跨單元綜合、或 (c) 提出高風險數學斷言時，才必須帶欄級 `refs.<field_path>` 覆寫**。OF1 的 source 充分性就是在強制這條：**何時必須欄級覆寫 ＝ 上述 (a)(b)(c) 任一；OF1 如何判 specific ＝ 看解析到的源有沒有直接陳述該欄位的斷言**——支持得了就 clean，源太寬（只「沾得上邊」卻沒陳述該斷言）就 flag 並要求更緊的 `refs:` 覆寫。（`source:` 是 freeform 人讀標籤，**不是**機器 ref，OF1 不據它判斷。）

## SC1–SC2 ＋ SC-adv／SC-honesty — 推導步驟覆蓋（expansion 層，spec §4）

審 storyboard 的 proof/derivation 有沒有**覆蓋** cited 源宣告的承重步驟——**與 OF 反方向**：OF 抓「上畫面文字**超出**源」，SC 抓「畫面**漏掉**源列的承重步驟」。錨＝`.md` 單元的 `screen_contract.required_steps`（作者宣告的承重步驟清單，帶 `id`／`tex`／`depends_on?`／`recap_required?`）＋ storyboard 場級 `covers:`。核心校準：**可合併／重排、不可掉**（一個 reveal 可 `covers` 多個 id；只有掉某承重步驟才是 finding）。**「可合併」只限覆蓋層——一個 reveal 合併多步仍可能因擠壓觸發 `PD1`（一 beat 多動作）；SC 與 PD1 不同切片、不互相豁免。**

- **SC1／SC2（確定性，surface 不重算）。** 由 [`../../pipeline/coverage.py`](../../pipeline/coverage.py) `coverage_issues` 確定性計算：**SC1**＝某「須顯示」步驟（`required_steps` 除「有 `depends_on` 且無 `recap_required`」的純回指外）未被該單元所有 `ref:` 場景之 `covers:` 聯集蓋到；**SC2**＝帶 `recap_required` 的 cash-in 步驟未被在地覆蓋（SC1 的回指子集，另標訊息）。agent **只帶教學脈絡 surface**（前綴 `[Surface SC1-det|SC2-det]`），不重算、**不計入 VERDICT 整數**（同 OF2／PD2-4 待遇）；gating 由 `schema.py` 的 `coverage_enforce` 管。
- **SC-honesty（blocking，agent 判斷，evidence-based）。** 某場 `covers:` 宣告某 id、但其上畫面 payload（`statement`／`proof.N`／`qed`／`steps[].math`…）語義上**沒有**該步驟 → blocking。**每條 finding 必 cite 確切可見欄位／reveal target（如 `proof.0`），非泛稱。** 這是把「`covers:` 當橡皮圖章」補實的守門——**`coverage_enforce` sign-off 前不可略過**。這是 **gate-1 自有 SC blocking**。
- **SC-adv（advisory，agent 判斷）。** 拿 `required_steps`／`covers` 對 **handout** 承重步驟比，疑似「併過頭、少了承重動作、初學者恐失脈絡」→ 建議加 `required_step`。**最終校準是作者的**（不 blocking）。與 `L1` 不同切片：SC-adv 問「screen contract 對初學者夠不夠」，非「`.md` 忠不忠於講義」。
- **生命週期／收斂：** 同 OF——`md:` 契約在 deck `CONTENT_APPROVED=yes` 才 gating；DRAFT 期 dry-run。收斂＝**SC blocking（＝SC-honesty）== 0**（opt-in 後）。

## 邊界與不重疊（§10）

本閘**獨立但從屬於既有 owner**；永不 raise 下表既有擁有者已擁有的 finding：

| 議題 | 既有擁有者 | 本閘不重疊切片 |
|---|---|---|
| 一個 unit 兩個教學**概念** | six-lens `L2` | — |
| 一個 **beat** 多個承重**動作**（含單一概念單元內部過度壓縮） | — | **PD1** |
| **intro tagline／recap takeaway** 存在性與定位 | `L6` | — |
| 個別 **content／divider** 場的 on-screen motive·problem（PD2 限 `theorem_proof`/`derivation`；PD3 限 `kind: divider`；intro/recap 已由 kind 排除） | — | **PD2/PD3** |
| `.md` 內容忠實講義 | `L1`（含 scaffold 例外 §5.5） | — |
| narration → HTML/spoken 衍生忠實 | `NFA` | — |
| **storyboard 上畫面文字 vs 核准源** | —（既有未守） | **OF1/OF2** |
| **storyboard 漏掉源列的承重步驟**（子集／掉步驟） | —（既有未守） | **SC1**（確定性）＋**SC-honesty**（覆蓋誠實） |
| **cash-in 缺在地 recap**（標註依賴） | —（既有未守） | **SC2**（確定性） |
| screen contract 對初學者夠不夠（vs handout） | `L1` 管 `.md` vs 講義 | **SC-adv**（不同切片：問 contract 夠不夠，非 `.md` 忠實） |
| scaffold／statement 數學**正確** | `L5`（`.md` 內） | OF1 只查「是否被源支持」，**不重算**正確性 |
| 圖可讀（窗格／爆框） | `V3` | — |
| 圖**凸顯**夠不夠 | — | `A7` 子準則 |
| 文字讀不到 | `V4`/`A6` | min-size floor |
| **render 後**畫面像素／hook 輸出／timing vs beat | `V6`/`V8` | OF 只查**撰寫期** storyboard 文字的 provenance／忠實，不碰 render 後像素 |
| hook 自繪、未宣告於 YAML 的教學文字 | hook-engineering `E1` ＋ 視覺閘 | OF 讀 YAML 看不到；重要 hook 文字須宣告進 YAML payload（§5.7） |

> **PD1 vs L2 tie-breaker：** `L2` ＝ **跨單元的概念計數**（unit 層，含 silent-drop／兩概念同框）；**PD1** ＝ **單一 beat 內的動作計數**（unit 拆對了、但一個 reveal 仍壓多步）。

## 生命週期（§5.6、D-P3-3）

OF／SC-honesty findings **只有當 cited content-script 的 deck 級 `CONTENT_APPROVED=yes`（已 lock）時才是 blocking 類**；DRAFT 階段（`CONTENT_APPROVED=no`，源未定）OF／SC-honesty 一律 **dry-run／advisory**（findings 報為 advisory／dry-run，**永不 blocking**）——否則是拿未核准的源當忠實基準。**deck→unit 繼承：** `md:<unit>` ref **繼承 deck 級 `CONTENT_APPROVED`**；`doc:<handout-anchor>` ref **一旦解析即可 gate**。

## 收斂線（§9.3）

- **收斂判準**：本閘收斂 ＝ **PD blocking == 0 AND OF blocking == 0 AND SC blocking == 0**（此處 PD/OF/SC blocking 指 **gate-1 自有層**＝PD1＋OF1＋SC-honesty，計數約定見 §回報規格；確定性層 PD2/3/4＋OF2＋SC1/SC2 另由 `schema.py` 以 `pedagogy_enforce`／`otf_enforce`／`coverage_enforce` 收斂），是 **per-deck opt-in 後**的收斂目標，**NOT 落地門檻**（落地當下一切 warn/dry-run，見上「兩軸澄清」）。
- advisory 由使用者**逐條裁決**，**不強制歸零**（同 [`NARRATION-FAITHFULNESS-RUBRIC.md`](NARRATION-FAITHFULNESS-RUBRIC.md):40、[`../../../handout/_audit/PROSE-AUDIT-RUBRIC.md`](../../../handout/_audit/PROSE-AUDIT-RUBRIC.md):40）。

## 不算 finding（別誤報）

- 已認可教學法的 restyle（不得 re-litigate）。
- 已被 `L1` scaffold 例外（§5.5）涵蓋的呈現重排／增補。
- intro／outro 的品牌／定位文字；recap takeaway（歸 `L6`）。
- render 期才看得到的像素／hook／timing（歸 `V6`/`V8`）。
- **不要 over-report**——**乾淨的維度是有效結果**。

## 回報規格（最終訊息；不寫任何檔案）

- 首行：`VERDICT: <P> PD blocking, <O> OF blocking, <S> SC blocking, <A> advisory`（PD／OF／SC **分開計**）。
- **VERDICT 整數的計數約定（calibration 已鎖，2026-06-30）：** `PD blocking`／`OF blocking` 整數**只計 gate-1 自有 blocking——PD1 與 OF1**。surfaced 的確定性結構 blocking（PD2/PD3/PD4 結構存在性＋OF2）由確定性層（`schema.py` → `../../pipeline/pedagogy.py`／`../../pipeline/provenance.py`）擁有並各自 gating（`pedagogy_enforce`／`otf_enforce`），**不計入本 VERDICT 整數**——免與確定性閘重複計數；它們仍逐條列出（見下）但不進首行整數。**`SC blocking` 同理只計 gate-1 自有的 SC-honesty；SC1／SC2 確定性（`../../pipeline/coverage.py`，`coverage_enforce` gating）以 `[Surface SC1-det|SC2-det]` 列出、不計入整數；SC-adv 計入 advisory。** `advisory` 整數只計 gate-1 自身的 advisory（如 PD2／PD3、SC-adv，**含 OF1／SC-honesty 因 §生命週期 降為 dry-run 者**）。
- 逐條（一行一筆）：
  `- [Blocking|Advisory] [PD#|OF#|SC#] <unit-id> · <beat/field> — issue（cite 源／文字）→ minimal fix`
  surfaced 的確定性 finding 改用 **`[Surface PD#-det|OF2-det|SC1-det|SC2-det]`** 前綴、帶教學脈絡列出（**不**進 VERDICT 整數）。
- 每個**乾淨**維度各一行（如 `PD3 clean`）。
- 末行：對「**PD／OF／SC blocking 是否各自歸零**」給明確結論（post-opt-in framing）。
- 護欄重申：稽核員**唯讀**，propose-not-act，只回報、不改任何檔，findings 交回使用者裁決。

**交付給使用者裁決時**：依 [`../../../CLAUDE.md`](../../../CLAUDE.md) 交付規則產 standalone HTML 審核稿、finding 標穩定編號。純版控紀錄（如本 rubric、`REPORT-*.md`）不在 HTML 之限。

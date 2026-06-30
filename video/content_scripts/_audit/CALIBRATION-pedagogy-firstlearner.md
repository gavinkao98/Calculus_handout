# CALIBRATION — pedagogy-firstlearner gate（兩軌期望表）

> 本檔是 `pedagogy-firstlearner` 閘家族的**期望findings 表**（calibration baseline）。施測對象是兩副校準 deck：
> - **deck A（approved）**：[`../../storyboards/_fixtures/pedagogy_audit.yml`](../../storyboards/_fixtures/pedagogy_audit.yml)，源 [`../_fixture_pedagogy.md`](../_fixture_pedagogy.md)（`CONTENT_APPROVED=yes`）。
> - **deck B（draft）**：[`../../storyboards/_fixtures/pedagogy_audit_draft.yml`](../../storyboards/_fixtures/pedagogy_audit_draft.yml)，源 [`../_fixture_pedagogy_draft.md`](../_fixture_pedagogy_draft.md)（`CONTENT_APPROVED=no`）。
>
> 契約見 [`PEDAGOGY-FIRSTLEARNER-RUBRIC.md`](PEDAGOGY-FIRSTLEARNER-RUBRIC.md)。表分**兩軌**：① 確定性層（[`../../pipeline/schema.py`](../../pipeline/schema.py) 驅動 [`../../pipeline/pedagogy.py`](../../pipeline/pedagogy.py)／[`../../pipeline/provenance.py`](../../pipeline/provenance.py)，本檔已 pin 確認基線）；② agent 判斷層（gate-1 `pedagogy-firstlearner-audit`，由 Task 4 dispatch 後比對本表）。Task 4 的 calibration run 把實測結果填進文末「Calibration run result」。

---

## ① 確定性層期望（schema.py → pedagogy.py / provenance.py）

確定性findings 由 `schema.py` 直接產出，**warn-only**（兩副 deck 的 meta 都沒有 `otf_enforce`／`pedagogy_enforce`，故 warn、exit 0）。下列字串是**逐字確認的基線**（直接貼自實跑輸出，見本節末）。

### deck A — 4 條（3 `[pedagogy]` ＋ 1 `[provenance]`），別無其他

| 軌 | code | scene · 欄位 | 逐字訊息（warn） |
|---|---|---|---|
| provenance | **OF2** | `of2_det_no_ref` · `statement` | ``of2_det_no_ref.statement: on-screen teaching text has no provenance ref (scene `ref:` or `refs.statement`)`` |
| pedagogy | **PD2** | `pd2_det_no_motive` | `pd2_det_no_motive: theorem_proof should carry scaffold.motive (on-screen 'why we're doing this')` |
| pedagogy | **PD3** | `pd3_det_no_problem` | `pd3_det_no_problem: divider should carry scaffold.problem (the concrete problem/expression being solved)` |
| pedagogy | **PD4** | `pd4_det_first_use` | `pd4_det_first_use: first_use_unit of 'radians' must render scaffold.flag: 'radians' (found None)` |

> 注意字串細節：OF2 訊息用 **backtick** 包 `` `ref:` ``／`` `refs.statement` ``（非單引號）；PD4 訊息經 Python `repr()`，故 `'radians'` 帶單引號、`None` 為 bareword。

**deck A 其餘所有 scene 確定性乾淨**——不產生任何 `[pedagogy]`／`[provenance]` finding：
- agent-judgment 軌（`pd1_compressed`／`of1_exceeds`／`of1_adequacy`／`pd2_adv_weak_motive`／`pd3_adv_vague_problem`）：每個都帶 resolvable `ref:`，且 `theorem_proof`／`derivation` 場都帶非空 `scaffold.motive`，故**不**觸 PD2-det／OF2；兩個 advisory divider 帶（即使模糊／空洞的）`scaffold.problem`／`motive`，故**不**觸 PD3-det／PD2-det。
- CLEAN 軌（`clean_segmented`／`clean_of1`）與 BOUNDARY 軌（`boundary_two_concepts`／`boundary_intro`／`boundary_recap`）：同理 ref 皆 resolvable、motive 皆在、divider 不在其中、intro 省略 `say`（不觸 silent-warn）且 OF2-exempt、recap 的 `points` 因 resolvable ref 而 OF2-clean。
- registry 只宣告一條 assumption `radians`，其 `first_use_unit` 指 `pd4_det_first_use`（唯一缺 flag 的 first-use 場），且**無任何 orphan `scaffold.flag`** → PD4 恰好觸發一次。

### deck B — 確定性乾淨

deck B 的單一 scene `draft_exceeds` 帶 resolvable `ref: md:unit_draft` ＋ 非空 `scaffold.motive`，`theorem_proof` 但 motive 在故無 PD2-det、ref 解析故無 OF2 → **無任何確定性 finding**，`schema.py` 印 `structure OK` 並 exit 0。

### 確認基線（逐字貼自 `schema.py` 實跑，repo venv python）

```
===== DECK A (pedagogy_audit.yml) =====
[schema] pedagogy_audit.yml: structure OK
[provenance] pedagogy_audit.yml: 1 finding(s) (warn-only; set meta.otf_enforce to gate)
  WARN   of2_det_no_ref.statement: on-screen teaching text has no provenance ref (scene `ref:` or `refs.statement`)
[pedagogy] pedagogy_audit.yml: 3 finding(s) (warn-only; set meta.pedagogy_enforce to gate)
  WARN   pd2_det_no_motive: theorem_proof should carry scaffold.motive (on-screen 'why we're doing this')
  WARN   pd3_det_no_problem: divider should carry scaffold.problem (the concrete problem/expression being solved)
  WARN   pd4_det_first_use: first_use_unit of 'radians' must render scaffold.flag: 'radians' (found None)
EXIT=0

===== DECK B (pedagogy_audit_draft.yml) =====
[schema] pedagogy_audit_draft.yml: structure OK
EXIT=0
```

---

## ② agent 判斷層期望（gate-1 `pedagogy-firstlearner-audit`）

對 **deck A（`CONTENT_APPROVED=yes`）** dispatch gate-1 agent 時，期望逐 scene 結果如下。agent 自有 blocking ＝ **PD1**（判斷）＋ **OF1**（讀真正解析到的源）；PD2/PD3/PD4 與 OF2 的結構 blocking 由確定性層擁有，agent 只**帶教學脈絡浮現（surface）**並擁有 advisory 層（rubric §硬紀律 D-P3-1）。

### deck A — agent 自有 blocking

| 期望 | code | scene · 欄位 | 判斷依據（源／文字）→ 最小修法 |
|---|---|---|---|
| **Blocking** | **PD1** | `pd1_compressed` · `{show statement}` | 單一 reveal 把「同除 $\sin\theta$」與「取倒數翻向」**≥2 個承重代數動作**塞進一拍；對 `first_time` 過度壓縮（unit_squeeze 支持內容但要求分步）→ 拆成多個 `{show}` beat（比照 `clean_segmented`）。 |
| **Blocking** | **OF1**（exceeds source） | `of1_exceeds` · `statement` | `statement` 斷言 $(\sin\theta)/\theta$ 在 $(0,\pi/2)$ **單調遞減且以 1 為上界**，但 `md:unit_narrow` 只陳述 $\theta\to0$ 單點極限、明言不對任何 $\theta\neq0$ 下結論 → 刪去超出源的單調／有界斷言，或改 cite 真正支持它的源。 |
| **Blocking** | **OF1**（source adequacy） | `of1_adequacy` · `statement` | scene-level `ref: md:unit_broad` 過寬：unit_broad 是主題層綜述、明言**不寫任何具體子斷言**（含不給 $(1-\cos\theta)/\theta\to0$），卻被用來 cite 這條具體極限；且無欄級 `refs:` 覆寫 → 補一個 `refs.statement` 指向真正陳述該斷言的更 specific locus（如 `md:unit_two`）。 |

### deck A — agent advisory（motive／problem 在，故無對應確定性 blocking）

| 期望 | code | scene · 欄位 | 判斷依據 → 最小修法 |
|---|---|---|---|
| **Advisory** | **PD2** | `pd2_adv_weak_motive` · `scaffold.motive` | motive **在**（故無 PD2-det）但空洞——「做這個證明」未說「為何而做」→ 補上實質動機（如「用幾何夾出極限、作為導數推導起點」）。 |
| **Advisory** | **PD3** | `pd3_adv_vague_problem` · `scaffold.problem` | problem **在**（故無 PD3-det）但非具體——「再來看更多三角的東西」不是一條具體式子 → 換成具體待解式（如「求 $\lim_{\theta\to0}(1-\cos\theta)/\theta$」）。 |

### deck A — agent SURFACES 4 條確定性 finding（帶教學脈絡）

agent **不重算**確定性層，但會把上節①的 4 條（PD2 `pd2_det_no_motive`、PD3 `pd3_det_no_problem`、PD4 `pd4_det_first_use`、OF2 `of2_det_no_ref.statement`）**帶教學脈絡浮現出來**。

### deck A — MUST-NOT-RAISE（agent 須保持沉默）

| scene | 為何不得 raise |
|---|---|
| `clean_segmented` | derivation 已分多 beat、每拍一動作，且忠實 unit_squeeze → PD1 clean。 |
| `clean_of1` | `statement` 恰好陳述 unit_squeeze 所述、完全被支持 → OF clean。 |
| `boundary_two_concepts` | `statement` 含兩個獨立教學**概念**＝ `L2` 領域（per-unit 概念計數，別處 owner），**非** PD1（per-beat 動作計數）；忠實 unit_two（兩概念皆陳述）→ 無 OF。agent 須**不** raise。 |
| `boundary_intro` | `kind: intro` tagline／品牌文字 ＝ `L6`；OF2-exempt（intro/outro）；省略 `say`。agent 須**不** raise。 |
| `boundary_recap` | `recap_cards` 的 takeaway ＝ `L6`（別處 owner）；`points` 因 resolvable ref 而 OF2-clean。agent 須**不** raise。 |

### deck B（draft，`CONTENT_APPROVED=no`）— 生命週期

| 期望 | code | scene · 欄位 | 判斷依據 → 處置 |
|---|---|---|---|
| **Advisory／dry-run（NOT blocking）** | **OF1** | `draft_exceeds` · `statement` | `statement` 超出 `md:unit_draft`（draft 只給單點極限，未核准導數結論），**但** deck 級 `CONTENT_APPROVED=no` → 依 rubric §生命週期，OF 一律 dry-run／advisory、**永不 blocking**（否則是拿未核准源當忠實基準）。確定性層此 deck 乾淨。 |

### 期望 VERDICT 形狀與「計數約定」（Task 4 需確認鎖定）

首行格式（PD 與 OF **分開計**，rubric §回報規格）：

```
VERDICT: <P> PD blocking, <O> OF blocking, <A> advisory
```

deck A 的**實質 per-scene 期望**已在上面釘死：agent 自有 PD1 ×1、OF1 ×2、PD2-advisory ×1、PD3-advisory ×1，並 surface 4 條確定性（PD2/PD3/PD4 + OF2）。但 VERDICT 的整數**是否把 surfaced-deterministic 計入**有兩種約定，需 Task 4 的 calibration run 確認並鎖定：

- **約定 A（含 surfaced）：** `PD blocking = PD1 + surfaced(PD2/PD3/PD4) = 1 + 3 = 4`；`OF blocking = OF1×2 + surfaced(OF2) = 2 + 1 = 3`。→ `VERDICT: 4 PD blocking, 3 OF blocking, 2 advisory`。
- **約定 B（僅 agent 自有）：** `PD blocking = PD1 = 1`；`OF blocking = OF1×2 = 2`。→ `VERDICT: 1 PD blocking, 2 OF blocking, 2 advisory`。

> **⚠️ 計數問題（flag 給 Task 4）：** 上述「VERDICT 整數含不含 surfaced-deterministic」是本校準唯一未鎖的約定。per-scene 的實質期望（誰 blocking／advisory／clean／surface）不受此影響、已 crisp。Task 4 跑完依實測擇一鎖定，並在下節記錄。advisory 計數兩約定皆為 2（`pd2_adv_weak_motive` + `pd3_adv_vague_problem`；surfaced-deterministic 不進 advisory 欄）。

---

## Calibration run result

> （留待 Task 4 填寫：dispatch gate-1 agent 於 deck A／deck B 後，貼回實際 `VERDICT` 行與逐條輸出，對照上表確認 per-scene 期望命中、鎖定 VERDICT 計數約定，並記錄任何偏差。）

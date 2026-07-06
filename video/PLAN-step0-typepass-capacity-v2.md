# Layout & Type Pass（Step 0）＋ 容量契約 v2（G1–G6）實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development`（建議）或 `superpowers:executing-plans` 逐 task 執行本計畫。步驟用 checkbox（`- [ ]`）追蹤。每 task 一 commit、雙閘 review 照本 repo 慣例。

**Goal:** 把 2026-07-05 使用者核可的兩案落地——(A) Layout & Type Pass：修四處「重要的字反而小」的型階反轉＋圖佔比授權指引；(B) 容量契約 v2：G1 語域執法、G2 標籤亮度地板、G3 稀疏出口、G4 卡片孤字、G5 Authoring Playbook、G6 守門串聯——使之後所有章節的 storyboard 直接套用、守門自動接住。

**Architecture:** 先 Step 0-a 用 A/B mock render 定死字級 token（使用者 sign-off 閘），Step 0-b 落地＋全回歸；然後 v2 按「純文檔 → lint 靜態閘 → sizecheck 量測閘 → 回歸 fixtures」推進，容量預算只在最終尺寸上校一次。G2 併入 Step 0 的 graph-label patch（同檔同回歸）。最後是 §3.1 單景 backlog（內容層，逐項 VLM 迴圈）。

**Tech Stack:** manim（本地 mock render）、pdflatex（MiKTeX）、`video/scratch_frames.py`（1080p 靜幀）、`pipeline/lint.py`／`sizecheck.py`／`capacity_selftest.py`、`visual-frame-audit` gate-1 agent、Codex read-only（standing consent）。**全程離線零計費：不動 TTS、不動 Gemini、不動 4K。**

---

## 0. 背景與依據（新對話必讀）

- 三輪裁決（2026-07-05，同一使用者 session）：
  1. §3.1 全 25 景場景效果分析（`output/_qa/REVIEW-s31-scene-effect-analysis.html`，gitignored 可重生）；
  2. **通用密度策略＝容量契約 v2（G1–G6）獲核可**（`output/_qa/PROPOSAL-universal-density-strategy.html` rev 2，Codex 8 findings 已處置）；
  3. **Layout & Type Pass 獲核可**（`output/_qa/PROPOSAL-layout-type-pass.html` rev 2，Codex 8 findings 已處置；其中 P-B 行長上限、P-D 節奏重構**經量測撤案**）。
- 本計畫是上述三份（gitignored）文件的**自足整併**：不需要讀原 HTML 也能執行。
- 工作分支：`video/template-redesign-navy-spine`。開工前 `git status` 確認前輪未 commit 的變更已由其所屬流程收掉（或明確 stash），**本計畫每 task 只 commit 自己的檔**。
- **MiKTeX 冷快取坑**（REBUILD_STATUS 2026-07-01 教訓）：批次 build 多 Tex 的步驟（sizecheck 全 deck、scratch_frames、capacity_selftest）偶發 `PermissionError`／`could not build scene`——**重跑即正常**，勿當真 diff／真缺幀。

### 0a. 不動清單（任何 task 不得越線；review 時據此擋 scope creep）

| 已拍板 | 內容 |
|---|---|
| 字級恆定 | 分量變異永不由縮字吸收；auto-fit 已否決。本計畫改的是**全域 token 校準**，不是 per-scene fit |
| PX_TO_FS=0.698／TEXT_SCALE=1.3102 | 數學／文字尺寸錨不動（重校全系統，風險不成比例） |
| h1=78 內容標題 | 已兩輪調降；預設不動，僅 Step 0-a 順渲 68 對照供使用者裁決 |
| Lectern bias | 上偏置中、留白集中底部＝設計語言；theorem 短 proof 錨 proof label 下＝2026-07-01 拍板。**「垂直置中」類建議已撤回，勿復活** |
| masthead 幾何 | MASTHEAD_TOP／TITLE_GAP／BODY_TOP_GAP_MAX 不動 |
| prose 行長 | 估寬器實測 ~65 加權字元（在可讀區間上緣）＝**不動**；`scaffold.motive` 滿 CONTENT_W 契約不動（P-B 撤案） |
| 縱向節奏 token | LINE_GAP／ROW_GAP／各模板 pitch 各有壓測紀錄＝不重構（P-D 撤案） |
| display-style 慣例 | `statement`／`math`／`proof`／`formulas`／`scaffold.problem`＝display 欄位用 `\frac`，**G1 不掃** |
| L3 aside | author-authored、opt-in；框架絕不自動生成內容填空 |
| 超量哲學 | warn 不 error；拆頁／精簡是作者決策 |
| v2.1 遞延項 | `label_plate` 選配、label-vs-own-curve 亮度差 advisory、`_wrap_mixed` widow-control、say↔reveal target 對齊閘——**本輪不做** |

### 0b. 檔案地圖（本計畫會動的檔）

| 檔 | 動什麼 |
|---|---|
| `pipeline/visuals/theme.py` | ＋`"tag": 30` scale token |
| `pipeline/brand.py` | `eyebrow()` 加 size 參數；`progress_dots` 半徑 |
| `pipeline/templates/graph.py` | 標籤 size 預設、`_carrier_label_role` 亮度地板、單圖/compare 預設尺寸 |
| `pipeline/templates/derivation.py` | result tag 用 `"tag"`、clamp px 按 kind 分派 |
| `pipeline/templates/_common.py` | `render_scaffold` 加 `problem_size`；part 頁碼 size |
| `pipeline/templates/divider.py` | hook 式傳 `problem_size=56` |
| `pipeline/lint.py` | ＋G1 `_display_math_in_inline`、G4 `_card_widow_issues` |
| `pipeline/sizecheck.py` | ＋G3 `_sparse_issues`（讀 `sparse_ok`） |
| `pipeline/_selftest_graph_labels.py`（新）、`pipeline/_selftest_lint_registers.py`（新） | 單元自測 |
| `storyboards/_demo_registers.yml`（新）、`storyboards/_demo_graph_muted.yml`（新）、`storyboards/_demo_capacity.yml` | fixtures |
| `capacity_selftest.py` | EXPECT 擴充 |
| `storyboards/ch03_trig_derivatives.yml` | G1/G4 示範修正（4＋1 處）＋（A/B 核可後）graph 授權尺寸 |
| `DESIGN.md`、`content_scripts/_audit/VISUAL-FRAME-RUBRIC.md`、`REBUILD_STATUS.md` | 文檔（Phase 1、各 phase 收尾） |

---

## Phase 0-a：A/B 定案輪（唯一的使用者 sign-off 閘在 Task 7）

### Task 1：渲染 baseline 靜幀（改動前）

**Files:** 無（只產 gitignored 輸出）

- [ ] **Step 1:** 確認分支與樹況：`git status`（記下既有未 commit 檔清單，本計畫不碰它們）。
- [ ] **Step 2:** 渲染 5 個代表景 baseline：

```bash
cd video
python scratch_frames.py --storyboard storyboards/ch03_trig_derivatives.yml \
  --scene divider_limit,difference_quotient_for_sine,sector_inequality,squeeze_graph,slope_equals_height \
  --out output/_qa/step0_ab/base
```

Expected: `output/_qa/step0_ab/base/` 出 5 張 1920×1080 PNG。（MiKTeX transient 失敗→重跑。）

### Task 2：P-A1＋G2——graph 標籤字級＋亮度地板（同一 patch）

**Files:**
- Modify: `pipeline/templates/graph.py`（`default_label_size` 一處＋3 個 label call site＋新 helper）
- Create: `pipeline/_selftest_graph_labels.py`

- [ ] **Step 1: 寫 failing selftest**

```python
"""Self-test: graph carrier-label role floor (P-A1/G2). Run from video/:
    python -m pipeline._selftest_graph_labels
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # graph.py top-level imports manim -- bootstrap FIRST (repo rule)

from pipeline.templates.graph import _carrier_label_role


def test_explicit_label_role_wins():
    # 作者顯式 label_role（即使是 muted）→ 尊重不動（覆蓋權，P6 warn-default 精神）
    assert _carrier_label_role({"label_role": "muted", "color_role": "blue"}) == "muted"


def test_inherited_dim_floors_to_text():
    # 繼承路徑：暗曲線（muted）的標籤升到 ink_2（"text"），曲線本身不動
    assert _carrier_label_role({"color_role": "muted"}) == "text"


def test_inherited_bright_kept():
    assert _carrier_label_role({"color_role": "amber"}) == "amber"


def test_default_secondary():
    assert _carrier_label_role({}) == "secondary"


if __name__ == "__main__":
    import sys, traceback
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS {name}")
            except Exception:
                fails += 1; print(f"FAIL {name}"); traceback.print_exc()
    sys.exit(1 if fails else 0)
```

- [ ] **Step 2:** `python -m pipeline._selftest_graph_labels` → Expected: FAIL（`_carrier_label_role` 不存在）。
- [ ] **Step 3: 實作。** `graph.py` 的 `_label()` 定義前加：

```python
# Carrier-label luminance floor (G2, 2026-07-05): a curve label INHERITS its curve's
# colour by default -- correct for bright accents, but a de-emphasised curve (muted /
# hairline grey) dragged its identity label below legibility (s3.1 frame 10 "cos t"
# nearly invisible). The curve may stay dim; its LABEL floors to ink_2 ("text").
# An explicit label_role is the author's override and is respected untouched.
_DIM_LABEL_ROLES = {"muted", "subtitle", "ink_3", "ink_faint",
                    "hairline", "hairline_strong", "hairline_faint", "grid_line"}


def _carrier_label_role(plot: dict) -> str:
    explicit = plot.get("label_role")
    if explicit is not None:
        return str(explicit)
    role = str(plot.get("color_role", "secondary"))
    return "text" if role in _DIM_LABEL_ROLES else role
```

**兩個「繼承曲線色」的 label call site**（function curve 與 line，grep `label_role.*color_role`）把

```python
role=plot.get("label_role", str(plot.get("color_role", "secondary"))),
```

改成

```python
role=_carrier_label_role(plot),
```

**第三處（point 讀數標籤，約 L350）不動**——它的現行預設是 `plot.get("label_role", "text")`（本來就 ink_2 地板、不繼承曲線色），套 `_carrier_label_role` 反而會把無 `color_role` 的 point 標籤預設從 text 改成 secondary＝行為倒退。（point 標籤的**字級**仍吃 `default_label_size` 的 30→math_sm 升級，正確。）

`default_label_size` 那行（約 L238）：

```python
default_label_size = str(ac.get("label_size", "math_sm"))   # was "label" (30px) -- carrier >= ticks (P-A1)
```

- [ ] **Step 4:** `python -m pipeline._selftest_graph_labels` → Expected: 4× PASS。
- [ ] **Step 5: Commit**

```bash
git add pipeline/templates/graph.py pipeline/_selftest_graph_labels.py
git commit -m "feat(video): graph carrier labels — default math_sm + luminance floor (P-A1/G2)"
```

### Task 3：P-A2——`tag` token、result 理由 tag、clamp px 分派、part 頁碼

**Files:**
- Modify: `pipeline/visuals/theme.py`（_SCALE_PX）、`pipeline/brand.py`（eyebrow）、`pipeline/templates/derivation.py`（_reason_mob＋clamp pre-pass）、`pipeline/templates/_common.py`（scene_head／example_head 的 part 頁碼）

- [ ] **Step 1:** `theme.py` `_SCALE_PX` 的 `"caption": 30, "eyebrow": 26,` 後插入：

```python
    "tag": 30,   # mono nav/emphasis tag: derivation result-reason + part pager (was eyebrow=26 == floor; A/B may settle 32)
```

- [ ] **Step 2:** `brand.py` `eyebrow()` 簽名與 font_size：

```python
def eyebrow(label: str, ground: str, *, role: str = "secondary", size="eyebrow") -> Tex:
```

（docstring 尾補一句：`*size* is a scale token or raw px -- "tag" for the result-reason / pager tier.`）
`font_size=_text_fs("eyebrow")` → `font_size=_text_fs(size)`。

- [ ] **Step 3:** `derivation.py` 模組頂（`_ROW_GAP` 旁）加單一 authored-px 源，並改 `_reason_mob` 兩分支——**authored size 與 clamp floor 必須同源**（Plan 4 durable 教訓「clamp↔lint px 必須對齊」；A/B 若拍板 reason 38 只改這一個常數）：

```python
_REASON_PX = T._SCALE_PX["prose_sm"]   # 一般 reason 的 authored px（A/B 開放值：35 或 38）
```

```python
    if row["kind"] == "result":
        return brand.eyebrow(str(reason), ground, role="amber_ink", size="tag")
```

（一般分支 `brand.prose(str(reason), ground, role="text", size="prose_sm")` 改 `size=_REASON_PX`——raw px 走同一 `fs()` 轉換，35 時 byte-equivalent。）

- [ ] **Step 4:** `derivation.py` clamp pre-pass（`if reason is not None and reason.width > reason_max_w > 0:` 區塊）改為按 kind 分派、同源常數、並更新該處 NOTE 註解（原「SP2 已知落差」已閉）：

```python
        if reason is not None and reason.width > reason_max_w > 0:
            # px dispatched by row kind, SAME SOURCE as the authored sizes above: a result
            # reason is an eyebrow at "tag", everything else at _REASON_PX -- keeps the clamp
            # floor equal to the authored px (closes the SP2 note; and an A/B re-tune of
            # _REASON_PX can never drift away from this guard).
            floor_px = T._SCALE_PX["tag"] if r["kind"] == "result" else _REASON_PX
            brand._clamp_shrink(reason, reason_max_w, floor_px)
```

- [ ] **Step 5:** `_common.py` 兩處 part 頁碼（`scene_head` 與 `example_head` 內 `pind = brand.eyebrow(_part_text(part), ground, role=role)`）改為：

```python
        pind = brand.eyebrow(_part_text(part), ground, role=role, size="tag")
```

- [ ] **Step 6: 驗證（build 級）：** 從 `video/` 跑一次快檢（Tex 需 LaTeX，本機有）：

```bash
python -c "import pipeline._bootstrap as B; B.bootstrap(); B.apply_tex_template(); import pipeline.brand as brand; from pipeline.visuals import theme as T; e=brand.eyebrow('1 / 2','dark',size='tag'); import math; assert math.isclose(e.font_size, T.fs('tag')*T.TEXT_SCALE, rel_tol=1e-6), e.font_size; print('tag size OK')"
```

Expected: `tag size OK`。（`bootstrap()`／`apply_tex_template()` 皆零參數，已驗簽名；從 `video/` 執行。）
再跑 `python -m pipeline.sizecheck storyboards/ch03_trig_derivatives.yml` → Expected: 0 error（tag 30 > floor 26，floor check 不觸發）。

- [ ] **Step 7: Commit**

```bash
git add pipeline/visuals/theme.py pipeline/brand.py pipeline/templates/derivation.py pipeline/templates/_common.py
git commit -m "feat(video): 'tag' scale token — result-reason + part pager 26->30, clamp px by kind (P-A2)"
```

### Task 4：P-A3——divider hook 式專用字級

**Files:** Modify: `pipeline/templates/_common.py`（render_scaffold）、`pipeline/templates/divider.py`

- [ ] **Step 1:** `render_scaffold` 簽名加 keyword-only 參數並用於 problem：

```python
def render_scaffold(scaffold, ground, meta=None, *, problem_size="prose") -> list[Block]:
```

problem 那行：

```python
        mob = brand.prose(problem, ground, role="text", size=problem_size,
                          max_width=CONTENT_W, align="LEFT")
```

（docstring 補：`*problem_size*: divider passes 56 so a pure-$math$ hook (-> MathTex path, no TEXT_SCALE) reads ABOVE the subtitle instead of ~80% of it; every other template keeps "prose".`）

- [ ] **Step 2:** `divider.py` 呼叫處：

```python
    scaffold_blocks = render_scaffold(spec.get("scaffold"), ground, ctx.get("meta"), problem_size=56)
```

- [ ] **Step 3: 驗證：** 其他 caller（theorem_proof／derivation／definition_math）不傳 → 預設不變。`python -m pipeline.sizecheck storyboards/ch03_trig_derivatives.yml` → 0 error。
- [ ] **Step 4: Commit** — `git add pipeline/templates/_common.py pipeline/templates/divider.py && git commit -m "feat(video): divider hook formula at 56px via render_scaffold problem_size (P-A3)"`

### Task 5：P-A4——進度點放大

**Files:** Modify: `pipeline/brand.py`（progress_dots 預設值）

- [ ] **Step 1:** `def progress_dots(current, total, ground, *, role="accent", gap: float = 0.34, r: float = 0.052)` → `gap: float = 0.44, r: float = 0.07`（14px→19px；pill 內部以 r 為基準自動同比）。
- [ ] **Step 2: Commit** — `git add pipeline/brand.py && git commit -m "feat(video): divider progress dots 14px -> 19px (P-A4)"`

### Task 6：P-C——graph 預設繪圖區（僅未覆寫景受影響）

**Files:** Modify: `pipeline/templates/graph.py`（兩組預設值）

- [ ] **Step 1:** 單圖（約 L405）`6.35`→`8.0`、`4.15`→`4.6`；compare（約 L487）`4.6`→`5.2`、`3.2`→`3.6`。各留註解 `# default raised toward the P5 zone ceiling (2026-07-05); _fit_graph_to_safe_zone still caps to the zone`。
- [ ] **Step 2: 驗證（注意覆蓋面）：** `_demo_graph_reveal`／`_demo_asymptote`／`_demo_label_overlap` 都有 explicit `x_length/y_length`——**吃得到新預設的只有 `_demo_graph_compare`（compare 預設）**；single 預設由 Task 13 的 `_demo_graph_muted.yml`（刻意不寫 x/y_length）補上覆蓋。本步跑：

```bash
python -m pipeline.sizecheck storyboards/_demo_graph_compare.yml
python -m pipeline.sizecheck storyboards/_demo_graph_reveal.yml
```

Expected: 全部 0 error（前者驗 compare 新預設不溢出——auto-scale 保證；後者驗 explicit 尺寸景不受影響）。single 新預設的驗證掛在 Task 13 Step 2。**ch01/ch03 真 deck 全部逐景覆寫尺寸，此改動不影響現有幀（提案已誠實標註）。**
- [ ] **Step 3: Commit** — `git add pipeline/templates/graph.py && git commit -m "feat(video): graph default plot area 6.35x4.15 -> 8.0x4.6 (compare 5.2x3.6) (P-C)"`

### Task 7：A/B 變體渲染＋對照頁 →【使用者 sign-off 閘】

**Files:** 無版控檔（輸出全在 gitignored `output/_qa/step0_ab/`）

- [ ] **Step 1:** 渲染「提案值」變體（Tasks 2–6 已落地）：同 Task 1 指令、`--out output/_qa/step0_ab/typepass`。
- [ ] **Step 2:** 開放值變體（每個：暫改→渲染→`git checkout --` 還原）：
  - **V-ticks35**：`graph.py` 兩處刻度 `size="math_sm"`→`size=35`（軸名 x/y 不動）→ 渲 `sector_inequality,squeeze_graph,slope_equals_height` → `--out .../ticks35` → 還原。
  - **V-tag32**：`theme.py` `"tag": 30`→`32` → 渲 `difference_quotient_for_sine` → `--out .../tag32` → 還原。
  - **V-reason38**：`derivation.py` `_REASON_PX`→`38`（單一常數，authored＋clamp 同步）→ 渲 `difference_quotient_for_sine` → `--out .../reason38` → 還原。
  - **V-h1_68**：`theme.py` `"h1": 78`→`68` → 渲 `difference_quotient_for_sine,squeeze_graph` → `--out .../h1_68` → 還原。
  - **V-authored**（開放問題 4，§3.1 單景尺寸順路 A/B）：storyboard `squeeze_graph` `x_length: 6.4/y_length: 3.6`→`8.0/4.2`、`slope_equals_height` `7.2/4.0`→`8.4/4.4` → 渲這兩景 → `--out .../authored` → 還原 storyboard。
- [ ] **Step 3:** 產 A/B 對照頁 `output/_qa/step0_ab/REVIEW-step0-typepass-AB.html`：每景一列、base vs typepass（＋各開放值變體欄）並排 `<img>`，欄標清楚；表尾列裁決欄（tag 30/32、ticks 40/35、reason 35/38、h1 78/68、authored 尺寸 採/不採）。
- [ ] **Step 4:**【**STOP——使用者 sign-off**】把對照頁交使用者裁決五個開放值。**未裁決不得進 Task 8。**
- [ ] **Step 5:** 按裁決把定案值寫進 code——每個開放值都是**單點修改**：tag→`theme._SCALE_PX["tag"]`；ticks→`graph.py` 兩處刻度 size；reason→`derivation._REASON_PX`（clamp 自動同步）；h1→`theme._SCALE_PX["h1"]`；authored 尺寸→storyboard 兩景。一個收束 commit：`fix(video): apply step0 A/B verdicts (<列出定案值>)`。

### Task 8：Step 0-b 全回歸＋re-baseline

- [ ] **Step 1:** 三 deck 靜態閘：

```bash
for f in ch01_inverse_functions ch03_trig_derivatives ch03_chain_rule; do
  python -m pipeline.schema    storyboards/$f.yml
  python -m pipeline.lint      storyboards/$f.yml
  python -m pipeline.sizecheck storyboards/$f.yml
done
```

Expected: schema/lint 照舊；sizecheck 0 error（既有 within-frame advisory 容許；**新增 warn 逐條人工判**——tag/標籤變大可能移動 clamp 邊界）。
- [ ] **Step 2:** `python capacity_selftest.py` → Expected: 全綠。若因字級改動位移 EXPECT 邊界：逐條記錄理由後 re-baseline（EXPECT 表同 commit 說明）。
- [ ] **Step 3:** 全景重渲兩 deck 靜幀：`scratch_frames.py --scene all` 各 deck → `output/_qa/step0_regression/<deck>/`。
- [ ] **Step 4:** 對 **graph 場景幀**（§3.1 的 sector_inequality／squeeze_graph／slope_equals_height／shm_stacked_graphs＋ch01 的 graph 景）dispatch `visual-frame-audit` gate-1 agent → Expected: **V blocking = 0**（A 級記錄即可）。特別驗：標籤 40px 後無 label-vs-label／label-vs-curve 新壓線（agent V4/V6 會看；另跑 `python -m pipeline.sizecheck` 的 graph label overlap advisory 汇总）。
- [ ] **Step 5:** 產 sign-off 紀錄頁 `output/_qa/REVIEW-step0-applied.html`（每個改動元素 before/after 並排＋定案值表＋回歸結果摘要），交使用者過目（紀錄性，不擋後續 phase）。
- [ ] **Step 6:** `REBUILD_STATUS.md` 加「Step 0 落地」entry（含定案值、commits、回歸結論）。Commit：`docs(video): REBUILD_STATUS — step0 type pass landed`。

---

## Phase 1（=v2 Step A）：文檔——Playbook＋語域規則＋量測表

### Task 9：DESIGN.md＋VISUAL-FRAME-RUBRIC

**Files:** Modify: `DESIGN.md`、`content_scripts/_audit/VISUAL-FRAME-RUBRIC.md`

- [ ] **Step 1:** `DESIGN.md`「Display-style 慣例（2026-06-29）」節的 inline 位置表列擴充——把該表第二列改為：

```markdown
| inline 位置（`title`・`prompt`・`body`（callout）・`points[]`（recap）・`scaffold.motive`・`reason`（含 `steps[].reason`）・`say`・table cell・axis label） | `\tfrac`／slash form／inline `\lim` | 顯式覆蓋回 text-size；display 級分數與堆疊上下標只進 display 欄位 |
```

並在節尾補一段：

```markdown
**G1 執法（2026-07-05）：** 上表由 `pipeline/lint.py` 的 `_display_math_in_inline` advisory 靜態執法
（掃 inline 欄位 `$...$` 內的 `\frac`/`\dfrac`/`\lim_`/`\sum_`/`\int_`）。display 欄位
（`statement`/`math`/`proof`/`formulas`/`scaffold.problem`）**不掃**。罕例真要 display 可無視 warn。
```

- [ ] **Step 2:** `DESIGN.md`「Template 選擇：離散步驟 vs 推導鏈」節之後新增完整節（內容即下表，照抄）：

```markdown
### Authoring Playbook：內容形狀 → 模板 → 單頁容量預算 → 超量／稀疏動作（2026-07-05 拍板）

寫 storyboard 時對照選模板、預估分頁；寫完跑 schema→lint→sizecheck→mock render→visual gate 即收斂。
預算與 `_demo_capacity.yml`／`capacity_selftest.py` 的 fit/over EXPECT 對齊，fixture 調整需同步本表。

| 內容形狀 | 模板 | 單頁容量預算 | 超量動作（DENSE） | 稀疏動作（SPARSE） |
|---|---|---|---|---|
| 連續推導鏈 | `derivation` | fraction 列：無 statement ~5、有 statement ~4；single 列 ~7 | 按邏輯階段切 `part:`，不硬切等號 | fill_gap 自動；勿加廢列 |
| 陳述＋符號式 | `definition_math` | statement ≤3 行＋math ≤4 列 | 拆 part 或把長鏈改 derivation 景 | 掛 `aside` 卡（L3） |
| 命題＋證明 | `theorem_proof` | proof ≤4 步＋qed（一般步 2–3；fraction 步更保守） | >4 步拆 statement＋proof 兩場、超頁 `part:` | statement-only 走 card＋aside 兩欄 |
| 離散步驟 | `procedure_steps` | 3–4 步、math ≤5u 寬 | 拆 part；長式改 derivation | ——（步驟自然 ≥3） |
| 單句警示／評註 | `callout` | 條列 2–4 點或段落 ≥3 行 | 條列砍到 ≤4 點 | G3 三出口：條列化／併景／`sparse_ok` |
| 函數圖／幾何圖 | `graph` | 圖主導：x 以 8.0u 起手、y 交 `_fit_graph_to_safe_zone` 封頂；有 caption band 時被自動縮回是預期行為；A7 量測為最終裁判；標籤走 carrier≥刻度＋亮度地板 | 拆 reveal beats（`{show plot.N}`） | 放大圖填版（P5 正向） |
| 數值對照 | `value_table` | ~5×3 格 | 砍列（教學點優先） | —— |
| 正負號分析 | `sign_chart` | 1 軸＋≤4 區 | —— | —— |
| 總結要點 | `recap_cards` | 4–5 點 | 砍點（recap 不拆頁） | —— |
| 章節轉場 | `divider` | title＋hook 式（56px）＋一句 subtitle | —— | —— |

**G3 稀疏出口（單塊 prose 場景）：** callout（字串 body）／definition_math（statement-only）實測佔 body zone
<35% 時 sizecheck advisory 提示三出口——① 條列化（callout body 用 list 形式）；② 併景（掛相鄰場景
`scaffold.flag`／`aside`）；③ `sparse_ok: true` 接受留白（pull-quote 式刻意孤句合法；render 不讀此欄位，
僅 sizecheck 讀＝advisory ack，非 magic boolean）。

**G4 卡片孤字：** aside／rail statement 的 prose 尾端孤 math token（frame 07 的孤 `$x_0$`）由 lint advisory
提示，修法＝改寫文案（如 `at every point $x_0$.`）。**不用 `~`**——`brand._escape_tex` 會把它印成可見波浪號。
```

- [ ] **Step 3:** `DESIGN.md` 排版（Text rendering）區塊後新增「型階與量測表（2026-07-05 體檢存檔）」節，內容四張表照抄提案：
  1. 型階承載表（112 hero＝無 call site 保留；92 divider；78 h1；58 h2；54 result；48 math；44 h3；42 prose/step；40 math_sm＝刻度/軸名；35 prose_sm＝reason rail/aside；30 tag 前身 label＝**graph 標籤已升 math_sm**；30 tag（新）；26 eyebrow=floor）；
  2. **數學三路徑表**（MathTex＝px×0.698 基準｜inline-in-prose＝×1.3102＝+31%｜inline-in-heading 同＋HEADING_MATH_SCALE=1.0）＋divider hook 案例一句；
  3. 縱向節奏 token 表（EYEBROW_GAP 22／TITLE_GAP 56／LINE_GAP 28／ROW_GAP 44／derivation 54／definition 48.6&95.9／theorem 67.5／procedure 等 1.25/0.95/1.4u／recap 47——「有壓測紀錄、不重構」）；
  4. 行長量測法（權威＝`brand._WIDTH_K=0.00507`＋CJK×2；CONTENT_W≈65 加權字元＝可讀上緣；**勿再用 0.5em 粗估**）。
- [ ] **Step 4:** `VISUAL-FRAME-RUBRIC.md` V4 節補一句（sharpen 既有維度、不立新 code）：

```markdown
- **carrier 標籤（曲線／直線／點讀數的身份與數值標籤）**：亮度低於 ink_2 或字級低於刻度數字
  （「carrier ≥ 刻度」階序）——承載值不可讀 → V4 blocking；可辨但弱 → A6 扣分。
```

- [ ] **Step 5: Commit** — `docs(video): DESIGN playbook + register/type tables; rubric carrier-label rule (v2 Step A)`

---

## Phase 2（=v2 Step B）：lint 靜態閘——G1＋G4

### Task 10：G1 `_display_math_in_inline`

**Files:** Modify: `pipeline/lint.py`；Create: `storyboards/_demo_registers.yml`、`pipeline/_selftest_lint_registers.py`

- [ ] **Step 1: fixture（作為 failing 驗收）**——`storyboards/_demo_registers.yml`：

```yaml
# G1/G4 register-lint probes (demo fixture, underscore prefix = not a real section)
meta:
  id: demo_registers
  chapter: "Demo"
  chapter_title: "Template Validation"
  section: "0.0"
  title: "Register Lint Demo"
  language: en
  theme: midnight
  voice: Kore
  video: { w: 1920, h: 1080, fps: 30 }
  sections:
    - { id: "0.0", title: "Register Lint Demo" }

scenes:
  - id: bad_title
    kind: content
    template: definition_math
    title: "The limit $\\lim_{x\\to0}\\frac{\\sin x}{x}$"
    math: ["$\\frac{\\sin x}{x}$"]          # display 欄位用 \frac —— 必須不觸發
    say: "probe. {show math.0}"
  - id: bad_callout
    kind: content
    template: callout
    type: caution
    title: "A trap"
    body: "At $\\theta=\\pi$ the ratio $\\frac{\\sin\\theta}{\\theta}$ is zero."
    say: "probe."
  - id: clean_scene
    kind: content
    template: callout
    type: remark
    title: "Fine"
    body: "Here $\\sin\\theta/\\theta$ and $\\tfrac{d}{dx}\\sin x$ stay textstyle."
    say: "probe."
```

- [ ] **Step 2: selftest** `pipeline/_selftest_lint_registers.py`：

```python
"""Self-test: G1 display-math-in-inline-register lint. Run from video/:
    python -m pipeline._selftest_lint_registers
"""
from pathlib import Path
from pipeline.lint import lint_file

FIX = Path(__file__).resolve().parent.parent / "storyboards"


def test_flags_title_and_callout_body_but_not_display_fields():
    msgs = [m for sev, m in lint_file(FIX / "_demo_registers.yml") if "inline register" in m.lower()]
    assert any("bad_title" in m for m in msgs), msgs
    assert any("bad_callout" in m for m in msgs), msgs
    assert not any("clean_scene" in m for m in msgs), msgs
    # display 欄位不觸發：訊息開頭是 "<sid>.<path>: ..."，取第一個冒號前的 path 檢查
    paths = [m.split(":", 1)[0] for m in msgs]
    assert not any(".math" in p or "math[" in p for p in paths), paths


def test_negative_control_derivation_lines():
    # _demo_derivation.yml 的 lines[]（display 欄位）滿是 \frac —— 必須零觸發
    msgs = [m for sev, m in lint_file(FIX / "_demo_derivation.yml") if "inline register" in m.lower()]
    assert msgs == [], msgs


if __name__ == "__main__":
    import sys, traceback
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS {name}")
            except Exception:
                fails += 1; print(f"FAIL {name}"); traceback.print_exc()
    sys.exit(1 if fails else 0)
```

（`lint_file` 回傳形狀以現檔為準——若是 `(severity, message)` 以外的形狀，測試同形調整。）
- [ ] **Step 3:** `python -m pipeline._selftest_lint_registers` → Expected: FAIL（rule 不存在）。
- [ ] **Step 4: 實作**——`lint.py` 加 rule，掛載＝`lint_storyboard()` 尾端照既有模式追加一行 `issues += _display_math_in_inline(data)`（現行尾端是 `_hollow_on_curve`／`_quantitative_without_scale`／`_example_missing_prompt`／`_scene_role_issues` 四行 `issues +=`）：

```python
_DISPLAY_IN_INLINE = re.compile(r"\\(?:d?frac(?![a-zA-Z])|lim_|sum_|int_)")

# G1 (2026-07-05): inline registers must stay textstyle -- the preamble's
# \everymath{\displaystyle} makes $\frac$ render display-height, so a stacked fraction
# in a title/prose line bulges the line box (s3.1 frames 11/12/19/25). Display FIELDS
# (statement/math/proof/formulas/scaffold.problem) keep \frac by contract -- not scanned.
def _inline_register_strings(data):
    out = []
    for i, sc in enumerate(data.get("scenes", []) or []):
        sid = sc.get("id", f"scene{i}")
        def add(path, val):
            if isinstance(val, str) and val.strip():
                out.append((f"{sid}.{path}", val))
        add("title", sc.get("title"))
        add("prompt", sc.get("prompt"))
        add("say", sc.get("say"))
        body = sc.get("body")
        if isinstance(body, str):
            add("body", body)
        elif isinstance(body, (list, tuple)):
            for j, item in enumerate(body):
                add(f"body[{j}]", item if isinstance(item, str) else None)
        for j, item in enumerate(sc.get("points", []) or []):
            add(f"points[{j}]", item if isinstance(item, str) else None)
        sca = sc.get("scaffold") or {}
        if isinstance(sca, dict):
            add("scaffold.motive", sca.get("motive"))
        for j, st in enumerate(sc.get("steps", []) or []):
            if isinstance(st, dict):
                add(f"steps[{j}].reason", st.get("reason"))
        for key in ("result", "check"):
            v = sc.get(key)
            if isinstance(v, dict):
                add(f"{key}.reason", v.get("reason"))
        for j, ln in enumerate(sc.get("lines", []) or []):
            if isinstance(ln, dict):
                add(f"lines[{j}].reason", ln.get("reason"))
    return out


def _display_math_in_inline(data) -> "list[tuple[str, str]]":
    issues = []
    for path, s in _inline_register_strings(data):
        for m in re.finditer(r"\$([^$]+)\$", s):
            if _DISPLAY_IN_INLINE.search(m.group(1)):
                issues.append(("warn",
                    f"{path}: display-style math in an INLINE register ({_snippet(m.group(0))}) "
                    f"-- use \\tfrac / slash form / inline lim (DESIGN.md display-style)"))
                break
    return issues
```

- [ ] **Step 5:** selftest → Expected: 全 PASS。三真 deck 跑 lint：`§3.1 命中 limit_not_identity.body／radians_essential.body／companion_limit.prompt／recap.points`（±既有 say 命中——say 屬 inline 契約，照 warn）；其他命中逐一人工判非誤報。
- [ ] **Step 6: §3.1 示範修正（4 處，僅上畫面欄位、不動語意→NFA 不重開）：** 在 `storyboards/ch03_trig_derivatives.yml`
  - `companion_limit` 的 `prompt`：`\lim...\frac{1-\cos\theta}{\theta} = 0` 形 → `Establish the companion limit $(1-\cos\theta)/\theta \to 0$ as $\theta \to 0$.`
  - `limit_not_identity.body`：`$\frac{\sin\theta}{\theta}$`→`$\sin\theta/\theta$`；`$\frac{2}{\pi}$`→`$2/\pi$`
  - `radians_essential.body`：兩個 display 分數→`$\sin(x^\circ)/x \to \pi/180$` 與 `$\tfrac{d}{dx}\sin(x^\circ)=\tfrac{\pi}{180}\cos(x^\circ)$`
  - `recap.points[0]`：`$\lim_{\theta\to0}\sin\theta/\theta = 1$`（slash 形）
  （以 grep 找現行字串，保住原句語序；改完 lint 對這 4 處歸零、`scratch_frames` 渲 4 景眼檢行距復原。）
- [ ] **Step 7: Commit ×2** — `feat(video): lint G1 — display math in inline registers (advisory)`；`fix(video/ch03): s3.1 textstyle in inline registers (G1 demo, visual-only)`

### Task 11：G4 `_card_widow_issues`

**Files:** Modify: `pipeline/lint.py`、`storyboards/_demo_registers.yml`（加 2 景）、`pipeline/_selftest_lint_registers.py`（加 2 測）、`storyboards/ch03_trig_derivatives.yml`（1 處示範）

- [ ] **Step 1:** fixture 加：

```yaml
  - id: widow_aside
    kind: content
    template: definition_math
    title: "Widow probe"
    statement: "A statement."
    aside: { label: "key idea", body: "This function is continuous at every $x_0$." }
    say: "probe."
  - id: widow_ok
    kind: content
    template: definition_math
    title: "No widow"
    statement: "A statement."
    aside: { body: "Continuity holds at every point $x_0$ of the domain." }
    say: "probe."
  - id: widow_statement
    kind: content
    template: theorem_proof
    title: "Rail widow probe"
    statement: "If $f$ is strictly monotone on an interval then it is one-to-one at $x_0$"
    proof: ["Take $x_1 < x_2$ in the interval.", "Monotonicity gives $f(x_1) \\ne f(x_2)$."]
    qed: "Therefore $f$ is one-to-one."
    say: "probe. {show proof.0} {show proof.1} {show qed}"
  - id: widow_statement_ok
    kind: content
    template: theorem_proof
    title: "Rail formula (no scan)"
    statement: "$\\tfrac{d}{dx}\\sin x = \\cos x$"
    proof: ["From the difference quotient.", "Apply the fundamental limit."]
    qed: "Hence the derivative."
    say: "probe. {show proof.0} {show proof.1} {show qed}"
```

- [ ] **Step 2:** selftest 加：

```python
def test_widow_flags_lone_trailing_math_token():
    msgs = [m for sev, m in lint_file(FIX / "_demo_registers.yml") if "widow" in m.lower()]
    assert any("widow_aside.aside" in m for m in msgs), msgs
    assert any("widow_statement.statement" in m for m in msgs), msgs       # rail statement 卡（prose 形）
    assert not any("widow_ok" in m for m in msgs), msgs
    assert not any("widow_statement_ok" in m for m in msgs), msgs          # 純 $formula$ 卡不掃
```

- [ ] **Step 3:** 實作（同 Task 10 掛載法：`lint_storyboard()` 尾端追加 `issues += _card_widow_issues(data)`）：

```python
# G4 (2026-07-05): a card's prose that ENDS on a lone short/math token tends to wrap the
# token onto its own last line (s3.1 frame 07's lone $x_0$). Advisory: reword the tail
# (e.g. "at every point $x_0$."). Card registers = aside bodies + theorem's rail statement
# (prose form only -- a pure-$formula$ statement centres in the card and never wraps).
def _widow_tail(text: str) -> "str | None":
    """The lone trailing short/math token if *text* risks a widow line, else None."""
    words = text.strip().rstrip(".,;:!?").split()
    if len(words) < 8:
        return None
    last = words[-1]
    if re.fullmatch(r"\$[^$]+\$", last) or len(last) <= 4:
        return last
    return None


def _card_widow_issues(data) -> "list[tuple[str, str]]":
    issues = []
    for i, sc in enumerate(data.get("scenes", []) or []):
        sid = sc.get("id", f"scene{i}")
        cards = []
        aside = sc.get("aside")
        body = aside.get("body") if isinstance(aside, dict) else aside
        if isinstance(body, str):
            cards.append(("aside", body))
        stmt = sc.get("statement")
        if (sc.get("template") == "theorem_proof" and isinstance(stmt, str)
                and not re.fullmatch(r"\s*\$[^$]+\$\s*", stmt)):   # prose statement only
            cards.append(("statement", stmt))
        for field, text in cards:
            last = _widow_tail(text)
            if last is not None:
                issues.append(("warn",
                    f"{sid}.{field}: ends on a lone short/math token ('{last}') -- likely "
                    f"widow line in the card; reword the tail (e.g. 'at every point {last}.')"))
    return issues
```

- [ ] **Step 4:** selftest 全 PASS；三 deck 跑 lint 記錄命中。
- [ ] **Step 5: §3.1 示範**——`continuity_statement_sin_limit` 的 aside body：grep `continuous at every`，改為 `... are continuous at every point $x_0$.`（visual-only；refs／`[source:]` 不動）。渲該景眼檢孤字消失。
- [ ] **Step 6: Commit** — `feat(video): lint G4 — card widow advisory; s3.1 aside reworded`

---

## Phase 3（=v2 Step C）：sizecheck 量測閘——G3 稀疏出口

### Task 12：`_sparse_issues`＋fixtures＋門檻校準

**Files:** Modify: `pipeline/sizecheck.py`、`storyboards/_demo_capacity.yml`、`capacity_selftest.py`

- [ ] **Step 1: fixture**——`_demo_capacity.yml` 加兩景（照該檔既有 meta/scene 形式）：

```yaml
  - id: callout_sparse
    kind: content
    template: callout
    type: remark
    title: "Sparse probe"
    body: "One short sentence."
    say: "probe."
  - id: callout_sparse_ok
    kind: content
    template: callout
    type: remark
    title: "Sparse but intended"
    body: "One short sentence."
    sparse_ok: true
    say: "probe."
```

（`sparse_ok` 是新 scene 欄位——schema.py 無 scene key 白名單（已 grep 驗證無 ALLOWED/unknown-key 檢查），可直接通過；G3 設計本義＝只有 sizecheck 讀它。）

- [ ] **Step 2: 實作**——`sizecheck.py`（放 `_capacity_issues` 旁、同簽名慣例）：

```python
SPARSE_FILL_MIN = 0.35   # G3: single-block content below this fraction of the body zone -> advisory

# G3 (2026-07-05): fill_gap needs n>=2 rows -- a SINGLE prose block (callout string body,
# statement-only definition) has no inter-row gap to open, so a one-liner strands ~half the
# zone (s3.1 frames 11/12/24). Advisory only; `sparse_ok: true` is the author's ack (read
# HERE only -- render never reads it, so it is not a render-behaviour flag).
def _sparse_issues(scene: dict, blocks) -> "list[tuple[str, str]]":
    from pipeline.visuals import theme as T   # sizecheck has no module-level T (helpers import locally)

    if scene.get("sparse_ok"):
        return []
    tpl = scene.get("template")
    if tpl == "callout" and isinstance(scene.get("body"), str):
        target = "body"
    elif tpl == "definition_math" and scene.get("statement") and not scene.get("math"):
        target = "statement"
    else:
        return []
    title = next((b.mobject for b in blocks if getattr(b, "id", "") == "title"), None)
    mob = next((b.mobject for b in blocks if getattr(b, "id", "") == target), None)
    if title is None or mob is None:
        return []
    zone_top = title.get_bottom()[1] - T.TITLE_GAP
    zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN
    ratio = mob.height / max(zone_top - zone_bottom, 1e-6)
    if ratio >= SPARSE_FILL_MIN:
        return []
    sid = scene.get("id", "?")
    return [("warn",
        f"{sid}: single-block fill {ratio:.0%} < {SPARSE_FILL_MIN:.0%} of body zone -- exits: "
        f"(a) bullet the body (list form), (b) merge into a neighbour (scaffold.flag/aside), "
        f"(c) `sparse_ok: true` to accept the calm whitespace")]
```

掛進 `check_scenes` 與 `_capacity_issues` 同一迭代點。
- [ ] **Step 3: EXPECT**——**注意：既有 `EXPECT` 表的判定字串是拆頁 warn（`"fit on one page"`），sparse warn 塞不進去**；在 `capacity_selftest.py` 加一張副表與 matcher（放 `EXPECT` 之後、`main()` 內迴圈之後照樣跑一輪）：

```python
# G3 sparse advisory (single-block fill < SPARSE_FILL_MIN) -- separate matcher from the
# split warn: EXPECT keys assert "fit on one page", these assert "single-block fill".
SPARSE_EXPECT = {
    "callout_sparse": True,
    "callout_sparse_ok": False,   # sparse_ok: true acks the advisory -> silent
}


def _has_sparse_warn(issues) -> bool:
    return any("single-block fill" in m for _sev, m in issues)
```

`main()` 內、既有迴圈後加同型迴圈（`missing` 檢查一併涵蓋 `SPARSE_EXPECT` 的 key）：

```python
    for sid, expect_warn in SPARSE_EXPECT.items():
        got_warn = _has_sparse_warn(check_scenes(meta, [by_id[sid]]))
        ok = got_warn == expect_warn
        mark = "ok  " if ok else "FAIL"
        print(f"  [{mark}] {sid:<18} sparse expect={expect_warn} got={got_warn}", flush=True)
        if not ok:
            failures += 1
```

最後把成功訊息的計數改成兩表合計（原本硬寫 `len(EXPECT)` 會印過期的「all 12」）：

```python
    total = len(EXPECT) + len(SPARSE_EXPECT)
    print(f"[capacity] all {total} scenes match the capacity contract.", flush=True)
```

跑 `python capacity_selftest.py`（cwd＝`video/`）→ 全綠（既有 12 條＋新 2 條，印 `all 14`）。
- [ ] **Step 4: 校準**——三真 deck 跑 sizecheck：Expected 命中 §3.1 `limit_not_identity`／`radians_essential`／`toward_the_chain_rule` 三景；ch01／ch03_chain 的命中逐一人工判。誤報過多才動 `SPARSE_FILL_MIN`（一常數、附理由 commit）。**不要順手改景**——那三景要不要收（條列化/併景/sparse_ok）是內容決策，列進 Task 14 backlog 交裁決。
- [ ] **Step 5: Commit** — `feat(video): sizecheck G3 — sparse single-block advisory + sparse_ok ack + fixtures`

---

## Phase 4（=v2 Step E）：回歸網收口

### Task 13：muted-label fixture＋canary＋全套自測

**Files:** Create: `storyboards/_demo_graph_muted.yml`；Modify: 無

- [ ] **Step 1:** fixture：

```yaml
# G2 carrier-label luminance-floor probe (demo fixture)
meta:
  id: demo_graph_muted
  chapter: "Demo"
  chapter_title: "Template Validation"
  section: "0.0"
  title: "Muted Label Demo"
  language: en
  theme: midnight
  voice: Kore
  video: { w: 1920, h: 1080, fps: 30 }
  sections:
    - { id: "0.0", title: "Muted Label Demo" }

scenes:
  - id: muted_curve_label
    kind: content
    template: graph
    accent: definition
    title: "Floor Probe"
    say: "probe."
    axes:
      x_range: [-3, 3, 1]
      y_range: [-2, 2, 1]
    plots:
      # 繼承路徑：暗曲線 -> 標籤應升 ink_2（G2 clamp 生效）
      - { kind: function, expression: "0.2*x*x - 1.5", color_role: muted, label: "$g(x)$" }
      # 顯式 label_role: muted -> 尊重不動（作者覆蓋權）
      - { kind: function, expression: "0.5*x", color_role: secondary, label: "$f(x)$", label_role: muted, label_side: down }
```

（plot 欄位名照 `_demo_graph_reveal.yml` 現行 schema：`kind: function` ＋ `expression:`；用多項式運算式避免函數名 eval 相依。）
- [ ] **Step 2:** `python -m pipeline.sizecheck storyboards/_demo_graph_muted.yml` build 通過；`scratch_frames` 渲 1 幀眼檢：cos 標籤亮（ink_2）、sin 標籤暗（作者顯式）。
- [ ] **Step 3: canary（故意破壞要會紅）**：暫時把 `_carrier_label_role` 的 return 改回 `role` → `python -m pipeline._selftest_graph_labels` 必 FAIL → 還原、再 PASS。
- [ ] **Step 4:** 全套自測跑一輪（graph_labels／lint_registers／capacity_selftest＋repo 既有 `_selftest_*` 受影響者）→ 全綠。
- [ ] **Step 5:** 產 `output/_qa/REVIEW-capacityv2-applied.html`（G1–G6 落地摘要＋lint/sizecheck 三 deck 命中表＋fixture 幀）交使用者過目；`REBUILD_STATUS.md` 加 v2 落地 entry。Commit：`feat(video): capacity v2 regression net — muted-label fixture + canary (G6)`＋`docs(video): REBUILD_STATUS — capacity v2 landed`。

---

## Phase 5：§3.1 單景 backlog（內容層；逐項 VLM 迴圈，可獨立排程）

### Task 14：單景項清單（每項：mock render → `visual-frame-audit` 0 blocking → VLM 複驗迭代）

依既有授權（「採納能讓影片更好的建議、VLM 複驗、迭代到完成」）逐項執行；單項不確定就 AskUserQuestion 裁決。hooks 在 `animations/ch03_trig_derivatives_hooks.py`，graph 場景 payload 在 storyboard。

| # | 景 | 規格 | 錨點 |
|---|---|---|---|
| 1 | `slope_equals_height`（16） | 三切點→cos 對應點加細虛線 connector（動畫時序：切線亮→虛線落→橘點亮）；`m=` 標籤貼各自切線端；三切線等長（以切點為中心裁）；讀值寫全稱 `\cos 0=1`／`\cos\frac{\pi}{2}=0`／`\cos\pi=-1`（消雙「0」混淆）；`y=\cos x` 標籤亮度隨 G2 已修 | hooks＋storyboard plots |
| 2 | `sector_inequality`（05） | 主圖放大（吃底部空帶；A/B 已試過的尺寸為準）；主圖內三區域用與右側 glyph 相同三色 fill 逐塊點亮（藍△OAB→橘扇→綠△OAC）、右側對應 glyph 同步亮；①②③ chip 錨進主圖對應區域；`\tan\theta` 標籤移 AC 段右外緣 | hooks |
| 3 | `derivative_cycle`（17） | 文字鏈改四節點環圖（方形環排列＋回繞箭頭，逐步點亮、第四步整環亮）；kicker 與 body 擇一收斂 | hooks（新小圖）＋storyboard 文案 |
| 4 | `shm_stacked_graphs`（23） | 兩虛線 guide 加 `t=\frac{\pi}{2}`／`t=\frac{3\pi}{2}` 標籤；三 panel 與虛線交點加 dot（旁白對應處逐點亮）；`s''=-s` 標籤錨 acceleration panel 右側 | hooks |
| 5 | `squeeze_graph`（10） | x 軸加 `\pm\frac{\pi}{2}` 兩刻度；`\tfrac{\sin\theta}{\theta}` 標籤移曲線上方空區（label_point） | storyboard |
| 6 | `toward_the_chain_rule`（24） | 三項 `\sin x\ \checkmark`／`\sin(x^2)\ ?`／`\sin(3x+1)\ ?` 改三張 chip 卡（✓綠框、?橘框）收尾；或作者選 `sparse_ok` 接受現狀 | hooks 或 callout 條列 |
| 7 | G3 命中三景 | `limit_not_identity`／`radians_essential`／`toward_the_chain_rule` 選出口（條列化／併景／sparse_ok）——內容決策，交使用者 | storyboard |
| 8 | divider hook 式 | P-A3 已修字級；順檢四張 divider 的 hook 式與 spine 曲線無互撞（scratch_frames 眼檢） | —— |

**驗收（每項）：** 渲該景 → `visual-frame-audit` V blocking=0 → VLM 複驗通過；lint/sizecheck 0 error；有旁白時序變化者跑 `make.py --reuse-audio --quality low` 確認 `[sync] clean`（§3.1 已有 MiMo 音軌——**只動畫面不動 `say`／spoken＝零計費、NFA 不重開**）。

---

## 執行紀律（全計畫）

1. **順序**：Phase 0-a → 0-b → 1 → 2 → 3 → 4 → 5。Phase 1（純文檔）可與 0-b 並行；Phase 5 可獨立延後。**Task 7 的使用者 sign-off 是硬閘。**
2. **每 task**：spec→實作→自測→commit（訊息照本檔）→ subagent 雙閘 review（實作者外的 reviewer 過一次 code＋一次 spec 對齊）。Phase 收尾跑 Codex read-only 覆核（standing consent，逕行）。
3. **計費紅線**：真 TTS／Gemini／4K 一律不碰；MiMo 音軌只 `--reuse-audio` 重用。違者停工徵同意。
4. **回歸不足時寧可多渲**：graph 相關改動一律附幀；「exit 0」不是驗收，眼見（或 agent 判）為憑。
5. **文檔同步**：每 phase 完成即補 `REBUILD_STATUS.md`（本 repo 的跨對話進度錨）；EXPECT／預算表改動與 DESIGN.md Playbook 同 commit。

## Self-review 紀錄（撰稿時已做；2026-07-05 送審前對 code 逐項複驗後更新）

- 覆蓋核對：G1→Task 9/10；G2→Task 2（＋13 fixture）；G3→Task 12（＋14#7 出口裁決）；G4→Task 11；G5→Task 9；G6→Task 8/13；P-A1..A4→Task 2/3/4/5；P-C→Task 6（＋9 Playbook 指引）；P-E→Task 9；A/B 開放值（tag/ticks/reason/h1/authored）→Task 7。撤案項（P-B/P-D/label_plate/own-curve/widow-control/say↔reveal）在 §0a 防復活。
- **送審前已對 code 複驗定案（不再是彈性點）：** `lint_storyboard` 回傳 `(severity, message)`＋尾端 `issues +=` 掛載（lint.py L289-328）；sizecheck `check_scenes` 於 `_capacity_issues` 後掛 `_sparse_issues`、Block 有 `.id`/`.mobject`（sizecheck L500-535）；`capacity_selftest` EXPECT 判「fit on one page」故 G3 另立 `SPARSE_EXPECT` 副表；graph plot 欄位＝`kind: function`＋`expression:`（`_demo_graph_reveal.yml`）；point-label call site 預設 `"text"` 不套 `_carrier_label_role`（graph.py ~L350）；`_bootstrap.bootstrap()`／`apply_tex_template()` 皆零參數；`schema.py` 有 CLI 入口且無 scene key 白名單（`sparse_ok` 可過）；`progress_dots` pill 幾何全繫於 r（放大安全）；`_demo_derivation.yml` lines[] 純字串不進 G1 掃描面（負控成立）；`scratch_frames.py` CLI＝`--storyboard/--scene a,b,c/--out`。
- 殘餘彈性點（僅一處）：`_demo_capacity.yml` 既有 meta 區塊形式——Task 12 fixture 是「追加 scenes」，照該檔現行縮排即可。

## Codex read-only 覆核紀錄（2026-07-05，standing consent）

**Round 1**（額度中斷）：Codex 跑到 grounding 一半用罄額度、未產出 findings → 本地照同一檢核單自驗，抓到並修 5 處
（point-label call site 排除／SPARSE_EXPECT 副表／fixture meta 與 plot 欄位名／lint 掛載點明確化／驗證 one-liner 補 bootstrap），
已列入上方 self-review「送審前已對 code 複驗定案」。

**Round 2**（完整覆核，7 findings，全數採納）：

| # | 級別 | Finding | 處置 |
|---|---|---|---|
| 1 | blocking | Task 2 selftest 直接 import graph.py（top-level import manim），缺 `_bootstrap.bootstrap()` 前置 | 已修：selftest 頭兩行先 bootstrap 再 import |
| 2 | blocking | `_sparse_issues` 用 `T.*` 但 sizecheck 無 module-level `T`（helper 慣例＝函式內局部 import） | 已修：函式內 `from pipeline.visuals import theme as T` |
| 3 | blocking | G4 實作只掃 aside，漏掉核可案明列的 rail statement 卡 | 已修：`_card_widow_issues` 加掃 theorem_proof 的 prose statement（純 `$formula$` 卡不掃）＋正反 fixture ×2＋斷言 |
| 4 | advisory | A/B 拍板 reason 38 時，clamp floor 硬寫 prose_sm 會與 authored size drift | 已修：`_REASON_PX` 單一常數同源 authored＋clamp；Task 7 開放值全部單點修改 |
| 5 | advisory | Task 6 的四個 demo 有三個 explicit 尺寸，驗不到 single 新預設 | 已修：Task 6 只驗 compare 預設＋explicit 不受影響；single 預設覆蓋掛 Task 13 無尺寸 fixture |
| 6 | advisory | G1 selftest 的 display-field 負斷言取錯欄（`split(":")[-1]` 是訊息文字非 path）＝vacuous | 已修：取第一個冒號前的 path 檢查 `.math`／`math[` |
| 7 | nit | `capacity_selftest` 成功訊息計數硬寫 `len(EXPECT)`，加表後印過期的「all 12」 | 已修：改兩表合計（`all 14`） |

Codex 同輪確認**非 finding**：Round 1 的 5 處自修全部正確（三個 label call site 判定、`_DIM_LABEL_ROLES` 覆蓋、eyebrow/fs/clamp-loop/part-pager 簽名、render_scaffold 相容、progress_dots pill 同比、scratch_frames CLI、storyboard 現值、`-m` 入口）。
其總裁決「修 blocking 1–3 後計畫可執行、advisory 同版補掉」——本表即為全數補掉後的狀態。

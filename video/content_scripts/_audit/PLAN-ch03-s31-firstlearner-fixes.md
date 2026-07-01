# PLAN — §3.1 first-learner sweep fixes (apply advisories to the video)

> 分支 `video/template-redesign-navy-spine`。承 sweep 報告 `REVIEW-ch03-s31-firstlearner-sweep.html`
> ＋ Codex 二審。使用者 2026-07-01 授權：五項全做（含 radians 一併登錄）、all_six 拆兩個 part、
> 需要新場景直接加、疑問跟 Codex 討論、改完 mock render §3.1 給使用者看。**真 TTS／最終 render 另議。**
> §3.1 現況＝mock 里程碑（未做真 TTS）→ 本輪＝改 source ＋ mock 重渲 ＋ 免費 gate ＋ sign-off，零計費。

## 校準線（沿用 detail-redo）
economical 但 comprehensible；detail over compression；**新增為呈現/直覺；數學須正確**（all_six 展開 cot′/csc′
是「顯示已述結果的推導」，非新事實）。每筆改動可追溯回 sweep 的某條 finding。

## 動到旁白（→ scoped NFA 回歸）：sine、cosine、all_six 三處。純上畫面（無 NFA）：cycle/toward motive、radians flag。

---

## 改動 1 — `derivative_of_sine`：補回定義行（清唯一 SC1）
**source finding：** SC1 `derivative_of_sine.def` ＋ SC-adv（reduced form 無「來自差分商」橋、~11 場無 recap）。

**storyboard scene 14（`proof` 從 2 行→3 行；covers 加 def）：**
```yaml
proof:
  - "$\\frac{d}{dx}\\sin x=\\lim_{h\\to 0}\\frac{\\sin(x+h)-\\sin x}{h}$"          # proof.0 = def（新）
  - "$=\\lim_{h\\to 0}\\cos\\!\\left(x+\\frac h2\\right)\\frac{\\sin(h/2)}{h/2}$"   # proof.1 = reduced（原 proof.0，前置 =）
  - "$\\cos\\!\\left(x+\\frac h2\\right)\\to\\cos x,\\quad \\frac{\\sin(h/2)}{h/2}\\to 1$"  # proof.2 = limits（原 proof.1）
qed: "$\\Rightarrow\\ \\cos x\\cdot 1=\\cos x$"
covers: [def, reduced, limits, qed]     # 加 def → coverage.py SC1 清零
```
**say（重排 {show} cue，對齊 .md 既有旁白——.md 本就唸出定義句）：**
```
{show proof.0} Start from the definition -- the derivative is the limit of the difference quotient.
{show proof.1} But we already did the hard algebra: that quotient is $\cos(x+\tfrac h2)$ times $\sin(h/2)$ over $h/2$.
{show proof.2} Let $h\to 0$: the first factor tends to $\cos x$ by continuity, the second to one by the fundamental limit.
{show qed} A continuous thing times a limit -- the product is $\cos x$ times one, just $\cos x$.
```
**.md `derivative_of_sine`：** narration 已含定義句（`d/dx sin x=lim(sin(x+h)-sin x)/h`），**不需改**；
visual_need 已列 4 步（def/reduced/limits/qed），**不需改**；screen_contract 已含 def，**不需改**。
**風險：** proof 3 行＋qed＋statement 較稠密 → 若 qed 出框，走 `part: 1/2`（statement+def+reduced｜limits+qed）。sizecheck/visual 定奪。

---

## 改動 2 — `derivative_of_cosine`：補獨立 limits reveal（與 sine 對稱）
**source finding：** SC-adv（limits 折進 qed、比 sine 少一條顯式行）。

**storyboard scene 15（`proof` 2→3 行；covers 不變，limits 從「併入 qed」變真 reveal）：**
```yaml
proof:
  - "$\\cos A-\\cos B=-2\\sin\\frac{A+B}{2}\\,\\sin\\frac{A-B}{2}$"                       # proof.0 companion identity
  - "$\\frac{\\cos(x+h)-\\cos x}{h}=-\\sin\\!\\left(x+\\frac h2\\right)\\frac{\\sin(h/2)}{h/2}$"  # proof.1 divided
  - "$-\\sin\\!\\left(x+\\frac h2\\right)\\to-\\sin x,\\quad \\frac{\\sin(h/2)}{h/2}\\to 1$"      # proof.2 limits（新）
qed: "$\\Rightarrow\\ -\\sin x\\cdot 1=-\\sin x$"     # \to → \Rightarrow（對齊 sine）
covers: [companion_identity, divide, limits, qed]     # limits 現對到真 reveal proof.2
```
**say（重排；對齊 .md「the sine factor goes to sin x… minus sign comes along」）：**
```
{show proof.0} This time use the companion sum-to-product formula.
{show proof.1} The same division by $h$ turns the difference quotient into $-\sin(x+\tfrac h2)$ times $\sin(h/2)$ over $h/2$.
{show proof.2} Send $h$ to zero: the sine factor tends to $\sin x$ by continuity, the second to one by the fundamental limit.
{show qed} The leading minus sign comes along -- leaving $-\sin x$. Same two tools, one extra minus sign.
```
**.md `derivative_of_cosine`：** narration 已唸兩因子極限＋minus；visual_need 已列 4 步（含 limits）；
screen_contract 已含 limits。**皆不需改**（原本 storyboard 折進 qed，現拆出＝更貼 .md）。
**風險：** 同改動 1（稠密）；若出框走 part:。

---

## 改動 3 — `all_six_trig_derivatives`：拆兩個 part 場 ＋ 展開 sec′/cot′/csc′
**source finding：** PD1（sec′ 一 reveal 併兩動作）＋ SC-adv（prompt 允諾四、cot/csc 只給裸結果）。
**做法（使用者裁決）：** 拆 `all_six_tan_sec`（part 1/2）＋ `all_six_cot_csc`（part 2/2）；sec′ 得 setup+result；cot′/csc′ 顯示商法則推導（非裸結果）。

**兩場都 `ref: md:all_six_trig_derivatives`**（同一教學單元＝「商法則推其餘四個」；covers 聯集蓋滿 contract）。

**scene 20a `all_six_tan_sec`（part: {current:1,total:2}；template derivation；accent example）：**
```yaml
prompt: "Differentiate $\\tan x$ and $\\sec x$."
steps:
  - { math: "\\frac{d}{dx}\\tan x = \\frac{(\\cos x)(\\cos x)-(\\sin x)(-\\sin x)}{\\cos^{2} x}", reason: "quotient rule on $\\tfrac{\\sin x}{\\cos x}$" }
  - { math: "= \\frac{\\cos^{2} x+\\sin^{2} x}{\\cos^{2} x} = \\frac{1}{\\cos^{2} x} = \\sec^{2} x", reason: "Pythagorean identity" }
  - { math: "\\frac{d}{dx}\\sec x = \\frac{d}{dx}\\frac{1}{\\cos x} = \\frac{0\\cdot\\cos x-1\\cdot(-\\sin x)}{\\cos^{2} x}", reason: "quotient rule on $\\tfrac{1}{\\cos x}$" }
result: { math: "= \\frac{\\sin x}{\\cos^{2} x} = \\sec x\\tan x" }
covers: [tan_quotient, tan_result, sec_setup, sec_result]
```
**scene 20b `all_six_cot_csc`（part: {current:2,total:2}；template derivation；accent example）：**
```yaml
prompt: "And the same rule on $\\cot x$ and $\\csc x$."
steps:
  - { math: "\\frac{d}{dx}\\cot x = \\frac{(-\\sin x)(\\sin x)-(\\cos x)(\\cos x)}{\\sin^{2} x}", reason: "quotient rule on $\\tfrac{\\cos x}{\\sin x}$" }
  - { math: "= \\frac{-(\\sin^{2} x+\\cos^{2} x)}{\\sin^{2} x} = -\\frac{1}{\\sin^{2} x} = -\\csc^{2} x", reason: "Pythagorean identity" }
  - { math: "\\frac{d}{dx}\\csc x = \\frac{d}{dx}\\frac{1}{\\sin x} = \\frac{0\\cdot\\sin x-1\\cdot\\cos x}{\\sin^{2} x}", reason: "quotient rule on $\\tfrac{1}{\\sin x}$" }
result: { math: "= -\\frac{\\cos x}{\\sin^{2} x} = -\\csc x\\cot x" }
covers: [cot_setup, cot_result, csc_setup, csc_result]
```
**say（part 1 / part 2；tan/sec 沿用原措辭，cot/csc 新增旁白比照 tan/sec 節奏）。**

**.md `all_six_trig_derivatives`（authoritative — 需更新，→ NFA）：**
- narration：tan/sec 沿用；**cot/csc 從「the very same move … gives −csc²x, −csc x cot x」擴為逐步**
  （cot′ 商法則 → −(sin²+cos²)/sin² = −csc²x；csc′ 商法則 → −cos/sin² = −csc x cot x）。
- visual_need：改列 4 段（tan / sec / cot / csc 各含步驟）。
- screen_contract.required_steps 改 8 步：`tan_quotient, tan_result, sec_setup, sec_result, cot_setup, cot_result, csc_setup, csc_result`。
**數學正確性：** cot′=−csc²x、csc′=−csc x cot x（handout Example 3.2 已陳述結果）；本輪只補「怎麼推」。→ 送 Codex／L5 盲算複核。
**風險：** part 場觸 `head[1]` latent bug？derivation 非 theorem_proof——REBUILD_STATUS 註 `derivation.py:143` 同款 bug 且「若有 part: derivation 場需比照以 id 取 title」。**這是首個 part: derivation 場 → 很可能要修 `derivation.py` 以 id 取 title**（外科式，比照 `theorem_proof.py` 的 `6851d0a`）。render 時盯。

---

## 改動 4 — `derivative_cycle` ＋ `toward_the_chain_rule`：補 scaffold.motive
**source finding：** PD2 advisory（definition_math 缺 motive，§9.2）。純上畫面字、無 NFA。

- scene 17 `derivative_cycle`：`scaffold: { motive: "Step back: what pattern do these two derivatives make together?" }`
  （lift 自 say 開場「Step back and watch the pattern these two derivatives make」→ 保 OF1）
- scene 23 `toward_the_chain_rule`：`scaffold: { motive: "We can do bare trig functions -- but not yet composed ones." }`
  （lift 自 say「only in its bare form … $\sin(x^2)$ … not yet」→ 保 OF1）
**風險：** definition_math 首次帶 scaffold（`definition_math.py:80` head[1] latent bug，non-part 不觸發但未實測）→ render 盯；若 motive 錯位，比照以 id 取 title 修 `definition_math.py`。

---

## 改動 5 — radians 登錄 `meta.assumptions`（PD4）
**source finding：** AMP → 假設機制（correctness-critical radians）。使用者本輪裁准登錄（推翻先前 D-A defer）。

**storyboard `meta`（於 `meta:` 之下，非頂層）：**
```yaml
  assumptions:
    - id: radians
      text: "angles in radians (arc $=\\theta$)"
      first_use_unit: why_trig_is_different
      source: "chapter3-print-standalone.html SS3.1 . radian convention"
```
**first_use_unit 場需帶 flag：** scene 2 `why_trig_is_different` 加 `scaffold: { flag: radians }`
（radians 於此場旁白首次點名「angles are measured in radians -- an assumption that turns out to be essential」）。
**渲染：** render_scaffold 於 definition_math 畫 ASSUMES badge（首次於 definition_math 用 scaffold → 同改動 4 風險，render 盯）。
**驗證：** pedagogy.py `assumptions_registry_issues` 需 clean（id/text/first_use_unit/source 齊、first_use_unit 是真場且帶 flag、無 orphan）。

---

## 執行順序 ＋ gate（全免費離線）
1. 改動 4＋5（純上畫面、風險低）先落，單獨 render 驗 definition_math scaffold 渲染（若 head[1] bug 觸發→修 template 以 id 取 title）。
2. 改動 1＋2（proof 補行）落，sizecheck＋render 驗 qed 餘裕（出框→part:）。
3. 改動 3（all_six 拆場＋擴 .md）落，render 驗 part: derivation（很可能修 `derivation.py`）。
4. 全 deck：`schema.py`（coverage 應 0 SC1、pedagogy 0）＋lint＋sizecheck 0-error。
5. `make.py --storyboard …ch03_trig_derivatives.yml --backend mock --quality high`（mock 全片）。
6. gate-1：`visual-frame-audit`（改動/新場的幀）＋ scoped `NFA`（sine/cosine/all_six 動旁白的單元）＋ pedagogy sweep 回歸（確認 SC1=0、advisory 降）。
7. 出片給使用者看（mp4 ＋ 代表幀）；更新 sweep 報告的「已修」狀態。
8. Codex 覆核：本 plan（動手前）＋ all_six 新 narration 數學（L5）＋ 改完 diff。

## 成功標準
coverage.py SC1＝0（def 補回）；pedagogy sweep：sine/cosine/all_six 的 SC-adv 消解、all_six PD1 消解、cycle/toward PD2 消解、radians 進 registry；schema/lint/sizecheck exit 0；mock render 全片成；visual-frame-audit 0 blocking；scoped NFA 對動到的單元 clean；§3.1 mp4 給使用者過目。

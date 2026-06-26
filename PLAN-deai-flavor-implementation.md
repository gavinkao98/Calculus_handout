# 去「AI 味」方案 Implementation Plan

> ⚠️ **偵測層已 SUPERSEDED（2026-06-26）。** 本檔 Phase 0–2 的「Vale 清單＋Dimension C 數 tell／密度」偵測實作，已由 [`PLAN-deai-semantic-critic.md`](PLAN-deai-semantic-critic.md)（語意/聲音 S/A/V critic）取代；緣由見該檔 §0。下方 Phase 0–4 步驟保留作**已完成工作的紀錄**，但 Dimension C（數 tell/密度）、Ch1 校準門檻、§3 的 Ch1 voice corpus 等均退役或替換——新的逐 task 展開以 semantic-critic 的 implementation plan 為準。

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

> **本檔是什麼：** [`PLAN-deai-flavor.md`](PLAN-deai-flavor.md)（設計/決策）的細顆粒度實作展開。設計層的「為什麼、決策、規格」看 `PLAN-deai-flavor.md`；本檔是「逐 task 怎麼做、怎麼驗」。執行者可零背景上手。完整診斷另見 [`REVIEW-ai-flavor-authoring-audit.html`](REVIEW-ai-flavor-authoring-audit.html)。

**Goal:** 在 handout（HTML 講義）與 video（旁白）兩條產線建立一套「flag-only 決定性 lint ＋ 人審語聲維度 ＋ 撰寫時預防」的防禦，系統性降低成稿散文的「AI 味」，且不誤砍合法數學散文。

---

## 執行進度（Handoff — 跨機器接手看這裡）

> **最後更新：2026-06-25（下班交接）。** 跨對話／跨機器進度錨（依 CLAUDE.md：進度寫進版控文檔，不只記本地 memory）。回家換電腦接手時先讀這節。步驟級 `- [ ]` checkbox 維持原樣，**task 級狀態以本節為準**。

### 環境（換機先做）
- 本案新依賴 **Vale 3.15.1** 已登記進 [`tools/doctor.py`](tools/doctor.py)／[`ENVIRONMENT.md`](ENVIRONMENT.md)（⑤b 段）。**新機器先跑：** `winget install errata-ai.Vale`（裝完開新 shell 讓 PATH 生效），再 `python tools/doctor.py` 確認 `vale` 行轉綠。
- 跑本案測試（需 vale 在 PATH）：`python tools/deai/check_seed.py`、`python tools/deai/test_vale_fixture.py`、`python tools/deai/build_seed.py --check`。

### 完成度
- **Phase 0（0.1–0.3）✅**：Vale 裝好＋進 doctor/ENVIRONMENT；種子 `reject`(14)/`accept`(9) + curation 守門；`.vale.ini` markup-aware + AItexture rule-pack（Phrases/Copula/Negative）+ fixture 測試（抓 tell、不誤砍數學、對照組乾淨）。
- **Phase 1（1.1–1.2）✅**：Dimension C 進 `PROSE-AUDIT-RUBRIC.md`；Ch1 校準（Vale **0 誤砍/9324 字**、人審真 tell≈0、唯一訊號 em-dash 峰值 ~4.0/500）→ [`handout/_audit/REPORT-deai-ch1-calibration.md`](handout/_audit/REPORT-deai-ch1-calibration.md) ＋ HTML。
- **Phase 2**：2.1 ✅（Dimension C 升 blocking、N=3 + 兩 refinement、§3 保護清單加密度天花板；fixture 現觸 Blocking、對照組仍 0）｜ 2.2 ✅（README Mode A/C 第 9 項 AI-texture sweep）｜ 2.3 ✅（Output Style `.claude/output-styles/deai-house-voice.md`）｜ **2.4 ⏳ 待你裁決（⛳#3，見下）**｜ 2.5 ⬜ 未開始（接 Vale 進 CONTENT_DIRECTION ⑤，doc-only 無 ⛳）。
- **Phase 3 / 4 ⬜**：未開始。

### 已拍板（locked，勿 re-litigate）
- **⛳#1**：blocking 門檻 **N=3** + (a) 只數真 tell（content-bearing 邊緣不計）(b) 短節絕對下限（≥3 absolute 且 ≥3/500）；**C6 em-dash** advisory ≥4/500、單句≥3 為熱點；C1–C6 措辭維持；**Ch1 不動**。
- **⛳#2**：Output Style 內容、§3 密度天花板（連接詞 distinct >3/500、em-dash ≥4/500、其餘四類僅進叢集才轉 finding）、Mode A 第 9 項措辭——三項照現狀採納。

### ⬇ 回家第一件事：⛳#3 voice corpus 入選
打開 [`handout/_audit/REVIEW-deai-voicecorpus-candidates.html`](handout/_audit/REVIEW-deai-voicecorpus-candidates.html) 勾選，或直接回覆要哪幾個 ID：
- **②a** §1.1 Example 1.7（worked solution 主錨，**最高優先缺口**，建議必加）
- **③a** §1.6 開場歷史段 ｜ **④a** §1.6 challenge-and-response（延伸 gloss）｜ **①a** §1.3 極限動機段（concrete-first，選擇性）
- 次選：②b 短解法、③b/④b tolerances（同段、擇一）、①b §1.2
- **我的建議組合：②a + ③a + ④a（＋可選 ①a）湊滿四型。**
- 選定後：2.4 Step 3-4（逐字插入 §3、標特徵、核對 verbatim 不動數學）→ commit → 2.5 → Phase 3（Ch2–4 定稿 Mode B，逐章 ⛳）→ Phase 4（video gate，⛳）。

### Commit / 分支
本案 Phase 0–2 已完成部分本次已 commit（撈：`git log --grep=deai`）。落在 `video/template-redesign-navy-spine`（使用者選定留此分支）。video WIP（`video/DESIGN.md`／`graph.py`／storyboard）非本案、未碰、未 commit。

---

**Architecture:** 三層——(1) 預防（Mode A 自查、Output Style、voice corpus）；(2) 決定性 lint（Vale，markup-aware，接進 `CONTENT_DIRECTION ⑤` 既有 linter lane，永遠 advisory）；(3) 人審 gate（`PROSE-AUDIT-RUBRIC.md` 新增 Dimension C，由既有 `handout-prose-audit` subagent ＋ Codex gate-2 繼承；video 平行 C6）。不做成 Skill。Workflow 只用於一次性唯讀掃描。

**Tech Stack:** Vale（Go binary，prose linter）；既有 Python 工具鏈（`tools/doctor.py`、`build.py`）；Markdown rubric 契約；Claude subagent（gate 1）＋ Codex（gate 2）；Claude Code Output Styles。平台 win32（PowerShell 主、Bash 可用）。

## Global Constraints

> 每個 task 的需求都隱含包含本節。數值逐字取自設計 spec。

- **語域恆定**：Stewart／Rogawski、自學高中生（升大學群體）讀得懂、**clarity > compactness**。**永不**把散文往「艱澀」調。
- **lint 永遠 flag-only / advisory，絕不 auto-reject**。Vale 嚴重度設 `warning`/`suggestion`，**不設 `error`**。決定性「擋稿」只在 Mode B 人審 Dimension C。
- **絕不用 AI-detector 機率分數當 gate**（GPTZero/CatchGPT 類；非母語 61% 偽陽、可 paraphrase 規避）。
- **不做成 Skill**：gate = rubric ＋ 既有 subagent ＋ Vale 工具；Workflow 僅用於一次性掃描。
- **密度啟發式**：同一節 ≥3 個 distinct AI-tell 落在約 500 字內 = 高密度叢集（blocking，僅階段二啟用）；單一合法用法不觸發。
- **兩階段上線**：階段一 Dimension C 只報不擋（advisory）；Ch1 校準後階段二才啟用 blocking。
- **種子清單必對數學詞 curate**：`accept.txt` 保護 `leverage, robust, comprehensive, integral, intrinsic, examine, demonstrate` 等真數學詞。
- **Vale scope = 只掃散文**：排除 `$...$`、`\(...\)`、LaTeX 命令、`<code>`／程式碼。
- **回填政策**：video 零回填（將整批重做，forward-only）；handout 不另開回填活動——Ch1 當校準基準，Ch2–4 搭定稿 Mode B 便車。
- **種子來源只用有授權的**：berenslab/llm-excess-vocab（MIT）、Wikipedia: Signs of AI writing（CC BY-SA，引用標示）；stop-slop/avoid-ai-writing（MIT）取 pattern；無授權清單不 vendor。
- **文檔繁體中文**（LaTeX／程式碼、套件名、檔名、技術術語保留英文）。
- **Commit 政策**：依 [`CLAUDE.md`](CLAUDE.md)——當輪未經要求不擅自 commit／push；Mode B 裁決寫進 commit body；訊息繁中、結尾加 `Co-Authored-By` trailer。本計畫各 task 末的 commit step 在執行者取得授權後才執行。

---

## File Structure（先鎖定分解）

新增/修改的檔，及各自職責：

**新增（Vale 基礎建設）：**
- `.vale.ini` — Vale 專案設定（掃哪些副檔名、套哪些 style、markup scope）
- `styles/AItexture/` — 自訂 style 目錄
  - `styles/AItexture/Phrases.yml` — 單詞/片語 existence rule（嚴重度 warning）
  - `styles/AItexture/Copula.yml` — copula-avoidance（serves as / stands as…）
  - `styles/AItexture/Negative.yml` — `not X but Y` / `not only…but also`
  - `styles/config/vocabularies/AItexture/reject.txt` — banned 種子（自動接上 `Vale.Avoid`）
  - `styles/config/vocabularies/AItexture/accept.txt` — 數學詞白名單（保護）
- `tools/deai/build_seed.py` — 從授權來源組裝＋curate 種子清單，產 `reject.txt`
- `tools/deai/check_seed.py` — curation 守門：斷言無數學詞混入、已知 tell 存在
- `handout/_audit/fixtures/ai-tell-fixture.html` — 含 seeded tell ＋ 數學的 fixture
- `handout/_audit/fixtures/clean-control.html` — 乾淨對照（Ch1 風格）
- `tools/deai/test_vale_fixture.py` — 跑 Vale 對 fixture、斷言 flag/不誤砍

**修改（rubric/方法論/環境）：**
- `handout/_audit/PROSE-AUDIT-RUBRIC.md` — 加 Dimension C（先 advisory；後升 blocking ＋ §3 密度天花板）
- `video/content_scripts/_audit/NARRATION-COPYEDIT-RUBRIC.md` — 加 C6、移出 tier-3 上限
- `CONTENT_SPEC.md` — §3 擴 voice corpus（4 型別，從 Ch1 提候選）
- `CONTENT_DIRECTION.md` — ⑤ 接 Vale lint lane
- `README.md` — Mode A 8 項稽核加第 9 項
- `video/CONTENT_METHODOLOGY.md` — §4 引導語頻率預算
- `ENVIRONMENT.md`、`tools/doctor.py`、`tools/setup.ps1` — 登記 Vale
- 新增 `.claude/output-styles/deai-house-voice.md` — 預防層 Output Style

---

## Phase 0 — Vale 基礎建設 + 種子清單

### Task 0.1：安裝 Vale 並登記進環境健檢

**Files:**
- Modify: `ENVIRONMENT.md`（新增 Vale 段）
- Modify: `tools/doctor.py`（新增 Vale 檢查）
- Modify: `tools/setup.ps1`（可選：自動安裝）

**Interfaces:**
- Produces: 一個可被後續 task 呼叫的 `vale` CLI（在 PATH 上）；`python tools/doctor.py` 含 Vale 檢查行。

- [ ] **Step 1：先寫失敗檢查** — 在 `tools/doctor.py` 找到既有檢查清單的結構（搜尋現有的 binary 檢查，如 `ffmpeg`），仿照新增一個 Vale 檢查函式：

```python
def check_vale():
    """Vale prose linter — 去 AI 味 lint 引擎（PLAN-deai-flavor）。"""
    exe = shutil.which("vale")
    if not exe:
        return ("Vale", False, "未安裝；見 ENVIRONMENT.md「Vale」段")
    try:
        out = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=10)
        ver = out.stdout.strip() or out.stderr.strip()
        return ("Vale", True, ver)
    except Exception as e:
        return ("Vale", False, f"執行失敗：{e}")
```
把它接進 doctor 既有的檢查彙總（比照其他檢查的註冊方式）。

- [ ] **Step 2：跑 doctor 確認 Vale 這項為紅**

Run: `python tools/doctor.py`
Expected: 輸出含 `Vale ... 未安裝`（紅），其餘維持原狀。

- [ ] **Step 3：安裝 Vale**

Windows（PowerShell）：`winget install errata-ai.Vale`
（備援：scoop `scoop install vale`；或自 https://github.com/errata-ai/vale/releases 下載 binary 放 PATH。）
確認版本：`vale --version`（記下版本字串供 pin）。

- [ ] **Step 4：跑 doctor 確認轉綠**

Run: `python tools/doctor.py`
Expected: `Vale ... vX.Y.Z`（綠）。

- [ ] **Step 5：更新 `ENVIRONMENT.md` 與（可選）`setup.ps1`**

在 `ENVIRONMENT.md` 新增「Vale」段：用途（去 AI 味 lint）、pinned 版本（Step 3 記下的）、安裝指令、doctor 檢查項。若 `setup.ps1` 有「從清單重現環境」段，加一行 `winget install --id errata-ai.Vale -e`（標為去 AI 味用）。

- [ ] **Step 6：Commit**（取得授權後）

```bash
git add tools/doctor.py ENVIRONMENT.md tools/setup.ps1
git commit -m "chore(deai): 登記 Vale 進 doctor/ENVIRONMENT（去 AI 味 lint 引擎）"
```

---

### Task 0.2：組裝並 curate 種子清單

**Files:**
- Create: `tools/deai/build_seed.py`
- Create: `tools/deai/check_seed.py`
- Create: `styles/config/vocabularies/AItexture/reject.txt`
- Create: `styles/config/vocabularies/AItexture/accept.txt`
- Test: `tools/deai/check_seed.py`（本身即測試）

**Interfaces:**
- Produces: `reject.txt`（每行一個 banned 單詞/片語）、`accept.txt`（每行一個受保護數學詞）。被 Task 0.3 的 Vale 設定消費。

- [ ] **Step 1：先寫守門測試 `tools/deai/check_seed.py`**

```python
"""種子清單 curation 守門：跑 `python tools/deai/check_seed.py`。"""
import sys, pathlib

VOCAB = pathlib.Path("styles/config/vocabularies/AItexture")
reject = (VOCAB / "reject.txt").read_text(encoding="utf-8").lower().splitlines()
accept = (VOCAB / "accept.txt").read_text(encoding="utf-8").lower().splitlines()

# 合法數學詞絕不可出現在 reject（否則誤砍課文）
MATH_WORDS = ["leverage", "robust", "comprehensive", "integral",
              "intrinsic", "examine", "demonstrate", "derive", "bound"]
# 已知 AI-tell 必須在 reject
MUST_FLAG = ["delve into", "it is worth noting that", "serves as a",
             "plays a crucial role in", "rich tapestry"]

errors = []
for w in MATH_WORDS:
    if any(w == line.strip() for line in reject):
        errors.append(f"數學詞誤入 reject：{w}")
    if not any(w == line.strip() for line in accept):
        errors.append(f"數學詞未受 accept 保護：{w}")
for p in MUST_FLAG:
    if not any(p == line.strip() for line in reject):
        errors.append(f"已知 tell 不在 reject：{p}")

if errors:
    print("FAIL:\n" + "\n".join(errors)); sys.exit(1)
print(f"OK: reject={len(reject)} accept={len(accept)}"); sys.exit(0)
```

- [ ] **Step 2：跑測試確認失敗（檔案還沒建）**

Run: `python tools/deai/check_seed.py`
Expected: FAIL（`FileNotFoundError` 或斷言失敗）。

- [ ] **Step 3：寫 `tools/deai/build_seed.py` 並產初版清單**

`build_seed.py` 從**有授權**來源組裝（執行時下載或手動放入 `tools/deai/sources/`）：berenslab `excess_words.csv`（MIT）取詞、Wikipedia「Signs of AI writing」與 stop-slop/avoid-ai-writing 取片語 pattern。對每個候選詞，若在 `MATH_WORDS`／數學語境常見 → 丟 `accept.txt`，否則進 `reject.txt`。最小可行做法：先手寫初版 `reject.txt`（用 `PLAN-deai-flavor.md §4.2` 的 banned-starter 清單 + berenslab 高頻詞中明顯非數學者），`accept.txt` 放 `MATH_WORDS`。`build_seed.py` 至少要能：讀來源、套 `accept` 過濾、輸出去重排序的 `reject.txt`。

`reject.txt` 起步內容（逐字，可再擴）：
```
delve into
it is worth noting that
it is important to note that
in this section we will explore
let us turn our attention to
serves as a
stands as a testament to
plays a crucial role in
plays a pivotal role in
the fundamental building block of
rich tapestry
ever-evolving landscape
underscoring the importance of
a powerful and elegant tool
```
`accept.txt` 起步內容：
```
leverage
robust
comprehensive
integral
intrinsic
examine
demonstrate
derive
bound
```

- [ ] **Step 4：跑測試確認通過**

Run: `python tools/deai/check_seed.py`
Expected: `OK: reject=… accept=…`

- [ ] **Step 5：Commit**（授權後）

```bash
git add tools/deai/ styles/config/vocabularies/AItexture/
git commit -m "feat(deai): 種子 banned/accept 清單 + curation 守門測試"
```

---

### Task 0.3：Vale 設定（markup-aware，只掃散文）

**Files:**
- Create: `.vale.ini`
- Create: `styles/AItexture/Phrases.yml`、`styles/AItexture/Copula.yml`、`styles/AItexture/Negative.yml`
- Create: `handout/_audit/fixtures/ai-tell-fixture.html`、`handout/_audit/fixtures/clean-control.html`
- Test: `tools/deai/test_vale_fixture.py`

**Interfaces:**
- Consumes: Task 0.2 的 `reject.txt`/`accept.txt`。
- Produces: 可跑的 `vale <file>`，對散文 flag AI-tell、對 `$...$` 內與數學詞不誤砍。

- [ ] **Step 1：先寫 fixtures（即測試輸入）**

`handout/_audit/fixtures/ai-tell-fixture.html`（含 seeded tell ＋ 數學）：
```html
<p>It is worth noting that the derivative serves as a fundamental building block of calculus.</p>
<p>Not only is $f$ continuous, but it is also differentiable, so we can delve into its behavior.</p>
<p>Let $f(x)=x^2$ on $[0,\infty)$. Then $f^{-1}(y)=\sqrt{y}$, and the integral is robust.</p>
```
`handout/_audit/fixtures/clean-control.html`（Ch1 風格、應零 flag）：
```html
<p>Not every function can be reversed. If two different inputs give the same output, we cannot recover the input uniquely.</p>
<p>Let $f$ be one-to-one. Notice that this rules out exactly the problem described above.</p>
```

- [ ] **Step 2：寫 `tools/deai/test_vale_fixture.py`（先讓它失敗）**

```python
"""跑 Vale 對 fixture，斷言 flag 命中且不誤砍。跑：python tools/deai/test_vale_fixture.py"""
import subprocess, sys, json

def vale_json(path):
    out = subprocess.run(["vale", "--output=JSON", path], capture_output=True, text=True)
    return json.loads(out.stdout or "{}")

tell = vale_json("handout/_audit/fixtures/ai-tell-fixture.html")
ctrl = vale_json("handout/_audit/fixtures/clean-control.html")

tell_hits = [m["Match"].lower() for alerts in tell.values() for m in alerts]
ctrl_hits = [m["Match"] for alerts in ctrl.values() for m in alerts]

errors = []
# 必須抓到的 tell（含 copula-avoidance、negative parallelism）
for needle in ["it is worth noting", "serves as", "delve", "not only"]:
    if not any(needle in h for h in tell_hits):
        errors.append(f"漏抓 tell：{needle}")
# 不可誤砍：數學詞 robust（在 accept）、$...$ 內任何符號
if any("robust" in h for h in tell_hits):
    errors.append("誤砍受保護數學詞 robust")
if any(sym in " ".join(tell_hits) for sym in ["sqrt", "x^2", "f^{-1}", "infty"]):
    errors.append("誤砍 $...$ 內數學符號")
# 對照組應乾淨（'Notice that' 是 §3 鼓勵連接詞，單次不該 flag）
if ctrl_hits:
    errors.append(f"對照組誤報：{ctrl_hits}")

if errors:
    print("FAIL:\n" + "\n".join(errors)); sys.exit(1)
print("OK: Vale fixture 通過"); sys.exit(0)
```

Run: `python tools/deai/test_vale_fixture.py`
Expected: FAIL（`.vale.ini` 還沒建，Vale 無 style 可套）。

- [ ] **Step 3：寫 `.vale.ini`（markup scope ＋ 套 AItexture）**

```ini
StylesPath = styles
MinAlertLevel = suggestion

Vocab = AItexture

[*.{html,md}]
BasedOnStyles = AItexture
# 只掃散文：略過行內與區塊數學、程式碼
BlockIgnores = (?s) *(\$\$.*?\$\$), (?s)(<code>.*?</code>)
TokenIgnores = (\$[^$\n]+\$), (\\\([^)]*\\\)), (\\[a-zA-Z]+\{[^}]*\})
```
（`Vocab = AItexture` 讓 `reject.txt` 自動接上 `Vale.Avoid`、`accept.txt` 受保護。`TokenIgnores` 排除 `$...$`、`\(...\)`、`\cmd{...}`。執行時用 fixture 微調 regex 直到 Step 5 綠。）

- [ ] **Step 4：寫三個自訂 rule（嚴重度 warning）**

`styles/AItexture/Copula.yml`：
```yaml
extends: existence
message: "copula-avoidance：'%s' 可考慮改回 is/are（C2）"
level: warning
ignorecase: true
tokens:
  - serves as a
  - stands as a
  - acts as a
```
`styles/AItexture/Negative.yml`：
```yaml
extends: existence
message: "裝飾性 negative parallelism：'%s'（C3）"
level: warning
ignorecase: true
tokens:
  - 'not only \w+ but also'
  - "not just \\w+,? (it's|but)"
```
`styles/AItexture/Phrases.yml`：
```yaml
extends: existence
message: "AI-tell 片語：'%s'（C1/C5）"
level: warning
ignorecase: true
tokens:
  - it is worth noting that
  - it is important to note that
  - this means that
  - delve into
```
（`reject.txt` 已涵蓋大部分片語；此處補 regex 型 negative parallelism 與 copula，因為它們不是固定字串。）

- [ ] **Step 5：跑 fixture 測試直到通過**

Run: `python tools/deai/test_vale_fixture.py`
Expected: `OK: Vale fixture 通過`
（若對照組誤報「Notice that」→ 確認沒把 §3 鼓勵連接詞放進 `reject.txt`；單次使用本就不該 flag，密度由人審維度 C 管。）

- [ ] **Step 6：Commit**（授權後）

```bash
git add .vale.ini styles/ handout/_audit/fixtures/ tools/deai/test_vale_fixture.py
git commit -m "feat(deai): Vale 設定 + AItexture rule-pack + fixture 測試（markup-aware、不誤砍數學）"
```

---

## Phase 1 — Dimension C（advisory）+ Ch1 校準

### Task 1.1：把 Dimension C 加進 PROSE-AUDIT-RUBRIC（先 advisory）

**Files:**
- Modify: `handout/_audit/PROSE-AUDIT-RUBRIC.md`
- Test（validation）: 用 `handout/_audit/fixtures/ai-tell-fixture.html` 跑 `handout-prose-audit` subagent，確認 C 維度開火、對照組乾淨。

**Interfaces:**
- Produces: rubric 新增「C. 語聲 AI-texture」維度，blocking 線**標明階段一停用**；既有 `handout-prose-audit` subagent 與 Codex gate-2 因單一真相來源自動繼承。

- [ ] **Step 1：在 `PROSE-AUDIT-RUBRIC.md`「兩個維度」之後插入第三維度**（逐字）

> 把標題「## 兩個維度」改為「## 三個維度」，並在 B 流暢性段之後插入：

```markdown
### C. 語聲 AI-texture（密度觸發；分兩階段上線）

讀者「會不會覺得這是機器寫的」。§3 語域權威不變，本維度只審 AI-tell 的**密度**，不審個別合法用法。**單一合法用法不算 finding；觸發擋稿的是密度。**

- **C1 空心 signposting / 連接詞超量** — signpost 開頭（It is worth/important to note、Recall that[無可回查]、In this section we will、Now let us turn our attention to）與「敘述顯而易見步驟」的連接詞（This means that、From this we can see、It follows naturally that）。§3 鼓勵的連接詞仍是特性，**但帶密度天花板**：同一節超過約每 500 字 3 個 distinct → C1。
- **C2 copula-avoidance** — 以 serves as / represents / marks / stands as 取代可用的 is/are。
- **C3 裝飾性 negative parallelism** — `not X but Y` / `not only…but also`，純為節奏、對比可隱含時。
- **C4 強迫性 rule-of-three** — 三形容詞／三子句堆疊為 cadence 而非真有三項。
- **C5 puffery / 借來的宏大** — powerful tool、elegant、profound、fundamental building block、rich tapestry，斷言而非由內容掙得；及無新意的 `In summary, we have seen…` 重述。
- **C6 em-dash 密度** — 散文中 em-dash 作插入語的頻率（§8 已要求謹慎；此處給密度線）。

**擋稿線：** BLOCKING = 任一節 C1–C6 合計 ≥3 個 distinct AI-tell 落在約 500 字內。單一 tell = ADVISORY。
**【階段一：本擋稿線停用——C 維度全部只報為 Optional/advisory，不擋收斂。Ch1 校準完成、門檻定案後（見 PLAN Phase 2）才啟用 blocking。】**

**不算 finding（§3-protected）：** §3 鼓勵連接詞、刻意教學重複、章末回查重述、Informally gloss、topic-term recurrence —— **階段一仍維持原無上限保護**；密度天花板於階段二再加（Task 2.1）。

唯讀、提議不行動，與 A/B 維度同護欄。Vale lint 的 flag 當預標餵入。
```

- [ ] **Step 2：更新 VERDICT 行格式說明**

在「回報規格」的 VERDICT 行說明加上 `<X> AI-texture`：`VERDICT: <B> blocking, <T> tighten, <O> optional, <X> AI-texture`。並在維度速覽（若有）補列 C1–C6。

- [ ] **Step 3：驗證 — 對 fixture 跑 subagent，確認 C 開火**

派 `handout-prose-audit` subagent 審 `handout/_audit/fixtures/ai-tell-fixture.html`。
Expected: 回報含 `[Optional] [C2]`（serves as）、`[Optional] [C1]`（it is worth noting / delve）、`[Optional] [C3]`（not only…but also）；**且因階段一，全為 Optional、無 Blocking**。

- [ ] **Step 4：驗證對照組乾淨**

派同一 subagent 審 `handout/_audit/fixtures/clean-control.html`。
Expected: C 維度 clean（單次 `Notice that` 不報）。

- [ ] **Step 5：Commit**（授權後）

```bash
git add handout/_audit/PROSE-AUDIT-RUBRIC.md
git commit -m "feat(deai): PROSE-AUDIT 加 Dimension C 語聲維度（階段一 advisory）"
```

---

### Task 1.2：Ch1 校準掃描，定門檻（交付＝校準報告）

**Files:**
- Create: `handout/_audit/REPORT-deai-ch1-calibration.md`
- 唯讀：不改任何 fragment。

**Interfaces:**
- Consumes: Phase 0 的 Vale、Task 1.1 的 Dimension C。
- Produces: 「高密度叢集」門檻的建議值（供 §6 使用者拍板）＋ Ch1 誤砍率記錄。

- [ ] **Step 1：對 Ch1 全 7 節 fragment 跑 Vale（唯讀），收 per-section 命中數**

Run: `vale --output=JSON handout/fragments/ch01/sec-*.html > /tmp/ch1-vale.json`
把每節的命中按 rule 歸類、估每 500 字密度。

- [ ] **Step 2：對 Ch1 各節跑 `handout-prose-audit`（含 C 維度，唯讀）**

逐節派 subagent，收 C1–C6 的 Optional findings。

- [ ] **Step 3：寫 `REPORT-deai-ch1-calibration.md`**

內容：每節的 Vale 密度 + 人審 C findings；Ch1（已簽核好散文）的密度分布；**建議門檻**（讓 Ch1 多數節落在門檻下，例如「每 500 字 ≥3 distinct」是否需調為 ≥4）；列出疑似誤砍（受保護連接詞、數學詞）以回頭調 `reject.txt`/`accept.txt`。

- [ ] **Step 4：驗收 — 誤砍率可接受**

人工檢視報告：受保護項（§3 連接詞、數學詞、`$...$`）誤報率低到可接受；門檻有 Ch1 資料支撐。若誤報偏高 → 回 Task 0.2/0.3 調 `accept.txt`/`TokenIgnores`，重跑。

- [ ] **Step 5：Commit**（授權後）

```bash
git add handout/_audit/REPORT-deai-ch1-calibration.md
git commit -m "chore(deai): Ch1 校準報告 + 高密度叢集門檻建議（待拍板）"
```

> **⛳ 使用者 sign-off 點（§6-2）：** 門檻起始值、C1–C6 措辭、是否對 Ch1 真熱點做選擇性小修。確認後才進 Phase 2。

---

## Phase 2 — 升 blocking + §3 密度天花板 + 預防層 + corpus

### Task 2.1：啟用 Dimension C blocking + 給 §3 保護清單加密度天花板

**Files:**
- Modify: `handout/_audit/PROSE-AUDIT-RUBRIC.md`

**Interfaces:**
- Consumes: Task 1.2 拍板的門檻值。
- Produces: C 維度具 blocking 效力；保護清單帶密度天花板。

- [ ] **Step 1：把 Task 1.1 插入的「【階段一：本擋稿線停用…】」整段刪除**，改為正式收斂判準：

```markdown
**收斂判準補一條：** 該節 AI-texture 通過 = 高密度叢集（C1–C6 合計 ≥N distinct / ~500 字）= 0。advisory（單一 tell）不強制歸零。
```
（`N` 用 Task 1.2 拍板值。）

- [ ] **Step 2：改寫「不算 finding（§3-protected）」段，加密度天花板**

```markdown
**不算 finding（§3-protected，但加密度天花板）：** §3 鼓勵連接詞、刻意教學重複、章末回查重述、Informally gloss、topic-term recurrence —— 仍是特性，**但任一者在單節內超過密度門檻即轉 C# finding**；舊版「絕不可當 finding」的無上限保護到此為止（這正是 AI scaffolding 過去被積極辯護而存活的漏洞）。
```

- [ ] **Step 3：把 Dimension C 接進「擋稿線（blocking vs advisory）」總表**

在既有「BLOCKING（讀者會卡住或被誤導）」清單末，加：「以及 **C 維度的高密度叢集**（≥N distinct AI-tell / ~500 字）」。

- [ ] **Step 4：驗證 — fixture 現在應觸發 Blocking**

派 `handout-prose-audit` 審 `ai-tell-fixture.html`（密集 tell）。
Expected: 現在回報含 `[Blocking] [C…]`（高密度叢集）。對 `clean-control.html` 仍 0 blocking。

- [ ] **Step 5：Commit**（授權後）

```bash
git add handout/_audit/PROSE-AUDIT-RUBRIC.md
git commit -m "feat(deai): 啟用 Dimension C blocking + §3 保護清單加密度天花板（階段二）"
```

---

### Task 2.2：Mode A 8 項稽核加第 9 項「AI-texture sweep」

**Files:**
- Modify: `README.md`（Mode A，及 Mode C 共用的 8 項稽核）

- [ ] **Step 1：定位 8 項放大稽核清單**，在末尾加第 9 項（逐字）：

```markdown
9. **AI-texture sweep** — 對每個 `<!-- expansion:` marker 緊接的散文，跑 banned-list 與密度檢查（可用 `vale <fragment>` 取預標）；對每個 flag：**補上**（改寫成更具體、變句長、砍空心 signposting）**或記錄**為刻意保留（roadmap Open questions）。比照其餘 8 項「補上或記錄」的處置。
```

- [ ] **Step 2：驗證 — 措辭與既有 8 項風格一致**，且明確複用「補上或記錄」機制（人工讀一次）。

- [ ] **Step 3：Commit**（授權後）

```bash
git add README.md
git commit -m "feat(deai): Mode A 放大稽核加第 9 項 AI-texture sweep"
```

---

### Task 2.3：Output Style（預防層）

**Files:**
- Create: `.claude/output-styles/deai-house-voice.md`

- [ ] **Step 1：寫 Output Style 檔**

```markdown
---
name: deai-house-voice
description: 講義 house voice + 避免 AI-tell（PLAN-deai-flavor 預防層）
keep-coding-instructions: true
---

撰寫英文講義散文時：語域 = Stewart/Rogawski，自學高中生（升大學）讀得懂，clarity > compactness。

避免下列 AI-tell（密度過高會被 Dimension C 擋）：空心 signposting（It is worth/important to note、In this section we will）、敘述顯而易見步驟（This means that、From this we can see）、copula-avoidance（serves as / stands as 取代 is/are）、裝飾性 `not X but Y`、強迫性三段排比、puffery（powerful tool、rich tapestry）、過量 em-dash。

偏好：句長有變化（具體 burstiness）、具體數值/例子先於抽象、動機先於形式、直覺不 hedge 地說出再收緊。語聲標靶見 CONTENT_SPEC §3 語聲參考範文。
```

- [ ] **Step 2：驗證 build/Manim 不受影響**

確認 `keep-coding-instructions: true` 已設。在啟用該 style 的 session 跑一次 `python handout/build.py ch01`（或 mock 流程），確認工程行為正常。
Expected: build 正常完成、無因 style 改變而壞。

- [ ] **Step 3：Commit**（授權後）

```bash
git add .claude/output-styles/deai-house-voice.md
git commit -m "feat(deai): Output Style 預防層（house voice + 避 AI-tell；keep-coding-instructions）"
```

> **⛳ sign-off 點（§6-6）：** Output Style 內容；§6-4：§3 密度天花板 N 值；§6-7：Mode A 第 9 項措辭。

---

### Task 2.4：建 voice corpus（提候選→使用者審定）

**Files:**
- Modify: `CONTENT_SPEC.md`（§3 語聲參考範文）

**Interfaces:**
- Consumes: 已簽核 Ch1 fragment。
- Produces: §3 擴成 3–4 段範文，含 worked-solution 型。

- [ ] **Step 1：從已簽核 Ch1 提候選**

掃 `handout/fragments/ch01/sec-*.html`，按四型別各挑 1–2 段候選：①動機鋪陳、②**worked solution（優先補、目前缺）**、③歷史/應用旁註、④直覺 gloss。每段附「為何代表語聲」理由與 burstiness/具體性標註。產一份候選清單交使用者。

- [ ] **Step 2：⛳ 使用者審定入選段落（§6-5）** — 等使用者點選哪幾段入選。

- [ ] **Step 3：把入選段落插入 `CONTENT_SPEC.md §3`**，擴充「語聲參考範文」為多段，各標關鍵特徵。

- [ ] **Step 4：驗證** — 每段確為 Ch1 已簽核原文（逐字核對，不得改數學）；四型別涵蓋；worked-solution 型已補。

- [ ] **Step 5：Commit**（授權後）

```bash
git add CONTENT_SPEC.md
git commit -m "feat(deai): §3 voice corpus 擴為多型別範文（補 worked-solution 語聲目標）"
```

---

### Task 2.5：接 Vale lint 進 CONTENT_DIRECTION ⑤ linter lane

**Files:**
- Modify: `CONTENT_DIRECTION.md`（⑤ advisory 審查迴圈）

- [ ] **Step 1：在 ⑤ 的 deterministic-linter 段補一句**：Vale AItexture 為該 lane 的一項（advisory、不擋收斂），其輸出當 prose gate Dimension C 的預標。明確標：**flag-only，決定性「擋」在 Mode B 人審 C，非此 lane**。

- [ ] **Step 2：驗證** — 與 ⑤ 既有「register 等 house rule 一律 advisory、不准擋收斂」的措辭一致、不矛盾（人工讀）。

- [ ] **Step 3：Commit**（授權後）

```bash
git add CONTENT_DIRECTION.md
git commit -m "docs(deai): CONTENT_DIRECTION ⑤ 接 Vale AItexture lint（advisory lane）"
```

---

## Phase 3 — Ch2–Ch4 定稿整合（apply，非 build）

### Task 3.1：每章定稿 Mode B 含 Dimension C

**Files:**
- Modify（逐章、逐 finding）: `handout/fragments/ch0{2,3,4}/sec-*.html`（僅經使用者裁決的 Rewrite）
- Create（每章）: `handout/_audit/REVIEW-ch0N-deai-gate1.html`（審核稿）

> 這是「用 gate」不是「建 gate」。對每章重複：

- [ ] **Step 1：跑 Vale 取該章預標**

Run: `vale handout/fragments/ch0N/sec-*.html`

- [ ] **Step 2：派 `handout-prose-audit`（含 A/B/C 三維度）審該章每節**，收 blocking（含 C 高密度叢集）＋ advisory。

- [ ] **Step 3：產 `REVIEW-ch0N-deai-gate1.html`** — 比照既有 `REVIEW-ch01-prose-audit-gate1.html` 格式（摘要表＋逐條卡片＋穩定編號）。

- [ ] **Step 4：⛳ 使用者逐條裁決 Rewrite**（propose-only，本即 Mode B 常態）。套用獲准的小修。**護欄：保留語意、不動數學。**

- [ ] **Step 5：回歸審核**（依 CLAUDE.md 2026-06-12 規則）— 對改過的節重跑一次審核，確認沒引入新問題；記錄於審核稿。

- [ ] **Step 6：重組並 Commit**（授權後）

```bash
python build.py ch0N
git add handout/fragments/ch0N/ handout/_audit/REVIEW-ch0N-deai-gate1.html
git commit -m "fix(deai): ch0N 定稿語聲收斂（Dimension C 高密度叢集歸零）"
```

> 對 Ch2、Ch3、Ch4 各跑一次本 task。

---

## Phase 4 — video gate 元件（forward-only，不碰現有實驗素材）

### Task 4.1：NARRATION-COPYEDIT 加 C6、移出 tier-3 上限

**Files:**
- Modify: `video/content_scripts/_audit/NARRATION-COPYEDIT-RUBRIC.md`

- [ ] **Step 1：在 C1–C5 之後加 C6**（逐字）：

```markdown
**C6 — AI-cadence（跨單元語聲一致）。** local C1–C5 漏掉的瀰漫性 tell：每單元重複的公式化引導語（每單元都開 `Here's the idea`／`Notice that`）、句長均勻無 burstiness、裝飾性 `not X but Y`、triadic cadence、過量 em-dash。flag 後交使用者逐筆收。
```

- [ ] **Step 2：把 C6 移出 tier-3 上限** — 在「回報規格」找到「tier 3（taste／voice drift）至多一行」，補例外：「**惟 C6 AI-cadence 不受 tier-3 一行上限**，全文報告、逐筆裁決（因 copyedit 是鎖稿前唯一去味窗口）」。

- [ ] **Step 3：驗證** — C6 措辭與 C1–C5 風格一致；與硬護欄（保留語意）不衝突（人工讀）。

- [ ] **Step 4：Commit**（授權後）

```bash
git add video/content_scripts/_audit/NARRATION-COPYEDIT-RUBRIC.md
git commit -m "feat(deai): NARRATION-COPYEDIT 加 C6 AI-cadence + 移出 tier-3 上限"
```

---

### Task 4.2：§4 引導語頻率預算

**Files:**
- Modify: `video/CONTENT_METHODOLOGY.md`（§4 Register）

- [ ] **Step 1：把軟註「別變口頭禪」改成具體預算**：在 §4 引導語段補「**頻率預算：任一引導語（`Here's the idea`／`Notice that`／`Watch what happens`…）至多每約 N 個單元出現一次**；超過由 C6 抓。」（`N` 起始值在 §6-8 拍板。）

- [ ] **Step 2：Commit**（授權後）

```bash
git add video/CONTENT_METHODOLOGY.md
git commit -m "docs(deai): §4 引導語頻率預算（避免每單元口頭禪）"
```

---

### Task 4.3：narration scope Vale 設定（待 video 重建時套用）

**Files:**
- Modify: `.vale.ini`（新增針對 `content_scripts/*.md` 的 narration scope）

- [ ] **Step 1：在 `.vale.ini` 加一段針對 narration `.md` 的設定**，掃 `narration` 欄散文，排除 `$...$`／LaTeX。複用 `AItexture` style。標註「forward-only：video 正式重建時於 copyedit 鎖稿前窗口使用」。

- [ ] **Step 2：驗證** — 對一個範例 `content_scripts/<deck>.md`（若有實驗檔）跑 `vale`，確認只掃 narration 散文、不誤砍 LaTeX。

- [ ] **Step 3：Commit**（授權後）

```bash
git add .vale.ini
git commit -m "feat(deai): narration scope Vale 設定（forward-only，待 video 重建）"
```

> **⛳ sign-off 點（§6-8）：** C6 措辭、引導語頻率預算 N 值。

---

## Self-Review（作者自審結果）

- **Spec coverage：** PLAN §4.1→Task 0.1/0.3；§4.2→0.2；§4.3→1.1/2.1；§4.4→4.1/4.2；§4.5→2.3；§4.6→2.4；§4.7→2.2；§5 Phase 0–4→Task 群；§4.1 lane 接點→2.5。Phase 3 回填＝Task 3.1。涵蓋完整。
- **Placeholder 掃描：** 門檻 `N`、引導語 `N` 為刻意留給校準＋使用者拍板（已標 ⛳ §6 連結），非漏填；其餘步驟均含實際內容/指令。
- **型別/命名一致：** `reject.txt`/`accept.txt`/`AItexture` style/`Dimension C (C1–C6)`/門檻「≥N distinct / ~500 字」全檔一致；fixture 路徑 `handout/_audit/fixtures/` 跨 task 一致。
- **TDD 適配：** build 類（Vale 設定、種子、doctor）為真 runnable 測試（fixture grep / check_seed / doctor）；doc-edit 類（rubric/README/方法論）以 seeded-fixture subagent 驗證 + 人工一致性檢查，比照你們既有 `REPORT-prose-gate-validation.md` 的 seeded-defect 做法。

---

## Execution Handoff

兩種執行方式（交新對話時擇一）：

1. **Subagent-Driven（推薦）** — 每個 task 派新 subagent、task 間 review、快迭代。REQUIRED SUB-SKILL：`superpowers:subagent-driven-development`。
2. **Inline Execution** — 同一 session 批次執行 + checkpoint。REQUIRED SUB-SKILL：`superpowers:executing-plans`。

> 新對話起手式建議：先讀 `PLAN-deai-flavor.md`（決策/規格）＋ 本檔（逐 task），再從 Phase 0 Task 0.1 開始。每個 ⛳ 點停下等使用者拍板。

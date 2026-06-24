# Route A — 全 LaTeX 文字 ＋ IBM Plex Sans 字體系統 實作計畫

> **For agentic workers:** 用 superpowers:subagent-driven-development 或 executing-plans 逐 task 執行。步驟用 `- [ ]` 追蹤。
> **驗證模型（本產線特性）：** 此管線不靠 pytest，靠 **離線抽幀（`scratch_frames.py`，零計費）＋ 目視 ＋ `lint` ＋ `sizecheck`**。每個會動視覺的 task 以「render→看圖／跑 lint+sizecheck」為驗證點。

**Goal:** 把所有螢幕文字（內文／標題／eyebrow）的 render 從 Pango `Text` 改走 LaTeX（pdflatex），以拿到正確 kerning；採 **IBM Plex Sans**（內文／標題）＋ **IBM Plex Mono**（eyebrow）＋ **Latin Modern**（數學）。navy 底與克制 spine 已完成、不在此計畫。

**Architecture:** manim `Text`（Pango）不套 kerning（已實測 `W("AVAVAV")`≈各字相加），故文字全改 `Tex`（LaTeX 會 kerning）。LaTeX 原生處理「文字＋內聯數學同行」，因此可**移除** `brand._compose` 的 Pango＋Tex baseline 對齊 hack，改成「每行一個 `Tex`（內含 `$math$`）」。字體在 TeX preamble 設定（`plex-sans`＋`plex-mono`＋`lmodern`，`familydefault=\sfdefault`），不再用 theme 的 Pango family 名。

**Tech Stack:** manim 0.20.1（`Tex`/`MathTex`，pdflatex→dvi→dvisvgm）；MiKTeX 套件 `plex-sans`／`plex-mono`／`lmodern`／`microtype`（皆本機既有，已 spike 驗證可編譯、子部件完好）。

**驗證資產：** 主測 3 景 `one_to_one_definition`（標題＋內文＋內聯數學＋display 數學）、`inverse_procedure`（步驟內聯數學＋worked）、`horizontal_line_test`（大標題＋annotation）；回歸全 §1.1 19 景。基準對照＝`video/output/_qa/route_a/B_plex_lmodern.png`（mock 目標樣式）。

---

## 開工前必讀：現況與脈絡（新對話零脈絡也能照做）

**這份計畫接續一段 2026-06-24 的探索；以下是接手所需的全部背景。**

- **倉庫：** `C:\Users\Kao\Downloads\Calculus_handout`。影片產線在 `video/`。分支目前 `experiment/seed-converge`（與本工作不對題，Task 8 會開對題分支）。
- **跑 manim 的方式：** deps 在 repo 根的 `.deps_voiceover`（manim 0.20.1）、`.deps`（PyYAML）；`video/pipeline/_bootstrap.bootstrap()` 會把它們上 `sys.path` 並設 TeX template。離線抽幀工具 `video/scratch_frames.py`（`save_last_frame`、1080p、零計費）。環境已驗：`python tools/doctor.py` 全綠（manim／MiKTeX／ffmpeg）。
- **已決定、不要再議：** navy 底（採）、克制 spine（採）、footer（暫緩、不做）、**字體＝IBM Plex Sans 內文/標題 ＋ IBM Plex Mono eyebrow ＋ Latin Modern 數學**、文字 render 走 **全 LaTeX/pdflatex**。
- **硬約束：** 只能 pdflatex。**lualatex/xelatex 會破壞 manim 的 `\special{dvisvgm:raw}` 數學子部件定址**（上色／逐步 reveal 失效、複雜式會 IndexError 崩）——已實測。所以 `newcomputermodern`（要 fontspec/lualatex）排除；數學用 `lmodern`。

**目前工作樹的「未 commit」狀態（重要——這是你的起點）：**

| 檔 | 現況 | 本計畫怎麼處理 |
|---|---|---|
| `video/pipeline/visuals/theme.py` | DARK ground 已改 **navy**（`bg=#0a1322`、`panel=#13233f`、`hairline=#22324f` 等）；`FONT_DISPLAY/FONT_BODY=NewComputerModern10`；`PX_TO_FS=0.698`/`TEX_TEXT_SCALE=1.34` 為 **NCM** 校準 | navy **保留**；字體與校準 Task 1/2/6 **改成 Plex** |
| `video/pipeline/templates/_common.py` | 已加 `DECOR_SPINE_X = SPINE_X − 0.22` ＋ `scene_spine()`（cap 追 `title.get_bottom()`） | **保留**（spine 已定案） |
| `video/pipeline/templates/__init__.py` | `build_blocks` 已注入 `scene_spine` 到所有 dark content 模板 | **保留** |
| `video/pipeline/_bootstrap.py` | 有 `_register_ncm_fonts()`（kpsewhich 註冊 `NewComputerModern10`）＋ TeX template 已是 `lmodern` 數學 | Task 1：**移除 NCM 註冊**、preamble 加 `plex-sans`/`plex-mono`；`lmodern` **保留** |
| `video/pipeline/brand.py` | `_WIDTH_K=0.0065`（NCM 校準）；文字仍走 Pango `Text`＋`_compose` | Task 2 重校 `_WIDTH_K`；Task 3-5 文字全改 `Tex` |

> 一句話：**navy＋spine 已落地且驗過、保留；NCM 是中途探索、本計畫用 Plex 取代它；數學 `lmodern` 沿用。**

- **kerning 發現（本計畫的根本動機）：** 實測 manim `Text`/`MarkupText`（Pango）**不套 kerning**（`W("AVAVAV")`≈各字寬相加），所有字體都偏鬆、sans 最明顯、數學(LaTeX)反而整齊。修法＝文字改走 LaTeX（會 kerning）＝本計畫。
- **既有 QA 報告（可參考，`output/` 已 gitignore、皆可重生）：** `video/output/_qa/REVIEW-navy-spine-render-AB.html`（navy/spine 對照）、`REVIEW-font-routeA.html`／`REVIEW-font-design.html`（字體決選）、`route_a/B_plex_lmodern.png`（**Plex+LM 目標樣式 mock**）。
- **驗證機制（本產線不用 pytest）：** `scratch_frames.py` 抽幀目視 ＋ `lint_storyboard` ＋ `sizecheck.check_scenes`。跑法見各 Task。

---

## 檔案結構（會動到的）

- `video/pipeline/_bootstrap.py` — TeX preamble 換 Plex/lmodern；移除 `_register_ncm_fonts`（不再用 Pango 文字字型）。
- `video/pipeline/brand.py` — 文字產生器全改走 `Tex`：`body_text`、`prose`（含 router）、`heading`、`heading_rich`、`eyebrow`、`prose_tex`；**移除** `_compose`／`_prose_mixed`／`_DESC_CHARS`；重校 `_WIDTH_K`。
- `video/pipeline/visuals/theme.py` — `PX_TO_FS`（重校 Plex-LaTeX）、`TEX_TEXT_SCALE`→`1.0`（全 Tex、無 Pango↔Tex 落差）、`HEADING_MATH_SCALE`（重評）、`FONT_*` Pango 名標為 unused/移除。
- `video/tools/doctor.py` ＋ `video/ENVIRONMENT.md`（根 `ENVIRONMENT.md`）— 加 `plex-sans.sty`／`plex-mono.sty`／`lmodern.sty` 檢查；移除 Times/Pango 文字字型檢查。
- `video/DESIGN.md` — 更新「Text rendering」節：全 LaTeX、Plex Sans＋LM、移除 Pango/`_compose` 敘述。

---

## 過時機制（Route A 一併移除／改）

> 2026-06-24 audit 結論：**並無**專為 kerning 寫的影片設計或程式（過去是 Pango 不 kerning、用 serif 容忍）。但有數個「因 Pango 而生」的機制在全 LaTeX 後過時。**現在不能刪**（Route A 落地前仍 load-bearing），於對應 task 移除：

- **`brand._compose` / `_prose_mixed` / `_DESC_CHARS` / 其內 `place`/`space`/`axis`/`descent`** — Pango 文字＋Tex 數學的 baseline 手動拼接。LaTeX 原生排「文字＋內聯數學同行」→ **整套移除**（Task 4）。
- **`theme.TEX_TEXT_SCALE`** — Pango↔Tex 尺寸對齊係數。全 Tex 後 Pango↔Tex 落差消失 → **設 1.0／移除**（Task 2）。
- **`brand._pango_dashes`** — Pango 不認 LaTeX dash ligature 才需。文字走 LaTeX 後 → **移除**（Task 3 改用 `_escape_tex`；Task 6 刪定義）。
- **`theme.FONT_DISPLAY/FONT_BODY/FONT_MONO`（Pango family 名）** — 無 Pango Text 後未用 → **移除/標 unused**（Task 6）。
- **保留（非 kerning、Route A 後仍需）：** `_WIDTH_K`／`estimate_text_width`／`_char_weight`／`wrap_text`（換行寬度估計，**重校** Task 2）；`PX_TO_FS`、`HEADING_MATH_SCALE`（型階校準，Task 2/5 重評）。
- **連帶解消的 advisory（記錄）：** REBUILD_STATUS 多處記過「derivation rail 文字↔inline math 邊界 spacing 偏緊」（`_compose` x-height 對齊老問題）——Route A 後由 LaTeX 原生處理，advisory 自然消失。

---

### Task 1：TeX preamble 換成 Plex＋lmodern（＋移除 Pango 字型註冊）

**Files:** Modify `video/pipeline/_bootstrap.py`

- [ ] **Step 1：改 `_set_tex_template` 的 preamble**（取代現行 `lmodern`-only/NCM 期的內容）：

```python
    tpl = TexTemplate()
    tpl.add_to_preamble(
        r"\usepackage{lmodern}" "\n"          # math = Latin Modern (locked)
        r"\usepackage{plex-sans}" "\n"        # text = IBM Plex Sans
        r"\usepackage{plex-mono}" "\n"        # mono (eyebrow) = IBM Plex Mono
        r"\renewcommand{\familydefault}{\sfdefault}" "\n"   # body default -> Plex Sans
        r"\usepackage{microtype}" "\n"        # kerning/protrusion + \textls tracking
        r"\DeclareMathOperator{\arccsc}{arccsc}" "\n"
        r"\DeclareMathOperator{\arcsec}{arcsec}" "\n"
        r"\DeclareMathOperator{\arccot}{arccot}"
    )
    config.tex_template = tpl
```

- [ ] **Step 2：移除 `_register_ncm_fonts`** 定義與 `bootstrap()` 內的呼叫（文字不再走 Pango，無需註冊 Pango 字型）。保留 `import subprocess` 若他處仍用，否則一併移除。更新模組 docstring 為「文字＋數學皆 LaTeX：Plex Sans／Plex Mono／Latin Modern」。

- [ ] **Step 3：驗證（spike 已過，再確認一次）**

Run: `python -c "import sys,os;[sys.path.insert(0,os.path.join(r'C:\Users\Kao\Downloads\Calculus_handout',d)) for d in ('.deps_voiceover','.deps')];os.chdir(r'C:\Users\Kao\Downloads\Calculus_handout');sys.path.insert(0,'video');from pipeline import _bootstrap;_bootstrap.bootstrap();from manim import Tex,MathTex;print('OK',len(MathTex('a','=','b').submobjects))"`
Expected: `OK 3`（子部件定址完好）。

- [ ] **Step 4：commit**（分支見 Task 8）：`feat(video): Route A preamble — Plex Sans/Mono text + lmodern math via LaTeX`

---

### Task 2：量測 ＋ 設定校準常數（Plex-via-LaTeX）

**Files:** 量測腳本（一次性，量完刪）；Modify `video/pipeline/visuals/theme.py`、`video/pipeline/brand.py`

- [ ] **Step 1：量 Plex-LaTeX 度量**（一次性腳本）：對 `Tex` 量 cap-height/fs 與 per-char 寬、確認全 Tex 後 Pango↔Tex 落差消失。

```python
# bootstrap() 後：
from manim import Tex
fs=100.0
H = Tex(r'H').height/fs                       # Plex-LaTeX cap height per fs
s='A function is one-to-one when different inputs'
w = Tex(s.replace(' ', r'\ ')).width          # 用 \  保留空格寬
print('H/fs=',H, 'w_per_char=', w/ (sum(0.5 if c==' ' else 1 for c in s)*fs))
```

- [ ] **Step 2：設常數**（依量到的值）：
  - `theme.PX_TO_FS = round(0.72*0.00920/H, 4)`（維持 cap height 與 Times 校準一致；填入實量 H）。
  - `brand._WIDTH_K = round(w_per_char*1.02, 5)`（Plex-LaTeX 實量＋2% 安全邊際；治 wrap 溢出）。
  - `theme.TEX_TEXT_SCALE = 1.0`（全文字皆 Tex，無 Pango↔Tex 尺寸落差；註解說明歷史值 1.34/1.36 作廢）。
  - `theme.HEADING_MATH_SCALE`：暫設 `1.0`，Task 5 render 帶數學標題後再定（LaTeX 原生內聯數學通常不需縮）。

- [ ] **Step 3：驗證**：印出設定後的常數值；本 task 無視覺輸出。commit：`chore(video): recalibrate type constants for Plex-via-LaTeX`

---

### Task 3：`brand.body_text` 改走 LaTeX（純文字內文）

**Files:** Modify `video/pipeline/brand.py`（`body_text`）

- [ ] **Step 1：改寫 `body_text`** — `mk(line)` 由 `Text(...)` 改為 `Tex(line, color=col, font_size=T.fs(size))`（familydefault 已是 Plex Sans）。`_pango_dashes` 改為 LaTeX-safe escape（`_escape_tex` 已存在）；wrap 邏輯（`estimate_text_width` 插 `\n`→改為逐行 `Tex` 再 `arrange(DOWN, aligned_edge=LEFT)`）沿用，但每行是 `Tex`。移除 `weight=` 參數（LaTeX 用 `\textbf`，body 不需）。

- [ ] **Step 2：render 驗證**

Run: `python video/scratch_frames.py --storyboard video/storyboards/ch01_inverse_functions.yml --scene one_to_one_definition --out video/output/_qa/A_step3`
看圖：`video/output/_qa/A_step3/one_to_one_definition.png` — 定義句為 Plex Sans、**kerning 緊實均勻**、不溢出、上偏置中正常。
Expected：對比 `route_a/B_plex_lmodern.png` 的內文質感一致。

- [ ] **Step 3：commit**：`feat(video): body_text via LaTeX (Plex Sans, kerned)`

---

### Task 4：`prose`／`heading_rich` 改純 LaTeX，移除 `_compose` hack

**Files:** Modify `video/pipeline/brand.py`（`prose`、`_prose_mixed`、`_compose`、`heading_rich`、`prose_tex`）

- [ ] **Step 1：`prose` 路由簡化**：所有 prose（含內聯 `$math$`）統一走「逐行 `Tex`（行內含 `$...$`）」。`Tex` 在 text mode 原生排「文字＋內聯數學同行」、baseline 正確、kerned。wrap：先用 `estimate_text_width`（已重校）切行（math span 視為 atomic、用近似寬），每行一個 `Tex`，`arrange(DOWN, buff, aligned_edge=LEFT)`。保留 `_mark_prose` 標記（sizecheck 用）。

- [ ] **Step 2：移除** `_compose`、`_prose_mixed`、`_DESC_CHARS`、`prose_tex` 內的 `\mbox` 特例若不再需要（改由統一路徑處理）。`heading_rich` 改為「`Tex(\textbf{...}$math$...)` 單行、超寬則 `scale_to_fit_width`」。

- [ ] **Step 3：render 驗證**（內聯數學最吃重的場景）

Run: `python video/scratch_frames.py --storyboard video/storyboards/ch01_inverse_functions.yml --scene inverse_procedure,invert_a_cubic,recap --out video/output/_qa/A_step4`
看圖：① `inverse_procedure` 步驟句「Write $y=f(x)$.」文字 sans＋數學 LM 同行、kerned、不錯位；② `invert_a_cubic` 標題「Inverting a Cubic」＋ derivation 內聯；③ `recap` 點含 `$y=x$`。皆無 garble、無溢出。
Expected：文字↔數學同行乾淨；無 `_compose` 殘留錯位。

- [ ] **Step 4：commit**：`refactor(video): pure-LaTeX prose+heading_rich, drop Pango/_compose baseline hack`

---

### Task 5：`heading` ＋ `eyebrow` 改 LaTeX（Plex Bold 標題、Plex Mono eyebrow）

**Files:** Modify `video/pipeline/brand.py`（`heading`、`eyebrow`）

- [ ] **Step 1：`heading`** → `Tex(r"\textbf{" + escaped + "}", font_size=T.fs(size))`（Plex Sans Bold）。移除 Pango `weight=SEMIBOLD`。

- [ ] **Step 2：`eyebrow`** → `Tex(r"\texttt{" + escaped_upper + "}", ...)`（Plex Mono）；tracking 用 microtype `\textls[160]{...}` 還原原本字距感（或先不加、Task 7 目視再定）。

- [ ] **Step 3：`HEADING_MATH_SCALE` 定值**：render 帶數學標題（`shape_can_mislead`/`invert_a_cubic`/`first_inverses`），若內聯數學相對標題過大才調，否則維持 `1.0`。

- [ ] **Step 4：render 驗證**

Run: `python video/scratch_frames.py --storyboard video/storyboards/ch01_inverse_functions.yml --scene one_to_one_definition,horizontal_line_test,first_inverses --out video/output/_qa/A_step5`
看圖：eyebrow＝Plex Mono tracked、標題＝Plex Bold kerned、含數學標題比例正常。
Expected：與 `route_a/B_plex_lmodern.png` 一致。

- [ ] **Step 5：commit**：`feat(video): heading=Plex Bold, eyebrow=Plex Mono via LaTeX`

---

### Task 6：theme.py 收尾 ＋ DESIGN.md 更新

**Files:** Modify `video/pipeline/visuals/theme.py`、`video/DESIGN.md`

- [ ] **Step 1：theme.py**：`FONT_DISPLAY`/`FONT_BODY`/`FONT_MONO`（Pango 名）標註「unused — 字體於 TeX preamble 設定」或移除（確認 grep 無他處引用：`grep -rn "FONT_BODY\|FONT_DISPLAY\|FONT_MONO\|FONTS" video/pipeline`，只移除因本改動而未用者）。確認 `PX_TO_FS`/`TEX_TEXT_SCALE`/`HEADING_MATH_SCALE` 為 Task 2/5 定值＋註解。
- [ ] **Step 2：DESIGN.md**「Text rendering：prose vs math」節**重寫**：全文字走 LaTeX（Plex Sans）＋數學 LM；移除 Pango `Text`／`_compose`／`TEX_TEXT_SCALE` 1.36 等過期敘述（與 2026-06-24 Step 0 修過的 `body_text`=Pango 描述一併更新為「Route A：全 LaTeX」）。
- [ ] **Step 3：commit**：`docs(video): DESIGN.md text-rendering = all-LaTeX Plex; theme cleanup`

---

### Task 7：全 §1.1 回歸（render＋lint＋sizecheck＋目視）

**Files:** 無（驗證）；如有容量溢出再回對應 template 微調

- [ ] **Step 1：lint＋sizecheck 全章**

Run（既有片段）：載入 `ch01_inverse_functions.yml`，跑 `lint_storyboard` ＋ `check_scenes`。
Expected：`lint` 0 error；`sizecheck` 0 error（warn 逐一檢視——Plex 寬度與 NewCM 不同，recap 等可能再現/消失，視 `_WIDTH_K` 重校後而定）。

- [ ] **Step 2：render 全 19 景**

Run: `python video/scratch_frames.py --storyboard video/storyboards/ch01_inverse_functions.yml --scene all --out video/output/_qa/A_full`
逐幀目視：kerning、無溢出、masthead/spine/navy 一致、數學唸法不變、glyph(✓✗∎) 正常。

- [ ] **Step 3：修容量回歸**：若某景溢出 safe margin（如 recap 點過長），於該 template 微調間距／或標 `part` 拆頁（**勿縮字**，house rule）。每修一景重 render 該景比對。

- [ ] **Step 4：產 HTML 報告**（CLAUDE.md：完成一輪要產雙擊即開報告）：`video/output/_qa/REVIEW-routeA-applied.html`，逐景前（NewCM/Times）後（Plex-LaTeX）對照 ＋ lint/sizecheck 結果。

- [ ] **Step 5：commit**：`test(video): §1.1 full regression for Route A (lint/sizecheck clean, frames verified)`

---

### Task 8：doctor.py ＋ ENVIRONMENT.md（新依賴入文檔）＋ 分支/commit 收尾

**Files:** Modify `video/tools/doctor.py`（或根 `tools/doctor.py`）、`ENVIRONMENT.md`

- [ ] **Step 1：doctor.py**：fonts 區把「Times New Roman 可見」改/補為檢查 LaTeX 套件 `kpsewhich plex-sans.sty`／`plex-mono.sty`／`lmodern.sty` 存在（文字＋數學現在都靠這些）。Courier New 檢查視 eyebrow 是否仍需而定（已改 Plex Mono → 可移除）。
- [ ] **Step 2：ENVIRONMENT.md**：記「video 文字＋數學皆 LaTeX；需 MiKTeX 套件 `plex` bundle（plex-sans/plex-mono）＋`lmodern`＋`microtype`」。驗收＝新機 `python tools/doctor.py` 全綠。
- [ ] **Step 3：分支**：本工作（navy/spine/字體 Route A）目前在 `experiment/seed-converge`（不對題）。開對題分支 `video/template-redesign-plex-routeA`（或 user 指定），把累積改動歸位。
- [ ] **Step 4：最終 commit ＋ 更新 TODO**：TODO 標 Route A 完成；`REBUILD_STATUS.md` 補一筆。commit：`chore(video): doctor/ENVIRONMENT for Plex+lmodern LaTeX deps`

---

## Self-review 註記
- **涵蓋**：preamble(T1)、校準(T2)、body(T3)、prose/heading_rich(T4)、heading/eyebrow(T5)、theme/DESIGN(T6)、回歸(T7)、env/commit(T8)——對應 spec 全部要素。
- **風險點**：① `_compose` 移除後內聯數學 baseline 由 LaTeX 接管（spike 已示可行，T4 render 把關）；② `_WIDTH_K` 重校不準會 wrap 溢出（T2 量測＋T3/T7 render 把關）；③ eyebrow tracking 還原（T5，非阻擋）。
- **不動**：navy 底、克制 spine、四色語意、容量契約機制、math 唸法。math 字體 = Latin Modern（已鎖）。

# 環境統一指南（每台機器要備什麼）

> 作者常在多台電腦間切換，各機已裝的東西不一。本檔是**整個 repo 環境需求的權威清單**；
> [`tools/doctor.py`](tools/doctor.py) 是它的可執行版（一行看出這台缺什麼），
> [`tools/setup.ps1`](tools/setup.ps1) 把 Python 端一鍵備妥。
> 目的：**換機後 agent 不要再花時間重新踩環境坑。**

## 換機後就做這兩件事

```powershell
# 1) 備妥 Python 端（建 .venv、裝鎖定版依賴），然後自動跑健檢
powershell -ExecutionPolicy Bypass -File tools\setup.ps1

# 2) 任何時候想知道「這台缺什麼、怎麼補」
python tools\doctor.py
```

`doctor.py` 是**純 stdlib、任何 python 都能跑**（venv 還沒建也能跑），會逐項印 `[ OK ]／[WARN]／[FAIL]`
與**確切補法**，最後給「能力摘要」告訴你現在哪些工作流跑得動。有 `[FAIL]` 時退出碼為 1。

## 環境分層（四層核心 ＋ 審核工具）

| 層 | 內容 | 怎麼統一 |
|---|---|---|
| **① Python 套件** | 共用 `.venv`（manim 0.20.1、PyYAML、ManimPango、Pillow、imageio-ffmpeg、fonttools、pymupdf…） | `setup.ps1` 從 [`requirements.lock`](requirements.lock) 精確重現 |
| **② 系統 binary** | `ffmpeg`、`ffprobe` | 每台 `winget install --id Gyan.FFmpeg -e`（**含 ffprobe**） |
| **③ LaTeX** | MiKTeX：`latex`、`dvisvgm` + `plex-sans`/`plex-mono`/`lmodern`/`microtype`（Route A：video 文字＋數學皆走 LaTeX；MiKTeX 首編自動補裝） | 每台裝 MiKTeX（manim 的 Tex/MathTex 沒有它就編不出來；無 code 繞法） |
| **①b 影片字型** | **全走 LaTeX**：文字 IBM Plex Sans/Mono、數學 Latin Modern（套件見 ③）。**不再用 Pango 系統字型**（Times/Courier 已棄） | 無需安裝系統字型；只要 ③ 的 MiKTeX 套件在即可（`doctor.py` 以 kpsewhich 驗）。video 不 vendored 任何字型 |
| **④ Node + 瀏覽器** | Node ≥21、Google Chrome（給 `handout/html/_render/shot.mjs` 截圖） | 每台裝 Node LTS + Chrome |
| **⑤ codex（審核工具，選用）** | Mode B 講義審核／video gate2 用的 `codex` CLI | 部署版控的 [`tools/codex.cmd`](tools/codex.cmd) shim（解 PATH＋stale-launcher 兩坑）；見下方 ⑤ |
| **⑤b Vale（去 AI 味 lint，選用）** | 散文 AI-tell flag 引擎（markup-aware，自動排除 `$...$`／LaTeX／code）；handout prose 與 video narration 去 AI 味用（[`PLAN-deai-flavor.md`](authoring/_archive/deai/PLAN-deai-flavor.md)） | 每台 `winget install errata-ai.Vale`；**flag-only／advisory**，缺它不擋核心產線（同 codex，WARN 不 FAIL）。見下方 ⑤b |
| **⑤c forced alignment（選用）** | `video/experiments/forced_alignment_dean/` 的本機 word-level timestamps，將整段 Dean 音訊對回 storyboard beats：`stable-ts`（transcript-constrained，**計時來源**）＋`whisper_timestamped`（自由 ASR，**QA 探針**） | 每台全局安裝一次：`python -m pip install --upgrade whisper-timestamped stable-ts`；第一次跑 `base.en` 會下載 Whisper model cache。缺它不擋核心產線，`doctor.py` 只 WARN |
| **祕鑰** | `MIMO_API_KEY` / `GEMINI_API_KEY` / `OPENAI_API_KEY` / `DEEPSEEK_API_KEY` | per-machine 設環境變數；**不進版控**（計費 API，依 [`CLAUDE.md`](CLAUDE.md) 徵同意） |

## 一次性安裝（每台機器各做一次）

本機驗證過的版本：Python 3.12.10、Node v24、MiKTeX、ffmpeg 8.1.1、Vale 3.15.1（選用）、whisper-timestamped 1.15.9 / openai-whisper 20250625 / stable-ts 2.19.1 / torchaudio 2.11.0（forced-alignment 實驗用）。

```powershell
# Python（lock 以 3.12 凍結，請用 3.12 以免 wheel 不相容）
winget install Python.Python.3.12

# ffmpeg 全套（含 ffprobe）— 裝完開「新的」shell 讓 PATH 生效
winget install --id Gyan.FFmpeg -e

# Node LTS（shot.mjs 用 global WebSocket/fetch，需 ≥21）
winget install OpenJS.NodeJS.LTS

# Google Chrome（shot.mjs 用 CDP 截圖）
winget install Google.Chrome

# Vale（去 AI 味散文 lint；選用，跑 PLAN-deai-flavor 的 prose lint 才需要）— 裝完開新 shell 讓 PATH 生效
winget install --id errata-ai.Vale -e

# forced alignment（選用，video 實驗線用；全局裝，方便任何 thread 直接呼叫）
python -m pip install --upgrade whisper-timestamped stable-ts

# LaTeX：裝 MiKTeX（https://miktex.org）。latex/dvisvgm 會進 PATH；
# video 文字＋數學皆走 LaTeX，需 plex(plex-sans/plex-mono)/lmodern/microtype 套件
# （MiKTeX 首次編譯自動補裝；只能 pdflatex）。
```

裝完跑 `tools\setup.ps1` 補 Python 端，再 `python tools\doctor.py` 應全綠。

## 各層細節與「為什麼」

### ① Python — 共用 `.venv`，以 lock 為準
- **單一來源：** 全 repo 共用 repo 根的 `.venv`。`pipeline/_bootstrap.py` 若偵測到舊的 vendored
  `.deps*` 目錄會**優先**它、可能蓋掉 venv 的 pin——**新機請不要重建 `.deps*`，只用 `.venv`**，
  來源才單一、不會悄悄版本漂移。
- **精確重現：** [`requirements.lock`](requirements.lock)（`pip freeze` 全圖、精確 `==`）是安裝權威。
  各區的人讀版直接依賴清單：[`video/requirements.txt`](video/requirements.txt)、
  [`authoring/seed_converge/requirements.txt`](authoring/seed_converge/requirements.txt)。
- **曾漏裝、現已納入：** `fonttools`（logo 外框一次性工具）、`pymupdf`/`fitz`（authoring 圖稽核）
  以前沒宣告也沒裝，換機重跑會 ImportError；現都進 lock。
  2026-07-17 起這兩個**還背著 LaTeX 出版線的字形閘**（[`handout/latex/check_glyphs.py`](handout/latex/check_glyphs.py)，
  KICKOFF §4.5 閘 4）：fonttools 讀原始字型輪廓、pymupdf 讀 PDF 嵌入字型。缺了閘跑不動，
  而該閘擋的是「PDF 文字層全對、印出來是別的字」這種 pdftotext 驗不出來的病（沿革見 KICKOFF
  狀態區塊的 Inter node-mode bug）——別因為它們在 doctor 裡標 optional 就跳過不裝。

### ② ffmpeg / ffprobe — 裝真正的全套（策略 A）
- `make.py` 的 compose 與 `critic.py` 抽幀用**裸名** `ffmpeg`／`ffprobe` 呼叫，必須在 PATH 上。
- **`ffprobe` 是過去的硬卡點：** `imageio-ffmpeg` 與舊的 `.venv\ffmpeg_shim` 都**只給 ffmpeg、不給 ffprobe**；
  缺它時 `make.py` render 後的時長健檢（`_probe_duration`）會 `FileNotFoundError` 直接崩、**compose 不跑＝沒有合併成片**。
- **統一作法：** 每台 `winget install --id Gyan.FFmpeg -e` 裝 Gyan 全套（ffmpeg＋ffprobe＋ffplay），兩者一起進 PATH。
  **裝了系統 ffmpeg 後，舊的 `.venv\ffmpeg_shim` 變多餘，可不再依賴。**

### ③ LaTeX — MiKTeX，沒有 code 繞法
- manim 的每個 `Tex`／`MathTex` 都要走真 TeX：`latex → .dvi → dvisvgm → svg`。
- `pipeline/_bootstrap.apply_tex_template()` 設的全域 TeX template 用 **`plex-sans` + `plex-mono`**（文字，`familydefault=\sfdefault`）
  **+ `lmodern`**（數學）**+ `microtype`**（kerning），外加 `\DeclareMathOperator` 三個反三角 operator（Route A，2026-06-24：
  所有螢幕文字＋數學都走 LaTeX 以拿到 kerning）。MiKTeX 首次編譯會自動補裝這些套件。**硬約束：只能 pdflatex**——
  lualatex/xelatex 會破壞 manim 的 `\special{dvisvgm:raw}` 數學子部件定址，故排除需 fontspec 的 `newcomputermodern`。
  （`newtx` 已不再是 video 需求，但仍是 `legacy/tex_handout/` 的需求。）
- handout 的 HTML 講義**不需要** LaTeX（數學走 MathJax/KaTeX CDN）；`video/` render 需要 pdflatex 路徑，
  出版排版線（`handout/latex/`）另需 lualatex 路徑（見 ③b）——同一套 MiKTeX、兩條互不干擾。
- **踩坑（2026-06-25）：Plex 文字 render 成空白／場景一開頭 `IndexError` 崩。** 症狀：含文字的場景 render 崩在
  `IndexError: too many indices for array`（標題 Tex 沒有任何點），或 latex 印 `'miktex-makemf.exe…plxSans-…mf'
  is not recognized`。**不是缺套件**——`kpsewhich plex-sans.sty` 找得到——而是這台 MiKTeX 的**字型檔名庫（FNDB）
  stale**：latex 找不到已裝的 Plex `.tfm`，就 fallback 去壞掉的 `makemf`，glyph 描成空白。修法：
  ```powershell
  initexmf --update-fndb     # 刷新檔名資料庫，latex 才找得到已裝的 Plex .tfm
  initexmf --mkmaps          # 重建字型 map（dvisvgm 描 Type1 外框要它）
  ```
  修完**還要刪 manim 的 Tex 快取** `media/Tex/`——壞掉時期那批空白 svg 會被 manim 依 hash 沿用，不清就還是空。
  `doctor.py` 的「Plex Tex 實編非空」檢查（`check_tex_compiles`）會實 build 一個 Plex Tex 抓這個坑（kpsewhich 查
  `.sty` 在 ≠ 編得出字）。另：MiKTeX 一直印「you have not checked for updates as a MiKTeX user」是同源警告，
  開一次 MiKTeX Console → Check for updates 可消。

### ③b handout LaTeX 出版排版線 — lualatex + memoir + NCM + vendored Inter
- **這條線是講義的出版排版（`handout/latex/`，[`handout/latex/KICKOFF-latex-pilot.md`](handout/latex/KICKOFF-latex-pilot.md)）**：
  fragment 經 `convert.py` 確定性轉換 → `template/calcbook.sty`（memoir）→ `latexmk -lualatex` 出 A4 PDF。
  與 video 的「只能 pdflatex」硬約束**不衝突**——兩條線各走各的引擎，同一套 MiKTeX。
- 需求全在 MiKTeX 內：`lualatex`／`latexmk` 內建；`newcomputermodern`（本文＋數學字體）首次編譯自動補裝；
  `pdftotext`（完整性閘 `check_prose.py`）MiKTeX 也自帶（poppler 系工具）。
- **UI sans＝vendored Inter（2026-07-16，M-B1 議題⑦ 拍板）**：字體檔在
  `handout/latex/template/fonts/inter/`（六字重 OTF＋OFL 授權，來源＝rsms/inter release v4.1 的
  `extras/otf`），`calcbook.sty` 以 `fontspec Path=` 載入。**隨 repo 走、換機零安裝**；對映 HTML 側的
  Inter（圖內標籤已嵌同字體，本文側圖說用它才同族）。
- `doctor.py` 的 `check_handout_latex`（區名 `handout-tex`）驗上述全部：lualatex／latexmk／pdftotext 在 PATH、
  `kpsewhich NewCM10-Regular.otf` 可尋、vendored Inter 六檔在。

### ①b 影片字型 — 全走 LaTeX（Plex Sans/Mono 文字 + Latin Modern 數學）
- Route A（2026-06-24）後，影片**所有螢幕文字＋數學都走 LaTeX/pdflatex**：文字 **IBM Plex Sans**（標題/內文）+ **IBM Plex Mono**
  （eyebrow/標籤），數學 **Latin Modern**。字體在 ③ 的 preamble 設定，**不再經 Pango、不用任何系統字型**（舊的 Times New Roman／
  Courier New 已棄）。根因：manim `Text`（Pango）不套 kerning，LaTeX 會。
- `doctor.py` 的 `check_fonts` 改以 **kpsewhich 驗 `plex-sans.sty`／`plex-mono.sty`／`lmodern.sty`／`microtype.sty`** 存在（缺了含
  文字／數學的場景會編譯失敗或 fallback）。
- **影片不 vendored 任何字型。** Direction D 的 vendored 設計字型早於 2026-06-20 清理移除；`fonttools` 仍是依賴（logo 外框工具
  `pipeline/assets/_outline_text.py` 用）。

### ④ Node + Chrome — 只給 handout 圖 render 用
- [`handout/html/build.py`](handout/html/build.py) 組裝 HTML 是**純 Python stdlib**，任何 python 都能跑、無額外需求。
- [`handout/html/_render/shot.mjs`](handout/html/_render/shot.mjs)（render `.sheet` 成 PNG 餵 figure 稽核）需要
  **Node ≥21**（global WebSocket/fetch）＋ **Google Chrome**。Chrome 路徑現在會先讀 `CHROME` 環境變數、
  再退回常見安裝位置（不再寫死單一路徑）。
- standalone HTML **檢視時需連網**載 MathJax/KaTeX CDN（非安裝需求）。

### ⑤ codex — 審核工具（Mode B 講義審核 / video gate2）

`codex` 常因「裝了但不在 PATH」在 agent 的**非互動 shell** 裡找不到。兩個關鍵觀念：

- **非互動 shell 只看持久（registry）的 User/Machine PATH，不載你互動 shell 的 profile／alias。**
  所以「互動視窗叫得動 codex」不代表 agent 叫得動——若 codex 的目錄只加在 profile、或根本沒進持久 PATH，agent 就找不到。
- **codex 的真 binary 在 `%LOCALAPPDATA%\OpenAI\Codex\bin\<hash>\codex.exe`，`<hash>` 每次自更新都變、每台機器也不同**；
  頂層穩定命名的 `bin\codex.exe` 可能是舊 build（會拒 `service_tier=priority` 等新 config key）。**絕不要寫死 `<hash>` 路徑。**

**統一作法——版控一支 shim [`tools/codex.cmd`](tools/codex.cmd)：** 把它放進**已在持久 PATH 的 npm 目錄**（`%APPDATA%\npm`），
它每次呼叫時動態解析 `OpenAI\Codex\bin` 底下**最新**的 `codex.exe`，一次解掉 PATH 與 stale-launcher 兩坑。

```powershell
# 一次性部署（每台機器）。tools\setup.ps1 會在 codex 還不在 PATH 時自動做這步。
copy tools\codex.cmd "%APPDATA%\npm\codex.cmd"
```

- 兩台機器這條指令**一模一樣**（`%APPDATA%`／`%LOCALAPPDATA%` 都按使用者展開），所以**不必管實際路徑差異**。
- codex 本體走它自己的安裝／自更新管道（自更新到 `%LOCALAPPDATA%\OpenAI\Codex\bin`）；shim 只負責「找得到 ＋ 找最新」。
- 換機後 `python tools\doctor.py` 會判定 codex 是「在 PATH／裝了但沒部署 shim／沒裝」哪一種，並給對應補法。

### ⑤b Vale — 去 AI 味散文 lint（選用、flag-only）

去 AI 味方案（[`PLAN-deai-flavor.md`](authoring/_archive/deai/PLAN-deai-flavor.md)）的決定性 lint 引擎。選 Vale 的理由：**markup-aware**（自動排除 `$...$`／`\(...\)`／LaTeX 命令／`<code>`，數學符號不會淹沒訊號）、單一 Go binary、跨平台、零 AI-detector 風險。

- **裝法（每台機器一次）：** `winget install --id errata-ai.Vale -e`（備援 `scoop install vale`，或自 <https://github.com/errata-ai/vale/releases> 下載 binary 放 PATH）。裝完開新 shell 讓 PATH 生效。**pinned 版本：3.15.1。**
- **定位：永遠 flag-only／advisory。** 嚴重度設 `warning`/`suggestion`、**不設 `error`**；決定性「擋不擋」交給 Mode B 人審維度 C，不在此。所以缺它不擋核心產線——`doctor.py` 判 **WARN 不 FAIL**（同 codex）。
- 設定檔（`.vale.ini` + `styles/AItexture/` + `reject.txt`/`accept.txt`）隨 repo 進版控；裝好 binary 即可對 fragment 跑 `vale <file>`。
- 換機後 `python tools\doctor.py` 的 `vale` 區會判「在 PATH／未安裝」並給補法。

### ⑤c forced alignment — 本機 word timestamps（選用）

`video/experiments/forced_alignment_dean/` 測「整段 Dean 音訊 → 對位 → storyboard beat durations → render/mux」的路線。這不是核心成片產線必需，所以缺了只在 `doctor.py` 顯示 WARN，不會讓一般 `make.py`／MiMo beat 流程 FAIL。兩個工具、兩種角色（2026-07-05 三場景實測拍板，詳見 [`RESULTS-2026-07-05.md`](video/experiments/forced_alignment_dean/RESULTS-2026-07-05.md)）：

- **`stable-ts`＝計時來源：** transcript-constrained forced alignment（`stable_whisper.align()`），被 plan transcript 約束、結構上不可能漏字，每字附 timestamp＋機率。wrapper：[`run_stable_ts_align.py`](video/experiments/forced_alignment_dean/run_stable_ts_align.py)。
- **`whisper_timestamped`＝QA 探針：** 自由 ASR＋DTW timestamps。ASR decoder 對重複的數學公式片語會跳字（實測 derivation 場景漏 12 字、後續 beat 全部錯位），**不可當計時來源**；改當獨立 QA——拿 ASR 文字 diff transcript，抓「TTS 沒唸／唸錯」這類 FA 結構上看不到的錯。wrapper：[`run_whisper_timestamped.py`](video/experiments/forced_alignment_dean/run_whisper_timestamped.py)。

- **裝法（每台機器一次，全局）：** `python -m pip install --upgrade whisper-timestamped stable-ts`。pip 會安裝 `whisper_timestamped` CLI、`openai-whisper`、`dtw-python`、`numba`、`tiktoken`、`torchaudio` 等依賴。
- **模型快取：** 兩者共用 openai-whisper 的 model cache（`base.en` 約 139 MB，第一次跑會下載；之後可離線重用）。模型下載不是計費 API，但仍需要網路。
- **目前驗證版本：** `whisper-timestamped 1.15.9`、`openai-whisper 20250625`、`stable-ts 2.19.1`（連帶裝 `torchaudio 2.11.0`）。
- **上游狀態注意：** `stable-ts` 上游（jianfch/stable-ts）已於 2026-05-30 封存（read-only、無後繼專案）。本機已驗證可用，故釘住上述版本組合；若未來 whisper／torch 升版造成不相容，備援路線是 `torchaudio` 的 CTC forced alignment（torchaudio 已隨 stable-ts 進環境）。

### 祕鑰
- 全部走環境變數，**永不進版控、不寫檔、不記 log**。`.env` 已 gitignored。
- 離線路徑不需要 key：`make.py --backend mock`、`tts.py --backend mock`、`critic.py --dry-run`、
  `doctor.py`。批次計費前依 [`CLAUDE.md`](CLAUDE.md) 報用量徵同意。

## 在用 / 不在用

- **在用：** `video/`（影片產線）、`handout/html/`（HTML 講義 + `_render/shot.mjs`）、
  `authoring/seed_converge/`（圖稽核 R&D，當前 `experiment/seed-converge` 分支）。
- **凍結（不在 doctor 檢查範圍）：** `legacy/tex_handout/tools/`（第一代 LaTeX 講義 linter）、
  `legacy/` 其餘第一代產物。要跑它們才另需完整 TeX，平時不需要。

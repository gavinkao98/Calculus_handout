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
| **③ LaTeX** | MiKTeX：`latex`、`dvisvgm` + `newtxtext`/`newtxmath`（video 數學 Times，2026-06-20 字型 revert 後；MiKTeX 首編自動補裝） | 每台裝 MiKTeX（manim 的 Tex/MathTex 沒有它就編不出來；無 code 繞法） |
| **①b 影片字型** | **Times New Roman**（標題/散文）+ **Courier New**（eyebrow/標籤）= Windows 系統字型；數學走 newtx（LaTeX，見 ③） | Windows 內建、無需安裝。（Direction D 的 Inter Tight/JetBrains Mono 仍 vendored 於 [`video/pipeline/assets/fonts/`](video/pipeline/assets/fonts) 但目前未用——換回時即可用） |
| **④ Node + 瀏覽器** | Node ≥21、Google Chrome（給 `handout/_render/shot.mjs` 截圖） | 每台裝 Node LTS + Chrome |
| **⑤ codex（審核工具，選用）** | Mode B 講義審核／video gate2 用的 `codex` CLI | 部署版控的 [`tools/codex.cmd`](tools/codex.cmd) shim（解 PATH＋stale-launcher 兩坑）；見下方 ⑤ |
| **祕鑰** | `MIMO_API_KEY` / `GEMINI_API_KEY` / `OPENAI_API_KEY` / `DEEPSEEK_API_KEY` | per-machine 設環境變數；**不進版控**（計費 API，依 [`CLAUDE.md`](CLAUDE.md) 徵同意） |

## 一次性安裝（每台機器各做一次）

本機驗證過的版本：Python 3.12.10、Node v24、MiKTeX、ffmpeg 8.1.1。

```powershell
# Python（lock 以 3.12 凍結，請用 3.12 以免 wheel 不相容）
winget install Python.Python.3.12

# ffmpeg 全套（含 ffprobe）— 裝完開「新的」shell 讓 PATH 生效
winget install --id Gyan.FFmpeg -e

# Node LTS（shot.mjs 用 global WebSocket/fetch，需 ≥21）
winget install OpenJS.NodeJS.LTS

# Google Chrome（shot.mjs 用 CDP 截圖）
winget install Google.Chrome

# LaTeX：裝 MiKTeX（https://miktex.org）。latex/dvisvgm 會進 PATH；
# video 數學用 Computer Modern（LaTeX base 內建，無需額外套件）。
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

### ② ffmpeg / ffprobe — 裝真正的全套（策略 A）
- `make.py` 的 compose 與 `critic.py` 抽幀用**裸名** `ffmpeg`／`ffprobe` 呼叫，必須在 PATH 上。
- **`ffprobe` 是過去的硬卡點：** `imageio-ffmpeg` 與舊的 `.venv\ffmpeg_shim` 都**只給 ffmpeg、不給 ffprobe**；
  缺它時 `make.py` render 後的時長健檢（`_probe_duration`）會 `FileNotFoundError` 直接崩、**compose 不跑＝沒有合併成片**。
- **統一作法：** 每台 `winget install --id Gyan.FFmpeg -e` 裝 Gyan 全套（ffmpeg＋ffprobe＋ffplay），兩者一起進 PATH。
  **裝了系統 ffmpeg 後，舊的 `.venv\ffmpeg_shim` 變多餘，可不再依賴。**

### ③ LaTeX — MiKTeX，沒有 code 繞法
- manim 的每個 `Tex`／`MathTex` 都要走真 TeX：`latex → .dvi → dvisvgm → svg`。
- `pipeline/_bootstrap.py` 設的全域 TeX template 用 **`newtxtext` + `newtxmath`**（Times 風數學，2026-06-20 字型自
  Direction D 的 CM revert 回 Times New Roman 後），外加 `\DeclareMathOperator` 三個反三角 operator。MiKTeX 首次編譯
  會自動補裝 newtx；newtx 同時也是 `legacy/tex_handout/` 的需求。
- handout 的 HTML 講義**不需要** LaTeX（數學走 MathJax/KaTeX CDN）；只有 `video/` render 需要。

### ①b 影片字型 — Times New Roman / Courier New（Windows 系統字型）
- 影片目前用 **Times New Roman**（標題/散文）+ **Courier New**（eyebrow/標籤），皆 Windows 內建系統字型、**無需安裝**；
  數學走 LaTeX newtx（見 ③）。`doctor.py` 驗 manimpango 看不看得到 `Times New Roman`／`Courier New`（Pango 找不到會靜默 fallback）。
- **影片不再 vendored 任何字型。** Direction D 的 vendored 設計字型（Inter Tight／JetBrains Mono／Computer Modern `cmun*.otf`）
  與 `_bootstrap.register_design_fonts()` 已於 2026-06-20 Times revert 的「舊設計清理」中**移除**（`video/pipeline/assets/fonts/` 已刪）。
  `fonttools` 仍是依賴（logo 外框工具 `pipeline/assets/_outline_text.py` 用）。

### ④ Node + Chrome — 只給 handout 圖 render 用
- [`handout/build.py`](handout/build.py) 組裝 HTML 是**純 Python stdlib**，任何 python 都能跑、無額外需求。
- [`handout/_render/shot.mjs`](handout/_render/shot.mjs)（render `.sheet` 成 PNG 餵 figure 稽核）需要
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

### 祕鑰
- 全部走環境變數，**永不進版控、不寫檔、不記 log**。`.env` 已 gitignored。
- 離線路徑不需要 key：`make.py --backend mock`、`tts.py --backend mock`、`critic.py --dry-run`、
  `doctor.py`。批次計費前依 [`CLAUDE.md`](CLAUDE.md) 報用量徵同意。

## 在用 / 不在用

- **在用：** `video/`（影片產線）、`handout/`（HTML 講義 + `_render/shot.mjs`）、
  `authoring/seed_converge/`（圖稽核 R&D，當前 `experiment/seed-converge` 分支）。
- **凍結（不在 doctor 檢查範圍）：** `legacy/tex_handout/tools/`（第一代 LaTeX 講義 linter）、
  `legacy/` 其餘第一代產物。要跑它們才另需完整 TeX，平時不需要。

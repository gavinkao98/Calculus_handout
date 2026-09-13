# tools/setup.ps1 — 一鍵備妥本機環境（Python 端自動裝，系統端交給 doctor 報缺）。
#
# 用法（在 repo 任何位置）：
#     powershell -ExecutionPolicy Bypass -File tools\setup.ps1
#
# 做什麼：
#   1) 沒有 repo 根 .venv 就用全域 python 建一個
#   2) 從 requirements.lock 裝鎖定版本的 Python 依賴（精確可重現）
#   3) 把 repo 內 vendored 的 Instrument Sans（影片文字字型）註冊給本機 MiKTeX（使用者層級）
#   4) 跑 tools/doctor.py，把系統層缺漏（ffmpeg／LaTeX／Node／Chrome）連同補法印出來
#
# 不碰計費 API、不裝系統軟體（系統層由 doctor 給 winget 指令，由你決定何時裝）。
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$py   = Join-Path $repo ".venv\Scripts\python.exe"
$lock = Join-Path $repo "requirements.lock"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[setup] 找不到全域 python。先裝 Python 3.12：winget install Python.Python.3.12" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $py)) {
    Write-Host "[setup] 建立 .venv ..." -ForegroundColor Cyan
    python -m venv (Join-Path $repo ".venv")
}

Write-Host "[setup] 升級 pip 並安裝 requirements.lock ..." -ForegroundColor Cyan
& $py -m pip install --upgrade pip | Out-Null
& $py -m pip install -r $lock

# 部署 codex shim（codex 還不在 PATH 且 npm 目錄存在時）——解非互動 shell 找不到 codex／stale-launcher 兩坑
$npmDir = Join-Path $env:APPDATA "npm"
if (-not (Get-Command codex -ErrorAction SilentlyContinue) -and (Test-Path $npmDir)) {
    Copy-Item (Join-Path $repo "tools\codex.cmd") (Join-Path $npmDir "codex.cmd") -Force
    Write-Host "[setup] 已部署 codex shim → $npmDir\codex.cmd" -ForegroundColor Cyan
}

# 部署 agy（Antigravity CLI）shim（agy 已裝、還不在 PATH、npm 目錄存在時）——多模型唯讀評審用；見 ENVIRONMENT.md ⑤c
$agyExe = Join-Path $env:LOCALAPPDATA "agy\bin\agy.exe"
if ((Test-Path $agyExe) -and -not (Get-Command agy -ErrorAction SilentlyContinue) -and (Test-Path $npmDir)) {
    Copy-Item (Join-Path $repo "tools\agy.cmd") (Join-Path $npmDir "agy.cmd") -Force
    Write-Host "[setup] 已部署 agy shim → $npmDir\agy.cmd" -ForegroundColor Cyan
}

# 影片文字字型 Instrument Sans：vendored 在 repo，但 dvisvgm 只讀它預設找到的第一個 map 檔，
# 沒有環境變數能加 map（實測 2026-09-13），所以要兩步 MiKTeX 使用者層級設定。冪等，可重複跑。
# 換機／搬 repo 後重跑本腳本即可對齊；驗收＝doctor.py 的 fonts 區三項全綠。見 ENVIRONMENT.md ①b。
$isTexmf = Join-Path $repo "video\pipeline\fonts\instrument-sans\texmf"
if ((Test-Path $isTexmf) -and (Get-Command initexmf -ErrorAction SilentlyContinue)) {
    Write-Host "[setup] 註冊 vendored Instrument Sans 給 MiKTeX ..." -ForegroundColor Cyan
    & initexmf "--register-root=$isTexmf"
    & miktex fontmaps configure
    Write-Host "[setup] 已註冊 $isTexmf 並重建字型 map" -ForegroundColor Cyan
} elseif (-not (Test-Path $isTexmf)) {
    Write-Host "[setup] 找不到 $isTexmf（vendored 字型應隨 git 而來；git status 檢查）" -ForegroundColor Yellow
} else {
    Write-Host "[setup] initexmf 不在 PATH，略過 Instrument Sans 註冊（先裝 MiKTeX）" -ForegroundColor Yellow
}

Write-Host "`n[setup] Python 端就緒。跑環境健檢：`n" -ForegroundColor Green
& $py (Join-Path $repo "tools\doctor.py")
Write-Host "`n[setup] 系統層（ffmpeg／LaTeX／Node／Chrome）若上面有 [FAIL]，照印出的 winget 指令裝完即可。" -ForegroundColor Yellow

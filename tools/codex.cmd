@echo off
rem === codex launcher shim (version-controlled canonical copy) ===========
rem Used by the Mode B handout review + video gate2 review loops.
rem
rem WHY THIS EXISTS — two cross-machine traps it solves at once:
rem   1) PATH: the agent's tools run in a NON-INTERACTIVE shell that only sees
rem      the persistent (registry) User/Machine PATH, not your interactive
rem      profile. Codex's real binaries live under an AppData dir that is often
rem      NOT on the persistent PATH, so bare `codex` "isn't found".
rem   2) STALE LAUNCHER: the stable-named top-level
rem        %LOCALAPPDATA%\OpenAI\Codex\bin\codex.exe
rem      can be an OLDER build that rejects newer config keys (e.g.
rem      service_tier=priority). The real, current binary lives at
rem        %LOCALAPPDATA%\OpenAI\Codex\bin\<hash>\codex.exe
rem      where <hash> changes on every self-update (and differs per machine).
rem
rem DEPLOY (one-time per machine): copy this file into a dir that is ALREADY on
rem your persistent User PATH -- the npm global dir works and needs no PATH edit:
rem   copy tools\codex.cmd "%APPDATA%\npm\codex.cmd"
rem (tools\setup.ps1 does this automatically when codex isn't already resolvable.)
rem Never hardcode the <hash> path -- it is per-version and per-machine; this
rem shim resolves the NEWEST build at call time instead.
rem =======================================================================
set "CODEX_EXE="
for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "(Get-ChildItem (Join-Path $env:LOCALAPPDATA 'OpenAI\Codex\bin') -Recurse -Filter codex.exe -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName"`) do set "CODEX_EXE=%%i"
if not defined CODEX_EXE (
  >&2 echo [codex.cmd] could not locate codex.exe under "%LOCALAPPDATA%\OpenAI\Codex\bin" -- is Codex CLI installed?
  exit /b 1
)
"%CODEX_EXE%" %*

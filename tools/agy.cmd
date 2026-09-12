@echo off
rem === agy (Antigravity CLI) launcher shim (version-controlled canonical copy) ===
rem Used for read-only multi-model review calls (e.g. the REWATCH multi-lens film
rem review, video/content_scripts/_audit/REWATCH-REVIEW-RUBRIC.md) -- the same role
rem tools\codex.cmd plays for Codex. Rules for calling it: root CLAUDE.md, "付費 API".
rem
rem WHY: the Antigravity CLI installs to %LOCALAPPDATA%\agy\bin\agy.exe. The installer
rem usually adds that dir to the USER PATH (verified on this machine 2026-09-12), but a
rem fresh machine / a different install route may not, and the agent's NON-INTERACTIVE
rem shell only sees the persistent PATH. Only when a bare `agy` is not found: deploy this
rem shim into a dir already on the persistent User PATH (the npm global dir works) --
rem tools\setup.ps1 does this automatically. Never run `agy install` for this (it edits
rem your shell settings). The binary self-updates in place; do not pin a version.
rem   copy tools\agy.cmd "%APPDATA%\npm\agy.cmd"
rem ================================================================================
set "AGY_EXE=%LOCALAPPDATA%\agy\bin\agy.exe"
if not exist "%AGY_EXE%" (
  >&2 echo [agy.cmd] %AGY_EXE% not found -- install the Antigravity CLI first (Antigravity IDE -> CLI)
  exit /b 1
)
"%AGY_EXE%" %*

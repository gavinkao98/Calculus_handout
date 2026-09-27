#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/claude_plugin_settings.py — 把「所有 Claude Code plugin 都自動更新」的設定，
冪等地合併進 %USERPROFILE%\\.claude\\settings.json（換機／重跑都安全，只動這幾個 key，
其餘既有設定原樣保留）。

背景見 ENVIRONMENT.md ④：官方文件（code.claude.com/docs/en/plugins/loading，2026-09-27）
- 每個 marketplace 的 autoUpdate 由 settings 檔裡 extraKnownMarketplaces 該筆的 autoUpdate 決定；
  官方 marketplace 預設開，第三方（如 remotion）預設關，故要逐筆明寫 true。
- DISABLE_AUTOUPDATER=1／DISABLE_UPDATES=1 會關掉整個 plugin 自動更新流程，除非
  FORCE_AUTOUPDATE_PLUGINS=1；Claude 桌面 App 會對它啟動的 session 注入 DISABLE_AUTOUPDATER=1
  （不是寫在 user/machine 環境變數裡，doctor 探測不到），所以要靠這個環境變數蓋過去。
- CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1 讓 plugin clone（install／marketplace update／背景自動更新）
  一律走 HTTPS，取代舊的 GIT_CONFIG_* 一次性 SSH→HTTPS hack。

用法：
    python tools/claude_plugin_settings.py                  # 對 %USERPROFILE%\\.claude\\settings.json 動手
    python tools/claude_plugin_settings.py <path/to/settings.json>   # 對指定檔案動手（測試用）

只裝這幾個 key、不覆寫其他任何既有內容；檔案或其父目錄不存在就建立。
印出實際改了什麼，或「已是最新設定」。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_REQUIRED_ENV = {
    "FORCE_AUTOUPDATE_PLUGINS": "1",
    "CLAUDE_CODE_PLUGIN_PREFER_HTTPS": "1",
}

_REQUIRED_MARKETPLACES = {
    "remotion": {"source": "github", "repo": "remotion-dev/claude-code-plugin"},
    "claude-plugins-official": {"source": "github", "repo": "anthropics/claude-plugins-official"},
}


def merge_settings(path: Path) -> list[str]:
    """就地合併 path 指向的 settings.json，回傳這次實際改動的說明列表（空＝沒改）。"""
    changes: list[str] = []

    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = {}

    env = data.setdefault("env", {})
    for key, value in _REQUIRED_ENV.items():
        if env.get(key) != value:
            env[key] = value
            changes.append(f"env.{key} = \"{value}\"")

    marketplaces = data.setdefault("extraKnownMarketplaces", {})

    # 補齊必要的兩個 marketplace（若使用者尚未裝過 remotion／official 也先寫好 autoUpdate:true）
    for name, source in _REQUIRED_MARKETPLACES.items():
        if name not in marketplaces:
            marketplaces[name] = {"source": source, "autoUpdate": True}
            changes.append(f"extraKnownMarketplaces.{name}（新增，autoUpdate=true）")

    # 對「既有」的每一筆都強制 autoUpdate=true，涵蓋未來新增的任何 marketplace
    for name, entry in marketplaces.items():
        if not isinstance(entry, dict):
            continue
        if entry.get("autoUpdate") is not True:
            entry["autoUpdate"] = True
            changes.append(f"extraKnownMarketplaces.{name}.autoUpdate = true")

    if changes:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return changes


def main() -> int:
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        path = Path.home() / ".claude" / "settings.json"

    changes = merge_settings(path)
    if changes:
        print(f"[claude_plugin_settings] 已更新 {path}：")
        for c in changes:
            print(f"  - {c}")
    else:
        print(f"[claude_plugin_settings] {path} 已是最新設定")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

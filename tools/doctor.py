#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/doctor.py — 全 repo 環境健檢（單檔、純 stdlib，任何 python 都能跑）。

一行看出「這台機器缺什麼、怎麼補」，讓 agent／作者換機後不必每次重新踩環境坑。
這支腳本本身不裝任何東西、不連網、不碰計費 API；只檢查並印出補法。

    python tools/doctor.py            # 全部檢查
    python tools/doctor.py --json     # 機器可讀（給 agent 解析）

退出碼：所有「必要」項通過＝0；有任何 [FAIL]＝1（[WARN]／[INFO] 不影響）。
    python tools/doctor.py --smoke    # 加跑 Remotion 分鏡的 deck 級閘：video/pipeline/check_storyboard.py 對
                                      # remotion/*/*.yml 全跑（結構＋內容層檢查器；不 render、不計費）
Manim 版的 --smoke（正典 deck 的 schema／lint／derive --check）於 2026-09-28 隨引擎封存退役；同日重掛為上述
Remotion 版（契約＝video/SPEC-remotion-storyboard-schema.md）。

權威說明見 repo 根的 ENVIRONMENT.md；本檔是它的可執行版。
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:  # 避免 Windows 主控台 cp950 把繁中／狀態符印成亂碼
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO = Path(__file__).resolve().parents[1]
IS_WIN = os.name == "nt"
VENV_PY = REPO / ".venv" / ("Scripts/python.exe" if IS_WIN else "bin/python")

PASS, WARN, FAIL, INFO = "PASS", "WARN", "FAIL", "INFO"
_SYMBOL = {PASS: "[ OK ]", WARN: "[WARN]", FAIL: "[FAIL]", INFO: "[info]"}

# (status, area, label, detail) — detail 對 FAIL/WARN 放「怎麼補」
_results: list[tuple[str, str, str, str]] = []


def record(status: str, area: str, label: str, detail: str = "") -> None:
    _results.append((status, area, label, detail))


def _run(cmd: list[str], timeout: int = 30) -> tuple[int, str]:
    try:
        r = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return r.returncode, ((r.stdout or "") + (r.stderr or "")).strip()
    except FileNotFoundError:
        return 127, "not found"
    except Exception as exc:  # noqa: BLE001 — doctor never crashes on a probe
        return 1, str(exc)


# ── ① Python 直譯器 + 共用 .venv + 套件 ───────────────────────────────

# 套件 → (import 名, 嚴重度, 用途)。critical 缺＝FAIL，optional 缺＝WARN。
_VENV_MODS = [
    ("PyYAML", "yaml", "critical", "讀 storyboard／fragment 設定（整條產線靠它）"),
    ("pillow", "PIL", "critical", "幀處理／稽核報告 base64 內嵌圖"),
    ("imageio-ffmpeg", "imageio_ffmpeg", "optional", "內附 ffmpeg 二進位（裝了系統 ffmpeg 後非必要）"),
    ("fonttools", "fontTools", "optional", "LaTeX 字形閘讀原始字型輪廓（handout/latex/check_glyphs.py）；產 logo 外框 SVG"),
    ("pymupdf", "fitz", "optional", "LaTeX 字形閘讀 PDF 嵌入字型（handout/latex/check_glyphs.py）；authoring 圖稽核轉點陣"),
    ("Brotli", "brotli", "optional", "LaTeX 字形閘讀圖裡 web 字型的 woff2 基準（fontTools 解 woff2 需要；template/fonts/webcm/）"),
]


def check_python_and_venv() -> None:
    pv = "%d.%d.%d" % sys.version_info[:3]
    py_ok = sys.version_info[:2] >= (3, 10)
    record(PASS if py_ok else WARN, "Python", f"執行 doctor 的 python {pv}",
           f"{sys.executable}" + ("" if py_ok else "  ←建議 3.10+（lock 以 3.12 凍結）"))

    if not VENV_PY.exists():
        record(FAIL, "Python", "repo 根 .venv 不存在",
               "跑 tools/setup.ps1；或手動：python -m venv .venv && "
               r".venv\Scripts\python -m pip install -r requirements.lock")
        return

    rc, out = _run([str(VENV_PY), "--version"])
    record(PASS if rc == 0 else FAIL, "Python", ".venv 直譯器", out or "無法執行 .venv python")

    probe = (
        "import importlib,json\n"
        "def v(m):\n"
        "    try:\n"
        "        return getattr(importlib.import_module(m),'__version__','?')\n"
        "    except Exception:\n"
        "        return None\n"
        "mods=%r\n"
        "print(json.dumps({m:v(m) for _,m,_,_ in mods}))\n" % (_VENV_MODS,)
    )
    rc, out = _run([str(VENV_PY), "-c", probe])
    versions: dict[str, str | None] = {}
    if rc == 0 and out:
        try:
            versions = json.loads(out.splitlines()[-1])
        except Exception:
            pass
    for pkg, mod, sev, use in _VENV_MODS:
        ver = versions.get(mod)
        if ver:
            record(PASS, "Python", f"{pkg} ({ver})", use)
        elif sev == "critical":
            record(FAIL, "Python", f"{pkg} 缺", f"{use}；補：.venv\\Scripts\\python -m pip install -r requirements.lock")
        else:
            record(WARN, "Python", f"{pkg} 缺（選用）", f"{use}；需要時：.venv\\Scripts\\python -m pip install {pkg}")


# ── ② 系統 binary：ffmpeg / ffprobe（成片後處理 + 抽幀稽核）──────────────

def check_ffmpeg() -> None:
    remedy = "winget install --id Gyan.FFmpeg -e  （裝完開新 shell 讓 PATH 生效）"
    for name in ("ffmpeg", "ffprobe"):
        path = shutil.which(name)
        if path:
            rc, out = _run([name, "-version"])
            ver = out.splitlines()[0] if out else ""
            record(PASS, "ffmpeg", f"{name} 在 PATH", ver or path)
        else:
            why = "Remotion 成片的 loudnorm／章節嵌入、rewatch_pack 抽幀、音訊量測都用裸名呼叫它" \
                if name == "ffmpeg" else "rewatch_pack 讀逐場時長／幀率用裸名呼叫它"
            record(FAIL, "ffmpeg", f"{name} 不在 PATH", f"{why}。補：{remedy}")


# ── ③ LaTeX（MiKTeX 本體；講義線 handout/latex/ 專用，影片線自 2026-09-28 起不需 TeX）──

def check_latex() -> None:
    """MiKTeX 在不在（以 `latex` 在 PATH 為探針）。講義出版線（handout/latex/）的 lualatex／latexmk／
    NCM／pdftotext 由 check_handout_latex 細驗。影片線改走 Remotion（數學由 MathJax 出 SVG）後不再需要
    TeX；原本為 Manim Tex→SVG 驗的 dvisvgm／dvipng 與影片字型套件檢查已隨 gen-2 引擎退役
    （見 video/KICKOFF-remotion-unification.md）。"""
    remedy = "裝 MiKTeX（https://miktex.org），latex／lualatex／latexmk 會進 PATH；首次編譯會自動補缺的套件"
    path = shutil.which("latex")
    if path:
        record(PASS, "LaTeX", "latex 在 PATH（MiKTeX 已裝）", path)
    else:
        record(FAIL, "LaTeX", "latex 不在 PATH（MiKTeX 未裝）",
               f"講義出版線（handout/latex/）排不出 PDF。補：{remedy}")


# ── ④ Node ≥21（Remotion 影片線正式依賴＋handout 圖 shot.mjs）＋ Chrome（shot.mjs）──

# Remotion 專案（2026-09-28 起影片線唯一渲染器；同日自 experiments/remotion_styles/paper/ 升格為 video/remotion/）
_REMOTION_DIR = ("video", "remotion")


def check_node_and_chrome() -> None:
    node = shutil.which("node")
    if not node:
        record(FAIL, "Node", "node 不在 PATH",
               "Remotion 影片線（render／studio）與 shot.mjs（render 講義圖供 figure 稽核）都要 Node ≥21。"
               "裝：winget install OpenJS.NodeJS.LTS")
    else:
        rc, out = _run(["node", "--version"])
        m = re.search(r"v(\d+)", out or "")
        major = int(m.group(1)) if m else 0
        if major >= 21:
            record(PASS, "Node", f"node {out.strip()}", f"{node}（Remotion 影片線正式依賴＋shot.mjs）")
        else:
            record(FAIL, "Node", f"node {out.strip()} < 21",
                   "Remotion 影片線與 shot.mjs（global WebSocket/fetch）都需 Node ≥21。"
                   "升級：winget install OpenJS.NodeJS.LTS")

    # Remotion 的 npm 依賴（node_modules 不進版控；版本由 video/remotion/package-lock.json 釘死，npm ci 精確重現）
    rdir = REPO.joinpath(*_REMOTION_DIR)
    if (rdir / "node_modules").is_dir():
        record(PASS, "Node", "Remotion node_modules 已裝", str(rdir / "node_modules"))
    else:
        record(WARN, "Node", "Remotion node_modules 不存在（影片 render 前要裝）",
               f"在 {rdir} 跑 `npm ci`（依 package-lock.json 精確重現，需網路）")

    # Chrome：shot.mjs 先讀 CHROME env，再退回常見安裝位置
    candidates = []
    if os.environ.get("CHROME"):
        candidates.append(os.environ["CHROME"])
    candidates += [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    found = next((c for c in candidates if c and Path(c).exists()), None)
    if found:
        record(PASS, "handout", "Google Chrome", found)
    else:
        record(FAIL, "handout", "找不到 Google Chrome",
               "shot.mjs 用 CDP 截圖。裝 Chrome：winget install Google.Chrome；"
               "或設 CHROME 環境變數指向 chrome.exe")


# ── ⑤ codex CLI（Mode B 講義審核 + video gate2 審核；選用）─────────────

def check_codex() -> None:
    """codex 走非互動 shell 常因「裝了但不在持久 PATH」找不到；shim 一併解決
    PATH 與 stale-launcher 兩坑。缺它不擋核心產線，故 WARN 不 FAIL。"""
    bin_dir = Path(os.path.expandvars(r"%LOCALAPPDATA%\OpenAI\Codex\bin"))
    native = list(bin_dir.rglob("codex.exe")) if bin_dir.exists() else []
    newest = max(native, key=lambda p: p.stat().st_mtime) if native else None
    ver = ""
    if newest:  # 直接問最新的原生 binary 版本，避開 .cmd 執行細節
        rc, out = _run([str(newest), "--version"])
        ver = out.splitlines()[0] if (rc == 0 and out) else ""
    onpath = shutil.which("codex")
    if onpath:
        record(PASS, "codex", "codex 在 PATH（審核可用）", f"{ver or '?'}  ←{onpath}")
    elif native:
        record(WARN, "codex", f"codex 已裝（{ver or '?'}）但不在 PATH",
               r'非互動 shell 找不到。部署 shim：copy tools\codex.cmd "%APPDATA%\npm\codex.cmd"'
               r'（npm 目錄已在持久 PATH；或跑 tools\setup.ps1 自動部署）')
    else:
        record(WARN, "codex", "codex 未安裝（選用，跑審核才需要）",
               r"裝 Codex CLI（自更新到 %LOCALAPPDATA%\OpenAI\Codex\bin）後，"
               r"把 tools\codex.cmd 複製進任一已在持久 PATH 的目錄（如 %APPDATA%\npm）")


# ── ⑤c agy（Antigravity CLI；多模型唯讀評審；選用）─────────────────────────

def check_agy() -> None:
    """agy 本體固定在 %LOCALAPPDATA%\\agy\\bin\\agy.exe、不進 PATH（`agy install` 會改 shell 設定，
    不用）；shim tools/agy.cmd 比照 codex。缺它不擋核心產線（只影響多鏡評審拉模型家族），WARN 不 FAIL。"""
    exe = Path(os.path.expandvars(r"%LOCALAPPDATA%\agy\bin\agy.exe"))
    ver = ""
    if exe.exists():
        rc, out = _run([str(exe), "--version"])
        ver = out.splitlines()[0].strip() if (rc == 0 and out) else ""
    onpath = shutil.which("agy")
    if onpath:
        record(PASS, "agy", "agy 在 PATH（多模型唯讀評審可用）", f"{ver or '?'}  ←{onpath}")
    elif exe.exists():
        record(WARN, "agy", f"agy 已裝（{ver or '?'}）但不在 PATH",
               r'部署 shim：copy tools\agy.cmd "%APPDATA%\npm\agy.cmd"（或跑 tools\setup.ps1）')
    else:
        record(WARN, "agy", "agy 未安裝（選用，多模型唯讀評審才需要）",
               r"由 Antigravity IDE 安裝 CLI（落在 %LOCALAPPDATA%\agy\bin），再部署 tools\agy.cmd；見 ENVIRONMENT.md ⑤c")


# ── ⑤d Remotion Agent Skills plugin（claude CLI user-scope plugin；選用）───────

def check_remotion_plugin() -> None:
    """Remotion Agent Skills 已從 project-copy（.claude/skills/remotion-*＋skills-lock.json）
    改成 claude CLI 的 user-scope plugin（2026-09-27 拍板，見 ENVIRONMENT.md ④），tools/setup.ps1
    會在缺的時候自動裝。缺它不擋核心產線（只影響 Remotion 影片製作的 skill 觸發），WARN 不 FAIL。"""
    claude = shutil.which("claude")
    if not claude:
        record(WARN, "remotion-skills", "claude CLI 未安裝，略過 Remotion plugin 檢查",
               "選用；裝 Claude Code 後跑 tools/setup.ps1 會自動裝 plugin")
        return
    rc, out = _run([claude, "plugin", "list"], timeout=30)
    if rc == 0 and "remotion@remotion" in out:
        record(PASS, "remotion-skills", "remotion@remotion plugin 已裝（user scope）", "")
    else:
        record(WARN, "remotion-skills", "remotion@remotion plugin 未裝",
               "跑 tools/setup.ps1（會自動裝），或手動："
               "claude plugin marketplace add remotion-dev/claude-code-plugin && "
               "claude plugin install remotion@remotion --scope user")


def check_plugin_autoupdate_settings() -> None:
    """所有 Claude Code plugin 都應自動更新（2026-09-27 使用者裁決，見 ENVIRONMENT.md ④）：
    ~/.claude/settings.json 要有 FORCE_AUTOUPDATE_PLUGINS／CLAUDE_CODE_PLUGIN_PREFER_HTTPS 兩個
    env，且每個 extraKnownMarketplaces 都要 autoUpdate:true。缺件不擋核心產線，故 WARN 不 FAIL。"""
    path = Path.home() / ".claude" / "settings.json"
    if not path.exists():
        record(WARN, "plugin-autoupdate", "~/.claude/settings.json 不存在，略過 plugin 自動更新設定檢查",
               "跑 tools/setup.ps1 會建立並補齊")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        record(WARN, "plugin-autoupdate", f"~/.claude/settings.json 讀不出來：{exc}", "跑 tools/setup.ps1")
        return

    env = data.get("env", {}) or {}
    missing = [k for k in ("FORCE_AUTOUPDATE_PLUGINS", "CLAUDE_CODE_PLUGIN_PREFER_HTTPS") if env.get(k) != "1"]
    marketplaces = data.get("extraKnownMarketplaces", {}) or {}
    stale = [name for name, entry in marketplaces.items()
             if isinstance(entry, dict) and entry.get("autoUpdate") is not True]

    if not missing and not stale:
        record(PASS, "plugin-autoupdate", "plugin 自動更新設定齊全（env＋所有 marketplace）", "")
    else:
        parts = []
        if missing:
            parts.append("缺 env：" + "、".join(missing))
        if stale:
            parts.append("autoUpdate 非 true 的 marketplace：" + "、".join(stale))
        record(WARN, "plugin-autoupdate", "plugin 自動更新設定不齊全（" + "；".join(parts) + "）",
               "跑 tools/setup.ps1（會冪等補齊 ~/.claude/settings.json）")


# ── ⑤b Vale prose linter（去 AI 味 lint 引擎；PLAN-deai-flavor；選用、flag-only）──

def check_vale() -> None:
    """Vale = 去 AI 味散文 lint 引擎（markup-aware，自動排除 $...$／LaTeX／code）。
    flag-only／advisory，決定性「擋不擋」交給 Mode B 人審維度 C，不在此——故缺它不擋
    核心產線，WARN 不 FAIL（同 codex）。裝法見 ENVIRONMENT.md「Vale」段。"""
    exe = shutil.which("vale")
    if not exe:
        record(WARN, "vale", "Vale 未安裝（選用，跑去 AI 味 lint 才需要）",
               "winget install errata-ai.Vale（備援 scoop install vale）；見 ENVIRONMENT.md「Vale」段")
        return
    rc, out = _run([exe, "--version"])
    ver = out.splitlines()[0].strip() if (rc == 0 and out) else ""
    if ver:
        record(PASS, "vale", f"Vale 在 PATH（{ver}）", exe)
    else:
        record(WARN, "vale", "Vale 在 PATH 但無法取得版本", f"執行回報：{out or '?'}（{exe}）")


# ── ⑥ 內附資產（進版控，理應永遠在）────────────────────────────────────

def check_forced_alignment() -> None:
    """Word-level alignment tools for the PRODUCTION scene-level FA path
    (video/pipeline/scene_align.py): stable-ts is the timing source, whisper_timestamped
    the ASR QA probe. Needed to produce narrated masters; mock iteration does not need
    them (so still WARN, not FAIL). Not an experiment -- experiments/forced_alignment_dean/
    is only the historical origin."""
    # QA probe: free ASR (can drop words on repeated math phrases; not a timing source).
    exe = shutil.which("whisper_timestamped")
    if not exe:
        record(
            WARN,
            "forced-alignment",
            "whisper_timestamped not on PATH",
            "Needed for narrated masters (production scene-level FA QA probe, "
            "pipeline/scene_align.py); install with "
            "python -m pip install --upgrade whisper-timestamped",
        )
    else:
        rc, out = _run([exe, "--versions"])
        ver = out.splitlines()[0].strip() if (rc == 0 and out) else ""
        if ver:
            record(PASS, "forced-alignment", f"whisper_timestamped ({ver})", exe)
        else:
            record(WARN, "forced-alignment", "whisper_timestamped on PATH but version probe failed",
                   f"{out or '?'} ({exe})")
    # Timing source: transcript-constrained aligner (cannot drop words; upstream
    # archived 2026-05-30, pinned version -- see ENVIRONMENT.md (5)c).
    rc, out = _run(
        [sys.executable, "-c", "import stable_whisper; print(stable_whisper.__version__)"],
        timeout=60,
    )
    ver = ""
    if rc == 0 and out:
        for line in out.splitlines():
            if re.match(r"^\d+\.\d+", line.strip()):
                ver = line.strip()
                break
    if ver:
        record(PASS, "forced-alignment", f"stable-ts ({ver})",
               "video/experiments/forced_alignment_dean/run_stable_ts_align.py")
    else:
        record(WARN, "forced-alignment", "stable-ts (stable_whisper) not importable",
               "Optional; transcript-constrained timing source for scene-level TTS; "
               "install with python -m pip install --upgrade stable-ts")


def check_chinese_alignment_model() -> None:
    """Local checksum only: never let Whisper auto-download during doctor."""
    path = Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache"))) / "whisper/small.pt"
    expected = "9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794"
    if not path.is_file():
        record(WARN, "forced-alignment", "中文 Whisper small 權重未快取",
               f"Q7 中文試片離線對齊需要 {path}（483617219 bytes）；安裝方式見 ENVIRONMENT.md §⑤c")
        return
    try:
        hasher = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                hasher.update(chunk)
        digest = hasher.hexdigest()
        valid = path.stat().st_size == 483617219 and digest == expected
        record(PASS if valid else WARN, "forced-alignment", "中文 Whisper small 本機權重完整性",
               f"{path}；SHA256={digest}" + ("；可供離線載入" if valid else "；大小或 checksum 不符，不可使用"))
    except OSError as exc:
        record(WARN, "forced-alignment", "中文 Whisper small 權重無法讀取", str(exc))


def check_assets() -> None:
    # The vendored brand asset is the outlined NTU lockup SVG -- the source of the copy the
    # Remotion project serves from video/remotion/public/brand/ for every intro/outro.
    lockup = REPO / "video" / "pipeline" / "assets" / "lockup-color-outlined.svg"
    if lockup.exists():
        record(PASS, "assets", "logo lockup SVG", str(lockup))
    else:
        record(WARN, "assets", "logo lockup SVG 缺",
               f"預期在 {lockup}（intro/outro render 要它；應隨 git 而來，git status 檢查是否誤刪）")


# ── ⑥b／⑥b2／⑥d 影片字型與 Tex 實編檢查：2026-09-28 隨 Manim gen-2 引擎退役 ──────────
# 原本驗 Route A 的 LaTeX 字型套件（plex-mono／lmodern／microtype）、vendored Instrument Sans 的
# MiKTeX 註冊（ps2pk.map），並實 build 一個 Tex。影片線改走 Remotion 後這些都不再需要；字型檔隨
# video/pipeline/fonts/ 進 legacy/manim_video/。回退見 video/KICKOFF-remotion-unification.md 的 tag。


# ── ⑥c handout LaTeX 排版線（pilot v2：lualatex＋latexmk＋NCM＋vendored Inter）──

def check_handout_latex() -> None:
    """講義出版排版線（handout/latex/，KICKOFF-latex-pilot.md）：模板走 lualatex＋
    memoir＋NewComputerModern，UI sans＝repo 內 vendored Inter（fontspec Path= 載入，
    換機零安裝——git 帶著走，這裡只驗檔案在）；完整性閘 check_prose.py 需 pdftotext。"""
    for name, why in (
        ("lualatex", "模板引擎（D4 拍板；MiKTeX 內建）"),
        ("latexmk", "建置驅動（MiKTeX 內建）"),
        ("pdftotext", "check_prose.py 散文子序列閘（poppler）"),
    ):
        path = shutil.which(name)
        if path:
            record(PASS, "handout-tex", f"{name} 在 PATH", path)
        else:
            record(FAIL, "handout-tex", f"{name} 不在 PATH", f"{why}。裝 MiKTeX／poppler 後開新 shell")
    # pdftotext 有兩種實作，只驗「在 PATH」不夠：poppler 版才正確處理 `-enc UTF-8`；
    # Git for Windows 內附的是 Xpdf 4.00（Glyph & Cog），同旗標吐出非 UTF-8 位元組，
    # check_prose.py 會崩在 `normalize(out.stdout)` 的 `NoneType.replace`——錯誤訊息完全
    # 看不出病因。Windows 上 Git 的 mingw64 常排在 MiKTeX 之前，於是「裝好了卻跑不動」。
    # 註：poppler 自己的橫幅也含 "Glyph & Cog"，故正面比對 "poppler"、不可反向排除。
    if shutil.which("pdftotext"):
        _, ver = _run(["pdftotext", "-v"])
        first = ver.splitlines()[0] if ver else ""
        if "poppler" in ver.lower():
            record(PASS, "handout-tex", "pdftotext 是 poppler 版", first)
        else:
            record(FAIL, "handout-tex", f"pdftotext 不是 poppler 版（{first or '版本不明'}）",
                   "完整性閘會崩。把 MiKTeX 的 bin 排到 Git 的 mingw64 之前"
                   "（如 C:\\Program Files\\MiKTeX\\miktex\\bin\\x64），或改裝 poppler")
    if shutil.which("kpsewhich"):
        rc, out = _run(["kpsewhich", "NewCM10-Regular.otf"])
        if rc == 0 and out:
            record(PASS, "handout-tex", "NewComputerModern otf 可尋", out.splitlines()[-1])
        else:
            record(FAIL, "handout-tex", "找不到 NewCM10-Regular.otf",
                   "MiKTeX 首次編譯通常自動補裝 newcomputermodern；或 `mpm --install newcomputermodern`")
    else:
        record(WARN, "handout-tex", "kpsewhich 不在 PATH，略過 NCM 檢查", "裝 MiKTeX 後會進 PATH")
    inter_dir = REPO / "handout" / "latex" / "template" / "fonts" / "inter"
    missing = [f"Inter-{w}.otf" for w in ("Regular", "Italic", "Medium", "SemiBold", "Bold", "BoldItalic")
               if not (inter_dir / f"Inter-{w}.otf").exists()]
    if not missing:
        record(PASS, "handout-tex", "vendored Inter 六字重齊備", str(inter_dir.relative_to(REPO)))
    else:
        record(FAIL, "handout-tex", f"vendored Inter 缺 {len(missing)} 檔（{', '.join(missing)}）",
               "字體檔應隨 repo（git pull／checkout 即得）；來源＝rsms/inter release v4.1 的 extras/otf")


# ── ⑦ API 金鑰（per-machine 祕鑰；未設不算錯，只是提示）────────────────

_KEYS = [
    ("MIMO_API_KEY", "video MiMo TTS／視覺 critic（公測免費，仍屬計費 API，依 CLAUDE.md 徵同意）"),
    ("GEMINI_API_KEY", "authoring figure 稽核（計費）"),
    ("OPENAI_API_KEY", "authoring seed-converge 迴圈（計費）"),
    ("DEEPSEEK_API_KEY", "authoring seed-converge 迴圈（計費）"),
]


def check_keys() -> None:
    for key, use in _KEYS:
        if os.environ.get(key):
            record(INFO, "keys", f"{key} 已設", use)
        else:
            record(INFO, "keys", f"{key} 未設", f"需要時才設（離線路徑不需要）：{use}")


# ── ⑧ --smoke：Remotion 分鏡的 deck 級閘（2026-09-28 重掛；不 render、不計費）──────

def check_video_smoke() -> None:
    """對每支現役 Remotion 分鏡（remotion/<片>/<片>.yml）跑
    video/pipeline/check_storyboard.py：結構驗證＋provenance／source_rev／pedagogy／coverage／
    example_coverage（契約＝video/SPEC-remotion-storyboard-schema.md）。exit 0＝PASS（附 WARN 數，
    warn-only 不擋）、exit 1（error）／2（讀不到）＝FAIL。Manim 版 smoke（schema／lint／derive --check）
    的對象已封存，不再回來。為何要有：doctor 只驗工具鏈，「工具鏈綠」與「分鏡在閘中止」曾同時成立
    （產線評估 2026-09-07 F1／F4）。模組 selftest 全套另跑 python video/pipeline/run_selftests.py。"""
    if not VENV_PY.exists():
        record(INFO, "video-smoke", "略過：無 .venv", "先跑 tools/setup.ps1 建環境再 --smoke")
        return
    rdir = REPO.joinpath(*_REMOTION_DIR)
    decks = sorted(p for p in rdir.glob("*/*.yml") if p.parent.name not in ("node_modules", "public", "out", "scripts"))
    if not decks:
        record(WARN, "video-smoke", "找不到 Remotion 分鏡", str(rdir / "*" / "*.yml"))
        return
    entry = REPO / "video" / "pipeline" / "check_storyboard.py"
    for deck in decks:
        rc, out = _run([str(VENV_PY), str(entry), str(deck)], timeout=120)
        lines = [ln for ln in out.splitlines() if ln.strip()]
        label = f"check_storyboard {deck.parent.name}/{deck.name}"
        if rc == 0:
            warns = sum(1 for ln in lines if ln.startswith("  WARN"))
            record(PASS, "video-smoke", label, f"{warns} 個 WARN（warn-only，不擋）" if warns else "")
        else:
            record(FAIL, "video-smoke", label, " | ".join(lines[-3:]) or f"exit {rc}")


# ── 報表 ──────────────────────────────────────────────────────────────

def _has(area: str, label_sub: str, status: str) -> bool:
    return any(s == status and a == area and label_sub in lbl for s, a, lbl, _ in _results)


def _missing(area: str, label_sub: str) -> bool:
    """True 若該項目前是 FAIL（缺）。"""
    return any(s == FAIL and a == area and label_sub in lbl for s, a, lbl, _ in _results)


def print_report(as_json: bool) -> int:
    fails = sum(1 for s, *_ in _results if s == FAIL)
    warns = sum(1 for s, *_ in _results if s == WARN)

    if as_json:
        payload = {
            "repo": str(REPO),
            "results": [{"status": s, "area": a, "label": l, "detail": d} for s, a, l, d in _results],
            "fails": fails, "warns": warns, "ok": fails == 0,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if fails == 0 else 1

    print(f"\n環境健檢 · {platform.system()} {platform.release()} · {REPO}\n" + "─" * 64)
    cur = None
    for s, area, label, detail in _results:
        if area != cur:
            print(f"\n{area}")
            cur = area
        line = f"  {_SYMBOL[s]} {label}"
        if detail:
            line += f"\n         {detail}"
        print(line)

    # 能力摘要：直接告訴你「現在哪些工作流跑得動」
    node_ok = not _missing("Node", "node")
    video_ok = node_ok and _has("Node", "Remotion node_modules", PASS) \
        and not any(_missing("Python", x) for x in ("PyYAML", "pillow")) \
        and not _missing("ffmpeg", "ffmpeg") and not _missing("ffmpeg", "ffprobe")
    handout_fig_ok = node_ok and not _missing("handout", "Chrome")
    print("\n能力摘要\n" + "─" * 64)
    print(f"  {'✅' if video_ok else '❌'} 影片 Remotion render＋後處理（Node≥21＋video/remotion/node_modules＋venv＋ffmpeg＋ffprobe）")
    print(f"  {'✅' if handout_fig_ok else '❌'} handout 圖 render／figure 稽核（Node≥21＋Chrome）")
    print("  ✅ handout build.py（純 stdlib，任何 python 皆可）")
    handout_tex_ok = not any(s == FAIL and a == "handout-tex" for s, a, *_ in _results)
    print(f"  {'✅' if handout_tex_ok else '❌'} handout LaTeX 排版線（lualatex＋latexmk＋NCM＋vendored Inter＋pdftotext）")
    codex_ok = any(s == PASS and a == "codex" for s, a, *_ in _results)
    print(f"  {'✅' if codex_ok else '⚠️ '} codex 審核（Mode B 講義／video gate2；缺＝不擋產線）")
    print("  ·  模組 selftest 全套另跑：python video/pipeline/run_selftests.py（不併進 doctor）")

    print("\n" + "─" * 64)
    verdict = "全部必要項通過 ✅" if fails == 0 else f"{fails} 項必要缺漏 ❌（見上方 [FAIL]）"
    print(f"  {verdict}" + (f"，另有 {warns} 項提醒" if warns else ""))
    print("  細節與一次性安裝步驟見 repo 根 ENVIRONMENT.md\n")
    return 0 if fails == 0 else 1


def main() -> int:
    as_json = "--json" in sys.argv[1:]
    smoke = "--smoke" in sys.argv[1:]
    check_python_and_venv()
    check_ffmpeg()
    check_latex()
    check_node_and_chrome()
    check_codex()
    check_agy()
    check_remotion_plugin()
    check_plugin_autoupdate_settings()
    check_vale()
    check_forced_alignment()
    check_chinese_alignment_model()
    check_assets()
    check_handout_latex()
    check_keys()
    if smoke:
        check_video_smoke()
    return print_report(as_json)


if __name__ == "__main__":
    raise SystemExit(main())

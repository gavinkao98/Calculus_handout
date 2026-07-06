#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/doctor.py — 全 repo 環境健檢（單檔、純 stdlib，任何 python 都能跑）。

一行看出「這台機器缺什麼、怎麼補」，讓 agent／作者換機後不必每次重新踩環境坑。
這支腳本本身不裝任何東西、不連網、不碰計費 API；只檢查並印出補法。

    python tools/doctor.py            # 全部檢查
    python tools/doctor.py --json     # 機器可讀（給 agent 解析）

退出碼：所有「必要」項通過＝0；有任何 [FAIL]＝1（[WARN]／[INFO] 不影響）。

權威說明見 repo 根的 ENVIRONMENT.md；本檔是它的可執行版。
"""
from __future__ import annotations

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
    ("manim", "manim", "critical", "影片場景 render"),
    ("ManimPango", "manimpango", "critical", "manim 文字排版／註冊內附字型"),
    ("pillow", "PIL", "critical", "幀處理／稽核報告 base64 內嵌圖"),
    ("imageio-ffmpeg", "imageio_ffmpeg", "optional", "內附 ffmpeg 二進位（裝了系統 ffmpeg 後非必要）"),
    ("fonttools", "fontTools", "optional", "一次性產 logo 外框 SVG（_outline_text.py）"),
    ("pymupdf", "fitz", "optional", "authoring 圖稽核 PDF 轉點陣（figure_critic.py）"),
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


# ── ② 系統 binary：ffmpeg / ffprobe（影片 compose + 視覺稽核）────────────

def check_ffmpeg() -> None:
    remedy = "winget install --id Gyan.FFmpeg -e  （裝完開新 shell 讓 PATH 生效）"
    for name in ("ffmpeg", "ffprobe"):
        path = shutil.which(name)
        if path:
            rc, out = _run([name, "-version"])
            ver = out.splitlines()[0] if out else ""
            record(PASS, "ffmpeg", f"{name} 在 PATH", ver or path)
        else:
            why = "compose 合併成片＋critic 抽幀都要它" if name == "ffmpeg" else \
                  "make.py render 後時長健檢用裸名呼叫，缺它會 compose 直接崩、無合併片"
            record(FAIL, "ffmpeg", f"{name} 不在 PATH", f"{why}。補：{remedy}")


# ── ③ LaTeX（manim 的 Tex/MathTex 一定要真 TeX 才能編譯）───────────────

def check_latex() -> None:
    remedy = "裝 MiKTeX（https://miktex.org），latex/dvisvgm 會進 PATH；首次用會自動補 newtx 套件"
    for name, sev in (("latex", "critical"), ("dvisvgm", "critical"), ("dvipng", "optional")):
        path = shutil.which(name)
        if path:
            record(PASS, "LaTeX", f"{name} 在 PATH", path)
        elif sev == "critical":
            record(FAIL, "LaTeX", f"{name} 不在 PATH", f"影片任何含數學的場景都編不出來。補：{remedy}")
        else:
            record(WARN, "LaTeX", f"{name} 不在 PATH（選用）", remedy)

    # Route A：video 文字＋數學皆走 LaTeX——_bootstrap.apply_tex_template 的 preamble \usepackage
    # plex-sans／plex-mono／lmodern／microtype。這些套件的存在由 check_fonts 以 kpsewhich 驗
    # （latex/dvisvgm 在 PATH 是先決條件）。newtx 已不再是 video 需求，但仍是 legacy/tex_handout 的需求。


# ── ④ handout HTML 圖 render：Node ≥21 + Chrome（shot.mjs）──────────────

def check_node_and_chrome() -> None:
    node = shutil.which("node")
    if not node:
        record(FAIL, "handout", "node 不在 PATH",
               "shot.mjs（render 講義圖供 figure 稽核）要 Node ≥21。裝：winget install OpenJS.NodeJS.LTS")
    else:
        rc, out = _run(["node", "--version"])
        m = re.search(r"v(\d+)", out or "")
        major = int(m.group(1)) if m else 0
        if major >= 21:
            record(PASS, "handout", f"node {out.strip()}", node)
        else:
            record(FAIL, "handout", f"node {out.strip()} < 21",
                   "shot.mjs 用 global WebSocket/fetch，需 Node ≥21。升級：winget install OpenJS.NodeJS.LTS")

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
    """Optional local word-level alignment tools for video timing experiments."""
    # QA probe: free ASR (can drop words on repeated math phrases; not a timing source).
    exe = shutil.which("whisper_timestamped")
    if not exe:
        record(
            WARN,
            "forced-alignment",
            "whisper_timestamped not on PATH",
            "Optional for video forced-alignment experiments; install with "
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


def check_assets() -> None:
    # The render-critical vendored asset is the outlined NTU lockup SVG -- brand
    # .logo_lockup_outlined() loads it for every intro/outro. (No design fonts are vendored:
    # Route A renders all text + math through LaTeX packages -- see check_fonts -- so there
    # is nothing under assets/fonts/ to expect.)
    lockup = REPO / "video" / "pipeline" / "assets" / "lockup-color-outlined.svg"
    if lockup.exists():
        record(PASS, "assets", "logo lockup SVG", str(lockup))
    else:
        record(WARN, "assets", "logo lockup SVG 缺",
               f"預期在 {lockup}（intro/outro render 要它；應隨 git 而來，git status 檢查是否誤刪）")


# ── ⑥b 影片字型：LaTeX 套件（Route A 後文字＋數學皆走 LaTeX，不再用 Pango 系統字型）──

def check_fonts() -> None:
    """Route A（2026-06-24）後，影片**所有螢幕文字＋數學都走 LaTeX/pdflatex**——文字 IBM Plex
    Sans／Mono、數學 Latin Modern，字體在 _bootstrap.apply_tex_template 的 preamble 設定，不再經
    Pango（舊的 Times New Roman／Courier New 系統字型已棄）。所以這裡驗的是這些 MiKTeX 套件存在
    （kpsewhich），缺了含文字／數學的場景會編譯失敗或 fallback。"""
    if not shutil.which("kpsewhich"):
        record(WARN, "fonts", "kpsewhich 不在 PATH，略過 LaTeX 字型套件檢查",
               "裝 MiKTeX 後 kpsewhich 會進 PATH（見 LaTeX 區）")
        return
    styles = (
        ("plex-sans.sty", FAIL, "影片文字（IBM Plex Sans，內文/標題）"),
        ("plex-mono.sty", FAIL, "eyebrow/label（IBM Plex Mono）"),
        ("lmodern.sty", FAIL, "影片數學（Latin Modern）"),
        ("microtype.sty", WARN, "kerning/protrusion（preamble 也載它）"),
    )
    for sty, sev, why in styles:
        rc, out = _run(["kpsewhich", sty])
        if rc == 0 and out.strip():
            record(PASS, "fonts", f"{sty} 可見", f"{why}")
        else:
            record(sev, "fonts", f"{sty} 找不到",
                   f"{why}。MiKTeX 首次編譯通常自動補裝；或手動 `mpm --install` 對應 bundle"
                   "（plex / lm / microtype）")


# ── ⑥d Plex 文字真的編得出來：實 build 一個 Tex、確認非空（補 kpsewhich 盲點）──

def check_tex_compiles() -> None:
    """kpsewhich 只證 `.sty` 檔在；**不證** latex→dvisvgm 真能把 Plex 字編成 glyph。
    踩坑（2026-06-25）：MiKTeX 字型檔名庫（FNDB）stale → latex 找不到 Plex .tfm、fallback 去壞掉的
    `makemf` → 文字 render 成空白 → 場景一開頭 `IndexError` 崩，但 doctor 全綠（只查 .sty）。
    這裡實 build 一個 Plex Sans Bold＋Plex Mono 的 Tex（每次用全新 media_dir，壞掉時期的空白快取
    才不會遮住真壞），斷言 family 有 glyph 點。修法見 ENVIRONMENT.md「Plex 文字 render 成空白」。"""
    if not VENV_PY.exists() or not shutil.which("latex") or not shutil.which("kpsewhich"):
        record(INFO, "fonts", "Plex Tex 實編檢查略過", "缺 .venv／latex／kpsewhich（見上方對應區）")
        return
    probe = (
        "import sys, os, json, tempfile\n"
        "sys.path.insert(0, %r)\n"
        "os.chdir(%r)\n"
        "from pipeline import _bootstrap\n"
        "_bootstrap.bootstrap()\n"
        "import manim\n"
        "manim.config.media_dir = tempfile.mkdtemp(prefix='doctor_tex_')\n"  # fresh -> 不吃舊空白快取
        "_bootstrap.apply_tex_template()\n"
        "from manim import Tex\n"
        "import numpy as np\n"
        "try:\n"
        "    t = Tex(r'\\textbf{Hg} \\texttt{Hg}')\n"            # Plex Sans Bold + Plex Mono
        "    n = sum(int(np.asarray(m.points).shape[0]) for m in t.family_members_with_points())\n"
        "    print('DOCTOR_TEX ' + json.dumps({'ok': n > 0, 'points': n}))\n"
        "except Exception as e:\n"
        "    print('DOCTOR_TEX ' + json.dumps({'ok': False, 'error': type(e).__name__ + ': ' + str(e)[:200]}))\n"
    ) % (str(REPO / "video"), str(REPO))
    _rc, out = _run([str(VENV_PY), "-c", probe], timeout=120)  # 一次 live latex 編譯，給足時間
    data: dict = {}
    for line in (out or "").splitlines():
        if line.startswith("DOCTOR_TEX "):
            try:
                data = json.loads(line[len("DOCTOR_TEX "):])
            except Exception:
                data = {}
    fix = ("字型查找壞（latex fallback 去 makemf）。修：`initexmf --update-fndb` ＋ `initexmf --mkmaps`，"
           "再刪 `media/Tex` 快取（manim 會沿用舊空白）。詳見 ENVIRONMENT.md「Plex 文字 render 成空白」。")
    if data.get("ok"):
        record(PASS, "fonts", "Plex Tex 實編非空",
               f"latex→dvisvgm 出 {data.get('points')} 個 glyph 點（文字真的 render 得出來）")
    elif data.get("error"):
        record(FAIL, "fonts", "Plex Tex 編譯失敗（render 會崩）", f"{data['error']}。{fix}")
    else:
        record(FAIL, "fonts", "Plex Tex 實編出空白（render 會崩）", fix)


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
    video_ok = not any(_missing("Python", x) for x in ("PyYAML", "manim", "ManimPango", "pillow")) \
        and not _missing("LaTeX", "latex") and not _missing("LaTeX", "dvisvgm") \
        and not _missing("ffmpeg", "ffmpeg") and not _missing("ffmpeg", "ffprobe") \
        and not _missing("fonts", "plex-sans.sty") and not _missing("fonts", "plex-mono.sty") \
        and not _missing("fonts", "lmodern.sty") and not _missing("fonts", "Plex Tex")
    handout_fig_ok = not _missing("handout", "node") and not _missing("handout", "< 21") \
        and not _missing("handout", "Chrome")
    print("\n能力摘要\n" + "─" * 64)
    print(f"  {'✅' if video_ok else '❌'} 影片完整 render→compose 成片（venv＋LaTeX＋ffmpeg＋ffprobe）")
    print(f"  {'✅' if handout_fig_ok else '❌'} handout 圖 render／figure 稽核（Node≥21＋Chrome）")
    print("  ✅ handout build.py（純 stdlib，任何 python 皆可）")
    codex_ok = any(s == PASS and a == "codex" for s, a, *_ in _results)
    print(f"  {'✅' if codex_ok else '⚠️ '} codex 審核（Mode B 講義／video gate2；缺＝不擋產線）")

    print("\n" + "─" * 64)
    verdict = "全部必要項通過 ✅" if fails == 0 else f"{fails} 項必要缺漏 ❌（見上方 [FAIL]）"
    print(f"  {verdict}" + (f"，另有 {warns} 項提醒" if warns else ""))
    print("  細節與一次性安裝步驟見 repo 根 ENVIRONMENT.md\n")
    return 0 if fails == 0 else 1


def main() -> int:
    as_json = "--json" in sys.argv[1:]
    check_python_and_venv()
    check_ffmpeg()
    check_latex()
    check_node_and_chrome()
    check_codex()
    check_vale()
    check_forced_alignment()
    check_assets()
    check_fonts()
    check_tex_compiles()
    check_keys()
    return print_report(as_json)


if __name__ == "__main__":
    raise SystemExit(main())

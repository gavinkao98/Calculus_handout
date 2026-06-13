from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / ".tmp" / "preamble_smoketest"
TEX_FILE = ROOT / "preamble_smoketest.tex"
LOG_FILE = OUTDIR / "preamble_smoketest.log"
POS_FILE = OUTDIR / "preamble_smoketest.pos"
POSITION_TOLERANCE = 100


def build_env() -> dict[str, str]:
    env = os.environ.copy()
    miktex_log_dir = ROOT / ".cache" / "miktex-log"
    miktex_log_dir.mkdir(parents=True, exist_ok=True)
    env["MIKTEX_LOG_DIR"] = str(miktex_log_dir)
    return env


def run_pdflatex() -> subprocess.CompletedProcess[str]:
    if OUTDIR.exists():
        shutil.rmtree(OUTDIR)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        [
            "pdflatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            f"-output-directory={OUTDIR}",
            str(TEX_FILE),
        ],
        cwd=ROOT,
        env=build_env(),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def read_log() -> str:
    if LOG_FILE.exists():
        return LOG_FILE.read_text(encoding="utf-8", errors="replace")
    return ""


def read_positions() -> dict[str, int]:
    if not POS_FILE.exists():
        return {}

    positions: dict[str, int] = {}
    for raw_line in POS_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
        key, _, value = raw_line.partition("=")
        if not key or not value:
            continue
        positions[key.strip()] = int(value.strip())
    return positions


def main() -> int:
    result = run_pdflatex()
    log_text = read_log()

    if result.returncode != 0:
        sys.stdout.write(result.stdout)
        if result.stderr:
            sys.stderr.write(result.stderr)
        if log_text:
            sys.stdout.write(log_text)
        return result.returncode

    positions = read_positions()
    required = ("baseline", "indented", "aligned", "condition")
    missing = [name for name in required if name not in positions]
    if missing:
        print("book_preamble_smoketest: missing recorded positions")
        for name in missing:
            print(f"  {name}")
        return 1

    baseline = positions["baseline"]
    indented = positions["indented"]
    failures: list[str] = []
    for name in ("aligned", "condition"):
        baseline_delta = abs(positions[name] - baseline)
        indented_delta = abs(positions[name] - indented)
        if baseline_delta > POSITION_TOLERANCE and baseline_delta >= indented_delta:
            failures.append(
                f"{name}: baseline x={baseline}, indented x={indented}, got x={positions[name]}"
            )

    if failures:
        print("book_preamble_smoketest: indentation drift detected")
        for failure in failures:
            print(f"  {failure}")
        return 1

    print("book_preamble_smoketest: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""run_selftests.py -- run every video/pipeline/_selftest_*.py from ANY cwd, one summary,
non-zero exit on any red.

    python video/pipeline/run_selftests.py              # all (run with the repo .venv)
    python video/pipeline/run_selftests.py -k lint      # substring filter on the name
    python video/pipeline/run_selftests.py --list       # just list what would run

Why this exists: the selftests grew three invocation conventions (path-inserting
`python video/pipeline/_selftest_X.py`; `_bootstrap`-style `python -m pipeline._selftest_X`
from video/; one that shells out to schema.py), no single cwd ran them all, and the ad-hoc
runner lived in a scratchpad. So after the 2026-08-10 layout refactor the canonical deck
failed its own provenance gate and one selftest went red for weeks with nothing noticing
(pipeline assessment 2026-09-07, F1/F4). This runner uses the ONE convention that works for
every selftest -- `<this interpreter> -m pipeline.<name>` with cwd=video/ -- so a Phase
close-out is one command. Manim-backed tests (sizecheck / template_registry / capacity /
type_scale / theorem_regime) build Tex and take minutes; the rest finish in seconds.
The fast deck-level gates (schema + lint + derive --check on the canonical decks) are
`python tools/doctor.py --smoke`, not this.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent      # video/pipeline
VIDEO = HERE.parent
PER_TEST_TIMEOUT = 900                      # seconds; manim-backed selftests can take minutes


def discover() -> list[str]:
    return sorted(p.stem for p in HERE.glob("_selftest_*.py"))


def run_one(name: str) -> tuple[bool, float, str]:
    """(passed, seconds, combined output) for one selftest module."""
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, "-m", f"pipeline.{name}"], cwd=VIDEO,
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=PER_TEST_TIMEOUT)
        return r.returncode == 0, time.time() - t0, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired as exc:
        out = (exc.stdout or b"").decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        return False, time.time() - t0, out + f"\n[run_selftests] TIMEOUT after {PER_TEST_TIMEOUT}s"


def main(argv: "list[str] | None" = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Run all pipeline selftests from any cwd.")
    ap.add_argument("-k", metavar="SUBSTR", default="", help="only selftests whose name contains SUBSTR")
    ap.add_argument("--list", action="store_true", help="list the selftests and exit")
    args = ap.parse_args(argv)

    names = [n for n in discover() if args.k in n]
    if args.list:
        print("\n".join(names))
        return 0
    if not names:
        print(f"[run_selftests] no selftest matches {args.k!r}")
        return 1

    print(f"[run_selftests] {len(names)} selftest(s) via {sys.executable} -m pipeline.<name> (cwd={VIDEO})", flush=True)
    failed: list[str] = []
    for name in names:
        ok, dt, out = run_one(name)
        print(f"  [{'ok  ' if ok else 'FAIL'}] {name:<42} {dt:6.1f}s", flush=True)
        if not ok:
            failed.append(name)
            tail = out.strip().splitlines()[-12:]
            print("\n".join("         " + ln for ln in tail), flush=True)
    if failed:
        print(f"[run_selftests] {len(failed)}/{len(names)} RED: {', '.join(failed)}", flush=True)
        return 1
    print(f"[run_selftests] all {len(names)} green", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

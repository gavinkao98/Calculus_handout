"""capacity_selftest.py -- regression net for the L1/L2 capacity contract.

Runs sizecheck over storyboards/_demo_capacity.yml and asserts each scene's
predictive split-warning status against EXPECT. A template's placement change that
breaks the capacity prediction (the stack/span height model, the per-column pitch,
the reserved bottom band) turns this red. See DESIGN.md "內容分量變異:容量契約三層架構".

Run:  python video/capacity_selftest.py        (exit 0 = all pass, 1 = mismatch)

This needs manim (sizecheck builds the blocks to measure them), so it is a LOCAL
check, not part of the manim-free handout CI. Pair it with a template edit.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipeline import _bootstrap

_bootstrap.bootstrap()

import logging  # noqa: E402

logging.disable(logging.INFO)

import yaml  # noqa: E402

from pipeline.sizecheck import check_scenes  # noqa: E402

# True  = this scene SHOULD raise the predictive split warning (over capacity)
# False = this scene should NOT (it fits one page) -- guards against false positives
EXPECT = {
    "derivation_fit": False,
    "derivation_over": True,
    "definition_fit": False,
    "definition_over": True,
    "procedure_fit": False,
    "procedure_over": True,
    "theorem_fit": False,
    "theorem_over": True,
    "recap_fit": False,
    "recap_over": True,
    "value_table_fit": False,
    "value_table_over": True,
}

_FIXTURE = Path(__file__).resolve().parent / "storyboards" / "_demo_capacity.yml"


def _has_split_warn(issues) -> bool:
    return any("fit on one page" in m for _sev, m in issues)


def main() -> int:
    data = yaml.safe_load(_FIXTURE.read_text(encoding="utf-8"))
    meta = data["meta"]
    by_id = {s["id"]: s for s in data["scenes"]}

    missing = [sid for sid in EXPECT if sid not in by_id]
    if missing:
        print(f"[capacity] FIXTURE missing scene(s): {missing}", flush=True)
        return 1

    failures = 0
    for sid, expect_warn in EXPECT.items():
        got_warn = _has_split_warn(check_scenes(meta, [by_id[sid]]))
        ok = got_warn == expect_warn
        mark = "ok  " if ok else "FAIL"
        want = "warn" if expect_warn else "fit "
        got = "warn" if got_warn else "fit "
        print(f"  [{mark}] {sid:<18} expect={want} got={got}", flush=True)
        if not ok:
            failures += 1

    if failures:
        print(f"[capacity] {failures}/{len(EXPECT)} scene(s) mismatched the capacity "
              "contract -- a template's height model or pitch may have drifted.", flush=True)
        return 1
    print(f"[capacity] all {len(EXPECT)} scenes match the capacity contract.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

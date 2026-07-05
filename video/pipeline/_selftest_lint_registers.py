"""Self-test: G1 display-math-in-inline-register lint. Run from video/:
    python -m pipeline._selftest_lint_registers
"""
from pathlib import Path
from pipeline.lint import lint_file

FIX = Path(__file__).resolve().parent.parent / "storyboards"


def test_flags_title_and_callout_body_but_not_display_fields():
    msgs = [m for sev, m in lint_file(FIX / "_demo_registers.yml") if "inline register" in m.lower()]
    assert any("bad_title" in m for m in msgs), msgs
    assert any("bad_callout" in m for m in msgs), msgs
    assert not any("clean_scene" in m for m in msgs), msgs
    # display 欄位不觸發：訊息開頭是 "<sid>.<path>: ..."，取第一個冒號前的 path 檢查
    paths = [m.split(":", 1)[0] for m in msgs]
    assert not any(".math" in p or "math[" in p for p in paths), paths


def test_negative_control_derivation_lines():
    # _demo_derivation.yml 的 lines[]（display 欄位）滿是 \frac —— 必須零觸發
    msgs = [m for sev, m in lint_file(FIX / "_demo_derivation.yml") if "inline register" in m.lower()]
    assert msgs == [], msgs


if __name__ == "__main__":
    import sys, traceback
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS {name}")
            except Exception:
                fails += 1; print(f"FAIL {name}"); traceback.print_exc()
    sys.exit(1 if fails else 0)

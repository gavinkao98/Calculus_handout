"""Self-test: graph carrier-label role floor (P-A1/G2). Run from video/:
    python -m pipeline._selftest_graph_labels
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # graph.py top-level imports manim -- bootstrap FIRST (repo rule)

from pipeline.templates.graph import _carrier_label_role


def test_explicit_label_role_wins():
    # 作者顯式 label_role（即使是 muted）→ 尊重不動（覆蓋權，P6 warn-default 精神）
    assert _carrier_label_role({"label_role": "muted", "color_role": "blue"}) == "muted"


def test_inherited_dim_floors_to_text():
    # 繼承路徑：暗曲線（muted）的標籤升到 ink_2（"text"），曲線本身不動
    assert _carrier_label_role({"color_role": "muted"}) == "text"


def test_inherited_bright_kept():
    assert _carrier_label_role({"color_role": "amber"}) == "amber"


def test_default_secondary():
    assert _carrier_label_role({}) == "secondary"


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

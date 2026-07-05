"""Self-test: the statement register is unified. Run from video/:
    python -m pipeline._selftest_type_scale

Every declarative `statement:` line (theorem / definition / value_table / sign_chart) renders at
the ONE canonical `statement` token, not the old scattered h3=44 / prose=42 / raw 40 (2026-07-05
raw-px straggler cleanup). Locks against a template drifting back to a hard-coded size.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()

from pipeline import sizecheck
from pipeline.templates import build_blocks
from pipeline.visuals import theme as T

_STMT_PX = T._SCALE_PX["statement"]
_META = {"id": "demo", "title": "T", "chapter": "0", "section": "0.0", "sections": []}
_STMT = "Sine and cosine are continuous functions."   # plain-text statement -> a text carrier


def _statement_px(spec) -> float:
    blocks = build_blocks(spec, {"ground": "dark", "meta": _META})
    card = next(b.mobject for b in blocks if getattr(b, "id", "") == "statement")
    pxs = [sizecheck._effective_font_px(n) for n in sizecheck._prose_nodes(card)]
    return max(pxs)


def _case(template: str, extra: dict) -> dict:
    return {"template": template, "kind": "content", "title": "T", "statement": _STMT, **extra}


def test_definition_statement_uses_statement_token():
    px = _statement_px(_case("definition_math", {"math": ["$x = 1$"]}))
    assert abs(px - _STMT_PX) < 1.0, px


def test_theorem_statement_uses_statement_token():
    px = _statement_px(_case("theorem_proof", {"proof": ["$x = 1$."], "qed": "Done."}))
    assert abs(px - _STMT_PX) < 1.0, px


def test_value_table_statement_uses_statement_token():
    px = _statement_px(_case("value_table", {"header": ["A", "B"], "rows": [["$1$", "$2$"]]}))
    assert abs(px - _STMT_PX) < 1.0, px


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

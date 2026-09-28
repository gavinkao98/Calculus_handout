"""Self-test: the statement register is unified + math has exactly three tiers. Run from video/:
    python -m pipeline._selftest_type_scale

Every declarative `statement:` line (theorem / definition / value_table / sign_chart) renders at
the ONE canonical `statement` token, not the old scattered h3=44 / prose=42 / raw 40 (2026-07-05
raw-px straggler cleanup). Locks against a template drifting back to a hard-coded size.

Second guard (T2, 2026-09-14): MathRules rule 5 -- math type has THREE tiers and no more,
`math_conclusion` 62 / `math` 48 / `math_rail` 34, and the old `math_sm` 40 tier is gone
(measurably indistinguishable from 48 on screen, so it only produced inconsistency).
"""
import ast
import importlib
import pathlib

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


# --------------------------------------------------------------------------------------
# MathRules rule 5: math type has exactly three tiers (62 / 48 / 34).
#
# METHOD (static, not a render): AST-scan every pipeline/templates/*.py for calls to
# `brand.math_line(...)` and `brand.glyph(...)` -- the templates' ONLY two MathTex
# constructors (they never build MathTex directly, and never size math through T.fs();
# grepped 2026-09-14) -- and resolve each call's `size=` argument to authored px:
#   str constant  -> T._SCALE_PX[token]      (an unknown token is itself a failure)
#   num constant  -> that raw px
#   module Name   -> import the module, read the attribute (e.g. worked_example.ANSWER_PX)
#   omitted       -> the builder default, "math"
# A size that is a function parameter or an expression cannot be resolved statically and is
# skipped (graph._label / value_table._cell pass their caller's size straight through).
_MATH_TIERS_PX = {62.0, 48.0, 34.0}      # rule 5 verbatim: conclusion / body / rail-inline

# Documented non-tier sizes. Keyed (module, px) so a NEW straggler -- a new value, or the
# same value appearing in another template -- still fails. These two raw-px sites predate
# T2 and are outside its contract (they are not rail/body/conclusion math); they are on the
# kickoff §8 backlog, not licensed drift.
_NON_TIER_ALLOWED = {
    ("theorem_proof", 44.0):
        'the `statement` register (44) -- a pure-math theorem statement routes through '
        'math_line but is a declarative statement, guarded by the statement tests above',
    ("procedure_steps", 44.0):
        "a procedure step's equation (raw 44, predates T2; §8 backlog)",
    ("sign_chart", 64.0):
        "the +/- / arrow mark (raw 64, intrinsically small glyph; predates T2; §8 backlog)",
}

_TEMPLATE_DIR = pathlib.Path(sizecheck.__file__).resolve().parent / "templates"
_MATH_BUILDERS = {"math_line", "glyph"}   # brand.<name>(...) -> MathTex


def _resolve_size(node, module: str):
    """(px, label) for a statically resolvable `size=`; (None, why) otherwise."""
    if isinstance(node, ast.Constant):
        value = node.value
        if isinstance(value, str):
            px = T._SCALE_PX.get(value)
            if px is None:
                return None, f'UNKNOWN TOKEN "{value}"'
            return float(px), f'"{value}"'
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value), f"raw {value}"
    if isinstance(node, ast.Name):
        const = getattr(importlib.import_module(f"pipeline.templates.{module}"), node.id, None)
        if isinstance(const, (int, float)) and not isinstance(const, bool):
            return float(const), node.id
    return None, "not statically resolvable"


def _math_size_sites():
    """(module, lineno, px|None, label) for every math-builder call in templates/."""
    sites = []
    for path in sorted(_TEMPLATE_DIR.glob("*.py")):
        module = path.stem
        for call in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if not isinstance(call, ast.Call):
                continue
            fn = call.func
            if not (isinstance(fn, ast.Attribute) and fn.attr in _MATH_BUILDERS
                    and isinstance(fn.value, ast.Name) and fn.value.id == "brand"):
                continue
            kw = next((k for k in call.keywords if k.arg == "size"), None)
            if kw is None:
                sites.append((module, call.lineno, float(T._SCALE_PX["math"]), "default"))
                continue
            px, label = _resolve_size(kw.value, module)
            sites.append((module, call.lineno, px, label))
    return sites


def test_math_tier_tokens_are_the_three_rule5_sizes():
    got = {k: T._SCALE_PX.get(k) for k in ("math_conclusion", "math", "math_rail")}
    assert got == {"math_conclusion": 62, "math": 48, "math_rail": 34}, got


def test_math_sm_tier_is_gone():
    assert "math_sm" not in T._SCALE_PX, "math_sm 40 must be deleted, not kept as an alias"


def test_template_math_sizes_are_only_the_three_tiers():
    offenders = [(m, ln, px, lbl) for m, ln, px, lbl in _math_size_sites()
                 if px is not None and px not in _MATH_TIERS_PX
                 and (m, px) not in _NON_TIER_ALLOWED]
    assert not offenders, "math sizes outside 62/48/34: " + "; ".join(
        f"templates/{m}.py:{ln} size={lbl} -> {px:g}px" for m, ln, px, lbl in offenders)


def test_math_size_scan_still_sees_the_call_sites():
    """Guard the guard: an AST scan that silently matches nothing would pass forever."""
    resolved = [s for s in _math_size_sites() if s[2] is not None]
    assert len(resolved) >= 15, resolved


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

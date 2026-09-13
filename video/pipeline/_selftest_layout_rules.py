"""_selftest_layout_rules.py -- regression net for the six deterministic design-system rules
sizecheck gained in T3: LayoutRules L1-L3 (conclusion weight / bottom-third fill / narrow column)
and MathRules M1-M3 (prose in a math line / mixed rail register / bare operator names).

Two layers:
  1. `storyboards/_fixtures/layout_rules.yml` run through `check_scenes`, with EXPECT pinning the
     verdict of every (scene x rule) pair -- both the violations AND the clean cases, so a detector
     that stops firing and a threshold that starts over-firing are equally red.
  2. Pure-function probes for the text detectors and the L1 geometry, so the rules stay pinned even
     if the templates change what they happen to build.

Run:  python video/pipeline/_selftest_layout_rules.py   (also under run_selftests.py)
Needs manim (layer 1 builds the fixture's blocks to measure them), like _selftest_capacity.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline import _bootstrap

_bootstrap.bootstrap()

import logging  # noqa: E402

logging.disable(logging.INFO)

import yaml  # noqa: E402

from pipeline import sizecheck as S  # noqa: E402

_FIXTURE = Path(__file__).resolve().parent.parent / "storyboards" / "_fixtures" / "layout_rules.yml"

# Substring that identifies each rule in its message. Kept here (not in sizecheck) so a message
# reworded without thinking turns this red rather than silently unpinning a rule.
_RULE_MARK = {
    "L1": "LayoutRules L1",
    "L2": "LayoutRules L2",
    "L3": "LayoutRules L3",
    "M1": "MathRules 1",
    "M2": "MathRules 2",
    "M3": "MathRules 3",
}

# The verdict for EVERY (scene, rule) pair: a rule listed here must fire on that scene, and a rule
# NOT listed must stay silent. See the fixture's own comments for what each scene is built to do.
EXPECT = {
    "chain_clean":              set(),
    "rail_mixed_register":      {"M2"},
    "math_line_carries_prose":  {"M1"},
    "operators_set_italic":     {"M3"},
    "thin_column_high":         {"L2", "L3"},
    # L1 must stay SILENT on a 44 px statement over a 43 px qed -- that 1 px is what
    # L1_WEIGHT_RATIO exists to absorb. The L1 VIOLATION is pinned by the synthetic-block probes
    # below instead: post-T2 no template can be steered into one from the storyboard (the payoff
    # tier is 62 px and nothing in a body zone is authored above it), so L1 guards against a
    # future template / hook regression rather than against an authoring mistake.
    "statement_just_over_qed":  {"L2"},
}


def _fired(issues, scene_id: str) -> set:
    """Which rules fired on *scene_id*, read back out of the messages."""
    return {code for code, mark in _RULE_MARK.items()
            if any(m.startswith(f"{scene_id}.") or m.startswith(f"{scene_id}:")
                   for _sev, m in issues if mark in m)}


def _run(meta_extra: "dict | None" = None):
    data = yaml.safe_load(_FIXTURE.read_text(encoding="utf-8"))
    meta = dict(data["meta"])
    meta.update(meta_extra or {})
    return S.check_scenes(meta, data["scenes"])


def test_fixture_matrix():
    issues = _run()
    bad = []
    for sid, want in EXPECT.items():
        got = _fired(issues, sid)
        if got != want:
            bad.append(f"  {sid}: expected {sorted(want) or '[]'}, got {sorted(got) or '[]'}")
    assert not bad, "design-rule verdicts drifted:\n" + "\n".join(bad) + "\n\nall issues:\n" + \
        "\n".join(f"  {s}  {m}" for s, m in issues)


def test_rules_are_warn_by_default():
    """Zero behaviour change for existing decks: every NEW rule is advisory until opted in."""
    issues = _run()
    new = [(s, m) for s, m in issues if any(mark in m for mark in _RULE_MARK.values())]
    assert new, "the fixture must trip some of the new rules"
    assert all(s == "warn" for s, _ in new), f"a new rule defaulted to error: {new}"


def test_layout_enforce_flips_layout_family_only():
    issues = _run({"layout_enforce": True})
    for s, m in issues:
        if any(_RULE_MARK[c] in m for c in ("L1", "L2", "L3")):
            assert s == "error", f"layout_enforce did not escalate: {m}"
        if any(_RULE_MARK[c] in m for c in ("M1", "M2", "M3")):
            assert s == "warn", f"layout_enforce leaked into the math family: {m}"


def test_mathtype_enforce_flips_math_family_only():
    issues = _run({"mathtype_enforce": True})
    for s, m in issues:
        if any(_RULE_MARK[c] in m for c in ("M1", "M2", "M3")):
            assert s == "error", f"mathtype_enforce did not escalate: {m}"
        if any(_RULE_MARK[c] in m for c in ("L1", "L2", "L3")):
            assert s == "warn", f"mathtype_enforce leaked into the layout family: {m}"


# -- M1: prose in a math line ------------------------------------------------------------------

def _m1(tex: str):
    return S._math_register_issues({"id": "s", "steps": [{"math": tex}]}, "warn")


def test_m1_flags_text_macro_and_bare_words():
    assert _m1(r"0 \le |\sin\theta| \quad \text{chord shorter than arc}")
    assert _m1(r"\sin\theta \le \theta \quad \mbox{by the chord bound}")
    assert _m1(r"|\theta| \to 0 \quad (chord shorter arc)")


def test_m1_scope_is_the_display_math_line_only():
    """The rule is about a MATH LINE, and the templates decide what is one. A `theorem_proof`
    `proof[]` row goes through `brand.prose`: a whole-`$...$` row is a display equation (in
    scope), a sentence with inline math is an authored prose row (out of scope). Same split for
    `definition_math.math[]` via math_line's documented mixed-text branch."""
    def _fired(scene):
        return bool(S._math_register_issues(scene, "warn"))

    assert _fired({"id": "s", "proof": [r"$0 \le |\sin\theta| \le |\theta| \quad (\text{chord} \le \text{arc})$"]})
    assert not _fired({"id": "s", "proof": ["Take any two distinct inputs in the interval $[a,b]$."]})
    assert not _fired({"id": "s", "proof": ["Write the difference as a difference quotient."]})
    assert _fired({"id": "s", "math": [r"$\dfrac{0}{0}\quad(\text{indeterminate})$"]})
    assert not _fired({"id": "s", "math": [r"if $f(x)=0$ then $x=a$ for some $a$"]})


def test_m1_silent_on_underbrace_labels():
    """`\\underbrace{X}_{\\text{label}}` hangs the words UNDER the line -- already the move the
    rule prescribes -- so it must not read as prose sitting in the line."""
    assert not _m1(r"\underbrace{f'(g(x_0))}_{\text{outer at inner}}\;\cdot\;\underbrace{g'(x_0)}_{\text{inner derivative}}")
    assert not _m1(r"f(x_0+h)\approx \underbrace{f(x_0)+m\,h}_{\text{tangent line}}")
    # ... but a \text{} run in the LINE is still caught, underbrace elsewhere or not.
    assert _m1(r"\underbrace{g'(x_0)}_{\text{inner}} \quad \text{is never optional}")


def test_m1_silent_on_pure_math():
    """The false positives that would kill the rule: LaTeX command names are not words, and
    braces / sub-superscripts break adjacency (a fraction is not a sentence)."""
    assert not _m1(r"\frac{\sin(x+h)-\sin x}{h}")
    assert not _m1(r"\frac{dy}{du}\cdot\frac{du}{dx}")
    assert not _m1(r"2\cos\!\left(x+\tfrac h2\right)\sin\tfrac h2")
    assert not _m1(r"\lim_{h\to 0}\frac{h+h^2}{h}")
    assert not _m1(r"{{\frac{d}{dx}\tan x}} = {{\sec^{2} x}}")


# -- M2: mixed register in the annotation rail --------------------------------------------------

def _m2(reason: str):
    return S._rail_register_issues({"id": "s", "steps": [{"math": "x", "reason": reason}]}, "warn")


def test_m2_flags_math_plus_running_words():
    assert _m2(r"write $h=2\cdot(h/2)$")
    assert _m2(r"cancel $h$")
    assert _m2(r"quotient rule on $\tfrac{\cos x}{\sin x}$")


def test_m2_silent_on_a_single_register():
    assert not _m2("sum-to-product")                    # all sans
    assert not _m2(r"$A=x+h,\ B=x$")                    # all math
    assert not _m2(r"$h(0)=h(2)=0$")                    # all math
    assert not _m2(r"$\div\sin\theta$, $\tan=\tfrac{\sin}{\cos}$")   # two spans, only punctuation between


# -- M3: operator names set as italic variables -------------------------------------------------

def _m3(tex: str):
    return S._operator_upright_issues({"id": "s", "steps": [{"math": tex}]}, "warn")


def test_m3_flags_bare_operator_names():
    assert _m3(r"lim_{h\to 0} \frac{sin h}{h}")
    assert _m3(r"cos^{2}x + \sin^{2}x")


def test_m3_silent_on_control_sequences():
    assert not _m3(r"\lim_{h\to 0}\frac{\sin h}{h}")
    assert not _m3(r"\arcsin x + \arccos x")            # \arcsin is one run, not a bare `sin`
    assert not _m3(r"\operatorname{sinh} x")            # upright already, via \operatorname
    assert not _m3(r"\text{the inner derivative}")      # \text body is M1's business, not M3's


# -- L1 geometry -------------------------------------------------------------------------------

def _px_node(px: float):
    """A MathTex authored at *px* on-screen. Built through the CONSTRUCTOR, not by assigning
    `.font_size` afterwards: manim's setter only scales the mob and leaves `_font_size` at the
    default, and `_font_size` is what `_authored_font_px` reads."""
    from manim import MathTex
    from pipeline.visuals import theme as T
    return MathTex("x", font_size=px * T.PX_TO_FS)


def test_authored_px_survives_substring_isolation():
    """The bug `_authored_font_px` exists for: a `{{...}}`-segmented MathTex rebuilds its
    submobjects after `initial_height` is taken, so manim's public `font_size` getter reads far
    over the authored size. The authored reading must stay put."""
    from pipeline import brand
    from pipeline.visuals import theme as T
    seg = brand.math_line(r"{{\lim_{h\to 0}}} {{\frac{h + h^2}{h}}}", "dark",
                          role="primary", size="math")
    assert abs(S._authored_font_px(seg) - T._SCALE_PX["math"]) < 1.0, \
        f"authored px drifted: {S._authored_font_px(seg)}"


def test_l1_flags_a_setup_heavier_than_the_payoff():
    from pipeline.blocks import Block
    blocks = [Block(id="result", mobject=_px_node(34)),
              Block(id="statement", mobject=_px_node(48))]
    out = S._conclusion_weight_issues({"id": "s"}, blocks, "warn")
    assert out and "statement" in out[0][1] and out[0][0] == "warn"


def test_l1_silent_when_the_payoff_leads():
    from pipeline.blocks import Block
    blocks = [Block(id="result", mobject=_px_node(62)),
              Block(id="statement", mobject=_px_node(48))]
    assert S._conclusion_weight_issues({"id": "s"}, blocks, "warn") == []


def test_l1_ignores_the_masthead_and_decoration():
    """An h1 title outweighs every conclusion by construction, so the header ids and the
    decoration layer must not count as set-up."""
    from pipeline.blocks import Block
    blocks = [Block(id="result", mobject=_px_node(62)),
              Block(id="title", mobject=_px_node(78)),
              Block(id="motif", mobject=_px_node(520), layer="decoration")]
    assert S._conclusion_weight_issues({"id": "s"}, blocks, "warn") == []


def test_l1_silent_without_a_conclusion_block():
    from pipeline.blocks import Block
    blocks = [Block(id="math.0", mobject=_px_node(48))]
    assert S._conclusion_weight_issues({"id": "s"}, blocks, "warn") == []


def test_rect_union_area_counts_overlap_once():
    assert abs(S._rect_union_area([(0, 2, 0, 2)]) - 4.0) < 1e-9
    assert abs(S._rect_union_area([(0, 2, 0, 2), (1, 3, 1, 3)]) - 7.0) < 1e-9   # 4 + 4 - 1
    assert S._rect_union_area([]) == 0.0


if __name__ == "__main__":
    test_fixture_matrix()
    test_rules_are_warn_by_default()
    test_layout_enforce_flips_layout_family_only()
    test_mathtype_enforce_flips_math_family_only()
    test_m1_flags_text_macro_and_bare_words()
    test_m1_scope_is_the_display_math_line_only()
    test_m1_silent_on_underbrace_labels()
    test_m1_silent_on_pure_math()
    test_m2_flags_math_plus_running_words()
    test_m2_silent_on_a_single_register()
    test_m3_flags_bare_operator_names()
    test_m3_silent_on_control_sequences()
    test_authored_px_survives_substring_isolation()
    test_l1_flags_a_setup_heavier_than_the_payoff()
    test_l1_silent_when_the_payoff_leads()
    test_l1_ignores_the_masthead_and_decoration()
    test_l1_silent_without_a_conclusion_block()
    test_rect_union_area_counts_overlap_once()
    print("OK layout-rules self-test")

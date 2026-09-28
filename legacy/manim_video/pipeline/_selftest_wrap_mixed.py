"""Self-test: brand._wrap_mixed keeps the author's spacing around inline `$math$`
(code review 2026-09-23 D2-03).

Run from video/:  python -m pipeline._selftest_wrap_mixed

`_wrap_mixed` used to cut a prose string into math spans + whitespace-split words and glue
back only a bare closing-punctuation word, then rebuild every line with `" ".join` -- so a
space appeared wherever a `$...$` span touched text with NO space in the source:
`($f$)` -> `( $f$)`, `$x$-axis` -> `$x$ -axis`, `$f$'s` -> `$f$ 's`, `$n$th` -> `$n$ th`,
`$\\varepsilon$–$\\delta$` -> `$\\varepsilon$ – $\\delta$`. That reached the screen in §3.1
(`all_six_tan_sec` / `all_six_cot_csc` reason "( cos x≠0)") and §3.2
(`proof_delicate_choices` motive "ε – δ"), and it applied with or without wrapping.

The contract now: a token is one whitespace-free run of the source (math spans atomic, text
glued on either side stays glued); lines are rebuilt with a single space only where the
source had whitespace, and a line only breaks at such a space.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # brand imports manim at module level -- bootstrap FIRST (repo rule)

from pipeline import brand   # noqa: E402

FS = brand._text_fs("prose")

GLUED = [
    "the $x$-axis ($f$)",
    "the inverse ($f^{-1}$) of $f$",
    "$f$'s graph",
    "the $n$th term",
    "an $\\varepsilon$–$\\delta$ argument",
    "quotient rule on $\\tfrac{\\sin x}{\\cos x}$ ($\\cos x\\neq 0$)",
    "at $x=2$, then $y=3$.",
]


def test_no_wrap_keeps_the_source_spacing_verbatim():
    assert brand._wrap_mixed("the $x$-axis ($f$)", FS, None) == ["the $x$-axis ($f$)"]
    for s in GLUED:
        assert brand._wrap_mixed(s, FS, None) == [s], (s, brand._wrap_mixed(s, FS, None))


def test_runs_of_whitespace_still_collapse_to_one_space():
    assert brand._wrap_mixed("  a   $x$\n  b  ", FS, None) == ["a $x$ b"]


def test_a_math_span_with_inner_spaces_is_one_token():
    assert brand._wrap_mixed("so $a + b = c$ holds", FS, 0.01) == ["so", "$a + b = c$", "holds"]


def test_wrapping_breaks_only_at_source_whitespace():
    text = ("the $x$-axis and the $y$-axis meet ($f$) where $f$'s graph turns, "
            "so the $n$th term of an $\\varepsilon$–$\\delta$ argument holds")
    words = text.split()
    for max_w in (0.01, 1.5, 3.0, 5.0):
        lines = brand._wrap_mixed(text, FS, max_w)
        assert " ".join(lines) == text, (max_w, lines)
        # every line is a whole run of source words -- no word was cut at a glued span
        flat = [w for ln in lines for w in ln.split(" ")]
        assert flat == words, (max_w, lines)
    # narrowest width: one source word per line, glued runs intact
    assert brand._wrap_mixed(text, FS, 0.01)[1] == "$x$-axis"


def test_glued_token_width_is_measured_piecewise():
    """A glued run is measured as its text pieces (char estimate) + its math spans (rendered
    width), not as one text string of LaTeX source characters."""
    tok = "($\\cos x\\neq 0$)"
    want = (brand.estimate_text_width("(", FS) + brand._math_render_width("$\\cos x\\neq 0$", FS)
            + brand.estimate_text_width(")", FS))
    assert abs(brand._token_width(tok, FS) - want) < 1e-9, (brand._token_width(tok, FS), want)
    # the old shapes are unchanged: bare math + trailing punctuation, and plain text
    assert abs(brand._token_width("$x$,", FS)
               - (brand._math_render_width("$x$", FS) + brand.estimate_text_width(",", FS))) < 1e-9
    assert brand._token_width("word", FS) == brand.estimate_text_width("word", FS)


def test_prose_sends_the_s31_reason_to_latex_without_the_phantom_space():
    s = "quotient rule on $\\tfrac{\\sin x}{\\cos x}$ ($\\cos x\\neq 0$)"
    mob = brand.prose(s, "dark", role="text", size="prose")
    assert "($\\cos x\\neq 0$)" in mob.tex_string, mob.tex_string
    assert "( $" not in mob.tex_string, mob.tex_string


if __name__ == "__main__":
    import sys
    import traceback
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except Exception:
                fails += 1
                print(f"FAIL {name}")
                traceback.print_exc()
    sys.exit(1 if fails else 0)

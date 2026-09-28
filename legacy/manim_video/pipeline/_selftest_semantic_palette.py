"""Stdlib assert self-test for the semantic colour axis (Direction B, 2026-09-12).

Run: .venv/Scripts/python.exe video/pipeline/_selftest_semantic_palette.py

The contract: the video's semantic colours are HUE-MATCHED to the handout's own axis in
`handout/latex/template/calcbook.sty` -- so a concept that is ochre in the PDF is ochre on
screen. LIGHT carries the handout hexes verbatim (same ground); DARK keeps the hue and
raises lightness for the navy ground. Render-free (pure dict/colour arithmetic).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.visuals import theme as T   # noqa: E402
from pipeline.blocks import ACCENT_ROLE   # noqa: E402


# The authority. Kept here as literals so this test fails loudly if either side drifts;
# `test_handout_source_of_truth_unchanged` re-reads calcbook.sty and checks these.
HANDOUT = {
    "concept":  "#994a00",   # aConcept   definition
    "result":   "#0068a7",   # aResult    theorem / proposition / corollary / proof
    "practice": "#04773b",   # aPractice  example / solution
    "caution":  "#aa3333",   # aCaution   caution
    "strategy": "#6453a7",   # aStrategy  strategy
    "aside":    "#5d646f",   # aAside     remark
}
SEMANTIC_ROLES = tuple(HANDOUT)
DARK_HUE_TOLERANCE_DEG = 4.0


def _hue(hex_str: str) -> float:
    """Hue in degrees (HSL convention). Grey returns 0.0."""
    h = hex_str.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hi, lo = max(r, g, b), min(r, g, b)
    d = hi - lo
    if d == 0:
        return 0.0
    if hi == r:
        deg = 60 * (((g - b) / d) % 6)
    elif hi == g:
        deg = 60 * (((b - r) / d) + 2)
    else:
        deg = 60 * (((r - g) / d) + 4)
    return deg % 360


def _lum(hex_str: str) -> float:
    h = hex_str.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _hue_delta(a: float, b: float) -> float:
    d = abs(a - b) % 360
    return min(d, 360 - d)


# -- the palette carries every semantic role -----------------------------------

def test_both_grounds_define_every_semantic_role():
    for ground, pal in (("dark", T.DARK), ("light", T.LIGHT)):
        for role in SEMANTIC_ROLES:
            assert role in pal, f"{ground} palette is missing semantic role {role!r}"
            assert role + "_ink" in pal, f"{ground} palette is missing {role}_ink"


def test_color_resolves_semantic_roles_without_falling_back():
    """theme.color() silently falls back to 'primary' for unknown roles -- a missing
    semantic key would render as ink and look merely 'a bit dull', never like an error."""
    for ground in ("dark", "light"):
        primary = T.color(ground, "primary")
        for role in SEMANTIC_ROLES:
            got = T.color(ground, role)
            assert got != primary, f"{ground}/{role} fell back to primary ({primary})"


# -- the handout correspondence ------------------------------------------------

def test_light_carries_the_handout_hexes_verbatim():
    """LIGHT is a paper ground, same as the PDF -- no lifting, so the hexes must match."""
    for role, want in HANDOUT.items():
        got = T.LIGHT[role].lower()
        assert got == want, f"light/{role} is {got}, handout says {want}"


def test_dark_preserves_the_handout_hue():
    for role, paper in HANDOUT.items():
        got = T.DARK[role]
        delta = _hue_delta(_hue(got), _hue(paper))
        assert delta <= DARK_HUE_TOLERANCE_DEG, (
            f"dark/{role} hue {_hue(got):.1f} deg drifts {delta:.1f} deg from the "
            f"handout's {_hue(paper):.1f} deg (tolerance {DARK_HUE_TOLERANCE_DEG})")


def test_dark_is_lifted_enough_to_read_on_navy():
    bg = _lum(T.DARK["bg"])
    for role in SEMANTIC_ROLES:
        assert _lum(T.DARK[role]) > bg + 0.18, (
            f"dark/{role} is too close in luminance to the navy ground")


def test_handout_source_of_truth_unchanged():
    """Re-read calcbook.sty. If the handout retunes its axis this test fails here rather
    than letting the two production lines drift apart silently."""
    sty = (Path(__file__).resolve().parents[2]
           / "handout" / "latex" / "template" / "calcbook.sty")
    if not sty.exists():                       # handout tree not checked out; skip
        return
    text = sty.read_text(encoding="utf-8", errors="replace")
    names = {"concept": "aConcept", "result": "aResult", "practice": "aPractice",
             "caution": "aCaution", "strategy": "aStrategy", "aside": "aAside"}
    import re
    for role, macro in names.items():
        m = re.search(r"\\definecolor\{" + macro + r"\}\s*\{HTML\}\{([0-9A-Fa-f]{6})\}", text)
        assert m, f"calcbook.sty no longer defines {macro}"
        assert "#" + m.group(1).lower() == HANDOUT[role], (
            f"calcbook.sty moved {macro} to #{m.group(1).lower()}; "
            f"this test (and theme.py) still say {HANDOUT[role]}")


# -- the semantic mapping ------------------------------------------------------

def test_accent_role_targets_exist_in_both_grounds():
    for accent, role in ACCENT_ROLE.items():
        for ground in ("dark", "light"):
            pal = T.palette(ground)
            assert role in pal, f"ACCENT_ROLE[{accent!r}] -> {role!r} missing from {ground}"


def test_definition_and_theorem_are_hue_distinct():
    """The bug Direction B fixes: the handout gives definition ochre and theorem blue;
    the video used to give definition blue and theorem amber -- i.e. swapped."""
    d = T.color("dark", ACCENT_ROLE["definition"])
    t = T.color("dark", ACCENT_ROLE["theorem"])
    assert _hue_delta(_hue(d), _hue(t)) > 90, (
        f"definition ({d}) and theorem ({t}) are not hue-distinct")


def test_definition_follows_the_handouts_concept_hue():
    got = T.color("dark", ACCENT_ROLE["definition"])
    assert _hue_delta(_hue(got), _hue(HANDOUT["concept"])) <= DARK_HUE_TOLERANCE_DEG, (
        f"definition resolves to {got}; the handout's concept hue is {HANDOUT['concept']}")


def test_theorem_family_shares_the_result_hue():
    for accent in ("theorem", "proposition", "proof"):
        assert accent in ACCENT_ROLE, f"ACCENT_ROLE is missing {accent!r}"
        got = T.color("dark", ACCENT_ROLE[accent])
        assert _hue_delta(_hue(got), _hue(HANDOUT["result"])) <= DARK_HUE_TOLERANCE_DEG, (
            f"{accent} resolves to {got}; the handout's result hue is {HANDOUT['result']}")


def test_example_is_the_practice_hue():
    got = T.color("dark", ACCENT_ROLE["example"])
    assert _hue_delta(_hue(got), _hue(HANDOUT["practice"])) <= DARK_HUE_TOLERANCE_DEG, got


def test_caution_and_remark_no_longer_share_a_colour():
    """They shared `callout` and so shared a colour; the handout separates them."""
    c = T.color("dark", ACCENT_ROLE["caution"])
    r = T.color("dark", ACCENT_ROLE["remark"])
    assert c != r, f"caution and remark both resolve to {c}"


def test_glow_agrees_with_the_stroke_colour():
    """A halo in the old hue under a retuned stroke reads as a coloured fringe."""
    for hue_name, (glow_hex, _op) in T.GLOW.items():
        assert hue_name in T.DARK, f"GLOW has {hue_name!r} with no DARK entry"
        assert glow_hex.lower() == T.DARK[hue_name].lower(), (
            f"GLOW[{hue_name}] is {glow_hex} but DARK[{hue_name}] is {T.DARK[hue_name]}")


if __name__ == "__main__":
    test_both_grounds_define_every_semantic_role()
    test_color_resolves_semantic_roles_without_falling_back()
    test_light_carries_the_handout_hexes_verbatim()
    test_dark_preserves_the_handout_hue()
    test_dark_is_lifted_enough_to_read_on_navy()
    test_handout_source_of_truth_unchanged()
    test_accent_role_targets_exist_in_both_grounds()
    test_definition_and_theorem_are_hue_distinct()
    test_definition_follows_the_handouts_concept_hue()
    test_theorem_family_shares_the_result_hue()
    test_example_is_the_practice_hue()
    test_caution_and_remark_no_longer_share_a_colour()
    test_glow_agrees_with_the_stroke_colour()
    print("OK semantic_palette self-test")

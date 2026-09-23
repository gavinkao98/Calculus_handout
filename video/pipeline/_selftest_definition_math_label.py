"""Self-test: definition_math's default eyebrow chip follows `accent` for every accent
value (code review 2026-09-23 D2-08).

Run from video/:  python -m pipeline._selftest_definition_math_label

definition_math's `LABEL` table predates Direction B's accent vocabulary: an accent it did
not list (caution / corollary / derivation / note / remark / ...) fell back to
"[ definition ]", so a scene without a `scene_role` / `kicker` / `label` override showed a
DEFINITION chip over a slate remark or a blue corollary. An accent missing from LABEL now
takes the chip scene_roles already defines for that word; corollary has its own entry.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # templates import manim at module level -- bootstrap FIRST (repo rule)

from pipeline.scene_roles import SCENE_ROLE_CHIP     # noqa: E402
from pipeline.templates import build_blocks          # noqa: E402

_META = {"id": "_t", "chapter": "Chapter 9", "section": "9.9", "title": "T", "theme": "midnight"}


def _eyebrow_tex(accent: str, **extra) -> str:
    spec = {"id": "dm", "kind": "content", "template": "definition_math", "accent": accent,
            "title": "A Frame", "say": "probe", "statement": "A statement.", **extra}
    blocks = build_blocks(spec, {"ground": "dark", "meta": _META})
    return next(b for b in blocks if b.id == "eyebrow").mobject.tex_string


def test_accents_missing_from_label_take_their_scene_role_chip():
    for accent in ("caution", "note", "remark", "derivation"):
        tex = _eyebrow_tex(accent)
        want = SCENE_ROLE_CHIP[accent].strip("[] ").upper()
        assert want in tex and "DEFINITION" not in tex, (accent, tex)


def test_corollary_has_its_own_chip():
    tex = _eyebrow_tex("corollary")
    assert "COROLLARY" in tex and "DEFINITION" not in tex, tex


def test_the_existing_label_table_is_unchanged():
    assert "DEFINITION" in _eyebrow_tex("definition")
    assert "THEOREM" in _eyebrow_tex("theorem")
    assert "NOTE" in _eyebrow_tex("warning")        # LABEL keeps warning -> [ note ]
    assert "RECAP" in _eyebrow_tex("recap")


def test_an_explicit_kicker_still_wins():
    assert "KEY IDEA" in _eyebrow_tex("remark", kicker="key idea")


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

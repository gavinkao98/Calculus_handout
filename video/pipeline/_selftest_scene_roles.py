"""Stdlib assert self-test for scene_roles.py (chip resolver) + lint scene_role checks
+ scene_head chipless rendering. Run: .venv/Scripts/python.exe video/pipeline/_selftest_scene_roles.py
The resolve_chip / lint tests are render-free (pure dict logic); the scene_head test
builds real mobjects (imports manim, renders nothing)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import scene_roles as SR   # noqa: E402
from pipeline import lint as L            # noqa: E402


# -- resolve_chip: precedence kicker > label > scene_role > default -------------

def test_exposition_roles_are_chipless():
    for role in ("motivation", "intuition", "bridge", "forward-ref", "setup", "roadmap"):
        assert SR.resolve_chip({"scene_role": role}, "[ definition ]") is None, role


def test_formal_role_maps_to_its_chip():
    assert SR.resolve_chip({"scene_role": "remark"}, "[ definition ]") == "[ remark ]"
    assert SR.resolve_chip({"scene_role": "theorem"}, "[ definition ]") == "[ theorem ]"


def test_default_used_when_no_override():
    assert SR.resolve_chip({}, "[ definition ]") == "[ definition ]"
    assert SR.resolve_chip({"accent": "definition"}, "[ table ]") == "[ table ]"


def test_kicker_wins_over_scene_role():
    # kicker is the highest-precedence explicit override (existing behaviour)
    assert SR.resolve_chip({"kicker": "derivation", "scene_role": "motivation"},
                           "[ definition ]") == "[ derivation ]"


def test_explicit_label_wins_over_scene_role():
    # protects theorem_proof's custom label from being erased by a later scene_role
    assert SR.resolve_chip({"label": "[ proof, cont. ]", "scene_role": "theorem"},
                           "[ theorem ]") == "[ proof, cont. ]"


def test_unknown_scene_role_raises():
    try:
        SR.resolve_chip({"scene_role": "bogus"}, "[ definition ]")
    except ValueError:
        return
    raise AssertionError("unknown scene_role must raise ValueError")


# -- lint: _scene_role_issues -------------------------------------------------

def test_lint_flags_unknown_scene_role():
    data = {"scenes": [{"id": "s1", "kind": "content", "scene_role": "bogus"}]}
    issues = L._scene_role_issues(data)
    assert any(sev == "error" and "bogus" in m for sev, m in issues), issues


def test_lint_flags_scene_role_label_conflict():
    data = {"scenes": [{"id": "s1", "kind": "content",
                        "scene_role": "remark", "label": "[ x ]"}]}
    issues = L._scene_role_issues(data)
    assert any(sev == "warn" and "s1" in m for sev, m in issues), issues


def test_lint_clean_on_valid_scene_role():
    data = {"scenes": [{"id": "s1", "kind": "content", "scene_role": "motivation"}]}
    assert L._scene_role_issues(data) == []


def test_lint_ignores_scenes_without_scene_role():
    data = {"scenes": [{"id": "s1", "kind": "content", "template": "definition_math",
                        "accent": "definition"}]}
    assert L._scene_role_issues(data) == []


# -- scene_head: chipless rendering (builds real mobjects) ---------------------

def test_scene_head_chipless_hides_eyebrow_but_keeps_title_y():
    from pipeline import _bootstrap
    _bootstrap.bootstrap()
    from pipeline.templates._common import scene_head
    ctx = {"ground": "dark", "meta": {}}

    def by_id(blocks, bid):
        return next(b.mobject for b in blocks if b.id == bid)

    def visible(mob):
        # a Tex is a VGroup of glyphs; the container's opacity is 0 while the glyphs
        # carry ink -- so probe the whole family, not the container.
        fam = mob.family_members_with_points()
        return bool(fam) and max(max(sm.get_fill_opacity(), sm.get_stroke_opacity())
                                 for sm in fam) > 0

    chipped = scene_head({"id": "a", "title": "Same Title"}, ctx, label="[ definition ]")
    chipless = scene_head({"id": "b", "title": "Same Title", "scene_role": "motivation"},
                          ctx, label="[ definition ]")

    # chipped eyebrow is visible; chipless eyebrow is invisible (opacity 0)
    assert visible(by_id(chipped, "eyebrow"))
    assert not visible(by_id(chipless, "eyebrow"))
    # title baseline does NOT drift: the invisible eyebrow still reserves its space
    y_chipped = by_id(chipped, "title").get_top()[1]
    y_chipless = by_id(chipless, "title").get_top()[1]
    assert abs(y_chipped - y_chipless) < 1e-6, (y_chipped, y_chipless)


if __name__ == "__main__":
    test_exposition_roles_are_chipless()
    test_formal_role_maps_to_its_chip()
    test_default_used_when_no_override()
    test_kicker_wins_over_scene_role()
    test_explicit_label_wins_over_scene_role()
    test_unknown_scene_role_raises()
    test_lint_flags_unknown_scene_role()
    test_lint_flags_scene_role_label_conflict()
    test_lint_clean_on_valid_scene_role()
    test_lint_ignores_scenes_without_scene_role()
    test_scene_head_chipless_hides_eyebrow_but_keeps_title_y()
    print("OK scene_roles self-test")

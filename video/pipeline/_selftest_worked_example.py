"""Self-test: the `worked_example` template. Run from video/:
    python -m pipeline._selftest_worked_example

Pins what the rest of the pipeline reads off this template, and the two contracts that
are easy to break from a distance:

  * GEOMETRY -- the answer band is pinned to the bottom safe margin at CONTENT_W and
    carries the frame's largest type; the step chain is flush on SPINE_X and stays clear
    of RAIL_X whenever the strategy / notes rail is open.
  * SCHEMA -- the five errors that make a malformed worked example fail loudly instead
    of rendering a problem with no answer (or a row whose reason has nowhere to go), and
    the one shape allowed to omit `result` (a non-final `part:` page).

Plus a byte-parity guard on `_derivation_issues`: worked_example shares derivation's row
grammar by REUSING its checks (schema._row_anim_issues), and that refactor must leave
derivation's own messages character-for-character identical.

Manim-backed (it builds real Tex to measure it), so it takes minutes -- same class as
_selftest_capacity / _selftest_transform.
"""
from pipeline import _bootstrap

_bootstrap.bootstrap()   # the template imports manim at module level -- bootstrap FIRST

import logging  # noqa: E402

logging.disable(logging.INFO)

from pathlib import Path  # noqa: E402

from pipeline import schema  # noqa: E402
from pipeline.blocks import accent_role  # noqa: E402
from pipeline.sizecheck import _effective_font_px, check_scenes  # noqa: E402
from pipeline.templates import build_blocks  # noqa: E402
from pipeline.templates import worked_example as WE  # noqa: E402
from pipeline.templates._common import CONTENT_W, RAIL_X, SPINE_X  # noqa: E402
from pipeline.timing import STOCK_ANIM_SECONDS, stock_animation_seconds  # noqa: E402
from pipeline.visuals import theme as T  # noqa: E402

_META = {"id": "_we", "chapter": "Demo", "section": "0.0", "title": "T", "theme": "midnight"}
_FIXTURE = Path(__file__).resolve().parent.parent / "storyboards" / "_demo_worked_example.yml"
_EPS = 0.02


def _spec(**over):
    spec = {
        "id": "we", "kind": "content", "template": "worked_example", "accent": "example",
        "number": "3.1", "title": "the companion limit",
        "prompt": "Establish the companion limit $(1-\\cos\\theta)/\\theta \\to 0$.",
        "strategy": "Multiply by the conjugate.",
        "notes": [{"math": "\\frac{\\sin\\theta}{\\theta}", "text": "$\\to 1$", "ref": "Prop 3.2"}],
        "say": "A. {show step.0} B. {show step.1} C. {show result} D.",
        "steps": [{"math": "\\frac{1-\\cos\\theta}{\\theta} = \\frac{1-\\cos^{2}\\theta}"
                           "{\\theta\\,(1+\\cos\\theta)}"},
                  {"math": "= \\frac{\\sin\\theta}{\\theta}\\cdot\\frac{\\sin\\theta}"
                           "{1+\\cos\\theta}", "anim": "transform", "frame": True}],
        "result": {"math": "\\lim_{\\theta\\to 0}\\frac{1-\\cos\\theta}{\\theta} = 0",
                   "reason": "answer"},
    }
    spec.update(over)
    return spec


def _blocks(spec=None):
    return build_blocks(spec or _spec(), {"ground": "dark", "meta": _META})


def _b(blocks, bid):
    return next(x for x in blocks if x.id == bid)


def _math_px(mob) -> float:
    """The largest authored px in a block -- what the viewer reads it at."""
    from manim import MathTex

    out = []

    def walk(m):
        if isinstance(m, MathTex):
            out.append(_effective_font_px(m))
        for s in getattr(m, "submobjects", []):
            walk(s)
    walk(mob)
    assert out, "no Tex node in the block"
    return max(out)


# -- block ids ---------------------------------------------------------------

def test_block_ids():
    ids = [b.id for b in _blocks()]
    assert set(ids) >= {"eyebrow", "prompt", "solrule", "sollead", "strategy", "note.0",
                        "step.0", "step.1", "result"}, ids
    assert "part" not in ids, "no part: in this fixture"
    assert "title" not in ids, "`title` is a tagline inside the eyebrow block, not a heading"
    assert "motif" not in ids, "the answer band already fills the corner the motif weighs"
    assert len(ids) == len(set(ids)), f"duplicate block id: {ids}"


def test_a_page_without_an_answer_band_keeps_the_corner_motif():
    spec = _spec(part={"current": 1, "total": 2}, say="A. {show step.0} B. {show step.1} C.")
    spec.pop("result")
    assert "motif" in {b.id for b in _blocks(spec)}


def test_solution_lead_says_cont_only_from_the_second_page_on():
    """`(CONT.)` asks 'does this page continue an earlier one' (current > 1) -- a different
    question from 'may this page omit the answer' (current < total). Page 1 of 2 answers
    yes to the second and no to the first."""
    def lead(part):
        spec = _spec(part=part, say="A. {show step.0} B. {show step.1} C.")
        spec.pop("result", None)
        return _b(_blocks(spec), "sollead").mobject.tex_string.lower()

    assert "cont" not in lead({"current": 1, "total": 2}), "page 1 does not continue anything"
    assert "cont" in lead({"current": 2, "total": 2})


def test_masthead_keeps_the_shared_header_ids():
    """sizecheck's HEADER set and _common.scene_spine both look for these exact ids; the
    template builds its own masthead, so this is what stops it drifting from example_head."""
    ids = {b.id for b in _blocks(_spec(part={"current": 1, "total": 2}))}
    assert {"eyebrow", "part", "prompt", "solrule", "sollead"} <= ids


# -- the answer band ---------------------------------------------------------

def test_answer_band_is_pinned_to_the_bottom_safe_margin_at_full_width():
    band = _b(_blocks(), "result").mobject
    assert abs(band.get_bottom()[1] - (-T.FRAME_H / 2 + T.SAFE_MARGIN)) < _EPS
    assert abs(band.width - CONTENT_W) < _EPS
    assert abs(band.get_left()[0] - SPINE_X) < _EPS


def test_answer_type_is_larger_than_every_step_row():
    """Layout rule 1: the conclusion is the frame's heaviest element. A 62px answer over
    48px steps is the whole reason this template exists rather than derivation+prompt."""
    blocks = _blocks()
    answer_px = _math_px(_b(blocks, "result").mobject)
    assert abs(answer_px - WE.ANSWER_PX) < 1e-6, answer_px   # px -> font_size -> px round-trip
    for bid in ("step.0", "step.1"):
        assert _math_px(_b(blocks, bid).mobject) < answer_px, bid


def test_answer_is_always_dynamic():
    assert _b(_blocks(), "result").static is False


def test_result_may_be_omitted_only_on_a_continuation_page():
    spec = _spec(part={"current": 1, "total": 2}, say="A. {show step.0} B. {show step.1} C.")
    spec.pop("result")
    ids = {b.id for b in _blocks(spec)}
    assert "result" not in ids
    assert WE.capacity_meta(spec)[0].extra_bottom == 0.0, "no band -> no reserved band"


# -- columns -----------------------------------------------------------------

def test_steps_are_flush_on_the_spine_and_the_rail_on_RAIL_X():
    blocks = _blocks()
    for bid in ("step.0", "step.1"):
        assert abs(_b(blocks, bid).mobject.get_left()[0] - SPINE_X) < _EPS, bid
    for bid in ("strategy", "note.0"):
        assert abs(_b(blocks, bid).mobject.get_left()[0] - RAIL_X) < _EPS, bid


def test_a_rail_keeps_the_steps_out_of_its_column():
    blocks = _blocks()
    for bid in ("step.0", "step.1"):
        assert _b(blocks, bid).mobject.get_right()[0] < RAIL_X, bid


def test_without_a_rail_the_steps_get_the_full_content_width():
    spec = _spec()
    spec.pop("strategy")
    spec.pop("notes")
    blocks = _blocks(spec)
    assert not [b for b in blocks if b.id.startswith(("strategy", "note.", "rail."))]
    # the same chain builds without the rail guard firing, at the same left edge
    assert abs(_b(blocks, "step.0").mobject.get_left()[0] - SPINE_X) < _EPS


def test_a_row_too_wide_for_the_rail_column_raises_and_names_itself():
    spec = _spec(steps=[{"math": "x " + "+ 1 " * 40 + "= 0"}],
                 say="A. {show step.0} B. {show result} C.")
    try:
        _blocks(spec)
    except ValueError as exc:
        msg = str(exc)
        assert "step.0" in msg, msg
        assert "strategy" in msg and "notes" in msg, "must name the drop-the-rail way out"
        assert "u wide" in msg and "only" in msg, "must give the width and the limit"
        return
    raise AssertionError("an over-wide row with a rail open must stop the build (D7)")


# -- reveal timing -----------------------------------------------------------

def test_rail_is_static_unless_the_narration_reveals_it():
    blocks = _blocks()
    assert _b(blocks, "strategy").static is True
    assert _b(blocks, "note.0").static is True
    marked = _blocks(_spec(say="A. {show strategy} B. {show note.0} C. {show step.0} "
                               "D. {show step.1} E. {show result} F."))
    assert _b(marked, "strategy").static is False
    assert _b(marked, "note.0").static is False


def test_transform_row_is_a_callable_that_advertises_its_seconds():
    block = _b(_blocks(), "step.1")
    assert callable(block.anim)
    want = STOCK_ANIM_SECONDS["transform"] + WE.derivation.FRAME_SECONDS   # frame: true
    assert block.anim_seconds == want, block.anim_seconds
    assert stock_animation_seconds(block.anim) == want
    assert _b(_blocks(), "step.0").anim == "write", "the first row has nothing to morph FROM"


def test_result_can_morph_from_the_last_step():
    spec = _spec()
    spec["result"] = {**spec["result"], "anim": "transform"}
    block = _b(_blocks(spec), "result")
    assert callable(block.anim)
    assert block.anim_seconds == STOCK_ANIM_SECONDS["transform"]


# -- accent ------------------------------------------------------------------

def test_accent_defaults_to_the_handout_example_green():
    spec = _spec()
    spec.pop("accent")
    _blocks(spec)
    assert accent_role(spec) == "practice", "build must write the default back for scene_spine"


# -- schema ------------------------------------------------------------------

def _errors(scene) -> "list[str]":
    return [m for sev, m in schema._worked_example_issues(scene["id"], scene) if sev == "error"]


def test_schema_requires_a_prompt():
    scene = _spec()
    scene.pop("prompt")
    assert any(".prompt:" in m for m in _errors(scene)), _errors(scene)


def test_schema_rejects_a_row_reason():
    scene = _spec()
    scene["steps"][0]["reason"] = "multiply by the conjugate"
    assert any("steps[0].reason" in m for m in _errors(scene)), _errors(scene)
    scene2 = _spec(check={"math": "x = x", "reason": "verified"})
    assert any("check.reason" in m for m in _errors(scene2)), _errors(scene2)


def test_schema_rejects_back_compat_lines():
    scene = _spec(lines=["a = b"])
    assert any(".lines:" in m for m in _errors(scene)), _errors(scene)


def test_schema_requires_a_result():
    scene = _spec()
    scene.pop("result")
    assert any(".result:" in m for m in _errors(scene)), _errors(scene)


def test_schema_lets_a_continuation_page_omit_the_result():
    scene = _spec(part={"current": 1, "total": 2})
    scene.pop("result")
    assert not _errors(scene), _errors(scene)
    final = _spec(part={"current": 2, "total": 2})
    final.pop("result")
    assert any(".result:" in m for m in _errors(final)), "the LAST page still needs one"


def test_schema_checks_seg_roles_against_the_rows_segments():
    scene = _spec()
    scene["steps"][0]["seg_roles"] = {"\\theta": "concept"}
    issues = schema._seg_roles_issues(scene["id"], scene)
    assert any("no {{...}} segments" in m for _s, m in issues), issues


def test_schema_checks_notes_and_strategy_shape():
    assert any("notes[0].math" in m for m in _errors(_spec(notes=[{"text": "no maths"}])))
    assert any(".strategy:" in m for m in _errors(_spec(strategy=42)))


def test_schema_reuses_the_shared_row_anim_checks():
    scene = _spec()
    scene["steps"][1] = {**scene["steps"][1], "anim": "cancel"}
    assert any("segments to point at" in m for m in _errors(scene)), _errors(scene)


# -- byte parity: derivation's own messages must not have moved ---------------

_DERIVATION_FIXTURE = {
    "id": "der", "kind": "content", "template": "derivation",
    "steps": [{"math": "a = b", "frame": True},
              {"math": "= c", "anim": "cancel", "cancel": [0]},
              {"math": "= d", "cancel": [1]}],
    "result": {"math": "{{= e}} {{+ 0}}", "anim": "cancel", "cancel": [5]},
}
_DERIVATION_EXPECTED = [
    ("error", "der.steps[0].frame: only applies with anim: transform | cancel (this row: None)"),
    ("error", "der.steps[1]: anim: cancel needs the previous row cut into {{...}} segments to point at"),
    ("error", "der.steps[2].cancel: needs anim: cancel (this row: None)"),
    ("error", "der.result: anim: cancel needs the previous row cut into {{...}} segments to point at"),
]


def test_derivation_messages_are_character_for_character_unchanged():
    """The row loop moved into schema._row_anim_issues so worked_example could share it.
    Pinned here as literal strings: a refactor that reworded ANY of derivation's findings
    would silently change what every existing deck's gate prints."""
    got = schema._derivation_issues("der", _DERIVATION_FIXTURE)
    assert got == _DERIVATION_EXPECTED, "\n".join(f"  {g}" for g in got)


def test_derivation_is_untouched_by_the_worked_example_checks():
    assert schema._worked_example_issues("der", _DERIVATION_FIXTURE) == []


# -- capacity (L2) on the demo fixture ---------------------------------------

def _split_warn(sid: str, data) -> bool:
    scene = next(s for s in data["scenes"] if s["id"] == sid)
    return any("fit on one page" in m for _s, m in check_scenes(data["meta"], [scene]))


def test_capacity_contract_on_the_demo_deck():
    """The two columns are audited independently and the answer band's room is counted
    ONCE (as the reserved bottom band, not also as a step row) -- the false positive that
    would otherwise fire on every scene that has an answer."""
    import yaml

    data = yaml.safe_load(_FIXTURE.read_text(encoding="utf-8"))
    assert not _split_warn("companion_limit_example", data)
    assert not _split_warn("no_rail", data)
    assert _split_warn("capacity_over", data)


def test_capacity_meta_declares_both_columns():
    plans = WE.capacity_meta(_spec())
    assert [p.x_bucket for p in plans] == [None, round(RAIL_X)]
    assert plans[0].min_pitch == WE.derivation.MIN_PITCH
    assert plans[1].min_pitch == WE.RAIL_GAP
    band = _b(_blocks(), "result").mobject
    assert abs(plans[0].extra_bottom - (band.height + WE.BAND_GAP)) < 1e-6, \
        "the reserved band must be MEASURED off the band build places (single source)"


if __name__ == "__main__":
    import sys
    import traceback

    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}", flush=True)
            except Exception:
                fails += 1
                print(f"FAIL {name}", flush=True)
                traceback.print_exc()
    print(f"[worked_example] {'all green' if not fails else f'{fails} RED'}", flush=True)
    sys.exit(1 if fails else 0)

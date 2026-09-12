"""Self-test: `carry:` / `exit:` storyboard validation (schema.py, manim-free). Run from video/:
    python -m pipeline._selftest_carry_schema

SPEC-motion-language rule 1 ("一場一張畫布"): a content scene may `carry` a block the
content scene right before it (inside the same act) built, and may `exit` blocks in its
tail. schema validates the SHAPE and the act/adjacency rule -- the things readable off
the YAML alone; block existence needs the built blocks and belongs to sizecheck
(_selftest_carry). Pins:
  (a) a well-formed carry from the immediately preceding content scene is clean
  (b) `from` that is not that scene (an earlier one, one across a divider, the act opener,
      an unknown id) is an error
  (c) `as` must be a non-empty id, unique across the entries
  (d) `to` is `keep` or {corner, scale} with a known corner and a positive scale
  (e) `to: keep` + `{show <as>}` is an error (the block is on screen from t=0)
  (f) `to: {corner}` without `{show <as>}` is a warning (the flight runs at scene end)
  (g) `exit` is a list of unique non-empty ids; carry/exit on a non-content scene is an error
"""
from pipeline import schema as S


def _content(sid, say="Words.", **extra):
    return {"id": sid, "kind": "content", "template": "callout", "title": sid, "say": say, **extra}


def _carry(src, block="plot.0", as_id="carried.x", to="keep"):
    return {"from": src, "block": block, "as": as_id, "to": to}


def _deck(*scenes):
    return {"meta": {"id": "d", "section": "0.0"}, "scenes": list(scenes)}


def _issues(*scenes):
    data = _deck(*scenes)
    return [(s, m) for s, m in S.schema_storyboard(data) if ".carry" in m or ".exit" in m
            or "'carry'" in m or "'exit'" in m]


def _errors(*scenes):
    return [m for s, m in _issues(*scenes) if s == "error"]


def _warns(*scenes):
    return [m for s, m in _issues(*scenes) if s == "warn"]


# -- (a) the good case ------------------------------------------------------------------

def test_carry_from_the_previous_content_scene_is_clean():
    deck = ({"id": "div", "kind": "divider"}, _content("a"),
            _content("b", carry=[_carry("a")]))
    assert _issues(*deck) == [], _issues(*deck)


def test_prev_content_in_act_walks_back_to_the_last_brand_frame():
    scenes = [{"id": "intro", "kind": "intro"}, _content("a"), _content("b"),
              {"id": "div", "kind": "divider"}, _content("c")]
    assert S._prev_content_in_act(scenes, 1) is None       # a opens the act
    assert S._prev_content_in_act(scenes, 2) == "a"
    assert S._prev_content_in_act(scenes, 4) is None       # c opens the next act


# -- (b) `from` ---------------------------------------------------------------------------

def test_from_must_be_the_scene_right_before():
    errs = _errors(_content("a"), _content("b"), _content("c", carry=[_carry("a")]))
    assert len(errs) == 1 and "c.carry[0].from 'a'" in errs[0] and "'b'" in errs[0], errs


def test_from_across_a_divider_is_an_error():
    errs = _errors(_content("a"), {"id": "div", "kind": "divider"},
                   _content("b", carry=[_carry("a")]))
    assert len(errs) == 1 and "opens its act" in errs[0], errs


def test_from_unknown_scene_is_an_error():
    errs = _errors(_content("a"), _content("b", carry=[_carry("zzz")]))
    assert len(errs) == 1 and "'zzz'" in errs[0], errs


def test_from_must_be_a_non_empty_string():
    errs = _errors(_content("a"), _content("b", carry=[{"block": "x", "as": "y"}]))
    assert any(".from: required" in m for m in errs), errs


# -- (c) `as` / `block` --------------------------------------------------------------------

def test_as_and_block_required():
    errs = _errors(_content("a"), _content("b", carry=[{"from": "a"}]))
    assert any(".block: required" in m for m in errs) and any(".as: required" in m for m in errs), errs


def test_as_must_be_unique_across_entries():
    errs = _errors(_content("a"), _content("b", carry=[_carry("a", "plot.0", "same"),
                                                       _carry("a", "plot.1", "same")]))
    assert len(errs) == 1 and "carry[1].as 'same'" in errs[0] and "duplicate" in errs[0], errs


# -- (d) `to` -----------------------------------------------------------------------------

def test_to_corner_shape():
    ok = _content("b", say="Go. {show carried.x} There.",
                  carry=[_carry("a", to={"corner": "top_right", "scale": 0.35})])
    assert _issues(_content("a"), ok) == []
    bad_corner = _content("b", carry=[_carry("a", to={"corner": "middle"})])
    assert any("corner" in m for m in _errors(_content("a"), bad_corner))
    bad_scale = _content("b", carry=[_carry("a", to={"corner": "top_left", "scale": 0})])
    assert any("scale" in m for m in _errors(_content("a"), bad_scale))
    bad_type = _content("b", carry=[_carry("a", to="fly")])
    assert any(".to" in m for m in _errors(_content("a"), bad_type))


def test_to_defaults_to_keep():
    entry = {"from": "a", "block": "plot.0", "as": "carried.x"}
    assert _issues(_content("a"), _content("b", carry=[entry])) == []


# -- (e)(f) the marker rules -----------------------------------------------------------------

def test_keep_with_a_show_marker_is_an_error():
    errs = _errors(_content("a"), _content("b", say="Go. {show carried.x} There.",
                                           carry=[_carry("a")]))
    assert len(errs) == 1 and "to: keep" in errs[0] and "{show carried.x}" in errs[0], errs


def test_corner_without_a_show_marker_warns_that_the_flight_is_at_scene_end():
    warns = _warns(_content("a"), _content("b", carry=[_carry("a", to={"corner": "top_right"})]))
    assert len(warns) == 1 and "scene end" in warns[0], warns


# -- (g) `exit` + non-content scenes ---------------------------------------------------------

def test_exit_shape():
    assert _issues(_content("a", exit=["axes", "plot.1"])) == []
    assert any(".exit: must be a list" in m for m in _errors(_content("a", exit="axes")))
    assert any(".exit: must be a list" in m for m in _errors(_content("a", exit=["axes", ""])))
    assert any("duplicate" in m for m in _errors(_content("a", exit=["axes", "axes"])))


def test_carry_and_exit_are_content_scene_fields():
    errs = _errors({"id": "div", "kind": "divider", "carry": [_carry("a")]})
    assert len(errs) == 1 and "'carry' is a content-scene field" in errs[0], errs
    errs = _errors({"id": "div", "kind": "divider", "exit": ["x"]})
    assert len(errs) == 1 and "'exit' is a content-scene field" in errs[0], errs


def test_carry_must_be_a_list_of_mappings():
    assert any(".carry: must be a list" in m for m in _errors(_content("a"), _content("b", carry="a")))
    assert any("not a mapping" in m for m in _errors(_content("a"), _content("b", carry=["a"])))


def test_block_may_be_a_list_of_ids():
    assert _errors(_content("a"), _content("b", carry=[_carry("a", block=["p", "q"])])) == []
    assert any(".block: a list must hold" in m
               for m in _errors(_content("a"), _content("b", carry=[_carry("a", block=[])])))
    assert any(".block: a list must hold" in m
               for m in _errors(_content("a"), _content("b", carry=[_carry("a", block=["p", ""])])))


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] carry schema green")

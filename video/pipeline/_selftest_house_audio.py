"""stdlib self-test for pipeline/house_audio.py.

Run with the bootstrap/venv python (no third-party deps needed here, but keep the
project convention):  python video/pipeline/_selftest_house_audio.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline import house_audio as ha  # noqa: E402


def test_brand_scenes_get_their_cue() -> None:
    assert ha.cue_for_scene({"kind": "intro"}) is ha._INTRO
    assert ha.cue_for_scene({"kind": "outro"}) is ha._OUTRO
    assert ha.cue_for_scene({"kind": "divider"}) is ha._DIVIDER


def test_teaching_templates_stay_dry() -> None:
    dry = (
        {"kind": "content", "template": "definition_math"},
        {"kind": "content", "template": "theorem_proof"},
        {"kind": "content", "template": "derivation"},
        {"kind": "content", "template": "graph"},
        {"kind": "content", "template": "value_table"},
        {"kind": "content", "template": "sign_chart"},
        {"kind": "content", "template": "recap_cards"},
        {"kind": "content", "template": "callout", "type": "caution"},  # ping OFF for §3.1
        {},  # default kind == content
    )
    for scene in dry:
        assert ha.cue_for_scene(scene) is None, scene


def test_candidate_b_cue_files_exist() -> None:
    for spec in (ha._INTRO, ha._OUTRO, ha._DIVIDER):
        assert spec.path.exists(), f"missing cue asset: {spec.path}"
        assert spec.path.name.startswith("candidate_b_"), spec.path.name


def test_levels_are_soft() -> None:
    assert ha._INTRO.gain == 1.0 and ha._OUTRO.gain == 1.0
    assert 0.0 < ha._DIVIDER.gain < 1.0            # "音量淡"
    for spec in (ha._INTRO, ha._OUTRO, ha._DIVIDER):
        assert spec.fade_out > 0.0


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"[selftest_house_audio] {len(tests)} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

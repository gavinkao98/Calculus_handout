"""Offline self-test for make.py per-boundary transition logic (T9 _segment_fades).
Run: python video/pipeline/_selftest_make_transition.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import make  # noqa: E402


def test_mock_synth_guard():   # Codex blocking-1: mock must not clobber real Dean WAVs
    with tempfile.TemporaryDirectory() as d:
        empty = Path(d) / "empty"; empty.mkdir()
        g = make._mock_synth_guard
        assert g(status="corrupt", existing=None, audio_dir=empty, force_clobber=False)         # corrupt -> abort
        wav = Path(d) / "aud"; (wav / "scenes").mkdir(parents=True)
        (wav / "scenes" / "07_x.wav").write_bytes(b"RIFF")
        assert g(status="absent", existing=None, audio_dir=wav, force_clobber=False)             # missing manifest + WAVs -> abort
        assert g(status="ok", existing={"backend": "mimo"}, audio_dir=empty, force_clobber=False)   # real backend -> abort
        assert g(status="ok", existing={"backend": "mock"}, audio_dir=empty, force_clobber=False) is None   # re-mock ok
        assert g(status="absent", existing=None, audio_dir=empty, force_clobber=False) is None    # first mock run ok
        assert g(status="corrupt", existing=None, audio_dir=wav, force_clobber=True) is None       # --force-clobber overrides


def test_segment_fades_brand_vs_content():
    # brand boundaries (intro/outro/divider) + the film's open/close keep `transition`;
    # a content-content boundary uses intra_act (0 = hard cut within an act).
    kinds = ["intro", "content", "content", "content", "outro"]
    assert make._segment_fades(kinds, 0.2, 0.0) == [
        (0.2, 0.2), (0.2, 0.0), (0.0, 0.0), (0.0, 0.2), (0.2, 0.2)]


def test_segment_fades_default_uniform():
    # intra_act == transition -> every boundary identical (behaviour before T9)
    assert make._segment_fades(["intro", "content", "content", "outro"], 0.2, 0.2) == [(0.2, 0.2)] * 4


def test_segment_fades_single_and_divider():
    assert make._segment_fades(["content"], 0.2, 0.0) == [(0.2, 0.2)]   # lone scene = film open+close
    # a divider between two content scenes is a brand boundary on BOTH its sides
    assert make._segment_fades(["content", "divider", "content"], 0.2, 0.0) == [
        (0.2, 0.2), (0.2, 0.2), (0.2, 0.2)]


def test_carry_boundaries_are_the_segments_that_carry_from_the_one_before():
    # SPEC-motion-language rule 1: a segment whose `carry.from` IS the previous segment
    # shares an object with it across the cut, so that boundary is a hard cut.
    a, b, c = {"id": "a"}, {"id": "b", "carry": [{"from": "a", "block": "x", "as": "y"}]}, {"id": "c"}
    assert make._carry_boundaries([a, b, c]) == {1}
    assert make._carry_boundaries([b, c]) == set(), "a --scene subset without the source: no handoff"
    assert make._carry_boundaries([a, c, b]) == set(), "from must be the segment right before"
    assert make._carry_boundaries([a, {"id": "z", "carry": "junk"}]) == set()


def test_segment_fades_carry_boundary_is_a_hard_cut_both_sides():
    kinds = ["divider", "content", "content", "content", "outro"]
    assert make._segment_fades(kinds, 0.2, 0.2, carried={2}) == [
        (0.2, 0.2), (0.2, 0.0), (0.0, 0.2), (0.2, 0.2), (0.2, 0.2)]
    # every other boundary (brand or content-content) is exactly as before
    assert make._segment_fades(kinds, 0.2, 0.2) == [(0.2, 0.2)] * 5
    assert make._segment_fades(kinds, 0.2, 0.0, carried={2, 3}) == [
        (0.2, 0.2), (0.2, 0.0), (0.0, 0.0), (0.0, 0.2), (0.2, 0.2)]


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] make transition green")

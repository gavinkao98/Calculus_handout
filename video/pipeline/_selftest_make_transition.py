"""Offline self-test for make.py per-boundary transition logic (T9 _segment_fades).
Run: python video/pipeline/_selftest_make_transition.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import make  # noqa: E402


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


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] make transition green")

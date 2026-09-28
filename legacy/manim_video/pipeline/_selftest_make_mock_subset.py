"""Offline self-test for make.py's mock-synth manifest write under `--scene` (no API, no
manim, no render: main() is stopped right after the manifest is on disk).
Run: python video/pipeline/_selftest_make_mock_subset.py"""
import json
import sys
import tempfile
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import make  # noqa: E402


class _Stop(Exception):
    """Raised where main() would move past synth into render."""


def _write_deck(path: Path, b_say: str, order: str = "abc") -> None:
    say = {"a": "Alpha one.", "b": b_say, "c": "Charlie three."}
    lines = ["meta:", "  id: _selftest_mock_subset", '  section: "9.9"', "scenes:"]
    for sid in order:
        lines += [f"  - id: {sid}", "    kind: content", f"    say: {json.dumps(say[sid])}"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _main_through_synth(storyboard: Path, sec_dir: Path, scene: str) -> None:
    """Run the real make.main() with this --scene, redirected to `sec_dir`, up to the point
    where the manifest has been written (the `pauses` fold that follows raises _Stop)."""
    def stop(*_a, **_k):
        raise _Stop

    saved = (sys.argv, make._bootstrap.section_output_dir, make.pauses)
    sys.argv = ["make.py", "--storyboard", str(storyboard), "--scene", scene,
                "--skip-schema", "--skip-lint", "--skip-sizecheck"]
    make._bootstrap.section_output_dir = lambda meta: sec_dir
    make.pauses = types.SimpleNamespace(apply_pauses=stop)
    try:
        make.main()
    except _Stop:
        pass
    else:
        raise AssertionError("main() went past synth")
    finally:
        sys.argv, make._bootstrap.section_output_dir, make.pauses = saved


def test_mock_scene_subset_merges_into_the_prior_manifest():
    # C-06 (code review 2026-09-23): tts.py merges a --scene subset into the prior manifest
    # (F5), but make.py's own mock writer overwrote it whole -- the other scenes' entries
    # vanished, and critic's `--scene all` (planned off the manifest) silently shrank to the
    # subset. The subset must replace only its own entries.
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        storyboard, sec_dir = d / "_selftest_mock_subset.yml", d / "sec"
        _write_deck(storyboard, "Bravo two.")
        _main_through_synth(storyboard, sec_dir, "all")
        _write_deck(storyboard, "Bravo, rewritten for the subset run.")
        _main_through_synth(storyboard, sec_dir, "b")
        manifest = json.loads((sec_dir / "audio" / "manifest.json").read_text(encoding="utf-8"))
        by_id = {s["scene_id"]: s for s in manifest["scenes"]}
        assert list(by_id) == ["a", "b", "c"], list(by_id)
        assert "rewritten" in by_id["b"]["script"], by_id["b"]["script"]   # fresh entry wins
        assert by_id["a"]["script"] == "Alpha one." and by_id["c"]["script"] == "Charlie three."
        assert [s["scene_number"] for s in manifest["scenes"]] == [1, 2, 3]


def test_mock_scene_subset_renumbers_carried_entries_to_todays_deck():
    # C-06, same as tts.py after its merge: entries carried over from an older deck order get
    # today's full-deck numbers (and their WAVs follow), or two scenes can share a number --
    # the 2026-09-13 collision that broke critic's frame extractor.
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        storyboard, sec_dir = d / "_selftest_mock_subset.yml", d / "sec"
        _write_deck(storyboard, "Bravo two.", order="abc")
        _main_through_synth(storyboard, sec_dir, "all")
        _write_deck(storyboard, "Bravo two.", order="cab")
        _main_through_synth(storyboard, sec_dir, "b")
        manifest = json.loads((sec_dir / "audio" / "manifest.json").read_text(encoding="utf-8"))
        got = [(s["scene_id"], s["scene_number"]) for s in manifest["scenes"]]
        assert got == [("c", 1), ("a", 2), ("b", 3)], got
        for s in manifest["scenes"]:
            assert Path(s["audio_file"]).name.startswith(f"{s['scene_number']:02d}_"), s["audio_file"]
            assert Path(s["audio_file"]).exists(), s["audio_file"]


def test_mock_scene_subset_over_another_identity_replaces_it_as_before():
    # a prior manifest of another identity (e.g. tts.py --backend mock records model/voice) is
    # not merged into -- merged_manifest would refuse with SystemExit -- the subset replaces it
    fresh = {"deck_id": "d", "backend": "mock", "scenes": [{"scene_id": "b", "scene_number": 2}]}
    prior = {**fresh, "model": "mimo-v2-tts", "scenes": [{"scene_id": "a", "scene_number": 1}]}
    deck = [{"id": "a"}, {"id": "b"}]
    assert make._merge_mock_subset(prior, fresh, deck, {"a": 1, "b": 2}) is fresh
    assert make._merge_mock_subset(None, fresh, deck, {"a": 1, "b": 2}) is fresh


if __name__ == "__main__":
    for name in sorted(n for n in dir() if n.startswith("test_")):
        globals()[name]()
        print(f"  ok {name}")
    print("[selftest] make mock subset green")

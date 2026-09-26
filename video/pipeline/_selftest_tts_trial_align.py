"""Chinese trial alignment tests: fake WAV/provider/model, no network or weights."""
import copy
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import tts_trial_align as A
from pipeline import tts_scene_trial as T
from pipeline._selftest_tts_scene_trial import FakeOpener, storyboard


def word(text, start, end):
    return {"word": text, "start": start, "end": end, "probability": .9}


class CueTests(unittest.TestCase):
    def map(self, texts, words, duration=4):
        beats = [{"text": text, "reveal": f"r{i}"} for i, text in enumerate(texts)]
        return A.map_cues(beats, " ".join(texts), words, duration)

    def test_chinese_repetition_uses_exact_occurrence(self):
        result = self.map(["一、一。", "一、一。"], [word("一、一。", .1, 1), word("一、一。", 2, 3)])
        self.assertEqual(result[1]["start_seconds"], 2)
        self.assertEqual(result[1]["char_start"], 2)
        self.assertFalse(result[1]["boundary"]["estimated"])

    def test_mixed_p_q_and_chinese(self):
        result = self.map(["p 跟 q。", "p 跟 q。"], [word("p", 0, .2), word("跟", .2, .3), word("q。", .3, .4),
                                                        word("p", 1, 1.2), word("跟", 1.2, 1.3), word("q。", 1.3, 1.4)])
        self.assertEqual(result[1]["start_seconds"], 1)

    def test_parent_spans_cross_cue_are_estimated(self):
        result = self.map(["甲", "乙丙"], [word("甲乙", 0, 2), word("丙", 2, 3)])
        self.assertEqual(result[1]["start_seconds"], 1)
        self.assertTrue(result[1]["boundary"]["estimated"])
        self.assertEqual(result[1]["boundary"]["source"], "character_share_within_word")

    def test_punctuation_spaces_only_normalization(self):
        self.assertEqual(A.spoken_chars("甲， p、q。"), "甲pq")
        self.assertEqual(A.spoken_chars("P+Q"), "P+Q")
        with self.assertRaises(A.TrialAlignmentError):
            self.map(["P"], [word("p", 0, 1)])

    def test_missing_char_fails(self):
        with self.assertRaises(A.TrialAlignmentError):
            self.map(["甲乙丙"], [word("甲乙", 0, 1)])

    def test_wrong_order_fails(self):
        with self.assertRaises(A.TrialAlignmentError):
            self.map(["甲乙"], [word("乙甲", 0, 1)])

    def test_nonmonotonic_fails(self):
        with self.assertRaises(A.TrialAlignmentError):
            self.map(["甲乙"], [word("甲", 1, 2), word("乙", 0, .5)])

    def test_overlap_fails(self):
        with self.assertRaises(A.TrialAlignmentError):
            self.map(["甲乙"], [word("甲", 0, 2), word("乙", 1, 3)])

    def test_out_of_bounds_and_nan_fail(self):
        for start, end in [(-.1, 1), (0, 5), (float("nan"), 1)]:
            with self.assertRaises(A.TrialAlignmentError):
                self.map(["甲"], [word("甲", start, end)])

    def test_zero_native_word_at_cue_is_estimated(self):
        result = self.map(["甲", "乙丙"], [word("甲", 0, .5), word("乙", 1, 1), word("丙", 1, 2)])
        self.assertTrue(result[1]["boundary"]["estimated"])
        self.assertEqual(result[1]["boundary"]["source"], "stable_ts_zero_duration_boundary")

    def test_zero_spoken_beat_rejects_export(self):
        with self.assertRaises(A.TrialAlignmentError):
            self.map(["甲", "乙", "丙"], [word("甲", 0, .5), word("乙", 1, 1), word("丙", 1, 2)])

    def test_scene_policy_boundaries_and_reveal_only(self):
        result = self.map(["甲", ""], [word("甲", .4, 1)], duration=2)
        self.assertEqual(result[0]["start_seconds"], 0)
        self.assertEqual(result[1]["start_seconds"], 2)
        self.assertEqual(result[1]["boundary"]["source"], "scene_end_policy")


class TrialTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.trial, self.output = self.root / "trial", self.root / "export"
        source = self.root / "source.yml"
        data = storyboard(2)
        data["meta"]["id"] = "fixture"
        source.write_text(T.yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
        self.plan = T.save_plan(source, self.trial)
        T.run_batch(self.trial, self.plan["plan_snapshot_hash"], opener=FakeOpener(), connection=("fake", T.BASE_URL))
        self.model = self.root / "small.pt"
        self.model.write_bytes(b"fake model")
        self.calls = []
        self.raw = {"segments": [{"words": [word("你好，", .02, .2), word("再見！", .25, .45)]}]}
        def align(*args, **kwargs):
            self.calls.append((args, kwargs))
            return SimpleNamespace(to_dict=lambda: copy.deepcopy(self.raw))
        self.fake_stable = SimpleNamespace(__version__="test", load_model=lambda *a, **k: SimpleNamespace(align=align))

    def run_align(self):
        with patch.object(A, "SMALL_SHA256", A.sha256_file(self.model)), patch.dict(sys.modules, {
                "stable_whisper": self.fake_stable, "torch": SimpleNamespace(set_num_threads=lambda n: None)}):
            return A.align_trial(self.trial, self.output, self.model)

    def test_all_success_receipts_verified(self):
        plan, completed = A.validate_trial(self.trial)
        self.assertEqual(len(completed), 2)
        self.assertEqual(plan, self.plan)

    def test_incomplete_batch_rejected_before_model(self):
        lines = (self.trial / "ledger.jsonl").read_text(encoding="utf-8").splitlines()
        (self.trial / "ledger.jsonl").write_text("\n".join(lines[:2]) + "\n", encoding="utf-8")
        with self.assertRaises(A.TrialAlignmentError):
            self.run_align()
        self.assertEqual(self.calls, [])

    def test_missing_wav_and_hash_mismatch_rejected(self):
        path = next((self.trial / "takes").glob("*/raw.wav"))
        original = path.read_bytes()
        path.write_bytes(original + b"changed")
        with self.assertRaises(ValueError):
            A.validate_trial(self.trial)
        path.unlink()
        with self.assertRaises(OSError):
            A.validate_trial(self.trial)

    def test_local_weights_required_never_download(self):
        self.model.unlink()
        with self.assertRaises(A.TrialAlignmentError):
            A.align_trial(self.trial, self.output, self.model)
        self.assertEqual(self.calls, [])

    def test_schema2_raw_audio_and_trial_labels(self):
        manifest = self.run_align()
        self.assertEqual(manifest["schema"], 2)
        self.assertFalse(manifest["audio_locked"])
        self.assertEqual([s["scene_id"] for s in manifest["scenes"]], ["title", "scene_0", "scene_1", "end"])
        narrated = [s for s in manifest["scenes"] if s["kind"] == "content"]
        for scene in narrated:
            self.assertNotIn("alignment", scene)  # no accidental English findWord consumption
            self.assertEqual(A.sha256_file(self.output / scene["audio_file"]), scene["audio_sha256"])
            self.assertFalse(scene["validation"]["human_verified_100ms"])
        self.assertTrue((self.output / "cue-quality.json").is_file())
        self.assertEqual(len(self.calls), 2)
        self.assertTrue(all(k["language"] == "zh" for _, k in self.calls))

    def test_cache_reuse_requires_identical_inputs(self):
        self.run_align()
        self.run_align()
        self.assertEqual(len(self.calls), 2)
        cache = next((self.output / "_alignment").glob("*.json"))
        saved = A.read_json(cache)
        saved["identity"]["transcript"] = "changed"
        A.write_json(cache, saved)
        self.run_align()
        self.assertEqual(len(self.calls), 3)

    def test_corrupt_cache_rejected(self):
        self.run_align()
        cache = next((self.output / "_alignment").glob("*.json"))
        saved = A.read_json(cache)
        saved["raw"]["segments"][0]["words"][0]["start"] = 0
        A.write_json(cache, saved)
        with self.assertRaises(A.TrialAlignmentError):
            self.run_align()

    def test_bad_alignment_never_publishes(self):
        self.raw["segments"][0]["words"].pop()
        with self.assertRaises(A.TrialAlignmentError):
            self.run_align()
        self.assertFalse((self.output / "manifest.json").exists())
        self.assertFalse((self.output / "scenes").exists())

    def test_external_paths_rejected(self):
        with self.assertRaises(A.TrialAlignmentError):
            A.checked_file(self.trial, "../small.pt", A.sha256_file(self.model))

    def test_aligner_abort_never_publishes_or_retries(self):
        calls = []
        def abort(*args, **kwargs):
            calls.append(args)
            return None
        self.fake_stable.load_model = lambda *a, **k: SimpleNamespace(align=abort)
        with self.assertRaises(A.TrialAlignmentError):
            self.run_align()
        self.assertEqual(len(calls), 1)
        self.assertFalse((self.output / "manifest.json").exists())

    def test_complete_fourteen_scene_batch(self):
        self.trial = self.root / "fourteen"
        data = storyboard(14)
        data["meta"]["id"] = "fixture"
        source = self.root / "fourteen.yml"
        source.write_text(T.yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
        plan = T.save_plan(source, self.trial)
        T.run_batch(self.trial, plan["plan_snapshot_hash"], opener=FakeOpener(), connection=("fake", T.BASE_URL))
        manifest = self.run_align()
        self.assertEqual(len(self.calls), 14)
        self.assertEqual(len(manifest["scenes"]), 16)


if __name__ == "__main__":
    unittest.main()

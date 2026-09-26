"""Gemini Q7 14 場合成與中文 manifest 的離線假回應回歸。"""
import copy
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import tts_scene_trial as mimo
from pipeline import tts_gemini_scene_trial as gemini
from pipeline import tts_trial_align as align
from pipeline._selftest_tts_gemini_trial import FakeOpener


class FullGeminiTrialTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / "mimo-plan.json"
        storyboard = mimo.yaml.safe_load((mimo.REPO_ROOT / "video/experiments/remotion_styles/paper/q7/q7.zh.yml")
                                           .read_text(encoding="utf-8"))
        self.mimo_plan = mimo.build_plan(storyboard, "video/experiments/remotion_styles/paper/q7/q7.zh.yml")
        self.source.write_bytes(mimo.json_bytes(self.mimo_plan))
        self.trial = self.root / "gemini"
        self.plan = gemini.save_plan(self.source, self.trial)
        self.approved = self.plan["plan_snapshot_hash"]

    def run_batch(self, opener=None):
        return gemini.run_batch(self.trial, self.approved, opener=opener or FakeOpener(), api_key="fake")

    def test_q7_all_fourteen_requests_are_complete_scene_text(self):
        self.assertEqual(self.plan["summary"], {"hard_cap_requests": 14, "planned_requests": 14,
            "characters_once": 2796, "automatic_retry": False})
        self.assertEqual(self.plan["scenes"], self.mimo_plan["scenes"])
        for request, original in zip(self.plan["requests"], self.mimo_plan["requests"]):
            self.assertEqual(request["scene_id"], original["scene_id"])
            self.assertEqual(request["segment"], original["segment"])
            self.assertEqual(request["payload"], {"model": "gemini-3.8-flash-tts",
                "input": [{"type": "user_input", "content": [{"type": "text", "text": original["segment"]["text"]}]}],
                "response_format": {"type": "audio"},
                "generation_config": {"speech_config": [{"voice": "Iapetus"}]}})

    def test_fourteen_attempts_receipts_reuse_and_manifest(self):
        fake = FakeOpener()
        self.assertEqual(self.run_batch(fake)["http_attempts_this_run"], 14)
        self.assertEqual(len(fake.calls), 14)
        attempts, completed = mimo.read_ledger(self.trial, self.plan)
        self.assertEqual((attempts, len(completed)), (14, 14))
        self.assertTrue(all(r["provider"] == "gemini" and r["voice"] == "Iapetus" for r in completed.values()))
        with patch.object(gemini.gemini, "load_key", side_effect=AssertionError):
            self.assertEqual(gemini.run_batch(self.trial, self.approved)["http_attempts_this_run"], 0)
        checked, verified = align.validate_trial(self.trial)
        self.assertEqual(checked, self.plan)
        self.assertEqual(len(verified), 14)

    def test_gemini_alignment_exports_q7zh_manifest(self):
        self.run_batch()
        model = self.root / "small.pt"
        model.write_bytes(b"fake weights")
        calls = []
        def align_scene(audio, transcript, **options):
            calls.append((audio, options))
            return SimpleNamespace(to_dict=lambda: {"segments": [{"words": [
                {"word": transcript, "start": 0.0, "end": 0.1, "probability": .9}]}]})
        fake_stable = SimpleNamespace(__version__="test", load_model=lambda *a, **k:
                                      SimpleNamespace(align=align_scene))
        output = self.root / "export"
        with patch.object(align, "SMALL_SHA256", align.sha256_file(model)), patch.dict(sys.modules, {
                "stable_whisper": fake_stable, "torch": SimpleNamespace(set_num_threads=lambda n: None)}):
            manifest = align.align_trial(self.trial, output, model)
        self.assertEqual(len(calls), 14)
        self.assertEqual(manifest["backend"], "gemini")
        self.assertEqual((manifest["model"], manifest["voice"]), (gemini.MODEL, gemini.VOICE))
        self.assertEqual(len(manifest["scenes"]), 16)
        self.assertEqual(sum(s.get("beat_count", 0) for s in manifest["scenes"]), 65)
        for scene in manifest["scenes"]:
            if "audio_file" in scene:
                self.assertEqual(align.sha256_file(output / scene["audio_file"]), scene["audio_sha256"])

    def test_unknown_stops_batch_without_retry(self):
        fake = FakeOpener(fail_at=3)
        with self.assertRaises(RuntimeError):
            self.run_batch(fake)
        self.assertEqual(len(fake.calls), 3)
        with self.assertRaisesRegex(ValueError, "unknown"):
            self.run_batch(FakeOpener())

    def test_tampering_and_missing_audio_never_resends(self):
        self.run_batch()
        wav = next((self.trial / "takes").glob("*/raw.wav"))
        wav.write_bytes(b"tampered")
        fake = FakeOpener()
        with self.assertRaises(ValueError):
            self.run_batch(fake)
        self.assertEqual(len(fake.calls), 0)

    def test_plan_contract_and_original_source_are_frozen(self):
        changed = copy.deepcopy(self.mimo_plan)
        changed["requests"][0]["segment"]["text"] = "changed"
        with self.assertRaises(ValueError):
            gemini.build_plan(changed)
        self.plan["voice"] = "Schedar"
        self.plan.pop("plan_snapshot_hash")
        self.approved = mimo.digest(self.plan)
        self.plan["plan_snapshot_hash"] = self.approved
        (self.trial / "plan.json").write_bytes(mimo.json_bytes(self.plan))
        with self.assertRaises(ValueError):
            self.run_batch()

    def test_cannot_overwrite_plan_and_run_lock(self):
        with self.assertRaises(FileExistsError):
            gemini.save_plan(self.source, self.trial)
        (self.trial / "run.lock").write_text("other run")
        with self.assertRaises(FileExistsError):
            self.run_batch()

    def test_direct_and_module_plan_cli(self):
        for index, entry in enumerate(([gemini.__file__], ["-m", "video.pipeline.tts_gemini_scene_trial"])):
            result = subprocess.run([sys.executable, *entry, "plan", "--source-plan", str(self.source),
                "--output-dir", str(self.root / f"cli{index}")], cwd=mimo.REPO_ROOT,
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('"hard_cap_requests": 14', result.stdout)


if __name__ == "__main__":
    unittest.main()

"""自然 scene 試跑安全回歸：所有 HTTP 均為本地假回應。"""
import base64
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import wave

try:
    from . import tts_scene_trial as trial
except ImportError:
    import tts_scene_trial as trial


def storyboard(count=2):
    return {"meta": {"voice": "冰糖"}, "scenes": [
        {"id": "title", "duration": 3},
        *[{"id": f"scene_{i}", "say": "你好，{show next}再見！"} for i in range(count)],
        {"id": "end", "say": "", "duration": 2}]}


def wav_bytes():
    stream = io.BytesIO()
    with wave.open(stream, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24000)
        wav.writeframes(b"\x00\x00" * 12000)
    return stream.getvalue()


class FakeOpener:
    def __init__(self, fail_at=None, response=None):
        self.calls = []
        self.fail_at = fail_at
        self.response = response or json.dumps({"id": "fake-provider-id", "usage": {"tokens": 1},
            "choices": [{"message": {"audio": {"data": base64.b64encode(wav_bytes()).decode()}}}]}).encode()

    def __call__(self, request, timeout):
        self.calls.append(request)
        if len(self.calls) == self.fail_at:
            raise TimeoutError("secret must never appear")
        return io.BytesIO(self.response)


class SceneTrialTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.output = self.root / "output"
        self.source = self.root / "storyboard.yml"
        self.make_plan()

    def make_plan(self, count=2):
        self.source.write_text(trial.yaml.safe_dump(storyboard(count), allow_unicode=True), encoding="utf-8")
        self.plan = trial.save_plan(self.source, self.output)
        self.approved = self.plan["plan_snapshot_hash"]

    def run_batch(self, fake=None):
        return trial.run_batch(self.output, self.approved, opener=fake or FakeOpener(), connection=("fake-key", trial.BASE_URL))

    def test_complete_scenes_silent_order_and_status(self):
        self.assertEqual([s["scene_id"] for s in self.plan["scenes"]], ["title", "scene_0", "scene_1", "end"])
        self.assertEqual(self.plan["scenes"][0]["duration"], 3)
        self.assertTrue(self.plan["scenes"][-1]["silent"])
        self.assertEqual(self.plan["requests"][0]["segment"]["text"], "你好，再見！")
        self.assertFalse(self.plan["audio_locked"])
        self.assertEqual(self.plan["nfa_status"], "not_verified")

    def test_general_and_fourteen_request_caps(self):
        for count in (1, 7, 14):
            plan = trial.build_plan(storyboard(count))
            self.assertEqual(plan["summary"]["hard_cap_requests"], count)
            self.assertEqual(len(plan["requests"]), count)
        self.assertFalse(self.plan["summary"]["automatic_retry"])

    def test_fourteen_scenes_call_once_each_then_zero(self):
        self.output = self.root / "fourteen"
        self.make_plan(14)
        fake = FakeOpener()
        self.assertEqual(self.run_batch(fake)["http_attempts_this_run"], 14)
        self.assertEqual(len(fake.calls), 14)
        self.assertEqual(self.run_batch(fake)["http_attempts_this_run"], 0)
        self.assertEqual(len(fake.calls), 14)

    def test_started_event_exists_before_http(self):
        fake = FakeOpener()

        def checked_opener(request, timeout):
            events = [json.loads(line) for line in (self.output / "ledger.jsonl").read_text().splitlines()]
            self.assertEqual(events[-1]["event"], "started")
            self.assertEqual(sum(e["event"] == "started" for e in events), len(fake.calls) + 1)
            return fake(request, timeout)

        self.run_batch(checked_opener)

    def test_existing_plan_never_overwritten(self):
        before = (self.output / "plan.json").read_bytes()
        with self.assertRaises(FileExistsError):
            trial.save_plan(self.source, self.output)
        self.assertEqual((self.output / "plan.json").read_bytes(), before)

    def test_modified_source_uses_frozen_snapshot(self):
        self.source.write_text("changed", encoding="utf-8")
        fake = FakeOpener()
        self.run_batch(fake)
        self.assertEqual(json.loads(fake.calls[0].data)["messages"][0]["content"], "你好，再見！")

    def test_tampering_and_wrong_approval_rejected_before_network(self):
        fake = FakeOpener()
        with self.assertRaises(ValueError):
            trial.run_batch(self.output, "bad", opener=fake, connection=("k", trial.BASE_URL))
        self.plan["requests"][0]["payload"]["audio"]["voice"] = "different"
        (self.output / "plan.json").write_bytes(trial.json_bytes(self.plan))
        with self.assertRaises(ValueError):
            self.run_batch(fake)
        self.assertEqual(len(fake.calls), 0)

    def test_inconsistent_rehashed_plan_rejected(self):
        self.plan["summary"]["hard_cap_requests"] = 100
        self.plan.pop("plan_snapshot_hash")
        self.approved = trial.digest(self.plan)
        self.plan["plan_snapshot_hash"] = self.approved
        (self.output / "plan.json").write_bytes(trial.json_bytes(self.plan))
        with self.assertRaises(ValueError):
            self.run_batch()

    def test_voice_and_model_environment_ignored(self):
        fake = FakeOpener()
        with patch.dict(os.environ, {"MIMO_TTS_MODEL": "wrong", "MIMO_TTS_VOICE": "wrong", "MIMO_TTS_STYLE": "wrong"}):
            self.run_batch(fake)
        payload = json.loads(fake.calls[0].data)
        self.assertEqual(payload["model"], "mimo-v2.5-tts")
        self.assertEqual(payload["audio"], {"voice": "冰糖", "format": "wav"})
        self.assertEqual(len(payload["messages"]), 1)

    def test_second_timeout_preserves_first_and_blocks_rerun(self):
        fake = FakeOpener(fail_at=2)
        with self.assertRaisesRegex(RuntimeError, "TimeoutError") as error:
            self.run_batch(fake)
        self.assertNotIn("secret", str(error.exception))
        self.assertEqual(len(list(self.output.glob("takes/*/receipt.json"))), 1)
        events = [json.loads(line) for line in (self.output / "ledger.jsonl").read_text().splitlines()]
        self.assertEqual([e["event"] for e in events], ["started", "completed", "started", "error_unknown"])
        second = FakeOpener()
        with self.assertRaises(ValueError):
            self.run_batch(second)
        self.assertEqual(len(second.calls), 0)

    def test_started_without_terminal_blocks_rerun(self):
        req = self.plan["requests"][0]
        trial.append_event(self.output, self.plan, {"event": "started", "take_id": "crashed", "scene_id": req["scene_id"], "request_hash": req["request_hash"]})
        fake = FakeOpener()
        with self.assertRaisesRegex(ValueError, "unknown"):
            self.run_batch(fake)
        self.assertEqual(len(fake.calls), 0)

    def test_successful_rerun_reuses_without_network_or_credentials(self):
        self.run_batch()
        before = {p: p.read_bytes() for p in self.output.rglob("*") if p.is_file()}
        with patch.object(trial, "load_connection", side_effect=AssertionError("must not need key")):
            result = trial.run_batch(self.output, self.approved)
        self.assertEqual(result, {"completed": 2, "reused": 2, "http_attempts_this_run": 0})
        self.assertEqual(before, {p: p.read_bytes() for p in self.output.rglob("*") if p.is_file()})

    def test_success_receipt_and_raw_audio_preserved(self):
        self.run_batch()
        count, receipts = trial.read_ledger(self.output, self.plan)
        self.assertEqual(count, 2)
        receipt = receipts["scene_0"]
        self.assertEqual(receipt["audio"]["sample_count"], 12000)
        self.assertEqual(receipt["audio"]["duration_seconds"], .5)
        self.assertEqual(receipt["provider_response_id"], "fake-provider-id")
        self.assertEqual((self.output / receipt["files"]["raw_audio"]["path"]).read_bytes(), wav_bytes())

    def test_missing_audio_refuses_regeneration(self):
        self.run_batch()
        next(self.output.glob("takes/*/raw.wav")).unlink()
        fake = FakeOpener()
        with self.assertRaises(FileNotFoundError):
            self.run_batch(fake)
        self.assertEqual(len(fake.calls), 0)

    def test_corrupt_audio_refuses_regeneration(self):
        self.run_batch()
        next(self.output.glob("takes/*/raw.wav")).write_bytes(b"changed")
        fake = FakeOpener()
        with self.assertRaisesRegex(ValueError, "hash"):
            self.run_batch(fake)
        self.assertEqual(len(fake.calls), 0)

    def test_response_preserved_when_decode_fails(self):
        raw = b'{"choices":[{"message":{"audio":{"data":"invalid-base64!"}}}]}'
        with self.assertRaises(RuntimeError):
            self.run_batch(FakeOpener(response=raw))
        self.assertEqual(next(self.output.glob("takes/*/response.json")).read_bytes(), raw)
        self.assertEqual(len(list(self.output.glob("takes/*/receipt.json"))), 0)

    def test_raw_wav_preserved_when_validation_fails(self):
        raw = b"not-a-wav"
        response = json.dumps({"choices": [{"message": {"audio": {"data": base64.b64encode(raw).decode()}}}]}).encode()
        with self.assertRaises(RuntimeError):
            self.run_batch(FakeOpener(response=response))
        self.assertEqual(next(self.output.glob("takes/*/raw.wav")).read_bytes(), raw)

    def test_existing_execution_lock_rejects_parallel_run(self):
        (self.output / "run.lock").write_text("another process")
        fake = FakeOpener()
        with self.assertRaises(FileExistsError):
            self.run_batch(fake)
        self.assertEqual(len(fake.calls), 0)
        self.assertTrue((self.output / "run.lock").exists())

    def test_redirect_rejected(self):
        self.assertIsNone(trial.NoRedirect().redirect_request(None, None, 302, "moved", {}, "https://other"))

    def test_empty_and_duplicate_scene_validation(self):
        with self.assertRaises(ValueError):
            trial.build_plan(storyboard(0))
        invalid = storyboard()
        invalid["scenes"][2]["id"] = "scene_0"
        with self.assertRaises(ValueError):
            trial.build_plan(invalid)
        invalid = storyboard()
        invalid["meta"] = {}
        with self.assertRaises(ValueError):
            trial.build_plan(invalid)

    def test_cli_direct_and_module_entry_points(self):
        for index, command in enumerate(([str(Path(trial.__file__))], ["-m", "video.pipeline.tts_scene_trial"])):
            result = subprocess.run([sys.executable, *command, "plan", "--storyboard", str(self.source),
                "--output-dir", str(self.root / f"cli_{index}")], cwd=trial.REPO_ROOT, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["planned_requests"], 2)


if __name__ == "__main__":
    unittest.main()

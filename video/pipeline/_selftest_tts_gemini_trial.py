"""三音色 runner 的離線假回應回歸，不呼叫 API。"""
import base64
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import wave

try:
    from . import tts_gemini_trial as trial
except ImportError:
    import tts_gemini_trial as trial


def wav_bytes():
    stream = io.BytesIO()
    with wave.open(stream, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24000)
        wav.writeframes(b"\x00\x01" * 2400)
    return stream.getvalue()


def response(audio=None):
    return {"id": "interaction-test", "usage": {"total_output_tokens": 3}, "steps": [
        {"type": "model_output", "content": [{"type": "audio", "data": base64.b64encode(audio or wav_bytes()).decode()}]}]}


class FakeOpener:
    def __init__(self, fail_at=None, data=None):
        self.calls, self.fail_at = [], fail_at
        self.data = json.dumps(data or response()).encode()

    def __call__(self, req, timeout):
        self.calls.append(req)
        if len(self.calls) == self.fail_at:
            raise TimeoutError("do not expose secret-key")
        return io.BytesIO(self.data)


class GeminiTrialTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.output = self.root / "trial"
        self.source = self.root / "source.json"
        original = trial.safe.build_plan({"meta": {"voice": "冰糖"}, "scenes": [
            {"id": "halfway", "say": "你好，{show next}完整說一次。"}]})
        self.source.write_bytes(trial.safe.json_bytes(original))
        self.plan = trial.save_plan(self.source, self.output)
        self.approved = self.plan["plan_snapshot_hash"]

    def run_batch(self, opener=None):
        return trial.run_batch(self.output, self.approved, opener=opener or FakeOpener(), api_key="fake")

    def test_three_voices_exact_text_no_style(self):
        fake = FakeOpener()
        self.assertEqual(self.run_batch(fake)["http_attempts_this_run"], 3)
        self.assertEqual(len(fake.calls), 3)
        for req, voice in zip(fake.calls, trial.VOICES):
            payload = json.loads(req.data)
            self.assertEqual(req.full_url, trial.ENDPOINT)
            self.assertEqual(req.get_header("X-goog-api-key"), "fake")
            self.assertEqual(payload["model"], trial.MODEL)
            self.assertEqual(payload["input"], [{"type": "user_input", "content": [{"type": "text", "text": "你好，完整說一次。"}]}])
            self.assertEqual(payload["generation_config"], {"speech_config": [{"voice": voice}]})
        self.assertEqual(self.plan["summary"]["hard_cap_requests"], 3)

    def test_last_model_output_audio_only(self):
        data = response(b"first")
        data["steps"].append({"type": "model_output", "content": [{"type": "text", "text": "ignored"},
            {"type": "audio", "data": base64.b64encode(wav_bytes()).decode()}]})
        data["steps"].append({"type": "user_input", "content": [{"type": "audio", "data": "ignored"}]})
        self.assertEqual(trial.decode_audio(data), wav_bytes())

    def test_preserves_complete_wav_receipt(self):
        self.run_batch()
        count, completed = trial.safe.read_ledger(self.output, self.plan)
        self.assertEqual(count, 3)
        receipt = completed["halfway.Iapetus"]
        self.assertEqual(receipt["provider_response_id"], "interaction-test")
        self.assertEqual(receipt["usage"], {"total_output_tokens": 3})
        self.assertEqual(receipt["audio"]["duration_seconds"], .1)
        self.assertEqual((self.output / receipt["files"]["raw_audio"]["path"]).read_bytes(), wav_bytes())

    def test_rerun_zero_calls_and_no_key_read(self):
        self.run_batch()
        fake = FakeOpener()
        with patch.object(trial, "load_key", side_effect=AssertionError):
            result = trial.run_batch(self.output, self.approved, opener=fake)
        self.assertEqual(result["reused"], 3)
        self.assertEqual(len(fake.calls), 0)

    def test_timeout_no_retry_and_unknown_blocks_rerun(self):
        fake = FakeOpener(fail_at=2)
        with self.assertRaises(RuntimeError) as error:
            self.run_batch(fake)
        self.assertNotIn("secret-key", str(error.exception))
        self.assertEqual(len(fake.calls), 2)
        retry = FakeOpener()
        with self.assertRaises(ValueError):
            self.run_batch(retry)
        self.assertEqual(len(retry.calls), 0)

    def test_started_before_http_and_unfinished_blocks(self):
        req = self.plan["requests"][0]
        trial.safe.append_event(self.output, self.plan, {"event": "started", "take_id": "crash", "scene_id": req["scene_id"], "request_hash": req["request_hash"]})
        with self.assertRaisesRegex(ValueError, "unknown"):
            self.run_batch()

    def test_http_error_body_preserved_without_retry(self):
        calls = []
        def fail(req, timeout):
            calls.append(req)
            events = (self.output / "ledger.jsonl").read_text().splitlines()
            self.assertEqual(json.loads(events[-1])["event"], "started")
            raise urllib.error.HTTPError(req.full_url, 400, "bad secret-key", {}, io.BytesIO(b'{"error":"test"}'))
        with self.assertRaises(RuntimeError) as error:
            self.run_batch(fail)
        self.assertEqual(len(calls), 1)
        self.assertNotIn("secret-key", str(error.exception))
        self.assertEqual(next(self.output.glob("takes/*/response.json")).read_bytes(), b'{"error":"test"}')

    def test_decode_failure_preserves_response(self):
        fake = FakeOpener(data={"steps": []})
        with self.assertRaises(RuntimeError):
            self.run_batch(fake)
        self.assertEqual(next(self.output.glob("takes/*/response.json")).read_bytes(), fake.data)

    def test_changed_audio_blocks_reuse(self):
        self.run_batch()
        next(self.output.glob("takes/*/raw.wav")).write_bytes(b"changed")
        fake = FakeOpener()
        with self.assertRaises(ValueError):
            self.run_batch(fake)
        self.assertEqual(len(fake.calls), 0)

    def test_wrong_hash_and_rehashed_contract_tamper_blocked(self):
        with self.assertRaises(ValueError):
            trial.read_plan(self.output, "wrong")
        self.plan["summary"]["hard_cap_requests"] = 4
        self.plan.pop("plan_snapshot_hash")
        self.approved = trial.safe.digest(self.plan)
        self.plan["plan_snapshot_hash"] = self.approved
        (self.output / "plan.json").write_bytes(trial.safe.json_bytes(self.plan))
        with self.assertRaises(ValueError):
            self.run_batch()

    def test_plan_cannot_overwrite(self):
        with self.assertRaises(FileExistsError):
            trial.save_plan(self.source, self.output)

    def test_direct_and_module_cli(self):
        for index, entry in enumerate(([trial.__file__], ["-m", "video.pipeline.tts_gemini_trial"])):
            result = subprocess.run([sys.executable, *entry, "plan", "--source-plan", str(self.source),
                "--output-dir", str(self.root / f"cli{index}")], cwd=trial.safe.REPO_ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["hard_cap_requests"], 3)


if __name__ == "__main__":
    unittest.main()

"""Gemini 官方預設音色三次同稿試聽；凍結 plan、無重試、unknown 禁止補送。"""
from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
import urllib.error
import urllib.request
import uuid

try:
    from . import tts_scene_trial as safe
except ImportError:
    import tts_scene_trial as safe

MODEL = "gemini-3.8-flash-tts"
VOICES = ("Iapetus", "Sulafat", "Schedar")
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"


def build_plan(source: dict, source_path: str) -> dict:
    if source.get("scene_id") != "halfway" or not isinstance(source.get("text"), str) or not source["text"].strip():
        raise ValueError("來源必須是 halfway 的非空完整文字")
    if source.get("text_hash") != safe.sha(source["text"].encode("utf-8")):
        raise ValueError("來源文字 hash 不符")
    requests = []
    for voice in VOICES:
        payload = {"model": MODEL, "input": [{"type": "user_input", "content": [
            {"type": "text", "text": source["text"]}]}], "response_format": {"type": "audio"},
            "generation_config": {"speech_config": [{"voice": voice}]}}
        requests.append({"scene_id": f"halfway.{voice}", "source_scene_id": "halfway", "voice": voice,
                         "payload": payload, "request_hash": safe.digest(payload)})
    plan = {"version": 1, "mode": "gemini_preset_trial", "source_path": source_path,
            "source": source, "model": MODEL, "voices": list(VOICES), "endpoint": ENDPOINT,
            "requests": requests, "summary": {"hard_cap_requests": 3, "planned_requests": 3,
                "characters_once": len(source["text"]), "automatic_retry": False},
            "audio_locked": False, "nfa_status": "not_verified"}
    plan["plan_snapshot_hash"] = safe.digest(plan)
    return plan


def save_plan(source_path: Path, output_dir: Path) -> dict:
    original = json.loads(source_path.read_text(encoding="utf-8"))
    if safe.digest({k: v for k, v in original.items() if k != "plan_snapshot_hash"}) != original["plan_snapshot_hash"]:
        raise ValueError("來源 MiMo plan hash 不符")
    matches = [r for r in original["requests"] if r["scene_id"] == "halfway"]
    if len(matches) != 1:
        raise ValueError("來源必須恰有一個 halfway scene")
    segment = matches[0]["segment"]
    source = {"scene_id": "halfway", "text": segment["text"], "text_hash": segment["text_hash"],
              "plan_snapshot_hash": original["plan_snapshot_hash"]}
    plan = build_plan(source, str(source_path.resolve()))
    output_dir.mkdir(parents=True, exist_ok=True)
    safe.write_new(output_dir / "plan.json", safe.json_bytes(plan))
    return plan


def read_plan(output_dir: Path, approved_hash: str) -> dict:
    plan = json.loads((output_dir / "plan.json").read_text(encoding="utf-8"))
    if (plan.get("plan_snapshot_hash") != approved_hash or
            safe.digest({k: v for k, v in plan.items() if k != "plan_snapshot_hash"}) != approved_hash):
        raise ValueError("plan 與授權 hash 不符")
    if build_plan(plan["source"], plan["source_path"]) != plan:
        raise ValueError("plan 不符合固定三音色契約")
    return plan


def load_key() -> str:
    env_path = safe.REPO_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8-sig").splitlines():
            name, separator, value = line.strip().partition("=")
            if separator and name.strip() == "GEMINI_API_KEY":
                os.environ.setdefault("GEMINI_API_KEY", value.strip().strip("\"'"))
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ValueError("缺少 GEMINI_API_KEY")
    return key


def decode_audio(data: dict) -> bytes:
    blocks = [part for step in data.get("steps", []) if step.get("type") == "model_output"
              for part in step.get("content", []) if part.get("type") == "audio"]
    if not blocks:
        raise ValueError("回應沒有 model_output audio")
    return base64.b64decode(blocks[-1]["data"], validate=True)


def run_batch(output_dir: Path, approved_hash: str, *, opener=None, api_key=None) -> dict:
    plan = read_plan(output_dir, approved_hash)
    lock = output_dir / "run.lock"
    safe.write_new(lock, str(os.getpid()).encode("ascii"))
    try:
        attempts, completed = safe.read_ledger(output_dir, plan)
        reused = len(completed)
        if reused == 3:
            return {"completed": 3, "reused": 3, "http_attempts_this_run": 0}
        key = api_key if api_key is not None else load_key()
        opener = opener or urllib.request.build_opener(safe.NoRedirect()).open
        for request in plan["requests"]:
            if request["scene_id"] in completed:
                continue
            if attempts >= 3:
                raise ValueError("已達三次 HTTP 硬上限")
            take_id = str(uuid.uuid4())
            take_dir = output_dir / "takes" / take_id
            take_dir.mkdir(parents=True, exist_ok=False)
            payload = safe.json_bytes(request["payload"])
            safe.write_new(take_dir / "payload.json", payload)
            req = urllib.request.Request(ENDPOINT, data=payload, method="POST",
                headers={"Content-Type": "application/json", "x-goog-api-key": key})
            identity = {"take_id": take_id, "scene_id": request["scene_id"], "request_hash": request["request_hash"]}
            safe.append_event(output_dir, plan, {**identity, "event": "started"})
            attempts += 1
            try:
                try:
                    with opener(req, timeout=180) as response:
                        raw_response = response.read()
                        safe.write_new(take_dir / "response.json", raw_response)
                except urllib.error.HTTPError as error:
                    safe.write_new(take_dir / "response.json", error.read())
                    raise
                data = json.loads(raw_response)
                audio = decode_audio(data)
                safe.write_new(take_dir / "raw.wav", audio)
                info = safe.wav_info(audio)
                files = {name: {"path": (take_dir / filename).relative_to(output_dir).as_posix(),
                                "sha256": safe.sha(content)}
                         for name, filename, content in (("payload", "payload.json", payload),
                             ("response", "response.json", raw_response), ("raw_audio", "raw.wav", audio))}
                receipt = {**identity, "source_scene_id": "halfway", "voice": request["voice"],
                    "model": MODEL, "provider": "gemini", "plan_snapshot_hash": approved_hash,
                    "provider_response_id": data.get("id"), "usage": data.get("usage"),
                    "audio": info, "files": files, "audio_locked": False, "nfa_status": "not_verified"}
                receipt_raw = safe.json_bytes(receipt)
                safe.write_new(take_dir / "receipt.json", receipt_raw)
                safe.append_event(output_dir, plan, {**identity, "event": "completed",
                    "receipt_path": (take_dir / "receipt.json").relative_to(output_dir).as_posix(),
                    "receipt_hash": safe.sha(receipt_raw)})
                completed[request["scene_id"]] = receipt
                print(f"完成 {request['voice']}：{info['duration_seconds']:.2f} 秒", flush=True)
            except BaseException as error:
                safe.append_event(output_dir, plan, {**identity, "event": "error_unknown", "error_type": type(error).__name__})
                raise RuntimeError(f"{request['voice']} 未完整完成（{type(error).__name__}）；停止且禁止補送") from None
        return {"completed": len(completed), "reused": reused, "http_attempts_this_run": attempts - reused}
    finally:
        lock.unlink()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser("plan")
    prepare.add_argument("--source-plan", type=Path, required=True)
    prepare.add_argument("--output-dir", type=Path, required=True)
    run = commands.add_parser("run")
    run.add_argument("--output-dir", type=Path, required=True)
    run.add_argument("--approve-plan", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "plan":
            plan = save_plan(args.source_plan, args.output_dir)
            print(json.dumps({"plan_snapshot_hash": plan["plan_snapshot_hash"], **plan["summary"]}))
        else:
            print(json.dumps(run_batch(args.output_dir, args.approve_plan)))
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

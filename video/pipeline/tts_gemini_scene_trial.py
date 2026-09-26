"""Q7 中文全片 Gemini Iapetus 試片：14 場各一次，凍結請求且不自動重試。"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import urllib.error
import urllib.request
import uuid

try:
    from . import tts_scene_trial as safe
    from . import tts_gemini_trial as gemini
except ImportError:
    import tts_scene_trial as safe
    import tts_gemini_trial as gemini

MODEL = gemini.MODEL
VOICE = "Iapetus"
HARD_CAP = 14


def build_plan(mimo_plan: dict) -> dict:
    source_hash = mimo_plan.get("plan_snapshot_hash")
    if source_hash != safe.digest({k: v for k, v in mimo_plan.items() if k != "plan_snapshot_hash"}):
        raise ValueError("來源 MiMo plan hash 不符")
    if mimo_plan != safe.build_plan(mimo_plan["source_snapshot"], mimo_plan["source_path"]):
        raise ValueError("來源 MiMo plan 不符合完整 scene 契約")
    if len(mimo_plan["requests"]) != HARD_CAP or mimo_plan["source_snapshot"]["meta"]["id"] != "q7_billiards_zh":
        raise ValueError("來源必須是 Q7 中文 14 場完整 scene plan")
    requests = []
    for original in mimo_plan["requests"]:
        segment = original["segment"]
        payload = {"model": MODEL, "input": [{"type": "user_input", "content": [
            {"type": "text", "text": segment["text"]}]}], "response_format": {"type": "audio"},
            "generation_config": {"speech_config": [{"voice": VOICE}]}}
        requests.append({"scene_id": original["scene_id"], "segment": segment,
                         "payload": payload, "request_hash": safe.digest(payload)})
    plan = {"version": 1, "mode": "gemini_scene_trial", "source_mimo_plan": mimo_plan,
            "source_snapshot": mimo_plan["source_snapshot"], "scenes": mimo_plan["scenes"],
            "model": MODEL, "voice": VOICE, "endpoint": gemini.ENDPOINT,
            "requests": requests, "summary": {"hard_cap_requests": HARD_CAP,
                "planned_requests": HARD_CAP,
                "characters_once": sum(r["segment"]["characters"] for r in requests),
                "automatic_retry": False}, "audio_locked": False, "nfa_status": "not_verified"}
    plan["plan_snapshot_hash"] = safe.digest(plan)
    return plan


def save_plan(source_plan: Path, output_dir: Path) -> dict:
    original = json.loads(source_plan.read_text(encoding="utf-8"))
    storyboard_path = safe.REPO_ROOT / "video/experiments/remotion_styles/paper/q7/q7.zh.yml"
    current_storyboard = safe.yaml.safe_load(storyboard_path.read_text(encoding="utf-8-sig"))
    if original.get("source_snapshot_hash") != safe.digest(current_storyboard):
        raise ValueError("來源 MiMo plan 與目前 q7.zh.yml 不一致")
    plan = build_plan(original)
    output_dir.mkdir(parents=True, exist_ok=True)
    safe.write_new(output_dir / "plan.json", safe.json_bytes(plan))
    return plan


def read_plan(output_dir: Path, approved_hash: str) -> dict:
    plan = json.loads((output_dir / "plan.json").read_text(encoding="utf-8"))
    if (plan.get("plan_snapshot_hash") != approved_hash or
            safe.digest({k: v for k, v in plan.items() if k != "plan_snapshot_hash"}) != approved_hash):
        raise ValueError("plan 與授權 hash 不符")
    if build_plan(plan["source_mimo_plan"]) != plan:
        raise ValueError("plan 不符合 Gemini Q7 14 場契約")
    return plan


def run_batch(output_dir: Path, approved_hash: str, *, opener=None, api_key=None) -> dict:
    plan = read_plan(output_dir, approved_hash)
    lock = output_dir / "run.lock"
    safe.write_new(lock, str(os.getpid()).encode("ascii"))
    try:
        attempts, completed = safe.read_ledger(output_dir, plan)
        reused = len(completed)
        if reused == HARD_CAP:
            return {"completed": HARD_CAP, "reused": HARD_CAP, "http_attempts_this_run": 0}
        key = api_key if api_key is not None else gemini.load_key()
        opener = opener or urllib.request.build_opener(safe.NoRedirect()).open
        for request in plan["requests"]:
            if request["scene_id"] in completed:
                continue
            if attempts >= HARD_CAP:
                raise ValueError("已達 14 次 HTTP 硬上限")
            take_id = str(uuid.uuid4())
            take_dir = output_dir / "takes" / take_id
            take_dir.mkdir(parents=True, exist_ok=False)
            payload = safe.json_bytes(request["payload"])
            safe.write_new(take_dir / "payload.json", payload)
            req = urllib.request.Request(gemini.ENDPOINT, data=payload, method="POST",
                headers={"Content-Type": "application/json", "x-goog-api-key": key})
            identity = {"take_id": take_id, "scene_id": request["scene_id"],
                        "request_hash": request["request_hash"]}
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
                audio = gemini.decode_audio(data)
                safe.write_new(take_dir / "raw.wav", audio)
                info = safe.wav_info(audio)
                files = {name: {"path": (take_dir / filename).relative_to(output_dir).as_posix(),
                                "sha256": safe.sha(content)}
                         for name, filename, content in (("payload", "payload.json", payload),
                             ("response", "response.json", raw_response), ("raw_audio", "raw.wav", audio))}
                receipt = {**identity, "voice": VOICE, "model": MODEL, "provider": "gemini",
                    "plan_snapshot_hash": approved_hash, "provider_response_id": data.get("id"),
                    "usage": data.get("usage"), "audio": info, "files": files,
                    "audio_locked": False, "nfa_status": "not_verified"}
                receipt_raw = safe.json_bytes(receipt)
                safe.write_new(take_dir / "receipt.json", receipt_raw)
                safe.append_event(output_dir, plan, {**identity, "event": "completed",
                    "receipt_path": (take_dir / "receipt.json").relative_to(output_dir).as_posix(),
                    "receipt_hash": safe.sha(receipt_raw)})
                completed[request["scene_id"]] = receipt
                print(f"完成 {request['scene_id']}：{info['duration_seconds']:.2f} 秒；累計 {attempts} 次", flush=True)
            except BaseException as error:
                safe.append_event(output_dir, plan, {**identity, "event": "error_unknown",
                                                       "error_type": type(error).__name__})
                raise RuntimeError(f"{request['scene_id']} 未完整完成（{type(error).__name__}）；停止且禁止補送") from None
        return {"completed": len(completed), "reused": reused,
                "http_attempts_this_run": attempts - reused}
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

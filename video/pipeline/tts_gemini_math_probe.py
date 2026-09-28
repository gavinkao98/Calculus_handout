"""Gemini 中文數學 A/B 試音：凍結六份請求、無重試、unknown 禁止補送。"""
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


SOURCE = safe.REPO_ROOT / "video/experiments/tts_workflow/latex_math_ab_20260927.json"
MODEL = "gemini-3.8-flash-tts"
VOICE = "Iapetus"
CASE_IDS = ("high_school", "calculus", "linear_algebra")
HARD_CAP = 6


def build_plan(source: dict) -> dict:
    if (source.get("model") != MODEL or source.get("voice") != VOICE or
            source.get("style") is not None or source.get("automatic_retry") is not False):
        raise ValueError("來源模型、聲線或參數超出授權")
    cases = source.get("cases")
    if not isinstance(cases, list) or tuple(c.get("id") for c in cases) != CASE_IDS:
        raise ValueError("來源必須是三個已核准科目")
    requests = []
    for case in cases:
        for variant, field in (("latex", "latex_input"), ("spoken", "spoken_input")):
            script = case.get(field)
            if not isinstance(script, str) or not script.strip():
                raise ValueError(f"{case['id']}.{variant} 缺少文稿")
            payload = {"model": MODEL, "input": [{"type": "user_input", "content": [
                {"type": "text", "text": script}]}], "response_format": {"type": "audio"},
                "generation_config": {"speech_config": [{"voice": VOICE}]}}
            requests.append({"scene_id": f"{case['id']}.{variant}", "case_id": case["id"],
                "variant": variant, "payload": payload, "request_hash": safe.digest(payload)})
    plan = {"version": 1, "mode": "gemini_math_latex_ab", "source": source,
        "model": MODEL, "voice": VOICE, "endpoint": gemini.ENDPOINT,
        "requests": requests, "summary": {"hard_cap_requests": HARD_CAP,
            "planned_requests": HARD_CAP, "automatic_retry": False,
            "characters_once": sum(len(r["payload"]["input"][0]["content"][0]["text"])
                                   for r in requests)}}
    plan["plan_snapshot_hash"] = safe.digest(plan)
    return plan


def save_plan(output_dir: Path) -> dict:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    plan = build_plan(source)
    output_dir.mkdir(parents=True, exist_ok=True)
    safe.write_new(output_dir / "plan.json", safe.json_bytes(plan))
    return plan


def read_plan(output_dir: Path, approved_hash: str) -> dict:
    plan = json.loads((output_dir / "plan.json").read_text(encoding="utf-8"))
    if (plan.get("plan_snapshot_hash") != approved_hash or
            safe.digest({k: v for k, v in plan.items() if k != "plan_snapshot_hash"}) != approved_hash or
            build_plan(plan["source"]) != plan):
        raise ValueError("plan 與授權文稿不符")
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
                raise ValueError("已達六次 HTTP 硬上限")
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
                receipt = {**identity, "case_id": request["case_id"], "variant": request["variant"],
                    "voice": VOICE, "model": MODEL, "provider": "gemini",
                    "plan_snapshot_hash": approved_hash, "provider_response_id": data.get("id"),
                    "usage": data.get("usage"), "audio": info, "files": files}
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
    commands.add_parser("plan").add_argument("--output-dir", required=True, type=Path)
    run = commands.add_parser("run")
    run.add_argument("--output-dir", required=True, type=Path)
    run.add_argument("--approve-plan", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "plan":
            plan = save_plan(args.output_dir)
            print(json.dumps({"plan_snapshot_hash": plan["plan_snapshot_hash"], **plan["summary"]}))
        else:
            print(json.dumps(run_batch(args.output_dir, args.approve_plan)))
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

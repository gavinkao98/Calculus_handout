"""完整 scene MiMo 試聽批次：先凍結 plan，再以明確授權的 hash 執行。

不重試、不裁音、不對齊，也不宣稱稿鎖、NFA 或音鎖完成。
任何已送出但未完整落盤的請求都視為 unknown，禁止補送。
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import urllib.request
import uuid
import wave
from datetime import datetime, timezone

try:
    from .tts_pilot_plan import digest, segment_from_scene, yaml
except ImportError:
    from tts_pilot_plan import digest, segment_from_scene, yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
MODEL = "mimo-v2.5-tts"
BASE_URL = "https://api.xiaomimimo.com/v1"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_new(path: Path, data: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def build_plan(storyboard: dict, source_path: str = "") -> dict:
    voice = storyboard.get("meta", {}).get("voice")
    if not isinstance(voice, str) or not voice.strip():
        raise ValueError("storyboard meta.voice 必須明確指定")
    scenes, requests, seen = [], [], set()
    for scene in storyboard.get("scenes", []):
        scene_id = scene.get("id")
        if not isinstance(scene_id, str) or not scene_id or scene_id in seen:
            raise ValueError("scene id 缺漏或重複")
        seen.add(scene_id)
        say = scene.get("say")
        if say is not None and not isinstance(say, str):
            raise ValueError(f"{scene_id}: say 必須為文字")
        item = {"scene_id": scene_id, "duration": scene.get("duration"),
                "silent": not bool(say and say.strip())}
        if not item["silent"]:
            segment = segment_from_scene(scene)
            payload = {"model": MODEL, "messages": [{"role": "assistant", "content": segment["text"]}],
                       "audio": {"format": "wav", "voice": voice}}
            requests.append({"scene_id": scene_id, "segment": segment,
                             "payload": payload, "request_hash": digest(payload)})
        scenes.append(item)
    if not requests:
        raise ValueError("沒有可合成的 scene")
    plan = {"version": 1, "mode": "scene_trial", "source_path": source_path,
            "source_snapshot_hash": digest(storyboard), "source_snapshot": storyboard,
            "model": MODEL, "voice": voice, "parameters": {"style": ""},
            "scenes": scenes, "requests": requests,
            "summary": {"hard_cap_requests": len(requests), "planned_requests": len(requests),
                        "characters_once": sum(r["segment"]["characters"] for r in requests),
                        "automatic_retry": False},
            "script_lock": "not_verified", "nfa_status": "not_verified", "audio_locked": False}
    plan["plan_snapshot_hash"] = digest(plan)
    return plan


def save_plan(storyboard_path: Path, output_dir: Path) -> dict:
    storyboard = yaml.safe_load(storyboard_path.read_text(encoding="utf-8-sig"))
    if not isinstance(storyboard, dict):
        raise ValueError("storyboard 必須為物件")
    plan = build_plan(storyboard, str(storyboard_path.resolve()))
    output_dir.mkdir(parents=True, exist_ok=True)
    write_new(output_dir / "plan.json", json_bytes(plan))
    return plan


def read_plan(output_dir: Path, approved_hash: str) -> dict:
    plan = json.loads((output_dir / "plan.json").read_text(encoding="utf-8"))
    stored_hash = plan.get("plan_snapshot_hash")
    if stored_hash != approved_hash or digest({k: v for k, v in plan.items() if k != "plan_snapshot_hash"}) != stored_hash:
        raise ValueError("plan hash 不符，禁止沿用舊授權")
    # Rebuild only from the saved snapshot; never re-read a changed storyboard.
    if build_plan(plan["source_snapshot"], plan["source_path"]) != plan:
        raise ValueError("plan 內容／請求契約不一致")
    return plan


def append_event(output_dir: Path, plan: dict, event: dict) -> None:
    event = {"plan_snapshot_hash": plan["plan_snapshot_hash"],
             "timestamp": datetime.now(timezone.utc).isoformat(), **event}
    with (output_dir / "ledger.jsonl").open("ab") as stream:
        stream.write(json.dumps(event, ensure_ascii=False, allow_nan=False).encode("utf-8") + b"\n")
        stream.flush()
        os.fsync(stream.fileno())


def child_path(output_dir: Path, relative: str) -> Path:
    path = (output_dir / relative).resolve()
    if not path.is_relative_to(output_dir.resolve()):
        raise ValueError("take 路徑超出批次目錄")
    return path


def verify_receipt(output_dir: Path, event: dict, request: dict) -> dict:
    raw = child_path(output_dir, event["receipt_path"]).read_bytes()
    if sha(raw) != event["receipt_hash"]:
        raise ValueError("receipt hash 不符")
    receipt = json.loads(raw)
    if (receipt["request_hash"] != request["request_hash"] or
            receipt["scene_id"] != request["scene_id"] or receipt["take_id"] != event["take_id"]):
        raise ValueError("take 身分不符")
    for info in receipt["files"].values():
        if sha(child_path(output_dir, info["path"]).read_bytes()) != info["sha256"]:
            raise ValueError("take 檔案 hash 不符，禁止重新生成")
    return receipt


def read_ledger(output_dir: Path, plan: dict) -> tuple[int, dict]:
    ledger = output_dir / "ledger.jsonl"
    events = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()] if ledger.exists() else []
    started, completed = {}, {}
    by_id = {r["scene_id"]: r for r in plan["requests"]}
    for event in events:
        if event.get("plan_snapshot_hash") != plan["plan_snapshot_hash"]:
            raise ValueError("ledger 與 plan 不符")
        scene_id, take_id = event["scene_id"], event["take_id"]
        if scene_id not in by_id or event["request_hash"] != by_id[scene_id]["request_hash"]:
            raise ValueError("ledger 與 request 不符")
        if event["event"] == "started":
            if take_id in started or scene_id in (e["scene_id"] for e in started.values()):
                raise ValueError("重複 attempt，禁止執行")
            started[take_id] = event
        elif event["event"] == "completed":
            if take_id not in started or scene_id in completed or started[take_id]["scene_id"] != scene_id:
                raise ValueError("ledger 完成事件無對應 attempt")
            completed[scene_id] = verify_receipt(output_dir, event, by_id[scene_id])
        else:
            raise ValueError("存在 error_unknown；須人工確認，禁止補送")
    if len(started) != len(completed):
        raise ValueError("存在無 terminal 的 started（unknown），禁止補送")
    if len(started) > plan["summary"]["hard_cap_requests"]:
        raise ValueError("累計 HTTP attempt 超過硬上限")
    return len(started), completed


def load_connection() -> tuple[str, str]:
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        for raw in env_path.read_text(encoding="utf-8-sig").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            if name.strip() in ("MIMO_API_KEY", "MIMO_BASE_URL"):
                os.environ.setdefault(name.strip(), value.strip().strip("\"'"))
    key = os.environ.get("MIMO_API_KEY")
    if not key:
        raise ValueError("缺少 MIMO_API_KEY")
    return key, os.environ.get("MIMO_BASE_URL", BASE_URL).rstrip("/")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    # Redirects would silently create another HTTP attempt outside the cap.
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def decode_audio(data: dict) -> bytes:
    audio = data["choices"][0]["message"]["audio"]
    if isinstance(audio, list):
        audio = audio[0]
    return base64.b64decode(audio["data"], validate=True)


def wav_info(raw: bytes) -> dict:
    with wave.open(io.BytesIO(raw), "rb") as wav:
        frames, rate = wav.getnframes(), wav.getframerate()
        channels, width = wav.getnchannels(), wav.getsampwidth()
        pcm = wav.readframes(frames)
        if not frames or len(pcm) != frames * channels * width:
            raise ValueError("WAV 空白或資料截斷")
        return {"sample_count": frames, "sample_rate": rate, "channels": channels,
                "sample_width": width, "duration_seconds": frames / rate,
                "pcm_sha256": sha(pcm)}


def run_batch(output_dir: Path, approved_hash: str, *, opener=None, connection=None) -> dict:
    plan = read_plan(output_dir, approved_hash)
    lock = output_dir / "run.lock"
    write_new(lock, str(os.getpid()).encode("ascii"))
    try:
        attempts, completed = read_ledger(output_dir, plan)
        reused = len(completed)
        if reused == len(plan["requests"]):
            return {"completed": reused, "reused": reused, "http_attempts_this_run": 0}
        key, base_url = connection if connection is not None else load_connection()
        if opener is None:
            opener = urllib.request.build_opener(NoRedirect()).open
        for request in plan["requests"]:
            if request["scene_id"] in completed:
                continue
            if attempts >= plan["summary"]["hard_cap_requests"]:
                raise ValueError("HTTP attempt 已達批次硬上限")
            take_id = str(uuid.uuid4())
            take_dir = output_dir / "takes" / take_id
            take_dir.mkdir(parents=True, exist_ok=False)
            payload_bytes = json_bytes(request["payload"])
            write_new(take_dir / "payload.json", payload_bytes)
            req = urllib.request.Request(base_url + "/chat/completions", data=payload_bytes, method="POST",
                                         headers={"Content-Type": "application/json", "api-key": key,
                                                  "Authorization": "Bearer " + key})
            identity = {"take_id": take_id, "scene_id": request["scene_id"], "request_hash": request["request_hash"]}
            append_event(output_dir, plan, {**identity, "event": "started"})
            attempts += 1
            try:
                with opener(req, timeout=180) as response:
                    response_bytes = response.read()
                    write_new(take_dir / "response.json", response_bytes)
                data = json.loads(response_bytes)
                raw_wav = decode_audio(data)
                write_new(take_dir / "raw.wav", raw_wav)
                info = wav_info(raw_wav)
                files = {}
                for name, content in (("payload", payload_bytes), ("response", response_bytes), ("raw_audio", raw_wav)):
                    filename = {"payload": "payload.json", "response": "response.json", "raw_audio": "raw.wav"}[name]
                    files[name] = {"path": (take_dir / filename).relative_to(output_dir).as_posix(), "sha256": sha(content)}
                receipt = {**identity, "plan_snapshot_hash": approved_hash, "provider": "mimo",
                           "provider_response_id": data.get("id"), "usage": data.get("usage"),
                           "audio": info, "files": files, "audio_locked": False, "nfa_status": "not_verified"}
                receipt_bytes = json_bytes(receipt)
                write_new(take_dir / "receipt.json", receipt_bytes)
                append_event(output_dir, plan, {**identity, "event": "completed",
                             "receipt_path": (take_dir / "receipt.json").relative_to(output_dir).as_posix(),
                             "receipt_hash": sha(receipt_bytes)})
                completed[request["scene_id"]] = receipt
                print(f"完成 {request['scene_id']}：{info['duration_seconds']:.2f} 秒；累計 {attempts} 次", flush=True)
            except BaseException as error:
                # Never include arbitrary provider/error text: it may contain credentials.
                append_event(output_dir, plan, {**identity, "event": "error_unknown", "error_type": type(error).__name__})
                raise RuntimeError(f"{request['scene_id']} 請求／落盤未完成（{type(error).__name__}）；已停止，禁止補送") from None
        return {"completed": len(completed), "reused": reused, "http_attempts_this_run": attempts - reused}
    finally:
        lock.unlink()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    plan_parser = commands.add_parser("plan")
    plan_parser.add_argument("--storyboard", type=Path, required=True)
    plan_parser.add_argument("--output-dir", type=Path, required=True)
    run_parser = commands.add_parser("run")
    run_parser.add_argument("--output-dir", type=Path, required=True)
    run_parser.add_argument("--approve-plan", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "plan":
            plan = save_plan(args.storyboard, args.output_dir)
            print(json.dumps({"plan_snapshot_hash": plan["plan_snapshot_hash"], **plan["summary"]}, ensure_ascii=False))
        else:
            print(json.dumps(run_batch(args.output_dir, args.approve_plan), ensure_ascii=False))
    except (OSError, ValueError, RuntimeError, KeyError, TypeError, yaml.YAMLError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

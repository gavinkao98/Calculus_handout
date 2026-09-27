"""One-shot Singapore CosyVoice SSML and word-timestamp probe.

Each text variant may be attempted once per output directory. An interrupted
attempt is terminal; a new request requires a new, explicitly approved batch.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from html import unescape
import io
import json
import os
from pathlib import Path
import re
import uuid
import wave
import xml.etree.ElementTree as ET

import websocket


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "video/_audit/REVIEW-aliyun-ssml-sync-plan-2026-09-27.html"
ENDPOINT = "wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference"
MODEL = "cosyvoice-v3-plus"
VOICE = "longanyang"
LENGTHS = {"plain": 71, "ssml": 149}


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def json_line(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def write_new(path: Path, value: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(value)
        stream.flush()
        os.fsync(stream.fileno())


def scripts() -> dict[str, str]:
    blocks = [unescape(text) for text in re.findall(
        r"<pre>(.*?)</pre>", SOURCE.read_text(encoding="utf-8"), re.S)]
    if len(blocks) != 2:
        raise ValueError("測試計畫必須恰有兩段文稿")
    plain, ssml = blocks
    if len(plain) != LENGTHS["plain"] or len(ssml) != LENGTHS["ssml"]:
        raise ValueError("文稿長度與報量不符")
    root = ET.fromstring(ssml)
    if root.tag != "speak" or "".join(root.itertext()) != plain:
        raise ValueError("兩版可朗讀文字不一致")
    if [tag.attrib for tag in root.findall("break")] != [{"time": "400ms"}] * 3:
        raise ValueError("SSML 停頓與計畫不符")
    return {"plain": plain, "ssml": ssml}


def key_from_env_file(path: Path) -> str:
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if line.startswith("DASHSCOPE_API_KEY="):
            value = line.split("=", 1)[1].strip().strip("\"'")
            if value:
                return value
    raise ValueError(".env 缺少 DASHSCOPE_API_KEY")


def normalize_wav(raw: bytes) -> tuple[bytes, float, float]:
    """Replace streaming WAV's placeholder sizes with sizes from received PCM."""
    with wave.open(io.BytesIO(raw), "rb") as source:
        channels = source.getnchannels()
        sample_width = source.getsampwidth()
        rate = source.getframerate()
        declared_duration = source.getnframes() / rate
        pcm = source.readframes(source.getnframes())
    frame_bytes = channels * sample_width
    if not pcm or len(pcm) % frame_bytes:
        raise ValueError("WAV PCM 資料為空或不完整")
    output = io.BytesIO()
    with wave.open(output, "wb") as target:
        target.setnchannels(channels)
        target.setsampwidth(sample_width)
        target.setframerate(rate)
        target.writeframes(pcm)
    return output.getvalue(), len(pcm) / frame_bytes / rate, declared_duration


def event(action: str, task_id: str, payload: dict) -> dict:
    return {"header": {"action": action, "task_id": task_id,
                       "streaming": "duplex"}, "payload": payload}


def run_task(ws: websocket.WebSocket, variant: str, text: str,
             event_log: Path) -> tuple[bytes, list[dict], dict]:
    task_id = str(uuid.uuid4())
    params = {"text_type": "PlainText", "voice": VOICE, "format": "wav",
              "sample_rate": 24000, "word_timestamp_enabled": True,
              "enable_ssml": variant == "ssml"}
    ws.send(json.dumps(event("run-task", task_id, {
        "task_group": "audio", "task": "tts", "function": "SpeechSynthesizer",
        "model": MODEL, "input": {}, "parameters": params}), ensure_ascii=False))

    chunks: list[bytes] = []
    words: list[dict] = []
    events = 0
    usage = None
    started = False
    submitted = False
    with event_log.open("xb") as log:
        while True:
            opcode, data = ws.recv_data()
            if opcode == websocket.ABNF.OPCODE_BINARY:
                chunks.append(bytes(data))
                continue
            if opcode != websocket.ABNF.OPCODE_TEXT:
                continue
            item = json.loads(data)
            log.write(json_line(item))
            log.flush()
            os.fsync(log.fileno())
            events += 1
            header = item.get("header") or {}
            if header.get("task_id") != task_id:
                raise ValueError("回應 task_id 不符")
            kind = header.get("event")
            if kind == "task-failed":
                raise ValueError("task-failed: " + str(header.get("error_code")))
            if kind == "task-started":
                if started:
                    raise ValueError("收到重複的 task-started")
                started = True
                ws.send(json.dumps(event("continue-task", task_id,
                    {"input": {"text": text}}), ensure_ascii=False))
                ws.send(json.dumps(event("finish-task", task_id,
                    {"input": {}}), ensure_ascii=False))
                submitted = True
            elif kind == "result-generated":
                output = (item.get("payload") or {}).get("output") or {}
                if output.get("type") == "sentence-end":
                    sentence = output.get("sentence") or {}
                    usage = (item.get("payload") or {}).get("usage") or usage
                    for word in sentence.get("words") or []:
                        words.append({"sentence_index": sentence.get("index"), **word})
            elif kind == "task-finished":
                if not (started and submitted):
                    raise ValueError("任務未完整提交")
                return b"".join(chunks), words, {
                    "task_id": task_id, "events": events, "audio_frames": len(chunks),
                    "usage": (item.get("payload") or {}).get("usage") or usage}


def run(variant: str, output_dir: Path, env_file: Path) -> dict:
    texts = scripts()
    key = key_from_env_file(env_file)
    output_dir.mkdir(parents=True, exist_ok=True)
    attempts_path = output_dir / "attempts.jsonl"
    attempts = [json.loads(line) for line in attempts_path.read_text(encoding="utf-8").splitlines()] if attempts_path.exists() else []
    if len(attempts) >= 2 or any(item.get("variant") == variant for item in attempts):
        raise ValueError("已達批次上限或此文稿已嘗試；禁止重送")
    if variant == "ssml" and not (output_dir / "plain" / "receipt.json").is_file():
        raise ValueError("A 版尚未完成，不能送 B 版")
    take = output_dir / variant
    take.mkdir(exist_ok=False)
    write_new(take / "request.json", json_bytes({
        "endpoint": ENDPOINT, "model": MODEL, "voice": VOICE,
        "text": texts[variant], "enable_ssml": variant == "ssml",
        "word_timestamp_enabled": True, "format": "wav", "sample_rate": 24000}))
    with attempts_path.open("ab") as log:
        log.write(json_line({"variant": variant,
                             "started_utc": datetime.now(timezone.utc).isoformat()}))
        log.flush()
        os.fsync(log.fileno())
    ws = None
    try:
        ws = websocket.create_connection(ENDPOINT,
            header=["Authorization: Bearer " + key], timeout=120)
        raw, words, info = run_task(ws, variant, texts[variant], take / "events.jsonl")
        if not raw:
            raise ValueError("沒有音訊資料")
        write_new(take / "raw.wav", raw)
        audio, duration, declared_duration = normalize_wav(raw)
        write_new(take / "audio.wav", audio)
        if not words:
            raise ValueError("沒有字詞時間戳")
        write_new(take / "words.json", json_bytes(words))
        receipt = {"variant": variant, "region": "ap-southeast-1",
                   "model": MODEL, "voice": VOICE,
                   "input_characters": len(texts[variant]),
                   "duration_seconds": duration, "word_count": len(words),
                   "stream_header_duration_seconds": declared_duration,
                   "raw_sha256": hashlib.sha256(raw).hexdigest(),
                   "audio_sha256": hashlib.sha256(audio).hexdigest(), **info}
        write_new(take / "receipt.json", json_bytes(receipt))
        return receipt
    except BaseException as error:
        status = getattr(error, "status_code", None)
        diagnostic = {"error_type": type(error).__name__,
                      "http_status": status}
        if isinstance(error, ValueError):
            diagnostic["message"] = str(error)
        write_new(take / "error.json", json_bytes(diagnostic))
        raise RuntimeError("新加坡 WebSocket 測試失敗；請看 error.json 與 events.jsonl，禁止重送") from None
    finally:
        if ws is not None:
            ws.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("variant", choices=("plain", "ssml"))
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--env-file", required=True, type=Path)
    args = parser.parse_args()
    receipt = run(args.variant, args.output_dir, args.env_file)
    print(json.dumps({key: receipt[key] for key in
        ("variant", "duration_seconds", "word_count", "usage", "input_characters")},
        ensure_ascii=False))


if __name__ == "__main__":
    main()

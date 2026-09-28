"""Two authorized Beijing CosyVoice calls for the SSML/Remotion timing probe.

The approved scripts live in the review HTML. Each variant may be attempted only
once; an interrupted request remains unknown and must not be resent.
"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
from html import unescape
import io
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.request
import wave
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "video/_audit/REVIEW-aliyun-ssml-sync-plan-2026-09-27.html"
ENDPOINT = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer"
MODEL = "cosyvoice-v3-plus"
VOICE = "longanyang"
LENGTHS = {"plain": 71, "ssml": 149}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_new(path: Path, raw: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def scripts() -> dict[str, str]:
    html = SOURCE.read_text(encoding="utf-8")
    blocks = [unescape(x) for x in re.findall(r"<pre>(.*?)</pre>", html, re.S)]
    if len(blocks) != 2:
        raise ValueError("測試計畫必須恰有兩段精確文稿")
    plain, ssml = blocks
    if len(plain) != LENGTHS["plain"] or len(ssml) != LENGTHS["ssml"]:
        raise ValueError("文稿字數與授權不符")
    root = ET.fromstring(ssml)
    if root.tag != "speak" or "".join(root.itertext()) != plain:
        raise ValueError("兩版可朗讀文字不一致")
    if [b.attrib for b in root.findall("break")] != [{"time": "400ms"}] * 3:
        raise ValueError("SSML 停頓與授權不符")
    return {"plain": plain, "ssml": ssml}


def key_from_local_env() -> str:
    env_path = ROOT / ".env"
    for raw in env_path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if line.startswith("DASHSCOPE_API_KEY_BEIJING="):
            key = line.split("=", 1)[1].strip().strip("\"'")
            if key:
                return key
    for raw in env_path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if line.startswith("DASHSCOPE_API_KEY="):
            key = line.split("=", 1)[1].strip().strip("\"'")
            if key:
                return key
    key = os.environ.get("DASHSCOPE_API_KEY_BEIJING") or os.environ.get("DASHSCOPE_API_KEY")
    if key:
        return key
    raise ValueError("本機找不到北京 DASHSCOPE_API_KEY")


def payload_for(variant: str, script: str) -> dict:
    return {"model": MODEL, "input": {"text": script, "voice": VOICE,
            "format": "wav", "sample_rate": 24000,
            "word_timestamp_enabled": True, "enable_ssml": variant == "ssml"}}


def parse_sse(raw: bytes) -> list[dict]:
    decoded = raw.decode("utf-8-sig")
    events = []
    for block in re.split(r"\r?\n\r?\n", decoded):
        data_lines = [line[5:].lstrip() for line in block.splitlines() if line.startswith("data:")]
        if not data_lines:
            continue
        value = "\n".join(data_lines)
        if value == "[DONE]":
            continue
        events.append(json.loads(value))
    if not events:
        raise ValueError("沒有 SSE JSON 事件")
    return events


def extract(events: list[dict]) -> tuple[bytes, list[dict], dict]:
    chunks, words = [], []
    final = None
    for item in events:
        output = item.get("output") or {}
        audio = output.get("audio") or {}
        chunk = audio.get("data")
        if chunk:
            chunks.append(base64.b64decode(chunk, validate=True))
        sentence = output.get("sentence") or {}
        for word in sentence.get("words") or []:
            words.append({"sentence_index": sentence.get("index"), **word})
        if output.get("finish_reason") == "stop":
            final = item
    if final is None:
        raise ValueError("串流沒有完成事件")
    if not chunks:
        raise ValueError("串流沒有音訊資料")
    audio = b"".join(chunks)
    with wave.open(io.BytesIO(audio), "rb") as wav:
        frames, rate = wav.getnframes(), wav.getframerate()
        if frames <= 0 or rate <= 0:
            raise ValueError("WAV 為空")
        if len(wav.readframes(frames)) != frames * wav.getnchannels() * wav.getsampwidth():
            raise ValueError("WAV 不完整")
        info = {"frames": frames, "sample_rate": rate,
                "duration_seconds": frames / rate}
    return audio, words, {**info, "usage": final.get("usage"),
                         "request_id": final.get("request_id"),
                         "audio_chunks": len(chunks), "sse_events": len(events)}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def run(variant: str, output_dir: Path) -> dict:
    all_scripts = scripts()
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "attempts.jsonl"
    attempts = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()] if log_path.exists() else []
    if len(attempts) >= 2 or any(item.get("variant") == variant for item in attempts):
        raise ValueError("已達兩次上限或此版本已送出；禁止重試")
    if variant == "ssml" and not (output_dir / "plain" / "receipt.json").is_file():
        raise ValueError("A 版未完成，暫停 B 版")
    key = key_from_local_env()
    payload = payload_for(variant, all_scripts[variant])
    raw_payload = json_bytes(payload)
    take_dir = output_dir / variant
    take_dir.mkdir(exist_ok=False)
    write_new(take_dir / "payload.json", raw_payload)
    event = {"variant": variant, "started_utc": datetime.now(timezone.utc).isoformat(),
             "payload_sha256": sha(raw_payload)}
    with log_path.open("ab") as stream:
        stream.write((json.dumps(event, ensure_ascii=False) + "\n").encode("utf-8"))
        stream.flush()
        os.fsync(stream.fileno())
    request = urllib.request.Request(ENDPOINT, data=raw_payload, method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "X-DashScope-SSE": "enable"})
    opener = urllib.request.build_opener(NoRedirect())
    try:
        try:
            with opener.open(request, timeout=180) as response:
                raw = response.read()
                status = response.status
        except urllib.error.HTTPError as error:
            raw = error.read()
            write_new(take_dir / "response_error.txt", raw)
            raise ValueError(f"HTTP {error.code}; 已保存錯誤回應，禁止補送") from None
        write_new(take_dir / "response.sse", raw)
        events = parse_sse(raw)
        audio, words, info = extract(events)
        write_new(take_dir / "raw.wav", audio)
        write_new(take_dir / "words.json", json_bytes(words))
        receipt = {"variant": variant, "model": MODEL, "voice": VOICE,
                   "region": "cn-beijing", "http_status": status,
                   "input_characters": len(all_scripts[variant]), **info,
                   "files": {"payload_sha256": sha(raw_payload),
                             "response_sha256": sha(raw), "wav_sha256": sha(audio)}}
        write_new(take_dir / "receipt.json", json_bytes(receipt))
        return receipt
    except BaseException:
        # A started event is deliberately terminal for this variant even on error.
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("variant", choices=("plain", "ssml"))
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.variant, args.output_dir)
    print(json.dumps({k: result[k] for k in ("variant", "duration_seconds", "audio_chunks",
          "sse_events", "usage", "input_characters")}, ensure_ascii=False))


if __name__ == "__main__":
    main()

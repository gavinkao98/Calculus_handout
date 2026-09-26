"""Q7 離線報量：完整 scene 為合成單位；本模組不執行 TTS。

Config (JSON or YAML): version: 1, pilot_id, language, scenes (3 ids),
glossary_revision, providers (3 entries). Each provider has id, model, voice,
voice_source, parameters, billing: {rule, unit_price, per_units, currency,
source, checked_on, note}. Rules: han_double, all_characters, free.
Missing voice/price produces a reviewable blocked plan, never a live request.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if (REPO_ROOT / ".deps").is_dir():
    sys.path.insert(0, str(REPO_ROOT / ".deps"))
import yaml

try:
    from . import narration
except ImportError:  # Direct CLI invocation.
    import narration


HARD_CAP = 9
# Unified ideographs, extensions, and compatibility ideographs (codepoints).
HAN = re.compile("[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\U00020000-\U0002ffff\U00030000-\U000323af]")
ENGLISH = re.compile(r"[A-Za-z]+(?:['’-][A-Za-z]+)*")


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def estimate_duration(text: str) -> dict:
    han, words = len(HAN.findall(text)), len(ENGLISH.findall(text))
    return {
        "han_characters": han, "english_words": words,
        "seconds_range": [round(han / 5 + words / 3, 2), round(han / 3 + words / 2, 2)],
        "calibrated": False, "status": "uncalibrated",
        "method": "Han 3–5 字／秒＋英文 2–3 詞／秒；未以既有音訊校準，標點停頓與數字未另建模；實際時長須量音檔。",
    }


def segment_from_scene(scene: dict) -> dict:
    scene_id, say = scene["id"], scene.get("say")
    if not isinstance(say, str) or not say.strip():
        raise ValueError(f"scene {scene_id}: 缺少非空 say")
    if narration.malformed_show_markers(say):
        raise ValueError(f"scene {scene_id}: 非法 show 標記")
    beats = narration.parse_say(say)
    # Use narration's single marker grammar; removing cues cannot add a TTS cut
    # or an artificial space inside a word. Whitespace alone is normalized.
    matches = list(narration._SHOW.finditer(say))
    text = " ".join(narration._SHOW.sub("", say).split())
    if not text:
        raise ValueError(f"scene {scene_id}: 去除標記後無文字")
    chunks, raw_start = [], 0
    for match in matches:
        chunks.append((raw_start, match.start()))
        raw_start = match.end()
    chunks.append((raw_start, len(say)))
    # parse_say drops only the empty opening chunk.
    if not " ".join(say[chunks[0][0]:chunks[0][1]].split()):
        chunks = chunks[1:]
    mapping, cursor, occurrences = [], 0, {}
    for beat, (raw_start, raw_end) in zip(beats, chunks, strict=True):
        start = text.find(beat.text, cursor) if beat.text else cursor
        if start < 0:
            raise ValueError(f"scene {scene_id}: 無法映射旁白文字")
        end = start + len(beat.text)
        base = f"{scene_id}.{beat.reveal or 'opening'}"
        occurrences[base] = occurrences.get(base, 0) + 1
        cue_id = base if occurrences[base] == 1 else f"{base}.{occurrences[base]}"
        mapping.append({"cue_id": cue_id, "scene_id": scene_id, "reveal": beat.reveal,
                        "text_span": [start, end], "source_say_span": [raw_start, raw_end],
                        "text": beat.text, "timing_status": "unresolved"})
        cursor = end
    return {"id": scene_id, "scene_id": scene_id, "text": text,
            "text_hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "scene_text_span": [0, len(text)], "source_say": say,
            "source": scene.get("source"), "cues": mapping,
            "characters": len(text), "nonwhitespace_characters": sum(not c.isspace() for c in text),
            "duration_estimate": estimate_duration(text)}


def _positive_number(value, *, zero=False):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and (value >= 0 if zero else value > 0))


def build_plan(storyboard: dict, config: dict, *, source_path: str = "") -> dict:
    if source_path:
        path = Path(source_path).resolve()
        source_path = path.relative_to(REPO_ROOT).as_posix() if path.is_relative_to(REPO_ROOT) else path.as_posix()
    if config.get("version") != 1:
        raise ValueError("config version 必須為 1")
    selected, providers = config.get("scenes"), config.get("providers")
    if not isinstance(selected, list) or len(selected) != 3 or any(not isinstance(x, str) for x in selected):
        raise ValueError("第一輪必須選取 3 個 scene id")
    if len(set(selected)) != len(selected):
        raise ValueError("config 重複 scene id")
    if not isinstance(providers, list) or len(providers) != 3:
        raise ValueError("第一輪必須設定 3 個 provider")
    scenes = storyboard.get("scenes", [])
    ids = [scene.get("id") for scene in scenes]
    if any(not isinstance(x, str) or not x for x in ids) or len(set(ids)) != len(ids):
        raise ValueError("storyboard scene id 缺漏或重複")
    by_id = {scene["id"]: scene for scene in scenes}
    unknown = set(selected) - set(by_id)
    if unknown:
        raise ValueError(f"未知 scene: {sorted(unknown)}")
    segments = [segment_from_scene(by_id[name]) for name in selected]
    requests, candidates, blockers, provider_ids = [], [], [], set()
    for provider in providers:
        provider_id = provider.get("id")
        if not isinstance(provider_id, str) or not provider_id or provider_id in provider_ids:
            raise ValueError("provider id 缺漏或重複")
        provider_ids.add(provider_id)
        model, voice = provider.get("model"), provider.get("voice")
        parameters = provider.get("parameters")
        if not isinstance(model, str) or not model:
            raise ValueError(f"{provider_id}: 缺少 model")
        if not isinstance(parameters, dict):
            raise ValueError(f"{provider_id}: parameters 必須為明確物件")
        if not isinstance(voice, str) or not voice.strip():
            blockers.append(f"{provider_id}: 尚未選定 voice")
        if not provider.get("voice_source"):
            blockers.append(f"{provider_id}: 缺少 voice 來源")
        billing = provider.get("billing") or {}
        rule = billing.get("rule")
        if rule not in ("han_double", "all_characters", "free"):
            raise ValueError(f"{provider_id}: 未知 billing rule")
        price_ok = (_positive_number(billing.get("unit_price"), zero=True)
                    and _positive_number(billing.get("per_units"))
                    and bool(billing.get("currency")))
        if not price_ok:
            blockers.append(f"{provider_id}: 價格／計價基數／幣別未齊")
        if rule == "free" and price_ok and billing["unit_price"] != 0:
            raise ValueError(f"{provider_id}: free 價格必須為 0")
        if not billing.get("source") or not billing.get("checked_on"):
            blockers.append(f"{provider_id}: 缺少公開價格來源／查價日期")
        total_units = 0
        for segment in segments:
            units = segment["characters"] + (segment["duration_estimate"]["han_characters"] if rule == "han_double" else 0)
            total_units += units
            payload = {"provider": provider_id, "model": model, "voice": voice,
                       "parameters": parameters, "text": segment["text"]}
            requests.append({"segment_id": segment["id"], "payload": payload,
                             "request_hash": digest(payload), "take_count": 1,
                             "billing_units": units,
                             "estimated_cost": round(units * billing["unit_price"] / billing["per_units"], 8) if price_ok else None,
                             "currency": billing.get("currency"), "status": "planned_only"})
        candidates.append({**provider, "request_count": 3, "billing_units": total_units,
                           "estimated_cost": round(total_units * billing["unit_price"] / billing["per_units"], 8) if price_ok else None})
    plan = {
        "version": 1, "pilot_id": config.get("pilot_id", "q7-tts-pilot"),
        "language": config.get("language", storyboard.get("meta", {}).get("language")),
        "mode": "offline_plan_only", "source_path": source_path,
        "source_snapshot_hash": digest(storyboard), "config_snapshot": config,
        "span_convention": "Python Unicode codepoint offsets [start,end); source_say_span refers to decoded YAML say; text_span refers to normalized request text",
        "normalization": "移除 show 標記並壓縮空白；保留所有標點；每個完整 scene 一次合成。",
        "segments": segments, "providers": candidates, "requests": requests,
        "summary": {"segment_count": 3, "provider_count": 3, "planned_requests": len(requests),
                    "hard_cap_requests": HARD_CAP, "takes_per_request": 1, "automatic_retry": False,
                    "reuse_count": 0, "take_registry": "not_implemented",
                    "reuse_note": "既有 MiMo beat 音檔不是本次完整語段的相同請求；本輪不宣稱命中，take registry 尚未建立。",
                    "characters_once": sum(s["characters"] for s in segments),
                    "seconds_range_once": [round(sum(s["duration_estimate"]["seconds_range"][i] for s in segments), 2) for i in range(2)],
                    "minutes_range_all_requests": [round(sum(s["duration_estimate"]["seconds_range"][i] for s in segments) * 3 / 60, 2) for i in range(2)],
                    "duration_calibrated": False},
        "approval": {"status": "pending", "approved_requests": 0},
        "script_lock": {"status": "pending", "nfa_status": "not_verified", "evidence": None},
        "blockers": ["本批外部呼叫尚未取得同意", "本次合成輸入的稿鎖與 NFA 尚未驗證", *blockers, *config.get("preflight_blockers", [])],
    }
    plan["plan_snapshot_hash"] = digest(plan)
    return plan


def render_html(plan: dict) -> str:
    def esc(value):
        return html.escape(str(value), quote=True)

    def pretty(value):
        return esc(json.dumps(value, ensure_ascii=False, indent=2))

    def source_link(value):
        label = esc(value or "待補")
        return f'<a href="{label}">{label}</a>' if isinstance(value, str) and re.match(r"https?://", value) else label

    summary = plan["summary"]
    parts = ['<!doctype html><html lang="zh-Hant"><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Q7 配音試驗・離線報量</title>',
             '<style>body{font:17px/1.7 system-ui,sans-serif;max-width:1080px;margin:40px auto;padding:0 24px;color:#243247;background:#faf9f6}h1,h2{line-height:1.3}section{margin:32px 0;padding:24px;background:white;border:1px solid #ddd;border-radius:12px;overflow-wrap:anywhere}table{width:100%;border-collapse:collapse}td,th{padding:10px;text-align:left;vertical-align:top;border-bottom:1px solid #ddd;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}.script{font-size:20px}.status{color:#8b4000}code{overflow-wrap:anywhere}</style>',
             '<h1>Q7 配音試驗・離線報量</h1>',
             f'<p>計畫：{esc(plan["pilot_id"])} ／ 語言：{esc(plan["language"])}</p>',
             '<p class="status">第一階段：報量準備。待確認稿件、音色與本批 API 同意。此工具只產生計畫，沒有 live 執行能力，也沒有合成音訊。</p>',
             f'<p>3 家 × 3 個完整語段 × 1 take＝{summary["planned_requests"]} 次；硬上限 {summary["hard_cap_requests"]} 次；不自動重試。voice 試音與重配另報批次。</p>',
             f'<p>文字共 {summary["characters_once"]} 字元；每家預估 {esc(summary["seconds_range_once"])} 秒。<strong>未校準</strong>：Han 3–5 字／秒＋英文 2–3 詞／秒，未另計標點停頓與數字。</p>',
             f'<p>9 次候選請求的合成音訊總量預估 {esc(summary["minutes_range_all_requests"])} 分鐘；不包含試音、重試或重配。</p>',
             f'<p>沿用 0 筆。{esc(summary["reuse_note"])}</p>',
             '<h2>目前阻擋項目</h2><ul>']
    parts.extend(f'<li>{esc(item)}</li>' for item in plan["blockers"])
    parts.append('</ul><h2>執行前說明</h2><ul>')
    parts.extend(f'<li>{esc(item)}</li>' for item in plan["config_snapshot"].get("preflight_notes", []))
    parts.append('</ul>')
    calibration = plan["config_snapshot"].get("calibration")
    if calibration:
        parts.append(f'<section><h2>既有音訊參考</h2><p>設定紀錄的 baseline 總長：{esc(calibration.get("measured_total_seconds"))} 秒；本計畫估計 {esc(summary["seconds_range_once"])} 秒。此工具未驗證音檔，亦未套用校準係數；估時計算仍為未校準。</p><details><summary>音訊參考證據</summary><pre>{pretty(calibration)}</pre></details></section>')
    parts.append('<h2>候選音色與公開報價</h2>')
    for provider in plan["providers"]:
        billing = provider["billing"]
        rule_label = {"han_double": "漢字每字 2，其餘（含空白與標點）每字 1；規則的證據與限制見下方說明", "all_characters": "所有字符（含空白與標點）每字 1", "free": "限時免費；仍列出文字用量"}[billing["rule"]]
        parts.append(f'<section><h3>{esc(provider["id"])} ／ {esc(provider["model"])}</h3><p>voice：{esc(provider.get("voice") or "待選定")}；來源：{source_link(provider.get("voice_source"))}</p><table><tbody><tr><th>公開單價</th><td>{esc(billing.get("unit_price"))} {esc(billing.get("currency"))} ／ {esc(billing.get("per_units"))} 計費單位</td></tr><tr><th>計字方式</th><td>{esc(rule_label)}</td></tr><tr><th>本批用量與估價</th><td>3 次請求，{provider["billing_units"]} 計費單位；估計 {esc(provider["estimated_cost"])} {esc(billing.get("currency"))}</td></tr><tr><th>價格來源／查價日期</th><td>{source_link(billing.get("source"))}<br>{esc(billing.get("checked_on"))}</td></tr></tbody></table><p>{esc(billing.get("note", ""))}</p><details><summary>完整合成參數與報價設定</summary><pre>{pretty(provider)}</pre></details></section>')
    parts.append('<h2>完整合成文字與畫面提示映射</h2>')
    for segment in plan["segments"]:
        parts.append(f'<section><h3>{esc(segment["id"])}</h3><p class="script">{esc(segment["text"])}</p><p>總字元 {segment["characters"]}；非空白 {segment["nonwhitespace_characters"]}；預估 {esc(segment["duration_estimate"]["seconds_range"])} 秒（未校準）。</p><p>文字 hash：<code>{esc(segment["text_hash"])}</code></p><table><thead><tr><th>cue ID／reveal</th><th>文字範圍 [start,end)</th><th>對應文字</th></tr></thead><tbody>')
        for cue in segment["cues"]:
            parts.append(f'<tr><td>{esc(cue["cue_id"])}<br>{esc(cue["reveal"])}</td><td>{esc(cue["text_span"])}</td><td>{esc(cue["text"])}</td></tr>')
        parts.append('</tbody></table><p>範圍依 Python Unicode codepoint；所有時間仍待定位，show 不是合成切點。</p></section>')
    parts.append(f'<h2>計畫快照</h2><p><code>{esc(plan["plan_snapshot_hash"])}</code></p><p>approval pending；script lock pending；NFA 未驗證。以下保留完整來源、參數、請求身分、價格與日期，供離線核對。</p><details><summary>完整計畫資料</summary><pre>{pretty(plan)}</pre></details></html>')
    return "\n".join(parts)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Q7 TTS 離線報量；不呼叫 API")
    for name in ("storyboard", "config", "output-json", "output-html"):
        parser.add_argument(f"--{name}", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        storyboard = yaml.safe_load(args.storyboard.read_text(encoding="utf-8-sig"))
        config = yaml.safe_load(args.config.read_text(encoding="utf-8-sig"))
        if not isinstance(storyboard, dict) or not isinstance(config, dict):
            raise ValueError("storyboard 與 config 必須為物件")
        plan = build_plan(storyboard, config, source_path=args.storyboard.as_posix())
        for path in (args.output_json, args.output_html):
            if path.resolve() in (args.storyboard.resolve(), args.config.resolve()):
                raise ValueError("輸出不可覆寫輸入檔")
        if args.output_json.resolve() == args.output_html.resolve():
            raise ValueError("JSON 與 HTML 輸出路徑不可相同")
        rendered = render_html(plan)
        for path in (args.output_json, args.output_html):
            path.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(plan, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        args.output_html.write_text(rendered, encoding="utf-8")
    except (ValueError, OSError, yaml.YAMLError) as error:
        parser.error(str(error))
    print(f"離線報量完成：{len(plan['requests'])} 次候選請求，上限 {HARD_CAP}；API 同意仍 pending。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

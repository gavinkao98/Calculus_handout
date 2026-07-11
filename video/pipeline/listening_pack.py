"""Offline listening pack: a per-take audio-QC HTML built from a manifest.

Reads a section's manifest.json and emits a standalone HTML (double-click to play)
that lists every scene's take -- spoken text, narration_mode, WPM, validation
status/warnings/qa, fallback_history, and measured LUFS/true-peak -- sorted
risk-first so the takes most worth a careful listen float to the top.

STRICTLY read-only w.r.t. audio: it never re-synthesizes and never triggers a
retry (respects the standing "don't re-run scene-level" decisions for §3.1's
fallback beats). It only READS existing WAVs (ffmpeg ebur128 analysis) and writes
one HTML file. This is a QC aid -- the release gate still requires listening to
the whole film once (REVIEW_GATES convention)."""
from __future__ import annotations

import html
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

WPM_MUST_LISTEN = 175   # a take above this reads fast enough to flag for a listen

_RANK_LABEL = {1: "FAIL", 2: "terminal-beat fallback", 3: "warnings",
               4: "qa 未跑 (skipped/error/legacy)", 5: f"WPM > {WPM_MUST_LISTEN}", 6: "clean"}


def _wpm(script: str, audio_seconds: float) -> float:
    if not script or not audio_seconds or audio_seconds <= 0:   # guard div-by-zero / silent
        return 0.0
    return len(script.split()) / audio_seconds * 60.0


def _qa_state(validation: dict) -> str:
    """ran|skipped|error|legacy-missing. 'qa' key absent (pre-T4 manifest) or null
    -> legacy-missing (Adv4: not the same risk class as this-run skipped/error)."""
    if "qa" not in validation:
        return "legacy-missing"
    qa = validation.get("qa")
    if not isinstance(qa, dict):
        return "legacy-missing"
    return str(qa.get("status", "legacy-missing"))


def _risk_rank(*, mode, status, warnings, qa_state, wpm, fallback_history) -> int:
    """Lowest-numbered (= highest-priority) category the take falls into (NA3 order)."""
    if mode == "silent":
        return 6                                    # nothing to listen to
    if status == "fail":
        return 1
    if mode == "beats" and fallback_history:
        return 2                                    # FA gave up -> most worth hearing
    if warnings:
        return 3
    if qa_state != "ran":
        return 4
    if wpm > WPM_MUST_LISTEN:
        return 5
    return 6


def rows_from_manifest(manifest: dict) -> list[dict]:
    """Pure: per-scene QC rows, sorted risk-first (then scene_id). No I/O."""
    rows: list[dict] = []
    for s in manifest.get("scenes", []):
        mode = s.get("narration_mode")
        validation = s.get("validation") or {}
        status = validation.get("status")
        warnings = validation.get("warnings") or []
        qa_state = _qa_state(validation)
        script = s.get("script") or ""
        audio_seconds = s.get("audio_seconds") or 0.0
        wpm = _wpm(script, audio_seconds)
        fh = s.get("fallback_history") or []
        rows.append({
            "scene_id": s.get("scene_id"), "narration_mode": mode, "script": script,
            "audio_file": s.get("audio_file"), "audio_seconds": audio_seconds,
            "wpm": round(wpm, 1), "status": status, "warnings": warnings,
            "qa_state": qa_state, "fallback_history": fh,
            "risk_rank": _risk_rank(mode=mode, status=status, warnings=warnings,
                                    qa_state=qa_state, wpm=wpm, fallback_history=fh),
        })
    rows.sort(key=lambda r: (r["risk_rank"], r["scene_id"] or ""))
    return rows


def measure_loudness(wav: Path) -> dict:
    """{'I': LUFS, 'TP': dBFS} via ffmpeg ebur128; {'error': ...} if ffmpeg is absent,
    the file is missing, or the summary can't be parsed -- never raises, so a missing
    tool degrades the pack (LUFS column shows the error) instead of breaking it."""
    wav = Path(wav)
    if not wav.exists():
        return {"error": f"missing wav: {wav.name}"}
    try:
        proc = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", str(wav),
             "-af", "ebur128=peak=true", "-f", "null", "-"],
            capture_output=True, text=True, timeout=120)
    except (FileNotFoundError, OSError, subprocess.SubprocessError) as exc:
        return {"error": f"ffmpeg unavailable: {exc}"}
    summary = (proc.stderr or "").rsplit("Summary:", 1)[-1]   # the integrated block is last
    m_i = re.search(r"\bI:\s*(-?\d+(?:\.\d+)?)\s*LUFS", summary)
    m_tp = re.search(r"\bPeak:\s*(-?\d+(?:\.\d+)?)\s*dBFS", summary)
    out: dict[str, Any] = {}
    if m_i:
        out["I"] = float(m_i.group(1))
    if m_tp:
        out["TP"] = float(m_tp.group(1))
    return out or {"error": "could not parse ebur128 summary"}


def _loudness_cell(loud: dict | None) -> str:
    if not loud:
        return "&mdash;"
    if "error" in loud:
        return f'<span class="dim">{html.escape(str(loud["error"]))}</span>'
    parts = []
    if "I" in loud:
        parts.append(f'{loud["I"]:.1f} LUFS')
    if "TP" in loud:
        parts.append(f'{loud["TP"]:.1f} dBTP')
    return html.escape(" · ".join(parts)) or "&mdash;"


def render_html(rows: list[dict], deck: str, out_dir: Path) -> str:
    """Standalone HTML (framing 繁中; escaped user text; <audio> src relative to out_dir)."""
    out_dir = Path(out_dir)
    trs = []
    for r in rows:
        af = r.get("audio_file")
        if af:
            src = os.path.relpath(af, out_dir).replace(os.sep, "/")
            audio = f'<audio controls preload="none" src="{html.escape(src)}"></audio>'
        else:
            audio = '<span class="dim">（無旁白音檔）</span>'
        warn = "<br>".join(html.escape(str(w)) for w in r["warnings"]) or "&mdash;"
        fb = html.escape(", ".join(str((h or {}).get("rung", h)) for h in r["fallback_history"])) or "&mdash;"
        trs.append(
            f'<tr class="rank{r["risk_rank"]}">'
            f'<td class="rk">{r["risk_rank"]}<span class="dim"> {html.escape(_RANK_LABEL[r["risk_rank"]])}</span></td>'
            f'<td>{html.escape(str(r["scene_id"]))}</td>'
            f'<td>{html.escape(str(r["narration_mode"]))}</td>'
            f'<td class="num">{r["wpm"]:.0f}</td>'
            f'<td>{html.escape(str(r["status"]))}</td>'
            f'<td>{html.escape(r["qa_state"])}</td>'
            f'<td class="warn">{warn}</td>'
            f'<td>{fb}</td>'
            f'<td>{_loudness_cell(r.get("loudness"))}</td>'
            f'<td class="audio">{audio}</td>'
            f'<td class="script">{html.escape(r["script"])}</td>'
            f'</tr>')
    rows_html = "\n".join(trs)
    return f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<title>Listening pack — {html.escape(deck)}</title>
<style>
 body{{font-family:system-ui,"Noto Sans TC",sans-serif;margin:1.2rem;color:#111;background:#fafafa}}
 h1{{font-size:1.2rem}} .lead{{color:#444;max-width:60rem}}
 table{{border-collapse:collapse;width:100%;font-size:.82rem;margin-top:1rem}}
 th,td{{border:1px solid #ddd;padding:.35rem .5rem;vertical-align:top;text-align:left}}
 th{{background:#f0f0f0;position:sticky;top:0}}
 td.num,td.rk{{white-space:nowrap}} .dim{{color:#999;font-size:.75rem}}
 td.script{{max-width:24rem;color:#333}} td.warn{{color:#b00;max-width:14rem}}
 audio{{height:1.8rem}}
 tr.rank1 td.rk{{color:#b00;font-weight:700}} tr.rank2 td.rk{{color:#c60;font-weight:700}}
 tr.rank3 td.rk{{color:#a80}}
</style></head><body>
<h1>Listening pack — {html.escape(deck)}（{len(rows)} 場）</h1>
<p class="lead">逐場聽感驗收表，依風險排序（1＝最該聽）。本 pack 為驗收輔助、<b>唯讀</b>：不重新合成、不觸發任何重試；
正式交付前仍應完整聽一次全片（REVIEW_GATES 慣例）。風險級：1 FAIL／2 terminal-beat fallback／3 warnings／
4 qa 未跑（skipped/error/legacy）／5 WPM&gt;{WPM_MUST_LISTEN}／6 clean。</p>
<table><thead><tr>
<th>風險</th><th>scene_id</th><th>mode</th><th>WPM</th><th>status</th><th>qa</th>
<th>warnings</th><th>fallback</th><th>LUFS / TP</th><th>試聽</th><th>spoken</th>
</tr></thead><tbody>
{rows_html}
</tbody></table></body></html>
"""


def write_listening_pack(manifest_path: Path, out_html: Path | None = None) -> Path:
    """Read manifest -> measure loudness of each existing take -> write the HTML.
    out_html defaults to REVIEW-<deck>-listening.html beside the manifest."""
    manifest_path = Path(manifest_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    deck = manifest.get("deck_id") or manifest_path.parent.name
    out_html = Path(out_html) if out_html else manifest_path.parent / f"REVIEW-{deck}-listening.html"
    rows = rows_from_manifest(manifest)
    for r in rows:
        if r["audio_file"]:
            r["loudness"] = measure_loudness(Path(r["audio_file"]))
    out_html.write_text(render_html(rows, deck, out_html.parent), encoding="utf-8")
    return out_html


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Offline per-take listening pack (HTML) from a manifest.")
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=None, help="HTML path (default: beside manifest)")
    args = ap.parse_args(argv)
    out = write_listening_pack(args.manifest, args.out)
    print(f"[listening_pack] wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

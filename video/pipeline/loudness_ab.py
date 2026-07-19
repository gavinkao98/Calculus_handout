"""Loudness A/B: normalize one sample take to several integrated-loudness targets via
ffmpeg two-pass loudnorm, so the house loudness target can be chosen by ear before it is
baked into make.py's compose (T10-3, post-adjudication).

Read-only w.r.t. the source WAV: it writes NEW normalized copies (to a scratch/output
dir) + one HTML A/B; it never touches the source. Two-pass loudnorm (measure, then apply
the measured values with linear=true) is the accurate, non-dynamic path -- the same one
T10-3 will wire into _concat -- not a one-pass dynamic normalize."""
from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

# Run-as-script bootstrap: put video/ on sys.path so `from pipeline.listening_pack ...`
# resolves when invoked directly (python video/pipeline/loudness_ab.py), not only when
# imported by a test that already inserted it (that gap made the CLI ModuleNotFoundError).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

TARGETS = (-19.0, -17.0, -15.5)   # candidate integrated-loudness targets (LUFS)
TRUE_PEAK = -1.5                    # dBTP ceiling (loudnorm never exceeds this)


def _parse_loudnorm_json(stderr: str) -> dict:
    """The measured block from a loudnorm `print_format=json` first pass
    (input_i/input_tp/input_lra/input_thresh/target_offset). Robust to the log noise
    that brackets the JSON; {} if not found / unparseable."""
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", stderr or "", re.DOTALL)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except ValueError:
        return {}


def measure_i_tp(wav: Path) -> dict:
    """{'I', 'TP'} via ebur128 (reuses listening_pack's measurement); {'error':...} safe."""
    from pipeline.listening_pack import measure_loudness
    return measure_loudness(Path(wav))


def loudnorm_2pass(in_wav: Path, out_wav: Path, target_i: float,
                   target_tp: float = TRUE_PEAK) -> dict:
    """Two-pass loudnorm to target_i LUFS / target_tp dBTP; returns the OUTPUT's actually
    measured {'I','TP'} (or {'error':...}). ffmpeg absent / bad input never raises."""
    in_wav, out_wav = Path(in_wav), Path(out_wav)
    if not in_wav.exists():
        return {"error": f"missing {in_wav.name}"}
    try:
        p1 = subprocess.run(
            ["ffmpeg", "-hide_banner", "-i", str(in_wav),
             "-af", f"loudnorm=I={target_i}:TP={target_tp}:print_format=json", "-f", "null", "-"],
            capture_output=True, text=True, timeout=300)
    except (FileNotFoundError, OSError, subprocess.SubprocessError) as exc:
        return {"error": f"ffmpeg unavailable: {exc}"}
    meas = _parse_loudnorm_json(p1.stderr or "")
    if not all(k in meas for k in ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset")):
        return {"error": "loudnorm pass-1 measurement failed"}
    af = (f"loudnorm=I={target_i}:TP={target_tp}:linear=true:"
          f"measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
          f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:"
          f"offset={meas['target_offset']}")
    try:
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-i", str(in_wav),
                        "-af", af, "-ar", "48000", "-ac", "2", str(out_wav)],
                       capture_output=True, text=True, timeout=300, check=True)
    except (subprocess.SubprocessError, OSError) as exc:
        return {"error": f"loudnorm pass-2 failed: {exc}"}
    return measure_i_tp(out_wav)


def _version_html(label: str, loud: dict, wav_relpath: str) -> str:
    if "error" in loud:
        meas = f'<span class="dim">{html.escape(str(loud["error"]))}</span>'
    else:
        i = f'{loud["I"]:.1f} LUFS' if "I" in loud else "?"
        tp = f'{loud["TP"]:.1f} dBTP' if "TP" in loud else "?"
        meas = html.escape(f"{i} · {tp}")
    src = html.escape(wav_relpath)
    return (f'<div class="col"><h3>{html.escape(label)}</h3>'
            f'<audio controls preload="none" src="{src}"></audio>'
            f'<p class="dim">實測：{meas}</p>'
            f'<p class="sha">{html.escape(os.path.basename(wav_relpath))}</p></div>')


def build_ab(sample_wav: Path, out_dir: Path, deck: str,
             targets: tuple[float, ...] = TARGETS, html_dir: Path | None = None) -> Path:
    """Normalize `sample_wav` to each target into out_dir; write an HTML A/B into
    html_dir (default out_dir). Returns the HTML path. WAVs are named <deck>_<target>.wav."""
    sample_wav, out_dir = Path(sample_wav), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    html_dir = Path(html_dir) if html_dir else out_dir
    html_dir.mkdir(parents=True, exist_ok=True)
    cols = []
    for t in targets:
        tag = f"{t:g}".replace("-", "m").replace(".", "_")
        out_wav = out_dir / f"{deck}_LUFS_{tag}.wav"
        loud = loudnorm_2pass(sample_wav, out_wav, t)
        rel = os.path.relpath(out_wav, html_dir).replace(os.sep, "/")
        cols.append(_version_html(f"target {t:g} LUFS", loud, rel))
    src_meas = measure_i_tp(sample_wav)
    src_i = f'{src_meas["I"]:.1f} LUFS' if "I" in src_meas else "?"
    doc = f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<title>Loudness A/B — {html.escape(deck)}</title>
<style>
 body{{font-family:system-ui,"Noto Sans TC",sans-serif;margin:1.5rem;max-width:64rem;color:#111;line-height:1.55}}
 h1{{font-size:1.3rem}} .banner{{background:#fff3cd;border:1px solid #e0c060;padding:.6rem .9rem;border-radius:6px;font-weight:600}}
 .grid{{display:flex;gap:1rem;flex-wrap:wrap;margin-top:1rem}}
 .col{{flex:1;min-width:15rem;border:1px solid #ddd;border-radius:8px;padding:.8rem}}
 .col h3{{margin:.2rem 0 .5rem}} audio{{width:100%}}
 code{{background:#f0f0f0;padding:.1rem .3rem;border-radius:3px;font-size:.85em}}
 .dim{{color:#777;font-size:.85rem}} .sha{{color:#999;font-size:.72rem}}
</style></head><body>
<h1>Loudness A/B — {html.escape(deck)}</h1>
<p class="banner">狀態：<b>awaiting adjudication</b>（等使用者裁決）。裁決後由執行者把選定 target 以 two-pass
loudnorm（I／TP）接進 <code>make.py</code> <code>_concat</code>（T10-3），並在 <code>compose()</code> 尾端印整片
I／TP 報告、超容差印 WARN。</p>
<p>樣本＝<code>{html.escape(sample_wav.name)}</code>（§3.1 代表性場，實測 {html.escape(src_i)}）。三版皆
<b>two-pass loudnorm</b>（先量測、再以 measured 值 <code>linear=true</code> 套用，非 one-pass dynamic），
true-peak 上限 <b>{TRUE_PEAK} dBTP</b>。<b>脈絡：</b>YouTube 參考位準約 <b>-14 LUFS</b>，且平台只會把過響的內容
<b>往下 normalize</b>（不會把安靜的內容拉響）——故 target 訂在 -14 以下較安全、避免被平台再壓一次。</p>
<div class="grid">
{''.join(cols)}
</div>
<h2>取捨</h2>
<ul>
 <li><b>-19 LUFS</b>：最保守、動態最寬；教學乾聲清楚，但整體偏小聲，觀眾可能需調大音量。</li>
 <li><b>-17 LUFS</b>：折衷；比 -19 響、仍在 YouTube 上傳不被大幅壓的區間。</li>
 <li><b>-15.5 LUFS</b>：最接近平台常見響度、開箱即聽感足；動態略窄，接近 -14 上限。</li>
</ul>
<p class="dim">WAV 在 gitignored 的 output/scratch；本說明 HTML 在 tracked 的 <code>video/_audit/</code>。</p>
</body></html>
"""
    out_html = html_dir / f"REVIEW-{deck}-loudness-ab.html"
    out_html.write_text(doc, encoding="utf-8")
    return out_html


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Loudness A/B (two-pass loudnorm) from a sample WAV.")
    ap.add_argument("--sample", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True, help="where the normalized WAVs go")
    ap.add_argument("--html-dir", type=Path, default=None, help="where the HTML goes (default: out-dir)")
    ap.add_argument("--deck", default="sample")
    args = ap.parse_args(argv)
    out = build_ab(args.sample, args.out_dir, args.deck, html_dir=args.html_dir)
    print(f"[loudness_ab] wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

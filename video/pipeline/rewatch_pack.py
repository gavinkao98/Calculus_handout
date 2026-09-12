"""rewatch_pack.py -- turn a rendered deck into something a reviewer who cannot PLAY video
can still "watch": per-scene contact sheets (sampled frames, each labelled with the time
and the words being spoken at that instant), a per-scene transcript timeline, and motion
statistics (how much of the scene the picture actually changes).

Why: the visual gate audits one "fullest" frame per scene and the pedagogy gate audits
the storyboard, so nothing in the pipeline sees the film as a viewer does -- time, dwell,
whether anything moves (pipeline assessment 2026-09-07, F7-F9). A model reviewer reads
images and text but not video; this pack is the bridge, and it is the shared input of the
multi-lens rewatch review so every lens looks at exactly the same evidence.

    python video/pipeline/rewatch_pack.py --deck ch03_trig_derivatives_mimo
    python video/pipeline/rewatch_pack.py --deck <deck> --scene sector_inequality,recap

Reads (all local, no API): storyboards/<deck>.yml (+ the base canonical deck for the
written-math form of each beat), the audio manifest (audio_mimo/ or audio/) for beat
timings + forced-alignment word timings, and output/_av/<deck>/<scene>.mp4 -- the per-scene
A/V files compose concatenated, so their durations give exact global scene starts.

Writes output/ch<NN>/s<X.Y>/rewatch_pack/ (gitignored, regenerable):
    INDEX.md            viewer-facing table of all scenes (times, reveals, motion) + how to read
    PRODUCTION.md       template / hook / narration_mode per scene (for NON-blind lenses only)
    pack.json           everything machine-readable (for the orchestrator / report generator)
    NN_<scene>.sheet.jpg contact sheet: 2 columns of 960x540 tiles, label = time + spoken words
    NN_<scene>.md       transcript timeline (beats, reveal times, words/sec) + motion stats
    NN_<scene>/f_XX_+<t>s.jpg   the sampled frames at full 1920x1080 for close reading

Timing model (video/pipeline/scene.py + timing.py): a content scene is SCENE_LEAD_SECONDS of
still, then one hold per beat (= that beat's audio length; the reveal animation plays at the
beat's start), then SCENE_TAIL_SECONDS. So a reveal lands at LEAD + beat.start_seconds; frames
are sampled just after each reveal (post fade-in) and at the midpoint of long beats.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pipeline import _bootstrap  # noqa: E402
from pipeline.timing import SCENE_LEAD_SECONDS  # noqa: E402

_bootstrap.bootstrap()
import numpy as np  # noqa: E402
import yaml  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

REPO = _bootstrap.REPO_ROOT
TILE_W, TILE_H, LABEL_H, COLS, PAD = 960, 540, 44, 2, 12
MAX_TILES = 12
POST_REVEAL = 0.7          # seconds after a reveal (past the 0.45-0.8 s fade-in) to sample
LONG_BEAT = 8.0            # beats longer than this also get a midpoint sample
MOTION_FPS = 4
CHANGE_FRAC = 0.002        # >0.2 % of pixels changed (|d|>12/255) => the picture moved
_SHOW = re.compile(r"\{show[^}]*\}")


def _run(cmd: list[str]) -> bytes:
    return subprocess.run(cmd, check=True, capture_output=True).stdout


def ffprobe_duration(p: Path) -> float:
    out = _run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)])
    return float(out.decode().strip())


def fmt(t: float) -> str:
    m, s = divmod(max(t, 0.0), 60)
    return f"{int(m)}:{s:04.1f}"


# ---- words at time -----------------------------------------------------------------

def load_words(entry: dict, audio_dir: Path) -> "list[dict] | None":
    """Forced-alignment words [{word,start,end}] for a scene_aligned scene, else None."""
    wf = (entry.get("alignment") or {}).get("words_file")
    if not wf:
        return None
    cand = [Path(wf), audio_dir / "align" / Path(wf).name]    # absolute (this machine) or relative
    for p in cand:
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            return data.get("words") if isinstance(data, dict) else data
    return None


def words_at(t_video: float, beats: list[dict], words: "list[dict] | None") -> tuple[str, int]:
    """(snippet with the current word in [brackets], beat index 1-based or 0) at video time t.
    scene_aligned: exact from FA words; beats mode: linear interpolation inside the beat (~)."""
    ta = t_video - SCENE_LEAD_SECONDS
    if ta < 0 or not beats:
        return ("(before narration starts)" if beats else "(silent scene)", 0)
    bi = 0
    for b in beats:
        if b["start_seconds"] - 1e-6 <= ta:
            bi = b["index"]
    b = next((x for x in beats if x["index"] == bi), None)
    if b is None:
        return ("(before narration starts)", 0)
    if ta > beats[-1]["end_seconds"] + 0.05:
        return ("(narration finished; tail)", bi)
    if words:
        idx = max((i for i, w in enumerate(words) if w["start"] <= ta), default=-1)
        if idx < 0:
            return ("(before first word)", bi)
        lo, hi = max(0, idx - 6), min(len(words), idx + 7)
        toks = [("[" + w["word"] + "]") if i == idx else w["word"] for i, w in enumerate(words[lo:hi], lo)]
        return (" ".join(toks), bi)
    toks = b["text"].split()
    span = max(b["end_seconds"] - b["start_seconds"], 1e-6)
    idx = min(len(toks) - 1, int((ta - b["start_seconds"]) / span * len(toks)))
    lo, hi = max(0, idx - 6), min(len(toks), idx + 7)
    toks2 = [("[" + w + "]") if i == idx else w for i, w in enumerate(toks[lo:hi], lo)]
    return ("~ " + " ".join(toks2), bi)


# ---- motion -------------------------------------------------------------------------

def motion_stats(av: Path, duration: float, reveal_times: list[float]) -> dict:
    """Decode at MOTION_FPS in 192x108 grey and measure frame-to-frame change."""
    raw = _run(["ffmpeg", "-v", "error", "-i", str(av), "-an", "-vf",
                f"fps={MOTION_FPS},scale=192:108,format=gray", "-f", "rawvideo", "-"])
    n = len(raw) // (192 * 108)
    frames = np.frombuffer(raw[: n * 192 * 108], dtype=np.uint8).reshape(n, 108, 192).astype(np.int16)
    if n < 2:
        return {"static_ratio": 1.0, "moving_seconds": 0.0, "longest_still_seconds": duration,
                "events": [], "non_reveal_events": [], "profile": ""}
    d = np.abs(frames[1:] - frames[:-1])
    frac = (d > 12).mean(axis=(1, 2))                      # fraction of pixels that changed
    moving = frac > CHANGE_FRAC
    dt = 1.0 / MOTION_FPS
    # runs of stillness
    longest = run = 0
    for m in moving:
        run = 0 if m else run + 1
        longest = max(longest, run)
    # change events = starts of moving runs
    events = [round((i + 1) * dt, 2) for i in range(len(moving)) if moving[i] and (i == 0 or not moving[i - 1])]
    # a reveal's fade-in registers at the sample just BEFORE its nominal time (1/MOTION_FPS
    # quantisation), so allow -0.3 s of slack or every reveal shows up as a phantom event
    non_reveal = [t for t in events if not any(-0.3 <= t - r <= 1.5 for r in reveal_times)
                  and t > SCENE_LEAD_SECONDS * 0.5 and t < duration - 0.8]
    # coarse profile: one level (0-8) per 2 s window = max change fraction in the window (log scale)
    glyphs = " ▁▂▃▄▅▆▇█"
    win = int(2 * MOTION_FPS)
    levels = []
    for i in range(0, len(frac), win):
        f = float(frac[i:i + win].max()) if len(frac[i:i + win]) else 0.0
        levels.append(0 if f <= CHANGE_FRAC else min(8, 1 + int(np.log10(f / CHANGE_FRAC) * 3)))
    return {
        "static_ratio": round(float(1 - moving.mean()), 3),
        "moving_seconds": round(float(moving.sum() * dt), 1),
        "longest_still_seconds": round(longest * dt, 1),
        "events": events,
        "non_reveal_events": [round(t, 1) for t in non_reveal],
        "profile": "".join(glyphs[l] for l in levels),   # text form (markdown); the sheet draws bars
        "levels": levels,
    }


# ---- sampling + sheet -----------------------------------------------------------------

def sample_times(duration: float, beats: list[dict]) -> list[tuple[float, str]]:
    """(t_video, why) samples: start, post-reveal per beat, midpoints of long beats, end."""
    out: list[tuple[float, str]] = [(min(0.5, duration / 2), "start")]
    if beats:
        for b in beats:
            r = SCENE_LEAD_SECONDS + b["start_seconds"]
            out.append((r + POST_REVEAL, f"beat {b['index']} reveal -> {b['reveal']}" if b.get("reveal")
                        else f"beat {b['index']} start (no reveal)"))
            if b["end_seconds"] - b["start_seconds"] > LONG_BEAT:
                out.append((SCENE_LEAD_SECONDS + (b["start_seconds"] + b["end_seconds"]) / 2, f"beat {b['index']} mid"))
    else:
        k = 5
        out += [(duration * (i + 1) / (k + 1), f"{i + 1}/{k}") for i in range(k)]
    out.append((max(duration - 0.6, 0.3), "end (fullest)"))
    out = [(min(max(t, 0.2), duration - 0.2), why) for t, why in out]
    out.sort()
    while len(out) > MAX_TILES:                      # drop midpoints first, then thin evenly
        mids = [i for i, (_, why) in enumerate(out) if why.endswith(" mid")]
        if mids:
            out.pop(mids[len(mids) // 2])
        else:
            out.pop(len(out) // 2)
    return out


def extract_frame(av: Path, t: float, dst: Path) -> None:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(av),
                    "-frames:v", "1", "-q:v", "2", str(dst)], check=True, capture_output=True)


def _font(size: int) -> ImageFont.ImageFont:
    for name in ("arial.ttf", "DejaVuSans.ttf", "consola.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _fit(draw: ImageDraw.ImageDraw, text: str, font, max_w: int) -> str:
    if draw.textlength(text, font=font) <= max_w:
        return text
    while text and draw.textlength(text + "…", font=font) > max_w:
        text = text[:-1]
    return text + "…"


def build_sheet(frames: list[tuple[Path, str]], header: list[str], dst: Path, levels: list[int]) -> None:
    rows = (len(frames) + COLS - 1) // COLS
    head_h = 26 * len(header) + 16
    W = PAD + COLS * (TILE_W + PAD)
    H = head_h + PAD + rows * (LABEL_H + TILE_H + PAD)
    sheet = Image.new("RGB", (W, H), (14, 18, 28))
    draw = ImageDraw.Draw(sheet)
    f_head, f_lab = _font(22), _font(19)
    # motion profile as a small bar chart at the right of the header (one bar per 2 s; arial has no block glyphs)
    bw, bg, bh = 6, 2, 40
    x0 = W - PAD - len(levels) * (bw + bg)
    draw.rectangle([x0 - 4, 6, W - PAD + 2, 6 + bh + 6], outline=(70, 84, 110))
    for i, lvl in enumerate(levels):
        h = max(2, int(bh * lvl / 8))
        draw.rectangle([x0 + i * (bw + bg), 6 + bh + 3 - h, x0 + i * (bw + bg) + bw, 6 + bh + 3],
                       fill=(255, 200, 90) if lvl else (52, 62, 84))
    for i, line in enumerate(header):
        draw.text((PAD, 8 + 26 * i), _fit(draw, line, f_head, x0 - 16 - PAD), fill=(230, 236, 245), font=f_head)
    for k, (path, label) in enumerate(frames):
        r, c = divmod(k, COLS)
        x = PAD + c * (TILE_W + PAD)
        y = head_h + PAD + r * (LABEL_H + TILE_H + PAD)
        draw.rectangle([x, y, x + TILE_W, y + LABEL_H], fill=(34, 44, 66))
        draw.text((x + 8, y + 11), _fit(draw, label, f_lab, TILE_W - 16), fill=(255, 226, 150), font=f_lab)
        img = Image.open(path).convert("RGB").resize((TILE_W, TILE_H), Image.LANCZOS)
        sheet.paste(img, (x, y + LABEL_H))
    sheet.save(dst, "JPEG", quality=88, optimize=True)


# ---- main ------------------------------------------------------------------------------

def load_manifest(section_dir: Path) -> tuple[dict, Path]:
    for sub in ("audio_mimo", "audio"):
        p = section_dir / sub / "manifest.json"
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8")), section_dir / sub
    raise SystemExit(f"[rewatch_pack] no manifest under {section_dir}/audio_mimo or audio/")


def canonical_beats(base_scene: "dict | None") -> list[str]:
    """Written (LaTeX) beat texts from the canonical deck's `say`, split at {show} markers."""
    if not base_scene or not isinstance(base_scene.get("say"), str):
        return []
    parts = _SHOW.split(base_scene["say"])
    return [re.sub(r"\s+", " ", p).strip() for p in parts if p.strip()]


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--deck", required=True, help="rendered deck id, e.g. ch03_trig_derivatives_mimo")
    ap.add_argument("--scene", default="all", help="comma-separated scene ids (default all)")
    ap.add_argument("--out", type=Path, default=None, help="pack dir (default <section>/rewatch_pack)")
    args = ap.parse_args()

    sb = yaml.safe_load((REPO / "video" / "storyboards" / f"{args.deck}.yml").read_text(encoding="utf-8"))
    meta = sb["meta"]
    base_id = args.deck[:-5] if args.deck.endswith("_mimo") else args.deck
    base_path = REPO / "video" / "storyboards" / f"{base_id}.yml"
    base = yaml.safe_load(base_path.read_text(encoding="utf-8")) if base_path.exists() and base_id != args.deck else None
    base_by_id = {s["id"]: s for s in (base or {}).get("scenes", [])}

    section_dir = _bootstrap.section_output_dir(meta)
    manifest, audio_dir = load_manifest(section_dir)
    by_id = {e["scene_id"]: e for e in manifest["scenes"]}
    av_dir = REPO / "video" / "output" / "_av" / args.deck
    out = args.out or (section_dir / "rewatch_pack")
    out.mkdir(parents=True, exist_ok=True)

    scenes = sb["scenes"]
    wanted = None if args.scene == "all" else set(args.scene.split(","))

    # exact global timeline from the concatenated per-scene files
    durs: dict[str, float] = {}
    for s in scenes:
        av = av_dir / f"{s['id']}.mp4"
        if not av.exists():
            raise SystemExit(f"[rewatch_pack] missing per-scene A/V file {av} (render the deck first)")
        durs[s["id"]] = ffprobe_duration(av)
    starts: dict[str, float] = {}
    t = 0.0
    for s in scenes:
        starts[s["id"]] = t
        t += durs[s["id"]]
    total = t

    records = []
    for n, s in enumerate(scenes, 1):
        sid = s["id"]
        if wanted and sid not in wanted:
            continue
        entry = by_id.get(sid, {})
        mode = entry.get("narration_mode", "silent")
        beats = [b for b in entry.get("beats", []) if "start_seconds" in b] if mode in ("beats", "scene_aligned") else []
        words = load_words(entry, audio_dir) if mode == "scene_aligned" else None
        dur, g0 = durs[sid], starts[sid]
        av = av_dir / f"{sid}.mp4"
        stem = f"{n:02d}_{sid}"
        title = s.get("title") or sid
        reveal_times = [SCENE_LEAD_SECONDS + b["start_seconds"] for b in beats if b.get("reveal")]
        print(f"[rewatch_pack] {stem}  {fmt(g0)}–{fmt(g0 + dur)}  ({dur:.1f}s, {mode}, {len(beats)} beats)", flush=True)

        # frames
        fdir = out / stem
        fdir.mkdir(exist_ok=True)
        samples = sample_times(dur, beats)
        frames: list[tuple[Path, str]] = []
        sample_rows = []
        for k, (tv, why) in enumerate(samples, 1):
            dst = fdir / f"f_{k:02d}_+{tv:05.1f}s.jpg"
            if not dst.exists():
                extract_frame(av, tv, dst)
            snippet, bi = words_at(tv, beats, words)
            label = f"#{k:02d}  +{tv:5.1f}s  ({fmt(g0 + tv)})  {why}  │  {snippet}"
            frames.append((dst, label))
            sample_rows.append({"k": k, "t_video": round(tv, 2), "t_global": round(g0 + tv, 2),
                                "why": why, "beat": bi, "words": snippet, "file": dst.name})
        mot = motion_stats(av, dur, reveal_times)
        header = [
            f"{stem}   \"{title}\"   global {fmt(g0)}–{fmt(g0 + dur)}   duration {dur:.1f}s   "
            f"{len(reveal_times)} reveals   picture static {mot['static_ratio'] * 100:.0f}% of the time",
            f"tiles: #k  +seconds into scene  (global m:ss)  why sampled  │  words being spoken "
            f"([current word]; ~ = interpolated inside the beat)      motion over the scene (2 s bars, right) →",
        ]
        build_sheet(frames, header, out / f"{stem}.sheet.jpg", mot["levels"])

        # transcript timeline (viewer-facing)
        canon = canonical_beats(base_by_id.get(sid))
        lines = [f"# {stem} — {title}", "",
                 f"- global {fmt(g0)} → {fmt(g0 + dur)}  (duration {dur:.1f} s; scene {n}/{len(scenes)})",
                 f"- narration: {mode}; {len(beats)} beats; {len(reveal_times)} on-screen reveals"
                 + (f"; first reveal at +{reveal_times[0]:.1f}s" if reveal_times else ""),
                 f"- picture: static {mot['static_ratio'] * 100:.0f}% of the time; moving {mot['moving_seconds']} s; "
                 f"longest still stretch {mot['longest_still_seconds']} s; change events at "
                 + (", ".join(f"+{e}" for e in mot["events"]) or "none")
                 + (f"; NOT tied to a reveal: {', '.join(f'+{e}' for e in mot['non_reveal_events'])}"
                    if mot["non_reveal_events"] else "; every change is a reveal fade-in"),
                 f"- motion profile (one glyph per 2 s, height = how much changed): `{mot['profile']}`", ""]
        if beats:
            lines += ["## Beats (what is said when; times are seconds into the scene video)", "",
                      "| beat | reveal | from | to | secs | words | words/s | spoken text |",
                      "|---|---|---|---|---|---|---|---|"]
            for b in beats:
                t0, t1 = SCENE_LEAD_SECONDS + b["start_seconds"], SCENE_LEAD_SECONDS + b["end_seconds"]
                nw = len(b["text"].split())
                lines.append(f"| {b['index']} | {b.get('reveal') or '(none)'} | +{t0:.1f} | +{t1:.1f} | {t1 - t0:.1f} | {nw} "
                             f"| {nw / max(t1 - t0, 0.1):.1f} | {b['text'].strip()} |")
            lines.append(f"| — | (tail) | +{SCENE_LEAD_SECONDS + beats[-1]['end_seconds']:.1f} | +{dur:.1f} | "
                         f"{dur - SCENE_LEAD_SECONDS - beats[-1]['end_seconds']:.1f} | 0 | | (narration over, picture holds) |")
            if canon and len(canon) == len(beats):
                lines += ["", "## Same beats, written form (LaTeX as in the canonical storyboard)", ""]
                lines += [f"{i}. {c}" for i, c in enumerate(canon, 1)]
        else:
            lines += ["## Silent scene (intro / divider / outro): no narration, animation only.", ""]
        lines += ["", "## Sampled frames (see the contact sheet; files in this folder)", "",
                  "| # | +s | global | why | beat | words at that instant |", "|---|---|---|---|---|---|"]
        lines += [f"| {r['k']:02d} | +{r['t_video']:.1f} | {fmt(r['t_global'])} | {r['why']} | {r['beat'] or '—'} | {r['words']} |"
                  for r in sample_rows]
        (out / f"{stem}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

        records.append({"n": n, "id": sid, "title": title, "kind": s.get("kind", "content"),
                        "template": s.get("template"), "hook": s.get("hook"), "mode": mode,
                        "global_start": round(g0, 3), "duration": round(dur, 3), "reveals": len(reveal_times),
                        "reveal_times": [round(r, 2) for r in reveal_times], "motion": mot,
                        "sheet": f"{stem}.sheet.jpg", "timeline": f"{stem}.md", "samples": sample_rows,
                        "beats": [{k: b.get(k) for k in ("index", "reveal", "start_seconds", "end_seconds", "text")} for b in beats],
                        "canonical_beats": canon})

    # INDEX (viewer-facing) + PRODUCTION (non-blind lenses) + pack.json
    idx = [f"# Rewatch pack — {args.deck}", "",
           f"Film: `{section_dir.name}/{args.deck}.mp4`, {fmt(total)} total, {len(records)} scenes. "
           "Each scene has a contact sheet (`NN_<scene>.sheet.jpg`: sampled frames labelled with the time and the words "
           "being spoken at that instant), a transcript timeline (`NN_<scene>.md`: every beat with its on-screen reveal, "
           "seconds and words/sec, plus motion statistics), and the sampled frames at full resolution (`NN_<scene>/`).",
           "", "How to read the motion numbers: the picture is sampled 4× per second in low resolution; a sample counts as "
           "*moving* when more than 0.2 % of pixels changed. `static` = share of the scene where nothing on screen changed; "
           "`change events` = moments something started changing; events *not tied to a reveal* mean motion beyond the "
           "fade-in of new text (i.e. an animation). The 2-s profile is a tiny bar chart of change over the scene.", "",
           "| # | scene | title | global start | secs | reveals | static | longest still | changes not tied to reveals |",
           "|---|---|---|---|---|---|---|---|---|"]
    for r in records:
        m = r["motion"]
        idx.append(f"| {r['n']:02d} | `{r['id']}` | {r['title']} | {fmt(r['global_start'])} | {r['duration']:.0f} | {r['reveals']} "
                   f"| {m['static_ratio'] * 100:.0f}% | {m['longest_still_seconds']}s | {len(m['non_reveal_events'])} |")
    (out / "INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    prod = ["# Production view (NOT for blind lenses)", "", "| # | scene | kind | template | hook | narration mode |", "|---|---|---|---|---|---|"]
    prod += [f"| {r['n']:02d} | `{r['id']}` | {r['kind']} | {r['template'] or '—'} | {r['hook'] or '—'} | {r['mode']} |" for r in records]
    (out / "PRODUCTION.md").write_text("\n".join(prod) + "\n", encoding="utf-8")
    (out / "pack.json").write_text(json.dumps({"deck": args.deck, "film": str(section_dir / f"{args.deck}.mp4"),
                                               "total_seconds": round(total, 3), "lead_seconds": SCENE_LEAD_SECONDS,
                                               "scenes": records}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[rewatch_pack] wrote {out}  ({len(records)} scenes; INDEX.md, PRODUCTION.md, pack.json)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

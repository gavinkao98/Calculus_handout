"""critic.py -- external visual-frame critic (VLM gate 2; advisory only).

The OFFLINE, zero-API half extracts the fullest frame of each content scene from
already-rendered scene videos and lays out exactly what would be sent to a vision
model -- WITHOUT calling one. The billed call is a separate, gated step (see
`critique_frame`), because every paid/external API call needs explicit per-run
approval with a cost estimate (CLAUDE.md).

Role in the review model: this is GATE 2 of the visual-frame audit -- the
external-VLM confidence check that mirrors the handout's figure-audit gate 2.
Gate 1 is a free Claude frame-grab subagent reading the same frames against
VISUAL-FRAME-RUBRIC.md every render; gate 2 (this, MiMo-V2.5) runs intermittently
before lock to cover gate 1's model blind spots. Both judge against the SAME SSOT
rubric, which this script injects VERBATIM into the prompt -- the dimensions live
only in VISUAL-FRAME-RUBRIC.md, never a second copy here. Convergence = visual
Blocking (V1-V10) == 0; A1-A7 are 0-100 magnitude that drive re-render priority.

Why frames, not the whole video: a content scene's reveal is additive (scene.py
_play_content), so the end of each beat is the fullest composition up to that
point -- the moment most likely to expose overlap / crowding / imbalance. One
PNG per scene is far cheaper than analysing every frame, and it is the same set
the gate-1 subagent needs.

Philosophy: the model drafts a *report* for a human to act on -- it never edits
the storyboard. The human stays the layout authority; the VLM only widens what
gets noticed.

Pipeline:
    storyboard.yml + output/audio/<id>/manifest.json + output/_media/.../*.mp4
        -> extract_frames()   ffmpeg grabs one fresh PNG per scene      (offline)
        -> build_prompt()     frame + VISUAL-FRAME rubric + beat context (offline)
        -> --dry-run          print the plan + a cost estimate          (offline)
        -> critique_frame()   the one billed call, gated behind --confirm

Run (offline, no key needed):
    python video/pipeline/critic.py --storyboard video/storyboards/_demo_derivation.yml --dry-run

Output dir: <section>/critic (or critic_mimo for an _mimo deck) by default, or --out <dir>
to pick another one (e.g. to keep a round's frames after a re-render, or to avoid two
concurrent runs on the same deck overwriting each other). Either way, existing frames/
under that dir are cleared first, so a run is always one complete retake, never a mix of
this round's and a prior round's PNGs.
"""
from __future__ import annotations

import argparse
import base64
import contextlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()

import numpy as np  # noqa: E402
import yaml  # noqa: E402

from pipeline import pauses  # noqa: E402
from pipeline.timing import SCENE_LEAD_SECONDS  # noqa: E402
from pipeline.sizecheck import graph_label_geometry  # noqa: E402
from pipeline.texlock import tex_lock  # noqa: E402

LEAD_SECONDS = SCENE_LEAD_SECONDS
BEAT_BACKOFF = 0.20     # grab this far before a beat boundary: reveal has settled,
                        # next beat not yet started (fullest frame for THIS beat)

# per == "scene" fullest-frame pick (backlog #10): decode the whole scene video at
# this fps in 192x108 gray, same recipe as rewatch_pack.motion_stats, to find which
# settled frame has the most "ink" -- for a scene with `exit:` that is NOT the last frame
# (the picture has been cleared by then), so grabbing the end (the old behaviour)
# extracted a blank frame and gate 1 audited nothing (scenes 06, 23, 2026-09-14).
INK_FPS = 4
INK_DIFF_THRESHOLD = 12   # same |pixel diff| > 12/255 convention as rewatch_pack.CHANGE_FRAC

# Cost estimate. MiMo-V2.5 (omnimodal) is Xiaomi's FREE public beta as of 2026-06
# (the same key/endpoint the project already uses for TTS), so the USD figure is
# $0. The call is still an EXTERNAL API, so --dry-run prints token magnitude and a
# run stays consent-gated per CLAUDE.md. If MiMo leaves free beta, set real rates
# here and the estimate updates; the token sizes below are rough, for magnitude.
PRICE_IN_PER_MTOK = 0.0     # USD per 1M input tokens  (MiMo free public beta, 2026-06)
PRICE_OUT_PER_MTOK = 0.0    # USD per 1M output tokens (MiMo free public beta, 2026-06)
EST_IMAGE_TOKENS = 1100     # rough input tokens for one 480p frame (magnitude only)
EST_PROMPT_TOKENS = 800     # text prompt + verbatim-injected VISUAL-FRAME rubric
EST_OUTPUT_TOKENS = 1700    # output tokens/frame: ~1300 MiMo reasoning + ~400 JSON

# MiMo platform (Xiaomi): OpenAI-compatible /chat/completions. Auth is the custom
# `api-key` header (Bearer is also sent, harmless if ignored). Vision model id is
# `mimo-v2.5` (the omnimodal one; `*-pro` is text-only). Key is read from the env
# var MIMO_API_KEY -- never a file, never logged, never committed.
DEFAULT_BASE_URL = "https://api.xiaomimimo.com/v1"
DEFAULT_MODEL = "mimo-v2.5"

# The visual-frame audit SSOT. Injected VERBATIM into the prompt so the dimensions
# live in exactly one place (VISUAL-FRAME-RUBRIC.md) -- the same file gate 1 reads.
RUBRIC_PATH = (Path(__file__).resolve().parent.parent
               / "content_scripts" / "_audit" / "VISUAL-FRAME-RUBRIC.md")


def load_rubric() -> str:
    """Read the VISUAL-FRAME rubric body for verbatim injection. Falls back to a
    one-line pointer if the file is missing, so an offline dry-run never crashes."""
    try:
        return RUBRIC_PATH.read_text(encoding="utf-8").strip()
    except OSError:
        return ("(VISUAL-FRAME-RUBRIC.md not found; judge V1-V10 visual blocking "
                "and score A1-A7 magnitude 0-100.)")


# ---- inputs -------------------------------------------------------------

def load_storyboard(path: Path) -> dict:
    return yaml.safe_load(path.resolve().read_text(encoding="utf-8"))


def load_manifest(deck_id: str, meta: dict | None = None) -> dict:
    if meta:
        sec_dir = _bootstrap.section_output_dir(meta)
        audio_subdir = "audio_mimo" if deck_id.endswith("_mimo") else "audio"
        mpath = sec_dir / audio_subdir / "manifest.json"
    else:
        mpath = _bootstrap.REPO_ROOT / "video" / "output" / "audio" / deck_id / "manifest.json"
    if not mpath.exists():
        raise SystemExit(
            f"No manifest at {mpath}. Render the deck first "
            f"(python video/make.py --storyboard <yml> --backend mock)."
        )
    return json.loads(mpath.read_text(encoding="utf-8"))


def find_scene_video(deck_id: str, scene_id: str) -> Path | None:
    """The freshest rendered mp4 for a scene (mirrors make.py's freshest-match:
    several resolution subdirs can hold a same-named clip)."""
    media = _bootstrap.REPO_ROOT / "video" / "output" / "_media"
    matches = list(media.rglob(f"{deck_id}__{scene_id}.mp4"))
    return max(matches, key=lambda p: p.stat().st_mtime) if matches else None


def _ffprobe_duration(video: Path) -> float | None:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(video)],
            capture_output=True, text=True,
        )
        return float(out.stdout.strip()) if out.returncode == 0 else None
    except Exception:  # noqa: BLE001
        return None


def _ffprobe_fps(video: Path) -> float | None:
    """The video stream's frame rate (`r_frame_rate`, e.g. "30/1"), or None."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=r_frame_rate", "-of", "default=noprint_wrappers=1:nokey=1", str(video)],
            capture_output=True, text=True,
        )
        num, _, den = out.stdout.strip().partition("/")
        return float(num) / float(den or 1) if out.returncode == 0 else None
    except Exception:  # noqa: BLE001
        return None


def _fullest_frame_ts(video: Path, settled: list[float],
                      end: float) -> "tuple[float, float | None] | None":
    """(ts_seconds, ink_ratio_vs_last) of the SETTLED frame with the most "ink", or None
    if the video can't be decoded (caller falls back to the end-of-scene pick).

    Only settled moments are candidates: `settled` (each beat's end, where its reveal and
    any `focus.indicate` are done and the next beat has not begun -- see `_settled_ts`)
    plus `end`, the last frame. An argmax over EVERY frame picked the middle of an
    indicate flash (block scaled 1.15x = +32 % ink) even in a purely additive scene
    (code review 2026-09-23, C-02). Ties go to the LATEST candidate; and if the last
    frame's ink is within 1% of the best, the last frame wins anyway -- so a purely
    additive scene still picks its end, and only a scene that clears itself (an `exit:`)
    moves off it.

    ink = fraction of pixels that differ from the scene's background gray level by
    more than INK_DIFF_THRESHOLD. The background level is not hard-coded (the deck
    can be light- or dark-ground): it is the single most common gray value across
    the whole decoded clip, since the background fills most of every frame even at
    the fullest reveal.
    """
    try:
        raw = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(video), "-an", "-vf",
             f"fps={INK_FPS},scale=192:108,format=gray", "-f", "rawvideo", "-"],
            capture_output=True, check=True,
        ).stdout
    except Exception:  # noqa: BLE001
        return None
    n = len(raw) // (192 * 108)
    if n < 1:
        return None
    frames = np.frombuffer(raw[: n * 192 * 108], dtype=np.uint8).reshape(n, 108, 192)
    bg = int(np.bincount(frames.reshape(-1)).argmax())
    ink = (np.abs(frames.astype(np.int16) - bg) > INK_DIFF_THRESHOLD).mean(axis=(1, 2))
    pool = [(t, float(ink[min(max(int(round(t * INK_FPS)), 0), n - 1)]))
            for t in sorted(settled) if t < end]
    pool.append((end, float(ink[-1])))   # the last decoded sample is the end composition
    best_ts, best_val = pool[0]
    for t, v in pool:                    # tie -> latest: >= keeps overwriting on ties
        if v >= best_val:
            best_ts, best_val = t, v
    last_val = pool[-1][1]
    if last_val >= 0.99 * best_val:      # purely additive: keep the end-of-scene pick
        best_ts = end
    ratio = round(best_val / last_val, 2) if last_val > 0 else None
    return best_ts, ratio


# ---- frame plan ---------------------------------------------------------

def _settled_ts(beat: dict) -> float:
    """Video time at which a beat's composition has settled: BEAT_BACKOFF before its end,
    after its reveal (and any indicate) and before the next beat's reveal begins."""
    return max(LEAD_SECONDS + float(beat["end_seconds"]) - BEAT_BACKOFF, 0.05)


def cumulative_reveals(beats: list[dict], upto: int) -> list[str]:
    """Reveal targets that should be on screen by the end of beat `upto`
    (additive reveal). Gives the VLM the 'what should be visible' context."""
    seen = []
    for b in beats[: upto + 1]:
        if b.get("reveal"):
            seen.append(b["reveal"])
    return seen


def plan_frames(storyboard: dict, manifest: dict, selector: str, per: str = "scene") -> list[dict]:
    """Frame plan + the context that travels with each frame (no extraction yet,
    so --dry-run stays free).

    per="scene" (default): ONE fullest frame per content scene -- the final
    composition after every reveal. That is what you actually want to judge: a
    mid-reveal beat is half-built, and the critic wrongly scores it as empty /
    unbalanced (a real artifact we hit and measured). per="beat": one frame per
    beat (progression view -- catches pacing issues, but ~3x the frames/cost).

    scene_number comes from the STORYBOARD's full scene order (1-based over every
    scene -- intro/divider/content/outro all take a number), not from the
    manifest entry: a manifest merged across renders (--reuse-existing) can carry
    a stale scene_number from a run where the deck had a different scene count,
    which duplicated 17 for two different scenes on 2026-09-13. This is the same
    counting rewatch_pack.py and a fresh tts.py manifest both use, so the three
    stay aligned."""
    titles = {s["id"]: s.get("title", "") for s in storyboard["scenes"]}
    scenes_by_id = {s["id"]: s for s in storyboard["scenes"]}
    scene_numbers = {s["id"]: i for i, s in enumerate(storyboard["scenes"], 1)}
    meta = storyboard.get("meta", {})
    by_id = {s["scene_id"]: s for s in manifest["scenes"]}
    if selector == "all":
        order = [s["scene_id"] for s in manifest["scenes"]]
    else:
        order = [x.strip() for x in selector.split(",") if x.strip()]

    plan: list[dict] = []
    # per="scene" attaches label geometry, and graph_label_geometry BUILDS the scene --
    # i.e. it compiles Tex into the cwd's shared media/Tex. One hold for the whole loop
    # rather than one per scene (pipeline/texlock.py). per="beat" builds nothing, so it
    # stays lock-free: a --dry-run beat plan must not queue behind someone else's render.
    with tex_lock(reason="critic label geometry") if per == "scene" else contextlib.nullcontext():
        for sid in order:
            entry = by_id.get(sid)
            if entry is None or entry.get("narration_mode") not in ("beats", "scene_aligned"):
                continue  # intro/outro are silent brand templates -- skip for now
            beats = entry.get("beats", [])
            if not beats:
                continue
            common = {"scene_id": sid, "scene_number": scene_numbers[sid],
                      "title": titles.get(sid, "")}
            if per == "scene":
                item = {**common, "beat_index": 0, "final": True,
                        # sentinel: extract_frames() resolves this to the fullest-ink ts
                        # among the settled moments below + the last frame (or, if that
                        # decode fails, clamps it to the last frame).
                        "ts": 1e9, "settled": [_settled_ts(b) for b in beats],
                        "fullest_ts": None, "ink_ratio_vs_last": None,
                        "narration": entry.get("script", ""), "reveal": None,
                        "revealed_so_far": cumulative_reveals(beats, len(beats) - 1)}
                # B.1b: attach deterministic graph-label geometry so build_prompt can
                # ground the VLM's V2/A1 judgment (only the fullest frame is judged, so
                # the final layout the labels settle into is the right one to describe).
                try:
                    geom = graph_label_geometry(meta, scenes_by_id.get(sid, {}), scenes_by_id)
                except Exception:  # noqa: BLE001
                    geom = None
                if geom:
                    item["label_geometry"] = geom
                plan.append(item)
            else:
                for i, beat in enumerate(beats):
                    plan.append({**common, "beat_index": beat["index"], "final": False,
                                 "ts": _settled_ts(beat),
                                 "narration": beat.get("text", ""), "reveal": beat.get("reveal"),
                                 "revealed_so_far": cumulative_reveals(beats, i)})
    return plan


def reset_frames_dir(out_dir: Path) -> None:
    """Clear out_dir/frames before a fresh extraction, so each run is one complete
    retake rather than PNGs from several rounds piling up in the same directory --
    e.g. renaming the whole critic dir to "keep as a snapshot" after a re-numbering
    fix silently carried five stale frames (incl. a pre-renumber scene) into the
    kept copy (2026-09-13). A directory kept as a snapshot (via --out) is untouched
    on the NEXT run only if it is given a new --out path."""
    frames_dir = out_dir / "frames"
    if frames_dir.exists() and any(frames_dir.iterdir()):
        shutil.rmtree(frames_dir)


def extract_frames(deck_id: str, plan: list[dict], out_dir: Path) -> list[dict]:
    """ffmpeg-grab one PNG per planned frame. Offline, free. Returns the plan
    with `frame_path` filled (or None on miss).

    A `final` (per=="scene") item first decodes the whole scene video once to find
    the fullest-ink frame (see `_fullest_frame_ts`). That is local work and no API
    call, so `--dry-run` -- gate 1's documented invocation -- does it too: skipping it
    there handed gate 1 the cleared end frame of every `exit:` scene (code review
    2026-09-23, C-01). If the decode fails, the item's `ts` sentinel falls through to
    the end-of-scene clamp below."""
    probes: dict[str, tuple[float | None, float | None]] = {}
    for item in plan:
        sid = item["scene_id"]
        video = find_scene_video(deck_id, sid)
        if video is None:
            print(f"[critic] no rendered mp4 for scene '{sid}' -- skipping", flush=True)
            item["frame_path"] = None
            continue
        if sid not in probes:
            probes[sid] = (_ffprobe_duration(video), _ffprobe_fps(video))
        dur, fps = probes[sid]
        # the last frame starts one frame interval before the end: aim half a frame
        # before it, so `-ss` lands on it at any fps (`dur - 0.05` fell past it < 20 fps)
        end = None if dur is None or not fps else dur - 1.5 / fps
        if item.get("final") and end is not None:
            found = _fullest_frame_ts(video, item.get("settled", []), end)
            if found is not None:
                item["ts"], item["ink_ratio_vs_last"] = found
                item["fullest_ts"] = item["ts"]
        ts = item["ts"] if end is None else min(item["ts"], end)
        frame_dir = out_dir / "frames" / f"{item['scene_number']:02d}_{sid}"
        frame_dir.mkdir(parents=True, exist_ok=True)
        name = "final.png" if item.get("final") else f"beat_{item['beat_index']:02d}.png"
        frame_path = frame_dir / name
        # freshness: drop any prior PNG first so a failed grab can never leave a
        # stale frame that the gate-1 subagent would read as current.
        frame_path.unlink(missing_ok=True)
        res = subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{ts:.3f}", "-i", str(video),
             "-frames:v", "1", "-q:v", "2", str(frame_path)],
            capture_output=True, text=True,
        )
        item["frame_path"] = str(frame_path) if res.returncode == 0 and frame_path.exists() else None
        if item["frame_path"] is None:
            print(f"[critic] ffmpeg miss {sid} beat {item['beat_index']} @ {ts:.2f}s", flush=True)
    return plan


# ---- prompt -------------------------------------------------------------

def _format_label_geometry(geom: dict) -> str:
    """Deterministic graph-label facts for the prompt (B.1b). Gives the VLM the
    exact label positions so it can ground V2 (label occludes) / A1 (label on a
    mark) instead of guessing, point any fix at real empty space, and -- when no
    overlap is listed -- NOT invent a collision. Frame-fraction coords, origin
    top-left. Kept compact: the rubric is already injected verbatim above."""
    lines = ["\nDeterministic graph-label facts (computed from the storyboard, not "
             "guessed) -- coordinates are fractions of the frame, origin TOP-LEFT, x "
             "right, y down. Use these to ground V2/A1 and aim any fix at real empty "
             "space:"]
    for lab in geom["labels"]:
        t = lab["text"] or lab["id"]
        b = lab["box"]
        lines.append(f"- label {t} at {lab['region']}, box x[{b[0]},{b[1]}] y[{b[2]},{b[3]}]")
    if geom["overlaps"]:
        for ov in geom["overlaps"]:
            lines.append(f"OVERLAP DETECTED (deterministic): {ov['a']} and {ov['b']} "
                         f"overlap {ov['pct']}% of the smaller -- a real V2/A1 defect. "
                         f"CRITICAL: You MUST provide two specific, mutually exclusive placement "
                         f"options in your suggestion (e.g., 'Option A: move {ov['a']} UP; "
                         f"Option B: move {ov['b']} to the RIGHT'), aimed at empty space.")
    else:
        lines.append("No equation-label overlap was detected geometrically -- do not "
                     "invent a label collision. However, if any label could be placed "
                     "in a more aesthetically pleasing, clear, or balanced position, "
                     "you MUST provide a specific suggestion (e.g., 'move [label] UP').")
    return "\n".join(lines) + "\n"


def build_prompt(item: dict, rubric: str) -> str:
    """The text half of one critique request (the frame image travels alongside).
    Injects VISUAL-FRAME-RUBRIC.md VERBATIM (the single source of the dimensions,
    the blocking line, and the 'not a finding' list) and asks for strict JSON:
    V1-V10 blocking findings + A1-A7 magnitude scores, so the report is
    machine-collatable. Two framings: a final-frame critique (judge the finished
    composition) vs a mid-beat critique (emptiness is expected)."""
    if item.get("final"):
        ctx = (
            "This is the FINAL, fullest frame of the scene -- every element that "
            "appears during the scene is now shown. They revealed progressively, in "
            "sync with the narration, so do NOT treat 'everything is visible at once' "
            "as a flaw, and do NOT expect motion in a still frame.\n"
            f"Scene title: {item['title']}\n"
            f"Full narration of the scene: {item['narration']}\n"
        )
    else:
        revealed = ", ".join(item["revealed_so_far"]) or "(title / scaffold only)"
        ctx = (
            "Judge ONLY what is visible in this single MID-scene frame. Elements "
            "reveal progressively, so empty space here is not necessarily a flaw.\n"
            f"Scene title: {item['title']}\n"
            f"Narration spoken as this frame shows: {item['narration']}\n"
            f"Elements visible by now: {revealed}\n"
        )
    geom = item.get("label_geometry")
    if geom and geom.get("labels"):
        ctx += _format_label_geometry(geom)
    return (
        "You are the external visual-frame critic (gate 2) for an educational "
        "mathematics video. Judge the attached frame STRICTLY against the rubric "
        "below -- it is the single source of truth for the dimensions, the blocking "
        "line, and what is NOT a finding.\n\n"
        "=== VISUAL-FRAME RUBRIC (verbatim) ===\n" + rubric +
        "\n=== END RUBRIC ===\n\n"
        + ctx +
        "\nNow judge THIS frame.\n"
        "- Layer 1 (V1-V10): for each visual issue cite the V-code and mark "
        "Blocking vs Advisory per the escalation rule -- loses info / contradicts "
        "the beat / garbled or missing math -> Blocking; merely cramped or unclear "
        "-> Advisory (score it in Layer 2 instead). Count the Blocking ones.\n"
        "- Layer 2 (A1-A7): score each 0-100 and list concrete defects with where "
        "in the frame they are.\n"
        "Honour the rubric's 'not a finding' list (dark-flat minimal background, "
        "progressive reveal, still frame, deliberate schematic scale). A clean "
        "frame is a valid result -- do not over-report.\n\n"
        "Return STRICT JSON only:\n"
        '{"visual_blocking_count":int,'
        '"v_findings":[{"code":"V1..V10","severity":"Blocking|Advisory",'
        '"where":str,"issue":str,"why":str,"suggestion":str}],'
        '"scores":{"a1_element_layout":int,"a2_attractiveness":int,'
        '"a3_logic_flow":int,"a4_visual_consistency":int,"a5_accuracy_depth":int,'
        '"a6_typography_wrapping":int,"a7_hierarchy_focus":int},'
        '"defects":[{"dimension":str,"severity":"low|med|high","where":str,'
        '"issue":str,"suggestion":str}],"overall":str}'
    )


# ---- billed call (gated behind --confirm) -------------------------------

def _image_data_url(path: str) -> str:
    b64 = base64.b64encode(Path(path).read_bytes()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def _extract_json(text: str) -> dict:
    """The model returns a JSON object, sometimes wrapped in a ```json fence or
    with prose around it. Be lenient: strip the fence, take the outer {...}, and
    repair invalid escapes -- MiMo writes LaTeX ($\\sqrt[3]{x}$, $\\to$) inside the
    string values, and a lone backslash is an illegal JSON escape that breaks
    json.loads."""
    s = text.strip()
    if s.startswith("```"):
        s = s.split("```", 2)[1]
        if s.lstrip().startswith("json"):
            s = s.lstrip()[4:]
    i, j = s.find("{"), s.rfind("}")
    if 0 <= i < j:
        s = s[i:j + 1]
    try:
        return json.loads(s)
    except Exception:  # noqa: BLE001
        # double any backslash that is not a legal JSON escape, so \sqrt -> \\sqrt
        # (decodes to a literal backslash) instead of crashing the parse
        return json.loads(re.sub(r'\\(?![\\"/bfnrtu])', r'\\\\', s))


def critique_frame(item: dict, *, base_url: str, api_key: str, model: str, rubric: str,
                   max_tokens: int = 8000, timeout: int = 180, retries: int = 3) -> dict:
    """One billed vision call: frame image + build_prompt(item) -> parsed JSON
    critique + token usage. OpenAI-compatible /chat/completions on the MiMo
    platform. Retries 429/5xx/timeouts with backoff. Advisory only -- the caller
    writes a report, nothing auto-edits.

    max_tokens is generous on purpose: MiMo-V2.5 is a REASONING model -- it spends
    completion tokens on hidden reasoning (`reasoning_content`) before emitting the
    JSON, so a low cap gets consumed by reasoning and returns empty `content`
    (cost us a wasted batch at 1200). Billing is on ACTUAL tokens, so a high cap
    only prevents truncation; it does not cost more."""
    body = json.dumps({
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": build_prompt(item, rubric)},
                {"type": "image_url",
                 "image_url": {"url": _image_data_url(item["frame_path"])}},
            ],
        }],
        "max_completion_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions", data=body, method="POST",
        headers={
            "Content-Type": "application/json",
            "api-key": api_key,                     # MiMo platform custom header
            "Authorization": f"Bearer {api_key}",   # also send Bearer (harmless)
        },
    )
    data = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep((2 ** attempt) * 2)   # 2s, 4s, 8s
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if attempt < retries:
                time.sleep((2 ** attempt) * 2)
                continue
            raise
    content = data["choices"][0]["message"]["content"]
    try:
        critique = _extract_json(content)
    except Exception:  # noqa: BLE001
        critique = None
    return {"raw": content, "critique": critique, "usage": data.get("usage", {})}


def _write_md(results: list[dict], path: Path) -> None:
    out = ["# Visual-frame critique (MiMo-V2.5, gate 2) -- advisory report\n",
           "> Convergence = visual Blocking (V1-V10) == 0. A1-A7 are 0-100 "
           "magnitude (drive re-render priority; advisory, do not gate).\n"]
    for r in results:
        lab = "final frame" if r.get("final") else f"beat {r['beat_index']:02d}"
        out.append(f"## {r['scene_number']:02d} {r['scene_id']} -- {lab}")
        out.append(f"*{r['title']}*  \n`{r['frame_path']}`\n")
        if r.get("error"):           # the call itself failed: say why, not "bad JSON"
            out.append(f"> call failed, no critique: {r['error']}\n")
            continue
        c = r.get("critique")
        if not c:
            out.append("> could not parse JSON; raw model output:\n")
            out.append("```\n" + (r.get("raw") or "")[:1500] + "\n```\n")
            continue
        vf = c.get("v_findings", []) or []
        n_block = c.get("visual_blocking_count")
        if n_block is None:
            n_block = sum(1 for f in vf
                          if str(f.get("severity", "")).lower().startswith("block"))
        out.append(f"**VERDICT: {n_block} visual blocking**\n")
        for f in vf:
            why = f" — {f['why']}" if f.get("why") else ""
            sug = f" → {f['suggestion']}" if f.get("suggestion") else ""
            out.append(f"- **[{f.get('severity','?')}] {f.get('code','V?')}** "
                       f"({f.get('where','?')}): {f.get('issue','?')}{why}{sug}")
        sc = c.get("scores", {})
        if sc:
            out.append("\n| A1 Layout | A2 Attract | A3 Flow | A4 Consist | "
                       "A5 Acc&Depth | A6 Typo/wrap | A7 Hierarchy |")
            out.append("|---|---|---|---|---|---|---|")
            out.append(f"| {sc.get('a1_element_layout','?')} | {sc.get('a2_attractiveness','?')} | "
                       f"{sc.get('a3_logic_flow','?')} | {sc.get('a4_visual_consistency','?')} | "
                       f"{sc.get('a5_accuracy_depth','?')} | {sc.get('a6_typography_wrapping','?')} | "
                       f"{sc.get('a7_hierarchy_focus','?')} |\n")
        for d in c.get("defects", []) or []:
            out.append(f"- **[{d.get('severity','?')}] {d.get('dimension','?')}** "
                       f"({d.get('where','?')}): {d.get('issue','?')} "
                       f"→ {d.get('suggestion','')}")
        if c.get("overall"):
            out.append(f"\n> {c['overall']}")
        out.append("")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def run_critique(plan: list[dict], *, base_url: str, api_key: str, model: str,
                 out_dir: Path, rubric: str, smoke: bool = False,
                 delay: float = 0.6) -> "list[dict] | None":
    have = [p for p in plan if p.get("frame_path")]
    if smoke:
        have = have[:1]
    if not have:
        print("[critic] no frames to critique.", flush=True)
        return None
    print(f"[critic] critiquing {len(have)} frame(s) via {model} ...", flush=True)
    results, tin, tout, failures = [], 0, 0, 0
    for n, item in enumerate(have):
        label = f"{item['scene_id']} beat {item['beat_index']:02d}"
        print(f"[critic] -> {label} ({n + 1}/{len(have)})", flush=True)
        fields = {k: item.get(k) for k in
                  ("scene_id", "scene_number", "beat_index", "title", "frame_path", "final")}
        # one bad frame must not lose the batch: record it and carry on
        try:
            r = critique_frame(item, base_url=base_url, api_key=api_key,
                               model=model, rubric=rubric)
        except urllib.error.HTTPError as e:  # noqa: PERF203
            msg = e.read().decode("utf-8", "replace")[:300]
            print(f"           HTTP {e.code}: {msg}  -- skipped", flush=True)
            failures += 1
            results.append(fields | {"usage": {}, "critique": None, "raw": None,
                                     "error": f"HTTP {e.code}: {msg}"})
            continue
        except Exception as e:  # noqa: BLE001
            print(f"           error: {e!r}  -- skipped", flush=True)
            failures += 1
            results.append(fields | {"usage": {}, "critique": None, "raw": None, "error": repr(e)})
            continue
        u = r["usage"]
        tin += int(u.get("prompt_tokens", 0))
        tout += int(u.get("completion_tokens", 0))
        if r["critique"] and r["critique"].get("scores"):
            print(f"           scores {r['critique']['scores']}", flush=True)
        elif r["critique"] is None:
            print("           (response not parseable JSON -- kept raw)", flush=True)
        results.append(fields | {"usage": u, "critique": r["critique"], "raw": r["raw"]})
        if delay and n < len(have) - 1:
            time.sleep(delay)
    (out_dir / "critique.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _write_md(results, out_dir / "critique.md")
    usd = tin / 1e6 * PRICE_IN_PER_MTOK + tout / 1e6 * PRICE_OUT_PER_MTOK
    ok = len(results) - failures
    print(f"\n[critic] done: {ok}/{len(results)} ok"
          f"{f', {failures} failed' if failures else ''}; tokens {tin:,} in + {tout:,} out "
          f"-> ~${usd:.4f} (MiMo free public beta, 2026-06). "
          f"reports -> {out_dir / 'critique.md'}", flush=True)
    return results


# ---- dry-run / cost estimate -------------------------------------------

def estimate_cost(n_frames: int) -> dict:
    in_tok = n_frames * (EST_IMAGE_TOKENS + EST_PROMPT_TOKENS)
    out_tok = n_frames * EST_OUTPUT_TOKENS
    usd = in_tok / 1e6 * PRICE_IN_PER_MTOK + out_tok / 1e6 * PRICE_OUT_PER_MTOK
    return {"frames": n_frames, "input_tokens": in_tok, "output_tokens": out_tok, "usd": usd}


def dry_run(plan: list[dict], rubric: str) -> None:
    have = [p for p in plan if p.get("frame_path")]
    print(f"\n[dry-run] {len(have)}/{len(plan)} frames extracted; "
          f"NO API call. This is what WOULD be sent to MiMo-V2.5:\n", flush=True)
    for p in plan:
        tag = p.get("frame_path") or "(no frame)"
        lab = "final" if p.get("final") else f"beat {p['beat_index']:02d}"
        if p.get("final"):
            ts = "end" if p.get("fullest_ts") is None else f"{p['fullest_ts']:.2f}s (fullest)"
        else:
            ts = f"{p['ts']:.2f}s"
        print(f"  {p['scene_number']:02d} {p['scene_id']} {lab} @ {ts} -> {tag}", flush=True)
    if have:
        print("\n  --- example prompt (first extracted frame) ---", flush=True)
        for line in build_prompt(have[0], rubric).splitlines():
            print(f"  | {line}", flush=True)
    est = estimate_cost(len(have))
    print(f"\n[estimate] {est['frames']} frames -> ~{est['input_tokens']:,} in + "
          f"~{est['output_tokens']:,} out tokens -> ~${est['usd']:.3f} "
          f"(MiMo-V2.5 free public beta, 2026-06; external API -- consent still "
          f"required per CLAUDE.md before --confirm).", flush=True)
    print("[note] no key was used and no request was sent.", flush=True)


def main() -> int:
    # The injected rubric and model output are UTF-8 (Chinese + ✓/✗); a Windows
    # cp950 console would otherwise crash on the dry-run prompt echo.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(
        description="External visual-frame critic / gate 2 (offline plan; billed VLM call gated).")
    parser.add_argument("--storyboard", required=True, type=Path)
    parser.add_argument("--scene", default="all", help="id, 'a,b,c', or 'all'")
    parser.add_argument("--dry-run", action="store_true",
                        help="extract frames + print the plan/prompt/estimate; never calls the API")
    parser.add_argument("--confirm", action="store_true",
                        help="actually call the VLM (BILLED). Reads key from env MIMO_API_KEY.")
    parser.add_argument("--smoke", action="store_true",
                        help="with --confirm, critique only the FIRST frame (one billed call)")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--per", choices=("scene", "beat"), default="scene",
                        help="scene = one fullest frame per scene (default); beat = one per beat")
    parser.add_argument("--out", type=Path, default=None,
                        help="output dir for frames/critique (default: <section>/critic"
                             " or critic_mimo). Existing frames/ under it are cleared first, "
                             "so two runs never mix frames from different rounds; use a fresh "
                             "--out to keep a prior round untouched. Only one run at a time "
                             "should target the same dir.")
    args = parser.parse_args()

    storyboard = load_storyboard(args.storyboard)
    meta = storyboard["meta"]
    deck_id = meta["id"]
    # make.py rendered from this manifest with the storyboard's `pauses:` folded in (in
    # memory only); fold the same holds in here or every grab after one is early
    manifest = pauses.apply_pauses_timing(storyboard["scenes"], load_manifest(deck_id, meta))

    sec_dir = _bootstrap.section_output_dir(meta)
    critic_subdir = "critic_mimo" if deck_id.endswith("_mimo") else "critic"
    out_dir = args.out if args.out else sec_dir / critic_subdir
    plan = plan_frames(storyboard, manifest, args.scene, per=args.per)
    if not plan:
        print("[critic] no content beats selected.", flush=True)
        return 0
    print(f"[critic] {deck_id}: planning {len(plan)} frame(s) across content scenes", flush=True)
    print(f"[critic] output dir: {out_dir}", flush=True)
    rubric = load_rubric()
    reset_frames_dir(out_dir)
    plan = extract_frames(deck_id, plan, out_dir)
    (out_dir / "frame_plan.json").write_text(
        json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if args.confirm:
        api_key = os.environ.get("MIMO_API_KEY")
        if not api_key:
            print("[critic] --confirm needs the API key in env MIMO_API_KEY "
                  "(never pass it on the command line as a flag).", flush=True)
            return 2
        res = run_critique(plan, base_url=args.base_url, api_key=api_key,
                           model=args.model, out_dir=out_dir, rubric=rubric,
                           smoke=args.smoke)
        if not res:
            return 1
        failed = [r for r in res if r.get("error")]
        if failed:           # recorded and skipped so the batch goes on -- not a pass
            print(f"[critic] {len(failed)}/{len(res)} VLM call(s) failed -- exit 1", flush=True)
            return 1
    elif args.dry_run:
        dry_run(plan, rubric)
    else:
        print("[critic] frames extracted. Re-run with --dry-run for the send plan + "
              "estimate, or --confirm to run the billed critique (env MIMO_API_KEY).",
              flush=True)
    # a gate that audits fewer frames than it planned must not pass as if it had audited them
    missed = [p for p in plan if not p.get("frame_path")]
    if missed:
        print(f"[critic] {len(missed)}/{len(plan)} planned frame(s) not extracted: "
              + ", ".join(f"{p['scene_id']} beat {p['beat_index']:02d}" for p in missed)
              + " -- exit 1", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

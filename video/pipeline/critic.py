"""critic.py -- P1 visual-critique scaffold (Code2Video adoption, advisory only).

What this is: the OFFLINE, zero-API half of the VLM critic. It extracts the
fullest frame of each narration beat from already-rendered scene videos and lays
out exactly what would be sent to a vision model -- WITHOUT calling one. The
billed call is a separate, gated step (see `critique_frame`), because every paid
API call needs explicit per-run approval with a cost estimate (CLAUDE.md).

Why frames, not the whole video: a content scene's reveal is additive (scene.py
_play_content), so the end of each beat is the fullest composition up to that
point -- the moment most likely to expose overlap / crowding / imbalance. One
PNG per beat is far cheaper than analysing every frame, and it is the same set a
VLM would need to judge layout.

Philosophy (unchanged from CODE2VIDEO_STUDY.md P1): the model drafts a *report*
for a human to act on -- it never edits the storyboard. The human stays the
layout authority; the VLM only widens what gets noticed. The five scoring
dimensions are the AES rubric written into DESIGN.md (Visual QA).

Pipeline:
    storyboard.yml + output/audio/<id>/manifest.json + output/_media/.../*.mp4
        -> extract_frames()   ffmpeg grabs one PNG per beat            (offline)
        -> build_prompt()     frame + title + beat narration + reveals (offline)
        -> --dry-run          print the plan + a cost estimate         (offline)
        -> critique_frame()   the one billed call, gated               (TODO: wire)

Run (offline, no key needed):
    python video/pipeline/critic.py --storyboard video/storyboards/ch01_inverse_functions.yml --dry-run
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()

import yaml  # noqa: E402

LEAD_SECONDS = 0.3      # matches scene.py's initial self.wait(0.3) before beat 1
BEAT_BACKOFF = 0.20     # grab this far before a beat boundary: reveal has settled,
                        # next beat not yet started (fullest frame for THIS beat)

# Placeholder pricing for the cost estimate, clearly labelled -- replace with the
# confirmed MiMo-V2.5 (omnimodal) vision rates once the provider is fixed. Sources
# put MiMo-V2.5 inference at ~half MiMo-V2.5-Pro ($0.435/$0.87 per 1M tok).
PRICE_IN_PER_MTOK = 0.22    # USD per 1M input tokens  (PLACEHOLDER)
PRICE_OUT_PER_MTOK = 0.44   # USD per 1M output tokens (PLACEHOLDER)
EST_IMAGE_TOKENS = 1100     # rough input tokens for one 480p frame (PLACEHOLDER)
EST_PROMPT_TOKENS = 320     # rough input tokens for the text prompt
EST_OUTPUT_TOKENS = 1700    # output tokens/frame: ~1300 MiMo reasoning + ~400 JSON

# MiMo platform (Xiaomi): OpenAI-compatible /chat/completions. Auth is the custom
# `api-key` header (Bearer is also sent, harmless if ignored). Vision model id is
# `mimo-v2.5` (the omnimodal one; `*-pro` is text-only). Key is read from the env
# var MIMO_API_KEY -- never a file, never logged, never committed.
DEFAULT_BASE_URL = "https://api.xiaomimimo.com/v1"
DEFAULT_MODEL = "mimo-v2.5"


# ---- inputs -------------------------------------------------------------

def load_storyboard(path: Path) -> dict:
    return yaml.safe_load(path.resolve().read_text(encoding="utf-8"))


def load_manifest(deck_id: str) -> dict:
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


# ---- frame plan ---------------------------------------------------------

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
    beat (progression view -- catches pacing issues, but ~3x the frames/cost)."""
    titles = {s["id"]: s.get("title", "") for s in storyboard["scenes"]}
    by_id = {s["scene_id"]: s for s in manifest["scenes"]}
    if selector == "all":
        order = [s["scene_id"] for s in manifest["scenes"]]
    else:
        order = [x.strip() for x in selector.split(",") if x.strip()]

    plan: list[dict] = []
    for sid in order:
        entry = by_id.get(sid)
        if entry is None or entry.get("narration_mode") != "beats":
            continue  # intro/outro are silent brand templates -- skip for now
        beats = entry.get("beats", [])
        if not beats:
            continue
        common = {"scene_id": sid, "scene_number": entry["scene_number"],
                  "title": titles.get(sid, "")}
        if per == "scene":
            plan.append({**common, "beat_index": 0, "final": True,
                         "ts": 1e9,  # extract clamps to (duration - 0.05): the last held frame
                         "narration": entry.get("script", ""), "reveal": None,
                         "revealed_so_far": cumulative_reveals(beats, len(beats) - 1)})
        else:
            for i, beat in enumerate(beats):
                plan.append({**common, "beat_index": beat["index"], "final": False,
                             "ts": max(LEAD_SECONDS + float(beat["end_seconds"]) - BEAT_BACKOFF, 0.05),
                             "narration": beat.get("text", ""), "reveal": beat.get("reveal"),
                             "revealed_so_far": cumulative_reveals(beats, i)})
    return plan


def extract_frames(deck_id: str, plan: list[dict], out_dir: Path) -> list[dict]:
    """ffmpeg-grab one PNG per planned frame. Offline, free. Returns the plan
    with `frame_path` filled (or None on miss)."""
    durations: dict[str, float | None] = {}
    for item in plan:
        sid = item["scene_id"]
        video = find_scene_video(deck_id, sid)
        if video is None:
            print(f"[critic] no rendered mp4 for scene '{sid}' -- skipping", flush=True)
            item["frame_path"] = None
            continue
        if sid not in durations:
            durations[sid] = _ffprobe_duration(video)
        dur = durations[sid]
        ts = item["ts"] if dur is None else min(item["ts"], dur - 0.05)
        frame_dir = out_dir / "frames" / f"{item['scene_number']:02d}_{sid}"
        frame_dir.mkdir(parents=True, exist_ok=True)
        name = "final.png" if item.get("final") else f"beat_{item['beat_index']:02d}.png"
        frame_path = frame_dir / name
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

RUBRIC = (
    "- Element Layout: overlap, crowding, spilling past the safe margin, balance.\n"
    "- Attractiveness: clear and purposeful, not a flat text slide.\n"
    "- Logic Flow: does what is shown match this narration beat.\n"
    "- Visual Consistency: consistent accent colours, font sizes, spacing.\n"
    "- Accuracy & Depth: does the visual convey the point; any visible labelling problem."
)


def build_prompt(item: dict) -> str:
    """The text half of one critique request (the frame image travels alongside).
    Mirrors DESIGN.md's Visual QA five dimensions; asks for strict JSON so the
    report is machine-collatable. Two framings: a final-frame critique (judge the
    finished composition) vs a mid-beat critique (emptiness is expected)."""
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
    return (
        "You are a visual-layout critic for an educational mathematics video "
        "(3Blue1Brown style, dark theme). NOTE the house style is deliberately flat "
        "and minimal -- a solid dark background with NO gradients, noise, or grid is "
        "intentional, not a defect; do not suggest adding them.\n\n"
        + ctx +
        "\nScore each dimension 0-100 and list concrete, specific defects with where "
        "in the frame they are:\n" + RUBRIC + "\n\n"
        "Return STRICT JSON only:\n"
        '{"scores":{"element_layout":int,"attractiveness":int,"logic_flow":int,'
        '"visual_consistency":int,"accuracy_depth":int},'
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


def critique_frame(item: dict, *, base_url: str, api_key: str, model: str,
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
                {"type": "text", "text": build_prompt(item)},
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
    out = ["# Visual critique (MiMo-V2.5) -- advisory report\n"]
    for r in results:
        lab = "final frame" if r.get("final") else f"beat {r['beat_index']:02d}"
        out.append(f"## {r['scene_number']:02d} {r['scene_id']} -- {lab}")
        out.append(f"*{r['title']}*  \n`{r['frame_path']}`\n")
        c = r.get("critique")
        if not c:
            out.append("> could not parse JSON; raw model output:\n")
            out.append("```\n" + (r.get("raw") or "")[:1500] + "\n```\n")
            continue
        sc = c.get("scores", {})
        if sc:
            out.append("| Element Layout | Attractiveness | Logic Flow | Visual Consistency | Accuracy & Depth |")
            out.append("|---|---|---|---|---|")
            out.append(f"| {sc.get('element_layout','?')} | {sc.get('attractiveness','?')} | "
                       f"{sc.get('logic_flow','?')} | {sc.get('visual_consistency','?')} | "
                       f"{sc.get('accuracy_depth','?')} |\n")
        for d in c.get("defects", []) or []:
            out.append(f"- **[{d.get('severity','?')}] {d.get('dimension','?')}** "
                       f"({d.get('where','?')}): {d.get('issue','?')} "
                       f"→ {d.get('suggestion','')}")
        if c.get("overall"):
            out.append(f"\n> {c['overall']}")
        out.append("")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def run_critique(plan: list[dict], *, base_url: str, api_key: str, model: str,
                 out_dir: Path, smoke: bool = False, delay: float = 0.6) -> "list[dict] | None":
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
            r = critique_frame(item, base_url=base_url, api_key=api_key, model=model)
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
          f"-> ~${usd:.4f} (placeholder rates). reports -> {out_dir / 'critique.md'}", flush=True)
    return results


# ---- dry-run / cost estimate -------------------------------------------

def estimate_cost(n_frames: int) -> dict:
    in_tok = n_frames * (EST_IMAGE_TOKENS + EST_PROMPT_TOKENS)
    out_tok = n_frames * EST_OUTPUT_TOKENS
    usd = in_tok / 1e6 * PRICE_IN_PER_MTOK + out_tok / 1e6 * PRICE_OUT_PER_MTOK
    return {"frames": n_frames, "input_tokens": in_tok, "output_tokens": out_tok, "usd": usd}


def dry_run(plan: list[dict]) -> None:
    have = [p for p in plan if p.get("frame_path")]
    print(f"\n[dry-run] {len(have)}/{len(plan)} frames extracted; "
          f"NO API call. This is what WOULD be sent to MiMo-V2.5:\n", flush=True)
    for p in plan:
        tag = p.get("frame_path") or "(no frame)"
        lab = "final" if p.get("final") else f"beat {p['beat_index']:02d}"
        ts = "end" if p.get("final") else f"{p['ts']:.2f}s"
        print(f"  {p['scene_number']:02d} {p['scene_id']} {lab} @ {ts} -> {tag}", flush=True)
    if have:
        print("\n  --- example prompt (first extracted frame) ---", flush=True)
        for line in build_prompt(have[0]).splitlines():
            print(f"  | {line}", flush=True)
    est = estimate_cost(len(have))
    print(f"\n[estimate] {est['frames']} frames -> ~{est['input_tokens']:,} in + "
          f"~{est['output_tokens']:,} out tokens -> ~${est['usd']:.3f} "
          f"(PLACEHOLDER pricing; confirm MiMo-V2.5 vision rates before any run).",
          flush=True)
    print("[note] no key was used and no request was sent.", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="P1 visual-critique scaffold (offline; billed call gated).")
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
    args = parser.parse_args()

    storyboard = load_storyboard(args.storyboard)
    deck_id = storyboard["meta"]["id"]
    manifest = load_manifest(deck_id)

    out_dir = _bootstrap.REPO_ROOT / "video" / "output" / "critic" / deck_id
    plan = plan_frames(storyboard, manifest, args.scene, per=args.per)
    if not plan:
        print("[critic] no content beats selected.", flush=True)
        return 0
    print(f"[critic] {deck_id}: planning {len(plan)} frame(s) across content scenes", flush=True)
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
                           model=args.model, out_dir=out_dir, smoke=args.smoke)
        return 0 if res else 1
    if args.dry_run:
        dry_run(plan)
    else:
        print("[critic] frames extracted. Re-run with --dry-run for the send plan + "
              "estimate, or --confirm to run the billed critique (env MIMO_API_KEY).",
              flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

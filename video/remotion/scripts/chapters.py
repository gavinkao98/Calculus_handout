"""Scene chapters for the §3.1 render: a readable list + MP4 chapter metadata.

Scene start times are computed exactly the way the composition does it
(src/s31/timing.ts `buildShow`): the LEAD / TAIL / OVER / FPS constants are
read from that file, so the chapters cannot drift from the render.

    python scripts/chapters.py public/audio/s31_scene/manifest.json out/s31_v3_chapters.txt \
        --embed out/s31_v3_final.mp4

--embed writes the chapters into the mp4 in place (ffmpeg -f ffmetadata, stream copy).
"""
import argparse
import json
import math
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]  # paper/
TIMING = HERE / "src" / "s31" / "timing.ts"

# short 繁中 labels per scene id (display only; order/timing come from the manifest)
LABELS = {
    "circle": "開場：單位圓上的速度",
    "title": "標題頁",
    "stuck": "代數卡關：一切歸結到 sinθ/θ",
    "rewrite": "和差化積：兩筆債",
    "areas": "三塊面積夾出不等式",
    "continuity": "債一：sin、cos 連續",
    "limit": "債二：關鍵極限 = 1",
    "warnings": "兩個提醒",
    "payoff": "兩個導數定理",
    "slope": "斜率等於高度",
    "companion": "伴隨極限 (1−cosθ)/θ",
    "four": "其餘四個三角導數",
    "spring": "彈簧上的重物",
    "cycle": "導數循環",
    "next": "下一節：連鎖律",
}


def constants() -> dict:
    src = TIMING.read_text(encoding="utf-8")
    out = {}
    for name in ("FPS", "LEAD", "TAIL", "OVER"):
        m = re.search(rf"export const {name} = (\d+);", src)
        if not m:
            sys.exit(f"[chapters] cannot find {name} in {TIMING}")
        out[name] = int(m.group(1))
    return out


def scenes(manifest: Path) -> tuple[list[dict], int, int]:
    """Mirror of buildShow: returns [{id, from, dur}], total frames, fps."""
    c = constants()
    fps, lead, tail, over = c["FPS"], c["LEAD"], c["TAIL"], c["OVER"]
    data = json.loads(manifest.read_text(encoding="utf-8"))
    t = 0
    out = []
    for i, s in enumerate(data["scenes"]):
        narrated = s["kind"] == "content" and s.get("audio_seconds") is not None
        # JS Math.round rounds .5 up; floor(x + .5) matches it for positive x
        dur = lead + math.ceil(s["audio_seconds"] * fps) + tail if narrated else math.floor(s.get("duration", 4) * fps + 0.5)
        start = 0 if i == 0 else t - over
        t = start + dur
        out.append({"id": s["scene_id"], "from": start, "dur": dur})
    return out, t, fps


def mmss(frames: int, fps: int) -> str:
    sec = int(frames // fps)  # whole seconds, floored: a jump lands on or just before the sheet slides in
    return f"{sec // 60:02d}:{sec % 60:02d}"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp950
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", type=Path)
    ap.add_argument("out_txt", type=Path)
    ap.add_argument("--embed", type=Path, help="mp4 to write the chapters into (in place, stream copy)")
    a = ap.parse_args()

    sc, total, fps = scenes(a.manifest)
    lines = [f"{mmss(s['from'], fps)}  {s['id']:<11} {LABELS.get(s['id'], s['id'])}" for s in sc]
    lines.append(f"# total {mmss(total, fps)} ({total} frames @ {fps} fps)")
    a.out_txt.parent.mkdir(parents=True, exist_ok=True)
    a.out_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    if a.embed:
        # ffmetadata chapters in milliseconds; each ends where the next begins
        meta = [";FFMETADATA1"]
        for i, s in enumerate(sc):
            start = round(s["from"] * 1000 / fps)
            end = round((sc[i + 1]["from"] if i + 1 < len(sc) else total) * 1000 / fps)
            title = f"{s['id']} · {LABELS.get(s['id'], s['id'])}".replace("=", "\\=").replace(";", "\\;").replace("#", "\\#")
            meta += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={start}", f"END={end}", f"title={title}"]
        meta_path = a.out_txt.with_suffix(".ffmeta")
        meta_path.write_text("\n".join(meta) + "\n", encoding="utf-8")
        tmp = a.embed.with_name(a.embed.stem + ".chapters_tmp" + a.embed.suffix)
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(a.embed), "-i", str(meta_path),
               "-map", "0", "-map_metadata", "0", "-map_chapters", "1", "-c", "copy", str(tmp)]
        subprocess.run(cmd, check=True)
        tmp.replace(a.embed)
        meta_path.unlink()
        print(f"[chapters] embedded {len(sc)} chapters into {a.embed}")


if __name__ == "__main__":
    main()

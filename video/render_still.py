"""Render the FINAL frame of storyboard scene(s) to PNG — fast visual QA.

No audio / beat timing: builds each scene's blocks and adds them all (final state),
then saves a 1920x1080 still. For checking layout/colour/font/glow against the
redesign frames during the Direction-D rebuild.

    python render_still.py storyboards/_demo_derivation.yml            # all scenes
    python render_still.py storyboards/_demo_derivation.yml d1         # one scene id
    python render_still.py storyboards/_demo_derivation.yml --idx 0    # by index
"""
import sys
sys.path.insert(0, ".")
from pathlib import Path
from pipeline import _bootstrap
_bootstrap.bootstrap()
import yaml
from manim import Scene, tempconfig, config
from pipeline.templates import build_blocks
from pipeline.visuals import theme as T


def ground_for(scene):
    k = scene.get("kind", "content")
    return "light" if k in ("intro", "outro") else "dark"


def render_scene(meta, scene, out_name):
    ground = ground_for(scene)
    blocks = build_blocks(scene, {"ground": ground, "meta": meta})

    class Still(Scene):
        def construct(self):
            self.camera.background_color = T.color(ground, "bg")
            for b in blocks:
                self.add(b.mobject)

    with tempconfig({"format": "png", "pixel_width": 1920, "pixel_height": 1080,
                     "frame_rate": 1, "disable_caching": True, "verbosity": "ERROR",
                     "media_dir": "output/_still", "output_file": out_name}):
        Still().render()
    # manim writes to output/_still/images/<out_name>.png
    return Path("output/_still/images") / f"{out_name}.png"


def main():
    args = [a for a in sys.argv[1:]]
    sb = Path(args[0])
    data = yaml.safe_load(sb.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    scenes = data.get("scenes", [])
    pick_id = None
    idx = None
    if len(args) > 1:
        if args[1] == "--idx":
            idx = int(args[2])
        else:
            pick_id = args[1]
    stem = sb.stem
    out = []
    for i, sc in enumerate(scenes):
        if pick_id and sc.get("id") != pick_id:
            continue
        if idx is not None and i != idx:
            continue
        name = f"{stem}__{sc.get('id', i)}"
        try:
            p = render_scene(meta, sc, name)
            out.append(str(p))
            print(f"[still] {sc.get('id', i)} -> {p}")
        except Exception as exc:
            import traceback
            print(f"[still] FAIL {sc.get('id', i)}: {exc!r}")
            traceback.print_exc()
    print("DONE", len(out), "still(s)")


if __name__ == "__main__":
    main()

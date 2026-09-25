"""Two-pass loudnorm a Remotion render to the house target (-19 LUFS, TP -1.5 dBTP).

Reuses video/make.py's `_loudnorm_final` (same filter, video stream-copied), so the
Remotion line ships at the same loudness as the Manim line.

    python scripts/loudnorm.py out/act3.mp4 out/act3_final.mp4
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))  # video/
import make  # noqa: E402

src, out = Path(sys.argv[1]), Path(sys.argv[2])
ok, loud = make._loudnorm_final(src, out, "192k", make.HOUSE_LUFS)
if not ok:
    sys.exit(f"[loudnorm] failed: {loud.get('error')}")
print(f"[loudnorm] {out}  I={loud.get('I')} LUFS  TP={loud.get('TP')} dBTP  (target {make.HOUSE_LUFS})")

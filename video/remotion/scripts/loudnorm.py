"""Two-pass loudnorm a Remotion render to the house target (-19 LUFS, TP -1.5 dBTP).

Uses video/pipeline/loudnorm.py's `_loudnorm_final` (same filter, video stream-copied; extracted
verbatim from the Manim-era make.py on 2026-09-28), so the Remotion line ships at the same
loudness the Manim line did.

    python scripts/loudnorm.py out/act3.mp4 out/act3_final.mp4
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # video/  (remotion/scripts/loudnorm.py -> video/)
from pipeline import loudnorm  # noqa: E402

src, out = Path(sys.argv[1]), Path(sys.argv[2])
ok, loud = loudnorm._loudnorm_final(src, out, "192k", loudnorm.HOUSE_LUFS)
if not ok:
    sys.exit(f"[loudnorm] failed: {loud.get('error')}")
print(f"[loudnorm] {out}  I={loud.get('I')} LUFS  TP={loud.get('TP')} dBTP  (target {loudnorm.HOUSE_LUFS})")

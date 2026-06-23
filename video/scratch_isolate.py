import sys
from pathlib import Path
sys.path.insert(0, str(Path(r"c:\Users\Kao\Downloads\Calculus_handout\video\pipeline").resolve().parent))
from pipeline import _bootstrap
_bootstrap.bootstrap()

from manim import MathTex

align_on = "="
tex = "\\sum_{k=1}^n x = 5"
mob = MathTex(tex, substrings_to_isolate=[align_on])

print("len(mob):", len(mob))
for i, m in enumerate(mob):
    print(f"mob[{i}] tex:", getattr(m, 'tex_string', 'N/A'))

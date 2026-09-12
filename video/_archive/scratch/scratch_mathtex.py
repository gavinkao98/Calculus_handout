import sys
from pathlib import Path
sys.path.insert(0, str(Path(r"c:\Users\Kao\Downloads\Calculus_handout\video\pipeline").resolve().parent))
from pipeline import _bootstrap
_bootstrap.bootstrap()

from manim import MathTex

mob1 = MathTex("m ", "=", " 1")
print("mob1 len:", len(mob1))

mob2 = MathTex("", "=", " 1")
print("mob2 len:", len(mob2))
for i, m in enumerate(mob2):
    print(f"mob2[{i}] tex:", getattr(m, 'tex_string', 'N/A'))

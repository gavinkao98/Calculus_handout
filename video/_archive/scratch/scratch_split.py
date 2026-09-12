import sys
from pathlib import Path
sys.path.insert(0, str(Path(r"c:\Users\Kao\Downloads\Calculus_handout\video\pipeline").resolve().parent))
from pipeline import _bootstrap
_bootstrap.bootstrap()

from manim import MathTex

def split_top_level(tex: str, symbol: str):
    depth = 0
    for i, char in enumerate(tex):
        if char == '{': depth += 1
        elif char == '}': depth -= 1
        elif tex[i:i+len(symbol)] == symbol and depth == 0:
            return [tex[:i], tex[i+len(symbol):]]
    return [tex]

align_on = "="
tex = "\\sum_{k=1}^n x = 5"
parts = split_top_level(tex, align_on)
print("parts:", parts)
if len(parts) == 2:
    math_parts = [p for p in (parts[0], align_on, parts[1]) if p]
    mob = MathTex(*math_parts)
    print("len(mob):", len(mob))
    for i, m in enumerate(mob):
        print(f"mob[{i}] tex:", getattr(m, 'tex_string', 'N/A'))

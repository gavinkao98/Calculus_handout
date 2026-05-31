"""Visual assets: Direction B theme (palette/type/layout) + graph sampling.

theme.py is the design system (NTU Calculus Video System, Direction B). The
graph sampling helpers are ported verbatim from the first-generation pipeline.
"""

from . import theme
from .graph_utils import cbrt, safe_eval_expression, sample_function_points

__all__ = ["theme", "cbrt", "safe_eval_expression", "sample_function_points"]

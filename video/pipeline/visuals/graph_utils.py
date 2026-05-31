"""Expression evaluation and sampling utilities for graph scenes.

Ported verbatim from the first-generation pipeline
(``tools/manim_templates/graph_utils.py``) -- same API, same behaviour, just
relocated into the new ``visuals`` package. Supports a restricted, safe
vocabulary of mathematical functions for plotting in graph scenes: expressions
are evaluated in a controlled namespace with no builtins, so a storyboard
author cannot inject arbitrary code through a plot expression.
"""
from __future__ import annotations

import math


def cbrt(x: float) -> float:
    """Cube root that handles negative inputs correctly (unlike ``x ** (1/3)``)."""
    return math.copysign(abs(x) ** (1.0 / 3.0), x)


def safe_eval_expression(expression: str, x: float) -> float:
    namespace = {
        "x": x,
        "math": math,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
        "exp": math.exp,
        "log": math.log,
        "cbrt": cbrt,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
    }
    return float(eval(expression, {"__builtins__": {}}, namespace))


def sample_function_points(
    expression: str,
    x_start: float,
    x_end: float,
    *,
    sample_count: int = 2000,
) -> tuple[list[float], list[float]]:
    if sample_count < 2:
        raise ValueError("sample_count must be at least 2.")

    step = (x_end - x_start) / (sample_count - 1)
    xs: list[float] = []
    ys: list[float] = []
    for index in range(sample_count):
        x = x_start + step * index
        try:
            y = safe_eval_expression(expression, x)
        except Exception:
            continue
        if not math.isfinite(y):
            continue
        xs.append(x)
        ys.append(y)
    return xs, ys

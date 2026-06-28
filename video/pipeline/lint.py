"""Storyboard lint -- catch text that would render as garble, before rendering.

Two failure modes this guards against, both of which shipped as real bugs before
this existed:

  * **Markup in a plain-Text field.** Inline ``$math$`` or a ``\\\\`` line break
    in a field that a template renders with manim ``Text`` (Pango) prints the
    markup *literally* -- the "``$f$``" / "``\\\\``" garble. Templates now route
    prose through ``brand.prose`` and titles through ``brand.heading_rich`` (the
    LaTeX path), so content fields accept markup. The fields checked below are the
    ones that are still plain Text on purpose (the intro/outro brand frames);
    markup there is an error.

  * **An unbalanced ``$``.** An odd number of ``$`` in any string means LaTeX
    either crashes or flips everything after the stray ``$`` into math mode. This
    is checked on *every* string in the storyboard.

This is intentionally a *static* check on the storyboard YAML -- it does not
render. It is the cheap second line of defence; the first is that templates route
markup correctly in the first place.

Run standalone:

    python video/pipeline/lint.py video/storyboards/ch01_inverse_functions.yml

``make.py`` runs it automatically before rendering and aborts on any error
(pass ``--skip-lint`` to bypass).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Meta fields rendered as plain Text by the intro/outro brand frames. Markup in
# these prints literally -- keep them plain prose / labels. (Content scenes route
# their prose + titles through brand.prose / brand.heading_rich, so those accept
# markup and are NOT listed here.)
PLAIN_META_FIELDS = ("chapter", "chapter_title", "section", "title", "tagline")


def _unescaped_dollars(s: str) -> int:
    """Count ``$`` that are not LaTeX-escaped (``\\$``)."""
    count = 0
    i = 0
    while i < len(s):
        if s[i] == "\\":      # skip the escaped char that follows a backslash
            i += 2
            continue
        if s[i] == "$":
            count += 1
        i += 1
    return count


def _has_markup(s: str) -> bool:
    """True if the string carries LaTeX markup (inline math or a backslash command)."""
    return "$" in s or "\\" in s


def _iter_strings(obj, path="") -> "list[tuple[str, str]]":
    """Flatten every string value in the storyboard to (path, value) pairs."""
    out: list[tuple[str, str]] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            out += _iter_strings(v, f"{path}.{k}" if path else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += _iter_strings(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        out.append((path, obj))
    return out


def _snippet(s: str, limit: int = 60) -> str:
    s = s.replace("\n", " ").strip()
    return s if len(s) <= limit else s[: limit - 1] + "…"


# Prose fields (rendered via brand.prose) -- where a manual '\\' break is an
# authoring artifact (brand.prose auto-wraps). Keyed by scene-level field.
_PROSE_SCALARS = ("statement", "takeaway", "qed")
_PROSE_LISTS = ("points", "proof")


def _prose_strings(data: dict) -> "list[tuple[str, str]]":
    out: list[tuple[str, str]] = []
    for si, scene in enumerate(data.get("scenes", []) or []):
        sid = scene.get("id", f"scenes[{si}]")
        for key in _PROSE_SCALARS:
            v = scene.get(key)
            if isinstance(v, str):
                out.append((f"{sid}.{key}", v))
        for key in _PROSE_LISTS:
            for i, v in enumerate(scene.get(key, []) or []):
                if isinstance(v, str):
                    out.append((f"{sid}.{key}[{i}]", v))
        for i, st in enumerate(scene.get("steps", []) or []):
            if isinstance(st, dict) and isinstance(st.get("text"), str):
                out.append((f"{sid}.steps[{i}].text", st["text"]))
        for i, an in enumerate(scene.get("annotations", []) or []):
            t = an.get("text") if isinstance(an, dict) else an
            if isinstance(t, str):
                out.append((f"{sid}.annotations[{i}]", t))
    return out


def _graph_kind(scene: dict) -> "str | None":
    """Effective graph type for a scene: 'focus' (single panel: top-level axes/plots)
    or 'compare' (two panels: left/right) for the `graph` template (dispatch on `mode`),
    else None. (The old graph_focus/graph_compare template names were retired in the
    2026-06-20 cleanup; `graph` + mode is the only form now.)"""
    if scene.get("template") != "graph":
        return None
    return "compare" if str(scene.get("mode", "single")).lower() in (
        "2up", "two-up", "twoup", "compare", "2-up") else "focus"


def _hollow_on_curve(data: dict) -> "list[tuple[str, str]]":
    """Warn for a hollow point that lies (interior) on a plotted curve -- almost
    always an attained value drawn wrong. Endpoints are skipped (a half-open
    domain's excluded endpoint is legitimately hollow)."""
    try:
        from pipeline.visuals.graph_utils import safe_eval_expression
    except Exception:
        return []
    out: list[tuple[str, str]] = []
    for si, scene in enumerate(data.get("scenes", []) or []):
        if _graph_kind(scene) != "focus":
            continue
        sid = scene.get("id", f"scenes[{si}]")
        plots = scene.get("plots", []) or []
        funcs = [p for p in plots if p.get("kind") == "function"]
        axes_xr = (scene.get("axes", {}) or {}).get("x_range")
        for p in plots:
            if p.get("kind") != "point" or not p.get("hollow"):
                continue
            if p.get("hollow_reason"):
                continue  # author declared a legitimate reason (excluded value); not a miss
            try:
                px, py = float(p["point"][0]), float(p["point"][1])
            except Exception:
                continue
            for f in funcs:
                expr = f.get("expression")
                if not expr:
                    continue
                try:
                    fy = safe_eval_expression(expr, px)
                except Exception:
                    continue
                if abs(fy - py) > 0.02:
                    continue
                xr = f.get("x_range") or axes_xr
                interior = True
                if xr and len(xr) >= 2:
                    lo, hi = float(xr[0]), float(xr[1])
                    span = max(abs(hi - lo), 1e-6)
                    interior = abs(px - lo) > 0.03 * span and abs(px - hi) > 0.03 * span
                if interior:
                    out.append(("warn",
                        f"{sid}: hollow point {p['point']} lies on curve '{expr}' "
                        f"(interior) -- if the value is attained it must be SOLID "
                        f"(hollow: false); only an excluded value stays hollow."))
                break
    return out


def _axes_has_ticks(axes: dict) -> bool:
    return isinstance(axes, dict) and (bool(axes.get("x_ticks")) or bool(axes.get("y_ticks")))


def _marks_specific_point(plots) -> bool:
    """A ``kind: point`` at a non-origin coordinate -- the scene is calling out a
    specific value, which a number-less axis leaves unanchored."""
    for p in plots or []:
        if not isinstance(p, dict) or p.get("kind") != "point":
            continue
        try:
            if any(abs(float(c)) > 1e-9 for c in p.get("point", [])):
                return True
        except (TypeError, ValueError):
            continue
    return False


def _quantitative_without_scale(data: dict) -> "list[tuple[str, str]]":
    """Warn: a graph scene marks a specific coordinate (a ``kind: point``) but its
    axes carry no teaching-ticks, so the cited value is not anchored to any readable
    scale -- the deterministic half of "gap A" (DESIGN.md graph "axis ticks: when to
    show"). Either add ``x_ticks``/``y_ticks`` for those values, or confirm the plot
    is purely qualitative (shape only).

    Advisory only: the qualitative/quantitative call is a judgement and the value may
    be carried by a point label, so this never blocks the render. The narration-
    semantic half (a value the narration asks you to read off, with no marker) is left
    to the visual-frame critic's V9 -- a regex over prose is too noisy here. Covers
    graph_focus (top-level axes/plots) and graph_compare (left/right panels)."""
    out: list[tuple[str, str]] = []
    for si, scene in enumerate(data.get("scenes", []) or []):
        gk = _graph_kind(scene)
        if gk == "focus":
            panels = [("", scene.get("axes", {}) or {}, scene.get("plots", []) or [])]
        elif gk == "compare":
            panels = [(f"{k} ", (scene.get(k, {}) or {}).get("axes", {}) or {},
                       (scene.get(k, {}) or {}).get("plots", []) or [])
                      for k in ("left", "right")]
        else:
            continue
        sid = scene.get("id", f"scenes[{si}]")
        for prefix, axes, plots in panels:
            if _axes_has_ticks(axes):
                continue
            if _marks_specific_point(plots):
                out.append(("warn",
                    f"{sid}: {prefix}graph marks a specific point but its axes have "
                    f"no x_ticks/y_ticks -- the coordinate is not anchored to a "
                    f"readable scale. Add teaching-ticks for those values, or confirm "
                    f"it is a qualitative shape plot (DESIGN.md graph 'axis ticks: "
                    f"when to show')."))
    return out


def _example_missing_prompt(data: dict) -> "list[tuple[str, str]]":
    """Warn: a ``derivation`` scene that DEPICTS a handout worked Example (its
    ``source`` descriptor begins with 'Example N.N') but carries no ``prompt:``.

    Such a scene renders with a plain title and NO problem statement on screen, so the
    viewer must infer the task from narration alone -- the exact gap the 2026-06-29
    example-prompt fix closed (ch03 §3.1). A worked example must state its problem; add
    a ``prompt:`` (a short / simplified statement is fine for a long problem), which
    routes the scene through ``_common.example_head`` (``[ EXAMPLE ]`` + problem +
    ``SOLUTION``). Non-example derivations are exempt -- their source does not name an
    Example, and they correctly default to the ``[ derivation ]`` eyebrow. Advisory,
    not an error: it must not abort building a chapter that has not yet been
    backfilled. See DESIGN.md 'Worked-example 題目結構'."""
    out: list[tuple[str, str]] = []
    for si, scene in enumerate(data.get("scenes", []) or []):
        if scene.get("template") != "derivation" or scene.get("prompt"):
            continue
        src = scene.get("source")
        if not isinstance(src, str):
            continue
        desc = src.rsplit(" . ", 1)[-1].strip()   # the content descriptor after the locus
        if re.match(r"Example\s+\d", desc):
            sid = scene.get("id", f"scenes[{si}]")
            out.append(("warn",
                f"{sid}: derivation depicts a handout Example ({_snippet(desc)!r}) but "
                f"has no `prompt:` -- the problem will not appear on screen, only in "
                f"narration. Add a `prompt:` with the problem statement (a simplified "
                f"version is fine for a long problem). See DESIGN.md 'Worked-example 題目結構'."))
    return out


def lint_storyboard(data: dict) -> "list[tuple[str, str]]":
    """Return a list of (severity, message); severity is 'error' or 'warn'.
    'error' aborts the render (broken output); 'warn' is advisory (has rare
    legitimate exceptions)."""
    issues: list[tuple[str, str]] = []
    meta = data.get("meta", {}) or {}

    # -- errors: garble (broken render) --
    for field in PLAIN_META_FIELDS:
        val = meta.get(field)
        if isinstance(val, str) and _has_markup(val):
            issues.append(("error",
                f"meta.{field}: plain-Text field contains LaTeX markup -- it will "
                f"print literally. Remove the $.../\\ or move it to a math field. "
                f"Got: {_snippet(val)!r}"))
    for i, sec in enumerate(meta.get("sections", []) or []):
        if isinstance(sec, dict):
            title = sec.get("title")
            if isinstance(title, str) and _has_markup(title):
                issues.append(("error",
                    f"meta.sections[{i}].title: plain-Text field contains LaTeX "
                    f"markup. Got: {_snippet(title)!r}"))
    for path, value in _iter_strings(data):
        if _unescaped_dollars(value) % 2 == 1:
            issues.append(("error",
                f"{path}: unbalanced '$' ({_unescaped_dollars(value)} unescaped) "
                f"-- LaTeX will crash or flip into math mode. Got: {_snippet(value)!r}"))

    # -- warnings: authoring smells (rare legit exceptions) --
    for path, text in _prose_strings(data):
        if "\\\\" in text:    # two consecutive backslashes == a manual LaTeX break
            issues.append(("warn",
                f"{path}: manual '\\\\' line break in prose -- brand.prose "
                f"auto-wraps at the column width; remove it unless the break is "
                f"deliberate. Got: {_snippet(text)!r}"))
    issues += _hollow_on_curve(data)
    issues += _quantitative_without_scale(data)
    issues += _example_missing_prompt(data)
    return issues


def lint_file(path: Path) -> "list[tuple[str, str]]":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from pipeline import _bootstrap

    _bootstrap.bootstrap()
    import yaml

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return lint_storyboard(data)


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Lint a storyboard for render-garble + authoring smells.")
    parser.add_argument("storyboard", type=Path)
    args = parser.parse_args(argv)

    issues = lint_file(args.storyboard)
    errors = [m for s, m in issues if s == "error"]
    if not issues:
        print(f"[lint] {args.storyboard.name}: clean")
        return 0
    warns = [m for s, m in issues if s == "warn"]
    print(f"[lint] {args.storyboard.name}: {len(errors)} error(s), {len(warns)} warning(s)")
    for sev, msg in issues:
        print(f"  {'ERROR' if sev == 'error' else 'WARN '}  {msg}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

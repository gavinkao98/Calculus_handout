"""Size-consistency guard: stacked sibling prose must render at one size.

Catches a *regression* of the "wrap, don't shrink" rule (DESIGN.md §Text
rendering): if a long prose line in a stacked group -- recap points, proof steps,
graph annotations, example/procedure step text -- gets ``scale_to_fit_width``'d
while its short neighbours don't, they render at visibly different sizes. That
was a real bug (a math-bearing recap point came out smaller than its siblings).
``lint.py`` catches garble; this catches size mismatch.

How it works: build each content scene's blocks (no video render), find the
``brand.prose``-tagged text in each block of a sibling group, and compare their
*scale-aware* font_size. ``brand.prose`` tags its output and never shrinks a
line, so a size gap means something scaled a prose mob after the fact (the
anti-pattern) or rendered one sibling through a different path. Tolerance is
tight because font_size is exact (Text vs Tex normalised by ``TEX_TEXT_SCALE``),
not a noisy height measurement.

Run standalone (checks every content scene):

    python video/pipeline/sizecheck.py video/storyboards/ch01_inverse_functions.yml

``make.py`` runs it on the scenes it is about to render (pass ``--skip-sizecheck``
to bypass).
"""
from __future__ import annotations

import sys
from pathlib import Path

# id prefixes whose blocks are STACKED PROSE SIBLINGS that must share a size.
# (math grids -- math/formula/worked -- and tight curve labels are exempt.)
SIBLING_PREFIXES = ("point", "proof", "step", "annotation", "row")
TOLERANCE = 1.06   # max allowed max/min scale-aware-font_size ratio within a group


def _prose_nodes(mob) -> list:
    """The brand.prose-tagged Text/Tex nodes under *mob* (stops at a tagged node)."""
    if getattr(mob, "_brand_prose", False):
        return [mob]
    out: list = []
    for sub in getattr(mob, "submobjects", []):
        out += _prose_nodes(sub)
    return out


def _norm_size(node, tex_text_scale: float) -> float:
    """font_size normalised so Text and prose Tex are comparable (Tex renders
    smaller per font_size, so prose_tex multiplies by TEX_TEXT_SCALE; undo it)."""
    from manim import MathTex, Tex
    fs = float(node.font_size)
    return fs / tex_text_scale if isinstance(node, (Tex, MathTex)) else fs


def _block_prose_size(block_mob, tex_text_scale: float):
    nodes = _prose_nodes(block_mob)
    if not nodes:
        return None
    # all prose lines in a block share a size; max is robust to a stray tag
    return max(_norm_size(n, tex_text_scale) for n in nodes)


def _overflow_issues(scene: dict, blocks) -> "list[tuple[str, str]]":
    """Layout guard: an element must stay inside the frame (hard) and ideally
    inside the broadcast-safe margin. Catches the "silently spills off-frame"
    class -- an over-wide formula/recap card, a long theorem statement, a
    procedure worked strip, an unclamped headline -- that the prose size check
    (which only compares sibling sizes) cannot see. Full-frame backgrounds and
    grids are deliberately frame-sized, so they are skipped."""
    from pipeline.visuals import theme as T

    sid = scene.get("id")
    safe_x, safe_y = T.FRAME_W / 2 - T.SAFE_MARGIN, T.FRAME_H / 2 - T.SAFE_MARGIN
    frame_x, frame_y = T.FRAME_W / 2, T.FRAME_H / 2
    tol = 0.04
    out: list[tuple[str, str]] = []
    for b in blocks:
        mob = getattr(b, "mobject", None)
        if mob is None:
            continue
        try:
            w, h = float(mob.width), float(mob.height)
        except Exception:  # noqa: BLE001
            continue
        if w <= 1e-6 or h <= 1e-6:
            continue
        if w >= T.FRAME_W - 0.05 and h >= T.FRAME_H - 0.05:
            continue  # full-frame background / grid: intentionally frame-sized
        try:
            left, right = float(mob.get_left()[0]), float(mob.get_right()[0])
            bottom, top = float(mob.get_bottom()[1]), float(mob.get_top()[1])
        except Exception:  # noqa: BLE001
            continue
        if (left < -frame_x - tol or right > frame_x + tol
                or bottom < -frame_y - tol or top > frame_y + tol):
            out.append(("error",
                f"{sid}: block '{b.id}' is clipped by the frame edge "
                f"(x[{left:.2f},{right:.2f}] y[{bottom:.2f},{top:.2f}] vs frame "
                f"+/-{frame_x:.2f}/{frame_y:.2f}) -- it will be cut off; shorten "
                f"it or clamp its width."))
        elif (left < -safe_x - tol or right > safe_x + tol
                or bottom < -safe_y - tol or top > safe_y + tol):
            out.append(("warn",
                f"{sid}: block '{b.id}' spills past the safe margin "
                f"(x[{left:.2f},{right:.2f}] y[{bottom:.2f},{top:.2f}] vs safe "
                f"+/-{safe_x:.2f}/{safe_y:.2f})."))
    return out


def check_scenes(meta: dict, scenes: list[dict]) -> list[str]:
    """Return (severity, message) tuples for the given scenes.
    'error' = stacked-prose size mismatch, or an element clipped off-frame (both
    abort the render); 'warn' = teaching prose in muted, or an element spilling
    past the broadcast-safe margin. Overflow is checked on every scene kind; the
    prose size/muted checks apply to content scenes only."""
    from pipeline.templates import build_blocks
    from pipeline.visuals import theme as T

    muted_hex = str(T.color("dark", "muted")).lower()
    issues: list[tuple[str, str]] = []
    for scene in scenes:
        kind = scene.get("kind", "content")
        ground = "light" if kind in ("intro", "outro") else "dark"
        ctx = {"ground": ground, "meta": meta}
        try:
            blocks = build_blocks(scene, ctx)
        except Exception as exc:  # noqa: BLE001
            issues.append(("error", f"{scene.get('id')}: could not build scene ({exc!r})"))
            continue

        # -- overflow guard (every kind): clipped off-frame, or into safe margin --
        issues += _overflow_issues(scene, blocks)

        # prose size + muted checks are about stacked prose -- content scenes only
        if kind != "content":
            continue

        # -- error: stacked siblings at different sizes (shrunk not wrapped) --
        groups: dict[str, list[tuple[str, float]]] = {}
        for b in blocks:
            prefix = str(b.id).split(".")[0]
            if prefix not in SIBLING_PREFIXES:
                continue
            size = _block_prose_size(b.mobject, T.TEX_TEXT_SCALE)
            if size is not None:
                groups.setdefault(prefix, []).append((b.id, size))
        for prefix, members in groups.items():
            if len(members) < 2:
                continue
            sizes = [s for _, s in members]
            if max(sizes) / min(sizes) > TOLERANCE:
                detail = ", ".join(f"{bid}={s:.1f}" for bid, s in members)
                issues.append(("error",
                    f"{scene.get('id')}: '{prefix}' siblings render at different "
                    f"sizes (>{round((TOLERANCE - 1) * 100)}%) -- a line was shrunk "
                    f"instead of wrapped. Sizes: {detail}"))

        # -- warn: teaching prose rendered in muted (too faint) --
        for b in blocks:
            faint = False
            for node in _prose_nodes(b.mobject):
                try:
                    if node.get_color().to_hex().lower() == muted_hex:
                        faint = True
                        break
                except Exception:
                    continue
            if faint:
                issues.append(("warn",
                    f"{scene.get('id')}: prose '{b.id}' is rendered in muted "
                    f"({muted_hex}) -- teaching content is too faint in muted; "
                    f"use role 'text'/'primary'."))
    return issues


def check_file(path: Path) -> list[str]:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from pipeline import _bootstrap

    _bootstrap.bootstrap()
    import yaml

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return check_scenes(data["meta"], data["scenes"])


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Guard stacked-prose size consistency.")
    parser.add_argument("storyboard", type=Path)
    args = parser.parse_args(argv)

    issues = check_file(args.storyboard)
    errors = [m for s, m in issues if s == "error"]
    if not issues:
        print(f"[sizecheck] {args.storyboard.name}: consistent")
        return 0
    warns = [m for s, m in issues if s == "warn"]
    print(f"[sizecheck] {args.storyboard.name}: {len(errors)} error(s), {len(warns)} warning(s)")
    for sev, msg in issues:
        print(f"  {'SIZE ' if sev == 'error' else 'WARN '}  {msg}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

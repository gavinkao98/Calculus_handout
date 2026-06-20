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
OVERLAP_FRAC = 0.20  # warn when two content blocks intersect over this fraction of the smaller
LABEL_OVERLAP_FRAC = 0.30  # graph equation labels: advisory-only, higher bar than
                           # content blocks -- small text near curves is common, so
                           # only a heavy overlap (two labels truly stacked) warns.


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


def _aabb(mob) -> "tuple[float, float, float, float] | None":
    """Axis-aligned bounding box (x0, x1, y0, y1) in manim units, or None for a
    degenerate/measureless mob. Same accessors _overflow_issues already trusts."""
    try:
        x0, x1 = float(mob.get_left()[0]), float(mob.get_right()[0])
        y0, y1 = float(mob.get_bottom()[1]), float(mob.get_top()[1])
    except Exception:  # noqa: BLE001
        return None
    if x1 - x0 <= 1e-6 or y1 - y0 <= 1e-6:
        return None
    return (x0, x1, y0, y1)


def _box_area(a) -> float:
    return (a[1] - a[0]) * (a[3] - a[2])


def _box_inter(a, b) -> float:
    ix = max(0.0, min(a[1], b[1]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[2], b[2]))
    return ix * iy


def _overlap_issues(scene: dict, blocks) -> "list[tuple[str, str]]":
    """Layout guard: two on-screen CONTENT blocks must not collide.

    Where _overflow_issues checks each block against the frame and the sibling
    check compares fonts, this checks blocks against *each other*. A content
    scene's reveal is additive -- every revealed block stays on screen (see
    scene.py _play_content) -- so the union of all content blocks is the fullest
    final frame, and pairwise AABB intersection there is the worst case. Only
    "content"-layer blocks take part: axes-space graph geometry (coincidence
    intentional), decoration (motifs, column rules, reference guides) and full
    backgrounds are exempt by Block.layer. Occupancy-style overlap detection in
    the spirit of Code2Video's anchor/occupancy table, but kept deterministic and
    continuous -- no grid quantisation. See video/CODE2VIDEO_STUDY.md (P0)."""
    sid = scene.get("id")
    items: list[tuple[str, tuple]] = []
    for b in blocks:
        if getattr(b, "layer", "content") != "content":
            continue
        mob = getattr(b, "mobject", None)
        if mob is None:
            continue
        box = _aabb(mob)
        if box is not None:
            items.append((str(b.id), box))

    out: list[tuple[str, str]] = []
    for i in range(len(items)):
        id_a, a = items[i]
        for j in range(i + 1, len(items)):
            id_b, bx = items[j]
            inter = _box_inter(a, bx)
            if inter <= 0.0:
                continue
            area_a, area_b = _box_area(a), _box_area(bx)
            sm, lg = min(area_a, area_b), max(area_a, area_b)
            if sm <= 1e-9:
                continue
            # Containment: a much larger block almost wholly covering a smaller one
            # is layering (a card behind text, a highlight box), not a clash.
            if inter >= 0.95 * sm and lg > 4.0 * sm:
                continue
            frac = inter / sm
            if frac > OVERLAP_FRAC:
                out.append(("warn",
                    f"{sid}: blocks '{id_a}' and '{id_b}' overlap "
                    f"({frac * 100:.0f}% of the smaller) -- they may collide on "
                    f"screen; reposition or split them."))
    return out


def _graph_labels(mob) -> list:
    """The graph_focus._label-tagged equation labels under *mob* (curve / line /
    point names), recursing into groups. Stops at a tagged node."""
    if getattr(mob, "_graph_label", False):
        return [mob]
    out: list = []
    for sub in getattr(mob, "submobjects", []):
        out += _graph_labels(sub)
    return out


def _graph_label_overlap_issues(scene: dict, blocks) -> "list[tuple[str, str]]":
    """Layout guard for the one collision the graph-layer exemption hides.

    _overlap_issues skips the whole "graph" layer because in-axes coincidence is
    usually intentional (a point on a curve, a guide through an intersection, a
    label hugging its curve -- see Block.layer docstring). But two EQUATION LABELS
    landing on top of each other is a genuine defect, and graph labels are placed
    by a heuristic / hand-tuned ``label_point`` with no collision avoidance. So we
    carve out just the labels (tagged by graph_focus._label, found wherever they
    sit -- a static ``label.N`` block or folded inside a revealed ``plot.N`` group)
    and check them pairwise. Advisory only (``warn``): the fix is a clearer
    ``label_point``, and a render-blocking error here would be too aggressive for a
    small-text heuristic. Covers graph_focus and graph_compare (shared _plot_blocks)."""
    sid = scene.get("id")
    items: list[tuple[str, tuple]] = []
    for b in blocks:
        mob = getattr(b, "mobject", None)
        if mob is None:
            continue
        for lab in _graph_labels(mob):
            box = _aabb(lab)
            if box is not None:
                items.append((str(b.id), box))

    out: list[tuple[str, str]] = []
    for i in range(len(items)):
        id_a, a = items[i]
        for j in range(i + 1, len(items)):
            id_b, bx = items[j]
            inter = _box_inter(a, bx)
            if inter <= 0.0:
                continue
            sm = min(_box_area(a), _box_area(bx))
            if sm <= 1e-9:
                continue
            frac = inter / sm
            if frac > LABEL_OVERLAP_FRAC:
                out.append(("warn",
                    f"{sid}: graph labels '{id_a}' and '{id_b}' overlap "
                    f"({frac * 100:.0f}% of the smaller) -- equation labels collide; "
                    f"give one an explicit label_point to separate them."))
    return out


def _label_region(nx: float, ny: float) -> str:
    """Coarse human-readable region for a frame-fraction centre (origin top-left)."""
    h = "left" if nx < 0.34 else ("right" if nx > 0.66 else "center")
    v = "upper" if ny < 0.34 else ("lower" if ny > 0.66 else "middle")
    return f"{v}-{h}"


def graph_label_geometry(meta: dict, scene: dict) -> "dict | None":
    """Deterministic geometry of a graph scene's equation labels, for the critic's
    VLM context (B.1b). Reuses the SAME _graph_labels machinery as the overlap guard
    so the critic is grounded on exactly what the guard sees.

    Returns ``{"labels": [{id, text, region, box}], "overlaps": [{a, b, pct}]}`` with
    boxes in frame-fraction coords (origin TOP-LEFT, x right, y down -- how the VLM
    reads the rendered image), or ``None`` when the scene is not a graph template, has
    no labels, or fails to build. Offline: builds blocks, no render, no API."""
    if scene.get("template") not in ("graph_focus", "graph_compare", "graph"):
        return None
    from pipeline.templates import build_blocks
    from pipeline.visuals import theme as T

    try:
        blocks = build_blocks(scene, {"ground": "dark", "meta": meta})
    except Exception:  # noqa: BLE001
        return None

    fw, fh = T.FRAME_W, T.FRAME_H
    labels: list[dict] = []
    boxes: list[tuple] = []
    for b in blocks:
        mob = getattr(b, "mobject", None)
        if mob is None:
            continue
        for lab in _graph_labels(mob):
            box = _aabb(lab)
            if box is None:
                continue
            x0, x1, y0, y1 = box
            # manim (origin centre, y up) -> frame fraction (origin top-left, y down)
            nx0, nx1 = (x0 + fw / 2) / fw, (x1 + fw / 2) / fw
            ny0, ny1 = (fh / 2 - y1) / fh, (fh / 2 - y0) / fh
            cx, cy = (nx0 + nx1) / 2, (ny0 + ny1) / 2
            text = str(getattr(lab, "_graph_label_text", "") or "")
            labels.append({"id": str(b.id), "text": text,
                           "region": _label_region(cx, cy),
                           "box": [round(nx0, 2), round(nx1, 2), round(ny0, 2), round(ny1, 2)]})
            boxes.append((str(b.id), text, box))
    if not labels:
        return None

    overlaps: list[dict] = []
    for i in range(len(boxes)):
        id_a, ta, a = boxes[i]
        for j in range(i + 1, len(boxes)):
            id_b, tb, bx = boxes[j]
            inter = _box_inter(a, bx)
            if inter <= 0.0:
                continue
            sm = min(_box_area(a), _box_area(bx))
            if sm <= 1e-9:
                continue
            frac = inter / sm
            if frac > LABEL_OVERLAP_FRAC:
                overlaps.append({"a": ta or id_a, "b": tb or id_b, "pct": round(frac * 100)})
    return {"labels": labels, "overlaps": overlaps}


def check_scenes(meta: dict, scenes: list[dict]) -> list[str]:
    """Return (severity, message) tuples for the given scenes.
    'error' = stacked-prose size mismatch, or an element clipped off-frame (both
    abort the render); 'warn' = teaching prose in muted, an element spilling past
    the broadcast-safe margin, or two content blocks overlapping. Overflow is
    checked on every scene kind; the prose size / muted / overlap checks apply to
    content scenes only."""
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

        # -- warn: two on-screen content blocks colliding. Additive reveal means
        # the union of revealed blocks is the fullest frame; screen-space layout
        # layer only (graph/decoration/background exempt by Block.layer). --
        issues += _overlap_issues(scene, blocks)

        # -- warn: two graph equation labels stacked (the one collision the graph
        # layer exemption above deliberately lets through). --
        issues += _graph_label_overlap_issues(scene, blocks)

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

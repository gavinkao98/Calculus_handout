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

import re
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


def _norm_size(node, text_scale: float) -> float:
    """font_size normalised to the canonical (math-anchored) scale so prose lines are
    comparable. brand renders text at fs(size) * theme.TEXT_SCALE, so divide a prose Tex's
    font_size back out by TEXT_SCALE to recover the canonical size before comparing."""
    from manim import MathTex, Tex
    fs = float(node.font_size)
    return fs / text_scale if isinstance(node, (Tex, MathTex)) else fs


def _block_prose_size(block_mob, text_scale: float):
    from manim import MathTex, Tex, Text

    nodes = _prose_nodes(block_mob)
    if not nodes:
        return None
    # The sibling check guards "a prose line was shrunk not wrapped". After Direction
    # D, inline $math$ in mixed prose (brand._compose) is x-height-matched to the
    # surrounding Times Text -- its CM font_size (~1.61x the Text size) is NOT
    # the TEX_TEXT_SCALE relation _norm_size assumes, so an inline-MathTex run would
    # falsely measure larger than its text siblings. Compare only the carriers
    # _norm_size CAN normalise: Text runs, or a standalone prose_tex Tex line (a
    # shrunk line shrinks these too). A pure inline-math prose line (only MathTex,
    # e.g. a reason rail "$h(0)=h(2)=0$") has no comparable carrier -- skip it rather
    # than mismeasure it against text siblings.
    carriers = [n for n in nodes
                if isinstance(n, Text) or (isinstance(n, Tex) and not isinstance(n, MathTex))]
    if not carriers:
        return None
    # all prose lines in a block share a size; max is robust to a stray tag
    return max(_norm_size(n, text_scale) for n in carriers)


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
        # Decoration / background bleed off-frame by design (the divider's hero curve
        # runs off the right edge; full-frame grounds, ghost numerals, corner motifs),
        # so they are not "content clipped off-frame". Mirrors the layer exemption in
        # _overlap_issues -- but keep "graph" checked: graph / sign_chart rely on this
        # guard for their reactive overflow (DESIGN.md, capacity contract).
        if getattr(b, "layer", "content") in ("decoration", "background"):
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
    """The graph._label-tagged equation labels under *mob* (curve / line /
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
    carve out just the labels (tagged by graph._label, found wherever they
    sit -- a static ``label.N`` block or folded inside a revealed ``plot.N`` group)
    and check them pairwise. Advisory only (``warn``): the fix is a clearer
    ``label_point``, and a render-blocking error here would be too aggressive for a
    small-text heuristic. Covers both graph modes (single / 2up, shared _plot_blocks)."""
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


def graph_label_geometry(meta: dict, scene: dict, scenes_by_id: "dict | None" = None) -> "dict | None":
    """Deterministic geometry of a graph scene's equation labels, for the critic's
    VLM context (B.1b). Reuses the SAME _graph_labels machinery as the overlap guard
    so the critic is grounded on exactly what the guard sees.

    Returns ``{"labels": [{id, text, region, box}], "overlaps": [{a, b, pct}]}`` with
    boxes in frame-fraction coords (origin TOP-LEFT, x right, y down -- how the VLM
    reads the rendered image), or ``None`` when the scene is not a graph template, has
    no labels, or fails to build. Offline: builds blocks, no render, no API."""
    if scene.get("template") != "graph":
        return None
    from pipeline.templates import build_blocks
    from pipeline.visuals import theme as T

    try:
        blocks = build_blocks(scene, {"ground": "dark", "meta": meta, "scenes_by_id": scenes_by_id})
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


def _capacity_issues(scene: dict, blocks) -> "list[tuple[str, str]]":
    """Predictive SPLIT trigger (not reactive like _overflow_issues). Asks: can the
    body content fit the zone at its TIGHTEST pitch? natural_min = sum(row heights) +
    (n-1)*MIN_PITCH, computed PER COLUMN (so a 2-column template -- recap points vs
    cards, procedure steps vs results -- is measured per column, not summed). If even
    at min pitch it exceeds the body zone (the band below the masthead), the scene
    cannot fit one page -> advise splitting into pages (warn, with a page estimate)
    instead of letting it silently spill or squeeze up into the masthead. The per-column
    min pitch (and any reserved bottom band) comes from the template's capacity_meta()
    when it declares one, else the legacy scalar MIN_PITCH -- the SAME source placement
    reads, so audit and layout never drift (capacity contract, DESIGN.md). Runs for any
    template declaring either; today that is the homogeneous chains (derivation,
    definition_math), whose uniform pitch makes natural_min accurate AND whose place_body
    clamp can HIDE overflow from the reactive off-frame check, so a predictive trigger is
    genuinely needed. Heterogeneous templates (theorem / procedure / recap) gain it once
    they declare capacity_meta (L2). Figures (graph / value_table / sign_chart) declare
    neither -- their height is non-linear (a uniform-pitch estimate would over-count their
    mixed gaps and false-positive), so they stay reactive via _overflow_issues."""
    import math
    import sys as _sys
    from pipeline.visuals import theme as T
    from pipeline.templates import REGISTRY

    builder = REGISTRY.get(scene.get("template"))
    if builder is None:
        return []
    mod = _sys.modules.get(builder.__module__)

    # Capacity contract: prefer the template's capacity_meta() (per-column min_pitch + a
    # reserved bottom band) over the legacy scalar MIN_PITCH, so this predictive audit
    # reads the SAME pitch placement does (single source, no drift). Falls back to
    # MIN_PITCH when a module declares no capacity_meta; figure templates declare neither
    # and are skipped (their height is non-linear -- caught reactively by _overflow_issues).
    plans = None
    cap = getattr(mod, "capacity_meta", None)
    if cap is not None:
        try:
            plans = [p for p in cap(scene) if p is not None]
        except Exception:  # noqa: BLE001
            plans = None
    if plans:
        model = plans[0].model
        extra_bottom = max((p.extra_bottom for p in plans), default=0.0)
        default_pitch = next((p.min_pitch for p in plans if p.x_bucket is None),
                             plans[0].min_pitch)
        bucket_pitch = {p.x_bucket: p.min_pitch for p in plans if p.x_bucket is not None}
    else:
        mp = getattr(mod, "MIN_PITCH", None)
        if mp is None:
            return []  # figure template -- not a vertical stack
        model, extra_bottom, default_pitch, bucket_pitch = "stack", 0.0, float(mp), {}

    HEADER = {"eyebrow", "title", "prompt", "solrule", "sollead", "part"}
    header_bottoms = [float(b.mobject.get_bottom()[1]) for b in blocks
                      if b.id in HEADER and getattr(b, "mobject", None) is not None]
    if not header_bottoms:
        return []
    zone_top = min(header_bottoms)
    floor_y = -T.FRAME_H / 2 + T.SAFE_MARGIN     # the frame's own bottom safe margin
    zone_floor = floor_y + extra_bottom          # ... raised by any reserved bottom band
    zone_h = zone_top - zone_floor
    if zone_h <= 0.5:
        return []

    cols: dict[int, list[tuple[float, float]]] = {}
    for b in blocks:
        if getattr(b, "layer", "content") != "content" or b.id in HEADER:
            continue
        mob = getattr(b, "mobject", None)
        if mob is None:
            continue
        try:
            left = float(mob.get_left()[0])
            top, bottom = float(mob.get_top()[1]), float(mob.get_bottom()[1])
        except Exception:  # noqa: BLE001
            continue
        # A block that sits wholly INSIDE the band the template reserved (extra_bottom)
        # IS that reserved content -- counting it as a zone row too would charge it twice:
        # once as the room taken out of the zone, once as a row that must fit what is
        # left. The double charge was invisible while the only pinned element had its own
        # x-bucket (procedure's worked strip is centred), but worked_example's answer band
        # is flush left on SPINE_X, in the step column's own bucket, so every scene with
        # one read as over capacity by roughly the band's own height. "Wholly inside"
        # means BOTH edges: a row that merely spilled down into the band (an over-capacity
        # chain) breaks the bottom edge and is still counted, so the split warn it exists
        # to raise still fires.
        if extra_bottom and top <= zone_floor + 1e-6 and bottom >= floor_y - 1e-6:
            continue
        if top - bottom <= 1e-6:
            continue
        cols.setdefault(round(left), []).append((top, bottom))
    if not cols:
        return []

    if model == "group":
        # centred FIGURE (value_table / sign_chart): one unit whose columns are not
        # independent streams, so the binding height is the COMBINED extent of all content,
        # not the tallest column. Measured -- conservative vs the figure's slightly inset zone.
        allrows = [r for rows in cols.values() for r in rows]
        natural_min = max(t for t, _ in allrows) - min(b for _, b in allrows)
    elif model == "span":
        # fixed-rhythm template: the built rows already sit at their real centre-to-centre
        # pitch, so a column's natural height is its MEASURED extent (max top - min bottom)
        # -- no tightest-pitch estimate, no row-height prediction.
        natural_min = max(max(t for t, _ in rows) - min(b for _, b in rows)
                          for rows in cols.values())
    else:
        # elastic template: placement would expand to fill, so ask whether it fits at the
        # TIGHTEST pitch -- Σ(row heights) + (n-1)*min_pitch, per column.
        natural_min = max(
            sum(t - b for t, b in rows)
            + (len(rows) - 1) * float(bucket_pitch.get(bucket, default_pitch))
            for bucket, rows in cols.items())

    if natural_min > zone_h + 0.15:
        pages = max(2, math.ceil(natural_min / zone_h))
        return [("warn",
            f"{scene.get('id')}: body content needs ~{natural_min:.1f}u at the tightest "
            f"pitch but the zone is only ~{zone_h:.1f}u -- it will not fit on one page. "
            f"Split into ~{pages} pages (each repeating the header + a "
            f"part: {{current, total}} indicator), or trim.")]
    return []


SPARSE_FILL_MIN = 0.35   # G3: single-block content below this fraction of the body zone -> advisory

# ids scene_head (and friends) add above/beside the body zone -- never part of a scene's
# content fill. Mirrors _capacity_issues' local HEADER; kept separate so the two checks
# stay independently readable (no shared-constant refactor for a one-line duplication).
_HEADER_IDS = {"eyebrow", "title", "prompt", "solrule", "sollead", "part"}


def _union_len(spans: "list[tuple[float, float]]") -> float:
    """Total length covered by 1-D (lo, hi) intervals, merging overlaps (so two blocks
    sharing vertical space are not double-counted)."""
    ivals = sorted(s for s in spans if s[1] > s[0])
    total = 0.0
    cur_lo = cur_hi = None
    for lo, hi in ivals:
        if cur_hi is None or lo > cur_hi:
            if cur_hi is not None:
                total += cur_hi - cur_lo
            cur_lo, cur_hi = lo, hi
        else:
            cur_hi = max(cur_hi, hi)
    if cur_hi is not None:
        total += cur_hi - cur_lo
    return total


# G3 (2026-07-05): fill_gap needs n>=2 rows -- a SINGLE prose block (callout string body,
# statement-only definition) has no inter-row gap to open, so a one-liner strands ~half the
# zone (s3.1 frames 11/12/24). Advisory only; `sparse_ok: true` is the author's ack (read
# HERE only -- render never reads it, so it is not a render-behaviour flag).
#
# G3 measurement blind spot (2026-09-13, hook-13-degrees): a hook can append its OWN block
# below `target` that fills the very whitespace this check exists to catch (radians_essential's
# degrees_flatten hook adds a `layer: graph` figure under `body`) -- measuring only `target`'s
# own height missed that fill entirely and reported "sparse" on a scene the hook had just
# filled. So this measures the UNION of vertical coverage, inside the zone, of every block
# except header (title/eyebrow/...), decoration and background layers -- `target` included --
# against the zone height, instead of `target` alone. In the common case (no such extra
# block) `target` sits fully inside the zone by construction of place_body, so the union
# collapses to exactly `target.height` -- the same number this used to compute directly.
def _sparse_issues(scene: dict, blocks) -> "list[tuple[str, str]]":
    from pipeline.visuals import theme as T   # sizecheck has no module-level T (helpers import locally)

    if scene.get("sparse_ok"):
        return []
    tpl = scene.get("template")
    if tpl == "callout" and isinstance(scene.get("body"), str):
        target = "body"
    elif tpl == "definition_math" and scene.get("statement") and not scene.get("math"):
        target = "statement"
    else:
        return []
    title = next((b.mobject for b in blocks if getattr(b, "id", "") == "title"), None)
    mob = next((b.mobject for b in blocks if getattr(b, "id", "") == target), None)
    if title is None or mob is None:
        return []
    zone_top = title.get_bottom()[1] - T.TITLE_GAP
    zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN
    zone_h = max(zone_top - zone_bottom, 1e-6)

    spans: list[tuple[float, float]] = []
    for b in blocks:
        if str(getattr(b, "id", "")) in _HEADER_IDS:
            continue
        if getattr(b, "layer", "content") in ("decoration", "background"):
            continue
        bm = getattr(b, "mobject", None)
        if bm is None:
            continue
        try:
            top, bottom = float(bm.get_top()[1]), float(bm.get_bottom()[1])
        except Exception:  # noqa: BLE001
            continue
        lo, hi = max(bottom, zone_bottom), min(top, zone_top)
        if hi > lo:
            spans.append((lo, hi))
    ratio = _union_len(spans) / zone_h
    if ratio >= SPARSE_FILL_MIN:
        return []
    sid = scene.get("id", "?")
    # Message text kept as "single-block fill" (not renamed to e.g. "content fill") --
    # _selftest_capacity.py's _has_sparse_warn matches this exact substring, and that file
    # is out of this change's scope (sizecheck.py / _selftest_sizecheck.py / DESIGN only).
    return [("warn",
        f"{sid}: single-block fill {ratio:.0%} < {SPARSE_FILL_MIN:.0%} of body zone -- exits: "
        f"(a) bullet the body (list form), (b) merge into a neighbour (scaffold.flag/aside), "
        f"(c) `sparse_ok: true` to accept the calm whitespace")]


def _statement_regime_issues(scene: dict, blocks) -> "list[tuple[str, str]]":
    """G-advisory: a theorem_proof statement that wrapped renders as a full-width BAND instead of the
    compact rail (measure-driven regime, DESIGN "字卡定位"). Reads the BUILT statement block's
    geometry -- a band spans ~CONTENT_W with its left edge on the spine; the rail card hangs narrow on
    the right gutter -- so the advisory reflects the ACTUAL capacity-aware outcome: a scene whose band
    would overflow falls back to rail in build() and correctly gets NO band advisory here, never
    drifting from the layout. Advisory only: the band is a valid outcome; this just flags that a
    wanted-compact-rail statement changed regime, so it can be trimmed to a single line."""
    if scene.get("template") != "theorem_proof":
        return []
    from pipeline.templates._common import SPINE_X, CONTENT_W
    card = next((getattr(b, "mobject", None) for b in blocks
                 if getattr(b, "id", "") == "statement"), None)
    if card is None:
        return []
    try:
        left, w = float(card.get_left()[0]), float(card.width)
    except Exception:  # noqa: BLE001
        return []
    if not (abs(left - SPINE_X) < 0.3 and w > 0.6 * CONTENT_W):   # band: spine-flush + ~full width
        return []
    sid = scene.get("id", "?")
    return [("warn",
        f"{sid}: the statement wrapped, so it renders as a full-width band (not the compact right "
        f"rail); trim it to a single rail line / a rail-width formula to keep the rail, or accept "
        f"the band.")]


def _effective_font_px(node) -> float:
    """The node's TRUE authored on-screen px, recovered from its manim font_size.
    text Tex renders at fs(px)*TEXT_SCALE; pure-math MathTex renders at fs(px)=px*PX_TO_FS.
    CRITICAL: in this manim `Tex` SUBCLASSES `MathTex` (.venv .../tex_mobject.py:227,607), so a
    text Tex IS-A MathTex -- you MUST test `Tex` FIRST, else every text node is mis-typed as
    math (and Step-2's `Tex("x")` assert fails on first run)."""
    from manim import MathTex, Tex
    from pipeline.visuals import theme as T
    fs = float(node.font_size)
    if isinstance(node, Tex):                       # text prose (carries TEXT_SCALE) -- Tex FIRST!
        return fs / (T.TEXT_SCALE * T.PX_TO_FS)
    if isinstance(node, MathTex):                   # pure-math carrier (no TEXT_SCALE)
        return fs / T.PX_TO_FS
    return fs / T.PX_TO_FS  # plain Text (no TEXT_SCALE); confirm against brand if such nodes occur


_FLOOR_EPS = 1e-6  # tolerance for float-boundary false-positives: the clamp lands a held node at
                   # floor ± ~1e-14 (sub-ULP drift from build transforms); 1e-6 absorbs that while
                   # staying far below any real sub-floor gap (genuinely too-small text is ≥ ~1px
                   # below floor, e.g. the 16.9px counterfactual or the 35px-vs-36 probe).


def _floor_findings(scene_id: str, sizes: list, floor: float, enforce: bool) -> "list[tuple[str, str]]":
    """(severity, message) for each (block_id, px) below `floor`. Pure: no manim."""
    sev = "error" if enforce else "warn"
    return [(sev, f"{scene_id}: '{bid}' renders at {px:.1f}px < MIN_FONT_FLOOR {floor:.0f}px "
                  f"-- too small to read (a line shrank below the floor, or an explicit tiny size)")
            for bid, px in sizes if px < floor - _FLOOR_EPS]


def _floor_issues(scene: dict, blocks, enforce: bool) -> "list[tuple[str, str]]":
    """Font-floor check for all _brand_prose nodes in a scene's blocks.

    Unlike _block_prose_size (which skips pure-inline-math single-line carriers for the
    SIBLING ratio check), an absolute floor needs no sibling group -- it includes ALL
    _prose_nodes, the inline-math-only carriers too. Delegates to _floor_findings."""
    from pipeline.visuals import theme as T
    sizes: list[tuple[str, float]] = []
    for b in blocks:
        mob = getattr(b, "mobject", None)
        if mob is None:
            continue
        for node in _prose_nodes(mob):
            sizes.append((str(b.id), _effective_font_px(node)))
    return _floor_findings(scene.get("id"), sizes, T.MIN_FONT_FLOOR, enforce)


# == design-system rules (T3, 2026-09-14) ====================================================
#
# The four LAYOUT rules (_audit/design-template-system/LayoutRules.dc.html `RULES`) and the five
# MATH rules (MathRules.dc.html) were written as design law after the §3.1 rewatch; three of each
# are deterministic enough to be a gate. What landed here, and why the rest did not, is the
# triage table in REVIEW_GATES.md §一 layer 6 / DESIGN.md §設計系統規則.
#
# ALL SIX ARE WARN-DEFAULT. The decks predate the rules, so a rule that errored on day one would
# simply be switched off with --skip-sizecheck; instead each family has an opt-in escalation flag
# (`meta.layout_enforce` for L*, `meta.mathtype_enforce` for M*), shaped after
# pedagogy.assumptions_registry_issues (`sev = "error" if enforce else "warn"`). A section opts in
# when it is clean; only after a section has run a full round enforcing with no false positive
# does changing the DEFAULT come up for discussion (kickoff T3-5).

L1_WEIGHT_RATIO = 1.15     # L1: how much heavier than the conclusion a set-up element must be
                           # before the hierarchy actually reads inverted. Calibrated, not
                           # invented: the rule's own evidence is a conclusion at the rail tier
                           # under a statement card (44/34 = 1.29) and today's payoff tier over
                           # the body tier (62/48 = 1.29), while theorem_proof's `qed` prose
                           # (43 px measured) under its `statement` card (44 px) is a 1 px gap
                           # nobody can see. Below this ratio the two read as the same weight, so
                           # warning would be noise, not a finding.
L2_BAND_FRAC = 1.0 / 3.0   # L2: the "bottom third" the rule names (360 px of 1080)
L2_MIN_FILL = 0.15         # L2: bbox-union coverage of that band below which it reads as dead space
L3_MAIN_W_FRAC = 0.58      # L3: main-content width below which a right column must open (or centre)
L3_CENTER_TOL = 0.6        # L3: |centre x| (manim u) within which narrow content counts as centred
CONCLUSION_IDS = ("result", "qed")   # the block a scene builds for its payoff: derivation /
                                     # worked_example answer band (`result`), theorem_proof (`qed`)


def _type_nodes(mob) -> list:
    """Every type-setting leaf under *mob* (Text / Tex / MathTex), stopping AT each one.

    Deliberately unlike `_prose_nodes`, which only sees nodes `brand.prose` tagged: a scene's
    conclusion is usually a bare `brand.math_line` MathTex (no prose tag), so the whole-tree walk
    is what L1 needs to compare it against the rest of the frame. Scope is kept to the new rules on
    purpose -- widening the EXISTING muted / floor checks to the whole tree is a separate change
    with its own blast radius (kickoff §8)."""
    from manim import MathTex, Tex, Text
    if isinstance(mob, (Tex, MathTex, Text)):
        return [mob]
    out: list = []
    for sub in getattr(mob, "submobjects", []):
        out += _type_nodes(sub)
    return out


def _authored_font_px(node) -> float:
    """The px the node's TYPE was authored at -- the quantity L1 compares.

    NOT `_effective_font_px`, which reads manim's public `font_size` getter
    (`height / initial_height / SCALE_FACTOR_PER_FONT_POINT`). A MathTex built with
    `substrings_to_isolate` -- every `{{...}}` segment and every deck `color_map` hit goes that
    way -- rebuilds its submobjects AFTER `initial_height` was taken, so the getter reads the
    rebuilt height against the un-rebuilt reference: measured 2.1x over on `_demo_tex_parts`'s
    `{{\\lim}} {{\\frac{h+h^2}{h}}}` step (102 px reported for a 48 px row). The `_font_size`
    manim records at construction is the authored value and survives the rebuild, so prefer it.
    The trade-off is that `_font_size` does not follow a later `.scale()`; that is the right call
    here (an authored TIER is what the rule compares) and shrink-after-the-fact is already the
    sibling and floor checks' business.

    Tex FIRST: in this manim `Tex` subclasses `MathTex`, so testing MathTex first mis-types every
    text node as math (same trap `_effective_font_px` documents)."""
    from manim import Tex
    from pipeline.visuals import theme as T
    fs = float(getattr(node, "_font_size", None) or node.font_size)
    return fs / (T.PX_TO_FS * T.TEXT_SCALE) if isinstance(node, Tex) else fs / T.PX_TO_FS


def _block_max_px(block) -> "float | None":
    """The largest authored on-screen px in *block* (None when it sets no type). Max, not min:
    a payoff band carries its equation AND a 26 px mono tag, and the equation is what "heaviest
    element" means."""
    mob = getattr(block, "mobject", None)
    if mob is None:
        return None
    sizes = [_authored_font_px(n) for n in _type_nodes(mob)]
    return max(sizes) if sizes else None


def _body_blocks(blocks) -> list:
    """The blocks that make up a scene's BODY: content and graph layers, minus the masthead.
    Decoration (motifs, column rules, pagers) and backgrounds are not content ink; the header ids
    (title / eyebrow / prompt / ...) are the frame's furniture, not the thing being argued -- an
    h1 title would otherwise be "the heaviest element" in every single scene."""
    return [b for b in blocks
            if getattr(b, "layer", "content") in ("content", "graph")
            and str(getattr(b, "id", "")) not in _HEADER_IDS
            and getattr(b, "mobject", None) is not None]


def _conclusion_weight_issues(scene: dict, blocks, sev: str) -> "list[tuple[str, str]]":
    """L1: the conclusion must be the heaviest type in the frame.

    `assert fs(conclusion) >= max(fs(x) for x in scene.blocks)` from the rule card, with "blocks"
    read as the BODY (see `_body_blocks`). Scenes that build no conclusion block return nothing --
    a definition or a graph has no payoff line to weigh, and inventing one is authoring, not a gate.
    The rule's second half ("and it must carry a semantic colour") is NOT checked here: which role
    counts as semantic is an authoring judgement, and the VISUAL-FRAME rubric already owns it
    (A7 hierarchy/focus for "the payoff is the accented thing", V10 for colour consistency)."""
    body = _body_blocks(blocks)
    concl = [b for b in body if str(b.id) in CONCLUSION_IDS]
    if not concl:
        return []
    concl_px = max((p for p in (_block_max_px(b) for b in concl) if p is not None), default=None)
    if concl_px is None:
        return []
    rest = [(str(b.id), _block_max_px(b)) for b in body if str(b.id) not in CONCLUSION_IDS]
    heavier = [(bid, px) for bid, px in rest
               if px is not None and px > concl_px * L1_WEIGHT_RATIO]
    if not heavier:
        return []
    bid, px = max(heavier, key=lambda t: t[1])
    return [(sev,
        f"{scene.get('id')}: the conclusion renders at {concl_px:.0f}px but '{bid}' renders at "
        f"{px:.0f}px -- the payoff must be the heaviest element on screen (LayoutRules L1); "
        f"lift the conclusion tier or lighten the set-up.")]


def _rect_union_area(rects: "list[tuple[float, float, float, float]]") -> float:
    """Area covered by (x0, x1, y0, y1) boxes, overlaps counted once. Coordinate-compressed
    sweep -- exact for axis-aligned boxes and small n (a scene has a dozen blocks)."""
    if not rects:
        return 0.0
    xs = sorted({x for r in rects for x in (r[0], r[1])})
    total = 0.0
    for i in range(len(xs) - 1):
        x0, x1 = xs[i], xs[i + 1]
        dx = x1 - x0
        if dx <= 0:
            continue
        spans = [(r[2], r[3]) for r in rects if r[0] <= x0 and r[1] >= x1]
        total += dx * _union_len(spans)
    return total


def _bottom_band_issues(scene: dict, blocks, sev: str) -> "list[tuple[str, str]]":
    """L2: the bottom third must not sit empty on the fullest frame.

    A content scene's reveal is additive (same premise `_overlap_issues` rests on), so the union of
    its body blocks IS the fullest frame. Coverage is measured as the BBOX union clipped to the
    band, not real ink: a bbox is always >= the ink inside it, so this over-states fill and can only
    ever under-report -- the direction a warn-default advisory should err in."""
    from pipeline.visuals import theme as T

    body = _body_blocks(blocks)
    if not body:
        return []
    band_top = -T.FRAME_H / 2 + T.FRAME_H * L2_BAND_FRAC
    band_area = T.FRAME_W * T.FRAME_H * L2_BAND_FRAC
    rects: list[tuple[float, float, float, float]] = []
    for b in body:
        box = _aabb(b.mobject)
        if box is None:
            continue
        x0, x1, y0, y1 = box
        lo, hi = max(y0, -T.FRAME_H / 2), min(y1, band_top)
        if hi > lo:
            rects.append((max(x0, -T.FRAME_W / 2), min(x1, T.FRAME_W / 2), lo, hi))
    fill = _rect_union_area(rects) / band_area
    if fill >= L2_MIN_FILL:
        return []
    # Wording note: this message must not contain "band" -- _selftest_theorem_regime._band_warns
    # picks the statement-promotion advisory out of check_scenes' output by matching
    # `sid in msg and "band" in msg.lower()`, so any other warn using that word on a
    # theorem_regime scene reads as a false promotion advisory there.
    return [(sev,
        f"{scene.get('id')}: the bottom third is {fill:.0%} filled (< {L2_MIN_FILL:.0%}) -- the "
        f"frame reads as half-loaded, and that strip is the most visible one in a lecture hall "
        f"(LayoutRules L2); drop the conclusion into it, keep the figure on screen, or pull the "
        f"body down.")]


def _main_width_issues(scene: dict, blocks, sev: str) -> "list[tuple[str, str]]":
    """L3: a narrow main column must either open the right column or move to the centre.

    `if main_width < 0.58 * W: require(aside or centered)`. Main width = the horizontal extent of
    the body blocks; `_common.build_aside` is the right column the rule means (`aside:` in the
    storyboard), and "centred" means the body's own centre sits near x=0 rather than hanging off
    the left spine. Fires often on today's decks by design -- the rule exists because 27 scenes of
    §3.1 never opened an aside and every one of them is left-hung with a dead right margin."""
    from pipeline.visuals import theme as T

    body = _body_blocks(blocks)
    boxes = [box for box in (_aabb(b.mobject) for b in body) if box is not None]
    if not boxes:
        return []
    left, right = min(b[0] for b in boxes), max(b[1] for b in boxes)
    width = right - left
    if width >= L3_MAIN_W_FRAC * T.FRAME_W:
        return []
    if scene.get("aside"):
        return []
    center = (left + right) / 2
    if abs(center) <= L3_CENTER_TOL:
        return []
    return [(sev,
        f"{scene.get('id')}: main content is {width / T.FRAME_W:.0%} of frame width "
        f"(< {L3_MAIN_W_FRAC:.0%}), hangs off centre (centre x={center:+.1f}u) and opens no "
        f"`aside:` -- a narrow column must either put something in the right column or move to the "
        f"centre (LayoutRules L3).")]


# -- math register (MathRules 1-3) ------------------------------------------------------------
#
# These read the STORYBOARD text, not the built mobjects: the rules are about what the author put
# in a math slot, and once LaTeX has set it the prose and the math are indistinguishable glyphs.

_TEXT_MACRO = re.compile(r"\\(?:text|textrm|textit|mbox|operatorname|mathrm|mathop)\*?\s*\{[^{}]*\}")
# `\underbrace{X}_{\text{outer at inner}}`: a word run opening a sub/superscript group is a LABEL
# hung under (or over) the formula, not prose sitting IN the line -- it is already the move the
# rule prescribes (get the words off the line), so M1 skips it.
_SCRIPT_LABEL = re.compile(r"[_^]\s*\{\s*\\(?:text|mbox)\*?\s*\{[^{}]*\}")
_TEX_CMD = re.compile(r"\\[A-Za-z]+\*?|\\[^A-Za-z]")
_MATH_SPAN = re.compile(r"\$[^$]*\$")
_WORD_RUN = re.compile(r"[A-Za-z]{2,}(?:[ \t]+[A-Za-z]{2,})+")
_LETTER_RUN = re.compile(r"(\\?)([A-Za-z]+)")

# Operators / function names that must be set upright, i.e. written as a LaTeX control sequence
# (`\sin`) and not as bare italic letters (`sin`, which sets as the product s*i*n).
_UPRIGHT_OPS = frozenset("""
sin cos tan sec csc cot sinh cosh tanh coth arcsin arccos arctan arcsec arccsc arccot
lim limsup liminf log ln lg exp max min sup inf det gcd deg dim ker arg hom
""".split())


def _is_whole_math_span(s: str) -> bool:
    """The storyboard convention for "this whole field is one display equation": a single
    `$...$` wrapping everything. `brand.prose` and `brand.math_line` both branch on exactly
    this test, so reading it here keeps the audit and the renderer on one definition."""
    s = s.strip()
    return s.startswith("$") and s.endswith("$") and s.count("$") == 2


def _math_fields(scene: dict) -> "list[tuple[str, str]]":
    """(locus, tex) for every storyboard field that renders as a DISPLAY MATH LINE -- the only
    thing MathRules 1 and 3 can be about.

    Not every math-ish field qualifies, and the split follows what the templates actually build:

    * `derivation` / `worked_example` chain rows (`steps[].math`, `result.math`, `check.math`,
      legacy `lines[].tex`) always go to `brand.math_line`, so they always count -- and these are
      the rows that HAVE the reason rail the rule tells you to move the wording into.
    * `definition_math.math[]` also goes to `math_line`, but `math_line` has a documented mixed
      branch: text with several inline `$...$` spans ("if $f(x)=0$ then $x=a$") is set as text-mode
      Tex, which is a prose line, not a math line. Only the display forms count.
    * `theorem_proof.proof[]` goes to `brand.prose`: a row is a display equation only when the
      whole row is one `$...$` span (`prose` routes exactly that case to `math_line`). Its other
      rows are authored prose sentences -- flagging those would be flagging the template for
      working as designed.

    Out of scope entirely: `statement:` (prose that MAY be a formula -- mixing is its documented
    job), graph curve labels (whole-label names, not lines), and `procedure_steps.worked[]`
    (whole-cell captions). Named here so the boundary is reviewable."""
    sid = scene.get("id", "?")
    out: list[tuple[str, str]] = []

    def _add(where: str, entry, *, display_only: bool = False, span_only: bool = False) -> None:
        tex = entry.get("math", entry.get("tex")) if isinstance(entry, dict) else entry
        if not isinstance(tex, str) or not tex.strip():
            return
        if span_only and not _is_whole_math_span(tex):
            return
        if display_only and "$" in tex and not _is_whole_math_span(tex):
            return
        out.append((f"{sid}.{where}", tex))

    for i, st in enumerate(scene.get("steps") or []):
        _add(f"steps[{i}]", st)
    for key in ("result", "check"):
        if scene.get(key) is not None:
            _add(key, scene[key])
    for i, ln in enumerate(scene.get("lines") or []):
        _add(f"lines[{i}]", ln)
    for i, m in enumerate(scene.get("math") or []):
        _add(f"math[{i}]", m, display_only=True)
    for i, p in enumerate(scene.get("proof") or []):
        _add(f"proof[{i}]", p, span_only=True)
    return out


def _reason_fields(scene: dict) -> "list[tuple[str, str]]":
    """(locus, reason) for every annotation-rail field: the `reason` of each chain row."""
    sid = scene.get("id", "?")
    out: list[tuple[str, str]] = []
    rows: list[tuple[str, object]] = [(f"steps[{i}]", st) for i, st in enumerate(scene.get("steps") or [])]
    rows += [(f"lines[{i}]", ln) for i, ln in enumerate(scene.get("lines") or [])]
    rows += [(k, scene.get(k)) for k in ("result", "check")]
    for where, row in rows:
        if isinstance(row, dict) and isinstance(row.get("reason"), str) and row["reason"].strip():
            out.append((f"{sid}.{where}.reason", row["reason"]))
    return out


def _math_register_issues(scene: dict, sev: str) -> "list[tuple[str, str]]":
    """M1: no prose inside a math line -- the explanation belongs in the right rail.

    Two detectors: an explicit `\\text{}` / `\\mbox{}` run, or two or more adjacent multi-letter
    words once the control sequences are stripped (`(chord \\le arc)` -> `(chord   arc)`). Braces
    and sub/superscript markers break adjacency, so `\\frac{dy}{dx}` is not a sentence. A word run
    that OPENS a sub/superscript group is an `\\underbrace` label, not prose in the line
    (`_SCRIPT_LABEL`), and is dropped before either detector runs."""
    out: list[tuple[str, str]] = []
    for where, raw in _math_fields(scene):
        tex = _SCRIPT_LABEL.sub(" ", raw)
        if "\\text{" in tex or "\\mbox{" in tex:
            out.append((sev, f"{where}: a math line carries \\text{{}}/\\mbox{{}} prose -- move the "
                              f"wording to the reason rail and leave the line pure math (MathRules 1)."))
            continue
        bare = _TEX_CMD.sub(" ", tex)
        bare = re.sub(r"[{}$^_&]", "\x00", bare)
        hit = _WORD_RUN.search(bare)
        if hit:
            out.append((sev, f"{where}: a math line carries running prose ({hit.group(0).strip()!r}) "
                              f"-- move the wording to the reason rail (MathRules 1)."))
    return out


def _rail_register_issues(scene: dict, sev: str) -> "list[tuple[str, str]]":
    """M2: the annotation rail speaks ONE register -- all math, or all sans caps, never both.

    A reason mixing `$...$` with bare running words ("write $h=2\\cdot(h/2)$") is the mixed case the
    rule names. A pure-math reason ("$A=x+h$, $B=x$" -- punctuation between spans is not prose) and
    a pure-words reason ("sum-to-product") both pass."""
    out: list[tuple[str, str]] = []
    for where, reason in _reason_fields(scene):
        if "$" not in reason:
            continue
        rest = _MATH_SPAN.sub(" ", reason)
        words = re.findall(r"[A-Za-z]{2,}", rest)
        if words:
            out.append((sev, f"{where}: the rail mixes registers -- math spans plus running words "
                              f"({', '.join(words[:3])}) in one reason; make it all math or all "
                              f"sans caps (MathRules 2)."))
    return out


def _operator_upright_issues(scene: dict, sev: str) -> "list[tuple[str, str]]":
    """M3 (the automatable half): a named operator written as bare letters sets as italic variables.

    `sin x` typesets as s*i*n*x; only `\\sin x` gets the upright roman operator and its spacing.
    Checks the known operator names outside `\\text{}`-family bodies. The FULL upright/italic rule
    (every variable italic, every constant upright) is not decidable from the source and stays with
    the VISUAL-FRAME rubric."""
    out: list[tuple[str, str]] = []
    for where, tex in _math_fields(scene):
        stripped = _TEXT_MACRO.sub(" ", tex)
        bad = sorted({m.group(2) for m in _LETTER_RUN.finditer(stripped)
                      if not m.group(1) and m.group(2) in _UPRIGHT_OPS})
        if bad:
            out.append((sev, f"{where}: operator name(s) {', '.join(bad)} written as bare letters "
                              f"-- they set as italic variables; use \\{bad[0]} so the operator is "
                              f"upright and spaced (MathRules 3)."))
    return out


def check_scenes(meta: dict, scenes: list[dict], deck: "list[dict] | None" = None) -> "list[tuple[str, str]]":
    """Return (severity, message) tuples for the given scenes.
    'error' = stacked-prose size mismatch, or an element clipped off-frame (both
    abort the render); 'warn' = teaching prose in muted, an element spilling past
    the broadcast-safe margin, or two content blocks overlapping. Overflow is
    checked on every scene kind; the prose size / muted / overlap checks apply to
    content scenes only.

    `deck` is the WHOLE storyboard's scene list when `scenes` is a subset (make.py
    --scene): a `carry:` rebuilds the scene it carries from, which may not be among the
    scenes being checked. Defaults to `scenes`."""
    from pipeline.templates import build_blocks
    from pipeline.visuals import theme as T
    from pipeline.schema import reveal_targets

    muted_hex = str(T.color("dark", "muted")).lower()
    scenes_by_id = {s["id"]: s for s in (scenes if deck is None else deck)
                    if isinstance(s, dict) and s.get("id")}
    issues: list[tuple[str, str]] = []
    for scene in scenes:
        kind = scene.get("kind", "content")
        ground = "light" if kind in ("intro", "outro") else "dark"
        ctx = {"ground": ground, "meta": meta, "scenes_by_id": scenes_by_id}
        try:
            blocks = build_blocks(scene, ctx)
        except Exception as exc:  # noqa: BLE001
            issues.append(("error", f"{scene.get('id')}: could not build scene ({exc!r})"))
            continue

        # -- overflow guard (every kind): clipped off-frame, or into safe margin --
        issues += _overflow_issues(scene, blocks)

        # -- error (F9): a {show <target>} naming no built block. schema.py checks
        # {show} SYNTAX only (target existence is explicitly out of its scope); here
        # the blocks are built, so a typo'd target -- silently skipped by the player,
        # then back-filled at scene end (wrong timing, no crash) -- is caught. --
        ids = {str(b.id) for b in blocks}
        for t in reveal_targets(scene.get("say", "")):
            if t and t not in ids:   # bare {show} is a pure beat split -- skip
                issues.append(("error", f"{scene.get('id')}: {{show {t}}} has no matching "
                                        f"block (built ids: {sorted(ids)})"))

        # Same check for `focus[].dim` (pipeline/focus.py): a typo'd id is silently
        # skipped by focus.apply -- the beat plays with nothing dimmed and looks merely
        # "a bit flat", which is exactly the kind of nothing-happened the focus primitive
        # exists to fix. schema.py validates `at` (it can read `say`); ids need the
        # built blocks, so they land here.
        for j, item in enumerate(scene.get("focus") or []):
            if not isinstance(item, dict):
                continue
            for d in item.get("dim") or []:
                if str(d) not in ids:
                    issues.append(("error", f"{scene.get('id')}.focus[{j}].dim {d!r}: no "
                                            f"matching block (built ids: {sorted(ids)})"))
            # `focus[].indicate` (the flash variant): same reasoning, same check.
            for d in item.get("indicate") or []:
                if str(d) not in ids:
                    issues.append(("error", f"{scene.get('id')}.focus[{j}].indicate {d!r}: "
                                            f"no matching block (built ids: {sorted(ids)})"))

        # Same check for `exit:` (scene.py _tail): a typo'd id is skipped there, so the
        # block meant to leave before the cut would simply stay -- no crash, wrong picture.
        # (`carry.block` / `as` are checked while building: templates._apply_carry raises,
        # and the "could not build scene" error above carries its message.)
        for e in scene.get("exit") or []:
            if str(e) not in ids:
                issues.append(("error", f"{scene.get('id')}.exit {e!r}: no matching block "
                                        f"(built ids: {sorted(ids)})"))

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

        # -- warn: content cannot fit one page even at tightest pitch -> split --
        issues += _capacity_issues(scene, blocks)

        # -- warn: single content block strands most of the body zone -> sparse --
        issues += _sparse_issues(scene, blocks)

        # -- warn: a theorem statement long enough to render as a band, not the compact rail --
        issues += _statement_regime_issues(scene, blocks)

        # -- error: stacked siblings at different sizes (shrunk not wrapped) --
        groups: dict[str, list[tuple[str, float]]] = {}
        for b in blocks:
            prefix = str(b.id).split(".")[0]
            if prefix not in SIBLING_PREFIXES:
                continue
            size = _block_prose_size(b.mobject, T.TEXT_SCALE)
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

        # -- font floor: warn (or error when fontfloor_enforce) for prose below MIN_FONT_FLOOR --
        enforce = bool(meta.get("fontfloor_enforce"))
        issues += _floor_issues(scene, blocks, enforce)

        # -- design-system rules (T3): warn-default, opt-in escalation per family --
        layout_sev = "error" if meta.get("layout_enforce") else "warn"
        issues += _conclusion_weight_issues(scene, blocks, layout_sev)   # L1
        issues += _bottom_band_issues(scene, blocks, layout_sev)         # L2
        issues += _main_width_issues(scene, blocks, layout_sev)          # L3
        math_sev = "error" if meta.get("mathtype_enforce") else "warn"
        issues += _math_register_issues(scene, math_sev)                 # M1
        issues += _rail_register_issues(scene, math_sev)                 # M2
        issues += _operator_upright_issues(scene, math_sev)              # M3
    return issues


def check_file(path: Path) -> "list[tuple[str, str]]":
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

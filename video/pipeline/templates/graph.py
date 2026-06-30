"""graph template -- the unified graph engine (single panel + 2-up compare).

One registered template, selected by ``mode``:
  - mode: single  (default) -> one panel   (top-level axes / plots / annotations)
  - mode: 2up    | compare  -> two side-by-side panels (left / right + annotations)

This merges the former graph_focus (single-panel engine) and graph_compare (2-up
wrapper) into one module; those template names + files were retired in the
2026-06-20 old-design cleanup. _build_single is the panel engine (was
graph_focus.build); _build_compare lays out two panels reusing its helpers (was
graph_compare.build). The glow recipe / colours / reveal ids are unchanged.
"""

from __future__ import annotations

import math
from typing import Any

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Axes,
    Circle,
    DashedLine,
    Dot,
    Line,
    Polygon,
    VGroup,
    VMobject,
)

from .. import brand
from ..blocks import Block
from ..visuals import theme as T
from ..visuals.graph_utils import safe_eval_expression
from ._common import motif_corner

_SIDE = {"up": UP, "down": DOWN, "left": LEFT, "right": RIGHT}
_TITLE_GRAPH_GAP = 0.45
_GRAPH_ANNOTATION_GAP = 0.35


def _range(values: list[float] | tuple[float, ...], default_step: float) -> list[float]:
    vals = [float(v) for v in values]
    if len(vals) == 2:
        vals.append(default_step)
    return vals


def _role_color(ground: str, spec: dict[str, Any], default_role: str) -> str:
    if "color" in spec:
        return str(spec["color"])
    return T.color(ground, str(spec.get("color_role", default_role)))


def _fmt_num(v: float) -> str:
    f = float(v)
    return str(int(f)) if f == int(f) else str(f)


def _tick_at_label(item: Any) -> "tuple[float, str]":
    """A tick spec is a bare number or {at, label}. The label defaults to the
    number and is rendered as math, so 'a'/'L' come out italic like the algebra."""
    if isinstance(item, dict):
        at = float(item["at"])
        return at, str(item.get("label", _fmt_num(at)))
    return float(item), _fmt_num(item)


def _axis_ticks(axes: Axes, ac: dict[str, Any], ground: str, plots: list[dict] | None = None):
    """Optional teaching ticks: a few key marks (e.g. a on x, L on y) so an
    otherwise number-less plot keeps a sense of scale. Returns a VGroup to fold
    into the graph group (so it scales with the axes), or None when unused."""
    col = T.color(ground, "text")
    tlen = 0.11
    mobs: list[Any] = []

    # explicit ticks
    x_ticks = list(ac.get("x_ticks", []) or [])
    y_ticks = list(ac.get("y_ticks", []) or [])

    # smart auto ticks from points
    if ac.get("auto_ticks") and plots:
        explicit_x = {float(_tick_at_label(item)[0]) for item in x_ticks}
        explicit_y = {float(_tick_at_label(item)[0]) for item in y_ticks}
        auto_x = set()
        auto_y = set()
        for plot in plots:
            if plot.get("kind") == "point" and "point" in plot:
                auto_x.add(float(plot["point"][0]))
                auto_y.add(float(plot["point"][1]))
        for x in auto_x:
            if x not in explicit_x:
                x_ticks.append(x)
        for y in auto_y:
            if y not in explicit_y:
                y_ticks.append(y)

    for item in x_ticks:
        at, lab = _tick_at_label(item)
        base = axes.x_axis.number_to_point(at)
        mark = Line(base + UP * tlen, base + DOWN * tlen, color=col, stroke_width=2.0)
        text = brand.math_line(lab, ground, role="text", size="math_sm")
        text.next_to(base, DOWN, buff=0.14)
        mobs += [mark, text]
    for item in y_ticks:
        at, lab = _tick_at_label(item)
        base = axes.y_axis.number_to_point(at)
        mark = Line(base + LEFT * tlen, base + RIGHT * tlen, color=col, stroke_width=2.0)
        text = brand.math_line(lab, ground, role="text", size="math_sm")
        text.next_to(base, LEFT, buff=0.14)
        mobs += [mark, text]
    return VGroup(*mobs) if mobs else None


def _add_axis_labels(axes: Axes, ground: str, ac: dict[str, Any]) -> None:
    """Add x/y axis labels near the tips — standard math convention.
    Disable per-scene with ``axis_labels: false`` in the YAML axes block."""
    if ac.get("axis_labels") is False:
        return
    x_lab = brand.math_line("x", ground, role="text", size="math_sm")
    y_lab = brand.math_line("y", ground, role="text", size="math_sm")
    x_lab.next_to(axes.x_axis.get_right(), DOWN, buff=0.1)
    y_lab.next_to(axes.y_axis.get_top(), LEFT, buff=0.1)
    axes.add(x_lab, y_lab)


def _title(text: str, ground: str):
    # Rich ($math$) titles go through brand.heading_rich -- one Tex, so text and
    # math share a baseline and the inline math is sized natively (was a split
    # Text+MathTex glued by arrange(aligned_edge=DOWN), which aligned bbox bottoms
    # not baselines, floating descender-free words and oversizing the math). Graph
    # titles sit at 0.88x h1; fs() takes px, so pass that size back in px units.
    if "$" in text:
        mob = brand.heading_rich(text, ground, role="primary",
                                 size=T.fs("h1") * 0.88 / T.PX_TO_FS)
    else:
        mob = brand.heading(text, ground, role="primary", size="h1")
    max_w = T.FRAME_W - 2 * T.SAFE_MARGIN
    size_px = T._SCALE_PX['h1'] * 0.88 if '$' in text else T._SCALE_PX['h1']
    if mob.width > max_w:
        brand._clamp_shrink(mob, max_w, size_px)
    return mob


def _label(text: str, ground: str, *, role: str = "text", size: str = "label"):
    mob = brand.math_line(text, ground, role=role, size=size) if "$" in text else brand.body_text(
        text, ground, role=role, size=size
    )
    # Tag every curve/line/point equation label so sizecheck can run a
    # label-vs-label overlap advisory: these live on the exempt "graph" layer
    # (intentional coincidence -- a label hugging its curve -- is fine), but two
    # EQUATION LABELS landing on top of each other is a real defect the layer
    # exemption otherwise hides. The 2up (compare) mode reuses _label via _plot_blocks,
    # so both modes are covered by this single tag. The raw text rides along so
    # the critic's deterministic geometry context (sizecheck.graph_label_geometry)
    # can name each label without re-deriving it from the rendered Tex.
    mob._graph_label = True
    mob._graph_label_text = text
    return mob


def _place_function_label(label, graph, axes: Axes, plot: dict[str, Any],
                          xr: list[float], yr: list[float]) -> None:
    if plot.get("label_point") is not None:
        point = plot["label_point"]
        label.move_to(axes.c2p(float(point[0]), float(point[1])), aligned_edge=LEFT)
        return
    side = _SIDE.get(str(plot.get("label_side", "up")).lower(), UP)
    label_x = plot.get("label_x")
    if label_x is not None:
        try:
            label.next_to(axes.input_to_graph_point(float(label_x), graph), side, buff=0.18)
            return
        except Exception:
            pass
    # Default: place near the tail end of the curve
    x_end = float(xr[1])
    y_span = yr[1] - yr[0]
    try:
        y_end = safe_eval_expression(plot["expression"], x_end)
        if math.isfinite(y_end) and yr[0] - y_span <= y_end <= yr[1] + y_span:
            label.next_to(axes.c2p(x_end, y_end), side, buff=0.18)
            return
    except Exception:
        pass
    label.next_to(graph, side, buff=0.13)


def _clipped_function_curve(axes: Axes, expression: str, xr: list[float],
                            y_lo: float, y_hi: float, col: str,
                            stroke_width: float, samples: int) -> VGroup:
    """Sample ``expression`` over ``xr`` and build the curve as one or more
    segments, breaking the path wherever a sample is non-finite (a pole) or
    falls outside ``[y_lo, y_hi]`` (off-frame). This is the asymptote/blow-up
    path for §1.4-style plots ($1/x^2$, $2x/(x-3)$, $\\ln x$): the bare
    ``axes.plot`` lambda crashes on a pole sample (ZeroDivisionError) and draws
    a spurious near-vertical connector across the asymptote, while an
    unclamped excursion to $\\pm\\infty$ blows up the graph bbox and squashes
    the whole figure under _fit_graph_to_safe_zone. Breaking into in-range runs
    fixes all three: the pole becomes a natural gap, and each branch exits
    cleanly at the clip boundary. Opt-in via a plot's ``y_clip`` -- without it
    the original ``axes.plot`` path is unchanged (so §1.1/§1.6 are untouched)."""
    n = max(int(samples), 2)
    step = (xr[1] - xr[0]) / n
    runs: list[list[Any]] = []
    cur: list[Any] = []
    for i in range(n + 1):
        x = xr[0] + step * i
        try:
            y = safe_eval_expression(expression, x)
        except Exception:
            y = None
        if y is None or not math.isfinite(y) or y < y_lo or y > y_hi:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
            continue
        cur.append(axes.c2p(x, y))
    if len(cur) >= 2:
        runs.append(cur)
    segs = VGroup()
    for pts in runs:
        seg = VMobject(stroke_color=col, stroke_width=stroke_width)
        seg.set_points_as_corners(pts)   # dense sampling -> visually smooth, no overshoot past clip
        segs.add(seg)
    return segs


def _plot_blocks(spec: dict[str, Any], axes: Axes, ground: str) -> tuple[list[Block], list[Any]]:
    blocks: list[Block] = []
    labels = []
    ac = spec["axes"]
    x_range = _range(ac["x_range"], 0.5)
    y_range = _range(ac["y_range"], 0.25)
    default_label_size = str(ac.get("label_size", "label"))

    for i, plot in enumerate(spec.get("plots", [])):
        kind = plot.get("kind")
        col = _role_color(ground, plot, "secondary")
        # reveal: true -> dynamic block, waits for {show plot.N}; its label is
        # folded into the same block so one marker reveals both (see docstring).
        static = not bool(plot.get("reveal"))

        if kind == "function":
            xr = _range(plot.get("x_range", x_range[:2]), x_range[2])
            sw = float(plot.get("stroke_width", 5.0))
            samples = int(plot.get("samples", 900))
            y_clip = plot.get("y_clip")
            if y_clip:
                # asymptote / blow-up path: sample + break at poles and off-frame
                # excursions (see _clipped_function_curve). y_clip: true -> axes
                # y_range; y_clip: [lo, hi] -> explicit bound.
                ylo, yhi = (y_range[0], y_range[1]) if y_clip is True else (float(y_clip[0]), float(y_clip[1]))
                graph = _clipped_function_curve(axes, plot["expression"], xr, ylo, yhi, col, sw, samples)
            else:
                step = abs(xr[1] - xr[0]) / float(samples)
                graph = axes.plot(
                    lambda x, expr=plot["expression"]: safe_eval_expression(expr, x),
                    x_range=[xr[0], xr[1], step],
                    color=col,
                    stroke_width=sw,
                )
            glow = graph.copy().set_stroke(col, width=12, opacity=0.24)
            group = VGroup(glow, graph)

            if plot.get("label"):
                # A function-curve label inherits the CURVE's colour by default,
                # so the name reads in the same colour as the curve it marks
                # (e.g. a cyan y=x^3 gets a cyan label, an orange cube root an
                # orange label). `label_role` still overrides. Mirrors the line
                # label below; see DESIGN.md "Plot label colour".
                lab = _label(plot["label"], ground,
                             role=plot.get("label_role", str(plot.get("color_role", "secondary"))),
                             size=plot.get("label_size", default_label_size))
                _place_function_label(lab, graph, axes, plot, xr, y_range)
                if static:
                    labels.append(lab)
                else:
                    group.add(lab)
            blocks.append(Block(f"plot.{i}", group, anim="create", static=static))
            if plot.get("label") and static:
                blocks.append(Block(f"label.{len(labels)-1}", lab, anim="fade", static=True))

        elif kind == "band":
            # Translucent strip across the plotting area -- the epsilon tube
            # (orientation: horizontal, y in [from,to]) or the delta tube
            # (vertical, x in [from,to]). Sits behind the curve/lines, so list it
            # before them in `plots`; folds into the graph group and scales with
            # the axes in _fit_graph_to_safe_zone.
            lo, hi = float(plot["from"]), float(plot["to"])
            if str(plot.get("orientation", "horizontal")).lower().startswith("h"):
                corners = [axes.c2p(x_range[0], lo), axes.c2p(x_range[1], lo),
                           axes.c2p(x_range[1], hi), axes.c2p(x_range[0], hi)]
            else:
                corners = [axes.c2p(lo, y_range[0]), axes.c2p(hi, y_range[0]),
                           axes.c2p(hi, y_range[1]), axes.c2p(lo, y_range[1])]
            band = Polygon(*corners, stroke_width=0, color=col, fill_color=col,
                           fill_opacity=float(plot.get("opacity", 0.14)))
            blocks.append(Block(f"plot.{i}", band, anim="fade", static=static))

        elif kind == "line":
            start = plot["start"]
            end = plot["end"]
            line_cls = DashedLine if plot.get("dashed") else Line
            line = line_cls(
                axes.c2p(float(start[0]), float(start[1])),
                axes.c2p(float(end[0]), float(end[1])),
                color=col,
                stroke_width=float(plot.get("stroke_width", 2.5)),
            )
            line_group = line
            if plot.get("label"):
                # A line label inherits the LINE's colour by default (mirrors the
                # function-curve label, which defaults to the curve colour). The
                # old "warning" default painted every unspecified line label coral
                # red -- so a muted y=x reference line got a jarring red label that
                # fought the de-emphasis it was drawn with. `label_role` still wins.
                lab = _label(plot["label"], ground,
                             role=plot.get("label_role", str(plot.get("color_role", "secondary"))),
                             size=plot.get("label_size", default_label_size))
                if plot.get("label_point") is not None:
                    p = plot["label_point"]
                    lab.move_to(axes.c2p(float(p[0]), float(p[1])), aligned_edge=LEFT)
                else:
                    side = _SIDE.get(str(plot.get("label_side", "up")).lower(), UP)
                    end_pt = plot["end"]
                    lab.next_to(axes.c2p(float(end_pt[0]), float(end_pt[1])), side, buff=0.18)
                if static:
                    labels.append(lab)
                else:
                    line_group = VGroup(line, lab)
            blocks.append(Block(f"plot.{i}", line_group, anim="fade", static=static))
            if plot.get("label") and static:
                blocks.append(Block(f"label.{len(labels)-1}", lab, anim="fade", static=True))

        elif kind == "point":
            point = axes.c2p(float(plot["point"][0]), float(plot["point"][1]))
            radius = float(plot.get("radius", 0.08))
            if plot.get("hollow"):
                dot = Circle(radius=radius, color=col, stroke_width=float(plot.get("stroke_width", 3.5)))
                dot.set_fill(T.color(ground, "bg"), opacity=1.0)
                dot.move_to(point)
            else:
                dot = Dot(point, color=col, radius=radius)
            dot_group = dot
            if plot.get("label"):
                lab = _label(plot["label"], ground, role=plot.get("label_role", "text"),
                             size=plot.get("label_size", default_label_size))
                side = _SIDE.get(str(plot.get("label_side", "up")).lower(), UP)
                lab.next_to(dot, side, buff=0.1)
                if static:
                    labels.append(lab)
                else:
                    dot_group = VGroup(dot, lab)
            blocks.append(Block(f"plot.{i}", dot_group, anim="grow", static=static))
            if plot.get("label") and static:
                blocks.append(Block(f"label.{len(labels)-1}", lab, anim="fade", static=True))

        else:
            raise ValueError(f"Unsupported graph plot kind: {kind!r}")

    return blocks, labels


def _fit_graph_to_safe_zone(graph_group: VGroup, title, annotation_group) -> None:
    """Keep the graph out of the title and bottom annotation zones."""
    zone_top = title.get_bottom()[1] - _TITLE_GRAPH_GAP
    if annotation_group is not None:
        zone_bottom = annotation_group.get_top()[1] + _GRAPH_ANNOTATION_GAP
    else:
        zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.75

    max_h = max(zone_top - zone_bottom, 1.5)
    max_w = T.FRAME_W - 2 * T.SIDE_GUTTER
    scale = min(max_w / graph_group.width, max_h / graph_group.height, 1.0)
    if scale < 1.0:
        graph_group.scale(scale)
    graph_group.move_to([0, (zone_top + zone_bottom) / 2, 0])


def _build_single(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []

    title = _title(spec.get("title", ""), ground)
    # left-anchor the title to the shared spine gutter (was SAFE_MARGIN, ~0.19u
    # further left than every other template -- the graph title visibly jumped left
    # when switching to a graph scene). SIDE_GUTTER == _common.SPINE_X.
    left = -T.FRAME_W / 2 + T.SIDE_GUTTER
    top = T.FRAME_H / 2 - T.SAFE_MARGIN
    title.move_to([left + title.width / 2, top - title.height / 2, 0])
    blocks.append(Block("title", title, anim="fade", static=True))

    ac = {
        "x_range": [-1.45, 1.45, 0.5],
        "y_range": [-0.28, 1.55, 0.25],
        **spec.get("axes", {}),
    }
    axes = Axes(
        x_range=_range(ac.get("x_range", [-1.45, 1.45, 0.5]), 0.5),
        y_range=_range(ac.get("y_range", [-0.28, 1.55, 0.25]), 0.25),
        x_length=float(ac.get("x_length", 6.35)),
        y_length=float(ac.get("y_length", 4.15)),
        tips=False,
        axis_config={
            "color": T.color(ground, "muted"),
            "stroke_width": 2.0,
            "include_ticks": False,
            "include_numbers": False,
        },
    )
    if bool(ac.get("tips", True)):
        axes.x_axis.add_tip(tip_length=0.16, tip_width=0.16)
        axes.y_axis.add_tip(tip_length=0.16, tip_width=0.16)
    axes.move_to([0, -0.2, 0])
    _add_axis_labels(axes, ground, ac)
    blocks.append(Block("axes", axes, anim="create", static=True, layer="graph"))

    plot_blocks, _ = _plot_blocks(spec, axes, ground)
    ticks = _axis_ticks(axes, ac, ground, spec.get("plots", []))
    if ticks is not None:
        plot_blocks.append(Block("ticks", ticks, anim="fade", static=True))
    # Axes-space geometry: coincidence here is intentional (a point sitting on a
    # curve, a coral guide crossing an intersection, a label hugging its curve).
    # Exempt the whole graph group from the screen-space overlap guard; its clash
    # with the title / annotation is already prevented by _fit_graph_to_safe_zone.
    for b in plot_blocks:
        b.layer = "graph"
    blocks.extend(plot_blocks)

    annotations = []
    max_w = T.FRAME_W - 2 * T.SIDE_GUTTER
    for entry in spec.get("annotations", []):
        text = entry.get("text", "") if isinstance(entry, dict) else str(entry)
        # prose() wraps an over-wide annotation instead of shrinking it, so two
        # annotations of different lengths keep the same size (the recap mismatch
        # class). _label stays for the tight curve/point labels.
        # role="text" (not "muted"): an annotation is a teaching takeaway students
        # must read; "muted" is for de-emphasised/retired content, too faint here.
        ann = brand.prose(text, ground, role="text", size="step", max_width=max_w, align="LEFT")
        annotations.append(ann)

    if annotations:
        group = VGroup(*annotations).arrange(DOWN, buff=0.25)
        # +0.55 (was +0.25): the caption sat ~5px above the safe margin, reading as a
        # footer parked on the bottom edge (Codex). Lift it for real breathing room.
        group.move_to([0, -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.55, 0])
    else:
        group = None

    graph_group = VGroup(axes, *[b.mobject for b in plot_blocks])
    _fit_graph_to_safe_zone(graph_group, title, group)

    if group is not None:
        for i, ann in enumerate(annotations):
            blocks.append(Block(f"annotation.{i}", ann, anim="fade", static=False))

    blocks.append(motif_corner(ground))
    return blocks


# ---- 2-up compare (merged from former graph_compare) ----

_PANEL_GAP = 1.2          # air between the two panels
_TITLE_PANEL_GAP = 0.45
_PANEL_CAPTION_GAP = 0.35
_VERDICT = {"ok": ("check", "success"), "bad": ("cross", "warning")}


def _panel(side_spec: dict[str, Any], ground: str, prefix: str) -> tuple[list[Block], VGroup]:
    """Build one panel's axes + plots, ids prefixed left./right. -- reuses the
    single-panel plot machinery, so plot kinds and `reveal: true` behave
    identically to a full-frame graph scene."""
    ac = {
        "x_range": [-1.45, 1.45, 0.5],
        "y_range": [-0.28, 1.55, 0.25],
        **side_spec.get("axes", {}),
    }
    side = dict(side_spec)
    side["axes"] = ac
    axes = Axes(
        x_range=_range(ac["x_range"], 0.5),
        y_range=_range(ac["y_range"], 0.25),
        x_length=float(ac.get("x_length", 4.6)),
        y_length=float(ac.get("y_length", 3.2)),
        tips=False,
        axis_config={
            "color": T.color(ground, "muted"),
            "stroke_width": 2.0,
            "include_ticks": False,
            "include_numbers": False,
        },
    )
    if bool(ac.get("tips", True)):
        axes.x_axis.add_tip(tip_length=0.14, tip_width=0.14)
        axes.y_axis.add_tip(tip_length=0.14, tip_width=0.14)
    _add_axis_labels(axes, ground, ac)

    panel_blocks: list[Block] = [Block("axes", axes, anim="create", static=True)]
    plot_blocks, _ = _plot_blocks(side, axes, ground)
    panel_blocks += plot_blocks
    ticks = _axis_ticks(axes, ac, ground, side_spec.get("plots", []))
    if ticks is not None:
        panel_blocks.append(Block("ticks", ticks, anim="fade", static=True))
    for b in panel_blocks:
        b.id = f"{prefix}.{b.id}"
        b.layer = "graph"
    group = VGroup(*[b.mobject for b in panel_blocks])
    return panel_blocks, group


def _build_compare(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []

    title = _title(spec.get("title", ""), ground)
    # left-anchor to the shared spine gutter (see _build_single) so the 2-up title
    # lines up with every other template's title instead of sitting further left.
    left_edge = -T.FRAME_W / 2 + T.SIDE_GUTTER
    top = T.FRAME_H / 2 - T.SAFE_MARGIN
    title.move_to([left_edge + title.width / 2, top - title.height / 2, 0])
    blocks.append(Block("title", title, anim="fade", static=True))

    content_w = T.FRAME_W - 2 * T.SIDE_GUTTER
    half_w = (content_w - _PANEL_GAP) / 2
    centers = {"left": -(half_w / 2 + _PANEL_GAP / 2), "right": half_w / 2 + _PANEL_GAP / 2}

    # -- bottom annotations (single-panel rules: prose, wraps, never shrinks) --
    annotations = []
    for entry in spec.get("annotations", []):
        text = entry.get("text", "") if isinstance(entry, dict) else str(entry)
        ann = brand.prose(text, ground, role="text", size="step",
                          max_width=content_w, align="LEFT")
        annotations.append(ann)
    ann_group = None
    if annotations:
        ann_group = VGroup(*annotations).arrange(DOWN, buff=0.25)
        ann_group.move_to([0, -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.25, 0])

    # -- captions reserve their band above the annotations --------------------
    captions: dict[str, VGroup] = {}
    cap_h = 0.0
    for key in ("left", "right"):
        side_spec = spec.get(key, {}) or {}
        if not side_spec.get("caption"):
            continue
        cap = brand.prose(side_spec["caption"], ground, role="text", size="step",
                          max_width=half_w - 0.2, align="CENTER")
        verdict = str(side_spec.get("verdict", "")).lower()
        if verdict in _VERDICT:
            # verdict glyph STACKED above the caption, centred under the panel -- it
            # is this panel's punchline and belongs with the graph above it. (The old
            # next_to(cap, RIGHT) floated the mark at the vertical middle of a wrapped
            # 2-line caption, reading as a detached margin glyph.)
            name, vrole = _VERDICT[verdict]
            gm = brand.glyph(name, ground, role=vrole, size="math")
            grp = VGroup(gm, cap).arrange(DOWN, buff=0.2)
        else:
            grp = VGroup(cap)
        captions[key] = grp
        cap_h = max(cap_h, grp.height)

    if ann_group is not None:
        cap_y = ann_group.get_top()[1] + _PANEL_CAPTION_GAP + cap_h / 2
    else:
        cap_y = -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.6 + cap_h / 2  # +0.6 (was +0.3): lift off the bottom edge (Codex)
    for key, grp in captions.items():
        grp.move_to([centers[key], cap_y, 0])

    # -- panels fill the band between title and captions ----------------------
    zone_top = title.get_bottom()[1] - _TITLE_PANEL_GAP
    if captions:
        zone_bottom = cap_y + cap_h / 2 + _PANEL_CAPTION_GAP
    elif ann_group is not None:
        zone_bottom = ann_group.get_top()[1] + _PANEL_CAPTION_GAP
    else:
        zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.75
    zone_h = max(zone_top - zone_bottom, 1.5)

    for key in ("left", "right"):
        side_spec = spec.get(key, {}) or {}
        panel_blocks, group = _panel(side_spec, ground, key)
        scale = min(half_w / group.width, zone_h / group.height, 1.0)
        if scale < 1.0:
            group.scale(scale)
        group.move_to([centers[key], (zone_top + zone_bottom) / 2, 0])
        blocks.extend(panel_blocks)

    for key, grp in captions.items():
        blocks.append(Block(f"caption.{key}", grp, anim="fade", static=False))
    if ann_group is not None:
        for i, ann in enumerate(annotations):
            blocks.append(Block(f"annotation.{i}", ann, anim="fade", static=False))

    blocks.append(motif_corner(ground))
    return blocks


_TWO_UP = {"2up", "two-up", "twoup", "compare", "2-up"}


def graph_mode(spec: dict[str, Any]) -> str:
    """Normalise a graph scene to 'single' or 'compare' (used by the critics too)."""
    return "compare" if str(spec.get("mode", "single")).lower() in _TWO_UP else "single"


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    if graph_mode(spec) == "compare":
        return _build_compare(spec, ctx)
    return _build_single(spec, ctx)

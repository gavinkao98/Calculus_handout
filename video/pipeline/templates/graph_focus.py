"""graph_focus template -- Direction B full-frame plot.

Ports the handoff's B_Graph / ParabolaPlot into Manim primitives:
mixed math title, a centered plot with axes only (no reference gridlines --
grids are disabled project-wide, see theme.SHOW_GRID), glowing cyan function
curves, coral dashed guides, points, math labels, and a bottom annotation reveal.

Point convention (`hollow` flag) -- this is mathematical notation, not styling:
  hollow: false (SOLID ●) -- the value IS attained here (default; intersections,
                            points that lie on the curve).
  hollow: true  (OPEN ○)  -- the value is NOT attained here (excluded endpoint of
                            a half-open domain, a removed point / hole).
Using an open dot for an attained point misleads students -- pick by the math.
"""
from __future__ import annotations

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
    MathTex,
    Polygon,
    Text,
    VGroup,
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


def _axis_ticks(axes: Axes, ac: dict[str, Any], ground: str):
    """Optional teaching ticks: a few key marks (e.g. a on x, L on y) so an
    otherwise number-less plot keeps a sense of scale. Returns a VGroup to fold
    into the graph group (so it scales with the axes), or None when unused."""
    col = T.color(ground, "text")
    tlen = 0.11
    mobs: list[Any] = []
    for item in ac.get("x_ticks", []) or []:
        at, lab = _tick_at_label(item)
        base = axes.x_axis.number_to_point(at)
        mark = Line(base + UP * tlen, base + DOWN * tlen, color=col, stroke_width=2.0)
        text = brand.math_line(lab, ground, role="text", size="math_sm")
        text.next_to(base, DOWN, buff=0.14)
        mobs += [mark, text]
    for item in ac.get("y_ticks", []) or []:
        at, lab = _tick_at_label(item)
        base = axes.y_axis.number_to_point(at)
        mark = Line(base + LEFT * tlen, base + RIGHT * tlen, color=col, stroke_width=2.0)
        text = brand.math_line(lab, ground, role="text", size="math_sm")
        text.next_to(base, LEFT, buff=0.14)
        mobs += [mark, text]
    return VGroup(*mobs) if mobs else None


def _title(text: str, ground: str):
    title_fs = T.fs("h1") * 0.88
    if "$" in text:
        parts = text.split("$")
        mobs = []
        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2:
                # TEX_TEXT_SCALE: same Pango-vs-LaTeX size mismatch as
                # brand.heading_rich -- unscaled, the title's math ran small.
                mobs.append(MathTex(part, color=T.color(ground, "primary"),
                                    font_size=title_fs * T.TEX_TEXT_SCALE))
            else:
                mobs.append(Text(part, font=T.FONT_DISPLAY, font_size=title_fs,
                                 color=T.color(ground, "primary"), weight="SEMIBOLD"))
        mob = VGroup(*mobs).arrange(RIGHT, buff=0.24, aligned_edge=DOWN)
    else:
        mob = brand.heading(text, ground, role="primary", size="h1")
    max_w = T.FRAME_W - 2 * T.SAFE_MARGIN
    if mob.width > max_w:
        mob.scale_to_fit_width(max_w)
    return mob


def _label(text: str, ground: str, *, role: str = "text", size: str = "label"):
    mob = brand.math_line(text, ground, role=role, size=size) if "$" in text else brand.body_text(
        text, ground, role=role, size=size
    )
    return mob


def _place_function_label(label, graph, axes: Axes, plot: dict[str, Any]) -> None:
    if plot.get("label_point") is not None:
        point = plot["label_point"]
        label.move_to(axes.c2p(float(point[0]), float(point[1])), aligned_edge=LEFT)
        return
    side = _SIDE.get(str(plot.get("label_side", "up")).lower(), UP)
    label_x = plot.get("label_x")
    if label_x is not None:
        try:
            label.next_to(axes.input_to_graph_point(float(label_x), graph), side, buff=0.13)
            return
        except Exception:
            pass
    label.next_to(graph, side, buff=0.13)


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

        if kind == "function":
            xr = _range(plot.get("x_range", x_range[:2]), x_range[2])
            step = abs(xr[1] - xr[0]) / float(plot.get("samples", 900))
            graph = axes.plot(
                lambda x, expr=plot["expression"]: safe_eval_expression(expr, x),
                x_range=[xr[0], xr[1], step],
                color=col,
                stroke_width=float(plot.get("stroke_width", 3.5)),
            )
            glow = graph.copy().set_stroke(col, width=12, opacity=0.16)
            group = VGroup(glow, graph)
            blocks.append(Block(f"plot.{i}", group, anim="create", static=True))

            if plot.get("label"):
                lab = _label(plot["label"], ground, role=plot.get("label_role", "primary"),
                             size=plot.get("label_size", default_label_size))
                _place_function_label(lab, graph, axes, plot)
                labels.append(lab)
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
            blocks.append(Block(f"plot.{i}", band, anim="fade", static=True))

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
            blocks.append(Block(f"plot.{i}", line, anim="fade", static=True))

            if plot.get("label"):
                lab = _label(plot["label"], ground, role=plot.get("label_role", "warning"),
                             size=plot.get("label_size", default_label_size))
                if plot.get("label_point") is not None:
                    # Explicit axes point -- for a sloped/diagonal guide, next_to(line,
                    # side) lands on the bbox edge (a y=x label asking for 'up' ended
                    # up pinned to the top of the y-axis). Mirrors the function path.
                    p = plot["label_point"]
                    lab.move_to(axes.c2p(float(p[0]), float(p[1])), aligned_edge=LEFT)
                else:
                    side = _SIDE.get(str(plot.get("label_side", "right")).lower(), RIGHT)
                    lab.next_to(line, side, buff=0.13)
                labels.append(lab)
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
            blocks.append(Block(f"plot.{i}", dot, anim="grow", static=True))

            if plot.get("label"):
                lab = _label(plot["label"], ground, role=plot.get("label_role", "text"),
                             size=plot.get("label_size", default_label_size))
                side = _SIDE.get(str(plot.get("label_side", "up")).lower(), UP)
                lab.next_to(dot, side, buff=0.1)
                labels.append(lab)
                blocks.append(Block(f"label.{len(labels)-1}", lab, anim="fade", static=True))

        else:
            raise ValueError(f"Unsupported graph_focus plot kind: {kind!r}")

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


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []

    title = _title(spec.get("title", ""), ground)
    left = -T.FRAME_W / 2 + T.SAFE_MARGIN
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
            "color": T.color(ground, "text"),
            "stroke_width": 2.0,
            "include_ticks": False,
            "include_numbers": False,
        },
    )
    if bool(ac.get("tips", True)):
        axes.x_axis.add_tip(tip_length=0.16, tip_width=0.16)
        axes.y_axis.add_tip(tip_length=0.16, tip_width=0.16)
    axes.move_to([0, -0.2, 0])
    blocks.append(Block("axes", axes, anim="create", static=True, layer="graph"))

    plot_blocks, _ = _plot_blocks(spec, axes, ground)
    ticks = _axis_ticks(axes, ac, ground)
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
        ann = brand.prose(text, ground, role="text", size="step", max_width=max_w, align="CENTER")
        annotations.append(ann)

    if annotations:
        group = VGroup(*annotations).arrange(DOWN, buff=0.25)
        group.move_to([0, -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.25, 0])
    else:
        group = None

    graph_group = VGroup(axes, *[b.mobject for b in plot_blocks])
    _fit_graph_to_safe_zone(graph_group, title, group)

    if group is not None:
        for i, ann in enumerate(annotations):
            blocks.append(Block(f"annotation.{i}", ann, anim="fade", static=False))

    blocks.append(motif_corner(ground))
    return blocks

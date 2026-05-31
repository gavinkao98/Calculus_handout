"""graph_focus template -- Direction B full-frame plot.

Ports the handoff's B_Graph / ParabolaPlot into Manim primitives:
mixed math title, a centered plot with axes only (no reference gridlines --
grids are disabled project-wide, see theme.SHOW_GRID), glowing cyan function
curves, coral dashed guides, hollow/solid points, math labels, and a bottom
annotation reveal.
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


def _title(text: str, ground: str):
    title_fs = T.fs("h1") * 0.88
    if "$" in text:
        parts = text.split("$")
        mobs = []
        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2:
                mobs.append(MathTex(part, color=T.color(ground, "primary"), font_size=title_fs))
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
                             size=plot.get("label_size", "label"))
                _place_function_label(lab, graph, axes, plot)
                labels.append(lab)
                blocks.append(Block(f"label.{len(labels)-1}", lab, anim="fade", static=True))

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
                             size=plot.get("label_size", "label"))
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
                             size=plot.get("label_size", "label"))
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
    blocks.append(Block("axes", axes, anim="create", static=True))

    plot_blocks, _ = _plot_blocks(spec, axes, ground)
    blocks.extend(plot_blocks)

    annotations = []
    for entry in spec.get("annotations", []):
        text = entry.get("text", "") if isinstance(entry, dict) else str(entry)
        ann = _label(text, ground, role="muted", size="step")
        max_w = T.FRAME_W - 2 * T.SIDE_GUTTER
        if ann.width > max_w:
            ann.scale_to_fit_width(max_w)
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

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from manim_storyboard_workflow import find_scene, load_storyboard, resolve_storyboard_path, to_tex_text
from manim_templates.graph_utils import safe_eval_expression, sample_function_points
from shared_media_paths import DEFAULT_DECK_ID, manim_graph_preview_path
from shared_runtime_bootstrap import REPO_ROOT, ensure_directory


LABEL_OFFSETS = {
    "up": (0, 12, "center", "bottom"),
    "down": (0, -12, "center", "top"),
    "left": (-12, 0, "right", "center"),
    "right": (12, 0, "left", "center"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a fast Matplotlib preview for a graph_focus storyboard scene."
    )
    parser.add_argument("--deck-id", default=DEFAULT_DECK_ID)
    parser.add_argument("--storyboard", type=Path)
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dpi", type=int, default=180)
    parser.add_argument("--sample-count", type=int, default=1200)
    parser.add_argument("--hide-label-anchors", action="store_true")
    return parser.parse_args()


def load_matplotlib():
    if importlib.util.find_spec("matplotlib") is None:
        raise RuntimeError(
            "matplotlib is not installed in the current Python environment. "
            "Install it to use manim_preview_graph_focus.py."
        )

    import matplotlib

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    return plt


def annotate_label(ax, text: str, x: float, y: float, side: str, color: str) -> None:
    dx, dy, ha, va = LABEL_OFFSETS.get(side, LABEL_OFFSETS["up"])
    ax.annotate(
        to_tex_text(text),
        xy=(x, y),
        xytext=(dx, dy),
        textcoords="offset points",
        ha=ha,
        va=va,
        color=color,
        fontsize=10,
    )


def add_plot_label(ax, plot: dict, color: str, show_anchor: bool, axes_x_range: list[float]) -> None:
    label = plot.get("label")
    if not label:
        return

    side = str(plot.get("label_side", "up")).lower()
    anchor_x: float
    anchor_y: float

    if plot["kind"] == "function":
        plot_x_range = plot.get("x_range", axes_x_range)
        anchor_x = float(plot.get("label_x", (plot_x_range[0] + plot_x_range[1]) / 2.0))
        try:
            anchor_y = safe_eval_expression(plot["expression"], anchor_x)
        except Exception:
            xs, ys = sample_function_points(
                plot["expression"],
                float(plot_x_range[0]),
                float(plot_x_range[1]),
                sample_count=200,
            )
            if not xs:
                return
            middle = len(xs) // 2
            anchor_x = xs[middle]
            anchor_y = ys[middle]
    elif plot["kind"] == "line":
        start_x, start_y = plot["start"]
        end_x, end_y = plot["end"]
        if side == "right":
            anchor_x, anchor_y = float(end_x), float(end_y)
        elif side == "left":
            anchor_x, anchor_y = float(start_x), float(start_y)
        else:
            anchor_x = (float(start_x) + float(end_x)) / 2.0
            anchor_y = (float(start_y) + float(end_y)) / 2.0
    else:
        anchor_x, anchor_y = map(float, plot["point"])

    annotate_label(ax, label, anchor_x, anchor_y, side, color)
    if show_anchor:
        ax.scatter([anchor_x], [anchor_y], color=color, s=18, alpha=0.8, zorder=5)


def main() -> int:
    args = parse_args()
    plt = load_matplotlib()

    storyboard_path = resolve_storyboard_path(args.deck_id, args.storyboard)
    storyboard = load_storyboard(storyboard_path)
    scene = find_scene(storyboard, args.scene_id)
    if scene["template"] != "graph_focus":
        raise ValueError(
            f"Scene '{scene['scene_id']}' uses template '{scene['template']}', not graph_focus."
        )

    output_path = (
        args.output
        or manim_graph_preview_path(REPO_ROOT, storyboard["deck_id"], scene["scene_id"])
    ).resolve()
    ensure_directory(output_path.parent)

    axes_cfg = scene["data"]["axes"]
    plots = scene["data"]["plots"]
    annotations = scene["data"]["annotations"]
    show_anchor = not args.hide_label_anchors

    fig, ax = plt.subplots(figsize=(8.4, 5.6))
    ax.set_title(to_tex_text(scene["title"]))
    ax.set_xlim(axes_cfg["x_range"][0], axes_cfg["x_range"][1])
    ax.set_ylim(axes_cfg["y_range"][0], axes_cfg["y_range"][1])
    ax.axhline(0, color="#bbbbbb", linewidth=0.8)
    ax.axvline(0, color="#bbbbbb", linewidth=0.8)
    ax.grid(True, color="#e6e6e6", linewidth=0.8, alpha=0.8)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    for plot in plots:
        color = str(plot.get("color", "#4cc9f0"))
        if plot["kind"] == "function":
            x_range = plot.get("x_range", axes_cfg["x_range"])
            xs, ys = sample_function_points(
                plot["expression"],
                float(x_range[0]),
                float(x_range[1]),
                sample_count=args.sample_count,
            )
            ax.plot(xs, ys, color=color, linewidth=2.0)
        elif plot["kind"] == "line":
            start_x, start_y = plot["start"]
            end_x, end_y = plot["end"]
            ax.plot(
                [start_x, end_x],
                [start_y, end_y],
                color=color,
                linewidth=2.0,
                linestyle="--" if plot.get("dashed") else "-",
            )
        else:
            point_x, point_y = plot["point"]
            ax.scatter([point_x], [point_y], color=color, s=30, zorder=5)

        add_plot_label(ax, plot, color, show_anchor, axes_cfg["x_range"])

    if annotations:
        note_text = "\n".join(f"- {to_tex_text(item['text'])}" for item in annotations)
        fig.subplots_adjust(bottom=0.25)
        fig.text(0.125, 0.04, note_text, ha="left", va="bottom", fontsize=9, color="#555555")

    fig.tight_layout(rect=(0, 0.08 if annotations else 0, 1, 1))
    fig.savefig(output_path, dpi=args.dpi, bbox_inches="tight")
    plt.close(fig)

    print(f"Wrote graph preview to {output_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        raise SystemExit(str(exc))

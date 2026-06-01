"""Demo: natural-language animation cue -> manim animation.

Realizes the storyboard HOOK on `why_square_cannot_invert` (line 120):

    水平線從上方下移掃過 parabola,落到 y=1/4 停住、閃示兩交點 ±1/2、
    各拉虛線回 x 軸。

i.e. a horizontal line sweeps down across g(x)=x^2, lands at y=1/4, flashes the
two intersections at x=±1/2, then drops dashed verticals to the x-axis -- the
"one height, two inputs" reason g can't be inverted on [-1,1].

Reuses the project look (theme palette, CMU fonts via _bootstrap, glow curve,
hollow points) so it sits inside Direction B. Standalone for now; the same body
could become a `hook` fn fired from scene.py.

Run:  .venv\\Scripts\\python video\\demo_hook_hlt.py     (renders 1080p30 mp4)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()

from manim import (  # noqa: E402
    DOWN, RIGHT, UP, Axes, Create, DashedLine, Dot, FadeIn, Flash,
    GrowFromCenter, Line, MathTex, Scene, VGroup, Write, ValueTracker,
    always_redraw, rate_functions,
)

from pipeline import brand  # noqa: E402
from pipeline.visuals import theme as T  # noqa: E402

GROUND = "dark"
Y_HIT = 0.25          # the height the line lands on (y = 1/4)
X_HIT = 0.5           # the two inputs that share it (x = ±1/2)


class HLTSweep(Scene):
    def construct(self) -> None:
        c = lambda role: T.color(GROUND, role)
        self.camera.background_color = c("bg")

        # -- title (top-left, like graph_focus) --
        title = brand.heading_rich(r"Why $g(x)=x^2$ Fails the Line Test", GROUND, size="h1")
        title.move_to([-T.FRAME_W / 2 + T.SAFE_MARGIN + title.width / 2,
                       T.FRAME_H / 2 - T.SAFE_MARGIN - title.height / 2, 0])
        self.play(FadeIn(title), run_time=0.6)

        # -- axes + parabola (Direction B: glow curve, no grid) --
        axes = Axes(
            x_range=[-1.45, 1.45, 0.5], y_range=[-0.28, 1.55, 0.25],
            x_length=7.0, y_length=4.3, tips=False,
            axis_config={"color": c("text"), "stroke_width": 2.0,
                         "include_ticks": False, "include_numbers": False},
        )
        axes.x_axis.add_tip(tip_length=0.16, tip_width=0.16)
        axes.y_axis.add_tip(tip_length=0.16, tip_width=0.16)
        axes.move_to([0, -0.35, 0])

        graph = axes.plot(lambda x: x * x, x_range=[-1.2, 1.2, 0.01],
                          color=c("secondary"), stroke_width=3.5)
        glow = graph.copy().set_stroke(c("secondary"), width=12, opacity=0.16)
        g_label = MathTex(r"g(x)=x^2", color=c("secondary"), font_size=T.fs("label"))
        g_label.next_to(axes.input_to_graph_point(1.12, graph), RIGHT, buff=0.12)

        self.play(Create(axes), run_time=0.8)
        self.play(Create(VGroup(glow, graph)), Write(g_label), run_time=1.1)

        # -- the sweeping horizontal line (ValueTracker drives the height) --
        y_track = ValueTracker(1.45)
        sweep = always_redraw(lambda: Line(
            axes.c2p(-1.32, y_track.get_value()), axes.c2p(1.32, y_track.get_value()),
            color=c("warning"), stroke_width=2.6,
        ))
        self.add(sweep)
        self.play(y_track.animate.set_value(Y_HIT), run_time=2.3,
                  rate_func=rate_functions.ease_in_out_sine)

        # freeze the landing as a dashed guide + label it y = 1/4
        self.remove(sweep)
        dashed = DashedLine(axes.c2p(-1.32, Y_HIT), axes.c2p(1.32, Y_HIT),
                            color=c("warning"), stroke_width=2.6, dash_length=0.12)
        y_lab = MathTex(r"y=\tfrac14", color=c("warning"), font_size=T.fs("label"))
        y_lab.next_to(dashed, RIGHT, buff=0.12)
        self.add(dashed)
        self.play(Write(y_lab), run_time=0.4)

        # -- the two intersections share that height: flash them --
        # SOLID dots: (±1/2, 1/4) are real points on g (g(±1/2)=1/4 exists). A
        # hollow/open dot means "the value is NOT attained here" -- wrong for an
        # attained point, and misleading to a student.
        def mark(x: float) -> Dot:
            return Dot(axes.c2p(x, Y_HIT), color=c("accent"), radius=0.09)

        left_dot, right_dot = mark(-X_HIT), mark(X_HIT)
        self.play(GrowFromCenter(left_dot), GrowFromCenter(right_dot), run_time=0.5)
        self.play(Flash(left_dot, color=c("accent"), line_length=0.18, num_lines=12, flash_radius=0.3),
                  Flash(right_dot, color=c("accent"), line_length=0.18, num_lines=12, flash_radius=0.3),
                  run_time=0.6)

        # -- drop dashed verticals to the x-axis + label x = ±1/2 --
        verticals, xlabels = [], []
        for x, tex in [(-X_HIT, r"-\tfrac12"), (X_HIT, r"\tfrac12")]:
            v = DashedLine(axes.c2p(x, Y_HIT), axes.c2p(x, 0.0),
                           color=c("accent"), stroke_width=2.2, dash_length=0.08)
            lab = MathTex(tex, color=c("accent"), font_size=T.fs("label"))
            lab.next_to(axes.c2p(x, 0.0), DOWN, buff=0.14)
            verticals.append(v)
            xlabels.append(lab)
        self.play(*[Create(v) for v in verticals], *[Write(l) for l in xlabels], run_time=0.9)

        # -- the takeaway --
        ann = brand.prose(
            r"One height $y=\tfrac14$ comes from two inputs $x=\pm\tfrac12$ — so $g$ has no inverse here.",
            GROUND, role="text", size="step", max_width=T.FRAME_W - 2 * T.SIDE_GUTTER,
        )
        ann.move_to([0, -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.2, 0])
        self.play(FadeIn(ann, shift=0.1 * UP), run_time=0.7)
        self.wait(1.4)


def _render() -> Path:
    from manim import tempconfig

    out = Path(__file__).resolve().parent / "output"
    media = out / "_demo_media"
    with tempconfig({
        "pixel_width": 1920, "pixel_height": 1080, "frame_rate": 30,
        "media_dir": str(media), "output_file": "demo_hlt",
        "disable_caching": True, "verbosity": "ERROR",
    }):
        HLTSweep().render()
    hits = sorted(media.rglob("demo_hlt.mp4"), key=lambda p: p.stat().st_mtime)
    return hits[-1] if hits else None


if __name__ == "__main__":
    path = _render()
    print(f"[demo] {path}")

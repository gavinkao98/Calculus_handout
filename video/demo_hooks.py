"""Demo: the remaining storyboard HOOK cues -> manim animations.

One Scene per natural-language cue, all in the Direction B look (theme palette,
CMU fonts via _bootstrap, glow curves, hollow points). Standalone previews; each
body could later become a `hook` fn fired from scene.py.

  cue1  MappingArrows        §why_reverse_needs_one_to_one (L40)
        左 f(x)=x 各輸入射向相異輸出;右 x^2 的 ±1/2 兩箭頭匯聚到 1/4。
  cue3  HLTSideBySide        §horizontal_line_test (L147)
        並排兩圖,各放水平線從上往下 sweep;左圖恆一個交點、右圖兩交點。
  cue4  CompositionRoundtrip §composition_identities (L234)
        x∈A 沿 f 箭頭到 f(x)∈B,再沿 f^{-1} 箭頭走回原 x(回到原位閃一下)。
  cue5  ReflectionYX         §reflection_across_y_equals_x (L254)
        畫 f(x)=x^3、對角虛線 y=x,曲線對 y=x 翻摺生成 ∛x;標 (a,b)→(b,a)。

Run:  .venv\\Scripts\\python video\\demo_hooks.py [all|cue1|cue3|cue4|cue5]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline import _bootstrap  # noqa: E402

_bootstrap.bootstrap()

from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Arrow, Axes, Create, CurvedArrow, DashedLine,
    Dot, Ellipse, FadeIn, Flash, GrowArrow, GrowFromCenter, Indicate, MathTex,
    Scene, TransformFromCopy, VGroup, Write, ValueTracker, always_redraw,
    rate_functions,
)

from pipeline import brand  # noqa: E402
from pipeline.visuals import theme as T  # noqa: E402

GROUND = "dark"


# ----- shared helpers ----------------------------------------------------

def _c(role: str) -> str:
    return T.color(GROUND, role)


def _bg(scene: Scene) -> None:
    scene.camera.background_color = _c("bg")


def _head(scene: Scene, eyebrow: str, title: str):
    """Eyebrow + title block, top-left (mirrors _common.scene_head)."""
    left = -T.FRAME_W / 2 + T.SIDE_GUTTER
    top = T.FRAME_H / 2 - T.SAFE_MARGIN
    eb = brand.eyebrow(eyebrow, GROUND, role="secondary")
    eb.move_to([left + eb.width / 2, top - eb.height / 2, 0])
    ti = brand.heading_rich(title, GROUND, size="h1")
    ti.next_to(eb, DOWN, buff=0.28).align_to(eb, LEFT)
    scene.play(FadeIn(eb), FadeIn(ti), run_time=0.5)
    return VGroup(eb, ti)


def _mark(axes: Axes, x: float, y: float, role: str = "accent", r: float = 0.085) -> Dot:
    """A SOLID point -- marks a value that IS attained (the function value exists
    there). A hollow/open dot means the value is NOT attained (excluded point);
    using it for an attained point is mathematically wrong and misleads students.
    """
    return Dot(axes.c2p(x, y), color=_c(role), radius=r)


def _cbrt(x: float) -> float:
    return (abs(x) ** (1.0 / 3.0)) * (1 if x >= 0 else -1)


def _glow(graph, role: str = "secondary"):
    return graph.copy().set_stroke(_c(role), width=12, opacity=0.16)


# ----- cue 1: mapping arrows (injective vs not) --------------------------

class MappingArrows(Scene):
    def construct(self) -> None:
        _bg(self)
        _head(self, "[ definition ]", "When Can a Process Be Reversed?")

        def panel(cx: float, fn_label: str, pairs, verdict, vrole, converge_to=None):
            din, dout = cx - 1.15, cx + 1.15           # domain / codomain rails
            lab = brand.heading_rich(fn_label, GROUND, role="primary", size="h2")
            lab.move_to([cx, 1.7, 0])
            self.play(FadeIn(lab), run_time=0.3)

            in_dots, out_dots, arrows = [], {}, []
            for (iy, oy, itx, otx) in pairs:
                idot = Dot([din, iy, 0], color=_c("text"), radius=0.07)
                in_dots.append((idot, itx))
                key = round(oy, 3)
                if key not in out_dots:
                    od = Dot([dout, oy, 0], color=_c("text"), radius=0.07)
                    out_dots[key] = (od, otx)
            for d, _t in in_dots:
                self.add(d)
            for od, _t in out_dots.values():
                self.add(od)
            # value labels -- "text" (readable), not "muted" (these are the actual
            # values, teaching content); slightly larger so they read at distance.
            for d, tx in in_dots:
                if tx:
                    m = MathTex(tx, color=_c("text"), font_size=T.fs("math_sm"))
                    m.next_to(d, LEFT, buff=0.14)
                    self.add(m)
            for od, tx in out_dots.values():
                if tx:
                    m = MathTex(tx, color=_c("text"), font_size=T.fs("math_sm"))
                    m.next_to(od, RIGHT, buff=0.14)
                    self.add(m)

            for (iy, oy, _i, _o) in pairs:
                a = Arrow([din + 0.12, iy, 0], [dout - 0.12, oy, 0], buff=0.0,
                          color=_c(vrole), stroke_width=3.0, max_tip_length_to_length_ratio=0.12)
                arrows.append(a)
            self.play(*[GrowArrow(a) for a in arrows], run_time=0.9)

            if converge_to is not None:
                hit = out_dots[round(converge_to, 3)][0]
                self.play(Flash(hit, color=_c("warning"), line_length=0.16,
                                num_lines=12, flash_radius=0.28), run_time=0.6)

            v = brand.prose(verdict, GROUND, role=vrole, size="step", max_width=5.4)
            v.move_to([cx, -1.95, 0])
            self.play(FadeIn(v), run_time=0.4)

        # left: identity, distinct outputs (one-to-one). f(x)=x so each input maps
        # to its own value -- label them 1->1, 2->2, 3->3 to make it concrete.
        panel(-3.45, r"$f(x)=x$",
              [(1.0, 1.0, "1", "1"), (0.0, 0.0, "2", "2"), (-1.0, -1.0, "3", "3")],
              r"distinct inputs $\to$ distinct outputs ($f$ is one-to-one)", "secondary")
        # right: x^2, two inputs collide
        panel(3.45, r"$g(x)=x^2$",
              [(1.0, 0.0, r"\tfrac12", r"\tfrac14"), (-1.0, 0.0, r"-\tfrac12", None)],
              r"two inputs $\to$ one output ($g$ is not)", "warning", converge_to=0.0)
        self.wait(1.2)


# ----- cue 3: horizontal line test, side by side -------------------------

class HLTSideBySide(Scene):
    def construct(self) -> None:
        _bg(self)
        _head(self, "[ example ]", "The Horizontal Line Test")
        y_hit = 0.5

        def panel(cx: float, expr, x_intersections, fn_label, ok: bool):
            axes = Axes(x_range=[-1.35, 1.35, 0.5], y_range=[-0.2, 1.35, 0.25],
                        x_length=4.7, y_length=3.1, tips=False,
                        axis_config={"color": _c("text"), "stroke_width": 1.8,
                                     "include_ticks": False, "include_numbers": False})
            axes.x_axis.add_tip(tip_length=0.13, tip_width=0.13)
            axes.y_axis.add_tip(tip_length=0.13, tip_width=0.13)
            axes.move_to([cx, -0.55, 0])
            graph = axes.plot(expr, x_range=[-1.2, 1.2, 0.01], color=_c("secondary"), stroke_width=3.0)
            lab = MathTex(fn_label, color=_c("secondary"), font_size=T.fs("label"))
            lab.next_to(axes.c2p(1.05, expr(1.05)), RIGHT, buff=0.1)
            self.play(Create(axes), run_time=0.5)
            self.play(Create(VGroup(_glow(graph), graph)), Write(lab), run_time=0.7)
            return axes, graph

        la, lg = panel(-3.5, lambda x: x ** 3 * 0.7 + 0.0, [], r"x^3", True)
        ra, rg = panel(3.5, lambda x: x * x, [], r"x^2", False)

        # shared sweep
        yt = ValueTracker(1.3)
        def sweep(ax):
            return always_redraw(lambda: DashedLine(
                ax.c2p(-1.3, yt.get_value()), ax.c2p(1.3, yt.get_value()),
                color=_c("warning"), stroke_width=2.2, dash_length=0.1))
        sl, sr = sweep(la), sweep(ra)
        self.add(sl, sr)
        self.play(yt.animate.set_value(y_hit), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)

        # left: ONE intersection (x^3*0.7 = 0.5 -> x ~ 0.957); right: TWO (x^2=0.5 -> ±0.707)
        xl = (0.5 / 0.7) ** (1 / 3)
        left_dot = _mark(la, xl, y_hit, role="success", r=0.08)
        right_dots = [_mark(ra, -0.7071, y_hit, role="warning", r=0.08),
                      _mark(ra, 0.7071, y_hit, role="warning", r=0.08)]
        self.play(GrowFromCenter(left_dot), *[GrowFromCenter(d) for d in right_dots], run_time=0.5)
        self.play(*[Indicate(d, color=_c("warning")) for d in right_dots], run_time=0.6)

        # verdicts
        ok = brand.prose(r"always one crossing $\to$ passes", GROUND, role="success", size="step", max_width=5.2)
        bad = brand.prose(r"two crossings $\to$ fails", GROUND, role="warning", size="step", max_width=5.2)
        ok.move_to([-3.5, -2.55, 0])
        bad.move_to([3.5, -2.55, 0])
        self.play(FadeIn(ok), FadeIn(bad), run_time=0.5)
        self.wait(1.2)


# ----- cue 4: composition round-trip -------------------------------------

class CompositionRoundtrip(Scene):
    def construct(self) -> None:
        _bg(self)
        _head(self, "[ proposition ]", "Composition Identities")

        ax, bx = -3.0, 3.0
        A = Ellipse(width=2.7, height=3.6, color=_c("hairline"), stroke_width=2.0).move_to([ax, -0.7, 0])
        B = Ellipse(width=2.7, height=3.6, color=_c("hairline"), stroke_width=2.0).move_to([bx, -0.7, 0])
        la = brand.eyebrow("set a", GROUND, role="muted").next_to(A, UP, buff=0.18)
        lb = brand.eyebrow("set b", GROUND, role="muted").next_to(B, UP, buff=0.18)
        self.play(Create(A), Create(B), FadeIn(la), FadeIn(lb), run_time=0.8)

        def roundtrip(y, src_x, dst_x, src_lbl, dst_lbl, fwd_lbl, bwd_lbl,
                      fwd_role, bwd_role, cap_tex, role):
            src = Dot([src_x, y, 0], color=_c(role), radius=0.08)
            dst = Dot([dst_x, y, 0], color=_c("text"), radius=0.08)
            # label on the OUTER side of each set (A on the left, B on the right)
            src_side = LEFT if src_x < 0 else RIGHT
            dst_side = LEFT if dst_x < 0 else RIGHT
            sl = MathTex(src_lbl, color=_c(role), font_size=T.fs("label")).next_to(src, src_side, buff=0.14)
            dl = MathTex(dst_lbl, color=_c("text"), font_size=T.fs("label")).next_to(dst, dst_side, buff=0.14)
            # arc bulge must follow travel direction, else a right->left round-trip
            # curves the wrong way and the two arrows cross. Same signed angle on
            # both: swapping endpoints flips the bulge, so fwd rides on top, bwd
            # underneath. Colour follows the FUNCTION (f / f^-1), not go/return.
            arc = -0.7 if dst_x > src_x else 0.7
            self.play(GrowFromCenter(src), FadeIn(sl), run_time=0.3)
            fwd = CurvedArrow(src.get_center() + 0.12 * UP, dst.get_center() + 0.12 * UP,
                              angle=arc, color=_c(fwd_role), stroke_width=3.0, tip_length=0.18)
            fl = MathTex(fwd_lbl, color=_c(fwd_role), font_size=T.fs("label")).next_to(fwd, UP, buff=0.05)
            self.play(Create(fwd), FadeIn(fl), GrowFromCenter(dst), FadeIn(dl), run_time=0.7)
            bwd = CurvedArrow(dst.get_center() + 0.12 * DOWN, src.get_center() + 0.12 * DOWN,
                              angle=arc, color=_c(bwd_role), stroke_width=3.0, tip_length=0.18)
            bl = MathTex(bwd_lbl, color=_c(bwd_role), font_size=T.fs("label")).next_to(bwd, DOWN, buff=0.05)
            self.play(Create(bwd), FadeIn(bl), run_time=0.7)
            self.play(Flash(src, color=_c(role), line_length=0.16, num_lines=12, flash_radius=0.28),
                      Indicate(src, color=_c(role)), run_time=0.6)
            cap = brand.prose(cap_tex, GROUND, role=role, size="step", max_width=12.0)
            return cap

        # f is always cyan (secondary), f^-1 always gold (accent) -- in both rows.
        c1 = roundtrip(0.55, ax, bx, r"x", r"f(x)", r"f", r"f^{-1}",
                       "secondary", "accent",
                       r"$f^{-1}(f(x)) = x$ — go and come back to where you started.", "secondary")
        c2 = roundtrip(-1.9, bx, ax, r"y", r"f^{-1}(y)", r"f^{-1}", r"f",
                       "accent", "secondary",
                       r"$f(f^{-1}(y)) = y$ — and the same the other way.", "accent")
        grp = VGroup(c1, c2).arrange(DOWN, buff=0.2).move_to([0, -3.05, 0])
        self.play(FadeIn(c1), run_time=0.4)
        self.play(FadeIn(c2), run_time=0.4)
        self.wait(1.2)


# ----- cue 5: reflection across y = x ------------------------------------

class ReflectionYX(Scene):
    def construct(self) -> None:
        _bg(self)
        _head(self, "[ example ]", r"Reflection Across $y=x$")

        axes = Axes(x_range=[-1.6, 1.6, 0.5], y_range=[-1.6, 1.6, 0.5],
                    x_length=5.0, y_length=5.0, tips=False,
                    axis_config={"color": _c("text"), "stroke_width": 1.8,
                                 "include_ticks": False, "include_numbers": False})
        axes.x_axis.add_tip(tip_length=0.14, tip_width=0.14)
        axes.y_axis.add_tip(tip_length=0.14, tip_width=0.14)
        axes.move_to([0.4, -0.45, 0])
        self.play(Create(axes), run_time=0.6)

        cube = axes.plot(lambda x: x ** 3, x_range=[-1.45, 1.45, 0.01], color=_c("secondary"), stroke_width=3.2)
        cube_g = VGroup(_glow(cube, "secondary"), cube)
        cube_lbl = MathTex(r"f(x)=x^3", color=_c("secondary"), font_size=T.fs("label"))
        cube_lbl.next_to(axes.input_to_graph_point(1.05, cube), LEFT, buff=0.22)
        self.play(Create(cube_g), Write(cube_lbl), run_time=1.0)

        diag = DashedLine(axes.c2p(-1.5, -1.5), axes.c2p(1.5, 1.5),
                          color=_c("muted"), stroke_width=2.0, dash_length=0.12)
        diag_lbl = MathTex(r"y=x", color=_c("muted"), font_size=T.fs("label"))
        diag_lbl.move_to(axes.c2p(-1.05, -0.72))
        self.play(Create(diag), FadeIn(diag_lbl), run_time=0.7)

        # marked point (a,b) on cube and its reflection (b,a)
        a = 0.85
        b = a ** 3
        # solid (points on the curves exist); white so they read on their own-
        # colour curve -- the labels below keep the cyan/gold curve association.
        P = _mark(axes, a, b, role="primary", r=0.08)
        Pp = _mark(axes, b, a, role="primary", r=0.08)
        P_lbl = MathTex(r"(a,b)", color=_c("secondary"), font_size=T.fs("label")).next_to(P, DOWN + RIGHT, buff=0.1)
        Pp_lbl = MathTex(r"(b,a)", color=_c("accent"), font_size=T.fs("label")).next_to(Pp, UP + LEFT, buff=0.1)
        self.play(GrowFromCenter(P), FadeIn(P_lbl), run_time=0.4)

        # reflect the curve across y = x -> cube root branch
        cbrt = axes.plot(_cbrt, x_range=[-1.5, 1.5, 0.01], color=_c("accent"), stroke_width=3.2)
        cbrt_g = VGroup(_glow(cbrt, "accent"), cbrt)
        cbrt_lbl = MathTex(r"f^{-1}(x)=\sqrt[3]{x}", color=_c("accent"), font_size=T.fs("label"))
        cbrt_lbl.next_to(axes.input_to_graph_point(1.35, cbrt), RIGHT, buff=0.18)
        tie = DashedLine(P.get_center(), Pp.get_center(), color=_c("muted"), stroke_width=1.6, dash_length=0.07)
        self.play(TransformFromCopy(cube_g, cbrt_g), run_time=1.4)
        self.play(Create(tie), GrowFromCenter(Pp), FadeIn(Pp_lbl), FadeIn(cbrt_lbl), run_time=0.8)

        cap = brand.prose(r"Reflecting $y=x^3$ across $y=x$ gives its inverse $\sqrt[3]{x}$; each $(a,b)$ becomes $(b,a)$.",
                          GROUND, role="text", size="step", max_width=T.FRAME_W - 2 * T.SIDE_GUTTER)
        cap.move_to([0, -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.2, 0])
        self.play(FadeIn(cap, shift=0.1 * UP), run_time=0.6)
        self.wait(1.2)


SCENES = {"cue1": MappingArrows, "cue3": HLTSideBySide,
          "cue4": CompositionRoundtrip, "cue5": ReflectionYX}


def _render(name: str) -> Path:
    from manim import tempconfig

    media = Path(__file__).resolve().parent / "output" / "_demo_media"
    out_name = f"demo_{name}"
    with tempconfig({
        "pixel_width": 1920, "pixel_height": 1080, "frame_rate": 30,
        "media_dir": str(media), "output_file": out_name,
        "disable_caching": True, "verbosity": "ERROR",
    }):
        SCENES[name]().render()
    hits = sorted(media.rglob(f"{out_name}.mp4"), key=lambda p: p.stat().st_mtime)
    return hits[-1] if hits else None


if __name__ == "__main__":
    import traceback

    argv = sys.argv[1:] or ["all"]
    names = list(SCENES) if argv == ["all"] else argv
    for n in names:
        print(f"[demo] rendering {n} ...", flush=True)
        try:
            p = _render(n)
            print(f"[demo] {n} -> {p}", flush=True)
        except Exception as exc:  # noqa: BLE001
            print(f"[demo] FAIL {n}: {exc!r}", flush=True)
            traceback.print_exc()

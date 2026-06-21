"""sign_chart template -- Direction D (dark teaching frame).

The workhorse of the derivative-application sections: a number line with
critical points, and signed interval rows beneath it -- f' sign ->
f increasing/decreasing (Monotonicity), later the full f'/f'' curve-sketching
chart. SCHEMATIC, not to scale: critical points are equally spaced.

Layout:
  eyebrow + title (scene_head; `kicker` override supported);
  optional centred prose `statement`;
  a horizontal number line with arrow tips both ends; each critical point is
  a tick with its math label beneath (`excluded: true` renders a hollow ring
  instead -- the value-absent convention, e.g. a vertical asymptote);
  below the line, one row per `rows` entry: a row label at the left ($f'$,
  $f$) and one mark per interval -- len(points)+1 marks, centred between
  ticks; faint vertical guides drop from each tick through the rows;
  the statement + chart centre vertically as one group.

Marks auto-colour by sign semantics: "+" -> success (green), "-" -> warning
(coral), anything else ("0", "\\nearrow", "DNE") -> text. Dict form
overrides: { tex: "\\nearrow", role: success }.

Reveal: line / ticks / labels / row labels / guides are static frame; each
mark waits for {show mark.R.I} (row R, interval I) -- the narration walks
the chart interval by interval.

YAML shape:
  template: sign_chart
  accent: procedure
  title: "Where is $f$ increasing?"
  statement: "$f(x)=x^3-3x$, so $f'(x)=3(x-1)(x+1)$."   # optional
  points: ["-1", "1"]              # or { label: "0", excluded: true }
  rows:
    - { label: "f'(x)", marks: ["+", "-", "+"] }
    - { label: "f", marks: [{ tex: "\\nearrow", role: success },
                            { tex: "\\searrow", role: warning },
                            { tex: "\\nearrow", role: success }] }
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, DoubleArrow, LEFT, Line, VGroup

from .. import brand
from ..blocks import Block
from ..visuals import theme as T
from ._common import scene_head, motif_corner

_TICK = 0.13
_ROW_GAP = 0.55       # air between mark rows (real-height cursor)
_FIRST_ROW_DROP = 0.95  # line y -> first mark-row centre

# No capacity_meta: sign_chart stays REACTIVE-only (like graph). Its number line is the
# chart's top edge but renders on layer="graph" (excluded from the content measurement),
# so a predictive group-span would read only the mark rows and miss the line + point
# labels above them -- an under-measure not worth a fragile fixed offset. Mark-row overflow
# is caught by _overflow_issues; an over-wide chart is an authoring error it also catches.

_SIGN_ROLE = {"+": "success", "-": "warning"}


def _mark_mob(entry: Any, ground: str):
    if isinstance(entry, dict):
        tex, mrole = str(entry["tex"]), str(entry.get("role", "text"))
    else:
        tex = str(entry)
        mrole = _SIGN_ROLE.get(tex.strip(), "text")
    # 64px, a step above the "math" role: a sign / arrow glyph is intrinsically
    # small, and the marks ARE this scene's content (first-render finding).
    m = brand.math_line(tex, ground, role=mrole, size=64)
    # a + / - sign gets a soft same-colour glow (green/red); arrows stay crisp.
    if tex.strip() in ("+", "-") and mrole in ("success", "warning"):
        m = brand.text_glow(m, ground, role=mrole, width=3.5, opacity=0.45)
    return m


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []
    blocks += scene_head(spec, ctx, label="[ sign chart ]")
    title = blocks[1].mobject

    content_w = T.FRAME_W - 2 * T.SIDE_GUTTER
    text_col = T.color(ground, "muted")   # number line + ticks read dim (ink-3)

    statement = None
    if spec.get("statement"):
        statement = brand.prose(spec["statement"], ground, role="primary", size=40,
                                max_width=content_w, align="CENTER")

    points = spec.get("points", [])
    rows = spec.get("rows", [])
    n_int = len(points) + 1
    for r in rows:
        if len(r.get("marks", [])) != n_int:
            raise ValueError(
                f"sign_chart row '{r.get('label')}': {len(r.get('marks', []))} marks "
                f"for {len(points)} points -- need len(points)+1 = {n_int}."
            )

    # -- row labels reserve the left column; the line takes the rest --------
    label_mobs = [brand.math_line(str(r.get("label", "")), ground,
                                  role="text", size="math") for r in rows]
    label_w = max([m.width for m in label_mobs], default=0.0)
    line_x0 = label_w + 0.7
    line_x1 = content_w
    seg = (line_x1 - line_x0) / n_int
    tick_xs = [line_x0 + (k + 1) * seg for k in range(len(points))]
    mark_xs = [line_x0 + (k + 0.5) * seg for k in range(n_int)]

    # -- the number line (built around local y=0, centred as a group later) --
    line = DoubleArrow([line_x0, 0, 0], [line_x1, 0, 0], buff=0,
                       color=text_col, stroke_width=2.0,
                       tip_length=0.16, max_tip_length_to_length_ratio=0.05)
    axis_parts: list[Any] = [line]
    for x, pt in zip(tick_xs, points):
        excluded = isinstance(pt, dict) and bool(pt.get("excluded"))
        label = str(pt.get("label", "")) if isinstance(pt, dict) else str(pt)
        if excluded:
            ring = brand.plot_dot(ground, role="warning", r=0.075)
            ring.set_fill(T.color(ground, "bg"), opacity=1.0)
            ring.set_stroke(T.color(ground, "warning"), width=3.0)
            ring.move_to([x, 0, 0])
            axis_parts.append(ring)
        else:
            axis_parts.append(Line([x, _TICK, 0], [x, -_TICK, 0],
                                   color=text_col, stroke_width=2.0))
        lab = brand.math_line(label, ground, role="primary", size="math_sm")
        lab.move_to([x, _TICK + 0.30 + lab.height / 2, 0])  # labels above the line,
        axis_parts.append(lab)                              # marks own the space below

    # -- mark rows: real-height cursor below the line ------------------------
    mark_grid: list[list[Any]] = []
    row_ys: list[float] = []
    y = -_FIRST_ROW_DROP
    prev_half = None
    for r, lab in zip(rows, label_mobs):
        marks = [_mark_mob(m, ground) for m in r.get("marks", [])]
        half = max([m.height for m in marks + [lab]], default=0.0) / 2
        if prev_half is not None:
            y -= prev_half + _ROW_GAP + half
        for m, x in zip(marks, mark_xs):
            m.move_to([x, y, 0])
        lab.move_to([0, y, 0], aligned_edge=LEFT)
        mark_grid.append(marks)
        row_ys.append(y)
        prev_half = half

    # -- guides: faint verticals dropping from each tick through the rows ----
    guides = []
    if rows and points:
        g_bottom = row_ys[-1] - 0.45
        for x in tick_xs:
            g = brand.vrule(-g_bottom + 0.2, ground, role="hairline", opacity=0.5)
            g.move_to([x, (0.2 + g_bottom) / 2, 0])
            guides.append(g)

    # -- centre statement + chart as one group in the zone -------------------
    chart = VGroup(*axis_parts, *label_mobs, *guides,
                   *[m for row in mark_grid for m in row])
    parts = ([statement] if statement is not None else []) + [chart]
    content = VGroup(*parts).arrange(DOWN, buff=0.75)
    zone_top = title.get_bottom()[1] - 0.55
    zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.45
    content.move_to([0, (zone_top + zone_bottom) / 2, 0])

    if statement is not None:
        blocks.append(Block("statement", statement, anim="fade", static=True))
    blocks.append(Block("axisline", VGroup(*axis_parts), anim="create",
                        static=True, layer="graph"))
    if guides:
        blocks.append(Block("guides", VGroup(*guides), anim="fade",
                            static=True, layer="decoration"))
    for i, lab in enumerate(label_mobs):
        blocks.append(Block(f"rowlabel.{i}", lab, anim="fade", static=True))
    for i, marks in enumerate(mark_grid):
        for k, m in enumerate(marks):
            blocks.append(Block(f"mark.{i}.{k}", m, anim="write", static=False))

    blocks.append(motif_corner(ground))
    return blocks

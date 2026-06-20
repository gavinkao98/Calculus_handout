"""value_table template -- Direction B (dark teaching frame).

A general table, one template for three recurring teaching uses:
  - the NUMERIC LIMIT TABLE ("x closes in on a, watch f(x)" -- the Section 1.3
    rhythm), revealed column by column;
  - a FORMULA GRID (e.g. the six trig derivatives -- too many rows for
    definition_math's single stack), revealed row by row;
  - a PROPERTY COMPARISON (left limit / right limit / conclusion).

Layout:
  eyebrow + title (scene_head; `kicker` override supported);
  optional centred prose `statement`;
  the table -- an optional `header` row with a hairline rule under it, then
  body `rows`; column widths follow the widest cell per column; the
  statement + table centre vertically as one group (definition_math rule).

Cells route like every author field: `$...$` / pure-math -> Tex/MathTex
(`brand.math_line`), plain words -> Text (`brand.prose`) -- so "does not
exist" never renders as run-together math italics. Keep cells one line;
an over-wide table is an authoring error sizecheck catches (a table cannot
wrap -- shorten cells or split the scene).

Reveal (`reveal: rows | cols`, default rows):
  rows -> header is static frame; each body row waits for {show row.N}.
  cols -> each COLUMN (its header cell + body cells) waits for {show col.N}
          -- the limit-table rhythm, every beat one step closer.

`accent_col: N` / `accent_row: N` (optional) colour those cells in the
scene's accent role -- the punchline column ("$\\to 4$") or the key row.

YAML shape:
  template: value_table
  accent: example
  title: "..."
  statement: "..."                                  # optional
  reveal: cols                                      # default rows
  header: ["$x$", "$1.9$", "$1.99$", "$\\to 2$"]    # optional
  rows:
    - ["$f(x)$", "$2.9$", "$2.99$", "$\\to 3$"]
  accent_col: 3                                     # optional
"""
from __future__ import annotations

from typing import Any

from manim import DOWN, Rectangle, VGroup

from .. import brand
from ..blocks import Block, accent_role
from ..visuals import theme as T
from ._common import scene_head, motif_corner

_COL_GAP = 0.7
_ROW_GAP = 0.5
_HEADER_RULE_GAP = 0.26


def _cell(text: str, ground: str, *, role: str, size):
    """One table cell. Routed on content like every author field: math (or
    text with inline $math$) -> math_line, plain words -> prose (Text)."""
    s = str(text).strip()
    if "$" in s:
        return brand.math_line(s, ground, role=role, size=size)
    return brand.prose(s, ground, role=role, size=size)


def build(spec: dict[str, Any], ctx: dict[str, Any]) -> list[Block]:
    ground = ctx["ground"]
    blocks: list[Block] = []
    blocks += scene_head(spec, ctx, label="[ table ]")
    title = blocks[1].mobject

    content_w = T.FRAME_W - 2 * T.SIDE_GUTTER
    role = accent_role(spec)

    statement = None
    if spec.get("statement"):
        statement = brand.prose(spec["statement"], ground, role="primary", size=40,
                                max_width=content_w, align="CENTER")

    header = [str(c) for c in spec.get("header", [])]
    rows = [[str(c) for c in r] for r in spec.get("rows", [])]
    n_cols = max([len(header)] + [len(r) for r in rows]) if (header or rows) else 0
    accent_col = spec.get("accent_col")
    accent_row = spec.get("accent_row")

    def cell_role(r: int | None, c: int) -> str:
        # r is None for the header row. The punchline (accent) column/row is
        # blue-ink; the row-label column 0 is ink-1; header ink-3; body ink-2.
        if accent_col is not None and c == int(accent_col):
            return "blue_ink"
        if r is not None and accent_row is not None and r == int(accent_row):
            return "blue_ink"
        if c == 0:
            return "primary"
        return "muted" if r is None else "text"

    header_mobs = [_cell(c, ground, role=cell_role(None, j), size=38)
                   for j, c in enumerate(header)]
    row_mobs = [[_cell(c, ground, role=cell_role(i, j), size=42) for j, c in enumerate(r)]
                for i, r in enumerate(rows)]

    # -- grid geometry: column width = widest cell in that column ----------
    col_w = [0.0] * n_cols
    for j, m in enumerate(header_mobs):
        col_w[j] = max(col_w[j], m.width)
    for r in row_mobs:
        for j, m in enumerate(r):
            col_w[j] = max(col_w[j], m.width)
    # equal centre-to-centre pitch so visual rhythm stays even when one
    # column (e.g. the accent punchline) is wider than the rest
    if n_cols <= 1:
        col_x = [col_w[0] / 2] if n_cols == 1 else []
        table_w = col_w[0] if n_cols == 1 else 0.0
    else:
        pitch = max(col_w[j] / 2 + col_w[j + 1] / 2
                    for j in range(n_cols - 1)) + _COL_GAP
        col_x = [col_w[0] / 2 + j * pitch for j in range(n_cols)]
        table_w = col_x[-1] + col_w[-1] / 2

    # rows top-anchored on real heights (the fused-rows lesson)
    table_parts: list[Any] = []
    y = 0.0
    rule = None
    if header_mobs:
        h = max(m.height for m in header_mobs)
        for j, m in enumerate(header_mobs):
            m.move_to([col_x[j], y - h / 2, 0])
        y -= h + _HEADER_RULE_GAP
        rule = brand.hrule(table_w, ground, role="hairline_strong", stroke=2.0)
        rule.move_to([table_w / 2, y, 0])
        y -= _HEADER_RULE_GAP
        table_parts += header_mobs + [rule]
    for r in row_mobs:
        if not r:
            continue
        h = max(m.height for m in r)
        for j, m in enumerate(r):
            m.move_to([col_x[j], y - h / 2, 0])
        y -= h + _ROW_GAP
        table_parts += r

    # -- faint blue tint behind the punchline (accent) column ---------------
    tint = None
    if accent_col is not None and 0 <= int(accent_col) < n_cols:
        ac = int(accent_col)
        tint_h = (0.0 - y) + 0.1
        tint = Rectangle(width=col_w[ac] + 0.6, height=tint_h,
                         fill_color=T.color(ground, "blue"), fill_opacity=T.ACCENT_DIM,
                         stroke_width=0)
        tint.move_to([col_x[ac], (0.0 + y) / 2 + _ROW_GAP / 2, 0])
        table_parts.insert(0, tint)   # behind the cells

    # -- centre statement + table as one group in the zone ------------------
    parts = []
    if statement is not None:
        parts.append(statement)
    table = VGroup(*table_parts) if table_parts else None
    if table is not None:
        parts.append(table)
    if parts:
        content = VGroup(*parts).arrange(DOWN, buff=0.8)
        zone_top = title.get_bottom()[1] - 0.55
        zone_bottom = -T.FRAME_H / 2 + T.SAFE_MARGIN + 0.45
        content.move_to([0, (zone_top + zone_bottom) / 2, 0])

    if tint is not None:
        blocks.append(Block("col_tint", tint, anim="fade", static=True, layer="background"))
    if statement is not None:
        blocks.append(Block("statement", statement, anim="fade", static=True))
    if rule is not None:
        blocks.append(Block("rule", rule, anim="fade", static=True, layer="decoration"))

    # -- reveal grouping -----------------------------------------------------
    if str(spec.get("reveal", "rows")) == "cols":
        # a column = its header cell + body cells; every beat one step closer
        for j in range(n_cols):
            cells = []
            if j < len(header_mobs):
                cells.append(header_mobs[j])
            cells += [r[j] for r in row_mobs if j < len(r)]
            if cells:
                blocks.append(Block(f"col.{j}", VGroup(*cells), anim="fade", static=False))
    else:
        if header_mobs:
            blocks.append(Block("header", VGroup(*header_mobs), anim="fade", static=True))
        for i, r in enumerate(row_mobs):
            if r:
                blocks.append(Block(f"row.{i}", VGroup(*r), anim="fade", static=False))

    blocks.append(motif_corner(ground))
    return blocks

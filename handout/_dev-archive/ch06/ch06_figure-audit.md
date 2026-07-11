# ch06 figure audit — raw record (gate-1 D1–D8 + gate-2 Codex)

> Raw working record (this `_dev-archive` tree is **not** version-controlled). Durable summary lives in
> `PLAN-ch06.md` §「M2 figure batch」＋ the standalone HTML report `handout/_audit/REVIEW-ch06-figure-audit.html`.
> Date: 2026-07-10 · branch `video/template-redesign-navy-spine` · **visual blocking = 0**.

## Population (enumerated from fragments — all `<figure>`, all `data-fig`, no inline-SVG)

8 figures across sec-6-1..6-4:

| Fig | id | § | locus | tier | status |
|---|---|---|---|---|---|
| 6.1 | riemann-lr-x2 | 6.1 | after Ex 6.1 | ess | prior session, re-audited |
| 6.2 | refinement-rn-x2 | 6.1 | Ex 6.1→6.2 | strong | new |
| 6.3 | velocity-distance-steps | 6.1 | after Ex 6.3 | strong | new |
| 6.4 | signed-area-line | 6.2 | after Ex 6.5 | ess | new |
| 6.5 | minmax-sqrt | 6.2 | after Ex 6.6 | strong | new |
| 6.6 | accumulation-sliver | 6.3 | accumulation subsec (before Thm 6.3) | ess | new (FTC-1 anchor) |
| 6.7 | ftc-trap | 6.3 | after FTC-1 proof | strong | new |
| 6.8 | velocity-signed-area | 6.4 | after Ex 6.12 | ess | new |

Render: `build.py ch06` (katex 0, math 741) → `linebreak-gate` 0 → `shot.mjs … figures` (8× 2× PNG,
scratchpad/ch6figs). Self-checked every PNG (rectangle/curve contact, shaded regions, grayscale) before gates.

## Gate-1 — `handout-figure-audit` subagent (D1–D8), 0 blocking

VERDICT = 0. All 8 figures D1–D8 clean. Verifier discipline applied: every D5/D6 claim re-checked against
`const FIGS` source; small-subscript vigilance for 6.7 (`m_h/M_h` at correct heights, `u_h/v_h` not swapped);
6.2 confirmed to carry **no `=1/3`** text element (D7). Dimension summary: D1 (no info-hiding labels), D2
(no clipping), D3 (windows readable), D4 (load-bearing ticks carry `tex`; 6.6 y-axis intentionally value-less =
label economy), D5 (figure↔caption consistent), D6 (coordinates verified), D7 (no worked-example leak), D8
(colour made redundant everywhere) — all clean.

2 borderline items → **non-finding** (transparent): (a) y-axis name abutting top tick (6.1/6.2/6.6/6.7/6.8) =
established house style, both glyphs legible; (b) 6.2 triple panels wrap 2+1 = reading order & comparison intact.

## Gate-2 — Codex `-i` visual second-reader (codex-cli 0.144.1), 0 blocking

`codex exec -s read-only -i <8 png> -` with per-figure domain-fact checklist, blind independent read. Result:

```
Figure 6.1: clean … Figure 6.8: clean
Overall verdict: total blocking count 0
```

All 8 clean. Independent confirmation of gate-1.

## D8 grayscale encoding (how colour is made redundant)

- Signed regions (6.4, 6.8): red/blue tone **+** large `+` / `−` glyph carrying the sign colour-independently.
- Min/max rectangles (6.5, 6.7): inscribed solid border vs circumscribed dashed border **+** `m`/`M` (`m_h`/`M_h`) labels.
- Single-curve/region figures (6.1–6.3, 6.6): no colour-coded distinction to survive; panel notes / dashed
  interpolation carry meaning.

## Kit / sizing notes

- Uses the M2 `buildPlot` fill primitives (`rect` / `area`) + fill CSS classes (`fill-area/fill-pos/fill-neg/
  rect-lo/rect-hi/rect-sum`), added & validated at M2 prerequisite step (persist across `build.py`, outside content region).
- **No `--fig-6-*` width vars needed**: all 8 render fine at buildPlot inline widths (single 250–320px,
  triple 215px/panel, pair 250px/panel). No shell CSS sizing tuning required.
- One-pass, zero blocking-iteration: the rect/area primitive + Figure 6.1 template made 6.2–6.8 correct on first draw.

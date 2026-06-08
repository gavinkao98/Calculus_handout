/* ============================================================
   figures.js — Chapter 3 figure registry.
   Each entry returns { layout, panels:[{svg, note}] }.
   Most chapter figures use buildPlot() (shared/plot.js) for
   function graphs. buildPlot has NO fill/sector primitive, so
   region-area schematics (e.g. the §3.1 sector inequality) are
   hand-built raw SVG here, inheriting the figure vocabulary
   (.fig-svg, .ptlab, var(--c-primary)/--ink…) from skin-hs.css.
   Labels are kept to single symbols (O, A, B, C, θ, 1); the
   areas and the inequality live in the caption and body prose
   (CONTENT_SPEC §10 "Label economy").
   Appended across sections — never overwrite.
   ============================================================ */
(function () {

  const FIGS = {

    /* §3.1 — Sector inequality on the unit circle.
       Three nested regions in the first quadrant ground the bound
       cos θ ≤ (sin θ)/θ ≤ 1:
         · triangle OAB  (inscribed)         = ½ sin θ
         · sector  OAB   (pie slice)         = ½ θ
         · triangle OAC  (out to tangent A)  = ½ tan θ,   C = (1, tan θ)
       Drawn as three non-overlapping fills (triangle OAB, the
       circular segment chord→arc, the corner arc→tangent) so the
       eye reads OAB ⊆ sector ⊆ OAC directly. The manuscript names
       the corner triangle ABC ( = OAC − OAB ); B lies on segment OC. */
    "sector-inequality": () => {
      const T = 40 * Math.PI / 180;            // display angle θ = 40°
      const R = 120, Ox = 130, Oy = 170;       // circle radius / centre (SVG px, y down)
      const c = Math.cos(T), s = Math.sin(T), t = Math.tan(T);
      const Ax = Ox + R,        Ay = Oy;                 // A = (1, 0)
      const Bx = Ox + R * c,    By = Oy - R * s;         // B = (cos θ, sin θ)
      const Cx = Ox + R,        Cy = Oy - R * t;         // C = (1, tan θ), on tangent at A
      const f1 = (n) => n.toFixed(1);
      const rT = 30;                                     // angle-arc radius near O
      const aEx = Ox + rT, aEy = Oy;                     // angle arc: start on OA
      const aBx = Ox + rT * c, aBy = Oy - rT * s;        //            end toward OB
      const mx = (Ox + Bx) / 2, my = (Oy + By) / 2;      // midpoint of OB (radius "1")

      const svg =
        `<svg viewBox="0 0 300 300" style="width:300px" class="fig-svg" role="img"` +
        ` aria-label="First-quadrant wedge of the unit circle centred at O. The inscribed triangle OAB sits inside the sector OAB, which sits inside the larger triangle OAC reaching the tangent line at A, so that one half sine theta is at most one half theta is at most one half tangent theta.">` +
        // --- region 3: corner outside the circle (arc → tangent), neutral slack ---
        `<path d="M${f1(Ax)},${f1(Ay)} L${f1(Cx)},${f1(Cy)} L${f1(Bx)},${f1(By)} ` +
          `A${R},${R} 0 0 1 ${f1(Ax)},${f1(Ay)} Z" fill="var(--ink)" fill-opacity="0.05" stroke="none"/>` +
        // --- region 2: circular segment (chord AB → arc), lighter primary ---
        `<path d="M${f1(Ax)},${f1(Ay)} A${R},${R} 0 0 0 ${f1(Bx)},${f1(By)} Z" ` +
          `fill="var(--c-primary)" fill-opacity="0.09" stroke="none"/>` +
        // --- region 1: inscribed triangle OAB, primary ---
        `<polygon points="${f1(Ox)},${f1(Oy)} ${f1(Ax)},${f1(Ay)} ${f1(Bx)},${f1(By)}" ` +
          `fill="var(--c-primary)" fill-opacity="0.17" stroke="none"/>` +
        // --- unit circle (context) ---
        `<circle cx="${Ox}" cy="${Oy}" r="${R}" fill="none" stroke="var(--ink-soft)" stroke-width="1"/>` +
        // --- tangent segment A→C (vertical tangent at A) ---
        `<line x1="${f1(Ax)}" y1="${f1(Ay)}" x2="${f1(Cx)}" y2="${f1(Cy)}" stroke="var(--ink)" stroke-width="1.4"/>` +
        // --- ray O→B→C (radius OB extended to the tangent at C) ---
        `<line x1="${f1(Ox)}" y1="${f1(Oy)}" x2="${f1(Cx)}" y2="${f1(Cy)}" stroke="var(--ink)" stroke-width="1.4"/>` +
        // --- radius OA ---
        `<line x1="${f1(Ox)}" y1="${f1(Oy)}" x2="${f1(Ax)}" y2="${f1(Ay)}" stroke="var(--ink)" stroke-width="1.4"/>` +
        // --- chord AB (edge of the inscribed triangle) ---
        `<line x1="${f1(Ax)}" y1="${f1(Ay)}" x2="${f1(Bx)}" y2="${f1(By)}" stroke="var(--ink-soft)" stroke-width="1"/>` +
        // --- right-angle tick at A (tangent ⊥ radius) ---
        `<path d="M${f1(Ax - 9)},${f1(Ay)} L${f1(Ax - 9)},${f1(Ay - 9)} L${f1(Ax)},${f1(Ay - 9)}" ` +
          `fill="none" stroke="var(--ink-soft)" stroke-width="1"/>` +
        // --- angle θ arc at O ---
        `<path d="M${f1(aEx)},${f1(aEy)} A${rT},${rT} 0 0 0 ${f1(aBx)},${f1(aBy)}" ` +
          `fill="none" stroke="var(--ink)" stroke-width="1.1"/>` +
        // --- dots at O, A, B, C ---
        `<circle cx="${f1(Ox)}" cy="${f1(Oy)}" r="2.5" class="dot"/>` +
        `<circle cx="${f1(Ax)}" cy="${f1(Ay)}" r="2.5" class="dot"/>` +
        `<circle cx="${f1(Bx)}" cy="${f1(By)}" r="2.5" class="dot"/>` +
        `<circle cx="${f1(Cx)}" cy="${f1(Cy)}" r="2.5" class="dot"/>` +
        // --- labels (single symbols; areas/inequality in caption + prose) ---
        `<text x="${f1(Ox - 9)}" y="${f1(Oy + 5)}" text-anchor="end" class="ptlab" font-style="italic">O</text>` +
        `<text x="${f1(Ax + 8)}" y="${f1(Ay + 16)}" text-anchor="middle" class="ptlab" font-style="italic">A</text>` +
        `<text x="${f1(Bx - 10)}" y="${f1(By - 6)}" text-anchor="end" class="ptlab" font-style="italic">B</text>` +
        `<text x="${f1(Cx + 9)}" y="${f1(Cy + 4)}" text-anchor="start" class="ptlab" font-style="italic">C</text>` +
        `<text x="${f1(Ox + rT + 9)}" y="${f1(Oy - 7)}" text-anchor="start" class="ptlab" font-style="italic">θ</text>` +
        `<text x="${f1(mx - 11)}" y="${f1(my - 3)}" text-anchor="end" class="ptlab">1</text>` +
        `</svg>`;

      return { layout: "single", panels: [{ svg }] };
    },

    /* §3.2 — The chain rule as a composed mapping.
       Three stacked horizontal axes (input x, intermediate u = g(x),
       output y = f(u)). A small increment h at the aligned base point is
       carried by g to a wider increment at u₀, then by f to a wider one
       still at y₀: the increment widths grow because the two local slopes
       g'(x₀), f'(g(x₀)) multiply. Single-symbol labels (x, u, y, h, x₀, u₀,
       y₀) plus the two arrow factors; the algebra (net stretch f'·g'·h)
       lives in the caption and body prose (CONTENT_SPEC §10). buildPlot has
       no multi-axis / propagation-arrow primitive, so this is raw SVG. */
    "composed-mapping": () => {
      const ax1 = 34, ax2 = 276;                 // axis horizontal extent
      const yIn = 46, yMid = 140, yOut = 234;    // input / intermediate / output axes (SVG px, y down)
      const bx = 92;                             // base points x₀, u₀, y₀ (drawn aligned)
      const inEnd = bx + 26;                     // input increment width = h
      const midEnd = bx + 42;                    // stretched by g'(x₀)   (display ratio ≈ 1.6)
      const outEnd = bx + 63;                    // stretched again by f'(g(x₀))  (≈ 1.5)
      const f1 = (n) => n.toFixed(1);

      const axis = (y) =>                        // axis line with a right arrowhead
        `<line x1="${ax1}" y1="${y}" x2="${ax2}" y2="${y}" stroke="var(--ink)" stroke-width="1.3"/>` +
        `<polygon points="${ax2},${y} ${ax2 - 7},${y - 3.5} ${ax2 - 7},${y + 3.5}" fill="var(--ink)"/>`;
      const inc = (y, xe) =>                      // increment highlight bx → xe
        `<line x1="${bx}" y1="${y}" x2="${f1(xe)}" y2="${y}" stroke="var(--c-primary)" stroke-width="3.6" stroke-linecap="round"/>`;
      const arrow = (x1, y1, x2, y2) =>          // downward map arrow with arrowhead
        `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="var(--ink-soft)" stroke-width="1.3"/>` +
        `<polygon points="${f1(x2)},${f1(y2)} ${f1(x2 - 3.4)},${f1(y2 - 6.5)} ${f1(x2 + 3.4)},${f1(y2 - 6.5)}" fill="var(--ink-soft)"/>`;

      const svg =
        `<svg viewBox="0 0 300 275" style="width:300px" class="fig-svg" role="img"` +
        ` aria-label="Three stacked horizontal axes: an input axis x, an intermediate axis u equal to g of x, and an output axis y equal to f of u. A small increment h at the base point x-zero is carried by g to a wider increment at u-zero, and by f to a wider increment still at y-zero, so the two slopes multiply.">` +
        // base-point alignment guide
        `<line x1="${bx}" y1="${yIn}" x2="${bx}" y2="${yOut}" stroke="var(--ink-soft)" stroke-width="1" stroke-dasharray="3 3" opacity="0.6"/>` +
        // three axes
        axis(yIn) + axis(yMid) + axis(yOut) +
        // increment highlights (growing widths show the magnification)
        inc(yIn, inEnd) + inc(yMid, midEnd) + inc(yOut, outEnd) +
        // map arrows: g (x → u) and f (u → y)
        arrow(inEnd, yIn + 7, midEnd, yMid - 7) +
        arrow(midEnd, yMid + 7, outEnd, yOut - 7) +
        // 'h' bracket above the input increment
        `<path d="M${bx},${yIn - 7} L${bx},${yIn - 11} L${f1(inEnd)},${yIn - 11} L${f1(inEnd)},${yIn - 7}" ` +
          `fill="none" stroke="var(--ink)" stroke-width="1"/>` +
        // base-point dots
        `<circle cx="${bx}" cy="${yIn}" r="2.5" class="dot"/>` +
        `<circle cx="${bx}" cy="${yMid}" r="2.5" class="dot"/>` +
        `<circle cx="${bx}" cy="${yOut}" r="2.5" class="dot"/>` +
        // axis variable labels
        `<text x="${ax2 - 4}" y="${yIn - 8}" text-anchor="end" class="ptlab" font-style="italic">x</text>` +
        `<text x="${ax2 - 4}" y="${yMid - 8}" text-anchor="end" class="ptlab" font-style="italic">u</text>` +
        `<text x="${ax2 - 4}" y="${yOut - 8}" text-anchor="end" class="ptlab" font-style="italic">y</text>` +
        // 'h' label
        `<text x="${f1((bx + inEnd) / 2)}" y="${yIn - 15}" text-anchor="middle" class="ptlab" font-style="italic">h</text>` +
        // base-point labels
        `<text x="${bx - 7}" y="${yIn + 16}" text-anchor="end" class="ptlab" font-style="italic">x₀</text>` +
        `<text x="${bx - 7}" y="${yMid + 16}" text-anchor="end" class="ptlab" font-style="italic">u₀</text>` +
        `<text x="${bx - 7}" y="${yOut + 16}" text-anchor="end" class="ptlab" font-style="italic">y₀</text>` +
        // magnification factors on the arrows
        `<text x="${f1(midEnd) + 9}" y="${f1((yIn + yMid) / 2) + 3}" text-anchor="start" class="ptlab">× g′(x₀)</text>` +
        `<text x="${f1(outEnd) + 9}" y="${f1((yMid + yOut) / 2) + 3}" text-anchor="start" class="ptlab">× f′(g(x₀))</text>` +
        `</svg>`;

      return { layout: "single", panels: [{ svg }] };
    },

  };

  /* ---- hydrateFigures: fills every <figure data-fig="id"> ---- */
  function hydrateFigures(root) {
    (root || document).querySelectorAll("[data-fig]").forEach(function (el) {
      var def = FIGS[el.dataset.fig];
      if (!def || el.dataset.figDone) return;
      var r = def();
      var layout = r.layout, panels = r.panels;
      var html;
      if (layout === "single" && panels.length === 1 && !panels[0].note) {
        html = '<div class="figure-art">' + panels[0].svg + '</div>';
      } else {
        var cls = { pair: "figure-art--pair", triple: "figure-art--triple", grid: "figure-art--grid" }[layout] || "";
        html = '<div class="figure-art ' + cls + '">' +
          panels.map(function (p) {
            return '<div class="fig-panel">' + p.svg + (p.note ? '<div class="fig-note">' + p.note + '</div>' : '') + '</div>';
          }).join("") + '</div>';
      }
      el.insertAdjacentHTML("afterbegin", html);
      el.dataset.figDone = "1";
    });
  }
  window.hydrateFigures = hydrateFigures;
})();

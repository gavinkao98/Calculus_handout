/* ============================================================
   figures.js — Chapter 2 figure registry.
   Each entry returns { layout, panels:[{svg, note}] }.
   Labels carry \( \) TeX, typeset by KaTeX.
   ============================================================ */
(function () {
  const sqrt = Math.sqrt;

  const FIGS = {

    /* §2.1 — Secant lines converging to the tangent line at P.
       Design: P at lower-left on a concave-up parabola; three Q points
       well-spaced to the right → secant lines fan out; tangent line in
       a distinct colour (caution/red) below the fan. */
    "secant-to-tangent": () => {
      var f = function (x) { return 0.1 * x * x + 0.5; };
      var c = 1, fc = 0.6, fprime = 0.2;
      var qxs = [7, 5, 3];                        // Q₁ farthest, Q₃ closest
      var slopes = qxs.map(function (qx) { return (f(qx) - fc) / (qx - c); });
      //  slopes = [0.8, 0.6, 0.4] — evenly spaced fan

      var xL = -0.3, xR = 8.5;
      var items = [
        // --- secant lines (dashed, extend as full lines) ---
        { type: "curve", fn: function (x) { return fc + slopes[0] * (x - c); },
          domain: [xL, xR], samples: 10, cls: "refline" },
        { type: "curve", fn: function (x) { return fc + slopes[1] * (x - c); },
          domain: [xL, xR], samples: 10, cls: "refline" },
        { type: "curve", fn: function (x) { return fc + slopes[2] * (x - c); },
          domain: [xL, xR], samples: 10, cls: "refline" },
        // --- tangent line (solid caution/red — visually distinct) ---
        { type: "curve", fn: function (x) { return fc + fprime * (x - c); },
          domain: [xL, xR], samples: 10, cls: "arrow-bwd" },
        // --- main curve (drawn last, on top) ---
        { type: "curve", fn: f, domain: [0, 8.2], samples: 200, cls: "curve" },
        // --- dots ---
        { type: "dot", x: c, y: fc, r: 3.5 },
        { type: "dot", x: 7, y: f(7), r: 2.5 },
        { type: "dot", x: 5, y: f(5), r: 2.5 },
        { type: "dot", x: 3, y: f(3), r: 2.5 },
        // --- P label (below-left) ---
        { type: "text", x: c - 0.1, y: fc - 0.4,
          tex: "P", cls: "a-pt", anchor: "end" },
        // --- Q labels (above-right of each dot) ---
        { type: "text", x: 7.25, y: f(7) + 0.35,
          tex: "Q_1", cls: "a-pt", anchor: "start" },
        { type: "text", x: 5.25, y: f(5) + 0.35,
          tex: "Q_2", cls: "a-pt", anchor: "start" },
        { type: "text", x: 3.25, y: f(3) + 0.35,
          tex: "Q_3", cls: "a-pt", anchor: "start" },
        // --- "Secant lines" group label (right side, between l1 and l3) ---
        { type: "text", x: xR + 0.2, y: fc + slopes[1] * (xR - c),
          tex: "\\text{Secant lines}", cls: "a-ref", anchor: "start", size: 12 },
        // --- "Tangent line" full label (right side) ---
        { type: "text", x: xR + 0.2, y: fc + fprime * (xR - c),
          tex: "\\text{Tangent line}", cls: "a-ref", anchor: "start", size: 12 },
        // --- curve label ---
        { type: "text", x: 8, y: f(8) + 0.45,
          tex: "y\\!=\\!f(x)", cls: "a-curve", anchor: "start" },
      ];
      return {
        layout: "single",
        panels: [{
          svg: buildPlot({
            w: 460, h: 300, xmin: -1, xmax: 10, ymin: -1, ymax: 7.5,
            xlabel: "x", ylabel: "y",
            xticks: [
              { x: c, tex: "c" },
              { x: 3, tex: "x_3" },
              { x: 5, tex: "x_2" },
              { x: 7, tex: "x_1" },
            ],
            aria: "Three secant lines through P fanning out as Q1, Q2, Q3 approach P from the right, converging toward the tangent line at P.",
            items: items,
          }),
        }],
      };
    },

    /* §2.2 — The derivative as a function: f above, f' below, drawn on a
       common x-axis. Top: parabola f(x)=x²+4x−2 (minimum at x=−2, f=−6).
       Bottom: line f'(x)=2x+4 (zero at x=−2). A shared dashed vertical at
       x=−2 links the minimum of f to the zero of f'. Both SVGs use the same
       w / pad / xmin / xmax, so a given x maps to the same horizontal pixel;
       returned as ONE panel whose .fig-panel column layout stacks them
       centred → the x-axes line up. Uses only the in-section result. */
    /* §2.3 — Non-differentiability at a corner: |x| near 0.
       Design: V-shape of |x|, two secant lines from the right (slope +1)
       and two from the left (slope −1), labeled to show disagreement.
       A dot at the origin marks the corner. */
    "abs-corner": () => {
      var f = function (x) { return Math.abs(x); };
      var dom = [-4, 4];
      // secant points: two from the right, two from the left
      var rPts = [3, 1.5];
      var lPts = [-3, -1.5];

      var items = [
        // --- secant lines from the right (slope +1, dashed) ---
        { type: "curve", fn: function (x) { return x; },
          domain: [-0.5, 4.2], samples: 10, cls: "refline" },
        // --- secant lines from the left (slope −1, dashed) ---
        { type: "curve", fn: function (x) { return -x; },
          domain: [-4.2, 0.5], samples: 10, cls: "refline" },
        // --- main curve |x| (solid, on top) ---
        { type: "curve", fn: f, domain: dom, samples: 200, cls: "curve" },
        // --- dots on secant endpoints ---
        { type: "dot", x: 3, y: 3, r: 2.5 },
        { type: "dot", x: 1.5, y: 1.5, r: 2.5 },
        { type: "dot", x: -3, y: 3, r: 2.5 },
        { type: "dot", x: -1.5, y: 1.5, r: 2.5 },
        // --- corner dot (origin) ---
        { type: "dot", x: 0, y: 0, r: 3.5 },
        // --- slope labels ---
        { type: "text", x: 3.2, y: 1.8,
          tex: "\\text{slope}=+1", cls: "a-pt", anchor: "start", size: 12 },
        { type: "text", x: -3.2, y: 1.8,
          tex: "\\text{slope}=-1", cls: "a-pt", anchor: "end", size: 12 },
        // --- curve label ---
        { type: "text", x: 3.8, y: 4.1,
          tex: "y\\!=\\!|x|", cls: "a-curve", anchor: "start" },
      ];
      return {
        layout: "single",
        panels: [{
          svg: buildPlot({
            w: 420, h: 280, xmin: -5, xmax: 5, ymin: -1, ymax: 5,
            xlabel: "x", ylabel: "y",
            xticks: [{ x: 0, tex: "0" }],
            aria: "V-shaped graph of |x| with secant lines from the left having slope -1 and from the right having slope +1, meeting at a corner at the origin where no single tangent exists.",
            items: items,
          }),
        }],
      };
    },

    "f-and-fprime": () => {
      var f  = function (x) { return x * x + 4 * x - 2; };
      var fp = function (x) { return 2 * x + 4; };
      var dom = [-6.4, 2.4];
      var common = { w: 460, xmin: -6.8, xmax: 2.8, xlabel: "x", ylabel: "y" };

      // --- top panel: f ---
      var top = buildPlot(Object.assign({}, common, {
        h: 250, ymin: -8, ymax: 14,
        xticks: [{ x: -2, tex: "-2" }],
        aria: "Graph of f(x)=x^2+4x-2, a parabola with its minimum at x=-2 where f=-6.",
        items: [
          { type: "vline", x: -2, cls: "refline" },
          { type: "curve", fn: f, domain: dom, samples: 200, cls: "curve" },
          { type: "dot", x: -2, y: -6, r: 3 },
          { type: "text", x: 2.45, y: 12, tex: "y\\!=\\!f(x)", cls: "a-curve", anchor: "start" },
          { type: "text", x: -2.35, y: -6, tex: "\\text{min}", cls: "a-pt", anchor: "end" },
        ],
      }));

      // --- bottom panel: f' (same horizontal scale as the top) ---
      var bot = buildPlot(Object.assign({}, common, {
        h: 210, ymin: -9, ymax: 9,
        xticks: [{ x: -2, tex: "-2" }],
        aria: "Graph of f'(x)=2x+4, a line crossing zero at x=-2; negative to the left, positive to the right.",
        items: [
          { type: "vline", x: -2, cls: "refline" },
          { type: "curve", fn: fp, domain: dom, samples: 12, cls: "curve" },
          { type: "dot", x: -2, y: 0, r: 3 },
          { type: "text", x: 2.45, y: 7, tex: "y\\!=\\!f'(x)", cls: "a-curve", anchor: "start" },
          { type: "text", x: -5.6, y: -4.5, tex: "f'<0", cls: "a-pt", anchor: "start" },
          { type: "text", x: -1.4, y: 4.5, tex: "f'>0", cls: "a-pt", anchor: "start" },
        ],
      }));

      return { layout: "stack", panels: [{ svg: top + bot }] };
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

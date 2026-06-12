/* ============================================================
   figures.js — Chapter 1 figure registry.
   Each entry returns { layout, panels:[{svg, note}] } (note may
   carry \( \) math, rendered by the page's KaTeX pass afterward).
   In-figure labels also carry TeX via { type:"text", tex:"…" } and
   are typeset by the same KaTeX pass — so every glyph in the graphs
   matches the body equations (Computer Modern).
   hydrateFigures(root) fills every <figure data-fig="id"> before
   its <figcaption>.
   ============================================================ */
(function () {
  const P = () => window.PIVAL;
  const pow2 = (x) => Math.pow(2, x);

  const FIGS = {
    /* ---------------- §1.1 ---------------- */
    "hlt": () => ({
      layout: "pair",
      panels: [
        {
          svg: buildPlot({
            w: 250, h: 200, xmin: -2.3, xmax: 2.2, ymin: -2.1, ymax: 2.3,
            xlabel: "x", ylabel: "y", aria: "A one-to-one line crossed once by a horizontal line.",
            items: [
              { type: "curve", fn: (x) => x, domain: [-1.5, 1.45], cls: "curve" },
              { type: "hline", y: 1, from: -2.1, to: 1.3, cls: "refline" },
              { type: "dot", x: 1, y: 1 },
              { type: "text", x: 1.55, y: 1.62, tex: "f", cls: "a-curve" },
              { type: "text", x: 1.42, y: 1.0, tex: "y=c", cls: "a-ref", anchor: "start", vAnchor: "bottom", dy: -2 },
              { type: "text", x: 1.06, y: 0.46, tex: "(x_1,\\,c)", cls: "a-pt", anchor: "start" },
            ],
          }),
          note: "One-to-one \u2014 a line meets the graph at most once.",
        },
        {
          svg: buildPlot({
            w: 250, h: 200, xmin: -2.3, xmax: 2.2, ymin: -2.1, ymax: 2.3,
            xlabel: "x", ylabel: "y", aria: "A parabola crossed twice by a horizontal line.",
            items: [
              { type: "curve", fn: (x) => 1.15 * x * x, domain: [-1.4, 1.4], cls: "curve" },
              { type: "hline", y: 1.25, from: -1.85, to: 1.85, cls: "refline" },
              { type: "dot", x: -1.043, y: 1.25 },
              { type: "dot", x: 1.043, y: 1.25 },
              { type: "text", x: 1.5, y: 2.18, tex: "f", cls: "a-curve" },
              { type: "text", x: 1.9, y: 1.25, tex: "y=c", cls: "a-ref", anchor: "start", vAnchor: "bottom", dy: -1 },
              { type: "text", x: -1.2, y: 0.98, tex: "(x_1,\\,c)", cls: "a-pt", anchor: "end" },
              { type: "text", x: 1.2, y: 0.98, tex: "(x_2,\\,c)", cls: "a-pt", anchor: "start" },
            ],
          }),
          note: "Not one-to-one \u2014 a line meets the graph more than once.",
        },
      ],
    }),

    "restrict-x2": () => ({
      layout: "single",
      panels: [{
        svg: buildPlot({
          w: 300, h: 300, xmin: -0.4, xmax: 2.7, ymin: -0.4, ymax: 2.7,
          xlabel: "x", ylabel: "y",
          aria: "The squaring function restricted to the nonnegative reals, its inverse square root, and the mirror line y equals x.",
          items: [
            { type: "curve", fn: (x) => x, domain: [0, 2.5], cls: "refline" },
            { type: "curve", fn: (x) => x * x, domain: [0, 1.6], cls: "curve" },
            { type: "curve", fn: (x) => Math.sqrt(x), domain: [0, 2.5], cls: "curve" },
            { type: "text", x: 1.02, y: 2.25, tex: "f(x)=x^{2}", cls: "a-curve", anchor: "end" },
            { type: "text", x: 2.5, y: 1.5, tex: "f^{-1}(x)=\\sqrt{x}", cls: "a-curve", anchor: "start" },
            { type: "text", x: 2.32, y: 2.5, tex: "y=x", cls: "a-ref", anchor: "start" },
          ],
        }),
      }],
    }),

    /* ---------------- §1.2 ---------------- */
    "sine-not-1to1": () => ({
      layout: "single",
      panels: [{
        svg: buildPlot({
          w: 620, h: 220, xmin: -6.9, xmax: 7.4, ymin: -1.35, ymax: 1.35,
          pad: { t: 16, r: 18, b: 26, l: 18 },
          xlabel: "x", ylabel: "y", aria: "The sine function on the real line is not one-to-one.",
          xticks: [{ x: -2 * P() }, { x: -P() }, { x: P() }, { x: 2 * P() }],
          yticks: [{ y: -1 }, { y: 1 }],
          items: [
            { type: "curve", fn: (x) => Math.sin(x), domain: [-6.8, 6.8], samples: 360, cls: "curve" },
            { type: "hline", y: 0.5, from: -6.8, to: 6.8, cls: "refline" },
            ...[0.5236, 2.618, 6.807, -3.6652, -5.7596].map((x) => ({ type: "dot", x, y: 0.5, r: 2.6 })),
            { type: "text", x: 3.25, y: 1.0, tex: "\\sin x", cls: "a-curve", anchor: "start" },
            { type: "text", x: 6.95, y: 0.5, tex: "y=c", cls: "a-ref", anchor: "start", vAnchor: "bottom", dy: -1 },
          ],
        }),
      }],
    }),
    "restricted-sine": () => ({
      layout: "single",
      panels: [{
        svg: buildPlot({
          w: 380, h: 260, xmin: -1.95, xmax: 1.95, ymin: -1.25, ymax: 1.25,
          xlabel: "x", ylabel: "y", aria: "Restricted branch of sine.",
          xticks: [{ x: -P() / 2 }, { x: P() / 2 }], yticks: [{ y: -1 }, { y: 1 }],
          items: [
            { type: "curve", fn: (x) => Math.sin(x), domain: [-P() / 2, P() / 2], cls: "curve" },
            { type: "text", x: 1.02, y: 1.12, tex: "\\sin x", cls: "a-curve", anchor: "start" },
          ],
        }),
      }],
    }),
    "restricted-cosine": () => ({
      layout: "single",
      panels: [{
        svg: buildPlot({
          w: 380, h: 200, xmin: -0.4, xmax: 3.6, ymin: -1.35, ymax: 1.75,
          xlabel: "x", ylabel: "y", aria: "Restricted branch of cosine.",
          xticks: [{ x: P() }], yticks: [{ y: -1 }, { y: 1 }],
          items: [
            { type: "curve", fn: (x) => Math.cos(x), domain: [0, P()], cls: "curve" },
            { type: "text", x: 1.25, y: 0.8, tex: "\\cos x", cls: "a-curve", anchor: "start" },
          ],
        }),
      }],
    }),
    "restricted-tangent": () => ({
      layout: "single",
      panels: [{
        svg: buildPlot({
          w: 320, h: 320, xmin: -1.95, xmax: 1.95, ymin: -5, ymax: 5,
          xlabel: "x", ylabel: "y", aria: "Restricted branch of tangent.",
          xticks: [{ x: -P() / 2 }, { x: P() / 2 }],
          items: [
            { type: "vline", x: -P() / 2, cls: "refline" },
            { type: "vline", x: P() / 2, cls: "refline" },
            { type: "curve", fn: (x) => Math.tan(x), domain: [-1.37, 1.37], samples: 300, cls: "curve" },
            { type: "text", x: 0.35, y: 2.8, tex: "\\tan x", cls: "a-curve", anchor: "start" },
          ],
        }),
      }],
    }),
    "arcsin-triangle": () => ({
      layout: "single",
      panels: [{
        svg: buildPlot({
          w: 300, h: 130, xmin: -0.3, xmax: 3.5, ymin: -0.35, ymax: 1.45, axes: false,
          aria: "Right triangle with angle theta, opposite 1, adjacent 2 root 2, hypotenuse 3.",
          items: [
            { type: "seg", x1: 0, y1: 0, x2: 3, y2: 0, cls: "curve" },
            { type: "seg", x1: 3, y1: 0, x2: 3, y2: 1, cls: "curve" },
            { type: "seg", x1: 3, y1: 1, x2: 0, y2: 0, cls: "curve" },
            { type: "seg", x1: 2.78, y1: 0, x2: 2.78, y2: 0.22, cls: "axis" },
            { type: "seg", x1: 2.78, y1: 0.22, x2: 3, y2: 0.22, cls: "axis" },
            { type: "text", x: 0.74, y: 0.085, tex: "\\theta", cls: "a-pt", anchor: "start" },
            { type: "text", x: 1.5, y: 0, tex: "2\\sqrt{2}", cls: "a-pt", anchor: "middle", vAnchor: "top", dy: 4 },
            { type: "text", x: 3, y: 0.5, tex: "1", cls: "a-pt", anchor: "start", dx: 4 },
            { type: "text", x: 1.25, y: 0.62, tex: "3", cls: "a-pt", anchor: "end" },
          ],
        }),
      }],
    }),

    /* ---------------- §1.3 ---------------- */
    "limit-same-near-a": () => {
      const base = (extra) => buildPlot(Object.assign({
        w: 250, h: 200, xmin: 0, xmax: 3.7, ymin: 0, ymax: 14,
        pad: { t: 14, r: 16, b: 20, l: 18 }, xlabel: "x", ylabel: "y",
        aria: "A function approaching L as x approaches a.",
      }, extra));
      const labels = [
        { type: "hline", y: 8, from: 0, to: 3, cls: "refline" },
        { type: "text", x: 3, y: 0, tex: "a", cls: "a-pt", anchor: "middle", vAnchor: "top", dy: 5 },
        { type: "text", x: 0, y: 8, tex: "L", cls: "a-pt", anchor: "end", dx: -4 },
      ];
      return {
        layout: "triple",
        panels: [
          {
            svg: base({ items: [{ type: "curve", fn: pow2, domain: [0.45, 3.45], cls: "curve" }, ...labels, { type: "dot", x: 3, y: 8 }] }),
            note: "\\(f(a) = L\\)",
          },
          {
            svg: base({ items: [
              { type: "curve", fn: pow2, domain: [0.45, 2.95], cls: "curve" },
              { type: "curve", fn: pow2, domain: [3.05, 3.45], cls: "curve" },
              ...labels, { type: "dot", x: 3, y: 8, hollow: true }, { type: "dot", x: 3, y: 5 },
            ] }),
            note: "\\(f(a) \\neq L\\)",
          },
          {
            svg: base({ items: [
              { type: "curve", fn: pow2, domain: [0.45, 2.95], cls: "curve" },
              { type: "curve", fn: pow2, domain: [3.05, 3.45], cls: "curve" },
              ...labels, { type: "dot", x: 3, y: 8, hollow: true },
            ] }),
            note: "\\(f(a)\\) is undefined",
          },
        ],
      };
    },

    "read-limit-graph": () => ({
      layout: "single",
      panels: [{
        svg: buildPlot({
          w: 460, h: 280, xmin: -3.3, xmax: 2.9, ymin: -2.7, ymax: 2.8,
          xlabel: "x", ylabel: "y",
          aria: "A function with limit 1 at x = -2, limit 0 at x = 0, and limit 2 at x = 2, although f(2) = -2.",
          xticks: [{ x: -2 }, { x: 2 }],
          items: [
            { type: "curve", fn: (x) => -0.0375 * x * x * x + 0.375 * x * x + 0.4 * x, domain: [-2.8, 1.98], samples: 200, cls: "curve" },
            { type: "dot", x: 2, y: 2, hollow: true },
            { type: "dot", x: 2, y: -2 },
            { type: "text", x: -2.7, y: 1.55, tex: "y=f(x)", cls: "a-curve", anchor: "start" },
          ],
        }),
      }],
    }),

    /* ---------------- §1.4 ---------------- */
    "one-sided-limits": () => ({
      layout: "single",
      panels: [{
        svg: buildPlot({
          w: 420, h: 260, xmin: -0.5, xmax: 4.5, ymin: -0.5, ymax: 3.2,
          xlabel: "x", ylabel: "y", aria: "Different left and right limits at a.",
          xticks: [{ x: 2, tex: "a" }], yticks: [{ y: 1, tex: "L_1" }, { y: 2, tex: "L_2" }],
          items: [
            { type: "curve", fn: (x) => 1 + 0.25 * (x - 2) * (x - 2), domain: [0.2, 1.95], cls: "curve" },
            { type: "curve", fn: (x) => 2 + 0.2 * (x - 2) * (x - 2), domain: [2.05, 4.2], cls: "curve" },
            { type: "dot", x: 2, y: 1, hollow: true }, { type: "dot", x: 2, y: 2, hollow: true },
          ],
        }),
      }],
    }),
    "one-sided-infinite": () => {
      const mk = (fn, dom, ymin, ymax) => buildPlot({
        w: 240, h: 210, xmin: -0.2, xmax: 3.2, ymin, ymax,
        pad: { t: 14, r: 14, b: 20, l: 16 }, xlabel: "x", ylabel: "y",
        aria: "A one-sided infinite limit.",
        xticks: [{ x: 2, tex: "a" }],
        items: [{ type: "vline", x: 2, cls: "refline" }, { type: "curve", fn, domain: dom, samples: 200, cls: "curve" }],
      });
      return {
        layout: "grid",
        panels: [
          { svg: mk((x) => 1 / (2 - x), [0.25, 1.68], -0.55, 3.2), note: "\\(\\lim_{x\\to a^{-}} f(x)=\\infty\\)" },
          { svg: mk((x) => 1 / (x - 2), [2.32, 3.0], -0.55, 3.2), note: "\\(\\lim_{x\\to a^{+}} f(x)=\\infty\\)" },
          { svg: mk((x) => -1 / (2 - x), [0.25, 1.68], -3.0, 0.75), note: "\\(\\lim_{x\\to a^{-}} f(x)=-\\infty\\)" },
          { svg: mk((x) => -1 / (x - 2), [2.32, 3.0], -3.0, 0.75), note: "\\(\\lim_{x\\to a^{+}} f(x)=-\\infty\\)" },
        ],
      };
    },
    "vertical-asymptote": () => ({
      layout: "single",
      panels: [{
        svg: buildPlot({
          w: 420, h: 260, xmin: -1, xmax: 7, ymin: -66, ymax: 66,
          xlabel: "x", ylabel: "y", aria: "Graph with a vertical asymptote at x = 3.",
          xticks: [{ x: 3, tex: "3" }],
          items: [
            { type: "vline", x: 3, cls: "refline" },
            { type: "curve", fn: (x) => (2 * x) / (x - 3), domain: [-0.8, 2.9], samples: 200, cls: "curve" },
            { type: "curve", fn: (x) => (2 * x) / (x - 3), domain: [3.1, 6.8], samples: 200, cls: "curve" },
          ],
        }),
      }],
    }),

    /* ---------------- §1.6 ---------------- */
    "precise-limit": () => {
      const Lm = 6.498019, Lp = 9.849155;
      return {
        layout: "single",
        panels: [{
          svg: buildPlot({
            w: 460, h: 300, xmin: 0, xmax: 3.8, ymin: 0, ymax: 14,
            pad: { t: 16, r: 18, b: 24, l: 58 }, xlabel: "x", ylabel: "y",
            aria: "Geometric interpretation of the epsilon-delta definition.",
            items: [
              { type: "curve", fn: pow2, domain: [0.45, 2.95], cls: "curve" },
              { type: "curve", fn: pow2, domain: [3.05, 3.45], cls: "curve" },
              { type: "hline", y: Lm, from: 0, to: 3.8, cls: "refline" },
              { type: "hline", y: Lp, from: 0, to: 3.8, cls: "refline" },
              { type: "vline", x: 2.7, cls: "refline" },
              { type: "vline", x: 3.3, cls: "refline" },
              { type: "dot", x: 3, y: 8, hollow: true },
              { type: "dot", x: 3, y: 11.6 },
              { type: "dot", x: 2.7, y: Lm, r: 1.8 },
              { type: "dot", x: 3.3, y: Lp, r: 1.8 },
              { type: "text", x: 2.7, y: 0, tex: "a-\\delta", cls: "a-pt", anchor: "middle", vAnchor: "top", dy: 5 },
              { type: "text", x: 3.02, y: 0, tex: "a", cls: "a-pt", anchor: "middle", vAnchor: "top", dy: 5 },
              { type: "text", x: 3.32, y: 0, tex: "a+\\delta", cls: "a-pt", anchor: "middle", vAnchor: "top", dy: 5 },
              { type: "text", x: 0, y: Lm, tex: "L-\\varepsilon", cls: "a-pt", anchor: "end", dx: -4 },
              { type: "text", x: 0, y: 8, tex: "L", cls: "a-pt", anchor: "end", dx: -4 },
              { type: "text", x: 0, y: Lp, tex: "L+\\varepsilon", cls: "a-pt", anchor: "end", dx: -4 },
            ],
          }),
        }],
      };
    },
  };

  function hydrateFigures(root) {
    (root || document).querySelectorAll("[data-fig]").forEach((el) => {
      const def = FIGS[el.dataset.fig];
      if (!def || el.dataset.figDone) return;
      const { layout, panels } = def();
      let html;
      if (layout === "single" && panels.length === 1 && !panels[0].note) {
        html = `<div class="figure-art">${panels[0].svg}</div>`;
      } else {
        const cls = { pair: "figure-art--pair", triple: "figure-art--triple", grid: "figure-art--grid" }[layout] || "";
        html = `<div class="figure-art ${cls}">` +
          panels.map((p) => `<div class="fig-panel">${p.svg}${p.note ? `<div class="fig-note">${p.note}</div>` : ""}</div>`).join("") +
          `</div>`;
      }
      el.insertAdjacentHTML("afterbegin", html);
      el.dataset.figDone = "1";
    });
  }

  window.hydrateFigures = hydrateFigures;
})();

/* ============================================================
   plot.js — tiny function-plotting engine for the Ch.1 figures.
   Reproduces the chapter's pgfplots graphs as inline SVG that
   inherits the handout figure vocabulary (.axis .curve .refline
   .dot) from skin-hs.css.

   Labels are NOT drawn as SVG <text>; they are emitted into a
   full-size <foreignObject> overlay as HTML spans carrying real
   \( … \) math, so the page's existing KaTeX pass typesets them in
   Computer Modern — matching the body equations exactly. Each label
   anchors precisely (left/centre/right × top/middle/bottom) with an
   optional pixel nudge, which fixes positioning.

   buildPlot(cfg) -> SVG markup string.
   Data coords map to a fixed viewBox; axes are drawn "middle"
   (through the origin when 0 is in range, else along the edge).
   ============================================================ */
(function () {
  let uid = 0;
  const PI = Math.PI;

  /* pretty TeX for multiples of pi (axis ticks) */
  function piTex(v) {
    const map = {
      [(-2 * PI).toFixed(4)]: "-2\\pi",
      [(-PI).toFixed(4)]: "-\\pi",
      [(-PI / 2).toFixed(4)]: "-\\tfrac{\\pi}{2}",
      [(PI / 2).toFixed(4)]: "\\tfrac{\\pi}{2}",
      [PI.toFixed(4)]: "\\pi",
      [(2 * PI).toFixed(4)]: "2\\pi",
      [(0).toFixed(4)]: "0",
    };
    return map[v.toFixed(4)];
  }

  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;"); }

  // anchor -> CSS transform (translate by own box) ; vAnchor default middle
  function anchorTransform(anchor, vAnchor) {
    const tx = anchor === "start" ? "0" : anchor === "end" ? "-100%" : "-50%";
    const ty = vAnchor === "top" ? "0" : vAnchor === "bottom" ? "-100%" : "-50%";
    return `translate(${tx},${ty})`;
  }

  function buildPlot(cfg) {
    const w = cfg.w, h = cfg.h;
    const pad = Object.assign({ t: 16, r: 18, b: 20, l: 22 }, cfg.pad || {});
    const { xmin, xmax, ymin, ymax } = cfg;
    const iw = w - pad.l - pad.r, ih = h - pad.t - pad.b;
    const SX = (x) => pad.l + ((x - xmin) / (xmax - xmin)) * iw;
    const SY = (y) => h - pad.b - ((y - ymin) / (ymax - ymin)) * ih;

    const id = "pl" + (++uid);
    const parts = [];
    const labels = []; // {px, py, tex|text, anchor, vAnchor, dx, dy, cls, size}

    function pushLabel(o) {
      labels.push(o);
    }

    parts.push(
      `<svg viewBox="0 0 ${w} ${h}" style="width:${w}px" class="fig-svg" role="img" aria-label="${esc(cfg.aria || "graph")}" preserveAspectRatio="xMidYMid meet">`
    );
    // crisp, smaller arrowhead
    parts.push(
      `<defs><marker id="${id}a" markerWidth="8" markerHeight="8" refX="5.4" refY="2.8" orient="auto" markerUnits="userSpaceOnUse">` +
      `<path d="M0,0 L5.4,2.8 L0,5.6" fill="none" stroke="var(--c-axis)" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>`
    );

    // ---- axes (middle) ----
    if (cfg.axes !== false) {
      const x0 = Math.min(Math.max(0, xmin), xmax);
      const y0 = Math.min(Math.max(0, ymin), ymax);
      const ax0 = SX(xmin), ax1 = SX(xmax), ayBase = SY(y0);
      parts.push(`<path d="M${ax0.toFixed(1)},${ayBase.toFixed(1)} H${(ax1 - 1).toFixed(1)}" class="axis" marker-end="url(#${id}a)"/>`);
      const ay0 = SY(ymin), ay1 = SY(ymax), axBase = SX(x0);
      parts.push(`<path d="M${axBase.toFixed(1)},${ay0.toFixed(1)} V${(ay1 + 1).toFixed(1)}" class="axis" marker-end="url(#${id}a)"/>`);
      if (cfg.xlabel) pushLabel({ px: ax1 + 1, py: ayBase + 4, tex: cfg.xlabel, anchor: "start", vAnchor: "top", cls: "a-ax", size: 13 });
      if (cfg.ylabel) pushLabel({ px: axBase - 5, py: ay1 + 1, tex: cfg.ylabel, anchor: "end", vAnchor: "top", cls: "a-ax", size: 13 });

      // ticks
      (cfg.xticks || []).forEach((t) => {
        const px = SX(t.x);
        parts.push(`<line x1="${px.toFixed(1)}" y1="${(ayBase - 3).toFixed(1)}" x2="${px.toFixed(1)}" y2="${(ayBase + 3).toFixed(1)}" class="axis"/>`);
        const tex = t.tex != null ? t.tex : (t.label != null ? null : piTex(t.x));
        if (tex != null) pushLabel({ px, py: ayBase + 6, tex, anchor: "middle", vAnchor: "top", cls: "a-pt", size: 12 });
        else if (t.label != null) pushLabel({ px, py: ayBase + 6, text: t.label, anchor: "middle", vAnchor: "top", cls: "a-pt", size: 12 });
      });
      (cfg.yticks || []).forEach((t) => {
        const py = SY(t.y);
        parts.push(`<line x1="${(axBase - 3).toFixed(1)}" y1="${py.toFixed(1)}" x2="${(axBase + 3).toFixed(1)}" y2="${py.toFixed(1)}" class="axis"/>`);
        const tex = t.tex != null ? t.tex : (t.label != null ? null : piTex(t.y));
        if (tex != null) pushLabel({ px: axBase - 6, py, tex, anchor: "end", vAnchor: "middle", cls: "a-pt", size: 12 });
        else if (t.label != null) pushLabel({ px: axBase - 6, py, text: t.label, anchor: "end", vAnchor: "middle", cls: "a-pt", size: 12 });
      });
    }

    // ---- items ----
    (cfg.items || []).forEach((it) => {
      if (it.type === "curve") {
        const cls = it.cls || "curve";
        const n = it.samples || 240;
        const [a, b] = it.domain;
        let d = "", pen = false;
        for (let i = 0; i <= n; i++) {
          const x = a + (b - a) * (i / n);
          const y = it.fn(x);
          if (!isFinite(y) || y < ymin - (ymax - ymin) * 0.04 || y > ymax + (ymax - ymin) * 0.04) { pen = false; continue; }
          const px = SX(x).toFixed(2), py = SY(y).toFixed(2);
          d += (pen ? "L" : "M") + px + "," + py + " ";
          pen = true;
        }
        if (d) parts.push(`<path d="${d.trim()}" class="${cls}"/>`);
      } else if (it.type === "vline") {
        parts.push(`<line x1="${SX(it.x).toFixed(1)}" y1="${SY(ymin).toFixed(1)}" x2="${SX(it.x).toFixed(1)}" y2="${SY(ymax).toFixed(1)}" class="${it.cls || "refline"}"/>`);
      } else if (it.type === "hline") {
        const a = it.from != null ? it.from : xmin, b = it.to != null ? it.to : xmax;
        parts.push(`<line x1="${SX(a).toFixed(1)}" y1="${SY(it.y).toFixed(1)}" x2="${SX(b).toFixed(1)}" y2="${SY(it.y).toFixed(1)}" class="${it.cls || "refline"}"/>`);
      } else if (it.type === "seg") {
        parts.push(`<line x1="${SX(it.x1).toFixed(1)}" y1="${SY(it.y1).toFixed(1)}" x2="${SX(it.x2).toFixed(1)}" y2="${SY(it.y2).toFixed(1)}" class="${it.cls || "curve"}"/>`);
      } else if (it.type === "dot") {
        const r = it.r || 3.0;
        if (it.hollow) parts.push(`<circle cx="${SX(it.x).toFixed(1)}" cy="${SY(it.y).toFixed(1)}" r="${r}" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.5"/>`);
        else parts.push(`<circle cx="${SX(it.x).toFixed(1)}" cy="${SY(it.y).toFixed(1)}" r="${r}" class="dot"/>`);
      } else if (it.type === "arrow") {
        parts.push(`<line x1="${SX(it.x1).toFixed(1)}" y1="${SY(it.y1).toFixed(1)}" x2="${SX(it.x2).toFixed(1)}" y2="${SY(it.y2).toFixed(1)}" class="axis" marker-end="url(#${id}a)"/>`);
      } else if (it.type === "text") {
        pushLabel({
          px: SX(it.x), py: SY(it.y),
          tex: it.tex, text: it.tex == null ? it.text : null,
          anchor: it.anchor || "middle",
          vAnchor: it.vAnchor || "middle",
          dx: it.dx || 0, dy: it.dy || 0,
          cls: it.cls || "a-pt",
          size: it.size,
        });
      }
    });

    // ---- label overlay (HTML in an oversized foreignObject; KaTeX typesets it) ----
    // The foreignObject is padded by M on every side and the SVG is overflow:visible,
    // so labels that extend past the plot edge are never clipped.
    if (labels.length) {
      const M = 52;
      const spans = labels.map((L) => {
        const left = (L.px + (L.dx || 0) + M).toFixed(1);
        const top = (L.py + (L.dy || 0) + M).toFixed(1);
        const tf = anchorTransform(L.anchor, L.vAnchor);
        const fs = L.size ? `font-size:${L.size}px;` : "";
        const body = L.tex != null ? `\\(${L.tex}\\)` : esc(L.text == null ? "" : L.text);
        return `<span class="fig-lbl ${L.cls || ""}" style="left:${left}px;top:${top}px;transform:${tf};${fs}">${body}</span>`;
      }).join("");
      parts.push(
        `<foreignObject x="${-M}" y="${-M}" width="${w + 2 * M}" height="${h + 2 * M}" class="fig-fo" requiredExtensions="http://www.w3.org/1999/xhtml">` +
        `<div xmlns="http://www.w3.org/1999/xhtml" class="fig-lyr">${spans}</div>` +
        `</foreignObject>`
      );
    }

    parts.push(`</svg>`);
    return parts.join("");
  }

  window.buildPlot = buildPlot;
  window.PIVAL = PI;
})();

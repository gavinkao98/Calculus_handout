// Figure export: built print-standalone -> one vector PDF per figure panel.
//
//   node export_figs.mjs <standalone.html> <outDir> [figId ...]
//
// Why re-render instead of screenshot: LaTeX wants vector art with embedded fonts, and
// shot.mjs only makes raster PNGs (figure-audit gate). So each panel is re-rendered in a
// throwaway wrapper page sized exactly to the panel, then Page.printToPDF'd.
//
// Fidelity approach: rather than enumerating SVG presentation properties and inlining
// computed values (lossy — miss one property and a stroke silently changes), the wrapper
// copies the page's <style> blocks verbatim and rebuilds the element's ancestor chain
// (class names intact). Descendant selectors (`.paper .curve`), CSS custom properties
// (`--c-axis`, including the var() inside buildPlot's <defs><marker>), and the @font-face
// blocks then apply unchanged. The only injected rule is a trailing @page that overrides
// the standalone's A4 sheet size with the panel's own box.
//
// Panel size is MEASURED in the real page (getBoundingClientRect) and re-asserted in the
// wrapper, so the viewBox->viewport scale stays 1:1 and text keeps its intended size.
// The measured CSS px width is what convert.py turns into a LaTeX width in mm; do not
// read --fig-N-* for this (in ch03 they are all `100%`, while the SVGs carry their own
// inline width) — see out/figures.json.
import { spawn } from "node:child_process";
import { writeFileSync, readFileSync, mkdirSync, existsSync } from "node:fs";
import { createServer } from "node:http";
import { resolve, join, basename } from "node:path";
import { pathToFileURL } from "node:url";

const CHROME = process.env.CHROME ?? [
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  (process.env.LOCALAPPDATA ?? "") + "\\Google\\Chrome\\Application\\chrome.exe",
].find(existsSync);
if (!CHROME) {
  console.error("Chrome not found — install it or set the CHROME env var to chrome.exe");
  process.exit(1);
}

const [, , SRC, OUTDIR, ...ONLY] = process.argv;
if (!SRC || !OUTDIR) {
  console.error("usage: node export_figs.mjs <standalone.html> <outDir> [figId ...]");
  process.exit(1);
}
mkdirSync(OUTDIR, { recursive: true });
const WRAPDIR = join(OUTDIR, "_wrap");
mkdirSync(WRAPDIR, { recursive: true });

const PORT = 9700 + (process.pid % 250);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ── Local fonts, served over http (2026-07-26) ──────────────────────────────────────────
// The standalone pulls its two typefaces from CDNs: Inter from Google Fonts and
// New Computer Modern from jsDelivr (TYPESETTING_GUIDE §9.1). For SCREEN that is fine, but
// for the print line it caused a measured defect: Google Fonts serves a SUBSET of Inter, and
// U+2080 SUBSCRIPT ZERO is not in it. ch03's composed-mapping labels `x₀`/`u₀`/`y₀` therefore
// printed the letter in Inter and the subscript in Times New Roman (Windows' last-resort
// fallback), and the stray Times subsets then failed the glyph gate, which verifies CFF only
// and refuses to silently skip what it cannot verify.
// The repo already ships the COMPLETE Inter OTFs for LaTeX (template/fonts/inter/, U+2080
// present in all six weights) and the LaTeX body text already uses the local NewCM10 OTFs.
// So the two lines were only nominally on "the same font". Serving those same files to the
// exporter makes them genuinely the same file, and as a side effect the export stops needing
// the network at all.
// Why an http server rather than file:// or data: URIs — a webfont is a CORS-checked
// subresource and a file:// page is an opaque origin, so both fail with
// "NetworkError: A network error occurred." even under --allow-file-access-from-files
// (all three measured). http://127.0.0.1 is a normal origin, so the fonts just load.
const INTER_DIR = resolve(new URL(".", import.meta.url).pathname.replace(/^\//, ""), "template/fonts/inter");
const FONT_ROUTES = new Map();

function route(file, abs) {
  if (!existsSync(abs)) {
    console.error(`font not found: ${abs}\nThe print line needs it; see TYPESETTING_GUIDE §9.1.`);
    process.exit(1);
  }
  FONT_ROUTES.set("/fonts/" + file, abs);
  return "/fonts/" + file;
}

// Inter only. New Computer Modern deliberately stays on the CDN: Chrome's OpenType
// Sanitizer REJECTS the TeX-tree NewCM10 OTFs that LuaTeX uses —
//     OTS parsing error: CFF : Failed validating CharStrings INDEX
// for NewCM10-Regular.otf and NewCM10-Italic.otf (Bold and BoldItalic happen to pass).
// So the browser cannot be pointed at the same NCM file the body text uses, and jsDelivr's
// web-sanitised woff2 build of the same typeface remains the only thing it will accept.
// That is also why the glyph gate still sees one unverifiable TrueType subset
// (WebCM-Serif-10-Regular, used by the .fig-lyr annotations) — see REVIEW-ch03-plain-applied.
const INTER = [["Regular", 400, "normal"], ["Medium", 500, "normal"], ["SemiBold", 600, "normal"],
               ["Bold", 700, "normal"], ["Italic", 400, "italic"], ["BoldItalic", 700, "italic"]];

const LOCAL_FONT_CSS = INTER.map(([name, wght, style]) => {
  const url = route(`Inter-${name}.otf`, join(INTER_DIR, `Inter-${name}.otf`));
  return `@font-face{font-family:"Inter";font-style:${style};font-weight:${wght};`
    + `font-display:block;src:url("${url}") format("opentype")}`;
}).join("");

// Drop Google's Inter and install the complete local one. Both halves are required: leaving
// Google's faces in place keeps their unicode-range-scoped subsets winning for latin, which
// is precisely the half-local state that produced the Times fallback for U+2080.
// jsDelivr (New Computer Modern) is deliberately left alone — see the note above.
const GF_LINK = /<link[^>]*(?:googleapis|gstatic)[^>]*>/gi;
const localize = (doc) => doc.replace(GF_LINK, "")
  .replace("</head>", `<style>${LOCAL_FONT_CSS}</style></head>`);

const FILE_PORT = PORT + 250;
const server = createServer((req, res) => {
  const path = decodeURIComponent(req.url.split("?")[0]);
  if (FONT_ROUTES.has(path)) {
    res.writeHead(200, { "content-type": "font/otf" });
    res.end(readFileSync(FONT_ROUTES.get(path)));
    return;
  }
  if (path.startsWith("/w/") && path.endsWith(".html")) {
    const f = join(WRAPDIR, basename(path));
    if (existsSync(f)) {
      res.writeHead(200, { "content-type": "text/html; charset=utf-8" });
      res.end(readFileSync(f));
      return;
    }
  }
  res.writeHead(404); res.end("not found");
});
await new Promise((r) => server.listen(FILE_PORT, "127.0.0.1", r));

const proc = spawn(CHROME, [
  "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  "--hide-scrollbars", `--remote-debugging-port=${PORT}`,
  "--user-data-dir=" + process.env.TEMP + "\\hk-figexport-" + process.pid,
  "--window-size=1120,1600", pathToFileURL(resolve(SRC)).href,
], { stdio: "ignore" });

async function getWs() {
  for (let i = 0; i < 100; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const page = list.find((t) => t.type === "page" && t.webSocketDebuggerUrl);
      if (page) return page.webSocketDebuggerUrl;
    } catch {}
    await sleep(150);
  }
  throw new Error("no CDP page target");
}

const ws = new WebSocket(await getWs());
await new Promise((res) => (ws.onopen = res));
let _id = 0;
const pending = new Map();
ws.onmessage = (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
};
const cmd = (method, params = {}) =>
  new Promise((res) => { const id = ++_id; pending.set(id, res); ws.send(JSON.stringify({ id, method, params })); });
const evalJs = async (expression) =>
  (await cmd("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true })).result?.result?.value;

await cmd("Page.enable");
await cmd("Runtime.enable");
// Font rejections surface only here: a face that Chrome's sanitizer refuses reports a bare
// "NetworkError" to FontFace.load(), while the reason ("Failed to decode downloaded font: …
// OTS parsing error: …") goes to the browser log. Without this the failure is unguessable.
const browserLog = [];
ws.addEventListener("message", (ev) => {
  const m = JSON.parse(ev.data);
  if (m.method === "Log.entryAdded") browserLog.push(m.params.entry.text);
});
await cmd("Log.enable");

// Same readiness signal as shot.mjs: #boot is dropped only after fragments assemble,
// MathJax typesets, figures hydrate and pagination runs. readyState guards the window
// before <body> is parsed, when #boot does not exist yet.
const readyExpr = "document.readyState!=='loading' && !document.getElementById('boot')";
let ok = false;
for (let i = 0; i < 240; i++) { if (await evalJs(readyExpr)) { ok = true; break; } await sleep(200); }
if (!ok) { console.error("page never became ready"); proc.kill(); server.close(); process.exit(1); }
await evalJs("document.fonts.ready");   // webfonts decide text metrics -> measure after
await sleep(400);

// Collect, per figure panel: the wrapper document and the measured box.
// Runs in-page so getComputedStyle/getBoundingClientRect see the real cascade.
const COLLECT = `(() => {
  const head = [...document.querySelectorAll('style')].map(s => '<style>' + s.innerHTML + '</style>').join('\\n')
    + [...document.querySelectorAll('link[rel="stylesheet"], link[rel="preconnect"]')]
        .map(l => l.outerHTML).join('\\n');
  const colWidth = (() => {
    const f = document.querySelector('figure.figure');
    return f ? f.getBoundingClientRect().width : null;
  })();
  const out = [];
  // Panels come from data-fig figures (drawn by the standalone's FIGS at load) AND from
  // figures whose SVG is written inline in the fragment, keyed by their id instead
  // (ch01 Figure 1.2, id fig-map, is the only one in the book; ch03 had none).
  for (const fig of document.querySelectorAll('figure.figure[data-fig], figure.figure[id]')) {
    const id = fig.getAttribute('data-fig') ?? fig.id;
    const svgs = [...fig.querySelectorAll('svg.fig-svg')];
    svgs.forEach((svg, i) => {
      const r = svg.getBoundingClientRect();
      if (r.width < 5 || r.height < 5) return;
      // Export the whole .fig-panel, not the bare <svg>: a panel is
      //   <div class="fig-panel"><svg …>…</svg><div class="fig-note">…</div></div>
      // and the note is a SIBLING of the svg (standalone: hydrateFigures). Cloning only the
      // svg silently dropped it — remainder-tangent (Figure 3.6) lost the "larger h" /
      // "smaller h" captions that say which panel has the bigger h. Verified: the string is
      // in the HTML's own print PDF and was absent from ours.
      const target = svg.closest('.fig-panel') || svg;
      const tr = target.getBoundingClientRect();
      // True ink box = svg UNION its labels UNION its notes. buildPlot deliberately overflows
      // the viewBox: it hangs a <foreignObject x="-52" width="w+104"> outside the plot and puts
      // the MathJax labels in that margin, which .fig-svg{overflow:visible} then shows. Sizing
      // the page to the bare SVG box clips them (sin t/t and cos t lost their theta; the axis
      // label vanished). Union the .fig-lbl spans, NOT .fig-fo — the foreignObject is the full
      // 52px-margin box, most of it empty. Note the ink box is NOT the panel box either: for a
      // single-panel figure the panel is a full-column-width block with the svg centred in it.
      let bx = { l: r.left, t: r.top, r: r.right, b: r.bottom };
      for (const q of [...target.querySelectorAll('.fig-lbl, .fig-note')]
                        .map(e => e.getBoundingClientRect())) {
        if (!q.width && !q.height) continue;
        bx = { l: Math.min(bx.l, q.left), t: Math.min(bx.t, q.top),
               r: Math.max(bx.r, q.right), b: Math.max(bx.b, q.bottom) };
      }
      const PAD = 1;   // guard against sub-pixel AA shaving an outermost glyph
      bx = { l: bx.l - PAD, t: bx.t - PAD, r: bx.r + PAD, b: bx.b + PAD };
      // rebuild the ancestor chain (body -> ... -> target's parent) so descendant
      // selectors and inherited custom properties keep matching in the wrapper.
      // The chain is reproduced for CSS MATCHING only. Its geometry must be neutralised:
      // it contains .sheet (the A4 page box, 210mm + margins), which would otherwise push
      // the figure out of a panel-sized viewport and clip it to a blank corner.
      const chain = [];
      for (let n = target.parentElement; n && n !== document.body; n = n.parentElement) {
        const attrs = [...n.attributes]
          .filter(a => a.name === 'class' || a.name === 'data-fig')
          .map(a => a.name === 'class'
            ? 'class="' + (a.value + ' fx-neutral').replace(/"/g, '&quot;') + '"'
            : a.name + '="' + a.value.replace(/"/g, '&quot;') + '"').join(' ');
        chain.unshift({ tag: n.tagName.toLowerCase(), attrs: attrs || 'class="fx-neutral"' });
      }
      const open = chain.map(c => '<' + c.tag + ' ' + c.attrs + '>').join('');
      const close = chain.map(c => '</' + c.tag + '>').reverse().join('');
      const rnd = (v) => Math.round(v * 100) / 100;
      const w = rnd(tr.width), h = rnd(tr.height);            // the panel's own measured box
      const pw = rnd(bx.r - bx.l), ph = rnd(bx.b - bx.t);     // the page = ink box
      // The panel is reproduced at its MEASURED size and offset so its interior lays out
      // exactly as it did on the real page (the note keeps its position under the plot);
      // the page then crops to the ink. offX/offY are negative for a full-width single panel
      // whose svg is centred — that is correct, the surplus is cropped away.
      const offX = rnd(tr.left - bx.l), offY = rnd(tr.top - bx.t);
      const clone = target.cloneNode(true);
      clone.setAttribute('class', (clone.getAttribute('class') || '') + ' fx-target');
      // Re-assert the SVG's OWN measured size, not just the panel's. The live page can
      // constrain an svg BELOW its inline width through a per-figure custom property
      // (hydrateFigures wires --fig-N-M into --fig-w as an INLINE STYLE on <figure>), and the
      // chain copy above keeps only class/data-fig — so that variable is absent in the wrapper
      // and the svg falls back to its inline width. Measured on recip-x-vs-x2 (Figure 1.16):
      // live 200x161 (max-width 200) vs inline width:244px, viewBox 244x196 → in the wrapper it
      // rendered 244 wide, ~35px taller, which pushed the .fig-note "y = 1/x²" past the page
      // box (sized from the LIVE ink box) and printed the panel with the note missing and the
      // plot cropped. check_prose's figure-note gate caught it; the panel PDF had 1 text char.
      const cloneSvg = clone.matches && clone.matches('svg.fig-svg')
        ? clone : clone.querySelector('svg.fig-svg');
      if (cloneSvg) cloneSvg.setAttribute('class', (cloneSvg.getAttribute('class') || '') + ' fx-svg');
      const doc = '<!doctype html><html lang="en"><head><meta charset="utf-8">' + head
        + '<style>@page{size:' + pw + 'px ' + ph + 'px;margin:0}'
        + 'html,body{margin:0;padding:0;background:#fff;width:' + pw + 'px;height:' + ph + 'px;'
        + 'overflow:hidden;position:relative}'
        // strip the chain's box geometry but keep its class names (and so its cascade)
        + '.fx-neutral{display:block!important;position:static!important;margin:0!important;'
        + 'padding:0!important;border:0!important;outline:0!important;width:auto!important;'
        + 'min-width:0!important;max-width:none!important;height:auto!important;'
        + 'min-height:0!important;max-height:none!important;transform:none!important;'
        + 'box-shadow:none!important;float:none!important;overflow:visible!important;'
        + 'text-align:left!important;background:none!important;columns:auto!important}'
        // pin the panel at its offset inside the ink box, at exactly its measured size
        // (so the viewBox->viewport scale stays 1:1 and label text keeps its intended size)
        + '.fx-target{position:absolute!important;left:' + offX + 'px!important;'
        + 'top:' + offY + 'px!important;'
        + 'margin:0!important;width:' + w + 'px!important;height:' + h + 'px!important;'
        + 'max-width:none!important;max-height:none!important;overflow:visible!important}'
        // pin the svg at ITS measured size too (see fx-svg note above): 1:1 viewBox scale and
        // the panel's interior (note under the plot) lays out exactly as measured.
        + '.fx-svg{width:' + rnd(r.width) + 'px!important;height:' + rnd(r.height) + 'px!important;'
        + 'min-width:0!important;max-width:none!important;max-height:none!important;'
        + 'flex:none!important}'
        + '</style></head><body class="' + document.body.className + '">'
        + open + clone.outerHTML + close + '</body></html>';
      // 申報這個 panel 帶了哪些「文字」（非數學）標籤。check_prose.py 用它逐條驗證那些字
      // 真的抵達 PDF。不能靠「全文詞集比對」代替：實測 remainder-tangent 的 note 是
      // "larger h"，而 "larger" 在課文散文裡也出現（the larger triangle OAC…），詞集比對
      // 找得到就誤判成沒掉——那條閘放行了它本來要抓的 bug。
      const notes = [...target.querySelectorAll('.fig-note')]
        .map(e => e.textContent.trim()).filter(Boolean);
      out.push({ id, panel: i, w, h, pw, ph, notes, doc });
    });
  }
  return JSON.stringify({ colWidth, panels: out });
})()`;

const { colWidth, panels } = JSON.parse(await evalJs(COLLECT));
console.log(`column width = ${colWidth}px   panels = ${panels.length}`);

const wanted = ONLY.length ? panels.filter((p) => ONLY.includes(p.id)) : panels;
if (ONLY.length && wanted.length === 0) {
  console.error("no panel matched:", ONLY.join(", "));
  proc.kill(); server.close(); process.exit(1);
}

const manifest = [];
for (const p of wanted) {
  const base = p.id + (panels.filter((q) => q.id === p.id).length > 1 ? "-" + (p.panel + 1) : "");
  const wrapFile = join(WRAPDIR, base + ".html");
  writeFileSync(wrapFile, localize(p.doc), "utf-8");
  // Served over http (not file://) so the local @font-face URLs above can actually load.
  await cmd("Page.navigate", { url: `http://127.0.0.1:${FILE_PORT}/w/${base}.html` });
  await sleep(250);
  // Force every declared @font-face to actually load before printing. Awaiting
  // document.fonts.ready alone is NOT enough — measured: with the forced load removed,
  // fonts.check() reports false for both NCM and Inter even after ready resolves, and the
  // print silently bakes in system fallbacks. ready only settles pending requests, and on
  // a one-figure page nothing has requested a face yet when it is awaited.
  const fontsOk = await evalJs(`(async () => {
    await Promise.all([...document.fonts].map(f => f.load().catch(() => {})));
    await document.fonts.ready;
    document.body.getBoundingClientRect();
    return JSON.stringify({
      ncm: document.fonts.check('italic 12px "New Computer Modern"'),
      inter: document.fonts.check('12px Inter'),
      // Per-face status: without it a false above says only "something is wrong", and the
      // family/weight/style that actually failed is exactly what you need to fix it.
      faces: [...document.fonts].map(f => f.family + '/' + f.style + '/' + f.weight + '=' + f.status),
    });
  })()`);
  const fs_ = JSON.parse(fontsOk);
  if (!fs_.ncm || !fs_.inter) {
    console.error(`  FAIL ${base}: webfont not loaded (NCM=${fs_.ncm} Inter=${fs_.inter}) — ` +
      "figure text would silently fall back to Times/system sans. The faces are served from " +
      "the local routes above; per-face status:\n    " +
      (fs_.faces || []).filter((f) => /Computer|Inter/.test(f)).join("\n    ") +
      (browserLog.length ? "\n  browser log:\n    " + browserLog.slice(-6).join("\n    ") : ""));
    proc.kill(); server.close(); process.exit(1);
  }
  await sleep(150);
  const { data } = (await cmd("Page.printToPDF", {
    printBackground: true,
    preferCSSPageSize: true,     // honour the injected @page size
    scale: 1,
    marginTop: 0, marginBottom: 0, marginLeft: 0, marginRight: 0,
  })).result;
  const pdf = join(OUTDIR, base + ".pdf");
  writeFileSync(pdf, Buffer.from(data, "base64"));
  // px -> mm against the measured text column (150mm live area, TYPESETTING_GUIDE §9).
  // Scale off the PAGE box (ink incl. overflowing labels) — that is what the PDF contains,
  // so this reproduces the HTML's on-page size. NOT --fig-N-* (all `100%` in ch03).
  const mm = Math.round((p.pw / colWidth) * 150 * 100) / 100;
  manifest.push({
    id: p.id, panel: p.panel, file: base + ".pdf",
    pagePx: [p.pw, p.ph], panelPx: [p.w, p.h], mm, notes: p.notes,
  });
  console.log(`  wrote ${base}.pdf  page ${p.pw}x${p.ph}px (panel ${p.w}x${p.h}) -> ${mm}mm wide`);
}

writeFileSync(join(OUTDIR, "figures.json"),
  JSON.stringify({ colWidthPx: colWidth, liveWidthMm: 150, panels: manifest }, null, 2), "utf-8");
console.log("manifest: " + join(OUTDIR, "figures.json"));
proc.kill(); server.close();
process.exit(0);

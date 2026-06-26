// Minimal dependency-free CDP screenshotter (Node >=21 for global WebSocket/fetch).
// Launches headless Chrome, waits for a readiness expression, then captures the full
// page, each <figure>, or each .sheet, at 2x device scale. Used to verify handout
// render fidelity and to feed rendered figure PNGs to the figure-audit subagent (gate 1).
//
//   node shot.mjs <url> <outDir/prefix> <mode> [readyExpr]
//     mode = "full"    -> prefix.png
//            "figures" -> prefix-<data-fig>.png, one per <figure class="figure">
//            "sheets"  -> prefix-pNN.png, one per .sheet
//
// Readiness: the default waits for the "#boot" overlay (the standalone's "Preparing …"
// curtain) to be removed — build() drops it only AFTER fragments assemble, MathJax
// typesets, figures hydrate, and pagination runs. So `!document.getElementById('boot')`
// is the signal that the page is fully rendered. Pass a custom [readyExpr] to override.
// NOTE: the print-standalone paginates via CSS @page, NOT .sheet divs, so "sheets" mode
// finds nothing on it — use "figures" (per-figure, for figure-audit) or "full".
//
import { spawn } from "node:child_process";
import { writeFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";

// Chrome path: honour $CHROME, else probe the usual Windows install locations.
// (Hardcoding one path silently broke on machines where Chrome lives elsewhere.)
const CHROME = process.env.CHROME ?? [
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  (process.env.LOCALAPPDATA ?? "") + "\\Google\\Chrome\\Application\\chrome.exe",
].find(existsSync);
if (!CHROME) {
  console.error("Chrome not found — install it or set the CHROME env var to chrome.exe");
  process.exit(1);
}
const [, , URL_, PREFIX, MODE = "sheets", READY] = process.argv;
if (PREFIX) mkdirSync(dirname(PREFIX), { recursive: true }); // ensure the output dir exists
// Unique per-run profile + port: a reused user-data-dir can be locked by a lingering
// headless Chrome from a previous run, which silently yields a stale/blank page.
const PORT = 9300 + (process.pid % 400);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const proc = spawn(CHROME, [
  "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  "--hide-scrollbars", `--remote-debugging-port=${PORT}`,
  "--user-data-dir=" + process.env.TEMP + "\\hk-chrome-cdp-" + process.pid,
  "--window-size=1120,1600", URL_,
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

// wait for readiness — default: the DOM is parsed AND the "#boot" Preparing-overlay has
// been removed (build complete: fragments assembled, MathJax typeset, figures hydrated,
// paginated, off-screen source template removed). The readyState!=='loading' guard is
// essential: #boot is static markup, so a bare !#boot is briefly TRUE *before* the body is
// parsed (and #boot exists) — capturing then grabs the half-built, off-screen page.
const readyExpr = READY || "document.readyState!=='loading' && !document.getElementById('boot')";
let ok = false;
for (let i = 0; i < 240; i++) { if (await evalJs(readyExpr)) { ok = true; break; } await sleep(200); }
await sleep(500); // settle
const errs = await evalJs("document.querySelectorAll('.katex-error').length");
const mjxN = await evalJs("document.querySelectorAll('mjx-container,.katex').length");
console.log(`ready=${ok}  math=${mjxN}  katex-errors=${errs}`);

const shoot = async (clip, file) => {
  const { data } = (await cmd("Page.captureScreenshot", {
    format: "png", captureBeyondViewport: true,
    clip: { ...clip, scale: 2 },
  })).result;
  writeFileSync(file, Buffer.from(data, "base64"));
  console.log("  wrote", file, `(${clip.width}x${clip.height})`);
};

if (MODE === "full") {
  const dims = JSON.parse(await evalJs(
    "JSON.stringify({w:document.documentElement.scrollWidth,h:document.documentElement.scrollHeight})"));
  await shoot({ x: 0, y: 0, width: dims.w, height: dims.h }, `${PREFIX}.png`);
} else if (MODE === "figures") {
  // Per-figure PNGs for the figure-audit gate: one crop per visible <figure class="figure">,
  // named by data-fig / id. Works regardless of pagination (the print-standalone has no
  // .sheet divs). Off-screen (un-paginated source template) and 0-size figures are skipped.
  await sleep(300); // small settle after build completes
  const PAD = 14;
  const figs = JSON.parse(await evalJs(
    "JSON.stringify([...document.querySelectorAll('figure.figure')].map((el,i)=>{const r=el.getBoundingClientRect();" +
    "return {name:(el.getAttribute('data-fig')||el.id||('fig'+i)),x:r.left+scrollX,y:r.top+scrollY,w:r.width,h:r.height};}))"));
  console.log(`  ${figs.length} figure(s)`);
  for (const fg of figs) {
    if (fg.w < 5 || fg.h < 5 || fg.x < -100) { console.log("  skip", fg.name, "(empty/off-screen)"); continue; }
    await shoot({
      x: Math.max(0, Math.round(fg.x - PAD)), y: Math.max(0, Math.round(fg.y - PAD)),
      width: Math.round(fg.w + 2 * PAD), height: Math.round(fg.h + 2 * PAD),
    }, `${PREFIX}-${fg.name}.png`);
  }
} else {
  const rects = JSON.parse(await evalJs(
    "JSON.stringify([...document.querySelectorAll('.sheet')].map(el=>{const r=el.getBoundingClientRect();" +
    "return {x:r.left+scrollX,y:r.top+scrollY,w:r.width,h:r.height};}))"));
  console.log(`  ${rects.length} sheet(s)`);
  if (!rects.length) console.log("  (no .sheet found — this standalone paginates via CSS @page; use mode 'figures' or 'full')");
  for (let i = 0; i < rects.length; i++) {
    const r = rects[i];
    await shoot({ x: Math.round(r.x), y: Math.round(r.y), width: Math.round(r.w), height: Math.round(r.h) },
      `${PREFIX}-p${String(i + 1).padStart(2, "0")}.png`);
  }
}

ws.close();
proc.kill();
process.exit(0);

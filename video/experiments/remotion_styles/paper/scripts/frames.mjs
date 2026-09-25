// Render several stills from one or more compositions with ONE browser.
//   node scripts/frames.mjs <outDir> <compId>:<frame>[,<frame>...] [...more]
//   e.g. node scripts/frames.mjs out/check S-intro:20,90,300 Act3:1200
// Frames may be given as seconds with an "s" suffix (e.g. 12.5s).
// Requires `npx remotion bundle` first (reads ./build).
// Input props (e.g. another manifest): PROPS='{"manifest":"audio/q7zh_beat/manifest.json"}' node scripts/frames.mjs …
import { openBrowser, renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";
import fs from "node:fs";

const [outDir, ...specs] = process.argv.slice(2);
fs.mkdirSync(outDir, { recursive: true });
const serveUrl = path.resolve("build");
const inputProps = process.env.PROPS ? JSON.parse(process.env.PROPS) : {};
const browser = await openBrowser("chrome");
for (const spec of specs) {
  const [id, list] = spec.split(":");
  const composition = await selectComposition({ serveUrl, id, puppeteerInstance: browser, inputProps });
  for (const raw of list.split(",")) {
    const frame = raw.endsWith("s") ? Math.round(parseFloat(raw) * composition.fps) : parseInt(raw, 10);
    const f = Math.min(frame, composition.durationInFrames - 1);
    const output = path.join(outDir, `${id}_${String(f).padStart(5, "0")}.png`);
    await renderStill({ composition, serveUrl, frame: f, output, puppeteerInstance: browser, inputProps: composition.props, imageFormat: "png" });
    console.log(output);
  }
}
await browser.close({ silent: true });

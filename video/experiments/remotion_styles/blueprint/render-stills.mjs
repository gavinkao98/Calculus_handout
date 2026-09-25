// 一次輸出四張風格幀（共用同一個 bundle，比逐張 `npx remotion still` 快）
// 用法：node render-stills.mjs [--frames 30,95,...]  （--frames 另抽 MotionTest 的幀到 out/check/）
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";

const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const jobs = [
  ["F0-title", "out/frames/F0_title.png"],
  ["F1-theorem", "out/frames/F1_theorem.png"],
  ["F2-slope-height", "out/frames/F2_slope_height.png"],
  ["F3-cycle", "out/frames/F3_cycle.png"],
];
const i = process.argv.indexOf("--frames");
const only = process.argv.indexOf("--only");
const frames = i > 0 ? process.argv[i + 1].split(",").map(Number) : [];
const pick = only > 0 ? process.argv[only + 1].split(",") : null;
for (const [id, output] of jobs) {
  if (pick && !pick.includes(id)) continue;
  const composition = await selectComposition({ serveUrl, id });
  await renderStill({ composition, serveUrl, output, overwrite: true });
  console.log("wrote", output);
}
if (frames.length) {
  const composition = await selectComposition({ serveUrl, id: "MotionTest" });
  for (const f of frames) {
    const output = `out/check/mt_${String(f).padStart(3, "0")}.png`;
    await renderStill({ composition, serveUrl, output, frame: f, overwrite: true });
    console.log("wrote", output);
  }
}

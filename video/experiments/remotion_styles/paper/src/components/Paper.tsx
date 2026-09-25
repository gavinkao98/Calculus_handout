import React from "react";
import { AbsoluteFill } from "remotion";
import { color } from "../theme";

/**
 * Laid paper: flat stock colour + large soft mottling + a grain tile
 * (specks and fibres) generated once, deterministically, on a canvas.
 * It lives on the page, so it moves with the Camera like a real sheet.
 *
 * Act 3 (file-size pass): the speck noise is generated at half resolution
 * (256 px, shown at 512 px → soft, low-frequency) and at ~⅓ the old alpha.
 * Per-pixel noise that moves with the camera is what x264 cannot predict;
 * the motion test (full-res specks, crf 16) ran 2.8 MB/s, this runs well
 * under 1 MB/s at crf 20 while still reading as paper, not flat colour.
 */
let grainUrl: string | null = null;
const grain = (): string => {
  if (grainUrl) return grainUrl;
  const N = 256; // drawn at half-res, displayed at 512 px (see note above)
  const c = document.createElement("canvas");
  c.width = N;
  c.height = N;
  const ctx = c.getContext("2d")!;
  let s = 20260925;
  const rnd = () => {
    s = (Math.imul(s, 1664525) + 1013904223) >>> 0;
    return s / 4294967296;
  };
  const img = ctx.createImageData(N, N);
  for (let i = 0; i < N * N; i++) {
    const v = rnd();
    const dark = v > 0.5;
    img.data[i * 4 + 0] = dark ? 92 : 255;
    img.data[i * 4 + 1] = dark ? 72 : 252;
    img.data[i * 4 + 2] = dark ? 44 : 240;
    img.data[i * 4 + 3] = Math.floor(Math.abs(v - 0.5) * 2 * (v > 0.992 ? 46 : 6));
  }
  ctx.putImageData(img, 0, 0);
  // fibres
  ctx.lineCap = "round";
  for (let k = 0; k < 40; k++) {
    const x = rnd() * N;
    const y = rnd() * N;
    const a = rnd() * Math.PI * 2;
    const L = 4 + rnd() * 14;
    ctx.strokeStyle = `rgba(120, 96, 60, ${0.05 + rnd() * 0.08})`;
    ctx.lineWidth = 0.4 + rnd() * 0.4;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.quadraticCurveTo(
      x + Math.cos(a) * L * 0.5 + (rnd() - 0.5) * 8,
      y + Math.sin(a) * L * 0.5 + (rnd() - 0.5) * 8,
      x + Math.cos(a) * L,
      y + Math.sin(a) * L,
    );
    ctx.stroke();
  }
  grainUrl = c.toDataURL("image/png");
  return grainUrl;
};

export const Paper: React.FC<{ w: number; h: number }> = ({ w, h }) => (
  <div
    style={{
      position: "absolute",
      left: 0,
      top: 0,
      width: w,
      height: h,
      backgroundColor: color.paper,
      backgroundImage: [
        "radial-gradient(ellipse 70% 60% at 28% 22%, rgba(255,253,246,0.55), rgba(255,253,246,0) 70%)",
        "radial-gradient(ellipse 60% 55% at 82% 88%, rgba(160,136,96,0.10), rgba(160,136,96,0) 70%)",
        "radial-gradient(ellipse 40% 50% at 6% 92%, rgba(160,136,96,0.07), rgba(160,136,96,0) 70%)",
      ].join(","),
    }}
  >
    <div
      style={{
        position: "absolute",
        inset: 0,
        backgroundImage: `url(${grain()})`,
        backgroundSize: "512px 512px",
      }}
    />
  </div>
);

/** Screen-fixed light falloff: a lamp over the desk, not part of the page. */
export const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{
      pointerEvents: "none",
      background:
        "radial-gradient(ellipse 85% 80% at 50% 45%, rgba(0,0,0,0) 60%, rgba(70,50,20,0.10) 100%)",
    }}
  />
);

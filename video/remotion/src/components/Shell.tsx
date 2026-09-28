import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { useFontsReady } from "../fonts";
import { color, font, features, grid, type } from "../theme";
import { Paper, Vignette } from "./Paper";
import { Rule, SmallCaps } from "./Type";

/**
 * Rostrum camera: the page is a physical sheet under a lens.  (cx, cy) is
 * the page point at the centre of the frame, s the magnification.
 */
export const Camera: React.FC<{ cx: number; cy: number; s: number; children: React.ReactNode }> = ({
  cx,
  cy,
  s,
  children,
}) => (
  <AbsoluteFill style={{ overflow: "hidden" }}>
    <div
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        transformOrigin: "0 0",
        transform: `translate(${960 - cx * s}px, ${540 - cy * s}px) scale(${s})`,
      }}
    >
      {children}
    </div>
  </AbsoluteFill>
);

/** The brand device (logo SVGs are used untouched; only the variant is chosen). */
export const BrandIcon: React.FC<{ x: number; y: number; h: number; opacity?: number }> = ({ x, y, h, opacity = 1 }) => (
  <Img src={staticFile("brand/icon-color.svg")} style={{ position: "absolute", left: x, top: y, height: h, width: h, opacity }} />
);
export const BrandLockup: React.FC<{ x: number; y: number; h: number; opacity?: number; style?: React.CSSProperties }> = ({
  x,
  y,
  h,
  opacity = 1,
  style,
}) => (
  <Img
    src={staticFile("brand/lockup-color-outlined.svg")}
    style={{ position: "absolute", left: x, top: y, height: h, width: (h * 1040) / 300, opacity, ...style }}
  />
);

export type ShellProps = {
  w?: number;
  h?: number;
  head?: { left: string; right: string; folio: string } | null;
  headFrom?: number; // frame the running head inks in (undefined = already there)
  headRight?: number; // opacity of the recto half of the running head (motion: hide while off-frame)
  device?: boolean; // brand icon in the foot margin
  children?: React.ReactNode;
};

/**
 * One page of the book: paper, running head (small caps · italic · folio),
 * hairline, and the brand device in the foot margin.  Children render in
 * page coordinates once the fonts are loaded.
 */
export const Page: React.FC<ShellProps> = ({ w = grid.w, h = grid.h, head, headFrom, headRight = 1, device = true, children }) => {
  const ready = useFontsReady();
  const mx = grid.marginX;
  return (
    <div style={{ position: "relative", width: w, height: h }}>
      {/* .halo = paper-coloured knockout behind labels that sit on lines */}
      <style>{`.halo path, .halo rect, .halo text { stroke: ${color.paper}; stroke-width: 9px; paint-order: stroke fill; stroke-linejoin: round; vector-effect: non-scaling-stroke; }`}</style>
      <Paper w={w} h={h} />
      {ready && head && (
        <>
          <div style={{ position: "absolute", left: mx, top: grid.headY - 26 }}>
            <SmallCaps>{head.left}</SmallCaps>
          </div>
          <div
            style={{
              position: "absolute",
              right: mx,
              top: grid.headY - 33,
              fontFamily: font.serif,
              fontSize: type.caption,
              fontStyle: "italic",
              color: color.ink2,
              fontFeatureSettings: features.text,
              display: "flex",
              gap: 28,
              alignItems: "baseline",
              opacity: headRight,
            }}
          >
            <span>{head.right}</span>
            <span style={{ fontStyle: "normal", color: color.ink, fontFeatureSettings: "'onum' 1" }}>{head.folio}</span>
          </div>
          <Rule x={mx} y={grid.headRuleY} w={w - 2 * mx} from={headFrom} len={24} color={color.rule} />
        </>
      )}
      {device && <BrandIcon x={w - mx - 44} y={h - 78} h={44} />}
      {ready && children}
    </div>
  );
};

/** A full-frame still/scene: page + lamp vignette. */
export const SceneShell: React.FC<ShellProps> = (p) => (
  <AbsoluteFill style={{ backgroundColor: color.paper }}>
    <Page {...p} />
    <Vignette />
  </AbsoluteFill>
);

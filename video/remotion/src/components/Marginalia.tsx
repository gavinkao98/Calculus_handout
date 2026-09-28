import React from "react";
import { color, features, font, grid, type } from "../theme";
import { SmallCaps } from "./Type";

/** Figure number (small caps, rubric red) + italic caption, in the sidenote column. */
export const FigureCaption: React.FC<{ n: string; y: number; children: React.ReactNode; x?: number; w?: number }> = ({
  n,
  y,
  children,
  x = grid.side.x,
  w = grid.side.w,
}) => (
  <div style={{ position: "absolute", left: x, top: y, width: w }}>
    <SmallCaps color={color.accent}>Figure {n}</SmallCaps>
    <div
      style={{
        marginTop: 14,
        fontFamily: font.serif,
        fontStyle: "italic",
        fontSize: type.caption - 2,
        lineHeight: 1.3,
        color: color.ink2,
        fontFeatureSettings: features.text,
      }}
    >
      {children}
    </div>
  </div>
);

/** A numbered sidenote: raised numeral + small roman text. */
export const Sidenote: React.FC<{ n?: string; y: number; children: React.ReactNode; x?: number; w?: number }> = ({
  n,
  y,
  children,
  x = grid.side.x,
  w = grid.side.w,
}) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: w,
      fontFamily: font.serif,
      fontSize: type.micro + 4,
      lineHeight: 1.36,
      color: color.ink2,
      fontFeatureSettings: features.text,
    }}
  >
    {n && <span style={{ color: color.accent, fontFeatureSettings: "'lnum' 1", marginRight: 6 }}>{n}</span>}
    {children}
  </div>
);

/** Superscript note marker in running text. */
export const NoteRef: React.FC<{ n: string }> = ({ n }) => (
  <sup style={{ color: color.accent, fontSize: "0.58em", fontFeatureSettings: "'lnum' 1", marginLeft: 2, fontStyle: "normal" }}>{n}</sup>
);

/** Equation number, set flush right at the text block edge. */
export const EqNumber: React.FC<{ y: number; n: string; right?: number; opacity?: number }> = ({ y, n, right = grid.w - grid.marginX, opacity = 1 }) => (
  <div
    style={{
      position: "absolute",
      left: right,
      translate: "-100% 0",
      top: y,
      fontFamily: font.serif,
      fontSize: type.body,
      color: color.ink2,
      fontFeatureSettings: "'onum' 1, 'kern' 1",
      opacity,
    }}
  >
    ({n})
  </div>
);

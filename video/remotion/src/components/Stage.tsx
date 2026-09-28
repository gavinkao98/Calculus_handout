/**
 * MathStage — keyframed, token-level typesetting.
 *
 * A stage is a bag of named pieces (TeX fragments, Garamond words, fraction
 * bars) and a list of keyframes, each giving every *present* piece a pose
 * (page x of its left edge, baseline y, size, opacity, colour).  Between two
 * keyframes a piece that exists in both glides on the token spring (with a
 * small arc so crossing glyphs never collide); a piece that appears inks in,
 * one that disappears lifts away; a bar draws on from its left end.
 *
 * This is how every derivation in the act moves: the "2" that slides under
 * the h, the product that flies from the margin into the numerator, the table
 * entries that bend into the derivative ring — all the same primitive.
 */
import React from "react";
import { interpolate, interpolateColors, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { tex } from "../math/tex";
import { color, ease, font, springs, stroke } from "../theme";
import { TokenGlyph } from "./Formula";
import { clamp, measure } from "./Type";

export type Piece = { tex?: string; text?: string; italic?: boolean; color?: string; bar?: boolean };
export type Pose = {
  x: number; // left edge (bars: left end)
  y: number; // baseline (bars: the rule's y)
  size: number;
  o?: number; // opacity
  c?: string; // colour override
  w?: number; // bars: length
  delay?: number; // frames after the keyframe before this piece moves
};
export type Poses = Record<string, Pose>;
export type Key = { at: number; poses: Poses };

// ── Metrics ──────────────────────────────────────────────────────────────
const k = (size: number) => (size * font.mathScale) / 1000;
export const pieceW = (p: Piece, size: number) =>
  p.tex !== undefined ? tex(p.tex).w * k(size) : measure(p.text ?? "", size, { italic: p.italic });
const ascent = (p: Piece, size: number) => (p.tex !== undefined ? -tex(p.tex).minY * k(size) : 0.66 * size);
const descent = (p: Piece, size: number) => (p.tex !== undefined ? (tex(p.tex).h + tex(p.tex).minY) * k(size) : 0.22 * size);

// ── Layout ───────────────────────────────────────────────────────────────
/** A row item: a piece key, [key, gap-before in em], or a built-up fraction. */
export type Item = string | [string, number] | { num: Item[]; den: Item[]; bar: string; gap?: number };

const AXIS = 0.25; // math axis height (em of the math font)

type Measured = { w: number; place: (x: number, y: number) => Poses };

const measureRow = (P: Record<string, Piece>, items: Item[], size: number): Measured => {
  const parts: { gap: number; m: Measured }[] = items.map((it, i) => {
    if (typeof it === "string" || Array.isArray(it)) {
      const key = typeof it === "string" ? it : it[0];
      const p = P[key];
      if (!p) throw new Error(`stage: unknown piece ${key}`);
      const gapEm = Array.isArray(it) ? it[1] : p.tex !== undefined ? 0.16 : 0.26;
      const w = pieceW(p, size);
      return { gap: i === 0 ? 0 : gapEm * size, m: { w, place: (x, y) => ({ [key]: { x, y, size } }) } };
    }
    const num = measureRow(P, it.num, size);
    const den = measureRow(P, it.den, size);
    const pad = 0.14 * size;
    const w = Math.max(num.w, den.w) + 2 * pad;
    const dn = Math.max(...it.num.map((n) => descent(P[typeof n === "string" ? n : Array.isArray(n) ? n[0] : n.bar], size)), 0);
    const ad = Math.max(...it.den.map((n) => ascent(P[typeof n === "string" ? n : Array.isArray(n) ? n[0] : n.bar], size)), 0);
    return {
      gap: i === 0 ? 0 : (it.gap ?? 0.2) * size,
      m: {
        w,
        place: (x, y) => {
          const barY = y - AXIS * size * font.mathScale;
          return {
            ...num.place(x + (w - num.w) / 2, barY - 0.16 * size - dn),
            ...den.place(x + (w - den.w) / 2, barY + 0.16 * size + ad),
            [it.bar]: { x, y: barY, size, w },
          };
        },
      },
    };
  });
  const w = parts.reduce((s, p) => s + p.gap + p.m.w, 0);
  return {
    w,
    place: (x0, y) => {
      let x = x0;
      let out: Poses = {};
      parts.forEach((p) => {
        x += p.gap;
        out = { ...out, ...p.m.place(x, y) };
        x += p.m.w;
      });
      return out;
    },
  };
};

/** Poses for a row whose left edge (or centre / right edge) is at x, baseline y. */
export const row = (
  P: Record<string, Piece>,
  items: Item[],
  x: number,
  y: number,
  size: number,
  align: "left" | "center" | "right" = "left",
): Poses => {
  const m = measureRow(P, items, size);
  const x0 = align === "center" ? x - m.w / 2 : align === "right" ? x - m.w : x;
  return m.place(x0, y);
};
export const rowWidth = (P: Record<string, Piece>, items: Item[], size: number) => measureRow(P, items, size).w;

/** Copy poses with overrides (e.g. dim a whole line). */
export const withPose = (p: Poses, over: Partial<Pose>): Poses =>
  Object.fromEntries(Object.entries(p).map(([k2, v]) => [k2, { ...v, ...over }]));

/** Right edge of a laid-out piece (for hanging annotations off it). */
export const extent = (P: Record<string, Piece>, poses: Poses, key: string) => {
  const q = poses[key];
  const p = P[key];
  const w = p.bar ? q.w ?? 0 : pieceW(p, q.size);
  return { x0: q.x, x1: q.x + w, cx: q.x + w / 2, y: q.y };
};

// ── Render ───────────────────────────────────────────────────────────────
export const MathStage: React.FC<{ pieces: Record<string, Piece>; keys: Key[]; opacity?: number }> = ({
  pieces,
  keys,
  opacity = 1,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const out: React.ReactNode[] = [];
  let i = -1;
  keys.forEach((kf, j) => {
    if (kf.at <= frame) i = j;
  });
  if (i < 0) return null;

  for (const [key, piece] of Object.entries(pieces)) {
    const cur = keys[i].poses[key];
    // keyframes are complete snapshots: a piece missing from one is absent there
    const prevKey = keys[i - 1]?.poses[key];
    const base = piece.color ?? color.ink;
    if (!cur && !prevKey) continue;
    const T = keys[i].at + (cur?.delay ?? 0);
    const f = frame - T;
    if (cur && prevKey) {
      const t = spring({ frame: f, fps, config: springs.token });
      const lin = interpolate(f, [0, 24], [0, 1], clamp);
      const dx = cur.x - prevKey.x;
      const amp = 0.38 * cur.size * Math.min(1, Math.abs(dx) / (3 * cur.size));
      const arc = piece.bar ? 0 : Math.sin(Math.PI * lin) * amp * (dx < 0 ? -1 : 1); // rules slide flat
      const size = prevKey.size + (cur.size - prevKey.size) * t;
      const o = (prevKey.o ?? 1) + ((cur.o ?? 1) - (prevKey.o ?? 1)) * interpolate(f, [0, 14], [0, 1], clamp);
      const c = interpolateColors(Math.min(1, Math.max(0, t)), [0, 1], [prevKey.c ?? base, cur.c ?? base]);
      const x = prevKey.x + dx * t;
      const y = prevKey.y + (cur.y - prevKey.y) * t + arc;
      if (piece.bar) {
        const w = (prevKey.w ?? 0) + ((cur.w ?? 0) - (prevKey.w ?? 0)) * t;
        out.push(<line key={key} x1={x} y1={y} x2={x + w} y2={y} stroke={c} strokeWidth={Math.max(2.2, size * 0.045)} strokeLinecap="round" opacity={o * opacity} />);
      } else {
        out.push(<TokenGlyph key={key} t={{ key, ...piece }} x={x} y={y} size={size} opacity={o * opacity} fill={c} />);
      }
    } else if (cur) {
      // ink in
      const q = interpolate(f, [0, 16], [0, 1], { ...clamp, easing: ease.out });
      if (q <= 0) continue;
      const c = cur.c ?? base;
      if (piece.bar) {
        const d = interpolate(f, [0, 18], [0, 1], { ...clamp, easing: ease.ink });
        out.push(
          <line key={key} x1={cur.x} y1={cur.y} x2={cur.x + (cur.w ?? 0) * d} y2={cur.y} stroke={c} strokeWidth={Math.max(2.2, cur.size * 0.045)} strokeLinecap="round" opacity={(cur.o ?? 1) * opacity} />,
        );
      } else {
        out.push(
          <TokenGlyph key={key} t={{ key, ...piece }} x={cur.x} y={cur.y + (1 - q) * cur.size * 0.16} size={cur.size} opacity={q * (cur.o ?? 1) * opacity} fill={c} />,
        );
      }
    } else if (prevKey) {
      // lift away
      const q = interpolate(frame - keys[i].at, [0, 12], [1, 0], { ...clamp, easing: ease.out });
      if (q <= 0) continue;
      const c = prevKey.c ?? base;
      if (piece.bar) {
        out.push(<line key={key} x1={prevKey.x} y1={prevKey.y} x2={prevKey.x + (prevKey.w ?? 0)} y2={prevKey.y} stroke={c} strokeWidth={stroke.hairline * 1.5} opacity={q * (prevKey.o ?? 1) * opacity} />);
      } else {
        out.push(
          <TokenGlyph key={key} t={{ key, ...piece }} x={prevKey.x} y={prevKey.y - (1 - q) * prevKey.size * 0.2} size={prevKey.size} opacity={q * (prevKey.o ?? 1) * opacity} fill={c} />,
        );
      }
    }
  }
  return <g>{out}</g>;
};

/**
 * Token-addressable typesetting.  A formula is a list of tokens — TeX
 * fragments (MathJax/Pagella glyphs) or Garamond words — each with a stable
 * `key`.  Layout is computed synchronously (MathJax metrics + canvas text
 * metrics), so two token lists can be morphed: shared keys glide on a
 * spring, the rest fade.  Everything renders in one SVG with the baseline
 * of the first line at y = 0.
 */
import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { tex } from "../math/tex";
import { color, ease, features, font, springs } from "../theme";
import { clamp, measure } from "./Type";

export type Token = {
  key: string;
  tex?: string; // math fragment
  text?: string; // Garamond words
  italic?: boolean;
  color?: string;
  gap?: number; // em of space before this token (default 0.22 text / 0.12 math)
  br?: boolean; // start a new line
  scale?: number; // relative size
};

export type Placed = { tok: Token; x: number; y: number; w: number; size: number };

export type LayoutOpts = { size: number; align?: "left" | "center" | "right"; leading?: number };

const tokenWidth = (t: Token, size: number) => {
  if (t.tex !== undefined) {
    const g = tex(t.tex);
    return (g.w / 1000) * size * font.mathScale;
  }
  return measure(t.text ?? "", size, { italic: t.italic });
};

export const layout = (tokens: Token[], o: LayoutOpts): { items: Placed[]; width: number } => {
  const lines: Placed[][] = [[]];
  const cursor = [0];
  tokens.forEach((t, i) => {
    const size = o.size * (t.scale ?? 1);
    if (t.br && i > 0) {
      lines.push([]);
      cursor.push(0);
    }
    const L = lines.length - 1;
    const first = lines[L].length === 0;
    const gap = first ? 0 : (t.gap ?? (t.tex !== undefined ? 0.12 : 0.24)) * o.size;
    const w = tokenWidth(t, size);
    lines[L].push({ tok: t, x: cursor[L] + gap, y: L * o.size * (o.leading ?? 1.25), w, size });
    cursor[L] += gap + w;
  });
  const width = Math.max(...cursor);
  const items: Placed[] = [];
  lines.forEach((line, L) => {
    const lw = cursor[L];
    const off = o.align === "center" ? -lw / 2 : o.align === "right" ? -lw : 0;
    line.forEach((p) => items.push({ ...p, x: p.x + off }));
  });
  return { items, width };
};

/** One token drawn with its left edge at x and baseline at y. */
export const TokenGlyph: React.FC<{
  t: Token;
  x: number;
  y: number;
  size: number;
  opacity?: number;
  fill?: string;
}> = ({ t, x, y, size, opacity = 1, fill }) => {
  const c = fill ?? t.color ?? color.ink;
  if (t.tex !== undefined) {
    const g = tex(t.tex);
    const k = (size * font.mathScale) / 1000;
    return (
      <g
        transform={`translate(${x - g.minX * k} ${y}) scale(${k})`}
        style={{ color: c }}
        opacity={opacity}
        dangerouslySetInnerHTML={{ __html: g.body }}
      />
    );
  }
  return (
    <text
      x={x}
      y={y}
      fill={c}
      opacity={opacity}
      style={{
        fontFamily: font.serif,
        fontSize: size,
        fontStyle: t.italic ? "italic" : "normal",
        fontFeatureSettings: features.text,
      }}
    >
      {t.text}
    </text>
  );
};

/** An absolutely-positioned SVG whose (0,0) sits at page point (x, y). */
export const Anchor: React.FC<{ x: number; y: number; children: React.ReactNode; style?: React.CSSProperties }> = ({
  x,
  y,
  children,
  style,
}) => (
  <svg
    width={1}
    height={1}
    style={{ position: "absolute", left: x, top: y, overflow: "visible", ...style }}
  >
    {children}
  </svg>
);

/** Static formula; `reveal` (0..1 per token, optional) fades tokens in. */
export const FormulaG: React.FC<{
  tokens: Token[];
  opts: LayoutOpts;
  reveal?: (i: number) => number;
}> = ({ tokens, opts, reveal }) => {
  const { items } = layout(tokens, opts);
  return (
    <g>
      {items.map((p, i) => {
        const r = reveal ? reveal(i) : 1;
        return <TokenGlyph key={p.tok.key} t={p.tok} x={p.x} y={p.y + (1 - r) * p.size * 0.12} size={p.size} opacity={r} />;
      })}
    </g>
  );
};

/** A display equation aligned on its relation symbol at x = 0 (like &= in align). */
export const AlignedEq: React.FC<{
  left: Token[];
  right: Token[];
  size: number;
  rel?: string;
  reveal?: (part: 0 | 1 | 2) => number;
}> = ({ left, right, size, rel = "=", reveal }) => {
  const g = tex(rel);
  const wr = (g.w / 1000) * size * font.mathScale;
  const sp = 0.28 * size;
  const r = (k: 0 | 1 | 2) => (reveal ? reveal(k) : 1);
  return (
    <g>
      <g transform={`translate(${-wr / 2 - sp} 0)`} opacity={r(0)}>
        <FormulaG tokens={left} opts={{ size, align: "right" }} />
      </g>
      <g opacity={r(1)}>
        <TokenGlyph t={{ key: "rel", tex: rel }} x={-wr / 2} y={0} size={size} />
      </g>
      <g transform={`translate(${wr / 2 + sp} 0)`} opacity={r(2)}>
        <FormulaG tokens={right} opts={{ size, align: "left" }} />
      </g>
    </g>
  );
};

/**
 * Token morph between two layouts.  `start` is the local frame the morph
 * begins; shared keys ride a spring (with a small arc), changed content
 * cross-fades mid-flight, orphans fade out early / newcomers fade in late.
 */
export const FormulaMorph: React.FC<{
  from: Token[];
  to: Token[];
  fromOpts: LayoutOpts;
  toOpts: LayoutOpts;
  toOffset?: [number, number]; // position of the target layout relative to the source
  start: number;
  stagger?: number;
  order?: string[]; // departure order of shared keys (default: left to right in the target)
}> = ({ from, to, fromOpts, toOpts, toOffset = [0, 0], start, stagger = 4, order: explicit }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const A = layout(from, fromOpts).items;
  const B = layout(to, toOpts).items.map((p) => ({ ...p, x: p.x + toOffset[0], y: p.y + toOffset[1] }));
  const bMap = new Map(B.map((p) => [p.tok.key, p]));
  const aMap = new Map(A.map((p) => [p.tok.key, p]));
  const shared = B.filter((p) => aMap.has(p.tok.key)).sort((a, b) => a.x - b.x);
  const order = new Map(
    explicit ? explicit.map((k, i) => [k, i] as const) : shared.map((p, i) => [p.tok.key, i] as const),
  );
  const f = frame - start;
  const out: React.ReactNode[] = [];

  // orphans of A: lift and dissolve before the travellers cross them
  A.filter((p) => !bMap.has(p.tok.key)).forEach((p) => {
    const o = interpolate(f, [0, 11], [1, 0], { ...clamp, easing: ease.out });
    out.push(<TokenGlyph key={`a-${p.tok.key}`} t={p.tok} x={p.x} y={p.y - (1 - o) * p.size * 0.22} size={p.size} opacity={o} />);
  });

  shared.forEach((b) => {
    const a = aMap.get(b.tok.key)!;
    const d = 6 + order.get(b.tok.key)! * stagger;
    const t = spring({ frame: f - d, fps, config: springs.token });
    const lin = interpolate(f - d, [0, 22], [0, 1], clamp);
    // two lanes, so travellers never pass through each other: leftward glyphs are
    // lifted over, rightward glyphs dip under; short trips barely arc at all
    const dx = b.x - a.x;
    const arcAmp = 0.42 * b.size * Math.min(1, Math.abs(dx) / (3 * b.size));
    const arc = Math.sin(Math.PI * lin) * arcAmp * (dx < 0 ? -1 : 1);
    const size = a.size + (b.size - a.size) * t;
    const same = a.tok.tex === b.tok.tex && a.tok.text === b.tok.text;
    if (same) {
      out.push(
        <TokenGlyph
          key={`s-${b.tok.key}`}
          t={b.tok}
          x={a.x + (b.x - a.x) * t}
          y={a.y + (b.y - a.y) * t + arc}
          size={size}
        />,
      );
    } else {
      // centres glide; the old words dissolve early (at their own size), the symbol condenses in
      const cx = a.x + a.w / 2 + (b.x + b.w / 2 - (a.x + a.w / 2)) * t;
      const y = a.y + (b.y - a.y) * t + arc;
      const ka = interpolate(lin, [0, 0.45], [1, 0], clamp);
      const kb = interpolate(lin, [0.3, 0.85], [0, 1], clamp);
      const wb = (b.w * size) / b.size;
      out.push(<TokenGlyph key={`x-${a.tok.key}`} t={a.tok} x={cx - a.w / 2} y={y} size={a.size} opacity={ka} />);
      out.push(<TokenGlyph key={`y-${b.tok.key}`} t={b.tok} x={cx - wb / 2} y={y} size={size} opacity={kb} />);
    }
  });

  // newcomers of B: settle down into place
  const last = 6 + shared.length * stagger;
  B.filter((p) => !aMap.has(p.tok.key)).forEach((p) => {
    const o = interpolate(f, [last, last + 16], [0, 1], clamp);
    out.push(<TokenGlyph key={`b-${p.tok.key}`} t={p.tok} x={p.x} y={p.y + (1 - o) * p.size * 0.2} size={p.size} opacity={o} />);
  });
  return <g>{out}</g>;
};

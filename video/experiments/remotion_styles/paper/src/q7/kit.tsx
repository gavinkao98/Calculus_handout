/**
 * Q7 kit: the sheet (own running head), the math → page map, and the billiard
 * drawing primitives — a table with its pockets, a path with a rolling ball,
 * and the unfolding view (copies of the table turning over their walls like
 * pages). Beat clock, TeX, arrows and the label guard come from the §3.1 kit.
 */
import React, { useContext } from "react";
import { AbsoluteFill } from "remotion";
import { color, features, font, grid, stroke, type } from "../theme";
import { Camera, Page } from "../components/Shell";
import { Vignette } from "../components/Paper";
import { InlineTex, Rule, SmallCaps } from "../components/Type";
import { Cam, HOME, Kicker as BaseKicker, Lbl, Mark, Pt, SceneCtx, Txt as BaseTxt, keepOnPage, tLbl as baseTLbl, useS as baseUseS, wipe } from "../s31/kit";
import { Shot, V, Wall, at, flip, foldedInto, polyAt } from "./geo";
import { CJK_MIN, CJK_STACK } from "./cjk";
import { LangCtx, TABLES } from "./i18n";

export * from "../s31/kit";

// ── Palette roles (validated inks of the paper system) ────────────────────
export const HOMEC = color.cobalt; // copies of the centre: "home"
export const POCKET = color.accent; // corner pockets (odd, odd)
export const EDGE = color.ochre; // edge-midpoint pockets (odd, even) / (even, odd); also the mirror hinge

// ── Language (one animation, two string tables; see i18n/) ────────────────
/** the zh text stack: Garamond for Latin and digits, Noto Serif TC for the rest; never a synthesized italic */
export const ZH_FONT = `${CJK_STACK}, serif`;
/** Chinese is never set below CJK_MIN (effective 29 px after size-adjust) */
const zhSize = (size: number) => Math.max(size, CJK_MIN);

const ROLE: Record<string, string> = { home: HOMEC, pocket: POCKET, edge: EDGE, ochre: color.ochre, ink2: color.ink2, ink3: color.ink3 };
type Tok = { k: "t"; s: string } | { k: "m"; s: string } | { k: "br" } | { k: "r"; italic: boolean; c?: string; kids: Tok[] };
/** en.ts markup → tokens: {role:…} (brace-balanced), $tex$, \n */
const parse = (s: string): Tok[] => {
  const out: Tok[] = [];
  let buf = "";
  const flush = () => {
    if (buf) out.push({ k: "t", s: buf });
    buf = "";
  };
  for (let i = 0; i < s.length; ) {
    const c = s[i];
    if (c === "$") {
      const j = s.indexOf("$", i + 1);
      if (j < 0) throw new Error(`unclosed $ in "${s}"`);
      flush();
      out.push({ k: "m", s: s.slice(i + 1, j) });
      i = j + 1;
      continue;
    }
    const role = c === "{" ? /^\{([a-z][a-z0-9]*(?:\.[a-z0-9]+)*):/.exec(s.slice(i)) : null;
    if (role) {
      let depth = 1;
      let j = i + role[0].length;
      for (; j < s.length && depth > 0; j++) {
        if (s[j] === "$") j = s.indexOf("$", j + 1);
        else if (s[j] === "{") depth++;
        else if (s[j] === "}") depth--;
      }
      if (depth) throw new Error(`unclosed {${role[1]}: in "${s}"`);
      const parts = role[1].split(".");
      const bad = parts.find((x) => x !== "i" && !(x in ROLE));
      if (bad) throw new Error(`unknown role "${bad}" in "${s}"`);
      flush();
      out.push({ k: "r", italic: parts.includes("i"), c: ROLE[parts.find((x) => x !== "i") ?? ""], kids: parse(s.slice(i + role[0].length, j - 1)) });
      i = j;
      continue;
    }
    if (c === "\n") {
      flush();
      out.push({ k: "br" });
      i++;
      continue;
    }
    buf += c;
    i++;
  }
  flush();
  return out;
};
const HAN = /[㐀-鿿豈-﫿]/;
const edgeChar = (t: Tok | undefined, side: "first" | "last"): string => {
  if (!t) return "";
  if (t.k === "t") return side === "first" ? t.s[0] : t.s[t.s.length - 1];
  if (t.k === "r") return edgeChar(t.kids[side === "first" ? 0 : t.kids.length - 1], side);
  return "";
};
/** inline TeX; in Chinese it keeps 0.18 em of air from an adjacent ideograph (none next to punctuation) */
const texNode = (src: string, c: string | undefined, zh: boolean, before: string, after: string, key: number) => {
  const m = <InlineTex key={zh ? undefined : key} src={src} color={c} />;
  if (!zh) return m;
  const gap = (ch: string) => (HAN.test(ch) ? "0.18em" : 0);
  return (
    <span key={key} style={{ marginLeft: gap(before), marginRight: gap(after), whiteSpace: "nowrap" }}>
      {m}
    </span>
  );
};
/**
 * 標點擠壓: a full-width closing mark carries half an em of air, so two in a row
 * (「）。」「。」」) leave a full em of dead space. The bundled Noto subsets do not
 * carry the `halt` feature text-spacing-trim needs, so the first mark of such a
 * pair gives back half an em by hand.
 */
const CLOSE = "）」』】〕》〉，、。：；？！";
const PUNCT = CLOSE + "（「『【〔《〈";
/** a closing mark directly followed by another mark */
const pair = (cs: string[], i: number) => CLOSE.includes(cs[i]) && i + 1 < cs.length && PUNCT.includes(cs[i + 1]);
const squeeze = (s: string, key: number): React.ReactNode => {
  const cs = [...s];
  if (!cs.some((c, i) => pair(cs, i))) return s;
  const out: React.ReactNode[] = [];
  let buf = "";
  cs.forEach((c, i) => {
    if (pair(cs, i)) {
      if (buf) out.push(buf);
      buf = "";
      out.push(
        <span key={i} style={{ marginRight: "-0.5em" }}>
          {c}
        </span>,
      );
    } else buf += c;
  });
  if (buf) out.push(buf);
  return React.createElement(React.Fragment, { key }, ...out);
};
const render = (toks: Tok[], zh: boolean, before = "", after = ""): React.ReactNode[] =>
  toks.map((t, i) => {
    const b = i ? edgeChar(toks[i - 1], "last") : before;
    const a = i < toks.length - 1 ? edgeChar(toks[i + 1], "first") : after;
    if (t.k === "t") return zh ? squeeze(t.s, i) : t.s;
    if (t.k === "br") return <br key={i} />;
    if (t.k === "m") return texNode(t.s, undefined, zh, b, a, i);
    // a coloured formula on its own: colour the TeX itself (no wrapper span)
    if (!t.italic && t.kids.length === 1 && t.kids[0].k === "m") return texNode(t.kids[0].s, t.c, zh, b, a, i);
    const kids = render(t.kids, zh, b, a);
    if (!t.italic) return React.createElement("span", { key: i, style: { color: t.c } }, ...kids);
    // emphasis: italic in English; in Chinese weight 600 (+ colour) — Chinese has no italic
    if (zh) return React.createElement("span", { key: i, style: { fontWeight: 600, color: t.c } }, ...kids);
    return React.createElement("i", { key: i, style: t.c ? { color: t.c } : undefined }, ...kids);
  });
/**
 * a table string with its markup set (see i18n/en.ts). Chinese breaks between
 * any two characters, so in zh the last three characters of a string are kept
 * together: a paragraph never ends on a one-character line (「個。」).
 */
export const rich = (s: string, zh: boolean): React.ReactNode => {
  const toks = parse(s);
  const last = toks[toks.length - 1];
  let tail: React.ReactNode = null;
  let after = "";
  if (zh && last?.k === "t" && [...last.s].length >= 2) {
    const cs = [...last.s];
    const k = Math.min(3, cs.length);
    const head = cs.slice(0, -k).join("");
    if (head) toks[toks.length - 1] = { k: "t", s: head };
    else toks.pop();
    after = cs[cs.length - k]; // what follows the rendered tokens (spacing after a formula)
    tail = (
      <span key="tail" style={{ whiteSpace: "nowrap" }}>
        {squeeze(cs.slice(-k).join(""), 0)}
      </span>
    );
  }
  return React.createElement(React.Fragment, null, ...render(toks, zh, "", after), tail);
};
/** the plain text of a marked-up string (for measuring) */
const plain = (s: string) => s.replace(/\{[a-z][a-z0-9.]*:/g, "").replace(/\}/g, "");

let zctx: CanvasRenderingContext2D | null = null;
const zw = new Map<string, number>();
/** advance width of a string set in the zh stack (fonts loaded: the zh sheets are gated on Noto) */
const measureZh = (s: string, size: number, weight = 400) => {
  const f = `${weight} ${size}px ${ZH_FONT}`;
  const k = `${f}|${s}`;
  const hit = zw.get(k);
  if (hit !== undefined) return hit;
  if (!zctx) zctx = document.createElement("canvas").getContext("2d")!;
  zctx.font = f;
  const w = zctx.measureText(s).width;
  zw.set(k, w);
  return w;
};
type TOpt = { italic?: boolean; align?: "left" | "center" | "right"; lh?: number };
/** `tLbl` for a zh `Txt`: measured in the stack that draws it, at the size it is drawn (never italic) */
const zhTLbl = (s: string, x: number, y: number, size: number, p: number, o = 1, opt: TOpt = {}): Lbl => {
  const sz = zhSize(size);
  const width = measureZh(plain(s), sz);
  const l = opt.align === "center" ? x - width / 2 : opt.align === "right" ? x - width : x;
  const em = y + (((opt.lh ?? 1.3) - 1) * sz) / 2;
  // Noto's ideographs (size-adjusted) fill more of the em than Garamond's glyphs: a slightly taller box
  return { name: s, box: { l, t: em + sz * 0.06, r: l + width, b: em + sz * 1.02 }, on: p >= 1 && o > 0.05 };
};

/** the strings of the current language, plus the lang-bound helpers */
export const useT = () => {
  const lang = useContext(LangCtx);
  const zh = lang === "zh";
  return {
    lang,
    zh,
    t: TABLES[lang],
    /** render a marked-up table string */
    r: (s: string) => rich(s, zh),
    /** the style of an italic aside: italic in English, upright in Chinese */
    it: (zh ? {} : { fontStyle: "italic" }) as React.CSSProperties,
    /** label-guard entry for a one-line `Txt` (same props as the Txt) */
    tLbl: (s: string, x: number, y: number, size: number, p: number, o = 1, opt: TOpt = {}): Lbl =>
      zh ? zhTLbl(s, x, y, size, p, o, opt) : baseTLbl(plain(s), x, y, size, p, o, opt),
  };
};

/** the §3.1 beat clock plus `has(id)`: whether this scene's storyboard has that beat (never throws) */
export const useS = () => {
  const s = baseUseS();
  const { beats } = useContext(SceneCtx);
  return { ...s, has: (id: string) => beats.some((b) => b.id === id) };
};

/**
 * `Txt` in the current language. zh: the zh stack, never italic, never below
 * CJK_MIN, strict line breaking, and lining figures (Garamond's old-style
 * figures sink below the ideographs' body: 「寬 2 個單位」).
 */
export const Txt: React.FC<React.ComponentProps<typeof BaseTxt>> = (props) => {
  const { zh } = useT();
  if (!zh) return <BaseTxt {...props} />;
  return (
    <BaseTxt
      {...props}
      // a plain string gets the same zh treatment as a marked-up one (orphan guard, punctuation squeeze)
      children={typeof props.children === "string" ? rich(props.children, true) : props.children}
      size={zhSize(props.size ?? type.body)}
      italic={false}
      style={{ fontFamily: ZH_FONT, fontSynthesis: "none", lineBreak: "strict", fontFeatureSettings: "'kern' 1, 'liga' 1, 'lnum' 1", ...props.style }}
    />
  );
};

/** small caps in English; in Chinese (no caps) a tracked 34 px label in weight 500 */
export const Caps: React.FC<{ children: React.ReactNode; size?: number; color?: string; style?: React.CSSProperties }> = ({ children, size, color: c, style }) => {
  const { zh } = useT();
  if (!zh) return <SmallCaps size={size} color={c} style={style}>{children}</SmallCaps>;
  return (
    <span
      style={{
        fontFamily: ZH_FONT,
        fontSize: zhSize(size ?? type.smallCaps),
        fontWeight: 500,
        letterSpacing: "0.24em",
        fontFeatureSettings: features.smallCaps,
        color: c ?? color.ink2,
        whiteSpace: "nowrap",
        ...style,
      }}
    >
      {typeof children === "string" ? untrackLatin(children) : children}
    </span>
  );
};
/** tracking is for the ideographs: Latin runs in a zh label ("(a)", "7") keep their own fit — 「(a)」 not 「( a )」 */
const untrackLatin = (s: string): React.ReactNode =>
  s.split(/([!-~]+)/).map((part, i) =>
    i % 2 ? (
      <span key={i} style={{ letterSpacing: "0.02em" }}>
        {part}
      </span>
    ) : (
      part
    ),
  );

export const Kicker: React.FC<React.ComponentProps<typeof BaseKicker>> = (props) => {
  const { zh } = useT();
  if (!zh) return <BaseKicker {...props} />;
  const { x, y, p = 1, c = color.accent, children, rule = true } = props;
  return (
    <div style={{ position: "absolute", left: x, top: y - 4, ...wipe(p, 0) }}>
      {rule && <div style={{ width: 56, height: 2.5, background: color.accent, marginBottom: 14 }} />}
      <Caps color={c}>{children}</Caps>
    </div>
  );
};

// ── The sheet ─────────────────────────────────────────────────────────────
/** the running head of a zh sheet (Page's own head is small caps + italic: neither exists in Chinese) */
const ZhHead: React.FC<{ w: number; left: string; right: string; folio: string }> = ({ w, left, right, folio }) => {
  const mx = grid.marginX;
  return (
    <>
      <div style={{ position: "absolute", left: mx, top: grid.headY - 33 }}>
        {/* a long line: tracked less than a kicker */}
        <Caps size={CJK_MIN} style={{ letterSpacing: "0.12em" }}>
          {left}
        </Caps>
      </div>
      <div
        style={{
          position: "absolute",
          right: mx,
          top: grid.headY - 36,
          fontFamily: ZH_FONT,
          fontSize: type.caption,
          color: color.ink2,
          fontFeatureSettings: features.text,
          display: "flex",
          gap: 28,
          alignItems: "baseline",
          whiteSpace: "nowrap",
        }}
      >
        <span>{right}</span>
        <span style={{ fontFamily: font.serif, color: color.ink, fontFeatureSettings: "'onum' 1" }}>{folio}</span>
      </div>
      <Rule x={mx} y={grid.headRuleY} w={w - 2 * mx} len={24} color={color.rule} />
    </>
  );
};
export const Sheet: React.FC<{
  folio: number;
  title: string;
  cam?: Cam;
  w?: number;
  h?: number;
  head?: boolean;
  device?: boolean;
  children: React.ReactNode;
}> = ({ folio, title, cam = HOME, w = 1920, h = 1080, head = true, device = true, children }) => {
  const { zh, t } = useT();
  return (
    <AbsoluteFill style={{ backgroundColor: "#2F2A24" }}>
      <Camera {...keepOnPage(cam, w, h)}>
        <Page w={w} h={h} head={head && !zh ? { left: t.head, right: title, folio: String(folio) } : null} device={device}>
          {head && zh && <ZhHead w={w} left={t.head} right={title} folio={String(folio)} />}
          {children}
        </Page>
      </Camera>
      <Vignette />
    </AbsoluteFill>
  );
};

// ── Math → page ───────────────────────────────────────────────────────────
export type World = { ox: number; oy: number; u: number };
export const px = (W: World, [x, y]: V): Pt => [W.ox + x * W.u, W.oy - y * W.u];
export const dOf = (W: World, pts: V[]) => pts.map((p, i) => `${i ? "L" : "M"}${px(W, p)[0].toFixed(1)} ${px(W, p)[1].toFixed(1)}`).join("");
export const pxs = (W: World, pts: V[]): Pt[] => pts.map((p) => px(W, p));

export const R_POCKET = 12;
export const W_POCKET = 3.4;
export const R_BALL = 11;

/** a pocket: a hollow ring (squashed to an ellipse while its table is turning over) */
export const Pocket: React.FC<{ W: World; p: V; c?: string; o?: number; sx?: number; sy?: number; r?: number; fill?: string }> = ({
  W,
  p,
  c = POCKET,
  o = 1,
  sx = 1,
  sy = 1,
  r = R_POCKET,
  fill = color.paper,
}) => {
  const [x, y] = px(W, p);
  return <ellipse cx={x} cy={y} rx={Math.max(0.5, r * sx)} ry={Math.max(0.5, r * sy)} fill={fill} stroke={c} strokeWidth={W_POCKET} opacity={o} />;
};
export const HomeDot: React.FC<{ W: World; p: V; o?: number; r?: number; sx?: number; sy?: number }> = ({ W, p, o = 1, r = 8, sx = 1, sy = 1 }) => {
  const [x, y] = px(W, p);
  return <ellipse cx={x} cy={y} rx={Math.max(0.5, r * sx)} ry={Math.max(0.5, r * sy)} fill={HOMEC} opacity={o} />;
};
export const Ball: React.FC<{ W: World; p: V; o?: number; r?: number }> = ({ W, p, o = 1, r = R_BALL }) => {
  const [x, y] = px(W, p);
  return <circle cx={x} cy={y} r={r} fill={color.ink} stroke={color.paper} strokeWidth={stroke.ring + 0.5} opacity={o} />;
};

export type PocketSet = "corners" | "all" | "none";
const CORNERS: V[] = [
  [1, 1],
  [-1, 1],
  [-1, -1],
  [1, -1],
];
const MIDS: V[] = [
  [1, 0],
  [0, 1],
  [-1, 0],
  [0, -1],
];

/**
 * One copy of the table with centre c (math units). `map` bends every point
 * (used for the page-turn); `sx`/`sy` squash round things the same way.
 */
export const Table: React.FC<{
  W: World;
  c?: V;
  pockets?: PocketSet;
  real?: boolean;
  o?: number;
  draw?: number; // 0→1 the outline inks on
  home?: boolean; // show the centre mark
  fill?: string;
  fillO?: number;
  map?: (p: V) => V;
  sx?: number;
  sy?: number;
  lineW?: number;
  lineC?: string;
  pocketO?: number;
}> = ({ W, c = [0, 0], pockets = "corners", real, o = 1, draw = 1, home = true, fill, fillO = 1, map = (p) => p, sx = 1, sy = 1, lineW, lineC, pocketO = 1 }) => {
  if (o <= 0) return null;
  const q = (p: V): V => map([c[0] + p[0], c[1] + p[1]]);
  const outline = [q([-1, -1]), q([1, -1]), q([1, 1]), q([-1, 1]), q([-1, -1])];
  const per = 4 * 2 * W.u;
  const lw = lineW ?? (real ? 4.2 : 2.2);
  return (
    <g opacity={o}>
      {fill && <path d={dOf(W, outline) + "Z"} fill={fill} opacity={fillO} />}
      <path
        d={dOf(W, outline)}
        fill="none"
        stroke={lineC ?? (real ? color.ink : color.ink2)}
        strokeWidth={lw}
        strokeLinejoin="miter"
        strokeDasharray={draw < 1 ? `${per * draw} ${per}` : undefined}
      />
      {home && draw >= 1 && <HomeDot W={W} p={q([0, 0])} sx={sx} sy={sy} r={real ? 8 : 7} />}
      {pockets !== "none" && draw >= 1 && CORNERS.map((p, i) => <Pocket key={`c${i}`} W={W} p={q(p)} sx={sx} sy={sy} o={pocketO} />)}
      {pockets === "all" && draw >= 1 && MIDS.map((p, i) => <Pocket key={`m${i}`} W={W} p={q(p)} c={EDGE} sx={sx} sy={sy} o={pocketO} />)}
    </g>
  );
};

/** guard marks for a table drawn by `Table` (outline + pockets + centre) */
export const tableMarks = (W: World, name: string, c: V = [0, 0], pockets: PocketSet = "corners", real = true, on = true): Mark[] => {
  const q = (p: V): V => [c[0] + p[0], c[1] + p[1]];
  const ms: Mark[] = [
    { name: `${name} outline`, pts: pxs(W, [q([-1, -1]), q([1, -1]), q([1, 1]), q([-1, 1]), q([-1, -1])]), w: real ? 4.2 : 2.2, on },
    { name: `${name} centre`, pts: [px(W, q([0, 0]))], w: 16, on },
  ];
  if (pockets !== "none") CORNERS.forEach((p) => ms.push({ name: `${name} pocket`, pts: [px(W, q(p))], w: 2 * R_POCKET + W_POCKET, on }));
  if (pockets === "all") MIDS.forEach((p) => ms.push({ name: `${name} edge pocket`, pts: [px(W, q(p))], w: 2 * R_POCKET + W_POCKET, on }));
  return ms;
};

/** a path (math polyline) inked up to `frac` of its length, with the ball at its head */
export const Rolling: React.FC<{
  W: World;
  pts: V[];
  frac: number;
  ball?: boolean;
  c?: string;
  w?: number;
  o?: number;
  ballO?: number;
  dash?: string;
}> = ({ W, pts, frac, ball = true, c = color.ink, w = 3.6, o = 1, ballO = 1, dash }) => {
  if (frac <= 0 || o <= 0) return null;
  const { p, upto } = polyAt(pts, frac);
  return (
    <g opacity={o}>
      <path d={dOf(W, upto)} fill="none" stroke={c} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={dash} />
      {ball && <Ball W={W} p={p} o={ballO} />}
    </g>
  );
};

/** an expanding ring (arrival flash) */
export const Flash: React.FC<{ W: World; p: V; t: number; c: string; r0?: number; r1?: number }> = ({ W, p, t, c, r0 = 12, r1 = 46 }) => {
  if (t <= 0 || t >= 1) return null;
  const [x, y] = px(W, p);
  return <circle cx={x} cy={y} r={r0 + (r1 - r0) * t} fill="none" stroke={c} strokeWidth={4 * (1 - t) + 0.5} opacity={1 - t} />;
};

// ── The unfolding view ────────────────────────────────────────────────────
/**
 * `stage` ∈ [0, n]: k = ⌊stage⌋ reflections done, and the (k+1)-th copy is
 * turning over its wall with progress stage − k. At stage k the line is
 * straight through copies 0..k and its remainder is folded back into copy k;
 * stage 0 is the real bouncing path, stage n the straight line.
 */
export const Unfold: React.FC<{
  W: World;
  s: Shot;
  stage: number;
  pockets?: PocketSet;
  lineFrac?: number; // how much of the path is inked (0→1 of the full length)
  pathC?: string;
  hinge?: boolean;
  ball?: V | null;
  copiesO?: number;
}> = ({ W, s, stage, pockets = "corners", lineFrac = 1, pathC = color.ink, hinge = true, ball = null, copiesO = 1 }) => {
  const n = s.cross.length;
  const st = Math.max(0, Math.min(n, stage));
  const k = Math.min(n, Math.floor(st + 1e-9));
  const u = st - k;
  const sigma = Math.cos(Math.PI * u);
  const tK1 = k < n ? s.cross[k] : s.T; // end of the straight part
  const straight: V[] = [
    [0, 0],
    at(s, tK1),
  ];
  const wall: Wall | null = k < n ? s.walls[k][0] : null;
  const turning = u > 1e-4 && wall && k + 1 <= n;
  // remainder after the straight part
  let rest: V[] = [];
  if (k < n) {
    if (turning) rest = foldedInto(s, tK1, s.tiles[k + 1]).map((p) => flip(p, wall!, sigma));
    else rest = foldedInto(s, tK1, s.tiles[k]);
  }
  const full = [...straight, ...rest.slice(1)];
  const shown = lineFrac >= 1 ? full : polyAt(full, lineFrac).upto;
  const squash = Math.abs(sigma);
  const sx = turning && wall!.axis === "x" ? squash : 1;
  const sy = turning && wall!.axis === "y" ? squash : 1;
  // hinge: the wall being turned over, along the side of copy k
  const hingeSeg: V[] | null = wall
    ? wall.axis === "x"
      ? [
          [wall.at, 2 * s.tiles[k][1] - 1],
          [wall.at, 2 * s.tiles[k][1] + 1],
        ]
      : [
          [2 * s.tiles[k][0] - 1, wall.at],
          [2 * s.tiles[k][0] + 1, wall.at],
        ]
    : null;
  const hingeO = turning ? Math.sin(Math.PI * u) : 0;
  return (
    <g>
      {s.tiles.slice(0, k + 1).map((c, i) => (
        <Table key={i} W={W} c={[2 * c[0], 2 * c[1]]} real={i === 0} pockets={pockets} o={i === 0 ? 1 : copiesO} />
      ))}
      {turning && (
        <Table
          W={W}
          c={[2 * s.tiles[k + 1][0], 2 * s.tiles[k + 1][1]]}
          map={(p) => flip(p, wall!, sigma)}
          sx={sx}
          sy={sy}
          pockets={pockets}
          fill={color.paperShade}
          fillO={0.35 + 0.5 * (1 - squash)}
          o={copiesO}
        />
      )}
      {hinge && hingeSeg && hingeO > 0 && (
        <path d={dOf(W, hingeSeg)} stroke={EDGE} strokeWidth={7} strokeLinecap="round" opacity={0.85 * hingeO} />
      )}
      <path d={dOf(W, shown)} fill="none" stroke={pathC} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round" />
      {ball && <Ball W={W} p={ball} />}
    </g>
  );
};

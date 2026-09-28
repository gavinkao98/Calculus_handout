/**
 * Beat clock + rostrum camera for narrated scenes.  Scenes never write
 * seconds: every cue is `at("<reveal id>")` (+ a fraction of that beat, or a
 * few frames of choreography offset), so the MiMo manifest re-times them.
 */
import React, { createContext, useContext } from "react";
import { Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { ease, springs } from "../theme";
import { findWord } from "../lib/words";
import type { ActTiming, SceneTiming } from "./timing";

const Ctx = createContext<SceneTiming | null>(null);

/** The whole act's timing (a scene may need a neighbour's, e.g. to freeze it). */
export const ActCtx = createContext<ActTiming | null>(null);
export const useAct = () => {
  const a = useContext(ActCtx);
  if (!a) throw new Error("no act timing");
  return a;
};
export const sceneTiming = (act: ActTiming, id: string) => {
  const s = act.scenes.find((x) => x.id === id);
  if (!s) throw new Error(`no scene ${id}`);
  return s;
};

export const SceneClock: React.FC<{ timing: SceneTiming; children: React.ReactNode }> = ({ timing, children }) => (
  <Ctx.Provider value={timing}>{children}</Ctx.Provider>
);

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export const useTiming = (): SceneTiming => {
  const t = useContext(Ctx);
  if (!t) throw new Error("scene rendered outside <SceneClock>");
  return t;
};

export const useBeats = () => {
  const t = useTiming();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const beat = (id: string) => {
    const b = t.beats[id];
    if (!b) throw new Error(`scene ${t.id}: no beat "${id}" in the manifest (act3.yml {show ${id}}?)`);
    return b;
  };
  /** Frame at which beat `id` starts, or a fraction `k` (0..1) into it. */
  const at = (id: string, k = 0) => {
    const b = beat(id);
    return Math.round(b.start + k * (b.end - b.start));
  };
  const end = (id: string) => beat(id).end;
  /** 0→1 over [from, from+len] with an easing (default: pen on paper). */
  const p = (from: number, len: number, easing: (x: number) => number = ease.ink) =>
    interpolate(frame, [from, from + len], [0, 1], { ...clamp, easing });
  /** A spring that starts at `from`. */
  const sp = (from: number, config: Parameters<typeof spring>[0]["config"] = springs.pop) =>
    spring({ frame: frame - from, fps, config });
  /**
   * Frame at which `phrase` is spoken in this scene's narration (the Nth
   * occurrence, default first), or `undefined` if the scene has no
   * word-level alignment (mock manifest) — callers must then fall back to
   * `at(...)`. `afterFrame` (e.g. a beat's `at(id)`) disambiguates a phrase
   * that recurs earlier in the scene.
   */
  const atWord = (phrase: string, opts: { occurrence?: number; afterFrame?: number } = {}): number | undefined => {
    const afterSeconds = opts.afterFrame === undefined ? undefined : (opts.afterFrame - t.lead) / fps;
    const seconds = findWord(t.words, phrase, { occurrence: opts.occurrence, afterSeconds });
    return seconds === undefined ? undefined : t.lead + Math.round(seconds * fps);
  };
  return { frame, fps, dur: t.dur, lead: t.lead, at, end, p, sp, has: (id: string) => id in t.beats, atWord };
};

// ── Camera ───────────────────────────────────────────────────────────────
export type Cam = { cx: number; cy: number; s: number };

export const mixCam = (a: Cam, b: Cam, t: number): Cam => ({
  cx: a.cx + (b.cx - a.cx) * t,
  cy: a.cy + (b.cy - a.cy) * t,
  s: a.s * Math.pow(b.s / a.s, t), // log-space zoom reads as constant speed
});

/** A camera move that starts at frame `f` and lands `len` frames later. */
export type CamMove = { f: number; to: Cam; len?: number };

/**
 * Evaluate a camera path: `start`, then each move in order (heavy symmetric
 * ease).  `drift` adds a slow push (fraction of scale per scene) so that no
 * long hold is ever perfectly frozen.
 */
export const camPath = (frame: number, start: Cam, bounds: Bounds, moves: CamMove[], drift = 0, dur = 1): Cam => {
  let c = start;
  for (const m of moves) {
    const t = interpolate(frame, [m.f, m.f + (m.len ?? 40)], [0, 1], { ...clamp, easing: ease.camera });
    if (t <= 0) break;
    c = mixCam(c, m.to, t);
  }
  if (drift) c = { ...c, s: c.s * (1 + drift * interpolate(frame, [0, dur], [0, 1], clamp)) };
  return keepOnPage(c, bounds);
};

export type Bounds = { w: number; h: number };
export const PAGE: Bounds = { w: 1920, h: 1080 };

/**
 * Keep the lens over paper: in each axis where the frame is smaller than the
 * page, clamp the centre so no desk shows.  (A deliberate pull-back past the
 * page edge -- the open-book shot -- is larger than the page and passes through.)
 */
export const keepOnPage = (c: Cam, b: Bounds): Cam => {
  const hw = 960 / c.s;
  const hh = 540 / c.s;
  const cx = 2 * hw <= b.w ? Math.min(b.w - hw, Math.max(hw, c.cx)) : c.cx;
  const cy = 2 * hh <= b.h ? Math.min(b.h - hh, Math.max(hh, c.cy)) : c.cy;
  return { ...c, cx, cy };
};

export const linear = Easing.linear;

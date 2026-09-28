/**
 * Manifest → frame timeline.  The ONLY place narration timing enters the act.
 *
 * Input is the manifest.json that video/pipeline/tts.py writes (mock or MiMo):
 *   scenes[] { scene_id, kind, audio_file?, audio_seconds?, duration?, beats[] }
 *   beats[]  { reveal: string|null, start_seconds, end_seconds, ... }
 * Swapping the mock manifest for the real one re-times every scene without a
 * code change: scene length = lead + audio + tail, every cue is a beat start.
 */
import { staticFile } from "remotion";
import { AlignedWord, loadSceneWords } from "../lib/words";

export const FPS = 30;
export const LEAD = 30; // frames of picture before the first word
export const TAIL = 30; // frames after the last word
export const TURN = 28; // page-turn overlap between two scenes

/** How each scene hands over to the next one. */
export type Handover = "turn" | "cut";

/** Act order + boundaries (the storyboard's scene order; ids must match act3.yml). */
export const ORDER: { id: string; out: Handover; lead?: number }[] = [
  { id: "intro", out: "turn", lead: 12 },
  { id: "derivative_of_sine", out: "cut" }, // → facing page: the camera slides, no cut visible
  { id: "derivative_of_cosine", out: "turn" },
  { id: "slope_equals_height", out: "turn" },
  { id: "derivative_cycle", out: "turn" },
  { id: "outro", out: "cut" },
];

type ManifestBeat = { reveal: string | null; start_seconds: number; end_seconds: number; text?: string };
type ManifestScene = {
  scene_id: string;
  kind: string;
  audio_file?: string;
  audio_seconds?: number;
  duration?: number;
  beats?: ManifestBeat[];
  alignment?: { words_file?: string };
};
export type Manifest = { backend?: string; scenes: ManifestScene[] };

export type BeatSpan = { start: number; end: number; text: string };
export type SceneTiming = {
  id: string;
  from: number; // first frame in the act
  dur: number; // frames
  lead: number;
  audio: string | null; // staticFile() src
  beats: Record<string, BeatSpan>; // key: reveal id ("_" = the words before the first {show})
  words?: AlignedWord[]; // forced-alignment word list, scene-relative seconds; absent for mock manifests
  out: Handover;
};
export type ActTiming = { scenes: SceneTiming[]; total: number; backend: string };

/** tts.py stores absolute paths; the act serves them from public/. */
const publicSrc = (abs: string): string => {
  const p = abs.replace(/\\/g, "/");
  const i = p.lastIndexOf("/public/");
  if (i < 0) throw new Error(`audio file is not under public/: ${abs}`);
  return staticFile(p.slice(i + "/public/".length));
};

const f = (s: number) => Math.round(s * FPS);

export const buildAct = (m: Manifest, wordsByScene: Map<string, AlignedWord[]> = new Map()): ActTiming => {
  const byId = new Map(m.scenes.map((s) => [s.scene_id, s]));
  let t = 0;
  const scenes: SceneTiming[] = ORDER.map((o, i) => {
    const s = byId.get(o.id);
    if (!s) throw new Error(`manifest has no scene "${o.id}" — re-run tts.py on act3.yml`);
    const lead = o.lead ?? LEAD;
    const beats: Record<string, BeatSpan> = {};
    let dur: number;
    if (s.kind === "content") {
      for (const b of s.beats ?? []) {
        beats[b.reveal ?? "_"] = { start: lead + f(b.start_seconds), end: lead + f(b.end_seconds), text: b.text ?? "" };
      }
      dur = lead + f(s.audio_seconds ?? 0) + TAIL;
    } else {
      dur = f(s.duration ?? 6);
    }
    const prevTurn = i > 0 && ORDER[i - 1].out === "turn";
    const from = t - (prevTurn ? TURN : 0);
    t = from + dur;
    return {
      id: o.id,
      from,
      dur,
      lead,
      audio: s.kind === "content" && s.audio_file ? publicSrc(s.audio_file) : null,
      beats,
      words: wordsByScene.get(o.id),
      out: o.out,
    };
  });
  return { scenes, total: t, backend: m.backend ?? "?" };
};

export const DEFAULT_MANIFEST = "audio/act3_mock/manifest.json";

export const loadAct = async (path: string): Promise<ActTiming> => {
  const res = await fetch(staticFile(path));
  if (!res.ok) throw new Error(`cannot load ${path} (${res.status}) — run tts.py --backend mock first (see act3/SCRIPT.md)`);
  const manifest = (await res.json()) as Manifest;
  const wordsByScene = await loadSceneWords(manifest.scenes);
  return buildAct(manifest, wordsByScene);
};

/**
 * §3.1 (unguided) timing — everything comes from tts.py's manifest.json.
 *   scene length = LEAD + narration seconds + TAIL   (silent scenes: manifest `duration`)
 *   beat start   = LEAD + beat.start_seconds          (looked up by its {show <id>})
 * Scenes overlap by OVER frames: the next sheet is laid over the last one.
 * Swap the manifest prop (mock → MiMo) and the whole film re-times itself.
 */
import { staticFile } from "remotion";
import { AlignedWord, loadSceneWords } from "../lib/words";

export const FPS = 30;
export const LEAD = 15; // frames of silence before a scene's narration
export const TAIL = 27; // frames after it (the next sheet slides in during the last OVER)
export const OVER = 22; // sheet-over-sheet transition overlap
export const DEFAULT_MANIFEST = "audio/s31_mock/manifest.json";

export type BeatT = { id: string; start: number; end: number }; // frames, scene-local
export type SceneT = {
  id: string;
  kind: string;
  from: number;
  dur: number;
  audio: string | null;
  beats: BeatT[];
  words?: AlignedWord[]; // forced-alignment word list, scene-relative seconds; absent for mock manifests
};
export type Show = { scenes: SceneT[]; total: number };

type MBeat = { reveal: string | null; start_seconds: number; end_seconds: number };
type MScene = {
  scene_id: string;
  kind: string;
  duration?: number;
  audio_file?: string;
  audio_seconds?: number;
  beats?: MBeat[];
  alignment?: { words_file?: string };
};

/** manifest paths are absolute on the machine that ran tts.py: keep the part under the manifest's folder */
const relAudio = (manifest: string, abs: string) => {
  const dir = manifest.slice(0, manifest.lastIndexOf("/"));
  const parts = abs.replace(/\\/g, "/").split("/");
  return `${dir}/${parts.slice(-2).join("/")}`; // scenes/NN_id.wav
};

export const buildShow = (manifest: string, data: { scenes: MScene[] }, wordsByScene: Map<string, AlignedWord[]> = new Map()): Show => {
  let t = 0;
  const scenes: SceneT[] = data.scenes.map((s, i) => {
    const narrated = s.kind === "content" && s.audio_seconds !== undefined;
    const dur = narrated
      ? LEAD + Math.ceil((s.audio_seconds ?? 0) * FPS) + TAIL
      : Math.round((s.duration ?? 4) * FPS);
    const beats: BeatT[] = (s.beats ?? []).map((b) => ({
      id: b.reveal ?? "start",
      start: LEAD + Math.round(b.start_seconds * FPS),
      end: LEAD + Math.round(b.end_seconds * FPS),
    }));
    const from = i === 0 ? 0 : t - OVER;
    t = from + dur;
    return {
      id: s.scene_id,
      kind: s.kind,
      from,
      dur,
      audio: narrated && s.audio_file ? relAudio(manifest, s.audio_file) : null,
      beats,
      words: wordsByScene.get(s.scene_id),
    };
  });
  return { scenes, total: t };
};

export const loadShow = async (manifest: string): Promise<Show> => {
  const res = await fetch(staticFile(manifest));
  if (!res.ok) throw new Error(`cannot load ${manifest} (run the tts.py mock command in s31/SCRIPT.md)`);
  const data = (await res.json()) as { scenes: MScene[] };
  const wordsByScene = await loadSceneWords(data.scenes);
  return buildShow(manifest, data, wordsByScene);
};

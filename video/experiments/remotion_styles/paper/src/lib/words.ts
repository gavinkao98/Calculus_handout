/**
 * Word-level narration timing (forced alignment), generic across acts/scenes.
 *
 * tts.py's scene-aligned backend writes one `*.words.json` per scene next to
 * the manifest: `{ summary, words: [{ word, start, end, probability }],
 * segments }`, times in seconds relative to that scene's audio file — the
 * same origin as a manifest beat's `start_seconds`. A manifest scene points
 * at its words file via `alignment.words_file` (an absolute path, same
 * convention as `audio_file`); mock manifests have no `alignment` at all.
 */
import { staticFile } from "remotion";

export type AlignedWord = { word: string; start: number; end: number; probability: number };
type WordsFileJson = { words: AlignedWord[] };
type ManifestSceneRef = { scene_id: string; alignment?: { words_file?: string } };

/** tts.py stores absolute paths; resolve the same way timing.ts resolves audio_file. */
const publicPath = (abs: string): string => {
  const p = abs.replace(/\\/g, "/");
  const i = p.lastIndexOf("/public/");
  if (i < 0) throw new Error(`words file is not under public/: ${abs}`);
  return p.slice(i + "/public/".length);
};

/**
 * Load every scene's word list, keyed by `scene_id`. A scene with no
 * `alignment.words_file` (a mock manifest, or a silent/outro scene) is
 * simply absent from the map — callers must treat that as "no alignment"
 * and fall back to beat-fraction timing, not as an error.
 */
export const loadSceneWords = async (scenes: ManifestSceneRef[]): Promise<Map<string, AlignedWord[]>> => {
  const out = new Map<string, AlignedWord[]>();
  await Promise.all(
    scenes.map(async (s) => {
      const file = s.alignment?.words_file;
      if (!file) return;
      const res = await fetch(staticFile(publicPath(file)));
      if (!res.ok) throw new Error(`cannot load words file for scene "${s.scene_id}" (${res.status}): ${file}`);
      const json = (await res.json()) as WordsFileJson;
      out.set(s.scene_id, json.words);
    }),
  );
  return out;
};

const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, "");

/**
 * Time (seconds, scene-relative) of the Nth (1-based, default 1) occurrence
 * of `phrase` — one or more words, space-separated — in a scene's word list.
 * Matching is case/punctuation-insensitive. `afterSeconds` restricts the
 * search to words starting at/after that time (e.g. a beat's start, to
 * disambiguate a word that recurs earlier in the scene).
 *
 * `words` is `undefined` for a scene with no alignment (mock manifest): that
 * is the one silent, non-throwing case, and it returns `undefined` so the
 * caller keeps its existing beat-fraction timing. Once a word list exists,
 * a phrase that isn't found throws — never a silent fallback.
 */
export const findWord = (
  words: AlignedWord[] | undefined,
  phrase: string,
  opts: { occurrence?: number; afterSeconds?: number } = {},
): number | undefined => {
  if (!words) return undefined;
  const { occurrence = 1, afterSeconds = -Infinity } = opts;
  const target = phrase.trim().split(/\s+/).map(norm);
  if (target.length === 0 || target.some((t) => !t)) throw new Error(`findWord: empty phrase "${phrase}"`);
  let hits = 0;
  for (let i = 0; i + target.length <= words.length; i++) {
    if (words[i].start < afterSeconds) continue;
    let ok = true;
    for (let j = 0; j < target.length; j++) {
      if (norm(words[i + j].word) !== target[j]) {
        ok = false;
        break;
      }
    }
    if (ok) {
      hits += 1;
      if (hits === occurrence) return words[i].start;
    }
  }
  throw new Error(
    `findWord: "${phrase}" (occurrence ${occurrence}) not found${afterSeconds > -Infinity ? ` after ${afterSeconds}s` : ""} among ${words.length} words`,
  );
};

/** Same as `findWord`, but in frames at `fps` (still `undefined` when unaligned). */
export const findWordFrame = (
  words: AlignedWord[] | undefined,
  fps: number,
  phrase: string,
  opts?: { occurrence?: number; afterSeconds?: number },
): number | undefined => {
  const t = findWord(words, phrase, opts);
  return t === undefined ? undefined : Math.round(t * fps);
};

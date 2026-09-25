/**
 * Q7 timing — the §3.1 manifest reader (scene length = LEAD + narration + TAIL,
 * beat start = LEAD + start_seconds, sheets overlap by OVER), plus a per-scene
 * HOLD: extra frames after the narration where the picture needs time to play
 * (the epilogue's long run). Swap the manifest prop (mock → MiMo) to re-time.
 */
import { staticFile } from "remotion";
import { loadSceneWords } from "../lib/words";
import { Show, buildShow } from "../s31/timing";
import type { Lang } from "./i18n";

export { FPS, LEAD, OVER, TAIL } from "../s31/timing";
export type { SceneT, Show } from "../s31/timing";
export const DEFAULT_MANIFEST = "audio/q7_mock/manifest.json";

/** extra frames at the end of a scene (after its narration), per language (each has its own scene list) */
export const HOLD: Record<Lang, Record<string, number>> = {
  en: { epilogue: 120, recap: 20, writeup: 45 },
  // ext_dense: the √2 run (Epilogue, shortened) ends ~3 s before the sheet leaves
  zh: { recap: 20, ext_design: 20, ext_room: 30, ext_family: 20, ext_dense: 90 },
};

const withHolds = (show: Show, hold: Record<string, number>): Show => {
  let shift = 0;
  const scenes = show.scenes.map((s) => {
    const out = { ...s, from: s.from + shift, dur: s.dur + (hold[s.id] ?? 0) };
    shift += hold[s.id] ?? 0;
    return out;
  });
  return { scenes, total: show.total + shift };
};

export const loadShow = async (manifest: string, lang: Lang = "en"): Promise<Show> => {
  const res = await fetch(staticFile(manifest));
  if (!res.ok) throw new Error(`cannot load ${manifest} (run the tts.py mock command in q7/SCRIPT.md)`);
  const data = await res.json();
  const words = await loadSceneWords(data.scenes);
  return withHolds(buildShow(manifest, data, words), HOLD[lang]);
};

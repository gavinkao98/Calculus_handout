/**
 * Bundled, open-licensed fonts (EB Garamond, SIL OFL via @fontsource).
 * No network at render time: the woff2 files are imported as bundle assets.
 */
import { loadFont } from "@remotion/fonts";
import { useEffect, useState } from "react";
import { continueRender, delayRender } from "remotion";
import r400 from "@fontsource/eb-garamond/files/eb-garamond-latin-400-normal.woff2";
import i400 from "@fontsource/eb-garamond/files/eb-garamond-latin-400-italic.woff2";
import r500 from "@fontsource/eb-garamond/files/eb-garamond-latin-500-normal.woff2";
import i500 from "@fontsource/eb-garamond/files/eb-garamond-latin-500-italic.woff2";
import r600 from "@fontsource/eb-garamond/files/eb-garamond-latin-600-normal.woff2";
import i600 from "@fontsource/eb-garamond/files/eb-garamond-latin-600-italic.woff2";

const faces: Array<[string, string, "normal" | "italic"]> = [
  [r400, "400", "normal"],
  [i400, "400", "italic"],
  [r500, "500", "normal"],
  [i500, "500", "italic"],
  [r600, "600", "normal"],
  [i600, "600", "italic"],
];

export const fontsReady: Promise<void> = Promise.all(
  faces.map(([url, weight, style]) =>
    loadFont({ family: "EB Garamond", url, weight, style }),
  ),
).then(() => undefined);

/** True once every face is loaded; holds the render until then. */
export const useFontsReady = (): boolean => {
  const [ready, setReady] = useState(false);
  const [handle] = useState(() => delayRender("EB Garamond"));
  useEffect(() => {
    fontsReady.then(() => {
      setReady(true);
      continueRender(handle);
    });
  }, [handle]);
  return ready;
};

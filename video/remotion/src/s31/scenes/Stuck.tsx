/** C1 — the recipe works for x² (the h cancels), jams for sine; everything funnels into sinθ/θ. */
import React from "react";
import { interpolate } from "remotion";
import { color, stroke, type } from "../../theme";
import { clamp } from "../../components/Type";
import { Arrow, HOME, Kicker, Layer, Ln, M, Sheet, Txt, camPath, texW, useS } from "../kit";

const A = color.accent;
const H = 1560;
const RECIPE_LHS = `{\\color{${A}}f'(x)}=\\lim_{h\\to0}`;
const RECIPE = `${RECIPE_LHS}\\frac{f(x+h)-f(x)}{h}`;

export const Stuck: React.FC = () => {
  const { f, at, p, pf, atWord } = useS();
  // emphasis lands as the narration names it (underline / caption ink), not with the camera
  const startAt = atWord("difference quotient", { afterFrame: at("start") }) ?? at("start", 0.55);
  const plugAt = atWord("pull out", { afterFrame: at("plug") }) ?? at("plug", 0.7);
  const funnelZeroAt = atWord("zero over zero", { afterFrame: at("funnel") }) ?? at("funnel", 0.55);
  // two regions on a tall sheet: the worked pair (top), then the funnel (bottom). One move, in the
  // gap after the (b) caption has inked and before the funnel starts drawing.
  const cam = camPath(f, HOME, [[at("funnel") - 48, { cx: 960, cy: 990, s: 1 }, 52]]);
  const rW = texW(RECIPE, 78);
  const qL = 960 - rW / 2 + texW(RECIPE_LHS, 78);
  const dimTop = 1 - 0.55 * p("funnel", 40);
  // the (a)/(b) captions sit on the lower frame's top edge: fade them rather than clip them
  const away = interpolate(cam.cy, [540, 760], [1, 0], clamp);
  const cancel = p("cancel", 26);
  return (
    <Sheet folio={113} title="Why sine resists algebra" cam={cam} h={H}>
      <div style={{ opacity: dimTop }}>
        <Kicker x={460} y={132} p={pf(10, 24)}>
          The recipe
        </Kicker>
        <M
          x={960}
          y={292}
          align="center"
          size={78}
          p={pf(20, 34)}
          t={RECIPE}
        />
        <Layer h={H}>
          {/* "the difference quotient": underline the quotient as it is named */}
          <Ln x1={qL} y1={376} x2={960 + rW / 2} y2={376} p={pf(startAt, 22)} c={A} w={3} o={1 - p("square", 30)} />
          <Ln x1={960} y1={400} x2={960} y2={860} p={p("square", 30)} c={color.rule} />
        </Layer>

        {/* (a) x squared */}
        <Txt x={160} y={410} size={type.label + 2} italic c={color.ink2} p={p("square", 20)} o={away} w={60}>
          (a)
        </Txt>
        <M x={212} y={440} size={44} c={color.ink2} p={p("square", 20)} o={away} t="f(x)=x^2" />
        <M x={160} y={560} size={62} p={p("square", 30, 8)} t="\frac{(x+h)^2-x^2}{h}=\frac{2xh+h^2}{h}" />
        <M
          x={160}
          y={700}
          size={62}
          p={cancel}
          t={`=\\frac{{\\color{${A}}\\cancel{\\color{${color.ink}}h}}\\,(2x+h)}{{\\color{${A}}\\cancel{\\color{${color.ink}}h}}}=2x+h`}
        />
        <M x={160} y={820} size={62} p={p("cancel", 26, 40)} t={`\\xrightarrow{\\;h\\to0\\;}\\ {\\color{${A}}2x}`} />
        <Txt x={500} y={790} w={420} size={type.caption} italic c={color.ink2} p={p("cancel", 26, 60)}>
          algebra removed the h
        </Txt>

        {/* (b) sine */}
        <Txt x={1020} y={410} size={type.label + 2} italic c={color.ink2} p={p("sine", 16)} o={away} w={60}>
          (b)
        </Txt>
        <M x={1072} y={440} size={44} c={color.ink2} p={p("sine", 16)} o={away} t="f(x)=\sin x" />
        <M x={1020} y={560} size={62} p={p("sine", 26, 4)} t="\frac{\sin(x+h)-\sin x}{h}" />
        <M x={1020} y={700} size={62} p={p("plug", 30)} t={`\\xrightarrow{\\;h=0\\;}\\ \\frac{\\sin x-\\sin x}{0}={\\color{${A}}\\frac{0}{0}}`} />
        <Txt x={1020} y={782} w={780} size={type.caption} italic c={A} p={pf(plugAt - 6, 26)}>
          and there is no factor of h to pull out of sin(x + h)
        </Txt>
      </div>

      {/* the funnel */}
      <Layer h={H}>
        <Arrow x1={1330} y1={850} x2={1236} y2={1190} p={p("funnel", 36, 10)} c={color.accent} w={2.6} bend={-50} />
        {/* double-ruled box around the key limit */}
        <rect x={700} y={1130} width={520} height={250} fill="none" stroke={color.ink} strokeWidth={2.4} opacity={p("funnel", 20, 30)} />
        <rect x={712} y={1142} width={496} height={226} fill="none" stroke={color.ink} strokeWidth={1} opacity={p("funnel", 20, 36)} />
      </Layer>
      <M x={960} y={1290} align="center" size={100} p={p("funnel", 30, 30)} t="\lim_{\theta\to0}\frac{\sin\theta}{\theta}" />
      <Kicker x={700} y={1082} p={p("funnel", 24, 30)} rule={false}>
        Everything comes down to
      </Kicker>
      <Txt x={1270} y={1140} w={560} size={type.body - 2} italic c={color.ink2} p={pf(funnelZeroAt - 4, 28)}>
        Also <span style={{ color: A, fontStyle: "normal" }}>0/0</span> — algebra can’t crack it.
      </Txt>
      <Txt x={1270} y={1250} w={330} size={type.body - 2} italic c={color.ink} p={p("funnel", 28, Math.round((at("radians") - at("funnel")) * 0.62))}>
        The new tool: <span style={{ fontStyle: "normal" }}>geometry on the unit circle.</span>
      </Txt>
      <Layer h={H}>
        {(() => {
          const q = p("funnel", 40, Math.round((at("radians") - at("funnel")) * 0.62) + 10);
          const O = { x: 1650, y: 1420 };
          const R = 105;
          const th = 0.75;
          return (
            <g opacity={q}>
              <line x1={O.x - 20} y1={O.y} x2={O.x + R + 30} y2={O.y} stroke={color.ink3} strokeWidth={stroke.axis} />
              <path d={`M${O.x} ${O.y} L${O.x + R} ${O.y} A${R} ${R} 0 0 0 ${O.x + R * Math.cos(th)} ${O.y - R * Math.sin(th)} Z`} fill="url(#h45)" stroke="none" />
              <path d={`M${O.x + R} ${O.y} A${R} ${R} 0 0 0 ${O.x} ${O.y - R}`} fill="none" stroke={color.ink} strokeWidth={2.6} strokeDasharray={`${R * 1.6 * q} 999`} />
              <line x1={O.x} y1={O.y} x2={O.x + R * Math.cos(th)} y2={O.y - R * Math.sin(th)} stroke={color.ink} strokeWidth={1.8} />
            </g>
          );
        })()}
        <defs>
          <pattern id="h45" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <line x1="0" y1="0" x2="0" y2="12" stroke={color.ink} strokeWidth="2" opacity="0.5" />
          </pattern>
        </defs>
      </Layer>

      {/* the convention */}
      <Kicker x={160} y={1140} p={p("radians", 24)}>
        Convention
      </Kicker>
      <Txt x={160} y={1196} w={460} size={type.body + 4} p={p("radians", 28, 8)}>
        Every angle in this section is measured in <i style={{ color: A }}>radians</i>.
      </Txt>
    </Sheet>
  );
};

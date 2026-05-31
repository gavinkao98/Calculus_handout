// =====================================================================
// graph.jsx — restyleable function-plot blueprint for graph_focus.
// The CURVE itself is drawn by Manim in production; this fixes the
// VISUAL STYLE: axis weight/color, gridlines, curve color, point fill
// (solid vs hollow = different mathematical meaning), dashed guides,
// and annotation placement.
//   ParabolaPlot({ axis, curve, guide, point, grid, w, h })
// =====================================================================
function ParabolaPlot({
  w=820, h=620,
  axis='var(--muted)', curve='var(--secondary)',
  guide='var(--warning)', point='var(--accent)',
  grid=false, gridColor='rgba(255,255,255,0.05)',
}){
  // data domain
  const xMin=-1.45, xMax=1.45, yMin=-0.28, yMax=1.55;
  const pad = { l:60, r:60, t:40, b:60 };
  const PX = x => pad.l + (x - xMin)/(xMax - xMin) * (w - pad.l - pad.r);
  const PY = y => (h - pad.b) - (y - yMin)/(yMax - yMin) * (h - pad.t - pad.b);

  // parabola path g(x)=x^2
  let d=''; for(let i=0;i<=120;i++){ const x=xMin+(xMax-xMin)*i/120; const y=x*x;
    d += (i?' L':'M')+PX(x).toFixed(1)+' '+PY(y).toFixed(1); }

  const x0=PX(0), y0=PY(0);
  const yLevel=PY(0.25);
  const ptL=[PX(-0.5),PY(0.25)], ptR=[PX(0.5),PY(0.25)];

  const ticks = grid ? [-1,-0.5,0.5,1] : [];

  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} style={{ overflow:'visible' }}>
      {/* optional faint gridlines */}
      {grid && ticks.map((t,i)=>(
        <g key={i}>
          <line x1={PX(t)} y1={pad.t} x2={PX(t)} y2={h-pad.b} stroke={gridColor} strokeWidth="1"/>
        </g>
      ))}
      {grid && [0.25,0.5,1,1.25].map((t,i)=>(
        <line key={'h'+i} x1={pad.l} y1={PY(t)} x2={w-pad.r} y2={PY(t)} stroke={gridColor} strokeWidth="1"/>
      ))}

      {/* axes */}
      <line x1={pad.l-10} y1={y0} x2={w-pad.r+10} y2={y0} stroke={axis} strokeWidth="2"/>
      <line x1={x0} y1={h-pad.b+10} x2={x0} y2={pad.t-10} stroke={axis} strokeWidth="2"/>
      {/* arrow heads */}
      <path d={`M${w-pad.r+10} ${y0} l-12 -6 l0 12 z`} fill={axis}/>
      <path d={`M${x0} ${pad.t-10} l-6 12 l12 0 z`} fill={axis}/>

      {/* dashed guide y = 1/4 */}
      <line x1={pad.l} y1={yLevel} x2={w-pad.r} y2={yLevel}
        stroke={guide} strokeWidth="2.5" strokeDasharray="3 9" strokeLinecap="round" opacity="0.9"/>

      {/* the curve */}
      <path d={d} fill="none" stroke={curve} strokeWidth="3.5" strokeLinejoin="round"
        style={{ filter:`drop-shadow(0 0 10px ${curve.includes('var')?'rgba(76,201,240,.35)':'rgba(76,201,240,.35)'})` }}/>

      {/* intersection points — HOLLOW = "shares same output, not unique" */}
      {[ptL,ptR].map((p,i)=>(
        <circle key={i} cx={p[0]} cy={p[1]} r="9" fill="var(--bg)" stroke={point} strokeWidth="3.5"/>
      ))}

      {/* labels (mono, like axis annotations) */}
      <text x={x0+16} y={pad.t+6} fill="var(--text)" fontFamily="var(--font-mono)" fontSize="22">g(x) = x²</text>
      <text x={w-pad.r+18} y={yLevel+7} fill={guide} fontFamily="var(--font-mono)" fontSize="20">y = 1/4</text>
    </svg>
  );
}
Object.assign(window, { ParabolaPlot });

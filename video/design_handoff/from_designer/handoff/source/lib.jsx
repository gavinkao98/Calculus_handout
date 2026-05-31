// =====================================================================
// lib.jsx — shared mockup primitives (exported to window)
//   • M           : KaTeX render helper (real LaTeX → HTML)
//   • Eyebrow     : mono uppercase tag
//   • HeadingRule : the signature underline + plotted-point node
//   • CornerTicks : registration ticks (graph-plane motif)
//   • PlotDot     : small node bullet
//   • BrandMark   : corner watermark placeholder (swap for user logo)
// =====================================================================

// ---- KaTeX render helper -------------------------------------------------
function tex(str, display){
  try{
    return window.katex.renderToString(str, {
      displayMode: !!display,
      throwOnError: false,
      strict: false,
    });
  }catch(e){ return '<span style="color:#ff6b6b">'+String(str)+'</span>'; }
}
function M({ children, display=false, className='', style }){
  const cls = (display ? 'math-display ' : 'math-sm ') + className;
  return <span className={cls} style={style}
    dangerouslySetInnerHTML={{ __html: tex(children, display) }} />;
}

// ---- eyebrow tag ---------------------------------------------------------
function Eyebrow({ children, color='var(--secondary)', style }){
  return <span className="eyebrow" style={{ color, ...style }}>{children}</span>;
}

// ---- a single plotted-point node (filled or hollow) ----------------------
function PlotDot({ r=7, color='var(--secondary)', hollow=false, style }){
  return (
    <span style={{
      display:'inline-block', width:r*2, height:r*2, borderRadius:'50%',
      background: hollow ? 'transparent' : color,
      border: hollow ? `2.5px solid ${color}` : 'none',
      boxShadow: hollow ? 'none' : `0 0 12px ${color}66`,
      ...style,
    }}/>
  );
}

// ---- heading rule: thin line that ends in a plotted point ----------------
function HeadingRule({ color='var(--secondary)', width='100%', node=true, glow=false }){
  return (
    <div style={{ display:'flex', alignItems:'center', width }}>
      <div style={{
        height:'var(--rule-w)', flex:1,
        background:`linear-gradient(90deg, ${color}, ${color}55)`,
        boxShadow: glow ? `0 0 16px ${color}66` : 'none',
        borderRadius:2,
      }}/>
      {node && <span style={{
        width:14, height:14, borderRadius:'50%', background:color, marginLeft:-2,
        boxShadow:`0 0 14px ${color}aa`, flex:'0 0 auto',
      }}/>}
    </div>
  );
}

// ---- corner registration ticks (graph-plane DNA) ------------------------
function CornerTicks({ color='var(--hairline)', inset='var(--safe)', size=26, weight=2 }){
  const arm = (pos)=>({ position:'absolute', ...pos });
  const h = { width:size, height:weight, background:color };
  const v = { width:weight, height:size, background:color };
  return (
    <div style={{ position:'absolute', inset:0, pointerEvents:'none' }}>
      {[['top','left'],['top','right'],['bottom','left'],['bottom','right']].map(([y,x],i)=>(
        <div key={i} style={arm({ [y]:inset, [x]:inset })}>
          <div style={{ position:'absolute', [y]:0, [x]:0, ...h }}/>
          <div style={{ position:'absolute', [y]:0, [x]:0, ...v }}/>
        </div>
      ))}
    </div>
  );
}

// ---- summit-bars motif (decorative device inspired by the mark) ---------
// Ascending rounded bars — the brand's "summit/peak" DNA, reused as a
// divider / corner device / level indicator. NOT the logo itself.
function SummitBars({ h=64, color='var(--brand-red)', peak='var(--brand-navy)',
                      star=true, starColor='var(--brand-gold)', gap=6, bw=11 }){
  const heights=[0.32,0.56,0.78,1,0.78,0.56,0.32];
  return (
    <div style={{ display:'flex', alignItems:'flex-end', gap, position:'relative' }}>
      {heights.map((f,i)=>(
        <div key={i} style={{ width:bw, height:h*f, borderRadius:bw/2,
          background: i===3 ? peak : color }}/>
      ))}
      {star && <svg width={h*0.34} height={h*0.34} viewBox="0 0 40 40"
        style={{ position:'absolute', left:'50%', top:-h*0.30, transform:'translateX(-50%)' }}>
        <path d="M20,2 L24,15 L37,19 L24,23 L20,36 L16,23 L3,19 L16,15 Z" fill={starColor}/>
      </svg>}
    </div>
  );
}

// ---- official logo (image embed — never recolored/distorted) ------------
// variant: 'lockup-white' | 'lockup-color' | 'icon-white' | 'icon-color' ...
function Logo({ variant='lockup-white', height=64, style }){
  const isIcon = variant.startsWith('icon');
  const ratio = isIcon ? 1 : (1040/300);
  return <img src={`assets/brand/${variant}.svg`} alt="NTU 數學組"
    style={{ height, width: height*ratio, ...style }}/>;
}

// ---- logo on a light plaque (for color variants on dark canvas) ---------
// The official color marks use navy/gray ink meant for light grounds, so on
// the dark canvas they need a light backing to read correctly.
function LogoPlaque({ variant='lockup-color', height=64, pad=22, radius=14, style }){
  return (
    <div style={{ display:'inline-flex', background:'#f4f5f7', borderRadius:radius,
      padding:`${pad}px ${pad*1.3}px`, boxShadow:'0 6px 22px rgba(0,0,0,0.22)', ...style }}>
      <Logo variant={variant} height={height}/>
    </div>
  );
}

// ---- brand watermark (corner) -------------------------------------------
function BrandMark({ corner='bottom-right', variant='icon-white', height=42, opacity=0.55, plaque=false }){
  const pos = {
    'bottom-right': { bottom:'var(--safe)', right:'var(--safe)' },
    'bottom-left':  { bottom:'var(--safe)', left:'var(--safe)' },
    'top-right':    { top:'var(--safe)', right:'var(--safe)' },
    'top-left':     { top:'var(--safe)', left:'var(--safe)' },
  }[corner];
  return (
    <div style={{ position:'absolute', ...pos, opacity, display:'flex', alignItems:'center', gap:14 }}>
      {plaque
        ? <LogoPlaque variant={variant} height={height} pad={height*0.34} radius={12}/>
        : <Logo variant={variant} height={height}/>}
    </div>
  );
}

Object.assign(window, { tex, M, Eyebrow, PlotDot, HeadingRule, CornerTicks, SummitBars, Logo, LogoPlaque, BrandMark });

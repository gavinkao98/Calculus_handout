// =====================================================================
// overview.jsx — GLOBAL VISUAL SYSTEM spec board (shared by all directions)
// Palette · Type scale · Layout grid · Emphasis states · Motif
// =====================================================================

function Sw({ name, hex, role, text='#0a0e1a' }){
  return (
    <div style={{ display:'flex', flexDirection:'column', gap:8 }}>
      <div style={{ height:84, background:hex, borderRadius:6, border:'1px solid rgba(255,255,255,0.08)',
        display:'flex', alignItems:'flex-end', padding:10 }}>
        <span style={{ fontFamily:'var(--font-mono)', fontSize:15, color:text, opacity:0.85 }}>{hex}</span>
      </div>
      <div style={{ fontFamily:'var(--font-display)', fontWeight:600, fontSize:18, color:'var(--primary)' }}>{name}</div>
      <div style={{ fontFamily:'var(--font-body)', fontSize:14, color:'var(--muted)', lineHeight:1.3 }}>{role}</div>
    </div>
  );
}
function SecLabel({ children }){
  return <div style={{ display:'flex', alignItems:'center', gap:14, marginBottom:26 }}>
    <span className="eyebrow" style={{ color:'var(--secondary)', fontSize:18 }}>{children}</span>
    <div style={{ flex:1, height:1, background:'var(--hairline)' }}/>
  </div>;
}

function Overview(){
  const pad=80;
  return (
    <div className="frame" style={{ height:1820, padding:pad, boxSizing:'border-box', overflow:'hidden' }}>
      {/* header */}
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start', marginBottom:50 }}>
        <div>
          <Eyebrow color="var(--secondary)">Global Visual System</Eyebrow>
          <h1 className="display" style={{ fontSize:64, marginTop:16 }}>Midnight Canvas <span style={{color:'var(--brand-red-bright)'}}>· NTU</span></h1>
          <p className="body" style={{ color:'var(--muted)', marginTop:14, fontSize:26, maxWidth:1100 }}>
            Dark navy canvas · luminous mathematics · zero chrome. Sans-serif UI type paired with LaTeX (serif) math.
          </p>
        </div>
        <Logo variant="icon-color" height={92}/>
      </div>

      {/* palette */}
      <SecLabel>Palette · 9 semantic roles</SecLabel>
      <div style={{ display:'grid', gridTemplateColumns:'repeat(9,1fr)', gap:18 }}>
        <Sw name="background" hex="#0a0e1a" role="navy-black canvas" text="#eef0f7"/>
        <Sw name="primary" hex="#eef0f7" role="headings, display"/>
        <Sw name="secondary" hex="#4cc9f0" role="definitions"/>
        <Sw name="accent" hex="#f4b13a" role="theorems, key"/>
        <Sw name="math" hex="#7df9ff" role="expressions"/>
        <Sw name="warning" hex="#ff6b6b" role="counter-examples"/>
        <Sw name="success" hex="#06d6a0" role="verify / QED"/>
        <Sw name="text" hex="#c8ccdb" role="narration"/>
        <Sw name="muted" hex="#7e8497" role="retired content" text="#eef0f7"/>
      </div>
      <div style={{ marginTop:26, marginBottom:50 }}>
        <div style={{ fontFamily:'var(--font-mono)', fontSize:15, color:'var(--muted)', marginBottom:14, letterSpacing:'0.1em' }}>NTU BRAND LAYER — logo, intro / outro, section markers</div>
        <div style={{ display:'grid', gridTemplateColumns:'repeat(9,1fr)', gap:18 }}>
          <Sw name="brand red 校門紅" hex="#BA0C2F" role="brand emphasis" text="#fff"/>
          <Sw name="brand navy 藏青" hex="#16294E" role="brand fields" text="#fff"/>
          <Sw name="brand gold 點綴金" hex="#B6892B" role="summit star" text="#fff"/>
        </div>
      </div>

      {/* type + grid two columns */}
      <div style={{ display:'grid', gridTemplateColumns:'1.3fr 1fr', gap:64 }}>
        <div>
          <SecLabel>Type scale</SecLabel>
          <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
            {[
              ['Display','Space Grotesk · 600','display',52,'Inverse Functions'],
              ['Heading','Space Grotesk · 600','h1',40,'One-to-One Functions'],
              ['Body','Hanken Grotesk · 400','body',32,'A function is one-to-one if…'],
              ['Eyebrow / tag','JetBrains Mono · 500','eyebrow',22,'SECTION 1.1'],
            ].map(([lab,fam,cls,sz,txt],i)=>(
              <div key={i} style={{ display:'flex', alignItems:'baseline', gap:24 }}>
                <div style={{ width:160, flex:'0 0 160px' }}>
                  <div style={{ fontFamily:'var(--font-display)', fontSize:17, color:'var(--primary)' }}>{lab}</div>
                  <div style={{ fontFamily:'var(--font-mono)', fontSize:12, color:'var(--muted)' }}>{fam}</div>
                </div>
                <div className={cls} style={{ fontSize:sz, color: cls==='eyebrow'?'var(--secondary)':undefined }}>{txt}</div>
              </div>
            ))}
            <div style={{ display:'flex', alignItems:'baseline', gap:24 }}>
              <div style={{ width:160, flex:'0 0 160px' }}>
                <div style={{ fontFamily:'var(--font-display)', fontSize:17, color:'var(--primary)' }}>Math</div>
                <div style={{ fontFamily:'var(--font-mono)', fontSize:12, color:'var(--muted)' }}>KaTeX · Computer Modern</div>
              </div>
              <M display>{String.raw`f(x_1)=f(x_2)\Rightarrow x_1=x_2`}</M>
            </div>
          </div>
        </div>
        <div>
          <SecLabel>Layout grid · 1920×1080</SecLabel>
          <div style={{ position:'relative', width:'100%', aspectRatio:'16/9',
            border:'1px solid var(--hairline)', background:'rgba(255,255,255,0.015)' }}>
            <div style={{ position:'absolute', left:'11.5%', right:'11.5%', top:0, bottom:0,
              borderLeft:'1px dashed var(--hairline)', borderRight:'1px dashed var(--hairline)' }}/>
            <div style={{ position:'absolute', left:'11.5%', right:'11.5%', top:'9%', height:0,
              borderTop:'2px solid var(--secondary)' }}/>
            <div style={{ position:'absolute', left:'11.5%', top:'4%', fontFamily:'var(--font-mono)', fontSize:12, color:'var(--secondary)' }}>heading zone</div>
            <div style={{ position:'absolute', left:'11.5%', top:'46%', fontFamily:'var(--font-mono)', fontSize:12, color:'var(--muted)' }}>content · 77% width</div>
            <div style={{ position:'absolute', left:'11.5%', bottom:'5%', fontFamily:'var(--font-mono)', fontSize:11, color:'var(--muted)' }}>footer / watermark</div>
          </div>
          <p className="step" style={{ color:'var(--muted)', fontSize:18, marginTop:16, lineHeight:1.4 }}>
            Safe margin 96px · side gutter 220px · content column ≈ 77% · single focus per moment.
          </p>
        </div>
      </div>

      {/* emphasis + motif */}
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:64, marginTop:50 }}>
        <div>
          <SecLabel>Emphasis & state</SecLabel>
          <div style={{ display:'flex', flexDirection:'column', gap:22 }}>
            <div style={{ display:'flex', alignItems:'center', gap:20 }}>
              <span className="glow-accent"><M display style={{color:'var(--accent)'}}>{String.raw`x_1=x_2`}</M></span>
              <span className="step" style={{ color:'var(--muted)', fontSize:18 }}>key line — gold glow (Manim flash)</span>
            </div>
            <div style={{ display:'flex', alignItems:'center', gap:20 }}>
              <span className="retired"><M display>{String.raw`x_1=x_2`}</M></span>
              <span className="step" style={{ color:'var(--muted)', fontSize:18 }}>prior step — faded to muted, not deleted</span>
            </div>
          </div>
        </div>
        <div>
          <SecLabel>Motif · the summit</SecLabel>
          <div style={{ display:'flex', alignItems:'center', gap:50, height:120 }}>
            <SummitBars h={88} color="var(--brand-red)" peak="var(--brand-navy)" starColor="var(--brand-gold)"/>
            <SummitBars h={88} color="var(--brand-red-bright)" peak="var(--secondary)" starColor="var(--brand-gold)"/>
            <span className="step" style={{ color:'var(--muted)', fontSize:18, maxWidth:240 }}>
              ascending bars + corner brackets echo the coordinate plane.
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
Object.assign(window, { Overview });

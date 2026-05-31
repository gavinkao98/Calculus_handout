// =====================================================================
// dir-b.jsx — DIRECTION B · "Blueprint Grid"
// Leans into the coordinate-plane / summit DNA. Faint full-frame grid,
// L-corner brackets (registration marks), axis-tick heading rules,
// bracketed mono tags, plotted-point bullets. Brand red marks the brand
// layer (origin node, transition); cyan/gold stay pedagogical.
// Exports: B_Intro, B_Definition, B_Outro, B_Graph
// =====================================================================

function B_Brackets(){
  // Corner registration brackets removed per request.
  return null;
}

function B_SceneHead({ title, tag }){
  return (
    <div style={{ position:'absolute', top:'var(--safe)', left:'var(--safe)', right:'var(--safe)' }}>
      {tag && <div style={{ marginBottom:14 }}>
        <span className="eyebrow" style={{ color:'var(--secondary)' }}>[&nbsp;{tag}&nbsp;]</span>
      </div>}
      <h1 className="h1" dangerouslySetInnerHTML={{__html:title}}/>
    </div>
  );
}

function B_Intro(){
  return (
    <div className="frame frame--grid frame--vignette">
      <B_Brackets color="var(--hairline)"/>
      <div style={{ position:'absolute', inset:0, display:'flex', flexDirection:'column',
        alignItems:'center', justifyContent:'center', gap:34 }}>
        {/* brand hero — full lockup, large enough to read the Chinese name */}
        <Logo variant="lockup-white" height={188}/>
        <div style={{ display:'flex', flexDirection:'column', alignItems:'center', gap:14, marginTop:28 }}>
          <Eyebrow color="var(--secondary)">// &nbsp;Section 1.1</Eyebrow>
          <h1 className="display" style={{ fontSize:88 }}>Inverse Functions</h1>
        </div>
        <p className="body" style={{ color:'var(--muted)', fontSize:34 }}>When can a function be run backwards?</p>
      </div>
    </div>
  );
}

// Light-ground opener — paper canvas so the official COLOR lockup sits
// naturally (navy ink, red bars, gold star) with no plaque / white box.
function B_IntroLight(){
  return (
    <div className="frame" style={{ background:'#eef1f6', color:'var(--brand-navy)' }}>
      {/* faint navy coordinate grid, echoing the dark frames' motif */}
      <div style={{ position:'absolute', inset:0, backgroundImage:
        'linear-gradient(rgba(22,41,78,0.045) 1px, transparent 1px),'+
        'linear-gradient(90deg, rgba(22,41,78,0.045) 1px, transparent 1px)',
        backgroundSize:'80px 80px' }}/>
      <div style={{ position:'absolute', inset:0, display:'flex', flexDirection:'column',
        alignItems:'center', justifyContent:'center', gap:36 }}>
        <Logo variant="lockup-color" height={188}/>
        <div style={{ display:'flex', flexDirection:'column', alignItems:'center', gap:16, marginTop:30 }}>
          <span className="eyebrow" style={{ color:'var(--brand-red)' }}>//&nbsp;&nbsp;Section 1.1</span>
          <h1 className="display" style={{ fontSize:88, color:'var(--brand-navy)' }}>Inverse Functions</h1>
        </div>
        <p className="body" style={{ color:'#5a6478', fontSize:34 }}>When can a function be run backwards?</p>
      </div>
    </div>
  );
}

function B_Definition(){
  return (
    <div className="frame frame--grid">
      <B_Brackets color="var(--hairline)"/>
      <B_SceneHead title="One-to-One Functions" tag="Definition"/>
      <div style={{ position:'absolute', inset:0, display:'flex', flexDirection:'column',
        alignItems:'center', justifyContent:'center', gap:50 }}>
        <p className="body" style={{ maxWidth:1180, textAlign:'center' }}>
          A function is <span className="c-secondary">one-to-one</span> if different inputs always produce different outputs.
        </p>
        {/* boxed math card on the grid */}
        <div style={{ display:'flex', flexDirection:'column', gap:30, alignItems:'center',
          padding:'46px 70px', border:'1.5px solid var(--hairline)', borderRadius:4,
          background:'rgba(10,14,26,0.6)', backdropFilter:'blur(2px)' }}>
          <M display>{String.raw`f(x_1) \neq f(x_2)\quad\text{whenever}\quad x_1 \neq x_2`}</M>
          <div style={{ width:'70%', height:1, background:'var(--hairline)' }}/>
          <span className="glow-accent"><M display style={{ color:'var(--accent)' }}>
            {String.raw`f(x_1) = f(x_2)\ \Longrightarrow\ x_1 = x_2`}</M></span>
        </div>
      </div>
      <BrandMark corner="bottom-right" variant="icon-white" height={58} opacity={0.55}/>
    </div>
  );
}

function B_Outro(){
  const items=[
    'A function can be reversed exactly when it is one-to-one.',
    'The reverse rule swaps the roles of input and output.',
  ];
  return (
    <div className="frame frame--grid frame--vignette">
      <B_Brackets color="var(--hairline)"/>
      <div style={{ position:'absolute', top:'var(--safe)', left:'var(--safe)' }}>
        <span className="eyebrow" style={{ color:'var(--accent)' }}>[&nbsp;Recap&nbsp;]</span>
      </div>
      <div style={{ position:'absolute', inset:0, display:'flex', flexDirection:'column',
        justifyContent:'center', paddingLeft:'var(--gutter)', paddingRight:'var(--gutter)', gap:40 }}>
        <div style={{ display:'flex', alignItems:'center', gap:26 }}>
          <h1 className="display" style={{ fontSize:78 }}>Key Takeaways</h1>
          <SummitBars h={48} color="var(--accent)" peak="var(--accent)" star={false} bw={8} gap={5}/>
        </div>
        <div style={{ display:'flex', flexDirection:'column', gap:24 }}>
          {items.map((t,i)=>(
            <div key={i} style={{ display:'flex', alignItems:'center', gap:22 }}>
              <span className="eyebrow" style={{ color:'var(--accent)', fontSize:22 }}>0{i+1}</span>
              <PlotDot r={6} color="var(--accent)"/>
              <span className="body">{t}</span>
            </div>
          ))}
        </div>
        <div style={{ display:'flex', alignItems:'center', gap:16, marginTop:6 }}>
          <span style={{ width:40,height:2,background:'var(--secondary)' }}/>
          <p className="body" style={{ color:'var(--secondary)', fontSize:34 }}>Up next — how to actually find an inverse.</p>
        </div>
      </div>
      <BrandMark corner="bottom-right" variant="icon-white" height={58} opacity={0.55}/>
    </div>
  );
}

// Light-ground outro — brand-moment bookend matching the light intro.
function B_OutroLight(){
  const items=[
    'A function can be reversed exactly when it is one-to-one.',
    'The reverse rule swaps the roles of input and output.',
  ];
  return (
    <div className="frame" style={{ background:'#eef1f6', color:'var(--brand-navy)' }}>
      <div style={{ position:'absolute', inset:0, backgroundImage:
        'linear-gradient(rgba(22,41,78,0.045) 1px, transparent 1px),'+
        'linear-gradient(90deg, rgba(22,41,78,0.045) 1px, transparent 1px)',
        backgroundSize:'80px 80px' }}/>
      <div style={{ position:'absolute', top:'var(--safe)', left:'var(--safe)' }}>
        <span className="eyebrow" style={{ color:'var(--brand-red)' }}>[&nbsp;Recap&nbsp;]</span>
      </div>
      <div style={{ position:'absolute', inset:0, display:'flex', flexDirection:'column',
        justifyContent:'center', paddingLeft:'var(--gutter)', paddingRight:'var(--gutter)', gap:40 }}>
        <div style={{ display:'flex', alignItems:'center', gap:26 }}>
          <h1 className="display" style={{ fontSize:78, color:'var(--brand-navy)' }}>Key Takeaways</h1>
          <SummitBars h={48} color="var(--brand-red)" peak="var(--brand-navy)" star={false} bw={8} gap={5}/>
        </div>
        <div style={{ display:'flex', flexDirection:'column', gap:24 }}>
          {items.map((t,i)=>(
            <div key={i} style={{ display:'flex', alignItems:'center', gap:22 }}>
              <span className="eyebrow" style={{ color:'var(--brand-red)', fontSize:22 }}>0{i+1}</span>
              <PlotDot r={6} color="var(--brand-red)"/>
              <span className="body" style={{ color:'#2b3242' }}>{t}</span>
            </div>
          ))}
        </div>
        <div style={{ display:'flex', alignItems:'center', gap:16, marginTop:6 }}>
          <span style={{ width:40,height:2,background:'var(--brand-red)' }}/>
          <p className="body" style={{ color:'var(--brand-red)', fontSize:34 }}>Up next — how to actually find an inverse.</p>
        </div>
      </div>
      <BrandMark corner="bottom-right" variant="icon-color" height={48} opacity={0.85}/>
    </div>
  );
}

function B_Graph(){
  return (
    <div className="frame frame--grid">
      <B_Brackets color="var(--hairline)"/>
      <B_SceneHead title={'Why '+tex('g(x)=x^2')+' cannot be inverted on '+tex('[-1,1]')}/>
      <div style={{ position:'absolute', top:230, left:0, right:0, bottom:120,
        display:'flex', alignItems:'center', justifyContent:'center' }}>
        <ParabolaPlot axis="var(--text)" curve="var(--secondary)" guide="var(--warning)"
          point="var(--accent)" grid w={860} h={600}/>
      </div>
      <div style={{ position:'absolute', bottom:78, left:0, right:0, textAlign:'center' }}>
        <span className="step" style={{ color:'var(--muted)' }}
          dangerouslySetInnerHTML={{__html:'Two inputs share the same output &mdash; &nbsp;'+tex('g^{-1}(\\{\\tfrac14\\})')+' is not well-defined.'}}/>
      </div>
      <BrandMark corner="bottom-right" variant="icon-white" height={58} opacity={0.55}/>
    </div>
  );
}

Object.assign(window, { B_Intro, B_IntroLight, B_Definition, B_Outro, B_OutroLight, B_Graph,
  B_Brackets, B_SceneHead });

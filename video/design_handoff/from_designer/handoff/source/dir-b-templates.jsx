// =====================================================================
// dir-b-templates.jsx — DIRECTION B · remaining scene templates
//   B_Example     · example_walkthrough  (steps + worked algebra)
//   B_Procedure   · procedure_steps       (big numerals + formula strip)
//   B_Theorem     · theorem_proof         (statement + proof + QED)
//   B_Transition  · section_transition    (mid-roll card + teaser)
//   B_Recap       · recap_cards           (points + formula-to-remember)
// Reuses B_Brackets / B_SceneHead from dir-b.jsx.
// =====================================================================

// ---------------------------------------------------------------------
// example_walkthrough — "Testing with Algebra"
// Left numbered reasoning · right worked LaTeX · bottom conclusion
// ---------------------------------------------------------------------
function B_Example(){
  const steps=[
    { t:<span><M>{String.raw`f(x)=x`}</M> on <M>{String.raw`[0,1]`}</M> gives distinct outputs.</span>,
      m:String.raw`f(x)=x,\quad 0\le x\le 1`, ok:true },
    { t:<span>Test <M>{String.raw`g(x)=x^2`}</M> at <M>{String.raw`x=\tfrac12`}</M> against <M>{String.raw`x=-\tfrac12`}</M>.</span>,
      m:String.raw`g\!\left(\tfrac12\right)=\tfrac14=g\!\left(-\tfrac12\right)`, hot:true },
    { t:<span>Two inputs collide, so <M>{String.raw`g`}</M> is <span className="c-warning">not</span> one-to-one.</span>,
      m:String.raw`\tfrac12 \neq -\tfrac12`, bad:true },
  ];
  return (
    <div className="frame frame--grid">
      <B_Brackets/>
      <B_SceneHead title="Testing with Algebra" tag="Example"/>
      <div style={{ position:'absolute', top:300, left:'var(--safe)', right:'var(--safe)', bottom:150,
        display:'grid', gridTemplateColumns:'1fr 1px 1fr', gap:64, alignItems:'center' }}>
        {/* left — reasoning */}
        <div style={{ display:'flex', flexDirection:'column', gap:46 }}>
          {steps.map((s,i)=>(
            <div key={i} style={{ display:'flex', gap:24, alignItems:'flex-start' }}>
              <span className="eyebrow" style={{ color:'var(--secondary)', fontSize:26, marginTop:4 }}>0{i+1}</span>
              <span className="step" style={{ fontSize:34 }}>{s.t}</span>
            </div>
          ))}
        </div>
        {/* axis divider */}
        <div style={{ width:1, height:'78%', alignSelf:'center', background:'var(--hairline)' }}/>
        {/* right — worked math, vertically aligned to steps */}
        <div style={{ display:'flex', flexDirection:'column', gap:46, justifyContent:'flex-start' }}>
          {steps.map((s,i)=>(
            <div key={i} style={{ minHeight:60, display:'flex', alignItems:'center', gap:18 }}>
              <span className={s.hot?'glow-accent':undefined}>
                <M display style={{ color: s.hot?'var(--accent)' : s.bad?'var(--warning)':'var(--math)' }}>{s.m}</M>
              </span>
              {s.ok && <span style={{ color:'var(--success)', fontSize:34 }}>✓</span>}
              {s.bad && <span style={{ color:'var(--warning)', fontSize:34 }}>✕</span>}
            </div>
          ))}
        </div>
      </div>
      <div style={{ position:'absolute', bottom:78, left:'var(--safe)', right:'var(--safe)',
        display:'flex', alignItems:'center', gap:16 }}>
        <span style={{ width:40,height:2,background:'var(--warning)' }}/>
        <p className="step" style={{ color:'var(--warning)', fontSize:28 }}>
          To disprove one-to-one, a single colliding pair of inputs is enough.
        </p>
      </div>
      <BrandMark corner="bottom-right" variant="icon-white" height={58} opacity={0.55}/>
    </div>
  );
}

// ---------------------------------------------------------------------
// procedure_steps — "Finding an Inverse"
// big mono numerals · step text · bottom worked-example strip
// ---------------------------------------------------------------------
function B_Procedure(){
  const steps=[
    { n:'1', t:'Write the rule as an equation.', m:String.raw`y = f(x)` },
    { n:'2', t:'Solve for the input in terms of the output.', m:String.raw`x = \dfrac{y-3}{2}` },
    { n:'3', t:'Swap the symbols to name the inverse.', m:String.raw`f^{-1}(x) = \dfrac{x-3}{2}` },
  ];
  return (
    <div className="frame frame--grid">
      <B_Brackets/>
      <B_SceneHead title="Finding an Inverse" tag="Procedure"/>
      <div style={{ position:'absolute', top:300, left:'var(--safe)', right:'var(--safe)', bottom:230,
        display:'flex', flexDirection:'column', justifyContent:'center', gap:34 }}>
        {steps.map((s,i)=>(
          <div key={i} style={{ display:'flex', alignItems:'center', gap:40 }}>
            <span style={{ fontFamily:'var(--font-display)', fontWeight:700, fontSize:72,
              color:'var(--secondary)', lineHeight:1, width:80, textAlign:'center',
              textShadow:'0 0 18px rgba(76,201,240,.3)' }}>{s.n}</span>
            <div style={{ width:2, height:62, background:'var(--hairline)' }}/>
            <span className="step" style={{ fontSize:36, flex:'0 0 640px' }}>{s.t}</span>
            <M display style={{ color:'var(--math)' }}>{s.m}</M>
          </div>
        ))}
      </div>
      {/* worked-example strip */}
      <div style={{ position:'absolute', bottom:96, left:'var(--safe)', right:'var(--safe)',
        border:'1.5px solid var(--hairline)', borderRadius:4, background:'rgba(10,14,26,0.6)',
        padding:'24px 40px', display:'flex', alignItems:'center', gap:30 }}>
        <span className="eyebrow" style={{ color:'var(--accent)', fontSize:20 }}>Worked</span>
        <span className="step" style={{ color:'var(--math)' }}
          dangerouslySetInnerHTML={{__html: tex('f(x)=2x+3') + '<span style="color:var(--muted);margin:0 22px">&rarr;</span>' + tex('y=2x+3') + '<span style="color:var(--muted);margin:0 22px">&rarr;</span>' + tex('f^{-1}(x)=\\tfrac{x-3}{2}') }}/>
      </div>
      <BrandMark corner="bottom-right" variant="icon-white" height={58} opacity={0.55}/>
    </div>
  );
}

// ---------------------------------------------------------------------
// theorem_proof — statement + proof steps + QED
// ---------------------------------------------------------------------
function B_Theorem(){
  const proof=[
    <span>Take any <M>{String.raw`x_1 < x_2`}</M> in the interval <M>{String.raw`I`}</M>.</span>,
    <span>Strictly increasing gives <M>{String.raw`f(x_1) < f(x_2)`}</M>.</span>,
    <span>So the outputs never coincide: <M>{String.raw`f(x_1) \neq f(x_2)`}</M>.</span>,
  ];
  return (
    <div className="frame frame--grid">
      <B_Brackets/>
      <B_SceneHead title="Strictly Increasing ⟹ One-to-One" tag="Theorem"/>
      <div style={{ position:'absolute', top:320, left:'var(--safe)', right:'var(--safe)', bottom:130,
        display:'flex', flexDirection:'column', gap:54 }}>
        {/* statement card — gold (theorem) */}
        <div style={{ display:'flex', gap:30, alignItems:'stretch', flex:'0 0 auto' }}>
          <div style={{ width:6, background:'var(--accent)', borderRadius:3, boxShadow:'0 0 14px rgba(244,177,58,.4)' }}/>
          <p className="body" style={{ fontSize:40, color:'var(--primary)', maxWidth:1400 }}>
            If <M>{String.raw`f`}</M> is <span className="c-accent">strictly increasing</span> on an interval <M>{String.raw`I`}</M>,
            then <M>{String.raw`f`}</M> is one-to-one on <M>{String.raw`I`}</M>.
          </p>
        </div>
        {/* proof */}
        <div style={{ display:'flex', flexDirection:'column', gap:30, paddingLeft:36, flex:'0 0 auto' }}>
          <span className="eyebrow" style={{ color:'var(--muted)', fontSize:22 }}>Proof</span>
          {proof.map((p,i)=>(
            <div key={i} style={{ display:'flex', gap:20, alignItems:'center', flex:'0 0 auto' }}>
              <PlotDot r={5} color="var(--secondary)"/>
              <span className="step" style={{ fontSize:34 }}>{p}</span>
            </div>
          ))}
          <div style={{ display:'flex', alignItems:'center', gap:18, marginTop:6, flex:'0 0 auto' }}>
            <span className="step" style={{ fontSize:34, color:'var(--success)' }}>
              Therefore <M style={{color:'var(--success)'}}>{String.raw`f`}</M> is one-to-one.
            </span>
            <span style={{ width:30,height:30,border:'3px solid var(--success)', borderRadius:3,
              display:'grid',placeItems:'center',color:'var(--success)',fontSize:18,
              boxShadow:'0 0 12px rgba(6,214,160,.4)' }}>∎</span>
          </div>
        </div>
      </div>
      <BrandMark corner="bottom-right" variant="icon-white" height={58} opacity={0.55}/>
    </div>
  );
}

// ---------------------------------------------------------------------
// section_transition — mid-roll card between subsections
// ---------------------------------------------------------------------
function B_Transition(){
  return (
    <div className="frame" style={{ background:'#eef1f6', color:'var(--brand-navy)' }}>
      <div style={{ position:'absolute', inset:0, backgroundImage:
        'linear-gradient(rgba(22,41,78,0.045) 1px, transparent 1px),'+
        'linear-gradient(90deg, rgba(22,41,78,0.045) 1px, transparent 1px)',
        backgroundSize:'80px 80px' }}/>
      {/* full color lockup once at the section opener */}
      <div style={{ position:'absolute', top:'var(--safe)', left:'var(--gutter)' }}>
        <Logo variant="lockup-color" height={132}/>
      </div>
      {/* oversized faint section index */}
      <div style={{ position:'absolute', right:120, top:90, fontFamily:'var(--font-display)',
        fontWeight:700, fontSize:240, color:'rgba(22,41,78,0.05)', lineHeight:0.8 }}>§1.1</div>
      <div style={{ position:'absolute', inset:0, display:'flex', flexDirection:'column',
        justifyContent:'center', paddingLeft:'var(--gutter)', gap:34 }}>
        <span className="eyebrow" style={{ color:'var(--brand-red)' }}>//&nbsp;&nbsp;Next</span>
        <h1 className="display" style={{ fontSize:96, maxWidth:1400, color:'var(--brand-navy)' }}>The Horizontal<br/>Line Test</h1>
        <p className="body" style={{ color:'#5a6478', fontSize:36, maxWidth:1100, marginTop:6 }}>
          A one-line picture-proof of whether a function is one-to-one.
        </p>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------
// recap_cards — end-of-section: key points + formulas to remember
// ---------------------------------------------------------------------
function B_Recap(){
  const points=[
    'One-to-one means inputs never collide on the same output.',
    'The Horizontal Line Test is the visual version of that check.',
    'An inverse exists exactly when the function is one-to-one.',
  ];
  const formulas=[
    String.raw`f(x_1)=f(x_2)\ \Longrightarrow\ x_1=x_2`,
    String.raw`\bigl(f^{-1}\!\circ f\bigr)(x)=x`,
  ];
  return (
    <div className="frame frame--grid">
      <B_Brackets/>
      <B_SceneHead title="Section 1.1 — Recap" tag="Recap"/>
      <div style={{ position:'absolute', top:300, left:'var(--safe)', right:'var(--safe)', bottom:120,
        display:'grid', gridTemplateColumns:'1.15fr 0.85fr', gap:80, alignItems:'center' }}>
        {/* points */}
        <div style={{ display:'flex', flexDirection:'column', gap:34 }}>
          {points.map((t,i)=>(
            <div key={i} style={{ display:'flex', gap:22, alignItems:'flex-start' }}>
              <span className="eyebrow" style={{ color:'var(--accent)', fontSize:24, marginTop:4 }}>0{i+1}</span>
              <PlotDot r={6} color="var(--accent)" style={{ marginTop:14 }}/>
              <span className="step" style={{ fontSize:34 }}>{t}</span>
            </div>
          ))}
        </div>
        {/* formula cards */}
        <div style={{ display:'flex', flexDirection:'column', gap:28 }}>
          <span className="eyebrow" style={{ color:'var(--secondary)', fontSize:20 }}>Remember</span>
          {formulas.map((f,i)=>(
            <div key={i} style={{ border:'1.5px solid var(--hairline)', borderRadius:4,
              background:'rgba(10,14,26,0.6)', padding:'30px 34px', display:'flex', alignItems:'center',
              justifyContent:'center', borderLeft:'4px solid var(--secondary)' }}>
              <M display style={{ color:'var(--math)' }}>{f}</M>
            </div>
          ))}
        </div>
      </div>
      <BrandMark corner="bottom-right" variant="icon-white" height={58} opacity={0.55}/>
    </div>
  );
}

Object.assign(window, { B_Example, B_Procedure, B_Theorem, B_Transition, B_Recap });

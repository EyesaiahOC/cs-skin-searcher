// Small reusable components for the CS Art Viewer UI kit
const { useState, useEffect, useRef } = React;

// --- Lucide-ish icons as inline SVG (to avoid CDN dep timing issues) ---
const Icon = ({ name, size=14 }) => {
  const paths = {
    search: <><circle cx="11" cy="11" r="7"/><path d="m21 21-4.35-4.35"/></>,
    'chevron-left':  <path d="m15 18-6-6 6-6"/>,
    'chevron-right': <path d="m9 18 6-6-6-6"/>,
    'arrow-up-right':<><path d="M7 7h10v10"/><path d="M7 17 17 7"/></>,
    crosshair: <><circle cx="12" cy="12" r="9"/><path d="M22 12h-4M6 12H2M12 6V2M12 22v-4"/></>,
    tag: <><path d="M12 2H2v10l9.29 9.29a1 1 0 0 0 1.41 0l7.3-7.3a1 1 0 0 0 0-1.41Z"/><circle cx="7" cy="7" r="1"/></>,
    plus: <path d="M5 12h14M12 5v14"/>,
    x: <path d="M18 6 6 18M6 6l12 12"/>,
    shuffle: <><path d="M2 18h1.9c1.5 0 2.9-.7 3.8-1.9l6.6-9.2A4.7 4.7 0 0 1 18.1 5H22"/><path d="m18 2 4 3-4 3M22 18h-3.9c-1.5 0-2.9-.7-3.8-1.9L13 14"/><path d="m2 6 4 3-4 3M18 22l4-3-4-3"/></>,
    filter: <path d="M3 6h18M7 12h10M10 18h4"/>,
    'skip-forward': <><polygon points="5 4 15 12 5 20 5 4"/><line x1="19" x2="19" y1="5" y2="19"/></>,
    'image-off': <><path d="M3 3l18 18"/><path d="M21 15V5a2 2 0 0 0-2-2H7"/><path d="M3 7v12a2 2 0 0 0 2 2h14"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L14 13"/><circle cx="10" cy="9" r="1.5"/></>,
  };
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
         stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"
         style={{display:'inline-block', verticalAlign:'middle'}}>
      {paths[name] || null}
    </svg>
  );
};

// --- Brand mark ---
const Brand = () => (
  <div className="brand">
    <svg width="22" height="22" viewBox="0 0 32 32">
      <rect x="1" y="1" width="30" height="30" fill="none" stroke="#3A6090" strokeWidth="2"/>
      <path d="M8 14 L14 8 L24 8 L24 14 L18 20 L8 20 Z" fill="none" stroke="#4A7FB5" strokeWidth="1.5"/>
      <circle cx="16" cy="14" r="2" fill="#E4AE39"/>
    </svg>
    <span>CS2 SKIN BROWSER</span>
  </div>
);

// --- Rarity pill ---
const RarityPill = ({ rarity }) => {
  const r = RARITY[rarity] || RARITY['Mil-Spec'];
  return (
    <span className="rarity-pill" style={{background:r.bg, color:r.color}}>
      <span className="dot" style={{background:r.color}}/>{rarity}
    </span>
  );
};

// --- Tag chip ---
const TagChip = ({ label, onRemove, selected, onClick }) => (
  <span className={'tag-chip' + (selected ? ' selected' : '')} onClick={onClick}>
    {label}
    {onRemove && <span className="rm" onClick={(e)=>{e.stopPropagation(); onRemove();}}><Icon name="x" size={11}/></span>}
  </span>
);

// --- Skin tile ---
const SkinTile = ({ skin, active, onClick }) => {
  return (
    <div className={'skin-tile' + (active ? ' active' : '')} onClick={onClick}>
      <div className="thumb" style={{background: skin.color || skin.grad || '#253347'}}>
        <div className="thumb-missing">
          <Icon name="image-off" size={22}/>
          <span>no preview</span>
        </div>
      </div>
      <div className="name">{skin.name}</div>
      <div className="meta">{skin.rarity} · {skin.collection?.replace(/^The |Collection$/g,'').trim() || '—'}</div>
    </div>
  );
};

// --- Top bar (nav) ---
const TopBar = ({ query, setQuery, weapon, setWeapon, resultCount, onTagger, onRandom, onBack, showBack }) => (
  <div className="nav-bar">
    <Brand/>
    {showBack && (
      <button className="btn" onClick={onBack}>
        <Icon name="chevron-left"/> Back
      </button>
    )}
    <select className="combo" value={weapon} onChange={e=>setWeapon(e.target.value)}>
      {WEAPONS.map(w => <option key={w} value={w}>{w}</option>)}
    </select>
    <input className="input search" placeholder="Search skins, tags…" value={query}
           onChange={e=>setQuery(e.target.value)} style={{width:240}}/>
    <span className="result-count">{resultCount} result{resultCount===1?'':'s'}</span>
    <div className="nav-spacer"/>
    <button className="btn" onClick={onRandom} title="Random skin"><Icon name="shuffle"/> Random</button>
    <button className="btn" onClick={onTagger}><Icon name="tag"/> Tagger</button>
  </div>
);

// --- Status bar ---
const StatusBar = ({ loaded, ready, current }) => (
  <div className="status-bar">
    <span>{loaded.toLocaleString()} skins loaded</span>
    <span>·</span>
    <span>{ready ? 'ready' : 'loading…'}</span>
    <div className="nav-spacer"/>
    {current && <span>now viewing: <span style={{color:'#E0E8F0'}}>{current}</span></span>}
  </div>
);

// --- Scrubber ---
const Scrubber = ({ frame, setFrame, total=10 }) => (
  <div className="scrubber">
    <button className="btn icon" onClick={()=>setFrame(Math.max(0, frame-1))}><Icon name="chevron-left"/></button>
    <input type="range" className="slider" min="0" max={total-1} value={frame}
           onChange={e=>setFrame(Number(e.target.value))} style={{flex:1}}/>
    <button className="btn icon" onClick={()=>setFrame(Math.min(total-1, frame+1))}><Icon name="chevron-right"/></button>
    <span className="frame-label">FRAME {frame+1} / {total}</span>
  </div>
);

// --- Card wrapper ---
const Card = ({ title, children, style }) => (
  <div className="card" style={style}>
    {title && <div className="card-title">{title}</div>}
    <div className="card-body">{children}</div>
  </div>
);

Object.assign(window, { Icon, Brand, RarityPill, TagChip, SkinTile, TopBar, StatusBar, Scrubber, Card });

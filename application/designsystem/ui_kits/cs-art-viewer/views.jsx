// Main views for CS Art Viewer UI kit

const BrowserView = ({ skins, query, setQuery, weapon, setWeapon, onOpen, activeIdx, onTagger, onRandom }) => {
  const filtered = skins.map((s, i) => ({s, i})).filter(({s}) => {
    if (weapon !== 'All Weapons' && s.weapon !== weapon) return false;
    if (!query.trim()) return true;
    const q = query.toLowerCase();
    return s.name.toLowerCase().includes(q)
        || s.weapon.toLowerCase().includes(q)
        || s.tags.some(t => t.toLowerCase().includes(q));
  });

  return (
    <>
      <TopBar query={query} setQuery={setQuery} weapon={weapon} setWeapon={setWeapon}
              resultCount={filtered.length} onTagger={onTagger} onRandom={onRandom}/>
      <div className="skin-grid scroll">
        {filtered.map(({s, i}) => (
          <SkinTile key={i} skin={s} active={i===activeIdx} onClick={()=>onOpen(i)}/>
        ))}
        {filtered.length === 0 && (
          <div style={{gridColumn:'1 / -1', textAlign:'center', padding:'60px 0', color:'#4A6080', fontFamily:'var(--font-mono)', letterSpacing:'.1em'}}>
            NO SKINS MATCH — try a different weapon or query
          </div>
        )}
      </div>
    </>
  );
};

const DetailView = ({ skin, onBack, onTagger, onRandom, weapon, setWeapon, query, setQuery, skins }) => {
  const [frame, setFrame] = React.useState(0);
  const [tags, setTags] = React.useState(skin.tags);
  const [newTag, setNewTag] = React.useState('');
  const [selectedTag, setSelectedTag] = React.useState(null);

  React.useEffect(()=>{ setTags(skin.tags); setFrame(0); setSelectedTag(null); }, [skin]);

  const addTag = () => {
    const t = newTag.trim().toLowerCase();
    if (t && !tags.includes(t)) setTags([...tags, t]);
    setNewTag('');
  };
  const removeTag = (t) => setTags(tags.filter(x=>x!==t));

  // Block color placeholder — real app swaps in webm frame URL here.
  const previewStyle = {
    background: skin.color || skin.grad || '#304060',
    width: '100%', height: '100%',
  };

  return (
    <>
      <TopBar query={query} setQuery={setQuery} weapon={weapon} setWeapon={setWeapon}
              resultCount={skins.length} onTagger={onTagger} onRandom={onRandom}
              onBack={onBack} showBack={true}/>
      <div className="detail-layout">
        <div className="detail-preview">
          <div className="preview-frame">
            <div style={previewStyle}/>
            <div className="missing-large">
              <Icon name="image-off" size={48}/>
              <span>no preview · webm not loaded</span>
            </div>
          </div>
          <Scrubber frame={frame} setFrame={setFrame}/>
        </div>

        <div style={{display:'flex', flexDirection:'column', gap:12, minHeight:0}}>
          <Card>
            <div style={{fontSize:18, fontWeight:700, color:'#E0E8F0', marginBottom:10, lineHeight:1.2}}>
              {skin.name}
            </div>
            <div style={{marginBottom:10}}><RarityPill rarity={skin.rarity}/></div>
            <div className="meta-row"><span className="k">Weapon:</span><span className="v">{skin.weapon}</span></div>
            <div className="meta-row"><span className="k">Rarity:</span><span className="v">{skin.rarity}</span></div>
            <div className="meta-row"><span className="k">Collection:</span><span className="v">{skin.collection || '—'}</span></div>
          </Card>

          <Card title="TAGS" style={{flex:1, display:'flex', flexDirection:'column', minHeight:0}}>
            <div style={{display:'flex', flexWrap:'wrap', gap:6, marginBottom:10}}>
              {tags.length === 0 && <span className="muted mono" style={{fontSize:11}}>no tags — add one below</span>}
              {tags.map(t => (
                <TagChip key={t} label={t}
                         selected={t===selectedTag}
                         onClick={()=>setSelectedTag(t===selectedTag ? null : t)}
                         onRemove={()=>removeTag(t)}/>
              ))}
            </div>
            <div className="row" style={{marginTop:'auto'}}>
              <input className="input" placeholder="new-tag…" value={newTag}
                     onChange={e=>setNewTag(e.target.value)}
                     onKeyDown={e=> e.key==='Enter' && addTag()}
                     style={{flex:1}}/>
              <button className="btn" onClick={addTag}><Icon name="plus"/> Add</button>
            </div>
          </Card>

          <div className="row">
            <button className="btn grow"><Icon name="arrow-up-right"/> Workshop</button>
            <button className="btn grow"><Icon name="crosshair"/> Inspect</button>
          </div>
        </div>
      </div>
    </>
  );
};

// --- Tagger modal ---
const TaggerModal = ({ onClose, skins }) => {
  const [idx, setIdx] = React.useState(0);
  const [frame, setFrame] = React.useState(0);
  const [tags, setTags] = React.useState([]);
  const [newTag, setNewTag] = React.useState('');

  const skin = skins[idx];
  React.useEffect(()=>{ setTags([]); setFrame(0); }, [idx]);

  const addTag = () => {
    const t = newTag.trim().toLowerCase();
    if (t && !tags.includes(t)) setTags([...tags, t]);
    setNewTag('');
  };
  const saveNext = () => { if (idx < skins.length-1) setIdx(idx+1); else onClose(); };
  const skip = () => { if (idx < skins.length-1) setIdx(idx+1); };
  const prev = () => { if (idx > 0) setIdx(idx-1); };

  const previewStyle = {
    background: skin.color || skin.grad || '#304060',
    width:'100%', height:'100%',
  };

  return (
    <div className="modal-scrim" onClick={onClose}>
      <div className="modal" onClick={e=>e.stopPropagation()}>
        <div className="modal-head">
          <div className="title"><Icon name="tag" size={13}/> &nbsp; Tagger</div>
          <div className="nav-spacer"/>
          <span className="result-count">Skin {idx+1} / {skins.length} untagged</span>
          <button className="btn icon" onClick={onClose}><Icon name="x"/></button>
        </div>
        <div style={{padding:'10px 14px'}}>
          <div className="progress"><div className="chunk" style={{width: `${((idx+1)/skins.length)*100}%`}}/>
            <div className="txt">{Math.round(((idx+1)/skins.length)*100)}%</div></div>
        </div>

        <div style={{display:'grid', gridTemplateColumns:'1fr 280px', gap:14, padding:'0 14px 14px', flex:1, minHeight:0}}>
          <div className="detail-preview">
            <div className="preview-frame"><div style={previewStyle}/>
              <div className="missing-large">
                <Icon name="image-off" size={40}/>
                <span>no preview</span>
              </div>
            </div>
            <Scrubber frame={frame} setFrame={setFrame}/>
          </div>
          <div className="col" style={{minHeight:0}}>
            <Card>
              <div style={{fontSize:14, fontWeight:700, color:'#E0E8F0', marginBottom:8}}>{skin.name}</div>
              <div className="meta-row"><span className="k">Weapon:</span><span className="v">{skin.weapon}</span></div>
              <div className="meta-row"><span className="k">Rarity:</span><span className="v">{skin.rarity}</span></div>
            </Card>
            <Card title="TAGS" style={{flex:1, display:'flex', flexDirection:'column', minHeight:0}}>
              <div style={{display:'flex', flexWrap:'wrap', gap:6, marginBottom:10, minHeight:40}}>
                {tags.map(t=> <TagChip key={t} label={t} onRemove={()=>setTags(tags.filter(x=>x!==t))}/>) }
                {tags.length===0 && <span className="muted mono" style={{fontSize:11}}>empty</span>}
              </div>
              <div className="row" style={{marginTop:'auto'}}>
                <input className="input" placeholder="tag…" value={newTag}
                       onChange={e=>setNewTag(e.target.value)}
                       onKeyDown={e=> e.key==='Enter' && addTag()}
                       style={{flex:1}}/>
                <button className="btn" onClick={addTag}><Icon name="plus"/></button>
              </div>
            </Card>
          </div>
        </div>

        <div style={{padding:'10px 14px', borderTop:'1px solid #304060', display:'flex', gap:8}}>
          <button className="btn" onClick={prev} disabled={idx===0}><Icon name="chevron-left"/> Prev</button>
          <button className="btn" onClick={skip}>Skip <Icon name="skip-forward"/></button>
          <div className="nav-spacer"/>
          <button className="btn primary" onClick={saveNext}>Save &amp; Next <Icon name="chevron-right"/></button>
        </div>
      </div>
    </div>
  );
};

Object.assign(window, { BrowserView, DetailView, TaggerModal });

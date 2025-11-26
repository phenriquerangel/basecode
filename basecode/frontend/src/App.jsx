import React, { useState, useEffect } from 'react';
import { jsPDF } from "jspdf";

function App() {
  const [questoes, setQuestoes] = useState([]);
  const [topicos, setTopicos] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [busca, setBusca] = useState("");
  const [filtroTopico, setFiltroTopico] = useState("");
  const [filtroDificuldade, setFiltroDificuldade] = useState("");

  const API_URL = "/api/questoes/";
  const TOPICOS_URL = "/api/topicos/";

  useEffect(() => {
    fetch(TOPICOS_URL).then(r=>r.json()).then(setTopicos).catch(console.error);
  }, []);

  useEffect(() => {
    setLoading(true);
    let url = `${API_URL}?search=${busca}`;
    if(filtroTopico) url += `&topico=${filtroTopico}`;
    if(filtroDificuldade) url += `&dificuldade=${filtroDificuldade}`;
    
    const delay = setTimeout(() => {
        fetch(url).then(r=>r.json()).then(d=>{setQuestoes(d);setLoading(false);}).catch(console.error);
    }, 300);
    return () => clearTimeout(delay);
  }, [busca, filtroTopico, filtroDificuldade]);

  const toggleSelect = (id) => selectedIds.includes(id) ? setSelectedIds(selectedIds.filter(i=>i!==id)) : setSelectedIds([...selectedIds, id]);
  const limparFiltros = () => { setBusca(""); setFiltroTopico(""); setFiltroDificuldade(""); };

  const gerarPDF = () => {
    const doc = new jsPDF();
    const selecionadas = questoes.filter(q => selectedIds.includes(q.id));
    let y = 20;
    doc.setFontSize(22); doc.setFont("helvetica", "bold"); doc.text("Avaliação MathMaster", 105, y, {align:"center"}); y+=15;
    doc.setFontSize(12); doc.setFont("helvetica", "normal"); doc.text(`Gerado com ${selecionadas.length} questões.`, 105, y, {align:"center"}); y+=20;
    selecionadas.forEach((q, i) => {
        if(y>270){doc.addPage();y=20;}
        doc.setFont("helvetica","bold");
        const lines = doc.splitTextToSize(`${i+1}) ${q.enunciado}`, 180);
        doc.text(lines, 15, y); y += (lines.length*6)+4;
        doc.setFont("helvetica","normal");
        ['a','b','c','d'].forEach(o=>{
             if(y>280){doc.addPage();y=20;}
             doc.text(`${o.toUpperCase()}) ${q['alternativa_'+o]}`, 20, y); y+=6;
        }); y+=8;
    });
    doc.addPage(); y=20; doc.setFontSize(16); doc.text("Gabarito", 105, y, {align:"center"}); y+=20; doc.setFontSize(12);
    selecionadas.forEach((q, i)=>{doc.text(`${i+1}) ${q.correta}`, 20, y); y+=8;});
    doc.save("Prova_MathMaster.pdf");
  };

  const s = {
    page: { fontFamily: 'Inter, sans-serif', backgroundColor: '#f8fafc', minHeight: '100vh', paddingBottom: '120px' },
    nav: { backgroundColor: 'white', padding: '15px 30px', borderBottom: '1px solid #e2e8f0', position:'sticky', top:0, zIndex:10 },
    filterBox: { maxWidth: '900px', margin: '30px auto', padding: '20px', backgroundColor: 'white', borderRadius: '16px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)', display: 'flex', gap: '15px', flexWrap: 'wrap' },
    input: { flex: 2, padding: '12px', borderRadius: '8px', border: '1px solid #cbd5e1' },
    select: { flex: 1, padding: '12px', borderRadius: '8px', border: '1px solid #cbd5e1', minWidth: '150px' },
    grid: { display: 'grid', gap: '20px', maxWidth: '900px', margin: '0 auto', padding: '0 20px' },
    card: (sel) => ({ backgroundColor: sel ? '#eff6ff' : 'white', border: sel ? '2px solid #3b82f6' : '1px solid #e2e8f0', borderRadius: '12px', padding: '24px', cursor: 'pointer', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', position:'relative' }),
    badge: (bg, col) => ({ backgroundColor: bg, color: col, padding: '4px 10px', borderRadius: '20px', fontSize: '0.75rem', fontWeight: 'bold' }),
    actionBar: { position: 'fixed', bottom: '30px', left: '50%', transform: 'translateX(-50%)', backgroundColor: '#1e293b', color: 'white', padding: '12px 24px', borderRadius: '50px', display: 'flex', gap: '20px', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.3)', zIndex: 50 },
    btn: { backgroundColor: '#3b82f6', color: 'white', border: 'none', padding: '10px 25px', borderRadius: '30px', fontWeight: 'bold', cursor: 'pointer' }
  };

  return (
    <div style={s.page}>
      <nav style={s.nav}><h1 style={{fontSize:'1.2rem', margin:0}}>🎓 MathMaster</h1></nav>
      <div style={s.filterBox}>
        <input placeholder="🔎 Pesquisar..." value={busca} onChange={e=>setBusca(e.target.value)} style={s.input}/>
        <select value={filtroTopico} onChange={e=>setFiltroTopico(e.target.value)} style={s.select}>
            <option value="">Todos Tópicos</option>{topicos.map(t=><option key={t.id} value={t.id}>{t.nome}</option>)}
        </select>
        <select value={filtroDificuldade} onChange={e=>setFiltroDificuldade(e.target.value)} style={s.select}>
            <option value="">Dificuldade</option><option value="F">Fácil</option><option value="M">Médio</option><option value="D">Difícil</option>
        </select>
        {(busca||filtroTopico||filtroDificuldade) && <button onClick={limparFiltros} style={{padding:'10px', border:'1px solid red', color:'red', background:'white', borderRadius:'8px', cursor:'pointer'}}>Limpar</button>}
      </div>
      <main style={s.grid}>
        {!loading && questionsList(questoes, selectedIds, toggleSelect, s)}
      </main>
      {selectedIds.length > 0 && (
          <div style={s.actionBar}><span><strong>{selectedIds.length}</strong> selecionadas</span><button style={s.btn} onClick={gerarPDF}>📥 Baixar PDF</button></div>
      )}
    </div>
  );
}

function questionsList(questoes, selectedIds, toggleSelect, s) {
    return questoes.map(q => {
        const isSel = selectedIds.includes(q.id);
        const difColor = q.dificuldade==='F'?'#16a34a':q.dificuldade==='M'?'#d97706':'#dc2626';
        return (
            <div key={q.id} style={s.card(isSel)} onClick={() => toggleSelect(q.id)}>
                <div style={{display:'flex', gap:'10px', marginBottom:'15px'}}>
                    <span style={s.badge('#eff6ff', '#2563eb')}>{q.topico_nome}</span>
                    <span style={{...s.badge('#f1f5f9', difColor)}}>{q.dificuldade}</span>
                    {isSel && <span style={{marginLeft:'auto'}}>✅</span>}
                </div>
                <h3 style={{marginTop:0}}>{q.enunciado}</h3>
                <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'5px', fontSize:'0.9rem', color:'#64748b'}}>
                    <div>A) {q.alternativa_a}</div><div>B) {q.alternativa_b}</div><div>C) {q.alternativa_c}</div><div>D) {q.alternativa_d}</div>
                </div>
            </div>
        );
    });
}
export default App;
import React, { useState, useEffect } from 'react';
import { jsPDF } from "jspdf";
function App() {
  const [questoes, setQuestoes] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [busca, setBusca] = useState("");
  const API_URL = "/api/questoes/";

  useEffect(() => {
    setLoading(true);
    let url = API_URL + (busca ? `?search=${busca}` : "");
    const delay = setTimeout(() => {
        fetch(url).then(r=>r.json()).then(d=>{setQuestoes(d);setLoading(false);}).catch(e=>{console.error(e);setLoading(false);});
    }, 300);
    return () => clearTimeout(delay);
  }, [busca]);

  const toggleSelect = (id) => selectedIds.includes(id) ? setSelectedIds(selectedIds.filter(i=>i!==id)) : setSelectedIds([...selectedIds, id]);

  const gerarPDF = () => {
    const doc = new jsPDF();
    const selecionadas = questoes.filter(q => selectedIds.includes(q.id));
    let y = 20;
    doc.setFontSize(18); doc.setFont("helvetica", "bold"); doc.text("Avaliação MathMaster", 105, y, {align:"center"}); y+=20;
    doc.setFontSize(12); doc.setFont("helvetica", "normal");
    selecionadas.forEach((q, i) => {
        if(y>270){doc.addPage();y=20;}
        doc.setFont("helvetica","bold");
        const lines = doc.splitTextToSize(`${i+1}) ${q.enunciado}`, 180);
        doc.text(lines, 15, y); y += (lines.length*6)+4;
        doc.setFont("helvetica","normal");
        ['a','b','c','d'].forEach(o=>{
             if(y>280){doc.addPage();y=20;}
             doc.text(`${o.toUpperCase()}) ${q['alternativa_'+o]}`, 20, y); y+=6;
        });
        y+=8;
    });
    doc.addPage(); y=20; doc.setFontSize(16); doc.text("Gabarito", 105, y, {align:"center"}); y+=20; doc.setFontSize(12);
    selecionadas.forEach((q, i)=>{doc.text(`${i+1}) ${q.correta}`, 20, y); y+=8;});
    doc.save("Prova_Matematica.pdf");
  };

  const s = {
    page: { fontFamily: 'Inter, sans-serif', backgroundColor: '#f8fafc', minHeight: '100vh', paddingBottom: '120px' },
    nav: { backgroundColor: 'white', padding: '15px 30px', borderBottom: '1px solid #e2e8f0', position:'sticky', top:0, zIndex:10 },
    searchBar: { maxWidth: '800px', margin: '30px auto', padding: '0 20px' },
    input: { width: '100%', padding: '16px', borderRadius: '12px', border: '1px solid #cbd5e1', fontSize: '1rem' },
    grid: { display: 'grid', gap: '20px', maxWidth: '800px', margin: '0 auto', padding: '0 20px' },
    card: (isSelected) => ({
        backgroundColor: isSelected ? '#eff6ff' : 'white',
        border: isSelected ? '2px solid #3b82f6' : '1px solid #e2e8f0',
        borderRadius: '16px', padding: '24px', cursor: 'pointer', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', position:'relative'
    }),
    badge: { backgroundColor: '#f1f5f9', color: '#475569', padding: '4px 10px', borderRadius: '20px', fontSize: '0.75rem', fontWeight: 'bold' },
    actionBar: {
        position: 'fixed', bottom: '30px', left: '50%', transform: 'translateX(-50%)',
        backgroundColor: '#1e293b', color: 'white', padding: '12px 24px', borderRadius: '50px',
        display: 'flex', alignItems: 'center', gap: '20px', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.3)', zIndex:50
    },
    btn: { backgroundColor: '#3b82f6', color: 'white', border: 'none', padding: '10px 20px', borderRadius: '30px', fontWeight: 'bold', cursor: 'pointer' }
  };

  return (
    <div style={s.page}>
      <nav style={s.nav}><h1 style={{fontSize:'1.2rem', margin:0}}>🎓 MathMaster</h1></nav>
      <div style={s.searchBar}><input placeholder="🔎 Pesquisar..." value={busca} onChange={e=>setBusca(e.target.value)} style={s.input}/></div>
      <main style={s.grid}>
        {!loading && questoes.map(q => {
           const isSel = selectedIds.includes(q.id);
           return (
             <div key={q.id} style={s.card(isSel)} onClick={() => toggleSelect(q.id)}>
               <div style={{display:'flex',gap:'10px',marginBottom:'15px'}}>
                   <span style={s.badge}>{q.topico_nome || 'Geral'}</span>
                   <span style={{...s.badge, color: q.dificuldade==='F'?'green':q.dificuldade==='M'?'orange':'red'}}>{q.dificuldade}</span>
               </div>
               {isSel && <div style={{position:'absolute',top:'20px',right:'20px',fontSize:'1.5rem'}}>✅</div>}
               <h3 style={{marginTop:0}}>{q.enunciado}</h3>
               <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'5px',fontSize:'0.9rem',color:'#666'}}>
                   <div>A) {q.alternativa_a}</div><div>B) {q.alternativa_b}</div><div>C) {q.alternativa_c}</div><div>D) {q.alternativa_d}</div>
               </div>
             </div>
           )
        })}
      </main>
      {selectedIds.length > 0 && (
          <div style={s.actionBar}><span><strong>{selectedIds.length}</strong> selecionadas</span><button style={s.btn} onClick={gerarPDF}>📥 Baixar PDF</button></div>
      )}
    </div>
  );
}
export default App;
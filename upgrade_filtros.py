import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Frontend Atualizado: {path}")

root_front = "basecode/frontend/src"

# APP.JSX (Com Filtros Avançados e UI Polida)
app_jsx = """
import React, { useState, useEffect } from 'react';
import { jsPDF } from "jspdf";

function App() {
  const [questoes, setQuestoes] = useState([]);
  const [topicos, setTopicos] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Estados dos Filtros
  const [busca, setBusca] = useState("");
  const [filtroTopico, setFiltroTopico] = useState("");
  const [filtroDificuldade, setFiltroDificuldade] = useState("");

  const API_URL = "/api/questoes/";
  const TOPICOS_URL = "/api/topicos/";

  // 1. Carrega Tópicos (Apenas uma vez)
  useEffect(() => {
    fetch(TOPICOS_URL).then(r=>r.json()).then(setTopicos).catch(console.error);
  }, []);

  // 2. Carrega Questões (Sempre que mudar filtros)
  useEffect(() => {
    setLoading(true);
    let url = `${API_URL}?search=${busca}`;
    if(filtroTopico) url += `&topico=${filtroTopico}`;
    if(filtroDificuldade) url += `&dificuldade=${filtroDificuldade}`;
    
    const delay = setTimeout(() => {
        fetch(url)
          .then(r => r.json())
          .then(d => { setQuestoes(d); setLoading(false); })
          .catch(e => { console.error(e); setLoading(false); });
    }, 300); // Debounce de 300ms
    return () => clearTimeout(delay);
  }, [busca, filtroTopico, filtroDificuldade]);

  // Ações
  const toggleSelect = (id) => selectedIds.includes(id) ? setSelectedIds(selectedIds.filter(i=>i!==id)) : setSelectedIds([...selectedIds, id]);
  
  const limparFiltros = () => {
    setBusca("");
    setFiltroTopico("");
    setFiltroDificuldade("");
  };

  const gerarPDF = () => {
    const doc = new jsPDF();
    const selecionadas = questoes.filter(q => selectedIds.includes(q.id));
    let y = 20;
    
    // Capa
    doc.setFontSize(22); doc.setFont("helvetica", "bold"); doc.text("Avaliação MathMaster", 105, y, {align:"center"}); y+=15;
    doc.setFontSize(12); doc.setFont("helvetica", "normal"); doc.text(`Gerado com ${selecionadas.length} questões selecionadas.`, 105, y, {align:"center"}); y+=20;

    // Questões
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

    // Gabarito
    doc.addPage(); y=20; doc.setFontSize(16); doc.text("Gabarito Oficial", 105, y, {align:"center"}); y+=20; doc.setFontSize(12);
    selecionadas.forEach((q, i)=>{doc.text(`${i+1}) ${q.correta}`, 20, y); y+=8;});
    
    doc.save("Prova_MathMaster.pdf");
  };

  // --- STYLES (Design Moderno) ---
  const s = {
    page: { fontFamily: 'Inter, sans-serif', backgroundColor: '#f8fafc', minHeight: '100vh', paddingBottom: '120px' },
    
    // Navbar
    nav: { backgroundColor: 'white', padding: '15px 30px', borderBottom: '1px solid #e2e8f0', position:'sticky', top:0, zIndex:10, display:'flex', justifyContent:'space-between', alignItems:'center' },
    brand: { fontSize: '1.25rem', fontWeight: '800', color: '#1e293b', margin: 0 },
    
    // Área de Filtros (Box Branco Flutuante)
    filterBox: { 
        maxWidth: '900px', margin: '30px auto', padding: '20px', 
        backgroundColor: 'white', borderRadius: '16px', 
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
        display: 'flex', gap: '15px', flexWrap: 'wrap', alignItems: 'center'
    },
    input: { flex: 2, padding: '12px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.95rem', minWidth: '200px' },
    select: { flex: 1, padding: '12px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.95rem', minWidth: '150px', backgroundColor: 'white' },
    btnClean: { padding: '12px 20px', borderRadius: '8px', border: '1px solid #ef4444', color: '#ef4444', background: 'white', cursor: 'pointer', fontWeight:'bold' },
    
    // Contador de Resultados
    resultsInfo: { maxWidth: '900px', margin: '0 auto 20px', padding: '0 20px', color: '#64748b', fontSize: '0.9rem', fontWeight: '500' },

    // Grid
    grid: { display: 'grid', gap: '20px', maxWidth: '900px', margin: '0 auto', padding: '0 20px' },
    
    // Cartões
    card: (isSelected) => ({
        backgroundColor: isSelected ? '#eff6ff' : 'white',
        border: isSelected ? '2px solid #3b82f6' : '1px solid #e2e8f0',
        borderRadius: '12px', padding: '24px', cursor: 'pointer',
        transition: 'all 0.2s ease', position: 'relative'
    }),
    
    badge: (bg, col) => ({ backgroundColor: bg, color: col, padding: '4px 10px', borderRadius: '20px', fontSize: '0.75rem', fontWeight: 'bold' }),
    
    // Empty State
    empty: { textAlign: 'center', padding: '50px', color: '#94a3b8' },

    // Floating Bar
    actionBar: {
        position: 'fixed', bottom: '30px', left: '50%', transform: 'translateX(-50%)',
        backgroundColor: '#1e293b', color: 'white', padding: '12px 24px', borderRadius: '50px',
        display: 'flex', alignItems: 'center', gap: '20px', boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.3)',
        zIndex: 50, minWidth: '300px', justifyContent: 'space-between'
    },
    btnDownload: { backgroundColor: '#3b82f6', color: 'white', border: 'none', padding: '10px 25px', borderRadius: '30px', fontWeight: 'bold', cursor: 'pointer' }
  };

  const temFiltroAtivo = busca || filtroTopico || filtroDificuldade;

  return (
    <div style={s.page}>
      <nav style={s.nav}>
        <h1 style={s.brand}>🎓 MathMaster <span style={{fontWeight:'normal', fontSize:'0.9rem', color:'#64748b'}}>| Professor</span></h1>
      </nav>

      <div style={s.filterBox}>
        <input 
            placeholder="🔎 Pesquisar enunciado..." 
            value={busca} onChange={e => setBusca(e.target.value)}
            style={s.input}
        />
        <select value={filtroTopico} onChange={e => setFiltroTopico(e.target.value)} style={s.select}>
            <option value="">Todos os Tópicos</option>
            {topicos.map(t => <option key={t.id} value={t.id}>{t.nome}</option>)}
        </select>
        <select value={filtroDificuldade} onChange={e => setFiltroDificuldade(e.target.value)} style={s.select}>
            <option value="">Todas Dificuldades</option>
            <option value="F">Fácil</option>
            <option value="M">Médio</option>
            <option value="D">Difícil</option>
        </select>
        
        {temFiltroAtivo && (
            <button onClick={limparFiltros} style={s.btnClean}>Limpar ✕</button>
        )}
      </div>

      <div style={s.resultsInfo}>
        {loading ? "Carregando..." : `${questoes.length} questões encontradas`}
      </div>

      <main style={s.grid}>
        {!loading && questionsList(questoes, selectedIds, toggleSelect, s)}
        
        {!loading && questoes.length === 0 && (
            <div style={s.empty}>
                <h2>Nenhuma questão encontrada 😕</h2>
                <p>Tente ajustar os filtros ou limpar a busca.</p>
                {temFiltroAtivo && <button onClick={limparFiltros} style={{...s.btnClean, marginTop:'20px'}}>Limpar Filtros</button>}
            </div>
        )}
      </main>

      {selectedIds.length > 0 && (
          <div style={s.actionBar}>
            <span><strong>{selectedIds.length}</strong> selecionadas</span>
            <button style={s.btnDownload} onClick={gerarPDF}>📥 Baixar PDF</button>
          </div>
      )}
    </div>
  );
}

function questionsList(questoes, selectedIds, toggleSelect, s) {
    return questoes.map(q => {
        const isSelected = selectedIds.includes(q.id);
        const difColor = q.dificuldade==='F'?'#16a34a':q.dificuldade==='M'?'#d97706':'#dc2626';
        const difBg = q.dificuldade==='F'?'#dcfce7':q.dificuldade==='M'?'#fef3c7':'#fee2e2';

        return (
            <div key={q.id} style={s.card(isSelected)} onClick={() => toggleSelect(q.id)}>
                <div style={{display:'flex', gap:'10px', marginBottom:'15px', alignItems:'center'}}>
                    <span style={s.badge('#eff6ff', '#2563eb')}>{q.topico_nome || 'Geral'}</span>
                    <span style={s.badge(difBg, difColor)}>
                        {q.dificuldade === 'F' ? 'Fácil' : q.dificuldade === 'M' ? 'Médio' : 'Difícil'}
                    </span>
                    {isSelected && <span style={{marginLeft:'auto', fontSize:'1.2rem'}}>✅</span>}
                </div>
                
                <h3 style={{margin:'0 0 15px 0', color:'#334155'}}>{q.enunciado}</h3>
                
                <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'8px', fontSize:'0.9rem', color:'#64748b'}}>
                    <div>A) {q.alternativa_a}</div><div>B) {q.alternativa_b}</div>
                    <div>C) {q.alternativa_c}</div><div>D) {q.alternativa_d}</div>
                </div>
            </div>
        );
    });
}

export default App;
"""

files = {
    f"{root_front}/App.jsx": app_jsx,
}

print("🎨 Atualizando Filtros do Frontend (v24)...")
for path, content in files.items():
    create_file(path, content)
print("✨ Feito! Execute o build v24.")
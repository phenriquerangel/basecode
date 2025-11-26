import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Frontend Atualizado: {path}")

root_front = "basecode/frontend"

# 1. PACKAGE.JSON (Garantindo jsPDF)
package_json = """
{
  "name": "front",
  "private": true,
  "version": "2.0.0",
  "type": "module",
  "scripts": { "dev": "vite", "build": "vite build" },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "jspdf": "^2.5.1" 
  },
  "devDependencies": { "@vitejs/plugin-react": "^4.2.1", "vite": "^5.2.0" }
}
"""

# 2. APP.JSX (A Interface do Professor + Gerador PDF)
app_jsx = """
import React, { useState, useEffect } from 'react';
import { jsPDF } from "jspdf";

function App() {
  const [questoes, setQuestoes] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [busca, setBusca] = useState("");
  
  // URL da API (usando o proxy interno)
  const API_URL = "/api/questoes/";

  // Carregar dados
  useEffect(() => {
    setLoading(true);
    let url = API_URL;
    if (busca) url += `?search=${busca}`;
    
    // Pequeno delay para não flodar a API enquanto digita
    const delay = setTimeout(() => {
        fetch(url)
          .then(r => r.json())
          .then(d => { setQuestoes(d); setLoading(false); })
          .catch(e => { console.error(e); setLoading(false); });
    }, 300);
    return () => clearTimeout(delay);
  }, [busca]);

  // Lógica de Seleção
  const toggleSelect = (id) => {
    if (selectedIds.includes(id)) {
      setSelectedIds(selectedIds.filter(i => i !== id));
    } else {
      setSelectedIds([...selectedIds, id]);
    }
  };

  // --- O GERADOR DE PDF ---
  const gerarPDF = () => {
    const doc = new jsPDF();
    const selecionadas = questoes.filter(q => selectedIds.includes(q.id));
    
    // Configurações iniciais
    let y = 20;
    const margemEsq = 15;
    const larguraTexto = 180;

    // --- PÁGINA 1: A PROVA ---
    doc.setFontSize(18);
    doc.setFont("helvetica", "bold");
    doc.text("Avaliação de Matemática", 105, y, { align: "center" });
    y += 10;
    
    doc.setFontSize(10);
    doc.setFont("helvetica", "normal");
    doc.text("Nome: _________________________________________________ Data: ___/___/___", 105, y, { align: "center" });
    y += 20;

    doc.setFontSize(12);

    selecionadas.forEach((q, index) => {
        // Checa se cabe na página
        if (y > 270) { doc.addPage(); y = 20; }

        // Enunciado
        doc.setFont("helvetica", "bold");
        const linhasTitulo = doc.splitTextToSize(`${index + 1}) ${q.enunciado}`, larguraTexto);
        doc.text(linhasTitulo, margemEsq, y);
        y += (linhasTitulo.length * 6) + 4;

        // Alternativas
        doc.setFont("helvetica", "normal");
        ['a', 'b', 'c', 'd'].forEach(opt => {
            if (y > 280) { doc.addPage(); y = 20; }
            const textoOpt = `${opt.toUpperCase()}) ${q['alternativa_' + opt]}`;
            doc.text(textoOpt, margemEsq + 5, y);
            y += 6;
        });
        y += 8; // Espaço entre questões
    });

    // --- PÁGINA FINAL: O GABARITO ---
    doc.addPage();
    y = 20;
    doc.setFontSize(16);
    doc.setFont("helvetica", "bold");
    doc.text("Gabarito do Professor", 105, y, { align: "center" });
    y += 20;

    doc.setFontSize(11);
    doc.setFont("helvetica", "normal");

    selecionadas.forEach((q, index) => {
        doc.text(`${index + 1}) Resposta: ${q.correta}`, margemEsq, y);
        
        // Justificativa
        doc.setFont("helvetica", "italic");
        doc.setTextColor(100); // Cinza
        const linhasJust = doc.splitTextToSize(`   Explicação: ${q.justificativa}`, larguraTexto);
        doc.text(linhasJust, margemEsq, y + 5);
        doc.setTextColor(0); // Preto
        doc.setFont("helvetica", "normal");

        y += (linhasJust.length * 5) + 12;
    });

    // Download
    doc.save("Prova_Matematica.pdf");
  };

  // --- ESTILOS (UI) ---
  const s = {
    page: { fontFamily: 'Inter, sans-serif', backgroundColor: '#f8fafc', minHeight: '100vh', paddingBottom: '120px' },
    nav: { backgroundColor: 'white', padding: '15px 30px', borderBottom: '1px solid #e2e8f0', position:'sticky', top:0, zIndex:10, boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' },
    brand: { fontSize: '1.25rem', fontWeight: '800', color: '#1e293b', margin: 0 },
    
    searchBar: { maxWidth: '800px', margin: '30px auto', padding: '0 20px' },
    input: { width: '100%', padding: '16px', borderRadius: '12px', border: '1px solid #cbd5e1', fontSize: '1rem', boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)' },
    
    grid: { display: 'grid', gap: '20px', maxWidth: '800px', margin: '0 auto', padding: '0 20px' },
    
    card: (isSelected) => ({
        backgroundColor: isSelected ? '#eff6ff' : 'white',
        border: isSelected ? '2px solid #3b82f6' : '1px solid #e2e8f0',
        borderRadius: '16px',
        padding: '24px',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        boxShadow: isSelected ? '0 4px 6px -1px rgba(59, 130, 246, 0.1)' : '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
        position: 'relative'
    }),
    
    badge: { backgroundColor: '#f1f5f9', color: '#475569', padding: '4px 10px', borderRadius: '20px', fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase' },
    check: { position: 'absolute', top: '20px', right: '20px', fontSize: '1.5rem', color: '#3b82f6' },
    
    // BARRA FLUTUANTE
    actionBar: {
        position: 'fixed', bottom: '30px', left: '50%', transform: 'translateX(-50%)',
        backgroundColor: '#1e293b', color: 'white', padding: '12px 24px', borderRadius: '50px',
        display: 'flex', alignItems: 'center', gap: '20px', boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.3)',
        zIndex: 50, minWidth: '300px', justifyContent: 'space-between'
    },
    btn: {
        backgroundColor: '#3b82f6', color: 'white', border: 'none', padding: '10px 20px',
        borderRadius: '30px', fontWeight: 'bold', cursor: 'pointer', fontSize: '0.95rem'
    }
  };

  return (
    <div style={s.page}>
      <nav style={s.nav}>
        <h1 style={s.brand}>🎓 MathMaster <span style={{fontWeight:'normal', fontSize:'0.9rem', color:'#64748b'}}>| Painel do Professor</span></h1>
      </nav>

      <div style={s.searchBar}>
        <input 
            placeholder="🔎 Pesquise por enunciado (ex: raiz quadrada, logaritmo)..." 
            value={busca} 
            onChange={e => setBusca(e.target.value)}
            style={s.input}
        />
      </div>

      <main style={s.grid}>
        {loading && <p style={{textAlign:'center', color:'#64748b'}}>Carregando questões...</p>}
        
        {!loading && questionsList(questoes, selectedIds, toggleSelect, s)}
      </main>

      {/* BARRA DE AÇÃO FLUTUANTE */}
      {selectedIds.length > 0 && (
          <div style={s.actionBar}>
            <span><strong>{selectedIds.length}</strong> questões selecionadas</span>
            <button style={s.btn} onClick={gerarPDF}>
                📥 Baixar PDF
            </button>
          </div>
      )}
    </div>
  );
}

function questionsList(questoes, selectedIds, toggleSelect, s) {
    if (questoes.length === 0) return <p style={{textAlign:'center', color:'#94a3b8'}}>Nenhuma questão encontrada.</p>;

    return questoes.map(q => {
        const isSelected = selectedIds.includes(q.id);
        return (
            <div key={q.id} style={s.card(isSelected)} onClick={() => toggleSelect(q.id)}>
                <div style={{display:'flex', gap:'10px', marginBottom:'15px'}}>
                    <span style={s.badge}>{q.topico_nome || 'Geral'}</span>
                    <span style={{...s.badge, color: q.dificuldade === 'F' ? '#16a34a' : q.dificuldade === 'M' ? '#d97706' : '#dc2626'}}>
                        {q.dificuldade === 'F' ? 'Fácil' : q.dificuldade === 'M' ? 'Médio' : 'Difícil'}
                    </span>
                </div>
                
                {isSelected && <div style={s.check}>✅</div>}
                
                <h3 style={{margin:'0 0 15px 0', color:'#334155'}}>{q.enunciado}</h3>
                
                <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'8px', fontSize:'0.9rem', color:'#64748b'}}>
                    <div>A) {q.alternativa_a}</div>
                    <div>B) {q.alternativa_b}</div>
                    <div>C) {q.alternativa_c}</div>
                    <div>D) {q.alternativa_d}</div>
                </div>
            </div>
        );
    });
}

export default App;
"""

files = {
    f"{root_front}/package.json": package_json,
    f"{root_front}/src/App.jsx": app_jsx,
}

print("📄 Criando UI do Professor com Gerador de PDF Cliente...")
for path, content in files.items():
    create_file(path, content)
print("✨ Arquivos atualizados! Faça o Build v23 (Frontend apenas).")

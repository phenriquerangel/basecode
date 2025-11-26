import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Atualizado: {path}")

root = "basecode/frontend/src"

# 1. APP.JSX (A Lógica Principal)
# Aqui fazemos o 'fetch' para pegar os dados do Django
app_jsx = """
import React, { useState, useEffect } from 'react';

function App() {
  const [questoes, setQuestoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState(null);

  // Endereço da API (No futuro, isso vira variável de ambiente)
  const API_URL = "http://localhost:8000/api/questoes/";

  useEffect(() => {
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error('Erro ao conectar com a API');
        }
        return response.json();
      })
      .then(data => {
        setQuestoes(data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Erro:", error);
        setErro("Não foi possível carregar as questões. Verifique se o Backend está rodando.");
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <header style={{ textAlign: 'center', marginBottom: '40px', borderBottom: '2px solid #eee', paddingBottom: '20px' }}>
        <h1 style={{ color: '#2c3e50' }}>📚 Banco de Questões</h1>
        <p style={{ color: '#7f8c8d' }}>Estude com questões atualizadas</p>
      </header>

      <main>
        {loading && <p style={{ textAlign: 'center' }}>Carregando questões...</p>}
        
        {erro && (
          <div style={{ backgroundColor: '#fee', color: '#c0392b', padding: '15px', borderRadius: '5px' }}>
            {erro}
          </div>
        )}

        {!loading && !erro && questionsList(questoes)}
      </main>
    </div>
  );
}

function questionsList(questoes) {
  if (questoes.length === 0) {
    return <p style={{ textAlign: 'center', color: '#999' }}>Nenhuma questão cadastrada ainda.</p>;
  }

  return (
    <div style={{ display: 'grid', gap: '20px' }}>
      {questoes.map(q => (
        <div key={q.id} style={{ 
            border: '1px solid #ddd', 
            borderRadius: '8px', 
            padding: '20px',
            backgroundColor: '#fff',
            boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
        }}>
          <div style={{ marginBottom: '10px' }}>
            <span style={{ 
                backgroundColor: '#e3f2fd', 
                color: '#1565c0', 
                padding: '4px 8px', 
                borderRadius: '4px', 
                fontSize: '0.8em',
                fontWeight: 'bold'
            }}>
              {q.topico_nome || 'Geral'}
            </span>
            <span style={{ 
                marginLeft: '10px',
                color: q.dificuldade === 'F' ? 'green' : q.dificuldade === 'M' ? 'orange' : 'red',
                fontWeight: 'bold',
                fontSize: '0.8em'
            }}>
              {q.dificuldade === 'F' ? 'Fácil' : q.dificuldade === 'M' ? 'Médio' : 'Difícil'}
            </span>
          </div>
          
          <h3 style={{ margin: '0 0 15px 0', color: '#333' }}>{q.enunciado}</h3>
          
          <div style={{ display: 'grid', gap: '8px' }}>
            <Option label="A" text={q.alternativa_a} />
            <Option label="B" text={q.alternativa_b} />
            <Option label="C" text={q.alternativa_c} />
            <Option label="D" text={q.alternativa_d} />
          </div>

          <details style={{ marginTop: '15px', borderTop: '1px solid #eee', paddingTop: '10px', color: '#666', cursor: 'pointer' }}>
            <summary>Ver Resposta</summary>
            <p><strong>Correta:</strong> {q.correta}</p>
            <p><em>{q.justificativa}</em></p>
          </details>
        </div>
      ))}
    </div>
  );
}

function Option({ label, text }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '8px', backgroundColor: '#f9f9f9', borderRadius: '4px' }}>
      <strong style={{ minWidth: '20px' }}>{label})</strong>
      <span>{text}</span>
    </div>
  );
}

export default App;
"""

files = {
    f"{root}/App.jsx": app_jsx,
}

print("🚀 Atualizando Frontend para consumir a API...")
for path, content in files.items():
    create_file(path, content)
print("✨ Frontend atualizado! Faça o Build v3 do Frontend.")
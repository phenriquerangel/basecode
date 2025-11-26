import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Atualizado: {path}")

root_front = "basecode/frontend"

# --- 1. NGINX.CONF (O Segredo da Comunicação Interna) ---
# Este arquivo diz: "Se alguém pedir /api, não mande para a internet.
# Mande para o servidor 'backend-service' que está aqui do meu lado no cluster."
nginx_conf = """
server {
    listen 80;

    # Rota 1: O Site (React)
    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
        try_files $uri $uri/ /index.html;
    }

    # Rota 2: A API (Proxy Reverso para o Django)
    location /api/ {
        # O Nginx resolve esse nome usando o DNS interno do Kubernetes
        proxy_pass http://backend-service.estudos.svc.cluster.local:8000;
        
        # Cabeçalhos para o Django não se perder
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
"""

# --- 2. APP.JSX (Frontend Limpo) ---
# Note que agora a API_URL não tem 'http' nem 'localhost'.
# É apenas um caminho relativo. O Nginx assume o controle.
app_jsx = """
import React, { useState, useEffect } from 'react';

function App() {
  const [questoes, setQuestoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState(null);

  // CONFIGURAÇÃO DE PROXY: Caminho relativo
  const API_URL = "/api/questoes/";

  useEffect(() => {
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error('Erro na comunicação com o servidor (Status: ' + response.status + ')');
        }
        return response.json();
      })
      .then(data => {
        setQuestoes(data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Erro:", error);
        setErro("Falha ao carregar questões. O Proxy interno pode estar indisponível.");
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <header style={{ textAlign: 'center', marginBottom: '40px', borderBottom: '2px solid #eee', paddingBottom: '20px' }}>
        <h1 style={{ color: '#2c3e50' }}>🎓 Banco de Questões</h1>
        <p style={{ color: '#16a085', fontWeight: 'bold' }}>Modo: Comunicação Interna (K8s)</p>
      </header>

      <main>
        {loading && <p style={{ textAlign: 'center', color: '#7f8c8d' }}>Conectando ao Backend via túnel seguro...</p>}
        
        {erro && (
          <div style={{ backgroundColor: '#ffebee', color: '#c62828', padding: '15px', borderRadius: '5px', border: '1px solid #ef9a9a' }}>
            <strong>Erro:</strong> {erro}
          </div>
        )}

        {!loading && !erro && questionsList(questoes)}
      </main>
    </div>
  );
}

function questionsList(questoes) {
  if (questoes.length === 0) {
    return <p style={{ textAlign: 'center', color: '#999' }}>Nenhuma questão encontrada no banco de dados.</p>;
  }

  return (
    <div style={{ display: 'grid', gap: '20px' }}>
      {questoes.map(q => (
        <div key={q.id} style={{ 
            border: '1px solid #e0e0e0', 
            borderRadius: '8px', 
            padding: '20px',
            backgroundColor: '#fff',
            boxShadow: '0 4px 6px rgba(0,0,0,0.05)',
            transition: 'transform 0.2s'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
             <span style={{ background: '#e3f2fd', color: '#1976d2', padding: '4px 8px', borderRadius: '4px', fontSize: '0.8em', fontWeight: 'bold' }}>
               {q.topico_nome || 'Geral'}
             </span>
             <span style={{ 
               color: q.dificuldade === 'F' ? '#2e7d32' : q.dificuldade === 'M' ? '#f57c00' : '#c62828',
               fontWeight: 'bold', fontSize: '0.8em' 
             }}>
               {q.dificuldade === 'F' ? 'Fácil' : q.dificuldade === 'M' ? 'Médio' : 'Difícil'}
             </span>
          </div>
          
          <h3 style={{ margin: '0 0 15px 0', color: '#37474f' }}>{q.enunciado}</h3>
          
          <div style={{ display: 'grid', gap: '8px', marginBottom: '15px' }}>
             {['a', 'b', 'c', 'd'].map(opt => (
               <div key={opt} style={{ display: 'flex', gap: '10px', padding: '8px', background: '#f5f5f5', borderRadius: '4px' }}>
                 <strong>{opt.toUpperCase()})</strong> {q[`alternativa_${opt}`]}
               </div>
             ))}
          </div>

          <details style={{ borderTop: '1px solid #eee', paddingTop: '10px', color: '#546e7a', cursor: 'pointer' }}>
             <summary style={{fontWeight: 'bold'}}>Ver Gabarito</summary>
             <div style={{ marginTop: '10px', padding: '10px', background: '#f1f8e9', borderRadius: '4px' }}>
               <p><strong>Resposta Correta:</strong> {q.correta}</p>
               <p>{q.justificativa}</p>
             </div>
          </details>
        </div>
      ))}
    </div>
  );
}

export default App;
"""

files = {
    f"{root_front}/nginx.conf": nginx_conf,
    f"{root_front}/src/App.jsx": app_jsx,
}

print("🚀 Gerando arquivos para Comunicação Interna (Nginx + React)...")
for path, content in files.items():
    create_file(path, content)
print("✨ Sucesso! Siga os passos de Build v4.")
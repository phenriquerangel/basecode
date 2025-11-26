import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Corrigido: {path}")

root_front = "basecode/frontend/src"

# MAIN.JSX (Corrigido)
# Antes: Mostrava HTML fixo.
# Agora: Importa e renderiza o componente <App />
main_jsx = """
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'  // <--- Importa o nosso código novo

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />  {/* <--- Renderiza o App em vez de texto fixo */}
  </React.StrictMode>,
)
"""

files = {
    f"{root_front}/main.jsx": main_jsx,
}

print("🚀 Conectando main.jsx ao App.jsx...")
for path, content in files.items():
    create_file(path, content)
print("✨ Feito! Agora o React vai carregar a aplicação correta.")
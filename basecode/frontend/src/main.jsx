import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'  // <--- Importa o nosso código novo

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />  {/* <--- Renderiza o App em vez de texto fixo */}
  </React.StrictMode>,
)
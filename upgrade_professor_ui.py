import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Atualizado: {path}")

root = "basecode"

# ==========================================
# 1. BACKEND (Adicionar Poder de Busca)
# ==========================================

# Adicionamos 'django-filter' para filtragem profissional
be_requirements = """
Django>=5.0,<6.0
djangorestframework>=3.14
psycopg2-binary>=2.9
django-cors-headers>=4.3
gunicorn>=21.2
django-jazzmin>=2.6.0
whitenoise>=6.6.0
weasyprint>=61.0
django-filter>=23.0
"""

# Views atualizadas com SearchFilter e DjangoFilterBackend
be_views = """
from rest_framework import viewsets, views, filters
from rest_framework.response import Response
from django.http import HttpResponse
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from weasyprint import HTML
from .models import Topico, Questao
from .serializers import TopicoSerializer, QuestaoSerializer

class TopicoViewSet(viewsets.ModelViewSet):
    queryset = Topico.objects.all()
    serializer_class = TopicoSerializer

class QuestaoViewSet(viewsets.ModelViewSet):
    queryset = Questao.objects.all().order_by('-id')
    serializer_class = QuestaoSerializer
    
    # Habilita Busca e Filtros
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    
    # Filtro exato: ?topico=1&dificuldade=F
    filterset_fields = ['topico', 'dificuldade']
    
    # Busca textual: ?search=pitagoras (busca no enunciado e justificativa)
    search_fields = ['enunciado', 'justificativa']

class GerarPDFView(views.APIView):
    def post(self, request):
        ids = request.data.get('ids', [])
        questoes = Questao.objects.filter(id__in=ids)
        if not questoes: return Response({"erro": "Vazio"}, status=400)
        
        html_string = render_to_string('questoes/prova.html', {'questoes': questoes})
        pdf_file = HTML(string=html_string).write_pdf()
        
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="prova.pdf"'
        return response
"""

# Settings (Adicionar django_filters)
be_settings = """
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_filters', # <--- NOVO
    'questoes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', 'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'core.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'banco_questoes'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'sua_senha_local'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}]
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
JAZZMIN_SETTINGS = {"site_title": "Banco de Questões", "site_header": "Admin", "site_brand": "MathMaster", "show_ui_builder": False}
JAZZMIN_UI_TWEAKS = {"theme": "flatly", "dark_mode_theme": "darkly"}
"""

# ==========================================
# 2. FRONTEND (Dashboard do Professor)
# ==========================================

# App.jsx: Agora com Barra de Busca, Layout Largo e Visualização Completa
fe_app = """
import React, { useState, useEffect } from 'react';

function App() {
  const [questoes, setQuestoes] = useState([]);
  const [topicos, setTopicos] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);

  // Filtros
  const [busca, setBusca] = useState("");
  const [filtroTopico, setFiltroTopico] = useState("");
  const [filtroDificuldade, setFiltroDificuldade] = useState("");

  const API_URL = "/api/questoes/";
  const TOPICOS_URL = "/api/topicos/";
  const PDF_URL = "/api/gerar-pdf/";

  // Carrega Tópicos (para o filtro) e Questões
  useEffect(() => {
    fetch(TOPICOS_URL).then(r=>r.json()).then(setTopicos).catch(console.error);
    fetchData();
  }, []);

  // Função de busca que chama o Backend
  const fetchData = () => {
    setLoading(true);
    let url = `${API_URL}?search=${busca}`;
    if (filtroTopico) url += `&topico=${filtroTopico}`;
    if (filtroDificuldade) url += `&dificuldade=${filtroDificuldade}`;

    fetch(url)
      .then(r => r.json())
      .then(d => { setQuestoes(d); setLoading(false); })
      .catch(e => { console.error(e); setLoading(false); });
  };

  // Debounce da busca (para não chamar API a cada letra)
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      fetchData();
    }, 500);
    return () => clearTimeout(delayDebounceFn);
  }, [busca, filtroTopico, filtroDificuldade]);

  const toggleSelect = (id) => {
    selectedIds.includes(id) ? setSelectedIds(selectedIds.filter(i=>i!==id)) : setSelectedIds([...selectedIds, id]);
  };

  const handleDownload = async () => {
    setDownloading(true);
    try {
        const response = await fetch(PDF_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ids: selectedIds })
        });
        if (!response.ok) throw new Error("Erro ao gerar PDF");
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "Prova_MathMaster.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
    } catch (err) { alert(err.message); } finally { setDownloading(false); }
  };

  // --- STYLES (Layout de Dashboard) ---
  const s = {
    page: { fontFamily: 'Inter, sans-serif', backgroundColor: '#f3f4f6', minHeight: '100vh', paddingBottom: '80px' },
    nav: { backgroundColor: 'white', padding: '15px 40px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', display:'flex', justifyContent:'space-between', alignItems:'center', position:'sticky', top:0, zIndex:10 },
    brand: { fontSize: '1.5rem', fontWeight: '800', color: '#111827', margin:0 },
    
    filtersBar: { maxWidth: '1200px', margin: '30px auto', display: 'flex', gap: '15px', padding: '0 20px', flexWrap: 'wrap' },
    input: { flex: 1, padding: '12px', borderRadius: '8px', border: '1px solid #d1d5db', fontSize: '1rem' },
    select: { padding: '12px', borderRadius: '8px', border: '1px solid #d1d5db', fontSize: '1rem', minWidth: '150px' },

    grid: { maxWidth: '1200px', margin: '0 auto', display: 'grid', gap: '20px', padding: '0 20px' },
    
    // O Cartão da Questão (Expandido)
    card: (sel) => ({
      backgroundColor: 'white', 
      border: sel ? '2px solid #2563eb' : '1px solid #e5e7eb',
      borderRadius: '12px', 
      padding: '25px', 
      position: 'relative',
      boxShadow: sel ? '0 10px 15px -3px rgba(37, 99, 235, 0.2)' : '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      transition: 'all 0.2s',
      cursor: 'pointer'
    }),
    
    cardHeader: { display: 'flex', justifyContent: 'space-between', marginBottom: '15px', alignItems: 'center' },
    badges: { display: 'flex', gap: '10px' },
    badge: (bg, col) => ({ backgroundColor: bg, color: col, padding: '4px 10px', borderRadius: '99px', fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase' }),
    
    enunciado: { fontSize: '1.15rem', color: '#1f2937', lineHeight: '1.6', marginBottom: '20px', whiteSpace: 'pre-wrap' },
    
    alternativas: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '20px' },
    altItem: { padding: '8px 12px', backgroundColor: '#f9fafb', borderRadius: '6px', fontSize: '0.9rem', color: '#4b5563', border: '1px solid #f3f4f6' },
    
    footer: { borderTop: '1px solid #f3f4f6', paddingTop: '15px', fontSize: '0.9rem' },
    
    // Barra Flutuante Inferior
    actionBar: {
      position: 'fixed', bottom: '30px', left: '50%', transform: 'translateX(-50%)',
      backgroundColor: '#1f2937', color: 'white', padding: '15px 40px',
      borderRadius: '50px', display: 'flex', alignItems: 'center', gap: '20px',
      boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.2)', zIndex: 50
    },
    btnDownload: {
      backgroundColor: '#3b82f6', color: 'white', border: 'none', padding: '10px 20px',
      borderRadius: '8px', fontWeight: 'bold', cursor: 'pointer', fontSize: '1rem'
    }
  };

  return (
    <div style={s.page}>
      <nav style={s.nav}>
        <h1 style={s.brand}>🎓 MathMaster <span style={{fontSize:'0.8rem', color:'#6b7280', fontWeight:'normal'}}>Painel do Professor</span></h1>
        <div>{selectedIds.length} selecionadas</div>
      </nav>

      {/* BARRA DE FILTROS E BUSCA */}
      <div style={s.filtersBar}>
        <input 
          style={s.input} 
          placeholder="🔎 Pesquisar enunciado (ex: triângulo)..." 
          value={busca} onChange={e => setBusca(e.target.value)}
        />
        
        <select style={s.select} value={filtroTopico} onChange={e => setFiltroTopico(e.target.value)}>
          <option value="">Todos os Tópicos</option>
          {topicos.map(t => <option key={t.id} value={t.id}>{t.nome}</option>)}
        </select>

        <select style={s.select} value={filtroDificuldade} onChange={e => setFiltroDificuldade(e.target.value)}>
          <option value="">Todas Dificuldades</option>
          <option value="F">Fácil</option>
          <option value="M">Médio</option>
          <option value="D">Difícil</option>
        </select>
      </div>

      <main style={s.grid}>
        {loading && <p style={{textAlign:'center'}}>Carregando banco de dados...</p>}
        
        {!loading && questionsList(questoes, selectedIds, toggleSelect, s)}
      </main>

      {selectedIds.length > 0 && (
        <div style={s.actionBar}>
          <span><strong>{selectedIds.length}</strong> questões na lista</span>
          <button style={s.btnDownload} onClick={handleDownload} disabled={downloading}>
            {downloading ? 'Gerando PDF...' : '📥 Baixar Prova'}
          </button>
        </div>
      )}
    </div>
  );
}

function questionsList(questoes, selectedIds, toggleSelect, s) {
  if (questoes.length === 0) return <p style={{textAlign:'center', color:'#6b7280'}}>Nenhuma questão encontrada.</p>;

  return questoes.map(q => {
    const isSel = selectedIds.includes(q.id);
    return (
      <div key={q.id} style={s.card(isSel)} onClick={() => toggleSelect(q.id)}>
        <div style={s.cardHeader}>
          <div style={s.badges}>
            <span style={s.badge('#eff6ff', '#2563eb')}>{q.topico_nome}</span>
            <span style={s.badge(q.dificuldade==='F'?'#ecfdf5':q.dificuldade==='M'?'#fff7ed':'#fef2f2', q.dificuldade==='F'?'#059669':q.dificuldade==='M'?'#d97706':'#dc2626')}>
              {q.dificuldade === 'F' ? 'Fácil' : q.dificuldade === 'M' ? 'Médio' : 'Difícil'}
            </span>
          </div>
          <div style={{
              width:'24px', height:'24px', borderRadius:'50%', 
              border: isSel ? '6px solid #2563eb' : '2px solid #d1d5db',
              transition: 'all 0.2s'
          }}></div>
        </div>

        <div style={s.enunciado}>{q.enunciado}</div>

        <div style={s.alternativas}>
          <div style={s.altItem}>A) {q.alternativa_a}</div>
          <div style={s.altItem}>B) {q.alternativa_b}</div>
          <div style={s.altItem}>C) {q.alternativa_c}</div>
          <div style={s.altItem}>D) {q.alternativa_d}</div>
        </div>

        <details onClick={(e) => e.stopPropagation()} style={{color: '#6b7280', fontSize:'0.9rem'}}>
          <summary style={{cursor:'pointer', fontWeight:'600'}}>Ver Gabarito</summary>
          <div style={{marginTop:'10px', padding:'10px', background:'#f3f4f6', borderRadius:'8px'}}>
            <strong>Resposta: {q.correta}</strong><br/>
            {q.justificativa}
          </div>
        </details>
      </div>
    );
  });
}

export default App;
"""

files = {
    f"{root}/backend/requirements.txt": be_requirements,
    f"{root}/backend/core/settings.py": be_settings,
    f"{root}/backend/questoes/views.py": be_views,
    f"{root}/frontend/src/App.jsx": fe_app,
}

print("👨‍🏫 Criando Painel do Professor (Busca + Filtros + Layout Expandido)...")
for path, content in files.items():
    create_file(path, content)
print("✨ Arquivos criados! Necessário Build do Backend (libs novas) e Frontend.")
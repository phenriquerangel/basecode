import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Restaurado: {path}")

root = "basecode"

print("↺ REVERTENDO PARA A VERSÃO ESTÁVEL (COM JAZZMIN + PDF SIMPLES)...")

# ==========================================
# 1. BACKEND (Versão Leve - Sem WeasyPrint)
# ==========================================

be_req = """
Django>=5.0,<6.0
djangorestframework>=3.14
psycopg2-binary>=2.9
django-cors-headers>=4.3
gunicorn>=21.2
django-jazzmin>=2.6.0
whitenoise>=6.6.0
"""

# Dockerfile simples (Sem bibliotecas gráficas do Linux)
be_docker = """
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
"""

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
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates','DIRS': [],'APP_DIRS': True,'OPTIONS': {'context_processors': ['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages',],},},]
WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
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

JAZZMIN_SETTINGS = {
    "site_title": "Banco de Questões",
    "site_header": "Admin",
    "site_brand": "MathMaster",
    "show_ui_builder": False,
}
JAZZMIN_UI_TWEAKS = {"theme": "flatly", "dark_mode_theme": "darkly"}
"""

# Views: Removemos a View de PDF complexa
be_views = """
from rest_framework import viewsets
from .models import Topico, Questao
from .serializers import TopicoSerializer, QuestaoSerializer

class TopicoViewSet(viewsets.ModelViewSet):
    queryset = Topico.objects.all()
    serializer_class = TopicoSerializer

class QuestaoViewSet(viewsets.ModelViewSet):
    queryset = Questao.objects.all().order_by('-id')
    serializer_class = QuestaoSerializer
    
    def get_queryset(self):
        qs = Questao.objects.all().order_by('-id')
        topico_id = self.request.query_params.get('topico')
        if topico_id:
            qs = qs.filter(topico_id=topico_id)
        return qs
"""

be_urls = """
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicoViewSet, QuestaoViewSet

router = DefaultRouter()
router.register(r'topicos', TopicoViewSet)
router.register(r'questoes', QuestaoViewSet)

urlpatterns = [path('', include(router.urls))]
"""

# ==========================================
# 2. FRONTEND (Versão com jsPDF no Navegador)
# ==========================================

fe_pkg = """
{
  "name": "front", "private": true, "version": "1.0.0", "type": "module",
  "scripts": { "dev": "vite", "build": "vite build" },
  "dependencies": { "react": "^18.2.0", "react-dom": "^18.2.0", "jspdf": "^2.5.1" },
  "devDependencies": { "@vitejs/plugin-react": "^4.2.1", "vite": "^5.2.0" }
}
"""

fe_app = """
import React, { useState, useEffect } from 'react';
import { jsPDF } from "jspdf";

function App() {
  const [questoes, setQuestoes] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const API_URL = "/api/questoes/";

  useEffect(() => {
    fetch(API_URL).then(r=>r.json()).then(d=>{setQuestoes(d);setLoading(false);})
    .catch(e=>{console.error(e);setLoading(false);});
  }, []);

  const toggleSelect = (id) => {
    selectedIds.includes(id) ? setSelectedIds(selectedIds.filter(i=>i!==id)) : setSelectedIds([...selectedIds, id]);
  };

  // GERAÇÃO DE PDF NO NAVEGADOR (Simples e Funcional)
  const generatePDF = () => {
    const doc = new jsPDF();
    const selecionadas = questoes.filter(q => selectedIds.includes(q.id));
    let y = 20;
    doc.setFontSize(16); doc.text("Prova MathMaster", 105, y, {align:'center'}); y+=20;
    doc.setFontSize(12);
    selecionadas.forEach((q, i) => {
        if(y>270){doc.addPage();y=20;}
        const lines = doc.splitTextToSize(`${i+1}) ${q.enunciado}`, 180);
        doc.text(lines, 10, y);
        y += (lines.length*7) + 5;
        ['a','b','c','d'].forEach(opt => {
            doc.text(`${opt.toUpperCase()}) ${q['alternativa_'+opt]}`, 15, y); y+=6;
        });
        y+=10;
    });
    doc.save("prova.pdf");
  };

  // Design Moderno
  const s = {
    page: { fontFamily: 'Inter, sans-serif', backgroundColor: '#f3f4f6', minHeight: '100vh', padding: '40px 20px' },
    header: { textAlign: 'center', marginBottom: '40px' },
    grid: { maxWidth: '900px', margin: '0 auto', display: 'grid', gap: '20px' },
    card: (sel) => ({
      backgroundColor: 'white', borderRadius: '12px', padding: '24px', 
      border: sel ? '2px solid #2563eb' : '1px solid #e5e7eb',
      boxShadow: '0 2px 4px rgba(0,0,0,0.05)', cursor: 'pointer'
    }),
    badge: { background: '#eff6ff', color: '#2563eb', padding: '4px 8px', borderRadius: '99px', fontSize: '0.75rem', fontWeight:'bold' },
    btn: { position:'fixed', bottom:'30px', right:'30px', padding:'15px 30px', background:'#2563eb', color:'white', borderRadius:'50px', border:'none', cursor:'pointer', fontWeight:'bold', boxShadow:'0 10px 15px -3px rgba(37, 99, 235, 0.3)' }
  };

  return (
    <div style={s.page}>
      <header style={s.header}>
        <h1 style={{fontSize:'2.5rem', color:'#1f2937', margin:0}}>🎓 MathMaster</h1>
        <p style={{color:'#6b7280'}}>Selecione as questões para o PDF</p>
      </header>

      <main style={s.grid}>
        {loading && <p style={{textAlign:'center'}}>Carregando...</p>}
        {!loading && questoes.map(q => {
           const isSel = selectedIds.includes(q.id);
           return (
             <div key={q.id} style={s.card(isSel)} onClick={() => toggleSelect(q.id)}>
               <div style={{marginBottom:'10px'}}><span style={s.badge}>{q.topico_nome}</span></div>
               <h3 style={{margin:'0 0 10px 0', color:'#374151'}}>{q.enunciado}</h3>
               <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'5px', fontSize:'0.9rem', color:'#6b7280'}}>
                 <div>A) {q.alternativa_a}</div><div>B) {q.alternativa_b}</div>
                 <div>C) {q.alternativa_c}</div><div>D) {q.alternativa_d}</div>
               </div>
             </div>
           )
        })}
      </main>

      {selectedIds.length > 0 && (
        <button style={s.btn} onClick={generatePDF}>📥 Baixar PDF ({selectedIds.length})</button>
      )}
    </div>
  );
}
export default App;
"""

files = {
    f"{root}/backend/requirements.txt": be_req,
    f"{root}/backend/Dockerfile": be_docker,
    f"{root}/backend/core/settings.py": be_settings,
    f"{root}/backend/questoes/views.py": be_views,
    f"{root}/backend/questoes/urls.py": be_urls,
    f"{root}/frontend/package.json": fe_pkg,
    f"{root}/frontend/src/App.jsx": fe_app,
}

for p, c in files.items(): create_file(p, c)

print("\n✨ CÓDIGO RESTAURADO PARA 'v21' (Backend Leve + Frontend com jsPDF)")
print("Agora faça o build das imagens v21.")
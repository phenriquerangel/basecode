import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Atualizado: {path}")

root = "basecode"

# ==========================================
# 1. BACKEND (Instalação e Configuração)
# ==========================================

# Adicionamos 'weasyprint'
be_requirements = """
Django>=5.0,<6.0
djangorestframework>=3.14
psycopg2-binary>=2.9
django-cors-headers>=4.3
gunicorn>=21.2
django-jazzmin>=2.6.0
whitenoise>=6.6.0
weasyprint>=61.0
"""

# Dockerfile: Precisamos instalar bibliotecas gráficas do Linux (Pango/Cairo)
# para que o WeasyPrint consiga desenhar o PDF.
be_dockerfile = """
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instala dependências do sistema para PostgreSQL E WeasyPrint (PDF)
RUN apt-get update && apt-get install -y \\
    gcc \\
    libpq-dev \\
    libpango-1.0-0 \\
    libpangoft2-1.0-0 \\
    libharfbuzz-subset0 \\
    libjpeg-dev \\
    libopenjp2-7-dev \\
    libxcb1 \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Coleta estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
"""

# Settings: Precisamos dizer ao Django onde ficam os Templates HTML do PDF
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # <--- Pasta de templates habilitada
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
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

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

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
    "site_header": "Administração",
    "site_brand": "MathMaster",
    "welcome_sign": "Admin",
    "copyright": "Codebase",
    "search_model": "questoes.Questao",
    "show_ui_builder": False,
}
JAZZMIN_UI_TWEAKS = {"theme": "flatly", "dark_mode_theme": "darkly"}
"""

# ==========================================
# 2. LOGICA DE GERAÇÃO (Views e HTML)
# ==========================================

# O Template HTML que vai virar PDF (Design bonito da prova)
pdf_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Lista de Exercícios</title>
    <style>
        @page { size: A4; margin: 2cm; }
        body { font-family: 'Helvetica', sans-serif; color: #333; }
        header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 30px; }
        h1 { margin: 0; font-size: 24px; }
        p.subtitle { color: #666; margin-top: 5px; }
        
        .questao { margin-bottom: 25px; page-break-inside: avoid; }
        .enunciado { font-weight: bold; margin-bottom: 10px; font-size: 14px; }
        .topico { font-size: 10px; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
        
        .alternativas { list-style-type: none; padding-left: 10px; }
        .alternativas li { margin-bottom: 5px; font-size: 13px; }
        
        .gabarito-section { page-break-before: always; }
        table.gabarito { width: 100%; border-collapse: collapse; margin-top: 20px; }
        table.gabarito th, table.gabarito td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        table.gabarito th { background-color: #f4f4f4; }
    </style>
</head>
<body>
    <header>
        <h1>MathMaster</h1>
        <p class="subtitle">Lista de Exercícios Gerada Automaticamente</p>
    </header>

    {% for q in questoes %}
    <div class="questao">
        <div class="topico">{{ q.topico.nome }} ({{ q.get_dificuldade_display }})</div>
        <div class="enunciado">{{ forloop.counter }}) {{ q.enunciado }}</div>
        <ul class="alternativas">
            <li>a) {{ q.alternativa_a }}</li>
            <li>b) {{ q.alternativa_b }}</li>
            <li>c) {{ q.alternativa_c }}</li>
            <li>d) {{ q.alternativa_d }}</li>
        </ul>
    </div>
    {% empty %}
        <p>Nenhuma questão selecionada.</p>
    {% endfor %}

    <div class="gabarito-section">
        <header>
            <h1>Gabarito e Resoluções</h1>
        </header>
        <table class="gabarito">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Resp.</th>
                    <th>Justificativa</th>
                </tr>
            </thead>
            <tbody>
                {% for q in questoes %}
                <tr>
                    <td>{{ forloop.counter }}</td>
                    <td><strong>{{ q.correta }}</strong></td>
                    <td>{{ q.justificativa }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

# View do Django que recebe IDs e gera o PDF
be_views = """
from rest_framework import viewsets, views
from rest_framework.response import Response
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Topico, Questao
from .serializers import TopicoSerializer, QuestaoSerializer

class TopicoViewSet(viewsets.ModelViewSet):
    queryset = Topico.objects.all()
    serializer_class = TopicoSerializer

class QuestaoViewSet(viewsets.ModelViewSet):
    queryset = Questao.objects.all()
    serializer_class = QuestaoSerializer
    def get_queryset(self):
        qs = Questao.objects.all()
        topico_id = self.request.query_params.get('topico')
        if topico_id: qs = qs.filter(topico_id=topico_id)
        return qs

class GerarPDFView(views.APIView):
    def post(self, request):
        ids = request.data.get('ids', [])
        questoes = Questao.objects.filter(id__in=ids)
        
        if not questoes:
            return Response({"erro": "Nenhuma questão encontrada"}, status=400)

        # 1. Renderiza HTML com os dados
        html_string = render_to_string('questoes/prova.html', {'questoes': questoes})
        
        # 2. Converte HTML para PDF
        pdf_file = HTML(string=html_string).write_pdf()
        
        # 3. Retorna o arquivo binário
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="prova_mathmaster.pdf"'
        return response
"""

be_urls = """
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicoViewSet, QuestaoViewSet, GerarPDFView

router = DefaultRouter()
router.register(r'topicos', TopicoViewSet)
router.register(r'questoes', QuestaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('gerar-pdf/', GerarPDFView.as_view(), name='gerar-pdf'), # Nova rota
]
"""

# ==========================================
# 3. FRONTEND (Consumir a nova API)
# ==========================================

# O App.jsx agora manda os IDs para o backend e recebe o BLOB
fe_app = """
import React, { useState, useEffect } from 'react';

function App() {
  const [questoes, setQuestoes] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);
  const API_URL = "/api/questoes/";
  const PDF_URL = "/api/gerar-pdf/";

  useEffect(() => {
    fetch(API_URL).then(r=>r.json()).then(d=>{setQuestoes(d);setLoading(false);});
  }, []);

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
        
        // Transforma a resposta em um arquivo baixável (Blob)
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "Lista_Exercicios.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
    } catch (err) {
        alert("Erro: " + err.message);
    } finally {
        setDownloading(false);
    }
  };

  // Styles (Mantendo o design bonito anterior)
  const styles = {
    container: { maxWidth: '900px', margin: '0 auto', padding: '40px 20px', paddingBottom: '100px' },
    header: { textAlign: 'center', marginBottom: '50px' },
    card: (sel) => ({
      backgroundColor: sel ? '#f0fdf4' : 'white',
      border: sel ? '2px solid #16a34a' : '1px solid #f3f4f6',
      borderRadius: '16px', padding: '24px', marginBottom: '20px', cursor: 'pointer',
      boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)', position: 'relative'
    }),
    floatBtn: {
      position: 'fixed', bottom: '30px', right: '30px',
      backgroundColor: downloading ? '#9ca3af' : '#2563eb',
      color: 'white', padding: '15px 30px', borderRadius: '50px',
      border: 'none', fontWeight: 'bold', cursor: downloading ? 'wait' : 'pointer',
      boxShadow: '0 10px 15px -3px rgba(37, 99, 235, 0.3)'
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={{fontSize: '2.5rem', color: '#1f2937'}}>🎓 MathMaster</h1>
        <p style={{color: '#6b7280'}}>Selecione para gerar PDF Profissional</p>
      </header>

      <main>
        {questoes.map(q => {
           const isSel = selectedIds.includes(q.id);
           return (
             <div key={q.id} style={styles.card(isSel)} onClick={() => toggleSelect(q.id)}>
               <div style={{display:'flex', justifyContent:'space-between', marginBottom:'10px'}}>
                 <span style={{background:'#eff6ff', color:'#2563eb', padding:'4px 8px', borderRadius:'12px', fontSize:'0.8rem', fontWeight:'bold'}}>{q.topico_nome}</span>
                 {isSel && <span style={{color:'#16a34a', fontWeight:'bold'}}>✓ SELECIONADO</span>}
               </div>
               <h3 style={{marginTop:0}}>{q.enunciado}</h3>
               <div style={{color:'#666', fontSize:'0.9rem'}}>A) {q.alternativa_a} ...</div>
             </div>
           )
        })}
      </main>

      {selectedIds.length > 0 && (
        <button style={styles.floatBtn} onClick={handleDownload} disabled={downloading}>
          {downloading ? 'Gerando PDF no Servidor...' : `📥 Baixar PDF (${selectedIds.length})`}
        </button>
      )}
    </div>
  );
}
export default App;
"""

files = {
    f"{root}/backend/requirements.txt": be_requirements,
    f"{root}/backend/Dockerfile": be_dockerfile,
    f"{root}/backend/core/settings.py": be_settings,
    f"{root}/backend/questoes/views.py": be_views,
    f"{root}/backend/questoes/urls.py": be_urls,
    f"{root}/backend/templates/questoes/prova.html": pdf_template,
    f"{root}/frontend/src/App.jsx": fe_app,
}

print("📄 Migrando geração de PDF para o Backend (WeasyPrint)...")
for path, content in files.items():
    create_file(path, content)
print("✨ Arquivos prontos! Agora os Builds são obrigatórios (Novas libs de sistema).")
import os
import time
import subprocess

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Criado: {path}")

def run_cmd(cmd):
    print(f"Executando: {cmd}")
    os.system(cmd)

root = "basecode"

print("🏗️ INICIANDO RECONSTRUÇÃO (Versão Estável v13)...")

# ==========================================
# 1. CONTEÚDO DOS ARQUIVOS
# ==========================================

# KUBERNETES
k8s_ns = "apiVersion: v1\nkind: Namespace\nmetadata:\n  name: estudos"
k8s_secret = """apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: estudos
type: Opaque
stringData:
  DB_NAME: "banco_questoes"
  DB_USER: "usuario_questoes"
  DB_PASSWORD: "senha_forte"
  DB_HOST: "postgres-db"
  SECRET_KEY: "django-insecure-key"
  DEBUG: "True"
"""
k8s_db = """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: estudos
spec:
  accessModes: ["ReadWriteOnce"]
  resources:
    requests:
      storage: 1Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: estudos
spec:
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports: [{containerPort: 5432}]
        env:
        - name: POSTGRES_DB
          valueFrom: {secretKeyRef: {name: app-secrets, key: DB_NAME}}
        - name: POSTGRES_USER
          valueFrom: {secretKeyRef: {name: app-secrets, key: DB_USER}}
        - name: POSTGRES_PASSWORD
          valueFrom: {secretKeyRef: {name: app-secrets, key: DB_PASSWORD}}
        volumeMounts:
        - mountPath: /var/lib/postgresql/data
          name: pg-data
      volumes:
      - name: pg-data
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-db
  namespace: estudos
spec:
  ports: [{port: 5432}]
  selector:
    app: postgres
  type: ClusterIP
"""

# BACKEND APONTANDO PARA V13
k8s_back = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: estudos
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        # <--- CORRIGIDO PARA V13 AQUI
        image: phenriquernagel/banco-questoes-backend:v13
        imagePullPolicy: Always
        ports: [{containerPort: 8000}]
        envFrom:
        - secretRef:
            name: app-secrets
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: estudos
spec:
  selector:
    app: backend
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
  type: ClusterIP
"""

# FRONTEND APONTANDO PARA V10 (Painel Professor)
k8s_front = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: estudos
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: phenriquernagel/banco-questoes-frontend:v10
        imagePullPolicy: Always
        ports: [{containerPort: 80}]
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: estudos
spec:
  selector:
    app: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort
"""

# ARQUIVOS DO CÓDIGO FONTE (Mantendo o mais recente para você poder buildar no futuro)
be_req = """Django>=5.0,<6.0
djangorestframework>=3.14
psycopg2-binary>=2.9
django-cors-headers>=4.3
gunicorn>=21.2
django-jazzmin>=2.6.0
whitenoise>=6.6.0
weasyprint>=61.0
django-filter>=23.0"""

be_docker = """FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update && apt-get install -y gcc libpq-dev libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 libjpeg-dev libopenjp2-7-dev libxcb1 fontconfig fonts-liberation && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "--workers", "3", "--timeout", "120", "--bind", "0.0.0.0:8000", "core.wsgi:application"]"""

be_settings = """import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = ['jazzmin','django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','rest_framework','corsheaders','django_filters','questoes']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware','corsheaders.middleware.CorsMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'core.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates','DIRS': [os.path.join(BASE_DIR, 'templates')],'APP_DIRS': True,'OPTIONS': {'context_processors': ['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages',],},},]
WSGI_APPLICATION = 'core.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql','NAME': os.environ.get('DB_NAME'),'USER': os.environ.get('DB_USER'),'PASSWORD': os.environ.get('DB_PASSWORD'),'HOST': os.environ.get('DB_HOST'),'PORT': '5432',}}
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
JAZZMIN_UI_TWEAKS = {"theme": "flatly", "dark_mode_theme": "darkly"}"""

be_urls = """from django.contrib import admin
from django.urls import path, include
urlpatterns = [path('admin/', admin.site.urls),path('api/', include('questoes.urls'))]"""

q_models = """from django.db import models
class Topico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    def __str__(self): return self.nome
class Questao(models.Model):
    DIFICULDADE_CHOICES = [('F', 'Fácil'), ('M', 'Médio'), ('D', 'Difícil')]
    enunciado = models.TextField()
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, related_name='questoes')
    dificuldade = models.CharField(max_length=1, choices=DIFICULDADE_CHOICES, default='M')
    alternativa_a = models.CharField(max_length=255)
    alternativa_b = models.CharField(max_length=255)
    alternativa_c = models.CharField(max_length=255)
    alternativa_d = models.CharField(max_length=255)
    correta = models.CharField(max_length=1, choices=[('A','A'), ('B','B'), ('C','C'), ('D','D')])
    justificativa = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    class Meta: verbose_name = "Questão"; verbose_name_plural = "Questões"
    def __str__(self): return self.enunciado[:30]"""

q_views = """from rest_framework import viewsets, views, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from weasyprint import HTML
from .models import Topico, Questao
from .serializers import TopicoSerializer, QuestaoSerializer

class TopicoViewSet(viewsets.ModelViewSet):
    queryset = Topico.objects.all()
    serializer_class = TopicoSerializer
    permission_classes = [AllowAny]

class QuestaoViewSet(viewsets.ModelViewSet):
    queryset = Questao.objects.all().order_by('-id')
    serializer_class = QuestaoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['topico', 'dificuldade']
    search_fields = ['enunciado', 'justificativa']
    permission_classes = [AllowAny]

class GerarPDFView(views.APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        ids = request.data.get('ids', [])
        questoes = Questao.objects.filter(id__in=ids)
        if not questoes: return Response({"erro": "Vazio"}, status=400)
        try:
            html_string = render_to_string('questoes/prova.html', {'questoes': questoes})
            html = HTML(string=html_string, base_url=str(settings.BASE_DIR))
            pdf_file = html.write_pdf(presentational_hints=True)
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="prova.pdf"'
            return response
        except Exception as e:
            return Response({"erro": str(e)}, status=500)"""

q_urls = """from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicoViewSet, QuestaoViewSet, GerarPDFView
router = DefaultRouter()
router.register(r'topicos', TopicoViewSet)
router.register(r'questoes', QuestaoViewSet)
urlpatterns = [path('', include(router.urls)), path('gerar-pdf/', GerarPDFView.as_view())]"""

q_serial = """from rest_framework import serializers
from .models import Topico, Questao
class TopicoSerializer(serializers.ModelSerializer):
    class Meta: model = Topico; fields = '__all__'
class QuestaoSerializer(serializers.ModelSerializer):
    topico_nome = serializers.ReadOnlyField(source='topico.nome')
    class Meta: model = Questao; fields = '__all__'"""

pdf_html = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page { size: A4; margin: 2cm; }
body { font-family: Helvetica, sans-serif; }
.questao { margin-bottom: 20px; page-break-inside: avoid; }
.gabarito { page-break-before: always; }
table { width: 100%; border-collapse: collapse; }
td, th { border: 1px solid #ddd; padding: 8px; }
</style></head><body>
<h1>MathMaster - Prova</h1>
{% for q in questoes %}
<div class="questao">
  <p><strong>{{ forloop.counter }})</strong> {{ q.enunciado }}</p>
  <ul>
    <li>a) {{ q.alternativa_a }}</li><li>b) {{ q.alternativa_b }}</li>
    <li>c) {{ q.alternativa_c }}</li><li>d) {{ q.alternativa_d }}</li>
  </ul>
</div>
{% endfor %}
<div class="gabarito"><h1>Gabarito</h1>
<table><tr><th>#</th><th>Resp</th><th>Explicação</th></tr>
{% for q in questoes %}
<tr><td>{{ forloop.counter }}</td><td>{{ q.correta }}</td><td>{{ q.justificativa }}</td></tr>
{% endfor %}</table></div></body></html>"""

fe_docker = """FROM node:18-alpine as build
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]"""

fe_nginx = """server {
    listen 80;
    location / { root /usr/share/nginx/html; index index.html index.htm; try_files $uri $uri/ /index.html; }
    location /api/ { proxy_pass http://backend-service.estudos.svc.cluster.local:8000; proxy_set_header Host $host; }
}"""

fe_pkg = """{
  "name": "front", "private": true, "version": "1.0.0", "type": "module",
  "scripts": { "dev": "vite", "build": "vite build" },
  "dependencies": { "react": "^18.2.0", "react-dom": "^18.2.0" },
  "devDependencies": { "@vitejs/plugin-react": "^4.2.1", "vite": "^5.2.0" }
}"""

fe_vite = "import { defineConfig } from 'vite'; import react from '@vitejs/plugin-react'; export default defineConfig({plugins: [react()], server: {port: 3000, host: true}});"

fe_app = """import React, { useState, useEffect } from 'react';
function App() {
  const [questoes, setQuestoes] = useState([]);
  const [topicos, setTopicos] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [busca, setBusca] = useState("");
  const [filtroTopico, setFiltroTopico] = useState("");
  const [filtroDificuldade, setFiltroDificuldade] = useState("");
  const [downloading, setDownloading] = useState(false);
  
  const API_URL = "/api/questoes/";
  const TOPICOS_URL = "/api/topicos/";
  const PDF_URL = "/api/gerar-pdf/";

  useEffect(() => { fetch(TOPICOS_URL).then(r=>r.json()).then(setTopicos).catch(console.error); }, []);
  
  useEffect(() => {
    let url = `${API_URL}?search=${busca}`;
    if (filtroTopico) url += `&topico=${filtroTopico}`;
    if (filtroDificuldade) url += `&dificuldade=${filtroDificuldade}`;
    
    const timer = setTimeout(() => {
      fetch(url).then(r=>r.json()).then(setQuestoes).catch(console.error);
    }, 500);
    return () => clearTimeout(timer);
  }, [busca, filtroTopico, filtroDificuldade]);

  const handleDownload = async () => {
    setDownloading(true);
    try {
        const res = await fetch(PDF_URL, {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ ids: selectedIds })
        });
        if(res.ok) {
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a'); a.href = url; a.download = "prova.pdf"; a.click();
        } else { alert("Erro ao gerar PDF"); }
    } finally { setDownloading(false); }
  };

  const s = {
      nav: {background:'white', padding:'15px', borderBottom:'1px solid #ddd', display:'flex', justifyContent:'space-between', alignItems:'center', position:'sticky', top:0},
      filters: {padding:'20px', display:'flex', gap:'10px', flexWrap:'wrap'},
      card: (sel) => ({background:'white', padding:'20px', borderRadius:'10px', border: sel ? '2px solid #2563eb' : '1px solid #ddd', cursor:'pointer', marginBottom:'15px'}),
      btn: {position:'fixed', bottom:'30px', right:'30px', padding:'15px 30px', background:'#2563eb', color:'white', borderRadius:'50px', border:'none', cursor:'pointer', fontWeight:'bold'}
  };

  return (
    <div style={{fontFamily:'sans-serif', backgroundColor:'#f3f4f6', minHeight:'100vh', paddingBottom:'100px'}}>
      <nav style={s.nav}>
        <h1 style={{margin:0, fontSize:'1.2rem'}}>MathMaster <small style={{color:'#666'}}>Professor</small></h1>
        <div>{selectedIds.length} selecionadas</div>
      </nav>
      <div style={s.filters}>
        <input placeholder="🔎 Pesquisar..." value={busca} onChange={e=>setBusca(e.target.value)} style={{padding:'8px', flex:1}}/>
        <select value={filtroTopico} onChange={e=>setFiltroTopico(e.target.value)} style={{padding:'8px'}}>
           <option value="">Todos Tópicos</option>
           {topicos.map(t=><option key={t.id} value={t.id}>{t.nome}</option>)}
        </select>
        <select value={filtroDificuldade} onChange={e=>setFiltroDificuldade(e.target.value)} style={{padding:'8px'}}>
           <option value="">Todas Dificuldades</option>
           <option value="F">Fácil</option><option value="M">Médio</option><option value="D">Difícil</option>
        </select>
      </div>
      <div style={{maxWidth:'1000px', margin:'0 auto', padding:'0 20px'}}>
        {questoes.length===0 && <p style={{textAlign:'center', color:'#666'}}>Nenhuma questão encontrada.</p>}
        {questoes.map(q => {
           const isSel = selectedIds.includes(q.id);
           return (
             <div key={q.id} style={s.card(isSel)} onClick={() => isSel ? setSelectedIds(selectedIds.filter(i=>i!==q.id)) : setSelectedIds([...selectedIds, q.id])}>
               <div style={{display:'flex', justifyContent:'space-between', marginBottom:'10px'}}>
                  <span style={{background:'#eff6ff', color:'#2563eb', padding:'4px 8px', borderRadius:'10px', fontSize:'0.8rem', fontWeight:'bold'}}>{q.topico_nome}</span>
                  <span style={{fontSize:'0.8rem', color: q.dificuldade==='F'?'green':q.dificuldade==='M'?'orange':'red'}}>{q.dificuldade}</span>
               </div>
               <h3 style={{margin:'0 0 10px 0'}}>{q.enunciado}</h3>
               <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'5px', fontSize:'0.9rem', color:'#555'}}>
                 <div>A) {q.alternativa_a}</div><div>B) {q.alternativa_b}</div>
                 <div>C) {q.alternativa_c}</div><div>D) {q.alternativa_d}</div>
               </div>
             </div>
           )
        })}
      </div>
      {selectedIds.length > 0 && (
          <button onClick={handleDownload} style={s.btn} disabled={downloading}>
            {downloading ? 'Gerando...' : `📥 Baixar PDF (${selectedIds.length})`}
          </button>
      )}
    </div>
  );
}
export default App;"""

fe_main = "import React from 'react'; import ReactDOM from 'react-dom/client'; import App from './App.jsx'; ReactDOM.createRoot(document.getElementById('root')).render(<App />);"
fe_html = '<!doctype html><html lang="pt-br"><head><meta charset="UTF-8"/><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet"><style>body{font-family:Inter,sans-serif;margin:0}</style><title>MathMaster</title></head><body><div id="root"></div><script type="module" src="/src/main.jsx"></script></body></html>'

# ==========================================
# 2. GERAR ARQUIVOS
# ==========================================

files = {
    f"{root}/k8s/00-namespace.yaml": k8s_ns,
    f"{root}/k8s/01-secrets.yaml": k8s_secret,
    f"{root}/k8s/02-database.yaml": k8s_db,
    f"{root}/k8s/03-backend.yaml": k8s_back,
    f"{root}/k8s/04-frontend.yaml": k8s_front,
    f"{root}/backend/Dockerfile": be_docker,
    f"{root}/backend/requirements.txt": be_req,
    f"{root}/backend/core/settings.py": be_settings,
    f"{root}/backend/core/urls.py": be_urls,
    f"{root}/backend/core/__init__.py": "",
    f"{root}/backend/core/wsgi.py": "import os; from django.core.wsgi import get_wsgi_application; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings'); application = get_wsgi_application()",
    f"{root}/backend/manage.py": "import os; import sys; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings'); from django.core.management import execute_from_command_line; execute_from_command_line(sys.argv)",
    f"{root}/backend/questoes/__init__.py": "",
    f"{root}/backend/questoes/models.py": q_models,
    f"{root}/backend/questoes/views.py": q_views,
    f"{root}/backend/questoes/urls.py": q_urls,
    f"{root}/backend/questoes/serializers.py": q_serial,
    f"{root}/backend/templates/questoes/prova.html": pdf_html,
    f"{root}/frontend/Dockerfile": fe_docker,
    f"{root}/frontend/nginx.conf": fe_nginx,
    f"{root}/frontend/package.json": fe_pkg,
    f"{root}/frontend/vite.config.js": fe_vite,
    f"{root}/frontend/src/App.jsx": fe_app,
    f"{root}/frontend/src/main.jsx": fe_main,
    f"{root}/frontend/index.html": fe_html,
}

for p, c in files.items(): create_file(p, c)

# ==========================================
# 3. APLICAÇÃO
# ==========================================

print("\n🚀 Aplicando Kubernetes (Backend v13 | Frontend v10)...")
run_cmd(f"kubectl apply -f {root}/k8s/00-namespace.yaml")
run_cmd(f"kubectl apply -f {root}/k8s/")

print("\n⏳ Aguardando Pods iniciarem...")
time.sleep(10)
run_cmd("kubectl wait --for=condition=ready pod -l app=backend -n estudos --timeout=120s")

print("\n⚙️ Tentando Restaurar Backup...")
try:
    pod = subprocess.check_output("kubectl get pod -l app=backend -n estudos -o jsonpath='{.items[0].metadata.name}'", shell=True, text=True).strip()
    run_cmd(f"kubectl exec -it {pod} -n estudos -- python manage.py migrate")
    
    if os.path.exists("backup_full.json"):
        run_cmd(f"kubectl cp backup_full.json {pod}:/app/backup_full.json -n estudos")
        run_cmd(f"kubectl exec -it {pod} -n estudos -- python manage.py loaddata backup_full.json")
        print("✅ Backup restaurado!")
    else:
        print("⚠️ Backup não encontrado. Crie um superusuário:")
        run_cmd(f"kubectl exec -it {pod} -n estudos -- python manage.py createsuperuser")

except Exception as e:
    print(f"Erro no restore: {e}")

print("\n✨ RECONSTRUÇÃO CONCLUÍDA!")
print("⚠️ IMPORTANTE: Este script gera o código mais recente, mas aponta para a imagem v13.")
print("   Se a v13 não tiver as bibliotecas novas (como WeasyPrint ou Filters), o pod pode falhar.")
print("   Se falhar, execute: cd basecode/backend && docker build -t phenriquernagel/banco-questoes-backend:v13 . && docker push ...")
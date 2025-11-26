import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Arquivo recriado: {path}")

root = "basecode"

print("🏗️ INICIANDO RECONSTRUÇÃO TOTAL (Versão Final Estável)...")

# ================= KUBERNETES =================
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

# Apontando para v22 (Admin Ativado + Jazzmin)
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
        image: phenriquernagel/banco-questoes-backend:v22
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

# Apontando para v23 (Painel Professor + PDF Cliente)
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
        image: phenriquernagel/banco-questoes-frontend:v23
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

# ================= BACKEND (Django) =================
be_req = """Django>=5.0,<6.0
djangorestframework>=3.14
psycopg2-binary>=2.9
django-cors-headers>=4.3
gunicorn>=21.2
django-jazzmin>=2.6.0
whitenoise>=6.6.0
"""

be_docker = """FROM python:3.11-slim
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

be_settings = """import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = ['jazzmin','django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','rest_framework','corsheaders','questoes']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware','corsheaders.middleware.CorsMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'core.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates','DIRS': [],'APP_DIRS': True,'OPTIONS': {'context_processors': ['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages',],},},]
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
JAZZMIN_UI_TWEAKS = {"theme": "flatly", "dark_mode_theme": "darkly"}
"""

be_urls = """from django.urls import path, include
from django.contrib import admin
urlpatterns = [path('admin/', admin.site.urls),path('api/', include('questoes.urls'))]
"""

# App Questoes
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
    def __str__(self): return self.enunciado[:30]
"""

q_admin = """from django.contrib import admin
from .models import Topico, Questao
@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'enunciado_curto', 'topico', 'dificuldade')
    list_filter = ('topico', 'dificuldade', 'correta')
    search_fields = ('enunciado',)
    def enunciado_curto(self, obj): return obj.enunciado[:50]
"""

q_views = """from rest_framework import viewsets
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
        search = self.request.query_params.get('search')
        if topico_id: qs = qs.filter(topico_id=topico_id)
        if search: qs = qs.filter(enunciado__icontains=search)
        return qs
"""

q_serial = """from rest_framework import serializers
from .models import Topico, Questao
class TopicoSerializer(serializers.ModelSerializer):
    class Meta: model = Topico; fields = '__all__'
class QuestaoSerializer(serializers.ModelSerializer):
    topico_nome = serializers.ReadOnlyField(source='topico.nome')
    class Meta: model = Questao; fields = '__all__'
"""

q_urls = """from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicoViewSet, QuestaoViewSet
router = DefaultRouter()
router.register(r'topicos', TopicoViewSet)
router.register(r'questoes', QuestaoViewSet)
urlpatterns = [path('', include(router.urls))]
"""

q_apps = "from django.apps import AppConfig\nclass QuestoesConfig(AppConfig):\n    default_auto_field = 'django.db.models.BigAutoField'\n    name = 'questoes'"

# ================= FRONTEND (React) =================
fe_pkg = """{
  "name": "front", "private": true, "version": "2.0.0", "type": "module",
  "scripts": { "dev": "vite", "build": "vite build" },
  "dependencies": { "react": "^18.2.0", "react-dom": "^18.2.0", "jspdf": "^2.5.1" },
  "devDependencies": { "@vitejs/plugin-react": "^4.2.1", "vite": "^5.2.0" }
}"""

fe_nginx = """server {
    listen 80;
    location / { root /usr/share/nginx/html; index index.html index.htm; try_files $uri $uri/ /index.html; }
    location /api/ { proxy_pass http://backend-service.estudos.svc.cluster.local:8000; proxy_set_header Host $host; }
}"""

fe_app = """import React, { useState, useEffect } from 'react';
import { jsPDF } from "jspdf";
function App() {
  const [questoes, setQuestoes] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [busca, setBusca] = useState("");
  const API_URL = "/api/questoes/";

  useEffect(() => {
    setLoading(true);
    let url = API_URL + (busca ? `?search=${busca}` : "");
    const delay = setTimeout(() => {
        fetch(url).then(r=>r.json()).then(d=>{setQuestoes(d);setLoading(false);}).catch(e=>{console.error(e);setLoading(false);});
    }, 300);
    return () => clearTimeout(delay);
  }, [busca]);

  const toggleSelect = (id) => selectedIds.includes(id) ? setSelectedIds(selectedIds.filter(i=>i!==id)) : setSelectedIds([...selectedIds, id]);

  const gerarPDF = () => {
    const doc = new jsPDF();
    const selecionadas = questoes.filter(q => selectedIds.includes(q.id));
    let y = 20;
    doc.setFontSize(18); doc.setFont("helvetica", "bold"); doc.text("Avaliação MathMaster", 105, y, {align:"center"}); y+=20;
    doc.setFontSize(12); doc.setFont("helvetica", "normal");
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
    doc.addPage(); y=20; doc.setFontSize(16); doc.text("Gabarito", 105, y, {align:"center"}); y+=20; doc.setFontSize(12);
    selecionadas.forEach((q, i)=>{doc.text(`${i+1}) ${q.correta}`, 20, y); y+=8;});
    doc.save("Prova_Matematica.pdf");
  };

  const s = {
    page: { fontFamily: 'Inter, sans-serif', backgroundColor: '#f8fafc', minHeight: '100vh', paddingBottom: '120px' },
    nav: { backgroundColor: 'white', padding: '15px 30px', borderBottom: '1px solid #e2e8f0', position:'sticky', top:0, zIndex:10 },
    searchBar: { maxWidth: '800px', margin: '30px auto', padding: '0 20px' },
    input: { width: '100%', padding: '16px', borderRadius: '12px', border: '1px solid #cbd5e1', fontSize: '1rem' },
    grid: { display: 'grid', gap: '20px', maxWidth: '800px', margin: '0 auto', padding: '0 20px' },
    card: (isSelected) => ({
        backgroundColor: isSelected ? '#eff6ff' : 'white',
        border: isSelected ? '2px solid #3b82f6' : '1px solid #e2e8f0',
        borderRadius: '16px', padding: '24px', cursor: 'pointer', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', position:'relative'
    }),
    badge: { backgroundColor: '#f1f5f9', color: '#475569', padding: '4px 10px', borderRadius: '20px', fontSize: '0.75rem', fontWeight: 'bold' },
    actionBar: {
        position: 'fixed', bottom: '30px', left: '50%', transform: 'translateX(-50%)',
        backgroundColor: '#1e293b', color: 'white', padding: '12px 24px', borderRadius: '50px',
        display: 'flex', alignItems: 'center', gap: '20px', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.3)', zIndex:50
    },
    btn: { backgroundColor: '#3b82f6', color: 'white', border: 'none', padding: '10px 20px', borderRadius: '30px', fontWeight: 'bold', cursor: 'pointer' }
  };

  return (
    <div style={s.page}>
      <nav style={s.nav}><h1 style={{fontSize:'1.2rem', margin:0}}>🎓 MathMaster</h1></nav>
      <div style={s.searchBar}><input placeholder="🔎 Pesquisar..." value={busca} onChange={e=>setBusca(e.target.value)} style={s.input}/></div>
      <main style={s.grid}>
        {!loading && questoes.map(q => {
           const isSel = selectedIds.includes(q.id);
           return (
             <div key={q.id} style={s.card(isSel)} onClick={() => toggleSelect(q.id)}>
               <div style={{display:'flex',gap:'10px',marginBottom:'15px'}}>
                   <span style={s.badge}>{q.topico_nome || 'Geral'}</span>
                   <span style={{...s.badge, color: q.dificuldade==='F'?'green':q.dificuldade==='M'?'orange':'red'}}>{q.dificuldade}</span>
               </div>
               {isSel && <div style={{position:'absolute',top:'20px',right:'20px',fontSize:'1.5rem'}}>✅</div>}
               <h3 style={{marginTop:0}}>{q.enunciado}</h3>
               <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'5px',fontSize:'0.9rem',color:'#666'}}>
                   <div>A) {q.alternativa_a}</div><div>B) {q.alternativa_b}</div><div>C) {q.alternativa_c}</div><div>D) {q.alternativa_d}</div>
               </div>
             </div>
           )
        })}
      </main>
      {selectedIds.length > 0 && (
          <div style={s.actionBar}><span><strong>{selectedIds.length}</strong> selecionadas</span><button style={s.btn} onClick={gerarPDF}>📥 Baixar PDF</button></div>
      )}
    </div>
  );
}
export default App;"""

fe_vite = "import { defineConfig } from 'vite'; import react from '@vitejs/plugin-react'; export default defineConfig({plugins: [react()], server: {port: 3000, host: true}});"
fe_main = "import React from 'react'; import ReactDOM from 'react-dom/client'; import App from './App.jsx'; ReactDOM.createRoot(document.getElementById('root')).render(<App />);"
fe_html = '<!doctype html><html lang="pt-br"><head><meta charset="UTF-8"/><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet"><style>body{font-family:Inter,sans-serif;margin:0}</style><title>MathMaster</title></head><body><div id="root"></div><script type="module" src="/src/main.jsx"></script></body></html>'

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
    f"{root}/backend/core/wsgi.py": "import os; from django.core.wsgi import get_wsgi_application; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings'); application = get_wsgi_application()",
    f"{root}/backend/manage.py": "import os; import sys; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings'); from django.core.management import execute_from_command_line; execute_from_command_line(sys.argv)",
    f"{root}/backend/questoes/models.py": q_models,
    f"{root}/backend/questoes/admin.py": q_admin,
    f"{root}/backend/questoes/views.py": q_views,
    f"{root}/backend/questoes/urls.py": q_urls,
    f"{root}/backend/questoes/serializers.py": q_serial,
    f"{root}/backend/questoes/apps.py": q_apps,
    f"{root}/frontend/Dockerfile": "FROM node:18-alpine as build\nWORKDIR /app\nCOPY package.json ./\nRUN npm install\nCOPY . .\nRUN npm run build\nFROM nginx:alpine\nCOPY --from=build /app/dist /usr/share/nginx/html\nCOPY nginx.conf /etc/nginx/conf.d/default.conf\nEXPOSE 80\nCMD [\"nginx\", \"-g\", \"daemon off;\"]",
    f"{root}/frontend/nginx.conf": fe_nginx,
    f"{root}/frontend/package.json": fe_pkg,
    f"{root}/frontend/vite.config.js": fe_vite,
    f"{root}/frontend/src/App.jsx": fe_app,
    f"{root}/frontend/src/main.jsx": fe_main,
    f"{root}/frontend/index.html": fe_html,
}

for p, c in files.items(): create_file(p, c)

print("\n✨ CÓDIGO FONTE FINAL RECRIADO COM SUCESSO!")
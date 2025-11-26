import os

def create_file(path, content):
    # Cria os diretórios necessários se não existirem
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Escreve o conteúdo no arquivo
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Criado: {path}")

# --- CONTEÚDOS DOS ARQUIVOS ---

# 1. KUBERNETES
k8s_namespace = """
apiVersion: v1
kind: Namespace
metadata:
  name: estudos
"""

# 2. BACKEND (Django)
backend_requirements = """
Django>=5.0,<6.0
djangorestframework>=3.14
psycopg2-binary>=2.9
django-cors-headers>=4.3
gunicorn>=21.2
"""

backend_dockerfile = """
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \\
    gcc \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
"""

# Simulação básica do manage.py
backend_manage = """
#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
"""

# Settings.py configurado para K8s e Docker
backend_settings = """
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
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
        'DIRS': [],
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

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
]
"""

backend_urls = """
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
"""

backend_wsgi = """
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_wsgi_application()
"""

# 3. FRONTEND (React + Vite + Nginx)
frontend_dockerfile = """
FROM node:18-alpine as build
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""

frontend_nginx = """
server {
    listen 80;
    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
        try_files $uri $uri/ /index.html;
    }
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
"""

frontend_package = """
{
  "name": "banco-questoes-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.2.0"
  }
}
"""

frontend_vite = """
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true
  }
})
"""

frontend_index = """
<!doctype html>
<html lang="pt-br">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Banco de Questões</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""

frontend_main = """
import React from 'react'
import ReactDOM from 'react-dom/client'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '20px', textAlign: 'center' }}>
      <h1>🎓 Banco de Questões</h1>
      <p>Infraestrutura inicial pronta!</p>
    </div>
  </React.StrictMode>,
)
"""

# 4. EXTRAS
gitignore = """
venv
__pycache__
*.pyc
db.sqlite3
node_modules
dist
.DS_Store
.env
"""

# --- EXECUÇÃO DO SCRIPT ---

root = "codebase"

# Mapeamento de Caminho -> Conteúdo
files = {
    # Backend
    f"{root}/backend/Dockerfile": backend_dockerfile,
    f"{root}/backend/requirements.txt": backend_requirements,
    f"{root}/backend/manage.py": backend_manage,
    f"{root}/backend/core/__init__.py": "",
    f"{root}/backend/core/settings.py": backend_settings,
    f"{root}/backend/core/urls.py": backend_urls,
    f"{root}/backend/core/wsgi.py": backend_wsgi,
    f"{root}/backend/.dockerignore": gitignore,
    
    # Frontend
    f"{root}/frontend/Dockerfile": frontend_dockerfile,
    f"{root}/frontend/nginx.conf": frontend_nginx,
    f"{root}/frontend/package.json": frontend_package,
    f"{root}/frontend/vite.config.js": frontend_vite,
    f"{root}/frontend/index.html": frontend_index,
    f"{root}/frontend/src/main.jsx": frontend_main,
    f"{root}/frontend/.dockerignore": gitignore,
    
    # K8s e Raiz
    f"{root}/k8s/00-namespace.yaml": k8s_namespace,
    f"{root}/.gitignore": gitignore,
}

print(f"🚀 Iniciando geração do projeto '{root}'...")

for path, content in files.items():
    create_file(path, content)

print("\n✨ Projeto gerado com sucesso!")
print(f"📂 Entre na pasta: cd {root}")

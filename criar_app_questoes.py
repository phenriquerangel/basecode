import os

def create_file(path, content):
    # Cria a pasta se não existir
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Escreve o conteúdo (sobrescreve se já existir)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Atualizado/Criado: {path}")

# Caminho base do projeto
root = "basecode/backend"

# --- 1. MODELS.PY (Tabelas do Banco) ---
models_content = """
from django.db import models

class Topico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class Questao(models.Model):
    DIFICULDADE_CHOICES = [
        ('F', 'Fácil'),
        ('M', 'Médio'),
        ('D', 'Difícil'),
    ]

    enunciado = models.TextField(verbose_name="Enunciado da Questão")
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, related_name='questoes')
    dificuldade = models.CharField(max_length=1, choices=DIFICULDADE_CHOICES, default='M')
    
    # Alternativas
    alternativa_a = models.CharField(max_length=255)
    alternativa_b = models.CharField(max_length=255)
    alternativa_c = models.CharField(max_length=255)
    alternativa_d = models.CharField(max_length=255)
    
    # Resposta
    correta = models.CharField(max_length=1, choices=[('A','A'), ('B','B'), ('C','C'), ('D','D')])
    justificativa = models.TextField(verbose_name="Explicação / Resolução", blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"

    def __str__(self):
        return f"{self.topico} - {self.enunciado[:50]}..."
"""

# --- 2. ADMIN.PY (Painel Administrativo) ---
admin_content = """
from django.contrib import admin
from .models import Topico, Questao

@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'questoes_count')

    def questoes_count(self, obj):
        return obj.questoes.count()
    questoes_count.short_description = 'Qtd Questões'

@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    list_display = ('enunciado_curto', 'topico', 'dificuldade', 'correta')
    list_filter = ('topico', 'dificuldade')
    search_fields = ('enunciado',)

    def enunciado_curto(self, obj):
        return obj.enunciado[:50] + "..."
    enunciado_curto.short_description = 'Enunciado'
"""

# --- 3. APPS.PY (Configuração da App) ---
apps_content = """
from django.apps import AppConfig

class QuestoesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'questoes'
"""

# --- 4. SETTINGS.PY (Configuração Geral com 'questoes' incluído) ---
settings_content = """
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
    # Libs de terceiros
    'rest_framework',
    'corsheaders',
    # NOSSAS APPS
    'questoes',  # <--- ESSENCIAL PARA A MIGRAÇÃO FUNCIONAR
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

# --- EXECUÇÃO: Criar os arquivos ---

files = {
    f"{root}/questoes/__init__.py": "",
    f"{root}/questoes/models.py": models_content,
    f"{root}/questoes/admin.py": admin_content,
    f"{root}/questoes/apps.py": apps_content,
    f"{root}/questoes/migrations/__init__.py": "", # Garante que a pasta migrations existe
    f"{root}/core/settings.py": settings_content,
}

print("🚀 Regenerando arquivos do módulo 'questoes'...")

for path, content in files.items():
    create_file(path, content)

print("\n✨ Arquivos regenerados com sucesso!")
print("⚠️ PRÓXIMO PASSO OBRIGATÓRIO: Fazer Build (sem cache) e Push da nova imagem.")
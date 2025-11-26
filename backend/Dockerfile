# Arquivo: backend/Dockerfile

# 1. Usar uma imagem oficial leve do Python
FROM python:3.11-slim

# 2. Definir variáveis de ambiente para evitar arquivos .pyc e logs presos
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Definir o diretório de trabalho dentro do container
WORKDIR /app

# 4. Instalar dependências do sistema necessárias para o Postgres
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar o arquivo de dependências e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar o restante do código do projeto
COPY . .

# 7. Expor a porta que o Django usa (padrão 8000)
EXPOSE 8000

# 8. Comando para iniciar o servidor (usaremos o gunicorn no futuro, mas runserver serve para dev)
# Usa o Gunicorn para rodar o Django de forma robusta na porta 8000
# 'core' é o nome da pasta onde está o settings.py (definimos isso lá no início)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
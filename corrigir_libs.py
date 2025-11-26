import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Arquivo atualizado: {path}")

root = "basecode/backend"

# Adicionamos explicitamente 'django-filter'
requirements = """
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

files = {
    f"{root}/requirements.txt": requirements,
}

print("🔧 Corrigindo lista de dependências...")
for path, content in files.items():
    create_file(path, content)
print("✨ Pronto. Agora o build v14 é OBRIGATÓRIO.")
import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Configurado: {path}")

root = "basecode/backend/questoes"

# Conteúdo do admin.py
# Aqui definimos quais colunas aparecem e os filtros laterais
admin_content = """
from django.contrib import admin
from .models import Topico, Questao

@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'descricao')
    search_fields = ('nome',)
    ordering = ('nome',)

@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    # Colunas que aparecem na lista
    list_display = ('id', 'enunciado_curto', 'topico', 'dificuldade', 'correta')
    
    # Filtros laterais (MUITO ÚTIL)
    list_filter = ('topico', 'dificuldade', 'correta')
    
    # Barra de pesquisa
    search_fields = ('enunciado', 'justificativa')
    
    # Paginação
    list_per_page = 20

    # Função para encurtar o texto na lista
    def enunciado_curto(self, obj):
        return obj.enunciado[:50] + "..."
    enunciado_curto.short_description = 'Enunciado'
"""

files = {
    f"{root}/admin.py": admin_content,
}

print("🔧 Configurando abas de Tópicos e Questões no Admin...")
for path, content in files.items():
    create_file(path, content)
print("✨ Arquivo admin.py atualizado! Faça o build v22.")
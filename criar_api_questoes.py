import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Criado: {path}")

root = "basecode/backend"

# 1. SERIALIZERS.PY (Tradutor Python -> JSON)
serializers_content = """
from rest_framework import serializers
from .models import Topico, Questao

class TopicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topico
        fields = ['id', 'nome', 'descricao']

class QuestaoSerializer(serializers.ModelSerializer):
    # Para mostrar o nome do tópico em vez de apenas o ID
    topico_nome = serializers.ReadOnlyField(source='topico.nome')

    class Meta:
        model = Questao
        fields = [
            'id', 'enunciado', 'topico', 'topico_nome', 'dificuldade',
            'alternativa_a', 'alternativa_b', 'alternativa_c', 'alternativa_d',
            'correta', 'justificativa'
        ]
"""

# 2. VIEWS.PY (A Lógica / O Porteiro)
views_content = """
from rest_framework import viewsets
from .models import Topico, Questao
from .serializers import TopicoSerializer, QuestaoSerializer

class TopicoViewSet(viewsets.ModelViewSet):
    queryset = Topico.objects.all()
    serializer_class = TopicoSerializer

class QuestaoViewSet(viewsets.ModelViewSet):
    queryset = Questao.objects.all()
    serializer_class = QuestaoSerializer
    
    # Permite filtrar por tópico ?topico=1
    def get_queryset(self):
        queryset = Questao.objects.all()
        topico_id = self.request.query_params.get('topico')
        if topico_id:
            queryset = queryset.filter(topico_id=topico_id)
        return queryset
"""

# 3. URLS.PY (Rotas da App Questoes)
urls_app_content = """
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicoViewSet, QuestaoViewSet

router = DefaultRouter()
router.register(r'topicos', TopicoViewSet)
router.register(r'questoes', QuestaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
"""

# 4. CORE/URLS.PY (Rota Principal - Atualizada)
# Adicionamos o path 'api/' apontando para a app questoes
urls_core_content = """
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('questoes.urls')), # <--- Nova Rota da API
]
"""

files = {
    f"{root}/questoes/serializers.py": serializers_content,
    f"{root}/questoes/views.py": views_content,
    f"{root}/questoes/urls.py": urls_app_content,
    f"{root}/core/urls.py": urls_core_content, # Substitui o original
}

print("🚀 Criando Camada de API (Serializers, Views, URLs)...")
for path, content in files.items():
    create_file(path, content)
print("✨ Código da API gerado! Faça o Build v7.")
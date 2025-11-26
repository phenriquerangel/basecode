import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Backend Corrigido: {path}")

root = "basecode/backend/questoes"

# VIEWS.PY (Agora com suporte a Dificuldade)
views_content = """
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
        
        # Captura os parâmetros da URL
        topico_id = self.request.query_params.get('topico')
        dificuldade = self.request.query_params.get('dificuldade') # <--- O QUE FALTAVA
        search = self.request.query_params.get('search')
        
        # Aplica os filtros se eles existirem
        if topico_id:
            qs = qs.filter(topico_id=topico_id)
            
        if dificuldade:
            qs = qs.filter(dificuldade=dificuldade) # <--- A LÓGICA NOVA
            
        if search:
            # Busca no enunciado OU na justificativa
            qs = qs.filter(enunciado__icontains=search) | qs.filter(justificativa__icontains=search)
            
        return qs
"""

files = {
    f"{root}/views.py": views_content,
}

print("🔧 Adicionando lógica de filtro de Dificuldade ao Backend...")
for path, content in files.items():
    create_file(path, content)
print("✨ Código corrigido! Necessário Build do Backend v25.")
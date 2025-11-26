import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Atualizado: {path}")

root = "basecode/backend"

# VIEWS.PY ATUALIZADO
# Adicionamos 'AllowAny' para corrigir o erro 403
views_content = """
from rest_framework import viewsets, views, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny # <--- Importante
from django.http import HttpResponse
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from weasyprint import HTML
from .models import Topico, Questao
from .serializers import TopicoSerializer, QuestaoSerializer

class TopicoViewSet(viewsets.ModelViewSet):
    queryset = Topico.objects.all()
    serializer_class = TopicoSerializer
    permission_classes = [AllowAny] # Permite leitura pública

class QuestaoViewSet(viewsets.ModelViewSet):
    queryset = Questao.objects.all().order_by('-id')
    serializer_class = QuestaoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['topico', 'dificuldade']
    search_fields = ['enunciado', 'justificativa']
    permission_classes = [AllowAny] # Permite leitura pública

class GerarPDFView(views.APIView):
    # --- A CORREÇÃO DO ERRO 403 ESTÁ AQUI ---
    permission_classes = [AllowAny] 
    authentication_classes = [] 
    # ----------------------------------------

    def post(self, request):
        ids = request.data.get('ids', [])
        questoes = Questao.objects.filter(id__in=ids)
        
        if not questoes:
            return Response({"erro": "Nenhuma questão encontrada"}, status=400)
        
        # Renderiza e gera PDF
        try:
            html_string = render_to_string('questoes/prova.html', {'questoes': questoes})
            pdf_file = HTML(string=html_string).write_pdf()
            
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="prova_mathmaster.pdf"'
            return response
        except Exception as e:
            print(f"ERRO AO GERAR PDF: {e}")
            return Response({"erro": str(e)}, status=500)
"""

files = {
    f"{root}/questoes/views.py": views_content,
}

print("🔓 Liberando permissões da API (Correção do 403)...")
for path, content in files.items():
    create_file(path, content)
print("✨ Arquivo views.py atualizado. Faça o Build v13 do Backend.")
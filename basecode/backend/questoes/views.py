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
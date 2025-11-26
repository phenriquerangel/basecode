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
        topico_id = self.request.query_params.get('topico')
        search = self.request.query_params.get('search')
        if topico_id: qs = qs.filter(topico_id=topico_id)
        if search: qs = qs.filter(enunciado__icontains=search)
        return qs
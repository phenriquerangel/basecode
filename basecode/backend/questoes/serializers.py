from rest_framework import serializers
from .models import Topico, Questao
class TopicoSerializer(serializers.ModelSerializer):
    class Meta: model = Topico; fields = '__all__'
class QuestaoSerializer(serializers.ModelSerializer):
    topico_nome = serializers.ReadOnlyField(source='topico.nome')
    class Meta: model = Questao; fields = '__all__'
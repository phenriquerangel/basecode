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
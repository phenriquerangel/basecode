from django.contrib import admin
from .models import Topico, Questao

@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'questoes_count')

    def questoes_count(self, obj):
        return obj.questoes.count()
    questoes_count.short_description = 'Qtd Questões'

@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    list_display = ('enunciado_curto', 'topico', 'dificuldade', 'correta')
    list_filter = ('topico', 'dificuldade')
    search_fields = ('enunciado',)

    def enunciado_curto(self, obj):
        return obj.enunciado[:50] + "..."
    enunciado_curto.short_description = 'Enunciado'
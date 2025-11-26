from django.contrib import admin
from .models import Topico, Questao
@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'enunciado_curto', 'topico', 'dificuldade')
    list_filter = ('topico', 'dificuldade', 'correta')
    search_fields = ('enunciado',)
    def enunciado_curto(self, obj): return obj.enunciado[:50]
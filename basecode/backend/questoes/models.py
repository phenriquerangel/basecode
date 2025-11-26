from django.db import models
class Topico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    def __str__(self): return self.nome

class Questao(models.Model):
    DIFICULDADE_CHOICES = [('F', 'Fácil'), ('M', 'Médio'), ('D', 'Difícil')]
    enunciado = models.TextField()
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, related_name='questoes')
    dificuldade = models.CharField(max_length=1, choices=DIFICULDADE_CHOICES, default='M')
    alternativa_a = models.CharField(max_length=255)
    alternativa_b = models.CharField(max_length=255)
    alternativa_c = models.CharField(max_length=255)
    alternativa_d = models.CharField(max_length=255)
    correta = models.CharField(max_length=1, choices=[('A','A'), ('B','B'), ('C','C'), ('D','D')])
    justificativa = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    class Meta: verbose_name = "Questão"; verbose_name_plural = "Questões"
    def __str__(self): return self.enunciado[:30]
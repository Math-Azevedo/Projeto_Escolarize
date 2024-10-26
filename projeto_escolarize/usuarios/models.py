from django.contrib.auth.models import User
from django.db import models

class Serie(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nome

class Materia(models.Model):
    nome = models.CharField(max_length=100)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name='materias')
    
    def __str__(self):
        return self.nome

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identificador = models.CharField(max_length=9999)
    nome = models.CharField(max_length=100)
    series = models.ManyToManyField(Serie, related_name="professores")
    materias = models.ManyToManyField(Materia, related_name="professores")
    
    def __str__(self):
        return self.nome

    @property
    def is_professor(self):
        return True

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identificador = models.CharField(max_length=10)
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    materias = models.ManyToManyField(Materia, related_name='alunos', blank=True)
    professores = models.ManyToManyField(Professor)
    pai_mae = models.ForeignKey('PaiMae', on_delete=models.CASCADE, related_name='alunos', null=False)
    is_pai = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome

class AlunoMateria(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nota_1bimestre = models.FloatField(null=True, blank=True)
    nota_2bimestre = models.FloatField(null=True, blank=True)
    nota_3bimestre = models.FloatField(null=True, blank=True)
    nota_4bimestre = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = (('aluno', 'materia'),)
        
    @property
    def media(self):
        notas = [self.nota_1bimestre, self.nota_2bimestre, self.nota_3bimestre, self.nota_4bimestre]
        return sum(nota for nota in notas if nota is not None) / len([nota for nota in notas if nota is not None])


class PaiMae(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identificador = models.CharField(max_length=9999)
    nome = models.CharField(max_length=100)
    is_pai = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome

class Mensagem(models.Model):
    remetente = models.ForeignKey(PaiMae, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    conteudo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Mensagem de {self.remetente} para {self.destinatario}'
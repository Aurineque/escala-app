from django.db import models

class Evento(models.Model):
    nome = models.CharField(max_length=100, help_text="Ex: Culto de Domingo, Santa Ceia")
    data = models.DateTimeField()
    vagas_midia = models.IntegerField(default=2, help_text="Quantas pessoas precisam servir neste dia?")

    @property
    def vagas_restantes(self):
        # O Django vai na tabela de Escala e conta quantos voluntários já estão ligados a este evento
        vagas_ocupadas = self.escala_set.count() 
        
        # Diminui o total de vagas pelas vagas ocupadas
        resultado = self.vagas_midia - vagas_ocupadas
        
        # Garante que não mostre número negativo se der algum bug
        return max(resultado, 0)

    def __str__(self):
        # Como o evento vai aparecer listado para você
        return f"{self.nome} - {self.data.strftime('%d/%m/%Y')}"

class Membro(models.Model):
    # Opções de funções para a mídia
    FUNCOES = [
        ('camera', 'Câmera'),
        ('story', 'Story'),
        ('projecao', 'Projeção'),
        ('geral', 'Apoio Geral')
    ]
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    funcao_principal = models.CharField(max_length=20, choices=FUNCOES, default='geral')

    def __str__(self):
        return self.nome

class Escala(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
    confirmado = models.BooleanField(default=False)

    funcao = models.CharField(
        max_length=20, 
        choices=Membro.FUNCOES, 
        default='geral'
    )

    class Meta:
        # Impede que o mesmo membro marque duas vezes no mesmo dia
        unique_together = ['evento', 'membro'] 

    def __str__(self):
        return f"{self.membro.nome} no(a) {self.evento.nome}"
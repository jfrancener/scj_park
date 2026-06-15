from django.db import models

class Estacionamento(models.Model):
    vagas_totais = models.IntegerField(default=100)
    vagas_ocupadas = models.IntegerField(default=0)

    def __str__(self):
        return f"Estacionamento: {self.vagas_ocupadas}/{self.vagas_totais} vagas"

    @property
    def vagas_disponiveis(self):
        return max(0, self.vagas_totais - self.vagas_ocupadas)

    @classmethod
    def obter_instancia(cls):
        instancia = cls.objects.first()
        if not instancia:
            instancia = cls.objects.create(vagas_totais=100, vagas_ocupadas=0)
        return instancia

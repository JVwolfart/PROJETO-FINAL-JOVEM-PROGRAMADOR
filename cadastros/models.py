from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class GrupoDespesa(models.Model):
    grupo = models.CharField(max_length=50)
    padrao = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Grupo de despesa'
        verbose_name_plural = 'Grupos de despesa'

    def __str__(self):
        return self.grupo

class TipoDespesa(models.Model):
    tipo = models.CharField(max_length=80)
    padrao = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    grupo = models.ForeignKey(GrupoDespesa, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Tipo de despesa'
        verbose_name_plural = 'Tipos de despesa'

    def __str__(self):
        return self.tipo

class FormaPagamento(models.Model):
    forma = models.CharField(max_length=30)
    padrao = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Forma de pagamento'
        verbose_name_plural = 'Formas de Pagamento'

    def __str__(self):
        return self.forma


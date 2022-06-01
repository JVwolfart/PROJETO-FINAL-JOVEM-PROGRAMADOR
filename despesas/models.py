from django.db import models
from django.contrib.auth.models import User
from cadastros.models import TipoDespesa, FormaPagamento
# Create your models here.

class Despesa(models.Model):
    despesa = models.TextField(blank=True, null=True)
    data = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoDespesa, on_delete=models.DO_NOTHING)
    fpag = models.ForeignKey(FormaPagamento, on_delete=models.DO_NOTHING)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'

    def __str__(self):
        return f'{self.tipo} {self.despesa}'

from django.contrib import admin
from cadastros.models import TipoDespesa, GrupoDespesa, FormaPagamento
# Register your models here.

class AdmGrupo(admin.ModelAdmin):
    list_display = ['id', 'grupo', 'padrao', 'ativo']
    list_display_links = ['id', 'grupo']
    list_editable = ['padrao', 'ativo']
    list_per_page = 10


class AdmTipo(admin.ModelAdmin):
    list_display = ['id', 'tipo', 'grupo', 'padrao', 'ativo']
    list_display_links = ['id', 'tipo']
    list_editable = ['grupo','padrao', 'ativo']
    list_per_page = 10

class AdmFpag(admin.ModelAdmin):
    list_display = ['id', 'forma', 'padrao', 'ativo']
    list_display_links = ['id', 'forma']
    list_editable = ['padrao', 'ativo']
    list_per_page = 10

admin.site.register(GrupoDespesa, AdmGrupo)
admin.site.register(TipoDespesa, AdmTipo)
admin.site.register(FormaPagamento, AdmFpag)
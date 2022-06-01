from django.contrib import admin
from despesas.models import Despesa
# Register your models here.

class AdmDespesas(admin.ModelAdmin):
    list_display = ['id', 'data', 'despesa', 'tipo', 'valor']
    list_display_links = ['id']
    list_per_page = 10
    search_fields = ['despesa', 'data', 'tipo']
    list_filter = ['tipo', 'data', 'usuario']

admin.site.register(Despesa, AdmDespesas)
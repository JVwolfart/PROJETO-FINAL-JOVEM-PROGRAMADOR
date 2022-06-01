from django.urls import path
from . import views

urlpatterns = [
    path('relatorios/', views.relatorios, name='relatorios'),
    path('despesas_por_data/', views.despesas_por_data, name='despesas_por_data'),
    path('ver_despesas/<str:data>', views.ver_despesas, name='ver_despesas'),
    path('despesas_por_intervalo/', views.despesas_por_intervalo, name='despesas_por_intervalo'),
    path('despesas_por_tipo/', views.despesas_por_tipo, name='despesas_por_tipo'),
    path('ver_despesas_tipo/<int:id>', views.ver_despesas_tipo, name='ver_despesas_tipo'),
    path('despesas_por_tipo_intervalo/', views.despesas_por_tipo_intervalo, name='despesas_por_tipo_intervalo'),
    path('ver_despesas_tipo_intervalo/<int:id>', views.ver_despesas_tipo_intervalo, name='ver_despesas_tipo_intervalo'),
    path('despesas_por_grupo/', views.despesas_por_grupo, name='despesas_por_grupo'),
    path('ver_despesas_grupo/<int:id>', views.ver_despesas_grupo, name='ver_despesas_grupo'),
    path('despesas_por_grupo_intervalo/', views.despesas_por_grupo_intervalo, name='despesas_por_grupo_intervalo'),
    path('ver_despesas_grupo_intervalo/<int:id>', views.ver_despesas_grupo_intervalo, name='ver_despesas_grupo_intervalo'),
    path('despesas_por_fpag/', views.despesas_por_fpag, name='despesas_por_fpag'),
    path('ver_despesas_fpag/<int:id>', views.ver_despesas_fpag, name='ver_despesas_fpag'),
    path('despesas_por_fpag_intervalo/', views.despesas_por_fpag_intervalo, name='despesas_por_fpag_intervalo'),
    path('ver_despesas_fpag_intervalo/<int:id>', views.ver_despesas_fpag_intervalo, name='ver_despesas_fpag_intervalo'),
]
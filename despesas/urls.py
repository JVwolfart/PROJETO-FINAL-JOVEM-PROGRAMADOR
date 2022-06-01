from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.index, name='home1'),
    path('despesa/', views.despesa, name='despesa'),
    path('lancar_despesa/', views.lancar_despesa, name='lancar_despesa'),
    path('alterar_despesa/<int:id>', views.alterar_despesa, name='alterar_despesa'),
    path('excluir_despesa/<int:id>', views.excluir_despesa, name='excluir_despesa'),
    path('manut_despesas/', views.manut_despesas, name='manut_despesas'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
]
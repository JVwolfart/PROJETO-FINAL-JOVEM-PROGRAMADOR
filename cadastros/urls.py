from django.urls import path
from . import views

urlpatterns = [
    path('cadastros/', views.cadastros, name='cadastros'),
    path('grupos/', views.grupos, name='grupos'),
    path('adicionar_grupo/', views.adicionar_grupo, name='adicionar_grupo'),
    path('alterar_grupo/<int:id>', views.alterar_grupo, name='alterar_grupo'),
    path('desativar_grupo/<int:id>', views.desativar_grupo, name='desativar_grupo'),
    path('tipos/', views.tipos, name='tipos'),
    path('adicionar_tipo/', views.adicionar_tipo, name='adicionar_tipo'),
    path('alterar_tipo/<int:id>', views.alterar_tipo, name='alterar_tipo'),
    path('desativar_tipo/<int:id>', views.desativar_tipo, name='desativar_tipo'),
    path('fpags/', views.fpags, name='fpags'),
    path('adicionar_fpag/', views.adicionar_fpag, name='adicionar_fpag'),
    path('alterar_fpag/<int:id>', views.alterar_fpag, name='alterar_fpag'),
    path('desativar_fpag/<int:id>', views.desativar_fpag, name='desativar_fpag'),
]
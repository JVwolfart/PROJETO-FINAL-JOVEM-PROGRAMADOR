from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutorial, name='tutorial'),
    path('tutorial_nl/', views.tutorial_nl, name='tutorial_nl'),
    path('documentacao/', views.documentacao, name='documentacao'),
    path('desenvolvedores/', views.desenvolvedores, name='desenvolvedores'),
    path('desenvolvedores_nl/', views.desenvolvedores_nl, name='desenvolvedores_nl'),
]
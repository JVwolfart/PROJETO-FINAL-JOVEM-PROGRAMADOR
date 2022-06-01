from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutorial, name='tutorial'),
    path('documentacao/', views.documentacao, name='documentacao'),
    path('desenvolvedores/', views.desenvolvedores, name='desenvolvedores'),
]
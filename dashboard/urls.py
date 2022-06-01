from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('dashboard_mes/', views.dashboard_mes, name='dashboard_mes'),
    path('despesas_dashboard/<int:id>', views.despesas_dashboard, name='despesas_dashboard'),
    path('despesas_dashboard_mes/<int:id>', views.despesas_dashboard_mes, name='despesas_dashboard_mes'),
    path('dashboard_ano/', views.dashboard_ano, name='dashboard_ano'),
]
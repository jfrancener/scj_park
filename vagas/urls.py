from django.urls import path
from . import views

app_name = 'vagas'

urlpatterns = [
    path('', views.index, name='index'),
    path('status/', views.status_vagas, name='status_vagas'),
    path('entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('saida/', views.registrar_saida, name='registrar_saida'),
    path('configurar/', views.configurar_estacionamento, name='configurar_estacionamento'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/registro/', views.clientes_registro, name='clientes_registro'),
    path('clientes/gestion/', views.clientes_gestion, name='clientes_gestion'),
    path('clientes/filtrar_clientes/', views.filtrar_clientes, name='filtrar_clientes'),
    path('clientes/gestion/modificar/<int:cliente_id>/', views.clientes_modificar, name='clientes_modificar'),
]

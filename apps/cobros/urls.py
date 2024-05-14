from django.urls import path
from . import views

urlpatterns = [
    path('cobros/', views.cobros, name='cobros'),
    path('buscar_producto/', views.buscar_producto, name='buscar_producto'),
    path('detalles_producto/', views.detalles_producto, name='detalles_producto'),
]

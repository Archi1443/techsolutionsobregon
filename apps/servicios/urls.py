from django.urls import path
from . import views
#from .views import enviar_mensaje_whatsapp


urlpatterns = [
    path('servicios/', views.servicios, name='servicios'),
    path('servicios/registro/', views.servicios_registro, name='servicios_registro'),
    path('servicios/gestion/', views.servicios_gestion, name='servicios_gestion'),
    path('buscar_cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('servicios/consulta/<int:id>/', views.servicios_consulta, name='servicios_consulta'),
    path('servicios/filtrar_servicios/', views.filtrar_servicios, name='filtrar_servicios'), 
    path('servicios/modificar/<int:id>/', views.servicios_editar, name='servicios_editar'),
    path('servicios/eliminar/<int:id>/', views.eliminar_servicio, name='eliminar_servicio'),
    #path('enviar-mensaje/', enviar_mensaje_whatsapp, name='enviar_mensaje'),
]

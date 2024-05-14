from django.urls import path
from . import views

urlpatterns = [
    path('empleados/', views.empleados, name='empleados'),
    path('empleados/registro/', views.empleados_registro, name='empleados_registro'),
    path('empleados/gestion/', views.empleados_gestion, name='empleados_gestion'),
    path('empleados/modificar/<int:id>/', views.empleados_modificar, name='empleados_modificar'),
    path('modificar/<int:id>/', views.empleados_modificar, name='empleados_modificar'),
     path('eliminar_empleado/<int:id>/', views.eliminar_empleado, name='empleados_eliminar'),
    path('buscar_empleado/', views.buscar_empleado, name='buscar_empleado'),
]

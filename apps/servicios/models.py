from django.db import models
from apps.clientes.models import Cliente, Celular
from apps.empleados.models import Empleado


class Servicio(models.Model):
    ESTADO_CHOICES = (
        ('ingresado', 'Ingresado'),
        ('en_proceso', 'En Proceso'),
        ('finalizado', 'Finalizado'),
        ('entregado', 'Entregado'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    celular = models.ForeignKey(Celular, on_delete=models.CASCADE)
    descripcion = models.TextField()
    cotizacion = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ingresado')
    pagado = models.BooleanField(default=False)
    anticipo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Nuevo campo para el anticipo

    @property
    def saldo_pendiente(self):
        return self.cotizacion - self.anticipo


class AccionesServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    foto_antes = models.ImageField(upload_to='fotos_antes/', null=True, blank=True)
    foto_despues = models.ImageField(upload_to='fotos_despues/', null=True, blank=True)

class Celular(models.Model):
    # tus campos existentes aquí
    imei = models.CharField(max_length=15, unique=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    # otros campos necesarios

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.imei})"



from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from apps.clientes.models import Cliente
from apps.empleados.models import Empleado
from apps.inventario.models import Producto
from apps.servicios.models import Servicio


class ProductoEnTicket(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='productos_en_ticket', null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.producto.cantidad -= self.cantidad
        else:
            original = ProductoEnTicket.objects.get(pk=self.pk)
            self.producto.cantidad += (original.cantidad - self.cantidad)
        self.producto.save()
        super().save(*args, **kwargs)

@receiver(post_delete, sender=ProductoEnTicket)
def revertir_cantidad(sender, instance, **kwargs):
    instance.producto.cantidad += instance.cantidad
    instance.producto.save()


class DetalleCobro(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='detalles_cobro')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='detalles_cobro')
    servicios = models.ManyToManyField(Servicio, related_name='detalles_cobro')
    productos = models.ManyToManyField(Producto, related_name='detalles_cobro')


class Cobro(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    detalle_cobro = models.ForeignKey(DetalleCobro, on_delete=models.CASCADE, related_name='cobros')

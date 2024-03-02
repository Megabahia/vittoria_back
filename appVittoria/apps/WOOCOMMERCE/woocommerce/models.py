from django.db import models


# Create your models here.
class Pedidos(models.Model):
    estado = models.CharField(max_length=255, null=False)
    envioTotal = models.FloatField(null=True)
    total = models.FloatField(null=True)
    facturacion = models.JSONField(null=True)
    envio = models.JSONField(null=True)
    metodoPago = models.CharField(max_length=255, null=False)
    numeroPedido = models.CharField(max_length=255, null=False)
    articulos = models.JSONField(null=True)
    envios = models.JSONField(null=True)
    json = models.JSONField(null=True)
    canal = models.CharField(max_length=255, null=True, blank=True)

    entregoProducto = models.CharField(max_length=255, null=True, blank=True)
    fechaEntrega = models.CharField(max_length=255, null=True, blank=True)
    horaEntrega = models.CharField(max_length=255, null=True, blank=True)
    calificacion = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

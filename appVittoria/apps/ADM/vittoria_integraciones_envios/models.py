from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class IntegracionesEnvios(models.Model):

    distancia =  models.FloatField(null=True, blank=True)
    costo =  models.FloatField(null=True, blank=True)

    pais = models.CharField(max_length=255, null=True, blank=True)
    provincia = models.CharField(max_length=255, null=True, blank=True)
    ciudad = models.CharField(max_length=255, null=True, blank=True)
    courier = models.CharField(max_length=255, null=True, blank=True)
    formaPago = models.JSONField(null=True)
    tamanio_inicial = models.FloatField(null=True, blank=True)
    tamanio_fin = models.FloatField(null=True, blank=True)
    peso_inicial = models.FloatField(null=True, blank=True)
    peso_fin = models.FloatField(null=True, blank=True)
    tiempo_entrega = models.IntegerField(null=True, blank=True)
    latitud = models.CharField(max_length=255, null=True, blank=True)
    longitud = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

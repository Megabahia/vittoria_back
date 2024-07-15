from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class IntegracionesEnvios(models.Model):
    ciudad_origen = models.CharField(max_length=250,null=True)
    ciudad_destino = models.CharField(max_length=250,null=True)
    distancia =  models.FloatField(null=True, blank=True)
    tamanio =  models.FloatField(null=True, blank=True)
    peso =  models.FloatField(null=True, blank=True)
    costo =  models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

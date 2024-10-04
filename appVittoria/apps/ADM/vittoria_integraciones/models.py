from django.db import models

# Create your models here.
class   Integraciones(models.Model):
    nombre = models.CharField(max_length=250,null=True)
    valor = models.CharField(max_length=250,null=True)
    pedidos_local = models.JSONField(null=True)
    pedidos_omniglobal = models.SmallIntegerField(default=0, null=True)
    despachos_local = models.JSONField(null=True)
    despachos_omniglobal = models.SmallIntegerField(default=0, null=True)

    tipoCanal = models.CharField(max_length=250,null=True)
    pais = models.CharField(max_length=250,null=True)
    provincia = models.CharField(max_length=250,null=True)
    ciudad = models.CharField(max_length=250,null=True)
    sector = models.CharField(max_length=250,null=True)
    latitud = models.CharField(max_length=250,null=True)
    longitud = models.CharField(max_length=250,null=True)

    prefijo = models.CharField(max_length=100,null=True)

    bodega_central = models.SmallIntegerField(default=0, null=True)

    descripcion_direccion = models.CharField(max_length=400, blank=True, null=True)
    direccion_mapa = models.CharField(max_length=400, blank=True, null=True)
    hora_atencion = models.CharField(max_length=400, blank=True, null=True)
    descuento = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

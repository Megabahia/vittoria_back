
from django.db import models

def upload_path(instance, filname):
  return '/'.join(['MDRP/imgProducto', str(instance.id) + "_" + filname])

# Create your models here.
class Productos(models.Model):

  nombre = models.CharField(max_length=150, null=True, blank=True)
  descripcion = models.TextField(null=True, blank=True)
  comentario = models.TextField(null=True, blank=True)
  codigo_barras = models.CharField(max_length=150, null=True, blank=True)
  lote = models.CharField(max_length=10, null=True, blank=True)
  stock = models.PositiveIntegerField(null=True, blank=True)
  proveedor = models.CharField(max_length=150, null=True, blank=True)
  costoCompra = models.FloatField(null=True, blank=True)
  imagen = models.FileField(blank=True, null=True, upload_to=upload_path)

  precioVentaA = models.FloatField(null=True, blank=True)
  precioVentaB = models.FloatField(null=True, blank=True)
  precioVentaC = models.FloatField(null=True, blank=True)
  precioVentaD = models.FloatField(null=True, blank=True)
  precioVentaE = models.FloatField(null=True, blank=True)
  precioVentaF = models.FloatField(null=True, blank=True)

  porcentaje_comision = models.IntegerField(null=True, blank=True)
  valor_comision = models.FloatField(null=True, blank=True)
  estado = models.CharField(max_length=150, null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  fecha_aprobacion = models.DateTimeField(null=True)
  fecha_confirmacion = models.DateTimeField(null=True)
  state = models.SmallIntegerField(default=1)


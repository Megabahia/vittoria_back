from django.db import models

# Create your models here.
class Productos(models.Model):
    categoria = models.CharField(max_length=150,null=True)
    subCategoria = models.CharField(max_length=150,null=True)
    nombre = models.CharField(max_length=150,null=True)
    descripcion = models.CharField(max_length=150,null=True)
    codigoBarras = models.CharField(max_length=150,null=True)
    refil = models.IntegerField(max_length=150,null=True)
    stock = models.IntegerField(max_length=150,null=True)
    caducidad = models.IntegerField(max_length=150,null=True)
    costoCompra = models.FloatField(null=True)
    precioVentaA = models.FloatField(null=True)
    precioVentaB = models.FloatField(null=True)
    precioVentaC = models.FloatField(null=True)
    precioVentaD = models.FloatField(null=True)
    precioVentaE = models.FloatField(null=True)
    precioVentaBultos = models.FloatField(null=True)
    alertaAbastecimiento = models.CharField(max_length=150,null=True)
    estado = models.CharField(max_length=150,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(Productos, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombre)

# Create your models here.
class ReporteAbastecimiento(models.Model):
    producto= models.ForeignKey(Productos, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con la categoria
    # stockActual = models.IntegerField(max_length=150,null=True)
    # alertaAbastecimiento = models.CharField(max_length=150,null=True)
    cantidadSugeridaStock = models.CharField(max_length=150,null=True)
    fechaMaximaStock = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(Productos, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombre)


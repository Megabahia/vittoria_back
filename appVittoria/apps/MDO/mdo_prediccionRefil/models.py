from django.db import models

# Create your models here.
class PrediccionRefil(models.Model):
    # codigo = models.IntegerField(null=False)
    fechaPredicciones = models.DateField(null=True)
    nombres = models.CharField(max_length=255,null=False)
    apellidos = models.CharField(max_length=255,null=False)
    identificacion = models.CharField(max_length=13,null=False)
    telefono = models.CharField(max_length=250,null=True)
    correo = models.EmailField(max_length=255,null=True)
    cliente = models.SmallIntegerField(null=True)
    negocio = models.SmallIntegerField(null=True)
    total = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(PrediccionRefil, self).save(*args, **kwargs)

class Detalles(models.Model):
    prediccionRefil = models.ForeignKey(PrediccionRefil, related_name='detalles', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Factura
    articulo = models.CharField(max_length=150,null=True)
    valorUnitario = models.FloatField(null=True)
    cantidad = models.PositiveIntegerField(null=True)
    precio = models.FloatField(null=True)
    codigo = models.CharField(max_length=250,null=True)
    informacionAdicional = models.TextField(null=True)
    descuento = models.FloatField(null=True)
    impuesto = models.FloatField(null=True)
    valorDescuento = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(Detalles, self).save(*args, **kwargs)


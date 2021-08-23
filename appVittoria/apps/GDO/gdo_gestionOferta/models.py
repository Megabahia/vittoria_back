from django.db import models

# Create your models here.
from apps.MDM.mdm_negocios.models import Negocios
from apps.MDM.mdm_clientes.models import Clientes

# Create your models here.
class Oferta(models.Model):
    negocio= models.SmallIntegerField(null=True)
    cliente= models.SmallIntegerField(null=True)
    codigoOferta = models.CharField(max_length=150,null=True, blank=True)
    fechaOferta = models.DateField(null=True)
    nombres = models.CharField(max_length=150,null=True)
    apellidos = models.CharField(max_length=150,null=True)
    identificacion = models.CharField(max_length=150,null=True)    
    telefono = models.CharField(max_length=150,null=True)
    correo = models.EmailField(max_length=150,null=True)
    vigenciaOferta = models.IntegerField(max_length=150,null=True)
    canalVentas = models.CharField(max_length=150,null=True)
    calificacionCliente = models.CharField(max_length=150,null=True)
    indicadorCliente = models.CharField(max_length=150,null=True)
    personaGenera = models.CharField(max_length=150,null=True)
    descripcion = models.CharField(max_length=150,null=True)
    total = models.FloatField(null=True)

    fechaCompra = models.DateField(null=True)
    comunicoOferta = models.CharField(max_length=150,null=True, blank=True)
    fechaComunicacion = models.DateField(null=True)
    aceptoOferta = models.CharField(max_length=150,null=True, blank=True)
    fechaAceptacion = models.DateField(null=True)
    calificacionOferta = models.CharField(max_length=150,null=True, blank=True)
    estado = models.CharField(max_length=150,null=True, blank=True)
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(Oferta, self).save(*args, **kwargs)

class OfertaDetalles(models.Model):
    # NOMBRAMOS A LA RELACION DETALLES
    oferta = models.ForeignKey(Oferta, related_name='detalles', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Oferta
    codigo = models.CharField(max_length=150,null=True)
    cantidad = models.SmallIntegerField(null=True)
    producto = models.CharField(max_length=150,null=True)
    precio = models.FloatField(null=True)
    descuento = models.FloatField(null=True)
    total = models.FloatField(null=True)
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(OfertaDetalles, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.id)
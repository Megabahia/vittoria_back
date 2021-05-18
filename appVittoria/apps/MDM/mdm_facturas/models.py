from django.db import models

from apps.MDM.mdm_negocios.models import Negocios
from apps.MDM.mdm_clientes.models import Clientes

# Create your models here.
class FacturasEncabezados(models.Model):
    idNegocio= models.ForeignKey(Negocios, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Negocios
    idCliente= models.ForeignKey(Clientes, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Clientes
    numeroFactura = models.CharField(max_length=150,null=True)
    fecha = models.DateField(null=True)
    idTipoIdentificacion= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    identificacion = models.CharField(max_length=150,null=True)
    razonSocial = models.CharField(max_length=150,null=True)
    direccion = models.CharField(max_length=150,null=True)
    telefono = models.CharField(max_length=150,null=True)
    correo = models.EmailField(max_length=150,null=True)
    nombreVendedor = models.CharField(max_length=150,null=True)
    subTotal = models.DecimalField(max_length=150,null=True)
    descuento = models.DecimalField(max_length=150,null=True)
    iva = models.DecimalField(max_length=150,null=True)
    total = models.DecimalField(max_length=150,null=True)
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(FacturasEncabezados, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)


class FacturasDetalles(models.Model):
    idArticulo = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Negocios
    valorUnitario = models.DecimalField(max_length=150,null=True)
    cantidad = models.PositiveIntegerField(max_length=150,null=True)
    precio = models.DecimalField(max_length=150,null=True)
    informacionAdicinal = models.CharField(max_length=250,null=True)
    descuento = models.DecimalField(max_length=150,null=True)
    impuesto = models.DecimalField(max_length=150,null=True)
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(FacturasDetalles, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)
from django.db import models


def upload_path(instance, filname):
    return '/'.join(['FACTURAS/facturas', str(instance.created_at) + "_" + filname])


class ArchivosFacturas(models.Model):
    archivo = models.FileField(blank=True, null=True, upload_to=upload_path)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(ArchivosFacturas, self).save(*args, **kwargs)


# Create your models here.
class FacturasEncabezados(models.Model):
    numeroPedido = models.CharField(max_length=255, null=True, blank=True)
    estadoPedido = models.CharField(max_length=255, null=True, blank=True)
    fechaPedido = models.DateField(null=True)
    notaCliente = models.CharField(max_length=255, null=True, blank=True)
    nombresFacturacion = models.CharField(max_length=255, null=True, blank=True)
    apellidosFacturacion = models.CharField(max_length=255, null=True, blank=True)
    empresaFacturacion = models.CharField(max_length=255, null=True, blank=True)
    direccionFacturacion = models.CharField(max_length=255, null=True, blank=True)
    ciudadFacturacion = models.CharField(max_length=255, null=True, blank=True)
    provinciaFacturacion = models.CharField(max_length=255, null=True, blank=True)
    codigoPostalFacturacion = models.CharField(max_length=255, null=True, blank=True)
    paisFacturacion = models.CharField(max_length=255, null=True, blank=True)
    correoElectronicoFacturacion = models.CharField(max_length=255, null=True, blank=True)
    telefonoFacturacion = models.CharField(max_length=255, null=True, blank=True)
    nombresEnvio = models.CharField(max_length=255, null=True, blank=True)
    apellidosEnvio = models.CharField(max_length=255, null=True, blank=True)
    direccionEnvio = models.CharField(max_length=255, null=True, blank=True)
    ciudadEnvio = models.CharField(max_length=255, null=True, blank=True)
    provinciaEnvio = models.CharField(max_length=255, null=True, blank=True)
    codigoPostalEnvio = models.CharField(max_length=255, null=True, blank=True)
    paisEnvio = models.CharField(max_length=255, null=True, blank=True)
    metodoPago = models.CharField(max_length=255, null=True, blank=True)
    descuentoCarrito = models.CharField(max_length=255, null=True, blank=True)
    subtotalPedido = models.CharField(max_length=255, null=True, blank=True)
    metodoEnvio = models.CharField(max_length=255, null=True, blank=True)
    importeEnvioPedido = models.CharField(max_length=255, null=True, blank=True)
    importeReemsolsadoPedido = models.CharField(max_length=255, null=True, blank=True)
    importeTotalPedido = models.CharField(max_length=255, null=True, blank=True)
    importeTotalImpuestoPedido = models.CharField(max_length=255, null=True, blank=True)
    estadoSRI = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(FacturasEncabezados, self).save(*args, **kwargs)


class FacturasDetalles(models.Model):
    # NOMBRAMOS A LA RELACION DETALLATES
    facturaEncabezado = models.ForeignKey(FacturasEncabezados, related_name='detalles', null=True, blank=True,
                                          on_delete=models.DO_NOTHING)  # Relacion Factura
    numeroPedido = models.CharField(max_length=255, null=True)
    SKU = models.CharField(max_length=255, null=True)
    articulo = models.CharField(max_length=255, null=True)
    nombreArticulo = models.CharField(max_length=255, null=True)
    cantidad = models.CharField(max_length=255, null=True)
    precio = models.CharField(max_length=255, null=True)
    cupon = models.CharField(max_length=255, null=True)
    importeDescuento = models.CharField(max_length=255, null=True)
    importeImpuestoDescuento = models.CharField(max_length=255, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(FacturasDetalles, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.id)

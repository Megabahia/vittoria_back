from django.db import models


# Create your models here.
class Contactos(models.Model):
    nombres = models.CharField(max_length=150, null=True, blank=True)
    apellidos = models.CharField(max_length=150, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    tipoCliente = models.CharField(max_length=150, null=True, blank=True)
    whatsapp = models.CharField(max_length=150, null=True, blank=True)
    facebook = models.CharField(max_length=150, null=True, blank=True)
    twitter = models.CharField(max_length=150, null=True, blank=True)
    instagram = models.CharField(max_length=150, null=True, blank=True)
    correo1 = models.EmailField(max_length=150, null=True, blank=True)
    correo2 = models.EmailField(max_length=150, null=True, blank=True)
    pais = models.CharField(max_length=255, null=True, blank=True)
    provincia = models.CharField(max_length=255, null=True, blank=True)
    ciudad = models.CharField(max_length=150, null=True, blank=True)
    canal = models.CharField(max_length=150, null=True, blank=True)
    canalOrigen = models.CharField(max_length=255, null=True, blank=True)
    metodoPago = models.CharField(max_length=255, null=True, blank=True)
    codigoProducto = models.CharField(max_length=150, null=True, blank=True)
    nombreProducto = models.TextField(null=True, blank=True)
    precio = models.FloatField(null=True, blank=True)
    tipoPrecio = models.CharField(max_length=250, null=True, blank=True)
    nombreVendedor = models.CharField(max_length=250, null=True, blank=True)
    confirmacionProspecto = models.CharField(max_length=250, null=True, blank=True)
    tipoIdentificacion = models.CharField(max_length=255, null=True, blank=True)
    identificacion = models.CharField(max_length=13, null=True, blank=True)
    nombreCompleto = models.CharField(max_length=255, null=True, blank=True)
    callePrincipal = models.CharField(max_length=255, null=True, blank=True)
    numeroCasa = models.CharField(max_length=255, null=True, blank=True)
    calleSecundaria = models.CharField(max_length=255, null=True, blank=True)
    referencia = models.CharField(max_length=255, null=True, blank=True)
    comentarios = models.CharField(max_length=255, null=True, blank=True)
    comentariosVendedor = models.CharField(max_length=255, null=True, blank=True)
    cantidad = models.IntegerField(default=1)
    subTotal = models.FloatField(null=True)
    descuento = models.FloatField(null=True)
    iva = models.FloatField(null=True)
    total = models.FloatField(null=True)
    courier = models.CharField(max_length=255, null=True, blank=True)
    articulos = models.JSONField(null=True)
    facturacion = models.JSONField(null=True)
    envio = models.JSONField(null=True)

    estado = models.CharField(max_length=100, null=True, blank=True)
    usuario = models.CharField(max_length=200, null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(Contactos, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)

class ContactosDetalles(models.Model):
    # NOMBRAMOS A LA RELACION DETALLATES
    contactoEncabezado = models.ForeignKey(Contactos, related_name='detalles', null=True, blank=True,
                                          on_delete=models.DO_NOTHING)  # Relacion Factura
    articulo = models.CharField(max_length=150, null=True)
    valorUnitario = models.FloatField(null=True)
    cantidad = models.PositiveIntegerField(null=True)
    precio = models.FloatField(null=True)
    codigo = models.CharField(max_length=250, null=True)
    informacionAdicional = models.CharField(max_length=250, null=True)
    descuento = models.FloatField(null=True)
    impuesto = models.FloatField(null=True)
    valorDescuento = models.FloatField(null=True)
    total = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(ContactosDetalles, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.id)

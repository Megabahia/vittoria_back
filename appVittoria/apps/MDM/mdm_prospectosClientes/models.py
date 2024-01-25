from django.db import models


def upload_path(instance, filname):
    return '/'.join(['MDM/prospectosClientes/imgProspectosClientes', str(instance.id) + "_" + filname])


# Create your models here.
class ProspectosClientes(models.Model):
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
    codigoProducto = models.CharField(max_length=150, null=True, blank=True)
    nombreProducto = models.TextField(null=True, blank=True)
    precio = models.FloatField(null=True, blank=True)
    tipoPrecio = models.CharField(max_length=250, null=True, blank=True)
    nombreVendedor = models.CharField(max_length=250, null=True, blank=True)
    confirmacionProspecto = models.CharField(max_length=250, null=True, blank=True)
    imagen = models.ImageField(blank=True, null=True, upload_to=upload_path)
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(ProspectosClientes, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)

class ProspectosClientesDetalles(models.Model):
    # NOMBRAMOS A LA RELACION DETALLATES
    prospectoClienteEncabezado = models.ForeignKey(ProspectosClientes, related_name='detalles', null=True, blank=True,
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
        return super(ProspectosClientesDetalles, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.id)

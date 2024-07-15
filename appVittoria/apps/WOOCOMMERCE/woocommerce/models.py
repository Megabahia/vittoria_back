from django.db import models

def upload_path(instance, filname):
    return '/'.join(['MP/woocommerce/archivosGuia', str(instance.created_at) + "_" + filname])



# Create your models here.
class Pedidos(models.Model):
    estado = models.CharField(max_length=255, null=False)
    envioTotal = models.FloatField(null=True)
    total = models.FloatField(null=True)
    subtotal = models.FloatField(null=True, blank=True)
    facturacion = models.JSONField(null=True)
    envio = models.JSONField(null=True)
    metodoPago = models.CharField(max_length=255, null=False)
    numeroPedido = models.CharField(max_length=255, null=False)
    articulos = models.JSONField(null=True)
    envios = models.JSONField(null=True)
    json = models.JSONField(null=True)
    canal = models.CharField(max_length=255, null=True, blank=True)
    codigoVendedor = models.CharField(max_length=255, null=True, blank=True)
    urlMetodoPago = models.CharField(max_length=255, null=True, blank=True)
    motivo = models.CharField(max_length=255, null=True, blank=True)

    entregoProducto = models.CharField(max_length=255, null=True, blank=True)
    fechaEntrega = models.CharField(max_length=255, null=True, blank=True)
    horaEntrega = models.CharField(max_length=255, null=True, blank=True)
    calificacion = models.CharField(max_length=255, null=True, blank=True)

    metodoConfirmacion = models.CharField(max_length=255, null=True, blank=True)
    codigoConfirmacion = models.CharField(max_length=255, null=True, blank=True)
    fechaHoraConfirmacion = models.CharField(max_length=255, null=True, blank=True)
    tipoFacturacion = models.CharField(max_length=255, null=True, blank=True)

    confirmacionEnvio = models.CharField(max_length=255, null=True, blank=True)
    canalEnvio = models.CharField(max_length=255, null=True, blank=True)
    archivoGuia = models.FileField(blank=True, null=True, upload_to=upload_path)
    fotoEmpaque = models.FileField(blank=True, null=True, upload_to=upload_path)
    videoEmpaque = models.FileField(blank=True, null=True, upload_to=upload_path)
    codigoCourier = models.CharField(max_length=255, null=True, blank=True)
    nombreCourier = models.CharField(max_length=255, null=True, blank=True)
    correoCourier = models.CharField(max_length=255, null=True, blank=True)
    evidenciaFotoEmpaque = models.FileField(blank=True, null=True, upload_to=upload_path)
    evidenciaVideoEmpaque = models.FileField(blank=True, null=True, upload_to=upload_path)
    archivoMetodoPago = models.FileField(blank=True, null=True, upload_to=upload_path)
    verificarPedido = models.BooleanField(default=False)
    numeroGuia = models.CharField(max_length=255, null=True, blank=True)
    verificarGeneracionGuia = models.BooleanField(default=False)
    fechaEmpacado = models.CharField(max_length=255, null=True, blank=True)
    guiServiEntrega = models.FileField(blank=True, null=True, upload_to=upload_path)
    tipoPago = models.CharField(max_length=255, null=True, blank=True)
    tipoEnvio = models.CharField(max_length=255, null=True, blank=True)
    evidenciaPago=models.FileField(blank=True, null=True, upload_to=upload_path)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    fotoCupon = models.FileField(blank=True, null=True, upload_to=upload_path)

    gestion_pedido = models.CharField(max_length=155, blank=True, null=True)
    gestion_despacho = models.CharField(max_length=155, blank=True, null=True)



class Productos(models.Model):

    pedido=models.ForeignKey(Pedidos, related_name='detalles', null=True, blank=True, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=150, null=True, blank=True)
    codigoBarras = models.CharField(max_length=150, null=True, blank=True)
    caracteristicas = models.CharField(max_length=250, null=True, blank=True)
    cantidad = models.PositiveIntegerField(null=True, blank=True)
    precio = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    bodega = models.CharField(max_length=150, null=True, blank=True)
    imagen = models.CharField(max_length=500, null=True, blank=True)

    estado = models.CharField(max_length=150, null=True, blank=True)
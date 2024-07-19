from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import models

from django.db.models import Avg, Min, Max, Count, Sum
import datetime
from django.utils import timezone
# IMPORTAR ENVIO CONFIGURACION CORREO
from apps.config.util2 import sendEmail

from ..mdp_parametrizaciones.models import Parametrizaciones


def upload_path(instance, filname):
    return '/'.join(['MDP/imgProductos', str(instance.id) + "_" + filname])


def upload_path_video(instance, filname):
    return '/'.join(['MDP/videoProductos', str(instance.id) + "_" + filname])


# Create your models here.
class Productos(models.Model):
    categoria = models.CharField(max_length=150, null=True, blank=True)
    subCategoria = models.CharField(max_length=150, null=True, blank=True)
    idPadre = models.CharField(max_length=150, null=True, blank=True)
    nombre = models.CharField(max_length=150, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    codigoBarras = models.CharField(max_length=150, null=True, blank=True)
    refil = models.PositiveIntegerField(null=True, blank=True)
    stock = models.PositiveIntegerField(null=True, blank=True)
    caducidad = models.IntegerField(default=0, null=True, blank=True)
    costoCompra = models.FloatField(null=True, blank=True)
    precioVentaA = models.FloatField(null=True, blank=True)
    precioVentaB = models.FloatField(null=True, blank=True)
    precioVentaC = models.FloatField(null=True, blank=True)
    precioVentaD = models.FloatField(null=True, blank=True)
    precioVentaE = models.FloatField(null=True, blank=True)
    precioVentaF = models.FloatField(null=True, blank=True)
    precioVentaBultos = models.FloatField(null=True, blank=True)
    parametrizacion = models.ForeignKey(Parametrizaciones, null=True, blank=True,
                                        on_delete=models.DO_NOTHING)  # Relacion Con la categoria

    woocommerceId = models.CharField(max_length=150,null=True, blank=True)
    canal = models.CharField(max_length=150, null=True, blank=True)
    stockVirtual = models.JSONField(null=True)


    estado = models.CharField(max_length=150, null=True, default="Inactivo", blank=True)
    variableRefil = models.CharField(max_length=150, null=True, blank=True)
    lote = models.CharField(max_length=150, null=True, blank=True)
    fechaElaboracion = models.DateField(null=True, blank=True)
    fechaCaducidad = models.DateField(null=True, blank=True)
    caracteristicas = models.TextField(null=True, blank=True)
    video = models.FileField(blank=True, null=True, upload_to=upload_path_video)
    precioOferta = models.FloatField(null=True, blank=True)
    envioNivelNacional = models.BooleanField(default=1, blank=True)
    lugarVentaProvincia = models.CharField(max_length=255, null=True, blank=True)
    lugarVentaCiudad = models.CharField(max_length=255, null=True, blank=True)
    courier = models.CharField(max_length=255, null=True, blank=True)
    estadoLanding = models.BooleanField(default=0, blank=True)
    precioLanding = models.FloatField(null=True, blank=True)
    precioLandingOferta = models.FloatField(null=True, blank=True)
    proveedor = models.CharField(max_length=150, null=True, blank=True)

    imagen_principal = models.FileField(blank=True, null=True, upload_to=upload_path)

    tamanio = models.FloatField(null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)

    prefijo = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(Productos, self).save(*args, **kwargs)

    # def __str__(self):
    #     return '{}'.format(self.nombre)


# Create your models here.
class ProductoImagen(models.Model):
    # NOMBRAMOS A LA RELACION DETALLATES    
    producto = models.ForeignKey(Productos, related_name='imagenes', null=True, blank=True,
                                 on_delete=models.DO_NOTHING)  # Relacion Con producto
    imagen = models.FileField(blank=True, null=True, upload_to=upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(ProductoImagen, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.id)


# Create your models here.
class ReporteAbastecimiento(models.Model):
    producto = models.ForeignKey(Productos, null=True, blank=True,
                                 on_delete=models.DO_NOTHING)  # Relacion Con la categoria
    cantidadSugeridaStock = models.IntegerField(null=True)
    fechaMaximaStock = models.DateField(null=True)
    mostrarAviso = models.SmallIntegerField(default=0)
    notificacionEnviada = models.SmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(ReporteAbastecimiento, self).save(*args, **kwargs)


# Create your models here.
class ReporteStock(models.Model):
    producto = models.ForeignKey(Productos, null=True, blank=True,
                                 on_delete=models.DO_NOTHING)  # Relacion Con la categoria
    fechaUltimaStock = models.DateField(null=True)
    montoCompra = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(ReporteStock, self).save(*args, **kwargs)


# Create your models here.
class ReporteCaducidad(models.Model):
    producto = models.ForeignKey(Productos, null=True, blank=True,
                                 on_delete=models.DO_NOTHING)  # Relacion Con la categoria
    fechaCaducidad = models.DateField(null=True)
    productosCaducados = models.IntegerField(null=True)
    diasParaCaducar = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(ReporteCaducidad, self).save(*args, **kwargs)


# Create your models here.
class ReporteRotacion(models.Model):
    producto = models.ForeignKey(Productos, null=True, blank=True,
                                 on_delete=models.DO_NOTHING)  # Relacion Con la categoria
    fechaInicio = models.DateField(null=True)
    fechaFin = models.DateField(null=True)
    diasPeriodo = models.IntegerField(null=True)
    productosVendidos = models.IntegerField(null=True)
    tipoRotacion = models.CharField(max_length=150, null=True)
    montoVenta = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(ReporteRotacion, self).save(*args, **kwargs)


# Create your models here.
class HistorialAvisos(models.Model):
    codigoBarras = models.CharField(max_length=150, null=True)
    fechaCompra = models.DateTimeField(null=True)
    productosVendidos = models.IntegerField(null=True)
    precioVenta = models.FloatField(null=True)
    alerta = models.SmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # TRIGGER ACTUALIZAR STOCK
        # Quita producto
        product = Productos.objects.get(codigoBarras=self.codigoBarras)
        timezone_now = timezone.localtime(timezone.now())
        product.stock -= self.productosVendidos
        product.updated_at = str(timezone_now)
        product.save()
        if product.parametrizacion.valor == 'stock' and product.parametrizacion is not None:
            if product.parametrizacion.minimo < product.stock and product.stock < product.parametrizacion.maximo:
                datos = HistorialAvisos.objects.filter(codigoBarras=self.codigoBarras, alerta=0).aggregate(
                    promedioProductos=Avg('productosVendidos'), fechaMinima=Min('fechaCompra'),
                    fechaMaxima=Max('fechaCompra'), totalRegistros=Count('alerta'))
                if datos['totalRegistros'] != 0:
                    supplyReport = ReporteAbastecimiento.objects.filter(producto=product).order_by('-created_at')[
                                   :1].get()
                    supplyReport.producto = product
                    supplyReport.cantidadSugeridaStock = datos['promedioProductos']
                    supplyReport.mostrarAviso = 1
                    supplyReport.notificacionEnviada = 1
                    daysAvg = ((datos['fechaMaxima'] - datos['fechaMinima']).days) / datos['totalRegistros']
                    maxDate = timezone_now + datetime.timedelta(days=daysAvg)
                    supplyReport.fechaMaximaStock = str(maxDate)
                    supplyReport.save()
                    self.alerta = 1
                    HistorialAvisos.objects.filter(codigoBarras=self.codigoBarras, alerta=0).update(alerta=1)
                    enviarEmailAvisoAbastecimiento(product, maxDate)
        else:
            diasAlerta = (product.fechaCaducidad - datetime.datetime.now().date()).days
            if diasAlerta <= product.parametrizacion.maximo and product.parametrizacion is not None:
                datos = HistorialAvisos.objects.filter(codigoBarras=self.codigoBarras, alerta=0).aggregate(
                    promedioProductos=Avg('productosVendidos'), fechaMinima=Min('fechaCompra'),
                    fechaMaxima=Max('fechaCompra'), totalRegistros=Count('alerta'))
                if datos['totalRegistros'] != 0:
                    supplyReport = ReporteAbastecimiento.objects.filter(producto=product).order_by('-created_at')[
                                   :1].get()
                    supplyReport.producto = product
                    supplyReport.cantidadSugeridaStock = datos['promedioProductos']
                    supplyReport.mostrarAviso = 1
                    supplyReport.notificacionEnviada = 1
                    daysAvg = ((datos['fechaMaxima'] - datos['fechaMinima']).days) / datos['totalRegistros']
                    maxDate = timezone_now + datetime.timedelta(days=daysAvg)
                    supplyReport.fechaMaximaStock = str(maxDate)[0:10]
                    supplyReport.save()
                    self.alerta = 1
                    HistorialAvisos.objects.filter(codigoBarras=self.codigoBarras, alerta=0).update(alerta=1)
                    enviarEmailAvisoAbastecimiento(product, maxDate)
        # AUMENTAR VENTA ROTACION
        rotacion = ReporteRotacion.objects.filter(producto=product).order_by('-created_at')[:1].get()
        rotacion.productosVendidos += self.productosVendidos
        rotacion.montoVenta += self.precioVenta
        consulta = IngresoProductos.objects.filter(created_at__gte=str(rotacion.fechaInicio),
                                                   created_at__lte=str(rotacion.fechaFin)).aggregate(
            promedioInventario=Avg('cantidad'))
        resultadoRotacion = rotacion.montoVenta / consulta["promedioInventario"] if consulta[
                                                                                        "promedioInventario"] != None else 0
        tipoRotacion = Parametrizaciones.objects.filter(tipo="TIPO_ROTACION",
                                                        maximo__lte=int(resultadoRotacion)).order_by('-maximo')[
                       :1].get()
        rotacion.tipoRotacion = tipoRotacion.nombre
        rotacion.save()
        # FIN TRIGGER ACTUALIZAR STOCK
        return super(HistorialAvisos, self).save(*args, **kwargs)


# Create your models here.
class IngresoProductos(models.Model):
    producto = models.ForeignKey(Productos, null=True, blank=True,
                                 on_delete=models.DO_NOTHING)  # Relacion Con la categoria
    cantidad = models.IntegerField(null=True)
    fechaElaboracion = models.DateField(null=True)
    fechaCaducidad = models.DateField(null=True)
    precioCompra = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(IngresoProductos, self).save(*args, **kwargs)


def enviarEmailAvisoAbastecimiento(product, maxDate):
    try:
        # enviar por email
        subject, from_email, to = 'Aviso de abastecimiento', "1760ab7178-1f5a2f@inbox.mailtrap.io", 'jsyar@pucesi.edu.ec'
        txt_content = """
                Alerta de abastecimiento Vittoria
                
                Aviso de stock inferior """ + str(product.stock) + """ """ + str(
            product.stock) + """ del producto """ + str(
            product.nombre) + """ se aconseja que la fecha maxima de reponer es """ + str(
            maxDate.strftime('%Y-%m-%d')) + """
                Atentamente,
                Equipo Vittoria.
        """
        html_content = """
        <html>
            <body>
                <h1>Alerta de abastecimiento Vittoria</h1>
                
                <br>
                Aviso de stock inferior a """ + str(product.stock) + """ del producto """ + str(
            product.nombre) + """ se aconseja que la fecha maxima de reponer es """ + str(
            maxDate.strftime('%Y-%m-%d')) + """<br>
                Atentamente,<br>
                Equipo Vittoria.<br>
            </body>
        </html>
        """
        if sendEmail(subject, txt_content, from_email, to, html_content):
            return True
        return False
    except:
        return False


@receiver(post_save, sender=Productos)
def createTablesReport(sender, instance, **kwargs):
    timezone_now = timezone.localtime(timezone.now())
    # CREAR INGRESO PRODUCTOS
    ingresoProductos = IngresoProductos.objects.filter(producto=instance, state=1).first()
    if ingresoProductos is None and instance.fechaElaboracion is not None and instance.fechaCaducidad is not None:
        IngresoProductos.objects.create(cantidad=instance.stock, fechaElaboracion=str(instance.fechaElaboracion),
                                        fechaCaducidad=str(instance.fechaCaducidad), precioCompra=instance.costoCompra,
                                        producto=instance)
    # CREAR REPORTE STOCK
    reporteStock = ReporteStock.objects.filter(producto=instance, state=1).first()
    if reporteStock is None and datetime.datetime.now().date() is not None:
        ReporteStock.objects.create(fechaUltimaStock=str(datetime.datetime.now().date()),
                                    montoCompra=instance.costoCompra, producto=instance)
    # CREAR REPORTE ABASTECIMIENTO
    reporteAbastecimiento = ReporteAbastecimiento.objects.filter(producto=instance, state=1).first()
    if reporteAbastecimiento is None:
        ReporteAbastecimiento.objects.create(cantidadSugeridaStock=0, state=1, producto=instance)
    # CREAR REPORTE ROTACION PRODUCTOS
    diasPeriodo = 7
    fechaFin = timezone_now + datetime.timedelta(days=diasPeriodo)
    reporteRotacion = ReporteRotacion.objects.filter(producto=instance, fechaFin__lte=fechaFin).first()
    if reporteRotacion is None and timezone_now is not None and fechaFin is not None:
        ReporteRotacion.objects.create(fechaInicio=str(timezone_now)[0:10], fechaFin=str(fechaFin)[0:10],
                                       diasPeriodo=diasPeriodo, productosVendidos=0, tipoRotacion="Bajo", montoVenta=0,
                                       producto=instance)
    ingresoProducto = IngresoProductos.objects.filter(fechaCaducidad__lte=str(datetime.datetime.now().date()), state=1,
                                                      producto=instance.id).aggregate(
        productosCaducados=Sum("cantidad"))
    if instance.fechaCaducidad != None:
        ahora = instance.fechaCaducidad
        if isinstance(ahora, str):
            datetimeobj = datetime.datetime.strptime(ahora, "%Y-%m-%d")
            diasParaCaducar = (datetimeobj - timezone_now.replace(tzinfo=None)).days
        else:
            diasParaCaducar = (ahora - datetime.datetime.now().date()).days
    else:
        diasParaCaducar = 0
    # CREAR REPORTE CADUCIDAD
    reporteCaducidad = ReporteCaducidad.objects.filter(producto=instance, state=1).first()
    if reporteCaducidad is None and instance.fechaCaducidad is not None:
        ReporteCaducidad.objects.create(fechaCaducidad=instance.fechaCaducidad,
                                        productosCaducados=ingresoProducto["productosCaducados"],
                                        diasParaCaducar=diasParaCaducar, producto=instance)
    return

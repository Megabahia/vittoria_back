from django.db import models

from django.db.models import Avg, Min, Max, Count
import datetime
from django.utils import timezone
#lib email
from apps.config.util import sendEmail

from apps.MDP.mdp_parametrizaciones.models import Parametrizaciones

def upload_path(instance, filname):
    return '/'.join(['MDP/imgProductos', str(instance.producto.id) +"_" + filname])

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
    parametrizacion= models.ForeignKey(Parametrizaciones, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con la categoria
    estado = models.CharField(max_length=150,null=True)
    variableRefil = models.CharField(max_length=150,null=True)

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
    producto= models.ForeignKey(Productos, related_name='imagenes', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con producto
    imagen=models.ImageField(blank=True,null=True,upload_to=upload_path)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(ProductoImagen, self).save(*args, **kwargs)
    
    def __str__(self):
        return '{}'.format(self.id)

# Create your models here.
class ReporteAbastecimiento(models.Model):
    producto= models.ForeignKey(Productos, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con la categoria
    cantidadSugeridaStock = models.CharField(max_length=150,null=True)
    fechaMaximaStock = models.DateTimeField(null=True)
    mostrarAviso = models.SmallIntegerField(default=0)
    notificacionEnviada = models.SmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(ReporteAbastecimiento, self).save(*args, **kwargs)

# Create your models here.
class ReporteStock(models.Model):
    producto= models.ForeignKey(Productos, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con la categoria
    fechaUltimaStock = models.DateTimeField(null=True)
    montoCompra = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(ReporteStock, self).save(*args, **kwargs)

# Create your models here.
class ReporteCaducidad(models.Model):
    producto= models.ForeignKey(Productos, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con la categoria
    fechaCaducidad = models.DateTimeField(null=True)
    productosCaducados = models.IntegerField(max_length=150,null=True)
    diasParaCaducar = models.IntegerField(max_length=150,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(ReporteCaducidad, self).save(*args, **kwargs)

# Create your models here.
class ReporteRotacion(models.Model):
    producto= models.ForeignKey(Productos, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con la categoria
    fechaInicio = models.DateTimeField(null=True)
    fechaFin = models.DateTimeField(null=True)
    diasPeriodo = models.IntegerField(max_length=150,null=True)
    productosVendidos = models.IntegerField(max_length=150,null=True)
    tipoRotacion = models.CharField(max_length=150,null=True)
    montoVenta = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(ReporteRotacion, self).save(*args, **kwargs)
    
# Create your models here.
class HistorialAvisos(models.Model):
    codigoBarras = models.CharField(max_length=150,null=True)
    fechaCompra = models.DateTimeField(null=True)
    productosVendidos = models.IntegerField(max_length=150,null=True)
    alerta = models.SmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # TRIGGER ACTUALIZAR STOCK
        product = Productos.objects.get(codigoBarras=self.codigoBarras)
        timezone_now = timezone.localtime(timezone.now())
        product.stock -= self.productosVendidos
        product.updated_at = str(timezone_now)
        product.save()
        if product.parametrizacion.valor == 'stock':
            if product.parametrizacion.minimo < product.stock and product.stock < product.parametrizacion.maximo:
                datos = HistorialAvisos.objects.filter(codigoBarras=self.codigoBarras,alerta=0).aggregate(promedioProductos=Avg('productosVendidos'),fechaMinima=Min('fechaCompra'),fechaMaxima=Max('fechaCompra'),totalRegistros=Count('alerta'))                
                supplyReport = ReporteAbastecimiento.objects.get(producto=product)
                supplyReport.cantidadSugeridaStock = datos['promedioProductos']
                supplyReport.mostrarAviso = 1
                supplyReport.notificacionEnviada = 1
                daysAvg = ((datos['fechaMaxima'] - datos['fechaMinima']).days) / datos['totalRegistros']
                maxDate = timezone_now + datetime.timedelta(days=daysAvg)
                supplyReport.fechaMaximaStock = str(maxDate)
                supplyReport.save()
                self.alerta = 1
                HistorialAvisos.objects.filter(codigoBarras=self.codigoBarras,alerta=0).update(alerta=1)
                enviarEmailAsignacionPassword(product)
        else:
            print("Dias")
        # FIN TRIGGER ACTUALIZAR STOCK
        return super(HistorialAvisos, self).save(*args, **kwargs)
    
def enviarEmailAsignacionPassword(product):
    try:
        #enviar por email            
        subject, from_email, to = 'Solicitud de Reinicio de contraseña Viitoria', "73ddd8bfb3-995a16@inbox.mailtrap.io",'jimmy1817@hotmail.com'
        txt_content="""
                Alerta de abastecimiento Vittoria
                
                Si al hacer click en el enlace anterior no funciona, copie y pegue la URL en una nueva ventana del navegador
                Atentamente,
                Equipo Vittoria.
        """
        html_content = """
        <html>
            <body>
                <h1>Alerta de abastecimiento Vittoria</h1>
                Haga clic en el siguiente enlace para registrar su contraseña:<br>
                <br>
                Si al hacer click en el enlace anterior no funciona, copie y pegue la URL en una nueva ventana del navegador<br>
                Atentamente,<br>
                Equipo Vittoria.<br>
            </body>
        </html>
        """
        if sendEmail():
            return True
        return False
    except:
        return False
    


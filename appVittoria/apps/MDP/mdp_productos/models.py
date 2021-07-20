from django.db import models

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
    alertaAbastecimiento = models.CharField(max_length=150,null=True)
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
    


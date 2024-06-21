from django.db import models


def upload_path(instance, filname):
    return '/'.join(['GDP/productos', str(instance.producto.id) + "_" + filname])


class Productos(models.Model):
    titulo = models.TextField(null=True)
    subtitulo = models.TextField(null=True)
    precio = models.FloatField(null=True)
    codigo = models.CharField(max_length=150, null=True)
    stock = models.IntegerField(null=True)
    precioOferta = models.FloatField(null=True)
    descripcion = models.TextField(null=True)
    caracteristicas = models.TextField(null=True)
    estado = models.CharField(max_length=150, null=True, default="Inactivo")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(Productos, self).save(*args, **kwargs)

    # def __str__(self):
    #     return '{}'.format(self.nombre)


class ProductoArchivos(models.Model):
    # NOMBRAMOS A LA RELACION DETALLATES
    producto = models.ForeignKey(Productos, related_name='imagenes', null=True, blank=True,
                                 on_delete=models.DO_NOTHING)  # Relacion Con producto
    archivo = models.FileField(blank=True, null=True, upload_to=upload_path)
    tipo = models.CharField(max_length=150, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(ProductoArchivos, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.id)

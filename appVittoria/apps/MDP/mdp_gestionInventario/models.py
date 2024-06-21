from django.db import models


def upload_path(instance, filname):
    return '/'.join(['MDP/gestionInventario/archivos', str(instance.created_at) + "_" + filname])


class ArchivosFacturas(models.Model):
    archivo = models.FileField(blank=True, null=True, upload_to=upload_path)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super(ArchivosFacturas, self).save(*args, **kwargs)


class Productos(models.Model):
    fechaAdquisicion = models.CharField(max_length=255, null=True, blank=True)
    codigoBarras = models.CharField(max_length=255, null=True, blank=True)
    nombreProducto = models.CharField(max_length=255, null=True, blank=True)
    proveedor = models.CharField(max_length=255, null=True, blank=True)
    precioAdquisicion = models.CharField(max_length=255, null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True, default=0)
    imagen = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)


class ProductosImagenes(models.Model):
    producto = models.CharField(max_length=255, null=True, blank=True)
    imagen = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

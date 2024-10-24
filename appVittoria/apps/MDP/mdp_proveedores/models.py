from django.db import models


def upload_path(instance, filname):
  return '/'.join(['MDP/imgProveedor', str(instance.id) + "_" + filname])

class Proveedores(models.Model):
  nombre = models.CharField(max_length=150, null=True, blank=True)
  apellido = models.CharField(max_length=150, null=True, blank=True)
  pais = models.CharField(max_length=150, null=True, blank=True)
  provincia = models.CharField(max_length=150, null=True, blank=True)
  ciudad = models.CharField(max_length=150, null=True, blank=True)
  telefono = models.CharField(max_length=15, null=True, blank=True)
  codigo = models.CharField(max_length=15, null=True, blank=True)
  imagen = models.FileField(blank=True, null=True, upload_to=upload_path)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True)
  state = models.SmallIntegerField(default=1)
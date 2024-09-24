from django.db import models
# Create your models here.
from ...ADM.vittoria_usuarios.models import Usuarios

def upload_path(instance, filname):
  return '/'.join(['MDM/archivosAsesor', str(instance.nombres) + "_" + filname])


class AsesoresComerciales(models.Model):
  usuario = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)
  canal = models.CharField(max_length=250, blank=True, null=True)
  imagen = models.ImageField(blank=True, null=True, upload_to=upload_path)
  nombres = models.CharField(max_length=150, blank=True, null=True)
  apellidos = models.CharField(max_length=250, blank=True, null=True)
  email = models.EmailField(max_length=255, unique=False)
  estado = models.CharField(max_length=200)
  gender = models.CharField(max_length=50, blank=True, null=True)
  pais = models.CharField(max_length=200)
  provincia = models.CharField(max_length=200, blank=True, null=True)
  ciudad = models.CharField(max_length=200, blank=True, null=True)
  whatsapp = models.CharField(max_length=30)
  created_at = models.DateTimeField(auto_now_add=True)
  fecha_nacimiento = models.DateTimeField(null=True)
  updated_at = models.DateTimeField(null=True)
  state = models.SmallIntegerField(default=1)

  saldo_asesor = models.FloatField(null=True)

  nombre_banco = models.CharField(max_length=100, blank=True, null=True)
  numero_cuenta = models.CharField(max_length=13,blank=True, null=True)
  tipo_cuenta = models.CharField(max_length=100,blank=True, null=True)
  identificacion = models.CharField(max_length=13,null=True)
  archivoCedula = models.FileField(blank=True, null=True, upload_to=upload_path)

  movimientos = models.JSONField(null=True)


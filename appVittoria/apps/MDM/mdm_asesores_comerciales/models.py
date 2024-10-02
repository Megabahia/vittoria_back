from django.db import models
# Create your models here.
from ...ADM.vittoria_usuarios.models import Usuarios

def upload_path(instance, filname):
  return '/'.join(['MDM/archivosAsesor', str(instance.asesor.nombres) + "_" + filname])


class AsesoresComerciales(models.Model):
  usuario = models.IntegerField(blank=True, null=True)
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
  observaciones = models.CharField(max_length=400, blank=True, null=True)
  numeroPedido = models.CharField(max_length=255,blank=True, null=False)

  nombre_banco = models.CharField(max_length=100, blank=True, null=True)
  numero_cuenta = models.CharField(max_length=13,blank=True, null=True)
  tipo_cuenta = models.CharField(max_length=100,blank=True, null=True)
  identificacion = models.CharField(max_length=13,null=True)
  tipoIdentificacion = models.CharField(max_length=255, null=True, blank=True)
  archivoCedula = models.FileField(blank=True, null=True, upload_to=upload_path)

class MovimientosAsesores(models.Model):
  asesor = models.ForeignKey(AsesoresComerciales, null=False, on_delete=models.CASCADE)
  tipo_movimiento = models.CharField(max_length=250, blank=True, null=True)
  saldo = models.FloatField(blank=True,null=True)
  saldo_ingreso = models.FloatField(blank=True,null=True)
  saldo_egreso = models.FloatField(blank=True,null=True)
  saldo_total = models.FloatField(blank=True,null=True)
  observaciones = models.CharField(max_length=400, blank=True, null=True)
  archivo_comprobante = models.FileField(blank=True, null=True, upload_to=upload_path)
  numero_transaccion = models.CharField(max_length=100, blank=True, null=True)

  created_at = models.DateTimeField(auto_now_add=True)
  state = models.SmallIntegerField(default=1)



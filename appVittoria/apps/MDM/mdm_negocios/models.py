from django.db import models

# Create your models here.
class Negocios(models.Model):
    idTipoNegocio= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    ruc = models.CharField(max_length=150,null=True)
    razonSocial = models.CharField(max_length=150,null=True)
    nombreComercial = models.CharField(max_length=150,null=True)    
    idNacionalidad= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    fechaCreacionNegocio = models.DateField(max_length=150,null=True)
    edadNegocio = models.CharField(max_length=150,null=True)
    idPaisOrigen= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idPaisResidencia= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idProvinciaResidencia= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idCiudadResidencia= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    numeroEmpleados = models.CharField(max_length=150,null=True)
    idSegmentoActividadEconomica= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idProvincia= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idActividadEcomica= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    llevarContabilidad = models.SmallIntegerField(default=1)
    ingresosPromedioMensual = models.CharField(max_length=150,null=True)
    gastosPromedioMensual = models.CharField(max_length=150,null=True)
    numeroEstablecimientos = models.CharField(max_length=20,null=True)
    telefonoOficina = models.CharField(max_length=150,null=True)
    celularOficina = models.CharField(max_length=150,null=True)
    celularPersonal = models.CharField(max_length=150,null=True)
    whatsappPersonal = models.CharField(max_length=150,null=True)
    whatsappSecundario = models.CharField(max_length=150,null=True)
    correoPersonal = models.CharField(max_length=150,null=True)
    correoOficina = models.CharField(max_length=150,null=True)
    googlePlus = models.CharField(max_length=150,null=True)
    twitter = models.CharField(max_length=150,null=True)
    facebook = models.CharField(max_length=150,null=True)
    instagram = models.CharField(max_length=150,null=True)
    foto = models.CharField(max_length=150,null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(Negocios, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)

class DireccionesEstablecimientosNegocios(models.Model):
    idNegocio= models.ForeignKey(Negocios, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Negocios
    idTipoDireccion= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idPais= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idProvincia= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idCiudad= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    callePrincipal = models.CharField(max_length=150,null=True)
    numero = models.CharField(max_length=20,null=True)
    calleSecundaria = models.CharField(max_length=150,null=True)
    edificio = models.CharField(max_length=150,null=True)
    piso = models.CharField(max_length=150,null=True)
    oficina = models.CharField(max_length=150,null=True)
    referencia = models.CharField(max_length=250,null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(DireccionesEstablecimientosNegocios, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)

class PersonalNegocios(models.Model):
    idNegocio= models.ForeignKey(Negocios, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Negocios
    idTipoContacto= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    cedula = models.CharField(max_length=10,null=True)
    nombres = models.CharField(max_length=150,null=True)
    apellidos = models.CharField(max_length=150,null=True)
    telefonoFijo = models.CharField(max_length=15,null=True)
    extension = models.CharField(max_length=15,null=True)
    celularEmpresa = models.CharField(max_length=15,null=True)
    whatsappEmpresa = models.CharField(max_length=15,null=True)
    celularPersonal = models.CharField(max_length=15,null=True)
    whatsappPersonal = models.CharField(max_length=15,null=True)
    correoEmpresa = models.CharField(max_length=150,null=True)
    correoPersonal = models.CharField(max_length=150,null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(PersonalNegocios, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)
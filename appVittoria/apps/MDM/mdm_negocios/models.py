from django.db import models

def upload_path(instance, filname):
    return '/'.join(['MDM/imgNegocios', str(instance.id) +"_" + filname])

# Create your models here.
class Negocios(models.Model):
    tipoNegocio = models.CharField(max_length=150,null=True)
    ruc = models.CharField(max_length=150,null=True, unique=True)
    razonSocial = models.CharField(max_length=150,null=True)
    nombreComercial = models.CharField(max_length=150,null=True)    
    nacionalidad = models.CharField(max_length=150,null=True)
    fechaCreacionNegocio = models.DateField(max_length=150,null=True)
    edadNegocio = models.CharField(max_length=150,null=True)
    paisOrigen= models.CharField(max_length=150,null=True)
    paisResidencia= models.CharField(max_length=150,null=True)
    provinciaResidencia = models.CharField(max_length=150,null=True)
    ciudadResidencia= models.CharField(max_length=150,null=True)
    numeroEmpleados = models.CharField(max_length=150,null=True)
    segmentoActividadEconomica= models.CharField(max_length=150,null=True)
    provincia= models.CharField(max_length=150,null=True)
    actividadEcomica= models.CharField(max_length=150,null=True)
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
    imagen=models.ImageField(blank=True,null=True,upload_to=upload_path)
    estado=models.CharField(max_length=200,default="Inactivo")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(Negocios, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)

class DireccionesEstablecimientosNegocios(models.Model):
    negocio= models.ForeignKey(Negocios, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Negocios
    tipoDireccion= models.CharField(max_length=150,null=True)
    pais= models.CharField(max_length=150,null=True)
    provincia= models.CharField(max_length=150,null=True)
    ciudad= models.CharField(max_length=150,null=True)
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
    negocio= models.ForeignKey(Negocios, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Negocios
    tipoContacto = models.CharField(max_length=150,null=True)
    cedula = models.CharField(max_length=10,null=True, unique= True)
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
    estado=models.CharField(max_length=200,default="Inactivo")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(PersonalNegocios, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)
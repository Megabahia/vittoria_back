from django.db import models

def upload_path(instance, filname):
    return '/'.join(['MDM/imgClientes', str(instance.id) +"_" + filname])

# Create your models here.
class Clientes(models.Model):
    tipoCliente = models.CharField(max_length=150,null=True)
    cedula = models.CharField(max_length=10,null=True,unique=True)
    nombres = models.CharField(max_length=150,null=True)
    apellidos = models.CharField(max_length=150,null=True)
    genero= models.CharField(max_length=150,null=True)
    nacionalidad= models.CharField(max_length=150,null=True)
    fechaNacimiento = models.DateField(null=True)
    edad = models.SmallIntegerField(null=True)
    paisNacimiento= models.CharField(max_length=150,null=True)
    provinciaNacimiento= models.CharField(max_length=150,null=True)
    ciudadNacimiento= models.CharField(max_length=150,null=True)
    estadoCivil= models.CharField(max_length=150,null=True)
    paisResidencia= models.CharField(max_length=150,null=True)
    provinciaResidencia= models.CharField(max_length=150,null=True)
    ciudadResidencia= models.CharField(max_length=150,null=True)
    nivelEstudios= models.CharField(max_length=150,null=True)
    profesion= models.CharField(max_length=150,null=True)
    lugarTrabajo = models.CharField(max_length=150,null=True)
    paisTrabajo= models.CharField(max_length=150,null=True)
    provinciaTrabajo= models.CharField(max_length=150,null=True)
    ciudadTrabajo= models.CharField(max_length=150,null=True)
    mesesUltimoTrabajo = models.PositiveIntegerField(null=True)
    mesesTotalTrabajo = models.PositiveIntegerField (null=True)
    ingresosPromedioMensual = models.FloatField()
    gastosPromedioMensual = models.FloatField()
    imagen=models.ImageField(blank=True,null=True,upload_to=upload_path)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(Clientes, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)

class DatosFisicosClientes(models.Model):
    cliente= models.ForeignKey(Clientes, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con el cliente
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
    referencia = models.CharField(max_length=150,null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(DatosFisicosClientes, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)

class DatosVirtualesClientes(models.Model):
    cliente= models.ForeignKey(Clientes, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con el cliente
    tipoContacto= models.CharField(max_length=150,null=True)
    informacion = models.CharField(max_length=150,null=True)
    icono = models.CharField(max_length=150,null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(DatosVirtualesClientes, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)

class Parientes(models.Model):
    tipoPariente= models.CharField(max_length=150,null=True)
    cedula = models.CharField(max_length=10,null=True,unique=True)
    nombres = models.CharField(max_length=150,null=True)
    apellidos = models.CharField(max_length=150,null=True)
    fechaMatrimonio = models.DateField(null=True)
    lugarMatrimonio = models.CharField(max_length=150,null=True)
    genero= models.CharField(max_length=150,null=True)
    nacionalidad= models.CharField(max_length=150,null=True)
    fechaNacimiento = models.DateField(null=True)
    edad = models.PositiveSmallIntegerField(null=True)
    paisNacimiento= models.CharField(max_length=150,null=True)
    provinciaNacimiento= models.CharField(max_length=150,null=True)
    ciudadNacimiento= models.CharField(max_length=150,null=True)
    estadoCivil= models.CharField(max_length=150,null=True)
    paisResidencia= models.CharField(max_length=150,null=True)
    provinciaResidencia= models.CharField(max_length=150,null=True)
    ciudadResidencia= models.CharField(max_length=150,null=True)
    callePrincipal = models.CharField(max_length=150,null=True)
    numero = models.CharField(max_length=20,null=True)
    calleSecundaria = models.CharField(max_length=150,null=True)
    edificio = models.CharField(max_length=150,null=True)
    piso = models.CharField(max_length=150,null=True)
    departamento = models.CharField(max_length=150,null=True)
    telefonoDomicilio = models.CharField(max_length=15,null=True)
    telefonoOficina = models.CharField(max_length=15,null=True)
    celularPersonal = models.CharField(max_length=15,null=True)
    celularOficina = models.CharField(max_length=15,null=True)
    whatsappPersonal = models.CharField(max_length=150,null=True)
    whatsappSecundario = models.CharField(max_length=150,null=True)
    correoPersonal = models.EmailField(max_length=150,null=True)
    correoTrabajo = models.EmailField(max_length=150,null=True)
    googlePlus = models.EmailField(max_length=150,null=True)
    twitter = models.CharField(max_length=150,null=True)
    facebook = models.CharField(max_length=150,null=True)
    instagram = models.CharField(max_length=150,null=True)
    nivelEstudios= models.CharField(max_length=150,null=True)
    profesion= models.CharField(max_length=150,null=True)
    lugarTrabajo = models.CharField(max_length=150,null=True)
    paisTrabajo= models.CharField(max_length=150,null=True)
    provinciaTrabajo= models.CharField(max_length=150,null=True)
    ciudadTrabajo= models.CharField(max_length=150,null=True)
    mesesUltimoTrabajo = models.PositiveIntegerField(null=True)
    mesesTotalTrabajo = models.PositiveIntegerField(null=True)
    ingresosPromedioMensual = models.FloatField()
    gastosPromedioMensual = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(Parientes, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)
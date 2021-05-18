from django.db import models

# Create your models here.
class Clientes(models.Model):
    idTipoCliente= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    cedula = models.CharField(max_length=10,null=True)
    nombres = models.CharField(max_length=150,null=True)
    apellidos = models.CharField(max_length=150,null=True)
    idGenero= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idNacionalidad= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    fechaNacimiento = models.DateField(null=True)
    edad = models.SmallIntegerField(null=True)
    idPaisNacimiento= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idProvinciaNacimiento= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idCiudadNacimiento= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idEstadoCivil= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idPaisResidencia= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idProvinciaResidencia= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idCiudadResidencia= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idNivelEstudios= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idProfesion= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    lugarTrabajo = models.CharField(max_length=150,null=True)
    idPaisTrabajo= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idProvinciaTrabajo= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idCiudadTrabajo= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    mesesUltimoTrabajo = models.PositiveIntegerField(null=True)
    mesesTotalTrabajo = models.PositiveIntegerField (null=True)
    ingresosPromedioMensual = models.DecimalField(null=True)
    gastosPromedioMensual = models.DecimalField(null=True)
    foto = models.CharField(max_length=250,null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(Clientes, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)

class DatosFisicosClientes(models.Model):
    idCliente= models.ForeignKey(Clientes, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con el cliente
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
    idCliente= models.ForeignKey(Clientes, null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Con el cliente
    idTipoContacto= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
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
    idTipoPariente= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    cedula = models.CharField(max_length=10,null=True)
    nombres = models.CharField(max_length=150,null=True)
    apellidos = models.CharField(max_length=150,null=True)
    fechaMatrimonio = models.DateField(null=True)
    lugarMatrimonio = models.CharField(max_length=150,null=True)
    idGenero= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idNacionalidad= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    fechaNacimiento = models.DateField(null=True)
    edad = models.PositiveSmallIntegerField(null=True)
    idPaisNacimiento= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idProvinciaNacimiento= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idCiudadNacimiento= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idEstadoCivil= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idPaisResidencia= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idProvinciaResidencia= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idCiudadResidencia= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
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
    idNivelEstudios= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idProfesion= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    lugarTrabajo = models.CharField(max_length=150,null=True)
    idPaisTrabajo= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idProvinciaTrabajo= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    idCiudadTrabajo= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    mesesUltimoTrabajo = models.PositiveIntegerField(null=True)
    mesesTotalTrabajo = models.PositiveIntegerField(null=True)
    ingresosPromedioMensual = models.DecimalField(null=True)
    gastosPromedioMensual = models.DecimalField(null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(Parientes, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)
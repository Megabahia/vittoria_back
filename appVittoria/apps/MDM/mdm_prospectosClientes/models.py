from django.db import models

def upload_path(instance, filname):
    return '/'.join(['MDM/prospectosClientes/imgProspectosClientes', str(instance.id) +"_" + filname])

# Create your models here.
class ProspectosClientes(models.Model):
    nombres = models.CharField(max_length=150,null=True)
    apellidos = models.CharField(max_length=150,null=True)
    telefono = models.CharField(max_length=15,null=True)
    tipoCliente= models.CharField(max_length=150,null=True)
    whatsapp = models.CharField(max_length=150,null=True)
    facebook = models.CharField(max_length=150,null=True)
    twitter = models.CharField(max_length=150,null=True)
    instagram = models.CharField(max_length=150,null=True)
    correo1 = models.EmailField(max_length=150,null=True)
    correo2 = models.EmailField(max_length=150,null=True)
    ciudad = models.CharField(max_length=150,null=True)
    canal = models.CharField(max_length=150,null=True)
    codigoProducto = models.CharField(max_length=150,null=True)
    nombreProducto = models.CharField(max_length=150,null=True)
    precio = models.FloatField(null=True)
    tipoPrecio = models.CharField(max_length=250,null=True)
    nombreVendedor = models.CharField(max_length=250,null=True)
    confirmacionProspecto = models.CharField(max_length=250,null=True)
    imagen=models.ImageField(blank=True,null=True,upload_to=upload_path)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)  

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(ProspectosClientes, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombres)

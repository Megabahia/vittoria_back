from django.db import models

# Create your models here.
class Parametros(models.Model):
    idPadre= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    nombre = models.CharField(max_length=150,null=True)
    tipo = models.CharField(max_length=150,null=True)
    tipoVariable = models.CharField(max_length=150,null=True)
    valor = models.CharField(max_length=150,null=True)
    descripcion = models.CharField(max_length=250,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        # self.tipo = self.tipo.upper()
        return super(Parametros, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombre)
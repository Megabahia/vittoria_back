from django.db import models

# Create your models here.
class Catalogo(models.Model):
    idPadre= models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    codigo = models.CharField(max_length=150,null=True)
    tipo = models.CharField(max_length=150,null=True)
    nombre = models.CharField(max_length=150,null=False)
    descripcion = models.CharField(max_length=250,null=True)
    config = models.TextField(default='{}')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.nombre)
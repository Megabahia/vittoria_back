from django.db import models

# Create your models here.
class GdParametrizaciones(models.Model):
    nombre = models.CharField(max_length=150,null=True)
    tipo = models.CharField(max_length=150,null=False)
    tipoVariable = models.CharField(max_length=150,null=False)
    valor = models.CharField(max_length=150,null=False)
    descripcion = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        self.tipo = self.tipo.upper()
        return super(GdParametrizaciones, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombre)
from django.db import models


# Create your models here.
class Roles(models.Model):
    codigo = models.CharField(max_length=150,null=True)
    nombre = models.CharField(unique=True,max_length=150,null=False)
    descripcion = models.CharField(max_length=250, null=True)
    config = models.TextField(default='{}')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.nombre)

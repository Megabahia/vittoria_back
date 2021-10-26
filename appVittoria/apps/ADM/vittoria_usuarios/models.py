
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,UserManager
from apps.ADM.vittoria_roles.models import Roles

def upload_path(instance, filname):
    return '/'.join(['ADM/imgUsuarios', str(instance.username) +"_" + filname])

# Create your models here.
class Usuarios(AbstractBaseUser):
    username = models.CharField(max_length=150,unique=True)
    imagen=models.ImageField(blank=True,null=True,upload_to=upload_path)
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=250)
    email = models.EmailField(max_length=255,unique=True)
    estado=models.CharField(max_length=200)
    idRol = models.ForeignKey(Roles, null=False, on_delete=models.CASCADE)  # Relacion Rol
    pais=models.CharField(max_length=200)
    telefono = models.CharField(max_length=30)
    whatsapp=models.CharField(max_length=30)
    compania=models.CharField(max_length=200)
    twitter=models.CharField(max_length=200)
    facebook=models.CharField(max_length=200)
    instagram=models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()
 


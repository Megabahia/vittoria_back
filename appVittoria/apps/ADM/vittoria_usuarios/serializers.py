from rest_framework import serializers
from import_export import resources

from .models import Usuarios
from ..vittoria_roles.serializers import RolFiltroSerializer


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        exclude = ('password',)


class UsuarioRolSerializer(serializers.ModelSerializer):
    idRol = RolFiltroSerializer(many=False, read_only=True)

    class Meta:
        model = Usuarios
        exclude = ('password',)

    def to_representation(self, instance):
        data = super(UsuarioRolSerializer, self).to_representation(instance)
        rol = data.pop('idRol')
        for key, val in rol.items():
            data.update({"rol" + key.lower().capitalize(): val})
        return data


class UsuarioCrearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ['nombres', 'apellidos', 'username', 'email', 'compania', 'pais', 'telefono', 'whatsapp', 'idRol',
                  'password', 'estado', 'imagen', 'canal']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        usuario = Usuarios(
            nombres=self.validated_data['nombres'],
            apellidos=self.validated_data['apellidos'],
            username=self.validated_data['username'],
            canal=self.validated_data['canal'],
            email=self.validated_data['email'],
            compania=self.validated_data['compania'],
            pais=self.validated_data['pais'],
            telefono=self.validated_data['telefono'],
            whatsapp=self.validated_data['whatsapp'],
            estado=self.validated_data['estado'],
            idRol=self.validated_data['idRol']
        )
        password = self.validated_data['password']
        usuario.set_password(password)
        usuario.save()
        return usuario


class UsuarioImagenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuarios
        fields = ['imagen', 'updated_at']


class UsuarioFiltroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ['id', 'nombres', 'apellidos']

    def to_representation(self, instance):
        data = super(UsuarioFiltroSerializer, self).to_representation(instance)
        # tomo y uno los nombres y apellidos y los asigno a la data como nombre
        nombreCompleto = str(data.pop('nombres')) + " " + str(data.pop('apellidos'))
        data.update({"nombre": nombreCompleto})
        return data


class UsuarioResource(resources.ModelResource):
    class Meta:
        model = Usuarios
        exclude = ('id', 'idPadre', 'password', 'last_login', 'imagen', 'idRol', 'created_at', 'updated_at', 'state')

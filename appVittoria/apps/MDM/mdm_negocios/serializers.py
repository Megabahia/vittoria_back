from rest_framework import serializers
from import_export import resources

from .models import Negocios, DireccionesEstablecimientosNegocios, PersonalNegocios


# NEGOCIOS
class NegociosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Negocios
        fields = '__all__'


# LISTAR NEGOCIOS
class NegociosListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Negocios
        fields = ['id', 'nombreComercial', 'razonSocial', 'imagen']


# SUBIR IMAGEN
class NegociosImagenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Negocios
        fields = ['imagen', 'updated_at']


# DIRECCIONES ESTABLECIMIENTOS
class DireccionesEstablecimientosNegociosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DireccionesEstablecimientosNegocios
        fields = '__all__'


# PERSONAL NEGOCIOS
class PersonalNegociosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalNegocios
        fields = '__all__'


class NegocioPrediccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Negocios
        fields = ['id', 'nombreComercial', 'correoPersonal', 'ruc', 'estado', 'paisOrigen', 'imagen']


class NegociosResource(resources.ModelResource):
    class Meta:
        model = Negocios
        exclude = ('id', 'created_at', 'updated_at', 'state')

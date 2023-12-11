from rest_framework import serializers
from import_export import resources

from .models import ProspectosClientes


# UTILIZO CREATE, UPDATE, RETRIEVE
class ProspectosClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProspectosClientes
        fields = '__all__'


class ProspectosClientesSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProspectosClientes
        fields = ['id', 'nombres', 'apellidos', 'telefono', 'identificacion', 'whatsapp', 'codigoProducto',
                  'nombreProducto', 'precio']


class ProspectosClientesListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProspectosClientes
        fields = ['id', 'nombres', 'apellidos', 'whatsapp', 'correo1', 'correo2', 'ciudad', 'codigoProducto',
                  'created_at']


class ProspectosClienteImagenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProspectosClientes
        fields = ['imagen', 'updated_at']


class ProspectosClientesResource(resources.ModelResource):
    class Meta:
        model = ProspectosClientes
        exclude = ('id', 'created_at', 'updated_at', 'state')

from rest_framework import serializers
from import_export import resources

from .models import GdParametrizaciones


class GdParametrizacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GdParametrizaciones
        fields = '__all__'


class GdParametrizacionesHijoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GdParametrizaciones
        fields = ['id', 'nombre', 'valor']


class GdParametrizacionesListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GdParametrizaciones
        fields = ['id', 'nombre', 'tipo', 'tipoVariable', 'valor', 'descripcion']


class GdParametrizacionesFiltroSerializer(serializers.ModelSerializer):
    class Meta:
        model = GdParametrizaciones
        fields = ['id', 'nombre', 'valor']


class GdParametrizacionesTipoSerializer(serializers.ModelSerializer):
    # asignamos como nombre al dato tipo en la bd
    valor = serializers.CharField(source='tipo')

    class Meta:
        model = GdParametrizaciones
        fields = ['id', 'valor']


class GdParametrizacionesResource(resources.ModelResource):
    class Meta:
        model = GdParametrizaciones
        exclude = ('id', 'created_at', 'updated_at', 'state')

from rest_framework import serializers
from import_export import resources

from .models import Parametrizaciones


class ParametrizacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametrizaciones
        fields = '__all__'


class ParametrizacionesHijoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametrizaciones
        fields = ['id', 'nombre', 'valor']


class ParametrizacionesListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametrizaciones
        fields = ['id', 'nombre', 'tipo', 'tipoVariable', 'valor', 'descripcion', 'maximo', 'minimo']


class ParametrizacionesFiltroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametrizaciones
        fields = ['id', 'nombre', 'valor', 'archivo']


class ParametrizacionesTipoSerializer(serializers.ModelSerializer):
    # asignamos como nombre al dato tipo en la bd
    valor = serializers.CharField(source='tipo')

    class Meta:
        model = Parametrizaciones
        fields = ['id', 'valor']


class ParametrizacionesResource(resources.ModelResource):
    class Meta:
        model = Parametrizaciones
        exclude = ('id', 'idPadre', 'created_at', 'updated_at', 'state')

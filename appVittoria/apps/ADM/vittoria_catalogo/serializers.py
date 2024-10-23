from rest_framework import serializers
from import_export import resources

from .models import Catalogo


class CatalogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
        fields = '__all__'


class CatalogoHijoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
        fields = ['id', 'nombre', 'valor']


class CatalogoListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
        fields = ['id', 'nombre', 'tipo', 'tipoVariable', 'valor', 'descripcion', 'tiempo_entrega', 'canal']


class CatalogoFiltroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
        fields = ['id', 'nombre', 'valor']


class CatalogoTipoSerializer(serializers.ModelSerializer):
    # asignamos como nombre al dato tipo en la bd
    valor = serializers.CharField(source='tipo')

    class Meta:
        model = Catalogo
        fields = ['id', 'valor']


class CatalogoResource(resources.ModelResource):
    class Meta:
        model = Catalogo
        exclude = ('id', 'idPadre', 'created_at', 'updated_at', 'state')

from rest_framework import serializers

from apps.ADM.vittoria_catalogo.models import Catalogo


class CatalogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
       	fields = '__all__'

class CatalogoHijoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
       	fields = ['id','valor']

class CatalogoListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
       	fields = ['id','nombre','tipo','tipoVariable','valor','descripcion']


class CatalogoFiltroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
       	fields = ['id','valor']

class CatalogoTipoSerializer(serializers.ModelSerializer):
    #asignamos como nombre al dato tipo en la bd
    valor = serializers.CharField(source='tipo')
    class Meta:
        model = Catalogo
       	fields = ['valor']
    




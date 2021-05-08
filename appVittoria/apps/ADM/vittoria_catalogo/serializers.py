from rest_framework import serializers

from apps.ADM.vittoria_catalogo.models import Catalogo


class CatalogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
       	fields = '__all__'

class CatalogoHijoSerializer(serializers.ModelSerializer):
    idTipo = serializers.CharField(source='idPadre.id', read_only=True)
    class Meta:
        model = Catalogo
       	fields = ['id','nombre','idTipo','descripcion']

class CatalogoFiltroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
       	fields = ['id','nombre']

class CatalogoTipoSerializer(serializers.ModelSerializer):
    #asignamos como nombre al dato tipo en la bd
    nombre = serializers.CharField(source='tipo')
    class Meta:
        model = Catalogo
       	fields = ['id','nombre']
    




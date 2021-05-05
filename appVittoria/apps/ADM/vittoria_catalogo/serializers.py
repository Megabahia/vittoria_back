from rest_framework import serializers

from apps.ADM.vittoria_catalogo.models import Catalogo


class CatalogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
       	fields = '__all__'

class CatalogoTipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
       	fields = ['id','codigo','nombre']





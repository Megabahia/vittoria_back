from rest_framework import serializers

from apps.GDO.gdo_parametrizaciones.models import Parametrizaciones


class ParametrizacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametrizaciones
       	fields = '__all__'

class ParametrizacionesHijoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametrizaciones
       	fields = ['id','nombre','valor']

class ParametrizacionesListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametrizaciones
       	fields = ['id','nombre','tipo','tipoVariable','valor','descripcion']


class ParametrizacionesFiltroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametrizaciones
       	fields = ['id','nombre','valor']

class ParametrizacionesTipoSerializer(serializers.ModelSerializer):
    #asignamos como nombre al dato tipo en la bd
    valor = serializers.CharField(source='tipo')
    class Meta:
        model = Parametrizaciones
       	fields = ['id','valor']
    




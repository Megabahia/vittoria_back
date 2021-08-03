from rest_framework import serializers

from apps.MDO.mdo_prediccionCrosseling.models import PrediccionCrosseling, Detalles

import requests
import datetime

# Listar predicciones crosseling
class PrediccionCrosselingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrediccionCrosseling
       	fields = '__all__'

# Guardar Factura
class DetallesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalles
       	fields = '__all__'

class PrediccionCrosselingSerializer(serializers.ModelSerializer):
    detalles = DetallesSerializer(many=True)

    class Meta:
        model = PrediccionCrosseling
       	fields = '__all__'

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        validated_data["fechaPredicciones"] = datetime.datetime.now().date()
        prediccionCrosseling = PrediccionCrosseling.objects.create(**validated_data)
        for detalle_data in detalles_data:
            Detalles.objects.create(prediccionCrosseling=prediccionCrosseling, **detalle_data)
        return prediccionCrosseling

# Detalles con imagenes
class DetallesImagenesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalles
       	fields = '__all__'

    def to_representation(self, instance):
        print(instance)
        auth_data = {'codigo': str(instance.codigo)}
        resp = requests.post('http://127.0.0.1:8000/mdp/productos/producto/image/', data=auth_data)
        data = super(DetallesImagenesSerializer, self).to_representation(instance)
        if resp.json()['imagen']:
            data['imagen'] = resp.json()['imagen']
        return data



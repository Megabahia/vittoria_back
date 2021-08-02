from rest_framework import serializers

from apps.MDO.mdo_prediccionCrosseling.models import PrediccionCrosseling, Detalles

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

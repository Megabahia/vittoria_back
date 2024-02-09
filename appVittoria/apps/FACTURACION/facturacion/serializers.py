from rest_framework import serializers

from .models import (
    ArchivosFacturas, FacturasEncabezados, FacturasDetalles
)


class ArchivosFacturasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivosFacturas
        fields = '__all__'


class FacturasListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturasEncabezados
        fields = '__all__'


class FacturasDetallesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = FacturasDetalles
        fields = '__all__'


class FacturasSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    detalles = FacturasDetallesSerializer(many=True, allow_empty=False)

    class Meta:
        model = FacturasEncabezados
        fields = '__all__'

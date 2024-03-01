from rest_framework import serializers

from .models import Pedidos


class PedidosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedidos
        fields = '__all__'


class CreateOrderSerializer(serializers.Serializer):
    estado = serializers.CharField(max_length=255)
    envioTotal = serializers.FloatField()
    total = serializers.FloatField()
    facturacion = serializers.JSONField()
    envio = serializers.JSONField()
    metodoPago = serializers.CharField(max_length=255, )
    numeroPedido = serializers.CharField(max_length=255, )
    articulos = serializers.JSONField()
    envios = serializers.JSONField()
    json = serializers.JSONField()
    canal = serializers.CharField(max_length=255)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Pedidos.objects.create(**validated_data)
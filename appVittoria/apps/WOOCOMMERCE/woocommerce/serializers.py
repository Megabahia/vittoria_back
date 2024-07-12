from rest_framework import serializers

from .models import Pedidos
from ...ADM.vittoria_usuarios.models import Usuarios
from ...WOOCOMMERCE.woocommerce.models import Productos as ProductosBodega


class PedidosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedidos
        fields = '__all__'

    def to_representation(self, instance):
        data = super(PedidosSerializer, self).to_representation(instance)
        user = Usuarios.objects.filter(username=data['facturacion']['codigoVendedor']).first()
        if user:
            data['nombreVendedor'] = user.nombres + ' ' + user.apellidos
            data['companiaVendedor'] = user.compania
        else:
            data['nombreVendedor'] = ''
            data['companiaVendedor'] = ''

        return data


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
    gestion_pedido = serializers.CharField(max_length=155)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Pedidos.objects.create(**validated_data)

class ProductosBodegaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductosBodega
        fields = '__all__'

    def to_representation(self, instance):
        data = super(ProductosBodegaListSerializer, self).to_representation(instance)
        pedido = Pedidos.objects.filter(id=data['pedido']).first()
        if pedido:
            data['fechaPedido'] = pedido.created_at
            data['canalPedido'] = pedido.canal
        else:
            data['fechaPedido'] = ''
            data['canalPedido'] = ''

        return data
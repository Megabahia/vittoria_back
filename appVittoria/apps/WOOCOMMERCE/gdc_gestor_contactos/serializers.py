from rest_framework import serializers

from .models import Contactos
from ...ADM.vittoria_usuarios.models import Usuarios


class ContactosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contactos
        fields = '__all__'

    def to_representation(self, instance):
        data = super(ContactosSerializer, self).to_representation(instance)
        user = Usuarios.objects.filter(username=data['facturacion']['codigoVendedor']).first()
        if user:
            data['nombreVendedor'] = user.nombres + ' ' + user.apellidos
            data['companiaVendedor'] = user.compania
        else:
            data['nombreVendedor'] = ''
            data['companiaVendedor'] = ''

        return data


class CreateContactSerializer(serializers.Serializer):
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
        return Contactos.objects.create(**validated_data)


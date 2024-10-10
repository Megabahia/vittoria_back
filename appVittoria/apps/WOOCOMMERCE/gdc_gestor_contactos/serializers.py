from rest_framework import serializers
import requests
import base64

from ...ADM.vittoria_integraciones.models import Integraciones
from .models import Contactos
from ...ADM.vittoria_usuarios.models import Usuarios
from ...ADM.vittoria_integraciones.serializers import IntegracionesSerializer

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
    subtotal = serializers.FloatField()
    facturacion = serializers.JSONField()
    envio = serializers.JSONField()
    metodoPago = serializers.CharField(max_length=255, )
    numeroPedido = serializers.CharField(max_length=255, )
    articulos = serializers.JSONField()
    envios = serializers.JSONField()
    json = serializers.JSONField()
    canal = serializers.CharField(max_length=255)
    comision = serializers.FloatField(required=False, allow_null=True)
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Contactos.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super(CreateContactSerializer, self).to_representation(instance)

        articulos = data.pop('articulos')
        articulosModificado = []
        if articulos:
            for articulo in articulos:
                url = articulo['imagen_principal']
                if url is not None:
                    response = requests.get(url)
                    b64_encoded = base64.b64encode(response.content)
                    # Convertir bytes a string y retornar
                    imagen = b64_encoded.decode('utf-8')
                else:
                    imagen = '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'

                articulosModificado.append({
                    **articulo,
                    "imagen_principal": f"data:image/jpg;base64,{imagen}"
                })


        data['articulos'] = articulosModificado
        return data

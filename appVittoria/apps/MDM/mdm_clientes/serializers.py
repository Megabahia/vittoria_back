from rest_framework import serializers

from apps.MDM.mdm_clientes.models import Clientes, DatosFisicosClientes, DatosVirtualesClientes, Parientes


class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
       	fields = '__all__'

class ClientesListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
       	fields = ['id','nombres','apellidos','imagen']

class ClienteImagenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Clientes
        fields = ['imagen','updated_at']

class DatosFisicosClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosFisicosClientes
       	fields = '__all__'

class DatosVirtualesClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosVirtualesClientes
       	fields = '__all__'

class ParientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parientes
       	fields = '__all__'


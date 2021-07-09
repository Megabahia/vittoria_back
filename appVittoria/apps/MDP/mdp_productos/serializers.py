from rest_framework import serializers

from apps.MDP.mdp_productos.models import Productos


class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
       	fields = '__all__'

class ProductosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
       	fields = ['id','codigoBarras','nombre','categoria','subCategoria','stock','estado']
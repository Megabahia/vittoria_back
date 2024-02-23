from rest_framework import serializers
from import_export import resources

from .models import (
    ArchivosFacturas, Productos, ProductosImagenes
)


class ArchivosFacturasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivosFacturas
        fields = '__all__'


class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = '__all__'

    def to_representation(self, instance):
        data = super(ProductosSerializer, self).to_representation(instance)
        images = ProductosImagenes.objects.filter(producto=data['id'])
        if images:
            data['imagenes'] = ProductosImagenesSerializer(images,many=True).data
        else:
            data['imagenes'] = []
        return data


class ProductosResource(resources.ModelResource):
    class Meta:
        model = Productos
        exclude = ('id', 'created_at', 'updated_at', 'state')

class ProveedoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = ['proveedor']

class ProductosImagenesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductosImagenes
        fields = ['imagen']
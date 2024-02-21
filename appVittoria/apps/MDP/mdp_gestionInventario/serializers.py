from rest_framework import serializers
from import_export import resources

from .models import (
    ArchivosFacturas, Productos,
)


class ArchivosFacturasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivosFacturas
        fields = '__all__'


class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = '__all__'


class ProductosResource(resources.ModelResource):
    class Meta:
        model = Productos
        exclude = ('id', 'created_at', 'updated_at', 'state')

class ProveedoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = ['proveedor']